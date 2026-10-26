# -*- coding: utf-8 -*-
"""CÂMERA LENTA (série nova) — episódio "CAIU E LEVANTOU: / ENTÃO NÃO QUEBROU?" (fratura na criança).

Mesma mecânica do piloto cf_cameralenta_ponta_pes: um REPLAY de TV. Uma criança cai da bicicleta em 1×
(rápido e borrado), a fita VOLTA, o lance é revisto em CÂMERA LENTA e CONGELA no detalhe. O tempo do filme
(`Filme.tf`) é separado do tempo do vídeo: o mundo (criança e bicicleta) é desenhado em função do tempo do
filme; a narração nunca para nem desacelera.

Cada câmera lenta REVELA o que o 1× escondeu, e só revê filme que o 1× JÁ passou:
  1. 1ª câmera lenta: a MÃO ESPALMADA chega primeiro ao chão (no 1× o toque fica dentro do borrão). O filme
     congela no toque e anéis dourados marcam o cotovelo e o punho, POR FORA da pele.
  2. Ainda congelado, uma LUPA esquemática OPACA (fundo claro e neutro; o antebraço de perfil, em pele opaca,
     chegando à mão; por dentro, os dois ossos em marfim com a ponta alargada no punho; sem rótulo) mostra os
     ossos ARQUEANDO e o de cima TRINCANDO do lado de fora da curva, sem se separar. Ao lado, um GALHINHO
     VERDE enverga e racha do mesmo jeito (o nome desenhado) e o carimbo GALHO VERDE. A lupa fecha.
  3. Volta o 1× (plano aberto, borrão maior): a criança termina a queda, vira para a bicicleta, AGACHA e,
     num movimento rápido, puxa o braço para junto do corpo, estica SÓ a outra mão ao guidão, aponta um ponto
     do antebraço — e levanta, braços soltos: "levantou bem". A fita volta e a 2ª câmera lenta revê esse
     trecho: congela no braço protegido (seguro pela outra mão), mostra só a mão livre indo ao guidão
     (bolinha e trilha douradas; o círculo FICA no braço que não sai do lugar) e congela no dedo que aponta.
  No "Viu", CORTE DE FITA para outra tomada (fita 2): de pé, calma, a outra mão apoia o braço, entra a tipoia
  improvisada no "Apoie" e o selo do estetoscópio no "avaliar" (some antes da CTA). Sem replay depois disso.

Regras da série e do verificador (storyboard.json), todas aqui:
  * O selo CÂMERA LENTA só EXISTE com a lentidão ligada (0,25× e os congelamentos dentro dela): nunca no 1×,
    no ◀◀, na tipoia ou na CTA. A moldura âmbar segue a mesma janela.
  * Vermelho e roxo/lilás PROIBIDOS no vídeo inteiro (roupa, bicicleta, pele, sombra, marcações).
  * Nada sobre o braço no 1× de "incha"/"roxa"; nenhum som de osso quebrando (nada de crackle); a trinca é
    um traço escuro de um lado só, sem deslocar, sem fragmento, sem sangue; a pele por fora não muda.
  * Criança SEM traços de rosto (sem olhos, sem boca, sem choro); ninguém puxa nem estica o braço; a dor é a
    própria criança mostrando o lugar (nenhuma mão de adulto aperta o braço).
  * Nada de ❚❚, barra de progresso, "PAUSA", timecode ou dígitos: congelar = flash + tique + chip apagado.
  * Nenhum texto além do `tela` (CÂMERA LENTA, 1×, 0,25×, GALHO VERDE), do gancho e da interface.
Assinatura sonora do piloto (batida some na câmera lenta, rebobinar com cliques, tique seco no congelamento,
chiado no corte de fita), com mix próprio (`mixar_cl`, cópia do piloto), sem mexer em som.py.

Helpers COPIADOS (não importados) do piloto cf_cameralenta_ponta_pes: Filme (adaptado), tubo, _trim, sstep,
_img/_blit/fundo_cl/monitor_fundo/varredura/faixas_tracking/corte_fita/cantoneiras/flash, relogio (orig.
cf_andador), chip_c, _setas, painel, circulo_mao, estetoscopio, ponto_ouro, desenha_trilha, selo_lenta,
trilha_partes, _fita, rebobinar, chiado, congelar, janelas, _media_movel, mixar_cl. Do cf_fratura_estresse:
a trinca irregular afinando e o osso longo com a ponta alargada (adaptados) e as cores do osso marfim. Do
cf_cotovelo_baba: a figura de criança sem rosto (aqui redesenhada DE PERFIL, montada em esqueleto) e a ideia
da lupa com a estrutura por dentro. Importados sem cópia: capa/interface/ancoras (cf_comum), carimbo_ouro,
comprimir, alinhar, montar_blocos (cf_fratura_cola), paleta e texto (cf_alongamento).
A cena é PRESA ao roteiro pelas palavras-âncora (ANCORAS): roteiro sem elas = KeyError no render.
"""
import math
import os

import numpy as np
import skia

from . import som, voz as _voz
from .base import FPS, codificar, previas as _previas
from .cf_alongamento import (BG_OUT, CX, F_BLACK, H, OSSO_B, OSSO_C, OSSO_L, OURO, PART, W, clamp, e_back,
                             e_inout, e_out, lerp, lerpc, paint, prog, texto)
from .cf_comum import ancoras, capa, interface
from .cf_fratura_cola import alinhar, carimbo_ouro, comprimir, montar_blocos

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "caiu": ("caiu", 1, False), "volta": ("volta", 1, False), "camera": ("câmera", 1, False),
    "lenta": ("lenta", 1, False), "entao": ("então", 1, False), "quebrou": ("quebrou", 1, False),
    "repara": ("repara", 1, False), "mao": ("mão", 1, False), "chegou": ("chegou", 1, False),
    "primeiro": ("primeiro", 1, False), "queda": ("queda", 1, False), "espalmada": ("espalmada", 1, False),
    "comum": ("comum", 1, False), "cotovelo": ("cotovelo", 1, False), "punho": ("punho", 1, False),
    "crianca": ("criança", 1, False), "proprias": ("próprias", 1, False), "como": ("como", 1, False),
    "galho": ("galho", 1, False), "verde": ("verde", 1, False), "nem": ("nem", 1, False),
    "toda": ("toda", 1, False), "fratura2": ("fratura", 2, False), "incha": ("incha", 1, False),
    "roxa": ("roxa", 1, False), "hora": ("hora", 1, False), "protege": ("protege", 1, False),
    "braco": ("braço", 1, False), "pega": ("pega", 1, False), "coisas": ("coisas", 1, False),
    "doi": ("dói", 1, False), "ponto": ("ponto", 1, False), "osso": ("osso", 1, False),
    "viu": ("viu", 1, False), "desses": ("desses", 1, False), "apoie": ("apoie", 1, False),
    "corpo": ("corpo", 1, False), "leve": ("leve", 1, False), "avaliar": ("avaliar", 1, False),
    "manda": ("manda", 1, False),
}
DESTAQUE = {"levantou", "quebrou", "primeiro", "espalmada", "cotovelo", "punho", "galho", "verde", "incha",
            "roxa", "protege", "pega", "ponto", "desses", "corpo", "avaliar"}
RESPIRO_CTA = 1.6
R_SELO, R_1X, R_LENTA, R_GALHO = "CÂMERA LENTA", "1×", "0,25×", "GALHO VERDE"     # todos em ep["tela"]

# ------------------------------------------------------------------ paleta (SEM vermelho e SEM roxo/lilás)
PELE, PELE_CL, PELE_ESC, PELE_LINHA = "#F0B49A", "#F7CDB8", "#DA987E", "#B9765E"
CAMISA, CAMISA_CL, CAMISA_ESC, CAMISA_LINHA = "#7EC8E3", "#A9DDEF", "#4FA3C4", "#2F7FA0"
BERMUDA, BERMUDA_ESC, BERMUDA_LINHA = "#C9CED6", "#A7AEB9", "#7E8794"
TENIS, TENIS_SOLA, TENIS_LINHA = "#F4F7FA", "#B8C2CC", "#7D8896"
CABELO = "#4A3426"
CAPACETE, CAPACETE_LINHA, FRISO = "#F7EEDD", "#B7A486", "#8FC3F0"
QUADRO, QUADRO_CL, QUADRO_ESC, QUADRO_LINHA = "#6FD3B5", "#9BE4CD", "#3A9C80", "#1F5E4D"
PNEU, ARO, RAIO, SELIM = "#26303A", "#C9D3DC", "#9AA8B5", "#3A4350"
PEDRA, PEDRA_CL, PEDRA_LINHA = "#8E99A4", "#B5BEC7", "#5B6570"
CALCADA, CALCADA_CL, CALCADA_JUNTA, MEIO_FIO = "#5E7186", "#6A7E93", "#93A6B9", "#C3D0DC"
GRAMA, GRAMA_ESC = "#2C5F52", "#244E44"
ARVORE, ARVORE_ESC, TRONCO_ARV = "#1E4A47", "#193F3D", "#2A3A3C"
TIPOIA, TIPOIA_LINHA = "#F7EEDD", "#B9A27E"
FUNDO_CARTAO = "#0B1824"
AMBAR = "#FFB547"
AZUL_CL = "#9CC9FF"
TRINCA = "#2B2118"
ESCURO = "#1C2A38"                                               # tom para a perna/braço de trás (opaco)

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
    """Cinemática inversa de dois segmentos (ombro->cotovelo->punho, quadril->joelho->tornozelo).
    dobra = +1: a junta vai para +x quando o membro desce (joelho); -1: para trás (cotovelo).
    Alvo fora do alcance: o membro fica esticado apontando para ele."""
    dx, dy = bx - ax, by - ay
    d0 = math.hypot(dx, dy) or 1.0
    d = max(abs(l1 - l2) + 1.0, min(d0, l1 + l2 - 0.5))
    a = math.atan2(dy, dx)
    A = math.acos(clamp((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d), -1.0, 1.0))
    g = a - dobra * A
    jx, jy = ax + l1 * math.cos(g), ay + l1 * math.sin(g)
    ux, uy = dx / d0, dy / d0
    ex, ey = ax + ux * d, ay + uy * d
    return (jx, jy), (ex, ey)


# ------------------------------------------------------------------ a bicicleta (coordenadas da bicicleta: eixo de trás = (0, 0))
R_RODA = 68.0
EIXO_D = (250.0, 0.0)
MOVEL = (92.0, 6.0)
QUADRIL_B = (58.0, -142.0)                                       # onde fica o quadril de quem pedala
MANOPLA = (176.0, -150.0)
TOQUE_D = (250.0, R_RODA)                                        # ponto de apoio da roda da frente (pivô do tranco)
PEDRA_X, PEDRA_R = 600.0, 26.0
V_BIKE = 420.0                                                   # px do mundo / s de filme (1×)
F_IMP = 0.40                                                     # a roda da frente bate na pedra
X_TRAS_IMP = 310.0                                               # eixo de trás no impacto (a roda da frente encosta na pedra)
F_LANCA, TOQUE, F_JOELHOS = 0.50, 0.80, 1.05                     # solta o guidão / a mão toca o chão / joelhos no chão
F_VIRA0, F_VIRA1, F_AGACHA = 1.08, 1.30, 1.36                    # vira de frente para a bicicleta / agachada
F_B = 1.52                                                       # instante em que a 2ª câmera lenta congela ("braço")
F2 = 20.0                                                        # tempo de filme da FITA 2 (outra tomada, depois do "Viu")
AG_X, AG_Y = 686.0, 1004.0                                       # quadril agachado (perto da roda da frente)
AG_PE_P, AG_PE_L = 648.0, 726.0                                  # tornozelos (x do mundo) agachada
V1, VL = 1.0, 0.25                                               # 1× e câmera lenta (0,25×)
DEITA = 0.36                                                     # bicicleta deitada (achatada contra o chão)


class Bike:
    """Estado da bicicleta no tempo de filme f: rola até a pedra, dá o tranco (a traseira sobe) e tomba."""

    def __init__(self, f):
        fc = min(f, F_IMP)
        self.xr = X_TRAS_IMP + V_BIKE * (fc - F_IMP)
        if f < F_IMP:
            self.pitch = 0.0
        elif f < 0.60:
            self.pitch = 22.0 * e_out(prog(f, F_IMP, 0.60))
        else:
            k = prog(f, 0.60, 0.86)
            self.pitch = 22.0 * (1 - k * k) + (3.0 * math.sin(math.pi * prog(f, 0.86, 1.0)) if f > 0.86 else 0.0)
        self.sq = lerp(1.0, DEITA, e_inout(prog(f, 0.78, 1.18)))
        self.sq += (0.04 * math.sin(math.pi * prog(f, 1.18, 1.32))) if f > 1.18 else 0.0
        # rodas: a de trás continua girando solta depois do tranco; a da frente trava na pedra
        rot0 = (self.xr - 140.0) / R_RODA
        self.giro_t = rot0 + (5.0 * 0.9 * (1 - math.exp(-(f - F_IMP) / 0.9)) if f > F_IMP else 0.0)
        self.giro_d = rot0
        self.pedal = 0.6 + (self.xr - 140.0) / R_RODA / 1.8
        m = skia.Matrix()
        m.setTranslate(-TOQUE_D[0], -TOQUE_D[1])
        m.postRotate(self.pitch)                                   # a traseira sobe (pivô na roda da frente)
        m.postTranslate(TOQUE_D[0], TOQUE_D[1])
        m.postTranslate(self.xr, GY - R_RODA)
        m.postTranslate(0, -GY); m.postScale(1.0, self.sq); m.postTranslate(0, GY)   # tomba (achata no chão)
        self.M = m

    def map(self, x, y):
        p = self.M.mapXY(x, y)
        return p.x(), p.y()

    def pedais(self):
        a = self.pedal
        perto = (MOVEL[0] + 30 * math.cos(a), MOVEL[1] + 30 * math.sin(a))
        longe = (MOVEL[0] - 30 * math.cos(a), MOVEL[1] - 30 * math.sin(a))
        return self.map(*perto), self.map(*longe)


def _roda(cv, cx, cy, giro, a=255):
    cv.drawCircle(cx, cy, R_RODA, paint(PNEU, a, "stroke", 13))
    cv.drawCircle(cx, cy, R_RODA - 9, paint(ARO, a, "stroke", 4))
    p = skia.Path()
    for i in range(8):
        g = giro + i * math.pi / 4
        p.moveTo(cx, cy); p.lineTo(cx + (R_RODA - 10) * math.cos(g), cy + (R_RODA - 10) * math.sin(g))
    cv.drawPath(p, paint(RAIO, a, "stroke", 2.2))
    cv.drawCircle(cx, cy, 7, paint(ARO, a))
    cv.drawCircle(cx, cy, 7, paint("#5E7186", a, "stroke", 2))


def _cano(cv, p0, p1, w):
    cv.drawLine(p0[0], p0[1], p1[0], p1[1], paint(QUADRO_LINHA, 255, "stroke", w + 4))
    cv.drawLine(p0[0], p0[1], p1[0], p1[1], paint(QUADRO, 255, "stroke", w))


def bicicleta(cv, b):
    """A bicicleta de desenho (quadro verde-menta, pneus escuros), no referencial dela."""
    cv.save(); cv.concat(b.M)
    _roda(cv, 0, 0, b.giro_t)
    _roda(cv, EIXO_D[0], EIXO_D[1], b.giro_d)
    topo_sel, topo_cx, base_cx = (68.0, -112.0), (196.0, -104.0), (206.0, -72.0)
    _cano(cv, (0, 0), MOVEL, 9)                                   # corrente / garfo de trás
    _cano(cv, (0, 0), (66, -98), 8)
    _cano(cv, MOVEL, topo_sel, 12)                                # tubo do selim
    _cano(cv, (68, -102), topo_cx, 11)                            # tubo de cima
    _cano(cv, MOVEL, base_cx, 13)                                 # tubo de baixo
    _cano(cv, topo_cx, base_cx, 15)                               # caixa de direção
    garfo = skia.Path(); garfo.moveTo(*base_cx); garfo.quadTo(238, -40, EIXO_D[0], EIXO_D[1])
    cv.drawPath(garfo, paint(QUADRO_LINHA, 255, "stroke", 13)); cv.drawPath(garfo, paint(QUADRO, 255, "stroke", 9))
    cv.drawLine(topo_cx[0], topo_cx[1], 200, -128, paint("#5E7186", 255, "stroke", 8))     # mesa
    cv.drawLine(200, -128, MANOPLA[0], MANOPLA[1], paint("#8796A6", 255, "stroke", 8))     # guidão
    cv.drawLine(200, -128, MANOPLA[0] + 4, MANOPLA[1] + 2, paint("#5E7186", 255, "stroke", 3))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(MANOPLA[0] - 16, MANOPLA[1] - 8, MANOPLA[0] + 10, MANOPLA[1] + 8), 7, 7),
                 paint(SELIM))
    cv.drawLine(topo_sel[0], topo_sel[1], 62, -126, paint("#8796A6", 255, "stroke", 7))    # canote
    sel = skia.Path(); sel.moveTo(30, -132); sel.quadTo(60, -144, 92, -134); sel.quadTo(64, -122, 30, -128); sel.close()
    cv.drawPath(sel, paint(SELIM)); cv.drawPath(sel, paint("#222A33", 255, "stroke", 2))
    for xx, yy, w in ((150, -100, 4), (40, -52, 3)):                                      # brilho do quadro
        cv.drawLine(xx - 30, yy, xx + 20, yy - 3, paint(QUADRO_CL, 200, "stroke", w))
    cv.drawCircle(MOVEL[0], MOVEL[1], 18, paint(RAIO, 255, "stroke", 4))                   # coroa
    for sg in (1, -1):                                                                     # pedivelas e pedais
        a = b.pedal
        px, py = MOVEL[0] + sg * 30 * math.cos(a), MOVEL[1] + sg * 30 * math.sin(a)
        cv.drawLine(MOVEL[0], MOVEL[1], px, py, paint("#5E7186", 255, "stroke", 6))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(px - 12, py - 4, px + 12, py + 4), 3, 3), paint("#3A4350"))
    cv.restore()


def pedra(cv):
    p = skia.Path()
    x, y, r = PEDRA_X, GY, PEDRA_R
    p.moveTo(x - r * 1.15, y + 2)
    p.cubicTo(x - r * 1.2, y - r * 0.9, x - r * 0.3, y - r * 1.45, x + r * 0.35, y - r * 1.3)
    p.cubicTo(x + r * 1.1, y - r * 1.1, x + r * 1.3, y - r * 0.3, x + r * 1.15, y + 2)
    p.close()
    cv.drawOval(skia.Rect(x - r * 1.4, y - 6, x + r * 1.5, y + 8), paint("#000000", 70, blur=5))
    cv.drawPath(p, paint(PEDRA)); cv.drawPath(p, paint(PEDRA_LINHA, 255, "stroke", 3))
    cv.drawLine(x - r * 0.5, y - r * 0.95, x + r * 0.2, y - r * 1.12, paint(PEDRA_CL, 230, "stroke", 5))


# ------------------------------------------------------------------ a criança de perfil (esqueleto)
L_TOR, L_OMBRO, L_PESC, R_CAB = 130.0, 118.0, 56.0, 58.0          # criança: cabeça grande, tronco curto
L_BR, L_AB = 78.0, 74.0                                          # braço, antebraço
L_CX, L_CN = 96.0, 92.0                                          # coxa, perna
MAO_K = 1.2                                                      # mão um pouco maior (leitura no celular)
ANK = GY - 24.0                                                  # tornozelo do pé apoiado no chão


def _base_pose():
    return dict(hx=0.0, hy=0.0, tor=0.0, cab=0.0,
                mp=(40.0, -40.0), mp_t=0.0, ml=(40.0, -40.0), ml_t=0.0,
                mp_rel=0.0, mp_abs=0.0, mp_w=0.0, ml_rel=0.0, ml_abs=0.0, ml_w=0.0,
                mp_abre=0.0, mp_chao=0.0, mp_aponta=0.0, ml_abre=0.0, ml_chao=0.0, ml_aponta=0.0,
                mp_cot=(0.0, 0.0), mp_cw=0.0, ml_cot=(0.0, 0.0), ml_cw=0.0, mp_k=1.0, ml_k=1.0,
                pp=(10.0, 210.0), pl=(-10.0, 210.0), ppa=0.0, pla=0.0, l_frente=0.0, l_topo=0.0, dir=1.0)


def P(**k):
    p = _base_pose(); p.update(k)
    return p


def w2l(hx, hy, d, x, y):
    return ((x - hx) * d, y - hy)


def lerp_pose(a, b, k):
    out = {}
    for key, va in a.items():
        vb = b[key]
        if isinstance(va, tuple):
            out[key] = _lp(va, vb, k)
        else:
            out[key] = lerp(va, vb, k)
    return out


def pose_bike(f):
    """Pedalando (procedural): quadril no selim, mãos no guidão, pés nos pedais."""
    b = Bike(f)
    hx, hy = b.map(*QUADRIL_B)
    g = b.map(*MANOPLA)
    pn, pf = b.pedais()
    return P(hx=hx, hy=hy, tor=22.0, cab=-10.0,
             mp=w2l(hx, hy, 1, g[0] - 2, g[1]), ml=w2l(hx, hy, 1, g[0] - 10, g[1] - 2), mp_rel=-8.0, ml_rel=-8.0,
             pp=w2l(hx, hy, 1, pn[0] - 4, pn[1] - 18), pl=w2l(hx, hy, 1, pf[0] - 4, pf[1] - 18), ppa=8.0, pla=8.0)


class Roteiro:
    """Os quadros-chave do FILME (segundos de filme). Depois do tombo, a criança vira para a bicicleta,
    AGACHA e, num movimento só e rápido (que o 1× atravessa borrado), puxa o braço machucado para junto do
    corpo e o segura com a outra mão (protege), estica a mão LIVRE até o guidão (só ela pega), volta essa
    mão e APONTA um ponto do antebraço (dói num ponto) — e então levanta e fica de pé, braços soltos:
    no 1× ela "levantou bem". A 2ª câmera lenta revê justamente esse trecho, preso às palavras-âncora.
    A FITA 2 (f >= F2) é outra tomada, depois do "Viu": de pé, calma, a outra mão apoia o braço (a tipoia
    entra no "Apoie"); não é continuação do 1×, por isso entra com corte de fita."""

    def __init__(self, T):
        k = {}
        k["prot"] = F_B - 0.03                                              # a mão livre já segura o antebraço
        k["solta"] = F_B + 0.025                                            # ...e sai em direção ao guidão
        k["barra"] = F_B + VL * (T["coisas"] + 0.40 - T["pega"])            # a mão livre chega ao guidão
        k["deixa"] = F_B + VL * (T["doi"] - 0.10 - T["pega"])               # solta o guidão e vai apontar
        k["fP"] = F_B + VL * (T["ponto"] - T["pega"])
        k["aponta"] = k["fP"] - 0.012                                       # o dedo chega ao ponto
        k["solta2"] = k["fP"] + 0.08
        k["em_pe"] = k["fP"] + 0.46
        self.k = k
        self.chaves = self._chaves()
        self.chaves2 = self._chaves2()

    def _chaves(self):
        k = self.k
        out = [(F_IMP, pose_bike(F_IMP))]
        b5 = Bike(F_LANCA)
        g = b5.map(*MANOPLA)
        hx, hy = 450.0, 860.0                                              # sai do selim, ainda segurando o guidão
        out.append((F_LANCA, P(hx=hx, hy=hy, tor=55.0, cab=-26.0, mp=w2l(hx, hy, 1, g[0] - 2, g[1]),
                               ml=w2l(hx, hy, 1, g[0] - 10, g[1] - 2), mp_rel=-8.0, ml_rel=-8.0,
                               pp=(-70.0, 120.0), pl=(-90.0, 105.0), ppa=40.0, pla=40.0)))
        hx, hy = 600.0, 915.0                                              # o mergulho: a mão chega primeiro
        out.append((TOQUE, P(hx=hx, hy=hy, tor=108.0, cab=-46.0,
                             mp=w2l(hx, hy, 1, 775.0, 1088.0), mp_abs=0.0, mp_w=1.0, mp_abre=1.0, mp_chao=1.0,
                             ml=w2l(hx, hy, 1, 748.0, 1068.0), ml_rel=-20.0, ml_abre=0.7,
                             pp=(-130.0, -70.0), pl=(-146.0, -52.0), ppa=100.0, pla=100.0)))
        hx, hy = 650.0, 984.0                                              # de quatro, joelhos no chão
        out.append((F_JOELHOS, P(hx=hx, hy=hy, tor=75.0, cab=-45.0,
                                 mp=w2l(hx, hy, 1, 775.0, 1088.0), mp_abs=0.0, mp_w=1.0, mp_abre=1.0, mp_chao=1.0,
                                 ml=w2l(hx, hy, 1, 752.0, 1088.0), ml_abs=0.0, ml_w=1.0, ml_abre=1.0, ml_chao=1.0,
                                 pp=w2l(hx, hy, 1, 560.0, 1084.0), pl=w2l(hx, hy, 1, 548.0, 1080.0), ppa=160.0, pla=160.0)))
        # agachada, virada para a bicicleta: o braço machucado (o da frente) vem para junto da barriga;
        # a mão livre apoia no joelho
        hx, hy = AG_X, AG_Y
        pes = dict(pp=w2l(hx, hy, -1, AG_PE_P, ANK), pl=w2l(hx, hy, -1, AG_PE_L, ANK))
        out.append((F_AGACHA, P(hx=hx, hy=hy, dir=-1.0, tor=26.0, cab=8.0, **pes,
                                mp=(56.0, -70.0), mp_t=1.0, mp_rel=-8.0, mp_abre=0.25,
                                ml=w2l(hx, hy, -1, AG_X - 52.0, 992.0), ml_t=0.0, ml_abre=0.6)))
        # PROTEGE: a mão livre segura o antebraço machucado por baixo, junto à barriga
        prot = P(hx=hx, hy=hy, dir=-1.0, tor=16.0, cab=10.0, **pes, **GUARDA_AG)
        prot.update(segura_livre(prot))
        out.append((k["prot"], prot))
        out.append((k["solta"], dict(prot)))
        # NÃO PEGA: inclina e só a mão LIVRE vai ao guidão; o braço machucado fica parado junto ao corpo
        b = Bike(3.0)
        gx, gy = b.map(*MANOPLA)
        hx2 = AG_X - 16.0
        alc = P(hx=hx2, hy=hy, dir=-1.0, tor=44.0, cab=-4.0, pp=w2l(hx2, hy, -1, AG_PE_P, ANK),
                pl=w2l(hx2, hy, -1, AG_PE_L, ANK), mp=(60.0, -72.0), mp_t=0.6, mp_rel=-6.0, mp_abre=0.15)
        alc.update(ml=w2l(hx2, hy, -1, gx + 4, gy), ml_t=0.0, ml_rel=10.0, ml_abre=0.0)
        out.append((k["barra"], alc))
        out.append((k["deixa"], dict(alc)))
        # DÓI NUM PONTO: endireita, olha para o braço e APONTA um ponto do antebraço com o indicador
        hx3 = AG_X - 6.0
        pt = P(hx=hx3, hy=hy, dir=-1.0, tor=APONTA["tor"], cab=APONTA["cab"], pp=w2l(hx3, hy, -1, AG_PE_P, ANK),
               pl=w2l(hx3, hy, -1, AG_PE_L, ANK), mp=APONTA["mp"], mp_t=1.0, mp_rel=APONTA["mp_rel"], mp_abre=0.15)
        pt.update(aponta_livre(pt))
        out.append((k["aponta"], pt))
        out.append((k["solta2"], dict(pt)))
        # de pé, braços soltos (o braço machucado parado, um pouco dobrado ao lado do corpo): "levantou bem"
        hx4, hy4 = 700.0, 892.0
        em_pe = P(hx=hx4, hy=hy4, dir=-1.0, tor=4.0, cab=6.0, pp=w2l(hx4, hy4, -1, 680.0, ANK),
                  pl=w2l(hx4, hy4, -1, 724.0, ANK), mp=(12.0, 4.0), mp_t=1.0, mp_rel=-4.0, mp_abre=0.35,
                  ml=(-6.0, 22.0), ml_t=1.0, ml_abre=0.45)
        out.append((k["em_pe"], em_pe))
        out.append((k["em_pe"] + 5.0, dict(em_pe)))
        return out

    def _chaves2(self):
        """FITA 2: de pé, calma, virada para a bicicleta; a outra mão vem apoiar o braço por baixo."""
        hx, hy = 700.0, 892.0
        base = dict(dir=-1.0, tor=5.0, cab=12.0, pp=w2l(hx, hy, -1, 680.0, ANK), pl=w2l(hx, hy, -1, 724.0, ANK))
        c0 = P(hx=hx, hy=hy, **base, mp=(64.0, -50.0), mp_t=1.0, mp_rel=-4.0, mp_abre=0.15,
               ml=(-6.0, 22.0), ml_t=1.0, ml_abre=0.45)
        c1 = P(hx=hx, hy=hy, **base, **GUARDA)
        c1.update(segura_livre(c1))
        return [(F2, c0), (F2 + 0.55, c1), (F2 + 60.0, dict(c1))]

    @staticmethod
    def _interp(ch, f):
        if f >= ch[-1][0]:
            return dict(ch[-1][1])
        if f <= ch[0][0]:
            return dict(ch[0][1])
        i = 0
        while ch[i + 1][0] <= f:
            i += 1
        (fa, pa), (fb, pb) = ch[i], ch[i + 1]
        return lerp_pose(pa, pb, e_inout(prog(f, fa, fb)))

    def pose(self, f):
        if f >= F2 - 1.0:                                                  # fita 2 (outra tomada)
            p = self._interp(self.chaves2, f)
            p["tor"] += 1.1 * math.sin(f * 2.6)
            return p
        if f <= F_IMP:
            p = pose_bike(f)
        else:
            p = self._interp(self.chaves, f)
            if f < F_LANCA:                                                # as mãos seguem o guidão até soltar
                b = Bike(f)
                g = b.map(*MANOPLA)
                p["mp"] = w2l(p["hx"], p["hy"], 1, g[0] - 2, g[1])
                p["ml"] = w2l(p["hx"], p["hy"], 1, g[0] - 10, g[1] - 2)
            if F_LANCA <= f < TOQUE:                                       # a mão abre no ar e assenta no toque
                k = prog(f, F_LANCA + 0.02, F_LANCA + 0.18)
                p["mp_abre"] = e_out(k)
                p["mp_chao"] = sstep(prog(f, TOQUE - 0.09, TOQUE))
                p["mp_w"] = sstep(prog(f, TOQUE - 0.14, TOQUE))
        # vira de frente para a bicicleta (no 1×, dentro do borrão)
        p["dir"] = math.cos(math.pi * sstep(prog(f, F_VIRA0, F_VIRA1)))
        if f > F_AGACHA:                                                   # respiração (só com o filme andando)
            p["tor"] += 1.1 * math.sin(f * 2.6)
        return p


# braço machucado junto ao corpo (o "protege"); a OUTRA mão o segura por baixo, por cima no desenho
GUARDA = dict(mp=(66.0, -54.0), mp_t=1.0, mp_rel=-4.0, mp_abre=0.15)                # de pé
GUARDA_AG = dict(mp=(66.0, -76.0), mp_t=1.0, mp_rel=-6.0, mp_abre=0.15)             # agachada: acima das coxas
SEGURA = dict(fr=0.48, ang=-64.0, dv=7.0, k=0.95, cot=(2.0, -44.0), abre=0.35)


def segura_livre(p):
    """A mão livre SEGURA o antebraço machucado: palma logo abaixo do meio do antebraço, dedos para cima,
    desenhada por cima dele (vê-se a mão segurando); o cotovelo fica escondido atrás do tronco."""
    q = dict(p); q["tor"] = 0.0
    J = _joints(q)
    c, w = J["cot_p"], J["pun_p"]
    fr = SEGURA["fr"]
    cx, cy = lerp(c[0], w[0], fr), lerp(c[1], w[1], fr) + SEGURA["dv"]
    a = math.radians(SEGURA["ang"])
    kk = MAO_K * SEGURA["k"]
    wx, wy = cx - 18 * kk * math.cos(a), cy - 18 * kk * math.sin(a)
    return dict(ml=(wx, wy), ml_t=1.0, ml_cot=SEGURA["cot"], ml_cw=1.0, ml_abs=SEGURA["ang"] + p["tor"], ml_w=1.0,
                ml_aponta=0.0, ml_abre=SEGURA["abre"], ml_k=SEGURA["k"], l_topo=1.0, l_frente=0.0, ml_rel=0.0)


# apontando o ponto do antebraço (ajustado olhando o desenho): o braço machucado à frente do corpo; a mão
# livre vem por cima, de frente, e o indicador (longo e grosso) encosta no antebraço do lado de fora do tronco
APONTA = dict(tor=8.0, cab=26.0, mp=(78.0, -46.0), mp_rel=-6.0,
              fr=0.78, ang=42.0, cot=(0.0, -70.0), k=0.88)


def aponta_livre(p):
    """Mão livre apontando: põe a PONTA do indicador sobre o antebraço machucado (lado de cima, a `fr` do
    cotovelo ao punho), com a mão inclinada `ang` graus e o cotovelo dado (escondido atrás do tronco: o
    braço vem cruzando por trás, em escorço). Tudo no referencial do TRONCO (gira junto com ele)."""
    q = dict(p); q["tor"] = 0.0
    J = _joints(q)
    c, w = J["cot_p"], J["pun_p"]
    fr = APONTA["fr"]
    cx, cy = lerp(c[0], w[0], fr), lerp(c[1], w[1], fr)
    dx, dy = w[0] - c[0], w[1] - c[1]
    L = math.hypot(dx, dy) or 1.0
    nx, ny = dy / L, -dx / L
    if ny > 0:
        nx, ny = -nx, -ny
    r = lerp(14.5, 11.5, fr)
    px, py = cx + nx * (r + 1.0), cy + ny * (r + 1.0)
    th = math.radians(APONTA["ang"])
    kk = MAO_K * APONTA["k"]
    lx, ly = (28.0 + 36.0 - 3.0) * kk, -9.0 * kk
    wx = px - (lx * math.cos(th) - ly * math.sin(th))
    wy = py - (lx * math.sin(th) + ly * math.cos(th))
    return dict(ml=(wx, wy), ml_t=1.0, ml_cot=APONTA["cot"], ml_cw=1.0, ml_abs=APONTA["ang"] + p["tor"], ml_w=1.0,
                ml_aponta=1.0, ml_abre=0.0, ml_k=APONTA["k"], l_topo=1.0, ml_rel=0.0)


# ------------------------------------------------------------------ desenho da criança
def _joints(p):
    """Juntas no referencial LOCAL (quadril na origem, +x = para onde ela olha)."""
    tor = p["tor"]
    J = {}
    J["pesc"] = rot((0.0, -L_TOR), tor)
    J["omb_p"] = rot((0.0, -L_OMBRO), tor)
    J["omb_l"] = rot((-5.0, -L_OMBRO + 3), tor)
    J["cab"] = _lp(J["pesc"], rot((0.0, -L_TOR - L_PESC), tor + p["cab"]), 1.0)
    J["cab"] = (J["pesc"][0] + rot((0.0, -L_PESC), tor + p["cab"])[0], J["pesc"][1] + rot((0.0, -L_PESC), tor + p["cab"])[1])
    for lado in ("p", "l"):
        alvo = p["m" + lado]
        alvo = _lp(alvo, rot(alvo, tor), p["m" + lado + "_t"])
        om = J["omb_" + lado]
        cot, pun = ik(om[0], om[1], alvo[0], alvo[1], L_BR, L_AB, -1)
        cw = p["m" + lado + "_cw"]
        if cw > 0:                                           # cotovelo dado à mão (braço em escorço) e punho no alvo
            ce = p["m" + lado + "_cot"]
            ce = _lp(ce, rot(ce, tor), p["m" + lado + "_t"])
            cot, pun = _lp(cot, ce, cw), _lp(pun, alvo, cw)
        J["cot_" + lado], J["pun_" + lado] = cot, pun
        ang_ab = math.degrees(math.atan2(pun[1] - cot[1], pun[0] - cot[0]))
        J["mao_ang_" + lado] = lerp(ang_ab + p["m" + lado + "_rel"], p["m" + lado + "_abs"], p["m" + lado + "_w"])
        q = (0.0, 0.0) if lado == "p" else (-4.0, 2.0)
        jo, to = ik(q[0], q[1], p["p" + lado][0], p["p" + lado][1], L_CX, L_CN, 1)
        J["joe_" + lado], J["tor_" + lado], J["quad_" + lado] = jo, to, q
    return J


def _sombrear(cv, path, cor, escuro, aro=((16, -0.10), (8, -0.20))):
    """Preenche e dá volume com um aro mais escuro por dentro do contorno (opaco, sem desfoque)."""
    cv.drawPath(path, paint(lerpc(cor, ESCURO, escuro)))
    cv.save(); cv.clipPath(path, skia.ClipOp.kIntersect, True)
    for larg, f in aro:
        c = lerpc(cor, "#000000", -f) if f < 0 else lerpc(cor, "#FFFFFF", f)
        cv.drawPath(path, paint(lerpc(c, ESCURO, escuro), 255, "stroke", larg))
    cv.restore()


def _mao_path(abre, aponta):
    """Mão de desenho no referencial do punho (+x = para fora da mão; -y = lado do polegar)."""
    p = skia.Path(); p.addOval(skia.Rect(2, -13, 34, 13))                      # palma
    dedos = (-9.0, -3.0, 3.0, 9.0)
    for i, yy in enumerate(dedos):
        comp = lerp(7.0, 22.0 - 2.0 * abs(i - 1.5), abre)
        r = 4.6
        if i == 0 and aponta > 0:                                # o indicador: mais longo e mais grosso
            comp = lerp(comp, 36.0, aponta); r = lerp(4.6, 6.6, aponta)
        abertura = (i - 1.5) * 9.0 * abre
        d = skia.Path(); d.addRRect(skia.RRect.MakeRectXY(skia.Rect(0, -r, comp, r), r, r))
        m = skia.Matrix(); m.setRotate(abertura); m.postTranslate(28, yy * lerp(1.0, 1.25, abre))
        d.transform(m)
        p = _uniao(p, d)
    pol = skia.Path(); pol.addRRect(skia.RRect.MakeRectXY(skia.Rect(0, -4.8, lerp(12.0, 20.0, abre), 4.8), 4.8, 4.8))
    m = skia.Matrix(); m.setRotate(lerp(-30.0, -62.0, abre)); m.postTranslate(10, -10)
    pol.transform(m)
    return _uniao(p, pol)


def mao(cv, pun, ang, abre, chao, aponta, escuro, contorno=0.0, k=1.0):
    cv.save(); cv.translate(*pun)
    cv.scale(1.0, lerp(1.0, 0.56, chao))
    cv.rotate(ang)
    cv.scale(MAO_K * k, MAO_K * k)
    pth = _mao_path(abre, aponta)
    if contorno > 0:                                                          # contorno dourado POR FORA da pele
        cv.drawPath(pth, paint(OURO, int(255 * contorno), "stroke", 11))
    _sombrear(cv, pth, PELE, escuro, aro=((9, -0.08),))
    cv.drawPath(pth, paint(PELE_LINHA, 230, "stroke", 2.6))
    cv.restore()


def braco(cv, J, lado, p, escuro, so_antebraco=False, contorno_mao=0.0):
    om, cot, pun = J["omb_" + lado], J["cot_" + lado], J["pun_" + lado]
    ab = tubo(cot[0], cot[1], 14.5, pun[0], pun[1], 11.5)
    if not so_antebraco:
        ab = _uniao(tubo(om[0], om[1], 17.0, cot[0], cot[1], 14.5), ab)
    _sombrear(cv, ab, PELE, escuro)
    cv.drawPath(ab, paint(PELE_LINHA, 230, "stroke", 2.8))
    mao(cv, pun, J["mao_ang_" + lado], p["m" + lado + "_abre"], p.get("m" + lado + "_chao", 0.0),
        p["m" + lado + "_aponta"], escuro, contorno_mao, p["m" + lado + "_k"])
    if not so_antebraco:                                                      # manga curta da camiseta
        L = math.hypot(cot[0] - om[0], cot[1] - om[1]) or 1.0
        ux, uy = (cot[0] - om[0]) / L, (cot[1] - om[1]) / L
        fim = (om[0] + ux * 40, om[1] + uy * 40)
        mg = tubo(om[0] - ux * 6, om[1] - uy * 6, 23.0, fim[0], fim[1], 21.0)
        _sombrear(cv, mg, CAMISA, escuro)
        cv.drawPath(mg, paint(CAMISA_LINHA, 230, "stroke", 2.6))


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


def perna(cv, J, lado, p, escuro):
    q, jo, to = J["quad_" + lado], J["joe_" + lado], J["tor_" + lado]
    pth = _uniao(tubo(q[0], q[1], 24.0, jo[0], jo[1], 19.0), tubo(jo[0], jo[1], 19.0, to[0], to[1], 13.0))
    _sombrear(cv, pth, PELE, escuro)
    cv.drawPath(pth, paint(PELE_LINHA, 230, "stroke", 2.8))
    tenis(cv, to, p["pp" + ("a" if lado == "p" else "")] if lado == "p" else p["pla"], escuro)
    L = math.hypot(jo[0] - q[0], jo[1] - q[1]) or 1.0                      # perna da bermuda
    ux, uy = (jo[0] - q[0]) / L, (jo[1] - q[1]) / L
    bm = tubo(q[0], q[1], 31.0, q[0] + ux * 62, q[1] + uy * 62, 27.0)
    _sombrear(cv, bm, BERMUDA, escuro, aro=((12, -0.08),))
    cv.drawPath(bm, paint(BERMUDA_LINHA, 230, "stroke", 2.6))


def _tronco_path():
    """Tronco de criança de perfil (camiseta), no referencial do tronco (+x = frente, para cima = -y)."""
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


def tronco(cv, p):
    hip = skia.Path(); hip.addOval(skia.Rect(-40, -26, 38, 34))                  # bermuda (quadril)
    _sombrear(cv, hip, BERMUDA, 0.0, aro=((12, -0.08),))
    cv.drawPath(hip, paint(BERMUDA_LINHA, 230, "stroke", 2.6))
    cv.save(); cv.rotate(p["tor"])
    _sombrear(cv, TRONCO_P, CAMISA, 0.0, aro=((18, -0.10), (8, -0.18)))
    cv.drawLine(-22, -110, -18, -36, paint(CAMISA_CL, 170, "stroke", 9))       # brilho
    cv.drawPath(TRONCO_P, paint(CAMISA_LINHA, 230, "stroke", 2.8))
    cv.drawLine(-34, 6, 30, 12, paint(CAMISA_ESC, 200, "stroke", 3))           # barra da camiseta
    cv.restore()


def cabeca(cv, J, p):
    cx, cy = J["cab"]
    ang = p["tor"] + p["cab"]
    pe = J["pesc"]
    cv.drawPath(tubo(pe[0], pe[1], 13.0, cx, cy, 13.0), paint(PELE))
    cv.save(); cv.translate(cx, cy); cv.rotate(ang)
    c = skia.Path(); c.addCircle(0, 0, R_CAB)
    _sombrear(cv, c, PELE, 0.0, aro=((12, -0.07),))
    cv.save(); cv.clipPath(c, skia.ClipOp.kIntersect, True)                    # cabelo na nuca (atrás)
    cab = skia.Path(); cab.moveTo(-60, -20); cab.quadTo(-30, -26, -14, -10); cab.quadTo(-16, 22, -34, 40)
    cab.lineTo(-70, 40); cab.close()
    cv.drawPath(cab, paint(CABELO))
    cv.restore()
    cv.drawPath(c, paint(PELE_LINHA, 230, "stroke", 2.8))
    cv.drawOval(skia.Rect(-10, -6, 6, 16), paint(PELE_ESC))                      # orelha (sem rosto)
    cv.drawOval(skia.Rect(-10, -6, 6, 16), paint(PELE_LINHA, 220, "stroke", 2.2))
    cv.drawLine(-4, 14, 20, 50, paint("#7E8794", 220, "stroke", 3))             # tira do capacete
    cap = skia.Path()                                                           # capacete (cúpula + aba)
    cap.moveTo(-58, 6); cap.cubicTo(-62, -52, -18, -70, 14, -64)
    cap.cubicTo(44, -58, 62, -36, 66, -10); cap.lineTo(70, -6); cap.quadTo(40, -16, 10, -14)
    cap.quadTo(-30, -12, -58, 6); cap.close()
    cv.drawPath(cap, paint(CAPACETE))
    cv.save(); cv.clipPath(cap, skia.ClipOp.kIntersect, True)
    cv.drawPath(cap, paint("#E3D6BF", 255, "stroke", 12))
    f = skia.Path(); f.moveTo(-50, -14); f.cubicTo(-40, -52, 10, -66, 52, -40)
    cv.drawPath(f, paint(FRISO, 255, "stroke", 9))
    cv.restore()
    cv.drawPath(cap, paint(CAPACETE_LINHA, 240, "stroke", 2.8))
    cv.restore()


def crianca(cv, p, bike=None, contorno_mao=0.0, tipoia=0.0):
    """A criança inteira, de perfil, sem rosto. Ordem: perna e braço de trás, (bicicleta), perna da frente,
    tronco, cabeça, antebraço protegido (na frente da barriga), tipoia e braço da frente."""
    J = _joints(p)
    d = p["dir"]
    cv.save(); cv.translate(p["hx"], p["hy"]); cv.scale(d if abs(d) > 0.02 else 0.02, 1.0)
    perna(cv, J, "l", p, 0.30)
    braco(cv, J, "l", p, 0.30)
    if bike is not None:
        cv.save(); cv.scale(1.0 / (d if abs(d) > 0.02 else 0.02), 1.0); cv.translate(-p["hx"], -p["hy"])
        bicicleta(cv, bike)
        cv.restore()
    perna(cv, J, "p", p, 0.0)
    tronco(cv, p)
    cabeca(cv, J, p)
    if p["l_frente"] >= 0.5 and p["l_topo"] < 0.5:                           # a outra mão segura por baixo, na frente da barriga
        braco(cv, J, "l", p, 0.16, so_antebraco=True)
    braco(cv, J, "p", p, 0.0, contorno_mao=contorno_mao)
    if tipoia > 0:
        desenha_tipoia(cv, J, tipoia)
    if p["l_topo"] >= 0.5:                                                    # a mão livre segura/aponta POR CIMA do antebraço
        braco(cv, J, "l", p, 0.07, so_antebraco=True)
    cv.restore()
    return J


def no_mundo(p, pt):
    return p["hx"] + p["dir"] * pt[0], p["hy"] + pt[1]


def desenha_tipoia(cv, J, k):
    """Tipoia improvisada: lenço triangular marfim com friso azul-claro por baixo do antebraço protegido,
    alça até o ombro do outro lado e o nó. Entra por baixo (k 0..1); o braço não muda de posição."""
    cot, pun = J["cot_p"], J["pun_p"]
    k1 = e_out(clamp(k / 0.6)); k2 = clamp((k - 0.45) / 0.55)
    if k1 <= 0:
        return
    meio = ((cot[0] + pun[0]) / 2, (cot[1] + pun[1]) / 2)
    desce = 46 * k1
    a0 = (cot[0] - 10, cot[1] + 4); a1 = (pun[0] + 16, pun[1] + 2)
    tri = skia.Path()
    tri.moveTo(a0[0], a0[1] - 4 * k1)
    tri.lineTo(a1[0], a1[1] - 3 * k1)
    tri.quadTo(a1[0] + 4, a1[1] + desce * 0.5, meio[0] + 6, meio[1] + desce)
    tri.quadTo(a0[0] - 8, a0[1] + desce * 0.6, a0[0], a0[1] - 4 * k1)
    tri.close()
    cv.drawPath(tri, paint(TIPOIA, int(255 * clamp(k1 * 2))))
    cv.save(); cv.clipPath(tri, skia.ClipOp.kIntersect, True)
    cv.drawLine(a0[0], a0[1] + 1 * k1, a1[0], a1[1] + 2 * k1, paint(FRISO, 255, "stroke", 7))
    cv.drawPath(tri, paint("#E3D6BF", 255, "stroke", 10))
    cv.restore()
    cv.drawPath(tri, paint(TIPOIA_LINHA, int(240 * clamp(k1 * 2)), "stroke", 2.6))
    if k2 > 0:                                                                 # alças até o ombro (nó do outro lado)
        no_ = (J["pesc"][0] - 4, J["pesc"][1] + 14)                     # nó junto ao pescoço, do outro lado
        for ini, larg in ((a1, 13), (a0, 11)):
            al = skia.Path(); al.moveTo(*ini); al.quadTo((ini[0] + no_[0]) / 2 + 10, (ini[1] + no_[1]) / 2, *no_)
            cv.drawPath(al, _trim(paint(TIPOIA_LINHA, 255, "stroke", larg + 4), k2))
            cv.drawPath(al, _trim(paint(TIPOIA, 255, "stroke", larg), k2))
        if k2 > 0.85:
            a = prog(k2, 0.85, 1.0)
            cv.drawCircle(no_[0], no_[1], 11 * e_back(a), paint(TIPOIA))
            cv.drawCircle(no_[0], no_[1], 11 * e_back(a), paint(TIPOIA_LINHA, 255, "stroke", 2.4))
            for dx, dy in ((14, 12), (4, 18)):
                cv.drawLine(no_[0], no_[1], no_[0] + dx * a, no_[1] + dy * a, paint(TIPOIA_LINHA, 255, "stroke", 9))
                cv.drawLine(no_[0], no_[1], no_[0] + dx * a, no_[1] + dy * a, paint(TIPOIA, 255, "stroke", 6))


# ------------------------------------------------------------------ o tempo do filme


class Filme:
    """Liga o tempo do VÍDEO ao tempo do FILME (cópia adaptada do piloto): play (1×), volta (rebobinar),
    lenta (0,25×), congela (0×). Presos às palavras-âncora.
    Regra desta versão: a 2ª câmera lenta só revê filme que o 1× JÁ passou (L..fP ⊂ TOQUE..f_prot); o que
    vem depois do "Viu" é a FITA 2 (outra tomada, F2), separada por corte de fita."""

    def __init__(self, T):
        s = []
        f_s = TOQUE - VL * (T["primeiro"] - T["camera"])                       # a 0,25×, a mão toca NO "primeiro"
        s.append((0.0, T["volta"], "play", 0.0, V1 * T["volta"], None))
        s.append((T["volta"], T["camera"], "volta", V1 * T["volta"], f_s, "inout"))
        s.append((T["camera"], T["primeiro"], "lenta", f_s, TOQUE, None))
        self.t_fecha = T["toda"] - 0.02                                         # a lupa fecha aqui (0,3 s)
        self.t1x = T["fratura2"] + 0.05                                         # o 1× volta (lupa já fechada)
        s.append((T["primeiro"], self.t1x, "congela", TOQUE, TOQUE, None))
        f_prot = TOQUE + V1 * (T["protege"] - self.t1x)                         # 1×: termina a queda, agacha, levanta
        s.append((self.t1x, T["protege"], "play", TOQUE, f_prot, None))
        self.t_l2 = T["protege"] + 0.25                                         # 2ª câmera lenta liga aqui
        self.t_fz = T["braco"] + 0.10                                           # congela no "braço"
        fB = F_B
        L = fB - VL * (self.t_fz - self.t_l2)
        s.append((T["protege"], self.t_l2, "volta", f_prot, L, "inout"))
        s.append((self.t_l2, self.t_fz, "lenta", L, fB, None))
        s.append((self.t_fz, T["pega"], "congela", fB, fB, None))
        fP = fB + VL * (T["ponto"] - T["pega"])
        s.append((T["pega"], T["ponto"], "lenta", fB, fP, None))
        s.append((T["ponto"], T["viu"], "congela", fP, fP, None))
        fim = T["total"] + 2.0
        s.append((T["viu"], fim, "play", F2, F2 + V1 * (fim - T["viu"]), None))      # FITA 2
        self.segs = s
        self.T = T
        self.fB, self.fP, self.f_prot, self.L = fB, fP, f_prot, L
        self.R = Roteiro(T)
        assert TOQUE < L < fB < fP < f_prot, ("2ª câmera lenta fora do que o 1× passou", L, fB, fP, f_prot)

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


def lento_k(t, T, F):
    """0..1: quanto a câmera lenta está LIGADA (selo e moldura âmbar existem só aqui)."""
    return max(prog(t, T["camera"], T["camera"] + 0.18) * (1 - prog(t, F.t1x - 0.22, F.t1x - 0.02)),
               prog(t, F.t_l2, F.t_l2 + 0.18) * (1 - prog(t, T["viu"] - 0.2, T["viu"])))


# ------------------------------------------------------------------ câmera (mundo -> tela)
BASE = (1.0, 540.0, GY, 540.0, GY)
CAM0 = (1.30, 360.0, 1100.0, 540.0, 1150.0)                       # quadro 0: perto da criança e da pedrinha


def _mist(a, b, k):
    return tuple(lerp(x, y, k) for x, y in zip(a, b))


def cameras(T, F):
    """Passos de câmera presos às palavras: (t0, duração, (escala, x_mundo, y_mundo, x_tela, y_tela))."""
    pt = F.R.pose(F.fP)
    Jp = _joints(pt)
    ab = no_mundo(pt, _lp(Jp["cot_p"], Jp["pun_p"], 0.5))
    return (
        (0.32, 0.7, BASE),                                                  # 1×: abre para o tombo
        (T["camera"], 0.8, (1.15, 360.0, 990.0, 540.0, 960.0)),            # entra na câmera lenta: criança e pedra
        (T["quebrou"] - 0.3, 1.6, (1.22, 620.0, 1000.0, 540.0, 960.0)),    # acompanha o tombo até a mão
        (T["primeiro"], 0.13, (1.55, 750.0, 1010.0, 560.0, 905.0)),        # zoom seco na mão espalmada
        (T["cotovelo"] - 0.12, 0.5, (1.30, 740.0, 1000.0, 600.0, 940.0)), # recua: o braço inteiro (lupa à esquerda)
        (F.t1x - 0.08, 0.45, BASE),                                         # 1×: plano aberto (a criança pequena)
        (F.t_l2 - 0.05, 0.5, (1.62, 640.0, 958.0, 540.0, 826.0)),          # 2ª câmera lenta: criança e guidão
        (T["doi"] - 0.05, 0.45, (2.0, ab[0], ab[1], 540.0, 800.0)),        # aproxima no antebraço
        (T["viu"], 0.04, (1.26, 690.0, 905.0, 540.0, 850.0)),              # fita 2 (sob o chiado do corte)
    )


def camera(t, T, F, passos):
    cam = CAM0
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


def praca(cv, s):
    """A praça no referencial do mundo: árvores ao fundo (baixo contraste), grama e a calçada com juntas."""
    for x, r in ((150.0, 120.0), (330.0, 90.0), (960.0, 135.0)):
        cv.drawRect(skia.Rect(x - 9, GY - 260, x + 9, GY - 30), paint(TRONCO_ARV))
        cv.drawCircle(x, GY - 300 - r * 0.2, r, paint(ARVORE))
        cv.drawCircle(x - r * 0.45, GY - 260, r * 0.62, paint(ARVORE_ESC))
    cv.drawRect(skia.Rect(-1500, GY - 40, 3000, GY), paint(GRAMA))
    for i in range(-30, 80):
        x = i * 26.0
        cv.drawLine(x, GY - 40, x + 6, GY - 52, paint(GRAMA_ESC, 255, "stroke", 4))
    cv.drawRect(skia.Rect(-1500, GY, 3000, GY + 700), paint(CALCADA))
    cv.drawRect(skia.Rect(-1500, GY, 3000, GY + 22), paint(CALCADA_CL))
    j = skia.Path()
    for i in range(-10, 20):
        x = i * 190.0
        j.moveTo(x, GY + 22); j.lineTo(x - 40, GY + 700)
        j.moveTo(x + 95, GY); j.lineTo(x + 95, GY + 22)
    j.moveTo(-1500, GY + 22); j.lineTo(3000, GY + 22)
    cv.drawPath(j, paint(CALCADA_JUNTA, 255, "stroke", 3.0 / s))
    cv.drawLine(-1500, GY, 3000, GY, paint(MEIO_FIO, 255, "stroke", 4.0 / s))


def varredura(cv, t, ambar, limpo=False):
    """(cópia do piloto) Linhas de varredura + granulação + moldura âmbar da câmera lenta."""
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
        h = 18 + 10 * i
        cv.drawRect(skia.Rect(CENA.left(), y, CENA.right(), y + h), paint("#FFFFFF", int(46 * a)))
        cv.drawRect(skia.Rect(CENA.left(), y + h, CENA.right(), y + h + 4), paint("#000000", int(70 * a)))


def corte_fita(cv, t, t0):
    """(cópia do piloto) Corte de fita: chiado (faixas de ruído e neve) por ~0,2 s — a cena muda por baixo."""
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


HUD_X, HUD_Y = 786, 1166
POP_C = (540, 560)
POP_C2 = (330, 540)                                              # 2ª câmera lenta: longe da cabeça


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
    if tipo == "congela":                                         # o rótulo do trecho anterior, apagado
        s = R_LENTA if lento_k(t, T, F) > 0 else R_1X
        chip_c(cv, s, *_chip_hud_c(s), a, dim=0.4)
        return
    s = R_LENTA if tipo == "lenta" else R_1X
    hx, hy = _chip_hud_c(s)
    k = t - t0
    if tipo == "lenta" and k < 0.75 and t0 in (T["camera"], F.t_l2):   # "0,25×" grande no meio, que voa para o painel
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
def circulo_mao(cv, cx, cy, rx, ry, k, a, larg=7, tracejado=False):
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
    sombra = paint("#000000", int(110 * a), "stroke", larg + 6, blur=4)
    ouro = paint(OURO, int(255 * a), "stroke", larg)
    if tracejado:
        ouro.setPathEffect(skia.DashPathEffect.Make([2.0, 16.0], 0.0))
        cv.drawPath(p, ouro)
        return
    cv.drawPath(p, _trim(sombra, e_out(k)))
    cv.drawPath(p, _trim(ouro, e_out(k)))


def estetoscopio(cv, x, y, esc, a):
    """Selo branco e calmo do "leva pra avaliar": estetoscópio desenhado (forma, sem texto). (cópia do piloto)"""
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


def desenha_trilha(cv, pts, a, s):
    """Pontilhado dourado no referencial do MUNDO. (cópia do piloto)"""
    if a <= 0 or len(pts) < 2:
        return
    p = skia.Path()
    p.moveTo(*pts[0])
    for i in range(1, len(pts) - 1):
        mx, my = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
        p.quadTo(pts[i][0], pts[i][1], mx, my)
    p.lineTo(*pts[-1])
    pt = paint(OURO, int(255 * a), "stroke", 7.0 / s)
    pt.setPathEffect(skia.DashPathEffect.Make([1.0 / s, 17.0 / s], 0))
    cv.drawPath(p, paint("#000000", int(60 * a), "stroke", 10.0 / s, blur=3.0 / s))
    cv.drawPath(p, pt)


def ponto_ouro(cv, x, y, a, r=13):
    if a <= 0:
        return
    cv.drawCircle(x, y, r + 10, paint(OURO, int(90 * a), blur=10))
    cv.drawCircle(x, y, r, paint(OURO, int(255 * a)))
    cv.drawCircle(x, y, r, paint(FUNDO_CARTAO, int(255 * a), "stroke", 3))


def anel(cv, x, y, r, a, t, t0):
    """Anel dourado que pulsa POR FORA da pele (cotovelo, punho, ponto)."""
    if a <= 0:
        return
    k = max(0.0, t - t0)
    pul = 1 + 0.10 * math.sin(k * 9) * math.exp(-k * 2.5)
    ent = e_back(clamp(k / 0.28))
    rr = r * pul * max(0.01, ent)
    cv.drawCircle(x, y, rr + 4, paint(OURO, int(90 * a), "stroke", 14, blur=7))
    cv.drawCircle(x, y, rr, paint(FUNDO_CARTAO, int(150 * a), "stroke", 10))
    cv.drawCircle(x, y, rr, paint(OURO, int(255 * a), "stroke", 6))


# ------------------------------------------------------------------ a lupa esquemática (OPACA; não é exame)
# Dentro da lupa, num fundo CLARO e neutro: o ANTEBRAÇO de perfil (pele opaca, com contorno) chegando à MÃO,
# e por dentro dele os dois ossos em marfim com a ponta alargada do lado do punho (desenho do osso longo do
# cf_fratura_estresse, adaptado). Nada escuro, nada translúcido, nenhum rótulo: é ilustração, não chapa.
# No "galho" os ossos ARQUEIAM (as pontas ficam paradas; a pele por fora não muda); no "verde" o de cima
# trinca do lado de FORA da curva, sem atravessar e sem separar.
LUPA_C, LUPA_R = (330.0, 588.0), 186.0
FUNDO_LUPA = "#DCE8F0"
HB_ANT, HB_PUNHO = 128.0, 108.0                                 # meia-largura do antebraço e do punho (local)
X_PUNHO = 96.0                                                   # punho, ao longo do antebraço (local)
PINO_A, PINO_B = -150.0, 84.0                                    # os ossos arqueiam entre estes dois pontos
X_FIM_OSSO = 78.0                                                # ponta alargada do osso, junto ao punho
OSSOS = ((-30.0, 78.0, 1.0), (58.0, 60.0, 0.9))                  # (deslocamento transversal, largura, fração da curva)
CURVA_MAX = 48.0                                                 # px na escala da lupa (o "galho" se vê)
ESC_LUPA = 0.8                                                   # escala do desenho dentro da lupa
DESL_LUPA = 64.0                                                 # puxa o punho para perto do centro (a mão aparece)
X_TRINCA = (PINO_A + PINO_B) / 2                                 # a trinca nasce no ápice da curva
N_TR = 6
TRINCA_PTS = ((0.0, 0.0), (8.0, 0.10), (-6.0, 0.20), (9.0, 0.31), (-5.0, 0.41), (7.0, 0.51), (1.0, 0.58))


def _desloc(x, curva):
    """Arco suave (sen²) entre os pinos: derivada zero nas pontas, máximo no meio."""
    if x <= PINO_A or x >= PINO_B:
        return 0.0
    s = math.sin(math.pi * (x - PINO_A) / (PINO_B - PINO_A))
    return curva * s * s


def _meia_larg(x, w):
    """Meia-largura do osso: diáfise um pouco mais fina no meio e a ponta alargada (metáfise) no punho."""
    base = w / 2 * (1 - 0.06 * math.sin(math.pi * clamp((x + 420) / (X_FIM_OSSO + 420))))
    return base + w / 2 * 0.42 * sstep((x - (X_FIM_OSSO - 78)) / 62)


def _osso_lupa(cv, off, w, curva):
    """Um osso do antebraço no referencial local (x ao longo, y atravessado). -> função (x, v) -> ponto."""
    def yc(x):
        return off + _desloc(x, curva)
    xs = [-420 + i * (X_FIM_OSSO + 420) / 60 for i in range(61)]
    cima = [(x, yc(x) - _meia_larg(x, w)) for x in xs]
    baixo = [(x, yc(x) + _meia_larg(x, w)) for x in xs]
    r = _meia_larg(X_FIM_OSSO, w)
    p = skia.Path(); p.moveTo(*cima[0])
    for q in cima[1:]:
        p.lineTo(*q)
    for i in range(1, 16):                                       # ponta arredondada
        a = -math.pi / 2 + math.pi * i / 16
        p.lineTo(X_FIM_OSSO + 0.62 * r * math.cos(a), yc(X_FIM_OSSO) + r * math.sin(a))
    for q in reversed(baixo):
        p.lineTo(*q)
    p.close()
    cv.drawPath(p, paint(OSSO_C))
    cv.save(); cv.clipPath(p, skia.ClipOp.kIntersect, True)
    cv.drawPath(p, paint(OSSO_B, 255, "stroke", 14))
    cv.drawPath(p, paint(lerpc(OSSO_B, OSSO_L, 0.3), 255, "stroke", 4))
    cl = skia.Path(); cl.moveTo(xs[0], yc(xs[0]) - w * 0.2)
    for x in xs[1:]:
        cl.lineTo(x, yc(x) - w * 0.2)
    cv.drawPath(cl, paint("#FFFFFF", 130, "stroke", 6))
    cv.restore()
    cv.drawPath(p, paint(OSSO_L, 240, "stroke", 3.2))
    return lambda x, v: (x, yc(x) + v)


def _antebraco_path():
    """Antebraço + mão de perfil no referencial local (punho em X_PUNHO, mão para +x)."""
    X = X_PUNHO
    p = skia.Path()
    p.moveTo(-420, -HB_ANT)
    p.cubicTo(-200, -HB_ANT - 4, X - 80, -HB_ANT + 2, X - 20, -HB_PUNHO)
    p.cubicTo(X + 20, -HB_PUNHO - 8, X + 40, -126, X + 76, -124)          # base do polegar
    p.cubicTo(X + 110, -122, X + 130, -102, X + 160, -92)
    p.lineTo(X + 260, -88); p.lineTo(X + 260, 104)
    p.cubicTo(X + 190, 114, X + 110, 122, X + 60, 114)
    p.cubicTo(X + 30, 110, X + 10, HB_PUNHO + 4, X - 20, HB_PUNHO)
    p.cubicTo(X - 80, HB_ANT - 2, -200, HB_ANT + 4, -420, HB_ANT)
    p.close()
    return p


ANTEBRACO_L = _antebraco_path()


def _polegar_path():
    X = X_PUNHO
    p = skia.Path()
    p.moveTo(X + 30, -112); p.cubicTo(X + 70, -168, X + 120, -176, X + 150, -150)
    p.cubicTo(X + 166, -136, X + 150, -116, X + 120, -112); p.close()
    return p


POLEGAR_L = _polegar_path()


def _desenha_antebraco(cv):
    p = _uniao(ANTEBRACO_L, POLEGAR_L)
    cv.drawPath(p, paint(PELE))
    cv.save(); cv.clipPath(p, skia.ClipOp.kIntersect, True)
    cv.drawPath(p, paint(PELE_ESC, 255, "stroke", 26))
    cv.drawPath(p, paint(lerpc(PELE, PELE_ESC, 0.5), 255, "stroke", 12))
    cv.drawLine(-420, -HB_ANT + 30, X_PUNHO - 40, -HB_PUNHO + 26, paint(PELE_CL, 200, "stroke", 12))   # brilho
    for yy in (-56, -18, 20, 58):                                           # dedos (sulcos), além do punho
        cv.drawLine(X_PUNHO + 150, yy, X_PUNHO + 260, yy * 1.05, paint(PELE_LINHA, 170, "stroke", 3))
    cv.drawPath(POLEGAR_L, paint(PELE_LINHA, 150, "stroke", 3))
    cv.restore()
    cv.drawPath(p, paint(PELE_LINHA, 255, "stroke", 4))


def _trinca(cv, ponto, w, tr, t, T):
    """Trinca escura e IRREGULAR saindo da borda de fora da curva (lado -y), até ~metade do osso; afina de
    13 px na borda para 4 px na ponta (×0,8 da escala da lupa), com borda clara; dois fios curtinhos; lampejo branco curto. Sem separar o osso."""
    if tr <= 0:
        return None
    topo = -_meia_larg(X_TRINCA, w)
    pts = [ponto(X_TRINCA + dx, topo + 2 + f * w) for dx, f in TRINCA_PTS]
    fl = 1 - prog(t, T["verde"], T["verde"] + 0.55)
    if fl > 0:
        cv.drawCircle(pts[1][0], pts[1][1], 50, paint("#FFFFFF", int(200 * fl), blur=14))
    halo = paint("#FFFDF4", 230, "stroke", 11); halo.setStrokeCap(skia.Paint.kRound_Cap)     # borda clara: lê-se como fenda
    n0 = e_out(tr) * N_TR
    for j in range(N_TR):
        f = clamp(n0 - j)
        if f <= 0:
            break
        (x0, y0), (x1, y1) = pts[j], pts[j + 1]
        cv.drawLine(x0 + 3, y0 + 1, lerp(x0, x1, f) + 3, lerp(y0, y1, f) + 1, halo)
    n = e_out(tr) * N_TR
    for j in range(N_TR):
        f = clamp(n - j)
        if f <= 0:
            break
        (x0, y0), (x1, y1) = pts[j], pts[j + 1]
        wl = lerp(13.0, 4.0, j / (N_TR - 1))
        pt = paint(TRINCA, 255, "stroke", wl); pt.setStrokeCap(skia.Paint.kRound_Cap)
        cv.drawLine(x0, y0, lerp(x0, x1, f), lerp(y0, y1, f), pt)
    for j, (du, dv) in ((2, (11.0, 8.0)), (4, (-10.0, 7.0))):
        g = clamp(n - j - 0.5)
        if g > 0:
            x0, y0 = pts[j]
            pt = paint(TRINCA, 240, "stroke", 3.4); pt.setStrokeCap(skia.Paint.kRound_Cap)
            cv.drawLine(x0, y0, x0 + du * g, y0 + dv * g, pt)
    return pts


def lupa(cv, t, T, F, base_xy, ang):
    """A lupa abre no "criança" a partir do antebraço, os ossos arqueiam no "como/galho", o de cima trinca
    no "verde"; fecha (encolhe até o antebraço e some) a partir do "toda". Fora dela, tudo congelado."""
    abre = e_out(prog(t, T["crianca"], T["crianca"] + 0.35))
    fecha = e_inout(prog(t, F.t_fecha, F.t_fecha + 0.3))
    k = abre * (1 - fecha)
    if k <= 0.01:
        return None
    cx, cy = lerp(base_xy[0], LUPA_C[0], k), lerp(base_xy[1], LUPA_C[1], k)
    r = LUPA_R * k
    some = 1 - prog(t, F.t_fecha + 0.08, F.t_fecha + 0.28)         # fechando, a lupa some (não pousa no corpo)
    cv.saveLayer(None, _alfa(some)) if some < 1 else cv.save()
    cv.drawLine(cx, cy, base_xy[0], base_xy[1], paint("#000000", int(110 * k), "stroke", 9, blur=3))
    cv.drawLine(cx, cy, base_xy[0], base_xy[1], paint("#FFFFFF", int(235 * k), "stroke", 4))
    cv.drawCircle(base_xy[0], base_xy[1], 13, paint("#FFFFFF", int(235 * k), "stroke", 4))
    cv.drawCircle(cx, cy, r + 14, paint("#000000", int(110 * k), blur=14))
    cv.save()
    clip = skia.Path(); clip.addCircle(cx, cy, r)
    cv.clipPath(clip, skia.ClipOp.kIntersect, True)
    cv.translate(cx, cy); cv.scale(max(k, 0.01), max(k, 0.01))
    cv.drawCircle(0, 0, LUPA_R + 4, paint(FUNDO_LUPA))
    cv.rotate(ang); cv.scale(ESC_LUPA, ESC_LUPA)                    # zoom menor: antebraço inteiro, ponta do osso e mão
    cv.translate(-DESL_LUPA, 0)
    _desenha_antebraco(cv)
    arco = e_inout(prog(t, T["como"], T["galho"] + 0.35))
    curva = -CURVA_MAX * arco                                       # para -y: o lado de FORA da curva é o de cima
    tr = prog(t, T["verde"] - 0.04, T["verde"] + 0.22)
    pontos = []
    for off, w, fr in OSSOS:
        pontos.append((_osso_lupa(cv, off, w, curva * fr), w))
    pts = _trinca(cv, pontos[0][0], pontos[0][1], tr, t, T)
    if pts is not None and k > 0.99:                                # círculo dourado em volta da trinca (DENTRO da lupa)
        mx, my = pts[2]
        a_c = prog(t, T["verde"] + 0.12, T["verde"] + 0.47)
        circulo_mao(cv, mx, my + 2, 54, 46, a_c, 1.0, larg=6)
    cv.restore()
    cv.drawCircle(cx, cy, r, paint("#FFFFFF", int(255 * k), "stroke", 6))
    cv.drawArc(skia.Rect(cx - r * 0.78, cy - r * 0.78, cx + r * 0.78, cy + r * 0.78), 200, 50, False,
               paint("#FFFFFF", int(120 * k), "stroke", 6))
    cv.restore()
    return cx, cy


# ------------------------------------------------------------------ o galho verde (o NOME desenhado)
GALHO_C = (790.0, 706.0)
GALHO_L, GALHO_W = 310.0, 30.0
CASCA, CASCA_CL, CASCA_LINHA, MIOLO, FOLHA, FOLHA_LINHA = "#7DBE5C", "#A6D98A", "#2F6A34", "#EEF4CC", "#5DAE4C", "#2F6A34"


def galho_verde(cv, t, T, F):
    """Um galhinho verde ao lado do carimbo: entra no "como", ENVERGA junto com o osso no "galho" e, no
    "verde", racha só do lado de fora da curva (aparece o miolo claro) — sem partir. Sai com a lupa."""
    a = prog(t, T["como"] - 0.1, T["como"] + 0.15) * (1 - prog(t, F.t_fecha, F.t_fecha + 0.25))
    if a <= 0:
        return
    arco = e_inout(prog(t, T["como"], T["galho"] + 0.35))
    tr = e_out(prog(t, T["verde"] - 0.04, T["verde"] + 0.22))
    sag = -30.0 * arco
    L, w = GALHO_L, GALHO_W

    def yc(x):
        s = math.sin(math.pi * (x + L / 2) / L)
        return sag * s * s
    xs = [-L / 2 + i * L / 40 for i in range(41)]
    cv.saveLayer(None, _alfa(a)) if a < 1 else cv.save()
    cv.translate(*GALHO_C); cv.rotate(-4)
    cv.translate(0, 0)
    # folhinhas na ponta da direita (fixas na ponta, que não se mexe)
    for ang, comp in ((-40, 60), (26, 54), (-8, 44)):
        cv.save(); cv.translate(L / 2 - 26, yc(L / 2 - 26)); cv.rotate(ang)
        fo = skia.Path(); fo.moveTo(0, 0); fo.quadTo(comp * 0.5, -comp * 0.42, comp, 0); fo.quadTo(comp * 0.5, comp * 0.42, 0, 0)
        cv.drawPath(fo, paint(FOLHA)); cv.drawPath(fo, paint(FOLHA_LINHA, 255, "stroke", 2.6))
        cv.drawLine(2, 0, comp * 0.85, 0, paint(FOLHA_LINHA, 200, "stroke", 2))
        cv.restore()
    p = skia.Path(); p.moveTo(xs[0], yc(xs[0]) - w / 2)
    for x in xs[1:]:
        p.lineTo(x, yc(x) - w / 2 * (1 - 0.25 * (x + L / 2) / L))
    p.lineTo(L / 2 + 4, yc(L / 2))
    for x in reversed(xs):
        p.lineTo(x, yc(x) + w / 2 * (1 - 0.25 * (x + L / 2) / L))
    p.close()
    cv.drawPath(p, paint("#000000", 70, blur=6))
    cv.drawPath(p, paint(CASCA))
    cv.save(); cv.clipPath(p, skia.ClipOp.kIntersect, True)
    hl = skia.Path(); hl.moveTo(xs[0], yc(xs[0]) - w * 0.18)
    for x in xs[1:]:
        hl.lineTo(x, yc(x) - w * 0.18)
    cv.drawPath(hl, paint(CASCA_CL, 230, "stroke", 5))
    cv.restore()
    cv.drawPath(p, paint(CASCA_LINHA, 255, "stroke", 3))
    cv.drawCircle(xs[0], yc(xs[0]), w / 2 - 1, paint(MIOLO))                 # ponta cortada (madeira clara)
    cv.drawCircle(xs[0], yc(xs[0]), w / 2 - 1, paint(CASCA_LINHA, 255, "stroke", 3))
    for xn in (-L * 0.22, L * 0.2):                                            # nós do galho
        cv.drawLine(xn - 3, yc(xn) - w * 0.42, xn + 3, yc(xn) + w * 0.42, paint(CASCA_LINHA, 150, "stroke", 3))
    if tr > 0:                                                                # racha de fora da curva, sem partir
        y0 = yc(0) - w / 2 * 0.89
        zz = ((0.0, 0.0), (5.0, 0.2), (-4.0, 0.38), (5.0, 0.56), (0.0, 0.66))
        n = tr * (len(zz) - 1)
        for j in range(len(zz) - 1):
            f = clamp(n - j)
            if f <= 0:
                break
            (a0, b0), (a1, b1) = zz[j], zz[j + 1]
            x0, yy0 = a0, y0 + b0 * w; x1, yy1 = a1, y0 + b1 * w
            pt = paint("#1E3A1C", 255, "stroke", lerp(7.0, 3.0, j / 3)); pt.setStrokeCap(skia.Paint.kRound_Cap)
            cv.drawLine(x0, yy0, lerp(x0, x1, f), lerp(yy0, yy1, f), pt)
        for dx, ang in ((-7.0, -120.0), (7.0, -60.0), (-2.0, -100.0)):          # lascas claras (fibras) para fora
            ln = 16.0 * tr
            x0 = dx; yy0 = y0 + 1
            x1 = x0 + ln * math.cos(math.radians(ang)); yy1 = yy0 + ln * math.sin(math.radians(ang))
            cv.drawLine(x0, yy0, x1, yy1, paint(CASCA_LINHA, 255, "stroke", 5.2))
            cv.drawLine(x0, yy0, x1, yy1, paint(MIOLO, 255, "stroke", 2.6))
    cv.restore()


# ------------------------------------------------------------------ o mundo (dentro do monitor)
OBTURADOR = {"play": 0.075, "volta": 0.03}                         # s de VÍDEO
OBT_1X_2 = 0.11                                                    # 1× do meio: borrão maior (o gesto passa borrado)
N_AMOSTRAS = 5


def amostras_borrao(t, F):
    """(cópia adaptada do piloto) instantes que entram no borrão do 1× e da volta; nunca antes de t = 0,
    nunca atravessando congelamento nem o corte de fita (fita 2)."""
    tipo = F.tipo(t)
    obt = OBTURADOR.get(tipo)
    if not obt:
        return [t]
    if tipo == "play" and F.t1x <= t < F.T["protege"]:
        obt = OBT_1X_2
    out = [t]
    seg = F.seg(t)
    for i in range(1, N_AMOSTRAS):
        tg = t - obt * i / (N_AMOSTRAS - 1)
        if tg < 0 or F.tipo(tg) == "congela" or (tipo == "play" and F.seg(tg) is not seg):
            break
        out.append(tg)
    return out


def _sombra_chao(cv, x, larg, a):
    cv.drawOval(skia.Rect(x - larg, GY - 7, x + larg, GY + 9), paint("#000000", int(80 * a), blur=6))


def ator(cv, f, R, contorno_mao=0.0, tipoia=0.0):
    """Bicicleta + criança no tempo de filme f. Pedalando, a bicicleta fica ENTRE as pernas; depois do tombo,
    atrás da criança."""
    b = Bike(f)
    p = R.pose(f)
    junto = f < 0.62
    if not junto:
        bicicleta(cv, b)
    _sombra_chao(cv, p["hx"] + 20 * p["dir"], 90, clamp(1 - (GY - 230 - p["hy"]) / 300) if p["hy"] < GY else 1.0)
    J = crianca(cv, p, bike=b if junto else None, contorno_mao=contorno_mao, tipoia=tipoia)
    return p, J, b


def ator_borrado(cv, t, F, R, caixa, tipoia=0.0):
    ams = amostras_borrao(t, F)
    if len(ams) == 1:
        return ator(cv, F.tf(t), R, tipoia=tipoia)
    cv.saveLayer(caixa, None)
    res = None
    for k, tg in enumerate(reversed(ams)):
        if k == 0:
            res = ator(cv, F.tf(tg), R, tipoia=tipoia)
        else:
            cv.saveLayer(caixa, _alfa(1.0 / (k + 1)))
            res = ator(cv, F.tf(tg), R, tipoia=tipoia)
            cv.restore()
    cv.restore()
    return res


def _centro_palma(J, p, lado="p"):
    pun = J["pun_" + lado]; a = math.radians(J["mao_ang_" + lado])
    sq = lerp(1.0, 0.56, p["m" + lado + "_chao"])
    kk = MAO_K * p["m" + lado + "_k"]
    return pun[0] + 18 * kk * math.cos(a), pun[1] + 18 * kk * math.sin(a) * sq


def ponta_dedo(J, p):
    """Ponta do indicador da mão LIVRE (a que aponta), no referencial local da criança."""
    pun = J["pun_l"]; a = math.radians(J["mao_ang_l"])
    kk = MAO_K * p["ml_k"]
    comp = 28.0 + lerp(7.0, 36.0, p["ml_aponta"]) - 3.0
    lx, ly = comp * kk, -9.0 * kk
    return pun[0] + lx * math.cos(a) - ly * math.sin(a), pun[1] + lx * math.sin(a) + ly * math.cos(a)


def trilha_mao(R, f0, f1, lado="p"):
    """Caminho do centro da palma (mão da frente 'p' ou mão livre 'l') de f0 até f1 (mundo)."""
    pts = []
    f = f0
    while f < f1:
        p = R.pose(f); J = _joints(p)
        pts.append(no_mundo(p, _centro_palma(J, p, lado)))
        f += 0.008
    p = R.pose(f1); J = _joints(p)
    pts.append(no_mundo(p, _centro_palma(J, p, lado)))
    return pts


def monitor(cv, t, T, F, passos):
    tipo = F.tipo(t)
    cam = camera(t, T, F, passos)
    if tipo == "volta":
        j = math.sin(t * 97) * 4 + math.sin(t * 41) * 3
        cam = (cam[0], cam[1], cam[2], cam[3] + j, cam[4])
    R = F.R
    f = F.tf(t)
    s = cam[0]
    cv.save(); cv.clipRect(CENA, True)
    monitor_fundo(cv)
    cv.save(); aplica(cv, cam)
    praca(cv, s)
    pedra(cv)
    # trilha dourada da palma ("repara"): só um rastro CURTO atrás da bolinha (os últimos ~0,1 s de filme),
    # que fica à frente do corpo, e apaga logo depois do "primeiro" (quando entra o círculo)
    a_tr = prog(t, T["repara"], T["repara"] + 0.15) * (1 - prog(t, T["primeiro"] + 0.1, T["primeiro"] + 0.4))
    f_rep = F.tf(T["repara"])
    k_cont = 0.0
    if T["espalmada"] <= t < T["espalmada"] + 1.0:              # contorno dourado da mão, pulsando uma vez
        k_cont = math.sin(math.pi * prog(t, T["espalmada"], T["espalmada"] + 1.0))
    tip = prog(t, T["apoie"] + 0.02, T["corpo"] + 0.1)
    caixa = skia.Rect(-400, 300, 1600, 1300)
    if tipo in OBTURADOR:
        p, J, b = ator_borrado(cv, t, F, R, caixa, tipoia=tip)
    else:
        p, J, b = ator(cv, f, R, contorno_mao=k_cont, tipoia=tip)
    f_tr0 = max(f_rep, min(f, TOQUE) - 0.11)
    if a_tr > 0 and min(f, TOQUE) > f_tr0 + 0.01 and T["repara"] <= t < F.t1x:
        desenha_trilha(cv, trilha_mao(R, f_tr0, min(f, TOQUE)), a_tr, s)
    # "não pega as coisas": trilha pontilhada SÓ da mão livre, do braço machucado até o guidão
    a_m = prog(t, T["pega"], T["pega"] + 0.12) * (1 - prog(t, T["doi"] - 0.3, T["doi"] - 0.05))
    if a_m > 0 and f > F.fB + 0.005:
        desenha_trilha(cv, trilha_mao(R, F.fB, min(f, R.k["barra"]), "l"), a_m, s)
    cv.restore()

    def tela(pt_local):
        return na_tela(cam, *no_mundo(p, pt_local))

    # bolinha dourada grudada na palma ("repara")
    if a_tr > 0 and t < F.t1x:
        ponto_ouro(cv, *tela(_centro_palma(J, p)), a_tr * prog(t, T["repara"], T["repara"] + 0.12))
    # congelou no toque: círculo do comentarista em volta da mão espalmada
    a_c = prog(t, T["primeiro"], T["primeiro"] + 0.05) * (1 - prog(t, T["cotovelo"] - 0.35, T["cotovelo"] - 0.1))
    if a_c > 0:
        mx, my = tela(_centro_palma(J, p))
        circulo_mao(cv, mx + 4 * s, my - 4 * s, 62 * s, 36 * s, prog(t, T["primeiro"] + 0.04, T["primeiro"] + 0.39), a_c)
    # anéis no cotovelo e no punho (por fora da pele)
    fim_aneis = 1 - prog(t, T["punho"] + 0.45, T["crianca"] - 0.02)          # apagam antes de a lupa abrir
    if T["cotovelo"] <= t < T["crianca"]:
        anel(cv, *tela(J["cot_p"]), 34 * s, prog(t, T["cotovelo"], T["cotovelo"] + 0.08) * fim_aneis, t, T["cotovelo"])
    if T["punho"] <= t < T["crianca"]:
        anel(cv, *tela(J["pun_p"]), 30 * s, prog(t, T["punho"], T["punho"] + 0.08) * fim_aneis, t, T["punho"])
    # a lupa sobre o antebraço, perto do punho
    if T["crianca"] - 0.05 <= t < F.t1x:
        cot, pun = tela(J["cot_p"]), tela(J["pun_p"])
        base = (lerp(cot[0], pun[0], 0.68), lerp(cot[1], pun[1], 0.68))
        ang = math.degrees(math.atan2(pun[1] - cot[1], pun[0] - cot[0]))
        lupa(cv, t, T, F, base, ang)
    # 2ª câmera lenta: braço protegido junto ao corpo (círculo no congelamento do "braço"); o círculo FICA
    # durante o "pega as coisas" (esse braço não sai do lugar) e sai antes do "dói"
    a_b = prog(t, F.t_fz, F.t_fz + 0.05) * (1 - prog(t, T["doi"] - 0.3, T["doi"] - 0.05))
    if a_b > 0:
        c0, c1 = tela(J["cot_p"]), tela(J["pun_p"])
        mx, my = (c0[0] + c1[0]) / 2 + 6 * s, (c0[1] + c1[1]) / 2 + 4 * s
        circulo_mao(cv, mx, my, 84 * s, 58 * s, prog(t, F.t_fz + 0.04, F.t_fz + 0.4), a_b)
    # ...e a bolinha dourada na mão LIVRE, a única que vai ao guidão
    if a_m > 0:
        ponto_ouro(cv, *tela(_centro_palma(J, p, "l")), a_m)
    # "dói num ponto": anel pequeno exatamente sob a ponta do dedo
    a_pt = prog(t, T["ponto"], T["ponto"] + 0.06) * (1 - prog(t, T["viu"] - 0.25, T["viu"] - 0.02))
    if a_pt > 0:
        anel(cv, *tela(ponta_dedo(J, p)), 24 * s, a_pt, t, T["ponto"])
    # "leve pra avaliar": selo calmo com o estetoscópio (apaga antes da CTA, como no piloto)
    a_e = prog(t, T["avaliar"], T["avaliar"] + 0.2) * (1 - prog(t, T["manda"] - 0.4, T["manda"] - 0.1))
    if a_e > 0:
        estetoscopio(cv, 905, 470, 1.35 * e_back(prog(t, T["avaliar"], T["avaliar"] + 0.3)), a_e)

    varredura(cv, t, lento_k(t, T, F))
    faixas_tracking(cv, t, 1.0 if tipo == "volta" else 0.0)
    if tipo == "volta":
        t0 = F.inicio_trecho(t)
        _setas(cv, 96, 410, (0.55 + 0.45 * (math.sin((t - t0) * 16) > -0.3)) * prog(t, t0, t0 + 0.06), 2.2, False)
    for t0, fo in ((T["primeiro"], 1.0), (F.t_fz, 0.8), (T["ponto"], 0.7)):
        flash(cv, t, t0, fo)
    corte_fita(cv, t, T["viu"])
    cv.restore()
    return cam, p, J


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


CARIMBO_XY = (785.0, 572.0)


def quadro(cv, t, T, blocos, ep, F, passos):
    fundo_cl(cv, t)
    monitor(cv, t, T, F, passos)
    fim = 1 - prog(t, T["manda"] - 0.4, T["manda"] - 0.1)
    cantoneiras(cv, fim)
    painel(cv, t, T, F, fim)
    # o galhinho verde (o NOME desenhado) e o carimbo GALHO VERDE, à direita da lupa; saem com ela
    cv.save(); cv.clipRect(CENA, True)
    galho_verde(cv, t, T, F)
    cv.restore()
    carimbo_ouro(cv, R_GALHO, CARIMBO_XY[0], CARIMBO_XY[1], -4, T["verde"] + 0.05, t,
                 dur=F.t_fecha + 0.25 - T["verde"])
    capa(cv, t, T["volta"], ep["gancho"][0], ep["gancho"][1])
    selo_lenta(cv, lento_k(t, T, F) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
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
    """(cópia do piloto) Corte de fita: estalo + chiado branco curto."""
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


def whoosh_invertido():
    return som.whoosh(0.4, seed=11)[::-1].copy()


def tique_agudo():
    SR = som.SR
    n = int(0.09 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * 1760 * t) * som._env(n, 0.001, 0.05) * 0.5


def ding_alto():
    """O ding de som.py um tom acima (reamostrado), para o 2º anel."""
    d = som.ding()
    idx = np.arange(0, len(d) - 1, 1.122)
    return np.interp(idx, np.arange(len(d)), d)


def janelas(T, F, dur):
    xs = np.arange(0, dur + 0.01, 0.01)
    gb = np.ones_like(xs); gh = np.ones_like(xs)
    for i, x in enumerate(xs):
        tp = F.tipo(x)
        gb[i] = {"play": 1.0, "lenta": 0.0, "congela": 0.45, "volta": 0.2}[tp]
        gh[i] = {"play": 1.0, "lenta": 0.8, "congela": 0.9, "volta": 0.55}[tp]
        if tp == "congela" and lento_k(x, T, F) > 0:
            gb[i] = 0.0
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
    ev = [(0.02, "whoosh", 0.25)]
    k = F.R.k
    for f, nome, g in ((TOQUE, "thump", 0.4), (F_JOELHOS, "thump", 0.35), (0.98, "click", 0.3), (1.08, "click", 0.3),
                       (1.2, "click", 0.25), (F_AGACHA, "tick", 0.25), (k["barra"], "tick", 0.25),
                       (k["em_pe"] - 0.08, "tick", 0.3)):
        for t0, t1, tipo, a, b, _ in F.segs:
            if tipo == "play" and a < f < b:                              # (o 1× do meio começa NO toque: sem repetir)
                ev.append((t0 + (f - a) / (b - a) * (t1 - t0), nome, g))
    ev += [(T["volta"], lambda: rebobinar(T["camera"] - T["volta"]), 0.9),
           (T["camera"], "pop", 0.55)]
    t_pedra = _video_de(F, F_IMP, ("lenta",))
    if t_pedra:
        ev.append((t_pedra, "tick", 0.4))
    t_barra = _video_de(F, k["barra"], ("lenta",))
    ev += [(T["repara"] + 0.05, "shimmer", 0.35),
           (T["primeiro"], congelar, 1.0), (T["primeiro"] + 0.02, "whoosh", 0.3),
           (T["espalmada"], "shimmer", 0.35),
           (T["cotovelo"], "ding", 0.35), (T["punho"], ding_alto, 0.35),
           (T["crianca"], "whoosh", 0.4),
           (T["como"] - 0.05, lambda: som.whoosh(0.7, seed=9), 0.25),
           (T["verde"], "tick", 0.45), (T["verde"] + 0.05, "thump", 0.6),
           (F.t_fecha, whoosh_invertido, 0.35),
           (F.t1x, "pop", 0.5),
           (T["protege"], lambda: rebobinar(F.t_l2 - T["protege"]), 0.9),
           (F.t_l2, "pop", 0.55),
           (F.t_fz, congelar, 0.9),
           (T["ponto"], congelar, 0.8), (T["ponto"] + 0.04, tique_agudo, 0.4),
           (T["viu"] - 0.02, chiado, 0.8),
           (T["apoie"] + 0.02, lambda: som.whoosh(0.5, seed=13), 0.35), (T["corpo"] + 0.1, "pop", 0.35),
           (T["avaliar"] + 0.02, "ding", 0.45),
           (T["manda"] + 0.05, "whoosh", 0.5)]
    if t_barra:
        ev.append((t_barra, "tick", 0.35))
    return ev


def tempos_previa(T, F):
    return (0.0, 0.42, 0.8, 1.2, T["volta"] + 0.35, T["camera"] + 0.15, T["camera"] + 0.6, T["entao"] + 0.3,
            T["quebrou"] + 0.4, T["repara"] + 0.3, T["chegou"] + 0.1, T["primeiro"] + 0.4, T["espalmada"] + 0.3,
            T["cotovelo"] + 0.3, T["punho"] + 0.3, T["crianca"] + 0.5, T["galho"] + 0.3, T["verde"] + 0.15,
            T["verde"] + 0.55, F.t_fecha + 0.15, F.t1x + 0.1, F.t1x + 0.45, F.t1x + 0.75, T["incha"] + 0.2,
            T["roxa"], T["hora"], T["protege"] - 0.12, T["protege"] + 0.12, F.t_l2 + 0.2, T["braco"] + 0.5,
            T["pega"] + 0.3, T["coisas"] + 0.25, T["coisas"] + 0.6, T["doi"] + 0.2, T["ponto"] + 0.3,
            T["viu"] + 0.05, T["viu"] + 0.4, T["apoie"] + 0.3, T["corpo"] + 0.3, T["avaliar"] + 0.5,
            T["manda"] - 0.6, T["manda"] + 1.2, T["total"] - 1 / 30)


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
