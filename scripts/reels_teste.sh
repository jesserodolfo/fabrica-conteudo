#!/bin/bash
# Rotina noturna dos reels de teste (decisão docs/decisoes/2026-11-12-video-madrugada.md).
# Chama o Claude Code sem interface com a skill lote-teste (até 3 reels sem rosto da fila pesquisa/fila-testes.md)
# e DEPOIS o próprio shell lê o manifesto e manda os vídeos no Telegram. Nada é publicado em rede social.
# Uso:
#   bash scripts/reels_teste.sh                 rotina completa (launchd com.fusiongrowth.reels-teste, 23h00)
#   bash scripts/reels_teste.sh --ensaio        não chama o Claude nem gasta voz: manda 1 vídeo já pronto com o prefixo ENSAIO
#   bash scripts/reels_teste.sh --so-enviar [AAAA-MM-DD]   reenvia o que está pronto e ainda não foi enviado
# Cada vídeo pronto vai com 2 botões (Aprovado, Ajuste); quem ouve o toque é scripts/telegram_ouvir.py
# (launchd com.fusiongrowth.telegram-ouvir). O message_id de cada vídeo fica no manifesto.
# Idempotente: trava de execução única; vídeo já enviado fica marcado no manifesto (enviado: true) e não repete.
set -uo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

export TZ="America/Sao_Paulo"
export PATH="/Users/dmelo/.local/bin:/Users/dmelo/.nvm/versions/node/v24.22.1/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export HOME="${HOME:-/Users/dmelo}"

MODO="rotina"; DATA_ARG=""
case "${1:-}" in
  "") ;;
  --ensaio) MODO="ensaio" ;;
  --so-enviar) MODO="so-enviar"; DATA_ARG="${2:-}" ;;
  *) echo "uso: reels_teste.sh [--ensaio | --so-enviar [AAAA-MM-DD]]" >&2; exit 2 ;;
esac

SAIDA="saidas/lote-teste"
FILA="pesquisa/fila-testes.md"
MODELO="claude-fable-5-2"
LIMITE_S=19800   # 5 h 30
TG="${REELS_TESTE_TG:-$DIR/scripts/telegram_enviar.sh}"   # REELS_TESTE_TG troca o enviador em teste
PY="$DIR/.venv/bin/python"; [ -x "$PY" ] || PY="/usr/bin/python3"
mkdir -p "$SAIDA"

# Tudo que o script imprime também fica em saidas/lote-teste/launchd.log.
exec > >(tee -a "$SAIDA/launchd.log") 2>&1 < /dev/null
dizer() { echo "$(date '+%F %T') [$MODO] $*"; }

avisar_mac() { osascript -e "display notification \"$2\" with title \"$1\"" >/dev/null 2>&1 || true; }

# (a) Trava de execução única. Trava de processo morto é assumida.
LOCK="$SAIDA/.lock"
if ! mkdir "$LOCK" 2>/dev/null; then
  OUTRO="$(cat "$LOCK/pid" 2>/dev/null || true)"
  if [ -n "$OUTRO" ] && kill -0 "$OUTRO" 2>/dev/null; then
    dizer "já tem uma execução rodando (pid $OUTRO). Saindo."
    exit 0
  fi
  dizer "trava antiga de processo morto (pid ${OUTRO:-?}). Assumindo."
  rm -rf "$LOCK"; mkdir "$LOCK" || { dizer "não consegui criar a trava"; exit 1; }
fi
echo $$ > "$LOCK/pid"
trap 'rm -rf "$LOCK"' EXIT
trap 'exit 130' INT TERM

# (b) Mac acordado enquanto este script viver.
caffeinate -i -w $$ &

# (c) Data alvo: o dia em que os vídeos vão ao ar. Depois de 12h é amanhã; de madrugada é hoje.
if [ -n "$DATA_ARG" ]; then
  ALVO="$DATA_ARG"
elif [ "$(date +%H)" -ge 12 ]; then
  ALVO="$(date -v+1d +%F)"
else
  ALVO="$(date +%F)"
fi
ALVO_BR="$(date -j -f %F "$ALVO" +%d/%m 2>/dev/null || echo "$ALVO")"

PREF=""
MAN="$SAIDA/$ALVO.json"
LOG="$SAIDA/log-$ALVO.txt"
if [ "$MODO" = "ensaio" ]; then PREF="ENSAIO · "; MAN="$SAIDA/ensaio-$ALVO.json"; fi

NFILA=0
[ -f "$FILA" ] && NFILA="$(grep -c '^## \[ \]' "$FILA" || true)"

tg() { bash "$TG" "$@"; }   # imprime "ok: ..." ou "ERRO: ..." (sem token) e devolve o status
CHAVE="$(basename "$MAN" .json)"   # vai no callback dos botões: ok|<chave>|<slug>. No ensaio é ensaio-AAAA-MM-DD.

# Lê e marca o manifesto. listar: uma linha por item (n, N, tipo, palavra, vídeo, capa, motivo), separada por TAB.
manifesto() {
  "$PY" - "$MAN" "$@" <<'PYEOF'
import json, os, sys
arq, op = sys.argv[1], sys.argv[2]
dados = json.load(open(arq, encoding="utf-8"))
itens = dados if isinstance(dados, list) else dados.get("videos", [])
limpa = lambda s: " ".join(str(s or "").replace(chr(8212), ",").replace(chr(8211), ",").split())
def texto(v):
    if isinstance(v, dict):
        return limpa(v.get("resultado", "")) + (": " + limpa("; ".join(map(str, v.get("itens", [])))) if v.get("itens") else "")
    return limpa(v)
reais = [i for i in itens if i.get("slug") != "fila"]
if op == "listar":
    for k, it in enumerate(itens):
        if it.get("enviado"):
            continue
        n = reais.index(it) + 1 if it in reais else 0
        regua, rev = texto(it.get("regua")), texto(it.get("revisor"))
        video, capa = it.get("video") or "", it.get("capa") or ""
        motivo = limpa(it.get("motivo"))
        tipo = "falhou"
        if it.get("slug") == "fila":
            tipo = "aviso"
        elif it.get("status") == "pronto":
            falta = []
            if not (video and os.path.isfile(video)): falta.append("vídeo não existe no disco")
            if not regua.upper().startswith("APROVADO"): falta.append("régua: " + (regua or "sem resultado"))
            if not rev.lower().startswith("aprovado"): falta.append("revisor: " + (rev or "sem resultado"))
            if falta:
                motivo = "; ".join(falta)
            else:
                tipo = "pronto"
        if tipo == "falhou" and not motivo:
            motivo = "; ".join(x for x in ("régua: " + regua if regua else "", "revisor: " + rev if rev else "") if x) or "sem motivo registrado"
        if not (capa and os.path.isfile(capa)): capa = ""
        print("\t".join([str(k), str(n), str(len(reais)), tipo, limpa(it.get("palavra")) or limpa(it.get("slug")) or "?", video or "-", capa or "-", motivo or "-", limpa(it.get("slug")) or "-"]))
elif op == "marcar":
    itens[int(sys.argv[3])]["enviado"] = True
    if len(sys.argv) > 4 and sys.argv[4].isdigit():
        itens[int(sys.argv[3])]["message_id"] = int(sys.argv[4])
    tmp = arq + ".tmp"
    json.dump(dados, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, arq)
PYEOF
}

# (f) Envio determinístico do manifesto. Devolve 0 se tudo que tentou chegou.
ENVIADOS=0; FALHAS_TG=0; PRONTOS=0
enviar_manifesto() {
  local k n total tipo palavra video capa motivo slug LISTA R MID
  if ! LISTA="$(manifesto listar)"; then
    dizer "manifesto ilegível: $MAN"
    tg texto "${PREF}Reels de teste: o manifesto $MAN está ilegível. Veja $LOG" || true
    FALHAS_TG=$((FALHAS_TG + 1)); return
  fi
  while IFS=$'\t' read -r k n total tipo palavra video capa motivo slug <&3; do
    [ -n "$k" ] || continue
    case "$tipo" in
      pronto)
        # A capa vai antes, pra o vídeo com os botões ficar por último na conversa.
        [ "$capa" != "-" ] && { tg foto "$capa" "${PREF}Capa do TESTE $n · $palavra" || FALHAS_TG=$((FALHAS_TG + 1)); }
        if R="$(TG_BOTOES="$CHAVE|$slug" tg video "$video" "${PREF}TESTE $n de $total · $palavra · régua aprovada · revisor aprovado")"; then
          echo "$R"
          MID="$(printf '%s' "$R" | sed -n 's/.*message_id=\([0-9][0-9]*\).*/\1/p' | tail -1)"
          manifesto marcar "$k" "${MID:-}"; ENVIADOS=$((ENVIADOS + 1)); PRONTOS=$((PRONTOS + 1))
        else
          echo "$R"
          FALHAS_TG=$((FALHAS_TG + 1))
        fi ;;
      falhou)
        if tg texto "${PREF}TESTE $n de $total · $palavra · FALHOU: $motivo"; then
          manifesto marcar "$k"; ENVIADOS=$((ENVIADOS + 1))
        else
          FALHAS_TG=$((FALHAS_TG + 1))
        fi ;;
      aviso)
        if tg texto "${PREF}Aviso da rotina: $motivo"; then manifesto marcar "$k"; else FALHAS_TG=$((FALHAS_TG + 1)); fi ;;
    esac
  done 3<<< "$LISTA"
}

fechar() {
  if [ "$PRONTOS" -gt 0 ]; then
    tg texto "${PREF}Toque em Aprovado ou Ajuste em cada vídeo. Aprovados saem hoje como Reel de teste (11h, 14h, 17h)." || FALHAS_TG=$((FALHAS_TG + 1))
  fi
  if [ "$FALHAS_TG" -gt 0 ]; then
    if [ "$MODO" = "ensaio" ]; then dizer "Telegram falhou em $FALHAS_TG envio(s). Corrija e rode de novo: bash scripts/reels_teste.sh --ensaio"
    else dizer "Telegram falhou em $FALHAS_TG envio(s). Rode: bash scripts/reels_teste.sh --so-enviar $ALVO"; fi
    avisar_mac "Reels de teste" "Telegram falhou. Rode --so-enviar"
    exit 1
  fi
  dizer "fim. $ENVIADOS item(ns) enviado(s). Manifesto: $MAN"
  exit 0
}

dizer "início. data alvo $ALVO, $NFILA pauta(s) na fila, manifesto $MAN"

# (h) Só reenviar o que está pronto e não foi enviado.
if [ "$MODO" = "so-enviar" ]; then
  [ -f "$MAN" ] || { dizer "não existe $MAN"; exit 1; }
  enviar_manifesto
  [ "$ENVIADOS" -eq 0 ] && [ "$FALHAS_TG" -eq 0 ] && dizer "nada a enviar em $MAN"
  fechar
fi

# (g) Ensaio: manifesto separado apontando pro vídeo que já existe.
if [ "$MODO" = "ensaio" ]; then
  EV="posts/2026-11-12-teste-planilha-caixa/saida/teste-saldo_v3.mp4"
  EC="posts/2026-11-12-teste-planilha-caixa/capa/capa-reel_v3.jpg"
  [ -f "$EV" ] || { dizer "vídeo do ensaio não existe: $EV"; exit 1; }
  "$PY" - "$MAN" "$EV" "$EC" <<'PYEOF'
import json, subprocess, sys
man, video, capa = sys.argv[1:4]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video],
                           capture_output=True, text=True).stdout or 0)
json.dump([{"slug": "saldo", "palavra": "SALDO", "pasta": "posts/2026-11-12-teste-planilha-caixa", "video": video, "capa": capa,
            "duracao": round(dur, 1), "regua": "APROVADO", "revisor": "aprovado", "status": "pronto",
            "motivo": "ensaio do envio, vídeo já existente", "enviado": False, "ensaio": True}],
          open(man, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
PYEOF
  tg texto "${PREF}Reels de teste: rotina começou, $NFILA pautas na fila. Isto é só o ensaio do envio, com 1 vídeo que já existe." || FALHAS_TG=$((FALHAS_TG + 1))
  enviar_manifesto
  fechar
fi

# (d) Aviso de início.
tg texto "Reels de teste: rotina começou, $NFILA pautas na fila (faço até 3). Vídeos pra $ALVO_BR chegam aqui quando ficarem prontos." || dizer "aviso de início não chegou no Telegram"

if [ "$NFILA" -eq 0 ]; then
  dizer "fila vazia ou ausente ($FILA). Nada a produzir."
  tg texto "Reels de teste: a fila ($FILA) está vazia ou não existe. Nada foi produzido esta noite." || true
  exit 0
fi

# (e) Claude Code sem interface, sem ferramenta de internet e sem MCP. Timeout via perl (o macOS não tem timeout).
PROMPT="Use a skill lote-teste. data=$ALVO fila=$FILA. Produza até 3 reels de teste, um por vez, e grave o manifesto saidas/lote-teste/$ALVO.json depois de cada vídeo. Rotina noturna sem ninguém pra responder: não pergunte nada, não publique nada, não use a internet."
# Sem teto de espera por agente em segundo plano (o padrão de 10 min derrubou o Editor em 16/11/2026).
# O teto de verdade continua sendo LIMITE_S. Decisão: docs/decisoes/2026-11-17-lote-teste-modelo-novo.md
export CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0
source "$DIR/scripts/claude_com_reserva.sh"   # limite do Fable: repete com o Opus 5.5
claude_com_reserva "$LIMITE_S" "$LOG" "$MODELO" "$PROMPT" \
  --permission-mode dontAsk --strict-mcp-config \
  --allowedTools "Skill" "Read" "Write" "Edit" "Glob" "Grep" "Agent" "Task" "Bash"
STATUS=$?
[ "$TROCOU_MODELO" -eq 1 ] && { dizer "limite do $MODELO: continuou com $MODELO_USADO"; tg texto "Reels de teste: o Fable bateu o limite de uso. A rotina continuou com o Opus 5.5 de onde parou." || true; }
dizer "Claude terminou com status $STATUS (142 = estourou 5 h 30). Log: $LOG"

if [ "$STATUS" -eq 142 ]; then
  tg texto "Reels de teste: a rotina passou de 5 h 30 e foi interrompida. Segue o que ficou pronto." || true
elif [ "$STATUS" -ne 0 ]; then
  tg texto "Reels de teste: o Claude saiu com erro (status $STATUS). Segue o que ficou pronto. Log: $LOG" || true
fi

if [ ! -s "$MAN" ]; then
  dizer "sem manifesto em $MAN"
  tg texto "Reels de teste: a rotina não gravou o manifesto ($MAN). Nenhum vídeo pronto. Veja $LOG" || true
  avisar_mac "Reels de teste" "Sem manifesto. Veja $LOG"
  exit 1
fi

enviar_manifesto
fechar
