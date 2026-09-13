# -*- coding: utf-8 -*-
"""
checar_legenda.py — lint da FILA (A4, 12/09/2026): toda legenda ainda não publicada em
reels.json e posts.json tem de passar em legenda.validar(): sem hashtag, sem pedido de curtida,
UMA CTA (enviar no reel / salvar no carrossel), 1–2 menções, assinatura com Médico+CRM+RQE.

Escopo = fila − state/published.json. O acervo já publicado NÃO é auditado (mexer no JSON não
muda o que está no ar; só sujaria a contagem — lição de 02/08). Os reels mudos legados
(reel04–reel30, lote LEGADO-PRE-GATE) entram no universo como qualquer item: legenda é legenda.

Exit: 0 = fila limpa (universo > 0); 1 = violação; 2 = erro de ambiente. Zero itens = FALHA.
Auto-teste embutido (--auto-teste): semeia uma legenda com hashtag e outra pedindo curtida e
exige reprovação — detector que nunca reprovou não vale (lição da casa).
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from legenda import validar  # noqa: E402


def _carrega(nome):
    with open(os.path.join(ROOT, nome), encoding="utf-8-sig") as f:
        return json.load(f)


def universo():
    st = _carrega(os.path.join("state", "published.json"))
    done = {e["id"] for e in st.get("published", [])}
    itens = []
    for lib, formato in (("reels.json", "reel"), ("posts.json", "post")):
        for x in _carrega(lib):
            if x.get("id") in done:
                continue
            itens.append((lib, formato, x.get("id"), x.get("caption", "")))
    return itens


def main(itens=None):
    itens = universo() if itens is None else itens
    if not itens:
        print("REPROVADO: universo VAZIO (0 itens na fila) — zero verificados = falha, não sucesso.")
        return 1
    ruins = []
    for lib, formato, iid, cap in itens:
        p = validar(cap, formato)
        if p:
            ruins.append((lib, iid, p))
    print(f"Universo: {len(itens)} legenda(s) na fila; violações: {len(ruins)}")
    for lib, iid, p in ruins:
        print(f"  [{lib}] {iid}: " + "; ".join(p))
    return 1 if ruins else 0


def auto_teste():
    ok_cap = ("Uma perna mais curta que a outra: quando avaliar.\n\nEnvia para quem precisa disso.\n\n"
              "Sociedade da área: @asami.brasil\n\nDr. Rafael Vargas · Médico · CRM-SP 226103 · RQE 137901\n"
              "Conteúdo educativo; não substitui avaliação individual.")
    casos = [
        ("controle NEGATIVO (legenda limpa passa)", [("reels.json", "reel", "t_ok", ok_cap)], 0),
        ("controle POSITIVO: hashtag", [("reels.json", "reel", "t_tag", ok_cap + "\n\n#fixador")], 1),
        ("controle POSITIVO: pede curtida", [("reels.json", "reel", "t_like", ok_cap.replace("Envia para quem precisa disso.", "Curte e envia para quem precisa disso."))], 1),
        ("controle POSITIVO: duas CTAs", [("posts.json", "post", "t_2cta", ok_cap)], 1),   # reel-CTA num post
        ("controle POSITIVO: sem menção", [("reels.json", "reel", "t_menc", ok_cap.replace("Sociedade da área: @asami.brasil\n\n", ""))], 1),
        ("controle POSITIVO: universo vazio", [], 1),
    ]
    falhas = 0
    for rotulo, itens, esperado in casos:
        rc = main(itens)
        passou = rc == esperado
        print(("[passou] " if passou else "[FALHOU] ") + f"{rotulo} (exit {rc}, esperado {esperado})")
        falhas += 0 if passou else 1
    print("AUTO-TESTE:", "PASSOU" if not falhas else f"REPROVOU ({falhas})")
    return 0 if not falhas else 1


if __name__ == "__main__":
    if "--auto-teste" in sys.argv:
        sys.exit(auto_teste())
    sys.exit(main())
