# -*- coding: utf-8 -*-
"""COMO FUNCIONA — escoliose ("A COLUNA ENTORTA / E NÃO DÓI?").

Mesmo estilo das cenas aprovadas (fundo azul-petróleo, marfim, dourado, rótulos, carimbo,
brilhos, checklist, legenda karaokê, CTA com aviãozinho). O que o verificador exigiu está aqui:
  * A coluna é uma pilha ESQUEMÁTICA de 7 blocos marfim (sem costela, bacia ou corpo em volta) com
    um pontinho dourado só como marcador do giro; a curva é UMA só, em C, para um lado.
  * No giro, os pontinhos escorregam para DENTRO do C (lado côncavo) e, nas costas, o lado mais
    alto é o de FORA do C — coerência de desenho, sem rótulo afirmando anatomia.
  * "COSTUMA NÃO DOER" sai junto com "NO COMEÇO" (a partir do "começo" nunca aparece sem ele).
  * Mochila: ninguém aparece levando culpa; o carimbo é "NÃO HÁ PROVA".
  * Criança de DESENHO (contorno arredondado, pele lisa, camiseta regata clara e shorts azul nas
    três vistas), sem osso, nada translúcido, rosto sem detalhe. A troca perfil -> costas é por
    fusão, sem câmera 3D. Nas costas inclinadas o dorso é UM arco convexo de camiseta (sem vértice
    na linha média). Nenhuma coluna é desenhada dentro das costas: a rotação aparece num medalhão
    separado, de fundo azul.
  * A coluna "apagada" do carimbo é ESCURECIDA por filtro de cor, opaca (nada de osso translúcido).
  * A lupa só aumenta o próprio desenho; o calendário não tem número; as duas setinhas de
    "mais rápido" são forma (traço), não caractere.
A cena é PRESA ao roteiro pelas palavras-âncora (ANCORAS): mudar o roteiro sem elas quebra o
render de propósito (KeyError), em vez de sair vídeo dessincronizado.
"""
import math

import skia

from .cf_alongamento import (BG_IN, F_BLACK, OSSO_B, OSSO_C, OSSO_L, OURO, PELE, VERMELHO, H, W, brilhos,
                             clamp, e_back, e_in_back, e_inout, e_out, fundo, lerp, paint, prog, rotulo, texto)
from .cf_comum import capa, carimbo, fazer_render, interface, selo_como_funciona
from .cf_fratura_cola import calendario

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "escoliose": ("escoliose", 1, False), "doer": ("doer", 1, False), "comeco": ("começo", 1, False),
    "costas": ("costas", 1, False), "curva": ("curva", 1, False), "gira": ("gira", 1, False),
    "mochila": ("mochila", 1, False), "prova": ("prova", 1, False), "teste": ("teste", 1, False),
    "juntos": ("juntos", 1, False), "esticados": ("esticados", 1, False), "inclinado": ("inclinado", 1, False),
    "olhe": ("olhe", 1, False), "alto": ("alto", 1, False), "rotacao": ("rotação", 1, False),
    "aparecendo": ("aparecendo", 1, False), "sinal2": ("sinal", 2, False), "leve": ("leve", 1, False),
    "avaliacao": ("avaliação", 1, False), "ortopedista": ("ortopedista", 1, False),
    "estirao": ("estirão", 1, False), "rapido": ("rápido", 1, False), "manda": ("manda", 1, False),
}
DESTAQUE = {"escoliose", "doer", "começo", "costas", "curva", "gira", "mochila", "prova", "teste", "juntos",
            "esticados", "inclinado", "olhe", "alto", "rotação", "sinal", "diagnóstico", "avaliação",
            "ortopedista", "estirão", "rápido"}

PELE_CL, PELE_ESC, PELE_LINHA = "#F7CDB8", "#DA987E", "#B9765E"
SHORT, SHORT_CL, SHORT_ESC = "#4C86C6", "#6FA3DA", "#3A6FA8"
CAMISA, CAMISA_CL, CAMISA_ESC, CAMISA_LINHA = "#6FC7B1", "#9EE0CF", "#3F9A85", "#2C7464"
CABELO = "#4A3426"
MOCH, MOCH_CL, MOCH_ESC = "#2F6DB5", "#4F8BD0", "#1E4F86"
FUNDO_CARTAO = "#0B1824"
MARFIM = OSSO_C


# ------------------------------------------------------------------ utilidades (copiadas do cf_pe_virado)
def _c(h, a=255):
    h = h.lstrip("#")
    return skia.ColorSetARGB(int(a), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _alfa(a):
    p = skia.Paint()
    p.setAlphaf(clamp(a))
    return p


def ponta(cv, x, y, ang, tam, cor, a):
    """Cabeça de seta em (x, y) apontando para `ang` (radianos)."""
    p = skia.Path()
    p.moveTo(x + tam * math.cos(ang), y + tam * math.sin(ang))
    p.lineTo(x + tam * 0.75 * math.cos(ang + 2.45), y + tam * 0.75 * math.sin(ang + 2.45))
    p.lineTo(x + tam * 0.75 * math.cos(ang - 2.45), y + tam * 0.75 * math.sin(ang - 2.45))
    p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))


def seta_pts(cv, pts, cor, a, larg=7, tam=22):
    if a <= 0 or len(pts) < 2:
        return
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    cv.drawPath(p, paint(cor, int(90 * a), "stroke", larg + 8, blur=6))
    cv.drawPath(p, paint(cor, int(255 * a), "stroke", larg))
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    ponta(cv, x1, y1, math.atan2(y1 - y0, x1 - x0), tam, cor, a)


def seta_arco(cv, cx, cy, rx, ry, a0, a1, cor, a, larg=7, tam=22):
    n = 18
    pts = [(cx + rx * math.cos(math.radians(lerp(a0, a1, k / n))), cy + ry * math.sin(math.radians(lerp(a0, a1, k / n))))
           for k in range(n + 1)]
    seta_pts(cv, pts, cor, a, larg, tam)


def chip(cv, s, x, y, cor, a, tam=40, borda=None):
    """Rótulo solto centrado em x; y = linha de base do texto."""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    rr = skia.RRect.MakeRectXY(skia.Rect(x - lw / 2 - 24, y - tam * 1.05, x + lw / 2 + 24, y + tam * 0.34), 16, 16)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(220 * a)))
    cv.drawRRect(rr, paint(borda or cor, int(255 * a), "stroke", 3))
    cv.drawString(s, x - lw / 2, y, f, paint(cor, int(255 * a)))


def chip_esq(cv, s, x, y, cor, a, tam=40, borda=None, dx=0.0):
    """Igual ao chip, alinhado pela ESQUERDA da caixa (x)."""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    x += dx
    rr = skia.RRect.MakeRectXY(skia.Rect(x, y - tam * 1.05, x + lw + 40, y + tam * 0.34), 16, 16)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(220 * a)))
    cv.drawRRect(rr, paint(borda or cor, int(255 * a), "stroke", 3))
    cv.drawString(s, x + 20, y, f, paint(cor, int(255 * a)))


def tracejada(cv, x0, y0, x1, y1, cor, a, larg=4, traco=16, vao=11, prog_=1.0, contorno=False):
    if a <= 0:
        return
    L = math.hypot(x1 - x0, y1 - y0)
    if L < 1:
        return
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    fim = L * prog_
    for passada in ((0, 1) if contorno else (1,)):
        d = 0.0
        while d < fim:
            e = min(d + traco, fim)
            if passada == 0:                                   # contorno escuro: lê sobre a camiseta clara
                cv.drawLine(x0 + ux * d, y0 + uy * d, x0 + ux * e, y0 + uy * e,
                            paint(FUNDO_CARTAO, int(150 * a), "stroke", larg + 5))
            else:
                cv.drawLine(x0 + ux * d, y0 + uy * d, x0 + ux * e, y0 + uy * e, paint(cor, int(255 * a), "stroke", larg))
            d += traco + vao


def estrela_dor(cv, x, y, r, a):
    if a <= 0:
        return
    p = skia.Path(); n = 9
    for i in range(2 * n):
        ang = -math.pi / 2 + i * math.pi / n
        rr = (r if i % 4 == 0 else r * 0.84) if i % 2 == 0 else r * 0.46
        (p.moveTo if i == 0 else p.lineTo)(x + rr * math.cos(ang), y + rr * math.sin(ang))
    p.close()
    cv.drawPath(p, paint(VERMELHO, int(110 * a), blur=12))
    cv.drawPath(p, paint(VERMELHO, int(230 * a)))
    cv.drawPath(p, paint("#FFD3D4", int(180 * a), "stroke", 2.5))


def _pele(cv, pth, x0, x1, a, linha=3.2):
    sh = skia.GradientShader.MakeLinear([skia.Point(x0, 0), skia.Point(x1, 0)],
                                        [_c(PELE_ESC), _c(PELE), _c(PELE_CL), _c(PELE), _c(PELE_ESC)],
                                        [0.0, 0.22, 0.5, 0.78, 1.0])
    cv.drawPath(pth, paint(PELE, int(255 * a), shader=sh))
    cv.drawPath(pth, paint(PELE_LINHA, int(230 * a), "stroke", linha))


def _camisa(cv, pth, x0, x1, a=1.0, linha=3.0):
    """Camiseta regata clara (a mesma nas três vistas: é ela que liga perfil, costas e de pé)."""
    sh = skia.GradientShader.MakeLinear([skia.Point(x0, 0), skia.Point(x1, 0)],
                                        [_c(CAMISA_ESC), _c(CAMISA), _c(CAMISA_CL), _c(CAMISA), _c(CAMISA_ESC)],
                                        [0.0, 0.24, 0.5, 0.76, 1.0])
    cv.drawPath(pth, paint(CAMISA, int(255 * a), shader=sh))
    cv.drawPath(pth, paint(CAMISA_LINHA, int(230 * a), "stroke", linha))


def manga(cv, x0, y0, x1, y1, larg, frac=0.3, a=1.0):
    """Manga curta da camiseta: cobre o começo do braço (de (x0, y0) em direção a (x1, y1))."""
    ang = math.degrees(math.atan2(y1 - y0, x1 - x0)) - 90
    L = math.hypot(x1 - x0, y1 - y0) * frac
    cv.save(); cv.translate(x0, y0); cv.rotate(ang)
    w0, w1 = larg * 0.40, larg * 0.54                          # um pouco mais larga na barra (manga solta)
    p = skia.Path()
    p.moveTo(-w0, 0); p.cubicTo(-w0, -larg * 0.55, w0, -larg * 0.55, w0, 0)
    p.lineTo(w1, L - 7); p.quadTo(w1, L, w1 - 7, L); p.lineTo(-w1 + 7, L); p.quadTo(-w1, L, -w1, L - 7)
    p.close()
    _camisa(cv, p, -w1 - 2, w1 + 2, a, 2.6)
    cv.drawLine(-w1 + 7, L - 8, w1 - 7, L - 8, paint(CAMISA_ESC, int(150 * a), "stroke", 3))
    cv.restore()


def capsula(cv, x0, y0, x1, y1, larg, a, mao=0.0):
    """Braço de desenho: tubo arredondado de (x0, y0) a (x1, y1), com mão redonda na ponta."""
    ang = math.degrees(math.atan2(y1 - y0, x1 - x0)) - 90
    L = math.hypot(x1 - x0, y1 - y0)
    cv.save(); cv.translate(x0, y0); cv.rotate(ang)
    p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect(-larg / 2, -larg / 2, larg / 2, L), larg / 2, larg / 2))
    if mao:
        m = skia.Path(); m.addOval(skia.Rect(-mao, L - mao * 1.3, mao, L + mao * 0.7))
        p = skia.Op(p, m, skia.PathOp.kUnion_PathOp) or p
    _pele(cv, p, -larg / 2 - 4, larg / 2 + 4, a, 2.6)
    cv.restore()


# ------------------------------------------------------------------ coluna esquemática (vista de trás)
NB = 7
BW, BH, BV = 176, 76, 13              # bloco: largura, altura, fresta
BD = 0.72 * BW                         # profundidade (só para o giro)
COL_X, COL_Y0 = 540, 400               # centro da pilha / topo do 1º bloco (mundo A)
PASSO = BH + BV
COL_CY = COL_Y0 + (NB * BH + (NB - 1) * BV) / 2
A_CURVA, ROT_MAX = 92.0, 30.0


def by(i):
    return COL_Y0 + i * PASSO + BH / 2


def estado_coluna(t, T, amp=A_CURVA, rotmax=ROT_MAX):
    """[(dx, inclinação, giro)] de cada bloco. Curva em C para a DIREITA da tela (vista de trás);
    o giro leva o pontinho (face de trás) para a ESQUERDA = para dentro do C."""
    out = []
    for i in range(NB):
        u = math.pi * (i + 0.5) / NB
        c = e_inout(prog(t, T["curva"] + 0.07 * i, T["curva"] + 0.07 * i + 0.5))
        dx = amp * math.sin(u) * c
        incl = -0.7 * math.degrees(math.atan(amp * c * math.pi / (NB * PASSO) * math.cos(u)))
        g = e_inout(prog(t, T["gira"] + 0.05 * i, T["gira"] + 0.05 * i + 0.55))
        out.append((dx, incl, rotmax * math.sin(u) * g))
    return out


def bloco(cv, x, y, incl, giro, a):
    cv.save(); cv.translate(x, y); cv.rotate(incl)
    r = math.radians(giro)
    xl = -(BW / 2) * math.cos(r) - (BD / 2) * math.sin(r)
    xr = (BW / 2) * math.cos(r) - (BD / 2) * math.sin(r)
    xs = (BW / 2) * math.cos(r) + (BD / 2) * math.sin(r)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(xl + 4, -BH / 2 + 6, max(xr, xs) + 4, BH / 2 + 6), 16, 16),
                 paint("#000000", int(70 * a), blur=10))
    if xs - xr > 0.8:                                          # face lateral que aparece com o giro
        lat = skia.RRect.MakeRectXY(skia.Rect(xr - 14, -BH / 2 + 2, xs, BH / 2 - 2), 14, 14)
        sh = skia.GradientShader.MakeLinear([skia.Point(xr, 0), skia.Point(xs, 0)], [_c(OSSO_B), _c("#B49C78")])
        cv.drawRRect(lat, paint(OSSO_B, int(255 * a), shader=sh))
        cv.drawRRect(lat, paint(OSSO_L, int(150 * a), "stroke", 2.5))
    face = skia.RRect.MakeRectXY(skia.Rect(xl, -BH / 2, xr, BH / 2), 16, 16)
    sh = skia.GradientShader.MakeLinear([skia.Point(xl, 0), skia.Point(xr, 0)],
                                        [_c(OSSO_B), _c(OSSO_C), _c(OSSO_C), _c(OSSO_B)], [0.0, 0.4, 0.6, 1.0])
    cv.drawRRect(face, paint(OSSO_C, int(255 * a), shader=sh))
    cv.drawRRect(face, paint(OSSO_L, int(150 * a), "stroke", 2.5))
    px = (xl + xr) / 2                                         # marcador do giro (não é anatomia)
    cv.drawCircle(px, 0, 15, paint(OURO, int(110 * a), blur=7))
    cv.drawCircle(px, 0, 9, paint(OURO, int(255 * a)))
    cv.drawCircle(px, 0, 9, paint("#8A6512", int(200 * a), "stroke", 2))
    cv.restore()


def coluna(cv, t, T, a, amp=A_CURVA, rotmax=ROT_MAX, saida=0.0, seta_a=0.0, giro_seta=None, linha_a=1.0):
    """A pilha. `saida` 0..1+: os blocos encolhem e caem um a um, OPACOS (nada fica translúcido)."""
    if a <= 0:
        return
    est = estado_coluna(t, T, amp, rotmax)
    tracejada(cv, COL_X, COL_Y0 - 12, COL_X, COL_Y0 + NB * PASSO + 18, OURO, 0.75 * a * linha_a, larg=4)
    dx3 = est[3][0]; cy3 = by(3)
    if seta_a > 0:                                             # metade de trás da seta que abraça a pilha
        cv.drawArc(skia.Rect(COL_X + dx3 - 128, cy3 - 30, COL_X + dx3 + 128, cy3 + 30), 200, 140, False,
                   paint("#9C7A2A", int(200 * seta_a * a), "stroke", 6))
    for i, (dx, incl, giro) in enumerate(est):
        k = prog(saida, i * 0.05, i * 0.05 + 0.65) if saida > 0 else 0.0
        if k >= 1:
            continue
        cv.save()
        if k > 0:
            e = e_in_back(k)
            sc = 1 - e
            if sc < 0.02:
                cv.restore()
                continue
            cv.translate(COL_X + dx, by(i) + 120 * e); cv.scale(sc, sc); cv.translate(-(COL_X + dx), -by(i))
        bloco(cv, COL_X + dx, by(i), incl, giro, a)
        cv.restore()
    if seta_a > 0:
        g0 = 18 if giro_seta is None else giro_seta
        seta_arco(cv, COL_X + dx3, cy3, 128, 30, g0, g0 + 132 * min(1.0, seta_a * 1.4), OURO, seta_a * a, larg=7, tam=22)


# ------------------------------------------------------------------ peças da primeira parte
def olho(cv, x, y, esc, a, abre=1.0):
    """Olho estilizado: amêndoa dourada com íris redonda (o sinal é visual)."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    L, hh = 82, 46 * max(0.06, abre)
    p = skia.Path(); p.moveTo(-L, 0)
    p.cubicTo(-L * 0.45, -hh * 1.3, L * 0.45, -hh * 1.3, L, 0)
    p.cubicTo(L * 0.45, hh * 1.3, -L * 0.45, hh * 1.3, -L, 0); p.close()
    cv.drawPath(p, paint(OURO, int(90 * a), blur=16))
    cv.drawPath(p, paint("#FFF6DD", int(255 * a)))
    cv.save(); cv.clipPath(p, skia.ClipOp.kIntersect, True)
    cv.drawCircle(0, 0, 31, paint(OURO, int(255 * a)))
    cv.drawCircle(0, 0, 31, paint("#9C7A2A", int(255 * a), "stroke", 4))
    cv.drawCircle(0, 0, 13, paint("#1B2430", int(255 * a)))
    cv.drawCircle(-9, -10, 6, paint("#FFFFFF", int(230 * a)))
    cv.restore()
    cv.drawPath(p, paint(OURO, int(255 * a), "stroke", 6))
    cv.restore()


def piscada(t, t0):
    """1 = aberto; fecha e abre rápido em t0."""
    k = t - t0
    if 0 <= k < 0.22:
        return abs(1 - 2 * k / 0.22)
    return 1.0


def mochila(cv, x, y, a, inc=0.0):
    """Mochila escolar de formas simples; (x, y) = meio da base."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y)
    cv.drawOval(skia.Rect(-112, -12, 112, 14), paint("#000000", int(80 * a), blur=8))
    cv.rotate(inc)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-34, -270, 34, -214), 26, 26), paint(MOCH_ESC, int(255 * a), "stroke", 12))
    for s in (-1, 1):                                          # as duas alças aparecendo dos lados
        q = skia.Path(); q.moveTo(s * 58, -232); q.cubicTo(s * 112, -190, s * 110, -90, s * 82, -26)
        cv.drawPath(q, paint(MOCH_ESC, int(255 * a), "stroke", 18))
    corpo = skia.RRect.MakeRectXY(skia.Rect(-96, -240, 96, 0), 48, 48)
    sh = skia.GradientShader.MakeLinear([skia.Point(-96, 0), skia.Point(96, 0)],
                                        [_c(MOCH_ESC), _c(MOCH), _c(MOCH_CL), _c(MOCH), _c(MOCH_ESC)],
                                        [0.0, 0.25, 0.5, 0.75, 1.0])
    cv.drawRRect(corpo, paint(MOCH, int(255 * a), shader=sh))
    cv.drawRRect(corpo, paint(MOCH_ESC, int(255 * a), "stroke", 3))
    cv.drawArc(skia.Rect(-80, -232, 80, -150), 200, 140, False, paint(MOCH_ESC, int(200 * a), "stroke", 4))
    bolso = skia.RRect.MakeRectXY(skia.Rect(-66, -118, 66, -18), 26, 26)
    cv.drawRRect(bolso, paint(MOCH_CL, int(255 * a)))
    cv.drawRRect(bolso, paint(MOCH_ESC, int(255 * a), "stroke", 3))
    cv.drawLine(-50, -98, 50, -98, paint(MOCH_ESC, int(255 * a), "stroke", 4))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(26, -102, 36, -76), 4, 4), paint(OURO, int(255 * a)))
    cv.restore()


# ------------------------------------------------------------------ criança de desenho (sem osso)
PISO = 1060                            # chão das vistas de costas
HX, HY = 600, 855                      # quadril no desenho de perfil (coordenadas de projeto)
L_PERNA = 192
PERF_X, PERF_PISO, PERF_K = 560, 1128, 1.1   # onde o perfil fica na tela (mais baixo: o checklist usa o alto)
OMBRO = 168                            # do quadril ao ombro, no perfil (pré-adolescente: tronco comprido)


def _shorts(cv, rr, a=1.0):
    cv.drawRRect(rr, paint(SHORT, int(255 * a)))


def perna_perfil(cv, ang, a, longe=False):
    """Perna de perfil (olhando para a direita), presa no quadril; o pé fica sempre plano no chão.
    A barra do shorts vem junto, no mesmo referencial da coxa."""
    cv.save(); cv.rotate(ang)
    p = skia.Path()
    p.moveTo(-34, -8)
    p.cubicTo(-37, 40, -26, 80, -23, 100)
    p.cubicTo(-22, 120, -31, 148, -20, L_PERNA)
    p.lineTo(15, L_PERNA)
    p.cubicTo(18, 150, 20, 118, 22, 100)
    p.cubicTo(25, 80, 34, 40, 33, -8)
    p.close()
    _pele(cv, p, -38, 36, a)
    if longe:                                                  # perna de trás um tom mais escura
        cv.drawPath(p, paint("#5A3A2E", int(60 * a)))
    cv.drawArc(skia.Rect(8, 88, 26, 112), -60, 120, False, paint(PELE_LINHA, int(140 * a), "stroke", 3))   # joelho
    _shorts(cv, skia.RRect.MakeRectXY(skia.Rect(-39, -14, 37, 62), 16, 16), a)
    cv.drawLine(-34, 56, 32, 56, paint(SHORT_ESC, int(200 * a), "stroke", 3))
    cv.translate(0, L_PERNA); cv.rotate(-ang)
    f = skia.Path()
    f.moveTo(-20, -10); f.cubicTo(-26, 4, -20, 12, -8, 12); f.lineTo(48, 12)
    f.cubicTo(62, 12, 62, -2, 50, -6); f.cubicTo(32, -10, 16, -14, 15, -22); f.lineTo(-19, -22); f.close()
    _pele(cv, f, -26, 62, a)
    if longe:
        cv.drawPath(f, paint("#5A3A2E", int(60 * a)))
    cv.restore()


def crianca_perfil(cv, t, T, a):
    """De perfil, em pé; pés se juntam no 'juntos'; o tronco inclina à frente no 'inclinado' e os
    braços soltos pendem em direção aos pés."""
    if a <= 0:
        return
    j = e_inout(prog(t, T["juntos"] - 0.05, T["juntos"] + 0.45))
    ang_tras, ang_frente = lerp(11, 0, j), lerp(-9, 0, j)
    fi = 84 * e_inout(prog(t, T["inclinado"] - 0.05, T["inclinado"] + 1.05))
    flex = 32 * e_inout(prog(t, T["inclinado"] + 0.1, T["inclinado"] + 1.15))
    cv.saveLayer(None, _alfa(a)) if a < 1 else cv.save()
    cv.translate(PERF_X, PERF_PISO); cv.scale(PERF_K, PERF_K); cv.translate(-HX, -PISO)
    cv.drawOval(skia.Rect(HX - 100, PISO - 10, HX + 150, PISO + 16), paint("#000000", 80, blur=10))
    cv.save(); cv.translate(HX - 6, HY); perna_perfil(cv, ang_tras, 1.0, longe=True); cv.restore()
    cv.save(); cv.translate(HX + 2, HY); perna_perfil(cv, ang_frente, 1.0); cv.restore()
    cv.drawCircle(HX - 2, HY - 4, 40, paint(SHORT))                 # quadril (une coxa e tronco no shorts)
    cv.save(); cv.translate(HX, HY); cv.rotate(fi)
    tr = skia.Path()                                           # tronco mais comprido (pré-adolescente)
    tr.moveTo(-40, 6)
    tr.cubicTo(-46, -44, -39, -124, -35, -160)
    tr.cubicTo(-33, -180, -13, -190, 6, -188)
    tr.cubicTo(26, -186, 38, -174, 38, -152)
    tr.cubicTo(42, -108, 34, -58, 36, -22)
    tr.cubicTo(37, 0, 32, 8, 28, 10)
    tr.close()
    pesc = skia.Path(); pesc.addRRect(skia.RRect.MakeRectXY(skia.Rect(-10, -210, 18, -176), 12, 12))
    _pele(cv, pesc, -12, 20, 1.0)
    _camisa(cv, tr, -46, 42)
    _shorts(cv, skia.RRect.MakeRectXY(skia.Rect(-45, -54, 41, 18), 20, 20))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-45, -54, 41, -36), 12, 12), paint(SHORT_CL))
    # cabeça menor (o pescoço dobra ao inclinar); cabelo na nuca e no alto, rosto sem detalhe
    cv.save(); cv.translate(4, -196); cv.rotate(flex)
    cx, cy = 8, -38
    cv.drawCircle(cx + 3, cy + 6, 44, paint("#000000", 50, blur=8))
    cab = skia.Path(); cab.addCircle(cx, cy, 42)
    _pele(cv, cab, cx - 44, cx + 44, 1.0)
    cv.save(); cv.clipPath(cab, skia.ClipOp.kIntersect, True)
    cv.drawCircle(cx - 19, cy - 17, 44, paint(CABELO))
    cv.drawCircle(cx + 12, cy - 34, 19, paint(CABELO))
    cv.restore()
    cv.restore()
    cv.restore()
    # braço: sempre pende para o chão ("braços soltos")
    r = math.radians(fi)
    ox, oy = HX + OMBRO * math.sin(r), HY - OMBRO * math.cos(r)
    caida = lerp(7, 3, fi / 84)
    bx, by_ = ox + 190 * math.sin(math.radians(caida)), oy + 190 * math.cos(math.radians(caida))
    capsula(cv, ox, oy, bx, by_, 27, 1.0, mao=15)
    manga(cv, ox, oy, bx, by_, 42, frac=0.3)
    cv.restore()


# vista de TRÁS, inclinada (teste das costas): o dorso, de camiseta, visto ao comprido
# (encurtado): faixa larga nos ombros, braços pendendo dos cantos, estreitando até a cintura,
# que some atrás do shorts. O alto é UM arco convexo (sem vértice na linha média).
OMB_E, OMB_D, OMB_Y, TOPO_Y = 404, 676, 742, 702   # cantos dos ombros e o alto do arco
CINTURA_E, CINTURA_D, CINTURA_Y = 446, 634, 842
BUMP_X, BUMP_S, BUMP_H = 598, 70, 34    # o lado de FORA do C (direita da tela) sobe no 'alto'
X_ESQ, X_DIR = 474, 606                 # pontos simétricos onde as tracejadas medem cada lado


def topo_costas(x, k):
    u = (x - 540) / ((OMB_D - OMB_E) / 2)
    return OMB_Y - (OMB_Y - TOPO_Y) * (1 - u * u) - BUMP_H * k * math.exp(-((x - BUMP_X) / BUMP_S) ** 2)


PICO_D = (BUMP_X, topo_costas(BUMP_X, 1.0))   # o alto do lado de fora do C, já subido


def path_costas(k):
    p = skia.Path()
    n = 64
    for i in range(n + 1):
        x = lerp(OMB_E, OMB_D, i / n)
        (p.moveTo if i == 0 else p.lineTo)(x, topo_costas(x, k))
    yd = topo_costas(OMB_D, k)
    p.cubicTo(OMB_D + 14, yd + 5, OMB_D + 20, yd + 30, OMB_D + 12, yd + 50)   # ombro arredondado (direita)
    p.cubicTo(OMB_D + 2, 818, CINTURA_D + 20, CINTURA_Y, CINTURA_D, CINTURA_Y)
    p.lineTo(CINTURA_E, CINTURA_Y)
    ye = topo_costas(OMB_E, k)
    p.cubicTo(CINTURA_E - 20, CINTURA_Y, OMB_E - 2, 818, OMB_E - 12, ye + 50)
    p.cubicTo(OMB_E - 20, ye + 30, OMB_E - 14, ye + 5, OMB_E, ye)
    p.close()
    return p


def costas_inclinada(cv, t, T, a, alto):
    """Criança inclinada vista por trás: pés juntos, braços soltos pendendo dos ombros, o dorso de
    camiseta visto ao comprido; `alto` 0..1 = o lado de FORA do C (direita) sobe."""
    if a <= 0:
        return
    cv.saveLayer(None, _alfa(a)) if a < 1 else cv.save()
    cv.drawOval(skia.Rect(400, PISO - 12, 680, PISO + 16), paint("#000000", 80, blur=10))
    for x0, x1 in ((OMB_E - 2, 440), (OMB_D + 2, 640)):       # braços soltos, pendendo em direção aos pés
        capsula(cv, x0, OMB_Y + 26, x1, 1004, 28, 1.0, mao=15)
        p = skia.Path(); p.moveTo(x0, OMB_Y + 26); p.lineTo(x1, 996)
        cv.drawPath(p, paint("#5A3A2E", 40, "stroke", 28))
        manga(cv, x0, OMB_Y + 26, x1, 1004, 44, frac=0.26)
    for xc in (510, 570):                                      # pernas, pés juntos
        p = skia.Path()
        p.moveTo(xc - 33, 846)
        p.cubicTo(xc - 36, 900, xc - 25, 950, xc - 23, 968)
        p.cubicTo(xc - 21, 992, xc - 19, 1020, xc - 18, 1040)
        p.lineTo(xc + 18, 1040)
        p.cubicTo(xc + 19, 1020, xc + 21, 992, xc + 23, 968)
        p.cubicTo(xc + 25, 950, xc + 36, 900, xc + 33, 846)
        p.close()
        _pele(cv, p, xc - 38, xc + 38, 1.0)
        cal = skia.Path(); cal.addOval(skia.Rect(xc - 24, 1026, xc + 24, 1064))       # calcanhar
        _pele(cv, cal, xc - 26, xc + 26, 1.0)
        cv.drawArc(skia.Rect(xc - 14, 955, xc + 14, 975), 200, 140, False, paint(PELE_LINHA, 140, "stroke", 3))
    col = path_costas(alto)
    cv.drawPath(col, paint("#000000", 80, blur=14))
    sh_v = skia.GradientShader.MakeLinear([skia.Point(0, TOPO_Y - 30), skia.Point(0, CINTURA_Y)],
                                          [_c(CAMISA_CL), _c(CAMISA), _c(CAMISA_ESC)], [0.0, 0.45, 1.0])
    cv.drawPath(col, paint(CAMISA, 255, shader=sh_v))          # mais claro no alto (a superfície vista ao comprido)
    sh_h = skia.GradientShader.MakeLinear([skia.Point(OMB_E - 12, 0), skia.Point(OMB_D + 12, 0)],
                                          [_c("#4A5C72", 110), _c("#4A5C72", 0), _c("#4A5C72", 0), _c("#4A5C72", 110)],
                                          [0.0, 0.22, 0.78, 1.0])
    cv.drawPath(col, paint("#000000", 255, shader=sh_h))       # volume: laterais mais escuras
    if alto > 0:                                               # o lado que subiu pega mais luz
        cv.save(); cv.clipPath(col, skia.ClipOp.kIntersect, True)
        cv.drawOval(skia.Rect(PICO_D[0] - 70, PICO_D[1] + 4, PICO_D[0] + 62, PICO_D[1] + 46),
                    paint("#FFFFFF", int(150 * alto), blur=14))
        cv.restore()
    cv.drawPath(col, paint(CAMISA_LINHA, 235, "stroke", 3.2))
    sh = skia.Path()                                           # shorts (o mais perto de quem olha)
    sh.moveTo(452, 822); sh.lineTo(628, 822)
    sh.cubicTo(644, 846, 650, 884, 638, 910)
    sh.cubicTo(614, 924, 570, 922, 548, 910); sh.lineTo(540, 902); sh.lineTo(532, 910)
    sh.cubicTo(510, 922, 466, 924, 442, 910)
    sh.cubicTo(430, 884, 436, 846, 452, 822); sh.close()
    cv.drawPath(sh, paint("#000000", 70, blur=10))
    cv.drawPath(sh, paint(SHORT))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(448, 818, 632, 842), 12, 12), paint(SHORT_CL))
    cv.drawLine(540, 852, 540, 890, paint(SHORT_ESC, 255, "stroke", 3))
    cv.restore()


def costas_em_pe(cv, a, esc):
    """De pé, vista de costas (camiseta, shorts); `esc` = escala a partir do chão."""
    if a <= 0:
        return
    cv.saveLayer(None, _alfa(a)) if a < 1 else cv.save()
    cv.translate(540, PISO); cv.scale(esc, esc); cv.translate(-540, -PISO)
    cv.drawOval(skia.Rect(430, PISO - 12, 650, PISO + 16), paint("#000000", 80, blur=10))
    for x0, x1 in ((448, 430), (632, 650)):                    # braços soltos ao lado do corpo
        capsula(cv, x0, 698, x1, 892, 29, 1.0, mao=15)
        manga(cv, x0, 698, x1, 892, 44, frac=0.3)
    for xc in (512, 568):
        p = skia.Path()
        p.moveTo(xc - 33, 858)
        p.cubicTo(xc - 35, 900, xc - 25, 940, xc - 23, 958)
        p.cubicTo(xc - 21, 985, xc - 19, 1020, xc - 18, 1040)
        p.lineTo(xc + 18, 1040)
        p.cubicTo(xc + 19, 1020, xc + 21, 985, xc + 23, 958)
        p.cubicTo(xc + 25, 940, xc + 35, 900, xc + 33, 858)
        p.close()
        _pele(cv, p, xc - 38, xc + 38, 1.0)
        cal = skia.Path(); cal.addOval(skia.Rect(xc - 24, 1026, xc + 24, 1064))
        _pele(cv, cal, xc - 26, xc + 26, 1.0)
        cv.drawArc(skia.Rect(xc - 14, 948, xc + 14, 968), 200, 140, False, paint(PELE_LINHA, 140, "stroke", 3))
    pesc = skia.Path(); pesc.addRRect(skia.RRect.MakeRectXY(skia.Rect(523, 612, 557, 664), 12, 12))
    _pele(cv, pesc, 519, 561, 1.0)
    tr = skia.Path()                                           # tronco de pré-adolescente (ombros ~50 px acima)
    tr.moveTo(462, 830)
    tr.cubicTo(452, 784, 458, 726, 448, 696)
    tr.cubicTo(438, 668, 468, 654, 516, 652)
    tr.lineTo(564, 652)
    tr.cubicTo(612, 654, 642, 668, 632, 696)
    tr.cubicTo(622, 726, 628, 784, 618, 830)
    tr.close()
    _camisa(cv, tr, 438, 642)
    sh = skia.Path()
    sh.moveTo(454, 806); sh.lineTo(626, 806)
    sh.cubicTo(640, 830, 644, 868, 636, 896)
    sh.cubicTo(612, 908, 570, 906, 548, 894); sh.lineTo(540, 880); sh.lineTo(532, 894)
    sh.cubicTo(510, 906, 468, 908, 444, 896)
    sh.cubicTo(436, 868, 440, 830, 454, 806); sh.close()
    cv.drawPath(sh, paint("#000000", 60, blur=8))
    cv.drawPath(sh, paint(SHORT))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(450, 802, 630, 826), 12, 12), paint(SHORT_CL))
    cv.drawLine(540, 836, 540, 874, paint(SHORT_ESC, 255, "stroke", 3))
    for s in (-1, 1):                                          # orelhas
        orl = skia.Path(); orl.addOval(skia.Rect(540 + s * 38 - 8, 576, 540 + s * 38 + 8, 602))
        _pele(cv, orl, 540 + s * 38 - 9, 540 + s * 38 + 9, 1.0, 2.2)
    cab = skia.Path(); cab.addCircle(540, 584, 40)
    _pele(cv, cab, 498, 582, 1.0)
    cv.save(); cv.clipPath(cab, skia.ClipOp.kIntersect, True)  # nuca: o cabelo cobre quase tudo
    cv.drawRect(skia.Rect(496, 540, 584, 600), paint(CABELO, 255))
    cv.drawOval(skia.Rect(506, 576, 574, 616), paint(CABELO, 255))
    cv.restore()
    cv.restore()


# ------------------------------------------------------------------ medalhão (a rotação, separada do corpo)
MED_X, MED_Y, MED_R = 872, 390, 148
MED_ESC = 0.38
CHEV_X = 656                            # as duas setinhas de "mais rápido", à esquerda do medalhão


def medalhao(cv, t, T, a):
    if a <= 0:
        return
    abre = e_back(prog(t, T["rotacao"], T["rotacao"] + 0.45))
    if abre <= 0:
        return
    mais = e_inout(prog(t, T["rapido"], T["rapido"] + 0.9))
    pulso = 1 + 0.10 * math.sin(math.pi * prog(t, T["rapido"], T["rapido"] + 0.6))
    cv.save(); cv.translate(MED_X, MED_Y); cv.scale(abre * pulso, abre * pulso)
    cv.drawCircle(0, 0, MED_R + 10, paint(OURO, int(90 * a), blur=16))
    fundo_m = skia.GradientShader.MakeRadial(skia.Point(0, -20), MED_R * 1.2, [_c(BG_IN), _c("#12304A")])
    cv.drawCircle(0, 0, MED_R, paint(BG_IN, int(255 * a), shader=fundo_m))
    cv.save()
    clip = skia.Path(); clip.addCircle(0, 0, MED_R - 4)
    cv.clipPath(clip, skia.ClipOp.kIntersect, True)
    cv.scale(MED_ESC, MED_ESC); cv.translate(-COL_X - 36 - 24 * mais, -COL_CY)
    fase = ((t - T["rotacao"]) * 0.7) % 1.0
    coluna(cv, t, T, a, amp=A_CURVA + 60 * mais, rotmax=ROT_MAX + 14 * mais, seta_a=1.0,
           giro_seta=lerp(-10, 50, fase), linha_a=1.0)
    cv.restore()
    cv.drawCircle(0, 0, MED_R, paint(OURO, int(255 * a), "stroke", 8))
    cv.drawCircle(0, 0, MED_R - 9, paint("#FFF1C2", int(110 * a), "stroke", 2.5))
    cv.restore()


def chevrons(cv, x, y, t, t0, a):
    """Ícone de 'mais rápido': duas setinhas de traço (forma, não caractere)."""
    if a <= 0:
        return
    for k in range(2):
        des = 6 * math.sin((t - t0) * 9 - k * 0.8)
        xx = x + k * 30 + des
        p = skia.Path(); p.moveTo(xx - 12, y - 22); p.lineTo(xx + 10, y); p.lineTo(xx - 12, y + 22)
        cv.drawPath(p, paint(OURO, int(100 * a), "stroke", 14, blur=6))
        cv.drawPath(p, paint(OURO, int(255 * a), "stroke", 8))


def prancheta(cv, x, y, a):
    """Prancheta simples: marfim, prendedor dourado, três linhas em branco (sem texto)."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(4, 8, 92, 124), 12, 12), paint("#000000", int(80 * a), blur=8))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(0, 0, 88, 116), 12, 12), paint(MARFIM, int(255 * a)))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(0, 0, 88, 116), 12, 12), paint(OSSO_L, int(200 * a), "stroke", 2.5))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(24, -10, 64, 14), 7, 7), paint(OURO, int(255 * a)))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(24, -10, 64, 14), 7, 7), paint("#8A6512", int(255 * a), "stroke", 2))
    for i in range(3):
        cv.drawLine(16, 42 + i * 24, 72, 42 + i * 24, paint("#B9AE98", int(230 * a), "stroke", 5))
    cv.restore()


# ------------------------------------------------------------------ câmeras
def dy_capa(t, T):
    """Enquanto a capa está no topo, a coluna fica 60 px mais baixa; sobe quando a capa sai."""
    return 60 * (1 - e_inout(prog(t, T["comeco"] + 0.35, T["comeco"] + 0.95)))


def esc_cd(t, T):
    """Câmera do perfil/costas inclinadas: chega perto no 'olhe' e no 'alto' e FICA (sem recuo no estirão)."""
    s = lerp(1.0, 1.12, e_inout(prog(t, T["olhe"], T["olhe"] + 1.6)))
    return lerp(s, 1.3, e_inout(prog(t, T["alto"] - 0.1, T["alto"] + 0.6)))


def aplica_cd(cv, s):
    cv.translate(540, PISO); cv.scale(s, s); cv.translate(-540, -PISO)


def na_tela(x, y, s):
    """Ponto do desenho das costas -> tela, com a câmera `s` (ancorada no chão)."""
    return 540 + (x - 540) * s, PISO + (y - PISO) * s


def mundo_cd(cv, t, T):
    """Criança: perfil -> costas inclinada (fusão). A criança de pé do estirão é desenhada fora da
    câmera (quadro), com escala própria: ela só cresce."""
    a_perf = prog(t, T["teste"] - 0.05, T["teste"] + 0.25) * (1 - prog(t, T["olhe"] - 0.12, T["olhe"] + 0.18))
    if a_perf > 0:
        cv.save(); cv.translate(120 * (1 - e_out(prog(t, T["teste"] - 0.05, T["teste"] + 0.5))), 0)
        crianca_perfil(cv, t, T, a_perf)
        cv.restore()
    alto = e_inout(prog(t, T["alto"], T["alto"] + 0.5))
    a_inc = prog(t, T["olhe"] + 0.1, T["olhe"] + 0.4) * (1 - prog(t, T["estirao"] - 0.05, T["estirao"] + 0.15))
    costas_inclinada(cv, t, T, a_inc, alto)
    a_lin = prog(t, T["alto"] + 0.1, T["alto"] + 0.3) * (1 - prog(t, T["estirao"] - 0.3, T["estirao"]))
    if a_lin > 0:                                              # as duas alturas
        pr = e_out(prog(t, T["alto"] + 0.1, T["alto"] + 0.6))
        yl, yr = topo_costas(X_ESQ, alto) - 6, topo_costas(X_DIR, alto) - 6
        for y_, a_ in ((yl, a_lin), (yr, a_lin * clamp(alto * 3))):
            tracejada(cv, 540, y_, 540 - 190 * pr, y_, OURO, a_, larg=4, contorno=True)
            tracejada(cv, 540, y_, 540 + 190 * pr, y_, OURO, a_, larg=4, contorno=True)
        if alto > 0.3:                                         # setinha para cima no lado mais alto
            xa = 540 + 176
            cv.drawLine(xa, yl - 2, xa, yr + 12, paint(OURO, int(255 * a_lin), "stroke", 6))
            ponta(cv, xa, yr + 2, -math.pi / 2, 18, OURO, a_lin)


LUPA_X, LUPA_Y, LUPA_R = 604, 588, 118


def lupa(cv, t, T, s_cam):
    t0 = T["ortopedista"]
    if t < t0 - 0.05:
        return
    a = 1 - prog(t, T["estirao"] - 0.05, T["estirao"] + 0.2)
    if a <= 0:
        return
    k1 = e_inout(prog(t, t0 - 0.05, t0 + 0.35))
    x = lerp(-160, LUPA_X, k1) + 4 * math.sin(t * 1.7)
    y = lerp(700, LUPA_Y, k1) + 3 * math.cos(t * 1.3)
    r, m = LUPA_R, 1.4
    cv.saveLayer(None, _alfa(a))
    cv.save()
    clip = skia.Path(); clip.addCircle(x, y, r)
    cv.clipPath(clip, skia.ClipOp.kIntersect, True)
    fundo(cv, t)
    cv.translate(x, y); cv.scale(m, m); cv.translate(-x, -y)
    aplica_cd(cv, s_cam)
    mundo_cd(cv, t, T)
    cv.restore()
    cv.drawCircle(x, y, r, paint("#FFFFFF", 22))                # lente clara: só aumenta o desenho
    hx, hy = x + r * 0.71, y + r * 0.71
    cv.drawLine(hx + 4, hy + 4, hx + 84, hy + 84, paint("#000000", 80, "stroke", 30, blur=6))
    cv.drawLine(hx + 6, hy + 6, hx + 82, hy + 82, paint("#8A6512", 255, "stroke", 26))
    cv.drawLine(hx + 6, hy + 6, hx + 82, hy + 82, paint(OURO, 255, "stroke", 16))
    cv.drawCircle(x, y, r, paint("#000000", 80, "stroke", 20, blur=6))
    cv.drawCircle(x, y, r, paint(OURO, 255, "stroke", 13))
    cv.drawCircle(x, y, r - 8, paint("#FFF1C2", 120, "stroke", 2.5))
    cv.drawArc(skia.Rect(x - r * 0.72, y - r * 0.72, x + r * 0.72, y + r * 0.72), 200, 55, False,
               paint("#FFFFFF", 150, "stroke", 7))
    cv.restore()


# ------------------------------------------------------------------ checklist do teste
CK_X, CK_Y, CK_PASSO, CK_TAM = 64, 374, 56, 34


def checklist_teste(cv, t, T, a, dx=0.0):
    if a <= 0:
        return
    cv.save(); cv.translate(dx, 0)
    itens = (("PÉS JUNTOS", T["juntos"]), ("JOELHOS ESTICADOS", T["esticados"]),
             ("TRONCO INCLINADO À FRENTE", T["inclinado"]), ("BRAÇOS SOLTOS", T["inclinado"] + 0.5))
    f = skia.Font(F_BLACK, CK_TAM)
    larg = max(f.measureText(s) for s, _ in itens) + 66 + 40
    painel = skia.RRect.MakeRectXY(skia.Rect(CK_X - 14, 258, CK_X - 14 + larg, CK_Y + 3 * CK_PASSO + 24), 22, 22)
    cv.drawRRect(painel, paint(FUNDO_CARTAO, int(165 * a)))
    cv.drawRRect(painel, paint(OURO, int(120 * a), "stroke", 2.5))
    texto(cv, "O TESTE", CK_X + 6, 318, F_BLACK, 44, OURO, int(255 * a * prog(t, T["teste"], T["teste"] + 0.2)),
          centro=False)
    for k, (s, t_ok) in enumerate(itens):
        y = CK_Y + k * CK_PASSO
        caixa = skia.RRect.MakeRectXY(skia.Rect(CK_X, y - 38, CK_X + 46, y + 8), 10, 10)
        cv.drawRRect(caixa, paint(FUNDO_CARTAO, int(230 * a)))
        cv.drawRRect(caixa, paint(OURO, int(255 * a * (0.45 + 0.55 * (t >= t_ok))), "stroke", 3.5))
        if t >= t_ok:
            pr = e_out(clamp((t - t_ok) / 0.3))
            p = skia.Path(); p.moveTo(CK_X + 10, y - 16)
            p.lineTo(CK_X + 10 + 11 * min(1, pr * 2), y - 16 + 11 * min(1, pr * 2))
            if pr > 0.5:
                q = (pr - 0.5) * 2
                p.lineTo(CK_X + 21 + 20 * q, y - 5 - 28 * q)
            cv.drawPath(p, paint(OURO, int(255 * a), "stroke", 6))
            k2 = clamp((t - t_ok) / 0.25)
            texto(cv, s, CK_X + 62 + 30 * (1 - e_out(k2)), y - 4, F_BLACK, CK_TAM, "#FFFFFF", int(255 * a * k2),
                  centro=False, contorno=8)
    cv.restore()


def chip_sinal(cv, x, y, a, tam=46):
    """'SINAL,' em dourado e 'NÃO DIAGNÓSTICO' em marfim — UMA string, pintada em duas cores."""
    if a <= 0:
        return
    s = "SINAL, NÃO DIAGNÓSTICO"
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s); corte = f.measureText("SINAL, ")
    x0 = x - lw / 2
    rr = skia.RRect.MakeRectXY(skia.Rect(x0 - 26, y - tam * 1.05, x0 + lw + 26, y + tam * 0.36), 18, 18)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(225 * a)))
    cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 3.5))
    cv.save(); cv.clipRect(skia.Rect(0, 0, x0 + corte - 4, H))
    cv.drawString(s, x0, y, f, paint(OURO, int(255 * a)))
    cv.restore()
    cv.save(); cv.clipRect(skia.Rect(x0 + corte - 4, 0, W, H))
    cv.drawString(s, x0, y, f, paint(MARFIM, int(255 * a)))
    cv.restore()


# ------------------------------------------------------------------ quadro
R1, R2 = 1130, 1200                    # linhas de rótulo da 1ª parte (abaixo da coluna)
Y_JOELHO = PERF_PISO + (HY + 100 - PISO) * PERF_K


def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    fim = 1 - prog(t, T["manda"] - 0.45, T["manda"] - 0.1)     # a CTA fica limpa

    # ---------------- parte 1: a coluna (mundo A)
    t_sai_col = T["teste"] - 0.5
    if t < t_sai_col + 1.0:
        dy = dy_capa(t, T)
        sai = clamp((t - t_sai_col) / 0.6)
        # câmera: a coluna cresce quando a capa sai e chega mais perto na curva
        s = lerp(1.0, 1.1, 1 - dy / 60)
        s = lerp(s, 1.15, e_inout(prog(t, T["curva"] - 0.2, T["mochila"])))
        cv.save(); cv.translate(540, COL_CY + dy); cv.scale(s, s); cv.translate(-540, -COL_CY)
        est = estado_coluna(t, T)
        a_rot = prog(t, T["escoliose"] + 0.35, T["escoliose"] + 0.6) * (1 - prog(t, T["mochila"] - 0.4, T["mochila"] - 0.1))
        rotulo(cv, "COLUNA", 120, 700, COL_X - BW / 2 + est[3][0] - 2, by(3), MARFIM, a_rot)
        # "não há prova": a pilha ESCURECE por filtro de cor e continua opaca (nada translúcido)
        k_dim = prog(t, T["prova"], T["prova"] + 0.2)
        if k_dim > 0:
            pd = skia.Paint()
            pd.setColorFilter(skia.ColorFilters.Blend(skia.ColorSetARGB(int(150 * k_dim), 0x12, 0x26, 0x38),
                                                      skia.BlendMode.kSrcATop))
            cv.saveLayer(None, pd)
        else:
            cv.save()
        a_seta = prog(t, T["gira"] + 0.05, T["gira"] + 0.55) * (1 - prog(t, T["prova"], T["prova"] + 0.3))
        coluna(cv, t, T, 1.0, saida=sai * 1.0, seta_a=a_seta, linha_a=1 - sai)
        cv.restore()
        brilhos(cv, COL_X + est[3][0], by(3), t, T["gira"] + 0.3, n=14, raio=210)
        # dor: surge fraquinha em vermelho suave, perde a cor e se desfaz em brilhos
        k = t - T["doer"]
        if 0 <= k < 1.4:
            a_d = 0.55 * clamp(k / 0.2) * (1 - prog(k, 0.55, 1.15))
            estrela_dor(cv, 740, 560, 50 * (1 + 0.15 * e_out(clamp(k / 0.3))), a_d)
        brilhos(cv, 740, 560, t, T["doer"] + 0.75, n=10, raio=110)
        # o sinal é visual: o olho pisca ao lado da coluna
        a_o = e_back(prog(t, T["costas"], T["costas"] + 0.3)) * (1 - prog(t, T["curva"] - 0.3, T["curva"]))
        olho(cv, 812, 560, clamp(a_o) * 0.95, clamp(a_o), piscada(t, T["costas"] + 0.75))
        # mochila: desce, pousa, "?" pulsa; sai com o carimbo
        if T["mochila"] - 0.1 <= t < T["teste"]:
            cai = e_out(prog(t, T["mochila"] - 0.05, T["mochila"] + 0.42))
            y = lerp(-80, 950, cai)
            bate = 10 * math.sin(math.pi * prog(t, T["mochila"] + 0.42, T["mochila"] + 0.62))
            fora = e_in_back(prog(t, T["prova"] + 0.35, T["prova"] + 0.9))
            mochila(cv, 250 - 520 * fora, y - bate, 1.0, inc=-6 * fora)
            a_q = prog(t, T["mochila"] + 0.35, T["mochila"] + 0.55) * (1 - prog(t, T["prova"] - 0.1, T["prova"] + 0.15))
            if a_q > 0:
                pulso = 1 + 0.08 * math.sin((t - T["mochila"]) * 8)
                cv.save(); cv.translate(250, 600); cv.scale(pulso, pulso)
                texto(cv, "?", 0, 50, F_BLACK, 150, OURO, int(255 * a_q), contorno=10)
                cv.restore()
        cv.restore()
        # título: só depois que a capa sai, POR CIMA da tracejada (fora do zoom: não invade o selo)
        e_t = e_back(prog(t, T["comeco"] + 0.75, T["comeco"] + 1.05))
        a_tit = prog(t, T["comeco"] + 0.75, T["comeco"] + 0.95) * (1 - prog(t, t_sai_col, t_sai_col + 0.3))
        if a_tit > 0 and e_t > 0:
            cv.save(); cv.translate(540, 300); cv.scale(e_t, e_t); cv.translate(-540, -300)
            chip(cv, "ESCOLIOSE", 540, 318, OURO, clamp(a_tit), tam=50)
            cv.restore()

    # ---------------- partes 2-3: a criança (mundo B-C), com câmera
    s_cam = esc_cd(t, T)
    if t >= T["teste"] - 0.1:
        cv.saveLayer(None, _alfa(fim)) if fim < 1 else cv.save()
        aplica_cd(cv, s_cam)
        mundo_cd(cv, t, T)
        brilhos(cv, PERF_X + 24, PERF_PISO - 8, t, T["juntos"] + 0.4, n=9, raio=90)
        k = t - (T["esticados"] + 0.05)                        # brilho passando pelos joelhos retos
        if 0 <= k < 0.8:
            xg = lerp(PERF_X - 70, PERF_X + 70, e_inout(clamp(k / 0.6)))
            cv.drawCircle(xg, Y_JOELHO, 36, paint(OURO, int(170 * (1 - k / 0.8)), blur=16))
        brilhos(cv, PERF_X, Y_JOELHO, t, T["esticados"] + 0.15, n=10, raio=100)
        cv.restore()

    # ---------------- parte 4: de pé, no estirão — escala PRÓPRIA (não herda a câmera): só cresce
    a_pe = prog(t, T["estirao"] + 0.12, T["estirao"] + 0.32) * fim
    if a_pe > 0:
        cresce = 1 + 0.10 * e_inout(prog(t, T["estirao"] + 0.4, T["rapido"] + 1.0))
        costas_em_pe(cv, a_pe, cresce)

    # ---------------- rótulos da parte 1 (posição fixa, abaixo da cena)
    sai_par = 1 - prog(t, T["costas"] - 0.35, T["costas"] - 0.1)
    chip(cv, "COSTUMA NÃO DOER", 540, R1, "#FFFFFF", prog(t, T["doer"], T["doer"] + 0.2) * sai_par, tam=44, borda=OURO)
    chip(cv, "NO COMEÇO", 540, R2, OURO, prog(t, T["comeco"], T["comeco"] + 0.2) * sai_par, tam=38)
    chip(cv, "O SINAL ESTÁ NAS COSTAS", 540, R1, "#FFFFFF",
         prog(t, T["costas"], T["costas"] + 0.2) * (1 - prog(t, T["curva"] - 0.3, T["curva"] - 0.05)), tam=44, borda=OURO)
    sai_cg = 1 - prog(t, T["prova"] - 0.3, T["prova"] - 0.05)  # a curva e o giro ficam lidos até a prova
    chip(cv, "CURVA PRO LADO", 540, R1, OURO, prog(t, T["curva"], T["curva"] + 0.2) * sai_cg, tam=44)
    chip(cv, "E GIRA JUNTO", 540, R2, OURO, prog(t, T["gira"], T["gira"] + 0.2) * sai_cg, tam=40)
    carimbo(cv, "NÃO HÁ PROVA", 540, 590, -6, T["prova"], t, dur=T["teste"] - T["prova"] - 0.4, tam=58)
    chip(cv, "DE QUE CAUSE ESCOLIOSE", 540, 700, "#FFFFFF",
         prog(t, T["prova"] + 0.25, T["prova"] + 0.45) * (1 - prog(t, T["teste"] - 0.7, T["teste"] - 0.4)), tam=40, borda=OURO)

    # ---------------- parte 2: o teste (checklist no canto)
    a_ck = prog(t, T["teste"], T["teste"] + 0.3) * (1 - prog(t, T["olhe"] - 0.05, T["olhe"] + 0.25))
    checklist_teste(cv, t, T, a_ck, dx=-90 * e_inout(prog(t, T["olhe"] - 0.05, T["olhe"] + 0.25)))

    # ---------------- parte 3: olhar as costas por trás
    a_olho2 = e_back(prog(t, T["olhe"] + 0.2, T["olhe"] + 0.55)) * (1 - prog(t, T["sinal2"] - 0.3, T["sinal2"]))
    olho(cv, 108, 300, 0.55 * clamp(a_olho2), clamp(a_olho2), piscada(t, T["olhe"] + 0.8))
    chip_esq(cv, "OLHE AS COSTAS POR TRÁS", 172, 324, "#FFFFFF",
             prog(t, T["olhe"] + 0.25, T["olhe"] + 0.45) * (1 - prog(t, T["alto"] - 0.25, T["alto"] - 0.05)), tam=40, borda=OURO)
    chip_esq(cv, "UM LADO MAIS ALTO", 172, 324, OURO,
             prog(t, T["alto"], T["alto"] + 0.2) * (1 - prog(t, T["sinal2"] - 0.3, T["sinal2"])), tam=40)
    px, py = na_tela(PICO_D[0], PICO_D[1], s_cam)
    brilhos(cv, px, py, t, T["alto"] + 0.25, n=10, raio=120)
    brilhos(cv, px, py, t, T["aparecendo"] + 0.05, n=12, raio=140)    # a rotação "aparecendo" no lado alto

    # rotação: medalhão no alto, ligado por um fio ao lado mais alto (o corpo não ganha coluna dentro)
    a_med = fim
    k_fio = e_out(prog(t, T["rotacao"] + 0.2, T["rotacao"] + 0.65)) * (1 - prog(t, T["leve"] - 0.3, T["leve"]))
    if k_fio > 0:
        fy = py - 8
        ang = math.atan2(fy - MED_Y, px - MED_X)
        x0, y0 = MED_X + MED_R * math.cos(ang), MED_Y + MED_R * math.sin(ang)
        x1, y1 = lerp(x0, px, k_fio), lerp(y0, fy, k_fio)
        cv.drawLine(x0, y0, x1, y1, paint(OURO, int(90 * fim * k_fio), "stroke", 10, blur=5))
        cv.drawLine(x0, y0, x1, y1, paint(OURO, int(255 * fim), "stroke", 4))
        bat = 1 + 0.6 * math.sin(math.pi * prog(t, T["aparecendo"], T["aparecendo"] + 0.35))
        cv.drawCircle(x1, y1, 8 * bat, paint(OURO, int(255 * fim)))
    medalhao(cv, t, T, a_med)
    carimbo(cv, "ROTAÇÃO DA COLUNA", 540, 1150, -4, T["rotacao"], t, dur=T["sinal2"] - T["rotacao"] - 0.05, tam=46)

    # sinal, não diagnóstico -> avaliação com o ortopedista
    chip_sinal(cv, 540, 1168, prog(t, T["sinal2"], T["sinal2"] + 0.2) * (1 - prog(t, T["estirao"] - 0.3, T["estirao"])))
    a_av = prog(t, T["avaliacao"] - 0.2, T["avaliacao"] + 0.1) * (1 - prog(t, T["estirao"] - 0.3, T["estirao"]))
    ent = e_back(prog(t, T["avaliacao"] - 0.2, T["avaliacao"] + 0.25))
    prancheta(cv, 62, 262 - 40 * (1 - ent), a_av)
    chip_esq(cv, "LEVE PARA AVALIAÇÃO", 172, 324, "#FFFFFF", a_av, tam=40, borda=OURO)
    chip_esq(cv, "COM O ORTOPEDISTA", 172, 400, OURO,
             prog(t, T["ortopedista"], T["ortopedista"] + 0.2) * (1 - prog(t, T["estirao"] - 0.3, T["estirao"])), tam=40)
    lupa(cv, t, T, s_cam)

    # ---------------- parte 4: estirão (calendário + rótulos à esquerda, medalhão à direita)
    a_est = prog(t, T["estirao"], T["estirao"] + 0.3) * fim
    calendario(cv, 64, 262, t, T["estirao"], a_est)
    chip_esq(cv, "NO ESTIRÃO", 182, 330, OURO, a_est, tam=40)
    a_rap = prog(t, T["rapido"], T["rapido"] + 0.25) * fim
    chip_esq(cv, "PODE MUDAR MAIS RÁPIDO", 64, 418, "#FFFFFF", a_rap, tam=34, borda=OURO)
    chevrons(cv, CHEV_X, 402, t, T["rapido"], a_rap)
    brilhos(cv, MED_X, MED_Y, t, T["rapido"] + 0.5, n=12, raio=170)

    capa(cv, t, T["comeco"] + 0.35, ep["gancho"][0], ep["gancho"][1])
    selo_como_funciona(cv, prog(t, T["comeco"] + 0.85, T["comeco"] + 1.2) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface(cv, t, T, blocos, DESTAQUE)

    # CTA: o aviãozinho leva um bloquinho marfim da coluna (mesma trajetória do aviao() do piloto),
    # passando por trás do cartão de identificação
    k = t - (T["manda"] + 0.2)
    if k >= 0:
        x = lerp(230, 850, e_inout(clamp(k / 1.4))); y = lerp(1420, 960, e_inout(clamp(k / 1.4)))
        a = clamp(k / 0.2)
        cv.save()
        cv.clipRRect(skia.RRect.MakeRectXY(skia.Rect(150, 1060, 930, 1214), 28, 28), skia.ClipOp.kDifference, True)
        cv.translate(x, y); cv.rotate(-28); cv.scale(1.5, 1.5)
        cv.drawLine(0, 14, 0, 26, paint("#FFFFFF", int(200 * a), "stroke", 2))
        cv.scale(0.24, 0.24); cv.translate(0, 230)
        bloco(cv, 0, 0, 0, 0, a)
        cv.restore()


def sons(T):
    ev = [(T["escoliose"], "pop", 0.5), (T["doer"], "pop", 0.3), (T["doer"] + 0.75, "shimmer", 0.35),
          (T["comeco"], "pop", 0.45), (T["comeco"] + 0.8, "pop", 0.4),
          (T["costas"], "ping", 0.45), (T["costas"] + 0.75, "tick", 0.4)]
    ev += [(T["curva"] + 0.07 * i + 0.3, "click", 0.55) for i in range(NB)]
    ev += [(T["gira"], "whoosh", 0.4), (T["gira"] + 0.3, "shimmer", 0.6),
           (T["mochila"] - 0.05, "whoosh", 0.45), (T["mochila"] + 0.42, "thump", 0.6), (T["mochila"] + 0.4, "pop", 0.35),
           (T["prova"] - 0.02, "thump", 0.9), (T["prova"] + 0.4, "whoosh", 0.4),
           (T["teste"] - 0.12, "whoosh", 0.5), (T["teste"] + 0.1, "pop", 0.5),
           (T["juntos"] + 0.3, "click", 0.6), (T["juntos"] + 0.05, "ping", 0.5),
           (T["esticados"] + 0.1, "shimmer", 0.45), (T["esticados"], "ping", 0.5),
           (T["inclinado"], "whoosh", 0.35), (T["inclinado"] + 0.05, "ping", 0.5), (T["inclinado"] + 0.5, "ping", 0.45),
           (T["olhe"], "whoosh", 0.5), (T["olhe"] + 0.8, "tick", 0.35), (T["alto"], "pop", 0.6), (T["alto"] + 0.25, "shimmer", 0.4),
           (T["rotacao"] - 0.02, "thump", 0.85), (T["rotacao"] + 0.1, "shimmer", 0.5),
           (T["aparecendo"], "pop", 0.45), (T["aparecendo"] + 0.05, "shimmer", 0.35),
           (T["sinal2"], "pop", 0.6), (T["avaliacao"] - 0.15, "pop", 0.5),
           (T["ortopedista"] - 0.05, "whoosh", 0.5), (T["ortopedista"] + 0.4, "ding", 0.55),
           (T["estirao"], "whoosh", 0.4)]
    ev += [(T["estirao"] + 0.2 * i, "tick", 0.3) for i in range(1, 8)]                 # folhinhas virando
    ev += [(T["rapido"], "click", 0.6), (T["rapido"] + 0.14, "click", 0.6), (T["rapido"] + 0.05, "thump", 0.45),
           (T["rapido"] + 0.5, "shimmer", 0.45), (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def tempos_previa(T):
    return (0.0, T["comeco"] + 1.0, T["gira"] + 0.8, T["mochila"] + 0.7, T["prova"] + 0.6,
            T["inclinado"] + 1.1, T["olhe"] + 0.8, T["alto"] + 0.6, T["ortopedista"] + 0.6,
            T["estirao"] + 0.9, T["rapido"] + 1.0, T["manda"] + 1.0)


# respiro antes da CTA: "PODE MUDAR MAIS RÁPIDO" e o medalhão ficam ~1,8 s na tela depois do "rápido"
render = fazer_render(quadro, ANCORAS, sons, tempos_previa, respiro_cta=2.0)
