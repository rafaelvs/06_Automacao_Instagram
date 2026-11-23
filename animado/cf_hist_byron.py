# -*- coding: utf-8 -*-
"""HISTÓRIA NO OSSO — Lord Byron ("UM POETA FAMOSO, / UM PÉ DIFERENTE").

Regras da cena:
  * Nenhum retrato: pessoas são silhuetas genéricas, sem rosto. Nenhum osso por dentro, nenhum exame.
  * O diagnóstico de Byron é DISCUTIDO: o pé dele só aparece visto de cima, virado pra dentro (o que a
    mãe descreveu). O desenho do pé torto do bebê (cf_pe_torto) só entra em HOJE, depois do rótulo.
    "PÉ TORTO" é carimbo dos médicos da época e ganha um "?" que fica; a etiqueta "PÉ TORTO?
    AINDA SE DISCUTE" acompanha o resto do passado.
  * Passado × presente por rótulo: NO PASSADO / 1791 / HOJE.
  * Aparelho antigo é esquemático; ele é posto de lado, sem zombaria. O nado cruza de margem a margem.
  * HOJE reaproveita cf_pe_torto: manipulação DESTORCE, gessos seguram, o "pra baixo" sai por último.
    Sem "depois", sem brilho de sucesso. Fonte na tela na órtese e no cartão final.
"""
import math

import skia

from . import cf_pe_torto as pt
from .cf_alongamento import F_BLACK, OURO, W, C, clamp, e_back, e_inout, e_out, fundo, lerp, paint, prog, texto
from .cf_comum import capa, fazer_render, interface
from .cf_pe_torto import CORAL, PELE, PELE_CL, PELE_LINHA, chip, chip_janela, ponta, seta_pts

ANCORAS = {k: (p, n, False) for k, p, n in (
    ("nasceu", "nasceu", 1), ("diferente", "diferente", 1), ("virou", "virou", 1), ("poetas", "poetas", 1),
    ("lord", "lord", 1), ("mae", "mãe", 1), ("direito", "direito", 1), ("vira", "vira", 1),
    ("dentro", "dentro", 1), ("medicos", "médicos", 1), ("torto1", "torto", 1), ("ate", "até", 1),
    ("discute", "discute", 1), ("trat", "tratamentos", 1), ("doiam", "doíam", 1),
    ("aparelho", "aparelho", 1), ("recusou", "recusou", 1), ("usar", "usar", 1), ("mesmo", "mesmo", 1),
    ("estreito", "estreito", 1), ("nado", "nado", 1), ("hoje", "hoje", 2), ("manip", "manipulação", 1),
    ("gessos", "gessos", 1), ("desde", "desde", 1), ("primeiras", "primeiras", 1), ("depois", "depois", 1),
    ("ortese", "órtese", 1), ("manter", "manter", 1), ("manda", "manda", 1))}
DESTAQUE = {"diferente", "poetas", "famosos", "byron", "mãe", "direito", "dentro", "médicos", "discute",
            "doíam", "recusou", "estreito", "nado", "manipulação", "suave", "gessos", "primeiras",
            "semanas", "órtese", "manter"}

PAPEL, PAPEL_B, TINTA = "#F0E2C0", "#D2BB8A", "#4A3522"
SILH, SILH_L = "#405E7C", "#9DB4CB"
COURO, COURO_E, FERRO, FERRO_E = "#8A5F3C", "#5C3D25", "#B8C2CC", "#5E6B78"


# ------------------------------------------------------------------ ajudas
def janela(t, a, b, ent=0.25, sai=0.25):
    return e_out(prog(t, a, a + ent)) * (1 - prog(t, b, b + sai))


def rr(x0, y0, x1, y1, r):
    return skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), r, r)


def caminho(pts, fechado=True):
    """[(x, y) início, depois (x, y) = reta ou (c1, c2, p) = curva]."""
    p = skia.Path(); p.moveTo(*pts[0])
    for s in pts[1:]:
        if len(s) == 2:
            p.lineTo(*s)
        else:
            p.cubicTo(*s[0], *s[1], *s[2])
    if fechado:
        p.close()
    return p


def forma(cv, p, cheio, borda, w=5):
    cv.drawPath(p, paint(cheio)); cv.drawPath(p, paint(borda, 255, "stroke", w))


def caixa(cv, r, cheio, borda, w=5):
    cv.drawRRect(r, paint(cheio)); cv.drawRRect(r, paint(borda, 255, "stroke", w))


def linha(cv, x0, y0, x1, y1, cor, w, a=255):
    cv.drawLine(x0, y0, x1, y1, paint(cor, a, "stroke", w))


# ------------------------------------------------------------------ pés vistos de cima (dedos para cima)
def pe_cima(cv, x, y, lado, rot, esc=1.0, ink=False):
    """lado = +1 pé direito (o dedão fica do lado esquerdo), -1 pé esquerdo. Gira em volta do calcanhar."""
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(esc * lado, esc)
    pe = caminho([(-40, 20), ((-58, -60), (-66, -140), (-72, -200)), ((-74, -246), (60, -246), (70, -186)),
                  ((76, -120), (52, -60), (44, 20)), ((40, 66), (-34, 66), (-40, 20))])
    cv.drawPath(pe, paint("#000000", 70, blur=10))
    for dx, dy, r in ((-46, -240, 27), (-6, -249, 19), (23, -242, 17), (46, -228, 15), (64, -208, 13)):
        cv.drawCircle(dx, dy, r, paint(PELE_CL)); cv.drawCircle(dx, dy, r, paint(PELE_LINHA, 255, "stroke", 4))
        cv.drawOval(skia.Rect(dx - r * .45, dy - r * .85, dx + r * .45, dy - r * .2), paint("#FFE6DA", 200))
    forma(cv, pe, PELE, PELE_LINHA, 4)
    cv.restore()


def manta(cv):
    """Manta de bebê cobrindo as perninhas: só os dois pés ficam de fora."""
    m = caminho([(150, 1180), ((130, 1000), (200, 890), (330, 880)), ((420, 872), (470, 918), (540, 918)),
                 ((610, 918), (660, 872), (750, 880)), ((880, 890), (950, 1000), (930, 1180)),
                 ((900, 1240), (180, 1240), (150, 1180))])
    cv.drawPath(m, paint("#000000", 80, blur=14)); cv.drawPath(m, paint("#E9DDC6"))
    cv.save(); cv.clipPath(m, skia.ClipOp.kIntersect, True)
    for i in range(-2, 12):
        linha(cv, 100 + 90 * i, 860, 40 + 90 * i, 1250, "#CDBB98", 8)
    for x, y in ((280, 1010), (440, 1090), (600, 1010), (760, 1090), (850, 990)):
        cv.drawCircle(x, y, 14, paint(OURO, 190))
    cv.restore()
    cv.drawPath(m, paint("#B7A688", 255, "stroke", 5))


# ------------------------------------------------------------------ silhueta genérica (sem rosto)
def pessoa(cv, x, y, esc=1.0, cartola=False, braco=None):
    """y = chão. braco = (dx, dy) da mão a partir do ombro direito da tela, ou None."""
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    corpo = caminho([(-78, 0), (-84, -150), ((-120, -240), (-120, -330), (-84, -366)),
                     ((-50, -392), (50, -392), (84, -366)), ((120, -330), (120, -240), (84, -150)), (78, 0),
                     (14, 0), (8, -140), (-8, -140), (-14, 0)])
    if braco:
        for cor, w in ((SILH_L, 62), (SILH, 52)):
            linha(cv, 66, -325, 66 + braco[0], -325 + braco[1], cor, w)
    partes = [rr(-24, -410, 24, -360, 10)]
    if cartola:
        partes += [rr(-50, -590, 50, -490, 12), rr(-84, -506, 84, -484, 10)]
    for p in (paint(SILH_L, 255, "stroke", 10), paint(SILH)):
        cv.drawPath(corpo, p); cv.drawCircle(0, -450, 58, p)
        for r in partes:
            cv.drawRRect(r, p)
    cv.drawPath(caminho([(-30, -372), (0, -290), (30, -372)], False), paint(SILH_L, 200, "stroke", 5))
    linha(cv, 0, -290, 0, -150, SILH_L, 4, 150)
    cv.restore()


def maleta(cv, x, y):
    cv.drawArc(skia.Rect(x - 28, y - 116, x + 28, y - 56), 180, 180, False, paint(COURO_E, 255, "stroke", 9))
    caixa(cv, rr(x - 62, y - 84, x + 62, y, 14), COURO, COURO_E)
    linha(cv, x, y - 60, x, y - 24, PAPEL, 10); linha(cv, x - 18, y - 42, x + 18, y - 42, PAPEL, 10)


# ------------------------------------------------------------------ 1) pé diferente -> livro e pena
def cena_nasceu(cv, t, T):
    a = 1 - prog(t, T["virou"] - 0.15, T["virou"] + 0.15)
    if a <= 0:
        return
    cv.saveLayerAlpha(None, int(255 * a))
    mexe = 2.5 * math.sin(t * 5)
    pe_cima(cv, 310, 890, -1, -4 + mexe, 1.3)
    u = e_back(prog(t, T["nasceu"], T["diferente"] + 0.2))
    pe_cima(cv, 780, 890, 1, lerp(-12, -38, u) - mexe, 1.3)
    manta(cv)
    b = prog(t, T["diferente"], T["diferente"] + 0.2)
    if b > 0:                                             # um anel chama o olhar, sem julgamento
        r = skia.Rect(505, 530, 875, 910)
        cv.drawOval(r, paint(OURO, int(120 * b), "stroke", 16, blur=10)); cv.drawOval(r, paint(OURO, int(255 * b), "stroke", 6))
    cv.restore()


def pena(cv, x, y, rot):
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(.72, .72)
    forma(cv, caminho([(0, 0), ((20, -60), (10, -110), (30, -160)), ((50, -230), (90, -290), (150, -330)),
                       ((150, -240), (120, -160), (70, -110)), ((50, -90), (30, -50), (0, 0))]), "#FFFFFF", SILH_L, 4)
    cv.drawPath(caminho([(0, 0), ((30, -90), (70, -200), (140, -310))], False), paint(SILH_L, 255, "stroke", 4))
    cv.restore()


def cena_poeta(cv, t, T):
    a = janela(t, T["virou"] - 0.1, T["lord"] - 0.2)
    if a <= 0:
        return
    cv.saveLayerAlpha(None, int(255 * a))
    cv.drawRRect(rr(140, 580, 940, 1060, 22), paint(COURO_E))
    for s in (-1, 1):
        forma(cv, caminho([(540, 610), ((540 + s * 90, 560), (540 + s * 250, 560), (540 + s * 370, 590)),
                           (540 + s * 370, 1020), ((540 + s * 250, 990), (540 + s * 90, 990), (540, 1040))]),
              PAPEL, PAPEL_B, 4)
    total = prog(t, T["virou"], T["lord"] - 0.35) * 12    # versos: linhas curtas, em estrofes
    px, py = 220, 665
    for i in range(12):
        u = clamp(total - i)
        col, lin = divmod(i, 6)
        x0 = 220 + col * 380; y0 = 665 + lin * 48 + (26 if lin >= 3 else 0)
        if u > 0:
            px, py = x0 + (240, 200, 260, 220, 250, 180)[lin] * u, y0
            linha(cv, x0, y0, px, y0, TINTA, 8)
    pena(cv, px, py, 4 * math.sin(t * 14))
    cv.restore()
    chip(cv, "POETA", 540, 1170, OURO, a, 50)


def cena_byron(cv, t, T):
    a = janela(t, T["lord"] - 0.15, T["mae"] - 0.3)
    if a <= 0:
        return
    cv.saveLayerAlpha(None, int(255 * a))
    cv.drawCircle(540, 720, 330, paint(OURO, 28)); cv.drawCircle(540, 720, 330, paint(OURO, 140, "stroke", 5))
    pessoa(cv, 540, 1040, 1.22)
    caixa(cv, rr(600, 760, 700, 880, 8), COURO, PAPEL)     # o livro na mão
    cv.restore()
    chip(cv, "LORD BYRON", 540, 1160, OURO, a, 60, esc=lerp(0.8, 1, e_back(prog(t, T["lord"], T["lord"] + .35))))


# ------------------------------------------------------------------ 2) a carta
def cena_carta(cv, t, T):
    a = janela(t, T["mae"] - 0.2, T["medicos"] - 0.3)
    if a <= 0:
        return
    cv.saveLayerAlpha(None, int(255 * a))
    cv.translate(540, 780); cv.rotate(lerp(-9, -2, e_out(prog(t, T["mae"] - .2, T["mae"] + .5)))); cv.translate(-540, -780)
    cv.drawRRect(rr(150, 380, 930, 1230, 12), paint("#000000", 110, blur=18))
    caixa(cv, rr(145, 372, 925, 1222, 10), PAPEL, PAPEL_B, 6)
    texto(cv, "CARTA DA MÃE", 200, 452, F_BLACK, 50, TINTA, centro=False)
    u = prog(t, T["mae"], T["direito"])
    for i, comp in enumerate((640, 560, 330)):            # letra de mão: rabisco, nada legível
        k = clamp(u * 3 - i)
        if k > 0:
            p = skia.Path(); n = int(70 * k) + 1
            for j in range(n + 1):
                x = 205 + comp * j / 70
                y = 515 + i * 46 + 9 * math.sin(j * 1.9 + i) * (0.4 + 0.6 * abs(math.sin(j * .33)))
                p.moveTo(x, y) if j == 0 else p.lineTo(x, y)
            cv.drawPath(p, paint(TINTA, 220, "stroke", 4))
    b = prog(t, T["direito"] - 0.45, T["direito"] - 0.1)
    if b > 0:
        cv.saveLayerAlpha(None, int(255 * b))
        g = e_inout(prog(t, T["vira"], T["dentro"] + 0.2))
        pe_cima(cv, 350, 1065, -1, 0, 1.1)
        pe_cima(cv, 720, 1065, 1, lerp(-3, -38, g), 1.1)
        c = prog(t, T["vira"], T["vira"] + 0.2)
        if c > 0:                                         # seta arqueada, de fora para dentro
            fim = lerp(-62, -108, e_out(prog(t, T["vira"], T["dentro"] + .2)))
            pts = [(720 + 355 * math.cos(g_), 1065 + 355 * math.sin(g_))
                   for g_ in (math.radians(lerp(-60, fim, i / 20)) for i in range(21))]
            seta_pts(cv, pts, "#D1492E", c, larg=11, tam=34, brilho=30)
        cv.restore()
    cv.restore()
    chip(cv, "PÉ DIREITO", 730, 1194, "#FFFFFF", janela(t, T["direito"] - .1, T["medicos"] - .3), 42, OURO)
    chip(cv, "PRA DENTRO", 750, 664, CORAL, janela(t, T["dentro"] - .15, T["medicos"] - .3), 40)


# ------------------------------------------------------------------ 3) médicos, carimbo e "?"
def cena_medicos(cv, t, T):
    a = janela(t, T["medicos"] - 0.2, T["trat"] - 0.35)
    if a <= 0:
        return
    cv.saveLayerAlpha(None, int(255 * a))
    linha(cv, 90, 1084, 990, 1084, SILH_L, 5, 120)
    d = 60 * (1 - e_out(prog(t, T["medicos"] - .2, T["medicos"] + .4)))
    for s in (-1, 1):
        pessoa(cv, 540 + s * (320 + d), 1080, 0.95, cartola=True)
        maleta(cv, 540 + s * (140 + d), 1080)
    cv.restore()
    chip(cv, "MÉDICOS DA ÉPOCA", 540, 1190, "#FFFFFF", a, 44, SILH_L)
    b = janela(t, T["torto1"] - .15, T["trat"] - .35)
    if b > 0:
        esc = lerp(1.6, 1, e_out(prog(t, T["torto1"] - .15, T["torto1"] + .1)))
        f = skia.Font(F_BLACK, 50); lw = f.measureText("PÉ TORTO")
        cv.save(); cv.translate(540, 700); cv.rotate(-4); cv.scale(esc, esc)
        r = rr(-lw / 2 - 24, -58, lw / 2 + 24, 24, 12)
        cv.drawRRect(r, paint(PAPEL, int(255 * b))); cv.drawRRect(r, paint(TINTA, int(255 * b), "stroke", 6))
        cv.drawString("PÉ TORTO", -lw / 2, 2, f, paint(TINTA, int(255 * b)))
        cv.restore()
    q = janela(t, T["ate"] - .05, T["trat"] - .35)
    if q > 0:
        s = lerp(.4, 1, e_back(prog(t, T["ate"] - .05, T["ate"] + .35))) * (1 + .04 * math.sin(t * 6))
        cv.save(); cv.translate(540, 860); cv.scale(s, s)
        texto(cv, "?", 0, 70, F_BLACK, 220, OURO, int(255 * q), contorno=14)
        cv.restore()


# ------------------------------------------------------------------ 4) tratamento que doía / aparelho posto de lado
def raio(cv, x, y, rot, s, a):
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(s, s)
    z = caminho([(-10, -50), (16, -50), (2, -10), (24, -10), (-16, 56), (-4, 6), (-24, 6)])
    cv.drawPath(z, paint(CORAL, int(120 * a), blur=10)); cv.drawPath(z, paint(CORAL, int(255 * a)))
    cv.restore()


def cena_tratamento(cv, t, T):
    a = janela(t, T["trat"] - .25, T["aparelho"] - .25)
    if a <= 0:
        return
    cv.saveLayerAlpha(None, int(255 * a))
    pe = caminho([(430, 440), ((428, 580), (440, 690), (430, 800)), ((410, 900), (400, 1000), (480, 1010)),
                  ((600, 1024), (740, 1024), (830, 1012)), ((890, 1000), (880, 945), (810, 925)),
                  ((730, 900), (660, 860), (635, 775)), ((618, 690), (630, 560), (635, 440))])
    forma(cv, pe, SILH, SILH_L, 6)
    cv.save(); cv.clipPath(pe, skia.ClipOp.kIntersect, True)   # faixas apertadas, sem modelo de aparelho
    for x0, y0, x1, y1 in ((360, 600, 720, 580), (360, 720, 720, 700), (380, 930, 690, 790), (560, 1050, 680, 830),
                           (720, 1060, 770, 880)):
        linha(cv, x0, y0, x1, y1, TINTA, 50); linha(cv, x0, y0, x1, y1, PAPEL, 42)
    cv.restore()
    cv.drawPath(pe, paint(SILH_L, 255, "stroke", 6))
    cv.restore()
    for i, (x, y, r) in enumerate(((330, 640, -25), (310, 880, -10), (750, 690, 25), (930, 860, 30))):
        k = prog(t, T["doiam"] - .05 + .08 * i, T["doiam"] + .12 + .08 * i)
        if k > 0:
            raio(cv, x, y, r, 1.35 * (1 + .12 * math.sin(t * 11 + i)), k * a)
    chip(cv, "DOÍA", 540, 1170, CORAL, janela(t, T["doiam"], T["aparelho"] - .25), 58)


def aparelho(cv, x, y, s, a=255):
    """Aparelho antigo, vazio: bota de couro, duas hastes de ferro, tiras."""
    cv.save(); cv.translate(x, y); cv.scale(s, s)
    cv.saveLayerAlpha(None, a)
    for dx in (-96, 96):
        linha(cv, dx, -470, dx, -20, FERRO_E, 22); linha(cv, dx, -470, dx, -20, FERRO, 14)
    forma(cv, caminho([(-80, -230), (80, -230), (84, -90), ((110, -70), (200, -70), (214, -20)), (214, 10), (-84, 10)]),
          COURO, COURO_E, 8)
    cv.drawRRect(rr(-92, 4, 220, 34, 8), paint(COURO_E))
    for yy in (-190, -150, -110):
        linha(cv, 10, yy, 70, yy + 14, PAPEL, 6)
    for yy in (-450, -340):
        caixa(cv, rr(-112, yy - 26, 112, yy + 26, 10), COURO, COURO_E, 6)
        cv.drawRRect(rr(-24, yy - 30, 24, yy + 30, 6), paint(FERRO, 255, "stroke", 8))
    for dx in (-96, 96):
        cv.drawCircle(dx, -60, 18, paint(FERRO)); cv.drawCircle(dx, -60, 18, paint(FERRO_E, 255, "stroke", 5))
    cv.restore(); cv.restore()


def cena_recusa(cv, t, T):
    a = janela(t, T["aparelho"] - .25, T["mesmo"] - .25)
    if a <= 0:
        return
    u = e_inout(prog(t, T["recusou"] - .05, T["recusou"] + .6))
    b = e_out(prog(t, T["recusou"] - .2, T["recusou"] + .2))
    cv.saveLayerAlpha(None, int(255 * a))
    linha(cv, 90, 1084, 990, 1084, SILH_L, 5, 120)
    aparelho(cv, lerp(640, 790, u), 1048, lerp(1.1, .95, u), int(lerp(255, 130, u)))
    pessoa(cv, 280, 1080, 1.1, braco=(lerp(30, 180, b), lerp(130, -8, b)))
    if u > .05:                                           # o aparelho é posto de lado
        x1 = lerp(680, 900, u)
        linha(cv, 680, 520, x1, 520, OURO, 10, int(255 * u)); ponta(cv, x1, 520, 0, 34, OURO, u)
    cv.restore()
    chip(cv, "APARELHO", 650, 480, "#FFFFFF", a * (1 - prog(t, T["recusou"] - .2, T["recusou"])), 44, SILH_L)
    chip(cv, "RECUSOU USAR", 540, 1180, OURO, janela(t, T["recusou"], T["mesmo"] - .25), 54)


# ------------------------------------------------------------------ 5) o estreito a nado
NIV = 780


def nadador(cv, x, y, t):
    """Crawl, silhueta genérica."""
    cor, fase = "#0C1B2A", t * 7.5
    for k in (0, math.pi):
        g = fase + k
        p = skia.Path(); p.moveTo(x + 30, y - 20)
        p.quadTo(x + 40 + 60 * math.cos(g - .5), y - 24 + 75 * math.sin(g - .5), x + 46 + 100 * math.cos(g), y - 22 + 92 * math.sin(g))
        cv.drawPath(p, paint(cor, 255, "stroke", 32))
    cv.drawPath(caminho([(x + 70, y - 24), ((x + 10, y - 62), (x - 80, y - 40), (x - 130, y - 8)),
                         ((x - 90, y + 30), (x + 20, y + 34), (x + 70, y - 24))]), paint(cor))
    cv.drawCircle(x + 92, y - 44, 40, paint(cor))
    for s in (0, 1):
        linha(cv, x - 110, y, x - 215, y + 8 + 18 * math.sin(fase * 1.6 + s * math.pi), cor, 26)


def cena_nado(cv, t, T):
    a = janela(t, T["mesmo"] - .25, T["hoje"] - .25)
    if a <= 0:
        return
    cv.saveLayerAlpha(None, int(255 * a))
    cv.save(); cv.clipRRect(rr(60, 410, 1020, 1110, 34), skia.ClipOp.kIntersect, True)
    cv.drawRect(skia.Rect(60, 400, 1020, NIV + 60), paint("#E0B37A", 255, shader=skia.GradientShader.MakeLinear(
        [skia.Point(0, 400), skia.Point(0, NIV)], [C("#31506B"), C("#E0B37A")])))
    cv.drawCircle(540, 620, 60, paint("#F7E2AE"))
    u = e_inout(prog(t, T["mesmo"], T["nado"] + .55))
    x = lerp(330, 760, u)
    nadador(cv, x, NIV - 6 + 8 * math.sin(t * 5), t)
    for i in range(4):                                    # a água cobre a metade de baixo do corpo
        p = skia.Path(); yb = NIV + 8 + i * 92
        for j in range(41):
            xx = 40 + j * 25; yy = yb + 10 * math.sin(j * .75 + t * 3 + i * 1.7)
            p.moveTo(xx, yy) if j == 0 else p.lineTo(xx, yy)
        if i == 0:
            q = skia.Path(p); q.lineTo(1040, 1120); q.lineTo(40, 1120); q.close()
            cv.drawPath(q, paint("#1D6A8C", 255, shader=skia.GradientShader.MakeLinear(
                [skia.Point(0, NIV), skia.Point(0, 1110)], [C("#2F8CB0"), C("#0E3B55")])))
        cv.drawPath(p, paint("#BFE6F5", 190 - 40 * i, "stroke", 6))
    tr = paint("#FFFFFF", 220, "stroke", 8); tr.setPathEffect(skia.DashPathEffect.Make([20, 18], 0))
    cv.drawLine(255, NIV + 95, x, NIV + 95, tr); ponta(cv, x + 8, NIV + 95, 0, 32, "#FFFFFF", .95)
    for s, bx in ((1, 60), (-1, 1020)):                   # as duas margens
        forma(cv, caminho([(bx, 560), ((bx + s * 60, 545), (bx + s * 100, 620), (bx + s * 130, 690)),
                           ((bx + s * 175, 740), (bx + s * 180, 900), (bx + s * 130, 1120)), (bx, 1120)]),
              "#6B5138", "#3F2E1E", 6)
        cv.drawPath(caminho([(bx, 560), ((bx + s * 60, 545), (bx + s * 100, 620), (bx + s * 130, 690)),
                             ((bx + s * 90, 690), (bx + s * 40, 640), (bx, 650))]), paint("#6F8F5B"))
    cv.restore()
    cv.drawRRect(rr(60, 410, 1020, 1110, 34), paint(SILH_L, 200, "stroke", 5))
    cv.restore()
    chip(cv, "HELESPONTO", 540, 510, "#FFFFFF", janela(t, T["estreito"] - .1, T["hoje"] - .25), 46, OURO)
    chip(cv, "A NADO", 540, 1190, OURO, janela(t, T["nado"] - .1, T["hoje"] - .25), 54)


# ------------------------------------------------------------------ 6 e 7) HOJE: cf_pe_torto reaproveitado
def trocas(T):
    """[(sai0, sai1, entra1, k0, k1)] — duas trocas entre 'gessos' e 'depois'."""
    t0 = T["gessos"] + .62; P = (T["depois"] - .12 - t0) / 2
    ks = (pt.K_MANIP, .46, pt.K_FIM)
    return [(t0 + i * P, t0 + (i + .25) * P, t0 + (i + .78) * P, ks[i], ks[i + 1]) for i in range(2)]


def k_em(t, T):
    k = lerp(0, pt.K_MANIP, e_inout(prog(t, T["manip"] + .2, T["gessos"] - .1)))
    for s0, s1, _, k0, k1 in trocas(T):
        if t > s0:                                        # o pé gira com o gesso velho já aberto
            k = lerp(k0, k1, e_inout(prog(t, s0 + .04, s1 + .18)))
    return k


def gesso_em(t, T):
    """-> (enrolado, saindo)"""
    if t >= T["depois"]:
        return 1.0, prog(t, T["depois"], T["depois"] + .4)
    v = (e_inout(prog(t, T["gessos"] - .05, T["gessos"] + .35)), 0.0)
    for s0, s1, e1, _, _ in trocas(T):
        if t >= s1:
            v = (e_inout(prog(t, s1, e1)), 0.0)
        elif t >= s0:
            v = (1.0, prog(t, s0, s1))
    return v


def cena_hoje(cv, t, T):
    a = janela(t, T["hoje"] - .2, T["manda"] - .4)
    if a <= 0:
        return
    T2 = dict(T, gesso=T["gessos"], dentro=1e9)
    k = k_em(t, T); enr, sai = gesso_em(t, T)
    cv.saveLayerAlpha(None, int(255 * a))
    cv.save()
    cv.translate(lerp(540, 620, e_inout(prog(t, T["gessos"], T["depois"]))), 810); cv.scale(.93, .93); cv.translate(-600, -860)
    cv.saveLayer(skia.Rect(-600, pt.Y_DISS0 - 200, W + 600, 1600), None)
    pt.desenha_pele(cv, t, T2, k)
    if sai < 1:
        pt.desenha_gesso(cv, k, enr, sai)
    pt.dedos(cv, k)
    m = skia.Paint(AntiAlias=True)
    m.setShader(skia.GradientShader.MakeLinear([skia.Point(0, pt.Y_DISS0), skia.Point(0, pt.Y_DISS1)],
                                               [skia.ColorSetARGB(0, 0, 0, 0), skia.ColorSetARGB(255, 0, 0, 0)]))
    m.setBlendMode(skia.BlendMode.kDstIn)
    cv.drawRect(skia.Rect(-600, pt.Y_DISS0 - 200, W + 600, 1600), m)
    cv.restore()
    pt.manipulacao(cv, t, T2, k)
    pt.ortese(cv, t, T2, k)
    cv.restore(); cv.restore()
    pt.icone_calendario(cv, t, dict(T, manip=T["depois"] + .2))
    chip_janela(cv, "MANIPULAÇÃO SUAVE", t, T["manip"], T["gessos"] - .15)
    chip_janela(cv, "TROCAS DE GESSO", t, T["gessos"] + .1, T["primeiras"] - .25)
    chip_janela(cv, "PRIMEIRAS SEMANAS", t, T["primeiras"], T["depois"] + .1)
    pt.cartao(cv, "GESSOS", "aos poucos", t, T["gessos"], T["depois"] - .1)
    pt.cartao(cv, "ÓRTESE", "pra manter", t, T["ortese"], T["manda"] - .45)


# ------------------------------------------------------------------ quadro
def faixa_epoca(cv, t, T):
    for s, t0, t1, cor, x in (("NO PASSADO", T["poetas"] + .6, T["mae"] - .35, PAPEL, 540),
                              ("1791", T["mae"] - .1, T["medicos"] - .4, PAPEL, 540),
                              ("NO PASSADO", T["medicos"] - .15, T["hoje"] - .35, PAPEL, 540),
                              ("HOJE", T["hoje"] - .1, T["manda"] - .45, OURO, 900)):
        chip(cv, s, x, 300, cor, janela(t, t0, t1, .2, .2), 46)


FONTE1, FONTE2 = "Diagnóstico de Byron: discutido", "Fonte: Hektoen International, 2018"
DISCUTE = "PÉ TORTO? AINDA SE DISCUTE"


def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    for cena in (cena_nasceu, cena_poeta, cena_byron, cena_carta, cena_medicos, cena_tratamento, cena_recusa,
                 cena_nado, cena_hoje):
        cena(cv, t, T)
    # o "?" fica: lembrete enquanto o passado segue
    chip(cv, DISCUTE, 540, 450, OURO, janela(t, T["discute"] - .1, T["trat"] - .4), 44)
    chip(cv, DISCUTE, 540, 374, OURO, janela(t, T["trat"] - .2, T["hoje"] - .35), 32)
    faixa_epoca(cv, t, T)
    a = janela(t, T["ortese"], T["manda"] - .45)
    if a > 0:
        texto(cv, FONTE1, 540, 1168, F_BLACK, 34, "#FFFFFF", int(255 * a), contorno=8)
        texto(cv, FONTE2, 540, 1216, F_BLACK, 30, pt.AZUL, int(255 * a), contorno=8)
    t_sai = T["poetas"] - .1
    capa(cv, t, t_sai, *ep["gancho"])
    a = prog(t, t_sai + .3, t_sai + .7) * (1 - prog(t, T["manda"] - .3, T["manda"]))
    if a > 0:
        cv.drawRRect(rr(330, 150, 750, 204, 27), paint("#FFFFFF", int(28 * a)))
        texto(cv, "HISTÓRIA NO OSSO", 540, 190, F_BLACK, 32, OURO, int(255 * a))
    interface(cv, t, T, blocos, DESTAQUE)
    a = prog(t, T["manda"] + .2, T["manda"] + .5)
    if a > 0:
        texto(cv, FONTE1, 540, 1276, F_BLACK, 34, "#FFFFFF", int(255 * a), contorno=6)
        texto(cv, FONTE2, 540, 1324, F_BLACK, 32, "#9CC9FF", int(255 * a), contorno=6)


def sons(T):
    ev = [(T["nasceu"], "pop", .5), (T["diferente"], "shimmer", .3), (T["virou"], "whoosh", .3),
          (T["lord"], "pop", .55), (T["mae"] - .1, "whoosh", .3), (T["direito"], "pop", .45),
          (T["vira"] + .1, "whoosh", .35), (T["medicos"], "whoosh", .25), (T["torto1"], "thump", .7),
          (T["ate"], "pop", .5), (T["discute"], "shimmer", .3), (T["trat"] - .1, "whoosh", .25),
          (T["doiam"], "thump", .5), (T["aparelho"], "pop", .45), (T["recusou"], "whoosh", .4),
          (T["mesmo"], "whoosh", .3), (T["nado"], "pop", .45), (T["hoje"], "shimmer", .35),
          (T["manip"], "pop", .4), (T["gessos"], "whoosh", .3)]
    for s0, s1, _, _, _ in trocas(T):
        ev += [(s0, "whoosh", .2), (s1 + .2, "click", .8)]
    ev += [(T["primeiras"] + .2 * i, "tick", .3) for i in range(4)]
    return ev + [(T["depois"], "whoosh", .2), (T["ortese"], "pop", .45), (T["manter"], "ping", .4),
                 (T["manda"] + .05, "whoosh", .5)]


def tempos_previa(T):
    return (0.0, T["diferente"] + .4, T["poetas"] + .8, T["lord"] + .6, T["direito"], T["dentro"] + .4,
            T["torto1"] + .3, T["discute"] + .3, T["doiam"] + .35, T["aparelho"] + .2, T["usar"],
            T["estreito"] + .2, T["hoje"] + .5, T["manip"] + .7, T["gessos"] + .4, T["primeiras"] + .4,
            T["ortese"] + .5, T["manda"] + 1.6)


render = fazer_render(quadro, ANCORAS, sons, tempos_previa, respiro_cta=1.8)
