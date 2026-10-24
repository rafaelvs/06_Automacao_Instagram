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
    cansativo". A 1ª versão (1 por semana) punha conversa numa segunda e outra na segunda seguinte,
    e ele estranhou ("conversa fixador hoje e já conversa com pinos na segunda?") -> agora é
    INTERVALO: no mínimo DIAS_ENTRE_CONVERSAS_PADRAO dias desde a última conversa publicada.
  * como_funciona — sem cota: é o formato principal.

ALL-IN (Rafael, 24/10/2026), depois dos primeiros números: cf_alongamento alcançou 2.049 contas em
2,8 dias (16 envios) e cf_fratura_cola 1.333 em menos de 1 dia, contra mediana 32 das lâminas em 90
dias; a conversa cv_fixador ficou em 56. "a gente tem que dar all-in agora nesse novo modelo [...] a
gente vai colocar todas as postagens dentro de um modelo parecido". Por padrão a lâmina fica com
cota 0 (suspensa) e a conversa desligada (CONVERSAS_ATIVAS_PADRAO = False): só COMO FUNCIONA sai.
Nada é apagado da fila — religar é mudar um padrão aqui. Dia de reel sem COMO FUNCIONA = dia sem
reel: a produção tem de manter a fila cheia (~4 por semana).
"""
import datetime as dt
import os

BRT = dt.timezone(dt.timedelta(hours=-3))
LAMINAS_POR_SEMANA_PADRAO = 0            # 24/10: all-in COMO FUNCIONA (era 1 por semana desde 18/10)
DIAS_ENTRE_CONVERSAS_PADRAO = 10          # Rafael, 19/10: "pode deixar a cada 10 dias" (vale se religar)
CONVERSAS_ATIVAS_PADRAO = False           # 24/10: all-in COMO FUNCIONA — conversa suspensa
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


def dias_entre_conversas(valor=None):
    """Intervalo mínimo (dias) entre duas conversas publicadas; -1/'off' = sem intervalo."""
    return _cota("DIAS_ENTRE_CONVERSAS", DIAS_ENTRE_CONVERSAS_PADRAO, valor)


def conversas_ativas(valor=None):
    """A série CONVERSA está ligada? Padrão False desde 24/10 (all-in COMO FUNCIONA)."""
    v = os.environ.get("CONVERSAS_ATIVAS") if valor is None else valor
    if v is None or str(v).strip() == "":
        return CONVERSAS_ATIVAS_PADRAO
    return str(v).strip().lower() in ("on", "1", "true", "sim", "yes")


def ultima_publicacao(state, reels, fmt_alvo):
    """Data BRT do último reel publicado do formato `fmt_alvo` (None se nunca saiu)."""
    fmt = {r["id"]: formato(r) for r in reels}
    ult = None
    for e in state.get("published", []):
        if e.get("kind") != "reel" or not e.get("at"):
            continue
        if (e.get("formato") or fmt.get(e["id"], "lamina")) != fmt_alvo:
            continue
        try:
            d = dt.datetime.fromisoformat(e["at"]).astimezone(BRT).date()
        except ValueError:
            continue
        ult = d if ult is None or d > ult else ult
    return ult


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


def proximo_reel(reels, done, state, agora_brt, cota=None, dias_conversa=None, conversa_ativa=None):
    """Primeiro reel da fila que pode sair hoje: como_funciona sempre; lâmina só dentro da cota
    semanal; conversa só se a série estiver ligada E a última saiu há pelo menos `dias_conversa`
    dias. `cota` = cota de lâminas (nome histórico)."""
    cota = cota_laminas() if cota is None else cota
    dias = dias_entre_conversas() if dias_conversa is None else dias_conversa
    ativa = conversas_ativas() if conversa_ativa is None else conversa_ativa
    ult = ultima_publicacao(state, reels, "conversa")
    livre = {"lamina": cota < 0 or publicados_na_semana(state, reels, agora_brt, "lamina") < cota,
             "conversa": ativa and (dias < 0 or ult is None or (agora_brt.date() - ult).days >= dias)}
    for x in reels:
        if x["id"] in done:
            continue
        if not livre.get(formato(x), True):
            continue
        return x
    return None
