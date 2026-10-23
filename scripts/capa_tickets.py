#!/usr/bin/env python3
"""Capa TICKETS (modelo do post ROSTO): fundo preto, foto real do cliente em cima, tickets coloridos
colados em volta (como post-it com fita) e título grande em caixa alta embaixo, com uma linha em amarelo.
Uso: .venv/bin/python scripts/capa_tickets.py clientes/<cliente>/marca.json capa_tickets.json saida.jpg
capa_tickets.json: {"foto": "caminho.jpg", "foco_y": 0.25, "pill": "CLAUDE · NO NEGÓCIO",
  "titulo": ["VOCÊ USA SÓ 1 DOS", "<y>4 JEITOS DO CLAUDE</y>", "NO SEU NEGÓCIO"],
  "tickets": ["/conversar", "/arquivos", "/construir", "/material"], "swipe": "ARRASTA"}
Até 6 tickets; cores e posições fixas, alternando lados.
"""
import json, os, sys, base64
from PIL import Image
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(sys.argv[1])); C = json.load(open(sys.argv[2])); out = os.path.abspath(sys.argv[3])

def abrir_navegador(p):
    try:
        return p.chromium.launch(channel="chrome")
    except Exception:
        return p.chromium.launch()

# foto: corta 1080x900 com foco vertical configurável
im = Image.open(C['foto']).convert('RGB'); W, H = im.size; r = 1080/900
fy = C.get('foco_y', 0.2)
if W/H > r:
    w = int(H*r); im = im.crop(((W-w)//2, 0, (W-w)//2+w, H))
else:
    h = int(W/r); top = int(max(0, min(H-h, H*fy - h*0.15))); im = im.crop((0, top, W, top+h))
tmp = out + '.foto.jpg'; im.resize((1080, 900), Image.LANCZOS).save(tmp, quality=93)
foto64 = base64.b64encode(open(tmp, 'rb').read()).decode()
av = os.path.abspath(M['foto_perfil']) if M.get('foto_perfil') else ''
av64 = base64.b64encode(open(av, 'rb').read()).decode() if av and os.path.exists(av) else ''

CORES = ['#ffe45c', '#ffb3c7', '#9ee6a8', '#ffc58f', '#9fd3ff', '#d9c2ff']
POS = [(60, 210, -5), (770, 300, 4), (70, 430, 3), (700, 470, -4), (110, 620, -3), (660, 660, 5)]
tk = ''
for i, t in enumerate(C['tickets'][:6]):
    x, y, rot = POS[i]
    tk += f'<div class="tk" style="left:{x}px;top:{y}px;background:{CORES[i]};transform:rotate({rot}deg)"><i></i>{t}</div>'
masc = ''
if C.get('mascote'):
    mc = C['mascote']; m64 = base64.b64encode(open(mc['img'], 'rb').read()).decode()
    masc = f'<img style="position:absolute;z-index:3;left:{mc["x"]}px;top:{mc["y"]}px;width:{mc["w"]}px;filter:drop-shadow(0 12px 24px rgba(0,0,0,.6))" src="data:image/png;base64,{m64}">'
tit = ''.join(f'<div>{l}</div>' for l in C['titulo']).replace('<y>', '<span class="y">').replace('</y>', '</span>')
font = os.path.join(HERE, 'fonts', 'Anton.woff2'); font2 = os.path.join(HERE, 'fonts', 'Archivo.ttf'); hand = os.path.join(HERE, 'fonts', 'Caveat-Bold.ttf')
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Anton;src:url('file://{font}')}}
@font-face{{font-family:Archivo;src:url('file://{font2}')}}
@font-face{{font-family:Caveat;src:url('file://{hand}')}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;background:#0b0b0b;overflow:hidden;font-family:Archivo,sans-serif;position:relative}}
.bar{{position:absolute;left:0;right:0;top:0;height:10px;background:{M['cor']};z-index:5}}
.foto{{position:absolute;left:0;top:0;width:1080px;height:900px;background:url(data:image/jpeg;base64,{foto64}) center/cover}}
.topfade{{position:absolute;left:0;right:0;top:0;height:200px;background:linear-gradient(180deg,rgba(11,11,11,.85),rgba(11,11,11,0));z-index:2}}
.fade{{position:absolute;left:0;right:0;top:420px;height:500px;background:linear-gradient(180deg,rgba(11,11,11,0),#0b0b0b 85%)}}
.head{{position:absolute;top:40px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:12px;color:#fff;font-weight:800;font-size:28px;z-index:4}}
.head img{{width:46px;height:46px;border-radius:50%;object-fit:cover}}
.head span{{color:rgba(255,255,255,.7);font-weight:500}}
.tk{{position:absolute;z-index:3;font-family:Caveat,cursive;font-size:54px;color:#111;padding:18px 34px 14px;box-shadow:0 14px 30px rgba(0,0,0,.45);min-width:290px}}
.tk i{{position:absolute;left:50%;top:-14px;width:90px;height:28px;margin-left:-45px;background:rgba(255,255,255,.55)}}
.pill{{position:absolute;left:72px;top:905px;background:#ffd23f;color:#111;font-weight:900;font-size:24px;letter-spacing:1.5px;padding:10px 18px;border-radius:6px;z-index:4}}
.tit{{position:absolute;left:72px;right:72px;top:960px;font-family:Anton,sans-serif;color:#fff;font-size:{C.get('tam',100)}px;line-height:{C.get('lh',1.02)};text-transform:uppercase;z-index:4}}
.tit .y{{color:#ffd23f}}
.sw{{position:absolute;right:72px;bottom:44px;color:#fff;font-weight:800;font-size:24px;letter-spacing:2px;z-index:4}}
</style></head><body>
<div class="bar"></div><div class="foto"></div><div class="fade"></div><div class="topfade"></div>
<div class="head">{('<img src="data:image/jpeg;base64,'+av64+'">') if av64 else ''}<b>{M['nome']}</b><span>{M['handle']}</span></div>
{tk}{masc}<div class="pill">{C.get('pill','')}</div><div class="tit">{tit}</div><div class="sw">{C.get('swipe','ARRASTA')} →</div>
</body></html>"""
hp = out + '.html'; open(hp, 'w').write(html)
with sync_playwright() as p:
    b = abrir_navegador(p); pg = b.new_page(viewport={'width': 1080, 'height': 1350})
    pg.goto('file://' + hp); pg.wait_for_timeout(600)
    pg.screenshot(path=out, type='jpeg', quality=93); b.close()
os.remove(tmp)
print('ok', out)
