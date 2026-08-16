# -*- coding: utf-8 -*-
"""
Card-resumo guardavel: substitui o ultimo slide (CTA generico) de UM post especifico
sobre discrepancia de membro NA CRIANCA por um resumo das faixas em cm que orientam
a avaliacao.

Escopo deliberadamente estreito: o conteudo vem de um post do LinkedIn do proprio
Rafael (li-010, 27/07/2026, escrito a colegas), autorizado por ele em 15/08/2026 para
"transpor as faixas em cm e a escada de condutas... para linguagem leiga". A escada
usa o multiplicador de Paley e a indicacao de epifisiodese — tecnica que só funciona
com a placa de crescimento ABERTA. Por isso o card so vai no post
`c_pnc_perna_curta_crianca` (mesma audiencia do texto-fonte: crianca). NAO aplicar a
posts de adulto (c_on_discrepancia, c_on_medir_antes etc.) seria transplantar conduta
pediatrica para contexto errado — o mais perto que este script chega de "inventar
dado clinico" e por isso o script recusa fazer isso.

Reusa as primitivas de desenho de carrossel.py (mesma identidade visual dos outros
4 slides do post: base(), footer() com paginacao, trk(), wrap(), fontes).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import carrossel as C

POST_ALVO = "c_pnc_perna_curta_crianca"
SLIDE_INDEX = 4  # 0-based -> arquivo _5.jpg (5o de 5 slides)

TIERS = [
    ("Até 1–2 cm", "costuma ser só acompanhar — diferença pequena, sem sintoma."),
    ("2 a 5 cm (projetada)", "pode indicar correção pelo próprio crescimento, no momento certo."),
    ("Acima de 5 cm", "ou causa que tende a piorar: o plano muda e o acompanhamento começa cedo."),
]
FECHO = "Guia geral — a avaliação do seu filho é sempre individual."


def render():
    img, d = C.base(motif=True, var=None)
    AC = C.GOLD

    C.trk(d, (C.M, 300), "PARA GUARDAR", C.F(C.NB, 24), AC, 5)
    d.line([(C.M, 340), (C.M + 58, 340)], fill=AC, width=3)

    tf = C.F(C.SB, 66)
    ty = 380
    for ln in C.wrap("Diferença de perna: quando avaliar", tf, C.W - 2 * C.M):
        d.text((C.M, ty), ln, font=tf, fill=C.CREAM)
        ty += int(tf.size * 1.1)
    ty += 26

    lead_f = C.F(C.NB, 32)
    body_f = C.F(C.NR, 34)
    for lead, corpo in TIERS:
        d.text((C.M, ty), lead, font=lead_f, fill=AC)
        ty += int(lead_f.size * 1.15)
        for ln in C.wrap(corpo, body_f, C.W - 2 * C.M):
            d.text((C.M, ty), ln, font=body_f, fill=C.TXT)
            ty += int(body_f.size * 1.28)
        ty += 22

    ty += 10
    for ln in C.wrap(FECHO, C.F(C.NR, 26), C.W - 2 * C.M):
        d.text((C.M, ty), ln, font=C.F(C.NR, 26), fill=C.MUT)
        ty += 34

    C.footer(d, SLIDE_INDEX, 5, ac=AC)

    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
    caminho = os.path.join(outdir, f"{POST_ALVO}_{SLIDE_INDEX + 1}.jpg")
    img.save(caminho, "JPEG", quality=92)
    return caminho


if __name__ == "__main__":
    p = render()
    print(f"slide gravado: {p}")
