#!/usr/bin/env python3
"""Renderiza o carrossel SEMANA em 3 estilos sem alterar render.py nem render_esboco.py.
Uso: .venv/bin/python scripts/render_semana.py <modo> marca.json slides.json esboco.json|- saida
modo: caderno (esboço sobre papel pautado) | branco (esboço sobre fundo branco) | escuro (render.py em tema escuro, usa o body do slides.json)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render
from playwright.sync_api import sync_playwright

PAPEL = """
.slide{background:#f7f0e1 repeating-linear-gradient(180deg,transparent 0,transparent 53px,rgba(120,140,170,.28) 53px,rgba(120,140,170,.28) 55px);padding-left:128px}
.slide:before{content:"";position:absolute;left:92px;top:0;bottom:0;width:3px;background:rgba(229,57,47,.45);z-index:0}
.slide:after{content:"";position:absolute;left:22px;top:0;bottom:0;width:36px;z-index:0;
 background:radial-gradient(circle at 18px 18px,#e9dfc9 0 13px,#b9ad92 13px 15px,transparent 16px) 0 0/36px 86px repeat-y}
.slide>*:not(.bar){position:relative;z-index:1}
.pill{background:#fff;border:2px solid __COR__}
"""

ESCURO = """
.slide{background:#0b0b0b;color:#fff}
.head span,.foot,.sub,.note{color:#9c9c9c}
.head b,.foot b,.sub b{color:#fff}
.pill{background:__COR__;color:#fff}
.card,.num{background:#171717;border:1px solid #2c2c2c;box-shadow:none}
.dark{background:#171717;border:2px solid __COR__;color:#fff}
.dark .lbl{color:__CLARA__}
.lbl{color:#8d8d8d}
.rule,.num .t{color:#fff}.num .d{color:#a5a5a5}
.li.g{color:#8d8d8d}.li i{background:#555}
.rule{font-size:50px!important}.card,.dark{padding:46px 48px}.lbl{font-size:26px}.li{font-size:46px;margin:0 0 26px}.li i{width:18px;height:18px;margin-top:20px}.num .t{font-size:48px}.num .d{font-size:33px}.num .n{width:72px;height:72px;font-size:36px}.num{padding:34px 38px}.dm p{font-size:42px!important}.dm .btn{font-size:40px;padding:26px}.note{font-size:36px;color:#d0d0d0}.body{gap:34px}
.dm{background:#1c1c1c}.dm p{color:#ddd}.dm .btn{background:#262626;color:#fff}
"""

def esboco_html(s, M, spec, fundo):
    s2 = dict(s); s2['body'] = '<div id="d"></div>'
    h = render.slide_html(s2, M)
    cor = M['cor']
    css = render_esboco_fonts()
    if fundo == 'caderno':
        css += PAPEL.replace('__COR__', cor)
    rough = open(os.path.join(HERE, 'vendor', 'rough.js')).read()
    js = open(os.path.join(HERE, 'esboco_semana.js')).read()
    esb = json.dumps({"cor": cor, "slide": spec}, ensure_ascii=False)
    extra = f"<style>{css}</style><script>{rough}</script><script>window.ESB={esb};</script><script>{js}</script>"
    return h.replace('</body>', extra + '</body>')

def render_esboco_fonts():
    return (f"@font-face{{font-family:Kalam;font-weight:700;src:url(file://{HERE}/fonts/Kalam-Bold.ttf)}}"
            f"@font-face{{font-family:Kalam;font-weight:400;src:url(file://{HERE}/fonts/Kalam-Regular.ttf)}}#d{{flex:1 1 0;min-height:0;width:100%}}")

def escuro_html(s, M):
    h = render.slide_html(s, M)
    css = ESCURO.replace('__COR__', M['cor']).replace('__CLARA__', M.get('cor_destaque_escuro', M['cor']))
    return h.replace('</style>', css + '</style>', 1)

def main():
    modo, mj, sj, ej, out = sys.argv[1:6]
    M = json.load(open(mj)); data = json.load(open(sj))
    esb = json.load(open(ej))['slides'] if ej != '-' else None
    os.makedirs(out, exist_ok=True)
    with sync_playwright() as p:
        b = render.abrir_navegador(p); pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for i, s in enumerate(data['slides'], 1):
            path = os.path.join(out, f"{i:02d}.html")
            html = escuro_html(s, M) if modo == 'escuro' else esboco_html(s, M, esb[i-1], modo)
            open(path, "w").write(html)
            pg.goto("file://" + os.path.abspath(path))
            if modo != 'escuro':
                pg.wait_for_function("window.__ready===true", timeout=15000)
                err = pg.evaluate("window.__err||''")
                if err: print("ERRO slide", i, err)
            pg.wait_for_timeout(300)
            pg.screenshot(path=os.path.join(out, f"{data['slug']}-{i:02d}.jpg"), type="jpeg", quality=93,
                          clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
        b.close()
    print("ok", len(data['slides']))

if __name__ == "__main__":
    main()
