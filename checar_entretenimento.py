#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
checar_entretenimento.py — portão do CI para a GERAÇÃO NOVA (episodios_entretenimento.py + as
entradas de formato novo em reels.json). Não importa skia: roda no CI leve.

O que reprova (exit 1):
  1. Episódio mal formado (campos, tamanhos, conversa começando pelo paciente, CTA de envio).
  2. Qualquer texto do episódio (tela, voz, legenda) com VIOLAÇÃO CFM.
  3. Entrada de reels.json com `formato` novo sem episódio, sem o mp4 no repo, com legenda que não
     passa em `legenda.validar`, sem a declaração de voz de IA (que liga o rótulo da Meta), ou cujo
     `scenes` não bate com o texto do episódio (o portão CFM do publish lê `scenes`: texto
     divergente = portão lendo outra coisa que não o vídeo).
  4. Universo vazio (nenhum episódio) — vazio não é aprovação.

Uso:
  python checar_entretenimento.py              # confere
  python checar_entretenimento.py --auto-teste # prova que reprova de verdade (controles semeados)
"""
import copy
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

ICONES = {"fixador", "gesso", "muleta", "pinos", "osso"}
CENAS = {"cf_alongamento", "cf_fratura_cola"}
FORMATOS = {"conversa", "como_funciona"}
SIG = "Dr. Rafael Vargas · Médico · CRM-SP 226103 · RQE 137901"


def textos(ep):
    t = list(ep.get("gancho", [])) + [f.get("texto", "") for f in ep.get("falas", [])] + list(ep.get("roteiro", []))
    return [x for x in t + [ep.get("cta", ""), ep.get("legenda", ""), ep.get("personagem", "")] if x]


def cenas_de(ep):
    """O texto que vai em reels.json -> scenes (o que o portão CFM do publish audita)."""
    if ep["formato"] == "conversa":
        return [{"quem": f["quem"], "vo": f["texto"]} for f in ep["falas"]] + [{"quem": "F", "vo": ep["cta"]}]
    return [{"vo": s} for s in ep["roteiro"]]


def checar_episodio(ep):
    p = []
    f = ep.get("formato")
    if f not in FORMATOS:
        return [f"formato inválido {f!r}"]
    for campo in ("id", "serie", "familia", "cta", "legenda"):
        if not ep.get(campo):
            p.append(f"falta {campo}")
    if ep.get("familia") not in ("reconstrucao", "pediatria"):
        p.append("familia tem de ser reconstrucao|pediatria")
    if not str(ep.get("cta", "")).startswith(("Manda ", "Envia ")):
        p.append("CTA tem de pedir ENVIO (começar por 'Manda ' ou 'Envia ')")
    if f == "conversa":
        if ep.get("icone") not in ICONES:
            p.append(f"icone {ep.get('icone')!r} fora de {sorted(ICONES)}")
        g = ep.get("gancho", [])
        if len(g) != 2 or any(len(x) > 24 for x in g):
            p.append("gancho = 2 linhas de até 24 caracteres")
        falas = ep.get("falas", [])
        if not falas or falas[0].get("quem") != "P":
            p.append("a conversa começa pelo paciente (P)")
        for a, b in zip(falas, falas[1:]):
            if a.get("quem") == b.get("quem"):
                p.append("falas P/F têm de alternar"); break
        for x in falas:
            lim = 50 if x.get("quem") == "P" else 110
            if len(x.get("texto", "")) > lim:
                p.append(f"fala {x.get('quem')} com {len(x['texto'])} caracteres (máx {lim}): {x['texto'][:40]!r}")
        if len(ep.get("cta", "")) > 60:
            p.append("CTA longa demais (máx 60)")
    else:
        if ep.get("cena") not in CENAS:
            p.append(f"cena {ep.get('cena')!r} sem módulo conhecido {sorted(CENAS)}")
        rot = ep.get("roteiro", [])
        if not rot or rot[-1] != ep.get("cta"):
            p.append("a última frase do roteiro tem de ser a CTA")
        n = sum(len(s.split()) for s in rot)
        if not 50 <= n <= 95:
            p.append(f"roteiro com {n} palavras (faixa 50-95)")
    from cfm_guardrails import auditar
    for s in textos(ep):
        for sev, regra, det in auditar(f"{s} · {SIG}", contexto="publico"):
            if sev == "VIOLACAO":
                p.append(f"CFM {regra}: {det} — {s[:50]!r}")
    return p


def checar_fila(eps, reels):
    import legenda
    p = []
    por_id = {e["id"]: e for e in eps}
    for it in reels:
        f = it.get("formato")
        if not f:
            continue
        iid = it["id"]
        if f not in FORMATOS:
            p.append(f"{iid}: formato {f!r} desconhecido"); continue
        ep = por_id.get(iid)
        if not ep:
            p.append(f"{iid}: entrada de formato novo SEM episódio em episodios_entretenimento.py"); continue
        if ep["formato"] != f:
            p.append(f"{iid}: formato da fila ({f}) diverge do episódio ({ep['formato']})")
        if not os.path.exists(os.path.join(ROOT, it.get("video", "").replace("/", os.sep))):
            p.append(f"{iid}: vídeo {it.get('video')!r} NÃO existe no repo — publicar falharia")
        cap = it.get("caption", "")
        for v in legenda.validar(cap, "reel"):
            p.append(f"{iid}: legenda — {v}")
        if "voz digital (ia)" not in cap.lower() and not it.get("voz_ia"):
            p.append(f"{iid}: sem declaração de voz de IA — o rótulo da Meta não seria ligado")
        if it.get("scenes") != cenas_de(ep):
            p.append(f"{iid}: `scenes` diverge do texto do episódio — o portão CFM leria outra coisa")
    return p


def conferir(eps=None, reels=None, verbose=True):
    if eps is None:
        from episodios_entretenimento import EPISODIOS_ENTRETENIMENTO as eps
    if reels is None:
        reels = json.load(open(os.path.join(ROOT, "reels.json"), encoding="utf-8-sig"))
    probs = []
    if not eps:
        probs.append("universo VAZIO: nenhum episódio — vazio não é aprovação")
    ids = [e.get("id") for e in eps]
    if len(ids) != len(set(ids)):
        probs.append("id de episódio duplicado")
    for e in eps:
        probs += [f"{e.get('id')}: {x}" for x in checar_episodio(e)]
    probs += checar_fila(eps, reels)
    if verbose:
        novos = [r for r in reels if r.get("formato")]
        print(f"episódios: {len(eps)} | na fila com formato novo: {len(novos)} | problemas: {len(probs)}")
        for x in probs:
            print("  -", x)
    return probs


def auto_teste():
    from episodios_entretenimento import EPISODIOS_ENTRETENIMENTO as base
    reels = json.load(open(os.path.join(ROOT, "reels.json"), encoding="utf-8-sig"))
    ok = True
    casos = []
    e1 = copy.deepcopy(base); e1[0]["legenda"] += " Corrige a dismetria."             # termo vetado
    casos.append(("termo vetado na legenda", e1, reels))
    e2 = copy.deepcopy(base)
    conv = next(e for e in e2 if e["formato"] == "conversa"); conv["falas"].insert(0, {"quem": "F", "texto": "oi"})
    casos.append(("conversa começando pelo personagem", e2, reels))
    e3 = copy.deepcopy(base); e3[0]["cta"] = "Curta e compartilhe."
    casos.append(("CTA sem pedido de envio", e3, reels))
    casos.append(("universo vazio", [], reels))
    r5 = copy.deepcopy(reels) + [{"id": base[0]["id"], "formato": base[0]["formato"], "video": "reels/_nao_existe.mp4",
                                   "caption": "x", "scenes": []}]
    casos.append(("fila com vídeo inexistente e legenda torta", base, r5))
    for nome, eps, rs in casos:
        pr = conferir(eps, rs, verbose=False)
        print(f"[{'ok' if pr else 'FALHOU'}] positivo: {nome} -> {len(pr)} problema(s)")
        ok &= bool(pr)
    pr = conferir(base, [r for r in reels if not r.get("formato")], verbose=False)
    print(f"[{'ok' if not pr else 'FALHOU'}] negativo: episódios reais sem entrada nova na fila passam ({pr[:2]})")
    ok &= not pr
    print("AUTO-TESTE:", "PASSOU" if ok else "REPROVOU — não confiar no portão")
    return 0 if ok else 1


def main():
    if "--auto-teste" in sys.argv:
        return auto_teste()
    return 1 if conferir() else 0


if __name__ == "__main__":
    sys.exit(main())
