# -*- coding: utf-8 -*-
"""COMO FUNCIONA — pernas em O e em X na criança ("PERNA EM O / QUE VIRA X?").

Mesmo estilo das cenas aprovadas (fundo azul-petróleo com partículas, dourado, rótulos com fio e
ponto, carimbo, brilhos, legenda karaokê, CTA com aviãozinho) e as pernas de DESENHO do
cf_pe_virado (contorno arredondado, pele lisa, short azul, sem rosto). O mecanismo: o par de pernas
dobra para fora (O), INVERTE devagar para X e alinha; o calendário (três folhas VAZIAS, sem
número) acende uma folha por fase. O que o verificador exigiu (lote4_cf/cf_pernas_x_o_storyboard.json):
  * Nada de osso, nada translúcido, nada de exame: a lupa do fim só aumenta o próprio desenho.
  * As pernas NUNCA crescem: o desenho tem o mesmo tamanho em todas as fases (a idade aparece só no
    calendário — nada de régua, nada de altura). Na fileira do "juntas" as três fases têm o mesmo
    tamanho.
  * "SOZINHA" só aparece dentro de "COSTUMA ALINHAR SOZINHA".
  * O chapéu de cowboy é ícone AO LADO do rótulo (nunca na criança) e sai no "inverte".
  * Dor: um raio vermelho discreto AO LADO da perna, sem apontar nenhum ponto do corpo.
  * RAQUITISMO é etiqueta marfim neutra: sem osso, sem alimento, sem nada que sugira culpa.
Cena PRESA ao roteiro pelas palavras-âncora (ANCORAS): roteiro sem elas = KeyError, não vídeo torto.

Desvio do contrato (anotado, mesmo caso do cf_fixador_circular): o edge-tts devolve a letra da 3ª
frase como "X." (com o ponto) e o `alinhar` comum recusa o vídeo ("palavra da voz 'X.' não achada no
roteiro"). Como cf_comum não pode ser mexido (entra no hash dos vídeos aprovados), esta cena monta o
próprio `render` com os MESMOS passos de `cf_comum.fazer_render` (cópia do `fazer_render_tolerante`
do cf_fixador_circular, copiada e não importada), só tirando a pontuação colada na palavra da voz
antes de alinhar. Quando o cf_comum ganhar essa limpeza, esta cena volta para
`render = fazer_render(...)`.
"""
import math
import os
import re

import skia

from . import som, voz as _voz
from .base import codificar, previas as _previas
from .cf_alongamento import (BG_IN, BG_OUT, F_BLACK, OSSO_C, OURO, PELE, VERMELHO, H, W, brilhos, clamp, e_back,
                             e_in_back, e_inout, e_out, fundo, larg_texto, lerp, lerpc, paint, prog)
from .cf_comum import (alinhar, ancoras, capa, carimbo, comprimir, interface, montar_blocos,
                       selo_como_funciona)

ANCORAS = {
    "torta": ("torta", 1, False), "fase": ("fase", 1, False), "cronograma": ("cronograma", 1, False),
    "dois": ("dois", 1, False), "arquear": ("arquear", 1, False), "perna2": ("perna", 2, False),
    "cowboy": ("cowboy", 1, False), "inverte": ("inverte", 1, False), "tres": ("três", 1, False),
    "vira": ("vira", 1, False), "x": ("x", 1, False), "seis": ("seis", 1, False),
    "alinhar": ("alinhar", 1, False), "sozinha": ("sozinha", 1, False), "juntas": ("juntas", 1, False),
    "desenv": ("desenvolvimento", 1, False), "alerta": ("alerta", 1, False), "lado": ("lado", 1, False),
    "doi": ("dói", 1, False), "piora": ("piora", 1, False), "avaliar": ("avaliar", 1, False),
    "causa": ("causa", 1, False), "raquitismo": ("raquitismo", 1, False), "manda": ("manda", 1, False),
}
DESTAQUE = {"torta", "fase", "cronograma", "dois", "arquear", "fora", "cowboy", "inverte", "três", "quatro", "x",
            "seis", "sete", "sozinha", "juntas", "desenvolvimento", "alerta", "lado", "dói", "piora", "avaliar",
            "causa", "raquitismo"}

# ------------------------------------------------------------------ textos da tela (TODOS estão em ep["tela"])
T_TORTA = "PERNA TORTA"
T_FASE = "QUASE SEMPRE É FASE"
T_CRONO = "CRONOGRAMA"
T_IDADES = ("ATÉ POR VOLTA DOS 2 ANOS", "DOS 3 AOS 4 ANOS", "POR VOLTA DOS 6 A 7 ANOS")
T_ARQ = "ARQUEADA PARA FORA"
T_O, T_VARO = "PERNA EM O", "VARO"
T_INV = "INVERTE"
T_X, T_VALGO = "EM X", "VALGO"
T_SOZ = "COSTUMA ALINHAR SOZINHA"
T_JUNTAS = "AS DUAS MUDAM JUNTAS"
T_DESENV = "DESENVOLVIMENTO"
T_ALERTA = "O ALERTA"
T_ITENS = ("SÓ DE UM LADO", "DÓI", "PIORA EM VEZ DE ALINHAR")
T_AVALIAR = "VALE AVALIAR"
T_CAUSA = "PODE TER UMA CAUSA"
T_RAQ = "RAQUITISMO"

PELE_CL, PELE_ESC, PELE_LINHA = "#F7CDB8", "#DA987E", "#B9765E"
SHORT, SHORT_CL, SHORT_ESC = "#4C86C6", "#6FA3DA", "#3A6FA8"
FUNDO_CARTAO = "#0B1824"
AZUL = "#9CC9FF"
CHAPEU, CHAPEU_ESC, CHAPEU_FITA = "#B07A3E", "#7E5427", "#4A3018"


def _alfa(a):
    p = skia.Paint()
    p.setAlphaf(clamp(a))
    return p


def _c(h, a=255):
    h = h.lstrip("#")
    return skia.ColorSetARGB(int(a), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


# ------------------------------------------------------------------ setas e rótulos (copiados do cf_pe_virado)
def ponta(cv, x, y, ang, tam, cor, a):
    p = skia.Path()
    p.moveTo(x + tam * math.cos(ang), y + tam * math.sin(ang))
    p.lineTo(x + tam * 0.75 * math.cos(ang + 2.45), y + tam * 0.75 * math.sin(ang + 2.45))
    p.lineTo(x + tam * 0.75 * math.cos(ang - 2.45), y + tam * 0.75 * math.sin(ang - 2.45))
    p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))


def seta_pts(cv, pts, cor, a, larg=7, tam=22):
    if a <= 0 or len(pts) < 2:
        return
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    cv.drawPath(p, paint(cor, int(90 * a), "stroke", larg + 8, blur=6))
    cv.drawPath(p, paint(cor, int(255 * a), "stroke", larg))
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    ponta(cv, x1, y1, math.atan2(y1 - y0, x1 - x0), tam, cor, a)


def seta_arco(cv, cx, cy, rx, ry, a0, a1, cor, a, larg=7, tam=22):
    n = 20
    pts = [(cx + rx * math.cos(math.radians(lerp(a0, a1, k / n))), cy + ry * math.sin(math.radians(lerp(a0, a1, k / n))))
           for k in range(n + 1)]
    seta_pts(cv, pts, cor, a, larg, tam)


def chip(cv, s, x, y, cor, a, tam=40, borda=None, fundo_a=220, nota=None):
    """Rótulo solto centrado em x; y = linha de base. `nota` = x de um biquinho no topo do chip."""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    r = skia.Rect(x - lw / 2 - 24, y - tam * 1.05, x + lw / 2 + 24, y + tam * 0.34)
    rr = skia.RRect.MakeRectXY(r, 16, 16)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(fundo_a * a)))
    if nota is not None:
        nx = clamp(nota, r.left() + 26, r.right() - 26)
        p = skia.Path(); p.moveTo(nx - 13, r.top() + 1); p.lineTo(nx, r.top() - 14); p.lineTo(nx + 13, r.top() + 1); p.close()
        cv.drawPath(p, paint(borda or cor, int(255 * a)))
    cv.drawRRect(rr, paint(borda or cor, int(255 * a), "stroke", 3))
    cv.drawString(s, x - lw / 2, y, f, paint(cor, int(255 * a)))


def rotulo_lado(cv, s, x, y, xa, ya, cor, a, tam=36):
    """Rótulo à direita da cena: caixa OPACA e fio que termina na borda esquerda da caixa (nunca
    risca o texto). (x, y) = canto esquerdo / linha de base."""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    cv.drawLine(xa, ya, x, y - tam * 0.36, paint(cor, int(210 * a), "stroke", 2.5))
    cv.drawCircle(xa, ya, 7, paint(FUNDO_CARTAO, int(220 * a)))
    cv.drawCircle(xa, ya, 5.5, paint(cor, int(255 * a)))
    rr = skia.RRect.MakeRectXY(skia.Rect(x, y - tam * 1.1, x + lw + 30, y + tam * 0.32), 14, 14)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(230 * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 2.5))
    cv.drawString(s, x + 15, y, f, paint(cor, int(255 * a)))


def etiqueta(cv, s, x, y, a, cor=AZUL, tam=32):
    """Etiqueta pequena (o nome técnico: VARO / VALGO), em pílula, sem fio."""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    rr = skia.RRect.MakeRectXY(skia.Rect(x, y - tam * 1.02, x + lw + 32, y + tam * 0.34), 20, 20)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(220 * a)))
    cv.drawRRect(rr, paint(cor, int(220 * a), "stroke", 2))
    cv.drawString(s, x + 16, y, f, paint(cor, int(255 * a)))


# ------------------------------------------------------------------ pernas de desenho (vista de frente)
WX, WY = 540, 730                 # ponto do mundo que a câmera põe em (X, Y)
YH, YK, YA = 470, 720, 950        # quadril (sob o short), joelho, tornozelo
HX = 100                          # meia distância entre os quadris: NUNCA muda (o desenho não cresce)
LARG = ((0.0, 66), (0.2, 60), (0.42, 47), (0.5, 50), (0.58, 45), (0.69, 50), (0.84, 39), (1.0, 31))
N_PTS = 36
PE_L, PE_W, K_PISO = 128, 84, 0.62


def afast(v):
    """v = +1 perna em O (varo), 0 reta, -1 em X (valgo); 0.8 = O da fase normal; 1.6 = a 'piora'.
    -> (quadril, joelho, tornozelo): distância de cada um até o meio. Só a FORMA muda."""
    if v >= 0:
        return HX, lerp(92, 140, v), max(48.0, lerp(80, 56, v))
    return HX, lerp(92, 47, -v), lerp(80, 125, -v)


def eixo(sgn, v):
    hx, kx, ax = afast(v)
    q = (WX + sgn * hx, YH); k = (WX + sgn * kx, YK); t = (WX + sgn * ax, YA)
    c = (2 * k[0] - (q[0] + t[0]) / 2, 2 * k[1] - (q[1] + t[1]) / 2)    # a curva passa pelo joelho
    return q, c, t


def bz(e, s):
    (x0, y0), (x1, y1), (x2, y2) = e; u = 1 - s
    return u * u * x0 + 2 * u * s * x1 + s * s * x2, u * u * y0 + 2 * u * s * y1 + s * s * y2


def bz_t(e, s):
    (x0, y0), (x1, y1), (x2, y2) = e
    tx = 2 * (1 - s) * (x1 - x0) + 2 * s * (x2 - x1); ty = 2 * (1 - s) * (y1 - y0) + 2 * s * (y2 - y1)
    n = math.hypot(tx, ty) or 1.0
    return tx / n, ty / n


def meia(s):
    for (s0, w0), (s1, w1) in zip(LARG, LARG[1:]):
        if s <= s1:
            return lerp(w0, w1, e_inout(clamp((s - s0) / (s1 - s0))))
    return LARG[-1][1]


def perna_path(sgn, v):
    e = eixo(sgn, v)
    esq, dir_ = [], []
    for i in range(N_PTS + 1):
        s = i / N_PTS
        cx, cy = bz(e, s); tx, ty = bz_t(e, s); nx, ny = -ty, tx; w = meia(s)
        esq.append((cx + nx * w, cy + ny * w)); dir_.append((cx - nx * w, cy - ny * w))
    p = skia.Path(); p.moveTo(*esq[0])
    for q in esq[1:]:
        p.lineTo(*q)
    tx, ty = bz_t(e, 1.0); k = meia(1.0) * 1.3
    p.cubicTo(esq[-1][0] + tx * k, esq[-1][1] + ty * k, dir_[-1][0] + tx * k, dir_[-1][1] + ty * k, *dir_[-1])
    for q in reversed(dir_[:-1]):
        p.lineTo(*q)
    p.close()
    return p, e


def pe_forma(x, y, lado):
    """Pé de frente saindo do tornozelo (encurtado); dedão do lado de dentro (lado = +1 na perna da
    esquerda da tela)."""
    p = skia.Path(); n = 48
    for i in range(n):
        ph = 2 * math.pi * i / n
        cu, su = math.cos(ph), math.sin(ph)
        u = math.copysign(abs(cu) ** 0.7, cu)
        aa = lerp(-20, PE_L, (u + 1) / 2)
        b = (PE_W / 2) * math.copysign(abs(su) ** 0.7, su) * (0.80 + 0.20 * (u + 1) / 2)
        (p.moveTo if i == 0 else p.lineTo)(x + b, y + aa * K_PISO)
    p.close()
    dedos = [(x + f * PE_W / 2 * lado, y + (PE_L - 6 + da) * K_PISO, r) for da, f, r in
             ((-2, 0.62, 13.5), (4, 0.27, 11), (4, -0.06, 10.5), (2, -0.38, 9.5), (-4, -0.66, 8.5))]
    return p, dedos


def pele_perna(cv, pth, e, k):
    """Pele opaca com sombra nas bordas e um brilho que ACOMPANHA a curva da perna."""
    cv.drawPath(pth, paint(PELE))
    cv.save(); cv.clipPath(pth, skia.ClipOp.kIntersect, True)
    cv.drawPath(pth, paint(PELE_ESC, 215, "stroke", 30, blur=12))
    hl = skia.Path()
    for i in range(N_PTS + 1):
        s = i / N_PTS
        cx, cy = bz(e, s); tx, ty = bz_t(e, s); w = meia(s) * 0.3
        (hl.moveTo if i == 0 else hl.lineTo)(cx - ty * w, cy + tx * w)
    cv.drawPath(hl, paint(PELE_CL, 210, "stroke", 30, blur=12))
    cv.restore()
    cv.drawPath(pth, paint(PELE_LINHA, 230, "stroke", 3.2 * k))
    kx, ky = bz(e, 0.5); tx, ty = bz_t(e, 0.5)                  # dobrinha do joelho
    cv.save(); cv.translate(kx, ky); cv.rotate(math.degrees(math.atan2(ty, tx)) - 90)
    cv.drawArc(skia.Rect(-20, -8, 20, 16), 25, 130, False, paint(PELE_LINHA, 140, "stroke", 3 * k))
    cv.restore()


def pe(cv, x, lado, k):
    pth, dedos = pe_forma(x, YA, lado)
    sh = skia.GradientShader.MakeLinear([skia.Point(x - 60, 0), skia.Point(x + 60, 0)],
                                        [_c(PELE_ESC), _c(PELE), _c(PELE_CL), _c(PELE), _c(PELE_ESC)],
                                        [0.0, 0.22, 0.5, 0.78, 1.0])
    cv.drawPath(pth, paint(PELE, shader=sh))
    cv.drawPath(pth, paint(PELE_LINHA, 230, "stroke", 3.2 * k))
    for dx, dy, r in dedos:
        cv.drawCircle(dx, dy, r, paint(PELE_CL))
        cv.drawCircle(dx, dy, r, paint(PELE_LINHA, 230, "stroke", 2.6 * k))
    return pth, dedos


def shorts(cv, k):
    p = skia.Path()
    p.moveTo(344, 424); p.lineTo(736, 424); p.lineTo(764, 568); p.lineTo(562, 574); p.lineTo(540, 532)
    p.lineTo(518, 574); p.lineTo(316, 568); p.close()
    pt = paint(SHORT); pt.setPathEffect(skia.CornerPathEffect.Make(18))
    cv.drawPath(p, paint("#000000", 70, blur=10))
    cv.drawPath(p, pt)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(342, 420, 738, 452), 14, 14), paint(SHORT_CL))
    cv.drawLine(540, 456, 540, 508, paint(SHORT_ESC, 255, "stroke", 3 * k))


def par(cv, vE, vD, s_cam, verm=0.0, fantasma=None, fant_a=0.0, t=0.0):
    """O par de pernas no mundo. `verm`: contorno vermelho fino na perna da DIREITA (a torta do
    alerta); `fantasma`: v da forma anterior dessa perna, tracejada ao lado para comparar."""
    k = (0.92 / s_cam) ** 0.6
    pernas = [perna_path(-1, vE), perna_path(1, vD)]
    for (_, e) in pernas:
        ax = e[2][0]
        cv.drawOval(skia.Rect(ax - 62, YA + 52, ax + 62, YA + 104), paint("#000000", 70, blur=12))
    if fantasma is not None and fant_a > 0:          # ANTES das pernas: só aparece a parte fora do contorno novo
        g, _ = perna_path(1, fantasma)
        pg = paint("#FFFFFF", int(200 * fant_a), "stroke", 3.5)
        pg.setPathEffect(skia.DashPathEffect.Make([14, 10], -t * 18))
        cv.drawPath(g, pg)
    pes = [pe(cv, pernas[0][1][2][0], 1, k), pe(cv, pernas[1][1][2][0], -1, k)]
    for pth, e in pernas:
        pele_perna(cv, pth, e, k)
    if verm > 0:
        uni = skia.Op(pernas[1][0], pes[1][0], skia.PathOp.kUnion_PathOp)
        cv.drawPath(uni, paint(VERMELHO, int(110 * verm), "stroke", 14, blur=7))
        cv.drawPath(uni, paint(VERMELHO, int(255 * verm), "stroke", 4.5))
    shorts(cv, k)


# ------------------------------------------------------------------ o tracejado dourado (O, X, retas)
def traco(cv, pth, a, s_cam, pr=1.0, t=0.0, cor=OURO):
    if a <= 0 or pr <= 0:
        return
    if pr < 1:
        m = skia.PathMeasure(pth, False); seg = skia.Path()
        m.getSegment(0, m.getLength() * pr, seg, True); pth = seg
    k = 1 / s_cam
    cv.drawPath(pth, paint(cor, int(70 * a), "stroke", 18 * k, blur=10 * k))
    for c, al, lw in ((FUNDO_CARTAO, 170, 10.5), (cor, 255, 6)):
        p = paint(c, int(al * a), "stroke", lw * k)
        p.setPathEffect(skia.DashPathEffect.Make([22 * k, 13 * k], -t * 22 * k))
        cv.drawPath(pth, p)


def path_o(v, s0=0.25, s1=0.965, folga=15):
    """O vão entre as duas pernas, contornado por dentro (o 'O' que as pernas desenham)."""
    pts = {}
    for sgn in (-1, 1):
        e = eixo(sgn, v); lst = []
        for i in range(25):
            s = lerp(s0, s1, i / 24)
            cx, cy = bz(e, s); tx, ty = bz_t(e, s); nx, ny = -ty, tx; w = meia(s) + folga
            lst.append((cx + sgn * nx * w, cy + sgn * ny * w))
        pts[sgn] = lst
    p = skia.Path(); p.moveTo(*pts[-1][0])
    for q in pts[-1][1:]:
        p.lineTo(*q)
    yb = max(pts[-1][-1][1], pts[1][-1][1])
    p.quadTo(WX, yb + 34, *pts[1][-1])
    for q in reversed(pts[1][:-1]):
        p.lineTo(*q)
    yt = min(pts[-1][0][1], pts[1][0][1])
    p.quadTo(WX, yt - 30, *pts[-1][0])
    p.close()
    return p


def path_x(vE, vD, m):
    """As duas linhas do X (quadril de um lado -> tornozelo do outro); `m` leva cada uma para a
    própria perna: viram duas retas paralelas."""
    q1, _, t1 = eixo(-1, vE); q2, _, t2 = eixo(1, vD)
    p = skia.Path()
    for q, ta, tb in ((q1, t2, t1), (q2, t1, t2)):
        fx, fy = lerp(ta[0], tb[0], m), lerp(ta[1], tb[1], m)
        dx, dy = fx - q[0], fy - q[1]
        p.moveTo(q[0] + dx * 0.22, q[1] + dy * 0.22); p.lineTo(q[0] + dx * 1.03, q[1] + dy * 1.03)
    return p


# ------------------------------------------------------------------ câmera
CAM1 = (0.92, 540, 790)
SLOTS = ((0.46, 250, 600), (0.46, 540, 600), (0.46, 830, 600))
CAM_AL = (0.80, 540, 690)


def aplica(cv, cam):
    s, x, y = cam
    cv.translate(x, y); cv.scale(s, s); cv.translate(-WX, -WY)


def na_tela(cam, x, y):
    s, X, Y = cam
    return X + (x - WX) * s, Y + (y - WY) * s


def lerp_cam(a, b, k):
    return tuple(lerp(a[i], b[i], k) for i in range(3))


def cam_principal(t, T):
    s, x, y = CAM1
    s += 0.03 * e_inout(prog(t, T["arquear"], T["cowboy"] + 0.4)) - 0.03 * e_inout(prog(t, T["inverte"], T["inverte"] + 1.2))
    return lerp_cam((s, x, y), SLOTS[2], e_inout(prog(t, T["juntas"] - 0.05, T["juntas"] + 0.7)))


def v_principal(t, T):
    v = 0.45                                                             # capa: já um pouco em O
    v = lerp(v, 0.8, e_inout(prog(t, T["arquear"], T["arquear"] + 0.7)))   # O da fase: curva MODERADA
    v = lerp(v, -1.0, e_inout(prog(t, T["inverte"] + 0.1, T["inverte"] + 2.0)))   # devagar: passa da reta
    return lerp(v, 0.0, e_inout(prog(t, T["alinhar"], T["alinhar"] + 0.8)))


def v_alerta(t, T):
    """Volta em O (a MESMA curva da fase normal, 0.8); no 'lado' a da esquerda alinha e a da direita
    CONTINUA arqueada; na 'piora' ela passa BEM da curva normal (1.6: joelho ~95 px fora da linha
    quadril-tornozelo contra ~50 px na fase normal), para o alerta não parecer igual ao normal."""
    k = e_inout(prog(t, T["lado"] - 0.05, T["lado"] + 0.55))
    vd = lerp(0.8, 1.6, e_inout(prog(t, T["piora"] + 0.15, T["piora"] + 0.85)))
    return lerp(0.8, 0.0, k), vd


# ------------------------------------------------------------------ calendário (folhas VAZIAS, sem número)
PAG_X = (250, 540, 830)
PAG_Y = 278


def pagina(cv, x, y, a, luz, t, t_luz, esc=1.0, cab_cor=OURO):
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    w2, h2 = 48, 46
    if luz > 0:
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-w2 - 12, -h2 - 12, w2 + 12, h2 + 12), 22, 22),
                     paint(cab_cor, int(130 * a * luz), blur=16))
    corpo = skia.RRect.MakeRectXY(skia.Rect(-w2, -h2, w2, h2), 12, 12)
    cv.drawRRect(corpo, paint("#000000", int(70 * a), blur=8))
    cv.drawRRect(corpo, paint(lerpc("#7D8C9B", "#EEF3F8", 0.35 + 0.65 * luz), int(255 * a)))
    cv.save(); cv.clipRRect(corpo, skia.ClipOp.kIntersect, True)
    cv.drawRect(skia.Rect(-w2, -h2, w2, -h2 + 24), paint(lerpc("#4E5F70", cab_cor, luz), int(255 * a)))
    for i in range(3):
        cv.drawLine(-34, -h2 + 44 + i * 16, 34, -h2 + 44 + i * 16, paint("#9AA8B5", int(200 * a), "stroke", 4))
    kf = prog(t, t_luz, t_luz + 0.4)
    if 0 < kf < 1:                                    # a folha de cima vira uma vez, para cima
        cv.save(); cv.translate(0, -h2 + 24); cv.scale(1, 1 - e_inout(kf))
        cv.drawRect(skia.Rect(-w2, 0, w2, 2 * h2 - 24), paint("#C9D3DC", int(255 * a)))
        for i in range(3):
            cv.drawLine(-34, 20 + i * 16, 34, 20 + i * 16, paint("#8A98A6", int(220 * a), "stroke", 4))
        cv.restore()
    cv.restore()
    for xx in (-24, 24):
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(xx - 4, -h2 - 9, xx + 4, -h2 + 9), 3, 3), paint("#5E7186", int(255 * a)))
    cv.restore()


def trilha_calendario(cv, t, T):
    a = prog(t, T["cronograma"], T["cronograma"] + 0.35) * (1 - prog(t, T["alerta"] - 0.1, T["alerta"] + 0.3))
    if a <= 0:
        return
    k = e_out(prog(t, T["cronograma"], T["cronograma"] + 0.6))
    p = skia.Path(); p.moveTo(PAG_X[0], PAG_Y); p.lineTo(lerp(PAG_X[0], PAG_X[2], k), PAG_Y)
    pt = paint(OURO, int(170 * a), "stroke", 5); pt.setPathEffect(skia.DashPathEffect.Make([16, 12], -t * 20))
    cv.drawPath(p, pt)
    for xm in ((PAG_X[0] + PAG_X[1]) / 2, (PAG_X[1] + PAG_X[2]) / 2):
        if lerp(PAG_X[0], PAG_X[2], k) > xm + 20:
            ponta(cv, xm + 14, PAG_Y, 0.0, 20, OURO, a)
    for i, (x, chave) in enumerate(zip(PAG_X, ("dois", "tres", "seis"))):
        ent = e_back(prog(t, T["cronograma"] + 0.12 * i, T["cronograma"] + 0.12 * i + 0.45))
        luz = prog(t, T[chave], T[chave] + 0.3)
        pulso = 1 + 0.08 * math.sin(math.pi * prog(t, T[chave], T[chave] + 0.45))
        pagina(cv, x, PAG_Y, a * clamp(ent * 2), luz, t, T[chave], esc=(0.6 + 0.4 * ent) * pulso)
        brilhos(cv, x, PAG_Y, t, T[chave] + 0.1, n=10, raio=95)


def rotulo_idade(cv, t, T):
    """Uma frase de idade por vez, embaixo da folha acesa (com biquinho apontando a folha)."""
    fim = 1 - prog(t, T["juntas"] - 0.1, T["juntas"] + 0.25)
    itens = ((T_CRONO, None, T["cronograma"], T["dois"]), (T_IDADES[0], 0, T["dois"], T["tres"]),
             (T_IDADES[1], 1, T["tres"], T["seis"]), (T_IDADES[2], 2, T["seis"], 1e9))
    for s, i, t0, t1 in itens:
        a = prog(t, t0 + 0.05, t0 + 0.3) * (1 - prog(t, t1 - 0.05, t1 + 0.12)) * fim
        if a <= 0:
            continue
        tam = 38
        meio = (larg_texto(s, F_BLACK, tam) * 1.1 + 48) / 2               # folga para a Roboto da nuvem
        x = 540 if i is None else clamp(PAG_X[i], 40 + meio, 1040 - meio)
        dy = 12 * (1 - e_out(prog(t, t0 + 0.05, t0 + 0.3)))
        chip(cv, s, x, 412 + dy, "#FFFFFF", a, tam=tam, borda=OURO, nota=None if i is None else PAG_X[i])


# ------------------------------------------------------------------ ícones
def chapeu(cv, x, y, esc, a, ang=0.0):
    """Chapéu de cowboy simples, de desenho (ícone da expressão, nunca na criança)."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.rotate(ang); cv.scale(esc, esc)
    aba = skia.Path()
    aba.moveTo(-78, -6); aba.cubicTo(-60, 22, 60, 22, 78, -6)
    aba.cubicTo(84, -16, 70, -20, 62, -12); aba.cubicTo(30, 8, -30, 8, -62, -12)
    aba.cubicTo(-70, -20, -84, -16, -78, -6); aba.close()
    copa = skia.Path()
    copa.moveTo(-40, 0); copa.cubicTo(-46, -30, -40, -58, -26, -62); copa.cubicTo(-14, -64, -8, -52, 0, -50)
    copa.cubicTo(8, -52, 14, -64, 26, -62); copa.cubicTo(40, -58, 46, -30, 40, 0); copa.close()
    cv.drawPath(copa, paint("#000000", int(70 * a), blur=8))
    cv.drawPath(copa, paint(CHAPEU, int(255 * a)))
    cv.drawPath(copa, paint(CHAPEU_ESC, int(255 * a), "stroke", 3))
    cv.drawLine(0, -48, 0, -22, paint(CHAPEU_ESC, int(160 * a), "stroke", 3))
    cv.save(); cv.clipPath(copa, skia.ClipOp.kIntersect, True)
    cv.drawRect(skia.Rect(-50, -16, 50, -4), paint(CHAPEU_FITA, int(255 * a)))
    cv.restore()
    cv.drawPath(aba, paint(CHAPEU, int(255 * a)))
    cv.drawPath(aba, paint(CHAPEU_ESC, int(255 * a), "stroke", 3))
    cv.restore()


def raio(cv, x, y, esc, a):
    """Ícone de dor: raio vermelho discreto (solto, não aponta lugar nenhum do corpo)."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    p = skia.Path()
    p.moveTo(8, -46); p.lineTo(-20, 4); p.lineTo(-2, 4); p.lineTo(-12, 46); p.lineTo(22, -10); p.lineTo(4, -10)
    p.lineTo(16, -46); p.close()
    pt = paint(VERMELHO, int(255 * a)); pt.setPathEffect(skia.CornerPathEffect.Make(4))
    cv.drawPath(p, paint(VERMELHO, int(100 * a), blur=12))
    cv.drawPath(p, pt)
    cv.drawPath(p, paint("#FFD3D4", int(170 * a), "stroke", 2))
    cv.restore()


def check_redondo(cv, x, y, r, pr, a):
    if a <= 0:
        return
    cv.drawCircle(x, y, r + 10, paint(OURO, int(90 * a), blur=14))
    cv.drawCircle(x, y, r, paint(FUNDO_CARTAO, int(235 * a)))
    cv.drawCircle(x, y, r, paint(OURO, int(255 * a), "stroke", 5))
    if pr > 0:
        p = skia.Path(); p.moveTo(x - r * 0.45, y + r * 0.02)
        p.lineTo(x - r * 0.45 + r * 0.3 * min(1, pr * 2), y + r * 0.02 + r * 0.3 * min(1, pr * 2))
        if pr > 0.5:
            q = (pr - 0.5) * 2
            p.lineTo(x - r * 0.15 + r * 0.62 * q, y + r * 0.32 - r * 0.7 * q)
        cv.drawPath(p, paint(OURO, int(255 * a), "stroke", 8))


# ------------------------------------------------------------------ 1ª parte: O -> X -> reta
def mundo_principal(cv, t, T, cam):
    v = v_principal(t, T); s = cam[0]
    par(cv, v, v, s)
    a_o = prog(t, T["arquear"] + 0.2, T["arquear"] + 0.35) * (1 - prog(t, T["inverte"], T["inverte"] + 0.3))
    traco(cv, path_o(v), a_o, s, e_inout(prog(t, T["arquear"] + 0.25, T["arquear"] + 0.95)), t)
    a_x = prog(t, T["vira"] - 0.05, T["vira"] + 0.1)
    m = e_inout(prog(t, T["alinhar"], T["alinhar"] + 0.8))
    traco(cv, path_x(v, v, m), a_x, s, e_inout(prog(t, T["vira"], T["vira"] + 0.6)), t)


X_ROT = 732                       # coluna dos rótulos da direita (caixa até ~1030 mesmo na Roboto)


def rotulos_principal(cv, t, T, cam):
    v = v_principal(t, T); _, kx, _ = afast(v)
    fim1 = 1 - prog(t, T["juntas"] - 0.2, T["juntas"] + 0.1)
    # PERNA TORTA (capa) -> apaga no "fase" -> sai no "cronograma"
    a = prog(t, T["torta"], T["torta"] + 0.25) * (1 - prog(t, T["cronograma"] - 0.1, T["cronograma"] + 0.2))
    dim = 1 - 0.45 * prog(t, T["fase"], T["fase"] + 0.3)
    xa, ya = na_tela(cam, WX + kx + meia(0.5) - 6, YK)
    rotulo_lado(cv, T_TORTA, X_ROT, 702, xa, ya, "#FFFFFF", a * dim, tam=34)
    # PERNA EM O + VARO + chapéu (saem no "inverte")
    sai = 1 - prog(t, T["inverte"] - 0.05, T["inverte"] + 0.25)
    xa, ya = na_tela(cam, WX + kx - meia(0.5) - 15, YK)
    a = prog(t, T["perna2"], T["perna2"] + 0.25) * sai
    rotulo_lado(cv, T_O, X_ROT, 702, xa, ya, OURO, a)
    etiqueta(cv, T_VARO, X_ROT, 764, prog(t, T["perna2"] + 0.2, T["perna2"] + 0.45) * sai)
    ent = e_back(prog(t, T["cowboy"], T["cowboy"] + 0.45))
    if t >= T["cowboy"]:
        voa = e_in_back(prog(t, T["inverte"] - 0.1, T["inverte"] + 0.4))
        bal = 6 * math.sin((t - T["cowboy"]) * 5) * (1 - prog(t, T["cowboy"] + 0.8, T["cowboy"] + 1.6))
        chapeu(cv, 880 + 260 * voa, 612 - 60 * voa, 1.0 * ent, clamp(ent * 2) * (1 - prog(t, T["inverte"] + 0.2, T["inverte"] + 0.4)),
               -10 + bal + 30 * voa)
        brilhos(cv, 880, 590, t, T["cowboy"] + 0.05, n=8, raio=90)
    # EM X + VALGO (do "vira" ao "alinhar")
    sai = 1 - prog(t, T["alinhar"] - 0.1, T["alinhar"] + 0.2)
    xa, ya = na_tela(cam, WX, YK - 22)
    rotulo_lado(cv, T_X, X_ROT, 702, xa, ya, OURO, prog(t, T["vira"], T["vira"] + 0.25) * sai)
    etiqueta(cv, T_VALGO, X_ROT, 764, prog(t, T["x"], T["x"] + 0.25) * sai)
    # linha de baixo (um chip por vez)
    chip(cv, T_ARQ, 540, 1182, "#FFFFFF", prog(t, T["arquear"], T["arquear"] + 0.25) * (1 - prog(t, T["inverte"] - 0.1, T["inverte"] + 0.1)),
         borda=OURO)
    chip(cv, T_INV, 540, 1182, OURO, prog(t, T["inverte"] + 0.1, T["inverte"] + 0.3) * (1 - prog(t, T["seis"] - 0.2, T["seis"])))
    a = prog(t, T["sozinha"], T["sozinha"] + 0.25) * fim1
    brilhos(cv, 540, 1100, t, T["sozinha"] + 0.05, n=12, raio=200)       # ANTES do chip: nunca sobre o texto
    chip(cv, T_SOZ, 540, 1182, "#FFFFFF", a, borda=OURO)
    # INVERTE: duas setas curvas douradas, espelhadas, varrendo duas vezes em volta dos joelhos
    for i in range(2):
        t0 = T["inverte"] + 0.1 + 0.95 * i
        k = e_out(prog(t, t0, t0 + 0.5)); a = prog(t, t0, t0 + 0.08) * (1 - prog(t, t0 + 0.75, t0 + 0.95))
        if a <= 0:
            continue
        for sgn in (-1, 1):
            xk, yk = na_tela(cam, WX + sgn * kx, YK)
            a0 = 165 if sgn < 0 else 15
            a1 = lerp(a0, 318 if sgn < 0 else -138, max(0.08, k))
            seta_arco(cv, xk, yk, 96, 96, a0, a1, OURO, a, larg=8, tam=24)
    # alinhou: brilho suave nas duas retas
    for sgn in (-1, 1):
        x, y = na_tela(cam, WX + sgn * 88, YK)
        brilhos(cv, x, y, t, T["alinhar"] + 0.75, n=8, raio=120)


# ------------------------------------------------------------------ "juntas": as três fases lado a lado
def fileira(cv, t, T):
    a = prog(t, T["juntas"] + 0.05, T["juntas"] + 0.3) * (1 - prog(t, T["alerta"] - 0.1, T["alerta"] + 0.3))
    if a <= 0:
        return
    for i, v in ((0, 0.8), (1, -1.0)):
        ent = e_back(prog(t, T["juntas"] + 0.3 + 0.15 * i, T["juntas"] + 0.75 + 0.15 * i))
        s, x, y = SLOTS[i]
        cam = (s * (0.5 + 0.5 * ent), x, y)
        al = a * clamp(ent * 2)
        if al <= 0:
            continue
        cv.saveLayer(skia.Rect(x - 220, 360, x + 220, 820), _alfa(al)) if al < 1 else cv.save()
        aplica(cv, cam)
        par(cv, v, v, cam[0])
        traco(cv, path_o(v) if v > 0 else path_x(v, v, 0.0), 1.0, cam[0], 1.0, t)
        cv.restore()


def setas_juntas(cv, t, T):
    """Setas espelhadas nos joelhos de cada fase: as duas pernas mudando no MESMO ritmo."""
    a = prog(t, T["juntas"] + 0.55, T["juntas"] + 0.8) * (1 - prog(t, T["alerta"] - 0.1, T["alerta"] + 0.2))
    if a <= 0:
        return
    vai = 7 * math.sin(2 * math.pi * 1.1 * (t - T["juntas"]))         # o mesmo vaivém nos dois lados
    for i, v, dentro in ((0, 0.8, True), (1, -1.0, False)):
        _, kx, _ = afast(v)
        for sgn in (-1, 1):
            xk, yk = na_tela(SLOTS[i], WX + sgn * (kx + meia(0.5)), YK)
            xo = xk + sgn * (12 + 40)
            xi = xk + sgn * 12
            if dentro:                                                   # O: joelhos vão para o meio
                seta_pts(cv, [(xo + sgn * vai, yk), (xi + sgn * vai, yk)], OURO, a, larg=6, tam=18)
            else:                                                        # X: joelhos vão para fora
                seta_pts(cv, [(xi - sgn * vai, yk), (xo - sgn * vai, yk)], OURO, a, larg=6, tam=18)
    s, x0, y0 = SLOTS[2]
    for sgn in (-1, 1):                                                  # retas: brilho nos dois joelhos juntos
        x, y = na_tela(SLOTS[2], WX + sgn * 92, YK)
        pul = 0.5 + 0.5 * math.sin(2 * math.pi * 1.1 * (t - T["juntas"]))
        cv.drawCircle(x, y, 20 + 6 * pul, paint(OURO, int(110 * a * pul), blur=10))
        cv.drawCircle(x, y, 5, paint("#FFF4CF", int(230 * a)))


def chave_juntas(cv, t, T):
    fim = 1 - prog(t, T["alerta"] - 0.1, T["alerta"] + 0.2)
    if t < T["juntas"] or fim <= 0:
        return
    a = prog(t, T["juntas"] + 0.3, T["juntas"] + 0.6) * fim
    k = e_out(prog(t, T["juntas"] + 0.3, T["juntas"] + 0.9))
    y = 788
    if a > 0:
        cv.drawLine(540 - 390 * k, y, 540 + 390 * k, y, paint(OURO, int(200 * a), "stroke", 4))
        for x in PAG_X:
            if abs(x - 540) <= 390 * k + 1:
                cv.drawLine(x, y, x, y - 22, paint(OURO, int(200 * a), "stroke", 4))
    brilhos(cv, 540, y, t, T["desenv"] + 0.1, n=14, raio=180)             # ANTES dos chips
    # entra só depois que o par principal já subiu para a 3ª folha (nunca sobre as canelas dele)
    chip(cv, T_JUNTAS, 540, 934, "#FFFFFF", prog(t, T["juntas"] + 0.5, T["juntas"] + 0.75) * fim, borda=OURO)
    a_ck = prog(t, T["desenv"], T["desenv"] + 0.2) * (1 - prog(t, T["alerta"] - 0.1, T["alerta"] + 0.2))
    if a_ck > 0:
        esc = e_back(prog(t, T["desenv"], T["desenv"] + 0.4))
        check_redondo(cv, 540, y, 40 * (0.5 + 0.5 * esc), e_out(prog(t, T["desenv"] + 0.15, T["desenv"] + 0.5)), a_ck)
        chip(cv, T_DESENV, 540, 1052, OURO, a_ck)


# ------------------------------------------------------------------ 2ª parte: o alerta
CK_X0, CK_Y0, CK_PASSO, CK_TAM = 262, 1028, 68, 36


def cam_alerta(t, T):
    k = e_back(prog(t, T["alerta"] + 0.2, T["alerta"] + 0.75))
    s, x, y = CAM_AL
    return s * (0.82 + 0.18 * k), x, y + 40 * (1 - e_out(prog(t, T["alerta"] + 0.2, T["alerta"] + 0.7)))


def mundo_alerta(cv, t, T, cam):
    vE, vD = v_alerta(t, T)
    verm = prog(t, T["lado"] + 0.1, T["lado"] + 0.4)
    fa = prog(t, T["piora"] + 0.15, T["piora"] + 0.45)
    par(cv, vE, vD, cam[0], verm=verm, fantasma=0.8 if fa > 0 else None, fant_a=fa, t=t)
    # dói: raio solto ao lado da canela, longe do corpo (piscando no começo, depois parado; sai antes da lupa)
    a_d = prog(t, T["doi"], T["doi"] + 0.12) * (1 - prog(t, T["causa"] - 0.15, T["causa"] + 0.1))
    if a_d > 0:
        pis = 0.75 + 0.25 * math.cos((t - T["doi"]) * 12) if t < T["doi"] + 1.0 else 1.0
        raio(cv, 985, 860, 1.05 * (0.6 + 0.4 * e_back(prog(t, T["doi"], T["doi"] + 0.35))), a_d * pis)
    # piora: seta vermelha para fora, no joelho
    k = e_out(prog(t, T["piora"] + 0.15, T["piora"] + 0.6))
    if k > 0:
        _, kx, _ = afast(vD)
        x0 = WX + kx + meia(0.5) + 18
        seta_pts(cv, [(x0, YK), (x0 + 90 * k + 4, YK)], VERMELHO, 1.0, larg=8, tam=24)


def checklist(cv, t, T):
    a = prog(t, T["alerta"] + 0.35, T["alerta"] + 0.65) * (1 - prog(t, T["manda"] - 0.45, T["manda"] - 0.1))
    if a <= 0:
        return
    dx = 40 * (1 - e_out(prog(t, T["alerta"] + 0.35, T["alerta"] + 0.75)))
    painel = skia.RRect.MakeRectXY(skia.Rect(CK_X0 - 30 + dx, CK_Y0 - 64, 1080 - CK_X0 + 70 + dx,
                                             CK_Y0 + 2 * CK_PASSO + 28), 22, 22)
    cv.drawRRect(painel, paint(FUNDO_CARTAO, int(160 * a)))
    cv.drawRRect(painel, paint(VERMELHO, int(110 * a), "stroke", 2.5))
    # sob o carimbo VALE AVALIAR os itens esmaecem (o carimbo fica limpo) e voltam inteiros depois
    esmaecer = 1 - 0.65 * prog(t, T["avaliar"], T["avaliar"] + 0.15) * (1 - prog(t, T["avaliar"] + 1.55, T["avaliar"] + 1.9))
    for i, (s, chave, atraso) in enumerate(zip(T_ITENS, ("lado", "doi", "piora"), (0.1, 0.05, 0.3))):
        y = CK_Y0 + i * CK_PASSO
        x = CK_X0 + dx
        ai = a * esmaecer * prog(t, T["alerta"] + 0.45 + 0.1 * i, T["alerta"] + 0.65 + 0.1 * i)
        caixa = skia.RRect.MakeRectXY(skia.Rect(x, y - 40, x + 46, y + 6), 10, 10)
        cv.drawRRect(caixa, paint(FUNDO_CARTAO, int(235 * ai)))
        t_ok = T[chave] + atraso
        cv.drawRRect(caixa, paint(VERMELHO, int(255 * ai * (0.55 + 0.45 * (t >= t_ok))), "stroke", 3.5))
        if t >= t_ok:
            pr = e_out(clamp((t - t_ok) / 0.3))
            p = skia.Path(); p.moveTo(x + 10, y - 18)
            p.lineTo(x + 10 + 11 * min(1, pr * 2), y - 18 + 11 * min(1, pr * 2))
            if pr > 0.5:
                q = (pr - 0.5) * 2
                p.lineTo(x + 21 + 20 * q, y - 7 - 28 * q)
            cv.drawPath(p, paint(VERMELHO, int(255 * ai), "stroke", 6))
            k2 = clamp((t - t_ok) / 0.25)
            f = skia.Font(F_BLACK, CK_TAM)
            cv.drawString(s, x + 64 + 24 * (1 - e_out(k2)), y - 3, f, paint("#FFFFFF", int(255 * ai * k2)))


def lupa(cv, t, T, cam):
    t0 = T["causa"] - 0.15
    if t < t0:
        return
    a = 1 - prog(t, T["manda"] - 0.45, T["manda"] - 0.1)
    if a <= 0:
        return
    _, vD = v_alerta(t, T); _, kx, _ = afast(vD)
    alvo = na_tela(cam, WX + kx, YK - 10)
    k = e_inout(prog(t, t0, t0 + 0.95))
    x = lerp(1250, alvo[0], k) + 4 * math.sin(t * 1.7)          # entra pela direita/baixo: só passa pela perna afetada
    y = lerp(900, alvo[1], k) + 3 * math.cos(t * 1.3)
    r, m = 122, 1.4
    cv.saveLayer(skia.Rect(x - r - 260, y - r - 30, W, y + r + 250), _alfa(a)) if a < 1 else cv.save()
    cv.save()
    clip = skia.Path(); clip.addCircle(x, y, r)
    cv.clipPath(clip, skia.ClipOp.kIntersect, True)
    # o mesmo fundo da cena (degradê do fundo() + o escurecido do alerta), só no disco da lente
    sh = skia.GradientShader.MakeRadial(skia.Point(W / 2, H * 0.42 + 40 * math.sin(t * 0.3)), H * 0.78,
                                        [_c(BG_IN), _c(BG_OUT)])
    cv.drawCircle(x, y, r + 2, paint(BG_IN, shader=sh))
    cv.drawCircle(x, y, r + 2, paint(BG_OUT, 100))
    cv.drawCircle(x, y, r + 2, paint("#FFFFFF", 24))                    # lente clara: só aumenta o desenho
    cv.translate(x, y); cv.scale(m, m); cv.translate(-x, -y)
    aplica(cv, cam)
    mundo_alerta(cv, t, T, cam)
    cv.restore()
    hx, hy = x + r * 0.71, y + r * 0.71
    cv.drawLine(hx + 4, hy + 4, hx + 80, hy + 80, paint("#000000", 80, "stroke", 30, blur=6))
    cv.drawLine(hx + 6, hy + 6, hx + 78, hy + 78, paint("#8A6512", 255, "stroke", 26))
    cv.drawLine(hx + 6, hy + 6, hx + 78, hy + 78, paint(OURO, 255, "stroke", 16))
    cv.drawCircle(x, y, r, paint("#000000", 80, "stroke", 20, blur=6))
    cv.drawCircle(x, y, r, paint(OURO, 255, "stroke", 13))
    cv.drawCircle(x, y, r - 8, paint("#FFF1C2", 120, "stroke", 2.5))
    cv.drawArc(skia.Rect(x - r * 0.72, y - r * 0.72, x + r * 0.72, y + r * 0.72), 200, 55, False,
               paint("#FFFFFF", 150, "stroke", 7))
    # RAQUITISMO: etiqueta marfim pendurada no CABO da lupa, à direita (fora das pernas)
    ar = prog(t, T["raquitismo"], T["raquitismo"] + 0.25)
    if ar > 0:
        xe, ye = 875, 905 + 10 * (1 - e_out(ar))
        cv.drawLine(hx + 78, hy + 78, xe, ye - 38, paint(OSSO_C, int(200 * ar), "stroke", 2.5))
        chip(cv, T_RAQ, xe, ye, OSSO_C, ar, tam=36, borda=OSSO_C, fundo_a=235)
    cv.restore()


def alerta(cv, t, T):
    a_pair = prog(t, T["alerta"] + 0.2, T["alerta"] + 0.38) * (1 - prog(t, T["manda"] - 0.35, T["manda"] + 0.1))
    if a_pair <= 0:
        return
    cam = cam_alerta(t, T)
    cv.saveLayer(skia.Rect(0, 380, W, 1000), _alfa(a_pair)) if a_pair < 1 else cv.save()
    aplica(cv, cam)
    mundo_alerta(cv, t, T, cam)
    cv.restore()
    # piora: uma folha do calendário vira (ao lado, do outro lado da perna)
    ap = prog(t, T["piora"] - 0.1, T["piora"] + 0.15) * (1 - prog(t, T["manda"] - 0.45, T["manda"] - 0.1))
    pagina(cv, 236, 560, ap, 1.0, t, T["piora"], esc=0.95 * (0.6 + 0.4 * e_back(prog(t, T["piora"] - 0.1, T["piora"] + 0.3))),
           cab_cor=VERMELHO)
    # topo: O ALERTA -> PODE TER UMA CAUSA
    sai = 1 - prog(t, T["manda"] - 0.45, T["manda"] - 0.1)
    k = e_back(prog(t, T["alerta"] + 0.1, T["alerta"] + 0.5))
    chip(cv, T_ALERTA, 540, lerp(285, 330, k), VERMELHO,
         clamp(k * 3) * (1 - prog(t, T["causa"] - 0.15, T["causa"] + 0.05)), tam=44, borda=VERMELHO)
    chip(cv, T_CAUSA, 540, 330, "#FFFFFF", prog(t, T["causa"], T["causa"] + 0.25) * sai, tam=40, borda=OURO)
    checklist(cv, t, T)
    brilhos(cv, 540, 1090, t, T["avaliar"] + 0.05, n=14, raio=200)       # ANTES do carimbo
    carimbo(cv, T_AVALIAR, 540, 1118, -6, T["avaliar"], t, dur=1.9)
    lupa(cv, t, T, cam)


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    esc = prog(t, T["alerta"] - 0.1, T["alerta"] + 0.4)              # o tom muda: escurece, sem virar preto
    if esc > 0:
        cv.drawRect(skia.Rect(0, 0, W, H), paint(BG_OUT, int(100 * esc)))

    trilha_calendario(cv, t, T)
    rotulo_idade(cv, t, T)

    # par principal: capa -> O -> X -> reta -> encolhe para a 3ª folha
    a_main = 1 - prog(t, T["alerta"] - 0.1, T["alerta"] + 0.3)
    if a_main > 0:
        cam = cam_principal(t, T)
        cv.saveLayer(skia.Rect(0, 360, W, 1120), _alfa(a_main)) if a_main < 1 else cv.save()
        aplica(cv, cam)
        mundo_principal(cv, t, T, cam)
        cv.restore()
        rotulos_principal(cv, t, T, cam)
    fileira(cv, t, T)
    setas_juntas(cv, t, T)
    chave_juntas(cv, t, T)

    brilhos(cv, 530, 845, t, T["fase"] + 0.05, n=14, raio=300)           # ANTES do carimbo
    carimbo(cv, T_FASE, 530, 872, -7, T["fase"], t, dur=T["cronograma"] - T["fase"] + 0.9)

    alerta(cv, t, T)

    capa(cv, t, T["fase"], ep["gancho"][0], ep["gancho"][1])
    selo_como_funciona(cv, prog(t, T["fase"] + 0.3, T["fase"] + 0.7) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface(cv, t, T, blocos, DESTAQUE)


def sons(T):
    ev = [(T["torta"] + 0.05, "pop", 0.45), (T["fase"] - 0.02, "thump", 0.85), (T["fase"] + 0.05, "shimmer", 0.6),
          (T["cronograma"], "whoosh", 0.4)]
    ev += [(T["cronograma"] + 0.12 * i + 0.2, "tick", 0.45) for i in range(3)]
    ev += [(T["dois"], "ping", 0.6), (T["arquear"], "whoosh", 0.45), (T["arquear"] + 0.3, "shimmer", 0.45),
           (T["perna2"], "pop", 0.45), (T["cowboy"], "pop", 0.7), (T["inverte"], "whoosh", 0.5),
           (T["inverte"] + 1.05, "whoosh", 0.3), (T["tres"], "ping", 0.6), (T["vira"], "shimmer", 0.6),
           (T["x"], "pop", 0.45), (T["seis"], "ping", 0.6), (T["alinhar"], "whoosh", 0.35),
           (T["alinhar"] + 0.75, "shimmer", 0.55), (T["sozinha"], "ding", 0.55),
           (T["juntas"], "whoosh", 0.4), (T["juntas"] + 0.34, "pop", 0.45), (T["juntas"] + 0.49, "pop", 0.45),
           (T["desenv"], "ding", 0.6), (T["desenv"] + 0.1, "shimmer", 0.55),
           (T["alerta"], "thump", 0.7), (T["lado"], "pop", 0.5), (T["lado"] + 0.1, "tick", 0.5),
           (T["doi"], "tick", 0.7), (T["piora"] + 0.3, "tick", 0.55), (T["piora"] + 0.2, "whoosh", 0.35),
           (T["avaliar"] - 0.02, "thump", 0.85), (T["causa"] - 0.1, "whoosh", 0.45), (T["raquitismo"], "pop", 0.5),
           (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def tempos_previa(T):
    return [0.0, T["torta"] + 1.0, T["fase"] + 0.5, T["dois"] + 0.6, T["cowboy"] + 0.6, T["inverte"] + 0.55,
            T["x"] + 0.5, T["sozinha"] + 0.6, T["desenv"] + 0.7, T["piora"] + 0.9, T["raquitismo"] + 0.9,
            T["manda"] + 1.4]


# ------------------------------------------------------------------ entrada única
_PONTA = re.compile(r"[.,:;!?—…]+$")


def fazer_render_tolerante(quadro_fn, mapa, sons_fn, tempos_fn, respiro_cta=1.6):
    """Os MESMOS passos de cf_comum.fazer_render, só que limpando a pontuação que o edge-tts às vezes
    cola na palavra ("X.") antes de alinhar com o roteiro (ver o docstring do módulo)."""
    def render(ep, mp4, tmp, previa=False):
        roteiro = "\n".join(ep["roteiro"])
        voz_bruta, palavras = _voz.narrar(roteiro, _voz.RITMO_COMO_FUNCIONA, os.path.join(tmp, "voz"))
        palavras = [dict(p, w=_PONTA.sub("", p["w"])) for p in palavras]
        voz_c, pal, tirado = comprimir(voz_bruta, palavras, respiro_cta=respiro_cta)
        pal = alinhar(pal, roteiro)
        T = ancoras(pal, mapa)
        print(f"{ep['id']}: silêncio cortado {tirado:.2f}s | duração final {T['total']:.2f}s")
        blocos = montar_blocos(pal)

        def quadro_t(cv, t):
            quadro_fn(cv, t, T, blocos, ep)

        if previa:
            return _previas(quadro_t, tempos_fn(T), tmp, ep["id"]), T["total"]
        wav = os.path.join(tmp, f"{ep['id']}_mix.wav")
        som.gravar_wav(wav, som.mixar(voz_c, T["total"], sons_fn(T), ganho_trilha=0.40))
        codificar(quadro_t, T["total"], wav, mp4)
        return mp4, T["total"]
    return render


# respiro antes da CTA: a etiqueta RAQUITISMO sob a lupa fica ~2,5 s na tela antes do "Manda".
render = fazer_render_tolerante(quadro, ANCORAS, sons, tempos_previa, respiro_cta=2.2)
