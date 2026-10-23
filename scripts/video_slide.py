#!/usr/bin/env python3
"""Transforma um vídeo em slide 1080x1350 de carrossel com cabeçalho da marca e texto em português.
Uso: .venv/bin/python scripts/video_slide.py clientes/<cliente>/marca.json entrada.mp4 saida.mp4 "Texto com <b>destaque</b>" [--crop W:H:X:Y] [--y 410] [--ate 27] [--sobre]
--crop  recorta só a área do vídeo original (tira faixas, legendas e marca d'água de quem repostou)
--y     altura onde o vídeo entra no quadro preto (padrão: centralizado abaixo do cabeçalho)
--ate   corta o vídeo nesse segundo
--sobre texto por cima do vídeo com degradê (use quando o vídeo já é 4:5 e limpo)
Regra: só use filmagem original/oficial. Não apague marca d'água de criador; corte apenas a moldura que ele colocou em volta de imagem que não é dele.
"""
import json, os, sys, subprocess, argparse
from playwright.sync_api import sync_playwright

def abrir_navegador(p):
    """Usa o Google Chrome instalado no Mac. Se não tiver, usa o Chromium do Playwright."""
    try:
        return p.chromium.launch(channel="chrome")
    except Exception:
        return p.chromium.launch()

HERE = os.path.dirname(os.path.abspath(__file__))
a = argparse.ArgumentParser(); a.add_argument('marca'); a.add_argument('ent'); a.add_argument('sai'); a.add_argument('texto')
a.add_argument('--crop'); a.add_argument('--y', type=int); a.add_argument('--ate', type=float); a.add_argument('--sobre', action='store_true')
o = a.parse_args(); M = json.load(open(o.marca))
top = 60 if o.sobre else 200
bg = 'background:linear-gradient(#000e 0,#000c 60%,transparent)' if o.sobre else ''
html = f'''<html><head><meta charset=utf-8><style>@font-face{{font-family:Archivo;src:url(file://{HERE}/fonts/Archivo.ttf);font-weight:100 900}}
*{{margin:0}}body{{width:1080px;height:1350px;background:transparent;font-family:Archivo,sans-serif;color:#fff}}
.h{{position:absolute;left:0;right:0;top:0;padding:{top}px 60px 60px;{bg}}}.t{{font-size:46px;font-weight:700;line-height:1.25}}.t b{{color:{M.get('cor_destaque_escuro', M['cor'])}}}</style></head>
<body><div class=h><div style="display:flex;align-items:center;gap:16px;margin-bottom:22px"><img src="file://{os.path.abspath(M['foto_perfil'])}" style="width:64px;height:64px;border-radius:50%;object-fit:cover;border:3px solid {M['cor']}">
<div style="font-weight:800;font-size:30px">{M['nome']} <span style="color:#1d9bf0">✔</span> <span style="font-weight:500;color:#aaa">{M['handle']}</span></div></div><div class=t>{o.texto}</div></div></body></html>'''
tmp = o.sai + '.ov.html'; png = o.sai + '.ov.png'; open(tmp, 'w').write(html)
with sync_playwright() as p:
    b = abrir_navegador(p); pg = b.new_page(viewport={'width': 1080, 'height': 1350})
    pg.goto('file://' + os.path.abspath(tmp)); pg.wait_for_timeout(300); pg.screenshot(path=png, omit_background=True); b.close()
if o.sobre:
    vf = '[0:v]scale=1080:1350:force_original_aspect_ratio=increase,crop=1080:1350,setsar=1[b]'
else:
    crop = f'crop={o.crop},' if o.crop else ''
    y = o.y if o.y is not None else '(oh-ih)/2+120'
    vf = f'[0:v]{crop}scale=1080:-2,pad=1080:1350:0:{y}:black,setsar=1[b]'
cmd = ['ffmpeg', '-v', 'error', '-y'] + (['-t', str(o.ate)] if o.ate else []) + ['-i', o.ent, '-i', png, '-filter_complex', vf + ';[b][1:v]overlay=0:0,format=yuv420p',
       '-c:v', 'libx264', '-crf', '20', '-preset', 'medium', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', o.sai]
subprocess.run(cmd, check=True); os.remove(tmp); os.remove(png); print('ok', o.sai)
