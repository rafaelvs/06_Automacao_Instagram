# -*- coding: utf-8 -*-
"""HISTÓRIA NO OSSO — Carlo Mauri ("UM EXPLORADOR E UM / OSSO QUE NÃO COLAVA").

Regras da cena:
  * Nenhum retrato: silhuetas genéricas, sem rosto. O osso é desenho (o mesmo de cf_alongamento), nunca exame.
  * Sem lado da perna e sem ano do acidente (as fontes divergem). Só 1980 e 1981 vão para a tela.
  * Foco RÍGIDO: não balança. O próprio foco é aberto aos poucos (nada de corte nem de transporte de segmento);
    anéis e fios ficam dois acima e dois abaixo do foco, e cada fio atravessa o osso (some por dentro dele).
  * Mapa esquemático: dois pontos e uma rota, sem contorno de país.
  * "CADA CASO É ÚNICO" e "NÃO É PROMESSA DE RESULTADO" entram junto com o resultado e voltam no HOJE (fim).
"""
import math

import skia

from . import cf_hist_byron as byron
from . import cf_transporte_osseo as tr
from .cf_alongamento import (ACO, ACO_ESC, CX, F_BLACK, HASTE, OSSO_C, OSSO_L, OURO, Y_BASE, Y_TOPO, brilhos, clamp,
                             desenha_regenerado, e_back, e_inout, e_out, fundo, haste, lerp, paint, path_osso_inf,
                             path_osso_sup, porca, prog, sombra_osso, texto)
from .cf_comum import capa, fazer_render, interface
from .cf_fratura_cola import _regiao_abaixo, _regiao_acima
from .cf_hist_byron import PAPEL, SILH, SILH_L, caixa, caminho, forma, janela, linha, pessoa, rr
from .cf_pe_torto import CORAL, chip, ponta

ANCORAS = {k: (p, n, False) for k, p, n in (
    ("explorador", "explorador", 1), ("osso1", "osso", 1), ("colava", "colava", 1), ("carlo", "carlo", 1),
    ("quebrou", "quebrou", 1), ("tibia", "tíbia", 1), ("esquiando", "esquiando", 1), ("osso2", "osso", 2),
    ("colou1", "colou", 1), ("infec", "infeccionou", 1), ("nome", "nome", 1), ("pseudo", "pseudartrose", 1),
    ("infectada", "infectada", 1), ("mil1", "mil", 1), ("foi", "foi", 1), ("russia", "rússia", 1),
    ("doutor", "doutor", 1), ("iliz", "ilizarov", 1), ("aparelho", "aparelho", 1), ("foco", "foco", 1),
    ("alongado", "alongado", 1), ("poucos", "poucos", 1), ("dois", "dois", 1), ("cm", "centímetros", 1),
    ("osso3", "osso", 3), ("colou2", "colou", 2), ("volta", "volta", 1), ("contou", "contou", 1),
    ("lecco", "lecco", 1), ("mil2", "mil", 2), ("eles", "eles", 1), ("comecaram", "começaram", 1),
    ("metodo", "método", 1), ("manda", "manda", 1))}
DESTAQUE = {"explorador", "osso", "colava", "carlo", "mauri", "tíbia", "infeccionou", "pseudartrose", "infectada",
            "rússia", "ilizarov", "foco", "alongado", "dois", "centímetros", "colou", "lecco", "método", "fratura"}

YF, VAO0, ABRE = 760, 20, 58             # foco; vão inicial (tecido, rígido); quanto abre (perto da escala de 2 cm)
Y_AN = (465, 635, 905, 1030)             # dois anéis antes e dois depois do foco
RX, RY = tr.RX2, tr.RY2
FIBRA, INFEC = "#B9788A", "#E5565E"
NEVE, NEVE_S = "#E9F1F8", "#A9BFD4"
UNICO, PROMESSA = "CADA CASO É ÚNICO", "NÃO É PROMESSA DE RESULTADO"


# ------------------------------------------------------------------ osso, anéis e fios
OSSO = skia.Op(path_osso_sup(Y_TOPO, YF + 2), path_osso_inf(YF - 2, Y_BASE), skia.PathOp.kUnion_PathOp)


def metade(cv, regiao):
    cv.save(); cv.clipPath(regiao, skia.ClipOp.kIntersect, True)
    cv.drawPath(OSSO, paint("#000000", 70, blur=14)); cv.drawPath(OSSO, paint(OSSO_C, shader=sombra_osso()))
    cv.drawPath(OSSO, paint(OSSO_L, 150, "stroke", 2.5))
    cv.restore()


def osso(cv, t, vao, fibra=0.0, infec=0.0, novo=0.0, duro=0.0, brilho=0.0):
    """Os dois pedaços e o que existe entre eles. O foco não balança: é rígido."""
    h = HASTE / 2
    if vao > 1:
        y0, y1 = YF - 12, YF + vao + 12
        if novo > 0:
            cv.drawRect(skia.Rect(CX - h + 2, y0, CX + h - 2, y1), paint(tr.AMBAR, int(255 * novo)))
            desenha_regenerado(cv, y0, y1, novo, brilho, duro, t)
        if fibra > 0:
            cv.drawRRect(rr(CX - h - 4, y0, CX + h + 4, y1, 8), paint(FIBRA, int(235 * fibra)))
    metade(cv, _regiao_acima(YF))
    cv.save(); cv.translate(0, vao); metade(cv, _regiao_abaixo(YF)); cv.restore()
    if infec > 0:                                        # calor no foco + pontinhos, sem ferida
        p = .75 + .25 * math.sin(t * 5)
        cv.save(); cv.clipPath(OSSO, skia.ClipOp.kIntersect, True)
        cv.drawOval(skia.Rect(CX - 150, YF - 105, CX + 150, YF + vao + 105), paint(INFEC, int(190 * infec * p), blur=32))
        cv.restore()
        cv.drawOval(skia.Rect(CX - 150, YF - 90, CX + 150, YF + vao + 90), paint(INFEC, int(255 * infec * p), "stroke", 6))
        for i in range(9):
            g = i * 2.4 + .5 * math.sin(t * 1.5 + i)
            d = 34 + (i * 37) % 60
            cv.drawCircle(CX + d * math.cos(g), YF + vao / 2 + d * .62 * math.sin(g), 8, paint("#8E2433", int(255 * infec)))


def fio(cv, y, pr):
    """Dois fios tensionados, cruzados, de borda a borda do anel; apagados onde passam por dentro do osso."""
    if pr <= 0:
        return
    h = HASTE / 2
    for s in (-1, 1):
        g = math.radians(24)
        x0, y0 = CX - RX * math.cos(g), y - s * RY * math.sin(g)
        x1, y1 = CX + RX * math.cos(g), y + s * RY * math.sin(g)
        for a, b, al in ((x0, CX - h, 255), (CX - h, CX + h, 80), (CX + h, x1, 255)):
            fim = min(b, lerp(x0, x1, pr))
            if fim > a:
                ya, yb = (lerp(y0, y1, (v - x0) / (x1 - x0)) for v in (a, fim))
                linha(cv, a, ya, fim, yb, "#DDE6EE" if al == 255 else "#5E6B78", 4, al)
                for v, yv in ((a, ya),) if al != 255 else ():
                    cv.drawCircle(v, yv, 5, paint(ACO_ESC))
        if pr > .98:
            cv.drawCircle(CX + h, lerp(y0, y1, (CX + h - x0) / (x1 - x0)), 5, paint(ACO_ESC))
            for xx, yy in ((x0, y0), (x1, y1)):
                cv.drawCircle(xx, yy, 8, paint(OURO)); cv.drawCircle(xx, yy, 8, paint("#8A6512", 255, "stroke", 2))


def aparelho(cv, d, pr, frente, giro=0.0):
    ys = [Y_AN[0], Y_AN[1], Y_AN[2] + d, Y_AN[3] + d]
    if not frente:
        for i, y in enumerate(ys):
            tr.anel(cv, y, 0, prog(pr, .1 * i, .1 * i + .25), "tras")      # aparece no lugar, já em volta do osso
        return
    for y in ys:
        fio(cv, y, prog(pr, .55, 1))
    a = prog(pr, .5, .8)
    for sx in (-1, 1):
        x = CX + sx * tr.X_HASTE
        haste(cv, x, ys[0], ys[1], a); haste(cv, x, ys[1], ys[2], a, rosca=True); haste(cv, x, ys[2], ys[3], a)
        porca(cv, x, ys[2] - 20, giro, a); porca(cv, x, ys[2] + 20, -giro, a)
    for i, y in enumerate(ys):
        tr.anel(cv, y, 0, prog(pr, .1 * i, .1 * i + .25), "frente")


def no_mundo(cv, cx, cy, s):
    cv.translate(cx, cy); cv.scale(s, s); cv.translate(-CX, -(YF - 25))


def lupa(cv, t, cx, cy, r, s, a, **k):
    """Círculo que mostra o osso por dentro da história."""
    cv.save(); cv.clipPath(skia.Path().addCircle(cx, cy, r), skia.ClipOp.kIntersect, True)
    cv.drawCircle(cx, cy, r, paint("#0D2233", int(255 * a)))
    no_mundo(cv, cx, cy, s); osso(cv, t, VAO0, **k); cv.restore()
    cv.drawCircle(cx, cy, r, paint(OURO, int(255 * a), "stroke", 8))


# ------------------------------------------------------------------ 1) o explorador e o osso
def montanhas(cv):
    for pts, cor in (((60, 1090, 130, 620, 300, 820, 465, 460, 640, 780, 900, 560, 1020, 900, 1020, 1090), "#456C8C"),
                     ((60, 1090, 60, 960, 330, 790, 560, 980, 760, 860, 1020, 1010, 1020, 1090), "#35566F")):
        p = skia.Path(); p.moveTo(pts[0], pts[1])
        for i in range(2, len(pts), 2):
            p.lineTo(pts[i], pts[i + 1])
        p.close(); cv.drawPath(p, paint(cor))
    for x, y, k in ((465, 460, 62),):
        cv.drawPath(caminho([(x, y), (x + k, y + k * 1.83), (x + k * .3, y + k * 1.4), (x - k * .2, y + k * 2),
                             (x - k * .75, y + k * 1.64)]), paint(NEVE))


def explorador(cv, x, y, s, t):
    cv.save(); cv.translate(x, y); cv.scale(s, s)
    caixa(cv, rr(-150, -380, -60, -150, 34), "#8A5F3C", "#5C3D25", 6)       # mochila
    cv.drawRRect(rr(-156, -412, -56, -368, 22), paint(OURO))
    linha(cv, 160, -330, 186, 0, "#C9A26B", 12)                              # bastão
    cv.restore()
    pessoa(cv, x, y, s, braco=(92, 70))


def cena_explorador(cv, t, T):
    a = 1 - prog(t, T["carlo"] - .35, T["carlo"] - .1)
    if a <= 0:
        return
    cv.saveLayerAlpha(None, int(255 * a))
    cv.save(); cv.clipRRect(rr(60, 400, 1020, 1120, 34), skia.ClipOp.kIntersect, True)
    cv.drawRect(skia.Rect(60, 400, 1020, 1120), paint("#16324A"))
    montanhas(cv); cv.drawRect(skia.Rect(60, 1070, 1020, 1120), paint("#27425A"))
    explorador(cv, 270, 1085, .98, t)
    cv.restore()
    cv.drawRRect(rr(60, 400, 1020, 1120, 34), paint(SILH_L, 160, "stroke", 4))
    p = 1 + .05 * math.sin(prog(t, T["osso1"], T["osso1"] + .5) * math.pi)
    lupa(cv, t, 745, 800, 245 * p, .78 * p, 1, fibra=1)
    cv.restore()
    b = janela(t, T["osso1"] - .05, T["carlo"] - .35)
    chip(cv, "NÃO COLAVA", 745, 1180, CORAL, b, 46)


# ------------------------------------------------------------------ 2) a queda na neve
def esquiador(cv, x, y, rot, cor, borda, s=1.0):
    """Silhueta genérica: capacete, tronco inclinado, joelhos dobrados, esquis e bastão."""
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(s, s)
    for c, d in ((borda, 10), (cor, 0)):
        linha(cv, -125, 4, 120, 4, c, 12 + d); linha(cv, 120, 4, 146, -14, c, 12 + d)          # esqui
        for pts in (((0, -6), (34, -72), (-24, -124)), ((-24, -124), (36, -222)), ((24, -205), (84, -160), (112, -178))):
            for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
                linha(cv, xa, ya, xb, yb, c, (46 if len(pts) == 2 else 32) + d)
        linha(cv, 112, -184, 60, -20, c, 6 + d * .5)                                            # bastão
        cv.drawCircle(64, -268, 36 + d / 2, paint(c))
    cv.restore()


def cena_neve(cv, t, T):
    a = janela(t, T["carlo"] - .2, T["osso2"] - .35)
    if a <= 0:
        return
    cv.saveLayerAlpha(None, int(255 * a))
    cv.save(); cv.clipRRect(rr(60, 400, 1020, 1120, 34), skia.ClipOp.kIntersect, True)
    cv.drawRect(skia.Rect(60, 400, 1020, 1120), paint("#3D6A91"))
    cv.drawPath(caminho([(60, 700), (230, 520), (400, 660), (640, 470), (1020, 760), (1020, 1120), (60, 1120)]), paint("#6F93B3"))
    cv.drawPath(caminho([(60, 720), (1020, 1010), (1020, 1120), (60, 1120)]), paint(NEVE))
    linha(cv, 60, 722, 1020, 1012, NEVE_S, 8)
    inc = 16.8                                           # inclinação da encosta
    u = e_inout(prog(t, T["carlo"] - .2, T["quebrou"] + .1))
    x = lerp(230, 520, u); v = lerp(-180, 330, e_inout(prog(t, T["carlo"], T["quebrou"] + .1)))
    bate = prog(t, T["quebrou"] + .05, T["quebrou"] + .45)
    ny = lambda xx: 720 + (xx - 60) * .302
    esquiador(cv, v, ny(v) - 4, inc - 14 * bate, "#7A8794", "#E4EAF0")          # o outro esquiador
    esquiador(cv, x + 40 * bate, ny(x + 40 * bate) - 4, inc + 68 * e_out(bate), SILH, OURO)
    k = prog(t, T["quebrou"] + .05, T["quebrou"] + .5)
    if 0 < k < 1:
        for i in range(10):
            g = i * math.tau / 10
            linha(cv, 470 + 60 * math.cos(g), 760 + 60 * math.sin(g), 470 + (60 + 110 * k) * math.cos(g),
                  760 + (60 + 110 * k) * math.sin(g), "#FFFFFF", 12, int(255 * (1 - k)))
    cv.restore()
    cv.drawRRect(rr(60, 400, 1020, 1120, 34), paint(SILH_L, 160, "stroke", 4))
    b = e_back(prog(t, T["tibia"] - .15, T["tibia"] + .25))
    if b > 0.02:
        lupa(cv, t, 790, 605, 185 * b, .56 * b, 1)
    cv.restore()
    chip(cv, "CARLO MAURI", 540, 1170, OURO, janela(t, T["carlo"], T["tibia"] - .25), 56)
    chip(cv, "TÍBIA QUEBRADA", 540, 1170, CORAL, janela(t, T["tibia"], T["osso2"] - .4), 52)


# ------------------------------------------------------------------ 3) não colou, infeccionou
def cena_pseudo(cv, t, T):
    a = janela(t, T["osso2"] - .2, T["mil1"] - .3)
    if a <= 0:
        return
    cv.saveLayerAlpha(None, int(255 * a))
    z = e_inout(prog(t, T["osso2"] - .2, T["mil1"]))
    cv.save(); no_mundo(cv, 540, 705, lerp(.67, .70, z))
    osso(cv, t, VAO0, fibra=prog(t, T["osso2"], T["colou1"]), infec=prog(t, T["infec"] - .1, T["infec"] + .3))
    cv.restore(); cv.restore()
    p = janela(t, T["colou1"] - .1, T["nome"] - .3)
    if p > 0:
        chip(cv, "NÃO COLOU", 825, 660, "#FFFFFF", p, 46, CORAL)
        linha(cv, 715, 682, 600, 742, CORAL, 6, int(255 * p))
    chip(cv, "INFECCIONOU", 540, 1190, CORAL, janela(t, T["infec"], T["nome"] - .2), 56)
    chip(cv, "O OSSO NÃO COLA", 540, 1172, "#FFFFFF", janela(t, T["nome"] + .1, T["pseudo"] - .25), 48, OURO)
    q = janela(t, T["pseudo"] - .05, T["mil1"] - .3)
    if q > 0:
        e = lerp(1.35, 1, e_out(prog(t, T["pseudo"] - .05, T["pseudo"] + .2)))
        chip(cv, "PSEUDARTROSE", 540, 1132, OURO, q, 66, esc=e)
    chip(cv, "INFECTADA", 540, 1225, CORAL, janela(t, T["infectada"] - .05, T["mil1"] - .3), 56)


# ------------------------------------------------------------------ 4) a viagem e o médico
def globo_rota(cv, t, u, volta=False):
    """Mapa esquemático: grade, dois pontos, uma rota. Sem contorno de país."""
    caixa(cv, rr(80, 420, 1000, 1080, 34), "#12304A", SILH_L, 4)
    cv.save(); cv.clipRRect(rr(80, 420, 1000, 1080, 34), skia.ClipOp.kIntersect, True)
    for i in range(1, 6):
        cv.drawArc(skia.Rect(-200, 420 + 110 * i, 1280, 820 + 110 * i), 180, 180, False, paint(SILH_L, 45, "stroke", 3))
        linha(cv, 80 + 155 * i, 420, 80 + 155 * i, 1080, SILH_L, 3, 45)
    A, B, K = (245, 930), (835, 640), (520, 480)
    q = lambda v: tuple((1 - v) ** 2 * A[i] + 2 * v * (1 - v) * K[i] + v * v * B[i] for i in (0, 1))
    n = 40
    for i in range(n):
        if i % 2 == 0:
            p0, p1 = q(i / n), q((i + 1) / n)
            linha(cv, *p0, *p1, OURO if i / n <= u else SILH_L, 9, 255 if i / n <= u else 110)
    for (x, y), cor in ((A, "#8FD3A5"), (B, CORAL)):
        cv.drawCircle(x, y, 22, paint(cor)); cv.drawCircle(x, y, 22, paint("#FFFFFF", 255, "stroke", 5))
    x, y = q(u)
    cv.drawCircle(x, y, 38, paint(OURO, 110, blur=12))
    pessoa(cv, x, y - 4, .26)
    cv.restore()
    chip(cv, "ITÁLIA", 245, 1020, "#FFFFFF", 1, 42, "#8FD3A5")
    chip(cv, "RÚSSIA", 835, 735, "#FFFFFF", 1, 42, CORAL)


def anel_icone(cv, x, y, s):
    """O aparelho genérico: dois anéis e hastes, pequeno."""
    for yy in (-60, 60):
        cv.drawOval(skia.Rect(x - 70 * s, y + (yy - 20) * s, x + 70 * s, y + (yy + 20) * s), paint(ACO, 255, "stroke", 11 * s))
    for dx in (-58, 0, 58):
        linha(cv, x + dx * s, y - 50 * s, x + dx * s, y + 68 * s, "#8FA3B8", 8 * s)


def medico(cv, x, y, s):
    """A mesma silhueta sem rosto, de jaleco claro."""
    a = byron.SILH, byron.SILH_L
    byron.SILH, byron.SILH_L = "#C3D0DC", "#4A5E72"
    try:
        pessoa(cv, x, y, s)
    finally:
        byron.SILH, byron.SILH_L = a


def cena_viagem(cv, t, T):
    a = janela(t, T["mil1"] - .2, T["doutor"] - .3)
    if a > 0:
        cv.saveLayerAlpha(None, int(255 * a))
        globo_rota(cv, t, e_inout(prog(t, T["foi"], T["doutor"] - .35)))
        cv.restore()
    a = janela(t, T["doutor"] - .2, T["aparelho"] - .45)
    if a > 0:
        cv.saveLayerAlpha(None, int(255 * a))
        linha(cv, 90, 1084, 990, 1084, SILH_L, 5, 120)
        linha(cv, 160, 740, 160, 1080, "#C9A26B", 14); linha(cv, 128, 740, 192, 740, "#C9A26B", 16)   # muleta
        pessoa(cv, 320, 1080, 1.1)
        medico(cv, 760, 1080, 1.1)
        cv.drawCircle(540, 770, 118, paint("#0D2233")); cv.drawCircle(540, 770, 118, paint(OURO, 255, "stroke", 6))
        anel_icone(cv, 540, 766, .95)
        cv.restore()
        chip(cv, "DR. ILIZAROV", 760, 1180, OURO, a, 52)


# ------------------------------------------------------------------ 5) o foco aberto aos poucos
N_PASSOS = 20


def abertura(t, T):
    k = prog(t, T["alongado"] - .1, T["cm"] + .5) * N_PASSOS
    i = math.floor(k)
    return ABRE if i >= N_PASSOS else ABRE * (i + e_inout(clamp((k - i) / .5))) / N_PASSOS


OS_CX = 400


def cena_foco(cv, t, T):
    a = janela(t, T["aparelho"] - .22, T["contou"] - .3)
    if a <= 0:
        return
    d = abertura(t, T); u = d / ABRE
    s, cy = .70, 660
    pr = prog(t, T["aparelho"] - .1, T["foco"] + .1)
    novo = .95 * clamp(u * 1.6)
    colou = e_inout(prog(t, T["osso3"] - .05, T["colou2"] + .4))
    cv.saveLayerAlpha(None, int(255 * a))
    cv.save(); no_mundo(cv, OS_CX, cy, s)
    aparelho(cv, d, pr, False)
    osso(cv, t, VAO0 + d, fibra=1 - clamp(u * 2.2), infec=.55 * (1 - colou),
         novo=novo, duro=.6 * colou, brilho=.5 * (1 - colou))
    aparelho(cv, d, pr, True, d * 4)
    brilhos(cv, CX, YF + (VAO0 + d) / 2, t, T["colou2"] + .05, n=12, raio=170)
    cv.restore()
    # o foco, apontado; depois as setas e a medida
    ya, yb = cy + 25 * s, cy + (25 + VAO0 + d) * s
    b = janela(t, T["foco"] - .05, T["dois"] - .25) * (1 - prog(t, T["osso3"], T["osso3"] + .2))
    if b > 0:
        linha(cv, 630, (ya + yb) / 2, 470, (ya + yb) / 2, OURO, 6, int(255 * b))
        ponta(cv, 462, (ya + yb) / 2, math.pi, 26, OURO, b)
        chip(cv, "O FOCO", 735, (ya + yb) / 2 + 16, OURO, b, 46)
    c = janela(t, T["dois"] - .1, T["contou"] - .3)
    if c > 0:
        x, ym = 575, yb - d * s                          # a medida é só o que abriu
        for yy in (ym, yb):
            linha(cv, x - 20, yy, x + 20, yy, OURO, 6, int(255 * c))
        linha(cv, x, ym, x, yb, OURO, 6, int(255 * c))
        chip(cv, "2 CM", 715, (ya + yb) / 2 + 22, OURO, c, 60)
    cv.restore()
    chip(cv, "AOS POUCOS", 775, 470, "#FFFFFF", janela(t, T["poucos"] - .25, T["osso3"] - .2), 46, OURO)
    chip(cv, "OSSO NOVO", 775, 560, OURO, janela(t, T["poucos"] + .25, T["contou"] - .35), 46)
    chip(cv, "COLOU", 775, 470, "#8FD3A5", janela(t, T["colou2"] - .05, T["contou"] - .35), 56)
    chip(cv, UNICO, 540, 1140, "#FFFFFF", janela(t, T["dois"] - .1, T["contou"] - .35), 46, OURO)
    chip(cv, PROMESSA, 540, 1226, "#FFFFFF", janela(t, T["cm"], T["contou"] - .35), 46, OURO)


# ------------------------------------------------------------------ 6) a volta: Lecco
def hospital(cv, acende):
    caixa(cv, rr(250, 560, 830, 1080, 12), "#33536E", SILH_L, 6)
    caixa(cv, rr(440, 470, 640, 570, 12), "#33536E", SILH_L, 6)
    for dx, dy in ((24, 8), (8, 24)):
        cv.drawRect(skia.Rect(540 - dx * 1.4, 520 - dy * 1.4, 540 + dx * 1.4, 520 + dy * 1.4), paint("#8FD3A5"))
    for i in range(2):
        for j in range(3):
            x, y = (330, 750)[i], 620 + 110 * j
            cv.drawRRect(rr(x - 40, y, x + 40, y + 70, 8), paint("#12304A" if acende <= 0 else OURO, 255 if acende <= 0 else int(90 + 130 * acende)))
    cv.drawRRect(rr(485, 930, 595, 1080, 10), paint("#12304A"))
    cv.drawCircle(540, 750, 125, paint("#0D2233")); cv.drawCircle(540, 750, 125, paint(OURO, int(255 * acende), "stroke", 7))


def cena_lecco(cv, t, T):
    a = janela(t, T["contou"] - .2, T["mil2"] - .35)
    if a > 0:
        cv.saveLayerAlpha(None, int(255 * a))
        linha(cv, 90, 1084, 990, 1084, SILH_L, 5, 120)
        pessoa(cv, 270, 1080, 1.0)
        for x in (620, 780, 930):
            medico(cv, x, 1080, .78)
        b = e_back(prog(t, T["contou"] - .1, T["contou"] + .3))
        cv.save(); cv.translate(380, 600); cv.scale(b, b); cv.translate(-380, -600)
        cv.drawPath(caminho([(400, 590), (330, 670), (470, 610)]), paint(PAPEL))
        cv.drawRRect(rr(360, 400, 620, 620, 40), paint(PAPEL))
        anel_icone(cv, 490, 506, .85)
        cv.restore(); cv.restore()
        chip(cv, "CARLO MAURI", 250, 1180, OURO, a, 42)
        chip(cv, "MÉDICOS DE LECCO", 750, 1180, "#FFFFFF", a, 42, SILH_L)
    a = janela(t, T["mil2"] - .2, T["manda"] - .4)
    if a > 0:
        cv.saveLayerAlpha(None, int(255 * a))
        linha(cv, 90, 1084, 990, 1084, SILH_L, 5, 120)
        ac = prog(t, T["comecaram"] - .1, T["comecaram"] + .4)
        hospital(cv, ac)
        e = e_back(prog(t, T["eles"] - .2, T["eles"] + .3))
        if e > .02:
            anel_icone(cv, 540, 746, e)
        cv.restore()
        chip(cv, "HOSPITAL DE LECCO", 540, 1190, "#FFFFFF", janela(t, T["mil2"], T["eles"] - .25), 46, SILH_L)
        chip(cv, "PASSOU A USAR O MÉTODO", 540, 1190, OURO, janela(t, T["eles"], T["manda"] - .4), 46)


# ------------------------------------------------------------------ quadro
def faixa_epoca(cv, t, T):
    for s, t0, t1 in (("NO PASSADO", T["carlo"] - .1, T["mil1"] - .35), ("1980", T["mil1"] - .1, T["osso3"] - .15),
                      ("NA VOLTA", T["volta"] - .1, T["mil2"] - .35), ("1981", T["mil2"] - .1, T["manda"] - .45)):
        chip(cv, s, 540, 300, PAPEL, janela(t, t0, t1, .2, .2), 46)


FONTE_DEPOIS = .9
FONTE1, FONTE2 = "Desenho ilustrativo: não é exame", "Fonte: Paley Institute"


def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    for cena in (cena_explorador, cena_neve, cena_pseudo, cena_viagem, cena_foco, cena_lecco):
        cena(cv, t, T)
    faixa_epoca(cv, t, T)
    t_sai = T["carlo"] - .65
    capa(cv, t, t_sai, *ep["gancho"])
    a = prog(t, t_sai + .5, t_sai + .9) * (1 - prog(t, T["manda"] - .3, T["manda"]))
    if a > 0:
        cv.drawRRect(rr(330, 150, 750, 204, 27), paint("#FFFFFF", int(28 * a)))
        texto(cv, "HISTÓRIA NO OSSO", 540, 190, F_BLACK, 32, OURO, int(255 * a))
    interface(cv, t, T, blocos, DESTAQUE)
    a = prog(t, T["manda"] + .1, T["manda"] + .4)
    chip(cv, "HOJE", 540, 240, OURO, a, 46)
    chip(cv, UNICO, 540, 340, "#FFFFFF", a, 46, OURO)
    chip(cv, PROMESSA, 540, 430, "#FFFFFF", a, 46, OURO)
    a = prog(t, T["manda"] + FONTE_DEPOIS, T["manda"] + FONTE_DEPOIS + .3)
    if a > 0:
        texto(cv, FONTE1, 540, 1276, F_BLACK, 34, "#FFFFFF", int(255 * a), contorno=6)
        texto(cv, FONTE2, 540, 1324, F_BLACK, 34, "#9CC9FF", int(255 * a), contorno=6)


def sons(T):
    ev = [(T["explorador"], "pop", .4), (T["osso1"], "shimmer", .35), (T["carlo"] - .1, "whoosh", .4),
          (T["quebrou"] + .1, "thump", .8), (T["tibia"], "pop", .5), (T["colou1"], "pop", .45),
          (T["infec"], "thump", .5), (T["pseudo"], "thump", .6), (T["infectada"], "pop", .45),
          (T["foi"], "whoosh", .35), (T["iliz"], "pop", .5), (T["aparelho"], "whoosh", .4),
          (T["foco"], "pop", .4), (T["dois"], "pop", .45), (T["colou2"], "shimmer", .45),
          (T["contou"], "pop", .45), (T["mil2"], "whoosh", .3), (T["comecaram"], "ping", .45)]
    t0, t1 = T["alongado"] - .1, T["cm"] + .5
    ev += [(t0 + (t1 - t0) * i / 10, "tick", .3) for i in range(10)]
    return ev + [(T["manda"] + .05, "whoosh", .5)]


def tempos_previa(T):
    return (0.0, T["colava"], T["quebrou"] + .15, T["esquiando"] + .3, T["infec"] + .4, T["infectada"] + .5,
            T["russia"], T["iliz"] + .5, T["foco"] + .1, T["poucos"] + .4, T["cm"] + .3, T["colou2"] + .5,
            T["lecco"] + .1, T["eles"] - .1, T["metodo"] + .3, T["manda"] + 1.7)


render = fazer_render(quadro, ANCORAS, sons, tempos_previa, respiro_cta=1.8)
