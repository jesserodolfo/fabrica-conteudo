#!/bin/bash
# Sobe o ouvinte do Telegram (scripts/telegram_ouvir.py) pelo launchd com.fusiongrowth.telegram-ouvir.
# O python roda como FILHO deste bash (sem exec) de propósito: quem tem permissão de ler ~/Documents no launchd
# é o /usr/local/bin/fusion-backup-bash, e os filhos herdam. Se o python cair, este script sai e o launchd sobe de novo.
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR" || exit 1
export TZ="America/Sao_Paulo"
export PATH="/Users/dmelo/.local/bin:/Users/dmelo/.nvm/versions/node/v24.22.1/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export HOME="${HOME:-/Users/dmelo}"
PY="$DIR/.venv/bin/python"; [ -x "$PY" ] || PY="/usr/bin/python3"
# Mantém o Mac acordado enquanto estiver na tomada (-s), pra o botão do Telegram responder na hora. Na bateria o Mac dorme normal.
caffeinate -s -w $$ &
"$PY" -u scripts/telegram_ouvir.py "$@"
