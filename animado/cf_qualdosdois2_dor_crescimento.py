# -*- coding: utf-8 -*-
"""QUAL DOS DOIS? v2 — "Mesma noite, duas manhãs" (conceito B, O PAI EM DÚVIDA; decisão do Rafael em
08/11/2026: "Vai com B"). Substitui o cf_qualdosdois_dor_crescimento na fila.

Uma rodada só + bônus, sem pílula de rodadas e sem contagem muda:
  1. (0 s -> 'A manhã')  NOITE vista de quem cuida: criança sentada na beira do SOFÁ (nunca cama, nunca
     criança acordando, nunca relógio), blusa de pijama de estrelinhas e short LISO; os braços de quem
     cuida entram PELOS LADOS (manga curta) e as mãos seguram as DUAS canelas em vai-e-vem; as pernas
     balançam desde 0,0 s. Lua na janela, abajur aceso. O gancho é o único texto grande do quadro 0.
  2. AVANÇO RÁPIDO (chip ▶▶ só ícone + faixas de fita): a câmera vai até a janela, a lua desce, o sol
     nasce, o abajur apaga, o sofá fica vazio com a manta dobrada.
  3. 'Mesma noite, duas manhãs': DOIS PAINÉIS DE LARGURA TOTAL empilhados (A em cima, B embaixo), a
     MESMA criança de pijama na sala de manhã. A = MARCHA ANTÁLGICA sutil (motor do cf_crianca_mancando:
     apoio da perna que dói ~0,36 do ciclo × ~0,70 da boa, o pé apoia INTEIRO — sola plana no chão,
     nunca ponta —, o quadril cai no apoio curto e a passada da perna boa fica curta e apressada).
     B = marcha normal simétrica. Nenhum halo, ondinha, estrela ou mão na perna. Depois do 'B?' 1,0 s
     de palpite com as duas andando, luz alternando e tique-taque (sem silêncio).
  4. 'A!': o painel A ocupa a tela, VOLTA (◀◀) e passa a 0,25× com cantoneiras e o chip '0,25×'. Uma
     linha tracejada marca a altura do quadril no apoio da perna boa; o círculo de caneta LARANJA
     aparece só enquanto dura o APOIO CURTO e envolve o QUADRIL que cai abaixo da linha (nunca os
     dedos). Moldura laranja.
  5. 'E o B?': o B ocupa a tela e corre atrás da bola (moldura ouro, nenhum círculo na bola).
  6. 'Nas duas pernas, à noite…': volta à noite (◀◀) com as mãos nas DUAS canelas (sem contorno).
  7. 'Na dúvida, avalie.': REGRA FIXA DA SÉRIE — 'NA DÚVIDA, AVALIE.' grande na tela sobre a manhã.
  8. Bônus 'Mancou com febre? Procure atendimento no mesmo dia.': a criança A manca e um termômetro
     GRANDE sem número sobe (o vermelho só nele); SEM calendário, data ou horário; moldura laranja;
     'MANCOU COM FEBRE?' e 'PROCURE ATENDIMENTO NO MESMO DIA.' escritos.
  9. CTA de envio (interface da casa) com a miniatura da noite.

Desenho COPIADO (não importado) da maquete B (lab/qdd_v2/B_pai_em_duvida) e do cf_crianca_mancando
(motor da manqueira). União de contornos com conferência por pontos de dentro (runbook §13): se a
união perde um pedaço, refaz com deslocamento de 0,4–2,2 px; se ainda falhar, desenha os pedaços
separados. Karaokê próprio (cópia do cf_comum.legenda) com duas diferenças locais: nenhuma palavra de
1–2 letras fica órfã no fim da linha ('À', 'E', 'O') e o 'pop' da palavra cresce em volta do PRÓPRIO
centro (não empurra a vizinha). Todo texto desenhado está em ep['tela'], no gancho, no roteiro
(karaokê) ou na interface genérica.
"""
import math
import os
import re

import numpy as np
import skia

from . import som, voz as _voz
from .base import codificar, previas as _previas
from .cf_alongamento import PART, BG_IN, H
from .cf_alongamento import (BG_OUT, CX, F_BLACK, OURO, VERMELHO, W, C, clamp, e_back, e_inout, e_out, fundo,
                             larg_texto, lerp, paint, prog, texto)
from .cf_comum import interface
from .cf_fratura_cola import alinhar, comprimir, montar_blocos

# ------------------------------------------------------------------ paleta
COR_A, COR_B = "#DDE6F0", "#DDE6F0"      # bordas NEUTRAS (laranja = 'merece avaliação' só na revelação)
SELO = "#FFFFFF"
LARANJA = "#F08A4B"                      # 'merece avaliação' (nunca vermelho)
FUNDO_CARTAO = "#0B1824"
PELE, PELE_CL, PELE_ESC, PELE_LINHA = "#F0B49A", "#F7CDB8", "#D9937A", "#B9765E"
SHORT, SHORT_CL, SHORT_ESC, SHORT_LINHA = "#4C86C6", "#6FA3DA", "#3A6FA8", "#2C5A8E"   # LISO (sem bolinha)
PIJAMA, PIJAMA_CL, PIJAMA_ESC = "#C9D8EC", "#E4ECF7", "#94A9C6"
PELE_A, PELE_A_CL, PELE_A_ESC = "#E5A587", "#F1C0A6", "#C98467"     # pele de quem cuida (outro tom)
CAMISA, CAMISA_CL, CAMISA_ESC = "#8D6E9E", "#A88BB8", "#6B5180"     # manga curta de quem cuida
SOFA, SOFA_CL, SOFA_ESC = "#3D6470", "#557E8B", "#294852"
PAREDE_A, PAREDE_B, RODAPE = "#EEF2F6", "#D3DCE5", "#A9B5C1"
PISO, PISO_CL, PISO_ESC = "#B9875C", "#CB9A6E", "#93653F"

STAGE = (40, 360, 1040, 1236)            # a cena larga (1000 x 876)
PAN_A = (40, 360, 1040, 790)             # painéis de LARGURA TOTAL empilhados (1000 x 430)
PAN_B = (40, 806, 1040, 1236)
RAIO = 30
PALPITE = 1.0                            # s de palpite depois do 'B?' (silêncio de voz, com tique-taque)
DESTAQUE = {"noite", "espero", "manhã", "pista", "duas", "manhãs", "avaliação", "passo", "mancou", "avalia",
            "normal", "pernas", "inchaço", "febre", "crescimento", "sono"}


def tons_de(c, cl, esc):
    return (esc, c, cl, c, esc)


TONS_PELE = tons_de(PELE, PELE_CL, PELE_ESC)
TONS_SHORT = tons_de(SHORT, SHORT_CL, SHORT_ESC)
TONS_PIJ = tons_de(PIJAMA, PIJAMA_CL, PIJAMA_ESC)
TONS_PELE_A = tons_de(PELE_A, PELE_A_CL, PELE_A_ESC)
TONS_CAMISA = tons_de(CAMISA, CAMISA_CL, CAMISA_ESC)
TONS_SOFA = tons_de(SOFA, SOFA_CL, SOFA_ESC)


# ------------------------------------------------------------------ geometria (cópia da maquete B)
def lerpc(c1, c2, x):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{int(lerp(a[i], b[i], clamp(x))):02X}" for i in range(3))


def escurece(tons, k, alvo="#0A1530"):
    return tuple(lerpc(c, alvo, k) for c in tons)


def lin(p0, p1, cores, pos=None):
    return skia.GradientShader.MakeLinear([skia.Point(*p0), skia.Point(*p1)],
                                          [C(c) if isinstance(c, str) else c for c in cores], pos)


def _alfa(a):
    p = skia.Paint(); p.setAlphaf(clamp(a)); return p


def _rr(r, raio=RAIO):
    return skia.RRect.MakeRectXY(skia.Rect(*r), raio, raio)


def poli(pts, fechar=True):
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if fechar:
        p.close()
    return p


def suave(pts, fechar=True):
    n = len(pts)
    p = skia.Path()
    if fechar:
        p.moveTo((pts[-1][0] + pts[0][0]) / 2, (pts[-1][1] + pts[0][1]) / 2)
        for i in range(n):
            a_, b_ = pts[i], pts[(i + 1) % n]
            p.quadTo(a_[0], a_[1], (a_[0] + b_[0]) / 2, (a_[1] + b_[1]) / 2)
        p.close()
    else:
        p.moveTo(*pts[0])
        for i in range(1, n - 1):
            a_, b_ = pts[i], pts[i + 1]
            p.quadTo(a_[0], a_[1], (a_[0] + b_[0]) / 2, (a_[1] + b_[1]) / 2)
        p.lineTo(*pts[-1])
    return p


def _pts_dentro(p, n=5):
    b = p.getBounds(); pts = []
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            x = b.left() + b.width() * i / (n + 1); y = b.top() + b.height() * j / (n + 1)
            if p.contains(x, y):
                pts.append((x, y))
    return pts


def uniao(*ps):
    """União CONFERIDA (runbook §13): todo ponto de dentro de cada pedaço tem de estar dentro da união.
    Se o PathOps perdeu um segmento, refaz com os pedaços deslocados 0,4–2,2 px; se ainda falhar,
    devolve None e quem chamou desenha os pedaços separados."""
    for jit in (0.0, 0.4, 1.1, 2.2):
        out = ps[0]
        for k, q in enumerate(ps[1:]):
            if jit:
                q = skia.Path(q); q.offset(jit * (0.5 if k % 2 else -0.5), jit * 0.5)
            r = skia.Op(out, q, skia.PathOp.kUnion_PathOp)
            if r is None:
                out = None; break
            out = r
        if out is not None and all(out.contains(x, y) for p in ps for x, y in _pts_dentro(p)):
            return out
    return None


def uniao_ou_lista(*ps):
    u = uniao(*ps)
    return [u] if u is not None else list(ps)


def capsula(p0, p1, w0, w1):
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]; L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    p = poli([(p0[0] + nx * w0 / 2, p0[1] + ny * w0 / 2), (p1[0] + nx * w1 / 2, p1[1] + ny * w1 / 2),
              (p1[0] - nx * w1 / 2, p1[1] - ny * w1 / 2), (p0[0] - nx * w0 / 2, p0[1] - ny * w0 / 2)])
    c0 = skia.Path(); c0.addCircle(p0[0], p0[1], w0 / 2)
    c1 = skia.Path(); c1.addCircle(p1[0], p1[1], w1 / 2 - 0.3)
    u = uniao(p, c0, c1)
    if u is None:
        u = skia.Path(p); u.addPath(c0); u.addPath(c1)
    return u


def pinta(cv, path, p0, p1, w, tons, a=1.0, linha=None, larg_linha=2.5):
    """Sombreado cilíndrico perpendicular ao eixo p0->p1."""
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]; L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    sh = lin((mx - nx * w * 0.62, my - ny * w * 0.62), (mx + nx * w * 0.62, my + ny * w * 0.62), list(tons),
             [0.0, 0.2, 0.48, 0.8, 1.0])
    cv.drawPath(path, paint(tons[1], int(255 * a), shader=sh))
    if linha:
        cv.drawPath(path, paint(linha, int(220 * a), "stroke", larg_linha))


def ik(a, b, L1, L2, frente):
    dx, dy = b[0] - a[0], b[1] - a[1]
    D = clamp(math.hypot(dx, dy), abs(L1 - L2) + 1.0, L1 + L2 - 0.5)
    cos_a = clamp((L1 * L1 + D * D - L2 * L2) / (2 * L1 * D), -1.0, 1.0)
    base = math.atan2(dy, dx); al = math.acos(cos_a)
    c1 = (a[0] + L1 * math.cos(base + al), a[1] + L1 * math.sin(base + al))
    c2 = (a[0] + L1 * math.cos(base - al), a[1] + L1 * math.sin(base - al))
    s1 = (c1[0] - a[0]) * frente[0] + (c1[1] - a[1]) * frente[1]
    s2 = (c2[0] - a[0]) * frente[0] + (c2[1] - a[1]) * frente[1]
    return c1 if s1 >= s2 else c2


def trim(pt, k):
    if k < 0.999:
        pe = skia.TrimPathEffect.Make(0.0, max(0.002, k))
        if pe is not None:
            pt.setPathEffect(pe)
    return pt


def bump(t, t0, dur=0.35):
    return math.sin(math.pi * clamp((t - t0) / dur)) if t >= t0 else 0.0


def _rot(p, graus):
    a = math.radians(graus); c, s = math.cos(a), math.sin(a)
    return p[0] * c - p[1] * s, p[0] * s + p[1] * c


# ------------------------------------------------------------------ astros
def lua(cv, x, y, r, a=1.0, cor="#F7EEDD", brilho=0.6):
    if a <= 0:
        return
    p = skia.Path(); p.addCircle(x, y, r)
    q = skia.Path(); q.addCircle(x + r * 0.48, y - r * 0.26, r * 0.86)
    c = skia.Op(p, q, skia.PathOp.kDifference_PathOp) or p
    if brilho > 0:
        cv.drawCircle(x, y, r * 1.7, paint(cor, int(60 * a * brilho), blur=26))
    cv.drawPath(c, paint(cor, int(110 * a), blur=12))
    cv.drawPath(c, paint(cor, int(255 * a)))


def sol(cv, x, y, r, a=1.0, giro=0.0, cor="#FFD25E"):
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.rotate(giro)
    cv.drawCircle(0, 0, r * 1.6, paint(cor, int(85 * a), blur=24))
    for i in range(10):
        cv.save(); cv.rotate(i * 36)
        cv.drawLine(0, -(r + 13), 0, -(r + 31), paint(cor, int(255 * a), "stroke", 7))
        cv.restore()
    cv.drawCircle(0, 0, r, paint(cor, int(255 * a)))
    cv.drawCircle(-r * 0.32, -r * 0.32, r * 0.34, paint("#FFFFFF", int(70 * a), blur=8))
    cv.restore()


def _estrela_mini(cv, x, y, r, cor="#8EA6CB", a=200):
    p = skia.Path()
    for i in range(10):
        an = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        (p.moveTo if i == 0 else p.lineTo)(x + rr * math.cos(an), y + rr * math.sin(an))
    p.close()
    cv.drawPath(p, paint(cor, a))


def _lua_mini(cv, x, y, r):
    a = skia.Path(); a.addCircle(x, y, r)
    b = skia.Path(); b.addCircle(x + r * 0.5, y - r * 0.3, r * 0.85)
    c = skia.Op(a, b, skia.PathOp.kDifference_PathOp) or a
    cv.drawPath(c, paint("#F2D38A", 220))


def estampa_pijama(cv, clip, x0, x1, y0, y1, passo=74):
    cv.save(); cv.clipPath(clip, skia.ClipOp.kIntersect, True)
    for j, yy in enumerate(range(int(y0), int(y1), passo)):
        for i, xx in enumerate(range(int(x0), int(x1), 78)):
            x = xx + (39 if j % 2 else 0)
            if (i + j) % 3 == 0:
                _lua_mini(cv, x, yy, 13)
            else:
                _estrela_mini(cv, x, yy, 11)
    cv.restore()


# ------------------------------------------------------------------ NOITE: sala, sofá, criança sentada, mãos
def sala_noite(cv, w, h, janela=(54, 40, 290, 262), amanhece=0.0):
    parede = lin((0, 0), (0, 620), [lerpc("#16294A", "#C9D6E4", amanhece * 0.85), lerpc("#21395F", "#E3EAF1", amanhece * 0.85)])
    cv.drawRect(skia.Rect(0, 0, w, h), paint("#16294A", shader=parede))
    k = 1 - amanhece                                                   # o abajur apaga com o dia
    cv.drawCircle(w - 120, 150, 300, paint("#FFB561", int(80 * k), blur=90))
    lx = w - 120
    cv.drawLine(lx, 190, lx, 640, paint(lerpc("#3A2A22", "#7E6A5A", amanhece), 255, "stroke", 9))
    cup = poli([(lx - 70, 190), (lx + 70, 190), (lx + 48, 92), (lx - 48, 92)])
    cv.drawPath(cup, paint(lerpc("#F7D9A8", "#E9E2D6", amanhece)))
    cv.drawPath(cup, paint("#FFE2B0", int(140 * k), blur=14))
    cv.drawPath(cup, paint(lerpc("#C99A5B", "#B8AFA2", amanhece), 220, "stroke", 3))
    cv.drawOval(skia.Rect(lx - 70, 180, lx + 70, 200), paint("#FFF1CF", int(220 * k)))
    x0, y0, x1, y1 = janela
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0 - 16, y0 - 16, x1 + 16, y1 + 16), 10, 10),
                 paint(lerpc("#2B4670", "#F7F9FB", amanhece)))
    ceu = lin((0, y0), (0, y1), [lerpc("#0A1A36", "#7CC4EE", amanhece),
                                 lerpc("#1D3D69", lerpc("#F6B27A", "#D8F0FC", clamp(amanhece * 1.6 - 0.6)), amanhece)])
    cv.drawRect(skia.Rect(x0, y0, x1, y1), paint("#0A1A36", shader=ceu))
    cv.save(); cv.clipRect(skia.Rect(x0, y0, x1, y1))
    if amanhece < 0.98:                                                # a lua DESCE e some
        lua(cv, lerp(x1 - 80, x1 - 60, amanhece), lerp(y0 + 82, y1 + 70, amanhece), 40, 1 - amanhece * 0.7, brilho=0.8)
        for fx, fy, r in ((0.18, 0.22, 2.8), (0.40, 0.12, 2.2), (0.30, 0.55, 2.4), (0.55, 0.38, 2.0), (0.12, 0.70, 2.0)):
            cv.drawCircle(x0 + fx * (x1 - x0), y0 + fy * (y1 - y0), r * 2.6, paint("#FFFFFF", int(45 * (1 - amanhece)), blur=4))
            cv.drawCircle(x0 + fx * (x1 - x0), y0 + fy * (y1 - y0), r, paint("#FFFFFF", int(230 * (1 - amanhece))))
    if amanhece > 0.3:                                                 # o sol NASCE
        sol(cv, lerp(x0 + 70, x0 + 90, amanhece), lerp(y1 + 60, y0 + 110, e_out(clamp(amanhece))), 34,
            clamp((amanhece - 0.3) / 0.4))
    cv.restore()
    cor_mold = lerpc("#2B4670", "#F7F9FB", amanhece)
    cv.drawLine((x0 + x1) / 2, y0, (x0 + x1) / 2, y1, paint(cor_mold, 255, "stroke", 10))
    cv.drawLine(x0, (y0 + y1) / 2, x1, (y0 + y1) / 2, paint(cor_mold, 255, "stroke", 10))
    cort = suave([(x1 + 20, y0 - 30), (x1 + 86, y0 - 30), (x1 + 96, y1 + 40), (x1 + 70, y1 + 70), (x1 + 34, y1 + 66),
                  (x1 + 26, (y0 + y1) / 2)])
    cv.drawPath(cort, paint(lerpc("#3A3F6E", "#9FB4CF", amanhece), 255))
    for xx in (x1 + 44, x1 + 66):
        cv.drawLine(xx, y0 - 20, xx + 6, y1 + 50, paint(lerpc("#2A2E58", "#8099B8", amanhece), 160, "stroke", 4))
    if amanhece > 0.35:
        kk = clamp((amanhece - 0.35) / 0.5)
        cv.drawPath(poli([(x0, y0), (x1, y0), (x1 + 520, h), (x0 + 160, h)]), paint("#FFD58A", int(70 * kk), blur=30))
    if amanhece < 0.6:
        cv.drawPath(poli([(x0, y1), (x1, y1), (x1 + 260, y1 + 380), (x0 + 120, y1 + 380)]),
                    paint("#9CC9FF", int(16 * (1 - amanhece)), blur=20))


def sofa(cv, w, y_ass, escuro):
    tons = escurece(TONS_SOFA, escuro) if escuro else TONS_SOFA
    y_top, y_enc = 300, y_ass - 40
    for x0, x1 in ((-40, w * 0.5 - 6), (w * 0.5 + 6, w + 40)):
        p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y_top, x1, y_enc + 30), 46, 46))
        cv.drawPath(p, paint(tons[1], shader=lin((0, y_top), (0, y_enc + 30), [tons[2], tons[1], tons[0]], [0.0, 0.35, 1.0])))
        cv.drawPath(p, paint(lerpc(tons[0], "#000000", 0.35), 200, "stroke", 3))
        for bx in (x0 + (x1 - x0) * 0.3, x0 + (x1 - x0) * 0.7):
            cv.drawCircle(bx, y_top + 110, 6, paint(lerpc(tons[0], "#000000", 0.3), 220))
    ya, yf, yb = y_ass - 52, y_ass, 650
    topo = skia.Path(); topo.addRRect(skia.RRect.MakeRectXY(skia.Rect(-40, ya, w + 40, yf + 20), 24, 24))
    cv.drawPath(topo, paint(tons[2]))
    fr = skia.Path(); fr.addRRect(skia.RRect.MakeRectXY(skia.Rect(-40, yf, w + 40, yb), 22, 22))
    cv.drawPath(fr, paint(tons[1], shader=lin((0, yf), (0, yb), [tons[1], tons[0]])))
    cv.drawPath(fr, paint(lerpc(tons[0], "#000000", 0.35), 200, "stroke", 3))
    cv.drawLine(w * 0.5, yf + 8, w * 0.5, yb - 8, paint(lerpc(tons[0], "#000000", 0.3), 200, "stroke", 3))
    for x in (90, w - 90):
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 14, yb - 4, x + 14, yb + 30), 6, 6), paint("#2A1D14"))


def piso_noite(cv, w, h, y0, amanhece=0.0):
    sh = lin((0, y0), (0, h), [lerpc("#2A1E1A", "#93653F", amanhece), lerpc("#3A2A22", "#B9875C", amanhece)])
    cv.drawRect(skia.Rect(0, y0, w, h), paint("#2A1E1A", shader=sh))
    y = y0; k = 0
    while y < h:
        cv.drawLine(0, y, w, y, paint("#000000", 60, "stroke", 2)); y += 18 + k * 8; k += 1


def _pele_frente(cv, pth, x, w, tons=TONS_PELE, linha=True):
    sh = lin((x - w / 2, 0), (x + w / 2, 0), list(tons), [0.0, 0.22, 0.5, 0.78, 1.0])
    cv.drawPath(pth, paint(tons[1], shader=sh))
    if linha:
        cv.drawPath(pth, paint(PELE_LINHA, 235, "stroke", 3.2))


def canela_frente(x, y_joe, y_tor, lado):
    p = skia.Path()
    rj, rt = 50, 30
    fora = -lado
    xo, xi = x + fora * rj, x - fora * rj
    p.moveTo(xo, y_joe)
    p.cubicTo(xo + fora * 9, y_joe + 80, x + fora * (rt + 8), y_tor - 80, x + fora * rt, y_tor)
    p.lineTo(x - fora * rt, y_tor)
    p.cubicTo(x - fora * (rt + 2), y_tor - 80, xi - fora * 3, y_joe + 70, xi, y_joe)
    p.close()
    k = skia.Path(); k.addOval(skia.Rect(x - rj, y_joe - rj * 0.85, x + rj, y_joe + rj * 0.9))
    return uniao_ou_lista(p, k)


def pe_pendurado(x, y_tor, lado):
    fora = -lado
    p = suave([(x - 27, y_tor - 12), (x + 27, y_tor - 12), (x + 40 + fora * 6, y_tor + 48), (x + 40 + fora * 10, y_tor + 84),
               (x + fora * 10, y_tor + 100), (x - 40 + fora * 10, y_tor + 84), (x - 40 + fora * 6, y_tor + 48)])
    xs = [-27, -12, 2, 15, 27] if fora < 0 else [27, 12, -2, -15, -27]
    rs = [12.5, 10, 9.5, 9, 8]
    dedos = [(x + dx + fora * 10, y_tor + 94 - (5 if abs(dx) > 20 else 0), r) for dx, r in zip(xs, rs)]
    return p, dedos


def crianca_sentada(cv, kx, y_ass, y_tor, ang, afasta=74):
    """Criança sentada na beira do sofá (de frente), recortada no peito: blusa de pijama de
    estrelinhas, short LISO, joelhos na beirada, canelas penduradas que BALANÇAM (`ang` = graus de
    cada canela em volta do joelho: (esquerda da tela, direita))."""
    cam = suave([(kx - 150, -80), (kx + 150, -80), (kx + 160, 160), (kx + 170, y_ass - 70),
                 (kx - 170, y_ass - 70), (kx - 160, 160)])
    pinta(cv, cam, (kx - 170, 200), (kx + 170, 200), 340, TONS_PIJ, linha=PIJAMA_ESC, larg_linha=3)
    estampa_pijama(cv, cam, kx - 200, kx + 220, -40, y_ass - 60)
    for s_ in (-1, 1):                                                   # braços da criança, mãos no sofá
        om = (kx + s_ * 146, -60); co = (kx + s_ * 214, 196); mp = (kx + s_ * 196, y_ass - 22)
        ante, bra = capsula(co, mp, 56, 50), capsula(om, co, 66, 58)
        mao = skia.Path(); mao.addRRect(skia.RRect.MakeRectXY(skia.Rect(mp[0] - 31, mp[1] - 24, mp[0] + 31, mp[1] + 36), 22, 22))
        pinta(cv, ante, co, mp, 56, TONS_PELE)
        pinta(cv, bra, om, co, 66, TONS_PELE)
        pol = capsula((mp[0] - s_ * 16, mp[1] - 4), (mp[0] - s_ * 40, mp[1] + 20), 22, 18)   # polegar p/ dentro
        pinta(cv, mao, (mp[0] - 31, mp[1]), (mp[0] + 31, mp[1]), 62, TONS_PELE)
        pinta(cv, pol, (mp[0] - s_ * 16, mp[1] - 4), (mp[0] - s_ * 40, mp[1] + 20), 22, TONS_PELE)
        for sil in uniao_ou_lista(ante, bra, mao, pol):                  # UM contorno: sem 'junta de boneco'
            cv.drawPath(sil, paint(PELE_LINHA, 235, "stroke", 3))
        mg = (lerp(om[0], co[0], 0.55), lerp(om[1], co[1], 0.55))
        pinta(cv, capsula(om, mg, 80, 74), om, mg, 80, TONS_PIJ, linha=PIJAMA_ESC, larg_linha=3)
        for dx in (-13, 0, 13):
            cv.drawLine(mp[0] + dx, mp[1] + 16, mp[0] + dx, mp[1] + 34, paint(PELE_LINHA, 150, "stroke", 2.4))
    sh = suave([(kx - 170, y_ass - 100), (kx + 170, y_ass - 100), (kx + 180, y_ass - 10),
                (kx + 154, y_ass + 24), (kx - 154, y_ass + 24), (kx - 180, y_ass - 10)])
    cv.drawPath(sh, paint("#000000", 60, blur=10))
    pinta(cv, sh, (kx - 180, 0), (kx + 180, 0), 360, TONS_SHORT, linha=SHORT_LINHA, larg_linha=3.4)
    cv.save(); cv.clipPath(sh, skia.ClipOp.kIntersect, True)
    cv.drawRect(skia.Rect(kx - 190, y_ass - 104, kx + 190, y_ass - 78), paint(SHORT_CL))
    cv.restore()
    cv.drawLine(kx, y_ass - 74, kx, y_ass + 12, paint(SHORT_LINHA, 160, "stroke", 3))
    for lado in (1, -1):
        x = kx - lado * afasta
        r = skia.Rect(x - 70, y_ass - 8, x + 70, y_ass + 40)
        cv.drawOval(r, paint(SHORT_ESC)); cv.drawOval(r, paint(SHORT_LINHA, 200, "stroke", 3))
    for i, lado in enumerate((1, -1)):
        x = kx - lado * afasta
        y_joe = y_ass + 30
        cv.save(); cv.rotate(ang[i], x, y_joe)
        pe, dedos = pe_pendurado(x, y_tor, lado)
        canela = canela_frente(x, y_joe, y_tor, lado)
        _pele_frente(cv, pe, x, 92, linha=False)
        for pth in canela:
            _pele_frente(cv, pth, x, 108, linha=False)
        for sil in uniao_ou_lista(pe, *canela):                          # UM contorno canela+pé
            cv.drawPath(sil, paint(PELE_LINHA, 235, "stroke", 3.2))
        for dx, dy, r in dedos:
            cv.drawCircle(dx, dy, r, paint(PELE_CL)); cv.drawCircle(dx, dy, r, paint(PELE_LINHA, 220, "stroke", 2.4))
        cv.drawArc(skia.Rect(x - 20, y_ass + 44, x + 20, y_ass + 64), 25, 130, False, paint(PELE_LINHA, 140, "stroke", 3))
        cv.drawOval(skia.Rect(x - 20, y_ass + 6, x + 10, y_ass + 30), paint(PELE_CL, 150))
        cv.restore()


def _bezier(p0, p1, p2, p3, u):
    a, b, c, d = (1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u ** 3
    return (a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1])


def _borda_interna(x, y_joe, y_tor, lado, n=24):
    """Pontos da borda INTERNA da canela (a do lado da outra perna), do joelho ao tornozelo: as mesmas
    curvas de `canela_frente`."""
    fora = -lado; rj, rt = 50, 30; xi = x - fora * rj
    return [_bezier((xi, y_joe), (xi - fora * 3, y_joe + 70), (x - fora * (rt + 2), y_tor - 80), (x - fora * rt, y_tor),
                    k / n) for k in range(n + 1)]


def _quadro_mao(x, y_joe, lado, desl, theta, esc):
    """Referencial da mão sobre a canela: H(a, b), a = rumo dos dedos (para DENTRO e para cima),
    b = lado do dedo mínimo (cima/fora); origem = meio da linha dos nós dos dedos."""
    fora = -lado; th = math.radians(theta)
    f = (-fora * math.cos(th), -math.sin(th)); nn = (fora * math.sin(th), -math.cos(th))
    K = (x + fora * 6, y_joe + desl)

    def H(a, b):
        return (K[0] + (f[0] * a + nn[0] * b) * esc, K[1] + (f[1] * a + nn[1] * b) * esc)
    return H


def _curva_dedo(a):                                                      # dedos se curvam ao envolver a perna
    return -0.0026 * max(0.0, a) ** 2


def pecas_mao_canela(H):
    """Dorso, dedos (UM bloco: juntos) e polegar aduzido, no referencial H."""
    cu = _curva_dedo
    dorso = suave([H(-98, 45), H(-62, 42), H(-26, 42), H(-2, 41), H(6, 22), H(6, -6), H(3, -33),   # polegar aduzido
                   H(-4, -41), H(8, -48), H(13, -56), H(4, -63), H(-22, -61), H(-52, -52), H(-98, -45)])
    cima = [H(a, 39 - 6 * a / 80 + cu(a)) for a in (-6, 14, 34, 54, 70)]
    baixo = [H(a, -38 + 5 * a / 80 + cu(a)) for a in (70, 54, 34, 14, -6)]
    dedos = suave(cima + [H(84, 18 + cu(84)), H(88, -6 + cu(88)), H(82, -28 + cu(82))] + baixo)
    return dorso, dedos


def mao_canela(cv, x, y_joe, y_tor, lado, desl, theta, esc=1.0):
    """Mão de quem cuida vista PELO DORSO (quem cuida está atrás da câmera), no referencial da canela
    (antes do giro): pulso do lado de FORA, dedos JUNTOS e levemente curvos subindo em diagonal para
    DENTRO e sumindo atrás da borda interna da canela (envolvem a perna); polegar aduzido do lado de
    DENTRO/baixo (voltado para a outra mão). Sem unha, sem palma, sem dedo espalhado."""
    fora = -lado
    H = _quadro_mao(x, y_joe, lado, desl, theta, esc)
    dorso, dedos = pecas_mao_canela(H)
    pecas = [dorso, dedos]

    borda = _borda_interna(x, y_joe, y_tor, lado)                        # o que passa da borda interna SOME
    vis = poli([(borda[0][0], y_joe - 400)] + borda + [(borda[-1][0], y_tor + 400),
               (x + fora * 3000, y_tor + 400), (x + fora * 3000, y_joe - 400)])
    canela = canela_frente(x, y_joe, y_tor, lado)
    cv.save(); cv.clipPath(vis, skia.ClipOp.kIntersect, True)
    cv.save()                                                            # sombra da mão na própria perna
    for pc in canela[:1]:
        cv.clipPath(pc, skia.ClipOp.kIntersect, True)
    for pc in pecas:
        q = skia.Path(pc); q.offset(fora * 3, 7)
        cv.drawPath(q, paint("#5A2E1E", 55, blur=8))
    cv.restore()
    tons = lin(H(0, -46), H(0, 46), [PELE_A_ESC, PELE_A, PELE_A_CL, PELE_A, PELE_A_ESC], [0.0, 0.22, 0.55, 0.82, 1.0])
    cv.saveLayer(None, None)                                             # o pulso FUNDE no antebraço (sem degrau)
    for pc in pecas:
        cv.drawPath(pc, paint(PELE_A, shader=tons))
    fade = paint("#000000", shader=lin(H(-98, 0), H(-80, 0), [C("#000000", 0), C("#000000", 255)]))
    fade.setBlendMode(skia.BlendMode.kDstIn)
    cv.drawPath(poli([H(-200, -300), H(400, -300), H(400, 300), H(-200, 300)]), fade)
    cv.restore()
    cv.save(); cv.clipPath(dedos, skia.ClipOp.kIntersect, True)          # dedos escurecem ao virar atrás da perna
    sh = lin(H(34, 0), H(90, 0), [C("#7A3E28", 0), C("#7A3E28", 110)])
    cv.drawPath(dedos, paint("#7A3E28", shader=sh))
    for b in (-19, 1, 20):                                               # 4 dedos JUNTOS: só as fendas
        pts = [H(a, b * (1 - 0.15 * a / 80) + _curva_dedo(a)) for a in (10, 30, 50, 70, 92)]
        cv.drawPath(suave(pts, fechar=False), paint("#A86A50", 170, "stroke", 2.4 * esc))
    cv.restore()
    for b in (-27, -9, 10, 28):                                          # nós dos dedos (dorso): só um brilho
        p0, p1 = H(-3, b - 6), H(-3, b + 6)
        cv.drawLine(*p0, *p1, paint(PELE_A_CL, 150, "stroke", 4.0 * esc))
    for b in (-16, 8):                                                   # tendões do dorso, bem discretos
        cv.drawLine(*H(-70, b * 0.6), *H(-12, b), paint("#A86A50", 60, "stroke", 2.2 * esc))
    cv.save()                                                            # sem risco no pulso: a mão CONTINUA o antebraço
    cv.clipPath(poli([H(-74, -300), H(400, -300), H(400, 300), H(-74, 300)]), skia.ClipOp.kIntersect, True)
    for sil in uniao_ou_lista(*pecas):                                   # UM contorno
        cv.drawPath(sil, paint("#A86A50", 235, "stroke", 3.0))
    cv.restore()
    cv.drawPath(suave([H(-3, -41), H(-16, -44), H(-34, -45)], fechar=False),   # fenda polegar/indicador
                paint("#A86A50", 200, "stroke", 2.6 * esc))
    cv.restore()
    cv.save()                                                            # a borda da perna passa POR CIMA
    cv.clipPath(dedos, skia.ClipOp.kIntersect, True)                     # da ponta dos dedos (eles vão atrás)
    cv.clipPath(vis, skia.ClipOp.kIntersect, True)
    cv.drawPath(suave(borda, fechar=False), paint(PELE_LINHA, 235, "stroke", 3.2))
    cv.restore()


def braco_lado(cv, ombro, cotovelo, pulso):
    """Braço de quem cuida entrando PELO LADO do quadro: braço com MANGA CURTA, cotovelo à mostra,
    antebraço de pele até o pulso (é o braço de quem olha, não de outra pessoa)."""
    pinta(cv, capsula(cotovelo, pulso, 92, 70), cotovelo, pulso, 92, TONS_PELE_A, linha="#A86A50", larg_linha=3)
    pinta(cv, capsula(ombro, cotovelo, 118, 100), ombro, cotovelo, 118, TONS_PELE_A, linha="#A86A50", larg_linha=3)
    corte = (lerp(ombro[0], cotovelo[0], 0.88), lerp(ombro[1], cotovelo[1], 0.88))
    pinta(cv, capsula(ombro, corte, 150, 136), ombro, corte, 150, TONS_CAMISA, linha=CAMISA_ESC, larg_linha=3)
    dx, dy = cotovelo[0] - ombro[0], cotovelo[1] - ombro[1]; L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    cv.drawLine(corte[0] + nx * 66, corte[1] + ny * 66, corte[0] - nx * 66, corte[1] - ny * 66, paint(CAMISA_ESC, 230, "stroke", 5))
    ex, ey = pulso[0] - cotovelo[0], pulso[1] - cotovelo[1]; Le = math.hypot(ex, ey) or 1.0
    ux, uy = ex / Le, ey / Le; px, py = -uy, ux                          # punho: vinco discreto antes da mão
    wx, wy = pulso[0] - ux * 16, pulso[1] - uy * 16
    cv.drawLine(wx + px * 20, wy + py * 20, wx - px * 20, wy - py * 20, paint("#A86A50", 120, "stroke", 2.6))
    cx_, cy_ = cotovelo[0] + ux * 8, cotovelo[1] + uy * 8                # cotovelo: dobrinha
    cv.drawArc(skia.Rect(cx_ - 26, cy_ - 26, cx_ + 26, cy_ + 26), math.degrees(math.atan2(py, px)) - 40, 80, False,
               paint("#A86A50", 150, "stroke", 3))


KX, Y_ASS, Y_TOR, E_KID, AFASTA = 520, 452, 752, 0.92, 74


def noite(cv, w, h, t, amanhece=0.0, vazio=False, crianca_a=1.0, maos=True, aperta=0.0):
    """Ponto de vista de quem cuida, à noite: as duas canelas balançam e as duas mãos seguram e
    deslizam nelas (vai-e-vem). `t` move tudo; `aperta` = pulso das mãos no 'duas pernas'."""
    escuro = 0.25 * (1 - amanhece)

    def fundo_noite(c):
        sala_noite(c, w, h, amanhece=amanhece)
        piso_noite(c, w, h, 670, amanhece)
        sofa(c, w, Y_ASS, escuro)
    if amanhece == 0:
        cv.drawImage(_imagem(("noite", w, h), w, h, fundo_noite), 0, 0)
    else:
        fundo_noite(cv)
    if vazio or crianca_a <= 0:                                          # manta dobrada no sofá vazio
        a = 1.0 if vazio else 1 - crianca_a
        m = skia.Path(); m.addRRect(skia.RRect.MakeRectXY(skia.Rect(KX - 150, Y_ASS - 112, KX + 150, Y_ASS - 46), 22, 22))
        cv.drawPath(m, paint("#B65E6B", int(255 * a))); cv.drawPath(m, paint("#7A3842", int(220 * a), "stroke", 3))
        for yy in (Y_ASS - 94, Y_ASS - 68):
            cv.drawLine(KX - 136, yy, KX + 136, yy, paint("#D98A95", int(200 * a), "stroke", 4))
        if vazio:
            return
    angs = (7.5 * math.sin(2 * math.pi * t / 1.15), 7.5 * math.sin(2 * math.pi * t / 1.15 + 2.3))
    cv.saveLayer(None, _alfa(crianca_a)) if crianca_a < 1 else cv.save()
    cv.translate(KX, Y_ASS); cv.scale(E_KID, E_KID); cv.translate(-KX, -Y_ASS)
    crianca_sentada(cv, KX, Y_ASS, Y_TOR, angs, AFASTA)
    cv.restore()
    if not maos or crianca_a < 1:
        return
    for i, lado in enumerate((1, -1)):                                   # mão no MEIO da canela (gira com ela)
        x = KX - lado * AFASTA; y_joe = Y_ASS + 30
        fora = -lado                                                     # para fora da tela, do lado desta perna
        vai = math.sin(2 * math.pi * t / 0.9 + i * math.pi)
        desl = 190 + 30 * vai                                            # vai-e-vem no MEIO da canela, longe do joelho
        cotovelo = (KX + fora * 370, 830 + 8 * vai)                      # cotovelo DOBRADO à vista no canto:
        ombro = (KX + fora * 520, 1010)                                  # braço sobe de baixo, antebraço entra

        def tela(p, a=angs[i], x=x, y_joe=y_joe):                        # referencial da canela -> tela
            rx, ry = _rot((p[0] - x, p[1] - y_joe), a)
            return (KX + (x + rx - KX) * E_KID, Y_ASS + (y_joe + ry - Y_ASS) * E_KID)
        esc = 0.86 * (1 + 0.04 * aperta)
        theta = 40.0
        for _ in range(3):                                               # o dorso continua o antebraço (+~22°)
            pt = tela(_quadro_mao(x, y_joe, lado, desl, theta, esc)(-80, 0))
            elev = math.degrees(math.atan2(cotovelo[1] - pt[1], fora * (cotovelo[0] - pt[0])))
            theta = clamp(elev + 22 - fora * angs[i], 34, 60)
        pulso = tela(_quadro_mao(x, y_joe, lado, desl, theta, esc)(-80, 0))
        braco_lado(cv, ombro, cotovelo, pulso)
        cv.save()
        cv.translate(KX, Y_ASS); cv.scale(E_KID, E_KID); cv.translate(-KX, -Y_ASS)
        cv.rotate(angs[i], x, y_joe)
        mao_canela(cv, x, y_joe, Y_TOR, lado, desl, theta, esc)
        cv.restore()


# ------------------------------------------------------------------ MANHÃ: sala que corre, criança de perfil
def sala_dia(cv, w, h, y_piso, off, esc):
    cv.drawRect(skia.Rect(0, 0, w, y_piso), paint(PAREDE_A, shader=lin((0, 0), (0, y_piso), [PAREDE_A, PAREDE_B])))
    jw, jh, jy = 220 * esc, 250 * esc, 60 * esc                          # janelas que passam (a sala anda)
    per = 1150 * esc
    x = (700 * esc - off) % per - per
    while x < w + per:
        jx0, jx1, jy0, jy1 = x, x + jw, jy, jy + jh
        if jx1 > -40 and jx0 < w + 40:
            cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(jx0 - 14 * esc, jy0 - 14 * esc, jx1 + 14 * esc, jy1 + 14 * esc), 8, 8),
                         paint("#FBFCFD"))
            cv.drawRect(skia.Rect(jx0, jy0, jx1, jy1), paint("#CFEAF8", shader=lin((jx0, jy0), (jx1, jy1), ["#8FD0F4", "#DDF2FC"])))
            cv.save(); cv.clipRect(skia.Rect(jx0, jy0, jx1, jy1))
            sol(cv, jx1 - 62 * esc, jy0 + 70 * esc, 30 * esc, 1.0)
            cv.restore()
            cv.drawLine((jx0 + jx1) / 2, jy0, (jx0 + jx1) / 2, jy1, paint("#FBFCFD", 255, "stroke", 10 * esc))
            cv.drawLine(jx0, (jy0 + jy1) / 2, jx1, (jy0 + jy1) / 2, paint("#FBFCFD", 255, "stroke", 10 * esc))
            cv.drawRect(skia.Rect(jx0 - 22 * esc, jy1 + 10 * esc, jx1 + 22 * esc, jy1 + 24 * esc), paint("#E7ECF1"))
            cv.drawPath(poli([(jx0, jy1 + 24 * esc), (jx1, jy1 + 24 * esc), (jx1 - 120 * esc, y_piso + 140 * esc),
                              (jx0 - 220 * esc, y_piso + 140 * esc)]), paint("#FFE7A8", 55, blur=18))
        x += per
    cv.drawRect(skia.Rect(0, y_piso - 16 * esc, w, y_piso), paint(RODAPE))
    cv.drawRect(skia.Rect(0, y_piso, w, h), paint(PISO, shader=lin((0, y_piso), (0, h), [PISO_ESC, PISO_CL])))
    y, k = y_piso, 0
    while y < h:
        cv.drawLine(0, y, w, y, paint(PISO_ESC, 150, "stroke", 2))
        dy_ = (16 + k * 7) * esc
        per_t = per / 3                                   # 1/3 da janela: a sala inteira repete a cada `per`
        x0 = (-off + (k % 3) * 140 * esc) % per_t - per_t
        while x0 < w + per_t:
            cv.drawLine(x0, y, x0, y + dy_, paint(PISO_ESC, 110, "stroke", 2))
            x0 += per_t
        y += dy_; k += 1
    cv.drawRect(skia.Rect(0, y_piso, w, y_piso + 26 * esc), paint("#000000", 40, blur=8))


_CACHE = {}


def _imagem(chave, larg, alt, desenha):
    """Fundo pronto em imagem (a máquina de render é compartilhada: o que não muda não se redesenha)."""
    if chave not in _CACHE:
        if len(_CACHE) > 40:
            _CACHE.clear()
        surf = skia.Surface(int(math.ceil(larg)), int(math.ceil(alt)))
        c = surf.getCanvas(); c.clear(skia.ColorTRANSPARENT)
        desenha(c)
        _CACHE[chave] = surf.makeImageSnapshot()
    return _CACHE[chave]


def sala_dia_rapida(cv, w, h, y_piso, off, esc):
    """= sala_dia(cv, w, h, y_piso, off, esc), mas de uma faixa pronta deslizada (período `per`)."""
    per = 1150 * esc
    chave = ("dia", round(w, 2), round(h, 2), round(y_piso, 2), round(esc, 4))
    img = _imagem(chave, w + per + 2, h, lambda c: sala_dia(c, w + per + 2, h, y_piso, 0.0, esc))
    cv.save(); cv.clipRect(skia.Rect(0, 0, w, h))
    cv.drawImage(img, -(off % per), 0)
    cv.restore()


L1, L2 = 150, 146
R_QUAD, R_JOE, R_TOR = 38, 28, 19


def pe_local():
    p = skia.Path()
    p.moveTo(-17, -17)
    p.cubicTo(-31, -8, -34, 20, -18, 29)
    p.cubicTo(-6, 33, 30, 32, 60, 31)
    p.cubicTo(84, 30, 88, 12, 72, 6)
    p.cubicTo(50, 0, 29, -6, 19, -17)
    p.close()
    return p


def pe_path(ank, rot):
    p = pe_local()
    m = skia.Matrix(); m.setScale(1.08, 1.04); m.postRotate(rot); m.postTranslate(*ank)
    p.transform(m)
    return p


def canela_path(knee, ank, frente):
    dx, dy = ank[0] - knee[0], ank[1] - knee[1]; L = math.hypot(dx, dy) or 1.0
    d = (dx / L, dy / L)
    f = (d[1], -d[0])
    if f[0] * frente[0] + f[1] * frente[1] < 0:
        f = (-f[0], -f[1])
    fr, tr = [], []
    for i in range(15):
        s = i / 14
        wf = lerp(R_JOE - 1, R_TOR, s)
        wb = R_JOE + 9 * math.sin(math.pi * clamp(s / 0.75)) ** 1.4 - 8 * s
        c = (knee[0] + d[0] * L * s, knee[1] + d[1] * L * s)
        fr.append((c[0] + f[0] * wf, c[1] + f[1] * wf)); tr.append((c[0] - f[0] * wb, c[1] - f[1] * wb))
    p = poli(fr + tr[::-1])
    k = skia.Path(); k.addCircle(knee[0], knee[1], R_JOE - 0.7)          # raio ≠ o do círculo da coxa (§13)
    a = skia.Path(); a.addCircle(ank[0], ank[1], R_TOR)
    u = uniao(p, k, a)
    if u is None:
        u = skia.Path(p); u.addPath(k); u.addPath(a)
    return u


def perna_crianca(cv, hip, ank, rot_pe, escuro=0.0):
    """Coxa + canela + pé: silhueta unida e CONFERIDA; se a união falhar, pedaços separados."""
    frente = (1, 0)
    knee = ik(hip, ank, L1, L2, frente)
    coxa = capsula(hip, knee, R_QUAD * 2, R_JOE * 2)
    can = canela_path(knee, ank, frente)
    pe = pe_path(ank, rot_pe)
    tons = escurece(TONS_PELE, escuro, "#6A3E36") if escuro else TONS_PELE
    for sil in uniao_ou_lista(coxa, can, pe):
        cv.save(); cv.clipPath(sil, skia.ClipOp.kIntersect, True)
        cv.drawPath(sil, paint(tons[1]))
        pinta(cv, coxa, hip, knee, R_QUAD * 2, tons)
        pinta(cv, can, knee, ank, (R_JOE + R_TOR) * 1.25, tons)
        t0 = _rot((10, -10), rot_pe); t1 = _rot((10, 32), rot_pe)
        pinta(cv, pe_path(ank, rot_pe), (ank[0] + t0[0], ank[1] + t0[1]), (ank[0] + t1[0], ank[1] + t1[1]), 44, tons)
        cv.drawCircle(knee[0] + 8, knee[1], 13, paint(PELE_CL, int(110 * (1 - escuro))))
        for (x0, y0), (x1, y1) in (((56, 8), (58, 24)), ((66, 9), (68, 24))):
            p0 = _rot((x0 * 1.08, y0 * 1.04), rot_pe); p1 = _rot((x1 * 1.08, y1 * 1.04), rot_pe)
            cv.drawLine(ank[0] + p0[0], ank[1] + p0[1], ank[0] + p1[0], ank[1] + p1[1], paint(PELE_LINHA, 110, "stroke", 2.4))
        cv.restore()
        cv.drawPath(sil, paint(lerpc(PELE_LINHA, "#2A1810", escuro * 0.6), 235, "stroke", 3.4))
    return knee


def manga(hip, knee, larg_quad=50, comp=88, larg_barra=52):
    hx, hy = hip; kx, ky = knee
    L = math.hypot(kx - hx, ky - hy) or 1.0
    ux, uy = (kx - hx) / L, (ky - hy) / L; nx, ny = -uy, ux
    ex, ey = hx + ux * comp, hy + uy * comp
    p = skia.Path()
    p.moveTo(hx + nx * larg_quad, hy + ny * larg_quad); p.lineTo(ex + nx * larg_barra, ey + ny * larg_barra)
    p.quadTo(ex + ux * 7, ey + uy * 7, ex - nx * larg_barra, ey - ny * larg_barra)
    p.lineTo(hx - nx * larg_quad, hy - ny * larg_quad); p.close()
    c = skia.Path(); c.addCircle(hx, hy, larg_quad)
    u = uniao(p, c) or p
    return u, (ux, uy, nx, ny), (ex, ey)


def _no_quadril(pth, hip, incl):
    m = skia.Matrix(); m.setRotate(incl); m.postTranslate(*hip); pth.transform(m)
    return pth


def cintura(hip, incl=0.0):
    p = skia.Path()
    p.moveTo(-64, -96); p.lineTo(58, -96)
    p.cubicTo(68, -46, 66, -6, 54, 24); p.lineTo(-40, 28)
    p.cubicTo(-84, 18, -88, -40, -64, -96); p.close()
    return _no_quadril(p, hip, incl)


def blusa(hip, incl=0.0, altura=230):
    """Tronco de perfil, um pouco MAIS LARGO que o quadril e alinhado com o short (barra sobre o cós)."""
    p = skia.Path()
    p.moveTo(-84, -92 - altura); p.lineTo(62, -92 - altura)
    p.cubicTo(84, -250, 92, -150, 78, -82)
    p.cubicTo(50, -68, -50, -68, -92, -80)
    p.cubicTo(-98, -160, -92, -260, -84, -92 - altura); p.close()
    return _no_quadril(p, hip, incl)


def _mao_path(abre):
    """Mão de criança de PERFIL no referencial do punho (+x = para fora da mão, -y = lado do polegar).
    Cópia adaptada da mão do cf_cameralenta_osso_crianca (palma oval + 4 dedos + polegar), com a
    união CONFERIDA por pontos de dentro (runbook §13); `abre` 0 = mão fechada (corrida), 1 = aberta."""
    pecas = []
    palma = skia.Path(); palma.addOval(skia.Rect(-2, -13, 32, 13))
    pecas.append(palma)
    for i, yy in enumerate((-8.5, -3.0, 2.5, 8.0)):
        comp = lerp(9.0, 22.0 - 2.0 * abs(i - 1.5), abre)
        r = 4.4
        d = skia.Path(); d.addRRect(skia.RRect.MakeRectXY(skia.Rect(0, -r, comp, r), r, r))
        m = skia.Matrix(); m.setRotate((i - 1.5) * 7.0 * abre + lerp(38, 8, abre)); m.postTranslate(26, yy)
        d.transform(m)
        pecas.append(d)
    pol = skia.Path(); pol.addRRect(skia.RRect.MakeRectXY(skia.Rect(0, -4.8, lerp(13.0, 19.0, abre), 4.8), 4.8, 4.8))
    m = skia.Matrix(); m.setRotate(lerp(-20.0, -48.0, abre)); m.postTranslate(9, -9)
    pol.transform(m)
    pecas.append(pol)
    return uniao_ou_lista(*pecas)


MAO_K = 1.75                     # a mão em unidades do corpo (antebraço ~32-38 de largura)


def mao_perfil(cv, pulso, ang_graus, abre, tons, linha):
    cv.save(); cv.translate(*pulso); cv.rotate(ang_graus); cv.scale(MAO_K, MAO_K)
    pecas = _mao_path(abre)
    sh = lin((0, -14), (0, 14), list(tons), [0.0, 0.2, 0.48, 0.8, 1.0])
    for pc in pecas:
        cv.drawPath(pc, paint(tons[1], shader=sh))
    for pc in pecas:
        cv.drawPath(pc, paint(linha, 235, "stroke", 3.0 / MAO_K))
    cv.restore()


def braco_de_pe(cv, hip, incl, ang, dobra, escuro=0.0, abre=0.45, recuo=0.0):
    """Braço de perfil que balança: OMBRO no alto do tronco -> COTOVELO -> PUNHO -> MÃO com palma,
    dedos e polegar (para a frente). `ang` = graus do braço (negativo = para a frente); `dobra` =
    flexão do cotovelo (o antebraço gira para a FRENTE, nunca para trás)."""
    om = _rot((-6 - recuo, -286), incl); om = (hip[0] + om[0], hip[1] + om[1])
    a1 = math.radians(ang); a2 = math.radians(ang - dobra)
    co = (om[0] - 112 * math.sin(a1), om[1] + 112 * math.cos(a1))
    pu = (co[0] - 100 * math.sin(a2), co[1] + 100 * math.cos(a2))
    tons = escurece(TONS_PELE, escuro, "#6A3E36") if escuro else TONS_PELE
    lin_ = lerpc(PELE_LINHA, "#2A1810", escuro * 0.6)
    bra, ante = capsula(om, co, 44, 38), capsula(co, pu, 38, 30)
    pecas = uniao_ou_lista(bra, ante)
    for pc in pecas:
        cv.save(); cv.clipPath(pc, skia.ClipOp.kIntersect, True)
        pinta(cv, bra, om, co, 44, tons); pinta(cv, ante, co, pu, 38, tons)
        cv.restore()
    for pc in pecas:                                                     # UM contorno ombro-punho
        cv.drawPath(pc, paint(lin_, 235, "stroke", 3.2))
    ang_mao = math.degrees(math.atan2(pu[1] - co[1], pu[0] - co[0])) - 6 * (1 - abre)
    mao_perfil(cv, (pu[0] - 3 * math.cos(a2 + math.pi / 2), pu[1] - 3 * math.sin(a2 + math.pi / 2)), ang_mao, abre,
               tons, lin_)
    mg = (lerp(om[0], co[0], 0.58), lerp(om[1], co[1], 0.58))
    tp = escurece(TONS_PIJ, escuro) if escuro else TONS_PIJ
    pinta(cv, capsula(om, mg, 60, 54), om, mg, 60, tp, linha=PIJAMA_ESC, larg_linha=3)
    return pu


def silhueta_braco_perto(pose, folga=10.0):
    """Silhueta (corpo, referencial do quadril) do braço de PERTO + mão + manga, com `folga` de borda: o círculo
    do replay passa POR TRÁS dele (o braço na frente do círculo, nunca o círculo envolvendo o punho)."""
    hip, incl = pose["hip"], pose["incl"]
    dif = pose["longe"][0][0] - pose["perto"][0][0]; lim = pose.get("lim_braco", 34)
    ang = -lim * math.tanh(pose.get("k_braco", 0.30) * dif / lim)
    dobra = pose.get("dobra", 14) + pose.get("dobra_var", 0) * max(0.0, -ang) / lim
    abre = pose.get("abre", 0.45)
    om = _rot((-6, -286), incl); om = (hip[0] + om[0], hip[1] + om[1])
    a1 = math.radians(ang); a2 = math.radians(ang - dobra)
    co = (om[0] - 112 * math.sin(a1), om[1] + 112 * math.cos(a1))
    pu = (co[0] - 100 * math.sin(a2), co[1] + 100 * math.cos(a2))
    out = skia.Path()
    out.addPath(capsula(om, co, 60 + folga, 54 + folga)); out.addPath(capsula(co, pu, 38 + folga, 30 + folga))
    ang_mao = math.degrees(math.atan2(pu[1] - co[1], pu[0] - co[0])) - 6 * (1 - abre)
    m = skia.Matrix(); m.setScale(MAO_K, MAO_K); m.postRotate(ang_mao)
    m.postTranslate(pu[0] - 3 * math.cos(a2 + math.pi / 2), pu[1] - 3 * math.sin(a2 + math.pi / 2))
    for pc in _mao_path(abre):
        q = skia.Path(pc); q.transform(m)
        out.addPath(q)
        r = q.getBounds(); out.addOval(skia.Rect(r.left() - folga / 2, r.top() - folga / 2, r.right() + folga / 2,
                                                 r.bottom() + folga / 2))
    out.setFillType(skia.PathFillType.kWinding)
    return out


def crianca_de_pe(cv, pose):
    """Pernas de perfil (olhando para a direita): a de trás (LONGE, um tom mais escura) é a perna boa,
    a da frente (PERTO) é a que dói. Short LISO e a barra da blusa do pijama."""
    hip, incl = pose["hip"], pose["incl"]
    hl = (hip[0] - 16, hip[1] - 6)                        # perna de longe um pouco atrás: as duas aparecem
    k_br = pose.get("k_braco", 0.30)                     # braço balança com a perna do OUTRO lado
    dif = pose["longe"][0][0] - pose["perto"][0][0]
    lim = pose.get("lim_braco", 34)
    ang_perto = -lim * math.tanh(k_br * dif / lim)       # saturação SUAVE (nada de braço travado)
    dobra = pose.get("dobra", 14)
    dobra_p = dobra + pose.get("dobra_var", 0) * max(0.0, -ang_perto) / lim   # dobra mais quando vai à frente
    dobra_l = dobra + pose.get("dobra_var", 0) * max(0.0, ang_perto) / lim
    abre = pose.get("abre", 0.45)
    # braço de LONGE: de perfil ele fica INTEIRO atrás do tronco (blusa larga); desenhado, só sobravam o
    # antebraço/punho brotando das costas ou do quadril (leitor, 3ª rodada). Some INTEIRO, nunca pela metade.
    if pose.get("braco_longe", False):
        braco_de_pe(cv, hip, incl, -ang_perto, dobra_l, escuro=0.24, abre=abre, recuo=4)
    lg = ((pose["longe"][0][0] - 10, pose["longe"][0][1] - 6), pose["longe"][1])
    kl = perna_crianca(cv, hl, lg[0], lg[1], escuro=0.24)
    m_l, _, _ = manga(hl, kl)
    cv.drawPath(m_l, paint(lerpc(SHORT_ESC, "#0E2033", 0.25)))
    cv.drawPath(m_l, paint(SHORT_LINHA, 220, "stroke", 3.2))
    kp = perna_crianca(cv, hip, pose["perto"][0], pose["perto"][1])
    m_p, e_p, (ex, ey) = manga(hip, kp)
    uni = uniao(cintura(hip, incl), m_p)
    corpo = uni if uni is not None else cintura(hip, incl)
    cv.drawPath(corpo, paint("#000000", 50, blur=8))
    pinta(cv, corpo, (hip[0] - 80, hip[1]), (hip[0] + 70, hip[1]), 160, TONS_SHORT)
    if uni is None:
        pinta(cv, m_p, hip, kp, 100, TONS_SHORT)
    ux, uy, nx, ny = e_p
    cv.save(); cv.clipPath(m_p, skia.ClipOp.kIntersect, True)
    cv.drawLine(ex + nx * 60 - ux * 4, ey + ny * 60 - uy * 4, ex - nx * 60 - ux * 4, ey - ny * 60 - uy * 4,
                paint(SHORT_CL, 255, "stroke", 16))
    cv.restore()
    cv.drawPath(corpo, paint(SHORT_LINHA, 230, "stroke", 3.6))
    cos_ = _no_quadril(poli([(-66, -100), (60, -100), (61, -78), (-67, -78)]), hip, incl)
    cv.drawPath(cos_, paint(SHORT_CL)); cv.drawPath(cos_, paint(SHORT_LINHA, 200, "stroke", 2.6))
    cam = blusa(hip, incl)                                                # blusa POR CIMA do cós (barra solta)
    cv.drawPath(cam, paint("#000000", 50, blur=8))
    pinta(cv, cam, (hip[0] - 90, hip[1] - 150), (hip[0] + 85, hip[1] - 150), 175, TONS_PIJ)
    estampa_pijama(cv, cam, hip[0] - 120, hip[0] + 120, hip[1] - 330, hip[1] - 60)
    cv.drawPath(cam, paint(PIJAMA_ESC, 230, "stroke", 3.2))
    braco_de_pe(cv, hip, incl, ang_perto, dobra_p, abre=abre)           # braço de PERTO, na frente


# ---- motores de marcha (cópia adaptada do cf_crianca_mancando: apoio longo na boa, curto na que dói)
GY_P = 282                       # tornozelo apoiado (quadril em 0); sola em ~ +32
SOLA = 314
F_P, LIFT_P = 58, 44
P_MAN, SD_BOA, S0_DOR, SD_DOR = 0.95, 0.70, 0.66, 0.36
DIP = 34                         # quanto o quadril (e o tronco junto) CAI no apoio curto
F_BOA, F_DOR = 46, 80            # a perna BOA pousa pouco à frente (passo curto e apressado)
P_NOR, SD_NOR = 0.95, 0.62
P_RUN, SD_RUN, F_RUN, LIFT_RUN = 0.56, 0.36, 74, 110


def pe_ciclo(fi, s0, sd, F, vp, lift):
    """-> (x do tornozelo, altura, giro do pé, no chão?, fração da fase). No chão o pé fica PLANO
    (giro 0: calcanhar e planta apoiados); no balanço, sai pela ponta e chega pelo calcanhar."""
    u = (fi - s0) % 1.0
    if u < sd:
        return F - vp * u, 0.0, 0.0, True, u / sd
    w_ = (u - sd) / (1 - sd)
    xb = F - vp * sd
    return lerp(xb, F, e_inout(w_)), lift * math.sin(math.pi * w_), 22 * (1 - 2 * w_) * math.sin(math.pi * w_), False, w_


def pose_mancando(fi):
    vp = 2 * F_P / SD_BOA
    xs, ys, ps, ch_s, fs = pe_ciclo(fi, 0.0, SD_BOA, F_BOA, vp, LIFT_P * 0.75)
    xm, ym, pm, ch_m, fm = pe_ciclo(fi, S0_DOR, SD_DOR, F_DOR, vp, LIFT_P * 0.8)
    dip = math.sin(math.pi * fm) ** 0.8 if ch_m else 0.0
    dy = (-6 * math.sin(math.pi * fs) if ch_s else 0.0) + DIP * dip
    return dict(hip=(0, dy), perto=((xm, GY_P - ym), pm), longe=((xs, GY_P - ys), ps), incl=5.0 * dip,
                dor_no_chao=ch_m, dor_fase=fm, dip=dip, boa_no_chao=ch_s, k_braco=0.30, lim_braco=24,
                dobra=16, dobra_var=14, abre=0.5)


def pose_normal(fi):
    vp = 2 * F_P / SD_NOR
    xa, ya, pa, ca, fa = pe_ciclo(fi, 0.0, SD_NOR, F_P, vp, LIFT_P)
    xb, yb, pb, cb, fb = pe_ciclo(fi, 0.5, SD_NOR, F_P, vp, LIFT_P)
    dy = -4 * max(math.sin(math.pi * fa) if ca else 0.0, math.sin(math.pi * fb) if cb else 0.0)
    return dict(hip=(0, dy), perto=((xb, GY_P - yb), pb), longe=((xa, GY_P - ya), pa), incl=0.0, k_braco=0.30, lim_braco=26,
                dobra=16, dobra_var=16, abre=0.5)


def pe_corrida(fi, s0, vp):
    """Corrida: apoio curto e plano; no balanço o calcanhar SOBE ATRÁS (chute para trás) e só depois
    o joelho leva o pé para a frente, pousando à frente do quadril. -> (x, altura, giro, no chão?)."""
    u = (fi - s0) % 1.0
    if u < SD_RUN:
        return F_RUN - vp * u, 0.0, 0.0, True
    w_ = (u - SD_RUN) / (1 - SD_RUN)
    xb = F_RUN - vp * SD_RUN
    x = lerp(xb, F_RUN, e_inout(clamp((w_ - 0.22) / 0.78)))
    y = LIFT_RUN * math.sin(math.pi * clamp(w_ / 0.9)) ** 0.8
    giro = 34 * math.sin(math.pi * clamp(w_ / 0.55)) - 12 * math.sin(math.pi * clamp((w_ - 0.6) / 0.4))
    return x, y, giro, False


def pose_corre(fi):
    vp = 2 * F_RUN / SD_RUN
    xa, ya, pa, ca = pe_corrida(fi, 0.0, vp)
    xb, yb, pb, cb = pe_corrida(fi, 0.5, vp)
    ua, ub = (fi % 1.0), ((fi - 0.5) % 1.0)
    apoio = max(math.sin(math.pi * ua / SD_RUN) if ca else 0.0, math.sin(math.pi * ub / SD_RUN) if cb else 0.0)
    voo = not (ca or cb)
    dy = -22 if voo else 10 * apoio - 10                                 # fase aérea: o corpo SOBE
    if voo:
        ya += 14; yb += 14
    return dict(hip=(10, dy), perto=((xb, GY_P - yb), pb), longe=((xa, GY_P - ya), pa),
                incl=9.0, k_braco=0.50, lim_braco=36, dobra=82, dobra_var=0, abre=0.12)


def passo_local(modo):
    """Quanto o chão corre (unidades locais) por ciclo — o pé apoiado fica PARADO no chão."""
    return {"manca": 2 * F_P / SD_BOA, "normal": 2 * F_P / SD_NOR, "corre": 2 * F_RUN / SD_RUN}[modo]


POSES = {"manca": pose_mancando, "normal": pose_normal, "corre": pose_corre}


def geo_manha(w, h):
    s = min(h * 0.00185, 1.40)                    # painel: 0,80 (aparece a blusa e o tronco que cai); cena larga: 1,18
    y_piso = h * 0.94
    return s, y_piso, w * 0.40, y_piso - SOLA * s


def manha(cv, w, h, modo, fi, bola_on=False, ref=None, bola_k=0.0, avanco=0.0, escala=None):
    """Sala de manhã + a criança de perfil andando no lugar (o chão e as janelas correm para trás).
    `avanco` desloca a criança no quadro (o B alcança a bola). -> (pose, hip_x, hip_y, s)."""
    s, y_piso, hip_x, hip_y = geo_manha(w, h)
    if escala:                                        # enquadramento mais aberto (aparece mais tronco/braço)
        s = min(s, escala); hip_y = y_piso - SOLA * s
    hip_x += avanco * w
    esc_sala = h / 876
    off = fi * passo_local(modo) * s
    sala_dia_rapida(cv, w, h, y_piso - 50 * esc_sala, off, esc_sala)
    pose = POSES[modo](fi)
    cv.save(); cv.translate(hip_x, hip_y); cv.scale(s, s)
    cv.drawOval(skia.Rect(-170, SOLA - 14, 190, SOLA + 14), paint("#000000", 60, blur=10))
    if ref is not None:
        ref(cv, pose, "atras")
    crianca_de_pe(cv, pose)
    cv.restore()
    if bola_on:                                       # a bola rola mais devagar que a criança: ela ALCANÇA e chuta
        r = 62 * s
        pe_x = hip_x + (F_RUN + 60) * s + r
        alc = e_inout(clamp(bola_k / 0.78))
        bx = lerp(w * 1.02, pe_x, alc)
        by = y_piso - r + 6 * s
        chute = e_out(clamp((bola_k - 0.78) / 0.22))
        bx += chute * w * 0.75; by -= math.sin(math.pi * clamp(chute * 1.4)) * 120 * s
        bola(cv, bx, by, r, giro=math.degrees(-(off * 0.45) / r + chute * 6))
    return pose, hip_x, hip_y, s


def bola(cv, x, y, r, giro=0.0):
    cv.drawOval(skia.Rect(x - r * 0.9, y + r * 0.86, x + r * 0.9, y + r * 1.08), paint("#000000", 60, blur=8))
    cv.save(); cv.translate(x, y); cv.rotate(giro)
    cv.drawCircle(0, 0, r, paint("#FFFFFF"))
    cl = skia.Path(); cl.addCircle(0, 0, r)
    cv.save(); cv.clipPath(cl, skia.ClipOp.kIntersect, True)
    for ang, cor in ((0, "#E85D5D"), (120, "#4FA3E0"), (240, "#F5C04A")):
        cv.save(); cv.rotate(ang)
        p = skia.Path(); p.moveTo(0, 0); p.lineTo(-r * 1.2, -r * 0.7); p.quadTo(0, -r * 1.6, r * 1.2, -r * 0.7); p.close()
        cv.drawPath(p, paint(cor))
        cv.restore()
    cv.drawCircle(-r * 0.35, -r * 0.4, r * 0.3, paint("#FFFFFF", 90, blur=6))
    cv.restore()
    cv.drawCircle(0, 0, r, paint("#5A3A2A", 200, "stroke", 3))
    cv.restore()


# ------------------------------------------------------------------ moldura, selos, chips, fita
def selo_letra(cv, letra, x, y, cor, esc=1.0, a=1.0):
    """Selo PEQUENO no canto (a letra não é o assunto: o passo é)."""
    if a <= 0:
        return
    r = 34
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    cv.drawCircle(0, 4, r, paint("#000000", int(90 * a), blur=8))
    cv.drawCircle(0, 0, r, paint(cor, int(255 * a)))
    cv.drawCircle(0, 0, r - 3, paint("#FFFFFF", int(70 * a), "stroke", 3))
    texto(cv, letra, 0, 50 * 0.355, F_BLACK, 50, FUNDO_CARTAO, int(255 * a))
    cv.restore()


def _rr_borrado(cv, r, cor, a, estilo, larg, blur):
    """Retângulo arredondado BORRADO (sombra/brilho) de imagem pronta: o blur grande é o que mais
    pesa por quadro; a imagem é feita uma vez por retângulo e desenhada com a opacidade do quadro."""
    if a <= 0:
        return
    m = int(3 * blur + larg + 4)
    x0, y0, x1, y1 = r
    chave = ("rr", round(x0, 1), round(y0, 1), round(x1, 1), round(y1, 1), cor, estilo, larg, blur)
    img = _imagem(chave, x1 - x0 + 2 * m, y1 - y0 + 2 * m,
                  lambda c: c.drawRRect(_rr((m, m, m + x1 - x0, m + y1 - y0)), paint(cor, 255, estilo, larg, blur=blur)))
    p = skia.Paint(); p.setAlphaf(clamp(a / 255))
    cv.drawImage(img, x0 - m, y0 - m, skia.SamplingOptions(), p)


def janela_cena(cv, r, desenho, borda="#FFFFFF", a_borda=60, marca=None, marca_a=1.0, luz=0.0):
    """Cena recortada num cartão (sombra, borda; `marca` = moldura da revelação; `luz` = palpite)."""
    x0, y0, x1, y1 = r
    _rr_borrado(cv, (x0, y0 + 12, x1, y1 + 12), "#000000", 120, "fill", 0, 20)
    cv.save(); cv.clipRRect(_rr(r), skia.ClipOp.kIntersect, True)
    cv.translate(x0, y0)
    out = desenho(cv, x1 - x0, y1 - y0)
    cv.restore()
    cv.drawRRect(_rr(r), paint(borda, a_borda, "stroke", 3))
    if luz > 0:
        _rr_borrado(cv, r, "#FFFFFF", int(150 * luz), "stroke", 26, 14)
        cv.drawRRect(_rr(r), paint("#FFFFFF", int(255 * luz), "stroke", 7))
    if marca and marca_a > 0:
        _rr_borrado(cv, r, marca, int(170 * marca_a), "stroke", 30, 16)
        cv.drawRRect(_rr(r), paint(marca, int(255 * marca_a), "stroke", 9))
    return out


def faixas_fita(cv, r, t, a=1.0):
    if a <= 0:
        return
    # Sem faixas brancas atravessando a cena (liam como falha/glitch por cima do corpo): o avanço e a
    # volta são marcados só pelo chip ▶▶/◀◀ e por um escurecimento SUAVE das bordas do cartão.
    _rr_borrado(cv, r, "#000000", int(120 * a), "stroke", 46, 22)


def chip_setas(cv, cx, cy, frente=True, a=1.0):
    """Pílula escura com ▶▶ ou ◀◀ (só ícone, sem texto)."""
    if a <= 0:
        return
    rr = skia.RRect.MakeRectXY(skia.Rect(cx - 62, cy - 34, cx + 62, cy + 34), 34, 34)
    cv.drawRRect(rr, paint("#000000", int(90 * a), blur=8))
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(235 * a)))
    cv.drawRRect(rr, paint(OURO, int(230 * a), "stroke", 3))
    cv.save(); cv.translate(cx + (4 if frente else -4), cy); cv.scale(0.95 if frente else -0.95, 0.95)
    for dx in (-22, 10):
        p = poli([(dx - 14, -22), (dx - 14, 22), (dx + 20, 0)])
        cv.drawPath(p, paint(OURO, int(255 * a)))
    cv.restore()


def chip_lento(cv, cx, cy, a=1.0):
    if a <= 0:
        return
    tam = 40; lw = larg_texto("0,25×", F_BLACK, tam)
    rr = skia.RRect.MakeRectXY(skia.Rect(cx - lw / 2 - 22, cy - tam * 0.78, cx + lw / 2 + 22, cy + tam * 0.42), 24, 24)
    cv.drawRRect(rr, paint("#000000", int(90 * a), blur=8))
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(235 * a)))
    cv.drawRRect(rr, paint(OURO, int(230 * a), "stroke", 3))
    texto(cv, "0,25×", cx, cy + tam * 0.06, F_BLACK, tam, OURO, int(255 * a))


def cantoneiras(cv, r, a=1.0):
    if a <= 0:
        return
    x0, y0, x1, y1 = r
    m = 16                                                    # rente à borda: não cobrem selo nem chip
    for (x, y, sx, sy) in ((x0 + m, y0 + m, 1, 1), (x1 - m, y0 + m, -1, 1), (x0 + m, y1 - m, 1, -1), (x1 - m, y1 - m, -1, -1)):
        p = skia.Path(); p.moveTo(x, y + 70 * sy); p.lineTo(x, y); p.lineTo(x + 70 * sx, y)
        cv.drawPath(p, paint("#000000", int(110 * a), "stroke", 13, blur=3))
        cv.drawPath(p, paint("#FFFFFF", int(255 * a), "stroke", 7))


def circulo_mao(cv, x, y, rx, ry, cor, a=1.0, k=1.0, seed=0.0, larg=8):
    """Círculo de caneta (telestrador), traço que se fecha até a fração k."""
    if a <= 0 or k <= 0:
        return
    n = 72; pts = []
    for i in range(n + 10):
        u = i / n
        ang = -math.pi * 0.62 + 2 * math.pi * u
        wob = 1 + 0.035 * math.sin(u * 2 * math.pi * 3 + seed) + 0.018 * math.sin(u * 2 * math.pi * 7 + 2 * seed)
        sp = 1 + 0.07 * u
        pts.append((x + rx * wob * sp * math.cos(ang), y + ry * wob * sp * math.sin(ang)))
    p = poli(pts, fechar=False)
    cv.drawPath(p, trim(paint(FUNDO_CARTAO, int(150 * a), "stroke", larg + 7), k))
    cv.drawPath(p, trim(paint(cor, int(110 * a), "stroke", larg + 10, blur=8), k))
    cv.drawPath(p, trim(paint(cor, int(255 * a), "stroke", larg), k))


def termometro(cv, x, y, nivel, a=1.0, esc=1.0):
    """(cópia do piloto) bulbo e coluna vermelha, SEM número; o único vermelho do vídeo."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-14, -50, 14, 26), 14, 14), paint("#000000", int(70 * a), blur=6))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-12, -48, 12, 24), 12, 12), paint("#EEF3F8", int(255 * a)))
    cv.drawCircle(0, 32, 19, paint("#EEF3F8", int(255 * a)))
    cv.drawCircle(0, 32, 13, paint(VERMELHO, int(255 * a)))
    hh = lerp(6, 64, clamp(nivel))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-5, 26 - hh, 5, 32), 5, 5), paint(VERMELHO, int(255 * a)))
    for k in range(4):
        cv.drawLine(5, -30 + k * 14, 11, -30 + k * 14, paint("#8FA3B8", int(220 * a), "stroke", 2))
    cv.restore()


def selo_serie(cv, a):
    if a <= 0:
        return
    rr = skia.RRect.MakeRectXY(skia.Rect(CX - 190, 150, CX + 190, 204), 27, 27)
    cv.drawRRect(rr, paint("#FFFFFF", int(28 * a)))
    texto(cv, "QUAL DOS DOIS?", CX, 190, F_BLACK, 32, OURO, int(255 * a))


def capa(cv, t, T, l1, l2):
    """Gancho de 2 linhas no topo (o único texto grande do quadro 0); sai no avanço rápido."""
    sai = e_inout(prog(t, T["ff"] - 0.05, T["ff"] + 0.35))
    if sai >= 1:
        return
    a = 1 - sai
    cv.drawRect(skia.Rect(0, 0, W, 360), paint(BG_OUT, 255, shader=skia.GradientShader.MakeLinear(
        [skia.Point(0, 0), skia.Point(0, 360)], [C(BG_OUT, int(235 * a)), C(BG_OUT, 0)])))
    pulso = 1 + 0.025 * math.sin(t * 5)
    cv.save(); cv.translate(CX, 205 - 120 * sai); cv.scale(pulso, pulso)
    texto(cv, l1, 0, 0, F_BLACK, 78, "#FFFFFF", int(255 * a), contorno=10)
    texto(cv, l2, 0, 88, F_BLACK, 78, OURO, int(255 * a), contorno=10)
    cv.restore()


def frase_grande(cv, s, y, cor, a, tam_max=96, larg_max=960, esc=1.0):
    """Rótulo de tela numa string só (o registro confere a frase inteira contra ep['tela'])."""
    if a <= 0:
        return
    tam = tam_max
    while larg_texto(s, F_BLACK, tam) > larg_max and tam > 30:
        tam -= 2
    cv.save(); cv.translate(CX, y); cv.scale(esc, esc)
    texto(cv, s, 0, tam * 0.36, F_BLACK, tam, cor, int(255 * a), contorno=12)
    cv.restore()


# ------------------------------------------------------------------ karaokê (cópia do cf_comum.legenda)
_CURTA = re.compile(r"^[\wÀ-ÿ]{1,2}$")


def _linhas(vivo, tam, esp=26, largura=920):
    linhas, linha, lw = [], [], 0
    for p in vivo:
        w = larg_texto(p["tok"].upper(), F_BLACK, tam)
        if linha and lw + esp + w > largura:
            linhas.append(linha); linha, lw = [], 0
        linha.append((p, w)); lw += (esp if lw else 0) + w
    if linha:
        linhas.append(linha)
    for i in range(len(linhas) - 1):                       # sem palavra curta órfã no fim da linha ('À', 'E')
        while len(linhas[i]) > 1 and _CURTA.match(linhas[i][-1][0]["tok"]):
            linhas[i + 1].insert(0, linhas[i].pop())
    return linhas


def karaoke(cv, blocos, t, destaque, y_base=1395, tam=80, fora=lambda b: False):
    """`fora(b)`: bloco que NÃO se desenha (a frase já está escrita grande), mas que ainda encerra o
    bloco anterior (nenhuma legenda velha fica por baixo da frase grande)."""
    vivo = None
    for i, b in enumerate(blocos):
        ini = b[0]["t"] - 0.12
        fim = blocos[i + 1][0]["t"] - 0.12 if i + 1 < len(blocos) else b[-1]["t"] + b[-1]["d"] + 2.5
        fim = min(fim, b[-1]["t"] + b[-1]["d"] + 2.5)
        if ini <= t < fim:
            vivo = b; break
    if not vivo or fora(vivo):
        return
    esp = 26
    linhas = _linhas(vivo, tam, esp)
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
            cv.save(); cv.translate(x + w / 2, y); cv.scale(esc, esc)     # pop em volta do centro da palavra
            texto(cv, p["tok"].upper(), -w / 2, 0, F_BLACK, tam, cor, int(a * entrada), centro=False, contorno=12)
            cv.restore()
            x += w + esp
        y += alt


def juntar_blocos(blocos):
    """'QUAL MERECE AVALIAÇÃO? A? OU B?' num bloco só (nunca um 'A?' sozinho antes do palpite) e
    'A!' junto de 'OLHA O PASSO:'."""
    out = []
    pend = None
    for b in blocos:
        b = list(b)
        if pend:
            b = pend + b; pend = None
        toks = [p["tok"] for p in b]
        if toks == ["A!"]:
            pend = b; continue
        if out and (toks == ["A?"] or toks[0] == "Ou"):
            out[-1] = out[-1] + b; continue
        out.append(b)
    if pend:
        out.append(pend)
    if not any([p["tok"] for p in b][-3:] == ["A?", "Ou", "B?"] for b in out):
        raise SystemExit("ERRO: o karaokê devia ter o bloco '... A? OU B?'.")
    return out


# ------------------------------------------------------------------ tempos
def _linhas_roteiro(ep):
    return [re.findall(r"[\wÀ-ÿ]+(?:-[\wÀ-ÿ]+)*[.,:;!?—]*", ln) for ln in ep["roteiro"]]


def inserir_palpite(voz, pal, dur=PALPITE):
    idx = [i for i, p in enumerate(pal) if p["tok"] == "B?" and i + 1 < len(pal) and pal[i + 1]["tok"] == "A!"]
    if len(idx) != 1:
        raise SystemExit(f"ERRO: o jogo precisa de exatamente 1 'B?' seguido de 'A!' (achei {len(idx)}).")
    i = idx[0]
    x = pal[i]["t"] + pal[i]["d"] + 0.05
    nova = np.concatenate([voz[:int(x * som.SR)], np.zeros(int(dur * som.SR), voz.dtype), voz[int(x * som.SR):]])
    pal = [dict(p, t=p["t"] + (dur if p["t"] > x else 0.0)) for p in pal]
    return nova, pal, x


ANCORAS = {"a_q": ("tok:A?", 1), "b_q": ("tok:B?", 1), "a_resp": ("tok:A!", 1), "passo": ("passo", 1),
           "mancou1": ("mancou", 1), "avalia": ("avalia", 1), "b_e": ("tok:B?", 2), "sumiu": ("sumiu", 1),
           "brinca": ("brinca", 1), "duas2": ("duas", 2), "pernas": ("pernas", 1), "inchaco": ("inchaço", 1),
           "padrao": ("padrão", 1), "duvida": ("dúvida", 1), "avalie": ("avalie", 1), "mancou2": ("mancou", 2),
           "febre2": ("febre", 2), "procure": ("procure", 1), "dia": ("dia", 1), "manda": ("manda", 1),
           "sono": ("sono", 1)}


def calcular_T(pal, ep, t_pal):
    T = {"palpite": t_pal}
    for chave, (alvo, n) in ANCORAS.items():
        c = 0
        for p in pal:
            ok = p["tok"] == alvo[4:] if alvo.startswith("tok:") else p["w"].lower() == alvo
            if ok:
                c += 1
                if c == n:
                    T[chave] = p["t"]; break
        else:
            raise KeyError(f"âncora não achada no roteiro: {alvo} #{n}")
    # início de cada frase do roteiro (a voz pode juntar/partir palavras: conta pelos tokens)
    toks = [p["tok"] for p in pal]
    linhas = _linhas_roteiro(ep)
    if sum(len(x) for x in linhas) != len(toks):
        raise SystemExit("ERRO: palavras da voz ≠ palavras do roteiro — tempos das cenas sairiam tortos.")
    i = 0
    for k, ln in enumerate(linhas):
        T[f"L{k}"] = pal[i]["t"]; i += len(ln)
    if len(linhas) != 11:
        raise SystemExit("ERRO: o roteiro deste módulo tem 11 frases.")
    T["fim_fala"] = pal[-1]["t"] + pal[-1]["d"]
    T["total"] = T["fim_fala"] + 2.2
    T["ff"] = T["L1"] - 0.15                       # avanço rápido (evento forte perto dos 3 s)
    T["jogo"] = T["L2"] - 0.10                     # entram os dois painéis
    T["rew"] = T["a_resp"] + 0.08                  # volta do A
    T["lento"] = T["a_resp"] + 0.62                # 0,25×
    T["cena_b"] = T["L6"] - 0.10
    T["volta_noite"] = T["L7"] - 0.12
    T["cena_duvida"] = T["L8"] - 0.10
    T["cena_bonus"] = T["L9"] - 0.10
    ordem = ["ff", "jogo", "a_q", "b_q", "palpite", "a_resp", "lento", "mancou1", "avalia", "cena_b", "sumiu",
             "volta_noite", "duas2", "padrao", "cena_duvida", "duvida", "cena_bonus", "mancou2", "febre2",
             "procure", "dia", "manda"]
    if not all(T[a] < T[b] for a, b in zip(ordem, ordem[1:])):
        raise SystemExit("ERRO: ordem das cenas fora do roteiro: " + ", ".join(f"{k}={T[k]:.2f}" for k in ordem))
    return T


# ------------------------------------------------------------------ fases das crianças
FI0_A, FI0_B = 0.30, 0.10


def fi_a(t, T):
    """Fase do A: normal até o 'A!'; VOLTA rápida (◀◀); depois 0,25× começando logo antes do apoio
    curto (o círculo pega o apoio inteiro)."""
    base = FI0_A + (t - T["jogo"]) / P_MAN
    resp = FI0_A + (T["rew"] - T["jogo"]) / P_MAN
    alvo = resp - ((resp - 0.56) % 1.0)
    if resp - alvo < 0.5:
        alvo -= 1.0
    if t < T["rew"]:
        return base
    if t < T["lento"]:
        return lerp(resp, alvo, e_inout(prog(t, T["rew"], T["lento"] - 0.05)))
    return alvo + 0.25 * (t - T["lento"]) / P_MAN


def fi_b(t, T):
    return FI0_B + (t - T["jogo"]) / P_NOR


def luz_palpite(t, T, letra):
    k = t - T["palpite"]
    if not 0 <= k < PALPITE:
        return 0.0
    fase = int(k / 0.5)
    if ("A", "B")[fase % 2] != letra:
        return 0.0
    return clamp((k - fase * 0.5) / 0.05) * (1 - prog(k, PALPITE - 0.2, PALPITE - 0.05))


# ------------------------------------------------------------------ cenas
def cena_noite_inicio(cv, t, T):
    """0 s -> avanço rápido -> manhã com o sofá vazio."""
    if t >= T["jogo"] + 0.45:
        return
    a = 1 - prog(t, T["jogo"], T["jogo"] + 0.4)
    k = prog(t, T["ff"], T["jogo"])                 # progresso do avanço rápido

    def desenho(c, w, h):
        z = e_inout(clamp(k / 0.45))
        c.save()
        cxz, cyz = lerp(w / 2, 292, z), lerp(h / 2, 258, z)
        c.translate(w / 2, h / 2); c.scale(lerp(1.0, 1.72, z), lerp(1.0, 1.72, z)); c.translate(-cxz, -cyz)
        amanhece = e_inout(prog(k, 0.12, 0.85))
        some = prog(k, 0.25, 0.45)
        noite(c, w, h, t, amanhece=amanhece, crianca_a=1 - some, vazio=some >= 1)
        c.restore()
    cv.saveLayer(None, _alfa(a)) if a < 1 else cv.save()
    janela_cena(cv, STAGE, desenho)
    fita = (prog(t, T["ff"], T["ff"] + 0.1) * (1 - prog(t, T["jogo"] - 0.15, T["jogo"])))
    faixas_fita(cv, STAGE, t, fita)
    chip_setas(cv, STAGE[2] - 96, STAGE[3] - 60, True, fita)
    cv.restore()


def painel(cv, r, letra, cor, modo, fi, luz=0.0, a=1.0, dx=0.0, marca=None, marca_a=0.0, bola_on=False, ref=None,
           selo_cor=None, **kw):
    """`cor` = borda (neutra); `selo_cor` = selo da letra (neutro no palpite, a cor só na revelação)."""
    if a <= 0:
        return None
    cv.saveLayer(None, _alfa(a)) if a < 1 else cv.save()
    cv.translate(dx, 0)
    out = janela_cena(cv, r, lambda c, w, h: manha(c, w, h, modo, fi, bola_on, ref, **kw), borda=cor, a_borda=255,
                      marca=marca, marca_a=marca_a, luz=luz)
    if letra:
        selo_letra(cv, letra, r[0] + 66, r[1] + 66, selo_cor or SELO)
    cv.restore()
    return out


def cena_jogo(cv, t, T):
    """Os dois painéis empilhados até o 'A!'; depois o A cresce e o B sai."""
    if t < T["jogo"] or t >= T["cena_b"] + 0.4:
        return
    ent = e_out(prog(t, T["jogo"], T["jogo"] + 0.45))
    cresce = e_inout(prog(t, T["a_resp"], T["a_resp"] + 0.45))
    sai_tudo = prog(t, T["cena_b"], T["cena_b"] + 0.35)
    # B
    a_b = 1 - prog(t, T["a_resp"], T["a_resp"] + 0.3)
    painel(cv, PAN_B, "B", COR_B, "normal", fi_b(t, T), luz_palpite(t, T, "B"), a_b, dx=(1 - ent) * 1100)
    # A
    r = tuple(lerp(p, q, cresce) for p, q in zip(PAN_A, STAGE))
    lento = prog(t, T["lento"] - 0.05, T["lento"] + 0.15)
    marca_a = prog(t, T["a_resp"], T["a_resp"] + 0.15) * (1 + 0.5 * bump(t, T["avalia"], 0.4))
    estado = {}
    a_pegada = lento * (1 - sai_tudo)

    def ref(c, pose, quando):
        """Replay: a PEGADA acende só enquanto o pé está no chão — branca e longa na perna boa,
        laranja e curta na que dói (o tempo de apoio, sem olhar para os dedos)."""
        estado["pose"] = pose
        if a_pegada <= 0:
            return
        for chave, lado_, cor in (("boa_no_chao", "longe", "#FFFFFF"), ("dor_no_chao", "perto", LARANJA)):
            if pose.get(chave):
                x = pose[lado_][0][0] + 22 - (10 if lado_ == "longe" else 0)
                c.drawOval(skia.Rect(x - 78, SOLA - 16, x + 92, SOLA + 22), paint(cor, int(150 * a_pegada), blur=12))
                c.drawOval(skia.Rect(x - 62, SOLA - 6, x + 76, SOLA + 14), paint(cor, int(235 * a_pegada), "stroke", 6))
        # linha tracejada de referência (altura do cós no apoio da perna BOA) ATRÁS da criança: não
        # risca o tronco nem o braço; aparece dos dois lados e o cós que cai fica visível abaixo dela
        y_ref = -102
        for x0 in range(-420, 470, 48):
            c.drawLine(x0, y_ref, x0 + 28, y_ref, paint(FUNDO_CARTAO, int(230 * a_pegada), "stroke", 9))
            c.drawLine(x0, y_ref, x0 + 28, y_ref, paint("#FFFFFF", int(255 * a_pegada), "stroke", 4))
    sel_a = LARANJA if t >= T["a_resp"] else SELO
    res = painel(cv, r, "A", COR_A, "manca", fi_a(t, T), luz_palpite(t, T, "A"), 1 - sai_tudo, dx=-(1 - ent) * 1100,
                 marca=LARANJA, marca_a=clamp(marca_a), ref=ref, selo_cor=sel_a)
    if res and lento > 0 and sai_tudo < 1:
        pose, hx, hy, s = res
        cv.save(); cv.translate(r[0], r[1])
        cv.clipRRect(_rr((0, 0, r[2] - r[0], r[3] - r[1])), skia.ClipOp.kIntersect, True)
        a = lento * (1 - sai_tudo)
        if pose["dor_no_chao"]:                              # o círculo dura SÓ o apoio curto: envolve o
            u = pose["dor_fase"]                             # CÓS que cai abaixo da linha (não a mão)
            k = e_out(clamp(u / 0.30)); sai = prog(u, 0.50, 0.66)   # sai ANTES de a mão chegar à frente do quadril
            sil = silhueta_braco_perto(pose)                 # o braço passa NA FRENTE do círculo (3ª rodada:
            mt = skia.Matrix(); mt.setScale(s, s); mt.postTranslate(hx, hy)   # o círculo envolvia o punho)
            sil.transform(mt)
            cv.save(); cv.clipPath(sil, skia.ClipOp.kDifference, True)
            circulo_mao(cv, hx + 56 * s, hy + (-92 + pose["hip"][1]) * s, 46 * s, 42 * s, LARANJA,
                        a * (1 - sai), k, seed=1.3)
            cv.restore()
        cv.restore()
        cantoneiras(cv, r, a)
        chip_lento(cv, r[2] - 110, r[3] - 52, a)
    chip_setas(cv, r[2] - 96, r[3] - 60, False, prog(t, T["rew"], T["rew"] + 0.08) * (1 - prog(t, T["lento"] - 0.12, T["lento"])))
    faixas_fita(cv, r, t, prog(t, T["rew"], T["rew"] + 0.08) * (1 - prog(t, T["lento"] - 0.12, T["lento"])))


def cena_b(cv, t, T):
    if t < T["cena_b"] or t >= T["volta_noite"] + 0.4:
        return
    ent = e_out(prog(t, T["cena_b"], T["cena_b"] + 0.4))
    a = 1 - prog(t, T["volta_noite"] + 0.05, T["volta_noite"] + 0.35)
    fi = 0.2 + (t - T["cena_b"]) / P_RUN * lerp(0.6, 1.0, prog(t, T["sumiu"], T["brinca"]))
    marca_a = prog(t, T["cena_b"] + 0.2, T["cena_b"] + 0.4) * (1 + 0.5 * bump(t, T["brinca"], 0.4))
    k = prog(t, T["cena_b"] + 0.1, T["volta_noite"] - 0.15)
    painel(cv, STAGE, "B", COR_B, "corre", fi, a=a * clamp(ent * 2), dx=(1 - ent) * 300, marca=OURO,
           marca_a=clamp(marca_a), bola_on=True, selo_cor=OURO, bola_k=k, avanco=lerp(-0.14, 0.06, e_inout(k)), escala=1.34)


def cena_noite_volta(cv, t, T):
    if t < T["volta_noite"] or t >= T["cena_duvida"] + 0.4:
        return
    a = prog(t, T["volta_noite"], T["volta_noite"] + 0.3) * (1 - prog(t, T["cena_duvida"], T["cena_duvida"] + 0.35))
    aperta = bump(t, T["duas2"], 0.4) + bump(t, T["pernas"], 0.4)
    cv.saveLayer(None, _alfa(a)) if a < 1 else cv.save()
    janela_cena(cv, STAGE, lambda c, w, h: noite(c, w, h, t, aperta=aperta))
    rew = prog(t, T["volta_noite"], T["volta_noite"] + 0.08) * (1 - prog(t, T["volta_noite"] + 0.55, T["volta_noite"] + 0.7))
    faixas_fita(cv, STAGE, t, rew)
    chip_setas(cv, STAGE[2] - 96, STAGE[3] - 60, False, rew)
    cv.restore()


def cena_duvida(cv, t, T):
    """REGRA FIXA DA SÉRIE: o lado 'espero' nunca termina sem 'NA DÚVIDA, AVALIE.' — sobre a manhã."""
    if t < T["cena_duvida"] or t >= T["cena_bonus"] + 0.4:
        return
    a = prog(t, T["cena_duvida"], T["cena_duvida"] + 0.3) * (1 - prog(t, T["cena_bonus"], T["cena_bonus"] + 0.3))
    painel(cv, PAN_A, "A", COR_A, "manca", fi_a(t, T), a=a, selo_cor=LARANJA, marca=LARANJA, marca_a=0.6)
    painel(cv, PAN_B, "B", COR_B, "normal", fi_b(t, T), a=a, selo_cor=OURO, marca=OURO, marca_a=0.6)


def cena_bonus(cv, t, T):
    if t < T["cena_bonus"]:
        return
    a = prog(t, T["cena_bonus"], T["cena_bonus"] + 0.3) * (1 - prog(t, T["manda"] - 0.35, T["manda"] - 0.12))
    if a <= 0:
        return
    fi = 0.3 + (t - T["cena_bonus"]) / P_MAN
    marca_a = prog(t, T["mancou2"] - 0.05, T["mancou2"] + 0.2) * (1 + 0.5 * bump(t, T["procure"], 0.45))
    painel(cv, STAGE, None, "#FFFFFF", "manca", fi, a=a, marca=LARANJA, marca_a=clamp(marca_a))
    kt = prog(t, T["mancou2"] - 0.2, T["mancou2"] + 0.2)          # entra JUNTO com a pergunta
    if kt > 0:                                       # termômetro GRANDE sem número, a coluna sobe
        nivel = lerp(0.08, 1.0, e_inout(prog(t, T["febre2"], T["febre2"] + 0.8)))
        esc = 3.6 * (1 + 0.06 * bump(t, T["febre2"] + 0.8, 0.3))
        termometro(cv, lerp(1150, 880, e_out(kt)), 640, nivel, clamp(kt * 3) * a, esc)


def placa(cv, y0, y1, a, cor_borda):
    if a <= 0:
        return
    rr = skia.RRect.MakeRectXY(skia.Rect(46, y0, W - 46, y1), 34, 34)
    cv.drawRRect(rr, paint("#000000", int(110 * a), blur=14))
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(240 * a)))
    cv.drawRRect(rr, paint(cor_borda, int(255 * a), "stroke", 5))


def textos_grandes(cv, t, T):
    # REGRA FIXA DA SÉRIE: placa própria, maior que o karaokê, entrada em carimbo
    a = prog(t, T["duvida"] - 0.25, T["duvida"] - 0.05) * (1 - prog(t, T["cena_bonus"] - 0.22, T["cena_bonus"] + 0.02))
    if a > 0:
        car = e_back(clamp((t - (T["duvida"] - 0.25)) / 0.32))
        cv.save(); cv.translate(CX, 1390); cv.scale(lerp(1.25, 1.0, car), lerp(1.25, 1.0, car)); cv.translate(-CX, -1390)
        placa(cv, 1262, 1520, a, OURO)
        frase_grande(cv, "NA DÚVIDA,", 1335, "#FFFFFF", a, 104)
        frase_grande(cv, "AVALIE.", 1448, OURO, a, 116, esc=1 + 0.07 * bump(t, T["avalie"], 0.35))
        cv.restore()
    sai = 1 - prog(t, T["manda"] - 0.35, T["manda"] - 0.12)
    a1 = prog(t, T["mancou2"] - 0.2, T["mancou2"] + 0.0) * sai
    placa(cv, 1250, 1535, a1, LARANJA)
    frase_grande(cv, "MANCOU COM FEBRE?", 1302, "#FFFFFF", a1, 68, esc=1 + 0.05 * bump(t, T["febre2"], 0.35))
    a2 = prog(t, T["procure"] - 0.15, T["procure"] + 0.05) * sai
    frase_grande(cv, "PROCURE ATENDIMENTO", 1395, LARANJA, a2, 86, larg_max=960, esc=1 + 0.05 * bump(t, T["procure"], 0.35))
    frase_grande(cv, "NO MESMO DIA.", 1487, LARANJA, a2, 86, larg_max=960, esc=1 + 0.06 * bump(t, T["dia"], 0.35))


def mini_noite(cv, t, T):
    k = prog(t, T["manda"] + 0.05, T["manda"] + 0.45)
    if k <= 0:
        return
    e = e_back(k)
    w, h = STAGE[2] - STAGE[0], STAGE[3] - STAGE[1]
    cv.save(); cv.translate(CX, 300); cv.rotate(-3 + 2 * math.sin(t * 2)); cv.scale(0.27 * e, 0.27 * e)
    cv.translate(-w / 2 - STAGE[0], -h / 2 - STAGE[1])
    cv.saveLayer(None, _alfa(clamp(k * 3)))
    janela_cena(cv, STAGE, lambda c, ww, hh: noite(c, ww, hh, t), borda=OURO, a_borda=255)
    cv.restore()
    cv.restore()


def bifurcacao(cv, t, T):
    """'Mesma noite, duas manhãs': a MESMA cena da noite em miniatura (canto de cima) e dela saem DOIS
    ramos, um para o A e outro para o B — as duas manhãs possíveis da MESMA criança (sem texto novo)."""
    a = (prog(t, T["jogo"] + 0.15, T["jogo"] + 0.45) * (1 - prog(t, T["a_resp"] - 0.1, T["a_resp"] + 0.2))
         + prog(t, T["cena_duvida"], T["cena_duvida"] + 0.3) * (1 - prog(t, T["cena_bonus"], T["cena_bonus"] + 0.3)))
    a = clamp(a)
    if a <= 0:
        return
    k = 1.0 if t >= T["cena_duvida"] else e_inout(prog(t, T["L2"] + 0.1, T["L2"] + 0.9))   # ramos se desenham
    w, h = STAGE[2] - STAGE[0], STAGE[3] - STAGE[1]
    e = 0.165; mx0, my0 = 52, 214                                         # miniatura 165 x 145
    mw, mh = w * e, h * e
    cv.saveLayer(None, _alfa(a))
    ramo_a = skia.Path(); ramo_a.moveTo(106, my0 + mh); ramo_a.lineTo(106, 378)          # -> selo A
    ramo_b = skia.Path(); ramo_b.moveTo(mx0, my0 + mh * 0.6); ramo_b.lineTo(20, my0 + mh * 0.6)
    ramo_b.lineTo(20, 872); ramo_b.lineTo(58, 872)                                        # -> selo B
    for rp in (ramo_a, ramo_b):
        cv.drawPath(rp, trim(paint(FUNDO_CARTAO, 230, "stroke", 13), k))
        cv.drawPath(rp, trim(paint(OURO, 255, "stroke", 6), k))
    if k > 0.97:                                                          # pontas de seta
        for tri in ([(106, 392), (93, 372), (119, 372)], [(72, 872), (52, 859), (52, 885)]):
            cv.drawPath(poli(tri), paint(FUNDO_CARTAO, 230, "stroke", 6))
            cv.drawPath(poli(tri), paint(OURO, 255))
    cv.save(); cv.translate(mx0, my0); cv.scale(e, e); cv.translate(-STAGE[0], -STAGE[1])
    janela_cena(cv, STAGE, lambda c, ww, hh: noite(c, ww, hh, t), borda=OURO, a_borda=255)
    cv.restore()
    cv.restore()


def fundo_rapido(cv, t):
    """= cf_alongamento.fundo, com o degradê radial (o que mais pesa no quadro) feito UMA vez numa
    imagem 80 px mais alta: mover o centro do degradê na vertical é deslizar a imagem."""
    def faz(c):
        sh = skia.GradientShader.MakeRadial(skia.Point(W / 2, H * 0.42 + 40), H * 0.78, [C(BG_IN), C(BG_OUT)])
        c.drawRect(skia.Rect(0, 0, W, H + 80), paint(BG_IN, shader=sh))
    cv.drawImage(_imagem(("fundo",), W, H + 80, faz), 0, 40 * math.sin(t * 0.3) - 40)
    for x, y, v, r, a in PART:
        yy = (y - v * t * 6) % H
        cv.drawCircle(x + 8 * math.sin(t * 0.5 + y), yy, r, paint("#BFE3FF", int(a)))


def quadro(cv, t, T, blocos, ep):
    fundo_rapido(cv, t)
    cena_noite_inicio(cv, t, T)
    cena_jogo(cv, t, T)
    cena_b(cv, t, T)
    cena_noite_volta(cv, t, T)
    cena_duvida(cv, t, T)
    cena_bonus(cv, t, T)
    bifurcacao(cv, t, T)
    capa(cv, t, T, ep["gancho"][0], ep["gancho"][1])
    selo_serie(cv, prog(t, T["jogo"], T["jogo"] + 0.35) * (1 - prog(t, T["manda"] - 0.35, T["manda"] - 0.12)))
    if 0.1 <= t < T["manda"] - 0.15:                 # karaokê desde 0,1 s; nas frases escritas grandes, não duplica
        karaoke(cv, blocos, t, DESTAQUE,
                fora=lambda b: T["L8"] - 0.01 <= b[0]["t"] < T["L10"] - 0.01 or b[0]["w"].lower() == "manda")
    textos_grandes(cv, t, T)
    interface(cv, t, T, [b for b in blocos if b[0]["w"].lower() == "manda"], DESTAQUE)
    mini_noite(cv, t, T)


# ------------------------------------------------------------------ som
def sons(T):
    ev = [(0.05, "pop", 0.45), (0.6, "tick", 0.15), (T["ff"], "whoosh", 0.55), (T["ff"] + 0.35, "shimmer", 0.4),
          (T["jogo"], "whoosh", 0.4), (T["jogo"] + 0.3, "pop", 0.45), (T["a_q"], "pop", 0.55), (T["b_q"], "pop", 0.55)]
    ev += [(T["palpite"] + 0.5 * i, "tick" if i % 2 == 0 else "click", 0.8 if i % 2 == 0 else 1.0) for i in range(2)]
    ev += [(T["a_resp"], "thump", 0.65), (T["a_resp"] + 0.02, "pop", 0.5), (T["rew"], "whoosh", 0.45),
           (T["lento"], "click", 0.6), (T["mancou1"], "tick", 0.4), (T["avalia"], "thump", 0.45),
           (T["cena_b"], "whoosh", 0.4), (T["sumiu"], "pop", 0.45), (T["brinca"], "ding", 0.35),
           (T["volta_noite"], "whoosh", 0.45), (T["duas2"], "pop", 0.4), (T["pernas"], "pop", 0.35),
           (T["cena_duvida"], "whoosh", 0.35), (T["duvida"], "thump", 0.55), (T["cena_bonus"], "whoosh", 0.35),
           (T["mancou2"], "pop", 0.5), (T["febre2"], "tick", 0.6), (T["febre2"] + 0.1, "shimmer", 0.3),
           (T["procure"], "thump", 0.5), (T["manda"] + 0.05, "whoosh", 0.5), (T["sono"], "pop", 0.4)]
    return ev


def _media_movel(x, w):
    xp = np.concatenate([np.zeros(w // 2), x, np.zeros((w - 1) // 2)])
    c = np.concatenate([[0.0], np.cumsum(xp)])
    return (c[w:w + len(x)] - c[:len(x)]) / w


def mixar_jogo(voz, dur, eventos, jan, ganho_trilha=0.40, fundo_palpite=0.45, rampa=0.15):
    """(do piloto) som.mixar + envelope que baixa a trilha na janela do palpite (o tique-taque aparece,
    sem silêncio)."""
    n = int(dur * som.SR)
    v = np.zeros(n); v[:min(n, len(voz))] = voz[:n]
    musica = som.trilha(dur) * ganho_trilha
    envv = np.sqrt(np.maximum(_media_movel(v ** 2, int(0.06 * som.SR)), 0.0))
    duck = _media_movel(np.where(envv > 0.02, 0.38, 1.0), int(0.25 * som.SR))
    tt = np.arange(n) / som.SR
    env = np.ones(n)
    for a, b in jan:
        k = np.clip((tt - (a - rampa)) / rampa, 0, 1) * np.clip(((b + rampa) - tt) / rampa, 0, 1)
        env = np.minimum(env, 1 - (1 - fundo_palpite) * k)
    fx = np.zeros(n)
    for t0, nome, g in eventos:
        s = som.SFX[nome]()
        p = int(t0 * som.SR)
        if 0 <= p < n:
            m = min(len(s), n - p)
            fx[p:p + m] += s[:m] * g
    mix = v + musica * duck * env + fx * 0.7
    pico = np.max(np.abs(mix)) or 1.0
    return mix / pico * 0.89


# ------------------------------------------------------------------ entrada
def tempos_previa(T):
    return (0.0, 1.3, T["ff"] + 0.35, T["jogo"] - 0.2, T["jogo"] + 0.8, T["palpite"] + 0.5, T["a_resp"] + 0.3,
            T["lento"] + 0.5, T["lento"] + 1.2, T["lento"] + 1.9, T["cena_b"] + 0.9, T["volta_noite"] + 0.3,
            T["pernas"] + 0.2, T["duvida"] + 0.2, T["mancou2"] + 0.2, T["febre2"] + 0.7, T["dia"] + 0.2,
            T["manda"] + 0.8, T["total"] - 0.1)


def preparar(ep, tmp):
    roteiro = "\n".join(ep["roteiro"])
    voz_bruta, palavras = _voz.narrar(roteiro, _voz.RITMO_COMO_FUNCIONA, os.path.join(tmp, "voz"))
    voz_c, pal, tirado = comprimir(voz_bruta, palavras, respiro_cta=0.6)
    pal = alinhar(pal, roteiro)
    voz_c, pal, t_pal = inserir_palpite(voz_c, pal)
    T = calcular_T(pal, ep, t_pal)
    if not T["b_q"] < T["palpite"] < T["a_resp"]:
        raise SystemExit("ERRO: o palpite tem de ficar entre o 'B?' e o 'A!'.")
    return voz_c, pal, T, tirado


def render(ep, mp4, tmp, previa=False):
    voz_c, pal, T, tirado = preparar(ep, tmp)
    print(f"{ep['id']}: silêncio cortado {tirado:.2f}s | avanço em {T['ff']:.2f}s | palpite em {T['palpite']:.2f}s"
          f" | A! em {T['a_resp']:.2f}s | duração final {T['total']:.2f}s")
    blocos = juntar_blocos(montar_blocos(pal))

    def quadro_t(cv, t):
        quadro(cv, t, T, blocos, ep)

    if previa:
        return _previas(quadro_t, tempos_previa(T), tmp, ep["id"]), T["total"]
    wav = os.path.join(tmp, f"{ep['id']}_mix.wav")
    som.gravar_wav(wav, mixar_jogo(voz_c, T["total"], sons(T), [(T["palpite"], T["palpite"] + PALPITE)]))
    codificar(quadro_t, T["total"], wav, mp4)
    return mp4, T["total"]
