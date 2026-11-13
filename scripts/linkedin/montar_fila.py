"""Monta pesquisa/linkedin/fila.json: posts do Instagram (Zernio) em ordem cronologica,
sem repostagem, com palavra, link do presente, checagem publica do Notion e horario LinkedIn.

Uso: .venv/bin/python -I scripts/linkedin/montar_fila.py
Chaves lidas do .env (nunca impressas).
"""
import datetime as dt
import json
import pathlib
import re
import unicodedata
import urllib.request

ROOT = pathlib.Path("/Users/dmelo/Documents/03-Marketing/fabrica-conteudo")
SAIDA = ROOT / "pesquisa/linkedin/fila.json"
BRT = dt.timezone(dt.timedelta(hours=-3))

# Repostagens removidas (fica a primeira). Motivo registrado no fila.json.
REMOVIDOS_MANUAL = {
    38: "reel NOTA (fio) repete o carrossel NOTA de 29/10 da manha: mesmo tema, mesma palavra, mesmo dia, legenda abre igual",
}


def ler_env():
    env = {}
    for linha in (ROOT / ".env").read_text().splitlines():
        if "=" in linha and not linha.lstrip().startswith("#"):
            k, v = linha.split("=", 1)
            env[k.strip()] = v.strip()
    return env


def get_json(url, chave):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {chave}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


def uuid_de(url):
    m = re.findall(r"([0-9a-f]{32})", url)
    if not m:
        return None
    h = m[-1]
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"


def presente_publico(url):
    """getPublicPageData do Notion: publicAccessRole 'reader' = publica."""
    bid = uuid_de(url)
    if not bid:
        return None, "sem id na URL"
    corpo = json.dumps({"type": "block-space", "name": "page", "blockId": bid}).encode()
    req = urllib.request.Request(
        "https://www.notion.so/api/v3/getPublicPageData",
        data=corpo,
        headers={"content-type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            txt = r.read().decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001
        return None, f"erro: {e}"
    m = re.search(r'"publicAccessRole":"([a-z_]*)"', txt)
    if not m:
        return None, "sem publicAccessRole na resposta"
    return m.group(1) == "reader", m.group(1)


def slots_linkedin(n):
    """10/11 so 12h e 18h (08h livre). Depois 08h, 12h, 18h por dia."""
    out = [dt.datetime(2026, 11, 10, 12, 0, tzinfo=BRT), dt.datetime(2026, 11, 10, 18, 0, tzinfo=BRT)]
    dia = dt.date(2026, 11, 11)
    while len(out) < n:
        for h in (8, 12, 18):
            out.append(dt.datetime(dia.year, dia.month, dia.day, h, 0, tzinfo=BRT))
        dia += dt.timedelta(days=1)
    return out[:n]


def tipo_de(tipos):
    if all(t == "video" for t in tipos):
        return "reel"
    if all(t == "image" for t in tipos):
        return "carrossel" if len(tipos) > 1 else "imagem"
    return "misto"


def main():
    env = ler_env()
    chave_ig = env["ZERNIO_API_KEY"]
    posts = []
    for pagina in (1, 2):
        d = get_json(f"https://zernio.com/api/v1/posts?status=published&limit=100&page={pagina}", chave_ig)
        posts += d["posts"]
    autos = get_json("https://zernio.com/api/v1/comment-automations", chave_ig)["automations"]

    ig = []
    for p in posts:
        pl = [x for x in p.get("platforms", []) if x.get("platform") == "instagram"]
        if not pl:
            continue
        x = pl[0]
        quando = x.get("publishedAt") or p.get("scheduledFor")
        ig.append({
            "zernio_post_id": p["_id"],
            "ig_post_id": x.get("platformPostId"),
            "quando_utc": quando,
            "midias": [m["url"] for m in p.get("mediaItems", [])],
            "tipos": [m["type"] for m in p.get("mediaItems", [])],
            "legenda": p.get("content") or "",
        })
    ig.sort(key=lambda r: r["quando_utc"] or "")

    fila, removidos = [], []
    for i, r in enumerate(ig, 1):
        if i in REMOVIDOS_MANUAL:
            removidos.append({"ordem_ig": i, "ig_post_id": r["ig_post_id"], "data_brt": r["quando_utc"], "motivo": REMOVIDOS_MANUAL[i]})
            continue
        r["ordem_ig"] = i
        fila.append(r)

    slots = slots_linkedin(len(fila))
    itens = []
    for n, r in enumerate(fila, 1):
        quando_brt = dt.datetime.fromisoformat(r["quando_utc"].replace("Z", "+00:00")).astimezone(BRT)
        # palavra = 1 ou 2 palavras em maiusculas depois de "Comenta" ("Comenta aí" nao conta)
        m = re.search(r'(?i:comenta)\s+"?([A-ZÀ-Ú0-9]{2,}(?: [A-ZÀ-Ú0-9]{2,})?)"?', r["legenda"])
        palavra = m.group(1) if m else None

        url_presente, origem = None, None
        if palavra:
            alvo = sem_acento(palavra)
            for a in autos:
                if a.get("postId") == r["zernio_post_id"] and a.get("buttons"):
                    url_presente, origem = a["buttons"][0]["url"], f"automacao por post: {a['name']}"
                    break
            if not url_presente:
                for a in autos:
                    kws = [sem_acento(k) for k in a.get("keywords", [])]
                    if not a.get("postId") and a.get("isActive") and alvo in kws and a.get("buttons"):
                        url_presente, origem = a["buttons"][0]["url"], f"automacao por palavra: {a['name']}"
                        break

        publico, status_pub = None, None
        if url_presente and "notion" in url_presente:
            publico, status_pub = presente_publico(url_presente)

        itens.append({
            "ordem": n,
            "ordem_ig": r["ordem_ig"],
            "id_ig": r["ig_post_id"],
            "id_zernio_post": r["zernio_post_id"],
            "data_ig_brt": quando_brt.strftime("%Y-%m-%d %H:%M"),
            "tipo": tipo_de(r["tipos"]),
            "midias": r["midias"],
            "legenda_original": r["legenda"],
            "palavra": palavra,
            "presente_url": url_presente,
            "presente_origem": origem,
            "presente_publico": publico,
            "presente_status_notion": status_pub,
            "horario_linkedin_brt": slots[n - 1].isoformat(),
            "pasta_local": None,
            "status": "pendente",
        })

    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(json.dumps({
        "gerado_em": dt.datetime.now(BRT).isoformat(),
        "total_ig": len(ig),
        "total_fila": len(itens),
        "removidos": removidos,
        "itens": itens,
    }, ensure_ascii=False, indent=1))
    print(f"ig={len(ig)} fila={len(itens)} removidos={len(removidos)}")


if __name__ == "__main__":
    main()
