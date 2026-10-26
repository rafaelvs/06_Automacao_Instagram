# -*- coding: utf-8 -*-
"""MITO NA PROVA (piloto, v4) — "GAZE LIMPA / PODE SUJAR?" (v2: "UMA GAZE LIMPA / DÁ PRA 3 PINOS?").

Série nova, ao lado do COMO FUNCIONA, com OUTRA mecânica de atenção: a pessoa APOSTA e a resposta
fica ESCONDIDA até a revelação. Um teste justo com controle (mesma perna clonada, mesma tinta,
mesmos 3 pinos; só muda a gaze) roda à vista, mas a "sujeira" é TINTA INVISÍVEL: depois das
limpezas tudo PARECE limpo ("Parece limpo?"). A luz negra pisca no silêncio (o suspense) e acende:
em um lado a gaze e os pinos 2 e 3 brilham, no outro nada. Só então o carimbo bate MITO na pergunta.

v2 (25/10/2026) — correções do leitor às cegas e do revisor sobre a v1:
  * Quadro 0 = UMA perna grande, em pé, com o fixador monolateral (barra + 3 pinos) e o rótulo
    FIXADOR; a voz abre com "Fixador na perna" (a v1 parecia "porta-toalhas" e só dizia fixador no fim).
    A voz COMPLEMENTA o gancho (não repete a pergunta, como no cf_alongamento aprovado).
  * Em "prova" a perna se CLONA em duas (o teste justo) — colunas lado a lado, 3 pinos grandes (40 px),
    brilho da tinta ≥ 100 px. Nada de "dois, três, quatro" repetido; nada de carimbo com "?" no quadro 0.
  * A resposta NÃO vaza: a gaze descartada sai sem virar e a tinta é invisível até a luz negra.
  * O conta-gotas virou PINCEL de artesanato; a voz diz que a tinta faz "o papel da sujeira".
  * O carimbo paira ao lado do cartão (sem cruzar o texto), bate em "mito" e sai em 0,14 s; a marca
    MITO aparece já na palavra. Borracha lisa.
  * "Foi junto" em ciano-tinta (sem ouro nem estrelas); ouro só para o jeito que vale ("cada").
  * Sinais de alarme: pictogramas que entram UM POR PALAVRA num cartão que cobre a bancada inteira
    (sem lupa sobre pele normal, sem asterisco); "AVISE A EQUIPE" (lastro: cf_dor_alongamento).
  * Atrás da CTA só a bancada com as pernas (cartões, rótulos e números recolhidos antes).
v3 (25/10/2026) — polimento final (leitor às cegas e revisor sobre a v2):
  * Gancho-paradoxo "GAZE LIMPA PODE / SUJAR O PINO?" (o bom senso diz "não"; o teste diz VERDADE).
  * A APOSTA fica na tela: selo "MITO OU VERDADE?" e, no cartão do veredito, as duas opções lado a
    lado; uma roleta dourada alterna entre elas (tiques que desaceleram) e o carimbo bate em VERDADE.
  * Cartão do veredito descido para y ≥ 148 (fora do cabeçalho do Instagram); rótulos das condições
    somem enquanto ele está na tela; a lâmpada sobe sem recuo.
  * Ponte para o alarme: "Sinais de infecção:" (lastro: episodios_pos_op, "é assim que uma infecção
    pula de um ponto pro outro" / "olho nos sinais de infecção"); "Com febre, pronto-socorro." num bloco.
  * "tinta invisível fazendo papel de sujeira"; rótulos entram com pulo (sem etiqueta cinza vazia);
    reflexo branco na gaze em "só" (sem estrelas escuras); nada de pontinho dourado nas gazes certas;
    nada de faísca no lado limpo durante a luz negra; pele sob a luz negra só levemente violeta.
  * Cartão de alarme sai no lugar (some e encolhe, recortado na bancada); fone e termômetro separados;
    véu navy atrás da CTA.
v4 (26/10/2026) — gancho para QUEM NÃO USA fixador (leitores às cegas: "pinos" não fala com quem não
convive com o aparelho e eles passariam nos 2 primeiros segundos; o que os prendeu foi "limpar com algo
limpo pode sujar"):
  * Gancho "GAZE LIMPA / PODE SUJAR?" — sem "pino": gaze qualquer pai/mãe conhece, e o paradoxo é
    universal. O veredito continua VERDADE (o cartão repete o gancho).
  * A voz abre pelo objeto universal: "Gaze limpa, fixador na perna, três pinos." — o reflexo de limpa
    atravessa a gaze na palavra "limpa" (âncora; antes era um tempo fixo).
  * Quadro 0 = capa: a gaze é a protagonista — 50 % maior, no espaço livre da bancada (à direita da
    bandeja), com dois brilhos claros nas quinas; desliza ao lugar entre "Vamos" e "prova" (as duas
    colunas do teste começam iguais). O rótulo FIXADOR desceu para dar lugar a ela.
  * Rótulos das condições voltam (depois do cartão e do zoom) com pulo de escala, sem esmaecer.
Regras mantidas: pele OPACA, nada vermelho/crosta/secreção na pele, tinta só no METAL; a luz negra é
uma lâmpada desenhada (luz violeta clara, não fundo preto de exame); todo texto desenhado está em
ep["tela"] (ou é o gancho / a interface comum). Nenhum arquivo existente de animado/ foi editado.

Render: passos de cf_fixador_circular.fazer_render_tolerante (pontuação limpa) + 0,6 s de silêncio
logo depois de "negra" (a lâmpada pisca) + trilha baixa nos sinais de alarme (cópia local de som.mixar).
Velocidade (CPU a 99% com renders em paralelo; o quadro levava 5-9 s): neste skia, gradiente ou imagem
ESCALADA em área grande custa ~1 s, cópia 1:1 de imagem custa ms. Por isso fundo_rapido() é o MESMO
fundo do cf_alongamento (mesmo gradiente e partículas PART; diferença máx. 1 nível de cor, conferida)
copiado de uma imagem pronta, e a parte parada da coluna é desenhada uma vez por transformação e copiada.
A cena é PRESA ao roteiro pelas palavras-âncora (ANCORAS): roteiro sem elas = KeyError.
"""
import math
import os
import re

import numpy as np
import skia

from . import som, voz as _voz
from .base import codificar, previas as _previas
from .cf_alongamento import (ACO, ACO_ESC, ACO_HL, BG_IN, BG_OUT, CX, F_BLACK, H, OURO, PART, PELE, VERMELHO, W, C,
                             clamp, e_back, e_in_back, e_inout, e_out, fundo, larg_texto, lerp, lerpc,
                             paint, porca, prog, texto)
from .cf_comum import alinhar, ancoras, capa, comprimir, interface, montar_blocos

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "gaze0": ("gaze", 1, False), "limpa0": ("limpa", 1, False),
    "fixador": ("fixador", 1, False), "perna": ("perna", 1, False), "tres": ("três", 1, False),
    "pinos": ("pinos", 1, False),
    "vamos": ("vamos", 1, False), "prova": ("prova", 1, False),
    "pino": ("pino", 1, False), "um": ("um", 1, False), "tinta": ("tinta", 1, False),
    "invisivel": ("invisível", 1, False), "sujeira": ("sujeira", 1, False),
    "de": ("de", 2, False), "lado": ("lado", 1, False), "gaze2": ("gaze", 2, False),
    "para": ("para", 1, False), "tres2": ("três", 2, False),
    "do": ("do", 1, False), "outro": ("outro", 1, False), "uma3": ("uma", 2, False),
    "gaze3": ("gaze", 3, False), "por": ("por", 1, False), "pino2": ("pino", 2, False),
    "parece": ("parece", 1, False), "limpo": ("limpo", 1, False), "luz": ("luz", 1, False),
    "negra": ("negra", 1, False), "veredito": ("veredito", 1, False), "verdade": ("verdade", 1, False),
    "sujeira2": ("sujeira", 2, False), "pegou": ("pegou", 1, False), "carona": ("carona", 1, False),
    "gaze4": ("gaze", 4, False), "um3": ("um", 3, False), "material": ("material", 1, False),
    "cada": ("cada", 1, False), "pino3": ("pino", 3, False),
    "sinais": ("sinais", 1, False), "infeccao": ("infecção", 1, False),
    "pus": ("pus", 1, False), "cheiro": ("cheiro", 1, False), "vermelhidao": ("vermelhidão", 1, False),
    "cresce": ("cresce", 1, False), "dor": ("dor", 1, False), "avise": ("avise", 1, False),
    "equipe": ("equipe", 1, False), "febre": ("febre", 1, False),
    "pronto": ("pronto-socorro", 1, False), "manda": ("manda", 1, False),
}
# "verdade" fica FORA: o karaokê o pinta de ouro só enquanto é dito, sem brigar com o vermelho do carimbo
DESTAQUE = {"fixador", "invisível", "sujeira", "mentira", "negra", "carona", "cada", "infecção", "equipe",
            "pronto-socorro"}

# ------------------------------------------------------------------ textos de tela (todos em ep["tela"])
R_FIX = "FIXADOR"
R_SELO = "MITO OU VERDADE?"
R_TESTE = "TESTE"
R_A = "UMA GAZE SÓ"
R_B = "UMA GAZE POR PINO"
NUMS = ("1", "2", "3")
R_MITO = "MITO"
R_VERDADE = "VERDADE"
R_CARONA = "PEGOU CARONA"
R_INFEC = "SINAIS DE INFECÇÃO"
R_PUS, R_CHEIRO, R_VERM1, R_VERM2, R_DOR = "PUS", "MAU CHEIRO", "VERMELHIDÃO", "QUE CRESCE", "DOR NOVA"
R_AVISE = "AVISE A EQUIPE"
R_FEBRE = "FEBRE: PRONTO-SOCORRO"

# ------------------------------------------------------------------ paleta
NAVY = "#0B1824"
BANCADA, BANCADA_BORDA = "#F3EADB", "#D6C6AA"
BANDEJA, BANDEJA_BORDA = "#EADDC6", "#D2C09F"
GAZE_TRAMA, GAZE_BORDA = "#D5DFE9", "#8FA3B8"
PELE_CL, PELE_ESC, PELE_LINHA = "#F8D0BC", "#DC9A7E", "#C4866B"
MADEIRA, MADEIRA_CL, MADEIRA_ESC = "#B9844D", "#D9A86E", "#7B5129"
BORRACHA, BORRACHA_ESC, BORRACHA_CL = "#9A3F33", "#4E1A14", "#C0675A"
CARTAO = "#FBF6EC"
UV_LUZ, UV_MULT = "#8E7BFF", "#5A62D2"            # luz negra: violeta CLARO (não é fundo preto de exame)
UV_PELE = 0.42                                    # na pele o tom é ~metade do da bancada (0,82)
NEON, NEON_CORE = "#4FFFE6", "#E8FFFB"            # a tinta invisível brilhando na luz negra
SHEEN = "#BFF3FF"                                 # tinta molhada (transparente) logo depois do pincel

def t_gaze(T):
    """O reflexo de gaze LIMPA atravessa a gaze quando a voz diz "limpa" (v4: a voz abre com
    "Gaze limpa", o objeto que qualquer pai/mãe conhece, antes de dizer "fixador")."""
    return T["limpa0"] - 0.05


GAZE_CAPA = 0.50                                  # durante o gancho a gaze é a protagonista: +50 % de tamanho
POS_CAPA = (432, 100)                             # (local) no espaço livre da bancada, à direita da bandeja


def capa_k(t, T):
    """1 enquanto o gancho está na tela; vai a 0 entre "Vamos" e "prova" (antes do clone)."""
    return 1 - e_inout(prog(t, T["vamos"] - 0.1, T["prova"] - 0.12))


def esc_gaze_capa(t, T):
    """Escala extra da gaze ÚNICA enquanto o gancho está na tela; volta a 1 antes do clone em "prova"
    (as duas colunas do teste começam IGUAIS)."""
    return 1 + GAZE_CAPA * capa_k(t, T)

# ------------------------------------------------------------------ geometria (1080 x 1920)
BANC = (24, 364, 1056, 1226)                      # bancada creme: a cena fica acima de y≈1226
OX = 70                                           # centro horizontal (local) da coluna
TRAY = (-180, -12, 320, 826)                      # bandeja (local)
TOP0, S0 = 392, 1.0                               # quadro 0: UMA perna grande no centro
CA, CB, TOP1, S1 = 270, 810, 452, 0.86            # depois de "prova": duas colunas iguais
PY = (250, 420, 590)                              # altura dos 3 pinos (local)
PIN_R = 23                                        # meia espessura do pino (46 px local ≈ 40 px na tela)
BAR_X, BAR_W, BAR_Y0, BAR_Y1 = 215, 32, 160, 670
CLAMP_W, CLAMP_H = 70, 62
PIN_X1 = 266                                      # ponta de fora do pino (além da presilha)
PARK = (212, 72)                                  # gaze parada, à direita do joelho
GW, GH = 128, 112                                 # gaze (local)
_SHIN = [(-20, 104), (40, 104), (150, 99), (250, 92), (300, 88), (420, 81), (590, 73), (668, 70)]
CARD = (100, 148, 980, 440)                       # cartão do veredito: abaixo do cabeçalho do Instagram
Q_Y = (223, 293)                                  # linhas de base da pergunta no cartão
TAM_Q = 62
SLOT_Y, SLOT_H, SLOT_W = 368, 80, 314             # as duas opções (aposta) lado a lado
SLOT_X = {"mito": 361, "verdade": 719}
TAM_SLOT = 50
MARCA = (SLOT_X["verdade"], SLOT_Y)               # onde o carimbo bate
TAM_MARCA = 58
ZOOM, ZPIV = 1.35, (CA + S1 * (150 - OX), TOP1 + S1 * 330)
ALARME = (44, 392, 1036, 1208)                    # cartão dos sinais de alarme (cobre a bancada)


def shin_x(y):
    """x (local) da pele da canela na altura y (onde o pino entra)."""
    for (y0, x0), (y1, x1) in zip(_SHIN, _SHIN[1:]):
        if y0 <= y <= y1:
            return lerp(x0, x1, (y - y0) / (y1 - y0))
    return _SHIN[-1][1]


def junc(i):
    """Centro (local) da faixa do pino logo acima da pele: é onde a tinta fica."""
    return shin_x(PY[i]) + 22, PY[i]


# ------------------------------------------------------------------ utilidades
def _blend(p, modo):
    p.setBlendMode(modo)
    return p


def estrela(cv, px, py, s, cor, a, borda=None):
    p = skia.Path(); p.moveTo(px, py - s * 2); p.lineTo(px + s * 0.5, py - s * 0.5); p.lineTo(px + s * 2, py)
    p.lineTo(px + s * 0.5, py + s * 0.5); p.lineTo(px, py + s * 2); p.lineTo(px - s * 0.5, py + s * 0.5)
    p.lineTo(px - s * 2, py); p.lineTo(px - s * 0.5, py - s * 0.5); p.close()
    if borda:
        cv.drawPath(p, paint(borda, int(200 * clamp(a)), "stroke", 3))
    cv.drawPath(p, paint(cor, int(255 * clamp(a))))


def brilhos(cv, x, y, t, t0, n=8, raio=90, cor="#FFFFFF", dur=0.8, raio0=28):
    """Estrelinhas que NASCEM fora do objeto (raio0) e se afastam — nunca um nó escuro no centro."""
    k = t - t0
    if k < 0 or k > dur:
        return
    for i in range(n):
        ang = i * 2 * math.pi / n + 0.3
        d = lerp(raio0, raio, e_out(k / dur)) * (0.7 + 0.3 * ((i * 37) % 10) / 10)
        estrela(cv, x + d * math.cos(ang), y + d * math.sin(ang) * 0.8, 8 * (1 - k / dur) + 3, cor, 1 - k / dur,
                borda="#A9C4DC" if cor == "#FFFFFF" else None)


def brilho_limpa(cv, t, T, gx, gy, gr, eg):
    """Gaze LIMPA desde o quadro 0 (é a capa): dois brilhos claros nas quinas, que piscam até "Vamos",
    mais o brilho da quina quando a voz diz "limpa". Borda clara, nunca um nó escuro sobre a gaze."""
    a = 1 - prog(t, T["vamos"] - 0.1, T["vamos"] + 0.2)
    cv.save(); cv.translate(gx, gy); cv.rotate(gr)
    hw, hh = eg * GW / 2, eg * GH / 2
    if a > 0:
        for (dx, dy, s0, fase) in ((hw - 6, -hh + 6, 10, 0.0), (-hw + 16, hh - 14, 6.5, 1.7)):
            s = s0 * (0.82 + 0.18 * math.sin(t * 5 + fase))
            cv.drawCircle(dx, dy, 3.2 * s, paint("#BFE3FF", int(120 * a), blur=10))
            estrela(cv, dx, dy, s, "#FFFFFF", a, borda="#A9C4DC")
    kg = prog(t, t_gaze(T) + 0.4, t_gaze(T) + 0.95)
    if 0 < kg < 1:
        sx, sy = hw - 6, -hh + 6
        cv.drawCircle(sx, sy, 34, paint("#BFE3FF", int(170 * math.sin(math.pi * kg)), blur=10))
        estrela(cv, sx, sy, 9 * math.sin(math.pi * kg) + 4, "#FFFFFF", math.sin(math.pi * kg), borda="#A9C4DC")
    cv.restore()


def t_alarme(T):
    """Quando o cartão dos sinais de infecção entra (rótulos, números e ouro recolhem antes)."""
    return T["sinais"] - 0.12


def pulo(t, t0, dur=0.32, alt=1.0):
    k = t - t0
    if k < 0 or k > dur:
        return 0.0
    return alt * math.sin(math.pi * k / dur)


# ------------------------------------------------------------------ colunas (pose e transformação)
def pose(nome, t, T):
    """-> (cx, topo, escala, alfa) da coluna. Até "prova" há UMA perna no centro; em "prova" ela se
    clona: A vai para a esquerda, B nasce de trás dela e vai para a direita (mesma perna, teste justo)."""
    tp = T["prova"]
    u = e_inout(prog(t, tp - 0.05, tp + 0.5))
    if nome == "A":
        return lerp(540, CA, u), lerp(TOP0, TOP1, u), lerp(S0, S1, u), 1.0
    return lerp(540, CB, u), lerp(TOP0, TOP1, u), lerp(S0, S1, u), (1.0 if t >= tp - 0.05 else 0.0)


def na_coluna(cv, ps):
    cx, top, s, _a = ps
    cv.translate(cx - s * OX, top); cv.scale(s, s)


def tela_de(ps, x, y):
    cx, top, s, _a = ps
    return cx + s * (x - OX), top + s * y


def camera(t, T):
    """Zoom de verdade (1,35x) na coluna A em "sujeira pegou carona"; volta em "Um material"."""
    u = e_inout(prog(t, T["sujeira2"] - 0.05, T["sujeira2"] + 0.35)) * (1 - e_inout(prog(t, T["um3"], T["um3"] + 0.4)))
    return lerp(1.0, ZOOM, u), lerp(540, ZPIV[0], u), lerp(800, ZPIV[1], u)


def aplica_camera(cv, cam):
    z, px, py = cam
    cv.translate(540, 800); cv.scale(z, z); cv.translate(-px, -py)


def cam_tela(cam, x, y):
    z, px, py = cam
    return 540 + z * (x - px), 800 + z * (y - py)


# ------------------------------------------------------------------ bancada, bandeja, perna
_CACHE = {}


def fundo_rapido(cv, t):
    """O fundo do cf_alongamento (mesmo gradiente radial, mesmo centro que oscila, mesmas partículas),
    com o gradiente pronto numa imagem e copiado 1:1 (o original custava 1,5 s por quadro aqui)."""
    if "fundo" not in _CACHE:
        sf = skia.Surface(W, H + 80)
        c = sf.getCanvas()
        sh = skia.GradientShader.MakeRadial(skia.Point(W / 2, H * 0.42 + 40), H * 0.78, [C(BG_IN), C(BG_OUT)])
        c.drawRect(skia.Rect(0, 0, W, H + 80), paint(BG_IN, shader=sh))
        _CACHE["fundo"] = sf.makeImageSnapshot()
    cv.drawImage(_CACHE["fundo"], 0, round(40 * math.sin(t * 0.3) - 40))
    for x, y, v, r, a in PART:
        yy = (y - v * t * 6) % H
        cv.drawCircle(x + 8 * math.sin(t * 0.5 + y), yy, r, paint("#BFE3FF", int(a)))


def bancada(cv):
    if "banc" not in _CACHE:
        sf = skia.Surface(W, 1300)
        c = sf.getCanvas(); c.clear(skia.ColorTRANSPARENT)
        _bancada(c)
        _CACHE["banc"] = sf.makeImageSnapshot()
    cv.drawImage(_CACHE["banc"], 0, 0)


def _bancada(cv):
    x0, y0, x1, y1 = BANC
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 34, 34)
    cv.drawRRect(rr, paint("#000000", 120, blur=24))
    cv.drawRRect(rr, paint(BANCADA, 255, shader=skia.GradientShader.MakeLinear(
        [skia.Point(0, y0), skia.Point(0, y1)], [C("#F7F0E3"), C(BANCADA), C("#EDE2CF")])))
    cv.drawRRect(rr, paint(BANCADA_BORDA, 255, "stroke", 3))


def bandeja(cv):
    r = skia.Rect(*TRAY)
    cv.drawRRect(skia.RRect.MakeRectXY(r, 28, 28), paint(BANDEJA))
    cv.drawRRect(skia.RRect.MakeRectXY(r, 28, 28), paint(BANDEJA_BORDA, 255, "stroke", 3))


def _perna_path():
    """Perna em pé, vista de lado (pé para a direita): panturrilha abaulada atrás, canela quase reta
    na frente, tornozelo, calcanhar e pé com os dedos — o contorno que o leigo lê como "perna"."""
    p = skia.Path()
    p.moveTo(-110, -12)
    p.cubicTo(-120, 60, -152, 120, -150, 205)                 # panturrilha
    p.cubicTo(-148, 330, -86, 470, -66, 600)                  # afina até o tendão
    p.cubicTo(-60, 650, -64, 690, -72, 712)
    p.cubicTo(-94, 742, -98, 800, -58, 808)                   # calcanhar
    p.lineTo(228, 812)                                        # planta
    p.cubicTo(262, 812, 284, 792, 274, 772)                   # ponta dos dedos
    p.cubicTo(262, 756, 226, 750, 192, 742)                   # dorso dos dedos
    p.cubicTo(140, 726, 90, 702, 70, 668)                     # peito do pé subindo ao tornozelo
    p.cubicTo(60, 560, 82, 420, 88, 300)                      # canela
    p.cubicTo(94, 200, 112, 110, 104, 40)                     # tuberosidade e joelho
    p.cubicTo(100, 20, 98, 0, 96, -12)
    p.close()
    return p


PERNA = _perna_path()


def perna(cv):
    """Pele OPACA com sombreado cilíndrico; o topo some na bandeja por máscara (é um recorte)."""
    caixa = skia.Rect(-200, -20, 330, 840)
    cv.saveLayer(caixa, None)
    cv.drawOval(skia.Rect(-120, 796, 300, 830), paint("#6B4A2A", 80, blur=10))    # sombra no chão
    cv.drawPath(PERNA, paint(PELE, 255, shader=skia.GradientShader.MakeLinear(
        [skia.Point(-152, 0), skia.Point(112, 0)],
        [C(PELE_ESC), C("#E6A387"), C(PELE), C(PELE_CL), C(PELE), C("#E2A084")],
        [0.0, 0.18, 0.42, 0.62, 0.84, 1.0])))
    cv.save(); cv.clipPath(PERNA, skia.ClipOp.kIntersect, True)                    # pé: sombra no sentido dele
    cv.drawRect(skia.Rect(-110, 690, 300, 820), paint(PELE, 255, shader=skia.GradientShader.MakeLinear(
        [skia.Point(0, 700), skia.Point(0, 815)], [C(PELE, 0), C(PELE_CL, 150), C(PELE, 200), C(PELE_ESC, 255)],
        [0.0, 0.35, 0.65, 1.0])))
    cv.drawOval(skia.Rect(-26, 632, 14, 678), paint(PELE_ESC, 90, blur=6))        # tornozelo (maléolo)
    cv.drawOval(skia.Rect(-20, 636, 6, 660), paint("#FFFFFF", 60, blur=4))
    cv.restore()
    cv.drawLine(30, 130, 18, 610, paint("#FFFFFF", 70, "stroke", 14, blur=8))     # reflexo da canela
    for dx, dy in ((252, 778), (236, 772), (220, 768)):                             # dedos
        cv.drawArc(skia.Rect(dx - 10, dy - 6, dx + 10, dy + 14), 250, 120, False, paint(PELE_LINHA, 150, "stroke", 2))
    cv.drawPath(PERNA, paint(PELE_LINHA, 220, "stroke", 2.5))
    masc = skia.Paint(AntiAlias=True)
    masc.setShader(skia.GradientShader.MakeLinear([skia.Point(0, -12), skia.Point(0, 110)],
                                                  [skia.ColorSetARGB(0, 0, 0, 0), skia.ColorSetARGB(255, 0, 0, 0)]))
    masc.setBlendMode(skia.BlendMode.kDstIn)
    cv.drawRect(caixa, masc)
    cv.restore()


# ------------------------------------------------------------------ fixador (barra + 3 pinos)
def pino(cv, i, brilho=0.0):
    y = PY[i]; x0 = shin_x(y) - 24; r = PIN_R
    sh = skia.GradientShader.MakeLinear([skia.Point(0, y - r), skia.Point(0, y + r)],
                                        [C(ACO_ESC), C(ACO_HL), C(ACO), C(ACO_ESC)], [0.0, 0.32, 0.62, 1.0])
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y - r, PIN_X1, y + r), 10, 10)
    cv.drawRRect(rr, paint(ACO, 255, shader=sh))
    cv.drawRRect(rr, paint(ACO_ESC, 210, "stroke", 1.8))
    if brilho > 0:                                            # reflexo correndo pelo pino ("pinos")
        xx = lerp(x0 + 30, PIN_X1 - 30, brilho)
        cv.drawRect(skia.Rect(xx - 14, y - r + 3, xx + 14, y + r - 3), paint("#FFFFFF", int(220 * math.sin(math.pi * brilho))))


def entrada_pele(cv, i):
    """Só uma sombra neutra em tom de pele onde o pino entra (nada vermelho)."""
    x, y = shin_x(PY[i]), PY[i]
    cv.drawOval(skia.Rect(x - 9, y - 30, x + 9, y + 30), paint(PELE_LINHA, 150, blur=3))
    cv.drawOval(skia.Rect(x - 5, y - 25, x + 6, y + 25), paint("#B87A60", 170))


def barra(cv):
    r = skia.Rect(BAR_X - BAR_W / 2, BAR_Y0, BAR_X + BAR_W / 2, BAR_Y1)
    cv.drawRRect(skia.RRect.MakeRectXY(r.makeOffset(6, 6), 14, 14), paint("#000000", 60, blur=8))
    cv.drawRRect(skia.RRect.MakeRectXY(r, 14, 14), paint(ACO, 255, shader=skia.GradientShader.MakeLinear(
        [skia.Point(r.left(), 0), skia.Point(r.right(), 0)], [C(ACO_ESC), C(ACO_HL), C(ACO), C(ACO_ESC)],
        [0.0, 0.3, 0.6, 1.0])))
    cv.drawRRect(skia.RRect.MakeRectXY(r, 14, 14), paint(ACO_ESC, 255, "stroke", 2))


def presilha_corpo(cv, i):
    y = PY[i]
    rc = skia.Rect(BAR_X - CLAMP_W / 2, y - CLAMP_H / 2, BAR_X + CLAMP_W / 2, y + CLAMP_H / 2)
    cv.drawRRect(skia.RRect.MakeRectXY(rc, 10, 10), paint("#4A5A6C", 255, shader=skia.GradientShader.MakeLinear(
        [skia.Point(rc.left(), 0), skia.Point(rc.right(), 0)], [C("#4A5A6C"), C("#8FA3B8"), C("#4A5A6C")])))
    cv.drawRRect(skia.RRect.MakeRectXY(rc, 10, 10), paint("#2E3A47", 255, "stroke", 2))


def presilha(cv, i, num_a=0.0, num_esc=1.0, num_ouro=0.0):
    """Porca ou disco com o número do pino (o corpo da presilha está na imagem da coluna)."""
    y = PY[i]
    if num_a < 1:
        cv.save(); cv.translate(BAR_X, y); cv.scale(1.5, 1.5)
        porca(cv, 0, 0, 0, 1.0 - num_a)
        cv.restore()
    if num_a > 0:
        cv.save(); cv.translate(BAR_X, y); cv.scale(num_esc, num_esc)
        cv.drawCircle(0, 0, 27, paint(NAVY, int(240 * num_a)))
        cv.drawCircle(0, 0, 27, paint(lerpc(OURO, "#FFFFFF", num_ouro), int(255 * num_a), "stroke", 3))
        texto(cv, NUMS[i], 0, 13, F_BLACK, 38, "#FFFFFF", int(255 * num_a))
        cv.restore()


COL_BOX = (-200, -30, 340, 850)


def _coluna_estatica(cv):
    bandeja(cv)
    for i in range(3):
        pino(cv, i)
    perna(cv)
    for i in range(3):
        entrada_pele(cv, i)
    barra(cv)
    for i in range(3):
        presilha_corpo(cv, i)


_COLS = {}


def _desenho_rapido(cv, nome, box, fn, pt=None):
    """Desenha `fn` numa imagem do tamanho exato NA TELA (uma vez por transformação; as fases paradas
    reaproveitam) e copia 1:1 — mesmo resultado do desenho direto. `pt`: paint da cópia (ex.: filtro)."""
    m = cv.getTotalMatrix()
    if abs(m.getSkewX()) > 1e-6 or abs(m.getSkewY()) > 1e-6:
        if pt is None:
            fn(cv)
        else:
            cv.saveLayer(skia.Rect(*box), pt); fn(cv); cv.restore()
        return
    sx, sy, tx, ty = m.getScaleX(), m.getScaleY(), m.getTranslateX(), m.getTranslateY()
    chave = (nome, round(sx, 4), round(sy, 4), round(tx, 2), round(ty, 2))
    x0, y0, x1, y1 = box
    ix, iy = math.floor(tx + sx * x0), math.floor(ty + sy * y0)
    if chave not in _COLS:
        if len(_COLS) > 12:
            _COLS.pop(next(iter(_COLS)))
        w, h = math.ceil(tx + sx * x1) - ix + 1, math.ceil(ty + sy * y1) - iy + 1
        sf = skia.Surface(max(1, w), max(1, h))
        c = sf.getCanvas(); c.clear(skia.ColorTRANSPARENT)
        c.translate(tx - ix, ty - iy); c.scale(sx, sy)
        fn(c)
        _COLS[chave] = sf.makeImageSnapshot()
    cv.save(); cv.resetMatrix()
    cv.drawImage(_COLS[chave], ix, iy, skia.SamplingOptions(), pt)
    cv.restore()


def coluna_estatica_rapida(cv):
    _desenho_rapido(cv, "coluna", COL_BOX, _coluna_estatica)


def _perna_com_entradas(cv):
    perna(cv)
    for i in range(3):
        entrada_pele(cv, i)


def perna_sob_uv(cv, forca):
    """A perna redesenhada por cima da luz negra com um tom MAIS LEVE que o da bancada: pele sob luz
    violeta, não "perna roxa" (dedos roxos são sinal de alarme ensinado na própria série)."""
    if forca <= 0:
        return
    pt = skia.Paint(ColorFilter=skia.ColorFilters.Blend(C(lerpc("#FFFFFF", UV_MULT, forca)), skia.BlendMode.kModulate))
    _desenho_rapido(cv, "perna", COL_BOX, _perna_com_entradas, pt)


def coluna(cv, t, T, nome):
    """Bandeja, pinos, perna, barra e presilhas de uma coluna (sem gazes nem efeitos). A parte que
    não anima vem de uma imagem desenhada uma vez (1,5x a resolução local)."""
    coluna_estatica_rapida(cv)
    for i in range(3):                                         # reflexo correndo pelos pinos ("pinos")
        b = prog(t, T["pinos"] + 0.1 * i, T["pinos"] + 0.1 * i + 0.4)
        if 0 < b < 1:
            y = PY[i]; xa = shin_x(y) + 8; xb = BAR_X - CLAMP_W / 2 - 6
            xx = lerp(xa + 14, xb - 14, b)
            cv.drawRect(skia.Rect(xx - 14, y - PIN_R + 3, xx + 14, y + PIN_R - 3), paint("#FFFFFF", int(220 * math.sin(math.pi * b))))
    k = prog(t, T["perna"], T["perna"] + 0.55)                  # "perna": um brilho desce pela perna
    if 0 < k < 1:
        cv.save(); cv.clipPath(PERNA, skia.ClipOp.kIntersect, True)
        yy = lerp(-40, 860, k)
        cv.drawRect(skia.Rect(-200, yy - 40, 330, yy + 40), paint("#FFFFFF", int(90 * math.sin(math.pi * k)), blur=18))
        cv.restore()
    ts = (T["tres"], T["tres"] + 0.16, T["pinos"] + 0.06)
    some = 1 - prog(t, t_alarme(T) - 0.3, t_alarme(T))        # números recolhem antes do cartão/CTA
    for i in range(3):
        p = prog(t, ts[i], ts[i] + 0.3)
        esc = e_back(p) if p < 1 else 1.0
        esc += 0.25 * pulo(t, T["pino"], 0.4) * (i == 0) + 0.18 * pulo(t, T["um"], 0.35) * (i == 0)
        ouro = 0.0
        if nome == "B":
            ouro = prog(t, T["cada"] + 0.12 * i, T["cada"] + 0.12 * i + 0.2)
        presilha(cv, i, clamp(p * 3) * some, max(0.01, esc), ouro)


# ------------------------------------------------------------------ objetos
def gaze(cv, x, y, w, h, rot, a, esc=1.0, sombra=1.0, reflexo=None, anel=0.0):
    """Gaze dobrada: almofada branca com trama diagonal, bainha, espessura e contorno cinza-azulado.
    `reflexo` (0-1): faixa branca diagonal atravessando a gaze ("limpa"); `anel`: contorno dourado."""
    if a <= 0 or esc <= 0.01:
        return
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(esc, esc)
    hw, hh = w / 2, h / 2
    al = int(255 * a)
    if sombra > 0:
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-hw + 7, -hh + 12, hw + 7, hh + 12), 14, 14),
                     paint("#3A2A18", int(70 * a * sombra), blur=10))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-hw + 4, -hh + 6, hw + 4, hh + 6), 14, 14), paint("#DCE4EC", al))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-hw + 4, -hh + 6, hw + 4, hh + 6), 14, 14), paint(GAZE_BORDA, al, "stroke", 2))
    corpo = skia.RRect.MakeRectXY(skia.Rect(-hw, -hh, hw, hh), 14, 14)
    cv.drawRRect(corpo, paint("#FFFFFF", al, shader=skia.GradientShader.MakeLinear(
        [skia.Point(0, -hh), skia.Point(0, hh)], [C("#FFFFFF", al), C("#F4F7FA", al)])))
    cv.save(); cv.clipRRect(corpo, skia.ClipOp.kIntersect, True)
    pt = paint(GAZE_TRAMA, int(200 * a), "stroke", 1.3)
    k = -hw - hh
    while k < hw + hh:
        cv.drawLine(k, -hh, k + 2 * hh, hh, pt)
        cv.drawLine(k, hh, k + 2 * hh, -hh, pt)
        k += 9
    cv.drawRect(skia.Rect(-hw, -3, hw, 5), paint("#9FB2C5", int(80 * a), blur=4))
    if reflexo is not None and 0 < reflexo < 1:
        xx = lerp(-hw - 70, hw + 70, e_inout(reflexo))
        faixa = skia.Path(); faixa.moveTo(xx - 26, hh + 10); faixa.lineTo(xx + 8, hh + 10)
        faixa.lineTo(xx + 58, -hh - 10); faixa.lineTo(xx + 24, -hh - 10); faixa.close()
        cv.drawPath(faixa, paint("#FFFFFF", int(235 * a * math.sin(math.pi * reflexo)), blur=3))
    cv.restore()
    inset = 13
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-hw + inset, -hh + inset, hw - inset, hh - inset), 8, 8),
                 paint("#B8C7D6", int(230 * a), "stroke", 2))
    cv.drawRRect(corpo, paint(GAZE_BORDA, al, "stroke", 3))
    if anel > 0:
        r = skia.RRect.MakeRectXY(skia.Rect(-hw - 12, -hh - 12, hw + 12, hh + 12), 22, 22)
        cv.drawRRect(r, paint(OURO, int(255 * anel * a), "stroke", 7))
    cv.restore()


def pincel(cv, x, y, ang, a):
    """Pincel de artesanato (cabo de madeira, virola, cerdas molhadas de tinta transparente).
    (x, y) = ponta das cerdas; o cabo sobe para a direita."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.rotate(ang)
    al = int(255 * a)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-9, -330, 9, -92), 9, 9), paint("#000000", int(60 * a), blur=8))
    cabo = skia.RRect.MakeRectXY(skia.Rect(-10, -330, 10, -96), 10, 10)
    cv.drawRRect(cabo, paint(MADEIRA, al, shader=skia.GradientShader.MakeLinear(
        [skia.Point(-10, 0), skia.Point(10, 0)], [C(MADEIRA_ESC, al), C(MADEIRA_CL, al), C(MADEIRA, al)])))
    cv.drawRRect(cabo, paint(MADEIRA_ESC, al, "stroke", 2))
    vir = skia.Path(); vir.moveTo(-10, -98); vir.lineTo(10, -98); vir.lineTo(13, -50); vir.lineTo(-13, -50); vir.close()
    cv.drawPath(vir, paint("#C9D3DC", al, shader=skia.GradientShader.MakeLinear(
        [skia.Point(-13, 0), skia.Point(13, 0)], [C("#8FA3B8", al), C("#EEF3F7", al), C("#8FA3B8", al)])))
    cv.drawPath(vir, paint("#5E7186", al, "stroke", 2))
    cer = skia.Path(); cer.moveTo(-13, -52); cer.cubicTo(-16, -24, -8, -6, 0, 2)
    cer.cubicTo(8, -6, 16, -24, 13, -52); cer.close()
    cv.drawPath(cer, paint("#D9B98A", al))
    cv.drawPath(cer, paint("#9C7A4C", al, "stroke", 2))
    molh = skia.Path(); molh.moveTo(-10, -26); molh.cubicTo(-8, -10, -4, -3, 0, 2); molh.cubicTo(4, -3, 8, -10, 10, -26)
    molh.close()
    cv.drawPath(molh, paint(SHEEN, int(210 * a)))                 # ponta molhada de tinta transparente
    cv.drawCircle(-4, -18, 3, paint("#FFFFFF", int(220 * a)))
    cv.restore()


def lampada(cv, x0, x1, y, liga, a):
    """Lâmpada tubular de luz negra numa calha, pendurada acima da bancada."""
    if a <= 0:
        return
    for xx in (x0 + 60, x1 - 60):
        cv.drawLine(xx, -10, xx, y - 18, paint("#5E7186", int(255 * a), "stroke", 3))
    calha = skia.RRect.MakeRectXY(skia.Rect(x0, y - 24, x1, y + 6), 12, 12)
    cv.drawRRect(calha, paint("#000000", int(90 * a), blur=8))
    cv.drawRRect(calha, paint("#2B3440", int(255 * a)))
    tubo = skia.RRect.MakeRectXY(skia.Rect(x0 + 18, y - 2, x1 - 18, y + 26), 14, 14)
    if liga > 0:
        cv.drawRRect(tubo, _blend(paint(UV_LUZ, int(255 * a * liga), blur=40), skia.BlendMode.kPlus))
        cv.drawRRect(tubo, _blend(paint(UV_LUZ, int(200 * a * liga), blur=14), skia.BlendMode.kPlus))
    cv.drawRRect(tubo, paint(lerpc("#5B4A8A", "#D9CCFF", liga), int(255 * a)))
    cv.drawRRect(tubo, paint(lerpc("#3E3266", "#FFFFFF", liga), int(255 * a), "stroke", 2))
    for xx in (x0 + 8, x1 - 30):
        cv.drawRect(skia.Rect(xx, y - 6, xx + 22, y + 30), paint("#4A5A6C", int(255 * a)))


def claquete(cv, x, y, fecha, a):
    """Claquete do teste: a haste bate em "prova"."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y)
    lousa = skia.Rect(0, 40, 236, 150)
    cv.drawRRect(skia.RRect.MakeRectXY(lousa.makeOffset(4, 8), 10, 10), paint("#000000", int(110 * a), blur=10))
    cv.drawRRect(skia.RRect.MakeRectXY(lousa, 10, 10), paint("#1B2733", int(255 * a)))
    cv.drawRRect(skia.RRect.MakeRectXY(lousa, 10, 10), paint("#FFFFFF", int(200 * a), "stroke", 3))
    texto(cv, R_TESTE, 118, 116, F_BLACK, 52, "#FFFFFF", int(255 * a))

    def listras(r):
        cv.save(); cv.clipRect(r, skia.ClipOp.kIntersect, True)
        cv.drawRect(r, paint("#F4F4F4", int(255 * a)))
        xx = r.left() - 30
        while xx < r.right() + 30:
            p = skia.Path(); p.moveTo(xx, r.bottom()); p.lineTo(xx + 22, r.bottom()); p.lineTo(xx + 42, r.top())
            p.lineTo(xx + 20, r.top()); p.close()
            cv.drawPath(p, paint("#1B2733", int(255 * a))); xx += 44
        cv.restore()
        cv.drawRect(r, paint("#1B2733", int(255 * a), "stroke", 2))
    listras(skia.Rect(0, 18, 236, 40))
    cv.save(); cv.translate(2, 18); cv.rotate(-30 * (1 - fecha)); cv.translate(-2, -18)
    listras(skia.Rect(0, -4, 236, 18))
    cv.restore()
    cv.drawCircle(8, 18, 6, paint("#8FA3B8", int(255 * a)))
    cv.restore()


def carimbo_obj(cv, x, y, rot, esc, a, esmaga=0.0, larg=188):
    """Carimbo de madeira; (x, y) = centro da borracha (LISA: sem texto gravado). `larg` = largura da
    borracha (carimbo comprido para uma palavra comprida; o cabo não muda)."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(esc, esc * (1 - 0.06 * esmaga))
    hl = larg / 2
    al = int(255 * a)
    pesc = skia.Path(); pesc.moveTo(-17, -252)
    pesc.cubicTo(-12, -220, -10, -190, -30, -150); pesc.lineTo(30, -150)
    pesc.cubicTo(10, -190, 12, -220, 17, -252); pesc.close()
    madeira_h = skia.GradientShader.MakeLinear([skia.Point(-hl - 6, 0), skia.Point(hl + 6, 0)],
                                               [C(MADEIRA_ESC, al), C(MADEIRA_CL, al), C(MADEIRA, al), C(MADEIRA_ESC, al)],
                                               [0.0, 0.35, 0.65, 1.0])
    cv.drawPath(pesc, paint("#000000", int(70 * a), blur=8))
    cv.drawPath(pesc, paint(MADEIRA, al, shader=madeira_h))
    cv.drawPath(pesc, paint(MADEIRA_ESC, al, "stroke", 2))
    cv.drawCircle(0, -272, 32, paint(MADEIRA, al, shader=skia.GradientShader.MakeRadial(
        skia.Point(-10, -284), 40, [C(MADEIRA_CL, al), C(MADEIRA, al), C(MADEIRA_ESC, al)])))
    cv.drawCircle(0, -272, 32, paint(MADEIRA_ESC, al, "stroke", 2))
    for r, rad in ((skia.Rect(-64, -152, 64, -134), 6), (skia.Rect(-hl - 6, -136, hl + 6, -50), 10)):
        cv.drawRRect(skia.RRect.MakeRectXY(r, rad, rad), paint(MADEIRA, al, shader=madeira_h))
        cv.drawRRect(skia.RRect.MakeRectXY(r, rad, rad), paint(MADEIRA_ESC, al, "stroke", 2.5))
    for k, yy in enumerate((-118, -100, -80, -64)):
        p = skia.Path(); p.moveTo(-hl + 6, yy)
        p.cubicTo(-hl * 0.4, yy - 6 + 4 * k % 3, hl * 0.3, yy + 6, hl - 6, yy - 2)
        cv.drawPath(p, paint(MADEIRA_ESC, int(90 * a), "stroke", 2))
    cv.drawRect(skia.Rect(-hl - 3, -50, hl + 3, -41), paint("#3B2A20", al))
    rb = skia.Rect(-hl, -41, hl, 41)
    cv.drawRRect(skia.RRect.MakeRectXY(rb, 8, 8), paint(BORRACHA, al, shader=skia.GradientShader.MakeLinear(
        [skia.Point(0, -41), skia.Point(0, 41)], [C(BORRACHA_CL, al), C(BORRACHA, al), C("#7A2F26", al)])))
    cv.drawRRect(skia.RRect.MakeRectXY(rb, 8, 8), paint(BORRACHA_ESC, al, "stroke", 2.5))
    cv.restore()


def larg_marca(s=R_VERDADE, tam=TAM_MARCA):
    return skia.Font(F_BLACK, tam).measureText(s) + 56


def marca_carimbo(cv, s, x, y, rot, a, tam=TAM_MARCA, esc=1.0):
    """A marca que o carimbo deixa no cartão: palavra em vermelho, moldura e falhas de tinta."""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(esc, esc)
    r = skia.Rect(-lw / 2 - 28, -tam * 0.5 - 14, lw / 2 + 28, tam * 0.5 + 14)
    cv.drawRRect(skia.RRect.MakeRectXY(r, 14, 14), paint(CARTAO, int(255 * a)))
    cv.drawRRect(skia.RRect.MakeRectXY(r, 14, 14), paint(VERMELHO, int(235 * a), "stroke", 8))
    texto(cv, s, 0, tam * 0.36, F_BLACK, tam, VERMELHO, int(245 * a))
    rng = np.random.default_rng(11)
    for _ in range(40):
        cv.drawCircle(rng.uniform(-lw / 2 - 28, lw / 2 + 28), rng.uniform(-tam * 0.5 - 14, tam * 0.5 + 14),
                      rng.uniform(1.5, 4.0), paint(CARTAO, int(170 * a)))
    cv.restore()


def telefone(cv, x, y, a, toque, t, cor="#FFFFFF", esc=1.25):
    """Fone genérico (cópia do cf_dor_alongamento), sem logotipo de aplicativo."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc); cv.rotate(-28 + 9 * math.sin(t * 46) * toque)
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
    """Termômetro simples, sem número (cópia do cf_dor_alongamento)."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-12, -48, 12, 24), 12, 12), paint("#FFFFFF", int(255 * a)))
    cv.drawCircle(0, 32, 19, paint("#FFFFFF", int(255 * a)))
    cv.drawCircle(0, 32, 12, paint("#D64045", int(255 * a)))
    h = lerp(6, 64, clamp(nivel))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-5, 26 - h, 5, 32), 5, 5), paint("#D64045", int(255 * a)))
    cv.restore()


# ------------------------------------------------------------------ pictogramas dos sinais de alarme
def ico_gota(cv, a, t, k):
    p = skia.Path(); p.moveTo(0, -56)
    p.cubicTo(18, -30, 38, -8, 38, 14); p.cubicTo(38, 38, 20, 54, 0, 54)
    p.cubicTo(-20, 54, -38, 38, -38, 14); p.cubicTo(-38, -8, -18, -30, 0, -56); p.close()
    cv.drawPath(p, paint("#FFFFFF", int(50 * a)))
    cv.drawPath(p, paint("#FFFFFF", int(255 * a), "stroke", 6))
    cv.drawArc(skia.Rect(-22, 0, 2, 34), 120, 80, False, paint("#FFFFFF", int(200 * a), "stroke", 5))


def ico_cheiro(cv, a, t, k):
    nariz = skia.Path(); nariz.moveTo(-40, -50); nariz.cubicTo(-30, -20, -14, 6, -6, 24)
    nariz.cubicTo(-2, 34, -12, 44, -26, 40); nariz.cubicTo(-34, 38, -40, 44, -40, 50)
    cv.drawPath(nariz, paint("#FFFFFF", int(255 * a), "stroke", 6))
    for i in range(3):                                         # ondas de cheiro subindo
        xx = 12 + 16 * i; fase = t * 5 + i
        p = skia.Path(); p.moveTo(xx, 46)
        for j in range(1, 9):
            yy = 46 - j * 12
            p.lineTo(xx + 7 * math.sin(fase + j * 0.9), yy)
        cv.drawPath(p, paint("#FFFFFF", int(230 * a), "stroke", 5))


def ico_vermelhidao(cv, a, t, k, cresce=0.0):
    """Círculos que CRESCEM com setas para fora: o sinal é a vermelhidão AUMENTAR (sem lesão desenhada)."""
    r0 = lerp(16, 34, cresce)
    for j, rr in enumerate((r0, r0 + 14)):
        cv.drawCircle(0, 0, rr, paint("#FF8A80", int((230 - 70 * j) * a), "stroke", 5))
    for q in range(4):
        ang = q * math.pi / 2 + math.pi / 4
        d0, d1 = r0 + 22, r0 + 44
        x0, y0, x1, y1 = d0 * math.cos(ang), d0 * math.sin(ang), d1 * math.cos(ang), d1 * math.sin(ang)
        cv.drawLine(x0, y0, x1, y1, paint("#FFFFFF", int(255 * a), "stroke", 5))
        for s in (-1, 1):
            ah = ang + math.pi + s * 0.5
            cv.drawLine(x1, y1, x1 + 14 * math.cos(ah), y1 + 14 * math.sin(ah), paint("#FFFFFF", int(255 * a), "stroke", 5))


def ico_raio(cv, a, t, k):
    p = skia.Path(); p.moveTo(10, -58); p.lineTo(-28, 6); p.lineTo(-2, 6); p.lineTo(-14, 58)
    p.lineTo(28, -10); p.lineTo(2, -10); p.lineTo(16, -58); p.close()
    cv.drawPath(p, paint(OURO, int(255 * a)))
    cv.drawPath(p, paint("#8A6512", int(255 * a), "stroke", 3))


# ------------------------------------------------------------------ estado (tudo a partir de T)
def _esfrega(t, t0, t1, amp=12):
    if not (t0 <= t <= t1):
        return 0.0
    u = (t - t0) / (t1 - t0)
    return amp * math.sin(2 * math.pi * 2 * u)


def janelas_A(T):
    """(chega, esfrega até) em cada pino da gaze ÚNICA."""
    return [(T["lado"], T["lado"] + 0.42), (T["gaze2"], T["gaze2"] + 0.32), (T["tres2"], T["tres2"] + 0.34)]


def janelas_B(T):
    return [(T["outro"], T["outro"] + 0.36), (T["gaze3"] + 0.08, T["gaze3"] + 0.36), (T["pino2"], T["pino2"] + 0.32)]


def esfrega_pos(i):
    jx, jy = junc(i)
    return jx + 30, jy


def gaze_A(t, T):
    """-> (x, y, rot) LOCAL da gaze única da coluna A."""
    park = (PARK[0], PARK[1] + 5 * math.sin(t * 2.3))
    kc = capa_k(t, T)                                         # no gancho: grande, no espaço livre; desliza ao lugar
    x, y = lerp(park[0], POS_CAPA[0], kc), lerp(park[1], POS_CAPA[1], kc) - 30 * math.sin(math.pi * kc)
    y -= 24 * pulo(t, t_gaze(T), 0.34)
    rot = 4 * math.sin(t * 1.7)
    jan = janelas_A(T)
    ant = park
    for i, (ch, fim) in enumerate(jan):
        ida = ch - (0.27 if i == 0 else 0.26)
        if t < ida:
            break
        ex, ey = esfrega_pos(i)
        u = e_inout(prog(t, ida, ch))
        x = lerp(ant[0], ex, u); y = lerp(ant[1], ey, u) - 46 * math.sin(math.pi * u)
        y += _esfrega(t, ch, fim)
        rot = -4 + 6 * math.sin(math.pi * u)
        ant = (ex, ey)
    t_volta = jan[2][1] + 0.05
    if t >= t_volta:
        u = e_inout(prog(t, t_volta, t_volta + 0.4))
        x = lerp(ant[0], park[0], u); y = lerp(ant[1], park[1], u) - 40 * math.sin(math.pi * u)
        rot = lerp(-4, 4 * math.sin(t * 1.7), u)
    return x, y, rot


def trilha_A(t, T):
    """Pontos (local) por onde a gaze única passou — o tracejado branco que mostra 1 -> 2 -> 3."""
    jan = janelas_A(T)
    pts = []
    for i, (ch, fim) in enumerate(jan):
        if t >= ch:
            pts.append(junc(i))
    return pts


def gazes_B(t, T):
    """-> [(x, y, rot, a, esc)] LOCAL das gazes de B (uma POR pino). A 1ª sai SEM virar."""
    out = []
    park = (PARK[0], PARK[1] + 5 * math.sin(t * 2.3 + 1.1))
    x, y = park; y -= 24 * pulo(t, t_gaze(T) + 0.06, 0.34)
    rot = 4 * math.sin(t * 1.7 + 0.8); a = 1.0
    (c1, f1), (c2, f2), (c3, f3) = janelas_B(T)
    ida = c1 - 0.22
    if t >= ida:
        ex, ey = esfrega_pos(0)
        u = e_inout(prog(t, ida, c1))
        x = lerp(park[0], ex, u); y = lerp(park[1], ey, u) - 40 * math.sin(math.pi * u)
        y += _esfrega(t, c1, f1); rot = -4
    if t >= f1:                                                   # descarte: sai pela DIREITA, abaixo do rótulo
        k = prog(t, f1, f1 + 0.42)
        ex, ey = esfrega_pos(0)
        x = lerp(ex, 640, e_in_back(k, 0.9)); y = ey - 60 * math.sin(math.pi * k * 0.8)
        rot = -4 + 25 * k
        a = 0.0 if k >= 1 else 1.0
    out.append((x, y, rot, a, 1.0))
    for i, (ch, fim) in ((1, (c2, f2)), (2, (c3, f3))):         # gazes NOVAS, uma por pino
        tn = ch - 0.2
        if t < tn:
            continue
        ex, ey = esfrega_pos(i)
        esc = e_back(prog(t, tn, tn + 0.22))
        yy = ey - 30 * (1 - e_out(prog(t, tn, ch))) + _esfrega(t, ch, fim, amp=11)
        sai = prog(t, fim, fim + 0.32)
        xx = ex + 260 * e_in_back(sai, 0.9)
        out.append((xx, yy - 40 * sai, 2 * math.sin(t * 1.9 + i), 1.0 if sai < 1 else 0.0, max(0.01, esc)))
    return out


def foco(t, T, nome):
    """Véu creme (0-1) na coluna que NÃO está em foco (escurecer deixaria a pele arroxeada)."""
    if nome == "B":
        d = prog(t, T["de"] - 0.1, T["de"] + 0.15) * (1 - prog(t, T["do"] - 0.2, T["do"]))
    else:
        d = prog(t, T["do"] - 0.1, T["do"] + 0.15) * (1 - prog(t, T["parece"] - 0.25, T["parece"]))
        d = max(d, 0.6 * prog(t, T["material"] - 0.1, T["material"] + 0.25) * (1 - prog(t, t_alarme(T) - 0.3, t_alarme(T))))
    return 0.62 * d


def uv(t, T):
    """Intensidade da luz negra (0-1): pisca no silêncio depois de "negra", acende, apaga em "Um"."""
    tn = T["negra"] + 0.12
    t_on = T["veredito"] - 0.42
    if t < tn:
        return 0.0
    if t < t_on:
        for a0, a1 in ((0.0, 0.07), (0.2, 0.25), (0.42, 0.52), (0.62, 0.66)):
            if tn + a0 <= t < tn + a1:
                return 0.55
        return 0.0
    return e_out(prog(t, t_on, t_on + 0.22)) * (1 - e_inout(prog(t, T["um3"], T["um3"] + 0.35)))


def tinta_A(t, T):
    """Quanto da tinta invisível está em cada lugar de A (pinos 2, 3 e a gaze) — só aparece na luz negra."""
    j = janelas_A(T)
    return {"p2": prog(t, j[1][0], j[1][0] + 0.2), "p3": prog(t, j[2][0], j[2][0] + 0.2),
            "gaze": prog(t, j[0][0], j[0][0] + 0.2)}


def tempos_revela(T):
    t_on = T["veredito"] - 0.42
    return {"p2": t_on + 0.12, "p3": t_on + 0.27, "gaze": t_on + 0.42}


# ------------------------------------------------------------------ desenho de cada camada
def tinta_molhada(cv, t, T):
    """Pincel em "tinta": a faixa do pino 1 fica molhada (transparente) e SOME em "invisível"."""
    ts = T["tinta"]; ti = T["invisivel"]
    a = prog(t, ts + 0.05, ts + 0.2) * (1 - prog(t, ti + 0.05, ti + 0.5))
    if a <= 0:
        return
    jx, jy = junc(0)
    r = skia.RRect.MakeRectXY(skia.Rect(jx - 18, jy - PIN_R - 3, jx + 18, jy + PIN_R + 3), 10, 10)
    cv.drawRRect(r, paint(SHEEN, int(170 * a)))
    cv.drawRRect(r, paint("#7FC8E0", int(200 * a), "stroke", 2.5))
    cv.drawLine(jx - 8, jy - 14, jx - 8, jy + 6, paint("#FFFFFF", int(230 * a), "stroke", 4))


def marca_sujeira(cv, t, T, nome):
    """Em "sujeira": círculo tracejado no pino 1 (a tinta invisível está ali); some quando a gaze limpa."""
    ts = T["sujeira"]
    limpa = janelas_A(T)[0][0] if nome == "A" else janelas_B(T)[0][0]
    a = prog(t, ts - 0.05, ts + 0.15) * (1 - prog(t, limpa + 0.1, limpa + 0.35))
    if a <= 0:
        return
    jx, jy = junc(0)
    r = 58 + 6 * pulo(t, ts, 0.35)
    p = paint("#FFFFFF", int(240 * a), "stroke", 5)
    p.setPathEffect(skia.DashPathEffect.Make([16, 11], -t * 40))
    cv.drawCircle(jx, jy, r + 2, paint("#5E7186", int(150 * a), "stroke", 9))
    cv.drawCircle(jx, jy, r, p)


def rastro_branco(cv, t, T):
    """Tracejado branco da rota da gaze ÚNICA (1 -> 2 -> 3) enquanto ela passa; some depois."""
    pts = trilha_A(t, T)
    a = 1 - prog(t, janelas_A(T)[2][1] + 0.2, janelas_A(T)[2][1] + 0.6)
    if len(pts) < 1 or a <= 0:
        return
    gx, gy, _ = gaze_A(t, T)
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if t < janelas_A(T)[2][1]:
        p.lineTo(gx - 30, gy)
    pt = paint("#FFFFFF", int(230 * a), "stroke", 5)
    pt.setPathEffect(skia.DashPathEffect.Make([14, 10], -t * 50))
    cv.drawPath(p, paint("#5E7186", int(140 * a), "stroke", 9))
    cv.drawPath(p, pt)


def neon(cv, x0, y0, x1, y1, a, rad=10):
    """Brilho da tinta na luz negra (soma de luz: sem mancha escura, sem cor de lesão)."""
    if a <= 0:
        return
    def rr(d):
        return skia.RRect.MakeRectXY(skia.Rect(x0 - d, y0 - d, x1 + d, y1 + d), max(1, rad + d), max(1, rad + d))
    cv.drawRRect(rr(46), _blend(paint(NEON, int(120 * a), blur=40), skia.BlendMode.kPlus))
    cv.drawRRect(rr(18), _blend(paint(NEON, int(170 * a), blur=18), skia.BlendMode.kPlus))
    cv.drawRRect(rr(0), _blend(paint(NEON, int(240 * a), blur=5), skia.BlendMode.kPlus))
    cv.drawRRect(rr(-6), paint(NEON_CORE, int(235 * a), blur=2))


def brilho_pino(cv, i, a, pulso=0.0, t=0.0, t_rev=None):
    jx, jy = junc(i)
    w = 26 * (1 + 0.25 * pulso)
    neon(cv, jx - w, jy - PIN_R - 4, jx + w, jy + PIN_R + 4, a, rad=14)
    if t_rev is not None and a > 0:                              # anel que estoura quando acende
        k = t - t_rev
        if 0 <= k <= 0.5:
            cv.drawCircle(jx, jy, lerp(40, 150, e_out(k / 0.5)),
                          _blend(paint(NEON, int(230 * (1 - k / 0.5)), "stroke", 7), skia.BlendMode.kPlus))


def brilho_gaze(cv, x, y, rot, a, pulso=0.0):
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(1 + 0.12 * pulso, 1 + 0.12 * pulso)
    m = skia.Path()
    for i in range(20):
        ang = i * 2 * math.pi / 20
        r = 46 + 8 * math.sin(i * 2.7) + 5 * math.cos(i * 1.3)
        (m.moveTo if i == 0 else m.lineTo)(-14 + r * math.cos(ang), 6 + r * 0.8 * math.sin(ang))
    m.close()
    cv.drawPath(m, _blend(paint(NEON, int(130 * a), blur=40), skia.BlendMode.kPlus))
    cv.drawPath(m, _blend(paint(NEON, int(170 * a), blur=18), skia.BlendMode.kPlus))
    cv.drawPath(m, _blend(paint(NEON, int(220 * a), blur=4), skia.BlendMode.kPlus))
    cv.drawPath(m, paint(NEON_CORE, int(150 * a), blur=3))
    cv.restore()


def rastro_neon(cv, t, T):
    """Em "sujeira pegou carona": a rota 1 -> 2 -> 3 em tracejado NEON, com um ponto correndo."""
    ts = T["sujeira2"]
    a = prog(t, ts - 0.05, ts + 0.15) * (1 - prog(t, T["um3"] - 0.1, T["um3"] + 0.2))
    if a <= 0:
        return
    cresce = e_out(prog(t, ts, ts + 0.6))
    p = skia.Path(); x0, y0 = junc(0); p.moveTo(x0 + 6, y0)
    for i in (1, 2):
        xa, ya = junc(i - 1); xb, yb = junc(i)
        p.cubicTo(xa + 150, ya + 30, xb + 150, yb - 30, xb + 6, yb)
    med = skia.PathMeasure(p, False); L = med.getLength()
    seg = skia.Path(); med.getSegment(0, L * cresce, seg, True)
    pt = _blend(paint(NEON, int(255 * a), "stroke", 7), skia.BlendMode.kPlus)
    pt.setPathEffect(skia.DashPathEffect.Make([20, 13], -t * 70))
    cv.drawPath(seg, _blend(paint(NEON, int(110 * a), "stroke", 18, blur=8), skia.BlendMode.kPlus))
    cv.drawPath(seg, pt)
    f = (t - ts) * 0.9 % 1.0 if cresce >= 1 else cresce
    pos, _tan = med.getPosTan(L * f)
    cv.drawCircle(pos.x(), pos.y(), 12, _blend(paint(NEON, int(255 * a), blur=6), skia.BlendMode.kPlus))
    cv.drawCircle(pos.x(), pos.y(), 7, paint(NEON_CORE, int(255 * a)))


def ouro_B(cv, t, T):
    """Em "cada": o jeito que vale acende — contorno dourado na bandeja e uma gazinha nova por pino,
    cada uma com um anel dourado NÍTIDO (nada de pontinho ou mancha amarela sobre a gaze)."""
    ac = prog(t, T["material"] - 0.05, T["material"] + 0.25) * (1 - prog(t, t_alarme(T) - 0.35, t_alarme(T)))
    if ac <= 0:
        return
    r = skia.Rect(*TRAY)
    cv.drawRRect(skia.RRect.MakeRectXY(r, 28, 28), paint(OURO, int(120 * ac), "stroke", 18, blur=9))
    cv.drawRRect(skia.RRect.MakeRectXY(r, 28, 28), paint(OURO, int(255 * ac), "stroke", 7))
    for i in range(3):
        ti = T["cada"] + 0.12 * i
        k = prog(t, ti, ti + 0.25)
        if k <= 0:
            continue
        ex, ey = esfrega_pos(i)
        gaze(cv, ex + 6, ey, 92, 80, 3 * math.sin(i * 2.1), ac * clamp(k * 2), esc=max(0.01, e_back(k)), sombra=0.6,
             anel=prog(t, ti + 0.1, ti + 0.3))


def sombra(cv, x0, y0, x1, y1, rad, blur, a):
    """Sombra borrada de um retângulo arredondado, desenhada uma vez por tamanho e reaproveitada."""
    if a <= 0:
        return
    w, h = x1 - x0, y1 - y0
    chave = ("sombra", int(w), int(h), rad, blur)
    m = 3 * blur
    if chave not in _CACHE:
        sf = skia.Surface(int(w + 2 * m), int(h + 2 * m))
        c = sf.getCanvas(); c.clear(skia.ColorTRANSPARENT)
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(m, m, m + w, m + h), rad, rad), paint("#000000", 255, blur=blur))
        _CACHE[chave] = sf.makeImageSnapshot()
    p = skia.Paint(); p.setAlphaf(clamp(a))
    cv.drawImage(_CACHE[chave], x0 - m, y0 - m, skia.SamplingOptions(), p)


def veu(cv, d):
    if d <= 0:
        return
    r = skia.Rect(TRAY[0] - 3, TRAY[1] - 3, TRAY[2] + 3, TRAY[3] + 3)
    cv.drawRRect(skia.RRect.MakeRectXY(r, 28, 28), paint(BANCADA, int(255 * d)))


def rotulo(cv, s, x, y, a, ouro=0.0, esc=1.0):
    """Rótulo da condição acima da coluna (navy, texto branco; ouro no jeito que vale). Entra com
    PULO de escala e opacidade cheia (a v2 entrava esmaecida e lia como etiqueta cinza vazia)."""
    if a <= 0 or esc <= 0.01:
        return
    lw = larg_texto(s, F_BLACK, 36)
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 22, -26, lw / 2 + 22, 26), 26, 26)
    cv.drawRRect(rr, paint("#000000", int(70 * a), blur=8))
    cv.drawRRect(rr, paint(NAVY, int(240 * a)))
    cv.drawRRect(rr, paint(lerpc("#5E7186", OURO, ouro), int(255 * a), "stroke", 3))
    texto(cv, s, 0, 13, F_BLACK, 36, lerpc("#FFFFFF", OURO, ouro), int(255 * a))
    cv.restore()


def chip(cv, s, x, y, a, esc=1.0, fundo_cor=NEON, cor=NAVY):
    if a <= 0:
        return
    lw = larg_texto(s, F_BLACK, 42)
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 26, -34, lw / 2 + 26, 32), 32, 32)
    cv.drawRRect(rr, paint("#000000", int(90 * a), blur=10))
    cv.drawRRect(rr, paint(fundo_cor, int(255 * a)))
    cv.drawRRect(rr, paint(NAVY, int(255 * a), "stroke", 3))
    texto(cv, s, 0, 15, F_BLACK, 42, cor, int(255 * a))
    cv.restore()


def tag_fixador(cv, t, T, ps):
    """Rótulo FIXADOR apontando a barra (desde o quadro 0; sai em "vamos")."""
    a = 1 - prog(t, T["vamos"], T["vamos"] + 0.3)
    if a <= 0:
        return
    bx, by = tela_de(ps, BAR_X + 18, 330)
    pulso = 1 + 0.08 * pulo(t, T["fixador"], 0.4)
    x, y = 875, 706                                           # abaixo da gaze grande da capa
    cv.drawLine(bx, by, x - 112, y, paint(OURO, int(230 * a), "stroke", 4))
    cv.drawCircle(bx, by, 8, paint(OURO, int(255 * a)))
    cv.save(); cv.translate(x, y); cv.scale(pulso, pulso)
    lw = larg_texto(R_FIX, F_BLACK, 40)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 22, -32, lw / 2 + 22, 30), 16, 16)
    cv.drawRRect(rr, paint(NAVY, int(240 * a)))
    cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 3))
    texto(cv, R_FIX, 0, 14, F_BLACK, 40, OURO, int(255 * a))
    cv.restore()


def selo_serie(cv, t, a, esc=1.0, flash=0.0):
    """Selo da série = a APOSTA: ponto vermelho DESENHADO (círculo) + MITO OU VERDADE?"""
    if a <= 0 or esc <= 0.01:
        return
    lw = larg_texto(R_SELO, F_BLACK, 32)
    conteudo = 20 + 14 + lw
    cv.save(); cv.translate(CX, 177); cv.scale(esc, esc)
    x0 = -conteudo / 2
    rr = skia.RRect.MakeRectXY(skia.Rect(x0 - 28, -27, x0 + conteudo + 28, 27), 27, 27)
    cv.drawRRect(rr, paint("#FFFFFF", int((28 + 60 * flash) * a)))
    if flash > 0:
        cv.drawRRect(rr, paint(OURO, int(255 * flash * a), "stroke", 3))
    pulso = 0.5 + 0.5 * math.sin(t * 4)
    cv.drawCircle(x0 + 10, 0, 14, paint(VERMELHO, int(90 * a * pulso), blur=5))
    cv.drawCircle(x0 + 10, 0, 10, paint(VERMELHO, int(255 * a)))
    texto(cv, R_SELO, x0 + 34, 12, F_BLACK, 32, "#FFFFFF", int(255 * a), centro=False)
    cv.restore()


# ------------------------------------------------------------------ veredito (topo): a aposta MITO | VERDADE
def cartao_pose(t, T):
    tv = T["veredito"]
    if t < tv - 0.05:
        return None
    u = e_back(prog(t, tv - 0.05, tv + 0.35), 1.1)
    dy = lerp(-460, 0, u)
    sai = prog(t, T["um3"], T["um3"] + 0.35) ** 3                # sobe SEM recuo (não desce sobre a cena)
    return dy - 520 * sai, 1.0 if sai < 1 else 0.0


def roleta(T):
    """Tiques da roleta dourada: começa em MITO, alterna e DESACELERA; o 6º tique para em VERDADE."""
    t0, t1 = T["veredito"] + 0.3, T["verdade"] - 0.12
    return [lerp(t0, t1, (k / 5) ** 1.6) for k in range(6)]


def selecao(t, T):
    """-> (índice selecionado 0=MITO 1=VERDADE ou None, pulso 0-1 do último tique)."""
    tiques = roleta(T)
    if t < tiques[0]:
        return None, 0.0
    k = max(i for i, ti in enumerate(tiques) if ti <= t)
    return k % 2, 1 - clamp((t - tiques[k]) / 0.12)


def opcao(cv, s, x, a, sel, pulso, apagado):
    """Uma das duas opções da aposta: vazia (tracejada) ou selecionada pela roleta (dourada)."""
    if a <= 0:
        return
    esc = 1 + 0.07 * sel + 0.05 * pulso * sel
    cv.save(); cv.translate(x, SLOT_Y); cv.scale(esc, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-SLOT_W / 2, -SLOT_H / 2, SLOT_W / 2, SLOT_H / 2), 22, 22)
    if sel > 0:
        cv.drawRRect(rr, paint(OURO, int(110 * a * sel), blur=14))
    cv.drawRRect(rr, paint(lerpc("#EDE3D1", OURO, sel), int(255 * a * (1 - 0.5 * apagado))))
    if sel < 1:
        pt = paint(NAVY, int(130 * a * (1 - sel) * (1 - 0.6 * apagado)), "stroke", 4)
        pt.setPathEffect(skia.DashPathEffect.Make([16, 10], 0))
        cv.drawRRect(rr, pt)
    if sel > 0:
        cv.drawRRect(rr, paint(NAVY, int(255 * a * sel), "stroke", 5))
    texto(cv, s, 0, TAM_SLOT * 0.36, F_BLACK, TAM_SLOT, NAVY, int(a * lerp(165, 255, sel) * (1 - 0.65 * apagado)))
    cv.restore()


def cartao_veredito(cv, t, T, ep):
    ps = cartao_pose(t, T)
    if not ps:
        return
    dy, a = ps
    if a <= 0:
        return
    cv.save(); cv.translate(0, dy)
    x0, y0, x1, y1 = CARD
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 30, 30)
    sombra(cv, x0, y0 + 14, x1, y1 + 14, 30, 20, 150 / 255)
    cv.drawRRect(rr, paint(CARTAO))
    cv.drawRRect(rr, paint(NAVY, 255, "stroke", 6))
    g1, g2 = ep["gancho"]
    texto(cv, g1, CX, Q_Y[0], F_BLACK, TAM_Q, NAVY)
    texto(cv, g2, CX, Q_Y[1], F_BLACK, TAM_Q, NAVY)
    tv = T["verdade"]
    sel, pulso = selecao(t, T)
    bateu = t >= tv
    apaga = prog(t, tv, tv + 0.25)
    opcao(cv, R_MITO, SLOT_X["mito"], 1.0, 1.0 * (sel == 0 and not bateu), pulso, apaga)
    opcao(cv, R_VERDADE, SLOT_X["verdade"], 1.0, 1.0 * (sel == 1), pulso, 0.0)
    if bateu:
        k = t - tv
        marca_carimbo(cv, R_VERDADE, MARCA[0], MARCA[1], -4, 1.0, esc=lerp(1.25, 1.0, e_out(clamp(k / 0.12))))
    cv.restore()


def carimbo_pose(t, T):
    """-> (x, y, rot, esc, a, esmaga, larg): o carimbo só aparece no golpe — desce do alto à direita,
    bate em VERDADE na palavra e sobe em 0,16 s (não paira sobre o texto do cartão)."""
    tv = T["verdade"]
    t_in = tv - 0.18
    if t < t_in or t > tv + 0.2:
        return None
    larg = larg_marca()
    alvo = (MARCA[0], MARCA[1], -4.0)
    if t < tv:
        u = clamp((t - t_in) / 0.18) ** 2
        x, y, rot = lerp(1180, alvo[0], u), lerp(-300, alvo[1], u), lerp(24.0, alvo[2], u)
        return x, y, rot, 1.0, 1.0, 0.0, larg
    esmaga = math.sin(math.pi * clamp((t - tv) / 0.08))
    w = e_out(prog(t, tv + 0.04, tv + 0.2))
    x, y, rot = lerp(alvo[0], 1200, w), lerp(alvo[1], -420, w), lerp(alvo[2], 20.0, w)
    return x, y, rot, 1.0, 1.0, esmaga, larg


def impacto(cv, t, T):
    k = t - T["verdade"]
    if k < 0 or k > 0.35:
        return
    mx, my = MARCA
    u = e_out(k / 0.35); a = 1 - k / 0.35
    for i in range(12):
        ang = i * 2 * math.pi / 12 + 0.2
        r0, r1 = 190 + 50 * u, 215 + 95 * u
        ex, ey = math.cos(ang), math.sin(ang) * 0.42
        cv.drawLine(mx + r0 * ex, my + r0 * ey, mx + r1 * ex, my + r1 * ey, paint(OURO, int(230 * a), "stroke", 7))


def tremor_cam(t, T):
    k = t - T["verdade"]
    if 0 <= k < 0.35:
        return 10 * math.sin(k * 70) * (1 - k / 0.35)
    return 0.0


# ------------------------------------------------------------------ cartão dos sinais de infecção
def cartao_alarme(cv, t, T):
    """Cartão navy que SOBE da bancada em "Sinais de infecção" (recortado nela: nunca invade o
    karaokê); um pictograma por palavra, o da vez com anel dourado; sai no lugar (some e encolhe)."""
    t0 = t_alarme(T)
    k = prog(t, t0, t0 + 0.32)
    if k <= 0:
        return
    t_sai = T["manda"] - 0.55
    sai = e_inout(prog(t, t_sai, t_sai + 0.3))
    a = clamp(k * 2.5) * (1 - sai)
    if a <= 0:
        return
    dy = 520 * (1 - e_out(k))
    esc = 1 - 0.06 * sai
    x0, y0, x1, y1 = ALARME
    cv.save()
    cv.clipRRect(skia.RRect.MakeRectXY(skia.Rect(*BANC), 34, 34), skia.ClipOp.kIntersect, True)
    cv.translate(CX, 800); cv.scale(esc, esc); cv.translate(-CX, -800 + dy)
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 34, 34)
    sombra(cv, x0, y0, x1, y1, 34, 20, 120 * a / 255)
    cv.drawRRect(rr, paint(NAVY, int(252 * a)))
    cv.drawRRect(rr, paint(VERMELHO, int(255 * a), "stroke", 4))
    # cabeçalho: a ponte entre o teste e o alarme
    ph = 1 + 0.08 * pulo(t, T["infeccao"], 0.35)
    lw = larg_texto(R_INFEC, F_BLACK, 36)
    cv.save(); cv.translate(CX, 398); cv.scale(ph, ph)
    pill = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 28, -30, lw / 2 + 28, 30), 30, 30)
    cv.drawRRect(pill, paint(VERMELHO, int(255 * a)))
    cv.drawRRect(pill, paint("#FFFFFF", int(200 * a), "stroke", 3))
    texto(cv, R_INFEC, 0, 13, F_BLACK, 36, "#FFFFFF", int(255 * a))
    cv.restore()
    celulas = [(300, 560, T["pus"], T["pus"] + 0.6, ico_gota, (R_PUS,)),
               (780, 560, T["cheiro"], T["cheiro"] + 0.6, ico_cheiro, (R_CHEIRO,)),
               (300, 812, T["vermelhidao"], T["cresce"] + 0.5, ico_vermelhidao, (R_VERM1, R_VERM2)),
               (780, 812, T["dor"], T["dor"] + 0.6, ico_raio, (R_DOR,))]
    for n, (cx, cy, ti, tf, ico, rot) in enumerate(celulas):
        kp = prog(t, T["sinais"] + 0.06 + 0.13 * n, T["sinais"] + 0.32 + 0.13 * n)   # lugar vazio à espera
        p = prog(t, ti - 0.06, ti + 0.24)
        if kp > 0 and p < 1:
            ap = a * clamp(kp * 3) * (1 - clamp(p * 2))
            pt = paint("#FFFFFF", int(150 * ap), "stroke", 4)
            pt.setPathEffect(skia.DashPathEffect.Make([18, 12], t * 30))
            r = 92 * (e_back(kp) if kp < 1 else 1.0) * (1 + 0.04 * math.sin(t * 6 + n))
            cv.drawCircle(cx, cy - 30, max(1.0, r), pt)
        if p <= 0:
            continue
        ai = a * clamp(p * 2.5)
        esc_i = e_back(p) if p < 1 else 1.0
        vez = prog(t, ti - 0.06, ti + 0.08) * (1 - prog(t, tf, tf + 0.25))
        cv.drawCircle(cx, cy - 30, 92, paint("#FFFFFF", int((22 + 18 * vez) * ai)))
        cv.drawCircle(cx, cy - 30, 92, paint(lerpc("#FFFFFF", OURO, vez), int(lerp(90, 255, vez) * ai), "stroke",
                                             lerp(3, 6, vez)))
        cv.save(); cv.translate(cx, cy - 30); cv.scale(max(0.01, esc_i) * 1.25, max(0.01, esc_i) * 1.25)
        if ico is ico_vermelhidao:
            ico(cv, ai, t, p, cresce=e_inout(prog(t, T["cresce"], T["cresce"] + 0.5)))
        else:
            ico(cv, ai, t, p)
        cv.restore()
        for j, s in enumerate(rot):
            texto(cv, s, cx, cy + 108 + 44 * j, F_BLACK, 42, "#FFFFFF", int(255 * ai))
    cv.drawLine(110, 1000, 970, 1000, paint("#FFFFFF", int(50 * a), "stroke", 2))
    ka = prog(t, T["avise"] - 0.05, T["avise"] + 0.25)
    if ka > 0:
        aa = a * clamp(ka * 2.5); dx = 40 * (1 - e_out(ka))
        toque = prog(t, T["avise"] + 0.1, T["avise"] + 0.25) * (1 - prog(t, T["avise"] + 1.3, T["avise"] + 1.7))
        telefone(cv, 180 + dx, 1046, aa, toque, t, esc=1.0)
        texto(cv, R_AVISE, 250 + dx, 1076, F_BLACK, 56, "#FFFFFF", int(255 * aa), centro=False)
    kf = prog(t, T["febre"] - 0.05, T["febre"] + 0.25)
    if kf > 0:
        af = a * clamp(kf * 2.5); dx = 40 * (1 - e_out(kf))
        termometro(cv, 176 + dx, 1150, prog(t, T["febre"], T["febre"] + 0.8), af, esc=0.9)
        texto(cv, R_FEBRE, 250 + dx, 1162, F_BLACK, 52, OURO, int(255 * af), centro=False)
    cv.restore()


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep):
    fundo_rapido(cv, t)
    tremor = tremor_cam(t, T)
    cv.save(); cv.translate(tremor, 0)
    bancada(cv)
    psA, psB = pose("A", t, T), pose("B", t, T)
    cam = camera(t, T)
    luz = uv(t, T)
    rv = tempos_revela(T)
    tA = tinta_A(t, T)

    cv.save()
    cv.clipRRect(skia.RRect.MakeRectXY(skia.Rect(*BANC), 34, 34), skia.ClipOp.kIntersect, True)
    aplica_camera(cv, cam)
    # ---- colunas (B nasce de trás de A em "prova")
    for nome, ps in (("B", psB), ("A", psA)):
        if ps[3] <= 0:
            continue
        cv.save(); na_coluna(cv, ps)
        coluna(cv, t, T, nome)
        tinta_molhada(cv, t, T)
        marca_sujeira(cv, t, T, nome)
        brilhos(cv, *junc(0), t, T["invisivel"] + 0.1, n=7, raio=64, dur=0.6, raio0=30)
        if nome == "A":
            rastro_branco(cv, t, T)
            gx, gy, gr = gaze_A(t, T)
            eg = esc_gaze_capa(t, T)
            tg = t_gaze(T)
            gaze(cv, gx, gy, GW, GH, gr, 1.0, esc=eg + 0.1 * pulo(t, T["gaze4"], 0.3),
                 reflexo=prog(t, tg, tg + 0.6))               # a voz diz "Gaze limpa": reflexo de limpa
            brilho_limpa(cv, t, T, gx, gy, gr, eg)
        else:
            for (x, y, rot, a, esc) in gazes_B(t, T):
                gaze(cv, x, y, GW, GH, rot, a, esc=esc)
            ouro_B(cv, t, T)
        for i in range(3):                                         # "Parece limpo?": tudo brilha limpo
            brilhos(cv, *junc(i), t, T["parece"] + 0.1 * i, n=6, raio=60, dur=0.7, raio0=30)
        veu(cv, foco(t, T, nome))
        cv.restore()
    # ---- pincel (as duas colunas ao mesmo tempo, mesma condição)
    tt = T["tinta"]
    ent = e_out(prog(t, tt - 0.35, tt)); sai = e_in_back(prog(t, tt + 0.3, tt + 0.7))
    if ent > 0 and sai < 1:
        for ps in (psA, psB):
            cv.save(); na_coluna(cv, ps)
            jx, jy = junc(0)
            tx = jx + 14 + 260 * (1 - ent) + 260 * sai
            ty = jy - 4 - 300 * (1 - ent) - 340 * sai + 14 * math.sin(2 * math.pi * 2 * prog(t, tt, tt + 0.3))
            pincel(cv, tx, ty, 38, 1.0)
            cv.restore()
    cv.restore()                                                   # sai da câmera e do recorte

    if luz > 0:
        cv.save()
        cv.clipRRect(skia.RRect.MakeRectXY(skia.Rect(*BANC), 34, 34), skia.ClipOp.kIntersect, True)
        cv.drawRect(skia.Rect(*BANC), _blend(paint(UV_MULT, int(255 * 0.82 * luz)), skia.BlendMode.kMultiply))
        cv.save(); aplica_camera(cv, cam)                          # a pele recebe um tom bem mais leve
        for ps in (psB, psA):
            cv.save(); na_coluna(cv, ps)
            perna_sob_uv(cv, UV_PELE * luz)
            cv.restore()
        cv.restore()
        cv.drawRect(skia.Rect(*BANC), _blend(paint(UV_LUZ, 255, shader=skia.GradientShader.MakeLinear(
            [skia.Point(0, BANC[1]), skia.Point(0, BANC[3])], [C(UV_LUZ, int(110 * luz)), C(UV_LUZ, int(20 * luz))])),
            skia.BlendMode.kScreen))
        aplica_camera(cv, cam)
        cv.save(); na_coluna(cv, psA)
        t_on = T["veredito"] - 0.42

        def revela(chave):                                         # no pisca-pisca: vislumbre; aceso: um por um
            return 1.0 if t < t_on else prog(t, rv[chave], rv[chave] + 0.15)
        pul = pulo(t, T["carona"], 0.4) + 0.6 * pulo(t, T["pegou"], 0.3)
        brilho_pino(cv, 1, luz * tA["p2"] * revela("p2"), pul, t, rv["p2"])
        brilho_pino(cv, 2, luz * tA["p3"] * revela("p3"), pul, t, rv["p3"])
        gx, gy, gr = gaze_A(t, T)
        brilho_gaze(cv, gx, gy, gr, luz * tA["gaze"] * revela("gaze"), pulo(t, T["gaze4"], 0.35))
        k = t - rv["gaze"]
        if 0 <= k <= 0.55:
            cv.drawCircle(gx, gy, lerp(60, 200, e_out(k / 0.55)),
                          _blend(paint(NEON, int(230 * (1 - k / 0.55)), "stroke", 8), skia.BlendMode.kPlus))
        rastro_neon(cv, t, T)
        cv.restore()
        cv.restore()                                               # lado B: nada acende (é a prova)

    # ---- rótulos das condições (acima das colunas, fora do zoom; somem sob o cartão do veredito)
    some = 1 - prog(t, t_alarme(T) - 0.35, t_alarme(T) - 0.1)
    # v4: na VOLTA (depois do cartão e do zoom) os rótulos entram de novo com PULO de escala e opacidade
    # cheia — a v3 voltava por esmaecimento e, por ~5 quadros, o de B lia como etiqueta cinza vazia
    volta = prog(t, T["um3"] + 0.36, T["um3"] + 0.58)
    some *= 1 - prog(t, T["veredito"] - 0.12, T["veredito"]) * (1 - clamp(volta * 5))
    esc_volta = max(0.01, e_back(volta)) if 0 < volta < 1 else (0.01 if t >= T["veredito"] and volta <= 0 else 1.0)
    pA, pB = prog(t, T["de"] - 0.05, T["de"] + 0.25), prog(t, T["do"] - 0.05, T["do"] + 0.25)
    aA = clamp(pA * 5) * some
    aB = clamp(pB * 5) * some * (1 - (cam[0] - 1) / (ZOOM - 1))  # no zoom em A, o rótulo de B sai
    rotulo(cv, R_A, CA, 418, aA, esc=(max(0.01, e_back(pA)) if pA < 1 else 1.0) * esc_volta)
    rotulo(cv, R_B, CB, 418, aB, ouro=prog(t, T["material"], T["material"] + 0.25),
           esc=((max(0.01, e_back(pB)) if pB < 1 else 1.0) + 0.06 * pulo(t, T["material"], 0.35)) * esc_volta)
    tag_fixador(cv, t, T, psA)
    # chip "PEGOU CARONA" (cor da tinta na luz negra; sem ouro, sem estrelas)
    kc = prog(t, T["carona"] - 0.05, T["carona"] + 0.3)
    ac = clamp(kc * 3) * (1 - prog(t, T["um3"] - 0.1, T["um3"] + 0.15))
    if ac > 0:
        chip(cv, R_CARONA, 320, 560, ac, max(0.01, e_back(kc)))
    # lâmpada de luz negra (desce em "luz", sobe em "Um" acelerando, SEM recuo sobre os rótulos)
    ky = e_out(prog(t, T["luz"] - 0.05, T["luz"] + 0.3)) * (1 - prog(t, T["um3"] - 0.1, T["um3"] + 0.3) ** 2)
    if ky > 0:
        lampada(cv, 190, 890, lerp(-60, 352, ky), luz, 1.0)
    cartao_alarme(cv, t, T)
    vcta = 0.86 * prog(t, T["manda"] - 0.55, T["manda"] - 0.25)   # véu navy: a CTA fica sobre fundo escuro
    if vcta > 0:
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(*BANC), 34, 34), paint(NAVY, int(255 * vcta)))
    cv.restore()

    # ---- topo: gancho (capa), claquete, selo (a aposta), cartão do veredito e carimbo
    capa(cv, t, T["vamos"], *ep["gancho"])
    kq = t - T["prova"]
    if -0.35 < kq < 1.25:
        aq = prog(t, T["prova"] - 0.35, T["prova"] - 0.2) * (1 - prog(t, T["prova"] + 1.0, T["prova"] + 1.25))
        fecha = e_in_back(prog(t, T["prova"] - 0.3, T["prova"]))
        dx = -300 * (1 - e_out(prog(t, T["prova"] - 0.35, T["prova"] - 0.15))) - 320 * e_in_back(prog(t, T["prova"] + 0.95, T["prova"] + 1.25))
        claquete(cv, 48 + dx, 196, fecha, aq)
    ps0 = prog(t, T["prova"] + 0.15, T["prova"] + 0.5)
    a0 = clamp(ps0 * 4) * (1 - prog(t, T["manda"] - 0.3, T["manda"]))
    a0 *= 1 - prog(t, T["veredito"] - 0.1, T["veredito"] + 0.1) * (1 - prog(t, T["um3"] + 0.2, T["um3"] + 0.45))
    selo_serie(cv, t, a0, esc=max(0.01, e_back(ps0)) if ps0 < 1 else 1.0,
               flash=prog(t, T["prova"] + 0.3, T["prova"] + 0.45) * (1 - prog(t, T["prova"] + 0.9, T["prova"] + 1.4)))
    cv.save(); cv.translate(tremor, 0)
    cartao_veredito(cv, t, T, ep)
    impacto(cv, t, T)
    cp = carimbo_pose(t, T)
    if cp:
        x, y, rot, s, a, esm, larg = cp
        carimbo_obj(cv, x, y, rot, s, a, esm, larg=larg)
    cv.restore()

    interface(cv, t, T, blocos, DESTAQUE)


# ------------------------------------------------------------------ sons
def sons(T):
    ev = [(T["fixador"] + 0.02, "click", 0.55), (T["fixador"] + 0.05, "pop", 0.3)]
    ev += [(T["tres"], "pop", 0.45), (T["tres"] + 0.16, "pop", 0.45), (T["pinos"] + 0.06, "pop", 0.45)]
    ev += [(T["pinos"] + 0.1 * i, "click", 0.4) for i in range(3)]
    ev += [(t_gaze(T) + 0.02, "ping", 0.35), (t_gaze(T) + 0.15, "shimmer", 0.3)]
    ev += [(T["vamos"], "whoosh", 0.25), (T["prova"] - 0.01, "tick", 0.35), (T["prova"] + 0.03, "whoosh", 0.3)]
    ev += [(T["pino"], "pop", 0.35), (T["tinta"] - 0.3, "whoosh", 0.25), (T["tinta"] + 0.05, "click", 0.35),
           (T["tinta"] + 0.2, "click", 0.35), (T["invisivel"] + 0.08, "shimmer", 0.45), (T["sujeira"], "ping", 0.35)]
    for i, (ch, fim) in enumerate(janelas_A(T)):
        ev += [(ch - 0.25, "whoosh", 0.22), (ch + 0.06, "click", 0.45), (ch + 0.2, "click", 0.4)]
    ev += [(janelas_A(T)[2][1] + 0.05, "whoosh", 0.2)]
    (c1, f1), (c2, f2), (c3, f3) = janelas_B(T)
    ev += [(c1 - 0.22, "whoosh", 0.22), (c1 + 0.06, "click", 0.45), (c1 + 0.2, "click", 0.4), (f1, "whoosh", 0.3)]
    ev += [(c2 - 0.2, "pop", 0.45), (c2 + 0.08, "click", 0.4), (c3 - 0.2, "pop", 0.45), (c3 + 0.08, "click", 0.4)]
    ev += [(T["parece"] + 0.05, "shimmer", 0.4)]
    ev += [(T["luz"], "whoosh", 0.3), (T["luz"] + 0.28, "click", 0.6)]
    tn = T["negra"] + 0.12
    ev += [(tn + a0, "tick", 0.28) for a0 in (0.0, 0.2, 0.42, 0.62)]
    rv = tempos_revela(T)
    ev += [(T["veredito"] - 0.42, "thump", 0.3), (T["veredito"] - 0.42, "shimmer", 0.5)]
    ev += [(rv["p2"], "ping", 0.45), (rv["p3"], "ping", 0.45), (rv["gaze"], "ding", 0.6)]
    ev += [(T["veredito"], "whoosh", 0.3)]
    for i, ti in enumerate(roleta(T)):                            # roleta: um tique por troca, desacelerando
        ev.append((ti, "tick", lerp(0.18, 0.32, i / 5)))
    ev += [(T["verdade"] - 0.17, "whoosh", 0.3), (T["verdade"], "thump", 0.4), (T["verdade"] + 0.02, "crackle", 0.4)]
    ev += [(T["sujeira2"], "whoosh", 0.3), (T["sujeira2"] + 0.05, "shimmer", 0.3), (T["carona"], "pop", 0.6),
           (T["gaze4"], "ping", 0.3)]
    ev += [(T["um3"], "click", 0.5), (T["um3"] + 0.05, "whoosh", 0.3), (T["material"], "shimmer", 0.25)]
    ev += [(T["cada"] + 0.12 * i, "ping", 0.3) for i in range(3)]
    ev += [(t_alarme(T), "whoosh", 0.3), (T["infeccao"], "click", 0.4)]
    ev += [(T["sinais"] + 0.06 + 0.13 * n, "tick", 0.16) for n in range(4)]     # os 4 lugares vazios
    ev += [(T[k], "pop", 0.45) for k in ("pus", "cheiro", "vermelhidao", "dor")]
    ev += [(T["cresce"], "tick", 0.15), (T["avise"], "pop", 0.55), (T["febre"], "pop", 0.55),
           (T["manda"] - 0.5, "whoosh", 0.25), (T["manda"] + 0.05, "whoosh", 0.3)]
    return ev


def tempos_previa(T):
    rv = tempos_revela(T)
    return (0.0, t_gaze(T) + 0.3, T["fixador"] + 0.2, T["tres"] + 0.4, T["prova"] - 0.02, T["prova"] + 0.6, T["tinta"] + 0.1,
            T["invisivel"] + 0.2, T["sujeira"] + 0.3, T["lado"] + 0.2, T["gaze2"] + 0.15, T["tres2"] + 0.4,
            T["outro"] + 0.2, T["gaze3"] + 0.05, T["pino2"] + 0.15, T["parece"] + 0.3, T["luz"] + 0.3,
            T["negra"] + 0.2, rv["p2"] + 0.1, rv["gaze"] + 0.3, roleta(T)[2] + 0.02, T["verdade"] - 0.05,
            T["verdade"] + 0.03, T["verdade"] + 0.4, T["carona"] + 0.3, T["material"] + 0.2, T["cada"] + 0.4,
            T["sinais"] + 0.3, T["pus"] + 0.2, T["vermelhidao"] + 0.5,
            T["dor"] + 0.3, T["avise"] + 0.4, T["febre"] + 0.7, T["manda"] - 0.3, T["manda"] + 1.6)


# ------------------------------------------------------------------ render local (pausa da luz negra)
_PONTA = re.compile(r"[.,:;!?—…]+$")
PAUSA_LUZ = 0.60
PAUSA_VEREDITO = 0.25                              # a roleta MITO | VERDADE respira antes do golpe
GANHO_TRILHA, GANHO_ALARME = 0.40, 0.15
LIM_FX = 0.6


def inserir_pausa(voz, pal, palavra, pausa):
    """Insere `pausa` s de silêncio logo depois de `palavra` (fim + 0,05 s) e empurra as seguintes."""
    i = next(k for k, p in enumerate(pal) if p["w"].lower() == palavra)
    t_ins = pal[i]["t"] + pal[i]["d"] + 0.05
    pos = int(t_ins * som.SR)
    nova = np.concatenate([voz[:pos], np.zeros(int(pausa * som.SR), dtype=voz.dtype), voz[pos:]])
    return nova, [dict(p, t=p["t"] + (pausa if p["t"] > t_ins else 0.0)) for p in pal]


def _media_movel(x, m):
    """O mesmo que np.convolve(x, np.ones(m) / m, "same") (o que som.mixar usa), por soma acumulada."""
    n = len(x)
    c = np.concatenate([[0.0], np.cumsum(x, dtype=np.float64)])
    k = np.arange(n) + (m - 1) // 2
    hi = np.minimum(k + 1, n); lo = np.maximum(k - m + 1, 0)
    return (c[hi] - c[lo]) / m


def mixar(voz, dur, eventos, ganho_trilha, baixa):
    """Cópia de som.mixar (som.py não se edita) com um envelope extra na trilha: de baixa[0] a
    baixa[1] ela desce para baixa[2] (sinais de alarme sóbrios)."""
    SR = som.SR
    n = int(dur * SR)
    v = np.zeros(n); v[:min(n, len(voz))] = voz[:n]
    musica = som.trilha(dur) * ganho_trilha
    t0, t1, g = baixa
    tt = np.arange(n) / SR
    musica = musica * (1 - (1 - g) * np.clip((tt - t0) / 0.4, 0, 1) * np.clip((t1 - tt) / 0.4, 0, 1))
    win = int(0.06 * SR)
    envv = np.sqrt(np.maximum(_media_movel(v ** 2, win), 0.0))
    alvo = np.where(envv > 0.02, 0.38, 1.0)
    duck = _media_movel(alvo, int(0.25 * SR))
    fx = np.zeros(n)
    for t_ev, nome, ganho in eventos:
        s = som.SFX[nome]()
        p = int(t_ev * SR)
        if 0 <= p < n:
            m = min(len(s), n - p)
            fx[p:p + m] += s[:m] * ganho
    fx = LIM_FX * np.tanh(fx / LIM_FX)                  # limitador suave: efeito nunca passa do pico da voz
    mix = v * 1.0 + musica * duck + fx * 0.7
    pico = np.max(np.abs(mix)) or 1.0
    return mix / pico * 0.89


def preparar(ep, tmp, respiro_cta=0.5):
    """Voz -> palavras limpas -> corte de silêncio -> alinhamento -> pausa da luz negra -> âncoras."""
    roteiro = "\n".join(ep["roteiro"])
    voz_bruta, palavras = _voz.narrar(roteiro, _voz.RITMO_COMO_FUNCIONA, os.path.join(tmp, "voz"))
    palavras = [dict(p, w=_PONTA.sub("", p["w"])) for p in palavras]
    voz_c, pal, tirado = comprimir(voz_bruta, palavras, respiro_cta=respiro_cta)
    pal = alinhar(pal, roteiro)
    voz_c, pal = inserir_pausa(voz_c, pal, "negra", PAUSA_LUZ)
    voz_c, pal = inserir_pausa(voz_c, pal, "veredito", PAUSA_VEREDITO)
    T = ancoras(pal, ANCORAS)
    return voz_c, pal, T, tirado


def fazer_render_luz(quadro_fn, sons_fn, tempos_fn, respiro_cta=0.5):
    """Os passos de cf_fixador_circular.fazer_render_tolerante + a pausa da luz negra + trilha baixa."""
    def render(ep, mp4, tmp, previa=False):
        voz_c, pal, T, tirado = preparar(ep, tmp, respiro_cta)
        print(f"{ep['id']}: silêncio cortado {tirado:.2f}s | pausas luz negra {PAUSA_LUZ:.2f}s + veredito {PAUSA_VEREDITO:.2f}s | "
              f"duração final {T['total']:.2f}s")
        blocos = montar_blocos(pal)

        def quadro_t(cv, t):
            quadro_fn(cv, t, T, blocos, ep)

        if previa:
            return _previas(quadro_t, tempos_fn(T), tmp, ep["id"]), T["total"]
        wav = os.path.join(tmp, f"{ep['id']}_mix.wav")
        baixa = (t_alarme(T) - 0.3, T["manda"] - 0.1, GANHO_ALARME / GANHO_TRILHA)
        som.gravar_wav(wav, mixar(voz_c, T["total"], sons_fn(T), GANHO_TRILHA, baixa))
        codificar(quadro_t, T["total"], wav, mp4)
        return mp4, T["total"]
    return render


render = fazer_render_luz(quadro, sons, tempos_previa, respiro_cta=0.5)
