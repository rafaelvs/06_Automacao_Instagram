# -*- coding: utf-8 -*-
"""COMO FUNCIONA — fisioterapia no alongamento ósseo ("O OSSO ALONGA. / E A ARTICULAÇÃO?").

Mesmo estilo e mesmas peças do cf_alongamento (osso marfim, osso novo dourado, anel/fio/haste do
fixador, brilhos, carimbos, legenda karaokê, CTA com aviãozinho). O que a cena mostra, cada coisa
disparada pela palavra falada:
  * capa: a tíbia esquemática JÁ dividida em duas partes por uma fenda fina (o corte é assunto do
    cf_alongamento e não acontece aqui);
  * "fixador": 4 anéis encaixam, fios até o osso; "milímetro": as pontas se afastam um clique por
    milímetro e o vão se enche de osso novo dourado — e esse relógio NÃO para: o vão segue abrindo,
    devagar, ao fundo de tudo o que acontece depois (o contraste é o espanto da peça);
  * "novo": o osso novo pulsa; "articulação": dobradiça SIMBÓLICA no topo do osso (pino de aço,
    bastão marfim curto, arco tracejado do quanto dobra) — nenhum joelho, cartilagem ou anatomia;
  * "parados": carimbo, a dobradiça congela enquanto o vão continua abrindo; "enrijecer": o arco
    encolhe até uma fatia, o pino fica cinza, cadeado;
  * "músculo": faixa rosada e lisa AO LADO do segmento de cima — não atravessa o vão (o roteiro não
    diz que o músculo estica junto); "encolher": a faixa afina sem mudar de comprimento;
  * "rigidez"/"rouba"/"ganho": um bloco cinza RIGIDEZ sai do cadeado e morde uma barra abstrata
    VERDE-ÁGUA "GANHO" (nunca dourada: dourado é osso novo), separada do osso, sem número nem régua;
    o vão dourado não muda (a rigidez não come osso);
  * "fisioterapia": PRIMEIRO o ícone de rebobinar e o filme INTEIRO volta em marcha a ré (barra,
    bloco, músculo, dobradiça, vão e fixador) até a capa; SÓ DEPOIS, sobre a cena zerada, bate o
    carimbo FISIOTERAPIA — lê-se "o filme voltou ao começo", nunca "a fisioterapia desfaz a rigidez"
    nem "fecha o osso";
  * "início": o fixador volta, o vão recomeça a abrir e a dobradiça já se mexe desde o 1º clique;
    "movimento": ela percorre o arco inteiro, em loop (nenhum exercício específico); "carga": seta
    grossa pressiona o topo; "dose": mostrador sem número, o ponteiro para na faixa do meio;
    "solta": o arco acende inteiro; "fortalecem": pontinhos dourados se juntam no vão e o osso novo
    fica mais denso (nada de osso translúcido ou de imagem de exame);
  * "treino": um halter cai no canto; "pesado": X vermelho; "pouco": 7 quadradinhos recebem um
    tique por vez (sem dia, sem número); "equipe": carimbo GUIADO PELA EQUIPE fecha a fileira;
  * "manda": plano aberto por trás da CTA, o vão ainda crescendo e a dobradiça balançando.
Todo texto desenhado está em ep["tela"] (o render recusa o vídeo se não estiver).
"""
import math

import numpy as np
import skia

from .cf_comum import capa, carimbo as carimbo_ouro, fazer_render, interface, selo_como_funciona
from .cf_alongamento import (ACO, ACO_ESC, ACO_HL, CX, F_BLACK, HASTE, NOVO_G, OSSO_B, OSSO_C, OSSO_L, OURO,
                             VERMELHO, W, H, C, brilhos, clamp, desenha_regenerado, e_back, e_inout, e_out,
                             fundo, haste, larg_texto, lerp, lerpc, paint, path_osso_inf, path_osso_sup, porca,
                             prog, sombra_osso, texto)

ANCORAS = {
    "alongamento": ("alongamento", 1, False),
    "fixador": ("fixador", 1, False), "milimetro": ("milímetro", 1, False), "novo": ("novo", 1, False),
    "art": ("articulação", 1, False), "parados": ("parados", 1, False), "enrijecer": ("enrijecer", 1, False),
    "musculo": ("músculo", 1, False), "encolher": ("encolher", 1, False), "rigidez": ("rigidez", 1, False),
    "rouba": ("rouba", 1, False), "ganho": ("ganho", 1, False), "fisio": ("fisioterapia", 1, False),
    "desde": ("desde", 1, False), "inicio": ("início", 1, False), "movimento": ("movimento", 1, False), "carga": ("carga", 1, False),
    "dose": ("dose", 1, False), "solta": ("solta", 1, False), "fortalecem": ("fortalecem", 1, False),
    "treino": ("treino", 1, False), "pesado": ("pesado", 1, False), "pouco": ("pouco", 1, False),
    "equipe": ("equipe", 1, False), "manda": ("manda", 1, False),
}
DESTAQUE = {"fixador", "milímetro", "novo", "articulação", "parados", "enrijecer", "músculo", "encolher",
            "rigidez", "rouba", "fisioterapia", "início", "movimento", "carga", "dose", "solta", "fortalecem",
            "pouco", "equipe"}

# ------------------------------------------------------------------ paleta própria
TEAL = "#4FD1C5"            # verde-água: movimento/ganho (NUNCA dourado — dourado é osso novo)
ROSA, ROSA_B = "#F2A3AA", "#C2707A"
CINZA, CINZA_C = "#6E7782", "#B8C2CC"
AMBAR = "#7A5420"           # base opaca do osso novo (nada translúcido)
FERRO, FERRO_HL = "#353C46", "#7C8794"
FUNDO_CX = "#0B1824"

# ------------------------------------------------------------------ geometria (mundo, antes da câmera)
Y_TOPO, Y_CORTE, Y_BASE = 300, 740, 1000
FENDA = 6
H2 = HASTE / 2
RX2, RY2 = 175, 38
X_HASTE = 158
Y_AN0, Y_AN1 = 390, Y_CORTE - 75
PX_MM = 5.5                 # escala esquemática do vão (NÃO vai para a tela)
PER = 0.62                  # segundos por "milímetro" na animação (um clique cada)
PINO = (CX, Y_TOPO - 6)
R_PINO, L_BARRA, R_BARRA, R_ARCO = 20, 168, 26, 208
A_CHEIO, A_RIGIDO = 50.0, 9.0
CADEADO = (CX + 86, Y_TOPO - 100)
MUSC_X, MUSC_Y0, MUSC_Y1 = CX + 110, 545, 730   # bordas a 79-141 px do eixo: livre da diáfise e das hastes
MUSC_CHEIO, MUSC_FINO = 62.0, 22.0

# câmera: (x na tela do eixo do osso, escala, y na tela do ponto YW do mundo)
YW = 600.0
CAM_CAPA = (540.0, 0.92, 696.0)      # capa: osso no centro, abaixo do gancho
CAM_LADO = (300.0, 0.84, 763.0)      # osso à esquerda: libera a coluna da direita (x >= 500)
CAM_FIM = (540.0, 0.74, 708.0)       # plano aberto atrás da CTA

# peças de tela (coluna da direita)
BARRA = (540, 650, 960, 706)          # GANHO: x0, y0, x1, y1
PEDACO = 130                          # o pedaço mordido (sem número na tela)
BLOCO = (895, 604)                    # repouso do bloco RIGIDEZ (acima do pedaço)
MOSTRADOR = (770, 800, 120)           # cx, cy, raio
HALTER = (770, 462)
FILEIRA_Y = 726


def mix_cam(c1, c2, a):
    return tuple(lerp(c1[i], c2[i], a) for i in range(3))


def na_tela(cam, x, y):
    px, s, ys = cam
    return px + (x - CX) * s, ys + (y - YW) * s


def mm_degraus(t, t0):
    """Milímetros já abertos: um degrau por clique (anda e para), ritmo constante."""
    if t < t0:
        return 0.0
    i = math.floor((t - t0) / PER)
    return i + e_inout(clamp((t - t0 - i * PER) / 0.3))


def clique(t, t0):
    """Lampejo do osso novo a cada clique: o relógio do alongamento à vista."""
    if t < t0:
        return 0.0
    f = ((t - t0) % PER) / PER
    return 0.5 * max(0.0, 1 - f * 3.5)


def janela_volta(T):
    return T["fisio"] - 0.12, T["fisio"] + 0.6


# ------------------------------------------------------------------ estado do mundo
def est1(T, u, t):
    """1º filme (fixador -> rigidez rouba o ganho), em função do tempo de filme `u` (que corre para
    trás no rebobinar)."""
    fx = T["fixador"]
    e = {"aneis": [e_back(prog(u, fx + 0.07 * i, fx + 0.07 * i + 0.5)) for i in range(4)],
         "fios": [prog(u, fx + 0.35 + 0.05 * i, fx + 0.6 + 0.05 * i) for i in range(4)],
         "hastes": prog(u, fx + 0.3, fx + 0.7)}
    mm = mm_degraus(u, T["milimetro"])
    e["mm"] = mm
    e["dens"] = 0.62 * clamp(mm)
    pulso = prog(u, T["novo"] - 0.1, T["novo"] + 0.25) * (1 - prog(u, T["novo"] + 1.0, T["novo"] + 2.0))
    e["brilho"] = max(0.3 * clamp(mm), pulso, clique(u, T["milimetro"]) * clamp(mm))
    e["firme"] = 0.0
    e["fenda"] = max(0.0, 1 - abs(u - (T["alongamento"] + 0.3)) / 0.45)
    a0 = T["art"]
    e["dob"] = e_back(prog(u, a0, a0 + 0.45))
    e["arco"] = prog(u, a0 + 0.15, a0 + 0.6)
    e["A"] = lerp(A_CHEIO, A_RIGIDO, e_inout(prog(u, T["enrijecer"], T["enrijecer"] + 0.6)))
    amp = 36 * prog(u, a0 + 0.35, a0 + 0.6) * (1 - e_inout(prog(u, T["parados"] - 0.15, T["parados"] + 0.25)))
    e["theta"] = amp * math.sin(2 * math.pi * (u - a0 - 0.35) / 1.3)
    e["cinza"] = prog(u, T["enrijecer"] + 0.1, T["enrijecer"] + 0.6)
    e["cadeado"] = e_back(prog(u, T["enrijecer"] + 0.3, T["enrijecer"] + 0.65))
    e["aceso"] = 0.0
    e["musc"] = prog(u, T["musculo"], T["musculo"] + 0.4)
    e["musc_l"] = lerp(MUSC_CHEIO, MUSC_FINO, e_inout(prog(u, T["encolher"], T["encolher"] + 0.7)))
    e["setas"] = prog(u, T["encolher"], T["encolher"] + 0.2) * (1 - prog(u, T["rigidez"] - 0.3, T["rigidez"]))
    e["barra"] = prog(u, T["rigidez"] + 0.1, T["rigidez"] + 0.45)
    e["bloco"] = e_back(prog(u, T["rigidez"], T["rigidez"] + 0.3))
    e["bloco_vai"] = e_inout(prog(u, T["rigidez"] + 0.15, T["rouba"] - 0.02))
    e["mordida"] = prog(u, T["rouba"], T["rouba"] + 0.55)
    e["cinza_barra"] = prog(u, T["ganho"], T["ganho"] + 0.35)
    e["carga"] = 0.0
    e["pontos"] = -1.0
    e["cam"] = mix_cam(CAM_CAPA, CAM_LADO, e_inout(prog(u, T["milimetro"] + 0.6, T["novo"] + 0.05)))
    return e


def est2(T, t):
    """2º filme (fisioterapia desde o início): tudo de novo, agora com movimento e carga."""
    i0 = T["inicio"]
    e = {"aneis": [e_back(prog(t, i0 + 0.05 * i, i0 + 0.05 * i + 0.4)) for i in range(4)],
         "fios": [prog(t, i0 + 0.2 + 0.04 * i, i0 + 0.4 + 0.04 * i) for i in range(4)],
         "hastes": prog(t, i0 + 0.15, i0 + 0.45)}
    mm = mm_degraus(t, i0 + 0.3)
    e["mm"] = mm
    forte = e_inout(prog(t, T["fortalecem"] + 0.3, T["fortalecem"] + 1.1))
    e["dens"] = lerp(0.62, 1.0, forte) * clamp(mm)
    e["brilho"] = max(0.3 * clamp(mm), 0.6 * forte, clique(t, i0 + 0.3) * clamp(mm))
    e["firme"] = forte
    e["fenda"] = 0.0
    e["dob"] = e_back(prog(t, i0 + 0.05, i0 + 0.5))
    e["arco"] = prog(t, i0 + 0.15, i0 + 0.55)
    e["A"] = A_CHEIO
    amp = lerp(14, 44, e_inout(prog(t, T["movimento"], T["movimento"] + 0.8))) * prog(t, i0 + 0.3, i0 + 0.6)
    e["theta"] = amp * math.sin(2 * math.pi * (t - i0 - 0.3) / 2.0)
    e["cinza"] = 0.0
    e["cadeado"] = 0.0
    e["aceso"] = prog(t, T["solta"], T["solta"] + 0.45)
    e["musc"] = prog(t, i0 + 0.15, i0 + 0.55)
    e["musc_l"] = MUSC_CHEIO
    e["setas"] = 0.0
    e["barra"] = e["bloco"] = e["bloco_vai"] = e["mordida"] = e["cinza_barra"] = 0.0
    e["carga"] = prog(t, T["carga"], T["carga"] + 0.3) * (1 - prog(t, T["treino"] - 0.3, T["treino"]))
    e["pontos"] = t - T["fortalecem"]
    # a câmera só vai para o lado em "movimento": até lá o carimbo FISIOTERAPIA fica sobre a cena parada
    cam = mix_cam(CAM_CAPA, CAM_LADO, e_inout(prog(t, T["movimento"] - 0.05, T["movimento"] + 0.65)))
    e["cam"] = mix_cam(cam, CAM_FIM, e_inout(prog(t, T["manda"] - 0.5, T["manda"] + 0.7)))
    return e


def estado(T, t):
    """-> (estado, rebobinando 0..1). No rebobinar o 1º filme corre para trás até a capa."""
    r0, r1 = janela_volta(T)
    if t < r0:
        return est1(T, t, t), 0.0
    if t < r1:
        return est1(T, lerp(r0, 0.0, e_inout(prog(t, r0, r1))), t), 1.0
    if t < T["inicio"]:
        return est1(T, 0.0, t), 0.0
    return est2(T, t), 0.0


# ------------------------------------------------------------------ mundo: fixador
def anel(cv, y, dx, alfa, metade):
    if alfa <= 0:
        return
    r = skia.Rect(CX + dx - RX2, y - RY2, CX + dx + RX2, y + RY2)
    if metade == "tras":
        cv.drawArc(r, 180, 180, False, paint(ACO_ESC, int(255 * alfa), "stroke", 14))
        return
    cv.drawArc(r, 0, 180, False, paint("#000000", int(80 * alfa), "stroke", 17, blur=6))
    cv.drawArc(r, 0, 180, False, paint(ACO, int(255 * alfa), "stroke", 14))
    cv.drawArc(skia.Rect(r.left() + 6, r.top() + 4, r.right() - 6, r.bottom() - 2), 20, 140, False,
               paint(ACO_HL, int(170 * alfa), "stroke", 3))
    for ang in (25, 90, 155):
        a = math.radians(ang)
        cv.drawCircle(CX + dx + RX2 * math.cos(a), y + RY2 * math.sin(a), 3.2, paint(ACO_ESC, int(255 * alfa)))


def fios(cv, y, pr, alfa):
    if pr <= 0 or alfa <= 0:
        return
    for s in (-1, 1):
        x0, y0, x1, y1 = CX - RX2 + 16, y - 12 * s, CX + RX2 - 16, y + 12 * s
        cv.drawLine(x0, y0, lerp(x0, x1, pr), lerp(y0, y1, pr), paint("#DDE6EE", int(230 * alfa), "stroke", 3.2))
        if pr > 0.98:
            xo = CX - 62 * s
            cv.drawCircle(xo, lerp(y0, y1, (xo - x0) / (x1 - x0)), 6, paint(OURO, int(255 * alfa)))


# ------------------------------------------------------------------ mundo: osso, músculo, dobradiça
def osso(cv, yc_sup, yc_inf, yb):
    sh = sombra_osso()
    for pth in (path_osso_sup(Y_TOPO, yc_sup), path_osso_inf(yc_inf, yb)):
        cv.drawPath(pth, paint("#000000", 70, blur=14))
        cv.drawPath(pth, paint(OSSO_C, shader=sh))
        cv.drawPath(pth, paint(OSSO_L, 150, "stroke", 2.5))
    for y0, y1 in ((Y_TOPO + 250, yc_sup), (yc_inf, yb - 190)):
        if y1 > y0:
            cv.drawRect(skia.Rect(CX - 16, y0, CX + 16, y1), paint(OSSO_B, 60, blur=6))


def musculo(cv, e):
    a = e["musc"]
    if a <= 0:
        return
    w = e["musc_l"]
    y0 = MUSC_Y0; y1 = lerp(MUSC_Y0 + 24, MUSC_Y1, e_out(a))
    rr = skia.RRect.MakeRectXY(skia.Rect(MUSC_X - w / 2, y0, MUSC_X + w / 2, y1), w / 2, w / 2)
    sh = skia.GradientShader.MakeLinear([skia.Point(MUSC_X - w / 2, 0), skia.Point(MUSC_X + w / 2, 0)],
                                        [C(ROSA_B), C(ROSA), C(ROSA), C(ROSA_B)], [0.0, 0.4, 0.6, 1.0])
    cv.drawRRect(rr, paint("#000000", int(55 * a), blur=8))
    cv.drawRRect(rr, paint(ROSA, int(255 * a), shader=sh))
    cv.drawRRect(rr, paint(ROSA_B, int(220 * a), "stroke", 2.5))
    s = e["setas"]
    if s > 0:                                                    # setinhas para dentro: afina
        for f in (0.3, 0.7):
            yy = lerp(y0, y1, f)
            for sg in (-1, 1):
                x = MUSC_X + sg * (w / 2 + 14)
                p = skia.Path(); p.moveTo(x + sg * 13, yy - 18); p.lineTo(x - sg * 4, yy); p.lineTo(x + sg * 13, yy + 18)
                cv.drawPath(p, paint(ROSA, int(255 * s), "stroke", 7))


def cadeado(cv, x, y, esc, alfa):
    if esc <= 0 or alfa <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    cv.drawArc(skia.Rect(-16, -34, 16, 2), 180, 180, False, paint(CINZA_C, int(255 * alfa), "stroke", 7))
    rr = skia.RRect.MakeRectXY(skia.Rect(-25, -10, 25, 30), 7, 7)
    cv.drawRRect(rr, paint("#000000", int(70 * alfa), blur=6))
    cv.drawRRect(rr, paint("#8B95A0", int(255 * alfa)))
    cv.drawRRect(rr, paint("#4A525C", int(255 * alfa), "stroke", 2.5))
    cv.drawCircle(0, 6, 5, paint("#2B3138", int(255 * alfa)))
    cv.drawRect(skia.Rect(-2, 8, 2, 18), paint("#2B3138", int(255 * alfa)))
    cv.restore()


def seta_carga(cv, L, alfa, t):
    """Seta grossa no eixo do bastão, empurrando o topo (desenhada no referencial do bastão)."""
    if alfa <= 0:
        return
    pz = 9 * (0.5 + 0.5 * math.sin(t * 5.2))
    ponta = -L - R_BARRA - 12 + pz; cauda = ponta - 122
    p = skia.Path()
    p.moveTo(-19, cauda); p.lineTo(19, cauda); p.lineTo(19, ponta - 52); p.lineTo(46, ponta - 52)
    p.lineTo(0, ponta); p.lineTo(-46, ponta - 52); p.lineTo(-19, ponta - 52); p.close()
    cv.drawPath(p, paint("#000000", int(80 * alfa), blur=8))
    cv.drawPath(p, paint("#FFFFFF", int(245 * alfa)))
    cv.drawPath(p, paint("#9FB3C6", int(255 * alfa), "stroke", 3))


def dobradica(cv, e, t):
    a = e["dob"]
    if a <= 0:
        return
    px, py = PINO
    A = e["A"]; ar = e["arco"]; acc = e["aceso"]
    rect = skia.Rect(px - R_ARCO, py - R_ARCO, px + R_ARCO, py + R_ARCO)
    if ar > 0:
        perdeu = clamp((A_CHEIO - A) / (A_CHEIO - A_RIGIDO))
        if perdeu > 0:                                           # o arco que se perdeu, apagadinho
            p = paint("#DDE6EE", int(55 * perdeu * ar), "stroke", 4)
            p.setPathEffect(skia.DashPathEffect.Make([12, 14], 0))
            cv.drawArc(rect, -90 - A_CHEIO, 2 * A_CHEIO, False, p)
        meia = A * e_out(ar)
        cor = lerpc("#DDE6EE", CINZA, e["cinza"])
        if acc > 0:                                              # "solta": o arco acende inteiro
            cv.drawArc(rect, -90 - meia, 2 * meia, False, paint(TEAL, int(130 * acc), "stroke", 22, blur=12))
            cv.drawArc(rect, -90 - meia, 2 * meia, False, paint(TEAL, int(255 * acc), "stroke", 8))
        p = paint(cor, int(235 * ar * (1 - acc)), "stroke", 6)
        p.setPathEffect(skia.DashPathEffect.Make([16, 12], -t * 18))
        cv.drawArc(rect, -90 - meia, 2 * meia, False, p)
        for sg in (-1, 1):
            ang = math.radians(-90 + sg * meia)
            cv.drawCircle(px + R_ARCO * math.cos(ang), py + R_ARCO * math.sin(ang), 8,
                          paint(lerpc(cor, TEAL, acc), int(255 * ar)))
    L = L_BARRA * a
    cv.save(); cv.translate(px, py); cv.rotate(e["theta"])
    rr = skia.RRect.MakeRectXY(skia.Rect(-R_BARRA, -L - R_BARRA, R_BARRA, R_BARRA), R_BARRA, R_BARRA)
    sh = skia.GradientShader.MakeLinear([skia.Point(-R_BARRA, 0), skia.Point(R_BARRA, 0)],
                                        [C(OSSO_B), C(OSSO_C), C(OSSO_C), C(OSSO_B)], [0.0, 0.42, 0.58, 1.0])
    cv.drawRRect(rr, paint("#000000", 70, blur=12))
    cv.drawRRect(rr, paint(OSSO_C, shader=sh))
    cv.drawRRect(rr, paint(OSSO_L, 150, "stroke", 2.5))
    seta_carga(cv, L, e["carga"], t)
    cv.restore()
    g = e["cinza"]
    r = R_PINO * clamp(a * 1.4)
    cv.drawCircle(px, py, r + 6, paint("#000000", 60, blur=6))
    sh = skia.GradientShader.MakeRadial(skia.Point(px - 6, py - 6), r * 1.6,
                                        [C(lerpc(ACO_HL, "#8A939D", g)), C(lerpc(ACO, CINZA, g))])
    cv.drawCircle(px, py, r, paint(ACO, shader=sh))
    cv.drawCircle(px, py, r, paint(lerpc(ACO_ESC, "#3E454E", g), 255, "stroke", 3))
    cv.drawCircle(px - 6, py - 6, 4.5, paint("#FFFFFF", int(200 * (1 - g))))
    cadeado(cv, CADEADO[0], CADEADO[1], e["cadeado"], clamp(e["cadeado"] * 2))


RNG = np.random.default_rng(31)
PONTOS = [(RNG.uniform(0, 2 * math.pi), RNG.uniform(120, 210), RNG.uniform(0, 0.35)) for _ in range(22)]


def pontinhos(cv, k, y_meio, meia_alt):
    """'fortalecem': pontinhos dourados vêm de fora e se juntam DENTRO do vão."""
    if k < 0 or k > 1.7:
        return
    some = 1 - prog(k, 1.15, 1.7)
    for ang, r0, atraso in PONTOS:
        f = e_inout(clamp((k - atraso) / 0.85))
        x = lerp(CX + r0 * math.cos(ang), CX + (H2 - 14) * 0.85 * math.cos(ang), f)
        y = lerp(y_meio + r0 * math.sin(ang), y_meio + max(2, meia_alt - 6) * 0.85 * math.sin(ang), f)
        cv.drawCircle(x, y, 11, paint(NOVO_G, int(110 * some), blur=6))
        cv.drawCircle(x, y, 6, paint(OURO, int(255 * some)))


def mundo(cv, e, t):
    gap = e["mm"] * PX_MM
    yc_sup = Y_CORTE; yc_inf = Y_CORTE + FENDA + gap; yb = Y_BASE + FENDA + gap
    y_an = [Y_AN0, Y_AN1, yc_inf + 62, yb - 112]
    dx = [(-900 if i % 2 == 0 else 900) * (1 - e["aneis"][i]) for i in range(4)]
    vis = [clamp(e["aneis"][i] * 3) for i in range(4)]
    for i in range(4):
        anel(cv, y_an[i], dx[i], vis[i], "tras")
    musculo(cv, e)
    osso(cv, yc_sup, yc_inf, yb)
    if gap > 1.5:
        y0, y1 = yc_sup + FENDA * 0.5, yc_inf - FENDA * 0.5
        cv.drawRect(skia.Rect(CX - H2 + 2, y0, CX + H2 - 2, y1), paint(AMBAR))
        if e["firme"] > 0:                                       # brilho firme, parado (não pulsa)
            cv.drawRect(skia.Rect(CX - H2 - 14, y0 - 10, CX + H2 + 14, y1 + 10),
                        paint(NOVO_G, int(90 * e["firme"]), blur=16))
        desenha_regenerado(cv, y0, y1, e["dens"], e["brilho"], 0.0, t)
    if e["fenda"] > 0 and gap < 1.5:                             # a fenda fina acende ("alongamento")
        yf = Y_CORTE + FENDA / 2
        cv.drawLine(CX - H2 - 30, yf, CX + H2 + 30, yf, paint("#FFFFFF", int(150 * e["fenda"]), "stroke", 14, blur=9))
        cv.drawLine(CX - H2 + 2, yf, CX + H2 - 2, yf, paint("#FFF4CF", int(255 * e["fenda"]), "stroke", 3))
    pontinhos(cv, e["pontos"], Y_CORTE + FENDA / 2 + gap / 2, gap / 2)
    for i in range(4):
        fios(cv, y_an[i], e["fios"][i], vis[i])
    a_h = e["hastes"]
    for sx in (-1, 1):
        x = CX + sx * X_HASTE
        haste(cv, x, y_an[0], y_an[1], a_h * vis[1])
        haste(cv, x, y_an[1], y_an[2], a_h * vis[2], rosca=True, fase=e["mm"])
        haste(cv, x, y_an[2], y_an[3], a_h * vis[3])
        porca(cv, x, y_an[1] + 20, e["mm"] * 90 + sx * 15, a_h * vis[1])
        porca(cv, x, y_an[2] - 20, -e["mm"] * 90, a_h * vis[2])
    for i in range(4):
        anel(cv, y_an[i], dx[i], vis[i], "frente")
    dobradica(cv, e, t)


# ------------------------------------------------------------------ peças de tela
def etiqueta(cv, s, x, y, ancora, cor, a, tam=40):
    """Rótulo com canto sup. esq. em (x, y) e fio fino até `ancora` (coordenada de tela)."""
    if a <= 0:
        return
    x += 26 * (1 - e_out(a))
    lw = larg_texto(s, F_BLACK, tam); hh = tam + 22
    if ancora:
        xa, ya = ancora
        cv.drawLine(xa, ya, x, y + hh / 2, paint(cor, int(200 * a), "stroke", 2.5))
        cv.drawCircle(xa, ya, 6, paint(cor, int(255 * a)))
    rr = skia.RRect.MakeRectXY(skia.Rect(x, y, x + lw + 32, y + hh), 14, 14)
    cv.drawRRect(rr, paint(FUNDO_CX, int(215 * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 2.5))
    texto(cv, s, x + 16, y + hh / 2 + tam * 0.36, F_BLACK, tam, cor, int(255 * a), centro=False)


def caixa(cv, s, cx, y, cor, a, tam=40, borda=None):
    """Rótulo centrado em `cx`, topo em `y` (sem fio)."""
    if a <= 0:
        return
    y += 18 * (1 - e_out(a))
    lw = larg_texto(s, F_BLACK, tam); hh = tam + 22
    rr = skia.RRect.MakeRectXY(skia.Rect(cx - lw / 2 - 16, y, cx + lw / 2 + 16, y + hh), 14, 14)
    cv.drawRRect(rr, paint(FUNDO_CX, int(215 * a)))
    cv.drawRRect(rr, paint(borda or cor, int(255 * a), "stroke", 2.5))
    texto(cv, s, cx, y + hh / 2 + tam * 0.36, F_BLACK, tam, cor, int(255 * a))


def carimbo_cor(cv, s, x, y, rot, t0, t, cor, dur=1.9, tam=62, esc0=1.9, fundo_a=170):
    """Carimbo do piloto com cor, tamanho e escala de entrada ajustáveis (o texto longo não cabe em
    62 px, e a entrada a 1,9x faria um rótulo largo sair da tela por alguns quadros)."""
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


def barra_ganho(cv, e):
    a = e["barra"]
    if a <= 0:
        return
    x0, y0, x1, y1 = BARRA
    texto(cv, "GANHO", x0, y0 - 16, F_BLACK, 40, TEAL, int(255 * a), centro=False, contorno=6)
    xf = lerp(x0 + 30, x1, e_out(a))
    mord = e["mordida"]; cz = e["cinza_barra"]
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0 - 6, y0 - 6, x1 + 6, y1 + 6), 14, 14),
                 paint("#FFFFFF", int(28 * a)))                    # trilho (sem régua, sem número)
    mordido = mord >= 0.25
    xc = x1 - PEDACO
    fim_teal = min(xf, xc - 5) if mordido else xf
    cv.save()
    cv.clipRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 10, 10), True)
    sh = skia.GradientShader.MakeLinear([skia.Point(0, y0), skia.Point(0, y1)], [C("#7FE6DB"), C(TEAL), C("#2E9E95")],
                                        [0.0, 0.45, 1.0])
    cv.drawRect(skia.Rect(x0, y0, fim_teal, y1), paint(TEAL, int(255 * a), shader=sh))
    if mordido:
        cor = lerpc("#5E8F8B", CINZA, cz)
        dente = skia.Path(); n = 4; hh = (y1 - y0) / n
        dente.moveTo(xc + 5, y0)
        for k in range(n):
            dente.lineTo(xc + 15, y0 + hh * (k + 0.5)); dente.lineTo(xc + 5, y0 + hh * (k + 1))
        dente.lineTo(x1, y1); dente.lineTo(x1, y0); dente.close()
        cv.drawPath(dente, paint(cor, int(255 * a)))
        # borda mordida do lado verde-água
        dt = skia.Path(); dt.moveTo(xc - 5, y0)
        for k in range(n):
            dt.lineTo(xc + 5, y0 + hh * (k + 0.5)); dt.lineTo(xc - 5, y0 + hh * (k + 1))
        cv.drawPath(dt, paint("#0B1824", int(220 * a), "stroke", 3))
    cv.restore()


def bloco_rigidez(cv, e, cam):
    b = e["bloco"]
    if b <= 0:
        return
    sx, sy = na_tela(cam, CADEADO[0], CADEADO[1])
    v = e["bloco_vai"]
    x = lerp(sx, BLOCO[0], v); y = lerp(sy, BLOCO[1], v) - 70 * math.sin(math.pi * v)
    m = e["mordida"]
    if 0 < m < 1:
        y += ((BARRA[1] + BARRA[3]) / 2 - BLOCO[1]) * abs(math.sin(2 * math.pi * m))
    esc = lerp(0.25, 1.0, min(1.0, b))
    a = clamp(b * 2)
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-100, -33, 100, 33), 12, 12)
    cv.drawRRect(rr, paint("#000000", int(90 * a), blur=10))
    cv.drawRRect(rr, paint("#59626D", int(255 * a)))
    cv.drawRRect(rr, paint(CINZA_C, int(255 * a), "stroke", 3))
    texto(cv, "RIGIDEZ", 0, 13, F_BLACK, 36, "#FFFFFF", int(255 * a))
    cv.restore()


def rebobinar(cv, t, r0, r1):
    a = prog(t, r0 - 0.08, r0 + 0.08) * (1 - prog(t, r1 - 0.16, r1))   # some ANTES de o carimbo bater
    if a <= 0:
        return
    for k in range(7):                                           # riscos de fita correndo
        y = (k * 283 + (t - r0) * 2600) % H
        cv.drawRect(skia.Rect(0, y, W, y + 5 + 3 * (k % 3)), paint("#CFE8FF", int(34 * a)))
    cv.drawRect(skia.Rect(0, 0, W, H), paint("#0B2A44", int(60 * a)))
    cx, cy = 540, 640
    pulso = 1 + 0.06 * math.sin((t - r0) * 22)
    cv.save(); cv.translate(cx, cy); cv.scale(pulso, pulso)
    cv.drawCircle(0, 0, 104, paint(FUNDO_CX, int(215 * a)))
    cv.drawCircle(0, 0, 104, paint("#FFFFFF", int(230 * a), "stroke", 5))
    for dx in (-44, 16):                                         # dois triângulos para a esquerda
        p = skia.Path(); p.moveTo(dx, 0); p.lineTo(dx + 56, -42); p.lineTo(dx + 56, 42); p.close()
        cv.drawPath(p, paint("#FFFFFF", int(255 * a)))
    cv.restore()


def mostrador(cv, t, t0, a):
    """'na dose certa': mostrador semicircular, SEM número; o ponteiro oscila e para no meio."""
    if a <= 0:
        return
    cx, cy, r = MOSTRADOR
    rect = skia.Rect(cx - r, cy - r, cx + r, cy + r)
    cv.drawArc(skia.Rect(cx - r - 26, cy - r - 26, cx + r + 26, cy + r + 26), 180, 180, True,
               paint(FUNDO_CX, int(200 * a)))
    for ini, cor in ((180, "#5E7186"), (240, TEAL), (300, VERMELHO)):
        p = paint(cor, int(255 * a), "stroke", 26); p.setStrokeCap(skia.Paint.kButt_Cap)
        cv.drawArc(rect, ini + 1.5, 57, False, p)
    k = max(0.0, t - t0)
    ang = 270 - 80 * math.exp(-2.4 * k) * math.cos(7.5 * k)
    no_meio = prog(k, 1.1, 1.4)
    if no_meio > 0:
        p = paint(TEAL, int(150 * a * no_meio), "stroke", 40, blur=12); p.setStrokeCap(skia.Paint.kButt_Cap)
        cv.drawArc(rect, 241.5, 57, False, p)
    rad = math.radians(ang)
    xp, yp = cx + (r - 8) * math.cos(rad), cy + (r - 8) * math.sin(rad)
    cv.drawLine(cx, cy, xp, yp, paint("#000000", int(90 * a), "stroke", 12, blur=4))
    cv.drawLine(cx, cy, xp, yp, paint("#FFFFFF", int(255 * a), "stroke", 8))
    cv.drawCircle(cx, cy, 15, paint("#FFFFFF", int(255 * a)))
    cv.drawCircle(cx, cy, 15, paint(ACO_ESC, int(255 * a), "stroke", 3))


def halter(cv, x, y, a):
    if a <= 0:
        return
    cv.save(); cv.translate(x, y)
    cv.drawRect(skia.Rect(-120, 52, 120, 64), paint("#000000", int(70 * a), blur=10))   # sombra no "chão"
    sh = skia.GradientShader.MakeLinear([skia.Point(0, -10), skia.Point(0, 10)], [C(FERRO_HL), C("#C9D3DD"), C(FERRO_HL)])
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-110, -9, 110, 9), 6, 6), paint(FERRO_HL, int(255 * a), shader=sh))
    for sg in (-1, 1):
        for x0, w, h in ((52, 34, 112), (88, 26, 82)):
            xa = sg * x0 - w / 2
            rr = skia.RRect.MakeRectXY(skia.Rect(xa, -h / 2, xa + w, h / 2), 8, 8)
            sh2 = skia.GradientShader.MakeLinear([skia.Point(xa, 0), skia.Point(xa + w, 0)],
                                                 [C(FERRO), C(FERRO_HL), C(FERRO)], [0.0, 0.45, 1.0])
            cv.drawRRect(rr, paint(FERRO, int(255 * a), shader=sh2))
            cv.drawRRect(rr, paint("#1C2128", int(255 * a), "stroke", 2.5))
    cv.restore()


def risco_x(cv, x, y, k, a):
    if k <= 0 or a <= 0:
        return
    for i, (x0, y0, x1, y1) in enumerate(((-150, -80, 150, 80), (150, -80, -150, 80))):
        f = e_out(clamp((k - 0.12 * i) / 0.16))
        if f <= 0:
            continue
        xe, ye = lerp(x0, x1, f), lerp(y0, y1, f)
        cv.drawLine(x + x0, y + y0, x + xe, y + ye, paint("#000000", int(110 * a), "stroke", 22, blur=4))
        cv.drawLine(x + x0, y + y0, x + xe, y + ye, paint(VERMELHO, int(255 * a), "stroke", 15))


def fileira(cv, t, t0, a):
    """'um pouco todo dia': 7 quadradinhos, um tique dourado por vez (sem dia, sem número)."""
    if a <= 0:
        return
    lado, esp = 50, 14
    x0 = HALTER[0] - (7 * lado + 6 * esp) / 2
    for i in range(7):
        x = x0 + i * (lado + esp)
        ent = e_back(prog(t, t0 + 0.03 * i, t0 + 0.03 * i + 0.3))
        if ent <= 0:
            continue
        cv.save(); cv.translate(x + lado / 2, FILEIRA_Y + lado / 2); cv.scale(ent, ent)
        rr = skia.RRect.MakeRectXY(skia.Rect(-lado / 2, -lado / 2, lado / 2, lado / 2), 10, 10)
        cv.drawRRect(rr, paint(FUNDO_CX, int(225 * a)))
        cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 3.5))
        tk = t - (t0 + 0.12 + 0.2 * i)
        if tk >= 0:
            pr = e_out(clamp(tk / 0.18))
            if pr < 1:
                cv.drawCircle(0, 0, 34 * pr, paint(NOVO_G, int(120 * a * (1 - pr)), blur=8))
            p = skia.Path(); p.moveTo(-14, 0)
            p.lineTo(-14 + 10 * min(1, pr * 2), 10 * min(1, pr * 2))
            if pr > 0.5:
                q = (pr - 0.5) * 2
                p.lineTo(-4 + 20 * q, 10 - 26 * q)
            cv.drawPath(p, paint(OURO, int(255 * a), "stroke", 6.5))
        cv.restore()


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    e, _ = estado(T, t)
    r0, r1 = janela_volta(T)
    px, s, ys = e["cam"]
    tremor = 0.0
    for t0, f in ((T["fixador"] + 0.5, 4), (T["parados"], 6), (r1 + 0.02, 6), (T["treino"] + 0.28, 9),
                  (T["equipe"], 4)):
        k = t - t0
        if 0 <= k < 0.35:
            tremor += f * math.sin(k * 70) * (1 - k / 0.35)
    cam = (px + tremor, s, ys)

    # ================= mundo (câmera)
    cv.save(); cv.translate(cam[0], ys); cv.scale(s, s); cv.translate(-CX, -YW)
    mundo(cv, e, t)
    cv.restore()

    gap = e["mm"] * PX_MM                                         # (rótulos do 1º filme saem antes de rebobinar)
    brilhos(cv, *na_tela(cam, CX, Y_CORTE + gap / 2), t, T["novo"] + 0.05, n=14, raio=150)
    brilhos(cv, *na_tela(cam, CX, Y_CORTE + gap / 2), t, T["fortalecem"] + 0.95, n=16, raio=170)

    # ---- 1º filme: rótulos
    a = prog(t, T["fixador"] + 0.35, T["fixador"] + 0.65) * (1 - prog(t, T["milimetro"] - 0.3, T["milimetro"]))
    etiqueta(cv, "FIXADOR", 742, 470, na_tela(cam, CX + RX2, Y_AN0), ACO_HL, a)
    a = prog(t, T["milimetro"] + 0.5, T["milimetro"] + 0.8) * (1 - prog(t, T["art"] + 0.2, T["art"] + 0.5))
    caixa(cv, "CERCA DE UM MILÍMETRO POR DIA", CX, 236, "#FFFFFF", a, borda=OURO)
    ancora_vao = na_tela(cam, CX + H2 - 4, Y_CORTE + FENDA / 2 + gap / 2)
    a = prog(t, T["novo"] + 0.05, T["novo"] + 0.35) * (1 - prog(t, T["parados"] - 0.3, T["parados"]))
    etiqueta(cv, "OSSO NOVO", 500, 905, ancora_vao, OURO, a)
    ancora_pino = na_tela(cam, PINO[0] + R_PINO, PINO[1])
    # fica até a 2ª "articulação" ("Parada, a articulação pode enrijecer") e troca no lugar por PODE ENRIJECER
    a = prog(t, T["art"] + 0.2, T["art"] + 0.5) * (1 - prog(t, T["enrijecer"] + 0.15, T["enrijecer"] + 0.4))
    etiqueta(cv, "ARTICULAÇÃO", 500, 452, ancora_pino, "#FFFFFF", a)
    carimbo_cor(cv, "NÃO GOSTAM DE FICAR PARADOS", 540, 712, -5, T["parados"], t, VERMELHO, dur=1.85, tam=46,
                esc0=1.15)
    a = prog(t, T["enrijecer"] + 0.4, T["enrijecer"] + 0.7) * (1 - prog(t, T["encolher"] - 0.2, T["encolher"] + 0.1))
    etiqueta(cv, "PODE ENRIJECER", 500, 452, na_tela(cam, CADEADO[0] + 26, CADEADO[1] + 10), CINZA_C, a)
    fim_musc = 1 - prog(t, T["rigidez"] - 0.2, T["rigidez"] + 0.1)
    a = prog(t, T["musculo"] + 0.15, T["musculo"] + 0.45) * fim_musc
    etiqueta(cv, "MÚSCULO", 500, 742, na_tela(cam, MUSC_X + e["musc_l"] / 2, 600), ROSA, a)
    a = prog(t, T["encolher"] + 0.1, T["encolher"] + 0.4) * fim_musc
    etiqueta(cv, "ENCOLHER", 500, 822, na_tela(cam, MUSC_X + e["musc_l"] / 2, 668), ROSA, a)
    barra_ganho(cv, e)
    bloco_rigidez(cv, e, cam)                                     # a mordida conta o "rouba": sem rótulo

    # ---- o filme volta ao começo; SÓ DEPOIS o carimbo (a tese da peça: fica até "movimento")
    rebobinar(cv, t, r0, r1)
    carimbo_ouro(cv, "FISIOTERAPIA", CX, 590, -6, r1 + 0.02, t, dur=T["movimento"] + 0.3 - r1)
    a = prog(t, T["desde"] + 0.05, T["desde"] + 0.3) * (1 - prog(t, T["movimento"] + 0.05, T["movimento"] + 0.3))
    caixa(cv, "DESDE O INÍCIO", CX, 646, OURO, a)

    # ---- 2º filme
    a = prog(t, T["movimento"] + 0.35, T["movimento"] + 0.65) * (1 - prog(t, T["dose"] + 0.6, T["dose"] + 0.9))
    etiqueta(cv, "MOVIMENTO", 500, 452, ancora_pino, TEAL, a)
    if e["carga"] > 0:
        ang = math.radians(e["theta"]); rr = L_BARRA + R_BARRA + 70
        ancora_seta = na_tela(cam, PINO[0] + rr * math.sin(ang) + 18 * math.cos(ang),
                              PINO[1] - rr * math.cos(ang) + 18 * math.sin(ang))
        a = prog(t, T["carga"] + 0.1, T["carga"] + 0.4) * (1 - prog(t, T["dose"] + 0.9, T["dose"] + 1.2))
        etiqueta(cv, "CARGA", 560, 236, ancora_seta, "#FFFFFF", a)
    a_m = prog(t, T["dose"] - 0.05, T["dose"] + 0.25) * (1 - prog(t, T["treino"] - 0.3, T["treino"]))
    if a_m > 0:
        cv.save(); cv.translate(0, 20 * (1 - e_out(a_m))); mostrador(cv, t, T["dose"], a_m); cv.restore()
    a = prog(t, T["dose"] + 0.2, T["dose"] + 0.5) * (1 - prog(t, T["solta"] - 0.1, T["solta"] + 0.2))
    caixa(cv, "NA DOSE CERTA", MOSTRADOR[0], MOSTRADOR[1] + 36, TEAL, a)
    ancora_arco = na_tela(cam, PINO[0] + R_ARCO * math.sin(math.radians(A_CHEIO)),
                          PINO[1] - R_ARCO * math.cos(math.radians(A_CHEIO)))
    a = prog(t, T["solta"] + 0.1, T["solta"] + 0.4) * (1 - prog(t, T["treino"] - 0.4, T["treino"] - 0.1))
    etiqueta(cv, "SOLTA", 520, 330, ancora_arco, TEAL, a)
    a = prog(t, T["fortalecem"] + 0.1, T["fortalecem"] + 0.4) * (1 - prog(t, T["pouco"] - 0.4, T["pouco"] - 0.1))
    etiqueta(cv, "FORTALECEM O OSSO", 500, 905, ancora_vao, OURO, a)

    # ---- treino pesado não; um pouco todo dia
    fim_col = 1 - prog(t, T["manda"] - 0.5, T["manda"] - 0.15)
    if t >= T["treino"]:
        k = t - T["treino"]
        y = lerp(-160, HALTER[1], clamp(k / 0.28) ** 2)
        if k > 0.28:
            y -= 22 * math.sin(math.pi * clamp((k - 0.28) / 0.2))
        a_h = (1 - 0.55 * prog(t, T["pouco"] - 0.1, T["pouco"] + 0.3)) * fim_col
        if a_h > 0:
            cv.saveLayerAlpha(None, int(255 * a_h))                   # apaga o grupo inteiro por igual
            halter(cv, HALTER[0], y, 1.0)
            if 0.28 <= k < 0.7:                                   # o baque
                q = (k - 0.28) / 0.42
                for sg in (-1, 1):
                    for j in range(3):
                        x0 = HALTER[0] + sg * (130 + 26 * q); yy = HALTER[1] + 40 - j * 22
                        cv.drawLine(x0, yy, x0 + sg * 26, yy - 6, paint("#FFFFFF", int(200 * (1 - q)), "stroke", 4))
            risco_x(cv, HALTER[0], HALTER[1], t - T["pesado"], 1.0)
            caixa(cv, "TREINO PESADO", HALTER[0], HALTER[1] + 84, VERMELHO, prog(t, T["treino"] + 0.25, T["treino"] + 0.5))
            cv.restore()
    a = prog(t, T["pouco"] - 0.05, T["pouco"] + 0.25) * fim_col
    if a > 0:
        texto(cv, "UM POUCO TODO DIA", HALTER[0], FILEIRA_Y - 22, F_BLACK, 40, OURO, int(255 * a), contorno=8)
        fileira(cv, t, T["pouco"], a)
    carimbo_cor(cv, "GUIADO PELA EQUIPE", HALTER[0] - 20, FILEIRA_Y + 150, -4, T["equipe"], t, OURO,
                dur=T["manda"] - T["equipe"], tam=38, esc0=1.3, fundo_a=160)

    capa(cv, t, T["milimetro"], ep["gancho"][0], ep["gancho"][1])
    selo_como_funciona(cv, prog(t, T["milimetro"] + 0.5, T["milimetro"] + 0.9) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface(cv, t, T, blocos, DESTAQUE)


# ------------------------------------------------------------------ som e prévias
def sons(T):
    r0, r1 = janela_volta(T)
    fx, i0 = T["fixador"], T["inicio"]
    ev = [(fx - 0.05, "whoosh", 0.6)]
    ev += [(fx + 0.07 * i + 0.4, "ping", 0.55) for i in range(4)]
    k = 0
    while T["milimetro"] + k * PER < r0 - 0.05:                   # o relógio do alongamento (1º filme)
        ev.append((T["milimetro"] + k * PER, "click", 0.55 if k < 4 else 0.38)); k += 1
    ev += [(T["novo"] - 0.05, "shimmer", 0.8), (T["art"] + 0.05, "pop", 0.65), (T["parados"], "thump", 0.85),
           (T["enrijecer"] + 0.1, "crackle", 0.45), (T["enrijecer"] + 0.35, "tick", 0.9),
           (T["musculo"], "whoosh", 0.25), (T["encolher"] + 0.05, "pop", 0.35),
           (T["rigidez"], "thump", 0.5), (T["rouba"] + 0.12, "crackle", 0.5), (T["rouba"] + 0.4, "crackle", 0.4),
           (T["ganho"] + 0.05, "pop", 0.3),
           (r0, "whoosh", 0.7)]
    ev += [(lerp(r0 + 0.05, r1 - 0.1, j / 9), "tick", 0.4) for j in range(10)]   # cliques em marcha a ré
    ev += [(r1 + 0.02, "thump", 0.9), (r1 + 0.1, "ding", 0.5),
           (i0, "whoosh", 0.45)]
    ev += [(i0 + 0.05 * i + 0.3, "ping", 0.45) for i in range(4)]
    k = 0
    while i0 + 0.3 + k * PER < T["total"] - 0.3:                  # o relógio recomeça (2º filme)
        tt = i0 + 0.3 + k * PER
        ev.append((tt, "click", 0.28 if tt > T["manda"] - 0.2 else 0.38)); k += 1
    ev += [(T["movimento"], "whoosh", 0.3), (T["carga"] + 0.05, "thump", 0.5),
           (T["dose"], "whoosh", 0.25), (T["dose"] + 1.25, "ding", 0.45),
           (T["solta"], "shimmer", 0.6), (T["fortalecem"], "shimmer", 0.85), (T["fortalecem"] + 0.95, "crackle", 0.4),
           (T["treino"] + 0.28, "thump", 1.0), (T["pesado"] + 0.02, "tick", 0.9)]
    ev += [(T["pouco"] + 0.12 + 0.2 * i, "pop", 0.5) for i in range(7)]
    ev += [(T["equipe"], "thump", 0.8), (T["equipe"] + 0.1, "ding", 0.5), (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def tempos_previa(T):
    r0, r1 = janela_volta(T)
    return [0.4, T["fixador"] + 0.9, T["novo"] + 0.4, T["parados"] + 0.5, T["encolher"] + 0.7,
            T["ganho"] + 0.6, (r0 + r1) / 2, T["inicio"] + 0.3, T["carga"] + 1.0, T["fortalecem"] + 0.9,
            T["equipe"] + 0.8, T["manda"] + 1.6]


render = fazer_render(quadro, ANCORAS, sons, tempos_previa, respiro_cta=1.8)
