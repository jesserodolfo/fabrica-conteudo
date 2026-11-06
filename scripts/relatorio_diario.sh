#!/bin/bash
# Relatório diário do Analista (time do Instagram). Roda a skill relatorio-diario com o Claude Code sem interface
# e manda o resultado no Telegram. Idempotente: rodar de novo no mesmo dia sobrescreve o relatório.
# Uso: bash scripts/relatorio_diario.sh
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

export TZ="America/Sao_Paulo"
export PATH="/Users/dmelo/.local/bin:/Users/dmelo/.nvm/versions/node/v24.22.1/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

HOJE="$(date +%F)"
SAIDA="saidas/relatorios"
REL="$SAIDA/$HOJE.md"
LOG="$SAIDA/log-$HOJE.txt"
mkdir -p "$SAIDA"

avisar() { # titulo, texto
  osascript -e "display notification \"$2\" with title \"$1\"" >/dev/null 2>&1 || true
}

# Variáveis do Telegram (nunca imprimir os valores)
if [ -f "$DIR/.env" ]; then
  set -a; . "$DIR/.env"; set +a
fi

rm -f "$REL"

PROMPT="Use a skill relatorio-diario. Data de hoje: $HOJE (fuso de Brasília). Escreva saidas/relatorios/$HOJE.md e imprima o relatório."

# Timeout de 10 min (600 s) via perl, porque o macOS não tem o comando timeout.
set +e
perl -e 'alarm shift; exec @ARGV' 600 claude -p "$PROMPT" \
  --output-format text --model opus \
  --permission-mode dontAsk \
  --allowedTools "Skill" "Read" "Glob" "Grep" \
    "Edit(saidas/relatorios/*)" \
    "Edit(pesquisa/analista-aprendizados.md)" "WebSearch" \
    "Bash(date:*)" "Bash(TZ=America/Sao_Paulo date:*)" \
    "mcp__claude_ai_Zenio__posts_list" \
    "mcp__claude_ai_Zenio__posts_list_failed" \
    "mcp__claude_ai_Zenio__analytics_get_daily_metrics" \
    "mcp__claude_ai_Zenio__analytics_get_analytics" \
  < /dev/null > "$LOG" 2>&1
STATUS=$?
set -e

if [ "$STATUS" -ne 0 ] || [ ! -s "$REL" ]; then
  echo "Falhou (status $STATUS). Veja $LOG" >&2
  avisar "Relatório de conteúdo" "Falhou. Veja $LOG"
  exit 1
fi

echo "Relatório gerado: $REL"

if [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_CHAT_ID:-}" ]; then
  # A URL com o token vai por stdin (-K -) pra não aparecer na lista de processos.
  RESP="$(printf 'url = "https://api.telegram.org/bot%s/sendMessage"\n' "$TELEGRAM_BOT_TOKEN" \
    | curl -sS -K - --max-time 30 \
        --data-urlencode "chat_id=$TELEGRAM_CHAT_ID" \
        --data-urlencode "text@$REL" 2>&1 || true)"
  if printf '%s' "$RESP" | grep -q '"ok":true'; then
    echo "Enviado no Telegram."
  else
    echo "Telegram falhou (resposta sem ok). O relatório ficou em $REL" >&2
    avisar "Relatório de conteúdo" "Telegram falhou. Relatório em $REL"
    exit 1
  fi
else
  echo "Telegram não configurado (faltam TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID no .env). Envio pulado."
  avisar "Relatório de conteúdo pronto" "Telegram não configurado. Abra $REL"
fi
