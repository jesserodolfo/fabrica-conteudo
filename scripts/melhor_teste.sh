#!/bin/bash
# Placar dos reels de teste, todo dia 09h30 (launchd com.fusiongrowth.melhor-teste).
# Lê as métricas (Zernio e Meta, só leitura), manda o placar de 24 h e 72 h no Telegram e os botões
# "Postar <PALAVRA> no perfil 18h" e "Hoje não". Regra do guia em scripts/melhor_teste.py.
# Uso: bash scripts/melhor_teste.sh [--ensaio] [--hoje AAAA-MM-DD] [--nao-enviar]
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"
export TZ="America/Sao_Paulo"
export PATH="/Users/dmelo/.local/bin:/Users/dmelo/.nvm/versions/node/v24.22.1/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export HOME="${HOME:-/Users/dmelo}"
mkdir -p saidas/lote-teste
{
  echo "$(date '+%F %T') [melhor_teste] início $*"
  "$DIR/.venv/bin/python" scripts/melhor_teste.py "$@"
  S=$?
  echo "$(date '+%F %T') [melhor_teste] fim, status $S"
  exit $S
} 2>&1 | tee -a saidas/lote-teste/melhor_teste.log
exit "${PIPESTATUS[0]}"
