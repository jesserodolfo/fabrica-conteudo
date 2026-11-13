"""Agenda no LinkedIn (Zernio REST, conta 6af20e7ac552269948f1684e) os itens 4 a 56 da fila.

Uso: .venv/bin/python -I scripts/linkedin/agendar_resto.py [--so-validar] [ordens...]
  --so-validar: só valida no endpoint de validação, não cria nada.
Chave lida do .env (ZERNIO_LINKEDIN_API_KEY), nunca impressa.
Grava em pesquisa/linkedin/fila.json: linkedin_post_id, horario_linkedin_brt, status, presente usado.
Grava legenda_linkedin.txt e first_comment.txt em cada pasta de item.
"""
import datetime as dt
import json
import pathlib
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from textos_resto import APLICACAO, TEXTOS, URL_OVERRIDE  # noqa: E402

ROOT = pathlib.Path("/Users/dmelo/Documents/03-Marketing/fabrica-conteudo")
FILA = ROOT / "pesquisa/linkedin/fila.json"
ACCOUNT_ID = "6af20e7ac552269948f1684e"
BASE = "https://zernio.com/api/v1"
BRT = dt.timezone(dt.timedelta(hours=-3))
APLIC_BASE = "https://jesserodolfo.com.br/aplicacao"


def chave():
    for linha in (ROOT / ".env").read_text().splitlines():
        if linha.startswith("ZERNIO_LINKEDIN_API_KEY="):
            return linha.split("=", 1)[1].strip()
    raise SystemExit("ZERNIO_LINKEDIN_API_KEY ausente no .env")


KEY = chave()


def api(metodo, caminho, corpo=None):
    dados = json.dumps(corpo).encode() if corpo is not None else None
    req = urllib.request.Request(
        BASE + caminho,
        data=dados,
        method=metodo,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


def slug(it):
    return sem_acento(it["palavra"]).replace(" ", "-") if it.get("palavra") else "sem-palavra"


def uuid_de(url):
    m = re.findall(r"([0-9a-f]{32})", url)
    if not m:
        return None
    h = m[-1]
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"


def notion_publico(url):
    bid = uuid_de(url)
    req = urllib.request.Request(
        "https://www.notion.so/api/v3/getPublicPageData",
        data=json.dumps({"type": "block-space", "name": "page", "blockId": bid}).encode(),
        headers={"content-type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        txt = r.read().decode("utf-8", "replace")
    m = re.search(r'"publicAccessRole":"([a-z_]*)"', txt)
    return bool(m and m.group(1) == "reader")


def url_presente(it):
    """Retorna a URL do firstComment ou None. Notion precisa estar público."""
    ordem = it["ordem"]
    if ordem in URL_OVERRIDE:
        url = URL_OVERRIDE[ordem]
    elif ordem in APLICACAO:
        url = f"{APLIC_BASE}?utm_source=linkedin&utm_medium=post&utm_content={slug(it)}"
    else:
        url = it.get("presente_url")
        if not url:
            return None
    if "notion" in url and not notion_publico(url):
        raise RuntimeError(f"presente Notion nao publico: {url}")
    return url


def titulo_documento(legenda):
    primeiro = legenda.split("\n\n")[0].strip()
    if len(primeiro) <= 100:
        return primeiro
    corte = primeiro[:100].rsplit(" ", 1)[0]
    return corte


def subir_pdf(caminho_pdf, nome):
    tamanho = caminho_pdf.stat().st_size
    st, r = api("POST", "/media/presign", {"filename": nome, "contentType": "application/pdf", "size": tamanho})
    if st != 200:
        raise RuntimeError(f"presign falhou {st}: {r}")
    req = urllib.request.Request(
        r["uploadUrl"], data=caminho_pdf.read_bytes(), method="PUT", headers={"Content-Type": "application/pdf"}
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        if resp.status != 200:
            raise RuntimeError(f"upload PDF falhou {resp.status}")
    return r["publicUrl"]


def tamanho_url(url):
    req = urllib.request.Request(url, method="HEAD")
    with urllib.request.urlopen(req, timeout=60) as r:
        return int(r.headers.get("Content-Length") or 0)


def preparar_midia(it, pasta):
    """Carrossel vira PDF hospedado; reel e misto usam o vídeo maior; imagem usa a própria URL."""
    tipo = it["tipo"]
    midias = it["midias"]
    if tipo == "carrossel":
        pasta_midia = pasta / "midia"
        pasta_midia.mkdir(parents=True, exist_ok=True)
        imgs = []
        for k, url in enumerate(midias, 1):
            ext = pathlib.Path(url.split("?")[0]).suffix.lower() or ".jpg"
            destino = pasta_midia / f"{k:02d}{ext}"
            if not destino.exists():
                destino.write_bytes(urllib.request.urlopen(url, timeout=120).read())
            imgs.append(Image.open(destino).convert("RGB"))
        pdf = pasta / "carrossel.pdf"
        imgs[0].save(pdf, "PDF", save_all=True, append_images=imgs[1:], resolution=72.0)
        publico = subir_pdf(pdf, f"linkedin-{it['ordem']:02d}-carrossel.pdf")
        return {"type": "document", "url": publico, "title": titulo_documento(TEXTOS[it["ordem"]]["legenda"])}, f"PDF {len(imgs)} paginas"
    if tipo == "imagem":
        return {"type": "image", "url": midias[0]}, "imagem"
    if tipo == "reel":
        return {"type": "video", "url": midias[0]}, "video"
    if tipo == "misto":
        videos = [u for u in midias if u.lower().split("?")[0].endswith(".mp4")]
        tamanhos = {u: tamanho_url(u) for u in videos}
        escolhido = max(tamanhos, key=tamanhos.get)
        return {"type": "video", "url": escolhido}, f"misto: usou o maior video ({tamanhos[escolhido]} bytes), descartou {len(midias) - 1} midias"
    raise RuntimeError(f"tipo desconhecido {tipo}")


def corpo_post(it, midia, fc, quando_brt):
    spec = {}
    if fc:
        spec["firstComment"] = fc
    if midia["type"] == "document":
        spec["documentTitle"] = midia["title"]
    return {
        "content": TEXTOS[it["ordem"]]["legenda"],
        "platforms": [{"platform": "linkedin", "accountId": ACCOUNT_ID, "platformSpecificData": spec}],
        "mediaItems": [midia],
        "scheduledFor": quando_brt.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "timezone": "America/Sao_Paulo",
        "publishNow": False,
    }


def pasta_do_item(it):
    return ROOT / "pesquisa/linkedin" / f"{it['data_ig_brt'][:10]}-{slug(it)}"


def processar(it, so_validar):
    ordem = it["ordem"]
    pasta = pasta_do_item(it)
    pasta.mkdir(parents=True, exist_ok=True)
    texto = TEXTOS[ordem]
    legenda = texto["legenda"]
    url = url_presente(it) if texto["fc"] else None
    fc = texto["fc"].format(URL=url) if url else None
    quando = dt.datetime.fromisoformat(it["horario_linkedin_brt"])

    midia, descricao = preparar_midia(it, pasta)
    (pasta / "legenda_linkedin.txt").write_text(legenda + "\n")
    (pasta / "first_comment.txt").write_text((fc or "") + ("\n" if fc else ""))

    corpo = corpo_post(it, midia, fc, quando)
    st, val = api("POST", "/tools/validate/post", corpo)
    if st != 200:
        return {"ok": False, "erro": f"validacao {st}: {str(val)[:300]}", "descricao": descricao}
    if so_validar:
        return {"ok": True, "validado": True, "descricao": descricao, "fc": fc, "url": url}
    st, cri = api("POST", "/posts", corpo)
    if st not in (200, 201):
        return {"ok": False, "erro": f"criacao {st}: {str(cri)[:300]}", "descricao": descricao}
    pid = (cri.get("post") or cri).get("_id") or cri.get("_id")
    return {"ok": True, "post_id": pid, "descricao": descricao, "fc": fc, "url": url, "midia": midia["type"]}


def verificar(pid, it, fc, midia_tipo):
    st, r = api("GET", f"/posts/{pid}")
    p = r.get("post", r)
    lp = p["platforms"][0]
    esperado = dt.datetime.fromisoformat(it["horario_linkedin_brt"]).astimezone(dt.timezone.utc)
    recebido = dt.datetime.fromisoformat(p["scheduledFor"].replace("Z", "+00:00"))
    problemas = []
    if p.get("status") != "scheduled":
        problemas.append(f"status {p.get('status')}")
    if recebido != esperado:
        problemas.append(f"horario {recebido} != {esperado}")
    if len(p.get("mediaItems", [])) != 1 or p["mediaItems"][0]["type"] != midia_tipo:
        problemas.append("midia")
    if (lp.get("platformSpecificData", {}).get("firstComment") or None) != (fc or None):
        problemas.append("firstComment")
    return problemas


def main(args):
    so_validar = "--so-validar" in args
    ordens_arg = [int(a) for a in args if a.isdigit()]
    fila = json.loads(FILA.read_text())
    resumo = []
    for it in fila["itens"]:
        o = it["ordem"]
        if o < 4 or (ordens_arg and o not in ordens_arg):
            continue
        if it.get("status") == "agendado" and not so_validar:
            continue
        try:
            res = processar(it, so_validar)
        except Exception as e:  # noqa: BLE001
            res = {"ok": False, "erro": f"excecao: {e}"}
        if res["ok"] and not so_validar:
            problemas = verificar(res["post_id"], it, res["fc"], "document" if it["tipo"] == "carrossel" else ("image" if it["tipo"] == "imagem" else "video"))
            it["linkedin_post_id"] = res["post_id"]
            it["status"] = "agendado" if not problemas else "agendado_com_alerta"
            it["linkedin_verificacao"] = problemas
            it["linkedin_presente_url"] = res["url"]
            it["linkedin_firstcomment"] = bool(res["fc"])
            it["linkedin_midia_nota"] = res["descricao"]
        elif not res["ok"]:
            it["status"] = "erro"
            it["linkedin_erro"] = res["erro"]
        it["horario_linkedin_brt"] = it["horario_linkedin_brt"]
        FILA.write_text(json.dumps(fila, ensure_ascii=False, indent=1))
        resumo.append((o, res))
        print(o, "OK" if res["ok"] else "ERRO", res.get("post_id") or res.get("erro"), res.get("descricao"), flush=True)
    print("total processados", len(resumo))


if __name__ == "__main__":
    main(sys.argv[1:])
