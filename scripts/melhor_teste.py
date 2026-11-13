#!/usr/bin/env python3
"""Placar dos reels de teste (09h30) e botão "Postar no perfil 18h".

Regra do guia (pesquisa/2026-11-12-reels-de-teste/guia-texto.txt, decidir.py), sempre contra a mediana do próprio lote:
  pulo (reels_skip_rate) acima da mediana  = gancho fraco, regravar os 3 primeiros segundos
  % assistido abaixo da mediana            = o meio cansa, cortar
  vencedor = passou nos 2 cortes e tem mais views em 72 h; desempate por compartilhamentos por mil views
Métrica vazia NÃO é zero (chega em até 24 h, pode atrasar 48 h): aparece "sem dado ainda" e não entra no ranking.

Fontes, só leitura: Zernio (status, link e analytics do post) e Meta (scripts/meta_metricas.py, pelo link do reel).
Uso (da raiz): .venv/bin/python scripts/melhor_teste.py [--ensaio] [--hoje AAAA-MM-DD] [--nao-enviar]
  --ensaio: prefixo ENSAIO, sem botão de perfil e sem gravar o placar do dia.
Grava saidas/lote-teste/placar-<hoje>.json (é o que o botão pf|placar-<hoje>|<slug> usa). Nenhuma chave é impressa.
"""
import datetime as dt
import json
import os
import re
import statistics as st
import subprocess
import sys
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lote_comum as lc  # noqa: E402

RAIZ, SAIDA = lc.RAIZ, lc.SAIDA
BRT = dt.timezone(dt.timedelta(hours=-3))
AVISOS = []


def env():
    e = {}
    for linha in (RAIZ / ".env").read_text().splitlines():
        linha = linha.strip()
        if linha and not linha.startswith("#") and "=" in linha:
            k, v = linha.split("=", 1)
            e[k.strip()] = v.strip().strip('"').strip("'")
    return e


def zernio(key, caminho):
    req = urllib.request.Request("https://zernio.com/api/v1" + caminho, headers={"Authorization": f"Bearer {key}"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"erro": f"HTTP {e.code}"}
    except Exception as e:
        return {"erro": type(e).__name__}


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def duracao(video):
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(RAIZ / video)],
                           capture_output=True, text=True, timeout=30)
        return float(r.stdout.strip() or 0)
    except Exception:
        return 0.0


def mais_novo(pasta, padrao):
    arqs = sorted((RAIZ / pasta).glob(padrao), key=lambda p: p.stat().st_mtime)
    return str(arqs[-1].relative_to(RAIZ)) if arqs else ""


def coletar():
    """Testes agendados: manifestos do lote e zernio_teste.txt das pastas (pilotos)."""
    testes, vistos = [], set()
    for arq in sorted(SAIDA.glob("20*.json")):
        try:
            _, itens = lc.ler(arq.stem)
        except Exception:
            continue
        for it in itens:
            pid = it.get("post_id")
            if pid and pid not in vistos:
                vistos.add(pid)
                testes.append({"slug": it.get("slug"), "palavra": str(it.get("palavra") or it.get("slug")).upper(),
                               "pasta": it.get("pasta"), "video": it.get("video"), "capa": it.get("capa"),
                               "duracao": float(it.get("duracao") or 0), "post_id": pid})
    for arq in sorted((RAIZ / "posts").glob("*/zernio_teste.txt")):
        m = re.search(r"reel teste (\S+).*?post ([0-9a-f]{24})", arq.read_text(encoding="utf-8"))
        if not m or m.group(2) in vistos:
            continue
        vistos.add(m.group(2))
        pasta = str(arq.parent.relative_to(RAIZ))
        pal = m.group(1).upper()
        testes.append({"slug": re.sub(r"[^a-z0-9]+", "-", sem_acento(pal).lower()).strip("-") or "teste", "palavra": pal,
                       "pasta": pasta, "video": mais_novo(pasta, "saida/*.mp4"), "capa": mais_novo(pasta, "capa/capa-reel*.jpg"),
                       "duracao": 0.0, "post_id": m.group(2)})
    return testes


def numero(v):
    """None, vazio ou zero de métrica ainda não sincronizada vira None."""
    try:
        v = float(v)
    except (TypeError, ValueError):
        return None
    return v if v > 0 else None


def ler_metricas(testes, e):
    key = e.get("ZERNIO_API_KEY", "")
    for t in testes:
        p = zernio(key, f"/posts/{t['post_id']}")
        if "erro" in p:
            AVISOS.append(f"Zernio não respondeu pro {t['palavra']} ({p['erro']})")
            t["status"] = "?"
            continue
        ig = [x for x in p.get("post", {}).get("platforms", []) if x.get("platform") == "instagram"]
        ig = ig[0] if ig else {}
        t["status"] = ig.get("status") or p.get("post", {}).get("status")
        t["erro_zernio"] = str(ig.get("errorMessage") or ig.get("error") or "")[:300]
        t["link"] = ig.get("platformPostUrl") or ""
        pub = ig.get("publishedAt")
        if pub:
            q = dt.datetime.fromisoformat(pub.replace("Z", "+00:00")).astimezone(BRT)
            t["publicado_em"] = q.strftime("%Y-%m-%dT%H:%M")
            t["dia"] = q.date().isoformat()
        if t["status"] == "published":
            a = zernio(key, f"/analytics?postId={t['post_id']}").get("analytics") or {}
            tm = numero(a.get("igReelsAvgWatchTime"))
            t["z"] = {"views": numero(a.get("views")), "shares": a.get("shares") if numero(a.get("views")) else None,
                      "tempo_medio_s": tm / 1000 if tm else None, "pulo": numero(a.get("reelsSkipRate"))}
    links = [t["link"] for t in testes if t.get("link")]
    meta = {}
    if links:
        try:
            import meta_metricas as mm
            marca = json.loads((RAIZ / "clientes/jesse-rodolfo/marca.json").read_text())["meta"]
            tok = e.get("META_USER_TOKEN")
            if not tok:
                AVISOS.append("META_USER_TOKEN ausente: usei só o Zernio")
            else:
                g = mm.Graph(tok, marca.get("api_version", "v21.0"))
                j, err = g.get(marca["ig_user_id"], {"fields": "id"})
                if j is None:
                    AVISOS.append(f"Meta recusou a leitura ({str(err)[:80]}): usei só o Zernio")
                else:
                    meta = mm.reels_por_link(g, marca["ig_user_id"], links)
        except Exception as x:
            AVISOS.append(f"Meta falhou ({type(x).__name__}): usei só o Zernio")
    for t in testes:
        m, z = meta.get(t.get("link"), {}), t.get("z", {})
        pega = lambda k: m.get(k) if numero(m.get(k)) is not None else z.get(k)
        t["views"] = numero(pega("views"))
        t["pulo"] = numero(pega("pulo"))
        tm = numero(pega("tempo_medio_s"))
        sh = m.get("shares") if m.get("shares") is not None else z.get("shares")
        t["fonte"] = "meta" if numero(m.get("views")) is not None else ("zernio" if t["views"] else "")
        if not t.get("duracao") and t.get("video"):
            t["duracao"] = duracao(t["video"])
        if t["pulo"] is not None and t["pulo"] <= 1:
            t["pulo"] *= 100  # fração vira porcentagem, como no decidir.py
        if tm and t.get("duracao") and tm > t["duracao"]:
            tm = tm / 1000  # veio em milissegundos
        t["tempo_medio_s"] = tm
        t["assistido"] = 100 * tm / t["duracao"] if tm and t.get("duracao") else None
        t["comp_mil"] = 1000 * float(sh or 0) / max(t["views"], 1) if t["views"] else None
    return testes


def julgar(lote):
    """Aplica a regra do guia no lote. Devolve (medianas, vencedor ou None). Quem está vazio não é ranqueado."""
    com = [t for t in lote if t["views"] is not None and t["pulo"] is not None and t["assistido"] is not None]
    med = {}
    if com:
        med = {"pulo": st.median(t["pulo"] for t in com), "assistido": st.median(t["assistido"] for t in com),
               "views": st.median(t["views"] for t in com)}
    for t in lote:
        if t in com:
            t["ok"] = t["pulo"] <= med["pulo"] and t["assistido"] >= med["assistido"]
            t["veredito"] = ("passou nos 2 cortes" if t["ok"] else
                             "gancho fraco, regravar 3 s" if t["pulo"] > med["pulo"] else "o meio cansa, cortar")
        elif t.get("status") and t["status"] != "published":
            t["ok"], t["veredito"] = False, f"não publicou ({t['status']})"
        elif t["views"] is not None:
            t["ok"], t["veredito"] = False, "sem pulo e tempo ainda"
        else:
            t["ok"], t["veredito"] = False, "sem dado ainda"
    bons = [t for t in com if t["ok"]] or com
    venc = max(bons, key=lambda t: (t["views"], t["comp_mil"] or 0)) if bons else None
    return med, venc


def fmt(n):
    return f"{n:,.0f}".replace(",", ".")


def linha(t):
    if t["views"] is None:
        return f"🟡 {t['palavra']}: {t['veredito']}"
    partes = [f"{fmt(t['views'])} views"]
    partes.append(f"pulo {t['pulo']:.0f}%" if t["pulo"] is not None else "pulo sem dado")
    partes.append(f"assistido {t['assistido']:.0f}% ({t['tempo_medio_s']:.1f} s)".replace(".", ",") if t["assistido"] is not None else "assistido sem dado")
    bola = "🟢" if t.get("ok") else ("🟡" if "sem" in t["veredito"] else "🔴")
    return f"{bola} {t['palavra']}: " + " · ".join(partes) + f" · {t['veredito']}"


def bloco(titulo, lote):
    med, venc = julgar(lote)
    L = [titulo] + [linha(t) for t in sorted(lote, key=lambda t: -(t["views"] or 0))]
    if med:
        L.append(f"Mediana do lote: pulo {med['pulo']:.0f}%, assistido {med['assistido']:.0f}%, {fmt(med['views'])} views")
    return L, med, venc


def enviar(texto, markup=None):
    amb = dict(os.environ)
    amb.pop("TG_BOTOES", None)
    amb.pop("TG_REPLY_MARKUP", None)
    if markup:
        amb["TG_REPLY_MARKUP"] = json.dumps(markup, ensure_ascii=False)
    r = subprocess.run(["bash", str(RAIZ / "scripts/telegram_enviar.sh"), "texto", texto], env=amb, capture_output=True, text=True)
    print((r.stdout + r.stderr).strip())
    return r.returncode == 0


def main():
    ensaio = "--ensaio" in sys.argv
    hoje = dt.date.fromisoformat(sys.argv[sys.argv.index("--hoje") + 1]) if "--hoje" in sys.argv else dt.date.today()
    pref = "ENSAIO · " if ensaio else ""
    e = env()
    testes = ler_metricas(coletar(), e)
    d1, d3 = (hoje - dt.timedelta(days=1)).isoformat(), (hoje - dt.timedelta(days=3)).isoformat()
    ontem = [t for t in testes if t.get("dia") == d1]
    tres = [t for t in testes if t.get("dia") == d3]
    falhos = [t for t in testes if t.get("status") == "failed"]
    br = lambda d: f"{d[8:10]}/{d[5:7]}"
    print(f"testes conhecidos: {len(testes)} · de ontem ({d1}): {len(ontem)} · de 3 dias ({d3}): {len(tres)} · avisos: {AVISOS}")

    L = [f"{pref}Placar dos testes · {hoje.strftime('%d/%m')}"]
    botoes, placar = [], []
    if not ontem and not tres:
        L = [f"{pref}Placar dos testes: nenhum teste publicado ontem nem há 3 dias. Nada pra ler hoje."]
    elif not any(t["views"] is not None for t in ontem + tres):
        L = [f"{pref}Placar dos testes: os {len(ontem + tres)} teste(s) ainda estão sem número ({', '.join(t['palavra'] for t in ontem + tres)}). "
             "Os dados chegam em até 24 h e podem atrasar 48 h. Mando de novo amanhã."]
    else:
        def candidato(t):
            if t is None:
                return None
            if (RAIZ / t["pasta"] / "zernio.txt").is_file():
                L.append(f"{t['palavra']} já está no perfil (zernio.txt na pasta): sem botão.")
                return None
            return t
        if ontem:
            B, med, lider = bloco(f"\n24 h (gancho) · testes de {br(d1)}", ontem)
            L += B
            if lider:
                L.append(f"Líder de ontem: {lider['palavra']}")
                c = candidato(lider)
                if c:
                    botoes.append(c)
        if tres:
            B, med, venc = bloco(f"\n72 h (vencedor) · testes de {br(d3)}", tres)
            L += B
            if venc:
                turb = "fez 2x a mediana, candidato a turbinar" if venc["views"] >= 2 * med["views"] and len(tres) > 1 else "abaixo de 2x a mediana, não turbinar"
                L.append(f"Vencedor de 72 h: {venc['palavra']} ({turb})")
                L.append("Ou no app: Compartilhar com todos (mantém os números do teste)")
                c = candidato(venc)
                if c and c not in botoes:
                    botoes.append(c)
    for t in falhos:
        if t.get("dia") in (None, d1) or True:
            cod = "sem o botão Teste na conta (2207081)" if "2207081" in t.get("erro_zernio", "") else \
                  "limite de testes do dia (2207078)" if "2207078" in t.get("erro_zernio", "") else t.get("erro_zernio", "")[:120]
            L.append(f"🔴 {t['palavra']} não publicou: {cod or 'erro sem mensagem'}")
    if AVISOS:
        L.append("⚠️ " + "; ".join(AVISOS))

    markup = None
    if botoes and not ensaio:
        chave = f"placar-{hoje.isoformat()}"
        for t in botoes:
            placar.append({k: t.get(k) for k in ("slug", "palavra", "pasta", "video", "capa", "duracao", "post_id", "publicado_em",
                                                  "views", "pulo", "assistido", "veredito")})
        antigo, itens_antigos = (None, [])
        try:
            antigo, itens_antigos = lc.ler(chave)
        except Exception:
            pass
        for it in placar:  # rodar de novo no mesmo dia não perde o que já foi pedido
            velho = lc.achar(itens_antigos, it["slug"]) or {}
            for k in ("perfil_pedido", "perfil_pedido_em", "perfil_agendado", "perfil_horario", "perfil_post_id"):
                if k in velho:
                    it[k] = velho[k]
        lc.salvar(chave, {"data": hoje.isoformat(), "videos": placar})
        linhas = [[{"text": f"📌 Postar {t['palavra']} no perfil 18h", "callback_data": f"pf|{chave}|{t['slug']}"}] for t in botoes]
        linhas.append([{"text": "Hoje não", "callback_data": "pn"}])
        markup = {"inline_keyboard": linhas}
    elif botoes and ensaio:
        L.append("(ensaio: no modo real viriam os botões " + ", ".join(f"Postar {t['palavra']} no perfil 18h" for t in botoes) + " e Hoje não)")

    texto = "\n".join(L).replace(chr(8212), ",").replace(chr(8211), ",")
    print(texto)
    if "--nao-enviar" in sys.argv:
        return 0
    return 0 if enviar(texto, markup) else 1


if __name__ == "__main__":
    sys.exit(main())
