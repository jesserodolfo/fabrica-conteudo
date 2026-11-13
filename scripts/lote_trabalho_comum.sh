#!/bin/bash
# Parte comum dos trabalhos do lote de teste (publicar_teste.sh, ajustar_teste.sh, publicar_perfil.sh).
# Não roda sozinho: é carregado com "source". Define DIR, SAIDA, PY, TG, CHAVE, SLUG, ENSAIO, PREF e as funções.
# Uso no trabalho: source scripts/lote_trabalho_comum.sh "<nome do trabalho>" "$@"
set -uo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"
export TZ="America/Sao_Paulo"
export PATH="/Users/dmelo/.local/bin:/Users/dmelo/.nvm/versions/node/v24.22.1/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export HOME="${HOME:-/Users/dmelo}"

TRABALHO="$1"; shift
SAIDA="saidas/lote-teste"
PY="$DIR/.venv/bin/python"; [ -x "$PY" ] || PY="/usr/bin/python3"
TG="${REELS_TESTE_TG:-$DIR/scripts/telegram_enviar.sh}"
mkdir -p "$SAIDA"

ENSAIO=0; ARGS=()
for a in "$@"; do
  if [ "$a" = "--ensaio" ]; then ENSAIO=1; else ARGS+=("$a"); fi
done
CHAVE="${ARGS[0]:-}"; SLUG="${ARGS[1]:-}"; EXTRA="${ARGS[2]:-}"
case "$CHAVE" in ensaio-*) ENSAIO=1 ;; esac
PREF=""; [ "$ENSAIO" -eq 1 ] && PREF="ENSAIO · "

dizer() { echo "$(date '+%F %T') [$TRABALHO${PREF:+ ensaio}] $*"; }
tg() { bash "$TG" "$@"; }
campo() { "$PY" scripts/lote_comum.py campo "$CHAVE" "$SLUG" "$1" 2>/dev/null; }
gravar() { "$PY" scripts/lote_comum.py gravar "$CHAVE" "$SLUG" "$1"; }
# json_str "texto": devolve o texto como string JSON (com aspas), sem travessão.
json_str() { printf '%s' "$1" | "$PY" -c 'import json,sys; print(json.dumps(" ".join(sys.stdin.read().replace(chr(8212), ",").replace(chr(8211), ",").split()), ensure_ascii=False))'; }
# res <arquivo> <campo>: lê um campo do JSON de resultado que o Claude gravou (vazio se não tem).
res() { "$PY" -c 'import json,sys
try:
    v = json.load(open(sys.argv[1], encoding="utf-8")).get(sys.argv[2], "")
except Exception:
    v = ""
print("" if v is None else (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)))' "$1" "$2"; }

if ! "$PY" -c 'import sys; sys.path.insert(0, "scripts"); import lote_comum as l; sys.exit(0 if l.valido(sys.argv[1], sys.argv[2]) else 1)' "$CHAVE" "$SLUG"; then
  echo "uso: $TRABALHO.sh <chave AAAA-MM-DD> <slug> [...] [--ensaio]" >&2; exit 2
fi

# A rotina das 23h tem prioridade: se ela está rodando, este trabalho sai com 75 e o ouvinte tenta de novo.
if "$PY" scripts/lote_comum.py trava; then
  dizer "rotina das 23h rodando (saidas/lote-teste/.lock). Saindo com 75 pra tentar depois."
  exit 75
fi

# Um trabalho por vez (Mac de 8 GB). Trava de processo morto é assumida.
LOCKT="$SAIDA/.lock-trabalho"
if ! mkdir "$LOCKT" 2>/dev/null; then
  OUTRO="$(cat "$LOCKT/pid" 2>/dev/null || true)"
  if [ -n "$OUTRO" ] && kill -0 "$OUTRO" 2>/dev/null; then
    dizer "outro trabalho rodando (pid $OUTRO). Saindo com 75."
    exit 75
  fi
  rm -rf "$LOCKT"; mkdir "$LOCKT" || { dizer "não consegui criar a trava do trabalho"; exit 1; }
fi
echo $$ > "$LOCKT/pid"
trap 'rm -rf "$LOCKT"' EXIT
trap 'exit 130' INT TERM

PALAVRA="$(campo palavra)"; PASTA="$(campo pasta)"; VIDEO="$(campo video)"; CAPA="$(campo capa)"
if [ -z "$PASTA" ] || [ -z "$VIDEO" ]; then
  dizer "não achei $SLUG no manifesto $SAIDA/$CHAVE.json"
  tg texto "${PREF}$TRABALHO: não achei $SLUG no manifesto $CHAVE." || true
  exit 1
fi
PALAVRA="${PALAVRA:-$SLUG}"
