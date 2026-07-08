# -*- coding: utf-8 -*-
"""
LINT v6 — mede o GAP das 3 ALAVANCAS da auditoria v6 no conteudo atual. 100% ADITIVO e ADVISORY:
arquivo NOVO, so leitura, NUNCA levanta pro gate, NUNCA entra em BLOQUEIOS/exit. So MEDE (relatorio
com % e a lista dos que faltam) para virar a porta dos proximos lotes — nao corrige conteudo agora.

As 3 alavancas (todas por EPISODIO, sobre os EPISODES de episodios_pe_no_chao):
  1. SEND-FIRST      : a peca termina com send-ask a um TERCEIRO por CONDICAO
                       (reusa checar_send_hook.classificar_caption == 'SEND_OK'; FRACO/AUSENTE = gap).
  2. TRIPLA KEYWORD  : a MESMA keyword clinica canonica aparece em (a) fala do TTS da cena 0 (vo[0]),
                       (b) texto on-screen da cena 0 (k+sc+sub, SEM vo) e (c) 1a frase da caption.
  3. RETENCAO/HOOK   : cena 0 e hook SEM intro (reusa INTROS de checar_send_hook) + proxy de duracao
                       (n de cenas do reel; teto sugerido: >6 cenas ~ provavelmente >30s).

REUSO (nao reimplementa nada): checar_send_hook.classificar_caption / norm / INTROS;
                               checar_termo_popular.sem_hashtags / KW_CANONICAS.
FONTE da caption (checks 1 e 2c): ep["caption"] — a FONTE DE VERDADE por episodio. As copias em
reels.json/posts.json ja sao varridas pelo bloco [3b] do gate (checar_send_hook.auditar_captions()),
entao aqui NAO reescaneamos as bibliotecas (evita duplicar [3b]) e mantemos o denominador por episodio.

Rodar: PYTHONIOENCODING=utf-8 python checar_v6.py   (idempotente, so leitura).
"""
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:  # robustez: garante o import do repo mesmo se o cwd for outro
    sys.path.insert(0, ROOT)

from episodios_pe_no_chao import EPISODES
from checar_send_hook import classificar_caption, norm, INTROS
from checar_termo_popular import sem_hashtags, KW_CANONICAS

# Proxy de duracao (retencao): reels com muitas cenas tendem a passar de 30s e derrubar retencao.
TETO_CENAS = 6  # >6 cenas ~ provavelmente >30s (teto SUGERIDO, so sinaliza — nunca bloqueia)


def _pct(n, d):
    return (100.0 * n / d) if d else 0.0


def _primeira_frase(caption):
    """1a frase da caption, normalizada: 1o bloco (ate a 1a quebra de linha) e 1a sentenca (ate . ? !).
    Remove hashtags antes (nao ha tags no corpo inicial, mas fica blindado)."""
    corpo = sem_hashtags(str(caption)).strip()
    corpo = corpo.split("\n", 1)[0]
    frase = re.split(r"[.?!]", corpo, maxsplit=1)[0]
    return norm(frase)


def _kws_em(txt):
    """Conjunto de keywords canonicas (substring literal) presentes num texto ja normalizado."""
    return {k for k in KW_CANONICAS if k in txt}


# ----------------------------------------------------------------------------------------------------
# ALAVANCA 1 — SEND-FIRST (send-ask a um terceiro POR CONDICAO na caption do episodio).
# ----------------------------------------------------------------------------------------------------
def checar_send_first():
    """OK = classificar_caption(ep['caption']) == 'SEND_OK'. FRACO/AUSENTE contam como gap."""
    ok = fraco = ausente = 0
    gaps = []
    for ep in EPISODES:
        classe = classificar_caption(ep.get("caption", ""))
        if classe == "SEND_OK":
            ok += 1
        elif classe == "SEND_FRACO":
            fraco += 1
            gaps.append((ep.get("id", "?"), "SEND_FRACO"))
        else:
            ausente += 1
            gaps.append((ep.get("id", "?"), "SEND_AUSENTE"))
    total = len(EPISODES)
    return {"total": total, "ok": ok, "fraco": fraco, "ausente": ausente,
            "gap": fraco + ausente, "pct_ok": _pct(ok, total), "gaps": gaps}


# ----------------------------------------------------------------------------------------------------
# ALAVANCA 2 — TRIPLA KEYWORD (a MESMA keyword canonica na fala[vo0], na tela[k+sc+sub], na 1a frase da cap).
# So faz sentido para episodios que USAM algum jargao canonico; os sem keyword ficam em "n/a"
# (nao ha keyword para reforcar) e NAO entram no gap acionavel.
# ----------------------------------------------------------------------------------------------------
def checar_tripla_keyword():
    total = len(EPISODES)
    triple = candidatos = sem_kw = 0
    miss_vo = miss_tela = miss_cap = 0
    gaps = []
    for ep in EPISODES:
        cenas = ep.get("scenes", [])
        if not cenas:
            sem_kw += 1
            continue
        s0 = cenas[0]
        # (a) fala do TTS da cena 0  |  (b) texto on-screen da cena 0 (EXCLUI vo)  |  (c) 1a frase da caption
        vo0 = norm(s0.get("vo", ""))
        onscreen0 = norm(" ".join([s0.get("k", "")] + s0.get("sc", []) + [s0.get("sub", "")]))
        cap1 = _primeira_frase(ep.get("caption", ""))
        # keyword canonica presente em QUALQUER parte do episodio => define se e "candidato"
        full = norm(" ".join(
            " ".join([sc.get("k", "")] + sc.get("sc", []) + [sc.get("sub", ""), sc.get("vo", "")])
            for sc in cenas) + " " + sem_hashtags(str(ep.get("caption", ""))))
        kws_ep = _kws_em(full)
        if not kws_ep:
            sem_kw += 1
            continue
        candidatos += 1
        kv, kt, kc = _kws_em(vo0), _kws_em(onscreen0), _kws_em(cap1)
        if kv & kt & kc:  # a MESMA keyword nas 3 camadas
            triple += 1
        else:
            faltou = []
            if not (kws_ep & kv):
                miss_vo += 1
                faltou.append("vo")
            if not (kws_ep & kt):
                miss_tela += 1
                faltou.append("tela")
            if not (kws_ep & kc):
                miss_cap += 1
                faltou.append("cap")
            gaps.append((ep.get("id", "?"), sorted(kws_ep), "+".join(faltou) or "sem-interseccao"))
    return {"total": total, "triple": triple, "candidatos": candidatos, "sem_kw": sem_kw,
            "gap": candidatos - triple, "miss_vo": miss_vo, "miss_tela": miss_tela,
            "miss_cap": miss_cap, "pct_triple_cand": _pct(triple, candidatos),
            "pct_triple_total": _pct(triple, total), "gaps": gaps}


# ----------------------------------------------------------------------------------------------------
# ALAVANCA 3 — RETENCAO/HOOK (cena 0 sem intro + proxy de duracao por n de cenas).
# ----------------------------------------------------------------------------------------------------
def checar_retencao_hook():
    total = len(EPISODES)
    hook_ok = 0
    intro_gaps = []
    longos = []
    dist = Counter()
    for ep in EPISODES:
        cenas = ep.get("scenes", [])
        n = len(cenas)
        dist[n] += 1
        if n > TETO_CENAS:
            longos.append((ep.get("id", "?"), n))
        if not cenas:
            continue
        s0 = cenas[0]
        # mesma construcao do HOOK de checar_send_hook.main() (k+sc+sub+vo da cena 0)
        gancho = norm(" ".join([s0.get("k", "")] + s0.get("sc", []) + [s0.get("sub", ""), s0.get("vo", "")]))
        if any(intro in gancho for intro in INTROS):
            intro_gaps.append((ep.get("id", "?"), "intro no gancho"))
        else:
            hook_ok += 1
    return {"total": total, "hook_ok": hook_ok, "intro_gap": len(intro_gaps),
            "intro_gaps": intro_gaps, "pct_hook_ok": _pct(hook_ok, total),
            "cenas_dist": dict(sorted(dist.items())), "longos": longos,
            "n_longos": len(longos), "teto": TETO_CENAS}


def auditar():
    """Roda as 3 alavancas e devolve o dict consolidado + gap_total (advisory)."""
    sf = checar_send_first()
    tk = checar_tripla_keyword()
    rh = checar_retencao_hook()
    gap_total = sf["gap"] + tk["gap"] + rh["intro_gap"] + rh["n_longos"]
    return {"send_first": sf, "tripla_keyword": tk, "retencao_hook": rh, "gap_total": gap_total}


def relatorio_v6():
    """Imprime '=== [v6] Alavancas ===' com as 3 linhas (OK/gap) e devolve o dict de auditar().
    BLINDADO: nunca levanta — em falha imprime AVISO (fail-open RUIDOSO) e devolve gap_total=0."""
    try:
        d = auditar()
    except Exception as e:  # noqa: BLE001 — fail-open ruidoso proposital
        print("AVISO (fail-open): auditar() v6 falhou —", e)
        return {"send_first": {}, "tripla_keyword": {}, "retencao_hook": {}, "gap_total": 0, "erro": str(e)}

    sf, tk, rh = d["send_first"], d["tripla_keyword"], d["retencao_hook"]
    print("=== [v6] Alavancas === (%d episodios | ADVISORY — nunca bloqueia)" % sf.get("total", 0))
    print("[1] SEND-FIRST    : OK=%d/%d (%.0f%%)  gap=%d (fraco=%d, ausente=%d)" % (
        sf["ok"], sf["total"], sf["pct_ok"], sf["gap"], sf["fraco"], sf["ausente"]))
    print("[2] TRIPLA KEYWORD: OK=%d/%d candidatos (%.0f%%) | %d/%d do total | "
          "gap-camada: vo=%d tela=%d cap=%d | s/ keyword=%d" % (
              tk["triple"], tk["candidatos"], tk["pct_triple_cand"], tk["triple"], tk["total"],
              tk["miss_vo"], tk["miss_tela"], tk["miss_cap"], tk["sem_kw"]))
    print("[3] RETENCAO/HOOK : hook OK=%d/%d (%.0f%%) gap(intro)=%d | cenas>%d=%d (proxy >30s) | dist=%s" % (
        rh["hook_ok"], rh["total"], rh["pct_hook_ok"], rh["intro_gap"], rh["teto"],
        rh["n_longos"], rh["cenas_dist"]))

    # listas dos que faltam (advisory / detalhe)
    if sf["gaps"]:
        print("   -- [1] SEND-FIRST gaps (%d):" % len(sf["gaps"]))
        for i, c in sf["gaps"]:
            print("      [%s] %s" % (c, i))
    if tk["gaps"]:
        print("   -- [2] TRIPLA KEYWORD gaps (%d) (episodio :: keywords :: camada_faltante):" % len(tk["gaps"]))
        for i, kws, faltou in tk["gaps"]:
            print("      %-22s :: %s :: falta=%s" % (i, ",".join(kws) or "-", faltou))
    if rh["intro_gaps"]:
        print("   -- [3] HOOK gaps (intro no gancho) (%d):" % len(rh["intro_gaps"]))
        for i, c in rh["intro_gaps"]:
            print("      %s - %s" % (i, c))
    if rh["longos"]:
        print("   -- [3] RETENCAO: reels >%d cenas (proxy >30s) (%d):" % (rh["teto"], rh["n_longos"]))
        for i, n in rh["longos"]:
            print("      %-22s %d cenas" % (i, n))

    print(">>> [v6] gap_total (advisory, NAO afeta BLOQUEIOS/EXIT):", d["gap_total"])
    return d


if __name__ == "__main__":
    relatorio_v6()
