# -*- coding: utf-8 -*-
"""Regra de QUAL reel sai em cada dia — fonte ÚNICA, usada pelo publish.py (que publica) e pelo
publish_agenda.py (que projeta o PROGRAMACAO.md). Antes eram duas cópias, e a da agenda lia a cota
do ambiente LOCAL enquanto o publish lia a variável do repositório: bastava mudar a variável para
a página mentir (auditoria 19/10/2026). Não importa nada pesado nem exige secret.

Cota de lâminas (Rafael, 18/10/2026: "desacelerar as lâminas"): item sem `formato` = lâmina de
texto antiga, no máximo LAMINAS_POR_SEMANA por semana (segunda 00:00 a domingo 23:59, BRT);
formato novo (conversa / como_funciona) sem cota. Mudar a cota = editar LAMINAS_POR_SEMANA_PADRAO
aqui e commitar (a página e o robô mudam juntos). A variável de ambiente LAMINAS_POR_SEMANA só
existe para os testes; o publish.yml NÃO a define.
"""
import datetime as dt
import os

BRT = dt.timezone(dt.timedelta(hours=-3))
LAMINAS_POR_SEMANA_PADRAO = 1
_SEM_COTA = ("off", "nao", "não", "no", "false", "sem", "-1")


def cota_laminas(valor=None):
    """-1 = sem cota; 0 = lâminas suspensas; N = até N por semana. Valor ilegível -> padrão com
    aviso (antes, 'off' derrubava o publish INTEIRO no import, posts e stories junto)."""
    v = os.environ.get("LAMINAS_POR_SEMANA") if valor is None else valor
    if v is None or str(v).strip() == "":
        return LAMINAS_POR_SEMANA_PADRAO
    v = str(v).strip().lower()
    if v in _SEM_COTA:
        return -1
    try:
        return int(v)
    except ValueError:
        print(f"::warning::LAMINAS_POR_SEMANA={v!r} ilegível — usando o padrão {LAMINAS_POR_SEMANA_PADRAO}", flush=True)
        return LAMINAS_POR_SEMANA_PADRAO


def formato(item):
    return (item.get("formato") or "lamina").strip().lower()


def laminas_na_semana(state, reels, agora_brt):
    """Quantas lâminas já saíram nesta semana (segunda 00:00 BRT até agora). Usa o `formato`
    gravado no registro do publish; registro antigo (sem o campo) cai no reels.json — peça nova
    retirada da fila depois de publicada não passa mais a contar como lâmina."""
    fmt = {r["id"]: formato(r) for r in reels}
    ini = (agora_brt - dt.timedelta(days=agora_brt.weekday())).date()
    n = 0
    for e in state.get("published", []):
        if e.get("kind") != "reel" or not e.get("at"):
            continue
        try:
            quando = dt.datetime.fromisoformat(e["at"]).astimezone(BRT).date()
        except ValueError:
            continue
        f = e.get("formato") or fmt.get(e["id"], "lamina")
        if quando >= ini and f == "lamina":
            n += 1
    return n


def proximo_reel(reels, done, state, agora_brt, cota=None):
    """Primeiro reel da fila que pode sair hoje: formato novo sempre; lâmina só dentro da cota."""
    cota = cota_laminas() if cota is None else cota
    cota_livre = cota < 0 or laminas_na_semana(state, reels, agora_brt) < cota
    for x in reels:
        if x["id"] in done:
            continue
        if formato(x) == "lamina" and not cota_livre:
            continue
        return x
    return None
