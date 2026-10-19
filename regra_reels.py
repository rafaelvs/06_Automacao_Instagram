# -*- coding: utf-8 -*-
"""Regra de QUAL reel sai em cada dia — fonte ÚNICA, usada pelo publish.py (que publica) e pelo
publish_agenda.py (que projeta o PROGRAMACAO.md). Antes eram duas cópias, e a da agenda lia a cota
do ambiente LOCAL enquanto o publish lia a variável do repositório: bastava mudar a variável para
a página mentir (auditoria 19/10/2026). Não importa nada pesado nem exige secret.

Cotas por formato, por semana (segunda 00:00 a domingo 23:59, BRT). Mudar uma cota = editar o
padrão aqui e commitar (a página e o robô mudam juntos). As variáveis de ambiente só existem para
os testes; o publish.yml NÃO as define.
  * lâmina (item sem `formato`, texto antigo lido em voz alta) — Rafael, 18/10/2026: "desacelerar
    as lâminas" -> no máximo 1 por semana.
  * conversa ("Se o seu ___ pudesse responder") — Rafael, 19/10/2026: "é legal, mas tem que ser mais
    espaçada [...] deixar essa série de responder vez ou outra somente, pq é um modelo mais
    cansativo" -> no máximo 1 por semana.
  * como_funciona — sem cota: é o formato principal.
"""
import datetime as dt
import os

BRT = dt.timezone(dt.timedelta(hours=-3))
LAMINAS_POR_SEMANA_PADRAO = 1
CONVERSAS_POR_SEMANA_PADRAO = 1
_SEM_COTA = ("off", "nao", "não", "no", "false", "sem", "-1")


def _cota(var, padrao, valor=None):
    """-1 = sem cota; 0 = suspenso; N = até N por semana. Valor ilegível -> padrão com aviso
    (antes, 'off' derrubava o publish INTEIRO no import, posts e stories junto)."""
    v = os.environ.get(var) if valor is None else valor
    if v is None or str(v).strip() == "":
        return padrao
    v = str(v).strip().lower()
    if v in _SEM_COTA:
        return -1
    try:
        return int(v)
    except ValueError:
        print(f"::warning::{var}={v!r} ilegível — usando o padrão {padrao}", flush=True)
        return padrao


def cota_laminas(valor=None):
    return _cota("LAMINAS_POR_SEMANA", LAMINAS_POR_SEMANA_PADRAO, valor)


def cota_conversas(valor=None):
    return _cota("CONVERSAS_POR_SEMANA", CONVERSAS_POR_SEMANA_PADRAO, valor)


def formato(item):
    return (item.get("formato") or "lamina").strip().lower()


def publicados_na_semana(state, reels, agora_brt, fmt_alvo):
    """Quantos reels do formato `fmt_alvo` já saíram nesta semana (segunda 00:00 BRT até agora).
    Usa o `formato` gravado no registro do publish; registro antigo (sem o campo) cai no
    reels.json — peça retirada da fila depois de publicada não muda mais de formato."""
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
        if quando >= ini and f == fmt_alvo:
            n += 1
    return n


def laminas_na_semana(state, reels, agora_brt):
    return publicados_na_semana(state, reels, agora_brt, "lamina")


def proximo_reel(reels, done, state, agora_brt, cota=None, cota_conversa=None):
    """Primeiro reel da fila que pode sair hoje: como_funciona sempre; lâmina e conversa só dentro
    da cota semanal de cada uma. `cota` = cota de lâminas (nome histórico)."""
    cotas = {"lamina": cota_laminas() if cota is None else cota,
             "conversa": cota_conversas() if cota_conversa is None else cota_conversa}
    livre = {f: c < 0 or publicados_na_semana(state, reels, agora_brt, f) < c for f, c in cotas.items()}
    for x in reels:
        if x["id"] in done:
            continue
        if not livre.get(formato(x), True):
            continue
        return x
    return None
