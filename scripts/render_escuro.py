#!/usr/bin/env python3
"""Slides internos tipográficos escuros (cópia leve do render.py, sem alterá-lo).
Uso: .venv/bin/python scripts/render_escuro.py marca.json slides.json saida [primeiro_numero]
Pula a capa (usa só "slides"). Fundo #0a0a0a, texto branco, <r> no destaque escuro da marca, título grande."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import render
from playwright.sync_api import sync_playwright
DARK = """<style>
.slide{background:#0a0a0a!important;color:#fff!important}
.head b{color:#fff!important}.head span{color:#9a9a9a!important}
.pill{background:#1c1c1c!important;color:#ff4a3d!important}
h1{font-size:104px!important;line-height:1.04!important;color:#fff}
h1 r{color:%s!important}
.sub{color:#bdbdbd!important;font-size:36px!important}
.foot{color:#7a7a7a!important}.foot b{color:#fff!important}
.body{color:#fff}
</style>"""
def main():
    M = json.load(open(sys.argv[1])); data = json.load(open(sys.argv[2])); out = sys.argv[3]
    start = int(sys.argv[4]) if len(sys.argv) > 4 else 2
    os.makedirs(out, exist_ok=True)
    with sync_playwright() as p:
        b = render.abrir_navegador(p); pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for i, s in enumerate(data['slides'], start):
            h = render.slide_html(s, M).replace('</head>', DARK % M.get('cor_destaque_escuro', '#ff4a3d') + '</head>')
            path = os.path.join(out, f"{i:02d}.html"); open(path, 'w').write(h)
            pg.goto('file://' + os.path.abspath(path)); pg.wait_for_timeout(500)
            pg.screenshot(path=os.path.join(out, f"{data['slug']}-{i:02d}.jpg"), type='jpeg', quality=93)
        b.close()
    print('ok')
main()
