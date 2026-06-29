# -*- coding: utf-8 -*-
"""
LINT CFM — roda os guardrails compartilhados (cfm_guardrails.auditar) sobre TODO o conteúdo:
  - EPISODES (roteiros narrados): legenda (contexto público, exige assinatura) + texto das cenas.
  - Bibliotecas PUBLICADAS: reels.json, posts.json, sequences.json, stories.json (legendas).
Saída: lista de VIOLACAO (proibido) e REVISAR (conferir contexto). Idempotente, só leitura.
Rodar: python checar_cfm.py   (use PYTHONIOENCODING=utf-8 no Windows).
Vira gate de publicação: 0 VIOLACAO é o alvo.
"""
import json
import os
from cfm_guardrails import auditar

ROOT = os.path.dirname(os.path.abspath(__file__))


def texto_cenas(ep):
    partes = []
    for sc in ep.get("scenes", []):
        partes += [sc.get("k", "")] + sc.get("sc", []) + [sc.get("sub", ""), sc.get("vo", "")]
    return " ".join(p for p in partes if p)


def main():
    violacoes = []   # (origem, id, severidade, regra, detalhe)
    revisar = []

    def registra(origem, _id, issues):
        for sev, regra, det in issues:
            (violacoes if sev == "VIOLACAO" else revisar).append((origem, _id, sev, regra, det))

    # 1) EPISODES
    try:
        from episodios_pe_no_chao import EPISODES
        for ep in EPISODES:
            registra("episodio:legenda", ep["id"], auditar(ep.get("caption", ""), "publico"))
            registra("episodio:cenas", ep["id"], auditar(texto_cenas(ep), "mensagem"))
        print(f"EPISODES auditados: {len(EPISODES)}")
    except Exception as e:
        print("AVISO: nao carregou EPISODES:", e)

    # 2) Bibliotecas publicadas
    for arq in ["reels.json", "posts.json", "sequences.json", "stories.json"]:
        p = os.path.join(ROOT, arq)
        if not os.path.exists(p):
            continue
        try:
            d = json.load(open(p, encoding="utf-8"))
            itens = d if isinstance(d, list) else []
            n = 0
            for it in itens:
                cap = it.get("caption") if isinstance(it, dict) else None
                if cap:
                    registra(arq, it.get("id", "?"), auditar(cap, "publico"))
                    n += 1
            print(f"{arq}: {n} legendas auditadas")
        except Exception as e:
            print(f"AVISO: {arq}:", e)

    # Relatório
    print("\n=== LINT CFM ===")
    print("VIOLACOES (proibido — corrigir):", len(violacoes))
    for origem, _id, sev, regra, det in violacoes:
        print(f"   [VIOLACAO] {origem:22s} {str(_id):26s} {regra}: {det}")
    # REVISAR: agrupar por regra (costuma ter muito da 'assinatura' falso-positivo de cena)
    from collections import Counter
    porreg = Counter(r[3] for r in revisar)
    print("\nREVISAR (conferir contexto):", len(revisar), "->", dict(porreg))
    # mostra os REVISAR que NAO sao 'assinatura' (esses sao os que importam)
    relevantes = [r for r in revisar if r[3] != "assinatura"]
    for origem, _id, sev, regra, det in relevantes[:40]:
        print(f"   [REVISAR]  {origem:22s} {str(_id):26s} {regra}: {det}")
    return violacoes, revisar


if __name__ == "__main__":
    main()
