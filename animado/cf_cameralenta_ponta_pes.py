# -*- coding: utf-8 -*-
"""CÂMERA LENTA (série nova, ao lado do COMO FUNCIONA) — piloto "FILHO NA PONTINHA: / NORMAL ATÉ QUANDO?".

A mecânica é a de um REPLAY de TV, não a de uma aula: o passo de uma criança pequena na ponta dos pés
passa em 1× (rápido e borrado: cadência real de criança pequena), a fita VOLTA, é revista em CÂMERA LENTA
e CONGELA no detalhe. Cada bloco da fala abre com uma manipulação do tempo do filme, e cada uma tem um
SENTIDO:
  * câmera lenta / congelar  -> o que o olho não pega em 1× (o calcanhar não desce);
  * AVANÇO RÁPIDO            -> o tempo passando: nos primeiros anos o passo assenta sozinho; depois dos
                                3 anos, o avanço mostra que ele fica na ponta "o tempo todo";
  * CORTE DE FITA (chiado)   -> OUTRA fita, com outro CHÃO: fita 1 = estúdio (o que costuma passar),
                                fita 2 = piso de madeira (3 anos, ainda na ponta), fita 3 = tapete de
                                EVA (os sinais: um lado só, panturrilha, andar tarde);
  * MELHORES MOMENTOS        -> no "esses sinais", as 3 miniaturas dos congelamentos dos sinais entram
                                uma por batida, sem texto, e o estetoscópio vem no "atenção".
A resposta do gancho (a IDADE) chega em "três", com as 3 velas acendendo juntas no bolo.

O tempo do filme (`Filme.tf`) é separado do tempo do vídeo: o mundo (pernas e chão que corre) é desenhado
em função do tempo do filme; a narração nunca para nem desacelera.

Polimento de 26/10 (nota dos leitores às cegas: "o selo aparecia o vídeo inteiro, inclusive em 1×, e a câmera
lenta prometia mais do que mostrava"):
  * O selo CÂMERA LENTA só EXISTE enquanto a lentidão está ligada (a 0,25× e no congelamento que fecha cada
    câmera lenta): entra com um pop quando a fita desacelera e sai antes de ela voltar a 1×, avançar ou ir
    para o elástico. Nenhum quadro em 1×, voltando ou avançando tem selo (nem apagado). A moldura âmbar segue
    a mesma janela, e no congelamento sem selo o painel mostra "1×" apagado (não mais "0,25×").
  * O 1× é BORRADO de verdade: borrão de movimento das DUAS pernas (média de 6 poses dentro do "obturador",
    em vez dos fantasmas da perna da frente). Na volta e no avanço também. A câmera lenta e os congelamentos
    ficam NÍTIDOS. O quadro 0 continua nítido (as amostras não passam de t = 0).
  * A câmera lenta REVELA o que o 1× esconde, com imagem própria: a LUZ NO VÃO. Quando o pé pousa pela ponta,
    acende uma luz dourada no espaço entre o calcanhar e o chão (a luz passa por baixo: o calcanhar não
    encosta) e ela fica acesa no congelamento do "calcanhar". Na fita 3, o 1× borrado não deixa ver diferença
    entre os pés; na câmera lenta, a luz acende sob UM calcanhar só e o outro pé, de sola inteira, não deixa
    passar luz nenhuma ("é só de um lado?"). A luz não é rótulo nem cor de "certo" no pé de sola inteira.
  * As marcações da câmera lenta (bolinha e trilha do calcanhar, círculo, seta do "desce") saem JUNTO com o
    selo: nada delas sobra no avanço rápido nem no elástico.
  * Miniatura do calendário nos melhores momentos tirada com o filme ainda parado (nítida).

Correções da 2ª revisão de 25/10 (leitor às cegas + revisor):
  * "Mas" = corte para a fita 2, JÁ na ponta: nenhum quadro de 10,5 a 14 s mostra a sola inteira (antes
    o passo assentava e voltava a subir no "ainda", como se a criança regredisse aos 3 anos).
  * "Mas a idade importa." no lugar de "Mas uma idade muda tudo." (sem drama); bolo sem velas até o
    "três": nenhum quadro mostra 2 velas com "TRÊS" na legenda.
  * Elástico de verdade (nada de disco/rebite): faixa chata verde-limão com costura ao comprido, um anel
    fino que abraça a panturrilha e uma alça fina em volta do calcanhar (recortados no contorno da perna:
    as pontas somem na borda, como faixa que dá a volta); em repouso já reta e esticada; no "durinha" o
    calcanhar desce ~27°, a faixa ALONGA ~22%, afina, clareia, a costura se abre e ela segura 0,3 s
    tremendo antes do estalo ("tuóim") e do balanço.
  * Pouso sincronizado: o pé toca no "ponta" e o filme FREIA até congelar no "calcanhar".
  * Câmera lenta nítida: sem rastro de fantasmas (o cruzamento das pernas fica limpo).
  * Trilha do calcanhar desenhada POR BAIXO das pernas; no "tempo todo" ela é uma onda suave (gráfico da
    altura do calcanhar, que nunca encosta no chão), começando num pico — sem "V" nem gancho.
  * Calendário só entra com a câmera já parada (nada sobre o joelho).
  * Selo CÂMERA LENTA acende em dourado só enquanto a câmera lenta está ligada.

Correções da 1ª revisão de 25/10 (leitor às cegas + revisor):
  * Pernas de CRIANÇA PEQUENA (coxa e canela curtas e grossas, joelho redondo, pé grande, dobrinha no
    tornozelo) e short infantil (cós de elástico franzido, barra larga, bolinhas). Gancho com "FILHO".
  * Quadro 0 com as pernas separadas: o pé de trás na ponta, calcanhar alto; o da frente no ar, à frente.
  * O bolo é preso à TELA: entra com as pernas paradas e sai pela direita ANTES de o passo recomeçar.
  * Sem estrelinhas sobre o pé; "costuma passar sozinho" = avanço rápido com o passo assentando.
  * "Durinha" = um ELÁSTICO por fora da perna (joelho -> calcanhar): o calcanhar tenta descer, o elástico
    estica, treme e puxa de volta. A panturrilha não afina.
  * Congelamento do "calcanhar" sem a perna de trás encostando no tornozelo da frente.
  * Selo da série só depois que o gancho saiu; chips de velocidade maiores e um "0,25×" grande que
    voa para o painel; calendário grande junto das pernas, que para de virar quando o passo recomeça.

Regras da série e do verificador (storyboard.json), todas aqui:
  * Nenhuma pegada no vídeo inteiro; quadro 0 com o pé da frente no ar.
  * Nada de ❚❚, barra de progresso ou "PAUSA": congelar = flash + tique + zoom.
  * Dourado nos achados; VERMELHO PROIBIDO neste episódio (inclusive no calendário).
  * Pele lisa e OPACA, nada por dentro da perna; sem fundo preto; sem rosto.
  * O pé que apoia a sola inteira não ganha rótulo nem cor de "certo".
  * Nenhum texto além do `tela` (CÂMERA LENTA, 1×, 0,25×, 3 ANOS), do gancho e da interface.
Assinatura sonora: a batida some na câmera lenta, rebobinar e avançar com cliques e chiado de fita,
tique seco no congelamento, chiado no corte. Mix próprio (`mixar_cl`), sem mexer em som.py.

Medição do teste entre formatos: o `formato` técnico é "como_funciona"; o BI separa esta série por
`serie` = "Câmera lenta" e pelo trecho "cameralenta" do id.

Helpers copiados (não importados) de outras cenas, como manda o contrato: relogio (cf_andador);
joelho, tubo, manga_short e path_cintura (cf_crianca_mancando, redesenhados para criança pequena);
calendario (cf_fratura_cola, cabeçalho sem vermelho). A cena é PRESA ao roteiro pelas palavras-âncora
(ANCORAS): roteiro sem elas = KeyError no render.
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
from .cf_fratura_cola import alinhar, carimbo_ouro, comprimir, montar_blocos

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "filho": ("filho", 1, False), "normal": ("normal", 1, False), "quando": ("quando", 1, False),
    "volta": ("volta", 1, False), "camera": ("câmera", 1, False), "lenta": ("lenta", 1, False),
    "pousa": ("pousa", 1, False), "ponta1": ("ponta", 1, False), "calcanhar": ("calcanhar", 1, False),
    "desce": ("desce", 1, False), "nos": ("nos", 1, False), "primeiros": ("primeiros", 1, False),
    "comum": ("comum", 1, False), "costuma": ("costuma", 1, False), "passar": ("passar", 1, False),
    "sozinho": ("sozinho", 1, False), "mas": ("mas", 1, False), "idade": ("idade", 1, False),
    "importa": ("importa", 1, False), "depois": ("depois", 1, False),
    "tres": ("três", 1, False), "anos2": ("anos", 2, False), "ainda": ("ainda", 1, False),
    "ponta2": ("ponta", 2, False), "tempo": ("tempo", 1, False), "todo": ("todo", 1, False),
    "vale": ("vale", 1, False), "avaliacao": ("avaliação", 1, False), "fica": ("fica", 1, False),
    "tambem": ("também", 1, False), "lado": ("lado", 1, False), "panturrilha": ("panturrilha", 1, False),
    "durinha": ("durinha", 1, False), "demorou": ("demorou", 1, False), "andar": ("andar", 1, False),
    "esses": ("esses", 1, False), "sinais": ("sinais", 1, False), "pedem": ("pedem", 1, False),
    "atencao": ("atenção", 1, False), "manda": ("manda", 1, False),
}
DESTAQUE = {"normal", "calcanhar", "comum", "sozinho", "idade", "três", "todo", "avaliação", "lado",
            "panturrilha", "durinha", "demorou", "atenção"}
RESPIRO_CTA = 1.6

# ------------------------------------------------------------------ paleta (sem vermelho)
PELE, PELE_LINHA = "#F0B49A", "#B9765E"
SHORT, SHORT_CL, SHORT_ESC, SHORT_LINHA = "#2E9C92", "#5CC6BB", "#1F6F68", "#134A45"
BOLINHA = "#E8FFFA"
FUNDO_CARTAO = "#0B1824"
AMBAR = "#FFB547"
AZUL_CL = "#9CC9FF"
LIMA, LIMA_CL, LIMA_ESC = "#B4E043", "#E2F7A0", "#4F7A16"      # o elástico: verde-limão de brinquedo
# pisos das 3 fitas (cores opacas: preencher área grande com cor translúcida é caro neste skia)
MADEIRA = ("#6C4731", "#5F3D29", "#77513A")
MADEIRA_JUNTA, MADEIRA_VEIO = "#3A2518", "#82603F"
EVA = ("#3A6396", "#8F7A3C", "#356F5D", "#5B4F86")
EVA_JUNTA = "#16222F"

# ------------------------------------------------------------------ o "monitor" de replay (tela)
CENA = skia.Rect(40, 330, 1040, 1230)                           # o mundo é recortado aqui (selo e karaokê livres)
Y_TELA_CHAO = 1090

# ------------------------------------------------------------------ mundo (unidades de desenho) — criança pequena
Y_CHAO = 1000                                                    # linha do chão no mundo
HX0 = 540                                                        # quadril (a esteira corre embaixo dele)
L1, L2 = 132, 124                                                # coxa, perna: curtas (criança de 2-3 anos)
R_QUAD, R_JOE, R_TOR = 46, 36, 26                                # grossas, joelho redondo, tornozelo gordinho
BOJO = 5.0                                                       # panturrilha fofa (sem contorno atlético)
P_CICLO, SD, FR, LIFT = 1.0, 0.6, 66.0, 36.0                     # ciclo (2 passos), fração de apoio, passada, altura
VEL = 2 * FR / (SD * P_CICLO)                                    # velocidade da esteira (px do mundo / s de filme)
PE_K = 1.08                                                      # pé proporcionalmente maior (criança)
BOLA = (50.0 * PE_K, 35.0 * PE_K)                                # ponto de apoio do antepé (referencial do tornozelo)
CALC = (-20.0 * PE_K, 34.0 * PE_K)                               # base do calcanhar
JUNTA = (52.0 * PE_K, 27.0 * PE_K)                               # onde os dedos dobram
TF0 = -0.05                                                      # quadro 0: pé da frente no ar, à frente; o de trás na ponta
V1 = 1.35                                                        # "1×": cadência real de criança pequena (2,7 passos/s)
VL = 0.25 * V1                                                   # "0,25×"
VR = 3.6                                                         # avanço rápido


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
    """1 = estúdio (até o "Mas"), 2 = piso de madeira (3 anos), 3 = tapete de EVA (os sinais)."""
    return 1 if t < T["mas"] else (2 if t < T["fica"] else 3)


class Filme:
    """Liga o tempo do VÍDEO ao tempo do FILME, por trechos presos às palavras-âncora:
    play (1×), volta (rebobinar, com aceleração), lenta (0,25×; a última freia até parar), avanca
    (avanço rápido), congela (0×). Os cortes de fita (em "Mas" e em "Fica") são saltos do tempo do filme
    escondidos pelo chiado: cada fita é outra cena, com outro chão."""

    def __init__(self, T):
        s = []
        t_toque = T["ponta1"] + 0.05                             # o pé toca o chão NO "ponta"
        a = TF0 + V1 * T["volta"]
        s.append((0.0, T["volta"], "play", TF0, a, None))
        voo = VL * (t_toque - T["camera"])
        n = round(a - 2.5 + voo)                                 # n inteiro = pouso do pé de perto
        tf_s = n - voo
        s.append((T["volta"], T["camera"], "volta", a, tf_s, "inout"))
        s.append((T["camera"], t_toque, "lenta", tf_s, n, None))
        tf_fz = n + VL * (T["calcanhar"] - t_toque) / 2          # freia de 0,25× até parar no "calcanhar"
        s.append((t_toque, T["calcanhar"], "lenta", n, tf_fz, "freia"))
        s.append((T["calcanhar"], T["nos"], "congela", tf_fz, tf_fz, None))
        tf_soz = tf_fz + VR * (T["sozinho"] - T["nos"])
        s.append((T["nos"], T["sozinho"], "avanca", tf_fz, tf_soz, None))
        tf_mas = tf_soz + V1 * (T["mas"] - T["sozinho"])
        s.append((T["sozinho"], T["mas"], "play", tf_soz, tf_mas, None))
        # fita 2: congelada com os DOIS pés na ponta (o de perto começando o apoio, o de trás saindo)
        tf_b = round(tf_mas) + 20 + 0.05
        s.append((T["mas"], T["ainda"], "congela", tf_b, tf_b, None))
        tf_tempo = tf_b + V1 * (T["tempo"] - T["ainda"])
        s.append((T["ainda"], T["tempo"], "play", tf_b, tf_tempo, None))
        tf_vale = round(tf_tempo + VR * (T["vale"] - T["tempo"]) - 0.25) + 0.25
        s.append((T["tempo"], T["vale"], "avanca", tf_tempo, tf_vale, None))
        s.append((T["vale"], T["fica"], "congela", tf_vale, tf_vale, None))
        # fita 3: no "lado" o pé de perto acabou de pousar na ponta; o de trás apoia a sola inteira
        tf_lado = round(tf_vale) + 20 + 0.04
        tf_tam = tf_lado - VL * (T["lado"] - T["tambem"])
        tf_fica = tf_tam - V1 * (T["tambem"] - T["fica"])
        s.append((T["fica"], T["tambem"], "play", tf_fica, tf_tam, None))
        s.append((T["tambem"], T["lado"], "lenta", tf_tam, tf_lado, None))
        s.append((T["lado"], T["andar"], "congela", tf_lado, tf_lado, None))
        fim = T["total"] + 2.0
        s.append((T["andar"], fim, "play", tf_lado, tf_lado + V1 * (fim - T["andar"]), None))
        self.segs = s
        self.T = T
        self.t_toque, self.n_pouso = t_toque, n
        self.tf_fz, self.tf_b, self.tf_vale, self.tf_lado = tf_fz, tf_b, tf_vale, tf_lado

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
        """Início do trecho corrido do mesmo tipo (a lenta que freia continua a mesma câmera lenta)."""
        i = self.segs.index(self.seg(t))
        while i > 0 and self.segs[i - 1][2] == self.segs[i][2] and self.segs[i - 1][1] == self.segs[i][0]:
            i -= 1
        return self.segs[i][0]


# ------------------------------------------------------------------ marcha na ponta dos pés
def _passo(fi, s0, pt):
    """-> (x da bola do pé rel. ao quadril, altura (neg = acima do chão), inclinação do pé, ângulo dos
    dedos, no chão?, fração da fase). `pt`: 1 = na ponta; 0 = apoia a sola inteira."""
    u = (fi - s0) % 1.0
    if u < SD:                                                  # apoio: a bola fica parada no chão (esteira)
        k = u / SD
        inc_p = lerp(38, 30, e_inout(k / 0.5)) if k < 0.5 else lerp(30, 56, ((k - 0.5) / 0.5) ** 2)
        return FR - 2 * FR * k, 0.0, lerp(0.0, inc_p, pt), 0.0, True, k
    w = (u - SD) / (1 - SD)                                     # balanço
    inc_p = lerp(56, 24, e_inout(w / 0.5)) if w < 0.5 else lerp(24, 38, e_inout((w - 0.5) / 0.5))
    inc = lerp(10 * math.sin(math.pi * w), inc_p, pt)
    dedos = inc * sstep(w / 0.3) * (1 - sstep((w - 0.7) / 0.3))
    return lerp(-FR, FR, e_inout(w)), -LIFT * math.sin(math.pi * w), inc, dedos, False, w


def _tornozelo(bx, by, inc):
    r = rot(BOLA, inc)
    return HX0 + bx - r[0], Y_CHAO + by - r[1]


class Pe:
    __slots__ = ("ax", "ay", "inc", "dedos", "chao", "k")

    def __init__(self, ax, ay, inc, dedos, chao, k):
        self.ax, self.ay, self.inc, self.dedos, self.chao, self.k = ax, ay, inc, dedos, chao, k

    def ponto(self, p):
        r = rot(p, self.inc)
        return self.ax + r[0], self.ay + r[1]

    def calcanhar(self):
        return self.ponto(CALC)

    def bola(self):
        return self.ponto(BOLA)


def pt_perto(t, T):
    """Na ponta (1) ou com a sola inteira (0). Fita 1: nos primeiros anos o passo assenta durante o
    avanço rápido ("costuma passar sozinho"). Fitas 2 e 3: na ponta o tempo todo."""
    if t < T["mas"]:
        return 1 - sstep(prog(t, T["costuma"], T["sozinho"] + 0.05))
    return 1.0


def pt_longe(t, T):
    """A perna de trás acompanha a da frente, menos na fita 3 ("só de um lado?"): sola inteira."""
    if t >= T["fica"]:
        return 0.0
    return pt_perto(t, T)


def pose(tf, t, T, dinc=0.0):
    """-> (quadril, pé de perto, pé de longe) no tempo de filme `tf`."""
    pes = []
    for s0, pt, extra in ((0.0, pt_perto(t, T), dinc), (0.5, pt_longe(t, T), 0.0)):
        bx, by, inc, dedos, chao, k = _passo(tf / P_CICLO, s0, pt)
        inc += extra
        ax, ay = _tornozelo(bx, by, inc)
        pes.append(Pe(ax, ay, inc, dedos, chao, k))
    hy = Y_CHAO - 330
    for p in pes:                                               # o quadril desce o que for preciso p/ as pernas alcançarem
        dx = p.ax - HX0; lmax = L1 + L2 - 2
        if abs(dx) < lmax:
            hy = max(hy, p.ay - math.sqrt(lmax * lmax - dx * dx))
    return (HX0, hy), pes[0], pes[1]


# ------------------------------------------------------------------ desenho da perna (cópia adaptada do cf_crianca_mancando)
def joelho(hx, hy, ax, ay):
    """Cinemática inversa de dois segmentos; o joelho dobra para a frente (+x). (cópia)"""
    dx, dy = ax - hx, ay - hy
    d = max(1.0, min(math.hypot(dx, dy), L1 + L2 - 0.5))
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


def canela(kx, ky, ax, ay, bojo):
    """Perna do joelho ao tornozelo, gordinha: frente quase reta, panturrilha só levemente abaulada."""
    L, ux, uy, nx, ny = _eixo(kx, ky, ax, ay)

    def P(a, b):
        return kx + ux * a + nx * b, ky + uy * a + ny * b
    p = skia.Path()
    p.moveTo(*P(0, R_JOE))
    p.cubicTo(*P(0.35 * L, R_JOE * 0.95), *P(0.72 * L, R_TOR * 1.12), *P(L, R_TOR))
    p.lineTo(*P(L, -R_TOR))
    p.cubicTo(*P(0.80 * L, -R_TOR * 1.06), *P(0.58 * L, -(R_JOE + bojo)), *P(0.36 * L, -(R_JOE + bojo)))
    p.cubicTo(*P(0.18 * L, -(R_JOE + bojo)), *P(0.04 * L, -R_JOE * 1.02), *P(0, -R_JOE))
    p.close()
    c0 = skia.Path(); c0.addCircle(kx, ky, R_JOE)
    c1 = skia.Path(); c1.addCircle(ax, ay, R_TOR)
    return _uniao(_uniao(p, c0), c1)


def _escala(p, k):
    m = skia.Matrix(); m.setScale(k, k)
    q = skia.Path(p); q.transform(m)
    return q


def _pe_tras():
    """Retropé + antepé de perfil, gordinho (origem = tornozelo, x para a frente, y para baixo)."""
    p = skia.Path()
    p.moveTo(14, -18)
    p.cubicTo(30, -9, 45, 3, 55, 12)                            # dorso alto e redondo
    p.lineTo(58, 20)
    p.cubicTo(62, 27, 59, 35, 50, 35)                           # frente da bola
    p.cubicTo(31, 37, 13, 32, -4, 33)                           # sola, arco discreto
    p.cubicTo(-18, 36, -32, 35, -32, 20)                        # calcanhar redondo
    p.cubicTo(-33, 6, -26, -7, -18, -20)
    p.lineTo(-15, -27)
    p.cubicTo(-4, -32, 8, -27, 14, -18)
    p.close()
    return _escala(p, PE_K)


def _pe_dedos():
    """Dedos rechonchudos (origem = junta dos dedos; a sola deles fica em y = +8)."""
    p = skia.Path()
    p.moveTo(-5, -9)
    p.cubicTo(8, -12, 22, -11, 28, -4)
    p.cubicTo(33, 2, 31, 9, 23, 9)
    p.lineTo(-5, 9)
    p.cubicTo(-9, 6, -9, -7, -5, -9)
    p.close()
    return _escala(p, PE_K)


PE_TRAS, PE_DEDOS = _pe_tras(), _pe_dedos()


def _mat(x, y, graus):
    m = skia.Matrix(); m.postRotate(graus); m.postTranslate(x, y)
    return m


def pe_path(pe):
    tras = skia.Path(PE_TRAS); tras.transform(_mat(pe.ax, pe.ay, pe.inc))
    jx, jy = pe.ponto(JUNTA)
    d = skia.Path(PE_DEDOS); d.transform(_mat(jx, jy, pe.dedos))
    return _uniao(tras, d)


def manga_short(hip, joe):
    """Barra do short no referencial da coxa: larga e evasê (roupa de criança). Adaptado do
    cf_crianca_mancando. -> (contorno, (bainha0, bainha1), (ux, uy, nx, ny))"""
    hx, hy = hip; kx, ky = joe
    L = math.hypot(kx - hx, ky - hy) or 1.0
    ux, uy = (kx - hx) / L, (ky - hy) / L; nx, ny = -uy, ux
    ex, ey = hx + ux * 84, hy + uy * 84
    p = skia.Path()
    p.moveTo(hx + nx * 50, hy + ny * 50); p.lineTo(ex + nx * 60, ey + ny * 60)
    p.quadTo(ex + ux * 6, ey + uy * 6, ex - nx * 60, ey - ny * 60)
    p.lineTo(hx - nx * 50, hy - ny * 50); p.close()
    c = skia.Path(); c.addCircle(hx, hy, 50)
    bainha = ((ex + nx * 57 - ux * 13, ey + ny * 57 - uy * 13), (ex - nx * 57 - ux * 13, ey - ny * 57 - uy * 13))
    return _uniao(p, c), bainha, (ux, uy, nx, ny)


def path_cintura(hip):
    """Cintura do short (adaptado do cf_crianca_mancando, com o bumbum redondo de criança pequena)."""
    hx, hy = hip
    p = skia.Path()
    p.moveTo(hx - 62, hy - 74)
    p.lineTo(hx + 54, hy - 74)
    p.cubicTo(hx + 64, hy - 36, hx + 62, hy + 2, hx + 50, hy + 26)
    p.lineTo(hx - 38, hy + 30)
    p.cubicTo(hx - 80, hy + 18, hx - 84, hy - 34, hx - 62, hy - 74)
    p.close()
    return p


def perna(cv, hip, pe, s, longe=False, bojo=BOJO, simples=False, claro=0.0):
    """Perna de criança num contorno só (coxa + perna + pé), pele lisa e OPACA. Sombreado único por
    dentro do contorno (faixas sem desfoque, que é caro). Devolve o joelho.
    `simples`: só a silhueta (os fantasmas do rastro). `claro`: perna de trás menos escura."""
    hx, hy = hip
    kx, ky = joelho(hx, hy, pe.ax, pe.ay)
    corpo = _uniao(_uniao(tubo(hx, hy, R_QUAD, kx, ky, R_JOE), canela(kx, ky, pe.ax, pe.ay, bojo)), pe_path(pe))
    if simples:
        cv.drawPath(corpo, paint(PELE))
        cv.drawPath(corpo, paint(PELE_LINHA, 200, "stroke", 5.0 / s))
        return kx, ky
    f_esc = 0.36 * (1 - claro)
    esc = (lambda c: lerpc(c, "#2A1B16", f_esc)) if longe else (lambda c: c)   # perna de trás, mais escura (opaca)
    cv.save(); cv.clipPath(corpo, skia.ClipOp.kIntersect, True)
    cv.drawPath(corpo, paint(esc(PELE)))
    for larg, cor in ((34, "#EDB197"), (20, "#E5A78B"), (9, "#DA9A80")):     # volume: aro mais escuro (opaco)
        cv.drawPath(corpo, paint(esc(cor), 255, "stroke", larg))
    L, ux, uy, nx, ny = _eixo(kx, ky, pe.ax, pe.ay)
    luz = paint(esc("#F5C4AB"), 255, "stroke", 15)                            # um brilho largo e curto (sem "definição")
    cv.drawLine(kx + nx * 14 + ux * 18, ky + ny * 14 + uy * 18, kx + nx * 10 + ux * 0.62 * L, ky + ny * 10 + uy * 0.62 * L, luz)
    cv.drawLine(hx + 16, hy + 30, kx + nx * 14 - (kx - hx) * 0.2, ky + ny * 14 - (ky - hy) * 0.2, luz)
    a0 = pe.ponto((6, -12)); a1 = pe.ponto((40, 8))
    cv.drawLine(a0[0], a0[1], a1[0], a1[1], paint(esc("#F5C4AB"), 255, "stroke", 11))
    dob = skia.Path(); dob.moveTo(-2, -29); dob.quadTo(11, -28, 17, -16)       # dobrinha do tornozelo (bebê)
    dob.transform(_mat(pe.ax, pe.ay, pe.inc))
    cv.drawPath(dob, paint(esc(PELE_LINHA), 150, "stroke", 3.0))
    jx, jy = pe.ponto(JUNTA)                                                  # dedinhos: duas dobras e a unha
    m = _mat(jx, jy, pe.dedos)
    for (x0, y0), (x1, y1) in (((13, -10), (15, -1)), ((21, -9), (23, 0))):
        p0 = m.mapXY(x0 * PE_K, y0 * PE_K); p1 = m.mapXY(x1 * PE_K, y1 * PE_K)
        cv.drawLine(p0.x(), p0.y(), p1.x(), p1.y(), paint(PELE_LINHA, 120, "stroke", 2.4))
    un = skia.Path(); un.addRRect(skia.RRect.MakeRectXY(skia.Rect(22, -10, 29, -5), 2.5, 2.5)); un.transform(m)
    cv.drawPath(un, paint("#FBE2D6", 210))
    cv.restore()
    cv.drawPath(corpo, paint(PELE_LINHA, 230, "stroke", 5.0 / s))
    return kx, ky


def _bolinhas_manga(cv, eixo, hip, cor, a=210):
    ux, uy, nx, ny = eixo; hx, hy = hip
    for d, o in ((22, -28), (22, 18), (48, -6), (48, 40), (48, -50), (72, -30), (72, 18)):
        cv.drawCircle(hx + ux * d + nx * o, hy + uy * d + ny * o, 6.0, paint(cor, a))


def pernas(cv, hip, perto, longe, s, bojo=BOJO, entre=None, claro=0.0):
    """Perna de trás (mais escura), perna da frente e o short infantil por cima (cós de elástico franzido,
    barra larga, bolinhas). `entre()`: o que vai entre as duas (o rastro da perna da frente)."""
    hx, hy = hip
    kl = perna(cv, hip, longe, s, longe=True, claro=claro)
    m_l, b_l, e_l = manga_short(hip, kl)
    cv.drawPath(m_l, paint(lerpc(SHORT_ESC, SHORT, claro)))
    cv.save(); cv.clipPath(m_l, skia.ClipOp.kIntersect, True)
    _bolinhas_manga(cv, e_l, hip, BOLINHA, 90)
    cv.restore()
    cv.drawPath(m_l, paint(SHORT_LINHA, 220, "stroke", 4.0 / s))
    cv.drawLine(b_l[0][0], b_l[0][1], b_l[1][0], b_l[1][1], paint(SHORT_LINHA, 150, "stroke", 4.0 / s))
    if entre:
        entre()
    kp = perna(cv, hip, perto, s, bojo=bojo)
    m_p, b_p, e_p = manga_short(hip, kp)
    sh = _uniao(path_cintura(hip), m_p)
    cv.drawPath(sh, paint("#000000", 50, blur=8))
    cv.drawPath(sh, paint(SHORT))
    cv.save(); cv.clipPath(sh, skia.ClipOp.kIntersect, True)
    cv.save(); cv.clipPath(m_p, skia.ClipOp.kIntersect, True)                # barra mais clara (barra virada)
    _bolinhas_manga(cv, e_p, hip, BOLINHA)
    ux, uy, nx, ny = e_p
    p0, p1 = b_p
    cv.drawLine(p0[0] + ux * 9, p0[1] + uy * 9, p1[0] + ux * 9, p1[1] + uy * 9, paint(SHORT_CL, 255, "stroke", 16))
    cv.restore()
    for x, y in ((-40, -36), (-6, -50), (26, -32), (-30, 0), (8, -10), (40, 4)):   # bolinhas da cintura
        cv.drawCircle(hx + x, hy + y, 6.0, paint(BOLINHA, 210))
    cv.drawRect(skia.Rect(hx - 95, hy - 80, hx + 95, hy - 52), paint(SHORT_CL))   # cós de elástico
    fr = skia.Path(); x = hx - 92
    while x < hx + 92:
        fr.moveTo(x, hy - 76); fr.lineTo(x + 1.5, hy - 56); x += 8
    cv.drawPath(fr, paint(SHORT_LINHA, 110, "stroke", 2.2))
    cv.drawLine(hx - 95, hy - 52, hx + 95, hy - 52, paint(SHORT_LINHA, 160, "stroke", 3.0))
    cv.restore()
    cv.drawPath(sh, paint(SHORT_LINHA, 230, "stroke", 4.4 / s))
    cv.drawLine(b_p[0][0], b_p[0][1], b_p[1][0], b_p[1][1], paint(SHORT_LINHA, 150, "stroke", 4.0 / s))
    return kp


# ------------------------------------------------------------------ câmera (mundo -> tela)
BASE = (1.95, HX0 + 10, Y_CHAO, 540, Y_TELA_CHAO)
ESQ = (1.72, HX0 + 15, Y_CHAO, 380, Y_TELA_CHAO)                 # pernas à esquerda: lugar p/ bolo e calendário
ABERTO = (1.7, HX0 - 10, Y_CHAO, 540, Y_TELA_CHAO)


def _mist(a, b, k):
    return tuple(lerp(x, y, k) for x, y in zip(a, b))


def camera(t, T, F):
    cam = BASE
    hz = pose(F.tf_fz, T["calcanhar"], T)[1].calcanhar()
    hip_l, pl, ll = pose(F.tf_lado, T["lado"], T)
    g = elastico_geo(hip_l, pl)
    hc = pl.calcanhar()
    mx = (pl.bola()[0] + ll.calcanhar()[0]) / 2
    passos = (
        (T["camera"], 0.8, (2.2, HX0 + 30, Y_CHAO - 10, 540, Y_TELA_CHAO - 10)),     # chega no pé
        (T["calcanhar"], 0.13, (3.0, hz[0], (hz[1] + Y_CHAO) / 2, 500, 860)),        # zoom seco no calcanhar
        (T["nos"], 0.5, BASE),
        (T["mas"], 0.02, ESQ),                                                        # corte: fita 2 (bolo)
        (T["ainda"] - 0.05, 0.5, BASE),
        (T["fica"], 0.02, ABERTO),                                                    # corte: fita 3
        (T["lado"], 0.16, (2.2, mx, Y_CHAO - 50, 540, 980)),
        (T["panturrilha"], 0.4, (2.45, (g["topo"][0] + hc[0]) / 2 - 10, (g["topo"][1] + hc[1]) / 2 + 10, 610, 770)),
        (T["durinha"] + 0.66, 0.4, ESQ),                                              # sai ANTES do calendário
        (T["esses"], 0.6, ABERTO),                                                    # fundo dos melhores momentos
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


# ------------------------------------------------------------------ chão, bolo, sombras
def chao(cv, tf, s, f=1):
    """Chão de cada fita, correndo com a esteira. 1: estúdio (linha + risquinhos; a faixa em degradê é
    desenhada em tela); 2: piso de madeira (tábuas em 3 fileiras); 3: tapete de EVA (placas coloridas)."""
    G = VEL * tf
    x0, x1 = HX0 - 900, HX0 + 900
    if f == 1:
        cv.drawLine(x0, Y_CHAO, x1, Y_CHAO, paint("#CFE3F5", 200, "stroke", 5.0 / s))
        for passo, y, comp, a, fat in ((60, Y_CHAO + 22, 22, 70, 1.0), (90, Y_CHAO + 58, 34, 42, 1.25)):
            off = (G * fat) % passo
            x = x0 - off
            pth = skia.Path()
            while x < x1:
                pth.moveTo(x, y); pth.lineTo(x + comp, y)
                x += passo
            cv.drawPath(pth, paint("#FFFFFF", a, "stroke", 6.0 / s))
        return
    if f == 2:
        filas = ((Y_CHAO, Y_CHAO + 30, 250, 1.0, 0.0), (Y_CHAO + 30, Y_CHAO + 72, 300, 1.2, 0.45),
                 (Y_CHAO + 72, Y_CHAO + 132, 350, 1.45, 0.2), (Y_CHAO + 132, Y_CHAO + 420, 420, 1.8, 0.7))
        cores, junta = MADEIRA, MADEIRA_JUNTA
    else:
        filas = ((Y_CHAO, Y_CHAO + 40, 120, 1.0, 0.0), (Y_CHAO + 40, Y_CHAO + 100, 150, 1.25, 0.5),
                 (Y_CHAO + 100, Y_CHAO + 420, 190, 1.6, 0.25))
        cores, junta = EVA, EVA_JUNTA
    pj = skia.Path()
    for r, (y0, y1, larg, fat, defas) in enumerate(filas):
        g = G * fat - defas * larg
        j = math.floor((x0 + g) / larg)
        while True:
            x = j * larg - g
            if x > x1:
                break
            cor = cores[(j * (2 if f == 2 else 1) + r * 3) % len(cores)]
            cv.drawRect(skia.Rect(x, y0, x + larg, y1), paint(cor))
            if f == 2:                                          # um veio claro em cada tábua
                yv = y0 + (y1 - y0) * (0.35 + 0.3 * ((j * 7) % 3) / 2)
                cv.drawLine(x + larg * 0.12, yv, x + larg * 0.7, yv, paint(MADEIRA_VEIO, 255, "stroke", 2.4 / s))
            pj.moveTo(x, y0); pj.lineTo(x, y1)
            j += 1
        pj.moveTo(x0, y0); pj.lineTo(x1, y0)
    cv.drawPath(pj, paint(junta, 255, "stroke", 3.0 / s))
    cv.drawLine(x0, Y_CHAO, x1, Y_CHAO, paint("#E9D2B8" if f == 2 else "#CFE3F5", 220, "stroke", 5.0 / s))


def sombra_pe(cv, pe):
    """Sombra no chão sob o pé: escura sob a ponta que encosta, fraca sob o calcanhar no ar."""
    baixo = max(pe.ponto(p)[1] for p in (CALC, BOLA))
    a = clamp(1 - (Y_CHAO - baixo) / 70)
    if a <= 0:
        return
    xb, xc = pe.bola()[0], pe.calcanhar()[0]
    ac = clamp(1 - (Y_CHAO - pe.calcanhar()[1]) / 40)
    cv.drawOval(skia.Rect(xb - 26, Y_CHAO - 5, xb + 48, Y_CHAO + 7), paint("#000000", int(110 * a), blur=5))
    cv.drawOval(skia.Rect(min(xb, xc) - 4, Y_CHAO - 4, max(xb, xc) + 4, Y_CHAO + 6),
                paint("#000000", int(60 * a * (0.3 + 0.7 * ac)), blur=6))


def bolo(cv, x, y, a, velas, chamas, t, esc=1.0):
    """Bolo de aniversário de desenho (dois andares, cobertura escorrendo), SEM número e SEM texto, em
    coordenadas de TELA (preso à tela, não ao chão que corre). `velas`/`chamas`: 0..1 de cada uma."""
    if a <= 0:
        return
    cv.saveLayer(skia.Rect(x - 160 * esc, y - 280 * esc, x + 160 * esc, y + 40 * esc), _alfa(a)) if a < 1 else cv.save()
    cv.translate(x, y); cv.scale(esc, esc)
    cv.drawOval(skia.Rect(-96, -10, 96, 12), paint("#000000", 70, blur=8))
    cv.drawOval(skia.Rect(-92, -14, 92, 8), paint("#DDE6EE"))                          # prato
    cv.drawOval(skia.Rect(-92, -14, 92, 8), paint("#8FA3B8", 255, "stroke", 2.5))
    for (w, y0, y1) in ((150, -78, -6), (104, -134, -78)):                            # andares
        r = skia.RRect.MakeRectXY(skia.Rect(-w / 2, y0, w / 2, y1), 10, 10)
        cv.drawRRect(r, paint("#F3DDB8"))
        cv.drawRect(skia.Rect(-w / 2, y1 - 20, w / 2, y1 - 12), paint("#E9C98F"))     # recheio
        cob = skia.Path(); cob.moveTo(-w / 2, y0 + 8)
        n = 6
        for i in range(n):                                                             # cobertura escorrendo
            xa = -w / 2 + w * i / n; xb = -w / 2 + w * (i + 0.5) / n; xc = -w / 2 + w * (i + 1) / n
            gota = 16 + 10 * ((i * 7) % 3)
            cob.lineTo(xa, y0 + 12); cob.quadTo(xb, y0 + 12 + gota * 2.0, xc, y0 + 12)
        cob.lineTo(w / 2, y0 + 8); cob.lineTo(w / 2, y0 + 6); cob.quadTo(0, y0 - 6, -w / 2, y0 + 6); cob.close()
        cv.drawPath(cob, paint("#FFF8EE"))
        cv.drawRRect(r, paint("#B98E57", 255, "stroke", 2.5))
        for k in range(5):                                                             # granulado dourado
            cv.drawCircle(-w / 2 + 16 + k * (w - 32) / 4, (y0 + y1) / 2 + 8, 3.2, paint(OURO))
    for i in range(3):                                                                 # velas
        v = velas[i]
        if v <= 0:
            continue
        xv = -30 + 30 * i
        hv = 40 * e_back(clamp(v))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(xv - 5, -134 - hv, xv + 5, -134), 3, 3), paint("#FFFFFF"))
        cv.save(); cv.clipRect(skia.Rect(xv - 5, -134 - hv, xv + 5, -134))
        for k in range(4):
            yy = -134 - hv + 4 + k * 11
            cv.drawLine(xv - 6, yy + 6, xv + 6, yy, paint(AZUL_CL, 255, "stroke", 3))
        cv.restore()
        cv.drawLine(xv, -134 - hv, xv, -134 - hv - 6, paint("#5E7186", 255, "stroke", 2))   # pavio
        c = chamas[i]
        if c > 0:
            fl = 1 + 0.08 * math.sin(t * 23 + i * 2.1)
            hf = 18 * e_back(clamp(c)) * fl
            cv.drawCircle(xv, -134 - hv - 12, 20 * clamp(c), paint(OURO, 110, blur=12))
            ch = skia.Path(); yb = -134 - hv - 4
            ch.moveTo(xv, yb - hf * 1.6)
            ch.cubicTo(xv + 8, yb - hf * 0.8, xv + 7, yb, xv, yb)
            ch.cubicTo(xv - 7, yb, xv - 8, yb - hf * 0.8, xv, yb - hf * 1.6)
            cv.drawPath(ch, paint("#FFB627"))
            cv.drawCircle(xv, yb - hf * 0.45, 3.2 * clamp(c), paint("#FFF4CC"))
    cv.restore()


# ------------------------------------------------------------------ camadas fixas em cache (desempenho)
# Neste skia, preencher área grande com cor translúcida ou degradê custa ~0,2-0,45 s por quadro, e
# desenhar uma IMAGEM pronta (mesmo translúcida) custa ~2 ms: as camadas que não mudam viram imagem.
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
    """O mesmo fundo do cf_alongamento.fundo (degradê radial que respira + partículas), com o degradê
    pronto em imagem."""
    def d(c):
        sh = skia.GradientShader.MakeRadial(skia.Point(W / 2, H * 0.42 + 60), H * 0.78, [_c("#17384C"), _c(BG_OUT)])
        c.drawRect(skia.Rect(0, 0, W, H + 120), paint("#17384C", shader=sh))
    _blit(cv, _img("fundo", W, H + 120, d), 0, -60 + 40 * math.sin(t * 0.3))
    for x, y, v, r, a in PART:
        yy = (y - v * t * 6) % H
        cv.drawCircle(x + 8 * math.sin(t * 0.5 + y), yy, r, paint("#BFE3FF", int(a)))


def _rel(c):
    """Desenha no referencial da imagem do tamanho da CENA."""
    c.translate(-CENA.left(), -CENA.top())


# ------------------------------------------------------------------ efeitos de "replay" (tela)
def monitor_fundo(cv):
    def d(c):
        _rel(c)
        c.drawRect(CENA, paint("#FFFFFF", 9))
        sh = skia.GradientShader.MakeRadial(skia.Point(540, 760), 780, [_c("#000000", 0), _c("#000000", 0), _c("#000000", 85)],
                                            [0.0, 0.55, 1.0])
        c.drawRect(CENA, paint("#000000", 255, shader=sh))
    _blit(cv, _img("monitor", CENA.width(), CENA.height(), d), CENA.left(), CENA.top())


def faixa_chao(cv, gy):
    """Faixa do chão (degradê) em coordenadas de TELA, a partir da linha do chão `gy`."""
    def d(c):
        sh = skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, 300)], [_c("#FFFFFF", 34), _c("#FFFFFF", 6)])
        c.drawRect(skia.Rect(0, 0, CENA.width(), 700), paint("#FFFFFF", 255, shader=sh))
    _blit(cv, _img("chao", CENA.width(), 700, d), CENA.left(), gy)


def profundidade(cv, gy):
    """Fitas 2 e 3: o chão escurece para baixo (profundidade), em imagem pronta."""
    def d(c):
        sh = skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, 520)], [_c(BG_OUT, 0), _c(BG_OUT, 170)])
        c.drawRect(skia.Rect(0, 0, CENA.width(), 900), paint(BG_OUT, 255, shader=sh))
    _blit(cv, _img("prof", CENA.width(), 900, d), CENA.left(), gy + 6)


def varredura(cv, t, ambar, limpo=False):
    """Linhas de varredura + granulação (semente = índice do quadro) + moldura âmbar da câmera lenta.
    `limpo` (miniaturas): só a moldura âmbar."""
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
    """Faixas de 'tracking' de fita de vídeo varrendo a cena (voltar e avançar a fita)."""
    if a <= 0:
        return
    for i in range(3):
        y = CENA.top() + ((t * 1300 + i * 330) % (CENA.height() + 60)) - 30
        h = 18 + 10 * i
        cv.drawRect(skia.Rect(CENA.left(), y, CENA.right(), y + h), paint("#FFFFFF", int(46 * a)))
        cv.drawRect(skia.Rect(CENA.left(), y + h, CENA.right(), y + h + 4), paint("#000000", int(70 * a)))


def corte_fita(cv, t, t0):
    """Corte de fita: chiado (faixas de ruído e neve) por ~0,2 s — a cena (e o chão) muda por baixo dele."""
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


HUD_X, HUD_Y = 786, 1166                                         # centro do relógio
X_BOLO = 800                                                     # onde o bolo para (tela)
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
        ant = [x for x in F.segs if x[1] <= t0 + 1e-6 and x[2] != "congela"]
        tipo_v = ant[-1][2] if ant else "play"
        s = "0,25×" if tipo_v == "lenta" and lento_k(t, T) > 0 else "1×"
        chip_c(cv, s, *_chip_hud_c(s), a, dim=0.4)
        return
    s = "0,25×" if tipo == "lenta" else "1×"
    hx, hy = _chip_hud_c(s)
    k = t - t0
    if tipo == "lenta" and k < 0.75:                             # "0,25×" grande no meio, que voa para o painel
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


def ponta_seta(cv, x, y, ang, tam, cor, a):
    p = skia.Path()
    p.moveTo(x + tam * math.cos(ang), y + tam * math.sin(ang))
    p.lineTo(x + tam * 0.75 * math.cos(ang + 2.45), y + tam * 0.75 * math.sin(ang + 2.45))
    p.lineTo(x + tam * 0.75 * math.cos(ang - 2.45), y + tam * 0.75 * math.sin(ang - 2.45))
    p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))


def estetoscopio(cv, x, y, esc, a):
    """Selo branco e calmo do "vale uma avaliação": estetoscópio desenhado (forma, sem texto)."""
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
    """Folhas virando, sem número (cópia do cf_fratura_cola, cabeçalho azul-claro: nada de vermelho).
    `t_para`: a partir daí as folhas param de virar."""
    if a <= 0:
        return
    ent = lerp(0.6, 1.0, e_back(prog(t, t0, t0 + 0.3)))
    cv.save(); cv.translate(x + 48 * esc, y + 46 * esc); cv.scale(esc * ent, esc * ent); cv.translate(-48, -46)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(3, 5, 99, 97), 12, 12), paint("#000000", int(80 * a), blur=8))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(0, 0, 96, 92), 12, 12), paint("#EEF3F8", int(255 * a)))
    cv.save(); cv.clipRRect(skia.RRect.MakeRectXY(skia.Rect(0, 0, 96, 92), 12, 12), True)
    cv.drawRect(skia.Rect(0, 0, 96, 24), paint(AZUL_CL, int(255 * a)))
    cv.restore()
    for xx in (24, 72):
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(xx - 4, -8, xx + 4, 10), 3, 3), paint("#5E7186", int(255 * a)))
    tt = t if t_para is None else min(t, t_para)
    k = (tt - t0) * 5
    fase = k - math.floor(k)
    if t_para is not None and t >= t_para:
        fase = 0.0
    for i in range(3):
        cv.drawLine(14, 42 + i * 16, 82, 42 + i * 16, paint("#9AA8B5", int(200 * a), "stroke", 4))
    if fase > 0:
        cv.save(); cv.translate(0, 24); cv.scale(1, 1 - fase)
        cv.drawRect(skia.Rect(0, 0, 96, 68), paint("#FFFFFF", int(170 * a * (1 - fase))))
        cv.restore()
    cv.restore()


# ------------------------------------------------------------------ trajetória dourada do calcanhar
def _calc_rel(u):
    """Calcanhar do pé de perto (na ponta) em relação ao quadril, na fase u do ciclo."""
    bx, by, inc, dedos, chao_, k = _passo(u, 0.0, 1.0)
    ax, ay = _tornozelo(bx, by, inc)
    r = rot(CALC, inc)
    return ax + r[0] - HX0, ay + r[1]


_US = [i / 400 for i in range(400)]
PICO_U = min(((_calc_rel(u)[1], u) for u in _US if u >= SD))[1]   # calcanhar mais alto no balanço
CX_CALC = sum(_calc_rel(u)[0] for u in _US) / len(_US)            # x médio do calcanhar (rel. ao quadril)


def pico_depois(tau):
    """Primeiro instante de filme >= tau em que o calcanhar de perto está no alto do balanço."""
    m = math.floor(tau - PICO_U)
    while m + PICO_U < tau - 1e-9:
        m += 1
    return m + PICO_U


def trilha_lenta(T, t, tau0, tf_agora):
    """Câmera lenta: o caminho real do calcanhar, do alto do balanço até o pouso (no referencial do
    chão de AGORA). Nesse trecho o caminho é uma curva lisa: não passa pelo apoio (onde fazia o 'V')."""
    pts = []
    tau = tau0
    while tau < tf_agora:
        h = pose(tau, t, T)[1].calcanhar()
        pts.append((h[0] - VEL * (tf_agora - tau), h[1]))
        tau += 0.006
    h = pose(tf_agora, t, T)[1].calcanhar()
    pts.append(h)
    return pts


def trilha_onda(T, t, tau0, tf_agora):
    """Avanço rápido ("o tempo todo"): GRÁFICO da altura do calcanhar riscado no chão que corre — uma
    onda lisa que nunca encosta no chão. A pena fica no x médio do calcanhar; só a ponta final se curva
    até o calcanhar de verdade."""
    taus = []
    tau = tau0
    while tau < tf_agora:
        taus.append(tau); tau += 0.01
    taus.append(tf_agora)
    hs = [pose(x, t, T)[1].calcanhar() for x in taus]
    ys = np.array([h[1] for h in hs])
    if len(ys) > 9:
        ys = np.convolve(np.pad(ys, 4, mode="edge"), np.ones(9) / 9, "valid")
    pts = []
    for x, h, y in zip(taus, hs, ys.tolist()):
        xl = HX0 + CX_CALC - VEL * (tf_agora - x)
        xa = h[0] - VEL * (tf_agora - x)
        w = sstep((x - (tf_agora - 0.16)) / 0.16)
        pts.append((lerp(xl, xa, w), lerp(y, h[1], w)))
    return pts


def desenha_trilha(cv, pts, a, s):
    """Pontilhado dourado no referencial do MUNDO (dentro de mundo(), por baixo das pernas)."""
    if a <= 0 or len(pts) < 2:
        return
    p = skia.Path()
    p.moveTo(*pts[0])
    for i in range(1, len(pts) - 1):                            # curva lisa pelos pontos médios
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


# ------------------------------------------------------------------ o "durinha": o calcanhar tenta descer e o elástico puxa de volta
DESCE, SEGURA, QUEDA = 0.3, 0.62, -27.0                          # desce em 0,3 s, segura até 0,62 s, solta


def dinc_durinha(t, T):
    k = t - T["durinha"]
    if k < 0:
        return 0.0
    if k < SEGURA:
        v = QUEDA * e_out(clamp(k / DESCE))
        v += 0.9 * math.sin(k * 64) * prog(k, DESCE, DESCE + 0.06)              # treme na tensão máxima
    else:                                                                      # o estalo: volta e quica
        k2 = k - SEGURA
        v = QUEDA * (1 - e_out(clamp(k2 / 0.1))) + 6.0 * math.exp(-k2 / 0.13) * math.sin(k2 * 42) * prog(k2, 0.0, 0.04)
    return v * (1 - prog(t, T["demorou"] + 0.1, T["demorou"] + 0.5))


D_ANEL = 0.46                                                   # anel: no meio da panturrilha (fração da perna)
ALCA_PRESA = (-33.5, 21.0)                                       # borda de trás do calcanhar (referencial do pé)


def elastico_geo(hip, pe):
    """Onde o elástico se prende: um ANEL que abraça a panturrilha e uma ALÇA em volta do calcanhar (o
    elástico cruza o tornozelo: quando o calcanhar desce, ele estica)."""
    kx, ky = joelho(hip[0], hip[1], pe.ax, pe.ay)
    L, ux, uy, nx, ny = _eixo(kx, ky, pe.ax, pe.ay)

    def P(a_, b_):
        return kx + ux * a_ + nx * b_, ky + uy * a_ + ny * b_
    d = D_ANEL * L
    return {"P": P, "d": d, "topo": P(d + 4, -(R_JOE + BOJO * 0.85)), "pe": pe.ponto(ALCA_PRESA)}


def _faixa_recortada(cv, sil, path, larg, a, s):
    """Faixa que ABRAÇA a perna: desenhada só dentro do contorno (as pontas somem na borda)."""
    cv.save(); cv.clipPath(sil, skia.ClipOp.kIntersect, True)
    cv.drawPath(path, paint("#000000", int(60 * a), "stroke", (larg + 8) / s, blur=3 / s))
    cv.drawPath(path, paint(LIMA_ESC, int(255 * a), "stroke", (larg + 4) / s))
    cv.drawPath(path, paint(LIMA, int(255 * a), "stroke", larg / s))
    cv.drawPath(path, paint(LIMA_CL, int(200 * a), "stroke", 2.2 / s))
    cv.restore()


def elastico(cv, t, T, F, hip, perto, s):
    """Elástico de brinquedo, verde-limão: um anel abraça a panturrilha, uma alça abraça o calcanhar e uma
    faixa chata corre POR FORA, atrás da perna, entre os dois. Em repouso já reta e esticada. No "durinha"
    o calcanhar desce: a faixa ALONGA, afina, clareia e treme; no estalo, ela puxa de volta e balança."""
    a = prog(t, T["panturrilha"] + 0.1, T["panturrilha"] + 0.25) * (1 - prog(t, T["demorou"] + 0.05, T["demorou"] + 0.3))
    if a <= 0:
        return
    g = elastico_geo(hip, perto)
    g0 = elastico_geo(*pose(F.tf(t), t, T)[:2])                    # sem o "durinha": comprimento de repouso
    P, d = g["P"], g["d"]
    kx, ky = P(0, 0)
    sil = _uniao(canela(kx, ky, perto.ax, perto.ay, BOJO), pe_path(perto))
    # anel da panturrilha: de lado a lado da perna, curvo (abraça), recortado no contorno
    k1 = e_back(prog(t, T["panturrilha"] + 0.1, T["panturrilha"] + 0.3))
    if k1 > 0:
        an = skia.Path(); an.moveTo(*P(d - 6, R_JOE + 20)); an.quadTo(*P(d + 16, -2), *P(d + 6, -(R_JOE + BOJO + 20)))
        _faixa_recortada(cv, sil, an, 10 * k1, a, s)
    # alça do calcanhar: da borda de trás do calcanhar até a frente do tornozelo (como alça de sandália)
    k2 = e_back(prog(t, T["panturrilha"] + 0.35, T["panturrilha"] + 0.55))
    if k2 > 0:
        al = skia.Path(); al.moveTo(*perto.ponto((-46.0, 30.0))); al.quadTo(*perto.ponto((-6.0, 22.0)), *perto.ponto((26.0, -16.0)))
        _faixa_recortada(cv, sil, al, 10 * k2, a, s)
    # a faixa
    (x0, y0), (x1, y1) = g["topo"], g["pe"]
    L = math.hypot(x1 - x0, y1 - y0) or 1.0
    L0 = math.hypot(g0["pe"][0] - g0["topo"][0], g0["pe"][1] - g0["topo"][1]) or 1.0
    r = max(1.0, L / L0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = -uy, ux
    cresce = e_out(prog(t, T["panturrilha"] + 0.3, T["panturrilha"] + 0.55))
    if cresce <= 0:
        return
    larg = 27.0 / (r ** 2.6) / s                                    # larguras em px de TELA
    tensao = clamp((r - 1) / 0.12)
    k3 = t - T["durinha"] - SEGURA                                  # balanço depois do estalo
    bal = 7.0 * math.exp(-k3 / 0.16) * math.sin(k3 * 46) if k3 > 0 else 0.0
    n = 18
    meio = []
    for i in range(n + 1):
        u = i / n * cresce
        b = bal * math.sin(math.pi * u) + 1.2 * tensao * math.sin(t * 90 + u * 9) * math.sin(math.pi * u)
        meio.append((x0 + ux * L * u + nx * b, y0 + uy * L * u + ny * b))
    fx = skia.Path()
    for i, (x, y) in enumerate(meio):
        (fx.moveTo if i == 0 else fx.lineTo)(x, y)
    cor = lerpc(LIMA, LIMA_CL, 0.6 * tensao)
    cv.drawPath(fx, paint("#000000", int(80 * a), "stroke", larg + 8 / s, blur=3 / s))
    cv.drawPath(fx, paint(LIMA_ESC, int(255 * a), "stroke", larg + 5 / s))
    cv.drawPath(fx, paint(cor, int(255 * a), "stroke", larg))
    cos = skia.Path()                                               # costura no meio: 6 tracinhos AO LONGO da faixa,
    for i in range(6):                                              # que se alongam e se afastam quando ela estica
        u0, u1 = (i + 0.25) / 6 * cresce, (i + 0.75) / 6 * cresce
        cos.moveTo(x0 + ux * L * u0 + nx * (bal * math.sin(math.pi * u0)), y0 + uy * L * u0 + ny * (bal * math.sin(math.pi * u0)))
        cos.lineTo(x0 + ux * L * u1 + nx * (bal * math.sin(math.pi * u1)), y0 + uy * L * u1 + ny * (bal * math.sin(math.pi * u1)))
    cv.drawPath(cos, paint(LIMA_ESC, int(220 * a), "stroke", 3.0 / s))
    if tensao > 0.05:                                               # marcas de tensão dos dois lados
        for sgn in (-1, 1):
            for f in (0.36, 0.5, 0.64):
                o = larg / 2 + 12 / s
                cx_ = x0 + ux * L * f + nx * sgn * o
                cy_ = y0 + uy * L * f + ny * sgn * o
                cv.drawLine(cx_ - ux * 9 / s, cy_ - uy * 9 / s, cx_ + ux * 9 / s, cy_ + uy * 9 / s,
                            paint(LIMA_CL, int(230 * a * tensao), "stroke", 3.4 / s))


# ------------------------------------------------------------------ o mundo (dentro do monitor)
def janela_trilha(t, T, F):
    """-> (função da trilha, tau0, alfa) ou None. 1ª câmera lenta: do alto do último balanço até o pouso
    (e no congelamento). "O tempo todo": onda desde o 1º pico depois do "tempo"."""
    if T["lenta"] <= t < T["nos"]:
        return (trilha_lenta, F.n_pouso - 1 + PICO_U,
                prog(t, T["lenta"], T["lenta"] + 0.15) * (1 - prog(t, T["nos"] - 0.25, T["nos"] - 0.02)))
    if T["tempo"] <= t < T["fica"]:
        return (trilha_onda, pico_depois(F.tf(T["tempo"])),
                prog(t, T["tempo"], T["tempo"] + 0.15) * (1 - prog(t, T["fica"] - 0.25, T["fica"] - 0.02)))
    return None


OBTURADOR = {"play": 0.09, "volta": 0.03, "avanca": 0.035}      # s de VÍDEO: ~0,12 ciclo de filme em cada um
N_AMOSTRAS = 6
CAIXA_PERNAS = skia.Rect(HX0 - 480, Y_CHAO - 600, HX0 + 480, Y_CHAO + 90)


def amostras_borrao(t, T, F):
    """Instantes (vídeo) que entram no borrão de movimento de `t`, do mais novo ao mais velho: só trechos
    em 1×, voltando ou avançando, sem atravessar corte de fita nem congelamento, e nunca antes de t = 0
    (o quadro 0 sai nítido)."""
    tipo = F.tipo(t)
    obt = OBTURADOR.get(tipo)
    if not obt:
        return [t]
    f = fita(t, T)
    out = [t]
    for i in range(1, N_AMOSTRAS):
        tg = t - obt * i / (N_AMOSTRAS - 1)
        if tg < 0 or fita(tg, T) != f or F.tipo(tg) == "congela":
            break
        out.append(tg)
    return out


def pernas_borradas(cv, t, T, F, s, claro):
    """Borrão de movimento do 1× (o que o olho pega): a MÉDIA das poses dentro do obturador. Cada amostra
    entra numa camada com alfa 1/(k+1) (média corrida): cor e cobertura saem na proporção exata do tempo
    em que a perna esteve em cada lugar."""
    ams = amostras_borrao(t, T, F)
    if len(ams) == 1:
        hip, perto, longe = pose(F.tf(t), t, T, dinc_durinha(t, T))
        pernas(cv, hip, perto, longe, s, claro=claro)
        return
    cv.saveLayer(CAIXA_PERNAS, None)
    for k, tg in enumerate(reversed(ams)):                      # do mais velho ao mais novo
        hip, perto, longe = pose(F.tf(tg), tg, T, dinc_durinha(tg, T))
        if k == 0:
            pernas(cv, hip, perto, longe, s, claro=claro)
        else:
            cv.saveLayer(CAIXA_PERNAS, _alfa(1.0 / (k + 1)))
            pernas(cv, hip, perto, longe, s, claro=claro)
            cv.restore()
    cv.restore()


# ------------------------------------------------------------------ a revelação: luz no vão sob o calcanhar
# contorno da sola (referencial do pé, antes do PE_K), um pouco PARA DENTRO do pé (o pé cobre a sobra)
SOLA_VAO = ((-31.0, 23.0), (-25.0, 31.0), (-12.0, 31.0), (-4.0, 30.0), (12.0, 30.0), (30.0, 32.0), (47.0, 31.0))


def janela_luz(t, T, F):
    """0..1: a luz no vão. Fita 1: acende quando o pé pousa pela ponta e fica no congelamento do "calcanhar".
    Fita 3: acende quando o pé de perto pousa no "lado" e apaga antes do elástico."""
    return max(prog(t, F.t_toque, F.t_toque + 0.2) * (1 - prog(t, T["nos"] - 0.25, T["nos"])),
               prog(t, T["lado"] - 0.02, T["lado"] + 0.18) * (1 - prog(t, T["panturrilha"] - 0.25, T["panturrilha"])))


def luz_vao(cv, t, T, pe, a, s, forte=0.0):
    """Luz dourada no espaço entre o calcanhar e o chão (só se o pé está no chão e o calcanhar no ar). É
    desenhada ANTES da perna de perto: o pé cobre o que sobra, e o que fica visível é exatamente o vão."""
    if a <= 0 or not pe.chao:
        return
    cx_, cy_ = pe.calcanhar()
    if Y_CHAO - cy_ < 10:                                       # calcanhar no chão: não passa luz
        return
    pts = [pe.ponto((x * PE_K, y * PE_K)) for x, y in SOLA_VAO]
    p = skia.Path()
    p.moveTo(pts[0][0], Y_CHAO)
    for x, y in pts:
        p.lineTo(x, min(y, Y_CHAO))
    p.lineTo(pts[-1][0], Y_CHAO)
    p.close()
    x0, x1 = pts[0][0], pts[-1][0]
    pulso = 0.9 + 0.1 * math.sin(t * 7.0)
    aa = a * pulso * (1 + 0.15 * forte)
    # luz e não objeto: sem borda dura, mais forte rente ao chão e sumindo para cima; o chão em volta acende
    # (mistura "tela": clareia o que está por baixo, como luz)
    def luz(pt):
        pt.setBlendMode(skia.BlendMode.kScreen)
        return pt
    cv.drawOval(skia.Rect(x0 - 6, Y_CHAO - 12, x1 + 14, Y_CHAO + 18), luz(paint(OURO, int(min(255, 190 * aa)), blur=10.0 / s)))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, cy_ + 2), skia.Point(0, Y_CHAO)],
                                        [_c(OURO, int(min(255, 40 * aa))), _c(OURO, int(min(255, 200 * aa))), _c("#FFF3C4", int(min(255, 255 * aa)))],
                                        [0.0, 0.5, 1.0])
    cv.drawPath(p, luz(paint(OURO, 255, blur=3.0 / s, shader=sh)))
    cv.drawPath(p, paint(OURO, int(min(255, 70 * aa)), blur=3.0 / s))
    cv.drawLine(x0 - 10, Y_CHAO, x1 + 4, Y_CHAO, luz(paint("#FFF8E2", int(min(255, 255 * aa)), "stroke", 5.0 / s, blur=1.5 / s)))


def mundo(cv, t, T, F, cam):
    """Chão da fita, sombras, trilha (por baixo), pernas (borradas no 1×, nítidas na lenta), luz no vão e
    elástico (referencial do mundo)."""
    tf = F.tf(t)
    tipo = F.tipo(t)
    f = fita(t, T)
    hip, perto, longe = pose(tf, t, T, dinc_durinha(t, T))
    s = cam[0]
    chao(cv, tf, s, f)
    sombra_pe(cv, longe); sombra_pe(cv, perto)
    jt = janela_trilha(t, T, F)
    if jt and jt[2] > 0 and tf > jt[1]:
        desenha_trilha(cv, jt[0](T, t, jt[1], tf), jt[2], s)
    claro = 0.8 if f == 3 else 0.0                              # "só de um lado": as duas pernas bem visíveis
    if tipo in OBTURADOR:                                       # 1×, voltando, avançando: borrado
        pernas_borradas(cv, t, T, F, s, claro)
        return hip, perto, longe
    a_luz = janela_luz(t, T, F)
    forte = max(1 - prog(t, T["calcanhar"], T["calcanhar"] + 0.6) if t >= T["calcanhar"] else 0.0,
                1 - prog(t, T["lado"], T["lado"] + 0.6) if t >= T["lado"] else 0.0)
    pernas(cv, hip, perto, longe, s, entre=(lambda: luz_vao(cv, t, T, perto, a_luz, s, forte)) if a_luz > 0 else None,
           claro=claro)
    elastico(cv, t, T, F, hip, perto, s)
    return hip, perto, longe


def lento_k(t, T):
    """0..1: quanto a câmera lenta está LIGADA (selo e moldura âmbar existem só aqui): da desaceleração
    ("câmera", "também") até o fim do congelamento que fecha cada câmera lenta. Apaga ANTES de o filme voltar
    a 1× ou avançar ("nos") e antes do elástico ("panturrilha"): nenhum quadro fora da lentidão tem selo."""
    return max(prog(t, T["camera"], T["camera"] + 0.18) * (1 - prog(t, T["nos"] - 0.22, T["nos"] - 0.02)),
               prog(t, T["tambem"], T["tambem"] + 0.18) * (1 - prog(t, T["panturrilha"] - 0.22, T["panturrilha"] - 0.02)))


def monitor(cv, t, T, F, limpo=False):
    """Tudo o que fica DENTRO do monitor de replay (recortado em CENA). `limpo`: miniatura (sem linhas de
    varredura, grão, chiado nem flash). -> (câmera, y do chão na tela, x do bolo)."""
    tipo = F.tipo(t)
    f = fita(t, T)
    cam = camera(t, T, F)
    if tipo == "volta":                                           # tremidinha de fita voltando
        j = math.sin(t * 97) * 4 + math.sin(t * 41) * 3
        cam = (cam[0], cam[1], cam[2], cam[3] + j, cam[4])
    for tc in (T["mas"], T["fica"]):                              # salto de quadro no corte
        if 0 <= t - tc < 0.18 and not limpo:
            j = 40 * math.sin((t - tc) * 140) * (1 - (t - tc) / 0.18)
            cam = (cam[0], cam[1], cam[2], cam[3] + j, cam[4] - j * 0.3)
    _, gy = na_tela(cam, 0, Y_CHAO)

    cv.save(); cv.clipRect(CENA, True)
    monitor_fundo(cv)
    if f == 1:
        faixa_chao(cv, gy)
    cv.save(); aplica(cv, cam)
    hip, perto, longe = mundo(cv, t, T, F, cam)
    cv.restore()
    if f != 1:
        profundidade(cv, gy)

    # o bolo (fita 2): preso à TELA; entra no "Mas" com a fita congelada e sai antes do passo recomeçar.
    # SEM velas até o "três": as 3 nascem juntas (nenhum quadro mostra 2 velas com "TRÊS" na legenda)
    a_b = prog(t, T["mas"], T["mas"] + 0.12) * (1 - prog(t, T["ainda"] + 0.1, T["ainda"] + 0.3))
    sai = e_inout(prog(t, T["ainda"] - 0.12, T["ainda"] + 0.25))
    x_b = X_BOLO + 560 * (1 - e_out(prog(t, T["mas"] + 0.05, T["idade"]))) + 520 * sai
    if a_b > 0:
        velas = [prog(t, T["tres"] - 0.06 + 0.03 * i, T["tres"] + 0.14 + 0.03 * i) for i in range(3)]
        chamas = [prog(t, T["tres"] + 0.14 + 0.08 * i, T["tres"] + 0.32 + 0.08 * i) for i in range(3)]
        quique = 1.0
        for tq, amp in ((T["idade"], 0.06), (T["importa"], 0.05)):
            k = t - tq
            if k > 0:
                quique += amp * math.sin(k * 22) * math.exp(-k * 7)
        bolo(cv, x_b, gy, a_b, velas, chamas, t, esc=1.55 * quique)

    # bolinha dourada no calcanhar: 1ª câmera lenta e "o tempo todo"
    a_pt = max(prog(t, T["lenta"], T["lenta"] + 0.15) * (1 - prog(t, T["nos"] - 0.25, T["nos"] - 0.02)),
               prog(t, T["tempo"], T["tempo"] + 0.15) * (1 - prog(t, T["fica"] - 0.25, T["fica"] - 0.02)))
    if a_pt > 0:
        hx, hy = na_tela(cam, *perto.calcanhar())
        ponto_ouro(cv, hx, hy, a_pt)

    # "pousa pela PONTA": o pé toca NO "ponta" — anel dourado no toque (sem pegada)
    k = t - F.t_toque
    if 0 <= k < 0.9 and t < T["calcanhar"]:
        bx, by = na_tela(cam, perto.bola()[0] + 12, Y_CHAO)
        rx = lerp(20, 95, e_out(k / 0.9))
        cv.drawOval(skia.Rect(bx - rx, by - rx * 0.2, bx + rx, by + rx * 0.2), paint(OURO, int(255 * (1 - k / 0.9)), "stroke", 5))

    # congelamentos: círculo do comentarista no vão do calcanhar ("calcanhar") e na ponta ("lado")
    for t0, t1, rx, dx in ((T["calcanhar"] + 0.08, T["nos"], 72, 44), (T["lado"] + 0.1, T["panturrilha"], 80, 58)):
        if t0 <= t < t1:                                         # estreito: só o vão sob o calcanhar, nada do outro pé
            hx, hy = na_tela(cam, *perto.calcanhar())            # (sai junto com o selo: é marcação da câmera lenta)
            ry = (gy - hy) / 2 + 30
            circulo_mao(cv, hx + dx, (hy + gy) / 2, rx, ry, prog(t, t0, t0 + 0.35), 1 - prog(t, t1 - 0.25, t1 - 0.02))

    # "desce": a seta tenta descer e volta (o calcanhar não desce)
    a_s = prog(t, T["desce"] - 0.05, T["desce"] + 0.1) * (1 - prog(t, T["nos"] - 0.25, T["nos"] - 0.02))
    if a_s > 0:
        hx, hy = na_tela(cam, *perto.calcanhar())
        k = t - T["desce"]
        ida = e_out(clamp(k / 0.25)); volta = 0.35 * sstep((k - 0.25) / 0.25)
        y1 = hy + 20 + (gy - hy - 34) * (ida - volta) * 0.92
        pt = paint("#FFFFFF", int(255 * a_s), "stroke", 6); pt.setPathEffect(skia.DashPathEffect.Make([16, 10], -t * 40))
        cv.drawLine(hx, hy + 20, hx, y1, pt)
        ponta_seta(cv, hx, y1 + 6, math.pi / 2, 22, "#FFFFFF", a_s)

    # "avaliação" (fita 2): selo calmo com o estetoscópio, longe do pé
    a_e = prog(t, T["avaliacao"], T["avaliacao"] + 0.2) * (1 - prog(t, T["fica"] - 0.05, T["fica"] + 0.15))
    if a_e > 0:
        estetoscopio(cv, 880, 500, 1.35 * e_back(prog(t, T["avaliacao"], T["avaliacao"] + 0.3)), a_e)

    # calendário (demorou pra andar): só entra com a câmera já parada; as folhas param quando o passo recomeça
    t_cal = T["demorou"] + 0.3
    a_c = prog(t, t_cal, t_cal + 0.15) * (1 - prog(t, T["andar"] + 0.45, T["andar"] + 0.75))
    calendario(cv, 640, 520, t, t_cal, a_c, esc=2.9, t_para=T["andar"])

    # efeitos de replay
    varredura(cv, t, lento_k(t, T), limpo)
    if not limpo:
        faixas_tracking(cv, t, {"volta": 1.0, "avanca": 0.7}.get(tipo, 0.0))
        if tipo in ("volta", "avanca"):                           # ◀◀ / ▶▶ grande no canto, letreiro do videocassete
            t0 = F.inicio_trecho(t)
            _setas(cv, 96, 410, (0.55 + 0.45 * (math.sin((t - t0) * 16) > -0.3)) * prog(t, t0, t0 + 0.06), 2.2, tipo == "avanca")
        for t0, fo in ((T["calcanhar"], 1.0), (T["vale"], 0.8), (T["lado"], 0.8), (T["esses"], 0.45)):
            flash(cv, t, t0, fo)
        corte_fita(cv, t, T["mas"]); corte_fita(cv, t, T["fica"])
    cv.restore()
    return cam, gy, x_b


# ------------------------------------------------------------------ "melhores momentos" (esses sinais pedem atenção)
def momentos(T):
    """Os congelamentos dos 3 sinais, na ordem da fala: um lado só, panturrilha durinha, demorou pra andar."""
    return ((T["esses"], T["lado"] + 0.5), (T["sinais"], T["durinha"] + 0.5), (T["pedem"], T["andar"] - 0.03))


def miniatura(T, F, tt):
    """O congelamento do instante `tt`, já desenhado (sem texto: o painel e o karaokê ficam fora do monitor)."""
    chave = ("mini", round(tt, 3))
    if chave not in _CACHE:
        sf = skia.Surface(int(CENA.width()), int(CENA.height())); c = sf.getCanvas(); c.clear(_c(BG_OUT))
        c.translate(-CENA.left(), -CENA.top())
        fundo_cl(c, tt)
        monitor(c, tt, T, F, limpo=True)
        _CACHE[chave] = sf.makeImageSnapshot()
    return _CACHE[chave]


MW, MH = 292, 263                                                # miniatura (proporção da CENA)


def melhores_momentos(cv, t, T, F):
    """Sem texto: a cena escurece e as 3 miniaturas entram uma por batida; o estetoscópio vem no "atenção"."""
    if t < T["esses"] - 0.05:
        return
    fim = 1 - prog(t, T["manda"] - 0.4, T["manda"] - 0.1)
    if fim <= 0:
        return
    cv.save(); cv.clipRect(CENA, True)
    img = _img("escurece", CENA.width(), CENA.height(), lambda c: c.clear(_c(BG_OUT, 255)))
    _blit(cv, img, CENA.left(), CENA.top(), 0.72 * prog(t, T["esses"] - 0.05, T["esses"] + 0.25) * fim)
    for i, (ti, tt) in enumerate(momentos(T)):
        if t < ti:
            continue
        k = prog(t, ti, ti + 0.32)
        esc = max(0.01, e_back(k))
        a = prog(t, ti, ti + 0.06) * fim
        cx, cy, giro = 540 + (i - 1) * 322, 850 + (1 - e_out(k)) * 50, (-4.0, 2.5, -2.5)[i]
        cv.save(); cv.translate(cx, cy); cv.rotate(giro * e_out(k)); cv.scale(esc, esc)
        borda = skia.RRect.MakeRectXY(skia.Rect(-MW / 2 - 9, -MH / 2 - 9, MW / 2 + 9, MH / 2 + 9), 14, 14)
        sombra = skia.RRect.MakeRectXY(skia.Rect(-MW / 2 - 3, -MH / 2 + 1, MW / 2 + 15, MH / 2 + 19), 14, 14)
        cv.drawRRect(sombra, paint("#000000", int(110 * a), blur=12))
        cv.drawRRect(borda, paint("#F4F7FA", int(255 * a)))
        dentro = skia.RRect.MakeRectXY(skia.Rect(-MW / 2, -MH / 2, MW / 2, MH / 2), 8, 8)
        cv.save(); cv.clipRRect(dentro, True)
        cv.drawImageRect(miniatura(T, F, tt), skia.Rect(-MW / 2, -MH / 2, MW / 2, MH / 2),
                         skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kNone), _alfa(a))
        cv.restore()
        brilho = 1 - prog(t, ti + 0.1, ti + 0.6)                  # contorno dourado na entrada
        if brilho > 0:
            cv.drawRRect(borda, paint(OURO, int(255 * a * brilho), "stroke", 6))
        cv.restore()
    a_e = prog(t, T["atencao"], T["atencao"] + 0.2) * fim
    if a_e > 0:
        estetoscopio(cv, 540, 560, 1.45 * e_back(prog(t, T["atencao"], T["atencao"] + 0.3)), a_e)
    cv.restore()


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep, F):
    fundo_cl(cv, t)
    cam, gy, x_b = monitor(cv, t, T, F)
    melhores_momentos(cv, t, T, F)

    fim = 1 - prog(t, T["manda"] - 0.4, T["manda"] - 0.1)
    cantoneiras(cv, fim)
    painel(cv, t, T, F, fim)

    # 3 ANOS: o carimbo responde ao gancho (acima do bolo, sai com ele)
    carimbo_ouro(cv, "3 ANOS", x_b, gy - 330, -7, T["anos2"], t, dur=T["ainda"] - T["anos2"] + 0.3)

    # gancho (sai na volta da fita) e selo da série: o selo SÓ EXISTE enquanto a câmera lenta está ligada
    # (lento_k): entra com um pop quando a fita desacelera e some antes de ela voltar a 1× ou avançar
    capa(cv, t, T["volta"], ep["gancho"][0], ep["gancho"][1])
    selo_lenta(cv, lento_k(t, T) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface(cv, t, T, blocos, DESTAQUE)


def selo_lenta(cv, lk):
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


# ------------------------------------------------------------------ som (mix próprio: som.py fica intacto)
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
    """Fita correndo: cliques que aceleram + tom que desliza de f0 a f1 + chiado (sintetizado aqui)."""
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
    """Fita voltando: cliques acelerando + chiado que desce."""
    return _fita(dur, 1960, 260, 0.085, 0.82, 77)


def avancar(dur):
    """Fita avançando: cliques rápidos + tom que sobe."""
    return _fita(dur, 380, 1500, 0.07, 0.9, 78) * 0.85


def chiado(dur=0.26):
    """Corte de fita: estalo + chiado branco curto."""
    SR = som.SR
    n = int(dur * SR); t = np.arange(n) / SR
    rui = som._noise(n, 79); rui = rui - np.convolve(rui, np.ones(4) / 4, "same")
    env = np.clip(t / 0.005, 0, 1) * np.clip((dur - t) / 0.12, 0, 1)
    y = rui * env * 0.55
    c = som.click(); y[:len(c)] += c[:n] * 1.4
    return y


def boing():
    """O elástico puxando de volta: 'tuóim' curto, com vibrato que morre."""
    SR = som.SR
    n = int(0.55 * SR); t = np.arange(n) / SR
    f = 150 + 90 * np.exp(-t * 9) + 14 * np.sin(2 * np.pi * 16 * t) * np.exp(-t * 5)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * som._env(n, 0.004, 0.38) * 0.6
    y += np.sin(2 * np.pi * np.cumsum(2 * f) / SR) * som._env(n, 0.004, 0.2) * 0.15
    return y


def congelar():
    """Tique seco + 'clac' grave curto (o quadro trava)."""
    SR = som.SR
    y = som.tick() * 1.0
    n = int(0.12 * SR); t = np.arange(n) / SR
    z = np.sin(2 * np.pi * np.cumsum(220 * np.exp(-t * 30) + 90) / SR) * som._env(n, 0.001, 0.03) * 0.5
    out = np.zeros(max(len(y), n)); out[:len(y)] += y; out[:n] += z
    return out


def janelas(T, F, dur):
    """Ganho da batida e da harmonia ao longo do tempo: a batida some na câmera lenta."""
    xs = np.arange(0, dur + 0.01, 0.01)
    gb = np.ones_like(xs); gh = np.ones_like(xs)
    for i, x in enumerate(xs):
        tp = F.tipo(x)
        gb[i] = {"play": 1.0, "lenta": 0.0, "congela": 0.45, "volta": 0.2, "avanca": 0.8}[tp]
        gh[i] = {"play": 1.0, "lenta": 0.8, "congela": 0.9, "volta": 0.55, "avanca": 0.8}[tp]
    k = np.ones(15) / 15                                          # transição de ~0,15 s
    gb = np.convolve(np.pad(gb, 7, mode="edge"), k, "valid"); gh = np.convolve(np.pad(gh, 7, mode="edge"), k, "valid")
    return xs, gb, gh


def _media_movel(x, w):
    """= np.convolve(x, np.ones(w) / w, "same"), por soma acumulada (a convolução direta de som.mixar
    leva minutos com janela de 12 mil amostras)."""
    n = len(x); off = (w - 1) // 2
    S = np.concatenate([[0.0], np.cumsum(x, dtype=np.float64)])
    i = np.arange(n)
    return (S[np.clip(i + off + 1, 0, n)] - S[np.clip(i + off - w + 1, 0, n)]) / w


def mixar_cl(voz, dur, eventos, T, F, ganho_trilha=0.40):
    """Mesmo mix e ducking do som.mixar, com a trilha em duas partes e efeitos próprios."""
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
    """Instantes (vídeo) em que cada pé pousa, só nos trechos em que o filme anda para a frente."""
    out = []
    ant = None
    x = 0.0
    anda = ("play", "lenta", "avanca")
    while x < T["total"]:
        tipo = F.tipo(x); tf = F.tf(x)
        if ant is not None and tipo in anda and ant[0] in anda and 0 < tf - ant[1] < 0.2:
            for s0, g in ((0.0, 1.0), (0.5, 0.7)):
                if math.floor(tf - s0) > math.floor(ant[1] - s0):
                    nome, ganho = {"lenta": ("tick", 0.6), "avanca": ("click", 0.22)}.get(tipo, ("click", 0.5))
                    out.append((x, nome, g * ganho))
        ant = (tipo, tf)
        x += 1 / 240
    return out


def sons(T, F):
    ev = [(t, nome, g) for t, nome, g in pisadas(T, F) if t < T["manda"] - 0.2]
    ev += [(T["volta"], lambda: rebobinar(T["camera"] - T["volta"]), 0.9),
           (T["camera"], "pop", 0.55), (T["lenta"] + 0.05, "shimmer", 0.32),
           (F.t_toque, "tick", 0.5), (F.t_toque + 0.04, "shimmer", 0.24),          # a luz acende no vão
           (T["calcanhar"], congelar, 1.0), (T["calcanhar"] + 0.02, "whoosh", 0.3),
           (T["desce"] + 0.2, "thump", 0.35),
           (T["nos"], lambda: avancar(T["sozinho"] - T["nos"]), 0.75),
           (T["sozinho"], "pop", 0.5), (T["sozinho"] + 0.03, "shimmer", 0.3),
           (T["mas"] - 0.02, chiado, 0.7), (T["mas"] + 0.06, "whoosh", 0.45),
           (T["idade"], "pop", 0.55), (T["importa"], "pop", 0.4)]
    ev += [(T["tres"] - 0.06 + 0.03 * i, "pop", 0.45) for i in range(3)]
    ev += [(T["tres"] + 0.14 + 0.08 * i, "pop", 0.3) for i in range(3)]
    ev += [(T["anos2"], "thump", 0.9), (T["ainda"] - 0.1, "whoosh", 0.45), (T["ainda"] + 0.05, "pop", 0.4),
           (T["tempo"], lambda: avancar(T["vale"] - T["tempo"]), 0.75),
           (T["vale"], congelar, 0.85), (T["avaliacao"] + 0.02, "ding", 0.45),
           (T["fica"] - 0.02, chiado, 0.7), (T["tambem"], "pop", 0.5), (T["tambem"] + 0.05, "shimmer", 0.3),
           (T["lado"], congelar, 0.85), (T["lado"] + 0.04, "shimmer", 0.22), (T["panturrilha"] + 0.1, "pop", 0.45), (T["panturrilha"] + 0.35, "pop", 0.4),
           (T["durinha"], "whoosh", 0.3), (T["durinha"] + SEGURA, boing, 0.75)]
    t_cal = T["demorou"] + 0.3
    ev += [(t_cal + 0.1 * i, "tick", 0.24) for i in range(max(1, int((T["andar"] - t_cal) / 0.1)))]
    ev += [(T["andar"], "pop", 0.45)]
    ev += [(ti, "tick", 0.55) for ti, _ in momentos(T)] + [(ti + 0.02, "pop", 0.35) for ti, _ in momentos(T)]
    ev += [(T["atencao"] + 0.02, "ding", 0.4), (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def tempos_previa(T, F):
    return (0.0, 0.55, T["volta"] + 0.3, T["camera"] + 0.15, T["camera"] + 0.5, T["lenta"] + 0.4,
            T["pousa"] + 0.1, F.t_toque + 0.1, T["calcanhar"] + 0.5, T["desce"] + 0.35, T["nos"] + 0.4,
            T["comum"] + 0.2, T["passar"] + 0.15, T["sozinho"] + 0.4, T["mas"] + 0.1, T["mas"] + 0.35,
            T["idade"] + 0.3, T["depois"] + 0.3, T["anos2"] + 0.35, T["ainda"] - 0.05, T["ainda"] + 0.2,
            T["ponta2"] + 0.1, T["todo"] + 0.2, T["vale"] + 0.3, T["avaliacao"] + 0.45, T["fica"] + 0.05,
            T["fica"] + 0.4, T["tambem"] + 0.3, T["lado"] + 0.45, T["panturrilha"] + 0.6,
            T["durinha"] + 0.15, T["durinha"] + 0.45, T["durinha"] + 0.7, T["demorou"] + 0.05, T["demorou"] + 0.15,
            T["demorou"] + 0.25, T["demorou"] + 0.45, T["andar"] + 0.3, T["esses"] + 0.2, T["sinais"] + 0.4,
            T["pedem"] + 0.4, T["atencao"] + 0.5, T["manda"] - 0.6, T["manda"] + 1.2, T["total"] - 1 / 30)


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
