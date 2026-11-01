# -*- coding: utf-8 -*-
"""CÂMERA LENTA (série nova) — episódio "TROPEÇA NO / PRÓPRIO PÉ?" (andar de pombinho, tema pe_virado).

Mesma mecânica do piloto cf_cameralenta_ponta_pes: um REPLAY de TV. Uma criança pequena corre no quintal, DE
FRENTE para a câmera (do short para baixo, descalça), atrás de uma bola, e tropeça no próprio pé em 1× (o
enganche fica dentro do borrão). A fita VOLTA e a CÂMERA LENTA revê o lance: a ponta do pé que vai balançar
está virada para dentro (linha pontilhada da direção da corrida, seta no eixo do pé, arco do ângulo, presos ao
pé) e, nesse passo, ela engancha no tornozelo do outro (congela, traços de "pop" só nos vãos, atrás das pernas). O tempo do
filme (`Filme.tf`) é separado do tempo do vídeo; a narração nunca para nem desacelera.

Depois:
  * CÂMERA 2 (de cima, faixa de terra): as pegadas da corrida, uma a uma, com a ponta para a linha do meio e
    a linha pontilhada da direção passando reta entre elas; o pombo atravessa SEPARADO (o nome, nunca a criança).
  * Diagrama em 1× (sem selo), criança PARADA: três anéis iguais (PÉ, CANELA, COXA) nas DUAS pernas — o vídeo
    não escolhe de onde vem o giro; a cada palavra as pontas viram mais um pouco para dentro (o que é "giro").
  * ▶▶ no quintal + calendário sem número: a regra é o tempo. Nenhum pé endireita na tela.
  * Corte de fita -> FITA 2 (casa, piso de madeira). Câmera lenta: só UM pé vira (SÓ DE UM LADO); congela com a
    mão da criança segurando a canela (DOR); ▶▶ com três desequilíbrios (pés sempre no chão), um pontinho
    dourado por tropeço (QUEDAS DEMAIS); câmera 2 sobre o tapete: as duas fileiras na tela DURANTE a palavra, a
    seguinte mais virada, arco maior (PIORA). Respiros curtos depois de cada pergunta do alerta (PAUSAS).
  * Melhores momentos: as 4 miniaturas GRANDES (grade 2×2), uma por batida, e o estetoscópio no meio; o celular
    (sem mão) filma a criança e a linha vai até o estetoscópio (ajuda na consulta); no "não" a tela do celular
    para e apaga, sem marca nenhuma; no "diagnóstico" o estetoscópio pulsa com um anel dourado. Segura até a
    CTA (sem voltar à fita 1).

Regras da série e do verificador (storyboard.json), todas aqui:
  * Selo CÂMERA LENTA só com a câmera lenta ligada ("câmera" -> "andar" e "só" -> "quedas"); nunca no 1×, no
    ◀◀, no ▶▶, no diagrama, no corte de fita, nas miniaturas ou na CTA. A moldura âmbar segue a mesma janela.
  * VERMELHO PROIBIDO (nem no ponto de gravação do celular, nem estrela de dor, nem pés do pombo).
  * Descalça no vídeo inteiro; nenhum adulto em cena; o celular aparece sozinho.
  * Pernas OPACAS e esquemáticas: nada por dentro, sem osso, sem fundo de chapa.
  * Tropeço SEM machucado e sem piada (sem som cômico); dor = mão na canela, sem rosto.
  * Nada de ❚❚, barra de progresso, timecode ou dígitos: congelar = flash + tique + chip esmaecido.
  * Nenhum texto além do `tela` (CÂMERA LENTA, 1×, 0,25×, PÉ, CANELA, COXA, SÓ DE UM LADO, DOR, QUEDAS DEMAIS,
    PIORA), do gancho e da interface. ◀◀ e ▶▶ são formas.

Helpers COPIADOS (não importados), como manda o contrato: Filme (adaptado), efeitos de replay, painel,
relogio (orig. cf_andador), chip_c, _setas, circulo_mao, estetoscopio, calendario (cabeçalho azul-claro),
selo_lenta, trilha_partes, _fita, rebobinar, avancar, chiado, congelar, janelas, _media_movel, mixar_cl (cf_
cameralenta_ponta_pes); corte_fita(dur), mão de criança e cotovelo (cf_cameralenta_joelho_estala); pe_forma,
_piso (adaptado), anel, seta_arco, rotulo_anel, pegada, pombo (cf_pe_virado, sem vermelho). Importados sem
cópia: capa/interface/ancoras (cf_comum), comprimir/alinhar/montar_blocos (cf_fratura_cola), paleta e texto
(cf_alongamento). A cena é PRESA ao roteiro pelas palavras-âncora (ANCORAS): roteiro sem elas = KeyError.
"""
import math
import os

import numpy as np
import skia

from . import som, voz as _voz
from .base import FPS, codificar, previas as _previas
from .cf_alongamento import (BG_OUT, CX, F_BLACK, H, OSSO_B, OSSO_C, OURO, PART, W, clamp, e_back, e_inout,
                             e_out, lerp, lerpc, paint, prog, texto)
from .cf_comum import ancoras, capa, interface
from .cf_fratura_cola import alinhar, comprimir, montar_blocos

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "tropeca": ("tropeça", 1, False), "pe1": ("pé", 1, False), "volta": ("volta", 1, False),
    "camera": ("câmera", 1, False), "lenta": ("lenta", 1, False), "repara": ("repara", 1, False),
    "ponta": ("ponta", 1, False), "pe2": ("pé", 2, False), "virou": ("virou", 1, False),
    "dentro": ("dentro", 1, False), "esbarrou": ("esbarrou", 1, False), "outro": ("outro", 1, False),
    "andar": ("andar", 1, False), "pombinho": ("pombinho", 1, False), "pode": ("pode", 1, False),
    "giro": ("giro", 1, False), "pe3": ("pé", 3, False), "canela": ("canela", 1, False),
    "coxa": ("coxa", 1, False), "regra": ("regra", 1, False), "tempo": ("tempo", 1, False),
    "rotacao": ("rotação", 1, False), "sozinha": ("sozinha", 1, False), "o2": ("o", 2, False),
    "alerta": ("alerta", 1, False), "so": ("só", 1, False), "lado": ("lado", 1, False),
    "dor": ("dor", 1, False), "quedas": ("quedas", 1, False), "piora": ("piora", 1, False),
    "ai": ("aí", 1, False), "vale": ("vale", 1, False), "ortopedista": ("ortopedista", 1, False),
    "olhar": ("olhar", 1, False), "filmar": ("filmar", 1, False), "ajuda": ("ajuda", 1, False),
    "nao": ("não", 1, False), "diagnostico": ("diagnóstico", 1, False), "manda": ("manda", 1, False),
}
DESTAQUE = {"tropeça", "próprio", "pé", "ponta", "dentro", "esbarrou", "outro", "pombinho", "giro", "canela",
            "coxa", "regra", "tempo", "rotação", "sozinha", "alerta", "lado", "dor", "quedas", "piora",
            "ortopedista", "filmar", "ajuda", "diagnóstico"}
RESPIRO_CTA = 1.6
# todo texto desenhado (fora gancho e interface) — todos em ep["tela"]
R_SELO, R_1X, R_LENTA = "CÂMERA LENTA", "1×", "0,25×"
R_PE, R_CANELA, R_COXA = "PÉ", "CANELA", "COXA"
R_LADO, R_DOR, R_QUEDAS, R_PIORA = "SÓ DE UM LADO", "DOR", "QUEDAS DEMAIS", "PIORA"

# ------------------------------------------------------------------ paleta (sem vermelho)
PELE, PELE_CL, PELE_ESC, PELE_LINHA = "#F0B49A", "#F7CDB8", "#DA987E", "#B9765E"
SHORT, SHORT_CL, SHORT_ESC, SHORT_LINHA = "#F4A6C6", "#FAC9DD", "#DE88AB", "#A8577A"
BOLSO, BOLSO_LINHA = "#FFFFFF", "#E7AFC6"
GRAMA = ("#4C8A43", "#589A4D")
GRAMA_LONGE = "#3D6F3B"
SEBE, SEBE_CL = "#284A31", "#376442"
FIAPO = "#86C766"
BOLA_BR, BOLA_AZ, BOLA_LINHA = "#F6F8FA", "#9CC9FF", "#7F95AA"
MADEIRA = ("#6C4731", "#5F3D29", "#77513A")
MADEIRA_JUNTA, MADEIRA_VEIO = "#3A2518", "#82603F"
PAREDE, PAREDE_CL, RODAPE = "#2E4459", "#36506A", "#DCD3C4"
TERRA, TERRA_CL, TERRA_ESC = "#946E4B", "#A9835D", "#7C5B3C"
TAPETE, TAPETE_BORDA, TAPETE_LISTRA = "#6F879C", "#4F667B", "#678095"
FUNDO_CARTAO = "#0B1824"
AMBAR = "#FFB547"
AZUL_CL = "#9CC9FF"
CEL, CEL_BORDA, CEL_TELA = "#141E28", "#F2F5F8", "#22313F"
POMBO_CORPO, POMBO_CAB, POMBO_ASA, POMBO_ESC = "#9DADBF", "#B2C0CE", "#7F92A8", "#4E6075"
POMBO_PESC, POMBO_PE = "#6FA59A", "#E2B48C"                     # pés cor de pêssego (nada de vermelho)

# ------------------------------------------------------------------ o "monitor" de replay (tela)
CENA = skia.Rect(40, 330, 1040, 1230)                            # o mundo é recortado aqui (selo e karaokê livres)

# ------------------------------------------------------------------ mundo, vista DE FRENTE (= tela na câmera BASE)
Y_PISO = 1000.0                                                  # chão sob o tornozelo, na profundidade 0
HIP_Y = 610.0                                                    # altura das articulações do quadril
HIP_DX = 94.0                                                    # meia distância entre as pernas
KZ = 0.42                                                        # profundidade (para a câmera) -> y de tela
R_QUAD, R_JOE, R_TOR = 62.0, 46.0, 30.0                          # pernas gordinhas de pré-escolar
PE_L, PE_W, K_PE = 124.0, 88.0, 0.62                             # pé (comprimento, largura, escorço no chão)
L_PERNA = Y_PISO - 12.0 - HIP_Y                                  # quadril -> tornozelo, de pé
HZ = 700.0                                                       # horizonte (y do mundo)
C_G, D_F = 1500.0, 5.0                                           # perspectiva do chão: y = HZ + C_G / D; pés em D_F

# fita 1 (quintal): corrida com a ponta dos DOIS pés levemente para dentro
P1, SD1, ZS1, LIFT1, MED1, YAW1 = 0.55, 0.56, 100.0, 72.0, 10.0, 20.0
WC = 0.45                                                        # o enganche: fração do balanço do pé A
UC = SD1 + WC * (1 - SD1)                                        # fase de A no contato
SW1 = (1 - SD1) * P1                                             # duração do balanço
TF_C = 20.0                                                      # tempo de FILME do contato
T1C = 1.20                                                       # tempo de VÍDEO do contato no 1× (logo após "pé")
HOLD = 0.04                                                      # o pé fica enganchado (filme)
T_POUSO = TF_C + (1 - WC) * SW1                                  # o passo de recuperação pousa aqui
VEL1 = 2 * ZS1 * KZ / (SD1 * P1) * D_F * D_F / C_G               # o chão corre junto com o pé de apoio
# fita 2 (casa): andando; só o pé da DIREITA (na tela) vira para dentro
P2, SD2, ZS2, LIFT2, MED2, YAW2 = 0.95, 0.62, 66.0, 38.0, 6.0, 22.0
TF2 = 100.0                                                      # o pé marcado pousa NO "só"
VEL2 = 2 * ZS2 * KZ / (SD2 * P2) * D_F * D_F / C_G
QUEDAS_FR = (0.20, 0.52, 0.84)                                   # os 3 tropeços: frações do ▶▶ "quedas" -> "piora"
QD = 0.8                                                         # duração de cada tropeço (filme)
# respiros curtos DEPOIS de cada pergunta do alerta (o leigo lê um sinal por vez; a voz não muda de ritmo)
PAUSAS = (("lado", 0.24), ("dor", 0.24), ("demais", 0.24), ("piora", 0.30))
V1, VL, VF, VR = 1.0, 0.25, 0.02, 3.0                            # 1×, 0,25×, quase parado, avanço rápido


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
    if k < 0.999:
        pe = skia.TrimPathEffect.Make(0.0, max(0.002, k))
        if pe is not None:
            pt.setPathEffect(pe)
    return pt


def sstep(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


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


# ------------------------------------------------------------------ o que está na tela em cada trecho
def vista(t, T):
    if t < T["andar"]:
        return "corre1"                                         # fita 1: quintal, de frente
    if t < T["pode"]:
        return "trilha"                                         # câmera 2: de cima, faixa de terra
    if t < T["regra"]:
        return "diagrama"                                       # parada, os três anéis
    if t < T["o2"]:
        return "brinca"                                         # ▶▶ no quintal e 1× calmo
    if t < T["piora"]:
        return "casa"                                           # fita 2: piso de madeira
    return "tapete"                                             # câmera 2: de cima, tapete


# ------------------------------------------------------------------ o tempo do filme
class Filme:
    """Liga o tempo do VÍDEO ao tempo do FILME (cópia adaptada do piloto): play (1×), volta (rebobinar), lenta
    (0,25×; o trecho do "repara" quase para), avanca (▶▶), congela (0×). Presos às palavras-âncora."""

    def __init__(self, T):
        s = []
        tf0 = TF_C - V1 * T1C
        a = tf0 + V1 * T["volta"]
        tf_v = TF_C - VL * (T["esbarrou"] - T["virou"])
        tf_r = tf_v - VF * (T["virou"] - T["repara"])
        tf_s = tf_r - VL * (T["repara"] - T["camera"])
        s.append((0.0, T["volta"], "play", tf0, a, None))
        s.append((T["volta"], T["camera"], "volta", a, tf_s, "inout"))
        s.append((T["camera"], T["repara"], "lenta", tf_s, tf_r, None))
        s.append((T["repara"], T["virou"], "lenta", tf_r, tf_v, None))          # freia (quase parado)
        s.append((T["virou"], T["esbarrou"], "lenta", tf_v, TF_C, None))
        s.append((T["esbarrou"], T["outro"], "congela", TF_C, TF_C, None))
        tf_a = TF_C + VL * (T["andar"] - T["outro"])
        s.append((T["outro"], T["andar"], "lenta", TF_C, tf_a, None))
        tf_p = tf_a + V1 * (T["regra"] - T["andar"])
        s.append((T["andar"], T["regra"], "play", tf_a, tf_p, None))             # câmera 2 e diagrama
        tf_soz = tf_p + VR * (T["sozinha"] - T["regra"])
        s.append((T["regra"], T["sozinha"], "avanca", tf_p, tf_soz, None))
        tf_o = tf_soz + V1 * (T["o2"] - T["sozinha"])
        s.append((T["sozinha"], T["o2"], "play", tf_soz, tf_o, None))
        # fita 2: outra tomada (o pé marcado pousa NO "só")
        self.t_dor = T["dor"] + 0.06                                              # congela com a mão na canela
        tf_o2 = TF2 - V1 * (T["so"] - T["o2"])
        s.append((T["o2"], T["so"], "play", tf_o2, TF2, None))
        tf_d = TF2 + VL * (self.t_dor - T["so"])
        s.append((T["so"], self.t_dor, "lenta", TF2, tf_d, None))
        s.append((self.t_dor, T["quedas"], "congela", tf_d, tf_d, None))
        tf_q = tf_d + VR * (T["piora"] - T["quedas"])
        s.append((T["quedas"], T["piora"], "avanca", tf_d, tf_q, None))
        self.quedas_f = tuple(VR * (T["piora"] - T["quedas"]) * f for f in QUEDAS_FR)   # tropeços (filme, após o congelamento)
        fim = T["total"] + 2.0
        s.append((T["piora"], fim, "play", tf_q, tf_q + V1 * (fim - T["piora"]), None))
        self.segs = s
        self.T = T
        self.tf_d = tf_d

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
    return max(prog(t, T["camera"], T["camera"] + 0.18) * (1 - prog(t, T["andar"] - 0.2, T["andar"] - 0.02)),
               prog(t, T["so"], T["so"] + 0.18) * (1 - prog(t, T["quedas"] - 0.2, T["quedas"] - 0.02)))


# ------------------------------------------------------------------ o pé visto de frente (no chão, para a câmera)
class Pe:
    """Pé de frente: `px, py` = ponto do chão sob o tornozelo (tela), `yaw` > 0 = ponta para o meio, `lado` +1 =
    perna da esquerda da tela (o meio fica em +x), `k` = escorço, `sc` = escala de profundidade."""
    __slots__ = ("px", "py", "yaw", "lado", "k", "sc", "z", "h", "calc", "alfa")

    def __init__(self, px, py, yaw, lado, k, sc, z, h, calc, alfa=1.0):
        self.px, self.py, self.yaw, self.lado, self.k, self.sc = px, py, yaw, lado, k, sc
        self.z, self.h, self.calc, self.alfa = z, h, calc, alfa

    def P(self, a, b):
        """(ao longo do pé, através do pé) -> tela. b * lado > 0 = lado de dentro (dedão)."""
        th = math.radians(self.yaw)
        dx, dz = math.sin(th) * self.lado, math.cos(th)
        nx, nz = dz, -dx
        return (self.px + (a * dx + b * nx) * self.sc, self.py + (a * dz + b * nz) * self.k * self.sc)

    def reto(self, a):
        """Ponto a `a` do calcanhar na direção da CORRIDA (reto para a câmera), com o mesmo escorço."""
        return self.px, self.py + a * self.k * self.sc

    def tornozelo(self):
        return self.px, self.py - 12.0 * self.sc

    def dedao(self):
        """Frente do dedão, do lado de dentro (onde ele engancha)."""
        return self.P(PE_L + 4, 0.80 * PE_W / 2 * self.lado)

    def centro(self):
        return self.P(PE_L * 0.42, 0)


def pe_forma(pe):
    """Contorno do pé (superelipse, mais largo nos dedos) e os dedos. (adaptado do cf_pe_virado)"""
    p = skia.Path(); n = 56
    for i in range(n):
        ph = 2 * math.pi * i / n
        cu, su = math.cos(ph), math.sin(ph)
        u = math.copysign(abs(cu) ** 0.7, cu)
        a = lerp(-20, PE_L, (u + 1) / 2)
        b = (PE_W / 2) * math.copysign(abs(su) ** 0.7, su) * (0.80 + 0.20 * (u + 1) / 2)
        (p.moveTo if i == 0 else p.lineTo)(*pe.P(a, b))
    p.close()
    dedos = [(*pe.P(PE_L - 6 + da, f * PE_W / 2 * pe.lado), r * pe.sc) for da, f, r in
             ((-2, 0.62, 13.5), (4, 0.27, 11.0), (4, -0.06, 10.5), (2, -0.38, 9.6), (-4, -0.66, 8.8))]
    return p, dedos


def pe_desenho(cv, pe):
    if pe.alfa <= 0:
        return
    a = pe.alfa
    pth, dedos = pe_forma(pe)
    cx = pe.centro()[0]
    sh = skia.GradientShader.MakeLinear([skia.Point(cx - 62 * pe.sc, 0), skia.Point(cx + 62 * pe.sc, 0)],
                                        [_c(PELE_ESC), _c(PELE), _c(PELE_CL), _c(PELE), _c(PELE_ESC)],
                                        [0.0, 0.22, 0.5, 0.78, 1.0])
    cv.drawPath(pth, paint(PELE, int(255 * a), shader=sh))
    cv.drawPath(pth, paint(PELE_LINHA, int(230 * a), "stroke", 3.0))
    for dx, dy, r in dedos:
        cv.drawCircle(dx, dy, r, paint(PELE_CL, int(255 * a)))
        cv.drawCircle(dx, dy, r, paint(PELE_LINHA, int(220 * a), "stroke", 2.4))


def sombra_pe(cv, pe, y_chao):
    a = (0.3 + 0.7 * clamp(1 - pe.h / 80.0)) * pe.alfa
    if a <= 0:
        return
    cx = pe.centro()[0]
    w = 74 * pe.sc * (1 - 0.25 * clamp(pe.h / 80.0))
    cv.drawOval(skia.Rect(cx - w, y_chao + 22, cx + w, y_chao + 66), paint("#000000", int(85 * a), blur=10))


# ------------------------------------------------------------------ a perna e o short (de frente)
class Perna:
    __slots__ = ("quad", "joe", "tor", "pe", "kj")

    def __init__(self, quad, joe, tor, pe, kj):
        self.quad, self.joe, self.tor, self.pe, self.kj = quad, joe, tor, pe, kj


def _perna(quad, pe, joe=None):
    tor = pe.tornozelo()
    L = math.hypot(tor[0] - quad[0], tor[1] - quad[1])
    kj = clamp((L_PERNA - L) / 130.0)                           # quanto o joelho dobrou (vem para a câmera)
    if joe is None:
        joe = (lerp(quad[0], tor[0], 0.53), lerp(quad[1], tor[1], 0.53) + 16 * kj)
    return Perna(quad, joe, tor, pe, kj)


def _contem_todos(p, pts):
    return all(p.contains(x, y) for x, y in pts)


def _uniao_conferida(fazer, pts, folgas=(0.0, 0.4, 0.9, -0.6)):
    """União de dois tubos que dividem a articulação, CONFERIDA por pontos de dentro. `fazer(dr)` -> (a, b) com
    o círculo da articulação de um deles `dr` px menor. O PathOps do skia erra em algumas poses quando os dois
    tubos trazem o círculo da articulação e SOME um segmento inteiro (achado do chat YouTube, kit16): se algum
    ponto de dentro cair fora, refaz com outra folga e, em último caso, soma os contornos sem união."""
    for dr in folgas:
        a, b = fazer(dr)
        u = skia.Op(a, b, skia.PathOp.kUnion_PathOp)
        if u is not None and _contem_todos(u, pts):
            return u
    a, b = fazer(0.0)
    u = skia.Path(a); u.addPath(b); u.setFillType(skia.PathFillType.kWinding)
    return u


def corpo_perna(pr):
    """Contorno único coxa + joelho + canela, com a união CONFERIDA (meio da coxa, joelho, meio da canela,
    tornozelo)."""
    (hx, hy), (kx, ky), (ax, ay) = pr.quad, pr.joe, pr.tor
    rj = R_JOE * (1 + 0.10 * pr.kj)
    rt = R_TOR * pr.pe.sc
    # (o círculo do joelho da canela é um pouco menor: dois círculos IGUAIS e concêntricos fazem a união do
    # skia perder a canela inteira)
    pts = ((lerp(hx, kx, 0.5), lerp(hy, ky, 0.5)), (kx, ky), (lerp(kx, ax, 0.5), lerp(ky, ay, 0.5)), (ax, ay - 2))
    return _uniao_conferida(lambda dr: (tubo(hx, hy, R_QUAD, kx, ky, rj), tubo(kx, ky, rj * 0.93 - dr, ax, ay, rt)),
                            pts)


def perna_desenho(cv, pr):
    """Perna de desenho de criança, OPACA (coxa + joelho + canela num contorno só)."""
    (hx, hy), (kx, ky), (ax, ay) = pr.quad, pr.joe, pr.tor
    corpo = corpo_perna(pr)
    L = math.hypot(ax - hx, ay - hy) or 1.0
    nx, ny = -(ay - hy) / L, (ax - hx) / L
    mx, my = (hx + ax) / 2, (hy + ay) / 2
    w = 68.0
    sh = skia.GradientShader.MakeLinear([skia.Point(mx - nx * w, my - ny * w), skia.Point(mx + nx * w, my + ny * w)],
                                        [_c(PELE_ESC), _c(PELE), _c(PELE_CL), _c(PELE), _c(PELE_ESC)],
                                        [0.0, 0.22, 0.5, 0.78, 1.0])
    cv.drawPath(corpo, paint(PELE, 255, shader=sh))
    cv.drawPath(corpo, paint(PELE_LINHA, 230, "stroke", 3.2))
    cv.drawArc(skia.Rect(kx - 20, ky - 8, kx + 20, ky + 16), 25, 130, False, paint(PELE_LINHA, 140, "stroke", 3))
    dob = skia.Path(); dob.moveTo(ax - 16 * pr.pe.sc, ay - 6); dob.quadTo(ax, ay - 1, ax + 16 * pr.pe.sc, ay - 6)
    cv.drawPath(dob, paint(PELE_LINHA, 110, "stroke", 2.4))


def short_frente(cv, hc, esc, rot):
    """Short infantil rosa-claro com bolso branco (de frente)."""
    hx, hy = hc
    cv.save(); cv.translate(hx, hy); cv.rotate(rot); cv.scale(esc, esc)
    p = skia.Path()
    p.moveTo(-150, -150); p.lineTo(150, -150); p.lineTo(176, 64); p.lineTo(16, 72); p.lineTo(0, 30)
    p.lineTo(-16, 72); p.lineTo(-176, 64); p.close()
    pt = paint(SHORT); pt.setPathEffect(skia.CornerPathEffect.Make(18))
    sm = paint("#000000", 70, blur=10); sm.setPathEffect(skia.CornerPathEffect.Make(18))
    cv.drawPath(p, sm)
    cv.drawPath(p, pt)
    cv.save(); cv.clipPath(p, skia.ClipOp.kIntersect, True)
    for sx in (-1, 1):                                            # barra virada (mais clara)
        cv.drawLine(sx * 22, 58, sx * 180, 50, paint(SHORT_CL, 255, "stroke", 18))
        cv.drawLine(sx * 22, 46, sx * 178, 38, paint(SHORT_LINHA, 90, "stroke", 2.2))
    cv.drawLine(0, -118, 0, 24, paint(SHORT_LINHA, 120, "stroke", 2.6))       # costura do meio
    cv.restore()
    ln = paint(SHORT_LINHA, 220, "stroke", 3.6); ln.setPathEffect(skia.CornerPathEffect.Make(18))
    cv.drawPath(p, ln)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-154, -158, 154, -122), 14, 14), paint(SHORT_CL))   # cós
    fr = skia.Path(); x = -148
    while x < 148:
        fr.moveTo(x, -154); fr.lineTo(x + 1.5, -126); x += 9
    cv.drawPath(fr, paint(SHORT_LINHA, 100, "stroke", 2.0))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-154, -158, 154, -122), 14, 14), paint(SHORT_LINHA, 170, "stroke", 2.6))
    bolso = skia.RRect.MakeRectXY(skia.Rect(52, -102, 116, -40), 10, 10)        # bolso branco
    cv.drawRRect(bolso, paint(BOLSO))
    pc = paint(BOLSO_LINHA, 255, "stroke", 2.2); pc.setPathEffect(skia.DashPathEffect.Make([6, 5], 0))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(58, -96, 110, -46), 7, 7), pc)
    cv.drawLine(52, -86, 116, -86, paint(BOLSO_LINHA, 255, "stroke", 2.2))
    cv.restore()


class Pose:
    __slots__ = ("hc", "esc", "rot", "pernas")

    def __init__(self, hc, esc, rot, pernas):
        self.hc, self.esc, self.rot, self.pernas = hc, esc, rot, pernas


def _quadris(hc, esc, rot):
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    return [(hc[0] + dx * c * esc, hc[1] + dx * s * esc) for dx in (-HIP_DX, HIP_DX)]


# ------------------------------------------------------------------ marcha
def _ciclo(u, sd, zs, lift):
    """-> (profundidade z, altura h, calcanhar no ar 0..1, fração do balanço ou -1 no apoio)."""
    u %= 1.0
    if u < sd:
        k = u / sd
        return zs * (1 - 2 * k), 0.0, sstep((k - 0.62) / 0.38), -1.0
    w = (u - sd) / (1 - sd)
    return -zs + 2 * zs * e_inout(w), lift * math.sin(math.pi * w) ** 0.9, 1 - sstep(w / 0.4), w


def _pe_marcha(u, x0, lado, sd, zs, lift, med, yaw):
    z, h, calc, w = _ciclo(u, sd, zs, lift)
    lat = med * math.sin(math.pi * w) * lado if w >= 0 else 0.0
    sc = 1 + z * 0.0011
    k = K_PE + 0.2 * calc if w < 0 else 0.5 + 0.32 * calc          # no balanço o pé aparece mais curto (de frente)
    return Pe(x0 + lat, Y_PISO + z * KZ - h - 22 * calc, yaw, lado, k, sc, z, h, calc)


def _tf_a(tf):
    """Tempo efetivo do pé A: enganchado por HOLD, depois o passo rápido de recuperação."""
    if tf <= TF_C:
        return tf
    if tf <= TF_C + HOLD:
        return TF_C
    if tf < T_POUSO:
        return lerp(TF_C, T_POUSO, e_out(prog(tf, TF_C + HOLD, T_POUSO)))
    return tf


def _u1(tf, perna):
    return (tf - TF_C) / P1 + UC + (0.0 if perna == 0 else 0.5)


_DELTA = {}


def _delta_contato():
    """Deslocamento do pé A no passo do contato para a frente do dedão encostar no lado de dentro do
    tornozelo do pé B (calculado uma vez)."""
    if "d" not in _DELTA:
        a = _pe_marcha(_u1(TF_C, 0), CX - HIP_DX, 1, SD1, ZS1, LIFT1, MED1, YAW1)
        b = _pe_marcha(_u1(TF_C, 1), CX + HIP_DX, -1, SD1, ZS1, LIFT1, MED1, YAW1)
        bx, by = b.tornozelo()
        alvo = (bx - R_TOR * b.sc * 0.55, by - 16)                  # na lateral de dentro do tornozelo
        dx, dy = a.dedao()
        _DELTA["d"] = (alvo[0] - dx, alvo[1] - dy)
    return _DELTA["d"]


def _bump_contato(tfa):
    t_to = TF_C - WC * SW1
    if tfa <= t_to or tfa >= T_POUSO:
        return 0.0
    if tfa <= TF_C:
        return sstep((tfa - t_to) / (TF_C - t_to))
    return 1 - sstep((tfa - TF_C) / (T_POUSO - TF_C))


def tropeco(tf):
    """0..1: o corpo embala para a frente depois do enganche e se recupera."""
    k = tf - TF_C
    if k <= 0.0 or k >= 0.56:
        return 0.0
    return e_out(prog(k, 0.0, 0.12)) * (1 - sstep(prog(k, 0.16, 0.54)))


def pose_corrida(tf):
    """Fita 1: corrida de frente (A = perna da esquerda da tela, a que engancha; B = a da direita). No tropeço o
    corpo embala PARA A CÂMERA (desce, cresce e inclina) e se recupera: legível já no 1×, sem queda."""
    lu = tropeco(tf)
    fi = (tf - TF_C) / P1
    hc = (CX + 12 * lu, HIP_Y - 5 * math.cos(4 * math.pi * fi) + 66 * lu)
    esc, rot = 1 + 0.10 * lu, -7.0 * lu
    qa, qb = _quadris(hc, esc, rot)
    tfa = _tf_a(tf)
    a = _pe_marcha(_u1(tfa, 0), CX - HIP_DX, 1, SD1, ZS1, LIFT1, MED1, YAW1)
    bmp = _bump_contato(tfa)
    b = _pe_marcha(_u1(tf, 1), CX + HIP_DX, -1, SD1, ZS1, LIFT1, MED1, YAW1)
    if bmp > 0:
        dx, dy = _delta_contato()
        a.px += dx * bmp; a.py += dy * bmp
        if bmp > 0.3:                                            # o pé que balança cruza NA FRENTE do tornozelo
            a.z = max(a.z, b.z + 1.0)
    return Pose(hc, esc, rot, [_perna(qa, a), _perna(qb, b)])


def pose_parado(yaw=16.0):
    hc = (CX, HIP_Y)
    qa, qb = _quadris(hc, 1.0, 0.0)
    a = Pe(CX - HIP_DX - 8, Y_PISO, yaw, 1, K_PE, 1.0, 0.0, 0.0, 0.0)
    b = Pe(CX + HIP_DX + 8, Y_PISO, yaw, -1, K_PE, 1.0, 0.0, 0.0, 0.0)
    return Pose(hc, 1.0, 0.0, [_perna(qa, a), _perna(qb, b)])


def yaw_diag(t, T):
    """Diagrama: a cada palavra ("giro", "pé", "canela", "coxa") as pontas dos DOIS pés viram mais um pouco para
    dentro e voltam, junto com a setinha do anel que acende: o giro é o que aponta a ponta para dentro. Igual
    nos três (nenhum é escolhido)."""
    b = 0.0
    for ch in ("giro", "pe3", "canela", "coxa"):
        b = max(b, math.sin(math.pi * prog(t, T[ch] + 0.04, T[ch] + 0.62)))
    return 16.0 + 9.0 * b


def k_queda(tf, F):
    """(0..1, índice) do tropeço da fita 2 em andamento."""
    for i, c in enumerate(F.quedas_f):
        x = (tf - F.tf_d - c) / QD + 0.5
        if 0 <= x <= 1:
            return math.sin(math.pi * x) ** 1.3, i
    return 0.0, -1


def pose_casa(tf, F):
    """Fita 2: andando; só o pé da direita (D) vira para dentro. Nos tropeços o corpo DESEQUILIBRA (embala para a
    frente e para baixo, inclina para um lado) com os DOIS pés no chão e um passo de recuperação para fora; os
    pés ficam sempre visíveis (nada de joelho no chão nem perna sem pé)."""
    fi = (tf - TF2) / P2
    hc = (CX, HIP_Y - 3 * math.cos(4 * math.pi * fi))
    ud = fi
    a = _pe_marcha(ud + 0.5, CX - HIP_DX, 1, SD2, ZS2, LIFT2, MED2, 0.0)
    d = _pe_marcha(ud, CX + HIP_DX, -1, SD2, ZS2, LIFT2, MED2, YAW2)
    q, i = k_queda(tf, F)
    if q <= 0:
        qa, qd = _quadris(hc, 1.0, 0.0)
        return Pose(hc, 1.0, 0.0, [_perna(qa, a), _perna(qd, d)])
    s = (-1.0, 0.6, -1.0)[i]                                     # para que lado o corpo embala (alterna; à direita
                                                                 # menos: não encosta no rótulo QUEDAS DEMAIS)
    esc = 1.0 + 0.08 * q
    hc2 = (CX + 26 * s * q, hc[1] + 72 * q)
    rot = 7.0 * s * q
    qa, qd = _quadris(hc2, esc, rot)
    for pe in (a, d):                                            # os dois pés no chão
        pe.py = lerp(pe.py, Y_PISO + pe.z * KZ, q); pe.h *= 1 - q
    passo = d if s > 0 else a                                    # o passo de recuperação, para fora
    passo.px += 46 * q * (1 if s > 0 else -1)
    pernas = []
    for quad, pe, fora in ((qa, a, -1), (qd, d, 1)):
        pr = _perna(quad, pe)
        joe = (pr.joe[0] + fora * 26 * q, pr.joe[1] + 6 * q)     # joelhos dobram para fora (base larga)
        pernas.append(Perna(quad, joe, pr.tor, pe, max(pr.kj, 0.6 * q)))
    return Pose(hc2, esc, rot, pernas)


# ------------------------------------------------------------------ anéis (cópia adaptada do cf_pe_virado: todos IGUAIS)
def ponta_seta(cv, x, y, ang, tam, cor, a):
    p = skia.Path()
    p.moveTo(x + tam * math.cos(ang), y + tam * math.sin(ang))
    p.lineTo(x + tam * 0.75 * math.cos(ang + 2.45), y + tam * 0.75 * math.sin(ang + 2.45))
    p.lineTo(x + tam * 0.75 * math.cos(ang - 2.45), y + tam * 0.75 * math.sin(ang - 2.45))
    p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))


def seta_pts(cv, pts, cor, a, larg=7, tam=22, halo=True):
    if a <= 0 or len(pts) < 2:
        return
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if halo:
        cv.drawPath(p, paint("#000000", int(90 * a), "stroke", larg + 6, blur=4))
    cv.drawPath(p, paint(cor, int(255 * a), "stroke", larg))
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    ponta_seta(cv, x1, y1, math.atan2(y1 - y0, x1 - x0), tam, cor, a)


def seta_arco(cv, cx, cy, rx, ry, a0, a1, cor, a, larg=6, tam=20):
    n = 18
    pts = [(cx + rx * math.cos(math.radians(lerp(a0, a1, k / n))), cy + ry * math.sin(math.radians(lerp(a0, a1, k / n))))
           for k in range(n + 1)]
    seta_pts(cv, pts, cor, a, larg, tam, halo=False)


def anel(cv, cx, cy, rx, ry, a, metade, t, t0, esc_traco=1.0):
    """Anel elíptico dourado, SEMPRE aceso por igual (nenhum pisca mais, nenhum é escolhido)."""
    if a <= 0:
        return
    r = skia.Rect(cx - rx, cy - ry, cx + rx, cy + ry)
    if metade == "tras":
        cv.drawArc(r, 180, 180, False, paint("#9C7A2A", int(255 * a), "stroke", 8 * esc_traco))
        return
    cv.drawArc(r, 0, 180, False, paint(OURO, int(150 * a), "stroke", 22 * esc_traco, blur=10 * esc_traco))
    cv.drawArc(r, 0, 180, False, paint(OURO, int(255 * a), "stroke", 9 * esc_traco))
    cv.drawArc(skia.Rect(cx - rx + 5, cy - ry + 3, cx + rx - 5, cy + ry - 2), 30, 120, False,
               paint("#FFF1C2", int(150 * a), "stroke", 2.5 * esc_traco))
    osc = 22 * math.sin(2 * math.pi * 0.85 * (t - t0))                       # setinha de giro, igual nos três
    seta_arco(cv, cx, cy, rx + 16 * esc_traco, ry + 11 * esc_traco, 40 + osc, 128 + osc, "#FFE08A", a,
              larg=6 * esc_traco, tam=20 * esc_traco)


def geo_aneis(pr):
    """(cx, cy, rx, ry) dos anéis do pé, da canela e da coxa de uma perna."""
    pe = pr.pe
    c = pe.centro()
    cx_c = lerp(pr.joe[0], pr.tor[0], 0.45); cy_c = lerp(pr.joe[1], pr.tor[1], 0.45)
    cx_q = lerp(pr.quad[0], pr.joe[0], 0.62); cy_q = lerp(pr.quad[1], pr.joe[1], 0.62)
    return {"pe": (c[0], c[1] + 4, 84 * pe.sc, 40 * pe.sc), "canela": (cx_c, cy_c, 50.0, 15.0),
            "coxa": (cx_q, cy_q, 64.0, 19.0)}


def crianca(cv, pose, aneis=None, t=0.0, y_chao=Y_PISO, esc_traco=1.0):
    """As duas pernas (a mais longe primeiro), cada uma com o pé por baixo, e o short por cima.
    `aneis`: {segmento: (alfa, t0)} acesos IGUAIS nas DUAS pernas (os dois lados = o comum; o "só de um lado"
    da fita 2 é o contraste)."""
    ordem = sorted(range(2), key=lambda i: pose.pernas[i].pe.z)
    for i in ordem:
        pr = pose.pernas[i]
        sombra_pe(cv, pr.pe, y_chao + pr.pe.z * KZ)
    for i in ordem:
        pr = pose.pernas[i]
        g = geo_aneis(pr) if aneis else None
        if g:
            for seg, (aa, t0) in aneis.items():
                anel(cv, *g[seg], aa, "tras", t, t0, esc_traco)
        pe_desenho(cv, pr.pe)
        perna_desenho(cv, pr)
        if g:
            for seg, (aa, t0) in aneis.items():
                anel(cv, *g[seg], aa, "frente", t, t0, esc_traco)
    short_frente(cv, pose.hc, pose.esc, pose.rot)


# ------------------------------------------------------------------ câmera (mundo -> tela)
BASE = (1.28, 540.0, 1000.0, 540.0, 1075.0)                     # a criança do short para baixo
BASE2 = (1.28, 540.0, 1000.0, 430.0, 1075.0)                     # fita 2: um pouco à esquerda (rótulos à direita)
LENTA1 = (2.0, 545.0, 1000.0, 540.0, 925.0)                      # 1ª câmera lenta: do joelho para baixo
LENTA2 = (1.55, 590.0, 940.0, 455.0, 895.0)                      # fita 2: canela e pés
DIAG = (1.15, 540.0, 1000.0, 540.0, 1010.0)                      # diagrama: anéis longe do painel


def _mist(a, b, k):
    return tuple(lerp(x, y, k) for x, y in zip(a, b))


_ZC = {}


def zoom_contato():
    """Zoom seco no ponto do enganche (congelamento do "esbarrou")."""
    if "z" not in _ZC:
        x, y = pose_corrida(TF_C).pernas[0].pe.dedao()
        _ZC["z"] = (2.7, x, y, 540.0, 900.0)
    return _ZC["z"]


def camera(t, T):
    v = vista(t, T)
    if v == "corre1":
        cam = _mist(BASE, LENTA1, e_inout(prog(t, T["camera"], T["camera"] + 0.8)))
        cam = _mist(cam, zoom_contato(), e_inout(prog(t, T["esbarrou"], T["esbarrou"] + 0.13)))
        return _mist(cam, LENTA1, e_inout(prog(t, T["outro"] - 0.05, T["outro"] + 0.4)))
    if v == "casa":
        k = e_inout(prog(t, T["so"], T["so"] + 0.6)) * (1 - e_inout(prog(t, T["quedas"], T["quedas"] + 0.3)))
        return _mist(BASE2, LENTA2, k)
    if v == "diagrama":
        return DIAG
    return BASE


def aplica(cv, cam):
    s, wx, wy, sx, sy = cam
    cv.translate(sx, sy); cv.scale(s, s); cv.translate(-wx, -wy)


def na_tela(cam, x, y):
    s, wx, wy, sx, sy = cam
    return sx + s * (x - wx), sy + s * (y - wy)


# ------------------------------------------------------------------ camadas fixas em cache (desempenho, cópia do piloto)
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


def vinheta(cv):
    def d(c):
        _rel(c)
        sh = skia.GradientShader.MakeRadial(skia.Point(540, 800), 760, [_c("#000000", 0), _c("#000000", 0), _c("#000000", 70)],
                                            [0.0, 0.6, 1.0])
        c.drawRect(CENA, paint("#000000", 255, shader=sh))
    _blit(cv, _img("vinheta", CENA.width(), CENA.height(), d), CENA.left(), CENA.top())


# ------------------------------------------------------------------ chão (vista de frente, em perspectiva)
def _y_prof(D):
    return HZ + C_G / D


def _faixas(cv, G, cores, x0=-320.0, x1=1420.0, junta=None, seed=0):
    """Faixas do chão (perpendiculares à corrida) que se afastam da câmera conforme G (distância corrida)."""
    banda = 0.8
    n = math.floor(G / banda); fr = G - n * banda
    pj = skia.Path() if junta else None
    y_far = None
    for j in range(0, 80):
        d0 = j * banda + fr
        d1 = d0 + banda
        if d1 <= 0.05:
            continue
        y1 = _y_prof(max(d0, 0.05)); y0 = _y_prof(d1)
        if y0 > 1700:
            continue
        idx = (j - n) % len(cores)
        cv.drawRect(skia.Rect(x0, y0, x1, min(y1, 1700)), paint(cores[idx]))
        y_far = y0
        if junta:
            pj.moveTo(x0, y0); pj.lineTo(x1, y0)
            esc = D_F / ((d0 + d1) / 2)
            off = (((j - n) * 0.37) % 1.0) * 520
            X = -1400 + off
            while X < 1400:
                xs = 540 + X * esc
                if x0 < xs < x1:
                    pj.moveTo(xs, y0); pj.lineTo(xs, min(y1, 1700))
                X += 520
        if y0 - HZ < 22:
            break
    if y_far is not None and y_far > HZ:
        cv.drawRect(skia.Rect(x0, HZ, x1, y_far + 1), paint(cores[0]))
    if junta:
        cv.drawPath(pj, paint(junta, 255, "stroke", 2.6))


def grama(cv, tf, vel=VEL1):
    """Quintal: sebe no horizonte e grama com faixas de corte que correm com o pé de apoio."""
    cv.drawRect(skia.Rect(-320, HZ - 120, 1420, HZ + 4), paint("#1D3346"))
    sebe = skia.Path()
    for i in range(-8, 40):
        x = -320 + i * 58
        r = 34 + 10 * ((i * 7) % 3)
        sebe.addCircle(x, HZ - 18, r)
    cv.drawPath(sebe, paint(SEBE))
    cv.drawRect(skia.Rect(-320, HZ - 22, 1420, HZ + 2), paint(SEBE))
    for i in range(-8, 40):
        x = -320 + i * 58
        cv.drawCircle(x - 8, HZ - 34 - 6 * ((i * 5) % 3), 12, paint(SEBE_CL))
    _faixas(cv, vel * tf, GRAMA)

    def d(c):
        sh = skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, 150)], [_c(GRAMA_LONGE, 235), _c(GRAMA_LONGE, 0)])
        c.drawRect(skia.Rect(0, 0, 1740, 150), paint("#000000", 255, shader=sh))
    _blit(cv, _img("nevoa_g", 1740, 150, d), -320, HZ)


def piso_madeira(cv, tf, vel=VEL2):
    """Casa: parede com rodapé e piso de tábuas correndo com o pé de apoio."""
    cv.drawRect(skia.Rect(-320, HZ - 420, 1420, HZ), paint(PAREDE))
    for i in range(-4, 16):
        cv.drawLine(-320 + i * 120, HZ - 420, -320 + i * 120, HZ - 16, paint(PAREDE_CL, 255, "stroke", 3))
    cv.drawRect(skia.Rect(-320, HZ - 18, 1420, HZ + 2), paint(RODAPE))
    _faixas(cv, vel * tf, MADEIRA, junta=MADEIRA_JUNTA)

    def d(c):
        sh = skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, 140)], [_c("#2A1A10", 200), _c("#2A1A10", 0)])
        c.drawRect(skia.Rect(0, 0, 1740, 140), paint("#000000", 255, shader=sh))
    _blit(cv, _img("nevoa_m", 1740, 140, d), -320, HZ)


# ------------------------------------------------------------------ bola e fiapos de grama
_ICO = []
for _sx in (-1, 1):
    for _sy in (-1, 1):
        for _v in ((0, _sx * 1, _sy * 1.618), (_sx * 1, _sy * 1.618, 0), (_sx * 1.618, 0, _sy * 1)):
            _n = math.sqrt(sum(q * q for q in _v))
            _ICO.append(tuple(q / _n for q in _v))


def bola(cv, x, y, r, giro, a=1.0):
    """Bola branca com gomos azul-claros, rolando (giro em torno do eixo horizontal)."""
    if a <= 0:
        return
    cv.save()
    clip = skia.Path(); clip.addCircle(x, y, r)
    cv.drawCircle(x, y, r, paint(BOLA_BR, int(255 * a)))
    cv.clipPath(clip, skia.ClipOp.kIntersect, True)
    cg, sg = math.cos(giro), math.sin(giro)
    for vx, vy, vz in _ICO:
        yy = vy * cg - vz * sg; zz = vy * sg + vz * cg
        if zz <= 0.05:
            continue
        rr = r * 0.26 * (0.35 + 0.65 * zz)
        cv.drawCircle(x + r * vx, y + r * yy, rr, paint(BOLA_AZ, int(255 * a)))
    cv.drawCircle(x - r * 0.35, y - r * 0.35, r * 0.35, paint("#FFFFFF", int(70 * a), blur=8))
    cv.restore()
    cv.drawCircle(x, y, r, paint(BOLA_LINHA, int(230 * a), "stroke", 3))


FIAPOS = ((-60, -260, 0.9), (-20, -330, -1.4), (25, -300, 1.7), (55, -250, -0.8), (-40, -380, 2.1), (10, -220, -2.4),
          (70, -340, 1.1))


def fiapos(cv, tf, origem):
    """Fiapos de grama que sobem e caem no tropeço (presos ao tempo do FILME: lentos na câmera lenta)."""
    k = tf - TF_C
    if not (0.0 < k < 0.55):
        return
    a = 1 - prog(k, 0.4, 0.55)
    ox, oy = origem
    for i, (vx, vy, w) in enumerate(FIAPOS):
        x = ox + vx * k * 1.6
        y = oy + vy * k * 1.6 + 0.5 * 1500 * k * k
        ang = w * k * 6 + i
        cv.drawLine(x - 7 * math.cos(ang), y - 7 * math.sin(ang), x + 7 * math.cos(ang), y + 7 * math.sin(ang),
                    paint(FIAPO, int(230 * a), "stroke", 4))


# ------------------------------------------------------------------ vista de cima: pegadas e pombo (cópias do cf_pe_virado)
def _sola():
    p = skia.Path()
    p.moveTo(2, 58)
    p.cubicTo(-16, 58, -24, 44, -24, 26)
    p.cubicTo(-24, 8, -28, -10, -27, -26)
    p.cubicTo(-26, -44, -12, -52, 3, -52)
    p.cubicTo(19, -52, 28, -42, 26, -26)
    p.cubicTo(24, -12, 11, -3, 12, 14)
    p.cubicTo(13, 30, 21, 40, 18, 50)
    p.cubicTo(15, 56, 8, 58, 2, 58)
    p.close()
    return p


SOLA = _sola()
DEDOS = ((15, -67, 10.5), (0, -71, 7.6), (-11, -67, 6.8), (-20, -60, 6.2), (-27, -50, 5.4))
PEGADA_LINHA = "#A08664"


def pegada(cv, x, y, ang, esc, a, direita=False):
    """Pegada de criança apontando para cima (pé esquerdo; `direita` espelha), girada `ang` graus."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.rotate(ang); cv.scale(-esc if direita else esc, esc)
    cv.save(); cv.translate(3, 5)
    cv.drawPath(SOLA, paint("#000000", int(55 * a), blur=7))
    cv.restore()
    cv.drawPath(SOLA, paint(OSSO_C, int(240 * a)))
    cv.drawPath(SOLA, paint(PEGADA_LINHA, int(235 * a), "stroke", 3.4))
    for dx, dy, r in DEDOS:
        cv.drawCircle(dx, dy, r, paint(OSSO_C, int(240 * a)))
        cv.drawCircle(dx, dy, r, paint(PEGADA_LINHA, int(235 * a), "stroke", 2.6))
    cv.restore()


def pombo(cv, x, y, esc, fase, andando, virado=1, a=1.0):
    """(cópia do cf_pe_virado, pés cor de pêssego)"""
    if a <= 0:
        return
    ph = fase * 2 * math.pi
    pulo = -3.5 * abs(math.sin(ph)) if andando else 0.0
    cab = 9 * math.sin(ph) if andando else 2 * math.sin(fase * 1.3)
    cv.save(); cv.translate(x, y); cv.scale(esc * virado, esc)
    cv.drawOval(skia.Rect(-62, -8, 58, 8), paint("#000000", int(70 * a), blur=6))
    for s in (1, -1):
        px = 11 * math.sin(ph) * s if andando else 7 * s
        lev = max(0.0, math.sin(ph) * s) * 7 if andando else 0.0
        cv.drawLine(2 + 6 * s, -30 + pulo, px, -lev, paint(POMBO_PE, int(255 * a), "stroke", 5))
        cv.drawLine(px - 7, -lev, px + 12, -lev, paint(POMBO_PE, int(255 * a), "stroke", 4))
    cv.save(); cv.translate(0, pulo)
    p = skia.Path(); p.moveTo(-44, -62); p.lineTo(-106, -46); p.lineTo(-102, -30); p.lineTo(-40, -44); p.close()
    cv.drawPath(p, paint(POMBO_ESC, int(255 * a)))
    cv.drawOval(skia.Rect(-64, -98, 50, -26), paint(POMBO_CORPO, int(255 * a)))
    cv.drawOval(skia.Rect(-10, -92, 48, -34), paint(POMBO_CAB, int(150 * a)))
    cv.save(); cv.rotate(-8)
    cv.drawOval(skia.Rect(-60, -86, 18, -48), paint(POMBO_ASA, int(255 * a)))
    for k in range(2):
        cv.drawLine(-38 + k * 18, -74, -28 + k * 18, -56, paint(POMBO_ESC, int(255 * a), "stroke", 5))
    cv.restore()
    cv.save(); cv.translate(26 + cab, -86)
    cv.drawOval(skia.Rect(-15, -34, 19, 12), paint(POMBO_PESC, int(255 * a)))
    cv.drawCircle(10, -40, 22, paint(POMBO_CAB, int(255 * a)))
    cv.drawCircle(17, -44, 6.5, paint("#F2B45A", int(255 * a)))
    cv.drawCircle(17, -44, 4.2, paint("#1B2430", int(255 * a)))
    cv.drawCircle(15.6, -45.6, 1.5, paint("#FFFFFF", int(255 * a)))
    b = skia.Path(); b.moveTo(29, -43); b.lineTo(50, -36); b.lineTo(29, -30); b.close()
    cv.drawPath(b, paint(OURO, int(255 * a)))
    cv.restore()
    cv.restore()
    cv.restore()


def linha_pontilhada(cv, x0, y0, x1, y1, a, larg=7, k=1.0):
    if a <= 0 or k <= 0:
        return
    x1, y1 = lerp(x0, x1, k), lerp(y0, y1, k)
    pt = paint(OURO, int(255 * a), "stroke", larg)
    pt.setPathEffect(skia.DashPathEffect.Make([1.0, larg * 2.6], 0))
    cv.drawLine(x0, y0, x1, y1, paint("#000000", int(70 * a), "stroke", larg + 4, blur=3))
    cv.drawLine(x0, y0, x1, y1, pt)


TRILHA = [(540 - 64 if i % 2 == 0 else 540 + 64, 1150 - i * 142, i % 2 == 1) for i in range(6)]
ANG_TRILHA = 18.0


def trilha_cima(cv, t, T):
    """Câmera 2: faixa de terra clara vista de cima; as pegadas da corrida chegam uma a uma, cada uma com a
    ponta para a linha do meio; a linha pontilhada da direção passa reta entre elas."""
    cv.drawRect(CENA, paint(GRAMA[0]))
    for i in range(12):
        cv.drawRect(skia.Rect(CENA.left(), CENA.top() + i * 80, CENA.right(), CENA.top() + i * 80 + 40), paint(GRAMA[1]))
    faixa = skia.Rect(318, CENA.top() - 10, 762, CENA.bottom() + 10)
    cv.drawRect(faixa, paint(TERRA))
    for i in range(46):                                        # pedrinhas e marcas da terra
        x = 330 + (i * 97) % 420; y = CENA.top() + (i * 173) % 900
        cv.drawCircle(x, y, 3 + (i % 3), paint(TERRA_ESC if i % 2 else TERRA_CL, 200))
    for x in (318, 762):
        cv.drawLine(x, CENA.top(), x, CENA.bottom(), paint(TERRA_ESC, 255, "stroke", 6))
    t0 = T["andar"]
    k_lin = prog(t, t0 + 0.05, t0 + 0.05 + 0.16 * len(TRILHA))
    linha_pontilhada(cv, 540, 1230, 540, 1230 - 900 * k_lin - 10, 1.0, larg=8)
    for i, (x, y, dir_) in enumerate(TRILHA):
        k = t - (t0 + 0.08 + 0.16 * i)
        if k < 0:
            continue
        esc = 1.0 * (0.6 + 0.4 * e_back(clamp(k / 0.22)))
        pegada(cv, x, y, ANG_TRILHA * (-1 if dir_ else 1), esc, clamp(k / 0.08), direita=dir_)
    # o pombinho: o NOME do jeito de andar, atravessando SEPARADO das pegadas, na borda de baixo
    tp = T["pombinho"] - 0.15
    if t >= tp:
        k = prog(t, tp, T["pode"])
        pombo(cv, lerp(70, 300, k), 1196, 0.58, t * 4.2, True, a=1 - prog(t, T["pode"] - 0.15, T["pode"]))


FILAS = ((300.0, 14.0), (690.0, 30.0))                           # (x da fileira, graus para dentro): antes / piora


def T_FILA2(T):
    """A fileira mais virada entra DURANTE a palavra "piora" (depois da folha do calendário)."""
    return T["piora"] + 0.18


PASSO_F1, PASSO_F2 = 0.025, 0.03
X_CAL = 420.0                                                     # calendário no vão entre as duas linhas (300 e 690)


def _fila(cv, t, x_c, ang, t0, passo, a=1.0):
    pts = []
    for i in range(5):
        x = x_c - 46 if i % 2 == 0 else x_c + 46
        y = 1100 - i * 122
        k = t - (t0 + passo * i)
        if k < 0:
            continue
        esc = 0.84 * (0.6 + 0.4 * e_back(clamp(k / 0.2)))
        pegada(cv, x, y, ang * (-1 if i % 2 else 1), esc, clamp(k / 0.08) * a, direita=i % 2 == 1)
        pts.append((x, y))
    return pts


def arco_angulo(cv, x, y, R, a0, a1, k, a, esc=1.0):
    """Arco dourado do ângulo entre a direção (a0) e o eixo do pé (a1), em graus de tela; enche com k."""
    if a <= 0 or k <= 0:
        return
    am = lerp(a0, a1, k)
    cunha = skia.Path(); cunha.moveTo(x, y)
    cunha.arcTo(skia.Rect(x - R, y - R, x + R, y + R), a0, am - a0, False); cunha.close()
    cv.drawPath(cunha, paint(OURO, int(85 * a)))
    arc = skia.Path(); arc.arcTo(skia.Rect(x - R, y - R, x + R, y + R), a0, am - a0, True)
    cv.drawPath(arc, paint("#000000", int(80 * a), "stroke", 10 * esc, blur=3))
    cv.drawPath(arc, paint(OURO, int(255 * a), "stroke", 6 * esc))


def tapete_cima(cv, t, T):
    """Câmera 2 sobre o tapete da sala: a fileira de antes e, depois de UMA folha do calendário, a seguinte MAIS
    virada para dentro, com o arco maior."""
    cv.drawRect(CENA, paint(TAPETE))
    for i in range(14):
        cv.drawLine(CENA.left(), CENA.top() + 30 + i * 66, CENA.right(), CENA.top() + 30 + i * 66,
                    paint(TAPETE_LISTRA, 255, "stroke", 6))
    r = skia.Rect(CENA.left() + 26, CENA.top() + 26, CENA.right() - 26, CENA.bottom() - 26)
    cv.drawRect(r, paint(TAPETE_BORDA, 255, "stroke", 14))
    t0 = T["piora"]
    for (xc, ang), ti, passo in ((FILAS[0], t0 - 0.25, PASSO_F1), (FILAS[1], T_FILA2(T), PASSO_F2)):
        linha_pontilhada(cv, xc, 1225, xc, 520, prog(t, ti, ti + 0.1), larg=6)
        pts = _fila(cv, t, xc, ang, ti, passo)
        if len(pts) == 5:                                       # arco no último passo da fileira
            x, y = pts[4]
            k = prog(t, ti + passo * 4 + 0.04, ti + passo * 4 + 0.2)
            arco_angulo(cv, x, y + 18, 118, -90, -90 + ang, k, 1.0)
            if k > 0:
                eixo = -90 + ang
                xe, ye = x + 124 * math.cos(math.radians(eixo)), y + 18 + 124 * math.sin(math.radians(eixo))
                cv.drawLine(x, y + 18, xe, ye, paint(OURO, int(255 * k), "stroke", 6))
                ponta_seta(cv, xe, ye, math.radians(eixo), 20, OURO, k)
    # o calendário vira UMA folha entre as duas fileiras (no vão entre elas: não cobre seta nem arco)
    t_cal = t0 + 0.0
    calendario(cv, X_CAL, 368, t, t_cal, prog(t, t0 - 0.3, t0 - 0.2), esc=1.6, t_para=t_cal + 0.2)


# ------------------------------------------------------------------ efeitos de "replay" (cópias do piloto)
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
        h = 18 + 10 * i
        cv.drawRect(skia.Rect(CENA.left(), y, CENA.right(), y + h), paint("#FFFFFF", int(46 * a)))
        cv.drawRect(skia.Rect(CENA.left(), y + h, CENA.right(), y + h + 4), paint("#000000", int(70 * a)))


def corte_fita(cv, t, t0, dur=0.25):
    """(cópia do cf_cameralenta_joelho_estala) Chiado: a cena muda por baixo dele."""
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


HUD_X, HUD_Y = 786, 1166
POP_C = (540, 600)


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
        s = R_LENTA if lento_k(t, T, F) > 0 else R_1X
        chip_c(cv, s, *_chip_hud_c(s), a, dim=0.4)
        return
    s = R_LENTA if tipo == "lenta" else R_1X
    hx, hy = _chip_hud_c(s)
    k = t - t0
    # "0,25×" grande, só quando a lenta LIGA; na fita 2 o voo é mais curto (libera o rótulo SÓ DE UM LADO)
    k_pop, k_voo = (0.32, 0.75) if t0 == T["camera"] else (0.18, 0.44)
    if tipo == "lenta" and k < k_voo and t0 in (T["camera"], T["so"]):
        cx, cy = POP_C
        if k < k_pop:
            chip_c(cv, s, cx, cy, a, esc=2.5 * e_back(clamp(k / 0.16)))
        else:
            v = e_inout(prog(k, k_pop, k_voo))
            chip_c(cv, s, lerp(cx, hx, v), lerp(cy, hy, v), a, esc=lerp(2.5, 1.0, v))
        return
    pop = 1 + 0.6 * (1 - e_out(prog(t, t0, t0 + 0.3))) if t0 > 0 else 1.0
    chip_c(cv, s, hx, hy, a, esc=pop)


# ------------------------------------------------------------------ marcações do comentarista (cópias do piloto)
def circulo_mao(cv, cx, cy, rx, ry, k, a, larg=7):
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
    """Selo branco e calmo: estetoscópio desenhado (forma, sem texto)."""
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


def calendario(cv, x, y, t, t0, a, esc=1.8, t_para=None):
    """Folhas virando, sem número (cópia do piloto, cabeçalho azul-claro: nada de vermelho)."""
    if a <= 0:
        return
    ent = lerp(0.6, 1.0, e_back(prog(t, t0 - 0.3, t0)))
    cv.save(); cv.translate(x + 48 * esc, y + 46 * esc); cv.scale(esc * ent, esc * ent); cv.translate(-48, -46)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(3, 5, 99, 97), 12, 12), paint("#000000", int(80 * a), blur=8))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(0, 0, 96, 92), 12, 12), paint("#EEF3F8", int(255 * a)))
    cv.save(); cv.clipRRect(skia.RRect.MakeRectXY(skia.Rect(0, 0, 96, 92), 12, 12), True)
    cv.drawRect(skia.Rect(0, 0, 96, 24), paint(AZUL_CL, int(255 * a)))
    cv.restore()
    for xx in (24, 72):
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(xx - 4, -8, xx + 4, 10), 3, 3), paint("#5E7186", int(255 * a)))
    fase = 0.0
    if t >= t0:
        tt = t if t_para is None else min(t, t_para)
        kk = (tt - t0) * 5
        fase = kk - math.floor(kk)
        if t_para is not None and t >= t_para:
            fase = 0.0
    for i in range(3):
        cv.drawLine(14, 42 + i * 16, 82, 42 + i * 16, paint("#9AA8B5", int(200 * a), "stroke", 4))
    if fase > 0:
        cv.save(); cv.translate(0, 24); cv.scale(1, 1 - fase)
        cv.drawRect(skia.Rect(0, 0, 96, 68), paint("#FFFFFF", int(170 * a * (1 - fase))))
        cv.restore()
    cv.restore()


def rotulo(cv, s, y, a, ancora=None, x=None, x_dir=None, tam=40):
    """Rótulo de caixa OPACA com fio até a borda esquerda (nunca risca o texto). (adaptado do cf_pe_virado)"""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    bx = (x - 10) if x is not None else (x_dir - lw - 30)
    if ancora is not None:
        xa, ya = ancora
        cv.drawLine(xa, ya, bx, y - tam * 0.42, paint(OURO, int(200 * a), "stroke", 2.5))
        cv.drawCircle(xa, ya, 6, paint(OURO, int(255 * a)))
    rr = skia.RRect.MakeRectXY(skia.Rect(bx, y - tam * 1.1, bx + lw + 30, y + tam * 0.25), 14, 14)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(235 * a)))
    cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 2.5))
    cv.drawString(s, bx + 15, y - tam * 0.08, f, paint(OURO, int(255 * a)))


# ------------------------------------------------------------------ mão de criança (cópia do cf_cameralenta_joelho_estala)
def _mao_path():
    """Mão de criança vista pelo dorso (origem = punho, dedos para +x, polegar para -y)."""
    m = skia.Path(); m.addRRect(skia.RRect.MakeRectXY(skia.Rect(0, -24, 46, 24), 15, 15))
    for yc, comp in ((-17.5, 29.0), (-5.8, 35.0), (5.8, 33.0), (17.0, 26.0)):
        m = _uniao(m, tubo(36, yc, 6.2, 36 + comp, yc + 1.5, 6.2))
    m = _uniao(m, tubo(12, -18, 7.0, 32, -38, 7.0))
    return m


MAO_P = _mao_path()
MAO_ESC = 1.45
# Braço de CRIANÇA (antes: 190 + 170 = quase a perna inteira, tubo fino de largura constante, esticado, sem
# cotovelo nem ombro, descendo do alto até o meio da canela). Agora: braço ~3/4 da perna, gordinho e afinando
# (ombro -> cotovelo -> punho), cotovelo DOBRADO para fora, ombro na borda de cima do quadro saindo da manga da
# camiseta, e a mão pega o alto da canela, logo abaixo do joelho.
UA, FA = 150.0, 135.0
R_OMBRO, R_COTOV, R_PUNHO = 36.0, 28.0, 20.5
PEGA_FR = 0.16                                                   # joelho -> tornozelo: onde a mão pega
OMBRO_DX, OMBRO_Y = 140.0, 588.0                                 # ombro: à direita do short, na borda de cima
MANGA, MANGA_CL, MANGA_LINHA = "#8EC3EA", "#B8DCF6", "#4C7FA8"   # camiseta azul-clara (nada de vermelho)


def _pega(pr):
    """Ponto da canela que a mão segura (o braço e a mão se montam a partir daqui)."""
    return lerp(pr.joe[0], pr.tor[0], PEGA_FR), lerp(pr.joe[1], pr.tor[1], PEGA_FR)


# Marca da DOR: o ponto do fio do rótulo e o círculo dourado ficam na canela VISÍVEL, abaixo da mão. Antes (rodada 3
# da revisão): o ponto saía de _pega + (100, -10) = (678, 720) na tela, no punho/antebraço que desce, e o círculo
# (108×92, centrado na mão) abraçava a mão e o braço junto com a canela. Agora: 57% do joelho ao tornozelo
# (≈ (523, 848) na tela; a mão termina em y ≈ 765 e o pé começa em y ≈ 940), círculo só da largura da canela.
DOR_FR = 0.57
DOR_RX, DOR_RY = 52.0, 42.0                                      # raios do círculo da DOR (mundo; × zoom na tela)


def _ponto_dor(pr):
    """Ponto da canela visível, abaixo da mão: centro do círculo da DOR e ponta do fio do rótulo DOR."""
    return lerp(pr.joe[0], pr.tor[0], DOR_FR), lerp(pr.joe[1], pr.tor[1], DOR_FR)


def _cotovelo(sx, sy, wx, wy):
    dx, dy = wx - sx, wy - sy
    d = max(1.0, min(math.hypot(dx, dy), UA + FA - 0.5))
    fi = math.atan2(dy, dx)
    al = math.acos(clamp((UA * UA + d * d - FA * FA) / (2 * UA * d), -1.0, 1.0))
    return sx + UA * math.cos(fi - al), sy + UA * math.sin(fi - al)


def _corpo_braco(om, co, pw):
    """Braço + antebraço num contorno só, afinando, com a união CONFERIDA (meio do braço, cotovelo, meio do
    antebraço, punho)."""
    pts = ((lerp(om[0], co[0], 0.5), lerp(om[1], co[1], 0.5)), co, (lerp(co[0], pw[0], 0.5), lerp(co[1], pw[1], 0.5)),
           (lerp(co[0], pw[0], 0.92), lerp(co[1], pw[1], 0.92)))
    return _uniao_conferida(lambda dr: (tubo(om[0], om[1], R_OMBRO, co[0], co[1], R_COTOV),
                                        tubo(co[0], co[1], R_COTOV * 0.94 - dr, pw[0], pw[1], R_PUNHO)), pts)


def _manga(cv, om, co):
    """Manga curta da camiseta no ombro (a ponta de cima sai do quadro): o braço é de um corpo, inclinado para
    pegar a perna — sem rosto."""
    L = math.hypot(co[0] - om[0], co[1] - om[1]) or 1.0
    ux, uy = (co[0] - om[0]) / L, (co[1] - om[1]) / L
    nx, ny = -uy, ux
    a0, a1 = -120.0, 0.40 * UA                                   # de bem acima do ombro até 40% do braço
    r0, r1 = R_OMBRO + 16, R_OMBRO + 9
    p = skia.Path()
    p.moveTo(om[0] + ux * a0 + nx * r0, om[1] + uy * a0 + ny * r0)
    p.lineTo(om[0] + ux * a1 + nx * r1, om[1] + uy * a1 + ny * r1)
    p.quadTo(om[0] + ux * (a1 + 9), om[1] + uy * (a1 + 9), om[0] + ux * a1 - nx * r1, om[1] + uy * a1 - ny * r1)
    p.lineTo(om[0] + ux * a0 - nx * r0, om[1] + uy * a0 - ny * r0)
    p.close()
    cv.drawPath(p, paint("#000000", 60, blur=7))
    cv.drawPath(p, paint(MANGA))
    cv.save(); cv.clipPath(p, skia.ClipOp.kIntersect, True)
    cv.drawLine(om[0] + ux * a0 + nx * r0 * 0.35, om[1] + uy * a0 + ny * r0 * 0.35,
                om[0] + ux * a1 + nx * r1 * 0.35, om[1] + uy * a1 + ny * r1 * 0.35, paint(MANGA_CL, 255, "stroke", 12))
    cv.drawLine(om[0] + ux * (a1 - 9) + nx * r1, om[1] + uy * (a1 - 9) + ny * r1,
                om[0] + ux * (a1 - 9) - nx * r1, om[1] + uy * (a1 - 9) - ny * r1, paint(MANGA_LINHA, 150, "stroke", 2.4))
    cv.restore()
    cv.drawPath(p, paint(MANGA_LINHA, 230, "stroke", 3.4))


def mao_canela(cv, pr, k):
    """A mão da própria criança desce pelo alto do quadro e segura o alto da canela (por fora, sem rosto):
    braço de criança com cotovelo dobrado e manga da camiseta no ombro. -> centro."""
    if k <= 0:
        return None
    sx, sy = _pega(pr)
    ang = math.radians(196)                                      # dedos atravessam a frente da canela, para dentro
    w = (sx + 62, sy - 12)
    desce = 1 - e_out(k)
    ox, oy = 30 * desce, -330 * desce
    pw = (w[0] + ox, w[1] + oy)
    om = (sx + OMBRO_DX + ox, OMBRO_Y + oy)
    co = _cotovelo(om[0], om[1], pw[0], pw[1])
    braco = _corpo_braco(om, co, pw)
    cv.drawPath(braco, paint("#000000", 50, blur=6))
    cv.drawPath(braco, paint(PELE))
    cv.save(); cv.clipPath(braco, skia.ClipOp.kIntersect, True)
    cv.drawPath(braco, paint("#E29F82", 255, "stroke", 16))
    for (x0, y0), (x1, y1) in ((om, co), (co, pw)):              # brilho ao longo do braço e do antebraço
        L = math.hypot(x1 - x0, y1 - y0) or 1.0
        nx, ny = -(y1 - y0) / L, (x1 - x0) / L
        cv.drawLine(lerp(x0, x1, 0.12) - nx * 8, lerp(y0, y1, 0.12) - ny * 8, lerp(x0, x1, 0.8) - nx * 7,
                    lerp(y0, y1, 0.8) - ny * 7, paint(PELE_CL, 200, "stroke", 9))
    cv.restore()
    cv.drawPath(braco, paint(PELE_LINHA, 230, "stroke", 3.6))
    # dobrinha do cotovelo (do lado de dentro da dobra)
    bx, by = (om[0] + pw[0]) / 2 - co[0], (om[1] + pw[1]) / 2 - co[1]
    bl = math.hypot(bx, by) or 1.0
    ix, iy = co[0] + bx / bl * 12, co[1] + by / bl * 12
    tx, ty = -by / bl, bx / bl
    dob = skia.Path(); dob.moveTo(ix - tx * 11, iy - ty * 11)
    dob.quadTo(ix + bx / bl * 5, iy + by / bl * 5, ix + tx * 11, iy + ty * 11)
    cv.drawPath(dob, paint(PELE_LINHA, 150, "stroke", 2.6))
    _manga(cv, om, co)
    m = skia.Path(MAO_P)
    mt = skia.Matrix(); mt.postScale(MAO_ESC, -MAO_ESC); mt.postRotate(math.degrees(ang)); mt.postTranslate(*pw)
    m.transform(mt)
    cv.drawPath(m, paint("#000000", 70, blur=6))
    cv.drawPath(m, paint(PELE))
    cv.save(); cv.clipPath(m, skia.ClipOp.kIntersect, True)
    cv.drawPath(m, paint("#E29F82", 255, "stroke", 12))
    cv.concat(mt)
    for yc in (-17.5, -5.8, 5.8, 17.0):
        cv.drawLine(40, yc - 4, 40, yc + 4, paint(PELE_LINHA, 150, "stroke", 2.2))
    cv.restore()
    cv.drawPath(m, paint(PELE_LINHA, 235, "stroke", 3.4))
    return (sx + 20 + ox, sy - 6 + oy)


# ------------------------------------------------------------------ borrão de movimento (1×, voltando, avançando)
OBTURADOR = {"play": 0.06, "volta": 0.03, "avanca": 0.03}
N_AMOSTRAS = 5
CAIXA = skia.Rect(-200, 300, 1300, 1400)


def amostras_borrao(t, T, F):
    tipo = F.tipo(t)
    obt = OBTURADOR.get(tipo)
    if not obt:
        return [t]
    v = vista(t, T)
    out = [t]
    for i in range(1, N_AMOSTRAS):
        tg = t - obt * i / (N_AMOSTRAS - 1)
        if tg < 0 or vista(tg, T) != v or F.tipo(tg) == "congela":
            break
        out.append(tg)
    return out


RASTRO_N = 8                      # amostras do rastro (o desfoque do layer funde uma na outra: rastro CONTÍNUO)
RASTRO_A = 0.55                   # opacidade do rastro (por baixo da pose atual, que fica nítida e opaca)
RASTRO_SIGMA = 4.5                # desfoque do rastro (mundo)


def _caixa_pes(pes, mg):
    xs, ys = [], []
    for pe in pes:
        for a, b in ((-20, -PE_W / 2), (-20, PE_W / 2), (PE_L + 14, -PE_W / 2), (PE_L + 14, PE_W / 2)):
            x, y = pe.P(a, b); xs.append(x); ys.append(y)
    return skia.Rect(min(xs) - mg, min(ys) - mg, max(xs) + mg, max(ys) + mg)


def _rastro_pes(cv, poses):
    """Rastro de movimento SÓ dos pés: silhuetas lisas (sem contorno nem dedos riscados) num layer DESFOCADO e
    translúcido, desenhado ANTES da criança (a pose atual cobre o que coincide; sobra o arrasto atrás do pé).
    `poses`: da mais nova para a mais velha; cada uma mais fraca que a anterior (o rastro some na ponta velha,
    preso ao pé, sem mancha solta no chão)."""
    grupos = [[pr.pe for pr in ps.pernas if pr.pe.alfa > 0] for ps in poses]
    todos = [pe for g in grupos for pe in g]
    if not todos:
        return
    pl = skia.Paint(); pl.setAlphaf(RASTRO_A)
    pl.setImageFilter(skia.ImageFilters.Blur(RASTRO_SIGMA, RASTRO_SIGMA))
    cv.saveLayer(_caixa_pes(todos, 3 * RASTRO_SIGMA + 30), pl)
    pp = paint(PELE)
    n = len(grupos)
    for i in range(n - 1, -1, -1):                               # da mais velha para a mais nova
        if not grupos[i]:
            continue
        cv.saveLayer(_caixa_pes(grupos[i], 30), _alfa(0.6 * (1 - i / n) ** 1.3))
        for pe in grupos[i]:
            pth, dedos = pe_forma(pe)
            cv.drawPath(pth, pp)
            for dx, dy, r in dedos:
                cv.drawCircle(dx, dy, r, pp)
        cv.restore()
    cv.restore()


def crianca_borrada(cv, t, T, F, pose_de):
    """Movimento rápido (1×, ◀◀, ▶▶): UMA criança nítida e opaca na pose do instante, com um rastro contínuo e
    desfocado só atrás dos pés. (Antes: 5 cópias INTEIRAS a 20% cada — o pé que balança virava 3-5 fileiras de
    dedos empilhadas, a perna do tropeço ganhava contornos paralelos e uma perna fantasma, o short duplicava.)"""
    ams = amostras_borrao(t, T, F)
    atual = pose_de(F.tf(t))
    if len(ams) > 1:
        t_ini = ams[-1]
        _rastro_pes(cv, [pose_de(F.tf(lerp(t, t_ini, i / RASTRO_N))) for i in range(1, RASTRO_N + 1)])
    crianca(cv, atual)


# ------------------------------------------------------------------ a 1ª câmera lenta: marcações presas ao pé A
def marcas_pe(cv, cam, pe, t, T, a):
    """Linha pontilhada da direção da corrida (reta para a câmera), seta no eixo do pé (calcanhar -> ponta) e o
    arco do ângulo entre elas — tudo POR FORA da pele, preso ao pé."""
    if a <= 0:
        return
    s = cam[0]
    a_ref = a * (1 - prog(t, T["esbarrou"] - 0.4, T["esbarrou"] - 0.12))   # no enganche, só a seta fica
    k_l = prog(t, T["ponta"], T["ponta"] + 0.3)
    if k_l > 0:
        x0, y0 = na_tela(cam, *pe.reto(-14))
        x1, y1 = na_tela(cam, *pe.reto(PE_L + 74))
        linha_pontilhada(cv, x0, y0, x1, y1, a_ref, larg=7, k=e_out(k_l))
        pts = [na_tela(cam, *pe.P(lerp(-14, PE_L + 22, i / 10), 0)) for i in range(11)]
        n = max(2, int(round(11 * e_out(k_l))))
        seta_pts(cv, pts[:n], OURO, a, larg=8, tam=24)
    k_a = prog(t, T["virou"], T["virou"] + 0.35)
    if k_a > 0 and a_ref > 0:
        a = a_ref
        cxp, cyp = na_tela(cam, *pe.reto(0))
        R = (PE_L + 20) * pe.sc * s
        pts = [na_tela(cam, *pe.reto(0))]
        n = 14
        th1 = pe.yaw * e_out(k_a)
        for i in range(n + 1):
            th = math.radians(th1 * i / n)
            dx, dz = math.sin(th) * pe.lado, math.cos(th)
            pts.append((cxp + R * dx, cyp + R * dz * pe.k))
        cunha = skia.Path(); cunha.moveTo(*pts[0])
        for q in pts[1:]:
            cunha.lineTo(*q)
        cunha.close()
        cv.drawPath(cunha, paint(OURO, int(95 * a)))
        arc = skia.Path(); arc.moveTo(*pts[1])
        for q in pts[2:]:
            arc.lineTo(*q)
        cv.drawPath(arc, paint("#000000", int(80 * a), "stroke", 11, blur=3))
        cv.drawPath(arc, paint(OURO, int(255 * a), "stroke", 7))


def pop_contato(cv, x, y, t, t0):
    """Traços curtos dourados ('pop' de quadrinho, sem letras) em volta do ponto de contato. Desenhados no MUNDO
    e ANTES das pernas: só aparecem nos vãos (entre as canelas e por fora do tornozelo), nunca sobre a pele."""
    k = t - t0
    if not (0 <= k < 0.55):
        return
    a = 1 - prog(k, 0.3, 0.55)
    g = e_out(clamp(k / 0.2))
    for ang in (-104.0, -126.0, -148.0, -38.0, -14.0):            # vão entre as canelas + fora do tornozelo
        r0 = 44 + 10 * g
        r1 = 60 + 26 * g
        q = math.radians(ang)
        cv.drawLine(x + r0 * math.cos(q), y + r0 * math.sin(q), x + r1 * math.cos(q), y + r1 * math.sin(q),
                    paint("#000000", int(90 * a), "stroke", 4.4, blur=1.2))
        cv.drawLine(x + r0 * math.cos(q), y + r0 * math.sin(q), x + r1 * math.cos(q), y + r1 * math.sin(q),
                    paint(OURO, int(255 * a), "stroke", 2.8))


def _pos_bola(tf):
    return 300.0, 1036.0 - 20 * abs(math.sin(math.pi * tf * 1.7))


# ------------------------------------------------------------------ o mundo dentro do monitor
X_PONTOS, Y_PONTOS, Y_SINAL = 812.0, 806.0, 724.0             # pontinhos dos tropeços; rótulos dos sinais


def _pontos_queda(T, F):
    return [T["quedas"] + c / VR for c in F.quedas_f]


def monitor(cv, t, T, F, limpo=False):
    """Tudo o que fica DENTRO do monitor de replay (recortado em CENA). `limpo`: miniatura (sem linhas de
    varredura, grão, chiado, faixas nem flash)."""
    tipo = F.tipo(t)
    v = vista(t, T)
    tf = F.tf(t)
    cam = camera(t, T)
    if tipo == "volta":
        j = math.sin(t * 97) * 4 + math.sin(t * 41) * 3
        cam = (cam[0], cam[1], cam[2], cam[3] + j, cam[4])
    if 0 <= t - T["o2"] < 0.18 and not limpo:                   # salto de quadro no corte de fita
        j = 40 * math.sin((t - T["o2"]) * 140) * (1 - (t - T["o2"]) / 0.18)
        cam = (cam[0], cam[1], cam[2], cam[3] + j, cam[4] - j * 0.3)
    if 0 <= t - T1C < 0.3 and t < T["volta"] and not limpo:      # o tranco do tropeço no 1× (câmera na mão)
        k = (t - T1C) / 0.3
        j = 16 * math.sin(k * 3 * math.pi) * (1 - k)
        cam = (cam[0], cam[1], cam[2], cam[3] + 0.4 * j, cam[4] + j)
    s = cam[0]
    cv.save(); cv.clipRect(CENA, True)
    monitor_fundo(cv)

    if v in ("corre1", "brinca", "diagrama"):
        cv.save(); aplica(cv, cam)
        tfg = tf if v != "diagrama" else F.tf(T["pode"])
        grama(cv, tfg)
        bx, by = _pos_bola(tfg)
        if v != "diagrama":
            cv.drawOval(skia.Rect(bx - 44, 1072, bx + 44, 1094), paint("#000000", 70, blur=8))
            bola(cv, bx, by, 46, -tfg * 7.0)
        if v == "corre1":                                       # fiapos e 'pop' ATRÁS das pernas (nunca sobre a pele)
            pc = pose_corrida(tf)
            b = pc.pernas[1].pe
            fiapos(cv, tf, (b.px - 150, b.py + 34))
            if T["esbarrou"] <= t < T["outro"] + 0.4:
                pop_contato(cv, *pc.pernas[0].pe.dedao(), t, T["esbarrou"])
        if v == "diagrama":
            crianca(cv, pose_parado(yaw_diag(t, T)), aneis=estado_aneis(t, T), t=t)
        elif tipo in OBTURADOR:
            crianca_borrada(cv, t, T, F, pose_corrida)
        else:
            crianca(cv, pose_corrida(tf))
        cv.restore()
        vinheta(cv)
        if v == "corre1":
            marcas_corrida(cv, t, T, F, cam)
        if v == "brinca":                                       # a regra é o tempo: folhas virando, sem número
            a_c = prog(t, T["tempo"] - 0.05, T["tempo"] + 0.12) * (1 - prog(t, T["o2"] - 0.25, T["o2"]))
            calendario(cv, 846, 368, t, T["tempo"], a_c, esc=1.6, t_para=T["sozinha"])
    elif v == "trilha":
        trilha_cima(cv, t, T)
    elif v == "casa":
        cv.save(); aplica(cv, cam)
        piso_madeira(cv, tf)
        if tipo in OBTURADOR:
            crianca_borrada(cv, t, T, F, lambda x: pose_casa(x, F))
            pose = None
        else:
            pose = pose_casa(tf, F)
            crianca(cv, pose)
        k_m = prog(t, T["dor"] - 0.22, F.t_dor) * (1 - prog(t, T["quedas"] - 0.05, T["quedas"] + 0.12))
        centro_mao = None
        if k_m > 0 and pose is not None:
            centro_mao = mao_canela(cv, pose.pernas[1], k_m)
        cv.restore()
        vinheta(cv)
        if pose is not None:
            marcas_casa(cv, t, T, F, cam, pose, centro_mao)
        # QUEDAS DEMAIS: um pontinho dourado por tropeço, numa fileira acima do chão (sem dígito)
        for i, tq in enumerate(_pontos_queda(T, F)):
            k = t - tq
            if k >= 0:
                r = 15 * e_back(clamp(k / 0.18))
                cv.drawCircle(X_PONTOS + i * 66, Y_PONTOS, r + 10, paint(OURO, 90, blur=8))
                cv.drawCircle(X_PONTOS + i * 66, Y_PONTOS, r, paint(OURO))
                cv.drawCircle(X_PONTOS + i * 66, Y_PONTOS, r, paint(FUNDO_CARTAO, 255, "stroke", 3))
    else:
        tapete_cima(cv, t, T)

    varredura(cv, t, lento_k(t, T, F), limpo)
    if not limpo:
        faixas_tracking(cv, t, {"volta": 1.0, "avanca": 0.7}.get(tipo, 0.0))
        if tipo in ("volta", "avanca"):
            t0 = F.inicio_trecho(t)
            _setas(cv, 76, 410, (0.55 + 0.45 * (math.sin((t - t0) * 16) > -0.3)) * prog(t, t0, t0 + 0.06), 1.9,
                   tipo == "avanca")
        flash(cv, t, T["esbarrou"], 1.0)
        flash(cv, t, F.t_dor, 0.8)
        corte_fita(cv, t, T["o2"])
    cv.restore()
    return cam


def marcas_corrida(cv, t, T, F, cam):
    """1ª câmera lenta: círculo nos dois pés, marcações presas ao pé A, 'pop' no contato."""
    tf = F.tf(t)
    pose = pose_corrida(tf)
    a_pe, b_pe = pose.pernas[0].pe, pose.pernas[1].pe
    s = cam[0]
    a_c = prog(t, T["repara"], T["repara"] + 0.05) * (1 - prog(t, T["ponta"] + 0.25, T["ponta"] + 0.5))
    if a_c > 0:
        ca, cb = na_tela(cam, *a_pe.centro()), na_tela(cam, *b_pe.centro())
        circulo_mao(cv, (ca[0] + cb[0]) / 2, (ca[1] + cb[1]) / 2 + 6 * s, 175 * s, 96 * s,
                    prog(t, T["repara"] + 0.02, T["repara"] + 0.37), a_c)
    a_m = prog(t, T["ponta"], T["ponta"] + 0.05) * (1 - prog(t, T["outro"] + 0.05, T["outro"] + 0.35))
    marcas_pe(cv, cam, a_pe, t, T, a_m)


def marcas_casa(cv, t, T, F, cam, pose, centro_mao):
    """Fita 2: seta e arco SÓ no pé que vira (o outro não ganha marca nem cor); círculo da dor na canela."""
    d = pose.pernas[1].pe
    a_m = prog(t, T["so"] + 0.08, T["so"] + 0.2) * (1 - prog(t, T["quedas"] - 0.25, T["quedas"] - 0.02))
    if a_m > 0:
        s = cam[0]
        x0, y0 = na_tela(cam, *d.reto(-14))
        x1, y1 = na_tela(cam, *d.reto(PE_L + 70))
        linha_pontilhada(cv, x0, y0, x1, y1, a_m, larg=7, k=e_out(prog(t, T["so"] + 0.08, T["so"] + 0.4)))
        pts = [na_tela(cam, *d.P(lerp(-14, PE_L + 56, i / 10), 0)) for i in range(11)]
        n = max(2, int(round(11 * e_out(prog(t, T["so"] + 0.12, T["so"] + 0.45)))))
        seta_pts(cv, pts[:n], OURO, a_m, larg=8, tam=24)
        k_a = prog(t, T["lado"], T["lado"] + 0.35)
        if k_a > 0:
            cxp, cyp = na_tela(cam, *d.reto(0))
            R = (PE_L + 16) * d.sc * s
            pts = [(cxp, cyp)]
            for i in range(15):
                th = math.radians(d.yaw * e_out(k_a) * i / 14)
                pts.append((cxp + R * math.sin(th) * d.lado, cyp + R * math.cos(th) * d.k))
            cunha = skia.Path(); cunha.moveTo(*pts[0])
            for q in pts[1:]:
                cunha.lineTo(*q)
            cunha.close()
            cv.drawPath(cunha, paint(OURO, int(95 * a_m)))
            arc = skia.Path(); arc.moveTo(*pts[1])
            for q in pts[2:]:
                arc.lineTo(*q)
            cv.drawPath(arc, paint(OURO, int(255 * a_m), "stroke", 7))
    if centro_mao is not None and t >= F.t_dor:                  # a mão está na canela: círculo na canela, NÃO na mão
        a = 1 - prog(t, T["quedas"] - 0.2, T["quedas"])
        mx, my = na_tela(cam, *_ponto_dor(pose.pernas[1]))
        circulo_mao(cv, mx, my, DOR_RX * cam[0], DOR_RY * cam[0], prog(t, F.t_dor + 0.04, F.t_dor + 0.4), a)


def estado_aneis(t, T):
    """{segmento: (alfa, t0)}: os três anéis acendem um por palavra e ficam IGUAIS; saem no "regra"."""
    sai = 1 - prog(t, T["regra"] - 0.3, T["regra"])
    out = {}
    for seg, t0 in (("pe", T["pe3"]), ("canela", T["canela"]), ("coxa", T["coxa"])):
        if t >= t0 and sai > 0:
            out[seg] = (prog(t, t0, t0 + 0.15) * sai, t0)
    return out


# ------------------------------------------------------------------ rótulos fora do monitor (nunca nas miniaturas)
def rotulos(cv, t, T, F):
    v = vista(t, T)
    if v == "diagrama":
        g = geo_aneis(pose_parado(yaw_diag(t, T)).pernas[1])      # rótulos só à direita, fio até a perna da direita
        sai = 1 - prog(t, T["regra"] - 0.3, T["regra"])
        cam = camera(t, T)
        for seg, s, t_on in (("pe", R_PE, T["pe3"]), ("canela", R_CANELA, T["canela"]), ("coxa", R_COXA, T["coxa"])):
            cx, cy, rx, ry = g[seg]
            xa, ya = na_tela(cam, cx + rx + 18, cy)
            rotulo(cv, s, ya + 18, prog(t, t_on, t_on + 0.25) * sai, ancora=(xa, ya), x=max(812, xa + 40))
    if v == "casa":
        cam = camera(t, T)
        pose = pose_casa(F.tf(t), F)
        d = pose.pernas[1]
        # SÓ DE UM LADO: preso à palavra "lado" e de pé até a "dor" (antes: alfa máximo 0,02 — nunca aparecia)
        a1 = prog(t, T["lado"] + 0.12, T["lado"] + 0.30) * (1 - prog(t, T["dor"] - 0.10, T["dor"] + 0.05))
        rotulo(cv, R_LADO, Y_SINAL, a1, ancora=na_tela(cam, *d.pe.P(PE_L * 0.5, -PE_W * 0.55 * d.pe.lado)), x_dir=1020, tam=38)
        a2 = prog(t, T["dor"] + 0.05, T["dor"] + 0.25) * (1 - prog(t, T["quedas"] - 0.12, T["quedas"]))
        rotulo(cv, R_DOR, Y_SINAL, a2, ancora=na_tela(cam, *_ponto_dor(d)), x_dir=1020, tam=38)   # ponto na canela
        a3 = prog(t, T["quedas"] + 0.08, T["quedas"] + 0.28) * (1 - prog(t, T["piora"] - 0.1, T["piora"]))
        rotulo(cv, R_QUEDAS, Y_SINAL, a3, x_dir=1020, tam=38)
    if v == "tapete":
        a4 = prog(t, T["piora"] + 0.1, T["piora"] + 0.3) * (1 - prog(t, T["ai"] + 0.05, T["ai"] + 0.2))
        rotulo(cv, R_PIORA, 492, a4, x_dir=1020, tam=38)


# ------------------------------------------------------------------ melhores momentos, celular e estetoscópio
def momentos(T, F):
    """Os 4 sinais, na ordem da fala: só de um lado, a mão na canela, os pontinhos dos tropeços, a piora."""
    return ((T["ai"], T["lado"] + 0.45), (T["vale"], F.t_dor + 0.4), (T["ortopedista"], _pontos_queda(T, F)[2]),
            (T["olhar"], T["ai"] - 0.03))


RECORTES = ((610.0, 940.0, 660.0), (650.0, 820.0, 640.0), (560.0, 880.0, 860.0), (540.0, 800.0, 960.0))
MW, MH = 212.0, 191.0
G_ESC = 1.72                                                      # miniaturas GRANDES em grade 2×2 (antes: fileira miúda)
GRADE = ((335.0, 556.0), (745.0, 556.0), (335.0, 924.0), (745.0, 924.0))
EST_C = (540.0, 740.0)                                            # estetoscópio no meio da grade


def miniatura(T, F, tt):
    chave = ("mini", round(tt, 3))
    if chave not in _CACHE:
        sf = skia.Surface(int(CENA.width()), int(CENA.height())); c = sf.getCanvas(); c.clear(_c(BG_OUT))
        c.translate(-CENA.left(), -CENA.top())
        fundo_cl(c, tt)
        monitor(c, tt, T, F, limpo=True)
        _CACHE[chave] = sf.makeImageSnapshot()
    return _CACHE[chave]


def recorte(i):
    cx, cy, w = RECORTES[i]
    h = w * MH / MW
    x0 = clamp(cx - CENA.left() - w / 2, 0, CENA.width() - w)
    y0 = clamp(cy - CENA.top() - h / 2, 0, CENA.height() - h)
    return skia.Rect(x0, y0, x0 + w, y0 + h)


def k_celular(t, T):
    """0..1: as miniaturas descem para a fileira estreita."""
    return e_inout(prog(t, T["filmar"] - 0.05, T["filmar"] + 0.3))


def k_cel_entra(t, T):
    """0..1: o celular entra no lugar (cresce e acende), depois que as miniaturas saíram de baixo dele."""
    return prog(t, T["filmar"] + 0.12, T["filmar"] + 0.42)


def melhores_momentos(cv, t, T, F):
    """Sem texto: a cena escurece, as 4 miniaturas entram GRANDES (grade 2×2), uma por batida, e o estetoscópio
    vem no meio delas depois do "olhar". No "filmar" elas descem para uma fileira estreita e sobe o celular.
    Seguram até a CTA (sem voltar à fita 1)."""
    if t < T["ai"] - 0.05:
        return
    cv.save(); cv.clipRect(CENA, True)
    img = _img("escurece", CENA.width(), CENA.height(), lambda c: c.clear(_c(BG_OUT, 255)))
    _blit(cv, img, CENA.left(), CENA.top(), 0.93 * prog(t, T["ai"] + 0.10, T["ai"] + 0.40))
    cta = max(0.14, 1 - prog(t, T["manda"] - 0.3, T["manda"] + 0.2))
    kc = k_celular(t, T)
    t_resp = T["diagnostico"] + 0.7
    resp = 1.0 + 0.02 * (0.5 - 0.5 * math.cos((t - t_resp) * 2.4)) if t > t_resp else 1.0
    for i, (ti, tt) in enumerate(momentos(T, F)):
        if t < ti:
            continue
        k = prog(t, ti, ti + 0.32)
        esc = max(0.01, e_back(k)) * lerp(G_ESC, 0.72, kc) * resp
        a = prog(t, ti, ti + 0.06) * cta
        cx = lerp(GRADE[i][0], 236 + i * 166, kc)
        cy = lerp(GRADE[i][1] + (1 - e_out(k)) * 40, 1040, kc)
        giro = (-3.0, 2.5, -2.0, 3.0)[i] * e_out(k) * (1 - kc)
        cv.save(); cv.translate(cx, cy); cv.rotate(giro); cv.scale(esc, esc)
        borda = skia.RRect.MakeRectXY(skia.Rect(-MW / 2 - 8, -MH / 2 - 8, MW / 2 + 8, MH / 2 + 8), 13, 13)
        sombra = skia.RRect.MakeRectXY(skia.Rect(-MW / 2 - 2, -MH / 2 + 2, MW / 2 + 14, MH / 2 + 18), 13, 13)
        cv.drawRRect(sombra, paint("#000000", int(110 * a), blur=12))
        cv.drawRRect(borda, paint("#F4F7FA", int(255 * a)))
        dentro = skia.RRect.MakeRectXY(skia.Rect(-MW / 2, -MH / 2, MW / 2, MH / 2), 8, 8)
        cv.save(); cv.clipRRect(dentro, True)
        cv.drawImageRect(miniatura(T, F, tt), recorte(i), skia.Rect(-MW / 2, -MH / 2, MW / 2, MH / 2),
                         skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kNone), _alfa(a))
        cv.restore()
        cv.drawRRect(borda, paint(OURO, int(255 * a * (0.55 + 0.45 * (1 - prog(t, ti + 0.1, ti + 0.6)))), "stroke", 4))
        cv.restore()
    # estetoscópio: entra 0,25 s depois do "olhar"; no "filmar" vai para a direita; no "diagnóstico" pulsa uma vez
    t_e = T["olhar"] + 0.12
    a_e = prog(t, t_e, t_e + 0.2) * cta
    if a_e > 0:
        pul = 1 + 0.10 * math.sin(math.pi * prog(t, T["diagnostico"], T["diagnostico"] + 0.5))
        ex, ey = lerp(EST_C[0], 790, kc), lerp(EST_C[1], 640, kc)
        ee = lerp(1.45, 1.3, kc) * e_back(prog(t, t_e, t_e + 0.3)) * pul * resp
        # no "diagnóstico": um anel dourado se abre UMA vez em volta do estetoscópio (quem diagnostica é o exame)
        kd = prog(t, T["diagnostico"], T["diagnostico"] + 0.7)
        if 0 < kd < 1:
            cv.drawCircle(ex, ey, (60 + 46 * e_out(kd)) * ee, paint(OURO, int(230 * (1 - kd) * a_e), "stroke", 7))
        if t >= T["diagnostico"]:
            cv.drawCircle(ex, ey, 64 * ee, paint(OURO, int(120 * prog(t, T["diagnostico"], T["diagnostico"] + 0.3) * a_e),
                                                 blur=14))
        estetoscopio(cv, ex, ey, ee, a_e)
    celular(cv, t, T, F, cta, resp)
    cv.restore()


CEL_R = skia.Rect(214, 424, 456, 902)
TELA_R = skia.Rect(230, 476, 440, 850)


def celular(cv, t, T, F, cta, resp):
    """Celular desenhado (sem mão, sem marca): filma a mesma criança correndo de frente; ponto de gravação
    DOURADO. Linha até o estetoscópio no "ajuda" (o vídeo vai para a consulta); no "não" a imagem para e a tela
    do celular apaga (nenhuma marca, nenhum anel: o vídeo não aponta de onde vem o giro); no "diagnóstico" o
    celular esmaece e o estetoscópio pulsa."""
    kc = k_cel_entra(t, T)
    if kc <= 0:
        return
    a = clamp(kc * 2.0) * cta * (1 - 0.45 * prog(t, T["diagnostico"], T["diagnostico"] + 0.3))
    resp = resp * lerp(0.6, 1.0, e_back(kc))
    # a linha do vídeo para a consulta (por baixo do celular e do estetoscópio)
    k_l = prog(t, T["ajuda"], T["ajuda"] + 0.35)
    if k_l > 0:
        linha_pontilhada(cv, CEL_R.right() + 8, 662, 712, 650, cta * (1 - 0.3 * prog(t, T["diagnostico"], T["diagnostico"] + 0.3)),
                         larg=8, k=e_out(k_l))
    cv.saveLayer(None, _alfa(a)) if a < 1 else cv.save()
    cx, cy = CEL_R.centerX(), CEL_R.centerY()
    cv.translate(cx, cy); cv.scale(resp, resp); cv.translate(-cx, -cy)
    corpo = skia.RRect.MakeRectXY(CEL_R, 34, 34)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(CEL_R.left() + 4, CEL_R.top() + 8, CEL_R.right() + 8, CEL_R.bottom() + 14), 34, 34),
                 paint("#000000", 110, blur=14))
    cv.drawRRect(corpo, paint(CEL))
    cv.drawRRect(corpo, paint(CEL_BORDA, 255, "stroke", 5))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(cx - 30, CEL_R.top() + 18, cx + 30, CEL_R.top() + 28), 5, 5), paint("#3A4A5A"))
    tela = skia.RRect.MakeRectXY(TELA_R, 12, 12)
    cv.save(); cv.clipRRect(tela, True)
    cv.drawRect(TELA_R, paint(CEL_TELA))
    parado = t >= T["nao"]
    tf_ph = 60.0 + (min(t, T["nao"]) - T["filmar"]) * 1.0
    cv.save()
    esc = 0.43
    cv.translate(TELA_R.centerX(), TELA_R.centerY() + 6); cv.scale(esc, esc); cv.translate(-540, -800)
    grama(cv, tf_ph)
    crianca(cv, pose_corrida(tf_ph))
    cv.restore()
    if parado:                                                   # "não": a imagem para e a tela apaga (véu escuro)
        cv.drawRect(TELA_R, paint("#0B1622", int(175 * prog(t, T["nao"], T["nao"] + 0.25))))
    cv.restore()
    cv.drawRRect(tela, paint("#FFFFFF", 60, "stroke", 2))
    if not parado and (t * 2.0) % 1.0 < 0.6:                     # gravando: ponto DOURADO piscando (para no "não")
        cv.drawCircle(TELA_R.left() + 22, TELA_R.top() + 22, 12, paint(OURO, 110, blur=6))
        cv.drawCircle(TELA_R.left() + 22, TELA_R.top() + 22, 9, paint(OURO))
    cv.restore()


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


def quadro(cv, t, T, blocos, ep, F):
    fundo_cl(cv, t)
    monitor(cv, t, T, F)
    melhores_momentos(cv, t, T, F)
    fim = 1 - prog(t, T["manda"] - 0.4, T["manda"] - 0.1)
    cantoneiras(cv, fim)
    painel(cv, t, T, F, fim)
    rotulos(cv, t, T, F)
    capa(cv, t, T["volta"], ep["gancho"][0], ep["gancho"][1])
    selo_lenta(cv, lento_k(t, T, F) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    if t >= 0.5 / FPS:                                          # quadro 0 (capa): o gancho é o ÚNICO texto grande
        interface(cv, t, T, blocos, DESTAQUE)


# ------------------------------------------------------------------ som (mix próprio: som.py fica intacto; cópias do piloto)
def trilha_partes(dur, bpm=100):
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


def avancar(dur):
    return _fita(dur, 380, 1500, 0.07, 0.9, 78) * 0.85


def chiado(dur=0.26):
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


def _esticar(x, fator):
    idx = np.arange(0, len(x) - 1, 1.0 / fator)
    return np.interp(idx, np.arange(len(x)), x)


def tuc():
    """O toque do pé no tornozelo: 'tuc' abafado e curto (nada de estalo, nada cômico)."""
    return som._onepole_lp(som.thump(), 900) * 0.9


def tuc_lento():
    """O MESMO 'tuc', esticado ~2× (mesma faixa de tom)."""
    return _esticar(tuc(), 2.0)


def farfalhar(dur=0.35, seed=21):
    """Farfalhar curto de grama (ruído filtrado com envelope macio)."""
    SR = som.SR
    n = int(dur * SR)
    r = som._noise(n, seed)
    r = r - np.convolve(r, np.ones(5) / 5, "same")
    return r * som._env(n, 0.03, dur * 0.6) * 0.45


def tap_lento():
    return _esticar(som._onepole_lp(som.click(), 1400), 1.7) * 0.9


def bip():
    """Início de gravação: bip curto e suave (sem tom de alarme)."""
    SR = som.SR
    n = int(0.11 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * 1180 * t) * som._env(n, 0.004, 0.06) * 0.5


def folha():
    return som._onepole_lp(som.click(), 2600) * 0.8


def ding_tom(semitons):
    d = som.ding()
    return _esticar(d, 1.0 / (2 ** (semitons / 12)))


def janelas(T, F, dur):
    xs = np.arange(0, dur + 0.01, 0.01)
    gb = np.ones_like(xs); gh = np.ones_like(xs)
    for i, x in enumerate(xs):
        tp = F.tipo(x)
        gb[i] = {"play": 1.0, "lenta": 0.0, "congela": 0.45, "volta": 0.2, "avanca": 0.8}[tp]
        gh[i] = {"play": 1.0, "lenta": 0.8, "congela": 0.9, "volta": 0.55, "avanca": 0.8}[tp]
        if tp == "congela" and lento_k(x, T, F) > 0:
            gb[i] = 0.0
        if T["pode"] <= x < T["regra"]:                          # diagrama: a batida volta baixinha
            gb[i] = 0.5
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


def pisadas(T, F):
    """Instantes (vídeo) em que cada pé pousa, só quando o filme anda para a frente e a criança está de frente."""
    out = []
    ant = None
    x = 0.0
    anda = ("play", "lenta", "avanca")
    while x < T["ai"]:
        v = vista(x, T)
        tipo = F.tipo(x); tf = F.tf(x)
        if v in ("corre1", "brinca", "casa"):
            P_, base = (P2, (tf - TF2) / P2) if v == "casa" else (P1, (tf - TF_C) / P1 + UC)
            if ant is not None and ant[2] == v and tipo in anda and ant[0] in anda and 0 < tf - ant[1] < 0.3:
                bant = (ant[1] - TF2) / P2 if v == "casa" else (ant[1] - TF_C) / P1 + UC
                for off in (0.0, 0.5):
                    if math.floor(base + off) > math.floor(bant + off):
                        if tipo == "lenta":
                            out.append((x, tap_lento, 0.28))
                        elif tipo == "avanca":
                            out.append((x, "click", 0.12))
                        else:
                            out.append((x, "click", 0.2 if v != "casa" else 0.24))
            ant = (tipo, tf, v)
        else:
            ant = None
        x += 1 / 240
    return out


def sons(T, F):
    ev = [e for e in pisadas(T, F) if not (T["volta"] - 0.05 < e[0] < T["camera"])]
    t1c = T1C
    ev += [(t1c, tuc, 0.32), (t1c + 0.01, farfalhar, 0.2),
           (T["volta"], lambda: rebobinar(T["camera"] - T["volta"]), 0.9),
           (T["camera"], "pop", 0.55),
           (T["repara"] + 0.02, lambda: som.whoosh(0.22, seed=31), 0.3),
           (T["ponta"], "shimmer", 0.3),
           (T["virou"] + 0.3, "tick", 0.35),
           (T["esbarrou"], congelar, 1.0), (T["esbarrou"] + 0.01, tuc_lento, 0.42),
           (T["outro"] + 0.05, lambda: farfalhar(0.8, 23), 0.2),
           (T["andar"], lambda: som.whoosh(0.3, seed=33), 0.3)]
    ev += [(T["andar"] + 0.08 + 0.16 * i, "click", 0.25) for i in range(len(TRILHA))]
    ev += [(T["pode"], lambda: som.whoosh(0.3, seed=35), 0.3),
           (T["pe3"], "ding", 0.35), (T["canela"], lambda: ding_tom(2), 0.35), (T["coxa"], lambda: ding_tom(4), 0.35),
           (T["regra"], lambda: avancar(T["sozinha"] - T["regra"]), 0.7)]
    ev += [(T["tempo"] + 0.2 * i, folha, 0.25) for i in range(int((T["sozinha"] - T["tempo"]) / 0.2))]
    ev += [(T["sozinha"], "pop", 0.4),
           (T["o2"] - 0.02, chiado, 0.7),
           (T["so"], "pop", 0.5), (T["so"] + 0.05, "shimmer", 0.25),
           (F.t_dor, congelar, 0.85),
           (T["quedas"], lambda: avancar(T["piora"] - T["quedas"]), 0.6)]
    ev += [(tq, "thump", 0.3) for tq in _pontos_queda(T, F)]
    ev += [(T["piora"], lambda: som.whoosh(0.3, seed=37), 0.3), (T["piora"] + 0.02, folha, 0.3),
           (T_FILA2(T) + PASSO_F2 * 4 + 0.2, "tick", 0.35)]
    ev += [(ti, "pop", 0.35) for ti, _ in momentos(T, F)] + [(ti + 0.01, lambda: som.whoosh(0.25, seed=41), 0.3)
                                                             for ti, _ in momentos(T, F)]
    ev += [(T["olhar"] + 0.12, "ding", 0.45),
           (T["filmar"], bip, 0.25), (T["ajuda"], lambda: som.whoosh(0.25, seed=43), 0.3),
           (T["nao"], "tick", 0.4), (T["diagnostico"], "ding", 0.4),
           (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def tempos_previa(T, F):
    return (0.0, 0.5, 1.0, T1C, T1C + 0.12, T["volta"] + 0.3, T["camera"] + 0.15, T["camera"] + 0.6,
            T["lenta"] + 0.3, T["repara"] + 0.4, T["ponta"] + 0.35, T["virou"] + 0.4, T["virou"] + 0.7,
            T["esbarrou"] + 0.08, T["esbarrou"] + 0.35, T["outro"] + 0.3, T["outro"] + 0.55,
            T["andar"] + 0.3, T["pombinho"] + 0.3, T["pode"] + 0.4, T["pe3"] + 0.3, T["canela"] + 0.3,
            T["coxa"] + 0.5, T["regra"] + 0.3, T["tempo"] + 0.5, T["sozinha"] + 0.4, T["o2"] + 0.05,
            T["o2"] + 0.4, T["so"] + 0.2, T["lado"] + 0.4, T["dor"] - 0.1, T["dor"] + 0.4,
            *_pontos_queda(T, F), T["piora"] + 0.2, T["piora"] + 0.55, T["ai"] - 0.05,
            T["ai"] + 0.2, T["ortopedista"] + 0.3, T["olhar"] + 0.4, T["filmar"] + 0.5,
            T["ajuda"] + 0.4, T["nao"] + 0.25, T["diagnostico"] + 0.4, T["manda"] - 0.6, T["manda"] + 1.2,
            T["total"] - 1 / 30)


# ------------------------------------------------------------------ entrada única (réplica do cf_comum.fazer_render, com mix próprio)
def pausar(voz, pal, pausas=PAUSAS):
    """Insere silêncio DEPOIS de cada palavra de `pausas` (no meio do vão até a próxima: nenhuma sílaba é
    cortada) e empurra as palavras seguintes. A voz não muda de ritmo; só ganha respiro entre as perguntas
    do alerta. Palavra ausente = StopIteration (falha ALTO, como as âncoras)."""
    SR = som.SR
    cortes = []
    for w, dur in pausas:
        i = next(k for k, p in enumerate(pal) if p["w"].lower() == w)
        fim = pal[i]["t"] + pal[i]["d"]
        prox = pal[i + 1]["t"] if i + 1 < len(pal) else fim
        cortes.append(((fim + max(fim, prox)) / 2, dur))
    cortes.sort()
    partes, ult = [], 0
    for t0, dur in cortes:
        p = int(round(t0 * SR))
        partes += [voz[ult:p], np.zeros(int(round(dur * SR)), dtype=voz.dtype)]
        ult = p
    partes.append(voz[ult:])
    nova = np.concatenate(partes)
    return nova, [dict(p, t=p["t"] + sum(d for t0, d in cortes if p["t"] >= t0)) for p in pal]


def preparar(ep, tmp):
    roteiro = "\n".join(ep["roteiro"])
    voz_bruta, palavras = _voz.narrar(roteiro, _voz.RITMO_COMO_FUNCIONA, os.path.join(tmp, "voz"))
    voz_c, pal, tirado = comprimir(voz_bruta, palavras, respiro_cta=RESPIRO_CTA)
    voz_c, pal = pausar(voz_c, pal)
    pal = alinhar(pal, roteiro)
    T = ancoras(pal, ANCORAS)
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
