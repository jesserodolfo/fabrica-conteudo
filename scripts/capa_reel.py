#!/usr/bin/env python3
"""Capa de reel 1080x1920 no padrão @igao.ia: fundo escuro com piso em perspectiva, título no topo
(linha 1 sans branca, linha 2 serifada itálica dentro de caixa de seleção vermelha, linha 3 cinza)
e um quadro chamativo do próprio vídeo em destaque, inclinado, com brilho.
Texto e quadro ficam dentro do recorte 3:4 do grid do perfil (y 240 a 1680).

Uso: .venv/bin/python scripts/capa_reel.py capa.json saida.jpg
capa.json: {"video": "posts/.../saida/X.mp4", "t": 6.0, "crop": [90,490,990,1310],
            "l1": "As 5 skills", "l2": "que eu mais uso", "l3": "no Claude Code", "chip": "Claude Code"}
"""
import json, os, sys, base64, subprocess, tempfile
from playwright.sync_api import sync_playwright
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)); F = lambda n: os.path.join(HERE, 'fonts', n)
C = json.load(open(sys.argv[1])); out = os.path.abspath(sys.argv[2])
tmp = tempfile.mkdtemp()
fr = os.path.join(tmp, 'f.png')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(C['t']), '-i', C['video'], '-frames:v', '1', fr], check=True)
im = Image.open(fr).convert('RGB')
if C.get('crop'): im = im.crop(tuple(C['crop']))
cp = os.path.join(tmp, 'c.png'); im.save(cp)
w, h = im.size; W = C.get('largura', 900); H = round(W * h / w)
b64 = base64.b64encode(open(cp, 'rb').read()).decode()
chip = f'<span class="chip"><i></i>{C["chip"]}</span>' if C.get('chip') else ''
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Archivo;src:url('file://{F('Archivo.ttf')}')}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;overflow:hidden;position:relative;background:#09090b;font-family:Archivo,sans-serif;color:#fff}}
.glow{{position:absolute;inset:0;background:radial-gradient(ellipse 70% 40% at 50% 62%,rgba(229,57,47,.20),transparent 70%),radial-gradient(ellipse 90% 60% at 50% 30%,rgba(255,255,255,.05),transparent 70%)}}
.floor{{position:absolute;left:-60%;right:-60%;top:1180px;height:1400px;transform:perspective(700px) rotateX(62deg);transform-origin:top;
background-image:linear-gradient(rgba(255,255,255,.07) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.07) 2px,transparent 2px);background-size:120px 120px;
-webkit-mask-image:linear-gradient(#000,transparent 75%)}}
.dots{{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.18) 1.5px,transparent 2px);background-size:140px 160px;opacity:.35;-webkit-mask-image:radial-gradient(ellipse at 50% 40%,transparent 30%,#000 80%)}}
.tit{{position:absolute;left:60px;right:60px;top:300px;text-align:center}}
.l1{{font-weight:800;font-size:76px;letter-spacing:-1.5px;line-height:1.1;display:flex;justify-content:center;align-items:center;gap:18px;flex-wrap:wrap}}
.chip{{display:inline-flex;align-items:center;gap:12px;background:#fff;color:#141414;font-size:46px;font-weight:800;padding:8px 22px 8px 16px;border-radius:14px;letter-spacing:-.5px}}
.chip i{{width:26px;height:26px;border-radius:7px;background:#e5392f;display:inline-block}}
.l2w{{margin-top:14px;display:inline-block;position:relative;padding:4px 30px 12px;border:3px solid #e5392f;background:rgba(229,57,47,.10)}}
.l2w b{{position:absolute;width:16px;height:16px;background:#fff;border:3px solid #e5392f}}
.l2{{font-family:Georgia,serif;font-style:italic;font-weight:400;font-size:104px;line-height:1.08;letter-spacing:-1px}}
.l3{{margin-top:20px;font-size:46px;font-weight:600;color:#a9a9b2}}
.card{{position:absolute;left:50%;top:{C.get('topo_card', 820)}px;width:{W}px;height:{H}px;margin-left:-{W//2}px;border-radius:26px;overflow:hidden;
transform:perspective(1600px) rotateX(14deg) rotateY(-6deg) rotateZ(1deg);
box-shadow:0 60px 120px rgba(0,0,0,.7),0 0 0 2px rgba(255,255,255,.08),0 0 140px rgba(229,57,47,.35)}}
.card img{{width:100%;height:100%;display:block}}
</style></head><body><div class="glow"></div><div class="floor"></div><div class="dots"></div>
<div class="tit"><div class="l1">{C['l1']}{chip}</div>
<div class="l2w"><b style="left:-10px;top:-10px"></b><b style="right:-10px;top:-10px"></b><b style="left:-10px;bottom:-10px"></b><b style="right:-10px;bottom:-10px"></b><div class="l2">{C['l2']}</div></div>
{('<div class="l3">'+C['l3']+'</div>') if C.get('l3') else ''}</div>
<div class="card"><img src="data:image/png;base64,{b64}"></div>
</body></html>"""
hp = out + '.html'; open(hp, 'w').write(html)
with sync_playwright() as p:
    try: b = p.chromium.launch(channel='chrome')
    except Exception: b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1080, 'height': 1920}); pg.goto('file://' + hp); pg.wait_for_timeout(600)
    pg.screenshot(path=out, type='jpeg', quality=93); b.close()
os.remove(hp)
print('ok', out)
