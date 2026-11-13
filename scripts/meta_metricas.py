#!/usr/bin/env python3
"""Lê métricas da Meta Graph API (só GET, nunca cria, altera ou apaga nada).

Uso (da raiz da pasta):
  .venv/bin/python scripts/meta_metricas.py --dias 7 --posts 30 --anuncios [--cliente jesse-rodolfo]

Saída: pesquisa/metricas/<AAAA-MM-DD>.json e pesquisa/metricas/<AAAA-MM-DD>-resumo.md
O token vem do .env (META_USER_TOKEN) e nunca é impresso nem gravado.
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

import requests

RAIZ = Path(__file__).resolve().parent.parent
AVISOS = []

METRICAS_CONTA = [
    "reach", "views", "profile_views", "accounts_engaged", "total_interactions",
    "likes", "comments", "saves", "shares", "follows_and_unfollows",
    "profile_links_taps", "website_clicks",
]
METRICAS_POST = [
    "reach", "views", "likes", "comments", "saved", "shares",
    "total_interactions", "follows", "profile_visits",
]
METRICAS_REEL = ["ig_reels_avg_watch_time", "ig_reels_video_view_total_time", "reels_skip_rate"]
# Leitura por reel pro placar dos testes (scripts/melhor_teste.py). reels_skip_rate = % que saiu nos 3 primeiros segundos.
METRICAS_TESTE = ["views", "reach", "shares", "saved", "ig_reels_avg_watch_time", "reels_skip_rate"]
PUBLICO = ["follower_demographics", "engaged_audience_demographics"]
CORTES = ["age", "gender", "city"]


def carregar_env():
    env = {}
    p = RAIZ / ".env"
    if p.exists():
        for linha in p.read_text().splitlines():
            linha = linha.strip()
            if not linha or linha.startswith("#") or "=" not in linha:
                continue
            k, v = linha.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


class Graph:
    def __init__(self, token, versao):
        self.token = token
        self.base = f"https://graph.facebook.com/{versao}"
        self.s = requests.Session()

    def get(self, caminho, params=None, aviso=None):
        """GET. Devolve (json, None) ou (None, mensagem de erro). Registra aviso se pedido."""
        p = dict(params or {})
        p["access_token"] = self.token
        url = caminho if caminho.startswith("http") else f"{self.base}/{caminho.lstrip('/')}"
        try:
            r = self.s.get(url, params=p, timeout=60)
            j = r.json()
        except Exception as e:  # rede ou JSON inválido
            msg = f"{type(e).__name__}"
            if aviso:
                AVISOS.append(f"{aviso}: {msg}")
            return None, msg
        if "error" in j:
            msg = j["error"].get("message", "erro")
            if aviso:
                AVISOS.append(f"{aviso}: {msg}")
            return None, msg
        return j, None

    def paginar(self, caminho, params, maximo=None, aviso=None):
        itens = []
        j, err = self.get(caminho, params, aviso)
        while j:
            itens += j.get("data", [])
            if maximo and len(itens) >= maximo:
                return itens[:maximo], None
            prox = j.get("paging", {}).get("next")
            if not prox:
                break
            j, err = self.get(prox, None, aviso)
        return itens, err


def ts(d):
    return int(d.timestamp())


def valor_total(item):
    tv = item.get("total_value")
    return tv.get("value") if tv else None


def insights_conta(g, ig, dias, hoje):
    fim = dt.datetime.combine(hoje, dt.time.min, tzinfo=dt.timezone.utc)
    ini = fim - dt.timedelta(days=dias)
    out = {"periodo": {"de": ini.date().isoformat(), "ate": (fim.date() - dt.timedelta(days=1)).isoformat(), "dias": dias}}
    j, _ = g.get(ig, {"fields": "username,followers_count,follows_count,media_count"}, "conta (campos basicos)")
    out["perfil"] = j or {}
    # alcance diário
    j, _ = g.get(f"{ig}/insights", {"metric": "reach", "period": "day", "since": ts(ini), "until": ts(fim + dt.timedelta(days=1))}, "alcance diario")
    diario = {}
    if j and j.get("data"):
        for v in j["data"][0].get("values", []):
            diario[v["end_time"][:10]] = v["value"]
    out["alcance_diario_bruto"] = diario
    # métricas totais, uma a uma para isolar recusas
    tot = {}
    for m in METRICAS_CONTA:
        j, _ = g.get(f"{ig}/insights", {"metric": m, "period": "day", "metric_type": "total_value",
                                         "since": ts(ini), "until": ts(fim)}, f"conta metrica {m}")
        if j and j.get("data"):
            tot[m] = valor_total(j["data"][0])
        if m == "follows_and_unfollows" and tot.get(m) is None:
            j, _ = g.get(f"{ig}/insights", {"metric": m, "period": "day", "metric_type": "total_value", "breakdown": "follow_type",
                                             "since": ts(ini), "until": ts(fim)}, "conta follows_and_unfollows (breakdown follow_type)")
            if j and j.get("data"):
                tv = j["data"][0].get("total_value", {})
                bd = tv.get("breakdowns", [{}])[0].get("results", []) if tv.get("breakdowns") else []
                tot["follows"] = sum(r["value"] for r in bd if r["dimension_values"][0] == "FOLLOWER")
                tot["unfollows"] = sum(r["value"] for r in bd if r["dimension_values"][0] == "NON_FOLLOWER")
                tot.pop(m, None)
    out["totais"] = tot
    return out


def publico(g, ig):
    out = {}
    for m in PUBLICO:
        out[m] = {}
        for c in CORTES:
            res = None
            for tf in ("this_month", "this_week", None):
                p = {"metric": m, "period": "lifetime", "metric_type": "total_value", "breakdown": c}
                if tf:
                    p["timeframe"] = tf
                j, err = g.get(f"{ig}/insights", p)
                if j and j.get("data"):
                    bd = j["data"][0].get("total_value", {}).get("breakdowns", [])
                    res = [{"chave": "/".join(r["dimension_values"]), "valor": r["value"]}
                           for r in (bd[0].get("results", []) if bd else [])]
                    res.sort(key=lambda x: -x["valor"])
                    break
            if res is None:
                AVISOS.append(f"publico {m} por {c}: recusado ou sem dados (menos de 100 seguidores/engajados, ou metrica indisponivel)")
            out[m][c] = res
    return out


def posts(g, ig, n, ini_periodo):
    campos = "id,media_type,media_product_type,timestamp,caption,permalink"
    itens, _ = g.paginar(f"{ig}/media", {"fields": campos, "limit": min(n, 50)}, n, "lista de posts")
    ruins = {}  # tipo -> metricas recusadas
    saida = []
    for it in itens:
        tipo = it.get("media_product_type") if it.get("media_product_type") == "REELS" else it.get("media_type")
        eh_reel = tipo == "REELS"
        pedir = METRICAS_POST + (METRICAS_REEL if eh_reel else [])
        pedir = [m for m in pedir if m not in ruins.get(tipo, set())]
        ins = {}
        j, err = g.get(f"{it['id']}/insights", {"metric": ",".join(pedir)})
        if j is None:
            # isola as recusadas uma vez por tipo
            for m in pedir:
                jj, e2 = g.get(f"{it['id']}/insights", {"metric": m})
                if jj and jj.get("data"):
                    ins[m] = jj["data"][0]["values"][0]["value"]
                else:
                    ruins.setdefault(tipo, set()).add(m)
                    AVISOS.append(f"post {tipo} metrica {m}: {e2}")
        else:
            for d in j.get("data", []):
                ins[d["name"]] = d["values"][0]["value"]
        reach = ins.get("reach") or 0
        tx = {}
        if reach:
            tx["interacoes_por_alcance"] = round((ins.get("total_interactions") or 0) / reach, 4)
            tx["salvamentos_por_alcance"] = round((ins.get("saved") or 0) / reach, 4)
            tx["compartilhamentos_por_alcance"] = round((ins.get("shares") or 0) / reach, 4)
            tx["seguidores_por_1000_alcance"] = round((ins.get("follows") or 0) / reach * 1000, 2)
        data = it.get("timestamp", "")[:10]
        saida.append({
            "id": it["id"], "tipo": tipo, "data": data,
            "em_periodo": bool(data and data >= ini_periodo),
            "legenda": (it.get("caption") or "").replace("\n", " ")[:120],
            "permalink": it.get("permalink"),
            "insights": ins, "taxas": tx,
        })
    return saida


def codigo_do_link(url):
    """https://www.instagram.com/reel/ABC123/ vira ABC123."""
    partes = [x for x in (url or "").split("?")[0].split("/") if x]
    return partes[-1] if partes else ""


def reels_por_link(g, ig, links, maximo=80):
    """Métricas por reel a partir do link do Instagram. Só GET.

    Devolve {link: {"id", "data", "views", "reach", "shares", "saved", "tempo_medio_s", "pulo", "avisos"}}.
    Métrica que a API não devolveu fica None (vazio não é zero: os números podem atrasar até 48 h).
    Reel que não aparece na lista de mídia da conta (pode acontecer com reel de teste) não entra no resultado.
    """
    codigos = {codigo_do_link(u): u for u in links if codigo_do_link(u)}
    itens, _ = g.paginar(f"{ig}/media", {"fields": "id,permalink,timestamp,media_product_type", "limit": 50}, maximo)
    out = {}
    for it in itens:
        cod = codigo_do_link(it.get("permalink"))
        if cod not in codigos:
            continue
        ins, avisos = {}, []
        j, err = g.get(f"{it['id']}/insights", {"metric": ",".join(METRICAS_TESTE)})
        if j is None:
            for m in METRICAS_TESTE:  # isola a métrica recusada
                jj, e2 = g.get(f"{it['id']}/insights", {"metric": m})
                if jj and jj.get("data"):
                    ins[m] = jj["data"][0]["values"][0]["value"]
                else:
                    avisos.append(f"{m}: {e2}")
        else:
            for d in j.get("data", []):
                ins[d["name"]] = d["values"][0]["value"]
        t = ins.get("ig_reels_avg_watch_time")
        out[codigos[cod]] = {
            "id": it["id"], "data": it.get("timestamp", "")[:10],
            "views": ins.get("views"), "reach": ins.get("reach"),
            "shares": ins.get("shares"), "saved": ins.get("saved"),
            "tempo_medio_s": round(t / 1000, 2) if t is not None else None,  # a API devolve em milissegundos
            "pulo": ins.get("reels_skip_rate"), "avisos": avisos,
        }
    return out


def acao(lista, tipos):
    for a in lista or []:
        if a.get("action_type") in tipos:
            return float(a["value"])
    return None


def anuncios(g, act):
    camp, _ = g.paginar(f"{act}/campaigns",
                        {"fields": "id,name,objective,status,effective_status,created_time", "limit": 100},
                        None, "campanhas")
    campos = ("campaign_id,spend,reach,impressions,cpm,clicks,ctr,cpc,inline_link_clicks,actions,"
              "cost_per_action_type,video_play_actions,video_avg_time_watched_actions,"
              "video_thruplay_watched_actions,video_p25_watched_actions,video_p50_watched_actions,"
              "video_p75_watched_actions,video_p100_watched_actions")
    ins, err = g.paginar(f"{act}/insights", {"level": "campaign", "date_preset": "maximum", "fields": campos, "limit": 100},
                         None, "insights de anuncios (maximum)")
    if not ins:
        ins, _ = g.paginar(f"{act}/insights", {"level": "campaign", "fields": campos, "limit": 100,
                           "time_range": json.dumps({"since": "2024-01-01", "until": dt.date.today().isoformat()})},
                           None, "insights de anuncios (time_range)")
    por_id = {i["campaign_id"]: i for i in ins}
    mapa_resultado = {
        "OUTCOME_ENGAGEMENT": ["post_engagement", "page_engagement"],
        "OUTCOME_TRAFFIC": ["link_click", "landing_page_view"],
        "OUTCOME_LEADS": ["lead", "onsite_conversion.lead_grouped"],
        "OUTCOME_SALES": ["purchase", "offsite_conversion.fb_pixel_purchase"],
        "OUTCOME_AWARENESS": [],
        "POST_ENGAGEMENT": ["post_engagement"],
        "LINK_CLICKS": ["link_click"],
        "REACH": [],
    }
    saida = []
    for c in camp:
        i = por_id.get(c["id"], {})
        spend = float(i.get("spend", 0) or 0)
        reach = int(i.get("reach", 0) or 0)
        tipos = mapa_resultado.get(c.get("objective"), ["post_engagement"])
        resultado, custo_res, rotulo = None, None, None
        if tipos:
            for t in tipos:
                v = acao(i.get("actions"), [t])
                if v:
                    resultado, rotulo = v, t
                    custo_res = acao(i.get("cost_per_action_type"), [t])
                    if custo_res is None and v:
                        custo_res = round(spend / v, 4)
                    break
        elif reach and spend:
            resultado, rotulo, custo_res = reach, "alcance", round(spend / reach * 1000, 2)  # custo por 1000 alcançadas
        visitas = None
        for a in i.get("actions", []) or []:
            if "profile" in a.get("action_type", "") and "visit" in a.get("action_type", ""):
                visitas = float(a["value"])
        video = {}
        for k in ("video_play_actions", "video_thruplay_watched_actions", "video_p25_watched_actions",
                  "video_p50_watched_actions", "video_p75_watched_actions", "video_p100_watched_actions",
                  "video_avg_time_watched_actions"):
            v = i.get(k)
            if v:
                video[k] = float(v[0]["value"])
        saida.append({
            "id": c["id"], "nome": c.get("name"), "objetivo": c.get("objective"),
            "status": c.get("effective_status") or c.get("status"),
            "gasto_reais": round(spend, 2), "alcance": reach,
            "impressoes": int(i.get("impressions", 0) or 0),
            "cpm": round(float(i["cpm"]), 2) if i.get("cpm") else None,
            "cliques": int(i.get("clicks", 0) or 0),
            "ctr": round(float(i["ctr"]), 2) if i.get("ctr") else None,
            "cpc": round(float(i["cpc"]), 2) if i.get("cpc") else None,
            "resultado_tipo": rotulo, "resultado": resultado, "custo_por_resultado": custo_res,
            "visitas_perfil": visitas, "video": video,
            "acoes": {a["action_type"]: float(a["value"]) for a in (i.get("actions") or [])},
        })
    return saida


def pagina_fb(g, page):
    j, _ = g.get(page, {"fields": "name,fan_count,followers_count"}, "pagina do Facebook")
    return j or {}


# ---------- resumo ----------
def pct(x):
    return f"{x * 100:.1f}%" if x is not None else "-"


def fmt_seg(s):
    return f"{s:.1f}s" if s is not None else "-"


def linha_post(p):
    i, t = p["insights"], p["taxas"]
    return (f"| {p['data']} | {p['legenda'][:50]} | {i.get('reach', '-')} | {pct(t.get('interacoes_por_alcance'))} "
            f"| {i.get('saved', '-')} | {i.get('shares', '-')} | {p['permalink'] or ''} |")


def tabela_posts(titulo, lista):
    if not lista:
        return [f"**{titulo}**: sem posts.", ""]
    L = [f"**{titulo}**", "", "| Data | Legenda | Alcance | Inter/alcance | Salv | Comp | Link |", "|---|---|---|---|---|---|---|"]
    L += [linha_post(p) for p in lista]
    return L + [""]


def top_piores(lista, chave, n=5):
    v = [p for p in lista if chave(p) is not None]
    v.sort(key=chave, reverse=True)
    return v[:n], v[::-1][:n] if len(v) > n else []


def gerar_resumo(d):
    c, P = d["conta"], d["posts"]
    L = [f"# Métricas Meta, {d['gerado_em']} ({d['cliente']})", ""]
    per = c["periodo"]
    L += [f"Período: {per['de']} a {per['ate']} ({per['dias']} dias). Seguidores: {c['perfil'].get('followers_count', '-')}.", ""]
    L += ["## Conta", "", "| Métrica | Total no período |", "|---|---|"]
    for k, v in c["totais"].items():
        L.append(f"| {k} | {v} |")
    if c["alcance_diario"]:
        L += ["", "Alcance diário (rótulo = end_time da Meta, ou seja, o dia anterior à data): " + ", ".join(f"{k[5:]}={v}" for k, v in sorted(c["alcance_diario"].items()))]
    L.append("")
    L += ["## Público", ""]
    for m, cortes in d["publico"].items():
        for corte, res in cortes.items():
            if res:
                tot = sum(r["valor"] for r in res) or 1
                L.append(f"- {m} por {corte}: " + ", ".join(f"{r['chave']} {r['valor'] / tot * 100:.0f}%" for r in res[:4]))
    L.append("")
    L += ["## Posts", ""]
    for nome, tipos in (("Reels", ["REELS"]), ("Carrosséis", ["CAROUSEL_ALBUM"]), ("Imagens", ["IMAGE"])):
        sub = [p for p in P if p["tipo"] in tipos and p["insights"].get("reach") is not None]
        if not sub:
            continue
        L += [f"### {nome} ({len(sub)} posts)", ""]
        t, w = top_piores(sub, lambda p: p["insights"].get("reach"))
        L += tabela_posts(f"Top 5 por alcance ({nome})", t) + tabela_posts(f"Piores 5 por alcance ({nome})", w)
        t, w = top_piores(sub, lambda p: p["taxas"].get("interacoes_por_alcance"))
        L += tabela_posts(f"Top 5 por interações/alcance ({nome})", t) + tabela_posts(f"Piores 5 por interações/alcance ({nome})", w)
    A = d.get("anuncios")
    if A is not None:
        L += ["## Anúncios antigos (lifetime, por custo por resultado)", ""]
        L += ["| Campanha | Obj | Status | Gasto R$ | Alcance | CPM | Cliques | CTR% | CPC | Resultado | Custo/res |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
        for a in sorted(A, key=lambda a: (a["custo_por_resultado"] is None, a["custo_por_resultado"] or 0)):
            L.append(f"| {(a['nome'] or '')[:40]} | {a['objetivo']} | {a['status']} | {a['gasto_reais']} | {a['alcance']} | {a['cpm']} "
                     f"| {a['cliques']} | {a['ctr']} | {a['cpc']} | {a['resultado']} ({a['resultado_tipo']}) | {a['custo_por_resultado']} |")
        L += ["", f"Gasto total: R$ {sum(a['gasto_reais'] for a in A):.2f}", ""]
    fb = d.get("pagina_facebook", {})
    L += ["## Página do Facebook", "", f"fan_count={fb.get('fan_count', '-')}, followers_count={fb.get('followers_count', '-')}", ""]
    # Pro criativo
    L += ["## Pro criativo", ""]
    com = [p for p in P if p["insights"].get("reach") is not None]
    por_tipo = {}
    for p in com:
        por_tipo.setdefault(p["tipo"], []).append(p)
    for tipo, v in sorted(por_tipo.items(), key=lambda kv: -sum(p["insights"]["reach"] for p in kv[1]) / len(kv[1])):
        med = sum(p["insights"]["reach"] for p in v) / len(v)
        mi = [p["taxas"]["interacoes_por_alcance"] for p in v if "interacoes_por_alcance" in p["taxas"]]
        L.append(f"- {tipo}: {len(v)} posts, alcance médio {med:.0f}, interações/alcance médio {pct(sum(mi) / len(mi)) if mi else '-'}.")
    if por_tipo:
        melhor = max(por_tipo.items(), key=lambda kv: sum(p["insights"]["reach"] for p in kv[1]) / len(kv[1]))[0]
        L.append(f"- Formato que mais alcança em média: {melhor}.")
    top = sorted(com, key=lambda p: -p["insights"]["reach"])[:5]
    if top:
        L.append("- Legendas dos 5 posts de maior alcance (veja o tema): " + " | ".join(f"\"{p['legenda'][:60]}\" ({p['insights']['reach']})" for p in top))
    seg = sorted([p for p in com if "seguidores_por_1000_alcance" in p["taxas"] and p["insights"].get("follows")],
                 key=lambda p: -p["taxas"]["seguidores_por_1000_alcance"])[:3]
    if seg:
        L.append("- Mais seguidores por 1000 de alcance: " + " | ".join(f"\"{p['legenda'][:50]}\" ({p['taxas']['seguidores_por_1000_alcance']})" for p in seg))
    wt = [p["insights"]["ig_reels_avg_watch_time"] for p in com if p["insights"].get("ig_reels_avg_watch_time") is not None]
    if wt:
        # a API devolve em milissegundos
        L.append(f"- Tempo médio assistido dos reels: {sum(wt) / len(wt) / 1000:.1f}s (média de {len(wt)} reels).")
    if A:
        com_res = [a for a in A if a["custo_por_resultado"] and a["gasto_reais"] > 0]
        if com_res:
            m = min(com_res, key=lambda a: a["custo_por_resultado"])
            L.append(f"- Anúncio mais barato por resultado: \"{m['nome']}\" ({m['resultado_tipo']}, R$ {m['custo_por_resultado']}).")
    if d["avisos"]:
        L += ["", "## Avisos (métricas recusadas)", ""] + [f"- {a}" for a in d["avisos"]]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Lê métricas da Meta (só leitura)")
    ap.add_argument("--cliente", default="jesse-rodolfo")
    ap.add_argument("--dias", type=int, default=7)
    ap.add_argument("--posts", type=int, default=30)
    ap.add_argument("--anuncios", action="store_true")
    ap.add_argument("--reels-links", help="links de reels separados por vírgula: imprime só as métricas deles em JSON e sai")
    a = ap.parse_args()

    marca = json.loads((RAIZ / "clientes" / a.cliente / "marca.json").read_text())
    meta = marca["meta"]
    token = carregar_env().get("META_USER_TOKEN")
    if not token:
        sys.exit("META_USER_TOKEN ausente no .env")
    g = Graph(token, meta.get("api_version", "v21.0"))
    if a.reels_links:
        print(json.dumps(reels_por_link(g, meta["ig_user_id"], a.reels_links.split(",")), ensure_ascii=False, indent=1))
        return
    hoje = dt.date.today()
    ini = (hoje - dt.timedelta(days=a.dias)).isoformat()

    dados = {"cliente": a.cliente, "gerado_em": hoje.isoformat(), "dias": a.dias}
    conta = insights_conta(g, meta["ig_user_id"], a.dias, hoje)
    conta["alcance_diario"] = conta.pop("alcance_diario_bruto")
    dados["conta"] = conta
    dados["publico"] = publico(g, meta["ig_user_id"])
    dados["posts"] = posts(g, meta["ig_user_id"], a.posts, ini)
    if a.anuncios:
        dados["anuncios"] = anuncios(g, meta["ad_account"])
    dados["pagina_facebook"] = pagina_fb(g, meta["page_id"])
    dados["avisos"] = sorted(set(AVISOS))

    out = RAIZ / "pesquisa" / "metricas"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{hoje}.json").write_text(json.dumps(dados, ensure_ascii=False, indent=2))
    (out / f"{hoje}-resumo.md").write_text(gerar_resumo(dados))
    print(f"ok: {out}/{hoje}.json e {hoje}-resumo.md | posts={len(dados['posts'])} avisos={len(dados['avisos'])}")


if __name__ == "__main__":
    main()
