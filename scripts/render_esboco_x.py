#!/usr/bin/env python3
"""render_esboco_robo.py + tipo "listax" (lista com X vermelho no lugar do visto). Não altera esboco.js.
Uso: igual ao render_esboco_robo.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import render_esboco as R
src = open(os.path.join(HERE, 'esboco.js')).read()
NOVO = """T.listax=()=>{const n=D.items.length,gap=24,h=(H-gap*(n-1))/n;
 D.items.forEach((it,i)=>{const y=i*(h+gap),last=i===n-1;
  box(0,y,W,h,{fill:last?HIL:null,fo:{hachureGap:15,fillWeight:1.5},sw:3.6});
  xmark(48,y+h/2,17,RED,6.5);
  if(it.d){txt(104,y+h*0.36,it.t,{size:fit(it.t,W-130,36,700)});txt(104,y+h*0.72,it.d,{size:fit(it.d,W-130,28,400),wt:400,c:'#555'});}
  else txt(104,y+h/2+2,it.t,{size:fit(it.t,W-130,40,700)});});};
"""
js = src.replace("(T[D.type]||(()=>{}))();", NOVO + "(T[D.type]||(()=>{}))();")
assert NOVO in js
orig = R.html_slide
def patched(s, M, spec):
    h = orig(s, M, spec)
    h = h.replace(src, js)
    if spec.get('robo_img'):
        img = os.path.abspath(spec['robo_img'])
        h = h.replace('</body>', f'<img src="file://{img}" style="position:absolute;left:50%;top:{spec.get("y",760)}px;height:{spec.get("h",420)}px;transform:translateX(-50%) rotate(-3deg)"></body>')
    return h
R.html_slide = patched
R.main()
