#!/usr/bin/env python3
"""CLI de anuncios na Meta (Graph API). Tudo nasce PAUSED. Uso:
.venv/bin/python scripts/meta_ads.py <contas|impulsionar|campanha|ativar|pausar|apagar|relatorio|listar> ...
O token fica no .env (META_USER_TOKEN) e nunca e impresso."""
import argparse, json, os, sys, time, datetime as dt
from pathlib import Path
import requests

RAIZ = Path(__file__).resolve().parent.parent
ANUNCIOS = RAIZ / "anuncios"
REGISTRO = ANUNCIOS / "registro.jsonl"
LIMITES = ANUNCIOS / "limites.json"


def carregar_env():
    f = RAIZ / ".env"
    if f.exists():
        for ln in f.read_text().splitlines():
            ln = ln.strip()
            if not ln or ln.startswith("#") or "=" not in ln:
                continue
            k, v = ln.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


class MetaErro(Exception):
    def __init__(self, resp):
        self.resp = resp
        e = resp.get("error", resp) if isinstance(resp, dict) else {"message": str(resp)}
        self.txt = (f"message={e.get('message')} | error_user_title={e.get('error_user_title')} | "
                    f"error_user_msg={e.get('error_user_msg')} | code={e.get('code')} | "
                    f"subcode={e.get('error_subcode')} | fbtrace={e.get('fbtrace_id')}")
        super().__init__(self.txt)


class Meta:
    def __init__(self, cliente):
        carregar_env()
        self.tok = os.environ.get("META_USER_TOKEN")
        if not self.tok:
            sys.exit("META_USER_TOKEN ausente no .env")
        m = json.loads((RAIZ / "clientes" / cliente / "marca.json").read_text())["meta"]
        self.m = m
        self.base = f"https://graph.facebook.com/{m['api_version']}"
        self.conta = m["ad_account"]
        self.num = self.conta.replace("act_", "")

    def _do(self, metodo, caminho, params=None, data=None, files=None):
        try:
            r = requests.request(metodo, f"{self.base}/{caminho.lstrip('/')}",
                                 params=(params or {}) if metodo == "GET" else None,
                                 data=data if metodo != "GET" else None, files=files, timeout=300,
                                 headers={"Authorization": f"Bearer {self.tok}"})
        except requests.RequestException as e:
            raise MetaErro({"error": {"message": f"erro de rede: {type(e).__name__}"}}) from None
        try:
            j = r.json()
        except Exception:
            j = {"error": {"message": r.text[:500]}}
        if isinstance(j, dict) and "error" in j:
            raise MetaErro(j)
        return j

    def get(self, c, **p):
        return self._do("GET", c, params=p)

    def post(self, c, files=None, **d):
        d = {k: (json.dumps(v) if isinstance(v, (dict, list)) else v) for k, v in d.items() if v is not None}
        return self._do("POST", c, data=d, files=files)

    def delete(self, c):
        return self._do("DELETE", c)


def log(acao, **kw):
    ANUNCIOS.mkdir(exist_ok=True)
    kw = {"data": dt.datetime.now().isoformat(timespec="seconds"), "acao": acao, **kw}
    with REGISTRO.open("a") as f:
        f.write(json.dumps(kw, ensure_ascii=False) + "\n")


def registro_campanha(cid):
    achado = None
    if REGISTRO.exists():
        for ln in REGISTRO.read_text().splitlines():
            try:
                j = json.loads(ln)
            except Exception:
                continue
            if j.get("acao") == "impulsionar" and j.get("campanha") == cid:
                achado = j
    return achado


def limites():
    try:
        return json.loads(LIMITES.read_text())
    except FileNotFoundError:
        return {}
    except Exception:
        print("RECUSADO: anuncios/limites.json ilegivel. Corrija antes de subir ou ativar.")
        sys.exit(2)


def checar_limites(dia, total):
    l = limites()
    if l.get("orcamento_dia_max") is not None and dia > l["orcamento_dia_max"]:
        print(f"RECUSADO: orcamento/dia R$ {dia:.2f} passa do teto R$ {l['orcamento_dia_max']:.2f} (anuncios/limites.json)")
        sys.exit(2)
    if l.get("total_campanha_max") is not None and total > l["total_campanha_max"]:
        print(f"RECUSADO: total R$ {total:.2f} passa do teto R$ {l['total_campanha_max']:.2f} (anuncios/limites.json)")
        sys.exit(2)


def reais(c):
    return float(c or 0) / 100


# ---------------- contas / listar ----------------
def cmd_contas(a, api):
    r = api.get("me/adaccounts", fields="id,name,account_status,currency,timezone_name,amount_spent,funding_source_details", limit=50)
    st = {1: "ATIVA", 2: "DESATIVADA", 3: "SEM PAGAMENTO", 7: "EM REVISAO", 9: "CARENCIA", 101: "FECHADA"}
    for c in r.get("data", []):
        fd = (c.get("funding_source_details") or {}).get("display_string", "sem cartao")
        print(f"{c['id']} | {c.get('name')} | status {st.get(c.get('account_status'), c.get('account_status'))} | "
              f"{c.get('currency')} | {c.get('timezone_name')} | cartao {fd} | gasto total R$ {reais(c.get('amount_spent')):.2f}")


def cmd_listar(a, api):
    r = api.get(f"{api.conta}/campaigns", fields="id,name,objective,status,effective_status,daily_budget,insights.date_preset(maximum).limit(1){spend}", limit=100)
    for c in r.get("data", []):
        ins = (c.get("insights") or {}).get("data", [])
        gasto = ins[0]["spend"] if ins else "0"
        print(f"{c['id']} | {c['name']} | {c.get('objective')} | {c['status']}/{c['effective_status']} | gasto R$ {gasto}")


# ---------------- impulsionar ----------------
CONFIG_OBJ = {
    "perfil": dict(objective="OUTCOME_TRAFFIC", dest="INSTAGRAM_PROFILE", goal="PROFILE_VISIT"),
    "engajamento": dict(objective="OUTCOME_ENGAGEMENT", dest="ON_POST", goal="POST_ENGAGEMENT"),
    "direct": dict(objective="OUTCOME_ENGAGEMENT", dest="INSTAGRAM_DIRECT", goal="CONVERSATIONS"),
    # site: so pelo comando "campanha" (arquivo JSON). Fallback LINK_CLICKS se a conta nao aceitar LANDING_PAGE_VIEWS.
    "site": dict(objective="OUTCOME_TRAFFIC", dest="WEBSITE", goal="LANDING_PAGE_VIEWS", goal_fallback="LINK_CLICKS"),
}


def subir_midia(api, arq):
    p = Path(arq)
    if not p.exists():
        sys.exit(f"arquivo nao existe: {arq}")
    ext = p.suffix.lower()
    if ext in (".png", ".jpg", ".jpeg"):
        with p.open("rb") as f:
            r = api._do("POST", f"{api.conta}/adimages", files={"filename": (p.name, f)})
        h = list(r["images"].values())[0]["hash"]
        return {"tipo": "imagem", "hash": h}
    if ext in (".mp4", ".mov"):
        with p.open("rb") as f:
            r = api._do("POST", f"{api.conta}/advideos", data={"title": p.stem}, files={"source": (p.name, f)})
        vid = r["id"]
        for _ in range(120):
            s = api.get(vid, fields="status,picture,thumbnails{uri,is_preferred}")
            est = (s.get("status") or {}).get("video_status")
            if est == "ready":
                break
            if est == "error":
                raise MetaErro({"error": {"message": f"video com erro: {s.get('status')}"}})
            time.sleep(5)
        else:
            raise MetaErro({"error": {"message": "video nao ficou pronto em 10 min"}})
        th = s.get("picture")
        for t in (s.get("thumbnails") or {}).get("data", []):
            if t.get("is_preferred"):
                th = t["uri"]
        return {"tipo": "video", "id": vid, "thumb": th}
    sys.exit("extensao nao suportada (use png, jpg ou mp4)")


def criativo(api, a, nome):
    m = api.m
    if a.post:
        return api.post(f"{api.conta}/adcreatives", name=nome + " criativo", object_id=m["page_id"],
                        instagram_user_id=m["ig_user_id"], source_instagram_media_id=a.post), {"post": a.post}
    if not (a.arquivo and a.texto):
        sys.exit("informe --post OU --arquivo + --texto")
    mid = subir_midia(api, a.arquivo)
    if mid["tipo"] == "imagem":
        spec = {"page_id": m["page_id"], "instagram_user_id": m["ig_user_id"],
                "link_data": {"image_hash": mid["hash"], "message": a.texto,
                              "link": f"https://www.instagram.com/{a.ig_usuario}/",
                              **({"name": a.titulo} if a.titulo else {}),
                              "call_to_action": {"type": a.cta or "LEARN_MORE", "value": {"link": f"https://www.instagram.com/{a.ig_usuario}/"}}}}
    else:
        vd = {"video_id": mid["id"], "message": a.texto,
              "call_to_action": {"type": a.cta or "LEARN_MORE", "value": {"link": f"https://www.instagram.com/{a.ig_usuario}/"}}}
        if mid.get("thumb"):
            vd["image_url"] = mid["thumb"]
        if a.titulo:
            vd["title"] = a.titulo
        spec = {"page_id": m["page_id"], "instagram_user_id": m["ig_user_id"], "video_data": vd}
    return api.post(f"{api.conta}/adcreatives", name=nome + " criativo", object_story_spec=spec), {"arquivo": a.arquivo, **mid}


def cmd_impulsionar(a, api):
    if a.objetivo == "site":
        sys.exit("objetivo site usa o comando: campanha --arquivo <json> [--teste]")
    cfg = CONFIG_OBJ[a.objetivo]
    dia = float(a.orcamento_dia)
    if dia <= 0 or a.dias < 1:
        sys.exit("RECUSADO: --orcamento-dia precisa ser maior que 0 e --dias pelo menos 1")
    if not a.post:
        if not (a.arquivo and a.texto):
            sys.exit("informe --post OU --arquivo + --texto")
        if not Path(a.arquivo).exists():
            sys.exit(f"arquivo nao existe: {a.arquivo}")
        if Path(a.arquivo).suffix.lower() not in (".png", ".jpg", ".jpeg", ".mp4", ".mov"):
            sys.exit("extensao nao suportada (use png, jpg ou mp4)")
    total = dia * a.dias
    checar_limites(dia, total)
    nome = a.nome or f"Impulso {a.objetivo} {dt.date.today()}"
    m = api.m
    criados = []  # (tipo, id)

    def rollback():
        for tipo, i in reversed(criados):
            try:
                api.delete(i)
                print(f"rollback: apagado {tipo} {i}")
            except Exception as e:
                print(f"rollback FALHOU em {tipo} {i}: {e}")
    try:
        camp = api.post(f"{api.conta}/campaigns", name=nome, objective=cfg["objective"], status="PAUSED",
                        special_ad_categories=[], buying_type="AUCTION", is_adset_budget_sharing_enabled=False)["id"]
        criados.append(("campanha", camp))
        inicio = dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=5)
        fim = inicio + dt.timedelta(days=a.dias)
        tg = {"geo_locations": {"countries": ["BR"]}, "age_min": a.idade_min, "age_max": a.idade_max,
              "targeting_automation": {"advantage_audience": 0},
              "publisher_platforms": ["instagram"],
              "instagram_positions": ["stream", "story", "reels", "explore_home"]}
        if a.interesses:
            tg["flexible_spec"] = [{"interests": [{"id": i} for i in a.interesses.split(",")]}]
        po = {"page_id": m["page_id"]}
        adset = api.post(f"{api.conta}/adsets", name=nome + " conjunto", campaign_id=camp, status="PAUSED",
                         daily_budget=int(round(dia * 100)), billing_event="IMPRESSIONS",
                         optimization_goal=cfg["goal"], destination_type=cfg["dest"],
                         bid_strategy="LOWEST_COST_WITHOUT_CAP", targeting=tg, promoted_object=po,
                         start_time=inicio.strftime("%Y-%m-%dT%H:%M:%S+0000"),
                         end_time=fim.strftime("%Y-%m-%dT%H:%M:%S+0000"))["id"]
        criados.append(("conjunto", adset))
        cr, info = criativo(api, a, nome)
        crid = cr["id"]
        criados.append(("criativo", crid))
        ad = api.post(f"{api.conta}/ads", name=nome + " anuncio", adset_id=adset, creative={"creative_id": crid}, status="PAUSED")["id"]
        criados.append(("anuncio", ad))
    except MetaErro as e:
        print("ERRO da Meta:", e.txt)
        print("resposta completa:", json.dumps(e.resp, ensure_ascii=False))
        rollback()
        log("impulsionar_falhou", objetivo=a.objetivo, erro=e.txt)
        sys.exit(1)
    except BaseException as e:
        print(f"ERRO inesperado: {type(e).__name__}. Desfazendo o que foi criado.")
        rollback()
        log("impulsionar_falhou", objetivo=a.objetivo, erro=type(e).__name__)
        raise
    log("impulsionar", objetivo=a.objetivo, campanha=camp, conjunto=adset, anuncio=ad, criativo=crid,
        orcamento_dia=dia, dias=a.dias, total=total, nome=nome, info_criativo=info)
    print(f"campanha {camp}\nconjunto {adset}\nanuncio  {ad}\ncriativo {crid}")
    print(f"resumo: objetivo {a.objetivo} | R$ {dia:.2f}/dia | {a.dias} dias | total R$ {total:.2f} | status PAUSED")
    print(f"gerenciador: https://adsmanager.facebook.com/adsmanager/manage/campaigns?act={api.num}")


# ---------------- campanha de site (varios anuncios, JSON) ----------------
def link_ok(u):
    if not str(u).startswith("https://"):
        sys.exit(f"RECUSADO: url precisa comecar com https:// ({u})")


def spec_anuncio(m, an, mid):
    """Monta o object_story_spec de um anuncio do tipo site. mid = midias ja enviadas (ou placeholders no dry-run)."""
    link_ok(an["url"])
    cta = {"type": an.get("cta", "LEARN_MORE"), "value": {"link": an["url"]}}
    if an["tipo"] == "carrossel":
        cards = []
        for h in mid["hashes"]:
            c = {"link": an["url"], "image_hash": h, "call_to_action": cta}
            if an.get("titulo"):
                c["name"] = an["titulo"]
            if an.get("descricao"):
                c["description"] = an["descricao"]
            cards.append(c)
        ld = {"link": an["url"], "message": an["texto"], "child_attachments": cards,
              "multi_share_optimized": False, "multi_share_end_card": False, "call_to_action": cta}
        return {"page_id": m["page_id"], "instagram_user_id": m["ig_user_id"], "link_data": ld}
    vd = {"video_id": mid["video_id"], "message": an["texto"], "call_to_action": cta}
    if mid.get("thumb_hash"):
        vd["image_hash"] = mid["thumb_hash"]
    if an.get("titulo"):
        vd["title"] = an["titulo"]
    if an.get("descricao"):
        vd["link_description"] = an["descricao"]
    return {"page_id": m["page_id"], "instagram_user_id": m["ig_user_id"], "video_data": vd}


def targeting_site(c):
    tg = {"geo_locations": {"countries": ["BR"]}, "age_min": c.get("idade_min", 25), "age_max": c.get("idade_max", 65),
          "targeting_automation": {"advantage_audience": 0},
          "publisher_platforms": ["instagram"],
          "instagram_positions": ["stream", "story", "reels", "explore_home"]}
    if c.get("interesses"):
        tg["flexible_spec"] = [{"interests": [{"id": str(i)} for i in c["interesses"]]}]
    return tg


def cmd_campanha(a, api):
    base = Path(a.arquivo).resolve()
    c = json.loads(base.read_text())
    raiz = base.parent
    cfg = CONFIG_OBJ["site"]
    dia = float(c["orcamento_dia"])
    dias = c.get("dias")  # opcional: sem dias, sem data de fim e sem total (ativar recusa ate definir)
    if dia <= 0:
        sys.exit("RECUSADO: orcamento_dia precisa ser maior que 0")
    total = dia * dias if dias else None
    checar_limites(dia, total if total is not None else 0)
    ans = c["anuncios"]
    if not ans:
        sys.exit("RECUSADO: nenhum anuncio no arquivo")
    for an in ans:
        link_ok(an["url"])
        for k in ("nome", "texto", "tipo"):
            if not an.get(k):
                sys.exit(f"RECUSADO: anuncio sem {k}")
        arqs = an.get("imagens", []) if an["tipo"] == "carrossel" else [an.get("video"), an.get("thumb")]
        if an["tipo"] == "carrossel" and len(an.get("imagens", [])) < 2:
            sys.exit("RECUSADO: carrossel precisa de 2 ou mais imagens")
        for f in arqs:
            if not f or not (raiz / f).exists():
                sys.exit(f"arquivo nao existe: {f}")
    nome = c["nome"]
    m = api.m
    tg = targeting_site(c)

    def payload_adset(camp, goal):
        d = dict(name=nome + " conjunto", campaign_id=camp, status="PAUSED", daily_budget=int(round(dia * 100)),
                 billing_event="IMPRESSIONS", optimization_goal=goal, destination_type=cfg["dest"],
                 bid_strategy="LOWEST_COST_WITHOUT_CAP", targeting=tg)
        if dias:
            fim = dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=dias, minutes=5)
            d["end_time"] = fim.strftime("%Y-%m-%dT%H:%M:%S+0000")
        return d

    if a.teste:
        print("TESTE (dry-run): nada sera enviado a Meta.")
        print("POST campaigns:", json.dumps(dict(name=nome, objective=cfg["objective"], status="PAUSED", special_ad_categories=[],
                                                   buying_type="AUCTION", is_adset_budget_sharing_enabled=False), ensure_ascii=False))
        print("POST adsets:", json.dumps(payload_adset("<CAMPANHA_ID>", cfg["goal"]), ensure_ascii=False, indent=1))
        for n, an in enumerate(ans, 1):
            if an["tipo"] == "carrossel":
                mid = {"hashes": [f"<hash {Path(f).name}>" for f in an["imagens"]]}
            else:
                mid = {"video_id": f"<id {Path(an['video']).name}>", "thumb_hash": f"<hash {Path(an['thumb']).name}>"}
            print(f"\n[{n}] anuncio '{an['nome']}' | status PAUSED | tipo {an['tipo']} | url {an['url']}")
            print("POST adcreatives object_story_spec:", json.dumps(spec_anuncio(m, an, mid), ensure_ascii=False, indent=1))
            print("POST ads:", json.dumps(dict(name=an["nome"], adset_id="<CONJUNTO_ID>", creative="<CRIATIVO_ID>", status="PAUSED"), ensure_ascii=False))
        print(f"\nresumo: {len(ans)} anuncios | R$ {dia:.2f}/dia | " + (f"{dias} dias | total R$ {total:.2f}" if dias else "sem data de fim") + " | tudo PAUSED")
        return

    criados = []

    def rollback():
        for tipo, i in reversed(criados):
            try:
                api.delete(i)
                print(f"rollback: apagado {tipo} {i}")
            except Exception as e:
                print(f"rollback FALHOU em {tipo} {i}: {e}")
    aviso = None
    try:
        camp = api.post(f"{api.conta}/campaigns", name=nome, objective=cfg["objective"], status="PAUSED",
                        special_ad_categories=[], buying_type="AUCTION", is_adset_budget_sharing_enabled=False)["id"]
        criados.append(("campanha", camp))
        goal = cfg["goal"]
        try:
            adset = api.post(f"{api.conta}/adsets", **payload_adset(camp, goal))["id"]
        except MetaErro as e:
            print("AVISO: LANDING_PAGE_VIEWS recusado (" + e.txt + "). Tentando LINK_CLICKS.")
            goal = cfg["goal_fallback"]
            aviso = f"LANDING_PAGE_VIEWS recusado, usado {goal}: {e.txt}"
            adset = api.post(f"{api.conta}/adsets", **payload_adset(camp, goal))["id"]
        criados.append(("conjunto", adset))
        out = []
        for an in ans:
            if an["tipo"] == "carrossel":
                mid = {"hashes": [subir_midia(api, str(raiz / f))["hash"] for f in an["imagens"]]}
            else:
                v = subir_midia(api, str(raiz / an["video"]))
                t = subir_midia(api, str(raiz / an["thumb"]))
                mid = {"video_id": v["id"], "thumb_hash": t["hash"]}
            cr = api.post(f"{api.conta}/adcreatives", name=an["nome"] + " criativo",
                          object_story_spec=spec_anuncio(m, an, mid))["id"]
            criados.append(("criativo", cr))
            ad = api.post(f"{api.conta}/ads", name=an["nome"], adset_id=adset, creative={"creative_id": cr}, status="PAUSED")["id"]
            criados.append(("anuncio", ad))
            out.append({"nome": an["nome"], "anuncio": ad, "criativo": cr, "url": an["url"], **{k: v for k, v in mid.items() if k == "video_id"}})
    except MetaErro as e:
        print("ERRO da Meta:", e.txt)
        print("resposta completa:", json.dumps(e.resp, ensure_ascii=False))
        rollback()
        log("campanha_site_falhou", erro=e.txt)
        sys.exit(1)
    except BaseException as e:
        print(f"ERRO inesperado: {type(e).__name__}. Desfazendo o que foi criado.")
        rollback()
        log("campanha_site_falhou", erro=type(e).__name__)
        raise
    log("impulsionar", objetivo="site", campanha=camp, conjunto=adset, anuncios=out, orcamento_dia=dia, dias=dias,
        total=total, nome=nome, otimizacao=goal, aviso=aviso, arquivo=str(base))
    print(f"campanha {camp}\nconjunto {adset} (otimizacao {goal})")
    for x in out:
        print(f"anuncio  {x['anuncio']} | criativo {x['criativo']} | {x['nome']}")
    print(f"resumo: site | R$ {dia:.2f}/dia | " + (f"{dias} dias | total R$ {total:.2f}" if dias else "sem data de fim, total indefinido") + " | tudo PAUSED")
    print(f"gerenciador: https://adsmanager.facebook.com/adsmanager/manage/campaigns?act={api.num}")


# ---------------- ativar / pausar / apagar ----------------
def filhos(api, camp):
    ads = [x["id"] for x in api.get(f"{camp}/ads", fields="id", limit=50).get("data", [])]
    sets = [x["id"] for x in api.get(f"{camp}/adsets", fields="id", limit=50).get("data", [])]
    return sets, ads


def cmd_ativar(a, api):
    reg = registro_campanha(a.campanha)
    if a.confirmo_gasto is None:
        print("RECUSADO: informe --confirmo-gasto <valor em reais> igual a orcamento_dia * dias.")
        sys.exit(2)
    if not reg:
        print("RECUSADO: campanha nao esta no anuncios/registro.jsonl, nao da pra conferir o gasto.")
        sys.exit(2)
    if reg.get("total") is None:
        print("RECUSADO: campanha registrada sem periodo (dias), total indefinido. Defina dias e o total com o Jesse antes de ativar.")
        sys.exit(2)
    if abs(float(a.confirmo_gasto) - reg["total"]) > 0.001:
        print(f"RECUSADO: --confirmo-gasto {a.confirmo_gasto} difere do total registrado (R$ {reg['total']:.2f}).")
        sys.exit(2)
    checar_limites(reg["orcamento_dia"], reg["total"])
    sets, ads = filhos(api, a.campanha)
    for s in sets:
        info = api.get(s, fields="daily_budget,end_time")
        if int(info.get("daily_budget") or 0) != int(round(reg["orcamento_dia"] * 100)):
            print(f"RECUSADO: orcamento do conjunto {s} na Meta (R$ {int(info.get('daily_budget') or 0)/100:.2f}) difere do registrado. Alguem mudou no Gerenciador.")
            sys.exit(2)
    try:
        api.post(a.campanha, status="ACTIVE")
        for i in sets + ads:
            api.post(i, status="ACTIVE")
    except BaseException as e:
        print(f"ERRO ao ativar ({type(e).__name__}). Pausando tudo de novo.")
        for i in [a.campanha] + sets + ads:
            try:
                api.post(i, status="PAUSED")
            except Exception:
                print(f"nao consegui pausar {i}, confira no Gerenciador")
        log("ativar_falhou", campanha=a.campanha)
        sys.exit(1)
    log("ativar", campanha=a.campanha, total=reg["total"])
    print(f"ATIVADA {a.campanha}. Vai gastar ate R$ {reg['total']:.2f}.")


def cmd_pausar(a, api):
    sets, ads = filhos(api, a.campanha)
    api.post(a.campanha, status="PAUSED")
    for i in sets + ads:
        api.post(i, status="PAUSED")
    log("pausar", campanha=a.campanha)
    print(f"PAUSADA {a.campanha}")


def cmd_apagar(a, api):
    if not registro_campanha(a.campanha) and not getattr(a, "confirmo_apagar", False):
        print("RECUSADO: campanha fora do anuncios/registro.jsonl. Pra apagar campanha antiga use --confirmo-apagar (so com GO do Jesse).")
        sys.exit(2)
    sets, ads = filhos(api, a.campanha)
    for i in ads + sets:
        api.delete(i)
    api.delete(a.campanha)
    log("apagar", campanha=a.campanha, conjuntos=sets, anuncios=ads)
    print(f"APAGADA {a.campanha} (+{len(sets)} conjuntos, {len(ads)} anuncios)")


# ---------------- relatorio ----------------
def acao(lista, *tipos):
    for x in lista or []:
        if x.get("action_type") in tipos:
            return float(x["value"])
    return None


def soma(lista):
    return sum(float(x["value"]) for x in lista or []) if lista else None


CAMPOS = ("spend,reach,impressions,frequency,cpm,clicks,ctr,cpc,actions,cost_per_action_type,"
          "video_p25_watched_actions,video_p50_watched_actions,video_p75_watched_actions,"
          "video_p100_watched_actions,video_thruplay_watched_actions,video_play_actions")


def cmd_relatorio(a, api):
    p = {"fields": CAMPOS, "limit": 100}
    if a.desde:
        p["time_range"] = json.dumps({"since": a.desde, "until": dt.date.today().isoformat()})
    else:
        p["date_preset"] = "maximum"
    per = {k: p[k] for k in ("time_range", "date_preset") if k in p}
    tot = api.get(f"{a.campanha}/insights", **p).get("data", [])
    out = {"campanha": a.campanha, "desde": a.desde, "geral": tot[0] if tot else None}
    if not tot:
        print("sem insights no periodo.")
    else:
        d = tot[0]
        imp = float(d.get("impressions", 0) or 0)
        print(f"gasto R$ {d.get('spend')} | alcance {d.get('reach')} | impressoes {d.get('impressions')} | freq {d.get('frequency')}")
        print(f"CPM {d.get('cpm')} | cliques {d.get('clicks')} | CTR {d.get('ctr')} | CPC {d.get('cpc')}")
        acts, custo = d.get("actions"), d.get("cost_per_action_type")
        visitas = acao(acts, "instagram_profile_visits", "profile_visit", "onsite_conversion.profile_visit")
        conv = acao(acts, "onsite_conversion.messaging_conversation_started_7d", "onsite_conversion.total_messaging_connection")
        print(f"visitas ao perfil {visitas} | conversas iniciadas {conv}")
        if custo:
            print("custo por resultado: " + "; ".join(f"{x['action_type']}={x['value']}" for x in custo[:8]))
        vp = acao(d.get("video_play_actions"), "video_view")
        plays3 = acao(acts, "video_view")
        print(f"video: plays {soma(d.get('video_play_actions'))} | 3s {plays3} | p25 {soma(d.get('video_p25_watched_actions'))} | "
              f"p50 {soma(d.get('video_p50_watched_actions'))} | p75 {soma(d.get('video_p75_watched_actions'))} | "
              f"p100 {soma(d.get('video_p100_watched_actions'))} | thruplay {soma(d.get('video_thruplay_watched_actions'))}")
        if plays3 and imp:
            print(f"taxa de gancho (3s/impressoes): {plays3 / imp * 100:.1f}%")
    for rot, bd in (("idade_genero", "age,gender"), ("posicionamento", "publisher_platform,platform_position")):
        try:
            r = api.get(f"{a.campanha}/insights", fields="spend,reach,impressions,clicks,ctr", breakdowns=bd,
                        limit=100, **per).get("data", [])
        except MetaErro as e:
            r = [{"erro": e.txt}]
        out[rot] = r
        print(f"\n[{rot}]")
        for x in r:
            chave = " ".join(str(x.get(k)) for k in bd.split(",") if x.get(k)) or str(x)
            print(f"  {chave}: gasto {x.get('spend')} | alcance {x.get('reach')} | impr {x.get('impressions')} | cliques {x.get('clicks')} | ctr {x.get('ctr')}")
    if a.json:
        (ANUNCIOS / "relatorios").mkdir(parents=True, exist_ok=True)
        f = ANUNCIOS / "relatorios" / f"{a.campanha}-{dt.date.today()}.json"
        f.write_text(json.dumps(out, ensure_ascii=False, indent=2))
        print(f"\nsalvo {f}")


def main():
    ap = argparse.ArgumentParser(description="Anuncios Meta (tudo nasce PAUSED)")
    ap.add_argument("--cliente", default="jesse-rodolfo")
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("contas")
    sp.add_parser("listar")
    i = sp.add_parser("impulsionar")
    i.add_argument("--objetivo", required=True, choices=list(CONFIG_OBJ))
    i.add_argument("--orcamento-dia", type=float, required=True)
    i.add_argument("--dias", type=int, required=True)
    i.add_argument("--nome")
    i.add_argument("--idade-min", type=int, default=28)
    i.add_argument("--idade-max", type=int, default=60)
    i.add_argument("--publico", default="brasil")
    i.add_argument("--interesses", help="ids separados por virgula")
    i.add_argument("--post")
    i.add_argument("--arquivo")
    i.add_argument("--texto")
    i.add_argument("--titulo")
    i.add_argument("--cta")
    i.add_argument("--ig-usuario", default="jesse.rodolfo")
    k = sp.add_parser("campanha")
    k.add_argument("--arquivo", required=True, help="JSON da campanha (nome, orcamento_dia, anuncios[])")
    k.add_argument("--teste", action="store_true", help="dry-run: imprime o payload, nao chama a API de criacao")
    t = sp.add_parser("ativar")
    t.add_argument("--campanha", required=True)
    t.add_argument("--confirmo-gasto", type=float)
    for n in ("pausar", "apagar"):
        x = sp.add_parser(n)
        x.add_argument("--campanha", required=True)
        if n == "apagar":
            x.add_argument("--confirmo-apagar", action="store_true")
    r = sp.add_parser("relatorio")
    r.add_argument("--campanha", required=True)
    r.add_argument("--desde")
    r.add_argument("--json", action="store_true")
    a = ap.parse_args()
    api = Meta(a.cliente)
    try:
        {"contas": cmd_contas, "listar": cmd_listar, "impulsionar": cmd_impulsionar, "campanha": cmd_campanha, "ativar": cmd_ativar,
         "pausar": cmd_pausar, "apagar": cmd_apagar, "relatorio": cmd_relatorio}[a.cmd](a, api)
    except MetaErro as e:
        print("ERRO da Meta:", e.txt)
        sys.exit(1)


if __name__ == "__main__":
    main()
