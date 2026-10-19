# -*- coding: utf-8 -*-
"""COMO FUNCIONA — pé torto congênito ("PÉ TORTO SE / CORRIGE COM GESSO?").

Mesmo estilo e mesmas peças das cenas aprovadas (fundo azul-petróleo com partículas, marfim,
dourado, rótulos, carimbo, legenda karaokê, CTA com aviãozinho). Storyboard e correções do
verificador (lote3_cf/cf_pe_torto_storyboard.json) respeitados aqui:
  * A perninha é de DESENHO, vista de lado: contorno arredondado e pele lisa, sem nenhum osso por
    dentro, nada translúcido, nenhum exame simulado. Ela vem de cima e se dissolve no fundo (sem
    joelho nem coxa).
  * O pé torto é o mesmo pé, só que girado pra baixo e torcido pra dentro (a sola aparece e os
    dedos se abrem em leque). Cada troca de gesso gira UM passo pequeno em direção à linha-alvo
    tracejada — direção, sem rótulo e sem desenho do pé "ideal". ORDEM (Ponseti, esquemática): a
    manipulação e os primeiros gessos DESTORCEM o pé (sai o "pra dentro") ainda apontando pra baixo;
    o "pra baixo" é corrigido por último. Nenhuma seta empurra a ponta do pé pra cima.
  * "Gessos, aos poucos": um rolo de atadura esquemático entra rolando e solta a faixa em trancos
    curtos; em "gesso" ele sobe pela perna e vira a faixa que enrola. Cada gesso fica PARADO
    segurando o pé antes da troca seguinte.
  * Rastro de movimento: só enquanto o pé gira, some em < 0,5 s; nunca dois pés parados lado a
    lado; nenhum rastro no último passo nem no fim. Nada de "DEPOIS", nada de brilho de sucesso: no
    fim a linha-alvo só se apaga.
  * Gesso rígido: na "flexibilidade" só um halo pulsa em volta; o gesso não se deforma. Sem serra,
    sem corte: o gesso se abre em duas metades e desliza para fora.
  * Órtese = contorno tracejado dourado em volta do pé (nenhum modelo de aparelho, nenhuma barra).
  * Acompanhamento: o pé recua inteiro, sem mudar; a linha do tempo não tem data nem número e os
    marcadores são círculos neutros (sem check); a perna não cresce.
  * Nenhum número de gessos, semanas ou meses na tela.
A cena é PRESA ao roteiro pelas palavras-âncora (ANCORAS): roteiro sem elas = KeyError no render,
em vez de vídeo dessincronizado. Todo texto desenhado está em ep["tela"].
"""
import math

import skia

from .cf_alongamento import (BG_OUT, F_BLACK, F_SEMI, OURO, W, C, clamp, e_back, e_inout, e_out, fundo,
                             larg_texto, lerp, paint, prog, texto)
from .cf_comum import capa, fazer_render, interface, selo_como_funciona
from .cf_fratura_cola import calendario

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "torto": ("torto", 1, False), "nasce": ("nasce", 1, False), "baixo": ("baixo", 1, False),
    "dentro": ("dentro", 1, False), "comum": ("comum", 1, False), "culpa": ("culpa", 1, False),
    "gravidez": ("gravidez", 1, False), "quem": ("quem", 1, False), "gessos": ("gessos", 1, False),
    "poucos": ("poucos", 1, False), "primeiras": ("primeiras", 1, False), "manip": ("manipulação", 1, False), "gesso": ("gesso", 1, False),
    "troca": ("troca", 1, False), "corrige2": ("corrige", 2, False), "pouco": ("pouco", 1, False),
    "gesso3": ("gesso", 3, False), "apos": ("após", 1, False), "cedo": ("cedo", 1, False),
    "flex": ("flexibilidade", 1, False), "depois": ("depois", 1, False), "ortese": ("órtese", 1, False),
    "manter": ("manter", 1, False), "acomp": ("acompanhamento", 1, False),
    "cresc": ("crescimento", 1, False), "manda": ("manda", 1, False),
}
DESTAQUE = {"torto", "baixo", "dentro", "comum", "gessos", "primeiras", "semanas", "manipulação",
            "suave", "troca", "pouco", "cedo", "flexibilidade", "órtese", "manter", "acompanhamento",
            "crescimento"}

# ------------------------------------------------------------------ paleta
PELE, PELE_CL, PELE_ESC, PELE_LINHA = "#F0B49A", "#F7CDB8", "#DA987E", "#B9765E"
PELE_FUNDO = "#8A4A3A"                     # tom quente em que o topo da perna escurece antes de sumir
SOLA = "#E7867A"
GESSO, GESSO_B, GESSO_L = "#F4EEE3", "#DCCFB8", "#B7A688"
CORAL = "#FF8A6B"
AZUL = "#9CC9FF"
FUNDO_CARTAO = "#0B1824"

# ------------------------------------------------------------------ perna (vista de lado; a frente do pé aponta para a esquerda)
PX, PY = 660.0, 800.0                      # tornozelo: pivô do pé (câmera neutra)
Y_DISS0, Y_DISS1 = 380.0, 440.0            # a perna se dissolve no fundo (sem retângulo por cima)
_PERNA = [(250, 112), (420, 114), (560, 108), (680, 94), (760, 82), (812, 76)]   # (y, meia-largura)


def perna_path(dr=0.0, y_min=None, y_max=None):
    p = skia.Path()
    pts = [(y, hw + dr) for y, hw in _PERNA]
    p.moveTo(PX - pts[0][1], pts[0][0])
    for (y0, h0), (y1, h1) in zip(pts, pts[1:]):
        ym = (y0 + y1) / 2
        p.cubicTo(PX - h0, ym, PX - h1, ym, PX - h1, y1)
    yb, hb = pts[-1]
    p.cubicTo(PX - hb, yb + hb * 0.55, PX - hb * 0.55, yb + hb * 0.62 + dr * 0.3, PX, yb + hb * 0.62 + dr * 0.3)
    p.cubicTo(PX + hb * 0.55, yb + hb * 0.62 + dr * 0.3, PX + hb, yb + hb * 0.55, PX + hb, yb)
    for (y0, h0), (y1, h1) in zip(reversed(pts), list(reversed(pts))[1:]):
        ym = (y0 + y1) / 2
        p.cubicTo(PX + h0, ym, PX + h1, ym, PX + h1, y1)
    p.close()
    if y_min is not None or y_max is not None:
        r = skia.Path(); r.addRect(skia.Rect(-500, y_min if y_min is not None else -2000, W + 500,
                                             y_max if y_max is not None else 4000))
        p = skia.Op(p, r, skia.PathOp.kIntersect_PathOp)
    return p


def meia_largura(y):
    for (y0, h0), (y1, h1) in zip(_PERNA, _PERNA[1:]):
        if y0 <= y <= y1:
            return lerp(h0, h1, (y - y0) / (y1 - y0))
    return _PERNA[0][1] if y < _PERNA[0][0] else _PERNA[-1][1]


# ------------------------------------------------------------------ pé: dois desenhos do MESMO pé, interpolados
# deslocamentos (x, y) a partir do tornozelo, já na tela (a frente do pé aponta para a esquerda). Cada ponto
# vai de um desenho ao outro em coordenadas POLARES em volta do tornozelo: a ponta do pé faz um arco (gira),
# não um atalho em linha reta, e o que está preso à canela fica parado.
_NORMAL = [(70, -80),
           ((80, -30), (104, 0), (98, 40)),             # atrás do tornozelo -> calcanhar
           ((96, 80), (80, 104), (48, 104)),            # calcanhar
           ((-30, 100), (-100, 106), (-160, 100)),      # sola
           ((-214, 96), (-268, 98), (-292, 82)),        # bola do pé
           ((-312, 68), (-312, 46), (-296, 36)),        # ponta
           ((-256, 24), (-200, 14), (-150, 6)),         # dorso
           ((-100, -2), (-78, -30), (-72, -74))]        # peito do pé -> canela
_TORTO = [(70, -80),
          ((78, -40), (86, -8), (80, 20)),              # calcanhar pequeno e alto
          ((74, 50), (56, 74), (40, 98)),
          ((20, 140), (-6, 200), (-36, 240)),           # sola (virada para trás e para quem assiste)
          ((-58, 270), (-70, 298), (-92, 306)),         # a frente do pé curva pra dentro
          ((-114, 314), (-136, 302), (-140, 280)),      # ponta
          ((-144, 232), (-140, 172), (-130, 120)),      # dorso
          ((-116, 60), (-84, 6), (-72, -74))]
_SOLA_N = [(48, 104), (-60, 102), (-160, 100), (-250, 94)]
_SOLA_T = [(34, 96), (0, 167), (-36, 232), (-82, 292)]           # rente à borda de trás: a sola aparece
_DORSO_N = [(-70, 30), (-150, 26), (-235, 34)]
_DORSO_T = [(-112, 100), (-122, 165), (-122, 230)]
# dedos: em leque (pé torcido, a sola de frente) -> de perfil (só a ponta dos menores aparece)
_DEDOS_T = [(-82, 304, 20), (-101, 313, 16), (-118, 310, 14.5), (-132, 299, 13), (-140, 284, 11.5)]
_DEDOS_N = [(-292, 66, 25), (-284, 46, 15), (-275, 36, 13), (-264, 28, 11.5), (-253, 22, 10.5)]
ANG_T, ANG_N = 111.0, 171.0                 # direção do pé (graus de tela) no pé torto e alinhado
K_FIM = 0.87                                # o pé chega PERTO da linha-alvo (sem "pé perfeito")

# ORDEM DA CORREÇÃO (Ponseti, esquemático): primeiro o pé DESTORCE ("pra dentro" sai: a sola some, os
# dedos voltam ao perfil) ainda apontando pra baixo; o "pra baixo" é o ÚLTIMO a sair. Por isso há um
# desenho do meio, _MEIO = o pé alinhado girado pra baixo (o mesmo ângulo do pé torto), e cada ponto
# vai TORTO -> MEIO (destorção, md) e MEIO -> ALINHADO (elevação, me). Nada força o pé pra cima cedo.
_DELTA = ANG_T - ANG_N
_PESO = [0.0, (0.2, 0.45, 0.7), (0.85, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, 1.0),
         (1.0, 1.0, 1.0), (0.85, 0.45, 0.0)]          # o que está preso à canela não gira


def _gira(p, w=1.0):
    a = math.radians(_DELTA * w)
    return p[0] * math.cos(a) - p[1] * math.sin(a), p[0] * math.sin(a) + p[1] * math.cos(a)


_MEIO = [_NORMAL[0]] + [tuple(_gira(q, w) for q, w in zip(seg, ws)) for seg, ws in zip(_NORMAL[1:], _PESO[1:])]


def destorcao(k):
    """'pra dentro' saindo: rápido nos primeiros passos."""
    return 1 - (1 - clamp(k / 0.55)) ** 2


def elevacao(k):
    """'pra baixo' saindo: só depois da destorção."""
    return clamp((k - 0.22) / 0.78)


def _pol_rel(p, q, m):
    """Ponto entre p e q em coordenadas POLARES em volta do tornozelo (gira, não corta caminho)."""
    r0, r1 = math.hypot(*p), math.hypot(*q)
    a0, a1 = math.atan2(p[1], p[0]), math.atan2(q[1], q[0])
    d = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
    r, a = lerp(r0, r1, m), a0 + d * m
    return r * math.cos(a), r * math.sin(a)


def _pol3(pt, pm, pn, k):
    """pé torto -> pé do meio (destorção) -> pé alinhado (elevação); devolve o ponto na tela."""
    q = _pol_rel(_pol_rel(pt, pm, destorcao(k)), pn, elevacao(k))
    return PX + q[0], PY + q[1]


def pe_contorno(k):
    p = skia.Path(); p.moveTo(*_pol3(_TORTO[0], _MEIO[0], _NORMAL[0], k))
    for st, sm, sn in zip(_TORTO[1:], _MEIO[1:], _NORMAL[1:]):
        c1, c2, q = (_pol3(st[i], sm[i], sn[i], k) for i in range(3))
        p.cubicTo(*c1, *c2, *q)
    p.close()
    return p


def _ang(k):
    return math.radians(lerp(ANG_T, ANG_N, elevacao(k)))


def eixo(k):
    """Referencial do pé na tela: (a = ao longo do pé, b = rumo à sola) -> tela."""
    fx, fy = math.cos(_ang(k)), math.sin(_ang(k))
    return skia.Matrix.MakeAll(fx, fy, PX, fy, -fx, PY, 0, 0, 1)


def no_eixo(k, a, b):
    fx, fy = math.cos(_ang(k)), math.sin(_ang(k))
    return PX + a * fx + b * fy, PY + a * fy - b * fx


def inflar(p, d):
    if d <= 0:
        return p
    pt = skia.Paint(AntiAlias=True); pt.setStyle(skia.Paint.kStroke_Style); pt.setStrokeWidth(2 * d)
    pt.setStrokeJoin(skia.Paint.kRound_Join)
    s = skia.Path(); pt.getFillPath(p, s)
    return skia.Op(p, s, skia.PathOp.kUnion_PathOp)


def pe_path(k, d=0.0, a_max=None):
    p = inflar(pe_contorno(k), d)
    if a_max is not None:                         # corta perpendicular ao pé (o gesso para antes dos dedos)
        r = skia.Path(); r.addRect(skia.Rect(-400, -400, a_max, 400)); r.transform(eixo(k))
        p = skia.Op(p, r, skia.PathOp.kIntersect_PathOp)
    return p


def dedos_tela(k):
    md = destorcao(k)
    return [(*_pol3(t[:2], _gira(n[:2]), n[:2], k), lerp(t[2], n[2], md)) for t, n in zip(_DEDOS_T, _DEDOS_N)]


def curva_pe(k, ts, ns):
    return [_pol3(t, _gira(n), n, k) for t, n in zip(ts, ns)]


# ------------------------------------------------------------------ linha do tempo do tratamento
def _ciclos(T):
    """Duas trocas rítmicas de 'gesso após gesso' (sem número na tela): [(início, período)].
    Cada gesso fica PARADO segurando o pé um tempo antes do próximo (segurar é a função dele)."""
    t0 = T["gesso3"] + 0.15
    P = (T["flex"] - 0.12 - t0) / 2
    return [(t0 + i * P, P) for i in range(2)]


K_MANIP, K_TROCA = 0.08, 0.27


def passos(T):
    """[(t_ini, t_fim, k_ini, k_fim, com_rastro)] — cada giro do pé."""
    ps = [(T["manip"] + 0.25, T["manip"] + 1.0, 0.0, K_MANIP, False),
          (T["corrige2"] - 0.1, T["pouco"], K_MANIP, K_TROCA, True)]
    k = K_TROCA
    for i, (c, P) in enumerate(_ciclos(T)):
        k1 = K_TROCA + (K_FIM - K_TROCA) * (i + 1) / 2
        ps.append((c + 0.22 * P, c + 0.48 * P, k, k1, i < 1))
        k = k1
    return ps


def k_em(t, T):
    k = 0.0
    for t0, t1, k0, k1, _ in passos(T):
        if t >= t1:
            k = k1
        elif t > t0:
            return lerp(k0, k1, e_inout(prog(t, t0, t1)))
        else:
            break
    return k


def gessos(T):
    """[(t_on0, t_on1, t_off0, t_off1)]: enrola de cima até o pé; sai em duas metades."""
    g = [(T["gesso"] - 0.05, T["gesso"] + 0.40, T["troca"], T["troca"] + 0.45),
         (T["pouco"] + 0.08, T["pouco"] + 0.5)]
    for c, P in _ciclos(T):
        g[-1] = g[-1] + (c, c + 0.18 * P)
        g.append((c + 0.50 * P, c + 0.74 * P))
    g[-1] = g[-1] + (T["depois"], T["depois"] + 0.45)
    return g


def estado_gesso(t, T):
    """-> (enrolado 0..1, saindo 0..1) do gesso da vez, ou None."""
    for on0, on1, off0, off1 in gessos(T):
        if on0 <= t < off1:
            return e_inout(prog(t, on0, on1)), e_inout(prog(t, off0, off1))
    return None


# ------------------------------------------------------------------ câmera
def camera(t, T):
    """-> (z, fx, fy, cx, cy): o ponto (fx, fy) da cena vai para (cx, cy) na tela, escala z."""
    z = lerp(0.93, 1.0, e_back(prog(t, T["nasce"] - 0.05, T["nasce"] + 0.45)))
    fx, fy, cx, cy = 600.0, 860.0, 600.0, 810.0             # a cena sobe 50 px: folga acima da legenda
    # "Quem corrige?": a câmera chega perto do pé; nos "gessos" volta e acompanha o giro
    z *= lerp(1.0, 1.07, e_inout(prog(t, T["quem"] - 0.1, T["quem"] + 0.9))) /         lerp(1.0, 1.07, e_inout(prog(t, T["gessos"] - 0.1, T["gessos"] + 0.9)))
    k = e_inout(prog(t, T["gessos"], T["depois"]))           # o pé gira para a esquerda: a câmera acompanha
    cx = lerp(cx, 650.0, k)
    k = e_inout(prog(t, T["acomp"], T["acomp"] + 0.9))       # acompanhamento: o pé recua inteiro
    z = lerp(z, 0.62, k); fx = lerp(fx, 560.0, k); fy = lerp(fy, 760.0, k)
    cx = lerp(cx, 560.0, k); cy = lerp(cy, 700.0, k)
    return z, fx, fy, cx, cy


def aplica(cv, cam):
    z, fx, fy, cx, cy = cam
    cv.translate(cx, cy); cv.scale(z, z); cv.translate(-fx, -fy)


def na_tela(cam, x, y):
    z, fx, fy, cx, cy = cam
    return cx + z * (x - fx), cy + z * (y - fy)


# ------------------------------------------------------------------ desenho: pele
def _curva(pts):
    p = skia.Path(); p.moveTo(*pts[0])
    for i in range(1, len(pts) - 1):
        mx, my = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
        p.quadTo(pts[i][0], pts[i][1], mx, my)
    p.lineTo(*pts[-1])
    return p


def desenha_pele(cv, t, T, k):
    perna = perna_path()
    pe = pe_contorno(k)
    uni = skia.Op(perna, pe, skia.PathOp.kUnion_PathOp)
    cv.drawPath(uni, paint("#000000", 70, blur=8))
    cv.drawPath(uni, paint(PELE))
    cv.save(); cv.clipPath(uni, skia.ClipOp.kIntersect, True)
    # volume da perna (claro no meio, escuro nas bordas), que some no tornozelo
    sh = skia.GradientShader.MakeLinear([skia.Point(PX - 120, 0), skia.Point(PX + 120, 0)],
                                        [C(PELE_ESC), C(PELE, 0), C(PELE_CL, 200), C(PELE, 0), C(PELE_ESC)],
                                        [0.0, 0.3, 0.5, 0.7, 1.0])
    cv.saveLayer(skia.Rect(PX - 200, Y_DISS0 - 300, PX + 200, PY + 100), None)
    cv.drawPath(perna, paint(PELE, 255, shader=sh))
    masc = skia.Paint(AntiAlias=True)
    masc.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 630), skia.Point(0, 790)],
                                                  [skia.ColorSetARGB(255, 0, 0, 0), skia.ColorSetARGB(0, 0, 0, 0)]))
    masc.setBlendMode(skia.BlendMode.kDstIn)
    cv.drawRect(skia.Rect(-500, 0, W + 500, 2000), masc)
    cv.restore()
    # volume do pé: dorso claro, sola mais escura; no pé torto a sola aparece (virado pra dentro)
    cv.drawPath(_curva(curva_pe(k, _DORSO_T, _DORSO_N)), paint(PELE_CL, 210, "stroke", 30, blur=12))
    sola = curva_pe(k, _SOLA_T, _SOLA_N)
    cv.drawPath(_curva(sola), paint(PELE_ESC, 200, "stroke", 26, blur=10))
    larg = lerp(46, 0, destorcao(k))                     # a sola some na DESTORÇÃO (primeiros passos)
    if larg > 1:
        cv.drawPath(_curva(sola), paint(SOLA, int(255 * clamp(larg / 12)), "stroke", larg, blur=2))
        pulso = math.sin(math.pi * prog(t, T["dentro"], T["dentro"] + 0.6))
        if pulso > 0:                                    # "pra dentro": a sola acende uma vez
            cv.drawPath(_curva(sola), paint(CORAL, int(160 * pulso), "stroke", larg + 10, blur=8))
    # o topo da perna escurece num tom quente antes de sumir (sem faixa cinza na capa)
    escurece = skia.GradientShader.MakeLinear(
        [skia.Point(0, Y_DISS0), skia.Point(0, Y_DISS1 + 70)],
        [C(PELE_FUNDO, 255), C(PELE_FUNDO, 216), C(PELE_FUNDO, 128), C(PELE_FUNDO, 40), C(PELE_FUNDO, 0)],
        [0.0, 0.25, 0.5, 0.75, 1.0])                     # curva suave: sem degrau onde o tom quente acaba
    cv.drawRect(skia.Rect(PX - 200, Y_DISS0 - 10, PX + 200, Y_DISS1 + 70), paint(PELE, 255, shader=escurece))
    cv.restore()
    # dobrinhas de bebê: tornozelo e panturrilha
    for y, w, a in ((744, 0.62, 110), (612, 0.42, 70)):
        hw = meia_largura(y) * w
        cv.drawArc(skia.Rect(PX - hw, y - 12, PX + hw, y + 12), 20, 140, False, paint(PELE_LINHA, a, "stroke", 3))
    pl = paint(PELE_LINHA, 230, "stroke", 3.2)
    cv.drawPath(uni, pl)


def dedos(cv, k, a=1.0):
    for x, y, r in reversed(dedos_tela(k)):
        cv.drawCircle(x + 1, y + 3, r, paint("#000000", int(40 * a), blur=4))
        cv.drawCircle(x, y, r, paint(PELE_CL, int(255 * a)))
        cv.drawCircle(x, y, r, paint(PELE_LINHA, int(230 * a), "stroke", 2.6))


# ------------------------------------------------------------------ gesso
A_DEDOS = 250.0                              # o gesso vai até a base dos dedos (os dedos ficam de fora)


def gesso_path(k, enr):
    """Contorno do gesso enrolado até `enr` (0..1): primeiro a perna, de cima até o tornozelo,
    depois o pé, do calcanhar até a base dos dedos. -> (todo, parte da perna, parte do pé, y_w, a_w)."""
    pl, pf = clamp(enr / 0.55), clamp((enr - 0.55) / 0.45)
    y_w = lerp(Y_DISS0 - 60, 860, pl)
    gp = perna_path(12.0, y_max=y_w)
    a_w, gf = None, None
    g = gp
    if pf > 0:
        a_w = lerp(-110, A_DEDOS, pf)
        gf = pe_path(k, 12.0, a_w)
        g = skia.Op(gp, gf, skia.PathOp.kUnion_PathOp)
    return g, gp, gf, y_w, a_w


def _faixas(cv, k, gp, gf):
    """Textura de atadura enrolada (faixas inclinadas: a espiral), na perna e no pé."""
    pt = paint(GESSO_B, 230, "stroke", 3.5)
    cv.save()
    so_perna = skia.Op(gp, gf, skia.PathOp.kDifference_PathOp) if gf is not None else gp
    cv.clipPath(so_perna, skia.ClipOp.kIntersect, True)
    for y in range(int(Y_DISS0 - 60), 900, 30):
        cv.drawLine(PX - 170, y - 16, PX + 170, y + 16, pt)
    cv.restore()
    if gf is not None:
        cv.save(); cv.clipPath(gf, skia.ClipOp.kIntersect, True); cv.concat(eixo(k))
        for a in range(-100, int(A_DEDOS) + 10, 27):
            cv.drawLine(a - 12, -160, a + 12, 160, pt)
        cv.restore()


def desenha_gesso(cv, k, enr, sai):
    if enr <= 0:
        return
    g, gp, gf, y_w, a_w = gesso_path(k, enr)
    b = g.computeTightBounds()
    sh = skia.GradientShader.MakeLinear([skia.Point(b.left(), 0), skia.Point(b.right(), 0)],
                                        [C(GESSO_B), C(GESSO), C("#FFFFFF"), C(GESSO), C(GESSO_B)],
                                        [0.0, 0.25, 0.5, 0.75, 1.0])
    metades = ((-1, skia.Rect(-2000, -2000, PX, 4000)), (1, skia.Rect(PX, -2000, 4000, 4000))) if sai > 0 \
        else ((0, None),)
    for lado, clip in metades:
        a = 1 - sai ** 2.2                                    # continua marfim enquanto desliza; some no fim
        if a <= 0:
            continue
        cv.save()
        if clip is not None:                                  # abre em duas metades e desliza para fora
            cv.translate(lado * 190 * e_out(sai), 30 * sai)
            cv.clipRect(clip)
        cv.saveLayerAlpha(None, int(255 * a))
        cv.drawPath(g, paint("#000000", 60, blur=12))
        cv.drawPath(g, paint(GESSO, 255, shader=sh))
        cv.save(); cv.clipPath(g, skia.ClipOp.kIntersect, True)
        _faixas(cv, k, gp, gf)
        if enr < 1:                                           # o rolo da atadura passando
            if a_w is None:
                cv.drawLine(PX - 200, y_w - 18, PX + 200, y_w + 14, paint(GESSO_L, 110, "stroke", 30, blur=8))
                cv.drawLine(PX - 200, y_w - 20, PX + 200, y_w + 12, paint("#FFFFFF", 255, "stroke", 16))
            else:
                cv.save(); cv.concat(eixo(k))
                cv.drawLine(a_w - 10, -170, a_w + 10, 170, paint(GESSO_L, 110, "stroke", 30, blur=8))
                cv.drawLine(a_w - 12, -170, a_w + 8, 170, paint("#FFFFFF", 255, "stroke", 16))
                cv.restore()
        cv.restore()
        cv.drawPath(g, paint(GESSO_L, 230, "stroke", 3))
        cv.restore()
        cv.restore()


# ------------------------------------------------------------------ setas
def ponta(cv, x, y, ang, tam, cor, a):
    p = skia.Path()
    p.moveTo(x + tam * math.cos(ang), y + tam * math.sin(ang))
    p.lineTo(x + tam * 0.75 * math.cos(ang + 2.45), y + tam * 0.75 * math.sin(ang + 2.45))
    p.lineTo(x + tam * 0.75 * math.cos(ang - 2.45), y + tam * 0.75 * math.sin(ang - 2.45))
    p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))


def seta_pts(cv, pts, cor, a, larg=8, tam=26, brilho=90):
    if a <= 0 or len(pts) < 2:
        return
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    cv.drawPath(p, paint(cor, int(brilho * a), "stroke", larg + 10, blur=7))
    cv.drawPath(p, paint(cor, int(255 * a), "stroke", larg))
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    ponta(cv, x1, y1, math.atan2(y1 - y0, x1 - x0), tam, cor, a)


def torcao(k, a0, a1, cresce, ac=176.0, ra=36.0, rb=120.0, n=30):
    """Seta de torção em volta da frente do pé (elipse ao redor do eixo do pé), em coordenadas locais."""
    bc = lerp(0, 52, destorcao(k))
    a1 = lerp(a0, a1, cresce)
    return [no_eixo(k, ac + ra * math.cos(math.radians(g)), bc + rb * math.sin(math.radians(g)))
            for g in [lerp(a0, a1, i / n) for i in range(n + 1)]]


def seta_baixo(cresce, n=20):
    """Seta curva coral rente à frente do pé, terminando abaixo dos dedos e apontando pra baixo."""
    p0, c, p1 = (PX - 214, PY + 110), (PX - 236, PY + 240), (PX - 188, PY + 336)
    return [((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * c[0] + u * u * p1[0],
             (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * c[1] + u * u * p1[1])
            for u in [cresce * i / n for i in range(n + 1)]]


def seta_torcao(cv, k, pts, cor, a, larg=7, tam=24):
    """A seta de torção: o trecho que passa por trás do pé fica apagado, o da frente cheio."""
    if a <= 0 or len(pts) < 2:
        return
    atras = skia.Path(); frente = skia.Path()
    n = len(pts)
    for i in range(n - 1):
        alvo = atras if i < n * 0.42 else frente
        alvo.moveTo(*pts[i]); alvo.lineTo(*pts[i + 1])
    cv.drawPath(atras, paint(cor, int(110 * a), "stroke", larg - 2))
    cv.drawPath(frente, paint(cor, int(90 * a), "stroke", larg + 10, blur=7))
    cv.drawPath(frente, paint(cor, int(255 * a), "stroke", larg))
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    ponta(cv, x1, y1, math.atan2(y1 - y0, x1 - x0), tam, cor, a)


# ------------------------------------------------------------------ peças de tela
def etiqueta(cv, s, x, y, xa, ya, cor, a, tam=40, esq=False):
    """Rótulo com fundo opaco; o fio termina na borda da caixa que fica do lado da seta (nunca risca o
    texto). `esq`: a caixa fica à esquerda da seta (o fio chega na borda direita)."""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    x += 24 * (1 - e_out(a)) * (-1 if esq else 1)
    cv.drawLine(xa, ya, x + (lw + 32 if esq else 0), y - tam * 0.4, paint(cor, int(210 * a), "stroke", 3))
    cv.drawCircle(xa, ya, 7, paint(cor, int(255 * a)))
    rr = skia.RRect.MakeRectXY(skia.Rect(x, y - tam * 1.1, x + lw + 32, y + tam * 0.32), 14, 14)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(232 * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 3))
    cv.drawString(s, x + 16, y, f, paint(cor, int(255 * a)))


def chip(cv, s, x, y, cor, a, tam=42, borda=None, glow=0.0, esc=1.0):
    """Pílula centrada em x; y = linha de base do texto."""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    cv.save(); cv.translate(x, y - tam * 0.35); cv.scale(esc, esc); cv.translate(-x, -(y - tam * 0.35))
    rr = skia.RRect.MakeRectXY(skia.Rect(x - lw / 2 - 26, y - tam * 1.08, x + lw / 2 + 26, y + tam * 0.38), 18, 18)
    if glow > 0:
        cv.drawRRect(rr, paint(borda or cor, int(150 * a * glow), "stroke", 22, blur=16))
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(228 * a)))
    cv.drawRRect(rr, paint(borda or cor, int(255 * a), "stroke", 3))
    cv.drawString(s, x - lw / 2, y, f, paint(cor, int(255 * a)))
    cv.restore()


def chip_janela(cv, s, t, t0, t1, x=540, y=1196, cor="#FFFFFF", borda=OURO, tam=42):
    """Chip da faixa de baixo: entra com um 'pop' na palavra, sai antes do próximo."""
    a = prog(t, t0, t0 + 0.15) * (1 - prog(t, t1, t1 + 0.18))
    chip(cv, s, x, y, cor, a, tam, borda, esc=lerp(0.8, 1.0, e_back(prog(t, t0, t0 + 0.35))))


def carimbo_opaco(cv, s, x, y, rot, t0, t, dur, tam=62, esc0=1.7):
    """Carimbo ouro torto (o mesmo gesto do 'DE PROPÓSITO'), com fundo opaco: legível sobre a pele."""
    k = t - t0
    if k < 0 or k > dur:
        return
    esc = lerp(esc0, 1.0, e_out(clamp(k / 0.16))); a = clamp(k / 0.08) * (1 - prog(k, dur - 0.35, dur))
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(esc, esc)
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 26, -tam, lw / 2 + 26, tam * 0.36), 12, 12)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(240 * a))); cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 7))
    cv.drawString(s, -lw / 2, 0, f, paint(OURO, int(255 * a)))
    cv.restore()


def cartao(cv, grande, sub, t, t0, t1):
    """Cartão de fase no canto de cima (estilo dos cartões do alongamento)."""
    a = prog(t, t0, t0 + 0.3) * (1 - prog(t, t1, t1 + 0.3))
    if a <= 0:
        return
    tam = min(92.0, 560 * 92 / larg_texto(grande, F_BLACK, 92))
    larg = max(larg_texto(grande, F_BLACK, tam), larg_texto(sub, F_SEMI, 36))
    dx = -36 * (1 - e_out(prog(t, t0, t0 + 0.4)))
    x0, y0 = 60 + dx, 220
    yb = y0 + 22 + tam * 0.78
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y0, x0 + larg + 56, yb + 70), 20, 20),
                 paint(FUNDO_CARTAO, int(205 * a)))
    texto(cv, grande, x0 + 26, yb, F_BLACK, tam, "#FFFFFF", int(255 * a), centro=False)
    texto(cv, sub, x0 + 30, yb + 48, F_SEMI, 36, AZUL, int(255 * a), centro=False)


CAL_X, CAL_Y = 200.0, 600.0                  # calendário (sem número) no espaço livre à esquerda do pé


def icone_calendario(cv, t, T):
    """'Primeiras semanas de vida': só o ícone, sem texto (a legenda já diz); vira 4 folhas e para."""
    a = prog(t, T["primeiras"] - 0.05, T["primeiras"] + 0.12) * (1 - prog(t, T["manip"] - 0.35, T["manip"] - 0.05))
    if a <= 0:
        return
    esc = 1.2 * lerp(0.6, 1.0, e_back(prog(t, T["primeiras"] - 0.05, T["primeiras"] + 0.3)))
    cx, cy = CAL_X + 48, CAL_Y + 46
    cv.save(); cv.translate(cx, cy); cv.scale(esc, esc); cv.translate(-cx, -cy)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(CAL_X - 4, CAL_Y + 2, CAL_X + 100, CAL_Y + 100), 14, 14),
                 paint("#000000", int(90 * a), blur=10))
    t_cal = T["primeiras"] + min(t - T["primeiras"], 0.795)          # 4 folhas (os 4 ticks) e para
    calendario(cv, CAL_X, CAL_Y, t_cal, T["primeiras"], a)
    cv.restore()


def rolo(cv, t, T):
    """Rolo de atadura esquemático (sem texto): entra rolando em 'gessos', solta um pedacinho de faixa
    em 'poucos' (aos poucos, em trancos curtos) e sobe pela perna para virar a faixa do 1º gesso."""
    t0 = T["gessos"] - 0.05
    a = prog(t, t0, t0 + 0.12) * (1 - prog(t, T["gesso"] - 0.12, T["gesso"] + 0.12))
    if a <= 0:
        return
    R = 50.0
    u = e_out(prog(t, t0, t0 + 0.7))
    x, y = lerp(-140, ROLO_X, u), ROLO_Y
    giro = (x - ROLO_X) / R                                       # rola sem escorregar
    fita = sum(e_out(prog(t, tt, tt + 0.13)) for tt in trancos(T))
    L = 34.0 * fita
    giro += L / R
    s = e_inout(prog(t, T["gesso"] - 0.5, T["gesso"] - 0.02))   # sobe até o alto da perna
    x, y = lerp(x, PX - 120, s), lerp(y, Y_DISS1 + 55, s)
    giro += 4.0 * s
    af = a * (1 - clamp(s * 2.5))
    cv.save()
    cv.drawOval(skia.Rect(x - R, y + R - 6, x + R + 24, y + R + 14), paint("#000000", int(70 * a * (1 - s)), blur=8))
    dx, dy = 18.0, -12.0                                          # profundidade do cilindro
    corpo = paint(GESSO_B, int(255 * a), "stroke", 2 * R); corpo.setStrokeCap(skia.Paint.kButt_Cap)
    cv.drawCircle(x + dx, y + dy, R, paint(GESSO_L, int(255 * a)))
    cv.drawLine(x + dx, y + dy, x, y, corpo)
    if af > 0 and L > 1:                                          # a faixa sai de cima do rolo, rumo ao pé
        fx = x + 22 + L
        p = skia.Path(); p.moveTo(x + 4, y - R + 7); p.quadTo(x + 22 + L * 0.55, y - R + 2, fx, y - R + 10 + 0.12 * L)
        cv.drawPath(p, paint("#000000", int(50 * af), "stroke", 22, blur=5))
        cv.drawPath(p, paint(GESSO_L, int(255 * af), "stroke", 20))
        cv.drawPath(p, paint(GESSO, int(255 * af), "stroke", 15))
    cv.drawCircle(x, y, R, paint(GESSO, int(255 * a)))
    cv.drawCircle(x, y, R, paint(GESSO_L, int(255 * a), "stroke", 3))
    esp = skia.Path()                                             # espiral da atadura enrolada
    n = 90
    for i in range(n + 1):
        f = i / n
        r = lerp(15, R - 5, f); g = giro + f * 2 * math.pi * 3.2
        q = (x + r * math.cos(g), y + r * math.sin(g))
        esp.moveTo(*q) if i == 0 else esp.lineTo(*q)
    cv.drawPath(esp, paint(GESSO_B, int(255 * a), "stroke", 3))
    cv.drawCircle(x, y, 11, paint(GESSO_L, int(255 * a)))
    cv.restore()


ROLO_X, ROLO_Y = 295.0, 985.0


def trancos(T):
    """'aos poucos': a faixa sai em três trancos curtos."""
    return [T["poucos"] + 0.06 + 0.2 * i for i in range(3)]


def linha_do_tempo(cv, t, T):
    """Linha do tempo sem datas: marcadores circulares neutros que acendem um a um."""
    a = prog(t, T["acomp"] + 0.2, T["acomp"] + 0.6) * (1 - prog(t, T["manda"] - 0.4, T["manda"] - 0.1))
    if a <= 0:
        return
    x0, x1, y = 150, 930, 1070
    cresce = e_inout(prog(t, T["acomp"] + 0.2, T["acomp"] + 0.9))
    cv.drawLine(x0, y, lerp(x0, x1, cresce), y, paint("#FFFFFF", int(110 * a), "stroke", 5))
    n = 5
    for i in range(n):
        x = lerp(x0 + 40, x1 - 40, i / (n - 1))
        if x > lerp(x0, x1, cresce) + 4:
            continue
        t_on = T["cresc"] + 0.05 + 0.28 * i
        on = e_out(prog(t, t_on, t_on + 0.3))
        cv.drawCircle(x, y, 17, paint(FUNDO_CARTAO, int(255 * a)))
        if on > 0:
            cv.drawCircle(x, y, 24, paint(OURO, int(80 * a * on), blur=10))
            cv.drawCircle(x, y, 13 * on, paint(OURO, int(235 * a)))
        cv.drawCircle(x, y, 17, paint(OURO if on > 0.5 else "#C8D6E4", int(255 * a * (0.6 + 0.4 * on)), "stroke", 4))


# ------------------------------------------------------------------ o mundo (dentro da câmera)
Y_ALVO = PY + 50                              # a linha-alvo passa pelo meio do pé alinhado


def linha_alvo(cv, t, T):
    a = 110 * e_out(prog(t, T["nasce"] + 0.1, T["nasce"] + 0.6))
    a = lerp(a, 215, prog(t, T["gessos"], T["gessos"] + 0.4))
    a *= 1 - prog(t, T["depois"] + 0.1, T["depois"] + 0.9)             # só se apaga: sem brilho
    if a <= 0:
        return
    cresce = e_out(prog(t, T["nasce"] + 0.1, T["nasce"] + 0.7))
    pt = paint(OURO, int(a), "stroke", 5)
    pt.setPathEffect(skia.DashPathEffect.Make([20, 13], t * 14))
    cv.drawLine(PX - 40, Y_ALVO, lerp(PX - 40, PX - 480, cresce), Y_ALVO, pt)


def rastro(cv, t, T, k):
    """Rastro de movimento enquanto o pé gira: some sozinho em < 0,5 s depois que ele para."""
    for t0, t1, k0, k1, com in passos(T):
        if com and t0 <= t <= t1 + 0.45:
            kl = k_em(t - 0.22, T)
            a = clamp(abs(k - kl) / 0.035) * (1 - prog(t, t1 + 0.1, t1 + 0.45))
            if a > 0:
                p = pe_contorno(kl)
                cv.save(); cv.clipPath(perna_path(), skia.ClipOp.kDifference, True)
                cv.drawPath(p, paint("#FFFFFF", int(70 * a), "stroke", 10, blur=6))
                cv.drawPath(p, paint("#FFFFFF", int(160 * a), "stroke", 3))
                cv.restore()


def manipulacao(cv, t, T, k):
    """Seta branca suave DESTORCENDO o pé (o sentido oposto ao 'pra dentro'), sem mão e sem força.
    Nada empurra a ponta do pé pra cima: no método o 'pra baixo' é corrigido por último."""
    a = prog(t, T["manip"], T["manip"] + 0.3) * (1 - prog(t, T["gesso"] - 0.3, T["gesso"]))
    if a <= 0:
        return
    cv.drawPath(pe_path(k), paint("#FFFFFF", int(70 * a), "stroke", 26, blur=18))
    cresce = e_out(prog(t, T["manip"] + 0.05, T["manip"] + 0.8))
    fluxo = 0.75 + 0.25 * math.sin((t - T["manip"]) * 5)
    seta_torcao(cv, k, torcao(k, 60, -200, cresce, rb=118), "#FFFFFF", a * 0.8 * fluxo, larg=7, tam=24)


def ortese(cv, t, T, k):
    a = prog(t, T["ortese"], T["ortese"] + 0.2) * (1 - prog(t, T["manda"] - 0.4, T["manda"] - 0.1))
    if a <= 0:
        return
    o = skia.Op(pe_path(k, 22.0), perna_path(22.0, y_min=PY - 150), skia.PathOp.kUnion_PathOp)
    pulso = math.sin(math.pi * prog(t, T["manter"], T["manter"] + 0.6))
    desenho = e_inout(prog(t, T["ortese"], T["ortese"] + 0.75))
    cv.drawPath(o, paint(OURO, int(24 * a)))
    if pulso > 0:
        cv.drawPath(o, paint(OURO, int(150 * a * pulso), "stroke", 26, blur=14))
    m = skia.PathMeasure(o, False)
    seg = skia.Path()
    m.getSegment(0, m.getLength() * desenho, seg, True)
    pt = paint(OURO, int(255 * a), "stroke", 6 + 3 * pulso)
    pt.setPathEffect(skia.DashPathEffect.Make([22, 14], 0))
    cv.drawPath(seg, pt)


def halo(cv, t, T, k):
    """Flexibilidade do bebê: um halo dourado macio pulsa UMA vez; o gesso não se deforma."""
    x = prog(t, T["flex"], T["flex"] + 0.9)
    if not 0 < x < 1:
        return
    p = math.sin(math.pi * x)
    cv.drawPath(pe_path(k, 12.0), paint(OURO, int(190 * p), "stroke", 36, blur=20))


def membro(cv, t, T, k):
    """Perna + pé + gesso numa camada; o topo se dissolve no fundo (sem retângulo por cima)."""
    cv.saveLayer(skia.Rect(-600, Y_DISS0 - 200, W + 600, 1600), None)
    desenha_pele(cv, t, T, k)
    rastro(cv, t, T, k)
    g = estado_gesso(t, T)
    if g:
        desenha_gesso(cv, k, g[0], g[1])
    dedos(cv, k)
    masc = skia.Paint(AntiAlias=True)
    masc.setShader(skia.GradientShader.MakeLinear([skia.Point(0, Y_DISS0), skia.Point(0, Y_DISS1)],
                                                  [skia.ColorSetARGB(0, 0, 0, 0), skia.ColorSetARGB(255, 0, 0, 0)]))
    masc.setBlendMode(skia.BlendMode.kDstIn)
    cv.drawRect(skia.Rect(-600, Y_DISS0 - 200, W + 600, 1600), masc)
    cv.restore()


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    cam = camera(t, T)
    k = k_em(t, T)
    fim = 1 - prog(t, T["manda"] - 0.4, T["manda"] - 0.1)              # a CTA fica limpa

    cv.saveLayerAlpha(None, int(255 * fim)) if fim < 1 else cv.save()
    aplica(cv, cam)
    linha_alvo(cv, t, T)
    membro(cv, t, T, k)
    halo(cv, t, T, k)
    manipulacao(cv, t, T, k)
    rolo(cv, t, T)
    ortese(cv, t, T, k)
    # setas do "pra baixo" e do "pra dentro" (coral); somem antes do "comum"
    sai = 1 - prog(t, T["comum"] + 0.15, T["comum"] + 0.55)
    a_b = prog(t, T["baixo"] - 0.05, T["baixo"] + 0.15) * sai
    a_d = prog(t, T["dentro"] - 0.05, T["dentro"] + 0.15) * sai
    pb = seta_baixo(e_out(prog(t, T["baixo"] - 0.05, T["baixo"] + 0.35)))
    pd = torcao(k, -150, 120, e_out(prog(t, T["dentro"] - 0.05, T["dentro"] + 0.45)))
    seta_pts(cv, pb, CORAL, a_b)
    seta_torcao(cv, k, pd, CORAL, a_d, larg=8, tam=26)
    cv.restore()
    veu = prog(t, T["acomp"], T["acomp"] + 0.9) * fim
    if veu > 0:
        cv.drawRect(skia.Rect(0, 0, W, 1920), paint(BG_OUT, int(70 * veu)))

    # rótulos das setas (tela), presos à ponta de cada seta
    xb, yb = na_tela(cam, *pb[-1]); xd, yd = na_tela(cam, *pd[-1])
    xm, ym = na_tela(cam, *pb[len(pb) // 2])
    etiqueta(cv, "PRA BAIXO", 64, 1010, xm - 14, ym, CORAL, a_b, esq=True)
    etiqueta(cv, "PRA DENTRO", 700, 1062, xd, yd, CORAL, a_d)      # abaixo e à direita da ponta da seta

    # é comum / não é culpa
    a = prog(t, T["comum"], T["comum"] + 0.25) * (1 - prog(t, T["quem"] - 0.1, T["quem"] + 0.2))
    brilho = math.sin(math.pi * prog(t, T["comum"], T["comum"] + 1.2))
    chip(cv, "É COMUM", 250, 700, OURO, a, 46, glow=brilho,
         esc=lerp(0.8, 1.0, e_back(prog(t, T["comum"], T["comum"] + 0.35))))
    carimbo_opaco(cv, "NÃO É CULPA", 290, 560, -6, T["culpa"], t, dur=T["gravidez"] + 0.6 - T["culpa"], tam=56)

    # cartões de fase (canto de cima) e calendário
    cartao(cv, "GESSOS", "aos poucos", t, T["gessos"], T["depois"] + 0.1)
    cartao(cv, "ÓRTESE", "pra manter", t, T["ortese"], T["acomp"] - 0.1)
    cartao(cv, "ACOMPANHAMENTO", "no crescimento", t, T["acomp"] + 0.2, T["manda"] - 0.45)
    icone_calendario(cv, t, T)
    a = prog(t, T["cedo"], T["cedo"] + 0.2) * (1 - prog(t, T["depois"] + 0.1, T["depois"] + 0.4))
    chip(cv, "COMEÇAR CEDO", 820, 300, OURO, a, 40, esc=lerp(0.8, 1.0, e_back(prog(t, T["cedo"], T["cedo"] + 0.35))))

    # faixa de ações (embaixo da cena, acima da legenda): uma de cada vez
    chip_janela(cv, "MANIPULAÇÃO SUAVE", t, T["manip"], T["gesso"] + 0.35)
    chip_janela(cv, "TROCA O GESSO", t, T["troca"], T["pouco"] + 0.2)
    chip_janela(cv, "GESSO APÓS GESSO", t, T["apos"] - 0.05, T["flex"] - 0.2)
    chip_janela(cv, "FLEXIBILIDADE DO BEBÊ", t, T["flex"], T["depois"] + 0.25)
    linha_do_tempo(cv, t, T)

    # capa (gancho no 1º quadro), selo, nome da condição
    t_sai = T["dentro"] + 0.4
    capa(cv, t, t_sai, ep["gancho"][0], ep["gancho"][1])
    selo_como_funciona(cv, prog(t, t_sai + 0.3, t_sai + 0.7) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    a = prog(t, t_sai + 0.45, t_sai + 0.85) * (1 - prog(t, T["gessos"] - 0.45, T["gessos"] - 0.15))
    if a > 0:
        texto(cv, "PÉ TORTO CONGÊNITO", 540, 268, F_BLACK, 40, "#FFFFFF", int(255 * a), contorno=8)
    interface(cv, t, T, blocos, DESTAQUE)


# ------------------------------------------------------------------ som e prévias
def sons(T):
    ev = [(T["nasce"], "pop", 0.6), (T["nasce"] + 0.05, "whoosh", 0.3),
          (T["baixo"], "whoosh", 0.35), (T["baixo"] + 0.1, "pop", 0.5),
          (T["dentro"], "whoosh", 0.35), (T["dentro"] + 0.1, "pop", 0.5),
          (T["comum"], "shimmer", 0.3), (T["culpa"] - 0.02, "thump", 0.7),
          (T["gessos"], "pop", 0.55), (T["gessos"] + 0.02, "whoosh", 0.25)]   # cartão + rolo entrando
    ev += [(tt, "tick", 0.25) for tt in trancos(T)]                      # a faixa sai aos poucos
    ev += [(T["primeiras"] + 0.2 * i, "tick", 0.3) for i in range(4)]
    ev += [(T["manip"] + 0.1, "shimmer", 0.25), (T["gesso"] - 0.5, "whoosh", 0.2)]   # rolo subindo
    g = gessos(T)                                                       # atadura enrolando / gesso saindo
    ev += [(g[0][0], "whoosh", 0.28), (g[0][2], "whoosh", 0.3), (g[1][0], "whoosh", 0.22)]
    ev += [(on0, "whoosh", 0.18) for on0, _, _, _ in g[2:]]             # ciclos: só a entrada soa
    ev += [(g[-1][2], "whoosh", 0.2)]                                   # o último gesso sai (sem vitória)
    for t0, t1, k0, k1, _ in passos(T)[1:]:                              # clique suave a cada passo
        ev.append((t1, "click", 0.9))
    ev += [(T["cedo"], "pop", 0.45), (T["flex"] + 0.05, "shimmer", 0.4),
           (T["ortese"], "whoosh", 0.3), (T["ortese"] + 0.1, "pop", 0.4), (T["manter"] + 0.05, "ping", 0.5),
           (T["acomp"], "whoosh", 0.35)]
    ev += [(T["cresc"] + 0.05 + 0.28 * i, "tick", 0.4) for i in range(5)]
    ev += [(T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def tempos_previa(T):
    return (0.0, T["dentro"] + 0.5, T["culpa"] + 0.5, T["poucos"] + 0.7, T["primeiras"] + 0.6,
            T["manip"] + 0.9, T["gesso"] + 0.12, T["pouco"] - 0.15, T["flex"] + 0.45, T["manter"] + 0.25,
            T["cresc"] + 1.3, T["manda"] + 1.6)


render = fazer_render(quadro, ANCORAS, sons, tempos_previa, respiro_cta=1.8)
