# -*- coding: utf-8 -*-
"""QUAL DOS DOIS? — pé chato (piloto da série-jogo; v4 de 26/10/2026, polimento depois dos leitores
às cegas: "a diferença entre A e B é sutil demais no celular").

Formato novo de reel para as vagas de ter/qui/sáb, ao lado do COMO FUNCIONA. Mecânica diferente:
em vez de assistir a um mecanismo, o espectador DÁ UM PALPITE antes da resposta, em DUAS rodadas e
um BÔNUS.

O DESENHO DOS PÉS (v4). Até a v3 os cartões mostravam pegadas molhadas no piso, e a única diferença
entre o pé chato e o pé com arco era a curva da borda de dentro: no celular, os dois leitores às
cegas acharam as pegadas "parecidas demais", e na rodada 2 ninguém via que um pé do B era diferente
do outro. Agora cada pé é a SOLA do pé de criança, em pele, com TINTA AZUL só na parte que encosta
no chão (o contorno do contato é a mesma `sola(k)` de antes):
  * pé chato  -> a sola fica azul inteira (só a bordinha de pele em volta);
  * pé com arco -> no meio do pé, do lado de dentro, sobra uma área grande de PELE sem tinta: o arco.
A diferença deixa de ser uma curva fina e vira uma MANCHA DE COR (pele contra azul) e uma forma
fechada dentro do pé: aparece num relance, em miniatura, e a rodada 2 não depende de detalhe (o B
tem um pé todo azul e o outro com a mancha de pele). O arco continua o arco COMUM: no meio do pé o
contato fica com ~39% da largura do antepé (acima de 1/3; menos que isso já pareceria pé cavo,
post51). O pezinho do bônus é a mesma sola, sem tinta: o estilo é um só do começo ao fim.

  * Rodada 1 (resposta A): "Pé de bebê: chato ou com arco?" — o gancho falado é o próprio gancho da
    tela, e ele FICA na tela durante a contagem (é a pergunta do jogo). No "chato" a tinta de A
    brilha; no "arco" a área de pele (o arco) de B acende. Contagem de 2 s (anel 2-1, tique-taque,
    luz A, B, A, B que APAGA no fim), revelação em OURO com ding: "A, o pé chato!". O porquê é
    animado: as solas encolhem até o tamanho de bebê e uma escadinha de pares sobe a tela, cada par
    maior e com o arco (a área de pele) maior, "ao longo da infância". O fim é NEUTRO (onda branca
    que percorre todos os pares + reflexo).
  * Rodada 2 (resposta B): "qual dos dois merece avaliação?" — A = dois pés chatos iguais (os dois
    azuis), B = um chato (azul) e o outro com arco (com a mancha de pele). Durante a contagem a
    pergunta fica escrita no lugar da legenda (quem vê sem som sabe o que está chutando). Revelação
    PRÓPRIA: B sobe, cresce, borda laranja, thump + pop. "Um PÉ é DIFERENTE do OUTRO": no "pé" o pé
    chato do B pula e a tinta brilha; no "diferente" pula o pé com arco e a área de pele acende (e
    fica acesa); no "outro" o pé chato pula de novo. No "isso" os dois pés de A pulsam juntos, iguais
    (A é o CONTROLE), e no "merece" um selo ≠ aparece sob o par B e um = sob o par A.
  * BÔNUS ("o pé que dói também merece"): a pílula vira BÔNUS, os cartões saem e entra um cartão
    novo; no "pé" entra a sola sem tinta, no "dói" a estrela de dor (do cf_pe_virado) e no "também"
    a MESMA marca laranja da resposta B se fecha em volta dele (thump + pop): "também merece" = "a
    mesma marca do B".
A opção que não é a resposta só apaga para 45%: nunca X, nunca vermelho, nunca deboche. Sem régua,
sem número, sem medição; a fala diz "pé", e a legenda declara que o desenho só ilustra.

Por que o render é próprio (e não `cf_comum.fazer_render`): a contagem é SILÊNCIO inserido no áudio
depois do `comprimir()` (que corta qualquer pausa > 0,42 s do roteiro), a legenda karaokê muda
durante a contagem e a trilha cai para ~15% nela (o `som.mixar` não tem envelope). Âncoras das letras
são por TOKEN ('A?', 'B?', 'A,', 'B!'). Sem exatamente 2 'B?' seguidos da resposta, o render aborta.
O karaokê não mostra a 1ª pergunta: ela já está escrita no gancho (que pulsa a cada linha dita).

Peças por IMPORT: fundo, paleta, texto (cf_alongamento), comprimir/alinhar/blocos (cf_fratura_cola),
legenda + identificação CFM + cartão final (cf_comum.interface; cf_comum.legenda para a pergunta
fixa). A estrela de dor é cópia do helper do cf_pe_virado e os tons de pele são os do cf_andador
(copiados, não importados, para este vídeo não depender do hash daquelas cenas). Todo texto
desenhado está em ep["tela"], no gancho, no roteiro (karaokê) ou na interface; ≠ e = são traços.
"""
import math
import os

import numpy as np
import skia

from . import som, voz as _voz
from .base import codificar, previas as _previas
from .cf_alongamento import (BG_OUT, CX, F_BLACK, OURO, VERMELHO, W, C, clamp, e_back, e_in_back,
                             e_inout, e_out, fundo, lerp, paint, prog, texto)
from .cf_comum import interface, legenda
from .cf_fratura_cola import alinhar, comprimir, montar_blocos

# ------------------------------------------------------------------ roteiro -> tempos
ANCORAS = {
    "bebe1": ("bebê", 1), "chato1": ("chato", 1), "arco1": ("arco", 1), "chuta": ("chuta", 1),
    "a1": ("tok:A?", 1), "b1": ("tok:B?", 1), "resp1": ("tok:A,", 1), "chato2": ("chato", 2),
    "todo": ("todo", 1), "bebe2": ("bebê", 2), "tem": ("tem", 1), "arco2": ("arco", 2),
    "forma": ("forma", 1), "sozinho": ("sozinho", 1), "infancia": ("infância", 1),
    "rodada": ("agora", 1), "dificil": ("difícil", 1), "avaliacao1": ("avaliação", 1),
    "a2": ("tok:A?", 2), "b2": ("tok:B?", 2), "resp2": ("tok:B!", 1), "pe3": ("pé", 3),
    "diferente": ("diferente", 1), "outro": ("outro", 1), "isso": ("isso", 1),
    "merece2": ("merece", 2), "merece3": ("merece", 3), "avaliacao2": ("avaliação", 2),
    "bonus": ("bônus", 1), "pe4": ("pé", 4), "doi": ("dói", 1), "tambem": ("também", 1),
    "manda": ("manda", 1), "preocupa": ("preocupado", 1),
}
DESTAQUE = {"bebê", "chato", "arco", "sozinho", "infância", "difícil", "merece", "avaliação",
            "diferente", "outro", "dói", "bônus"}
CONTAGEM = 2.0                     # segundos de palpite (silêncio inserido depois de cada "B?")
RESPOSTAS = ("A!", "A,", "B!", "B,")


def ancoras_jogo(pal, mapa):
    """{chave: tempo}. 'tok:X' compara o TOKEN do roteiro (com pontuação); o resto, a palavra em
    minúscula. Âncora ausente = KeyError (vídeo dessincronizado não sai)."""
    T = {}
    for chave, (alvo, n) in mapa.items():
        c = 0
        for p in pal:
            ok = p["tok"] == alvo[4:] if alvo.startswith("tok:") else p["w"].lower() == alvo
            if ok:
                c += 1
                if c == n:
                    T[chave] = p["t"]; break
        else:
            raise KeyError(f"âncora não achada no roteiro: {alvo} #{n}")
    T["fim_fala"] = pal[-1]["t"] + pal[-1]["d"]
    T["total"] = T["fim_fala"] + 2.2
    return T


def inserir_contagens(voz, pal, dur=CONTAGEM):
    """Insere `dur` s de silêncio logo depois de cada token 'B?' (no áudio JÁ comprimido) e empurra o
    tempo das palavras seguintes. Devolve (voz, pal, [início de cada contagem no tempo final])."""
    idx = [i for i, p in enumerate(pal) if p["tok"] == "B?"]
    if len(idx) != 2:
        raise SystemExit(f"ERRO: o jogo precisa de exatamente 2 'B?' no roteiro (achei {len(idx)}).")
    for i in idx:
        if i + 1 >= len(pal) or pal[i + 1]["tok"] not in RESPOSTAS:
            raise SystemExit("ERRO: depois de cada 'B?' vem a resposta ('A!'/'A,' ou 'B!'/'B,') — roteiro fora do jogo.")
    ins = [pal[i]["t"] + pal[i]["d"] + 0.05 for i in idx]
    partes, ult = [], 0.0
    for x in ins:
        partes.append(voz[int(ult * som.SR):int(x * som.SR)]); partes.append(np.zeros(int(dur * som.SR), voz.dtype))
        ult = x
    partes.append(voz[int(ult * som.SR):])
    novas = [dict(p, t=p["t"] + dur * sum(1 for x in ins if p["t"] > x)) for p in pal]
    return np.concatenate(partes), novas, [ins[0], ins[1] + dur]


# ------------------------------------------------------------------ paleta do jogo
COR_A, COR_B = "#4FA3E0", "#F08A4B"
TINTA, TINTA_CL, TINTA_ESC = "#3D8EDB", "#72B6F0", "#2A6FB5"     # a tinta azul onde o pé encosta
FUNDO_CARTAO = "#0B1824"
PISO_1, PISO_2 = "#1D4A5E", "#12303F"
# pele: mesmos tons do cf_andador / cf_cotovelo_baba (copiados)
PELE, PELE_CL, PELE_ESC, PELE_LINHA = "#F0B49A", "#F7CDB8", "#DA987E", "#B9765E"
LUZ_ARCO = "#FFF4E8"               # o arco (a pele sem tinta) acendendo: branco quente
CART_A = (36, 392, 528, 1230)
CART_B = (552, 392, 1044, 1230)
CART_C = (290, 392, 790, 1230)     # o cartão do BÔNUS, no centro
LARGO = (36, 392, 1044, 1230)
Y_PES, H_PE = 828, 470             # par de solas no cartão: centro e altura de cada pé
Y_SELO_CMP = 1152                  # selo ≠ / = sob o par (abaixo dos calcanhares)


def _alfa(a):
    p = skia.Paint(); p.setAlphaf(clamp(a)); return p


def _rr(r, raio=30):
    return skia.RRect.MakeRectXY(skia.Rect(*r), raio, raio)


def _centro(r):
    return (r[0] + r[2]) / 2, (r[1] + r[3]) / 2


def bump(t, t0, dur=0.35):
    """0 -> 1 -> 0 em `dur` s a partir de t0 (pulso)."""
    return math.sin(math.pi * clamp((t - t0) / dur)) if t >= t0 else 0.0


def flash(t, t0, dur=0.75):
    """Acende rápido em t0 (0,12 s) e apaga devagar até t0 + dur."""
    if t < t0:
        return 0.0
    return e_out(clamp((t - t0) / 0.12)) * (1 - prog(t, t0 + 0.25, t0 + dur))


def segura(t, t0, ate, nivel=0.6):
    """Acende em t0 (pico 1), assenta em `nivel` e fica até `ate` (some em 0,3 s)."""
    if t < t0:
        return 0.0
    v = e_out(clamp((t - t0) / 0.12)) * lerp(1.0, nivel, prog(t, t0 + 0.3, t0 + 0.7))
    return v * (1 - prog(t, ate, ate + 0.3))


def balanco(t, t0, amp=1.5, dur=1.0):
    """Balanço curto (graus) que amortece: o 'qual dos dois?' de quem pergunta."""
    k = t - t0
    if k < 0 or k > dur:
        return 0.0
    return amp * math.sin(2 * math.pi * k / 0.5) * (1 - k / dur)


# ------------------------------------------------------------------ a sola do pé, com tinta onde encosta
_SOLAS = {}
_ARCOS = {}


def _L(a, b, k):
    return lerp(a[0], b[0], k), lerp(a[1], b[1], k)


def sola(k):
    """Contorno da área de CONTATO (pé ESQUERDO, dedos para cima, lado de dentro = +x). k=0: pé
    chato, contato com a sola inteira; sola(0) é também o contorno do PÉ. k=1: arco COMUM — no meio
    do pé o contato fica com ~39% da largura do antepé (acima de 1/3; menos que isso já pareceria pé
    cavo, post51). Medido em _trabalho/medir_arco.py."""
    k = round(clamp(k), 2)
    if k in _SOLAS:
        return _SOLAS[k]
    p = skia.Path()
    p.moveTo(-1, 100)
    p.cubicTo(-16, 100, -22, 89, -22, 74)                 # calcanhar (mais estreito que o antepé)
    p.cubicTo(-22, 52, -28, 22, -31, -6)                  # borda de fora (sempre apoiada)
    p.cubicTo(-34, -34, -21, -54, 1, -55)                 # antepé
    p.cubicTo(20, -56, 35, -46, 35, -26)                  # bola do dedão
    c1, c2, m = _L((36, -4), (32, -3), k), _L((31, 22), (9, 8), k), _L((28, 44), (2, 40), k)
    p.cubicTo(*c1, *c2, *m)                               # borda de dentro: o ARCO
    c1, c2 = _L((26, 60), (-2, 60), k), _L((23, 70), (15, 67), k)
    p.cubicTo(*c1, *c2, 19, 80)
    p.cubicTo(17, 94, 10, 100, -1, 100)
    p.close()
    _SOLAS[k] = p
    return p


def arco_zona(k):
    """A parte da sola que NÃO encosta no chão (o arco): o pé, sola(0), menos o contato, sola(k).
    Vazia no pé chato."""
    k = round(clamp(k), 2)
    if k not in _ARCOS:
        _ARCOS[k] = (skia.Op(sola(0), sola(k), skia.PathOp.kDifference_PathOp) or skia.Path()) if k > 0 else None
    return _ARCOS[k]


DEDOS = ((23, -72, 12.0), (8, -79.5, 8.6), (-5, -78.5, 7.6), (-16, -74, 7.0), (-26, -65, 6.2))
DEDO_DY = (6, 6, 7, 9, 11)          # quanto cada dedo desce para encostar no antepé (o mínimo, mais)
BORDA_PELE = 3.5                   # (unidades da sola) bordinha de pele em volta da tinta: ~9 px no cartão
_SH = {}


def _sh(nome):
    """Degradês (fixos, em coordenadas da sola) criados uma vez."""
    if nome not in _SH:
        if nome == "pele":
            _SH[nome] = skia.GradientShader.MakeLinear(
                [skia.Point(-34, 0), skia.Point(36, 0)],
                [C(PELE_ESC), C(PELE), C(PELE_CL), C(PELE), C(PELE_ESC)], [0.0, 0.22, 0.5, 0.78, 1.0])
        else:
            _SH[nome] = skia.GradientShader.MakeLinear(
                [skia.Point(0, -60), skia.Point(0, 100)], [C(TINTA_CL), C(TINTA), C(TINTA_ESC)], [0.0, 0.45, 1.0])
    return _SH[nome]


def pe_sola(cv, x, y, h, k, a=1.0, direita=False, ang=0.0, esc=1.0, borda=None, borda_a=0.0,
            tinta=1.0, luz_contato=0.0, luz_arco=0.0):
    """Sola de um pé de criança vista de baixo, com `h` px de altura (centro em x, y): pele, dedos
    presos ao antepé e TINTA AZUL só onde o pé encosta (`sola(k)`). `tinta`=0: só a pele (bônus).
    `luz_contato` = brilho branco sobre a tinta; `luz_arco` = a área de pele do arco acendendo;
    `borda` = contorno aceso em volta do pé (cor, força em `borda_a`)."""
    if a <= 0:
        return
    s = h / 185 * esc; u = 1.0 / s
    cv.save(); cv.translate(x, y); cv.rotate(ang); cv.scale(-s if direita else s, s); cv.translate(0, -7.5)
    pe = sola(0)
    cv.save(); cv.translate(6 * u, 18 * u)                # sombra no piso
    cv.drawPath(pe, paint("#000000", int(110 * a), blur=11 * u))
    for (dx, dy, r), o in zip(DEDOS, DEDO_DY):
        cv.drawCircle(dx, dy + o, r * 1.15, paint("#000000", int(90 * a), blur=8 * u))
    cv.restore()
    for (dx, dy, r), o in zip(DEDOS, DEDO_DY):           # dedos ATRÁS do antepé: presos ao pé
        cv.drawCircle(dx, dy + o, r * 1.15, paint(PELE, int(255 * a), shader=_sh("pele")))
        cv.drawCircle(dx, dy + o, r * 1.15, paint(PELE_LINHA, int(230 * a), "stroke", 3 * u))
        cv.drawOval(skia.Rect(dx - r * 0.55, dy + o - r * 0.75, dx + r * 0.3, dy + o - r * 0.15),
                    paint("#FFFFFF", int(60 * a)))
    cv.drawPath(pe, paint(PELE, int(255 * a), shader=_sh("pele")))
    if tinta < 1:                                         # sem tinta (bônus): almofadas da bola do pé e do calcanhar
        ap = a * (1 - clamp(tinta))
        cv.drawOval(skia.Rect(-25, -48, 30, -18), paint(PELE_CL, int(200 * ap), blur=5 * u))
        cv.drawOval(skia.Rect(-19, 60, 13, 95), paint(PELE_CL, int(200 * ap), blur=5 * u))
    at = a * clamp(tinta)
    if at > 0:
        cv.save(); cv.clipPath(pe, skia.ClipOp.kIntersect, True)
        cv.drawPath(sola(k), paint(TINTA, int(255 * at), shader=_sh("tinta")))
        if luz_contato > 0:                               # brilho: borda clara + véu leve (a tinta continua azul)
            cv.drawPath(sola(k), paint("#FFFFFF", int(70 * at * clamp(luz_contato))))
            cv.drawPath(sola(k), paint("#FFFFFF", int(200 * at * clamp(luz_contato)), "stroke", 5 * u, blur=3 * u))
        cv.drawPath(pe, paint(PELE, int(255 * a), "stroke", 2 * BORDA_PELE, shader=_sh("pele")))   # bordinha de pele
        cv.restore()
        for (dx, dy, r), o in zip(DEDOS, DEDO_DY):       # ponta dos dedos com tinta
            cv.drawCircle(dx, dy + o - 3, r * 0.74, paint(TINTA, int(255 * at)))
            if luz_contato > 0:
                cv.drawCircle(dx, dy + o - 3, r * 0.74, paint("#FFFFFF", int(70 * at * clamp(luz_contato))))
        cv.drawOval(skia.Rect(-15, 70, -3, 82), paint("#FFFFFF", int(85 * at)))        # brilho da tinta
        cv.drawOval(skia.Rect(-16, -42, 2, -33), paint("#FFFFFF", int(75 * at)))
    zona = arco_zona(k)
    if zona is not None and luz_arco > 0:                 # o arco (pele sem tinta) acende
        la = clamp(luz_arco)
        cv.save(); cv.clipPath(pe, skia.ClipOp.kIntersect, True)
        cv.drawPath(zona, paint(LUZ_ARCO, int(150 * a * la), blur=9 * u))
        cv.drawPath(zona, paint(LUZ_ARCO, int(170 * a * la)))
        cv.restore()
    cv.drawPath(pe, paint(PELE_LINHA, int(235 * a), "stroke", 3.2 * u))
    if borda and borda_a > 0:
        cv.drawPath(pe, paint(borda, int(120 * a * borda_a), "stroke", 16 * u, blur=7 * u))
        cv.drawPath(pe, paint(borda, int(255 * a * borda_a), "stroke", 6 * u))
    cv.restore()


def par(cx, cy, h, kE, kD, **kw):
    """Par de solas (esquerda/direita, dedão para o meio, ponta levemente para fora)."""
    return [dict(x=cx - 0.23 * h, y=cy, h=h, k=kE, direita=False, ang=-5, **kw),
            dict(x=cx + 0.23 * h, y=cy, h=h, k=kD, direita=True, ang=5, **kw)]


# ------------------------------------------------------------------ cartão A | B
def piso(cv, r):
    x0, y0, x1, y1 = r
    cv.drawRect(skia.Rect(*r), paint(PISO_1, shader=skia.GradientShader.MakeLinear(
        [skia.Point(x0, y0), skia.Point(x1, y1)], [C(PISO_1), C(PISO_2)])))
    lado = 98.4
    i = 0; x = 36.0
    while x < x1:
        j = 0; y = 392.0
        while y < y1:
            if (i + j) % 2 and x + lado > x0 and y + lado > y0:
                cv.drawRect(skia.Rect(x, y, x + lado, y + lado), paint("#FFFFFF", 9))
            y += lado; j += 1
        x += lado; i += 1
    x = 36.0
    while x < x1:
        if x > x0:
            cv.drawLine(x, y0, x, y1, paint("#A9D3E6", 40, "stroke", 1.5))
        x += lado
    y = 392.0
    while y < y1:
        if y > y0:
            cv.drawLine(x0, y, x1, y, paint("#A9D3E6", 40, "stroke", 1.5))
        y += lado


_BASES = {}


def _desenha_base(cv, r):
    cv.drawRRect(_rr((r[0], r[1] + 12, r[2], r[3] + 12)), paint("#000000", 110, blur=20))
    cv.save(); cv.clipRRect(_rr(r), skia.ClipOp.kIntersect, True)
    piso(cv, r)
    cv.restore()


def base_cartao(cv, r):
    """Sombra + piso do cartão. Nos retângulos fixos (A, B, C, piso largo) vem de uma imagem pronta:
    o desenho é o mesmo, sem refazer degradê, ladrilho e sombra borrada em todo quadro."""
    if r not in (CART_A, CART_B, CART_C, LARGO):
        _desenha_base(cv, r); return
    if r not in _BASES:
        m = 60
        surf = skia.Surface(int(r[2] - r[0] + 2 * m), int(r[3] - r[1] + 2 * m))
        c = surf.getCanvas(); c.clear(skia.ColorTRANSPARENT); c.translate(m - r[0], m - r[1])
        _desenha_base(c, r)
        _BASES[r] = (surf.makeImageSnapshot(), r[0] - m, r[1] - m)
    img, x, y = _BASES[r]
    cv.drawImage(img, x, y)


def selo_letra(cv, letra, x, y, cor, esc=1.0, a=1.0, badge_esc=1.0):
    if a <= 0:
        return
    r = 44 * badge_esc
    x, y = x + r - 44, y + r - 44                         # o selo cresce para dentro do cartão
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    cv.drawCircle(0, 5, r, paint("#000000", int(90 * a), blur=8))
    cv.drawCircle(0, 0, r, paint(cor, int(255 * a)))
    cv.drawCircle(0, 0, r - 3, paint("#FFFFFF", int(70 * a), "stroke", 3))
    tam = 64 * badge_esc
    texto(cv, letra, 0, tam * 0.355, F_BLACK, tam, FUNDO_CARTAO, int(255 * a))
    cv.restore()


def selo_comparacao(cv, x, y, igual, a, esc):
    """Selo '=' (os dois pés iguais) ou '≠' (um diferente do outro), desenhado com TRAÇOS (não é
    texto): círculo escuro do jogo, sinal branco."""
    if a <= 0 or esc <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    cv.drawCircle(0, 7, 54, paint("#000000", int(110 * a), blur=9))
    cv.drawCircle(0, 0, 52, paint(FUNDO_CARTAO, int(240 * a)))
    cv.drawCircle(0, 0, 52, paint("#FFFFFF", int(150 * a), "stroke", 3))
    for dy in (-11, 11):
        cv.drawLine(-24, dy, 24, dy, paint("#FFFFFF", int(255 * a), "stroke", 9))
    if not igual:
        cv.drawLine(12, -29, -12, 29, paint("#FFFFFF", int(255 * a), "stroke", 9))
    cv.restore()


def cartao(cv, t, r, letra, cor, pes, alfa=1.0, dx=0.0, dy=0.0, rot=0.0, esc=1.0, pulso=0.0,
           acende=0.0, luz=0.0, marca=None, marca_a=0.0, reflexo=-1.0, badge_esc=1.0, extra=None,
           por_cima=None):
    """Cartão com piso de ladrilho, solas e o selo da letra (`letra=None`: sem selo). `luz` = luz
    da contagem (branca); `marca` = marcador da revelação (OURO na rodada 1; a cor do B na rodada 2
    e no bônus). `extra(cv)` desenha dentro do cartão (recortado); `por_cima(cv)`, depois da borda."""
    if alfa <= 0:
        return
    cx, cy = _centro(r)
    cv.saveLayer(None, _alfa(alfa)) if alfa < 1 else cv.save()
    cv.translate(dx, dy)
    cv.translate(cx, cy); cv.rotate(rot); cv.scale(esc, esc); cv.translate(-cx, -cy)
    rr = _rr(r)
    base_cartao(cv, r)
    cv.save(); cv.clipRRect(rr, skia.ClipOp.kIntersect, True)
    for p in pes:
        pe_sola(cv, p["x"], p["y"], p["h"], p["k"], p.get("a", 1.0), p["direita"], p["ang"], p.get("esc", 1.0),
                p.get("borda"), p.get("borda_a", 0.0), p.get("tinta", 1.0), p.get("luz_contato", 0.0),
                p.get("luz_arco", 0.0))
    if 0 <= reflexo < 1:                                  # reflexo de luz atravessando o piso
        xr = lerp(r[0] - 260, r[2] + 260, e_inout(reflexo))
        cv.save(); cv.translate(xr, cy); cv.rotate(-22)
        cv.drawRect(skia.Rect(-55, -900, 55, 900), paint("#FFFFFF", int(46 * math.sin(math.pi * reflexo)), blur=18))
        cv.restore()
    if extra:
        extra(cv)
    cv.restore()
    cv.drawRRect(rr, paint(cor, 255, "stroke", 3))
    if acende > 0:
        cv.drawRRect(rr, paint("#FFFFFF", int(200 * clamp(acende)), "stroke", 5))
    if luz > 0:
        cv.drawRRect(rr, paint("#FFFFFF", int(150 * luz), "stroke", 26, blur=14))
        cv.drawRRect(rr, paint("#FFFFFF", int(255 * luz), "stroke", 8))
    if marca and marca_a > 0:
        cv.drawRRect(rr, paint(marca, int(170 * marca_a), "stroke", 30, blur=16))
        cv.drawRRect(rr, paint(marca, int(255 * marca_a), "stroke", 9))
    if por_cima:
        por_cima(cv)
    if letra:
        selo_letra(cv, letra, r[0] + 62, r[1] + 62, cor, 1.0 + 0.35 * pulso, 1.0, badge_esc)
    cv.restore()


# ------------------------------------------------------------------ contagem e luz
def em_contagem(t, T, rodada=None):
    r1 = T["cont1"] <= t < T["resp1"] - 0.12
    r2 = T["cont2"] <= t < T["resp2"] - 0.12
    return r1 if rodada == 1 else r2 if rodada == 2 else (r1 or r2)


def luz_de(t, T, letra):
    """Luz da contagem: alterna a cada 0,5 s (ritmo constante de relógio) e APAGA nos últimos 0,2 s.
    Rodada 1: A, B, A, B; rodada 2: B, A, B, A — nas duas a luz termina na opção que NÃO é a
    resposta, e a revelação nunca se confunde com a luz que parou."""
    for i, t0 in enumerate((T["cont1"], T["cont2"])):
        k = t - t0
        if 0 <= k < CONTAGEM:
            fase = int(k / 0.5)
            ordem = ("A", "B") if i == 0 else ("B", "A")
            if ordem[fase % 2] != letra:
                return 0.0
            return clamp((k - fase * 0.5) / 0.05) * (1 - prog(k, CONTAGEM - 0.2, CONTAGEM - 0.05))
    return 0.0


def anel_contagem(cv, t, t0, x=540, y=811, r=90):
    k = t - t0
    if k < -0.05 or k > CONTAGEM + 0.22:
        return
    ent = e_back(clamp((k + 0.05) / 0.25))
    sai = clamp((k - CONTAGEM) / 0.22)
    esc = ent * lerp(1.0, 1.35, e_out(sai)); a = clamp((k + 0.05) / 0.08) * (1 - sai)
    cv.saveLayer(None, _alfa(a)) if a < 1 else cv.save()
    cv.translate(x, y); cv.scale(esc, esc)
    cv.drawCircle(0, 8, r + 6, paint("#000000", 120, blur=12))
    cv.drawCircle(0, 0, r, paint(FUNDO_CARTAO, 245))
    cv.drawCircle(0, 0, r - 12, paint("#FFFFFF", 38, "stroke", 12))
    resto = 1 - clamp(k / CONTAGEM)
    if resto > 0:
        cv.drawArc(skia.Rect(-(r - 12), -(r - 12), r - 12, r - 12), -90, 360 * resto, False, paint(OURO, 255, "stroke", 12))
    n = "2" if k < 1.0 else "1"
    pop = 1 + 0.25 * (1 - e_out(clamp((k - (0 if k < 1.0 else 1.0)) / 0.15)))
    cv.save(); cv.scale(pop, pop)
    texto(cv, n, 0, 44, F_BLACK, 120, "#FFFFFF", 255, contorno=0)
    cv.restore()
    cv.restore()


# ------------------------------------------------------------------ BÔNUS: sola sem tinta + estrela
def estrela_dor(cv, x, y, r, a):
    """Cópia do helper do cf_pe_virado (aprovado)."""
    if a <= 0:
        return
    p = skia.Path(); n = 9
    for i in range(2 * n):
        ang = -math.pi / 2 + i * math.pi / n
        rr = (r if i % 4 == 0 else r * 0.84) if i % 2 == 0 else r * 0.46
        (p.moveTo if i == 0 else p.lineTo)(x + rr * math.cos(ang), y + rr * math.sin(ang))
    p.close()
    cv.drawPath(p, paint(VERMELHO, int(120 * a), blur=12))
    cv.drawPath(p, paint(VERMELHO, int(255 * a)))
    cv.drawPath(p, paint("#FFD3D4", int(200 * a), "stroke", 2.5))


def saida_final(t, T):
    """0 -> 1 ANTES de o cartão final entrar (T['manda'] - 0,15): nada sob a CTA."""
    return prog(t, T["manda"] - 0.55, T["manda"] - 0.18)


def bonus(cv, t, T):
    """No 'Bônus': entra o cartão C (mesmo piso do jogo, sem letra). No 'pé', a sola (a mesma do
    jogo, sem tinta) pisa nele; no 'dói', a estrela de dor; no 'também', a MESMA marca laranja da
    resposta B se fecha em volta."""
    ent = prog(t, T["bonus"] + 0.18, T["bonus"] + 0.55)          # entra quando A e B já saíram
    if ent <= 0:
        return
    a = clamp(ent * 2.5) * (1 - saida_final(t, T))
    if a <= 0:
        return
    e = e_back(ent)
    fecha = prog(t, T["tambem"] - 0.05, T["tambem"] + 0.2)
    cx, cy = _centro(CART_C)

    def extra(cv):
        pe = prog(t, T["pe4"] - 0.15, T["pe4"] + 0.25)
        if pe <= 0:
            return
        h = 590
        rot = -8 + balanco(t, T["doi"], amp=2.5, dur=0.8)
        ep = e_back(pe)
        cv.save(); cv.translate(cx, Y_PES - 14); cv.rotate(rot); cv.scale(ep, ep)
        pe_sola(cv, 0, 0, h, 0, clamp(pe * 3), tinta=0.0)
        k = t - (T["doi"] - 0.05)
        if k > 0:
            s = h / 185
            r = 64 * e_back(clamp(k / 0.3)) * (0.88 + 0.12 * math.cos(k * 11))
            estrela_dor(cv, 7 * s, (36 - 7.5) * s, r, clamp(k / 0.08))
        cv.restore()

    esc = lerp(0.82, 1.0, e) * (1 + 0.035 * bump(t, T["tambem"], 0.35) + 0.03 * bump(t, T["merece3"], 0.4))
    cartao(cv, t, CART_C, None, "#FFFFFF", [], alfa=a, esc=esc, dy=40 * (1 - e),
           marca=COR_B, marca_a=fecha, acende=bump(t, T["bonus"] + 0.3, 0.4) + bump(t, T["merece3"], 0.4), extra=extra)
    if 0 < fecha < 1:                                     # a marca FECHA: um contorno que encolhe até a borda
        g = lerp(1.14, 1.0, e_out(fecha))
        cv.save(); cv.translate(cx, cy); cv.scale(g, g); cv.translate(-cx, -cy)
        cv.drawRRect(_rr(CART_C), paint(COR_B, int(220 * a * (1 - fecha)), "stroke", 9))
        cv.restore()


# ------------------------------------------------------------------ brilhos da revelação 1
def brilhos_borda(cv, r, t, t0, n=20, dur=0.85):
    """Estrelinhas douradas saindo da borda do cartão (a revelação comemora sem cobrir os pés)."""
    k = t - t0
    if k < 0 or k > dur:
        return
    x0, y0, x1, y1 = r; lw, lh = x1 - x0, y1 - y0; per = 2 * (lw + lh)
    for i in range(n):
        d = (i + 0.5) / n * per
        if d < lw:
            px, py, nx, ny = x0 + d, y0, 0, -1
        elif d < lw + lh:
            px, py, nx, ny = x1, y0 + d - lw, 1, 0
        elif d < 2 * lw + lh:
            px, py, nx, ny = x1 - (d - lw - lh), y1, 0, 1
        else:
            px, py, nx, ny = x0, y1 - (d - 2 * lw - lh), -1, 0
        off = 40 * e_out(k / dur) * (0.6 + 0.4 * ((i * 37) % 10) / 10)
        x, y = px + nx * off, py + ny * off
        sz = 11 * (1 - k / dur) + 3; a = int(255 * (1 - k / dur))
        p = skia.Path(); p.moveTo(x, y - sz * 2); p.lineTo(x + sz * 0.5, y - sz * 0.5); p.lineTo(x + sz * 2, y)
        p.lineTo(x + sz * 0.5, y + sz * 0.5); p.lineTo(x, y + sz * 2); p.lineTo(x - sz * 0.5, y + sz * 0.5)
        p.lineTo(x - sz * 2, y); p.lineTo(x - sz * 0.5, y - sz * 0.5); p.close()
        cv.drawPath(p, paint(OURO, a))


# ------------------------------------------------------------------ rodada 1
BEBE = (540, 870, 230)             # o par de bebê no meio do piso, antes de virar o 1º degrau da escadinha
TRILHA = ((150, 1112, 160, 0.0), (345, 995, 218, 0.35), (582, 840, 282, 0.7), (856, 624, 340, 1.0))


def rodada1(cv, t, T):
    sai = e_inout(prog(t, T["rodada"], T["rodada"] + 0.6))
    if sai >= 1:
        return
    dx_all = -1120 * sai
    luz_a, luz_b = luz_de(t, T, "A"), luz_de(t, T, "B")
    carimbo = lambda t0: 1 + 0.12 * bump(t, t0, 0.28)    # noqa: E731  re-pop do quadro 0
    puls_peg = 1 + 0.05 * bump(t, T["bebe1"], 0.35)
    refl = prog(t, T["bebe1"], T["bebe1"] + 0.8) if T["bebe1"] <= t < T["bebe1"] + 0.8 else -1.0

    # ---- B: no "arco" (e no "B?") a área de pele do arco acende; sai pela direita no "todo"
    sai_b = e_in_back(prog(t, T["todo"], T["todo"] + 0.45))
    if sai_b < 1:
        bx, _ = _centro(CART_B)
        pb = puls_peg * (1 + 0.07 * bump(t, T["arco1"], 0.4)) * carimbo(0.40)
        la = max(flash(t, T["arco1"] - 0.05, 0.9), flash(t, T["b1"] - 0.05))
        pes = [dict(p, esc=pb, luz_arco=la) for p in par(bx, Y_PES, H_PE, 1, 1)]
        cartao(cv, t, CART_B, "B", COR_B, pes, alfa=1 - 0.55 * prog(t, T["resp1"], T["resp1"] + 0.25),
               dx=dx_all + 760 * sai_b, rot=balanco(t, T["chuta"] + 0.14),
               pulso=bump(t, T["arco1"]) + bump(t, T["b1"]) + 0.12 * luz_b,
               acende=bump(t, T["arco1"], 0.45) + bump(t, T["b1"], 0.45), luz=luz_b, reflexo=refl)

    # ---- A: no "chato" a tinta (a sola inteira) brilha; vira a resposta, cresce e vira o piso da escadinha
    expande = e_inout(prog(t, T["todo"], T["todo"] + 0.5))
    r = tuple(lerp(a, b, expande) for a, b in zip(CART_A, LARGO)) if 0 < expande < 1 else (CART_A if expande <= 0 else LARGO)
    ax, _ = _centro(CART_A)
    k_bebe = e_inout(prog(t, T["bebe2"], T["bebe2"] + 0.5))
    k_trilha = e_inout(prog(t, T["arco2"] - 0.1, T["arco2"] + 0.3))
    x0, y0, h0 = (lerp(lerp(a, b, k_bebe), c, k_trilha) for a, b, c in zip((ax, Y_PES, H_PE), BEBE, TRILHA[0][:3]))
    onda = lambda i: 0.8 * bump(t, T["infancia"] + 0.25 + 0.09 * i, 0.45)   # noqa: E731  fim NEUTRO
    pa = puls_peg * (1 + 0.07 * bump(t, T["chato1"], 0.4)) * carimbo(0.30)
    lc = max(flash(t, T["chato1"] - 0.05, 0.9), flash(t, T["a1"] - 0.05),
             flash(t, T["chato2"] - 0.05, 0.9)) * (1 - expande)            # "A, o pé CHATO!": a tinta de novo
    pes = [dict(p, esc=pa, borda="#FFFFFF", borda_a=max(bump(t, T["tem"], 0.6), onda(0)), luz_contato=lc)
           for p in par(x0, y0, h0, 0, 0)]
    for i, t0 in ((1, T["forma"]), (2, T["sozinho"]), (3, T["infancia"])):
        if t >= t0:
            x, y, h, k = TRILHA[i]
            dd = dict(esc=1 + 0.18 * (1 - e_out(clamp((t - t0) / 0.22))), a=clamp((t - t0) / 0.1),
                      borda="#FFFFFF", borda_a=onda(i), luz_arco=flash(t, t0 + 0.05, 0.9))
            pes += par(x, y, h, k, k, **dd)
    marca_a = prog(t, T["resp1"], T["resp1"] + 0.12) * (1 - prog(t, T["todo"], T["todo"] + 0.4))
    refl_fim = prog(t, T["infancia"] + 0.2, T["infancia"] + 1.1) if T["infancia"] + 0.2 <= t < T["infancia"] + 1.1 else -1.0
    cartao(cv, t, r, "A", COR_A, pes, dx=dx_all, rot=balanco(t, T["chuta"]) * (1 - expande),
           pulso=bump(t, T["chato1"]) + bump(t, T["a1"]) + 0.12 * luz_a + bump(t, T["resp1"], 0.45),
           acende=bump(t, T["chato1"], 0.45) + bump(t, T["a1"], 0.45),
           luz=luz_a, marca=OURO, marca_a=marca_a, reflexo=refl if refl >= 0 else refl_fim)
    brilhos_borda(cv, tuple(v + (dx_all if i % 2 == 0 else 0) for i, v in enumerate(CART_A)), t, T["resp1"] + 0.03)


# ------------------------------------------------------------------ rodada 2
def pes_rodada2(cx, letra, t, T):
    """O par de cada cartão na rodada 2. A: dois pés chatos (os dois azuis). B: o esquerdo chato, o
    direito com arco (a mancha de pele). 'Um PÉ é DIFERENTE do OUTRO': no 'pé' o chato do B pula e a
    tinta brilha; no 'diferente' pula o pé com arco e o arco acende (e fica aceso até o bônus); no
    'outro' o chato pula de novo. No 'isso' os dois pés de A pulsam JUNTOS, iguais: A é o controle."""
    if letra == "A":
        pul = 1 + 0.06 * bump(t, T["isso"], 0.45)
        lc = max(flash(t, T["a2"] - 0.05), 0.8 * flash(t, T["isso"] - 0.05, 0.6))
        return [dict(p, esc=pul, luz_contato=lc) for p in par(cx, Y_PES, H_PE, 0, 0)]
    pe_e, pe_d = par(cx, Y_PES, H_PE, 0, 1)
    pe_e = dict(pe_e, esc=1 + 0.10 * (bump(t, T["pe3"], 0.4) + bump(t, T["outro"], 0.4)),
                luz_contato=max(flash(t, T["pe3"] - 0.05), flash(t, T["outro"] - 0.05)))
    pe_d = dict(pe_d, esc=1 + 0.10 * bump(t, T["diferente"], 0.45),
                luz_arco=max(flash(t, T["b2"] - 0.05), segura(t, T["diferente"] - 0.05, T["bonus"] - 0.1)))
    return [pe_e, pe_d]


def rodada2(cv, t, T):
    if t < T["rodada"] + 0.05:
        return
    sai = e_inout(prog(t, T["bonus"] - 0.05, T["bonus"] + 0.3))
    if sai < 1:
        lift = e_back(prog(t, T["resp2"], T["resp2"] + 0.3)) if t >= T["resp2"] else 0.0
        cmp = prog(t, T["merece2"] - 0.08, T["merece2"] + 0.22)          # selo ≠ / = no "merece"
        for i, (r, letra, cor) in enumerate(((CART_A, "A", COR_A), (CART_B, "B", COR_B))):
            ent = e_inout(prog(t, T["rodada"] + 0.05 * i, T["rodada"] + 0.6 + 0.05 * i))   # mesmo passo do piso que sai
            cx, _ = _centro(r)
            t_l = T["a2"] if letra == "A" else T["b2"]
            luz = luz_de(t, T, letra)
            pes = pes_rodada2(cx, letra, t, T)
            comum = dict(dx=(1 - ent) * 1120, rot=balanco(t, T["dificil"] + 0.1 * i, amp=3.0, dur=0.7)
                         + balanco(t, T["avaliacao1"] + 0.14 * i), acende=bump(t, t_l, 0.45), luz=luz)
            selo = (lambda cv, cx=cx, ig=(letra == "A"): selo_comparacao(cv, cx, Y_SELO_CMP, ig, clamp(cmp * 3),
                                                                        e_back(cmp)))
            if letra == "A":                              # não é a resposta: só apaga (e fica apagado)
                apaga = 0.55 * prog(t, T["resp2"], T["resp2"] + 0.25)
                cartao(cv, t, r, letra, cor, pes, alfa=(1 - apaga) * (1 - sai),
                       esc=(1 - 0.03 * lift) * (1 - 0.15 * sai), pulso=bump(t, t_l) + 0.12 * luz,
                       por_cima=selo, **comum)
            else:                                         # a resposta: sobe, cresce, borda da cor do B
                cartao(cv, t, r, letra, cor, pes, alfa=1 - sai, dy=-7 * lift,
                       esc=(1 + 0.025 * lift) * (1 - 0.15 * sai) * (1 + 0.03 * bump(t, T["avaliacao2"], 0.4)),
                       pulso=bump(t, t_l) + 0.12 * luz + 0.5 * bump(t, T["resp2"], 0.35) + 0.5 * bump(t, T["avaliacao2"], 0.4),
                       marca=COR_B, marca_a=prog(t, T["resp2"], T["resp2"] + 0.12), badge_esc=1 + 0.3 * lift,
                       por_cima=selo, **comum)
    bonus(cv, t, T)


# ------------------------------------------------------------------ topo: gancho, selo da série, rodada
def capa_jogo(cv, t, T, l1, l2):
    """Gancho de 2 linhas (como cf_comum.capa), cada linha pulsa quando é dita ('bebê' / 'chato').
    FICA durante a contagem (é a pergunta) e sai para CIMA na resposta, antes de o selo entrar."""
    sai = e_inout(prog(t, T["resp1"], T["resp1"] + 0.3))
    if sai >= 1:
        return
    a = 1 - sai
    cv.drawRect(skia.Rect(0, 0, W, 360), paint(BG_OUT, 255, shader=skia.GradientShader.MakeLinear(
        [skia.Point(0, 0), skia.Point(0, 360)], [C(BG_OUT, int(235 * a)), C(BG_OUT, 0)])))
    pulso = 1 + 0.025 * math.sin(t * 5)
    cv.save(); cv.translate(CX, 205 - 170 * sai); cv.scale(pulso, pulso)
    for y, s, cor, t0 in ((0, l1, "#FFFFFF", T["bebe1"]), (88, l2, OURO, T["chato1"])):
        e = 1 + 0.06 * bump(t, t0, 0.35)
        cv.save(); cv.translate(0, y - 28); cv.scale(e, e)
        texto(cv, s, 0, 28, F_BLACK, 78, cor, int(255 * a), contorno=10)
        cv.restore()
    cv.restore()


def selo_serie(cv, a):
    if a <= 0:
        return
    rr = skia.RRect.MakeRectXY(skia.Rect(CX - 190, 150, CX + 190, 204), 27, 27)
    cv.drawRRect(rr, paint("#FFFFFF", int(28 * a)))
    texto(cv, "QUAL DOS DOIS?", CX, 190, F_BLACK, 32, OURO, int(255 * a))


def pilula(cv, t, T):
    """'2 RODADAS' na capa; 'RODADA 1' / 'RODADA 2' com bolinhas de placar; 'BÔNUS' no fim."""
    a = 1 - saida_final(t, T)
    if a <= 0:
        return
    if t < T["cont1"]:
        s, n, t0 = "2 RODADAS", 0, 0.05
    elif t < T["rodada"]:
        s, n, t0 = "RODADA 1", 1, T["cont1"]
    elif t < T["bonus"]:
        s, n, t0 = "RODADA 2", 2, T["rodada"]
    else:
        s, n, t0 = "BÔNUS", 2, T["bonus"]
    esc = 1 + 0.15 * bump(t, t0, 0.3) + 0.18 * bump(t, T["dificil"], 0.35)
    tam = 32; lw = skia.Font(F_BLACK, tam).measureText(s)
    larg = lw + 36 + 18 + 2 * 22
    cv.save(); cv.translate(CX, 346); cv.scale(esc, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-larg / 2, -24, larg / 2, 24), 24, 24)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(225 * a)))
    cv.drawRRect(rr, paint(OURO, int(200 * a), "stroke", 2.5))
    texto(cv, s, -larg / 2 + 18, 11, F_BLACK, tam, "#FFFFFF", int(255 * a), centro=False)
    for k in range(2):
        x = -larg / 2 + 18 + lw + 18 + 11 + 22 * k
        if n > k:
            cv.drawCircle(x, 0, 8, paint(OURO, int(255 * a)))
        else:
            cv.drawCircle(x, 0, 7, paint("#FFFFFF", int(170 * a), "stroke", 2.5))
    cv.restore()


# ------------------------------------------------------------------ CTA: os dois cartões em miniatura
def minis(cv, t, T):
    k = prog(t, T["manda"] + 0.05, T["manda"] + 0.45)
    if k <= 0:
        return
    e = e_back(k)
    for i, (r, letra, cor, x) in enumerate(((CART_A, "A", COR_A, 458), (CART_B, "B", COR_B, 622))):
        cx, cy = _centro(r)
        rot = balanco(t, T["preocupa"] + 0.13 * i, amp=4.0, dur=0.9)
        cv.save(); cv.translate(x, 368); cv.rotate(rot); cv.scale(0.28 * e, 0.28 * e); cv.translate(-cx, -cy)
        cartao(cv, t, r, letra, cor, par(cx, Y_PES, H_PE, 0, 0 if letra == "A" else 1), alfa=clamp(k * 3),
               badge_esc=1.75)
        cv.restore()


# ------------------------------------------------------------------ quadro
def pergunta_fixa(blocos, T):
    """O bloco da pergunta da rodada 2 ('QUAL DOS DOIS / MERECE AVALIAÇÃO?'), esticado para ficar na
    tela durante a contagem (quem vê sem som sabe o que está chutando)."""
    for b in blocos:
        if any(abs(p["t"] - T["avaliacao1"]) < 1e-6 for p in b):
            ult = dict(b[-1], d=max(b[-1]["d"], T["resp2"] - b[-1]["t"]))
            return b[:-1] + [ult]
    raise SystemExit("ERRO: bloco da pergunta da rodada 2 não achado.")


def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    rodada1(cv, t, T)
    rodada2(cv, t, T)
    anel_contagem(cv, t, T["cont1"])
    anel_contagem(cv, t, T["cont2"])
    capa_jogo(cv, t, T, ep["gancho"][0], ep["gancho"][1])
    selo_serie(cv, prog(t, T["resp1"] + 0.35, T["resp1"] + 0.7) * (1 - saida_final(t, T)))
    pilula(cv, t, T)
    # karaokê: a 1ª pergunta já é o gancho escrito (não duplica); na contagem 1 o gancho fica (é a
    # pergunta); na contagem 2 a pergunta da rodada fica escrita no lugar da legenda
    kara = [] if em_contagem(t, T) else [b for b in blocos if b[-1]["t"] >= T["chuta"] - 0.05]
    interface(cv, t, T, kara, DESTAQUE)
    if em_contagem(t, T, 2):
        a = prog(t, T["cont2"], T["cont2"] + 0.2)
        cv.saveLayer(None, _alfa(a)) if a < 1 else cv.save()
        legenda(cv, [T["_pergunta2"]], t, DESTAQUE)
        cv.restore()
    minis(cv, t, T)


# ------------------------------------------------------------------ som
def sons(T):
    ev = [(0.05, "pop", 0.5), (0.30, "pop", 0.45), (0.40, "pop", 0.4),
          (T["bebe1"], "shimmer", 0.3), (T["chato1"], "pop", 0.55), (T["arco1"], "pop", 0.55),
          (T["arco1"] + 0.03, "shimmer", 0.2),
          (T["chuta"], "whoosh", 0.25), (T["a1"], "pop", 0.6), (T["b1"], "pop", 0.6)]
    for t0 in (T["cont1"], T["cont2"]):                          # tique-taque constante
        ev += [(t0 + 0.5 * i, "tick" if i % 2 == 0 else "click", 0.75 if i % 2 == 0 else 1.0) for i in range(4)]
    ev += [(T["resp1"], "ding", 0.45), (T["chato2"], "pop", 0.35), (T["todo"], "whoosh", 0.4),
           (T["bebe2"], "pop", 0.6), (T["tem"], "shimmer", 0.25), (T["arco2"], "whoosh", 0.25),
           (T["forma"], "pop", 0.6), (T["sozinho"], "pop", 0.6), (T["infancia"], "pop", 0.6),
           (T["infancia"] + 0.25, "shimmer", 0.5),
           (T["rodada"], "whoosh", 0.5), (T["rodada"] + 0.05, "pop", 0.4), (T["rodada"] + 0.55, "thump", 0.4),
           (T["dificil"], "pop", 0.45), (T["a2"], "pop", 0.6), (T["b2"], "pop", 0.6),
           (T["resp2"], "thump", 0.65), (T["resp2"] + 0.02, "pop", 0.5),
           (T["pe3"], "pop", 0.45), (T["diferente"], "pop", 0.55), (T["diferente"] + 0.03, "shimmer", 0.3),
           (T["outro"], "pop", 0.45),
           (T["isso"], "pop", 0.4), (T["merece2"] - 0.05, "pop", 0.55),
           (T["bonus"] - 0.05, "whoosh", 0.35), (T["bonus"] + 0.2, "pop", 0.45), (T["pe4"], "pop", 0.55),
           (T["doi"], "tick", 0.6), (T["tambem"], "thump", 0.6), (T["tambem"] + 0.02, "pop", 0.5), (T["merece3"], "shimmer", 0.3),
           (T["manda"] + 0.05, "whoosh", 0.5), (T["preocupa"], "pop", 0.4)]
    return ev


def janelas(T):
    return [(T["cont1"], T["cont1"] + CONTAGEM), (T["cont2"], T["cont2"] + CONTAGEM)]


def _media_movel(x, w):
    """= np.convolve(x, np.ones(w) / w, "same"), por soma acumulada (o convolve direto levou 509 s
    nesta máquina para 28 s de áudio)."""
    xp = np.concatenate([np.zeros(w // 2), x, np.zeros((w - 1) // 2)])
    c = np.concatenate([[0.0], np.cumsum(xp)])
    return (c[w:w + len(x)] - c[:len(x)]) / w


def mixar_jogo(voz, dur, eventos, jan, ganho_trilha=0.40, fundo_contagem=0.15, rampa=0.15):
    """Como som.mixar (ducking pela voz, efeitos), mais um envelope que baixa a trilha para
    ~15% nas janelas de contagem (rampa de 0,15 s): o tique-taque fica sozinho."""
    n = int(dur * som.SR)
    v = np.zeros(n); v[:min(n, len(voz))] = voz[:n]
    musica = som.trilha(dur) * ganho_trilha
    win = int(0.06 * som.SR)
    envv = np.sqrt(np.maximum(_media_movel(v ** 2, win), 0.0))
    alvo = np.where(envv > 0.02, 0.38, 1.0)
    duck = _media_movel(alvo, int(0.25 * som.SR))
    tt = np.arange(n) / som.SR
    env = np.ones(n)
    for a, b in jan:
        k = np.clip((tt - (a - rampa)) / rampa, 0, 1) * np.clip(((b + rampa) - tt) / rampa, 0, 1)
        env = np.minimum(env, 1 - (1 - fundo_contagem) * k)
    fx = np.zeros(n)
    for t0, nome, g in eventos:
        s = som.SFX[nome]()
        p = int(t0 * som.SR)
        if 0 <= p < n:
            m = min(len(s), n - p)
            fx[p:p + m] += s[:m] * g
    mix = v + musica * duck * env + fx * 0.7
    pico = np.max(np.abs(mix)) or 1.0
    return mix / pico * 0.89


# ------------------------------------------------------------------ entrada
def tempos_previa(T):
    return (0.0, T["arco1"] + 0.3, T["cont1"] + 1.2, T["resp1"] + 0.5, T["bebe2"] + 0.45,
            T["infancia"] + 0.45, T["rodada"] + 0.7, T["cont2"] + 1.7, T["resp2"] + 0.3,
            T["diferente"] + 0.25, T["outro"] + 0.3, T["merece2"] + 0.4, T["doi"] + 0.3, T["tambem"] + 0.3,
            T["manda"] + 0.8, T["total"] - 0.1)


def preparar(ep, tmp):
    roteiro = "\n".join(ep["roteiro"])
    voz_bruta, palavras = _voz.narrar(roteiro, _voz.RITMO_COMO_FUNCIONA, os.path.join(tmp, "voz"))
    voz_c, pal, tirado = comprimir(voz_bruta, palavras, respiro_cta=0.6)
    pal = alinhar(pal, roteiro)
    voz_c, pal, conts = inserir_contagens(voz_c, pal)
    T = ancoras_jogo(pal, ANCORAS)
    T["cont1"], T["cont2"] = conts
    if not (T["chuta"] < T["cont1"] < T["resp1"] < T["rodada"] < T["cont2"] < T["resp2"] < T["pe3"]
            < T["diferente"] < T["outro"] < T["isso"] < T["merece2"] < T["bonus"] < T["pe4"] < T["doi"]
            < T["tambem"] < T["manda"]):
        raise SystemExit("ERRO: ordem do jogo fora do roteiro (rodada 1 -> rodada 2 -> bônus -> CTA).")
    return voz_c, pal, T, tirado


def render(ep, mp4, tmp, previa=False):
    voz_c, pal, T, tirado = preparar(ep, tmp)
    print(f"{ep['id']}: silêncio cortado {tirado:.2f}s | contagens em {T['cont1']:.2f}s e {T['cont2']:.2f}s"
          f" | duração final {T['total']:.2f}s")
    blocos = montar_blocos(pal)
    T["_pergunta2"] = pergunta_fixa(blocos, T)

    def quadro_t(cv, t):
        quadro(cv, t, T, blocos, ep)

    if previa:
        return _previas(quadro_t, tempos_previa(T), tmp, ep["id"]), T["total"]
    wav = os.path.join(tmp, f"{ep['id']}_mix.wav")
    som.gravar_wav(wav, mixar_jogo(voz_c, T["total"], sons(T), janelas(T)))
    codificar(quadro_t, T["total"], wav, mp4)
    return mp4, T["total"]
