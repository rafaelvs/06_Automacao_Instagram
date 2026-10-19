# -*- coding: utf-8 -*-
"""Agenda do publish.py exposta SEM importar o publish (que exige os secrets e aborta sem eles).
Fonte única: os mesmos valores de publish.py — se mudar lá, mude aqui (teste_agenda abaixo confere)."""
import datetime as dt
import os
import re

POST_WEEKDAYS = {1, 3, 5}
POST2_WEEKDAYS = {6}
SEQ_WEEKDAYS = {1, 3, 5}
REEL_WEEKDAYS = {0, 2, 4, 6}
BRT = dt.timezone(dt.timedelta(hours=-3))
# Cota de laminas (18/10/2026): mesmo default e mesma variavel do publish.py.
LAMINAS_POR_SEMANA = int(os.environ.get("LAMINAS_POR_SEMANA", "1") or 1)


def formato(item):
    return (item.get("formato") or "lamina").strip().lower()


def projeta_reels(itens, base, ja_hoje, laminas_ja_na_semana=0, cota=None, horizonte_dias=730):
    """Datas de reel com a MESMA regra do publish.proximo_reel: em cada dia de reel sai o primeiro
    item da fila permitido — formato novo sempre, lamina so' dentro da cota semanal. Dia sem item
    permitido fica sem reel. Devolve [(data, id)]."""
    cota = LAMINAS_POR_SEMANA if cota is None else cota
    pend = list(itens); out = []
    d = base + dt.timedelta(days=1 if ja_hoje else 0)
    semana = (d - dt.timedelta(days=d.weekday()))
    usadas = laminas_ja_na_semana if (base - dt.timedelta(days=base.weekday())) == semana else 0
    fim = base + dt.timedelta(days=horizonte_dias)
    while pend and d <= fim:
        seg = d - dt.timedelta(days=d.weekday())
        if seg != semana:
            semana, usadas = seg, 0
        if d.weekday() in REEL_WEEKDAYS:
            livre = cota < 0 or usadas < cota
            esc = next((x for x in pend if formato(x) != "lamina" or livre), None)
            if esc is not None:
                out.append((d, esc["id"])); pend.remove(esc)
                if formato(esc) == "lamina":
                    usadas += 1
        d += dt.timedelta(days=1)
    return out


def teste_agenda():
    """Confere que os conjuntos acima batem com os literais do publish.py (sem importá-lo)."""
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "publish.py"), encoding="utf-8").read()
    for nome, val in (("POST_WEEKDAYS", POST_WEEKDAYS), ("POST2_WEEKDAYS", POST2_WEEKDAYS),
                      ("SEQ_WEEKDAYS", SEQ_WEEKDAYS), ("REEL_WEEKDAYS", REEL_WEEKDAYS)):
        m = re.search(nome + r"\s*=\s*\{([^}]*)\}", src)
        assert m, nome
        assert {int(x) for x in m.group(1).split(",")} == val, f"{nome} divergente do publish.py"
    m = re.search(r'LAMINAS_POR_SEMANA\s*=\s*int\(os\.environ\.get\("LAMINAS_POR_SEMANA",\s*"(-?\d+)"', src)
    assert m and int(m.group(1)) == int(os.environ.get("LAMINAS_POR_SEMANA_PADRAO", "1")), \
        "default de LAMINAS_POR_SEMANA divergente do publish.py"
    # controle da simulacao: 2 laminas + 1 conversa a partir de uma segunda, cota 1 ->
    # seg lamina, qua conversa, sex NADA (cota cheia), dom NADA, seg seguinte a 2a lamina
    seg = dt.date(2026, 10, 19)
    r = projeta_reels([{"id": "l1"}, {"id": "l2"}, {"id": "c1", "formato": "conversa"}], seg, False, 0, cota=1)
    assert r == [(seg, "l1"), (seg + dt.timedelta(days=2), "c1"), (seg + dt.timedelta(days=7), "l2")], r
    return True


if __name__ == "__main__":
    print("agenda confere com publish.py:", teste_agenda())
