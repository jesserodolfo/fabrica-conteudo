#!/usr/bin/env python3
"""Capa com imagem gerada ocupando a tela toda e título grande em caixa alta em cima (modelo dos concorrentes:
fundo creme com palavra em caixa vermelha, ou fundo escuro com destaque laranja).
Uso: .venv/bin/python scripts/capa_titulo.py clientes/<cliente>/marca.json capa_titulo.json saida.jpg
capa_titulo.json: {"foto": "img.png", "tema": "claro"|"escuro", "linhas": ["VOCÊ USA SÓ 1", "DOS 4 JEITOS", "DO <box>CLAUDE</box>"],
  "sub": "texto menor", "tam": 112, "topo": 150, "swipe": "ARRASTA"}
<box>..</box> = palavra em caixa da cor da marca (texto branco); <y>..</y> = palavra em amarelo/laranja.
"""
import json, os, sys, base64
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(sys.argv[1])); C = json.load(open(sys.argv[2])); out = os.path.abspath(sys.argv[3])
f64 = base64.b64encode(open(C['foto'], 'rb').read()).decode()
av = os.path.abspath(M.get('foto_perfil', ''))
av64 = base64.b64encode(open(av, 'rb').read()).decode() if os.path.isfile(av) else ''
claro = C.get('tema', 'claro') == 'claro'
cor_txt = '#141414' if claro else '#ffffff'
dest = M['cor'] if claro else '#ff4a3d'
F = lambda n: os.path.join(HERE, 'fonts', n)
linhas = ''.join(f'<div>{l}</div>' for l in C['linhas']).replace('<box>', '<span class="bx">').replace('</box>', '</span>').replace('<y>', '<span class="y">').replace('</y>', '</span>')
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Anton;src:url('file://{F('Anton.woff2')}')}}
@font-face{{font-family:Archivo;src:url('file://{F('Archivo.ttf')}')}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;overflow:hidden;position:relative;font-family:Archivo,sans-serif;background:#000}}
.bg{{position:absolute;inset:0;background:url(data:image/png;base64,{f64}) center bottom/cover}}
.head{{position:absolute;top:40px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:12px;font-weight:800;font-size:28px;color:{cor_txt}}}
.head img{{width:46px;height:46px;border-radius:50%;object-fit:cover}} .head span{{opacity:.6;font-weight:500}}
.tit{{position:absolute;left:64px;right:64px;top:{C.get('topo',140)}px;font-family:Anton,sans-serif;text-transform:uppercase;color:{cor_txt};font-size:{C.get('tam',112)}px;line-height:{C.get('lh',1.02)};text-align:center}}
.bx{{background:{dest};color:#fff;padding:0 18px;display:inline-block;transform:rotate(-1.5deg)}}
.y{{color:{dest}}}
.sub{{margin-top:22px;font-family:Archivo;text-transform:none;font-size:34px;font-weight:600;line-height:1.3;opacity:.85}}
.sw{{position:absolute;right:64px;bottom:44px;font-weight:800;font-size:24px;letter-spacing:2px;color:{cor_txt}}}
.bar{{position:absolute;left:0;right:0;top:0;height:10px;background:{M['cor']}}}
</style></head><body><div class="bg"></div><div class="bar"></div>
<div class="head">{('<img src="data:image/jpeg;base64,'+av64+'">') if av64 else ''}<b>{M['nome']}</b><span>{M['handle']}</span></div>
<div class="tit">{linhas}{('<div class="sub">'+C['sub']+'</div>') if C.get('sub') else ''}</div>
<div class="sw">{C.get('swipe','ARRASTA')} →</div></body></html>"""
hp = out + '.html'; open(hp, 'w').write(html)
with sync_playwright() as p:
    try:
        b = p.chromium.launch(channel="chrome")
    except Exception:
        b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1080, 'height': 1350}); pg.goto('file://' + hp); pg.wait_for_timeout(600)
    pg.screenshot(path=out, type='jpeg', quality=93); b.close()
print('ok', out)
