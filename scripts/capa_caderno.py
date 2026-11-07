#!/usr/bin/env python3
"""Capa em caderno pautado (modelo @nataliateixeira.ia): papel com margem e furos, '5' em pincel, título cursivo, foto recortada à direita, clipe e fita.
Uso: .venv/bin/python scripts/capa_caderno.py clientes/<cliente>/marca.json capa_caderno.json saida.jpg
capa_caderno.json: {"foto":"recorte.png (RGBA)","pill":"ESTA SEMANA","num":"5","palavra":"tarefas","linhas":["que voltam","pra sua mesa","toda semana"],
  "sub1":"pra você ensinar ao","dest":"Claude","sub2":"esta semana","foto_w":900,"foto_x":330}
"""
import json, os, sys, base64
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(sys.argv[1])); C = json.load(open(sys.argv[2])); out = os.path.abspath(sys.argv[3])
COR = M['cor']
f64 = base64.b64encode(open(C['foto'], 'rb').read()).decode() if C.get('foto') else ''
ROUGH = open(os.path.join(HERE, 'vendor', 'rough.js')).read()
F = lambda n: os.path.join(HERE, 'fonts', n)
fw = C.get('foto_w', 900); fx = C.get('foto_x', 330)
linhas = ''.join(f'<div>{l}</div>' for l in C['linhas'])
ROBO_JS = """
const svg=document.getElementById('rb'),rc=rough.svg(svg);let seed=5;
const o=x=>Object.assign({roughness:1.4,bowing:1.3,strokeWidth:5,stroke:'#111',seed:(seed+=13)},x||{});
const hach=(c,g)=>({fill:c,fillStyle:'hachure',hachureGap:g||12,fillWeight:2,hachureAngle:-41});
const box=(x,y,w,h,x2)=>svg.appendChild(rc.rectangle(x,y,w,h,o(x2)));
const ell=(cx,cy,w,h,x2)=>svg.appendChild(rc.ellipse(cx,cy,w,h,o(x2)));
const line=(a,b,c,d,x2)=>svg.appendChild(rc.line(a,b,c,d,o(x2)));
const lp=(p,x2)=>svg.appendChild(rc.linearPath(p,o(x2)));
const RED='__COR__',HIL='#ffe27a';
const s=290,x=150,y=130,hw=s,hh=s*0.8;
line(x+hw/2,y,x+hw/2+4,y-s*0.22,{strokeWidth:5});
ell(x+hw/2+4,y-s*0.28,s*0.14,s*0.14,Object.assign({stroke:RED},hach(RED,5)));
box(x,y,hw,hh,Object.assign({strokeWidth:5.5},hach(HIL,12)));
box(x-s*0.07,y+hh*0.35,s*0.07,hh*0.3,{strokeWidth:4});box(x+hw,y+hh*0.35,s*0.07,hh*0.3,{strokeWidth:4});
ell(x+hw*0.30,y+hh*0.36,s*0.17,s*0.17,Object.assign({stroke:RED,roughness:1},hach(RED,4)));
ell(x+hw*0.70,y+hh*0.36,s*0.17,s*0.17,Object.assign({stroke:RED,roughness:1},hach(RED,4)));
lp([[x+hw*0.28,y+hh*0.66],[x+hw*0.40,y+hh*0.80],[x+hw*0.60,y+hh*0.80],[x+hw*0.72,y+hh*0.66]],{strokeWidth:5,roughness:1});
box(x+hw*0.25,y+hh+8,hw*0.5,s*0.22,{strokeWidth:4.5});
const by=y+hh+8+s*0.22+4, bx=x+hw*0.08, bw=hw*0.84;
box(bx,by,bw,330,Object.assign({strokeWidth:5.5},hach('#f4a7a1',14)));
ell(bx+bw/2,by+90,70,70,Object.assign({stroke:RED,strokeWidth:5},hach(RED,6)));
// bracos abertos: sobem em V
const ay=by+50;
line(bx,ay,bx-140,ay-100,{strokeWidth:9});line(bx+bw,ay,bx+bw+140,ay-100,{strokeWidth:9});
box(bx-175,ay-170,70,70,Object.assign({strokeWidth:5},hach(HIL,9)));box(bx+bw+105,ay-170,70,70,Object.assign({strokeWidth:5},hach(HIL,9)));
"""
def _b64(path): return base64.b64encode(open(path, 'rb').read()).decode()
if C.get('robo_png'):
    FIGURA = ('<img style="position:absolute;left:%spx;bottom:%spx;width:%spx" src="data:image/png;base64,%s">'
              % (C.get('png_x', 455), C.get('png_b', 50), C.get('png_w', 610), _b64(C['robo_png'])))
elif C.get('robo'):
    FIGURA = '<svg id="rb" style="position:absolute;left:460px;top:520px" width="610" height="830"></svg><script>' + ROUGH + '</script><script>' + ROBO_JS.replace('__COR__', COR) + '</script>'
else:
    FIGURA = '<img class="foto" src="data:image/png;base64,' + f64 + '">'
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Caveat;font-weight:700;src:url('file://{F('Caveat-Bold.ttf')}')}}
@font-face{{font-family:Archivo;src:url('file://{F('Archivo.ttf')}');font-weight:100 900}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;overflow:hidden;position:relative;background:#f7f0e1 repeating-linear-gradient(180deg,transparent 0,transparent 53px,rgba(120,140,170,.30) 53px,rgba(120,140,170,.30) 55px);font-family:Caveat,cursive;color:#161616}}
.mg{{position:absolute;left:92px;top:0;bottom:0;width:3px;background:rgba(229,57,47,.5)}}
.holes{{position:absolute;left:18px;top:0;bottom:0;width:40px;background:radial-gradient(circle at 20px 20px,#e9dfc9 0 14px,#b3a68a 14px 16px,transparent 17px) 0 0/40px 86px repeat-y}}
.five{{position:absolute;left:70px;top:-116px;font-size:800px;line-height:1;color:{COR};filter:url(#rough);letter-spacing:-10px}}
.pill{{position:absolute;left:112px;top:46px;font-family:Archivo;font-weight:800;font-size:24px;letter-spacing:3px;background:{COR};color:#fff;padding:10px 22px;border-radius:999px}}
.pal{{position:absolute;left:100px;top:560px;font-size:176px;line-height:1;transform:rotate(-4deg);transform-origin:left;filter:url(#rough2)}}
.ul{{position:absolute;left:100px;top:722px;width:470px;height:30px}}
.txt{{position:absolute;left:112px;top:766px;font-size:66px;line-height:1.02;font-weight:700;transform:rotate(-2deg);transform-origin:left}}
.sub{{position:absolute;left:112px;top:985px;font-size:60px;line-height:1.04;transform:rotate(-2deg);transform-origin:left}}
.dest:before{{content:'';position:absolute;left:-26px;right:-26px;top:6px;bottom:-4px;background:{COR};opacity:.9;filter:url(#rough3);border-radius:8px;z-index:-1}}
.dest{{position:relative;font-size:92px;line-height:1.05;color:#fff;display:inline-block;margin:10px 0 8px 22px;z-index:1}}
.foto{{position:absolute;left:{fx}px;bottom:0;width:{fw}px}}
.clip{{position:absolute;right:50px;top:-26px}}
.tape{{position:absolute;left:-70px;bottom:14px;width:230px;height:84px;background:rgba(196,168,128,.78);transform:rotate(-24deg);box-shadow:0 2px 8px rgba(0,0,0,.15)}}
.star{{position:absolute;left:250px;bottom:38px}}
.faisca{{position:absolute;right:130px;top:130px}}
</style></head><body>
<svg width="0" height="0" style="position:absolute"><defs>
<filter id="rough" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" seed="4" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="16"/></filter>
<filter id="rough2"><feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" seed="9" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="5"/></filter>
<filter id="rough3"><feTurbulence type="fractalNoise" baseFrequency="0.04 0.12" numOctaves="3" seed="2" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="22"/></filter>
</defs></svg>
<div class="mg"></div><div class="holes"></div>
<div class="pill">{C['pill']}</div>
<div class="five">{C['num']}</div>
<div class="pal">{C['palavra']}</div>
<svg class="ul" viewBox="0 0 520 30" fill="none"><path d="M6 14 C120 6 300 20 512 8" stroke="{COR}" stroke-width="9" stroke-linecap="round" filter="url(#rough2)"/><path d="M30 26 C160 20 330 28 470 20" stroke="{COR}" stroke-width="5" stroke-linecap="round"/></svg>
<div class="txt">{linhas}</div>
<div class="sub">{C['sub1']}<br><span class="dest">{C['dest']}</span><br>{C['sub2']}</div>
{FIGURA}
<svg class="clip" width="90" height="190" viewBox="0 0 90 190" fill="none"><path d="M55 20 L55 140 C55 170 20 170 20 140 L20 40 C20 8 70 8 70 40 L70 130" stroke="{COR}" stroke-width="7" stroke-linecap="round"/></svg>
<svg style="position:absolute;left:560px;top:150px" width="200" height="190" viewBox="0 0 200 190" stroke="{COR}" stroke-width="9" stroke-linecap="round"><path d="M20 130L70 100M60 60L90 20M120 40L130 6M30 80L6 72"/></svg>
<svg style="position:absolute;left:60px;top:300px" width="80" height="140" viewBox="0 0 80 140" stroke="{COR}" stroke-width="8" stroke-linecap="round"><path d="M70 20L26 40M60 80L10 70"/></svg>
<div class="tape"></div>
<svg class="star" width="90" height="90" viewBox="0 0 120 120" stroke="{COR}" stroke-width="9" stroke-linecap="round"><path d="M60 8V112M8 60H112M23 23L97 97M97 23L23 97"/></svg>
</body></html>"""
hp = out + '.html'; open(hp, 'w').write(html)
with sync_playwright() as p:
    try: b = p.chromium.launch(channel="chrome")
    except Exception: b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1080, 'height': 1350}); pg.goto('file://' + hp); pg.wait_for_timeout(700)
    pg.screenshot(path=out, type='jpeg', quality=93); b.close()
print('ok', out)
