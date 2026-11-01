# -*- coding: utf-8 -*-
"""CÂMERA LENTA (série nova) — episódio "UM LADO ABRE MENOS / NA HORA DA FRALDA?" (displasia do
desenvolvimento do quadril: o ÚNICO sinal de MOVIMENTO que dá para olhar na troca de fralda).

v2 (correção pós-revisão de 31/10): o vídeo se concentra no único sinal que a câmera lenta REVELA — um lado
abre menos — e deixa de repetir o cf_quadril_bebe (agendado 06/11): saíram a 2ª câmera lenta (dobrinhas e
perna curta, sinais ESTÁTICOS que a lenta não revela), o cartão e o carimbo TESTE DO PEZINHO NÃO DETECTA (gancho
do outro vídeo; a frase ficou só na voz) e o selo de tique no "na dúvida". O problema agora tem NOME na voz
("displasia do quadril: o quadril que não encaixa"), o bebê nunca fica parado (chute calmo em 1× ao fundo) e o
fecho fica num cartão claro GRANDE + recapitulação em polaroide do congelamento.

Mesma mecânica do piloto cf_cameralenta_ponta_pes: um REPLAY de TV. Visto DE CIMA, do ponto de vista de quem
troca a fralda (a cabeça e o rosto ficam FORA do quadro: o recorte de cima passa na barriga), o bebê chuta as
perninhas em 1× (rápido e borrado), a fita VOLTA, o lance é revisto em CÂMERA LENTA e CONGELA no detalhe. O
tempo do filme (`Filme.tf`) é separado do tempo do vídeo: as pernas são desenhadas em função do tempo do filme;
a narração nunca para nem desacelera.

O FILME (o que a câmera gravou, em segundos de filme):
  chutes alternados -> as pernas esticam e param lado a lado (descanso) -> as duas se abrem SOZINHAS, juntas;
  a da direita da tela PARA em 17° e a da esquerda segue até 34° -> fecham e voltam a chutar.
  No 1× tudo isso passa em meio segundo, dentro do borrão. Depois do avanço rápido o bebê chuta CALMO (amplitude
  pequena, sem abrir: não repete o sinal) e, no respiro antes da CTA, um replay LIMPO em 1× do mesmo lance.
A câmera lenta REVELA o que o 1× escondeu: desacelera nos chutes, as pernas param lado a lado e se abrem; um
  ponto dourado gruda em cada pé e risca um ARCO pontilhado, e um LEQUE dourado translúcido sai de cada quadril
  mostrando QUANTO cada perna abriu (o tamanho do leque é a comparação que o leigo lê de relance). A da direita
  PARA no "para" (tracinho dourado); a da esquerda segue. Congela no fim de "caminho": zoom seco, o pedaço de
  leque que FALTA do lado curto aparece em branco tracejado, círculo do comentarista e o carimbo
  UM LADO ABRE MENOS (responde ao gancho). O carimbo se desfaz no borrão do avanço rápido ("com pressa, passa
  batido").
Fecho sem susto, num cartão CLARO grande à direita (o bebê recua para a esquerda e segue chutando calmo):
  "displasia do quadril: o quadril que não encaixa" = PICTOGRAMA de brinquedo fora do corpo, ligado ao quadril do
  lado curto por um fio dourado: uma bolinha marfim desce para a conchinha e PARA na borda, sem assentar; o lugar
  onde ela assentaria aparece tracejado. "Avaliação clínica" = estetoscópio grande com anel dourado (sem
  ultrassom desenhado). "Primeiros meses" = calendário sem números cujas primeiras colunas acendem. "Na dúvida"
  = a cena escurece e entra a POLAROIDE do congelamento (os dois leques) + o estetoscópio com anel dourado no
  "ortopedista" (consulta, não aprovação).

Regras da série e do verificador (storyboard.json), todas aqui:
  * É OLHAR, nunca manobra: nenhuma mão (de adulto ou de médico) em nenhum quadro; as perninhas abrem SOZINHAS,
    devagar, sem passar de uma abertura natural.
  * Bebê em traço esquemático: pele lisa e OPACA, sem rosto, sem choro, fralda fechada; nada por dentro da perna
    (sem osso, sem cabeça do fêmur); SEM ultrassom desenhado; nada que lembre chapa (cartões CLAROS).
  * Um sinal só no desenho: as duas pernas têm o MESMO comprimento e as MESMAS dobrinhas (v2); só a abertura muda.
  * VERMELHO PROIBIDO no vídeo inteiro (aqui é dourado ou branco). O lado que abre mais NÃO ganha rótulo nem cor
    de "certo". Sem antes e depois (sem suspensório; a bolinha NUNCA assenta: nada de "conserto" prometido).
  * Selo CÂMERA LENTA e moldura âmbar só na janela da câmera lenta (nunca no 1×, no ◀◀, no ▶▶, nos cartões
    ou na CTA). Nada de ❚❚, barra de progresso, "PAUSA", timecode ou dígitos: congelar = flash + tique + chip
    apagado.
  * Som: nenhum "clique" no quadril nem estalo; nenhum choro; a perna que PARA não ganha baque (só um brilho
    baixo); a bolinha encosta na borda com um "bup" grave e macio.
  * Nenhum texto além do `tela` (CÂMERA LENTA, 1×, 0,25×, UM LADO ABRE MENOS), do gancho e da interface.

Helpers COPIADOS (não importados), como manda o contrato: do piloto cf_cameralenta_ponta_pes — Filme (adaptado,
com relógio contínuo), _trim, sstep, _img/_blit/fundo_cl/_rel/monitor_fundo/varredura/faixas_tracking/
cantoneiras/flash, relogio (orig. cf_andador), chip_dim/chip_c, _setas, painel, circulo_mao, ponta_seta,
estetoscopio, ponto_ouro, selo_lenta, miniatura/polaroide (de melhores_momentos), trilha_partes, _fita,
rebobinar, avancar, janelas, _media_movel, mixar_cl; do cf_quadril_bebe — _perna_path, perna_bebe, PE_Y0, HQ/HY,
pe_fundo, _fralda/fralda, o trocador de troca_fralda (aqui CLARO), arco_pts; carimbo (orig. carimbo_ouro do
cf_fratura_cola / cf_comum.carimbo, com tamanho e "desfazer no borrão"). Importados sem cópia:
capa/interface/ancoras (cf_comum), comprimir/alinhar/montar_blocos (cf_fratura_cola), paleta, texto, brilhos e
aviao (cf_alongamento).

v3 (correção de desenho de 01/11; texto, voz e tempos intactos): o "0,25×" grande nasce abaixo dos pés e desliza
até o painel sem cruzar a perna da direita (`_pop_c`); o aviãozinho da CTA passa na frente da caixa de crédito
(`aviao_na_frente`).
v4 (2ª rodada de 01/11; texto, voz, sons e tempos intactos): no chute as duas pernas têm o MESMO comprimento aparente
a cada instante (`_k_igual`; antes o k corria em contrafase e uma perna ficava 15-20% mais curta, conferido em todo
quadro por um assert no `Filme`); o borrão do 1×/◀◀/▶▶ virou pose nítida + rastro contínuo sem contorno
(`pernas_borradas`; antes 6 poses inteiras empilhadas = vários pés no quadro pausado); o ponto dourado gruda no pé
também com o joelho dobrado.
v5 (3ª rodada de 01/11; texto, voz, sons e tempos de fala intactos): a saída da polaroide do "na dúvida" deixou de
ser dissolução cruzada com a cena cheia (duas figuras desalinhadas somadas por ~10 quadros: quatro pernas, duas
fraldas) e passa por FUNDO ESCURO, com a volta da câmera do recuo para BASE escondida no escuro total (`recap`,
REC_*).
A cena é PRESA ao roteiro pelas palavras-âncora (ANCORAS): roteiro sem elas = KeyError no render.
"""
import math
import os

import numpy as np
import skia

from . import som, voz as _voz
from .base import FPS, codificar, previas as _previas
from .cf_alongamento import (BG_OUT, CX, F_BLACK, H, OURO, PART, PELE, W, aviao, brilhos, clamp, e_back, e_inout,
                             e_out, lerp, lerpc, paint, prog, texto)
from .cf_comum import ancoras, capa, interface
from .cf_fratura_cola import alinhar, comprimir, montar_blocos

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "um": ("um", 1, False), "volta": ("volta", 1, False), "camera": ("câmera", 1, False),
    "lenta": ("lenta", 1, False), "repara": ("repara", 1, False), "perninha": ("perninha", 1, False),
    "para": ("para", 1, False), "caminho": ("caminho", 1, False), "troca": ("troca", 1, False),
    "pressa": ("pressa", 1, False), "batido": ("batido", 1, False), "pode": ("pode", 1, False),
    "displasia": ("displasia", 1, False), "quadril2": ("quadril", 2, False), "encaixa": ("encaixa", 1, False),
    "teste": ("teste", 1, False), "detecta": ("detecta", 1, False), "avaliacao": ("avaliação", 1, False),
    "clinica": ("clínica", 1, False), "ultrassom": ("ultrassom", 1, False),
    "identificado": ("identificado", 1, False), "primeiros": ("primeiros", 1, False), "meses": ("meses", 1, False),
    "simples": ("simples", 1, False), "duvida": ("dúvida", 1, False), "ortopedista": ("ortopedista", 1, False),
    "pediatrico": ("pediátrico", 1, False), "manda": ("manda", 1, False),
}
DESTAQUE = {"menos", "perninha", "caminho", "pressa", "batido", "displasia", "encaixa", "pezinho", "detecta",
            "clínica", "primeiros", "meses", "simples", "dúvida", "ortopedista", "pediátrico"}
RESPIRO_CTA = 1.6
R_SELO, R_1X, R_LENTA = "CÂMERA LENTA", "1×", "0,25×"                                  # todos em ep["tela"]
R_ABRE = "UM LADO ABRE MENOS"

# ------------------------------------------------------------------ paleta (SEM vermelho e SEM lilás)
PELE_CL, PELE_ESC, PELE_LINHA = "#F7CDB8", "#DA987E", "#B9765E"
FRALDA, FRALDA_SOMBRA, FRALDA_LINHA = "#F4F7FB", "#CBD7E4", "#97AABE"
AZUL_CLARO = "#9CC9FF"
CAMISA, CAMISA_CL, CAMISA_LINHA = "#8FC9E8", "#B7DDF1", "#4D8FB5"
TROCADOR, TROCADOR_ESC, TROCADOR_BORDA, COSTURA = "#CFE7DF", "#BCDCD1", "#7FB3A2", "#93C4B4"
MADEIRA, MADEIRA_JUNTA, MADEIRA_VEIO = "#9C7A5A", "#7E5F44", "#AD8B6A"   # tampo da cômoda (sem preto/cinza)
FUNDO_CARTAO = "#0B1824"
CARTAO, CARTAO_BORDA, TINTA = "#F3F7FB", "#C9D6E2", "#2B4A66"
MARFIM, MARFIM_ESC, MARFIM_LINHA = "#F6ECD6", "#DCCBA8", "#A48A5E"
AMBAR = "#FFB547"
AZUL_CL = "#9CC9FF"
NAVY = "#16324A"

# ------------------------------------------------------------------ o "monitor" de replay (tela)
CENA = skia.Rect(40, 330, 1040, 1230)                            # o mundo é recortado aqui (selo e karaokê livres)


def _c(h, a=255):
    h = h.lstrip("#")
    return skia.ColorSetARGB(int(a), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _alfa(a):
    p = skia.Paint()
    p.setAlphaf(clamp(a))
    return p


def _trim(pt, k):
    """Traço desenhado até a fração k (cópia do piloto)."""
    if k < 0.999:
        pe = skia.TrimPathEffect.Make(0.0, max(0.002, k))
        if pe is not None:
            pt.setPathEffect(pe)
    return pt


def sstep(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def rot(p, graus):
    a = math.radians(graus); c, s = math.cos(a), math.sin(a)
    return p[0] * c - p[1] * s, p[0] * s + p[1] * c


# ------------------------------------------------------------------ o bebê (coordenadas locais = as do cf_quadril_bebe)
HQ, HY = (455, 625), 480          # quadris (x da perna da esquerda e da direita da tela) e altura
K_CURTA = 1.0                     # v2: as duas pernas têm o MESMO comprimento (um sinal só no desenho: a abertura)
PE_Y0 = 322                       # início do pé (unidades da perna, antes do fator de comprimento)
DOBRAS_E, DOBRAS_D = (116, 166), (116, 166)                     # v2: dobrinhas IGUAIS dos dois lados
S_B, BEBE_Y = 1.24, 575.0         # local -> mundo: escala e altura dos quadris no mundo


def pe_fundo(k):
    """Ponta dos dedos (unidades locais, a partir do quadril). (cópia do cf_quadril_bebe)"""
    return PE_Y0 * k + 84


def l2m(lx, ly):
    """Coordenada local do bebê -> mundo."""
    return 540 + S_B * (lx - 540), BEBE_Y + S_B * (ly - HY)


def bebe_aplica(cv):
    cv.translate(540, BEBE_Y); cv.scale(S_B, S_B); cv.translate(-540, -HY)


def _perna_path(k):
    """(cópia do cf_quadril_bebe)"""
    def Y(v):
        return v * k
    p = skia.Path()
    p.moveTo(-66, -30)
    p.cubicTo(-76, Y(40), -78, Y(120), -62, Y(178))
    p.cubicTo(-54, Y(206), -52, Y(226), -55, Y(254))
    p.cubicTo(-57, Y(292), -44, Y(318), -36, Y(336))
    p.lineTo(36, Y(336))
    p.cubicTo(44, Y(318), 57, Y(292), 55, Y(254))
    p.cubicTo(52, Y(226), 54, Y(206), 62, Y(178))
    p.cubicTo(78, Y(120), 76, Y(40), 66, -30)
    p.close()
    return p


def perna_bebe(cv, hx, ang, k, dentro, dobras, pe_esc=1.0, sombra=True):
    """Perna de desenho (pele lisa, sem osso), presa no quadril (hx, HY), girada `ang` graus. (cópia adaptada do
    cf_quadril_bebe: `k` encurta a perna no chute — o joelho sobe na direção de quem olha, e o pé cresce um pouco
    (`pe_esc`))."""
    cv.save(); cv.translate(hx, HY); cv.rotate(ang)
    sh = skia.GradientShader.MakeLinear([skia.Point(-80, 0), skia.Point(80, 0)],
                                        [_c(PELE_ESC), _c(PELE), _c(PELE_CL), _c(PELE), _c(PELE_ESC)],
                                        [0.0, 0.22, 0.5, 0.78, 1.0])
    pe_top = PE_Y0 * k
    perna = _perna_path(k)
    if sombra:
        cv.save(); cv.translate(7, 9)
        cv.drawPath(perna, paint("#1E4A40", 70, blur=9))
        cv.restore()
    cv.save(); cv.translate(0, pe_top + 40); cv.scale(pe_esc, pe_esc); cv.translate(0, -(pe_top + 40))
    pe = skia.RRect.MakeRectXY(skia.Rect(-44, pe_top, 44, pe_top + 80), 40, 40)
    cv.drawRRect(pe, paint(PELE, shader=sh))
    cv.drawRRect(pe, paint(PELE_LINHA, 230, "stroke", 3.2))
    for i, (fx, r) in enumerate(((-29, 9), (-15, 9.5), (-1, 10), (14, 11), (30, 13))):
        xx = fx * dentro
        cv.drawCircle(xx, pe_top + 74 - (2 if i == 4 else 0), r, paint(PELE_CL))
        cv.drawCircle(xx, pe_top + 74 - (2 if i == 4 else 0), r, paint(PELE_LINHA, 230, "stroke", 2.6))
    cv.restore()
    cv.drawPath(perna, paint(PELE, shader=sh))
    cv.drawPath(perna, paint(PELE_LINHA, 230, "stroke", 3.2))
    cv.drawArc(skia.Rect(-22, 200 * k - 12, 22, 200 * k + 12), 25, 130, False, paint(PELE_LINHA, 140, "stroke", 3))
    for y in dobras:                                                  # dobrinhas da coxa (iguais dos dois lados)
        p = skia.Path(); p.moveTo(72 * dentro, y - 6)
        p.quadTo(36 * dentro, y + 14, -14 * dentro, y + 4)
        cv.drawPath(p, paint(PELE_LINHA, 200, "stroke", 4))
    cv.restore()


def _fralda():
    """(cópia do cf_quadril_bebe)"""
    p = skia.Path()
    p.moveTo(342, 400); p.lineTo(738, 400)
    p.cubicTo(748, 450, 742, 500, 716, 528)
    p.cubicTo(680, 540, 640, 555, 600, 592)
    p.cubicTo(575, 612, 505, 612, 480, 592)
    p.cubicTo(440, 555, 400, 540, 364, 528)
    p.cubicTo(338, 500, 332, 450, 342, 400)
    p.close()
    return p


FRALDA_P = _fralda()


def fralda(cv):
    """Fralda branca FECHADA, com abas (cópia do cf_quadril_bebe)."""
    cv.save(); cv.translate(0, -28)
    sh = skia.GradientShader.MakeLinear([skia.Point(0, 400), skia.Point(0, 610)], [_c(FRALDA), _c(FRALDA_SOMBRA)])
    pf = paint(FRALDA, shader=sh); pf.setPathEffect(skia.CornerPathEffect.Make(18))
    sombra = paint("#1E4A40", 80, blur=12); sombra.setPathEffect(skia.CornerPathEffect.Make(18))
    cv.drawPath(FRALDA_P, sombra)
    cv.drawPath(FRALDA_P, pf)
    po = paint(FRALDA_LINHA, 255, "stroke", 3); po.setPathEffect(skia.CornerPathEffect.Make(18))
    cv.drawPath(FRALDA_P, po)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(346, 404, 734, 432), 10, 10), paint("#DDE7F1"))
    for x0 in (330, 708):                                             # abas
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0, 444, x0 + 42, 490), 10, 10), paint(AZUL_CLARO))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0, 444, x0 + 42, 490), 10, 10), paint("#6E9CC9", 255, "stroke", 2.5))
    for x, y in ((470, 470), (540, 505), (610, 470), (505, 545), (575, 545)):   # estampa de bolinhas
        cv.drawCircle(x, y, 7, paint(AZUL_CLARO, 170))
    cv.restore()


def _tronco():
    """Barriga (o recorte de cima passa aqui: cabeça e rosto ficam fora do quadro)."""
    p = skia.Path()
    p.moveTo(316, 120); p.lineTo(764, 120)
    p.cubicTo(772, 240, 766, 320, 750, 400)
    p.lineTo(330, 400)
    p.cubicTo(314, 320, 308, 240, 316, 120)
    p.close()
    return p


TRONCO_P = _tronco()


def tronco(cv):
    cv.save(); cv.translate(8, 10)
    cv.drawPath(TRONCO_P, paint("#1E4A40", 60, blur=12))
    cv.restore()
    sh = skia.GradientShader.MakeLinear([skia.Point(300, 0), skia.Point(780, 0)],
                                        [_c(PELE_ESC), _c(PELE), _c(PELE_CL), _c(PELE), _c(PELE_ESC)],
                                        [0.0, 0.2, 0.5, 0.8, 1.0])
    cv.drawPath(TRONCO_P, paint(PELE, shader=sh))
    cv.save(); cv.clipPath(TRONCO_P, skia.ClipOp.kIntersect, True)        # camisetinha puxada para cima
    cam = skia.Path(); cam.moveTo(280, 100); cam.lineTo(800, 100); cam.lineTo(800, 300)
    cam.cubicTo(700, 318, 380, 318, 280, 300); cam.close()
    cv.drawPath(cam, paint(CAMISA))
    for y in (190, 240):                                                # listrinhas
        cv.drawLine(280, y, 800, y, paint(CAMISA_CL, 255, "stroke", 14))
    barra = skia.Path(); barra.moveTo(280, 300); barra.cubicTo(380, 318, 700, 318, 800, 300)
    cv.drawPath(barra, paint(CAMISA_LINHA, 255, "stroke", 6))
    cv.restore()
    cv.drawPath(TRONCO_P, paint(PELE_LINHA, 230, "stroke", 3.2))
    cv.drawArc(skia.Rect(531, 338, 549, 352), 20, 140, False, paint(PELE_LINHA, 170, "stroke", 3))   # umbigo


def trocador(cv):
    """Trocador CLARO e calmo (mundo), com costura tracejada, sobre o tampo de madeira de uma cômoda; continua para
    fora do quadro em cima."""
    cv.drawRect(skia.Rect(-900, -400, 2000, 2200), paint(MADEIRA))
    pj = skia.Path(); pv = skia.Path()
    for i in range(-6, 19):
        x = i * 150.0
        pj.moveTo(x, -400); pj.lineTo(x, 2200)
        pv.moveTo(x + 40 + 25 * (i % 3), -400); pv.lineTo(x + 40 + 25 * (i % 3), 2200)
    cv.drawPath(pv, paint(MADEIRA_VEIO, 255, "stroke", 4))
    cv.drawPath(pj, paint(MADEIRA_JUNTA, 255, "stroke", 4))
    mat = skia.RRect.MakeRectXY(skia.Rect(70, 60, 1010, 1135), 58, 58)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(70, 72, 1010, 1147), 58, 58), paint("#3A2A1E", 90, blur=14))
    cv.drawRRect(mat, paint(TROCADOR))
    cv.save(); cv.clipRRect(mat, True)
    for y in (300, 560, 820):                                           # gomos acolchoados
        cv.drawLine(70, y, 1010, y, paint(TROCADOR_ESC, 255, "stroke", 6))
    cv.restore()
    cv.drawRRect(mat, paint(TROCADOR_BORDA, 255, "stroke", 4))
    ps = paint(COSTURA, 255, "stroke", 3.5); ps.setPathEffect(skia.DashPathEffect.Make([16, 11], 0))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(96, 86, 984, 1109), 40, 40), ps)


# ------------------------------------------------------------------ o FILME: as pernas em função do tempo do filme
P_CHUTE = 0.6                     # ciclo do chute (s de filme = s de vídeo em 1×)
REST = 3.0                        # pernas esticadas, lado a lado (graus de abertura de cada uma)
ABRE_E, ABRE_D = 34.0, 17.0       # abertura natural: a da esquerda da tela vai a 34°, a da direita PARA na metade
PHI_L = 0.0                       # v2 (pernas iguais): no quadro 0 as duas têm o mesmo ângulo e o mesmo tamanho
KE, R1, OPEN0, DO = 0.36, 0.48, 0.66, 0.47
H1 = OPEN0 + DO + 0.05            # segura aberta
C1 = H1 + 0.22                    # fecha e volta a chutar
CALMA = 100.0                     # trecho "bebê tranquilo": chute CALMO, pequeno e sem abrir (não repete o sinal)
P_CALMA = 1.3                     # ciclo do chute calmo (s)
V1, VL, VR = 1.0, 0.25, 2.5       # 1×, 0,25×, avanço rápido
MISTURA = 0.4                     # s de vídeo para misturar duas poses nos saltos de filme (sem "pulo" de pernas)


K_CHUTE = (0.78, 0.98)            # v4: comprimento aparente no chute (joelhos dobrados .. esticadas), IGUAL nas duas
K_CALMA = (0.85, 0.99)            # v4: idem no chute calmo


def _k_igual(w, faixa):
    """v4 (correção de 01/11, 2ª rodada): o comprimento aparente das DUAS pernas, o mesmo a cada instante. Antes o
    k corria em CONTRAFASE (0,84±0,14 no chute, 0,92±0,07 no calmo): uma perna ficava 15-20% mais curta que a outra
    e, num vídeo sobre quadril de bebê, perna 'mais curta' é sinal de alerta. Agora o joelho continua subindo e
    descendo (o pé cresce um pouco, escorço de quem olha de cima), mas nas duas ao mesmo tempo: as duas esticam
    juntas quando QUALQUER uma chega ao fim do chute (sin² = máximo em w = 90° e 270°, os mesmos instantes das
    batidinhas de `chutes_som`, que não mudam) e dobram juntas quando se cruzam no meio."""
    return faixa[0] + (faixa[1] - faixa[0]) * math.sin(w) ** 2


def chute(tf):
    """Chutes alternados (abre-fecha rápido): a abertura de cada perna corre defasada meio ciclo; o comprimento
    aparente é o MESMO nas duas (v4, `_k_igual`)."""
    w = 2 * math.pi * tf / P_CHUTE
    k = _k_igual(w + PHI_L, K_CHUTE)
    return (12 + 9 * math.sin(w), k, 12 + 9 * math.sin(w + math.pi), k)


def chute_calmo(u):
    """Chute CALMO de fundo (fecho): amplitude pequena, quase sem abrir, igual dos dois lados (comprimento igual
    nas duas a cada instante, v4)."""
    w = 2 * math.pi * u / P_CALMA
    k = _k_igual(w, K_CALMA)
    return (REST + 2.5 + 2.5 * math.sin(w), k, REST + 2.5 + 2.5 * math.sin(w + math.pi), k)


DESCANSO = (REST, 1.0, REST, 1.0)


def _mix(a, b, k):
    return tuple(lerp(x, y, k) for x, y in zip(a, b))


def abre(tf):
    """As duas perninhas se abrem SOZINHAS, juntas; a da direita da tela para em ABRE_D."""
    u = clamp((tf - OPEN0) / DO)
    e = REST + (ABRE_E - REST) * e_inout(u)
    return (e, 1.0, min(e, ABRE_D), 1.0)


U_PARA = next(i / 2000 for i in range(2001) if REST + (ABRE_E - REST) * e_inout(i / 2000) >= ABRE_D)
TF_PARA = OPEN0 + U_PARA * DO     # instante de filme em que a perna da direita para


def pose(tf):
    """-> (abertura E, comprimento E, abertura D, comprimento D)."""
    if tf >= CALMA:
        return chute_calmo(tf - CALMA)
    if tf < KE:
        return chute(tf)
    if tf < R1:
        return _mix(chute(tf), DESCANSO, sstep((tf - KE) / (R1 - KE)))
    if tf < OPEN0:
        return DESCANSO
    if tf < H1:
        return abre(tf)
    if tf < C1:
        return _mix(abre(H1), chute(tf), sstep((tf - H1) / (C1 - H1)))
    return chute(tf)


def em_chute(tf):
    return tf < KE or C1 <= tf < CALMA


class Filme:
    """Liga o tempo do VÍDEO ao tempo do FILME (cópia adaptada do piloto), por trechos presos às palavras-âncora:
    play (1×), volta (rebobinar), lenta (0,25×), congela (0×), avanca (avanço rápido). O relógio do painel segue
    um tempo CONTÍNUO (`relogio`). Nos dois saltos de filme (avanço -> chute calmo; chute calmo -> replay limpo)
    as poses se MISTURAM por MISTURA s (`pose_video`): as pernas não pulam."""

    def __init__(self, T):
        s = []
        self.tf_fz1 = OPEN0 + DO + 0.01                                   # congela com a da esquerda em 34°
        self.t_para = T["para"] - 0.03                                    # a da direita PARA no "para"
        self.t_fz = self.t_para + (self.tf_fz1 - TF_PARA) / VL            # ... e congela quando a outra chega
        tf_s1 = self.tf_fz1 - VL * (self.t_fz - T["camera"])
        assert 0.0 <= tf_s1 <= OPEN0, ("a câmera lenta não começa antes da abertura", tf_s1)
        assert T["lenta"] < self.t_para < self.t_fz < T["pressa"] - 1.0, ("congelamento curto demais", self.t_fz)
        s.append((0.0, T["volta"], "play", 0.0, V1 * T["volta"], None))
        assert V1 * T["volta"] > C1, "o 1× tem de passar o lance inteiro antes de a fita voltar"
        s.append((T["volta"], T["camera"], "volta", V1 * T["volta"], tf_s1, "inout"))
        s.append((T["camera"], self.t_fz, "lenta", tf_s1, self.tf_fz1, None))
        s.append((self.t_fz, T["pressa"], "congela", self.tf_fz1, self.tf_fz1, None))
        self.t_calma = T["pode"] - 0.05
        self.tf_ou = self.tf_fz1 + VR * (self.t_calma - T["pressa"])
        s.append((T["pressa"], self.t_calma, "avanca", self.tf_fz1, self.tf_ou, None))
        self.t_rep = T["pediatrico"] + 0.45                                # replay limpo no respiro antes da CTA
        s.append((self.t_calma, self.t_rep, "play", CALMA, CALMA + V1 * (self.t_rep - self.t_calma), None))
        fim = T["total"] + 2.0
        s.append((self.t_rep, fim, "play", R1, R1 + V1 * (fim - self.t_rep), None))
        self.segs = s
        self.T = T
        rel, acc = [], 0.0                                                # relógio contínuo
        for x in s:
            rel.append(acc); acc += x[4] - x[3]
        self.rel0 = rel
        self.tf_s1 = tf_s1
        self.misturas = ((self.t_calma, pose(self.tf_ou)),
                         (self.t_rep, pose(CALMA + V1 * (self.t_rep - self.t_calma))))
        # v4: um sinal só no desenho — em NENHUM quadro (nem nas amostras do rastro) uma perna fica mais curta
        n = int(round((T["total"] + 0.2) * FPS * 4))
        dif = max(abs(p[1] - p[3]) for p in (pose_video(i / (FPS * 4), self) for i in range(n)))
        assert dif < 1e-9, ("pernas com comprimentos diferentes", dif)

    def seg(self, t):
        for x in self.segs:
            if x[0] <= t < x[1]:
                return x
        return self.segs[-1] if t >= self.segs[-1][0] else self.segs[0]

    def tf(self, t):
        t0, t1, tipo, a, b, ease = self.seg(t)
        k = prog(t, t0, t1)
        if ease == "inout":
            k = e_inout(k)
        return lerp(a, b, k)

    def relogio(self, t):
        x = self.seg(t)
        return self.rel0[self.segs.index(x)] + self.tf(t) - x[3]

    def tipo(self, t):
        return self.seg(t)[2]

    def inicio_trecho(self, t):
        i = self.segs.index(self.seg(t))
        while i > 0 and self.segs[i - 1][2] == self.segs[i][2] and self.segs[i - 1][1] == self.segs[i][0]:
            i -= 1
        return self.segs[i][0]


def pose_video(t, F):
    """A pose desenhada no instante de VÍDEO t (com as misturas dos saltos de filme)."""
    ps = pose(F.tf(t))
    for t0, de in F.misturas:
        if t0 <= t < t0 + MISTURA:
            ps = _mix(de, ps, sstep((t - t0) / MISTURA))
    return ps


def lento_k(t, T):
    """0..1: quanto a câmera lenta está LIGADA (selo e moldura âmbar existem só aqui): da desaceleração até o fim
    do congelamento; apaga ANTES do avanço rápido. Uma câmera lenta só (v2)."""
    return prog(t, T["camera"], T["camera"] + 0.18) * (1 - prog(t, T["pressa"] - 0.22, T["pressa"] - 0.02))


# ------------------------------------------------------------------ geometria das pernas (local -> mundo -> tela)
def _ang(lado, th):
    return th if lado == "E" else -th


def ponto_perna(lado, th, k, d):
    """Ponto a distância d do quadril, ao longo da perna aberta `th` graus (local)."""
    hx = HQ[0] if lado == "E" else HQ[1]
    x, y = rot((0.0, d), _ang(lado, th))
    return hx + x, HY + y


def r_pe(lado):
    return PE_Y0 * (1.0 if lado == "E" else K_CURTA) + 40


def r_arco(lado):
    """Raio do arco e do ponto dourado: logo além da ponta dos dedos (o ponto encosta no pé, o arco não o cobre)."""
    return pe_fundo(1.0 if lado == "E" else K_CURTA) + 20


def pe_centro(lado, ps):
    th = ps[0] if lado == "E" else ps[2]
    return ponto_perna(lado, th, 1.0, r_pe(lado))


def arco_pts(lado, a0, a1, d, n=40):
    """Pontos do arco do pé (local), de a0 a a1 graus de abertura. (cópia adaptada do cf_quadril_bebe)"""
    return [ponto_perna(lado, lerp(a0, a1, i / n), 1.0, d) for i in range(n + 1)]


def leque_path(lado, a0, a1, d):
    """Fatia (leque) que sai do quadril e vai até o arco do pé, de a0 a a1 graus (local)."""
    hx = HQ[0] if lado == "E" else HQ[1]
    p = skia.Path(); p.moveTo(hx, HY)
    for q in arco_pts(lado, a0, a1, d, n=30):
        p.lineTo(*q)
    p.close()
    return p


# ------------------------------------------------------------------ câmera (mundo -> tela)
BASE = (1.0, 540.0, 700.0, 540.0, 700.0)
RECUO = (0.8, 540.0, 760.0, 295.0, 800.0)                          # bebê à esquerda; cartão claro à direita


def _mist(a, b, k):
    return tuple(lerp(x, y, k) for x, y in zip(a, b))


def cameras(T, F):
    """Passos de câmera presos às palavras: (t0, duração, (escala, x_mundo, y_mundo, x_tela, y_tela))."""
    pts = [l2m(*q) for q in arco_pts("E", REST, ABRE_E, r_arco("E")) + arco_pts("D", REST, ABRE_E, r_arco("D"))]
    pts += [l2m(*pe_centro(lado, pose(F.tf_fz1))) for lado in ("E", "D")]
    x0, x1 = min(p[0] for p in pts) - 40, max(p[0] for p in pts) + 78
    y0, y1 = min(p[1] for p in pts) - 40, max(p[1] for p in pts) + 40
    zf = min(1.3, 980.0 / (x1 - x0))
    return (
        (T["camera"] - 0.05, 0.8, (0.9, 540.0, 760.0, 540.0, 760.0)),          # a câmera lenta abre um pouco
        (F.t_fz, 0.13, (zf, (x0 + x1) / 2, (y0 + y1) / 2, 540.0, 1000.0)),     # zoom seco nos dois leques
        (T["pressa"], 0.5, BASE),
        (F.t_calma, 0.6, RECUO),                                                 # recua; lugar p/ o cartão
        (F.t_rep + REC_CAM[0], REC_CAM[1], BASE),                                # replay limpo (v5: dentro do escuro)
    )


def camera(t, passos):
    cam = BASE
    for t0, d, alvo in passos:
        k = e_inout(prog(t, t0, t0 + d))
        if k > 0:
            cam = _mist(cam, alvo, k)
    return cam


def aplica(cv, cam):
    s, wx, wy, sx, sy = cam
    cv.translate(sx, sy); cv.scale(s, s); cv.translate(-wx, -wy)


def na_tela(cam, x, y):
    s, wx, wy, sx, sy = cam
    return sx + s * (x - wx), sy + s * (y - wy)


def tela(cam, lx, ly):
    """Local do bebê -> tela."""
    return na_tela(cam, *l2m(lx, ly))


# ------------------------------------------------------------------ camadas fixas em cache (cópia do piloto)
_CACHE = {}


def _img(chave, w, h, desenha):
    if chave not in _CACHE:
        s = skia.Surface(int(w), int(h)); c = s.getCanvas(); c.clear(skia.ColorTRANSPARENT)
        desenha(c)
        _CACHE[chave] = s.makeImageSnapshot()
    return _CACHE[chave]


def _blit(cv, img, x, y, a=1.0):
    if a <= 0:
        return
    if a >= 1:
        cv.drawImage(img, x, y)
    else:
        cv.drawImage(img, x, y, skia.SamplingOptions(), _alfa(a))


def fundo_cl(cv, t):
    """(cópia do piloto) Fundo do cf_alongamento com o degradê pronto em imagem."""
    def d(c):
        sh = skia.GradientShader.MakeRadial(skia.Point(W / 2, H * 0.42 + 60), H * 0.78, [_c("#17384C"), _c(BG_OUT)])
        c.drawRect(skia.Rect(0, 0, W, H + 120), paint("#17384C", shader=sh))
    _blit(cv, _img("fundo", W, H + 120, d), 0, -60 + 40 * math.sin(t * 0.3))
    for x, y, v, r, a in PART:
        yy = (y - v * t * 6) % H
        cv.drawCircle(x + 8 * math.sin(t * 0.5 + y), yy, r, paint("#BFE3FF", int(a)))


def _rel(c):
    c.translate(-CENA.left(), -CENA.top())


def monitor_fundo(cv):
    def d(c):
        _rel(c)
        c.drawRect(CENA, paint("#FFFFFF", 9))
    _blit(cv, _img("monitor", CENA.width(), CENA.height(), d), CENA.left(), CENA.top())


def vinheta(cv):
    def d(c):
        _rel(c)
        sh = skia.GradientShader.MakeRadial(skia.Point(540, 780), 760, [_c("#000000", 0), _c("#000000", 0), _c("#000000", 70)],
                                            [0.0, 0.6, 1.0])
        c.drawRect(CENA, paint("#000000", 255, shader=sh))
    _blit(cv, _img("vinheta", CENA.width(), CENA.height(), d), CENA.left(), CENA.top())


def varredura(cv, t, ambar):
    """(cópia do piloto) Linhas de varredura + granulação (semente = índice do quadro) + moldura âmbar."""
    if ambar > 0:
        def d(c):
            _rel(c)
            sh = skia.GradientShader.MakeRadial(skia.Point(540, 780), 720,
                                                [_c(AMBAR, 0), _c(AMBAR, 0), _c(AMBAR, 70), _c(AMBAR, 150)],
                                                [0.0, 0.5, 0.85, 1.0])
            c.drawRect(CENA, paint(AMBAR, 255, shader=sh))
            r = skia.Rect(CENA.left() + 6, CENA.top() + 6, CENA.right() - 6, CENA.bottom() - 6)
            c.drawRect(r, paint(AMBAR, 230, "stroke", 5))
            c.drawRect(CENA, paint(AMBAR, 18))
        _blit(cv, _img("ambar", CENA.width(), CENA.height(), d), CENA.left(), CENA.top(), ambar)

    def dl(c):
        _rel(c)
        lin = skia.Path()
        y = CENA.top() + 2
        while y < CENA.bottom():
            lin.moveTo(CENA.left(), y); lin.lineTo(CENA.right(), y); y += 6
        c.drawPath(lin, paint("#000000", 20, "stroke", 2))
    _blit(cv, _img("linhas", CENA.width(), CENA.height(), dl), CENA.left(), CENA.top())
    rng = np.random.default_rng(int(round(t * FPS)) + 1)
    xs = rng.uniform(CENA.left(), CENA.right(), 340); ys = rng.uniform(CENA.top(), CENA.bottom(), 340)
    pts = [skia.Point(float(a), float(b)) for a, b in zip(xs, ys)]
    cv.drawPoints(skia.Canvas.kPoints_PointMode, pts[:170], paint("#FFFFFF", 30, "stroke", 2.2))
    cv.drawPoints(skia.Canvas.kPoints_PointMode, pts[170:], paint("#000000", 36, "stroke", 2.2))


def faixas_tracking(cv, t, a):
    """(cópia do piloto) Faixas de 'tracking' de fita de vídeo varrendo a cena (voltar e avançar a fita)."""
    if a <= 0:
        return
    for i in range(3):
        y = CENA.top() + ((t * 1300 + i * 330) % (CENA.height() + 60)) - 30
        h = 18 + 10 * i
        cv.drawRect(skia.Rect(CENA.left(), y, CENA.right(), y + h), paint("#FFFFFF", int(46 * a)))
        cv.drawRect(skia.Rect(CENA.left(), y + h, CENA.right(), y + h + 4), paint("#000000", int(70 * a)))


def cantoneiras(cv, a):
    """(cópia do piloto, com sombra: o trocador é claro)"""
    if a <= 0:
        return
    r = CENA; L = 60
    for cor, alfa, larg in (("#000000", 90, 9), ("#FFFFFF", 170, 5)):
        pt = paint(cor, int(alfa * a), "stroke", larg)
        pt.setStrokeCap(skia.Paint.kSquare_Cap)
        for x, y, sx, sy in ((r.left(), r.top(), 1, 1), (r.right(), r.top(), -1, 1),
                             (r.left(), r.bottom(), 1, -1), (r.right(), r.bottom(), -1, -1)):
            p = skia.Path(); p.moveTo(x, y + sy * L); p.lineTo(x, y); p.lineTo(x + sx * L, y)
            cv.drawPath(p, pt)


def flash(cv, t, t0, forte=1.0):
    k = t - t0
    if 0 <= k < 0.1:
        img = _img("flash", CENA.width(), CENA.height(), lambda c: c.clear(_c("#FFFFFF", 255)))
        _blit(cv, img, CENA.left(), CENA.top(), 0.52 * forte * (1 - k / 0.1))


# ------------------------------------------------------------------ painel do replay (cronômetro + velocidade; cópias do piloto)
def relogio(cv, x, y, r, a, ang):
    """Relógio de ponteiros, sem números. (cópia do piloto / cf_andador)"""
    if a <= 0:
        return
    cv.drawCircle(x, y, r + 4, paint("#000000", int(70 * a), blur=8))
    cv.drawCircle(x, y, r, paint("#EEF3F8", int(255 * a)))
    cv.drawCircle(x, y, r, paint(OURO, int(255 * a), "stroke", 5))
    for i in range(12):
        q = i * math.pi / 6
        r0 = r * (0.74 if i % 3 == 0 else 0.82)
        cv.drawLine(x + r0 * math.cos(q), y + r0 * math.sin(q), x + r * 0.88 * math.cos(q), y + r * 0.88 * math.sin(q),
                    paint("#5E7186", int(230 * a), "stroke", 3 if i % 3 == 0 else 2))
    cv.drawLine(x, y, x + r * 0.45 * math.cos(ang / 12 - 1.9), y + r * 0.45 * math.sin(ang / 12 - 1.9),
                paint("#16324A", int(255 * a), "stroke", 6))
    cv.drawLine(x, y, x + r * 0.7 * math.cos(ang - math.pi / 2), y + r * 0.7 * math.sin(ang - math.pi / 2),
                paint("#16324A", int(255 * a), "stroke", 4))
    cv.drawCircle(x, y, 5, paint(OURO, int(255 * a)))


TAM_CHIP = 50


def chip_dim(s, tam=TAM_CHIP):
    lw = skia.Font(F_BLACK, tam).measureText(s)
    return lw, lw + 34, tam * 1.34


def chip_c(cv, s, cx, cy, a, tam=TAM_CHIP, dim=1.0, esc=1.0):
    """Rótulo de velocidade CENTRADO em (cx, cy). (cópia do piloto)"""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam)
    lw, w, h = chip_dim(s, tam)
    cv.save(); cv.translate(cx, cy); cv.scale(esc, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-w / 2, -h / 2, w / 2, h / 2), 14, 14)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(230 * a)))
    cv.drawRRect(rr, paint(OURO, int(255 * a * dim), "stroke", 3.5))
    cv.drawString(s, -lw / 2, tam * 0.36, f, paint(OURO, int(255 * a * dim)))
    cv.restore()


def _setas(cv, x, y, a, esc, para_frente):
    """◀◀ ou ▶▶ desenhado (a fonte não tem o símbolo). (cópia do piloto)"""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    for dx in (0, 30):
        p = skia.Path()
        if para_frente:
            p.moveTo(dx, -18); p.lineTo(dx + 30, 0); p.lineTo(dx, 18)
        else:
            p.moveTo(dx + 30, -18); p.lineTo(dx, 0); p.lineTo(dx + 30, 18)
        p.close()
        if esc > 1.5:
            cv.drawPath(p, paint("#000000", int(140 * a), "stroke", 5))
        cv.drawPath(p, paint("#FFFFFF", int(255 * a)))
    cv.restore()


HUD_X, HUD_Y = 786, 1172                                          # centro do relógio (abaixo do trocador)
POP_ESC = 2.5                                                    # tamanho do "0,25×" grande (e_back passa ~10%)
POP_Y = 1190                                                     # v3: o "0,25×" grande nasce ABAIXO dos pés


def _chip_hud_c(s):
    _, w, _ = chip_dim(s)
    return HUD_X + 50 + w / 2, HUD_Y


def _pop_c(s):
    """Onde o "0,25×" grande aparece (v3, correção de 01/11). Antes nascia no meio da cena (540, 600), sobre a fralda
    e o alto das coxas, e descia em linha reta até o painel ATRAVESSANDO a perna da direita (coxa, canela e pé). Agora
    nasce na faixa de baixo do monitor (fim do trocador + tampo de madeira), abaixo da ponta dos dedos e à esquerda
    do relógio, e só desliza para a direita até a vaga ao lado do relógio: nunca passa por cima do bebê.
    Conferido no quadro: com o tranco do e_back (x1,1) o topo do selo fica em ~1098, abaixo dos dedos (~1084 com a
    câmera ainda em 1×; sobem quando ela abre) e dos pontos dourados; a base fica acima da legenda karaokê."""
    _, w, _ = chip_dim(s)
    return min(540.0, HUD_X - 34 - 14 - POP_ESC * 1.1 * w / 2), POP_Y


def painel(cv, t, T, F, a):
    """(cópia adaptada do piloto)"""
    if a <= 0:
        return
    tipo = F.tipo(t)
    relogio(cv, HUD_X, HUD_Y, 34, a, F.relogio(t) * 2 * math.pi)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(HUD_X - 7, HUD_Y - 50, HUD_X + 7, HUD_Y - 38), 3, 3), paint(OURO, int(255 * a)))
    t0 = F.inicio_trecho(t)
    if tipo in ("volta", "avanca"):
        _setas(cv, HUD_X + 52, HUD_Y, a * (0.75 + 0.25 * math.sin(t * 18)), 1.25, tipo == "avanca")
        return
    if tipo == "congela":                                         # o rótulo do trecho, apagado
        s = R_LENTA if lento_k(t, T) > 0 else R_1X
        chip_c(cv, s, *_chip_hud_c(s), a, dim=0.4)
        return
    s = R_LENTA if tipo == "lenta" else R_1X
    hx, hy = _chip_hud_c(s)
    k = t - t0
    if tipo == "lenta" and k < 0.75:                              # "0,25×" grande embaixo, que desliza para o painel
        cx, cy = _pop_c(s)
        if k < 0.32:
            chip_c(cv, s, cx, cy, a, esc=POP_ESC * e_back(clamp(k / 0.16)))
        else:
            v = e_inout(prog(k, 0.32, 0.75))
            chip_c(cv, s, lerp(cx, hx, v), lerp(cy, hy, v), a, esc=lerp(POP_ESC, 1.0, v))
        return
    pop = 1 + 0.6 * (1 - e_out(prog(t, t0, t0 + 0.3))) if t0 > 0 and t0 != F.t_rep and t0 != F.t_calma else 1.0
    chip_c(cv, s, hx, hy, a, esc=pop)


# ------------------------------------------------------------------ marcações do comentarista (cópias do piloto)
def circulo_mao(cv, cx, cy, rx, ry, k, a, larg=7):
    """Círculo dourado traçado à mão (traço irregular, com pontinha de sobra)."""
    if a <= 0 or k <= 0:
        return
    p = skia.Path(); n = 52
    for i in range(n + 1):
        u = i / n
        ang = -2.4 + u * 2 * math.pi * 1.1
        rr = 1 + 0.05 * math.sin(u * 9) + 0.07 * u
        px, py = cx + rx * rr * math.cos(ang), cy + ry * rr * math.sin(ang)
        (p.moveTo if i == 0 else p.lineTo)(px, py)
    cv.drawPath(p, _trim(paint("#000000", int(110 * a), "stroke", larg + 6, blur=4), e_out(k)))
    cv.drawPath(p, _trim(paint(OURO, int(255 * a), "stroke", larg), e_out(k)))


def estetoscopio(cv, x, y, esc, a):
    """Selo branco e calmo: estetoscópio desenhado (forma, sem texto). (cópia do piloto)"""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    cv.drawCircle(0, 0, 60, paint("#000000", int(80 * a), blur=10))
    cv.drawCircle(0, 0, 56, paint(FUNDO_CARTAO, int(235 * a)))
    cv.drawCircle(0, 0, 56, paint("#FFFFFF", int(255 * a), "stroke", 4))
    br = paint("#FFFFFF", int(255 * a), "stroke", 5.5)
    for sx in (-1, 1):
        p = skia.Path(); p.moveTo(17 * sx, -30)
        p.cubicTo(20 * sx, -8, 15 * sx, 8, 0, 10)
        cv.drawPath(p, br)
        cv.drawCircle(17 * sx, -33, 4.5, paint("#FFFFFF", int(255 * a)))
    p = skia.Path(); p.moveTo(0, 10); p.cubicTo(0, 34, 30, 36, 30, 16)
    cv.drawPath(p, br)
    cv.drawCircle(30, 7, 11, paint(OURO, int(255 * a)))
    cv.drawCircle(30, 7, 5, paint("#8A6512", int(255 * a)))
    cv.restore()


def anel_ouro(cv, x, y, r, t, t0, a):
    """Anel dourado pulsando em volta de um ícone (a consulta 'acende')."""
    a = a * prog(t, t0, t0 + 0.25)
    if a <= 0:
        return
    pul = 0.5 + 0.5 * math.sin((t - t0) * 5.5)
    cv.drawCircle(x, y, r + 8 * pul, paint(OURO, int(120 * a * (0.5 + 0.5 * pul)), "stroke", 10, blur=6))
    cv.drawCircle(x, y, r + 8 * pul, paint(OURO, int(255 * a), "stroke", 5))


def ponto_ouro(cv, x, y, a, r=13):
    if a <= 0:
        return
    cv.drawCircle(x, y, r + 10, paint(OURO, int(90 * a), blur=10))
    cv.drawCircle(x, y, r, paint(OURO, int(255 * a)))
    cv.drawCircle(x, y, r, paint(FUNDO_CARTAO, int(255 * a), "stroke", 3))


def pontilhado(cv, pts, cor, a, larg=8.0, passo=19.0, sombra=True):
    """Arco pontilhado (pontos redondos) em coordenadas de TELA (como a trilha do piloto)."""
    if a <= 0 or len(pts) < 2:
        return
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if sombra:                                                    # aro escuro em cada ponto (trocador claro)
        ps = paint(NAVY, int(170 * a), "stroke", larg + 5)
        ps.setPathEffect(skia.DashPathEffect.Make([0.5, passo], 0))
        cv.drawPath(p, ps)
    pt = paint(cor, int(255 * a), "stroke", larg)
    pt.setPathEffect(skia.DashPathEffect.Make([0.5, passo], 0))
    cv.drawPath(p, pt)


def carimbo(cv, s, x, y, rot_, t0, t, dur, tam=62, desfaz=None):
    """Carimbo dourado (cópia adaptada do carimbo_ouro do cf_fratura_cola / cf_comum.carimbo): tamanho ajustável;
    `desfaz` = (t0, t1): o carimbo se desfaz em borrão (avanço rápido)."""
    k = t - t0
    if k < 0 or k > dur:
        return
    esc = lerp(1.6, 1.0, e_out(clamp(k / 0.16))); a = clamp(k / 0.08) * (1 - prog(k, dur - 0.35, dur))
    bl, sx = 0.0, 1.0
    if desfaz:
        d = prog(t, *desfaz)
        a *= 1 - d; bl = 26 * d; sx = 1 + 0.4 * d
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam)
    lw = f.measureText(s)
    if bl > 0.3:
        pb = skia.Paint(); pb.setImageFilter(skia.ImageFilters.Blur(bl, bl * 0.25)); cv.saveLayer(None, pb)
    else:
        cv.save()
    cv.translate(x, y); cv.rotate(rot_); cv.scale(esc * sx, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 24, -tam, lw / 2 + 24, tam * 0.36), 12, 12)
    cv.drawRRect(rr, paint("#0B1824", int(175 * a))); cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 7))
    cv.drawString(s, -lw / 2, 0, f, paint(OURO, int(255 * a)))
    cv.restore()


def selo_lenta(cv, lk):
    """(cópia do piloto) O selo da série, aceso só com a câmera lenta ligada."""
    if lk <= 0:
        return
    esc = lerp(0.55, 1.0, e_back(lk))
    cv.save(); cv.translate(CX, 177); cv.scale(esc, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-205, -31, 205, 31), 31, 31)
    cv.drawRRect(rr, paint(AMBAR, int(90 * lk), blur=16))
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(225 * lk)))
    cv.drawRRect(rr, paint(AMBAR, int(60 * lk)))
    cv.drawRRect(rr, paint(OURO, int(255 * lk), "stroke", 3.5))
    texto(cv, R_SELO, 0, 14, F_BLACK, 38, OURO, int(255 * lk))
    cv.restore()


# ------------------------------------------------------------------ o mundo (dentro do monitor)
DELTA_F = {"play": 0.16, "avanca": 0.26, "volta": 0.14}          # borrão: quanto FILME cabe no "obturador"
N_AMOSTRAS = 18                   # v4: amostras do RASTRO, bem próximas (antes 6 poses inteiras empilhadas)
RASTRO_A = 0.40                   # v4: opacidade da amostra mais nova do rastro (a mais velha vai a 0)
RASTRO_COR = lerpc(PELE_CL, "#FFFFFF", 0.55)                    # v4: pele bem CLARA, quase branca (rastro, nunca halo avermelhado)
RASTRO_BLUR = 3.5                 # v4: desfoque do rastro (unidades locais do bebê): sem degraus entre amostras
CAIXA_PERNAS = skia.Rect(-60, 360, 1140, 1000)                    # (local do bebê)


def amostras_borrao(t, F):
    """Instantes (vídeo) que entram no borrão de movimento de `t`, do mais novo ao mais velho: só 1×, voltando
    ou avançando, sem atravessar congelamento nem salto de filme, e nunca antes de t = 0 (quadro 0 nítido).
    O chute calmo não borra (é lento)."""
    seg = F.seg(t)
    tipo = seg[2]
    if tipo not in DELTA_F or seg[3] >= CALMA:
        return [t]
    vel = abs(seg[4] - seg[3]) / max(1e-6, seg[1] - seg[0])
    obt = min(0.16, DELTA_F[tipo] / max(vel, 1e-6))
    out = [t]
    for i in range(1, N_AMOSTRAS):
        tg = t - obt * i / (N_AMOSTRAS - 1)
        if tg < 0:
            break
        sg = F.seg(tg)
        if sg is not seg and (sg[2] == "congela" or abs(sg[4] - seg[3]) > 1e-6):
            break
        out.append(tg)
    return out


def pernas(cv, ps, sombra=True):
    the, lae, thd, lad = ps
    perna_bebe(cv, HQ[0], the, lae, 1, [y * lae for y in DOBRAS_E], pe_esc=1 + 0.35 * (1 - lae), sombra=sombra)
    perna_bebe(cv, HQ[1], -thd, K_CURTA * lad, -1, [y * lad for y in DOBRAS_D], pe_esc=1 + 0.35 * (1 - lad),
               sombra=sombra)


def silhueta_perna(cv, hx, ang, k, dentro, pe_esc, pt):
    """v4: só a MANCHA da perna (coxa+canela, pé e dedos cheios, mesma geometria de `perna_bebe`), sem contorno,
    sem dobrinha, sem joelho e sem sombra: a matéria do rastro de movimento."""
    cv.save(); cv.translate(hx, HY); cv.rotate(ang)
    pe_top = PE_Y0 * k
    cv.drawPath(_perna_path(k), pt)
    cv.save(); cv.translate(0, pe_top + 40); cv.scale(pe_esc, pe_esc); cv.translate(0, -(pe_top + 40))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-44, pe_top, 44, pe_top + 80), 40, 40), pt)
    for i, (fx, r) in enumerate(((-29, 9), (-15, 9.5), (-1, 10), (14, 11), (30, 13))):
        cv.drawCircle(fx * dentro, pe_top + 74 - (2 if i == 4 else 0), r, pt)
    cv.restore()
    cv.restore()


def pernas_borradas(cv, t, F):
    """Borrão de movimento do 1×, do ◀◀ e do ▶▶: a pose do instante NÍTIDA por cima de um RASTRO contínuo.
    v4 (correção de 01/11, 2ª rodada): antes eram 6 poses INTEIRAS empilhadas (contorno, dedos e sombra em cada
    uma) e, pausado, o bebê parecia ter vários pés. Agora as amostras de dentro do obturador (18, bem próximas) viram
    só manchas de pele bem clara, sem contorno nem dedos desenhados, cada vez mais apagadas quanto mais velhas e
    desfocadas juntas numa camada: um rastro liso atrás do pé, que dá a sensação de 'rápido' sem duplicar o pé."""
    ams = amostras_borrao(t, F)
    if len(ams) > 1:
        pl = skia.Paint(); pl.setImageFilter(skia.ImageFilters.Blur(RASTRO_BLUR, RASTRO_BLUR))
        cv.saveLayer(CAIXA_PERNAS, pl)
        n = len(ams) - 1
        for i in range(n, 0, -1):                                  # do mais velho ao mais novo (sem o instante)
            the, lae, thd, lad = pose_video(ams[i], F)
            pt = paint(RASTRO_COR, int(255 * RASTRO_A * (1 - (i - 1) / (N_AMOSTRAS - 1))))
            silhueta_perna(cv, HQ[0], the, lae, 1, 1 + 0.35 * (1 - lae), pt)
            silhueta_perna(cv, HQ[1], -thd, K_CURTA * lad, -1, 1 + 0.35 * (1 - lad), pt)
        cv.restore()
    pernas(cv, pose_video(t, F))


def a_marcas(t, T, F):
    """Alfa das marcas da câmera lenta: entram com a lentidão e somem no avanço rápido."""
    return prog(t, T["lenta"], T["lenta"] + 0.15) * (1 - prog(t, T["pressa"] - 0.05, T["pressa"] + 0.2))


def leques(cv, t, T, F):
    """(local, SOB as pernas e a fralda) Leque dourado translúcido de cada perna: QUANTO cada uma abriu. No
    congelamento, o pedaço que FALTA do lado curto aparece em branco com contorno tracejado."""
    a = a_marcas(t, T, F)
    if a <= 0 or t < T["lenta"]:
        return
    tf = F.tf(t) if t < T["pressa"] else F.tf_fz1
    if tf < OPEN0:                                                 # só o lance da ABERTURA ganha leque
        return
    ps = pose(tf)
    a_v = a * prog(t, F.t_fz + 0.05, F.t_fz + 0.3)
    if a_v > 0:                                                    # o pedaço que falta (lado curto)
        p = leque_path("D", ABRE_D, ABRE_E, r_arco("D"))
        cv.drawPath(p, paint("#FFFFFF", int(255 * a_v), shader=_rastro("D", "#FFFFFF", 0.95)))
        pd = paint(NAVY, int(150 * a_v), "stroke", 4); pd.setPathEffect(skia.DashPathEffect.Make([14, 10], 0))
        q = skia.Path(); q.moveTo(*ponto_perna("D", ABRE_E, 1.0, r_arco("D") * 0.42))
        q.lineTo(*ponto_perna("D", ABRE_E, 1.0, r_arco("D")))
        cv.drawPath(q, pd)
    for lado, th in (("E", ps[0]), ("D", ps[2])):
        if th > REST + 0.3:
            p = leque_path(lado, REST, th, r_arco(lado))
            cv.drawPath(p, paint(OURO, int(255 * a), shader=_rastro(lado, OURO, 0.88)))


def _rastro(lado, cor, forte):
    """Degradê radial a partir do quadril: transparente perto do quadril, forte no arco do pé (rastro do pé)."""
    hx = HQ[0] if lado == "E" else HQ[1]
    r = r_arco(lado)
    return skia.GradientShader.MakeRadial(skia.Point(hx, HY), r, [_c(cor, 0), _c(cor, int(60 * forte)), _c(cor, int(255 * forte))],
                                          [0.0, 0.3, 1.0])


def mundo(cv, t, T, F, cam):
    """Trocador, barriga, leques, pernas (borradas no 1×, nítidas na lenta) e fralda (referencial do mundo)."""
    trocador(cv)
    cv.save(); bebe_aplica(cv)
    tronco(cv)
    leques(cv, t, T, F)
    if F.tipo(t) in DELTA_F:
        pernas_borradas(cv, t, F)
    else:
        pernas(cv, pose_video(t, F))
    fralda(cv)
    cv.restore()


def marcas_lenta(cv, t, T, F, cam):
    """Câmera lenta: pontos dourados nos pés, arcos pontilhados, tracinho onde a da direita para, o vão que
    sobra (pontilhado branco) e o círculo do comentarista. Tudo sai junto com a lentidão."""
    a = a_marcas(t, T, F)
    if a <= 0 or t < T["lenta"]:
        return
    tf = F.tf(t) if t < T["pressa"] else F.tf_fz1
    ps = pose(tf)
    for lado, th in (("E", ps[0]), ("D", ps[2])):
        if th > REST + 0.3 and tf >= OPEN0:
            pts = [tela(cam, *q) for q in arco_pts(lado, REST, th, r_arco(lado))]
            pontilhado(cv, pts, OURO, a, larg=11, passo=24)
    if t >= F.t_para:                                               # o ponto em que a da direita PARA
        k = prog(t, F.t_para, F.t_para + 0.15)
        d = r_arco("D")
        p0 = tela(cam, *ponto_perna("D", ABRE_D, 1.0, d - 30 * k))
        p1 = tela(cam, *ponto_perna("D", ABRE_D, 1.0, d + 30 * k))
        cv.drawLine(*p0, *p1, paint(NAVY, int(170 * a), "stroke", 15))
        cv.drawLine(*p0, *p1, paint(OURO, int(255 * a), "stroke", 9))
    a_v = a * prog(t, F.t_fz + 0.05, F.t_fz + 0.3)                  # o vão: até onde o outro lado chegou
    if a_v > 0:
        pts = [tela(cam, *q) for q in arco_pts("D", ABRE_D, ABRE_E, r_arco("D"))]
        pontilhado(cv, pts, "#FFFFFF", a_v * 0.9, larg=9, passo=24, sombra=True)
    for lado, th, kk in (("E", ps[0], ps[1]), ("D", ps[2], ps[3])):
        # v4: o ponto GRUDA no pé também enquanto o joelho ainda está dobrado (início da lenta, k < 1): antes ficava
        # no raio da perna esticada, solto abaixo do pé; com k = 1 (abertura, congelamento) é o mesmo r_arco de antes
        r = r_arco(lado) - (PE_Y0 - 47 * 0.35) * (1 - kk)
        ponto_ouro(cv, *tela(cam, *ponto_perna(lado, th, 1.0, r)), a)
    a_c = a * prog(t, F.t_fz + 0.06, F.t_fz + 0.1)
    if a_c > 0:                                                      # círculo: o arco curto + o vão que sobra
        pts = [tela(cam, *q) for q in arco_pts("D", ABRE_D - 4, ABRE_E, r_arco("D"))]
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        cx_, cy_ = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        circulo_mao(cv, cx_, cy_, (max(xs) - min(xs)) / 2 + 44, (max(ys) - min(ys)) / 2 + 46,
                    prog(t, F.t_fz + 0.08, F.t_fz + 0.43), a_c)


def monitor(cv, t, T, F, passos, limpo=False):
    """Tudo o que fica DENTRO do monitor de replay (recortado em CENA). -> câmera. `limpo`: sem fita, âmbar,
    granulação nem flash (para a miniatura da polaroide)."""
    tipo = F.tipo(t)
    cam = camera(t, passos)
    if tipo == "volta" and not limpo:                             # tremidinha de fita voltando
        j = math.sin(t * 97) * 4 + math.sin(t * 41) * 3
        cam = (cam[0], cam[1], cam[2], cam[3] + j, cam[4])
    cv.save(); cv.clipRect(CENA, True)
    monitor_fundo(cv)
    cv.save(); aplica(cv, cam)
    mundo(cv, t, T, F, cam)
    cv.restore()
    vinheta(cv)
    marcas_lenta(cv, t, T, F, cam)
    if not limpo:
        varredura(cv, t, lento_k(t, T))
        faixas_tracking(cv, t, {"volta": 1.0, "avanca": 0.7}.get(tipo, 0.0))
        if tipo in ("volta", "avanca"):                           # ◀◀ / ▶▶ grande no canto, letreiro do videocassete
            t0 = F.inicio_trecho(t)
            _setas(cv, 96, 410, (0.55 + 0.45 * (math.sin((t - t0) * 16) > -0.3)) * prog(t, t0, t0 + 0.06), 2.2,
                   tipo == "avanca")
        flash(cv, t, F.t_fz, 1.0)
    cv.restore()
    return cam


# ------------------------------------------------------------------ fecho: UM cartão CLARO grande à direita
CARTAO_R = skia.Rect(522, 405, 1018, 935)
CC = ((CARTAO_R.left() + CARTAO_R.right()) / 2, (CARTAO_R.top() + CARTAO_R.bottom()) / 2)


def cartao(cv, dx, a):
    if a <= 0:
        return
    r = skia.Rect(CARTAO_R.left() + dx, CARTAO_R.top(), CARTAO_R.right() + dx, CARTAO_R.bottom())
    rr = skia.RRect.MakeRectXY(r, 34, 34)
    cv.drawRRect(rr, paint("#000000", int(90 * a), blur=16))
    cv.drawRRect(rr, paint(CARTAO, int(255 * a)))
    cv.drawRRect(rr, paint(CARTAO_BORDA, int(255 * a), "stroke", 3))


def _entra_sai(t, t_in, t_out):
    """-> (deslocamento x, alfa) de um cartão que entra pela direita e sai pela direita."""
    ki = e_out(prog(t, t_in, t_in + 0.45)); ko = e_inout(prog(t, t_out, t_out + 0.35))
    return 540 * (1 - ki) + 540 * ko, clamp(ki * 2) * (1 - ko)


def _troca(t, t_in, t_out):
    """Conteúdo do cartão: entra com um pop em t_in e some em t_out. -> (escala, alfa)."""
    if t < t_in - 0.01 or t > t_out + 0.2:
        return 0.0, 0.0
    return max(0.01, e_back(prog(t, t_in, t_in + 0.35))), prog(t, t_in, t_in + 0.12) * (1 - prog(t, t_out, t_out + 0.2))


R_CONCHA, R_BOLA, E_PICTO = 96.0, 75.0, 1.5
BOLA_FORA = (80.0, -58.0)                     # onde a bolinha PARA: na borda, sem assentar (pictograma local)


def encaixe_picto(cv, cx, cy, t, T, a, esc):
    """'O quadril que não encaixa': PICTOGRAMA de brinquedo fora do corpo. Conchinha de contorno dourado; a bolinha
    marfim desce no "quadril" e PARA NA BORDA no "encaixa" (não assenta: nada de conserto prometido); o lugar onde
    ela assentaria aparece tracejado. Sem osso, sem fundo escuro, sem clique."""
    if a <= 0:
        return
    cv.save(); cv.translate(cx, cy); cv.scale(esc * E_PICTO, esc * E_PICTO)
    r = skia.Rect(-R_CONCHA, -R_CONCHA, R_CONCHA, R_CONCHA)
    tig = skia.Path(); tig.addArc(r, 0, 180)
    cv.drawPath(tig, paint("#FBEFD2", int(255 * a)))
    cv.drawArc(r, -8, 196, False, paint(OURO, int(255 * a), "stroke", 13))
    cv.drawArc(r, -8, 196, False, paint("#B8862A", int(255 * a), "stroke", 3))
    a_l = a * prog(t, T["encaixa"] + 0.35, T["encaixa"] + 0.6)          # o lugar vazio, tracejado
    if a_l > 0:
        pl = paint(TINTA, int(200 * a_l), "stroke", 5); pl.setPathEffect(skia.DashPathEffect.Make([14, 11], 0))
        cv.drawCircle(0, R_CONCHA - R_BOLA, R_BOLA - 4, pl)
    k = e_inout(prog(t, T["quadril2"], T["encaixa"] + 0.15))           # desce e para na borda
    p0, p1, p2 = (95.0, -125.0), (95.0, -90.0), BOLA_FORA
    bx = (1 - k) ** 2 * p0[0] + 2 * (1 - k) * k * p1[0] + k * k * p2[0]
    by = (1 - k) ** 2 * p0[1] + 2 * (1 - k) * k * p1[1] + k * k * p2[1]
    kb = t - (T["encaixa"] + 0.15)
    if kb > 0:                                                          # balança de leve na borda (vivo, calmo)
        bx += 4 * math.sin(kb * 9) * math.exp(-kb / 0.5) + 1.5 * math.sin(kb * 2.6)
    cv.drawCircle(bx + 5, by + 8, R_BOLA, paint("#000000", int(50 * a), blur=8))
    sh = skia.GradientShader.MakeRadial(skia.Point(bx - 20, by - 22), R_BOLA * 1.6,
                                        [_c("#FFFDF6"), _c(MARFIM), _c(MARFIM_ESC)], [0.0, 0.45, 1.0])
    cv.drawCircle(bx, by, R_BOLA, paint(MARFIM, int(255 * a), shader=sh))
    cv.drawCircle(bx, by, R_BOLA, paint(MARFIM_LINHA, int(220 * a), "stroke", 3))
    cv.drawArc(r, 20, 140, False, paint(OURO, int(255 * a), "stroke", 13))   # borda da frente da tigela
    cv.restore()


def calendario_cedo(cv, x, y, t, T, a, esc):
    """Calendário SEM números e SEM vermelho: as primeiras colunas acendem em dourado, uma por vez ("primeiros
    meses")."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    w, h = 250, 210
    r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2)
    cv.drawRRect(skia.RRect.MakeRectXY(r.makeOffset(4, 6), 18, 18), paint("#000000", int(60 * a), blur=10))
    cv.drawRRect(skia.RRect.MakeRectXY(r, 18, 18), paint("#FFFFFF", int(255 * a)))
    cv.drawRRect(skia.RRect.MakeRectXY(r, 18, 18), paint(CARTAO_BORDA, int(255 * a), "stroke", 3))
    cv.save(); cv.clipRRect(skia.RRect.MakeRectXY(r, 18, 18), True)
    cv.drawRect(skia.Rect(-w / 2, -h / 2, w / 2, -h / 2 + 44), paint(AZUL_CL, int(255 * a)))
    cv.restore()
    for xx in (-60, 60):
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(xx - 7, -h / 2 - 14, xx + 7, -h / 2 + 16), 4, 4), paint("#5E7186", int(255 * a)))
    acesas = (prog(t, T["primeiros"], T["primeiros"] + 0.2), prog(t, T["meses"], T["meses"] + 0.2))
    cw, ch, gx, gy = 44, 34, 12, 12
    x0 = -(4 * cw + 3 * gx) / 2; y0 = -h / 2 + 60
    for c in range(4):
        k = acesas[c] if c < 2 else 0.0
        for rr_ in range(3):
            cel = skia.RRect.MakeRectXY(skia.Rect(x0 + c * (cw + gx), y0 + rr_ * (ch + gy),
                                                  x0 + c * (cw + gx) + cw, y0 + rr_ * (ch + gy) + ch), 7, 7)
            cv.drawRRect(cel, paint(lerpc("#CDD8E2", OURO, k), int(255 * a)))
            if k > 0:
                cv.drawRRect(cel, paint(OURO, int(120 * a * k), "stroke", 6, blur=4))
    cv.restore()


def fecho(cv, t, T, F, cam):
    """O cartão claro grande (entra no "displasia", sai no "dúvida") com 3 conteúdos, um por vez."""
    dx, a = _entra_sai(t, T["displasia"] - 0.15, T["duvida"] - 0.2)
    if a <= 0:
        return
    hx, hy = tela(cam, HQ[1], HY)                                     # o quadril do lado CURTO (sob a fralda)
    k_fio = prog(t, T["displasia"] + 0.25, T["displasia"] + 0.6) * a * (1 - prog(t, T["avaliacao"] - 0.2, T["avaliacao"]))
    if k_fio > 0:
        bx, by = CARTAO_R.left() + dx, CC[1] + 30
        xf, yf = lerp(hx, bx, e_out(k_fio)), lerp(hy, by, e_out(k_fio))
        pf = paint(OURO, int(255 * k_fio), "stroke", 6); pf.setPathEffect(skia.DashPathEffect.Make([14, 10], -t * 30))
        cv.drawLine(hx, hy, xf, yf, paint("#000000", int(70 * k_fio), "stroke", 10, blur=3))
        cv.drawLine(hx, hy, xf, yf, pf)
        ponto_ouro(cv, hx, hy, k_fio, r=12)
    cartao(cv, dx, a)
    cx, cy = CC[0] + dx, CC[1]
    esc, ae = _troca(t, T["displasia"] - 0.15, T["avaliacao"] - 0.2)
    encaixe_picto(cv, cx - 20, cy + 60, t, T, a * ae, 1.0 if t > T["displasia"] + 0.2 else esc)
    esc, ast = _troca(t, T["avaliacao"], T["identificado"] - 0.2)
    if ast > 0:
        anel_ouro(cv, cx, cy, 170, t, T["avaliacao"] + 0.3, a * ast)
        estetoscopio(cv, cx, cy, 2.55 * esc, a * ast)
    esc, acl = _troca(t, T["identificado"], T["duvida"] - 0.2)
    if acl > 0:
        calendario_cedo(cv, cx, cy + 20, t, T, a * acl, 1.75 * esc)
        brilhos(cv, cx, cy + 20, t, T["simples"], n=14, raio=230)


# ------------------------------------------------------------------ "na dúvida": polaroide do congelamento (cópia adaptada do piloto)
def miniatura(T, F, passos, tt):
    """O congelamento do instante `tt`, já desenhado (sem texto: o painel e o karaokê ficam fora do monitor)."""
    chave = ("mini", round(tt, 3))
    if chave not in _CACHE:
        sf = skia.Surface(int(CENA.width()), int(CENA.height())); c = sf.getCanvas(); c.clear(_c(BG_OUT))
        c.translate(-CENA.left(), -CENA.top())
        monitor(c, tt, T, F, passos, limpo=True)
        _CACHE[chave] = sf.makeImageSnapshot()
    return _CACHE[chave]


MW, MH = 640.0, 576.0                                             # polaroide (proporção da CENA)
POL_C = (520.0, 745.0)
# v5 (3ª rodada de 01/11): a saída da polaroide passa por FUNDO ESCURO (instantes relativos a F.t_rep, o replay limpo)
REC_PRETO = (-0.45, -0.30)        # o escurecido vai de 0,7 a 1,0 (opaco): o bebê do fundo some ANTES da foto sair
REC_SAI = (-0.30, -0.12)          # a polaroide e o estetoscópio somem SOBRE o escuro total (nada atrás deles)
REC_CAM = (-0.28, 0.14)           # (início, duração) do recuo -> BASE da câmera: todo dentro do escuro total
REC_CLAREIA = (-0.12, 0.14)       # o escuro sai e revela a cena cheia já parada em BASE (antes de as pernas abrirem)
assert REC_PRETO[1] <= REC_SAI[0] and REC_SAI[1] <= REC_CLAREIA[0], "a foto só sai sobre o escuro total"
assert REC_PRETO[1] <= REC_CAM[0] and REC_CAM[0] + REC_CAM[1] <= REC_CLAREIA[0], "a câmera só anda no escuro total"
assert REC_CLAREIA[1] < OPEN0 - R1, "o escuro abre antes de as pernas começarem a abrir no replay"


def recap(cv, t, T, F, passos):
    """Sem texto: a cena escurece, entra a POLAROIDE do congelamento (os dois leques: o que olhar) e o
    estetoscópio acende com o anel dourado no "ortopedista" (consulta, não aprovação).
    v5 (correção de 01/11, 3ª rodada): antes a polaroide saía numa DISSOLUÇÃO cruzada com a cena cheia (a foto
    apagava enquanto o escurecido também apagava e a câmera voltava do recuo): por ~10 quadros as duas figuras
    desalinhadas se somavam (quatro pernas, quatro pés, duas fraldas). Agora a saída passa por FUNDO ESCURO: o
    escurecido fecha até opaco com a foto ainda inteira, a foto some sobre o escuro, a câmera volta para BASE
    dentro do escuro (`cameras`, REC_CAM) e só então o escuro abre sobre a cena cheia. Em nenhum quadro há dois
    bebês sobrepostos."""
    t0 = T["duvida"] - 0.05
    if t < t0:
        return
    tr = F.t_rep
    preto = lerp(0.7, 1.0, prog(t, tr + REC_PRETO[0], tr + REC_PRETO[1]))
    escuro = preto * prog(t, t0, t0 + 0.25) * (1 - prog(t, tr + REC_CLAREIA[0], tr + REC_CLAREIA[1]))
    fim = 1 - prog(t, tr + REC_SAI[0], tr + REC_SAI[1])
    if escuro <= 0 and fim <= 0:
        return
    cv.save(); cv.clipRect(CENA, True)
    img = _img("escurece", CENA.width(), CENA.height(), lambda c: c.clear(_c(BG_OUT, 255)))
    _blit(cv, img, CENA.left(), CENA.top(), escuro)
    if fim <= 0:
        cv.restore()
        return
    k = prog(t, t0, t0 + 0.32)
    esc = max(0.01, e_back(k)); a = prog(t, t0, t0 + 0.06) * fim
    cx, cy = POL_C[0], POL_C[1] + (1 - e_out(k)) * 50
    cv.save(); cv.translate(cx, cy); cv.rotate(-3.0 * e_out(k)); cv.scale(esc, esc)
    borda = skia.RRect.MakeRectXY(skia.Rect(-MW / 2 - 14, -MH / 2 - 14, MW / 2 + 14, MH / 2 + 14), 16, 16)
    sombra = skia.RRect.MakeRectXY(skia.Rect(-MW / 2 - 6, -MH / 2 + 2, MW / 2 + 22, MH / 2 + 26), 16, 16)
    cv.drawRRect(sombra, paint("#000000", int(110 * a), blur=14))
    cv.drawRRect(borda, paint("#F4F7FA", int(255 * a)))
    dentro = skia.RRect.MakeRectXY(skia.Rect(-MW / 2, -MH / 2, MW / 2, MH / 2), 9, 9)
    cv.save(); cv.clipRRect(dentro, True)
    cv.drawImageRect(miniatura(T, F, passos, F.t_fz + 0.6), skia.Rect(-MW / 2, -MH / 2, MW / 2, MH / 2),
                     skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kNone), _alfa(a))
    cv.restore()
    brilho = 1 - prog(t, t0 + 0.1, t0 + 0.6)                       # contorno dourado na entrada
    if brilho > 0:
        cv.drawRRect(borda, paint(OURO, int(255 * a * brilho), "stroke", 7))
    cv.restore()
    a_e = prog(t, T["ortopedista"], T["ortopedista"] + 0.2) * fim
    if a_e > 0:
        ex, ey = POL_C[0] + MW / 2 - 40, POL_C[1] + MH / 2 - 40
        anel_ouro(cv, ex, ey, 112, t, T["ortopedista"] + 0.2, a_e)
        estetoscopio(cv, ex, ey, 1.65 * e_back(prog(t, T["ortopedista"], T["ortopedista"] + 0.3)), a_e)
    cv.restore()


# ------------------------------------------------------------------ CTA: o aviãozinho passa POR CIMA da caixa de crédito
CAIXA_CREDITO = skia.Rect(150, 1060, 930, 1214)                  # a caixa do cartão final de cf_comum.interface (sem nota)


def aviao_na_frente(cv, t, T):
    """v3 (correção de 01/11): no cf_comum.interface o aviãozinho é desenhado ANTES da caixa de crédito, então some
    atrás dela por ~0,2 s ao subir (28,17-28,47 s). cf_comum entra no hash de vídeos já publicados e não pode mudar:
    aqui, depois da interface, o MESMO aviao (mesma função, mesmo instante, mesma trajetória) é redesenhado só DENTRO
    da caixa (recorte com folga de 5 px para cobrir o contorno dourado). Fora da caixa nada muda (o desenho da
    interface fica como está); dentro dela o avião passa na frente, inteiro."""
    t0 = T["manda"] + 0.2                                           # o mesmo t0 que cf_comum.interface usa
    if t < t0:
        return
    cv.save(); cv.clipRect(CAIXA_CREDITO.makeOutset(5, 5), True)
    aviao(cv, t, t0)
    cv.restore()


# ------------------------------------------------------------------ quadro
CARIMBO_XY = (540.0, 455.0)                                      # acima das pernas (sobre a barriga/fralda)


def quadro(cv, t, T, blocos, ep, F, passos):
    fundo_cl(cv, t)
    cam = monitor(cv, t, T, F, passos)
    fim = 1 - prog(t, T["manda"] - 0.4, T["manda"] - 0.1)
    cv.save(); cv.clipRect(CENA, True)
    fecho(cv, t, T, F, cam)
    cv.restore()
    recap(cv, t, T, F, passos)
    cantoneiras(cv, fim)
    painel(cv, t, T, F, fim)
    # o carimbo responde ao gancho: entra no congelamento e se desfaz no borrão do avanço rápido
    carimbo(cv, R_ABRE, CARIMBO_XY[0], CARIMBO_XY[1], -4, F.t_fz + 0.2, t, dur=T["pressa"] + 0.5 - F.t_fz - 0.2,
            tam=60, desfaz=(T["pressa"], T["pressa"] + 0.45))
    capa(cv, t, T["volta"], ep["gancho"][0], ep["gancho"][1])
    selo_lenta(cv, lento_k(t, T) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface(cv, t, T, blocos, DESTAQUE)
    aviao_na_frente(cv, t, T)


# ------------------------------------------------------------------ som (mix próprio: som.py fica intacto; cópias do piloto)
def trilha_partes(dur, bpm=100):
    """A MESMA trilha de som.trilha, separada em (harmonia: pad + baixo, batida: kick + hat). (cópia do piloto)"""
    SR = som.SR
    n = int(dur * SR); t = np.arange(n) / SR
    beat = 60 / bpm; bar = 4 * beat
    harm = np.zeros(n); bat = np.zeros(n)
    acordes = [(220.0, 261.63, 329.63), (174.61, 220.0, 261.63), (130.81, 164.81, 196.0), (196.0, 246.94, 293.66)]
    raizes = [110.0, 87.31, 65.41, 98.0]
    for b in range(int(dur / bar) + 1):
        ini = int(b * bar * SR); fim = min(n, int((b + 1) * bar * SR))
        if ini >= n:
            break
        m = fim - ini; tt = np.arange(m) / SR
        env = np.clip(tt / 0.6, 0, 1) * np.clip((m / SR - tt) / 0.4, 0, 1)
        for f in acordes[b % 4]:
            for det in (-0.6, 0.6):
                harm[ini:fim] += np.sin(2 * np.pi * (f + det) * tt) * env * 0.045
        for k in (0, 2):
            p = ini + int(k * beat * SR)
            if p < fim:
                mm = min(int(beat * 1.6 * SR), n - p); t2 = np.arange(mm) / SR
                harm[p:p + mm] += np.sin(2 * np.pi * raizes[b % 4] * t2) * som._env(mm, 0.01, 0.35) * 0.22
    for k in range(int(dur / beat) + 1):
        p = int(k * beat * SR)
        if p >= n:
            break
        if k % 2 == 0:
            mm = min(int(0.25 * SR), n - p); t2 = np.arange(mm) / SR
            f = 110 * np.exp(-t2 * 22) + 42
            bat[p:p + mm] += np.sin(2 * np.pi * np.cumsum(f) / SR) * som._env(mm, 0.001, 0.11) * 0.38
        ph = p + int(beat / 2 * SR)
        if ph < n:
            mm = min(int(0.05 * SR), n - ph)
            h = som._noise(mm, 100 + k); h = h - np.convolve(h, np.ones(6) / 6, "same")
            bat[ph:ph + mm] += h * som._env(mm, 0.0005, 0.012) * 0.10
    fade = np.clip(t / 0.8, 0, 1) * np.clip((dur - t) / 1.5, 0, 1)
    return harm * fade, bat * fade


def _fita(dur, f0, f1, iv0, fator, semente):
    """Fita correndo: cliques que aceleram + tom que desliza + chiado. (cópia do piloto)"""
    SR = som.SR
    n = int(dur * SR); t = np.arange(n) / SR
    y = np.zeros(n)
    tt, iv = 0.0, iv0
    clk = som.click()
    while tt < dur - 0.04:
        p = int(tt * SR); m = min(len(clk), n - p)
        y[p:p + m] += clk[:m] * 1.6
        tt += iv; iv = max(0.028, iv * fator)
    f = f0 + (f1 - f0) * (1 - np.exp(-1.6 * t / dur)) / (1 - math.exp(-1.6))
    tom = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.55 + 0.45 * np.sin(2 * np.pi * 31 * t))
    env = np.clip(t / 0.04, 0, 1) * np.clip((dur - t) / 0.12, 0, 1)
    rui = som._noise(n, semente); rui = rui - np.convolve(rui, np.ones(12) / 12, "same")
    y += (tom * 0.07 + rui * 0.05) * env
    return y


def rebobinar(dur):
    return _fita(dur, 1960, 260, 0.085, 0.82, 77)


def avancar(dur):
    return _fita(dur, 380, 1500, 0.07, 0.9, 78) * 0.85


def batidinha():
    """Batidinha MACIA de pezinho no trocador (grave, curta, sem ataque metálico): nada de clique nem estalo."""
    SR = som.SR
    n = int(0.16 * SR); t = np.arange(n) / SR
    f = 150 * np.exp(-t * 18) + 95
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.clip(t / 0.006, 0, 1) * np.exp(-t / 0.045)
    rui = som._noise(n, 41); rui = np.convolve(rui, np.ones(40) / 40, "same")
    return (y * 0.55 + rui * np.exp(-t / 0.02) * 0.35)


def bup():
    """A bolinha encosta na borda da conchinha: 'bup' grave e macio (ataque lento). Nunca 'clique'."""
    SR = som.SR
    n = int(0.3 * SR); t = np.arange(n) / SR
    f = 300 * np.exp(-t * 6) + 200
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.clip(t / 0.012, 0, 1) * np.exp(-t / 0.09) * 0.5


def janelas(T, F, dur):
    """Ganho da batida e da harmonia: a batida some na câmera lenta e volta baixa com o bebê tranquilo."""
    xs = np.arange(0, dur + 0.01, 0.01)
    gb = np.ones_like(xs); gh = np.ones_like(xs)
    for i, x in enumerate(xs):
        tp = F.tipo(x)
        gb[i] = {"play": 1.0, "lenta": 0.0, "congela": 0.2, "volta": 0.2, "avanca": 0.85}[tp]
        gh[i] = {"play": 1.0, "lenta": 0.8, "congela": 0.9, "volta": 0.55, "avanca": 0.8}[tp]
        if tp == "play" and F.tf(x) >= CALMA:
            gb[i] = 0.6
    k = np.ones(15) / 15
    gb = np.convolve(np.pad(gb, 7, mode="edge"), k, "valid"); gh = np.convolve(np.pad(gh, 7, mode="edge"), k, "valid")
    return xs, gb, gh


def _media_movel(x, w):
    """(cópia do piloto)"""
    n = len(x); off = (w - 1) // 2
    S = np.concatenate([[0.0], np.cumsum(x, dtype=np.float64)])
    i = np.arange(n)
    return (S[np.clip(i + off + 1, 0, n)] - S[np.clip(i + off - w + 1, 0, n)]) / w


def mixar_cl(voz, dur, eventos, T, F, ganho_trilha=0.40):
    """Mesmo mix e ducking do som.mixar, com a trilha em duas partes e efeitos próprios. (cópia do piloto)"""
    SR = som.SR
    n = int(dur * SR)
    v = np.zeros(n); v[:min(n, len(voz))] = voz[:n]
    harm, bat = trilha_partes(dur)
    xs, gb, gh = janelas(T, F, dur)
    tt = np.arange(n) / SR
    musica = (harm * np.interp(tt, xs, gh) + bat * np.interp(tt, xs, gb)) * ganho_trilha
    win = int(0.06 * SR)
    envv = np.sqrt(np.maximum(_media_movel(v ** 2, win), 0.0))
    alvo = np.where(envv > 0.02, 0.38, 1.0)
    duck = _media_movel(alvo, int(0.25 * SR))
    fx = np.zeros(n)
    for t0, nome, g in eventos:
        s = nome() if callable(nome) else som.SFX[nome]()
        p = int(t0 * SR)
        if 0 <= p < n:
            m = min(len(s), n - p)
            fx[p:p + m] += s[:m] * g
    mix = v * 1.0 + musica * duck + fx * 0.7
    pico = np.max(np.abs(mix)) or 1.0
    return mix / pico * 0.89


def chutes_som(T, F):
    """Uma batidinha a cada chute (perna esticando), só onde o filme anda para a frente em 1× ou avançando; o
    chute calmo do fecho ganha batidinhas bem baixas."""
    out = []
    w0 = (math.pi / 2 - PHI_L) / (2 * math.pi) * P_CHUTE              # fase em que a perna da esquerda estica
    for t0, t1, tipo, a, b, _ in F.segs:
        if tipo not in ("play", "avanca") or b <= a:
            continue
        if a >= CALMA:                                                  # chute calmo: ciclo próprio
            u0, u1 = a - CALMA, b - CALMA
            for off in (0.0, P_CALMA / 2):
                n = math.ceil((u0 - P_CALMA / 4 - off) / P_CALMA)
                while True:
                    f = P_CALMA / 4 + off + n * P_CALMA
                    if f >= u1:
                        break
                    tv = t0 + (f - u0)
                    if t0 + MISTURA < tv < min(t1, T["manda"] - 0.2):
                        out.append((tv, batidinha, 0.12))
                    n += 1
            continue
        g = 0.3 if tipo == "play" else 0.14
        for off in (0.0, P_CHUTE / 2):
            n = math.ceil((a - w0 - off) / P_CHUTE)
            while True:
                f = w0 + off + n * P_CHUTE
                if f >= b:
                    break
                if em_chute(f):
                    tv = t0 + (f - a) / (b - a) * (t1 - t0)
                    if tv < T["manda"] - 0.2:
                        out.append((tv, batidinha, g))
                n += 1
    return out


SECOS = ("tick", "click", "ping", "crackle", "thump")


def sons(T, F):
    ev = chutes_som(T, F)
    ev += [(T["volta"], lambda: rebobinar(T["camera"] - T["volta"]), 0.9),
           (T["camera"], "pop", 0.55), (T["lenta"] + 0.05, "shimmer", 0.35),
           (F.t_para, "shimmer", 0.22),                                      # a da direita para: só um brilho baixo
           (F.t_fz, "tick", 0.9), (F.t_fz + 0.02, lambda: som.whoosh(0.3, seed=7), 0.3),
           (F.t_fz + 0.2, "thump", 0.8),                                     # o carimbo bate
           (T["pressa"], lambda: avancar(F.t_calma - T["pressa"]), 0.7), (T["pressa"], lambda: som.whoosh(0.4, seed=8), 0.35),
           (F.t_calma, "whoosh", 0.4),
           (T["displasia"] - 0.15, lambda: som.whoosh(0.45, seed=12), 0.35),
           (T["encaixa"] + 0.15, bup, 0.6),
           (T["avaliacao"], "ding", 0.45),
           (T["primeiros"], "pop", 0.3), (T["meses"], "pop", 0.3),
           (T["simples"], "shimmer", 0.5),
           (T["duvida"] - 0.05, lambda: som.whoosh(0.4, seed=13), 0.35),
           (T["ortopedista"], "ding", 0.4),
           (T["manda"] + 0.05, "whoosh", 0.5)]
    # nenhum som seco no quadril: nem quando a perna PARA, nem no "displasia ... não encaixa" (o clique no quadril
    # é sinal clínico; a perna parando não pode "bater")
    assert not [e for e in ev if abs(e[0] - F.t_para) < 0.15 and e[1] in SECOS]
    assert not [e for e in ev if T["pode"] - 0.2 <= e[0] < T["avaliacao"] and e[1] in SECOS]
    return ev


def tempos_previa(T, F):
    return (0.0, 0.3, 0.75, 1.1, T["volta"] + 0.3, T["camera"] + 0.15, T["camera"] + 0.6, T["repara"] + 0.2,
            T["perninha"], F.t_para + 0.15, T["caminho"], F.t_fz + 0.15, F.t_fz + 0.5, T["troca"] + 0.3,
            T["pressa"] + 0.15, T["pressa"] + 0.35, T["batido"] + 0.3, F.t_calma + 0.3, F.t_calma + 0.8,
            T["displasia"] + 0.3, T["displasia"] + 0.8, T["quadril2"] + 0.4, T["encaixa"] + 0.3, T["encaixa"] + 0.8,
            T["teste"] + 0.3, T["detecta"] + 0.3, T["avaliacao"] + 0.5, T["ultrassom"] + 0.3, T["identificado"] + 0.4,
            T["meses"] + 0.4, T["simples"] + 0.3, T["duvida"] + 0.1, T["duvida"] + 0.6, T["ortopedista"] + 0.4,
            T["pediatrico"] + 0.3, F.t_rep + 0.3, F.t_rep + 0.7, F.t_rep + 1.1, T["manda"] - 0.3, T["manda"] + 1.0,
            T["total"] - 1 / 30)


# ------------------------------------------------------------------ entrada única (réplica do cf_comum.fazer_render, com mix próprio)
def preparar(ep, tmp):
    roteiro = "\n".join(ep["roteiro"])
    voz_bruta, palavras = _voz.narrar(roteiro, _voz.RITMO_COMO_FUNCIONA, os.path.join(tmp, "voz"))
    voz_c, pal, tirado = comprimir(voz_bruta, palavras, respiro_cta=RESPIRO_CTA)
    pal = alinhar(pal, roteiro)
    T = ancoras(pal, ANCORAS)
    print(f"{ep['id']}: silêncio cortado {tirado:.2f}s | duração final {T['total']:.2f}s")
    return voz_c, pal, T


def render(ep, mp4, tmp, previa=False):
    voz_c, pal, T = preparar(ep, tmp)
    blocos = montar_blocos(pal)
    F = Filme(T)
    passos = cameras(T, F)

    def quadro_t(cv, t):
        quadro(cv, t, T, blocos, ep, F, passos)

    if previa:
        return _previas(quadro_t, tempos_previa(T, F), tmp, ep["id"]), T["total"]
    wav = os.path.join(tmp, f"{ep['id']}_mix.wav")
    som.gravar_wav(wav, mixar_cl(voz_c, T["total"], sons(T, F), T, F, ganho_trilha=0.40))
    codificar(quadro_t, T["total"], wav, mp4)
    return mp4, T["total"]
