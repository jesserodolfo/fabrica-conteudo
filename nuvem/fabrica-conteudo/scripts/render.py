#!/usr/bin/env python3
"""Renderiza carrossel 1080x1350 no modelo branco e vermelho.
Uso: .venv/bin/python scripts/render.py clientes/<cliente>/marca.json posts/<slug>/slides.json posts/<slug>/saida
O JSON de slides tem {"slug":..., "slides":[{pill,title,sub,body,small,photo,tag,foot_r}]}.
No title, <r>palavra</r> fica na cor da marca.
"""
import json, os, sys
HERE=os.path.dirname(os.path.abspath(__file__))
from playwright.sync_api import sync_playwright

def abrir_navegador(p):
    """Usa o Google Chrome instalado no Mac. Se não tiver, usa o Chromium do Playwright."""
    try:
        return p.chromium.launch(channel="chrome")
    except Exception:
        return p.chromium.launch()


CHECK = ('<svg width="28" height="28" viewBox="0 0 24 24" aria-label="verificado"><path fill="#1d9bf0" d="M22.5 12.5c0-1.58-.88-2.95-2.15-3.6.15-.44.24-.9.24-1.4 0-2.21-1.71-4-3.82-4-.47 0-.92.08-1.34.25C14.82 2.42 13.51 1.5 12 1.5s-2.82.92-3.44 2.25c-.41-.17-.87-.25-1.34-.25-2.11 0-3.82 1.79-3.82 4 0 .49.08.96.24 1.4-1.27.65-2.15 2.02-2.15 3.6 0 1.5.78 2.8 1.94 3.49-.02.17-.03.34-.03.51 0 2.21 1.71 4 3.82 4 .47 0 .92-.09 1.34-.25.62 1.33 1.92 2.25 3.44 2.25s2.82-.92 3.44-2.25c.41.16.86.25 1.34.25 2.11 0 3.82-1.79 3.82-4 0-.17-.01-.34-.03-.51 1.16-.69 1.94-1.99 1.94-3.49z"></path><path fill="#ffffff" d="M10.4 16.2 6.8 12.6l1.4-1.4 2.2 2.2 5.4-5.4 1.4 1.4z"></path></svg>')

CSS_T = """
@font-face{font-family:Archivo;src:url(file://__FONT__);font-weight:100 900}
*{box-sizing:border-box}
body{margin:0;background:#fff}
.slide{width:1080px;height:1350px;background:#fff;color:#111;font-family:Archivo,sans-serif;position:relative;overflow:hidden;display:flex;flex-direction:column;padding:0 72px 48px}
.bar{position:absolute;left:0;top:0;right:0;height:10px;background:#e5392f}
.head{display:flex;justify-content:center;align-items:center;gap:14px;padding-top:52px}
.head b{font-weight:800;font-size:28px}
.head span{color:#8a8a8a;font-size:28px}
.pill{align-self:flex-start;margin-top:52px;background:#fdecea;color:#d12f25;font-weight:800;font-size:22px;letter-spacing:2px;padding:12px 22px;border-radius:999px;text-transform:uppercase}
h1{margin:26px 0 0;font-size:80px;font-weight:900;letter-spacing:-0.5px;word-spacing:10px;line-height:1.08}
h1.small{font-size:72px}
h1 r{color:#e5392f}
.sub{margin:24px 0 0;font-size:32px;line-height:1.4;color:#555}
.sub b{color:#111;font-weight:800}
.body{flex:1 1 0;min-height:0;display:flex;flex-direction:column;justify-content:center;gap:26px;padding-top:28px}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:24px;color:#8a8a8a}
.foot b{color:#111;font-weight:700;font-size:28px}
.card{background:#fff;border:1px solid #ececec;border-radius:24px;box-shadow:0 24px 70px rgba(0,0,0,.12);padding:36px 40px}
.dark{background:#111;color:#fff;border-radius:24px;padding:34px 38px}
.dark .lbl{color:#ff6b61}
.lbl{font-size:22px;font-weight:800;letter-spacing:2px;text-transform:uppercase;color:#9a9a9a;margin-bottom:18px}
.lbl.red{color:#d12f25}
.row{display:flex;align-items:center;gap:20px;padding:16px 0;border-bottom:1px solid #f0f0f0;font-size:30px;font-weight:700}
.row:last-child{border-bottom:0}
.row .k{width:34px;height:34px;border-radius:9px;background:#e5392f;flex-shrink:0;display:flex;align-items:center;justify-content:center;color:#fff;font-size:20px}
.row .o{width:34px;height:34px;border-radius:9px;border:3px solid #d0d0d0;flex-shrink:0}
.row .w{width:34px;height:34px;border-radius:9px;background:#f3b200;flex-shrink:0;display:flex;align-items:center;justify-content:center;color:#111;font-size:20px;font-weight:900}
.row .g{color:#8a8a8a;font-weight:500;font-size:26px;margin-left:auto}
.num{display:flex;gap:24px;align-items:flex-start;background:#fff;border:1px solid #ececec;border-radius:22px;box-shadow:0 18px 50px rgba(0,0,0,.10);padding:28px 32px}
.num .n{width:60px;height:60px;border-radius:50%;background:#e5392f;color:#fff;font-weight:900;font-size:30px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.num .t{font-size:38px;font-weight:900;letter-spacing:-1px;line-height:1.1}
.num .d{font-size:27px;line-height:1.4;color:#666;margin-top:6px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:36px}
.cols .c2{border-left:2px solid #f1f1f1;padding-left:36px}
.li{display:flex;gap:14px;align-items:flex-start;font-size:29px;line-height:1.3;margin:0 0 18px}
.li i{width:12px;height:12px;border-radius:50%;background:#c8c8c8;margin-top:13px;flex-shrink:0}
.li.r i{background:#e5392f}
.li.r{font-weight:800}
.li.g{color:#8a8a8a}
table{width:100%;border-collapse:collapse;font-size:26px}
th{text-align:left;font-size:20px;letter-spacing:2px;text-transform:uppercase;color:#9a9a9a;padding:0 0 14px;font-weight:800}
td{padding:14px 0;border-top:1px solid #f0f0f0;vertical-align:top;line-height:1.3}
td.b{font-weight:800;font-size:28px}
td.red{color:#d12f25;font-weight:700}
.chat{position:relative;height:400px;overflow:hidden;background:#fff;border:1px solid #ececec;border-radius:24px;box-shadow:0 24px 70px rgba(0,0,0,.14)}
.chat .top{display:flex;align-items:center;gap:10px;padding:20px 28px;border-bottom:1px solid #f0f0f0}
.chat .top i{width:14px;height:14px;border-radius:50%;background:#e0e0e0;display:block}
.chat .top span{margin-left:14px;font-size:22px;font-weight:700;color:#8a8a8a}
.chat .msg{margin:28px;background:#f2f2f2;border-radius:22px 22px 6px 22px;padding:26px 30px;font-size:28px;line-height:1.45;color:#222}
.chat .msg b{color:#e5392f}
.chat .fade{position:absolute;left:0;right:0;bottom:0;height:190px;background:linear-gradient(rgba(255,255,255,0),#fff 62%);display:flex;align-items:flex-end;justify-content:center;padding-bottom:28px}
.chat .fade span{background:#e5392f;color:#fff;font-weight:800;font-size:24px;letter-spacing:1.5px;padding:14px 26px;border-radius:999px;text-transform:uppercase}
.rule{font-size:38px;font-weight:800;line-height:1.25;letter-spacing:-.5px}
.cmt{display:flex;gap:18px;align-items:flex-start}
.cmt .av{width:52px;height:52px;border-radius:50%;background:#d9d9d9;flex-shrink:0}
.cmt .av.me{width:44px;height:44px;background:#1a1a1a}
.cmt .nm{font-size:24px;font-weight:800}
.cmt .nm span{font-weight:500;color:#9a9a9a}
.cmt .tx{font-size:34px;font-weight:800;letter-spacing:1px;margin-top:6px}
.cmt .tx2{font-size:30px;margin-top:6px}
.dm{align-self:flex-end;width:760px;background:#f2f2f2;border-radius:26px 26px 26px 8px;padding:28px 30px}
.dm p{margin:0;font-size:27px;line-height:1.45;color:#222}
.dm .btn{margin-top:20px;background:#fff;border-radius:14px;padding:18px;text-align:center;font-size:26px;font-weight:800;color:#1d6fe0}
.bars .b{display:flex;align-items:center;gap:18px;margin:0 0 22px}
.bars .b span{width:260px;font-size:27px;font-weight:700;flex-shrink:0}
.bars .b i{height:34px;border-radius:8px;background:#e5392f;display:block}
.bars .b i.g{background:#c8c8c8}
.bars .b em{font-style:normal;font-size:26px;color:#8a8a8a;font-weight:600}
.note{font-size:22px;color:#9a9a9a;margin-top:14px}
/* capa com foto */
.slide.cover{padding:0;background:#111;color:#fff}
.cover .photo{position:absolute;inset:0;background-size:cover;background-position:center top}
.cover .shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.55) 0%,rgba(0,0,0,.05) 30%,rgba(0,0,0,.15) 52%,rgba(0,0,0,.88) 78%,#0b0b0b 100%)}
.cover .head{position:relative;z-index:2;color:#fff}
.cover .head b{color:#fff}.cover .head span{color:rgba(255,255,255,.75)}
.cover .ctext{position:absolute;z-index:2;left:72px;right:72px;bottom:120px}
.cover .pill{display:inline-block;background:#e5392f;color:#fff;margin-top:0}
.cover h1{color:#fff;font-size:84px;text-shadow:0 6px 30px rgba(0,0,0,.5)}
.cover h1 r{color:#ff6b61}
.cover .sub{color:rgba(255,255,255,.82)}
.cover .sub b{color:#fff}
.cover .foot{position:absolute;z-index:2;left:72px;right:72px;bottom:48px;color:rgba(255,255,255,.7)}
.cover .foot b{color:#fff}
.cover.top .ctext{top:130px;bottom:auto}
.cover.top .shade{background:linear-gradient(180deg,rgba(0,0,0,.92) 0%,rgba(0,0,0,.7) 30%,rgba(0,0,0,.05) 55%,rgba(0,0,0,0) 80%,rgba(0,0,0,.6) 100%)}
.cover .tag{position:absolute;z-index:2;right:72px;top:150px;background:#fff;color:#111;font-weight:900;font-size:24px;letter-spacing:1.5px;padding:14px 22px;border-radius:12px;text-transform:uppercase;transform:rotate(4deg);box-shadow:0 14px 40px rgba(0,0,0,.35)}
"""

def slide_html(s, M):
    CSS=CSS_T.replace('__FONT__',os.path.join(HERE,'fonts','Archivo.ttf')).replace('#e5392f',M['cor']).replace('#d12f25',M.get('cor_escura',M['cor'])).replace('#fdecea',M.get('cor_clara','#fdecea')).replace('#ff6b61',M.get('cor_destaque_escuro','#ff6b61'))
    NOME, AT = M['nome'], M['handle']
    small = ' class="small"' if s.get('small') else ''
    foot_r = s.get('foot_r') or 'arrasta →'
    if s.get('photo'):
        photo = os.path.abspath(s['photo'])
        tag = f"<div class='tag'>{s['tag']}</div>" if s.get('tag') else ''
        return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="slide cover{' top' if s.get('text_top') else ''}"><div class="photo" style="background-image:url('file://{photo}')"></div><div class="shade"></div><div class="bar" style="z-index:3"></div>
<div class="head"><b>{NOME}</b>{CHECK if M.get('verificado',True) else ''}<span>{AT}</span></div>{tag}
<div class="ctext"><div class="pill">{s['pill']}</div>
<h1{small}>{s['title']}</h1>
{('<p class="sub">'+s['sub']+'</p>') if s.get('sub') else ''}</div>
<div class="foot"><span>{AT}</span><span>{foot_r}</span></div>
</div></body></html>"""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="slide"><div class="bar"></div>
<div class="head"><b>{NOME}</b>{CHECK if M.get('verificado',True) else ''}<span>{AT}</span></div>
<div class="pill">{s['pill']}</div>
<h1{small}>{s['title']}</h1>
{('<p class="sub">'+s['sub']+'</p>') if s.get('sub') else ''}
<div class="body">{s.get('body','')}</div>
<div class="foot"><span>{AT}</span><span>{foot_r}</span></div>
</div></body></html>"""

def main():
    M = json.load(open(sys.argv[1])); src, out = sys.argv[2], sys.argv[3]
    data = json.load(open(src))
    os.makedirs(out, exist_ok=True)
    with sync_playwright() as p:
        b = abrir_navegador(p); pg = b.new_page(viewport={"width":1080,"height":1350})
        for i, s in enumerate(data['slides'], 1):
            path = os.path.join(out, f"{i:02d}.html")
            open(path, "w").write(slide_html(s, M))
            pg.goto("file://"+os.path.abspath(path)); pg.wait_for_timeout(300)
            pg.evaluate("document.fonts.ready")
            pg.screenshot(path=os.path.join(out, f"{data['slug']}-{i:02d}.jpg"), type="jpeg", quality=93,
                          clip={"x":0,"y":0,"width":1080,"height":1350})
        b.close()
    print("ok", len(data['slides']))

if __name__ == "__main__":
    main()
