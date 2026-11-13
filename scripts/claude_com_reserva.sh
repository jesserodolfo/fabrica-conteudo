#!/bin/bash
# Chama o Claude Code sem interface com tempo máximo e, se o modelo principal bater o LIMITE de uso,
# repete a mesma chamada com o modelo reserva (decisão do Jessé em 13/11/2026: Fable 5.2 > Opus 5.5).
# Não roda sozinho: é carregado com "source" por reels_teste.sh e ajustar_teste.sh.
#
# Uso:  claude_com_reserva <limite_s> <log> <modelo> <prompt> [opções do claude...]
# Devolve o status da última chamada (142 = estourou o tempo). Depois da chamada:
#   MODELO_USADO  = modelo que fez a última tentativa
#   TROCOU_MODELO = 1 se caiu no reserva, 0 se não
# Só troca quando a saída DESTA chamada tem a mensagem de limite; erro comum e tempo estourado não trocam.
# O reserva roda só com o tempo que sobrou. Se o reserva também bater o limite, devolve o erro dele.
MODELO_RESERVA="${MODELO_RESERVA:-claude-opus-5-5}"
CLAUDE_BIN="${CLAUDE_BIN:-claude}"
MODELO_USADO=""; TROCOU_MODELO=0

claude_com_reserva() {
  local limite="$1" log="$2" modelo="$3" prompt="$4"; shift 4
  local antes inicio status resto
  antes="$(wc -l < "$log" 2>/dev/null | tr -d ' ')"; antes="${antes:-0}"
  inicio="$(date +%s)"
  MODELO_USADO="$modelo"; TROCOU_MODELO=0
  perl -e 'alarm shift; exec @ARGV' "$limite" "$CLAUDE_BIN" -p "$prompt" --output-format text --model "$modelo" "$@" \
    < /dev/null >> "$log" 2>&1
  status=$?
  [ "$status" -eq 0 ] && return 0
  [ "$status" -eq 142 ] && return 142
  [ "$modelo" = "$MODELO_RESERVA" ] && return "$status"
  tail -n +"$((antes + 1))" "$log" 2>/dev/null | grep -qiE "reached your .*limit|usage limit" || return "$status"
  resto=$(( limite - ($(date +%s) - inicio) ))
  [ "$resto" -lt 600 ] && return "$status"
  echo "$(date '+%F %T') [reserva] $modelo bateu o limite de uso; repetindo com $MODELO_RESERVA (${resto}s restantes)" >> "$log"
  MODELO_USADO="$MODELO_RESERVA"; TROCOU_MODELO=1
  perl -e 'alarm shift; exec @ARGV' "$resto" "$CLAUDE_BIN" -p "$prompt" --output-format text --model "$MODELO_RESERVA" "$@" \
    < /dev/null >> "$log" 2>&1
}
