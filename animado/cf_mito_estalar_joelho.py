# -*- coding: utf-8 -*-
"""MITO NA PROVA — "JOELHO ESTALANDO / FAZ MAL?" (cf_mito_estalar_joelho, série do piloto cf_mitonaprova_pinos).

Mesma mecânica do piloto aprovado: a crença em pergunta de sim/não no quadro 0; UM objeto grande (uma
criança de desenho, de perfil, AGACHADA para pegar uma bola, com o "crec" desenhado POR FORA do joelho)
que se CLONA em "prova" (teste justo: as duas colunas são idênticas, só muda o estalo); selo "MITO OU
VERDADE?"; "um joelho que NÃO estala": só B agacha, em silêncio; o teste roda à vista e EMPURRA a aposta
para VERDADE (agacham juntas, crec, crec, crec, cada estrela MAIOR em A); a virada ("os dois correm e
pulam"): a bola do quadro 0 VOLTA rolando nas duas colunas e as duas pulam POR CIMA dela ao mesmo tempo,
joelho esticado no ar (o desfecho concreto: brincam igual); cartão do veredito com a pergunta + MITO |
VERDADE, roleta que segura em VERDADE e cai em MITO na palavra; carimbo bate e sai; o porquê (SEM DOR);
o jeito que vale (O SINTOMA GUIA / NÃO O BARULHO); o asterisco sóbrio (cartão escuro de borda ÂMBAR, um
pictograma por sinal, nunca desenhado na criança); CTA.

v2 (leitor às cegas + revisor): proporção de CRIANÇA (cabeça ~1/5 da altura, pernas curtas) e gancho
"JOELHO DO FILHO"; agacha EM "Agacha"; sem o crec sobre "não estala"; sem as 3 estrelinhas do acúmulo
(símbolo abstrato) e sem o contorno dourado da virada (trocado pela bola); cartão do asterisco só entra
depois que o da regra saiu, com a criança coberta; chip SEM DOR na altura do joelho.

Fonte de verdade: lab/formato_novo/cf_mito_estalar_joelho/storyboard.json (tempos MEDIDOS da voz).

Regras de desenho (storyboard, regras_visuais):
  * Criança de desenho: cabeça lisa sem rosto (o cabelo mostra a direção), pele lisa e OPACA, camiseta
    verde-água, bermuda grafite, meia e tênis brancos. Nenhum osso, nada translúcido, nada POR DENTRO do
    joelho (sem tendão, bolha, cartilagem, lupa ou fundo de exame). O crec é uma estrela de estalo POR
    FORA, sem letras; som seco e suave (dois cliques), nunca grave.
  * Vermelho só no carimbo MITO e no ponto do selo. Nenhuma estrela de dor, joelho inchado, travado ou mão
    no joelho desenhados numa criança: os 4 sinais são PICTOGRAMAS de traço no cartão do asterisco.
  * Sem régua, número, medidor ou "nível de desgaste": o "acúmulo" é só o crec que cresce (80→100→120).
  * Todo texto desenhado está em ep["tela"] (ou é o gancho / a interface comum). Cena acima de y≈1226.
Nenhum arquivo existente de animado/ foi editado: os helpers vêm COPIADOS do cf_mitonaprova_pinos (fundo,
bancada, claquete, selo, roleta, carimbo, cartões, ícone de raio, pausa e mixagem) e do
cf_chamaovar_rotina_fixador (capsula, pinta, ik2, canela, cabeça, mão), adaptados a uma criança.

Render: passos do piloto (pontuação limpa, corte de silêncio com respiro 0,5 s antes da CTA) + 0,50 s de
silêncio logo depois de "Veredito:" (a roleta) + trilha baixa no asterisco (cópia local de som.mixar, que
também conhece o "crec" sintetizado aqui: dois cliques defasados 12 ms + um tique leve).
A cena é PRESA ao roteiro pelas palavras-âncora (ANCORAS): roteiro sem elas = KeyError.
"""
import math
import os
import re

import numpy as np
import skia

from . import som, voz as _voz
from .base import codificar, previas as _previas
from .cf_alongamento import (BG_IN, BG_OUT, CX, F_BLACK, H, OURO, PART, PELE, VERMELHO, W, C, clamp, e_back,
                             e_in_back, e_inout, e_out, larg_texto, lerp, lerpc, paint, prog, texto)
from .cf_comum import alinhar, ancoras, capa, comprimir, interface, montar_blocos

# ------------------------------------------------------------------ sincronia com a fala
# prefixo SEMPRE False: "agacha" com prefixo casaria "agachou"; "estala" ≠ "estalo"
ANCORAS = {
    "agachou": ("agachou", 1, False), "joelho": ("joelho", 1, False), "crec": ("crec", 1, False),
    "vamos": ("vamos", 1, False), "prova": ("prova", 1, False),
    "outro": ("outro", 1, False), "lado": ("lado", 1, False), "joelho2": ("joelho", 2, False),
    "estala": ("estala", 1, False),
    "agacha": ("agacha", 1, False), "novo": ("novo", 1, False),
    "crec2": ("crec", 2, False), "crec3": ("crec", 3, False), "crec4": ("crec", 4, False),
    "agora": ("agora", 1, False), "dois": ("dois", 1, False), "correm": ("correm", 1, False),
    "pulam": ("pulam", 1, False),
    "veredito": ("veredito", 1, False), "mito": ("mito", 1, False),
    "estalo": ("estalo", 1, False), "joelho3": ("joelho", 3, False), "sem": ("sem", 1, False),
    "dor": ("dor", 1, False), "inofensivo": ("inofensivo", 1, False),
    "sintoma": ("sintoma", 1, False), "barulho": ("barulho", 1, False),
    "mas": ("mas", 1, False), "joelho4": ("joelho", 4, False), "doi": ("dói", 1, False),
    "incha": ("incha", 1, False), "trava": ("trava", 1, False), "falseia": ("falseia", 1, False),
    "avaliacao": ("avaliação", 1, False), "manda": ("manda", 1, False),
}
# "mito" fica FORA: o karaokê o pinta de ouro só enquanto é dito, sem brigar com o vermelho do carimbo
DESTAQUE = {"crec", "estala", "pulam", "inofensivo", "sintoma", "barulho", "dói", "incha", "trava", "falseia",
            "avaliação", "assusta"}

# ------------------------------------------------------------------ textos de tela (todos em ep["tela"])
R_TESTE = "TESTE"
R_SELO = "MITO OU VERDADE?"
R_A, R_B = "ESTALA", "NÃO ESTALA"
R_MITO, R_VERDADE = "MITO", "VERDADE"
R_SEMDOR = "SEM DOR"
R_GUIA, R_BARULHO = "O SINTOMA GUIA", "NÃO O BARULHO"
R_ALERTA = "O QUE LIGA O ALERTA"
R_DOI, R_INCHA, R_TRAVA, R_FALSEIA = "DÓI", "INCHA", "TRAVA", "FALSEIA"
R_AVALIA = "MERECE AVALIAÇÃO"

# ------------------------------------------------------------------ paleta
NAVY = "#0B1824"
BANCADA, BANCADA_BORDA = "#F3EADB", "#D6C6AA"
PAINEL, PAINEL_BORDA = "#EADDC6", "#D2C09F"
CHAO, CHAO_LINHA, CHAO_TRACO = "#E3D3B6", "#CDB993", "#D2BF9C"
CARTAO = "#FBF6EC"
AMBAR = "#FFB547"
MADEIRA, MADEIRA_CL, MADEIRA_ESC = "#B9844D", "#D9A86E", "#7B5129"
BORRACHA, BORRACHA_ESC, BORRACHA_CL = "#9A3F33", "#4E1A14", "#C0675A"
# criança: camiseta verde-água, bermuda grafite, meia e tênis brancos (≠ mochila e ≠ câmera lenta)
PELE_CL, PELE_ESC, PELE_LINHA = "#F7CDB8", "#D9937A", "#B9765E"
CAMISA, CAMISA_CL, CAMISA_ESC = "#4DBFAE", "#7FD8CA", "#33907F"
BERM, BERM_CL, BERM_ESC = "#4B5563", "#677182", "#353C48"
MEIA, MEIA_ESC = "#F6F8FA", "#C9D2DC"
TENIS, TENIS_ESC, SOLA = "#FBFCFD", "#CBD4DE", "#B8C2CD"
CABELO = "#3B2A20"
BOLA, BOLA_CL, BOLA_ESC = "#3E7BD6", "#8DB6F0", "#24508F"

TONS_PELE = (PELE_ESC, PELE, PELE_CL, PELE, PELE_ESC)
TONS_CAMISA = (CAMISA_ESC, CAMISA, CAMISA_CL, CAMISA, CAMISA_ESC)
TONS_BERM = (BERM_ESC, BERM, BERM_CL, BERM, BERM_ESC)
TONS_MEIA = (MEIA_ESC, MEIA, "#FFFFFF", MEIA, MEIA_ESC)

# ------------------------------------------------------------------ geometria (1080 x 1920)
BANC = (24, 340, 1056, 1226)                      # bancada creme: a cena fica acima de y≈1226
PISO_Y = 1186                                     # onde a sola encosta (todas as vistas)
S0, X0 = 1.62, 452                                # quadro 0: UMA criança grande (x = tornozelo)
S1 = 0.80                                         # nas colunas: ~575 px em pé
XC = 560                                          # a criança sozinha, já no tamanho das colunas
XA, XB = 215, 725                                 # tornozelos nas colunas A e B
XM = 470                                          # cenas 7-8: A no centro (a estrela fica à direita)
PAINEL_A, PAINEL_B = (40, 450, 530, 1214), (550, 450, 1040, 1214)
ROT_Y = 406                                       # centro dos rótulos ESTALA / NÃO ESTALA
CARD = (100, 148, 980, 440)                       # cartão do veredito: abaixo do cabeçalho do Instagram
Q_Y = (223, 293)
TAM_Q = 62
SLOT_Y, SLOT_H, SLOT_W = 368, 80, 314
SLOT_X = {"mito": 361, "verdade": 719}
TAM_SLOT = 50
MARCA = (SLOT_X["mito"], SLOT_Y)                  # onde o carimbo bate
TAM_MARCA = 58
REGRA = (150, 356, 930, 544)                      # cartão "O SINTOMA GUIA / NÃO O BARULHO"
ALERTA = (60, 354, 1020, 1212)                    # cartão do asterisco (dentro da bancada)

# esqueleto da criança (unidades = px na escala 1). Proporção de CRIANÇA de ~7 anos (cabeça ≈ 1/5 da
# altura, pernas curtas, tronco atarracado): na v1 (cabeça 1/7) o leitor às cegas viu um adolescente.
L1 = L2 = 168.0                                   # coxa e canela
ANK_H = 30.0                                      # tornozelo acima do chão
TRONCO, PESC, HR = 186.0, 26.0, 74.0
BRACO, ANTEB = 102.0, 96.0
HIP_PE = (-6.0, -(ANK_H + L1 + L2 - 6))           # em pé
HIP_AG = (-93.0, -152.0)                          # agachamento fundo (calcanhar no chão)
ANK_N, ANK_F = (8.0, -ANK_H), (-6.0, -ANK_H)      # tornozelos no chão (perto / longe)
BOLA_C, BOLA_R = (112.0, -42.0), 42.0             # a bola no quadro 0 (entre os pés, à frente)
J_MAX = 190.0                                     # altura do pulo (≈ 150 px nas colunas): a bola passa por baixo
TENIS_K = 0.88                                    # o tênis acompanha o pé menor
PE_AR = 14.0                                      # ponta do pé no ar (graus): pouca, para a bola passar
PE_X = 58.0                                       # centro do pé no ar, à frente do tornozelo (unidades)
V_BOLA = 780.0                                    # px/s: a bola que VOLTA rolando na virada
R_BOLA_V = 50.0                                   # raio dela nas colunas (unidades): legível a 360 px


# ------------------------------------------------------------------ utilidades (cópias do cf_chamaovar_rotina_fixador)
def _c(h, a=255):
    h = h.lstrip("#")
    return skia.ColorSetARGB(int(a), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def esc_cor(h, k):
    return lerpc(h, "#000000", k)


def tons_escuros(tons, k):
    return tuple(esc_cor(c, k) for c in tons)


def uniao(*ps):
    out = ps[0]
    for q in ps[1:]:
        out = skia.Op(out, q, skia.PathOp.kUnion_PathOp) or out
    return out


def poli(pts, fechar=True):
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if fechar:
        p.close()
    return p


def capsula(p0, p1, w0, w1):
    """Tubo afinando de p0 (largura w0) a p1 (w1), pontas redondas."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]; L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    p = poli([(p0[0] + nx * w0 / 2, p0[1] + ny * w0 / 2), (p1[0] + nx * w1 / 2, p1[1] + ny * w1 / 2),
              (p1[0] - nx * w1 / 2, p1[1] - ny * w1 / 2), (p0[0] - nx * w0 / 2, p0[1] - ny * w0 / 2)])
    c0 = skia.Path(); c0.addCircle(p0[0], p0[1], w0 / 2)
    c1 = skia.Path(); c1.addCircle(p1[0], p1[1], w1 / 2)
    return uniao(p, c0, c1)


def pinta(cv, path, p0, p1, w, tons, a, linha=None, larg_linha=2.5):
    """Preenche com sombreado cilíndrico perpendicular ao eixo p0->p1 (pele/roupa chapada e opaca)."""
    if a <= 0:
        return
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]; L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    g0 = skia.Point(mx - nx * w * 0.62, my - ny * w * 0.62); g1 = skia.Point(mx + nx * w * 0.62, my + ny * w * 0.62)
    sh = skia.GradientShader.MakeLinear([g0, g1], [_c(c) for c in tons], [0.0, 0.2, 0.48, 0.8, 1.0])
    cv.drawPath(path, paint(tons[1], int(255 * a), shader=sh))
    if linha:
        cv.drawPath(path, paint(linha, int(200 * a), "stroke", larg_linha))


def ik2(a, b, L1_, L2_, lado):
    """Cinemática inversa de 2 ossos: junta do meio e ponta efetivamente alcançada.
    lado = +1 dobra a junta para a frente (joelho de quem olha para a direita), -1 para trás (cotovelo)."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    D = clamp(math.hypot(dx, dy), abs(L1_ - L2_) + 1.0, L1_ + L2_ - 0.5)
    cos_a = clamp((L1_ * L1_ + D * D - L2_ * L2_) / (2 * L1_ * D), -1.0, 1.0)
    ang = math.atan2(dy, dx) - lado * math.acos(cos_a)
    j = (a[0] + L1_ * math.cos(ang), a[1] + L1_ * math.sin(ang))
    ang2 = math.atan2(b[1] - j[1], b[0] - j[0])
    return j, (j[0] + L2_ * math.cos(ang2), j[1] + L2_ * math.sin(ang2))


def lerp2(p, q, k):
    return (lerp(p[0], q[0], k), lerp(p[1], q[1], k))


def soma(p, q, k=1.0):
    return (p[0] + q[0] * k, p[1] + q[1] * k)


def norm(v):
    L = math.hypot(v[0], v[1]) or 1.0
    return (v[0] / L, v[1] / L)


def chaves(t, ks):
    """Interpolação suave entre (tempo, valor) ordenados; constante fora do intervalo."""
    if t <= ks[0][0]:
        return ks[0][1]
    for (t0, v0), (t1, v1) in zip(ks, ks[1:]):
        if t <= t1:
            return lerp(v0, v1, e_inout(prog(t, t0, t1))) if t1 > t0 else v1
    return ks[-1][1]


def pulo(t, t0, dur=0.32, alt=1.0):
    k = t - t0
    if k < 0 or k > dur:
        return 0.0
    return alt * math.sin(math.pi * k / dur)


def _blend(p, modo):
    p.setBlendMode(modo)
    return p


# ------------------------------------------------------------------ fundo e bancada (cópias do piloto)
_CACHE = {}


def fundo_rapido(cv, t):
    """O fundo do cf_alongamento (mesmo gradiente radial, mesmo centro que oscila, mesmas partículas),
    com o gradiente pronto numa imagem e copiado 1:1."""
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
        x0, y0, x1, y1 = BANC
        rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 34, 34)
        c.drawRRect(rr, paint("#000000", 120, blur=24))
        c.drawRRect(rr, paint(BANCADA, 255, shader=skia.GradientShader.MakeLinear(
            [skia.Point(0, y0), skia.Point(0, y1)], [C("#F7F0E3"), C(BANCADA), C("#EDE2CF")])))
        c.save(); c.clipRRect(rr, skia.ClipOp.kIntersect, True)
        c.drawRect(skia.Rect(x0, PISO_Y, x1, y1), paint(CHAO))          # o chão (faixa de baixo)
        c.drawLine(x0, PISO_Y, x1, PISO_Y, paint(CHAO_LINHA, 255, "stroke", 3))
        c.restore()
        c.drawRRect(rr, paint(BANCADA_BORDA, 255, "stroke", 3))
        _CACHE["banc"] = sf.makeImageSnapshot()
    cv.drawImage(_CACHE["banc"], 0, 0)


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


def paineis(cv, t, T):
    """As duas colunas do teste (mesmo chão, mesma moldura): entram no clone, saem em "Estalo"."""
    a = prog(t, T["prova"] - 0.05, T["prova"] + 0.4) * (1 - prog(t, T["estalo"], T["estalo"] + 0.4))
    if a <= 0:
        return
    for (x0, y0, x1, y1) in (PAINEL_A, PAINEL_B):
        rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 26, 26)
        cv.drawRRect(rr, paint(PAINEL, int(150 * a)))
        cv.drawRRect(rr, paint(PAINEL_BORDA, int(255 * a), "stroke", 3))


def chao_correndo(cv, t, T, x0, x1, k):
    """Tracinhos do chão correndo para trás durante a corrida no lugar (dentro da coluna)."""
    if k <= 0:
        return
    cv.save(); cv.clipRect(skia.Rect(x0 + 6, PISO_Y + 4, x1 - 6, BANC[3] - 4))
    off = (t - T["correm"]) * 900 % 70
    x = x0 - off
    while x < x1 + 70:
        cv.drawLine(x, PISO_Y + 20, x + 34, PISO_Y + 20, paint(CHAO_LINHA, int(255 * k), "stroke", 5))
        x += 70
    cv.restore()


# ------------------------------------------------------------------ a criança (de perfil, olhando para a direita)
def canela_path(knee, ank, k=0.86):
    """Canela de perfil (cópia adaptada do cf_chamaovar): frente quase reta, panturrilha abaulada atrás."""
    dx, dy = ank[0] - knee[0], ank[1] - knee[1]; L = math.hypot(dx, dy) or 1.0
    d = (dx / L, dy / L); f = (d[1], -d[0])
    fr, tr = [], []
    for i in range(15):
        s = i / 14
        wf = lerp(29, 19, s) * k
        wb = (30 + 15 * math.sin(math.pi * clamp(s / 0.7)) ** 1.3 - 9 * s) * k
        c = (knee[0] + d[0] * L * s, knee[1] + d[1] * L * s)
        fr.append((c[0] + f[0] * wf, c[1] + f[1] * wf)); tr.append((c[0] - f[0] * wb, c[1] - f[1] * wb))
    p = poli(fr + tr[::-1])
    kk = skia.Path(); kk.addCircle(knee[0], knee[1], 29 * k)
    aa = skia.Path(); aa.addCircle(ank[0], ank[1], 19 * k)
    return uniao(p, kk, aa)


def _tenis_path():
    """Tênis de perfil (tornozelo na origem, sola em y = +34 com o pé chapado)."""
    p = skia.Path()
    p.moveTo(-26, -10)
    p.cubicTo(-38, 0, -40, 24, -32, 34)
    p.lineTo(104, 34)
    p.cubicTo(126, 34, 128, 14, 110, 6)
    p.cubicTo(84, -2, 56, -6, 34, -14)
    p.cubicTo(24, -20, 14, -22, 6, -20)
    p.close()
    return p


TENIS_P = _tenis_path()


def tenis(cv, ank, ang, esc_k, a):
    """Tênis branco com sola cinza; `ang` (graus): ponta para baixo (pé esticado no ar)."""
    cv.save(); cv.translate(ank[0], ank[1]); cv.rotate(ang); cv.scale(TENIS_K, TENIS_K)
    cv.drawPath(TENIS_P, paint(TENIS, int(255 * a), shader=skia.GradientShader.MakeLinear(
        [skia.Point(0, -20), skia.Point(0, 34)], [_c(esc_cor("#FFFFFF", esc_k)), _c(esc_cor(TENIS, esc_k)),
                                                   _c(esc_cor(TENIS_ESC, esc_k))], [0.0, 0.6, 1.0])))
    cv.save(); cv.clipPath(TENIS_P, skia.ClipOp.kIntersect, True)
    cv.drawRect(skia.Rect(-50, 25, 140, 40), paint(esc_cor(SOLA, esc_k), int(255 * a)))
    cv.restore()
    cv.drawPath(TENIS_P, paint(esc_cor("#8796A6", esc_k), int(255 * a), "stroke", 2.6))
    for i in range(3):                                         # cadarço (três traços)
        x = 24 + 15 * i
        cv.drawLine(x, -10 + 3 * i, x + 8, -2 + 3 * i, paint(esc_cor("#9AA8B6", esc_k), int(230 * a), "stroke", 3))
    cv.restore()


def perna(cv, hip, knee, ank, pe_ang, k_esc, a):
    """Perna inteira: coxa e canela de pele, meia, tênis e a barra da bermuda (até acima do joelho)."""
    tp = tons_escuros(TONS_PELE, k_esc); tb = tons_escuros(TONS_BERM, k_esc); tm = tons_escuros(TONS_MEIA, k_esc)
    linha = esc_cor(PELE_LINHA, k_esc)
    coxa = capsula(hip, knee, 64, 50)
    pinta(cv, coxa, hip, knee, 64, tp, a, linha=linha)
    can = canela_path(knee, ank, k=0.80)
    pinta(cv, can, knee, ank, 52, tp, a, linha=linha)
    d = norm((knee[0] - ank[0], knee[1] - ank[1]))
    topo_meia = soma(ank, d, 46)
    meia = capsula(ank, topo_meia, 36, 38)
    pinta(cv, meia, ank, topo_meia, 38, tm, a, linha=esc_cor("#AEB9C5", k_esc), larg_linha=2)
    tenis(cv, ank, pe_ang, k_esc, a)
    m = lerp2(hip, knee, 0.56)
    berm = capsula(hip, m, 76, 70)
    pinta(cv, berm, hip, m, 76, tb, a, linha=esc_cor("#262B33", k_esc))


def mao(cv, p, dirx, diry, tons, a):
    """Mão aberta e lisa (cópia do cf_chamaovar, garra 0)."""
    L = math.hypot(dirx, diry) or 1.0; ux, uy = dirx / L, diry / L
    comp, larg = 26, 30
    q0 = (p[0] - ux * comp * 0.5, p[1] - uy * comp * 0.5); q1 = (p[0] + ux * comp * 0.5, p[1] + uy * comp * 0.5)
    pinta(cv, capsula(q0, q1, larg, larg * 0.86), q0, q1, larg, tons, a, linha=esc_cor(tons[0], 0.25), larg_linha=2)


def braco(cv, ombro, cot, mao_p, k_esc, a):
    tp = tons_escuros(TONS_PELE, k_esc); tc = tons_escuros(TONS_CAMISA, k_esc)
    up = capsula(ombro, cot, 32, 28)
    pinta(cv, up, ombro, cot, 32, tp, a, linha=esc_cor(tp[0], 0.25))
    pulso = lerp2(cot, mao_p, 0.84)
    fo = capsula(cot, pulso, 28, 23)
    pinta(cv, fo, cot, pulso, 28, tp, a, linha=esc_cor(tp[0], 0.25))
    mao(cv, mao_p, mao_p[0] - cot[0], mao_p[1] - cot[1], tp, a)
    mg = lerp2(ombro, cot, 0.46)
    pinta(cv, capsula(ombro, mg, 46, 42), ombro, mg, 46, tc, a, linha=esc_cor(tc[0], 0.3))


def cabeca(cv, head, al, up, fw, a):
    """Cabeça: círculo liso, sem rosto; cabelo atrás e em cima (mostra para onde a criança olha).
    (cópia do cf_chamaovar, com o raio de criança)"""
    sh_c = skia.GradientShader.MakeRadial(skia.Point(head[0] + fw[0] * 16 + up[0] * 14, head[1] + fw[1] * 16 + up[1] * 14),
                                          HR * 1.4, [_c(PELE_CL), _c(PELE), _c(PELE_ESC)], [0.0, 0.55, 1.0])
    cv.drawCircle(head[0], head[1], HR, paint(PELE, int(255 * a), shader=sh_c))
    cv.drawCircle(head[0], head[1], HR, paint(PELE_LINHA, int(180 * a), "stroke", 2.5))
    k = HR / 50.0
    cv.save(); cv.translate(head[0], head[1]); cv.rotate(math.degrees(al)); cv.scale(k, k)
    cab = skia.Path(); cab.addCircle(0, 0, 53)
    cl = skia.Path(); cl.moveTo(-70, 34); cl.lineTo(-70, -70); cl.lineTo(34, -70); cl.lineTo(26, -26)
    cl.cubicTo(8, -18, -14, -4, -20, 34); cl.close()
    cab = skia.Op(cab, cl, skia.PathOp.kIntersect_PathOp)
    if cab is not None:
        cv.drawPath(cab, paint(CABELO, int(255 * a)))
        cv.drawPath(cab, paint("#5A4434", int(140 * a), "stroke", 2))
    cv.restore()


def pose(t, T, nome):
    """-> parâmetros da pose: ag (agachamento 0-1), bola (mãos na bola), corre, fase, J (altura do pulo),
    braços para a frente, braços para cima."""
    ks = [(0.0, 1.0), (T["agachou"], 1.0), (T["agachou"] + 0.32, 0.72), (T["crec"], 1.0),
          (T["vamos"] + 0.25, 1.0), (T["vamos"] + 0.62, 0.0)]
    if nome == "B":
        # "um joelho que NÃO estala": só B agacha, em silêncio (A fica em pé, no véu); sobe no respiro
        ks += [(T["estala"] - 0.30, 0.0), (T["estala"] + 0.12, 1.0), (T["estala"] + 0.38, 1.0)]
    # "Agacha" = as duas DESCEM na palavra; "de novo" = um quique; o fundo cai em cada "crec"
    ks += [(T["agacha"] - 0.04, 0.0), (T["agacha"] + 0.45, 0.62), (T["novo"] + 0.25, 0.48),
           (T["crec2"], 1.0), (T["crec2"] + 0.24, 0.40), (T["crec3"], 1.0), (T["crec3"] + 0.25, 0.40),
           (T["crec4"], 1.0), (T["agora"], 1.0), (T["agora"] + 0.3, 0.0)]
    t_dec, t_pou = t_salto(T)
    ks += [(T["pulam"], 0.0), (T["pulam"] + 0.08, 0.45), (t_dec + 0.03, 0.0), (t_pou - 0.01, 0.0),
           (t_pou + 0.07, 0.42), (t_pou + 0.30, 0.0)]
    ks += [(T["joelho3"] - 0.30, 0.0), (T["joelho3"] + 0.05, 1.0), (T["inofensivo"], 1.0),
           (T["inofensivo"] + 0.32, 0.0), (T["barulho"] - 0.05, 0.0), (T["barulho"] + 0.22, 0.85),
           (T["barulho"] + 0.50, 0.0)]
    ag = chaves(t, ks)
    bola = 1 - prog(t, T["vamos"] + 0.25, T["vamos"] + 0.5)
    corre = prog(t, T["correm"] - 0.06, T["correm"] + 0.06) * (1 - prog(t, T["pulam"] - 0.04, T["pulam"] + 0.06))
    fase = 0.5 - 0.5 * math.cos(2 * math.pi * (t - T["correm"]) / 0.24)
    J = 0.0
    if t_dec <= t <= t_pou:
        u = (t - t_dec) / (t_pou - t_dec)
        J = J_MAX * 4 * u * (1 - u)
    # braços à frente nos agachamentos do teste (equilíbrio); no ar, para cima e à frente
    frente = ag * (1 - bola)
    cima = clamp(J / 50.0)
    return dict(ag=ag, bola=bola, corre=corre, fase=fase, J=J, frente=frente, cima=cima)


def t_salto(T):
    t_dec = T["pulam"] + 0.09
    return t_dec, t_dec + 0.54


def t_pico(T):
    t_dec, t_pou = t_salto(T)
    return (t_dec + t_pou) / 2


def esqueleto(ps):
    """Pontos da criança (unidades, origem no chão sob o tornozelo)."""
    ag, bola, corre, fase, J = ps["ag"], ps["bola"], ps["corre"], ps["fase"], ps["J"]
    hip = lerp2(HIP_PE, HIP_AG, ag)
    lean = lerp(4, lerp(34, 46, bola), ag)
    ankN, ankF = ANK_N, ANK_F
    peN = peF = 0.0
    if corre > 0:                                              # corrida no lugar: 2 poses que se alternam
        # passada: perna da frente com o joelho alto, a de trás esticada (o chão corre embaixo)
        bob = -9 * abs(math.sin(math.pi * fase))
        hip_c = (0.0, HIP_PE[1] + 12 + bob)
        frente_p, tras_p = (55.0, -95.0), (-129.0, -83.0)
        cN = lerp2(frente_p, tras_p, fase); cF = lerp2(tras_p, frente_p, fase)
        hip = lerp2(hip, hip_c, corre)
        ankN = lerp2(ankN, cN, corre); ankF = lerp2(ankF, (cF[0] - 8, cF[1]), corre)
        peN = corre * lerp(10, 55, fase); peF = corre * lerp(55, 10, fase)
        lean = lerp(lean, 12, corre)
    hip = (hip[0], hip[1] - J)
    if J > 0:                                                  # no ar: pernas ESTICADAS, ponta do pé para baixo
        reto = (hip[0] + math.sin(math.radians(5)) * (L1 + L2 - 1), hip[1] + math.cos(math.radians(5)) * (L1 + L2 - 1))
        ankN = (reto[0] + 6, reto[1]); ankF = (reto[0] - 10, reto[1] - 4)
        pe = PE_AR * clamp(J / 40.0)
        peN, peF = pe, pe
    al = math.radians(lean)
    up = (math.sin(al), -math.cos(al)); fw = (math.cos(al), math.sin(al))
    sh = soma(hip, up, TRONCO)
    head = soma(soma(sh, up, PESC + HR - 4), fw, 10)
    ombro = soma(soma(sh, up, -16), fw, 2)
    ombroF = (ombro[0] - 6, ombro[1] - 3)
    kN, aN = ik2(hip, ankN, L1, L2, 1)
    hipF = (hip[0] - 4, hip[1] - 2)
    kF, aF = ik2(hipF, ankF, L1, L2, 1)
    # mãos: penduradas / à frente / na bola / balanço da corrida / para cima no pulo
    pend_N, pend_F = soma(ombro, (10, 194)), soma(ombroF, (-2, 194))
    fr_N, fr_F = soma(ombro, (170, -36)), soma(ombroF, (162, -46))    # à frente, acima da estrela e abaixo da cara
    bo_N = (BOLA_C[0] - 8, BOLA_C[1] - BOLA_R + 4); bo_F = (BOLA_C[0] - 18, BOLA_C[1] - BOLA_R + 2)
    sw = math.cos(math.pi * fase)                              # braço oposto à perna
    co_N, co_F = soma(ombro, (34 - 92 * sw, 132 - 18 * abs(sw))), soma(ombroF, (34 + 92 * sw, 132 - 18 * abs(sw)))
    ci_N, ci_F = soma(ombro, (156, -80)), soma(ombroF, (148, -90))
    hN, hF = pend_N, pend_F
    hN = lerp2(hN, fr_N, ps["frente"]); hF = lerp2(hF, fr_F, ps["frente"])
    hN = lerp2(hN, bo_N, bola); hF = lerp2(hF, bo_F, bola)
    hN = lerp2(hN, co_N, corre); hF = lerp2(hF, co_F, corre)
    hN = lerp2(hN, ci_N, ps["cima"]); hF = lerp2(hF, ci_F, ps["cima"])
    eN, mN = ik2(ombro, hN, BRACO, ANTEB, -1)
    eF, mF = ik2(ombroF, hF, BRACO, ANTEB, -1)
    return dict(hip=hip, hipF=hipF, al=al, up=up, fw=fw, sh=sh, head=head, ombro=ombro, ombroF=ombroF,
                kN=kN, aN=aN, kF=kF, aF=aF, eN=eN, mN=mN, eF=eF, mF=mF, peN=peN, peF=peF, bola=bola)


def frente_joelho(b):
    """Direção da FRENTE do joelho de cá (para onde a patela aponta), em unidades."""
    u1 = norm((b["kN"][0] - b["hip"][0], b["kN"][1] - b["hip"][1]))
    u2 = norm((b["aN"][0] - b["kN"][0], b["aN"][1] - b["kN"][1]))
    return norm((u1[1] + u2[1], -u1[0] - u2[0]))


def desenha_crianca(cv, b, a=1.0, meio=None):
    """Ordem: perna de lá, braço de lá, tronco e cabeça, (bola), braços entre os joelhos, perna de cá, braço de cá."""
    entre = b["bola"] > 0.5
    perna(cv, b["hipF"], b["kF"], b["aF"], b["peF"], 0.16, a)
    if not entre:
        braco(cv, b["ombroF"], b["eF"], b["mF"], 0.16, a)
    hip, sh, up, fw = b["hip"], b["sh"], b["up"], b["fw"]
    pesc = soma(sh, up, PESC + 6)
    pinta(cv, capsula(sh, pesc, 34, 32), sh, pesc, 34, TONS_PELE, a)
    tr = capsula(soma(hip, up, 18), soma(sh, up, -14), 100, 106)
    pinta(cv, tr, hip, sh, 106, TONS_CAMISA, a, linha=esc_cor(CAMISA_ESC, 0.3))
    q = soma(hip, up, 34)
    pinta(cv, capsula(hip, q, 96, 100), hip, q, 100, TONS_BERM, a, linha=esc_cor(BERM_ESC, 0.3))
    cabeca(cv, b["head"], b["al"], up, fw, a)
    if meio is not None:
        meio(cv)
    if entre:
        braco(cv, b["ombroF"], b["eF"], b["mF"], 0.16, a)
        braco(cv, b["ombro"], b["eN"], b["mN"], 0.0, a)
    perna(cv, hip, b["kN"], b["aN"], b["peN"], 0.0, a)
    if not entre:
        braco(cv, b["ombro"], b["eN"], b["mN"], 0.0, a)


def bola_desenho(cv, x, y, r, rot, a):
    """Bola azul de brincar (listra branca curva), com sombra no chão."""
    if a <= 0:
        return
    cv.drawOval(skia.Rect(x - r * 0.9, PISO_Y - 8, x + r * 0.9, PISO_Y + 8), paint("#6B4A2A", int(70 * a), blur=6))
    cv.save(); cv.translate(x, y); cv.rotate(rot)
    sh = skia.GradientShader.MakeRadial(skia.Point(-r * 0.35, -r * 0.4), r * 1.5, [_c(BOLA_CL), _c(BOLA), _c(BOLA_ESC)],
                                        [0.0, 0.5, 1.0])
    cv.drawCircle(0, 0, r, paint(BOLA, int(255 * a), shader=sh))
    cv.save(); cv.clipPath(_circ(r), skia.ClipOp.kIntersect, True)
    cv.drawArc(skia.Rect(-r * 1.6, -r * 0.55, r * 0.5, r * 1.9), 250, 110, False, paint("#FFFFFF", int(235 * a), "stroke", r * 0.22))
    cv.restore()
    cv.drawCircle(0, 0, r, paint(BOLA_ESC, int(255 * a), "stroke", 3))
    cv.restore()
    cv.drawCircle(x - r * 0.38, y - r * 0.42, r * 0.16, paint("#FFFFFF", int(150 * a), blur=3))


def _circ(r):
    p = skia.Path(); p.addCircle(0, 0, r); return p


# ------------------------------------------------------------------ posição de cada criança na tela
def transf(t, T, nome):
    """-> (x do tornozelo, escala, alfa). Quadro 0: UMA criança grande; em "Vamos" ela encolhe ao tamanho
    das colunas; em "prova" se CLONA (B nasce de trás de A); em "Estalo" B sai e A vai para o centro."""
    u = e_inout(prog(t, T["vamos"], T["vamos"] + 0.55))
    s, x = lerp(S0, S1, u), lerp(X0, XC, u)
    uc = e_inout(prog(t, T["prova"] - 0.05, T["prova"] + 0.5))
    u7 = e_inout(prog(t, T["estalo"], T["estalo"] + 0.4))
    if nome == "A":
        x = lerp(x, XA, uc)
        return lerp(x, XM, u7), s, 1.0
    a = (1.0 if t >= T["prova"] - 0.05 else 0.0) * (1 - u7)
    return lerp(lerp(XC, XB, uc), XB + 380, u7), s, a


def na_tela(tr, p):
    x, s, _a = tr
    return x + s * p[0], PISO_Y + s * p[1]


def tremor_A(t, T):
    """Só a coluna A treme um pouco a cada crec do teste."""
    d = 0.0
    for k in ("crec2", "crec3", "crec4"):
        kk = t - T[k]
        if 0 <= kk < 0.15:
            d += 4 * math.sin(kk * 90) * (1 - kk / 0.15)
    return d


def tremor_cam(t, T):
    d = 0.0
    k = t - T["crec"]
    if 0 <= k < 0.15:
        d += 4 * math.sin(k * 90) * (1 - k / 0.15)
    k = t - (T["mito"] + 0.12)
    if 0 <= k < 0.3:
        d += 8 * math.sin(k * 70) * (1 - k / 0.3)
    return d


def bola_virada(cv, t, T):
    """A virada concreta: a bola do quadro 0 VOLTA rolando (da frente, a 780 px/s) nas DUAS colunas e passa
    por baixo dos pés no pico do pulo — as duas pulam por cima dela ao mesmo tempo (correm, pulam e brincam
    igual). Desenhada antes das crianças; recortada em cada coluna."""
    pico = t_pico(T)
    r = R_BOLA_V * S1
    for x_tor, (x0, y0, x1, y1) in ((XA, PAINEL_A), (XB, PAINEL_B)):
        cx = x_tor + PE_X * S1 + V_BOLA * (pico - t)
        if cx - r > x1 or cx + r < x0:
            continue
        cv.save(); cv.clipRect(skia.Rect(x0 + 3, y0 + 3, x1 - 3, y1 - 3))
        bola_desenho(cv, cx, PISO_Y - r, r, -math.degrees((cx - x_tor) / r), 1.0)
        cv.restore()


# ------------------------------------------------------------------ o "crec" (por FORA do joelho)
def estalo(cv, x, y, R, a, cinza=0.0, giro=0.0):
    """Estrela de estalo: 6 raios curtos (ouro, com contorno escuro para ler sobre o creme) e núcleo branco.
    Sem letras. Nenhum raio aponta para trás (para dentro do joelho)."""
    if a <= 0 or R <= 1:
        return
    cor = lerpc(OURO, "#A9B1BA", cinza); borda = lerpc("#8A5A00", "#59636E", cinza)
    if cinza < 0.5:
        cv.drawCircle(x, y, R * 0.55, paint(OURO, int(80 * a * (1 - cinza)), blur=R * 0.25))
    larg = max(4.5, 14 * R / 100)
    for i in range(6):
        ang = math.radians(giro + 30 + 60 * i)
        r0, r1 = 0.40 * R, R * (1.0 if math.cos(ang) > 0.1 else 0.74)   # os de trás, mais curtos
        x0, y0, x1, y1 = x + r0 * math.cos(ang), y + r0 * math.sin(ang), x + r1 * math.cos(ang), y + r1 * math.sin(ang)
        cv.drawLine(x0, y0, x1, y1, paint(borda, int(200 * a), "stroke", larg + 6))
        cv.drawLine(x0, y0, x1, y1, paint(cor, int(255 * a), "stroke", larg))
    cv.drawCircle(x, y, R * 0.21, paint("#FFFFFF", int(255 * a)))
    cv.drawCircle(x, y, R * 0.21, paint(cor, int(255 * a), "stroke", max(2.5, 4 * R / 100)))


def pos_estalo(b, tr, R):
    """Centro da estrela: à FRENTE do joelho (mais para a frente que para cima), fora da pele."""
    kx, ky = na_tela(tr, b["kN"])
    f = frente_joelho(b)
    d = norm((f[0] + 1.0, f[1] + 0.42))
    off = 34 * tr[1] + 0.68 * R
    return kx + d[0] * off, ky + d[1] * off


def tracejado_joelho(cv, t, b, tr, a):
    """Contorno tracejado dourado em volta do joelho (o objeto do mito)."""
    if a <= 0:
        return
    kx, ky = na_tela(tr, b["kN"])
    r = 50 * tr[1]
    cv.drawCircle(kx, ky, r, paint("#8A5A00", int(110 * a), "stroke", 10))
    p = paint(OURO, int(255 * a), "stroke", 6)
    p.setPathEffect(skia.DashPathEffect.Make([15, 10], -t * 40))
    cv.drawCircle(kx, ky, r, p)


def estrela4(cv, px, py, s, cor, a, borda=None):
    """Brilhinho de 4 pontas (cópia do piloto)."""
    p = skia.Path(); p.moveTo(px, py - s * 2); p.lineTo(px + s * 0.5, py - s * 0.5); p.lineTo(px + s * 2, py)
    p.lineTo(px + s * 0.5, py + s * 0.5); p.lineTo(px, py + s * 2); p.lineTo(px - s * 0.5, py + s * 0.5)
    p.lineTo(px - s * 2, py); p.lineTo(px - s * 0.5, py - s * 0.5); p.close()
    if borda:
        cv.drawPath(p, paint(borda, int(200 * clamp(a)), "stroke", 3))
    cv.drawPath(p, paint(cor, int(255 * clamp(a))))


def brilhos_sobem(cv, x, y, t, t0, n=7, dur=0.9, raio=70):
    """A estrela de estalo se desfaz em brilhos dourados que SOBEM e somem (era só som)."""
    k = t - t0
    if k < 0 or k > dur:
        return
    u = k / dur
    for i in range(n):
        ang = -math.pi / 2 + (i - (n - 1) / 2) * 0.42
        d = raio * (0.3 + 0.9 * e_out(u)) * (0.75 + 0.25 * ((i * 37) % 10) / 10)
        estrela4(cv, x + d * math.cos(ang), y + d * math.sin(ang) - 60 * u, 9 * (1 - u) + 3, OURO, 1 - u, borda="#8A5A00")


# ------------------------------------------------------------------ objetos do ritual (cópias do piloto)
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


def rotulo(cv, s, x, y, a, esc=1.0):
    """Rótulo da condição acima da coluna (pílula escura, texto 40 px), entra com PULO de escala."""
    if a <= 0 or esc <= 0.01:
        return
    lw = larg_texto(s, F_BLACK, 40)
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 24, -29, lw / 2 + 24, 29), 29, 29)
    cv.drawRRect(rr, paint("#000000", int(70 * a), blur=8))
    cv.drawRRect(rr, paint(NAVY, int(240 * a)))
    cv.drawRRect(rr, paint("#5E7186", int(255 * a), "stroke", 3))
    texto(cv, s, 0, 14, F_BLACK, 40, "#FFFFFF", int(255 * a))
    cv.restore()


def chip(cv, s, x, y, a, esc=1.0):
    """Chip claro (40 px): SEM DOR."""
    if a <= 0 or esc <= 0.01:
        return
    lw = larg_texto(s, F_BLACK, 40)
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 26, -33, lw / 2 + 26, 31), 32, 32)
    cv.drawRRect(rr, paint("#000000", int(90 * a), blur=10))
    cv.drawRRect(rr, paint("#FFFFFF", int(255 * a)))
    cv.drawRRect(rr, paint(NAVY, int(255 * a), "stroke", 4))
    texto(cv, s, 0, 14, F_BLACK, 40, NAVY, int(255 * a))
    cv.restore()


# ------------------------------------------------------------------ veredito (topo): a aposta MITO | VERDADE
def cartao_pose(t, T):
    tv = T["veredito"]
    if t < tv - 0.05:
        return None
    u = e_back(prog(t, tv - 0.05, tv + 0.35), 1.1)
    dy = lerp(-460, 0, u)
    sai = prog(t, T["estalo"] - 0.36, T["estalo"] - 0.04) ** 3        # sobe SEM recuo, antes de "Estalo"
    return dy - 520 * sai, 1.0 if sai < 1 else 0.0


def roleta(T):
    """7 tiques que DESACELERAM: começa em MITO e alterna; o 6º PARA em VERDADE (~0,25 s) e o 7º cai em
    MITO exatamente na palavra."""
    t0, t5 = T["veredito"] + 0.32, T["mito"] - 0.25
    return [lerp(t0, t5, (k / 5) ** 1.6) for k in range(6)] + [T["mito"]]


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


def larg_marca(s=R_MITO, tam=TAM_MARCA):
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
    for _ in range(36):
        cv.drawCircle(rng.uniform(-lw / 2 - 28, lw / 2 + 28), rng.uniform(-tam * 0.5 - 14, tam * 0.5 + 14),
                      rng.uniform(1.5, 4.0), paint(CARTAO, int(170 * a)))
    cv.restore()


def t_bate(T):
    return T["mito"] + 0.12


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
    tb = t_bate(T)
    sel, pulso = selecao(t, T)
    bateu = t >= tb
    apaga = prog(t, tb, tb + 0.25)
    opcao(cv, R_MITO, SLOT_X["mito"], 1.0, 1.0 * (sel == 0), pulso, 0.0)
    opcao(cv, R_VERDADE, SLOT_X["verdade"], 1.0, 1.0 * (sel == 1 and not bateu), pulso, apaga)
    if bateu:
        k = t - tb
        marca_carimbo(cv, R_MITO, MARCA[0], MARCA[1], -4, 1.0, esc=lerp(1.25, 1.0, e_out(clamp(k / 0.12))))
    cv.restore()


def carimbo_obj(cv, x, y, rot, esc, a, esmaga=0.0, larg=188):
    """Carimbo de madeira; (x, y) = centro da borracha (LISA: sem texto gravado). (cópia do piloto)"""
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


def carimbo_pose(t, T):
    """O carimbo só aparece no golpe: desce do alto à direita a partir de "mito", BATE em 0,12 s em MITO
    e sobe em 0,16 s (nunca paira sobre o texto do cartão)."""
    tb = t_bate(T)
    t_in = tb - 0.12
    if t < t_in or t > tb + 0.16:
        return None
    larg = larg_marca()
    alvo = (MARCA[0], MARCA[1], -4.0)
    if t < tb:
        u = clamp((t - t_in) / 0.12) ** 2
        x, y, rot = lerp(1180, alvo[0], u), lerp(-300, alvo[1], u), lerp(24.0, alvo[2], u)
        return x, y, rot, 1.0, 1.0, 0.0, larg
    esmaga = math.sin(math.pi * clamp((t - tb) / 0.06))
    w = e_out(prog(t, tb + 0.03, tb + 0.16))
    x, y, rot = lerp(alvo[0], 1200, w), lerp(alvo[1], -420, w), lerp(alvo[2], 20.0, w)
    return x, y, rot, 1.0, 1.0, esmaga, larg


def impacto(cv, t, T):
    k = t - t_bate(T)
    if k < 0 or k > 0.35:
        return
    mx, my = MARCA
    u = e_out(k / 0.35); a = 1 - k / 0.35
    for i in range(12):
        ang = i * 2 * math.pi / 12 + 0.2
        r0, r1 = 150 + 50 * u, 175 + 95 * u
        ex, ey = math.cos(ang), math.sin(ang) * 0.42
        cv.drawLine(mx + r0 * ex, my + r0 * ey, mx + r1 * ex, my + r1 * ey, paint(OURO, int(230 * a), "stroke", 7))


# ------------------------------------------------------------------ cena 8: a regra
def cartao_regra(cv, t, T):
    """Cartão claro no alto da bancada: O SINTOMA GUIA (64 px) / NÃO O BARULHO (44 px)."""
    k = prog(t, T["sintoma"] - 0.08, T["sintoma"] + 0.22)
    if k <= 0:
        return
    sai = e_inout(prog(t, T["mas"] - 0.28, T["mas"] + 0.02))          # sai INTEIRO antes do asterisco
    a = clamp(k * 2.5) * (1 - sai)
    if a <= 0:
        return
    x0, y0, x1, y1 = REGRA
    esc = (e_back(k) if k < 1 else 1.0) * (1 - 0.08 * sai) + 0.03 * pulo(t, T["barulho"], 0.3)
    cv.save(); cv.translate(CX, (y0 + y1) / 2); cv.scale(max(0.01, esc), max(0.01, esc)); cv.translate(-CX, -(y0 + y1) / 2)
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 28, 28)
    sombra(cv, x0, y0 + 12, x1, y1 + 12, 28, 18, 120 * a / 255)
    cv.drawRRect(rr, paint(CARTAO, int(255 * a)))
    cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 6))
    texto(cv, R_GUIA, CX, y0 + 86, F_BLACK, 64, NAVY, int(255 * a))
    kb = prog(t, T["barulho"] - 0.08, T["barulho"] + 0.18)
    if kb > 0:
        cv.save(); cv.translate(CX, y0 + 150); s = max(0.01, e_back(kb)) if kb < 1 else 1.0; cv.scale(s, s)
        texto(cv, R_BARULHO, 0, 0, F_BLACK, 44, "#5E7186", int(255 * a * clamp(kb * 3)))
        cv.restore()
    cv.restore()


# ------------------------------------------------------------------ cena 9: o asterisco (pictogramas de traço)
def ico_raio(cv, a, t, k):
    """Raio (cópia do ícone DOR NOVA do piloto)."""
    p = skia.Path(); p.moveTo(10, -58); p.lineTo(-28, 6); p.lineTo(-2, 6); p.lineTo(-14, 58)
    p.lineTo(28, -10); p.lineTo(2, -10); p.lineTo(16, -58); p.close()
    cv.drawPath(p, paint(OURO, int(255 * a)))
    cv.drawPath(p, paint("#8A5A00", int(255 * a), "stroke", 3))


def _perninha(cv, a, joelho, tornozelo, bojo=0.0):
    """Perninha de TRAÇO (pictograma, nunca a criança): coxa, canela e pé em contorno branco."""
    quadril = (-6, -62)
    coxa = capsula(quadril, joelho, 30, 24)
    can = capsula(joelho, tornozelo, 24, 18)
    pe = capsula(tornozelo, (tornozelo[0] + 34, tornozelo[1] + 4), 16, 14)
    pth = uniao(coxa, can, pe)
    if bojo > 0:
        kk = skia.Path(); kk.addCircle(joelho[0] + 4, joelho[1], 13 + 9 * bojo)
        pth = uniao(pth, kk)
    cv.drawPath(pth, paint("#FFFFFF", int(40 * a)))
    cv.drawPath(pth, paint("#FFFFFF", int(255 * a), "stroke", 5))


def _seta_curta(cv, x0, y0, ang, L, a):
    x1, y1 = x0 + L * math.cos(ang), y0 + L * math.sin(ang)
    pt = paint(AMBAR, int(255 * a), "stroke", 5)
    cv.drawLine(x0, y0, x1, y1, pt)
    for s in (-1, 1):
        ah = ang + math.pi + s * 0.55
        cv.drawLine(x1, y1, x1 + 11 * math.cos(ah), y1 + 11 * math.sin(ah), pt)


def ico_incha(cv, a, t, k):
    """Perninha reta com o joelho mais cheio e 3 setinhas para fora."""
    _perninha(cv, a, (0, 0), (-4, 58), bojo=0.5 + 0.5 * e_out(clamp(k * 2)))
    for ang in (-50, 0, 50):
        r = math.radians(ang)
        _seta_curta(cv, 4 + 26 * math.cos(r), 26 * math.sin(r), r, 22, a)


def ico_trava(cv, a, t, k):
    """Perninha dobrada com um cadeadinho no joelho."""
    _perninha(cv, a, (14, -4), (-34, 46))
    x, y = 34, -20
    cv.drawArc(skia.Rect(x - 12, y - 30, x + 12, y - 4), 180, 180, False, paint(AMBAR, int(255 * a), "stroke", 5))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 17, y - 14, x + 17, y + 14), 5, 5), paint(AMBAR, int(255 * a)))
    cv.drawCircle(x, y - 2, 3.5, paint(NAVY, int(255 * a)))
    cv.drawLine(x, y, x, y + 7, paint(NAVY, int(255 * a), "stroke", 3))


def ico_falseia(cv, a, t, k):
    """Perninha que CEDE no joelho (zigue-zague) com dois arquinhos de movimento."""
    dx = 6 * math.sin(t * 9)
    _perninha(cv, a, (20 + dx, 2), (-4, 58))
    for i, r in enumerate((24, 36)):
        cv.drawArc(skia.Rect(26 + dx - r, 2 - r, 26 + dx + r, 2 + r), -40, 80, False,
                   paint(AMBAR, int((255 - 70 * i) * a), "stroke", 4))


def estetoscopio(cv, x, y, a):
    """Estetoscópio de traço (avaliação)."""
    pt = paint(NAVY, int(255 * a), "stroke", 5)
    cv.save(); cv.translate(x, y)
    cv.drawLine(-14, -24, -10, -6, pt); cv.drawLine(14, -24, 10, -6, pt)
    p = skia.Path(); p.moveTo(-10, -6); p.cubicTo(-10, 12, 10, 12, 10, -6)
    cv.drawPath(p, pt)
    q = skia.Path(); q.moveTo(0, 8); q.cubicTo(0, 26, 22, 26, 22, 12)
    cv.drawPath(q, pt)
    cv.drawCircle(22, 6, 7, paint(NAVY, int(255 * a)))
    cv.drawCircle(22, 6, 3, paint(OURO, int(255 * a)))
    cv.restore()


CELULAS = ((300, 612, "doi", ico_raio, R_DOI), (780, 612, "incha", ico_incha, R_INCHA),
           (300, 896, "trava", ico_trava, R_TRAVA), (780, 896, "falseia", ico_falseia, R_FALSEIA))


def cartao_asterisco(cv, t, T):
    """Cartão escuro de borda ÂMBAR que sobe da bancada em "Mas" (recortado nela); um pictograma por
    palavra (o da vez com anel dourado); "MERECE AVALIAÇÃO" no pé; recolhe no lugar antes da CTA."""
    t0 = T["mas"] + 0.04                                               # só depois que a regra saiu
    k = prog(t, t0, t0 + 0.32)
    if k <= 0:
        return
    sai = e_inout(prog(t, T["manda"] - 0.4, T["manda"]))
    a = clamp(k * 6) * (1 - sai)                                       # sobe já opaco (nada de bloco cinza)
    if a <= 0:
        return
    dy = 520 * (1 - e_out(k))
    esc = 1 - 0.06 * sai
    x0, y0, x1, y1 = ALERTA
    cv.save()
    cv.clipRRect(skia.RRect.MakeRectXY(skia.Rect(*BANC), 34, 34), skia.ClipOp.kIntersect, True)
    cv.translate(CX, 800); cv.scale(esc, esc); cv.translate(-CX, -800 + dy)
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 34, 34)
    sombra(cv, x0, y0, x1, y1, 34, 20, 120 * a / 255)
    cv.drawRRect(rr, paint(NAVY, int(252 * a)))
    cv.drawRRect(rr, paint(AMBAR, int(255 * a), "stroke", 4))
    ph = 1 + 0.08 * pulo(t, T["joelho4"], 0.35)
    lw = larg_texto(R_ALERTA, F_BLACK, 40)
    cv.save(); cv.translate(CX, 410); cv.scale(ph, ph)
    pill = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 28, -32, lw / 2 + 28, 32), 32, 32)
    cv.drawRRect(pill, paint(NAVY, int(255 * a)))
    cv.drawRRect(pill, paint(OURO, int(255 * a), "stroke", 3))
    texto(cv, R_ALERTA, 0, 14, F_BLACK, 40, OURO, int(255 * a))
    cv.restore()
    for n, (cx, cy, chave, ico, rot) in enumerate(CELULAS):
        ti = T[chave]
        kp = prog(t, T["mas"] + 0.2 + 0.12 * n, T["mas"] + 0.46 + 0.12 * n)      # lugar vazio à espera
        p = prog(t, ti - 0.06, ti + 0.24)
        if kp > 0 and p < 1:
            ap = a * clamp(kp * 3) * (1 - clamp(p * 2))
            pt = paint("#FFFFFF", int(150 * ap), "stroke", 4)
            pt.setPathEffect(skia.DashPathEffect.Make([18, 12], t * 30))
            r = 90 * (e_back(kp) if kp < 1 else 1.0) * (1 + 0.04 * math.sin(t * 6 + n))
            cv.drawCircle(cx, cy - 34, max(1.0, r), pt)
        if p <= 0:
            continue
        ai = a * clamp(p * 2.5)
        esc_i = e_back(p) if p < 1 else 1.0
        tf = CELULAS[n + 1][2] if n + 1 < len(CELULAS) else "avaliacao"
        vez = prog(t, ti - 0.06, ti + 0.08) * (1 - prog(t, T[tf] - 0.05, T[tf] + 0.2))
        cv.drawCircle(cx, cy - 34, 90, paint("#FFFFFF", int((22 + 18 * vez) * ai)))
        cv.drawCircle(cx, cy - 34, 90, paint(lerpc("#FFFFFF", OURO, vez), int(lerp(90, 255, vez) * ai), "stroke",
                                             lerp(3, 6, vez)))
        cv.save(); cv.translate(cx, cy - 34); cv.scale(max(0.01, esc_i) * 1.25, max(0.01, esc_i) * 1.25)
        ico(cv, ai, t, p)
        cv.restore()
        texto(cv, rot, cx, cy + 104, F_BLACK, 40, "#FFFFFF", int(255 * ai))
    ka = prog(t, T["avaliacao"] - 0.08, T["avaliacao"] + 0.22)
    if ka > 0:
        aa = a * clamp(ka * 2.5)
        lw = larg_texto(R_AVALIA, F_BLACK, 40)
        s = (e_back(ka) if ka < 1 else 1.0) * (1 + 0.06 * pulo(t, T["avaliacao"] + 0.3, 0.35))
        cv.save(); cv.translate(CX, 1132); cv.scale(max(0.01, s), max(0.01, s))
        larg_tot = lw + 70
        pill = skia.RRect.MakeRectXY(skia.Rect(-larg_tot / 2 - 28, -34, larg_tot / 2 + 28, 34), 34, 34)
        cv.drawRRect(pill, paint(OURO, int(255 * aa)))
        cv.drawRRect(pill, paint("#FFFFFF", int(200 * aa), "stroke", 3))
        estetoscopio(cv, -larg_tot / 2 + 18, -2, aa)
        texto(cv, R_AVALIA, -larg_tot / 2 + 70, 14, F_BLACK, 40, NAVY, int(255 * aa), centro=False)
        cv.restore()
    cv.restore()


# ------------------------------------------------------------------ quadro
def crianca(cv, t, T, nome, extra_meio=None):
    """Desenha uma criança (A ou B) no lugar dela; devolve (esqueleto, transformação) ou None."""
    tr = transf(t, T, nome)
    x, s, a = tr
    if a <= 0:
        return None
    ps = pose(t, T, nome)
    b = esqueleto(ps)
    dx = tremor_A(t, T) if nome == "A" else 0.0
    pul = 1 + 0.04 * pulo(t, T["dois"], 0.3)
    cv.save()
    if a < 1:
        p = skia.Paint(); p.setAlphaf(a); cv.saveLayer(None, p)
    cv.translate(x + dx, PISO_Y); cv.scale(s * pul, s * pul)
    if ps["J"] <= 0:
        cv.drawOval(skia.Rect(-70, -10, 150, 10), paint("#6B4A2A", 70, blur=8))       # sombra no chão
    else:
        k = 1 - 0.5 * ps["J"] / J_MAX
        cv.drawOval(skia.Rect(-60 * k, -8, 130 * k, 8), paint("#6B4A2A", int(60 * k), blur=8))
    desenha_crianca(cv, b, 1.0, meio=extra_meio)
    if a < 1:
        cv.restore()
    cv.restore()
    return b, (x + dx, s * pul, a)


def pos_chip():
    """Chip SEM DOR na ALTURA do joelho, logo à direita da estrela do crec (A agachada no centro)."""
    if "chip" not in _CACHE:
        b = esqueleto(dict(ag=1.0, bola=0.0, corre=0.0, fase=0.0, J=0.0, frente=1.0, cima=0.0))
        R = 95.0
        sx, sy = pos_estalo(b, (XM, S1, 1.0), R)
        lw = larg_texto(R_SEMDOR, F_BLACK, 40)
        _CACHE["chip"] = (min(sx + 0.85 * R + lw / 2 + 26 + 20, BANC[2] - lw / 2 - 50), sy)
    return _CACHE["chip"]


def quadro(cv, t, T, blocos, ep):
    fundo_rapido(cv, t)
    tremor = tremor_cam(t, T)
    cv.save(); cv.translate(tremor, 0)
    bancada(cv)
    cv.save()
    cv.clipRRect(skia.RRect.MakeRectXY(skia.Rect(*BANC), 34, 34), skia.ClipOp.kIntersect, True)
    paineis(cv, t, T)
    corre = prog(t, T["correm"] - 0.06, T["correm"] + 0.06) * (1 - prog(t, T["pulam"] - 0.04, T["pulam"] + 0.1))
    chao_correndo(cv, t, T, PAINEL_A[0], PAINEL_A[2], corre)
    chao_correndo(cv, t, T, PAINEL_B[0], PAINEL_B[2], corre)

    # ---- bola (quadro 0): entre os pés, sai rolando em "Vamos"
    def bola_meio(cv2):
        kb = prog(t, T["vamos"] + 0.05, T["vamos"] + 0.75)
        if kb >= 1:
            return
        rx = BOLA_C[0] + 640 * kb ** 2
        bola_desenho(cv2, rx, BOLA_C[1], BOLA_R, math.degrees(640 * kb ** 2 / BOLA_R), 1.0)

    # ---- a bola que VOLTA na virada (atrás das crianças)
    bola_virada(cv, t, T)
    # ---- as crianças (B atrás, A na frente)
    rB = crianca(cv, t, T, "B")
    rA = crianca(cv, t, T, "A", extra_meio=bola_meio)
    # ---- véu na coluna fora de foco ("Do outro lado... que NÃO estala": B em foco e agacha sozinha)
    fo = prog(t, T["outro"] - 0.15, T["outro"] + 0.1) * (1 - prog(t, T["estala"] + 0.30, T["estala"] + 0.55))
    if fo > 0:
        x0, y0, x1, y1 = PAINEL_A
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0 + 2, y0 + 2, x1 - 2, y1 - 2), 24, 24), paint(BANCADA, int(140 * fo)))
    # ---- tracejado dourado no joelho (o objeto do mito)
    pico = t_pico(T)
    if rA:
        bA, trA = rA
        aj = prog(t, T["joelho"] - 0.05, T["joelho"] + 0.15) * (1 - prog(t, T["crec"] + 0.25, T["crec"] + 0.5))
        aj = max(aj, prog(t, T["joelho3"] - 0.05, T["joelho3"] + 0.15) * (1 - prog(t, T["inofensivo"], T["inofensivo"] + 0.3)))
        # no pico do pulo: o joelho que estala, ESTICADO no ar, por cima da bola
        aj = max(aj, prog(t, pico - 0.16, pico - 0.06) * (1 - prog(t, pico + 0.16, pico + 0.28)))
        tracejado_joelho(cv, t, bA, trA, aj * (1 + 0.15 * pulo(t, T["joelho"], 0.3)))
    if rB:
        bB, trB = rB
        aj = prog(t, T["joelho2"] - 0.05, T["joelho2"] + 0.15) * (1 - prog(t, T["estala"] + 0.30, T["estala"] + 0.55))
        tracejado_joelho(cv, t, bB, trB, aj)
    # ---- o CREC (só na coluna A)
    if rA:
        bA, trA = rA
        cena_crec(cv, t, T, bA, trA)
    # ---- rastro de velocidade atrás das costas na corrida
    if corre > 0:
        for r in (rA, rB):
            if not r:
                continue
            b, tr_ = r
            hx, hy = na_tela(tr_, b["hip"])
            for j in range(3):
                f = ((t - T["correm"]) * 3.2 + j * 0.33) % 1.0
                yy = hy - 150 * tr_[1] + j * 52 * tr_[1]
                xx = hx - 70 * tr_[1] - 90 * f
                cv.drawLine(xx, yy, xx - 60, yy, paint("#9C8A6A", int(200 * corre * (1 - f)), "stroke", 6))
    # ---- chip SEM DOR (cena 7)
    kc = prog(t, T["sem"] - 0.05, T["sem"] + 0.25)
    ac = clamp(kc * 3) * (1 - prog(t, T["sintoma"] - 0.3, T["sintoma"] - 0.1))
    if ac > 0:
        cx_, cy_ = pos_chip()
        chip(cv, R_SEMDOR, cx_, cy_, ac, max(0.01, (e_back(kc) if kc < 1 else 1.0) + 0.08 * pulo(t, T["dor"], 0.35)))
    cartao_regra(cv, t, T)
    # ---- véu OPACO antes do asterisco (a criança some por inteiro e não volta) e cartão do asterisco
    vm = prog(t, T["mas"] - 0.25, T["mas"] + 0.04)
    if vm > 0:
        cv.drawRect(skia.Rect(*BANC), paint(BANCADA, int(255 * vm)))
    cartao_asterisco(cv, t, T)
    vcta = 0.86 * prog(t, T["manda"] - 0.55, T["manda"] - 0.25)       # véu navy: a CTA fica sobre fundo escuro
    if vcta > 0:
        cv.drawRect(skia.Rect(*BANC), paint(NAVY, int(255 * vcta)))
    cv.restore()                                                       # sai do recorte da bancada

    # ---- rótulos das colunas (entram ~0,27 s depois de "estala", saem em "Veredito")
    pr = prog(t, T["estala"] + 0.22, T["estala"] + 0.5)
    ar = clamp(pr * 4) * (1 - prog(t, T["veredito"] - 0.12, T["veredito"] + 0.02))
    if ar > 0:
        er = max(0.01, e_back(pr)) if pr < 1 else 1.0
        rotulo(cv, R_A, (PAINEL_A[0] + PAINEL_A[2]) / 2, ROT_Y, ar, er)
        rotulo(cv, R_B, (PAINEL_B[0] + PAINEL_B[2]) / 2, ROT_Y, ar, er)
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
    a0 *= 1 - prog(t, T["veredito"] - 0.1, T["veredito"] + 0.1) * (1 - prog(t, T["estalo"] + 0.1, T["estalo"] + 0.35))
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


def cena_crec(cv, t, T, b, tr):
    """Onde e quando a estrela de estalo aparece em A (sempre por FORA do joelho)."""
    # cena 1: visível no quadro 0, esmaece em 0,3 s; ESTOURA de novo em "crec" e some em "Vamos"
    a1 = 1 - prog(t, 0.05, 0.35)
    k = t - T["crec"]
    esc1 = 1.0
    if k >= 0:
        u = clamp(k / 0.25)
        esc1 = lerp(0.6, 1.15, e_out(u / 0.6)) if u < 0.6 else lerp(1.15, 1.0, (u - 0.6) / 0.4)
        a1 = max(a1, clamp(k / 0.05) * (1 - prog(t, T["vamos"], T["vamos"] + 0.25)))
    if a1 > 0:
        R = 100 * esc1
        estalo(cv, *pos_estalo(b, tr, R), R, a1)
    # cena 4: um crec em A no fundo de cada agachamento, cada um MAIOR (B fica em silêncio). Na cena 3
    # ("um joelho que NÃO estala") só B agacha e nada estala: nenhum crec sobre a palavra negada.
    for chave, R0 in (("crec2", 80), ("crec3", 100), ("crec4", 120)):
        t0 = T[chave]
        k = t - t0
        if -0.01 <= k <= 0.5:
            u = clamp(k / 0.22)
            esc = lerp(0.6, 1.12, e_out(u / 0.6)) if u < 0.6 else lerp(1.12, 1.0, (u - 0.6) / 0.4)
            R = R0 * esc
            estalo(cv, *pos_estalo(b, tr, R), R, 1 - prog(k, 0.3, 0.5))
    # cena 7: crec em "joelho" #3; fica até "inofensivo" e vira brilho que sobe
    t7 = T["joelho3"] + 0.05
    k = t - t7
    ti = T["inofensivo"]
    if k >= -0.01 and t < ti + 1.0:
        u = clamp(k / 0.22)
        esc = lerp(0.6, 1.12, e_out(u / 0.6)) if u < 0.6 else lerp(1.12, 1.0, (u - 0.6) / 0.4)
        R = 95 * esc * (1 + 0.04 * math.sin(t * 5))
        a7 = 1 - prog(t, ti, ti + 0.25)
        x, y = pos_estalo(b, tr, R)
        if a7 > 0:
            estalo(cv, x, y, R, a7)
        if t >= ti:
            if "p7" not in _CACHE or _CACHE["p7"][0] != round(ti, 3):
                _CACHE["p7"] = (round(ti, 3), (x, y))
            px, py = _CACHE["p7"][1]
            brilhos_sobem(cv, px, py, t, ti, n=8, dur=0.9, raio=80)
    # cena 8: em "barulho", um crec PEQUENO e CINZA (o barulho perdeu a importância)
    t8 = T["barulho"] + 0.22
    k = t - t8
    if -0.01 <= k <= 0.5:
        R = 40 * (lerp(0.7, 1.0, e_out(clamp(k / 0.15))))
        estalo(cv, *pos_estalo(b, tr, R), R, 1 - prog(k, 0.3, 0.5), cinza=1.0)


# ------------------------------------------------------------------ sons
def _crec():
    """O crec: dois cliques defasados 12 ms + um tique leve em +20 ms (seco e suave, sem grave)."""
    SR = som.SR
    a, b, c = som.click(5), som.click(7), som.tick(3)
    n = int(0.03 * SR) + max(len(a), len(b), len(c))
    y = np.zeros(n)
    y[:len(a)] += a
    o = int(0.012 * SR); y[o:o + len(b)] += b
    o = int(0.020 * SR); y[o:o + len(c)] += 0.2 * c
    return y * 2.6                                   # curto (35 ms): precisa de ganho para se ouvir sob a voz


SFX_LOCAL = {"crec": _crec}


def sons(T):
    ev = [(T["agachou"], "whoosh", 0.2), (T["joelho"], "tick", 0.3), (T["crec"], "crec", 0.5)]
    ev += [(T["vamos"], "whoosh", 0.25)] + [(T["vamos"] + 0.12 + 0.15 * i, "tick", 0.15) for i in range(3)]
    ev += [(T["prova"] - 0.01, "tick", 0.5), (T["prova"] + 0.03, "whoosh", 0.35)]
    # "um joelho que NÃO estala": B agacha em SILÊNCIO (nenhum crec sobre a palavra negada); só o pop dos rótulos
    ev += [(T["outro"], "whoosh", 0.3), (T["joelho2"], "tick", 0.3), (T["estala"] + 0.27, "pop", 0.5)]
    ev += [(T["agacha"], "whoosh", 0.2), (T["crec2"], "crec", 0.45), (T["crec3"], "crec", 0.55), (T["crec4"], "crec", 0.65)]
    t_dec, t_pou = t_salto(T)
    ev += [(T["agora"], "whoosh", 0.3), (T["dois"], "pop", 0.3)]
    ev += [(T["correm"] + 0.06 + 0.12 * i, "tick", 0.25) for i in range(4)]
    ev += [(t_pico(T) - 0.42, "whoosh", 0.2)]                    # a bola volta rolando
    ev += [(T["pulam"], "whoosh", 0.35), (t_pico(T), "ding", 0.5), (t_pou, "thump", 0.4)]
    ev += [(T["veredito"], "whoosh", 0.4)]
    for i, ti in enumerate(roleta(T)):                            # roleta: um tique por troca, desacelerando
        ev.append((ti, "tick", lerp(0.35, 0.7, i / 6)))
    ev += [(t_bate(T), "thump", 0.6), (t_bate(T) + 0.02, "crackle", 0.4)]
    ev += [(T["estalo"], "whoosh", 0.3), (T["joelho3"] + 0.05, "crec", 0.5), (T["sem"], "pop", 0.5),
           (T["inofensivo"], "shimmer", 0.35)]
    ev += [(T["sintoma"], "pop", 0.6), (T["barulho"], "pop", 0.4), (T["barulho"] + 0.22, "crec", 0.2)]
    ev += [(T["mas"], "whoosh", 0.25)] + [(T[k], "pop", 0.5) for k in ("doi", "incha", "trava", "falseia")]
    ev += [(T["avaliacao"], "ding", 0.5), (T["manda"] - 0.4, "whoosh", 0.2), (T["manda"], "whoosh", 0.5)]
    return ev


def tempos_previa(T):
    t_dec, t_pou = t_salto(T)
    pico = t_pico(T)
    return (0.0, T["agachou"] + 0.3, T["crec"] + 0.1, T["vamos"] + 0.3, T["prova"] + 0.6, T["joelho2"] + 0.2,
            T["estala"] + 0.15, T["estala"] + 0.5, T["agacha"] + 0.1, T["agacha"] + 0.3, T["novo"] + 0.1,
            T["crec2"] + 0.05, T["crec4"] + 0.1, T["correm"] + 0.15, pico - 0.3, pico - 0.15, pico, pico + 0.15,
            t_pou + 0.05, T["veredito"] + 0.5, roleta(T)[5] + 0.1, t_bate(T) + 0.05, T["joelho3"] + 0.3,
            T["dor"] + 0.4, T["inofensivo"] + 0.4, T["barulho"] + 0.25, T["mas"] - 0.1, T["mas"] + 0.15,
            T["mas"] + 0.5, T["falseia"] + 0.4, T["avaliacao"] + 0.5, T["manda"] - 0.3, T["manda"] + 2.0)


# ------------------------------------------------------------------ render local (pausa do veredito)
_PONTA = re.compile(r"[.,:;!?—…]+$")
PAUSA_VEREDITO = 0.50                              # a roleta MITO | VERDADE respira antes do golpe
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
    """Cópia de som.mixar (som.py não se edita) com um envelope extra na trilha (de baixa[0] a baixa[1]
    ela desce para baixa[2]: o asterisco sóbrio) e o "crec" sintetizado aqui."""
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
    cache = {}
    for t_ev, nome, ganho in eventos:
        if nome not in cache:
            cache[nome] = SFX_LOCAL[nome]() if nome in SFX_LOCAL else som.SFX[nome]()
        s = cache[nome]
        p = int(t_ev * SR)
        if 0 <= p < n:
            m = min(len(s), n - p)
            fx[p:p + m] += s[:m] * ganho
    fx = LIM_FX * np.tanh(fx / LIM_FX)                  # limitador suave: efeito nunca passa do pico da voz
    mix = v * 1.0 + musica * duck + fx * 0.7
    pico = np.max(np.abs(mix)) or 1.0
    return mix / pico * 0.89


def preparar(ep, tmp, respiro_cta=0.5):
    """Voz -> palavras limpas -> corte de silêncio -> alinhamento -> pausa do veredito -> âncoras."""
    roteiro = "\n".join(ep["roteiro"])
    voz_bruta, palavras = _voz.narrar(roteiro, _voz.RITMO_COMO_FUNCIONA, os.path.join(tmp, "voz"))
    palavras = [dict(p, w=_PONTA.sub("", p["w"])) for p in palavras]
    voz_c, pal, tirado = comprimir(voz_bruta, palavras, respiro_cta=respiro_cta)
    pal = alinhar(pal, roteiro)
    voz_c, pal = inserir_pausa(voz_c, pal, "veredito", PAUSA_VEREDITO)
    T = ancoras(pal, ANCORAS)
    return voz_c, pal, T, tirado


def fazer_render_mito(quadro_fn, sons_fn, tempos_fn, respiro_cta=0.5):
    """Os passos do piloto (fazer_render_luz) com só a pausa do veredito + trilha baixa no asterisco."""
    def render(ep, mp4, tmp, previa=False):
        voz_c, pal, T, tirado = preparar(ep, tmp, respiro_cta)
        print(f"{ep['id']}: silêncio cortado {tirado:.2f}s | pausa do veredito {PAUSA_VEREDITO:.2f}s | "
              f"duração final {T['total']:.2f}s")
        blocos = montar_blocos(pal)

        def quadro_t(cv, t):
            quadro_fn(cv, t, T, blocos, ep)

        if previa:
            return _previas(quadro_t, tempos_fn(T), tmp, ep["id"]), T["total"]
        wav = os.path.join(tmp, f"{ep['id']}_mix.wav")
        baixa = (T["mas"] - 0.3, T["manda"] - 0.1, GANHO_ALARME / GANHO_TRILHA)
        som.gravar_wav(wav, mixar(voz_c, T["total"], sons_fn(T), GANHO_TRILHA, baixa))
        codificar(quadro_t, T["total"], wav, mp4)
        return mp4, T["total"]
    return render


render = fazer_render_mito(quadro, sons, tempos_previa, respiro_cta=0.5)
