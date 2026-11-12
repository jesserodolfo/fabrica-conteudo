#!/usr/bin/env python3
"""Apaga a mídia pesada de um post JÁ PUBLICADO (decisão docs/decisoes/2026-11-12-limpeza-videos-postados.md).

Uso:
  .venv/bin/python scripts/limpar_post.py posts/<pasta>                 # simulação, só lista
  .venv/bin/python scripts/limpar_post.py posts/<pasta> --apagar        # confere no Zernio e apaga
  O ID do post vem SÓ do zernio.txt da pasta (gravado pelo Publicador), nunca da linha de comando.
  ... --sem-zernio "motivo"          # retroativo sem ID, só com ok do Jessé; o motivo vai pro limpeza.md

Apaga: .mp4 .mov .m4a .wav .mp3 .webm em qualquer subpasta e as pastas versoes/,
saida/frames*/, hf/renders, hf/.cache. Fica: textos, json, imagens finais e geradores (trabalho/ fica, só perde a mídia).
Idempotente: rodar de novo apaga 0 arquivos.
"""
import argparse, datetime, json, os, shutil, sys, urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
EXT = {".mp4", ".mov", ".m4a", ".wav", ".mp3", ".webm"}
PASTAS = {"versoes"}


def chave():
    for linha in (RAIZ / ".env").read_text().splitlines():
        if linha.startswith("ZERNIO_API_KEY="):
            return linha.split("=", 1)[1].strip().strip('"')
    sys.exit("ZERNIO_API_KEY não está no .env")


def status_zernio(pid):
    req = urllib.request.Request(f"https://zernio.com/api/v1/posts/{pid}",
                                 headers={"Authorization": f"Bearer {chave()}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        p = json.loads(r.read()).get("post", {})
    ig = [x for x in p.get("platforms", []) if x.get("platform") == "instagram"]
    return (ig[0].get("status") if ig else None) or p.get("status")


def alvos(pasta):
    pastas, arqs = [], []
    for d in sorted(pasta.rglob("*")):
        if not d.is_dir() or any(d.is_relative_to(p) for p in pastas):
            continue
        rel = d.relative_to(pasta)
        if (d.name in PASTAS or (rel.parts[0] == "saida" and d.name.startswith("frames"))
                or (len(rel.parts) >= 2 and rel.parts[-2] == "hf" and d.name in {"renders", ".cache"})):
            pastas.append(d)
    for f in sorted(pasta.rglob("*")):
        if f.is_file() and f.suffix.lower() in EXT and not any(f.is_relative_to(p) for p in pastas):
            arqs.append(f)
    return pastas, arqs


def tamanho(p):
    if p.is_file():
        return p.stat().st_size
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file() and not f.is_symlink())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pasta")
    ap.add_argument("--apagar", action="store_true")
    ap.add_argument("--sem-zernio")
    a = ap.parse_args()

    pasta = Path(a.pasta).resolve()
    if not pasta.is_dir() or not pasta.is_relative_to(RAIZ / "posts") or pasta == RAIZ / "posts":
        sys.exit(f"recuso: {pasta} não é uma pasta de post dentro de posts/")

    pastas, arqs = alvos(pasta)
    total = sum(tamanho(p) for p in pastas + arqs)
    for p in pastas:
        print(f"[pasta] {p.relative_to(pasta)}/  {tamanho(p)/1e6:.1f} MB")
    for f in arqs:
        print(f"[arq]   {f.relative_to(pasta)}  {tamanho(f)/1e6:.1f} MB")
    print(f"{len(pastas)} pastas, {len(arqs)} arquivos, {total/1e6:.1f} MB")

    if not a.apagar:
        print("simulação: nada apagado (use --apagar)")
        return

    if a.sem_zernio:
        origem = f"sem Zernio: {a.sem_zernio}"
    else:
        zt = pasta / "zernio.txt"
        if not zt.exists() or not zt.read_text().split():
            sys.exit("recuso: sem zernio.txt na pasta (o Publicador grava o ID do post ali)")
        pid = zt.read_text().split()[0]
        st = status_zernio(pid)
        if st != "published":
            print(f"recuso: post {pid} está '{st}' no Zernio, não publicado")
            sys.exit(1)
        origem = f"Zernio {pid} publicado"

    for p in pastas:
        shutil.rmtree(p)
    for f in arqs:
        f.unlink()
    agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(pasta / "limpeza.md", "a") as fh:
        fh.write(f"- {agora}: {len(pastas)} pastas, {len(arqs)} arquivos, {total/1e6:.1f} MB apagados ({origem})\n")
    print(f"apagado: {total/1e6:.1f} MB ({origem})")


if __name__ == "__main__":
    main()
