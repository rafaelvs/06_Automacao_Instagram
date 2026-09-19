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


def teste_agenda():
    """Confere que os conjuntos acima batem com os literais do publish.py (sem importá-lo)."""
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "publish.py"), encoding="utf-8").read()
    for nome, val in (("POST_WEEKDAYS", POST_WEEKDAYS), ("POST2_WEEKDAYS", POST2_WEEKDAYS),
                      ("SEQ_WEEKDAYS", SEQ_WEEKDAYS), ("REEL_WEEKDAYS", REEL_WEEKDAYS)):
        m = re.search(nome + r"\s*=\s*\{([^}]*)\}", src)
        assert m, nome
        assert {int(x) for x in m.group(1).split(",")} == val, f"{nome} divergente do publish.py"
    return True


if __name__ == "__main__":
    print("agenda confere com publish.py:", teste_agenda())
