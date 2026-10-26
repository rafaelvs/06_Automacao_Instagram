# -*- coding: utf-8 -*-
"""MITO NA PROVA — "MOCHILA PESADA / ENTORTA A COLUNA?" (série do piloto cf_mitonaprova_pinos).

Mecânica da série (a mesma do piloto v3/v4): a crença universal vira pergunta de sim/não no quadro 0;
UM objeto grande (a criança de perfil com a mochila ENORME) se CLONA em "prova" num teste justo em que
só muda UMA variável (o peso da mochila); selo "MITO OU VERDADE?"; o teste roda à vista e empurra a
aposta para VERDADE (a criança A se curva, estrelas de dor); a virada ("tira a mochila: a postura
volta" — a voz DIZ o resultado do teste enquanto A volta reta, igual a B); cartão do veredito com a
pergunta + MITO | VERDADE, um CURSOR dourado (só contorno, sem preencher) que corre entre as duas,
desacelera e ASSENTA em MITO (sem finta final para VERDADE) — na palavra, MITO se pinta e o carimbo bate; "Pode doer, mas causar escoliose?
Não há prova." (as estrelas de dor e o veredito não se contradizem); o jeito que vale (a mochila
gigante ENCOLHE para uma mochila escolar cheia, as duas voltam às costas, regra dos 10-15 % do peso);
o asterisco sóbrio (escoliose costuma não doer no começo; o sinal está numa TERCEIRA criança); CTA.

Correção 26/10 (leitor às cegas + revisor): cursor no lugar do botão aceso; linha-guia só depois que a
mochila sai das costas (sem cunha, nunca por cima da mochila); sem objetos voando (a palavra é "cheia");
cartão da regra inteiro de uma vez; quadro 0 já inclinado (13°, cabeça à frente).

Regras do storyboard (roteirista/verificador, 26/10/2026) seguidas aqui:
  * Criança de DESENHO do cf_escoliose (contorno arredondado, pele lisa, rosto sem detalhe, camiseta
    clara, shorts azul). Nada translúcido, nenhum osso, nenhuma coluna desenhada: a postura ruim é só
    o CONTORNO do corpo inclinado a partir do quadril; a linha-guia é tracejada, dourada e lisa (sem
    prumo, sem marca, sem número) e só aparece com as costas LIVRES (lê-se "reto").
  * As duas colunas do teste são idênticas em tudo, menos a mochila (mesma criança clonada, mesmo
    chão, mesmo ritmo de passo).
  * Estrelas de dor (estrela_dor do cf_escoliose) SÓ sobre camiseta/alça da criança A, só na cena 4;
    somem em brilhos na virada.
  * O sinal de escoliose aparece SÓ numa terceira criança, de costas, sem mochila, camiseta LARANJA:
    ombro direito mais alto e vão braço-cintura maior de um lado. Sem escápula, sem coluna por dentro.
  * Cartão do veredito em y ≥ 148; o carimbo só aparece no golpe (desce, bate, sobe em 0,16 s).
  * Selo com ponto vermelho DESENHADO (círculo). Todo texto desenhado está em ep["tela"] (ou é o
    gancho / a interface comum). Cena acima de y≈1226; abaixo, karaokê e rodapé CFM.
Helpers copiados (não importados) do piloto cf_mitonaprova_pinos e do cf_escoliose: nenhum arquivo
existente de animado/ foi editado.

Render: os passos de cf_fixador_circular.fazer_render_tolerante (pontuação limpa, corte de silêncio
com respiro_cta=0,5, alinhamento) + 0,50 s de silêncio logo depois de "Veredito:" (a roleta respira)
+ trilha baixa no asterisco (cópia local de som.mixar). A cena é PRESA ao roteiro pelas palavras-âncora
(ANCORAS): roteiro sem elas = KeyError.
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
ANCORAS = {
    "todo": ("todo", 1, False), "mochila": ("mochila", 1, False), "assim": ("assim", 1, False),
    "vamos": ("vamos", 1, False), "prova": ("prova", 1, False), "outro": ("outro", 1, False),
    "lado": ("lado", 1, False), "mochila2": ("mochila", 2, False), "leve": ("leve", 1, False),
    "peso": ("peso", 1, False), "exagerado": ("exagerado", 1, False), "dor": ("dor", 1, False),
    "costas": ("costas", 1, False), "ombros": ("ombros", 1, False), "postura": ("postura", 1, False),
    "carrega": ("carrega", 1, False), "agora": ("agora", 1, False), "tira": ("tira", 1, False),
    "mochila3": ("mochila", 3, False), "postura2": ("postura", 2, False), "volta": ("volta", 1, False),
    "veredito": ("veredito", 1, False), "mito": ("mito", 1, False), "doer1": ("doer", 1, False),
    "causar": ("causar", 1, False), "escoliose": ("escoliose", 1, False), "prova2": ("prova", 2, False),
    "mochila4": ("mochila", 4, False), "cheia": ("cheia", 1, False), "dez": ("dez", 1, False),
    "peso2": ("peso", 2, False), "crianca": ("criança", 1, False), "escoliose2": ("escoliose", 2, False),
    "costuma": ("costuma", 1, False), "doer": ("doer", 2, False), "comeco": ("começo", 1, False),
    "ombro": ("ombro", 1, False), "alto": ("alto", 1, False), "cintura": ("cintura", 1, False),
    "assimetrica": ("assimétrica", 1, False), "leve2": ("leve", 2, False),
    "avaliacao": ("avaliação", 1, False), "manda": ("manda", 1, False),
}
# "mito" fica FORA: o karaokê o pinta de ouro só enquanto é dito, sem brigar com o vermelho do carimbo
DESTAQUE = {"exagerado", "dor", "postura", "tira", "volta", "escoliose", "cheia", "quinze", "doer", "ombro",
            "cintura", "avaliação"}

# ------------------------------------------------------------------ textos de tela (todos em ep["tela"])
R_SELO = "MITO OU VERDADE?"
R_TESTE = "TESTE"
R_PESADA = "MOCHILA PESADA"                       # = linha 1 do gancho (já permitida)
R_LEVE = "MOCHILA LEVE"
R_MITO = "MITO"
R_VERDADE = "VERDADE"
R_REGRA1 = "ATÉ 10 A 15%"
R_REGRA2 = "DO PESO DA CRIANÇA"
R_ESC = "ESCOLIOSE"
R_DOER = "COSTUMA NÃO DOER"
R_COMECO = "NO COMEÇO"
R_OMBRO = "OMBRO MAIS ALTO"
R_CINTURA = "CINTURA ASSIMÉTRICA"
R_AVAL = "LEVE PARA AVALIAÇÃO"

# ------------------------------------------------------------------ paleta
NAVY = "#0B1824"
BANCADA, BANCADA_BORDA = "#F3EADB", "#D6C6AA"
PAINEL, PAINEL_BORDA = "#EADDC6", "#D2C09F"
CARTAO = "#FBF6EC"
MADEIRA, MADEIRA_CL, MADEIRA_ESC = "#B9844D", "#D9A86E", "#7B5129"
BORRACHA, BORRACHA_ESC, BORRACHA_CL = "#9A3F33", "#4E1A14", "#C0675A"
PELE_CL, PELE_ESC, PELE_LINHA = "#F7CDB8", "#DA987E", "#B9765E"          # cf_escoliose
SHORT, SHORT_CL, SHORT_ESC = "#4C86C6", "#6FA3DA", "#3A6FA8"
CAMISA, CAMISA_CL, CAMISA_ESC, CAMISA_LINHA = "#6FC7B1", "#9EE0CF", "#3F9A85", "#2C7464"
CAM3, CAM3_CL, CAM3_ESC, CAM3_LINHA = "#F2A154", "#F8C68E", "#CB7A2E", "#9A5418"   # 3ª criança: OUTRA cor
CABELO = "#4A3426"
MOCH, MOCH_CL, MOCH_ESC = "#6A4FB6", "#8F78DA", "#46318A"                 # mochila roxa (≠ shorts azul)
LIVROS = (("#F2B33D", "#B07A12"), ("#57B36A", "#2F7A41"), ("#4FA3E0", "#2A6FA6"))
CHIP_FUNDO = "#16304A"

# ------------------------------------------------------------------ geometria (1080 x 1920)
BANC = (24, 364, 1056, 1226)                      # bancada creme: a cena fica acima de y≈1226
PISO = 1186                                       # chão das crianças (tela)
S0, X0 = 1.55, 676                                # quadro 0: UMA criança grande (quadril em x=676)
S1, XA, XB = 1.2, 334, 844                        # depois de "prova": duas colunas iguais
PAINEIS = {"A": (44, 452, 528, 1206), "B": (552, 452, 1036, 1206)}
X_ROT = {"A": 286, "B": 794}
Y_ROT = 418
CARD = (100, 148, 980, 440)                       # cartão do veredito: abaixo do cabeçalho do Instagram
Q_Y = (223, 293)
TAM_Q = 62
SLOT_Y, SLOT_H, SLOT_W = 368, 80, 314
SLOT_X = {"mito": 361, "verdade": 719}
TAM_SLOT = 50
MARCA = (SLOT_X["mito"], SLOT_Y)                  # onde o carimbo bate
TAM_MARCA = 58
REGRA = (150, 374, 930, 566)                      # cartão da regra (cabeças abaixo de y≈600)
ASTER = (44, 392, 1036, 1208)                     # cartão do asterisco (cobre a bancada)

# criança de perfil — referencial LOCAL: origem no chão sob o quadril, unidades do cf_escoliose
QY = -205                                         # quadril
L_PERNA = 192
OMBRO = 168
LINHA_X, LINHA_Y0, LINHA_Y1 = -46, -198, -418     # linha-guia: atrás das costas, do quadril ao pescoço
BAG_X = -38                                       # a mochila encosta nas costas (referencial do tronco)
CHAO_BAG_X = -34                                  # mochila no chão, logo atrás das pernas (cabe na coluna)
FI_MAX, FLEX_MAX = 26.0, 14.0                     # A carregando: tronco à frente a partir do quadril
FI0, FLEX0 = 13.0, 5.0                            # quadro 0: a mochila gigante JÁ inclina (a capa mostra a dúvida)
CHEIA_OK = 0.38                                   # a mochila escolar certa, cheia (lombadas na tampa)
ESTRELAS = (("dor", (-24, -34)), ("costas", (-22, -108)), ("ombros", (26, -160)))


# ------------------------------------------------------------------ utilidades (cópias do piloto / cf_escoliose)
def _c(h, a=255):
    h = h.lstrip("#")
    return skia.ColorSetARGB(int(a), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _alfa(a):
    p = skia.Paint()
    p.setAlphaf(clamp(a))
    return p


def onda(t, t0, t1):
    """Meia senoide 0 -> 1 -> 0 entre t0 e t1 e ZERO fora (sin(pi) não é zero em ponto flutuante:
    um efeito "desligado" com alfa 1e-16 ainda custaria uma camada inteira por quadro)."""
    if t <= t0 or t >= t1:
        return 0.0
    return math.sin(math.pi * (t - t0) / (t1 - t0))


def pulo(t, t0, dur=0.32, alt=1.0):
    k = t - t0
    if k < 0 or k > dur:
        return 0.0
    return alt * math.sin(math.pi * k / dur)


def estrela(cv, px, py, s, cor, a, borda=None):
    p = skia.Path(); p.moveTo(px, py - s * 2); p.lineTo(px + s * 0.5, py - s * 0.5); p.lineTo(px + s * 2, py)
    p.lineTo(px + s * 0.5, py + s * 0.5); p.lineTo(px, py + s * 2); p.lineTo(px - s * 0.5, py + s * 0.5)
    p.lineTo(px - s * 2, py); p.lineTo(px - s * 0.5, py - s * 0.5); p.close()
    if borda:
        cv.drawPath(p, paint(borda, int(200 * clamp(a)), "stroke", 3))
    cv.drawPath(p, paint(cor, int(255 * clamp(a))))


def brilhos(cv, x, y, t, t0, n=8, raio=90, cor=OURO, dur=0.8, raio0=28, borda="#8A6512"):
    """Estrelinhas que NASCEM fora do objeto (raio0) e se afastam — nunca um nó escuro no centro."""
    k = t - t0
    if k < 0 or k > dur:
        return
    for i in range(n):
        ang = i * 2 * math.pi / n + 0.3
        d = lerp(raio0, raio, e_out(k / dur)) * (0.7 + 0.3 * ((i * 37) % 10) / 10)
        estrela(cv, x + d * math.cos(ang), y + d * math.sin(ang) * 0.8, 8 * (1 - k / dur) + 3, cor, 1 - k / dur,
                borda=borda)


def ponta(cv, x, y, ang, tam, cor, a):
    """Cabeça de seta em (x, y) apontando para `ang` (radianos)."""
    p = skia.Path()
    p.moveTo(x + tam * math.cos(ang), y + tam * math.sin(ang))
    p.lineTo(x + tam * 0.75 * math.cos(ang + 2.45), y + tam * 0.75 * math.sin(ang + 2.45))
    p.lineTo(x + tam * 0.75 * math.cos(ang - 2.45), y + tam * 0.75 * math.sin(ang - 2.45))
    p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))


def tracejada(cv, x0, y0, x1, y1, cor, a, larg=4, traco=16, vao=11, prog_=1.0, contorno=False):
    if a <= 0:
        return
    L = math.hypot(x1 - x0, y1 - y0)
    if L < 1:
        return
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    fim = L * prog_
    for passada in ((0, 1) if contorno else (1,)):
        d = 0.0
        while d < fim:
            e = min(d + traco, fim)
            if passada == 0:                                   # contorno escuro: lê sobre o creme e sobre a mochila
                cv.drawLine(x0 + ux * d, y0 + uy * d, x0 + ux * e, y0 + uy * e,
                            paint(NAVY, int(150 * a), "stroke", larg + 5))
            else:
                cv.drawLine(x0 + ux * d, y0 + uy * d, x0 + ux * e, y0 + uy * e, paint(cor, int(255 * a), "stroke", larg))
            d += traco + vao


def estrela_dor(cv, x, y, r, a):
    """Ícone de dor já aprovado (cf_escoliose) — aqui só sobre camiseta/alça."""
    if a <= 0:
        return
    p = skia.Path(); n = 9
    for i in range(2 * n):
        ang = -math.pi / 2 + i * math.pi / n
        rr = (r if i % 4 == 0 else r * 0.84) if i % 2 == 0 else r * 0.46
        (p.moveTo if i == 0 else p.lineTo)(x + rr * math.cos(ang), y + rr * math.sin(ang))
    p.close()
    cv.drawPath(p, paint(VERMELHO, int(110 * a), blur=12))
    cv.drawPath(p, paint(VERMELHO, int(230 * a)))
    cv.drawPath(p, paint("#FFD3D4", int(180 * a), "stroke", 2.5))


def _pele(cv, pth, x0, x1, a, linha=3.2):
    sh = skia.GradientShader.MakeLinear([skia.Point(x0, 0), skia.Point(x1, 0)],
                                        [_c(PELE_ESC), _c(PELE), _c(PELE_CL), _c(PELE), _c(PELE_ESC)],
                                        [0.0, 0.22, 0.5, 0.78, 1.0])
    cv.drawPath(pth, paint(PELE, int(255 * a), shader=sh))
    cv.drawPath(pth, paint(PELE_LINHA, int(230 * a), "stroke", linha))


def _camisa(cv, pth, x0, x1, a=1.0, linha=3.0, cores=None):
    """Camiseta (regata clara do cf_escoliose; `cores` = (cor, clara, escura, linha) para a 3ª criança)."""
    cor, cl, esc, lin = cores or (CAMISA, CAMISA_CL, CAMISA_ESC, CAMISA_LINHA)
    sh = skia.GradientShader.MakeLinear([skia.Point(x0, 0), skia.Point(x1, 0)],
                                        [_c(esc), _c(cor), _c(cl), _c(cor), _c(esc)], [0.0, 0.24, 0.5, 0.76, 1.0])
    cv.drawPath(pth, paint(cor, int(255 * a), shader=sh))
    cv.drawPath(pth, paint(lin, int(230 * a), "stroke", linha))


def manga(cv, x0, y0, x1, y1, larg, frac=0.3, a=1.0, cores=None):
    """Manga curta da camiseta: cobre o começo do braço (de (x0, y0) em direção a (x1, y1))."""
    ang = math.degrees(math.atan2(y1 - y0, x1 - x0)) - 90
    L = math.hypot(x1 - x0, y1 - y0) * frac
    cv.save(); cv.translate(x0, y0); cv.rotate(ang)
    w0, w1 = larg * 0.40, larg * 0.54
    p = skia.Path()
    p.moveTo(-w0, 0); p.cubicTo(-w0, -larg * 0.55, w0, -larg * 0.55, w0, 0)
    p.lineTo(w1, L - 7); p.quadTo(w1, L, w1 - 7, L); p.lineTo(-w1 + 7, L); p.quadTo(-w1, L, -w1, L - 7)
    p.close()
    _camisa(cv, p, -w1 - 2, w1 + 2, a, 2.6, cores)
    esc = (cores or (CAMISA, CAMISA_CL, CAMISA_ESC, CAMISA_LINHA))[2]
    cv.drawLine(-w1 + 7, L - 8, w1 - 7, L - 8, paint(esc, int(150 * a), "stroke", 3))
    cv.restore()


def capsula(cv, x0, y0, x1, y1, larg, a, mao=0.0):
    """Braço de desenho: tubo arredondado de (x0, y0) a (x1, y1), com mão redonda na ponta."""
    ang = math.degrees(math.atan2(y1 - y0, x1 - x0)) - 90
    L = math.hypot(x1 - x0, y1 - y0)
    cv.save(); cv.translate(x0, y0); cv.rotate(ang)
    p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect(-larg / 2, -larg / 2, larg / 2, L), larg / 2, larg / 2))
    if mao:
        m = skia.Path(); m.addOval(skia.Rect(-mao, L - mao * 1.3, mao, L + mao * 0.7))
        p = skia.Op(p, m, skia.PathOp.kUnion_PathOp) or p
    _pele(cv, p, -larg / 2 - 4, larg / 2 + 4, a, 2.6)
    cv.restore()


def path_braco(x0, y0, x1, y1, larg, mao):
    """O mesmo contorno da capsula(), já no referencial do desenho (para recortar o vão braço-cintura)."""
    ang = math.degrees(math.atan2(y1 - y0, x1 - x0)) - 90
    L = math.hypot(x1 - x0, y1 - y0)
    p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect(-larg / 2, -larg / 2, larg / 2, L), larg / 2, larg / 2))
    m = skia.Path(); m.addOval(skia.Rect(-mao, L - mao * 1.3, mao, L + mao * 0.7))
    p = skia.Op(p, m, skia.PathOp.kUnion_PathOp) or p
    mat = skia.Matrix(); mat.setRotate(ang); mat.postTranslate(x0, y0)
    p.transform(mat)
    return p


def chip_esq(cv, s, x, y, cor, a, tam=38, borda=None, esc=1.0):
    """Rótulo alinhado pela ESQUERDA (x); y = linha de base do texto (estilo do cf_escoliose)."""
    if a <= 0:
        return None
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    r = skia.Rect(x, y - tam * 1.05, x + lw + 40, y + tam * 0.34)
    cv.save(); cv.translate(x, r.centerY()); cv.scale(esc, esc); cv.translate(-x, -r.centerY())
    rr = skia.RRect.MakeRectXY(r, 16, 16)
    cv.drawRRect(rr, paint("#000000", int(80 * a), blur=8))
    cv.drawRRect(rr, paint(CHIP_FUNDO, int(240 * a)))
    cv.drawRRect(rr, paint(borda or cor, int(255 * a), "stroke", 3))
    texto(cv, s, x + 20, y, F_BLACK, tam, cor, int(255 * a), centro=False)
    cv.restore()
    return r


# ------------------------------------------------------------------ fundo e bancada (cópia do piloto)
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


# ------------------------------------------------------------------ a mochila (vista de LADO)
def dim_mochila(cheia):
    """(profundidade, altura) da mochila: fina (escolar) .. ENORME (maior que o tronco)."""
    return lerp(60, 170, cheia), lerp(158, 254, cheia)


def mochila_perfil(cv, cheia, a=1.0, contorno=0.0, t=0.0):
    """Mochila escolar de LADO. Origem = canto de baixo do lado das COSTAS; ela se estende para trás
    (-x) e para cima (-y). `cheia` 0 = fina, 1 = ENORME e estufada, com lombadas de livros saindo pela
    abertura de cima. `contorno` = tracejado dourado em volta (o objeto do mito, no quadro 0)."""
    if a <= 0:
        return
    d, h = dim_mochila(cheia)
    al = int(255 * a)
    r = min(40, d * 0.42)
    kl = prog(cheia, 0.25, 0.85)
    if kl > 0:                                                    # livros saindo por cima (atrás do corpo)
        for (fx, w, alt, rot), (cor, esc) in zip(((0.74, 30, 52, -9), (0.50, 34, 66, 3), (0.27, 26, 46, 11)), LIVROS):
            cv.save(); cv.translate(-d * fx, -h + 18); cv.rotate(rot)
            rr = skia.RRect.MakeRectXY(skia.Rect(-w / 2, -alt * kl, w / 2, 24), 5, 5)
            cv.drawRRect(rr, paint(cor, al))
            cv.drawRRect(rr, paint(esc, al, "stroke", 2.5))
            cv.drawLine(-w / 2 + 6, -alt * kl + 12, w / 2 - 6, -alt * kl + 12, paint(esc, int(200 * a), "stroke", 3))
            cv.restore()
    sh = skia.GradientShader.MakeLinear([skia.Point(-d - 10, 0), skia.Point(0, 0)],
                                        [_c(MOCH_ESC), _c(MOCH), _c(MOCH_CL), _c(MOCH), _c(MOCH_ESC)],
                                        [0.0, 0.18, 0.45, 0.8, 1.0])
    corpo = skia.Path()                                           # costas retas; o lado de fora ESTUFA
    b = 12 * cheia
    corpo.moveTo(-r * 0.4, 0)
    corpo.lineTo(-d + r, 0)
    corpo.cubicTo(-d - b, 0, -d - b, -h, -d + r, -h)
    corpo.lineTo(-r * 0.4, -h)
    corpo.quadTo(0, -h, 0, -h + r * 0.5)
    corpo.lineTo(0, -r * 0.5)
    corpo.quadTo(0, 0, -r * 0.4, 0)
    corpo.close()
    cv.drawPath(corpo, paint("#000000", int(60 * a), blur=8))
    cv.drawPath(corpo, paint(MOCH, al, shader=sh))
    cv.drawPath(corpo, paint(MOCH_ESC, al, "stroke", 3))
    # alça de mão no alto e zíper da abertura
    cv.drawArc(skia.Rect(-d * 0.62, -h - 26, -d * 0.30, -h + 14), 180, 180, False, paint(MOCH_ESC, al, "stroke", 7))
    cv.drawLine(-d + r * 0.6, -h + 14, -10, -h + 14, paint(MOCH_ESC, int(170 * a), "stroke", 3))
    # bolso de fora (no lado de trás): estufa com a mochila cheia
    bx0 = -d - lerp(6, 16, cheia)
    bolso = skia.RRect.MakeRectXY(skia.Rect(bx0, -h * 0.60, -d + d * lerp(0.62, 0.40, cheia), -h * 0.10), 20, 20)
    cv.drawRRect(bolso, paint(MOCH_CL, al))
    cv.drawRRect(bolso, paint(MOCH_ESC, al, "stroke", 3))
    cv.drawLine(bx0 + 12, -h * 0.60 + 16, -d + d * lerp(0.62, 0.40, cheia) - 12, -h * 0.60 + 16,
                paint(MOCH_ESC, int(200 * a), "stroke", 3))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(bx0 + 14, -h * 0.60 + 10, bx0 + 22, -h * 0.60 + 34), 3, 3),
                 paint("#E6E1F2", al))
    if contorno > 0:                                              # o objeto do mito (quadro 0)
        m = 18 + 6 * math.sin(t * 9)
        rr = skia.RRect.MakeRectXY(skia.Rect(-d - b - 22 - m * 0.3, -h - 60 * kl - m, 8 + m * 0.3, m * 0.6), 30, 30)
        pt = paint(OURO, int(255 * contorno), "stroke", 7)
        pt.setPathEffect(skia.DashPathEffect.Make([22, 14], -t * 60))
        cv.drawRRect(rr, paint(NAVY, int(110 * contorno), "stroke", 12))
        cv.drawRRect(rr, pt)


def alca(cv, bot, top, a, ouro=0.0):
    """Alça da mochila no referencial do TRONCO: sai do alto da mochila, passa por cima do ombro, desce
    pela frente do peito e volta por baixo do braço até a base da mochila."""
    if a <= 0:
        return
    p = skia.Path()
    p.moveTo(BAG_X + 2, top + 34)
    p.cubicTo(-30, -198, -2, -204, 20, -192)
    p.cubicTo(38, -180, 42, -150, 36, -124)
    p.cubicTo(28, -96, -4, (bot - 30) * 0.5 - 60, BAG_X + 4, bot - 26)
    cv.drawPath(p, paint("#000000", int(50 * a), "stroke", 18, blur=4))
    cv.drawPath(p, paint(MOCH_ESC, int(255 * a), "stroke", 15))
    cv.drawPath(p, paint(MOCH, int(255 * a), "stroke", 7))
    if ouro > 0:
        cv.drawPath(p, paint(OURO, int(150 * ouro * a), "stroke", 26, blur=8))
        cv.drawPath(p, paint(OURO, int(255 * ouro * a), "stroke", 9))


# ------------------------------------------------------------------ a troca da mochila (cena 6: "Mochila cheia")
def centro_bag_chao(st):
    """Centro (tela) da mochila de A no chão — onde a troca solta os brilhos."""
    d, h = dim_mochila(st["cheia"])
    return st["x"] + st["s"] * (CHAO_BAG_X - d * 0.5), PISO + st["s"] * (-h * 0.5)


# ------------------------------------------------------------------ criança de perfil (cf_escoliose, adaptada)
def perna_perfil(cv, ang, a, longe=False):
    """Perna de perfil (olhando para a direita), presa no quadril; o pé fica plano no chão."""
    cv.save(); cv.rotate(ang)
    p = skia.Path()
    p.moveTo(-34, -8)
    p.cubicTo(-37, 40, -26, 80, -23, 100)
    p.cubicTo(-22, 120, -31, 148, -20, L_PERNA)
    p.lineTo(15, L_PERNA)
    p.cubicTo(18, 150, 20, 118, 22, 100)
    p.cubicTo(25, 80, 34, 40, 33, -8)
    p.close()
    _pele(cv, p, -38, 36, a)
    if longe:
        cv.drawPath(p, paint("#5A3A2E", int(60 * a)))
    cv.drawArc(skia.Rect(8, 88, 26, 112), -60, 120, False, paint(PELE_LINHA, int(140 * a), "stroke", 3))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-39, -14, 37, 62), 16, 16), paint(SHORT, int(255 * a)))
    cv.drawLine(-34, 56, 32, 56, paint(SHORT_ESC, int(200 * a), "stroke", 3))
    cv.translate(0, L_PERNA); cv.rotate(-ang)
    f = skia.Path()
    f.moveTo(-20, -10); f.cubicTo(-26, 4, -20, 12, -8, 12); f.lineTo(48, 12)
    f.cubicTo(62, 12, 62, -2, 50, -6); f.cubicTo(32, -10, 16, -14, 15, -22); f.lineTo(-19, -22); f.close()
    _pele(cv, f, -26, 62, a)
    if longe:
        cv.drawPath(f, paint("#5A3A2E", int(60 * a)))
    cv.restore()


def _rot(fi, x, y):
    r = math.radians(fi)
    return x * math.cos(r) - y * math.sin(r), x * math.sin(r) + y * math.cos(r)


def no_tronco(st, x, y):
    """Ponto do referencial do tronco -> referencial local da criança."""
    rx, ry = _rot(st["fi"], x, y)
    return rx, QY + st["dip"] + ry


def corpo(cv, st):
    """Pernas, tronco (inclina a partir do quadril), alça, cabeça e braço — o CONTORNO do corpo, sem osso."""
    fi, flex, dip = st["fi"], st["flex"], st["dip"]
    hy = QY + dip
    k = (-hy) / (-QY)                                              # o quadril desce, o pé fica no chão
    for dx, ang, longe in ((-6, st["ang_tras"], True), (2, st["ang_frente"], False)):
        cv.save(); cv.translate(dx, hy); cv.scale(1, k); perna_perfil(cv, ang, 1.0, longe=longe); cv.restore()
    cv.drawCircle(-2, hy - 4, 40, paint(SHORT))
    cv.save(); cv.translate(0, hy); cv.rotate(fi)
    tr = skia.Path()
    tr.moveTo(-40, 6)
    tr.cubicTo(-46, -44, -39, -124, -35, -160)
    tr.cubicTo(-33, -180, -13, -190, 6, -188)
    tr.cubicTo(26, -186, 38, -174, 38, -152)
    tr.cubicTo(42, -108, 34, -58, 36, -22)
    tr.cubicTo(37, 0, 32, 8, 28, 10)
    tr.close()
    pesc = skia.Path(); pesc.addRRect(skia.RRect.MakeRectXY(skia.Rect(-10, -210, 18, -176), 12, 12))
    _pele(cv, pesc, -12, 20, 1.0)
    _camisa(cv, tr, -46, 42)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-45, -54, 41, 18), 20, 20), paint(SHORT))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-45, -54, 41, -36), 12, 12), paint(SHORT_CL))
    a_alca = st["alca_a"]
    if a_alca > 0:
        bot = st["bag_bot"] + st["sink"]
        alca(cv, bot, bot - dim_mochila(st["cheia"])[1], a_alca, st["alca_ouro"])
    cv.save(); cv.translate(4, -196); cv.rotate(flex)
    cx, cy = 8, -38
    cv.drawCircle(cx + 3, cy + 6, 44, paint("#000000", 50, blur=8))
    cab = skia.Path(); cab.addCircle(cx, cy, 42)
    _pele(cv, cab, cx - 44, cx + 44, 1.0)
    cv.save(); cv.clipPath(cab, skia.ClipOp.kIntersect, True)
    cv.drawCircle(cx - 19, cy - 17, 44, paint(CABELO))
    cv.drawCircle(cx + 12, cy - 34, 19, paint(CABELO))
    cv.restore()
    cv.restore()
    cv.restore()
    ox, oy = no_tronco(st, 0, -OMBRO)                              # braço: sempre pende para o chão
    caida = lerp(7, 3, clamp(fi / 30))
    bx, by_ = ox + 190 * math.sin(math.radians(caida)), oy + 190 * math.cos(math.radians(caida))
    capsula(cv, ox, oy, bx, by_, 27, 1.0, mao=15)
    manga(cv, ox, oy, bx, by_, 42, frac=0.3)


def _halo_paint(forca):
    """Camada que pinta a silhueta de ouro e a engorda (o "contorno dourado" rápido da virada)."""
    p = skia.Paint()
    cf = skia.ColorFilters.Blend(C(OURO), skia.BlendMode.kSrcIn)
    p.setImageFilter(skia.ImageFilters.ColorFilter(cf, skia.ImageFilters.Dilate(7, 7)))
    p.setAlphaf(clamp(forca))
    return p


def bag_pose(st):
    """-> (x, y, rot) LOCAL da origem da mochila: nas costas (gira com o tronco) ou no chão."""
    bx, by = no_tronco(st, BAG_X, st["bag_bot"] + st["sink"])
    u = st["u_chao"]
    x = lerp(bx, CHAO_BAG_X, u)
    y = lerp(by, 0.0, u) - st["arco"] * math.sin(math.pi * u) - st["pulinho"]
    return x, y, lerp(st["fi"], 0.0, u) + st["giro"] * math.sin(math.pi * u)


def linha_guia(cv, st):
    """Linha tracejada dourada, RETA, rente às costas (do quadril ao pescoço). Só existe com as costas
    LIVRES (a mochila no chão): lê-se "reto" — nunca atravessa a mochila. Sem prumo, marcas ou números."""
    a = st["linha_a"]
    if a <= 0:
        return
    if st["flash"] > 0:
        cv.drawLine(LINHA_X, LINHA_Y0, LINHA_X, LINHA_Y1, paint(OURO, int(200 * st["flash"] * a), "stroke", 22, blur=10))
    tracejada(cv, LINHA_X, LINHA_Y0, LINHA_X, LINHA_Y1, OURO, a, larg=5, traco=18, vao=12, contorno=True)


def crianca(cv, st, t, T):
    """Uma coluna do teste, no referencial local (o chamador posiciona e escala)."""
    cv.drawOval(skia.Rect(-120, -12, 150, 16), paint("#6B4A2A", 70, blur=10))   # sombra no chão
    linha_guia(cv, st)                                              # a linha passa ATRÁS da mochila (nunca a risca)
    if st["bag_a"] > 0:                                            # a mochila fica atrás do corpo
        x, y, rot = bag_pose(st)
        cv.save(); cv.translate(x, y); cv.rotate(rot)
        mochila_perfil(cv, st["cheia"], st["bag_a"], st["contorno"], t)
        cv.restore()
    if st["halo"] > 0:
        cv.saveLayer(skia.Rect(-150, -540, 190, 30), _halo_paint(st["halo"]))   # só a caixa da criança
        corpo(cv, st)
        cv.restore()
    corpo(cv, st)
    for chave, (px, py) in ESTRELAS:                                # dor: só na criança A, só na cena 4
        a_e = st["estrelas"].get(chave, 0.0)
        if a_e > 0:
            x, y = no_tronco(st, px, py)
            k = prog(t, T[chave], T[chave] + 0.25)
            r = 25 * (e_back(k) if k < 1 else 1.0) * (1 + 0.06 * math.sin(t * 9))
            estrela_dor(cv, x, y, max(1.0, r), a_e)


# ------------------------------------------------------------------ estado das duas colunas (tudo a partir de T)
def andando(t, T):
    """1 enquanto as crianças "carregam" (passo pesado no lugar); param em "Agora"."""
    return 1 - prog(t, T["agora"] - 0.05, T["agora"] + 0.2)


def estado(nome, t, T):
    w = andando(t, T)
    ritmo = 0.5 - 0.5 * math.cos(2 * math.pi * t / 0.6)            # um passo a cada 0,6 s
    fase = math.sin(math.pi * t / 0.6)
    st = {"dip": 5 * ritmo * w + 7 * pulo(t, T["mochila"], 0.4),
          "ang_tras": 6 + 3.5 * fase * w, "ang_frente": -4 - 3.5 * fase * w,
          "flex": 0.0, "sink": 10 * pulo(t, T["mochila"], 0.45), "pulinho": 0.0, "giro": 0.0, "arco": 30.0,
          "contorno": prog(t, T["assim"] - 0.05, T["assim"] + 0.12) * (1 - prog(t, T["vamos"] - 0.1, T["vamos"] + 0.2)),
          "estrelas": {}, "flash": 0.0, "alca_ouro": 0.0, "halo": 0.0, "bag_a": 1.0}
    u_clone = e_inout(prog(t, T["prova"] - 0.05, T["prova"] + 0.5))
    if nome == "A":
        st["x"], st["s"], st["a"] = lerp(X0, XA, u_clone), lerp(S0, S1, u_clone), 1.0
    else:
        st["x"], st["s"] = lerp(X0, XB, u_clone), lerp(S0, S1, u_clone)
        st["a"] = 1.0 if t >= T["prova"] - 0.05 else 0.0
    m3, tira, m4 = T["mochila3"], T["tira"], T["mochila4"]
    t_volta0, t_volta1 = T["postura2"] - 0.08, T["volta"] + 0.12     # "a postura VOLTA": endireita com mola
    troca = e_inout(prog(t, m4 + 0.05, m4 + 0.45))                   # "Mochila cheia": a mochila certa
    if nome == "A":
        st["dip"] += 9 * pulo(t, T["exagerado"], 0.4) + 6 * pulo(t, T["carrega"], 0.4)
        inc = e_inout(prog(t, T["exagerado"], T["carrega"] + 0.2))
        fi, flex = lerp(FI0, FI_MAX, inc), lerp(FLEX0, FLEX_MAX, inc)
        volta = prog(t, t_volta0, t_volta1)
        if volta > 0:
            r = e_back(volta, 2.0)
            fi, flex = lerp(FI_MAX, 0, r), lerp(FLEX_MAX, 0, r)
        st["fi"], st["flex"] = fi, flex
        st["sink"] += 12 * e_out(prog(t, T["exagerado"], T["exagerado"] + 0.2))
        st["cheia"] = lerp(1.0, CHEIA_OK, troca)                      # a gigante ENCOLHE para a escolar cheia
        sai = prog(t, tira - 0.02, tira + 0.25)                      # com esforço: sobe um pouco e CAI no chão
        st["u_chao"] = sai * sai
        st["arco"] = 40.0
        st["pulinho"] = 22 * pulo(t, T["doer1"], 0.35) + 10 * pulo(t, m4 + 0.05, 0.3)
        # "Pode doer": a mochila pesada (no chão) ganha o contorno dourado — a dor vem DELA
        st["contorno"] = max(st["contorno"], prog(t, T["doer1"] - 0.05, T["doer1"] + 0.12)
                             * (1 - prog(t, T["escoliose"] - 0.05, T["escoliose"] + 0.2)))
        for chave, _p in ESTRELAS:
            st["estrelas"][chave] = prog(t, T[chave] - 0.02, T[chave] + 0.1) * (1 - prog(t, m3 - 0.02, m3 + 0.12))
    else:
        dir_b = e_back(prog(t, T["mochila2"] + 0.1, T["mochila2"] + 0.55))
        st["fi"], st["flex"] = lerp(FI0, 0, dir_b), lerp(FLEX0, 0, dir_b)
        st["cheia"] = (1 - e_inout(prog(t, T["mochila2"] - 0.05, T["mochila2"] + 0.35))) * (1 - troca) + CHEIA_OK * troca
        st["u_chao"] = e_inout(prog(t, tira, tira + 0.32))
        st["arco"] = 24.0
    st["sink"] *= 1 - prog(t, tira - 0.02, tira + 0.1)
    volta_costas = e_inout(prog(t, T["cheia"] - 0.05, T["cheia"] + 0.35))   # "cheia": as duas voltam às costas
    if volta_costas > 0:
        st["u_chao"] = 1 - volta_costas
        st["arco"] = 50.0
    st["bag_bot"] = lerp(-40, 40, st["cheia"])
    st["alca_a"] = 1 - clamp(st["u_chao"] * 4)
    st["alca_ouro"] = onda(t, T["cheia"] + 0.3, T["cheia"] + 0.85)
    # a linha-guia só com as costas LIVRES: entra quando a postura volta, sai antes de a mochila voltar
    st["linha_a"] = prog(t, t_volta0, t_volta0 + 0.3) * (1 - prog(t, m4, m4 + 0.3))
    fl = onda(t, T["volta"] - 0.02, T["volta"] + 0.5) if nome == "A" else 0.0
    st["flash"] = max(fl, 0.8 * onda(t, T["prova2"], T["prova2"] + 0.5))
    st["halo"] = 0.85 * onda(t, T["volta"], T["volta"] + 0.36) if nome == "A" else 0.0
    return st


def tela_local(st, x, y):
    return st["x"] + st["s"] * x, PISO + st["s"] * y


# ------------------------------------------------------------------ peças de interface do teste
def paineis(cv, t, T):
    """Em "prova" a bancada vira duas colunas iguais (o teste justo)."""
    a = prog(t, T["prova"], T["prova"] + 0.4)
    if a <= 0:
        return
    for nome in ("A", "B"):
        r = skia.RRect.MakeRectXY(skia.Rect(*PAINEIS[nome]), 28, 28)
        cv.drawRRect(r, paint(PAINEL, int(255 * a)))
        cv.drawRRect(r, paint(PAINEL_BORDA, int(255 * a), "stroke", 3))


def veu_foco(cv, t, T):
    """'Do outro lado': a coluna B ganha foco; a A fica sob um véu creme por ~1 s."""
    d = 0.5 * prog(t, T["outro"] - 0.12, T["outro"] + 0.1) * (1 - prog(t, T["mochila2"] + 0.1, T["mochila2"] + 0.4))
    if d <= 0:
        return
    x0, y0, x1, y1 = PAINEIS["A"]
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0 - 2, y0 - 2, x1 + 2, y1 + 2), 28, 28), paint(BANCADA, int(255 * d)))


def rotulo(cv, s, x, y, a, esc=1.0):
    """Rótulo da condição acima da coluna (navy, texto branco), com PULO de escala (cópia do piloto)."""
    if a <= 0 or esc <= 0.01:
        return
    lw = larg_texto(s, F_BLACK, 36)
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 22, -26, lw / 2 + 22, 26), 26, 26)
    cv.drawRRect(rr, paint("#000000", int(70 * a), blur=8))
    cv.drawRRect(rr, paint(NAVY, int(240 * a)))
    cv.drawRRect(rr, paint("#5E7186", int(255 * a), "stroke", 3))
    texto(cv, s, 0, 13, F_BLACK, 36, "#FFFFFF", int(255 * a))
    cv.restore()


def rotulos(cv, t, T):
    some = 1 - prog(t, T["veredito"] - 0.12, T["veredito"] + 0.05)
    for nome, s, dt in (("A", R_PESADA, 0.0), ("B", R_LEVE, 0.08)):
        p = prog(t, T["leve"] - 0.05 + dt, T["leve"] + 0.25 + dt)
        rotulo(cv, s, X_ROT[nome], Y_ROT, clamp(p * 5) * some, esc=max(0.01, e_back(p)) if p < 1 else 1.0)


def claquete(cv, x, y, fecha, a):
    """Claquete do teste: a haste bate em "prova" (cópia do piloto)."""
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


# ------------------------------------------------------------------ veredito (topo): a aposta MITO | VERDADE
def t_card_sai(T):
    return T["mochila4"] - 0.3


def cartao_pose(t, T):
    tv = T["veredito"]
    if t < tv - 0.05:
        return None
    u = e_back(prog(t, tv - 0.05, tv + 0.35), 1.1)
    dy = lerp(-460, 0, u)
    sai = prog(t, t_card_sai(T), t_card_sai(T) + 0.35) ** 3          # sobe SEM recuo (não desce sobre a cena)
    return dy - 520 * sai, 1.0 if sai < 1 else 0.0


def roleta(T):
    """6 tiques (chegadas do cursor): começa em VERDADE, alterna e DESACELERA; o 6º ASSENTA em MITO ~0,3 s
    antes da palavra e fica (o carimbo bate em "mito"). Sem finta para VERDADE no fim: o leitor às cegas
    leu a parada em VERDADE como resposta ("pareceu que o vídeo mudou de ideia")."""
    t0, t5 = T["veredito"] + 0.3, T["mito"] - 0.32
    return [lerp(t0, t5, (k / 5) ** 1.6) for k in range(6)]


def cursor(t, T):
    """-> (x, alfa, pulso) do CURSOR da roleta, ou None. O cursor é um aro dourado SEM preenchimento que
    corre entre MITO e VERDADE: nenhum dos dois botões acende antes do golpe. Cada movimento TERMINA no
    tique (o som cai na chegada); depois do último, fica em MITO até o golpe."""
    tiques = roleta(T)
    xs = (SLOT_X["verdade"], SLOT_X["mito"])                       # k par = VERDADE, k ímpar = MITO (k=5)
    if t < tiques[0] - 0.14 or t >= T["mito"]:
        return None
    if t < tiques[0]:
        return xs[0], prog(t, tiques[0] - 0.14, tiques[0]), 0.0
    k = max(i for i, ti in enumerate(tiques) if ti <= t)
    x = xs[k % 2]
    if k + 1 < len(tiques):
        tn = tiques[k + 1]
        dm = min(0.1, 0.6 * (tn - tiques[k]))
        u = prog(t, tn - dm, tn)
        if u > 0:
            x = lerp(xs[k % 2], xs[(k + 1) % 2], e_inout(u))
    return x, 1.0, 1 - clamp((t - tiques[k]) / (0.2 if k + 1 == len(tiques) else 0.12))


def desenha_cursor(cv, x, a, pulso):
    if a <= 0:
        return
    esc = 1 + 0.05 * pulso
    cv.save(); cv.translate(x, SLOT_Y); cv.scale(esc, esc)
    w, h = SLOT_W / 2 + 12, SLOT_H / 2 + 12
    rr = skia.RRect.MakeRectXY(skia.Rect(-w, -h, w, h), 30, 30)
    cv.drawRRect(rr, paint(OURO, int(150 * a), "stroke", 14, blur=8))
    cv.drawRRect(rr, paint(NAVY, int(255 * a), "stroke", 11))
    cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 6))
    cv.restore()


def opcao(cv, s, x, a, sel, pulso, apagado, aceso=0.0):
    """Uma das duas opções da aposta: vazia (tracejada) ou a ESCOLHIDA (dourada, só no golpe).
    `aceso` = o cursor está por cima: só o texto ganha força (o fundo não muda)."""
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
    texto(cv, s, 0, TAM_SLOT * 0.36, F_BLACK, TAM_SLOT, NAVY,
          int(a * lerp(165, 255, max(sel, aceso)) * (1 - 0.65 * apagado)))
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
    for _ in range(30):
        cv.drawCircle(rng.uniform(-lw / 2 - 28, lw / 2 + 28), rng.uniform(-tam * 0.5 - 14, tam * 0.5 + 14),
                      rng.uniform(1.5, 4.0), paint(CARTAO, int(170 * a)))
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
    tm = T["mito"]
    bateu = t >= tm
    apaga = prog(t, tm, tm + 0.25)
    cur = cursor(t, T)
    vivo = prog(t, T["veredito"] + 0.15, T["veredito"] + 0.3)      # as duas opções com a MESMA força: só o aro anda
    opcao(cv, R_MITO, SLOT_X["mito"], 1.0, 1.0 * bateu, 1 - clamp((t - tm) / 0.12) if bateu else 0.0, 0.0,
          aceso=vivo)
    opcao(cv, R_VERDADE, SLOT_X["verdade"], 1.0, 0.0, 0.0, apaga, aceso=vivo)
    if cur:
        desenha_cursor(cv, *cur)
    if bateu:
        k = t - tm
        esc = lerp(1.25, 1.0, e_out(clamp(k / 0.12))) * (1 + 0.1 * pulo(t, T["escoliose"], 0.4))
        marca_carimbo(cv, R_MITO, MARCA[0], MARCA[1], -4, 1.0, esc=esc)
    cv.restore()


def carimbo_obj(cv, x, y, rot, esc, a, esmaga=0.0, larg=188):
    """Carimbo de madeira; (x, y) = centro da borracha (LISA: sem texto gravado). Cópia do piloto."""
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
    """-> (x, y, rot, esc, a, esmaga, larg): o carimbo só aparece no golpe — desce do alto à direita,
    bate em MITO na palavra e sobe em 0,16 s (não paira sobre o texto do cartão)."""
    tm = T["mito"]
    t_in = tm - 0.18
    if t < t_in or t > tm + 0.2:
        return None
    larg = larg_marca()
    alvo = (MARCA[0], MARCA[1], -4.0)
    if t < tm:
        u = clamp((t - t_in) / 0.18) ** 2
        x, y, rot = lerp(760, alvo[0], u), lerp(-320, alvo[1], u), lerp(22.0, alvo[2], u)
        return x, y, rot, 1.0, 1.0, 0.0, larg
    esmaga = math.sin(math.pi * clamp((t - tm) / 0.08))
    w = e_out(prog(t, tm + 0.04, tm + 0.2))
    x, y, rot = lerp(alvo[0], 820, w), lerp(alvo[1], -440, w), lerp(alvo[2], 20.0, w)
    return x, y, rot, 1.0, 1.0, esmaga, larg


def impacto(cv, t, T):
    k = t - T["mito"]
    if k < 0 or k > 0.35:
        return
    mx, my = MARCA
    u = e_out(k / 0.35); a = 1 - k / 0.35
    for i in range(12):
        ang = i * 2 * math.pi / 12 + 0.2
        r0, r1 = 150 + 50 * u, 175 + 95 * u
        ex, ey = math.cos(ang), math.sin(ang) * 0.42
        cv.drawLine(mx + r0 * ex, my + r0 * ey, mx + r1 * ex, my + r1 * ey, paint(OURO, int(230 * a), "stroke", 7))


def tremor_cam(t, T):
    k = t - T["mito"]
    if 0 <= k < 0.3:
        return 10 * math.sin(k * 70) * (1 - k / 0.3)
    return 0.0


# ------------------------------------------------------------------ o jeito que vale (a regra)
def cartao_regra(cv, t, T):
    t0 = T["dez"] - 0.08
    k = prog(t, t0, t0 + 0.32)
    if k <= 0:
        return
    sai = prog(t, T["escoliose2"] - 0.32, T["escoliose2"] - 0.06)
    a = clamp(k * 3) * (1 - sai)
    if a <= 0:
        return
    esc = (e_back(k) if k < 1 else 1.0) * (1 - 0.08 * sai)
    x0, y0, x1, y1 = REGRA
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    cv.save(); cv.translate(cx, cy); cv.scale(esc, esc); cv.translate(-cx, -cy)
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 28, 28)
    sombra(cv, x0, y0 + 12, x1, y1 + 12, 28, 18, 140 * a / 255)
    cv.drawRRect(rr, paint(CARTAO, int(255 * a)))
    cv.drawRRect(rr, paint(NAVY, int(255 * a), "stroke", 5))
    texto(cv, R_REGRA1, CX, y0 + 92, F_BLACK, 66, NAVY, int(255 * a))
    # "DO PESO DA CRIANÇA" entra JUNTO (o leitor às cegas ficou sem saber "15 % de quê"); pulsa em "peso"
    e2 = 1 + 0.08 * pulo(t, T["peso2"], 0.4)
    cv.save(); cv.translate(CX, y0 + 150); cv.scale(e2, e2)
    texto(cv, R_REGRA2, 0, 0, F_BLACK, 46, "#2F5A86", int(255 * a))
    cv.restore()
    cv.restore()


# ------------------------------------------------------------------ o asterisco: a 3ª criança, de costas
# desenho no referencial do cf_escoliose.costas_em_pe (centro x=540, chão y=1060), ADAPTADO: camiseta
# LARANJA, sem mochila, ombro DIREITO (da tela) mais alto e o vão braço-cintura maior do lado esquerdo.
BR_E = ((449, 700), (412, 888))
BR_D = ((631, 666), (668, 858))
OMB_E_TOPO, OMB_D_TOPO = (475, 653), (602, 628)                 # alto de cada ombro (onde a linha passa)
CINT_Y0, CINT_Y1 = (716, 806), (688, 806)                       # faixa do vão (esq., dir.) até o shorts
X3, PISO3, K3 = 290, 1100, 1.12                                 # onde ela fica no cartão (terço esquerdo)


def tronco3():
    tr = skia.Path()
    tr.moveTo(462, 832)
    tr.cubicTo(500, 798, 486, 744, 449, 698)                    # cintura MAIS marcada (vão maior)
    tr.cubicTo(438, 670, 468, 650.5, 516, 639.5)               # a linha dos ombros INCLINA para a direita
    tr.lineTo(564, 630.5)
    tr.cubicTo(612, 623.5, 642, 632, 631, 664)                 # ombro direito ~25 mais alto
    tr.cubicTo(622, 700, 622, 778, 620, 832)                    # lado direito quase reto (vão menor)
    tr.close()
    return tr


def vao3(lado):
    """Região entre o braço e a cintura (recorte exato: faixa - braço - tronco)."""
    (xa, ya), (xb, yb) = BR_E if lado == "E" else BR_D
    y0, y1 = CINT_Y0 if lado == "E" else CINT_Y1

    def bx(y):
        return lerp(xa, xb, (y - ya) / (yb - ya))
    q = skia.Path(); q.moveTo(bx(y0), y0); q.lineTo(bx(y1), y1); q.lineTo(540, y1); q.lineTo(540, y0); q.close()
    r = skia.Op(q, path_braco(xa, ya, xb, yb, 29, 15), skia.PathOp.kDifference_PathOp) or q
    return skia.Op(r, tronco3(), skia.PathOp.kDifference_PathOp) or r


_VAOS = {}


def costas3(cv, a):
    """De pé, vista de costas (camiseta laranja, shorts azul), sem mochila, sem nada por dentro do corpo."""
    if a <= 0:
        return
    cores = (CAM3, CAM3_CL, CAM3_ESC, CAM3_LINHA)
    cv.drawOval(skia.Rect(420, 1048, 660, 1076), paint("#000000", 90, blur=10))
    for (x0, y0), (x1, y1) in (BR_E, BR_D):                     # braços soltos ao lado do corpo
        capsula(cv, x0, y0, x1, y1, 29, 1.0, mao=15)
        manga(cv, x0, y0, x1, y1, 44, frac=0.3, cores=cores)
    for xc in (512, 568):
        p = skia.Path()
        p.moveTo(xc - 33, 858)
        p.cubicTo(xc - 35, 900, xc - 25, 940, xc - 23, 958)
        p.cubicTo(xc - 21, 985, xc - 19, 1020, xc - 18, 1040)
        p.lineTo(xc + 18, 1040)
        p.cubicTo(xc + 19, 1020, xc + 21, 985, xc + 23, 958)
        p.cubicTo(xc + 25, 940, xc + 35, 900, xc + 33, 858)
        p.close()
        _pele(cv, p, xc - 38, xc + 38, 1.0)
        cal = skia.Path(); cal.addOval(skia.Rect(xc - 24, 1026, xc + 24, 1064))
        _pele(cv, cal, xc - 26, xc + 26, 1.0)
        cv.drawArc(skia.Rect(xc - 14, 948, xc + 14, 968), 200, 140, False, paint(PELE_LINHA, 140, "stroke", 3))
    pesc = skia.Path(); pesc.addRRect(skia.RRect.MakeRectXY(skia.Rect(523, 608, 557, 662), 12, 12))
    _pele(cv, pesc, 519, 561, 1.0)
    _camisa(cv, tronco3(), 438, 646, cores=cores)
    sh = skia.Path()
    sh.moveTo(454, 806); sh.lineTo(626, 806)
    sh.cubicTo(640, 830, 644, 868, 636, 896)
    sh.cubicTo(612, 908, 570, 906, 548, 894); sh.lineTo(540, 880); sh.lineTo(532, 894)
    sh.cubicTo(510, 906, 468, 908, 444, 896)
    sh.cubicTo(436, 868, 440, 830, 454, 806); sh.close()
    cv.drawPath(sh, paint("#000000", 60, blur=8))
    cv.drawPath(sh, paint(SHORT))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(450, 802, 630, 826), 12, 12), paint(SHORT_CL))
    cv.drawLine(540, 836, 540, 874, paint(SHORT_ESC, 255, "stroke", 3))
    for s in (-1, 1):                                           # orelhas
        orl = skia.Path(); orl.addOval(skia.Rect(540 + s * 38 - 8, 572, 540 + s * 38 + 8, 598))
        _pele(cv, orl, 540 + s * 38 - 9, 540 + s * 38 + 9, 1.0, 2.2)
    cab = skia.Path(); cab.addCircle(540, 580, 40)
    _pele(cv, cab, 498, 582, 1.0)
    cv.save(); cv.clipPath(cab, skia.ClipOp.kIntersect, True)    # nuca: o cabelo cobre quase tudo
    cv.drawRect(skia.Rect(496, 536, 584, 596), paint(CABELO, 255))
    cv.drawOval(skia.Rect(506, 572, 574, 612), paint(CABELO, 255))
    cv.restore()


def tela3(x, y):
    """Ponto do desenho da 3ª criança -> tela (dentro do cartão)."""
    return X3 + (x - 540) * K3, PISO3 + (y - 1060) * K3


def guia(cv, x0, y0, x1, y1, a):
    cv.drawLine(x0, y0, x1, y1, paint(OURO, int(230 * a), "stroke", 3))
    cv.drawCircle(x0, y0, 6, paint(OURO, int(255 * a)))


def cartao_asterisco(cv, t, T):
    """'E a escoliose?': véu sobre a bancada e um cartão escuro que SOBE no lugar (recortado nela: nunca
    invade o karaokê). Dentro, a 3ª criança de costas e os sinais; recolhe (some e encolhe) antes da CTA."""
    t0 = T["escoliose2"] - 0.08
    k = prog(t, t0, t0 + 0.34)
    if k <= 0:
        return
    sai = e_inout(prog(t, T["manda"] - 0.4, T["manda"] - 0.05))
    a = clamp(k * 2.5) * (1 - sai)
    if a <= 0:
        return
    cv.save()
    cv.clipRRect(skia.RRect.MakeRectXY(skia.Rect(*BANC), 34, 34), skia.ClipOp.kIntersect, True)
    cv.drawRect(skia.Rect(*BANC), paint(NAVY, int(140 * a)))                        # véu
    dy = 520 * (1 - e_out(k))
    esc = 1 - 0.06 * sai
    cv.translate(CX, 800); cv.scale(esc, esc); cv.translate(-CX, -800 + dy)
    x0, y0, x1, y1 = ASTER
    sombra(cv, x0, y0, x1, y1, 34, 20, 120 * a / 255)
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 34, 34)
    cv.drawRRect(rr, paint(NAVY, int(255 * a)))
    cv.drawRRect(rr, paint(OURO, int(200 * a), "stroke", 3))
    # faixa de título
    lw = larg_texto(R_ESC, F_BLACK, 44)
    pf = 1 + 0.06 * pulo(t, T["escoliose2"] + 0.2, 0.35)
    cv.save(); cv.translate(CX, 438); cv.scale(pf, pf)
    pill = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 34, -31, lw / 2 + 34, 31), 31, 31)
    cv.drawRRect(pill, paint(OURO, int(255 * a)))
    texto(cv, R_ESC, 0, 16, F_BLACK, 44, NAVY, int(255 * a))
    cv.restore()
    # a 3ª criança (de costas, sem mochila, camiseta de outra cor)
    cv.save(); cv.translate(X3, PISO3); cv.scale(K3, K3); cv.translate(-540, -1060)
    if a < 1:
        cv.saveLayer(None, _alfa(a))
    else:
        cv.save()
    costas3(cv, 1.0)
    # vãos braço-cintura (contorno dourado, um visivelmente maior)
    kv = prog(t, T["cintura"] - 0.05, T["cintura"] + 0.25)
    if kv > 0:
        for lado in ("E", "D"):
            if lado not in _VAOS:
                _VAOS[lado] = vao3(lado)
            pv = _VAOS[lado]
            pulsa = 1 + 0.6 * pulo(t, T["assimetrica"], 0.4)
            cv.drawPath(pv, paint("#FFD76E", int(55 * kv)))
            cv.drawPath(pv, paint(OURO, int(255 * kv), "stroke", 4.5 * pulsa))
    # linha dos ombros (inclinada) com a setinha no ombro mais alto
    ko = prog(t, T["ombro"] - 0.05, T["ombro"] + 0.4)
    if ko > 0:
        (xl, yl), (xr, yr) = OMB_E_TOPO, OMB_D_TOPO
        m = (yr - yl) / (xr - xl)
        xa_, xb_ = xl - 70, xr + 74
        ya_, yb_ = yl + m * (xa_ - xl) - 8, yl + m * (xb_ - xl) - 8
        tracejada(cv, xa_, ya_, xb_, yb_, OURO, 1.0, larg=5, traco=16, vao=10, prog_=e_out(ko), contorno=True)
        ks = prog(t, T["ombro"] + 0.3, T["ombro"] + 0.55)
        if ks > 0:
            xs = xr + 20
            y_base = yl - 8 + m * (xs - xl) + 34
            ytop = y_base - 34 - 26 * e_out(ks)
            cv.drawLine(xs, y_base, xs, ytop + 10, paint(NAVY, int(150 * ks), "stroke", 11))
            cv.drawLine(xs, y_base, xs, ytop + 10, paint(OURO, int(255 * ks), "stroke", 6))
            ponta(cv, xs, ytop, -math.pi / 2, 20, OURO, ks)
    cv.restore()
    cv.restore()
    # coluna de chips à direita (a criança fica no terço esquerdo)
    XC = 516
    a1 = prog(t, T["doer"] - 0.05, T["doer"] + 0.15)
    chip_esq(cv, R_DOER, XC, 522, "#FFFFFF", a * a1, tam=38, borda=OURO, esc=1 + 0.06 * pulo(t, T["doer"], 0.3))
    a2 = prog(t, T["comeco"] - 0.05, T["comeco"] + 0.15)
    chip_esq(cv, R_COMECO, XC, 582, OURO, a * a2, tam=38, esc=1 + 0.06 * pulo(t, T["comeco"], 0.3))
    a3 = prog(t, T["alto"] - 0.05, T["alto"] + 0.15)
    if a3 > 0:
        r = chip_esq(cv, R_OMBRO, XC, 652, "#FFFFFF", a * a3, tam=38, borda=OURO, esc=1 + 0.06 * pulo(t, T["alto"], 0.3))
        (xl, yl), (xr, yr) = OMB_E_TOPO, OMB_D_TOPO
        m = (yr - yl) / (xr - xl)
        px, py = tela3(xr + 74, yl + m * (xr + 74 - xl) - 8)
        guia(cv, px + 4, py + dy, r.left() - 2, r.centerY(), a * a3)
    a4 = prog(t, T["assimetrica"] - 0.05, T["assimetrica"] + 0.15)
    if a4 > 0:
        r = chip_esq(cv, R_CINTURA, XC, 800, "#FFFFFF", a * a4, tam=37, borda=OURO,
                     esc=1 + 0.06 * pulo(t, T["assimetrica"], 0.3))
        px, py = tela3(630, 760)
        guia(cv, px + 6, py + dy, r.left() - 2, r.centerY(), a * a4)
    a5 = prog(t, T["leve2"] - 0.06, T["leve2"] + 0.18)
    if a5 > 0:
        lw = larg_texto(R_AVAL, F_BLACK, 42)
        pa = (e_back(a5) if a5 < 1 else 1.0) * (1 + 0.08 * pulo(t, T["avaliacao"], 0.4))
        cv.save(); cv.translate(CX, 1162 + dy); cv.scale(pa, pa)
        pill = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 30, -33, lw / 2 + 30, 33), 33, 33)
        cv.drawRRect(pill, paint(OURO, int(110 * a * a5), blur=12))
        cv.drawRRect(pill, paint(OURO, int(255 * a * a5)))
        texto(cv, R_AVAL, 0, 15, F_BLACK, 42, NAVY, int(255 * a * a5))
        cv.restore()
    cv.restore()


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep):
    fundo_rapido(cv, t)
    tremor = tremor_cam(t, T)
    cv.save(); cv.translate(tremor, 0)
    bancada(cv)
    sts = {n: estado(n, t, T) for n in ("A", "B")}
    cv.save()
    cv.clipRRect(skia.RRect.MakeRectXY(skia.Rect(*BANC), 34, 34), skia.ClipOp.kIntersect, True)
    paineis(cv, t, T)
    for nome in ("B", "A"):                                         # B nasce de trás de A em "prova"
        st = sts[nome]
        if st["a"] <= 0:
            continue
        cv.save(); cv.translate(st["x"], PISO); cv.scale(st["s"], st["s"])
        crianca(cv, st, t, T)
        cv.restore()
        if nome == "A" and 0 <= t - T["mochila3"] < 0.6:            # as estrelas somem em brilhos na virada
            for chave, (px, py) in ESTRELAS:
                x, y = tela_local(st, *no_tronco(estado("A", T["mochila3"], T), px, py))
                brilhos(cv, x, y, t, T["mochila3"] + 0.02, n=5, raio=62, dur=0.55, raio0=22)
        if nome == "A" and 0 <= t - T["mochila4"] < 0.9:            # a gigante encolhe: brilhos em volta
            bx, by = centro_bag_chao(st)
            brilhos(cv, bx, by, t, T["mochila4"] + 0.05, n=10, raio=190, dur=0.75, raio0=90)
        hx, hy = tela_local(st, 10, -300)
        brilhos(cv, hx, hy, t, T["crianca"] + 0.02 * (nome == "B"), n=12, raio=260, dur=0.9, raio0=150)
    veu_foco(cv, t, T)
    cv.restore()
    rotulos(cv, t, T)
    cartao_regra(cv, t, T)
    cartao_asterisco(cv, t, T)
    vcta = 0.8 * prog(t, T["manda"] - 0.55, T["manda"] - 0.25)     # véu navy: a CTA fica sobre fundo escuro
    if vcta > 0:
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(*BANC), 34, 34), paint(NAVY, int(255 * vcta)))
    cv.restore()

    # ---- topo: gancho (capa), claquete, selo (a aposta), cartão do veredito e carimbo
    capa(cv, t, T["vamos"], *ep["gancho"])
    kq = t - T["prova"]
    if -0.35 < kq < 1.25:
        aq = prog(t, T["prova"] - 0.35, T["prova"] - 0.2) * (1 - prog(t, T["prova"] + 1.0, T["prova"] + 1.25))
        fecha = e_in_back(prog(t, T["prova"] - 0.3, T["prova"]))
        dx = (-300 * (1 - e_out(prog(t, T["prova"] - 0.35, T["prova"] - 0.15)))
              - 320 * e_in_back(prog(t, T["prova"] + 0.95, T["prova"] + 1.25)))
        claquete(cv, 48 + dx, 196, fecha, aq)
    ps0 = prog(t, T["prova"] + 0.15, T["prova"] + 0.5)
    a0 = clamp(ps0 * 4) * (1 - prog(t, T["manda"] - 0.3, T["manda"]))
    a0 *= 1 - prog(t, T["veredito"] - 0.1, T["veredito"] + 0.1) * (1 - prog(t, t_card_sai(T) + 0.2, t_card_sai(T) + 0.45))
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
    ev = [(T["mochila"] + 0.05, "thump", 0.6), (T["assim"], "shimmer", 0.3)]
    ev += [(T["vamos"], "whoosh", 0.25), (T["prova"] - 0.01, "tick", 0.45), (T["prova"] + 0.03, "whoosh", 0.35)]
    ev += [(T["outro"], "whoosh", 0.3), (T["mochila2"], "whoosh", 0.2), (T["leve"], "pop", 0.6),
           (T["leve"] + 0.08, "pop", 0.4)]
    ev += [(T["exagerado"], "thump", 0.7), (T["dor"], "pop", 0.5), (T["costas"], "pop", 0.5), (T["ombros"], "pop", 0.5),
           (T["postura"], "whoosh", 0.3), (T["carrega"], "thump", 0.5)]
    ev += [(T["tira"], "whoosh", 0.5), (T["tira"] + 0.25, "thump", 0.6), (T["mochila3"] + 0.05, "shimmer", 0.35),
           (T["postura2"], "whoosh", 0.25), (T["volta"], "ding", 0.6)]
    ev += [(T["veredito"], "whoosh", 0.4)]
    tiq = roleta(T)
    for i, ti in enumerate(tiq):                                    # roleta: um tique por chegada, desacelerando
        ev.append((ti, "tick", lerp(0.2, 0.36, i / 5)))
    ev += [(T["mito"] - 0.17, "whoosh", 0.3), (T["mito"], "thump", 0.55), (T["mito"] + 0.02, "crackle", 0.4)]
    ev += [(T["doer1"], "ping", 0.3), (T["prova2"], "shimmer", 0.25)]
    ev += [(T["mochila4"], "whoosh", 0.4), (T["mochila4"] + 0.08, "shimmer", 0.4)]
    ev += [(T["cheia"], "whoosh", 0.3), (T["cheia"] + 0.35, "click", 0.5), (T["dez"], "pop", 0.6),
           (T["peso2"], "pop", 0.4), (T["crianca"], "shimmer", 0.35)]
    ev += [(T["escoliose2"], "whoosh", 0.25), (T["doer"], "pop", 0.5), (T["comeco"], "pop", 0.5),
           (T["ombro"], "tick", 0.4), (T["alto"], "pop", 0.5), (T["cintura"], "tick", 0.4),
           (T["assimetrica"], "pop", 0.5), (T["leve2"], "pop", 0.35), (T["avaliacao"], "ding", 0.5)]
    ev += [(T["manda"] - 0.5, "whoosh", 0.25), (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def tempos_previa(T):
    return (0.0, T["mochila"] + 0.15, T["assim"] + 0.2, T["prova"] - 0.02, T["prova"] + 0.6, T["outro"] + 0.3,
            T["mochila2"] + 0.25, T["leve"] + 0.4, T["dor"] + 0.2, T["ombros"] + 0.3, T["postura"] + 0.3,
            T["carrega"] + 0.3, T["tira"] + 0.15, T["mochila3"] + 0.3, T["postura2"], T["volta"] + 0.2,
            T["volta"] + 0.6, T["veredito"] + 0.5, roleta(T)[3] + 0.05, roleta(T)[5] + 0.06, T["mito"] - 0.08,
            T["mito"] + 0.03, T["mito"] + 0.4, T["doer1"] + 0.2, T["prova2"] + 0.2, T["mochila4"] + 0.2,
            T["mochila4"] + 0.5, T["cheia"] + 0.5, T["dez"] + 0.3, T["crianca"] + 0.3, T["escoliose2"] + 0.4,
            T["comeco"] + 0.3,
            T["alto"] + 0.4, T["assimetrica"] + 0.4, T["avaliacao"] + 0.3, T["manda"] - 0.3, T["manda"] + 1.6)


# ------------------------------------------------------------------ render local (pausa do veredito)
_PONTA = re.compile(r"[.,:;!?—…]+$")
PAUSA_VEREDITO = 0.50                              # a roleta MITO | VERDADE respira antes do golpe
GANHO_TRILHA, GANHO_ASTERISCO = 0.40, 0.15
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
    baixa[1] ela desce para baixa[2] (o asterisco sóbrio)."""
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
    """Voz -> palavras limpas -> corte de silêncio -> alinhamento -> pausa do veredito -> âncoras."""
    roteiro = "\n".join(ep["roteiro"])
    voz_bruta, palavras = _voz.narrar(roteiro, _voz.RITMO_COMO_FUNCIONA, os.path.join(tmp, "voz"))
    palavras = [dict(p, w=_PONTA.sub("", p["w"])) for p in palavras]
    voz_c, pal, tirado = comprimir(voz_bruta, palavras, respiro_cta=respiro_cta)
    pal = alinhar(pal, roteiro)
    voz_c, pal = inserir_pausa(voz_c, pal, "veredito", PAUSA_VEREDITO)
    T = ancoras(pal, ANCORAS)
    return voz_c, pal, T, tirado


def fazer_render_luz(quadro_fn, sons_fn, tempos_fn, respiro_cta=0.5):
    """Os passos de cf_fixador_circular.fazer_render_tolerante + a pausa do veredito + trilha baixa."""
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
        baixa = (T["escoliose2"] - 0.3, T["manda"] - 0.1, GANHO_ASTERISCO / GANHO_TRILHA)
        som.gravar_wav(wav, mixar(voz_c, T["total"], sons_fn(T), GANHO_TRILHA, baixa))
        codificar(quadro_t, T["total"], wav, mp4)
        return mp4, T["total"]
    return render


render = fazer_render_luz(quadro, sons, tempos_previa, respiro_cta=0.5)
