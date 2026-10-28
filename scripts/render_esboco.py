#!/usr/bin/env python3
"""Renderiza carrossel 1080x1350 no modelo da marca, mas com o miolo (body) desenhado à mão
(rough.js + fonte manuscrita Kalam), estilo Excalidraw. Não altera o render.py.
Uso: .venv/bin/python scripts/render_esboco.py clientes/<cliente>/marca.json posts/<slug>/slides.json posts/<slug>/esboco.json posts/<slug>/saida
O esboco.json tem {"slides":[{"type":...,...}]} (um desenho por slide, mesma ordem do slides.json).
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render
from playwright.sync_api import sync_playwright

FONTS = f"""
@font-face{{font-family:Kalam;font-weight:700;src:url(file://{HERE}/fonts/Kalam-Bold.ttf)}}
@font-face{{font-family:Kalam;font-weight:400;src:url(file://{HERE}/fonts/Kalam-Regular.ttf)}}
#d{{flex:1 1 0;min-height:0;width:100%}}
"""

def capa_tweet(s, M):
    # capa estilo tweet: avatar grande, texto corrido com negrito e desenho embaixo (#d)
    h0 = render.slide_html(dict(s, body=''), M)
    css = h0.split('<style>')[1].split('</style>')[0]
    foto = os.path.abspath(M['foto_perfil'])
    extra = (".slide{padding:0 70px}.tw-h{display:flex;align-items:center;gap:34px;margin-top:70px}"
      ".tw-h .av{width:150px;height:150px;border-radius:50%;background:url('file://"+foto+"') center/cover;flex:none}"
      ".tw-h b{font-size:46px;font-weight:800;display:flex;align-items:center;gap:12px}.tw-h span{display:block;font-size:34px;color:#8a8a8a;font-weight:500;margin-top:4px}"
      ".tw-t{font-size:41px;line-height:1.34;color:#111;margin-top:46px;font-weight:400}.tw-t p{margin:0 0 26px}.tw-t b{font-weight:800}"
      ".tw-d{flex:1 1 0;min-height:0;margin-top:6px;position:relative}")
    check = getattr(render, 'CHECK', '')
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{css}{extra}</style></head><body>'
      f'<div class="slide"><div class="tw-h"><div class="av"></div><div><b>{M["nome"]}{check}</b><span>{M["handle"]}</span></div></div>'
      f'<div class="tw-t">{s["tweet"]}</div><div id="d" class="tw-d"></div>'
      f'<div class="foot"><span>{M["handle"]}</span><span>{s.get("foot_r") or "arrasta"}</span></div></div></body></html>')

def html_slide(s, M, spec):
    s2 = dict(s); s2['body'] = '<div id="d"></div>'
    h = capa_tweet(s, M) if s.get('tweet') else render.slide_html(s2, M)
    rough = open(os.path.join(HERE, 'vendor', 'rough.js')).read()
    js = open(os.path.join(HERE, 'esboco.js')).read()
    esb = json.dumps({"cor": M['cor'], "slide": spec}, ensure_ascii=False)
    extra = f"<style>{FONTS}</style><script>{rough}</script><script>window.ESB={esb};</script><script>{js}</script>"
    return h.replace('</body>', extra + '</body>')

def main():
    M = json.load(open(sys.argv[1])); data = json.load(open(sys.argv[2]))
    esb = json.load(open(sys.argv[3]))['slides']; out = sys.argv[4]
    os.makedirs(out, exist_ok=True)
    with sync_playwright() as p:
        b = render.abrir_navegador(p); pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for i, s in enumerate(data['slides'], 1):
            path = os.path.join(out, f"{i:02d}.html")
            open(path, "w").write(html_slide(s, M, esb[i-1]))
            pg.goto("file://" + os.path.abspath(path))
            pg.wait_for_function("window.__ready===true", timeout=15000)
            err = pg.evaluate("window.__err||''")
            if err: print("ERRO slide", i, err)
            pg.wait_for_timeout(200)
            pg.screenshot(path=os.path.join(out, f"{data['slug']}-{i:02d}.jpg"), type="jpeg", quality=93,
                          clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
        b.close()
    print("ok", len(data['slides']))

if __name__ == "__main__":
    main()
