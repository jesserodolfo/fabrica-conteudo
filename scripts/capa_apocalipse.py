#!/usr/bin/env python3
"""Capa 1080x1920 do reel NOTÍCIAS (cópia adaptada de capa_reel.py): título grande + post inclinado na frente.
Uso: .venv/bin/python scripts/capa_apocalipse.py A|B saida.jpg"""
import os, sys, base64, subprocess, tempfile
from playwright.sync_api import sync_playwright
from PIL import Image
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
P=ROOT+'/posts/2026-11-08-reel-noticias'
opt=sys.argv[1]; out=os.path.abspath(sys.argv[2]); tmp=tempfile.mkdtemp()
fr=tmp+'/f.png'; subprocess.run(['ffmpeg','-v','error','-y','-ss','12','-i',P+'/bruto/noticia.mp4','-frames:v','1',fr],check=True)
b64=lambda p:base64.b64encode(open(p,'rb').read()).decode()
post=Image.open('posts/2026-11-08-reel-noticias/telas/crop-05b.png'); pp=tmp+'/p.png'; post.save(pp)
F=lambda n:os.path.join(HERE,'fonts',n)
common=f"""@font-face{{font-family:Archivo;src:url('file://{F('Archivo.ttf')}')}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;overflow:hidden;position:relative;background:#09090b;font-family:Archivo,sans-serif;color:#fff}}
.tit{{position:absolute;left:40px;right:40px;text-align:center;z-index:5}}
.t1{{font-weight:900;font-size:128px;line-height:.98;letter-spacing:-3px;text-transform:uppercase;text-shadow:0 8px 40px rgba(0,0,0,.7)}}
.t1 em{{font-style:normal;color:#ff3b30}}
.sub{{display:inline-block;margin-top:26px;font-family:Georgia,serif;font-style:italic;font-size:62px;border:3px solid #e5392f;background:rgba(229,57,47,.18);padding:2px 28px 10px;text-shadow:0 4px 20px rgba(0,0,0,.6)}}
.post{{position:absolute;border-radius:28px;overflow:hidden;z-index:6;box-shadow:0 50px 100px rgba(0,0,0,.75),0 0 0 6px #fff,0 0 120px rgba(229,57,47,.45)}}
.post img{{width:100%;display:block}}"""
if opt=='A':
    css=common+f"""
.bg{{position:absolute;inset:0;background:url(data:image/png;base64,{b64(fr)}) center/cover}}
.sh{{position:absolute;inset:0;background:linear-gradient(#000e 0,#0009 22%,#0000 40%,#0000 70%,#000a 100%)}}
.tit{{top:270px}}
.post{{left:680px;top:1190px;width:390px;transform:rotate(7deg)}}"""
    body=f'<div class="bg"></div><div class="sh"></div>'
else:
    css=common+f"""
.bg{{position:absolute;inset:0;background:radial-gradient(ellipse 80% 45% at 50% 60%,rgba(229,57,47,.38),transparent 70%),#09090b}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.05) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.05) 2px,transparent 2px);background-size:90px 90px}}
.vid{{position:absolute;left:330px;top:740px;width:740px;height:880px;border-radius:30px;overflow:hidden;transform:rotate(4deg);box-shadow:0 40px 90px #000a,0 0 0 3px #fff3;z-index:3;background:url(data:image/png;base64,{b64(fr)}) 50px -300px/820px auto}}
.tit{{top:280px}}
.post{{left:10px;top:1040px;width:470px;transform:rotate(-7deg)}}"""
    body='<div class="bg"></div><div class="grid"></div><div class="vid"></div>'
html=f"""<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{body}
<div class="tit"><div class="t1">Será o<br><em>apocalipse?</em></div><div class="sub">olha essa semana</div></div>
<div class="post"><img src="data:image/png;base64,{b64(pp)}"></div></body></html>"""
hp=tmp+'/c.html'; open(hp,'w').write(html)
with sync_playwright() as p:
    try: b=p.chromium.launch(channel='chrome')
    except Exception: b=p.chromium.launch()
    pg=b.new_page(viewport={'width':1080,'height':1920}); pg.goto('file://'+hp); pg.wait_for_timeout(600)
    print(pg.evaluate("()=>[...document.querySelectorAll('.t1,.sub,.post')].map(e=>{const r=e.getBoundingClientRect();return e.className+' '+[r.left,r.top,r.right,r.bottom].map(Math.round)})"))
    pg.screenshot(path=out,type='jpeg',quality=93); b.close()
