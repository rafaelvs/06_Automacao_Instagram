# -*- coding: utf-8 -*-
"""Agenda do publish.py exposta SEM importar o publish (que exige os secrets e aborta sem eles).
Os dias da semana são cópia dos literais do publish.py (teste_agenda confere); a REGRA de qual reel
sai em cada dia NÃO é cópia: é a mesma função do robô (regra_reels.proximo_reel), chamada dia a
dia sobre a fila e o estado reais. Antes havia uma reimplementação aqui, e a cota vinha do
ambiente local enquanto o publish lia a variável do repositório (auditoria 19/10/2026)."""
import datetime as dt
import os
import re

import regra_reels

POST_WEEKDAYS = {1, 3, 5}
POST2_WEEKDAYS = {6}
SEQ_WEEKDAYS = {1, 3, 5}
REEL_WEEKDAYS = {0, 2, 4, 6}
REEL_MIN = 15 * 60
BRT = regra_reels.BRT
formato = regra_reels.formato


def cota_vigente():
    return regra_reels.cota_laminas()


def projeta_reels(fila, published, base, ja_hoje, cota=None, horizonte_dias=730, dias_conversa=None,
                  conversa_ativa=None):
    """[(data, id)] dos reels que vão sair, simulando o publish em cada dia de reel às 15h:
    `fila` = reels.json INTEIRO (na ordem), `published` = state['published'] real. Cada peça
    projetada entra no estado simulado com o formato — exatamente o que o log() do publish grava."""
    cota = cota_vigente() if cota is None else cota
    dias_conversa = regra_reels.dias_entre_conversas() if dias_conversa is None else dias_conversa
    conversa_ativa = regra_reels.conversas_ativas() if conversa_ativa is None else conversa_ativa
    st = {"published": list(published)}
    done = {e["id"] for e in published}
    out = []
    d = base + dt.timedelta(days=1 if ja_hoje else 0)
    fim = base + dt.timedelta(days=horizonte_dias)
    while d <= fim and any(x["id"] not in done for x in fila):
        if d.weekday() in REEL_WEEKDAYS:
            agora = dt.datetime(d.year, d.month, d.day, REEL_MIN // 60, REEL_MIN % 60 + 5, tzinfo=BRT)
            esc = regra_reels.proximo_reel(fila, done, st, agora, cota=cota, dias_conversa=dias_conversa,
                                           conversa_ativa=conversa_ativa)
            if esc is not None:
                out.append((d, esc["id"])); done.add(esc["id"])
                st["published"].append({"id": esc["id"], "kind": "reel", "at": agora.isoformat(),
                                        "formato": formato(esc)})
        d += dt.timedelta(days=1)
    return out


def teste_agenda():
    """Confere (1) os dias da semana contra os literais do publish.py; (2) que o publish usa a
    regra única e que o publish.yml não sobrescreve a cota por variável; (3) a simulação contra
    um caso calculado à mão, incluindo id repetido e peça nova publicada fora da fila."""
    raiz = os.path.dirname(os.path.abspath(__file__))
    src = open(os.path.join(raiz, "publish.py"), encoding="utf-8").read()
    for nome, val in (("POST_WEEKDAYS", POST_WEEKDAYS), ("POST2_WEEKDAYS", POST2_WEEKDAYS),
                      ("SEQ_WEEKDAYS", SEQ_WEEKDAYS), ("REEL_WEEKDAYS", REEL_WEEKDAYS)):
        m = re.search(nome + r"\s*=\s*\{([^}]*)\}", src)
        assert m, nome
        assert {int(x) for x in m.group(1).split(",")} == val, f"{nome} divergente do publish.py"
    m = re.search(r"REEL_MIN\s*=\s*(\d+)\s*\*\s*60", src)
    assert m and int(m.group(1)) * 60 == REEL_MIN, "REEL_MIN divergente do publish.py"
    assert "regra_reels.proximo_reel(" in src and "regra_reels.cota_laminas()" in src \
        and "regra_reels.dias_entre_conversas()" in src and "regra_reels.conversas_ativas()" in src, \
        "publish.py deixou de usar a regra única (regra_reels)"
    yml = open(os.path.join(raiz, ".github", "workflows", "publish.yml"), encoding="utf-8").read()
    for var in ("LAMINAS_POR_SEMANA", "DIAS_ENTRE_CONVERSAS", "CONVERSAS_ATIVAS"):
        assert not re.search(r"^\s*" + var + r"\s*:", yml, re.M), \
            f"publish.yml voltou a definir {var} — a página leria outra cota que o robô"
    seg = dt.date(2026, 10, 19)
    l1, l2, c1 = {"id": "l1"}, {"id": "l2"}, {"id": "c1", "formato": "conversa"}
    # 2 lâminas + 1 conversa a partir de uma segunda, cota 1: seg l1, qua c1, sex/dom nada, seg seguinte l2
    r = projeta_reels([l1, l2, c1], [], seg, False, cota=1, conversa_ativa=True)
    assert r == [(seg, "l1"), (seg + dt.timedelta(days=2), "c1"), (seg + dt.timedelta(days=7), "l2")], r
    # id repetido na fila: sai uma vez só (o publish só publica uma vez)
    r = projeta_reels([c1, l1, dict(c1)], [], seg, False, cota=1, conversa_ativa=True)
    assert [i for _, i in r] == ["c1", "l1"], r
    # conversa publicada na segunda e JÁ FORA da fila: não conta como lâmina (formato no registro)
    pub = [{"id": "c0", "kind": "reel", "at": "2026-10-19T15:05:00-03:00", "formato": "conversa"}]
    r = projeta_reels([l1], pub, seg, True, cota=1, conversa_ativa=True)
    assert r == [(seg + dt.timedelta(days=2), "l1")], r
    # conversa: só 10 dias depois da anterior (19/10). Fila c1 c2 f1 f2 f3 a partir de segunda:
    # seg c1, qua f1, sex f2, dom f3; seg+7 ainda não pode; c2 no 1º dia de reel a partir de +10 (sex, +11)
    c2 = {"id": "c2", "formato": "conversa"}
    f1, f2, f3 = ({"id": f"f{k}", "formato": "como_funciona"} for k in (1, 2, 3))
    r = projeta_reels([c1, c2, f1, f2, f3], [], seg, False, cota=1, dias_conversa=10, conversa_ativa=True)
    assert [(d - seg).days for d, _ in r] == [0, 2, 4, 6, 11] and [i for _, i in r] == ["c1", "f1", "f2", "f3", "c2"], r
    # ALL-IN (24/10): padrão = lâmina 0 e conversa desligada -> só COMO FUNCIONA sai, um por dia de reel
    r = projeta_reels([l1, c1, f1, c2, f2], [], seg, False, cota=0, conversa_ativa=False)
    assert [i for _, i in r] == ["f1", "f2"] and [(d - seg).days for d, _ in r] == [0, 2], r
    # cota 0 = lâminas suspensas: nada sai, e a projeção fica vazia (o gerador tem de avisar)
    assert projeta_reels([l1], [], seg, False, cota=0, horizonte_dias=30) == []
    return True


if __name__ == "__main__":
    print("agenda confere com publish.py:", teste_agenda())
