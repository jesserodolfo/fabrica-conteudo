#!/usr/bin/env python3
"""Capa de notícia (fundo preto, letra grande, foto real em cima e círculo de detalhe).
Uso: .venv/bin/python scripts/capa_noticia.py clientes/<cliente>/marca.json capa.json saida.jpg
capa.json: {"foto": "caminho.jpg", "circulo": "caminho.jpg ou vazio", "tag": "NOTÍCIA · TEXAS",
            "titulo": "<r>Tesla</r> acaba de mostrar o Roadster que <r>sai do chão</r>", "swipe": "ARRASTA PRO LADO ➜"}
A foto principal é cortada pra 1080x820 pelo centro. Use foto real (frame do vídeo oficial ou foto da matéria).
"""
import json, os, sys
from PIL import Image
from playwright.sync_api import sync_playwright

def abrir_navegador(p):
    """Usa o Google Chrome instalado no Mac. Se não tiver, usa o Chromium do Playwright."""
    try:
        return p.chromium.launch(channel="chrome")
    except Exception:
        return p.chromium.launch()

HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(sys.argv[1])); C = json.load(open(sys.argv[2])); out = os.path.abspath(sys.argv[3])
tmp = os.path.join(os.path.dirname(out) or '.', '_capa_tmp'); os.makedirs(tmp, exist_ok=True)
im = Image.open(C['foto']).convert('RGB'); W, H = im.size; r = 1080/820
if W/H > r: w = int(H*r); im = im.crop(((W-w)//2, 0, (W-w)//2+w, H))
else: h = int(W/r); im = im.crop((0, (H-h)//2, W, (H-h)//2+h))
im.resize((1080, 820), Image.LANCZOS).save(f'{tmp}/top.jpg', quality=93)
circ = ''
if C.get('circulo'):
    c = Image.open(C['circulo']).convert('RGB'); s = min(c.size)
    c.crop(((c.width-s)//2, (c.height-s)//2, (c.width-s)//2+s, (c.height-s)//2+s)).resize((420, 420)).save(f'{tmp}/circ.jpg', quality=92)
    circ = '<div class=circ></div>'
foto_perfil = os.path.abspath(M['foto_perfil']); cor = M['cor']
html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:A;src:url(file://{HERE}/fonts/Anton.woff2)}}
@font-face{{font-family:Archivo;src:url(file://{HERE}/fonts/Archivo.ttf);font-weight:100 900}}
*{{margin:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;background:#050505;position:relative;overflow:hidden;font-family:Archivo,Arial,sans-serif}}
.top{{position:absolute;top:0;left:0;width:1080px;height:820px;background:url(top.jpg) center/cover}}
.fade{{position:absolute;top:590px;left:0;width:1080px;height:260px;background:linear-gradient(transparent,#050505)}}
.circ{{position:absolute;top:60px;right:46px;width:290px;height:290px;border-radius:50%;border:4px solid #fff;background:url(circ.jpg) center/cover;box-shadow:0 10px 40px rgba(0,0,0,.6)}}
.line{{position:absolute;top:830px;left:60px;right:60px;display:flex;align-items:center;gap:22px}}
.line i{{flex:1;height:2px;background:#555}}
.line img{{width:62px;height:62px;border-radius:50%;border:3px solid {cor};object-fit:cover}}
h1{{position:absolute;top:915px;left:40px;right:40px;text-align:center;font-family:A;font-weight:400;font-size:108px;line-height:1.02;color:#fff;text-transform:uppercase;letter-spacing:1px}}
h1 r{{color:{cor}}}
.sw{{position:absolute;bottom:34px;left:50%;transform:translateX(-50%);border:2px solid #fff;border-radius:40px;padding:10px 28px;color:#fff;font-size:24px;font-weight:700;letter-spacing:2px}}
.tag{{position:absolute;top:56px;left:56px;background:{cor};color:#fff;font-weight:800;font-size:24px;letter-spacing:2px;padding:10px 22px;border-radius:30px}}
</style></head><body><div class=top></div><div class=fade></div>{circ}
{('<div class=tag>'+C['tag']+'</div>') if C.get('tag') else ''}
<div class=line><i></i><img src="file://{foto_perfil}"><i></i></div>
<h1>{C['titulo']}</h1>{('<div class=sw>'+C['swipe']+'</div>') if C.get('swipe') else ''}</body></html>'''
open(f'{tmp}/capa.html', 'w').write(html)
with sync_playwright() as p:
    b = abrir_navegador(p); pg = b.new_page(viewport={'width': 1080, 'height': 1350})
    pg.goto(f'file://{tmp}/capa.html'); pg.wait_for_timeout(600)
    pg.screenshot(path=out, type='jpeg', quality=92); b.close()
print('ok', out)
