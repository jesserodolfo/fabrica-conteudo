#!/usr/bin/env python3
"""Sobe arquivos pro Zernio direto pela API (presign + PUT) e devolve as URLs públicas.

Existe pra tirar o upload da mão do modelo: publicar_teste.sh e publicar_perfil.sh chamam este
script ANTES de chamar o Claude e passam as URLs prontas no pedido. Sem Bash do modelo, sem "Bash negado".

Uso:  .venv/bin/python scripts/zernio_subir.py <arquivo> [<arquivo> ...]
Saída (última linha, JSON):
  {"ok": true, "urls": {"<arquivo>": "<publicUrl>", ...}}
  {"ok": false, "erro": "..."}
Idempotente: rodar de novo sobe de novo e devolve URLs novas; nada é criado além da mídia.
Só biblioteca padrão. A chave (ZERNIO_API_KEY do .env) nunca é impressa.
"""
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BASE = "https://zernio.com/api/v1"
TIPOS = {".mp4": "video/mp4", ".mov": "video/quicktime", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}
TENTATIVAS = 3


def chave():
    for linha in (RAIZ / ".env").read_text().splitlines():
        if linha.startswith("ZERNIO_API_KEY="):
            return linha.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def sair(d):
    print(json.dumps(d, ensure_ascii=False))
    sys.exit(0 if d.get("ok") else 1)


def presign(key, arq, tipo):
    corpo = json.dumps({"filename": arq.name, "contentType": tipo, "size": arq.stat().st_size}).encode()
    req = urllib.request.Request(BASE + "/media/presign", data=corpo, method="POST",
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return None, f"presign {e.code}: {e.read()[:300].decode('utf-8', 'replace')}"
    except Exception as e:
        return None, f"presign falhou: {type(e).__name__}"
    if "uploadUrl" not in d or "publicUrl" not in d:
        return None, f"presign sem uploadUrl: {str(d)[:300]}"
    return d, ""


def enviar(url, arq, tipo):
    req = urllib.request.Request(url, data=arq.read_bytes(), method="PUT", headers={"Content-Type": tipo})
    try:
        with urllib.request.urlopen(req, timeout=900) as r:
            return "" if r.status == 200 else f"upload {r.status}"
    except urllib.error.HTTPError as e:
        return f"upload {e.code}"
    except Exception as e:
        return f"upload falhou: {type(e).__name__}"


def conferir(url, tamanho):
    """A URL pública tem que responder com o mesmo tamanho do arquivo local."""
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            n = r.headers.get("Content-Length")
            if r.status != 200:
                return f"conferência {r.status}"
            if n is not None and int(n) != tamanho:
                return f"tamanho diferente: {n} no Zernio, {tamanho} local"
            return ""
    except urllib.error.HTTPError as e:
        return f"conferência {e.code}"
    except Exception as e:
        return f"conferência falhou: {type(e).__name__}"


def subir(key, arq, tipo):
    erro = ""
    for n in range(1, TENTATIVAS + 1):
        d, erro = presign(key, arq, tipo)
        if d:
            erro = enviar(d["uploadUrl"], arq, tipo) or conferir(d["publicUrl"], arq.stat().st_size)
            if not erro:
                return d["publicUrl"], ""
        if n < TENTATIVAS:
            time.sleep(3 * n)
    return "", f"{arq.name}: {erro} (após {TENTATIVAS} tentativas)"


def main():
    nomes = sys.argv[1:]
    if not nomes:
        sair({"ok": False, "erro": "uso: zernio_subir.py <arquivo> [<arquivo> ...]"})
    key = chave()
    if not key:
        sair({"ok": False, "erro": "ZERNIO_API_KEY ausente no .env"})
    urls = {}
    for nome in nomes:
        arq = Path(nome) if Path(nome).is_absolute() else RAIZ / nome
        if not arq.is_file():
            sair({"ok": False, "erro": f"arquivo não existe: {nome}"})
        tipo = TIPOS.get(arq.suffix.lower())
        if not tipo:
            sair({"ok": False, "erro": f"tipo não aceito: {nome}"})
        url, erro = subir(key, arq, tipo)
        if erro:
            sair({"ok": False, "erro": erro})
        urls[nome] = url
    sair({"ok": True, "urls": urls})


if __name__ == "__main__":
    main()
