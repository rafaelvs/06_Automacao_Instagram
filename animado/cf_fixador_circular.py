# -*- coding: utf-8 -*-
"""COMO FUNCIONA — fixador circular de Ilizarov ("QUE GAIOLA É ESSA / NA PERNA?").

Mesmo estilo e mesmas peças do piloto aprovado (cf_alongamento): fundo azul-petróleo com partículas,
tíbia marfim dentro do contorno suave da perna, anéis/hastes/porcas douradas do fixador, osso novo
dourado, rótulos com linha e ponto, carimbos, brilhos, legenda karaokê e CTA com aviãozinho.
O que o verificador exigiu (lote3_cf/cf_fixador_circular_storyboard.json) está aqui:
  * NENHUM fio cruzando o anel e NENHUMA oliva (a função fios() do piloto fica fora desta cena): no
    lugar deles, PINOS curtos que vão do anel até o osso.
  * Os pinos crescem como traço (o recurso de progressão dos fios do piloto), um de cada vez com um
    tique leve; ao cruzar a linha da pele só acende um ponto em tom de pele — sem perfuração
    realista, sem pele afundando, sem sangue.
  * "Endireita": só as duas partes do osso, separadas pelo CORTE ÓSSEO PLANEJADO, se alinhando aos
    poucos; o fixador fica esmaecido ao fundo, sem anel inclinando e sem dobradiça.
  * Nenhum número na tela (nem milímetro, nem dia, nem contador, nem item numerado); nenhum exame
    simulado.
  * A lista das 3 CAPACIDADES (endireita / alonga / puxa) fica na tela até a palavra "ritmo"; é lista
    de marcadores que acendem na palavra, sem ordinal e sem ✓ (não são "as 3 etapas" de todo
    tratamento: o transporte só existe quando há falha).
  * Troca de pose do osso (inteiro <-> vinhetas) é CORTE SECO na metade da transição: nunca há duas
    poses sobrepostas nem osso translúcido.
Cena PRESA ao roteiro pelas palavras-âncora (ANCORAS): roteiro sem elas = KeyError, não vídeo torto.

Desvio do contrato (anotado): a voz do edge-tts devolve a última palavra da 7ª frase como "papel."
(com o ponto) e o `alinhar` comum recusa o vídeo ("palavra da voz 'papel.' não achada no roteiro").
Como cf_comum não pode ser mexido (entra no hash dos vídeos aprovados), esta cena monta o próprio
`render` com os MESMOS passos de `cf_comum.fazer_render` (cópia de cf_comum.fazer_render de 19/10),
só tirando a pontuação colada na palavra da voz antes de alinhar. Pendência para quem cuida do
cf_comum: aplicar a mesma limpeza (`_PONTA.sub('', p['w'])`) no fazer_render/alinhar comum na
próxima versão que puder invalidar hashes e então voltar esta cena para `render = fazer_render(...)`.
"""
import math
import os
import re

import skia

from . import som, voz as _voz
from .base import codificar, previas as _previas
from .cf_alongamento import (ACO, ACO_ESC, ACO_HL, CX, F_BLACK, F_SEMI, HASTE, NOVO_G, OSSO_B, OSSO_C, OSSO_L,
                             OURO, PELE, RX, RY, VERMELHO, H, W, Y_BASE, Y_TOPO, C, anel, brilhos, clamp,
                             desenha_regenerado, e_back, e_in_back, e_inout, e_out, fundo, haste, larg_texto, lerp,
                             lerpc, paint, path_osso_inf, path_osso_sup, porca, prog, sombra_osso, texto)
from .cf_comum import (alinhar, ancoras, capa, carimbo as carimbo_ouro, comprimir, interface, montar_blocos,
                       selo_como_funciona)

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "gaiola": ("gaiola", 1, False), "fixador": ("fixador", 1, False), "ilizarov": ("ilizarov", 1, False),
    "pinos": ("pinos", 1, False), "ate": ("até", 1, False), "aneis": ("anéis", 1, False),
    "segura": ("segura", 1, False), "pele": ("pele", 1, False), "ajusta": ("ajusta", 1, False),
    "aos": ("aos", 1, False), "reabrir": ("reabrir", 1, False), "endireita": ("endireita", 1, False),
    "alonga": ("alonga", 1, False), "puxa": ("puxa", 1, False), "falha": ("falha", 1, False),
    "ritmo": ("ritmo", 1, False), "apertar": ("apertar", 1, False), "aparelho": ("aparelho", 1, False),
    "sair": ("sair", 1, False), "papel": ("papel", 1, False), "manda": ("manda", 1, False),
}
DESTAQUE = {"gaiola", "fixador", "circular", "ilizarov", "pinos", "anéis", "segura", "pele", "pouquinhos",
            "reabrir", "endireita", "alonga", "puxa", "falha", "ritmo", "equipe", "apertar", "sair", "papel"}

# ------------------------------------------------------------------ textos de tela (todos em ep["tela"])
T_FIX, T_ILI = "FIXADOR CIRCULAR", "DE ILIZAROV"
T_PINOS, T_ATE, T_ANEIS = "PINOS", "ATÉ O OSSO", "ANÉIS"
T_SEGURA, T_PELE = "SEGURA O OSSO", "POR FORA DA PELE"
T_POUCO, T_REABRIR = "AOS POUQUINHOS", "SEM REABRIR A CADA ETAPA"
T_CORTE = ("CORTE ÓSSEO", "PLANEJADO")
ITENS = (("ENDIREITA", None, "endireita"), ("ALONGA", "ALONGAMENTO ÓSSEO", "alonga"),
         ("PUXA UM PEDAÇO DE OSSO", "TRANSPORTE ÓSSEO", "puxa"))
T_FALHA, T_RITMO = "FALHA", "O RITMO É DA EQUIPE"
T_NADA, T_CONTA = "NADA DE APERTAR PEÇA", "POR CONTA PRÓPRIA"
T_SAIR, T_PAPEL = "COSTUMA SAIR", "QUANDO O OSSO CUMPRE SEU PAPEL"
AZUL = "#9CC9FF"

# ------------------------------------------------------------------ geometria (mundo)
FOCO = 740                                   # centro vertical do osso no mundo (platô 300 ... maléolo 1186)
Y_AN = (385, 610, 845, 1040)                 # os 4 anéis (mesmo anel do piloto: RX x RY)
X_HASTE = 204                                # hastes nas laterais do anel, como no piloto
H2 = HASTE / 2
Y_C = 640                                    # o corte ósseo planejado das vinhetas (diáfise)
THETA = 9.0                                  # leve ângulo da vinheta "endireita" (graus, esquemático)
GAP_A = 60                                   # quanto as partes se afastam na vinheta "alonga" (esquemático)
SEG = 110                                    # o pedaço que viaja na vinheta "puxa"
Y_G1 = 950                                   # fim da falha (início do osso de baixo)
CURSO = 0.78 * (Y_G1 - (Y_C + SEG))          # quanto o pedaço anda: vai ocupando a falha, sem fechar em cena
AJ_PASSO = 4.0                               # o "tiquinho" que o anel desce a cada clique do close
CLIQUES_AJ = (0.15, 0.5, 0.85, 1.2)          # cliques do close, a partir de "ajusta" (NÃO vão para a tela)
GIRO = 30                                    # graus por clique: o hexágono alterna ponta/lado (dá para ver)
ORDEM_PINO = (2, 1, 3, 0, 4, 5, 6, 7)        # posição na fila de cada pino: o rotulado (PINOS[3]) cresce 1º


def _perna_path(yb=Y_BASE):
    """Contorno da perna do piloto (joelho, panturrilha, tornozelo) — mesmo desenho."""
    L = yb - (Y_TOPO - 50)

    def y(f):
        return Y_TOPO - 50 + L * f
    p = skia.Path()
    p.moveTo(CX - 150, y(0.0))
    p.cubicTo(CX - 168, y(0.10), CX - 200, y(0.22), CX - 196, y(0.36))
    p.cubicTo(CX - 192, y(0.52), CX - 140, y(0.66), CX - 112, y(0.80))
    p.cubicTo(CX - 100, y(0.88), CX - 112, y(0.96), CX - 100, y(1.04))
    p.lineTo(CX + 108, y(1.04))
    p.cubicTo(CX + 112, y(0.95), CX + 104, y(0.88), CX + 112, y(0.80))
    p.cubicTo(CX + 132, y(0.64), CX + 176, y(0.50), CX + 172, y(0.34))
    p.cubicTo(CX + 168, y(0.20), CX + 152, y(0.08), CX + 140, y(0.0))
    p.close()
    return p


PERNA = _perna_path()
OSSO_INTEIRO = skia.Op(path_osso_sup(Y_TOPO, Y_C + 6), path_osso_inf(Y_C - 6, Y_BASE), skia.PathOp.kUnion_PathOp)


def _borda(path, y, lado, limite=320):
    """x da borda de `path` na altura y, do lado (-1 esq., +1 dir.), varrendo a partir do eixo."""
    ult = 0
    for d in range(0, limite):
        if path.contains(CX + lado * d, y):
            ult = d
    return CX + lado * ult


def _pinos():
    """8 pinos curtos (2 por anel): do anel (frente, lateral) até a superfície do osso.
    -> [(anel, (x0, y0) no anel, (x1, y1) no osso, u em que cruza a pele)]."""
    out = []
    angs = ((150, 30), (154, 26), (148, 32), (156, 24))
    for r, y in enumerate(Y_AN):
        for k, lado in enumerate((-1, 1)):
            a = math.radians(angs[r][k])
            x0, y0 = CX + RX * math.cos(a) - lado * 6, y + RY * math.sin(a) - 2
            y1 = y + 8 + (3 if lado > 0 else -3)
            x1 = _borda(OSSO_INTEIRO, y1, lado) - lado * 2
            u = 1.0
            for j in range(1, 200):
                uu = j / 200
                if PERNA.contains(lerp(x0, x1, uu), lerp(y0, y1, uu)):
                    u = uu; break
            out.append((r, (x0, y0), (x1, y1), u))
    return out


PINOS = _pinos()
_PONTA_PINO = {}


def ponta_pino(i, dy):
    """Ponta do pino i no osso quando o anel dele desceu dy: o pino inteiro translada junto com o anel
    (fica paralelo, não 'entorta') e a ponta só desliza pela superfície do osso."""
    k = (i, int(round(dy)))
    if k not in _PONTA_PINO:
        r, _, (_, y1), _ = PINOS[i]
        lado = -1 if i % 2 == 0 else 1
        yy = y1 + k[1]
        _PONTA_PINO[k] = (_borda(OSSO_INTEIRO, yy, lado) - lado * 2, yy)
    return _PONTA_PINO[k]


# ------------------------------------------------------------------ tempo
def passos(x, n, suave=0.5):
    """0..1 em n passinhos (anda e para), sem número na tela."""
    k = clamp(x) * n; i = math.floor(k)
    if i >= n:
        return 1.0
    return (i + e_inout(clamp((k - i) / suave))) / n


def vinheta(t, T):
    """0 = cena da perna com o fixador; 1 = vinhetas (endireita/alonga/puxa) com o fixador esmaecido."""
    return e_inout(prog(t, T["endireita"] - 0.24, T["endireita"] - 0.06)) * (1 - e_inout(prog(t, T["ritmo"] - 0.1, T["ritmo"] + 0.1)))


def theta(t, T):
    return THETA * (1 - passos(prog(t, T["endireita"] + 0.05, T["alonga"] + 0.12), 4))


def janela_alonga(T):
    return T["alonga"] + 0.05, T["puxa"] + 0.3


def gap_alonga(t, T):
    t0, t1 = janela_alonga(T)
    return GAP_A * passos(prog(t, t0, t1), 4)


def troca_v3(T):
    """Instante do corte seco vinheta 2 -> vinheta 3 (na palavra "pedaço")."""
    return T["puxa"] + 0.35


def janela_transporte(T):
    return T["puxa"] + 0.55, T["ritmo"] - 0.1


def desloc(t, T):
    t0, t1 = janela_transporte(T)
    return CURSO * passos(prog(t, t0, t1), 10, 0.55)


def ajuste(t, T):
    return sum(e_out(prog(t, T["ajusta"] + c, T["ajusta"] + c + 0.14)) for c in CLIQUES_AJ)


def metronomo(T):
    out, k = [], 0
    while True:
        tc = T["ritmo"] + 0.38 + 0.42 * k
        if tc > T["apertar"] - 0.22:
            return out
        out.append(tc); k += 1


# ------------------------------------------------------------------ câmera
K0 = (CX, FOCO, 540, 800, 0.90)              # capa: perna inteira, centrada, abaixo do gancho
K1 = (CX, FOCO, 380, 800, 0.88)              # libera a coluna da direita para os rótulos
KC = (CX + X_HASTE, 745, 480, 700, 2.0)      # close numa haste entre dois anéis (o ajuste)
K3 = (CX, FOCO, 540, 800, 0.88)              # volta ao conjunto, centrado (carimbo)
K4 = (CX, 765, 540, 875, 0.735)              # vinhetas: osso inteiro (com o vão de GAP_A) entre lista e legenda
K5 = (CX, FOCO, 540, 830, 0.85)              # fim: perna inteira, topo livre para os cartões


def camera(t, T):
    cur = K0
    for t0, t1, k in ((T["fixador"] - 0.1, T["fixador"] + 0.7, K1), (T["ajusta"] - 0.3, T["ajusta"] + 0.3, KC),
                      (T["reabrir"] - 0.15, T["reabrir"] + 0.45, K3), (T["endireita"] - 0.4, T["endireita"] - 0.02, K4),
                      (T["ritmo"] - 0.1, T["ritmo"] + 0.5, K5)):
        a = e_inout(prog(t, t0, t1))
        if a > 0:
            cur = tuple(lerp(c, d, a) for c, d in zip(cur, k))
    tremor = 0.0
    for t0, forca in ((T["segura"] + 0.05, 11), (T["reabrir"] + 0.15, 5), (T["apertar"], 6)):
        k = t - t0
        if 0 <= k < 0.4:
            tremor += forca * math.sin(k * 70) * (1 - k / 0.4)
    fx, fy, sx, sy, s = cur
    return fx, fy, sx + tremor, sy, s


def na_tela(cam, x, y):
    fx, fy, sx, sy, s = cam
    return sx + (x - fx) * s, sy + (y - fy) * s


# ------------------------------------------------------------------ desenho: perna e osso
def desenha_perna(cv, alfa, borda=0.0):
    if alfa <= 0:
        return
    y0, y1 = Y_TOPO - 50, Y_TOPO - 50 + (Y_BASE - (Y_TOPO - 50)) * 1.04
    sh = skia.GradientShader.MakeLinear([skia.Point(CX - 200, 0), skia.Point(CX + 180, 0)],
                                        [C(PELE, int(85 * alfa)), C(PELE, int(25 * alfa)), C(PELE, int(70 * alfa))],
                                        [0.0, 0.5, 1.0])
    cv.saveLayer(skia.Rect(0, y0 - 40, W, y1 + 40), None)
    cv.drawPath(PERNA, paint(PELE, 255, shader=sh))
    cv.drawPath(PERNA, paint(PELE, int(70 * alfa), "stroke", 14, blur=10))
    cv.drawPath(PERNA, paint(PELE, int(190 * alfa), "stroke", 3))
    if borda > 0:                                                    # a pele "continua fechada"
        cv.drawPath(PERNA, paint("#FFD9C6", int(150 * borda * alfa), "stroke", 16, blur=9))
        cv.drawPath(PERNA, paint("#FFE6D8", int(235 * borda * alfa), "stroke", 4))
    masc = skia.Paint(AntiAlias=True)
    masc.setShader(skia.GradientShader.MakeLinear([skia.Point(0, y0), skia.Point(0, y0 + 120)],
                                                  [skia.ColorSetARGB(0, 0, 0, 0), skia.ColorSetARGB(255, 0, 0, 0)]))
    masc.setBlendMode(skia.BlendMode.kDstIn)
    cv.drawRect(skia.Rect(0, y0 - 40, W, y1 + 40), masc)
    cv.restore()


def peca(cv, pth):
    cv.drawPath(pth, paint("#000000", 70, blur=14))
    cv.drawPath(pth, paint(OSSO_C, shader=sombra_osso()))
    cv.drawPath(pth, paint(OSSO_L, 150, "stroke", 2.5))


def osso_inteiro(cv, brilho=0.0):
    if brilho > 0:
        cv.drawPath(OSSO_INTEIRO, paint(NOVO_G, int(120 * brilho), "stroke", 26, blur=22))
    peca(cv, OSSO_INTEIRO)
    cv.drawRect(skia.Rect(CX - 16, Y_TOPO + 250, CX + 16, Y_BASE - 190), paint(OSSO_B, 60, blur=6))


def tracejado(cv, x0, y0, x1, y1, cor, alfa, larg=5, traco=16, vazio=12, fase=0.0):
    if alfa <= 0:
        return
    p = paint(cor, int(alfa), "stroke", larg)
    p.setPathEffect(skia.DashPathEffect.Make([traco, vazio], fase))
    cv.drawLine(x0, y0, x1, y1, p)


def osso_v12(cv, t, T):
    """Vinhetas 1 e 2: as duas partes (corte planejado) em leve ângulo se alinham aos poucos; depois
    se afastam um pouco e o vão se enche de osso novo dourado."""
    th = theta(t, T); g = gap_alonga(t, T)
    cv.save(); cv.translate(0, g); cv.translate(CX, Y_C); cv.rotate(th); cv.translate(-CX, -Y_C)
    peca(cv, path_osso_inf(Y_C, Y_BASE))
    cv.restore()
    peca(cv, path_osso_sup(Y_TOPO, Y_C))
    if g > 0.5:
        dens = clamp(g / 16)
        brilho = prog(t, T["alonga"] + 0.05, T["alonga"] + 0.3)
        desenha_regenerado(cv, Y_C, Y_C + g, dens, max(brilho, 0.35 * dens), 0.0, t)
    a_corte = 1 - prog(t, T["alonga"] + 0.05, T["alonga"] + 0.25)
    if a_corte > 0:
        pisca = 0.5 + 0.5 * math.sin(t * 9)
        tracejado(cv, CX - H2 - 18, Y_C, CX + H2 + 18, Y_C, VERMELHO, a_corte * (150 + 105 * pisca), larg=6)


def osso_v3(cv, t, T):
    """Vinheta 3: um pedaço separado pela linha tracejada desliza para dentro da falha e deixa atrás
    um rastro de osso novo dourado (a mesma lógica visual do cf_transporte_osseo).
    O tornozelo fica ONDE a vinheta 2 o deixou (Y_BASE + GAP_A): no corte seco entre as vinhetas só
    o meio do osso muda, nada pula na ponta de baixo."""
    d = desloc(t, T)
    s0, s1 = Y_C + d, Y_C + SEG + d
    peca(cv, path_osso_sup(Y_TOPO, Y_C))
    seg = skia.Path(); seg.addRRect(skia.RRect.MakeRectXY(skia.Rect(CX - H2, s0, CX + H2, s1), 4, 4))
    peca(cv, seg)
    peca(cv, path_osso_inf(Y_G1, Y_BASE + GAP_A))
    if d > 3:                                                        # rastro de osso novo atrás do pedaço
        dens = 0.45 + 0.55 * clamp(d / 60)
        desenha_regenerado(cv, Y_C, s0, dens, 0.55, 0.0, t)
    resto = Y_G1 - s1
    if resto > 8:                                                    # a falha: contorno tracejado, vazia
        for xx in (CX - H2, CX + H2):
            tracejado(cv, xx, s1 + 6, xx, Y_G1 - 6, "#DDE6EE", 210, larg=4, traco=18, vazio=12, fase=-t * 10)
    a_tr = 1 - prog(t, T["ritmo"] - 0.6, T["ritmo"] - 0.3)
    if resto > 60 and a_tr > 0:                                       # trilha pontilhada + setinha
        passo = 24; y = s1 + 16 + (t * 40) % passo
        while y < Y_G1 - 40:
            cv.drawCircle(CX, y, 5, paint(OURO, int(220 * a_tr))); y += passo
        sp = skia.Path(); sp.moveTo(CX - 16, Y_G1 - 36); sp.lineTo(CX, Y_G1 - 18); sp.lineTo(CX + 16, Y_G1 - 36)
        cv.drawPath(sp, paint(OURO, int(255 * a_tr), "stroke", 6))
    r = skia.RRect.MakeRectXY(skia.Rect(CX - H2 - 3, s0 - 3, CX + H2 + 3, s1 + 3), 6, 6)   # o pedaço que viaja
    cv.drawRRect(r, paint(NOVO_G, 110, "stroke", 14, blur=8))
    cv.drawRRect(r, paint(OURO, 255, "stroke", 5))
    a_corte = 1 - clamp(d / 8)
    if a_corte > 0:
        pisca = 0.5 + 0.5 * math.sin(t * 9)
        tracejado(cv, CX - H2 - 18, Y_C, CX + H2 + 18, Y_C, VERMELHO, a_corte * (150 + 105 * pisca), larg=6)


# ------------------------------------------------------------------ desenho: fixador
def pino(cv, p0, p1, g, a):
    if a <= 0 or g <= 0:
        return
    x, y = lerp(p0[0], p1[0], g), lerp(p0[1], p1[1], g)
    cv.drawLine(p0[0], p0[1], x, y, paint("#000000", int(80 * a), "stroke", 13, blur=4))
    cv.drawLine(p0[0], p0[1], x, y, paint("#C6D3DF", int(255 * a), "stroke", 9))
    cv.drawLine(p0[0], p0[1] - 2, x, y - 2, paint(ACO_HL, int(190 * a), "stroke", 2.5))
    cv.drawCircle(x, y, 5.5, paint(ACO_ESC, int(255 * a)))                    # ponta do pino
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(p0[0] - 12, p0[1] - 11, p0[0] + 12, p0[1] + 11), 5, 5),
                 paint(ACO_ESC, int(255 * a)))                                  # presilha no anel
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(p0[0] - 8, p0[1] - 7, p0[0] + 8, p0[1] - 1), 3, 3),
                 paint(ACO_HL, int(160 * a)))


def t_pino(i, T):
    """Quando o pino i começa a crescer (o rotulado PINOS[3] é o 1º da fila)."""
    return T["pinos"] + 0.3 + 0.11 * ORDEM_PINO[i]


def estado_pino(i, t, T):
    """-> (quanto o traço já cresceu, alfa)."""
    if t < T["pinos"] + 0.15:
        g, a = 1.0, 1 - prog(t, T["pinos"] - 0.12, T["pinos"] + 0.08)
    else:
        ti = t_pino(i, T)
        g = e_out(prog(t, ti, ti + 0.22)); a = 1.0 if g > 0 else 0.0
    a *= (1 - vinheta(t, T)) * (1 - prog(t, T["sair"] - 0.15, T["sair"] + 0.1))
    return g, a


DIR1 = (-1, -1, 1, 1)                        # saída da vista desmontada (o contrário da entrada do piloto)
DIR2 = (-1, 1, -1, 1)                        # saída final, um a um


def aneis_dx(t, T):
    out = []
    for i in range(4):
        k1 = e_in_back(prog(t, T["pinos"] - 0.15 + 0.05 * i, T["pinos"] + 0.3 + 0.05 * i))
        k2 = e_back(prog(t, T["aneis"] - 0.3 + 0.09 * i, T["aneis"] + 0.2 + 0.09 * i))
        k3 = e_in_back(prog(t, T["sair"] - 0.05 + 0.14 * i, T["sair"] + 0.4 + 0.14 * i))
        out.append(DIR1[i] * 1250 * k1 * (1 - k2) + DIR2[i] * 1250 * k3)
    return out


def brilho_anel(cv, y, dx, k, cor=ACO_HL):
    if k <= 0:
        return
    r = skia.Rect(CX + dx - RX, y - RY, CX + dx + RX, y + RY)
    cv.drawArc(r, 0, 180, False, paint(cor, int(160 * k), "stroke", 22, blur=10))
    cv.drawArc(r, 0, 180, False, paint("#FFFFFF", int(230 * k), "stroke", 5))


def reflexo(cv, y, dx, u):
    """Brilho de metal correndo pelo arco da frente do anel (u: 0..1)."""
    if not 0 < u < 1:
        return
    r = skia.Rect(CX + dx - RX, y - RY, CX + dx + RX, y + RY)
    ang = lerp(170, 10, u) - 14; a = math.sin(math.pi * u)
    cv.drawArc(r, ang, 34, False, paint("#FFFFFF", int(170 * a), "stroke", 28, blur=10))
    cv.drawArc(r, ang, 30, False, paint("#FFFFFF", int(255 * a), "stroke", 8))


def contorno_ouro(cv, t, T, y3):
    """Contorno dourado que envolve fixador e osso ("segura"), traçado de uma vez."""
    pr = e_out(prog(t, T["segura"] + 0.1, T["segura"] + 0.6))
    a = pr * (1 - prog(t, T["pele"] + 0.25, T["pele"] + 0.7))
    if a <= 0:
        return
    x0, x1, ya, yb, rr = CX - RX - 20, CX + RX + 20, Y_AN[0] - RY - 34, y3 + RY + 30, 70
    per = 2 * ((x1 - x0) + (yb - ya)) - 8 * rr + 2 * math.pi * rr
    pth = skia.Path(); pth.addRRect(skia.RRect.MakeRectXY(skia.Rect(x0, ya, x1, yb), rr, rr))
    for larg, alfa, blur in ((22, 90, 14), (6, 255, 0)):
        p = paint(OURO, int(alfa * a), "stroke", larg, blur=blur)
        p.setPathEffect(skia.DashPathEffect.Make([per * pr + 0.1, per + 10], 0))
        cv.drawPath(pth, p)


def chave_boca(cv, x, y, ang, a):
    """Chave de boca simples (forma esquemática); a boca (abertura) encaixa em (x, y)."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.rotate(ang); cv.scale(1.25, 1.25); cv.translate(22, 0)
    cab = skia.Path(); cab.addCircle(0, 0, 42)
    fenda = skia.Path(); fenda.addRect(skia.Rect(-60, -16, 4, 16))
    forma = skia.Op(cab, fenda, skia.PathOp.kDifference_PathOp)
    cabo = skia.Path(); cabo.addRRect(skia.RRect.MakeRectXY(skia.Rect(26, -17, 320, 17), 17, 17))
    forma = skia.Op(forma, cabo, skia.PathOp.kUnion_PathOp)
    sh = skia.GradientShader.MakeLinear([skia.Point(0, -42), skia.Point(0, 42)], [C(ACO_HL), C(ACO), C(ACO_ESC)])
    cv.drawPath(forma, paint("#000000", int(90 * a), blur=10))
    p = paint(ACO, int(255 * a), shader=sh)
    cv.saveLayerAlpha(None, int(255 * a)); cv.drawPath(forma, p); cv.restore()
    cv.drawPath(forma, paint(ACO_ESC, int(255 * a), "stroke", 3))
    cv.restore()


# ------------------------------------------------------------------ peças de tela (fora da câmera)
def etiqueta(cv, linhas, x, y, ancora, cor, a, seta=False, cresce=1.0):
    """Caixa com 1 ou 2 linhas (canto sup. esq. em x, y) e linha fina até `ancora` (ponto ou seta).
    linhas = [(texto, fonte, tamanho, cor)]; `cresce` abre a 2ª linha."""
    if a <= 0:
        return
    x += 26 * (1 - e_out(a))
    vis = linhas[:1] + (linhas[1:] if cresce > 0 else [])
    larg = max(larg_texto(s, f, tam) for s, f, tam, _ in vis)
    larg = lerp(larg_texto(*linhas[0][:3]), larg, cresce) if len(vis) > 1 else larg
    alt = linhas[0][2] * 1.22 + sum(tam * 1.22 for _, _, tam, _ in linhas[1:]) * cresce + 22
    xa, ya = ancora
    ym = y + alt / 2
    cv.drawLine(xa, ya, x, ym, paint(cor, int(210 * a), "stroke", 3))
    if seta:
        ang = math.atan2(ya - ym, xa - x)
        p = skia.Path(); p.moveTo(xa, ya)
        for da in (2.6, -2.6):
            p.lineTo(xa + 24 * math.cos(ang + da), ya + 24 * math.sin(ang + da))
        p.close(); cv.drawPath(p, paint(cor, int(255 * a)))
    else:
        cv.drawCircle(xa, ya, 7, paint(cor, int(255 * a)))
    rr = skia.RRect.MakeRectXY(skia.Rect(x, y, x + larg + 34, y + alt), 14, 14)
    cv.drawRRect(rr, paint("#0B1824", int(220 * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 2.5))
    yy = y + 11
    for k, (s, f, tam, c) in enumerate(vis):
        aa = a if k == 0 else a * clamp((cresce - 0.35) / 0.65)
        yy += tam * 1.22 * (1 if k == 0 else cresce)
        if aa > 0:
            texto(cv, s, x + 17, yy - tam * 0.26, f, tam, c, int(255 * aa), centro=False)


def cartao(cv, s, x, y, a, tam=40, cor=OURO, dx_entrada=30):
    if a <= 0:
        return
    lw = larg_texto(s, F_BLACK, tam)
    x += dx_entrada * (1 - e_out(a))
    rr = skia.RRect.MakeRectXY(skia.Rect(x, y, x + lw + 48, y + tam + 42), 18, 18)
    cv.drawRRect(rr, paint("#0B1824", int(225 * a))); cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 3))
    texto(cv, s, x + 24, y + tam + 12, F_BLACK, tam, "#FFFFFF", int(255 * a), centro=False)


def checklist(cv, t, T, a):
    """Lista das 3 CAPACIDADES do aparelho (não são etapas de todo tratamento): sem ordinal e sem ✓;
    um marcador redondo acende em ouro na palavra, e o item da vez fica mais claro que os anteriores."""
    if a <= 0:
        return
    cv.save(); cv.translate(-34 * (1 - e_out(a)), 0)
    larg = max(max(larg_texto(s, F_BLACK, 40) for s, _, _ in ITENS),
               max(larg_texto(sub, F_SEMI, 32) for _, sub, _ in ITENS if sub))
    rr = skia.RRect.MakeRectXY(skia.Rect(40, 226, min(1040, 128 + larg + 44), 506), 22, 22)
    cv.drawRRect(rr, paint("#0B1824", int(205 * a))); cv.drawRRect(rr, paint(OURO, int(110 * a), "stroke", 2))
    ons = [e_out(prog(t, T[chave] - 0.05, T[chave] + 0.2)) for _, _, chave in ITENS] + [0.0]
    for k, ((s, sub, chave), y) in enumerate(zip(ITENS, (284, 348, 450))):
        t_on = T[chave]; on = ons[k]; depois = ons[k + 1]
        bx, by = 87, y - 15
        if on > 0:
            cv.drawCircle(bx, by, 22, paint(OURO, int(a * on * (120 * (1 - prog(t, t_on + 0.3, t_on + 0.9)) + 35)), blur=12))
        cv.drawCircle(bx, by, 13, paint("#0B1824", int(235 * a)))
        cv.drawCircle(bx, by, 13, paint(lerpc("#5E7186", OURO, on), int(255 * a), "stroke", 3.5))
        if on > 0:
            cv.drawCircle(bx, by, 8 * e_back(on), paint(OURO, int(255 * a * clamp(on * 2))))
        cor = lerpc(lerpc("#71859B", "#FFFFFF", on), "#B9C6D3", depois)
        texto(cv, s, 128, y, F_BLACK, 40, cor, int(255 * a), centro=False)
        if sub:
            a_sub = a * prog(t, t_on + 0.2, t_on + 0.45)
            if a_sub > 0:
                texto(cv, sub, 130, y + 40, F_SEMI, 32, AZUL, int(255 * a_sub), centro=False)
    cv.restore()


def prancheta(cv, x, y, a):
    """Ícone simples de prancheta com checklist (sem texto)."""
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x, y, x + 64, y + 78), 9, 9), paint("#EEF3F8", int(255 * a)))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x + 17, y - 7, x + 47, y + 9), 5, 5), paint(ACO_ESC, int(255 * a)))
    for k in range(3):
        yy = y + 26 + k * 17
        p = skia.Path(); p.moveTo(x + 10, yy - 2); p.lineTo(x + 15, yy + 3); p.lineTo(x + 23, yy - 7)
        cv.drawPath(p, paint("#C88E12", int(255 * a), "stroke", 3.5))
        cv.drawLine(x + 29, yy - 2, x + 54, yy - 2, paint("#9AA8B5", int(255 * a), "stroke", 4))


def cartao_ritmo(cv, t, T, a):
    if a <= 0:
        return
    tam = 42; lw = larg_texto(T_RITMO, F_BLACK, tam); wt = 28 + 64 + 22 + lw + 30
    x0 = CX - wt / 2; y0 = 228 - 16 * (1 - e_out(a))
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x0 + wt, y0 + 100), 20, 20)
    cv.drawRRect(rr, paint("#0B1824", int(225 * a))); cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 3))
    prancheta(cv, x0 + 28, y0 + 13, a)
    texto(cv, T_RITMO, x0 + 28 + 64 + 22, y0 + 66, F_BLACK, tam, "#FFFFFF", int(255 * a), centro=False)


def check_ouro(cv, cx, cy, r, pr, a):
    cv.drawCircle(cx, cy, r + 10, paint(OURO, int(90 * a * pr), blur=12))
    cv.drawCircle(cx, cy, r, paint("#0B1824", int(235 * a * pr)))
    cv.drawCircle(cx, cy, r, paint(OURO, int(255 * a * pr), "stroke", 4))
    p = skia.Path(); p.moveTo(cx - r * 0.45, cy)
    p.lineTo(cx - r * 0.45 + r * 0.33 * min(1, pr * 2), cy + r * 0.33 * min(1, pr * 2))
    if pr > 0.5:
        q = (pr - 0.5) * 2
        p.lineTo(cx - r * 0.12 + r * 0.62 * q, cy + r * 0.33 - r * 0.72 * q)
    cv.drawPath(p, paint(OURO, int(255 * a), "stroke", 6))


def cartao_final(cv, t, T, a):
    """COSTUMA SAIR (na palavra "sair") e, na palavra "papel", o check com a condição."""
    if a <= 0:
        return
    g = e_out(prog(t, T["papel"] - 0.05, T["papel"] + 0.35))
    w1 = larg_texto(T_SAIR, F_BLACK, 50); w2 = 60 + 16 + larg_texto(T_PAPEL, F_BLACK, 36)
    wt = lerp(w1, max(w1, w2), g) + 60; h = 92 + 62 * g
    x0 = CX - wt / 2; y0 = 226 - 16 * (1 - e_out(a))
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x0 + wt, y0 + h), 20, 20)
    cv.drawRRect(rr, paint("#0B1824", int(225 * a))); cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 3))
    texto(cv, T_SAIR, CX, y0 + 66, F_BLACK, 50, "#FFFFFF", int(255 * a))
    if g > 0.05:
        a2 = a * clamp((g - 0.8) / 0.2)                     # a 2ª linha só aparece com o cartão já aberto
        xs = CX - w2 / 2
        cv.save(); cv.clipRRect(rr, True)                   # e nada vaza da borda enquanto ele abre
        check_ouro(cv, xs + 28, y0 + 118, 26, e_out(prog(t, T["papel"], T["papel"] + 0.4)), a * clamp((g - 0.6) / 0.3))
        if a2 > 0:
            texto(cv, T_PAPEL, xs + 76, y0 + 131, F_BLACK, 36, OURO, int(255 * a2), centro=False)
        cv.restore()


def carimbo_duplo(cv, l1, l2, x, y, rot, t0, t, dur):
    """Carimbo vermelho do piloto, com uma segunda linha menor embaixo."""
    k = t - t0
    if k < 0 or k > dur:
        return
    esc = lerp(1.9, 1.0, e_out(clamp(k / 0.16))); a = clamp(k / 0.08) * (1 - prog(k, dur - 0.35, dur))
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(esc, esc)
    f1, f2 = skia.Font(F_BLACK, 56), skia.Font(F_BLACK, 40)
    w1, w2 = f1.measureText(l1), f2.measureText(l2); lw = max(w1, w2)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 26, -58, lw / 2 + 26, 70), 12, 12)
    cv.drawRRect(rr, paint("#0B1824", int(185 * a))); cv.drawRRect(rr, paint(VERMELHO, int(255 * a), "stroke", 7))
    cv.drawString(l1, -w1 / 2, 0, f1, paint(VERMELHO, int(255 * a)))
    cv.drawString(l2, -w2 / 2, 50, f2, paint("#FFFFFF", int(255 * a)))
    cv.restore()


def risco_x(cv, x, y, pr, a):
    if pr <= 0 or a <= 0:
        return
    for k, (dx0, dy0) in enumerate(((-1, -1), (1, -1))):
        q = clamp(pr * 2 - k)
        if q <= 0:
            continue
        x0, y0 = x + dx0 * 62, y + dy0 * 62
        x1, y1 = lerp(x0, x - dx0 * 62, q), lerp(y0, y + 62, q)
        cv.drawLine(x0, y0, x1, y1, paint("#000000", int(200 * a), "stroke", 20))
        cv.drawLine(x0, y0, x1, y1, paint(VERMELHO, int(255 * a), "stroke", 13))


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    cam = camera(t, T)
    fx, fy, sx, sy, s = cam
    v = vinheta(t, T)
    dxs = aneis_dx(t, T)
    aj = ajuste(t, T)
    g_al = gap_alonga(t, T) * v                       # na vinheta "alonga" os anéis de baixo descem junto
    y_an = [Y_AN[0], Y_AN[1], Y_AN[2] + AJ_PASSO * aj + g_al, Y_AN[3] + AJ_PASSO * aj + g_al]
    dim = lerp(1.0, 0.2, v)                           # fixador esmaecido ao fundo nas vinhetas
    a_haste = (1 - prog(t, T["pinos"] - 0.3, T["pinos"] - 0.12) + prog(t, T["aneis"] + 0.3, T["aneis"] + 0.6))
    a_haste = clamp(a_haste) * (1 - prog(t, T["sair"] - 0.25, T["sair"] - 0.05)) * dim
    metro = metronomo(T)
    n_metro = sum(e_out(prog(t, tc, tc + 0.12)) for tc in metro)

    # ================= mundo (câmera)
    # no close, a perna passaria da faixa da legenda: o mundo some em degradê antes de y 1232. A máscara
    # segue a ESCALA da câmera (não o relógio): fica inteira sempre que o zoom passa de ~0,95 (a partir
    # daí a ponta da perna desceria abaixo de 1232) e só solta quando a perna já cabe acima da legenda.
    m_close = clamp((s - 0.89) / 0.06)
    if m_close > 0:
        cv.saveLayer(None, None)
    cv.save(); cv.translate(sx, sy); cv.scale(s, s); cv.translate(-fx, -fy)
    borda = max(0.0, 1 - abs(t - (T["reabrir"] + 0.5)) / 0.7)
    desenha_perna(cv, 1 - v, borda)
    for i in range(4):
        anel(cv, y_an[i], dxs[i], dim, "tras")

    # osso: inteiro <-> vinhetas. CORTE SECO na metade de cada transição: só a pose dominante é
    # desenhada, opaca (nunca duas poses sobrepostas, nunca osso translúcido / tornozelo fantasma).
    # O corte vinheta 2 -> 3 cai na palavra "pedaço", mascarado por um brilho.
    t3 = troca_v3(T)
    w3 = 1.0 if t >= t3 else 0.0
    poses = [(1 - v, lambda: osso_inteiro(cv, brilho=max(0.0, 1 - abs(t - (T["papel"] + 0.35)) / 0.6))),
             (v * (1 - w3), lambda: osso_v12(cv, t, T)), (v * w3, lambda: osso_v3(cv, t, T))]
    max(poses, key=lambda p: p[0])[1]()
    brilhos(cv, CX, Y_C + 20, t, T["alonga"] + 0.12, n=14, raio=170)
    brilhos(cv, CX, Y_C + 60, t, t3 - 0.12, n=12, raio=170)       # já abertos no instante do corte
    brilhos(cv, CX, (Y_TOPO + Y_BASE) / 2, t, T["papel"] + 0.05, n=16, raio=260)

    # pinos (do anel até o osso) + o marcador neutro onde cada um cruza a pele. O pino INTEIRO
    # translada com o anel dele (fica paralelo); a ponta só desliza pela superfície do osso.
    a_pele = prog(t, T["pele"] - 0.05, T["pele"] + 0.3) * (1 - prog(t, T["reabrir"] - 0.2, T["reabrir"] + 0.3))
    for i, (r, p0, p1, u) in enumerate(PINOS):
        g, a = estado_pino(i, t, T)
        if a <= 0 or g <= 0:
            continue
        dy = y_an[r] - Y_AN[r]
        x0, y0 = p0[0], p0[1] + dy
        x1, y1 = ponta_pino(i, dy) if abs(dy) >= 0.5 else p1
        pino(cv, (x0, y0), (x1, y1), g, a)
        xc, yc = lerp(x0, x1, u), lerp(y0, y1, u)
        ti = t_pino(i, T)                                         # o traço passa pela pele: ponto acende
        k = max(0.0, 1 - abs(t - (ti + 0.22 * u)) / 0.18) if t > T["pinos"] else 0.0
        kp = max(k, a_pele)
        if kp > 0 and g >= u:                                     # marcador neutro e estável (não é "inflamação")
            cv.drawCircle(xc, yc, 11, paint(OURO, int(230 * kp * a), "stroke", 2.5))
            cv.drawCircle(xc, yc, 7, paint("#FFFFFF", int(200 * kp * a)))

    # hastes e porcas (as do meio têm rosca; a porca de baixo dá os passinhos do ajuste)
    for sxh in (-1, 1):
        x = CX + sxh * X_HASTE
        haste(cv, x, y_an[0], y_an[1], a_haste)
        haste(cv, x, y_an[1], y_an[2], a_haste, rosca=True, fase=aj * 3)
        haste(cv, x, y_an[2], y_an[3], a_haste)
        porca(cv, x, y_an[1] + 22, sxh * 15, a_haste)
        porca(cv, x, y_an[2] - 22, 10 - (GIRO * (aj + n_metro) if sxh > 0 else 0), a_haste)
    # porca do close / metrônomo: brilho a cada clique
    pulso = 0.0
    for tc in [T["ajusta"] + c for c in CLIQUES_AJ] + metro:
        pulso = max(pulso, 1 - clamp((t - tc) / 0.35) if t >= tc else 0.0)
    if pulso > 0 and a_haste > 0:
        cv.drawCircle(CX + X_HASTE, y_an[2] - 22, 30, paint(OURO, int(150 * pulso * a_haste), blur=12))
        porca(cv, CX + X_HASTE, y_an[2] - 22, 10 - GIRO * (aj + n_metro), a_haste)
    for i in range(4):
        anel(cv, y_an[i], dxs[i], dim, "frente")
        reflexo(cv, y_an[i], dxs[i], prog(t, T["gaiola"] + 0.08 + 0.1 * i, T["gaiola"] + 0.5 + 0.1 * i))
        brilho_anel(cv, y_an[i], dxs[i], max(0.0, 1 - abs(t - (T["fixador"] + 0.08 + 0.11 * i)) / 0.2) * dim)
    contorno_ouro(cv, t, T, y_an[3])

    # setinhas do "tiquinho" (no close): o anel desce
    a_set = prog(t, T["ajusta"] + 0.1, T["ajusta"] + 0.3) * (1 - prog(t, T["reabrir"] - 0.3, T["reabrir"]))
    if a_set > 0:
        # referência FIXA na haste: onde a porca estava antes do 1º clique (a descida se lê contra ela)
        xr, yr = CX + X_HASTE, Y_AN[2] - 22
        cv.drawLine(xr + 17, yr, xr + 42, yr, paint(OURO, int(235 * a_set), "stroke", 3.5))
        cv.drawLine(xr - 42, yr, xr - 17, yr, paint(OURO, int(235 * a_set), "stroke", 3.5))
        for k in range(2):
            yy = y_an[2] + RY + 22 + k * 15 + 5 * pulso
            p = skia.Path(); p.moveTo(CX + X_HASTE - 11, yy); p.lineTo(CX + X_HASTE, yy + 9); p.lineTo(CX + X_HASTE + 11, yy)
            cv.drawPath(p, paint(OURO, int(255 * a_set * (0.55 + 0.45 * pulso)), "stroke", 4))

    # a chave de boca que chega perto da porca e recua (riscada)
    ka = e_out(prog(t, T["apertar"] - 0.45, T["apertar"] + 0.05))
    kr = e_in_back(prog(t, T["apertar"] + 0.95, T["apertar"] + 1.45))
    a_ch = prog(t, T["apertar"] - 0.45, T["apertar"] - 0.25) * (1 - prog(t, T["apertar"] + 1.2, T["apertar"] + 1.45))
    if a_ch > 0:
        ang = 36; rec = 280 * (1 - ka) + 330 * kr
        nx, ny = CX + X_HASTE, y_an[2] - 22
        chave_boca(cv, nx + rec * math.cos(math.radians(ang)), ny + rec * math.sin(math.radians(ang)), ang, a_ch)
        hx = nx + (rec + 245) * math.cos(math.radians(ang)); hy = ny + (rec + 245) * math.sin(math.radians(ang))
        risco_x(cv, hx, hy, prog(t, T["apertar"] + 0.42, T["apertar"] + 0.72), a_ch)
    cv.restore()
    if m_close > 0:
        masc = skia.Paint(AntiAlias=True)
        masc.setShader(skia.GradientShader.MakeLinear(
            [skia.Point(0, 1120), skia.Point(0, 1232)],
            [skia.ColorSetARGB(255, 0, 0, 0), skia.ColorSetARGB(int(255 * (1 - m_close)), 0, 0, 0)]))
        masc.setBlendMode(skia.BlendMode.kDstIn)
        cv.drawRect(skia.Rect(0, 1000, W, H), masc)
        cv.restore()

    # ================= tela (rótulos, cartões, carimbos)
    X_COL = 612
    a = prog(t, T["fixador"] + 0.05, T["fixador"] + 0.3) * (1 - prog(t, T["pinos"] - 0.15, T["pinos"] + 0.05))
    etiqueta(cv, [(T_FIX, F_BLACK, 36, "#FFFFFF"), (T_ILI, F_SEMI, 32, AZUL)], X_COL, 380,
             na_tela(cam, CX + RX * math.cos(math.radians(32)), Y_AN[0] + RY * math.sin(math.radians(32))), ACO_HL, a,
             cresce=e_out(prog(t, T["ilizarov"] - 0.12, T["ilizarov"] + 0.12)))
    p_dir = [p for p in PINOS if p[1][0] > CX]
    a = prog(t, T["pinos"] + 0.4, T["pinos"] + 0.6) * (1 - prog(t, T["aneis"] - 0.3, T["aneis"] - 0.05))
    r, p0, p1, _ = p_dir[1]                                        # = PINOS[3], o 1º pino a crescer
    etiqueta(cv, [(T_PINOS, F_BLACK, 36, "#FFFFFF")], X_COL, 586, na_tela(cam, lerp(p0[0], p1[0], 0.35), lerp(p0[1], p1[1], 0.35)),
             "#C6D3DF", a)
    a = prog(t, T["ate"] - 0.05, T["ate"] + 0.2) * (1 - prog(t, T["aneis"] - 0.3, T["aneis"] - 0.05))
    r, p0, p1, _ = p_dir[2]
    etiqueta(cv, [(T_ATE, F_BLACK, 36, OURO)], X_COL, 952, na_tela(cam, p1[0] + 4, p1[1] + 2), OURO, a, seta=True)
    a = prog(t, T["aneis"] + 0.1, T["aneis"] + 0.35) * (1 - prog(t, T["segura"] - 0.1, T["segura"] + 0.15))
    etiqueta(cv, [(T_ANEIS, F_BLACK, 36, "#FFFFFF")], X_COL, 586, na_tela(cam, CX + RX - 4, Y_AN[1] + 10), ACO_HL, a)
    a = prog(t, T["segura"] + 0.15, T["segura"] + 0.4) * (1 - prog(t, T["ajusta"] - 0.5, T["ajusta"] - 0.25))
    etiqueta(cv, [(T_SEGURA, F_BLACK, 36, "#FFFFFF")], X_COL, 752, na_tela(cam, CX + H2 + 2, 730), OURO, a)
    a = prog(t, T["pele"] + 0.05, T["pele"] + 0.3) * (1 - prog(t, T["ajusta"] - 0.5, T["ajusta"] - 0.25))
    etiqueta(cv, [(T_PELE, F_BLACK, 36, "#FFFFFF")], X_COL, 968, na_tela(cam, CX + RX - 2, Y_AN[2] + 8), PELE, a)

    cartao(cv, T_POUCO, 600, 560, prog(t, T["aos"] - 0.05, T["aos"] + 0.25) * (1 - prog(t, T["reabrir"] - 0.25, T["reabrir"])), tam=38)
    carimbo_ouro(cv, T_REABRIR, CX, 690, -5, T["reabrir"] + 0.15, t, dur=0.95, tam=50)   # some antes da vinheta

    # vinhetas: checklist (até "ritmo") e rótulos do osso
    a_ck = prog(t, T["endireita"] - 0.25, T["endireita"] + 0.02) * (1 - prog(t, T["ritmo"] - 0.15, T["ritmo"] + 0.15))
    checklist(cv, t, T, a_ck)
    a = prog(t, T["endireita"] - 0.05, T["endireita"] + 0.25) * (1 - prog(t, T["puxa"] + 0.7, T["puxa"] + 1.0))
    etiqueta(cv, [(T_CORTE[0], F_BLACK, 36, "#FFFFFF"), (T_CORTE[1], F_BLACK, 36, "#FFFFFF")], 64, 740,
             na_tela(cam, CX - H2 - 20, Y_C), VERMELHO, a)
    d = desloc(t, T)
    a = prog(t, T["falha"] - 0.1, T["falha"] + 0.12) * (1 - prog(t, T["ritmo"] - 0.3, T["ritmo"] - 0.05))   # some antes do corte
    etiqueta(cv, [(T_FALHA, F_BLACK, 36, "#FFFFFF")], 760, 940,
             na_tela(cam, CX + H2 + 8, (Y_C + SEG + d + Y_G1) / 2), "#DDE6EE", a)

    # ritmo, chave riscada e o fim
    cartao_ritmo(cv, t, T, prog(t, T["ritmo"] + 0.1, T["ritmo"] + 0.4) * (1 - prog(t, T["aparelho"] - 0.4, T["aparelho"] - 0.1)))
    carimbo_duplo(cv, T_NADA, T_CONTA, CX, 600, -5, T["apertar"], t, T["aparelho"] - 0.1 - T["apertar"])
    cartao_final(cv, t, T, prog(t, T["sair"] + 0.1, T["sair"] + 0.4) * (1 - prog(t, T["manda"] - 0.35, T["manda"] - 0.1)))

    capa(cv, t, T["ilizarov"] + 0.3, ep["gancho"][0], ep["gancho"][1])
    selo_como_funciona(cv, prog(t, T["ilizarov"] + 0.75, T["ilizarov"] + 1.1) * (1 - prog(t, T["manda"] - 0.3, T["manda"]))
                       * (1 - clamp(m_close * 2)))        # no close o selo sai da frente da haste
    interface(cv, t, T, blocos, DESTAQUE)


# ------------------------------------------------------------------ som e prévias
def sons(T):
    ev = [(T["gaiola"] + 0.12 + 0.1 * i, "ping", 0.45) for i in range(4)]
    ev += [(T["fixador"] - 0.05, "whoosh", 0.3), (T["fixador"] + 0.05, "ping", 0.75), (T["ilizarov"] + 0.05, "pop", 0.5),
           (T["pinos"] - 0.15, "whoosh", 0.6)]
    ev += [(T["pinos"] + 0.3 + 0.11 * i, "tick", 0.42) for i in range(8)]          # um tique leve por pino
    ev += [(T["ate"] + 0.05, "pop", 0.45), (T["aneis"] - 0.3, "whoosh", 0.45)]
    ev += [(T["aneis"] - 0.11 + 0.09 * i, "ping", 0.6) for i in range(4)]          # cada anel encaixa
    ev += [(T["segura"] + 0.05, "thump", 0.85), (T["segura"] + 0.15, "shimmer", 0.4), (T["pele"], "shimmer", 0.5),
           (T["ajusta"] - 0.3, "whoosh", 0.4)]
    ev += [(T["ajusta"] + c, "click", 0.95) for c in CLIQUES_AJ]
    ev += [(T["aos"], "pop", 0.45), (T["reabrir"] - 0.15, "whoosh", 0.4), (T["reabrir"] + 0.15, "thump", 0.85),
           (T["endireita"] - 0.35, "whoosh", 0.45), (T["endireita"], "pop", 0.6)]
    t0, t1 = T["endireita"] + 0.05, T["alonga"] + 0.12
    ev += [(lerp(t0, t1, i / 4), "click", 0.6) for i in range(4)]
    ev += [(T["alonga"], "pop", 0.6), (T["alonga"] + 0.1, "shimmer", 0.8)]
    t0, t1 = janela_alonga(T)
    ev += [(lerp(t0, t1, i / 4), "click", 0.55) for i in range(4)]
    ev += [(T["puxa"], "pop", 0.6), (troca_v3(T) - 0.06, "whoosh", 0.35), (troca_v3(T), "shimmer", 0.45),
           (T["falha"], "pop", 0.45)]
    t0, t1 = janela_transporte(T)
    ev += [(lerp(t0, t1, i / 10), "click", 0.5) for i in range(10)]
    ev += [(T["ritmo"] - 0.1, "whoosh", 0.45), (T["ritmo"] + 0.12, "pop", 0.45)]
    ev += [(tc, "click", 0.9) for tc in metronomo(T)]                              # o metrônomo do ajuste
    ev += [(T["apertar"] - 0.45, "whoosh", 0.3), (T["apertar"], "thump", 0.9), (T["apertar"] + 0.45, "tick", 0.7),
           (T["apertar"] + 0.95, "whoosh", 0.3)]
    ev += [(T["sair"] - 0.05 + 0.14 * i, "whoosh", 0.45) for i in range(4)]
    ev += [(T["sair"] + 0.12, "pop", 0.4), (T["papel"], "ding", 0.6), (T["papel"] + 0.05, "shimmer", 0.5),
           (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def tempos_previa(T):
    return [0.25, T["ilizarov"] + 0.55, T["aneis"] - 0.45, T["aneis"] + 0.6, T["pele"] + 0.35, T["aos"] + 0.4,
            T["reabrir"] + 0.55, T["alonga"] + 0.75, T["falha"] + 0.3, T["apertar"] + 0.7, T["papel"] + 0.8,
            T["manda"] + 1.6]


# ------------------------------------------------------------------ entrada única
_PONTA = re.compile(r"[.,:;!?—…]+$")


def fazer_render_tolerante(quadro_fn, mapa, sons_fn, tempos_fn, respiro_cta=1.6):
    """Os MESMOS passos de cf_comum.fazer_render, só que limpando a pontuação que o edge-tts às vezes
    cola na palavra ("papel.") antes de alinhar com o roteiro (ver o docstring do módulo)."""
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


render = fazer_render_tolerante(quadro, ANCORAS, sons, tempos_previa, respiro_cta=2.0)   # ~2 s de leitura do check
