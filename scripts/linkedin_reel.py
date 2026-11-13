#!/usr/bin/env python3
"""Agenda um reel no LinkedIn pessoal do Jessé pela conta separada do Zernio (ZERNIO_LINKEDIN_API_KEY).

Decisão: docs/decisoes/2026-11-09-linkedin-retroativo.md (todo post do Instagram sai no LinkedIn no mesmo horário).
Uso (da raiz):
  .venv/bin/python scripts/linkedin_reel.py <pasta do post> <video.mp4> <AAAA-MM-DDTHH:MM hora de São Paulo>
  ... --so-validar [--url-midia URL]   só valida o corpo no Zernio (/tools/validate/post), não sobe nem cria nada
A legenda vem de <pasta>/legenda_linkedin.txt (texto corrido, até 3 hashtags, sem link, sem "comenta X").
Imprime uma linha JSON: {"ok": true, "post_id": "..."} ou {"ok": false, "erro": "..."}. A chave nunca é impressa.
Grava <pasta>/zernio_linkedin.txt com o ID. Idempotente: se o arquivo já tem ID, não cria outro.
"""
import datetime as dt
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ACCOUNT_ID = "6af20e7ac552269948f1684e"
BASE = "https://zernio.com/api/v1"
BRT = dt.timezone(dt.timedelta(hours=-3))


def chave():
    for linha in (RAIZ / ".env").read_text().splitlines():
        if linha.startswith("ZERNIO_LINKEDIN_API_KEY="):
            return linha.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def api(key, metodo, caminho, corpo=None):
    req = urllib.request.Request(BASE + caminho, data=json.dumps(corpo).encode() if corpo is not None else None,
                                 method=metodo, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read() or b"{}")
        except ValueError:
            return e.code, {}
    except Exception as e:
        return 0, {"error": type(e).__name__}


def sair(d):
    print(json.dumps(d, ensure_ascii=False))
    sys.exit(0 if d.get("ok") else 1)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    so_validar = "--so-validar" in sys.argv
    url_midia = sys.argv[sys.argv.index("--url-midia") + 1] if "--url-midia" in sys.argv else None
    if url_midia in args:
        args.remove(url_midia)
    if len(args) != 3:
        sair({"ok": False, "erro": "uso: linkedin_reel.py <pasta> <video> <AAAA-MM-DDTHH:MM> [--so-validar [--url-midia URL]]"})
    pasta, video, quando = RAIZ / args[0], RAIZ / args[1], args[2]
    key = chave()
    if not key:
        sair({"ok": False, "erro": "ZERNIO_LINKEDIN_API_KEY ausente no .env"})
    leg = pasta / "legenda_linkedin.txt"
    if not leg.is_file() or not leg.read_text(encoding="utf-8").strip():
        sair({"ok": False, "erro": f"falta {args[0]}/legenda_linkedin.txt"})
    texto = leg.read_text(encoding="utf-8").strip()
    if chr(8212) in texto or chr(8211) in texto:
        sair({"ok": False, "erro": "legenda_linkedin.txt tem travessão"})
    marca = pasta / "zernio_linkedin.txt"
    if not so_validar and marca.is_file() and marca.read_text().strip():
        sair({"ok": True, "post_id": marca.read_text().strip().split()[0], "ja_existia": True})
    if not video.is_file():
        sair({"ok": False, "erro": f"vídeo não existe: {args[1]}"})
    q = dt.datetime.fromisoformat(quando).replace(tzinfo=BRT)

    if so_validar:
        url = url_midia or "https://media.zernio.com/media/exemplo.mp4"
    else:
        st, r = api(key, "POST", "/media/presign", {"filename": video.name, "contentType": "video/mp4", "size": video.stat().st_size})
        if st != 200 or "uploadUrl" not in r:
            sair({"ok": False, "erro": f"presign {st}: {str(r)[:300]}"})
        req = urllib.request.Request(r["uploadUrl"], data=video.read_bytes(), method="PUT", headers={"Content-Type": "video/mp4"})
        try:
            with urllib.request.urlopen(req, timeout=600) as resp:
                if resp.status != 200:
                    sair({"ok": False, "erro": f"upload {resp.status}"})
        except Exception as e:
            sair({"ok": False, "erro": f"upload falhou: {type(e).__name__}"})
        url = r["publicUrl"]

    corpo = {
        "content": texto,
        "platforms": [{"platform": "linkedin", "accountId": ACCOUNT_ID, "platformSpecificData": {}}],
        "mediaItems": [{"type": "video", "url": url}],
        "scheduledFor": q.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "timezone": "America/Sao_Paulo",
        "publishNow": False,
    }
    st, val = api(key, "POST", "/tools/validate/post", corpo)
    if st != 200:
        sair({"ok": False, "erro": f"validação {st}: {str(val)[:300]}"})
    if so_validar:
        sair({"ok": True, "validado": True, "resposta": str(val)[:200]})
    st, cri = api(key, "POST", "/posts", corpo)
    if st not in (200, 201):
        sair({"ok": False, "erro": f"criação {st}: {str(cri)[:300]}"})
    pid = (cri.get("post") or cri).get("_id") or cri.get("_id")
    marca.write_text(f"{pid}\n")
    sair({"ok": True, "post_id": pid})


if __name__ == "__main__":
    main()
