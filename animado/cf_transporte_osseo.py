# -*- coding: utf-8 -*-
"""COMO FUNCIONA — transporte ósseo ("FALTAVAM 17 CM / DE OSSO. E AGORA?"). Caso real da
literatura (Pentela et al., J Orthop Case Rep 2023), tratado por OUTRA equipe; ilustração
esquemática, nunca imagem do paciente.

Mesmo estilo e mesmas peças das duas cenas aprovadas (osso marfim, osso novo dourado, anel/fio/
haste do fixador, rótulos, carimbos, brilhos, calendário, legenda karaokê, CTA com aviãozinho).
O que a cena mostra, cada coisa disparada pela palavra falada:
  * capa (t=0): a tíbia interrompida no terço médio; o trecho que falta é só um contorno
    tracejado, vazio (sem ferida, sem sangue, sem acidente desenhado, sem exame simulado);
  * "dezessete": cota vertical ao lado do vão + "17 cm"; "canela": rótulo da tíbia;
  * "fixador": 4 anéis encaixam um a um nas posições do quadro B aprovado (1º acima do corte,
    2º logo abaixo dele — no pedaço que vai viajar —, 3º e 4º no pedaço de baixo); a câmera mostra
    a tíbia inteira com o fixador (sem silhueta de perna) e desliza para liberar a coluna de rótulos;
  * "médicos"/"cortaram": linha vermelha pisca entre o 1º e o 2º anel, clarão, fenda fina;
    "propósito": carimbo vermelho do piloto;
  * "deslizando": o pedaço (preso ao 2º anel pelos fios) desce em passinhos, um clique por passo,
    sem contador; trilha pontilhada e setinha à frente; "devagarinho" se escreve letra por letra
    na legenda; "Atrás dele": o osso novo nasce fraco atrás do pedaço; "rastro"/"novo": ganha corpo
    dourado e brilha;
  * "quatro": calendário + 4 MESES / aos poucos; o tracejado e a cota se apagam;
  * "transporte": carimbo dourado; "alongamento": miniatura do gesto do cf_alongamento;
  * "objetivo": o pedaço encosta; tíbia contínua com o trecho novo marcado entre dois tracinhos
    (o fixador fica: o roteiro não fala em tirar); "osso" (4ª vez)/"comprimento"/"função": chips SEM
    check + chip honesto do desfecho (encurtamento E rigidez no tornozelo; cada caso é único).
Todo texto desenhado está em ep["tela"] (o render recusa o vídeo se não estiver).
"""
import math

import skia

from .cf_comum import capa, carimbo as carimbo_ouro, fazer_render, interface, selo_como_funciona
from .cf_alongamento import (ACO, ACO_ESC, ACO_HL, CX, F_BLACK, F_SEMI, HASTE, NOVO, NOVO_G, OSSO_C,
                             OSSO_L, OURO, VERMELHO, brilhos, carimbo as carimbo_vermelho, clamp,
                             desenha_regenerado, e_back, e_inout, e_out, fundo, haste, larg_texto, lerp,
                             paint, path_osso_inf, path_osso_sup, porca, prog, sombra_osso, texto)
from .cf_fratura_cola import calendario

ANCORAS = {
    "perdeu": ("perdeu", 1, False), "dezessete": ("dezessete", 1, False), "canela": ("canela", 1, False),
    "fixador": ("fixador", 1, False), "medicos": ("médicos", 1, False), "cortaram": ("cortaram", 1, False),
    "proposito": ("propósito", 1, False), "deslizando": ("deslizando", 1, False),
    "devagarinho": ("devagarinho", 1, False), "atras": ("atrás", 1, False), "rastro": ("rastro", 1, False),
    "novo": ("novo", 1, False), "quatro": ("quatro", 1, False), "transporte": ("transporte", 1, False),
    "alongamento": ("alongamento", 1, False), "objetivo": ("objetivo", 1, False),
    "osso4": ("osso", 4, False), "comprimento": ("comprimento", 1, False), "funcao": ("função", 1, False),
    "manda": ("manda", 1, False),
}
DESTAQUE = {"dezessete", "centímetros", "canela", "fixador", "ilizarov", "cortaram", "propósito", "deslizando",
            "devagarinho", "rastro", "novo", "quatro", "meses", "transporte", "ósseo", "alongamento",
            "comprimento", "função"}

# ------------------------------------------------------------------ textos de tela (todos em ep["tela"])
FAIXA = ("Caso real da literatura", "tratado por outra equipe")
ESQUEMA = "ilustração esquemática"
NOTA = "Caso publicado, tratado por outra equipe"
HONESTO = ("neste caso: ficou 1,5 cm", "de encurtamento e rigidez", "no tornozelo")
UNICO = "cada caso é único"

# ------------------------------------------------------------------ geometria (mundo, antes da câmera)
Y_TOPO, Y_CORTE, Y_G0, Y_G1, Y_BASE = 300, 550, 660, 1020, 1290
VAO = Y_G1 - Y_G0                       # a falha (esquemática: ~1/3 da tíbia desenhada)
FENDA = 8                               # a fenda fina do corte
CURSO = VAO - FENDA                     # quanto o pedaço anda até encostar no osso de baixo
H2 = HASTE / 2
RX2, RY2 = 175, 38                      # anel um pouco menor que o do piloto: sobra coluna para os rótulos
X_HASTE = 150
Y_ANEIS = (405, 605, 1110, 1240)        # 1º acima do corte; 2º no pedaço que viaja; 3º e 4º embaixo
N_PASSOS = 30                           # passinhos do transporte (um clique cada; NÃO vai para a tela)
FOCO = 803                              # centro do osso no mundo (platô 280 ... maléolo 1326)
X_COL = 580                             # coluna da direita (rótulos e chips), fora dos anéis
AZUL = "#9CC9FF"
AMBAR = "#7A5420"                       # base do osso novo enquanto ainda é fraco


# ------------------------------------------------------------------ tempo e câmera
def janela_transporte(T):
    return T["deslizando"] + 0.15, T["objetivo"] + 0.2      # último passinho encosta na palavra "objetivo"


def deslocamento(t, T):
    """Quanto o pedaço já desceu: passinhos curtos (anda e para), sem número na tela."""
    t0, t1 = janela_transporte(T)
    k = prog(t, t0, t1) * N_PASSOS
    i = math.floor(k)
    if i >= N_PASSOS:
        return CURSO
    return CURSO * (i + e_inout(clamp((k - i) / 0.45))) / N_PASSOS


def camera(t, T):
    """-> (x na tela do eixo do osso, y na tela do centro do osso, escala). Capa: tíbia inteira,
    centrada, abaixo do gancho (topo >= ~350) e acima da legenda (<= 1230). No "fixador" (o gancho já
    saiu) ela sobe, cresce um pouco e desliza para a esquerda, liberando a coluna da direita."""
    a = e_inout(prog(t, T["fixador"] - 0.1, T["fixador"] + 1.0))
    tremor = 0.0
    for t0, forca in ((T["cortaram"] + 0.1, 9), (T["proposito"], 6), (T["transporte"], 5)):
        k = t - t0
        if 0 <= k < 0.35:
            tremor += forca * math.sin(k * 70) * (1 - k / 0.35)
    return lerp(540, 400, a) + tremor, lerp(791, 765, a), lerp(0.84, 0.87, a)


def na_tela(cam, x, y):
    px, yc, s = cam
    return px + (x - CX) * s, yc + (y - FOCO) * s


# ------------------------------------------------------------------ fixador (anel menor que o do piloto)
def anel(cv, y, dx, alfa, metade):
    if alfa <= 0:
        return
    r = skia.Rect(CX + dx - RX2, y - RY2, CX + dx + RX2, y + RY2)
    if metade == "tras":
        cv.drawArc(r, 180, 180, False, paint(ACO_ESC, int(255 * alfa), "stroke", 14))
        return
    cv.drawArc(r, 0, 180, False, paint("#000000", int(80 * alfa), "stroke", 17, blur=6))
    cv.drawArc(r, 0, 180, False, paint(ACO, int(255 * alfa), "stroke", 14))
    cv.drawArc(skia.Rect(r.left() + 6, r.top() + 4, r.right() - 6, r.bottom() - 2), 20, 140, False,
               paint(ACO_HL, int(170 * alfa), "stroke", 3))
    for ang in (25, 90, 155):
        a = math.radians(ang)
        cv.drawCircle(CX + dx + RX2 * math.cos(a), y + RY2 * math.sin(a), 3.2, paint(ACO_ESC, int(255 * alfa)))


def fios(cv, y, pr, alfa):
    if pr <= 0 or alfa <= 0:
        return
    for s in (-1, 1):
        x0, y0, x1, y1 = CX - RX2 + 16, y - 12 * s, CX + RX2 - 16, y + 12 * s
        cv.drawLine(x0, y0, lerp(x0, x1, pr), lerp(y0, y1, pr), paint("#DDE6EE", int(230 * alfa), "stroke", 3.2))
        if pr > 0.98:                                              # oliva, em cima do fio
            xo = CX - 62 * s
            cv.drawCircle(xo, lerp(y0, y1, (xo - x0) / (x1 - x0)), 6, paint(OURO, int(255 * alfa)))


# ------------------------------------------------------------------ osso
def peca(cv, pth):
    cv.drawPath(pth, paint("#000000", 70, blur=14))
    cv.drawPath(pth, paint(OSSO_C, shader=sombra_osso()))
    cv.drawPath(pth, paint(OSSO_L, 150, "stroke", 2.5))


def tracejado(cv, x0, y0, x1, y1, cor, alfa, larg=4, traco=22, vazio=14, fase=0.0):
    if alfa <= 0:
        return
    p = paint(cor, int(alfa), "stroke", larg)
    p.setPathEffect(skia.DashPathEffect.Make([traco, vazio], fase))
    cv.drawLine(x0, y0, x1, y1, p)


# ------------------------------------------------------------------ peças de tela (fora da câmera)
def etiqueta(cv, linhas, x, y, ancora, cor, a):
    """Caixa de rótulo (1 ou 2 linhas) com canto sup. esq. em (x, y) e linha fina até `ancora`.
    linhas = [(texto, fonte, tamanho, cor)]."""
    if a <= 0:
        return
    x += 26 * (1 - e_out(a))
    larg = max(larg_texto(s, f, tam) for s, f, tam, _ in linhas)
    alt = sum(tam * 1.22 for _, _, tam, _ in linhas) + 20
    xa, ya = ancora
    cv.drawLine(xa, ya, x, y + alt / 2, paint(cor, int(200 * a), "stroke", 2.5))
    cv.drawCircle(xa, ya, 6, paint(cor, int(255 * a)))
    rr = skia.RRect.MakeRectXY(skia.Rect(x, y, x + larg + 32, y + alt), 14, 14)
    cv.drawRRect(rr, paint("#0B1824", int(215 * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 2.5))
    yy = y + 10
    for s, f, tam, c in linhas:
        yy += tam * 1.22
        texto(cv, s, x + 16, yy - tam * 0.3, f, tam, c, int(255 * a), centro=False)


def cota(cv, x, y0, y1, pr, a, t_pop, t):
    """Cota vertical com pontinhas nas duas extremidades; '17 cm' acende em ouro à direita dela."""
    if a <= 0 or pr <= 0:
        return
    ym = (y0 + y1) / 2; meia = (y1 - y0) / 2 * pr
    cv.drawLine(x, ym - meia, x, ym + meia, paint("#DDE6EE", int(230 * a), "stroke", 3))
    for yy in (ym - meia, ym + meia):
        cv.drawLine(x - 14, yy, x + 14, yy, paint("#DDE6EE", int(230 * a), "stroke", 3))
        cv.drawCircle(x, yy, 5, paint("#DDE6EE", int(255 * a)))
    k = t - t_pop
    if k >= 0:
        esc = lerp(1.6, 1.0, e_out(clamp(k / 0.22)))
        lw = larg_texto("17 cm", F_BLACK, 62)
        cv.save(); cv.translate(x + 26 + lw / 2, ym + 21); cv.scale(esc, esc)
        cv.drawRect(skia.Rect(-lw / 2 - 20, -62, lw / 2 + 20, 20), paint(OURO, int(70 * a * (1 - clamp(k / 0.6))), blur=18))
        texto(cv, "17 cm", 0, 0, F_BLACK, 62, OURO, int(255 * a * clamp(k / 0.1)), contorno=8)
        cv.restore()


def faixa_caso(cv, a):
    """Atribuição do caso, logo acima da identificação CFM (sem tocar nas duas linhas dela)."""
    if a <= 0:
        return
    w1, w2 = (larg_texto(s, F_SEMI, 30) for s in FAIXA)
    x0 = CX - (w1 + 34 + w2) / 2; y = 1543
    texto(cv, FAIXA[0], x0, y, F_SEMI, 30, AZUL, int(235 * a), centro=False, contorno=5)
    cv.drawCircle(x0 + w1 + 17, y - 10, 4, paint(AZUL, int(235 * a)))
    texto(cv, FAIXA[1], x0 + w1 + 34, y, F_SEMI, 30, AZUL, int(235 * a), centro=False, contorno=5)


def miniatura(cv, t, t0, a):
    """O gesto do cf_alongamento em miniatura: dois blocos de osso se afastam e o dourado preenche."""
    if a <= 0:
        return
    s = "mesmo princípio do alongamento ósseo"
    lw = larg_texto(s, F_SEMI, 31)
    total = 200 + 22 + lw + 48
    x0 = CX - total / 2; y0, y1 = 216, 300
    cv.save(); cv.translate(0, 10 * (1 - e_out(a)))             # entra de baixo: nunca invade o selo
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x0 + total, y1), 22, 22)
    cv.drawRRect(rr, paint("#0B1824", int(220 * a))); cv.drawRRect(rr, paint(OURO, int(170 * a), "stroke", 2.5))
    xm, ym = x0 + 24 + 100, (y0 + y1) / 2
    sep = lerp(6, 56, e_inout(prog(t, t0 + 0.25, t0 + 1.3)))
    if sep > 8:                                                   # osso novo no meio, com estrias
        cv.drawRect(skia.Rect(xm - sep / 2, ym - 15, xm + sep / 2, ym + 15), paint(NOVO, int(235 * a)))
        n = max(2, int(sep / 9))
        for k in range(n):
            xx = xm - sep / 2 + 4 + k * (sep - 8) / max(1, n - 1)
            cv.drawLine(xx, ym - 13, xx, ym + 13, paint("#B5701A", int(150 * a), "stroke", 2))
        cv.drawRect(skia.Rect(xm - sep / 2 - 10, ym - 26, xm + sep / 2 + 10, ym + 26), paint(NOVO_G, int(60 * a), blur=10))
    for lado in (-1, 1):
        xa = xm + lado * sep / 2; xb = xa + lado * 70
        r = skia.Rect(min(xa, xb), ym - 17, max(xa, xb), ym + 17)
        cv.drawRRect(skia.RRect.MakeRectXY(r, 8, 8), paint(OSSO_C, int(255 * a)))
        cv.drawRRect(skia.RRect.MakeRectXY(r, 8, 8), paint(OSSO_L, int(160 * a), "stroke", 2))
    texto(cv, s, x0 + 24 + 200 + 22, ym + 11, F_SEMI, 31, "#FFFFFF", int(255 * a), centro=False)
    cv.restore()


def chip(cv, s, x, y, w, t0, t):
    k = t - t0
    if k < 0:
        return
    a = clamp(k / 0.15); esc = lerp(0.6, 1.0, e_back(clamp(k / 0.35)))
    acende = 1 - clamp(k / 0.9)
    cv.save(); cv.translate(x + w / 2, y + 32); cv.scale(esc, esc)
    r = skia.Rect(-w / 2, -32, w / 2, 32)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-w / 2 - 8, -40, w / 2 + 8, 40), 24, 24),
                 paint(NOVO_G, int(a * (50 + 140 * acende)), blur=16))
    cv.drawRRect(skia.RRect.MakeRectXY(r, 18, 18), paint("#0B1824", int(225 * a)))
    cv.drawRRect(skia.RRect.MakeRectXY(r, 18, 18), paint(OURO, int(255 * a), "stroke", 3.5))
    texto(cv, s, 0, 14, F_BLACK, 40, "#FFFFFF", int(255 * a))
    cv.restore()


def chip_honesto(cv, x, y, t0, t):
    k = t - t0
    if k < 0:
        return
    a = e_out(clamp(k / 0.35))
    linhas = [(s, "#FFFFFF") for s in HONESTO] + [(UNICO, AZUL)]
    tam, passo = 32, 44                                           # 32 px: lido no celular em ~3 s
    lw = max(larg_texto(s, F_SEMI, tam) for s, _ in linhas)
    cv.save(); cv.translate(22 * (1 - a), 0)
    rr = skia.RRect.MakeRectXY(skia.Rect(x, y, x + lw + 36, y + 30 + passo * len(linhas)), 16, 16)
    cv.drawRRect(rr, paint("#0B1824", int(225 * a))); cv.drawRRect(rr, paint(AZUL, int(200 * a), "stroke", 2.5))
    for i, (s, c) in enumerate(linhas):
        texto(cv, s, x + 18, y + passo * (i + 1) + (6 if i == len(linhas) - 1 else 0), F_SEMI, tam, c,
              int(255 * a), centro=False)
    cv.restore()


class _Devagarinho:
    """Canvas-envelope para a interface: na legenda, DEVAGARINHO se escreve letra por letra, bem
    devagar (a piada tipográfica do 'devagar' do piloto). O texto registrado é a palavra inteira do
    roteiro; só o desenho sai aos poucos (mesmo mecanismo do `track` de `texto`)."""
    def __init__(self, cv, t, t0, dur):
        self._cv, self._t, self._t0, self._dur = cv, t, t0, dur

    def drawString(self, s, x, y, f, p):
        if s.rstrip(",.").upper() != "DEVAGARINHO":
            return self._cv.drawString(s, x, y, f, p)
        getattr(self._cv, "registra", lambda _s: None)(s)
        real = getattr(self._cv, "real", self._cv)
        vis = len(s) * clamp((self._t - self._t0) / self._dur)
        a0 = p.getAlpha(); cx = x
        for i, ch in enumerate(s):
            k = vis - i
            if k <= 0:
                break
            w = f.measureText(ch); pop = clamp(k)
            p.setAlpha(int(a0 * pop))
            real.save(); real.translate(cx + w / 2, y); esc = lerp(1.6, 1.0, e_out(pop)); real.scale(esc, esc)
            real.drawString(ch, -w / 2, 0, f, p)
            real.restore()
            cx += w
        p.setAlpha(a0)

    def __getattr__(self, nome):
        return getattr(self._cv, nome)


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    cam = camera(t, T)
    px, yc, s = cam
    t_cta = T["manda"] - 0.15

    fenda = FENDA * e_out(prog(t, T["cortaram"] + 0.05, T["cortaram"] + 0.25))
    d = deslocamento(t, T)
    seg0, seg1 = Y_CORTE + fenda + d, Y_G0 + fenda + d          # o pedaço que viaja
    encostou = prog(t, T["objetivo"] - 0.1, T["objetivo"] + 0.2)
    y_an = [Y_ANEIS[0], Y_ANEIS[1] + fenda + d, Y_ANEIS[2], Y_ANEIS[3]]
    p_an = [e_back(prog(t, T["fixador"] + 0.12 * i, T["fixador"] + 0.12 * i + 0.5)) for i in range(4)]
    dx = [(-900 if i % 2 == 0 else 900) * (1 - p_an[i]) for i in range(4)]
    vis = [clamp(p_an[i] * 3) for i in range(4)]

    # ================= mundo (câmera)
    cv.save(); cv.translate(px, yc); cv.scale(s, s); cv.translate(-CX, -FOCO)
    for i in range(4):
        anel(cv, y_an[i], dx[i], vis[i], "tras")

    if t < T["cortaram"] + 0.1:                                  # antes do corte: um osso só, sem emenda
        peca(cv, path_osso_sup(Y_TOPO, Y_G0))
    else:
        peca(cv, path_osso_sup(Y_TOPO, Y_CORTE))
        seg = skia.Path(); seg.addRRect(skia.RRect.MakeRectXY(skia.Rect(CX - H2, seg0, CX + H2, seg1), 4, 4))
        peca(cv, seg)
    peca(cv, path_osso_inf(Y_G1, Y_BASE))

    # osso novo no rastro do pedaço: nasce fraco no "Atrás dele" (o vão atrás do pedaço não fica vazio
    # tempo demais) e ganha corpo no "rastro"; cresce do corte até o pedaço e o acompanha
    nasce = e_out(prog(t, T["atras"] - 0.05, T["atras"] + 0.4))
    if nasce > 0 and seg0 - Y_CORTE > 12:
        dens = 0.35 + 0.65 * e_inout(prog(t, T["rastro"] - 0.05, T["rastro"] + 0.45))
        brilho = prog(t, T["novo"] - 0.1, T["novo"] + 0.3) * (1 - 0.6 * prog(t, T["novo"] + 1.4, T["novo"] + 2.4))
        duro = 0.42 * e_inout(prog(t, T["objetivo"] + 0.2, T["objetivo"] + 1.4))   # dourado mais claro no fim
        y0 = Y_CORTE + fenda * 0.5; y1 = lerp(y0, seg0 - fenda * 0.5, nasce)
        # base âmbar opaca: o osso novo ainda fraco fica caramelo (nem oliva sobre o azul, nem translúcido)
        cv.drawRect(skia.Rect(CX - H2 + 2, y0, CX + H2 - 2, y1), paint(AMBAR))
        desenha_regenerado(cv, y0, y1, dens, max(brilho, 0.3 * dens), duro, t)

    # o vão: contorno tracejado claro e vazio (encolhe com a viagem; apaga a partir do "quatro")
    resto = Y_G1 - seg1
    pulso = max(0.0, 1 - abs(t - (T["perdeu"] + 0.25)) / 0.45)
    a_vao = (170 + 85 * pulso) * (1 - 0.7 * prog(t, T["quatro"], T["quatro"] + 1.2)) * (1 - encostou)
    if resto > 10:
        for xx in (CX - H2, CX + H2):
            tracejado(cv, xx, seg1 + 8, xx, Y_G1 - 8, "#DDE6EE", a_vao, larg=4, fase=-t * 10)
    # trilha pontilhada e setinha à frente do pedaço
    a_tr = prog(t, T["deslizando"] - 0.05, T["deslizando"] + 0.35) * (1 - encostou)
    if a_tr > 0 and resto > 70:
        passo = 26; y = seg1 + 18 + (t * 40) % passo
        while y < Y_G1 - 52:
            cv.drawCircle(CX, y, 5, paint(OURO, int(220 * a_tr))); y += passo
        sp = skia.Path(); sp.moveTo(CX - 18, Y_G1 - 46); sp.lineTo(CX, Y_G1 - 24); sp.lineTo(CX + 18, Y_G1 - 46)
        cv.drawPath(sp, paint(OURO, int(255 * a_tr), "stroke", 6))
    # borda dourada do pedaço que viaja
    a_borda = prog(t, T["deslizando"] - 0.1, T["deslizando"] + 0.3) * (1 - prog(t, T["objetivo"] + 0.4, T["objetivo"] + 1.2))
    if a_borda > 0:
        r = skia.RRect.MakeRectXY(skia.Rect(CX - H2 - 3, seg0 - 3, CX + H2 + 3, seg1 + 3), 6, 6)
        cv.drawRRect(r, paint(NOVO_G, int(120 * a_borda), "stroke", 14, blur=8))
        cv.drawRRect(r, paint(OURO, int(255 * a_borda), "stroke", 5))
    # tracinhos que marcam o trecho novo (honestidade visual do quadro aprovado)
    a_tick = prog(t, T["objetivo"] + 0.3, T["objetivo"] + 0.8)
    if a_tick > 0:
        for yy in (Y_CORTE + fenda * 0.5, seg0 - fenda * 0.5):
            for lado in (-1, 1):
                x0 = CX + lado * (H2 + 8); x1 = CX + lado * (H2 + 36)
                cv.drawLine(x0, yy, x1, yy, paint("#FFFFFF", int(235 * a_tick), "stroke", 4))

    # o corte: tracejado vermelho piscando entre o 1º e o 2º anel, clarão e fenda
    if T["medicos"] - 0.55 <= t < T["cortaram"] + 0.1:
        pisca = 0.5 + 0.5 * math.sin(t * 10)
        a = prog(t, T["medicos"] - 0.55, T["medicos"] - 0.25)
        tracejado(cv, CX - 96, Y_CORTE + 3, CX + 96, Y_CORTE + 3, VERMELHO, a * (120 + 135 * pisca), larg=6,
                  traco=16, vazio=12)
    k = t - (T["cortaram"] + 0.1)
    if 0 <= k < 1.0:
        a = 1 - k
        cv.drawLine(CX - 150, Y_CORTE + 4, CX + 150, Y_CORTE + 4, paint(VERMELHO, int(220 * a), "stroke", 16, blur=10))
        cv.drawLine(CX - 120 * e_out(clamp(k / 0.12)), Y_CORTE + 4, CX + 120 * e_out(clamp(k / 0.12)), Y_CORTE + 4,
                    paint("#FFFFFF", int(255 * a), "stroke", 4))
        cv.drawCircle(CX, Y_CORTE + 4, 120 * e_out(clamp(k / 0.25)), paint("#FFFFFF", int(140 * (1 - clamp(k / 0.3))), blur=30))

    brilhos(cv, CX, (Y_CORTE + seg0) / 2, t, T["novo"] + 0.05, n=16, raio=200)
    brilhos(cv, CX, Y_G1, t, T["objetivo"] + 0.05, n=12, raio=170)

    # fixador (frente): fios, hastes (o 2º anel corre nelas, porcas girando), anéis
    for i in range(4):
        fios(cv, y_an[i], prog(t, T["fixador"] + 0.45 + 0.06 * i, T["fixador"] + 0.75 + 0.06 * i), vis[i])
    a_h = prog(t, T["fixador"] + 0.4, T["fixador"] + 0.8)
    for sx in (-1, 1):
        x = CX + sx * X_HASTE
        haste(cv, x, y_an[0], y_an[1], a_h)
        haste(cv, x, y_an[1], y_an[2], a_h, rosca=True, fase=-d * 0.6)
        haste(cv, x, y_an[2], y_an[3], a_h)
        porca(cv, x, y_an[1] - 20, d * 3 + sx * 15, a_h)
        porca(cv, x, y_an[1] + 20, -d * 3, a_h)
    for i in range(4):
        anel(cv, y_an[i], dx[i], vis[i], "frente")
    cv.restore()

    # ================= tela (rótulos, carimbos, interface)
    a_cota = prog(t, T["dezessete"] - 0.05, T["dezessete"] + 0.15) * (1 - prog(t, T["quatro"], T["quatro"] + 0.8))
    xc, yg0 = na_tela(cam, CX + RX2 + 42, Y_G0); _, yg1 = na_tela(cam, CX, Y_G1)
    cota(cv, xc, yg0, yg1, e_out(prog(t, T["dezessete"] - 0.05, T["dezessete"] + 0.35)), a_cota, T["dezessete"] + 0.2, t)

    a = prog(t, T["canela"] + 0.1, T["canela"] + 0.4) * (1 - prog(t, T["fixador"] - 0.2, T["fixador"] + 0.1))
    etiqueta(cv, [("osso da canela (tíbia)", F_BLACK, 34, "#FFFFFF")], 616, 548,
             na_tela(cam, CX + H2 - 4, 530), OSSO_C, a)
    a = prog(t, T["fixador"] + 0.7, T["fixador"] + 1.0) * (1 - prog(t, T["cortaram"] - 0.1, T["cortaram"] + 0.2))
    etiqueta(cv, [("fixador de Ilizarov", F_BLACK, 34, "#FFFFFF")], X_COL, 344,
             na_tela(cam, CX + RX2 * 0.8, Y_ANEIS[0] + RY2 * 0.6), ACO_HL, a)
    a = prog(t, T["cortaram"] + 0.15, T["cortaram"] + 0.45) * (1 - prog(t, T["rastro"] - 0.4, T["rastro"] - 0.1))
    etiqueta(cv, [("corte no osso saudável", F_BLACK, 34, "#FFFFFF")], X_COL, 496,
             na_tela(cam, CX + H2, Y_CORTE + 4), VERMELHO, a)
    a = prog(t, T["rastro"] + 0.1, T["rastro"] + 0.4) * (1 - prog(t, T["transporte"] - 0.3, T["transporte"]))
    # (no lugar que o "corte no osso saudável" acabou de liberar: acima da cota, sem tocá-la)
    etiqueta(cv, [("osso novo", F_BLACK, 36, OURO), ("atrás do segmento", F_SEMI, 32, "#FFFFFF")], X_COL, 462,
             na_tela(cam, CX + H2 - 10, (Y_CORTE + seg0) / 2), OURO, a)

    # 4 MESES, aos poucos (rótulo fixo: o calendário vira folhas sem número) — abaixo da cota, que se apaga
    a = prog(t, T["quatro"] - 0.05, T["quatro"] + 0.3) * (1 - prog(t, T["objetivo"] + 0.1, T["objetivo"] + 0.5))
    if a > 0:
        dxm = 30 * (1 - e_out(a))
        calendario(cv, X_COL + dxm, 1000, t, T["quatro"], a)
        texto(cv, "4 MESES", X_COL + 118 + dxm, 1060, F_BLACK, 64, "#FFFFFF", int(255 * a), centro=False, contorno=8)
        texto(cv, "aos poucos", X_COL + 121 + dxm, 1108, F_SEMI, 36, AZUL, int(255 * a), centro=False)

    a = prog(t, T["alongamento"] - 0.05, T["alongamento"] + 0.3) * (1 - prog(t, T["funcao"] + 0.2, T["funcao"] + 0.6))
    miniatura(cv, t, T["alongamento"], a)

    carimbo_vermelho(cv, "DE PROPÓSITO", 480, 432, -8, T["proposito"] - 0.02, t)
    carimbo_ouro(cv, "UM PEDAÇO VIAJA", 540, 300, -4, T["deslizando"] + 0.3, t)   # topo: deixa a trilha à vista
    carimbo_ouro(cv, "TRANSPORTE ÓSSEO", 470, 640, -6, T["transporte"] - 0.02, t)

    wc = 400
    a_fim = 1 - prog(t, T["manda"] - 0.35, T["manda"] - 0.1)        # chips saem antes da CTA (não brigam com ela)
    if a_fim > 0:
        cv.saveLayerAlpha(None, int(255 * a_fim))
        chip(cv, "OSSO", X_COL, 420, wc, T["osso4"], t)
        chip(cv, "COMPRIMENTO", X_COL, 500, wc, T["comprimento"], t)
        chip(cv, "FUNÇÃO", X_COL, 580, wc, T["funcao"], t)
        chip_honesto(cv, X_COL, 672, T["funcao"] + 0.15, t)
        cv.restore()

    # atribuição + aviso de esquema (até a CTA)
    a_caso = 1 - prog(t, t_cta - 0.3, t_cta)
    faixa_caso(cv, a_caso)
    if a_caso > 0:
        lw = larg_texto(ESQUEMA, F_SEMI, 30)
        texto(cv, ESQUEMA, 1030 - lw, 1210, F_SEMI, 30, AZUL, int(215 * a_caso), centro=False, contorno=5)

    capa(cv, t, T["canela"], ep["gancho"][0], ep["gancho"][1])
    selo_como_funciona(cv, prog(t, T["fixador"], T["fixador"] + 0.4) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    dur_dev = clamp(T["atras"] - T["devagarinho"] - 0.45, 0.8, 1.7)
    interface(_Devagarinho(cv, t, T["devagarinho"], dur_dev), t, T, blocos, DESTAQUE, nota=NOTA)


# ------------------------------------------------------------------ som e prévias
def sons(T):
    ev = [(T["dezessete"] + 0.18, "thump", 0.85), (T["canela"] + 0.05, "whoosh", 0.35),
          (T["fixador"] - 0.05, "whoosh", 0.6)]
    ev += [(T["fixador"] + 0.12 * i + 0.38, "ping", 0.55) for i in range(4)]
    ev += [(T["cortaram"] + 0.08, "tick", 1.0), (T["proposito"] - 0.02, "thump", 0.9),
           (T["deslizando"] + 0.3, "thump", 0.55), (T["rastro"], "shimmer", 0.45), (T["novo"] - 0.05, "shimmer", 0.85),
           (T["quatro"], "whoosh", 0.35), (T["transporte"] - 0.02, "thump", 0.85), (T["alongamento"], "pop", 0.6),
           (T["objetivo"] - 0.05, "thump", 0.5), (T["objetivo"] + 0.12, "ding", 0.55),
           (T["osso4"], "pop", 0.75), (T["comprimento"], "pop", 0.75), (T["funcao"], "pop", 0.75),
           (T["funcao"] + 0.15, "whoosh", 0.25), (T["manda"] + 0.05, "whoosh", 0.5)]
    t0, t1 = janela_transporte(T)
    ev += [(lerp(t0, t1, i / N_PASSOS), "click", 0.55) for i in range(N_PASSOS)]   # um clique por passinho
    return ev


def tempos_previa(T):
    return [0.4, T["dezessete"] + 0.7, T["canela"] + 0.6, T["fixador"] + 1.3, T["proposito"] + 0.35,
            T["devagarinho"] + 0.9, T["rastro"] + 0.5, T["quatro"] + 0.6, T["transporte"] + 0.35,
            T["alongamento"] + 1.0, T["objetivo"] + 0.6, T["funcao"] + 2.0, T["manda"] + 1.6]


render = fazer_render(quadro, ANCORAS, sons, tempos_previa, respiro_cta=3.0)   # ~3 s de leitura do chip honesto
