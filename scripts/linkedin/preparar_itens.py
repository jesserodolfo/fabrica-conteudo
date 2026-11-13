"""Baixa a midia de itens da fila em pesquisa/linkedin/<data>-<slug>/ e gera PDF se for carrossel.

Uso: .venv/bin/python -I scripts/linkedin/preparar_itens.py 1 2 3
Tamanho do PDF = tamanho original de cada slide (sem recorte nem redimensionamento).
"""
import json
import pathlib
import sys
import urllib.request

from PIL import Image

ROOT = pathlib.Path("/Users/dmelo/Documents/03-Marketing/fabrica-conteudo")
FILA = ROOT / "pesquisa/linkedin/fila.json"
SLUGS = {1: "planilha", 2: "cinco-metricas", 3: "crm-perguntas"}


def main(ordens):
    fila = json.loads(FILA.read_text())
    itens = {it["ordem"]: it for it in fila["itens"]}
    for n in ordens:
        it = itens[n]
        pasta = ROOT / "pesquisa/linkedin" / f"{it['data_ig_brt'][:10]}-{SLUGS[n]}"
        midia = pasta / "midia"
        midia.mkdir(parents=True, exist_ok=True)
        arquivos = []
        for k, url in enumerate(it["midias"], 1):
            ext = pathlib.Path(url.split("?")[0]).suffix.lower() or ".bin"
            destino = midia / f"{k:02d}{ext}"
            destino.write_bytes(urllib.request.urlopen(url, timeout=120).read())
            arquivos.append(destino)
        it["pasta_local_linkedin"] = str(pasta)
        if it["tipo"] == "carrossel":
            imgs = [Image.open(a).convert("RGB") for a in arquivos]
            pdf = pasta / "carrossel.pdf"
            imgs[0].save(pdf, "PDF", save_all=True, append_images=imgs[1:], resolution=72.0)
            print(f"ordem {n}: {len(imgs)} paginas {imgs[0].size} -> {pdf}")
        else:
            print(f"ordem {n}: {len(arquivos)} arquivo(s) {it['tipo']} -> {midia}")
    FILA.write_text(json.dumps(fila, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main([int(x) for x in sys.argv[1:]])
