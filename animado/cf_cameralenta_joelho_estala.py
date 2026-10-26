# -*- coding: utf-8 -*-
"""CÂMERA LENTA (série nova, ao lado do COMO FUNCIONA) — "JOELHO FEZ “CREC”? / SÓ SOM OU ALERTA?".

Mesma mecânica do piloto (cf_cameralenta_ponta_pes): um REPLAY de TV. O lance de uma criança pequena brincando
de PULO DE SAPO passa em 1× (pousa, agacha, "crec", salta), a fita VOLTA e o MESMO pulo é revisto em CÂMERA
LENTA. A câmera lenta não procura o barulho: procura O QUE VEM JUNTO com ele.
  * fita 1 (piso emborrachado de parquinho): estala, o joelho estica INTEIRO no impulso (congelado, linha reta
    dourada colada à frente da perna) e ela segue pulando (▶▶ só no "seguiu pulando") -> carimbo "SÓ SOM". A
    explicação roda a 1×: o mesmo "crec" no "tendão", na "bolha" e no "corpo", que vira brilhos ("normal").
  * corte de fita -> fita 2 (piso de madeira): o MESMO "crec" vem com (1) a mão no joelho, (2) um joelho mais
    cheio (câmera 2, de frente) e (3) o joelho que TRAVA: ela levanta com os pés lado a lado, a perna de trás
    estica inteira e o joelho de perto bate num batente a ~35°, quica 2 vezes e fica dobrado, calcanhar no ar
    (a linha volta tracejada, seguindo a coxa além do joelho). Melhores momentos: as 3 miniaturas dos sinais +
    o estetoscópio, seguradas até a CTA e apagadas sob o texto dela.

v2 (revisão do leitor às cegas e do revisor): "Joelho do FILHO" na voz + proporções de criança pequena (coxa e
canela curtas, joelho roliço, tênis grande de velcro, meia colorida); "trava" redesenhado (subida de 0,62 s,
2 quiques visíveis, pés lado a lado, sem o arco do ângulo); linha do "inteirinho" tangente à perna; ▶▶ de 5,7 s
trocado por 1× com um acontecimento por palavra-chave; brilhos que não se juntam numa estrela; CTA sobre fundo
liso; escurecimento de 0,93; braço curto com cotovelo dobrado; "crec" a 1× no respiro antes do "Volta";
"Fenômenos normais do corpo" -> "Coisa normal do corpo".

Regras da série e do storyboard, todas aqui:
  * Selo CÂMERA LENTA SÓ com a câmera lenta ligada (0,25× ou congelamento dentro dela): "câmera" -> "seguiu" e
    "atenção" -> "aí". Nunca no 1×, no ◀◀, no ▶▶, no corte de fita ou na CTA.
  * O "crec" (som e arcos dourados) é IDÊNTICO nas duas fitas: o barulho não distingue nada.
  * Nada por dentro do joelho (sem bolha, tendão, osso ou lupa): o "crec" é desenhado POR FORA (arcos de "pop").
  * VERMELHO PROIBIDO: inchaço = contorno mais cheio na MESMA cor de pele; dor = mão no joelho; sem rosto.
  * Sem antes e depois: a perna que travou nunca aparece esticando depois; nada volta à fita 1 depois de
    "procure avaliação" (melhores momentos + estetoscópio seguram até a CTA).
  * O joelho que não mudou (câmera 2) e a perna que esticou não ganham rótulo nem cor de "certo".
  * Nada de ❚❚, barra de progresso, "PAUSA", timecode ou dígitos: congelar = flash + tique + chip esmaecido.
  * Nenhum texto além do `tela` (CÂMERA LENTA, 1×, 0,25×, SÓ SOM), do gancho e da interface.

O tempo do filme (`Filme.tf`) é separado do tempo do vídeo; a narração nunca para nem desacelera. A fita 1 é um
ciclo de pulo de sapo em função do tempo do filme; a fita 2 é uma coreografia presa às palavras-âncora (o
tempo do filme dela só move o ponteiro do cronômetro).

Helpers COPIADOS (não importados) de outras cenas, como manda o contrato: Filme, efeitos de replay, painel,
relogio (cf_andador), circulo_mao, estetoscopio, mix próprio e sons de fita (cf_cameralenta_ponta_pes);
joelho e tubo (cf_crianca_mancando); carimbo_ouro (cf_fratura_cola); brilhos (cf_alongamento, adaptado para
subir). A cena é PRESA ao roteiro pelas palavras-âncora (ANCORAS): roteiro sem elas = KeyError no render.
"""
import math
import os

import numpy as np
import skia

from . import som, voz as _voz
from .base import FPS, codificar, previas as _previas
from .cf_alongamento import (BG_OUT, CX, F_BLACK, H, OURO, PART, W, clamp, e_back, e_inout, e_out, lerp,
                             lerpc, paint, prog, texto)
from .cf_comum import alinhar, ancoras, capa, comprimir, interface, montar_blocos

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "joelho1": ("joelho", 1, False), "crec": ("crec", 1, False), "volta": ("volta", 1, False),
    "camera": ("câmera", 1, False), "lenta": ("lenta", 1, False), "so1": ("só", 1, False),
    "alerta": ("alerta", 1, False), "repara": ("repara", 1, False), "junto": ("junto", 1, False),
    "estalou": ("estalou", 1, False), "esticou": ("esticou", 1, False), "inteirinho": ("inteirinho", 1, False),
    "seguiu": ("seguiu", 1, False), "pulando": ("pulando", 1, False), "sem1": ("sem", 1, False),
    "inchaco": ("inchaço", 1, False), "so2": ("só", 2, False), "costuma": ("costuma", 1, False),
    "tendao": ("tendão", 1, False), "bolha": ("bolha", 1, False), "coisa": ("coisa", 1, False),
    "normal": ("normal", 1, False), "corpo": ("corpo", 1, False), "agora": ("agora", 1, False), "atencao": ("atenção", 1, False),
    "estalo": ("estalo", 1, False), "vem2": ("vem", 2, False), "dor2": ("dor", 2, False),
    "joelho2": ("joelho", 2, False), "incha": ("incha", 1, False), "trava": ("trava", 1, False),
    "estica": ("estica", 1, False), "ai": ("aí", 1, False), "sim": ("sim", 1, False),
    "procure": ("procure", 1, False), "avaliacao": ("avaliação", 1, False), "manda": ("manda", 1, False),
}
DESTAQUE = {"crec", "alerta", "junto", "inteirinho", "pulando", "dor", "inchaço", "som", "tendão", "gás",
            "normal", "atenção", "incha", "trava", "estica", "avaliação"}
RESPIRO_CTA = 1.6

# ------------------------------------------------------------------ paleta (sem vermelho)
PELE, PELE_LINHA = "#EFB194", "#B47258"
SHORT, SHORT_CL, SHORT_ESC, SHORT_LINHA = "#6A4C93", "#8D6DB8", "#4C346E", "#2B1C42"
FRISO = "#F4F1FA"
MEIA, MEIA_LISTRA, MEIA_SOMBRA = "#86CFF2", "#F6F8FA", "#5FA9D1"   # meia colorida de criança (azul-claro listrado)
TENIS, TENIS_SOMBRA, SOLA, SOLA_ESC = "#FBFCFD", "#D3DCE5", "#C3CBD3", "#8E99A5"
VELCRO, VELCRO_ESC = "#5DA9E9", "#2F6FA8"                         # tiras de velcro do tênis infantil
FUNDO_CARTAO = "#0B1824"
AMBAR = "#FFB547"
# fita 1: piso emborrachado de parquinho (placas azul-petróleo com granulado claro)
BORRACHA = ("#1E5C67", "#236A76", "#1A525C")
BORRACHA_JUNTA, GRANULADO = "#0F3439", "#9FD1D6"
# fita 2: piso de madeira (paleta do piloto)
MADEIRA = ("#6C4731", "#5F3D29", "#77513A")
MADEIRA_JUNTA, MADEIRA_VEIO = "#3A2518", "#82603F"

# ------------------------------------------------------------------ o "monitor" de replay (tela)
CENA = skia.Rect(40, 330, 1040, 1230)                           # o mundo é recortado aqui (selo e karaokê livres)
Y_TELA_CHAO = 1090

# ------------------------------------------------------------------ mundo (unidades de desenho) — CRIANÇA (5-7 anos)
# v2 (revisão): proporções de criança pequena — coxa e canela CURTAS em relação ao short e ao tênis, joelho
# roliço, tênis grande de velcro e meia colorida (o revisor lia as pernas da v1 como de adolescente/adulto).
Y_CHAO = 1000
HX0 = 540                                                        # quadril (a esteira corre embaixo dele)
F_CRI = 0.816                                                    # escala das distâncias do pulo (v1 -> criança)
L1, L2 = 150.0, 142.0                                            # coxa e perna curtas (criança pequena)
LMAX = L1 + L2 - 0.05
R_QUAD, R_JOE, R_TOR = 42.0, 33.0, 20.0                          # joelho roliço de criança
BOJO = 6.0
TS = 1.18                                                        # tênis grande (pé de criança "calçado")
BOLA = (60.0 * TS, 40.0 * TS)                                    # ponto de apoio do antepé do tênis (ref. tornozelo)
CALC = (-32.0 * TS, 40.0 * TS)                                   # base do calcanhar do tênis
DX_LONGE = -24.0                                                 # a perna de trás, um pouco atrás (profundidade): quadril E pé
HEM = 80.0                                                       # barra do short, ao longo da coxa

# ciclo do pulo de sapo (tempo de FILME): pouso -> agacha até o fundo (SQ) -> impulso (PU) -> voo (FL)
SQ, PU, EXT, FL = 0.75, 0.30, 0.26, 0.66                         # EXT: joelho todo esticado, pontas ainda no chão
P_CICLO = SQ + PU + FL
HH_POUSO, HH_FUNDO = 365.0 * F_CRI, 152.0 * F_CRI                # altura do quadril (acima do chão)
HJ, HFP = 95.0 * F_CRI, 150.0 * F_CRI                            # subida do quadril e dos pés no voo (encolhe)
BR_AG = 35.0 * F_CRI + BOLA[0]                                   # bola do pé rel. ao quadril: agachada
BR_DEC = -105.0 * F_CRI + BOLA[0]                                #   ... e decolando
INC_POUSO, INC_FUNDO, INC_EXT, INC_DEC = 8.0, 12.0, 34.0, 48.0
D_VOO = 110.0 * F_CRI
CICLO_G = (BR_AG - BR_DEC) + D_VOO                               # quanto o chão corre por pulo

V1 = 1.05                                                        # "1×"
VL = 0.25 * V1                                                   # "0,25×"
VR = 3.0                                                         # avanço rápido


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
    """Traço desenhado até a fração k (cópia do cf_crianca_mancando)."""
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


# ------------------------------------------------------------------ o tempo do filme
def fita(t, T):
    """1 = parquinho (até o "Agora"), 2 = piso de madeira (os sinais)."""
    return 1 if t < T["agora"] else 2


def t_crec1(T):
    """O "crec" a 1× cai no RESPIRO entre "crec?" e "Volta" (v2: a própria palavra cobria o som na v1)."""
    return T["volta"] - 0.25


U0_ABERTURA = 1.13                                               # quadro 0: no ar, logo depois de decolar


def _fundo_perto(tf, dt, v):
    """Fundo de agachamento (n*P + SQ) mais perto de tf + v*dt (a 1×, a velocidade só ajusta uns %)."""
    alvo = tf + v * dt
    n = round((alvo - SQ) / P_CICLO)
    cands = [k * P_CICLO + SQ for k in range(n - 2, n + 3)]
    cands = [b for b in cands if b > tf + 0.55 * v * dt]
    return min(cands, key=lambda b: abs(b - alvo))


def t_perfil2(T):
    """Fita 2: fim da câmera 2 (de frente) — volta ao perfil logo depois do contorno do "incha"."""
    return T["incha"] + 0.36


SUBIDA = 0.62                                                    # "trava": levanta da agachada em 0,62 s (a 0,25×)


def t_congela_trava(T):
    """Congela o joelho travado DEPOIS dos 2 quiques contra o batente (nunca antes do "estica")."""
    return max(T["estica"] + 0.1, t_lock_trava(T) + QUIQUES[-1][0] + QUIQUES[-1][1] + 0.03)


class Filme:
    """Liga o tempo do VÍDEO ao tempo do FILME por trechos presos às palavras-âncora: play (1×), volta
    (rebobinar), lenta (0,25×), avanca (avanço rápido), congela (0×). Na fita 2 o tempo do filme só move o
    ponteiro (a coreografia é por tempo de vídeo).
    v2: a câmera lenta revê O MESMO pulo do 1× (ciclo B); o ▶▶ fica só no "seguiu pulando" (o tempo passa e ela
    segue pulando) e a explicação roda a 1×, com um "crec" no "tendão", outro na "bolha" e o do "corpo"
    virando brilhos (v1: 5,7 s de ▶▶ borrado davam a impressão de pular a explicação)."""

    def __init__(self, T):
        s = []
        B = P_CICLO                                              # o ciclo que estala (o 2º do filme)
        tc1 = t_crec1(T)
        fundo1 = B + SQ
        v_ab = (fundo1 - U0_ABERTURA) / tc1                      # abertura: do voo ao fundo, que cai no respiro
        a = fundo1 + v_ab * (T["volta"] - tc1)
        s.append((0.0, T["volta"], "play", U0_ABERTURA, a, None))
        tf_s = B - VL * (T["so1"] - T["camera"])                 # no ar, antes do pouso; toca o chão NO "só"
        s.append((T["volta"], T["camera"], "volta", a, tf_s, "inout"))
        s.append((T["camera"], T["so1"], "lenta", tf_s, B, None))
        tf_r = B + 0.66 * SQ
        tf_j = tf_r + 0.035                                      # "repara": o filme quase para
        s.append((T["so1"], T["repara"], "lenta", B, tf_r, None))
        s.append((T["repara"], T["junto"], "lenta", tf_r, tf_j, None))
        s.append((T["junto"], T["estalou"], "lenta", tf_j, B + SQ, None))      # fundo NO "estalou"
        s.append((T["estalou"], T["inteirinho"], "lenta", B + SQ, B + SQ + EXT, None))
        tf_c = B + SQ + EXT
        s.append((T["inteirinho"], T["seguiu"], "congela", tf_c, tf_c, None))
        tf_s1 = tf_c + VR * (T["sem1"] - T["seguiu"])             # ▶▶ só no "seguiu pulando"
        s.append((T["seguiu"], T["sem1"], "avanca", tf_c, tf_s1, None))
        t_ant, tf_ant = T["sem1"], tf_s1
        self.fundos_1x = []
        for chave in ("tendao", "bolha", "corpo"):               # 1×: um fundo de agachamento em cada palavra
            tfb = _fundo_perto(tf_ant, T[chave] - t_ant, V1)
            s.append((t_ant, T[chave], "play", tf_ant, tfb, None))
            self.fundos_1x.append((chave, (tfb - tf_ant) / (T[chave] - t_ant) / V1))
            t_ant, tf_ant = T[chave], tfb
        tf_a = tf_ant + V1 * (T["agora"] - t_ant)
        s.append((t_ant, T["agora"], "play", tf_ant, tf_a, None))
        # fita 2 (pseudo-filme para o cronômetro)
        b = math.floor(tf_a) + 40.0
        tcg = t_congela_trava(T)
        trechos = ((T["agora"], T["atencao"], "play"), (T["atencao"], T["dor2"], "lenta"),
                   (T["dor2"], T["joelho2"], "congela"), (T["joelho2"], tcg, "lenta"),
                   (tcg, T["ai"], "congela"), (T["ai"], T["total"] + 2.0, "play"))
        for t0, t1, tipo in trechos:
            v = {"play": V1, "lenta": VL, "congela": 0.0}[tipo]
            s.append((t0, t1, tipo, b, b + v * (t1 - t0), None))
            b += v * (t1 - t0)
        self.segs = s
        self.T = T
        self.v_abertura = v_ab / V1

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
        """Início do trecho corrido do mesmo tipo."""
        i = self.segs.index(self.seg(t))
        while i > 0 and self.segs[i - 1][2] == self.segs[i][2] and self.segs[i - 1][1] == self.segs[i][0]:
            i -= 1
        return self.segs[i][0]


# ------------------------------------------------------------------ pé (tênis) e pose
class Pe:
    __slots__ = ("ax", "ay", "inc", "chao")

    def __init__(self, ax, ay, inc, chao):
        self.ax, self.ay, self.inc, self.chao = ax, ay, inc, chao

    def ponto(self, p):
        r = rot(p, self.inc)
        return self.ax + r[0], self.ay + r[1]

    def calcanhar(self):
        return self.ponto(CALC)

    def bola(self):
        return self.ponto(BOLA)


def _pe_na_bola(bx, inc):
    """Pé apoiado no antepé: a bola fica no chão em x = bx (girar o pé = levantar o calcanhar)."""
    r = rot(BOLA, inc)
    return Pe(bx - r[0], Y_CHAO - r[1], inc, True)


def _quadril_alcanca(hy, pes, hx=HX0):
    """O quadril desce o que for preciso para as pernas alcançarem os pés (perna esticada no limite). O 2º pé
    é o da perna de trás, cujo quadril fica DX_LONGE atrás."""
    for i, p in enumerate(pes):
        dx = p.ax - hx - (DX_LONGE if i == 1 else 0.0)
        if abs(dx) < LMAX:
            hy = max(hy, p.ay - math.sqrt(LMAX * LMAX - dx * dx))
    return hy


def ciclo(tf):
    """Pulo de sapo no tempo de filme `tf` -> (y do quadril, pé de perto, pé de longe, chão corrido G).
    O pé apoiado não escorrega: a bola fica parada no chão (a esteira corre o mesmo que o quadril avança)."""
    n = math.floor(tf / P_CICLO)
    u = tf - n * P_CICLO
    G = n * CICLO_G
    if u < SQ:                                                  # pouso -> fundo do agachamento
        k = u / SQ
        hh = lerp(HH_POUSO, HH_FUNDO, 1 - (1 - k) ** 2)
        inc = INC_POUSO * (1 - sstep(k / 0.2)) + INC_FUNDO * sstep((k - 0.5) / 0.5)
        br, chao = BR_AG, True
    elif u < SQ + PU:                                           # impulso: estica inteiro, sobe na ponta e sai
        k = (u - SQ) / PU
        ke = clamp(k / (EXT / PU))
        hh = lerp(HH_FUNDO, 520.0, e_inout(ke) ** 0.8)          # alto demais de propósito: a perna estica no limite
        inc = lerp(INC_FUNDO, INC_EXT, sstep((ke - 0.3) / 0.7)) + (INC_DEC - INC_EXT) * clamp((k - EXT / PU) / (1 - EXT / PU))
        br, chao = lerp(BR_AG, BR_DEC, e_inout(ke)), True
        G += BR_AG - br
    else:                                                       # voo: o quadril sobe HJ, os pés sobem mais (encolhe)
        w = (u - SQ - PU) / FL
        p0 = _pe_na_bola(HX0 + BR_DEC, INC_DEC)
        p1 = _pe_na_bola(HX0 + BR_AG, INC_POUSO)
        hh0 = Y_CHAO - _quadril_alcanca(0.0, [p0])
        inc = lerp(INC_DEC, INC_POUSO, sstep(w / 0.7))
        ax = lerp(p0.ax, p1.ax, e_inout(w))
        ay = lerp(p0.ay, p1.ay, w) - HFP * 4 * w * (1 - w)
        hh = lerp(hh0, HH_POUSO, w) + HJ * 4 * w * (1 - w)
        G += (BR_AG - BR_DEC) + D_VOO * w
        perto = Pe(ax, ay, inc, False)
        longe = Pe(ax + DX_LONGE, ay, inc, False)
        hy = _quadril_alcanca(Y_CHAO - hh, [perto, longe])
        return hy, perto, longe, G
    perto = _pe_na_bola(HX0 + br, inc)
    longe = _pe_na_bola(HX0 + br + DX_LONGE, inc)
    hy = _quadril_alcanca(Y_CHAO - hh, [perto, longe])
    return hy, perto, longe, G


# fita 2 — coreografia por tempo de vídeo
HH_EM_PE2, HH_FUNDO2 = 392.0 * F_CRI, 165.0 * F_CRI
AX_AG = BR_AG - BOLA[0]                                          # tornozelo na agachada (à frente do quadril)
DX_PE_TRAVA = 4.0                                                # em pé: tornozelos sob os quadris (pés lado a lado)
TRAVA_FLEX = 35.0                                                # o joelho de perto para dobrado a ~35°
QUIQUES = ((0.0, 0.17, 13.0), (0.17, 0.14, 10.5))                 # o pé fica na ponta (não sai do chão)                # (início após bater, duração, graus que volta)


def _d_flex(graus):
    """Distância quadril-tornozelo com o joelho dobrado `graus`."""
    return math.sqrt(L1 * L1 + L2 * L2 + 2 * L1 * L2 * math.cos(math.radians(graus)))


def _e_sub(k):
    """Subida que sai do repouso e CHEGA com velocidade (bate em pé, sem frear)."""
    k = clamp(k)
    return 2 * k * k - k ** 3


_SHIFT = AX_AG - DX_PE_TRAVA
HY_ST = Y_CHAO - BOLA[1] - math.sqrt(LMAX * LMAX - DX_PE_TRAVA ** 2)   # quadril com a perna de trás reta


def _subida(u):
    """Levantar (u = tempo desde o fim da câmera 2) -> (quadril y, pé de trás, x da bola do pé de perto, inc base)."""
    k = clamp(u / SUBIDA)
    e = _e_sub(k)
    sh = _SHIFT * e
    inc0 = INC_FUNDO * (1 - sstep(k / 0.7))
    longe = _pe_na_bola(HX0 + DX_LONGE + BR_AG - sh, inc0)
    hy = lerp(Y_CHAO - HH_FUNDO2, HY_ST, e)
    dx = longe.ax - (HX0 + DX_LONGE)
    hy = max(hy, longe.ay - math.sqrt(max(1.0, LMAX * LMAX - dx * dx)))
    return hy, longe, HX0 + BR_AG - sh, inc0


def _pe_limitado(hip, bx, inc0, d_lim):
    """Pé de perto com a bola em `bx` no chão; o calcanhar sobe o que for preciso para o joelho NÃO passar do
    limite (distância quadril-tornozelo <= d_lim). Se nem na ponta alcança, o pé sai do chão."""
    def dist(inc):
        pe = _pe_na_bola(bx, inc)
        return math.hypot(pe.ax - hip[0], pe.ay - hip[1]), pe
    d0, pe0 = dist(inc0)
    if d0 <= d_lim:
        return pe0
    b = min((inc0 + 2.0 * i for i in range(int((70.0 - inc0) / 2.0) + 1)), key=lambda x: dist(x)[0])
    a = inc0                                                     # a distância desce até `b` e depois sobe
    db, peb = dist(b)
    if db > d_lim:                                               # pendura na ponta, fora do chão
        ux, uy = (peb.ax - hip[0]) / db, (peb.ay - hip[1]) / db
        return Pe(hip[0] + ux * d_lim, hip[1] + uy * d_lim, b, False)
    for _ in range(22):
        m = 0.5 * (a + b)
        if dist(m)[0] > d_lim:
            a = m
        else:
            b = m
    return dist(b)[1]


def _u_lock():
    """Instante (desde o fim da câmera 2) em que o joelho de perto chega aos 35° e bate no batente."""
    d35 = _d_flex(TRAVA_FLEX)
    u = 0.0
    while u < SUBIDA:
        hy, _, bx, inc0 = _subida(u)
        pe = _pe_na_bola(bx, inc0)
        if math.hypot(pe.ax - HX0, pe.ay - hy) > d35:
            return u
        u += 0.002
    return SUBIDA


U_LOCK = _u_lock()


def t_lock_trava(T):
    return t_perfil2(T) + U_LOCK


def quique(v):
    """Graus que o joelho volta a dobrar depois de bater no batente (2 quiques que diminuem)."""
    for t0, d, amp in QUIQUES:
        if t0 <= v < t0 + d:
            return amp * math.sin(math.pi * (v - t0) / d)
    return 0.0


def pose2(t, T):
    """Fita 2 -> (y do quadril, pé de perto, pé de longe, G). Até a câmera 2: pés juntos (agacha devagar e fica
    embaixo, a mão chega). Depois ("trava"): levanta com os pés LADO A LADO; a perna de trás estica inteira e o
    joelho de perto bate num batente invisível a ~35°, quica 2 vezes e fica dobrado, com o calcanhar no ar."""
    tp = t_perfil2(T)
    if t < tp:
        te = min(t, T["dor2"] + 0.02)                            # congela junto com o filme no "dor"
        k = sstep(prog(te, T["atencao"] + 0.02, T["estalo"] - 0.02))
        hh = lerp(HH_EM_PE2, HH_FUNDO2, k) + (2.0 * math.sin((te - T["estalo"]) * 5) if te > T["estalo"] else 0.0)
        inc = INC_FUNDO * sstep((k - 0.55) / 0.45)
        perto = _pe_na_bola(HX0 + BR_AG, inc)
        longe = _pe_na_bola(HX0 + BR_AG + DX_LONGE, inc)
        hy = _quadril_alcanca(Y_CHAO - hh, [perto, longe])
        return hy, perto, longe, 0.0
    u = min(t, t_congela_trava(T)) - tp
    hy, longe, bx, inc0 = _subida(u)
    flex = TRAVA_FLEX + (quique(u - U_LOCK) if u >= U_LOCK else 0.0)
    perto = _pe_limitado((HX0, hy), bx, inc0, _d_flex(flex))
    return hy, perto, longe, _SHIFT * _e_sub(u / SUBIDA)


def frente2(t, T):
    """Câmera 2 (de frente): do "joelho" até logo depois do contorno do "incha"."""
    return T["joelho2"] <= t < t_perfil2(T)


def pose(t, T, F):
    if fita(t, T) == 1:
        return ciclo(F.tf(t))
    return pose2(t, T)


# ------------------------------------------------------------------ desenho da perna (cópias adaptadas)
def joelho(hx, hy, ax, ay):
    """Cinemática inversa de dois segmentos; o joelho dobra para a frente (+x). (cópia do cf_crianca_mancando)"""
    dx, dy = ax - hx, ay - hy
    d = max(1.0, min(math.hypot(dx, dy), L1 + L2 - 0.02))
    fi = math.atan2(dy, dx)
    al = math.acos(clamp((L1 * L1 + d * d - L2 * L2) / (2 * L1 * d), -1.0, 1.0))
    return hx + L1 * math.cos(fi - al), hy + L1 * math.sin(fi - al)


def tubo(x0, y0, r0, x1, y1, r1):
    """(cópia do cf_crianca_mancando)"""
    L = math.hypot(x1 - x0, y1 - y0) or 1.0
    nx, ny = -(y1 - y0) / L, (x1 - x0) / L
    p = skia.Path()
    p.moveTo(x0 + nx * r0, y0 + ny * r0); p.lineTo(x1 + nx * r1, y1 + ny * r1)
    p.lineTo(x1 - nx * r1, y1 - ny * r1); p.lineTo(x0 - nx * r0, y0 - ny * r0); p.close()
    c0 = skia.Path(); c0.addCircle(x0, y0, r0)
    c1 = skia.Path(); c1.addCircle(x1, y1, r1)
    return _uniao(_uniao(p, c0), c1)


def _eixo(kx, ky, ax, ay):
    L = math.hypot(ax - kx, ay - ky) or 1.0
    ux, uy = (ax - kx) / L, (ay - ky) / L
    return L, ux, uy, uy, -ux                                   # (comprimento, descendo, frente)


def canela(kx, ky, ax, ay, bojo=BOJO):
    """Perna do joelho ao tornozelo: frente quase reta, panturrilha levemente abaulada (cópia do piloto)."""
    L, ux, uy, nx, ny = _eixo(kx, ky, ax, ay)

    def P(a, b):
        return kx + ux * a + nx * b, ky + uy * a + ny * b
    p = skia.Path()
    p.moveTo(*P(0, R_JOE))
    p.cubicTo(*P(0.35 * L, R_JOE * 0.9), *P(0.75 * L, R_TOR * 1.1), *P(L, R_TOR))
    p.lineTo(*P(L, -R_TOR))
    p.cubicTo(*P(0.80 * L, -R_TOR * 1.1), *P(0.55 * L, -(R_JOE + bojo)), *P(0.33 * L, -(R_JOE + bojo)))
    p.cubicTo(*P(0.16 * L, -(R_JOE + bojo)), *P(0.04 * L, -R_JOE * 1.02), *P(0, -R_JOE))
    p.close()
    c0 = skia.Path(); c0.addCircle(kx, ky, R_JOE)
    c1 = skia.Path(); c1.addCircle(ax, ay, R_TOR)
    return _uniao(_uniao(p, c0), c1)


def _tenis():
    """Tênis de perfil (origem = tornozelo, x para a frente, y para baixo, sola em y = 40)."""
    p = skia.Path()
    p.moveTo(-27, -12)
    p.cubicTo(-36, -2, -40, 20, -38, 32)                        # calcanhar
    p.cubicTo(-37, 38, -33, 40, -27, 40)
    p.lineTo(84, 40)                                            # sola
    p.cubicTo(97, 40, 101, 30, 95, 22)                          # bico redondo
    p.cubicTo(84, 12, 58, 4, 30, -6)                            # peito do pé
    p.lineTo(24, -16)                                           # língua
    p.cubicTo(10, -19, -12, -15, -27, -12)                      # colarinho
    p.close()
    return p


TENIS_P = _tenis()


def _mat(x, y, graus, esc=1.0):
    m = skia.Matrix(); m.postScale(esc, esc); m.postRotate(graus); m.postTranslate(x, y)
    return m


def tenis(cv, pe, s, esc=lambda c: c):
    """Tênis branco GRANDE de criança: sola cinza-clara, biqueira e duas tiras de velcro azuis (sem cadarço)."""
    m = _mat(pe.ax, pe.ay, pe.inc, TS)
    corpo = skia.Path(TENIS_P); corpo.transform(m)
    cv.drawPath(corpo, paint(esc(TENIS)))
    cv.save(); cv.clipPath(corpo, skia.ClipOp.kIntersect, True)
    cv.concat(m)
    cv.drawRect(skia.Rect(-45, 29, 105, 45), paint(esc(SOLA)))                      # sola
    cv.drawLine(-45, 29, 105, 29, paint(esc(SOLA_ESC), 255, "stroke", 2.4))
    cv.drawLine(-45, 35, 105, 35, paint(esc(SOLA_ESC), 120, "stroke", 1.6))
    bq = skia.Path(); bq.moveTo(70, 29); bq.cubicTo(78, 16, 90, 16, 100, 22)        # biqueira
    cv.drawPath(bq, paint(esc(TENIS_SOMBRA), 255, "stroke", 3))
    cv.drawPath(TENIS_P, paint(esc(TENIS_SOMBRA), 255, "stroke", 9))                # volume (aro)
    cv.drawLine(-20, 4, -8, 26, paint(esc(TENIS_SOMBRA), 255, "stroke", 3))          # costura do calcanhar
    for x0 in (14.0, 38.0):                                                         # 2 tiras de velcro
        tira = skia.Path()
        tira.moveTo(x0 - 6, -26); tira.lineTo(x0 + 9, -26); tira.lineTo(x0 + 21, 24); tira.lineTo(x0 + 6, 24); tira.close()
        cv.drawPath(tira, paint(esc(VELCRO)))
        cv.drawPath(tira, paint(esc(VELCRO_ESC), 255, "stroke", 2.2))
        cv.drawLine(x0 + 2, -18, x0 + 12, 18, paint(esc("#A9D3F7"), 200, "stroke", 2.0))
    cv.restore()
    cv.drawPath(corpo, paint("#5C6B7A", 220, "stroke", 3.6 / (s * TS)))


def manga_short(hip, joe):
    """Barra do short no referencial da coxa (reta, de criança maior). Adaptado do cf_crianca_mancando."""
    hx, hy = hip; kx, ky = joe
    L = math.hypot(kx - hx, ky - hy) or 1.0
    ux, uy = (kx - hx) / L, (ky - hy) / L; nx, ny = -uy, ux
    ex, ey = hx + ux * HEM, hy + uy * HEM
    p = skia.Path()
    p.moveTo(hx + nx * 47, hy + ny * 47); p.lineTo(ex + nx * 50, ey + ny * 50)
    p.quadTo(ex + ux * 4, ey + uy * 4, ex - nx * 50, ey - ny * 50)
    p.lineTo(hx - nx * 47, hy - ny * 47); p.close()
    c = skia.Path(); c.addCircle(hx, hy, 47)
    bainha = ((ex + nx * 48 - ux * 10, ey + ny * 48 - uy * 10), (ex - nx * 48 - ux * 10, ey - ny * 48 - uy * 10))
    return _uniao(p, c), bainha, (ux, uy, nx, ny)


def path_cintura(hip):
    hx, hy = hip
    p = skia.Path()
    p.moveTo(hx - 58, hy - 82)
    p.lineTo(hx + 52, hy - 82)
    p.cubicTo(hx + 60, hy - 40, hx + 58, hy + 2, hx + 46, hy + 26)
    p.lineTo(hx - 36, hy + 30)
    p.cubicTo(hx - 74, hy + 16, hx - 76, hy - 40, hx - 58, hy - 82)
    p.close()
    return p


def perna(cv, hip, pe, s, longe=False):
    """Perna num contorno só (coxa + perna), pele lisa e OPACA, meia curta e tênis. Devolve o joelho."""
    hx, hy = hip
    kx, ky = joelho(hx, hy, pe.ax, pe.ay)
    corpo = _uniao(tubo(hx, hy, R_QUAD, kx, ky, R_JOE), canela(kx, ky, pe.ax, pe.ay))
    esc = (lambda c: lerpc(c, "#2A1B16", 0.3)) if longe else (lambda c: c)
    cv.save(); cv.clipPath(corpo, skia.ClipOp.kIntersect, True)
    cv.drawPath(corpo, paint(esc(PELE)))
    for larg, cor in ((30, "#EAAA8C"), (18, "#E29F82"), (8, "#D69276")):           # volume: aro mais escuro
        cv.drawPath(corpo, paint(esc(cor), 255, "stroke", larg))
    L, ux, uy, nx, ny = _eixo(kx, ky, pe.ax, pe.ay)
    luz = paint(esc("#F6C6AE"), 255, "stroke", 12)
    cv.drawLine(kx + nx * 12 + ux * 22, ky + ny * 12 + uy * 22, kx + nx * 9 + ux * 0.6 * L, ky + ny * 9 + uy * 0.6 * L, luz)
    Lc = math.hypot(kx - hx, ky - hy) or 1.0
    tx, ty = (kx - hx) / Lc, (ky - hy) / Lc
    cv.drawLine(hx + tx * 70 + ty * 16, hy + ty * 70 - tx * 16, kx - tx * 30 + ty * 14, ky - ty * 30 - tx * 14, luz)
    # meia colorida de criança (azul-claro com 2 listras brancas), do tornozelo até ~36 acima
    meia = paint(esc(MEIA), 255, "stroke", R_TOR * 3)
    meia.setStrokeCap(skia.Paint.kButt_Cap)
    cv.drawLine(pe.ax - ux * 36, pe.ay - uy * 36, pe.ax + ux * 30, pe.ay + uy * 30, meia)
    for o, cor, lg in ((33, MEIA_SOMBRA, 2.4), (27, MEIA_LISTRA, 5.0), (18, MEIA_LISTRA, 5.0)):
        cv.drawLine(pe.ax - ux * o + nx * R_TOR * 1.4, pe.ay - uy * o + ny * R_TOR * 1.4,
                    pe.ax - ux * o - nx * R_TOR * 1.4, pe.ay - uy * o - ny * R_TOR * 1.4,
                    paint(esc(cor), 235, "stroke", lg))
    cv.restore()
    cv.drawPath(corpo, paint(PELE_LINHA, 230, "stroke", 4.6 / s))
    tenis(cv, pe, s, esc)
    return kx, ky


def pernas(cv, hip, perto, longe, s):
    """Perna de trás (mais escura), perna da frente e o short roxo-uva por cima (friso branco na lateral)."""
    hx, hy = hip
    hl = (hx + DX_LONGE, hy)
    kl = perna(cv, hl, longe, s, longe=True)
    m_l, b_l, _ = manga_short(hl, kl)
    cv.drawPath(m_l, paint(SHORT_ESC))
    cv.drawPath(m_l, paint(SHORT_LINHA, 220, "stroke", 4.0 / s))
    kp = perna(cv, hip, perto, s)
    m_p, b_p, e_p = manga_short(hip, kp)
    sh = _uniao(path_cintura(hip), m_p)
    cv.drawPath(sh, paint("#000000", 50, blur=8))
    cv.drawPath(sh, paint(SHORT))
    cv.save(); cv.clipPath(sh, skia.ClipOp.kIntersect, True)
    ux, uy, nx, ny = e_p
    p0, p1 = b_p
    cv.drawLine(p0[0] + ux * 6, p0[1] + uy * 6, p1[0] + ux * 6, p1[1] + uy * 6, paint(SHORT_CL, 255, "stroke", 9))   # barra
    cv.drawRect(skia.Rect(hx - 90, hy - 90, hx + 90, hy - 62), paint(SHORT_ESC))                                   # cós
    cv.drawLine(hx - 90, hy - 62, hx + 90, hy - 62, paint(SHORT_LINHA, 170, "stroke", 3.0))
    fr = skia.Path()                                                                                               # friso branco
    fr.moveTo(hx + 2, hy - 62); fr.lineTo(hx + 2, hy - 10)
    fr.lineTo(hx + ux * (HEM + 4), hy + uy * (HEM + 4))
    cv.drawPath(fr, paint(FRISO, 235, "stroke", 9))
    cv.restore()
    cv.drawPath(sh, paint(SHORT_LINHA, 230, "stroke", 4.4 / s))
    cv.drawLine(b_p[0][0], b_p[0][1], b_p[1][0], b_p[1][1], paint(SHORT_LINHA, 150, "stroke", 3.5 / s))
    return kp, kl


def frente_joelho(hip, pe):
    """-> (joelho, direção 'para fora' na frente do joelho, ângulo de flexão em graus)."""
    kx, ky = joelho(hip[0], hip[1], pe.ax, pe.ay)
    a = (hip[0] - kx, hip[1] - ky); b = (pe.ax - kx, pe.ay - ky)
    la, lb = math.hypot(*a) or 1.0, math.hypot(*b) or 1.0
    a = (a[0] / la, a[1] / la); b = (b[0] / lb, b[1] / lb)
    bx, by = -(a[0] + b[0]), -(a[1] + b[1])
    lb2 = math.hypot(bx, by)
    if lb2 < 1e-3:                                               # perna reta: a frente é a normal do eixo
        bx, by = -a[1], a[0]
        if bx < 0:
            bx, by = -bx, -by
        lb2 = 1.0
    cosang = clamp(a[0] * b[0] + a[1] * b[1], -1.0, 1.0)
    return (kx, ky), (bx / lb2, by / lb2), 180.0 - math.degrees(math.acos(cosang))


# ------------------------------------------------------------------ câmera (mundo -> tela)
BASE = (1.55, HX0 + 70, Y_CHAO, 470, Y_TELA_CHAO)
ZOOM = (1.94, HX0 + 85, Y_CHAO - 175, 520, 780)                   # 1,25× sobre o joelho
MEIO = (1.72, HX0 + 80, Y_CHAO, 480, Y_TELA_CHAO)                # explicação a 1×: chega um pouco mais perto
ZOOM2 = (1.80, HX0 + 70, Y_CHAO - 175, 520, 800)                  # fita 2: espaço para a mão que desce
BASE2 = (1.55, HX0 + 70, Y_CHAO, 470, Y_TELA_CHAO)
TRAVA = (1.80, HX0 + 20, Y_CHAO, 540, 1105)                      # fita 2, "trava": as duas pernas em pé no quadro


_CAM_MAO = {}


def cam_mao(T):
    """Fita 2, "dor": bem perto do joelho, com o topo do quadro na altura do ombro (o braço entra por cima)."""
    chave = round(T["dor2"], 4)
    if chave not in _CAM_MAO:
        hy, perto, _, _ = pose2(T["dor2"], T)
        kx, ky = joelho(HX0, hy, perto.ax, perto.ay)
        _CAM_MAO[chave] = (2.45, kx, ky, 610, 712)
    return _CAM_MAO[chave]


def _mist(a, b, k):
    return tuple(lerp(x, y, k) for x, y in zip(a, b))


def camera(t, T):
    cam = BASE
    passos = (
        (T["camera"], 0.8, ZOOM),
        (T["seguiu"], 0.4, BASE),
        (T["costuma"], 1.4, MEIO),
        (T["agora"], 0.02, BASE2),
        (T["atencao"], 0.7, ZOOM2),
        (T["vem2"] - 0.25, 0.35, cam_mao(T)),
        (t_perfil2(T), 0.02, TRAVA),
    )
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


# ------------------------------------------------------------------ chão
def chao(cv, G, s, f=1):
    """Fita 1: placas de borracha de parquinho com granulado; fita 2: tábuas de madeira. Correm com a esteira."""
    x0, x1 = HX0 - 1000, HX0 + 1000
    if f == 1:
        filas = ((Y_CHAO, Y_CHAO + 36, 150, 1.0, 0.0), (Y_CHAO + 36, Y_CHAO + 92, 180, 1.25, 0.5),
                 (Y_CHAO + 92, Y_CHAO + 420, 220, 1.6, 0.25))
        cores, junta = BORRACHA, BORRACHA_JUNTA
    else:
        filas = ((Y_CHAO, Y_CHAO + 30, 250, 1.0, 0.0), (Y_CHAO + 30, Y_CHAO + 72, 300, 1.2, 0.45),
                 (Y_CHAO + 72, Y_CHAO + 132, 350, 1.45, 0.2), (Y_CHAO + 132, Y_CHAO + 420, 420, 1.8, 0.7))
        cores, junta = MADEIRA, MADEIRA_JUNTA
    pj = skia.Path()
    claros, escuros = [], []
    for r, (y0, y1, larg, fat, defas) in enumerate(filas):
        g = G * fat - defas * larg
        j = math.floor((x0 + g) / larg)
        while True:
            x = j * larg - g
            if x > x1:
                break
            cor = cores[(j * (2 if f == 2 else 1) + r * 3) % len(cores)]
            cv.drawRect(skia.Rect(x, y0, x + larg, y1), paint(cor))
            if f == 2:
                yv = y0 + (y1 - y0) * (0.35 + 0.3 * ((j * 7) % 3) / 2)
                cv.drawLine(x + larg * 0.12, yv, x + larg * 0.7, yv, paint(MADEIRA_VEIO, 255, "stroke", 2.4 / s))
            else:                                              # granulado: pontinhos fixos em cada placa
                rng = np.random.default_rng((j * 131 + r * 17) % 100000)
                n = int(10 + (y1 - y0) / 12)
                xs = rng.uniform(4, larg - 4, n); ys = rng.uniform(y0 + 3, y1 - 3, n)
                for k in range(n):
                    (claros if k % 3 else escuros).append(skia.Point(float(x + xs[k]), float(ys[k])))
            pj.moveTo(x, y0); pj.lineTo(x, y1)
            j += 1
        pj.moveTo(x0, y0); pj.lineTo(x1, y0)
    if claros:
        cv.drawPoints(skia.Canvas.kPoints_PointMode, claros, paint(GRANULADO, 150, "stroke", 4.0 / s))
        cv.drawPoints(skia.Canvas.kPoints_PointMode, escuros, paint("#0B2A30", 150, "stroke", 4.0 / s))
    cv.drawPath(pj, paint(junta, 255, "stroke", 3.0 / s))
    cv.drawLine(x0, Y_CHAO, x1, Y_CHAO, paint("#E9D2B8" if f == 2 else "#BFE6EA", 220, "stroke", 5.0 / s))


def sombra_pe(cv, pe):
    baixo = max(pe.ponto(p)[1] for p in (CALC, BOLA))
    a = clamp(1 - (Y_CHAO - baixo) / 90)
    if a <= 0:
        return
    xb, xc = pe.bola()[0], pe.calcanhar()[0]
    cv.drawOval(skia.Rect(min(xb, xc) - 12, Y_CHAO - 6, max(xb, xc) + 44, Y_CHAO + 8), paint("#000000", int(105 * a), blur=6))


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
    """O fundo do cf_alongamento.fundo (degradê radial que respira + partículas), com o degradê em imagem."""
    def d(c):
        sh = skia.GradientShader.MakeRadial(skia.Point(W / 2, H * 0.42 + 60), H * 0.78, [_c("#17384C"), _c(BG_OUT)])
        c.drawRect(skia.Rect(0, 0, W, H + 120), paint("#17384C", shader=sh))
    _blit(cv, _img("fundo", W, H + 120, d), 0, -60 + 40 * math.sin(t * 0.3))
    for x, y, v, r, a in PART:
        yy = (y - v * t * 6) % H
        cv.drawCircle(x + 8 * math.sin(t * 0.5 + y), yy, r, paint("#BFE3FF", int(a)))


def _rel(c):
    c.translate(-CENA.left(), -CENA.top())


# ------------------------------------------------------------------ efeitos de "replay" (cópias do piloto)
def monitor_fundo(cv):
    def d(c):
        _rel(c)
        c.drawRect(CENA, paint("#FFFFFF", 9))
        sh = skia.GradientShader.MakeRadial(skia.Point(540, 760), 780, [_c("#000000", 0), _c("#000000", 0), _c("#000000", 85)],
                                            [0.0, 0.55, 1.0])
        c.drawRect(CENA, paint("#000000", 255, shader=sh))
    _blit(cv, _img("monitor", CENA.width(), CENA.height(), d), CENA.left(), CENA.top())


def profundidade(cv, gy):
    """O chão escurece para baixo (profundidade), em imagem pronta."""
    def d(c):
        sh = skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, 520)], [_c(BG_OUT, 0), _c(BG_OUT, 170)])
        c.drawRect(skia.Rect(0, 0, CENA.width(), 900), paint(BG_OUT, 255, shader=sh))
    _blit(cv, _img("prof", CENA.width(), 900, d), CENA.left(), gy + 6)


def varredura(cv, t, ambar, limpo=False):
    """Linhas de varredura + granulação + tinta âmbar da câmera lenta. `limpo` (miniaturas): só o âmbar."""
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


def corte_fita(cv, t, t0, dur=0.25):
    """Corte de fita: chiado (faixas de ruído e neve) — a cena muda por baixo dele."""
    k = t - t0
    if not (-0.03 <= k < dur):
        return
    a = 1.0 if k < 0.1 else 1 - prog(k, 0.1, dur)
    rng = np.random.default_rng(int(round(t * FPS)) + 911)
    img = _img("ruido", CENA.width(), CENA.height(), lambda c: c.clear(_c("#6E7C88", 255)))
    _blit(cv, img, CENA.left(), CENA.top(), 0.6 * a)
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


# ------------------------------------------------------------------ painel do replay (cronômetro + velocidade)
def relogio(cv, x, y, r, a, ang):
    """Relógio de ponteiros, sem números. (cópia do cf_andador)"""
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
    """Rótulo de velocidade CENTRADO em (cx, cy)."""
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


HUD_X, HUD_Y = 786, 1166                                         # centro do relógio (na linha do chão, à direita)
POP_C = (540, 600)                                               # onde o "0,25×" grande aparece


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
    if tipo in ("volta", "avanca"):
        _setas(cv, HUD_X + 52, HUD_Y, a * (0.75 + 0.25 * math.sin(t * 18)), 1.25, tipo == "avanca")
        return
    if tipo == "congela":                                        # o rótulo do trecho anterior, apagado
        s = "0,25×" if lento_k(t, T) > 0 else "1×"
        chip_c(cv, s, *_chip_hud_c(s), a, dim=0.4)
        return
    s = "0,25×" if tipo == "lenta" else "1×"
    hx, hy = _chip_hud_c(s)
    k = t - t0
    if tipo == "lenta" and k < 0.75 and t0 in (T["camera"], T["atencao"]):   # "0,25×" grande que voa para o painel
        cx, cy = POP_C
        if k < 0.32:
            chip_c(cv, s, cx, cy, a, esc=2.5 * e_back(clamp(k / 0.16)))
        else:
            v = e_inout(prog(k, 0.32, 0.75))
            chip_c(cv, s, lerp(cx, hx, v), lerp(cy, hy, v), a, esc=lerp(2.5, 1.0, v))
        return
    pop = 1 + 0.6 * (1 - e_out(prog(t, t0, t0 + 0.3))) if t0 > 0 and tipo != "lenta" else 1.0
    chip_c(cv, s, hx, hy, a, esc=pop)


# ------------------------------------------------------------------ marcações do comentarista
def circulo_mao(cv, cx, cy, rx, ry, k, a, larg=7):
    """Círculo dourado traçado à mão (traço irregular, com pontinha de sobra). (cópia do piloto)"""
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
    """Selo branco e calmo da avaliação: estetoscópio desenhado (forma, sem texto). (cópia do piloto)"""
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


def carimbo_ouro(cv, s, x, y, rot_, t0, t, dur=1.9):
    """(cópia do cf_fratura_cola)"""
    k = t - t0
    if k < 0 or k > dur:
        return
    esc = lerp(1.9, 1.0, e_out(clamp(k / 0.16))); a = clamp(k / 0.08) * (1 - prog(k, dur - 0.35, dur))
    cv.save(); cv.translate(x, y); cv.rotate(rot_); cv.scale(esc, esc)
    f = skia.Font(F_BLACK, 62); lw = f.measureText(s)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 24, -62, lw / 2 + 24, 22), 12, 12)
    cv.drawRRect(rr, paint("#0B1824", int(160 * a))); cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 7))
    cv.drawString(s, -lw / 2, 0, f, paint(OURO, int(255 * a)))
    cv.restore()


def brilhos_sobem(cv, x, y, t, t0, n=7, raio=95, dur=0.75):
    """Brilhos dourados do cf_alongamento.brilhos que sobem e somem. v2: nascem JÁ afastados uns dos outros
    (anel de 0,45-1,0 do raio) e entram em rampa, para nunca se juntarem numa estrela pontuda colada ao
    joelho (o símbolo de impacto/dor dos quadrinhos que o storyboard proíbe)."""
    k = t - t0
    if k < 0 or k > dur:
        return
    for i in range(n):
        ang = -math.pi / 2 + (i - (n - 1) / 2) * 0.42 + 0.12 * math.sin(i * 2.7)
        d = raio * (0.45 + 0.55 * ((i * 37) % 10) / 10) * (1 + 0.35 * e_out(k / dur))
        a = int(255 * clamp(k / 0.12) * (1 - prog(k, 0.55 * dur, dur)))
        sobe = (70 + 60 * ((i * 53) % 7) / 7) * e_out(k / dur)
        px, py = x + d * math.cos(ang) * 1.15, y + d * math.sin(ang) * 0.75 - sobe
        s = 9 * (1 - 0.5 * k / dur) + 2
        p = skia.Path(); p.moveTo(px, py - s * 2); p.lineTo(px + s * 0.5, py - s * 0.5); p.lineTo(px + s * 2, py)
        p.lineTo(px + s * 0.5, py + s * 0.5); p.lineTo(px, py + s * 2); p.lineTo(px - s * 0.5, py + s * 0.5)
        p.lineTo(px - s * 2, py); p.lineTo(px - s * 0.5, py - s * 0.5); p.close()
        cv.drawPath(p, paint(OURO, a))


# ------------------------------------------------------------------ o "crec": três arcos de "pop" POR FORA do joelho
def arcos_crec(cv, cam, hip, pe, k, esc=1.0):
    """Três arcos curtos dourados que saltam da FRENTE do joelho (sem letras). `k`: 0..1 (abre e some)."""
    if k <= 0 or k >= 1:
        return
    (kx, ky), (fx, fy), _ = frente_joelho(hip, pe)
    s = cam[0]
    sx, sy = na_tela(cam, kx, ky)
    base = math.atan2(fy, fx)
    a = clamp(k / 0.15) * (1 - prog(k, 0.6, 1.0))
    abre = e_out(clamp(k / 0.55))
    r0 = (R_JOE + 10) * s
    for i, dang in enumerate((-0.62, 0.0, 0.62)):
        ang = base + dang
        d0 = r0 + (10 + 34 * abre) * esc
        comp = (16 + 22 * abre) * esc * (1.0 if i == 1 else 0.82)
        x0, y0 = sx + d0 * math.cos(ang), sy + d0 * math.sin(ang)
        x1, y1 = sx + (d0 + comp) * math.cos(ang), sy + (d0 + comp) * math.sin(ang)
        cx_, cy_ = (x0 + x1) / 2 - 7 * esc * math.sin(ang), (y0 + y1) / 2 + 7 * esc * math.cos(ang)
        p = skia.Path(); p.moveTo(x0, y0); p.quadTo(cx_, cy_, x1, y1)
        cv.drawPath(p, paint("#000000", int(120 * a), "stroke", 13 * esc, blur=3))
        cv.drawPath(p, paint(OURO, int(255 * a), "stroke", 8 * esc))


def janelas_crec(T, F):
    """(t0, duração, escala) de cada "crec" desenhado. 1×: 0,25 s; câmera lenta: 0,8 s. v2: o 1× da explicação
    tem um "crec" no "tendão", um na "bolha" e o do "corpo" (que vira brilhos), todos na escala cheia."""
    return ((t_crec1(T) - 0.02, 0.24, 1.0), (T["estalou"], 0.8, 1.0), (T["tendao"] - 0.02, 0.3, 1.0),
            (T["bolha"] - 0.02, 0.3, 1.0), (T["corpo"] - 0.02, 0.3, 1.0), (T["estalo"], 0.8, 1.0))


# ------------------------------------------------------------------ mão no joelho (fita 2, "dor")
def _rcap(x0, y0, x1, y1, r):
    """Cápsula (segmento com pontas redondas) como path."""
    p = tubo(x0, y0, r, x1, y1, r)
    return p


def _mao_path():
    """Mão de criança vista pelo dorso (origem = punho, dedos para +x, polegar para -y)."""
    m = skia.Path(); m.addRRect(skia.RRect.MakeRectXY(skia.Rect(0, -24, 46, 24), 15, 15))
    for yc, comp in ((-17.5, 29.0), (-5.8, 35.0), (5.8, 33.0), (17.0, 26.0)):
        m = _uniao(m, _rcap(36, yc, 36 + comp, yc + 1.5, 6.2))
    m = _uniao(m, _rcap(12, -18, 32, -38, 7.0))
    return m


MAO_P = _mao_path()
MAO_ESC = 1.0


UA, FA = 112.0, 104.0                                            # braço e antebraço de criança (mundo)


def _cotovelo(sx, sy, wx, wy):
    """Cinemática inversa ombro-punho; o cotovelo fica para baixo/trás, o antebraço apoiado sobre a coxa."""
    dx, dy = wx - sx, wy - sy
    d = max(1.0, min(math.hypot(dx, dy), UA + FA - 0.5))
    fi = math.atan2(dy, dx)
    al = math.acos(clamp((UA * UA + d * d - FA * FA) / (2 * UA * d), -1.0, 1.0))
    return sx + UA * math.cos(fi + al), sy + UA * math.sin(fi + al)


def mao_geo(hip, pe):
    """-> (centro da mão, ângulo dos dedos, punho, ombro) com a mão pousada na frente do joelho de perto.
    v2: braço de criança (UA + FA ~ 1,45 coxa) vindo de um ombro logo ACIMA do quadro (câmera MAO), com o
    cotovelo dobrado; os dedos continuam o antebraço e caem por cima da frente do joelho."""
    (kx, ky), (fx, fy), _ = frente_joelho(hip, pe)
    hc = (kx + fx * 14, ky + fy * 14)
    ombro = (kx - 80, ky - 158)
    ang = math.atan2(fy, fx) + 1.15
    for _ in range(3):
        w = (hc[0] - 36 * MAO_ESC * math.cos(ang), hc[1] - 36 * MAO_ESC * math.sin(ang))
        co = _cotovelo(ombro[0], ombro[1], w[0], w[1])
        ang = math.atan2(w[1] - co[1], w[0] - co[0]) + 0.85
    w = (hc[0] - 36 * MAO_ESC * math.cos(ang), hc[1] - 36 * MAO_ESC * math.sin(ang))
    return hc, ang, w, ombro


def mao(cv, hip, pe, k, s):
    """Mão de criança que desce pelo alto e segura a frente do joelho (braço dobrado + mão, sem rosto)."""
    if k <= 0:
        return None
    hc, ang, w, ombro = mao_geo(hip, pe)
    desce = 1 - e_out(k)
    ox, oy = -20 * desce, -150 * desce
    pw = (w[0] + ox, w[1] + oy)
    om = (ombro[0] + ox, ombro[1] + oy)
    co = _cotovelo(om[0], om[1], pw[0], pw[1])
    braco = _uniao(tubo(om[0], om[1], 20, co[0], co[1], 16), tubo(co[0], co[1], 16, pw[0], pw[1], 13))
    cv.drawPath(braco, paint("#000000", 50, blur=6))
    cv.drawPath(braco, paint(PELE))
    cv.save(); cv.clipPath(braco, skia.ClipOp.kIntersect, True)
    cv.drawPath(braco, paint("#E29F82", 255, "stroke", 12))
    cv.restore()
    cv.drawPath(braco, paint(PELE_LINHA, 230, "stroke", 4.6 / s))
    m = skia.Path(MAO_P)
    mt = skia.Matrix(); mt.postScale(MAO_ESC, MAO_ESC); mt.postRotate(math.degrees(ang)); mt.postTranslate(*pw)
    m.transform(mt)
    cv.drawPath(m, paint("#000000", 70, blur=6))
    cv.drawPath(m, paint(PELE))
    cv.save(); cv.clipPath(m, skia.ClipOp.kIntersect, True)
    cv.drawPath(m, paint("#E29F82", 255, "stroke", 10))
    cv.concat(mt)
    for yc in (-17.5, -5.8, 5.8, 17.0):                              # nós dos dedos
        cv.drawLine(40, yc - 4, 40, yc + 4, paint(PELE_LINHA, 150, "stroke", 2.2))
    cv.restore()
    cv.drawPath(m, paint(PELE_LINHA, 235, "stroke", 4.2 / s))
    return hc[0] + ox, hc[1] + oy


def mao_centro(hip, pe):
    return mao_geo(hip, pe)[0]


def k_mao(t, T):
    return prog(t, T["vem2"] - 0.05, T["dor2"] + 0.02)


# ------------------------------------------------------------------ câmera 2: as duas pernas DE FRENTE (tela)
def _perna_frente(cv, x, y_bainha, y_joe, y_tor, r_joe, cheio, lado):
    """Uma perna de frente, do short ao tênis, em coordenadas de tela. `cheio`: joelho mais cheio (MESMA cor)."""
    hw_top, hw_joe, hw_pant, hw_tor = 68.0, 52.0, 50.0, 33.0           # pernas curtas e cheinhas de criança
    p = skia.Path()
    p.moveTo(x - hw_top, y_bainha - 30)
    p.cubicTo(x - hw_top, y_joe - 120, x - hw_joe - 4, y_joe - 60, x - hw_joe, y_joe)
    p.cubicTo(x - hw_joe, y_joe + 60, x - hw_pant - 2, y_joe + 110, x - hw_pant + 4, y_joe + 150)
    p.cubicTo(x - hw_pant + 12, y_tor - 70, x - hw_tor, y_tor - 30, x - hw_tor, y_tor)
    p.lineTo(x + hw_tor, y_tor)
    p.cubicTo(x + hw_tor, y_tor - 30, x + hw_pant - 12, y_tor - 70, x + hw_pant - 4, y_joe + 150)
    p.cubicTo(x + hw_pant + 2, y_joe + 110, x + hw_joe, y_joe + 60, x + hw_joe, y_joe)
    p.cubicTo(x + hw_joe + 4, y_joe - 60, x + hw_top, y_joe - 120, x + hw_top, y_bainha - 30)
    p.close()
    j = skia.Path()
    if cheio:                                                    # inchaço: contorno ~14% mais largo, e cheio acima da patela
        j.addOval(skia.Rect(x - r_joe * 1.17, y_joe - r_joe * 1.34, x + r_joe * 1.17, y_joe + r_joe * 1.04))
    else:
        j.addOval(skia.Rect(x - r_joe, y_joe - r_joe * 1.05, x + r_joe, y_joe + r_joe * 0.95))
    corpo = _uniao(p, j)
    cv.save(); cv.clipPath(corpo, skia.ClipOp.kIntersect, True)
    cv.drawPath(corpo, paint(PELE))
    for larg, cor in ((30, "#EAAA8C"), (18, "#E29F82"), (8, "#D69276")):
        cv.drawPath(corpo, paint(cor, 255, "stroke", larg))
    cv.drawLine(x - 10 * lado, y_bainha + 30, x - 12 * lado, y_joe - 70, paint("#F6C6AE", 255, "stroke", 13))
    cv.drawLine(x - 8 * lado, y_joe + 60, x - 6 * lado, y_tor - 80, paint("#F6C6AE", 255, "stroke", 12))
    if not cheio:                                                # contorno da patela (some no joelho mais cheio)
        for lado_ in (-1, 1):
            pat = skia.Path(); pat.moveTo(x + 24 * lado_, y_joe - 18); pat.quadTo(x + 30 * lado_, y_joe, x + 22 * lado_, y_joe + 16)
            cv.drawPath(pat, paint(PELE_LINHA, 70, "stroke", 3))
    meia = skia.Rect(x - hw_tor - 4, y_tor - 40, x + hw_tor + 4, y_tor + 30)
    cv.drawRect(meia, paint(MEIA))
    cv.drawLine(x - hw_tor - 4, y_tor - 37, x + hw_tor + 4, y_tor - 37, paint(MEIA_SOMBRA, 235, "stroke", 2.6))
    for yy in (y_tor - 30, y_tor - 18):                          # 2 listras brancas
        cv.drawLine(x - hw_tor - 4, yy, x + hw_tor + 4, yy, paint(MEIA_LISTRA, 235, "stroke", 5.5))
    cv.restore()
    cv.drawPath(corpo, paint(PELE_LINHA, 230, "stroke", 3.4))
    # tênis de frente
    tn = skia.Path()
    tn.moveTo(x - 52, y_tor + 2)                                 # tênis grande de criança, de frente
    tn.cubicTo(x - 74, y_tor + 30, x - 76, y_tor + 76, x - 66, y_tor + 92)
    tn.lineTo(x + 66, y_tor + 92)
    tn.cubicTo(x + 76, y_tor + 76, x + 74, y_tor + 30, x + 52, y_tor + 2)
    tn.cubicTo(x + 28, y_tor - 9, x - 28, y_tor - 9, x - 52, y_tor + 2)
    tn.close()
    cv.drawPath(tn, paint(TENIS))
    cv.save(); cv.clipPath(tn, skia.ClipOp.kIntersect, True)
    cv.drawRect(skia.Rect(x - 90, y_tor + 74, x + 90, y_tor + 98), paint(SOLA))
    cv.drawLine(x - 90, y_tor + 74, x + 90, y_tor + 74, paint(SOLA_ESC, 255, "stroke", 2.4))
    cv.drawPath(tn, paint(TENIS_SOMBRA, 255, "stroke", 10))
    for yy in (y_tor + 14, y_tor + 38):                          # 2 tiras de velcro
        tira = skia.RRect.MakeRectXY(skia.Rect(x - 40, yy, x + 40, yy + 16), 5, 5)
        cv.drawRRect(tira, paint(VELCRO))
        cv.drawRRect(tira, paint(VELCRO_ESC, 255, "stroke", 2.2))
    cv.restore()
    cv.drawPath(tn, paint("#5C6B7A", 220, "stroke", 3.0))
    return corpo


X_PERNAS_FRENTE = (420.0, 660.0)
Y_FR = dict(bainha=600.0, joe=795.0, tor=995.0, chao=1100.0)
R_JOE_FRENTE = 57.0
I_CHEIO = 1                                                      # o joelho da direita (na tela) está mais cheio


def contorno_cheio():
    x = X_PERNAS_FRENTE[I_CHEIO]; y = Y_FR["joe"]; r = R_JOE_FRENTE
    return x, y - r * 0.15, r * 1.17 + 22, r * 1.19 + 26


def frente(cv, t, T):
    """Câmera 2: as duas pernas de frente, paradas, no piso de madeira (tela, dentro do monitor)."""
    yc = Y_FR["chao"]
    for r, (y0, y1, n) in enumerate(((yc - 70, yc - 20, 7), (yc - 20, yc + 50, 6), (yc + 50, CENA.bottom(), 5))):
        cv.drawRect(skia.Rect(CENA.left(), y0, CENA.right(), y1), paint(MADEIRA[r % 3]))
        for i in range(n + 1):                                   # juntas em perspectiva
            xb = CENA.left() + (CENA.width()) * i / n + (30 if r % 2 else 0)
            cv.drawLine(xb, y0, xb + (xb - 540) * 0.08, y1, paint(MADEIRA_JUNTA, 255, "stroke", 3))
        cv.drawLine(CENA.left(), y0, CENA.right(), y0, paint(MADEIRA_JUNTA, 255, "stroke", 3))
    cv.drawLine(CENA.left(), yc - 70, CENA.right(), yc - 70, paint("#E9D2B8", 200, "stroke", 4))
    profundidade(cv, yc - 70)
    for i, x in enumerate(X_PERNAS_FRENTE):
        cv.drawOval(skia.Rect(x - 78, Y_FR["tor"] + 80, x + 78, Y_FR["tor"] + 102), paint("#000000", 100, blur=7))
    for i, x in enumerate(X_PERNAS_FRENTE):
        _perna_frente(cv, x, Y_FR["bainha"], Y_FR["joe"], Y_FR["tor"], R_JOE_FRENTE, i == I_CHEIO, -1 if i == 0 else 1)
    # short de frente: duas pernas do short + gancho no meio, friso branco nas laterais
    sh = skia.Path()
    xl, xr = X_PERNAS_FRENTE
    sh.moveTo(xl - 80, CENA.top() - 10); sh.lineTo(xr + 80, CENA.top() - 10)
    sh.lineTo(xr + 74, Y_FR["bainha"]); sh.lineTo(xr - 70, Y_FR["bainha"] + 6)
    sh.lineTo((xl + xr) / 2, Y_FR["bainha"] - 70)
    sh.lineTo(xl + 70, Y_FR["bainha"] + 6); sh.lineTo(xl - 74, Y_FR["bainha"]); sh.close()
    cv.drawPath(sh, paint("#000000", 60, blur=8))
    cv.drawPath(sh, paint(SHORT))
    cv.save(); cv.clipPath(sh, skia.ClipOp.kIntersect, True)
    for x0, x1 in ((xl - 74, xl + 70), (xr - 70, xr + 74)):
        cv.drawLine(x0, Y_FR["bainha"] - 8, x1, Y_FR["bainha"] - 6, paint(SHORT_CL, 255, "stroke", 12))
    for x in (xl - 66, xr + 66):
        cv.drawLine(x, CENA.top(), x + (4 if x > 540 else -4), Y_FR["bainha"], paint(FRISO, 235, "stroke", 10))
    cv.drawLine((xl + xr) / 2, CENA.top(), (xl + xr) / 2, Y_FR["bainha"] - 70, paint(SHORT_LINHA, 160, "stroke", 3))
    cv.restore()
    cv.drawPath(sh, paint(SHORT_LINHA, 230, "stroke", 4))
    # o contorno dourado do joelho mais cheio, traçado no "incha"
    k = prog(t, T["incha"], T["incha"] + 0.35)
    if k > 0:
        x, y, rx, ry = contorno_cheio()
        circulo_mao(cv, x, y, rx, ry, k, 1.0)


# ------------------------------------------------------------------ linha reta dourada (esticou inteiro / para antes)
def _raio_coxa(a):
    """Raio do contorno da coxa a `a` do quadril (o tubo vai de R_QUAD no quadril a R_JOE no joelho)."""
    return lerp(R_QUAD, R_JOE, clamp(a / L1))


FOLGA = 12.0                                                     # a linha corre a 12 unidades da pele


def linha_reta(cv, cam, hip, pe, k, a, tracejada=False):
    """Linha dourada colada à FRENTE da perna.
    * cheia (perna esticada inteira): tangente à frente da coxa na barra do short e à frente da canela no
      tornozelo — corre junto da perna inteira (v1: afastamento fixo, abria ~9° e parecia que a perna não
      alcançava a linha);
    * tracejada (joelho que travou): continua a frente da COXA além do joelho; a canela fica para trás dela."""
    if a <= 0 or k <= 0:
        return
    (kx, ky), (fx, fy), _ = frente_joelho(hip, pe)
    hx, hy = hip
    if tracejada:                                                # eixo da coxa
        L = math.hypot(kx - hx, ky - hy) or 1.0
        ux, uy = (kx - hx) / L, (ky - hy) / L
    else:                                                        # eixo quadril-tornozelo (perna reta)
        L = math.hypot(pe.ax - hx, pe.ay - hy) or 1.0
        ux, uy = (pe.ax - hx) / L, (pe.ay - hy) / L
    nx, ny = -uy, ux
    if nx * fx + ny * fy < 0:                                    # para a FRENTE do joelho
        nx, ny = -nx, -ny
    a0 = HEM + 6
    o0 = _raio_coxa(a0) + FOLGA
    if tracejada:
        o1 = R_JOE + FOLGA                                       # frente do joelho: a reta da coxa, prolongada
        a1 = L1
        a_fim = L1 + L2 + 10
        o_fim = o0 + (o1 - o0) * (a_fim - a0) / (a1 - a0)
    else:
        a_fim = L - 4
        o_fim = R_TOR + FOLGA
    p0 = (hx + ux * a0 + nx * o0, hy + uy * a0 + ny * o0)
    p1 = (hx + ux * a_fim + nx * o_fim, hy + uy * a_fim + ny * o_fim)
    s0 = na_tela(cam, *p0); s1 = na_tela(cam, *p1)
    kk = e_out(k)
    e = (lerp(s0[0], s1[0], kk), lerp(s0[1], s1[1], kk))
    sombra = paint("#000000", int(110 * a), "stroke", 16, blur=4)
    ouro = paint(OURO, int(255 * a), "stroke", 10)
    if tracejada:
        for pt in (sombra, ouro):
            pt.setPathEffect(skia.DashPathEffect.Make([30.0, 18.0], 0))
    pth = skia.Path(); pth.moveTo(*s0); pth.lineTo(*e)
    cv.drawPath(pth, sombra); cv.drawPath(pth, ouro)


# ------------------------------------------------------------------ o mundo (dentro do monitor)
OBTURADOR = {"play": 0.04, "volta": 0.03, "avanca": 0.02}      # s de VÍDEO de borrão (v2: menos borrão)
N_AMOSTRAS = 6
CAIXA_PERNAS = skia.Rect(HX0 - 600, Y_CHAO - 800, HX0 + 600, Y_CHAO + 90)


def amostras_borrao(t, T, F):
    """Instantes (vídeo) do borrão de movimento de `t`: só fita 1 em 1×, voltando ou avançando, sem atravessar
    congelamento, nunca antes de t = 0 (o quadro 0 sai nítido)."""
    if fita(t, T) != 1:
        return [t]
    obt = OBTURADOR.get(F.tipo(t))
    if not obt:
        return [t]
    out = [t]
    for i in range(1, N_AMOSTRAS):
        tg = t - obt * i / (N_AMOSTRAS - 1)
        if tg < 0 or fita(tg, T) != 1 or F.tipo(tg) in ("congela", "lenta"):
            break
        out.append(tg)
    return out


def pernas_borradas(cv, t, T, F, s, G_ref):
    """Borrão de movimento (média das poses dentro do obturador, no referencial do chão de agora)."""
    ams = amostras_borrao(t, T, F)
    if len(ams) == 1:
        hy, perto, longe, _ = pose(t, T, F)
        return pernas(cv, (HX0, hy), perto, longe, s)
    cv.saveLayer(CAIXA_PERNAS, None)
    kp = None
    for k, tg in enumerate(reversed(ams)):
        hy, perto, longe, _ = pose(tg, T, F)
        if k == 0:
            kp = pernas(cv, (HX0, hy), perto, longe, s)
        else:
            cv.saveLayer(CAIXA_PERNAS, _alfa(1.0 / (k + 1)))
            kp = pernas(cv, (HX0, hy), perto, longe, s)
            cv.restore()
    cv.restore()
    return kp


def lento_k(t, T):
    """0..1: quanto a câmera lenta está LIGADA (selo e âmbar existem só aqui): "câmera" -> "seguiu" e
    "atenção" -> "aí"; apaga ANTES de o filme voltar a 1×."""
    return max(prog(t, T["camera"], T["camera"] + 0.18) * (1 - prog(t, T["seguiu"] - 0.2, T["seguiu"] - 0.02)),
               prog(t, T["atencao"], T["atencao"] + 0.18) * (1 - prog(t, T["ai"] - 0.2, T["ai"] - 0.02)))


def monitor(cv, t, T, F, limpo=False):
    """Tudo o que fica DENTRO do monitor de replay (recortado em CENA). `limpo`: miniatura."""
    tipo = F.tipo(t)
    f = fita(t, T)
    cam = camera(t, T)
    if tipo == "volta":                                          # tremidinha de fita voltando
        j = math.sin(t * 97) * 4 + math.sin(t * 41) * 3
        cam = (cam[0], cam[1], cam[2], cam[3] + j, cam[4])
    for tc in (T["agora"], T["joelho2"], t_perfil2(T)):          # salto de quadro no corte
        if 0 <= t - tc < 0.18 and not limpo:
            j = 30 * math.sin((t - tc) * 140) * (1 - (t - tc) / 0.18)
            cam = (cam[0], cam[1], cam[2], cam[3] + j, cam[4] - j * 0.3)

    cv.save(); cv.clipRect(CENA, True)
    monitor_fundo(cv)
    if frente2(t, T):
        frente(cv, t, T)
    else:
        hy, perto, longe, G = pose(t, T, F)
        hip = (HX0, hy)
        s = cam[0]
        _, gy = na_tela(cam, 0, Y_CHAO)
        cv.save(); aplica(cv, cam)
        cv.translate(0, 0)
        chao(cv, G, s, f)
        sombra_pe(cv, longe); sombra_pe(cv, perto)
        if f == 1 and tipo in OBTURADOR:
            pernas_borradas(cv, t, T, F, s, G)
        else:
            pernas(cv, hip, perto, longe, s)
        # a mão no joelho (fita 2): desce no "vem", segura no "dor" e fica até o corte para a câmera 2
        if f == 2 and t < T["joelho2"]:
            km = k_mao(t, T)
            if km > 0:
                mao(cv, hip, perto, km, s)
        cv.restore()
        profundidade(cv, gy)

        # o "crec": os MESMOS três arcos (mesma forma) nas duas fitas
        for t0, d, esc in janelas_crec(T, F):
            k = (t - t0) / d
            if 0 < k < 1:
                arcos_crec(cv, cam, hip, perto, k, esc)
        if f == 1 and 0 <= t - T["corpo"] - 0.1 < 0.75:           # o "crec" do "corpo" vira brilhos que sobem
            hy_c, perto_c, _, _ = pose(T["corpo"], T, F)            # presos ONDE o crec estalou (no fundo)
            (kx, ky), (fx, fy), _ = frente_joelho((HX0, hy_c), perto_c)
            bx, by = na_tela(camera(T["corpo"], T), kx + fx * 40, ky + fy * 40)
            brilhos_sobem(cv, bx, by, t, T["corpo"] + 0.1)

        # "repara": círculo dourado em volta do joelho (fica; pulsa no "estalou"; sai no "esticou")
        if T["repara"] <= t < T["esticou"] + 0.25 and f == 1:
            (kx, ky), (fx, fy), _ = frente_joelho(hip, perto)
            cx_, cy_ = na_tela(cam, kx + fx * 8, ky + fy * 8)
            puls = 1 + 0.12 * math.sin(math.pi * clamp((t - T["estalou"]) / 0.3)) if t >= T["estalou"] else 1.0
            r = R_JOE * 1.45 * s * puls
            circulo_mao(cv, cx_, cy_, r * 1.12, r, prog(t, T["repara"], T["repara"] + 0.35),
                        1 - prog(t, T["esticou"], T["esticou"] + 0.25))

        # "inteirinho": linha reta dourada por fora da perna esticada (sai no "seguiu")
        if T["inteirinho"] <= t < T["seguiu"] + 0.1 and f == 1:
            linha_reta(cv, cam, hip, perto, prog(t, T["inteirinho"] + 0.05, T["inteirinho"] + 0.4),
                       1 - prog(t, T["seguiu"] - 0.06, T["seguiu"] + 0.06))

        # "dor": círculo em volta da mão no joelho (congelado)
        if f == 2 and T["dor2"] <= t < T["joelho2"]:
            c = mao_centro(hip, perto)
            cx_, cy_ = na_tela(cam, *c)
            circulo_mao(cv, cx_, cy_, 66 * s, 58 * s, prog(t, T["dor2"] + 0.08, T["dor2"] + 0.43), 1.0)

        # "estica" (congelado depois dos quiques): a linha volta TRACEJADA, seguindo a coxa além do joelho; a
        # canela fica para trás dela (v2: sem o arco do ângulo, que o leitor às cegas não entendeu)
        tcg = t_congela_trava(T)
        if f == 2 and t >= tcg:
            linha_reta(cv, cam, hip, perto, prog(t, tcg + 0.05, tcg + 0.42), 1.0, tracejada=True)

    # efeitos de replay
    varredura(cv, t, lento_k(t, T), limpo)
    if not limpo:
        faixas_tracking(cv, t, {"volta": 1.0, "avanca": 0.7}.get(tipo, 0.0))
        if tipo in ("volta", "avanca"):                          # ◀◀ / ▶▶ grande no canto
            t0 = F.inicio_trecho(t)
            _setas(cv, 96, 410, (0.55 + 0.45 * (math.sin((t - t0) * 16) > -0.3)) * prog(t, t0, t0 + 0.06), 2.2, tipo == "avanca")
        for t0, fo in ((T["inteirinho"], 1.0), (T["dor2"], 0.9), (t_congela_trava(T), 0.9)):
            flash(cv, t, t0, fo)
        corte_fita(cv, t, T["agora"] - 0.02)
    cv.restore()
    return cam


# ------------------------------------------------------------------ "melhores momentos" (aí sim, procure avaliação)
def momentos(T):
    """Os congelamentos dos 3 sinais, na ordem da fala: mão no joelho, joelho mais cheio, joelho que para dobrado."""
    return ((T["ai"], T["dor2"] + 0.5), (T["sim"], T["incha"] + 0.32), (T["procure"], t_congela_trava(T) + 0.45))


def miniatura(T, F, tt):
    chave = ("mini", round(tt, 3))
    if chave not in _CACHE:
        sf = skia.Surface(int(CENA.width()), int(CENA.height())); c = sf.getCanvas(); c.clear(_c(BG_OUT))
        c.translate(-CENA.left(), -CENA.top())
        fundo_cl(c, tt)
        monitor(c, tt, T, F, limpo=True)
        _CACHE[chave] = sf.makeImageSnapshot()
    return _CACHE[chave]


MW, MH = 292, 263                                                # miniatura (proporção da CENA)
CW_MINI = 620.0                                                  # recorte da cena que vai na miniatura (aproxima o sinal)


def recorte_mini(T, F, i, tt):
    """Retângulo (coordenadas da imagem da CENA) em volta do sinal de cada miniatura."""
    if i == 1:                                                   # as duas pernas de frente, na altura dos joelhos
        cx, cy = 540.0, Y_FR["joe"] + 40
    else:
        hy, perto, longe, _ = pose(tt, T, F)
        cam = camera(tt, T)
        if i == 0:
            cx, cy = na_tela(cam, *mao_centro((HX0, hy), perto))
            cx -= 40; cy += 40
        else:
            (kx, ky), _, _ = frente_joelho((HX0, hy), perto)
            cx, cy = na_tela(cam, kx, ky)
            cy += 60
    w, h = CW_MINI, CW_MINI * MH / MW
    x0 = clamp(cx - CENA.left() - w / 2, 0, CENA.width() - w)
    y0 = clamp(cy - CENA.top() - h / 2, 0, CENA.height() - h)
    return skia.Rect(x0, y0, x0 + w, y0 + h)


def melhores_momentos(cv, t, T, F):
    """Sem texto: a cena escurece e as 3 miniaturas entram uma por batida; o estetoscópio vem na "avaliação".
    SEGURAM até a CTA (respiram de leve), sem voltar à fita 1. v2: escurecimento quase total (a pose de fundo não
    vaza por baixo) e, na CTA, miniaturas e estetoscópio APAGAM até 12% — o texto da CTA fica sobre fundo liso."""
    if t < T["ai"] - 0.05:
        return
    cv.save(); cv.clipRect(CENA, True)
    img = _img("escurece", CENA.width(), CENA.height(), lambda c: c.clear(_c(BG_OUT, 255)))
    _blit(cv, img, CENA.left(), CENA.top(), 0.93 * prog(t, T["ai"] - 0.05, T["ai"] + 0.25))
    cta = max(0.12, 1 - prog(t, T["manda"] - 0.3, T["manda"] + 0.2))
    resp = 1.0 + 0.02 * (0.5 - 0.5 * math.cos(max(0.0, t - T["avaliacao"] - 0.6) * 2.4)) if t > T["avaliacao"] + 0.6 else 1.0
    for i, (ti, tt) in enumerate(momentos(T)):
        if t < ti:
            continue
        k = prog(t, ti, ti + 0.32)
        esc = max(0.01, e_back(k)) * resp
        a = prog(t, ti, ti + 0.06) * cta
        cx, cy, giro = 540 + (i - 1) * 322, 790 + (1 - e_out(k)) * 50, (-4.0, 2.5, -2.5)[i]
        cv.save(); cv.translate(cx, cy); cv.rotate(giro * e_out(k)); cv.scale(esc, esc)
        borda = skia.RRect.MakeRectXY(skia.Rect(-MW / 2 - 9, -MH / 2 - 9, MW / 2 + 9, MH / 2 + 9), 14, 14)
        sombra = skia.RRect.MakeRectXY(skia.Rect(-MW / 2 - 3, -MH / 2 + 1, MW / 2 + 15, MH / 2 + 19), 14, 14)
        cv.drawRRect(sombra, paint("#000000", int(110 * a), blur=12))
        cv.drawRRect(borda, paint("#F4F7FA", int(255 * a)))
        dentro = skia.RRect.MakeRectXY(skia.Rect(-MW / 2, -MH / 2, MW / 2, MH / 2), 8, 8)
        cv.save(); cv.clipRRect(dentro, True)
        cv.drawImageRect(miniatura(T, F, tt), recorte_mini(T, F, i, tt), skia.Rect(-MW / 2, -MH / 2, MW / 2, MH / 2),
                         skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kNone), _alfa(a))
        cv.restore()
        cv.drawRRect(borda, paint(OURO, int(255 * a * (0.55 + 0.45 * (1 - prog(t, ti + 0.1, ti + 0.6)))), "stroke", 4))
        cv.restore()
    a_e = prog(t, T["avaliacao"], T["avaliacao"] + 0.2) * cta
    if a_e > 0:
        estetoscopio(cv, 540, 505, 1.3 * e_back(prog(t, T["avaliacao"], T["avaliacao"] + 0.3)) * resp, a_e)
    cv.restore()


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep, F):
    fundo_cl(cv, t)
    monitor(cv, t, T, F)
    melhores_momentos(cv, t, T, F)

    fim = 1 - prog(t, T["manda"] - 0.4, T["manda"] - 0.1)
    cantoneiras(cv, fim)
    painel(cv, t, T, F, fim)

    # SÓ SOM: responde a 1ª metade do gancho, na área livre à direita (sai no "costuma")
    carimbo_ouro(cv, "SÓ SOM", 850, 800, -7, T["so2"], t, dur=T["costuma"] - T["so2"] + 0.3)

    # gancho (sai na volta da fita) e selo da série (SÓ com a câmera lenta ligada)
    capa(cv, t, T["volta"], ep["gancho"][0], ep["gancho"][1])
    selo_lenta(cv, lento_k(t, T) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    if t >= 0.5 / FPS:                                          # quadro 0 (capa): o gancho é o ÚNICO texto grande
        interface(cv, t, T, blocos, DESTAQUE)


def selo_lenta(cv, lk):
    """(cópia do piloto)"""
    if lk <= 0:
        return
    esc = lerp(0.55, 1.0, e_back(lk))
    cv.save(); cv.translate(CX, 177); cv.scale(esc, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-205, -31, 205, 31), 31, 31)
    cv.drawRRect(rr, paint(AMBAR, int(90 * lk), blur=16))
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(225 * lk)))
    cv.drawRRect(rr, paint(AMBAR, int(60 * lk)))
    cv.drawRRect(rr, paint(OURO, int(255 * lk), "stroke", 3.5))
    texto(cv, "CÂMERA LENTA", 0, 14, F_BLACK, 38, OURO, int(255 * lk))
    cv.restore()


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
    """Fita correndo: cliques que aceleram + tom que desliza de f0 a f1 + chiado."""
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
    """Fita avançando: cliques rápidos + tom que sobe (no trecho longo, o tom sobe só no começo)."""
    y = _fita(min(dur, 1.2), 380, 1500, 0.07, 0.9, 78) * 0.85
    if dur <= 1.2:
        return y
    SR = som.SR                                                  # depois, só cliques rápidos e chiado leve
    n = int(dur * SR); out = np.zeros(n); out[:len(y)] += y
    clk = som.click(); tt = 1.2
    while tt < dur - 0.05:
        p = int(tt * SR); m = min(len(clk), n - p)
        out[p:p + m] += clk[:m] * 0.9
        tt += 0.045
    t = np.arange(n) / SR
    rui = som._noise(n, 81); rui = rui - np.convolve(rui, np.ones(12) / 12, "same")
    env = np.clip((t - 1.1) / 0.1, 0, 1) * np.clip((dur - t) / 0.15, 0, 1)
    out += rui * 0.03 * env
    return out


def chiado(dur=0.28):
    SR = som.SR
    n = int(dur * SR); t = np.arange(n) / SR
    rui = som._noise(n, 79); rui = rui - np.convolve(rui, np.ones(4) / 4, "same")
    env = np.clip(t / 0.005, 0, 1) * np.clip((dur - t) / 0.12, 0, 1)
    y = rui * env * 0.55
    c = som.click(); y[:len(c)] += c[:n] * 1.4
    return y


def congelar():
    """Tique seco + 'clac' curto (o quadro trava)."""
    SR = som.SR
    y = som.tick() * 1.0
    n = int(0.12 * SR); t = np.arange(n) / SR
    z = np.sin(2 * np.pi * np.cumsum(220 * np.exp(-t * 30) + 90) / SR) * som._env(n, 0.001, 0.03) * 0.5
    out = np.zeros(max(len(y), n)); out[:len(y)] += y; out[:n] += z
    return out


def _banda(x, w_alto, w_baixo):
    """Passa-faixa barato: média curta (corta o agudo demais) menos média longa (corta o grave)."""
    a = np.convolve(x, np.ones(w_alto) / w_alto, "same")
    return a - np.convolve(a, np.ones(w_baixo) / w_baixo, "same")


def crec(esticado=1.0, eco=False):
    """O "crec" do episódio: estalo SUAVE e seco — 2 cliques a 12 ms (corpo na faixa de 2-3 kHz) + micro-chiado
    agudo, SEM grave (nada de osso quebrando). `esticado` ~2 na câmera lenta: mais longo, MESMA faixa de tom,
    com eco curto."""
    SR = som.SR
    dur = 0.12 * esticado + (0.25 if eco else 0.0)
    n = int(dur * SR); y = np.zeros(n)
    for i, (t0, g, f) in enumerate(((0.0, 1.0, 2350.0), (0.012 * esticado, 0.8, 2900.0))):
        m = int(0.012 * esticado * SR); p = int(t0 * SR)
        tt = np.arange(m) / SR
        corpo = np.sin(2 * np.pi * f * tt) * som._env(m, 0.0002, 0.0022 * esticado)
        ruido = _banda(som._noise(m, 300 + i), 3, 14) * som._env(m, 0.0001, 0.0012 * esticado) * 0.9
        y[p:p + m] += (corpo + ruido) * g
    m = int(0.03 * esticado * SR); p = int(0.018 * esticado * SR)
    y[p:p + m] += _banda(som._noise(m, 310), 3, 9) * som._env(m, 0.001, 0.007 * esticado) * 0.25
    if eco:
        base = y.copy()
        for d, g in ((0.075, 0.35), (0.15, 0.15)):
            k = int(d * SR)
            y[k:] += base[:n - k] * g
    return y * 0.85


def janelas(T, F, dur):
    """Ganho da batida e da harmonia ao longo do tempo: a batida some na câmera lenta."""
    xs = np.arange(0, dur + 0.01, 0.01)
    gb = np.ones_like(xs); gh = np.ones_like(xs)
    for i, x in enumerate(xs):
        tp = F.tipo(x)
        gb[i] = {"play": 1.0, "lenta": 0.0, "congela": 0.45, "volta": 0.2, "avanca": 0.8}[tp]
        gh[i] = {"play": 1.0, "lenta": 0.8, "congela": 0.9, "volta": 0.55, "avanca": 0.8}[tp]
    k = np.ones(15) / 15
    gb = np.convolve(np.pad(gb, 7, mode="edge"), k, "valid"); gh = np.convolve(np.pad(gh, 7, mode="edge"), k, "valid")
    return xs, gb, gh


def _media_movel(x, w):
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


def pousos(T, F):
    """Instantes (vídeo) em que os tênis tocam o chão na fita 1, só com o filme andando para a frente."""
    out = []
    ant = None
    x = 0.0
    anda = ("play", "lenta", "avanca")
    while x < T["agora"]:
        tipo = F.tipo(x); tf = F.tf(x)
        if ant is not None and tipo in anda and ant[0] in anda and 0 < tf - ant[1] < 0.2:
            if math.floor(tf / P_CICLO) > math.floor(ant[1] / P_CICLO):
                nome, ganho = {"lenta": ("tick", 0.4), "avanca": ("click", 0.18)}.get(tipo, ("thump", 0.3))
                out.append((x, nome, ganho))
        ant = (tipo, tf)
        x += 1 / 240
    return out


def sons(T, F):
    """v2: o "crec" a 1× cai no respiro entre "crec?" e "Volta" e sobe ~5 dB (na v1 a palavra o cobria); o ▶▶ só
    no "seguiu pulando"; a explicação a 1× tem o MESMO crec no "tendão", na "bolha" e no "corpo"; o "trava"
    tem o batente e o 2º quique audíveis."""
    ev = pousos(T, F)
    tl = t_lock_trava(T)
    tcg = t_congela_trava(T)
    ev += [(t_crec1(T) - 0.02, crec, 0.95),
           (T["volta"], lambda: rebobinar(T["camera"] - T["volta"]), 0.9),
           (T["camera"], "pop", 0.55),
           (T["repara"], lambda: som.whoosh(0.22, 11), 0.3),
           (T["estalou"], lambda: crec(2.0, True), 0.55),
           (T["inteirinho"], congelar, 1.0), (T["inteirinho"] + 0.05, "shimmer", 0.4),
           (T["seguiu"], lambda: avancar(T["sem1"] - T["seguiu"] - 0.03), 0.45),
           (T["so2"], "thump", 0.8),
           (T["tendao"] - 0.02, crec, 0.5), (T["bolha"] - 0.02, crec, 0.5), (T["corpo"] - 0.02, crec, 0.5),
           (T["corpo"] + 0.1, "shimmer", 0.45),
           (T["agora"] - 0.04, chiado, 0.7),
           (T["atencao"], "pop", 0.55),
           (T["estalo"], lambda: crec(2.0, True), 0.55),
           (T["dor2"], congelar, 0.9),
           (T["joelho2"], "tick", 0.55),
           (T["incha"], lambda: som.whoosh(0.22, 13), 0.3),
           (t_perfil2(T), "tick", 0.45),
           (tl, "thump", 0.55), (tl + QUIQUES[1][0], "thump", 0.3),
           (tcg, congelar, 0.85)]
    ev += [(ti, lambda: som.whoosh(0.3, 14), 0.35) for ti, _ in momentos(T)]
    ev += [(T["avaliacao"] + 0.02, "ding", 0.45), (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def tempos_previa(T, F):
    tl, tcg, tp = t_lock_trava(T), t_congela_trava(T), t_perfil2(T)
    return (0.0, 0.35, t_crec1(T), T["volta"] + 0.35, T["camera"] + 0.15, T["camera"] + 0.6,
            T["so1"] + 0.05, T["alerta"] + 0.2, T["repara"] + 0.45, T["junto"] + 0.3, T["estalou"] + 0.2,
            T["estalou"] + 0.5, T["esticou"] + 0.2, T["inteirinho"] + 0.45, T["seguiu"] + 0.25, T["pulando"] + 0.3,
            T["sem1"] + 0.3, T["inchaco"] + 0.3, T["so2"] + 0.3, T["costuma"] + 0.3, T["tendao"] + 0.05,
            T["bolha"] + 0.05, T["coisa"] + 0.1, T["corpo"] + 0.05, T["corpo"] + 0.35, T["agora"] + 0.05,
            T["agora"] + 0.4, T["atencao"] + 0.3, T["estalo"] + 0.2, T["vem2"] + 0.2, T["dor2"] + 0.5,
            T["joelho2"] + 0.2, T["incha"] + 0.3, tp + 0.05, tp + 0.3, tl, tl + 0.08, tl + 0.24, tcg + 0.5,
            T["ai"] + 0.3, T["sim"] + 0.3, T["procure"] + 0.3, T["avaliacao"] + 0.4, T["manda"] - 0.6,
            T["manda"] + 1.2, T["total"] - 1 / 30)


# ------------------------------------------------------------------ entrada única (réplica do cf_comum.fazer_render, com mix próprio)
def render(ep, mp4, tmp, previa=False):
    roteiro = "\n".join(ep["roteiro"])
    voz_bruta, palavras = _voz.narrar(roteiro, _voz.RITMO_COMO_FUNCIONA, os.path.join(tmp, "voz"))
    voz_c, pal, tirado = comprimir(voz_bruta, palavras, respiro_cta=RESPIRO_CTA)
    pal = alinhar(pal, roteiro)
    T = ancoras(pal, ANCORAS)
    print(f"{ep['id']}: silêncio cortado {tirado:.2f}s | duração final {T['total']:.2f}s")
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
