# -*- coding: utf-8 -*-
"""CÂMERA LENTA (série) — episódio "PERNA MAIS CURTA: / NORMAL ATÉ ONDE?" (discrepância de membro na criança).

Mesma mecânica do piloto cf_cameralenta_ponta_pes: um REPLAY de TV. Uma menina corre num corredor de casa,
vista DE COSTAS, e a câmera a acompanha à mesma distância (quem anda são as tábuas e os batentes). Em 1× a
corrida passa (borrão curto: o balanço da cabeça já se nota); a fita VOLTA e, em CÂMERA LENTA, um ponto
dourado no elástico do rabo de cavalo risca a trilha da cabeça (como a pena de um gráfico que corre para a
direita): fundo-raso-fundo, uma pisada afunda bem mais que a outra (MANCA, com fio até o vale fundo anterior,
circulado). Congelada NO fundo da pisada (zoom 1,65), dois pontos dourados nas pontas do elástico da cintura
e uma horizontal azul-clara mostram a linha inclinada, mais baixa do lado esquerdo dela (DESNÍVEL NO QUADRIL).
O tempo do filme (`Filme.tf`) é separado do tempo do vídeo; a narração nunca para nem desacelera.

Roteiro visual (presos às palavras-âncora):
  * "Diferença bem pequena? Quase toda criança tem": o quadro congelado encolhe para uma miniatura de VT no
    alto e entram TRÊS outras fitas (outras crianças de costas correndo em 1×, trilhas de ondas iguais,
    cintura nivelada), sem rótulo, sem ✓ e sem verde de "certo".
  * "Mancar, desnível no quadril...": ◀◀, a miniatura volta a ocupar a cena, 2ª câmera lenta e congela no
    mesmo fundo (sem carimbo de "diferença nítida": a perna nunca é desenhada diferente).
  * "avaliação": a câmera lenta desliga e o quadro vira um cartão de VT parado; o estetoscópio acende.
    "A diferença se mede com exame, não no olho": um olho aparece, um aro dourado acende no cartão no
    "exame", o olho FECHA no "olho" e as marcas do cartão esmaecem.
  * "Ela ainda vai crescer": o cartão vai para o canto; a menina está PARADA, calma (a cintura segue um pouco
    desnivelada, sem marca), junto de um calendário de parede (crescer = TEMPO, nunca altura). As folhas
    viram até o "prever"; a trilha dourada vai até uma folha lá na frente e a estrelinha acende em "a
    diferença"; o pino crava no "planejar". "Diferença que aumenta": a cena escurece, o cartão volta grande
    com aro âmbar e o vale circulado afunda; "rápido": as folhas viram depressa (▶▶ desenhado). "Procure
    avaliação": o cartão volta ao canto e o estetoscópio pulsa e desce para perto dela.

Regras da série e do verificador (storyboard.json), todas aqui:
  * Selo CÂMERA LENTA só com a lentidão ligada (0,25× e os congelamentos dentro dela): nunca no 1×, no ◀◀,
    no ▶▶, no calendário ou na CTA. A moldura âmbar segue a mesma janela.
  * As duas pernas desenhadas IGUAIS o vídeo inteiro (mesmo comprimento, mesma forma): a câmera lenta mostra
    SINAIS (a trilha que afunda, a cintura inclinada), nunca a medida. Nenhuma régua, fita, trena, marca de
    altura, quadro de crescimento, raio-X, osso, número ou grau. A menina não cresce.
  * Marcas SÓ na trilha da cabeça e no elástico da cintura; nenhuma linha em ombros, costas ou coluna.
  * Sem antes e depois: depois do 2º congelamento ela nunca mais corre (fica parada, calma, até a CTA).
  * Menina de costas, sem rosto, sem choro; nada vermelho no vídeo inteiro.
  * Pisadas no mesmo volume (as duas pernas); nada de "boing"; congelar = flash + tique + chip apagado
    (nada de ❚❚, barra de progresso, "PAUSA", timecode ou dígitos no cronômetro).
  * Nenhum texto além do `tela` (CÂMERA LENTA, 1×, 0,25×, MANCA, DESNÍVEL NO QUADRIL, ELA AINDA CRESCE),
    do gancho e da interface; ◀◀ e ▶▶ são formas.

Helpers COPIADOS (não importados) do piloto cf_cameralenta_ponta_pes e dos episódios da série: Filme
(adaptado), tubo, _trim, sstep, rot, _img/_blit, fundo_cl, monitor_fundo, varredura, faixas_tracking,
cantoneiras, flash, relogio (orig. cf_andador), chip_dim, chip_c, _setas, painel (adaptado), circulo_mao,
ponta_seta, estetoscopio, calendario (adaptado para a parede, em perspectiva), ponto_ouro, desenha_trilha,
selo_lenta, trilha_partes, _fita, rebobinar, avancar, congelar, janelas, _media_movel, mixar_cl, pisadas
(adaptado); ik e _sombrear do cf_cameralenta_osso_crianca (a figura de criança sem rosto, aqui redesenhada
DE COSTAS, com rabo de cavalo); olho do cf_escoliose (o olho que fecha). Importados sem cópia:
capa/ancoras/SIG/DISC (cf_comum; a legenda e a interface vêm COPIADAS, com o espaço da CTA maior), comprimir/alinhar/montar_blocos (cf_fratura_cola), paleta e texto
(cf_alongamento). A cena é PRESA ao roteiro pelas palavras-âncora (ANCORAS): roteiro sem elas = KeyError.
"""
import functools
import math
import os

import numpy as np
import skia

from . import som, voz as _voz
from .base import FPS, codificar, previas as _previas
from .cf_alongamento import (BG_OUT, CX, F_BLACK, F_REG, F_SEMI, OURO, PART, W, H, aviao, clamp, e_back, e_inout,
                             e_out, larg_texto, lerp, lerpc, paint, prog, texto)
from .cf_comum import DISC, SIG, ancoras, capa
from .cf_fratura_cola import alinhar, comprimir, montar_blocos

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "perna": ("perna", 1, False), "onde": ("onde", 1, False), "volta": ("volta", 1, False),
    "fita": ("fita", 1, False),
    "camera": ("câmera", 1, False), "lenta": ("lenta", 1, False), "repara": ("repara", 1, False),
    "manca": ("manca", 1, False), "quadril": ("quadril", 1, False), "desnivelado": ("desnivelado", 1, False),
    "diferenca": ("diferença", 1, False), "pequena": ("pequena", 1, False), "crianca": ("criança", 1, False),
    "sintoma": ("sintoma", 1, False), "mancar": ("mancar", 1, False),
    "desnivel": ("desnível", 1, False), "quadril2": ("quadril", 2, False), "nitida": ("nítida", 1, False),
    "avaliacao": ("avaliação", 1, False), "quem": ("diferença", 3, False), "mede": ("mede", 1, False),
    "exame": ("exame", 1, False), "nao_olho": ("não", 2, False), "olho": ("olho", 1, False),
    "trunfo": ("ela", 2, False), "crescimento": ("crescer", 1, False), "prever": ("prever", 1, False),
    "diferenca_prever": ("diferença", 4, False), "final": ("final", 1, False), "planejar": ("planejar", 1, False),
    "tempo": ("calma", 1, False), "preciso": ("precisar", 1, False),
    "diferenca_rapido": ("diferença", 5, False), "aumenta": ("aumenta", 1, False), "rapido": ("rápido", 1, False),
    "procure": ("procure", 1, False), "avaliacao2": ("avaliação", 2, False), "manda": ("manda", 1, False),
}
DESTAQUE = {"curta", "onde", "manca", "quadril", "desnivelado", "pequena", "criança", "sintoma", "mancar",
            "desnível", "nítida", "avaliação", "exame", "olho", "crescer", "prever", "final", "planejar",
            "calma", "aumenta", "rápido", "procure", "filho"}
RESPIRO_CTA = 1.6
R_SELO, R_1X, R_LENTA = "CÂMERA LENTA", "1×", "0,25×"                         # todos em ep["tela"]
R_MANCA, R_DESNIVEL, R_CRESCE = "MANCA", "DESNÍVEL NO QUADRIL", "ELA AINDA CRESCE"
MAS_ANTES = 0.28                                                 # o 2º ◀◀ começa este tanto antes de "Mancar"

# ------------------------------------------------------------------ paleta (SEM vermelho)
PELE, PELE_ESC, PELE_LINHA = "#F0B49A", "#DA987E", "#B9765E"
FUNDO_CARTAO = "#0B1824"
AMBAR = "#FFB547"
AZUL_CL = "#9CC9FF"
MARFIM = "#F3EBDD"
ESCURO = "#1C2A38"

# a menina (camiseta azul-lavanda, short jeans com elástico marfim, tênis branco de sola verde-água)
ROUPA_MENINA = dict(camisa="#A7B3EC", camisa_linha="#5F6AAE", short="#4F6FA8", short_cl="#6F8DC2",
                    short_linha="#2B416A", costura="#A9C0E6", elastico=MARFIM, elastico_linha="#B9AA92",
                    cabelo="#3E2A1E", cabelo_esc="#2A1C14", prende=MARFIM, rabo=True,
                    sola="#7FD6C2", sola_esc="#4FAE98")
# as outras fitas: a mesma figura, roupas verde-menta, areia e azul-céu (nada vermelho, nada de rótulo)
ROUPAS_OUTRAS = (
    dict(ROUPA_MENINA, camisa="#93D8BE", camisa_linha="#3E8E72", short="#5E7186", short_cl="#7C8FA4",
         short_linha="#36485A", costura="#A9B8C8", cabelo="#2E2119", cabelo_esc="#1F1610", prende="#9CC9FF"),
    dict(ROUPA_MENINA, camisa="#E6D2A6", camisa_linha="#A88F5C", short="#3F5F8F", short_cl="#5B7BAE",
         short_linha="#253B5E", cabelo="#6B4A2E", cabelo_esc="#4E3520", rabo=False),
    dict(ROUPA_MENINA, camisa="#8CC8F0", camisa_linha="#3F86B8", short="#AEB6C2", short_cl="#C9CFD8",
         short_linha="#6E7886", costura="#E3E8EE", cabelo="#4A3426", cabelo_esc="#33241A", prende="#F7EEDD"),
)
TENIS, TENIS_LINHA = "#F4F7FA", "#7D8896"
MEIA = "#FFFFFF"

# corredor (tábuas, paredes azul-acinzentadas um tom acima do fundo, rodapé claro) e as variantes das outras fitas
VARIANTES = (
    dict(pe="#21374A", pd="#1D3244", teto="#132433", fundo="#2C475B", tab=("#6B4F3A", "#7A5B43", "#735540", "#6F523D"),
         junta="#B39474", vinco="#3E2C20", rodape="#C3D0DC", batente="#D3DDE6", vao="#0E1A25"),
    dict(pe="#24403C", pd="#203833", teto="#14272A", fundo="#2E4C47", tab=("#82644B", "#8E6F54", "#7A5D46", "#876850"),
         junta="#C2A383", vinco="#4A3626", rodape="#CFE0D8", batente="#DCE8E2", vao="#0E1C1A"),
    dict(pe="#363440", pd="#302E39", teto="#1C1B24", fundo="#45424F", tab=("#5F6A73", "#68737C", "#59636C", "#636E77"),
         junta="#9AA6B0", vinco="#353C42", rodape="#D6D3DE", batente="#E2E0E8", vao="#14131A"),
    dict(pe="#273452", pd="#222E4A", teto="#161F33", fundo="#33415F", tab=("#6B4F3A", "#7A5B43", "#735540", "#6F523D"),
         junta="#B39474", vinco="#3E2C20", rodape="#C9D3E6", batente="#D7DFEE", vao="#0F1626"),
)

# ------------------------------------------------------------------ o "monitor" de replay e o corredor em perspectiva
CENA = skia.Rect(40, 330, 1040, 1230)                            # o mundo é recortado aqui (selo e karaokê livres)
VP = (540.0, 560.0)                                              # ponto de fuga
PY, PX, TY = 550.0, 430.0, -760.0                                # chão, paredes, teto (px a Z = 1, a distância da menina)
Z_PERTO, Z_FUNDO = 0.6, 6.0
TABUAS = 12
LARG_TAB = 2 * PX / TABUAS
COMP_TAB = 1.15                                                  # comprimento de uma tábua (unidades de Z)
VZ = 1.4                                                         # velocidade da corrida (unidades de Z / s de filme)
Z_PARADA = 1.4                                                   # onde a câmera fica na cena parada (portas longe do calendário)

# ------------------------------------------------------------------ a menina (px de tela, zoom 1)
GX = 415.0                                                       # x da menina correndo
GX_PARADA = 650.0                                                # x da menina parada (o calendário fica à esquerda)
GX_OUTRAS = 430.0                                                # x das crianças das outras fitas
Y_TORN = 1086.0                                                  # tornozelo do pé apoiado
HY0 = 836.0                                                      # quadril no voo (mais alto)
HY_PARADA = 848.0
LT, LS = 122.0, 120.0                                            # coxa e perna: IGUAIS nas duas pernas, sempre
LU, LF = 76.0, 62.0                                              # braço e antebraço
KZ = 0.28                                                        # quanto a profundidade sobe na tela
P_CICLO = 0.68                                                   # ciclo de corrida (2 passos) em s de filme: 2,9 passos/s
PH0 = 0.6                                                        # fase no quadro 0 (pé esquerdo no ar, sola à mostra)
SD = 0.36                                                        # fração de apoio de cada pé (há voo entre os apoios)
ZL, ZT = 40.0, 50.0                                              # o pé pousa à frente e sai atrás
D_ONDA = 9.0                                                     # descida do corpo em cada apoio (rasa)
L_MANCA = 40.0                                                   # descida A MAIS no apoio do pé esquerdo (a manqueira)
W_MANCA = 0.12                                                   # vale largo (um U, não um risco)
I_MANCA = 10.0                                                   # inclinação da cintura no apoio esquerdo (graus; nunca na tela)
U_INCL = 0.19                                                    # fase do pico da inclinação (= o congelamento)
BOT = (2 + 0.18 - PH0) * P_CICLO                                 # fundo da pisada esquerda revista na câmera lenta
BOT_ANT = BOT - P_CICLO                                          # o fundo da pisada esquerda ANTERIOR (o vale circulado)
DFZ = 0.0                                                        # congela NO fundo: a cabeça está no vale mais fundo
TF0 = 0.0
V1, VL, VR = 1.0, 0.25, 4.0
K_TRILHA = 455.0                                                 # a trilha corre para a direita (px por s de filme)
JAN_TRILHA = 0.95                                                # cabe fundo-raso-fundo no quadro congelado
PIVO = (592.0, 700.0)                                            # zoom: cabeça e cintura ocupam o monitor, trilha à direita
S0, S_LENTA, S_CONG = 1.12, 1.3, 1.65                            # zoom no 1×, na câmera lenta e no congelamento


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


def _wrap(x):
    return (x + 0.5) % 1.0 - 0.5


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


def _sombrear(cv, path, cor, escuro=0.0, aro=((16, -0.10), (8, -0.20))):
    """(cópia do cf_cameralenta_osso_crianca) Preenche e dá volume com um aro mais escuro por dentro."""
    cv.drawPath(path, paint(lerpc(cor, ESCURO, escuro)))
    cv.save(); cv.clipPath(path, skia.ClipOp.kIntersect, True)
    for larg, f in aro:
        c = lerpc(cor, "#000000", -f) if f < 0 else lerpc(cor, "#FFFFFF", f)
        cv.drawPath(path, paint(lerpc(c, ESCURO, escuro), 255, "stroke", larg))
    cv.restore()


def _poly(pts):
    p = skia.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    return p


def _M(x, y, graus):
    m = skia.Matrix(); m.setRotate(graus); m.postTranslate(x, y)
    return m


def _mp(m, x, y):
    p = m.mapXY(x, y)
    return p.x(), p.y()


def ik_sag(z, y):
    """Cinemática inversa no plano de perfil (z = para a frente, longe da câmera; y = para baixo), quadril na
    origem; o joelho dobra para a FRENTE (+z). (adaptado do ik do cf_cameralenta_osso_crianca)"""
    d0 = math.hypot(z, y) or 1.0
    d = max(abs(LT - LS) + 1.0, min(d0, LT + LS - 0.5))
    a = math.atan2(y, z)
    A = math.acos(clamp((LT * LT + d * d - LS * LS) / (2 * LT * d), -1.0, 1.0))
    g = a - A
    return (LT * math.cos(g), LT * math.sin(g)), (z / d0 * d, y / d0 * d)


# ------------------------------------------------------------------ a corrida (vista de costas)
def dip(u, manca):
    """Quanto o corpo desce (px) na fase u: as duas pisadas descem igual; com a manqueira, a esquerda desce MAIS."""
    return (D_ONDA * (0.5 + 0.5 * math.cos(4 * math.pi * (u - 0.18)))
            + manca * L_MANCA * math.exp(-(_wrap(u - 0.18) / W_MANCA) ** 2))


def incl(u, manca):
    """Inclinação da cintura (graus; + = lado esquerdo dela mais baixo): só no apoio do pé esquerdo."""
    return manca * I_MANCA * math.exp(-(_wrap(u - U_INCL) / 0.13) ** 2)


def balanco_x(u):
    return -5.0 * math.cos(2 * math.pi * (u - 0.18))


KF_BAL = ((0.0, -50.0, 0.0), (0.25, -80.0, 92.0), (0.5, -28.0, 112.0), (0.75, 24.0, 52.0), (1.0, 40.0, 0.0))


def pe_balanco(w):
    """Caminho do pé no balanço (z, altura): sai atrás, sobe (a sola aparece), vem para a frente e pousa."""
    n = len(KF_BAL) - 1
    i = min(n - 1, int(w * n)); s = w * n - i

    def P(j, c):
        if j < 0:
            return 2 * KF_BAL[0][c] - KF_BAL[1][c]
        if j > n:
            return 2 * KF_BAL[n][c] - KF_BAL[n - 1][c]
        return KF_BAL[j][c]
    out = []
    for c in (1, 2):
        p0, p1, p2, p3 = P(i - 1, c), P(i, c), P(i + 1, c), P(i + 2, c)
        out.append(0.5 * ((2 * p1) + (-p0 + p2) * s + (2 * p0 - 5 * p1 + 4 * p2 - p3) * s * s
                          + (-p0 + 3 * p1 - 3 * p2 + p3) * s ** 3))
    return out[0], max(0.0, out[1])


QUEDA_MIN_BAL = 166.0                                            # do quadril ao tornozelo NA TELA, no balanço (px, zoom 1)


def _smin(a, b, k):
    """Mínimo suave (sem quina no movimento)."""
    return 0.5 * (a + b - math.sqrt((a - b) ** 2 + k * k))


def fase(tf, ph=PH0):
    return (tf / P_CICLO + ph) % 1.0


def pose_corrida(tf, manca=1.0, ph=PH0, gx=GX):
    u = fase(tf, ph)
    return _pose(u, gx + balanco_x(u), HY0 + dip(u, manca), incl(u, manca), True)


def pose_parada(t, gx=GX_PARADA):
    """De pé, calma, de costas (respira devagar e olha um pouco para a esquerda, para o calendário)."""
    return _pose(0.0, gx, HY_PARADA + 1.2 * math.sin(t * 2.1), INC_PARADA, False, olha=1.0)


INC_PARADA = 3.0                                                 # de pé, a cintura continua um pouco desnivelada (sem marca)


def _pose(u, hx, hy, inc, corrida, olha=0.0):
    M = _M(hx, hy, -inc)                                          # quadril: + inclinação = lado esquerdo dela mais baixo
    pernas = []
    for lado, off in ((-1, 0.0), (1, 0.5)):
        q = _mp(M, 30.0 * lado, 4.0)
        sf = None
        if corrida:
            v = (u - off) % 1.0
            if v < SD:
                k = v / SD
                z, up = ZL - (ZL + ZT) * k, 0.0
                sf = 0.45 * sstep((k - 0.5) / 0.5)                 # o calcanhar sobe no fim do apoio
            else:
                z, up = pe_balanco((v - SD) / (1 - SD))
                # o pé do balanço nunca sobe tanto que a barra do short engula a canela: quando a pelve
                # desce (a pisada funda da manqueira), ele sobe menos — a perna segue inteira na tela
                # (coxa saindo do short, joelho, canela, meia, tênis), do mesmo tamanho da outra
                up_max = Y_TORN - q[1] - KZ * z - QUEDA_MIN_BAL
                up = max(0.0, _smin(up, up_max, 24.0))
        else:
            z, up, sf = 4.0, 0.0, 0.0
        (jz, jy), (az, ay) = ik_sag(z, (Y_TORN - up) - q[1])
        if sf is None:
            v1 = (jz, jy); v2 = (az - jz, ay - jy)
            cos_ = (v1[0] * v2[0] + v1[1] * v2[1]) / ((math.hypot(*v1) * math.hypot(*v2)) or 1.0)
            flex = math.degrees(math.acos(clamp(cos_, -1.0, 1.0)))
            sf = clamp((flex - 45.0) / 65.0)
        jo = (q[0] - lado * 2.0, q[1] + jy - KZ * jz)
        to = (q[0] - lado * (6.0 if corrida else 3.0), q[1] + ay - KZ * az)
        pernas.append(dict(lado=lado, q=q, j=jo, t=to, sf=sf))
    tx, ysh = hx, hy - 150.0
    bracos = []
    for lado, sgn in ((-1, 1.0), (1, -1.0)):
        o = (tx + 49.0 * lado, ysh + 16.0)
        if corrida:                                               # cotovelo dobrado, para fora do tronco
            sw = math.sin(2 * math.pi * (u - 0.18)) * sgn             # + = braço vai à frente (some atrás do tronco)
            b, f = max(0.0, -sw), max(0.0, sw)
            c = (o[0] + lado * (16.0 + 14.0 * b), o[1] + 62.0 - 20.0 * b)
            m = (c[0] - lado * (12.0 + 14.0 * f), c[1] + 30.0 - 6.0 * b - 22.0 * f)
            frente = f > 0.2
        else:                                                     # parada: braços soltos ao lado do corpo
            c = (o[0] + lado * 11.0, o[1] + 74.0)
            m = (c[0] + lado * 1.0, c[1] + 60.0)
            frente = False
        bracos.append(dict(lado=lado, o=o, c=c, m=m, frente=frente))
    if corrida:
        rabo, quique = 10.0 * math.sin(2 * math.pi * (u - 0.05)), 5.0 * math.cos(4 * math.pi * (u - 0.22))
    else:
        rabo, quique = 3.0, 0.0
    cab = (tx + 3.0 * olha, ysh - 64.0)
    return dict(M=M, hx=hx, hy=hy, inc=inc, tx=tx, ysh=ysh, cab=cab, pernas=pernas, bracos=bracos,
                rabo=rabo, quique=quique, olha=olha)


def ponto_cabeca(P):
    """O elástico do rabo de cavalo (onde gruda o ponto dourado)."""
    cx, cy = P["cab"]
    return cx + 2.0 * P["olha"], cy - 18.0


def cabeca_em(tf, manca=1.0, ph=PH0, gx=GX):
    """(x, y) do ponto da cabeça no tempo de filme tf, sem montar a pose inteira (para a trilha)."""
    u = fase(tf, ph)
    return gx + balanco_x(u), HY0 + dip(u, manca) - 150.0 - 64.0 - 18.0


def pontos_cintura(P):
    """Pontas do elástico da cintura, POR FORA da roupa (onde acendem os pontos dourados)."""
    return _mp(P["M"], -80.0, -41.0), _mp(P["M"], 80.0, -41.0)


# ------------------------------------------------------------------ desenho da menina (sem rosto: de costas)
def _tenis(cv, x, y, sf):
    """Tênis branco de sola verde-água visto de trás: em `sf` = 1 a sola inteira vira para a câmera."""
    he = 18.0 * sf
    corpo = skia.RRect.MakeRectXY(skia.Rect(x - 24, y - 6, x + 24, y + 28 + he), 13, 13)
    cv.drawRRect(corpo, paint(TENIS))
    topo = lerp(y + 20 + he, y + 1, sf); ins = lerp(0.0, 5.0, sf)
    sola = skia.RRect.MakeRectXY(skia.Rect(x - 25 + ins, topo, x + 25 - ins, y + 28 + he - ins * 0.6),
                                 lerp(4.0, 11.0, sf), lerp(4.0, 11.0, sf))
    cv.save(); cv.clipRRect(corpo, True)
    cv.drawRRect(sola, paint(ROUPA_MENINA["sola"]))
    if sf > 0.3:
        a = int(255 * prog(sf, 0.3, 0.7))
        for k in range(4):
            yy = lerp(topo + 8, y + 22 + he, k / 3)
            cv.drawLine(x - 15 + ins, yy, x + 15 - ins, yy, paint(ROUPA_MENINA["sola_esc"], a, "stroke", 3))
    cv.restore()
    cv.drawRRect(corpo, paint(TENIS_LINHA, 230, "stroke", 2.6))
    if sf < 0.5:                                                  # alcinha do calcanhar
        a = int(255 * (1 - sf * 2))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 7, y - 13, x + 7, y - 3), 4, 4), paint(TENIS, a))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 7, y - 13, x + 7, y - 3), 4, 4), paint(TENIS_LINHA, a, "stroke", 2.2))


def _perna(cv, p):
    (qx, qy), (jx, jy), (tx, ty) = p["q"], p["j"], p["t"]
    pth = _uniao(tubo(qx, qy, 30.0, jx, jy, 23.0), tubo(jx, jy, 22.0, tx, ty, 14.0))
    _sombrear(cv, pth, PELE, 0.0, aro=((14, -0.08), (6, -0.16)))
    cv.drawPath(pth, paint(PELE_LINHA, 230, "stroke", 2.6))
    if ty > jy + 60:                                              # dobrinha atrás do joelho (perna esticada)
        cv.drawArc(skia.Rect(jx - 11, jy - 2, jx + 11, jy + 10), 200, 140, False, paint(PELE_LINHA, 130, "stroke", 2.4))
    meia = tubo(tx, ty - 12, 15.0, tx, ty + 2, 15.0)
    cv.drawPath(meia, paint(MEIA)); cv.drawPath(meia, paint("#C3CCD6", 230, "stroke", 2.2))
    _tenis(cv, tx, ty, p["sf"])


def _braco(cv, b, R):
    (ox, oy), (cx_, cy_), (mx, my) = b["o"], b["c"], b["m"]
    pth = _uniao(tubo(ox, oy, 14.0, cx_, cy_, 12.0), tubo(cx_, cy_, 11.5, mx, my, 10.0))
    _sombrear(cv, pth, PELE, 0.1 if b["frente"] else 0.0, aro=((10, -0.08),))
    cv.drawPath(pth, paint(PELE_LINHA, 230, "stroke", 2.4))
    mao = skia.Path(); mao.addOval(skia.Rect(mx - 11, my - 9, mx + 11, my + 13))
    _sombrear(cv, mao, PELE, 0.1 if b["frente"] else 0.0, aro=((7, -0.08),))
    cv.drawPath(mao, paint(PELE_LINHA, 230, "stroke", 2.4))
    k = 0.45
    mg = tubo(ox, oy - 2, 19.0, lerp(ox, cx_, k), lerp(oy, cy_, k), 17.0)
    _sombrear(cv, mg, R["camisa"], 0.1 if b["frente"] else 0.0, aro=((10, -0.10),))
    cv.drawPath(mg, paint(R["camisa_linha"], 230, "stroke", 2.4))


def _camisa(cv, P, R):
    tx, ysh = P["tx"], P["ysh"]
    pesc = skia.RRect.MakeRectXY(skia.Rect(tx - 15, ysh - 34, tx + 15, ysh + 4), 9, 9)
    cv.drawRRect(pesc, paint(PELE_ESC)); cv.drawRRect(pesc, paint(PELE_LINHA, 200, "stroke", 2.2))
    bl, br = _mp(P["M"], -57.0, -42.0), _mp(P["M"], 57.0, -42.0)
    p = skia.Path()
    p.moveTo(tx - 19, ysh - 10)
    p.quadTo(tx - 40, ysh - 8, tx - 52, ysh + 6)
    p.cubicTo(tx - 57, ysh + 14, tx - 56, ysh + 40, tx - 53, ysh + 60)
    p.cubicTo(tx - 51, ysh + 86, bl[0] - 2, bl[1] - 26, bl[0], bl[1])
    p.lineTo(*br)
    p.cubicTo(br[0] + 2, br[1] - 26, tx + 51, ysh + 86, tx + 53, ysh + 60)
    p.cubicTo(tx + 56, ysh + 40, tx + 57, ysh + 14, tx + 52, ysh + 6)
    p.quadTo(tx + 40, ysh - 8, tx + 19, ysh - 10)
    p.quadTo(tx, ysh - 4, tx - 20, ysh - 10)
    p.close()
    _sombrear(cv, p, R["camisa"], 0.0, aro=((22, -0.08), (9, -0.16)))
    cv.save(); cv.clipPath(p, skia.ClipOp.kIntersect, True)
    cv.drawLine(tx - 26, ysh + 18, tx - 30, ysh + 70, paint(lerpc(R["camisa"], "#FFFFFF", 0.22), 150, "stroke", 12))
    cv.restore()
    cv.drawPath(p, paint(R["camisa_linha"], 230, "stroke", 2.6))
    gola = skia.Path(); gola.moveTo(tx - 21, ysh - 9); gola.quadTo(tx, ysh - 2, tx + 21, ysh - 9)
    cv.drawPath(gola, paint(R["camisa_linha"], 200, "stroke", 5))


def _short(cv, P, R):
    M = P["M"]
    seat = skia.Path(); seat.addRRect(skia.RRect.MakeRectXY(skia.Rect(-63, -34, 63, 26), 20, 20)); seat.transform(M)
    sh = seat
    bainhas = []
    for p in P["pernas"]:
        (qx, qy), (jx, jy) = p["q"], p["j"]
        L = math.hypot(jx - qx, jy - qy) or 1.0
        ux, uy = (jx - qx) / L, (jy - qy) / L
        c = min(60.0, L * 0.8 + 6.0)
        ex, ey = qx + ux * c, qy + uy * c
        sh = _uniao(sh, tubo(qx, qy, 32.0, ex, ey, 31.0))
        bainhas.append((ex, ey, -uy, ux))
    _sombrear(cv, sh, R["short"], 0.0, aro=((16, -0.10), (6, -0.18)))
    cv.save(); cv.clipPath(sh, skia.ClipOp.kIntersect, True)
    for ex, ey, nx, ny in bainhas:                                # barra dobrada (mais clara)
        cv.drawLine(ex + nx * 40, ey + ny * 40, ex - nx * 40, ey - ny * 40, paint(R["short_cl"], 255, "stroke", 14))
    cv.save(); cv.concat(M)
    cost = paint(R["costura"], 200, "stroke", 2.2); cost.setPathEffect(skia.DashPathEffect.Make([6.0, 5.0], 0))
    for s in (-1, 1):                                              # bolsos de trás
        b = skia.Path()
        b.moveTo(s * 14, -26); b.lineTo(s * 52, -26); b.lineTo(s * 50, 0); b.lineTo(s * 33, 8); b.lineTo(s * 16, 0); b.close()
        cv.drawPath(b, paint(lerpc(R["short"], "#000000", 0.08)))
        cv.drawPath(b, cost)
    cv.drawLine(0, -30, 0, 20, paint(R["short_linha"], 170, "stroke", 2.6))
    cv.restore()
    cv.restore()
    cv.drawPath(sh, paint(R["short_linha"], 230, "stroke", 2.6))
    # o ELÁSTICO marfim da cintura, de ponta a ponta (é a linha que mostra o desnível)
    cv.save(); cv.concat(M)
    el = skia.RRect.MakeRectXY(skia.Rect(-66, -52, 66, -30), 10, 10)
    cv.drawRRect(el, paint(R["elastico"]))
    fr = skia.Path(); x = -60.0
    while x < 60:
        fr.moveTo(x, -49); fr.lineTo(x + 1.2, -33); x += 7.5
    cv.save(); cv.clipRRect(el, True)
    cv.drawPath(fr, paint(R["elastico_linha"], 120, "stroke", 1.8))
    cv.drawLine(-66, -33, 66, -33, paint(R["elastico_linha"], 120, "stroke", 3))
    cv.restore()
    cv.drawRRect(el, paint(R["elastico_linha"], 230, "stroke", 2.4))
    cv.restore()


def _cabeca(cv, P, R):
    cx, cy = P["cab"]
    for s in (-1, 1):                                             # orelhas
        o = skia.Path(); o.addOval(skia.Rect(cx + s * 44 - 8, cy - 4, cx + s * 44 + 8, cy + 22))
        _sombrear(cv, o, PELE, 0.0, aro=((5, -0.08),)); cv.drawPath(o, paint(PELE_LINHA, 220, "stroke", 2.2))
    c = skia.Path(); c.addCircle(cx, cy, 46.0)
    _sombrear(cv, c, R["cabelo"], 0.0, aro=((14, -0.12),))
    cv.save(); cv.clipPath(c, skia.ClipOp.kIntersect, True)
    nuca = skia.Path()                                            # nuca: a linha do cabelo preso
    base = 31.0 if R["rabo"] else 38.0
    nuca.moveTo(cx - 40, cy + 60); nuca.lineTo(cx - 36, cy + base + 2)
    nuca.cubicTo(cx - 24, cy + base - 8, cx - 12, cy + base - 2, cx, cy + base + 2)
    nuca.cubicTo(cx + 12, cy + base - 2, cx + 24, cy + base - 8, cx + 36, cy + base + 2)
    nuca.lineTo(cx + 40, cy + 60); nuca.close()
    cv.drawPath(nuca, paint(PELE_ESC))
    ex, ey = ponto_cabeca(P)
    fios = paint(R["cabelo_esc"], 200, "stroke", 2.4)
    if R["rabo"]:                                                 # fios penteados até o prendedor
        for x0, y0 in ((-38, 18), (-22, 30), (22, 30), (38, 18), (-30, -30), (30, -30)):
            f = skia.Path(); f.moveTo(cx + x0, cy + y0)
            f.quadTo(cx + x0 * 0.45, cy + (y0 + ey - cy) * 0.5, ex + x0 * 0.12, ey + 4)
            cv.drawPath(f, fios)
    else:
        for x0 in (-30, -12, 8, 26):
            f = skia.Path(); f.moveTo(cx + x0, cy - 40); f.quadTo(cx + x0 * 1.1, cy, cx + x0 * 1.15, cy + 34)
            cv.drawPath(f, fios)
    cv.restore()
    cv.drawPath(c, paint(R["cabelo_esc"], 230, "stroke", 2.6))
    if not R["rabo"]:
        return
    L = 78.0 + P["quique"]
    cv.save(); cv.translate(ex, ey); cv.rotate(P["rabo"])
    rb = skia.Path()
    rb.moveTo(-12, 2); rb.cubicTo(-24, 26, -20, 54, -2, L); rb.cubicTo(16, 54, 24, 26, 12, 2); rb.close()
    _sombrear(cv, rb, R["cabelo"], 0.0, aro=((8, -0.12),))
    for xx in (-6, 5):
        f = skia.Path(); f.moveTo(xx, 8); f.quadTo(xx * 1.4, 36, xx * 0.3, L - 10)
        cv.drawPath(f, paint(R["cabelo_esc"], 180, "stroke", 2.0))
    cv.drawPath(rb, paint(R["cabelo_esc"], 230, "stroke", 2.4))
    pr = skia.RRect.MakeRectXY(skia.Rect(-15, -7, 15, 8), 7, 7)
    cv.drawRRect(pr, paint(R["prende"])); cv.drawRRect(pr, paint(TENIS_LINHA, 220, "stroke", 2.2))
    cv.restore()


def desenha_crianca(cv, P, R=ROUPA_MENINA):
    """A criança inteira, de costas (sem rosto): braços que vão à frente (atrás do tronco), pernas, camiseta,
    short com o elástico da cintura, cabeça com o rabo de cavalo e os braços que vão para trás."""
    for b in P["bracos"]:
        if b["frente"]:
            _braco(cv, b, R)
    pernas = sorted(P["pernas"], key=lambda p: p["sf"])           # a que levanta a sola vem por cima
    for p in pernas:
        _perna(cv, p)
    _camisa(cv, P, R)
    _short(cv, P, R)
    _cabeca(cv, P, R)
    for b in P["bracos"]:
        if not b["frente"]:
            _braco(cv, b, R)


def sombra_crianca(cv, P, a=1.0):
    x = P["hx"]
    k = clamp((P["hy"] - HY0) / 40.0)
    cv.drawOval(skia.Rect(x - 92, 1098, x + 92, 1126), paint("#000000", int((60 + 50 * k) * a), blur=9))


# ------------------------------------------------------------------ o corredor em perspectiva de um ponto
def proj(X, Y, Z):
    return VP[0] + X / Z, VP[1] + Y / Z


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


def _rel(c):
    """Desenha no referencial da imagem do tamanho da CENA."""
    c.translate(-CENA.left(), -CENA.top())


def corredor_fixo(iv):
    """Paredes, teto, tábuas (as emendas compridas fogem para o ponto de fuga e não se movem), rodapé e a
    janela clara no fim do corredor — em imagem pronta. PROIBIDO aqui: régua, fita, marcas de altura."""
    V = VARIANTES[iv]

    def d(c):
        _rel(c)
        c.drawRect(CENA, paint(V["teto"]))
        zp, zf = 0.35, Z_FUNDO
        for lado, cor in ((-1, V["pe"]), (1, V["pd"])):
            X = lado * PX
            c.drawPath(_poly([proj(X, PY, zp), proj(X, TY, zp), proj(X, TY, zf), proj(X, PY, zf)]), paint(cor))
        c.drawPath(_poly([proj(-PX, TY, zp), proj(PX, TY, zp), proj(PX, TY, zf), proj(-PX, TY, zf)]), paint(V["teto"]))
        for i in range(TABUAS):                                     # tábuas
            X0 = -PX + i * LARG_TAB
            c.drawPath(_poly([proj(X0, PY, zp), proj(X0 + LARG_TAB, PY, zp), proj(X0 + LARG_TAB, PY, zf), proj(X0, PY, zf)]),
                       paint(V["tab"][(i * 3) % len(V["tab"])]))
        for i in range(1, TABUAS):
            X0 = -PX + i * LARG_TAB
            a0, a1 = proj(X0, PY, zp), proj(X0, PY, zf)
            c.drawLine(*a0, *a1, paint(V["vinco"], 255, "stroke", 3.0))
        for lado in (-1, 1):                                         # rodapé claro
            X = lado * PX
            c.drawPath(_poly([proj(X, PY, zp), proj(X, PY - 40, zp), proj(X, PY - 40, zf), proj(X, PY, zf)]), paint(V["rodape"]))
            c.drawLine(*proj(X, PY - 40, zp), *proj(X, PY - 40, zf), paint("#000000", 60, "stroke", 2.5))
            c.drawLine(*proj(X, PY, zp), *proj(X, PY, zf), paint("#000000", 90, "stroke", 3.0))
            c.drawLine(*proj(X, TY, zp), *proj(X, TY, zf), paint("#000000", 70, "stroke", 2.5))
        x0, y0 = proj(-PX, TY, zf); x1, y1 = proj(PX, PY, zf)        # parede do fundo com a janela
        c.drawRect(skia.Rect(x0, y0, x1, y1), paint(V["fundo"]))
        jx0, jy0 = proj(-170, -400, zf); jx1, jy1 = proj(170, -40, zf)
        c.drawRect(skia.Rect(jx0 - 40, jy0 - 40, jx1 + 40, jy1 + 40), paint("#DDEEFF", 60, blur=26))
        c.drawRect(skia.Rect(jx0 - 4, jy0 - 4, jx1 + 4, jy1 + 4), paint(V["batente"]))
        c.drawRect(skia.Rect(jx0, jy0, jx1, jy1), paint("#CFE6F7"))
        c.drawLine((jx0 + jx1) / 2, jy0, (jx0 + jx1) / 2, jy1, paint(V["batente"], 255, "stroke", 3))
        c.drawLine(jx0, (jy0 + jy1) / 2, jx1, (jy0 + jy1) / 2, paint(V["batente"], 255, "stroke", 3))
        fx, fy = proj(0, PY, zf)                                     # reflexo da janela no chão
        c.drawOval(skia.Rect(fx - 70, fy + 10, fx + 70, fy + 230), paint("#DDEEFF", 26, blur=30))
        sh = skia.GradientShader.MakeRadial(skia.Point(*VP), 760, [_c("#000000", 0), _c("#000000", 0), _c("#000000", 120)],
                                            [0.0, 0.35, 1.0])
        c.drawRect(CENA, paint("#000000", 255, shader=sh))
    return _img(("corredor", iv), CENA.width(), CENA.height(), d)


def corredor(cv, zc, iv=0, portas_esq=True):
    """O corredor no ponto zc da corrida: a imagem fixa + batentes e juntas das tábuas que vêm na direção de
    quem assiste (é o chão que anda; a menina fica do mesmo tamanho)."""
    V = VARIANTES[iv]
    _blit(cv, corredor_fixo(iv), CENA.left(), CENA.top())
    for lado, base in ((-1, 1.6), (1, 0.1)):                       # batentes de porta (de cada lado)
        if lado < 0 and not portas_esq:                           # cena parada: a parede esquerda é do calendário
            continue
        X = lado * PX
        n0 = math.floor((zc + Z_PERTO - base - 0.7) / 3.2)
        for n in range(n0, n0 + 4):
            z1 = base + n * 3.2 - zc
            z2 = z1 + 0.55
            if z2 < Z_PERTO - 0.1 or z1 > Z_FUNDO - 0.2:
                continue
            za, zb = max(0.32, z1 - 0.05), z2 + 0.05
            cv.drawPath(_poly([proj(X, PY, za), proj(X, 50, za), proj(X, 50, zb), proj(X, PY, zb)]), paint(V["batente"]))
            za, zb = max(0.32, z1), z2
            cv.drawPath(_poly([proj(X, PY, za), proj(X, 76, za), proj(X, 76, zb), proj(X, PY, zb)]), paint(V["vao"]))
    pj = skia.Path()                                              # juntas das tábuas (claras), correndo
    for i in range(TABUAS):
        X0 = -PX + i * LARG_TAB
        off = ((i * 0.37) % 1.0) * COMP_TAB
        j0 = math.ceil((zc + Z_PERTO - off) / COMP_TAB)
        j1 = math.floor((zc + Z_FUNDO - off) / COMP_TAB)
        for j in range(j0, j1 + 1):
            Z = off + j * COMP_TAB - zc
            a0, a1 = proj(X0 + 3, PY, Z), proj(X0 + LARG_TAB - 3, PY, Z)
            pj.moveTo(*a0); pj.lineTo(*a1)
    cv.drawPath(pj, paint(V["junta"], 230, "stroke", 3.0))


# ------------------------------------------------------------------ câmera (zoom em torno do quadril)
def aplica(cv, cam):
    s, px, py = cam
    cv.translate(px, py); cv.scale(s, s); cv.translate(-px, -py)


def na_tela(cam, x, y):
    s, px, py = cam
    return px + s * (x - px), py + s * (y - py)


def camera(t, T):
    s = S0
    s = lerp(s, S_LENTA, e_inout(prog(t, T["camera"], T["camera"] + 0.8)))
    s = lerp(s, S_CONG, e_out(prog(t, T["manca"], T["manca"] + 0.13)))       # zoom seco no congelamento
    if t >= T["mas"]:
        s = lerp(S_CONG, S_LENTA, e_inout(prog(t, T["mas"], T["mancar"])))
    if t >= T["desnivel"]:
        s = lerp(S_LENTA, S_CONG, e_out(prog(t, T["desnivel"], T["desnivel"] + 0.13)))
    return (s, PIVO[0], PIVO[1])


# ------------------------------------------------------------------ o tempo do filme
class Filme:
    """Liga o tempo do VÍDEO ao tempo do FILME, por trechos presos às palavras-âncora (como no piloto):
    play (1×), volta (rebobinar), lenta (0,25×; a 1ª freia até parar), congela (0×) e avanca (▶▶)."""

    def __init__(self, T):
        s = []
        a = TF0 + V1 * T["volta"]
        self.tf_fz = tf_fz = BOT + DFZ                            # o MESMO quadro nos dois congelamentos
        t_fr = T["manca"] - 0.4
        tf_s = tf_fz - VL * 0.2 - VL * (t_fr - T["camera"])
        s.append((0.0, T["volta"], "play", TF0, a, None))
        s.append((T["volta"], T["camera"], "volta", a, tf_s, "inout"))
        s.append((T["camera"], t_fr, "lenta", tf_s, tf_fz - VL * 0.2, None))
        s.append((t_fr, T["manca"], "lenta", tf_fz - VL * 0.2, tf_fz, "freia"))
        s.append((T["manca"], T["mas"], "congela", tf_fz, tf_fz, None))
        tf_s2 = tf_fz - VL * (T["desnivel"] - T["mancar"])
        s.append((T["mas"], T["mancar"], "volta", tf_fz, tf_s2, "inout"))
        s.append((T["mancar"], T["desnivel"], "lenta", tf_s2, tf_fz, None))
        s.append((T["desnivel"], T["trunfo"], "congela", tf_fz, tf_fz, None))
        tf_p = 20.0                                                 # cena parada (o filme só move o cronômetro)
        tf_r = tf_p + (T["rapido"] - T["trunfo"])
        s.append((T["trunfo"], T["rapido"], "play", tf_p, tf_r, None))
        tf_r2 = tf_r + VR * (T["procure"] - T["rapido"])
        s.append((T["rapido"], T["procure"], "avanca", tf_r, tf_r2, None))
        fim = T["total"] + 2.0
        s.append((T["procure"], fim, "play", tf_r2, tf_r2 + (fim - T["procure"]), None))
        self.segs = s
        self.T = T
        self.tf_s, self.tf_s2 = tf_s, tf_s2

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
        elif ease == "freia":
            k = 2 * k - k * k
        return lerp(a, b, k)

    def tipo(self, t):
        return self.seg(t)[2]

    def inicio_trecho(self, t):
        i = self.segs.index(self.seg(t))
        while i > 0 and self.segs[i - 1][2] == self.segs[i][2] and self.segs[i - 1][1] == self.segs[i][0]:
            i -= 1
        return self.segs[i][0]

    def relogio(self, t):
        """Ângulo do cronômetro: segue o filme, e corre em 1× enquanto as outras fitas passam."""
        T = self.T
        if T["diferenca"] <= t < T["mas"]:
            return self.tf_fz + (t - T["diferenca"])
        if T["mas"] <= t < T["mancar"]:
            return lerp(self.tf_fz + (T["mas"] - T["diferenca"]), self.tf_s2, e_inout(prog(t, T["mas"], T["mancar"])))
        return self.tf(t)


def lento_k(t, T):
    """0..1: câmera lenta LIGADA (selo e moldura âmbar só aqui): da desaceleração até o fim do congelamento
    que fecha cada câmera lenta; apaga antes das outras fitas ("Diferença") e antes do cartão ("avaliação")."""
    return max(prog(t, T["camera"], T["camera"] + 0.18) * (1 - prog(t, T["diferenca"] - 0.22, T["diferenca"] - 0.02)),
               prog(t, T["mancar"], T["mancar"] + 0.18) * (1 - prog(t, T["avaliacao"] - 0.22, T["avaliacao"] - 0.02)))


# ------------------------------------------------------------------ fundo e efeitos de "replay" (cópias do piloto)
def fundo_cl(cv, t):
    def d(c):
        sh = skia.GradientShader.MakeRadial(skia.Point(W / 2, H * 0.42 + 60), H * 0.78, [_c("#17384C"), _c(BG_OUT)])
        c.drawRect(skia.Rect(0, 0, W, H + 120), paint("#17384C", shader=sh))
    _blit(cv, _img("fundo", W, H + 120, d), 0, -60 + 40 * math.sin(t * 0.3))
    for x, y, v, r, a in PART:
        yy = (y - v * t * 6) % H
        cv.drawCircle(x + 8 * math.sin(t * 0.5 + y), yy, r, paint("#BFE3FF", int(a)))


def monitor_fundo(cv):
    def d(c):
        _rel(c)
        c.drawRect(CENA, paint("#FFFFFF", 9))
        sh = skia.GradientShader.MakeRadial(skia.Point(540, 760), 780, [_c("#000000", 0), _c("#000000", 0), _c("#000000", 85)],
                                            [0.0, 0.55, 1.0])
        c.drawRect(CENA, paint("#000000", 255, shader=sh))
    _blit(cv, _img("monitor", CENA.width(), CENA.height(), d), CENA.left(), CENA.top())


def escurece(cv, a):
    _blit(cv, _img("escuro", CENA.width(), CENA.height(), lambda c: c.clear(_c("#08121B", 255))), CENA.left(), CENA.top(), a)


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
        _blit(cv, img, CENA.left(), CENA.top(), 0.48 * forte * (1 - k / 0.1))


# ------------------------------------------------------------------ painel do replay (cronômetro + velocidade)
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
    """◀◀ ou ▶▶ desenhado (a fonte não tem o símbolo)."""
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


HUD_X, HUD_Y = 790, 1170                                         # centro do relógio (sobre o piso, à direita)
POP_C = (775, 560)                                               # onde o "0,25×" grande aparece (lado vazio do corredor)


def _chip_hud_c(s):
    _, w, _ = chip_dim(s)
    return HUD_X + 50 + w / 2, HUD_Y


def hud(t, T):
    """-> (rótulo ou "volta"/"avanca", apagado?, início do trecho)."""
    marcos = ((0.0, "1×", False), (T["volta"], "volta", False), (T["camera"], "0,25×", False),
              (T["manca"], "0,25×", True), (T["diferenca"], "1×", False), (T["mas"], "volta", False),
              (T["mancar"], "0,25×", False), (T["desnivel"], "0,25×", True), (T["avaliacao"], "1×", True),
              (T["trunfo"], "1×", False), (T["rapido"], "avanca", False), (T["procure"], "1×", False))
    atual = marcos[0]
    for m in marcos:
        if t >= m[0]:
            atual = m
    return atual[1], atual[2], atual[0]


def painel(cv, t, T, F, a):
    if a <= 0:
        return
    s, apagado, t0 = hud(t, T)
    relogio(cv, HUD_X, HUD_Y, 34, a, F.relogio(t) * 2 * math.pi)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(HUD_X - 7, HUD_Y - 50, HUD_X + 7, HUD_Y - 38), 3, 3), paint(OURO, int(255 * a)))
    if s in ("volta", "avanca"):
        _setas(cv, HUD_X + 52, HUD_Y, a * (0.75 + 0.25 * math.sin(t * 18)), 1.25, s == "avanca")
        return
    if apagado:
        chip_c(cv, s, *_chip_hud_c(s), a, dim=0.4)
        return
    hx, hy = _chip_hud_c(s)
    k = t - t0
    if s == R_LENTA and t0 == T["camera"] and k < 0.75:           # "0,25×" grande, que voa para o painel
        cx, cy = POP_C
        if k < 0.32:
            chip_c(cv, s, cx, cy, a, esc=2.5 * e_back(clamp(k / 0.16)))
        else:
            v = e_inout(prog(k, 0.32, 0.75))
            chip_c(cv, s, lerp(cx, hx, v), lerp(cy, hy, v), a, esc=lerp(2.5, 1.0, v))
        return
    pop = 1 + 0.6 * (1 - e_out(prog(t, t0, t0 + 0.3))) if t0 > 0 else 1.0
    chip_c(cv, s, hx, hy, a, esc=pop)


# ------------------------------------------------------------------ marcações do comentarista
def circulo_mao(cv, cx, cy, rx, ry, k, a, larg=7):
    """(cópia do piloto) Círculo dourado traçado à mão."""
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


def ponto_ouro(cv, x, y, a, r=13):
    if a <= 0:
        return
    cv.drawCircle(x, y, r + 10, paint(OURO, int(90 * a), blur=10))
    cv.drawCircle(x, y, r, paint(OURO, int(255 * a)))
    cv.drawCircle(x, y, r, paint(FUNDO_CARTAO, int(255 * a), "stroke", 3))


def desenha_trilha(cv, pts, a, s, k=1.0):
    """(cópia do piloto) Pontilhado dourado; `k`: fração desenhada a partir do primeiro ponto."""
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
    if k < 0.999:
        sombra = _trim(paint("#000000", int(60 * a), "stroke", 10.0 / s, blur=3.0 / s), k)
        cv.drawPath(p, sombra)
        meas = skia.PathMeasure(p, False)
        seg = skia.Path()
        meas.getSegment(0, meas.getLength() * max(0.002, k), seg, True)
        cv.drawPath(seg, pt)
        return
    cv.drawPath(p, paint("#000000", int(60 * a), "stroke", 10.0 / s, blur=3.0 / s))
    cv.drawPath(p, pt)


def pontos_trilha(tf, tau0, manca=1.0, ph=PH0, gx=GX):
    """A trilha do ponto da cabeça, do instante de filme tf para trás até tau0, riscada como a pena de um
    gráfico: cada instante passado fica K px mais à DIREITA. Começa na cabeça (o ponto mais novo)."""
    pts = []
    tau = tf
    while tau > tau0:
        x, y = cabeca_em(tau, manca, ph, gx)
        pts.append((x + K_TRILHA * (tf - tau), y))
        tau -= 0.004
    x, y = cabeca_em(tau0, manca, ph, gx)
    pts.append((x + K_TRILHA * (tf - tau0), y))
    return pts


def ponta_seta(cv, x, y, ang, tam, cor, a):
    p = skia.Path()
    p.moveTo(x + tam * math.cos(ang), y + tam * math.sin(ang))
    p.lineTo(x + tam * 0.75 * math.cos(ang + 2.45), y + tam * 0.75 * math.sin(ang + 2.45))
    p.lineTo(x + tam * 0.75 * math.cos(ang - 2.45), y + tam * 0.75 * math.sin(ang - 2.45))
    p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))


def tracejada(cv, x0, y0, x1, y1, cor, a, larg, traco, vao, k=1.0, fase=0.0):
    if a <= 0 or k <= 0:
        return
    pt = paint(cor, int(255 * a), "stroke", larg)
    pt.setStrokeCap(skia.Paint.kButt_Cap)
    pt.setPathEffect(skia.DashPathEffect.Make([traco, vao], fase))
    cv.drawLine(x0, y0, lerp(x0, x1, k), lerp(y0, y1, k), paint("#000000", int(90 * a), "stroke", larg + 4, blur=2))
    cv.drawLine(x0, y0, lerp(x0, x1, k), lerp(y0, y1, k), pt)


def marcas_cintura(cv, P, s, a_pts, k_lin, k_hor, brilho):
    """Os dois pontos dourados nas pontas do elástico (por FORA da roupa), a linha tracejada que os liga e a
    horizontal AZUL-CLARA (contorno escuro: contrasta com o elástico marfim e com a parede) que sai do ponto
    mais alto (o lado direito dela) e passa dos dois pontos: o desnível é um SINAL, sem medida."""
    if a_pts <= 0:
        return
    pe, pd = pontos_cintura(P)
    if brilho > 0 and k_hor > 0:                                   # o triangulinho entre as duas linhas
        tri = _poly([pd, pe, (pe[0], pd[1])])
        cv.drawPath(tri, paint(OURO, int(150 * brilho * a_pts)))
    if k_hor > 0:
        x0, x1 = pd[0] + 60.0 / s, pe[0] - 60.0 / s
        tracejada(cv, x0, pd[1], x1, pd[1], "#0B1824", a_pts * 0.9, 9.0 / s, 18.0 / s, 9.0 / s, k_hor)
        tracejada(cv, x0, pd[1], x1, pd[1], AZUL_CL, a_pts, 5.0 / s, 18.0 / s, 9.0 / s, k_hor)
    if k_lin > 0:
        tracejada(cv, pd[0], pd[1], pe[0], pe[1], OURO, a_pts, 6.0 / s, 16.0 / s, 10.0 / s, k_lin)
    for x, y in (pe, pd):
        ponto_ouro(cv, x, y, a_pts * e_back(clamp(a_pts)), r=11)


def etiqueta(cv, s, x, y, a, esc=1.0, tam=44):
    """Carimbo dourado (tag) centrado em (x, y). -> meia largura (para o fio)."""
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    if a <= 0:
        return lw / 2 + 20
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 20, -tam * 0.68, lw / 2 + 20, tam * 0.62), 12, 12)
    cv.drawRRect(rr, paint("#000000", int(90 * a), blur=8))
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(215 * a)))
    cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 5))
    cv.drawString(s, -lw / 2, tam * 0.36, f, paint(OURO, int(255 * a)))
    cv.restore()
    return lw / 2 + 20


def fio(cv, x0, y0, x1, y1, a, k=1.0):
    """Fio fino do carimbo até o detalhe."""
    if a <= 0 or k <= 0:
        return
    x, y = lerp(x0, x1, k), lerp(y0, y1, k)
    cv.drawLine(x0, y0, x, y, paint("#000000", int(80 * a), "stroke", 6, blur=2))
    cv.drawLine(x0, y0, x, y, paint(MARFIM, int(235 * a), "stroke", 3))
    if k >= 0.99:
        cv.drawCircle(x1, y1, 6, paint(MARFIM, int(255 * a)))


def estetoscopio(cv, x, y, esc, a):
    """(cópia do piloto) Selo branco e calmo: estetoscópio desenhado (forma, sem texto)."""
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


def olho(cv, x, y, esc, a, abre=1.0):
    """(cópia do cf_escoliose) Olho estilizado: amêndoa dourada com íris redonda; `abre` = 0,06 é fechado."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    L, hh = 82, 46 * max(0.06, abre)
    p = skia.Path(); p.moveTo(-L, 0)
    p.cubicTo(-L * 0.45, -hh * 1.3, L * 0.45, -hh * 1.3, L, 0)
    p.cubicTo(L * 0.45, hh * 1.3, -L * 0.45, hh * 1.3, -L, 0); p.close()
    am = a * clamp((abre - 0.06) / 0.3)                           # a amêndoa some ao fechar (só fica a pálpebra)
    cv.drawPath(p, paint(OURO, int(90 * a), blur=16))
    cv.drawPath(p, paint("#FFF6DD", int(255 * am)))
    cv.save(); cv.clipPath(p, skia.ClipOp.kIntersect, True)
    cv.drawCircle(0, 0, 31, paint(OURO, int(255 * am)))
    cv.drawCircle(0, 0, 31, paint("#9C7A2A", int(255 * am), "stroke", 4))
    cv.drawCircle(0, 0, 13, paint("#1B2430", int(255 * am)))
    cv.drawCircle(-9, -10, 6, paint("#FFFFFF", int(230 * am)))
    cv.restore()
    cv.drawPath(p, paint(OURO, int(255 * am), "stroke", 6))
    if abre < 0.5:                                                # pálpebra fechada: arco grosso + cílios longos para baixo
        af = 1 - abre * 2
        lid = skia.Path(); lid.moveTo(-L, 0); lid.quadTo(0, 30, L, 0)
        pt = paint(OURO, int(255 * a * af), "stroke", 11); pt.setStrokeCap(skia.Paint.kRound_Cap)
        cv.drawPath(lid, paint("#000000", int(110 * a * af), "stroke", 17, blur=3))
        cv.drawPath(lid, pt)
        for dx in (-50, -18, 18, 50):
            y0 = 15 * (1 - (dx / L) ** 2) + 2
            pc = paint(OURO, int(255 * a * af), "stroke", 8); pc.setStrokeCap(skia.Paint.kRound_Cap)
            cv.drawLine(dx, y0, dx * 1.18, y0 + 26, pc)
    cv.restore()


# ------------------------------------------------------------------ calendário de parede (crescer = TEMPO, nunca altura)
CAL_QUAD = ((95.0, 640.0), (285.0, 665.0), (285.0, 845.0), (95.0, 870.0))       # TL, TR, BR, BL (na parede esquerda)
FOLHA_QUAD = ((380.0, 545.0), (438.0, 551.0), (438.0, 621.0), (380.0, 627.0))    # a folha "lá na frente"


def _persp(quad, w, h):
    m = skia.Matrix()
    m.setPolyToPoly([skia.Point(0, 0), skia.Point(w, 0), skia.Point(w, h), skia.Point(0, h)],
                    [skia.Point(*q) for q in quad])
    return m


def calendario(cv, a, n_folhas):
    """Calendário de parede SEM número (cópia adaptada do cf_fratura_cola/piloto, cabeçalho azul-claro: nada
    de vermelho), em perspectiva na parede. `n_folhas`: quantas folhas já viraram (a fração anima a virada)."""
    if a <= 0:
        return
    q = CAL_QUAD
    cv.drawPath(_poly([(x + 8, y + 10) for x, y in q]), paint("#000000", int(90 * a), blur=10))
    cv.save(); cv.concat(_persp(q, 96, 92))
    corpo = skia.RRect.MakeRectXY(skia.Rect(0, 0, 96, 92), 10, 10)
    cv.drawRRect(corpo, paint("#EEF3F8", int(255 * a)))
    cv.save(); cv.clipRRect(corpo, True)
    cv.drawRect(skia.Rect(0, 0, 96, 24), paint(AZUL_CL, int(255 * a)))
    cv.restore()
    for xx in (24, 72):
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(xx - 4, -8, xx + 4, 10), 3, 3), paint("#5E7186", int(255 * a)))
    for i in range(3):
        cv.drawLine(14, 42 + i * 16, 82, 42 + i * 16, paint("#9AA8B5", int(200 * a), "stroke", 4))
    fase_ = n_folhas - math.floor(n_folhas)
    if fase_ > 0.001:                                              # a folha de cima levanta e vira
        cv.save(); cv.translate(0, 24); cv.scale(1, 1 - fase_)
        cv.drawRect(skia.Rect(0, 0, 96, 68), paint("#FFFFFF", int(200 * a * (1 - fase_))))
        cv.drawLine(14, 18, 82, 18, paint("#9AA8B5", int(150 * a * (1 - fase_)), "stroke", 4))
        cv.restore()
        cv.drawRect(skia.Rect(2, 24 - 10 * math.sin(math.pi * fase_), 94, 26), paint("#FFFFFF", int(160 * a * math.sin(math.pi * fase_))))
    cv.drawRRect(corpo, paint("#9AA8B5", int(255 * a), "stroke", 2))
    cv.restore()


def folha_frente(cv, a, esc):
    """A folha lá na frente (no fim do corredor = mais adiante no tempo), em perspectiva, sem número."""
    if a <= 0:
        return
    q = FOLHA_QUAD
    cx = sum(x for x, _ in q) / 4; cy = sum(y for _, y in q) / 4
    cv.save(); cv.translate(cx, cy); cv.scale(esc, esc); cv.translate(-cx, -cy)
    cv.drawPath(_poly([(x + 4, y + 6) for x, y in q]), paint("#000000", int(80 * a), blur=6))
    cv.save(); cv.concat(_persp(q, 60, 76))
    corpo = skia.RRect.MakeRectXY(skia.Rect(0, 0, 60, 76), 7, 7)
    cv.drawRRect(corpo, paint("#EEF3F8", int(255 * a)))
    cv.save(); cv.clipRRect(corpo, True)
    cv.drawRect(skia.Rect(0, 0, 60, 16), paint(AZUL_CL, int(255 * a)))
    cv.restore()
    for i in range(3):
        cv.drawLine(9, 32 + i * 12, 51, 32 + i * 12, paint("#9AA8B5", int(200 * a), "stroke", 3))
    cv.drawRRect(corpo, paint("#9AA8B5", int(255 * a), "stroke", 2))
    cv.restore()
    cv.restore()


def estrela(cv, x, y, r, a, giro=0.0):
    if a <= 0:
        return
    p = skia.Path()
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5 + giro
        rr = r if i % 2 == 0 else r * 0.45
        (p.moveTo if i == 0 else p.lineTo)(x + rr * math.cos(ang), y + rr * math.sin(ang))
    p.close()
    cv.drawCircle(x, y, r * 2.0, paint(OURO, int(110 * a), blur=14))
    cv.drawPath(p, paint(OURO, int(255 * a)))
    cv.drawPath(p, paint("#8A6512", int(200 * a), "stroke", 2))


def pino(cv, x, y, a, k):
    """Alfinete de mural dourado espetado na folha (cai de cima e crava)."""
    if a <= 0:
        return
    dy = -60 * (1 - e_out(k))
    cv.save(); cv.translate(x, y + dy)
    cv.drawOval(skia.Rect(-6, 10, 10, 16), paint("#000000", int(90 * a), blur=3))
    cv.drawLine(0, 0, 3, 12, paint("#C9D3DC", int(255 * a), "stroke", 3))
    cv.drawCircle(0, -4, 12, paint(OURO, int(255 * a)))
    cv.drawCircle(0, -4, 12, paint("#8A6512", int(255 * a), "stroke", 2.5))
    cv.drawCircle(-4, -8, 3.5, paint("#FFF4CC", int(230 * a)))
    cv.restore()


def n_folhas(t, T):
    """Folhas que viraram: 3, calmas, de "crescer" até "prever"; 8, depressa, no "rápido"."""
    return (3 * prog(t, T["crescimento"] + 0.05, T["prever"] - 0.05)
            + 8 * prog(t, T["rapido"], T["procure"] - 0.05))


def fim_cta(t, T):
    """Tudo o que é da cena parada (calendário, folha, estrela, pino, estetoscópio) sai antes da CTA."""
    return 1 - prog(t, T["manda"] - 0.4, T["manda"] - 0.1)


# ------------------------------------------------------------------ o que a fita mostra (corredor + menina + marcas)
OBTURADOR = {"play": 0.04, "volta": 0.03}                        # s de VÍDEO (curto: o balanço da cabeça já se nota no 1×)
N_AMOSTRAS = 5
CAIXA = skia.Rect(GX - 260, 420, GX + 260, 1220)


def amostras_borrao(t, F):
    """(cópia adaptada do piloto) Instantes que entram no borrão do 1× e da volta: nunca antes de t = 0 (o
    quadro 0 sai nítido) e nunca atravessando congelamento."""
    obt = OBTURADOR.get(F.tipo(t))
    if not obt or t >= F.T["trunfo"]:
        return [t]
    out = [t]
    for i in range(1, N_AMOSTRAS):
        tg = t - obt * i / (N_AMOSTRAS - 1)
        if tg < 0 or F.tipo(tg) == "congela":
            break
        out.append(tg)
    return out


def marcas(t, T, F, cheio=False):
    """Alfas e progressos das marcações (1ª câmera lenta até "Diferença"; 2ª câmera lenta + cartão até "trunfo").
    `cheio`: sem o esmaecer do "não no olho" (para a miniatura que mostra a diferença que aumenta)."""
    m = dict(a_pt=0.0, tau0=None, k_rev=1.0, a_circ=0.0, k_circ=0.0, a_cint=0.0, k_lin=0.0, k_hor=0.0, brilho=0.0)
    if T["repara"] <= t < T["diferenca"]:
        fim = 1 - prog(t, T["diferenca"] - 0.25, T["diferenca"] - 0.02)
        m["a_pt"] = prog(t, T["repara"], T["repara"] + 0.12) * fim
        m["tau0"] = -1e9                                           # a janela inteira (fundo-raso-fundo)
        m["k_rev"] = e_out(prog(t, T["repara"], T["repara"] + 0.45))
        if t >= T["manca"] + 0.05:
            m["a_circ"], m["k_circ"] = fim, prog(t, T["manca"] + 0.05, T["manca"] + 0.4)
        if t >= T["quadril"]:
            m["a_cint"] = prog(t, T["quadril"], T["quadril"] + 0.15) * fim
            m["k_lin"] = e_out(prog(t, T["quadril"] + 0.1, T["quadril"] + 0.45))
            m["k_hor"] = e_out(prog(t, T["desnivelado"], T["desnivelado"] + 0.35))
            m["brilho"] = math.sin(math.pi * prog(t, T["desnivelado"] + 0.3, T["desnivelado"] + 0.95))
    elif T["mancar"] <= t < T["trunfo"]:
        fim = 1 - (0.0 if cheio else 0.6) * prog(t, T["olho"], T["olho"] + 0.3)   # "não no olho": as marcas esmaecem
        m["a_pt"] = prog(t, T["mancar"], T["mancar"] + 0.12) * fim
        m["tau0"] = -1e9
        m["k_rev"] = e_out(prog(t, T["mancar"], T["mancar"] + 0.3))
        if t >= T["desnivel"] + 0.05:
            m["a_circ"], m["k_circ"] = fim, prog(t, T["desnivel"] + 0.05, T["desnivel"] + 0.35)
        if t >= T["desnivel"]:
            m["a_cint"] = prog(t, T["desnivel"], T["desnivel"] + 0.1) * fim
            m["k_lin"] = e_out(prog(t, T["desnivel"] + 0.05, T["desnivel"] + 0.3))
            m["k_hor"] = e_out(prog(t, T["desnivel"] + 0.25, T["desnivel"] + 0.5))
            m["brilho"] = math.sin(math.pi * prog(t, T["desnivel"] + 0.45, T["desnivel"] + 1.0))
    return m


def vale_mundo(tf, manca=1.0):
    """O vale fundo ANTERIOR da trilha (a pisada esquerda de um passo atrás), no referencial da cena: fica
    longe da cabeça, entre o raso e a borda (a cabeça, congelada, está no vale fundo de agora)."""
    x, y = cabeca_em(BOT_ANT, manca)
    return x + K_TRILHA * (tf - BOT_ANT), y


def vale(F, cam):
    """O vale circulado, na tela."""
    return na_tela(cam, *vale_mundo(F.tf_fz))


def conteudo_corrida(cv, t, T, F, limpo=False, manca=1.0, cheio=False):
    """A fita da corrida no instante t (corredor, menina, trilha e marcas), em coordenadas de tela."""
    tf = F.tf(t); tipo = F.tipo(t)
    cam = camera(t, T)
    if tipo == "volta" and not limpo:                              # tremidinha de fita voltando
        j = math.sin(t * 97) * 3 + math.sin(t * 41) * 2
        cam = (cam[0], cam[1] + j, cam[2])
    s = cam[0]
    cv.save(); aplica(cv, cam)
    corredor(cv, VZ * tf)
    P = pose_corrida(tf, manca)
    sombra_crianca(cv, P)
    ams = amostras_borrao(t, F) if not limpo else [t]
    if len(ams) == 1:
        desenha_crianca(cv, P)
    else:                                                          # borrão de movimento: média das poses no obturador
        cv.saveLayer(CAIXA, None)
        for k, tg in enumerate(reversed(ams)):
            Pk = pose_corrida(F.tf(tg), manca)
            if k == 0:
                desenha_crianca(cv, Pk)
            else:
                cv.saveLayer(CAIXA, _alfa(1.0 / (k + 1)))
                desenha_crianca(cv, Pk)
                cv.restore()
        cv.restore()
    m = marcas(t, T, F, cheio)
    if m["tau0"] is not None and m["a_pt"] > 0:
        tau0 = max(m["tau0"], tf - JAN_TRILHA)
        desenha_trilha(cv, pontos_trilha(tf, tau0, manca), m["a_pt"], s, m["k_rev"])
    if m["a_circ"] > 0:
        vx, vy = vale_mundo(tf, manca)
        circulo_mao(cv, vx, vy + 4, 46, 34, m["k_circ"], m["a_circ"], larg=6.0 / s * 1.2)
    marcas_cintura(cv, P, s, m["a_cint"], m["k_lin"], m["k_hor"], m["brilho"])
    if m["a_pt"] > 0:
        ponto_ouro(cv, *ponto_cabeca(P), m["a_pt"] * e_back(clamp(m["a_pt"])), r=11)
    cv.restore()
    return cam, P


T_MENINA_PARADA = 0.22                                           # s depois do "Ela": o cartão (x <= 569) já saiu da frente dela


def conteudo_parada(cv, t, T, F):
    """A cena parada: a menina de costas, calma, junto do calendário de parede (sem corrida, sem replay)."""
    corredor(cv, Z_PARADA, portas_esq=False)
    P = pose_parada(t)
    # ela só aparece depois que o cartão grande (que vai para o canto) saiu de cima dela: nunca meia menina
    # (pernas sob o cartão) enquanto ele passa
    a_g = prog(t, T["trunfo"] + T_MENINA_PARADA, T["trunfo"] + T_MENINA_PARADA + 0.2)
    if a_g > 0:
        if a_g < 1:
            cv.saveLayer(CENA, _alfa(a_g))
        sombra_crianca(cv, P)
        desenha_crianca(cv, P)
        if a_g < 1:
            cv.restore()
    fc = fim_cta(t, T)
    calendario(cv, fc, n_folhas(t, T))
    # "prever": a trilha dourada sai da folha de hoje e vai até uma folha lá na frente; "a diferença": ela
    # surge e a estrelinha acende; "planejar": o pino crava (sozinho, na palavra dele)
    t_tr, t_dp = T["prever"] - 0.05, T["diferenca_prever"]
    k_tr = e_inout(prog(t, t_tr, t_dp))
    if k_tr > 0 and fc > 0:
        p = skia.Path(); p.moveTo(292, 690); p.quadTo(335, 560, 376, 596)
        pt = paint(OURO, int(255 * fc), "stroke", 7); pt.setPathEffect(skia.DashPathEffect.Make([1.0, 15.0], 0))
        meas = skia.PathMeasure(p, False); seg = skia.Path()
        meas.getSegment(0, meas.getLength() * k_tr, seg, True)
        cv.drawPath(seg, paint("#000000", int(60 * fc), "stroke", 10, blur=3))
        cv.drawPath(seg, pt)
    a_f = prog(t, t_dp - 0.2, t_dp) * fc
    folha_frente(cv, a_f, e_back(prog(t, t_dp - 0.2, t_dp + 0.1)))
    a_e = prog(t, t_dp, t_dp + 0.15) * fc
    if a_e > 0:
        tw = 1 + 0.12 * math.sin(t * 6)
        estrela(cv, 409, 590, 17 * tw * e_back(prog(t, t_dp, t_dp + 0.3)), a_e, giro=0.2 * math.sin(t * 2))
    if t >= T["planejar"]:
        pino(cv, 409, 553, prog(t, T["planejar"], T["planejar"] + 0.08) * fc, prog(t, T["planejar"], T["planejar"] + 0.22))
    return P


# ------------------------------------------------------------------ as outras fitas (é comum, e não dá sintoma)
MINIS = ((215.0, 918.0), (540.0, 918.0), (865.0, 918.0))
MW, MH = 300.0, 270.0
OUTRAS = ((1, 0.12, 0.35), (2, 0.47, 0.9), (3, 0.81, 1.6))       # (variante do corredor, fase, z inicial)


def conteudo_outra(cv, i, tt):
    """Outra fita: outra criança de costas correndo em 1×, trilha de ondas IGUAIS e cintura nivelada."""
    iv, ph, z0 = OUTRAS[i]
    cam = (1.35, GX_OUTRAS, 860.0)
    cv.save(); aplica(cv, cam)
    corredor(cv, z0 + VZ * tt, iv)
    P = pose_corrida(tt, manca=0.0, ph=ph, gx=GX_OUTRAS)
    sombra_crianca(cv, P)
    desenha_crianca(cv, P, ROUPAS_OUTRAS[i])
    desenha_trilha(cv, pontos_trilha(tt, tt - 0.6, manca=0.0, ph=ph, gx=GX_OUTRAS), 1.0, 0.5)
    ponto_ouro(cv, *ponto_cabeca(P), 1.0, r=18)
    cv.restore()


def _map_rect(cv, r):
    """Leva o referencial da CENA para o retângulo r (mesma proporção)."""
    cv.translate(r.left(), r.top())
    cv.scale(r.width() / CENA.width(), r.height() / CENA.height())
    cv.translate(-CENA.left(), -CENA.top())


def _lerp_rect(a, b, k):
    return skia.Rect(lerp(a.left(), b.left(), k), lerp(a.top(), b.top(), k), lerp(a.right(), b.right(), k),
                     lerp(a.bottom(), b.bottom(), k))


def _moldura(cv, r, a, brilho=0.0):
    if a <= 0:
        return
    borda = skia.RRect.MakeRectXY(skia.Rect(r.left() - 9, r.top() - 9, r.right() + 9, r.bottom() + 9), 14, 14)
    sombra = skia.RRect.MakeRectXY(skia.Rect(r.left() - 3, r.top() + 1, r.right() + 15, r.bottom() + 19), 14, 14)
    cv.drawRRect(sombra, paint("#000000", int(110 * a), blur=12))
    cv.drawRRect(borda, paint("#F4F7FA", int(255 * a)))
    if brilho > 0:
        cv.drawRRect(borda, paint(OURO, int(255 * a * brilho), "stroke", 6))


def outras_fitas(cv, t, T):
    t0 = T["diferenca"]
    # no ◀◀ as outras fitas somem ANTES que a miniatura (que cresce até a cena toda) chegue às cabeças das
    # crianças delas (~0,07 s): nada de pernas de criança sobrando embaixo do quadro que cresce
    fim = 1 - prog(t, T["mas"], T["mas"] + 0.06)
    if fim <= 0:
        return
    for i, (cx, cy) in enumerate(MINIS):
        ti = t0 + 0.32 + 0.26 * i
        if t < ti:
            continue
        k = prog(t, ti, ti + 0.32)
        esc = max(0.01, e_back(k))
        a = prog(t, ti, ti + 0.06) * fim
        giro = (-2.5, 1.5, -1.5)[i] * e_out(k)
        cv.save(); cv.translate(cx, cy + (1 - e_out(k)) * 40); cv.rotate(giro); cv.scale(esc, esc)
        r = skia.Rect(-MW / 2, -MH / 2, MW / 2, MH / 2)
        _moldura(cv, r, a, 1 - prog(t, ti + 0.1, ti + 0.6))
        dentro = skia.RRect.MakeRectXY(r, 8, 8)
        cv.save(); cv.clipRRect(dentro, True)
        if a < 1:
            cv.saveLayer(r, _alfa(a))
        _map_rect(cv, r)
        conteudo_outra(cv, i, t - t0 + 0.4 * i)
        if a < 1:
            cv.restore()
        cv.restore()
        cv.restore()


# ------------------------------------------------------------------ os quadros congelados como miniatura / cartão
MINI_TL = skia.Rect(320, 348, 760, 744)                          # o congelamento, no alto (as outras fitas embaixo)
CARTAO = skia.Rect(85, 437, 825, 1103)                           # o cartão de VT parado (avaliação)
MINI_TL2 = skia.Rect(56, 346, 276, 544)                          # o cartão guardado no canto (cena parada)


def imagem_congelada(t_ref, T, F, manca=1.0, cheio=False):
    chave = ("cong", round(t_ref, 3), round(manca, 3), cheio)
    if chave not in _CACHE:
        sf = skia.Surface(int(CENA.width()), int(CENA.height())); c = sf.getCanvas(); c.clear(_c(BG_OUT))
        c.translate(-CENA.left(), -CENA.top())
        conteudo_corrida(c, t_ref, T, F, limpo=True, manca=manca, cheio=cheio)
        _CACHE[chave] = sf.makeImageSnapshot()
    return _CACHE[chave]


MANCAS_AUMENTA = (1.0, 1.3, 1.6, 1.9)                            # "aumenta": o vale circulado afunda na miniatura


def imagem_aumenta(cv, t_ref, T, F, r, a, d):
    """A miniatura do congelamento com a manqueira crescendo (d = 0..1), em degraus que se fundem."""
    x = d * (len(MANCAS_AUMENTA) - 1)
    i = min(len(MANCAS_AUMENTA) - 2, int(x)); f = x - i
    _desenha_img(cv, imagem_congelada(t_ref, T, F, MANCAS_AUMENTA[i], True), r, a)
    if f > 0.001:
        _desenha_img(cv, imagem_congelada(t_ref, T, F, MANCAS_AUMENTA[i + 1], True), r, a * f)


def _desenha_img(cv, img, r, a=1.0):
    cv.drawImageRect(img, r, skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kNone), _alfa(a))


# ------------------------------------------------------------------ carimbos
MANCA_DY = 150.0                                                 # MANCA fica logo abaixo do vale circulado
DESN_XY = (715.0, 1040.0)                                        # DESNÍVEL NO QUADRIL: abaixo e à direita da cintura


def _pop(t, t0, dur=0.16, pico=1.2):
    """Pop curto (≤ 1,2×): nenhum carimbo sai da tela nem cobre o ponto que ele aponta."""
    return lerp(pico, 1.0, e_out(clamp((t - t0) / dur))) if t >= t0 else 1.0


def carimbos(cv, t, T, F, cam, P, a_glob=1.0):
    """MANCA (fio até o vale circulado) e DESNÍVEL NO QUADRIL (fio até o ponto alto da cintura)."""
    if a_glob <= 0:
        return
    if T["manca"] <= t < T["diferenca"]:
        fim = 1 - prog(t, T["diferenca"] - 0.25, T["diferenca"] - 0.02)
        t_m, t_d = T["manca"] + 0.08, T["desnivelado"] + 0.1
        fio_m, fio_d = T["manca"] + 0.2, T["desnivelado"] + 0.25
    elif T["mancar"] <= t < T["trunfo"]:
        fim = 1 - 0.6 * prog(t, T["olho"], T["olho"] + 0.3)
        t_m, t_d = T["mancar"] + 0.02, T["desnivel"] + 0.08
        fio_m, fio_d = T["desnivel"] + 0.15, T["desnivel"] + 0.3
    else:
        return
    fim *= a_glob
    vx, vy = vale(F, cam)
    s = cam[0]
    if t >= t_m:
        ym = vy + MANCA_DY
        etiqueta(cv, R_MANCA, vx, ym, prog(t, t_m, t_m + 0.08) * fim, _pop(t, t_m))
        if t >= fio_m:
            fio(cv, vx, ym - 44 * 0.68, vx, vy + 38 * s, fim, e_out(prog(t, fio_m, fio_m + 0.25)))
    if t >= t_d:
        dx, dy = DESN_XY
        hw = etiqueta(cv, R_DESNIVEL, dx, dy, prog(t, t_d, t_d + 0.08) * fim, _pop(t, t_d, pico=1.12), tam=42)
        if t >= fio_d:
            pd = na_tela(cam, *pontos_cintura(P)[1])
            fio(cv, dx - hw + 40, dy - 42 * 0.68, pd[0] + 8, pd[1] + 14 * s, fim, e_out(prog(t, fio_d, fio_d + 0.25)))


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


# ------------------------------------------------------------------ o monitor (tudo dentro da CENA)
EST_A = (935.0, 432.0, 1.35)                                     # estetoscópio: alto à direita
EST_B = (848.0, 600.0, 1.6)                                      # "procure avaliação": desce para perto dela
OLHO_XY, OLHO_ESC = (930.0, 805.0), 0.92
# "aumenta": o cartão volta grande e a manqueira afunda — no alto, ENTRE o canto e a menina em pé: nunca passa
# por cima dela (cabeça em x >= 600 a partir de y 585) nem do calendário (topo em y 628), que segue virando as folhas
MINI_TL3 = skia.Rect(172, 342, 472, 612)


def aumenta_g(t, T):
    """0..1: o cartão do congelamento volta grande ("Diferença que aumenta") e volta ao canto no "Procure"."""
    return (e_inout(prog(t, T["diferenca_rapido"] - 0.1, T["aumenta"]))
            * (1 - e_inout(prog(t, T["procure"], T["procure"] + 0.4))))


def monitor(cv, t, T, F):
    tipo = F.tipo(t)
    cv.save(); cv.clipRect(CENA, True)
    monitor_fundo(cv)
    cam, P = None, None
    if t < T["diferenca"]:
        cam, P = conteudo_corrida(cv, t, T, F)
    elif t < T["mas"]:                                             # o congelamento vai para o canto; entram as outras fitas
        escurece(cv, 0.86)
        outras_fitas(cv, t, T)
        k = e_inout(prog(t, T["diferenca"], T["diferenca"] + 0.35))
        r = _lerp_rect(CENA, MINI_TL, k)
        _moldura(cv, r, k)
        _desenha_img(cv, imagem_congelada(T["diferenca"] - 0.3, T, F), r)
    elif t < T["avaliacao"]:                                       # ◀◀: a miniatura volta a ocupar a cena
        k = e_inout(prog(t, T["mas"], T["mas"] + 0.28))
        if k < 1:
            escurece(cv, 0.86)
            outras_fitas(cv, t, T)
            r = _lerp_rect(MINI_TL, CENA, k)
            _moldura(cv, r, 1 - k)
            cv.save(); cv.clipRect(r, True); _map_rect(cv, r)
            cam, P = conteudo_corrida(cv, t, T, F, limpo=True)
            cv.restore()
            cam = None
        else:
            cam, P = conteudo_corrida(cv, t, T, F)
    elif t < T["trunfo"]:                                          # o cartão de VT parado
        escurece(cv, 0.86)
        k = e_inout(prog(t, T["avaliacao"], T["avaliacao"] + 0.35))
        r = _lerp_rect(CENA, CARTAO, k)
        # "exame": um aro dourado acende em volta do cartão (é o exame que mede, não o que se vê no vídeo)
        aro = math.sin(math.pi * prog(t, T["exame"], T["exame"] + 0.55)) if t < T["exame"] + 0.3 else 0.75
        aro *= 1 - prog(t, T["trunfo"] - 0.2, T["trunfo"])
        _moldura(cv, r, k, aro if t >= T["exame"] else 0.0)
        cv.save(); cv.clipRect(r, True); _map_rect(cv, r)
        cam_c, P_c = conteudo_corrida(cv, t, T, F, limpo=True)
        carimbos(cv, t, T, F, cam_c, P_c, 1 - prog(t, T["trunfo"] - 0.15, T["trunfo"]))
        cv.restore()
    else:                                                          # a cena parada (o cartão vai para o canto)
        a_p = prog(t, T["trunfo"], T["trunfo"] + 0.35)
        if a_p < 1:
            escurece(cv, 0.86)
            cv.saveLayer(CENA, _alfa(a_p))
        P = conteudo_parada(cv, t, T, F)
        if a_p < 1:
            cv.restore()
        k = e_inout(prog(t, T["trunfo"], T["trunfo"] + 0.45))
        r = _lerp_rect(CARTAO, MINI_TL2, k)
        # "Diferença que aumenta": a miniatura volta a 100 %, cresce, pulsa com aro âmbar e o vale afunda
        g = aumenta_g(t, T)
        if g > 0:                                                  # a cena parada escurece; o calendário segue aceso
            escurece(cv, 0.72 * g)
            calendario(cv, fim_cta(t, T), n_folhas(t, T))
        r = _lerp_rect(r, MINI_TL3, g)
        a_m = lerp(lerp(1.0, 0.5, k), 1.0, g) * fim_cta(t, T)
        d = e_inout(prog(t, T["aumenta"], T["rapido"] + 0.1))
        pulso = 0.6 + 0.4 * math.sin(max(0.0, t - T["aumenta"]) * 12) if t >= T["aumenta"] else 0.0
        _moldura(cv, r, a_m * lerp(0.8, 1.0, g))
        _desenha_img(cv, imagem_congelada(T["trunfo"] - 0.02, T, F), r, a_m)
        if d > 0:                                                  # as marcas voltam a 100 % e o vale afunda
            imagem_aumenta(cv, T["olho"] - 0.05, T, F, r, a_m * min(1.0, d * 4), d)
        if g > 0 and pulso > 0:
            borda = skia.RRect.MakeRectXY(skia.Rect(r.left() - 9, r.top() - 9, r.right() + 9, r.bottom() + 9), 14, 14)
            cv.drawRRect(borda, paint(AMBAR, int(255 * a_m * g * pulso), "stroke", 8))
    # o estetoscópio: acende na "avaliação", desce para perto dela e pulsa no "procure"; sai antes da CTA
    if t >= T["avaliacao"]:
        a_e = prog(t, T["avaliacao"], T["avaliacao"] + 0.2) * fim_cta(t, T) * (1 - aumenta_g(t, T))
        k = e_inout(prog(t, T["procure"], T["procure"] + 0.5))
        x, y = lerp(EST_A[0], EST_B[0], k), lerp(EST_A[1], EST_B[1], k)
        esc = lerp(EST_A[2], EST_B[2], k) * e_back(prog(t, T["avaliacao"], T["avaliacao"] + 0.3))
        if t >= T["procure"]:
            esc *= 1 + 0.18 * math.sin(math.pi * prog(t, T["procure"], T["procure"] + 0.4))
        estetoscopio(cv, x, y, esc, a_e)
    # o olho: aparece no começo da frase ("A diferença se mede"), FECHA no "olho" (e fica fechado), sai com o cartão
    if T["quem"] <= t < T["trunfo"] + 0.3:
        a_o = prog(t, T["quem"], T["quem"] + 0.15) * (1 - prog(t, T["trunfo"], T["trunfo"] + 0.3))
        abre = lerp(1.0, 0.06, e_inout(prog(t, T["olho"], T["olho"] + 0.3)))
        olho(cv, *OLHO_XY, OLHO_ESC * e_back(prog(t, T["quem"], T["quem"] + 0.3)), a_o, abre)
    # ELA AINDA CRESCE (junto do calendário)
    if t >= T["crescimento"]:
        a_c = prog(t, T["crescimento"], T["crescimento"] + 0.08) * fim_cta(t, T)
        etiqueta(cv, R_CRESCE, 312, 935, a_c, _pop(t, T["crescimento"], pico=1.12), tam=42)
    # efeitos de replay
    varredura(cv, t, lento_k(t, T))
    faixas_tracking(cv, t, {"volta": 1.0, "avanca": 0.35}.get(tipo, 0.0) * (0.0 if t >= T["manda"] - 0.3 else 1.0))
    if tipo == "volta":                                            # ◀◀ grande no canto (letreiro do videocassete)
        t0 = F.inicio_trecho(t)
        _setas(cv, 96, 410, (0.55 + 0.45 * (math.sin((t - t0) * 16) > -0.3)) * prog(t, t0, t0 + 0.06), 2.2, False)
    for t0, fo in ((T["manca"], 1.0), (T["desnivel"], 0.8)):
        flash(cv, t, t0, fo)
    cv.restore()
    return cam, P


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep, F):
    fundo_cl(cv, t)
    cam, P = monitor(cv, t, T, F)
    if cam is not None and t < T["avaliacao"]:
        carimbos(cv, t, T, F, cam, P)
    fim = 1 - prog(t, T["manda"] - 0.4, T["manda"] - 0.1)
    cantoneiras(cv, fim)
    painel(cv, t, T, F, fim)
    capa(cv, t, T["volta"], ep["gancho"][0], ep["gancho"][1])
    selo_lenta(cv, lento_k(t, T) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface_cl(cv, t, T, blocos, DESTAQUE)


# ------------------------------------------------------------------ interface (cópia do cf_comum, espaço maior na CTA)
def legenda_cl(cv, blocos, t, destaque, y_base=1395, tam=80):
    """(cópia do cf_comum.legenda) Igual, com o espaço entre palavras proporcional ao corpo: na CTA (92 px)
    o contorno + o pop da palavra recém-dita colavam "CURTA" em "NO"."""
    import re
    vivo = None
    for i, b in enumerate(blocos):
        ini = b[0]["t"] - 0.12
        fim = blocos[i + 1][0]["t"] - 0.12 if i + 1 < len(blocos) else b[-1]["t"] + b[-1]["d"] + 2.5
        if ini <= t < fim:
            vivo = b; break
    if not vivo:
        return
    esp = 26 if tam <= 80 else 36
    linhas, linha, lw = [], [], 0
    for p in vivo:
        w = larg_texto(p["tok"].upper(), F_BLACK, tam)
        if linha and lw + esp + w > 920:
            linhas.append(linha); linha, lw = [], 0
        linha.append((p, w)); lw += (esp if lw else 0) + w
    if linha:
        linhas.append(linha)
    entrada = e_out(clamp((t - (vivo[0]["t"] - 0.12)) / 0.15))
    alt = tam * 1.18
    y = y_base - (len(linhas) - 1) * alt / 2 + (1 - entrada) * 24
    for ln in linhas:
        total = sum(w for _, w in ln) + esp * (len(ln) - 1); x = CX - total / 2
        for p, w in ln:
            k = t - p["t"]; base = re.sub(r"[.,:;!?—]", "", p["tok"]).lower()
            dita = k >= -0.03; falando = p["t"] - 0.03 <= t <= p["t"] + p["d"] + 0.06
            cor, a = (OURO, 255) if falando else ((OURO if base in destaque else "#FFFFFF"), 255) if dita else ("#FFFFFF", 105)
            esc = 1.0 + (0.06 * (1 - e_out(clamp(k / 0.16))) if dita else 0.0)
            cv.save(); cv.translate(x + w / 2, y); cv.scale(esc, esc)          # pop pelo centro da palavra
            texto(cv, p["tok"].upper(), -w / 2, 0, F_BLACK, tam, cor, int(a * entrada), centro=False, contorno=12)
            cv.restore()
            x += w + esp
        y += alt


def interface_cl(cv, t, T, blocos, destaque):
    """(cópia do cf_comum.interface, sem `nota`) Legenda + identificação CFM + cartão final com a CTA."""
    t_cta = T["manda"] - 0.15
    if t < t_cta:
        legenda_cl(cv, blocos, t, destaque)
    if 3.0 <= t < t_cta:
        a = prog(t, 3.0, 3.6)
        texto(cv, SIG, CX, 1585, F_SEMI, 27, "#FFFFFF", int(200 * a))
        texto(cv, DISC, CX, 1620, F_REG, 23, "#FFFFFF", int(150 * a))
    if t >= t_cta:
        a = prog(t, t_cta, t_cta + 0.35)
        cv.drawRect(skia.Rect(0, 0, W, H), paint(BG_OUT, int(175 * a)))
        # a POSIÇÃO da legenda é do BLOCO, não do relógio: o cartão começa em "Manda" - 0,15 s, mas o bloco
        # anterior ("PROCURE AVALIAÇÃO.") ainda vale até "Manda" - 0,12 s; nesse quadro ele seguia vivo e saltava
        # para y 700 (em cima da cabeça dela). Agora ele fica embaixo, onde estava, até o bloco da CTA entrar.
        ini_cta = next((b[0]["t"] - 0.12 for b in blocos if any(abs(p["t"] - T["manda"]) < 1e-6 for p in b)), t_cta)
        if t < ini_cta:
            legenda_cl(cv, blocos, t, destaque)
        else:
            legenda_cl(cv, blocos, t, destaque, y_base=700, tam=92)
        aviao(cv, t, T["manda"] + 0.2)
        rr = skia.RRect.MakeRectXY(skia.Rect(150, 1060, 930, 1214), 28, 28)
        cv.drawRRect(rr, paint("#0B1824", int(230 * a))); cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 3))
        texto(cv, "Dr. Rafael Vargas · Médico ortopedista", CX, 1112, F_BLACK, 36, "#FFFFFF", int(255 * a))
        texto(cv, "CRM-SP 226103 · RQE 137901 · @rafaelvargasmd", CX, 1154, F_SEMI, 28, OURO, int(255 * a))
        texto(cv, DISC, CX, 1190, F_REG, 22, "#FFFFFF", int(170 * a))


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
    """(cópia do piloto) Fita correndo: cliques que aceleram + tom que desliza + chiado."""
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


def congelar():
    """(cópia do piloto) Tique seco + 'clac' grave curto."""
    SR = som.SR
    y = som.tick() * 1.0
    n = int(0.12 * SR); t = np.arange(n) / SR
    z = np.sin(2 * np.pi * np.cumsum(220 * np.exp(-t * 30) + 90) / SR) * som._env(n, 0.001, 0.03) * 0.5
    out = np.zeros(max(len(y), n)); out[:len(y)] += y; out[:n] += z
    return out


@functools.lru_cache(maxsize=None)
def _pisada_base(lenta):
    """Pisada de tênis na madeira: baque curto e abafado (na câmera lenta, mais grave e mais longo)."""
    SR = som.SR
    dur = 0.34 if lenta else 0.12
    n = int(dur * SR); t = np.arange(n) / SR
    rui = som._onepole_lp(som._noise(n, 31 if lenta else 21), 260 if lenta else 700)
    f0 = 58 if lenta else 105
    tom = np.sin(2 * np.pi * np.cumsum(f0 * (1 + 0.4 * np.exp(-t * 30))) / SR)
    y = rui * som._env(n, 0.003 if lenta else 0.0015, 0.12 if lenta else 0.04) * 2.2
    y += tom * som._env(n, 0.004 if lenta else 0.001, 0.14 if lenta else 0.05) * 0.55
    return tuple((y / (np.max(np.abs(y)) or 1.0) * 0.6).tolist())


def pisada():
    return np.array(_pisada_base(False))


def pisada_lenta():
    return np.array(_pisada_base(True))


@functools.lru_cache(maxsize=None)
def _folha_base():
    SR = som.SR
    n = int(0.16 * SR); t = np.arange(n) / SR
    rui = som._noise(n, 41)
    alto = rui - som._onepole_lp(rui, 1800)
    y = alto * som._env(n, 0.012, 0.05) * np.clip(1 - t / 0.16, 0, 1)
    return tuple((y / (np.max(np.abs(y)) or 1.0) * 0.4).tolist())


def folha():
    """'fft' suave de folha de calendário virando."""
    return np.array(_folha_base())


def palpebra():
    SR = som.SR
    n = int(0.08 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * 820 * t) * som._env(n, 0.002, 0.02) * 0.35


def janelas(T, F, dur):
    """Ganho da batida e da harmonia: a batida some na câmera lenta e volta com as outras fitas."""
    xs = np.arange(0, dur + 0.01, 0.01)
    gb = np.ones_like(xs); gh = np.ones_like(xs)
    for i, x in enumerate(xs):
        tp = F.tipo(x)
        gb[i] = {"play": 1.0, "lenta": 0.0, "congela": 0.45, "volta": 0.2, "avanca": 0.8}[tp]
        gh[i] = {"play": 1.0, "lenta": 0.8, "congela": 0.9, "volta": 0.55, "avanca": 0.8}[tp]
        if tp == "congela" and lento_k(x, T) > 0:
            gb[i] = 0.0
        if T["diferenca"] <= x < T["mas"]:
            gb[i], gh[i] = 1.0, 1.0
    k = np.ones(15) / 15
    gb = np.convolve(np.pad(gb, 7, mode="edge"), k, "valid"); gh = np.convolve(np.pad(gh, 7, mode="edge"), k, "valid")
    return xs, gb, gh


def _media_movel(x, w):
    n = len(x); off = (w - 1) // 2
    S = np.concatenate([[0.0], np.cumsum(x, dtype=np.float64)])
    i = np.arange(n)
    return (S[np.clip(i + off + 1, 0, n)] - S[np.clip(i + off - w + 1, 0, n)]) / w


def mixar_cl(voz, dur, eventos, T, F, ganho_trilha=0.40):
    """(cópia do piloto) Mesmo mix e ducking do som.mixar, com a trilha em duas partes e efeitos próprios."""
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


def pisadas(T, F):
    """Instantes (vídeo) em que cada pé pousa, só com o filme andando para a frente: o MESMO volume nos dois
    pés (a manqueira não vira efeito sonoro); e as pisadas leves das outras fitas."""
    out = []
    ant = None
    x = 0.0
    while x < T["trunfo"]:
        tipo = F.tipo(x); tf = F.tf(x)
        if ant is not None and tipo in ("play", "lenta") and ant[0] == tipo and 0 < tf - ant[1] < 0.2:
            if math.floor(2 * (tf / P_CICLO + PH0)) > math.floor(2 * (ant[1] / P_CICLO + PH0)):
                out.append((x, pisada_lenta if tipo == "lenta" else pisada, 0.55 if tipo == "lenta" else 0.5))
        ant = (tipo, tf)
        x += 1 / 240
    for i, (iv, ph, z0) in enumerate(OUTRAS):                      # as outras fitas
        ti = T["diferenca"] + 0.32 + 0.26 * i
        x = ti
        while x < T["mas"]:
            tt0, tt1 = x - T["diferenca"] + 0.4 * i, x + 1 / 240 - T["diferenca"] + 0.4 * i
            if math.floor(2 * (tt1 / P_CICLO + ph)) > math.floor(2 * (tt0 / P_CICLO + ph)):
                out.append((x, pisada, 0.2))
            x += 1 / 240
    return out


def sons(T, F):
    ev = [(t, nome, g) for t, nome, g in pisadas(T, F)]
    ev += [(T["volta"], lambda: rebobinar(T["camera"] - T["volta"]), 0.9),
           (T["camera"], "pop", 0.55), (T["repara"] + 0.03, "shimmer", 0.35),
           (T["manca"], congelar, 1.0), (T["manca"] + 0.02, lambda: som.whoosh(0.22, seed=12), 0.3),
           (T["quadril"], "shimmer", 0.3), (T["desnivelado"] + 0.1, "tick", 0.3),
           (T["diferenca"], "pop", 0.5)]
    ev += [(T["diferenca"] + 0.32 + 0.26 * i, "pop", 0.35) for i in range(3)]
    ev += [(T["mas"], lambda: rebobinar(T["mancar"] - T["mas"]), 0.85),
           (T["mancar"], "pop", 0.5), (T["mancar"] + 0.03, "shimmer", 0.22),
           (T["desnivel"], congelar, 0.85),
           (T["avaliacao"], lambda: som.whoosh(0.35, seed=14), 0.25), (T["avaliacao"] + 0.02, "ding", 0.45),
           (T["quem"], "shimmer", 0.22), (T["exame"], "ding", 0.22), (T["olho"] + 0.05, palpebra, 0.6),
           (T["trunfo"], lambda: som.whoosh(0.45, seed=15), 0.3), (T["trunfo"] + 0.05, "pop", 0.35),
           (T["crescimento"], "shimmer", 0.3)]
    dc = T["prever"] - 0.1 - (T["crescimento"] + 0.05)
    ev += [(T["crescimento"] + 0.05 + dc * (i + 0.5) / 3, folha, 0.55) for i in range(3)]
    ev += [(T["diferenca_prever"], "shimmer", 0.3), (T["planejar"] + 0.18, "tick", 0.35), (T["planejar"] + 0.2, "pop", 0.25),
           (T["diferenca_rapido"] - 0.05, lambda: som.whoosh(0.3, seed=16), 0.25), (T["aumenta"], "pop", 0.35),
           (T["rapido"], lambda: avancar(T["procure"] - T["rapido"]), 0.6)]
    nr = 8; dr = T["procure"] - 0.05 - T["rapido"]
    ev += [(T["rapido"] + dr * i / nr, folha, 0.35) for i in range(nr)]
    ev += [(T["procure"], "pop", 0.4), (T["procure"] + 0.02, "ding", 0.45), (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def tempos_previa(T, F):
    return (0.0, 0.5, 1.2, T["volta"] + 0.3, T["camera"] + 0.12, T["camera"] + 0.5, T["lenta"] + 0.4,
            T["repara"] + 0.15, T["repara"] + 0.5, T["manca"] - 0.1, T["manca"] + 0.12, T["manca"] + 0.45,
            T["quadril"] + 0.4, T["desnivelado"] + 0.5, T["desnivelado"] + 0.95, T["diferenca"] + 0.2,
            T["diferenca"] + 0.9, T["crianca"] + 0.3, T["sintoma"] + 0.3, T["mas"] + 0.12, T["mas"] + 0.27,
            T["mancar"] + 0.3, T["desnivel"] - 0.05, T["desnivel"] + 0.12, T["desnivel"] + 0.6, T["nitida"] + 0.3,
            T["avaliacao"] + 0.15, T["avaliacao"] + 0.5, T["quem"] + 0.3, T["exame"] + 0.2, T["olho"] + 0.4,
            T["trunfo"] + 0.2, T["trunfo"] + 0.6, T["crescimento"] + 0.3, T["prever"] + 0.1,
            T["diferenca_prever"] + 0.1, T["final"] + 0.2, T["planejar"] + 0.3, T["preciso"] + 0.2,
            T["diferenca_rapido"] + 0.1, T["aumenta"] + 0.25, T["rapido"] + 0.25, T["procure"] + 0.6,
            T["avaliacao2"] + 0.5, T["manda"] - 0.6, T["manda"] + 0.3, T["manda"] + 1.2, T["total"] - 1 / 30)


# ------------------------------------------------------------------ entrada única (réplica do cf_comum.fazer_render, com mix próprio)
def preparar(ep, tmp):
    roteiro = "\n".join(ep["roteiro"])
    voz_bruta, palavras = _voz.narrar(roteiro, _voz.RITMO_COMO_FUNCIONA, os.path.join(tmp, "voz"))
    voz_c, pal, tirado = comprimir(voz_bruta, palavras, respiro_cta=RESPIRO_CTA)
    pal = alinhar(pal, roteiro)
    T = ancoras(pal, ANCORAS)
    T["mas"] = T["mancar"] - MAS_ANTES                             # o 2º ◀◀ (a frase começa direto em "Mancar")
    print(f"{ep['id']}: silêncio cortado {tirado:.2f}s | duração final {T['total']:.2f}s")
    return voz_c, pal, T


def render(ep, mp4, tmp, previa=False):
    voz_c, pal, T = preparar(ep, tmp)
    blocos = montar_blocos(pal)
    F = Filme(T)

    def quadro_t(cv, t):
        quadro(cv, t, T, blocos, ep, F)

    if previa:
        return _previas(quadro_t, tempos_previa(T, F), tmp, ep["id"]), T["total"]
    wav = os.path.join(tmp, f"{ep['id']}_mix.wav")
    som.gravar_wav(wav, mixar_cl(voz_c, T["total"], sons(T, F), T, F, ganho_trilha=0.40))
    codificar(quadro_t, T["total"], wav, mp4)
    return mp4, T["total"]
