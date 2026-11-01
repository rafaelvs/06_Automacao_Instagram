# -*- coding: utf-8 -*-
"""CÂMERA LENTA (série) — episódio "TRONCO À FRENTE: / OLHA AS COSTAS." (escoliose, pediatria). Versão 2 (31/10),
corrigida pelo leitor às cegas e pelo revisor da v1.

Mesma mecânica do piloto cf_cameralenta_ponta_pes: um REPLAY de TV. Um alongamento da educação física passa em 1×
(rápido e borrado), a fita VOLTA ("De novo"), o lance é revisto em CÂMERA LENTA e CONGELA no detalhe. O tempo do
filme (`Filme.tf`) é separado do tempo do vídeo: a criança é desenhada em função do tempo do filme; a narração nunca
para nem desacelera.

O filme (uma tomada só, quadra de escola, criança SEMPRE de costas):
  * quadro 0: de pé, braços esticados para cima (alongamento) — já em movimento; no "frente", uma 1ª flexão rápida
    só até a metade (aquecimento, `AQUEC`), volta de pé com os braços para cima e, no "por trás", a flexão
    completa (pés juntos, joelhos esticados, braços balançando até os tênis) — a POSIÇÃO do teste do acervo
    (esc_teste_adams). A flexão chega ao fundo SEM parar (balanço): no 1× o fundo cai dentro do borrão, ~1 quadro
    antes de a fita voltar, e a câmera lenta só revê filme que o 1× JÁ passou.
  * depois: sobe; alongamento calmo com os braços para cima; abaixa; fica de pé, parada.
Cada manipulação do tempo tem um sentido:
  1. 1× (0 s até o "De"): ação contínua desde o quadro 0 (braços, 1ª flexão no "frente", flexão completa no "por
     trás"), tudo borrado (média de 6 poses + desfoque vertical): não dá para ver qual lado sobe.
  2. ◀◀ ("De novo") até o tronco a ~1/4 da descida; 0,25× ("câmera"): a lenta começa com o tronco JÁ descendo e os
     braços ainda vindo; dois pontos dourados grudam no alto das costas ("lenta") e deixam trilha; o lado
     direito sobe à vista. O "0,25×" grande entra AO LADO (longe da cabeça) e voa para o painel.
  3. CONGELA na flexão completa ("lado", ~5,9 s): flash, tique, zoom seco 1,5× (e um empurrão lento até 1,6×);
     tracejada branca no alto do lado esquerdo; no "alto", traço dourado no lado alto, círculo, marcador de
     desnível e carimbo UM LADO MAIS ALTO (os pontos e as trilhas somem: já cumpriram a função); no "girando",
     tudo baixa para ~25% e um ANEL dourado dá 3/4 de volta EM TORNO do tronco, por fora (a parte de baixo passa
     por trás do quadril): a coluna "girando" é o que levanta um lado.
  4. 1× calmo e NÍTIDO ("Costuma"): ela sobe e alonga os braços, sem sinal de dor; COSTUMA NÃO DOER em branco ACIMA
     do monitor (sem selo nessa hora); no "visual", um olho pisca.
  5. "Olha também": a câmera vai aos ombros e CONGELA no "ombro" (flash + tique, sem 2ª câmera lenta: não havia o
     que revelar). Ombro: tracejada branca na altura do ombro ESQUERDO; no "alto", traço dourado no contorno do
     ombro direito, que passa acima da linha, e o marcador de desnível. "Cintura": a câmera desce; os vãos
     braço-cintura em dourado forte — o esquerdo ~3× o direito —, pulsando no "torta". "Escápula": a câmera sobe
     às DUAS escápulas (2,3×): a direita faz relevo no tecido (luz e sombra macias, placa achatada com a borda de
     dentro e o ângulo de baixo), a esquerda fica plana; um círculo pequeno só na direita. Sem lupa.
  6. "sinal" (3ª): recapitulação no padrão do piloto — 4 polaroides sem texto, carimbo SINAL (depois que a cena
     escurece), NÃO DIAGNÓSTICO em branco (calmo) e o estetoscópio no "leve" ("com o ortopedista"). A cena ao vivo
     atrás vira FUNDO (92% escura e desfocada): a criança de pé não fica legível sob os elementos.
  7. ▶▶ ("estirão"): o recap some em 0,15 s; calendário de folhas (sem número, cabeçalho azul-claro), carimbo NO
     ESTIRÃO (sozinho), e no "rápido" um ponto dourado pulsa no alto da metade direita das costas. Nada cresce.
  8. Replay limpo a 0,25× (respiro antes da CTA): os últimos graus da flexão; as trilhas começam no trecho revisto
     e terminam em alturas diferentes. Depois, a CTA do cf_comum (atrás do véu, desfocada e mais escura, ela
     segue em 1×: sobe e fica de pé com os braços ao lado do corpo, sem passar do título).

Regras do storyboard e do verificador, todas aqui:
  * Assimetria SEMPRE do lado DIREITO da criança (de costas = direita da tela): na flexão, a metade direita do alto
    das costas sobe até ~36 px (amplitude = dobra²); em pé: ombro direito ~14 px mais alto, escápula direita com
    relevo no tecido, vão braço-cintura maior do lado ESQUERDO (o tronco um pouco para a direita).
  * Sem coluna, vértebras, raio-X, transparência; nada por dentro do corpo (o relevo da escápula é só luz e sombra
    na camiseta, sem contorno de osso). Sem mochila, nível, régua, marca de altura nem instrumento. Camiseta JUSTA
    azul-clara que nunca sobe (a barra fica sempre por baixo do cós do short); pele só em braços e pernas; rosto
    nunca aparece (só a nuca/coque).
  * Vermelho PROIBIDO no episódio inteiro (inclusive no calendário). Dourado só nos achados.
  * Nada de ❚❚, barra de progresso, "PAUSA", timecode ou dígitos (cronômetro sem números): congelar = flash + tique
    + zoom + marcação. Nenhum texto além do `tela` (CÂMERA LENTA, 1×, 0,25×, UM LADO MAIS ALTO, COSTUMA NÃO DOER,
    SINAL, NÃO DIAGNÓSTICO, NO ESTIRÃO), do gancho e da interface. Sem loop prometido.
  * O selo CÂMERA LENTA e a moldura âmbar só EXISTEM com a lentidão ligada (a 1ª câmera lenta + o congelamento que
    a fecha, e o replay final), como no piloto polido de 26/10.

Helpers COPIADOS (não importados) do piloto cf_cameralenta_ponta_pes: _trim, sstep, _img/_blit, fundo_cl,
monitor (vinheta), varredura, faixas_tracking, cantoneiras, flash, relogio (orig. cf_andador), chip_dim,
chip_c, _setas, painel (adaptado), circulo_mao, ponta_seta, estetoscopio, calendario (orig. cf_fratura_cola,
cabeçalho azul-claro, velocidade variável), desenha_trilha, ponto_ouro, selo_lenta, trilha_partes, _fita,
rebobinar, avancar, congelar, janelas, _media_movel, mixar_cl. Do cf_escoliose: o olho (adaptado: contorno
dourado, olho branco) e a ideia do alto das costas como UM arco de camiseta com o lado de fora subindo.
Importados sem cópia: capa/interface/ancoras (cf_comum), carimbo_ouro, comprimir, alinhar, montar_blocos
(cf_fratura_cola), paleta e texto (cf_alongamento).
A cena é PRESA ao roteiro pelas palavras-âncora (ANCORAS): roteiro sem elas = KeyError no render.
"""
import math
import os

import numpy as np
import skia

from . import som, voz as _voz
from .base import FPS, codificar, previas as _previas
from .cf_alongamento import (BG_OUT, CX, F_BLACK, F_SEMI, H, OURO, PART, W, clamp, e_back, e_inout, e_out, lerp,
                             paint, prog, texto)
from .cf_comum import ancoras, capa, interface
from .cf_fratura_cola import alinhar, carimbo_ouro, comprimir, montar_blocos

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "tronco": ("tronco", 1, False), "frente": ("frente", 1, False), "olha": ("olha", 1, False),
    "costas": ("costas", 1, False), "por": ("por", 1, False), "tras": ("trás", 1, False), "de": ("de", 1, False),
    "novo": ("novo", 1, False), "camera": ("câmera", 1, False), "lenta": ("lenta", 1, False),
    "repara": ("repara", 1, False), "lado": ("lado", 1, False), "alto1": ("alto", 1, False),
    "coluna": ("coluna", 1, False), "girando": ("girando", 1, False), "sinal1": ("sinal", 1, False),
    "escoliose": ("escoliose", 1, False), "costuma": ("costuma", 1, False), "doer": ("doer", 1, False),
    "comeco": ("começo", 1, False), "visual": ("visual", 1, False), "olha2": ("olha", 2, False),
    "ombro": ("ombro", 1, False), "alto2": ("alto", 2, False), "cintura": ("cintura", 1, False),
    "torta": ("torta", 1, False), "escapula": ("escápula", 1, False), "saliente": ("saliente", 1, False),
    "sinal3": ("sinal", 3, False), "nao2": ("não", 2, False), "diagnostico": ("diagnóstico", 1, False),
    "leve": ("leve", 1, False), "avaliacao": ("avaliação", 1, False), "ortopedista": ("ortopedista", 1, False),
    "estirao": ("estirão", 1, False), "curva": ("curva", 1, False), "rapido": ("rápido", 1, False),
    "manda": ("manda", 1, False),
}
DESTAQUE = {"frente", "costas", "lado", "alto", "girando", "escoliose", "doer", "visual", "ombro", "cintura",
            "torta", "escápula", "saliente", "diagnóstico", "ortopedista", "estirão", "rápido"}
RESPIRO_CTA = 1.6
R_SELO, R_1X, R_LENTA = "CÂMERA LENTA", "1×", "0,25×"                 # todos em ep["tela"]
R_ALTO, R_SINAL, R_NAO, R_ESTIRAO = "UM LADO MAIS ALTO", "SINAL", "NÃO DIAGNÓSTICO", "NO ESTIRÃO"
R_DOER = "COSTUMA NÃO DOER"

# ------------------------------------------------------------------ paleta (sem vermelho)
PELE, PELE_CL, PELE_ESC, PELE_LINHA = "#F0B49A", "#F7CDB8", "#DA987E", "#B9765E"
CABELO, CABELO_CL, ELASTICO = "#3B2A20", "#5A4232", "#2B4C7E"
CAM, CAM_CL, CAM_ESC, CAM_LINHA = "#9CC9FF", "#D3E8FF", "#6E9DD6", "#3E6EA6"       # camiseta azul-clara, justa
SHORT, SHORT_CL, SHORT_LINHA, LISTRA = "#1E3560", "#2D4B82", "#0E1C36", "#F4F7FA"   # azul-marinho, listra branca
MEIA, MEIA_SOMBRA = "#F6F8FA", "#C3CDD8"
TENIS, TENIS_SOLA, TENIS_DET = "#E2E8EE", "#3A4450", "#2B4C7E"
PAREDE, PAREDE_CL, RODAPE = "#3A566D", "#46647D", "#1C2833"
PISO, PISO_B, PISO_JUNTA, LINHA_QUADRA = "#D9BC8C", "#CFB07E", "#A9895A", "#F7F3EA"
FUNDO_CARTAO = "#0B1824"
AMBAR = "#FFB547"
AZUL_CL = "#9CC9FF"

# ------------------------------------------------------------------ o "monitor" de replay (tela)
CENA = skia.Rect(40, 330, 1040, 1230)                            # o mundo é recortado aqui (selo e karaokê livres)
Y_SOLA = 1080.0                                                  # sola do tênis (mundo = tela na câmera BASE)
XC = 540.0

# ------------------------------------------------------------------ o filme (segundos de FILME)
B = 1.0                                                          # descida até a flexão completa
T_PREP = 0.45                                                    # preparo (cabeça baixa) antes da descida
R_SOBE = 0.9                                                     # subida
F_BR = (2.5, 3.2, 3.8, 4.4)                                      # braços sobem, ficam, descem (alongamento calmo)
F_IDLE = 4.8                                                     # de pé, parada (o congelamento do "ombro" cai depois)
V1 = 1.25                                                        # "1×"
VL = 0.25 * V1                                                   # "0,25×"
VR = 4.0 * V1                                                    # avanço rápido
BUMP = 36.0                                                      # o lado direito das costas sobe até ~36 px
OMBRO_DIF = 14.0                                                 # de pé: ombro direito ~14 px mais alto
# aquecimento do 1× (filme ANTES da flexão revista): braços para cima e uma 1ª flexão rápida, só até a metade,
# no "frente". [início, fundo, fim, profundidade] em segundos de FILME; o Filme preenche pelas âncoras.
AQUEC = [-2.6, -1.85, -0.95, 0.62]


def _c(h, a=255):
    h = h.lstrip("#")
    return skia.ColorSetARGB(int(a), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _alfa(a):
    p = skia.Paint()
    p.setAlphaf(clamp(a))
    return p


def _trim(pt, k):
    """Traço desenhado até a fração k. (cópia do piloto)"""
    if k < 0.999:
        pe = skia.TrimPathEffect.Make(0.0, max(0.002, k))
        if pe is not None:
            pt.setPathEffect(pe)
    return pt


def sstep(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def _lp(a, b, k):
    return (lerp(a[0], b[0], k), lerp(a[1], b[1], k))


def _suave(pts, fechar=True):
    """Caminho liso pelos pontos (quadráticas pelos pontos médios)."""
    p = skia.Path()
    n = len(pts)
    if fechar:
        m0 = ((pts[-1][0] + pts[0][0]) / 2, (pts[-1][1] + pts[0][1]) / 2)
        p.moveTo(*m0)
        for i in range(n):
            a = pts[i]; b = pts[(i + 1) % n]
            p.quadTo(a[0], a[1], (a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        p.close()
        return p
    p.moveTo(*pts[0])
    for i in range(1, n - 1):
        p.quadTo(pts[i][0], pts[i][1], (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2)
    p.lineTo(*pts[-1])
    return p


# ------------------------------------------------------------------ o filme: dobra do tronco e braços
def dobra(tf):
    """0 = de pé; 1 = flexão completa. A descida acelera e chega ao fundo SEM parar; a subida sai com a mesma
    velocidade (balanço de alongamento): o fundo nunca fica parado no 1×."""
    if tf <= 0:
        s, pk, fim, prof = AQUEC                                 # 1ª flexão do aquecimento (só no 1× borrado)
        if s < tf < pk:
            u = (tf - s) / (pk - s)
            return prof * (0.3 * sstep(u) + 0.7 * u ** 1.5)      # desce acelerando e não para no fundo
        if pk <= tf < fim:
            v = (tf - pk) / (fim - pk)
            return prof * (1 - v) ** 1.35                        # sobe e assenta de pé
        return 0.0
    if tf < B:
        u = tf / B
        return 0.25 * sstep(u) + 0.75 * u ** 1.6
    if tf < B + R_SOBE:
        v = (tf - B) / R_SOBE
        m0 = 0.75 * 1.6 * R_SOBE / B
        f = (v ** 3 - 2 * v * v + v) * m0 + (-2 * v ** 3 + 3 * v * v)
        return clamp(1.0 - f)
    return 0.0


def preparo(tf):
    """Antes de descer, ela abaixa a cabeça e arredonda os ombros (o alongamento começa no "sinal");
    na subida o preparo se desfaz."""
    if tf <= B:
        return sstep((tf + T_PREP) / T_PREP)
    if tf < B + R_SOBE:
        return 1 - sstep((tf - B) / R_SOBE)
    return 0.0


def bracos(tf):
    """0 = braços ao lado do corpo; 1 = esticados para cima. Antes do fundo da flexão os braços estão para cima
    (aquecimento): ao descer, eles balançam até os tênis; depois de subir, o alongamento calmo do "não doer"."""
    if tf < B:
        return 1.0
    return e_inout(prog(tf, F_BR[0], F_BR[1])) * (1 - e_inout(prog(tf, F_BR[2], F_BR[3])))


class Pose:
    __slots__ = ("d", "up", "sway", "br", "pr")

    def __init__(self, tf):
        self.d = dobra(tf)
        self.up = bracos(tf)
        self.pr = preparo(tf)
        q = 1 - self.d
        self.sway = 2.2 * math.sin(2 * math.pi * tf / 2.6) * q            # balanço sutil de quem está de pé
        self.br = math.sin(2 * math.pi * tf / 3.3) * q                    # respiração


def pose_t(t, F):
    """A pose do instante de VÍDEO t. No cartão final (a partir de F.t_cta) ela sobe da flexão e fica de pé com
    os braços AO LADO do corpo: o alongamento com os braços para cima (F_BR) punha antebraços e mãos inteiros
    acima do título da CTA, com a cabeça e o tronco atrás das letras (2ª rodada, 28,4–29,1 s: "dois braços saindo
    do texto"). O tempo do filme e o som não mudam; só os braços deixam de subir atrás do título."""
    p = Pose(F.tf(t))
    if t >= F.t_cta:
        p.up = 0.0
    return p


# ------------------------------------------------------------------ geometria da criança (vista de COSTAS)
# u em [-1, 1] atravessa os ombros: -1 = lado ESQUERDO da criança (esquerda da tela), +1 = DIREITO.
def _meia(e):
    return lerp(90.0, 128.0, e)


def x_u(u, p):
    e = p.d
    return XC + p.sway + _meia(e) * u


def bump(u, e):
    """O lado DIREITO do alto das costas sobe na flexão (amplitude = dobra²)."""
    return BUMP * e * e * math.exp(-((u - 0.38) / 0.42) ** 2)


def topo(u, p):
    """Contorno de cima do tronco: de pé = ombros e nuca; na flexão = UM arco de camiseta (a cúpula)."""
    e = p.d
    au = abs(u)
    y0 = 588 + 10 * sstep((au - 0.22) / 0.55) + 18 * sstep((au - 0.80) / 0.20)
    if u > 0:
        y0 -= OMBRO_DIF * sstep((u - 0.15) / 0.55)               # ombro direito ~14 px mais alto (discreto no 1×)
    y0 -= 1.5 * p.br
    y0 += 5 * p.pr * (1 - au)                                    # preparo: os ombros arredondam
    y1 = 696 + 46 * u ** 4
    return lerp(y0, y1, e) - bump(u, e)


# laterais do tronco (de baixo para a axila): de pé / flexão. De pé, a cintura ESQUERDA é mais funda e o
# tronco fica um pouco para a direita: o vão braço-cintura do lado esquerdo fica ~3× o do direito.
LAT_E0 = ((477, 806), (485, 752), (459, 694), (447, 648))
LAT_E1 = ((460, 864), (446, 832), (418, 800), (404, 768))
LAT_D0 = ((619, 806), (625, 752), (634, 694), (633, 636))
LAT_D1 = ((620, 864), (634, 832), (662, 800), (676, 768))
U_PONTO = 0.42                                                   # onde os pontos dourados grudam (sobre as escápulas)


def _lat(k0, k1, p):
    e = p.d
    return [(lerp(a[0], b[0], e) + p.sway * (1 - e), lerp(a[1], b[1], e) - 1.2 * p.br * (1 - e)) for a, b in zip(k0, k1)]


def tronco_path(p):
    pts = list(_lat(LAT_E0, LAT_E1, p))
    n = 34
    for i in range(n + 1):
        u = -1 + 2 * i / n
        pts.append((x_u(u, p), topo(u, p)))
    pts += list(reversed(_lat(LAT_D0, LAT_D1, p)))
    return _suave(pts)


def lado_x(p, lado, y):
    """x da lateral do tronco na altura y (interpolação dos pontos-chave)."""
    ks = _lat(LAT_E0, LAT_E1, p) if lado < 0 else _lat(LAT_D0, LAT_D1, p)
    ks = sorted(ks, key=lambda q: q[1])
    if y <= ks[0][1]:
        return ks[0][0]
    for a, b in zip(ks, ks[1:]):
        if a[1] <= y <= b[1]:
            return lerp(a[0], b[0], (y - a[1]) / max(1e-6, b[1] - a[1]))
    return ks[-1][0]


def ponto_costas(p, lado):
    """Ponto dourado grudado na camiseta, sobre a escápula (lado -1 esquerdo, +1 direito)."""
    u = lado * U_PONTO
    return x_u(u, p), topo(u, p) + lerp(54.0, 16.0, p.d)


# braços (ombro, cotovelo, mão): de pé / para cima / na flexão (pendendo em direção aos tênis)
BR_BAIXO = {-1: ((440, 630), (429, 748), (424, 860)), 1: ((640, 616), (649, 738), (652, 850))}
BR_CIMA = {-1: ((442, 626), (416, 510), (436, 402)), 1: ((638, 612), (664, 496), (644, 388))}
BR_FLEX = {-1: ((416, 762), (440, 894), (476, 1022)), 1: ((664, 758), (640, 894), (604, 1022))}
# Os braços NÃO se interpolam por posição (v2 de 31/10): a média de "para cima" com "pendente" punha cotovelo e
# mão em cima do ombro (comprimento ~0) e o braço virava só a manga com um toco de pele (4,40–4,90 s, pose em
# "T" amputada no 11,5 s, fundo da 1ª flexão sem antebraço). Agora cada segmento é (ângulo, comprimento) a
# partir do ombro: o comprimento nunca encolhe, e o braço passa PELO LADO (abdução) ao subir/descer.
E_SOLTA = 0.24              # na descida, os braços já pendem soltos (teste de Adams) quando a dobra passa disto


def _polar(lado, a, b):
    """Segmento a->b como (ângulo a partir de "para baixo", positivo = para FORA do corpo; comprimento)."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    return math.atan2(lado * dx, dy), math.hypot(dx, dy)


def _rig(lado, chave):
    s, c, m = chave[lado]
    f1, l1 = _polar(lado, s, c)
    f2, l2 = _polar(lado, c, m)
    while f2 - f1 > math.pi:                                     # antebraço no mesmo "giro" do braço
        f2 -= 2 * math.pi
    while f2 - f1 < -math.pi:
        f2 += 2 * math.pi
    return s, f1, l1, f2, l2


RIG = {lado: {"B": _rig(lado, BR_BAIXO), "C": _rig(lado, BR_CIMA), "F": _rig(lado, BR_FLEX)} for lado in (-1, 1)}


def braco_geo(p, lado):
    """(ombro, cotovelo, mão). O ombro segue o tronco como antes; braço e antebraço giram com comprimento
    constante. Nos extremos (de pé, braços para cima, flexão completa) dá EXATAMENTE os pontos de BR_*."""
    e = p.d
    rb, rc, rf = RIG[lado]["B"], RIG[lado]["C"], RIG[lado]["F"]
    up = p.up * (1 - sstep(e / E_SOLTA))                         # ao dobrar, os braços descem (pelo lado) e pendem
    s = _lp(_lp(rb[0], rc[0], p.up), rf[0], e)

    def par(i):                                                  # pendente (segue a dobra) -> para cima
        return lerp(lerp(rb[i], rf[i], e), rc[i], up)
    f1, l1, f2, l2 = par(1), par(2), par(3), par(4)
    c = (s[0] + lado * l1 * math.sin(f1), s[1] + l1 * math.cos(f1))
    m = (c[0] + lado * l2 * math.sin(f2), c[1] + l2 * math.cos(f2))
    return [(q[0] + p.sway * (1 - e), q[1] - 1.2 * p.br * (1 - e)) for q in (s, c, m)]


def cabeca_y(p):
    """A cabeça desce junto e some atrás das costas (fica entre os braços)."""
    hd = e_inout(clamp(p.d * 1.35))
    return lerp(512.0 + 16 * p.pr, 808.0, hd) - 1.2 * p.br


# ------------------------------------------------------------------ desenho da criança
def _pele(cv, pth, x0, x1, linha=3.0):
    sh = skia.GradientShader.MakeLinear([skia.Point(x0, 0), skia.Point(x1, 0)],
                                        [_c(PELE_ESC), _c(PELE), _c(PELE_CL), _c(PELE), _c(PELE_ESC)],
                                        [0.0, 0.22, 0.5, 0.78, 1.0])
    cv.drawPath(pth, paint(PELE, 255, shader=sh))
    cv.drawPath(pth, paint(PELE_LINHA, 230, "stroke", linha))


def _uniao(a, b):
    """skia.Op de união que NÃO derruba o render: o PathOps levanta RuntimeError ("Failed to apply op") em
    algumas poses de braço (círculos de articulação quase coincidentes) -> None."""
    if a is None or b is None:
        return None
    try:
        return skia.Op(a, b, skia.PathOp.kUnion_PathOp)
    except RuntimeError:
        return None


def _segmento(x0, y0, x1, y1, r0, r1):
    L = math.hypot(x1 - x0, y1 - y0) or 1.0
    nx, ny = -(y1 - y0) / L, (x1 - x0) / L
    p = skia.Path()
    p.moveTo(x0 + nx * r0, y0 + ny * r0); p.lineTo(x1 + nx * r1, y1 + ny * r1)
    p.lineTo(x1 - nx * r1, y1 - ny * r1); p.lineTo(x0 - nx * r0, y0 - ny * r0); p.close()
    c0 = skia.Path(); c0.addCircle(x0, y0, r0)
    c1 = skia.Path(); c1.addCircle(x1, y1, r1)
    u = _uniao(_uniao(p, c0), c1)
    if u is not None and all(u.contains(x, y) for x, y in ((x0, y0), (x1, y1), ((x0 + x1) / 2, (y0 + y1) / 2))):
        return u
    s = skia.Path(p); s.addPath(c0); s.addPath(c1); s.setFillType(skia.PathFillType.kWinding)   # soma (mesmo preenchimento)
    return s


def braco_path(jx, jy, ex, ey, hx, hy):
    """Contorno único braço + antebraço + mão com UNIÃO CONFERIDA. Braço e antebraço trazem o MESMO círculo do
    cotovelo, e o PathOps do skia pode errar a união e SUMIR um segmento (achado do chat YouTube, kit16): o
    resultado é conferido por pontos de dentro (meio do braço, cotovelo, meio do antebraço, punho, mão) e, se
    falhar (ou se o Op levantar erro), refeito com o círculo do cotovelo um fio menor (invisível).
    -> (path, ok); ok=False = peças soltas (desenhadas com o contorno por baixo e a pele por cima)."""
    L = math.hypot(hx - ex, hy - ey) or 1.0
    ux, uy = (hx - ex) / L, (hy - ey) / L
    mao = skia.Path(); mao.addOval(skia.Rect(-13.5, -6, 13.5, 33))
    m = skia.Matrix(); m.setRotate(math.degrees(math.atan2(uy, ux)) - 90); m.postTranslate(hx, hy)
    mao.transform(m)
    pts = (((jx + ex) / 2, (jy + ey) / 2), (ex, ey), ((ex + hx) / 2, (ey + hy) / 2), (hx, hy),
           (hx + ux * 14, hy + uy * 14))
    for dr in (0.0, 0.4, 0.9, -0.6):
        a = _segmento(jx, jy, ex, ey, 17.0, 14.5 - dr)
        b = _segmento(ex, ey, hx, hy, 14.5, 12.0)
        u = _uniao(_uniao(a, b), mao)
        if u is not None and all(u.contains(x, y) for x, y in pts):
            return u, True
    return [_segmento(jx, jy, ex, ey, 17.0, 14.5), _segmento(ex, ey, hx, hy, 14.5, 12.0), mao], False


def desenha_braco(cv, p, lado):
    (jx, jy), (ex, ey), (hx, hy) = braco_geo(p, lado)
    br, ok = braco_path(jx, jy, ex, ey, hx, hy)
    xs = (jx, ex, hx)
    if ok:
        _pele(cv, br, min(xs) - 18, max(xs) + 18, 2.8)
    else:                                                        # sem união: contorno por baixo, pele por cima
        sh = skia.GradientShader.MakeLinear([skia.Point(min(xs) - 18, 0), skia.Point(max(xs) + 18, 0)],
                                            [_c(PELE_ESC), _c(PELE), _c(PELE_CL), _c(PELE), _c(PELE_ESC)],
                                            [0.0, 0.22, 0.5, 0.78, 1.0])
        for pc in br:
            cv.drawPath(pc, paint(PELE_LINHA, 230, "stroke", 5.6))
        for pc in br:
            cv.drawPath(pc, paint(PELE, 255, shader=sh))
    # cotovelo: dobrinha discreta
    cv.drawCircle(ex, ey, 3.2, paint(PELE_LINHA, 90))
    # manga curta (camiseta): cobre o começo do braço
    Lb = math.hypot(ex - jx, ey - jy) or 1.0
    vx, vy = (ex - jx) / Lb, (ey - jy) / Lb
    nx, ny = -vy, vx
    k = 0.42 * Lb
    mg = skia.Path()
    mg.moveTo(jx + nx * 20 - vx * 8, jy + ny * 20 - vy * 8)
    mg.lineTo(jx + vx * k + nx * 23, jy + vy * k + ny * 23)
    mg.quadTo(jx + vx * (k + 4), jy + vy * (k + 4), jx + vx * k - nx * 23, jy + vy * k - ny * 23)
    mg.lineTo(jx - nx * 20 - vx * 8, jy - ny * 20 - vy * 8)
    mg.quadTo(jx - vx * 26, jy - vy * 26, jx + nx * 20 - vx * 8, jy + ny * 20 - vy * 8)
    mg.close()
    sh = skia.GradientShader.MakeLinear([skia.Point(jx - 24, 0), skia.Point(jx + 24, 0)],
                                        [_c(CAM_ESC), _c(CAM), _c(CAM_ESC)], [0.0, 0.5, 1.0])
    cv.drawPath(mg, paint(CAM, 255, shader=sh))
    cv.drawPath(mg, paint(CAM_LINHA, 220, "stroke", 2.6))
    cv.drawLine(jx + vx * (k - 7) + nx * 19, jy + vy * (k - 7) + ny * 19, jx + vx * (k - 7) - nx * 19,
                jy + vy * (k - 7) - ny * 19, paint(CAM_ESC, 200, "stroke", 3))


def desenha_cabeca(cv, p):
    hx, hy = XC + p.sway * 1.1, cabeca_y(p)
    pesc_y1 = topo(0.0, p) + 14
    if pesc_y1 > hy:
        pc = skia.Path(); pc.addRRect(skia.RRect.MakeRectXY(skia.Rect(hx - 20, hy + 10, hx + 20, pesc_y1), 12, 12))
        _pele(cv, pc, hx - 22, hx + 22, 2.4)
    for s in (-1, 1):                                            # orelhas (atrás do cabelo)
        o = skia.Path(); o.addOval(skia.Rect(hx + s * 49 - 9, hy - 6, hx + s * 49 + 9, hy + 24))
        _pele(cv, o, hx + s * 49 - 10, hx + s * 49 + 10, 2.2)
    cab = skia.Path(); cab.addCircle(hx, hy, 50)
    _pele(cv, cab, hx - 52, hx + 52, 2.6)                        # nuca em pele; o cabelo cobre o resto
    cv.save(); cv.clipPath(cab, skia.ClipOp.kIntersect, True)
    cabelo = skia.Path()
    cabelo.moveTo(hx - 60, hy - 70); cabelo.lineTo(hx + 60, hy - 70); cabelo.lineTo(hx + 60, hy + 26)
    cabelo.cubicTo(hx + 34, hy + 40, hx + 14, hy + 30, hx, hy + 40)
    cabelo.cubicTo(hx - 14, hy + 30, hx - 34, hy + 40, hx - 60, hy + 26); cabelo.close()
    sh = skia.GradientShader.MakeLinear([skia.Point(hx - 50, 0), skia.Point(hx + 50, 0)],
                                        [_c(CABELO), _c(CABELO_CL), _c(CABELO)], [0.0, 0.5, 1.0])
    cv.drawPath(cabelo, paint(CABELO, 255, shader=sh))
    for k in (-26, -10, 8, 24):                                  # fios penteados para o coque
        fio = skia.Path(); fio.moveTo(hx + k * 1.4, hy + 28); fio.quadTo(hx + k * 0.9, hy, hx + k * 0.3, hy - 14)
        cv.drawPath(fio, paint("#2A1D16", 120, "stroke", 2.4))
    cv.restore()
    cv.drawCircle(hx, hy, 50, paint(PELE_LINHA, 120, "stroke", 2.4))
    cv.drawCircle(hx, hy - 16, 22, paint(CABELO))                # coque (cabelo preso)
    cv.drawCircle(hx - 6, hy - 22, 9, paint(CABELO_CL, 160))
    cv.drawCircle(hx, hy - 16, 22, paint("#21160F", 200, "stroke", 2.4))
    el = skia.RRect.MakeRectXY(skia.Rect(hx - 17, hy + 2, hx + 17, hy + 9), 3, 3)
    cv.drawRRect(el, paint(ELASTICO))                            # elástico do coque


def desenha_tronco(cv, p, a_escapula=1.0):
    e = p.d
    pth = tronco_path(p)
    y_top = topo(0.0, p)
    xl, xr = x_u(-1.05, p), x_u(1.05, p)
    cv.drawPath(pth, paint("#000000", 70, blur=10))
    sh_v = skia.GradientShader.MakeLinear([skia.Point(0, y_top - 30), skia.Point(0, y_top + 220)],
                                          [_c(lerpc_(CAM, CAM_CL, 0.6 * e)), _c(CAM), _c(CAM_ESC)], [0.0, 0.5, 1.0])
    cv.drawPath(pth, paint(CAM, 255, shader=sh_v))
    sh_h = skia.GradientShader.MakeLinear([skia.Point(xl, 0), skia.Point(xr, 0)],
                                          [_c("#2F4F7A", 120), _c("#2F4F7A", 0), _c("#2F4F7A", 0), _c("#2F4F7A", 120)],
                                          [0.0, 0.24, 0.76, 1.0])
    cv.drawPath(pth, paint("#000000", 255, shader=sh_h))
    cv.save(); cv.clipPath(pth, skia.ClipOp.kIntersect, True)
    if e > 0.05:                                                 # na flexão: o lado que subiu pega mais luz
        bx, by = x_u(0.38, p), topo(0.38, p)
        cv.drawOval(skia.Rect(bx - 66, by + 4, bx + 58, by + 44), paint("#FFFFFF", int(120 * e * e), blur=14))
    q = 1 - e
    if q > 0.02 and a_escapula > 0:                              # de pé: o relevo das escápulas no tecido
        escapulas(cv, p, q * a_escapula)
    # costura do meio das costas (só de pé, some na flexão): dá leitura de "costas"
    if q > 0.05:
        cv.drawLine(XC + p.sway, y_top + 30, XC + p.sway + 2, y_top + 200, paint(CAM_ESC, int(60 * q), "stroke", 2.4))
    cv.restore()
    cv.drawPath(pth, paint(CAM_LINHA, 235, "stroke", 3.2))
    if q > 0.05:                                                 # gola (só de pé: na flexão fica do outro lado)
        g = skia.Path()
        for i in range(13):
            u = -0.3 + 0.6 * i / 12
            (g.moveTo if i == 0 else g.lineTo)(x_u(u, p), topo(u, p) + 4)
        cv.drawPath(g, paint(CAM_ESC, int(255 * q), "stroke", 7))
        cv.drawPath(g, paint(CAM_LINHA, int(200 * q), "stroke", 2))


def escapula_geo(p, s):
    """Pontos (mundo) da placa da escápula do lado s (+1 direito, -1 esquerdo), vista de costas por cima da
    camiseta: placa achatada e triangular, borda de dentro perto do meio das costas, ângulo de baixo apontando
    para baixo. -> (topo de dentro, topo de fora, ângulo de baixo)."""
    x0, y0 = XC + p.sway, topo(0.0, p)
    return (x0 + s * 22, y0 + 38), (x0 + s * 80, y0 + 30), (x0 + s * 36, y0 + 110)


def escapulas(cv, p, a):
    """Relevo das escápulas NO TECIDO (nada por dentro do corpo): só luz e sombra macias, sem contorno. A placa
    saliente pega luz em cima e faz sombra na borda de dentro e embaixo do ângulo. A DIREITA é a saliente; a
    esquerda fica quase plana (é a comparação)."""
    for s, forca in ((1, 1.0), (-1, 0.12)):
        aa = clamp(a * forca, 0, 2)
        if aa <= 0.01:
            continue
        (mx, my), (lx, ly), (ax, ay) = escapula_geo(p, s)
        placa = skia.Path()
        placa.moveTo(mx, my)
        placa.quadTo((mx + lx) / 2, my - 6, lx, ly)
        placa.quadTo(lx - s * 6, (ly + ay) / 2 + 4, ax, ay)
        placa.quadTo(mx - s * 4, (my + ay) / 2 + 2, mx, my)
        placa.close()
        cv.drawPath(placa, paint(CAM_CL, int(min(255, 85 * aa)), blur=7))              # a placa pega luz
        sombra = skia.Path()                                                           # sombra macia: borda de dentro
        sombra.moveTo(mx - s * 4, my + 2)
        sombra.quadTo(mx - s * 9, (my + ay) / 2 + 4, ax - s * 4, ay + 2)
        sombra.quadTo(ax + s * 14, ay + 12, ax + s * 30, ay - 10)                       # e embaixo do ângulo
        cv.drawPath(sombra, paint(CAM_ESC, int(min(255, 70 * aa)), "stroke", 12, blur=7))
        cv.drawPath(sombra, paint(CAM_LINHA, int(min(255, 55 * aa)), "stroke", 3, blur=2.5))


def lerpc_(c1, c2, x):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{int(lerp(a[i], b[i], clamp(x))):02X}" for i in range(3))


def desenha_pernas(cv, p):
    e = p.d
    sx = p.sway * (1 - e) * 0.4
    for s, c in ((-1, 513.0), (1, 567.0)):
        c += sx
        o = -s                                                   # lado de fora
        pt = skia.Path()
        pt.moveTo(c + o * 28, 846)
        pt.cubicTo(c + o * 30, 900, c + o * 22, 945, c + o * 23, 968)
        pt.cubicTo(c + o * 25, 992, c + o * 18, 1020, c + o * 15, 1040)
        pt.lineTo(c - o * 13, 1040)
        pt.cubicTo(c - o * 14, 1010, c - o * 15, 990, c - o * 19, 968)
        pt.cubicTo(c - o * 24, 940, c - o * 27, 900, c - o * 27, 846)
        pt.close()
        _pele(cv, pt, c - 30, c + 30, 2.8)
        cv.drawArc(skia.Rect(c - 13, 958, c + 13, 974), 200, 140, False, paint(PELE_LINHA, 130, "stroke", 2.6))
        # meia branca
        m = skia.Path()
        m.moveTo(c - 17, 1012); m.lineTo(c + 17, 1012); m.lineTo(c + 19, 1050); m.lineTo(c - 19, 1050); m.close()
        cv.drawPath(m, paint(MEIA))
        cv.drawLine(c - 17, 1020, c + 17, 1020, paint(MEIA_SOMBRA, 220, "stroke", 3))
        cv.drawPath(m, paint(MEIA_SOMBRA, 230, "stroke", 2.2))
        # tênis visto por trás: contraforte do calcanhar, sola escura, puxador azul
        tn = skia.Path()
        tn.moveTo(c - 25, Y_SOLA)
        tn.cubicTo(c - 28, 1062, c - 24, 1046, c - 12, 1041)
        tn.quadTo(c, 1038, c + 12, 1041)
        tn.cubicTo(c + 24, 1046, c + 28, 1062, c + 25, Y_SOLA)
        tn.close()
        sh = skia.GradientShader.MakeLinear([skia.Point(c - 26, 0), skia.Point(c + 26, 0)],
                                            [_c("#B9C4CF"), _c(TENIS), _c("#FFFFFF"), _c(TENIS), _c("#B9C4CF")],
                                            [0.0, 0.25, 0.5, 0.75, 1.0])
        cv.drawPath(tn, paint(TENIS, 255, shader=sh))
        cv.drawRect(skia.Rect(c - 26, Y_SOLA - 9, c + 26, Y_SOLA), paint(TENIS_SOLA))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(c - 6, 1037, c + 6, 1056), 3, 3), paint(TENIS_DET))
        cv.drawPath(tn, paint("#5E6B78", 230, "stroke", 2.4))


def short_path(p):
    e = p.d
    sx = p.sway * (1 - e) * 0.6
    S0 = ((452, 772), (444, 822), (440, 880), (538, 885), (540, 868), (542, 885), (640, 880), (636, 822), (628, 772))
    S1 = ((446, 818), (432, 866), (436, 912), (538, 918), (540, 898), (542, 918), (644, 912), (648, 866), (634, 818))
    q = [(lerp(a[0], b[0], e) + sx, lerp(a[1], b[1], e)) for a, b in zip(S0, S1)]
    pth = skia.Path()
    pth.moveTo(*q[0])
    pth.cubicTo(q[0][0] - 6, q[0][1] + 18, q[1][0] - 2, q[1][1] - 18, *q[1])
    pth.cubicTo(q[1][0] + 1, q[1][1] + 22, q[2][0] - 2, q[2][1] - 22, *q[2])
    pth.lineTo(*q[3]); pth.lineTo(*q[4]); pth.lineTo(*q[5]); pth.lineTo(*q[6])
    pth.cubicTo(q[6][0] + 2, q[6][1] - 22, q[7][0] - 1, q[7][1] + 22, *q[7])
    pth.cubicTo(q[7][0] + 2, q[7][1] - 18, q[8][0] + 6, q[8][1] + 18, *q[8])
    arco = lerp(0.0, 8.0, e)                                     # na flexão, o cós faz um arquinho
    pth.quadTo(540 + sx, q[0][1] - arco * 2, *q[0])
    pth.close()
    return pth, q


def desenha_short(cv, p):
    pth, q = short_path(p)
    cv.drawPath(pth, paint("#000000", 60, blur=8))
    sh = skia.GradientShader.MakeLinear([skia.Point(q[1][0], 0), skia.Point(q[7][0], 0)],
                                        [_c("#14264A"), _c(SHORT), _c(SHORT_CL), _c(SHORT), _c("#14264A")],
                                        [0.0, 0.25, 0.5, 0.75, 1.0])
    cv.drawPath(pth, paint(SHORT, 255, shader=sh))
    cv.save(); cv.clipPath(pth, skia.ClipOp.kIntersect, True)
    cos_y = (q[0][1] + q[8][1]) / 2
    cv.drawRect(skia.Rect(q[1][0] - 20, cos_y - 30, q[7][0] + 20, cos_y + 20), paint(SHORT_CL))   # cós
    cv.drawLine(q[1][0] - 20, cos_y + 20, q[7][0] + 20, cos_y + 20, paint(SHORT_LINHA, 200, "stroke", 2.6))
    for a, b in ((q[0], q[2]), (q[8], q[6])):                    # listra lateral branca
        s = 1 if a[0] < 540 else -1
        li = skia.Path(); li.moveTo(a[0] + s * 9, a[1] + 4)
        mid = ((a[0] + b[0]) / 2 + s * 3, (a[1] + b[1]) / 2 + 6)
        li.quadTo(mid[0], mid[1], b[0] + s * 10, b[1] - 4)
        cv.drawPath(li, paint(LISTRA, 235, "stroke", 7))
    cv.drawLine(540 + p.sway * (1 - p.d) * 0.6, cos_y + 26, 540 + p.sway * (1 - p.d) * 0.6, q[4][1] - 4,
                paint(SHORT_LINHA, 200, "stroke", 2.6))           # costura do meio
    cv.restore()
    cv.drawPath(pth, paint(SHORT_LINHA, 235, "stroke", 3.0))


def crianca(cv, p, antes_bracos=None, antes_crianca=None, a_escapula=1.0):
    """A criança inteira, de costas. `antes_crianca()`: o que fica atrás dela (parte de trás do anel);
    `antes_bracos()`: o que fica atrás dos braços e do tronco (o dourado dos vãos)."""
    cv.drawOval(skia.Rect(430, Y_SOLA - 10, 650, Y_SOLA + 14), paint("#000000", 90, blur=10))
    if antes_crianca:
        antes_crianca()
    desenha_cabeca(cv, p)
    if antes_bracos:
        antes_bracos()
    desenha_braco(cv, p, -1); desenha_braco(cv, p, 1)
    desenha_tronco(cv, p, a_escapula)
    desenha_pernas(cv, p)
    desenha_short(cv, p)


# ------------------------------------------------------------------ a quadra (mundo)
def quadra(cv):
    """Quadra de escola em desenho: parede, rodapé escuro, piso de madeira clara com UMA linha branca. Sem
    placa, número, texto ou outra pessoa."""
    x0, x1 = -700, 1800
    cv.drawRect(skia.Rect(x0, -400, x1, 905), paint(PAREDE))
    cv.drawRect(skia.Rect(x0, 640, x1, 905), paint(PAREDE_CL))   # faixa de baixo da parede (pintura de quadra)
    cv.drawLine(x0, 640, x1, 640, paint("#2F4859", 255, "stroke", 4))
    cv.drawRect(skia.Rect(x0, 900, x1, 930), paint(RODAPE))
    cv.drawRect(skia.Rect(x0, 930, x1, 1700), paint(PISO))
    ys = [930, 948, 969, 994, 1023, 1057, 1096, 1141, 1192, 1250, 1316, 1390, 1475, 1570]
    for i, (ya, yb) in enumerate(zip(ys, ys[1:])):               # tábuas: fileiras que crescem para a frente
        if i % 2:
            cv.drawRect(skia.Rect(x0, ya, x1, yb), paint(PISO_B))
        larg = 150 + 30 * i
        off = (i * 97) % larg
        x = x0 - off
        while x < x1:
            cv.drawLine(x, ya, x + (x - 540) * 0.08, yb, paint(PISO_JUNTA, 150, "stroke", 2))
            x += larg
        cv.drawLine(x0, ya, x1, ya, paint(PISO_JUNTA, 200, "stroke", 2.4))
    cv.drawRect(skia.Rect(x0, 959, x1, 967), paint(LINHA_QUADRA, 235))   # a linha pintada da quadra


# ------------------------------------------------------------------ o tempo do filme
class Filme:
    """Liga o tempo do VÍDEO ao tempo do FILME, por trechos presos às palavras-âncora (cópia adaptada do
    piloto): play (1×), volta (rebobinar), lenta (0,25×), congela (0×), avanca (avanço rápido).
    A 1ª câmera lenta revê a descida que o 1× JÁ passou (borrada); a 2ª revê a criança de pé que o 1× calmo
    já mostrou; o replay final revê os últimos graus da flexão."""

    def __init__(self, T):
        s = []
        self.t_1x = T["de"] - B / V1 - 0.03                                # o fundo passa ~1 quadro antes da volta
        tf_a = -V1 * self.t_1x
        tf_v = V1 * (T["de"] - self.t_1x)

        def f1(tv):                                                        # vídeo -> filme no 1× do começo
            return V1 * (tv - self.t_1x)
        # 1ª flexão: desce no "frente" e sobe devagar até emendar no preparo da flexão completa (sem pausa de pé)
        AQUEC[:] = [f1(T["tronco"]), f1(T["frente"] + 0.28), min(-T_PREP - 0.05, f1(T["por"]) - T_PREP - 0.05), 0.62]
        L1 = B - VL * (T["lado"] - T["camera"])                            # a 0,25×, chega ao fundo NO "lado"
        s.append((0.0, T["de"], "play", tf_a, tf_v, None))
        s.append((T["de"], T["camera"], "volta", tf_v, L1, "sai"))         # "De novo": a fita volta de supetão
        s.append((T["camera"], T["lado"], "lenta", L1, B, None))
        s.append((T["lado"], T["costuma"], "congela", B, B, None))
        self.tf_o = B + V1 * (T["ombro"] - T["costuma"])                   # 1× calmo até o "ombro": de pé, parada
        s.append((T["costuma"], T["ombro"], "play", B, self.tf_o, None))
        s.append((T["ombro"], T["estirao"], "congela", self.tf_o, self.tf_o, None))
        self.t_rp = T["rapido"] + 0.42                                     # replay limpo (fim do "rápido")
        tf_ff = self.tf_o + VR * (self.t_rp - T["estirao"])
        s.append((T["estirao"], self.t_rp, "avanca", self.tf_o, tf_ff, None))
        self.t_cta = T["manda"] - 0.15
        self.R0 = B - VL * (self.t_cta - self.t_rp)
        s.append((self.t_rp, self.t_cta, "lenta", self.R0, B, None))
        fim = T["total"] + 2.0
        s.append((self.t_cta, fim, "play", B, B + V1 * (fim - self.t_cta), None))
        self.segs = s
        self.T = T
        self.L1 = L1
        self.tf_cola = L1 + VL * (T["lenta"] - T["camera"])                # os pontos grudam aqui
        assert 0.1 < L1 < 0.7, ("a câmera lenta tem de começar com o tronco JÁ descendo", L1)
        assert 0.3 < self.R0 < B, self.R0
        assert self.tf_o > F_IDLE, ("no 'ombro' ela tem de estar de pé, parada, braços ao lado", self.tf_o)
        assert tf_v > B, "o 1× tem de passar pela flexão completa antes da volta"
        assert tf_a < AQUEC[0] < AQUEC[1] < AQUEC[2] < -T_PREP, ("o aquecimento cabe antes do preparo", AQUEC, tf_a)

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
        elif ease == "sai":
            k = 1 - (1 - k) ** 2
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
    return max(prog(t, T["camera"], T["camera"] + 0.18) * (1 - prog(t, T["costuma"] - 0.22, T["costuma"] - 0.02)),
               prog(t, F.t_rp, F.t_rp + 0.18) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))


# ------------------------------------------------------------------ câmera (mundo -> tela)
BASE = (1.0, XC, Y_SOLA, XC, Y_SOLA)
LENTA = (1.12, XC, 760.0, XC, 770.0)
ZOOM_LADO = (1.5, 560.0, 760.0, XC, 760.0)
ZOOM_LADO2 = (1.6, 562.0, 752.0, XC, 760.0)                      # empurrão lento durante o congelamento
OMBROS = (1.8, 540.0, 598.0, XC, 720.0)
CINTURA = (1.8, 545.0, 728.0, XC, 770.0)
ESCAPULA = (2.3, 552.0, 652.0, XC, 770.0)
ESTIRAO = (0.9, XC, Y_SOLA, XC, 1110.0)


def _mist(a, b, k):
    return tuple(lerp(x, y, k) for x, y in zip(a, b))


def camera(t, T, F):
    cam = BASE
    passos = ((T["camera"] + 0.1, 1.4, LENTA),
              (T["lado"], 0.13, ZOOM_LADO),                       # zoom seco 1,5× nas costas
              (T["lado"] + 0.2, T["costuma"] - T["lado"] - 0.3, ZOOM_LADO2),
              (T["costuma"], 0.6, BASE),
              (T["olha2"] + 0.05, 0.55, OMBROS),                  # "Olha também": ombros
              (T["cintura"] - 0.05, 0.45, CINTURA),
              (T["escapula"] - 0.05, 0.45, ESCAPULA),
              (T["sinal3"] - 0.1, 0.5, BASE),
              (T["estirao"], 0.45, ESTIRAO),
              (F.t_rp, 0.05, LENTA),
              (F.t_cta, 0.6, BASE))
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
    """O mesmo fundo do cf_alongamento.fundo (degradê radial que respira + partículas). (cópia do piloto)"""
    def d(c):
        sh = skia.GradientShader.MakeRadial(skia.Point(W / 2, H * 0.42 + 60), H * 0.78, [_c("#17384C"), _c(BG_OUT)])
        c.drawRect(skia.Rect(0, 0, W, H + 120), paint("#17384C", shader=sh))
    _blit(cv, _img("fundo", W, H + 120, d), 0, -60 + 40 * math.sin(t * 0.3))
    for x, y, v, r, a in PART:
        yy = (y - v * t * 6) % H
        cv.drawCircle(x + 8 * math.sin(t * 0.5 + y), yy, r, paint("#BFE3FF", int(a)))


def _rel(c):
    c.translate(-CENA.left(), -CENA.top())


def vinheta(cv):
    def d(c):
        _rel(c)
        sh = skia.GradientShader.MakeRadial(skia.Point(540, 760), 760, [_c("#000000", 0), _c("#000000", 0), _c("#000000", 110)],
                                            [0.0, 0.5, 1.0])
        c.drawRect(CENA, paint("#000000", 255, shader=sh))
    _blit(cv, _img("vinheta", CENA.width(), CENA.height(), d), CENA.left(), CENA.top())


def varredura(cv, t, ambar, limpo=False):
    """Linhas de varredura + granulação (semente = índice do quadro) + tinta âmbar da câmera lenta."""
    if ambar > 0:
        def d(c):
            _rel(c)
            sh = skia.GradientShader.MakeRadial(skia.Point(540, 780), 720,
                                                [_c(AMBAR, 0), _c(AMBAR, 0), _c(AMBAR, 70), _c(AMBAR, 150)],
                                                [0.0, 0.5, 0.85, 1.0])
            c.drawRect(CENA, paint(AMBAR, 255, shader=sh))
            r = skia.Rect(CENA.left() + 6, CENA.top() + 6, CENA.right() - 6, CENA.bottom() - 6)
            c.drawRect(r, paint(AMBAR, 230, "stroke", 5))
            c.drawRect(CENA, paint(AMBAR, 40))
        _blit(cv, _img("ambar", CENA.width(), CENA.height(), d), CENA.left(), CENA.top(), ambar)
    if limpo:
        return

    def dl(c):
        _rel(c)
        lin = skia.Path()
        y = CENA.top() + 2
        while y < CENA.bottom():
            lin.moveTo(CENA.left(), y); lin.lineTo(CENA.right(), y); y += 6
        c.drawPath(lin, paint("#000000", 10, "stroke", 2))
    _blit(cv, _img("linhas", CENA.width(), CENA.height(), dl), CENA.left(), CENA.top())
    rng = np.random.default_rng(int(round(t * FPS)) + 1)
    xs = rng.uniform(CENA.left(), CENA.right(), 340); ys = rng.uniform(CENA.top(), CENA.bottom(), 340)
    pts = [skia.Point(float(a), float(b)) for a, b in zip(xs, ys)]
    cv.drawPoints(skia.Canvas.kPoints_PointMode, pts[:170], paint("#FFFFFF", 12, "stroke", 2.2))
    cv.drawPoints(skia.Canvas.kPoints_PointMode, pts[170:], paint("#000000", 14, "stroke", 2.2))


def faixas_tracking(cv, t, a):
    """Faixas de 'tracking' de fita de vídeo varrendo a cena (voltar e avançar a fita). (cópia do piloto)"""
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
    pt = paint("#FFFFFF", int(150 * a), "stroke", 5)
    pt.setStrokeCap(skia.Paint.kSquare_Cap)
    for x, y, sx, sy in ((r.left(), r.top(), 1, 1), (r.right(), r.top(), -1, 1),
                         (r.left(), r.bottom(), 1, -1), (r.right(), r.bottom(), -1, -1)):
        p = skia.Path(); p.moveTo(x, y + sy * L); p.lineTo(x, y); p.lineTo(x + sx * L, y)
        cv.drawPath(p, pt)


def flash(cv, t, t0, forte=1.0):
    k = t - t0
    if 0 <= k < 0.07:                                            # 2 quadros
        img = _img("flash", CENA.width(), CENA.height(), lambda c: c.clear(_c("#FFFFFF", 255)))
        _blit(cv, img, CENA.left(), CENA.top(), 0.47 * forte * (1 - k / 0.07))


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


TAM_CHIP = 40


def chip_dim(s, tam=TAM_CHIP):
    lw = skia.Font(F_BLACK, tam).measureText(s)
    return lw, lw + 30, tam * 1.36


def chip_c(cv, s, cx, cy, a, tam=TAM_CHIP, dim=1.0, esc=1.0):
    """Rótulo de velocidade CENTRADO em (cx, cy). (cópia do piloto)"""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam)
    lw, w, h = chip_dim(s, tam)
    cv.save(); cv.translate(cx, cy); cv.scale(esc, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-w / 2, -h / 2, w / 2, h / 2), 13, 13)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(235 * a)))
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


HUD_X, HUD_Y = 812, 1166                                         # centro do relógio (na linha do chão, à direita)
POP_C = (872, 640)                                               # onde o "0,25×" grande aparece: ao lado, longe da cabeça
POP_ESC = 2.1                                                    # e do lado do painel: o voo DESCE pela direita, sem
                                                                 # cruzar a criança (os braços inteiros pendem dos 2 lados)


def _chip_hud_c(s):
    _, w, _ = chip_dim(s)
    return HUD_X + 46 + w / 2, HUD_Y


def painel(cv, t, T, F, a):
    if a <= 0:
        return
    # placa escura atrás do painel (o piso é claro)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(HUD_X - 48, HUD_Y - 46, HUD_X + 196, HUD_Y + 44), 22, 22),
                 paint(FUNDO_CARTAO, int(150 * a)))
    tipo = F.tipo(t)
    relogio(cv, HUD_X, HUD_Y, 32, a, F.tf(t) * 2 * math.pi)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(HUD_X - 7, HUD_Y - 47, HUD_X + 7, HUD_Y - 36), 3, 3), paint(OURO, int(255 * a)))
    t0 = F.inicio_trecho(t)
    if tipo in ("volta", "avanca"):
        _setas(cv, HUD_X + 50, HUD_Y, a * (0.75 + 0.25 * math.sin(t * 18)), 1.1, tipo == "avanca")
        return
    if tipo == "congela":                                        # o rótulo do trecho anterior, apagado
        s = R_LENTA if lento_k(t, T, F) > 0 else R_1X
        chip_c(cv, s, *_chip_hud_c(s), a, dim=0.4)
        return
    s = R_LENTA if tipo == "lenta" else R_1X
    hx, hy = _chip_hud_c(s)
    k = t - t0
    if tipo == "lenta" and k < 0.75 and t0 == T["camera"]:      # "0,25×" grande que voa para o painel
        cx, cy = POP_C
        if k < 0.32:
            chip_c(cv, s, cx, cy, a, esc=POP_ESC * e_back(clamp(k / 0.16)))
        else:
            v = e_inout(prog(k, 0.32, 0.75))
            chip_c(cv, s, lerp(cx, hx, v), lerp(cy, hy, v), a, esc=lerp(POP_ESC, 1.0, v))
        return
    pop = 1 + 0.6 * (1 - e_out(prog(t, t0, t0 + 0.3))) if t0 > 0 else 1.0
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


def ponta_seta(cv, x, y, ang, tam, cor, a):
    p = skia.Path()
    p.moveTo(x + tam * math.cos(ang), y + tam * math.sin(ang))
    p.lineTo(x + tam * 0.75 * math.cos(ang + 2.45), y + tam * 0.75 * math.sin(ang + 2.45))
    p.lineTo(x + tam * 0.75 * math.cos(ang - 2.45), y + tam * 0.75 * math.sin(ang - 2.45))
    p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))


def tracejada(cv, x0, y, x1, a, k=1.0, cor="#FFFFFF", larg=5):
    """Linha horizontal tracejada de referência (traçada da esquerda para a direita)."""
    if a <= 0 or k <= 0:
        return
    xk = lerp(x0, x1, e_out(k))
    sombra = paint("#000000", int(120 * a), "stroke", larg + 4, blur=3)
    cv.drawLine(x0, y, xk, y, sombra)
    pt = paint(cor, int(255 * a), "stroke", larg)
    pt.setPathEffect(skia.DashPathEffect.Make([18.0, 12.0], 0.0))
    cv.drawLine(x0, y, xk, y, pt)


def estetoscopio(cv, x, y, esc, a):
    """Selo branco e calmo do "leve para avaliação": estetoscópio desenhado (forma, sem texto). (cópia do piloto)"""
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
    """Olho desenhado (o sinal é para ser VISTO): contorno dourado, olho branco, sem texto. (do cf_escoliose)"""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    L, hh = 82, 46 * max(0.06, abre)
    p = skia.Path(); p.moveTo(-L, 0)
    p.cubicTo(-L * 0.45, -hh * 1.3, L * 0.45, -hh * 1.3, L, 0)
    p.cubicTo(L * 0.45, hh * 1.3, -L * 0.45, hh * 1.3, -L, 0); p.close()
    cv.drawPath(p, paint(OURO, int(90 * a), blur=16))
    cv.drawPath(p, paint("#FFFFFF", int(255 * a)))
    cv.save(); cv.clipPath(p, skia.ClipOp.kIntersect, True)
    cv.drawCircle(0, 0, 30, paint("#2E5C8A", int(255 * a)))
    cv.drawCircle(0, 0, 30, paint("#1C3B5C", int(255 * a), "stroke", 4))
    cv.drawCircle(0, 0, 13, paint("#0E1A26", int(255 * a)))
    cv.drawCircle(-9, -10, 6, paint("#FFFFFF", int(230 * a)))
    cv.restore()
    cv.drawPath(p, paint(OURO, int(255 * a), "stroke", 7))
    cv.restore()


def piscada(t, t0):
    k = t - t0
    if 0 <= k < 0.22:
        return abs(1 - 2 * k / 0.22)
    return 1.0


def calendario(cv, x, y, t, t0, a, esc=1.9, t_rapido=None):
    """Folhas virando, SEM número (cópia do cf_fratura_cola via piloto, cabeçalho azul-claro: nada de
    vermelho). A partir de `t_rapido` as folhas viram ainda mais depressa."""
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
    k = (t - t0) * 5 + (max(0.0, t - t_rapido) * 7 if t_rapido is not None else 0.0)
    fase = k - math.floor(k)
    for i in range(3):
        cv.drawLine(14, 42 + i * 16, 82, 42 + i * 16, paint("#9AA8B5", int(200 * a), "stroke", 4))
    if fase > 0:
        cv.save(); cv.translate(0, 24); cv.scale(1, 1 - fase)
        cv.drawRect(skia.Rect(0, 0, 96, 68), paint("#FFFFFF", int(170 * a * (1 - fase))))
        cv.restore()
    cv.restore()


def desenha_trilha(cv, pts, a, s):
    """Pontilhado dourado no referencial do MUNDO. (cópia do piloto)"""
    if a <= 0 or len(pts) < 2:
        return
    p = _suave(pts, fechar=False)
    pt = paint(OURO, int(255 * a), "stroke", 7.0 / s)
    pt.setPathEffect(skia.DashPathEffect.Make([1.0 / s, 16.0 / s], 0))
    cv.drawPath(p, paint("#000000", int(60 * a), "stroke", 10.0 / s, blur=3.0 / s))
    cv.drawPath(p, pt)


def ponto_ouro(cv, x, y, a, r=12):
    if a <= 0:
        return
    cv.drawCircle(x, y, r + 10, paint(OURO, int(90 * a), blur=10))
    cv.drawCircle(x, y, r, paint(OURO, int(255 * a)))
    cv.drawCircle(x, y, r, paint(FUNDO_CARTAO, int(255 * a), "stroke", 3))


def trilhas(tf0, tf1):
    """Os caminhos (mundo) dos dois pontos dourados entre os instantes de filme tf0 e tf1."""
    out = {-1: [], 1: []}
    if tf1 <= tf0:
        return out
    n = max(2, int((tf1 - tf0) / 0.012))
    for i in range(n + 1):
        p = Pose(lerp(tf0, tf1, i / n))
        for lado in (-1, 1):
            out[lado].append(ponto_costas(p, lado))
    return out


# ------------------------------------------------------------------ o ANEL da rotação (por fora do tronco)
ANEL_C, ANEL_RX, ANEL_RY, ANEL_GIRO = (540.0, 792.0), 206.0, 146.0, -11.0
ANEL_A0, ANEL_VOLTA = 150.0, 270.0                               # começa embaixo à esquerda, 3/4 de volta


def anel_pts(k):
    """Pontos do anel (mundo) até a fração k; cada um marcado se passa POR TRÁS do quadril (parte de baixo)."""
    n = 90
    g = math.radians(ANEL_GIRO); cg, sg = math.cos(g), math.sin(g)
    pts = []
    for i in range(int(n * k) + 1):
        ang = math.radians(ANEL_A0 - ANEL_VOLTA * i / n)         # ângulo diminui: no lado direito, o anel SOBE
        x, y = ANEL_RX * math.cos(ang), ANEL_RY * math.sin(ang)
        atras = math.sin(ang) > 0.42
        pts.append((ANEL_C[0] + x * cg - y * sg, ANEL_C[1] + x * sg + y * cg, atras))
    return pts


def desenha_anel(cv, k, a, s, parte):
    """parte = "tras" (antes da criança) ou "frente" (depois). Traço em px de TELA."""
    if a <= 0 or k <= 0:
        return
    pts = anel_pts(k)
    trechos, atual = [], []
    for x, y, atras in pts:
        if (parte == "tras") == atras:
            atual.append((x, y))
        elif atual:
            trechos.append(atual); atual = []
    if atual:
        trechos.append(atual)
    fator = 0.55 if parte == "tras" else 1.0
    for tr in trechos:
        if len(tr) < 2:
            continue
        p = skia.Path(); p.moveTo(*tr[0])
        for q in tr[1:]:
            p.lineTo(*q)
        cv.drawPath(p, paint("#000000", int(110 * a * fator), "stroke", 15.0 / s, blur=4.0 / s))
        cv.drawPath(p, paint(OURO, int(255 * a * fator), "stroke", 9.0 / s))
    if parte == "frente" and len(pts) >= 2 and not pts[-1][2]:
        (x0, y0, _), (x1, y1, _) = pts[-2], pts[-1]
        ponta_seta(cv, x1, y1, math.atan2(y1 - y0, x1 - x0), 30.0 / s, OURO, a)


# ------------------------------------------------------------------ o dourado dos vãos braço-cintura (de pé)
def vao_path(p, lado):
    """Região entre o braço e a cintura (mundo): desenhada ATRÁS do braço e do tronco, só o vão aparece."""
    (jx, jy), (ex, ey), (hx, hy) = braco_geo(p, lado)

    def braco_x(y):
        if y <= ey:
            return lerp(jx, ex, (y - jy) / max(1e-6, ey - jy))
        return lerp(ex, hx, (y - ey) / max(1e-6, hy - ey))
    ys = [656 + 8 * i for i in range(17)]                        # da axila até o cós
    ida = [(braco_x(y), y) for y in ys]
    volta = [(lado_x(p, lado, y) - lado * 10, y) for y in reversed(ys)]
    pth = skia.Path(); pth.moveTo(*ida[0])
    for q in ida[1:] + volta:
        pth.lineTo(*q)
    pth.close()
    return pth


# ------------------------------------------------------------------ borrão de movimento (1×, voltando, avançando)
OBTURADOR = {"play": 0.09, "volta": 0.05, "avanca": 0.04}        # s de VÍDEO
OBT_1X_1 = 0.16                                                  # o 1× do começo: borrão maior (o fundo passa borrado)
OBT_CALMO = 0.0                                                  # o 1× calmo sai nítido
N_AMOSTRAS = 6
CAIXA = skia.Rect(250, 300, 830, 1110)


def amostras_borrao(t, F):
    """Instantes (vídeo) que entram no borrão de `t`: só no 1×, voltando ou avançando, sem atravessar
    congelamento nem a troca de trecho, e nunca antes de t = 0 (o quadro 0 sai nítido). (adaptado do piloto)"""
    tipo = F.tipo(t)
    obt = OBTURADOR.get(tipo)
    if not obt:
        return [t]
    if tipo == "play" and t < F.T["de"]:
        obt = OBT_1X_1
    elif tipo == "play" and t < F.t_cta:
        obt = OBT_CALMO                                          # o 1× calmo do "não doer": nítido
    if obt <= 0:
        return [t]
    seg = F.seg(t)
    n = _n_amostras(t, obt, F)
    out = [t]
    for i in range(1, n):
        tg = t - obt * i / (n - 1)
        if tg < 0 or F.seg(tg) is not seg:
            break
        out.append(tg)
    return out


PASSO_MAO = 7.0                                                  # px: deslocamento máximo da mão entre 2 amostras
N_AMOSTRAS_MAX = 48


def _n_amostras(t, obt, F):
    """Quantas poses entram no borrão: 6, ou mais quando o braço varre rápido (subir/descer pelo lado). Com 6
    poses um braço inteiro girando sai em 6 CÓPIAS separadas (leque de ecos); com o passo da mão limitado a
    ~7 px as cópias se sobrepõem e o borrão vira rastro contínuo."""
    k = 16
    ps = [pose_t(max(0.0, t - obt * i / k), F) for i in range(k + 1)]
    L = 0.0
    for lado in (-1, 1):
        g = [braco_geo(p, lado) for p in ps]
        for j in (1, 2):                                         # cotovelo e mão
            L = max(L, sum(math.hypot(b[j][0] - a[j][0], b[j][1] - a[j][1]) for a, b in zip(g, g[1:])))
    return int(clamp(math.ceil(L / PASSO_MAO) + 1, N_AMOSTRAS, N_AMOSTRAS_MAX))


def crianca_borrada(cv, t, F, **kw):
    ams = amostras_borrao(t, F)
    poses = [pose_t(x, F) for x in ams]
    if len(poses) == 1 or (max(abs(q.d - poses[0].d) for q in poses) < 0.003
                           and max(abs(q.up - poses[0].up) for q in poses) < 0.003):
        crianca(cv, poses[0], **kw)
        return
    pf = skia.Paint()
    sy = 6.0 if t < F.T["camera"] else 3.0                          # 1º 1× e 1ª volta: o fundo passa borrado
    pf.setImageFilter(skia.ImageFilters.Blur(1.0, sy))
    cv.saveLayer(CAIXA, pf)
    for k, p in enumerate(reversed(poses)):                      # do mais velho ao mais novo (média corrida)
        if k == 0:
            crianca(cv, p, **kw)
        else:
            cv.saveLayer(CAIXA, _alfa(1.0 / (k + 1)))
            crianca(cv, p, **kw)
            cv.restore()
    cv.restore()


# ------------------------------------------------------------------ marcações de pé (ombro, cintura, escápula)
def setas_desnivel(cv, x, y_alto, y_baixo, a, ka):
    """Marcador de desnível: duas setinhas por fora do vão, uma apontando para cada linha (sem régua)."""
    if a <= 0 or ka <= 0:
        return
    for y_tip, sentido in ((y_alto - 3, 1), (y_baixo + 3, -1)):
        y0 = y_tip - sentido * 44 * ka
        cv.drawLine(x, y0, x, y_tip - sentido * 10, paint("#000000", int(110 * a), "stroke", 9, blur=3))
        cv.drawLine(x, y0, x, y_tip - sentido * 10, paint(OURO, int(255 * a), "stroke", 5))
        ponta_seta(cv, x, y_tip - sentido * 8, math.pi / 2 * sentido, 20, OURO, a * ka)


def contorno_ombro(cv, cam, p, a, k):
    """Traço dourado por cima do contorno do ombro DIREITO (é ele que está mais alto)."""
    if a <= 0 or k <= 0:
        return
    pth = skia.Path()
    n = 16
    for i in range(n + 1):
        u = 0.32 + 0.72 * i / n
        x, y = na_tela(cam, x_u(u, p), topo(u, p) - 3)
        (pth.moveTo if i == 0 else pth.lineTo)(x, y)
    cv.drawPath(pth, _trim(paint("#000000", int(110 * a), "stroke", 13, blur=4), e_out(k)))
    cv.drawPath(pth, _trim(paint(OURO, int(255 * a), "stroke", 8), e_out(k)))


def marcas_de_pe(cv, t, T, F, cam):
    """Congelamento de pé (do "ombro" ao "sinal" da 3ª vez): uma marcação por vez, a câmera vai até ela."""
    pO = Pose(F.tf_o)
    fim = 1 - prog(t, T["sinal3"] - 0.1, T["sinal3"] + 0.2)
    # OMBRO: tracejada branca na altura do ombro ESQUERDO; o direito passa acima (traço dourado + desnível)
    a_o = prog(t, T["ombro"] + 0.05, T["ombro"] + 0.15) * (1 - prog(t, T["cintura"] - 0.1, T["cintura"] + 0.2)) * fim
    if a_o > 0:
        y_e = topo(-0.86, pO)
        xa, yy = na_tela(cam, x_u(-1.4, pO), y_e)
        xb, _ = na_tela(cam, x_u(1.5, pO), y_e)
        tracejada(cv, xa, yy, xb, a_o, prog(t, T["ombro"] + 0.05, T["ombro"] + 0.35))
        a2 = a_o * prog(t, T["alto2"], T["alto2"] + 0.1)
        if a2 > 0:
            contorno_ombro(cv, cam, pO, a2, prog(t, T["alto2"], T["alto2"] + 0.35))
            y_d = topo(0.86, pO)
            xd, yd = na_tela(cam, x_u(1.38, pO), y_d)
            setas_desnivel(cv, xd, yd, yy, a2, e_out(prog(t, T["alto2"] + 0.15, T["alto2"] + 0.45)))
    # ESCÁPULA: círculo pequeno na escápula DIREITA (a esquerda, plana, fica sem marca: é a comparação)
    a_e = prog(t, T["escapula"] + 0.3, T["escapula"] + 0.4) * fim
    if a_e > 0:
        (mx, my), (lx, ly), (ax, ay) = escapula_geo(pO, 1)
        cx_, cy_ = na_tela(cam, (mx + lx + ax) / 3 + 2, (my + ly + ay) / 3 + 4)
        circulo_mao(cv, cx_, cy_, 52 * cam[0], 64 * cam[0], prog(t, T["escapula"] + 0.3, T["escapula"] + 0.7), a_e)


# ------------------------------------------------------------------ o mundo (dentro do monitor)
def monitor(cv, t, T, F, limpo=False):
    """Tudo o que fica DENTRO do monitor de replay (recortado em CENA). `limpo`: miniatura (sem linhas de
    varredura, grão, tracking nem flash). -> câmera."""
    tipo = F.tipo(t)
    cam = camera(t, T, F)
    if tipo == "volta":                                          # tremidinha de fita voltando
        j = math.sin(t * 97) * 4 + math.sin(t * 41) * 3
        cam = (cam[0], cam[1], cam[2], cam[3] + j, cam[4])
    s = cam[0]
    tf = F.tf(t)
    p = pose_t(t, F)

    cv.save(); cv.clipRect(CENA, True)
    cv.save(); aplica(cv, cam)
    quadra(cv)

    # anel da rotação (congelado na flexão): a parte de baixo passa por trás do quadril
    a_flex = 1 - prog(t, T["costuma"] - 0.05, T["costuma"] + 0.25)
    k_anel = e_inout(prog(t, T["girando"], T["girando"] + 0.6))
    a_anel = prog(t, T["girando"], T["girando"] + 0.08) * a_flex if t >= T["girando"] else 0.0

    # CINTURA: o dourado dos vãos braço-cintura (de pé, congelado), atrás dos braços e do tronco
    a_vao = prog(t, T["cintura"], T["cintura"] + 0.25) * (1 - prog(t, T["escapula"] - 0.05, T["escapula"] + 0.25)) \
        if t >= T["cintura"] else 0.0
    pulso_vao = 0.5 + 0.5 * math.sin((t - T["torta"]) * 9) if t >= T["torta"] else 1.0

    def vaos():
        for lado in (-1, 1):
            pth = vao_path(p, lado)
            cv.drawPath(pth, paint(OURO, int(150 * a_vao * pulso_vao), blur=10 / s))
            cv.drawPath(pth, paint(OURO, int(245 * a_vao)))

    crianca_borrada(cv, t, F, antes_crianca=(lambda: desenha_anel(cv, k_anel, a_anel, s, "tras")) if a_anel > 0 else None,
                    antes_bracos=vaos if a_vao > 0 else None)
    desenha_anel(cv, k_anel, a_anel, s, "frente")

    # pontos dourados e trilhas (1ª câmera lenta até o "alto"; replay final)
    a_pt1 = prog(t, T["lenta"], T["lenta"] + 0.15) * (1 - prog(t, T["alto1"] + 0.05, T["alto1"] + 0.45))
    a_pt3 = prog(t, F.t_rp + 0.05, F.t_rp + 0.3) * (1 - prog(t, T["manda"] - 0.3, T["manda"]))
    if a_pt1 > 0 or a_pt3 > 0:
        a_pt = max(a_pt1, a_pt3)
        tf0 = F.tf_cola if a_pt1 >= a_pt3 else F.R0             # trilha só do trecho revisto (sem "anteninha")
        tr = trilhas(tf0, min(tf, B))
        for lado in (-1, 1):
            desenha_trilha(cv, tr[lado], a_pt, s)
        for lado in (-1, 1):
            x, y = ponto_costas(p, lado)
            k = t - T["lenta"]
            gruda = 1 + 0.5 * (1 - e_out(clamp(k / 0.25))) if a_pt1 > 0 else 1.0
            ponto_ouro(cv, x, y, a_pt, r=12 * gruda / s * 1.12)
    # "rápido": um ponto dourado pulsa no alto da metade direita das costas (é ali que se olha)
    a_pul = prog(t, T["rapido"], T["rapido"] + 0.15) * (1 - prog(t, F.t_rp - 0.1, F.t_rp + 0.05))
    if a_pul > 0:
        x, y = ponto_costas(p, 1)
        k = t - T["rapido"]
        r = (12 + 3 * math.sin(k * 12)) / s
        cv.drawCircle(x, y, r * 2.6 * (0.6 + 0.4 * (0.5 + 0.5 * math.sin(k * 12))), paint(OURO, int(80 * a_pul), blur=10 / s))
        ponto_ouro(cv, x, y, a_pul, r=r)
    cv.restore()
    vinheta(cv)

    # ---------------- marcações em tela (px de tela)
    pB = Pose(B)
    # (1) flexão congelada: tracejada no alto do lado ESQUERDO; o direito fica acima dela. No "girando", tudo
    #     baixa para ~25% e só o anel (e o carimbo) ficam em destaque.
    if T["lado"] <= t < T["costuma"] + 0.3:
        a = a_flex * (1 - 0.75 * prog(t, T["girando"], T["girando"] + 0.3))
        u_ref = -0.38
        yref_m = topo(u_ref, pB)
        xa, yref = na_tela(cam, x_u(-1.25, pB), yref_m)
        xb, _ = na_tela(cam, x_u(1.65, pB), yref_m)
        tracejada(cv, xa, yref, xb, a, prog(t, T["lado"] + 0.12, T["lado"] + 0.45))
        a2 = prog(t, T["alto1"], T["alto1"] + 0.1) * a
        if a2 > 0:
            ytop_m = topo(0.38, pB)
            bx, ytop = na_tela(cam, x_u(0.38, pB), ytop_m)
            xm, _ = na_tela(cam, x_u(1.45, pB), ytop_m)
            tracejada(cv, bx - 30, ytop, xm + 40, a2, prog(t, T["alto1"], T["alto1"] + 0.3), cor=OURO, larg=4)
            circulo_mao(cv, bx, ytop + 24, 92, 60, prog(t, T["alto1"], T["alto1"] + 0.35), a2)
            setas_desnivel(cv, xm, ytop, yref, a2, e_out(prog(t, T["alto1"] + 0.15, T["alto1"] + 0.45)))
    # (2) de pé, congelada: ombro, cintura (os vãos já estão no mundo), escápula
    if T["ombro"] <= t < T["sinal3"] + 0.3:
        marcas_de_pe(cv, t, T, F, cam)

    # (3) o olho do "visual"
    a_o = prog(t, T["visual"], T["visual"] + 0.15) * (1 - prog(t, T["olha2"] + 0.1, T["olha2"] + 0.35))
    if a_o > 0:
        olho(cv, 880, 440, 0.72 * e_back(prog(t, T["visual"], T["visual"] + 0.3)), a_o, piscada(t, T["visual"] + 0.45))

    # (4) estirão: calendário de folhas (sem número), no alto à direita
    a_cal = prog(t, T["estirao"] + 0.1, T["estirao"] + 0.3) * (1 - prog(t, F.t_rp - 0.05, F.t_rp + 0.2))
    if a_cal > 0:
        calendario(cv, 824, 380, t, T["estirao"] + 0.1, a_cal, esc=1.85, t_rapido=T["rapido"])

    # efeitos de replay
    varredura(cv, t, lento_k(t, T, F), limpo)
    if not limpo:
        faixas_tracking(cv, t, {"volta": 1.0, "avanca": 0.7}.get(tipo, 0.0))
        if tipo in ("volta", "avanca"):                          # ◀◀ / ▶▶ grande no canto, letreiro do videocassete
            t0 = F.inicio_trecho(t)
            _setas(cv, 96, 410, (0.55 + 0.45 * (math.sin((t - t0) * 16) > -0.3)) * prog(t, t0, t0 + 0.06), 2.2,
                   tipo == "avanca")
        for t0, fo in ((T["lado"], 1.0), (T["ombro"], 0.85), (F.t_rp, 0.4)):
            flash(cv, t, t0, fo)
    cv.restore()
    return cam


# ------------------------------------------------------------------ recapitulação (o "sinal" da 3ª vez)
def momentos(T):
    """Os congelamentos dos 4 sinais: costas na flexão (lado alto + anel), ombros, vãos da cintura, escápula."""
    return (T["escoliose"] + 0.2, T["alto2"] + 0.55, T["torta"] + 0.35, T["saliente"] + 0.45)


def miniatura(T, F, tt):
    """O congelamento do instante `tt`, já desenhado (sem texto)."""
    chave = ("mini", round(tt, 3))
    if chave not in _CACHE:
        sf = skia.Surface(int(CENA.width()), int(CENA.height())); c = sf.getCanvas(); c.clear(_c(BG_OUT))
        c.translate(-CENA.left(), -CENA.top())
        fundo_cl(c, tt)
        monitor(c, tt, T, F, limpo=True)
        _CACHE[chave] = sf.makeImageSnapshot()
    return _CACHE[chave]


MW, MH = 204, 184                                                # miniatura (proporção da CENA)
REC_Y = 872
# A cena AO VIVO atrás da recapitulação e do cartão final (2ª rodada, 01/11). Com a cena só 74% escura e nítida,
# a criança de pé ficava legível atrás de tudo: o carimbo SINAL nos ombros, o NÃO DIAGNÓSTICO na cintura, as
# polaroides no short e nas coxas e o estetoscópio EXATAMENTE sobre a cabeça ("um corpo com um ícone no lugar da
# cabeça"); na CTA, antebraços e mãos saíam acima do título. Agora a cena vira fundo: desfocada E mais escura,
# sem forma de corpo legível atrás dos elementos (as 4 polaroides continuam mostrando a criança inteira).
REC_ESCURO, REC_DESF = 0.92, 16.0                                # recap: escuro (0..1) e sigma do desfoque (px)
CTA_ESCURO, CTA_DESF = 0.5, 12.0                                 # CTA: escuro extra por baixo do véu do cf_comum


def fundo_rec(t, T):
    """0..1: quanto a cena ao vivo está escura e desfocada na recap. Entra no "sinal" e sai no "estirão" um
    pouco DEPOIS dos elementos (polaroides, NÃO DIAGNÓSTICO e estetoscópio somem de 0 a 0,15 s, o SINAL até
    0,1 s; a cena clareia de 0,1 a 0,25 s): nenhum quadro da saída mostra elemento por cima da criança nítida."""
    if t < T["sinal3"] - 0.1:
        return 0.0                                               # já escura quando o SINAL bate (sinal + 0,15 s)
    return prog(t, T["sinal3"] - 0.1, T["sinal3"] + 0.15) * (1 - e_inout(prog(t, T["estirao"] + 0.1, T["estirao"] + 0.25)))


def veu_cena(t, T):
    """-> (sigma do desfoque, escuro extra da CTA) da cena ao vivo no instante t: recap (fundo_rec) e CTA (entra
    com o véu do cf_comum, t_cta = manda - 0,15)."""
    cta = prog(t, T["manda"] - 0.15, T["manda"] + 0.2)
    return max(REC_DESF * fundo_rec(t, T), CTA_DESF * cta), CTA_ESCURO * cta


def monitor_desfocado(cv, t, T, F, sig):
    """O monitor desenhado à parte e desfocado (bordas presas na CENA: sem halo na moldura)."""
    sf = skia.Surface(int(CENA.width()), int(CENA.height())); c = sf.getCanvas(); c.clear(_c(BG_OUT))
    c.translate(-CENA.left(), -CENA.top())
    fundo_cl(c, t)
    monitor(c, t, T, F)
    pf = skia.Paint()
    pf.setImageFilter(skia.ImageFilters.Blur(sig, sig, skia.TileMode.kClamp))
    cv.save(); cv.clipRect(CENA, True)
    cv.drawImage(sf.makeImageSnapshot(), CENA.left(), CENA.top(), skia.SamplingOptions(), pf)
    cv.restore()


def recap(cv, t, T, F):
    """Sem texto nas polaroides: a cena escurece e as 4 entram deslizando; o estetoscópio vem no "leve"."""
    if t < T["sinal3"] - 0.1:
        return
    fim = 1 - e_inout(prog(t, T["estirao"], T["estirao"] + 0.15))
    k_fundo = fundo_rec(t, T)
    if fim <= 0 and k_fundo <= 0:
        return
    cv.save(); cv.clipRect(CENA, True)
    img = _img("escurece", CENA.width(), CENA.height(), lambda c: c.clear(_c(BG_OUT, 255)))
    _blit(cv, img, CENA.left(), CENA.top(), REC_ESCURO * k_fundo)
    for i, tt in enumerate(momentos(T)):
        ti = T["sinal3"] + 0.09 * i
        if t < ti or fim <= 0:
            continue
        k = e_out(prog(t, ti, ti + 0.38))
        a = prog(t, ti, ti + 0.08) * fim
        cx = 540 + (i - 1.5) * 240
        cy = REC_Y + (1 - k) * 330 + (1 - fim) * 60
        giro = (-4.0, 2.5, -2.0, 3.5)[i] * k
        cv.save(); cv.translate(cx, cy); cv.rotate(giro)
        borda = skia.RRect.MakeRectXY(skia.Rect(-MW / 2 - 9, -MH / 2 - 9, MW / 2 + 9, MH / 2 + 9), 12, 12)
        sombra = skia.RRect.MakeRectXY(skia.Rect(-MW / 2 - 3, -MH / 2 + 1, MW / 2 + 15, MH / 2 + 19), 12, 12)
        cv.drawRRect(sombra, paint("#000000", int(110 * a), blur=12))
        cv.drawRRect(borda, paint("#F4F7FA", int(255 * a)))
        dentro = skia.RRect.MakeRectXY(skia.Rect(-MW / 2, -MH / 2, MW / 2, MH / 2), 7, 7)
        cv.save(); cv.clipRRect(dentro, True)
        cv.drawImageRect(miniatura(T, F, tt), skia.Rect(-MW / 2, -MH / 2, MW / 2, MH / 2),
                         skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kNone), _alfa(a))
        cv.restore()
        brilho = 1 - prog(t, ti + 0.1, ti + 0.6)
        if brilho > 0:
            cv.drawRRect(borda, paint(OURO, int(255 * a * brilho), "stroke", 6))
        cv.restore()
    a_e = prog(t, T["leve"], T["leve"] + 0.2) * fim
    if a_e > 0:
        estetoscopio(cv, 540, 452, 1.2 * e_back(prog(t, T["leve"], T["leve"] + 0.3)), a_e)
    cv.restore()


# ------------------------------------------------------------------ quadro
def selo_lenta(cv, lk):
    """Selo da série: SÓ existe com a câmera lenta ligada. (cópia do piloto)"""
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
    sig, esc_cta = veu_cena(t, T)
    if sig > 0.05:                                               # recap e CTA: a cena ao vivo vira fundo
        monitor_desfocado(cv, t, T, F, sig)
    else:
        monitor(cv, t, T, F)
    if esc_cta > 0:
        img = _img("escurece", CENA.width(), CENA.height(), lambda c: c.clear(_c(BG_OUT, 255)))
        _blit(cv, img, CENA.left(), CENA.top(), esc_cta)
    recap(cv, t, T, F)

    fim = 1 - prog(t, T["manda"] - 0.4, T["manda"] - 0.1)
    cantoneiras(cv, fim)
    painel(cv, t, T, F, fim)

    # carimbos (dourados) e o NÃO DIAGNÓSTICO (branco, calmo), todos dentro da área de cena
    carimbo_ouro(cv, R_ALTO, 540, 486, -4, T["alto1"], t, dur=T["costuma"] - T["alto1"] + 0.15)
    # SINAL sai com a recapitulação (até estirão + 0,1 s, ainda com a cena escura); antes o rabo do carimbo ia a
    # estirão + 0,2 s e ficava, apagando, sobre os ombros da criança já nítida
    carimbo_ouro(cv, R_SINAL, 540, 640, -5, T["sinal3"] + 0.15, t, dur=T["estirao"] - T["sinal3"] - 0.05)
    a_n = prog(t, T["nao2"], T["nao2"] + 0.2) * (1 - prog(t, T["estirao"] - 0.05, T["estirao"] + 0.12))
    if a_n > 0:
        texto(cv, R_NAO, 540, 728 + 10 * (1 - e_out(prog(t, T["nao2"], T["nao2"] + 0.25))), F_SEMI, 50, "#FFFFFF",
              int(255 * a_n), contorno=8)
    carimbo_ouro(cv, R_ESTIRAO, 520, 470, -5, T["estirao"] + 0.22, t, dur=F.t_rp - T["estirao"] - 0.12)

    # "Costuma não doer": título branco e calmo ACIMA do monitor (a área do selo está livre no 1×)
    a_d = prog(t, T["costuma"], T["costuma"] + 0.2) * (1 - prog(t, T["olha2"] - 0.3, T["olha2"]))
    if a_d > 0:
        texto(cv, R_DOER, CX, 262 + 12 * (1 - e_out(prog(t, T["costuma"], T["costuma"] + 0.3))), F_BLACK, 58,
              "#FFFFFF", int(255 * a_d), contorno=10)

    capa(cv, t, T["de"], ep["gancho"][0], ep["gancho"][1])
    selo_lenta(cv, lento_k(t, T, F) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface(cv, t, T, blocos, DESTAQUE)


# ------------------------------------------------------------------ som (mix próprio: som.py fica intacto; cópia do piloto)
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
    """Fita correndo: cliques que aceleram + tom que desliza de f0 a f1 + chiado. (cópia do piloto)"""
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
    """Fita voltando: cliques acelerando (0,09 s -> 0,03 s) + chiado que desce."""
    return _fita(dur, 1960, 260, 0.09, 0.82, 77)


def avancar(dur):
    """Fita avançando: cliques rápidos + tom que sobe."""
    return _fita(dur, 380, 1500, 0.07, 0.9, 78) * 0.85


def congelar():
    """Tique seco + 'clac' grave curto (o quadro trava). (cópia do piloto)"""
    SR = som.SR
    y = som.tick() * 1.0
    n = int(0.12 * SR); t = np.arange(n) / SR
    z = np.sin(2 * np.pi * np.cumsum(220 * np.exp(-t * 30) + 90) / SR) * som._env(n, 0.001, 0.03) * 0.5
    out = np.zeros(max(len(y), n)); out[:len(y)] += y; out[:n] += z
    return out


def whoosh_curto():
    return som.whoosh(0.32, seed=11)


def ambiente(dur):
    """Ambiente de quadra MUITO baixo: ar de ginásio (ruído grave filtrado), sem apito nem voz."""
    SR = som.SR
    n = int(dur * SR)
    r = som._noise(n, 91)
    r = _media_movel(r, 160)
    r = r - _media_movel(r, 2400)
    env = np.clip(np.arange(n) / SR / 0.6, 0, 1) * np.clip((dur - np.arange(n) / SR) / 0.6, 0, 1)
    return r / (np.max(np.abs(r)) or 1.0) * env * 0.05


def janelas(T, F, dur):
    """Ganho da batida e da harmonia ao longo do tempo: a batida some na câmera lenta. (cópia do piloto)"""
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
    """= np.convolve(x, np.ones(w) / w, "same"), por soma acumulada. (cópia do piloto)"""
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


def sons(T, F):
    ev = [(0.0, lambda: ambiente(T["manda"]), 1.0),
          (AQ_VIDEO(F, 0) + 0.05, whoosh_curto, 0.28),                           # 1ª flexão (aquecimento)
          (F.t_1x + 0.05, whoosh_curto, 0.3),                                    # a flexão em 1×
          (T["de"], lambda: rebobinar(T["camera"] - T["de"]), 0.9), (T["de"] + 0.05, whoosh_curto, 0.25),
          (T["camera"], "pop", 0.55), (T["lenta"] + 0.03, "shimmer", 0.35),
          (T["lado"], congelar, 1.0), (T["lado"] + 0.02, whoosh_curto, 0.3),
          (T["alto1"], "thump", 0.8), (T["girando"], "whoosh", 0.4),
          (T["costuma"], "pop", 0.4), (T["visual"], "ding", 0.4),
          (T["olha2"] + 0.05, whoosh_curto, 0.3),
          (T["ombro"], congelar, 0.9), (T["alto2"], "tick", 0.5),
          (T["cintura"] - 0.05, whoosh_curto, 0.3), (T["cintura"] + 0.1, "tick", 0.6),
          (T["escapula"] - 0.05, whoosh_curto, 0.3), (T["escapula"] + 0.3, "tick", 0.5),
          (T["sinal3"], "whoosh", 0.45), (T["sinal3"] + 0.2, "thump", 0.8), (T["nao2"], "click", 0.5),
          (T["leve"], "ding", 0.45),
          (T["estirao"], lambda: avancar(F.t_rp - T["estirao"]), 0.7), (T["estirao"] + 0.22, "thump", 0.8),
          (T["rapido"], "shimmer", 0.3),
          (F.t_rp, "click", 0.5), (F.t_rp + 0.02, whoosh_curto, 0.35), (F.t_rp + 0.04, "pop", 0.35),
          (T["manda"] + 0.05, "whoosh", 0.5)]
    ev += [(T["estirao"] + 0.12 + 0.2 * i, "click", 0.6) for i in range(5)]       # folhas virando
    ev += [(T["rapido"] + 0.1 * i, "click", 0.45) for i in range(4)]             # ainda mais depressa
    return ev


def AQ_VIDEO(F, i):
    """Instante de VÍDEO de um ponto do aquecimento (AQUEC[i], em filme)."""
    return F.t_1x + AQUEC[i] / V1


def tempos_previa(T, F):
    return (0.0, 0.35, 0.6, 0.8, 1.1, 1.5, 1.9, F.t_1x + 0.3, F.t_1x + 0.6, F.t_1x + 0.78, T["de"] + 0.3,
            T["camera"] + 0.15, T["camera"] + 0.5, T["lenta"] + 0.3, T["repara"] + 0.2, T["repara"] + 0.6,
            T["lado"] - 0.05, T["lado"] + 0.5, T["alto1"] + 0.6, T["girando"] + 0.8, T["escoliose"] + 0.4,
            T["costuma"] + 0.4, T["costuma"] + 1.0, T["doer"] + 0.8, T["visual"] + 0.3, T["olha2"] + 0.4,
            T["ombro"] + 0.3, T["alto2"] + 0.6, T["cintura"] + 0.4, T["torta"] + 0.4, T["escapula"] + 0.5,
            T["saliente"] + 0.5, T["sinal3"] + 0.2, T["sinal3"] + 0.5, T["nao2"] + 0.4, T["leve"] + 0.5,
            T["ortopedista"] + 0.3, T["estirao"] + 0.1, T["estirao"] + 0.5, T["curva"] + 0.2, T["rapido"] + 0.3,
            F.t_rp + 0.3, F.t_rp + 0.9, T["manda"] - 0.3, T["manda"] + 1.2, T["total"] - 1 / 30)


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
