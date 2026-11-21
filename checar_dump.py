# -*- coding: utf-8 -*-
"""Vigia da MEDIÇÃO (auditoria v3, 21/11/2026 — ação 3 da v2, que ficou pela metade).

O insights.yml grava toda segunda um dump de 30 dias em AUDITORIA/evidencias/. Se o cron morrer
(token, workflow desativado por 60 dias sem push humano, mudança de API), ninguém fica sabendo:
a auditoria seguinte descobre semanas depois que mediu no escuro (v2: 3 medições perdidas).
Este checador falha (exit 1) quando o dump de 30 dias mais novo tem mais de MAX_DIAS dias.

Uso: python checar_dump.py [--hoje AAAA-MM-DD] | --auto-teste
"""
import argparse, datetime as dt, os, re, sys

MAX_DIAS = 10           # cron semanal + 3 dias de folga
PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AUDITORIA", "evidencias")
PADRAO = re.compile(r"^insights_(\d{4}-\d{2}-\d{2})_30d\.json$")


def mais_novo(nomes):
    datas = [dt.date.fromisoformat(m.group(1)) for n in nomes for m in [PADRAO.match(n)] if m]
    return max(datas) if datas else None


def veredito(nomes, hoje):
    d = mais_novo(nomes)
    if d is None:
        return 1, "REPROVADO: nenhum dump insights_*_30d.json em AUDITORIA/evidencias/ — a medição nunca rodou ou a pasta mudou."
    idade = (hoje - d).days
    if idade > MAX_DIAS:
        return 1, f"REPROVADO: dump de 30d mais novo é de {d} ({idade} dias > {MAX_DIAS}) — o insights.yml parou de medir."
    return 0, f"ok: dump de 30d mais novo é de {d} ({idade} dia(s))"


def auto_teste():
    hoje = dt.date(2026, 11, 21)
    casos = [
        ("positivo: dump de 12 dias reprova", ["insights_2026-11-09_30d.json"], 1),
        ("positivo: sem dump nenhum reprova", ["insights_2026-11-20_90d.json", "outro.json"], 1),
        ("negativo: dump de 5 dias passa", ["insights_2026-11-09_30d.json", "insights_2026-11-16_30d.json"], 0),
        ("fronteira: exatamente 10 dias passa", ["insights_2026-11-11_30d.json"], 0),
        ("fronteira: 11 dias reprova", ["insights_2026-11-10_30d.json"], 1),
    ]
    falhas = 0
    for nome, nomes, esperado in casos:
        rc, _ = veredito(nomes, hoje)
        ok = rc == esperado
        falhas += not ok
        print(f"[{'ok' if ok else 'FALHOU'}] {nome}")
    print(f"AUTO-TESTE: {len(casos) - falhas}/{len(casos)} —", "PASSOU" if not falhas else "REPROVOU")
    return 1 if falhas else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--hoje"); ap.add_argument("--auto-teste", action="store_true")
    a = ap.parse_args()
    if a.auto_teste:
        sys.exit(auto_teste())
    hoje = dt.date.fromisoformat(a.hoje) if a.hoje else dt.datetime.now(dt.timezone.utc).date()
    rc, msg = veredito(os.listdir(PASTA), hoje)
    print(msg); sys.exit(rc)
