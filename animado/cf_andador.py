# -*- coding: utf-8 -*-
"""COMO FUNCIONA — andador ("ANDADOR ENSINA / A ANDAR?").

Mesmo estilo das cenas aprovadas (fundo azul-petróleo, dourado, rótulos em caixa opaca, carimbo,
brilhos, checklist, legenda karaokê, CTA com aviãozinho). Storyboard e correções do verificador
(lote5_cf/cf_andador_storyboard.json) respeitados aqui:
  * Bebê de DESENHO no padrão do cf_cotovelo_baba: pele lisa e opaca no tom PELE, macacão simples,
    rosto sem detalhe. Nunca marfim (a cor do osso), nada translúcido, nenhum exame simulado.
  * "Ponta dos pés": só a ponta toca o chão (círculo dourado no ponto de contato) e empurra para
    trás; nenhuma outra parte do pé é marcada ou nomeada.
  * Sons só os do som.py: whoosh na entrada/saída do andador, thump nos carimbos.
  * Equilíbrio: só a gangorra (nível de bolha) inclina no "caindo"; ninguém cai.
  * "Quedas": triângulo âmbar desenhado (a exclamação é forma, não texto) ao lado do andador já
    PARADO (o bebê sentado nele, como na capa; no "usado em excesso" ele só desliza de leve e para
    antes do triângulo) — sem bebê caindo, sem escada, sem ferimento.
  * Empurrador: o bebê já está de pé sem segurar em nada e só pousa a mão na alça no "sozinho".
Atos: A) o bebê no andador (o quadro 0 é a capa: o gancho é o único texto grande), carimbo NÃO
ENSINA, "parece que ajuda", o andador rola e volta, desliza (o chão passa) e a ponta dos pés
empurra; B) o nível de bolha e o ciclo caindo -> levantando -> firmando, e o bebê de pé no próprio
peso; C) o andador volta pequeno: NÃO ANTECIPA O ANDAR, USADO EM EXCESSO, QUEDAS; D) checklist
O QUE AJUDA; E) o empurrador.
A cena é PRESA ao roteiro pelas palavras-âncora (ANCORAS): mudar o roteiro sem elas quebra o render
de propósito (KeyError), em vez de sair vídeo dessincronizado.
"""
import math

import skia

from .cf_alongamento import (ACO, ACO_ESC, ACO_HL, F_BLACK, OURO, PELE, brilhos, carimbo, clamp, e_back,
                             e_in_back, e_inout, e_out, fundo, lerp, paint, prog)
from .cf_comum import capa, fazer_render, interface, selo_como_funciona

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "ensina": ("ensina", 1, False), "parece": ("parece", 1, False),
    "move": ("move", 1, False), "mas": ("mas", 1, False), "desliza": ("desliza", 1, False),
    "empurrando": ("empurrando", 1, False), "ponta": ("ponta", 1, False),
    "andar2": ("andar", 2, False), "equilibrio1": ("equilíbrio", 1, False),
    "equilibrio2": ("equilíbrio", 2, False), "caindo": ("caindo", 1, False),
    "levantando": ("levantando", 1, False), "firmando": ("firmando", 1, False), "peso": ("peso", 1, False),
    "andador2": ("andador", 2, False), "antecipa": ("antecipa", 1, False), "usado": ("usado", 1, False),
    "excesso": ("excesso", 1, False), "quedas": ("quedas", 1, False), "ajuda2": ("ajuda", 2, False),
    "chao": ("chão", 1, False), "descalco": ("descalço", 1, False), "tempo": ("tempo", 1, False),
    "empurrador": ("empurrador", 1, False), "sozinho": ("sozinho", 1, False), "manda": ("manda", 1, False),
}
DESTAQUE = {"andador", "ensina", "desliza", "ponta", "pés", "equilíbrio", "caindo", "levantando", "firmando",
            "peso", "antecipa", "excesso", "quedas", "chão", "livre", "descalço", "tempo", "empurrador",
            "sozinho"}

# rótulos (todos estão em ep["tela"])
R_NAO_ENSINA = "NÃO ENSINA"
R_PARECE = "PARECE QUE AJUDA"
R_DESLIZA = "SÓ DESLIZA"
R_PONTA = "PONTA DOS PÉS"
R_EQUIL = "EQUILÍBRIO"
R_CICLO = ("CAINDO", "LEVANTANDO", "FIRMANDO")
R_PESO = "O PRÓPRIO PESO"
R_ANTECIPA = "NÃO ANTECIPA O ANDAR"
R_EXCESSO = "USADO EM EXCESSO"
R_QUEDAS = "QUEDAS"
R_AJUDA = "O QUE AJUDA"
R_CHAO, R_DESC, R_TEMPO = "CHÃO LIVRE", "DESCALÇO", "TEMPO"
R_EMPURR = "EMPURRADOR"
R_SOZINHO = "quando o bebê já fica de pé sozinho"

# ------------------------------------------------------------------ paleta
FUNDO_CARTAO = "#0B1824"
AZUL = "#9CC9FF"
CINZA = "#9AAABB"
AMBAR = "#FFA53A"
PELE_CL, PELE_ESC, PELE_LINHA = "#F7CDB8", "#DA987E", "#B9765E"          # = cf_cotovelo_baba
ROUPA, ROUPA_CL, ROUPA_ESC, ROUPA_LINHA = "#6FC7B1", "#9EE0CF", "#3F9A85", "#2C7464"
CABELO = "#4A3426"
TECIDO, TECIDO_CL, TECIDO_ESC = "#4C86C6", "#6FA3DA", "#2F5E94"           # assento do andador
RODA, RODA_HUB = "#25313E", "#8FA3B8"
BRINQ, BRINQ_CL, BRINQ_ESC = "#8E7CC3", "#B3A5DD", "#5E4E96"              # carrinho de empurrar
TONS_PELE = (PELE_ESC, PELE, PELE_CL, PELE, PELE_ESC)
TONS_ROUPA = (ROUPA_ESC, ROUPA, ROUPA_CL, ROUPA, ROUPA_ESC)
TONS_ACO = (ACO_ESC, ACO, ACO_HL, ACO, ACO_ESC)
TONS_BRINQ = (BRINQ_ESC, BRINQ, BRINQ_CL, BRINQ, BRINQ_ESC)
TOPO = 318                                     # linha de base dos rótulos do alto (abaixo do selo)
R1 = 1186                                      # linha de base dos rótulos de baixo (acima da legenda)


# ------------------------------------------------------------------ utilidades (copiadas de cf_cotovelo_baba / cf_quadril_bebe)
def _c(h, a=255):
    h = h.lstrip("#")
    return skia.ColorSetARGB(int(a), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def camada(cv, a):
    """saveLayer com transparência (o grupo inteiro aparece/some junto, sem ver uma peça pela outra)."""
    if a >= 0.999:
        cv.save(); return
    p = skia.Paint()
    p.setAlphaf(clamp(a))
    cv.saveLayer(None, p)


def janela(t, t0, t1, d_in=0.25, d_out=0.3):
    return prog(t, t0, t0 + d_in) * (1 - prog(t, t1, t1 + d_out))


def _pele(cv, pth, p0, p1, a, tons=TONS_PELE, linha=3.0, cor_linha=PELE_LINHA):
    sh = skia.GradientShader.MakeLinear([skia.Point(*p0), skia.Point(*p1)], [_c(c) for c in tons],
                                        [0.0, 0.22, 0.5, 0.78, 1.0])
    cv.drawPath(pth, paint(tons[1], int(255 * a), shader=sh))
    if linha:
        cv.drawPath(pth, paint(cor_linha, int(230 * a), "stroke", linha))


def rr_path(x0, y0, x1, y1, r):
    p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), r, r)); return p


def oval_path(x0, y0, x1, y1):
    p = skia.Path(); p.addOval(skia.Rect(x0, y0, x1, y1)); return p


def uniao(*ps):
    out = ps[0]
    for q in ps[1:]:
        out = skia.Op(out, q, skia.PathOp.kUnion_PathOp) or out
    return out


def tubo_path(x0, y0, x1, y1, larg, mao=0.0):
    """Tubo arredondado de (x0, y0) a (x1, y1) (com mão redonda na ponta), já no lugar."""
    ang = math.degrees(math.atan2(y1 - y0, x1 - x0)) - 90
    L = math.hypot(x1 - x0, y1 - y0)
    p = rr_path(-larg / 2, -larg / 2, larg / 2, L + larg / 2, larg / 2)
    if mao:
        p = uniao(p, oval_path(-mao, L - mao * 0.4, mao, L + mao * 1.7))
    m = skia.Matrix.Translate(x0, y0); m.preRotate(ang)
    p.transform(m)
    return p


def ponta(cv, x, y, ang, tam, cor, a):
    """Cabeça de seta em (x, y) apontando para `ang` (radianos)."""
    p = skia.Path()
    p.moveTo(x + tam * math.cos(ang), y + tam * math.sin(ang))
    p.lineTo(x + tam * 0.75 * math.cos(ang + 2.45), y + tam * 0.75 * math.sin(ang + 2.45))
    p.lineTo(x + tam * 0.75 * math.cos(ang - 2.45), y + tam * 0.75 * math.sin(ang - 2.45))
    p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))


def seta(cv, x0, y0, x1, y1, cor, a, larg=9, tam=30, contorno=False):
    if a <= 0 or math.hypot(x1 - x0, y1 - y0) < 2:
        return
    ang = math.atan2(y1 - y0, x1 - x0)
    xb, yb = x1 - tam * 0.55 * math.cos(ang), y1 - tam * 0.55 * math.sin(ang)
    if contorno:
        cv.drawLine(x0, y0, xb, yb, paint(FUNDO_CARTAO, int(200 * a), "stroke", larg + 8))
        ponta(cv, x1 + 3 * math.cos(ang), y1 + 3 * math.sin(ang), ang, tam + 9, FUNDO_CARTAO, 0.8 * a)
    cv.drawLine(x0, y0, xb, yb, paint(cor, int(90 * a), "stroke", larg + 10, blur=7))
    cv.drawLine(x0, y0, xb, yb, paint(cor, int(255 * a), "stroke", larg))
    ponta(cv, x1, y1, ang, tam, cor, a)


def curva_pts(p0, p1, p2, n=28):
    return [((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0],
             (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1]) for u in (i / n for i in range(n + 1))]


def seta_curva(cv, pts, pr, cor, a, larg=8, tam=26, tracejada=False):
    """Seta que se desenha ao longo de `pts` (pr 0..1)."""
    if a <= 0 or pr <= 0:
        return
    n = max(2, int(round(len(pts) * pr)))
    q = pts[:n]
    p = skia.Path(); p.moveTo(*q[0])
    for x, y in q[1:]:
        p.lineTo(x, y)
    if tracejada:
        pm = paint(cor, int(255 * a), "stroke", larg)
        pm.setPathEffect(skia.DashPathEffect.Make([14.0, 12.0], 0.0))
        cv.drawPath(p, pm)
        return
    cv.drawPath(p, paint(cor, int(90 * a), "stroke", larg + 10, blur=7))
    cv.drawPath(p, paint(cor, int(255 * a), "stroke", larg))
    (xa, ya), (xb, yb) = q[-2], q[-1]
    ponta(cv, xb, yb, math.atan2(yb - ya, xb - xa), tam, cor, a)


def chip(cv, s, x, y, cor, a, tam=42, borda=None, esc=1.0, rot=0.0):
    """Rótulo solto centrado em x; y = linha de base do texto."""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    cy = y - tam * 0.35
    cv.save(); cv.translate(x, cy); cv.rotate(rot); cv.scale(esc, esc); cv.translate(-x, -cy)
    rr = skia.RRect.MakeRectXY(skia.Rect(x - lw / 2 - 24, y - tam * 1.05, x + lw / 2 + 24, y + tam * 0.34), 16, 16)
    cv.drawRRect(rr, paint("#000000", int(70 * a), blur=10))
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(228 * a)))
    cv.drawRRect(rr, paint(borda or cor, int(255 * a), "stroke", 3))
    cv.drawString(s, x - lw / 2, y, f, paint(cor, int(255 * a)))
    cv.restore()


def caixa_check(cv, x0, y, t_ok, t, a, tam=56):
    """Caixinha do checklist (mesmo traço do cf_fratura_cola); o tique se desenha em `t_ok`."""
    if a <= 0:
        return
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y - tam * 0.84, x0 + tam, y + tam * 0.16), 12, 12)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(235 * a)))
    cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 4))
    if t >= t_ok:
        k = tam / 50
        pr = e_out(clamp((t - t_ok) / 0.3))
        p = skia.Path(); p.moveTo(x0 + 10 * k, y - 18 * k)
        p.lineTo(x0 + (10 + 12 * min(1, pr * 2)) * k, y + (-18 + 12 * min(1, pr * 2)) * k)
        if pr > 0.5:
            q = (pr - 0.5) * 2
            p.lineTo(x0 + (22 + 22 * q) * k, y + (-6 - 30 * q) * k)
        cv.drawPath(p, paint(OURO, int(255 * a), "stroke", 7))


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


def pegadinha(cv, x, y, esc, cor, a, espelho=False):
    """Pegadinha de bebê só no contorno (a mesma do cf_quadril_bebe)."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(-esc if espelho else esc, esc)
    cv.drawPath(SOLA, paint(cor, int(255 * a), "stroke", 4.5))
    for dx, dy, r in DEDOS:
        cv.drawCircle(dx, dy, r, paint(cor, int(255 * a), "stroke", 3.5))
    cv.restore()


def relogio(cv, x, y, r, a, ang):
    """Relógio de ponteiros, sem números."""
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


def triangulo_alerta(cv, x, y, esc, a):
    """Triângulo âmbar; a exclamação é FORMA (barra + ponto), não texto."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    p = skia.Path(); p.moveTo(0, -50); p.lineTo(58, 46); p.lineTo(-58, 46); p.close()
    for pt in (paint(AMBAR, int(90 * a), blur=16), paint(FUNDO_CARTAO, int(240 * a)), paint(AMBAR, int(255 * a), "stroke", 8)):
        pt.setPathEffect(skia.CornerPathEffect.Make(14))
        cv.drawPath(p, pt)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-6, -22, 6, 16), 6, 6), paint(AMBAR, int(255 * a)))
    cv.drawCircle(0, 30, 7, paint(AMBAR, int(255 * a)))
    cv.restore()


# ------------------------------------------------------------------ o bebê de desenho (origem = chão entre os pés; de frente)
def _macacao():
    p = skia.Path()
    p.moveTo(-56, -340)
    p.cubicTo(-86, -326, -100, -276, -98, -228)
    p.cubicTo(-96, -186, -84, -160, -66, -148)
    p.lineTo(-6, -148); p.lineTo(0, -160); p.lineTo(6, -148); p.lineTo(66, -148)
    p.cubicTo(84, -160, 96, -186, 98, -228)
    p.cubicTo(100, -276, 86, -326, 56, -340)
    p.close()
    return p


MACACAO = _macacao()
OMBRO = (74.0, -318.0)
L_BRACO = 50.0                              # braço e antebraço (bebê: curtinhos)


def bebe_tronco(cv):
    """Macacão + cabeça (rosto sem detalhe, topete curto)."""
    cv.drawPath(MACACAO, paint("#000000", 60, blur=10))
    _pele(cv, MACACAO, (-100, 0), (100, 0), 1.0, tons=TONS_ROUPA, cor_linha=ROUPA_LINHA)
    for yy in (-296, -266):                                          # botõezinhos do macacão
        cv.drawCircle(0, yy, 5.5, paint(ROUPA_CL))
        cv.drawCircle(0, yy, 5.5, paint(ROUPA_LINHA, 200, "stroke", 2))
    for s in (-1, 1):                                                # orelhas
        orl = oval_path(s * 80 - 12, -430, s * 80 + 12, -394)
        _pele(cv, orl, (s * 80 - 13, 0), (s * 80 + 13, 0), 1.0, linha=2.2)
    cab = skia.Path(); cab.addCircle(0, -410, 80)
    cv.drawCircle(3, -404, 82, paint("#000000", 50, blur=8))
    _pele(cv, cab, (-82, 0), (82, 0), 1.0)
    cv.save(); cv.clipPath(cab, skia.ClipOp.kIntersect, True)
    cv.drawOval(skia.Rect(-70, -500, 70, -452), paint(CABELO))
    cv.restore()
    top = skia.Path(); top.moveTo(-6, -486)
    top.cubicTo(-4, -520, 34, -518, 28, -496); top.cubicTo(24, -484, 8, -490, 14, -502)
    cv.drawPath(top, paint(CABELO, 255, "stroke", 8))


def manga(cv, x0, y0, x1, y1, larg, frac=0.42):
    """Manga curta do macacão: cobre o começo do braço (de (x0, y0) em direção a (x1, y1))."""
    ang = math.degrees(math.atan2(y1 - y0, x1 - x0)) - 90
    L = math.hypot(x1 - x0, y1 - y0) * frac
    cv.save(); cv.translate(x0, y0); cv.rotate(ang)
    w0, w1 = larg * 0.42, larg * 0.56
    p = skia.Path()
    p.moveTo(-w0, 0); p.cubicTo(-w0, -larg * 0.55, w0, -larg * 0.55, w0, 0)
    p.lineTo(w1, L - 7); p.quadTo(w1, L, w1 - 7, L); p.lineTo(-w1 + 7, L); p.quadTo(-w1, L, -w1, L - 7)
    p.close()
    _pele(cv, p, (-w1 - 2, 0), (w1 + 2, 0), 1.0, tons=TONS_ROUPA, linha=2.6, cor_linha=ROUPA_LINHA)
    cv.restore()


def cotovelo_ik(s, ox, oy, wx, wy, para_baixo=True):
    """Cotovelo para braço/antebraço de mesmo tamanho (L_BRACO) ligando ombro e punho."""
    d = math.hypot(wx - ox, wy - oy)
    if d >= 2 * L_BRACO - 0.5:
        return (ox + (wx - ox) / 2, oy + (wy - oy) / 2)
    h = math.sqrt(max(0.0, L_BRACO ** 2 - (d / 2) ** 2))
    mx, my = (ox + wx) / 2, (oy + wy) / 2
    nx, ny = -(wy - oy) / d, (wx - ox) / d
    c1, c2 = (mx + nx * h, my + ny * h), (mx - nx * h, my - ny * h)
    if para_baixo:
        return c1 if c1[1] > c2[1] else c2
    return c1 if s * c1[0] > s * c2[0] else c2


def bebe_braco(cv, s, punho, cotovelo):
    ox, oy = OMBRO[0] * s, OMBRO[1]
    ex, ey = cotovelo; wx, wy = punho
    p = uniao(tubo_path(ox, oy, ex, ey, 40), tubo_path(ex, ey, wx, wy, 36, mao=19))
    L = math.hypot(ex - ox, ey - oy) or 1
    nx, ny = -(ey - oy) / L, (ex - ox) / L
    cv.drawPath(p, paint("#000000", 50, blur=8))
    _pele(cv, p, (ox - nx * 24, oy - ny * 24), (ox + nx * 24, oy + ny * 24), 1.0, linha=2.6)
    manga(cv, ox, oy, ex, ey, 54, frac=0.5)


BRACO_SOLTO = {s: ((s * 100, -222), (s * 94, -270)) for s in (-1, 1)}     # (punho, cotovelo), de pé


def bebe_de_pe(cv, punho_dir=None, glow_pes=0.0):
    """O bebê inteiro, de pé, os dois pés apoiados. `punho_dir`: punho do braço direito (da tela)."""
    cv.drawOval(skia.Rect(-120, -12, 120, 16), paint("#000000", 80, blur=10))
    if glow_pes > 0:
        for s in (-1, 1):
            cv.drawOval(skia.Rect(s * 44 - 62, -14, s * 44 + 62, 22), paint(OURO, int(170 * glow_pes), blur=14))
    for s in (-1, 1):
        perna = rr_path(s * 34 - 28, -190, s * 34 + 28, -18, 28)
        _pele(cv, perna, (s * 34 - 31, 0), (s * 34 + 31, 0), 1.0, linha=2.6)
        pe = oval_path(s * 44 - 38, -32, s * 44 + 38, 4)
        _pele(cv, pe, (s * 44 - 38, 0), (s * 44 + 38, 0), 1.0, linha=2.6)
    bebe_tronco(cv)
    bebe_braco(cv, -1, *BRACO_SOLTO[-1])
    if punho_dir is None:
        bebe_braco(cv, 1, *BRACO_SOLTO[1])
    else:
        bebe_braco(cv, 1, punho_dir, cotovelo_ik(1, OMBRO[0], OMBRO[1], *punho_dir))


# ------------------------------------------------------------------ o andador (de frente; origem = chão no centro)
BY = -262.0                                    # centro da bandeja
BRX, BRY, FAIXA = 212.0, 44.0, 24.0
FURO = (112.0, 25.0, BY - 4)
SOBE = 22.0                                    # o bebê no andador fica 22 px acima do bebê de pé (pés de ponta)


def _bandeja():
    ext = oval_path(-BRX, BY - BRY, BRX, BY + BRY)
    furo = oval_path(-FURO[0], FURO[2] - FURO[1], FURO[0], FURO[2] + FURO[1])
    return skia.Op(ext, furo, skia.PathOp.kDifference_PathOp)


def _faixa():
    n = 40
    sup = [(BRX * math.cos(math.pi * i / n), BY + BRY * math.sin(math.pi * i / n)) for i in range(n + 1)]
    p = skia.Path(); p.moveTo(*sup[0])
    for x, y in sup[1:]:
        p.lineTo(x, y)
    for x, y in reversed(sup):
        p.lineTo(x, y + FAIXA)
    p.close()
    return p


def _assento():
    p = skia.Path(); p.moveTo(-108, -214); p.lineTo(108, -214)
    p.cubicTo(104, -180, 86, -156, 62, -150); p.lineTo(-62, -150)
    p.cubicTo(-86, -156, -104, -180, -108, -214); p.close()
    return p


BANDEJA, FAIXA_P, ASSENTO = _bandeja(), _faixa(), _assento()
RODAS_TRAS, RODAS_FRENTE = ((-150, 15), (150, 15)), ((-214, 18), (214, 18))


def roda(cv, x, r, ang, escura=False):
    y = -r
    cv.drawRect(skia.Rect(x - 6, -40, x + 6, y), paint("#4A5A6C" if escura else ACO_ESC))
    cv.drawCircle(x, y, r, paint("#1A222C" if escura else RODA))
    cv.drawCircle(x, y, r, paint("#000000", 120, "stroke", 2))
    for k in range(2):
        g = ang + k * math.pi / 2
        cv.drawLine(x - r * 0.72 * math.cos(g), y - r * 0.72 * math.sin(g), x + r * 0.72 * math.cos(g),
                    y + r * 0.72 * math.sin(g), paint(RODA_HUB, 150 if escura else 220, "stroke", 3.2))
    cv.drawCircle(x, y, r * 0.36, paint(RODA_HUB, 170 if escura else 255))


def tubo_aco(cv, x0, y0, x1, y1, larg=13, escuro=False):
    cv.drawLine(x0, y0, x1, y1, paint("#000000", 70, "stroke", larg + 4, blur=4))
    cv.drawLine(x0, y0, x1, y1, paint(ACO_ESC if escuro else ACO, 255, "stroke", larg))
    cv.drawLine(x0 - 2, y0, x1 - 2, y1, paint(ACO_HL, 90 if escuro else 160, "stroke", 2.5))


def pernas_ponta(cv, chute):
    """Pernas penduradas do assento; os pés de ponta, girando no tornozelo (ponta para trás = esquerda)."""
    tips = []
    for i, s in enumerate((-1, 1)):
        x = s * 32
        perna = rr_path(x - 27, -205, x + 27, -40, 27)
        _pele(cv, perna, (x - 30, 0), (x + 30, 0), 1.0, linha=2.6)
        cv.save(); cv.translate(x, -50); cv.rotate(chute[i])
        pe = rr_path(-21, -12, 21, 52, 20)
        _pele(cv, pe, (-22, 0), (22, 0), 1.0, linha=2.6)
        for xd in (-9, 0, 9):                                    # dedinhos (só a dobrinha)
            cv.drawLine(xd, 38, xd, 48, paint(PELE_LINHA, 150, "stroke", 2.2))
        cv.restore()
        g = math.radians(chute[i])
        tips.append((x - 50 * math.sin(g), -50 + 50 * math.cos(g)))
    return tips


def andador(cv, x, y, esc, viagem, a=1.0, bebe=True, chute=(0.0, 0.0), t=0.0, contato=0.0, empurra=(0.0, 0.0)):
    """Andador de frente (aro/bandeja em aço claro sobre armação com 4 rodinhas), com ou sem o bebê.
    `viagem`: quanto já rolou (px da tela) — gira as rodinhas."""
    if a <= 0:
        return
    camada(cv, a)
    cv.translate(x, y); cv.scale(esc, esc)
    ang = viagem / esc / 17.0
    cv.drawOval(skia.Rect(-260, -14, 260, 16), paint("#000000", 90, blur=12))
    # fundo: rodinhas e pernas de trás, aro da base
    for xr, r in RODAS_TRAS:
        roda(cv, xr, r, ang, escura=True)
    for s in (-1, 1):
        tubo_aco(cv, s * 128, BY - 18, s * 150, -38, 11, escuro=True)
    cv.drawOval(skia.Rect(-232, -46, 232, -26), paint(ACO_ESC, 255, "stroke", 11))
    cv.drawOval(skia.Rect(-232, -46, 232, -26), paint(ACO_HL, 110, "stroke", 2.5))
    # metade de trás da bandeja (atrás do tronco)
    sh = skia.GradientShader.MakeLinear([skia.Point(0, BY - BRY), skia.Point(0, BY + BRY)], [_c(ACO_HL), _c(ACO)])
    cv.save(); cv.clipRect(skia.Rect(-400, -600, 400, FURO[2]))
    cv.drawPath(BANDEJA, paint(ACO, 255, shader=sh))
    cv.drawPath(BANDEJA, paint(ACO_ESC, 255, "stroke", 3))
    cv.restore()
    cv.drawArc(skia.Rect(-FURO[0], FURO[2] - FURO[1], FURO[0], FURO[2] + FURO[1]), 180, 180, False,
               paint("#3B4A5C", 255, "stroke", 7))
    tips = None
    if bebe:
        tips = pernas_ponta(cv, chute)
        cv.save(); cv.translate(0, -SOBE); bebe_tronco(cv); cv.restore()
    # assento de tecido (por baixo da bandeja)
    _pele(cv, ASSENTO, (-110, 0), (110, 0), 1.0, tons=(TECIDO_ESC, TECIDO, TECIDO_CL, TECIDO, TECIDO_ESC),
          linha=2.5, cor_linha=TECIDO_ESC)
    cv.drawLine(-70, -156, 70, -156, paint(TECIDO_CL, 200, "stroke", 3))
    # frente da bandeja + faixa
    _pele(cv, FAIXA_P, (-BRX, 0), (BRX, 0), 1.0, tons=TONS_ACO, linha=2.5, cor_linha=ACO_ESC)
    cv.save(); cv.clipRect(skia.Rect(-400, FURO[2], 400, 100))
    cv.drawPath(BANDEJA, paint(ACO, 255, shader=sh))
    cv.drawPath(BANDEJA, paint(ACO_ESC, 255, "stroke", 3))
    cv.restore()
    cv.drawArc(skia.Rect(-BRX + 10, BY - BRY + 6, BRX - 10, BY + BRY - 4), 200, 140, False, paint("#FFFFFF", 120, "stroke", 3))
    for xk, cor in ((-62, "#F29DB2"), (0, "#FFD27A"), (62, "#9CC9FF")):     # botõezinhos de brinquedo
        yk = BY + BRY * math.sqrt(max(0.0, 1 - (xk / BRX) ** 2)) - 13
        cv.drawOval(skia.Rect(xk - 12, yk - 8, xk + 12, yk + 8), paint("#000000", 80, blur=3))
        cv.drawOval(skia.Rect(xk - 11, yk - 9, xk + 11, yk + 6), paint(cor))
        cv.drawOval(skia.Rect(xk - 5, yk - 7, xk + 3, yk - 3), paint("#FFFFFF", 160))
    if bebe:                                                     # bracinhos apoiados na bandeja
        cv.save(); cv.translate(0, -SOBE)
        for s in (-1, 1):
            bebe_braco(cv, s, (s * 150, -258), (s * 114, -292))
        cv.restore()
    # frente: pernas da armação e rodinhas
    for s in (-1, 1):
        tubo_aco(cv, s * 188, BY + BRY + FAIXA - 8, s * 214, -38, 13)
    for xr, r in RODAS_FRENTE:
        roda(cv, xr, r, ang)
    # ponto de contato da ponta dos pés + setinhas de empurrão (para trás)
    if bebe and tips and contato > 0:
        for i, (tx, ty) in enumerate(tips):
            pul = 1 + 0.18 * math.sin(t * 9 + i * 1.3)
            cv.drawCircle(tx, 0, 26 * pul, paint(OURO, int(120 * contato), blur=10))
            cv.drawCircle(tx, 0, 15 * pul, paint(OURO, int(255 * contato), "stroke", 4.5))
            cv.drawCircle(tx, 0, 5, paint(OURO, int(255 * contato)))
            e = empurra[i] * contato
            if e > 0.02:                                         # cada seta fica sob o próprio pé, abaixo do círculo
                dx = -12 * e                                     # (comprimento fixo; só anda um pouco no empurrão)
                seta(cv, tx + 26 + dx, 40, tx - 34 + dx, 40, "#FFFFFF", min(1.0, 1.6 * e), larg=7, tam=22)
    cv.restore()


# ------------------------------------------------------------------ ato A: o bebê no andador
S_A, Y_A = 1.45, 1150.0
CAM_LARGA = (1.0, 540.0, 800.0, 540.0, 800.0)          # (escala, x e y do mundo, x e y na tela)
CAM_DESL = (1.4, 540.0, 1040.0, 540.0, 850.0)
CAM_PONTA = (2.0, 540.0, 1095.0, 540.0, 800.0)
V_DESL = 430.0                                          # px/s do chão passando


def mistura(c1, c2, k):
    return tuple(lerp(a, b, k) for a, b in zip(c1, c2))


def cam_a(t, T):
    c = mistura(CAM_LARGA, CAM_DESL, e_inout(prog(t, T["desliza"] - 0.15, T["desliza"] + 0.55)))
    c = mistura(c, CAM_PONTA, e_inout(prog(t, T["ponta"] - 0.25, T["ponta"] + 0.45)))
    return mistura(c, CAM_LARGA, e_inout(prog(t, T["andar2"] - 0.05, T["andar2"] + 0.6)))


def aplica(cv, cam):
    s, wx, wy, sx, sy = cam
    cv.translate(sx, sy); cv.scale(s, s); cv.translate(-wx, -wy)


def x_andador(t, T):
    """Rola para a direita e volta ("se move"); no "andar" sai pela direita."""
    vai = math.sin(math.pi * e_inout(prog(t, T["move"] - 0.3, T["move"] + 0.85)))
    sai = e_in_back(prog(t, T["andar2"], T["andar2"] + 0.7), 1.2)
    return 540 + 190 * vai + 1400 * sai


def rolagem(t, T):
    """Quanto o chão já passou (px do mundo): a câmera acompanha o andador enquanto ele desliza."""
    t0, t1, ramp = T["desliza"] - 0.05, T["andar2"], 0.35
    k = min(t, t1) - t0
    if k <= 0:
        return 0.0
    return V_DESL * (k - ramp / 2 if k > ramp else k * k / (2 * ramp))


def chutes(t, T):
    """Ângulo de cada pé (graus; + = a ponta raspa para trás). Alternados a partir de "empurrando"."""
    if t < T["empurrando"]:
        return (0.0, 0.0), (0.0, 0.0)
    liga = prog(t, T["empurrando"], T["empurrando"] + 0.2) * (1 - prog(t, T["andar2"], T["andar2"] + 0.3))
    ang, emp = [], []
    for fase in (0.0, 0.5):
        f = ((t - T["empurrando"]) / 0.62 + fase) % 1.0
        v = max(0.0, math.sin(2 * math.pi * f))
        ang.append(20 * v * liga); emp.append(v * liga)
    return tuple(ang), tuple(emp)


def chao_a(cv, rol, a):
    if a <= 0:
        return
    cv.drawLine(-1600, Y_A, 2700, Y_A, paint("#CFE3F5", int(150 * a), "stroke", 4))
    x = -1600 - (rol % 140)
    while x < 2700:
        cv.drawLine(x, Y_A + 24, x + 54, Y_A + 24, paint("#CFE3F5", int(55 * a), "stroke", 5))
        x += 140


def linhas_mov(cv, x, v, a):
    """Três linhas de movimento atrás do andador (do lado de onde ele vem)."""
    k = clamp(abs(v) / 650) * a
    if k <= 0.02:
        return
    s = 1 if v > 0 else -1
    k_e = S_A / 1.27
    for i, (yy, L) in enumerate(((Y_A - 150 * k_e, 150), (Y_A - 290 * k_e, 210), (Y_A - 430 * k_e, 130))):
        x0 = x - s * (300 * k_e + 26 * i)
        cv.drawLine(x0, yy, x0 - s * L * (0.4 + 0.6 * k), yy, paint("#DDEBF7", int(200 * k), "stroke", 8))


def setas_deslize(cv, x, t, t0, a):
    """Setas douradas de deslize correndo sob o andador."""
    if a <= 0:
        return
    for i in range(3):
        f = ((t - t0) * 1.4 + i / 3) % 1.0
        xx = x - 280 + 560 * f
        al = a * math.sin(math.pi * f)
        seta(cv, xx - 60, Y_A + 52, xx + 60, Y_A + 52, OURO, al, larg=8, tam=26)


def ato_a(cv, t, T, cam):
    k = t - T["ensina"]
    tremor = 10 * math.sin(k * 70) * (1 - k / 0.35) if 0 <= k < 0.35 else 0.0
    rol = rolagem(t, T)
    xa = x_andador(t, T)
    v = (x_andador(t + 0.02, T) - x_andador(t - 0.02, T)) / 0.04
    a_chao = 1 - prog(t, T["andar2"] + 0.3, T["andar2"] + 0.7)
    deslizando = prog(t, T["desliza"], T["desliza"] + 0.3) * (1 - prog(t, T["andar2"] - 0.1, T["andar2"] + 0.2))
    a_setas = prog(t, T["desliza"] + 0.3, T["desliza"] + 0.6) * (1 - prog(t, T["andar2"] - 0.1, T["andar2"] + 0.2))
    a_setas *= 1 - prog(t, T["ponta"] - 0.1, T["ponta"] + 0.3)      # no close, a vez é da ponta dos pés (o chão passando já mostra o deslize)
    ang, emp = chutes(t, T)
    contato = prog(t, T["ponta"], T["ponta"] + 0.25) * (1 - prog(t, T["andar2"] - 0.1, T["andar2"] + 0.15))
    cv.save(); cv.translate(tremor, 0)
    aplica(cv, cam)
    chao_a(cv, rol, a_chao)
    linhas_mov(cv, xa, v + V_DESL * deslizando, 1 - prog(t, T["andar2"] + 0.35, T["andar2"] + 0.5))   # não cruzam o nível que entra
    setas_deslize(cv, xa, t, T["desliza"], a_setas)
    andador(cv, xa, Y_A, S_A, (xa - 540) + rol, bebe=True, chute=ang, t=t, contato=contato, empurra=emp)
    cv.restore()

    carimbo(cv, R_NAO_ENSINA, 540 + tremor, 800, -8, T["ensina"], t, dur=T["parece"] - T["ensina"] + 0.05)
    # "parece que ajuda": balança de leve, em dúvida
    a_p = janela(t, T["parece"], T["mas"], 0.25, 0.3)
    if a_p > 0:
        rot = 3.2 * math.sin((t - T["parece"]) * 4.2)
        chip(cv, R_PARECE, 540, TOPO + 4 * math.sin((t - T["parece"]) * 2.1), "#FFFFFF", a_p, tam=46, borda=CINZA,
             esc=lerp(1.15, 1.0, e_out(prog(t, T["parece"], T["parece"] + 0.3))), rot=rot)
    chip(cv, R_DESLIZA, 540, R1, OURO, janela(t, T["desliza"] + 0.05, T["ponta"] - 0.25, 0.25, 0.25), tam=46,
         esc=lerp(1.15, 1.0, e_out(prog(t, T["desliza"] + 0.05, T["desliza"] + 0.35))))
    chip(cv, R_PONTA, 540, R1, OURO, janela(t, T["ponta"], T["andar2"] - 0.1, 0.25, 0.25), tam=46,
         esc=lerp(1.15, 1.0, e_out(prog(t, T["ponta"], T["ponta"] + 0.3))))


# ------------------------------------------------------------------ ato B: equilíbrio (nível de bolha) e o ciclo
NV_X, NV_Y = 540.0, 650.0                       # ponta do apoio (pivô da régua)
NOS = ((200.0, 905.0), (540.0, 905.0), (880.0, 905.0))
Y_ROT_CICLO = 990


def ang_nivel(t, T):
    """Inclinação da régua (graus; + = ponta direita desce)."""
    e1 = T["equilibrio1"]
    th = 2.4 * math.sin((t - e1) * 3.1) * prog(t, e1 + 0.2, e1 + 0.7) * (1 - prog(t, T["caindo"] - 0.35, T["caindo"]))
    th += 15 * e_out(prog(t, T["caindo"], T["caindo"] + 0.5))
    th -= 19 * e_inout(prog(t, T["levantando"], T["levantando"] + 0.5))
    if t >= T["firmando"]:
        k = t - T["firmando"]
        th = -4 * math.exp(-k * 4.5) * math.cos(k * 10)
    return th


def bolha(t, T):
    """A bolha corre para a ponta que SOBE (com um atraso de líquido)."""
    th = ang_nivel(t - 0.12, T) if t - 0.12 >= T["equilibrio1"] else 0.0
    return -clamp(th / 12, -1, 1) * 0.92


def nivel(cv, x, y, esc, ang, bx, brilho, a):
    if a <= 0:
        return
    camada(cv, a)
    cv.translate(x, y); cv.scale(esc, esc)
    tri = skia.Path(); tri.moveTo(0, 0); tri.lineTo(62, 100); tri.lineTo(-62, 100); tri.close()
    cv.drawPath(tri, paint("#000000", 80, blur=10))
    _pele(cv, tri, (-62, 0), (62, 0), 1.0, tons=TONS_ACO, linha=2.5, cor_linha=ACO_ESC)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-110, 98, 110, 116), 8, 8), paint(ACO_ESC))
    cv.save(); cv.rotate(ang)
    corpo = rr_path(-320, -70, 320, -2, 16)
    cv.drawPath(corpo, paint("#000000", 90, blur=14))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, -70), skia.Point(0, -2)], [_c(ACO_HL), _c(ACO), _c(ACO_ESC)])
    cv.drawPath(corpo, paint(ACO, 255, shader=sh))
    cv.drawPath(corpo, paint(ACO_ESC, 255, "stroke", 3))
    for s in (-1, 1):
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(s * 320 - (44 if s > 0 else 0), -70, s * 320 + (0 if s > 0 else 44), -2), 14, 14),
                     paint("#3B4A5C"))
    tubo = skia.RRect.MakeRectXY(skia.Rect(-250, -52, 250, -20), 16, 16)
    cv.drawRRect(tubo, paint("#CFEDE6"))
    cv.drawRRect(tubo, paint("#6FA79D", 255, "stroke", 3))
    for s in (-1, 1):
        cv.drawLine(s * 40, -56, s * 40, -16, paint("#2D3E4E", 255, "stroke", 4))
    px = bx * 200
    if brilho > 0:
        cv.drawCircle(px, -36, 70, paint(OURO, int(160 * brilho), blur=24))
    b = skia.RRect.MakeRectXY(skia.Rect(px - 36, -48, px + 36, -24), 12, 12)
    cv.drawRRect(b, paint(OURO))
    cv.drawRRect(b, paint("#8A6512", 255, "stroke", 2.5))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(px - 22, -45, px + 6, -39), 3, 3), paint("#FFF1C2", 220))
    cv.restore()
    cv.restore()


def ciclo(cv, t, T, a):
    """Três nós e três setas curvas: caindo -> levantando -> firmando -> (volta)."""
    if a <= 0:
        return
    t_on = (T["caindo"], T["levantando"], T["firmando"])
    arcos = [curva_pts((NOS[0][0] + 34, NOS[0][1] - 18), (370, 812), (NOS[1][0] - 34, NOS[1][1] - 18)),
             curva_pts((NOS[1][0] + 34, NOS[1][1] - 18), (710, 812), (NOS[2][0] - 34, NOS[2][1] - 18)),
             curva_pts((NOS[2][0] + 70, Y_ROT_CICLO + 26), (540, 1150), (NOS[0][0] - 70, Y_ROT_CICLO + 26))]
    pr = (e_inout(prog(t, T["caindo"] + 0.1, T["levantando"] - 0.05)),
          e_inout(prog(t, T["levantando"] + 0.1, T["firmando"] - 0.05)),
          e_inout(prog(t, T["firmando"] + 0.05, T["firmando"] + 0.55)))
    fecha = prog(t, T["firmando"] + 0.5, T["firmando"] + 0.8)
    for i, pts in enumerate(arcos):
        seta_curva(cv, pts, 1.0, "#FFFFFF", 0.22 * a, larg=5, tracejada=True)
        seta_curva(cv, pts, pr[i], OURO, a, larg=8, tam=28)
    for i, ((x, y), s) in enumerate(zip(NOS, R_CICLO)):
        on = prog(t, t_on[i], t_on[i] + 0.2)
        pop = e_back(prog(t, t_on[i], t_on[i] + 0.4))
        cv.drawCircle(x, y, 22, paint(FUNDO_CARTAO, int(230 * a)))
        cv.drawCircle(x, y, 22, paint("#FFFFFF", int(110 * a * (1 - on)), "stroke", 4))
        if on > 0:
            r = 22 * (0.6 + 0.4 * pop)
            cv.drawCircle(x, y, r + 14, paint(OURO, int((110 + 80 * fecha) * a * on), blur=12))
            cv.drawCircle(x, y, r, paint(OURO, int(255 * a * on)))
            chip(cv, s, x, Y_ROT_CICLO, "#FFFFFF", a * on, tam=38, borda=OURO, esc=lerp(1.08, 1.0, e_out(on)))


def ato_b(cv, t, T):
    a = prog(t, T["equilibrio1"] - 0.05, T["equilibrio1"] + 0.2) * (1 - prog(t, T["andador2"] - 0.1, T["andador2"] + 0.2))
    if a <= 0 and t > T["andador2"] + 0.5:          # o bebê de pé e O PRÓPRIO PESO têm fade próprio até ~andador2+0,45
        return
    ent = e_back(prog(t, T["equilibrio1"] - 0.05, T["equilibrio1"] + 0.4))
    # o nível abre espaço já no "próprio": quando o bebê aparece (no "peso") a ponta direita está em x≈640, longe dele
    lado = e_inout(prog(t, T["peso"] - 0.3, T["peso"] + 0.25))
    esc = lerp(0.6, 1.0, ent) * lerp(1.0, 0.6, lado)
    x = lerp(NV_X, 285, lado)
    brilho = prog(t, T["firmando"] + 0.25, T["firmando"] + 0.55)
    nivel(cv, x, NV_Y, esc, ang_nivel(t, T), bolha(t, T), brilho, a * clamp(ent * 2))
    brilhos(cv, x, NV_Y - 38 * esc, t, T["firmando"] + 0.5, n=14, raio=200 * esc)
    a_c = prog(t, T["equilibrio2"] - 0.1, T["equilibrio2"] + 0.3) * a
    ciclo(cv, t, T, a_c)
    # o bebê de pé, sem andador, os dois pés no chão; uma seta dourada desce do corpo até os pés
    a_b = prog(t, T["peso"], T["peso"] + 0.2) * (1 - prog(t, T["andador2"] + 0.15, T["andador2"] + 0.45))
    if a_b > 0:
        bx, by, be = 800.0, 800.0, 0.8
        pop = e_back(prog(t, T["peso"], T["peso"] + 0.35))
        camada(cv, a_b)
        cv.drawLine(bx - 150, by, bx + 160, by, paint("#CFE3F5", 150, "stroke", 4))
        cv.translate(bx, by); cv.scale(be * lerp(0.85, 1.0, pop), be * lerp(0.85, 1.0, pop))
        bebe_de_pe(cv, glow_pes=prog(t, T["peso"] + 0.45, T["peso"] + 0.65))
        pr = e_out(prog(t, T["peso"] + 0.1, T["peso"] + 0.5))
        if pr > 0:
            seta(cv, 0, -300, 0, lerp(-300, -16, pr), OURO, 1.0, larg=12, tam=40, contorno=True)
        cv.restore()
    chip(cv, R_EQUIL, 540, TOPO, OURO, janela(t, T["equilibrio1"], T["peso"] - 0.3, 0.25, 0.2) * a, tam=50,
         esc=lerp(1.2, 1.0, e_out(prog(t, T["equilibrio1"], T["equilibrio1"] + 0.3))))
    chip(cv, R_PESO, 540, TOPO, OURO, janela(t, T["peso"] - 0.05, T["andador2"] + 0.1, 0.25, 0.3), tam=50,
         esc=lerp(1.2, 1.0, e_out(prog(t, T["peso"], T["peso"] + 0.3))))


# ------------------------------------------------------------------ ato C: o andador volta pequeno
X_C, Y_C, S_C = 400.0, 990.0, 0.92


def uso_c(t, T):
    """No "usado em excesso": o mesmo mecanismo do começo, em pequeno — os pés raspam e o andador
    desliza devagar para lá e para cá. Para ANTES do triângulo de QUEDAS (ninguém cai)."""
    t0 = T["usado"] + 0.1
    liga = prog(t, t0, t0 + 0.35) * (1 - prog(t, T["quedas"] - 0.4, T["quedas"] - 0.05))
    if liga <= 0:
        return (0.0, 0.0), 0.0
    ang = []
    for fase in (0.0, 0.5):
        f = ((t - t0) / 0.62 + fase) % 1.0
        ang.append(18 * max(0.0, math.sin(2 * math.pi * f)) * liga)
    return tuple(ang), 34 * math.sin((t - t0) * 2.4) * liga


def ato_c(cv, t, T):
    # entra 0,15 s depois: o nível e o ciclo do ato B já sumiram quando o andador passa por ali
    ent = e_out(prog(t, T["andador2"] + 0.15, T["andador2"] + 0.7))
    sai = e_in_back(prog(t, T["ajuda2"] - 0.4, T["ajuda2"] + 0.05), 1.2)
    a = prog(t, T["andador2"] + 0.15, T["andador2"] + 0.35) * (1 - prog(t, T["ajuda2"] - 0.2, T["ajuda2"] + 0.0))
    if a <= 0:
        return
    k = t - T["antecipa"]
    tremor = 8 * math.sin(k * 70) * (1 - k / 0.35) if 0 <= k < 0.35 else 0.0
    chute, dx = uso_c(t, T)
    x = lerp(-420, X_C, ent) - 900 * sai + tremor + dx
    camada(cv, a)
    cv.drawLine(x - dx - 300, Y_C, x - dx + 300, Y_C, paint("#CFE3F5", 130, "stroke", 4))
    andador(cv, x, Y_C, S_C, x - X_C, bebe=True, chute=chute)   # sem queda: só desliza e para antes de QUEDAS
    cv.restore()
    carimbo(cv, R_ANTECIPA, 540 + tremor, 760, -6, T["antecipa"], t, dur=T["usado"] - T["antecipa"] + 0.25)
    fim_c = 1 - prog(t, T["ajuda2"] - 0.4, T["ajuda2"] - 0.15)
    e_x = prog(t, T["usado"], T["usado"] + 0.3)
    chip(cv, R_EXCESSO, X_C, Y_C + 98, AMBAR, e_x * fim_c, tam=42, esc=lerp(1.15, 1.0, e_out(e_x)))
    q = prog(t, T["quedas"] - 0.05, T["quedas"] + 0.3)
    if q > 0:
        pul = 1 + 0.04 * math.sin((t - T["quedas"]) * 6)
        triangulo_alerta(cv, 815, 690, 1.45 * lerp(0.6, 1.0, e_back(q)) * pul, q * fim_c)
        chip(cv, R_QUEDAS, 815, 840, AMBAR, q * fim_c, tam=46, esc=lerp(1.15, 1.0, e_out(q)))


# ------------------------------------------------------------------ ato D: o que ajuda (checklist)
CARTAO = (100.0, 382.0, 980.0, 932.0)
LINHAS = ((R_CHAO, "chao", 628), (R_DESC, "descalco", 748), (R_TEMPO, "tempo", 868))
Y_CHAO_E = 1062.0
ESC_CARTAO = 0.62                              # no alto: título 33 px, itens 32 px (>= 30 px)


def cartao_ajuda(cv, t, T, fim):
    t0 = T["ajuda2"]
    ent = e_back(prog(t, t0 - 0.02, t0 + 0.45))
    sai = e_inout(prog(t, T["empurrador"] - 0.2, T["empurrador"] + 0.3))
    a = prog(t, t0 - 0.02, t0 + 0.2) * fim
    if a <= 0:
        return
    camada(cv, a)
    cx, cy = 540, 657
    esc = lerp(0.9, 1.0, ent) * lerp(1.0, ESC_CARTAO, sai)
    cv.translate(cx, cy + 120 * (1 - ent) - 262 * sai); cv.scale(esc, esc); cv.translate(-cx, -cy)   # topo y≈224: folga do selo
    x0, y0, x1, y1 = CARTAO
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 30, 30)
    cv.drawRRect(rr, paint("#000000", 100, blur=18))
    cv.drawRRect(rr, paint(FUNDO_CARTAO, 245))
    cv.drawRRect(rr, paint(OURO, 255, "stroke", 4))
    f = skia.Font(F_BLACK, 54); lw = f.measureText(R_AJUDA)
    cv.drawString(R_AJUDA, 540 - lw / 2, y0 + 92, f, paint(OURO))
    cv.drawLine(x0 + 60, y0 + 128, x1 - 60, y0 + 128, paint("#FFFFFF", 50, "stroke", 3))
    for rot, chave, y in LINHAS:
        caixa_check(cv, 160, y, T[chave], t, 1.0, tam=60)
        k = prog(t, T[chave], T[chave] + 0.25)
        if k > 0:
            fl = skia.Font(F_BLACK, 52)
            cv.drawString(rot, 250 + 30 * (1 - e_out(k)), y, fl, paint("#FFFFFF", int(255 * k)))
    kd = prog(t, T["descalco"] + 0.1, T["descalco"] + 0.4)
    ke = prog(t, T["descalco"] + 0.3, T["descalco"] + 0.6)
    pegadinha(cv, 770, 724, 0.62, OURO, kd, espelho=True)
    pegadinha(cv, 860, 712, 0.62, OURO, ke)
    kr = prog(t, T["tempo"] + 0.05, T["tempo"] + 0.35)
    if kr > 0:
        cv.save(); cv.translate(815, 846); s = lerp(0.5, 1.0, e_back(kr)); cv.scale(s, s)
        relogio(cv, 0, 0, 44, kr, (t - T["tempo"]) * 4.5)
        cv.restore()
    cv.restore()


# ------------------------------------------------------------------ ato E: o empurrador
BEBE_E = (384.0, Y_CHAO_E, 0.92)


def empurrador(cv, dx, ang, a):
    """Carrinho de empurrar, de lado: caixa com blocos, 4 rodinhas e alça alta (formas simples)."""
    if a <= 0:
        return
    F = Y_CHAO_E
    camada(cv, a)
    cv.translate(dx, 0)
    cv.drawOval(skia.Rect(570, F - 12, 910, F + 14), paint("#000000", 90, blur=10))
    for xr in (646, 866):                                            # rodinhas de trás (mais escuras)
        cv.save(); cv.translate(xr + 18, F - 6); roda_lado(cv, 20, ang, True); cv.restore()
    # alça (tubo inclinado) com a pega na ponta
    tubo_aco(cv, 612, F - 96, 566, F - 286, 16)
    cv.drawCircle(560, F - 294, 22, paint("#000000", 80, blur=6))
    cv.drawCircle(560, F - 294, 20, paint("#47617E"))
    cv.drawCircle(560, F - 294, 20, paint("#2C3E52", 255, "stroke", 3))
    cv.drawCircle(554, F - 300, 6, paint("#9FB6CC", 200))
    # blocos (formas, sem letra)
    for x0, y0, w, cor, forma in ((640, F - 168, 62, "#6FC7B1", "c"), (712, F - 160, 56, "#F29DB2", "t"),
                                  (778, F - 172, 66, "#9CC9FF", "q")):
        r = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x0 + w, y0 + w), 10, 10)
        cv.drawRRect(r, paint(cor)); cv.drawRRect(r, paint("#000000", 70, "stroke", 2.5))
        mx, my = x0 + w / 2, y0 + w / 2
        if forma == "c":
            cv.drawCircle(mx, my, w * 0.22, paint("#FFFFFF", 200))
        elif forma == "t":
            p = skia.Path(); p.moveTo(mx, my - w * 0.24); p.lineTo(mx + w * 0.24, my + w * 0.18); p.lineTo(mx - w * 0.24, my + w * 0.18); p.close()
            cv.drawPath(p, paint("#FFFFFF", 200))
        else:
            cv.drawRect(skia.Rect(mx - w * 0.2, my - w * 0.2, mx + w * 0.2, my + w * 0.2), paint("#FFFFFF", 200))
    corpo = rr_path(590, F - 118, 900, F - 36, 18)
    cv.drawPath(corpo, paint("#000000", 90, blur=10))
    _pele(cv, corpo, (0, F - 118), (0, F - 36), 1.0, tons=TONS_BRINQ, linha=3, cor_linha=BRINQ_ESC)
    cv.drawLine(608, F - 96, 882, F - 96, paint(BRINQ_CL, 200, "stroke", 5))
    for xr in (646, 866):                                            # rodinhas da frente
        cv.save(); cv.translate(xr, F); roda_lado(cv, 24, ang, False); cv.restore()
    cv.restore()


def roda_lado(cv, r, ang, escura):
    cv.drawCircle(0, -r, r, paint("#1A222C" if escura else RODA))
    for k in range(3):
        g = ang + k * math.pi / 3
        cv.drawLine(-r * 0.75 * math.cos(g), -r - r * 0.75 * math.sin(g), r * 0.75 * math.cos(g), -r + r * 0.75 * math.sin(g),
                    paint(RODA_HUB, 140 if escura else 220, "stroke", 3))
    cv.drawCircle(0, -r, r * 0.34, paint(RODA_HUB, 160 if escura else 255))


def ato_e(cv, t, T, fim):
    t0 = T["empurrador"]
    if t < t0 - 0.1:
        return
    ent = e_out(prog(t, t0 + 0.1, t0 + 0.9))
    dx = 700 * (1 - ent)
    empurrador(cv, dx, -dx / 22, prog(t, t0 + 0.1, t0 + 0.25))
    bx, by, be = BEBE_E
    a_b = prog(t, t0 + 0.25, t0 + 0.5)                          # entra depois que o checklist subiu
    if a_b > 0:
        pop = e_back(prog(t, t0 + 0.25, t0 + 0.65))
        # a mão só vai para a alça DEPOIS do "sozinho" (antes: de pé, sem segurar em nada)
        km = e_inout(prog(t, T["sozinho"] + 0.3, T["sozinho"] + 0.95))
        alvo = ((560 - bx) / be - 19 * 0.8, (Y_CHAO_E - 294 - by) / be + 4)
        p0 = BRACO_SOLTO[1][0]
        punho = (lerp(p0[0], alvo[0], km), lerp(p0[1], alvo[1], km) - 40 * math.sin(math.pi * km))
        camada(cv, a_b)
        cv.translate(bx, by); s = be * lerp(0.85, 1.0, pop); cv.scale(s, s)
        bebe_de_pe(cv, punho_dir=punho if km > 0 else None)
        cv.restore()
        k = t - (T["sozinho"] + 0.95)
        if 0 <= k < 0.8:
            cv.drawCircle(560, Y_CHAO_E - 294, 40, paint(OURO, int(170 * math.sin(math.pi * k / 0.8)), blur=14))
    chip(cv, R_EMPURR, 822, 812, OURO, janela(t, t0 + 0.45, 99, 0.25) * fim, tam=44,
         esc=lerp(1.15, 1.0, e_out(prog(t, t0 + 0.45, t0 + 0.75))))
    chip(cv, R_SOZINHO, 540, 1166, "#FFFFFF", prog(t, T["sozinho"] - 0.05, T["sozinho"] + 0.25) * fim, tam=36,
         borda=OURO, esc=lerp(1.1, 1.0, e_out(prog(t, T["sozinho"], T["sozinho"] + 0.3))))


def ato_de(cv, t, T, fim):
    cartao_ajuda(cv, t, T, fim)
    # na CTA a cena do empurrador RECUA e escurece (o aviãozinho pousa em fundo limpo, fora do carrinho)
    k = e_inout(prog(t, T["manda"] - 0.45, T["manda"]))
    camada(cv, lerp(1.0, 0.6, k))
    s = lerp(1.0, 0.75, k)
    cv.translate(380, 700); cv.scale(s, s); cv.translate(-380, -700)
    # chão livre: a linha do chão se estende de ponta a ponta (e vira o chão do empurrador)
    hw = 560 * e_out(prog(t, T["chao"] + 0.05, T["chao"] + 0.7))
    if hw > 1:
        cv.drawLine(540 - hw, Y_CHAO_E, 540 + hw, Y_CHAO_E, paint("#CFE3F5", 160, "stroke", 4))
    ato_e(cv, t, T, fim)
    cv.restore()


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    fim = 1 - prog(t, T["manda"] - 0.45, T["manda"] - 0.1)      # a CTA fica limpa de rótulos
    cam = cam_a(t, T)
    if t < T["andar2"] + 1.0:
        ato_a(cv, t, T, cam)
    if T["equilibrio1"] - 0.1 <= t < T["andador2"] + 0.6:
        ato_b(cv, t, T)
    if T["andador2"] - 0.05 <= t < T["ajuda2"] + 0.5:
        ato_c(cv, t, T)
    if t >= T["ajuda2"] - 0.1:
        ato_de(cv, t, T, fim)

    t_sai = T["ensina"] + 0.3
    capa(cv, t, t_sai, ep["gancho"][0], ep["gancho"][1])
    perto = clamp((cam[0] - 1.0) / 0.08)                         # zoom nos pés: o selo sai logo no começo do zoom
    selo_como_funciona(cv, prog(t, t_sai + 0.35, t_sai + 0.7) * (1 - perto) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface(cv, t, T, blocos, DESTAQUE)


def sons(T):
    ev = [(T["ensina"] - 0.02, "thump", 0.9), (T["parece"] + 0.02, "pop", 0.4),
          (T["move"] - 0.3, "whoosh", 0.4), (T["move"] + 0.35, "whoosh", 0.3),
          (T["desliza"] - 0.1, "whoosh", 0.5), (T["ponta"], "pop", 0.45), (T["ponta"] + 0.15, "ping", 0.35),
          (T["andar2"], "whoosh", 0.6), (T["equilibrio1"], "pop", 0.55), (T["equilibrio2"], "pop", 0.3),
          (T["caindo"], "whoosh", 0.35), (T["caindo"] + 0.05, "pop", 0.4),
          (T["levantando"], "whoosh", 0.3), (T["levantando"] + 0.05, "pop", 0.4),
          (T["firmando"] + 0.05, "pop", 0.4), (T["firmando"] + 0.5, "ding", 0.55), (T["firmando"] + 0.55, "shimmer", 0.45),
          (T["peso"] + 0.05, "thump", 0.45), (T["peso"] + 0.45, "shimmer", 0.35),
          (T["andador2"] + 0.15, "whoosh", 0.5), (T["antecipa"] - 0.02, "thump", 0.9),
          (T["usado"] + 0.02, "pop", 0.45), (T["quedas"], "ping", 0.5),
          (T["ajuda2"] - 0.1, "whoosh", 0.45), (T["ajuda2"] + 0.2, "pop", 0.35),
          (T["chao"] + 0.02, "tick", 0.7), (T["chao"] + 0.1, "whoosh", 0.25),
          (T["descalco"] + 0.02, "tick", 0.7), (T["descalco"] + 0.15, "pop", 0.3), (T["descalco"] + 0.35, "pop", 0.3),
          (T["tempo"] + 0.02, "tick", 0.7), (T["tempo"] + 0.3, "ding", 0.45),
          (T["empurrador"] - 0.05, "whoosh", 0.45), (T["empurrador"] + 0.3, "pop", 0.4),
          (T["sozinho"] + 0.02, "pop", 0.45), (T["sozinho"] + 0.95, "ding", 0.5),
          (T["manda"] + 0.05, "whoosh", 0.5)]
    # rodinhas rolando enquanto o andador desliza (cliques leves)
    t = T["desliza"] + 0.2
    while t < T["andar2"] - 0.1:
        ev.append((t, "click", 0.22)); t += 0.34
    # e de novo, mais baixinho, no deslize curto do "usado em excesso" (para antes de QUEDAS)
    t = T["usado"] + 0.45
    while t < T["quedas"] - 0.4:
        ev.append((t, "click", 0.14)); t += 0.4
    return ev


def tempos_previa(T):
    return (0.0, T["ensina"] + 0.25, T["move"] + 0.15, T["desliza"] + 0.9, T["ponta"] + 0.45,
            T["caindo"] + 0.45, T["peso"] + 0.55, T["antecipa"] + 0.35, T["excesso"] + 0.5,
            T["quedas"] + 0.6, T["sozinho"] + 1.2, T["manda"] + 1.6)


# respiro antes da CTA: o rótulo "quando o bebê já fica de pé sozinho" e a mão na alça ficam ~2 s na tela
render = fazer_render(quadro, ANCORAS, sons, tempos_previa, respiro_cta=1.9)
