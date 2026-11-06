#!/usr/bin/env python
"""Carrossel da série "Acaba com a bagunça / Padronizar" (8 slides 1080x1350).
Uso: .venv/bin/python scripts/carrossel_serie.py posts/<pasta> [--out saida/final]
Lê posts/<pasta>/trabalho/conteudo.json e gera <slug>-01.jpg ... <slug>-08.jpg + previa.jpg.
O Designer NÃO escreve código: só preenche o JSON (modelo em posts/2026-11-07-vendas/trabalho/conteudo.json).
Roda em primeiro plano, 30 a 60 s."""
import json, sys, re
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = Path('/Users/dmelo/Documents/03-Marketing/fabrica-conteudo')
if len(sys.argv) < 2: sys.exit(__doc__)
post = (ROOT / sys.argv[1]).resolve()
out = post / (sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else 'saida/final')
out.mkdir(parents=True, exist_ok=True)
C = json.loads((post / 'trabalho/conteudo.json').read_text())
slug = C['slug']

# base visual da série (CSS, cabeçalho, rodapé, helpers) vem do primeiro post da série
base = ROOT / 'posts/2026-10-31-atendimento/trabalho/build_final.py'
src = base.read_text(); ns = {'__file__': str(base)}
exec(src[:src.index('B={}')], ns)
wb = ns['wb']; W7 = ns['W7']; XI = ns['XI']; EXTRA = ns['EXTRA']; items = ns['items']

ROBO = C.get('robo', str(ROOT / 'posts/2026-11-02-stories-venda/trabalho/robo-recorte.png'))
ICON_BAG = '<svg width="128" height="128" viewBox="0 0 96 96" fill="none"><g transform="rotate(-14 30 40)"><rect x="12" y="18" width="40" height="48" rx="6" fill="#fff" stroke="#c2410c" stroke-width="3"/><path d="M20 32h24M20 42h24M20 52h14" stroke="#c2410c" stroke-width="3" stroke-linecap="round"/></g><g transform="rotate(12 62 46)"><rect x="42" y="26" width="40" height="46" rx="6" fill="#fff" stroke="#c2410c" stroke-width="3"/><path d="M50 40h24M50 50h18M50 60h22" stroke="#c2410c" stroke-width="3" stroke-linecap="round"/></g><path d="M30 70c-10 0-16 6-16 12 0 4 3 7 8 8l-3 6 9-6h12c6 0 10-4 10-8s-4-12-20-12z" fill="#e5392f"/><text x="39" y="87" font-family="Archivo,Arial" font-weight="800" font-size="16" fill="#fff">?</text><circle cx="78" cy="18" r="11" fill="#e5392f"/><path d="M74 14l8 8M82 14l-8 8" stroke="#fff" stroke-width="3" stroke-linecap="round"/></svg>'
ICON_PRO = '<svg width="128" height="128" viewBox="0 0 96 96" fill="none"><rect x="20" y="10" width="56" height="74" rx="8" fill="#fff" stroke="#15803d" stroke-width="3"/><rect x="34" y="4" width="28" height="12" rx="4" fill="#15803d"/><g stroke="#15803d" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M29 34l5 5 9-9"/><path d="M50 36h18"/><path d="M29 50l5 5 9-9"/><path d="M50 52h18"/><path d="M29 66l5 5 9-9"/><path d="M50 68h12"/></g><circle cx="78" cy="78" r="13" fill="#15803d"/><path d="M72 78l4 4 8-8" stroke="#fff" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARROW = '<svg width="54" height="34" viewBox="0 0 54 34" fill="none"><path d="M4 17h40" stroke="#8b94a6" stroke-width="5" stroke-linecap="round"/><path d="M34 6l12 11-12 11" stroke="#8b94a6" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
EXTRA += """<style>
.map2{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:44px}
.nd2{flex:1;height:262px;border-radius:28px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;text-align:center}
.nd2 small{font-size:21px;letter-spacing:4px;font-weight:800;margin-top:2px}
.nd2 b{font-size:33px;letter-spacing:-1px;font-weight:800;line-height:1}
.b1{background:#fdecea;border:3px solid #f3b7af}.b1 small,.b1 b{color:#c2410c}
.b2{background:radial-gradient(circle at 50% 40%,#2a1a3a 0%,#0f1830 70%);border:3px solid #0f1830}.b2 img{height:176px;display:block}.b2 small{color:#fff;margin-top:4px}
.b3{background:#e9f7ec;border:3px solid #a9dcb3}.b3 small,.b3 b{color:#15803d}
.ar2{flex:0 0 54px;display:flex;align-items:center;justify-content:center}
</style>"""
MAPA = ('<div class="map2"><div class="nd2 b1">' + ICON_BAG + '<small>HOJE</small><b>BAGUNÇA</b></div><div class="ar2">' + ARROW +
        '</div><div class="nd2 b2"><img src="file://' + ROBO + '"><small>CLAUDE</small></div><div class="ar2">' + ARROW +
        '</div><div class="nd2 b3">' + ICON_PRO + '<small>VIRA</small><b>PROCESSO</b></div></div>')

def title(s, size=None):
    st = f' style="font-size:{size}px"' if size else ''
    return f'<div class="t"{st}>{s}</div>'

def slide_html(n, s):
    h = f'<div class="eye">{s["eye"]}</div>' + title(s['title'], s.get('size'))
    if 'items' in s:
        h += items(s['items'], XI if s.get('icon') == 'x' else W7)
    if 'steps' in s:
        h += '<div class="st3">' + ''.join(f'<div class="stp"><b>{i}</b>{x}</div>' for i, x in enumerate(s['steps'], 1)) + '</div>'
    if 'text' in s:
        h += f'<div class="ap" style="font-size:{s.get("text_size",46)}px;margin-top:50px">{s["text"]}</div>'
    if 'ap' in s:
        h += f'<div class="ap">{s["ap"]}</div>'
    return h

B = {}
cp = C['capa']
B[1] = wb(f'<div class="eye">{cp["eye"]}</div>' + title(cp['title'], cp.get('size', 84)) + f'<div class="ap">{cp["ap"]}</div>' + (MAPA if cp.get('mapa', True) else ''), 1, 'arrasta')
for i, s in enumerate(C['slides'], 2):
    B[i] = wb(slide_html(i, s), i, 'arrasta')
ct = C['cta']
B[8] = wb(f'<div class="eye">{ct["palavra"]}</div>' + title(f'Comenta <r>{ct["palavra"]}</r>', 96) +
          f'<div class="cmt"><div class="u">você &middot; agora</div><div class="w">{ct["palavra"]}</div></div><div class="ap">{ct["texto"]}</div>', 8, ct.get('rodape', 'arrasta'))
assert len(B) == 8, f'precisa de exatamente 6 slides no meio (tem {len(C["slides"])})'

html_dir = post / 'trabalho/html'; html_dir.mkdir(exist_ok=True)
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome')
    for i, h in B.items():
        h = h.replace('</head>', EXTRA + '</head>')
        hp = html_dir / f'{i:02d}.html'; hp.write_text(h)
        pg = br.new_page(viewport={'width': 1080, 'height': 1350}, device_scale_factor=2)
        pg.goto(f'file://{hp}'); pg.wait_for_timeout(500)
        over = pg.evaluate("()=>{const m=document.querySelector('.main');return m.scrollHeight-m.clientHeight}")
        cut = pg.evaluate("()=>Math.max(0,...[...document.querySelectorAll('.t,.w')].map(e=>e.scrollWidth-e.clientWidth))")
        if over > 0 or cut > 0: print(f'AVISO slide {i}: texto vazando (altura {over}px, largura {cut}px)')
        pg.screenshot(path=str(post / 'trabalho/t.png')); pg.close()
        Image.open(post / 'trabalho/t.png').convert('RGB').resize((1080, 1350), Image.LANCZOS).save(out / f'{slug}-{i:02d}.jpg', quality=95)
    br.close()
(post / 'trabalho/t.png').unlink()
ims = [Image.open(out / f'{slug}-{i:02d}.jpg').resize((540, 675)) for i in range(1, 9)]
g = Image.new('RGB', (540 * 4 + 50, 675 * 2 + 30), 'white')
for k, im in enumerate(ims): g.paste(im, (10 + (k % 4) * 550, 10 + (k // 4) * 685))
g.save(out / 'previa.jpg', quality=90)
print('ok', out, '8 slides + previa.jpg')
