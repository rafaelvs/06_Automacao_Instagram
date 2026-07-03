# -*- coding: utf-8 -*-
"""
Rotação determinística de LAYOUT (composição espacial + ritmo tipográfico) por episode_id.
Espelha ganchos.py. Combate a política "Inauthentic Content" do YouTube (jan/2026) variando
a COMPOSIÇÃO entre vídeos, sem quebrar marca (premium/minimalista) nem CFM (footer CRM/RQE).

ROTAÇÃO: hash de caracteres % 5 sobre os layouts NÃO-triviais (L1..L5). L0 'classico' é o
default puro e FICA FORA da roleta (congelamento byte-idêntico). Offset +2 para _kids
(coprimo com 5 → par adulto+infantil nunca compartilha layout). Sal distinto do +3 de
ganchos.arquetipo para descorrelacionar layout×arquétipo.

USO ao autorar um episódio novo (opt-in explícito, igual a palette):
    import ganchos_layout
    episode["layout"] = ganchos_layout.layout_para("artrorrise")   # ex.: "faixa_direita"
Ou deixe episode["layout"] = "auto" e o render resolve sozinho.
"""

# L0 ('classico') NÃO entra — é o default congelado. Roleta = 5 layouts distintos.
LAYOUTS_ROT = [
    "editorial_baixo",   # L1
    "centro_focal",      # L2
    "faixa_direita",     # L3
    "distico_bicolor",   # L4
    "manchete_regua",    # L5
]

_SALT = 2  # descorrela de ganchos.arquetipo (que usa +3 e módulo 6)


def layout_para(episode_id: str) -> str:
    """Layout determinístico do episódio (roleta L1..L5). Opt-in: grave em episode['layout']."""
    eid = str(episode_id)
    idx = (sum(map(ord, eid)) + _SALT) % len(LAYOUTS_ROT)
    if eid.endswith("_kids"):
        idx = (idx + 2) % len(LAYOUTS_ROT)   # +2 coprimo com 5: par adulto+infantil difere
    return LAYOUTS_ROT[idx]


def layout_para_sequencia(ids):
    """Atribuição BALANCEADA + anti-consecutivo + par-adulto/kids-nunca-igual, determinística.
    Parte do layout hash-preferido de cada episódio, mas escolhe o candidato MENOS USADO até então
    que não repita o vizinho anterior nem o layout do par adulto (para _kids). Distribui uniforme
    (evita o desbalanço do hash puro, ex.: centro_focal 2/34) sem perder a variação. Use ao autorar o batch."""
    from collections import Counter
    used = Counter(); out = []; prev = None; byid = {}
    n = len(LAYOUTS_ROT)
    for eid in ids:
        start = LAYOUTS_ROT.index(layout_para(eid))
        cands = [LAYOUTS_ROT[(start + k) % n] for k in range(n)]   # ordem determinística a partir do hash
        forbidden = set()
        if prev is not None: forbidden.add(prev)
        if str(eid).endswith("_kids"):
            adult = str(eid)[:-5]
            if adult in byid: forbidden.add(byid[adult])            # par adulto+kids nunca igual (robusto a reordenação)
        ok = [c for c in cands if c not in forbidden] or cands
        lay = min(ok, key=lambda c: (used[c], cands.index(c)))      # menos usado; empate → ordem do hash
        out.append(lay); used[lay] += 1; prev = lay; byid[eid] = lay
    return out


_DESC = {
    "editorial_baixo": "Hook aterra na base (terço-inferior); vazio em cima; motivo em wash; header faixa.",
    "centro_focal":    "Bloco centralizado no eixo X (pôster); sem motivo; header minimal.",
    "faixa_direita":   "Texto encostado à direita (espelho do L0); motivo empurrado à esquerda.",
    "distico_bicolor": "Linha1 pequena/mut → linha2 enorme/dourada: clímax de escala inter-linha.",
    "manchete_regua":  "Manchete no topo extremo, sem motivo, régua dourada estruturando a página.",
}


def info(episode_id: str) -> dict:
    nome = layout_para(episode_id)
    return {"layout": nome, "desc": _DESC[nome]}


def resumo_todos(ids=None) -> None:
    """Tabela layout × episódio (cruze com ganchos.resumo_todos para inspecionar correlação)."""
    ids = ids or [
        "gesso_pos_op", "gesso_pos_op_kids", "fixador_externo", "fixador_externo_kids",
        "carga_fisio", "carga_fisio_kids", "artrorrise", "artrorrise_kids",
        "growth_guided", "growth_guided_kids",
    ]
    seq = layout_para_sequencia(ids)
    print(f"{'ID':<26}{'LAYOUT(hash)':<20}{'LAYOUT(seq)'}")
    print("-" * 66)
    for eid, s in zip(ids, seq):
        print(f"{eid:<26}{layout_para(eid):<20}{s}")


if __name__ == "__main__":
    resumo_todos()
