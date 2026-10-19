# -*- coding: utf-8 -*-
"""COMO FUNCIONA — "Osso também pega infecção?" (osteomielite).

Mesmo estilo e mesmas peças das duas cenas aprovadas (osso marfim, osso novo dourado, rótulos,
carimbo ouro, checklist, legenda karaokê, CTA com aviãozinho). Storyboard e correções do
verificador (lote2_cf/cf_osteomielite_storyboard.json) respeitados aqui:
  * As portas de entrada (fratura exposta, cirurgia, sangue) deixam passar PONTINHOS vermelho-
    escuros, sem rosto e sem olhos: a infecção nunca vira personagem.
  * "Destruindo por dentro" = manchas cinza-amarronzadas crescendo devagar e o marfim ficando
    opaco. Sem tremor de câmera, sem som grave, sem pedaço solto; o osso continua opaco e
    esquemático (nada de exame, negativo, filme ou osso translúcido).
  * Etapa 3 condicional ("3 RECONSTRUIR, SE SOBRAR VÃO") e o vão se enche AOS POUCOS, sem
    completar em cena e sem explosão de brilho (o acervo: "bem devagar ... processo longo").
  * Alarme pós-operatório com os 4 gatilhos do acervo (febre, pus, ferida que abriu, vermelhidão
    se alastrando) e a conduta: pronto-socorro na hora, avisando a equipe.
Cena PRESA ao roteiro pelas palavras-âncora: roteiro sem elas = KeyError, não vídeo torto.
"""
import math

import numpy as np
import skia

from .cf_alongamento import (CX, F_BLACK, F_SEMI, HASTE, OSSO_C, OSSO_L, OURO, VASO, VERMELHO, W,
                             Y_BASE, Y_TOPO, C, clamp, desenha_regenerado, e_back, e_in_back, e_inout, e_out, fundo,
                             lerp, lerpc, paint, path_osso_inf, path_osso_sup, prog, rotulo, sombra_osso,
                             texto)
from .cf_comum import capa, fazer_render, interface, selo_como_funciona

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "osteo": ("osteomielite", 1, False),
    "entrar": ("entrar", 1, False),
    "fratura": ("fratura", 1, False),
    "exposta": ("exposta", 1, False),
    "cirurgia": ("cirurgia", 1, False),
    "sangue": ("sangue", 1, False),
    "instalada": ("instalada", 1, False),
    "destruindo": ("destruindo", 1, False),
    "dentro": ("dentro", 1, False),
    "dor": ("dor", 1, False),
    "inchaco": ("inchaço", 1, False),
    "calor": ("calor", 1, False),
    "verm1": ("vermelhidão", 1, False),
    "febre1": ("febre", 1, False),
    "secrecao": ("secreção", 1, False),
    "ignore": ("ignore", 1, False),
    "tratamento": ("tratamento", 1, False),
    "combater": ("combater", 1, False),
    "remover": ("remover", 1, False),
    "doente": ("doente", 1, False),
    "vao": ("vão", 1, False),
    "reconstruir": ("reconstruir", 1, False),
    "operou": ("operou", 1, False),
    "febre2": ("febre", 2, False),
    "pus": ("pus", 1, False),
    "ferida": ("ferida", 1, False),
    "abriu": ("abriu", 1, False),
    "verm2": ("vermelhidão", 2, False),
    "alastrando": ("alastrando", 1, False),
    "pronto": ("pronto-socorro", 1, False),
    "hora": ("hora", 1, False),
    "avisando": ("avisando", 1, False),
    "equipe": ("equipe", 1, False),
    "manda": ("manda", 1, False),
}
DESTAQUE = {"osteomielite", "exposta", "cirurgia", "sangue", "destruindo", "dentro", "ignore", "tratamento",
            "combater", "remover", "doente", "reconstruir", "febre", "pus", "abriu", "alastrando",
            "pronto-socorro", "equipe"}

# ------------------------------------------------------------------ geometria (mundo)
YM = 745                       # meio da diáfise: onde a infecção se instala
Y1, Y2 = 655, 835              # cortes acima e abaixo do trecho doente
SY = 790                       # âncora vertical da câmera na tela
H2 = HASTE / 2
COR_MANCHA, COR_MANCHA_B = "#8C7B66", "#64564A"
COR_PONTO = "#8E1B22"
COR_PUS = "#E3C25B"


def _osso_path():
    return skia.Op(path_osso_sup(Y_TOPO, YM + 4), path_osso_inf(YM - 4, Y_BASE), skia.PathOp.kUnion_PathOp)


OSSO = _osso_path()
RNG = np.random.default_rng(31)
ALVOS = []                      # onde cada pontinho se aloja no osso (mundo)
while len(ALVOS) < 18:
    _dx, _dy = RNG.uniform(-44, 44), RNG.uniform(-56, 56)
    if (_dx / 47) ** 2 + (_dy / 64) ** 2 <= 1:
        ALVOS.append((CX + _dx, YM + _dy, RNG.uniform(0, 6.28)))
MANCHAS = [(-16, -30, 22, 0.3), (22, -6, 19, 1.7), (-10, 18, 23, 2.9), (24, 36, 16, 4.1), (-24, 40, 15, 5.0),
           (8, -40, 14, 0.9)]


def camera(t, T):
    """-> (bx, s, fy): o ponto do mundo (CX, fy) vai para (bx, SY) na tela, com escala s."""
    bx, s, fy = 540.0, 1.0, 725.0
    k = e_inout(prog(t, T["instalada"] + 0.3, T["destruindo"] + 0.3))       # aproxima no trecho
    s = lerp(s, 1.1, k); fy = lerp(fy, 770.0, k)
    # abre espaço p/ o checklist ANTES de as caixinhas chegarem (elas entram pela direita)
    k = e_inout(prog(t, T["dor"] - 0.4, T["dor"] + 0.35))
    bx = lerp(bx, 280.0, k)
    # abre espaço p/ as etapas só DEPOIS de o checklist sair (nada de texto fantasma sobre o osso)
    k = e_inout(prog(t, T["tratamento"] + 0.05, T["tratamento"] + 0.65))
    bx = lerp(bx, 810.0, k); s = lerp(s, 1.05, k); fy = lerp(fy, 738.0, k)
    # recentra enquanto o cartão do alerta cobre tudo: na CTA o osso fica no meio, como no aprovado
    k = e_inout(prog(t, T["operou"] + 0.6, T["operou"] + 1.6))
    bx = lerp(bx, 540.0, k); s = lerp(s, 1.0, k); fy = lerp(fy, 725.0, k)
    return bx, s, fy


def tela(cam, x, y):
    bx, s, fy = cam
    return bx + s * (x - CX), SY + s * (y - fy)


# ------------------------------------------------------------------ desenho: utilidades
def _blob(x, y, r, ph, n=26):
    p = skia.Path()
    for k in range(n):
        th = 2 * math.pi * k / n
        rr = r * (1 + 0.2 * math.sin(3 * th + ph) + 0.1 * math.sin(5 * th + 2 * ph))
        px, py = x + rr * math.cos(th), y + rr * math.sin(th) * 1.15
        (p.moveTo if k == 0 else p.lineTo)(px, py)
    p.close()
    return p


def tracejado(cv, x0, y0, x1, y1, cor, a, w=5, traco=16, vao=11):
    L = math.hypot(x1 - x0, y1 - y0)
    if L <= 0 or a <= 0:
        return
    ux, uy = (x1 - x0) / L, (y1 - y0) / L; d = 0.0
    while d < L:
        e = min(L, d + traco)
        cv.drawLine(x0 + ux * d, y0 + uy * d, x0 + ux * e, y0 + uy * e, paint(cor, int(a), "stroke", w))
        d += traco + vao


def pilula(cv, s, cx, y, cor, a, tam=34, esq=None):
    """Rótulo sem linha-guia (nome de cada porta). `esq`: x da borda esquerda (senão, centrado)."""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    x0 = esq if esq is not None else cx - lw / 2 - 16
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y - tam * 0.95, x0 + lw + 32, y + tam * 0.33), 13, 13)
    cv.drawRRect(rr, paint("#0B1824", int(215 * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 2.5))
    cv.drawString(s, x0 + 16, y, f, paint(cor, int(255 * a)))


def termometro(cv, x, y, nivel, a, esc=1.0):
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-12, -48, 12, 24), 12, 12), paint("#EEF3F8", int(255 * a)))
    cv.drawCircle(0, 32, 19, paint("#EEF3F8", int(255 * a)))
    cv.drawCircle(0, 32, 13, paint(VERMELHO, int(255 * a)))
    h = lerp(6, 64, clamp(nivel))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-5, 26 - h, 5, 32), 5, 5), paint(VERMELHO, int(255 * a)))
    for k in range(4):
        cv.drawLine(5, -30 + k * 14, 11, -30 + k * 14, paint("#8FA3B8", int(220 * a), "stroke", 2))
    cv.restore()


def gota(cv, x, y, r, cor, a):
    if a <= 0 or r <= 0:
        return
    p = skia.Path()
    p.moveTo(x, y - 1.75 * r)
    p.cubicTo(x + 0.35 * r, y - 1.1 * r, x + r, y - 0.55 * r, x + r, y + 0.1 * r)
    p.cubicTo(x + r, y + 0.72 * r, x + 0.56 * r, y + r, x, y + r)
    p.cubicTo(x - 0.56 * r, y + r, x - r, y + 0.72 * r, x - r, y + 0.1 * r)
    p.cubicTo(x - r, y - 0.55 * r, x - 0.35 * r, y - 1.1 * r, x, y - 1.75 * r)
    p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))
    cv.drawOval(skia.Rect(x - 0.55 * r, y - 0.35 * r, x - 0.2 * r, y + 0.25 * r), paint("#FFFFFF", int(150 * a)))


def raio(cv, x, y, a, esc=1.0):
    """Raio em zigue-zague (dor)."""
    if a <= 0:
        return
    pts = [(6, -46), (-16, -2), (2, -2), (-8, 46), (20, -8), (2, -8), (16, -46)]
    p = skia.Path(); p.moveTo(x + pts[0][0] * esc, y + pts[0][1] * esc)
    for px, py in pts[1:]:
        p.lineTo(x + px * esc, y + py * esc)
    p.close()
    cv.drawPath(p, paint(OURO, int(110 * a), blur=10))
    cv.drawPath(p, paint(OURO, int(255 * a)))
    cv.drawPath(p, paint("#8A5A00", int(255 * a), "stroke", 2))


def cruz(cv, x, y, lado, a):
    rr = skia.RRect.MakeRectXY(skia.Rect(x - lado / 2, y - lado / 2, x + lado / 2, y + lado / 2), 14, 14)
    cv.drawRRect(rr, paint("#E5484D", int(255 * a)))
    b = lado * 0.13; L = lado * 0.33
    cv.drawRect(skia.Rect(x - b, y - L, x + b, y + L), paint("#FFFFFF", int(255 * a)))
    cv.drawRect(skia.Rect(x - L, y - b, x + L, y + b), paint("#FFFFFF", int(255 * a)))


def telefone(cv, x, y, a, toque, t):
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(1.25, 1.25); cv.rotate(-28 + 9 * math.sin(t * 46) * toque)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-24, -42, 4, -22), 8, 8), paint("#FFFFFF", int(255 * a)))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-24, 22, 4, 42), 8, 8), paint("#FFFFFF", int(255 * a)))
    p = skia.Path(); p.moveTo(-14, -30); p.quadTo(-40, 0, -14, 30)
    cv.drawPath(p, paint("#FFFFFF", int(255 * a), "stroke", 14))
    cv.restore()
    if toque > 0:                                              # ondas de chamada
        for i in range(2):
            f = ((t * 1.8) + i * 0.5) % 1.0
            r = 30 + 22 * f
            cv.drawArc(skia.Rect(x - r + 14, y - r, x + r + 14, y + r), -40, 80, False,
                       paint(OURO, int(255 * a * toque * (1 - f)), "stroke", 4))


# ------------------------------------------------------------------ portas de entrada (tela)
# (x, y) = canto superior esquerdo da porta, lado da dobradiça, palavra que dá nome, palavra que abre
PW, PH = 120, 180
PORTAS = ((110, 730, "esq", "fratura", "exposta", "FRATURA EXPOSTA"),
          (830, 470, "dir", "cirurgia", "cirurgia", "CIRURGIA"),
          (830, 905, "dir", "sangue", "sangue", "SANGUE"))


def _porta_dx(t, T, i):
    lado = -1 if PORTAS[i][2] == "esq" else 1
    entra = e_back(prog(t, T["entrar"] + 0.1 * i, T["entrar"] + 0.1 * i + 0.55))
    sai = e_in_back(prog(t, T["destruindo"] - 0.55, T["destruindo"] + 0.05))
    return lado * (380 * (1 - entra) + 420 * sai)


def _alpha_portas(t, T):
    return clamp(prog(t, T["entrar"], T["entrar"] + 0.25)) * (1 - prog(t, T["destruindo"] - 0.3, T["destruindo"] + 0.05))


def porta(cv, i, t, T):
    x, y, dobra, _, t_abre, _ = PORTAS[i]
    a = _alpha_portas(t, T)
    if a <= 0:
        return
    x += _porta_dx(t, T, i)
    ang = math.radians(78) * e_out(prog(t, T[t_abre], T[t_abre] + 0.45))
    # vão da porta: luz quente quando abre
    cv.drawRect(skia.Rect(x, y, x + PW, y + PH), paint("#06101A", int(235 * a)))
    if ang > 0:
        luz = ang / math.radians(78)
        sh = skia.GradientShader.MakeLinear([skia.Point(x, y), skia.Point(x, y + PH)],
                                            [C("#FFF4D8", int(235 * a * luz)), C("#F5C04A", int(170 * a * luz))])
        cv.drawRect(skia.Rect(x + 4, y + 4, x + PW - 4, y + PH - 4), paint("#FFF4D8", 255, shader=sh))
    cv.drawRect(skia.Rect(x - 3, y - 3, x + PW + 3, y + PH + 3), paint(OURO, int(200 * a), "stroke", 3))  # batente
    # folha da porta girando na dobradiça, com perspectiva (a borda livre vem para a frente)
    hx = x if dobra == "esq" else x + PW
    fx = hx + (1 if dobra == "esq" else -1) * PW * math.cos(ang)
    lift = 24 * math.sin(ang)
    m = skia.Matrix()
    m.setPolyToPoly([skia.Point(0, 0), skia.Point(PW, 0), skia.Point(PW, PH), skia.Point(0, PH)],
                    [skia.Point(hx, y), skia.Point(fx, y - lift), skia.Point(fx, y + PH + lift), skia.Point(hx, y + PH)])
    cv.save(); cv.concat(m)
    escurece = lerpc("#1B4866", "#0E2638", clamp(ang / math.radians(78)))
    cv.drawRect(skia.Rect(0, 0, PW, PH), paint(escurece, int(255 * a)))
    cv.drawRect(skia.Rect(0, 0, PW, PH), paint(OURO, int(255 * a), "stroke", 4))
    cv.drawRect(skia.Rect(14, 14, PW - 14, PH * 0.46), paint(OURO, int(90 * a), "stroke", 2.5))
    cv.drawRect(skia.Rect(14, PH * 0.54, PW - 14, PH - 14), paint(OURO, int(90 * a), "stroke", 2.5))
    cv.drawCircle(PW - 20, PH * 0.5, 8, paint(OURO, int(255 * a)))         # maçaneta redonda
    if i == 0:                                                           # zigue-zague de fratura
        p = skia.Path(); p.moveTo(18, 42)
        for k in range(1, 7):
            p.lineTo(18 + k * (PW - 36) / 6, 42 + (12 if k % 2 else -2))
        cv.drawPath(p, paint(VERMELHO, int(255 * a), "stroke", 5))
    if i == 2:                                                           # gota de sangue
        gota(cv, PW / 2 - 6, 52, 13, VASO, a)
    cv.restore()


def _saida_porta(t, T, i):
    x, y, dobra = PORTAS[i][:3]
    x += _porta_dx(t, T, i)
    return (x + PW - 18, y + PH * 0.5) if dobra == "esq" else (x + 18, y + PH * 0.5)


def _vaso_pts(t, T, cam, n=60):
    """Vaso ondulado da porta SANGUE até a borda do osso (tela)."""
    sx, sy = _saida_porta(t, T, 2)
    ex, ey = tela(cam, CX + H2 - 2, YM + 30)
    p1 = (sx - 110, sy + 10); p2 = (ex + 110, ey + 50)
    pts = []
    for k in range(n + 1):
        u = k / n; v = 1 - u
        x = v ** 3 * sx + 3 * v * v * u * p1[0] + 3 * v * u * u * p2[0] + u ** 3 * ex
        y = v ** 3 * sy + 3 * v * v * u * p1[1] + 3 * v * u * u * p2[1] + u ** 3 * ey
        pts.append([x, y])
    for k in range(1, n):                                       # ondulação perpendicular
        dx, dy = pts[k + 1][0] - pts[k - 1][0], pts[k + 1][1] - pts[k - 1][1]; L = math.hypot(dx, dy) or 1
        off = 6.5 * math.sin(k / n * 3.5 * 2 * math.pi + t * 1.4) * math.sin(math.pi * k / n)
        pts[k][0] += -dy / L * off; pts[k][1] += dx / L * off
    return pts


def _no_vaso(pts, u):
    f = clamp(u) * (len(pts) - 1); k = min(int(f), len(pts) - 2); r = f - k
    return lerp(pts[k][0], pts[k + 1][0], r), lerp(pts[k][1], pts[k + 1][1], r)


def vaso(cv, t, T, cam):
    a = clamp(prog(t, T["sangue"] + 0.1, T["sangue"] + 0.3)) * (1 - prog(t, T["destruindo"] - 0.4, T["destruindo"]))
    if a <= 0:
        return
    cresce = e_out(prog(t, T["sangue"] + 0.15, T["sangue"] + 0.6))
    pts = _vaso_pts(t, T, cam)
    m = max(2, int(len(pts) * cresce))
    p = skia.Path(); p.moveTo(*pts[0])
    for x, y in pts[1:m]:
        p.lineTo(x, y)
    cv.drawPath(p, paint(VASO, int(90 * a), "stroke", 16, blur=5))
    cv.drawPath(p, paint(VASO, int(255 * a), "stroke", 10))


# ------------------------------------------------------------------ pontinhos (tela)
def _bez(p0, c, p1, u):
    v = 1 - u
    return v * v * p0[0] + 2 * v * u * c[0] + u * u * p1[0], v * v * p0[1] + 2 * v * u * c[1] + u * u * p1[1]


def pontinhos(cv, t, T, cam):
    s = cam[1]
    some = prog(t, T["combater"], T["combater"] + 0.9)
    if some >= 1:
        return
    for j, (tx, ty, ph) in enumerate(ALVOS):
        porta_i, k = divmod(j, 6)
        t_abre = T[PORTAS[porta_i][4]]
        t0 = t_abre + 0.3 + 0.11 * k
        if t < t0:
            continue
        alvo = tela(cam, tx + 2.0 * math.sin(t * 1.3 + ph), ty + 2.0 * math.cos(t * 1.1 + ph))
        if porta_i < 2:
            u = e_inout(clamp((t - t0) / 0.8))
            ini = _saida_porta(t, T, porta_i)
            ctrl = ((ini[0] + alvo[0]) / 2, min(ini[1], alvo[1]) - 70)
            x, y = _bez(ini, ctrl, alvo, u) if u < 1 else alvo
        else:                                                   # pelo sangue: corre dentro do vaso
            u = (t - t0) / 0.75
            if u < 1:
                x, y = _no_vaso(_vaso_pts(t, T, cam), e_inout(u))
            else:
                fim = _no_vaso(_vaso_pts(t, T, cam), 1.0)
                w = e_inout(clamp((u - 1) * 0.75 / 0.3))
                x, y = lerp(fim[0], alvo[0], w), lerp(fim[1], alvo[1], w)
        r = 7.5 * s * (1 - 0.6 * some)
        a = clamp((t - t0) / 0.15) * (1 - some)
        cv.drawCircle(x, y, r + 3, paint("#FF8A8F", int(110 * a)))
        cv.drawCircle(x, y, r, paint(COR_PONTO, int(255 * a)))


# ------------------------------------------------------------------ osso, manchas, corte, vão (mundo)
def _conteudo_trecho(cv, t, T):
    """Manchas + marfim opaco DENTRO do trecho doente (mundo, sem recorte)."""
    g0 = T["destruindo"]
    a_op = e_inout(prog(t, g0, g0 + 1.8))
    if a_op > 0:
        sh = skia.GradientShader.MakeLinear([skia.Point(0, Y1), skia.Point(0, Y2)],
                                            [C("#B5A68D", 0), C("#B5A68D", int(200 * a_op)),
                                             C("#B5A68D", int(200 * a_op)), C("#B5A68D", 0)], [0.0, 0.22, 0.78, 1.0])
        cv.drawRect(skia.Rect(CX - 90, Y1, CX + 90, Y2), paint("#B5A68D", 255, shader=sh))
    for i, (dx, dy, r, ph) in enumerate(MANCHAS):
        g = e_out(prog(t, g0 + 0.12 * i, g0 + 1.5 + 0.12 * i)) * (1 + 0.1 * prog(t, g0 + 1.6, T["tratamento"]))
        if g <= 0:
            continue
        p = _blob(CX + dx, YM + dy, r * g, ph)
        cv.drawPath(p, paint(COR_MANCHA, 235))
        cv.drawPath(p, paint(COR_MANCHA_B, 200, "stroke", 2.5))


def _parte(cv, clip_rect, dx=0.0):
    sh = sombra_osso()
    cv.save(); cv.translate(dx, 0); cv.clipRect(clip_rect)
    cv.drawPath(OSSO, paint("#000000", 70, blur=14))
    cv.drawPath(OSSO, paint(OSSO_C, shader=sh))
    cv.drawPath(OSSO, paint(OSSO_L, 150, "stroke", 2.5))
    cv.restore()


def osso(cv, t, T):
    t_corte = T["remover"] + 0.35
    if t < t_corte:
        _parte(cv, skia.Rect(0, -2000, W, 4000))
        cv.save(); cv.clipPath(OSSO, skia.ClipOp.kIntersect, True); cv.clipRect(skia.Rect(0, Y1 + 3, W, Y2 - 3))
        _conteudo_trecho(cv, t, T)
        cv.restore()
        return
    _parte(cv, skia.Rect(0, -2000, W, Y1))
    _parte(cv, skia.Rect(0, Y2, W, 4000))
    for y in (Y1, Y2):                                          # pontas limpas do corte
        cv.drawLine(CX - H2 + 1, y, CX + H2 - 1, y, paint(OSSO_L, 170, "stroke", 2.5))
    # o trecho doente desliza para o lado e some
    dx = trecho_dx(t, T)
    a = 1 - prog(t, T["doente"] + 0.6, T["doente"] + 1.1)        # fica legível até perto de "vão"
    if a > 0:
        cv.saveLayerAlpha(skia.Rect(0, Y1 - 60, W, Y2 + 60), int(255 * a))
        _parte(cv, skia.Rect(0, Y1, W, Y2), dx)
        cv.save(); cv.translate(dx, 0); cv.clipPath(OSSO, skia.ClipOp.kIntersect, True)
        cv.clipRect(skia.Rect(0, Y1 + 3, W, Y2 - 3))
        _conteudo_trecho(cv, t, T)
        cv.restore()
        cv.drawLine(CX - H2 + 1 + dx, Y1, CX + H2 - 1 + dx, Y1, paint(OSSO_L, 170, "stroke", 2.5))
        cv.drawLine(CX - H2 + 1 + dx, Y2, CX + H2 - 1 + dx, Y2, paint(OSSO_L, 170, "stroke", 2.5))
        cv.restore()


def trecho_dx(t, T):
    return -300 * e_inout(prog(t, T["doente"] - 0.2, T["doente"] + 0.9))


def cortes(cv, t, T):
    k0 = T["remover"]
    if k0 - 0.05 <= t < k0 + 0.45:                               # linhas tracejadas piscando
        pisca = 0.5 + 0.5 * math.sin(t * 18)
        for y in (Y1, Y2):
            tracejado(cv, CX - 100, y, CX + 100, y, VERMELHO, 120 + 135 * pisca, w=5)
    for y, t0 in ((Y1, k0 + 0.2), (Y2, k0 + 0.35)):             # o traço de corte do alongamento
        k = t - t0
        if 0 <= k < 0.6:
            a = 1 - k / 0.6
            cv.drawLine(CX - 120, y, CX + 120, y, paint(VERMELHO, int(220 * a), "stroke", 16, blur=10))
            ab = 100 * e_out(clamp(k / 0.12))
            cv.drawLine(CX - ab, y, CX + ab, y, paint("#FFFFFF", int(255 * a), "stroke", 4))


def vao_e_reconstrucao(cv, t, T):
    if t < T["remover"] + 0.35:
        return
    # osso novo dourado, de baixo para cima e DEVAGAR: não completa em cena
    f = 0.6 * e_out(prog(t, T["reconstruir"], T["reconstruir"] + 6.0))
    if f > 0.004:
        desenha_regenerado(cv, Y2 - f * (Y2 - Y1), Y2, 0.85, 0.35, 0.0, t)
    a = prog(t, T["vao"] - 0.1, T["vao"] + 0.2)
    if a > 0:
        pisca = 0.55 + 0.45 * math.sin(t * 8)
        aa = 255 * a * pisca * (1 - 0.4 * prog(t, T["reconstruir"] + 1.5, T["reconstruir"] + 2.5))
        x0, x1 = CX - H2 - 6, CX + H2 + 6
        tracejado(cv, x0, Y1 + 4, x1, Y1 + 4, OURO, aa, w=4, traco=12, vao=9)
        tracejado(cv, x1, Y1 + 4, x1, Y2 - 4, OURO, aa, w=4, traco=12, vao=9)
        tracejado(cv, x1, Y2 - 4, x0, Y2 - 4, OURO, aa, w=4, traco=12, vao=9)
        tracejado(cv, x0, Y2 - 4, x0, Y1 + 4, OURO, aa, w=4, traco=12, vao=9)


def anel_capa(cv, t, T):
    """Anel vermelho tracejado piscando em volta do meio do osso (capa)."""
    a = 1 - prog(t, T["osteo"] + 0.5, T["entrar"])
    if a <= 0:
        return
    pisca = 0.5 + 0.5 * math.sin(t * 7)
    r = skia.Rect(CX - 118, YM - 92, CX + 118, YM + 92)
    for k in range(16):
        cv.drawArc(r, k * 22.5 + t * 20, 13, False, paint(VERMELHO, int((130 + 125 * pisca) * a), "stroke", 6))


def halo(cv, t, T):
    a = prog(t, T["inchaco"] - 0.1, T["inchaco"] + 0.4) * (1 - prog(t, T["combater"], T["combater"] + 0.9))
    if a <= 0:
        return
    infla = e_back(prog(t, T["inchaco"], T["inchaco"] + 0.6))
    vermelho = e_inout(prog(t, T["verm1"], T["verm1"] + 0.45))
    cor = lerpc("#DCEBFF", "#FF4A50", vermelho)
    rx = lerp(110, 150, infla) + 4 * math.sin(t * 3.0); ry = lerp(105, 145, infla) + 4 * math.sin(t * 3.0)
    cv.drawOval(skia.Rect(CX - rx, YM - ry, CX + rx, YM + ry), paint(cor, int(lerp(120, 170, vermelho) * a), blur=30))


def sinais_no_osso(cv, t, T):
    fim = 1 - prog(t, T["tratamento"], T["tratamento"] + 0.4)
    a = prog(t, T["dor"], T["dor"] + 0.15) * fim
    if a > 0:                                                    # dor: raio piscando ao lado do trecho
        raio(cv, CX - 132, YM - 30, a * (0.55 + 0.45 * abs(math.sin(t * 6))), 1.15)
    a = prog(t, T["calor"] - 0.05, T["calor"] + 0.3) * fim
    if a > 0:                                                    # calor: 3 ondas juntas subindo do halo
        f = ((t - T["calor"]) * 0.9) % 1.0
        sobe = 34 * f; aa = a * math.sin(math.pi * clamp(f * 1.15))
        for i in range(3):
            x = CX + H2 + 34 + i * 30
            y0 = YM - 40 - sobe
            p = skia.Path(); p.moveTo(x, y0)
            for k in range(1, 15):
                p.lineTo(x + 6 * math.sin(k * 0.85 + i * 0.4), y0 - k * 5.5)
            cv.drawPath(p, paint("#FF8A3D", int(120 * aa), "stroke", 12, blur=6))
            cv.drawPath(p, paint("#FFB070", int(255 * aa), "stroke", 5.5))


# ------------------------------------------------------------------ interface da cena (tela)
def etiqueta_osteo(cv, t, T, cam):
    a = prog(t, T["osteo"], T["osteo"] + 0.25) * (1 - prog(t, T["entrar"] + 0.05, T["entrar"] + 0.35))
    if a <= 0:
        return
    xa, ya = tela(cam, CX - H2 + 10, YM)                      # aponta DENTRO da diáfise
    f = skia.Font(F_BLACK, 46); lw = f.measureText("OSTEOMIELITE")
    x0, y0 = 50, 590
    cv.drawLine(xa, ya, x0 + lw + 20, y0 + 30, paint(VERMELHO, int(220 * a), "stroke", 3))
    cv.drawCircle(xa, ya, 7, paint(VERMELHO, int(255 * a)))
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x0 + lw + 34, y0 + 62), 14, 14)
    cv.drawRRect(rr, paint("#0B1824", int(220 * a))); cv.drawRRect(rr, paint(VERMELHO, int(255 * a), "stroke", 3))
    cv.drawString("OSTEOMIELITE", x0 + 17, y0 + 48, f, paint("#FFFFFF", int(255 * a)))
    texto(cv, "infecção no osso", x0 + 6, y0 + 108, F_SEMI, 36, "#9CC9FF", int(255 * a), centro=False, contorno=6)


def carimbo_opaco(cv, s, x, y, rot, t0, t, dur, tam=62, esc0=1.9):
    """Carimbo ouro torto (o mesmo do cf_fratura_cola), com fundo opaco: legível sobre o osso claro.
    `esc0`: escala da batida (menor nos carimbos largos, para não estourar as bordas da tela)."""
    k = t - t0
    if k < 0 or k > dur:
        return
    esc = lerp(esc0, 1.0, e_out(clamp(k / 0.16))); a = clamp(k / 0.08) * (1 - prog(k, dur - 0.35, dur))
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(esc, esc)
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 24, -tam, lw / 2 + 24, tam * 0.36), 12, 12)
    cv.drawRRect(rr, paint("#0B1824", int(240 * a))); cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 7))
    cv.drawString(s, -lw / 2, 0, f, paint(OURO, int(255 * a)))
    cv.restore()


def checklist_sinais(cv, t, T):
    # sai ANTES de a câmera levar o osso para a direita
    a_g = prog(t, T["dor"] - 0.1, T["dor"] + 0.3) * (1 - prog(t, T["tratamento"] - 0.1, T["tratamento"] + 0.15))
    a_g *= 1 - 0.3 * prog(t, T["ignore"], T["ignore"] + 0.15)       # o carimbo ganha a cena, a lista segue legível
    if a_g <= 0:
        return
    itens = (("DOR QUE NÃO PASSA", T["dor"]), ("INCHAÇO", T["inchaco"]), ("CALOR", T["calor"]),
             ("VERMELHIDÃO", T["verm1"]), ("ÀS VEZES FEBRE", T["febre1"]), ("OU SECREÇÃO", T["secrecao"]))
    x0 = 520 + 220 * (1 - e_out(prog(t, T["dor"] - 0.1, T["dor"] + 0.35)))   # entra pela direita
    for k, (rot, t_ok) in enumerate(itens):
        y = 470 + k * 95
        rr = skia.RRect.MakeRectXY(skia.Rect(x0, y - 42, x0 + 50, y + 8), 10, 10)
        cv.drawRRect(rr, paint("#0B1824", int(220 * a_g))); cv.drawRRect(rr, paint(OURO, int(255 * a_g), "stroke", 3.5))
        if t >= t_ok:
            pr = e_out(clamp((t - t_ok) / 0.3))
            p = skia.Path(); p.moveTo(x0 + 10, y - 18)
            p.lineTo(x0 + 10 + 12 * min(1, pr * 2), y - 18 + 12 * min(1, pr * 2))
            if pr > 0.5:
                q = (pr - 0.5) * 2
                p.lineTo(x0 + 22 + 22 * q, y - 6 - 30 * q)
            cv.drawPath(p, paint(OURO, int(255 * a_g), "stroke", 6))
            ai = a_g * clamp((t - t_ok) / 0.2)
            texto(cv, rot, x0 + 66, y - 4, F_BLACK, 36, "#FFFFFF", int(255 * ai), centro=False, contorno=8)
            if k == 4:
                termometro(cv, 975, y - 22, e_out(prog(t, t_ok, t_ok + 0.9)) * 0.85, ai, 0.72)
            if k == 5:
                gota(cv, 975, y - 14, 17 * e_back(prog(t, t_ok, t_ok + 0.4)), COR_PUS, ai)


def etapas(cv, t, T):
    # entram com o osso já parado à direita; saem na palavra "operou", antes de o cartão chegar
    a = prog(t, T["tratamento"] + 0.6, T["tratamento"] + 0.85) * (1 - prog(t, T["operou"], T["operou"] + 0.2))
    if a <= 0:
        return
    for i, (rot, t_on) in enumerate((("1 COMBATER A INFECÇÃO", T["combater"]), ("2 REMOVER O OSSO DOENTE", T["remover"]),
                                     ("3 RECONSTRUIR, SE SOBRAR VÃO", T["reconstruir"]))):
        y = 292 + i * 60; on = t >= t_on
        pr = e_back(prog(t, t_on, t_on + 0.35)) if on else 0
        if on:
            cv.drawCircle(72, y - 11, 20 * pr, paint(OURO, int(90 * a), blur=8))
            cv.drawCircle(72, y - 11, 14 * pr, paint(OURO, int(255 * a)))
        else:
            cv.drawCircle(72, y - 11, 14, paint("#FFFFFF", int(90 * a), "stroke", 3))
        texto(cv, rot, 100, y, F_BLACK, 30, "#FFFFFF" if on else "#8FA3B8", int(255 * a), centro=False, contorno=6)


def rotulos_tratamento(cv, t, T, cam):
    # OSSO DOENTE acompanha o trecho enquanto ele sai
    a = prog(t, T["doente"], T["doente"] + 0.2) * (1 - prog(t, T["doente"] + 0.65, T["doente"] + 1.1))
    if a > 0:
        dx = trecho_dx(t, T)
        xa, ya = tela(cam, CX - H2 + dx, YM - 30)
        rotulo(cv, "OSSO DOENTE", max(60, xa - 360), ya - 70, xa, ya, "#D9C7A8", a)   # nunca sai da borda
    a = prog(t, T["vao"], T["vao"] + 0.2) * (1 - prog(t, T["operou"], T["operou"] + 0.2))
    if a > 0:
        xa, ya = tela(cam, CX - H2 - 6, YM)
        rotulo(cv, "VÃO", xa - 230, ya + 20, xa, ya, OURO, a)


# ------------------------------------------------------------------ alerta pós-operatório (tela)
def icone_ferida(cv, y, ab, a):
    """Corte reto com 4 pontos de sutura; as duas bordas se afastam (ab 0..1). Sem sangue, sem pele."""
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(112, y - 32, 208, y + 32), 16, 16), paint("#5E7186", int(255 * a)))
    g = 11 * ab
    if g > 0.5:
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(126, y - g, 194, y + g), g, g), paint("#0B1824", int(255 * a)))
    for yy in (y - g, y + g):
        cv.drawLine(126, yy, 194, yy, paint("#E6EEF6", int(255 * a), "stroke", 4))
    for k in range(4):
        x = 134 + k * 17
        cv.drawLine(x, y - g - 9, x, y - g, paint("#E6EEF6", int(255 * a), "stroke", 3))
        cv.drawLine(x, y + g, x, y + g + 9, paint("#E6EEF6", int(255 * a), "stroke", 3))


def icone_vermelhidao(cv, y, k, a):
    """Mesmo quadrado neutro da ferida, com uma mancha rosada difusa que cresce (vermelhidão da pele)."""
    rr = skia.RRect.MakeRectXY(skia.Rect(112, y - 32, 208, y + 32), 16, 16)
    cv.drawRRect(rr, paint("#5E7186", int(255 * a)))
    cv.save(); cv.clipRRect(rr, skia.ClipOp.kIntersect, True)
    r = lerp(10, 58, k)
    sh = skia.GradientShader.MakeRadial(skia.Point(160, y), r,
                                        [C("#FF6A6F", int(230 * a)), C("#FF6A6F", int(120 * a)), C("#FF6A6F", 0)],
                                        [0.0, 0.55, 1.0])
    cv.drawCircle(160, y, r, paint("#FF6A6F", 255, shader=sh))
    cv.restore()


def alerta(cv, t, T):
    # véu: entra NA palavra e sai junto com o véu da CTA (cruzado) — o osso nunca volta a acender
    ov = prog(t, T["operou"], T["operou"] + 0.3) * (1 - prog(t, T["manda"] - 0.15, T["manda"] + 0.35))
    if ov > 0:
        cv.drawRect(skia.Rect(0, 0, W, 1920), paint("#0A1520", int(240 * ov)))
    t_in = T["operou"] + 0.15                                    # o cartão chega depois de as etapas saírem
    a_g = prog(t, t_in - 0.05, t_in + 0.35) * (1 - prog(t, T["manda"] - 0.45, T["manda"] - 0.1))
    if a_g <= 0:
        return
    esc = lerp(0.9, 1.0, e_back(prog(t, t_in, t_in + 0.45)))
    cv.save(); cv.translate(540, 720); cv.scale(esc, esc); cv.translate(-540, -720)
    card = skia.RRect.MakeRectXY(skia.Rect(70, 250, 1010, 1190), 30, 30)
    cv.drawRRect(card, paint("#0B1824", int(255 * a_g)))
    cv.drawRRect(card, paint(VERMELHO, int(255 * a_g), "stroke", 6))
    texto(cv, "DEPOIS DA CIRURGIA", 540, 340, F_BLACK, 46, VERMELHO, int(255 * a_g))
    cv.drawLine(160, 378, 920, 378, paint(VERMELHO, int(110 * a_g), "stroke", 2.5))

    def linha(i, rot, t0):
        k = prog(t, t0 - 0.05, t0 + 0.25)
        if k <= 0:
            return 0.0, 0.0
        y = 475 + i * 104
        texto(cv, rot, 240 - 30 * (1 - e_out(k)), y + 15, F_BLACK, 40, "#FFFFFF", int(255 * a_g * k), centro=False)
        return a_g * k, y
    a, y = linha(0, "FEBRE", T["febre2"])
    if a > 0:
        termometro(cv, 160, y + 4, e_out(prog(t, T["febre2"], T["febre2"] + 0.9)) * 0.9, a, 0.85)
    a, y = linha(1, "PUS", T["pus"])
    if a > 0:
        gota(cv, 160, y + 6, 22 * e_back(prog(t, T["pus"], T["pus"] + 0.4)), COR_PUS, a)
    a, y = linha(2, "FERIDA QUE ABRIU", T["ferida"])
    if a > 0:                                   # corte com pontos; as bordas se afastam em "abriu"
        icone_ferida(cv, y, e_out(prog(t, T["abriu"], T["abriu"] + 0.5)), a)
    a, y = linha(3, "VERMELHIDÃO SE ALASTRANDO", T["verm2"])
    if a > 0:                                   # mancha rosada difusa que cresce em "alastrando"
        icone_vermelhidao(cv, y, e_out(prog(t, T["alastrando"] - 0.1, T["alastrando"] + 1.0)), a)
    # botão do pronto-socorro
    k = prog(t, T["pronto"] - 0.05, T["pronto"] + 0.3)
    if k > 0:
        a = a_g * k
        pulso = 1 + 0.035 * math.sin((t - T["hora"]) * 8) if t >= T["hora"] else 1.0
        pop = lerp(0.85, 1.0, e_back(k))
        cv.save(); cv.translate(540, 925); cv.scale(pulso * pop, pulso * pop)
        bt = skia.RRect.MakeRectXY(skia.Rect(-430, -58, 430, 58), 26, 26)
        if t >= T["hora"]:
            cv.drawRRect(bt, paint("#FF4A50", int(120 * a * (0.6 + 0.4 * math.sin((t - T["hora"]) * 8))), blur=18))
        cv.drawRRect(bt, paint("#1A0C10", int(255 * a)))
        cv.drawRRect(bt, paint(VERMELHO, int(255 * a), "stroke", 5))
        cruz(cv, -372, 0, 80, a)
        texto(cv, "PRONTO-SOCORRO NA HORA", -312, 15, F_BLACK, 42, "#FFFFFF", int(255 * a), centro=False)
        cv.restore()
    # telefone: avise a equipe
    k = prog(t, T["avisando"] - 0.05, T["avisando"] + 0.3)
    if k > 0:
        a = a_g * k
        toque = prog(t, T["equipe"], T["equipe"] + 0.15)
        telefone(cv, 350, 1080, a, toque, t)
        texto(cv, "AVISE A EQUIPE", 440, 1095, F_BLACK, 40, OURO, int(255 * a), centro=False)
    cv.restore()


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    cam = camera(t, T)

    # portas e vaso (tela), atrás do osso
    a_tit = prog(t, T["entrar"], T["entrar"] + 0.3) * (1 - prog(t, T["destruindo"] - 0.4, T["destruindo"]))
    vaso(cv, t, T, cam)
    for i in range(3):
        porta(cv, i, t, T)

    # mundo (câmera)
    bx, s, fy = cam
    cv.save(); cv.translate(bx, SY); cv.scale(s, s); cv.translate(-CX, -fy)
    halo(cv, t, T)
    osso(cv, t, T)
    vao_e_reconstrucao(cv, t, T)
    cortes(cv, t, T)
    anel_capa(cv, t, T)
    sinais_no_osso(cv, t, T)
    cv.restore()

    pontinhos(cv, t, T, cam)

    # rótulos e painéis (tela)
    if a_tit > 0:
        texto(cv, "PORTAS DE ENTRADA", CX, 300, F_BLACK, 42, OURO, int(255 * a_tit), contorno=8)
    for i, (_, _, dobra, t_nome, _, nome) in enumerate(PORTAS):
        a = prog(t, T[t_nome] - 0.05, T[t_nome] + 0.2) * _alpha_portas(t, T)
        x, y = PORTAS[i][0] + _porta_dx(t, T, i), PORTAS[i][1]
        if i == 0:
            pilula(cv, nome, 0, y - 22, OURO, a, esq=x - 60)
        else:
            pilula(cv, nome, x + PW / 2, y - 22, OURO, a)
    etiqueta_osteo(cv, t, T, cam)
    a = prog(t, T["dentro"], T["dentro"] + 0.2) * (1 - prog(t, T["dor"] - 0.3, T["dor"] - 0.05))  # sai antes da lista
    if a > 0:
        xa, ya = tela(cam, CX + 20, YM + 5)
        rotulo(cv, "POR DENTRO", 650, ya - 150, xa, ya, "#D9C7A8", a)
    checklist_sinais(cv, t, T)
    # NÃO IGNORE no espaço livre ABAIXO da lista (a lista termina em y≈953): não cobre nenhum sinal
    carimbo_opaco(cv, "NÃO IGNORE", 740, 1045, -6, T["ignore"], t, dur=T["tratamento"] - T["ignore"] + 0.2,
                  esc0=1.35)
    etapas(cv, t, T)
    rotulos_tratamento(cv, t, T, cam)
    # ressalva CFM da reconstrução: opaca (legível sobre o osso claro) e batendo NA palavra
    carimbo_opaco(cv, "SEMPRE INDIVIDUALIZADO", 490, 1110, -5, T["reconstruir"], t,
                  dur=T["operou"] - T["reconstruir"] + 0.3, tam=50, esc0=1.25)

    alerta(cv, t, T)

    capa(cv, t, T["osteo"], ep["gancho"][0], ep["gancho"][1])
    selo_como_funciona(cv, prog(t, T["osteo"] + 0.3, T["osteo"] + 0.7) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface(cv, t, T, blocos, DESTAQUE)


# ------------------------------------------------------------------ som e prévias
def sons(T):
    ev = [(T["osteo"] + 0.05, "ping", 0.55), (T["entrar"], "whoosh", 0.55),
          (T["exposta"], "whoosh", 0.3), (T["exposta"] + 0.35, "pop", 0.55),
          (T["cirurgia"], "whoosh", 0.3), (T["cirurgia"] + 0.35, "pop", 0.55),
          (T["sangue"], "whoosh", 0.35), (T["sangue"] + 0.35, "pop", 0.55),
          (T["destruindo"] - 0.5, "whoosh", 0.3), (T["dentro"], "ping", 0.4)]
    ev += [(T[k], "tick", 0.75) for k in ("dor", "inchaco", "calor", "verm1", "febre1", "secrecao")]
    ev += [(T["ignore"] - 0.02, "thump", 0.85), (T["tratamento"], "whoosh", 0.45),
           (T["combater"], "ping", 0.6), (T["combater"] + 0.1, "shimmer", 0.2),
           (T["remover"], "ping", 0.45), (T["remover"] + 0.2, "tick", 0.9), (T["remover"] + 0.35, "tick", 0.9),
           (T["doente"] - 0.15, "whoosh", 0.5), (T["vao"], "ping", 0.45),
           # reconstruir: sem "brilho mágico" (o vão mal começa a encher) — ping discreto + a batida do carimbo
           (T["reconstruir"], "ping", 0.4), (T["reconstruir"], "thump", 0.7),
           (T["operou"] + 0.05, "whoosh", 0.55), (T["febre2"], "pop", 0.6), (T["pus"], "pop", 0.6),
           (T["ferida"], "pop", 0.6), (T["verm2"], "pop", 0.6), (T["pronto"], "thump", 0.6),
           (T["hora"], "ding", 0.6), (T["equipe"], "ping", 0.5), (T["equipe"] + 0.22, "ping", 0.45),
           (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def tempos_previa(T):
    return (0.4, T["osteo"] + 0.7, T["sangue"] + 0.8, T["dentro"] + 0.4, T["secrecao"] + 0.5,
            T["ignore"] + 0.3, T["combater"] + 0.8, T["doente"] + 0.4, T["reconstruir"] + 0.6,
            T["alastrando"] + 0.6, T["equipe"] + 0.8, T["manda"] + 1.6)


render = fazer_render(quadro, ANCORAS, sons, tempos_previa)
