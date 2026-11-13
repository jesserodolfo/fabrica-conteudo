#!/usr/bin/env python3
"""Funções comuns do lote de reels de teste: manifesto, horários e trava.

Usado por scripts/telegram_ouvir.py e, pela linha de comando, pelos scripts de trabalho
(publicar_teste.sh, ajustar_teste.sh, publicar_perfil.sh). Python puro, sem dependência.

Linha de comando (da raiz do projeto):
  lote_comum.py campo <chave> <slug> <campo>          imprime o campo do item (vazio se não existe)
  lote_comum.py gravar <chave> <slug> <json>          mescla o JSON no item do manifesto
  lote_comum.py horarios <chave> [perfil|<slug>]           horários candidatos, um por linha: ISO<TAB>rótulo
  lote_comum.py trava                                 sai 0 se a rotina das 23h está rodando, 1 se não

<chave> é o nome do manifesto sem .json: AAAA-MM-DD, ensaio-AAAA-MM-DD ou placar-AAAA-MM-DD.
"""
import datetime as dt
import json
import os
import re
import sys
import time
from pathlib import Path

os.environ["TZ"] = "America/Sao_Paulo"
time.tzset()

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "saidas" / "lote-teste"
RE_CHAVE = re.compile(r"^(ensaio-|placar-)?\d{4}-\d{2}-\d{2}$")
RE_SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{0,40}$")
SLOTS_TESTE = [(11, 0), (14, 0), (17, 0)]


def valido(chave, slug):
    return bool(RE_CHAVE.match(chave or "") and RE_SLUG.match(slug or ""))


def caminho(chave):
    if not RE_CHAVE.match(chave or ""):
        raise ValueError("chave inválida")
    return SAIDA / f"{chave}.json"


def ler(chave):
    """Devolve (dados, itens). Manifesto é lista ou {"videos": [...]}. Sem arquivo: (None, [])."""
    arq = caminho(chave)
    if not arq.is_file():
        return None, []
    dados = json.loads(arq.read_text(encoding="utf-8"))
    itens = dados if isinstance(dados, list) else dados.get("videos", [])
    return dados, itens


def salvar(chave, dados):
    arq = caminho(chave)
    tmp = arq.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, arq)


def achar(itens, slug):
    for it in itens:
        if it.get("slug") == slug:
            return it
    return None


def gravar(chave, slug, campos):
    """Mescla campos no item. Devolve o item ou None."""
    dados, itens = ler(chave)
    it = achar(itens, slug)
    if it is None:
        return None
    it.update(campos)
    salvar(chave, dados)
    return it


def data_da_chave(chave):
    return dt.date.fromisoformat(chave[-10:])


def rotulo(quando):
    return quando.strftime("%Hh%M")


def horarios(chave, perfil=False, agora=None, slug=None):
    """Candidatos em ordem. Teste: 11h, 14h, 17h do dia da chave que ainda não passaram nem estão em uso
    no manifesto; depois 20 min a partir de agora e de hora em hora. Perfil: hoje 18h, senão 20 min depois de agora."""
    agora = agora or dt.datetime.now()
    margem = agora + dt.timedelta(minutes=10)
    cand = []
    if perfil:
        d18 = dt.datetime.combine(agora.date(), dt.time(18, 0))
        if d18 > margem:
            cand.append(d18)
    else:
        dia = data_da_chave(chave)
        if dia < agora.date():
            dia = agora.date()
        _, itens = ler(chave)
        if slug:
            eu = achar(itens, slug) or {}
            try:  # limite de testes do dia (erro 2207078): só a partir do dia seguinte
                dia = max(dia, dt.date.fromisoformat(str(eu.get("nao_antes", ""))[:10]))
            except ValueError:
                pass
        usados = {str(i.get("horario", ""))[:16] for i in itens if i.get("horario")}
        for h, m in SLOTS_TESTE:
            q = dt.datetime.combine(dia, dt.time(h, m))
            if q > margem and q.strftime("%Y-%m-%dT%H:%M") not in usados:
                cand.append(q)
    base = agora + dt.timedelta(minutes=20)
    base = base.replace(second=0, microsecond=0) + dt.timedelta(minutes=(5 - base.minute % 5) % 5)
    if cand and base <= cand[-1]:
        base = cand[-1] + dt.timedelta(hours=1)
    for k in range(4):
        cand.append(base + dt.timedelta(hours=k))
    return cand


def trava_rotina():
    """True se a rotina das 23h (saidas/lote-teste/.lock) está rodando."""
    pid_arq = SAIDA / ".lock" / "pid"
    try:
        pid = int(pid_arq.read_text().strip())
        os.kill(pid, 0)
        return True
    except (OSError, ValueError):
        return False


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    op = argv[1]
    if op == "trava":
        return 0 if trava_rotina() else 1
    if op == "horarios":
        perfil = len(argv) > 3 and argv[3] == "perfil"
        for q in horarios(argv[2], perfil=perfil, slug=None if perfil or len(argv) < 4 else argv[3]):
            print(q.strftime("%Y-%m-%dT%H:%M") + "\t" + rotulo(q))
        return 0
    if op in ("campo", "gravar"):
        chave, slug = argv[2], argv[3]
        if not valido(chave, slug):
            print("chave ou slug inválido", file=sys.stderr)
            return 2
        if op == "campo":
            _, itens = ler(chave)
            it = achar(itens, slug)
            if it is None:
                return 1
            v = it.get(argv[4], "")
            print(v if isinstance(v, str) else json.dumps(v, ensure_ascii=False))
            return 0
        it = gravar(chave, slug, json.loads(argv[4]))
        return 0 if it is not None else 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
