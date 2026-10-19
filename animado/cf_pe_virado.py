# -*- coding: utf-8 -*-
"""COMO FUNCIONA — andar de pombinho ("Andar de pombinho? Pode ser a coxa.").

Mesmo estilo das duas cenas aprovadas (fundo azul-petróleo, marfim, dourado, rótulos, carimbo,
brilhos, legenda karaokê, CTA com aviãozinho). O que o verificador exigiu está aqui:
  * Pernas de DESENHO, só contorno arredondado e pele lisa: nenhum osso, nada translúcido, nenhum
    fundo preto — a lupa do fim só aumenta o próprio desenho.
  * Os anéis (pé, canela, coxa) são POSSIBILIDADES, um OU outro: quando um acende, o anterior baixa
    o brilho; na "rotação" pulsam um de cada vez, soltos, sem engrenagem.
  * "SOZINHO" nunca aparece sem "NA MAIORIA DAS VEZES" logo acima.
  * Quedas: a pegada sai do alinhamento e fica PARADA, contorno vermelho, sem graça.
  * O pombinho (piada com a expressão, não com a criança) some a partir do "alerta".
A cena é PRESA ao roteiro pelas palavras-âncora (ANCORAS): mudar o roteiro sem elas quebra o
render de propósito (KeyError), em vez de sair vídeo dessincronizado.
"""
import math

import skia

from .cf_alongamento import (BG_OUT, F_BLACK, OSSO_B, OSSO_C, OURO, PELE, VERMELHO, H, W, brilhos, clamp,
                             e_back, e_inout, e_out, fundo, lerp, paint, prog, texto)
from .cf_comum import capa, carimbo, fazer_render, interface, selo_como_funciona
from .cf_fratura_cola import calendario

ANCORAS = {
    "pombinho": ("pombinho", 1, False), "vira": ("vira", 1, False), "dentro1": ("dentro", 1, False),
    "onde": ("onde", 1, False), "giro": ("giro", 1, False), "pe2": ("pé", 2, False),
    "canela": ("canela", 1, False), "coxa": ("coxa", 1, False), "rotacao": ("rotação", 1, False),
    "dentro2": ("dentro", 2, False), "fora": ("fora", 1, False), "crescimento": ("crescimento", 1, False),
    "maioria": ("maioria", 1, False), "alinha": ("alinha", 1, False), "sozinho": ("sozinho", 1, False),
    "alerta": ("alerta", 1, False), "lado": ("lado", 1, False), "dor": ("dor", 1, False),
    "quedas": ("quedas", 1, False), "piora": ("piora", 1, False), "ortopedista": ("ortopedista", 1, False),
    "manda": ("manda", 1, False),
}
DESTAQUE = {"pombinho", "dentro", "pé", "giro", "canela", "coxa", "rotação", "natural", "fora", "crescimento",
            "sozinho", "alerta", "lado", "dor", "quedas", "piora", "ortopedista"}

PELE_CL, PELE_ESC, PELE_LINHA = "#F7CDB8", "#DA987E", "#B9765E"
SHORT, SHORT_CL = "#4C86C6", "#6FA3DA"
POMBO_CORPO, POMBO_CAB, POMBO_ASA, POMBO_ESC = "#9DADBF", "#B2C0CE", "#7F92A8", "#4E6075"
POMBO_PESC, POMBO_PE = "#6FA59A", "#E59A94"
FUNDO_CARTAO = "#0B1824"


# ------------------------------------------------------------------ utilidades
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
    """Seta curva por uma lista de pontos; a cabeça segue a tangente do último trecho."""
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
    """Rótulo solto (sem ponteiro), centrado em x; y = linha de base do texto."""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    rr = skia.RRect.MakeRectXY(skia.Rect(x - lw / 2 - 24, y - tam * 1.05, x + lw / 2 + 24, y + tam * 0.34), 16, 16)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(220 * a)))
    cv.drawRRect(rr, paint(borda or cor, int(255 * a), "stroke", 3))
    cv.drawString(s, x - lw / 2, y, f, paint(cor, int(255 * a)))


# ------------------------------------------------------------------ pegada (vista de cima)
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


def pegada(cv, x, y, ang, esc, a, direita=False, borda=None, borda_a=0.0):
    """Pegada de criança apontando para cima (pé esquerdo; `direita` espelha), girada `ang` graus."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.rotate(ang); cv.scale(-esc if direita else esc, esc)
    cv.save(); cv.translate(3, 5)
    cv.drawPath(SOLA, paint("#000000", int(55 * a), blur=7))
    cv.restore()
    cv.drawPath(SOLA, paint(OSSO_C, int(240 * a)))
    cv.drawPath(SOLA, paint(OSSO_B, int(200 * a), "stroke", 3))
    for dx, dy, r in DEDOS:
        cv.drawCircle(dx, dy, r, paint(OSSO_C, int(240 * a)))
        cv.drawCircle(dx, dy, r, paint(OSSO_B, int(200 * a), "stroke", 2.4))
    if borda and borda_a > 0:
        cv.drawPath(SOLA, paint(borda, int(110 * a * borda_a), "stroke", 14, blur=6))
        cv.drawPath(SOLA, paint(borda, int(255 * a * borda_a), "stroke", 5))
        for dx, dy, r in DEDOS:
            cv.drawCircle(dx, dy, r, paint(borda, int(255 * a * borda_a), "stroke", 3.5))
    cv.restore()


# ------------------------------------------------------------------ pombinho (formas simples)
def pombo(cv, x, y, esc, fase, andando, virado=1, olhar=0.0, a=1.0):
    """(x, y) = chão entre os pés. `virado` 1 = olhando para a direita. `olhar` inclina a cabeça."""
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
    cv.drawOval(skia.Rect(-10, -92, 48, -34), paint(POMBO_CAB, int(150 * a)))              # peito mais claro
    cv.save(); cv.rotate(-8)
    cv.drawOval(skia.Rect(-60, -86, 18, -48), paint(POMBO_ASA, int(255 * a)))
    for k in range(2):
        cv.drawLine(-38 + k * 18, -74, -28 + k * 18, -56, paint(POMBO_ESC, int(255 * a), "stroke", 5))
    cv.restore()
    cv.save(); cv.translate(26 + cab, -86); cv.rotate(olhar * 26)
    cv.drawOval(skia.Rect(-15, -34, 19, 12), paint(POMBO_PESC, int(255 * a)))              # pescoço
    cv.drawCircle(10, -40, 22, paint(POMBO_CAB, int(255 * a)))
    cv.drawCircle(17, -44, 6.5, paint("#F29D38", int(255 * a)))
    cv.drawCircle(17, -44, 4.2, paint("#1B2430", int(255 * a)))
    cv.drawCircle(15.6, -45.6, 1.5, paint("#FFFFFF", int(255 * a)))
    b = skia.Path(); b.moveTo(29, -43); b.lineTo(50, -36); b.lineTo(29, -30); b.close()
    cv.drawPath(b, paint(OURO, int(255 * a)))
    cv.drawOval(skia.Rect(25, -45, 34, -38), paint("#F1F4F7", int(255 * a)))
    cv.restore()
    cv.restore()
    cv.restore()


# ------------------------------------------------------------------ pernas de desenho (vista de frente)
XE, XD = 420, 660                 # perna da esquerda / da direita da tela
Y_PISO = 992                      # tornozelo no chão: ponto de giro do pé
PE_L, PE_W, K_PISO = 150, 96, 0.70
ANEL_COXA = (650, 84, 22)         # (y, rx, ry) em volta da coxa
ANEL_CANELA = (880, 68, 18)


def perna_path(x):
    """Coxa + joelho + canela num contorno só, arredondado (perna de desenho, sem osso)."""
    p = skia.Path()
    p.moveTo(x - 64, 470)
    p.cubicTo(x - 67, 600, x - 52, 700, x - 47, 768)
    p.cubicTo(x - 44, 815, x - 52, 860, x - 45, 900)
    p.cubicTo(x - 40, 940, x - 33, 958, x - 31, 982)
    p.arcTo(skia.Rect(x - 31, 951, x + 31, 1013), 180, -180, False)
    p.cubicTo(x + 33, 958, x + 40, 940, x + 45, 900)
    p.cubicTo(x + 52, 860, x + 44, 815, x + 47, 768)
    p.cubicTo(x + 52, 700, x + 67, 600, x + 64, 470)
    p.close()
    return p


def _piso(x, ang, lado):
    """Projeção de um ponto do chão: (ao longo do pé, através do pé) -> tela."""
    th = math.radians(ang)
    dx, dz = math.sin(th) * lado, math.cos(th)
    nx, nz = dz, -dx

    def P(a, b):
        return x + a * dx + b * nx, Y_PISO + (a * dz + b * nz) * K_PISO
    return P


def pe_forma(x, ang, lado):
    """Pé no chão saindo do tornozelo; `ang` > 0 = ponta para o meio. Devolve (contorno, dedos)."""
    P = _piso(x, ang, lado)
    p = skia.Path(); n = 56
    for i in range(n):                                 # superelipse: pé gordinho, mais largo nos dedos
        ph = 2 * math.pi * i / n
        cu, su = math.cos(ph), math.sin(ph)
        u = math.copysign(abs(cu) ** 0.7, cu)
        a = lerp(-20, PE_L, (u + 1) / 2)
        b = (PE_W / 2) * math.copysign(abs(su) ** 0.7, su) * (0.80 + 0.20 * (u + 1) / 2)
        (p.moveTo if i == 0 else p.lineTo)(*P(a, b))
    p.close()
    med = lado                                         # lado de dentro = dedão
    dedos = [(*P(PE_L - 6 + da, f * PE_W / 2 * med), r) for da, f, r in
             ((-2, 0.62, 15.5), (4, 0.27, 12.5), (4, -0.06, 12), (2, -0.38, 11), (-4, -0.66, 10))]
    return p, dedos


def _pele(cv, pth, x, w, a, sombra=True):
    sh = skia.GradientShader.MakeLinear([skia.Point(x - w / 2, 0), skia.Point(x + w / 2, 0)],
                                        [_c(PELE_ESC), _c(PELE), _c(PELE_CL), _c(PELE), _c(PELE_ESC)],
                                        [0.0, 0.22, 0.5, 0.78, 1.0])
    cv.drawPath(pth, paint(PELE, int(255 * a), shader=sh))
    cv.drawPath(pth, paint(PELE_LINHA, int(230 * a), "stroke", 3.2))


def _c(h, a=255):
    h = h.lstrip("#")
    return skia.ColorSetARGB(int(a), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def anel(cv, cx, cy, rx, ry, a, brilho, metade, t, t0, forte=False):
    """Anel elíptico dourado (como o do fixador): metade de trás antes do segmento, da frente depois.
    `brilho` 1 = aceso (com setinha que gira de leve), ~0.35 = apagado. `forte` (coxa): traço e halo
    maiores — o espanto do "até na coxa"."""
    if a <= 0:
        return
    r = skia.Rect(cx - rx, cy - ry, cx + rx, cy + ry)
    if metade == "tras":
        cv.drawArc(r, 180, 180, False, paint("#9C7A2A", int(255 * a * (0.45 + 0.55 * brilho)), "stroke",
                                             10 if forte else 8))
        return
    if brilho > 0.4:
        cv.drawArc(r, 0, 180, False, paint(OURO, int((200 if forte else 170) * a * (brilho - 0.35) / 0.65), "stroke",
                                           30 if forte else 24, blur=14 if forte else 12))
    cv.drawArc(r, 0, 180, False, paint(OURO, int(255 * a * (0.45 + 0.55 * brilho)), "stroke", 12 if forte else 9))
    cv.drawArc(skia.Rect(cx - rx + 5, cy - ry + 3, cx + rx - 5, cy + ry - 2), 30, 120, False,
               paint("#FFF1C2", int(150 * a * brilho), "stroke", 2.5))
    aset = a * clamp((brilho - 0.35) / 0.65)
    if aset > 0:                                       # setinha curva que gira de leve
        osc = 22 * math.sin(2 * math.pi * 0.85 * (t - t0))
        seta_arco(cv, cx, cy, rx + 16, ry + 11, 40 + osc, 128 + osc, "#FFE08A", aset, larg=6, tam=20)


def perna(cv, x, lado, ang, verm, aneis, t):
    """Perna de desenho sempre OPACA, cor de pele normal (nada translúcido, nada cinza)."""
    pe, dedos = pe_forma(x, ang, lado)
    corpo = perna_path(x)
    pc = _piso(x, ang, lado)(PE_L * 0.42, 0)
    geo = {"pe": (pc[0], pc[1] + 4, 112, 50), "canela": (x, ANEL_CANELA[0], ANEL_CANELA[1], ANEL_CANELA[2]),
           "coxa": (x, ANEL_COXA[0], ANEL_COXA[1], ANEL_COXA[2])}
    for seg, (aa, b, esc, t0) in (aneis or {}).items():
        cx, cy, rx, ry = geo[seg]
        anel(cv, cx, cy, rx * esc, ry * esc, aa, b, "tras", t, t0, forte=seg == "coxa")
    _pele(cv, pe, x + 30 * lado * math.sin(math.radians(ang)), 140, 1.0)
    for dx, dy, r in dedos:
        cv.drawCircle(dx, dy, r, paint(PELE_CL, 255))
        cv.drawCircle(dx, dy, r, paint(PELE_LINHA, 230, "stroke", 2.6))
    _pele(cv, corpo, x, 130, 1.0)
    cv.drawArc(skia.Rect(x - 20, 748, x + 20, 772), 25, 130, False, paint(PELE_LINHA, 140, "stroke", 3))   # joelho
    for seg, (aa, b, esc, t0) in (aneis or {}).items():
        cx, cy, rx, ry = geo[seg]
        anel(cv, cx, cy, rx * esc, ry * esc, aa, b, "frente", t, t0, forte=seg == "coxa")
    if verm > 0:
        uni = skia.Op(corpo, pe, skia.PathOp.kUnion_PathOp)
        cv.drawPath(uni, paint(VERMELHO, int(120 * verm), "stroke", 18, blur=8))
        cv.drawPath(uni, paint(VERMELHO, int(255 * verm), "stroke", 6))
        for dx, dy, r in dedos:
            cv.drawCircle(dx, dy, r, paint(VERMELHO, int(255 * verm), "stroke", 4))


def shorts(cv):
    p = skia.Path()
    p.moveTo(344, 424); p.lineTo(736, 424); p.lineTo(764, 566); p.lineTo(562, 572); p.lineTo(540, 530)
    p.lineTo(518, 572); p.lineTo(316, 566); p.close()
    pt = paint(SHORT); pt.setPathEffect(skia.CornerPathEffect.Make(18))
    cv.drawPath(p, paint("#000000", 70, blur=10))
    cv.drawPath(p, pt)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(342, 420, 738, 452), 14, 14), paint(SHORT_CL))
    cv.drawLine(540, 456, 540, 506, paint("#3A6FA8", 255, "stroke", 3))


def seta_pe(cv, x, lado, psi0, psi1, cor, a, R=PE_L + 30):
    """Seta curva no chão, em volta do tornozelo: psi > 0 = ponta para o meio."""
    if a <= 0:
        return
    n = 16
    pts = []
    for k in range(n + 1):
        ps = math.radians(lerp(psi0, psi1, k / n))
        pts.append((x + R * math.sin(ps) * lado, Y_PISO + R * math.cos(ps) * K_PISO))
    seta_pts(cv, pts, cor, a, larg=7, tam=22)


def estrela_dor(cv, x, y, r, a):
    if a <= 0:
        return
    p = skia.Path(); n = 9
    for i in range(2 * n):
        ang = -math.pi / 2 + i * math.pi / n
        rr = (r if i % 4 == 0 else r * 0.84) if i % 2 == 0 else r * 0.46
        (p.moveTo if i == 0 else p.lineTo)(x + rr * math.cos(ang), y + rr * math.sin(ang))
    p.close()
    cv.drawPath(p, paint(VERMELHO, int(120 * a), blur=12))
    cv.drawPath(p, paint(VERMELHO, int(255 * a)))
    cv.drawPath(p, paint("#FFD3D4", int(200 * a), "stroke", 2.5))


# ------------------------------------------------------------------ estado da cena (tudo a partir das palavras)
def ang_pes(t, T):
    """Ângulo de cada pé (graus, > 0 = ponta para o meio): (esquerda, direita)."""
    a = 22.0
    a = lerp(a, 32, e_inout(prog(t, T["dentro2"], T["dentro2"] + 0.3)))
    a = lerp(a, -18, e_inout(prog(t, T["fora"], T["fora"] + 0.35)))
    a = lerp(a, 22, e_inout(prog(t, T["fora"] + 0.5, T["crescimento"] + 0.25)))   # volta ao pombinho...
    a = lerp(a, 0, e_inout(prog(t, T["crescimento"] + 0.25, T["sozinho"])))      # ...e alinha aos poucos
    e = d = a
    for t0 in (T["giro"], T["canela"], T["coxa"]):          # cada giro lá em cima leva o pé junto
        d += 6 * math.sin(math.pi * prog(t, t0, t0 + 0.6))
    e = lerp(e, 28, e_inout(prog(t, T["lado"], T["lado"] + 0.3)))           # só de um lado
    k = e_inout(prog(t, T["quedas"], T["quedas"] + 0.4))                     # volta a quase reto
    e, d = lerp(e, 4, k), lerp(d, 4, k)
    k = e_inout(prog(t, T["piora"], T["piora"] + 0.4))                       # piora: volta a virar
    return lerp(e, 26, k), lerp(d, 26, k)


def estado_aneis(t, T):
    """{segmento: (alfa, brilho, escala, t0)} dos anéis na perna da direita."""
    nasc = (("pe", T["giro"]), ("canela", T["canela"]), ("coxa", T["coxa"]))
    some = 1 - prog(t, T["crescimento"], T["crescimento"] + 0.8)
    out = {}
    for i, (seg, t0) in enumerate(nasc):
        if t < t0 or some <= 0:
            continue
        esc = e_back(clamp((t - t0) / 0.4))
        if t < T["rotacao"]:
            prox = nasc[i + 1][1] if i < 2 else 1e9
            b = 1 - 0.65 * prog(t, prox, prox + 0.3)
        elif t < T["dentro2"]:
            k = (t - T["rotacao"]) / 0.5 - i                                 # um de cada vez: pé, canela, coxa
            fase = k % 3 if k >= 0 else -1
            b = 0.35 + 0.65 * (math.sin(math.pi * fase) if 0 <= fase <= 1 else 0.0)
            if i == 2 and t < T["rotacao"] + 0.15:
                b = max(b, 1 - prog(t, T["rotacao"], T["rotacao"] + 0.15))
        else:
            b = 0.35
        out[seg] = (clamp(prog(t, t0, t0 + 0.15)) * some, b, 0.6 + 0.4 * esc, t0)
    return out


LAY = {"pernas": (0.94, 540, 392), "sozinho": (0.74, 540, 236), "alerta": (0.86, 290, 300)}


def camera(t, T):
    s, cx, top = LAY["pernas"]
    for nome, t0, t1 in (("sozinho", T["crescimento"] + 0.1, T["maioria"] + 0.1),
                         ("alerta", T["alerta"] - 0.15, T["alerta"] + 0.55)):
        k = e_inout(prog(t, t0, t1)); s2, cx2, top2 = LAY[nome]
        s, cx, top = lerp(s, s2, k), lerp(cx, cx2, k), lerp(top, top2, k)
    return s, cx, top


def aplica(cv, cam, dy=0.0):
    s, cx, top = cam
    cv.translate(cx, top + dy); cv.scale(s, s); cv.translate(-540, -430)


def mundo(cv, t, T):
    """Pernas, shorts, anéis, setas dos pés e a estrela da dor (coordenadas do mundo)."""
    ae, ad = ang_pes(t, T)
    verm = prog(t, T["lado"], T["lado"] + 0.3) * (1 - prog(t, T["quedas"], T["quedas"] + 0.4))
    for x in (XE, XD):
        cv.drawOval(skia.Rect(x - 104, Y_PISO + 52, x + 104, Y_PISO + 112), paint("#000000", 75, blur=12))
    perna(cv, XE, 1, ae, verm, None, t)
    perna(cv, XD, -1, ad, 0.0, estado_aneis(t, T), t)
    shorts(cv)
    # setas dos pés: pra dentro / pra fora (ouro) e a piora (vermelho)
    a_in = prog(t, T["dentro2"], T["dentro2"] + 0.1) * (1 - prog(t, T["fora"] - 0.12, T["fora"]))
    a_out = prog(t, T["fora"], T["fora"] + 0.1) * (1 - prog(t, T["fora"] + 0.45, T["fora"] + 0.7))
    a_pio = prog(t, T["piora"], T["piora"] + 0.1)
    for x, lado in ((XE, 1), (XD, -1)):
        if a_in > 0:
            seta_pe(cv, x, lado, 2, lerp(2, 28, e_out(prog(t, T["dentro2"], T["dentro2"] + 0.3))), OURO, a_in)
        if a_out > 0:
            seta_pe(cv, x, lado, -2, lerp(-2, -32, e_out(prog(t, T["fora"], T["fora"] + 0.3))), OURO, a_out)
        if a_pio > 0:
            seta_pe(cv, x, lado, 4, lerp(4, 30, e_out(prog(t, T["piora"], T["piora"] + 0.35))), VERMELHO, a_pio)
    a_dor = prog(t, T["dor"], T["dor"] + 0.12) * (1 - prog(t, T["piora"], T["piora"] + 0.3))
    if a_dor > 0:
        pisca = 0.72 + 0.28 * math.cos((t - T["dor"]) * 13) if t < T["dor"] + 1.2 else 1.0
        estrela_dor(cv, XE - 108, 860, 44 * (0.9 + 0.1 * pisca), a_dor * pisca)


def rotulo_anel(cv, s, x, y, xa, ya, a, dim):
    """Rótulo de anel: caixa OPACA e fio que termina na BORDA esquerda da caixa (nunca risca o texto).
    `a` = entrada/saída (vale para tudo); `dim` (0,6 a 1) = aceso ou apagado — só fio, borda e texto
    esmaecem, o fundo continua opaco para o rótulo apagado seguir legível no celular."""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, 40); lw = f.measureText(s)
    bx = x - 10; k = a * dim
    cv.drawLine(xa, ya, bx, y - 17, paint(OURO, int(200 * k), "stroke", 2.5))
    cv.drawCircle(xa, ya, 6, paint(OURO, int(255 * k)))
    rr = skia.RRect.MakeRectXY(skia.Rect(bx, y - 44, bx + lw + 30, y + 10), 14, 14)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(230 * a)))
    cv.drawRRect(rr, paint(OURO, int(255 * k), "stroke", 2.5))
    cv.drawString(s, bx + 15, y - 3, f, paint(OURO, int(255 * k)))


def rotulos_pernas(cv, t, T):
    """PÉ / CANELA / COXA, presos aos anéis da perna da direita (espaço da câmera)."""
    an = estado_aneis(t, T)
    fim = 1 - prog(t, T["dentro2"], T["dentro2"] + 0.3)
    _, ad = ang_pes(t, T)
    pc = _piso(XD, ad, -1)(PE_L * 0.42, 0)
    for seg, s, t_on, (xa, ya), y in (("pe", "PÉ", T["pe2"], (pc[0] + 112, pc[1] + 4), pc[1] + 30),
                                      ("canela", "CANELA", T["canela"], (XD + ANEL_CANELA[1], ANEL_CANELA[0]), ANEL_CANELA[0] + 26),
                                      ("coxa", "COXA", T["coxa"], (XD + ANEL_COXA[1], ANEL_COXA[0]), ANEL_COXA[0] + 26)):
        if seg not in an:
            continue
        b = an[seg][1]
        dim = 0.6 + 0.4 * clamp((b - 0.35) / 0.65)
        rotulo_anel(cv, s, 824, y, xa, ya, prog(t, t_on, t_on + 0.25) * fim, dim)
    brilhos(cv, XD, ANEL_COXA[0], t, T["coxa"] + 0.05, n=12, raio=130)      # "até na coxa": brilho a mais


# ------------------------------------------------------------------ trilhas de pegadas
TRILHA0 = [(485 if i % 2 == 0 else 595, 1150 - i * 115, i % 2 == 1) for i in range(7)]   # subindo a tela


def t_passo(i):
    """Cinco pegadas já estão na capa; as duas últimas chegam com o pombinho."""
    return -1.4 + i * 0.26 if i < 5 else 0.40 + (i - 5) * 0.26


TRILHA1 = [(150 + i * 112, 1085 if i % 2 == 0 else 1140, i % 2 == 1) for i in range(7)]  # reta, para a direita
QUEDA = 3                                                                                  # a pegada que sai da linha


def abertura(cv, t, T):
    """Chão visto de cima: a trilha do andar de pombinho + o pombinho que entra e sai."""
    a = 1 - prog(t, T["onde"] - 0.2, T["onde"] + 0.15)
    if a <= 0:
        return
    giro = 12 + 12 * e_inout(prog(t, T["vira"], T["vira"] + 0.35))
    for i, (x, y, dir_) in enumerate(TRILHA0):
        k = t - t_passo(i)
        if k < 0:
            continue
        esc = 1.05 * (0.6 + 0.4 * e_back(clamp(k / 0.22)))
        pegada(cv, x, y, giro * (-1 if dir_ else 1), esc, a * clamp(k / 0.1), direita=dir_)
        ks = prog(t, T["vira"] + 0.04 * i, T["vira"] + 0.04 * i + 0.3)    # setinha curva na ponta
        if ks > 0:
            a0 = -90 + (8 if dir_ else -8)
            a1 = a0 + (-58 if dir_ else 58) * e_out(ks)
            seta_arco(cv, x, y, 82, 82, a0, a1, OURO, a * clamp(ks * 4), larg=6, tam=18)
    brilhos(cv, 850, 770, t, T["dentro1"], n=12, raio=170)
    rotulo_anel(cv, "PRA DENTRO", 712, 790, 612, 760, prog(t, T["vira"], T["vira"] + 0.25) * a, 1.0)
    # pombinho: inteiro no quadro já na capa (parado, balançando a cabeça), anda no "pombinho",
    # sai no "vira". Corpo de x-117 a x+93 (escala 1,1): x >= 160 não corta na borda.
    if t < T["vira"] + 1.2:
        ent = e_inout(prog(t, T["pombinho"], T["pombinho"] + 0.85))
        sai = prog(t, T["vira"] + 0.15, T["vira"] + 1.0)
        if sai > 0:
            pombo(cv, lerp(260, -160, e_inout(sai)), 1010, 1.1, t * 4.2, True, virado=-1, a=a)
        else:
            pombo(cv, lerp(160, 260, ent), 1010, 1.1, t * 4.2, 0 < ent < 0.98, a=a)


def trilha_reta(cv, t, T):
    """Trilha reta (vista de cima) do "sozinho" em diante; no "quedas" uma pegada sai da linha."""
    a = 1 - prog(t, T["ortopedista"], T["ortopedista"] + 0.4)
    if t < T["sozinho"] - 0.1 or a <= 0:
        return
    for i, (x, y, dir_) in enumerate(TRILHA1):
        t0 = T["sozinho"] - 0.08 + 0.07 * i
        k = t - t0
        if k < 0:
            continue
        esc = 0.82 * (0.6 + 0.4 * e_back(clamp(k / 0.22)))
        ang, dx, dy, borda = 90.0, 0.0, 0.0, 0.0
        if i == QUEDA:
            q = e_out(prog(t, T["quedas"], T["quedas"] + 0.3))
            ang, dx, dy, borda = 90 + 30 * q, 16 * q, 40 * q, prog(t, T["quedas"], T["quedas"] + 0.15)
        pegada(cv, x + dx, y + dy, ang, esc, a * clamp(k / 0.1), direita=dir_, borda=VERMELHO, borda_a=borda)
        brilhos(cv, x, y, t, t0 + 0.05, n=5, raio=58)


def pombo_volta(cv, t, T):
    """O pombinho volta, olha a trilha reta, inclina a cabeça e sai (some antes do alerta)."""
    t_in, t_ol, t_sai = T["alinha"] - 0.2, T["alinha"] + 0.35, T["sozinho"] + 0.45
    if not (t_in <= t < T["alerta"]):
        return
    if t < t_ol:
        k = e_inout(prog(t, t_in, t_ol))
        pombo(cv, lerp(1200, 965, k), 1140, 0.95, t * 4.2, k < 0.98, virado=-1)
    elif t < t_sai:
        ol = e_inout(prog(t, t_ol, t_ol + 0.25))
        pombo(cv, 965, 1140, 0.95, t * 4.2, False, virado=-1, olhar=ol)
    else:
        k = prog(t, t_sai, T["alerta"] - 0.05)
        pombo(cv, lerp(965, 1220, e_inout(k)), 1140, 0.95, t * 4.2, True, virado=1)


# ------------------------------------------------------------------ alerta
FICHAS = (("lado", ("SÓ DE UM LADO",)), ("dor", ("DOR",)), ("quedas", ("QUEDAS DEMAIS",)),
          ("piora", ("PIORA EM VEZ", "DE MELHORA")))
X_FICHA, TAM_FICHA = 548, 36


def triangulo(cv, x, y, a):
    if a <= 0:
        return
    p = skia.Path(); p.moveTo(x, y - 70); p.lineTo(x + 80, y + 64); p.lineTo(x - 80, y + 64); p.close()
    pt = paint(VERMELHO, int(255 * a)); pt.setPathEffect(skia.CornerPathEffect.Make(18))
    gl = paint(VERMELHO, int(110 * a), blur=18); gl.setPathEffect(skia.CornerPathEffect.Make(18))
    cv.drawPath(p, gl); cv.drawPath(p, pt)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 9, y - 32, x + 9, y + 22), 9, 9), paint("#FFFFFF", int(255 * a)))
    cv.drawCircle(x, y + 43, 10, paint("#FFFFFF", int(255 * a)))


def ficha(cv, linhas, x, y, a):
    if a <= 0:
        return 0
    f = skia.Font(F_BLACK, TAM_FICHA)
    lw = max(f.measureText(s) for s in linhas)
    alt = 58 + 44 * (len(linhas) - 1)
    rr = skia.RRect.MakeRectXY(skia.Rect(x, y - 44, x + lw + 76, y - 44 + alt), 14, 14)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(225 * a)))
    cv.drawRRect(rr, paint(VERMELHO, int(255 * a), "stroke", 3))
    cv.drawCircle(x + 28, y - 14, 9, paint(VERMELHO, int(255 * a)))
    for k, s in enumerate(linhas):
        cv.drawString(s, x + 50, y + 44 * k, f, paint("#FFFFFF", int(255 * a)))
    return alt


def alerta(cv, t, T):
    sai = 1 - prog(t, T["manda"] - 0.45, T["manda"] - 0.1)
    a_tri = prog(t, T["alerta"], T["alerta"] + 0.1) * sai
    if a_tri <= 0:
        return
    junta = e_inout(prog(t, T["ortopedista"], T["ortopedista"] + 0.5))
    if junta > 0:                                       # as quatro fichas se juntam embaixo do triângulo
        rr = skia.RRect.MakeRectXY(skia.Rect(522, lerp(232, 228, junta), 1004, lerp(800, 762, junta)), 24, 24)
        cv.drawRRect(rr, paint(FUNDO_CARTAO, int(150 * junta * sai)))
        cv.drawRRect(rr, paint(VERMELHO, int(200 * junta * sai), "stroke", 3))
    y_tri = lerp(-160, 300, e_back(prog(t, T["alerta"], T["alerta"] + 0.45)))
    triangulo(cv, 763, y_tri, a_tri)
    y = lerp(470, 456, junta)
    for chave, linhas in FICHAS:
        k = prog(t, T[chave], T[chave] + 0.3)
        if k > 0:
            alt = ficha(cv, linhas, X_FICHA + 60 * (1 - e_out(k)), y, clamp(k * 1.6) * sai)
            y += alt + lerp(18, 10, junta)


def lupa(cv, t, T, cam):
    t0 = T["ortopedista"]
    if t < t0:
        return
    a = 1 - prog(t, T["manda"] - 0.45, T["manda"] - 0.1)
    if a <= 0:
        return
    # entra pela esquerda, passa pela coxa da perna destacada e para sobre os pés
    k1 = e_inout(prog(t, t0, t0 + 0.8)); k2 = e_inout(prog(t, t0 + 0.8, t0 + 1.9))
    x = lerp(lerp(-180, 205, k1), 290, k2) + 5 * math.sin(t * 1.7)
    y = lerp(lerp(560, 500, k1), 818, k2) + 4 * math.cos(t * 1.3)
    r, m = 136, 1.4
    cv.saveLayer(None, _alfa(a))
    cv.save()
    clip = skia.Path(); clip.addCircle(x, y, r)
    cv.clipPath(clip, skia.ClipOp.kIntersect, True)
    fundo(cv, t)
    cv.drawRect(skia.Rect(0, 0, W, H), paint("#FFFFFF", 26))         # lente clara: só aumenta o desenho
    cv.translate(x, y); cv.scale(m, m); cv.translate(-x, -y)
    aplica(cv, cam)
    mundo(cv, t, T)
    cv.restore()
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


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    esc = prog(t, T["alerta"] - 0.1, T["alerta"] + 0.4)              # o fundo escurece no alerta
    if esc > 0:
        cv.drawRect(skia.Rect(0, 0, W, H), paint(BG_OUT, int(100 * esc)))

    abertura(cv, t, T)

    cam = camera(t, T)
    ent = prog(t, T["onde"] + 0.05, T["onde"] + 0.5)
    vis = ent * (1 - prog(t, T["manda"] - 0.35, T["manda"] + 0.1))      # a CTA fica limpa
    if vis > 0:
        cv.saveLayer(None, _alfa(vis)) if vis < 1 else cv.save()
        aplica(cv, cam, 150 * (1 - e_out(ent)))
        mundo(cv, t, T)
        rotulos_pernas(cv, t, T)
        cv.restore()

    # "?" dourado pulsando: de onde vem?
    a_q = prog(t, T["onde"] + 0.15, T["onde"] + 0.45) * (1 - prog(t, T["giro"] - 0.1, T["giro"] + 0.2))
    if a_q > 0:
        pulso = 1 + 0.07 * math.sin((t - T["onde"]) * 7)
        cv.save(); cv.translate(196, 700); cv.scale(pulso, pulso)
        texto(cv, "?", 0, 66, F_BLACK, 190, OURO, int(255 * a_q), contorno=10)
        cv.restore()

    # rotação natural; pra dentro / pra fora
    chip(cv, "ROTAÇÃO NATURAL", 540, 340, OURO,
         prog(t, T["rotacao"], T["rotacao"] + 0.25) * (1 - prog(t, T["crescimento"], T["crescimento"] + 0.3)), tam=44)
    # os dois chips nunca dividem a tela (mesmo lugar): um sai antes de o outro entrar
    chip(cv, "PRA DENTRO", 540, 1196, OURO,
         prog(t, T["dentro2"], T["dentro2"] + 0.2) * (1 - prog(t, T["fora"] - 0.12, T["fora"])))
    chip(cv, "PRA FORA", 540, 1196, OURO,
         prog(t, T["fora"], T["fora"] + 0.15) * (1 - prog(t, T["fora"] + 0.45, T["fora"] + 0.7)))

    # crescimento: folhinhas de calendário (sem número); na maioria das vezes; sozinho
    a_cal = prog(t, T["crescimento"], T["crescimento"] + 0.3) * (1 - prog(t, T["alerta"] - 0.2, T["alerta"] + 0.1))
    calendario(cv, 64, 246, t, T["crescimento"], a_cal)
    a_mai = prog(t, T["maioria"], T["maioria"] + 0.25) * (1 - prog(t, T["alerta"] - 0.1, T["alerta"] + 0.2))
    chip(cv, "NA MAIORIA DAS VEZES", 540, 830, "#FFFFFF", a_mai, borda=OURO)
    brilhos(cv, 540, 690, t, T["sozinho"] - 0.05, n=12, raio=150)
    carimbo(cv, "SOZINHO", 540, 952, -5, T["sozinho"], t, dur=T["alerta"] - T["sozinho"] + 0.15)
    trilha_reta(cv, t, T)
    pombo_volta(cv, t, T)

    # alerta: triângulo + fichas; ortopedista: lupa e rótulo
    alerta(cv, t, T)
    lupa(cv, t, T, cam)
    chip(cv, "VALE O ORTOPEDISTA OLHAR", 540, 1150, "#FFFFFF",
         prog(t, T["ortopedista"] + 0.25, T["ortopedista"] + 0.5) * (1 - prog(t, T["manda"] - 0.45, T["manda"] - 0.1)),
         borda=OURO)

    capa(cv, t, T["onde"], ep["gancho"][0], ep["gancho"][1])
    selo_como_funciona(cv, prog(t, T["onde"] + 0.3, T["onde"] + 0.7) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface(cv, t, T, blocos, DESTAQUE)

    # CTA: o aviãozinho leva uma pegadinha marfim (mesma trajetória do aviao() do piloto). Fica na
    # mesma camada do avião (acima do escurecimento da CTA) e, como ele, passa POR TRÁS do cartão de
    # identificação: o recorte exclui o cartão inteiro, e o pendurado curto para acima dele.
    k = t - (T["manda"] + 0.2)
    if k >= 0:
        x = lerp(230, 850, e_inout(clamp(k / 1.4))); y = lerp(1420, 960, e_inout(clamp(k / 1.4)))
        cv.save()
        cv.clipRRect(skia.RRect.MakeRectXY(skia.Rect(150, 1060, 930, 1214), 28, 28), skia.ClipOp.kDifference, True)
        cv.translate(x, y); cv.rotate(-28); cv.scale(1.5, 1.5)
        cv.drawLine(0, 14, 0, 22, paint("#FFFFFF", int(200 * clamp(k / 0.2)), "stroke", 2))
        pegada(cv, 0, 44, 0, 0.36, clamp(k / 0.2))
        cv.restore()


def sons(T):
    ev = [(t_passo(i), "click", 0.45) for i in range(len(TRILHA0)) if t_passo(i) > 0.02]
    ev += [(T["pombinho"], "pop", 0.5), (T["vira"], "whoosh", 0.4), (T["dentro1"], "shimmer", 0.55),
           (T["onde"], "whoosh", 0.6), (T["onde"] + 0.2, "pop", 0.55),
           (T["giro"], "ping", 0.6), (T["canela"], "ping", 0.6), (T["coxa"], "ping", 0.75), (T["coxa"] + 0.05, "shimmer", 0.45)]
    ev += [(T["rotacao"] + 0.5 * i, "click", 0.6) for i in range(int((T["dentro2"] - T["rotacao"]) / 0.5) + 1)]
    ev += [(T["dentro2"], "whoosh", 0.35), (T["fora"], "whoosh", 0.35)]
    ev += [(T["crescimento"] + 0.2 * i, "tick", 0.35) for i in range(8)]                     # folhinhas virando
    ev += [(T["maioria"], "pop", 0.5), (T["sozinho"], "thump", 0.8), (T["sozinho"] + 0.05, "shimmer", 0.8),
           (T["alerta"], "thump", 0.7), (T["lado"], "pop", 0.55), (T["dor"], "tick", 0.7), (T["quedas"], "pop", 0.5),
           (T["piora"], "whoosh", 0.4), (T["ortopedista"], "whoosh", 0.5), (T["ortopedista"] + 0.6, "ding", 0.5),
           (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def tempos_previa(T):
    return (0.0, T["vira"] + 0.55, T["coxa"] + 0.45, T["rotacao"] + 1.2, T["fora"] + 0.3,
            T["crescimento"] + 0.7, T["sozinho"] + 0.5, T["lado"] + 0.6, T["piora"] + 0.9,
            T["ortopedista"] + 2.2, T["manda"] + 1.0, T["total"] - 0.05)


# respiro maior antes da CTA (precedente: cf_transporte_osseo, 2,4): a lupa fica parada sobre os pés com
# "VALE O ORTOPEDISTA OLHAR" mais ~1,2 s. O resto do piso de ~30 s depende do roteiro (79 palavras).
render = fazer_render(quadro, ANCORAS, sons, tempos_previa, respiro_cta=2.8)
