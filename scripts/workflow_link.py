#!/usr/bin/env python3
"""Acrescenta (ou troca) a mensagem final com o link do presente num workflow de entrega do Zernio.

Uso:  .venv/bin/python scripts/workflow_link.py <workflow_id> <url_publica_notion.site>
Antes de mexer, confere pela API do Notion se a página está pública (publicAccessRole reader). Privada: sai com erro.
Idempotente: o nó tem id fixo "link"; rodar de novo só troca o texto. Entra logo antes do nó "end".
A chave (ZERNIO_API_KEY do .env) nunca é impressa.
"""
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BASE = "https://zernio.com/api/v1"
TEXTO = "O passo a passo completo de como usar, com as dicas, está aqui:\n{url}"


def chave():
    for linha in (RAIZ / ".env").read_text().splitlines():
        if linha.startswith("ZERNIO_API_KEY="):
            return linha.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("ZERNIO_API_KEY ausente no .env")


def api(metodo, caminho, corpo=None):
    req = urllib.request.Request(BASE + caminho, data=json.dumps(corpo).encode() if corpo is not None else None, method=metodo,
                                 headers={"Authorization": f"Bearer {chave()}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, {"erro": e.read()[:400].decode("utf-8", "replace")}


def publica(url):
    m = re.search(r"([0-9a-f]{32})(?:\?|$)", url)
    if not m or "notion.site" not in url:
        return False, "o link precisa ser o público (notion.site) e terminar no id da página"
    h = m.group(1)
    uid = f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"
    req = urllib.request.Request("https://www.notion.so/api/v3/getPublicPageData", method="POST",
                                 data=json.dumps({"type": "block-space", "name": "page", "blockId": uid}).encode(),
                                 headers={"content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        papel = json.loads(r.read()).get("publicAccessRole")
    return papel == "reader", f"publicAccessRole={papel}"


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    wid, url = sys.argv[1], sys.argv[2].split("?")[0]
    ok, motivo = publica(url)
    if not ok:
        sys.exit(f"ERRO: página não está pública ({motivo}). Nada foi alterado.")
    st, d = api("GET", f"/workflows/{wid}")
    if st != 200:
        sys.exit(f"ERRO ao ler o workflow: {st} {d}")
    w = d.get("workflow", d)
    nodes, edges = w["nodes"], w["edges"]
    fim = next(n["id"] for n in nodes if n["type"] == "end")
    texto = TEXTO.format(url=url)
    velho = next((n for n in nodes if n["id"] == "link"), None)
    if velho:
        velho["config"] = {"text": texto, "messageType": "text"}
    else:
        nodes.insert(len(nodes) - 1, {"id": "link", "type": "send_message", "config": {"text": texto, "messageType": "text"}})
        for e in edges:
            if e["target"] == fim:
                e["target"] = "link"
        edges.append({"id": "e-link", "source": "link", "target": fim})
    corpo = {"nodes": nodes, "edges": edges, "entryNodeId": w.get("entryNodeId")}
    st, r = api("PATCH", f"/workflows/{wid}", corpo)
    if st not in (200, 201):
        st, r = api("PUT", f"/workflows/{wid}", corpo)
    if st not in (200, 201):
        sys.exit(f"ERRO ao salvar: {st} {r}")
    st, d = api("GET", f"/workflows/{wid}")
    w = d.get("workflow", d)
    ordem, atual, mapa = [], w["entryNodeId"], {e["source"]: e["target"] for e in w["edges"]}
    while atual:
        ordem.append(atual)
        atual = mapa.get(atual)
    lk = next(n for n in w["nodes"] if n["id"] == "link")
    print(f"ok {w['name']} | status {w['status']} | ordem {' > '.join(ordem)} | link: {lk['config']['text'].splitlines()[-1]}")


if __name__ == "__main__":
    main()
