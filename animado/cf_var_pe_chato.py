# -*- coding: utf-8 -*-
"""CHAMA O VAR — "TÊNIS CARO / CORRIGE PÉ CHATO?" (pé chato na criança: pode ou não pode?).

Série "Chama o VAR" (ter/qui/sáb), construído sobre o piloto cf_chamaovar_rotina_fixador e o cf_var_gesso:
os helpers da série (monitor, selo VAR + chip de estado, telestrador, carimbo de 2 linhas, rebobinar, TV
desligando, busto, apito, sons, legenda karaokê, render com CHECANDO) estão COPIADOS aqui, sem importar
nenhuma outra cena; a perna/pé de criança de perfil parte do cf_cameralenta_ponta_pes (joelho/tubo/canela,
COPIADOS). Contrato de cena do cf_comum (ANCORAS, DESTAQUE, quadro, sons, tempos_previa, render no nível de
cima). Roteiro, fontes e portões: lab/formato_novo/cf_var_pe_chato/storyboard.json.

Lances (o VAR julga o LANCE, nunca a pessoa: o tênis caro e a palmilha entram SOZINHOS em cena):
  1. tênis caro para corrigir pé chato -> ANULADO (pnc_tenis_caro: "Tênis caro NÃO molda nem corrige o pé da
     criança."); JEITO CERTO: tênis simples que protege, sola que dobra, folga de um dedo (marcha-sex);
  2. palmilha para formar o arco -> ANULADO / NÃO MOLDA O ARCO (pnc_pe_chato: "a palmilha NÃO molda esse
     arco"); o X cai na SETA de moldar, nunca na palmilha; flexível e sem dor costuma melhorar sozinho
     (qa_pe_chato_palmilha), mostrado com o calendário e o pé crescendo;
  3. descalço em casa, em piso seguro -> VALIDADO (pnc_tenis_caro; marcha-qua; post33).

O que a cena mostra (a palavra falada comanda o quadro — ANCORAS):
  * quadro 0: o lance 1 JÁ CONGELADO: tênis caro branco-perolado e dourado no chão da entrada de casa (sem
    marca, etiqueta só com moedas), a perna de criança (barra da bermuda amarela no alto) com o pé de PERFIL
    pairando acima com a sola reta, seta pontilhada
    dourada do tênis para o meio do pé (a "promessa de moldar"), círculo de telestrador, ícone de pausa;
    o gancho é o único texto;
  * "VAR": rebobina 0,5 s (o pé sobe) e a câmera abre (prateleira com o tênis simples, caixa, pufe);
    "Tênis": brilho corre o tênis; "caro": a etiqueta balança e a pilha de moedas cresce; "corrigir": o pé
    desce; "pé": a seta se desenha; "chato": a linha da sola acende (encosta inteira); "pode?": congela;
    "Anulado": carimbo; "tênis": os brilhos caem e o dourado apaga; "molda": X âmbar na SETA; "Só": cortina
    do VAR -> o tênis simples no pé, o caro na caixa; "protege": contorno verde; replay sem fala: a sola
    DOBRA na frente (a ponta fica no chão) com o telestrador VERDE na dobra e o visto (sem mão adulta);
  * "Palmilha": o pé sai do tênis simples, que volta para a prateleira; a palmilha cai sozinha VISTA DE CIMA
    (forma de sola de pé, com a cunha do arco) e deita em 3/4 no chão;
    "formar": seta do calombo para o meio do pé; "arco": a linha sob o meio do pé acende; "pode?": congela;
    "Anulado": carimbo ANULADO / NÃO MOLDA O ARCO; "molda": X na SETA; "arco": a palmilha desliza para o
    lado (deitada, sem X); "criança": o pé pousa descalço; "Flexível": os dedinhos mexem; "costuma": calendário vira
    as folhas e o pé cresce; "sozinho": a curvinha do arco aparece, discreta, com contorno verde;
  * "Descalço" (corte, LANCE 3): sala com tapete; a criança anda descalça (só pernas e barra do short);
    "casa": a câmera abre; "piso": varredura ciano rente ao chão; "seguro": contorno verde no piso; "pode?":
    congela no meio do passo; "Validado": carimbo verde, volta a andar; "custa": a etiqueta de moedas do tênis
    caro aparece (e a tampa da caixa se fecha na prateleira); "nada": as moedas pulam fora e a etiqueta fica
    VAZIA; "fortalece": equilíbrio num pé só (o pé de trás sai do chão, joelho dobrado), contorno verde na sola
    de apoio; "pé": visto verde encostado nesse pé;
  * apito final e a TV desliga; "Pé": um pé de perfil num cartão; "dói": zigue-zague âmbar; "durinho": os
    dedos não dobram + cadeado; "chato": o cartão abre para os DOIS pés da MESMA criança (a mesma bermuda),
    um com a curvinha e o outro chato, linha branca nas duas solas; "lado": sinal de DIFERENTE âmbar entre
    as duas solas (marca a diferença, não o pé chato); "Aí": os três sinais juntos (zigue-zague | o par |
    cadeado) sobem e o apito vai ao busto, que acende em "ortopedista"; selo CHAMA O VAR; CTA.
A CRIANÇA aparece sempre do mesmo jeito (perna curta e gordinha, bermuda amarela, barra da camiseta lilás):
nenhuma ponta de perna solta em nenhuma câmera.
Guardrails: pele OPACA de desenho; nenhum osso, exame, pegada, régua, tinta ou medição; nenhum rosto; nenhuma
marca, logo, loja ou número; nenhuma mão adulta em cena; âmbar só em X, círculos, zigue-zague, cadeado,
sinal de diferente e carimbo (vermelho não aparece); ciano = só grafismo do VAR; verde = VALIDADO/JEITO CERTO. Todo
texto desenhado está em ep["tela"]. Cena PRESA ao roteiro pelas palavras-âncora.
"""
import math
import os

import numpy as np
import skia

from . import som, voz as _voz
from .base import codificar, previas as _previas
from .cf_alongamento import (BG_OUT, CX, F_BLACK, F_REG, F_SEMI, H, OURO, W, aviao, clamp, e_back, e_inout,
                             e_out, larg_texto, lerp, lerpc, paint, prog, texto)
from .cf_comum import DISC, SIG
from .cf_fratura_cola import alinhar, comprimir, montar_blocos

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    # lance 1 — tênis caro
    "chama": ("chama", 1, False), "var": ("var", 1, False), "tenis1": ("tênis", 1, False), "caro": ("caro", 1, False),
    "corrigir": ("corrigir", 1, False), "pe1": ("pé", 1, False), "chato1": ("chato", 1, False),
    "pode1": ("pode", 1, False), "anulado1": ("anulado", 1, False), "tenis2": ("tênis", 2, False),
    "molda1": ("molda", 1, False), "pe2": ("pé", 2, False), "so1": ("só", 1, False), "protege": ("protege", 1, False),
    # lance 2 — palmilha
    "palmilha1": ("palmilha", 1, False), "formar": ("formar", 1, False), "arco1": ("arco", 1, False),
    "pode2": ("pode", 2, False), "anulado2": ("anulado", 2, False), "palmilha2": ("palmilha", 2, False),
    "molda2": ("molda", 2, False), "arco2": ("arco", 2, False), "crianca": ("criança", 1, False),
    "flexivel": ("flexível", 1, False),
    "dor": ("dor", 1, False), "costuma": ("costuma", 1, False), "melhorar": ("melhorar", 1, False),
    "sozinho": ("sozinho", 1, False),
    # lance 3 — descalço
    "descalco": ("descalço", 1, False), "casa": ("casa", 1, False), "piso": ("piso", 1, False),
    "seguro": ("seguro", 1, False), "pode3": ("pode", 3, False), "validado": ("validado", 1, False),
    "custa": ("custa", 1, False), "nada": ("nada", 1, False), "fortalece": ("fortalece", 1, False),
    "pe3": ("pé", 3, False),
    # fecho
    "pe4": ("pé", 4, False), "doi": ("dói", 1, False), "durinho": ("durinho", 1, False), "chato2": ("chato", 2, False),
    "lado": ("lado", 1, False), "ai": ("aí", 1, False), "quem": ("quem", 1, False), "apita": ("apita", 1, False),
    "ortopedista": ("ortopedista", 1, False), "manda": ("manda", 1, False),
}
FIM_DE = ("pode1", "pode2", "pode3", "protege", "chato1", "arco2", "sozinho", "seguro", "pe3", "ortopedista")
DESTAQUE = {"var", "caro", "molda", "protege", "palmilha", "arco", "criança", "sozinho", "descalço", "fortalece",
            "durinho", "lado", "ortopedista"}

# rótulos (todos estão em ep["tela"])
T_VAR = "VAR"
T_LANCE = ("LANCE 1", "LANCE 2", "LANCE 3")
T_CHEC = "CHECANDO"
T_ANUL = "ANULADO"
T_ARCO = "NÃO MOLDA O ARCO"
T_VALID = "VALIDADO"
T_CERTO = "JEITO CERTO"
T_SERIE = "CHAMA O VAR"

# ------------------------------------------------------------------ paleta (identidade da série, do piloto)
ARD_IN, ARD_OUT = "#22303F", "#121A24"
CIANO = "#4FD1FF"
VERDE = "#3DDC84"
AMBAR = "#FFA53A"
CARTAO = "#0B1824"
SELO_BG = "#1E2A44"
TEAL = "#5FC4B6"
PELE, PELE_CL, PELE_ESC, PELE_LINHA = "#F0B49A", "#F7CDB8", "#D9937A", "#B9765E"     # criança
SHORT, SHORT_CL, SHORT_ESC, SHORT_LINHA = "#E2AA3C", "#F0C76B", "#BE8A28", "#8E6420"  # short amarelo-mostarda
CAMISETA, CAMISETA_CL, CAMISETA_ESC = "#9B7ED0", "#B9A2E4", "#7558AC"
PAREDE_A, PAREDE_B = "#E4EAF0", "#CBD5DF"
RODAPE = "#F5F7F9"
PISO, PISO_ESC, PISO_CL = "#E2C69A", "#C9A877", "#EED8B4"
PRAT, PRAT_ESC, PRAT_CL = "#C9A57A", "#9C7A52", "#DDBE95"
PUFE, PUFE_ESC, PUFE_CL = "#6F8FAE", "#55728F", "#8EAAC4"
CAIXA, CAIXA_TOPO, CAIXA_ESC, CAIXA_LINHA = "#D9C39D", "#E8D7B5", "#BCA47C", "#9E8760"
SEDA = "#F7ECF0"
PEROLA, PEROLA_CL, PEROLA_ESC, PEROLA_LINHA = "#F3EFE7", "#FFFFFF", "#D3CCBE", "#9E9584"
DOURADO, DOURADO_CL, DOURADO_ESC = "#E2B142", "#F8DC8C", "#A9791A"
LONA, LONA_CL, LONA_ESC, LONA_LINHA = "#86AEDB", "#AAC8EA", "#6489BA", "#46699A"
BORRACHA, BORRACHA_ESC = "#F2EDE3", "#C9BFAE"
PALM, PALM_TOPO, PALM_ESC, PALM_LINHA = "#E4CDA2", "#F6EAD0", "#C7A973", "#6E5330"
MOEDA, MOEDA_CL, MOEDA_LINHA = "#E8B83E", "#FBE39A", "#8E6612"
ETIQ, ETIQ_LINHA = "#FBF6E8", "#B5A98F"
TAPETE, TAPETE_CL, TAPETE_ESC = "#B8B2D6", "#CCC7E4", "#9C95C2"
SOFA, SOFA_CL, SOFA_ESC = "#3F516B", "#566B88", "#2C3A4E"
SETA_OURO = "#F2B544"

# ------------------------------------------------------------------ o monitor (janela da cena) — igual ao piloto
JX0, JY0, JX1, JY1 = 28.0, 300.0, 1052.0, 1226.0
JCX, JCY = (JX0 + JX1) / 2, (JY0 + JY1) / 2
JAN = skia.Rect(JX0, JY0, JX1, JY1)
JAN_R = 26


# ------------------------------------------------------------------ utilidades (cópias do piloto)
def _c(h, a=255):
    h = h.lstrip("#")
    return skia.ColorSetARGB(int(a), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def esc_cor(h, k):
    return lerpc(h, "#000000", k)


def janela(t, t0, t1, d_in=0.25, d_out=0.3):
    return prog(t, t0, t0 + d_in) * (1 - prog(t, t1, t1 + d_out))


def uniao(*ps):
    out = ps[0]
    for q in ps[1:]:
        out = skia.Op(out, q, skia.PathOp.kUnion_PathOp) or out
    return out


def rr_path(x0, y0, x1, y1, r):
    p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), r, r)); return p


def oval_path(x0, y0, x1, y1):
    p = skia.Path(); p.addOval(skia.Rect(x0, y0, x1, y1)); return p


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


def ponta(cv, x, y, ang, tam, cor, a):
    p = skia.Path()
    p.moveTo(x + tam * math.cos(ang), y + tam * math.sin(ang))
    p.lineTo(x + tam * 0.75 * math.cos(ang + 2.45), y + tam * 0.75 * math.sin(ang + 2.45))
    p.lineTo(x + tam * 0.75 * math.cos(ang - 2.45), y + tam * 0.75 * math.sin(ang - 2.45))
    p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))


def _trim(pt, k):
    """Traço desenhado até a fração k (TrimPathEffect devolve None em k = 0). (cópia do piloto)"""
    if k < 0.999:
        pe = skia.TrimPathEffect.Make(0.0, max(0.002, k))
        if pe is not None:
            pt.setPathEffect(pe)
    return pt


def lerp2(p, q, k):
    return (lerp(p[0], q[0], k), lerp(p[1], q[1], k))


def lerp3(p, q, k):
    return tuple(lerp(p[i], q[i], k) for i in range(len(p)))


def _mat(x, y, graus, esc=1.0):
    m = skia.Matrix(); m.setScale(esc, esc); m.postRotate(graus); m.postTranslate(x, y)
    return m


def _transf(p, m):
    q = skia.Path(p); q.transform(m)
    return q


def _mapa(m, x, y):
    q = m.mapXY(x, y)
    return q.x(), q.y()


_CACHE = {}
LINEAR = skia.SamplingOptions(skia.FilterMode.kLinear)


def cacheado(chave, w, h, desenha):
    """Camada estática desenhada uma vez só (o raster do skia aqui é lento para degradês e desfoques)."""
    if chave not in _CACHE:
        sf = skia.Surface(int(w), int(h)); c = sf.getCanvas(); c.clear(skia.ColorTRANSPARENT)
        desenha(c)
        _CACHE[chave] = sf.makeImageSnapshot()
    return _CACHE[chave]


# ------------------------------------------------------------------ câmera
def aplica(cv, cam):
    s, fx, fy = cam[:3]
    cv.translate(JCX, JCY); cv.scale(s, s); cv.translate(-fx, -fy)


def na_tela(cam, x, y):
    s, fx, fy = cam[:3]
    return JCX + (x - fx) * s, JCY + (y - fy) * s


# ================================================================== A PERNA E O PÉ DE CRIANÇA (de perfil)
# Unidades do pé (referencial do tornozelo): x = para os dedos, y = para baixo. A sola fica em y = Y_SOLA.
# Perfil INTERNO (o lado do arco): o arco é a curvinha da sola que não encosta no chão (arco = 0: chato).
Y_SOLA = 48.0
ARCO_MAX = 11.0
J_DEDOS = (70.0, 34.0)                 # onde os dedos dobram
L1, L2 = 205.0, 200.0                  # coxa, perna (unidades do pé)
R_QUAD, R_JOE, R_TOR, BOJO = 50.0, 37.0, 22.0, 7.0
# proporção de CRIANÇA (revisão): perna mais curta (LK) e mais gordinha (GK) em TODOS os lances, a mesma
# bermuda amarela (BARRA = comprimento da bermuda ao longo da coxa) — o mesmo menino do começo ao fim
LK, GK, BARRA = 0.86, 1.12, 150.0


def pe_tras_path(arco):
    a = ARCO_MAX * clamp(arco, 0.0, 1.2)
    p = skia.Path()
    y = Y_SOLA
    p.moveTo(12, -20)
    p.cubicTo(30, -16, 46, -8, 58, 4)                         # dorso redondo (gordinho)
    p.cubicTo(65, 11, 71, 17, 76, 21)
    p.lineTo(78, y - 6)
    p.cubicTo(75, y - 1, 70, y, 64, y)                        # bola do pé
    p.cubicTo(52, y, 44, y - a, 28, y - a)                    # sola: o arco (a = 0: encosta inteira)
    p.cubicTo(13, y - a, 5, y - a * 0.3, -6, y)
    p.cubicTo(-20, y + 1, -30, y - 5, -31, y - 18)            # calcanhar redondo
    p.cubicTo(-32, y - 32, -27, y - 44, -22, -6)
    p.lineTo(-20, -20)
    p.cubicTo(-8, -25, 2, -25, 12, -20)
    p.close()
    return p


def sola_pts(arco, n=24):
    """Pontos da linha da sola, do calcanhar à bola (para a luz branca e o contorno verde)."""
    a = ARCO_MAX * clamp(arco, 0.0, 1.2)
    pts = []
    for i in range(n + 1):
        u = i / n
        x = lerp(-10, 66, u)
        b = math.exp(-((x - 28) / 25.0) ** 2)
        pts.append((x, Y_SOLA - a * b))
    return pts


DEDAO = capsula((0, 0), (21, 1.5), 28, 25)                   # dedão gordinho (pé de criança)
DEDINHO1 = capsula((-2, -6), (16, -6), 18, 16)               # o dedinho de trás espiando por cima
DEDINHO2 = capsula((-6, -9), (6, -9), 14, 12)


def joelho(hx, hy, ax, ay, l1, l2):
    """Cinemática inversa de dois segmentos; o joelho dobra para a frente (+x). (cópia do piloto da câmera lenta)"""
    dx, dy = ax - hx, ay - hy
    d = max(1.0, min(math.hypot(dx, dy), l1 + l2 - 0.5))
    fi = math.atan2(dy, dx)
    al = math.acos(clamp((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d), -1.0, 1.0))
    return hx + l1 * math.cos(fi - al), hy + l1 * math.sin(fi - al)


def tubo(x0, y0, r0, x1, y1, r1):
    L = math.hypot(x1 - x0, y1 - y0) or 1.0
    nx, ny = -(y1 - y0) / L, (x1 - x0) / L
    p = skia.Path()
    p.moveTo(x0 + nx * r0, y0 + ny * r0); p.lineTo(x1 + nx * r1, y1 + ny * r1)
    p.lineTo(x1 - nx * r1, y1 - ny * r1); p.lineTo(x0 - nx * r0, y0 - ny * r0); p.close()
    c0 = skia.Path(); c0.addCircle(x0, y0, r0)
    c1 = skia.Path(); c1.addCircle(x1, y1, r1)
    return uniao(p, c0, c1)


def canela(kx, ky, ax, ay, rj, rt, bojo):
    """Perna do joelho ao tornozelo, gordinha: frente quase reta, panturrilha levemente abaulada. (cópia)"""
    L = math.hypot(ax - kx, ay - ky) or 1.0
    ux, uy = (ax - kx) / L, (ay - ky) / L
    nx, ny = uy, -ux

    def P(a, b):
        return kx + ux * a + nx * b, ky + uy * a + ny * b
    p = skia.Path()
    p.moveTo(*P(0, rj))
    p.cubicTo(*P(0.35 * L, rj * 0.95), *P(0.72 * L, rt * 1.12), *P(L, rt))
    p.lineTo(*P(L, -rt))
    p.cubicTo(*P(0.80 * L, -rt * 1.1), *P(0.58 * L, -(rj + bojo)), *P(0.36 * L, -(rj + bojo)))
    p.cubicTo(*P(0.18 * L, -(rj + bojo)), *P(0.04 * L, -rj * 1.02), *P(0, -rj))
    p.close()
    c0 = skia.Path(); c0.addCircle(kx, ky, rj)
    c1 = skia.Path(); c1.addCircle(ax, ay, rt)
    return uniao(p, c0, c1)


class Pe:
    """Pose de um pé: tornozelo (mundo), inclinação (graus), dedos (graus: + dobra para baixo, - abre para
    cima), arco (0 chato .. 1 curvinha), escala (unidades do pé -> mundo)."""
    __slots__ = ("ax", "ay", "inc", "dedos", "arco", "esc")

    def __init__(self, ax, ay, inc=0.0, dedos=0.0, arco=0.0, esc=1.25):
        self.ax, self.ay, self.inc, self.dedos, self.arco, self.esc = ax, ay, inc, dedos, arco, esc

    def m(self):
        return _mat(self.ax, self.ay, self.inc, self.esc)

    def ponto(self, x, y):
        return _mapa(self.m(), x, y)

    def m_dedos(self):
        m = skia.Matrix(); m.setRotate(self.dedos); m.postTranslate(*J_DEDOS); m.postConcat(self.m())
        return m


def pe_paths(pe):
    """(contorno do pé com o dedão, dedinhos de trás) no mundo."""
    tras = _transf(pe_tras_path(pe.arco), pe.m())
    md = pe.m_dedos()
    return uniao(tras, _transf(DEDAO, md)), (_transf(DEDINHO1, md), _transf(DEDINHO2, md))


def perna(cv, hip, pe, longe=False, claro=0.0, a=1.0, so_pe=False):
    """Perna de criança num contorno só (coxa + perna + pé), pele lisa e OPACA, sombreado por faixas (cópia
    adaptada do cf_cameralenta_ponta_pes), na proporção de criança (LK, GK). Devolve (joelho, contorno)."""
    s = pe.esc
    hx, hy = hip
    kx, ky = joelho(hx, hy, pe.ax, pe.ay, L1 * LK * s, L2 * LK * s)
    pe_c, dinhos = pe_paths(pe)
    g = GK * s
    if so_pe:
        corpo = uniao(canela(pe.ax - 4 * s, pe.ay - 420 * s, pe.ax, pe.ay, R_TOR * 1.35 * g, R_TOR * g, BOJO * g), pe_c)
    else:
        corpo = uniao(tubo(hx, hy, R_QUAD * g, kx, ky, R_JOE * g), canela(kx, ky, pe.ax, pe.ay, R_JOE * g, R_TOR * g, BOJO * g),
                      pe_c)
    f_esc = 0.34 * (1 - claro)
    esc = (lambda c: lerpc(c, "#2A1B16", f_esc)) if longe else (lambda c: c)
    aa = int(255 * a)
    # dedinhos de trás (um tom abaixo), atrás do dedão
    for k, dp in enumerate(dinhos):
        cv.drawPath(dp, paint(esc(lerpc(PELE, "#C98068", 0.25 + 0.12 * k)), aa))
        cv.drawPath(dp, paint(PELE_LINHA, int(200 * a), "stroke", 2.2 * s))
    cv.save(); cv.clipPath(corpo, skia.ClipOp.kIntersect, True)
    cv.drawPath(corpo, paint(esc(PELE), aa))
    for larg, cor in ((30, "#EDB197"), (18, "#E5A78B"), (8, "#DA9A80")):        # volume: aro mais escuro (opaco)
        cv.drawPath(corpo, paint(esc(cor), aa, "stroke", larg * s))
    luz = paint(esc("#F5C4AB"), aa, "stroke", 12 * s)
    if not so_pe:
        cv.drawLine(kx + 10 * s, ky + 16 * s, lerp(kx, pe.ax, 0.62) + 9 * s, lerp(ky, pe.ay, 0.62), luz)
    a0 = pe.ponto(10, -6); a1 = pe.ponto(44, 6)
    cv.drawLine(a0[0], a0[1], a1[0], a1[1], paint(esc("#F5C4AB"), aa, "stroke", 9 * s))
    dob = skia.Path(); dob.moveTo(-6, -22); dob.quadTo(8, -21, 14, -10)          # dobrinha do tornozelo (bebê)
    cv.drawPath(_transf(dob, pe.m()), paint(esc(PELE_LINHA), int(140 * a), "stroke", 2.6 * s))
    md = pe.m_dedos()
    p0 = _mapa(md, 2, -12); p1 = _mapa(md, 4, 8)
    cv.drawLine(p0[0], p0[1], p1[0], p1[1], paint(PELE_LINHA, int(110 * a), "stroke", 2.2 * s))
    cv.restore()
    cv.drawPath(corpo, paint(PELE_LINHA, int(230 * a), "stroke", 3.2 * s))
    return (kx, ky), corpo


def manga_short(hip, joe, s):
    """Barra do short no referencial da coxa: larga e evasê (roupa de criança). (cópia adaptada)"""
    hx, hy = hip; kx, ky = joe
    L = math.hypot(kx - hx, ky - hy) or 1.0
    ux, uy = (kx - hx) / L, (ky - hy) / L; nx, ny = -uy, ux
    d = BARRA * LK * s
    ex, ey = hx + ux * d, hy + uy * d
    g = GK * s                                         # a bermuda acompanha a coxa gordinha
    p = skia.Path()
    p.moveTo(hx + nx * 54 * g, hy + ny * 54 * g); p.lineTo(ex + nx * 62 * g, ey + ny * 62 * g)
    p.quadTo(ex + ux * 6 * s, ey + uy * 6 * s, ex - nx * 62 * g, ey - ny * 62 * g)
    p.lineTo(hx - nx * 54 * g, hy - ny * 54 * g); p.close()
    c = skia.Path(); c.addCircle(hx, hy, 54 * g)
    bainha = ((ex + nx * 59 * g - ux * 13 * s, ey + ny * 59 * g - uy * 13 * s),
              (ex - nx * 59 * g - ux * 13 * s, ey - ny * 59 * g - uy * 13 * s))
    return uniao(p, c), bainha, (ux, uy, nx, ny)


def short_perna(cv, hip, joe, s, longe=False):
    m, b, e = manga_short(hip, joe, s)
    cor = (lambda c: lerpc(c, "#2A1B16", 0.25)) if longe else (lambda c: c)
    cv.drawPath(m, paint("#000000", 50, blur=8))
    cv.drawPath(m, paint(cor(SHORT)))
    cv.save(); cv.clipPath(m, skia.ClipOp.kIntersect, True)
    ux, uy, nx, ny = e
    cv.drawLine(b[0][0] + ux * 9 * s, b[0][1] + uy * 9 * s, b[1][0] + ux * 9 * s, b[1][1] + uy * 9 * s,
                paint(cor(SHORT_CL), 255, "stroke", 15 * s))
    cv.drawLine(hip[0] + nx * 30 * s, hip[1] + ny * 30 * s, b[0][0] - ux * 30 * s, b[0][1] - uy * 30 * s,
                paint(cor(SHORT_CL), 120, "stroke", 10 * s))
    cv.restore()
    cv.drawPath(m, paint(SHORT_LINHA, 220, "stroke", 3.6 * s))
    cv.drawLine(b[0][0], b[0][1], b[1][0], b[1][1], paint(SHORT_LINHA, 150, "stroke", 3.4 * s))


def corpo_baixo(cv, hip, s):
    """Cintura do short + barra da camiseta lilás por cima (a criança continua para cima, fora do quadro)."""
    hx, hy = hip
    p = skia.Path()
    p.moveTo(hx - 70 * s, hy - 92 * s); p.lineTo(hx + 62 * s, hy - 92 * s)
    p.cubicTo(hx + 72 * s, hy - 40 * s, hx + 68 * s, hy + 6 * s, hx + 54 * s, hy + 30 * s)
    p.lineTo(hx - 42 * s, hy + 34 * s)
    p.cubicTo(hx - 88 * s, hy + 18 * s, hx - 92 * s, hy - 40 * s, hx - 70 * s, hy - 92 * s)
    p.close()
    cv.drawPath(p, paint("#000000", 50, blur=8))
    cv.drawPath(p, paint(SHORT))
    cv.drawPath(p, paint(SHORT_LINHA, 220, "stroke", 3.6 * s))
    cam = rr_path(hx - 100 * s, hy - 420 * s, hx + 92 * s, hy - 70 * s, 26 * s)
    cv.drawPath(cam, paint("#000000", 60, blur=10))
    sh = skia.GradientShader.MakeLinear([skia.Point(hx - 100 * s, 0), skia.Point(hx + 92 * s, 0)],
                                        [_c(CAMISETA_ESC), _c(CAMISETA), _c(CAMISETA_CL), _c(CAMISETA)], [0, 0.3, 0.6, 1])
    cv.drawPath(cam, paint(CAMISETA, shader=sh))
    cv.drawLine(hx - 96 * s, hy - 84 * s, hx + 88 * s, hy - 84 * s, paint(CAMISETA_ESC, 200, "stroke", 4 * s))
    cv.drawPath(cam, paint(esc_cor(CAMISETA_ESC, 0.3), 220, "stroke", 3.4 * s))


# ================================================================== O TÊNIS (de perfil, no referencial do pé)
ESP = {"caro": 24.0, "simples": 12.0}           # espessura do solado
BOLA_X = 66.0                                   # onde a sola dobra
SHOE_DY = Y_SOLA - 60.0                         # o tênis foi desenhado para a sola em 60: desce junto


def sola_y(tipo):
    return 52.0 + ESP[tipo] + SHOE_DY


def _cabedal():
    p = skia.Path()
    p.moveTo(-36, -6)
    p.cubicTo(-46, 2, -50, 28, -48, 56)
    p.lineTo(114, 56)
    p.cubicTo(126, 54, 128, 40, 119, 32)
    p.cubicTo(110, 24, 96, 19, 82, 15)
    p.cubicTo(64, 9, 46, -2, 31, -14)
    p.cubicTo(29, -24, 19, -29, 13, -20)
    p.cubicTo(6, -6, -12, -1, -22, -5)
    p.cubicTo(-28, -7, -33, -8, -36, -6)
    p.close()
    return p


def _abertura():
    p = skia.Path()
    p.moveTo(-36, -6)
    p.cubicTo(-26, -19, 0, -26, 13, -20)
    p.cubicTo(6, -6, -12, -1, -22, -5)
    p.cubicTo(-28, -7, -33, -8, -36, -6)
    p.close()
    return p


CABEDAL, ABERTURA = _cabedal(), _abertura()
LACO_LINHA = ((33, -10), (78, 11))            # linha do cadarço (do colarinho à ponta)


def _solado(tipo):
    return rr_path(-52, 50, 132, 52.0 + ESP[tipo], min(11.0, ESP[tipo] * 0.5))      # (referencial do desenho)


def brilho4(cv, x, y, r, a, cor=DOURADO_CL):
    """Brilho de 4 pontas (sem texto)."""
    if a <= 0 or r <= 0:
        return
    p = skia.Path()
    p.moveTo(x, y - r); p.quadTo(x + r * 0.16, y - r * 0.16, x + r, y); p.quadTo(x + r * 0.16, y + r * 0.16, x, y + r)
    p.quadTo(x - r * 0.16, y + r * 0.16, x - r, y); p.quadTo(x - r * 0.16, y - r * 0.16, x, y - r); p.close()
    cv.drawPath(p, paint(DOURADO_ESC, int(150 * a), "stroke", 4))
    cv.drawPath(p, paint(cor, int(255 * a)))
    cv.drawCircle(x, y, r * 0.18, paint("#FFFFFF", int(255 * a)))


def tenis_fundo(cv, m, tipo, a=1.0):
    """O lado de dentro (a abertura escura): vai ANTES da perna."""
    if a <= 0:
        return
    cv.save(); cv.concat(m); cv.translate(0, SHOE_DY)
    cv.drawPath(ABERTURA, paint("#3B332F" if tipo == "caro" else "#2E3A4C", int(255 * a)))
    rim = skia.Path(); rim.moveTo(-36, -6); rim.cubicTo(-26, -19, 0, -26, 13, -20)
    cv.drawPath(rim, paint(PEROLA_ESC if tipo == "caro" else LONA_ESC, int(255 * a), "stroke", 4))
    cv.restore()


def tenis_frente(cv, m, tipo, a=1.0, dour=1.0, brilho=-1.0, verde=0.0, vazio=False, clip_x=None):
    """Cabedal + solado + detalhes, no referencial do pé (`m`). Sem marca, sem logo, sem letra.
    `dour`: força do dourado (apaga no ANULADO); `brilho`: faixa de luz correndo (0..1); `verde`: contorno do
    JEITO CERTO; `clip_x`: (x0, x1) desenha só essa fatia (a sola que dobra)."""
    if a <= 0:
        return
    aa = int(255 * a)
    cv.save(); cv.concat(m)
    if clip_x is not None:
        cv.clipRect(skia.Rect(clip_x[0], -200, clip_x[1], 200), skia.ClipOp.kIntersect, True)
    cv.translate(0, SHOE_DY)
    sol = _solado(tipo)
    yb = sola_y(tipo) - SHOE_DY
    if clip_x is None:                       # na sola que dobra, a sombra é desenhada uma vez só, inteira
        cv.drawOval(skia.Rect(-60, yb - 8, 142, yb + 12), paint("#000000", int(70 * a), blur=10))
    if verde > 0:
        cv.drawPath(uniao(CABEDAL, sol), paint(VERDE, int(140 * verde * a), "stroke", 22, blur=8))
    if vazio:
        cv.drawPath(ABERTURA, paint("#3B332F" if tipo == "caro" else "#2E3A4C", aa))
        rim = skia.Path(); rim.moveTo(-36, -6); rim.cubicTo(-26, -19, 0, -26, 13, -20)
        cv.drawPath(rim, paint(PEROLA_ESC if tipo == "caro" else LONA_ESC, aa, "stroke", 4))
        cv.drawPath(poli([(-30, -8), (-8, -16), (10, -19), (6, -11), (-14, -5)]), paint("#000000", int(60 * a), blur=3))
    if tipo == "caro":
        ouro = lerpc(DOURADO, "#CFC6B4", 1 - dour)
        ouro_cl = lerpc(DOURADO_CL, "#E6E0D4", 1 - dour)
        sh = skia.GradientShader.MakeLinear([skia.Point(0, -30), skia.Point(0, 56)],
                                            [_c(PEROLA_CL), _c(PEROLA), _c(PEROLA_ESC)], [0.0, 0.55, 1.0])
        cv.drawPath(CABEDAL, paint(PEROLA, aa, shader=sh))
        cv.save(); cv.clipPath(CABEDAL, skia.ClipOp.kIntersect, True)
        painel = skia.Path(); painel.moveTo(-50, 26); painel.cubicTo(10, 18, 54, 30, 100, 58); painel.lineTo(-50, 58)
        painel.close()
        cv.drawPath(painel, paint(PEROLA_ESC, int(120 * a)))
        cv.drawLine(-50, 25, 100, 57, paint(ouro, aa, "stroke", 3))
        cv.drawRect(skia.Rect(-60, 44, 160, 56), paint(ouro, aa))                    # faixa dourada junto do solado
        cv.drawLine(-60, 45, 160, 45, paint(ouro_cl, aa, "stroke", 2.5))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-56, -10, -40, 26), 6, 6), paint(ouro, aa))   # aba do calcanhar
        if 0 < brilho < 1:
            x = lerp(-80, 170, brilho)
            g = skia.GradientShader.MakeLinear([skia.Point(x - 40, 0), skia.Point(x + 40, 0)],
                                               [_c("#FFFFFF", 0), _c("#FFF6D8", 235), _c("#FFFFFF", 0)])
            cv.drawRect(skia.Rect(x - 40, -40, x + 40, 80), paint("#FFFFFF", aa, shader=g))
        cv.restore()
        cv.drawPath(CABEDAL, paint(PEROLA_LINHA, aa, "stroke", 2.4))
        rim = skia.Path(); rim.moveTo(13, -20); rim.cubicTo(6, -6, -12, -1, -22, -5); rim.cubicTo(-28, -7, -33, -8, -36, -6)
        cv.drawPath(rim, paint(ouro, aa, "stroke", 4))
        # cadarço branco e ilhoses dourados
        for i in range(4):
            k = 0.12 + 0.24 * i
            x, y = lerp2(LACO_LINHA[0], LACO_LINHA[1], k)
            cv.drawLine(x - 7, y - 9, x + 9, y + 5, paint("#FFFFFF", aa, "stroke", 5))
            cv.drawLine(x - 7, y - 9, x + 9, y + 5, paint(PEROLA_LINHA, int(140 * a), "stroke", 1.2))
            cv.drawCircle(x + 6, y + 9, 3.6, paint(ouro, aa))
        # solado alto, branco e brilhante, com friso dourado
        sh2 = skia.GradientShader.MakeLinear([skia.Point(0, 50), skia.Point(0, yb)], [_c("#FFFFFF"), _c("#E8E3D9")])
        cv.drawPath(sol, paint("#FFFFFF", aa, shader=sh2))
        cv.drawLine(-48, 50 + ESP["caro"] * 0.55, 128, 50 + ESP["caro"] * 0.55, paint(ouro, aa, "stroke", 3))
        cv.drawLine(-40, 54, 118, 54, paint("#FFFFFF", int(200 * a), "stroke", 3))
        cv.drawPath(sol, paint(PEROLA_LINHA, aa, "stroke", 2.4))
    else:
        sh = skia.GradientShader.MakeLinear([skia.Point(0, -30), skia.Point(0, 56)],
                                            [_c(LONA_CL), _c(LONA), _c(LONA_ESC)], [0.0, 0.5, 1.0])
        cv.drawPath(CABEDAL, paint(LONA, aa, shader=sh))
        cv.save(); cv.clipPath(CABEDAL, skia.ClipOp.kIntersect, True)
        for xx in range(-50, 150, 9):                                              # trama da lona (bem leve)
            cv.drawLine(xx, -40, xx + 30, 60, paint(LONA_CL, int(40 * a), "stroke", 1.4))
        bico = oval_path(92, 20, 156, 92)                                           # biqueira de borracha
        cv.drawPath(bico, paint(BORRACHA, aa))
        cv.drawPath(bico, paint(BORRACHA_ESC, aa, "stroke", 2.4))
        cv.drawRect(skia.Rect(-60, 45, 160, 56), paint(BORRACHA, aa))
        cv.drawLine(-60, 45, 160, 45, paint(BORRACHA_ESC, aa, "stroke", 2))
        cv.restore()
        cv.drawPath(CABEDAL, paint(LONA_LINHA, aa, "stroke", 2.4))
        for i in range(4):
            k = 0.12 + 0.24 * i
            x, y = lerp2(LACO_LINHA[0], LACO_LINHA[1], k)
            cv.drawLine(x - 7, y - 9, x + 9, y + 5, paint("#FFFFFF", aa, "stroke", 5))
            cv.drawCircle(x + 6, y + 9, 3.4, paint("#8C98A6", aa))
        sh2 = skia.GradientShader.MakeLinear([skia.Point(0, 50), skia.Point(0, yb)], [_c(BORRACHA), _c("#DDD5C6")])
        cv.drawPath(sol, paint(BORRACHA, aa, shader=sh2))
        cv.drawLine(-48, 57, 128, 57, paint(BORRACHA_ESC, int(200 * a), "stroke", 2))
        cv.drawPath(sol, paint(BORRACHA_ESC, aa, "stroke", 2.4))
    if verde > 0:
        cv.drawPath(uniao(CABEDAL, sol), paint(VERDE, int(255 * verde * a), "stroke", 6))
    cv.restore()


def etiqueta(cv, m, ang, n_moedas, a=1.0, pulo=0.0):
    """Etiqueta pendurada na aba do calcanhar: cartão claro com a pilha de moedas (sem número, sem cifrão)."""
    if a <= 0:
        return
    aa = int(255 * a)
    cv.save(); cv.concat(m); cv.translate(0, SHOE_DY)
    px, py = -50, -2
    cv.save(); cv.translate(px, py); cv.rotate(ang)
    cv.drawLine(0, 0, -16, 36, paint("#8C8172", aa, "stroke", 2.2))
    cv.translate(-16, 36); cv.rotate(-10)
    card = rr_path(-24, 0, 24, 62, 8)
    cv.drawPath(card, paint("#000000", int(60 * a), blur=6))
    cv.drawPath(card, paint(ETIQ, aa))
    cv.drawPath(card, paint(ETIQ_LINHA, aa, "stroke", 2.2))
    cv.drawCircle(0, 8, 3.4, paint(ETIQ_LINHA, aa))
    n = int(n_moedas)
    base = 52 - 4 * pulo
    for i in range(n):
        y = base - i * 8.5
        cv.drawOval(skia.Rect(-14, y - 5, 14, y + 5), paint(MOEDA_LINHA, aa))
        cv.drawOval(skia.Rect(-13, y - 6.5, 13, y + 2.5), paint(MOEDA, aa))
        cv.drawOval(skia.Rect(-13, y - 6.5, 13, y + 2.5), paint(MOEDA_LINHA, aa, "stroke", 1.6))
        if i == n - 1:
            cv.drawOval(skia.Rect(-7, y - 5, 3, y - 1.5), paint(MOEDA_CL, aa))
    cv.restore()
    cv.restore()


def etiqueta_vazia(cv, x, y, esc, a, t, t_nada):
    """A etiqueta do tênis caro (cartão claro com a pilha de moedas, sem número, sem cifrão) solta no quadro:
    em "nada" as moedas pulam fora uma a uma e somem; fica a etiqueta VAZIA (não custa nada)."""
    if a <= 0:
        return
    aa = int(255 * a)
    cv.save(); cv.translate(x, y); cv.rotate(-8 + 3 * math.sin(t * 3)); cv.scale(esc, esc)
    cv.drawLine(0, -12, 0, -30, paint("#8C8172", aa, "stroke", 2.2))
    card = rr_path(-24, -12, 24, 50, 8)
    cv.drawPath(card, paint("#000000", int(70 * a), blur=6))
    cv.drawPath(card, paint(ETIQ, aa))
    cv.drawPath(card, paint(ETIQ_LINHA, aa, "stroke", 2.2))
    cv.drawCircle(0, -4, 3.4, paint(ETIQ_LINHA, aa))
    for i in range(4):
        base = 40 - i * 8.5
        k = prog(t, t_nada + 0.07 * (3 - i), t_nada + 0.07 * (3 - i) + 0.32)       # a de cima sai primeiro
        if k >= 1:
            continue
        dx = (22 if i % 2 else -22) * k
        yy = base - 70 * math.sin(math.pi * 0.5 * k) + 30 * k * k
        am = int(255 * a * (1 - k))
        cv.drawOval(skia.Rect(-14 + dx, yy - 5, 14 + dx, yy + 5), paint(MOEDA_LINHA, am))
        cv.drawOval(skia.Rect(-13 + dx, yy - 6.5, 13 + dx, yy + 2.5), paint(MOEDA, am))
        cv.drawOval(skia.Rect(-13 + dx, yy - 6.5, 13 + dx, yy + 2.5), paint(MOEDA_LINHA, am, "stroke", 1.6))
    cv.restore()


def palmilha_path():
    """Palmilha de perfil com o calombo alto no meio (referencial próprio: base no chão, y = 0)."""
    p = skia.Path()
    p.moveTo(-40, 0)
    p.lineTo(106, 0)
    p.cubicTo(116, 0, 117, -10, 106, -10)
    p.lineTo(64, -10)
    p.cubicTo(50, -10, 44, -36, 28, -36)
    p.cubicTo(12, -36, 6, -13, -10, -13)
    p.lineTo(-30, -14)
    p.cubicTo(-38, -15, -44, -24, -48, -18)
    p.cubicTo(-50, -9, -46, 0, -40, 0)
    p.close()
    return p


PALMILHA = palmilha_path()
TOPO_CALOMBO = (28.0, -36.0)


def _sola_topo():
    """Contorno da palmilha VISTA DE CIMA (forma de sola de pé: calcanhar estreito, cintura do arco, antepé largo
    e ponta redonda). Eixo x = do calcanhar à ponta; v = 0 na borda de DENTRO (a do arco), v < 0 para fora."""
    p = skia.Path()
    p.moveTo(-40, -6)
    p.cubicTo(-10, -2, 6, -15, 30, -15)          # borda de dentro: a cintura do arco
    p.cubicTo(54, -15, 70, -1, 92, -1)
    p.cubicTo(112, -1, 120, -20, 116, -36)       # a ponta
    p.cubicTo(112, -56, 92, -64, 72, -64)
    p.cubicTo(40, -64, 6, -50, -22, -48)         # borda de fora
    p.cubicTo(-46, -46, -54, -34, -54, -24)      # o calcanhar
    p.cubicTo(-54, -12, -50, -7, -40, -6)
    p.close()
    return p


SOLA_TOPO = _sola_topo()


def palmilha(cv, x, y, esc, a=1.0, rot=0.0, verde=0.0, q=0.36):
    """Palmilha de 3/4: a placa com FORMA DE SOLA DE PÉ vista um pouco de cima (q = achatamento: 1 = vista de
    cima, na queda) e, na borda da frente, o calombo do arco de perfil."""
    if a <= 0:
        return
    aa = int(255 * a)
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(esc, esc)
    cv.drawOval(skia.Rect(-54, -5, 118, 9), paint("#000000", int(70 * a), blur=6))
    # a placa (o tampo da palmilha) com a forma de sola, achatada pela perspectiva
    cv.save(); cv.translate(0, -9); cv.scale(1.0, q)
    sh = skia.GradientShader.MakeLinear([skia.Point(0, -64), skia.Point(0, 0)], [_c(PALM_TOPO), _c(PALM)])
    cv.drawPath(SOLA_TOPO, paint(PALM_ESC, aa))
    cv.translate(0, -4 / max(q, 0.2))
    cv.drawPath(SOLA_TOPO, paint(PALM_TOPO, aa, shader=sh))
    cv.drawPath(SOLA_TOPO, paint(PALM_LINHA, aa, "stroke", 3.0 / max(q, 0.3)))
    # costura em volta (palmilha de verdade)
    cv.save(); cv.clipPath(SOLA_TOPO, skia.ClipOp.kIntersect, True)
    pc = paint(PALM_ESC, int(170 * a), "stroke", 2.0 / max(q, 0.3))
    pc.setPathEffect(skia.DashPathEffect.Make([7.0, 6.0], 0.0))
    m_in = skia.Matrix(); m_in.setScale(0.9, 0.82, 30, -32)
    cv.drawPath(_transf(SOLA_TOPO, m_in), pc)
    cv.drawOval(skia.Rect(2, -30, 60, -6), paint(PALM_ESC, int(110 * a), blur=4))       # a cunha do arco
    cv.drawOval(skia.Rect(10, -26, 50, -12), paint(PALM_TOPO, int(150 * a), blur=3))
    cv.restore()
    cv.restore()
    if q > 0.8:                                   # vista de cima: o calombo do arco é só uma cunha marcada
        cv.restore()
        return
    sh = skia.GradientShader.MakeLinear([skia.Point(0, -36), skia.Point(0, 0)], [_c(PALM_TOPO), _c(PALM), _c(PALM_ESC)],
                                        [0.0, 0.55, 1.0])
    cv.drawPath(PALMILHA, paint(PALM, aa, shader=sh))
    cv.save(); cv.clipPath(PALMILHA, skia.ClipOp.kIntersect, True)
    cv.drawRect(skia.Rect(-60, -4, 130, 2), paint(PALM_ESC, aa))                    # a borda de baixo (espessura)
    cv.restore()
    top = skia.Path(); top.moveTo(106, -10); top.lineTo(64, -10); top.cubicTo(50, -10, 44, -36, 28, -36)
    top.cubicTo(12, -36, 6, -13, -10, -13); top.lineTo(-30, -14)
    cv.drawPath(top, paint("#FFF6E2", aa, "stroke", 3.4))
    cv.drawPath(PALMILHA, paint(PALM_LINHA, aa, "stroke", 3.2))
    cv.restore()


def caixa(cv, x0, yb, w, h, a=1.0, conteudo=None):
    """Caixa lisa de sapato (sem texto), aberta: fundo, papel de seda, conteúdo, frente; a tampa encostada no
    lado direito. `conteudo(cv)`: o que está dentro (desenhado entre o fundo e a frente)."""
    aa = int(255 * a)
    x1 = x0 + w; yt = yb - h; dp = 16
    cv.drawRect(skia.Rect(x0 + 6, yb - 6, x1 + 40, yb + 10), paint("#000000", int(60 * a), blur=10))
    # a tampa, em pé, encostada no lado direito
    cv.save(); cv.translate(x1 + dp + 34, yb + 2); cv.rotate(-104)
    tampa_r = skia.Rect(0, -16, w + 8, 4)
    cv.drawRect(tampa_r, paint(CAIXA_TOPO, aa)); cv.drawRect(tampa_r, paint(CAIXA_LINHA, aa, "stroke", 2.4))
    cv.drawLine(4, -4, w + 4, -4, paint(CAIXA_ESC, aa, "stroke", 2))
    cv.restore()
    cv.drawPath(poli([(x0, yt), (x0 + dp, yt - dp * 0.7), (x1 + dp, yt - dp * 0.7), (x1, yt)]), paint("#6E5D45", aa))
    cv.drawPath(poli([(x1, yt), (x1 + dp, yt - dp * 0.7), (x1 + dp, yb - dp * 0.7), (x1, yb)]), paint(CAIXA_ESC, aa))
    cv.drawRect(skia.Rect(x0 + 8, yt - 26, x1 - 8, yt + 6), paint(SEDA, aa))      # papel de seda
    for i in range(4):
        xx = lerp(x0 + 14, x1 - 20, i / 3)
        cv.drawLine(xx, yt - 24, xx + 12, yt + 4, paint("#E4CFD8", aa, "stroke", 2))
    if conteudo is not None:
        conteudo(cv)
    sh = skia.GradientShader.MakeLinear([skia.Point(0, yt), skia.Point(0, yb)], [_c(CAIXA_TOPO), _c(CAIXA)])
    cv.drawRect(skia.Rect(x0, yt, x1, yb), paint(CAIXA, aa, shader=sh))
    cv.drawRect(skia.Rect(x0, yt, x1, yb), paint(CAIXA_LINHA, aa, "stroke", 2.4))
    cv.drawLine(x0, yt + 8, x1, yt + 8, paint(CAIXA_TOPO, aa, "stroke", 3))


def caixa_tampa_fecha(cv, x0, yb, w, h, fecha, a=1.0, conteudo=None):
    """Caixa na prateleira com a tampa encostada atrás, que gira e fecha (fecha 0 -> 1)."""
    aa = int(255 * a)
    x1 = x0 + w; yt = yb - h; dp = 14
    cv.drawRect(skia.Rect(x0 + 4, yb - 4, x1 + 10, yb + 6), paint("#000000", int(60 * a), blur=8))
    # tampa (atrás) enquanto aberta
    ang = lerp(-78, 0, e_inout(fecha))
    tampa = skia.Rect(0, -12, w + dp * 0.3, 0)

    def _tampa():
        cv.save(); cv.translate(x0 + dp * 0.4, yt - dp * 0.7); cv.rotate(ang)
        cv.drawRect(tampa, paint(CAIXA_TOPO, aa)); cv.drawRect(tampa, paint(CAIXA_LINHA, aa, "stroke", 2.2))
        cv.restore()
    if fecha < 0.55:
        _tampa()
    cv.drawPath(poli([(x0, yt), (x0 + dp, yt - dp * 0.7), (x1 + dp, yt - dp * 0.7), (x1, yt)]), paint("#6E5D45", aa))
    cv.drawPath(poli([(x1, yt), (x1 + dp, yt - dp * 0.7), (x1 + dp, yb - dp * 0.7), (x1, yb)]), paint(CAIXA_ESC, aa))
    cv.drawRect(skia.Rect(x0 + 6, yt - 18, x1 - 6, yt + 6), paint(SEDA, aa))
    if conteudo is not None:
        conteudo(cv)
    sh = skia.GradientShader.MakeLinear([skia.Point(0, yt), skia.Point(0, yb)], [_c(CAIXA_TOPO), _c(CAIXA)])
    cv.drawRect(skia.Rect(x0, yt, x1, yb), paint(CAIXA, aa, shader=sh))
    cv.drawRect(skia.Rect(x0, yt, x1, yb), paint(CAIXA_LINHA, aa, "stroke", 2.2))
    if fecha >= 0.55:
        _tampa()
        if fecha >= 0.98:
            cv.drawRect(skia.Rect(x0 - 3, yt - 12, x1 + 4, yt + 14), paint(CAIXA_TOPO, aa))
            cv.drawRect(skia.Rect(x0 - 3, yt - 12, x1 + 4, yt + 14), paint(CAIXA_LINHA, aa, "stroke", 2.2))


def seta_moldar(cv, p0, p1, k, a, esc=1.0):
    """Seta curva PONTILHADA dourada (a 'promessa de moldar'): bolinhas ao longo de uma curva + ponta.
    Desenhada até a fração k."""
    if a <= 0 or k <= 0:
        return None
    c = ((p0[0] + p1[0]) / 2 - 70 * esc, (p0[1] + p1[1]) / 2)
    pts = []
    for i in range(121):
        u = i / 120
        x = (1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * c[0] + u * u * p1[0]
        y = (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * c[1] + u * u * p1[1]
        pts.append((x, y))
    comp = [0.0]
    for q0, q1 in zip(pts, pts[1:]):
        comp.append(comp[-1] + math.hypot(q1[0] - q0[0], q1[1] - q0[1]))
    tot = comp[-1]; lim = tot * k
    passo = 17 * esc; s = 6 * esc
    j = 0
    pontos = []
    while s < lim - 14 * esc:
        while j < len(comp) - 1 and comp[j + 1] < s:
            j += 1
        f = (s - comp[j]) / max(1e-6, comp[j + 1] - comp[j])
        pontos.append(lerp2(pts[j], pts[min(j + 1, len(pts) - 1)], f))
        s += passo
    for (x, y) in pontos:
        cv.drawCircle(x, y, 7.6 * esc, paint(CARTAO, int(170 * a)))
    for (x, y) in pontos:
        cv.drawCircle(x, y, 5.2 * esc, paint(SETA_OURO, int(255 * a)))
    # ponta (na fração k)
    jj = max(1, min(len(pts) - 1, int(120 * k)))
    tip = pts[jj]; ant = pts[max(0, jj - 6)]
    ang = math.atan2(tip[1] - ant[1], tip[0] - ant[0])
    ponta(cv, tip[0] + 3 * math.cos(ang), tip[1] + 3 * math.sin(ang), ang, 30 * esc, CARTAO, 0.7 * a)
    ponta(cv, tip[0], tip[1], ang, 24 * esc, SETA_OURO, a)
    return pts[60]


def luz_sola(cv, pe, cor, a, larg=7.0):
    """Linha acesa ao longo da sola (branca: 'encosta inteira'; verde: JEITO CERTO)."""
    if a <= 0:
        return
    pts = [pe.ponto(x, y + 2) for (x, y) in sola_pts(pe.arco)]
    p = poli(pts, fechar=False)
    cv.drawPath(p, paint(cor, int(150 * a), "stroke", larg * 3 * pe.esc / 1.25, blur=7))
    cv.drawPath(p, paint(cor, int(255 * a), "stroke", larg * pe.esc / 1.25))


def sombra_pe(cv, pe, y_chao, a=1.0, arco=0.0):
    """Sombra de contato no chão: inteira (chato) ou em duas manchas (com arco)."""
    if a <= 0:
        return
    s = pe.esc
    hx = pe.ponto(-20, 0)[0]; bx = pe.ponto(100, 0)[0]
    alt = clamp((y_chao - (pe.ay + Y_SOLA * s)) / (120 * s))
    k = 1 - alt
    if k <= 0:
        return
    mx = pe.ponto(30, 0)[0]
    cv.drawOval(skia.Rect(hx - 20 * s, y_chao - 7 * s, bx + 14 * s, y_chao + 9 * s), paint("#000000", int(55 * a * k * (1 - 0.6 * arco)), blur=8))
    cv.drawOval(skia.Rect(hx - 14 * s, y_chao - 5 * s, hx + 30 * s, y_chao + 6 * s), paint("#000000", int(60 * a * k), blur=5))
    cv.drawOval(skia.Rect(mx + 26 * s, y_chao - 5 * s, bx + 6 * s, y_chao + 6 * s), paint("#000000", int(60 * a * k), blur=5))


# ================================================================== CENÁRIO 1: a entrada de casa (lances 1 e 2)
Y_CHAO = 1060.0                 # o chão onde estão o tênis, a palmilha e o pé
Y_RODAPE = 930.0                # parede -> piso
ESC = 1.25                      # unidades do pé -> mundo
X_PE = 450.0                    # tornozelo (lances 1 e 2)
Y_PAIRA = 750.0                 # tornozelo do pé pairando sobre o tênis
Y_PE_CHAO = Y_CHAO - Y_SOLA * ESC
CARO_M = _mat(X_PE, Y_CHAO - sola_y("caro") * ESC, 0.0, ESC)
PALM_X = X_PE + (30 - 28) * ESC
PRAT_X0, PRAT_X1, PRAT_TOPO, PRAT_MEIO = 105.0, 335.0, 752.0, 856.0
SIMPLES_PRAT = (178.0, PRAT_TOPO - sola_y("simples") * 1.0, 1.0)      # (x, y, esc) do tênis simples guardado
CAIXA_E = (648.0, 1002.0, 186.0, 92.0)                                # x0, base, largura, altura


_P_ALVO = _mapa(_mat(X_PE, Y_PAIRA, 0.0, ESC), 30, Y_SOLA + 6)        # o meio da sola do pé pairando
SETA1 = (_mapa(CARO_M, 26, 18 + SHOE_DY), _P_ALVO)                                 # do tênis caro para o meio do pé
SETA2 = ((PALM_X + TOPO_CALOMBO[0] * ESC, Y_CHAO + TOPO_CALOMBO[1] * ESC - 8), _P_ALVO)   # do calombo


def meio_seta(p0, p1):
    c = ((p0[0] + p1[0]) / 2 - 70, (p0[1] + p1[1]) / 2)
    return (0.25 * p0[0] + 0.5 * c[0] + 0.25 * p1[0], 0.25 * p0[1] + 0.5 * c[1] + 0.25 * p1[1])


def entrada(cv):
    E0X, E0Y, E1X, E1Y, ESC_C = -60.0, 300.0, 1140.0, 1400.0, 1.5

    def _d(c):
        c.scale(ESC_C, ESC_C); c.translate(-E0X, -E0Y); _entrada(c)
    img = cacheado("entrada", (E1X - E0X) * ESC_C, (E1Y - E0Y) * ESC_C, _d)
    cv.save(); cv.translate(E0X, E0Y); cv.scale(1 / ESC_C, 1 / ESC_C)
    cv.drawImage(img, 0, 0, LINEAR)
    cv.restore()


def _piso(cv, y0, y1, x0=-200, x1=1400, seed=3):
    sh = skia.GradientShader.MakeLinear([skia.Point(0, y0), skia.Point(0, y1)], [_c(PISO_CL), _c(PISO), _c(PISO_ESC)],
                                        [0.0, 0.45, 1.0])
    cv.drawRect(skia.Rect(x0, y0, x1, y1), paint(PISO, shader=sh))
    ys = [y0]
    h = 22.0
    while ys[-1] < y1:
        ys.append(ys[-1] + h); h *= 1.22
    rng = np.random.default_rng(seed)
    for i, (ya, yb) in enumerate(zip(ys, ys[1:])):
        cv.drawLine(x0, ya, x1, ya, paint(PISO_ESC, 150, "stroke", 2))
        off = float(rng.uniform(0, 300))
        x = x0 + off
        while x < x1:
            cv.drawLine(x, ya, x, min(yb, y1), paint(PISO_ESC, 120, "stroke", 2))
            x += float(rng.uniform(260, 420))


def _entrada(cv):
    sh = skia.GradientShader.MakeLinear([skia.Point(0, 300), skia.Point(0, Y_RODAPE)], [_c(PAREDE_A), _c(PAREDE_B)])
    cv.drawRect(skia.Rect(-200, 0, 1400, Y_RODAPE), paint(PAREDE_A, shader=sh))
    # batente de porta à direita (casa), sem texto
    cv.drawRect(skia.Rect(1036, 360, 1060, Y_RODAPE), paint("#F2F5F8"))
    cv.drawRect(skia.Rect(1060, 360, 1200, Y_RODAPE), paint("#B9C5D1"))
    _piso(cv, Y_RODAPE, 1420)
    cv.drawRect(skia.Rect(-200, Y_RODAPE - 22, 1400, Y_RODAPE + 2), paint(RODAPE))
    cv.drawLine(-200, Y_RODAPE - 22, 1400, Y_RODAPE - 22, paint("#C3CCD5", 255, "stroke", 2))
    # a prateleira de sapatos (madeira clara), sem texto
    cv.drawRect(skia.Rect(PRAT_X0 + 6, PRAT_TOPO, PRAT_X1 + 10, Y_RODAPE + 12), paint("#000000", 50, blur=12))
    for x in (PRAT_X0, PRAT_X1 - 16):
        cv.drawRect(skia.Rect(x, PRAT_TOPO - 6, x + 16, Y_RODAPE + 8), paint(PRAT_ESC))
    for y in (PRAT_TOPO, PRAT_MEIO, Y_RODAPE - 6):
        cv.drawRect(skia.Rect(PRAT_X0 - 8, y, PRAT_X1 + 8, y + 14), paint(PRAT))
        cv.drawLine(PRAT_X0 - 8, y + 2, PRAT_X1 + 8, y + 2, paint(PRAT_CL, 255, "stroke", 3))
        cv.drawRect(skia.Rect(PRAT_X0 - 8, y, PRAT_X1 + 8, y + 14), paint(PRAT_ESC, 220, "stroke", 2))
    # cesto trançado na prateleira do meio
    cesto = rr_path(150, PRAT_MEIO - 64, 290, PRAT_MEIO, 14)
    cv.drawPath(cesto, paint("#C99A5E"))
    cv.save(); cv.clipPath(cesto, skia.ClipOp.kIntersect, True)
    for i in range(6):
        cv.drawLine(150, PRAT_MEIO - 60 + i * 11, 290, PRAT_MEIO - 60 + i * 11, paint("#A97B42", 255, "stroke", 3))
    cv.restore()
    cv.drawPath(cesto, paint("#8C6533", 230, "stroke", 2.4))
    # pufe redondo ao fundo, à direita
    pufe = rr_path(866, 838, 1080, 968, 46)
    cv.drawOval(skia.Rect(860, 950, 1090, 982), paint("#000000", 60, blur=10))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, 838), skia.Point(0, 968)], [_c(PUFE_CL), _c(PUFE), _c(PUFE_ESC)])
    cv.drawPath(pufe, paint(PUFE, shader=sh))
    cv.drawLine(870, 878, 1076, 878, paint(PUFE_ESC, 200, "stroke", 3))
    for x in range(900, 1080, 44):
        cv.drawLine(x, 878, x - 6, 966, paint(PUFE_ESC, 140, "stroke", 2.4))
    cv.drawPath(pufe, paint(esc_cor(PUFE_ESC, 0.25), 220, "stroke", 2.6))


# ================================================================== CENÁRIO 2: a sala (lance 3)
Y3 = 1170.0                     # o tapete onde a criança anda
ESC3 = 1.2
Y_TORN3 = Y3 - Y_SOLA * ESC3
HIP3_Y = Y_TORN3 - (L1 + L2) * LK * ESC3 * 0.95
X3_0 = 250.0                    # quadril no começo do lance
PASSO_A, CICLO, APOIO = 56.0, 1.3, 0.6
LONGE_DX, LONGE_DY = -16.0, -6.0  # a perna de trás fica um pouco atrás (profundidade)
VEL3 = 2 * PASSO_A / (APOIO * CICLO)
RODAPE3 = 1010.0
TAP_Y0, TAP_Y1 = 1100.0, 1250.0
PRAT3 = (70.0, 430.0, 772.0, 902.0)      # x0, x1, tábua de cima, tábua do meio
CAIXA3 = (236.0, 902.0, 168.0, 80.0)


def sala(cv):
    S0X, S0Y, S1X, S1Y, ESC_C = -120.0, 380.0, 1700.0, 1460.0, 1.3

    def _d(c):
        c.scale(ESC_C, ESC_C); c.translate(-S0X, -S0Y); _sala(c)
    img = cacheado("sala", (S1X - S0X) * ESC_C, (S1Y - S0Y) * ESC_C, _d)
    cv.save(); cv.translate(S0X, S0Y); cv.scale(1 / ESC_C, 1 / ESC_C)
    cv.drawImage(img, 0, 0, LINEAR)
    cv.restore()


def _sala(cv):
    sh = skia.GradientShader.MakeLinear([skia.Point(0, 380), skia.Point(0, RODAPE3)], [_c("#E6EDF2"), _c("#D0DAE3")])
    cv.drawRect(skia.Rect(-300, 0, 1900, RODAPE3), paint("#E6EDF2", shader=sh))
    # janela ao fundo (luz do dia)
    jx0, jy0, jx1, jy1 = 560, 470, 820, 730
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(jx0 - 14, jy0 - 14, jx1 + 14, jy1 + 14), 8, 8), paint("#F7F9FB"))
    vid = skia.GradientShader.MakeLinear([skia.Point(jx0, jy0), skia.Point(jx1, jy1)], [_c("#BFE3F7"), _c("#E9F6FD")])
    cv.drawRect(skia.Rect(jx0, jy0, jx1, jy1), paint("#CFEAF8", shader=vid))
    cv.drawLine((jx0 + jx1) / 2, jy0, (jx0 + jx1) / 2, jy1, paint("#F7F9FB", 255, "stroke", 12))
    cv.drawLine(jx0, (jy0 + jy1) / 2, jx1, (jy0 + jy1) / 2, paint("#F7F9FB", 255, "stroke", 12))
    _piso(cv, RODAPE3, 1500, -300, 1900, seed=5)
    cv.drawRect(skia.Rect(-300, RODAPE3 - 22, 1900, RODAPE3 + 2), paint(RODAPE))
    cv.drawLine(-300, RODAPE3 - 22, 1900, RODAPE3 - 22, paint("#C3CCD5", 255, "stroke", 2))
    # sofá ao fundo, à direita
    sx0, sx1 = 930.0, 1700.0
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(sx0 + 8, 780, sx1, RODAPE3 + 14), 40, 40), paint("#000000", 60, blur=16))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, 760), skia.Point(0, RODAPE3)], [_c(SOFA_CL), _c(SOFA), _c(SOFA_ESC)])
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(sx0, 760, sx1, RODAPE3 - 8), 40, 40), paint(SOFA, shader=sh))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(sx0 - 20, 850, sx0 + 90, RODAPE3 - 8), 34, 34), paint(SOFA_CL))
    cv.drawLine(sx0 + 90, 880, sx1, 880, paint(SOFA_ESC, 170, "stroke", 4))
    for x in range(int(sx0) + 140, int(sx1), 150):
        cv.drawCircle(x, 940, 6, paint(SOFA_ESC, 200))
    # a prateleira de sapatos (os dois tênis guardados)
    x0, x1, yt, ym = PRAT3
    cv.drawRect(skia.Rect(x0 + 6, yt, x1 + 10, RODAPE3 + 12), paint("#000000", 50, blur=12))
    for x in (x0, x1 - 16):
        cv.drawRect(skia.Rect(x, yt - 6, x + 16, RODAPE3 + 8), paint(PRAT_ESC))
    for y in (yt, ym, RODAPE3 - 6):
        cv.drawRect(skia.Rect(x0 - 8, y, x1 + 8, y + 14), paint(PRAT))
        cv.drawLine(x0 - 8, y + 2, x1 + 8, y + 2, paint(PRAT_CL, 255, "stroke", 3))
        cv.drawRect(skia.Rect(x0 - 8, y, x1 + 8, y + 14), paint(PRAT_ESC, 220, "stroke", 2))
    # o tênis simples, guardado na tábua de cima
    m = _mat(150.0, yt - sola_y("simples") * 1.0, 0.0, 1.0)
    tenis_frente(cv, m, "simples", 1.0, vazio=True)
    # o tapete (passadeira lisa, macia)
    tap = skia.Path(); tap.addRRect(skia.RRect.MakeRectXY(skia.Rect(-300, TAP_Y0, 1900, TAP_Y1), 18, 18))
    cv.drawPath(tap, paint("#000000", 50, blur=10))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, TAP_Y0), skia.Point(0, TAP_Y1)], [_c(TAPETE_CL), _c(TAPETE), _c(TAPETE_ESC)],
                                        [0.0, 0.5, 1.0])
    cv.drawPath(tap, paint(TAPETE, shader=sh))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-290, TAP_Y0 + 10, 1890, TAP_Y1 - 10), 12, 12), paint(TAPETE_CL, 200, "stroke", 3))
    cv.drawPath(tap, paint(TAPETE_ESC, 220, "stroke", 2.5))


# ================================================================== ESTADOS (tempo -> o que a cena mostra)
def estado_entrada(t, T, certo=None):
    """Lances 1 e 2 (a entrada de casa)."""
    V = T["var"]
    e = {}
    ts = t
    if t < V or T["pode1"] <= t < T["anulado1"]:
        ts = T["pode1"]
    elif T["pode2"] <= t < T["anulado2"]:
        ts = T["pode2"]
    e["ts"] = ts
    if certo is None:
        certo = t >= T["wipe"] + 0.36
    e["certo"] = certo
    lance2 = t >= T["palmilha1"]
    e["lance2"] = lance2
    # ---------- lance 1 (antes da cortina): o pé paira sobre o tênis caro
    if t < V:
        fora = 0.0
    elif t < V + 0.5:
        fora = e_inout(prog(t, V, V + 0.5))
    else:
        fora = 1 - e_out(prog(ts, T["corrigir"] - 0.08, T["corrigir"] + 0.34))
    e["fora1"] = fora
    if t < V:
        k1 = 1.0
    elif t < V + 0.5:
        k1 = 1 - prog(t, V, V + 0.22)
    else:
        k1 = e_out(prog(ts, T["pe1"] - 0.03, T["pe1"] + 0.32))
    e["seta1"] = k1
    e["seta1_a"] = 1 - prog(t, T["molda1"] + 0.22, T["molda1"] + 0.5)
    e["luz_chata"] = janela(ts, T["chato1"] - 0.02, T["chato1_fim"] + 0.12, 0.1, 0.25) if t >= V + 0.5 else 0.0
    if V <= t < V + 0.5:
        e["moedas"] = 4 if t < V + 0.25 else 2
    else:
        e["moedas"] = 2 if ts < T["caro"] + 0.05 else (3 if ts < T["caro"] + 0.16 else 4)
    k = ts - T["caro"]
    e["etq_ang"] = 18 * math.sin(k * 11) * math.exp(-k * 2.6) if k > 0 and t >= V + 0.5 else 0.0
    e["etq_pulo"] = math.sin(math.pi * prog(ts, T["caro"] + 0.05, T["caro"] + 0.3)) if t >= V + 0.5 else 0.0
    e["corre"] = prog(ts, T["tenis1"] - 0.04, T["tenis1"] + 0.5) if t >= V + 0.5 else -1.0
    e["dour"] = 1 - 0.75 * e_inout(prog(t, T["tenis2"], T["tenis2"] + 0.5))
    e["queda"] = prog(t, T["tenis2"] - 0.02, T["tenis2"] + 0.8)
    # ---------- JEITO CERTO do lance 1 (depois da cortina): o tênis simples no pé
    e["verde1"] = janela(t, T["protege"] - 0.02, T["protege_fim"] - 0.05, 0.18, 0.2)
    pf = T["protege_fim"]
    e["dobra"] = 24 * e_inout(prog(t, pf + 0.02, pf + 0.26)) * (1 - e_inout(prog(t, pf + 0.52, pf + 0.7)))
    e["tele_dobra"] = janela(t, pf + 0.06, T["palmilha1"] - 0.04, 0.12, 0.16)
    e["ok1"] = janela(t, pf + 0.4, T["palmilha1"] + 0.05, 0.12, 0.15)
    # ---------- lance 2: o pé sai do tênis simples, a palmilha cai sozinha
    P1 = T["palmilha1"]
    e["sai"] = e_inout(prog(t, P1 - 0.02, P1 + 0.3))                         # o pé sobe do tênis
    e["guarda"] = e_inout(prog(t, P1 + 0.22, P1 + 0.62))                     # o tênis simples volta à prateleira
    e["cai"] = prog(ts, P1 + 0.15, P1 + 0.62)                                # a palmilha chega ao chão
    e["seta2"] = e_out(prog(ts, T["formar"] - 0.02, T["formar"] + 0.32))
    e["seta2_a"] = 1 - prog(t, T["molda2"] + 0.22, T["molda2"] + 0.5)
    e["luz_arco"] = janela(ts, T["arco1"] - 0.02, T["arco1"] + 0.42, 0.1, 0.25)
    e["pulinho"] = math.sin(math.pi * prog(t, T["palmilha2"] - 0.04, T["palmilha2"] + 0.26))
    e["desliza"] = e_inout(prog(t, T["arco2"] - 0.02, T["arco2"] + 0.45))
    e["pousa"] = e_inout(prog(t, T["crianca"] - 0.12, T["crianca"] + 0.2))
    ka = t - (T["flexivel"] - 0.05)
    e["mexe"] = (16 * math.sin(ka * 2 * math.pi * 2.0) * janela(t, T["flexivel"] - 0.05, T["costuma"] - 0.1, 0.12, 0.2)
                 if ka > 0 else 0.0)
    # o calendário vira 3 folhas e o pé cresce a cada uma
    viradas = [T["costuma"] + 0.05 + 0.32 * i for i in range(3)]
    e["viradas"] = viradas
    e["cresce"] = sum(e_inout(prog(t, v0 + 0.08, v0 + 0.3)) for v0 in viradas) / 3.0
    e["arco"] = e_inout(prog(t, T["sozinho"] - 0.02, T["sozinho"] + 0.5))
    e["verde2"] = janela(t, T["sozinho"] + 0.28, T["descalco"] - 0.02, 0.25, 0.05)
    return e


def quadril_entrada(pe):
    """Quadril acima do tornozelo, perna quase reta, na proporção de criança. O corpo (bermuda + barra da
    camiseta) é desenhado por cima e sobe para fora do quadro: nenhuma ponta de perna solta aparece."""
    return (pe.ax + 10 * pe.esc, pe.ay - (L1 + L2 - 4) * LK * pe.esc)


def corpo_entrada(cv, hip, joe, s):
    corpo_baixo(cv, hip, s)
    short_perna(cv, hip, joe, s)


def pe_entrada(e, t, T):
    """Pose do pé (e o tênis que ele calça) na entrada, conforme o estado."""
    if not e["lance2"]:
        if not e["certo"]:
            y = lerp(Y_PAIRA, Y_PAIRA - 640, e["fora1"])
            return Pe(X_PE, y, 0.0, 0.0, 0.0, ESC), None
        yb = Y_CHAO - sola_y("simples") * ESC
        return Pe(X_PE, yb, 0.0, 0.0, 0.0, ESC), "simples"
    # lance 2
    if e["pousa"] <= 0:
        y0 = Y_CHAO - sola_y("simples") * ESC
        y = lerp(y0, Y_PAIRA, e["sai"])
        return Pe(X_PE, y, 0.0, -6 * e["sai"] * (1 - e["sai"]) * 4, 0.0, ESC), ("simples" if e["sai"] < 0.8 else None)
    esc = ESC * (1 + 0.16 * e["cresce"])
    calc_x = X_PE - 31 * ESC                                                   # o calcanhar fica no lugar
    ax = calc_x + 31 * esc
    y_chao = Y_CHAO - Y_SOLA * esc
    y = lerp(Y_PAIRA, y_chao, e["pousa"])
    return Pe(ax, y, 0.0, e["mexe"], e["arco"], esc), None


def estado_sala(t, T):
    """Lance 3 (a sala): relógio da marcha, quadril, os dois pés."""
    e = {}
    D, P3, Vd, F = T["descalco"], T["pode3"], T["validado"], T["fortalece"]
    m = max(0.0, min(t, P3) - D) + max(0.0, min(t, F) - Vd)
    e["m"] = m
    m_p3 = P3 - D
    fase0 = 0.86 - m_p3 / CICLO                                               # no 'pode?' o pé da frente está no ar
    fi = m / CICLO + fase0
    hx = X3_0 + VEL3 * m
    hy = HIP3_Y + 3.0 * math.cos(4 * math.pi * fi)
    pes = []
    for off in (0.0, 0.5):
        ph = (fi + off) % 1.0
        if ph < APOIO:
            s = ph / APOIO
            dx, lift, inc, dd = PASSO_A - 2 * PASSO_A * s, 0.0, 0.0, 0.0
        else:
            s = (ph - APOIO) / (1 - APOIO)
            dx = -PASSO_A + 2 * PASSO_A * e_inout(s)
            lift = 44 * math.sin(math.pi * s)
            inc = -9 * math.sin(math.pi * s)
            dd = -16 * math.sin(math.pi * s)
        lx, ly = (LONGE_DX, LONGE_DY) if off else (0.0, 0.0)
        pes.append([hx + dx - 8 + lx, Y_TORN3 - lift + ly, inc, dd, ph])
    # equilíbrio num pé só a partir de "fortalece": o pé da frente fica no tapete (contorno verde) e o de TRÁS
    # sai claramente do chão, joelho dobrado, com uma oscilação pequena de equilíbrio
    kb = e_inout(prog(t, F - 0.02, F + 0.3))
    sway = 0.0
    if kb > 0:
        apoio, outro = 0, 1
        pes[apoio][1] = lerp(pes[apoio][1], Y_TORN3, kb)
        pes[apoio][2] = lerp(pes[apoio][2], 0.0, kb)
        aperta = janela(t, F + 0.1, T["off"], 0.18, 0.1)
        pes[apoio][3] = lerp(pes[apoio][3], 9.0 * aperta, kb)
        ks = max(0.0, t - F - 0.2)
        sway = kb * 5.0 * math.sin(ks * 7.0) * math.exp(-ks * 0.8)
        pes[outro][0] = lerp(pes[outro][0], hx - 70 + LONGE_DX + 0.6 * sway, kb)
        pes[outro][1] = lerp(pes[outro][1], Y_TORN3 - 138 + LONGE_DY + 3.0 * sway, kb)
        pes[outro][2] = lerp(pes[outro][2], -20.0, kb)
        pes[outro][3] = lerp(pes[outro][3], -8.0, kb)
        e["apoio"] = apoio
    else:
        e["apoio"] = 0 if pes[0][4] < APOIO else 1
    e["hip"] = (hx + sway, hy)
    e["pes"] = [Pe(p[0], p[1], p[2], p[3], 0.25, ESC3) for p in pes]      # pé de criança: arco discreto
    e["tampa"] = e_inout(prog(t, T["custa"] - 0.04, T["custa"] + 0.42))
    # "não custa nada": a etiqueta de moedas do tênis caro aparece e se esvazia (4 -> 0)
    e["etq_a"] = janela(t, T["custa"] - 0.12, T["fortalece"] + 0.25, 0.16, 0.25)
    e["verde3"] = janela(t, F + 0.15, T["off"], 0.2, 0.1)
    return e


# ================================================================== câmeras
CAM_Q0 = (1.35, 505.0, 775.0)     # quadro 0: a bermuda + o pé pairando + a seta + o tênis caro
CAM_JOGO = (1.35, 500.0, 772.0)
CAM_TENIS = (1.85, 470.0, 960.0)  # "Tênis caro": o brilho e as moedas de perto
CAM_L1_PERTO = (1.62, 525.0, 846.0)
CAM_L2_PERTO = (1.62, 525.0, 858.0)
CAM_CERTO = (1.55, 560.0, 905.0)  # o tênis simples no pé (JEITO CERTO do lance 1)
CAM_PE = (1.55, 500.0, 905.0)     # o pé no chão (crescendo)


def cam_entrada(t, T):
    V = T["var"]
    if t < V:
        return CAM_Q0
    cam = lerp3(CAM_Q0, CAM_JOGO, e_inout(prog(t, V, V + 0.5)))
    cam = lerp3(cam, CAM_TENIS, e_inout(prog(t, T["tenis1"] - 0.1, T["tenis1"] + 0.3)))
    cam = lerp3(cam, CAM_JOGO, e_inout(prog(t, T["corrigir"] - 0.12, T["corrigir"] + 0.3)))
    cam = lerp3(cam, CAM_L1_PERTO, e_inout(prog(t, T["pode1"], T["pode1"] + 0.3)))
    cheg = prog(t, T["pode1_fim"], T["anulado1"])
    cam = (cam[0] * (1 + 0.05 * e_inout(cheg)),) + tuple(cam[1:])
    cam = lerp3(cam, CAM_JOGO, e_inout(prog(t, T["anulado1"] + 0.5, T["molda1"] + 0.3)))
    cam = lerp3(cam, CAM_CERTO, e_inout(prog(t, T["wipe"] + 0.3, T["protege"] + 0.1)))
    cam = lerp3(cam, CAM_JOGO, e_inout(prog(t, T["palmilha1"] + 0.05, T["palmilha1"] + 0.55)))
    cam = lerp3(cam, CAM_L2_PERTO, e_inout(prog(t, T["pode2"], T["pode2"] + 0.3)))
    cheg = prog(t, T["pode2_fim"], T["anulado2"])
    cam = (cam[0] * (1 + 0.05 * e_inout(cheg)),) + tuple(cam[1:])
    cam = lerp3(cam, CAM_JOGO, e_inout(prog(t, T["anulado2"] + 0.5, T["molda2"] + 0.3)))
    return lerp3(cam, CAM_PE, e_inout(prog(t, T["crianca"] + 0.1, T["costuma"])))


def cam_sala(t, T, e):
    hx = e["hip"][0]
    fx = 520 + 0.72 * (hx - 520)                 # acompanha a criança (o visto e a etiqueta cabem no quadro)
    perto = (1.36, hx + 70, 1010.0)
    longe = (1.12, fx, 988.0)
    return lerp3(perto, longe, e_inout(prog(t, T["casa"] - 0.05, T["casa"] + 0.5)))


# ================================================================== cenas
def cena_entrada(cv, t, T, cam, e):
    cv.save(); aplica(cv, cam)
    entrada(cv)
    pe, calca = pe_entrada(e, t, T)
    # o tênis simples: na prateleira (lance 1 antes da cortina), no pé (jeito certo) ou voltando (lance 2)
    sx, sy, se = SIMPLES_PRAT
    no_pe = _mat(X_PE, Y_CHAO - sola_y("simples") * ESC, 0.0, ESC)
    if not e["certo"]:
        tenis_frente(cv, _mat(sx, sy, 0.0, se), "simples", 1.0, vazio=True)
    elif e["lance2"] and calca is None:
        g = e["guarda"]
        x = lerp(X_PE, sx, g); y = lerp(Y_CHAO - sola_y("simples") * ESC, sy, g) - 160 * math.sin(math.pi * g)
        tenis_frente(cv, _mat(x, y, -14 * math.sin(math.pi * g), lerp(ESC, se, g)), "simples", 1.0, vazio=True)
    # a caixa: vazia (o tênis caro está no chão) ou com o tênis caro guardado (depois da cortina)
    x0, yb, w, h = CAIXA_E

    def _dentro(c):
        m = _mat(x0 + 56, yb - 6 - sola_y("caro") * 1.0, -4.0, 1.0)
        tenis_frente(c, m, "caro", 1.0, dour=e["dour"], vazio=True)
        etiqueta(c, m, 8.0, 4, 1.0)
    caixa(cv, x0, yb, w, h, 1.0, _dentro if e["certo"] else None)
    # a palmilha (lance 2): cai sozinha no chão, sob o pé; depois desliza para o lado, deitada
    if e["lance2"] and e["cai"] > 0:
        k = e["cai"]
        x = lerp(PALM_X + 300, PALM_X, e_out(k)) - 250 * e["desliza"]
        y = lerp(Y_CHAO - 260, Y_CHAO, k * k) - 18 * e["pulinho"]
        rot = lerp(-18, 0, e_out(k))
        q = lerp(1.0, 0.36, e_inout(prog(k, 0.55, 1.0)))          # cai vista de cima (forma de sola) e deita em 3/4
        if k >= 1:
            y -= 10 * math.sin(math.pi * prog(e["ts"], T["palmilha1"] + 0.62, T["palmilha1"] + 0.79))
        palmilha(cv, x, y, ESC, 1.0, rot, q=q)
    # o tênis caro no chão (lance 1, antes da cortina)
    if not e["certo"]:
        m = CARO_M
        tenis_fundo(cv, m, "caro")
        tenis_frente(cv, m, "caro", 1.0, dour=e["dour"], brilho=e["corre"], vazio=True)
        etiqueta(cv, m, e["etq_ang"], e["moedas"], 1.0, e["etq_pulo"])
        # brilhos dourados piscando; no ANULADO caem como poeira e apagam
        for i, (bx, by, r0, fase) in enumerate(((-70, -36, 18, 0.0), (66, -58, 22, 1.7), (150, -6, 16, 3.1),
                                                 (112, 82, 13, 4.4), (-20, -66, 12, 5.3))):
            x, y = _mapa(m, bx, by)
            q = e["queda"]
            y += 160 * q * q
            pis = 0.6 + 0.4 * math.sin(e["ts"] * 6 + fase) if t >= T["var"] else 1.0
            brilho4(cv, x, y, r0 * pis * (1 - 0.5 * q), 1 - q)
    # o pé (e a perna)
    if pe.ay < Y_CHAO + 200 and (e["certo"] or e["fora1"] < 0.999):
        hip = quadril_entrada(pe)
        if calca is None:
            sombra_pe(cv, pe, Y_CHAO, 1.0, pe.arco)
            joe, _ = perna(cv, hip, pe)
        else:
            m = no_pe
            dob = e["dobra"] if not e["lance2"] else 0.0
            if dob > 0:
                joe, hip = _pe_dobrando(cv, hip, pe, m, dob, e)
            else:
                tenis_fundo(cv, m, "simples")
                joe, _ = perna(cv, hip, pe)
                tenis_frente(cv, m, "simples", 1.0, verde=e["verde1"] if not e["lance2"] else 0.0)
        corpo_entrada(cv, hip, joe, pe.esc)
        if e["luz_chata"] > 0 and not e["certo"]:
            luz_sola(cv, pe, "#FFFFFF", e["luz_chata"])
        if e["lance2"] and e["luz_arco"] > 0 and e["pousa"] <= 0:
            pa = Pe(pe.ax, pe.ay, 0, 0, 0, pe.esc)
            pts = [pa.ponto(x, y + 2) for (x, y) in sola_pts(0.0) if 4 <= x <= 56]
            pth = poli(pts, fechar=False)
            cv.drawPath(pth, paint("#FFFFFF", int(150 * e["luz_arco"]), "stroke", 22, blur=8))
            cv.drawPath(pth, paint("#FFFFFF", int(255 * e["luz_arco"]), "stroke", 8))
        if e["verde2"] > 0:
            luz_sola(cv, pe, VERDE, e["verde2"])
    # as setas de 'moldar' (do tênis / do calombo da palmilha para o meio do pé)
    meio = None
    if not e["certo"] and e["seta1"] > 0:
        seta_moldar(cv, *SETA1, e["seta1"], e["seta1_a"], 1.0)
    if e["lance2"] and e["seta2"] > 0 and e["seta2_a"] > 0:
        seta_moldar(cv, *SETA2, e["seta2"], e["seta2_a"], 1.0)
    meio = meio_seta(*(SETA2 if e["lance2"] else SETA1))
    cv.restore()
    return pe, meio


def _pe_dobrando(cv, hip, pe, m, dob, e):
    """A sola do tênis simples DOBRA na frente: a ponta fica no chão e a parte de trás (com o pé) gira na bola do
    pé, como quem fica na ponta dos pés; a PERNA continua em pé (o quadril sobe junto com o tornozelo), então
    o que se vê dobrar é o solado, não o tênis inteiro inclinando. Devolve (joelho, quadril)."""
    yb = sola_y("simples")
    piv = _mapa(m, BOLA_X, yb)
    cv.save(); cv.concat(m); cv.translate(0, SHOE_DY)
    cv.drawOval(skia.Rect(-60, yb - SHOE_DY - 8, 142, yb - SHOE_DY + 12), paint("#000000", 70, blur=10))
    cv.restore()
    # a ponta (fica no chão), um pouco mais comprida para trás: preenche a dobra por cima
    tenis_frente(cv, m, "simples", 1.0, clip_x=(BOLA_X - 26, 200))
    r = skia.Matrix(); r.setRotate(dob, piv[0], piv[1])          # + = horário na tela: o CALCANHAR sobe
    ax, ay = _mapa(r, pe.ax, pe.ay)
    pe_r = Pe(ax, ay, pe.inc + dob, -dob, pe.arco, pe.esc)
    hip_r = (hip[0] + (ax - pe.ax), hip[1] + (ay - pe.ay))
    cv.save(); cv.concat(r); tenis_fundo(cv, m, "simples"); cv.restore()
    dentro = uniao(rr_path(-600, -40 + SHOE_DY, BOLA_X - 6, 300, 0), rr_path(-600, -900, 600, -40 + SHOE_DY, 0))
    cv.save(); cv.clipPath(_transf(_transf(dentro, m), r), skia.ClipOp.kIntersect, True)
    joe, _ = perna(cv, hip_r, pe_r)
    cv.restore()
    cv.save(); cv.concat(r)
    tenis_frente(cv, m, "simples", 1.0, clip_x=(-200, BOLA_X + 1))
    cv.restore()
    # o vinco da dobra (em V) no cabedal e no solado
    k = clamp(dob / 20.0)
    q0 = _mapa(m, BOLA_X + 6, 26 + SHOE_DY); q1 = _mapa(m, BOLA_X + 1, yb - 2)
    cv.drawLine(q0[0], q0[1], q1[0], q1[1], paint(LONA_LINHA, int(220 * k), "stroke", 3.4))
    for dx in (-10, 12):
        a0 = _mapa(m, BOLA_X + dx, 30 + SHOE_DY); a1 = _mapa(m, BOLA_X + dx * 0.5, 44 + SHOE_DY)
        cv.drawLine(a0[0], a0[1], a1[0], a1[1], paint(LONA_LINHA, int(150 * k), "stroke", 2.4))
    return joe, hip_r


def _inversa(m):
    inv = skia.Matrix()
    m.invert(inv)
    return inv


def cena_sala(cv, t, T, cam, e):
    cv.save(); aplica(cv, cam)
    sala(cv)
    # a caixa do tênis caro na prateleira (a tampa fecha sozinha em "custa")
    x0, yb, w, h = CAIXA3

    def _dentro(c):
        mm = _mat(x0 + 48, yb - 6 - sola_y("caro") * 0.9, -3.0, 0.9)
        tenis_frente(c, mm, "caro", 1.0, dour=0.25, vazio=True)
        etiqueta(c, mm, 6.0, 4, 1.0)
    caixa_tampa_fecha(cv, x0, yb, w, h, e["tampa"], 1.0, _dentro)
    # "seguro": o piso varrido ganha um contorno verde suave (as bordas do tapete)
    if e.get("seguro_a", 0) > 0:
        a = e["seguro_a"]
        for y in (TAP_Y0 + 2, TAP_Y1 - 2):
            cv.drawLine(-300, y, 1900, y, paint(VERDE, int(120 * a), "stroke", 18, blur=8))
            cv.drawLine(-300, y, 1900, y, paint(VERDE, int(255 * a), "stroke", 5))
    # as pernas: a de trás (mais escura), a da frente e o short por cima
    hip = e["hip"]
    pes = e["pes"]
    perto, longe = pes[0], pes[1]
    hip_l = (hip[0] + LONGE_DX, hip[1] + LONGE_DY)
    sombra_pe(cv, longe, Y3 + LONGE_DY, 0.9, longe.arco)
    sombra_pe(cv, perto, Y3, 0.9, perto.arco)
    kl, _ = perna(cv, hip_l, longe, longe=True)
    short_perna(cv, hip_l, kl, ESC3, longe=True)
    kp, _ = perna(cv, hip, perto)
    corpo_baixo(cv, hip, ESC3)
    short_perna(cv, hip, kp, ESC3)
    if e["verde3"] > 0:
        luz_sola(cv, pes[e["apoio"]], VERDE, e["verde3"] * (0.75 + 0.25 * math.sin(t * 9)))
    cv.restore()


# ================================================================== HUD do VAR (desenho próprio, cópia do piloto)
def fundo(cv, t):
    def _d(c):
        sh = skia.GradientShader.MakeRadial(skia.Point(W / 2, H * 0.42), H * 0.75, [_c(ARD_IN), _c(ARD_OUT)])
        c.drawRect(skia.Rect(0, 0, W, H), paint(ARD_IN, shader=sh))
    cv.drawImage(cacheado("fundo", W, H, _d), 0, 0)


def vinheta(cv):
    def _d(c):
        c.translate(-JX0, -JY0)
        vin = skia.GradientShader.MakeRadial(skia.Point(JCX, JCY), 760, [_c("#000000", 0), _c("#000000", 0), _c("#000000", 90)],
                                             [0.0, 0.62, 1.0])
        c.drawRect(JAN, paint("#000000", shader=vin))
    cv.drawImage(cacheado("vinheta", JX1 - JX0, JY1 - JY0, _d), JX0, JY0)


def capa(cv, t, t_sai, linha1, linha2):
    """Gancho de 2 linhas ACIMA do monitor (não encosta na janela da cena)."""
    sai = e_inout(prog(t, t_sai, t_sai + 0.45))
    if sai >= 1:
        return
    a = 1 - sai
    pulso = 1 + 0.02 * math.sin(t * 5)
    cv.save(); cv.translate(CX, 168 - 50 * sai); cv.scale(pulso, pulso)
    texto(cv, linha1, 0, 0, F_BLACK, 74, "#FFFFFF", int(255 * a), contorno=10)
    texto(cv, linha2, 0, 84, F_BLACK, 74, "#F5C04A", int(255 * a), contorno=10)
    cv.restore()


def moldura(cv, t, a, varre=0.0):
    """Cantoneiras em L nos cantos da janela, fio ciano e varredura SÓ nas bordas."""
    if a <= 0:
        return
    rr = skia.RRect.MakeRectXY(JAN, JAN_R, JAN_R)
    cv.drawRRect(rr, paint(CIANO, int(70 * a), "stroke", 2))
    cv.save(); cv.clipRRect(rr, skia.ClipOp.kIntersect, True)
    inner = skia.RRect.MakeRectXY(skia.Rect(JX0 + 36, JY0 + 36, JX1 - 36, JY1 - 36), 10, 10)
    cv.clipRRect(inner, skia.ClipOp.kDifference, True)
    off = (t * 24) % 6
    y = JY0 + off
    pl = paint("#FFFFFF", int(26 * a), "stroke", 2)
    while y < JY1:
        cv.drawLine(JX0, y, JX1, y, pl); y += 6
    cv.restore()
    if varre > 0:
        cv.save(); cv.clipRRect(rr, skia.ClipOp.kIntersect, True)
        y = lerp(JY0 - 80, JY1 + 20, varre)
        sh = skia.GradientShader.MakeLinear([skia.Point(0, y - 70), skia.Point(0, y + 10)],
                                            [_c(CIANO, 0), _c(CIANO, int(70 * a)), _c(CIANO, 0)], [0.0, 0.8, 1.0])
        cv.drawRect(skia.Rect(JX0, y - 70, JX1, y + 10), paint(CIANO, shader=sh))
        cv.drawLine(JX0, y, JX1, y, paint(CIANO, int(120 * a), "stroke", 2))
        cv.restore()
    for (x, y, sx, sy) in ((JX0, JY0, 1, 1), (JX1, JY0, -1, 1), (JX0, JY1, 1, -1), (JX1, JY1, -1, -1)):
        p = skia.Path(); p.moveTo(x + 6 * sx, y + 76 * sy); p.lineTo(x + 6 * sx, y + 6 * sy); p.lineTo(x + 76 * sx, y + 6 * sy)
        cv.drawPath(p, paint("#000000", int(110 * a), "stroke", 13, blur=3))
        cv.drawPath(p, paint("#FFFFFF", int(255 * a), "stroke", 7))
        cv.drawPath(p, paint(CIANO, int(255 * a), "stroke", 2))


def selo_var(cv, t, x, y, esc, a, chip=None, a_chip=1.0, pontos=-1.0, cor_chip="#FFFFFF", flash=0.0):
    """Caixa VAR + chip de estado à direita (x, y = canto sup. esq.)."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    f = skia.Font(F_BLACK, 52); lw = f.measureText(T_VAR)
    rr = skia.RRect.MakeRectXY(skia.Rect(0, 0, lw + 36, 64), 10, 10)
    cv.drawRRect(rr, paint("#000000", int(100 * a), blur=10))
    cv.drawRRect(rr, paint(SELO_BG, int(250 * a)))
    cv.drawRRect(rr, paint(CIANO, int(255 * a), "stroke", 4))
    texto(cv, T_VAR, 18, 52, F_BLACK, 52, "#FFFFFF", int(255 * a), centro=False)
    if chip and a_chip > 0:
        aa = a * a_chip
        fc = skia.Font(F_BLACK, 34); cw = fc.measureText(chip)
        extra = 70 if pontos >= 0 else 0
        x0 = lw + 50
        r2 = skia.RRect.MakeRectXY(skia.Rect(x0, 8, x0 + cw + 70 + extra, 56), 24, 24)
        cv.drawRRect(r2, paint(CARTAO, int(235 * aa)))
        if flash > 0:
            cv.drawRRect(r2, paint("#FFFFFF", int(200 * flash * aa)))
        cv.drawRRect(r2, paint(cor_chip, int((230 if cor_chip != "#FFFFFF" else 60) * aa), "stroke", 3 if cor_chip != "#FFFFFF" else 2))
        pisca = 0.55 + 0.45 * math.sin(t * 9)
        ponto = cor_chip if cor_chip != "#FFFFFF" else CIANO
        cv.drawCircle(x0 + 26, 32, 8, paint(ponto, int(255 * aa * (1.0 if cor_chip != "#FFFFFF" else pisca))))
        texto(cv, chip, x0 + 46, 44, F_BLACK, 34, cor_chip, int(255 * aa), centro=False)
        if pontos >= 0:
            for i in range(3):
                acesa = pontos > i / 3 + 0.02
                cv.drawCircle(x0 + 46 + cw + 22 + i * 22, 33, 7, paint(CIANO if acesa else "#FFFFFF", int(255 * aa) if acesa else int(70 * aa)))
    cv.restore()


def icone_pausa(cv, x, y, a):
    if a <= 0:
        return
    for dx in (-14, 14):
        r = skia.RRect.MakeRectXY(skia.Rect(x + dx - 8, y - 26, x + dx + 8, y + 26), 4, 4)
        cv.drawRRect(r, paint("#000000", int(110 * a), blur=6))
        cv.drawRRect(r, paint(CIANO, int(255 * a)))


def icone_rebobina(cv, x, y, a):
    if a <= 0:
        return
    for dx in (-24, 8):
        p = poli([(x + dx + 26, y - 24), (x + dx + 26, y + 24), (x + dx - 8, y)])
        cv.drawPath(p, paint("#000000", int(110 * a), blur=6))
        cv.drawPath(p, paint(CIANO, int(255 * a)))


def circulo_tele(cv, x, y, rx, ry, k, a, seed=0.0, pulso=0.0, cor=CIANO):
    """Círculo de caneta do telestrador: traço com tremor, desenhado em `k` (0..1)."""
    if a <= 0 or k <= 0:
        return
    n = 72
    pts = []
    for i in range(n + 10):
        u = i / n
        ang = -math.pi * 0.62 + 2 * math.pi * u
        wob = 1 + 0.035 * math.sin(u * 2 * math.pi * 3 + seed) + 0.018 * math.sin(u * 2 * math.pi * 7 + 2 * seed)
        sp = 1 + 0.07 * u
        esc = (1 + 0.05 * pulso) * wob * sp
        pts.append((x + rx * esc * math.cos(ang), y + ry * esc * math.sin(ang)))
    p = poli(pts, fechar=False)
    cv.drawPath(p, _trim(paint(CARTAO, int(150 * a), "stroke", 15), k))
    cv.drawPath(p, _trim(paint(cor, int(110 * a * (0.6 + 0.4 * pulso)), "stroke", 18, blur=8), k))
    cv.drawPath(p, _trim(paint(cor, int(255 * a), "stroke", 8), k))


def carimbo_cor(cv, s, x, y, rot, t0, t, dur, cor, tam=88, esc0=1.9, sub=None, tam_sub=44):
    """Carimbo do veredito: OPACO, cor do semáforo, entra batendo e sai encolhendo para o chip do selo.
    `sub`: 2ª linha dentro do mesmo carimbo (a condição: NÃO MOLDA O ARCO). (cópia do cf_var_gesso)"""
    k = t - t0
    if k < 0 or k > dur:
        return
    esc = lerp(esc0, 1.0, e_out(clamp(k / 0.16)))
    sai = prog(k, dur - 0.28, dur)
    esc *= lerp(1.0, 0.35, e_inout(sai))
    a = clamp(k / 0.06) * (1 - sai)
    xx = lerp(x, 330, e_inout(sai)); yy = lerp(y, 180, e_inout(sai))
    cv.save(); cv.translate(xx, yy); cv.rotate(rot * (1 - sai)); cv.scale(esc, esc)
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    baixo = tam * 0.38 + (tam_sub * 1.25 if sub else 0)
    lw2 = skia.Font(F_BLACK, tam_sub).measureText(sub) if sub else 0
    meia = max(lw, lw2) / 2
    rr = skia.RRect.MakeRectXY(skia.Rect(-meia - 32, -tam * 1.02, meia + 32, baixo), 16, 16)
    cv.drawRRect(rr, paint("#000000", int(110 * a), blur=16))
    cv.drawRRect(rr, paint(CARTAO, int(245 * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 9))
    rr2 = skia.RRect.MakeRectXY(skia.Rect(-meia - 20, -tam * 0.9, meia + 20, baixo - tam * 0.12), 10, 10)
    cv.drawRRect(rr2, paint(cor, int(120 * a), "stroke", 2.5))
    cv.drawString(s, -lw / 2, 0, f, paint(cor, int(255 * a)))
    if sub:
        cv.drawLine(-meia + 6, tam * 0.2, meia - 6, tam * 0.2, paint(cor, int(150 * a), "stroke", 2.5))
        texto(cv, sub, 0, tam * 0.2 + tam_sub * 1.02, F_BLACK, tam_sub, "#FFFFFF", int(255 * a))
    cv.restore()


def ruido_vhs(cv, t, a):
    """Faixas de ruído correndo (fita rebobinando)."""
    if a <= 0:
        return
    rng = np.random.default_rng(int(t * 60))
    cv.save(); cv.clipRRect(skia.RRect.MakeRectXY(JAN, JAN_R, JAN_R), skia.ClipOp.kIntersect, True)
    for k in range(3):
        yc = JY0 + ((t * (900 + 300 * k) + k * 330) % (JY1 - JY0))
        hb = 14 + 8 * k
        cv.drawRect(skia.Rect(JX0, yc, JX1, yc + hb), paint("#FFFFFF", int(40 * a)))
        for _ in range(26):
            x = rng.uniform(JX0, JX1); w = rng.uniform(10, 90); yy = yc + rng.uniform(0, hb)
            cv.drawLine(x, yy, x + w, yy, paint("#FFFFFF", int(rng.uniform(80, 200) * a), "stroke", rng.uniform(1, 3)))
    cv.restore()


def busto(cv, x, y, esc, cor, a):
    """Busto simples, sem mão, sem instrumento, sem rosto (cópia do piloto)."""
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    om = skia.Path(); om.addRRect(skia.RRect.MakeRectXY(skia.Rect(-56, -6, 56, 74), 46, 46))
    clip = skia.Path(); clip.addRect(skia.Rect(-60, -10, 60, 58))
    om = skia.Op(om, clip, skia.PathOp.kIntersect_PathOp)
    cv.drawPath(om, paint("#000000", int(80 * a), blur=8))
    cv.drawPath(om, paint(cor, int(255 * a)))
    gola = skia.Path(); gola.moveTo(-16, -4); gola.lineTo(0, 18); gola.lineTo(16, -4)
    cv.drawPath(gola, paint(CARTAO, int(150 * a), "stroke", 4))
    cv.drawCircle(0, -40, 30, paint("#000000", int(80 * a), blur=6))
    cv.drawCircle(0, -40, 30, paint("#EEF3F8", int(255 * a)))
    cv.drawArc(skia.Rect(-30, -70, 30, -10), 200, 140, False, paint(cor, int(255 * a), "stroke", 10))
    cv.restore()


def apito_icone(cv, x, y, esc, a, rot=-14.0):
    """Apito de árbitro (desenho, sem texto): corpo redondo, bocal e cordão ciano. (cópia do piloto)"""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(esc, esc)
    cv.drawArc(skia.Rect(-96, -40, -24, 40), 60, 240, False, paint(CIANO, int(230 * a), "stroke", 6))
    corpo_ = skia.Path(); corpo_.addCircle(0, 6, 38)
    corpo_ = uniao(corpo_, rr_path(-6, -34, 92, 2, 10))
    cv.drawPath(corpo_, paint("#000000", int(100 * a), blur=10))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, -34), skia.Point(0, 44)], [_c("#F4F8FB"), _c("#B9C6D3")])
    cv.drawPath(corpo_, paint("#DDE6EE", int(255 * a), shader=sh))
    cv.drawPath(corpo_, paint(CIANO, int(255 * a), "stroke", 4))
    cv.drawCircle(-4, 10, 13, paint(SELO_BG, int(255 * a)))
    cv.drawRect(skia.Rect(70, -30, 86, -2), paint(SELO_BG, int(200 * a)))
    cv.drawCircle(-40, 0, 7, paint(CIANO, int(255 * a), "stroke", 4))
    cv.restore()


def selo_serie(cv, a):
    if a <= 0:
        return
    lw = larg_texto(T_SERIE, F_BLACK, 36)
    rr = skia.RRect.MakeRectXY(skia.Rect(CX - lw / 2 - 34, 148, CX + lw / 2 + 34, 208), 30, 30)
    cv.drawRRect(rr, paint(SELO_BG, int(235 * a)))
    cv.drawRRect(rr, paint(CIANO, int(255 * a), "stroke", 3))
    texto(cv, T_SERIE, CX, 191, F_BLACK, 36, CIANO, int(255 * a))


def marca_x(cv, x, y, r, cor, a):
    """X desenhado (sem texto) num disco escuro: o contraexemplo."""
    if a <= 0:
        return
    cv.drawCircle(x, y, r + 6, paint("#000000", int(90 * a), blur=8))
    cv.drawCircle(x, y, r, paint(CARTAO, int(235 * a)))
    cv.drawCircle(x, y, r, paint(cor, int(255 * a), "stroke", 5))
    d = r * 0.45
    cv.drawLine(x - d, y - d, x + d, y + d, paint(cor, int(255 * a), "stroke", 9))
    cv.drawLine(x - d, y + d, x + d, y - d, paint(cor, int(255 * a), "stroke", 9))


def marca_ok(cv, x, y, r, cor, a):
    """Visto desenhado (sem texto) num disco escuro."""
    if a <= 0:
        return
    cv.drawCircle(x, y, r + 6, paint("#000000", int(90 * a), blur=8))
    cv.drawCircle(x, y, r, paint(CARTAO, int(235 * a)))
    cv.drawCircle(x, y, r, paint(cor, int(255 * a), "stroke", 5))
    p = poli([(x - r * 0.45, y + r * 0.02), (x - r * 0.12, y + r * 0.35), (x + r * 0.5, y - r * 0.32)], fechar=False)
    pt = paint(cor, int(255 * a), "stroke", 9); pt.setStrokeCap(skia.Paint.kRound_Cap); pt.setStrokeJoin(skia.Paint.kRound_Join)
    cv.drawPath(p, pt)


def calendario(cv, x, y, t, viradas, a, esc=1.5):
    """Calendário de folhas SEM número (cabeçalho azul-claro, nada de vermelho); vira uma folha em cada
    tempo de `viradas`. (desenho do cf_cameralenta_ponta_pes, com as viradas presas à fala)"""
    if a <= 0:
        return
    ent = lerp(0.6, 1.0, e_back(prog(t, viradas[0] - 0.12, viradas[0] + 0.18)))
    cv.save(); cv.translate(x, y); cv.scale(esc * ent, esc * ent); cv.translate(-48, -46)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(3, 5, 99, 97), 12, 12), paint("#000000", int(80 * a), blur=8))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(0, 0, 96, 92), 12, 12), paint("#EEF3F8", int(255 * a)))
    cv.save(); cv.clipRRect(skia.RRect.MakeRectXY(skia.Rect(0, 0, 96, 92), 12, 12), True)
    cv.drawRect(skia.Rect(0, 0, 96, 24), paint("#9CC9FF", int(255 * a)))
    cv.restore()
    for xx in (24, 72):
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(xx - 4, -8, xx + 4, 10), 3, 3), paint("#5E7186", int(255 * a)))
    for i in range(3):
        cv.drawLine(14, 42 + i * 16, 82, 42 + i * 16, paint("#9AA8B5", int(200 * a), "stroke", 4))
    for v0 in viradas:
        f = prog(t, v0, v0 + 0.22)
        if 0 < f < 1:
            cv.save(); cv.translate(0, 24); cv.scale(1, 1 - f)
            cv.drawRect(skia.Rect(0, 0, 96, 68), paint("#FFFFFF", int(200 * a * (1 - f))))
            cv.drawLine(0, 68, 96, 68, paint("#9AA8B5", int(200 * a * (1 - f)), "stroke", 2))
            cv.restore()
    cv.restore()


def ziguezague(cv, x, y, esc, a, rot=0.0):
    """'Dor' desenhada: zigue-zague âmbar com contorno (sem vermelho, sem rosto)."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(esc, esc)
    p = poli([(-26, 8), (-12, -10), (0, 8), (12, -10), (26, 8)], fechar=False)
    pt = paint(CARTAO, int(170 * a), "stroke", 13); pt.setStrokeJoin(skia.Paint.kRound_Join); cv.drawPath(p, pt)
    pt = paint(AMBAR, int(255 * a), "stroke", 7); pt.setStrokeJoin(skia.Paint.kRound_Join); cv.drawPath(p, pt)
    cv.restore()


def cadeado(cv, x, y, esc, a):
    """Cadeado âmbar pequeno ('durinho, travado'), sem texto."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    cv.drawArc(skia.Rect(-15, -34, 15, 0), 180, 180, False, paint(CARTAO, int(180 * a), "stroke", 12))
    cv.drawArc(skia.Rect(-15, -34, 15, 0), 180, 180, False, paint(AMBAR, int(255 * a), "stroke", 6))
    cv.drawLine(-15, -17, -15, -6, paint(AMBAR, int(255 * a), "stroke", 6))
    cv.drawLine(15, -17, 15, -6, paint(AMBAR, int(255 * a), "stroke", 6))
    corpo_ = rr_path(-24, -10, 24, 26, 7)
    cv.drawPath(corpo_, paint("#000000", int(90 * a), blur=6))
    cv.drawPath(corpo_, paint(AMBAR, int(255 * a)))
    cv.drawPath(corpo_, paint(CARTAO, int(200 * a), "stroke", 3))
    cv.drawCircle(0, 5, 5, paint(CARTAO, int(230 * a)))
    cv.drawLine(0, 6, 0, 16, paint(CARTAO, int(230 * a), "stroke", 4))
    cv.restore()


# palavras de ligação: nunca terminam um bloco nem uma linha da legenda (cópia do cf_var_gesso)
LIGACAO = {"a", "o", "as", "os", "e", "de", "da", "do", "das", "dos", "em", "no", "na", "nos", "nas", "um", "uma",
           "pra", "que", "com", "é", "sua", "seu", "lá", "ele", "ou", "não", "sem"}
ESP_LEG, LARG_LEG = 26, 920


def _base_tok(p):
    import re
    return re.sub(r"[.,:;!?—]", "", p["tok"]).lower()


def partir_linhas(bloco, tam):
    """Linhas da legenda de um bloco (quebra equilibrada, sem linha terminando em palavra de ligação). (cópia)"""
    from itertools import combinations
    ws = [(p, larg_texto(p["tok"].upper(), F_BLACK, tam)) for p in bloco]

    def larg(seg):
        return sum(w for _, w in seg) + ESP_LEG * (len(seg) - 1)
    gul, linha, lw = [], [], 0
    for p, w in ws:
        if linha and lw + ESP_LEG + w > LARG_LEG:
            gul.append(linha); linha, lw = [], 0
        linha.append((p, w)); lw += (ESP_LEG if lw else 0) + w
    if linha:
        gul.append(linha)
    k = len(gul)
    if k <= 1 or len(ws) > 12:
        return gul
    melhor = None
    for cortes in combinations(range(1, len(ws)), k - 1):
        lims = (0,) + cortes + (len(ws),)
        lns = [ws[lims[j]:lims[j + 1]] for j in range(k)]
        if any(larg(ln) > LARG_LEG for ln in lns):
            continue
        sc = max(larg(ln) for ln in lns)
        for ln in lns[:-1]:
            if _base_tok(ln[-1][0]) in LIGACAO:
                sc += 400
            if ln[-1][0].get("virg"):
                sc -= 60
        if len(lns[-1]) == 1 and len(ws) > k:
            sc += 150
        if melhor is None or sc < melhor[0]:
            melhor = (sc, lns)
    return melhor[1] if melhor else gul


def montar_blocos_var(pal):
    """Blocos da legenda (cópia do cf_var_gesso): frase por frase, um bloco só se tiver até 6 palavras E couber
    em 2 linhas; senão divide no melhor ponto, nunca depois de palavra de ligação."""
    frases = []
    for b in montar_blocos(pal):
        if frases and not frases[-1][-1]["fim_frase"]:
            frases[-1] = frases[-1] + b
        else:
            frases.append(list(b))

    def dividir(fr):
        if fr[0]["w"].lower() == "manda" or (len(fr) <= 6 and len(partir_linhas(fr, 80)) <= 2):
            return [fr]
        melhor = None
        for i in range(1, len(fr)):
            sc = abs(i - (len(fr) - i))
            if _base_tok(fr[i - 1]) in LIGACAO:
                sc += 100
            if fr[i - 1].get("virg"):
                sc -= 3
            if _base_tok(fr[i]) in ("e", "mas"):
                sc -= 2
            if i == 1 or len(fr) - i == 1:
                sc += 3
            if i < len(fr) - i:
                sc += 0.25
            if melhor is None or sc < melhor[0]:
                melhor = (sc, i)
        i = melhor[1]
        return dividir(fr[:i]) + dividir(fr[i:])
    blocos = []
    for fr in frases:
        blocos += dividir(fr)
    return blocos


def legenda_var(cv, blocos, t, destaque, y_base=1395, tam=80, a_extra=1.0):
    """Legenda karaokê do piloto (palavra ativa cresce do próprio centro), quebra equilibrada. (cópia)"""
    import re
    if a_extra <= 0:
        return
    vivo = None
    for i, b in enumerate(blocos):
        ini = b[0]["t"] - 0.12
        fim = blocos[i + 1][0]["t"] - 0.12 if i + 1 < len(blocos) else b[-1]["t"] + b[-1]["d"] + 2.5
        if ini <= t < fim:
            vivo = b; break
    if not vivo:
        return
    esp = ESP_LEG
    linhas = partir_linhas(vivo, tam)
    entrada_ = e_out(clamp((t - (vivo[0]["t"] - 0.12)) / 0.15))
    a_x = clamp(a_extra)
    alt = tam * 1.18
    y = y_base - (len(linhas) - 1) * alt / 2 + (1 - entrada_) * 24
    for ln in linhas:
        total = sum(w for _, w in ln) + esp * (len(ln) - 1); x = CX - total / 2
        for p, w in ln:
            k = t - p["t"]; base = re.sub(r"[.,:;!?—]", "", p["tok"]).lower()
            dita = k >= -0.03; falando = p["t"] - 0.03 <= t <= p["t"] + p["d"] + 0.06
            cor, a = (OURO, 255) if falando else ((OURO if base in destaque else "#FFFFFF"), 255) if dita else ("#FFFFFF", 105)
            esc = 1.0 + (min(0.06, 14.0 / max(w, 1.0)) * (1 - e_out(clamp(k / 0.16))) if dita else 0.0)
            cv.save(); cv.translate(x + w / 2, y); cv.scale(esc, esc)
            texto(cv, p["tok"].upper(), -w / 2, 0, F_BLACK, tam, cor, int(a * entrada_ * a_x), centro=False, contorno=12)
            cv.restore()
            x += w + esp
        y += alt


def interface_var(cv, t, T, blocos, destaque):
    """Cópia do cf_comum.interface (rodapé CFM a partir de 3 s, cartão final com a CTA e o aviãozinho)."""
    t_cta = T["manda"] - 0.15
    if t < t_cta:
        legenda_var(cv, blocos, t, destaque)
    if 3.0 <= t < t_cta:
        a = prog(t, 3.0, 3.6)
        texto(cv, SIG, CX, 1585, F_SEMI, 27, "#FFFFFF", int(200 * a))
        texto(cv, DISC, CX, 1620, F_REG, 23, "#FFFFFF", int(150 * a))
    if t >= t_cta:
        a = prog(t, t_cta, t_cta + 0.35)
        cv.drawRect(skia.Rect(0, 0, W, H), paint(BG_OUT, int(175 * a)))
        legenda_var(cv, blocos, t, destaque, y_base=700, tam=92)
        aviao(cv, t, T["manda"] + 0.2)
        rr = skia.RRect.MakeRectXY(skia.Rect(150, 1060, 930, 1214), 28, 28)
        cv.drawRRect(rr, paint("#0B1824", int(230 * a))); cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 3))
        texto(cv, "Dr. Rafael Vargas · Médico ortopedista", CX, 1112, F_BLACK, 36, "#FFFFFF", int(255 * a))
        texto(cv, "CRM-SP 226103 · RQE 137901 · @rafaelvargasmd", CX, 1154, F_SEMI, 28, OURO, int(255 * a))
        texto(cv, DISC, CX, 1190, F_REG, 22, "#FFFFFF", int(170 * a))


# ================================================================== quadro
VEREDITOS = (("pode1", "anulado1", T_ANUL, AMBAR), ("pode2", "anulado2", T_ANUL, AMBAR),
             ("pode3", "validado", T_VALID, VERDE))
DUR_CARIMBOS = (1.35, 1.5, 1.35)
POS_CARIMBOS = ((790.0, 450.0), (790.0, 440.0), (800.0, 420.0))
SUB_CARIMBOS = (None, T_ARCO, None)


def chip_estado(t, T):
    """(texto, alfa, pontos, cor, flash) do chip: LANCE n -> CHECANDO -> (carimbo) -> veredito -> JEITO CERTO."""
    cortes = (0.0, T["palmilha1"], T["descalco"], 1e9)
    certo = (T["wipe"] + 0.14, T["flexivel"] - 0.02, T["fortalece"] - 0.02)
    for k, (pd, vd, s, cor) in enumerate(VEREDITOS):
        if not (cortes[k] <= t < cortes[k + 1]):
            continue
        flash = 0.0
        if t < T[pd + "_fim"] + 0.04:
            a = 1.0
            if k == 1:
                a = prog(t, cortes[k] + 0.02, cortes[k] + 0.12)
                flash = 1 - prog(t, cortes[k] + 0.06, cortes[k] + 0.3)
            elif k == 2:
                a = prog(t, cortes[k] + 0.45, cortes[k] + 0.6)
            return T_LANCE[k], a, -1, "#FFFFFF", flash
        if t < T[vd] - 0.04:
            t0 = T[pd + "_fim"] + 0.04
            return T_CHEC, 1.0, prog(t, t0, T[vd] - 0.12), "#FFFFFF", 0.0
        dur = DUR_CARIMBOS[k]
        if t < T[vd] + dur - 0.05:
            return None, 0.0, -1, "#FFFFFF", 0.0
        if t >= certo[k]:
            return T_CERTO, prog(t, certo[k], certo[k] + 0.18), -1, VERDE, 0.0
        a = prog(t, T[vd] + dur - 0.1, T[vd] + dur + 0.1) * (1 - prog(t, certo[k] - 0.12, certo[k]))
        return s, a, -1, cor, 0.0
    return None, 0.0, -1, "#FFFFFF", 0.0


def cena(cv, t, T):
    """O lance da vez (com a cortina do VAR no jeito certo do lance 1). Devolve o que o HUD precisa."""
    info = {}
    if t < T["descalco"]:
        e = estado_entrada(t, T)
        cam = cam_entrada(t, T)
        kw = prog(t, T["wipe"], T["wipe"] + 0.36)
        if kw <= 0 or kw >= 1:
            pe, meio = cena_entrada(cv, t, T, cam, e)
            info.update(lance=1 if t < T["palmilha1"] else 2, cam=cam, e=e, pe=pe, meio=meio)
        else:
            xw = lerp(JX0 - 10, JX1 + 10, e_inout(kw))
            cv.save(); cv.clipRect(skia.Rect(xw, 0, W, H), True)
            pe, meio = cena_entrada(cv, t, T, cam, estado_entrada(t, T, certo=False))
            cv.restore()
            cv.save(); cv.clipRect(skia.Rect(0, 0, xw, H), True)
            cena_entrada(cv, t, T, cam, estado_entrada(t, T, certo=True))
            cv.restore()
            cv.drawLine(xw, JY0, xw, JY1, paint(CIANO, 160, "stroke", 26, blur=10))
            cv.drawLine(xw, JY0, xw, JY1, paint("#FFFFFF", 255, "stroke", 6))
            info.update(lance=1, cam=cam, e=e, pe=pe, meio=meio, xw=xw)
    else:
        e = estado_sala(t, T)
        cam = cam_sala(t, T, e)
        e["seguro_a"] = janela(t, T["seguro"] - 0.02, T["pode3"] - 0.05, 0.2, 0.25)
        cena_sala(cv, t, T, cam, e)
        info.update(lance=3, cam=cam, e=e)
    return info


def hud_lances(cv, t, T, info):
    """Grafismo sobre a imagem (coordenadas de tela, dentro da janela)."""
    lance = info.get("lance")
    cam = info.get("cam")
    if lance is None:
        return
    s = cam[0]
    e = info["e"]
    if lance in (1, 2):
        pe_ref = Pe(X_PE, Y_PAIRA, 0, 0, 0, ESC)
        ax, ay = na_tela(cam, *pe_ref.ponto(30, Y_SOLA + 6))
        if lance == 1 and not e["certo"]:
            # círculo no tênis + meio do pé (a seta de moldar)
            bx, by = na_tela(cam, *_mapa(CARO_M, 30, 20))
            cx_, cy_ = (ax + bx) / 2 - 10 * s, (ay + by) / 2
            k1 = e_out(prog(t, T["pode1"] + 0.12, T["pode1"] + 0.47))
            k0 = 1.0 if t < T["var"] else 0.0
            fora = 1 - prog(t, T["anulado1"] + 0.3, T["anulado1"] + 0.55)
            a_c = max(k0 * (1 - prog(t, T["var"], T["var"] + 0.12)), k1 * fora)
            k_tr = 1.0 if t < T["var"] else k1
            pul = 0.5 + 0.5 * math.sin(t * 8) if t < T["var"] or T["pode1_fim"] < t < T["anulado1"] else 0.0
            pul += 1.5 * max(0.0, 1 - abs(t - T["chama"] - 0.1) / 0.18)
            circulo_tele(cv, cx_, cy_, 170 * s, 150 * s, k_tr, a_c, 0.7, pul)
        if lance == 1 and info.get("meio") is not None:
            a_x = janela(t, T["molda1"] - 0.04, T["molda1"] + 0.32, 0.1, 0.18)
            if a_x > 0:
                mx, my = info["meio"]
                k_x = e_back(prog(t, T["molda1"] - 0.04, T["molda1"] + 0.2))
                cv.save(); cv.translate(*na_tela(cam, mx, my)); cv.scale(clamp(k_x, 0, 1.2), clamp(k_x, 0, 1.2))
                marca_x(cv, 0, 0, 40, AMBAR, a_x)
                cv.restore()
        if lance == 1 and e["certo"] and e["tele_dobra"] > 0:
            m_s = _mat(X_PE, Y_CHAO - sola_y("simples") * ESC, 0, ESC)
            dx_, dy_ = na_tela(cam, *_mapa(m_s, BOLA_X + 18, sola_y("simples") - 10))
            k_tl = e_out(prog(t, T["protege_fim"] + 0.06, T["protege_fim"] + 0.36))
            circulo_tele(cv, dx_, dy_, 120 * s, 64 * s, k_tl, e["tele_dobra"], 3.3, 0.0, VERDE)
        if lance == 1 and e["certo"] and e["ok1"] > 0:
            ox, oy = na_tela(cam, *_mapa(_mat(X_PE, Y_CHAO - sola_y("simples") * ESC, 0, ESC), -110, -10))
            k_ok = e_back(prog(t, T["protege_fim"] + 0.4, T["protege_fim"] + 0.63))
            cv.save(); cv.translate(ox, oy); cv.scale(clamp(k_ok, 0, 1.2), clamp(k_ok, 0, 1.2))
            marca_ok(cv, 0, 0, 38, VERDE, e["ok1"])
            cv.restore()
        if lance == 2:
            # círculo no calombo da palmilha + meio do pé
            bx, by = na_tela(cam, PALM_X + TOPO_CALOMBO[0] * ESC, Y_CHAO - 20)
            cx_, cy_ = (ax + bx) / 2 - 10 * s, (ay + by) / 2
            k1 = e_out(prog(t, T["pode2"] + 0.12, T["pode2"] + 0.47))
            fora = 1 - prog(t, T["anulado2"] + 0.3, T["anulado2"] + 0.55)
            pul = 0.5 + 0.5 * math.sin(t * 8) if T["pode2_fim"] < t < T["anulado2"] else 0.0
            circulo_tele(cv, cx_, cy_, 175 * s, 160 * s, k1, k1 * fora, 4.3, pul)
            a_x = janela(t, T["molda2"] - 0.04, T["molda2"] + 0.32, 0.1, 0.18)
            if a_x > 0 and info.get("meio") is not None:
                mx, my = info["meio"]
                k_x = e_back(prog(t, T["molda2"] - 0.04, T["molda2"] + 0.2))
                cv.save(); cv.translate(*na_tela(cam, mx, my)); cv.scale(clamp(k_x, 0, 1.2), clamp(k_x, 0, 1.2))
                marca_x(cv, 0, 0, 40, AMBAR, a_x)
                cv.restore()
            a_cal = janela(t, e["viradas"][0] - 0.12, T["descalco"] - 0.02, 0.15, 0.05)
            calendario(cv, JX1 - 150, JY0 + 140, t, e["viradas"], a_cal, 1.5)
    else:
        pes = e["pes"]
        cx_ = sum(na_tela(cam, *p.ponto(40, 30))[0] for p in pes) / 2
        cy_ = sum(na_tela(cam, *p.ponto(40, 30))[1] for p in pes) / 2
        k1 = e_out(prog(t, T["pode3"] + 0.12, T["pode3"] + 0.47))
        fora = 1 - prog(t, T["validado"] + 0.3, T["validado"] + 0.55)
        pul = 0.5 + 0.5 * math.sin(t * 8) if T["pode3_fim"] < t < T["validado"] else 0.0
        circulo_tele(cv, cx_, cy_ + 10 * s, 210 * s, 120 * s, k1, k1 * fora, 2.1, pul)
        # "piso": varredura ciano rente ao chão, da esquerda para a direita (nada pelo caminho)
        kv = prog(t, T["piso"] - 0.05, T["piso"] + 0.55)
        if 0 < kv < 1:
            y0 = na_tela(cam, 0, TAP_Y0 - 30)[1]; y1 = min(JY1, na_tela(cam, 0, TAP_Y1 + 40)[1])
            x = lerp(JX0 - 60, JX1 + 60, e_inout(kv))
            a_v = 1 - prog(kv, 0.85, 1.0)
            sh = skia.GradientShader.MakeLinear([skia.Point(x - 140, 0), skia.Point(x, 0)], [_c(CIANO, 0), _c(CIANO, int(110 * a_v))])
            cv.drawRect(skia.Rect(x - 140, y0, x, y1), paint(CIANO, shader=sh))
            cv.drawLine(x, y0, x, y1, paint("#FFFFFF", int(230 * a_v), "stroke", 5))
            cv.drawLine(x, y0, x, y1, paint(CIANO, int(140 * a_v), "stroke", 18, blur=8))
        if e["etq_a"] > 0:
            k_e = e_back(prog(t, T["custa"] - 0.12, T["custa"] + 0.16))
            etiqueta_vazia(cv, JX0 + 330, JY0 + 360, 2.3 * clamp(k_e, 0, 1.2), e["etq_a"], t, T["nada"] - 0.04)
        a_ok = janela(t, T["pe3"] - 0.06, T["off"], 0.12, 0.1)
        if a_ok > 0:
            p = pes[e["apoio"]]
            ox, oy = na_tela(cam, *p.ponto(170, 6))
            k_ok = e_back(prog(t, T["pe3"] - 0.06, T["pe3"] + 0.2))
            cv.save(); cv.translate(ox, oy); cv.scale(clamp(k_ok, 0, 1.2), clamp(k_ok, 0, 1.2))
            marca_ok(cv, 0, 0, 40, VERDE, a_ok)
            cv.restore()


# ---------- o fecho: o VAR saiu; o pé que merece avaliação; quem apita é o ortopedista
CART_A0 = (540.0, 760.0, 1.0)


def cartao_pe(cv, cx, cy, esc, a, arco, t, dedos=0.0, dor=0.0, trava=0.0, alvo=0.0, alvo_k=0.0, luz=0.0):
    """Cartão claro com um pé de perfil num chão (o mesmo desenho do vídeo). Coordenadas de tela."""
    if a <= 0:
        return
    w, h = 500.0, 400.0
    cv.save(); cv.translate(cx, cy); cv.scale(esc, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-w / 2, -h / 2, w / 2, h / 2), 26, 26)
    cv.drawRRect(rr, paint("#000000", int(110 * a), blur=16))
    cv.saveLayerAlpha(None, int(255 * a))
    cv.clipRRect(rr, skia.ClipOp.kIntersect, True)
    sh = skia.GradientShader.MakeLinear([skia.Point(0, -h / 2), skia.Point(0, 90)], [_c(PAREDE_A), _c(PAREDE_B)])
    cv.drawRect(skia.Rect(-w / 2, -h / 2, w / 2, 122), paint(PAREDE_A, shader=sh))
    cv.drawRect(skia.Rect(-w / 2, 122, w / 2, h / 2), paint(PISO))
    cv.drawLine(-w / 2, 122, w / 2, 122, paint(PISO_ESC, 200, "stroke", 3))
    pe = Pe(-112 + 31 * 2.0, 152 - Y_SOLA * 2.0, 0.0, dedos, arco, 2.0)
    sombra_pe(cv, pe, 152, 1.0, arco)
    perna(cv, (0, 0), pe, so_pe=True)
    if luz > 0:
        luz_sola(cv, pe, "#FFFFFF", luz, larg=6.0)
    cv.restore()
    cv.drawRRect(rr, paint("#FFFFFF", int(200 * a), "stroke", 4))
    if dor > 0:
        for i, (x, y, r) in enumerate(((-150, 70, -24), (60, -60, 10), (196, 70, 34))):
            ziguezague(cv, x, y, 1.0 + 0.12 * math.sin(t * 10 + i * 2), dor, r)
    if trava > 0:
        px, py = pe.ponto(-30, -40)
        cadeado(cv, px - 50, py - 40, 1.4, trava)
    if alvo > 0:
        px, py = pe.ponto(36, 26)
        circulo_tele(cv, px, py + 6, 200, 96, alvo_k, alvo, 1.9, 0.0, AMBAR)
    cv.restore()


def disco_icone(cv, x, y, r, a, k, tipo):
    """Disco escuro com contorno âmbar e o ícone desenhado (sem texto): 'dor' (zigue-zague), 'trava' (cadeado)
    ou 'dif' (sinal de diferente, as duas linhas da sola não batem)."""
    if a <= 0 or k <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(k, k)
    cv.drawCircle(0, 0, r + 6, paint("#000000", int(90 * a), blur=8))
    cv.drawCircle(0, 0, r, paint(CARTAO, int(235 * a)))
    cv.drawCircle(0, 0, r, paint(AMBAR, int(255 * a), "stroke", 5))
    if tipo == "dor":
        ziguezague(cv, 0, 2, r / 32, a)
    elif tipo == "trava":
        cadeado(cv, 0, 6, r / 44, a)
    else:
        d = r * 0.46
        pt = paint(AMBAR, int(255 * a), "stroke", 0.2 * r); pt.setStrokeCap(skia.Paint.kRound_Cap)
        cv.drawLine(-d, -d * 0.36, d, -d * 0.36, pt)
        cv.drawLine(-d, d * 0.36, d, d * 0.36, pt)
        cv.drawLine(d * 0.42, -d * 0.98, -d * 0.42, d * 0.98, pt)
    cv.restore()


def cartao_par(cv, cx, cy, esc, a, luz=0.0, dif=0.0, dif_k=0.0):
    """Os DOIS pés da MESMA criança num cartão só (a mesma bermuda amarela, a mesma perna): o direito com a
    curvinha, o esquerdo (espelhado) chato. O âmbar marca a DIFERENÇA entre as duas linhas da sola (sinal de
    diferente entre elas), não circula 'o pé chato' sozinho."""
    if a <= 0:
        return
    w, h, ych, fe = 860.0, 540.0, 180.0, 1.2
    cv.save(); cv.translate(cx, cy); cv.scale(esc, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-w / 2, -h / 2, w / 2, h / 2), 26, 26)
    cv.drawRRect(rr, paint("#000000", int(110 * a), blur=16))
    cv.saveLayerAlpha(None, int(255 * a))
    cv.clipRRect(rr, skia.ClipOp.kIntersect, True)
    sh = skia.GradientShader.MakeLinear([skia.Point(0, -h / 2), skia.Point(0, ych)], [_c(PAREDE_A), _c(PAREDE_B)])
    cv.drawRect(skia.Rect(-w / 2, -h / 2, w / 2, ych), paint(PAREDE_A, shader=sh))
    cv.drawRect(skia.Rect(-w / 2, ych, w / 2, h / 2), paint(PISO))
    cv.drawLine(-w / 2, ych, w / 2, ych, paint(PISO_ESC, 200, "stroke", 3))
    hy = ych - Y_SOLA * fe - (L1 + L2 - 4) * LK * fe
    # o fundilho da bermuda une as duas pernas (é UMA criança)
    cv.drawPath(rr_path(-92, hy - 120, 92, hy + 92, 40), paint(SHORT))
    for lado, arco in ((-1, 0.0), (1, 1.2)):
        cv.save(); cv.scale(lado, 1)
        pe = Pe(106.0, ych - Y_SOLA * fe, 0.0, 0.0, arco, fe)
        hip = (pe.ax - 30.0, hy)
        sombra_pe(cv, pe, ych, 1.0, arco)
        joe, _ = perna(cv, hip, pe)
        short_perna(cv, hip, joe, fe)
        if luz > 0:                               # a linha da sola, grossa e contornada (curva x reta)
            pth = poli([pe.ponto(x, y + 3) for (x, y) in sola_pts(pe.arco)], fechar=False)
            for cor, al, lg in ((CARTAO, 150, 17), ("#FFFFFF", 120, 26), ("#FFFFFF", 255, 8)):
                pt = paint(cor, int(al * luz), "stroke", lg, blur=8 if lg == 26 else 0)
                pt.setStrokeCap(skia.Paint.kRound_Cap); cv.drawPath(pth, pt)
        cv.restore()
    cv.restore()
    cv.drawRRect(rr, paint("#FFFFFF", int(200 * a), "stroke", 4))
    disco_icone(cv, 0, ych - 18, 44, dif, dif_k, "dif")
    cv.restore()


def fecho(cv, t, T):
    P4 = T["pe4"]
    a = prog(t, P4 - 0.12, P4 + 0.1) * (1 - prog(t, T["manda"] - 0.35, T["manda"] - 0.1))
    if a <= 0:
        return
    kpar = e_inout(prog(t, T["chato2"] - 0.06, T["chato2"] + 0.26))
    sobe = e_inout(prog(t, T["ai"] - 0.1, T["ai"] + 0.35))
    ent = e_back(prog(t, P4 - 0.1, P4 + 0.25))
    # cartão A: UM pé de perfil (dói, durinho); em "chato" ele abre para o par
    if kpar < 1:
        ea = 1.3 * clamp(ent, 0, 1.2) * lerp(1.0, 0.86, kpar)
        dor = janela(t, T["doi"] - 0.04, T["chato2"] - 0.05, 0.12, 0.2)
        trava = janela(t, T["durinho"] - 0.04, T["chato2"] - 0.05, 0.12, 0.2)
        tenta = 0.0
        if trava > 0:
            k = t - T["durinho"]
            tenta = 3.0 * math.sin(k * 26) * janela(t, T["durinho"], T["durinho"] + 0.5, 0.05, 0.1)
        cartao_pe(cv, 540, 760, ea, a * (1 - kpar), 1.0, t, dedos=tenta, dor=dor, trava=trava)
    # o par: os dois pés da MESMA criança; em "lado" o sinal de diferente entre as duas solas
    if kpar > 0:
        kp = clamp(e_back(prog(t, T["chato2"] - 0.06, T["chato2"] + 0.3)), 0, 1.2)
        yp = lerp(760, 515, sobe)
        ep_ = lerp(1.0, 0.64, sobe) * lerp(0.84, 1.0, kp)
        luz = janela(t, T["chato2"] + 0.12, T["manda"] - 0.3, 0.2, 0.25)
        dif = janela(t, T["lado"] - 0.06, T["manda"] - 0.3, 0.12, 0.2)
        dif_k = clamp(e_back(prog(t, T["lado"] - 0.06, T["lado"] + 0.24)), 0, 1.2)
        cartao_par(cv, 540, yp, ep_, a * clamp(kpar * 1.6), luz=luz, dif=dif, dif_k=dif_k)
    # os três sinais JUNTOS enquanto o apito chega: dói (zigue-zague) | o par | durinho (cadeado)
    if sobe > 0:
        k1 = clamp(e_back(prog(t, T["ai"], T["ai"] + 0.3)), 0, 1.2)
        k2 = clamp(e_back(prog(t, T["ai"] + 0.12, T["ai"] + 0.42)), 0, 1.2)
        disco_icone(cv, 116, 515, 66, a * sobe, k1, "dor")
        disco_icone(cv, 964, 515, 66, a * sobe, k2, "trava")
    # quem apita é o ortopedista: o busto acende e o apito chega
    a_b = prog(t, T["ai"] - 0.05, T["ai"] + 0.25) * (1 - prog(t, T["manda"] - 0.35, T["manda"] - 0.1))
    if a_b > 0:
        kb = e_back(prog(t, T["ai"] - 0.05, T["ai"] + 0.35))
        acende = prog(t, T["ortopedista"] - 0.05, T["ortopedista"] + 0.3)
        cv.drawCircle(CX, 1000, 220, paint(TEAL, int((30 + 50 * acende) * a_b), blur=60))
        busto(cv, CX, 1030 + 40 * (1 - clamp(kb)), 1.9 * clamp(kb, 0, 1.2), lerpc("#4E9E94", TEAL, acende), a_b)
        pul = 1 + 0.06 * max(0.0, 1 - abs(t - T["ortopedista"] - 0.15) / 0.22)
        if pul > 1:
            cv.drawCircle(CX, 1000, 190 * pul, paint(TEAL, int(70 * (pul - 1) / 0.06), "stroke", 6, blur=4))
        ka = e_out(prog(t, T["quem"] - 0.05, T["apita"] + 0.15))
        if ka > 0:
            x = lerp(140, CX + 160, ka); y = lerp(330, 890, ka) - 60 * math.sin(math.pi * ka)
            balanco = 10 * math.sin(max(0.0, t - T["apita"]) * 9) * math.exp(-max(0.0, t - T["apita"]) * 3)
            apito_icone(cv, x, y, lerp(0.7, 1.0, ka), a_b * clamp(ka * 3), -14 + balanco)


def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    t_off = T["off"]
    k_v = prog(t, t_off, t_off + 0.14) ** 1.5; k_h = e_inout(prog(t, t_off + 0.13, t_off + 0.3))
    tela_ligada = t < t_off + 0.38
    jan_rr = skia.RRect.MakeRectXY(JAN, JAN_R, JAN_R)
    a_tv = 1 - prog(t, t_off + 0.6, t_off + 0.95)
    if a_tv > 0:
        cv.drawRRect(jan_rr, paint("#0E151D", int(255 * a_tv)))
    info = {}
    if tela_ligada:
        cv.save()
        if t >= t_off:
            sy = max(0.006, 1 - clamp(k_v)); sx = max(0.01, 1 - k_h)
            cv.translate(JCX, JCY); cv.scale(sx, sy); cv.translate(-JCX, -JCY)
        cv.clipRRect(jan_rr, skia.ClipOp.kIntersect, True)
        rebob = janela(t, T["var"], T["var"] + 0.5, 0.03, 0.06)
        if rebob > 0:
            cv.translate(6 * math.sin(t * 97) * rebob, 0)
        info = cena(cv, t, T)
        vinheta(cv)
        if t >= t_off:
            cv.drawRect(JAN, paint("#FFFFFF", int(235 * clamp(k_v * 2.6))))
        cv.restore()
        ruido_vhs(cv, t, rebob)
    if t_off <= t < t_off + 0.62:                       # a linha e o ponto de luz
        k = prog(t, t_off + 0.16, t_off + 0.62)
        a_lin = clamp((0.3 - (1 - k_v)) / 0.25)
        if t < t_off + 0.36 and a_lin > 0:
            w = (JX1 - JX0) / 2 * max(0.02, 1 - k_h)
            cv.drawLine(JCX - w, JCY, JCX + w, JCY, paint("#FFFFFF", int(240 * a_lin), "stroke", 6, blur=3))
            cv.drawLine(JCX - w, JCY, JCX + w, JCY, paint("#DFF6FF", int(255 * a_lin), "stroke", 3))
        r = lerp(10, 2, k)
        a_pt = prog(t, t_off + 0.18, t_off + 0.26) * (1 - k)
        cv.drawCircle(JCX, JCY, r * 3, paint(CIANO, int(120 * a_pt), blur=10))
        cv.drawCircle(JCX, JCY, r, paint("#FFFFFF", int(255 * a_pt)))

    a_hud = 1 - prog(t, t_off + 0.2, t_off + 0.45)

    # ---------- grafismo sobre a imagem (coordenadas de tela)
    if tela_ligada and a_hud > 0:
        cv.save(); cv.clipRRect(jan_rr, skia.ClipOp.kIntersect, True)
        if t < t_off:
            hud_lances(cv, t, T, info)
        for t0, forca in ((T["pode1"], 150), (T["pode2"], 150), (T["pode3"], 150), (T["descalco"], 190)):
            k = t - t0
            if 0 <= k < 0.16:
                cv.drawRect(JAN, paint("#FFFFFF", int(forca * (1 - k / 0.16))))
        cv.restore()
        varre = 0.0
        for pd, vd, _, _ in VEREDITOS:
            if T[pd + "_fim"] < t < T[vd]:
                varre = prog(t, T[pd + "_fim"], T[vd] - 0.05)
        moldura(cv, t, a_hud, varre)
        congelado = t < T["var"] or any(T[pd] + 0.02 <= t < T[vd] for pd, vd, _, _ in VEREDITOS)
        icone_pausa(cv, JX1 - 70, JY1 - 74, a_hud * (1.0 if congelado else 0.0))
        a_reb = janela(t, T["var"], T["var"] + 0.5, 0.03, 0.08)
        icone_rebobina(cv, JX1 - 76, JY1 - 74, a_hud * a_reb)
        for (pd, vd, s_, cor), dur, (px, py), sub in zip(VEREDITOS, DUR_CARIMBOS, POS_CARIMBOS, SUB_CARIMBOS):
            carimbo_cor(cv, s_, px, py, -5, T[vd] - 0.02, t, dur, cor, sub=sub)
        # rótulo grande do corte de lance (LANCE 3)
        k = t - T["descalco"]
        if -0.02 <= k < 0.6:
            a = prog(k, 0.0, 0.08) * (1 - prog(k, 0.42, 0.6))
            esc = lerp(1.25, 1.0, e_out(prog(k, 0.0, 0.16)))
            cv.save(); cv.translate(JX0 + 210, JY0 + 112); cv.scale(esc, esc)
            f = skia.Font(F_BLACK, 70); lw = f.measureText(T_LANCE[2])
            rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 34, -70, lw / 2 + 34, 26), 16, 16)
            cv.drawRRect(rr, paint(CARTAO, int(225 * a))); cv.drawRRect(rr, paint(CIANO, int(255 * a), "stroke", 4))
            texto(cv, T_LANCE[2], 0, 0, F_BLACK, 70, "#FFFFFF", int(255 * a))
            cv.restore()

    # ---------- selo VAR + chip: entra em "VAR", dentro do monitor; sobe depois que o gancho saiu
    t_capa = T["pode1_fim"] + 0.06
    sobe = e_inout(prog(t, t_capa + 0.45, t_capa + 0.85))
    chip, a_chip, pontos, cor_chip, flash = chip_estado(t, T)
    k_s = prog(t, T["var"] - 0.04, T["var"] + 0.14)
    esc_s = lerp(0.92, 1.08, sobe) * (1 + 0.25 * (1 - e_back(k_s))) if k_s < 1 else lerp(0.92, 1.08, sobe)
    selo_var(cv, t, lerp(56, 64, sobe), lerp(JY0 + 24, 146, sobe), esc_s, a_hud * clamp(k_s * 1.5), chip, a_chip,
             pontos, cor_chip, flash)

    # ---------- fim: o VAR saiu; o pé que merece avaliação; quem apita é o ortopedista
    fecho(cv, t, T)
    selo_serie(cv, prog(t, T["ortopedista"] - 0.1, T["ortopedista"] + 0.2) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))

    capa(cv, t, t_capa, ep["gancho"][0], ep["gancho"][1])
    interface_var(cv, t, T, blocos, DESTAQUE)


# ================================================================== som (sintetizado aqui, sem licença)
SR = som.SR


def _env(n, a=0.005, r=0.2):
    return som._env(n, a, r)


def _passa_banda(x, f_lo, f_hi):
    lp = som._onepole_lp(x, f_hi)
    return lp - som._onepole_lp(lp, f_lo)


def _banda_fft(x, f_lo, f_hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < f_lo) | (f > f_hi)] = 0
    y = np.fft.irfft(X, len(x))
    return y / (np.max(np.abs(y)) or 1.0)


def apito(dur=0.30, seed=11, ganho=0.55, solta=0.04):
    """Apito de árbitro: senoide ~3,2 kHz com o trinado da bolinha (FM e AM a ~40 Hz) + sopro. (piloto)"""
    n = int(dur * SR); t = np.arange(n) / SR
    fm = 3150 + 130 * np.sin(2 * np.pi * 41 * t)
    ph = 2 * np.pi * np.cumsum(fm) / SR
    am = 1 - 0.55 * (0.5 + 0.5 * np.sin(2 * np.pi * 41 * t + 0.7))
    tom = (np.sin(ph) + 0.22 * np.sin(2 * ph) + 0.08 * np.sin(3 * ph)) * am
    sopro = _passa_banda(np.random.default_rng(seed).standard_normal(n), 2000, 6000) * 0.5
    env = np.clip(t / 0.012, 0, 1) * np.clip((dur - t) / solta, 0, 1)
    return (tom + sopro * 0.6) * env * ganho


def apito_final():
    """Curto, longo (fim de jogo)."""
    return np.concatenate([apito(0.14, 21), np.zeros(int(0.07 * SR)), apito(0.42, 23, solta=0.14)])


def rebobinar(seed=31):
    n = int(0.5 * SR); t = np.arange(n) / SR
    x = np.random.default_rng(seed).standard_normal(n)
    fc = 600 + 2600 * np.abs(np.sin(np.pi * t / 0.5 * 1.5))
    y = np.zeros(n); acc = 0.0
    for i in range(n):
        a = np.exp(-2 * np.pi * fc[i] / SR); acc = (1 - a) * x[i] + a * acc; y[i] = acc
    f = 900 * np.exp(-t * 3.2) + 200
    saw = 2 * ((np.cumsum(f) / SR) % 1.0) - 1
    env = np.clip(t / 0.02, 0, 1) * np.clip((0.5 - t) / 0.05, 0, 1)
    return (y * 0.9 + saw * 0.18 + x * 0.04) * env * 0.8


def bipe(f=1600.0, dur=0.075):
    n = int(dur * SR); t = np.arange(n) / SR
    env = np.clip(t / 0.004, 0, 1) * np.clip((dur - t) / 0.02, 0, 1)
    return np.sin(2 * np.pi * f * t) * env * 0.42


def bipe_alto():
    return bipe(2100.0, 0.11)


def obturador(seed=41):
    a = som.tick(seed) * 0.8
    gap = np.zeros(int(0.05 * SR))
    n = int(0.06 * SR)
    ruido = np.random.default_rng(seed).standard_normal(n) * _env(n, 0.001, 0.015) * 0.35
    b = som.tick(seed + 1) * 0.6
    return np.concatenate([a, gap, b + np.pad(ruido, (0, max(0, len(b) - n)))[:len(b)]])


def tv_desliga(seed=71):
    n = int(0.36 * SR); t = np.arange(n) / SR
    f = 1200 * np.exp(-t * 10) + 60
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.002, 0.22) * 0.55
    rng = np.random.default_rng(seed)
    for _ in range(14):
        p = int(rng.uniform(0, n - 600)); m = int(rng.uniform(80, 400))
        y[p:p + m] += rng.standard_normal(m) * _env(m, 0.0002, 0.003) * 0.35
    return y


# ---- efeitos novos deste episódio
def moedinhas(seed=161):
    """3 tiques metálicos agudos (2,5–4 kHz), decaimento curto, espaçados 70 ms."""
    rng = np.random.default_rng(seed)
    n = int(0.3 * SR); y = np.zeros(n)
    for i in range(3):
        f = rng.uniform(2500, 4000); m = int(0.05 * SR); tt = np.arange(m) / SR
        s = (np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 1.47 * tt)) * np.exp(-tt / 0.012)
        p = int(i * 0.07 * SR); y[p:p + m] += s * 0.5
    return y


def passinho(seed=171):
    """Pisada macia de pé descalço no tapete: ruído grave filtrado, 60 ms."""
    n = int(0.06 * SR)
    x = som._onepole_lp(np.random.default_rng(seed).standard_normal(n), 300)
    return x * _env(n, 0.004, 0.05) * 4.0


def pagina(seed=181):
    """Folha do calendário virando: tique seco + sopro curto."""
    n = int(0.09 * SR)
    x = _banda_fft(np.random.default_rng(seed).standard_normal(n), 1000, 3000) * _env(n, 0.003, 0.07) * 0.5
    return x + np.pad(som.tick(seed) * 0.5, (0, max(0, n - len(som.tick(seed)))))[:n]


def tampa(seed=191):
    """Tampa de caixa fechando: baque macio (thump com passa-baixa)."""
    return som._onepole_lp(som.thump(seed), 400) * 1.6


def brilho_desce():
    """Shimmer com o tom descendo (os brilhos do tênis caem)."""
    s = som.shimmer()
    n = len(s)
    idx = np.cumsum(np.linspace(1.0, 0.75, n))
    idx = idx[idx < n - 1]
    return np.interp(idx, np.arange(n), s) * 0.8


SFX = dict(som.SFX)
SFX.update({"apito": apito, "apito_final": apito_final, "rebobinar": rebobinar, "bipe": bipe, "bipe_alto": bipe_alto,
            "obturador": obturador, "tv_desliga": tv_desliga, "moedinhas": moedinhas, "passinho": passinho,
            "pagina": pagina, "tampa": tampa, "brilho_desce": brilho_desce})


def _media_movel(x, w):
    n = len(x)
    c = np.concatenate([[0.0], np.cumsum(x)])
    i = np.arange(n)
    lo = np.clip(i - w // 2, 0, n); hi = np.clip(i + (w - 1) // 2 + 1, 0, n)
    return (c[hi] - c[lo]) / w


def mixar(voz, dur, eventos, ganho_trilha=0.40):
    """Cópia do som.mixar do piloto (mesma trilha, mesmo ducking) que conhece os efeitos desta série."""
    n = int(dur * SR)
    v = np.zeros(n); v[:min(n, len(voz))] = voz[:n]
    musica = som.trilha(dur) * ganho_trilha
    win = int(0.06 * SR)
    envv = np.sqrt(np.maximum(_media_movel(v ** 2, win), 0.0))
    alvo = np.where(envv > 0.02, 0.38, 1.0)
    duck = _media_movel(alvo, int(0.25 * SR))
    fx = np.zeros(n)
    cache = {}
    for t0, nome, g in eventos:
        if nome not in cache:
            cache[nome] = SFX[nome]()
        s = cache[nome]
        p = int(t0 * SR)
        if 0 <= p < n:
            m = min(len(s), n - p)
            fx[p:p + m] += s[:m] * g
    mix = v * 1.0 + musica * duck + fx * 0.7
    pico = np.max(np.abs(mix)) or 1.0
    return mix / pico * 0.89


def pisadas(T):
    """Tempos em que um pé descalço encosta no tapete (lance 3), pelo mesmo relógio da marcha da cena."""
    out = []
    D, P3, Vd, F = T["descalco"], T["pode3"], T["validado"], T["fortalece"]
    m_p3 = P3 - D
    fase0 = 0.86 - m_p3 / CICLO
    for t0, t1, m0 in ((D, P3, 0.0), (Vd, F, m_p3)):
        tt = t0
        while tt < t1:
            m = m0 + (tt - t0)
            for off in (0.0, 0.5):
                ph = (m / CICLO + fase0 + off) % 1.0
                ph2 = ((m + 1 / 60) / CICLO + fase0 + off) % 1.0
                if ph2 < ph:                                  # passou de 1 -> 0: o pé encostou
                    out.append(tt)
            tt += 1 / 60
    return out


def sons(T):
    ev = [(0.0, "apito", 0.85), (T["chama"] + 0.02, "pop", 0.25), (T["var"] - 0.02, "rebobinar", 0.7)]
    for pd, vd, _, _ in VEREDITOS:
        ev.append((T[pd] - 0.01, "obturador", 0.85))
        t0 = T[pd + "_fim"] + 0.07
        ev += [(t0, "bipe", 0.75), (t0 + 0.22, "bipe", 0.75), (t0 + 0.44, "bipe_alto", 0.8)]
        ev.append((T[vd] - 0.02, "thump", 0.9))
    ev += [(T["validado"] - 0.26, "apito", 0.45)]                  # apito curto no silêncio antes do VALIDADO
    # lance 1 — tênis caro
    ev += [(T["tenis1"], "shimmer", 0.3), (T["caro"] + 0.04, "moedinhas", 0.22)]
    ev += [(T["corrigir"] - 0.06, "whoosh", 0.3), (T["pe1"] + 0.02, "ping", 0.28)]
    ev += [(T["tenis2"], "brilho_desce", 0.28), (T["molda1"] - 0.02, "thump", 0.45)]
    ev += [(T["wipe"] - 0.02, "whoosh", 0.42), (T["wipe"] + 0.05, "tick", 0.4), (T["protege"] + 0.05, "shimmer", 0.25)]
    pf = T["protege_fim"]
    ev += [(pf + 0.04, "pop", 0.22), (pf + 0.2, "click", 0.3), (pf + 0.42, "shimmer", 0.22)]
    # lance 2 — palmilha
    ev += [(T["palmilha1"] - 0.02, "whoosh", 0.35), (T["palmilha1"] + 0.02, "tick", 0.4),
           (T["palmilha1"] + 0.6, "pop", 0.3), (T["formar"] + 0.02, "ping", 0.28)]
    ev += [(T["palmilha2"] - 0.02, "pop", 0.22), (T["molda2"] - 0.02, "thump", 0.45), (T["arco2"] + 0.02, "whoosh", 0.22)]
    ev += [(T["flexivel"] + 0.15, "pop", 0.2), (T["flexivel"] + 0.45, "pop", 0.16), (T["flexivel"] + 0.7, "pop", 0.14)]
    ev += [(T["costuma"] + 0.05 + 0.32 * i, "pagina", 0.4) for i in range(3)]
    ev += [(T["sozinho"] + 0.3, "shimmer", 0.3)]
    # lance 3 — descalço
    ev += [(T["descalco"] - 0.03, "tick", 0.55), (T["descalco"] + 0.02, "whoosh", 0.45)]
    ev += [(tp, "passinho", 0.32) for tp in pisadas(T)]
    ev += [(T["piso"] - 0.03, "whoosh", 0.22), (T["seguro"] + 0.02, "tick", 0.35)]
    ev += [(T["custa"] + 0.36, "tampa", 0.5), (T["custa"] - 0.1, "pop", 0.22), (T["nada"] - 0.04, "moedinhas", 0.22),
           (T["fortalece"] + 0.2, "shimmer", 0.3), (T["pe3"], "ping", 0.3)]
    # apito final, TV desligando, fecho, CTA
    ev += [(T["apito_f"], "apito_final", 0.6), (T["off"] + 0.02, "tv_desliga", 0.75)]
    ev += [(T["pe4"], "pop", 0.3), (T["doi"], "pop", 0.24), (T["durinho"] + 0.05, "click", 0.35),
           (T["chato2"], "pop", 0.28), (T["lado"] - 0.04, "ping", 0.28), (T["ai"], "pop", 0.26),
           (T["ai"] + 0.12, "pop", 0.22), (T["apita"] + 0.1, "pop", 0.32),
           (T["ortopedista"], "shimmer", 0.4), (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def tempos_previa(T):
    return [0.0, T["var"] + 0.25, T["tenis1"] + 0.25, T["caro"] + 0.2, T["corrigir"] + 0.3, T["chato1"] + 0.2,
            T["pode1"] + 0.6, T["anulado1"] + 0.3, T["tenis2"] + 0.4, T["molda1"] + 0.25, T["wipe"] + 0.18,
            T["protege"] + 0.3, T["protege_fim"] + 0.2, T["protege_fim"] + 0.62,
            T["palmilha1"] + 0.3, T["palmilha1"] + 0.6, T["formar"] + 0.35, T["arco1"] + 0.2, T["pode2"] + 0.6,
            T["anulado2"] + 0.3, T["molda2"] + 0.25, T["arco2"] + 0.4, T["crianca"] + 0.3, T["flexivel"] + 0.5,
            T["costuma"] + 0.5,
            T["sozinho"] + 0.55, T["descalco"] + 0.3, T["casa"] + 0.6, T["piso"] + 0.3, T["seguro"] + 0.4,
            T["pode3"] + 0.6, T["validado"] + 0.3, T["custa"] + 0.2, T["nada"] + 0.2, T["fortalece"] + 0.4,
            T["pe3"] + 0.2,
            T["off"] + 0.1, T["pe4"] + 0.2, T["doi"] + 0.25, T["durinho"] + 0.25, T["chato2"] + 0.45,
            T["lado"] + 0.35, T["ai"] - 0.1, T["apita"] + 0.3, T["ortopedista"] + 0.4, T["manda"] + 0.5,
            T["manda"] + 1.6]


# ================================================================== render (cópia do piloto + os vãos deste episódio)
VAO_CHECANDO = 0.86                   # fim de "pode?" -> veredito: ~0,3 s de congelar + ~0,55 s de CHECANDO
VAOS_EXTRA = (("palmilha", 1, 0.85),  # replay do JEITO CERTO (a sola que dobra na frente) antes de "Palmilha"
              ("pé", 4, 1.12),        # apito final + TV desligando, antes de "Pé que dói"
              ("aí", 1, 0.78))        # o par de pés com o sinal de diferente fica na tela antes de "Aí quem apita"
PRE_APITO = 0.25                      # o apito do quadro 0 não embola com "Chama"


def pausa_checando(audio, pal, vao=VAO_CHECANDO):
    """Insere silêncio depois de cada 'pode?' até o vão chegar a `vao` (cópia do piloto)."""
    ins = []
    for i in range(len(pal) - 1):
        if pal[i]["tok"].lower() == "pode?":
            fim = pal[i]["t"] + pal[i]["d"]; gap = pal[i + 1]["t"] - fim
            if gap < vao:
                ins.append((fim + 0.04, vao - gap))
    partes, ult = [], 0
    for t0, extra in ins:
        p = int(t0 * SR); partes += [audio[ult:p], np.zeros(int(extra * SR), dtype=audio.dtype)]; ult = p
    partes.append(audio[ult:])
    novo = np.concatenate(partes)

    def remap(t):
        return t + sum(extra for t0, extra in ins if t > t0)
    return novo, [dict(p, t=remap(p["t"])) for p in pal], ins


def garantir_vao(audio, pal, palavra, n, vao):
    """Silêncio antes da n-ésima `palavra` até o vão chegar a `vao` (nada da fala é cortado). (piloto)"""
    c = 0
    for i, p in enumerate(pal):
        if p["w"].lower() == palavra:
            c += 1
            if c == n:
                break
    else:
        raise KeyError(f"palavra não achada para a pausa: {palavra} #{n}")
    fim = pal[i - 1]["t"] + pal[i - 1]["d"]; gap = p["t"] - fim
    if gap >= vao:
        return audio, pal
    t0 = fim + 0.04; extra = vao - gap; k = int(t0 * SR)
    audio = np.concatenate([audio[:k], np.zeros(int(extra * SR), dtype=audio.dtype), audio[k:]])
    return audio, [dict(q, t=q["t"] + (extra if q["t"] > t0 else 0.0)) for q in pal]


def montar_T(pal, mapa):
    T = {}
    for chave, (palavra, n, prefixo) in mapa.items():
        c = 0
        for p in pal:
            w = p["w"].lower()
            if w == palavra or (prefixo and w.startswith(palavra)):
                c += 1
                if c == n:
                    T[chave] = p["t"]
                    if chave in FIM_DE:
                        T[chave + "_fim"] = p["t"] + p["d"]
                    break
        else:
            raise KeyError(f"palavra-âncora não achada no roteiro: {palavra} #{n}")
    T["fim_fala"] = pal[-1]["t"] + pal[-1]["d"]
    T["total"] = T["fim_fala"] + 2.2
    T["wipe"] = T["so1"] - 0.06                  # cortina do VAR: o jeito certo (tênis simples) entra em "Só"
    T["apito_f"] = T["pe4"] - 1.0                # apito final (curto, longo) no silêncio
    T["off"] = T["pe4"] - 0.48                   # a TV desliga no sopro longo
    return T


def fazer_render_var(quadro_fn, mapa, sons_fn, tempos_fn, respiro_cta=0.8):
    def render(ep, mp4, tmp, previa=False):
        roteiro = "\n".join(ep["roteiro"])
        voz_bruta, palavras = _voz.narrar(roteiro, _voz.RITMO_COMO_FUNCIONA, os.path.join(tmp, "voz"))
        voz_c, pal, tirado = comprimir(voz_bruta, palavras, respiro_cta=respiro_cta)
        pal = alinhar(pal, roteiro)
        voz_c, pal, ins = pausa_checando(voz_c, pal)
        for palavra, n, vao in VAOS_EXTRA:
            voz_c, pal = garantir_vao(voz_c, pal, palavra, n, vao)
        voz_c = np.concatenate([np.zeros(int(PRE_APITO * SR), dtype=voz_c.dtype), voz_c])
        pal = [dict(p, t=p["t"] + PRE_APITO) for p in pal]
        T = montar_T(pal, mapa)
        print(f"{ep['id']}: silêncio cortado {tirado:.2f}s | CHECANDO {[round(x[1], 2) for x in ins]} | "
              f"duração final {T['total']:.2f}s")
        blocos = montar_blocos_var(pal)

        def quadro_t(cv, t):
            quadro_fn(cv, t, T, blocos, ep)

        if previa:
            return _previas(quadro_t, tempos_fn(T), tmp, ep["id"]), T["total"]
        wav = os.path.join(tmp, f"{ep['id']}_mix.wav")
        som.gravar_wav(wav, mixar(voz_c, T["total"], sons_fn(T)))
        codificar(quadro_t, T["total"], wav, mp4)
        return mp4, T["total"]
    return render


render = fazer_render_var(quadro, ANCORAS, sons, tempos_previa, respiro_cta=0.8)
