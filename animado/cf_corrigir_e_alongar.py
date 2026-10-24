# -*- coding: utf-8 -*-
"""COMO FUNCIONA — corrigir e alongar com o mesmo aparelho ("PERNA ARQUEADA E / 14 CM MAIS CURTA").
Caso real da literatura (Hong e colaboradores, Medicina (Kaunas) 2023), tratado por OUTRA equipe;
ilustração esquemática, nunca imagem do paciente.

Mesmo estilo das cenas aprovadas (fundo azul-petróleo com partículas, marfim, dourado, anéis/hastes/porcas
do fixador do piloto, rótulos com fio e ponto, calendário do cf_fratura_cola, brilhos, legenda karaokê,
CTA com aviãozinho). O desenho é a representação JÁ PUBLICADA deste caso (painel_triplo do ep302):
contorno de UMA perna com eixo tracejado; 4 anéis completos com hastes; placa reta por fora.
O que o verificador exigiu (lote5_cf/cf_corrigir_e_alongar_storyboard.json):
  * Nada de osso por dentro, fíbula, corte, fenda, metades, giro de anel, vão ou osso novo dourado: a
    fonte do caso não descreve o gesto nem onde o comprimento foi ganho. "Endireitou" = contorno e eixo
    passam de curvos a retos em passinhos, com a seta curva de correção; "alongou" = os 2 anéis de baixo
    descem em passinhos e o contorno entre os pares de anéis se estende junto.
  * Endireitar e alongar são SEQUENCIAIS na animação (nada sugere simultaneidade).
  * A cota "14 cm" some no "fixador" e NÃO volta: a cena nunca mostra quanto foi recuperado; nenhuma
    régua, contador de dias ou comparação lado a lado.
  * Nenhum pino, fio, parafuso, ferida ou pele atravessada; a placa é uma barra lisa, por fora.
  * Faixa "Caso real da literatura · tratado por outra equipe" e "ilustração esquemática" do quadro 0
    ao último (inclusive na CTA). No quadro 0 o gancho é o único texto grande.
  * Custo honesto em chips SEM check (rigidez no tornozelo; duas infecções no trajeto dos pinos, tratadas
    com antibiótico), com "cada caso é único" e a fonte.
Todo texto desenhado está em ep["tela"] (o render recusa o vídeo se não estiver).

Desvio do contrato (anotado, mesmo caso do cf_fixador_circular e do cf_pernas_x_o): o edge-tts devolve
"real." (com o ponto) na 1ª frase e o `alinhar` comum recusa o vídeo ("palavra da voz 'real.' não achada
no roteiro"). Como cf_comum não pode ser mexido (entra no hash dos vídeos aprovados), esta cena monta o
próprio `render` com os MESMOS passos de `cf_comum.fazer_render` (cópia do `fazer_render_tolerante` do
cf_fixador_circular, copiada e não importada), só tirando a pontuação colada na palavra da voz antes de
alinhar. Quando o cf_comum ganhar essa limpeza, esta cena volta para `render = fazer_render(...)`.
"""
import math
import os
import re

import skia

from . import som, voz as _voz
from .base import codificar, previas as _previas
from .cf_alongamento import (ACO, ACO_ESC, ACO_HL, CX, F_BLACK, F_SEMI, OSSO_C, OURO, W, C, brilhos, clamp,
                             e_back, e_in_back, e_inout, e_out, fundo, haste, larg_texto, lerp, lerpc, paint,
                             porca, prog, texto)
from .cf_comum import alinhar, ancoras, capa, comprimir, interface, montar_blocos, selo_como_funciona
from .cf_fratura_cola import calendario

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "perna": ("perna", 1, False), "arqueada": ("arqueada", 1, False), "catorze": ("catorze", 1, False),
    "caso": ("caso", 1, False), "causa": ("causa", 1, False), "infeccao": ("infecção", 1, False),
    "infancia": ("infância", 1, False), "vinte": ("vinte", 1, False), "chegou": ("chegou", 1, False),
    "fixador": ("fixador", 1, False), "duas": ("duas", 1, False), "endireitou": ("endireitou", 1, False), "alongou": ("alongou", 1, False),
    "milimetro": ("milímetro", 1, False), "quatro2": ("quatro", 2, False), "meses": ("meses", 1, False),
    "externa": ("externa", 1, False), "substituiu": ("substituiu", 1, False), "firmar": ("firmar", 1, False),
    "saiu": ("saiu", 1, False), "quinze": ("quinze", 1, False), "meses2": ("meses", 2, False),
    "custo": ("custo", 1, False), "rigidez": ("rigidez", 1, False), "tornozelo": ("tornozelo", 1, False),
    "manda": ("manda", 1, False),
}
DESTAQUE = {"arqueada", "catorze", "centímetros", "real", "infecção", "infância", "mancando", "fixador",
            "ilizarov", "endireitou", "alongou", "milímetro", "meses", "placa", "externa", "firmar", "saiu",
            "quinze", "honesto", "rigidez", "tornozelo"}

# ------------------------------------------------------------------ textos de tela (TODOS estão em ep["tela"])
FAIXA = ("Caso real da literatura", "tratado por outra equipe")
ESQUEMA = "ilustração esquemática"
T_ARQ, T_14, T_INF = "ARQUEADA", "14 cm", "infecção no osso"
T_INFANCIA, T_24, T_MANCANDO = "INFÂNCIA", "AOS 24 ANOS", "chegou ao hospital mancando"
T_FIX, T_DUAS, T_ENDI, T_ALON = "fixador de Ilizarov", "AS DUAS COISAS", "ENDIREITOU", "E ALONGOU"
T_1MM, T_DIA, T_4M = "1 MM", "por dia", "4 MESES"
T_PLACA, T_15M = "PLACA EXTERNA", "15 MESES DEPOIS"
T_CUSTO = "O CUSTO HONESTO"
CHIPS = ("neste caso: rigidez no tornozelo", "duas infecções no trajeto dos pinos", "tratadas com antibiótico")
T_UNICO, T_FONTE = "cada caso é único", "Hong e colaboradores, 2023"

AZUL = "#9CC9FF"
FUNDO_CARTAO = "#0B1824"

# ------------------------------------------------------------------ geometria (mundo, antes da câmera)
FOCO = 790                               # y do mundo que a câmera põe em `py`
Y_K, Y_A = 400, 920                      # topo da perna (some em degradê) e tornozelo (u = 0 .. 1)
SOLA_H = 43                              # do tornozelo à sola
BOW = 64                                 # quanto a perna arqueia (px no ápice, para a direita: o lado dos dedos)
EXT = 110                                # quanto o contorno se estende no alongamento (esquemático; NÃO vai à tela)
Y_AN = (480, 590, 740, 860)              # 4 anéis: 2 acima e 2 abaixo do ponto mais curvo (u = 0,5 -> y 660)
RX2, RY2 = 168, 38
X_HASTE = 124
X_PLACA = 174                            # a barra fica na distância dos anéis, por fora do contorno
COTA = (980, 1178)                       # a cota vazia abaixo da sola (14 cm, sem régua)
N_RETO, N_LONGO = 4, 8                   # passinhos (um clique cada; NÃO vão para a tela)
X_COL = 530                              # coluna da direita (depois que a câmera desliza)


# ------------------------------------------------------------------ tempo
def passos(x, n, suave=0.55):
    """0..1 em n passinhos (anda e para), sem número na tela."""
    k = clamp(x) * n; i = math.floor(k)
    if i >= n:
        return 1.0
    return (i + e_inout(clamp((k - i) / suave))) / n


def jan_reto(T):
    """Endireitar: da palavra 'endireitou' até logo antes de 'milímetro' (~1,3 s para 4 passinhos)."""
    return T["endireitou"] - 0.02, T["milimetro"] - 0.2


def jan_longo(T):
    """Alongar: casa os passinhos com 'Um milímetro por dia, por quatro meses' (~2,2 s para 8)."""
    return T["milimetro"] - 0.1, T["meses"] + 0.4


def bow_de(t, T):
    return BOW * (1 - passos(prog(t, *jan_reto(T)), N_RETO, 0.7))


def ext_de(t, T):
    return EXT * passos(prog(t, *jan_longo(T)), N_LONGO)


# ------------------------------------------------------------------ câmera
K0 = (540.0, 380 + (FOCO - Y_K) * 1.05, 1.05)               # capa: perna + cota abaixo do gancho
K1 = (540.0, 250 + (FOCO - Y_K) * 0.92, 0.92)                # o gancho saiu: sobe e abre espaço p/ a linha do tempo
K2 = (262.0, 245 + (FOCO - Y_K) * 1.2, 1.2)                  # o fixador chegou: aproxima e desliza p/ a esquerda (coluna)
K3 = (540.0, 620 + (FOCO - 737) * 0.9, 0.9)                  # o custo: recentra, a perna fica ao fundo


def camera(t, T):
    cur = K0
    for t0, t1, k in ((T["causa"] - 0.1, T["causa"] + 0.8, K1), (T["fixador"] - 0.1, T["fixador"] + 0.9, K2),
                      (T["custo"] - 0.1, T["custo"] + 0.8, K3)):
        a = e_inout(prog(t, t0, t1))
        if a > 0:
            cur = tuple(lerp(c, d, a) for c, d in zip(cur, k))
    tremor = 0.0
    for t0, forca in ((T["catorze"] + 0.05, 6), (T["externa"] + 0.5, 4)):
        k = t - t0
        if 0 <= k < 0.35:
            tremor += forca * math.sin(k * 70) * (1 - k / 0.35)
    px, py, s = cur
    return px + tremor, py, s


def na_tela(cam, x, y):
    px, py, s = cam
    return px + (x - CX) * s, py + (y - FOCO) * s


# ------------------------------------------------------------------ a perna (contorno marfim + eixo tracejado)
_MEIA = ((0.0, 90), (0.22, 102), (0.5, 88), (0.75, 68), (0.92, 50), (1.0, 52))


def meia(u):
    for (u0, h0), (u1, h1) in zip(_MEIA, _MEIA[1:]):
        if u <= u1:
            return lerp(h0, h1, e_inout(clamp((u - u0) / (u1 - u0))))
    return _MEIA[-1][1]


def y_de(u, ext):
    """y do mundo do ponto u da perna; o trecho entre o 2º e o 3º anel se estende no alongamento."""
    y0 = lerp(Y_K, Y_A, u)
    return y0 + ext * clamp((y0 - Y_AN[1]) / (Y_AN[2] - Y_AN[1]))


def x_de(u, bow):
    return CX + bow * math.sin(math.pi * u)


def perna_path(bow, ext, n=56):
    us = [k / n for k in range(n + 1)]
    p = skia.Path()
    p.moveTo(x_de(0, bow) - meia(0), y_de(0, ext))
    for u in us[1:]:
        p.lineTo(x_de(u, bow) - meia(u), y_de(u, ext))
    ya = y_de(1, ext); ca = x_de(1, bow); sola = ya + SOLA_H
    # pé simples, de lado, apontando para a direita (sem dedos, sem detalhe), como no painel publicado
    p.cubicTo(ca - 66, ya + 10, ca - 64, sola, ca - 30, sola)
    p.lineTo(ca + 150, sola)
    p.cubicTo(ca + 180, sola, ca + 182, ya + 30, ca + 150, ya + 24)
    p.cubicTo(ca + 112, ya + 14, ca + 56, ya + 18, ca + meia(1), ya)
    for u in reversed(us[:-1]):
        p.lineTo(x_de(u, bow) + meia(u), y_de(u, ext))
    p.close()
    return p


def eixo_path(bow, ext, u0, u1, n=48):
    p = skia.Path()
    if u1 <= u0:
        return p
    for k in range(n + 1):
        u = lerp(u0, u1, k / n)
        (p.moveTo if k == 0 else p.lineTo)(x_de(u, bow), y_de(u, ext))
    return p


def desenha_perna(cv, bow, ext, alfa, brilho, g_firme, t):
    """Contorno marfim com o topo dissolvendo no fundo (a perna continua para cima), eixo tracejado por
    dentro; `g_firme` (0..1): até onde o eixo já virou linha contínua."""
    if alfa <= 0:
        return
    pth = perna_path(bow, ext)
    y0, y1 = Y_K, y_de(1, ext) + SOLA_H
    caixa = skia.Rect(0, y0 - 60, W, y1 + 60)
    cv.saveLayer(caixa, None)
    cv.drawPath(pth, paint(OSSO_C, int(24 * alfa)))
    if brilho > 0:
        cv.drawPath(pth, paint(OSSO_C, int(150 * brilho * alfa), "stroke", 26, blur=14))
    cv.drawPath(pth, paint(OSSO_C, int(55 * alfa), "stroke", 14, blur=8))
    cv.drawPath(pth, paint(OSSO_C, int(235 * alfa), "stroke", 5))
    # eixo: contínuo até g_firme, tracejado depois
    if g_firme > 0:
        cv.drawPath(eixo_path(bow, ext, 0.0, g_firme), paint(OSSO_C, int(240 * alfa), "stroke", 5))
    if g_firme < 1:
        pe = paint(OSSO_C, int(175 * alfa), "stroke", 4)
        pe.setPathEffect(skia.DashPathEffect.Make([18, 12], -t * 8))
        cv.drawPath(eixo_path(bow, ext, g_firme, 1.0), pe)
    masc = skia.Paint(AntiAlias=True)
    masc.setShader(skia.GradientShader.MakeLinear([skia.Point(0, y0), skia.Point(0, y0 + 95)],
                                                  [skia.ColorSetARGB(0, 0, 0, 0), skia.ColorSetARGB(255, 0, 0, 0)]))
    masc.setBlendMode(skia.BlendMode.kDstIn)
    cv.drawRect(caixa, masc)
    cv.restore()


def arco_ouro(cv, bow, ext, pr, a, t):
    """Arco dourado tracejado por fora da curva (lado convexo), traçado de cima a baixo."""
    if a <= 0 or pr <= 0:
        return
    p = skia.Path(); n = 40
    for k in range(n + 1):
        u = lerp(0.1, 0.92, k / n)
        (p.moveTo if k == 0 else p.lineTo)(x_de(u, bow) + meia(u) + 36, y_de(u, ext))
    ytop = y_de(0.1, ext); ybot = y_de(0.92, ext)
    cv.save(); cv.clipRect(skia.Rect(0, ytop - 20, W, lerp(ytop, ybot, pr) + 6))
    cv.drawPath(p, paint(OURO, int(90 * a), "stroke", 16, blur=10))
    pe = paint(OURO, int(255 * a), "stroke", 6)
    pe.setPathEffect(skia.DashPathEffect.Make([22, 13], -t * 14))
    cv.drawPath(p, pe)
    cv.restore()


def seta_correcao(cv, bow, ext, a):
    """A pequena seta curva de correção do painel publicado do caso, em volta do ápice da curva."""
    if a <= 0:
        return
    cx, cy, r = x_de(0.5, bow), y_de(0.5, ext), 46
    ret = skia.Rect(cx - r, cy - r, cx + r, cy + r)
    cv.drawArc(ret, 240, -140, False, paint(OURO, int(90 * a), "stroke", 14, blur=8))
    cv.drawArc(ret, 240, -140, False, paint(OURO, int(255 * a), "stroke", 6))
    ang = math.radians(100)
    ex, ey = cx + r * math.cos(ang), cy + r * math.sin(ang)
    tx, ty = math.sin(ang), -math.cos(ang)                      # tangente no sentido anti-horário
    nx, ny = -ty, tx
    p = skia.Path(); p.moveTo(ex + tx * 16, ey + ty * 16)
    p.lineTo(ex - tx * 6 + nx * 12, ey - ty * 6 + ny * 12); p.lineTo(ex - tx * 6 - nx * 12, ey - ty * 6 - ny * 12)
    p.close(); cv.drawPath(p, paint(OURO, int(255 * a)))


def seta_dupla(cv, x, ya, yb, a):
    """Seta dupla vertical fina (o alongamento), ao lado dos anéis."""
    if a <= 0 or yb - ya < 20:
        return
    cv.drawLine(x, ya + 10, x, yb - 10, paint(OURO, int(80 * a), "stroke", 12, blur=7))
    cv.drawLine(x, ya + 10, x, yb - 10, paint(OURO, int(255 * a), "stroke", 4))
    for y, d in ((ya, 1), (yb, -1)):
        p = skia.Path(); p.moveTo(x, y); p.lineTo(x - 13, y + d * 20); p.lineTo(x + 13, y + d * 20); p.close()
        cv.drawPath(p, paint(OURO, int(255 * a)))


def cota(cv, x, y0, y1, a, t, t_pop):
    """Cota tracejada vertical abaixo da sola; recebe '14 cm' na palavra 'catorze' e pulsa uma vez."""
    if a <= 0:
        return
    k = t - t_pop
    acende = max(0.0, 1 - abs(k - 0.2) / 0.5) if k >= 0 else 0.0
    cor = lerpc("#DDE6EE", OURO, acende)
    pe = paint(cor, int(225 * a), "stroke", 4)
    pe.setPathEffect(skia.DashPathEffect.Make([16, 11], 0))
    cv.drawLine(x, y0, x, y1, pe)
    for yy in (y0, y1):
        cv.drawLine(x - 16, yy, x + 16, yy, paint(cor, int(235 * a), "stroke", 4))
    if k >= 0:
        esc = lerp(1.6, 1.0, e_out(clamp(k / 0.22))) + 0.08 * math.sin(math.pi * clamp((k - 0.3) / 0.35))
        lw = larg_texto(T_14, F_BLACK, 62); ym = (y0 + y1) / 2
        cv.save(); cv.translate(x + 30 + lw / 2, ym + 21); cv.scale(esc, esc)
        cv.drawRect(skia.Rect(-lw / 2 - 20, -62, lw / 2 + 20, 20), paint(OURO, int(80 * a * (1 - clamp(k / 0.7))), blur=18))
        texto(cv, T_14, 0, 0, F_BLACK, 62, OURO, int(255 * a * clamp(k / 0.1)), contorno=8)
        cv.restore()


# ------------------------------------------------------------------ fixador (anéis completos + hastes) e placa
def anel(cv, x, y, alfa, metade):
    if alfa <= 0:
        return
    r = skia.Rect(x - RX2, y - RY2, x + RX2, y + RY2)
    if metade == "tras":
        cv.drawArc(r, 180, 180, False, paint(ACO_ESC, int(255 * alfa), "stroke", 14))
        return
    cv.drawArc(r, 0, 180, False, paint("#000000", int(80 * alfa), "stroke", 17, blur=6))
    cv.drawArc(r, 0, 180, False, paint(ACO, int(255 * alfa), "stroke", 14))
    cv.drawArc(skia.Rect(r.left() + 6, r.top() + 4, r.right() - 6, r.bottom() - 2), 20, 140, False,
               paint(ACO_HL, int(170 * alfa), "stroke", 3))
    for ang in (25, 90, 155):
        a = math.radians(ang)
        cv.drawCircle(x + RX2 * math.cos(a), y + RY2 * math.sin(a), 3.2, paint(ACO_ESC, int(255 * alfa)))


def brilho_anel(cv, x, y, k):
    if k <= 0:
        return
    r = skia.Rect(x - RX2, y - RY2, x + RX2, y + RY2)
    cv.drawArc(r, 0, 180, False, paint(ACO_HL, int(160 * k), "stroke", 22, blur=10))
    cv.drawArc(r, 0, 180, False, paint("#FFFFFF", int(230 * k), "stroke", 5))


def placa(cv, x, y0, y1, a, brilho=0.0):
    """Barra fina, reta e lisa, de aço claro (sem parafuso, sem ponto de fixação)."""
    if a <= 0:
        return
    w = 18
    rr = skia.RRect.MakeRectXY(skia.Rect(x - w / 2, y0, x + w / 2, y1), 9, 9)
    cv.drawRRect(rr, paint("#000000", int(80 * a), blur=8))
    if brilho > 0:
        cv.drawRRect(rr, paint(ACO_HL, int(150 * brilho * a), "stroke", 20, blur=12))
    sh = skia.GradientShader.MakeLinear([skia.Point(x - w / 2, 0), skia.Point(x + w / 2, 0)],
                                        [C(ACO_HL, int(255 * a)), C(ACO, int(255 * a)), C(ACO_ESC, int(255 * a))])
    cv.drawRRect(rr, paint(ACO, 255, shader=sh))
    cv.drawLine(x - 3, y0 + 10, x - 3, y1 - 10, paint("#FFFFFF", int(150 * a), "stroke", 2.5))


def estado_aneis(t, T, ext):
    """-> lista de (x, y, alfa) dos 4 anéis: encaixam um a um no "fixador" (lados alternados), os de
    baixo descem no alongamento, e no "substituiu" sobem um pouco e somem um a um (some antes de chegar
    à altura do selo COMO FUNCIONA)."""
    out = []
    for i in range(4):
        p = e_back(prog(t, T["fixador"] + 0.12 * i, T["fixador"] + 0.12 * i + 0.5))
        dx = (-900 if i % 2 == 0 else 900) * (1 - p)
        k = prog(t, T["substituiu"] + 0.14 * i, T["substituiu"] + 0.14 * i + 0.55)
        dy = -220 * k * k
        y = Y_AN[i] + (ext if i >= 2 else 0) + dy
        out.append((CX + dx, y, clamp(p * 3) * (1 - clamp(k / 0.6)) ** 1.6))
    return out


# ------------------------------------------------------------------ peças de tela (fora da câmera)
def etiqueta(cv, s, x, y, ancora, cor, a, tam=34, fonte=F_BLACK, cor_txt="#FFFFFF", esq=False, linha=1.0):
    """Caixa de rótulo de 1 linha (topo em y). esq=False: borda esquerda em x; esq=True: borda direita
    em x. Fio fino até `ancora` (com ponto); `linha` (0..1) faz o fio crescer a partir da âncora."""
    if a <= 0:
        return
    lw = larg_texto(s, fonte, tam); alt = tam * 1.22 + 20
    x += (-1 if esq else 1) * 26 * (1 - e_out(a))
    bx = x - (lw + 32) if esq else x
    xa, ya = ancora; xb, yb = (bx + lw + 32 if esq else bx), y + alt / 2
    if linha > 0:
        cv.drawLine(xa, ya, lerp(xa, xb, linha), lerp(ya, yb, linha), paint(cor, int(210 * a), "stroke", 3))
        cv.drawCircle(xa, ya, 7, paint(cor, int(255 * a)))
    if linha >= 1:
        rr = skia.RRect.MakeRectXY(skia.Rect(bx, y, bx + lw + 32, y + alt), 14, 14)
        cv.drawRRect(rr, paint(FUNDO_CARTAO, int(220 * a)))
        cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 2.5))
        texto(cv, s, bx + 16, y + 10 + tam * 0.96, fonte, tam, cor_txt, int(255 * a), centro=False)


def faixa_caso(cv, a, brilho):
    """Atribuição do caso, logo acima da identificação CFM; dá um brilho curto no "Caso real"."""
    if a <= 0:
        return
    w1, w2 = (larg_texto(s, F_SEMI, 30) for s in FAIXA)
    x0 = CX - (w1 + 34 + w2) / 2; y = 1543
    if brilho > 0:
        rr = skia.RRect.MakeRectXY(skia.Rect(x0 - 24, y - 34, x0 + w1 + 34 + w2 + 24, y + 12), 22, 22)
        cv.drawRRect(rr, paint(OURO, int(70 * brilho * a), blur=16))
    cor = lerpc(AZUL, "#FFE7A8", brilho)
    texto(cv, FAIXA[0], x0, y, F_SEMI, 30, cor, int(235 * a), centro=False, contorno=5)
    cv.drawCircle(x0 + w1 + 17, y - 10, 4, paint(cor, int(235 * a)))
    texto(cv, FAIXA[1], x0 + w1 + 34, y, F_SEMI, 30, cor, int(235 * a), centro=False, contorno=5)


def ponto(cv, x, y, r, aceso, a):
    if a <= 0:
        return
    if aceso > 0:
        cv.drawCircle(x, y, r + 9, paint(OURO, int(110 * aceso * a), blur=10))
    cv.drawCircle(x, y, r, paint(FUNDO_CARTAO, int(235 * a)))
    cv.drawCircle(x, y, r, paint(lerpc("#8FA3B8", OURO, aceso), int(255 * a), "stroke", 3.5))
    if aceso > 0:
        cv.drawCircle(x, y, (r - 5) * e_back(aceso), paint(OURO, int(255 * a * clamp(aceso * 2))))


def linha_tempo(cv, t, T):
    """INFÂNCIA -> AOS 24 ANOS: surge grande abaixo da perna e encolhe para o canto de baixo, onde fica
    pequena até a CTA (sem contador de anos, sem rótulo de espera)."""
    # (sai antes da CTA: o cartão final ocupa essa faixa da tela)
    a0 = prog(t, T["infancia"] - 0.15, T["infancia"] + 0.2) * (1 - prog(t, T["manda"] - 0.4, T["manda"] - 0.15))
    if a0 <= 0:
        return
    k = e_inout(prog(t, T["fixador"] + 0.15, T["fixador"] + 0.85))
    xl, xr, y = lerp(190, 126, k), lerp(870, 436, k), lerp(1100, 1202, k)
    tam, dy = lerp(40, 30, k), lerp(34, 24, k)
    a = a0 * lerp(1.0, 0.85, k)
    pr = e_out(prog(t, T["infancia"] - 0.1, T["infancia"] + 0.5))
    cv.drawLine(xl, y, lerp(xl, xr, pr), y, paint("#FFFFFF", int(110 * a), "stroke", lerp(4, 3, k)))
    m = e_inout(prog(t, T["vinte"] - 0.05, T["vinte"] + 0.55))
    xm = lerp(xl, xr, m)
    if m > 0:
        cv.drawLine(xl, y, xm, y, paint(OURO, int(255 * a), "stroke", lerp(5, 4, k)))
    r = lerp(13, 10, k)
    ponto(cv, xl, y, r, e_out(prog(t, T["infancia"], T["infancia"] + 0.25)), a)
    ponto(cv, xr, y, r, e_out(prog(t, T["vinte"] + 0.5, T["vinte"] + 0.75)), a * prog(t, T["infancia"] + 0.3, T["infancia"] + 0.5))
    if 0 < m < 1:                                                # o marcador deslizando
        cv.drawCircle(xm, y, r + 10, paint(OURO, int(140 * a), blur=10))
        cv.drawCircle(xm, y, r - 2, paint("#FFF4CF", int(255 * a)))
    a1 = a * prog(t, T["infancia"], T["infancia"] + 0.2)
    texto(cv, T_INFANCIA, xl, y - dy, F_BLACK, tam, "#FFFFFF", int(255 * a1), contorno=6)
    a2 = a * prog(t, T["vinte"] + 0.45, T["vinte"] + 0.65)
    if a2 > 0:
        esc = lerp(1.2, 1.0, e_out(prog(t, T["vinte"] + 0.45, T["vinte"] + 0.75)))
        cv.save(); cv.translate(xr, y - dy); cv.scale(esc, esc)
        texto(cv, T_24, 0, 0, F_BLACK, tam, OURO, int(255 * a2), contorno=6)
        cv.restore()
    a3 = a_mancando(t, T)
    if a3 > 0:                                                   # branco: não se confunde com o aviso de esquema (azul)
        lw = larg_texto(T_MANCANDO, F_SEMI, 38)
        texto(cv, T_MANCANDO, 1030 - lw, 1158 + 12 * (1 - e_out(a3)), F_SEMI, 38, "#FFFFFF", int(255 * a3), centro=False,
              contorno=6)


def a_mancando(t, T):
    return prog(t, T["chegou"] - 0.05, T["chegou"] + 0.25) * (1 - prog(t, T["fixador"] + 0.1, T["fixador"] + 0.4))


def chip_ouro(cv, s, x, y, t0, t, a_geral, tam=40):
    k = t - t0
    if k < 0 or a_geral <= 0:
        return
    a = clamp(k / 0.15) * a_geral; esc = lerp(0.6, 1.0, e_back(clamp(k / 0.35)))
    lw = larg_texto(s, F_BLACK, tam); w, h = lw + 48, tam + 26
    acende = 1 - clamp(k / 0.9)
    cv.save(); cv.translate(x + w / 2, y + h / 2); cv.scale(esc, esc)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-w / 2 - 8, -h / 2 - 8, w / 2 + 8, h / 2 + 8), 24, 24),
                 paint(OURO, int(a * (40 + 140 * acende)), blur=16))
    r = skia.RRect.MakeRectXY(skia.Rect(-w / 2, -h / 2, w / 2, h / 2), 18, 18)
    cv.drawRRect(r, paint(FUNDO_CARTAO, int(230 * a))); cv.drawRRect(r, paint(OURO, int(255 * a), "stroke", 3.5))
    texto(cv, s, 0, tam * 0.36, F_BLACK, tam, OURO, int(255 * a))
    cv.restore()


def linha_vazia(cv, s, x, y, t_linha, t_txt, t, a_geral, tam=48):
    """Uma das duas linhas vazias embaixo do chip; vira texto na palavra (sem caixinha de check)."""
    if a_geral <= 0 or t < t_linha:
        return
    pr = e_out(prog(t, t_linha, t_linha + 0.35))
    on = e_out(prog(t, t_txt, t_txt + 0.3))
    cor = lerpc("#8FA3B8", OURO, on)
    cv.drawLine(x, y + 16, x + 360 * pr, y + 16, paint(cor, int(200 * a_geral), "stroke", 3))
    if t >= t_txt:
        k = t - t_txt
        esc = lerp(1.5, 1.0, e_out(clamp(k / 0.22)))
        lw = larg_texto(s, F_BLACK, tam)
        cv.save(); cv.translate(x + 4, y); cv.scale(esc, esc)
        cv.drawRect(skia.Rect(-8, -tam, lw + 8, 8), paint(OURO, int(90 * a_geral * (1 - clamp(k / 0.7))), blur=14))
        texto(cv, s, 0, 0, F_BLACK, tam, "#FFFFFF", int(255 * a_geral * clamp(k / 0.1)), centro=False, contorno=6)
        cv.restore()


def coluna_fixador(cv, t, T, cam, aneis):
    """Fase do fixador: rótulo, AS DUAS COISAS com as duas linhas, 1 MM por dia, calendário 4 MESES."""
    fim = 1 - prog(t, T["externa"] - 0.45, T["externa"] - 0.15)
    a = prog(t, T["fixador"] + 0.6, T["fixador"] + 0.9) * fim
    x0, y0, _ = aneis[0]
    etiqueta(cv, T_FIX, X_COL, 232, na_tela(cam, x0 + RX2 * math.cos(math.radians(32)), y0 + RY2 * math.sin(math.radians(32))),
             ACO_HL, a)
    chip_ouro(cv, T_DUAS, X_COL, 318, T["duas"] - 0.03, t, fim)
    linha_vazia(cv, T_ENDI, X_COL + 6, 460, T["duas"] + 0.15, T["endireitou"] - 0.02, t, fim)
    linha_vazia(cv, T_ALON, X_COL + 6, 540, T["duas"] + 0.3, T["alongou"] - 0.02, t, fim)
    a = prog(t, T["milimetro"] - 0.05, T["milimetro"] + 0.2) * fim
    if a > 0:
        t0, t1 = jan_longo(T)
        pulso = 0.0
        for i in range(N_LONGO):
            tc = lerp(t0, t1, i / N_LONGO)
            if t >= tc:
                pulso = max(pulso, 1 - clamp((t - tc) / 0.25))
        esc = 1 + 0.07 * pulso
        cv.save(); cv.translate(X_COL, 660); cv.scale(esc, esc)
        texto(cv, T_1MM, 0, 0, F_BLACK, 72, "#FFFFFF", int(255 * a), centro=False, contorno=8)
        cv.restore()
        texto(cv, T_DIA, X_COL + larg_texto(T_1MM, F_BLACK, 72) + 18, 660, F_SEMI, 36, AZUL, int(255 * a), centro=False)
    a = prog(t, T["meses"] - 0.05, T["meses"] + 0.2) * (1 - prog(t, T["externa"] - 0.45, T["externa"] - 0.15))
    if a > 0:
        esc = lerp(1.4, 1.0, e_out(prog(t, T["meses"] - 0.05, T["meses"] + 0.25)))
        cv.save(); cv.translate(X_COL + 114, 784); cv.scale(esc, esc)
        texto(cv, T_4M, 0, 0, F_BLACK, 60, "#FFFFFF", int(255 * a), centro=False, contorno=8)
        cv.restore()


Y_CAL2 = 520                             # 2º calendário (15 MESES DEPOIS): sobe para o meio da coluna vazia


def calendario_coluna(cv, t, T):
    """O calendário folheia (sem número) até o '4 MESES', sai com ele quando a placa entra, e volta
    folheando no 'quinze' até o '15 MESES DEPOIS'."""
    for t_in, t_out, y in ((T["quatro2"], T["externa"] - 0.15, 712), (T["quinze"], T["custo"], Y_CAL2)):
        a = prog(t, t_in - 0.1, t_in + 0.2) * (1 - prog(t, t_out - 0.3, t_out))
        if a <= 0:
            continue
        dx = 24 * (1 - e_out(prog(t, t_in - 0.1, t_in + 0.3)))
        folheia = t <= t_in + 0.7
        calendario(cv, X_COL + dx, y, t if folheia else t_in, t_in, a)


def cabe(s, fonte, tam_max, larg_max):
    """Maior tamanho (até tam_max) em que o rótulo cabe com 10% de folga (Roboto na nuvem)."""
    return min(tam_max, larg_max / (1.1 * larg_texto(s, fonte, 1.0)))


def coluna_placa(cv, t, T, x_placa_tela):
    """Fase da placa: só o rótulo PLACA EXTERNA com fio até a barra (do pouso até o 'saiu'); o resto
    (anéis saindo, eixo que vira linha contínua, barra saindo) é o mecanismo que conta, sem ecoar a
    legenda. Depois, o calendário volta com '15 MESES DEPOIS'."""
    fim = 1 - prog(t, T["custo"] - 0.3, T["custo"])
    if fim <= 0:
        return
    t_pouso = T["externa"] + 0.4                                 # a barra já pousou (k_in ~ 0,95)
    a = prog(t, t_pouso, t_pouso + 0.15) * (1 - prog(t, T["saiu"] - 0.1, T["saiu"] + 0.2)) * fim
    if a > 0 and x_placa_tela is not None:
        y = 404; alt = 34 * 1.22 + 20
        etiqueta(cv, T_PLACA, X_COL, y, (x_placa_tela, y + alt / 2), ACO_HL, a,
                 linha=e_out(prog(t, t_pouso, t_pouso + 0.22)))
    a = prog(t, T["meses2"] - 0.05, T["meses2"] + 0.2) * fim
    if a > 0:
        tam = cabe(T_15M, F_BLACK, 44, 1030 - (X_COL + 114))
        esc = lerp(1.12, 1.0, e_out(prog(t, T["meses2"] - 0.05, T["meses2"] + 0.25)))   # cresce p/ a direita: pouco
        cv.save(); cv.translate(X_COL + 114, Y_CAL2 + 66); cv.scale(esc, esc)
        texto(cv, T_15M, 0, 0, F_BLACK, tam, OURO, int(255 * a), centro=False, contorno=8)
        cv.restore()


def chip_texto(cv, s, y, t0, t, a_geral, destaque=0.0):
    k = t - t0
    if k < 0 or a_geral <= 0:
        return
    a = e_out(clamp(k / 0.3)) * a_geral
    tam = 36; lw = larg_texto(s, F_SEMI, tam); w, h = lw + 44, 68
    esc = 1 + 0.06 * destaque * math.sin(math.pi * clamp(destaque * 1.0))
    cv.save(); cv.translate(CX, y + h / 2 + 16 * (1 - e_out(clamp(k / 0.3)))); cv.scale(esc, esc)
    if destaque > 0:
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-w / 2 - 10, -h / 2 - 10, w / 2 + 10, h / 2 + 10), 26, 26),
                     paint(OURO, int(110 * destaque * a), blur=16))
    r = skia.RRect.MakeRectXY(skia.Rect(-w / 2, -h / 2, w / 2, h / 2), 18, 18)
    cv.drawRRect(r, paint(FUNDO_CARTAO, int(235 * a)))
    cv.drawRRect(r, paint(lerpc("#6F8BA6", OURO, destaque), int(255 * a), "stroke", lerp(2.5, 4, destaque)))
    texto(cv, s, 0, 13, F_SEMI, tam, "#FFFFFF", int(255 * a))
    cv.restore()


def custo_honesto(cv, t, T):
    a = prog(t, T["custo"] - 0.05, T["custo"] + 0.3) * (1 - prog(t, T["manda"] - 0.35, T["manda"] - 0.1))
    if a <= 0:
        return
    esc = lerp(1.25, 1.0, e_out(prog(t, T["custo"] - 0.05, T["custo"] + 0.3)))
    cv.save(); cv.translate(CX, 372); cv.scale(esc, esc)
    texto(cv, T_CUSTO, 0, 0, F_BLACK, 46, OURO, int(255 * a), contorno=8)
    cv.restore()
    lw = larg_texto(T_CUSTO, F_BLACK, 46) * e_out(prog(t, T["custo"] + 0.1, T["custo"] + 0.5))
    cv.drawLine(CX - lw / 2, 394, CX + lw / 2, 394, paint(OURO, int(200 * a), "stroke", 3))
    dest = max(0.0, min(1.0, prog(t, T["tornozelo"] - 0.05, T["tornozelo"] + 0.25)))
    tempos = (T["rigidez"] - 0.05, T["tornozelo"] + 0.5, T["tornozelo"] + 0.9)
    for i, (s, t0) in enumerate(zip(CHIPS, tempos)):
        chip_texto(cv, s, 432 + 88 * i, t0, t, a, destaque=dest if i == 0 else 0.0)
    t0 = T["tornozelo"] + 1.3
    if t >= t0:
        k = e_out(clamp((t - t0) / 0.3)); aa = a * k
        lw = larg_texto(T_UNICO, F_SEMI, 32)
        y = 724 + 14 * (1 - k)
        rr = skia.RRect.MakeRectXY(skia.Rect(CX - lw / 2 - 24, y, CX + lw / 2 + 24, y + 56), 28, 28)
        cv.drawRRect(rr, paint(FUNDO_CARTAO, int(225 * aa))); cv.drawRRect(rr, paint(AZUL, int(220 * aa), "stroke", 2.5))
        texto(cv, T_UNICO, CX, y + 38, F_SEMI, 32, AZUL, int(255 * aa))
    t0 = T["tornozelo"] + 1.6
    if t >= t0:
        aa = a * e_out(clamp((t - t0) / 0.3))
        texto(cv, T_FONTE, CX, 832, F_SEMI, 30, "#C9D6E2", int(235 * aa), contorno=5)


class _SemLegenda:
    """Canvas-envelope para a interface antes da 1ª palavra: a legenda karaokê (fonte de 80 px) mostraria
    o bloco inteiro apagado já no quadro 0, competindo com o gancho; até a voz começar, só o gancho fala
    grande. Todo o resto passa direto (mesmo mecanismo do envelope _Devagarinho do cf_transporte_osseo)."""
    def __init__(self, cv):
        self._cv = cv

    def drawString(self, s, x, y, f, p):
        if f.getSize() >= 79:
            return None
        return self._cv.drawString(s, x, y, f, p)

    def __getattr__(self, nome):
        return getattr(self._cv, nome)


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    cam = camera(t, T)
    px, py, s = cam
    t_cta = T["manda"] - 0.15
    bow, ext = bow_de(t, T), ext_de(t, T)
    aneis = estado_aneis(t, T, ext)
    # a perna vai ao fundo ANTES do título do custo entrar, e quase some quando entra a fonte (sem caixa)
    a_perna = (1 - 0.84 * prog(t, T["custo"] - 0.5, T["custo"] + 0.05)) * \
              (1 - 0.6 * prog(t, T["tornozelo"] + 1.3, T["tornozelo"] + 1.6))
    t0r, t1r = jan_reto(T)

    # ================= mundo (câmera)
    cv.save(); cv.translate(px, py); cv.scale(s, s); cv.translate(-CX, -FOCO)
    for x, y, al in aneis:
        anel(cv, x, y, al, "tras")
    brilho_p = max(0.0, 1 - abs(t - (T["perna"] + 0.25)) / 0.35)
    g_firme = e_inout(prog(t, T["firmar"] + 0.05, T["firmar"] + 0.7))
    desenha_perna(cv, bow, ext, a_perna, brilho_p, g_firme, t)
    if 0 < g_firme < 1:                                          # o brilho percorre o eixo de cima a baixo
        gx, gy = x_de(g_firme, bow), y_de(g_firme, ext)
        cv.drawCircle(gx, gy, 34, paint(OURO, 150, blur=16))
        cv.drawCircle(gx, gy, 9, paint("#FFF4CF", 255))
    brilhos(cv, x_de(0.6, bow), y_de(0.6, ext), t, T["firmar"] + 0.72, n=14, raio=190)

    # arqueada: arco dourado por fora da curva; fica VISÍVEL no endireitar (achata junto com o contorno) e
    # só some quando a perna já está reta
    a_arco = prog(t, T["arqueada"] - 0.05, T["arqueada"] + 0.1) * (1 - prog(t, t1r - 0.25, t1r + 0.1))
    arco_ouro(cv, bow, ext, e_inout(prog(t, T["arqueada"], T["arqueada"] + 0.6)), a_arco, t)
    seta_correcao(cv, bow, ext, prog(t, t0r - 0.1, t0r + 0.1) * (1 - prog(t, t1r - 0.2, t1r + 0.05)))
    brilhos(cv, x_de(0.5, bow), y_de(0.5, ext), t, t1r + 0.05, n=12, raio=150)   # depois que a seta apagou
    t0, t1 = jan_longo(T)
    seta_dupla(cv, CX + 188, Y_AN[1], Y_AN[2] + ext, prog(t, t0 - 0.15, t0 + 0.1) * (1 - prog(t, t1 + 0.4, t1 + 0.8)))

    # cota vazia (quadro 0) -> '14 cm' no 'catorze'; some no 'fixador' e não volta
    a_cota = 1 - prog(t, T["fixador"] - 0.1, T["fixador"] + 0.3)
    cota(cv, CX, COTA[0], COTA[1], a_cota, t, T["catorze"])

    # hastes e porcas (as do meio com rosca; a porca gira a cada passinho do alongamento)
    a_h = prog(t, T["fixador"] + 0.4, T["fixador"] + 0.8) * (1 - prog(t, T["substituiu"] - 0.05, T["substituiu"] + 0.3))
    if a_h > 0:
        ys = [y for _, y, _ in aneis]
        giro = 60 * N_LONGO * ext / EXT
        for sx in (-1, 1):
            x = CX + sx * X_HASTE
            haste(cv, x, ys[0], ys[1], a_h)
            haste(cv, x, ys[1], ys[2], a_h, rosca=True, fase=-ext * 0.6)
            haste(cv, x, ys[2], ys[3], a_h)
            porca(cv, x, ys[1] + 22, sx * 15, a_h)
            porca(cv, x, ys[2] - 22, giro + sx * 15, a_h)
    for i, (x, y, al) in enumerate(aneis):
        anel(cv, x, y, al, "frente")
        brilho_anel(cv, x, y, max(0.0, 1 - abs(t - (T["fixador"] + 0.12 * i + 0.42)) / 0.22) * al)

    # placa externa: entra pela lateral, segura, sai
    k_in = e_out(prog(t, T["externa"], T["externa"] + 0.55))
    k_out = e_out(prog(t, T["saiu"] - 0.02, T["saiu"] + 0.35))       # desliza um pouco para fora e some
    a_pl = prog(t, T["externa"], T["externa"] + 0.1) * (1 - prog(t, T["saiu"] + 0.02, T["saiu"] + 0.32))
    x_pl = CX + X_PLACA + 820 * (1 - k_in) + 22 * k_out
    y_pl0, y_pl1 = Y_AN[0] - 10, Y_AN[3] + EXT + 10
    placa(cv, x_pl, y_pl0, y_pl1, a_pl, brilho=max(0.0, 1 - abs(t - (T["externa"] + 0.55)) / 0.3))
    cv.restore()

    # ================= tela (rótulos, linha do tempo, colunas)
    a = prog(t, T["arqueada"] + 0.1, T["arqueada"] + 0.35) * (1 - prog(t, T["fixador"] - 0.4, T["fixador"] - 0.1))
    ax, ay = na_tela(cam, x_de(0.5, bow) + meia(0.5) + 36, y_de(0.5, ext))
    etiqueta(cv, T_ARQ, ax + 18, ay - 33, (ax, ay), OURO, a, tam=38, cor_txt=OURO)
    a = prog(t, T["causa"] - 0.05, T["causa"] + 0.15) * (1 - prog(t, T["fixador"] - 0.4, T["fixador"] - 0.1))
    ix, iy = na_tela(cam, x_de(0.5, bow), y_de(0.5, ext))
    etiqueta(cv, T_INF, 440, iy - 34, (ix, iy), "#FF9A7A", a, tam=36, esq=True,
             linha=e_out(prog(t, T["causa"], T["infeccao"] - 0.05)) if t < T["infeccao"] else 1.0)
    linha_tempo(cv, t, T)
    coluna_fixador(cv, t, T, cam, aneis)
    calendario_coluna(cv, t, T)
    x_pl_tela = na_tela(cam, x_pl + 9, 0)[0]                     # o fio acompanha a barra quando ela sai
    coluna_placa(cv, t, T, x_pl_tela)
    custo_honesto(cv, t, T)

    capa(cv, t, T["causa"], ep["gancho"][0], ep["gancho"][1])
    selo_como_funciona(cv, prog(t, T["causa"] + 0.4, T["causa"] + 0.8) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface(_SemLegenda(cv) if t < T["perna"] - 0.03 else cv, t, T, blocos, DESTAQUE)

    # atribuição + aviso de esquema: do quadro 0 ao último (por cima do escurecimento da CTA)
    faixa_caso(cv, 1.0, max(0.0, 1 - abs(t - (T["caso"] + 0.3)) / 0.45))
    # o do canto sai ANTES do cartão final acender; o de baixo entra logo que o rodapé CFM da tela (y 1585)
    # dá lugar ao cartão (nunca por cima do cartão nem do rodapé; a troca é um cruzamento, sem buraco);
    # enquanto 'chegou ao hospital mancando' está logo acima, o do canto fica a 40%
    k_out = prog(t, t_cta - 0.35, t_cta)
    k_in = prog(t, t_cta + 0.02, t_cta + 0.32)
    lw = larg_texto(ESQUEMA, F_SEMI, 30)
    if k_out < 1:
        texto(cv, ESQUEMA, 1030 - lw, 1210, F_SEMI, 30, AZUL, int(215 * (1 - k_out) * (1 - 0.6 * a_mancando(t, T))),
              centro=False, contorno=5)
    if k_in > 0:
        texto(cv, ESQUEMA, CX, 1592, F_SEMI, 30, AZUL, int(215 * k_in), contorno=5)


# ------------------------------------------------------------------ som e prévias
def sons(T):
    ev = [(T["perna"] + 0.05, "shimmer", 0.35), (T["arqueada"], "whoosh", 0.45), (T["catorze"] + 0.05, "thump", 0.85),
          (T["caso"] + 0.1, "shimmer", 0.35), (T["causa"] + 0.05, "whoosh", 0.3), (T["infeccao"] - 0.03, "pop", 0.6),
          (T["infancia"], "pop", 0.55), (T["vinte"], "whoosh", 0.35), (T["vinte"] + 0.5, "ding", 0.5),
          (T["chegou"], "pop", 0.4), (T["fixador"] - 0.05, "whoosh", 0.6)]
    ev += [(T["fixador"] + 0.12 * i + 0.4, "ping", 0.55) for i in range(4)]       # cada anel encaixa
    ev += [(T["duas"], "pop", 0.65), (T["endireitou"], "pop", 0.55), (T["alongou"], "pop", 0.55)]
    t0, t1 = jan_reto(T)
    ev += [(lerp(t0, t1, i / N_RETO), "click", 0.85) for i in range(N_RETO)]
    t0, t1 = jan_longo(T)
    ev += [(lerp(t0, t1, i / N_LONGO), "click", 0.75) for i in range(N_LONGO)]   # um clique por passinho
    ev += [(T["milimetro"], "pop", 0.4), (T["quatro2"] - 0.1, "whoosh", 0.3), (T["meses"], "ding", 0.5),
           (T["externa"], "whoosh", 0.6), (T["externa"] + 0.5, "thump", 0.6)]
    ev += [(T["substituiu"] + 0.14 * i, "whoosh", 0.35) for i in range(4)]
    ev += [(T["firmar"] + 0.05, "shimmer", 0.75), (T["firmar"] + 0.7, "crackle", 0.6), (T["saiu"], "whoosh", 0.6),
           (T["quinze"] - 0.05, "whoosh", 0.3), (T["meses2"], "ding", 0.5), (T["custo"], "whoosh", 0.35),
           (T["custo"] + 0.05, "pop", 0.5), (T["rigidez"], "pop", 0.55), (T["tornozelo"], "thump", 0.5),
           (T["tornozelo"] + 0.5, "pop", 0.45), (T["tornozelo"] + 0.9, "pop", 0.45), (T["tornozelo"] + 1.3, "pop", 0.4),
           (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def tempos_previa(T):
    return [0.05, T["catorze"] + 0.5, T["infeccao"] + 0.5, T["chegou"] + 0.6, T["fixador"] + 1.2,
            T["endireitou"] + 0.7, T["milimetro"] + 1.2, T["externa"] + 0.9, T["firmar"] + 0.35,
            T["meses2"] + 0.5, T["tornozelo"] + 1.9, T["manda"] + 1.6]


# ------------------------------------------------------------------ entrada única
_PONTA = re.compile(r"[.,:;!?—…]+$")


def fazer_render_tolerante(quadro_fn, mapa, sons_fn, tempos_fn, respiro_cta=1.6):
    """Os MESMOS passos de cf_comum.fazer_render, só que limpando a pontuação que o edge-tts às vezes
    cola na palavra ("real.") antes de alinhar com o roteiro (ver o docstring do módulo)."""
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


render = fazer_render_tolerante(quadro, ANCORAS, sons, tempos_previa, respiro_cta=3.0)   # ~3 s de leitura do custo honesto
