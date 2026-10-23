#!/usr/bin/env python3
"""Slides internos no modelo TICKETS (combina com capa_tickets.py): fundo preto, título Anton em caixa alta
com destaque amarelo, tickets coloridos (post-it com fita), passos numerados e caixa de prompt pronta pra copiar.
Uso: .venv/bin/python scripts/slides_tickets.py clientes/<cliente>/marca.json slides_tickets.json pasta_saida [inicio]
slides_tickets.json: {"slug": "...", "slides": [ {"pill": "...", "titulo": ["LINHA", "<y>DESTAQUE</y>"],
   "blocos": [ {"tipo": "texto", "txt": "..."},
               {"tipo": "onde", "txt": "Chat do Claude, no celular"},
               {"tipo": "tickets", "itens": [["/conversar", "pensar uma decisão"], ...]},   (até 4, grade 2x2)
               {"tipo": "passos", "itens": ["Conte a situação", "..."]},
               {"tipo": "prompt", "txt": "Vou decidir [X]..."},
               {"tipo": "tabela", "itens": [["Tarefa", "/ticket", cor_idx], ...]},
               {"tipo": "ordem", "itens": ["Mapa", "Gargalo", "Ferramenta"]},
               {"tipo": "cta", "palavra": "QUATRO", "txt": "que eu te mando ...", "nota": "Precisa me seguir"} ],
   "foot": "texto do rodapé direito (padrão ARRASTA →)"} ]}
Cores dos tickets por índice: 0 amarelo, 1 rosa, 2 verde, 3 laranja, 4 azul, 5 lilás.
"""
import json, os, sys, base64, html as H
from PIL import Image
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(sys.argv[1])); D = json.load(open(sys.argv[2])); OUT = os.path.abspath(sys.argv[3])
INI = int(sys.argv[4]) if len(sys.argv) > 4 else 1
os.makedirs(OUT, exist_ok=True)
CORES = ['#ffe45c', '#ffb3c7', '#9ee6a8', '#ffc58f', '#9fd3ff', '#d9c2ff']
av = os.path.abspath(M.get('foto_perfil', ''))
av64 = base64.b64encode(open(av, 'rb').read()).decode() if av and os.path.isfile(av) else ''
F = lambda n: os.path.join(HERE, 'fonts', n)

def y(t):
    return t.replace('<y>', '<span class="y">').replace('</y>', '</span>')

def printbox(b, L, with_caption=True):
    im = Image.open(b['img']); iw, ih = im.size; k = L / iw
    caixas = b.get('caixas') or [b['caixa']]
    img64 = base64.b64encode(open(b['img'], 'rb').read()).decode()
    hls = ''.join(f'<div class="hl" style="left:{int(x*k)-6}px;top:{int(yy*k)-6}px;width:{int(w*k)+12}px;height:{int(h*k)+12}px"></div>' for x, yy, w, h in caixas)
    box = (f'<div class="pbox" style="width:{L}px;height:{int(ih*k)}px">'
           f'<img src="data:image/png;base64,{img64}" style="width:{L}px;height:{int(ih*k)}px">{hls}</div>')
    if not with_caption:
        return box
    return f'<div class="pw">{box}<div class="pc"><b>ONDE</b><p>{y(b.get("txt",""))}</p></div></div>'

def bloco(b, i):
    t = b['tipo']
    if t == 'texto':
        return f'<p class="txt">{y(b["txt"])}</p>'
    if t == 'onde':
        return f'<div class="onde"><b>ONDE</b>{y(b["txt"])}</div>'
    if t == 'tickets':
        s = ''
        for k, it in enumerate(b['itens']):
            rot = [-2.5, 2, 1.5, -2][k % 4]; cor = CORES[it[2] if len(it) > 2 else k]
            s += f'<div class="tk" style="background:{cor};transform:rotate({rot}deg)"><i></i><div class="tl">{it[0]}</div><div class="ts">{it[1]}</div></div>'
        return f'<div class="grid">{s}</div>'
    if t == 'passos':
        return '<div class="passos">' + ''.join(f'<div class="ps"><span>{k+1}</span><div>{y(p)}</div></div>' for k, p in enumerate(b['itens'])) + '</div>'
    if t == 'prompt':
        return f'<div class="pr"><div class="pl">{b.get("label","PROMPT PRA COPIAR")}</div><div class="pt">{y(H.escape(b["txt"]).replace("&lt;y&gt;","<y>").replace("&lt;/y&gt;","</y>"))}</div></div>'
    if t == 'tabela':
        s = ''
        for it in b['itens']:
            cor = CORES[it[2] if len(it) > 2 else 0]
            s += f'<div class="tr"><div class="tt">{it[0]}</div><div class="chip" style="background:{cor}">{it[1]}</div></div>'
        return f'<div class="tab">{s}</div>'
    if t == 'ordem':
        n = len(b['itens'])
        s = ''.join(f'<div class="od{" last" if k==n-1 else ""}"><span>{k+1}</span>{it}</div>' + ('<div class="ar">→</div>' if k < n-1 else '') for k, it in enumerate(b['itens']))
        return f'<div class="ordem">{s}</div>'
    if t == 'print':
        return printbox(b, b.get('larg', 600), with_caption=True)
    if t == 'jeitos':
        out = ''
        for k, it in enumerate(b['itens']):
            cor = CORES[it.get('cor', k)]
            out += (f'<div class="jr"><div class="jt" style="background:{cor}"><div class="tl">{it["label"]}</div><div class="ts">{it["sub"]}</div></div>'
                    f'<div class="ja">→</div>{printbox(it, b.get("larg", 330), with_caption=False)}</div>')
        return f'<div class="jw">{out}</div>'
    if t == 'cta':
        avimg = ('<img src="data:image/jpeg;base64,' + av64 + '">') if av64 else ''
        return (f'<div class="cta"><div class="cm"><div class="cav">{avimg}</div>'
                f'<div><div class="cu">você</div><div class="cw">{b["palavra"]}</div></div></div>'
                f'<p class="ctxt">Comenta <span class="y">{b["palavra"]}</span> {b["txt"]}</p>'
                f'<div class="cn">{b.get("nota","")}</div></div>')
    return ''

CSS = f"""
@font-face{{font-family:Anton;src:url('file://{F('Anton.woff2')}')}}
@font-face{{font-family:Archivo;src:url('file://{F('Archivo.ttf')}')}}
@font-face{{font-family:Caveat;src:url('file://{F('Caveat-Bold.ttf')}')}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;background:#0b0b0b;color:#fff;overflow:hidden;font-family:Archivo,sans-serif;position:relative}}
.bar{{position:absolute;left:0;right:0;top:0;height:10px;background:{M['cor']}}}
.head{{position:absolute;top:40px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:12px;font-weight:800;font-size:28px}}
.head img{{width:46px;height:46px;border-radius:50%;object-fit:cover}} .head span{{color:rgba(255,255,255,.6);font-weight:500}}
.wrap{{position:absolute;left:72px;right:72px;top:130px;bottom:110px;display:flex;flex-direction:column;gap:32px}}
.pill{{align-self:flex-start;background:#ffd23f;color:#111;font-weight:900;font-size:24px;letter-spacing:1.5px;padding:10px 18px;border-radius:6px}}
.tit{{font-family:Anton,sans-serif;font-size:96px;line-height:1.03;text-transform:uppercase;margin-top:-6px}}
.y{{color:#ffd23f}}
.txt{{font-size:38px;line-height:1.4;color:rgba(255,255,255,.82)}}
.onde{{font-size:34px;color:rgba(255,255,255,.85);display:flex;gap:16px;align-items:center}}
.onde b{{font-size:20px;letter-spacing:2px;background:#222;border:1px solid #444;color:#ffd23f;padding:6px 12px;border-radius:6px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:42px 34px;margin-top:10px}}
.tk{{position:relative;color:#111;padding:26px 26px 22px;box-shadow:0 14px 30px rgba(0,0,0,.5)}}
.tk i{{position:absolute;left:50%;top:-13px;width:84px;height:26px;margin-left:-42px;background:rgba(255,255,255,.55)}}
.tl{{font-family:Caveat,cursive;font-size:66px;line-height:1}} .ts{{font-size:31px;font-weight:600;margin-top:8px;line-height:1.25}}
.passos{{display:flex;flex-direction:column;gap:20px}}
.ps{{display:flex;gap:24px;align-items:flex-start;font-size:38px;line-height:1.3;font-weight:600}}
.ps span{{flex:none;width:64px;height:64px;border-radius:50%;background:#ffd23f;color:#111;font-family:Anton;font-size:34px;display:flex;align-items:center;justify-content:center}}
.pr{{background:#161616;border:2px dashed #ffd23f;border-radius:14px;padding:22px 28px}}
.pl{{font-size:20px;letter-spacing:2px;font-weight:900;color:#ffd23f;margin-bottom:12px}}
.pt{{font-size:32px;line-height:1.4;color:#fff}}
.tab{{display:flex;flex-direction:column;gap:28px}}
.tr{{display:flex;justify-content:space-between;align-items:center;gap:20px;border-bottom:1px solid #2a2a2a;padding-bottom:16px}}
.tt{{font-size:37px;font-weight:600;line-height:1.25}}
.chip{{flex:none;color:#111;font-family:Caveat,cursive;font-size:52px;padding:6px 20px;transform:rotate(-2deg);box-shadow:0 8px 18px rgba(0,0,0,.5)}}
.ordem{{display:flex;align-items:center;gap:14px}}
.od{{flex:1;background:#1a1a1a;border:2px solid #333;border-radius:14px;padding:36px 12px;text-align:center;font-family:Anton;font-size:48px;text-transform:uppercase}}
.od span{{display:block;font-family:Archivo;font-size:22px;color:#999;margin-bottom:6px}}
.od.last{{background:#ffd23f;color:#111;border-color:#ffd23f}} .od.last span{{color:#333}}
.ar{{font-size:44px;color:#ffd23f}}
.cta{{display:flex;flex-direction:column;gap:26px;margin-top:10px}}
.cm{{display:flex;gap:20px;align-items:center;background:#161616;border-radius:18px;padding:26px 30px}}
.cav{{width:96px;height:96px;border-radius:50%;background:#333;overflow:hidden}} .cav img{{width:100%;height:100%;object-fit:cover}}
.cu{{font-size:24px;color:#999}} .cw{{font-family:Anton;font-size:96px;color:#ffd23f;letter-spacing:2px}}
.ctxt{{font-size:48px;line-height:1.3;font-weight:700}} .cn{{font-size:32px;color:rgba(255,255,255,.65)}}
.pw{{display:flex;gap:28px;align-items:center}}
.pbox{{position:relative;flex:none;border-radius:14px;overflow:hidden;box-shadow:0 14px 36px rgba(0,0,0,.6);border:2px solid #333}}
.pbox img{{display:block;image-rendering:auto}}
.hl{{position:absolute;border:5px solid #ffd23f;border-radius:12px;box-shadow:0 0 0 4px rgba(255,210,63,.25),0 0 28px rgba(255,210,63,.6)}}
.pc{{font-size:30px;line-height:1.35;color:rgba(255,255,255,.85);display:flex;flex-direction:column;gap:10px}}
.pc b{{align-self:flex-start;font-size:20px;letter-spacing:2px;background:#222;border:1px solid #444;color:#ffd23f;padding:6px 12px;border-radius:6px}}
.jw{{display:flex;flex-direction:column;gap:26px;margin-top:6px}}
.jr{{display:flex;align-items:center;gap:20px}}
.jt{{flex:none;width:430px;color:#111;padding:18px 22px;box-shadow:0 10px 24px rgba(0,0,0,.5);transform:rotate(-1.5deg)}}
.jt .tl{{font-size:54px}} .jt .ts{{font-size:25px}}
.ja{{font-size:52px;color:#ffd23f;font-weight:900}}
.foot{{position:absolute;left:72px;right:72px;bottom:44px;display:flex;justify-content:space-between;font-size:24px;color:rgba(255,255,255,.6)}}
.foot b{{color:#fff;letter-spacing:2px}}
"""

with sync_playwright() as p:
    try:
        br = p.chromium.launch(channel="chrome")
    except Exception:
        br = p.chromium.launch()
    pg = br.new_page(viewport={'width': 1080, 'height': 1350})
    for k, s in enumerate(D['slides']):
        n = INI + k
        corpo = ''.join(bloco(b, k) for b in s.get('blocos', []))
        tit = '<br>'.join(y(l) for l in s['titulo'])
        doc = f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="bar"></div>
<div class="head">{('<img src="data:image/jpeg;base64,'+av64+'">') if av64 else ''}<b>{M['nome']}</b><span>{M['handle']}</span></div>
<div class="wrap"><div class="pill">{s.get('pill','')}</div><div class="tit">{tit}</div>{corpo}</div>
<div class="foot"><span>{M['handle']}</span><b>{s.get('foot','ARRASTA →')}</b></div></body></html>"""
        hp = os.path.join(OUT, f'{n:02d}.html'); open(hp, 'w').write(doc)
        pg.goto('file://' + hp); pg.wait_for_timeout(400)
        pg.screenshot(path=os.path.join(OUT, f"{D.get('slug','slide')}-{n:02d}.jpg"), type='jpeg', quality=92)
    br.close()
print('ok', len(D['slides']))
