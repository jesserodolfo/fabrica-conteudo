#!/bin/bash
# Envia texto, vídeo ou foto no Telegram do Jessé pelo bot do projeto.
# Uso:
#   bash scripts/telegram_enviar.sh texto "mensagem"
#   bash scripts/telegram_enviar.sh video caminho.mp4 "legenda"
#   bash scripts/telegram_enviar.sh foto  caminho.jpg "legenda"
# Token e chat vêm do .env (TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID). A URL com o token vai por stdin do curl (-K -):
# nunca aparece na linha de comando, na lista de processos nem em log. Sai com erro se a resposta não tiver "ok":true.
# Botões (teclado inline), opcionais, por variável de ambiente:
#   TG_BOTOES="<data>|<slug>"   põe os 2 botões do lote: "✅ Aprovado" (ok|data|slug) e "✏️ Ajuste" (aj|data|slug)
#   TG_REPLY_MARKUP='{"inline_keyboard":[...]}'   teclado inline livre, em JSON
# Com sucesso imprime: ok: ... ("ok":true) message_id=<n> reply_markup=<sim|nao>
# Vídeo acima de 50 MB (limite do bot) é recomprimido com ffmpeg num arquivo temporário antes do envio.
set -uo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

MODO="${1:-}"
LIMITE=$((50 * 1024 * 1024))
ALVO_MB=46

uso() { echo "uso: telegram_enviar.sh texto \"mensagem\" | video caminho.mp4 \"legenda\" | foto caminho.jpg \"legenda\"" >&2; exit 2; }

# Lê só as duas variáveis do .env, sem carregar o resto e sem imprimir valor.
ler_env() {
  local v
  v="$(grep -m1 "^$1=" "$DIR/.env" 2>/dev/null | cut -d= -f2-)"
  v="${v%$'\r'}"; v="${v%\"}"; v="${v#\"}"; v="${v%\'}"; v="${v#\'}"
  printf '%s' "$v"
}
TOKEN="${TELEGRAM_BOT_TOKEN:-$(ler_env TELEGRAM_BOT_TOKEN)}"
CHAT="${TELEGRAM_CHAT_ID:-$(ler_env TELEGRAM_CHAT_ID)}"
if [ -z "$TOKEN" ] || [ -z "$CHAT" ]; then
  echo "ERRO: faltam TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID no .env" >&2; exit 1
fi

# Teclado inline opcional. callback_data aceita até 64 bytes.
MARKUP="${TG_REPLY_MARKUP:-}"
if [ -z "$MARKUP" ] && [ -n "${TG_BOTOES:-}" ]; then
  if [ "$(printf '%s' "aj|$TG_BOTOES" | wc -c)" -gt 64 ]; then
    echo "ERRO: TG_BOTOES passa de 64 bytes: $TG_BOTOES" >&2; exit 1
  fi
  case "$TG_BOTOES" in *\"*|*\\*) echo "ERRO: TG_BOTOES com caractere inválido" >&2; exit 1 ;; esac
  MARKUP="$(printf '{"inline_keyboard":[[{"text":"✅ Aprovado","callback_data":"ok|%s"},{"text":"✏️ Ajuste","callback_data":"aj|%s"}]]}' "$TG_BOTOES" "$TG_BOTOES")"
fi
MK_FORM=(); MK_DATA=()
if [ -n "$MARKUP" ]; then
  MK_FORM=(--form-string "reply_markup=$MARKUP")
  MK_DATA=(--data-urlencode "reply_markup=$MARKUP")
fi

TMP=""
trap '[ -n "$TMP" ] && rm -f "$TMP"' EXIT

# chamar <método> <tempo máximo> <argumentos do curl...>; imprime a resposta sem o token.
chamar() {
  local metodo="$1" tempo="$2"; shift 2
  printf 'url = "https://api.telegram.org/bot%s/%s"\n' "$TOKEN" "$metodo" \
    | curl -sS -K - --max-time "$tempo" "$@" 2>&1 \
    | sed "s|$TOKEN|***|g"
}

conferir() { # resposta, rótulo
  if printf '%s' "$1" | grep -q '"ok":true'; then
    local mid rm="nao"
    mid="$(printf '%s' "$1" | sed -n 's/.*"result":{"message_id":\([0-9][0-9]*\).*/\1/p' | head -1)"
    printf '%s' "$1" | grep -q '"reply_markup"' && rm="sim"
    echo "ok: $2 enviado (\"ok\":true) message_id=${mid:-?} reply_markup=$rm"
  else
    echo "ERRO: Telegram recusou $2. Resposta: $(printf '%s' "$1" | head -c 400)" >&2
    exit 1
  fi
}

case "$MODO" in
  texto)
    [ $# -ge 2 ] || uso
    # O Telegram aceita até 4096 caracteres por mensagem.
    MSG="$(printf '%s' "$2" | cut -c1-4000)"
    R="$(chamar sendMessage 30 --data-urlencode "chat_id=$CHAT" --data-urlencode "text=$MSG" --data-urlencode "disable_web_page_preview=true" ${MK_DATA[@]+"${MK_DATA[@]}"})"
    conferir "$R" "texto"
    ;;
  video)
    [ $# -ge 2 ] || uso
    ARQ="$2"; LEG="$(printf '%s' "${3:-}" | cut -c1-1000)"
    [ -f "$ARQ" ] || { echo "ERRO: vídeo não encontrado: $ARQ" >&2; exit 1; }
    TAM=$(stat -f%z "$ARQ")
    ENVIO="$ARQ"
    if [ "$TAM" -gt "$LIMITE" ]; then
      DUR="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$ARQ" | cut -d. -f1)"
      [ -n "$DUR" ] && [ "$DUR" -gt 0 ] || { echo "ERRO: não li a duração de $ARQ" >&2; exit 1; }
      # Bitrate de vídeo pra caber em ALVO_MB, com 128 kbps de áudio.
      VBR=$(( ALVO_MB * 8192 / DUR - 128 ))
      [ "$VBR" -lt 300 ] && VBR=300
      TMP="$(mktemp -t telegram_envio).mp4"
      echo "vídeo com $((TAM / 1048576)) MB passa de 50 MB: recomprimindo a ${VBR}k"
      ffmpeg -v error -y -i "$ARQ" -c:v libx264 -preset veryfast -b:v "${VBR}k" -maxrate "${VBR}k" -bufsize "$((VBR * 2))k" \
        -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart "$TMP" < /dev/null \
        || { echo "ERRO: ffmpeg falhou ao recomprimir $ARQ" >&2; exit 1; }
      ENVIO="$TMP"
      [ "$(stat -f%z "$ENVIO")" -le "$LIMITE" ] || { echo "ERRO: mesmo recomprimido passou de 50 MB" >&2; exit 1; }
    fi
    R="$(chamar sendVideo 600 -F "chat_id=$CHAT" -F "video=@\"$ENVIO\";type=video/mp4;filename=$(basename "$ARQ")" \
          --form-string "caption=$LEG" -F "supports_streaming=true" -F "width=1080" -F "height=1920" ${MK_FORM[@]+"${MK_FORM[@]}"})"
    conferir "$R" "vídeo $(basename "$ARQ")"
    ;;
  foto)
    [ $# -ge 2 ] || uso
    ARQ="$2"; LEG="$(printf '%s' "${3:-}" | cut -c1-1000)"
    [ -f "$ARQ" ] || { echo "ERRO: foto não encontrada: $ARQ" >&2; exit 1; }
    R="$(chamar sendPhoto 120 -F "chat_id=$CHAT" -F "photo=@\"$ARQ\"" --form-string "caption=$LEG" ${MK_FORM[@]+"${MK_FORM[@]}"})"
    conferir "$R" "foto $(basename "$ARQ")"
    ;;
  *) uso ;;
esac
