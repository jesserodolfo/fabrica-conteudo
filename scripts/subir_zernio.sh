#!/bin/bash
# Sobe um arquivo pro Zernio usando a URL assinada que o MCP devolve (media_get_media_presigned_url).
# Uso: scripts/subir_zernio.sh arquivo.jpg "UPLOAD_URL"
# Depois use a publicUrl no posts_create, na ordem dos slides.
set -e
f="$1"; url="$2"
case "$f" in *.jpg|*.jpeg) t=image/jpeg;; *.png) t=image/png;; *.mp4) t=video/mp4;; *) t=application/octet-stream;; esac
code=$(curl -sS -X PUT -H "Content-Type: $t" --data-binary @"$f" -o /dev/null -w "%{http_code}" "$url")
[ "$code" = "200" ] && echo "ok $f" || { echo "falhou $f ($code)"; exit 1; }
