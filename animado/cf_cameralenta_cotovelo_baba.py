# -*- coding: utf-8 -*-
"""CÂMERA LENTA (série) — episódio "UPA PELA MÃO / E O BRAÇO PAROU?" (pronação dolorosa, o "cotovelo de
babá"; o apelido fica SÓ na legenda: a voz e a tela dizem "pronação dolorosa").

Mesma mecânica do piloto cf_cameralenta_ponta_pes: um REPLAY de TV. O "upa!" pela mão para vencer uma poça
passa em 1× (rápido e borrado: a criança sobe, pousa e o braço para, tudo DENTRO do borrão), a fita VOLTA
(rápida, embaçada e com faixas de tracking, e acaba ANTES da subida), o lance é revisto em CÂMERA LENTA e
CONGELA no detalhe. O tempo do filme (`Filme.tf`) é separado do tempo do vídeo: o mundo é desenhado em função
do tempo do filme; a narração nunca para nem desacelera.

Cada câmera lenta REVELA o que o 1× escondeu:
  1. congela no alto do arco, sobre a poça: o puxão é lá em cima, NA MÃO (círculo nas mãos dadas), mas o que
     acontece é no meio do braço, NO COTOVELO (anel por fora da pele; 2º passo de câmera a ~1,45× no cotovelo).
     Uma LUPA esquemática OPACA (fundo no tom da pele, uma CINTA marfim longa e fibrosa atravessando o braço,
     sobre o "lugar" dela em tracejado BRANCO) mostra a cinta ESCORREGANDO para o lado do ombro, com um ECO de 2
     fantasmas que fica no quadro parado — e ela FICA ali (nunca volta: nenhuma manobra de redução, nem insinuada);
  2. descongela a 0,25× (0,2 s antes do "Pousou": o pé toca no "Pou-"): a mão adulta solta no toque e sai pelo
     alto, o braço cai ESTICADO num arco até o lado do corpo durante o "Pousou"; congela e uma seta tracejada
     tenta sair da mãozinha e volta (não quer mexer);
  3. no 2º lance (CORTE de fita no "Pra ajudar a prevenir": OUTRA criança, outra poça) o upa é pelas AXILAS, em
     câmera lenta: as mãos adultas chegam POR TRÁS, na altura do peito (antebraço quase horizontal, cotovelo em
     curva; v5: o MESMO braço do 1º lance — manga azul, punho claro, antebraço e mão de pele — e a mão de lá só
     aparece atrás do tronco, com as pontas dos dedos à frente do peito), os braços da criança ficam soltos para
     baixo; círculo na axila,
     e o ícone (criança genérica cinza pendurada pela mão de uma mão adulta com manga azul) leva um X BRANCO.
Depois da câmera lenta: nome e frequência em 1×, com push-in lento no braço parado e micromovimento (cabeça baixa,
ombro encolhido); "não puxe nem force" = a mão adulta vem, PARA a ~200 px do braço, abre a palma (polegar junto)
e recua já no "force" (ninguém toca, gira, dobra, puxa ou estica o braço parado); "leve pra avaliar" = ela sai
andando devagar, de cabeça baixa, com o braço do puxão parado (não balança), o estetoscópio pulsa em "avaliar",
"ortopedista" e "rápida" (sem check, sem selo de resolvido). A criança do braço parado NÃO reaparece.
v2 (31/10, revisor + leitor às cegas): roteiro com sujeito explícito ("a criança deixa o braço"), a frase calma
literal do post31 ("a correção pelo ortopedista costuma ser rápida") e a prevenção anunciada no corte ("Pra ajudar
a prevenir, upa pelas axilas"); no congelamento a câmera DERIVA devagar (nenhum trecho > 1,2 s parado).

Regras da série e do verificador (storyboard.json), todas aqui:
  * O selo CÂMERA LENTA só EXISTE com a lentidão ligada (0,25× e os congelamentos dentro dela): do "câmera" ao
    "É" e do 2º "upa" ao fim do "pulsos"; nunca no 1×, no ◀◀, no corte de fita ou na CTA. A moldura âmbar segue
    a mesma janela.
  * VERMELHO PROIBIDO no vídeo inteiro (a faixa da lupa é marfim; o X do ícone é BRANCO); sem sangue, sem pele
    rompida; nada desenhado sobre o cotovelo por fora no 1× e depois do pouso (seria lido como inchaço).
  * Lupa = ilustração esquemática opaca: fundo no tom da pele, faixa marfim, SEM osso, anel, nome, fundo escuro
    ou brilho de raio-X.
  * Sem culpado: do adulto só manga e mão (sem rosto, sem uniforme); criança sem traços de rosto, sem lágrima,
    sem som de choro (a dor é postura: cabeça inclinada, ombro encolhido).
  * Som: NUNCA estalo, clique ou "pop" no braço; ligamento = deslize suave; pousos = thump macio.
  * Nada de ❚❚, barra de progresso, "PAUSA", timecode ou dígitos: congelar = flash + tique + chip apagado.
  * Nenhum texto além do `tela` (CÂMERA LENTA, 1×, 0,25×, NA MÃO, NO COTOVELO, NÃO PUXE NEM FORCE, PELAS
    AXILAS), do gancho e da interface; ◀◀ desenhado como forma.
Assinatura sonora do piloto (batida some na câmera lenta, rebobinar com cliques, tique seco no congelamento,
chiado no corte de fita), com mix próprio (`mixar_cl`, cópia do piloto), sem mexer em som.py.

Helpers COPIADOS (não importados), como manda o contrato:
  * do piloto cf_cameralenta_ponta_pes / cf_cameralenta_osso_crianca: Filme (adaptado), tubo, ik, _trim, sstep,
    _img/_blit/fundo_cl/monitor_fundo/varredura/faixas_tracking/corte_fita/cantoneiras/flash, relogio, chip_c,
    _setas, painel, circulo_mao, anel, estetoscopio, selo_lenta, trilha_partes, _fita, rebobinar, chiado,
    congelar, janelas, _media_movel, mixar_cl; a criança de perfil montada em esqueleto (_joints, braco, mao,
    perna, tenis, tronco), com cabelo no lugar do capacete;
  * do cf_cotovelo_baba: _pele, camada, rr_path, oval_path, uniao, desvanecer, ponta, seta, mao_adulta_tras/
    frente (com manga longa), chip, etiqueta_fio e a ideia da faixa esquemática na lupa (RECOLORIDA: marfim, sem
    contorno vermelho). O ícone cinza do "não pelas mãos" segue a ideia do icone_puxar (mão adulta segurando a
    mãozinha pelo alto), mas como PICTOGRAMA de uma criança genérica pendurada pela mão (o icone_puxar, pequeno,
    era lido como "mão segurando um bastão"); o X é BRANCO e nunca fica sobre a criança da cena.
Importados sem cópia: capa/interface/ancoras (cf_comum), comprimir, alinhar, montar_blocos (cf_fratura_cola),
paleta e texto (cf_alongamento). A cena é PRESA ao roteiro pelas palavras-âncora (ANCORAS): roteiro sem elas =
KeyError no render.
"""
import math
import os

import numpy as np
import skia

from . import som, voz as _voz
from .base import FPS, codificar, previas as _previas
from .cf_alongamento import (BG_OUT, CX, F_BLACK, H, OURO, PART, W, clamp, e_back, e_inout, e_out, lerp,
                             lerpc, paint, prog, texto)
from .cf_comum import ancoras, capa, interface
from .cf_fratura_cola import alinhar, comprimir, montar_blocos

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "upa": ("upa", 1, False), "mao1": ("mão", 1, False), "volta": ("volta", 1, False),
    "camera": ("câmera", 1, False), "lenta": ("lenta", 1, False), "braco1": ("braço", 1, False),
    "parou": ("parou", 1, False), "repara": ("repara", 1, False), "puxao": ("puxão", 1, False),
    "mao2": ("mão", 2, False), "cotovelo": ("cotovelo", 1, False), "ligamento": ("ligamento", 1, False),
    "escorrega": ("escorrega", 1, False), "pousou": ("pousou", 1, False), "crianca": ("criança", 1, False),
    "deixa": ("deixa", 1, False), "esticado": ("esticado", 1, False), "corpo": ("corpo", 1, False),
    "nao1": ("não", 1, False), "mexer": ("mexer", 1, False), "e3": ("é", 3, False),
    "pronacao": ("pronação", 1, False), "comum": ("comum", 1, False), "pequenas": ("pequenas", 1, False),
    "nao2": ("não", 2, False), "puxe": ("puxe", 1, False), "force": ("force", 1, False),
    "leve": ("leve", 1, False), "avaliar": ("avaliar", 1, False), "correcao": ("correção", 1, False),
    "ortopedista": ("ortopedista", 1, False), "costuma": ("costuma", 1, False), "rapida": ("rápida", 1, False),
    "corte": ("pra", 2, False), "prevenir": ("prevenir", 1, False), "upa2": ("upa", 2, False),
    "pelas1": ("pelas", 1, False), "axilas": ("axilas", 1, False), "nao3": ("não", 3, False),
    "pulsos": ("pulsos", 1, False), "manda": ("manda", 1, False),
}
DESTAQUE = {"mão", "parou", "puxão", "cotovelo", "ligamento", "escorrega", "esticado", "corpo", "mexer",
            "pronação", "dolorosa", "comum", "puxe", "force", "avaliar", "ortopedista", "rápida", "prevenir",
            "axilas", "mãos", "pulsos"}
RESPIRO_CTA = 1.6
# rótulos (todos em ep["tela"])
R_SELO, R_1X, R_LENTA = "CÂMERA LENTA", "1×", "0,25×"
R_NAMAO, R_NOCOT, R_PUXE, R_AXI = "NA MÃO", "NO COTOVELO", "NÃO PUXE NEM FORCE", "PELAS AXILAS"

# ------------------------------------------------------------------ paleta (SEM vermelho e sem rosado-avermelhado nas marcações)
PELE, PELE_CL, PELE_ESC, PELE_LINHA = "#F0B49A", "#F7CDB8", "#DA987E", "#B9765E"
AD, AD_CL, AD_ESC, AD_LINHA = "#C98D6E", "#DDA98C", "#A56C50", "#7C4C37"        # mão adulta: outro tom
TONS_PELE = (PELE_ESC, PELE, PELE_CL, PELE, PELE_ESC)
TONS_AD = (AD_ESC, AD, AD_CL, AD, AD_ESC)
MANGA1 = dict(tons=("#435C76", "#5C7A99", "#7F9BB8", "#5C7A99", "#435C76"), linha="#2F445A", punho="#A7BED4")
TONS_PUNHO_ICONE = ("#27415F", "#3B5C84", "#5479A6", "#3B5C84", "#27415F")
ROUPA1 = dict(camisa="#6FD3B5", camisa_cl="#A3E6D2", camisa_esc="#3A9C80", camisa_linha="#23705C",
              bermuda="#C9CED6", bermuda_linha="#7E8794", cabelo="#5A3A26", estilo="puxinhos")
ROUPA2 = dict(camisa="#7EC8E3", camisa_cl="#A9DDEF", camisa_esc="#4FA3C4", camisa_linha="#2F7FA0",
              bermuda="#D8C6A0", bermuda_linha="#9A8564", cabelo="#1E1A1A", estilo="cachos")
TENIS, TENIS_SOLA, TENIS_LINHA = "#F4F7FA", "#B8C2CC", "#7D8896"
POCA, POCA_ESC, POCA_CL = "#86A9C8", "#3E5A76", "#E2EEF8"
CALCADA, CALCADA_CL, CALCADA_JUNTA, MEIO_FIO = "#55677B", "#61758A", "#8296AA", "#B6C4D2"
MARFIM, MARFIM_CL, MARFIM_LINHA = "#F3E6CF", "#FBF5EA", "#B49673"                # a faixa (esquema)
FUNDO_CARTAO = "#0B1824"
AMBAR = "#FFB547"
AZUL_CL = "#9CC9FF"
CINZA = "#9AAABB"
ESCURO = "#1C2A38"                                               # tom para perna/braço de trás (opaco)

# ------------------------------------------------------------------ o "monitor" de replay (tela)
CENA = skia.Rect(40, 330, 1040, 1230)                            # o mundo é recortado aqui (selo e karaokê livres)
GY = 1100.0                                                      # linha do chão no mundo (= tela na câmera base)


def _c(h, a=255):
    h = h.lstrip("#")
    return skia.ColorSetARGB(int(a), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _alfa(a):
    p = skia.Paint()
    p.setAlphaf(clamp(a))
    return p


def _uniao(a, b):
    return skia.Op(a, b, skia.PathOp.kUnion_PathOp) or a


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


def _lp(a, b, k):
    return (lerp(a[0], b[0], k), lerp(a[1], b[1], k))


def tubo(x0, y0, r0, x1, y1, r1):
    """(cópia do piloto / cf_crianca_mancando)"""
    L = math.hypot(x1 - x0, y1 - y0) or 1.0
    nx, ny = -(y1 - y0) / L, (x1 - x0) / L
    p = skia.Path()
    p.moveTo(x0 + nx * r0, y0 + ny * r0); p.lineTo(x1 + nx * r1, y1 + ny * r1)
    p.lineTo(x1 - nx * r1, y1 - ny * r1); p.lineTo(x0 - nx * r0, y0 - ny * r0); p.close()
    c0 = skia.Path(); c0.addCircle(x0, y0, r0)
    c1 = skia.Path(); c1.addCircle(x1, y1, r1)
    return _uniao(_uniao(p, c0), c1)


def ik(ax, ay, bx, by, l1, l2, dobra):
    """(cópia do cf_cameralenta_osso_crianca) Cinemática inversa de dois segmentos. dobra = +1: a junta vai
    para +x quando o membro desce (joelho); -1: para trás (cotovelo). Fora do alcance: membro esticado."""
    dx, dy = bx - ax, by - ay
    d0 = math.hypot(dx, dy) or 1.0
    d = max(abs(l1 - l2) + 1.0, min(d0, l1 + l2 - 0.5))
    a = math.atan2(dy, dx)
    A = math.acos(clamp((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d), -1.0, 1.0))
    g = a - dobra * A
    jx, jy = ax + l1 * math.cos(g), ay + l1 * math.sin(g)
    ux, uy = dx / d0, dy / d0
    return (jx, jy), (ax + ux * d, ay + uy * d)


# ------------------------------------------------------------------ utilidades do cf_cotovelo_baba (cópias)
def rr_path(x0, y0, x1, y1, r):
    p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), r, r)); return p


def oval_path(x0, y0, x1, y1):
    p = skia.Path(); p.addOval(skia.Rect(x0, y0, x1, y1)); return p


def uniao(*ps):
    out = ps[0]
    for q in ps[1:]:
        out = skia.Op(out, q, skia.PathOp.kUnion_PathOp) or out
    return out


def camada(cv, a, cinza=0.0, escuro=0.0):
    """saveLayer com transparência (e, se pedido, tons de cinza e escurecimento). (cópia)"""
    if a >= 0.999 and cinza <= 0 and escuro <= 0:
        cv.save(); return
    p = skia.Paint()
    p.setAlphaf(clamp(a))
    if cinza > 0 or escuro > 0:
        k = clamp(cinza); s = 1 - k; m = 1 - clamp(escuro)
        r, g, b = 0.2126 * k, 0.7152 * k, 0.0722 * k
        p.setColorFilter(skia.ColorFilters.Matrix([(r + s) * m, g * m, b * m, 0, 0,
                                                   r * m, (g + s) * m, b * m, 0, 0,
                                                   r * m, g * m, (b + s) * m, 0, 0,
                                                   0, 0, 0, 1, 0]))
    cv.saveLayer(None, p)


def camada_escura(cv, a, escuro):
    """v4: o mesmo que camada(cv, a, escuro=escuro), mas SEM filtro de cor na camada: nesta build do skia o
    ColorFilters.Matrix custa ~170 ns por pixel da camada inteira (~160 ms por camada, duas por amostra no 2º lance),
    o que torna inviável o rastro contínuo (dezenas de amostras por quadro). Abre uma camada só de alfa; quem desenha
    chama `escurecer` com uma silhueta que cubra tudo o que desenhou, ANTES do restore. Devolve True se escurece."""
    if escuro <= 0:
        camada(cv, a)
        return False
    cv.saveLayer(None, _alfa(a))
    return True


def escurecer(cv, silhueta, escuro, folga=10.0):
    """Multiplica o RGB do que JÁ está na camada (dentro da silhueta + folga) por 1 - escuro, alfa intacto: preto
    com alfa `escuro` em kSrcATop (cor = cor·(1 - escuro); alfa = alfa) — a mesma conta do filtro de matriz que
    camada(escuro=...) usa. A camada só tem o desenho a escurecer, então a folga não toca em mais nada."""
    q = skia.Paint(AntiAlias=True)
    q.setColor(skia.ColorSetARGB(int(round(255 * clamp(escuro))), 0, 0, 0))
    q.setBlendMode(skia.BlendMode.kSrcATop)
    q.setStyle(skia.Paint.kStrokeAndFill_Style)
    q.setStrokeWidth(folga)
    cv.drawPath(silhueta, q)


def _pele(cv, pth, p0, p1, a, tons=TONS_PELE, linha=3.0, cor_linha=PELE_LINHA):
    sh = skia.GradientShader.MakeLinear([skia.Point(*p0), skia.Point(*p1)], [_c(c) for c in tons],
                                        [0.0, 0.22, 0.5, 0.78, 1.0])
    cv.drawPath(pth, paint(tons[1], int(255 * a), shader=sh))
    if linha:
        cv.drawPath(pth, paint(cor_linha, int(230 * a), "stroke", linha))


def desvanecer(cv, x0, y0, x1, y1):
    """Dentro de um saveLayer: apaga em degradê de (x0, y0) [opaco] a (x1, y1) [some] (DstIn). (cópia)"""
    m = skia.Paint(AntiAlias=True)
    m.setShader(skia.GradientShader.MakeLinear([skia.Point(x0, y0), skia.Point(x1, y1)],
                                               [skia.ColorSetARGB(255, 0, 0, 0), skia.ColorSetARGB(0, 0, 0, 0)]))
    m.setBlendMode(skia.BlendMode.kDstIn)
    cv.drawRect(skia.Rect(-4000, -4000, 4000, 4000), m)


def ponta(cv, x, y, ang, tam, cor, a):
    p = skia.Path()
    p.moveTo(x + tam * math.cos(ang), y + tam * math.sin(ang))
    p.lineTo(x + tam * 0.75 * math.cos(ang + 2.45), y + tam * 0.75 * math.sin(ang + 2.45))
    p.lineTo(x + tam * 0.75 * math.cos(ang - 2.45), y + tam * 0.75 * math.sin(ang - 2.45))
    p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))


def seta(cv, x0, y0, x1, y1, cor, a, larg=9, tam=30):
    if a <= 0 or math.hypot(x1 - x0, y1 - y0) < 2:
        return
    ang = math.atan2(y1 - y0, x1 - x0)
    xb, yb = x1 - tam * 0.55 * math.cos(ang), y1 - tam * 0.55 * math.sin(ang)
    cv.drawLine(x0, y0, xb, yb, paint(cor, int(90 * a), "stroke", larg + 10, blur=7))
    cv.drawLine(x0, y0, xb, yb, paint(cor, int(255 * a), "stroke", larg))
    ponta(cv, x1, y1, ang, tam, cor, a)


def mao_adulta_tras(cv, a, manga=None, some=(330, 540), comp=560):
    """Antebraço com manga e palma: fica ATRÁS da mãozinha. (cópia do cf_cotovelo_baba; `manga` = cores da
    manga, `some` = None deixa a manga longa, sem desvanecer, para sair pela borda do recorte da cena)"""
    tons_m = (manga or {}).get("tons", TONS_PUNHO_ICONE)
    cor_l = (manga or {}).get("linha", "#27415F")
    punho = (manga or {}).get("punho", "#5479A6")
    cv.saveLayer(None, None)
    ante = rr_path(30, -46, min(360, comp), 46, 44)
    _pele(cv, ante, (0, -46), (0, 46), a, tons=TONS_AD, cor_linha=AD_LINHA)
    mg = rr_path(190, -60, comp, 60, 20)
    _pele(cv, mg, (0, -60), (0, 60), a, tons=tons_m, cor_linha=cor_l)
    cv.drawRect(skia.Rect(190, -58, 222, 58), paint(punho, int(235 * a)))
    cv.drawLine(222, -58, 222, 58, paint(cor_l, int(200 * a), "stroke", 3))
    if some:
        desvanecer(cv, some[0], 0, some[1], 0)
    cv.restore()
    palma = rr_path(-36, -62, 100, 60, 46)
    _pele(cv, palma, (0, -62), (0, 60), a, tons=TONS_AD, cor_linha=AD_LINHA)


def mao_adulta_frente(cv, a):
    """Quatro dedos dobrados por cima da mãozinha + polegar. (cópia)"""
    for i in range(4):
        x0 = -42 + i * 30
        d = rr_path(x0, -16, x0 + 32, 64, 16)
        _pele(cv, d, (x0, 0), (x0 + 32, 0), a, tons=TONS_AD, cor_linha=AD_LINHA, linha=2.5)
    pol = rr_path(-54, -76, 52, -40, 18)
    _pele(cv, pol, (0, -76), (0, -40), a, tons=TONS_AD, cor_linha=AD_LINHA, linha=2.5)


ROUPA_ICONE = dict(camisa="#9FB2C4", camisa_cl="#C3D0DC", camisa_esc="#7A8EA2", camisa_linha="#4D6074",
                   bermuda="#8496A8", bermuda_linha="#56687A", cabelo="#46525E", estilo="simples")


def icone_desenho(cv, x, y, ang, esc, a, cinza=1.0):
    """Ícone CINZA de "erguer pela mão": uma criança GENÉRICA (outra roupa, sem rosto) pendurada pela mãozinha,
    a mão adulta segurando pelo alto, e uma seta para cima. (A mão adulta e a mãozinha seguem o desenho do
    icone_puxar do cf_cotovelo_baba; o pictograma inteiro sai em tons de cinza.)"""
    if a <= 0:
        return
    cv.save()
    cv.translate(x, y); cv.scale(esc, esc)
    A = (0.0, 0.0)
    tor, ab = 4.0, 6.0
    hip = quadril_pendurado(A, tor, ab)
    om = _ombro_mundo(hip, tor, 0.0)
    ux, uy = A[0] - om[0], A[1] - om[1]; d = math.hypot(ux, uy) or 1.0
    mp = (A[0] - ux / d * PALMA_D - hip[0], A[1] - uy / d * PALMA_D - hip[1])
    p = _base_pose(hx=hip[0], hy=hip[1], tor=tor, cab=-8.0, mp=mp, ml=(8.0, 30.0), mp_abre=0.1,
                   pp=(10.0, 182.0), pl=(-8.0, 180.0), ppa=26.0, pla=28.0)
    # v2 (revisor): a criança genérica em CINZA; a manga AZUL e a mão adulta EM COR, inteiras dentro da caixa,
    # segurando a mãozinha pelo alto (contraste: "levantar pela mão")
    camada(cv, a, cinza)
    crianca(cv, p, ROUPA_ICONE)
    cv.restore()
    camada(cv, a)
    cv.scale(1.5, 1.5)
    adulto_tras(cv, A, -90.0, MANGA1, 1.0)
    adulto_frente(cv, A, -90.0, 1.0)
    cv.restore()
    camada(cv, a)
    seta(cv, 175, 300, 175, 40, "#FFFFFF", 1.0, larg=16, tam=48)
    cv.restore()
    cv.restore()


def xis_branco(cv, x, y, L, pr, a):
    """X BRANCO com contorno escuro (nada de vermelho); pr 0..1 = os dois traços."""
    if pr <= 0 or a <= 0:
        return
    for k, sx in enumerate((-1, 1)):
        q = clamp(pr * 2 - k)
        if q <= 0:
            continue
        x0, y0 = x - L, y - sx * L
        x1, y1 = lerp(x0, x + L, e_out(q)), lerp(y0, y + sx * L, e_out(q))
        cv.drawLine(x0, y0, x1, y1, paint(FUNDO_CARTAO, int(220 * a), "stroke", 19))
        cv.drawLine(x0, y0, x1, y1, paint("#FFFFFF", int(255 * a), "stroke", 9))


def etiqueta_fio(cv, s, x, y, xa, ya, cor, a, tam=40, borda=None):
    """Caixa alinhada pela esquerda em x (linha de base y) com fio até (xa, ya). (cópia do cf_cotovelo_baba,
    recolorida: fundo #0B1824, borda e texto na cor dada)"""
    if a <= 0:
        return
    borda = borda or cor
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    x1 = x + lw + 30; ym = y - tam * 0.35
    xb = x1 if xa > x1 else x
    cv.drawLine(xb, ym, xa, ya, paint(FUNDO_CARTAO, int(150 * a), "stroke", 7))
    cv.drawLine(xb, ym, xa, ya, paint(borda, int(235 * a), "stroke", 3))
    cv.drawCircle(xa, ya, 8, paint(FUNDO_CARTAO, int(200 * a)))
    cv.drawCircle(xa, ya, 6, paint(borda, int(255 * a)))
    rr = skia.RRect.MakeRectXY(skia.Rect(x, y - tam * 1.05, x1, y + tam * 0.34), 14, 14)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(225 * a)))
    cv.drawRRect(rr, paint(borda, int(255 * a), "stroke", 3))
    cv.drawString(s, x + 15, y, f, paint(cor, int(255 * a)))


def chip_txt(cv, s, x, y, cor, a, tam=40, borda=None, esc=1.0):
    """Rótulo solto centrado em x; y = linha de base do texto. (cópia do chip do cf_cotovelo_baba)"""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    cv.save(); cv.translate(x, y - tam * 0.35); cv.scale(esc, esc); cv.translate(-x, -(y - tam * 0.35))
    rr = skia.RRect.MakeRectXY(skia.Rect(x - lw / 2 - 24, y - tam * 1.05, x + lw / 2 + 24, y + tam * 0.34), 16, 16)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(230 * a)))
    cv.drawRRect(rr, paint(borda or cor, int(255 * a), "stroke", 3))
    cv.drawString(s, x - lw / 2, y, f, paint(cor, int(255 * a)))
    cv.restore()


# ------------------------------------------------------------------ a criança de perfil (esqueleto; cópia adaptada do cf_cameralenta_osso_crianca)
L_TOR, L_OMBRO, L_PESC, R_CAB = 130.0, 118.0, 56.0, 58.0          # criança pequena: cabeça grande, tronco curto
L_BR, L_AB = 78.0, 74.0                                          # braço, antebraço
L_CX, L_CN = 96.0, 92.0                                          # coxa, perna
MAO_K = 1.2
ANK = GY - 24.0                                                  # tornozelo do pé apoiado no chão
PALMA_D = 18.0 * MAO_K                                           # do punho ao centro da palma
ALCANCE = L_BR + L_AB - 1.5                                      # ombro -> punho com o braço esticado


def _joints(p):
    """Juntas no referencial LOCAL (quadril na origem, +x = para onde ela olha). Alvos das mãos e dos pés no
    referencial do quadril, SEM girar com o tronco."""
    tor = p["tor"]
    J = {}
    J["pesc"] = rot((0.0, -L_TOR), tor)
    J["omb_p"] = rot((2.0, -L_OMBRO - 9.0 * p["enc"]), tor)        # ombro encolhido (dor = postura)
    J["omb_l"] = rot((-5.0, -L_OMBRO + 3), tor)
    c = rot((0.0, -L_PESC), tor + p["cab"])
    J["cab"] = (J["pesc"][0] + c[0], J["pesc"][1] + c[1])
    for lado in ("p", "l"):
        om = J["omb_" + lado]
        alvo = p["m" + lado]
        cot, pun = ik(om[0], om[1], alvo[0], alvo[1], L_BR, L_AB, -1)
        J["cot_" + lado], J["pun_" + lado] = cot, pun
        ang_ab = math.degrees(math.atan2(pun[1] - cot[1], pun[0] - cot[0]))
        J["mao_ang_" + lado] = ang_ab + p["m" + lado + "_rel"]
        q = (0.0, 0.0) if lado == "p" else (-4.0, 2.0)
        jo, to = ik(q[0], q[1], p["p" + lado][0], p["p" + lado][1], L_CX, L_CN, 1)
        J["joe_" + lado], J["tor_" + lado], J["quad_" + lado] = jo, to, q
    return J


def _sombrear(cv, path, cor, escuro, aro=((16, -0.10), (8, -0.20))):
    """Preenche e dá volume com um aro mais escuro por dentro do contorno (opaco, sem desfoque). (cópia)"""
    cv.drawPath(path, paint(lerpc(cor, ESCURO, escuro)))
    cv.save(); cv.clipPath(path, skia.ClipOp.kIntersect, True)
    for larg, f in aro:
        c = lerpc(cor, "#000000", -f) if f < 0 else lerpc(cor, "#FFFFFF", f)
        cv.drawPath(path, paint(lerpc(c, ESCURO, escuro), 255, "stroke", larg))
    cv.restore()


def _mao_path(abre):
    """Mão de desenho no referencial do punho (+x = para fora da mão; -y = lado do polegar). (cópia)"""
    p = skia.Path(); p.addOval(skia.Rect(2, -13, 34, 13))
    for i, yy in enumerate((-9.0, -3.0, 3.0, 9.0)):
        comp = lerp(7.0, 22.0 - 2.0 * abs(i - 1.5), abre)
        r = 4.6
        abertura = (i - 1.5) * 9.0 * abre
        d = skia.Path(); d.addRRect(skia.RRect.MakeRectXY(skia.Rect(0, -r, comp, r), r, r))
        m = skia.Matrix(); m.setRotate(abertura); m.postTranslate(28, yy * lerp(1.0, 1.25, abre))
        d.transform(m)
        p = _uniao(p, d)
    pol = skia.Path(); pol.addRRect(skia.RRect.MakeRectXY(skia.Rect(0, -4.8, lerp(12.0, 20.0, abre), 4.8), 4.8, 4.8))
    m = skia.Matrix(); m.setRotate(lerp(-30.0, -62.0, abre)); m.postTranslate(10, -10)
    pol.transform(m)
    return _uniao(p, pol)


def mao(cv, pun, ang, abre, escuro):
    cv.save(); cv.translate(*pun); cv.rotate(ang); cv.scale(MAO_K, MAO_K)
    pth = _mao_path(abre)
    _sombrear(cv, pth, PELE, escuro, aro=((9, -0.08),))
    cv.drawPath(pth, paint(PELE_LINHA, 230, "stroke", 2.6))
    cv.restore()


def braco(cv, J, lado, p, roupa, escuro):
    om, cot, pun = J["omb_" + lado], J["cot_" + lado], J["pun_" + lado]
    ab = _uniao(tubo(om[0], om[1], 17.0, cot[0], cot[1], 14.5), tubo(cot[0], cot[1], 14.5, pun[0], pun[1], 11.5))
    _sombrear(cv, ab, PELE, escuro)
    cv.drawPath(ab, paint(PELE_LINHA, 230, "stroke", 2.8))
    mao(cv, pun, J["mao_ang_" + lado], p["m" + lado + "_abre"], escuro)
    L = math.hypot(cot[0] - om[0], cot[1] - om[1]) or 1.0           # manga curta da camiseta
    ux, uy = (cot[0] - om[0]) / L, (cot[1] - om[1]) / L
    fim = (om[0] + ux * 38, om[1] + uy * 38)
    mg = tubo(om[0] - ux * 6, om[1] - uy * 6, 23.0, fim[0], fim[1], 21.0)
    _sombrear(cv, mg, roupa["camisa"], escuro)
    cv.drawPath(mg, paint(roupa["camisa_linha"], 230, "stroke", 2.6))


def tenis(cv, to, ang, escuro):
    s = skia.Path()
    s.moveTo(-18, 6); s.quadTo(-18, -8, -6, -10); s.lineTo(14, -12); s.quadTo(30, -6, 44, 2)
    s.quadTo(58, 6, 58, 16); s.quadTo(58, 25, 46, 25); s.lineTo(-12, 25); s.quadTo(-19, 25, -19, 16); s.close()
    cv.save(); cv.translate(*to); cv.rotate(ang)
    cv.drawPath(s, paint(lerpc(TENIS, ESCURO, escuro)))
    cv.save(); cv.clipPath(s, skia.ClipOp.kIntersect, True)
    cv.drawRect(skia.Rect(-30, 17, 70, 30), paint(lerpc(TENIS_SOLA, ESCURO, escuro)))
    cv.drawLine(4, -8, 22, -3, paint(lerpc(AZUL_CL, ESCURO, escuro), 255, "stroke", 4))
    cv.restore()
    cv.drawPath(s, paint(TENIS_LINHA, 230, "stroke", 2.6))
    cv.restore()


def perna(cv, J, lado, p, roupa, escuro):
    q, jo, to = J["quad_" + lado], J["joe_" + lado], J["tor_" + lado]
    pth = _uniao(tubo(q[0], q[1], 24.0, jo[0], jo[1], 19.0), tubo(jo[0], jo[1], 19.0, to[0], to[1], 13.0))
    _sombrear(cv, pth, PELE, escuro)
    cv.drawPath(pth, paint(PELE_LINHA, 230, "stroke", 2.8))
    tenis(cv, to, p["ppa"] if lado == "p" else p["pla"], escuro)
    L = math.hypot(jo[0] - q[0], jo[1] - q[1]) or 1.0                  # perna da bermuda
    ux, uy = (jo[0] - q[0]) / L, (jo[1] - q[1]) / L
    bm = tubo(q[0], q[1], 31.0, q[0] + ux * 60, q[1] + uy * 60, 27.0)
    _sombrear(cv, bm, roupa["bermuda"], escuro, aro=((12, -0.08),))
    cv.drawPath(bm, paint(roupa["bermuda_linha"], 230, "stroke", 2.6))


def _tronco_path():
    """Tronco de criança de perfil (camiseta), no referencial do tronco (+x = frente, para cima = -y). (cópia)"""
    p = skia.Path()
    m = skia.Matrix(); m.setScale(1.08, L_TOR / 150.0)
    p.moveTo(-36, 14)
    p.cubicTo(-42, -30, -40, -100, -34, -128)
    p.cubicTo(-30, -150, -14, -160, 4, -158)
    p.cubicTo(20, -156, 30, -146, 32, -124)
    p.cubicTo(36, -90, 44, -50, 40, -10)
    p.cubicTo(38, 6, 34, 16, 26, 20)
    p.close()
    p.transform(m)
    return p


TRONCO_P = _tronco_path()


def tronco(cv, p, roupa):
    hip = skia.Path(); hip.addOval(skia.Rect(-40, -26, 38, 34))
    _sombrear(cv, hip, roupa["bermuda"], 0.0, aro=((12, -0.08),))
    cv.drawPath(hip, paint(roupa["bermuda_linha"], 230, "stroke", 2.6))
    cv.save(); cv.rotate(p["tor"])
    _sombrear(cv, TRONCO_P, roupa["camisa"], 0.0, aro=((18, -0.10), (8, -0.18)))
    cv.drawLine(-22, -110, -18, -36, paint(roupa["camisa_cl"], 170, "stroke", 9))
    cv.drawPath(TRONCO_P, paint(roupa["camisa_linha"], 230, "stroke", 2.8))
    cv.drawLine(-34, 6, 30, 12, paint(roupa["camisa_esc"], 200, "stroke", 3))
    cv.restore()


def cabeca(cv, J, p, roupa):
    """Cabeça de perfil SEM rosto (sem olhos, sem boca, sem lágrima): cabelo e orelha. Criança 1: castanho
    com dois puxinhos; criança 2: cabelo preto cacheado."""
    cx, cy = J["cab"]
    ang = p["tor"] + p["cab"]
    pe = J["pesc"]
    cv.drawPath(tubo(pe[0], pe[1], 13.0, cx, cy, 13.0), paint(PELE))
    cv.save(); cv.translate(cx, cy); cv.rotate(ang)
    cor = roupa["cabelo"]
    if roupa["estilo"] == "puxinhos":                                # os dois puxinhos (atrás do contorno)
        for (x, y, r) in ((-30, -58, 17), (-4, -66, 15)):
            cv.drawCircle(x, y, r, paint(lerpc(cor, "#000000", 0.12)))
            cv.drawCircle(x, y, r, paint("#000000", 70, "stroke", 2.4))
    c = skia.Path(); c.addCircle(0, 0, R_CAB)
    _sombrear(cv, c, PELE, 0.0, aro=((12, -0.07),))
    # v2 (revisor): o contorno da cabeça vem ANTES do cabelo e o cabelo o cobre (antes o círculo atravessava o
    # cabelo e parecia um "capacete transparente"); a borda do cabelo leva um traço no tom escuro do próprio cabelo
    cv.drawPath(c, paint(PELE_LINHA, 230, "stroke", 2.8))
    c2 = skia.Path(); c2.addCircle(0, 0, R_CAB + 1.8)
    cv.save(); cv.clipPath(c2, skia.ClipOp.kIntersect, True)
    cab = skia.Path()                                                # topo e nuca; o lado do rosto fica livre
    cab.moveTo(-70, 40); cab.lineTo(-70, -70); cab.lineTo(40, -70)
    cab.quadTo(46, -40, 28, -30); cab.quadTo(6, -24, -2, -10); cab.quadTo(-14, 10, -22, 36); cab.close()
    cv.drawPath(cab, paint(cor))
    cv.drawLine(-36, -40, -12, -52, paint(lerpc(cor, "#FFFFFF", 0.18), 200, "stroke", 5))
    cv.save(); cv.clipPath(cab, skia.ClipOp.kIntersect, True)
    cv.drawCircle(0, 0, R_CAB, paint(lerpc(cor, "#000000", 0.35), 230, "stroke", 2.8))
    cv.restore()
    cv.restore()
    if roupa["estilo"] == "cachos":                                  # cachos por cima do contorno
        for (x, y, r) in ((-46, -24, 15), (-52, 0, 14), (-46, 22, 12), (-30, -44, 15), (-8, -54, 15),
                          (16, -54, 14), (34, -44, 12), (-24, -10, 10)):
            cv.drawCircle(x, y, r, paint(cor))
            cv.drawCircle(x - 3, y - 3, r * 0.45, paint(lerpc(cor, "#FFFFFF", 0.14)))
    elif roupa["estilo"] == "puxinhos":
        for (x, y, r) in ((-30, -58, 17),):                          # amarradores dos puxinhos (azul-claro)
            cv.drawCircle(x + 9, y + 9, 5, paint(AZUL_CL))
        cv.drawCircle(-4 + 6, -66 + 11, 4.5, paint(AZUL_CL))
    cv.drawOval(skia.Rect(-12, -6, 4, 16), paint(PELE_ESC))           # orelha
    cv.drawOval(skia.Rect(-12, -6, 4, 16), paint(PELE_LINHA, 220, "stroke", 2.2))
    cv.restore()


def crianca(cv, p, roupa, cbs=None):
    """A criança inteira, de perfil. Ordem: perna e braço de trás, [atras], perna da frente, tronco, [meio],
    cabeça, [frente], braço da frente, [fim]. Os ganchos desenham em coordenadas do MUNDO."""
    cbs = cbs or {}
    J = _joints(p)
    cv.save(); cv.translate(p["hx"], p["hy"])

    def gancho(nome):
        if nome in cbs:
            cv.save(); cv.translate(-p["hx"], -p["hy"]); cbs[nome](J); cv.restore()
    perna(cv, J, "l", p, roupa, 0.30)
    braco(cv, J, "l", p, roupa, 0.30)
    gancho("atras")
    perna(cv, J, "p", p, roupa, 0.0)
    tronco(cv, p, roupa)
    gancho("meio")
    cabeca(cv, J, p, roupa)
    gancho("frente")
    braco(cv, J, "p", p, roupa, 0.0)
    gancho("fim")
    cv.restore()
    return J


def no_mundo(p, pt):
    return p["hx"] + pt[0], p["hy"] + pt[1]


def centro_palma(J, lado="p"):
    pun = J["pun_" + lado]; a = math.radians(J["mao_ang_" + lado])
    return pun[0] + PALMA_D * math.cos(a), pun[1] + PALMA_D * math.sin(a)


# ------------------------------------------------------------------ quadros-chave com Hermite (Catmull-Rom não uniforme)
def _soma(a, b, s=1.0):
    if isinstance(a, tuple):
        return tuple(x + s * y for x, y in zip(a, b))
    return a + s * b


def _esc(a, s):
    if isinstance(a, tuple):
        return tuple(x * s for x in a)
    return a * s


class Chaves:
    """Quadros-chave (f, {campo: valor}) com valores herdados da chave anterior. Interpolação de Hermite com
    tangentes de Catmull-Rom (não uniforme): o movimento passa pelas chaves sem parar. Chave com "_para": True
    (e as pontas) tem tangente zero: ali o movimento assenta."""

    def __init__(self, chaves):
        self.ts, self.vs, self.para = [], [], []
        ant = {}
        for f, d in chaves:
            v = dict(ant); v.update({k: x for k, x in d.items() if k != "_para"})
            self.ts.append(f); self.vs.append(v); self.para.append(bool(d.get("_para")))
            ant = v
        self.campos = list(self.vs[-1].keys())
        n = len(self.ts)
        self.tg = []
        for i in range(n):
            m = {}
            for c in self.campos:
                if i == 0 or i == n - 1 or self.para[i]:
                    m[c] = _esc(self.vs[i][c], 0.0)
                else:
                    dt = self.ts[i + 1] - self.ts[i - 1]
                    m[c] = _esc(_soma(self.vs[i + 1][c], self.vs[i - 1][c], -1.0), 1.0 / dt)
            self.tg.append(m)

    def pose(self, f):
        ts = self.ts
        if f <= ts[0]:
            return dict(self.vs[0])
        if f >= ts[-1]:
            return dict(self.vs[-1])
        i = 0
        while ts[i + 1] <= f:
            i += 1
        h = ts[i + 1] - ts[i]; u = (f - ts[i]) / h
        h00 = 2 * u ** 3 - 3 * u ** 2 + 1; h10 = u ** 3 - 2 * u ** 2 + u
        h01 = -2 * u ** 3 + 3 * u ** 2; h11 = u ** 3 - u ** 2
        out = {}
        for c in self.campos:
            p0, p1 = self.vs[i][c], self.vs[i + 1][c]
            m0, m1 = self.tg[i][c], self.tg[i + 1][c]
            v = _soma(_soma(_esc(p0, h00), _esc(m0, h10 * h)), _soma(_esc(p1, h01), _esc(m1, h11 * h)))
            out[c] = v
        return out


def _ombro_mundo(hip, tor, enc):
    o = rot((2.0, -L_OMBRO - 9.0 * enc), tor)
    return hip[0] + o[0], hip[1] + o[1]


def quadril_pendurado(A, tor, ab, enc=0.0):
    """Quadril de quem está pendurado pela mão (palma no ponto A), com o tronco inclinado `tor` e o braço
    esticado a `ab` graus da vertical (para a frente)."""
    so = rot((2.0, -L_OMBRO - 9.0 * enc), tor)
    L = ALCANCE + PALMA_D
    return A[0] - so[0] - L * math.sin(math.radians(ab)), A[1] - so[1] + L * math.cos(math.radians(ab))


def _base_pose(**k):
    p = dict(hx=0.0, hy=0.0, tor=0.0, cab=0.0, enc=0.0, mp=(8.0, 32.0), ml=(4.0, 30.0), mp_rel=0.0, ml_rel=0.0,
             mp_abre=0.25, ml_abre=0.45, pp=(10.0, 184.0), pl=(-12.0, 184.0), ppa=0.0, pla=0.0, dir=1.0)
    p.update(k)
    return p


# ------------------------------------------------------------------ 1º lance: o upa pela mão (tempo de FILME)
# v2 (revisor): descida mais curta (o pé toca o chão NO "Pou-"), a mão adulta solta NO toque e o braço cai durante
# o "Pousou" (antes: tocava 0,5 s depois e o "deixa o braço esticado" aparecia com o braço ERGUIDO e seguro)
F_AGACHA, F_SOBE, F_DESCOLA, F_PICO, F_POUSO, F_SOLTA, F_DESCE = 0.04, 0.20, 0.27, 0.45, 0.54, 0.57, 0.70
X0, X_POUSO = 400.0, 852.0                                       # quadril: antes da poça e depois dela
PE1_ANTES, PE1_DEPOIS = (414.0, 388.0), (866.0, 840.0)           # tornozelos (perto, longe) no chão
POCA1 = (640.0, 128.0)                                           # centro x e meio-eixo x da poça do 1º lance
POCA2 = (560.0, 118.0)


class Lance1:
    """O upa pela mão. Posturas por quadros-chave; a mão adulta (A = centro da palma da criança, dentro da mão
    adulta) segue a sua própria trilha. Enquanto segura, a criança é PUXADA para que a mão alcance A (o braço
    nunca se solta da mão adulta) e o alvo da mão dela é A."""

    def __init__(self, f_anda0=None, f_anda1=None):
        self.f_anda0, self.f_anda1 = f_anda0, f_anda1
        h0 = dict(hip=(X0, 892.0), A=(526.0, 668.0), tor=3.0, cab=0.0, enc=0.0, ml=(4.0, 30.0), mp_abre=0.1,
                  ml_abre=0.45, plx=(14.0, -12.0), ppa=0.0, pla=0.0, ppy=(184.0, 184.0), ad=1.0)
        ch = [(-3.0, dict(h0, _para=True)),
              (F_AGACHA, dict(_para=True)),
              (F_SOBE, dict(hip=(406.0, 912.0), A=(530.0, 690.0), tor=14.0, cab=-6.0, plx=(14.0, -10.0),
                            ppy=(164.0, 164.0))),
              (F_DESCOLA, dict(hip=quadril_pendurado((600.0, 604.0), 22.0, 34.0), A=(600.0, 604.0), tor=22.0,
                               cab=-26.0, plx=(-14.0, -30.0), ppy=(178.0, 174.0), ppa=26.0, pla=30.0,
                               ml=(-18.0, 26.0))),
              (0.36, dict(hip=quadril_pendurado((700.0, 540.0), 24.0, 46.0), A=(700.0, 540.0), tor=24.0,
                          cab=-36.0, plx=(-6.0, -20.0), ppy=(181.0, 178.0), ppa=30.0, pla=32.0, ml=(4.0, 30.0))),
              (F_PICO, dict(hip=quadril_pendurado((800.0, 520.0), 25.0, 55.0), A=(800.0, 520.0), tor=25.0,
                            cab=-44.0, plx=(6.0, -10.0), ppy=(182.0, 180.0), ppa=32.0, pla=34.0, ml=(16.0, 30.0))),
              (0.50, dict(hip=quadril_pendurado((880.0, 566.0), 12.0, 34.0), A=(880.0, 566.0), tor=12.0,
                          cab=-20.0, plx=(22.0, 6.0), ppy=(180.0, 180.0), ppa=10.0, pla=12.0, ml=(14.0, 28.0))),
              (F_POUSO, dict(hip=(X_POUSO, 904.0), A=(985.0, 682.0), tor=6.0, cab=-4.0, plx=(14.0, -12.0),
                             ppy=(172.0, 172.0), ppa=0.0, pla=0.0, ml=(8.0, 30.0))),
              (F_SOLTA, dict(hip=(X_POUSO, 893.0), A=(988.0, 678.0), tor=4.0, cab=0.0, ppy=(183.0, 183.0),
                             _para=True)),
              (0.70, dict(A=(950.0, 470.0), cab=6.0)),
              (0.84, dict(A=(880.0, 180.0), cab=15.0, enc=1.0, tor=6.0, ad=0.0)),
              (1.00, dict(cab=17.0, _para=True)),
              # v2 (revisor): micromovimento no 1× do nome/frequência (a dor é postura): a cabeça baixa mais, o
              # ombro encolhe, o tronco se curva um pouco, e volta — o quadro nunca fica parado
              (1.30, dict(_para=True)),
              (2.10, dict(cab=25.0, enc=1.6, tor=9.0)),
              (2.90, dict(cab=20.0, enc=1.25, tor=6.5)),
              (3.70, dict(cab=26.0, enc=1.7, tor=9.5)),
              (4.50, dict(cab=21.0, enc=1.35, tor=7.0, _para=True)),
              (60.0, dict(_para=True))]
        self.K = Chaves(ch)
        self.alvo_solta = None
        self.alvo_solta = self._base(F_SOLTA)[2]

    def _base(self, f):
        """-> (chaves, quadril depois da puxada, alvo do punho segurando (rel. ao quadril))."""
        k = self.K.pose(f)
        hip = k["hip"]; A = k["A"]; tor = k["tor"]
        if f <= F_SOLTA + 0.05:                                    # puxada: a mão alcança A
            om = _ombro_mundo(hip, tor, k["enc"])
            dx, dy = A[0] - om[0], A[1] - om[1]
            d = math.hypot(dx, dy) or 1.0
            lim = ALCANCE + PALMA_D
            if d > lim:
                s = (d - lim) / d
                hip = (hip[0] + dx * s, hip[1] + dy * s)
        om = _ombro_mundo(hip, tor, k["enc"])
        ux, uy = A[0] - om[0], A[1] - om[1]; d = math.hypot(ux, uy) or 1.0
        alvo = (A[0] - ux / d * PALMA_D - hip[0], A[1] - uy / d * PALMA_D - hip[1])
        return k, hip, alvo

    def chao(self, f):
        """1 = pés no chão; 0 = no ar."""
        return 1 - sstep(prog(f, F_SOBE + 0.03, F_DESCOLA)) + sstep(prog(f, F_POUSO - 0.035, F_POUSO))

    def pose(self, f):
        """-> (pose da criança, A (mundo) ou None, alfa da mão adulta, segurando 0..1)."""
        k, hip, alvo_seg = self._base(f)
        A = k["A"]; tor = k["tor"]
        segura = 1.0 - sstep(prog(f, F_SOLTA, F_SOLTA + 0.05))
        hx, hy = hip
        chao = clamp(self.chao(f))
        antes = f < (F_SOBE + F_POUSO) / 2
        pw = PE1_ANTES if antes else PE1_DEPOIS
        ppy = lerp(k["ppy"][0], ANK - hy, chao) if chao > 0 else k["ppy"][0]
        ply = lerp(k["ppy"][1], ANK - hy, chao) if chao > 0 else k["ppy"][1]
        ppx = lerp(k["plx"][0], pw[0] - hx, chao)
        plx = lerp(k["plx"][1], pw[1] - hx, chao)
        ppy = min(ppy, ANK - hy); ply = min(ply, ANK - hy)
        # a mão da criança: enquanto segura, o punho mira A (a palma fica dentro da mão adulta); depois de soltar
        # ela desce do ponto em que soltou (não acompanha a mão adulta que vai embora) até ficar ao lado do corpo
        desce = e_inout(prog(f, F_SOLTA, F_DESCE))
        if f >= F_SOLTA and self.alvo_solta is not None:
            # v2: o braço cai ESTICADO, num arco em volta do ombro (pêndulo), sem dobrar o cotovelo no caminho
            om = rot((2.0, -L_OMBRO - 9.0 * k["enc"]), tor)
            a0 = (self.alvo_solta[0] - om[0], self.alvo_solta[1] - om[1])
            a1 = (6.0 - om[0], 32.0 - om[1])
            g0, g1 = math.atan2(a0[1], a0[0]), math.atan2(a1[1], a1[0])
            g = lerp(g0, g1, desce); r = lerp(math.hypot(*a0), math.hypot(*a1), desce)
            mp = (om[0] + r * math.cos(g), om[1] + r * math.sin(g))
        else:
            mp = alvo_seg
        resp = 1.4 * math.sin(f * 2.6) * prog(f, F_DESCE, F_DESCE + 0.3)     # respiração (filme andando)
        ml = k["ml"]; ppa, pla = k["ppa"], k["pla"]
        # v2: "leve pra avaliar" = ela sai andando devagar para a direita, de cabeça baixa, e o braço do puxão
        # CONTINUA parado ao lado do corpo (não balança); só o outro braço balança. Ninguém toca no braço.
        if self.f_anda0 is not None and f > self.f_anda0:
            a0, a1 = self.f_anda0, self.f_anda1
            w_anda = prog(f, a0, a0 + 0.35) * (1 - prog(f, a1 - 0.3, a1))
            dist = 0.0
            n = 40; b = min(f, a1)
            for i in range(n):
                x = a0 + (b - a0) * (i + 0.5) / n
                dist += V_ANDA1 * prog(x, a0, a0 + 0.35) * (1 - prog(x, a1 - 0.3, a1)) * (b - a0) / n
            hx += dist
            pw = (PE1_DEPOIS[0] + dist, PE1_DEPOIS[1] + dist)
            ppx = pw[0] - hx; plx = pw[1] - hx
            if w_anda > 0:
                u = (f - a0) / P_ANDA1
                hy -= 3.0 * abs(math.sin(2 * math.pi * u)) * w_anda
                pa, ya, aa = _pe_anda(u, 0.0, P_S1); pb, yb, ab_ = _pe_anda(u, 0.5, P_S1)
                ppx = lerp(ppx, pa, w_anda); ppy = lerp(ppy, ANK - hy - ya, w_anda); ppa = lerp(ppa, aa, w_anda)
                plx = lerp(plx, pb, w_anda); ply = lerp(ply, ANK - hy - yb, w_anda); pla = lerp(pla, ab_, w_anda)
                ml = (ml[0] + math.sin(2 * math.pi * u) * 10 * w_anda, ml[1])
        p = _base_pose(hx=hx, hy=hy, tor=tor + resp, cab=k["cab"], enc=k["enc"], mp=mp, ml=ml,
                       mp_abre=lerp(0.1, 0.35, desce), ml_abre=k["ml_abre"], pp=(ppx, ppy), pl=(plx, ply),
                       ppa=ppa, pla=pla)
        ang = angulo_adulto(f)
        return p, A, clamp(k["ad"] if f > F_SOLTA else 1.0), segura, ang


def angulo_adulto(f):
    """Direção do antebraço adulto (da mão para o cotovelo, graus): sobe pela esquerda; puxa mais para cima no
    alto do arco."""
    return lerp(-118.0, -104.0, sstep(prog(f, F_SOBE, F_PICO))) + 10.0 * sstep(prog(f, F_PICO, F_POUSO))


ESC_AD = 0.42                                                    # mão adulta na escala da criança


def adulto_tras(cv, A, ang, manga, a=1.0):
    """Antebraço + manga (longa: sai pela borda do recorte da cena) + palma, ATRÁS da mãozinha."""
    if a <= 0:
        return
    camada(cv, a)
    cv.translate(*A); cv.rotate(ang); cv.scale(ESC_AD, ESC_AD)
    mao_adulta_tras(cv, 1.0, manga=manga, some=None, comp=4200)
    cv.restore()


def adulto_frente(cv, A, ang, a=1.0):
    if a <= 0:
        return
    camada(cv, a)
    cv.translate(*A); cv.rotate(ang); cv.scale(ESC_AD, -ESC_AD)
    mao_adulta_frente(cv, 1.0)
    cv.restore()


# ------------------------------------------------------------------ 2º lance: o upa pelas axilas (OUTRA criança)
F2 = 20.0                                                        # tempo de filme da FITA 2 (outra tomada)
X2, X2_POUSO = 352.0, 780.0
PE2_ANTES, PE2_DEPOIS = (366.0, 340.0), (794.0, 768.0)
# v2 (revisor): o braço adulto do 2º lance vem de TRÁS, na altura do peito, quase HORIZONTAL (nunca desce por cima
# da cabeça), com COTOVELO visível: antebraço curto + braço subindo em outro ângulo até a borda (antes: um tubo
# reto de ~2.200 px que lia como "bastão/remo" batendo na nuca)
ANG_ANTE = -172.0                                                # da palma para o cotovelo (para trás, quase horizontal)
ANG_BRACO = -112.0                                               # do cotovelo para o ombro (sobe e sai pela borda)
L_ANTE = 165.0                                                   # antebraço adulto (~2x o da criança)
AXILA = (-20.0, -74.0)                                           # palma no flanco, atrás do braço dela, logo abaixo da axila
AXILA_L = (8.0, -86.0)                                           # a outra mão (do outro lado): só as pontas dos dedos passam
                                                                 # da frente do peito


class Lance2:
    """Pelas axilas (OUTRA criança, outra poça): as duas mãos adultas chegam POR TRÁS, na altura do peito (1×),
    a criança sobe num arco sobre a poça (0,25×) com os braços SOLTOS para baixo, pousa macio, as mãos saem para
    trás e ela segue andando."""

    def __init__(self, T):
        L0 = F2 + (T["upa2"] - T["corte"])                        # a subida começa NO "upa"
        self.L0 = L0
        self.f_topo = L0 + VL * (T["nao3"] - T["upa2"])
        self.f_pouso = L0 + VL * (T["pulsos_fim"] - T["upa2"]) - 0.02
        self.f_solta = self.f_pouso + 0.15
        self.f_anda0 = self.f_pouso + 0.70
        self.f_anda1 = self.f_anda0 + 1.6
        h0 = dict(hip=(X2, 892.0), tor=2.0, cab=0.0, enc=0.0, ml=(8.0, 30.0), mp=(12.0, 30.0), plx=(14.0, -12.0),
                  ppy=(184.0, 184.0), ppa=0.0, pla=0.0)
        ft, fp = self.f_topo, self.f_pouso
        ch = [(F2 - 1.0, dict(h0, _para=True)),
              (L0, dict(hip=(X2 + 2.0, 896.0), enc=0.3, _para=True)),
              (L0 + 0.12, dict(hip=(X2 + 40.0, 846.0), tor=6.0, cab=-6.0, enc=0.85, plx=(4.0, -18.0),
                               ppy=(176.0, 174.0), ppa=18.0, pla=22.0, mp=(6.0, 31.0), ml=(2.0, 31.0))),
              (ft, dict(hip=(492.0, 730.0), tor=8.0, cab=-10.0, enc=0.95, plx=(2.0, -16.0), ppy=(174.0, 172.0),
                        ppa=24.0, pla=26.0, mp=(22.0, 27.0), ml=(14.0, 28.0))),
              (lerp(ft, fp, 0.55), dict(hip=(640.0, 742.0), tor=6.0, cab=-6.0, plx=(14.0, -4.0),
                                        ppy=(176.0, 176.0), ppa=12.0, pla=14.0, mp=(30.0, 23.0), ml=(20.0, 25.0))),
              (fp - 0.06, dict(hip=(752.0, 860.0), tor=4.0, plx=(16.0, -10.0), ppy=(180.0, 180.0), ppa=4.0,
                               pla=4.0)),
              (fp, dict(hip=(X2_POUSO, 904.0), tor=4.0, cab=0.0, enc=0.6, ppy=(172.0, 172.0), ppa=0.0, pla=0.0,
                        mp=(20.0, 27.0))),
              (fp + 0.2, dict(hip=(X2_POUSO, 893.0), ppy=(183.0, 183.0), enc=0.0, _para=True)),
              (fp + 0.75, dict(mp=(14.0, 28.0), ml=(8.0, 28.0), _para=True)),
              (60.0 + F2, dict(_para=True))]
        self.K = Chaves(ch)

    def chao(self, f):
        return 1 - sstep(prog(f, self.L0 + 0.05, self.L0 + 0.12)) + sstep(prog(f, self.f_pouso - 0.03, self.f_pouso))

    def maos(self, f):
        """0..1: as mãos adultas chegam por trás (horizontal) e, depois do pouso, voltam para trás e saem."""
        chega = e_out(prog(f, F2 + 0.10, F2 + 0.80))
        sai = e_inout(prog(f, self.f_solta, self.f_solta + 0.55))
        return chega, sai

    def pose(self, f):
        k = self.K.pose(f)
        hx, hy = k["hip"]
        # andando (depois do pouso): passo curto de criança pequena
        w_anda = prog(f, self.f_anda0, self.f_anda0 + 0.25) * (1 - prog(f, self.f_anda1 - 0.25, self.f_anda1))
        dist = 0.0
        if f > self.f_anda0:
            n = 40; a, b = self.f_anda0, min(f, self.f_anda1)
            for i in range(n):
                x = a + (b - a) * (i + 0.5) / n
                dist += V_ANDA * prog(x, self.f_anda0, self.f_anda0 + 0.25) * (1 - prog(x, self.f_anda1 - 0.25, self.f_anda1)) * (b - a) / n
        hx += dist
        chao = clamp(self.chao(f))
        pw = PE2_ANTES if f < (self.L0 + self.f_pouso) / 2 else (PE2_DEPOIS[0] + dist, PE2_DEPOIS[1] + dist)
        ppy = min(lerp(k["ppy"][0], ANK - hy, chao), ANK - hy)
        ply = min(lerp(k["ppy"][1], ANK - hy, chao), ANK - hy)
        ppx = lerp(k["plx"][0], pw[0] - hx, chao)
        plx = lerp(k["plx"][1], pw[1] - hx, chao)
        mp, ml = k["mp"], k["ml"]
        ppa, pla = k["ppa"], k["pla"]
        if w_anda > 0:
            u = (f - self.f_anda0) / P_ANDA
            hy -= 3.0 * abs(math.sin(2 * math.pi * u)) * w_anda
            pa, ya, aa = _pe_anda(u, 0.0); pb, yb, ab_ = _pe_anda(u, 0.5)
            ppx = lerp(ppx, pa, w_anda); ppy = lerp(ppy, ANK - hy - ya, w_anda); ppa = lerp(ppa, aa, w_anda)
            plx = lerp(plx, pb, w_anda); ply = lerp(ply, ANK - hy - yb, w_anda); pla = lerp(pla, ab_, w_anda)
            bal = math.sin(2 * math.pi * u) * 12 * w_anda
            mp = (mp[0] - bal, mp[1]); ml = (ml[0] + bal, ml[1])
        resp = 1.0 * math.sin(f * 2.6)
        p = _base_pose(hx=hx, hy=hy, tor=k["tor"] + resp * 0.6, cab=k["cab"], enc=k["enc"], mp=mp, ml=ml,
                       mp_abre=0.55, ml_abre=0.55, mp_rel=10.0, ml_rel=10.0, pp=(ppx, ppy), pl=(plx, ply),
                       ppa=ppa, pla=pla)
        return p


P_ANDA, S_ANDA = 0.9, 26.0                                      # período do ciclo (2 passos), meia passada
V_ANDA = 4 * S_ANDA / P_ANDA                                     # o pé de apoio não escorrega
P_ANDA1, P_S1 = 1.0, 22.0                                        # 1º lance: passo mais curto e lento (dor)
V_ANDA1 = 4 * P_S1 / P_ANDA1


def _pe_anda(u, o, S=S_ANDA):
    """Pé no ciclo de marcha: -> (x rel. ao quadril, altura acima do chão, ângulo do tênis)."""
    v = (u + o) % 1.0
    if v < 0.5:
        k = v / 0.5
        return S - 2 * S * k, 0.0, 0.0
    w = (v - 0.5) / 0.5
    return -S + 2 * S * e_inout(w), 20.0 * math.sin(math.pi * w), 8.0 * math.sin(math.pi * w)


def axila_mundo(p, ponto=AXILA):
    o = rot(ponto, p["tor"])
    return p["hx"] + o[0], p["hy"] + o[1]


def _dir(graus):
    a = math.radians(graus)
    return math.cos(a), math.sin(a)


def _pt(o, d, k):
    return o[0] + d[0] * k, o[1] + d[1] * k


# v5 (3ª rodada da verificação em resolução cheia, 01/11): o braço do 2º lance era um TUBO cinza de largura constante
# — dois `tubo` unidos no cotovelo (quina viva por dentro), punho da manga num cilindro MAIS ESCURO, só ~30 px de pele
# entre a palma e a manga, duas linhas de brilho e uma prega — e, 12 px acima e paralelo a ele, o braço da mão de
# trás (contorno DUPLO): lia como cano/guindaste e não combinava com o 1º lance (3,0 s), em que o braço adulto tem
# manga AZUL, punho CLARO, antebraço e mão de pele. Agora é o MESMO braço do 1º lance (mao_adulta_tras na escala
# ESC_AD): pele da palma até K_PUNHO (os 190 × 0,42 de lá), punho claro, manga MANGA1 com o degradê cilíndrico de 5
# tons e contorno ÚNICO, um pouco mais larga que o antebraço e afinando para o punho; o cotovelo é uma CURVA (o eixo
# faz o canto num arco de círculo, e o degradê acompanha o arco). Os contornos são montados ponto a ponto (curvas
# paralelas ao eixo), sem skia.Op: nenhuma união que some em alguma pose. A geometria (ANG_ANTE, ANG_BRACO, L_ANTE,
# as palmas) é a mesma: o cotovelo continua no mesmo lugar (acima do inset do "não pelas mãos").
K_PUNHO = 72.0                                                   # da palma ao punho da manga (pele visível antes)
K_PUNHO_FAIXA = 13.0                                             # largura do punho claro (32 × 0,42 no 1º lance)
T_CURVA = 28.0                                                   # o eixo deixa a reta a T_CURVA do cotovelo (arco)
MEIA_PELE = (15.0, 17.0)                                         # antebraço de pele: no pulso, sob o punho
MEIA_MANGA = (21.0, 25.0, 29.0)                                  # manga: no punho, no cotovelo, no braço (bíceps)
MEIA_DEGRADE = 24.0                                              # meia largura do degradê (a mesma nos três trechos)
PARADAS = [0.0, 0.22, 0.5, 0.78, 1.0]


def _faixa_lados(pts, larg):
    """Os dois lados (esq. e dir. de quem anda de pts[0] para pts[-1]) de uma faixa de meia largura larg[i] em volta
    da linha pts: curvas paralelas ao eixo, ponto a ponto (sem skia.Op)."""
    n = len(pts)
    esq, dir_ = [], []
    for i in range(n):
        a = pts[max(i - 1, 0)]; b = pts[min(i + 1, n - 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tx, ty) or 1.0
        nx, ny = -ty / L, tx / L
        esq.append((pts[i][0] + nx * larg[i], pts[i][1] + ny * larg[i]))
        dir_.append((pts[i][0] - nx * larg[i], pts[i][1] - ny * larg[i]))
    return esq, dir_


def _poli(pontos):
    p = skia.Path()
    p.moveTo(*pontos[0])
    for q in pontos[1:]:
        p.lineTo(*q)
    p.close()
    return p


def _curva_cotovelo(P, u, v):
    """O canto do cotovelo como ARCO de círculo tangente às duas retas (antebraço ao longo de u, braço ao longo de
    v): -> (T0, T1, centro O, raio r, ângulo inicial e varredura em graus)."""
    E = _pt(P, u, L_ANTE)
    vira = math.degrees(math.atan2(u[0] * v[1] - u[1] * v[0], u[0] * v[0] + u[1] * v[1]))   # quanto o eixo gira
    r = T_CURVA / math.tan(math.radians(abs(vira)) / 2)
    s = 1.0 if vira > 0 else -1.0
    n_in = (-u[1] * s, u[0] * s)                                   # para dentro da curva
    T0 = _pt(E, u, -T_CURVA); T1 = _pt(E, v, T_CURVA)
    O = _pt(T0, n_in, r)
    g0 = math.degrees(math.atan2(T0[1] - O[1], T0[0] - O[0]))
    return T0, T1, O, r, g0, vira


def _eixo_braco(P, u, v):
    """Eixo da manga (do punho ao fim do braço, fora da cena) e a meia largura em cada ponto."""
    T0, T1, O, r, g0, vira = _curva_cotovelo(P, u, v)
    k_t0 = L_ANTE - T_CURVA
    pts, ws = [], []
    n0 = 10                                                        # antebraço (reto): do punho até o arco
    for i in range(n0):
        k = K_PUNHO + (k_t0 - K_PUNHO) * i / n0
        pts.append(_pt(P, u, k)); ws.append(lerp(MEIA_MANGA[0], MEIA_MANGA[1], (k - K_PUNHO) / (k_t0 - K_PUNHO)))
    n1 = 24                                                        # o arco do cotovelo
    for i in range(n1 + 1):
        g = math.radians(g0 + vira * i / n1)
        pts.append((O[0] + r * math.cos(g), O[1] + r * math.sin(g))); ws.append(MEIA_MANGA[1])
    for k in (60.0, 110.0, 170.0, 260.0, 420.0, 900.0, 1500.0):   # braço (reto): engrossa e sai da cena
        pts.append(_pt(T1, v, k - T_CURVA))
        ws.append(lerp(MEIA_MANGA[1], MEIA_MANGA[2], sstep((k - T_CURVA) / 230.0)))
    return pts, ws


def _meio_plano(Q, d):
    """Meio-plano {X : (X - Q)·d > 0} (polígono grande)."""
    m = (-d[1], d[0]); G = 6000.0
    return _poli([_pt(Q, m, G), _pt(Q, m, -G), _pt(_pt(Q, m, -G), d, G), _pt(_pt(Q, m, G), d, G)])


def _degrade(o, nrm, w, tons):
    """Degradê cilíndrico (5 tons simétricos) perpendicular ao eixo reto que passa por o."""
    return skia.GradientShader.MakeLinear([skia.Point(*_pt(o, nrm, w)), skia.Point(*_pt(o, nrm, -w))],
                                          [_c(c) for c in tons], PARADAS)


def _degrade_arco(O, r, w, tons):
    """O mesmo degradê seguindo o ARCO (radial em volta do centro da curva)."""
    R = r + w
    return skia.GradientShader.MakeRadial(skia.Point(*O), R, [_c(tons[0])] + [_c(c) for c in tons],
                                          [0.0] + [(r - w + f * 2 * w) / R for f in PARADAS])


def braco_adulto(cv, P, manga, a, escuro=0.0):
    """Braço adulto do 2º lance, da palma em P, no MESMO desenho do 1º lance (v5): antebraço de pele, punho claro,
    manga com degradê cilíndrico e contorno único, quase horizontal PARA TRÁS, cotovelo em CURVA e o braço subindo
    até sair pela borda da cena."""
    if a <= 0:
        return
    esc = camada_escura(cv, a, escuro)                             # v4: sem filtro de cor (ver camada_escura)
    u = _dir(ANG_ANTE); v = _dir(ANG_BRACO)
    nu = (-u[1], u[0]); nv = (-v[1], v[0])
    # antebraço de pele: do meio da palma até um pouco DENTRO da manga (a manga o cobre); ponta redonda sob a palma
    k0, k1 = 2.0, K_PUNHO + 14.0
    eixo = [_pt(P, u, k0 + (k1 - k0) * i / 8) for i in range(9)]
    e, d = _faixa_lados(eixo, [lerp(MEIA_PELE[0], MEIA_PELE[1], i / 8) for i in range(9)])
    P0 = eixo[0]
    tampa = [_pt(P0, (-math.cos(g) * nu[0] - math.sin(g) * u[0], -math.cos(g) * nu[1] - math.sin(g) * u[1]),
                 MEIA_PELE[0]) for g in [math.pi * j / 12 for j in range(1, 12)]]     # de d[0] a e[0] pela palma
    pele = _poli(e + d[::-1] + tampa)
    _pele(cv, pele, _pt(P, nu, MEIA_PELE[1]), _pt(P, nu, -MEIA_PELE[1]), 1.0, tons=TONS_AD, cor_linha=AD_LINHA,
          linha=2.4)
    # a manga: UM contorno, do punho até fora da cena
    pts, ws = _eixo_braco(P, u, v)
    e, d = _faixa_lados(pts, ws)
    C = pts[0]
    mg = skia.Path()
    mg.moveTo(*e[0])
    for q in e[1:]:
        mg.lineTo(*q)
    for q in d[::-1]:
        mg.lineTo(*q)
    mg.quadTo(*_pt(C, u, -5.0), *e[0])                              # a boca da manga, levemente abaulada
    mg.close()
    # degradê em três trechos (antebraço, arco, braço) cortados nas retas que ligam o centro do arco aos pontos de
    # tangência: ali a distância ao eixo reto é a mesma distância ao arco, e os tons são simétricos -> sem emenda.
    # O arco vai inteiro por baixo; os trechos retos, recortados, por cima (sem fresta de antialias na emenda).
    T0, T1, O, r, g0, vira = _curva_cotovelo(P, u, v)
    cv.drawPath(mg, paint(manga["tons"][1], 255, shader=_degrade_arco(O, r, MEIA_DEGRADE, manga["tons"])))
    for Q, dd, o, nrm in ((T0, (-u[0], -u[1]), T0, nu), (T1, v, T1, nv)):
        cv.save(); cv.clipPath(_meio_plano(Q, dd), skia.ClipOp.kIntersect, True)
        cv.drawPath(mg, paint(manga["tons"][1], 255, shader=_degrade(o, nrm, MEIA_DEGRADE, manga["tons"])))
        cv.restore()
    # punho claro na boca da manga (como no 1º lance) e a costura que o separa da manga
    cv.save(); cv.clipPath(mg, skia.ClipOp.kIntersect, True)
    C1 = _pt(C, u, K_PUNHO_FAIXA)
    cv.drawPath(_poli([_pt(_pt(C, u, -12.0), nu, 40.0), _pt(C1, nu, 40.0), _pt(C1, nu, -40.0),
                       _pt(_pt(C, u, -12.0), nu, -40.0)]), paint(manga["punho"], 235))
    cv.drawLine(*_pt(C1, nu, 30.0), *_pt(C1, nu, -30.0), paint(manga["linha"], 200, "stroke", 1.6))
    for fr, L in ((0.36, 10.0), (0.66, 7.5)):                      # o tecido franze POR DENTRO do cotovelo
        g = math.radians(g0 + vira * fr); dg = (math.cos(g), math.sin(g)); r_in = r - MEIA_MANGA[1]
        cv.drawLine(*_pt(O, dg, r_in + 1.0), *_pt(O, dg, r_in + L), paint(manga["linha"], 150, "stroke", 2.0))
    cv.restore()
    cv.drawPath(mg, paint(manga["linha"], 235, "stroke", 2.6))
    if esc:                                                        # caixa que cobre pele e manga (a camada só tem o
        b0, b1 = pele.computeTightBounds(), mg.computeTightBounds()          # braço: a caixa não toca em mais nada)
        escurecer(cv, rr_path(min(b0.left(), b1.left()), min(b0.top(), b1.top()), max(b0.right(), b1.right()),
                              max(b0.bottom(), b1.bottom()), 1.0), escuro)
    cv.restore()


def mao_axila(cv, P, a, escuro=0.0):
    """Palma no flanco (logo abaixo da axila) e quatro dedos para a FRENTE, abraçando o peito; polegar para cima,
    atrás do ombro."""
    if a <= 0:
        return
    esc = camada_escura(cv, a, escuro)                             # v4: sem filtro de cor (ver camada_escura)
    cv.translate(*P); cv.rotate(ANG_ANTE + 180.0)
    for i, L in enumerate((44.0, 52.0, 51.0, 44.0)):
        y0 = -23 + i * 11.5
        d = rr_path(4, y0, 4 + L, y0 + 11.5, 5.75)
        _pele(cv, d, (0, y0), (0, y0 + 11.5), 1.0, tons=TONS_AD, cor_linha=AD_LINHA, linha=2.2)
    palma = skia.Path(); palma.addOval(skia.Rect(-26, -25, 20, 24))
    _pele(cv, palma, (0, -25), (0, 24), 1.0, tons=TONS_AD, cor_linha=AD_LINHA, linha=2.4)
    cv.save(); cv.translate(-6, -16); cv.rotate(-78)
    pol = rr_path(0, -6.5, 34, 6.5, 6.5)
    _pele(cv, pol, (0, -6.5), (0, 6.5), 1.0, tons=TONS_AD, cor_linha=AD_LINHA, linha=2.2)
    cv.restore()
    if esc:                                                        # caixa que cobre dedos, palma e polegar
        escurecer(cv, rr_path(-36.0, -62.0, 66.0, 38.0, 8.0), escuro)
    cv.restore()


# ------------------------------------------------------------------ o tempo do filme
V1, VL = 1.0, 0.25


def fita(t, T):
    """1 = o upa pela mão; 2 = OUTRA criança, outra poça (depois do corte de fita no "Pra ajudar a prevenir")."""
    return 1 if t < T["corte"] else 2


def t_descongela(T):
    """v2 (revisor): a 0,25× a descida dura 0,36 s de vídeo; descongelar 0,2 s ANTES do "Pousou" faz o pé tocar o
    chão no "Pou-"."""
    return T["pousou"] - 0.2


class Filme:
    """Liga o tempo do VÍDEO ao tempo do FILME (cópia adaptada do piloto): play (1×), volta (rebobinar),
    lenta (0,25×), congela (0×), presos às palavras-âncora. O ◀◀ acaba ANTES da subida; o 2º lance entra por
    CORTE de fita (salto do tempo do filme escondido pelo chiado), nunca voltando a fita pelo braço parado."""

    def __init__(self, T):
        s = []
        s.append((0.0, T["volta"], "play", 0.0, V1 * T["volta"], None))
        f_s = F_PICO - VL * (T["repara"] - T["camera"])          # a 0,25×, chega ao alto do arco NO "repara"
        s.append((T["volta"], T["camera"], "volta", V1 * T["volta"], f_s, "inout"))
        s.append((T["camera"], T["repara"], "lenta", f_s, F_PICO, None))
        td = t_descongela(T)
        s.append((T["repara"], td, "congela", F_PICO, F_PICO, None))
        f_c = F_PICO + VL * (T["corpo"] - td)
        s.append((td, T["corpo"], "lenta", F_PICO, f_c, None))
        s.append((T["corpo"], T["e3"], "congela", f_c, f_c, None))
        s.append((T["e3"], T["corte"], "play", f_c, f_c + V1 * (T["corte"] - T["e3"]), None))
        L0 = F2 + V1 * (T["upa2"] - T["corte"])
        s.append((T["corte"], T["upa2"], "play", F2, L0, None))
        fa = L0 + VL * (T["pulsos_fim"] - T["upa2"])
        s.append((T["upa2"], T["pulsos_fim"], "lenta", L0, fa, None))
        fim = T["total"] + 2.0
        s.append((T["pulsos_fim"], fim, "play", fa, fa + V1 * (fim - T["pulsos_fim"]), None))
        self.segs = s
        self.T = T
        self.f_s, self.f_c = f_s, f_c
        assert f_s < F_AGACHA, ("o ◀◀ tem de acabar ANTES da subida", f_s)
        f_anda0 = f_c + (T["avaliar"] + 0.15 - T["e3"])                # "leve pra avaliar": ela sai andando
        self.R1 = Lance1(f_anda0, f_c + (T["corte"] - T["e3"]) + 1.0)
        self.R2 = Lance2(T)

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

    def tipo(self, t):
        return self.seg(t)[2]

    def inicio_trecho(self, t):
        i = self.segs.index(self.seg(t))
        while i > 0 and self.segs[i - 1][2] == self.segs[i][2] and self.segs[i - 1][1] == self.segs[i][0]:
            i -= 1
        return self.segs[i][0]


def lento_k(t, T):
    """0..1: quanto a câmera lenta está LIGADA (selo e moldura âmbar existem só aqui): do "câmera" ao "é" e do
    2º "upa" ao fim do "pulsos"."""
    return max(prog(t, T["camera"], T["camera"] + 0.18) * (1 - prog(t, T["e3"] - 0.2, T["e3"])),
               prog(t, T["upa2"], T["upa2"] + 0.18) * (1 - prog(t, T["pulsos_fim"] - 0.2, T["pulsos_fim"])))


# ------------------------------------------------------------------ câmera (mundo -> tela)
BASE = (1.1, 630.0, 1000.0, 540.0, 990.0)                      # 1×: o lance inteiro, poça no meio


def _mist(a, b, k):
    return tuple(lerp(x, y, k) for x, y in zip(a, b))


def _cotovelo_pico(F):
    p, A, _, _, _ = F.R1.pose(F_PICO)
    J = _joints(p)
    return no_mundo(p, J["cot_p"])


def cam_congela(F):
    """Câmera do congelamento no alto do arco (1,15×: o chão e a poça aparecem embaixo — ela está NO AR)."""
    c = _cotovelo_pico(F)
    return (1.15, c[0], c[1], CAM_COT[0], CAM_COT[1])


def cam_cotovelo(F):
    """v2 (revisor): 2º passo no "cotovelo": ~1,45× centrado no cotovelo (o detalhe ocupa o quadro)."""
    c = _cotovelo_pico(F)
    return (1.45, c[0], c[1], CAM_COT2[0], CAM_COT2[1])


CAM_COT = (560.0, 540.0)                                         # o cotovelo na tela, congelado (o chão e a poça
                                                                 # aparecem embaixo: ela está NO AR, sobre a poça)
CAM_COT2 = (470.0, 640.0)                                        # no 2º passo: lupa à direita, longe do braço


def cameras(T, F):
    """Passos de câmera presos às palavras: (t0, duração, (escala, x_mundo, y_mundo, x_tela, y_tela))."""
    cz = cam_congela(F)
    cc = cam_cotovelo(F)
    p, _, _, _, _ = F.R1.pose(F.f_c)
    J = _joints(p)
    br = no_mundo(p, J["cot_p"])                                  # o braço parado (mundo)
    td = t_descongela(T)
    fim_ped = T["pequenas"] + 0.6
    x_anda = p["hx"] + V_ANDA1 * (T["corte"] - T["avaliar"] - 0.4)    # aonde ela chega andando
    return (
        (T["camera"], 0.9, (1.22, 450.0, 800.0, 470.0, 790.0)),                # chega no braço erguido e nas mãos
        (T["braco1"], T["repara"] - T["braco1"], (1.12, 640.0, 700.0, 540.0, 640.0)),   # acompanha a subida
        (T["repara"], 0.13, cz),                                                 # zoom seco no braço
        # v2 (revisor: congelamento parado demais): no quadro congelado a câmera DERIVA devagar (linear)
        (T["repara"] + 0.13, T["cotovelo"] - T["repara"] - 0.18, (1.32,) + cz[1:], "lin"),
        (T["cotovelo"] - 0.05, 0.55, cc),                                        # 2º passo: o cotovelo de perto
        (T["cotovelo"] + 0.5, td - T["cotovelo"] - 0.5, (1.54,) + cc[1:], "lin"),
        (td, 0.75, (1.2, 800.0, 820.0, 560.0, 780.0)),                           # acompanha a descida
        (T["crianca"] - 0.1, 0.8, (1.30, p["hx"], 860.0, 560.0, 800.0)),        # o braço parado, perto
        (T["crianca"] + 0.7, T["corpo"] - T["crianca"] - 0.7, (1.42, p["hx"], 860.0, 560.0, 800.0), "lin"),
        (T["corpo"], T["e3"] - T["corpo"], (1.52, p["hx"], 860.0, 560.0, 800.0), "lin"),
        (T["e3"], 0.45, (1.15, br[0], br[1], 470.0, 760.0)),                    # 1×: abre um pouco
        (T["pronacao"], fim_ped - T["pronacao"], (1.40, br[0], br[1], 430.0, 720.0)),   # push-in lento no braço
        (T["leve"] - 0.1, 1.0, (1.14, p["hx"] + 60.0, 940.0, 470.0, 930.0)),    # abre: o plano geral
        (T["avaliar"] + 0.5, T["corte"] - T["avaliar"] - 0.5,
         (1.12, x_anda - 40.0, 940.0, 560.0, 930.0)),                            # acompanha ela saindo, devagar
        (T["corte"], 0.03, (1.1, 560.0, 1000.0, 540.0, 990.0)),                 # fita 2 (sob o chiado)
        (T["corte"] + 0.05, T["upa2"] - T["corte"] - 0.15,
         (1.2, 420.0, 860.0, 520.0, 850.0)),                                     # as mãos chegam por trás (perto)
        (T["upa2"] - 0.1, 0.9, (1.12, 560.0, 900.0, 540.0, 880.0)),             # 2ª câmera lenta: o arco
        (T["pulsos_fim"], 0.7, (1.1, 640.0, 1000.0, 540.0, 990.0)),
    )


def camera(t, passos):
    cam = BASE
    for passo in passos:
        t0, d, alvo = passo[:3]
        k = prog(t, t0, t0 + d) if len(passo) > 3 else e_inout(prog(t, t0, t0 + d))
        if k > 0:
            cam = _mist(cam, alvo, k)
    return cam


def aplica(cv, cam):
    s, wx, wy, sx, sy = cam
    cv.translate(sx, sy); cv.scale(s, s); cv.translate(-wx, -wy)


def na_tela(cam, x, y):
    s, wx, wy, sx, sy = cam
    return sx + s * (x - wx), sy + s * (y - wy)


# ------------------------------------------------------------------ camadas fixas em cache (desempenho; cópia do piloto)
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
        sh = skia.GradientShader.MakeRadial(skia.Point(540, 760), 780, [_c("#000000", 0), _c("#000000", 0), _c("#000000", 85)],
                                            [0.0, 0.55, 1.0])
        c.drawRect(CENA, paint("#000000", 255, shader=sh))
    _blit(cv, _img("monitor", CENA.width(), CENA.height(), d), CENA.left(), CENA.top())


# ------------------------------------------------------------------ cenário: a calçada à noite e as poças
def _poste(cv, x, s):
    """Poste de luz (forma) com o brilho pronto em imagem."""
    def d(c):
        sh = skia.GradientShader.MakeRadial(skia.Point(200, 200), 200, [_c("#FFE6A8", 90), _c("#FFE6A8", 0)])
        c.drawCircle(200, 200, 200, paint("#FFE6A8", 255, shader=sh))
    cv.drawImage(_img("brilho_poste", 400, 400, d), x - 200 + 26, GY - 560 - 200 + 12)
    cv.drawRect(skia.Rect(x - 7, GY - 560, x + 7, GY - 30), paint("#22384A"))
    cv.drawRect(skia.Rect(x - 7, GY - 560, x + 40, GY - 548), paint("#22384A"))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x + 10, GY - 552, x + 44, GY - 536), 6, 6), paint("#F6E3B0"))


def _poca(cv, cx, rx, s):
    """Poça: elipse azul-acinzentada no chão, com riscos claros de reflexo."""
    ry = 21.0
    cy = GY + 18.0
    cv.drawOval(skia.Rect(cx - rx - 4, cy - ry - 2, cx + rx + 4, cy + ry + 3), paint(POCA_ESC))
    cv.drawOval(skia.Rect(cx - rx, cy - ry, cx + rx, cy + ry), paint(POCA))
    cv.save(); cv.clipRect(skia.Rect(cx - rx, cy - ry, cx + rx, cy + ry))
    cv.drawOval(skia.Rect(cx - rx * 0.7, cy - ry * 0.75, cx + rx * 0.55, cy + ry * 0.35), paint(lerpc(POCA, POCA_CL, 0.25)))
    cv.restore()
    for dx, dy, L in ((-0.42, -0.25, 0.30), (0.05, 0.05, 0.22), (0.30, -0.35, 0.16)):
        x0 = cx + dx * rx; y0 = cy + dy * ry
        cv.drawLine(x0, y0, x0 + L * rx, y0, paint(POCA_CL, 230, "stroke", 4.0 / s))


def cenario(cv, fit, s):
    """Fundo no referencial do mundo. Fita 1: prédios baixos, cerca-viva e poste; fita 2 (OUTRO lugar): árvores e
    um muro baixo com grade. Calçada com juntas, meio-fio e a poça de cada fita."""
    if fit == 1:
        for x, w, h in ((-300, 300, 430), (20, 230, 340), (270, 280, 480), (590, 240, 390), (850, 300, 460),
                        (1170, 280, 370)):
            cv.drawRect(skia.Rect(x, GY - 60 - h, x + w, GY - 60), paint("#163246"))
            for j in range(2):
                for i in range(int(w // 70)):
                    xx = x + 26 + i * 70; yy = GY - 60 - h + 40 + j * 90
                    if yy < GY - 120:
                        lit = (i * 3 + j * 5 + x) % 7 == 0
                        cv.drawRect(skia.Rect(xx, yy, xx + 28, yy + 40), paint("#5E7A86" if lit else "#1E3D52"))
        cv.drawRect(skia.Rect(-1500, GY - 64, 3000, GY), paint("#1E4A47"))          # cerca-viva
        for i in range(-30, 80):
            cv.drawCircle(i * 30.0, GY - 64, 18, paint("#1E4A47"))
        _poste(cv, 1000.0, s)
        _poste(cv, 120.0, s)
    else:
        for x, r in ((90.0, 110.0), (980.0, 130.0)):
            cv.drawRect(skia.Rect(x - 9, GY - 270, x + 9, GY - 40), paint("#2A3A3C"))
            cv.drawCircle(x, GY - 310, r, paint("#1E4A47"))
            cv.drawCircle(x - r * 0.45, GY - 268, r * 0.62, paint("#193F3D"))
        cv.drawRect(skia.Rect(-1500, GY - 120, 3000, GY), paint("#2B4256"))          # muro baixo
        cv.drawRect(skia.Rect(-1500, GY - 128, 3000, GY - 116), paint("#3A5469"))
        gr = skia.Path()
        for i in range(-60, 120):
            gr.moveTo(i * 24.0, GY - 128); gr.lineTo(i * 24.0, GY - 230)
        gr.moveTo(-1500, GY - 222); gr.lineTo(3000, GY - 222)
        cv.drawPath(gr, paint("#203547", 255, "stroke", 4.0))
    cv.drawRect(skia.Rect(-1500, GY, 3000, GY + 700), paint(CALCADA if fit == 1 else "#5B6879"))
    cv.drawRect(skia.Rect(-1500, GY, 3000, GY + 20), paint(CALCADA_CL if fit == 1 else "#67768A"))
    j = skia.Path()
    passo = 190.0 if fit == 1 else 150.0
    for i in range(-10, 24):
        x = i * passo
        j.moveTo(x, GY + 20); j.lineTo(x - 40, GY + 700)
    j.moveTo(-1500, GY + 20); j.lineTo(3000, GY + 20)
    cv.drawPath(j, paint(CALCADA_JUNTA, 255, "stroke", 3.0 / s))
    cv.drawLine(-1500, GY, 3000, GY, paint(MEIO_FIO, 255, "stroke", 4.0 / s))
    _poca(cv, *(POCA1 if fit == 1 else POCA2), s)


def sombra_crianca(cv, p):
    """Sombra no chão sob a criança: some quando ela sobe."""
    pe = max(p["hy"] + p["pp"][1], p["hy"] + p["pl"][1])
    a = clamp(1 - (ANK - pe) / 260)
    x = p["hx"] + 8
    larg = 70 + 30 * a
    cv.drawOval(skia.Rect(x - larg, GY - 7, x + larg, GY + 9), paint("#000000", int(85 * a), blur=6))


# ------------------------------------------------------------------ efeitos de replay (cópias do piloto)
def varredura(cv, t, ambar, limpo=False):
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
    if limpo:
        return

    def dl(c):
        _rel(c)
        lin = skia.Path()
        y = CENA.top() + 2
        while y < CENA.bottom():
            lin.moveTo(CENA.left(), y); lin.lineTo(CENA.right(), y); y += 6
        c.drawPath(lin, paint("#000000", 22, "stroke", 2))
    _blit(cv, _img("linhas", CENA.width(), CENA.height(), dl), CENA.left(), CENA.top())
    rng = np.random.default_rng(int(round(t * FPS)) + 1)
    xs = rng.uniform(CENA.left(), CENA.right(), 340); ys = rng.uniform(CENA.top(), CENA.bottom(), 340)
    pts = [skia.Point(float(a), float(b)) for a, b in zip(xs, ys)]
    cv.drawPoints(skia.Canvas.kPoints_PointMode, pts[:170], paint("#FFFFFF", 30, "stroke", 2.2))
    cv.drawPoints(skia.Canvas.kPoints_PointMode, pts[170:], paint("#000000", 40, "stroke", 2.2))


def faixas_tracking(cv, t, a):
    if a <= 0:
        return
    for i in range(3):
        y = CENA.top() + ((t * 1300 + i * 330) % (CENA.height() + 60)) - 30
        h = 22 + 12 * i
        cv.drawRect(skia.Rect(CENA.left(), y, CENA.right(), y + h), paint("#FFFFFF", int(52 * a)))
        cv.drawRect(skia.Rect(CENA.left(), y + h, CENA.right(), y + h + 4), paint("#000000", int(70 * a)))


def corte_fita(cv, t, t0):
    """Corte de fita: chiado por ~0,2 s — a cena (outra criança, outra poça) muda por baixo dele."""
    k = t - t0
    if not (-0.03 <= k < 0.2):
        return
    a = 1.0 if k < 0.08 else 1 - prog(k, 0.08, 0.2)
    rng = np.random.default_rng(int(round(t * FPS)) + 911)
    img = _img("ruido", CENA.width(), CENA.height(), lambda c: c.clear(_c("#6E7C88", 255)))
    _blit(cv, img, CENA.left(), CENA.top(), 0.55 * a)
    for _ in range(22):
        y = rng.uniform(CENA.top(), CENA.bottom()); h = rng.uniform(4, 34)
        g = int(rng.uniform(40, 235))
        cv.drawRect(skia.Rect(CENA.left(), y, CENA.right(), y + h), paint(f"#{g:02X}{g:02X}{g:02X}", int(170 * a)))
    xs = rng.uniform(CENA.left(), CENA.right(), 1400); ys = rng.uniform(CENA.top(), CENA.bottom(), 1400)
    pts = [skia.Point(float(p), float(q)) for p, q in zip(xs, ys)]
    cv.drawPoints(skia.Canvas.kPoints_PointMode, pts[:700], paint("#FFFFFF", int(200 * a), "stroke", 3.0))
    cv.drawPoints(skia.Canvas.kPoints_PointMode, pts[700:], paint("#000000", int(200 * a), "stroke", 3.0))


def cantoneiras(cv, a):
    if a <= 0:
        return
    r = CENA; L = 60
    pt = paint("#FFFFFF", int(160 * a), "stroke", 5)
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


# ------------------------------------------------------------------ painel do replay (cronômetro + velocidade; cópia do piloto)
def relogio(cv, x, y, r, a, ang):
    """Relógio de ponteiros, sem números. (cópia do cf_andador, via piloto)"""
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
    """◀◀ desenhado (a fonte não tem o símbolo). (cópia do piloto)"""
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


HUD_X, HUD_Y = 786, 1172
# v3 (verificação em resolução cheia, 01/11): em (300, 560) o "0,25×" grande (2,5×, ~440×168 px) ficava PARADO
# sobre a pegada (topo da cabeça, puxinhos, mãos erguidas, mão adulta) e depois voava para o painel atravessando
# rosto, ombro e braço da menina. Na 1ª câmera lenta a criança e a mão adulta ficam em x <= ~565 (mundo à esquerda
# da poça); o selo nasce à DIREITA, no céu/prédios, e o voo até o painel (canto inferior direito) só se afasta dela.
POP_C = (780, 572)                                               # 1ª câmera lenta: à direita, longe da pegada
                                                                 # (e dentro da moldura âmbar, mesmo no pulo)
POP_C2 = (820, 520)                                              # 2ª câmera lenta: à frente do arco


def _chip_hud_c(s):
    _, w, _ = chip_dim(s)
    return HUD_X + 50 + w / 2, HUD_Y


def painel(cv, t, T, F, a):
    if a <= 0:
        return
    tipo = F.tipo(t)
    relogio(cv, HUD_X, HUD_Y, 34, a, F.tf(t) * 2 * math.pi)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(HUD_X - 7, HUD_Y - 50, HUD_X + 7, HUD_Y - 38), 3, 3), paint(OURO, int(255 * a)))
    t0 = F.inicio_trecho(t)
    if tipo == "volta":
        _setas(cv, HUD_X + 52, HUD_Y, a * (0.75 + 0.25 * math.sin(t * 18)), 1.25, False)
        return
    if tipo == "congela":                                          # o rótulo do trecho anterior, apagado
        s = R_LENTA if lento_k(t, T) > 0 else R_1X
        chip_c(cv, s, *_chip_hud_c(s), a, dim=0.4)
        return
    s = R_LENTA if tipo == "lenta" else R_1X
    hx, hy = _chip_hud_c(s)
    k = t - t0
    if tipo == "lenta" and k < 0.75 and t0 in (T["camera"], T["upa2"]):   # "0,25×" grande que voa para o painel
        cx, cy = POP_C if t0 == T["camera"] else POP_C2
        if k < 0.32:
            chip_c(cv, s, cx, cy, a, esc=2.5 * e_back(clamp(k / 0.16)))
        else:
            v = e_inout(prog(k, 0.32, 0.75))
            chip_c(cv, s, lerp(cx, hx, v), lerp(cy, hy, v), a, esc=lerp(2.5, 1.0, v))
        return
    pop = 1 + 0.6 * (1 - e_out(prog(t, t0, t0 + 0.3))) if t0 > 0 and tipo != "lenta" else 1.0
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


def anel(cv, x, y, r, a, t, t0):
    """Anel dourado que pulsa POR FORA da pele. (cópia do cf_cameralenta_osso_crianca)"""
    if a <= 0:
        return
    k = max(0.0, t - t0)
    pul = 1 + 0.10 * math.sin(k * 9) * math.exp(-k * 2.5)
    ent = e_back(clamp(k / 0.28))
    rr = r * pul * max(0.01, ent)
    cv.drawCircle(x, y, rr + 4, paint(OURO, int(90 * a), "stroke", 14, blur=7))
    cv.drawCircle(x, y, rr, paint(FUNDO_CARTAO, int(150 * a), "stroke", 10))
    cv.drawCircle(x, y, rr, paint(OURO, int(255 * a), "stroke", 6))


def estetoscopio(cv, x, y, esc, a):
    """Selo branco e calmo do "leve pra avaliar": estetoscópio desenhado (forma, sem texto). (cópia do piloto)"""
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


# ------------------------------------------------------------------ a lupa esquemática (OPACA; não é exame)
# Fundo no tom da pele (a pele lisa do próprio desenho, ampliada, com as bordas do braço um pouco mais escuras)
# e, no centro, UMA faixa marfim deitada sobre a marca tracejada dourada do "lugar" dela. Sem osso, sem anel,
# sem nome, sem fundo escuro, sem brilho de raio-X. No "escorrega" a faixa desliza devagar para fora da marca e
# FICA ali (nunca volta). A lupa fecha antes do pouso.
LUPA_C, LUPA_R = (856.0, 560.0), 172.0
DESLIZE = 62.0


def _cinta_path(larg, R):
    """A CINTA (v2, revisor: a cápsula curta lia como comprimido): faixa LONGA e levemente curva que atravessa a
    lupa inteira (as pontas saem pela borda), no eixo y do referencial da lupa (x = ao longo do braço)."""
    p = skia.Path()
    n = 24
    pts = []
    for i in range(n + 1):
        y = -R + 2 * R * i / n
        pts.append((9.0 * (y / R) ** 2, y))
    for i, (x, y) in enumerate(pts):
        (p.moveTo if i == 0 else p.lineTo)(x - larg / 2, y)
    for x, y in reversed(pts):
        p.lineTo(x + larg / 2, y)
    p.close()
    return p


def _cinta(cv, R, a=1.0, fibras=True):
    larg = 40.0
    pth = _cinta_path(larg, R)
    if a < 1.0:
        camada(cv, a)
    cv.drawPath(pth, paint("#000000", 55, blur=6))
    sh = skia.GradientShader.MakeLinear([skia.Point(-larg / 2, 0), skia.Point(larg / 2, 0)],
                                        [_c("#E3D3B6"), _c(MARFIM), _c(MARFIM_CL), _c(MARFIM), _c("#DCCAA8")],
                                        [0.0, 0.25, 0.5, 0.75, 1.0])
    cv.drawPath(pth, paint(MARFIM, 255, shader=sh))
    if fibras:                                                      # fibras ao longo da cinta (tecido, não comprimido)
        cv.save(); cv.clipPath(pth, skia.ClipOp.kIntersect, True)
        for dx in (-12.0, -4.0, 4.0, 12.0):
            f = skia.Path()
            for i in range(25):
                y = -R + 2 * R * i / 24
                (f.moveTo if i == 0 else f.lineTo)(9.0 * (y / R) ** 2 + dx + 1.6 * math.sin(y * 0.09 + dx), y)
            cv.drawPath(f, paint(MARFIM_LINHA, 120, "stroke", 2.0))
        cv.restore()
    cv.drawPath(pth, paint(MARFIM_LINHA, 255, "stroke", 3.2))
    if a < 1.0:
        cv.restore()


def lupa(cv, t, T, base_xy, ang):
    """Lupa ESQUEMÁTICA opaca (não é exame): pele lisa ampliada, a CINTA marfim atravessando o braço e, por baixo,
    o "lugar" dela em tracejado BRANCO. No "escorrega" a cinta desliza para o lado do ombro deixando um ECO (2
    fantasmas esmaecidos) que continua no quadro parado — a faixa fora da marca se lê sem o movimento — e uma seta
    branca curta. Ela NUNCA volta. A lupa abre no "que um ligamento" e fecha (encolhendo no lugar, sem ir para cima
    do cotovelo) antes de o pé tocar o chão."""
    abre = e_out(prog(t, T["ligamento"] - 0.3, T["ligamento"]))
    t_fecha = t_descongela(T)
    fecha = e_inout(prog(t, t_fecha, t_fecha + 0.28))
    k = abre * (1 - fecha)
    if k <= 0.01:
        return
    m = abre                                                       # abre saindo do cotovelo; fecha no lugar
    cx, cy = lerp(base_xy[0], LUPA_C[0], m), lerp(base_xy[1], LUPA_C[1], m)
    r = LUPA_R * k
    # fio curto até o cotovelo
    dx, dy = base_xy[0] - cx, base_xy[1] - cy; d = math.hypot(dx, dy) or 1.0
    x0, y0 = cx + dx / d * r, cy + dy / d * r
    if d > r + 4:
        cv.drawLine(x0, y0, base_xy[0], base_xy[1], paint("#000000", int(110 * k), "stroke", 9, blur=3))
        cv.drawLine(x0, y0, base_xy[0], base_xy[1], paint("#FFFFFF", int(235 * k), "stroke", 4))
    cv.drawCircle(cx, cy, r + 14, paint("#000000", int(110 * k), blur=14))
    camada(cv, 1 - fecha)                                          # v2: fecha encolhendo E esmaecendo
    cv.save()
    clip = skia.Path(); clip.addCircle(cx, cy, r)
    cv.clipPath(clip, skia.ClipOp.kIntersect, True)
    cv.translate(cx, cy); cv.scale(max(k, 0.01), max(k, 0.01)); cv.rotate(ang)
    R = LUPA_R + 6
    sh = skia.GradientShader.MakeLinear([skia.Point(0, -R), skia.Point(0, R)],
                                        [_c(PELE_ESC), _c(PELE), _c(PELE_CL), _c(PELE), _c(PELE_ESC)],
                                        [0.0, 0.2, 0.5, 0.8, 1.0])
    cv.drawRect(skia.Rect(-R, -R, R, R), paint(PELE, 255, shader=sh))
    cv.drawLine(-R, -R * 0.55, R, -R * 0.55, paint(PELE_CL, 120, "stroke", 16))       # brilho largo da pele
    # o LUGAR da cinta: sulco levemente mais escuro + tracejado BRANCO de alto contraste
    a_m = prog(t, T["ligamento"] - 0.15, T["ligamento"] + 0.1)
    lugar = _cinta_path(52.0, R + 20)
    cv.drawPath(lugar, paint(PELE_ESC, int(150 * a_m)))
    cv.drawPath(lugar, paint(FUNDO_CARTAO, int(120 * a_m), "stroke", 8))
    pm = paint("#FFFFFF", int(255 * a_m), "stroke", 4.5)
    pm.setPathEffect(skia.DashPathEffect.Make([14.0, 9.0], 0.0))
    cv.drawPath(lugar, pm)
    entra = e_out(prog(t, T["ligamento"] - 0.2, T["ligamento"] + 0.12))
    v = e_inout(prog(t, T["escorrega"], T["escorrega"] + 0.42))    # desliza e PARA (nunca volta)
    desl = DESLIZE * v
    if entra > 0:
        for fr, al in ((0.35, 0.28), (0.68, 0.42)):                # o ECO: fica no quadro parado
            if v >= fr:
                cv.save(); cv.translate(-DESLIZE * fr, 0)
                _cinta(cv, R, al, fibras=False)
                cv.restore()
        cv.save(); cv.translate(-desl, 0); cv.scale(1.0, entra)
        brilho = math.exp(-((t - T["ligamento"] - 0.15) / 0.18) ** 2)       # acende no "ligamento"
        if brilho > 0.02:
            cv.drawPath(_cinta_path(40.0, R), paint("#FFFFFF", int(170 * brilho), "stroke", 14, blur=8))
        _cinta(cv, R)
        cv.restore()
        a_s = prog(t, T["escorrega"] + 0.1, T["escorrega"] + 0.3)  # seta branca do deslize (para o lado do ombro)
        if a_s > 0:
            yb = R * 0.58
            seta(cv, 34.0, yb, 34.0 - 30.0 - 60.0 * v, yb, "#FFFFFF", a_s, larg=8, tam=28)
    cv.restore()
    cv.drawCircle(cx, cy, r, paint("#FFFFFF", int(255 * k), "stroke", 6))
    cv.drawArc(skia.Rect(cx - r * 0.78, cy - r * 0.78, cx + r * 0.78, cy + r * 0.78), 200, 50, False,
               paint("#FFFFFF", int(120 * k), "stroke", 6))
    cv.restore()


# ------------------------------------------------------------------ "não puxe nem force": a mão adulta PARA longe do braço e recua
def mao_aberta(cv, x, y, ang, esc, abre, a, manga):
    """Antebraço com manga + mão que se abre (palma para quem vê, dedos afastados): o gesto de "pare"."""
    if a <= 0:
        return
    camada(cv, a)
    cv.translate(x, y); cv.rotate(ang); cv.scale(esc, esc)
    cv.saveLayer(None, None)
    ante = rr_path(20, -42, 380, 42, 40)
    _pele(cv, ante, (0, -42), (0, 42), 1.0, tons=TONS_AD, cor_linha=AD_LINHA)
    mg = rr_path(170, -56, 1600, 56, 18)
    _pele(cv, mg, (0, -56), (0, 56), 1.0, tons=manga["tons"], cor_linha=manga["linha"])
    cv.drawRect(skia.Rect(170, -54, 200, 54), paint(manga["punho"], 235))
    cv.restore()
    cv.save(); cv.translate(-18, -40); cv.rotate(lerp(8.0, 14.0, abre))           # v2: polegar JUNTO aos dedos
    pol = rr_path(-70, -14, 0, 14, 14)
    _pele(cv, pol, (0, -14), (0, 14), 1.0, tons=TONS_AD, cor_linha=AD_LINHA, linha=2.6)
    cv.restore()
    for i in range(4):                                             # quatro dedos (para -x), afastados ao abrir
        yy = (i - 1.5) * lerp(25.0, 31.0, abre)
        g = (i - 1.5) * lerp(2.0, 9.0, abre)
        L = lerp(70.0, 100.0 - 9 * abs(i - 1.5), abre)
        cv.save(); cv.translate(-46, yy * 0.8); cv.rotate(g)
        d = rr_path(-L, -13, 6, 13, 13)
        _pele(cv, d, (0, -13), (0, 13), 1.0, tons=TONS_AD, cor_linha=AD_LINHA, linha=2.6)
        cv.restore()
    palma = rr_path(-70, -60, 40, 60, 44)
    _pele(cv, palma, (0, -60), (0, 60), 1.0, tons=TONS_AD, cor_linha=AD_LINHA)
    cv.restore()


def estado_nao_puxe(t, T):
    """-> (avanço 0..1, abre 0..1, alfa). A mão vem pelo alto, PARA a ~120 px do braço, abre a palma e sobe
    de volta esmaecendo. Nunca encosta."""
    vem = e_out(prog(t, T["nao2"] - 0.15, T["nao2"] + 0.42))
    abre = e_back(prog(t, T["nao2"] + 0.30, T["nao2"] + 0.60))
    vai = e_inout(prog(t, T["force"], T["leve"]))                  # v2: o recuo começa já no "force"
    a = prog(t, T["nao2"] - 0.15, T["nao2"] + 0.05) * (1 - prog(t, T["force"] + 0.2, T["leve"] + 0.1))
    return vem * (1 - vai), abre, a


def ponto_nao_puxe(p, J):
    """Onde a mão adulta para: à frente e acima do braço parado, ~200 px dele (mundo; v2, revisor)."""
    om = no_mundo(p, J["omb_p"]); pu = no_mundo(p, J["pun_p"])
    meio = ((om[0] + pu[0]) / 2, (om[1] + pu[1]) / 2)
    return meio[0] + 262.0, meio[1] - 70.0


# ------------------------------------------------------------------ o mundo (dentro do monitor)
OBTURADOR = {"play": 0.085, "volta": 0.13}                       # s de VÍDEO (na volta, ~0,35 s de filme)
# v4 (2ª rodada da verificação em resolução cheia, 01/11): o borrão era a MÉDIA de 5 cópias (8 na volta) da criança
# inteira, cada uma com contorno, espalhadas pelos 0,085 s do obturador. No 1× o pulo anda ~3.000 px/s: as cópias
# ficavam a 30-70 px uma da outra e liam como crianças SEPARADAS e nítidas (0,600 s: duas cabeças, dois coques, duas
# camisas; 0,667 s: o braço que cai em três degraus com todos os dedos; o mesmo na volta e nas mãos adultas do 2º
# lance). Agora: a pose ATUAL é desenhada inteira e opaca por cima, e atrás dela fica um RASTRO CONTÍNUO — amostras
# tão próximas que nenhuma parte anda mais de PASSO_RASTRO px de tela entre duas vizinhas (os contornos de ~3 px se
# fundem num véu), MÉDIA PONDERADA de verdade (soma em float, ver `rastro`) no TEMPO, a ponta mais velha some (peso
# (1 - idade)^QUEDA_RASTRO), vezes ALFA_RASTRO.
# Onde nada se mexe o rastro fica embaixo da pose atual: ele só aparece nas partes que se movem.
PASSO_RASTRO = 2.5                                               # px de tela entre amostras vizinhas (parte mais rápida)
N_RASTRO_MAX = 44                                                # teto de amostras; acima dele o rastro encurta (no tempo)
ALFA_RASTRO = 0.60                                               # opacidade do rastro logo atrás da pose atual
QUEDA_RASTRO = 1.0                                               # peso = (1 - idade)^QUEDA: a ponta mais velha some
JUNTAS_RASTRO = ("cab", "pesc", "omb_p", "omb_l", "cot_p", "pun_p", "cot_l", "pun_l", "joe_p", "tor_p", "joe_l",
                 "tor_l")
ANG_NP = -58.0                                                   # direção da mão aberta do "não puxe nem force"


def _mao_np(tg, T, p, J):
    """"Não puxe nem force": (x, y, abre, alfa) da mão adulta aberta (mundo) no instante de vídeo tg."""
    vem, abre, a = estado_nao_puxe(tg, T)
    px, py = ponto_nao_puxe(p, J)
    u = (math.cos(math.radians(ANG_NP)), math.sin(math.radians(ANG_NP)))
    dist = 520.0 * (1 - vem)
    return px + u[0] * dist, py + u[1] * dist, abre, a


# v5 (3ª rodada, 01/11): a mão de trás (escura) e o braço dela eram desenhados inteiros, 12 px acima e ~30 px à frente
# da mão de cá: atrás das costas o braço dela virava um 2º contorno paralelo ao da frente, e na chegada (~22,5-22,85 s)
# e na saída (~26,8-27,15 s), com as duas mãos no ar, longe da criança, liam como UMA mão com dois polegares e ~8
# dedos. De perfil, com o adulto atrás da criança, o braço de lá fica escondido pelo de cá; então a mão de trás só é
# desenhada DENTRO do meio-plano que começa a X_CORTE_COSTAS das costas (no referencial do tronco, que gira com ela):
# ali o tronco a cobre e só as pontas dos dedos aparecem à frente do peito. Fora da criança ela não existe.
X_CORTE_COSTAS = -30.0                                           # o contorno das costas fica em x ~ -43 nessa altura


def atras_do_tronco(p):
    """Meio-plano x > X_CORTE_COSTAS no referencial do tronco (girado de p["tor"]), em coordenadas do mundo."""
    G = 6000.0
    cs = [(X_CORTE_COSTAS, -G), (G, -G), (G, G), (X_CORTE_COSTAS, G)]
    return _poli([no_mundo(p, rot(q, p["tor"])) for q in cs])


def _maos_axila(R, f, p):
    """2º lance: (alfa, palma do lado de cá, palma do outro lado) das mãos adultas (mundo) no tempo de filme f."""
    chega, sai = R.maos(f)
    a_m = clamp(chega * 3) * (1 - prog(sai, 0.75, 1.0))
    # v2: as mãos chegam e saem PELA HORIZONTAL, por trás (ao longo do antebraço), nunca por cima da cabeça
    u = _dir(ANG_ANTE)
    off = 420.0 * (1 - chega) + 700.0 * sai
    P = axila_mundo(p); Pf = axila_mundo(p, AXILA_L)
    return a_m, (P[0] + u[0] * off, P[1] + u[1] * off), (Pf[0] + u[0] * off, Pf[1] + u[1] * off)


def _pontos_ator(tg, T, F):
    """Pontos (mundo) que resumem o movimento do que `ator` desenha em tg — juntas, topo da cabeça, palmas, bicos
    dos tênis e as mãos adultas (None = invisível). Lista de tamanho fixo (compara instantes ponto a ponto)."""
    f = F.tf(tg)
    if fita(tg, T) == 1:
        p, A, a_ad, _, ang = F.R1.pose(f)
        J = _joints(p)
        x, y, _, a = _mao_np(tg, T, p, J)
        extra = [A if a_ad > 0 else None, _pt(A, _dir(ang), 160.0) if a_ad > 0 else None,
                 (x, y) if a > 0 else None]
    else:
        p = F.R2.pose(f)
        J = _joints(p)
        a_m, Pn, Pl = _maos_axila(F.R2, f, p)
        u = _dir(ANG_ANTE)
        extra = [Pn, Pl, _pt(Pn, u, L_ANTE), _pt(Pl, u, L_ANTE)] if a_m > 0 else [None] * 4
    pts = [no_mundo(p, J[k]) for k in JUNTAS_RASTRO]
    pts += [no_mundo(p, centro_palma(J, lado)) for lado in ("p", "l")]
    topo = rot((-30.0, -58.0), p["tor"] + p["cab"])
    pts.append(no_mundo(p, (J["cab"][0] + topo[0], J["cab"][1] + topo[1])))
    for lado, ang_t in (("p", p["ppa"]), ("l", p["pla"])):
        bico = rot((58.0, 16.0), ang_t)
        pts.append(no_mundo(p, (J["tor_" + lado][0] + bico[0], J["tor_" + lado][1] + bico[1])))
    return pts + extra


def amostras_borrao(t, F, T, s=1.0):
    """Instantes do rastro do 1× e da volta, do mais novo (t) ao mais velho, com o peso de cada um no tempo:
    [(tg, dt)]. Nunca antes de t = 0, nunca atravessando congelamento nem o corte de fita (a janela não sai do
    trecho de t). v4: a janela é varrida em K pedaços; cada pedaço recebe amostras até que a parte mais rápida ande
    no máximo PASSO_RASTRO px de tela entre duas vizinhas; acima de N_RASTRO_MAX o rastro perde a ponta mais velha."""
    obt = OBTURADOR.get(F.tipo(t))
    if not obt:
        return [(t, 0.0)]
    seg = F.seg(t)
    t_ini = max(t - obt, seg[0], 0.0)
    if t - t_ini < 1e-3:
        return [(t, 0.0)]
    K = 12
    ts = [t - (t - t_ini) * i / K for i in range(K + 1)]
    pts = [_pontos_ator(x, T, F) for x in ts]
    cortes = []                                                    # (início, fim, nº de subdivisões) do novo ao velho
    total = 0
    for i in range(K):
        d = 0.0
        for a, b in zip(pts[i], pts[i + 1]):
            if a is not None and b is not None:
                d = max(d, math.hypot(a[0] - b[0], a[1] - b[1]))
        m = int(math.ceil(d * s / PASSO_RASTRO))
        if m == 0:
            m = 1 if d * s > 0.05 else 0
        if total + m > N_RASTRO_MAX - 1:                           # estoura o teto: corta o pedaço e para
            resto = N_RASTRO_MAX - 1 - total
            if resto > 0:
                cortes.append((ts[i], ts[i] - (ts[i] - ts[i + 1]) * resto / m, resto))
            break
        cortes.append((ts[i], ts[i + 1], m))
        total += m
    tempos = [t]
    for a, b, m in cortes:
        if m == 0:                                                 # nada se mexe neste pedaço: uma amostra só
            tempos.append(b)
            continue
        for j in range(1, m + 1):
            tempos.append(a - (a - b) * j / m)
    if len(tempos) < 3 or all(m == 0 for _, _, m in cortes):
        return [(t, 0.0)]
    out = []
    for i, x in enumerate(tempos):                                 # peso no tempo (trapézio)
        x0 = tempos[i - 1] if i > 0 else x
        x1 = tempos[i + 1] if i + 1 < len(tempos) else x
        out.append((x, (x0 - x1) / 2))
    return out


def ator(cv, tg, T, F, sombra=True):
    """Desenha a criança (e as mãos adultas) no instante de vídeo `tg`. -> (pose, juntas)."""
    f = F.tf(tg)
    if fita(tg, T) == 1:
        p, A, a_ad, segura, ang = F.R1.pose(f)
        if sombra:
            sombra_crianca(cv, p)
        cbs = {}
        if a_ad > 0:
            cbs["frente"] = lambda J: adulto_tras(cv, A, ang, MANGA1, a_ad)
            if segura > 0.5:
                cbs["fim"] = lambda J: adulto_frente(cv, A, ang, a_ad)
        J = crianca(cv, p, ROUPA1, cbs)
        x, y, abre, a = _mao_np(tg, T, p, J)                       # "não puxe nem force"
        if a > 0:
            mao_aberta(cv, x, y, ANG_NP, 0.60, abre, a, MANGA1)
        return p, J
    R = F.R2
    p = R.pose(f)
    if sombra:
        sombra_crianca(cv, p)
    a_m, Pn, Pl = _maos_axila(R, f, p)
    cbs = {}
    if a_m > 0:
        def atras(J):                                              # a mão do outro lado (atrás do tronco): só
            cv.save()                                              # as pontas dos dedos passam da frente do peito
            cv.clipPath(atras_do_tronco(p), skia.ClipOp.kIntersect, True)     # v5: nada dela fora do tronco
            braco_adulto(cv, Pl, MANGA1, a_m, escuro=0.35)
            mao_axila(cv, Pl, a_m, escuro=0.35)
            cv.restore()

        def meio(J):                                               # a mão do lado de cá: por cima do tronco e
            braco_adulto(cv, Pn, MANGA1, a_m)                      # POR BAIXO do braço solto da criança
            mao_axila(cv, Pn, a_m)

        cbs["atras"] = atras
        cbs["meio"] = meio
    J = crianca(cv, p, ROUPA2, cbs)
    return p, J


_RASTRO_BUF = {}


def _buffers_rastro(w, h):
    if (w, h) not in _RASTRO_BUF:
        info = skia.ImageInfo.MakeN32Premul(w, h)                  # N32 (BGRA aqui): o blit de volta é direto
        _RASTRO_BUF[(w, h)] = (info, skia.Surface.MakeRaster(info), np.empty((h, w, 4), np.uint8),
                               np.zeros((h, w, 4), np.float32), np.empty((h, w, 4), np.float32))
    return _RASTRO_BUF[(w, h)]


def rastro(cv, t, ams, T, F):
    """O rastro: MÉDIA PONDERADA de verdade (soma em float, pixel a pixel) das amostras passadas, cada uma desenhada
    sozinha numa superfície do tamanho da cena e somada com o seu peso (tempo × (1 - idade)^QUEDA_RASTRO), vezes
    ALFA_RASTRO, e posta na cena por baixo da pose atual. (A média "incremental" por camadas com alfa 1/(k+1) só é
    média onde TODAS as amostras cobrem o pixel: onde só uma amostra velha cobre, nada a atenua e ela fica OPACA — por
    isso as cópias do borrão antigo saíam inteiras e nítidas. Camadas F16 com soma resolveriam, mas nesta build do
    skia custam ~120 ms cada.) Sem sombra no chão: a sombra é só a da pose atual."""
    idade = t - ams[-1][0]
    pesos = [(tg, (1.0 - (t - tg) / idade) ** QUEDA_RASTRO * dt) for tg, dt in ams[1:]]
    pesos = [(tg, w) for tg, w in pesos if w > 1e-9]
    W = sum(w for _, w in pesos)
    if W <= 0:
        return
    x0, y0, w, h = int(CENA.left()), int(CENA.top()), int(CENA.width()), int(CENA.height())
    info, surf, buf, acc, tmp = _buffers_rastro(w, h)
    m = cv.getTotalMatrix()
    c = surf.getCanvas()
    l0, l1, c0, c1 = h, 0, w, 0
    for tg, wt in pesos:
        c.clear(skia.ColorTRANSPARENT)
        c.save(); c.translate(-x0, -y0); c.concat(m)
        ator(c, tg, T, F, sombra=False)
        c.restore()
        surf.readPixels(info, buf, w * 4, 0, 0)
        al = buf[:, :, 3]
        ls = np.flatnonzero(al.any(axis=1))
        if ls.size == 0:
            continue
        cs = np.flatnonzero(al.any(axis=0))
        a0, a1, b0, b1 = int(ls[0]), int(ls[-1]) + 1, int(cs[0]), int(cs[-1]) + 1
        l0, l1, c0, c1 = min(l0, a0), max(l1, a1), min(c0, b0), max(c1, b1)
        np.multiply(buf[a0:a1, b0:b1], np.float32(wt / W * ALFA_RASTRO), out=tmp[a0:a1, b0:b1], dtype=np.float32)
        np.add(acc[a0:a1, b0:b1], tmp[a0:a1, b0:b1], out=acc[a0:a1, b0:b1])
    if l1 <= l0:
        return
    reg = np.ascontiguousarray(np.clip(np.rint(acc[l0:l1, c0:c1]), 0, 255).astype(np.uint8))
    acc[l0:l1, c0:c1] = 0.0                                        # o acumulador volta zerado para o próximo quadro
    img = skia.Image.fromarray(reg, colorType=info.colorType(), alphaType=skia.AlphaType.kPremul_AlphaType)
    cv.save(); cv.resetMatrix()
    cv.drawImage(img, x0 + c0, y0 + l0)
    cv.restore()


def ator_borrado(cv, t, T, F, s=1.0):
    """v4: rastro contínuo ATRÁS da pose atual (ver PASSO_RASTRO e `rastro`); a pose atual vem por cima, inteira e
    opaca — uma criança só, nunca cópias soltas."""
    ams = amostras_borrao(t, F, T, s)
    if len(ams) >= 3:
        rastro(cv, t, ams, T, F)
    return ator(cv, t, T, F)


def monitor(cv, t, T, F, passos):
    tipo = F.tipo(t)
    cam = camera(t, passos)
    if tipo == "volta":
        j = math.sin(t * 97) * 4 + math.sin(t * 41) * 3
        cam = (cam[0], cam[1], cam[2], cam[3] + j, cam[4])
    if 0 <= t - T["corte"] < 0.18:                                  # salto de quadro no corte
        j = 40 * math.sin((t - T["corte"]) * 140) * (1 - (t - T["corte"]) / 0.18)
        cam = (cam[0], cam[1], cam[2], cam[3] + j, cam[4] - j * 0.3)
    s = cam[0]
    fit = fita(t, T)
    cv.save(); cv.clipRect(CENA, True)
    monitor_fundo(cv)
    cv.save(); aplica(cv, cam)
    cenario(cv, fit, s)
    if tipo in OBTURADOR:
        p, J = ator_borrado(cv, t, T, F, s)
    else:
        p, J = ator(cv, t, T, F)
    cv.restore()

    def tela(pt_local):
        return na_tela(cam, *no_mundo(p, pt_local))

    if fit == 1:
        marcas_lance1(cv, t, T, F, p, J, tela, s)
    else:
        marcas_lance2(cv, t, T, F, p, J, tela, s)
    # "leve pra avaliar": selo calmo com o estetoscópio (sem check, sem selo de resolvido)
    a_e = prog(t, T["leve"], T["leve"] + 0.2) * (1 - prog(t, T["corte"] - 0.3, T["corte"] - 0.05))
    if a_e > 0:
        pul = 1.0
        for chave in ("avaliar", "ortopedista", "rapida"):          # v2: um pulso calmo em cada palavra
            pul += 0.09 * math.sin(math.pi * prog(t, T[chave], T[chave] + 0.45))
        estetoscopio(cv, 900, 450, 1.35 * e_back(prog(t, T["leve"], T["leve"] + 0.3)) * pul, a_e)

    varredura(cv, t, lento_k(t, T))
    faixas_tracking(cv, t, 1.4 if tipo == "volta" else 0.0)
    if tipo == "volta":
        t0 = F.inicio_trecho(t)
        _setas(cv, 96, 410, (0.55 + 0.45 * (math.sin((t - t0) * 16) > -0.3)) * prog(t, t0, t0 + 0.06), 2.2, False)
    for t0, fo in ((T["repara"], 1.0), (T["corpo"], 0.8)):
        flash(cv, t, t0, fo)
    corte_fita(cv, t, T["corte"])
    cv.restore()
    return cam, p, J


NAMAO_XY, NOCOT_XY = (150.0, 420.0), (690.0, 800.0)


def marcas_lance1(cv, t, T, F, p, J, tela, s):
    """Marcações do comentarista no 1º lance (só na câmera lenta; nada sobre o cotovelo no 1× nem depois do
    pouso)."""
    mao_xy = tela(centro_palma(J))
    cot_xy = tela(J["cot_p"])
    sai_cong = 1 - prog(t, t_descongela(T), t_descongela(T) + 0.3)
    # "o puxão é NA MÃO": círculo nas mãos dadas
    a_c = prog(t, T["mao2"], T["mao2"] + 0.05) * (1 - prog(t, T["cotovelo"] - 0.05, T["cotovelo"] + 0.25))
    if a_c > 0:
        circulo_mao(cv, mao_xy[0] + 4, mao_xy[1] - 4, 72, 62, prog(t, T["mao2"] + 0.02, T["mao2"] + 0.37), a_c)
    a_nm = prog(t, T["mao2"] + 0.05, T["mao2"] + 0.25) * lerp(1.0, 0.4, prog(t, T["cotovelo"], T["cotovelo"] + 0.25)) * sai_cong
    etiqueta_fio(cv, R_NAMAO, NAMAO_XY[0], NAMAO_XY[1], mao_xy[0] - 70, mao_xy[1] - 24, OURO, a_nm, tam=40)
    # "mas é NO COTOVELO": anel por fora da pele + etiqueta
    a_r = prog(t, T["cotovelo"], T["cotovelo"] + 0.08) * sai_cong
    if a_r > 0:
        anel(cv, cot_xy[0], cot_xy[1], 30 * s, a_r, t, T["cotovelo"])
    a_nc = prog(t, T["cotovelo"] + 0.05, T["cotovelo"] + 0.25) * sai_cong
    etiqueta_fio(cv, R_NOCOT, NOCOT_XY[0], NOCOT_XY[1], cot_xy[0] + 30 * s, cot_xy[1] + 18 * s, OURO, a_nc, tam=40)
    # a lupa (abre no "ligamento", fecha no "pousou")
    if T["ligamento"] - 0.35 <= t < t_descongela(T) + 0.35:
        om, pu = tela(J["omb_p"]), tela(J["pun_p"])
        ang = math.degrees(math.atan2(pu[1] - om[1], pu[0] - om[0]))
        lupa(cv, t, T, cot_xy, ang)
    # congelou no "corpo": círculo largo em volta do braço inteiro, afastado da pele
    a_b = prog(t, T["corpo"], T["corpo"] + 0.05) * (1 - prog(t, T["e3"] - 0.25, T["e3"] - 0.02))
    if a_b > 0:
        om, pu = tela(J["omb_p"]), tela(centro_palma(J))
        circulo_mao(cv, (om[0] + pu[0]) / 2 + 8, (om[1] + pu[1]) / 2, 86 * s / 1.3, 150 * s / 1.3,
                    prog(t, T["corpo"] + 0.04, T["corpo"] + 0.42), a_b)
    # "e não quer mexer": seta tracejada sai da mãozinha, avança até a metade e VOLTA (quique)
    a_s = prog(t, T["nao1"] - 0.05, T["nao1"] + 0.1) * (1 - prog(t, T["e3"] - 0.25, T["e3"] - 0.02))
    if a_s > 0:
        hx, hy = tela(centro_palma(J))
        k = t - T["nao1"]
        ida = e_out(clamp(k / 0.3)); volta = 0.55 * sstep((k - 0.3) / 0.25)
        L = 120 * s / 1.3 * (ida - volta)
        ang = math.radians(-38)
        x0, y0 = hx + 36 * s / 1.3, hy - 6
        x1, y1 = x0 + L * math.cos(ang), y0 + L * math.sin(ang)
        if L > 6:
            pt = paint("#FFFFFF", int(255 * a_s), "stroke", 6); pt.setPathEffect(skia.DashPathEffect.Make([16, 10], -t * 40))
            cv.drawLine(x0, y0, x1, y1, pt)
            ponta(cv, x1 + 8 * math.cos(ang), y1 + 8 * math.sin(ang), ang, 24, "#FFFFFF", a_s)
    # "não puxe nem force": a etiqueta saiu daqui (v3) — ver etiqueta_nao_puxe, desenhada FORA do monitor


# v3 (verificação em resolução cheia, 01/11): dentro da cena (linha de base y = 432, caixa y ~388-446) a etiqueta
# ficava sobre os puxinhos da menina (topo da cabeça em y ~420 com o push-in de 1,40× no braço parado): a cabeça
# parecia cortada pelo texto. Nenhum vão da cena comporta a etiqueta inteira (~490-525 px) sem encostar na cabeça
# ou no caminho da mão adulta, então ela sobe para FORA do monitor, no espaço do selo/gancho, que no 1× está vazio
# (o selo CÂMERA LENTA só existe com a lentidão ligada; o gancho sai no "volta"). Caixa em y ~246-304 (até ~244-307
# no pulo de 1,08×), 23 px acima da borda da cena (y = 330): não cobre nada da criança nem da mão.
PUXE_XY = (540.0, 290.0)                                         # centro x e linha de base do texto


def etiqueta_nao_puxe(cv, t, T):
    """"Não puxe nem force": etiqueta (borda azul-clara; sem X, sem vermelho) acima do monitor."""
    a_np = prog(t, T["nao2"], T["nao2"] + 0.2) * (1 - prog(t, T["leve"] - 0.2, T["leve"]))
    chip_txt(cv, R_PUXE, PUXE_XY[0], PUXE_XY[1], "#FFFFFF", a_np, tam=42, borda=AZUL_CL,
             esc=lerp(1.08, 1.0, e_out(prog(t, T["nao2"], T["nao2"] + 0.3))))


# v3 (verificação em resolução cheia, 01/11): em (854, 516) o inset ficava no caminho do arco — de ~25,9 s ao fim
# a criança, pousando à direita, passava POR BAIXO dele e ficava sem cabeça. Agora o inset mora no canto INFERIOR
# ESQUERDO, num vão que ninguém atravessa enquanto ele existe: a criança já saiu dali (topo do arco em diante), o
# braço adulto passa ACIMA (cotovelo em y < ~610) e a etiqueta "PELAS AXILAS" fica embaixo, com o fio saindo da
# ponta direita dela (x >= ~370) para cima e para a direita. Caixa 280 px (era 320) para caber nesse vão, com a
# borda esquerda alinhada à da etiqueta (x = 70) e longe da moldura âmbar; o desenho de dentro é escalado junto
# (ICONE_ESC e os deslocamentos foram pensados para 320 px).
ICONE_C = (210.0, 858.0)                                         # caixa x 70-350, y 718-998
ICONE_H, ICONE_ESC = 280.0, 0.46
ICONE_REF = 320.0                                                # tamanho da caixa para o qual o desenho foi feito


def marcas_lance2(cv, t, T, F, p, J, tela, s):
    fim = 1 - prog(t, T["pulsos_fim"] - 0.1, T["pulsos_fim"] + 0.35)
    ax = na_tela_axila(p, tela)
    a_c = prog(t, T["axilas"], T["axilas"] + 0.05) * fim
    if a_c > 0:
        circulo_mao(cv, ax[0] - 6, ax[1] + 4, 82 * s, 70 * s, prog(t, T["axilas"] + 0.02, T["axilas"] + 0.38), a_c)
    a_l = prog(t, T["axilas"] + 0.05, T["axilas"] + 0.25) * fim
    etiqueta_fio(cv, R_AXI, 70, 1080, ax[0] - 30 * s, ax[1] + 64 * s, OURO, a_l, tam=40)
    # "Não pelas mãos ou pulsos": ícone CINZA no canto (mão adulta puxando a mãozinha pelo alto) + X BRANCO
    k = prog(t, T["nao3"] - 0.1, T["nao3"] + 0.25)
    a_i = clamp(k * 2) * fim
    if a_i > 0:
        x, y = ICONE_C
        H2 = ICONE_H / 2                                            # v2 (revisor): caixa MAIOR
        ke = ICONE_H / ICONE_REF                                    # v3: desenho escalado com a caixa
        rr = skia.RRect.MakeRectXY(skia.Rect(x - H2, y - H2, x + H2, y + H2), 24 * ke, 24 * ke)
        cv.drawRRect(rr, paint(FUNDO_CARTAO, int(248 * a_i)))
        cv.drawRRect(rr, paint(CINZA, int(220 * a_i), "stroke", 3.5))
        cv.save(); cv.clipRRect(rr, True)
        icone_desenho(cv, x - 34 * ke, y - H2 + 88 * ke, 0, ICONE_ESC * ke * lerp(0.92, 1.0, e_out(k)), a_i, cinza=1.0)
        cv.restore()
        xis_branco(cv, x, y + 4 * ke, H2 * 0.62, e_out(prog(t, T["nao3"] + 0.2, T["nao3"] + 0.55)), a_i)


def na_tela_axila(p, tela):
    o = rot(AXILA, p["tor"])
    return tela(o)


# ------------------------------------------------------------------ quadro
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


def quadro(cv, t, T, blocos, ep, F, passos):
    fundo_cl(cv, t)
    monitor(cv, t, T, F, passos)
    etiqueta_nao_puxe(cv, t, T)                                    # v3: fora do monitor (não cobre a cabeça)
    fim = 1 - prog(t, T["manda"] - 0.4, T["manda"] - 0.1)
    cantoneiras(cv, fim)
    painel(cv, t, T, F, fim)
    capa(cv, t, T["volta"], ep["gancho"][0], ep["gancho"][1])
    selo_lenta(cv, lento_k(t, T) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface(cv, t, T, blocos, DESTAQUE)


# ------------------------------------------------------------------ som (mix próprio: som.py fica intacto; cópias do piloto)
def trilha_partes(dur, bpm=100):
    """A MESMA trilha de som.trilha, separada em (harmonia: pad + baixo, batida: kick + hat)."""
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


def chiado(dur=0.26):
    """(cópia do piloto) Corte de fita: estalo de fita + chiado branco curto."""
    SR = som.SR
    n = int(dur * SR); t = np.arange(n) / SR
    rui = som._noise(n, 79); rui = rui - np.convolve(rui, np.ones(4) / 4, "same")
    env = np.clip(t / 0.005, 0, 1) * np.clip((dur - t) / 0.12, 0, 1)
    y = rui * env * 0.55
    c = som.click(); y[:len(c)] += c[:n] * 1.4
    return y


def congelar():
    SR = som.SR
    y = som.tick() * 1.0
    n = int(0.12 * SR); t = np.arange(n) / SR
    z = np.sin(2 * np.pi * np.cumsum(220 * np.exp(-t * 30) + 90) / SR) * som._env(n, 0.001, 0.03) * 0.5
    out = np.zeros(max(len(y), n)); out[:len(y)] += y; out[:n] += z
    return out


def deslize():
    """O ligamento escorregando: fricção curta e macia (ruído filtrado, sem ataque seco). NUNCA clique/estalo."""
    SR = som.SR
    n = int(0.62 * SR); t = np.arange(n) / SR
    x = som._noise(n, 41)
    fc = 500 + 900 * np.sin(np.pi * t / 0.62)
    y = np.zeros(n); acc = 0.0
    for i in range(n):
        a = math.exp(-2 * math.pi * fc[i] / SR)
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    env = np.sin(np.pi * t / 0.62) ** 2
    return y * env * 1.4


def whoosh_lento():
    return som.whoosh(1.0, seed=9)


def whoosh_recuo():
    """Recuo suave da mão adulta no "força" (sem ataque, sem impacto)."""
    return som.whoosh(0.55, seed=13)[::-1].copy() * 0.8


def whoosh_invertido():
    return som.whoosh(0.4, seed=11)[::-1].copy()


def tique_duplo():
    a = som.tick(); n = len(a) + int(0.11 * som.SR)
    y = np.zeros(n); y[:len(a)] += a * 0.8; y[int(0.11 * som.SR):int(0.11 * som.SR) + len(a)] += a * 0.6
    return y


def janelas(T, F, dur):
    xs = np.arange(0, dur + 0.01, 0.01)
    gb = np.ones_like(xs); gh = np.ones_like(xs)
    for i, x in enumerate(xs):
        tp = F.tipo(x)
        gb[i] = {"play": 1.0, "lenta": 0.0, "congela": 0.45, "volta": 0.2}[tp]
        gh[i] = {"play": 1.0, "lenta": 0.8, "congela": 0.9, "volta": 0.55}[tp]
        if tp == "congela" and lento_k(x, T) > 0:
            gb[i] = 0.0
        if tp == "play" and T["e3"] <= x < T["corte"]:
            gb[i] = 0.6                                           # "a batida da trilha volta, baixa"
    k = np.ones(15) / 15
    gb = np.convolve(np.pad(gb, 7, mode="edge"), k, "valid"); gh = np.convolve(np.pad(gh, 7, mode="edge"), k, "valid")
    return xs, gb, gh


def _media_movel(x, w):
    n = len(x); off = (w - 1) // 2
    S = np.concatenate([[0.0], np.cumsum(x, dtype=np.float64)])
    i = np.arange(n)
    return (S[np.clip(i + off + 1, 0, n)] - S[np.clip(i + off - w + 1, 0, n)]) / w


def mixar_cl(voz, dur, eventos, T, F, ganho_trilha=0.40):
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


def _video_de(F, f, tipos=("play",)):
    """Primeiro instante de VÍDEO em que o filme passa por f num trecho dos `tipos` dados (ou None)."""
    for t0, t1, tipo, a, b, _ in F.segs:
        if tipo in tipos and a <= f < b and b > a:
            return t0 + (f - a) / (b - a) * (t1 - t0)
    return None


def sons(T, F):
    ev = []
    R2 = F.R2
    for f, nome, g in ((F_SOBE, "whoosh", 0.3), (F_POUSO, "thump", 0.3)):        # o 1× (dentro do borrão)
        t0 = _video_de(F, f)
        if t0 is not None and t0 < T["volta"]:
            ev.append((t0, nome, g))
    t_sobe_l = _video_de(F, F_SOBE, ("lenta",))
    t_pouso_l = _video_de(F, F_POUSO, ("lenta",))
    ev += [(T["volta"], lambda: rebobinar(T["camera"] - T["volta"]), 0.9),
           (T["camera"], "pop", 0.55)]
    if t_sobe_l:
        ev.append((t_sobe_l, whoosh_lento, 0.25))
    ev += [(T["repara"], congelar, 1.0), (T["repara"] + 0.02, "whoosh", 0.25),
           (T["mao2"] + 0.02, "tick", 0.45),
           (T["cotovelo"] + 0.02, "ding", 0.35),
           (T["ligamento"], "whoosh", 0.4),
           (T["escorrega"] + 0.05, deslize, 0.35),
           (t_descongela(T) - 0.1, whoosh_invertido, 0.3)]
    if t_pouso_l:
        ev.append((t_pouso_l, "thump", 0.3))
    ev += [(T["corpo"], congelar, 0.85),
           (T["nao1"] + 0.3, "tick", 0.25),                        # v2: a seta que volta = tique, não impacto
           (T["e3"], "pop", 0.45),
           (T["force"], whoosh_recuo, 0.22),                         # v2: a mão RECUA (sem thump: nada encosta)
           (T["leve"] + 0.02, "ding", 0.45),
           (T["corte"] - 0.02, chiado, 0.25), (T["corte"] + 0.12, "click", 0.4),
           (T["upa2"], "pop", 0.5), (T["upa2"] + 0.05, whoosh_lento, 0.25),
           (T["axilas"] + 0.05, "tick", 0.3),
           (T["nao3"] + 0.2, tique_duplo, 0.35)]
    t_p2 = _video_de(F, R2.f_pouso, ("play", "lenta"))
    if t_p2:
        ev.append((t_p2, "thump", 0.25))
    ev += [(T["pulsos_fim"] + 0.05, "click", 0.3),
           (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def tempos_previa(T, F):
    return (0.0, 0.25, 0.4, 0.6, 0.9, T["volta"] + 0.2, T["volta"] + 0.45, T["camera"] + 0.15, T["camera"] + 0.6,
            T["braco1"] + 0.1, T["parou"] + 0.1, T["parou"] + 0.4, T["repara"] + 0.3, T["mao2"] + 0.4,
            T["cotovelo"] + 0.4, T["ligamento"] + 0.1, T["escorrega"] + 0.2, T["escorrega"] + 0.5,
            T["pousou"] - 0.05, T["pousou"] + 0.2, T["pousou"] + 0.5, T["crianca"] + 0.1, T["deixa"] + 0.3,
            T["esticado"] + 0.3, T["corpo"] + 0.5, T["nao1"] + 0.3, T["mexer"] + 0.3, T["e3"] + 0.4,
            T["dolorosa"] if "dolorosa" in T else T["pronacao"] + 0.6, T["comum"] + 0.3, T["pequenas"] + 0.4,
            T["nao2"] + 0.3, T["puxe"] + 0.4, T["force"] + 0.3, T["leve"] + 0.5, T["avaliar"] + 0.6,
            T["ortopedista"] + 0.3, T["rapida"] + 0.3, T["corte"] + 0.1, T["corte"] + 0.5, T["prevenir"] + 0.2,
            T["upa2"] + 0.2, T["axilas"] + 0.5, T["nao3"] + 0.6, T["pulsos"] + 0.3, T["pulsos_fim"] + 0.5,
            T["pulsos_fim"] + 1.2, T["manda"] + 1.2, T["total"] - 1 / 30)


# ------------------------------------------------------------------ entrada única (réplica do cf_comum.fazer_render, com mix próprio)
def preparar(ep, tmp):
    roteiro = "\n".join(ep["roteiro"])
    voz_bruta, palavras = _voz.narrar(roteiro, _voz.RITMO_COMO_FUNCIONA, os.path.join(tmp, "voz"))
    voz_c, pal, tirado = comprimir(voz_bruta, palavras, respiro_cta=RESPIRO_CTA)
    pal = alinhar(pal, roteiro)
    T = ancoras(pal, ANCORAS)
    pf = next(p for p in pal if p["w"].lower() == "pulsos")              # fim da 2ª câmera lenta
    T["pulsos_fim"] = pf["t"] + pf["d"]
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
