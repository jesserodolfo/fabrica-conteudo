#!/usr/bin/env python3
"""Igual ao render_esboco.py, mas cola o robô (PNG original, nunca redesenhado) no slide 1 se esboco.json tiver "robo": caminho.
Uso: .venv/bin/python scripts/render_esboco_robo.py marca.json slides.json esboco.json saida  (esboco.json: {"robo":"...png","slides":[...]})"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import render_esboco as R
orig = R.html_slide
ROBO = {}
def patched(s, M, spec):
    h = orig(s, M, spec)
    if spec.get('robo_img'):
        img = os.path.abspath(spec['robo_img'])
        tag = f'<img src="file://{img}" style="position:absolute;left:50%;top:{spec.get("y",760)}px;height:{spec.get("h",420)}px;transform:translateX(-50%) rotate(-3deg)">'
        h = h.replace('</body>', tag + '</body>')
    return h
R.html_slide = patched
R.main()
