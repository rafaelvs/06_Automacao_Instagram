# -*- coding: utf-8 -*-
"""COMO FUNCIONA — dor no alongamento ósseo ("ALONGAR O OSSO / DÓI?").

Mesmo estilo e mesmas peças do cf_alongamento e do cf_fisioterapia (osso marfim, vão de osso novo
dourado, anéis/fios/hastes do fixador, faixa rosada do músculo, carimbos, legenda karaokê, CTA com
aviãozinho). O que a cena mostra, cada coisa disparada pela palavra falada:
  * capa: tíbia esquemática JÁ dividida, com um vão fino de osso novo dourado, dentro de um fixador
    de 4 anéis; o gancho é o único texto grande; nada se mexe até o espanto;
  * "dói": um ponto de interrogação DESENHADO (traço, não letra) cai ao lado do aparelho e balança;
    "desconforto": ele vira a etiqueta âmbar DESCONFORTO pendurada no anel; "manejo": a etiqueta
    verde-água MANEJO pendura do outro lado, na mesma altura — em equilíbrio, sem balança nem placar;
  * "ajuste": etiqueta de papel DIAS DE AJUSTE no anel de cima; o vão abre só um pouquinho, com um
    clique suave (sem porca em close, sem número, sem régua);
  * "pressão": três ondinhas âmbar claras em volta do aparelho inteiro (sem vermelho, sem apontar
    para ponto nenhum); "muscular": a faixa rosada do cf_fisioterapia AO LADO do segmento de cima,
    com ondinhas leves; "comuns": carimbo de cor neutra SÃO COMUNS logo abaixo das duas etiquetas;
  * "analgesia": o fixador encolhe para a esquerda e esmaece; ao lado, cartão branco ANALGESIA E
    FISIOTERAPIA; "início": o selo DESDE O INÍCIO encaixa SÓ sob esse cartão (a fonte não o estende
    às camadas);
  * "camadas": fixador e cartão sobem para o topo e abre-se a moldura EM CAMADAS com 4 linhas
    vazias (o selo continua preso ao cartão, fora da moldura); "medicação": relógio sem número cujo ponteiro
    pula de marca em marca; "alongamento": músculo fusiforme com fibras e tendões, que se espreguiça;
    "posicionamento": perna esquemática com o calcanhar APOIADO num travesseiro e o pé para cima;
    "sono": lua e estrelinhas;
    "meta": carimbo dourado META DE TRATAMENTO sobre a pilha completa;
  * "dor que dispara": gráfico sem eixo numerado nem escala — linha baixa ondulada (DESCONFORTO) que
    sobe num pico vertical coral (DISPARA DE REPENTE) e fica lá em cima, reta (NÃO CEDE COM A
    MEDICAÇÃO); "avise": a linha vira seta até o cartão branco AVISE A EQUIPE (telefone genérico);
    "febre": cartão coral com termômetro sem número e sinal de mais BRANCO (nunca a cruz vermelha
    sobre branco, nunca a letra H): COM FEBRE, PRONTO-SOCORRO;
  * "conversa": o fixador da capa volta com a etiqueta e um balão DOR SE CONVERSA; "aguenta": NÃO SE
    AGUENTA em letra menor, sem X; no respiro antes da CTA, plano aberto: a pilha das 4 camadas
    (ícones e tiques) com o carimbo entra ao lado. Quando a CTA entra, saem etiqueta, balão, NÃO SE
    AGUENTA, pilha e carimbo: atrás da CTA fica só o fantasma do fixador, como no cf_fisioterapia.
Nenhum exame de imagem, nenhum rosto, nenhum comprimido com nome, nenhuma dose, nenhum número.
Todo texto desenhado está em ep["tela"] (o render recusa o vídeo se não estiver).
"""
import math

import skia

from .cf_comum import capa, fazer_render, interface, selo_como_funciona
from .cf_alongamento import (ACO, ACO_ESC, ACO_HL, CX, F_BLACK, HASTE, NOVO_G, OSSO_B, OSSO_C, OSSO_L, OURO,
                             W, C, brilhos, clamp, desenha_regenerado, e_back, e_inout, e_out, fundo, haste,
                             larg_texto, lerp, paint, path_osso_inf, path_osso_sup, porca, prog, sombra_osso,
                             texto)

ANCORAS = {
    "doi": ("dói", 1, False), "desconforto": ("desconforto", 1, False), "manejo": ("manejo", 1, False),
    "ajuste": ("ajuste", 1, False), "pressao": ("pressão", 1, False), "muscular": ("muscular", 1, False),
    "comuns": ("comuns", 1, False), "analgesia": ("analgesia", 1, False), "inicio": ("início", 1, False),
    "camadas": ("camadas", 1, False), "medicacao": ("medicação", 1, False),
    "alongamento": ("alongamento", 1, False), "posicionamento": ("posicionamento", 1, False),
    "sono": ("sono", 1, False), "controlada": ("controlada", 1, False), "meta": ("meta", 1, False),
    "luxo": ("luxo", 1, False), "dor3": ("dor", 3, False), "dispara": ("dispara", 1, False),
    "repente": ("repente", 1, False), "ou": ("ou", 1, False), "cede": ("cede", 1, False), "avise": ("avise", 1, False),
    "equipe": ("equipe", 1, False), "febre": ("febre", 1, False), "pronto": ("pronto", 1, True),
    "dor4": ("dor", 4, False), "conversa": ("conversa", 1, False), "aguenta": ("aguenta", 1, False),
    "manda": ("manda", 1, False),
}
DESTAQUE = {"dói", "desconforto", "manejo", "ajuste", "pressão", "muscular", "comuns", "analgesia",
            "fisioterapia", "início", "camadas", "meta", "dispara", "cede", "avise", "equipe", "febre",
            "conversa", "aguenta"}

# ------------------------------------------------------------------ paleta própria
AMBAR_T = "#FFB547"         # etiqueta DESCONFORTO
AMBAR_CL = "#FFD58F"        # ondinhas de pressão (âmbar claro, nunca vermelho)
TEAL = "#4FD1C5"            # MANEJO
ROSA, ROSA_B = "#F2A3AA", "#C2707A"
PAPEL, PAPEL_B, TINTA = "#F3E9D2", "#BFA678", "#2A2118"
NEUTRO = "#D6E4F0"          # carimbo SÃO COMUNS (cor neutra, não de alarme)
CORAL, CORAL_ESC = "#FF6B5E", "#D9434A"
NAVY = "#12324A"
AMBAR = "#7A5420"           # base opaca do vão (nada translúcido)
FUNDO_CX = "#0B1824"
PELE, PELE_B = "#F0B49A", "#C98A70"
LUA = "#F7EEDD"

# ------------------------------------------------------------------ geometria do mundo (fixador)
Y_TOPO, Y_CORTE, Y_BASE = 300, 740, 1000
FENDA = 6
H2 = HASTE / 2
RX2, RY2 = 175, 38
X_HASTE = 158
Y_AN0, Y_AN1 = 390, Y_CORTE - 75
GAP0, GAP1 = 22.0, 40.0     # o vão já existe na capa; no "ajuste" abre um pouquinho, VISÍVEL (sem número)
MUSC_X, MUSC_Y0, MUSC_Y1, MUSC_L = CX + 110, 545, 730, 58.0
YW = 600.0
TAM_TAG = 32                # DESCONFORTO / MANEJO: folga para Roboto sem passar de x 40

# câmera: (x na tela do eixo do osso, escala, y na tela do ponto YW do mundo)
CAM_CAPA = (540.0, 0.92, 735.0)
CAM_LADO = (470.0, 0.80, 700.0)      # libera a coluna da direita para as etiquetas
CAM_MEIO = (190.0, 0.50, 700.0)      # encolhido à esquerda, esmaecido, ao lado do cartão
CAM_MINI = (170.0, 0.30, 385.0)      # sobe para o canto quando a moldura das camadas abre
CAM_CONV = (290.0, 0.70, 810.0)      # volta da capa, ao lado do balão
CAM_FIM = (280.0, 0.66, 812.0)       # plano aberto atrás da CTA


def mix(c1, c2, a):
    return tuple(lerp(c1[i], c2[i], a) for i in range(3))


def na_tela(cam, x, y):
    px, s, ys = cam
    return px + (x - CX) * s, ys + (y - YW) * s


def camera(t, T):
    c = mix(CAM_CAPA, CAM_LADO, e_inout(prog(t, T["ajuste"] - 0.3, T["ajuste"] + 0.4)))
    c = mix(c, CAM_MEIO, e_inout(prog(t, T["analgesia"] - 0.15, T["analgesia"] + 0.4)))
    c = mix(c, CAM_MINI, e_inout(prog(t, T["camadas"] - 0.25, T["camadas"] + 0.25)))
    if t >= T["dor4"] - 0.3:                                   # o fixador da capa volta, entrando pela esquerda
        k = e_out(prog(t, T["dor4"] - 0.3, T["conversa"] + 0.2))
        c = (lerp(-330.0, CAM_CONV[0], k), CAM_CONV[1], CAM_CONV[2])
        c = mix(c, CAM_FIM, e_inout(prog(t, T["aguenta"] + 0.35, T["aguenta"] + 1.1)))
    return c


def alfa_mundo(t, T):
    if t >= T["dor4"] - 0.3:
        return prog(t, T["dor4"] - 0.3, T["dor4"])
    a = lerp(1.0, 0.42, prog(t, T["analgesia"] - 0.1, T["analgesia"] + 0.4))
    return a * (1 - prog(t, T["meta"] - 0.45, T["meta"] - 0.05))


def vao(t, T):
    return lerp(GAP0, GAP1, e_inout(prog(t, T["ajuste"] + 0.25, T["ajuste"] + 0.9)))


def aneis_y(g):
    yc_inf = Y_CORTE + FENDA + g; yb = Y_BASE + FENDA + g
    return [Y_AN0, Y_AN1, yc_inf + 62, yb - 112]


def janela(t, t0, t1, d_in=0.25, d_out=0.3):
    return prog(t, t0, t0 + d_in) * (1 - prog(t, t1, t1 + d_out))


# ------------------------------------------------------------------ mundo: fixador (estilo cf_fisioterapia)
def anel(cv, y, alfa, metade):
    if alfa <= 0:
        return
    r = skia.Rect(CX - RX2, y - RY2, CX + RX2, y + RY2)
    if metade == "tras":
        cv.drawArc(r, 180, 180, False, paint(ACO_ESC, int(255 * alfa), "stroke", 14))
        return
    cv.drawArc(r, 0, 180, False, paint("#000000", int(80 * alfa), "stroke", 17, blur=6))
    cv.drawArc(r, 0, 180, False, paint(ACO, int(255 * alfa), "stroke", 14))
    cv.drawArc(skia.Rect(r.left() + 6, r.top() + 4, r.right() - 6, r.bottom() - 2), 20, 140, False,
               paint(ACO_HL, int(170 * alfa), "stroke", 3))
    for ang in (25, 90, 155):
        a = math.radians(ang)
        cv.drawCircle(CX + RX2 * math.cos(a), y + RY2 * math.sin(a), 3.2, paint(ACO_ESC, int(255 * alfa)))


def fios(cv, y, alfa):
    for s in (-1, 1):
        x0, y0, x1, y1 = CX - RX2 + 16, y - 12 * s, CX + RX2 - 16, y + 12 * s
        cv.drawLine(x0, y0, x1, y1, paint("#DDE6EE", int(230 * alfa), "stroke", 3.2))
        xo = CX - 62 * s
        cv.drawCircle(xo, lerp(y0, y1, (xo - x0) / (x1 - x0)), 6, paint(OURO, int(255 * alfa)))


def osso(cv, yc_sup, yc_inf, yb):
    sh = sombra_osso()
    for pth in (path_osso_sup(Y_TOPO, yc_sup), path_osso_inf(yc_inf, yb)):
        cv.drawPath(pth, paint("#000000", 70, blur=14))
        cv.drawPath(pth, paint(OSSO_C, shader=sh))
        cv.drawPath(pth, paint(OSSO_L, 150, "stroke", 2.5))
    for y0, y1 in ((Y_TOPO + 250, yc_sup), (yc_inf, yb - 190)):
        if y1 > y0:
            cv.drawRect(skia.Rect(CX - 16, y0, CX + 16, y1), paint(OSSO_B, 60, blur=6))


def faixa_musculo(cv, x0, y0, x1, y1, a, vertical=True):
    """A faixa rosada e lisa do cf_fisioterapia (cápsula com degradê)."""
    if a <= 0:
        return
    w = (x1 - x0) if vertical else (y1 - y0)
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), w / 2, w / 2)
    if vertical:
        pts = [skia.Point(x0, 0), skia.Point(x1, 0)]
    else:
        pts = [skia.Point(0, y0), skia.Point(0, y1)]
    sh = skia.GradientShader.MakeLinear(pts, [C(ROSA_B), C(ROSA), C(ROSA), C(ROSA_B)], [0.0, 0.4, 0.6, 1.0])
    cv.drawRRect(rr, paint("#000000", int(55 * a), blur=8))
    cv.drawRRect(rr, paint(ROSA, int(255 * a), shader=sh))
    cv.drawRRect(rr, paint(ROSA_B, int(220 * a), "stroke", 2.5))


def mundo(cv, t, T, cam, g, musc):
    px, s, ys = cam
    cv.save(); cv.translate(px, ys); cv.scale(s, s); cv.translate(-CX, -YW)
    yc_inf = Y_CORTE + FENDA + g; yb = Y_BASE + FENDA + g
    y_an = aneis_y(g)
    for y in y_an:
        anel(cv, y, 1.0, "tras")
    if musc > 0:                                                  # AO LADO do segmento de cima, sem cruzar o vão
        y1 = lerp(MUSC_Y0 + 24, MUSC_Y1, e_out(musc))
        faixa_musculo(cv, MUSC_X - MUSC_L / 2, MUSC_Y0, MUSC_X + MUSC_L / 2, y1, musc)
    osso(cv, Y_CORTE, yc_inf, yb)
    y0, y1 = Y_CORTE + FENDA * 0.5, yc_inf - FENDA * 0.5
    cv.drawRect(skia.Rect(CX - H2 + 2, y0, CX + H2 - 2, y1), paint(AMBAR))
    k = t - (T["ajuste"] + 0.3)
    flash = (1 - prog(k, 0.0, 0.9)) if k >= 0 else 0.0           # o "clique": o osso novo acende um instante
    desenha_regenerado(cv, y0, y1, 0.8, 0.3 + 0.7 * flash, 0.0, 0.0)
    for y in y_an:
        fios(cv, y, 1.0)
    for sx in (-1, 1):
        x = CX + sx * X_HASTE
        haste(cv, x, y_an[0], y_an[1], 1.0)
        haste(cv, x, y_an[1], y_an[2], 1.0, rosca=True, fase=g * 0.4)
        haste(cv, x, y_an[2], y_an[3], 1.0)
        porca(cv, x, y_an[1] + 20, 15 * sx, 1.0)
        porca(cv, x, y_an[2] - 20, -15 * sx, 1.0)
    for y in y_an:
        anel(cv, y, 1.0, "frente")
    cv.restore()


# ------------------------------------------------------------------ peças de tela
Q_CENTRO = 99.0      # distância (em unidades do glifo) da base-pivô até o centro visual do '?'


def interrogacao(cv, x, y, esc, ang, a, centro=False):
    """Ponto de interrogação DESENHADO (traço + ponto): não é letra. Pivô na base (x, y); com
    `centro=True`, (x, y) é o centro visual do glifo e a escala/rotação acontecem em torno dele."""
    if a <= 0 or esc <= 0:
        return
    cv.save(); cv.translate(x, y); cv.rotate(ang); cv.scale(esc, esc)
    cv.translate(-2, 3) if centro else cv.translate(0, -96)
    p = skia.Path()
    p.moveTo(-40, -44)
    p.cubicTo(-40, -96, 44, -104, 44, -48)
    p.cubicTo(44, -14, 2, -10, 2, 22)
    p.lineTo(2, 36)
    for cor, al, larg, blur in (("#000000", 90, 34, 10), ("#FFFFFF", 255, 26, 0)):
        pt = paint(cor, int(al * a), "stroke", larg, blur=blur)
        cv.drawPath(p, pt)
        cv.drawCircle(2, 78, larg * 0.62, paint(cor, int(al * a), blur=blur))
    cv.restore()


def etiqueta_pend(cv, s, ax, ay, lado, a, ang, fundo_cor, borda, cor_txt, ent=1.0, tam=34, papel=False):
    """Etiqueta pendurada por um fio em (ax, ay) — ponto da borda de um anel. `lado` +1/-1: para que
    lado do aparelho ela pende. Gira em torno do furo (balanço)."""
    if a <= 0 or ent <= 0:
        return
    tw = larg_texto(s, F_BLACK, tam); h = tam + 28; w = tw + 70
    hx, hy = ax + lado * 28, ay + 46
    cv.drawLine(ax, ay, hx, hy, paint("#E6EEF6", int(220 * a), "stroke", 2.5))
    cv.drawCircle(ax, ay, 5, paint(ACO_HL, int(255 * a)))
    cv.save(); cv.translate(hx, hy); cv.rotate(ang); cv.scale(ent, ent)
    if lado > 0:
        x0, x1 = -22.0, w - 22.0
    else:
        x0, x1 = -(w - 22.0), 22.0
    y0, y1 = -h / 2, h / 2
    ch = 18                                                        # cantos chanfrados do lado do furo
    p = skia.Path()
    if lado > 0:
        p.moveTo(x0 + ch, y0); p.lineTo(x1 - 10, y0); p.quadTo(x1, y0, x1, y0 + 10); p.lineTo(x1, y1 - 10)
        p.quadTo(x1, y1, x1 - 10, y1); p.lineTo(x0 + ch, y1); p.lineTo(x0, y1 - ch); p.lineTo(x0, y0 + ch)
    else:
        p.moveTo(x1 - ch, y0); p.lineTo(x0 + 10, y0); p.quadTo(x0, y0, x0, y0 + 10); p.lineTo(x0, y1 - 10)
        p.quadTo(x0, y1, x0 + 10, y1); p.lineTo(x1 - ch, y1); p.lineTo(x1, y1 - ch); p.lineTo(x1, y0 + ch)
    p.close()
    cv.drawPath(p, paint("#000000", int(80 * a), blur=10))
    cv.drawPath(p, paint(fundo_cor, int((255 if papel else 225) * a)))
    cv.drawPath(p, paint(borda, int(255 * a), "stroke", 2.5))
    # ilhós metálico pequeno, em cor DIFERENTE da do texto (o anel na cor do texto lia como letra a mais)
    cv.drawCircle(0, 0, 6, paint(ACO_HL, int(255 * a)))
    cv.drawCircle(0, 0, 2.5, paint(FUNDO_CX, int(255 * a)))
    cx = (x0 + x1) / 2 + lado * 15
    texto(cv, s, cx, tam * 0.36, F_BLACK, tam, cor_txt, int(255 * a))
    cv.restore()


def centro_etiqueta(s, ax, ay, lado, tam=34):
    """Centro do texto de uma etiqueta_pend (sem o balanço): para onde o '?' encolhe."""
    w = larg_texto(s, F_BLACK, tam) + 70
    return ax + lado * 28 + lado * (w / 2 - 7), ay + 46


def balanco(t, t0, amp=10.0):
    """Ângulo de uma etiqueta que acabou de pendurar: balança, amortece e fica num vaivém mínimo."""
    k = t - t0
    if k < 0:
        return 0.0
    return amp * math.exp(-3.2 * k) * math.sin(9.5 * k) + 1.6 * math.sin(1.7 * t) * prog(k, 0.2, 1.0)


def etiqueta(cv, s, x, y, ancora, cor, a, tam=36, halo=0.0):
    """Rótulo com canto sup. esq. em (x, y) e fio fino até `ancora` (do cf_fisioterapia).
    `halo` (0-1): contorno branco com blur em volta da caixa (pulso de destaque, sem texto novo)."""
    if a <= 0:
        return
    x += 26 * (1 - e_out(a))
    lw = larg_texto(s, F_BLACK, tam); hh = tam + 22
    if ancora:
        xa, ya = ancora
        cv.drawLine(xa, ya, x, y + hh / 2, paint(cor, int(200 * a), "stroke", 2.5))
        cv.drawCircle(xa, ya, 6, paint(cor, int(255 * a)))
    rr = skia.RRect.MakeRectXY(skia.Rect(x, y, x + lw + 32, y + hh), 14, 14)
    if halo > 0:
        cv.drawRRect(rr, paint("#FFFFFF", int(200 * a * halo), "stroke", 14, blur=10))
        cv.drawRRect(rr, paint("#FFFFFF", int(255 * a * halo), "stroke", 4))
    cv.drawRRect(rr, paint(FUNDO_CX, int(215 * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 2.5))
    texto(cv, s, x + 16, y + hh / 2 + tam * 0.36, F_BLACK, tam, cor, int(255 * a), centro=False)


def carimbo_cor(cv, s, x, y, rot, t0, t, cor, dur=1.9, tam=62, esc0=1.9, fundo_a=170):
    """Carimbo do piloto com cor, tamanho e escala de entrada ajustáveis (do cf_fisioterapia)."""
    k = t - t0
    if k < 0 or k > dur:
        return
    esc = lerp(esc0, 1.0, e_out(clamp(k / 0.16))); a = clamp(k / 0.08) * (1 - prog(k, dur - 0.35, dur))
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(esc, esc)
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 24, -tam, lw / 2 + 24, tam * 0.36), 12, 12)
    cv.drawRRect(rr, paint(FUNDO_CX, int(fundo_a * a))); cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 7))
    cv.drawString(s, -lw / 2, 0, f, paint(cor, int(255 * a)))
    cv.restore()


def ondas(cv, cx, cy, rx, ry, t, t0, cor, n=3, dur=1.0, esp=0.24, larg=6):
    """Ondinhas concêntricas suaves que pulsam e somem."""
    for i in range(n):
        k = (t - t0 - i * esp) / dur
        if not 0 <= k <= 1:
            continue
        s = lerp(0.84, 1.2, e_out(k)); a = math.sin(math.pi * k) ** 1.2
        r = skia.Rect(cx - rx * s, cy - ry * s, cx + rx * s, cy + ry * s)
        cv.drawOval(r, paint(cor, int(90 * a), "stroke", larg + 10, blur=9))
        cv.drawOval(r, paint(cor, int(210 * a), "stroke", larg))


def tique(cv, x, y, pr, cor, a, esc=1.0, larg=6.5):
    if pr <= 0 or a <= 0:
        return
    p = skia.Path(); p.moveTo(x - 14 * esc, y)
    p.lineTo(x + (-14 + 10 * min(1, pr * 2)) * esc, y + 10 * min(1, pr * 2) * esc)
    if pr > 0.5:
        q = (pr - 0.5) * 2
        p.lineTo(x + (-4 + 20 * q) * esc, y + (10 - 26 * q) * esc)
    cv.drawPath(p, paint(cor, int(255 * a), "stroke", larg))


def estrela(cv, x, y, s, cor, a):
    if a <= 0 or s <= 0:
        return
    p = skia.Path(); p.moveTo(x, y - s * 2); p.lineTo(x + s * 0.5, y - s * 0.5); p.lineTo(x + s * 2, y)
    p.lineTo(x + s * 0.5, y + s * 0.5); p.lineTo(x, y + s * 2); p.lineTo(x - s * 0.5, y + s * 0.5)
    p.lineTo(x - s * 2, y); p.lineTo(x - s * 0.5, y - s * 0.5); p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))


def lua(cv, x, y, r, a, cor=LUA):
    if a <= 0:
        return
    p = skia.Path(); p.addCircle(x, y, r)
    q = skia.Path(); q.addCircle(x + r * 0.48, y - r * 0.26, r * 0.86)
    c = skia.Op(p, q, skia.PathOp.kDifference_PathOp) or p
    cv.drawPath(c, paint(cor, int(110 * a), blur=12))
    cv.drawPath(c, paint(cor, int(255 * a)))


# ------------------------------------------------------------------ ícones das camadas (sem texto)
MARCAS = (-90.0, 30.0, 150.0)       # horários marcados no mostrador (sem número)


def icone_relogio(cv, x, y, a, t, t0, r=40):
    if a <= 0:
        return
    cv.drawCircle(x, y + 4, r + 4, paint("#000000", int(70 * a), blur=8))
    cv.drawCircle(x, y, r, paint("#EEF3F8", int(255 * a)))
    cv.drawCircle(x, y, r, paint(OURO, int(255 * a), "stroke", 5))
    for k in range(12):                                            # tracinhos, nenhum número
        ang = math.radians(k * 30)
        r0 = r - (10 if k % 3 == 0 else 6)
        cv.drawLine(x + r0 * math.cos(ang), y + r0 * math.sin(ang), x + (r - 3) * math.cos(ang),
                    y + (r - 3) * math.sin(ang), paint("#5E7186", int(230 * a), "stroke", 2.5 if k % 3 == 0 else 1.6))
    for m in MARCAS:                                               # os horários certos: pontinhos dourados
        ang = math.radians(m)
        cv.drawCircle(x + (r - 17) * math.cos(ang), y + (r - 17) * math.sin(ang), 5.5, paint(OURO, int(255 * a)))
    k = t - t0                                                     # o ponteiro pula de marca em marca
    passo = 0.55
    i = int(max(0.0, k) // passo)
    f = e_back(clamp((max(0.0, k) - i * passo) / 0.22), 2.2)
    m0 = MARCAS[i % 3] + 360 * (i // 3)
    m1 = MARCAS[(i + 1) % 3] + 360 * ((i + 1) // 3)
    ang = math.radians(lerp(m0, m1, f) if k >= 0 else MARCAS[0])
    cv.drawLine(x, y, x + (r - 14) * math.cos(ang), y + (r - 14) * math.sin(ang), paint(NAVY, int(255 * a), "stroke", 5))
    cv.drawLine(x, y, x + (r * 0.45) * math.cos(math.radians(-150)), y + (r * 0.45) * math.sin(math.radians(-150)),
                paint(NAVY, int(255 * a), "stroke", 6.5))
    cv.drawCircle(x, y, 5, paint(NAVY, int(255 * a)))


TENDAO, TENDAO_B = "#DCE6F2", "#8FA3B8"


def icone_musculo(cv, x, y, a, t, t0):
    """Músculo esquemático sozinho: barriga fusiforme (larga no meio, afinando nas pontas) com fibras
    longitudinais e tendões curtos nas pontas; se espreguiça devagar (estica, afina e volta). Sem as
    setinhas e sem a cápsula lisa — fora do osso, a cápsula lia como comprimido."""
    if a <= 0:
        return
    k = max(0.0, t - t0)
    est = 0.5 - 0.5 * math.cos(2 * math.pi * k / 2.4)
    Lb = 90 + 14 * est; hb = 17 - 3.5 * est; tl = 16 + 3 * est
    xl, xr = x - Lb / 2, x + Lb / 2
    for sg, xe in ((-1, xl), (1, xr)):                             # tendões: cordão que AFINA até a ponta
        xt = xe + sg * tl
        q = skia.Path(); q.moveTo(xe - sg * 8, y - 4.2); q.lineTo(xt, y - 2.0)
        q.quadTo(xt + sg * 2.6, y, xt, y + 2.0); q.lineTo(xe - sg * 8, y + 4.2); q.close()
        cv.drawPath(q, paint(TENDAO, int(255 * a)))
        cv.drawPath(q, paint(TENDAO_B, int(230 * a), "stroke", 1.4))
    p = skia.Path()
    p.moveTo(xl, y - 5)
    p.cubicTo(xl + Lb * 0.22, y - hb * 1.4, xr - Lb * 0.3, y - hb * 1.3, xr, y - 5)
    p.lineTo(xr, y + 5)
    p.cubicTo(xr - Lb * 0.3, y + hb * 1.3, xl + Lb * 0.22, y + hb * 1.4, xl, y + 5)
    p.close()
    sh = skia.GradientShader.MakeLinear([skia.Point(0, y - hb), skia.Point(0, y + hb)],
                                        [C("#F7C3C8"), C(ROSA), C(ROSA_B)], [0.0, 0.45, 1.0])
    cv.drawPath(p, paint("#000000", int(60 * a), blur=7))
    cv.drawPath(p, paint(ROSA, int(255 * a), shader=sh))
    for f in (-0.66, -0.22, 0.22, 0.66):                           # fibras longitudinais
        q = skia.Path(); q.moveTo(xl + 6, y + f * 4)
        q.cubicTo(xl + Lb * 0.25, y + f * hb * 1.25, xr - Lb * 0.3, y + f * hb * 1.2, xr - 6, y + f * 4)
        cv.drawPath(q, paint(ROSA_B, int(200 * a), "stroke", 2.0))
    cv.drawPath(p, paint(ROSA_B, int(235 * a), "stroke", 2.5))


def icone_travesseiro(cv, x, y, a, t, t0):
    """Perna esquemática (sem anatomia além do contorno) que desce e fica APOIADA no travesseiro: o
    calcanhar descansa sobre ele, com o pé virado para cima (um 'L' arredondado, sem dedos), e a outra
    ponta na linha da cama (apoiada, não pendurada)."""
    if a <= 0:
        return
    k = t - t0
    desce = e_out(clamp(k / 0.45))
    amassa = math.sin(math.pi * clamp((k - 0.3) / 0.35)) if k > 0.3 else 0.0
    yc = y + 36                                                    # linha da cama
    cv.drawLine(x - 66, yc, x + 78, yc, paint("#8FA3B8", int(200 * a), "stroke", 3))
    # travesseiro (do lado direito), amassa um pouco quando a perna pousa
    px, py = x + 34, yc - 15
    cv.save(); cv.translate(px, yc); cv.scale(1 + 0.05 * amassa, 1 - 0.14 * amassa); cv.translate(-px, -yc)
    p = skia.Path()
    p.moveTo(px - 40, py); p.cubicTo(px - 44, py - 16, px - 24, py - 17, px, py - 16)
    p.cubicTo(px + 24, py - 17, px + 44, py - 16, px + 40, py)
    p.cubicTo(px + 44, py + 16, px + 24, py + 16, px, py + 15); p.cubicTo(px - 24, py + 16, px - 44, py + 16, px - 40, py)
    p.close()
    cv.drawPath(p, paint("#000000", int(60 * a), blur=8))
    cv.drawPath(p, paint("#DCE6F2", int(255 * a)))
    cv.drawPath(p, paint("#8FA3B8", int(255 * a), "stroke", 2.5))
    cv.restore()
    # perna: inclinada, calcanhar sobre o travesseiro e pé virado para cima
    alto = py - 16 - 13 + 3 * amassa
    x0, y0, x1, y1 = x - 60, yc - 12, x + 44, alto
    ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
    L = math.hypot(x1 - x0, y1 - y0)
    cv.save(); cv.translate(x0, y0 - 28 * (1 - desce)); cv.rotate(ang)
    perna = skia.Path(); perna.addRRect(skia.RRect.MakeRectXY(skia.Rect(-6, -13, L + 6, 13), 13, 13))
    pe = skia.Path(); pe.addRRect(skia.RRect.MakeRectXY(skia.Rect(L - 22, -13 - 26, L + 7, 13), 13, 13))
    forma = skia.Op(perna, pe, skia.PathOp.kUnion_PathOp) or perna
    sh = skia.GradientShader.MakeLinear([skia.Point(0, -13), skia.Point(0, 13)],
                                        [C("#F6C9B4"), C(PELE), C(PELE_B)], [0.0, 0.5, 1.0])
    cv.drawPath(forma, paint("#000000", int(60 * a), blur=6))
    cv.drawPath(forma, paint(PELE, int(255 * a), shader=sh))
    cv.drawPath(forma, paint(PELE_B, int(255 * a), "stroke", 2.5))
    cv.restore()


def icone_lua(cv, x, y, a, t, t0):
    if a <= 0:
        return
    k = t - t0
    lua(cv, x - 8, y + 2, 34, a)
    for i, (dx, dy, s) in enumerate(((34, -26, 7.5), (44, 16, 5.0))):
        tw = 0.75 + 0.25 * math.sin(t * 4 + i * 2.1)
        estrela(cv, x + dx, y + dy, s * e_back(clamp((k - 0.15 - 0.12 * i) / 0.3)) * tw, OURO, a)


# ------------------------------------------------------------------ ato 2: cartão, selo e camadas
CARD = (300, 270, 1030, 370)          # posição final (topo), depois que a moldura das camadas abre
CARD_DY0 = 330                        # antes: o cartão fica no meio da tela, ao lado do fixador


def card_dy(t, T):
    return CARD_DY0 * (1 - e_inout(prog(t, T["camadas"] - 0.25, T["camadas"] + 0.25)))
CK_X0, CK_X1, CK_Y0 = 50, 1030, 548
ROW_H, ROW_ESP, ROW_Y0 = 104, 10, 632
ITENS = (("MEDICAÇÃO EM HORÁRIOS CERTOS", "medicacao", icone_relogio),
         ("ALONGAMENTO MUSCULAR", "alongamento", icone_musculo),
         ("POSICIONAMENTO", "posicionamento", icone_travesseiro),
         ("SONO CUIDADO", "sono", icone_lua))


def row_c(i):
    return ROW_Y0 + ROW_H / 2 + i * (ROW_H + ROW_ESP)


def ck_y1():
    return row_c(3) + ROW_H / 2 + 22


def cartao_analgesia(cv, t, T, a):
    if a <= 0:
        return
    k = e_out(prog(t, T["analgesia"] + 0.22, T["analgesia"] + 0.62))
    dx = 90 * (1 - k)                                              # entra deslizando sem passar de x 1040
    a *= clamp(k * 2.5)
    x0, y0, x1, y1 = CARD
    dy = card_dy(t, T); y0 += dy; y1 += dy
    rr = skia.RRect.MakeRectXY(skia.Rect(x0 + dx, y0, x1 + dx, y1), 24, 24)
    cv.drawRRect(rr, paint("#000000", int(90 * a), blur=14))
    cv.drawRRect(rr, paint("#FFFFFF", int(250 * a)))
    texto(cv, "ANALGESIA E FISIOTERAPIA", (x0 + x1) / 2 + dx, (y0 + y1) / 2 + 15, F_BLACK, 40, NAVY, int(255 * a))


def selo_inicio(cv, t, T, a):
    if a <= 0:
        return
    k = prog(t, T["inicio"] - 0.12, T["inicio"] + 0.3)
    if k <= 0:
        return
    s = "DESDE O INÍCIO"; tam = 36
    lw = larg_texto(s, F_BLACK, tam); cx = (CARD[0] + CARD[2]) / 2
    base = CARD[3] + 22 + card_dy(t, T)
    y = base + 46 * (1 - e_back(k, 2.4))
    aa = a * clamp(k * 3)
    rr = skia.RRect.MakeRectXY(skia.Rect(cx - lw / 2 - 30, y, cx + lw / 2 + 30, y + tam + 22), 29, 29)
    for dx in (-90, 90):                                           # as duas presilhas que prendem o selo no cartão
        cv.drawRect(skia.Rect(cx + dx - 7, base - 28, cx + dx + 7, y + 8), paint("#C9D6E2", int(255 * aa)))
    cv.drawRRect(rr, paint("#000000", int(80 * aa), blur=10))
    cv.drawRRect(rr, paint(OURO, int(255 * aa)))
    cv.drawRRect(rr, paint("#8A5A00", int(255 * aa), "stroke", 2.5))
    texto(cv, s, cx, y + (tam + 22) / 2 + tam * 0.36, F_BLACK, tam, NAVY, int(255 * aa))
    # (os brilhos do "início" são desenhados em quadro(), ANTES do cartão: cartão e selo os cobrem)


def camadas(cv, t, T, a):
    if a <= 0:
        return
    ab = e_out(prog(t, T["camadas"] + 0.08, T["camadas"] + 0.5))
    if ab <= 0:
        return
    y1 = lerp(CK_Y0 + 84, ck_y1(), ab)
    rr = skia.RRect.MakeRectXY(skia.Rect(CK_X0, CK_Y0, CK_X1, y1), 28, 28)
    cv.drawRRect(rr, paint("#000000", int(90 * a), blur=16))
    cv.drawRRect(rr, paint(FUNDO_CX, int(225 * a)))
    cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 3))
    texto(cv, "EM CAMADAS", CX, CK_Y0 + 58, F_BLACK, 44, OURO, int(255 * a * clamp(ab * 2)))
    cv.save(); cv.clipRect(skia.Rect(CK_X0, CK_Y0, CK_X1, y1))
    brilho_meta = prog(t, T["controlada"], T["controlada"] + 0.3)
    for i, (rot, chave, icone) in enumerate(ITENS):
        yc = row_c(i)
        e_row = prog(t, T["camadas"] + 0.25 + 0.08 * i, T["camadas"] + 0.5 + 0.08 * i)
        if e_row <= 0:
            continue
        r = skia.RRect.MakeRectXY(skia.Rect(CK_X0 + 22, yc - ROW_H / 2, CK_X1 - 22, yc + ROW_H / 2), 18, 18)
        t_on = T[chave]
        cheio = prog(t, t_on - 0.08, t_on + 0.25)
        cv.drawRRect(r, paint("#16324A", int(255 * a * e_row * (0.55 + 0.45 * cheio))))
        p = paint("#FFFFFF", int(70 * a * e_row * (1 - cheio)), "stroke", 3)
        p.setPathEffect(skia.DashPathEffect.Make([14, 12], 0))
        cv.drawRRect(r, p)
        if cheio > 0:
            cv.drawRRect(r, paint(OURO, int(150 * a * cheio), "stroke", 2.5))
            # ícone
            pop = e_back(prog(t, t_on - 0.08, t_on + 0.3))
            cv.save(); cv.translate(150, yc); cv.scale(pop, pop); cv.translate(-150, -yc)
            icone(cv, 150, yc, a * clamp(cheio * 2), t, t_on)
            cv.restore()
            kx = e_out(prog(t, t_on, t_on + 0.35))
            texto(cv, rot, 244 + 30 * (1 - kx), yc + 13, F_BLACK, 34, "#FFFFFF", int(255 * a * kx), centro=False)
            # tique dourado
            bx = CK_X1 - 22 - 70
            cv.drawCircle(bx + 25, yc, 27, paint(FUNDO_CX, int(230 * a * cheio)))
            cv.drawCircle(bx + 25, yc, 27, paint(OURO, int(255 * a * cheio), "stroke", 3.5))
            tk = prog(t, t_on + 0.3, t_on + 0.6)
            if 0 < tk < 1:
                cv.drawCircle(bx + 25, yc, 30 + 22 * tk, paint(NOVO_G, int(110 * a * (1 - tk)), blur=8))
            tique(cv, bx + 27, yc + 2, tk, OURO, a)
            if brilho_meta > 0:                                    # "dor controlada": as 4 camadas acendem juntas
                g = brilho_meta * (0.6 + 0.4 * math.sin((t - T["controlada"]) * 6 - i * 0.7))
                cv.drawRRect(r, paint(OURO, int(90 * a * g), "stroke", 10, blur=8))
    cv.restore()


# ------------------------------------------------------------------ ato 3: o gráfico do alarme
GX0, GX_SP, GX1 = 70.0, 335.0, 985.0
Y_LO, Y_HI = 740.0, 400.0


def y_calmo(x, t):
    return Y_LO + 15 * math.sin((x - GX0) / 30.0 + 0.9 * t) + 6 * math.sin((x - GX0) / 13.0 - 0.6 * t)


def grafico(cv, t, T, a):
    if a <= 0:
        return
    t_ini = T["luxo"] + 0.25
    # trecho calmo, ondulado, desenhado da esquerda para a direita
    xc = lerp(GX0, GX_SP, prog(t, t_ini, T["dispara"]))
    p = skia.Path(); p.moveTo(GX0, y_calmo(GX0, t))
    x = GX0
    while x < xc:
        x = min(xc, x + 5); p.lineTo(x, y_calmo(x, t))
    cv.drawPath(p, paint(AMBAR_CL, int(90 * a), "stroke", 20, blur=9))
    cv.drawPath(p, paint(AMBAR_CL, int(255 * a), "stroke", 9))
    if xc < GX_SP:
        cv.drawCircle(xc, y_calmo(xc, t), 9, paint("#FFFFFF", int(255 * a)))
    # pico vertical: de repente
    ks = e_out(prog(t, T["dispara"], T["dispara"] + 0.16))
    if ks > 0:
        y0 = y_calmo(GX_SP, t)
        xs = GX_SP + 18 * ks; ys = lerp(y0, Y_HI, ks)
        kp = prog(t, T["repente"] - 0.1, T["cede"] + 0.75)
        xp = lerp(GX_SP + 18, GX1, kp)
        q = skia.Path(); q.moveTo(GX_SP, y0); q.lineTo(xs, ys)
        if kp > 0:
            q.lineTo(xp, Y_HI + 1.5 * math.sin(t * 3))
        pulso = 0.6 + 0.4 * math.sin((t - T["dispara"]) * 7)
        acende = prog(t, T["dispara"] + 0.05, T["dispara"] + 0.3)
        cv.drawPath(q, paint(CORAL, int(150 * a * acende * pulso), "stroke", 36, blur=18))
        cv.drawPath(q, paint(CORAL, int(255 * a), "stroke", 10))
        ponta = (xp, Y_HI) if kp > 0 else (xs, ys)
        cv.drawCircle(ponta[0], ponta[1], 10, paint("#FFFFFF", int(255 * a)))
        # o pico "acende": um clarão no topo
        kf = t - T["dispara"] - 0.12
        if 0 <= kf < 0.6:
            cv.drawCircle(GX_SP + 18, Y_HI, 20 + 70 * e_out(kf / 0.6), paint(CORAL, int(170 * a * (1 - kf / 0.6)), "stroke", 6))
        ko = t - T["ou"]                                           # "ou": o pico pulsa sozinho (1º sinal, por si só)
        if 0 <= ko < 0.5:
            cv.drawCircle(GX_SP + 18, Y_HI, 16 + 46 * e_out(ko / 0.5), paint("#FFFFFF", int(210 * a * (1 - ko / 0.5)), "stroke", 5))
    # seta: a linha sai do platô e desce até o cartão
    kseta = e_inout(prog(t, T["avise"] - 0.05, T["avise"] + 0.35))
    if kseta > 0:
        P0, C1, C2, P3 = (GX1, Y_HI), (1042.0, Y_HI), (1042.0, (AV[1] + AV[3]) / 2), (1000.0, (AV[1] + AV[3]) / 2)
        sp = skia.Path(); sp.moveTo(*P0)
        n = 40; ult = P0; pen = P0
        for i in range(1, int(n * kseta) + 1):
            u = i / n
            bx = (1 - u) ** 3 * P0[0] + 3 * (1 - u) ** 2 * u * C1[0] + 3 * (1 - u) * u ** 2 * C2[0] + u ** 3 * P3[0]
            by = (1 - u) ** 3 * P0[1] + 3 * (1 - u) ** 2 * u * C1[1] + 3 * (1 - u) * u ** 2 * C2[1] + u ** 3 * P3[1]
            pen, ult = ult, (bx, by)
            sp.lineTo(bx, by)
        cv.drawPath(sp, paint("#FFFFFF", int(235 * a), "stroke", 7))
        if kseta > 0.08:
            ang = math.atan2(ult[1] - pen[1], ult[0] - pen[0])
            cv.save(); cv.translate(*ult); cv.rotate(math.degrees(ang))
            hp = skia.Path(); hp.moveTo(14, 0); hp.lineTo(-16, -17); hp.lineTo(-16, 17); hp.close()
            cv.drawPath(hp, paint("#FFFFFF", int(255 * a)))
            cv.restore()


def telefone(cv, x, y, a, toque, t, cor=NAVY):
    """Fone genérico (do cf_osteomielite), sem logotipo de aplicativo."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(1.25, 1.25); cv.rotate(-28 + 9 * math.sin(t * 46) * toque)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-24, -42, 4, -22), 8, 8), paint(cor, int(255 * a)))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-24, 22, 4, 42), 8, 8), paint(cor, int(255 * a)))
    p = skia.Path(); p.moveTo(-14, -30); p.quadTo(-40, 0, -14, 30)
    cv.drawPath(p, paint(cor, int(255 * a), "stroke", 14))
    cv.restore()
    if toque > 0:
        for i in range(2):
            f = ((t * 1.8) + i * 0.5) % 1.0
            r = 30 + 22 * f
            cv.drawArc(skia.Rect(x - r + 14, y - r, x + r + 14, y + r), -40, 80, False,
                       paint(OURO, int(255 * a * toque * (1 - f)), "stroke", 4))


def termometro(cv, x, y, nivel, a, esc=1.0):
    """Termômetro simples, sem número (do cf_osteomielite), em branco sobre o coral."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-12, -48, 12, 24), 12, 12), paint("#FFFFFF", int(255 * a)))
    cv.drawCircle(0, 32, 19, paint("#FFFFFF", int(255 * a)))
    cv.drawCircle(0, 32, 12, paint("#8E1B22", int(255 * a)))
    h = lerp(6, 64, clamp(nivel))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-5, 26 - h, 5, 32), 5, 5), paint("#8E1B22", int(255 * a)))
    cv.restore()


def sinal_mais(cv, x, y, lado, a):
    """Sinal de mais BRANCO estilizado direto sobre o coral (não é a cruz vermelha sobre branco)."""
    if a <= 0:
        return
    b = lado * 0.15; L = lado * 0.5
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - b, y - L, x + b, y + L), b, b), paint("#FFFFFF", int(255 * a)))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - L, y - b, x + L, y + b), b, b), paint("#FFFFFF", int(255 * a)))


AV = (110, 872, 990, 984)            # cartão AVISE A EQUIPE
FB = (70, 1014, 1010, 1134)           # cartão COM FEBRE, PRONTO-SOCORRO


def cartoes_alarme(cv, t, T, a):
    if a <= 0:
        return
    k = prog(t, T["avise"] + 0.2, T["avise"] + 0.5)
    if k > 0:
        aa = a * k; dy = 30 * (1 - e_out(k))
        x0, y0, x1, y1 = AV
        rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0 + dy, x1, y1 + dy), 26, 26)
        cv.drawRRect(rr, paint("#000000", int(90 * aa), blur=14))
        cv.drawRRect(rr, paint("#FFFFFF", int(250 * aa)))
        toque = prog(t, T["equipe"], T["equipe"] + 0.15) * (1 - prog(t, T["equipe"] + 1.6, T["equipe"] + 2.0))
        telefone(cv, x0 + 82, (y0 + y1) / 2 + dy, aa, toque, t)
        texto(cv, "AVISE A EQUIPE", x0 + 150, (y0 + y1) / 2 + dy + 16, F_BLACK, 46, NAVY, int(255 * aa), centro=False)
    k = prog(t, T["febre"] - 0.08, T["febre"] + 0.3)
    if k > 0:
        aa = a * k
        x0, y0, x1, y1 = FB
        pop = lerp(0.9, 1.0, e_back(k))
        pulso = 1 + 0.025 * math.sin((t - T["pronto"]) * 8) if t >= T["pronto"] else 1.0
        cxm, cym = (x0 + x1) / 2, (y0 + y1) / 2
        cv.save(); cv.translate(cxm, cym); cv.scale(pop * pulso, pop * pulso); cv.translate(-cxm, -cym)
        rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 26, 26)
        if t >= T["pronto"]:
            cv.drawRRect(rr, paint(CORAL, int(110 * aa * (0.6 + 0.4 * math.sin((t - T["pronto"]) * 8))), blur=18))
        cv.drawRRect(rr, paint("#000000", int(90 * aa), blur=14))
        cv.drawRRect(rr, paint(CORAL_ESC, int(255 * aa)))
        cv.drawRRect(rr, paint("#FFB3AC", int(255 * aa), "stroke", 3))
        termometro(cv, x0 + 56, cym - 6, e_out(prog(t, T["febre"], T["febre"] + 0.8)) * 0.9, aa, 0.82)
        sinal_mais(cv, x0 + 128, cym, 50 * e_back(prog(t, T["pronto"] - 0.1, T["pronto"] + 0.25)), aa)
        texto(cv, "COM FEBRE, PRONTO-SOCORRO", x0 + 178, cym + 15, F_BLACK, 40, "#FFFFFF", int(255 * aa), centro=False)
        cv.restore()


# ------------------------------------------------------------------ ato 4: a conversa
BAL = (330, 252, 1010, 466)
BAL_PONTA = (372, 572)


def sai_cta(t, T):
    """Tudo o que tem texto ou fica atrás das linhas da CTA (etiqueta, balão, NÃO SE AGUENTA, pilha e
    carimbo) sai ANTES de a CTA aparecer: atrás dela fica só o fantasma do fixador."""
    return 1 - prog(t, T["manda"] - 0.4, T["manda"] - 0.1)


def balao(cv, t, T, a):
    a *= sai_cta(t, T)                                              # sai antes da CTA (ficava colado nela)
    if a <= 0:
        return
    esc = e_back(prog(t, T["conversa"] - 0.1, T["conversa"] + 0.35), 1.0)
    if esc <= 0:
        return
    x0, y0, x1, y1 = BAL
    px, py = BAL_PONTA
    cv.save(); cv.translate(px, py); cv.scale(esc, esc); cv.translate(-px, -py)
    corpo = skia.Path(); corpo.addRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 44, 44))
    rabo = skia.Path(); rabo.moveTo(x0 + 70, y1 - 10); rabo.lineTo(x0 + 150, y1 - 10); rabo.lineTo(px, py); rabo.close()
    forma = skia.Op(corpo, rabo, skia.PathOp.kUnion_PathOp) or corpo
    cv.drawPath(forma, paint("#000000", int(100 * a), blur=16))
    cv.drawPath(forma, paint("#FFFFFF", int(252 * a)))
    texto(cv, "DOR SE CONVERSA", (x0 + x1) / 2, (y0 + y1) / 2 + 21, F_BLACK, 58, NAVY, int(255 * a))
    cv.restore()
    k = prog(t, T["aguenta"] - 0.08, T["aguenta"] + 0.3)
    if k > 0:
        texto(cv, "NÃO SE AGUENTA", (x0 + x1) / 2, y1 + 70 - 16 * e_out(k), F_BLACK, 40, "#FFFFFF",
              int(255 * a * k), contorno=8)


PILHA_X0, PILHA_X1, PILHA_Y0, PILHA_H, PILHA_ESP = 800, 1020, 858, 70, 12


def pilha_mini(cv, t, T, a):
    """Antes da CTA: as 4 camadas (só ícones e tiques) e o carimbo, ao lado do fixador e do balão."""
    sai = sai_cta(t, T)                                             # sai INTEIRA antes da CTA
    a *= sai
    if a <= 0:
        return
    t0 = T["aguenta"] + 0.45
    icones = (icone_relogio, icone_musculo, icone_travesseiro, icone_lua)
    for i, ic in enumerate(icones):
        k = e_out(prog(t, t0 + 0.07 * i, t0 + 0.07 * i + 0.4))
        if k <= 0:
            continue
        y = PILHA_Y0 + i * (PILHA_H + PILHA_ESP); dx = 160 * (1 - k)
        rr = skia.RRect.MakeRectXY(skia.Rect(PILHA_X0 + dx, y, PILHA_X1 + dx, y + PILHA_H), 16, 16)
        cv.drawRRect(rr, paint(FUNDO_CX, int(230 * a * k)))
        cv.drawRRect(rr, paint(OURO, int(220 * a * k), "stroke", 2.5))
        cx, cy = PILHA_X0 + 70 + dx, y + PILHA_H / 2
        cv.save(); cv.translate(cx, cy); cv.scale(0.62, 0.62); cv.translate(-cx, -cy)
        ic(cv, cx, cy, a * k, t, T["aguenta"])
        cv.restore()
        tique(cv, PILHA_X1 - 46 + dx, cy + 2, 1.0, OURO, a * k)
    if sai < 1:
        cv.saveLayerAlpha(None, int(255 * sai))
    carimbo_cor(cv, "META DE TRATAMENTO", 815, PILHA_Y0 - 30, -5, T["aguenta"] + 0.8, t, OURO,
                dur=T["total"] + 1 - T["aguenta"], tam=30, esc0=1.3, fundo_a=210)
    if sai < 1:
        cv.restore()


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    cam = camera(t, T)
    g = vao(t, T)
    y_an = aneis_y(g)

    tremor = 0.0
    for t0, f in ((T["doi"], 5), (T["comuns"], 5), (T["meta"], 6), (T["dispara"] + 0.1, 7), (T["febre"], 4)):
        k = t - t0
        if 0 <= k < 0.35:
            tremor += f * math.sin(k * 70) * (1 - k / 0.35)
    cv.save(); cv.translate(tremor, 0)

    # ================= ato 1: o aparelho, a pergunta e o que é comum
    ccx, ccy = na_tela(cam, CX, 690)
    ondas(cv, ccx, ccy, 190 * cam[1] / 0.8, 380 * cam[1] / 0.8, t, T["pressao"] - 0.05, AMBAR_CL, n=3, dur=1.1)
    a_m = alfa_mundo(t, T)
    musc = prog(t, T["muscular"] - 0.05, T["muscular"] + 0.35) * (1 - prog(t, T["analgesia"] - 0.1, T["analgesia"] + 0.25))
    if a_m > 0:
        if a_m < 1:
            cv.saveLayerAlpha(None, int(255 * a_m))
        mundo(cv, t, T, cam, g, musc)
        if a_m < 1:
            cv.restore()
    mx, my = na_tela(cam, MUSC_X, (MUSC_Y0 + MUSC_Y1) / 2)
    ondas(cv, mx, my, 62, 120, t, T["muscular"] + 0.1, AMBAR_CL, n=3, dur=0.9, esp=0.2, larg=4)
    brilhos(cv, *na_tela(cam, CX, Y_CORTE + g / 2), t, T["ajuste"] + 0.32, n=10, raio=110)

    # o espanto: a interrogação cai ao lado do aparelho e balança uma vez
    qx, qy = 218.0, 990.0
    k = t - (T["doi"] - 0.26)
    if k >= 0 and t < T["desconforto"] + 0.3:
        cai = clamp(k / 0.26)
        y = qy - 300 * (1 - cai * cai)
        kk = k - 0.26
        amassa = 0.12 * math.sin(math.pi * clamp(kk / 0.18)) if kk > 0 else 0.0
        ang = 16 * math.exp(-3.0 * kk) * math.sin(8.5 * kk) if kk > 0 else 0.0
        some = e_inout(prog(t, T["desconforto"] - 0.12, T["desconforto"] + 0.16))
        aq = clamp(k / 0.1) * (1 - some) ** 1.5
        if kk > 0:                                                 # o pouso: anel no chão e risquinhos de impacto
            ki = clamp(kk / 0.45)
            if ki < 1:
                rx = 40 + 90 * e_out(ki)
                cv.drawOval(skia.Rect(qx - rx, qy - rx * 0.22, qx + rx, qy + rx * 0.22),
                            paint("#FFFFFF", int(150 * (1 - ki) * aq), "stroke", 4))
                for sg in (-1, 1):
                    for j in range(3):
                        x0 = qx + sg * (58 + 30 * e_out(ki)); yy = qy - 18 - j * 26
                        cv.drawLine(x0, yy, x0 + sg * 24, yy - 8 + j * 4,
                                    paint("#FFFFFF", int(210 * (1 - ki) * aq), "stroke", 4.5))
        if some <= 0:
            cv.drawCircle(qx, y - 130, 120, paint(OURO, int(40 * aq), blur=40))
            cv.save(); cv.translate(qx, y); cv.scale(1 + amassa * 0.6, 1 - amassa); cv.translate(-qx, -y)
            interrogacao(cv, qx, y, 1.3, ang, aq)
            cv.restore()
        else:
            # a interrogação ENCOLHE DENTRO da etiqueta que nasce: o centro do glifo viaja até o centro
            # do texto DESCONFORTO e a escala/giro acontecem em torno dele
            d = Q_CENTRO * 1.3; ra = math.radians(ang)
            c0x, c0y = qx + d * math.sin(ra), y - d * math.cos(ra)
            tcx, tcy = centro_etiqueta("DESCONFORTO", *na_tela(cam, CX - RX2, y_an[1]), -1, TAM_TAG)
            gx, gy = lerp(c0x, tcx, some), lerp(c0y, tcy, some)
            cv.drawCircle(gx, gy, 120 * (1 - some) + 30, paint(OURO, int(40 * aq), blur=40))
            interrogacao(cv, gx, gy, 1.3 * (1.0 - some), ang + 140 * some, aq, centro=True)

    fim12 = 1 - prog(t, T["ajuste"] - 0.35, T["ajuste"] - 0.05)
    ax, ay = na_tela(cam, CX - RX2, y_an[1])
    k = prog(t, T["desconforto"], T["desconforto"] + 0.37)
    etiqueta_pend(cv, "DESCONFORTO", ax, ay, -1, clamp(k * 3) * fim12, balanco(t, T["desconforto"] + 0.1),
                  FUNDO_CX, AMBAR_T, AMBAR_T, ent=e_back(k), tam=TAM_TAG)
    bx, by = na_tela(cam, CX + RX2, y_an[1])
    k = prog(t, T["manejo"] - 0.02, T["manejo"] + 0.35)
    etiqueta_pend(cv, "MANEJO", bx, by, +1, clamp(k * 3) * fim12, -balanco(t, T["manejo"] + 0.1),
                  FUNDO_CX, TEAL, TEAL, ent=e_back(k), tam=TAM_TAG)

    fim1 = 1 - prog(t, T["analgesia"] - 0.15, T["analgesia"] + 0.2)
    tx, ty = na_tela(cam, CX + RX2, y_an[0])
    k = prog(t, T["ajuste"] - 0.02, T["ajuste"] + 0.35)
    if t < T["dor4"] - 0.3:
        etiqueta_pend(cv, "DIAS DE AJUSTE", tx, ty, +1, clamp(k * 3) * fim1, balanco(t, T["ajuste"] + 0.1, 12),
                      PAPEL, PAPEL_B, TINTA, ent=e_back(k), papel=True)
    a = prog(t, T["pressao"] + 0.05, T["pressao"] + 0.35) * fim1
    etiqueta(cv, "PRESSÃO", 646, 646, None, AMBAR_CL, a)
    a = prog(t, T["muscular"] + 0.15, T["muscular"] + 0.45) * fim1
    etiqueta(cv, "DOR MUSCULAR", 646, 728, na_tela(cam, MUSC_X + MUSC_L / 2, 650), ROSA, a)
    carimbo_cor(cv, "SÃO COMUNS", 812, 872, -6, T["comuns"], t, NEUTRO, dur=T["analgesia"] + 0.15 - T["comuns"],
                tam=46, esc0=1.5, fundo_a=190)

    # ================= ato 2: analgesia e fisioterapia; as camadas; meta
    a2 = prog(t, T["analgesia"] - 0.05, T["analgesia"] + 0.3) * (1 - prog(t, T["luxo"] + 0.1, T["luxo"] + 0.4))
    a_card = a2 * (1 - prog(t, T["meta"] - 0.45, T["meta"] - 0.05))
    if a_card > 0:                                                 # brilhos ATRÁS do cartão e do selo (só em volta)
        brilhos(cv, (CARD[0] + CARD[2]) / 2, CARD[3] + 22 + card_dy(t, T) + 28, t, T["inicio"] + 0.18, n=10, raio=200)
    cartao_analgesia(cv, t, T, a_card)
    selo_inicio(cv, t, T, a_card)
    camadas(cv, t, T, a2)
    carimbo_cor(cv, "META DE TRATAMENTO", CX, 500, -4, T["meta"], t, OURO, dur=T["luxo"] + 0.4 - T["meta"],
                tam=48, esc0=1.5, fundo_a=200)

    # ================= ato 3: o alarme
    a3 = prog(t, T["luxo"] + 0.2, T["luxo"] + 0.45) * (1 - prog(t, T["dor4"] - 0.35, T["dor4"] - 0.05))
    grafico(cv, t, T, a3)
    etiqueta(cv, "DESCONFORTO", 70, 784, None, AMBAR_T, a3 * prog(t, T["luxo"] + 0.45, T["luxo"] + 0.75), tam=40)
    # "OU": dois gatilhos SEPARADOS. No "ou" o pico pulsa sozinho; no "avise" os DOIS rótulos pulsam
    # juntos enquanto a seta desenha (cada sinal, sozinho, já é motivo de aviso).
    h_av = math.sin(math.pi * prog(t, T["avise"] - 0.05, T["avise"] + 0.55))
    h_ou = math.sin(math.pi * prog(t, T["ou"] - 0.05, T["ou"] + 0.35))
    etiqueta(cv, "DISPARA DE REPENTE", 372, 290, None, CORAL, a3 * prog(t, T["dispara"] + 0.12, T["dispara"] + 0.42),
             tam=40, halo=max(h_av, h_ou))
    etiqueta(cv, "NÃO CEDE COM A MEDICAÇÃO", 372, 434, None, "#FFFFFF", a3 * prog(t, T["cede"] + 0.1, T["cede"] + 0.4),
             tam=34, halo=h_av)
    cartoes_alarme(cv, t, T, a3)

    # ================= ato 4: dor se conversa
    a4 = prog(t, T["dor4"] - 0.3, T["dor4"])
    if a4 > 0:
        tx, ty = na_tela(cam, CX + RX2, y_an[0])
        k = prog(t, T["conversa"] + 0.05, T["conversa"] + 0.4)
        etiqueta_pend(cv, "DIAS DE AJUSTE", tx, ty, +1, a4 * clamp(k * 3) * sai_cta(t, T),
                      balanco(t, T["conversa"] + 0.15, 9),
                      PAPEL, PAPEL_B, TINTA, ent=e_back(k), papel=True)
        balao(cv, t, T, a4)
        pilha_mini(cv, t, T, a4)
    cv.restore()

    capa(cv, t, T["manejo"] + 0.2, ep["gancho"][0], ep["gancho"][1])
    selo_como_funciona(cv, prog(t, T["manejo"] + 0.6, T["manejo"] + 1.0) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface(cv, t, T, blocos, DESTAQUE)


# ------------------------------------------------------------------ som e prévias
def sons(T):
    ev = [(T["doi"] - 0.02, "thump", 0.75), (T["doi"] + 0.05, "pop", 0.4),
          (T["desconforto"], "whoosh", 0.35), (T["desconforto"] + 0.12, "pop", 0.5),
          (T["manejo"] + 0.12, "pop", 0.5), (T["manejo"] + 0.2, "ding", 0.35),
          (T["ajuste"], "whoosh", 0.3), (T["ajuste"] + 0.12, "pop", 0.4), (T["ajuste"] + 0.3, "click", 0.7),
          (T["ajuste"] + 0.34, "shimmer", 0.35),
          (T["pressao"], "whoosh", 0.3), (T["pressao"] + 0.25, "whoosh", 0.22),
          (T["muscular"], "pop", 0.35), (T["comuns"], "thump", 0.8),
          (T["analgesia"] - 0.05, "whoosh", 0.6), (T["analgesia"] + 0.25, "pop", 0.45),
          (T["inicio"] + 0.05, "tick", 0.8), (T["inicio"] + 0.18, "ding", 0.5),
          (T["camadas"] - 0.2, "whoosh", 0.4)]
    for i in range(4):
        ev.append((T["camadas"] + 0.42 + 0.08 * i, "tick", 0.25))
    for ch in ("medicacao", "alongamento", "posicionamento", "sono"):
        ev += [(T[ch] - 0.02, "pop", 0.5), (T[ch] + 0.35, "tick", 0.55)]
    for j in range(1, 4):                                          # o ponteiro do relógio pulando de marca em marca
        ev.append((T["medicacao"] + 0.55 * j, "tick", 0.25))
    ev += [(T["sono"] + 0.2, "shimmer", 0.4), (T["controlada"], "shimmer", 0.45),
           (T["meta"], "thump", 0.9), (T["meta"] + 0.08, "ding", 0.5),
           (T["luxo"] + 0.3, "whoosh", 0.45), (T["dispara"], "whoosh", 0.55), (T["dispara"] + 0.12, "thump", 0.85),
           (T["ou"], "tick", 0.35), (T["cede"] + 0.1, "tick", 0.5), (T["avise"] - 0.05, "whoosh", 0.45), (T["avise"] + 0.3, "pop", 0.5),
           (T["equipe"], "ping", 0.55), (T["equipe"] + 0.45, "ping", 0.45),
           (T["febre"] - 0.05, "thump", 0.7), (T["pronto"], "ding", 0.45),
           (T["dor4"] - 0.15, "whoosh", 0.55), (T["conversa"] - 0.05, "pop", 0.55),
           (T["conversa"] + 0.2, "pop", 0.3), (T["aguenta"], "pop", 0.4),
           (T["aguenta"] + 0.45, "whoosh", 0.35), (T["aguenta"] + 0.8, "thump", 0.6),
           (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def tempos_previa(T):
    return [0.0, T["doi"] + 0.45, T["manejo"] + 0.4, T["ajuste"] + 1.0, T["comuns"] + 0.4, T["inicio"] + 0.5,
            T["posicionamento"] + 0.6, T["meta"] + 0.5, T["avise"] + 0.3, T["febre"] + 0.9, T["aguenta"] + 1.3,
            T["manda"] + 1.6]


render = fazer_render(quadro, ANCORAS, sons, tempos_previa, respiro_cta=2.2)   # ~1,5 s de plano aberto antes da CTA
