# -*- coding: utf-8 -*-
"""COMO FUNCIONA — "Suas pernas têm o mesmo tamanho?" (de onde vem a discrepância de membro).

Mesmo estilo e mesmas peças das cenas aprovadas (osso marfim liso, carimbo ouro opaco, legenda
karaokê, CTA com aviãozinho). Storyboard e correções do verificador
(lote4_cf/cf_discrepancia_causas_storyboard.json) respeitados aqui:
  * Dois ossos marfim LISOS, de pé sobre o chão, maléolos voltados para o meio (o par visto de
    frente). Nenhum exame simulado: nada de fundo preto, negativo, filme ou osso translúcido.
  * "milímetros": a câmera aproxima dos topos; o da direita está um fio mais baixo e uma régua
    pequena SEM números (só tracinhos) marca o vão. "tolerada": carimbo ouro, SEM check.
  * "maior": o osso da direita encurta suavemente e a cota entre os topos abre, SEM número.
  * "onde": "?" sobre o osso curto e, no alto, um VARAL com três etiquetas de bagagem em branco
    (não são as portas do cf_osteomielite). Cada origem desce, se prende no osso curto e vira:
    DE NASCENÇA (o osso não se mexe), ACIDENTE GRAVE (rebobina; traço fino em zigue-zague, sem
    sangue, sem fragmento solto, sem deslocamento; "às vezes"; "cola": as partes se aproximam e
    o traço vira costura fina no próprio marfim — sem calo dourado, sem check), NA INFÂNCIA
    (rebobina; os dois ossos encolhem por escala uniforme até tamanho de criança, iguais).
  * "lesão": balão de lupa SOLTO (marfim / faixa azul-clara / marfim, padrão cf_placa_crescimento),
    sem seta, sem linha de chamada, sem apontar ponto do osso; traço em zigue-zague na faixa.
    "cartilagem": a faixa acende. O osso inteiro NUNCA ganha faixa desenhada.
  * "infecção": halo âmbar discreto pulsa UMA vez em volta do osso (sem pontinhos, sem pus, sem
    cor de sangue). "afetar": o balão se fecha.
  * "crescer": os dois ossos crescem por escala uniforme (sem mostrar onde crescem); o da direita
    cresce menos (não para, sem contorno vermelho); a cota alarga devagar, sem número.
  * Alarme: checklist (mancar que apareceu ou piorou / diferença que aumenta rápido) e o carimbo
    PROCURE AVALIAÇÃO. Fecho: as três etiquetas se alinham no varal acima do par de ossos.
  * Cortados da tela sugerida por repetirem a legenda karaokê ao pé da letra (menos texto, mais
    mecanismo): QUASE TODO MUNDO, VEM DE ONDE?, O OSSO COLA ENCURTADO, AFETAR O CRESCIMENTO.
Cena PRESA ao roteiro pelas palavras-âncora (roteiro sem elas = KeyError, não vídeo torto).
Todo texto desenhado está em ep["tela"] (o render recusa o vídeo se não estiver).
"""
import math

import skia

from .cf_alongamento import (F_BLACK, NOVO_G, OSSO_B, OSSO_C, OSSO_L, OURO, W, C, brilhos, clamp, e_back,
                             e_in_back, e_inout, e_out, fundo, larg_texto, lerp, lerpc, paint, prog, texto)
from .cf_comum import capa, fazer_render, interface, selo_como_funciona

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "quase": ("quase", 1, False),
    "milimetros": ("milímetros", 1, False),
    "pequena": ("pequena", 1, False),
    "tolerada": ("tolerada", 1, False),
    "maior": ("maior", 1, False),
    "onde": ("onde", 1, False),
    "pode1": ("pode", 1, False),
    "nascenca": ("nascença", 1, False),
    "ou1": ("ou", 1, False),
    "acidente": ("acidente", 1, False),
    "grave": ("grave", 1, False),
    "vezes": ("vezes", 1, False),
    "cola": ("cola", 1, False),
    "encurtado": ("encurtado", 1, False),
    "na": ("na", 1, False),
    "infancia": ("infância", 1, False),
    "lesao": ("lesão", 1, False),
    "cartilagem": ("cartilagem", 1, False),
    "infeccao": ("infecção", 1, False),
    "afetar": ("afetar", 1, False),
    "dif1": ("diferença", 1, False),
    "crescer": ("crescer", 1, False),
    "crianca1": ("criança", 1, False),
    "mancar": ("mancar", 1, False),
    "dif2": ("diferença", 2, False),
    "aumenta": ("aumenta", 1, False),
    "avaliacao": ("avaliação", 1, False),
    "manda": ("manda", 1, False),
}
DESTAQUE = {"milímetros", "tolerada", "maior", "onde", "nascença", "acidente", "grave", "encurtado", "infância",
            "lesão", "cartilagem", "infecção", "crescer", "criança", "mancar", "piorou", "aumenta", "rápido",
            "avaliação"}

# ------------------------------------------------------------------ textos de tela (todos em ep["tela"])
MILIMETROS = "MILÍMETROS"
TOLERADA = "BEM TOLERADA"
INTERROGA = "?"
ORIGENS = ("DE NASCENÇA", "ACIDENTE GRAVE", "NA INFÂNCIA")
AS_VEZES = "ÀS VEZES"
LESAO = "LESÃO"
CARTILAGEM = ("CARTILAGEM", "DE CRESCIMENTO")
INFECCAO = "INFECÇÃO NO OSSO"
CRESCE = ("A DIFERENÇA PODE CRESCER", "COM A CRIANÇA")
ALARME = ("MANCAR QUE APARECEU OU PIOROU", "DIFERENÇA QUE AUMENTA RÁPIDO")
PROCURE = "PROCURE AVALIAÇÃO"

# ------------------------------------------------------------------ paleta própria
FUNDO_CARTAO = "#0B1824"
AZUL = "#9CC9FF"
CART, CART_HL, CART_ESC = "#8ECFEE", "#CDEEFB", "#4F93BA"      # cartilagem: azul-clara (cf_placa_crescimento)
ROSA = "#FF8A8F"
TRINCA = "#2B2118"
AMBAR = "#F0A43A"
ETQ, ETQ_B, ETQ_TXT, ETQ_LIN, ETQ_ARO = "#F2E2BC", "#A88442", "#13283A", "#CDB68A", "#D8BF86"
FIO = "#E6EDF3"
PREGADOR = "#C79A55"

# ------------------------------------------------------------------ geometria
Y_CHAO = 1150                 # chão onde os ossos ficam de pé
L0 = 850                      # comprimento de desenho do osso (do platô ao tornozelo)
TOPO_OFF = -7.8               # o platô sobe 7,8 acima de y0 (bounds do desenho)
S_AD, S_CR = 0.70, 0.46       # escala adulta e de criança
CAM_X, CAM_Y = 540, 700       # âncora da câmera na tela
BX, BY, BR = 815, 575, 158    # balão de lupa (solto)


def _p(cor, a=255, estilo="fill", w=0, blur=0, junta=False, traco=None):
    p = paint(cor, a, estilo, w, blur)
    if junta:
        p.setStrokeJoin(skia.Paint.kRound_Join)
    if traco:
        p.setPathEffect(skia.DashPathEffect.Make(list(traco), 0.0))
    return p


def _poli(pts, pr):
    """Polilinha desenhada até a fração `pr` (cópia do cf_placa_crescimento)."""
    n = len(pts) - 1; k = clamp(pr) * n; i = int(k)
    p = skia.Path(); p.moveTo(*pts[0])
    for j in range(1, min(i, n) + 1):
        p.lineTo(*pts[j])
    if i < n:
        f = k - i; (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        p.lineTo(lerp(x0, x1, f), lerp(y0, y1, f))
    return p


def path_osso(L):
    """O osso do piloto num contorno ÚNICO (platô em cima, maléolo embaixo), com a diáfise de
    comprimento variável: centrado em x=0, ponta de baixo em y=0 (o maléolo desce até +36)."""
    y0, yb, h = -L, 0.0, 64
    p = skia.Path()
    p.moveTo(-128, y0 + 40)
    p.cubicTo(-135, y0 - 6, -60, y0 - 18, -10, y0 + 6)
    p.cubicTo(30, y0 - 20, 132, y0 - 10, 126, y0 + 42)
    p.cubicTo(120, y0 + 120, h + 8, y0 + 150, h, y0 + 230)
    p.lineTo(h, yb - 190)
    p.cubicTo(h + 4, yb - 110, 84, yb - 70, 80, yb - 22)
    p.cubicTo(76, yb + 2, 30, yb - 4, -10, yb - 2)
    p.cubicTo(-40, yb, -52, yb + 34, -70, yb + 36)
    p.cubicTo(-92, yb + 36, -96, yb - 10, -92, yb - 60)
    p.cubicTo(-88, yb - 120, -h - 4, yb - 140, -h, yb - 190)
    p.lineTo(-h, y0 + 230)
    p.cubicTo(-h - 8, y0 + 150, -122, y0 + 120, -128, y0 + 40)
    p.close()
    return p


SH_OSSO = skia.GradientShader.MakeLinear([skia.Point(-140, 0), skia.Point(140, 0)],
                                         [C(OSSO_B), C(OSSO_C), C(OSSO_C), C(OSSO_B)], [0.0, 0.42, 0.58, 1.0])


def y_meio(L):
    """Meio da diáfise (coordenadas do osso)."""
    return -(190 + (L - 420) / 2)


def topo(s, L):
    """y do ponto mais alto do osso (mundo)."""
    return Y_CHAO - 36 * s + s * (-L + TOPO_OFF)


def osso(cv, x, s, L, esp, trinca=0.0, a_trinca=0.0, costura=0.0):
    """Osso de pé no chão em x, escala `s`, diáfise `L`; esp=-1 espelha (maléolo para o outro lado).
    trinca: quanto do traço em zigue-zague já foi riscado; costura: o traço vira costura fina
    no próprio marfim (sem calo, sem dourado)."""
    p = path_osso(L)
    cv.save(); cv.translate(x, Y_CHAO - 36 * s); cv.scale(s * esp, s)
    cv.drawPath(p, paint("#000000", 70, blur=14))
    cv.drawPath(p, paint(OSSO_C, shader=SH_OSSO))
    cv.drawPath(p, _p(OSSO_L, 150, "stroke", 2.5 / s, junta=True))
    if trinca > 0 and a_trinca > 0:
        cv.save(); cv.clipPath(p, skia.ClipOp.kIntersect, True)
        yc = y_meio(L); amp = lerp(11, 3.5, costura)
        pts = [(lerp(-72, 72, k / 8), yc + (amp if k % 2 else -amp)) for k in range(9)]
        pth = _poli(pts, trinca)
        cor = lerpc(TRINCA, OSSO_L, costura)
        cv.drawPath(pth, _p(cor, int(255 * a_trinca * lerp(1.0, 0.85, costura)), "stroke",
                            lerp(4.5, 3.0, costura) / s, junta=True))
        cv.restore()
    cv.restore()


# ------------------------------------------------------------------ estado da cena
def camera(t, T):
    """Aproxima dos topos em "milímetros", empurra devagar até "tolerada" (o plano não congela) e
    volta depois. Os topos ficam em y≈620 no zoom, para caber mais diáfise antes da máscara."""
    kz = (e_inout(prog(t, T["milimetros"] - 0.05, T["milimetros"] + 0.65))
          * (1 - e_inout(prog(t, T["tolerada"] + 0.5, T["maior"] + 0.3))))
    s_z = lerp(1.6, 1.75, e_inout(prog(t, T["milimetros"] + 0.65, T["tolerada"])))
    s = lerp(1.0, s_z, kz)
    fy = lerp(CAM_Y, topo(S_AD, L0) + 48, kz)
    return s, CAM_X, fy


def na_tela(cam, x, y):
    s, fx, fy = cam
    return CAM_X + s * (x - fx), CAM_Y + s * (y - fy)


def fim_alarme(T):
    """Início do resumo (depois do carimbo, antes da CTA)."""
    return T["manda"] - 1.25


def estado_ossos(t, T):
    # par centrado na capa; abre espaço à direita quando a câmera volta
    k1 = e_inout(prog(t, T["tolerada"] + 0.5, T["maior"] + 0.3))
    xl, xr = lerp(420, 310, k1), lerp(660, 540, k1)
    # alarme: deslizam para a esquerda e esmaecem; no resumo voltam ao centro
    k2 = e_inout(prog(t, T["mancar"] - 0.2, T["mancar"] + 0.25))   # saem ANTES do checklist entrar
    k3 = e_inout(prog(t, fim_alarme(T), fim_alarme(T) + 0.6))
    xl, xr = lerp(xl - 260 * k2, 420, k3), lerp(xr - 260 * k2, 660, k3)
    alfa = lerp(1 - k2, 1.0, k3)
    # tamanho: adulto -> criança (iguais) -> crescem, o da direita menos
    kc = e_inout(prog(t, T["na"], T["infancia"] + 0.5))
    s = lerp(S_AD, S_CR, kc)
    g = e_inout(prog(t, T["dif1"] + 0.25, T["crianca1"] + 0.5))
    ent = lerp(0.9, 1.0, e_back(prog(t, 0.0, 0.55)))
    sl, sr = s * lerp(1, 1.45, g) * ent, s * lerp(1, 1.30, g) * ent
    # comprimento do osso da direita
    Lr = L0 - 16                                                               # um fio mais baixo
    Lr = lerp(Lr, L0 - 165, e_inout(prog(t, T["maior"], T["maior"] + 0.7)))   # a maior
    Lr = lerp(Lr, L0, e_inout(prog(t, T["ou1"], T["ou1"] + 0.45)))             # rebobina
    Lr = lerp(Lr, L0 - 150, e_inout(prog(t, T["cola"], T["encurtado"] + 0.45)))  # cola encurtado
    Lr = lerp(Lr, L0, e_inout(prog(t, T["na"], T["na"] + 0.45)))              # rebobina de novo
    return dict(xl=xl, xr=xr, sl=sl, sr=sr, Lr=Lr, alfa=alfa)


def tremor(t, eventos):
    d = 0.0
    for t0, forca in eventos:
        k = t - t0
        if 0 <= k < 0.35:
            d += forca * math.sin(k * 70) * (1 - k / 0.35)
    return d


# ------------------------------------------------------------------ peças de tela
def chip(cv, s, x, y, cor, a, tam=36, cor_txt=None, esc=1.0, brilho=0.0):
    """Rótulo solto centrado em x; y = linha de base do texto."""
    if a <= 0:
        return
    lw = larg_texto(s, F_BLACK, tam)
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 22, -tam * 1.05, lw / 2 + 22, tam * 0.36), 15, 15)
    if brilho > 0:
        cv.drawRRect(rr, paint(cor, int(120 * a * brilho), blur=18))
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(228 * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 3))
    texto(cv, s, 0, 0, F_BLACK, tam, cor_txt or cor, int(255 * a))
    cv.restore()


def carimbo_opaco(cv, s, x, y, rot, t0, t, dur, tam=62, esc0=1.9):
    """Carimbo ouro torto com fundo opaco (cópia do cf_osteomielite)."""
    k = t - t0
    if k < 0 or k > dur:
        return
    esc = lerp(esc0, 1.0, e_out(clamp(k / 0.16))); a = clamp(k / 0.08) * (1 - prog(k, dur - 0.35, dur))
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(esc, esc)
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 24, -tam, lw / 2 + 24, tam * 0.36), 12, 12)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(240 * a))); cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 7))
    cv.drawString(s, -lw / 2, 0, f, paint(OURO, int(255 * a)))
    cv.restore()


def cota(cv, x, ya, yb, a, t):
    """Cota dourada entre os dois topos, SEM número (cf_placa_crescimento)."""
    if a <= 0 or yb - ya < 1:
        return
    pr = e_out(clamp(a * 1.4))
    ym = (ya + yb) / 2; m = (yb - ya) / 2 * pr
    cv.drawLine(x, ym - m, x, ym + m, paint(NOVO_G, int(110 * a * (0.7 + 0.3 * math.sin(t * 5))), "stroke", 16, blur=8))
    cv.drawLine(x, ym - m, x, ym + m, paint(OURO, int(255 * a), "stroke", 5))
    for yy in (ym - m, ym + m):
        cv.drawLine(x - 16, yy, x + 16, yy, paint(OURO, int(255 * a), "stroke", 5))


def regua_mm(cv, x, ya, yb, a, t, pulso=0.0):
    """Régua pequena SEM números (só tracinhos); o vão entre os topos acende em ouro.
    pulso 0..1: brilho único da faixa ("pequena assim")."""
    if a <= 0:
        return
    y0, y1 = ya - 100, yb + 100
    rr = skia.RRect.MakeRectXY(skia.Rect(x, y0, x + 44, y1), 8, 8)
    cv.drawRRect(rr, paint("#000000", int(90 * a), blur=8))
    cv.drawRRect(rr, paint("#EEF3F8", int(240 * a)))
    cv.drawRRect(rr, paint("#5E7186", int(255 * a), "stroke", 2.5))
    if pulso > 0:
        cv.drawRect(skia.Rect(x - 18 * pulso, ya - 12 * pulso, x + 44 + 18 * pulso, yb + 12 * pulso),
                    paint(NOVO_G, int(210 * a * pulso), blur=22))
    cv.drawRect(skia.Rect(x + 2, ya, x + 42, yb), paint(OURO, int(150 * a * (0.75 + 0.25 * math.sin(t * 6))), blur=8))
    cv.drawRect(skia.Rect(x + 2, ya, x + 42, yb), paint(lerpc(OURO, "#FFF3C4", pulso), int(235 * a)))
    yy, i = y0 + 6, 0
    while yy < y1 - 4:
        cv.drawLine(x + 2, yy, x + (20 if i % 5 == 0 else 12), yy, paint("#3C4B5C", int(230 * a), "stroke", 2.2))
        yy += 8; i += 1


def rebobina(cv, x, y, t, t0):
    """Símbolo de rebobinar (dois triângulos, sem texto)."""
    k = t - t0
    if k < 0 or k > 0.8:
        return
    a = clamp(k / 0.1) * (1 - prog(k, 0.5, 0.8)); esc = lerp(0.6, 1.0, e_back(clamp(k / 0.25)))
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    cv.drawCircle(0, 0, 56, paint(FUNDO_CARTAO, int(200 * a)))
    cv.drawCircle(0, 0, 56, paint("#FFFFFF", int(180 * a), "stroke", 3))
    for dx in (-22, 10):
        p = skia.Path(); p.moveTo(dx - 16, 0); p.lineTo(dx + 16, -22); p.lineTo(dx + 16, 22); p.close()
        cv.drawPath(p, paint("#FFFFFF", int(255 * a)))
    cv.restore()


def interrogacao(cv, x, y, t, t0, t1):
    a = prog(t, t0, t0 + 0.12) * (1 - prog(t, t1, t1 + 0.3))
    if a <= 0:
        return
    pul = lerp(0.5, 1.0, e_back(prog(t, t0, t0 + 0.4))) * (1 + 0.05 * math.sin(t * 6.5))
    cv.save(); cv.translate(x, y); cv.scale(pul, pul)
    cv.drawCircle(0, -60, 85, paint(NOVO_G, int(70 * a), blur=34))
    texto(cv, INTERROGA, 0, 0, F_BLACK, 156, OURO, int(255 * a), contorno=12)
    cv.restore()


# ------------------------------------------------------------------ varal e etiquetas de bagagem
TAM_ETQ = 30
ETQ_W = [larg_texto(s, F_BLACK, TAM_ETQ) + 64 for s in ORIGENS]
SLOT_C = (202, 540, 880)                                   # centro do corpo de cada etiqueta no varal
SLOT_X = [c + 22 - w / 2 for c, w in zip(SLOT_C, ETQ_W)]   # x do furo (onde o fio prende)
Y_VARAL, SAG = 236, 46


def y_corda(x, sag):
    return Y_VARAL + sag * (1 - ((x - 540) / 560) ** 2)


def etiqueta(cv, i, hx, hy, ang, flip, a, esc=1.0, brilho=0.0):
    """Etiqueta de bagagem com o furo em (hx, hy); o corpo pende à direita do furo.
    flip 0..1: a etiqueta vira; em branco até a metade, com a origem escrita depois."""
    if a <= 0:
        return
    w, h = ETQ_W[i], 60
    x0, y0, x1, y1 = -22, -20, -22 + w, 40
    cv.save(); cv.translate(hx, hy); cv.rotate(ang); cv.scale(esc, esc)
    sx = max(0.04, abs(math.cos(math.pi * clamp(flip))))
    cx = (x0 + x1) / 2
    cv.translate(cx, 0); cv.scale(sx, 1); cv.translate(-cx, 0)
    p = skia.Path()
    p.moveTo(x0 + 16, y0); p.lineTo(x1 - 8, y0); p.quadTo(x1, y0, x1, y0 + 8); p.lineTo(x1, y1 - 8)
    p.quadTo(x1, y1, x1 - 8, y1); p.lineTo(x0 + 16, y1); p.lineTo(x0, y1 - 16); p.lineTo(x0, y0 + 16); p.close()
    if brilho > 0:
        cv.drawPath(p, paint(OURO, int(150 * a * brilho), blur=20))
    cv.drawPath(p, paint("#000000", int(80 * a), blur=10))
    cv.drawPath(p, paint(ETQ, int(255 * a)))
    cv.drawPath(p, _p(ETQ_B, int(255 * a), "stroke", 3, junta=True))
    cv.drawCircle(0, 0, 11, paint(ETQ_ARO, int(255 * a)))                 # reforço do furo
    cv.drawCircle(0, 0, 11, paint(ETQ_B, int(255 * a), "stroke", 2))
    cv.drawCircle(0, 0, 5.5, paint("#0E2232", int(255 * a)))
    if flip >= 0.5:
        texto(cv, ORIGENS[i], 24, 21, F_BLACK, TAM_ETQ, ETQ_TXT, int(255 * a), centro=False)
    else:
        for yy, fr in ((3, 1.0), (21, 0.6)):
            cv.drawLine(26, yy, 26 + (x1 - 50) * fr, yy, paint(ETQ_LIN, int(255 * a), "stroke", 5))
    cv.restore()


def tempos_etq(T):
    """(desce0, desce1 = vira, sobe0, sobe1) de cada etiqueta, presos às palavras. Em SÉRIE: a
    etiqueta seguinte só desce depois que a anterior chegou de volta ao varal (nada se cruza)."""
    sobe0 = (T["ou1"] - 0.2, T["ou1"] + 0.25)
    sobe1 = (T["na"] - 0.35, T["na"] + 0.1)
    return ((T["pode1"] + 0.05, T["nascenca"] + 0.05) + sobe0,
            (max(T["acidente"], sobe0[1] + 0.02), T["grave"] + 0.05) + sobe1,
            (sobe1[1] + 0.02, T["infancia"] + 0.4, T["dif1"], T["dif1"] + 0.55))


Y_CORREDOR = 410          # altura do furo no voo: abaixo das etiquetas do varal, acima do "?" e dos topos
X_DESCIDA = 728           # a descida corre à direita da cota e do platô do osso curto


def trilha_desce(i, slot, anexo):
    """Pontos de passagem do furo: corredor horizontal no alto e descida pela direita do osso."""
    sx, sy = slot
    xd = min(X_DESCIDA, 1036 - (ETQ_W[i] - 22))          # o corpo da etiqueta não passa de x=1036
    if i == 2:
        pts = [slot, (sx - 12, Y_CORREDOR + 10)]
    else:
        pts = [slot, (sx + 24, Y_CORREDOR)]       # primeiro desce, depois corre: não raspa a vizinha
        if i == 0:
            pts.append((420, Y_CORREDOR + 4))
        pts.append((xd - 30, Y_CORREDOR + 14))
    pts += [(xd, 600), (xd - 14, 840), anexo]
    return pts


def _na_trilha(pts, u):
    """Catmull-Rom pelos pontos, percorrida por fração do comprimento (velocidade uniforme)."""
    dens = []
    n = len(pts)
    for j in range(n - 1):
        p0, p1, p2, p3 = pts[max(j - 1, 0)], pts[j], pts[j + 1], pts[min(j + 2, n - 1)]
        for k in range(16):
            s = k / 16; s2, s3 = s * s, s * s * s
            dens.append(tuple(0.5 * (2 * p1[c] + (-p0[c] + p2[c]) * s + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * s2
                                     + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * s3) for c in (0, 1)))
    dens.append(pts[-1])
    acc = [0.0]
    for a, b in zip(dens, dens[1:]):
        acc.append(acc[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    alvo = clamp(u) * acc[-1]
    for j in range(1, len(acc)):
        if acc[j] >= alvo:
            f = (alvo - acc[j - 1]) / max(1e-6, acc[j] - acc[j - 1])
            return lerp(dens[j - 1][0], dens[j][0], f), lerp(dens[j - 1][1], dens[j][1], f)
    return pts[-1]


def ponto_anexo(st, cam):
    """Onde a etiqueta se prende no osso da direita: laço na diáfise, perto do pé."""
    sr, xr = st["sr"], st["xr"]
    xa, ya = na_tela(cam, xr, Y_CHAO - 36 * sr - 250 * sr)
    hw = 64 * sr * cam[0]
    return xa, ya, hw


def varal(cv, t, T, st, cam):
    # entra de cima só 70 px: nada atravessa o selo COMO FUNCIONA (y 150-204)
    dy = lerp(-70, 0, e_back(prog(t, T["onde"] - 0.05, T["onde"] + 0.55), 1.4))
    a_v = prog(t, T["onde"] - 0.05, T["onde"] + 0.2)
    if a_v <= 0:
        return
    alinha = e_inout(prog(t, T["manda"] - 0.05, T["manda"] + 0.45))
    a_v *= lerp(1.0, 0.55, prog(t, T["mancar"], T["mancar"] + 0.4) * (1 - prog(t, fim_alarme(T), fim_alarme(T) + 0.4)))
    sag = SAG * (1 - alinha)
    # corda
    p = skia.Path(); p.moveTo(-20, y_corda(-20, sag) + dy)
    for k in range(1, 41):
        x = lerp(-20, 1100, k / 40); p.lineTo(x, y_corda(x, sag) + dy)
    cv.drawPath(p, paint("#000000", int(70 * a_v), "stroke", 7, blur=4))
    cv.drawPath(p, paint(FIO, int(230 * a_v), "stroke", 3.5))
    for i in range(3):                                         # fecho: brilham ATRÁS das etiquetas (texto limpo)
        x = SLOT_C[i]; y = y_corda(SLOT_X[i], 0) + 24 + 10
        brilhos(cv, x, y, t, T["manda"] + 0.35, n=10, raio=150)
    xa, ya, hw = ponto_anexo(st, cam)
    for i, (d0, d1, u0, u1) in enumerate(tempos_etq(T)):
        sx = SLOT_X[i]; sy = y_corda(sx, sag) + dy
        slot = (sx, sy + 24)
        amp = lerp(5, 2.2, prog(t, T["onde"], T["onde"] + 2.0)) * (1 - alinha)
        ang_v = amp * math.sin(t * 2.3 + i * 1.7)
        anexo = (xa + hw + 56, ya + 26)
        flip = prog(t, d1, d1 + 0.3)
        brilho = (1 - prog(t, T["manda"] + 0.6, T["manda"] + 1.4)) * prog(t, T["manda"], T["manda"] + 0.3)
        a_i = a_v if (t < d0 or t >= u1) else 1.0
        pregador = True
        if t < d0 or t >= u1:
            (hx, hy), ang, esc = slot, ang_v, 1.0
        elif t < d1:                                           # desce: corredor no alto, cai pela direita
            u = e_inout(prog(t, d0, d1))
            hx, hy = _na_trilha(trilha_desce(i, slot, anexo), u)
            ang, esc = -3 * math.sin(math.pi * u), lerp(1.0, 1.06, prog(u, 0.85, 1.0)); pregador = False
        elif t < u0:                                           # presa no osso
            (hx, hy), ang, esc = anexo, 3 * math.sin(t * 2.0 + i), 1.06; pregador = False
        else:                                                  # sobe de volta ao varal (já escrita), mesma trilha
            u = e_inout(prog(t, u0, u1))
            hx, hy = _na_trilha(trilha_desce(i, slot, anexo)[::-1], u)
            ang, esc = -3 * math.sin(math.pi * u), lerp(1.06, 1.0, prog(u, 0.0, 0.15)); pregador = False
        # fio
        if pregador:
            cv.drawLine(sx, sy, hx, hy, paint(FIO, int(220 * a_i), "stroke", 2.5))
            cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(sx - 6, sy - 14, sx + 6, sy + 12), 3, 3),
                         paint(PREGADOR, int(255 * a_i)))
            cv.drawLine(sx, sy - 12, sx, sy + 10, paint("#8A6A35", int(255 * a_i), "stroke", 1.5))
        elif d1 <= t < u0:                                     # laço na diáfise + fio até o furo
            k = prog(t, d1 - 0.05, d1 + 0.15)
            r = skia.Rect(xa - hw - 4, ya - 7, xa + hw + 4, ya + 7)
            cv.drawArc(r, 0, 180, False, paint(FIO, int(255 * k), "stroke", 3))
            cv.drawLine(xa + hw + 2, ya, lerp(xa + hw + 2, hx, k), lerp(ya, hy, k), paint(FIO, int(240 * k), "stroke", 2.5))
            cv.drawCircle(xa + hw + 3, ya, 5, paint(FIO, int(255 * k)))
        else:                                                  # em voo: pedaço de fio solto
            cv.drawLine(hx, hy, hx - 6, hy - 24, paint(FIO, 220, "stroke", 2.5))
        etiqueta(cv, i, hx, hy, ang, flip, a_i, esc, brilho)


# ------------------------------------------------------------------ balão de lupa (solto)
_RS = BR + 50
SOMBRA_BALAO = skia.GradientShader.MakeRadial(
    skia.Point(0, 14), _RS, [C("#000000", 120), C("#000000", 120), C("#000000", 50), C("#000000", 0)],
    [0.0, (BR - 30) / _RS, BR / _RS, 1.0])


def lupa(cv, t, T, esc):
    """Balão SOLTO: marfim / faixa azul-clara / marfim; traço em zigue-zague na faixa (lesão)."""
    if esc <= 0.01:
        return
    by = BY + 4 * math.sin(t * 1.2)
    cv.save(); cv.translate(BX, by); cv.scale(esc, esc)
    cv.drawCircle(0, 14, _RS, paint("#000000", shader=SOMBRA_BALAO))
    cv.save()
    clip = skia.Path(); clip.addCircle(0, 0, BR)
    cv.clipPath(clip, skia.ClipOp.kIntersect, True)
    sh = skia.GradientShader.MakeLinear([skia.Point(-BR, 0), skia.Point(BR, 0)],
                                        [C(OSSO_B), C(OSSO_C), C(OSSO_C), C(OSSO_B)], [0.0, 0.36, 0.64, 1.0])
    cv.drawRect(skia.Rect(-BR, -BR, BR, BR), paint(OSSO_C, shader=sh))
    y0, y1 = 2, 60
    b = prog(t, T["cartilagem"] - 0.05, T["cartilagem"] + 0.25)
    b = b * lerp(1.0, 0.45, e_out(prog(t, T["cartilagem"] + 0.3, T["cartilagem"] + 1.0)))
    if b > 0:
        cv.drawRect(skia.Rect(-BR, y0 - 16, BR, y1 + 16), paint(AZUL, int(150 * b), blur=18))
    cv.drawRect(skia.Rect(-BR, y0, BR, y1), paint(CART))
    cv.drawRect(skia.Rect(-BR, y0, BR, y0 + 10), paint(CART_HL, 150))
    if b > 0:
        cv.drawRect(skia.Rect(-BR, y0, BR, y1), paint("#FFFFFF", int(110 * b)))
    cv.drawLine(-BR, y0, BR, y0, paint(CART_ESC, 210, "stroke", 2.5))
    cv.drawLine(-BR, y1, BR, y1, paint(CART_ESC, 210, "stroke", 2.5))
    tr = e_out(prog(t, T["lesao"] + 0.15, T["lesao"] + 0.45))
    if tr > 0:
        yc = (y0 + y1) / 2
        pts = [(lerp(-BR, BR, k / 14), yc + (11 if k % 2 else -11)) for k in range(15)]
        cv.drawPath(_poli(pts, tr), _p(TRINCA, 255, "stroke", 4.5, junta=True))
    cv.restore()
    cv.drawCircle(0, 0, BR, paint("#000000", 90, "stroke", 22, blur=8))
    cv.drawCircle(0, 0, BR, paint(OURO, 255, "stroke", 11))
    cv.drawCircle(0, 0, BR - 9, paint("#FFFFFF", 80, "stroke", 3))
    # rótulo LESÃO dentro do balão, com setinha até a faixa (não aponta o osso)
    a = prog(t, T["lesao"] + 0.1, T["lesao"] + 0.3)
    if a > 0:
        tam = 32; lw = larg_texto(LESAO, F_BLACK, tam); yp = -62
        rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 18, yp - tam - 4, lw / 2 + 18, yp + 12), 14, 14)
        cv.drawRRect(rr, paint(FUNDO_CARTAO, int(232 * a))); cv.drawRRect(rr, paint(ROSA, int(255 * a), "stroke", 3))
        texto(cv, LESAO, 0, yp, F_BLACK, tam, ROSA, int(255 * a))
        cv.drawLine(0, yp + 14, 0, y0 - 14, paint(ROSA, int(255 * a), "stroke", 4))
        p = skia.Path(); p.moveTo(-10, y0 - 16); p.lineTo(10, y0 - 16); p.lineTo(0, y0 - 3); p.close()
        cv.drawPath(p, paint(ROSA, int(255 * a)))
    cv.restore()


def rotulo_cartilagem(cv, t, T):
    a = prog(t, T["cartilagem"], T["cartilagem"] + 0.25) * (1 - prog(t, T["afetar"] - 0.1, T["afetar"] + 0.2))
    if a <= 0:
        return
    tam = 32; lw = max(larg_texto(s, F_BLACK, tam) for s in CARTILAGEM)
    dy = 14 * (1 - e_out(prog(t, T["cartilagem"], T["cartilagem"] + 0.35)))
    y0 = BY + BR + 22 + dy
    rr = skia.RRect.MakeRectXY(skia.Rect(BX - lw / 2 - 22, y0, BX + lw / 2 + 22, y0 + 96), 16, 16)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(228 * a))); cv.drawRRect(rr, paint(AZUL, int(255 * a), "stroke", 3))
    texto(cv, CARTILAGEM[0], BX, y0 + 42, F_BLACK, tam, "#FFFFFF", int(255 * a))
    texto(cv, CARTILAGEM[1], BX, y0 + 82, F_BLACK, tam, AZUL, int(255 * a))


# ------------------------------------------------------------------ halo da infecção e rótulo
def halo(cv, t, T, st):
    up = prog(t, T["infeccao"] - 0.05, T["infeccao"] + 0.3)
    a = up * lerp(1.0, 0.35, e_out(prog(t, T["infeccao"] + 0.3, T["infeccao"] + 1.1))) * (1 - prog(t, T["afetar"], T["afetar"] + 0.6))
    if a <= 0:
        return
    sr, xr = st["sr"], st["xr"]
    yt = topo(sr, L0); ym = (yt + Y_CHAO) / 2
    infla = 1 + 0.08 * e_out(prog(t, T["infeccao"], T["infeccao"] + 0.5))
    rx = (132 * sr + 46) * infla; ry = ((Y_CHAO - yt) / 2 + 40) * infla
    cv.drawOval(skia.Rect(xr - rx, ym - ry, xr + rx, ym + ry), paint(AMBAR, int(150 * a), blur=30))


def rotulo_infeccao(cv, t, T, st, cam):
    a = prog(t, T["infeccao"], T["infeccao"] + 0.25) * (1 - prog(t, T["afetar"] - 0.1, T["afetar"] + 0.2))
    if a <= 0:
        return
    tam = 34; lw = larg_texto(INFECCAO, F_BLACK, tam)
    # encostado no osso da direita (à esquerda do balão, acima da linha de nível); a linha-guia
    # desce em diagonal pelo vão e termina NO contorno da diáfise do osso da direita
    x0, yb = 445 - (lw + 30) / 2, 690
    sr = st["sr"]
    xa, ya = na_tela(cam, st["xr"] - 64 * sr, Y_CHAO - (Y_CHAO - topo(sr, L0)) * 0.45)
    cv.drawLine(430, yb + 13, xa, ya, paint(AMBAR, int(220 * a), "stroke", 2.5))
    cv.drawCircle(xa, ya, 6, paint(AMBAR, int(255 * a)))
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, yb - tam - 6, x0 + lw + 30, yb + 13), 14, 14)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(228 * a))); cv.drawRRect(rr, paint(AMBAR, int(255 * a), "stroke", 3))
    texto(cv, INFECCAO, x0 + 15, yb, F_BLACK, tam, AMBAR, int(255 * a), centro=False)


# ------------------------------------------------------------------ alarme
def triangulo_alerta(cv, x, y, a, esc):
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    p = skia.Path(); p.moveTo(0, -46); p.lineTo(52, 42); p.lineTo(-52, 42); p.close()
    cv.drawPath(p, paint(OURO, int(90 * a), blur=14))
    cv.drawPath(p, _p(FUNDO_CARTAO, int(240 * a), junta=True))
    cv.drawPath(p, _p(OURO, int(255 * a), "stroke", 7, junta=True))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-5, -18, 5, 16), 5, 5), paint(OURO, int(255 * a)))
    cv.drawCircle(0, 28, 6, paint(OURO, int(255 * a)))
    cv.restore()


def checklist(cv, t, T):
    """Entra só depois que os ossos saíram (encadeado, nada sobreposto)."""
    t0 = T["mancar"] + 0.2
    a_g = prog(t, t0, t0 + 0.3) * (1 - prog(t, fim_alarme(T) - 0.1, fim_alarme(T) + 0.2))
    if a_g <= 0:
        return
    x0 = 118 + 180 * (1 - e_out(prog(t, t0, t0 + 0.45)))
    triangulo_alerta(cv, CAM_X, 470, a_g, lerp(0.6, 1.0, e_back(prog(t, t0, t0 + 0.45))))
    for k, (rot, t_txt, t_ok) in enumerate(((ALARME[0], t0, T["mancar"] + 0.5),
                                            (ALARME[1], T["dif2"], T["aumenta"]))):
        y = 610 + k * 112
        rr = skia.RRect.MakeRectXY(skia.Rect(x0, y - 44, x0 + 52, y + 8), 10, 10)
        cv.drawRRect(rr, paint(FUNDO_CARTAO, int(220 * a_g))); cv.drawRRect(rr, paint(OURO, int(255 * a_g), "stroke", 3.5))
        pr = e_out(prog(t, t_ok, t_ok + 0.3))
        if pr > 0:
            p = skia.Path(); p.moveTo(x0 + 10, y - 19)
            p.lineTo(x0 + 10 + 12 * min(1, pr * 2), y - 19 + 12 * min(1, pr * 2))
            if pr > 0.5:
                q = (pr - 0.5) * 2
                p.lineTo(x0 + 22 + 24 * q, y - 7 - 32 * q)
            cv.drawPath(p, paint(OURO, int(255 * a_g), "stroke", 6))
        ai = a_g * prog(t, t_txt - 0.05, t_txt + 0.2)
        if ai > 0:
            ok = prog(t, t_ok, t_ok + 0.25)
            texto(cv, rot, x0 + 70 - 20 * (1 - e_out(prog(t, t_txt - 0.05, t_txt + 0.3))), y - 4, F_BLACK, 36,
                  lerpc("#C8D3DE", "#FFFFFF", ok), int(255 * ai), centro=False, contorno=8)


def cartao_cresce(cv, t, T):
    a = prog(t, T["crescer"] - 0.05, T["crescer"] + 0.2) * (1 - prog(t, T["mancar"] - 0.3, T["mancar"] - 0.05))
    if a <= 0:
        return
    tam = 36; lw = larg_texto(CRESCE[0], F_BLACK, tam)
    esc = lerp(0.85, 1.0, e_back(prog(t, T["crescer"] - 0.05, T["crescer"] + 0.4)))
    cv.save(); cv.translate(CAM_X, 455); cv.scale(esc, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 26, -60, lw / 2 + 26, 62), 20, 20)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(235 * a))); cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 3.5))
    texto(cv, CRESCE[0], 0, -12, F_BLACK, tam, "#FFFFFF", int(255 * a))
    a2 = a * prog(t, T["crianca1"] - 0.05, T["crianca1"] + 0.2)
    if a2 > 0:
        texto(cv, CRESCE[1], 0, 38 + 10 * (1 - e_out(prog(t, T["crianca1"], T["crianca1"] + 0.3))), F_BLACK, tam,
              OURO, int(255 * a2))
    cv.restore()


# ------------------------------------------------------------------ mundo (ossos) e medidas
def mundo(cv, t, T, st, cam):
    s, fx, fy = cam
    dx = tremor(t, ((T["grave"] + 0.02, 7),))
    cv.save(); cv.translate(CAM_X + dx, CAM_Y); cv.scale(s, s); cv.translate(-fx, -fy)
    xl, xr, sl, sr, Lr = st["xl"], st["xr"], st["sl"], st["sr"], st["Lr"]
    cv.drawLine(xl - 190 * max(sl, 0.5), Y_CHAO + 2, xr + 190 * max(sr, 0.5), Y_CHAO + 2,
                paint("#FFFFFF", 55, "stroke", 3))
    halo(cv, t, T, st)
    osso(cv, xl, sl, L0, -1)
    pr = e_out(prog(t, T["grave"], T["grave"] + 0.18))
    a_tr = 1 - prog(t, T["na"], T["na"] + 0.4)
    costura = e_inout(prog(t, T["cola"], T["encurtado"] + 0.3))
    osso(cv, xr, sr, Lr, 1, pr, a_tr, costura)
    cv.restore()


def medidas(cv, t, T, st, cam):
    """Linha de nível nos topos, régua dos milímetros e cota (tela)."""
    s = cam[0]
    xl_s, yl_s = na_tela(cam, st["xl"], topo(st["sl"], L0))
    xr_s, yr_s = na_tela(cam, st["xr"], topo(st["sr"], st["Lr"]))
    alfa = st["alfa"]
    x_ini = xl_s - 150 * st["sl"] * s
    x_cota = xr_s + 132 * st["sr"] * s + 34
    a_reg = prog(t, T["milimetros"] + 0.3, T["milimetros"] + 0.55) * (1 - prog(t, T["tolerada"] + 0.45, T["tolerada"] + 0.75))
    x_fim = x_cota + (44 if a_reg > 0 else 24)
    # nível do topo da esquerda (desenha da esquerda para a direita)
    pr = e_inout(prog(t, T["quase"] + 0.2, T["quase"] + 0.85))
    a0 = prog(t, T["quase"] + 0.2, T["quase"] + 0.4) * alfa
    if a0 > 0 and pr > 0:
        xe = lerp(x_ini, x_fim, pr)
        cv.drawLine(x_ini, yl_s, xe, yl_s, _p(FUNDO_CARTAO, int(150 * a0), "stroke", 8, traco=(18, 12)))
        cv.drawLine(x_ini, yl_s, xe, yl_s, _p("#FFFFFF", int(225 * a0), "stroke", 3.5, traco=(18, 12)))
    gap = yr_s - yl_s
    a_c = clamp((gap - 6) / 14) * prog(t, T["maior"] + 0.05, T["maior"] + 0.35) * alfa
    a_r = max(a_c, a_reg * clamp((gap - 4) / 8))
    if a_r > 0:
        cv.drawLine(xr_s - 110 * st["sr"] * s, yr_s, x_fim, yr_s, _p(FUNDO_CARTAO, int(150 * a_r), "stroke", 8, traco=(18, 12)))
        cv.drawLine(xr_s - 110 * st["sr"] * s, yr_s, x_fim, yr_s, _p("#FFFFFF", int(225 * a_r), "stroke", 3.5, traco=(18, 12)))
    if a_reg > 0:
        pulso = math.sin(math.pi * prog(t, T["pequena"] - 0.02, T["pequena"] + 0.42))
        regua_mm(cv, x_cota, yl_s, yr_s, a_reg, t, pulso)
        brilhos(cv, x_cota + 22, (yl_s + yr_s) / 2, t, T["pequena"], n=8, raio=64)
        chip(cv, MILIMETROS, x_cota - 150, yl_s - 50,
             OURO, a_reg, tam=34, cor_txt="#FFFFFF", esc=lerp(0.8, 1.0, e_back(prog(t, T["milimetros"] + 0.3, T["milimetros"] + 0.65))))
    cota(cv, x_cota, yl_s, yr_s, a_c, t)
    return xr_s, yr_s


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    cam = camera(t, T)
    st = estado_ossos(t, T)

    # mundo numa camada: com a câmera perto, o osso não invade a faixa da legenda (y > 1230)
    alfa = st["alfa"]
    if alfa > 0:
        cv.saveLayerAlpha(None, int(255 * alfa)) if alfa < 1 else cv.saveLayer(None, None)
        mundo(cv, t, T, st, cam)
        z = clamp((CAM_Y + cam[0] * (Y_CHAO + 40 - cam[2]) - 1225) / 40)
        if z > 0:
            masc = skia.Paint(AntiAlias=True)
            masc.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 1110), skia.Point(0, 1228)],
                                                          [skia.ColorSetARGB(255, 0, 0, 0),
                                                           skia.ColorSetARGB(int(255 * (1 - z)), 0, 0, 0)]))
            masc.setBlendMode(skia.BlendMode.kDstIn)
            cv.drawRect(skia.Rect(0, 1000, W, 1920), masc)
        cv.restore()

    xr_s, yr_s = medidas(cv, t, T, st, cam)

    # rótulos e peças de tela
    # acima dos topos no zoom e no plano aberto; some antes do osso encurtar em "maior"
    carimbo_opaco(cv, TOLERADA, 540, 400, -6, T["tolerada"], t, dur=T["maior"] - T["tolerada"] + 0.1, tam=58, esc0=1.6)
    interrogacao(cv, xr_s, yr_s - 46, t, T["onde"], T["nascenca"] + 0.05)
    # some antes de a etiqueta 2 subir pela direita do osso
    a_v = prog(t, T["vezes"] - 0.05, T["vezes"] + 0.2) * (1 - prog(t, T["encurtado"] + 0.1, T["encurtado"] + 0.4))
    if a_v > 0:
        lw = larg_texto(AS_VEZES, F_BLACK, 34)
        y_tr = Y_CHAO - 36 * st["sr"] + st["sr"] * y_meio(st["Lr"])
        chip(cv, AS_VEZES, st["xr"] + 64 * st["sr"] + 26 + lw / 2 + 22, y_tr - 44, OURO, a_v, tam=34,
             esc=lerp(0.7, 1.0, e_back(prog(t, T["vezes"] - 0.05, T["vezes"] + 0.35))),
             brilho=1 - prog(t, T["vezes"] + 0.2, T["vezes"] + 0.9))
    rebobina(cv, 130, 640, t, T["ou1"])     # abaixo do corredor das etiquetas
    rebobina(cv, 130, 640, t, T["na"])

    esc_l = e_back(prog(t, T["lesao"] - 0.05, T["lesao"] + 0.35)) * (1 - e_in_back(prog(t, T["afetar"], T["afetar"] + 0.4)))
    lupa(cv, t, T, esc_l)
    rotulo_cartilagem(cv, t, T)
    rotulo_infeccao(cv, t, T, st, cam)
    cartao_cresce(cv, t, T)
    checklist(cv, t, T)
    carimbo_opaco(cv, PROCURE, CAM_X, 880, -5, T["avaliacao"], t, dur=fim_alarme(T) - T["avaliacao"] + 0.15,
                  tam=58, esc0=1.5)

    capa(cv, t, T["milimetros"] + 0.1, ep["gancho"][0], ep["gancho"][1])
    selo_como_funciona(cv, prog(t, T["milimetros"] + 0.55, T["milimetros"] + 0.95) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    t_cta = T["manda"] - 0.15
    if t < t_cta:
        varal(cv, t, T, st, cam)
        interface(cv, t, T, blocos, DESTAQUE)
    else:                       # fecho: o varal (resumo das três origens) fica por cima do véu da CTA
        interface(cv, t, T, blocos, DESTAQUE)
        varal(cv, t, T, st, cam)


# ------------------------------------------------------------------ som e prévias
def sons(T):
    te = tempos_etq(T)
    ev = [(0.05, "whoosh", 0.4), (0.3, "pop", 0.45), (T["quase"] + 0.25, "tick", 0.3),
          (T["milimetros"] - 0.05, "whoosh", 0.45), (T["milimetros"] + 0.3, "ping", 0.45)]
    ev += [(T["milimetros"] + 0.38 + 0.09 * i, "click", 0.35) for i in range(3)]
    ev += [(T["pequena"], "ping", 0.35)]
    ev += [(T["tolerada"], "thump", 0.85), (T["tolerada"] + 0.5, "whoosh", 0.35),
           (T["maior"] + 0.05, "whoosh", 0.3), (T["maior"] + 0.15, "pop", 0.55),
           (T["onde"], "pop", 0.65), (T["onde"] + 0.05, "whoosh", 0.45), (T["onde"] + 0.55, "tick", 0.35),
           (te[0][0], "whoosh", 0.4), (te[0][1] + 0.12, "pop", 0.6),
           (T["ou1"], "whoosh", 0.5), (te[1][0] + 0.05, "whoosh", 0.3), (te[1][1] + 0.12, "pop", 0.6),
           (T["grave"], "tick", 1.0), (T["grave"] + 0.02, "thump", 0.8),
           (T["vezes"], "ping", 0.45),
           (T["cola"], "click", 0.6), (T["cola"] + 0.25, "click", 0.5), (T["encurtado"] + 0.35, "thump", 0.5),
           (te[1][2], "whoosh", 0.3), (T["na"], "whoosh", 0.5), (te[2][0] + 0.05, "whoosh", 0.3), (te[2][1] + 0.12, "pop", 0.6),
           (T["lesao"] - 0.05, "pop", 0.65), (T["lesao"] + 0.2, "tick", 0.6),
           (T["cartilagem"], "shimmer", 0.5), (T["infeccao"], "ping", 0.45),
           (T["afetar"], "whoosh", 0.4), (te[2][2], "whoosh", 0.35)]
    t0, t1 = T["dif1"] + 0.3, T["crianca1"] + 0.45                 # os dois ossos crescendo
    n = max(2, int((t1 - t0) / 0.22))
    ev += [(t0 + 0.22 * i, "click", 0.45) for i in range(n)]
    ev += [(T["crescer"], "pop", 0.45), (T["crianca1"], "ding", 0.45),
           (T["mancar"] - 0.2, "whoosh", 0.5), (T["mancar"] + 0.2, "pop", 0.45), (T["mancar"] + 0.5, "tick", 0.75),
           (T["aumenta"], "tick", 0.75),
           (T["avaliacao"], "thump", 0.9), (fim_alarme(T), "whoosh", 0.4),
           (T["manda"], "shimmer", 0.6), (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def tempos_previa(T):
    return [0.0, T["pequena"] + 0.15, T["tolerada"] + 0.25, T["onde"] + 0.7, T["nascenca"] + 0.6,
            T["grave"] + 0.6, T["encurtado"] + 0.6, T["cartilagem"] + 0.5, T["infeccao"] + 0.6,
            T["crianca1"] + 0.4, T["avaliacao"] + 0.4, T["manda"] + 1.6]


render = fazer_render(quadro, ANCORAS, sons, tempos_previa, respiro_cta=2.0)
