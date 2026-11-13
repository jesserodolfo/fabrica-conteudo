#!/usr/bin/env python3
"""Ouvinte do Telegram do lote de reels de teste (bot @meuinstagramjesse_bot).

Decisão: docs/decisoes/2026-11-12-video-madrugada.md, adendo de 12/11 20h25.
Roda pelo launchd com.fusiongrowth.telegram-ouvir (scripts/telegram_ouvir.sh). Python puro (urllib).

  telegram_ouvir.py                       ouve de verdade (long polling)
  telegram_ouvir.py --simular arq.json    processa os updates do arquivo sem falar com o Telegram
                                          (as chamadas saem no log como [simulado]); os trabalhos rodam em --ensaio

Segurança: só processa update do chat do dono (TELEGRAM_CHAT_ID). Qualquer outro é ignorado e registrado só com o id.
O token nunca é impresso nem gravado: fica só na memória deste processo.

Botões (callback_data):
  ok|<chave>|<slug>   aprova: marca aprovado no manifesto e enfileira PUBLICAR_TESTE (toque repetido não duplica)
  aj|<chave>|<slug>   pede ajuste: a próxima mensagem de texto do dono vira o pedido (AJUSTAR)
  pf|<chave>|<slug>   manda o teste pro perfil hoje 18h (PUBLICAR_PERFIL); chave = placar-AAAA-MM-DD
  pn                  hoje não
Comandos: /status /fila /ajuda

Trabalhos rodam um por vez, em processo separado, e esperam a rotina das 23h (saidas/lote-teste/.lock).
"""
import datetime as dt
import fcntl
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lote_comum as lc  # noqa: E402

RAIZ = lc.RAIZ
SAIDA = lc.SAIDA
OFFSET = SAIDA / ".telegram_offset"
LOG = SAIDA / "ouvir.log"
LOG_TRAB = SAIDA / "trabalhos.log"
FILA_PAUTAS = RAIZ / "pesquisa" / "fila-testes.md"
BASH = "/usr/local/bin/fusion-backup-bash" if os.access("/usr/local/bin/fusion-backup-bash", os.X_OK) else "/bin/bash"
SCRIPTS = {
    "PUBLICAR_TESTE": "scripts/publicar_teste.sh",
    "AJUSTAR": "scripts/ajustar_teste.sh",
    "PUBLICAR_PERFIL": "scripts/publicar_perfil.sh",
}
AJUDA = ("Reels de teste, como funciona:\n"
         "✅ Aprovado: agendo o vídeo como Reel de teste no próximo horário livre (11h, 14h, 17h).\n"
         "✏️ Ajuste: eu pergunto o que mudar, você escreve, o vídeo volta aqui consertado.\n"
         "Também dá pra responder (reply) um vídeo com o pedido de ajuste.\n"
         "/status: lote do dia\n/fila: próximas pautas\n/ajuda: esta mensagem")

SIMULAR = False
TOKEN = ""
CHAT = ""
PROCS = {}


def agora():
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(msg):
    linha = f"{agora()} {msg}"
    if TOKEN:
        linha = linha.replace(TOKEN, "***")
    print(linha, flush=True)
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(linha + "\n")
    except OSError:
        pass


def ler_env():
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


# ---------- Telegram ----------
def api(metodo, params=None, tempo=30):
    """Chama o Bot API. Devolve o JSON da resposta (com "ok"). Nunca levanta; erro vira {"ok": False, ...}."""
    if SIMULAR and metodo != "getUpdates":
        log(f"[simulado] {metodo} {json.dumps(params or {}, ensure_ascii=False)[:400]}")
        return {"ok": True, "result": {"message_id": 0}}
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{TOKEN}/{metodo}",
        data=json.dumps(params or {}).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=tempo) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            j = json.loads(e.read())
        except Exception:
            j = {}
        return {"ok": False, "error_code": e.code, "description": str(j.get("description", ""))[:200]}
    except Exception as e:  # rede, timeout
        return {"ok": False, "error_code": 0, "description": type(e).__name__}


def enviar(texto, markup=None, responder_a=None):
    p = {"chat_id": CHAT, "text": texto[:4000], "disable_web_page_preview": True}
    if markup is not None:
        p["reply_markup"] = markup
    if responder_a:
        p["reply_to_message_id"] = responder_a
        p["allow_sending_without_reply"] = True
    r = api("sendMessage", p)
    if not r.get("ok"):
        log(f"sendMessage falhou: {r.get('error_code')} {r.get('description')}")
    return (r.get("result") or {}).get("message_id")


def responder_toque(cq_id, texto=""):
    r = api("answerCallbackQuery", {"callback_query_id": cq_id, "text": texto[:190]})
    if not r.get("ok"):
        log(f"answerCallbackQuery falhou: {r.get('error_code')} {r.get('description')}")


def trocar_botoes(message_id, texto=None):
    """Troca o teclado da mensagem por um botão só (sem ação) ou tira o teclado."""
    if not message_id:
        return
    teclado = [[{"text": texto, "callback_data": "nada"}]] if texto else []
    r = api("editMessageReplyMarkup", {"chat_id": CHAT, "message_id": message_id,
                                       "reply_markup": {"inline_keyboard": teclado}})
    if not r.get("ok") and "not modified" not in r.get("description", ""):
        log(f"editMessageReplyMarkup falhou: {r.get('error_code')} {r.get('description')}")


# ---------- estado ----------
def arq_estado():
    return SAIDA / ("estado_telegram.simulacao.json" if SIMULAR else "estado_telegram.json")


def ler_estado():
    try:
        e = json.loads(arq_estado().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        e = {}
    e.setdefault("esperando_ajuste", None)
    e.setdefault("fila", [])
    e.setdefault("rodando", None)
    e.setdefault("feitos", [])
    return e


def salvar_estado(e):
    tmp = arq_estado().with_suffix(".tmp")
    tmp.write_text(json.dumps(e, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, arq_estado())


def enfileirar(e, tipo, chave, slug, arquivo=None):
    """Idempotente pra PUBLICAR_*: não entra duas vezes o mesmo trabalho."""
    pend = list(e["fila"]) + ([e["rodando"]] if e["rodando"] else [])
    if tipo != "AJUSTAR" and any(t["tipo"] == tipo and t["chave"] == chave and t["slug"] == slug for t in pend):
        log(f"fila: {tipo} {chave} {slug} já estava na fila, não duplica")
        return False
    t = {"id": f"{int(time.time() * 1000)}", "tipo": tipo, "chave": chave, "slug": slug,
         "arquivo": arquivo, "criado": agora(), "tentativas": 0}
    e["fila"].append(t)
    log(f"fila: entrou {tipo} {chave} {slug}" + (f" ({arquivo})" if arquivo else ""))
    return True


def pendente(e, tipo, chave, slug):
    pend = list(e["fila"]) + ([e["rodando"]] if e["rodando"] else [])
    return any(t["tipo"] == tipo and t["chave"] == chave and t["slug"] == slug for t in pend)


# ---------- trabalhos ----------
def comando(t):
    c = [BASH, str(RAIZ / SCRIPTS[t["tipo"]]), t["chave"], t["slug"]]
    if t["tipo"] == "AJUSTAR":
        c.append(t["arquivo"] or "")
    if SIMULAR or t["chave"].startswith("ensaio-"):
        c.append("--ensaio")
    return c


def vivo(pid):
    try:
        os.kill(int(pid), 0)
        return True
    except (OSError, ValueError, TypeError):
        return False


def despachar(e, esperar=False):
    """Fecha o trabalho que terminou e começa o próximo. Um por vez. Devolve True se mudou o estado."""
    mudou = False
    r = e.get("rodando")
    if r:
        proc = PROCS.get(r["id"])
        if proc is not None:
            rc = proc.wait() if esperar else proc.poll()
            if rc is None:
                return False
            PROCS.pop(r["id"], None)
        elif vivo(r.get("pid")):
            return False
        else:
            rc = -1  # o ouvinte reiniciou e o trabalho já tinha acabado: resultado está no log do trabalho
        e["rodando"] = None
        mudou = True
        if rc == 75 and r.get("tentativas", 0) < 60:
            r["tentativas"] = r.get("tentativas", 0) + 1
            r["nao_antes"] = time.time() + 300
            e["fila"].insert(0, r)
            log(f"trabalho {r['tipo']} {r['slug']}: rotina das 23h rodando, volta pra fila (tentativa {r['tentativas']})")
        else:
            r["fim"] = agora()
            r["status"] = rc
            e["feitos"] = (e["feitos"] + [r])[-30:]
            log(f"trabalho {r['tipo']} {r['chave']} {r['slug']} terminou com status {rc}")
    if not e["fila"]:
        return mudou
    t = e["fila"][0]
    if t.get("nao_antes", 0) > time.time() and not SIMULAR:
        return mudou
    if lc.trava_rotina():
        if not e.get("avisou_trava"):
            log("rotina das 23h rodando (.lock): os trabalhos esperam")
            e["avisou_trava"] = True
            mudou = True
        return mudou
    e.pop("avisou_trava", None)
    e["fila"].pop(0)
    c = comando(t)
    try:
        with open(LOG_TRAB, "a", encoding="utf-8") as saida:
            saida.write(f"{agora()} >>> {t['tipo']} {t['chave']} {t['slug']}\n")
            saida.flush()
            proc = subprocess.Popen(c, cwd=str(RAIZ), stdin=subprocess.DEVNULL, stdout=saida,
                                    stderr=subprocess.STDOUT, start_new_session=True)
    except OSError as x:
        log(f"não consegui iniciar {t['tipo']} {t['slug']}: {type(x).__name__}")
        t["status"] = "nao iniciou"
        e["feitos"] = (e["feitos"] + [t])[-30:]
        return True
    t["pid"] = proc.pid
    t["inicio"] = agora()
    PROCS[t["id"]] = proc
    e["rodando"] = t
    log(f"trabalho iniciado: {t['tipo']} {t['chave']} {t['slug']} (pid {proc.pid}" + (", --ensaio)" if "--ensaio" in c else ")"))
    return True


# ---------- lote ----------
def palavra_de(it, slug):
    return str(it.get("palavra") or slug).upper()


def achar_por_mensagem(message_id):
    """Procura nos manifestos recentes o vídeo cuja mensagem (atual ou antiga) tem esse id."""
    if not message_id:
        return None, None
    arqs = sorted(SAIDA.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    for arq in arqs[:12]:
        chave = arq.stem
        if not lc.RE_CHAVE.match(chave) or chave.startswith("placar-"):
            continue
        try:
            _, itens = lc.ler(chave)
        except ValueError:
            continue
        for it in itens:
            if message_id == it.get("message_id") or message_id in (it.get("mensagens_antigas") or []):
                return chave, it
    return None, None


def estado_item(e, chave, it):
    slug = it.get("slug")
    if it.get("slug") == "fila":
        return None
    if it.get("agendado"):
        return f"agendado {str(it.get('horario_rotulo') or it.get('horario') or '')}".strip()
    if pendente(e, "AJUSTAR", chave, slug):
        return "em ajuste"
    if it.get("aprovado"):
        return "aprovado, agendando"
    if it.get("erro_publicar"):
        return "erro ao agendar: " + str(it["erro_publicar"])[:120]
    if it.get("status") == "pronto":
        return "esperando você (Aprovado ou Ajuste)" if it.get("enviado") else "pronto, ainda não enviado"
    return "falhou: " + str(it.get("motivo") or "sem motivo")[:120]


def cmd_status(e):
    hoje = dt.date.today()
    linhas = []
    for dia in (hoje, hoje + dt.timedelta(days=1)):
        chave = dia.isoformat()
        try:
            dados, itens = lc.ler(chave)
        except ValueError:
            continue
        if dados is None:
            continue
        linhas.append(f"Lote de {dia.strftime('%d/%m')}:")
        for it in itens:
            est = estado_item(e, chave, it)
            if est:
                linhas.append(f"- {palavra_de(it, it.get('slug'))}: {est}")
    if not linhas:
        linhas.append("Sem lote de hoje nem de amanhã ainda. A rotina roda às 23h.")
    if e["rodando"]:
        linhas.append(f"Rodando agora: {e['rodando']['tipo']} {e['rodando']['slug']}")
    if e["fila"]:
        linhas.append(f"Na fila: {len(e['fila'])} trabalho(s)")
    if lc.trava_rotina():
        linhas.append("A rotina das 23h está rodando.")
    return "\n".join(linhas)


def cmd_fila():
    try:
        txt = FILA_PAUTAS.read_text(encoding="utf-8")
    except OSError:
        return "Não achei pesquisa/fila-testes.md."
    tit = re.findall(r"^## \[ \] (.+)$", txt, flags=re.M)
    if not tit:
        return "A fila de pautas está vazia."
    return f"Próximas pautas ({len(tit)} na fila):\n" + "\n".join(f"{k}. {t.strip()}" for k, t in enumerate(tit[:5], 1))


def receber_ajuste(e, chave, slug, texto, msg_id):
    try:
        _, itens = lc.ler(chave)
    except ValueError:
        itens = []
    it = lc.achar(itens, slug)
    if it is None:
        enviar("Não achei esse vídeo no lote. Manda /status pra ver o que tem.", responder_a=msg_id)
        return
    pal = palavra_de(it, slug)
    if it.get("agendado") or it.get("aprovado"):
        enviar(f"{pal} já foi aprovado, não dá pra ajustar por aqui.", responder_a=msg_id)
        return
    arq = SAIDA / f"ajuste-{chave}-{slug}-{int(time.time())}.txt"
    arq.write_text(texto.strip() + "\n", encoding="utf-8")
    antigo = it.get("message_id")
    enfileirar(e, "AJUSTAR", chave, slug, str(arq.relative_to(RAIZ)))
    if e.get("esperando_ajuste") and e["esperando_ajuste"].get("slug") == slug:
        e["esperando_ajuste"] = None
    enviar(f"Anotado. Ajustando {pal}, te mando de novo.", responder_a=msg_id)
    trocar_botoes(antigo, "✏️ Em ajuste...")


def tratar_toque(e, cq):
    cq_id = cq.get("id")
    dado = str(cq.get("data") or "")
    msg_id = (cq.get("message") or {}).get("message_id")
    partes = dado.split("|")
    acao = partes[0]
    if acao == "nada":
        responder_toque(cq_id)
        return
    if acao == "pn":
        responder_toque(cq_id, "Ok, hoje não.")
        trocar_botoes(msg_id, None)
        log("toque: pn (hoje não)")
        return
    if acao not in ("ok", "aj", "pf") or len(partes) != 3 or not lc.valido(partes[1], partes[2]):
        responder_toque(cq_id, "Botão inválido.")
        log("toque com dado inválido, ignorado")
        return
    chave, slug = partes[1], partes[2]
    try:
        dados, itens = lc.ler(chave)
    except ValueError:
        dados, itens = None, []
    it = lc.achar(itens, slug)
    if it is None:
        responder_toque(cq_id, "Não achei esse vídeo no lote.")
        log(f"toque {acao}: {chave} {slug} não existe no manifesto")
        return
    pal = palavra_de(it, slug)

    if acao == "pf":
        if chave != f"placar-{dt.date.today().isoformat()}":
            responder_toque(cq_id, "Esse placar é de outro dia. Espera o de hoje.")
            trocar_botoes(msg_id, None)
            return
        if it.get("perfil_pedido"):
            responder_toque(cq_id, f"{pal} já foi pedido pro perfil.")
            log(f"toque pf repetido: {chave} {slug}, não duplica")
            return
        lc.gravar(chave, slug, {"perfil_pedido": True, "perfil_pedido_em": agora()})
        enfileirar(e, "PUBLICAR_PERFIL", chave, slug)
        responder_toque(cq_id, f"{pal} vai pro perfil. Agendando...")
        trocar_botoes(msg_id, f"📌 {pal} no perfil, agendando...")
        return

    if msg_id and msg_id in (it.get("mensagens_antigas") or []):
        responder_toque(cq_id, "Esse é o vídeo antigo. Usa os botões do vídeo novo.")
        trocar_botoes(msg_id, None)
        return

    if acao == "ok":
        if it.get("agendado"):
            responder_toque(cq_id, f"{pal} já está agendado.")
            log(f"toque ok repetido: {chave} {slug} já agendado, não duplica")
            return
        if it.get("aprovado"):
            responder_toque(cq_id, f"{pal} já foi aprovado, estou agendando.")
            log(f"toque ok repetido: {chave} {slug} já aprovado, não duplica")
            return
        if pendente(e, "AJUSTAR", chave, slug):
            responder_toque(cq_id, f"{pal} está em ajuste. Espera o vídeo novo.")
            return
        if it.get("status") != "pronto":
            responder_toque(cq_id, f"{pal} não está pronto.")
            return
        responder_toque(cq_id, f"{pal} aprovado. Agendando...")
        lc.gravar(chave, slug, {"aprovado": True, "aprovado_em": agora(), "erro_publicar": ""})
        enfileirar(e, "PUBLICAR_TESTE", chave, slug)
        trocar_botoes(msg_id, "✅ Aprovado, agendando...")
        if e.get("esperando_ajuste") and e["esperando_ajuste"].get("slug") == slug:
            e["esperando_ajuste"] = None
        return

    # aj
    if it.get("agendado") or it.get("aprovado"):
        responder_toque(cq_id, f"{pal} já foi aprovado.")
        return
    responder_toque(cq_id)
    pergunta = enviar(f"O que ajustar no vídeo {pal}? Escreve aqui.")
    e["esperando_ajuste"] = {"chave": chave, "slug": slug, "palavra": pal, "desde": time.time(), "pergunta_id": pergunta}
    log(f"toque aj: esperando o texto do ajuste de {chave} {slug}")


def tratar_mensagem(e, msg):
    msg_id = msg.get("message_id")
    texto = msg.get("text")
    if not texto:
        enviar("Por aqui eu só leio texto. Escreve o pedido ou manda /ajuda.", responder_a=msg_id)
        log("mensagem sem texto do dono (foto, áudio ou outro)")
        return
    t = texto.strip()
    if t.startswith("/"):
        c = t.split()[0].split("@")[0].lower()
        log(f"comando {c}")
        if c == "/status":
            enviar(cmd_status(e))
        elif c == "/fila":
            enviar(cmd_fila())
        else:
            enviar(AJUDA)
        return
    resp = (msg.get("reply_to_message") or {}).get("message_id")
    esp = e.get("esperando_ajuste")
    if esp and time.time() - esp.get("desde", 0) > 12 * 3600:
        esp = e["esperando_ajuste"] = None
    if resp:
        chave, it = achar_por_mensagem(resp)
        if it is not None:
            log(f"texto respondendo o vídeo {chave} {it.get('slug')}: ajuste ({len(t)} caracteres)")
            receber_ajuste(e, chave, it.get("slug"), t, msg_id)
            return
    if esp:
        log(f"texto do ajuste de {esp['chave']} {esp['slug']} ({len(t)} caracteres)")
        receber_ajuste(e, esp["chave"], esp["slug"], t, msg_id)
        return
    log(f"texto solto do dono ({len(t)} caracteres), sem ajuste esperando")
    enviar("Não sei de qual vídeo é. Toca em Ajuste no vídeo ou responde (reply) o vídeo com o pedido. /ajuda")


def tratar(e, upd):
    cq = upd.get("callback_query")
    msg = upd.get("message")
    if cq:
        de = str((cq.get("from") or {}).get("id"))
        chat = str(((cq.get("message") or {}).get("chat") or {}).get("id"))
        if de != CHAT or chat != CHAT:
            log(f"ignorado: toque de id {de} (não é o dono)")
            return
        tratar_toque(e, cq)
    elif msg:
        de = str((msg.get("from") or {}).get("id"))
        chat = str((msg.get("chat") or {}).get("id"))
        if de != CHAT or chat != CHAT:
            log(f"ignorado: mensagem do chat {chat} (não é o dono)")
            return
        tratar_mensagem(e, msg)
    else:
        log("ignorado: update de outro tipo")


def conferir_publicados():
    """Depois do horário, confere no Zernio (só GET) se o teste saiu. Falha vira aviso claro no Telegram.
    Erros do guia: 2207081 (conta sem o botão Teste) e 2207078 (limite de testes do dia). Nunca vira reel normal."""
    import melhor_teste as mt
    key = mt.env().get("ZERNIO_API_KEY", "")
    hoje = dt.date.today()
    for dia in (hoje, hoje - dt.timedelta(days=1)):
        chave = dia.isoformat()
        try:
            _, itens = lc.ler(chave)
        except Exception:
            continue
        for it in itens:
            if not (it.get("agendado") and it.get("post_id") and it.get("horario")) or it.get("conferido"):
                continue
            try:
                quando = dt.datetime.fromisoformat(str(it["horario"])[:16])
            except ValueError:
                continue
            if dt.datetime.now() < quando + dt.timedelta(minutes=12):
                continue
            r = mt.zernio(key, f"/posts/{it['post_id']}")
            ig = [x for x in r.get("post", {}).get("platforms", []) if x.get("platform") == "instagram"]
            ig = ig[0] if ig else {}
            status = ig.get("status") or r.get("post", {}).get("status")
            pal, slug = palavra_de(it, it.get("slug")), it.get("slug")
            if status == "published":
                lc.gravar(chave, slug, {"conferido": True, "publicado": True, "link": ig.get("platformPostUrl") or ""})
                log(f"conferido: {pal} publicado como teste")
            elif status == "failed":
                erro = str(ig.get("errorMessage") or ig.get("error") or r.get("post", {}).get("errorMessage") or "sem mensagem")[:400]
                if "2207081" in erro:
                    lc.gravar(chave, slug, {"conferido": True, "publicado": False, "erro_publicar": erro})
                    enviar(f"❌ {pal} NÃO saiu: a conta está sem o botão Teste (erro 2207081). Nenhum reel de teste sai até "
                           f"isso voltar no app (tela de compartilhar reel). Não virou reel normal. Erro: {erro}")
                elif "2207078" in erro:
                    amanha = (hoje + dt.timedelta(days=1)).isoformat()
                    lc.gravar(chave, slug, {"conferido": True, "publicado": False, "agendado": False, "aprovado": False,
                                            "nao_antes": amanha, "erro_publicar": erro})
                    enviar(f"⚠️ {pal} ficou pra amanhã: a conta bateu o limite de reels de teste de hoje (erro 2207078). "
                           "Não virou reel normal. Toque pra agendar amanhã.",
                           markup={"inline_keyboard": [[{"text": "🔁 Agendar amanhã", "callback_data": f"ok|{chave}|{slug}"}]]})
                else:
                    lc.gravar(chave, slug, {"conferido": True, "publicado": False, "erro_publicar": erro})
                    enviar(f"❌ {pal} NÃO saiu no horário. Erro do Zernio: {erro}. Não virou reel normal.")
                log(f"conferido: {pal} FALHOU ao publicar")
            elif "erro" in r:
                log(f"conferir {pal}: Zernio não respondeu ({r['erro']})")


# ---------- laços ----------
def simular(arquivo):
    global SIMULAR
    SIMULAR = True
    arq_estado().unlink(missing_ok=True)
    updates = json.loads(Path(arquivo).read_text(encoding="utf-8"))
    log(f"[simulado] início: {len(updates)} update(s) de {arquivo}")
    e = ler_estado()
    for upd in updates:
        nota = upd.pop("_nota", "")
        log(f"[simulado] update {upd.get('update_id')}: {nota}")
        tratar(e, upd)
        salvar_estado(e)
    log(f"[simulado] fila depois dos updates: {[(t['tipo'], t['slug']) for t in e['fila']]}")
    while e["fila"] or e["rodando"]:
        if lc.trava_rotina():
            log("[simulado] rotina das 23h rodando: paro aqui sem rodar os trabalhos")
            break
        despachar(e, esperar=True)
        salvar_estado(e)
    log(f"[simulado] fim. feitos: {[(t['tipo'], t['slug'], t.get('status')) for t in e['feitos']]}")


def ouvir():
    trava = open(SAIDA / ".ouvir.lock", "w")
    try:
        fcntl.flock(trava, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        log("já existe um ouvinte rodando. Saindo.")
        time.sleep(20)
        return 0
    eu = api("getMe")
    if not eu.get("ok"):
        log(f"getMe falhou: {eu.get('error_code')} {eu.get('description')}. Tento de novo em 60 s.")
        time.sleep(60)
        return 1
    log(f"ouvinte no ar: bot @{eu['result'].get('username')}, pid {os.getpid()}, interpretador de trabalho {BASH}")
    try:
        offset = int(OFFSET.read_text().strip())
    except (OSError, ValueError):
        # Primeira vez: descarta o que estava parado no bot pra não responder mensagem velha.
        r = api("getUpdates", {"offset": -1, "timeout": 0})
        ult = [u["update_id"] for u in r.get("result", [])] if r.get("ok") else []
        offset = (ult[-1] + 1) if ult else 0
        OFFSET.write_text(str(offset))
        log(f"primeira execução: offset inicial {offset}")
    espera, ciclo, ult_conf = 5, 0, 0.0
    while True:
        if time.time() - ult_conf > 600:
            ult_conf = time.time()
            try:
                conferir_publicados()
            except Exception as x:
                log(f"conferir_publicados falhou: {type(x).__name__}: {str(x)[:150]}")
        e = ler_estado()
        if despachar(e):
            salvar_estado(e)
        ocupado = bool(e["fila"] or e["rodando"])
        tempo = 10 if ocupado else 20   # curto de propósito: depois que o Mac acorda, a conexão velha cai em até 25 s
        r = api("getUpdates", {"offset": offset, "timeout": tempo, "allowed_updates": ["message", "callback_query"]},
                tempo=tempo + 5)
        ciclo += 1
        if not r.get("ok"):
            cod = r.get("error_code")
            log(f"getUpdates falhou: {cod} {r.get('description')}. Espero {espera} s.")
            time.sleep(300 if cod == 401 else (30 if cod == 409 else espera))
            espera = min(espera * 2, 10)   # rede volta rápido depois de acordar; não vale esperar 60 s
            continue
        espera = 5
        ups = r.get("result", [])
        if ciclo <= 3 or ups or ciclo % 60 == 0:
            log(f"ciclo {ciclo}: getUpdates ok, {len(ups)} update(s), offset {offset}")
        for upd in ups:
            e = ler_estado()
            try:
                tratar(e, upd)
            except Exception as x:  # um update ruim não derruba o ouvinte
                log(f"erro ao tratar update {upd.get('update_id')}: {type(x).__name__}: {str(x)[:200]}")
            salvar_estado(e)
            offset = upd["update_id"] + 1
            OFFSET.write_text(str(offset))


def main():
    global TOKEN, CHAT
    SAIDA.mkdir(parents=True, exist_ok=True)
    env = ler_env()
    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or env.get("TELEGRAM_BOT_TOKEN", "")
    CHAT = str(os.environ.get("TELEGRAM_CHAT_ID") or env.get("TELEGRAM_CHAT_ID", ""))
    if not TOKEN or not CHAT:
        log("faltam TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID no .env")
        time.sleep(60)
        return 1
    if len(sys.argv) >= 3 and sys.argv[1] == "--simular":
        simular(sys.argv[2])
        return 0
    return ouvir()


if __name__ == "__main__":
    sys.exit(main())
