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

Reusa as primitivas de carrossel.py / marca.py (v2 da marca, 14/10/2026): mesmo
card-resumo dos verbetes (slide_resumo), rodapé CFM com paginação.
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


TITULO = "Diferença de perna: quando avaliar"


def slide():
    """Spec do slide no formato de carrossel.render_post (v2 da marca, 14/10/2026)."""
    return {"resumo": True, "kicker": "Para guardar", "title": TITULO,
            "bullets": [list(t) for t in TIERS], "fecho": FECHO}


def render():
    """Re-renderiza SÓ o 5º slide do post-alvo, no visual v2 (marca.py)."""
    from PIL import ImageDraw
    import marca as K
    var = C._var(POST_ALVO)
    ac = var["acento"] if var else C.GOLD
    img = K.fundo({"motivo": "diagonais"})
    K.cabecalho(img, x=C.M)
    d = ImageDraw.Draw(img)
    s = slide()
    C.slide_resumo(img, d, s["title"], s["bullets"], var, ac, fecho=s["fecho"], rotulo=s["kicker"])
    C.footer(d, SLIDE_INDEX, 5, ac=ac)
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
    caminho = os.path.join(outdir, f"{POST_ALVO}_{SLIDE_INDEX + 1}.jpg")
    img.convert("RGB").save(caminho, "JPEG", quality=92)
    return caminho


if __name__ == "__main__":
    p = render()
    print(f"slide gravado: {p}")
