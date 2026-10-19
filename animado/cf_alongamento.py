# -*- coding: utf-8 -*-
"""COMO FUNCIONA — alongamento ósseo ("Cortar o osso de propósito?"). Piloto A, aprovado pelo
Rafael em 18/10/2026; o desenho é o do piloto, sem alteração.

O que a cena mostra, sincronizado com a fala (o tempo de cada palavra comanda o quadro): o osso é
cortado (carimbo "DE PROPÓSITO"), o fixador encaixa com som de metal, o osso "dorme" na pausa e
acorda, as partes se afastam 1 mm por dia com um clique a cada milímetro, o espaço se enche de
osso novo que brilha, pele/nervo/vaso esticam junto, o osso novo endurece e o aparelho sai.

A cena é PRESA ao roteiro: `montar()` procura palavras exatas ("cortar", "propósito", "aparelho",
"fixador", "alguns", "acordar", "aí", "separar", "milímetro", "osso novo", "pele", "nervo", "vaso",
"devagar", "endurece", "sai", "manda"). Mudar o roteiro sem manter essas palavras quebra o render
de propósito (KeyError) — não sai vídeo dessincronizado.
"""
import math, os, re
import numpy as np
import skia

from . import fontes, som, voz as _voz
from .base import W, H, FPS, codificar, previas as _previas

F_BLACK = fontes.fonte("black")
F_BOLD = fontes.fonte("bold")
F_REG = fontes.fonte("reg")
F_SEMI = fontes.fonte("semi")

# ------------------------------------------------------------------ paleta
def C(hexs, a=255):
    h = hexs.lstrip("#")
    return skia.ColorSetARGB(int(a), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

BG_IN, BG_OUT = "#17384C", "#0A1520"
OSSO_C, OSSO_B, OSSO_L = "#F7EEDD", "#D5C3A2", "#8C7656"
NOVO, NOVO_G = "#F2B544", "#FFB627"
ACO, ACO_ESC, ACO_HL = "#A9BCCF", "#5E7186", "#E6EEF6"
OURO = "#F5C04A"
VERMELHO = "#FF5A5F"
NERVO, VASO, PELE = "#F4D35E", "#E5484D", "#F0B49A"

# ------------------------------------------------------------------ easing
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= a)
def e_out(x): return 1 - (1 - x) ** 3
def e_inout(x): return 3 * x * x - 2 * x * x * x
def e_back(x, s=1.7):
    x -= 1
    return x * x * ((s + 1) * x + s) + 1
def e_in_back(x, s=1.7): return x * x * ((s + 1) * x - s)
def lerp(a, b, x): return a + (b - a) * x
def lerpc(c1, c2, x):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{int(lerp(a[i], b[i], x)):02X}" for i in range(3))

# ------------------------------------------------------------------ voz: tira o ar morto entre frases
def comprimir(voz, palavras, max_gap=0.30, limiar=0.42):
    """Encurta silêncios > `limiar` s para `max_gap` s e remapeia o tempo de cada palavra."""
    cortes = []                                   # (inicio_s, fim_s) a remover
    for a, b in zip(palavras, palavras[1:]):
        fim_a = a["t"] + a["d"]; gap = b["t"] - fim_a
        alvo = 0.85 if b["w"].lower() == "manda" else max_gap   # respiro: deixa ver o aparelho sair
        if gap > max(limiar, alvo):
            meio = fim_a + gap / 2; tirar = gap - alvo
            cortes.append((meio - tirar / 2, meio + tirar / 2))
    partes, ult = [], 0
    for c0, c1 in cortes:
        partes.append(voz[int(ult * som.SR):int(c0 * som.SR)]); ult = c1
    partes.append(voz[int(ult * som.SR):])
    nova = np.concatenate(partes)

    def remap(t):
        return t - sum(min(c1, t) - c0 for c0, c1 in cortes if t > c0)
    novas = [dict(p, t=remap(p["t"])) for p in palavras]
    return nova, novas, sum(c1 - c0 for c0, c1 in cortes)

# ------------------------------------------------------------------ palavras -> pontuação do roteiro
def alinhar(palavras, roteiro):
    toks = re.findall(r"[\wÀ-ÿ]+[.,:;!?—]*", roteiro)
    out = []; j = 0
    for p in palavras:
        alvo = p["w"].lower()
        while j < len(toks) and re.sub(r"[.,:;!?—]", "", toks[j]).lower() != alvo:
            j += 1
        tok = toks[j] if j < len(toks) else p["w"]
        out.append(dict(p, tok=tok, fim_frase=bool(re.search(r"[.!?:]$", tok)), virg=tok.endswith(",")))
        j += 1
    return out

# ------------------------------------------------------------------ desenho: utilidades
def paint(cor, a=255, estilo="fill", w=0, blur=0, shader=None):
    p = skia.Paint(AntiAlias=True)
    p.setColor(C(cor, a))
    p.setStyle(skia.Paint.kStroke_Style if estilo == "stroke" else skia.Paint.kFill_Style)
    if w: p.setStrokeWidth(w)
    if estilo == "stroke": p.setStrokeCap(skia.Paint.kRound_Cap)
    if blur: p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    if shader is not None: p.setShader(shader)
    return p

def texto(cv, s, x, y, fonte, tam, cor, a=255, centro=True, contorno=0, track=0.0):
    f = skia.Font(fonte, tam); f.setEdging(skia.Font.Edging.kAntiAlias)
    larg = f.measureText(s) + track * max(0, len(s) - 1)
    x0 = x - larg / 2 if centro else x
    if track:
        cx = x0
        for ch in s:
            if contorno: cv.drawString(ch, cx, y, f, paint("#000000", int(a * 0.85), "stroke", contorno))
            cv.drawString(ch, cx, y, f, paint(cor, a)); cx += f.measureText(ch) + track
    else:
        if contorno: cv.drawString(s, x0, y, f, paint("#000000", int(a * 0.85), "stroke", contorno))
        cv.drawString(s, x0, y, f, paint(cor, a))
    return larg

def larg_texto(s, fonte, tam):
    return skia.Font(fonte, tam).measureText(s)

# ------------------------------------------------------------------ osso
CX = 540
Y_TOPO, Y_CORTE, Y_BASE = 300, 735, 1150      # comprimento inicial (antes do alongamento)
HASTE = 128                                    # largura da diáfise
PX_MM = 6.0                                    # escala esquemática: 35 mm = 210 px

def path_osso_sup(y0, yc):
    p = skia.Path(); h = HASTE / 2
    p.moveTo(CX - 128, y0 + 40)
    p.cubicTo(CX - 135, y0 - 6, CX - 60, y0 - 18, CX - 10, y0 + 6)       # platô medial
    p.cubicTo(CX + 30, y0 - 20, CX + 132, y0 - 10, CX + 126, y0 + 42)    # platô lateral
    p.cubicTo(CX + 120, y0 + 120, CX + h + 8, y0 + 150, CX + h, y0 + 230)
    p.lineTo(CX + h, yc); p.lineTo(CX - h, yc); p.lineTo(CX - h, y0 + 230)
    p.cubicTo(CX - h - 8, y0 + 150, CX - 122, y0 + 120, CX - 128, y0 + 40)
    p.close(); return p

def path_osso_inf(yc, yb):
    """Tíbia distal: alarga pouco, com o maléolo medial descendo só de um lado (não é um
    "osso de cachorro" simétrico)."""
    p = skia.Path(); h = HASTE / 2
    p.moveTo(CX - h, yc); p.lineTo(CX + h, yc); p.lineTo(CX + h, yb - 190)
    p.cubicTo(CX + h + 4, yb - 110, CX + 84, yb - 70, CX + 80, yb - 22)   # face lateral
    p.cubicTo(CX + 76, yb + 2, CX + 30, yb - 4, CX - 10, yb - 2)          # superfície articular
    p.cubicTo(CX - 40, yb, CX - 52, yb + 34, CX - 70, yb + 36)            # ponta do maléolo medial
    p.cubicTo(CX - 92, yb + 36, CX - 96, yb - 10, CX - 92, yb - 60)
    p.cubicTo(CX - 88, yb - 120, CX - h - 4, yb - 140, CX - h, yb - 190)
    p.close(); return p

def sombra_osso():
    return skia.GradientShader.MakeLinear(
        [skia.Point(CX - 140, 0), skia.Point(CX + 140, 0)],
        [C(OSSO_B), C(OSSO_C), C(OSSO_C), C(OSSO_B)], [0.0, 0.42, 0.58, 1.0])

def desenha_osso(cv, yc_sup, yc_inf, yb):
    sh = sombra_osso()
    for pth in (path_osso_sup(Y_TOPO, yc_sup), path_osso_inf(yc_inf, yb)):
        cv.drawPath(pth, paint("#000000", 70, blur=14))                  # sombra suave
        cv.drawPath(pth, paint(OSSO_C, shader=sh))
        cv.drawPath(pth, paint(OSSO_L, 150, "stroke", 2.5))
    # canal medular (insinuação de profundidade)
    for y0, y1 in ((Y_TOPO + 250, yc_sup), (yc_inf, yb - 190)):
        if y1 > y0:
            cv.drawRect(skia.Rect(CX - 16, y0, CX + 16, y1), paint(OSSO_B, 60, blur=6))

def desenha_regenerado(cv, y0, y1, densidade, brilho, duro, t):
    if y1 - y0 < 1.5:
        return
    h = HASTE / 2 - 2
    cor = lerpc(NOVO, OSSO_C, duro)
    if brilho > 0.01:
        cv.drawRect(skia.Rect(CX - h - 26, y0 - 18, CX + h + 26, y1 + 18), paint(NOVO_G, int(150 * brilho * (1 - duro)), blur=26))
    cv.drawRect(skia.Rect(CX - h, y0, CX + h, y1), paint(cor, int(60 + 195 * densidade)))
    # estrias longitudinais (o "osso novo" nasce em fibras no sentido da tração)
    n = 9
    for k in range(n):
        x = CX - h + 8 + k * (2 * h - 16) / (n - 1)
        pth = skia.Path(); pth.moveTo(x, y0)
        segs = max(2, int((y1 - y0) / 18))
        for s in range(1, segs + 1):
            yy = y0 + (y1 - y0) * s / segs
            pth.lineTo(x + math.sin(s * 1.7 + k + t * 2.2) * 3.2, yy)
        cv.drawPath(pth, paint(lerpc("#B5701A", OSSO_B, duro), int(150 * densidade * (1 - 0.85 * duro)), "stroke", 3))

# ------------------------------------------------------------------ fixador
RX, RY = 232, 46
def anel(cv, y, dx, alfa, metade):
    if alfa <= 0:
        return
    r = skia.Rect(CX + dx - RX, y - RY, CX + dx + RX, y + RY)
    if metade == "tras":
        cv.drawArc(r, 180, 180, False, paint(ACO_ESC, int(255 * alfa), "stroke", 15))
    else:
        cv.drawArc(r, 0, 180, False, paint("#000000", int(80 * alfa), "stroke", 18, blur=6))
        cv.drawArc(r, 0, 180, False, paint(ACO, int(255 * alfa), "stroke", 15))
        cv.drawArc(skia.Rect(r.left() + 6, r.top() + 4, r.right() - 6, r.bottom() - 2), 20, 140, False,
                   paint(ACO_HL, int(170 * alfa), "stroke", 3))
        for ang in (25, 90, 155):                                   # furos do anel
            a = math.radians(ang)
            cv.drawCircle(CX + dx + RX * math.cos(a), y + RY * math.sin(a), 3.2, paint(ACO_ESC, int(255 * alfa)))

def fios(cv, y, prog_fio, alfa):
    if prog_fio <= 0 or alfa <= 0:
        return
    for s in (-1, 1):
        x0, y0 = CX - RX + 18, y - 14 * s
        x1, y1 = CX + RX - 18, y + 14 * s
        xe = lerp(x0, x1, prog_fio); ye = lerp(y0, y1, prog_fio)
        cv.drawLine(x0, y0, xe, ye, paint("#DDE6EE", int(230 * alfa), "stroke", 3.2))
        if prog_fio > 0.98:
            cv.drawCircle(CX - 70 * s, y - 5 * s, 6, paint(OURO, int(255 * alfa)))   # oliva

def haste(cv, x, ya, yb, alfa, rosca=False, fase=0.0):
    if alfa <= 0 or yb <= ya:
        return
    cv.drawLine(x, ya, x, yb, paint("#000000", int(70 * alfa), "stroke", 12, blur=4))
    cv.drawLine(x, ya, x, yb, paint("#8FA3B8", int(255 * alfa), "stroke", 9))
    cv.drawLine(x - 2, ya, x - 2, yb, paint(ACO_HL, int(140 * alfa), "stroke", 2))
    if rosca:
        y = ya + (fase * 9) % 9
        while y < yb:
            cv.drawLine(x - 5, y, x + 5, y + 3, paint(ACO_ESC, int(200 * alfa), "stroke", 1.6)); y += 9

def porca(cv, x, y, ang, alfa):
    if alfa <= 0:
        return
    p = skia.Path()
    for k in range(6):
        a = math.radians(ang + k * 60)
        (p.moveTo if k == 0 else p.lineTo)(x + 14 * math.cos(a), y + 9 * math.sin(a))
    p.close()
    cv.drawPath(p, paint(OURO, int(255 * alfa)))
    cv.drawPath(p, paint("#8A6512", int(255 * alfa), "stroke", 2))

# ------------------------------------------------------------------ partes moles
def perna(cv, yb, alfa):
    """Contorno de perna de verdade: joelho, panturrilha que abaula no terço superior,
    afinando até o tornozelo. Antes era um retângulo translúcido que parecia vidro."""
    if alfa <= 0:
        return
    L = yb - (Y_TOPO - 50)                                   # comprimento acompanha o alongamento
    def y(f): return Y_TOPO - 50 + L * f
    p = skia.Path()
    p.moveTo(CX - 150, y(0.0))                                 # joelho, lado medial
    p.cubicTo(CX - 168, y(0.10), CX - 200, y(0.22), CX - 196, y(0.36))   # panturrilha
    p.cubicTo(CX - 192, y(0.52), CX - 140, y(0.66), CX - 112, y(0.80))
    p.cubicTo(CX - 100, y(0.88), CX - 112, y(0.96), CX - 100, y(1.04))   # tornozelo
    p.lineTo(CX + 108, y(1.04))
    p.cubicTo(CX + 112, y(0.95), CX + 104, y(0.88), CX + 112, y(0.80))
    p.cubicTo(CX + 132, y(0.64), CX + 176, y(0.50), CX + 172, y(0.34))
    p.cubicTo(CX + 168, y(0.20), CX + 152, y(0.08), CX + 140, y(0.0))
    p.close()
    sh = skia.GradientShader.MakeLinear([skia.Point(CX - 200, 0), skia.Point(CX + 180, 0)],
                                        [C(PELE, int(85 * alfa)), C(PELE, int(25 * alfa)), C(PELE, int(70 * alfa))],
                                        [0.0, 0.5, 1.0])
    # a perna é desenhada numa camada e o topo é apagado por máscara em degradê (DstIn):
    # dissolve no fundo de verdade, sem retângulo de cor "parecida" por cima
    cv.saveLayer(skia.Rect(0, y(0.0) - 40, W, y(1.04) + 40), None)
    cv.drawPath(p, paint(PELE, 255, shader=sh))
    cv.drawPath(p, paint(PELE, int(70 * alfa), "stroke", 14, blur=10))
    cv.drawPath(p, paint(PELE, int(190 * alfa), "stroke", 3))
    masc = skia.Paint(AntiAlias=True)
    masc.setShader(skia.GradientShader.MakeLinear([skia.Point(0, y(0.0)), skia.Point(0, y(0.0) + 120)],
                                                  [skia.ColorSetARGB(0, 0, 0, 0), skia.ColorSetARGB(255, 0, 0, 0)]))
    masc.setBlendMode(skia.BlendMode.kDstIn)
    cv.drawRect(skia.Rect(0, y(0.0) - 40, W, y(1.04) + 40), masc)
    cv.restore()

def tecido_linha(cv, x, ya, yb, amp, cor, larg, alfa, t, fase):
    if alfa <= 0:
        return
    p = skia.Path(); p.moveTo(x, ya); n = 48
    for k in range(1, n + 1):
        y = ya + (yb - ya) * k / n
        p.lineTo(x + amp * math.sin(k * 0.9 + fase + t * 1.4), y)
    cv.drawPath(p, paint(cor, int(90 * alfa), "stroke", larg + 6, blur=5))
    cv.drawPath(p, paint(cor, int(255 * alfa), "stroke", larg))

def rotulo(cv, s, x, y, xa, ya, cor, alfa, esq=True):
    if alfa <= 0:
        return
    cv.drawLine(xa, ya, x + (70 if esq else -10), y - 12, paint(cor, int(200 * alfa), "stroke", 2.5))
    cv.drawCircle(xa, ya, 6, paint(cor, int(255 * alfa)))
    f = skia.Font(F_BLACK, 40); lw = f.measureText(s)
    bx = x - (lw + 30) if not esq else x - 10
    rr = skia.RRect.MakeRectXY(skia.Rect(bx, y - 44, bx + lw + 30, y + 10), 14, 14)
    cv.drawRRect(rr, paint("#0B1824", int(215 * alfa)))
    cv.drawRRect(rr, paint(cor, int(255 * alfa), "stroke", 2.5))
    cv.drawString(s, bx + 15, y - 3, f, paint(cor, int(255 * alfa)))

# ------------------------------------------------------------------ efeitos de cena
def carimbo(cv, s, x, y, rot, t0, t, dur=1.9):
    k = t - t0
    if k < 0 or k > dur:
        return
    esc = lerp(1.9, 1.0, e_out(clamp(k / 0.16)))
    alfa = clamp(k / 0.08) * (1 - prog(k, dur - 0.35, dur))
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(esc, esc)
    f = skia.Font(F_BLACK, 62); lw = f.measureText(s)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 24, -62, lw / 2 + 24, 22), 12, 12)
    cv.drawRRect(rr, paint("#0B1824", int(160 * alfa)))
    cv.drawRRect(rr, paint(VERMELHO, int(255 * alfa), "stroke", 7))
    cv.drawString(s, -lw / 2, 0, f, paint(VERMELHO, int(255 * alfa)))
    cv.restore()

def zzz(cv, x, y, t, t0, t1):
    if not (t0 <= t <= t1 + 0.6):
        return
    for k in range(3):
        fase = ((t - t0) * 0.55 + k / 3) % 1.0
        a = math.sin(math.pi * fase) * (1 - prog(t, t1, t1 + 0.6))
        texto(cv, "Z", x + 90 * fase + k * 14, y - 190 * fase, F_BLACK, int(56 + 54 * fase), "#9CC9FF", int(255 * a), False, contorno=8)

def brilhos(cv, x, y, t, t0, n=14, raio=190):
    k = t - t0
    if k < 0 or k > 0.9:
        return
    for i in range(n):
        ang = i * 2 * math.pi / n + 0.3
        d = raio * e_out(k / 0.9) * (0.6 + 0.4 * ((i * 37) % 10) / 10)
        a = int(255 * (1 - k / 0.9))
        px, py = x + d * math.cos(ang), y + d * math.sin(ang) * 0.8
        s = 9 * (1 - k / 0.9) + 3
        p = skia.Path(); p.moveTo(px, py - s * 2); p.lineTo(px + s * 0.5, py - s * 0.5); p.lineTo(px + s * 2, py)
        p.lineTo(px + s * 0.5, py + s * 0.5); p.lineTo(px, py + s * 2); p.lineTo(px - s * 0.5, py + s * 0.5)
        p.lineTo(px - s * 2, py); p.lineTo(px - s * 0.5, py - s * 0.5); p.close()
        cv.drawPath(p, paint(OURO, a))

def aviao(cv, t, t0):
    k = t - t0
    if k < 0:
        return
    x = lerp(230, 850, e_inout(clamp(k / 1.4))); y = lerp(1420, 960, e_inout(clamp(k / 1.4)))
    a = clamp(k / 0.2)
    for i in range(12):                                              # rastro pontilhado
        kk = k - i * 0.06
        if kk <= 0:
            break
        xx = lerp(230, 850, e_inout(clamp(kk / 1.4))); yy = lerp(1420, 960, e_inout(clamp(kk / 1.4)))
        cv.drawCircle(xx - 30, yy + 20, 4, paint("#FFFFFF", int(120 * a * (1 - i / 12))))
    cv.save(); cv.translate(x, y); cv.rotate(-28); cv.scale(1.5, 1.5)
    p = skia.Path(); p.moveTo(-40, 0); p.lineTo(46, -26); p.lineTo(4, 30); p.lineTo(-6, 6); p.close()
    cv.drawPath(p, paint("#FFFFFF", int(255 * a)))
    p2 = skia.Path(); p2.moveTo(-6, 6); p2.lineTo(46, -26); p2.lineTo(2, 12); p2.close()
    cv.drawPath(p2, paint("#C9D6E2", int(255 * a)))
    cv.restore()

# ------------------------------------------------------------------ fundo
RNG = np.random.default_rng(7)
PART = [(RNG.uniform(0, W), RNG.uniform(0, H), RNG.uniform(6, 22), RNG.uniform(1.5, 4.5), RNG.uniform(20, 55)) for _ in range(46)]

def fundo(cv, t):
    sh = skia.GradientShader.MakeRadial(skia.Point(W / 2, H * 0.42 + 40 * math.sin(t * 0.3)), H * 0.78,
                                        [C(BG_IN), C(BG_OUT)])
    cv.drawRect(skia.Rect(0, 0, W, H), paint(BG_IN, shader=sh))
    for x, y, v, r, a in PART:
        yy = (y - v * t * 6) % H
        cv.drawCircle(x + 8 * math.sin(t * 0.5 + y), yy, r, paint("#BFE3FF", int(a)))

# ------------------------------------------------------------------ legenda palavra a palavra
DESTAQUE = {"cortar", "propósito", "fixador", "milímetro", "dia", "novo", "devagar", "endurece",
            "sai", "possível", "mais", "curta", "pele", "nervo", "vaso", "acordar"}

def montar_blocos(pal):
    """Blocos = frases; frase longa quebra em pedaços equilibrados de até 5 palavras,
    preferindo a vírgula. Evita palavra órfã ("NOVO." sozinho na tela)."""
    frases, atual = [], []
    for p in pal:
        atual.append(p)
        if p["fim_frase"]:
            frases.append(atual); atual = []
    if atual:
        frases.append(atual)
    blocos = []
    for fr in frases:
        if len(fr) <= 6 or fr[0]["w"].lower() == "manda":     # a CTA fica inteira, num bloco só
            blocos.append(fr); continue
        n = math.ceil(len(fr) / 5); alvo = len(fr) / n; ini = 0
        for k in range(1, n):
            corte = round(alvo * k)
            virgs = [i + 1 for i in range(ini, len(fr) - 1) if fr[i]["virg"] and abs(i + 1 - corte) <= 1]
            corte = virgs[0] if virgs else corte
            blocos.append(fr[ini:corte]); ini = corte
        blocos.append(fr[ini:])
    return blocos

def legenda(cv, blocos, t, y_base=1395, tam=80, cta=False):
    """Estilo karaokê: o bloco inteiro aparece (as palavras ainda não ditas em branco
    apagado), a palavra que está sendo dita acende em ouro e cresce um pouco."""
    vivo = None
    for i, b in enumerate(blocos):
        ini = b[0]["t"] - 0.12
        fim = blocos[i + 1][0]["t"] - 0.12 if i + 1 < len(blocos) else b[-1]["t"] + b[-1]["d"] + 2.5
        if ini <= t < fim:
            vivo = b; break
    if not vivo:
        return
    fonte = F_BLACK; esp = 26
    linhas, linha, lw = [], [], 0
    for p in vivo:
        w = larg_texto(p["tok"].upper(), fonte, tam)
        if linha and lw + esp + w > 920:
            linhas.append(linha); linha, lw = [], 0
        linha.append((p, w)); lw += (esp if lw else 0) + w
    if linha:
        linhas.append(linha)
    entrada = e_out(clamp((t - (vivo[0]["t"] - 0.12)) / 0.15))
    alt_lin = tam * 1.18
    y = y_base - (len(linhas) - 1) * alt_lin / 2 + (1 - entrada) * 24
    for ln in linhas:
        total = sum(w for _, w in ln) + esp * (len(ln) - 1)
        x = CX - total / 2
        for p, w in ln:
            k = t - p["t"]
            base = re.sub(r"[.,:;!?—]", "", p["tok"]).lower()
            dita = k >= -0.03
            falando = p["t"] - 0.03 <= t <= p["t"] + p["d"] + 0.06
            if falando:
                cor, a = OURO, 255
            elif dita:
                cor, a = (OURO if base in DESTAQUE else "#FFFFFF"), 255
            else:
                cor, a = "#FFFFFF", 105
            esc = 1.0 + (0.10 * (1 - e_out(clamp(k / 0.16))) if dita else 0.0)
            s = p["tok"].upper()
            track = 0.0
            if base == "devagar" and dita:                    # piada tipográfica: a palavra "demora"
                track = 9 * e_out(clamp(k / 1.2))
            cv.save(); cv.translate(x, y); cv.scale(esc, esc)  # escala ancorada na ESQUERDA: não invade o vizinho
            texto(cv, s, 0, 0, fonte, tam, cor, int(a * entrada), centro=False, contorno=12, track=track)
            cv.restore()
            x += w + esp + track * (len(s) - 1)
        y += alt_lin

# ------------------------------------------------------------------ cronologia (a partir das palavras)
def montar(pal):
    def em(palavra, n=1, bigrama=None):
        c = 0
        for i, p in enumerate(pal):
            if p["w"].lower() == palavra:
                if bigrama and (i + 1 >= len(pal) or pal[i + 1]["w"].lower() != bigrama):
                    continue
                c += 1
                if c == n:
                    return p["t"]
        raise KeyError(f"palavra nao achada: {palavra} #{n}")
    fim_fala = pal[-1]["t"] + pal[-1]["d"]
    T = dict(
        cortar=em("cortar"), prop1=em("propósito", 1), aparelho=em("aparelho", 1), fixador=em("fixador"),
        alguns=em("alguns"), acordar=em("acordar"), ai=em("aí"), separar=em("separar"),
        milimetro=em("milímetro"), osso_novo=em("osso", 1, "novo"), pele=em("pele"), nervo=em("nervo"),
        vaso=em("vaso"), devagar=em("devagar"), prop2=em("propósito", 2), endurece=em("endurece"),
        sai=em("sai"), manda=em("manda"), fim_fala=fim_fala)
    T["dist_ini"] = T["separar"] + 0.15
    T["dist_fim"] = T["endurece"] - 0.25
    T["total"] = fim_fala + 2.2
    return T

LAT_DIAS, MM_TOTAL = 5, 35

def estado(T, t):
    """Quanto o osso já separou (mm) e em que dia do tratamento estamos."""
    if t < T["alguns"]:
        return 0.0, 0
    if t < T["dist_ini"]:
        d = 1 + int(prog(t, T["alguns"], T["dist_ini"]) * (LAT_DIAS - 0.01))
        return 0.0, d
    x = prog(t, T["dist_ini"], T["dist_fim"])
    mm = MM_TOTAL * x                                        # linear: 1 mm por dia é ritmo constante
    return mm, LAT_DIAS + int(round(mm))

# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, eventos_clique):
    fundo(cv, t)
    mm, dia = estado(T, t)
    gap = mm * PX_MM
    fenda = 7 * e_out(prog(t, T["cortar"] + 0.05, T["cortar"] + 0.25))
    yc_sup = Y_CORTE; yc_inf = Y_CORTE + fenda + gap; yb = Y_BASE + fenda + gap

    # câmera: começa perto do corte, abre quando o fixador chega, recua no fim
    z0 = 1.08; z1 = 1.0; z2 = 0.9
    s = lerp(z0, z1, e_inout(prog(t, T["aparelho"] - 0.2, T["aparelho"] + 0.9)))
    s = lerp(s, 0.95, e_inout(prog(t, T["dist_ini"], T["dist_fim"])))
    s = lerp(s, z2, e_inout(prog(t, T["sai"], T["sai"] + 1.2)))
    foco = lerp(Y_CORTE, (Y_TOPO + yb) / 2, e_inout(prog(t, T["aparelho"] - 0.2, T["aparelho"] + 0.9)))
    tremor = 0.0
    for t0, forca in ((T["cortar"] + 0.1, 9), (T["fixador"] + 0.12, 6), (T["prop1"], 5)):
        k = t - t0
        if 0 <= k < 0.35:
            tremor += forca * math.sin(k * 70) * (1 - k / 0.35)
    cv.save()
    cv.translate(W / 2 + tremor, 790)
    cv.scale(s, s)
    cv.translate(-W / 2, -foco)

    # aparição do fixador
    p_an = [e_back(prog(t, T["aparelho"] + 0.07 * i, T["aparelho"] + 0.07 * i + 0.55)) for i in range(4)]
    saida = e_in_back(prog(t, T["sai"] - 0.1, T["sai"] + 0.7))
    alfa_fix = 1 - prog(t, T["sai"] + 0.35, T["sai"] + 0.75)
    y_aneis = [Y_TOPO + 70, Y_CORTE - 70, yc_inf + 100, yb - 150]
    dx = [lerp(-900, 0, p_an[0]), lerp(-900, 0, p_an[1]), lerp(900, 0, p_an[2]), lerp(900, 0, p_an[3])]
    dx = [d + (900 if i >= 2 else -900) * saida for i, d in enumerate(dx)]
    vis = [alfa_fix * clamp(p_an[i] * 3) for i in range(4)]

    # partes moles (atrás do osso)
    a_pele = prog(t, T["pele"] - 0.1, T["pele"] + 0.4) * (1 - prog(t, T["endurece"] + 0.6, T["endurece"] + 1.3))
    perna(cv, yb, a_pele)
    for i in range(4):
        anel(cv, y_aneis[i], dx[i], vis[i], "tras")
    tens = prog(t, T["pele"], T["dist_fim"])
    tecido_linha(cv, CX - 104, Y_TOPO + 110, yb - 90, lerp(16, 3, tens), VASO, 7,
                 prog(t, T["vaso"] - 0.1, T["vaso"] + 0.3) * (1 - prog(t, T["endurece"] + 0.6, T["endurece"] + 1.3)), t, 0.0)
    tecido_linha(cv, CX + 104, Y_TOPO + 90, yb - 110, lerp(18, 3, tens), NERVO, 6,
                 prog(t, T["nervo"] - 0.1, T["nervo"] + 0.3) * (1 - prog(t, T["endurece"] + 0.6, T["endurece"] + 1.3)), t, 1.3)

    # osso + osso novo
    desenha_osso(cv, yc_sup, yc_inf, yb)
    dens = clamp(mm / 6) if mm > 0 else 0
    brilho = prog(t, T["osso_novo"] - 0.1, T["osso_novo"] + 0.3) * (1 - 0.5 * prog(t, T["osso_novo"] + 1.5, T["osso_novo"] + 2.5))
    brilho = max(brilho, 0.35 * dens)
    duro = e_inout(prog(t, T["endurece"], T["endurece"] + 1.3))
    desenha_regenerado(cv, yc_sup + fenda * 0.5, yc_inf - fenda * 0.5, dens, brilho, duro, t)

    # o corte
    k = t - (T["cortar"] + 0.1)
    if 0 <= k < 1.0:
        a = 1 - k / 1.0
        cv.drawLine(CX - 150, Y_CORTE + 3, CX + 150, Y_CORTE + 3, paint(VERMELHO, int(220 * a), "stroke", 16, blur=10))
        cv.drawLine(CX - 120 * e_out(clamp(k / 0.12)), Y_CORTE + 3, CX + 120 * e_out(clamp(k / 0.12)), Y_CORTE + 3,
                    paint("#FFFFFF", int(255 * a), "stroke", 4))
    if t < T["cortar"] + 0.1:                                        # linha tracejada antes do corte
        pisca = 0.5 + 0.5 * math.sin(t * 9)
        x = CX - 112
        while x < CX + 112:
            cv.drawLine(x, Y_CORTE + 3, x + 16, Y_CORTE + 3, paint(VERMELHO, int(120 + 135 * pisca), "stroke", 5)); x += 28

    brilhos(cv, CX, Y_CORTE + 4, t, T["acordar"] + 0.15)

    # fixador (frente)
    for i in range(4):
        fios(cv, y_aneis[i], prog(t, T["fixador"] + 0.05 * i, T["fixador"] + 0.05 * i + 0.3), vis[i])
    a_h = alfa_fix * prog(t, T["fixador"] - 0.1, T["fixador"] + 0.3)
    for sx in (-1, 1):
        x = CX + sx * 204
        haste(cv, x + dx[0] * 0, y_aneis[0], y_aneis[1], a_h * vis[0])
        haste(cv, x + dx[2] * 0, y_aneis[2], y_aneis[3], a_h * vis[2])
        haste(cv, x, y_aneis[1], y_aneis[2], a_h * vis[1], rosca=True, fase=mm)
        porca(cv, x, y_aneis[1] + 22, mm * 90 + sx * 15, a_h * vis[1])
        porca(cv, x, y_aneis[2] - 22, -mm * 90, a_h * vis[2])
    for i in range(4):
        anel(cv, y_aneis[i], dx[i], vis[i], "frente")
    # o "osso dormindo" na pausa (por cima do fixador, para não sumir atrás do anel)
    zzz(cv, CX + 70, Y_CORTE - 30, t, T["alguns"] + 0.2, T["acordar"])

    # rótulos de partes moles
    rotulo(cv, "PELE", CX - 300, Y_TOPO + 210, CX - 172, Y_TOPO + 230, PELE,
           prog(t, T["pele"], T["pele"] + 0.25) * (1 - prog(t, T["devagar"] + 0.8, T["devagar"] + 1.3)))
    rotulo(cv, "NERVO", CX + 300, Y_CORTE + 160, CX + 108, Y_CORTE + 150, NERVO,
           prog(t, T["nervo"], T["nervo"] + 0.25) * (1 - prog(t, T["devagar"] + 0.8, T["devagar"] + 1.3)), esq=False)
    rotulo(cv, "VASO", CX - 300, Y_CORTE + 320, CX - 104, Y_CORTE + 300, VASO,
           prog(t, T["vaso"], T["vaso"] + 0.25) * (1 - prog(t, T["devagar"] + 0.8, T["devagar"] + 1.3)))

    carimbo(cv, "DE PROPÓSITO", CX + 150, Y_CORTE - 150, -9, T["prop1"], t)
    carimbo(cv, "DE PROPÓSITO", CX - 120, Y_CORTE - 120, 7, T["prop2"], t)
    cv.restore()

    # ---------------- interface fixa (fora da câmera)
    # GANCHO ESCRITO no primeiro quadro: quem rola o feed sem som decide em 1 s, e a resposta
    # ("de propósito") só chega na voz aos ~3 s. É também a capa do reel no perfil.
    sai_g = e_inout(prog(t, T["cortar"] + 0.35, T["cortar"] + 0.85))
    if sai_g < 1:
        a = 1 - sai_g
        cv.drawRect(skia.Rect(0, 0, W, 360), paint(BG_OUT, 255, shader=skia.GradientShader.MakeLinear(
            [skia.Point(0, 0), skia.Point(0, 360)], [C(BG_OUT, int(235 * a)), C(BG_OUT, 0)])))
        pulso = 1 + 0.025 * math.sin(t * 5)
        cv.save(); cv.translate(CX, 205 - 60 * sai_g); cv.scale(pulso, pulso)
        texto(cv, "CORTAR O OSSO", 0, 0, F_BLACK, 78, "#FFFFFF", int(255 * a), contorno=10)
        texto(cv, "DE PROPÓSITO?", 0, 88, F_BLACK, 78, OURO, int(255 * a), contorno=10)
        cv.restore()
    # selo da série (entra quando o gancho sai)
    a0 = prog(t, T["cortar"] + 0.6, T["cortar"] + 1.0) * (1 - prog(t, T["manda"] - 0.3, T["manda"]))
    if a0 > 0:
        rr = skia.RRect.MakeRectXY(skia.Rect(CX - 190, 150, CX + 190, 204), 27, 27)
        cv.drawRRect(rr, paint("#FFFFFF", int(28 * a0)))
        texto(cv, "COMO FUNCIONA", CX, 190, F_BLACK, 32, OURO, int(255 * a0), track=4)

    # contador de dias e régua
    a_ui = prog(t, T["alguns"] - 0.2, T["alguns"] + 0.3) * (1 - prog(t, T["sai"] + 0.6, T["sai"] + 1.1))
    if a_ui > 0:
        texto(cv, "DIA", 92, 250, F_BLACK, 34, OURO, int(255 * a_ui), centro=False, track=3)
        texto(cv, f"{max(dia, 1)}", 88, 360, F_BLACK, 116, "#FFFFFF", int(255 * a_ui), centro=False)
        if t < T["dist_ini"]:
            texto(cv, "pausa", 94, 410, F_SEMI, 34, "#9CC9FF", int(255 * a_ui), centro=False)
        x = 968; ytop, ybot = 300, 1060
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 16, ytop, x + 16, ybot), 16, 16), paint("#FFFFFF", int(40 * a_ui)))
        alt = (ybot - ytop - 8) * (mm / MM_TOTAL)
        if alt > 0:
            cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 12, ybot - 4 - alt, x + 12, ybot - 4), 12, 12),
                         paint(OURO, int(255 * a_ui)))
        for k in range(0, MM_TOTAL + 1, 5):
            yy = ybot - 4 - (ybot - ytop - 8) * k / MM_TOTAL
            cv.drawLine(x - 30, yy, x - 20, yy, paint("#FFFFFF", int(120 * a_ui), "stroke", 2))
        texto(cv, f"+{int(round(mm))} mm", x - 4, ybot - 4 - alt - 22, F_BLACK, 40, OURO, int(255 * a_ui))

    # legendas (área segura: acima da faixa onde o Instagram desenha nome e legenda do post)
    t_cta = T["manda"] - 0.15
    if t < t_cta:
        legenda(cv, blocos, t)

    # identificação CFM (a partir de 3 s — decisão D9 — e completa no cartão final)
    if 3.0 <= t < t_cta:
        a = prog(t, 3.0, 3.6)
        texto(cv, "Dr. Rafael Vargas · Médico · CRM-SP 226103 · RQE 137901", CX, 1585, F_SEMI, 27, "#FFFFFF", int(200 * a))
        texto(cv, "Conteúdo educativo · não substitui avaliação médica · voz digital (IA)", CX, 1620, F_REG, 23, "#FFFFFF", int(150 * a))

    # CTA: a cena escurece e a frase de compartilhamento ocupa o centro da tela
    if t >= t_cta:
        a = prog(t, t_cta, t_cta + 0.35)
        cv.drawRect(skia.Rect(0, 0, W, H), paint(BG_OUT, int(175 * a)))
        legenda(cv, blocos, t, y_base=700, tam=92)
        aviao(cv, t, T["manda"] + 0.2)
        rr = skia.RRect.MakeRectXY(skia.Rect(150, 1060, 930, 1214), 28, 28)
        cv.drawRRect(rr, paint("#0B1824", int(230 * a)))
        cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 3))
        texto(cv, "Dr. Rafael Vargas · Médico ortopedista", CX, 1112, F_BLACK, 36, "#FFFFFF", int(255 * a))
        texto(cv, "CRM-SP 226103 · RQE 137901 · @rafaelvargasmd", CX, 1154, F_SEMI, 28, OURO, int(255 * a))
        texto(cv, "Conteúdo educativo · não substitui avaliação médica · voz digital (IA)", CX, 1190, F_REG, 22, "#FFFFFF", int(170 * a))

# ------------------------------------------------------------------ entrada única
def render(ep, mp4, tmp, previa=False):
    roteiro = "\n".join(ep["roteiro"])
    voz_bruta, palavras = _voz.narrar(roteiro, _voz.RITMO_COMO_FUNCIONA, os.path.join(tmp, "voz"))
    voz_c, pal, tirado = comprimir(voz_bruta, palavras)
    pal = alinhar(pal, roteiro)
    T = montar(pal)
    print(f"{ep['id']}: silêncio cortado {tirado:.2f}s | duração final {T['total']:.2f}s")
    blocos = montar_blocos(pal)

    def quadro_t(cv, t):
        quadro(cv, t, T, blocos, None)

    if previa:
        tempos = (0.4, T["cortar"] + 0.3, T["fixador"] + 0.8, T["acordar"] - 0.4, T["osso_novo"] + 0.6,
                  T["vaso"] + 0.6, T["devagar"] + 0.5, T["endurece"] + 1.6, T["sai"] + 0.6, T["manda"] + 1.6)
        return _previas(quadro_t, tempos, tmp, ep["id"]), T["total"]

    # eventos sonoros, presos às palavras
    ev = [(T["cortar"] + 0.08, "tick", 1.0), (T["prop1"] - 0.02, "thump", 0.9), (T["aparelho"] - 0.05, "whoosh", 0.8)]
    ev += [(T["aparelho"] + 0.07 * i + 0.42, "ping", 0.55) for i in range(4)]
    ev += [(T["fixador"] + 0.05, "whoosh", 0.35), (T["acordar"] + 0.12, "shimmer", 0.5),
           (T["osso_novo"] - 0.05, "shimmer", 0.85), (T["prop2"] - 0.02, "thump", 0.75),
           (T["endurece"] + 0.05, "crackle", 0.8), (T["sai"] - 0.1, "whoosh", 0.8), (T["sai"] + 0.5, "ding", 0.6),
           (T["manda"] + 0.05, "whoosh", 0.5)]
    for mm in range(1, MM_TOTAL + 1):                     # um clique por milímetro
        ev.append((lerp(T["dist_ini"], T["dist_fim"], mm / MM_TOTAL), "click", 0.9))
    wav = os.path.join(tmp, f"{ep['id']}_mix.wav")
    som.gravar_wav(wav, som.mixar(voz_c, T["total"], ev, ganho_trilha=0.40))
    codificar(quadro_t, T["total"], wav, mp4)
    return mp4, T["total"]
