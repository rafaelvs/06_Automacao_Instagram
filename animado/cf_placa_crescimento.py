# -*- coding: utf-8 -*-
"""COMO FUNCIONA — "Onde o osso da criança cresce?" (placa de crescimento / fise).

Mesmo estilo e mesmas peças das cenas aprovadas (osso marfim liso, osso novo dourado, carimbo do
piloto, brilhos, legenda karaokê, CTA com aviãozinho). Storyboard e correções do verificador
(lote3_cf/cf_placa_crescimento_storyboard.json) respeitados aqui:
  * O osso inteiro NUNCA ganha faixa desenhada: o acervo não diz onde fica a placa. A placa só
    aparece num balão de lupa SOLTO (marfim / faixa azul-clara / marfim), sem seta, sem linha de
    chamada e sem cabo apontando para um ponto do osso. O osso inteiro cresce por escala
    uniforme (não mostra em que ponto cresce).
  * "por ali … aumenta": camadas de osso novo dourado nascem junto à faixa, uma por palavra, de
    "ali" até "aumenta" (a 4ª cai em "aumenta" e tudo termina antes de "Só"); ao mesmo tempo o
    osso inteiro fica visivelmente mais comprido e uma régua SEM números acompanha.
  * "fratura": traço fino em zigue-zague na faixa (sem sangue, sem fragmento, sem deslocamento).
  * "acompanhamento": olho dourado piscando devagar — sem lista e sem contagem de consultas.
  * "alinhado": eixo tracejado, SEM check nem selo de resultado (é o objetivo, não promessa).
  * "curta": dois ossos (maléolos voltados para o meio, como um par visto de frente) crescem
    juntos, o de contorno vermelho para antes; cota SEM número.
  * "acompanhar": um marcador desliza numa linha do tempo, sem consultas contadas; a faixa do
    balão segue acesa (a cena não mostra a placa fechando).
  * "colar": o zigue-zague se FECHA no tom da própria cartilagem (costura fina azul-escura) com
    um brilho dourado só de passagem. Não vira traço de osso dourado DENTRO da faixa (isso
    leria como ponte óssea na placa, o mecanismo do encurtamento), não some, não vira calo,
    sem check.
  * Sem faixa de rótulos repetindo a legenda: o texto na tela só nomeia o que a legenda não
    desenha (a cartilagem, a placa, o osso formado, os carimbos, a bandeira do fim).
  * Nenhum exame simulado: nada de fundo preto, negativo, filme ou osso translúcido.
Cena PRESA ao roteiro pelas palavras-âncora (roteiro sem elas = KeyError, não vídeo torto).
Todo texto desenhado está em ep["tela"] (o render recusa o vídeo se não estiver).
"""
import math

import skia

from .cf_alongamento import (CX, F_BLACK, F_SEMI, NOVO, NOVO_G, OSSO_B, OSSO_C, OSSO_L, OURO, VERMELHO, C,
                             brilhos, carimbo as carimbo_vermelho, clamp, e_back, e_inout, e_out, fundo,
                             larg_texto, lerp, paint, prog, sombra_osso, texto)
from .cf_comum import capa, fazer_render, interface, selo_como_funciona

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "onde": ("onde", 1, False), "area": ("área", 1, False), "cartilagem": ("cartilagem", 1, False),
    "placa": ("placa", 1, False), "ali": ("ali", 1, False), "aumenta": ("aumenta", 1, False),
    "so": ("só", 1, False), "fragil": ("frágil", 1, False),
    "formado": ("formado", 1, False), "fratura": ("fratura", 1, False),
    "acompanhamento": ("acompanhamento", 1, False), "pro": ("pro", 1, False), "alinhado": ("alinhado", 1, False),
    "acidente": ("acidente", 1, False), "lesao": ("lesão", 1, False), "pode": ("pode", 1, False),
    "curta": ("curta", 1, False), "acompanhar": ("acompanhar", 1, False), "fim": ("fim", 1, False),
    "cresc2": ("crescimento", 2, False), "lado": ("lado", 1, False), "colar": ("colar", 1, False),
    "manda": ("manda", 1, False),
}
DESTAQUE = {"cresce", "cartilagem", "placa", "crescimento", "aumenta", "frágil", "fratura", "acompanhamento",
            "alinhado", "acidente", "lesão", "curta", "acompanhar", "fim", "bom", "colar", "rápido"}

# ------------------------------------------------------------------ textos de tela (todos em ep["tela"])
INTERROGA = "?"
AREA = "ÁREA DE CARTILAGEM"
PLACA, FISE = "PLACA DE CRESCIMENTO", "fise"
FRAGIL = "MAIS FRÁGIL"
FORMADO = "OSSO JÁ FORMADO"
FRATURA = "FRATURA"
ACIDENTE = "ACIDENTE GRAVE"
FIM = "FIM DO CRESCIMENTO"
BOM = "DO LADO BOM"

# ------------------------------------------------------------------ paleta própria
FUNDO_CARTAO = "#0B1824"
AZUL = "#9CC9FF"
CART, CART_HL, CART_ESC = "#8ECFEE", "#CDEEFB", "#4F93BA"      # cartilagem: azul-clara, lisa, opaca
ROSA = "#FF8A8F"
VERDE, VERDE_CL = "#2E9E62", "#8DE3B4"
TRINCA = "#2B2118"


def mistura(c0, c1, k):
    """Cor hex entre c0 e c1 (k de 0 a 1)."""
    k = clamp(k)
    a = [int(c0.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    b = [int(c1.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    return "#" + "".join(f"{round(lerp(x, y, k)):02X}" for x, y in zip(a, b))


def _p(cor, a=255, estilo="fill", w=0, blur=0, junta=False, traco=None):
    p = paint(cor, a, estilo, w, blur)
    if junta:
        p.setStrokeJoin(skia.Paint.kRound_Join)
    if traco:
        p.setPathEffect(skia.DashPathEffect.Make(list(traco), 0.0))
    return p


# ------------------------------------------------------------------ osso inteiro (um contorno só, sem faixa)
def _path_osso():
    """Mesmo desenho do osso do piloto (platô em cima, maléolo embaixo), num contorno ÚNICO:
    o osso inteiro não tem emenda nem faixa (não se sabe, pelo acervo, onde fica a placa)."""
    y0, yb, h = 300, 1150, 64
    p = skia.Path()
    p.moveTo(CX - 128, y0 + 40)
    p.cubicTo(CX - 135, y0 - 6, CX - 60, y0 - 18, CX - 10, y0 + 6)
    p.cubicTo(CX + 30, y0 - 20, CX + 132, y0 - 10, CX + 126, y0 + 42)
    p.cubicTo(CX + 120, y0 + 120, CX + h + 8, y0 + 150, CX + h, y0 + 230)
    p.lineTo(CX + h, yb - 190)
    p.cubicTo(CX + h + 4, yb - 110, CX + 84, yb - 70, CX + 80, yb - 22)
    p.cubicTo(CX + 76, yb + 2, CX + 30, yb - 4, CX - 10, yb - 2)
    p.cubicTo(CX - 40, yb, CX - 52, yb + 34, CX - 70, yb + 36)
    p.cubicTo(CX - 92, yb + 36, CX - 96, yb - 10, CX - 92, yb - 60)
    p.cubicTo(CX - 88, yb - 120, CX - h - 4, yb - 140, CX - h, yb - 190)
    p.lineTo(CX - h, y0 + 230)
    p.cubicTo(CX - h - 8, y0 + 150, CX - 122, y0 + 120, CX - 128, y0 + 40)
    p.close()
    return p


OSSO = _path_osso()
_BB = OSSO.computeTightBounds()
TOP_L, BOT_L = _BB.top(), _BB.bottom()
ALT_L = BOT_L - TOP_L


def osso(cv, x, yb, s, verm=0.0, brilho_verm=0.0, esp=1):
    """Osso inteiro com a ponta de baixo em (x, yb), escala uniforme `s`.
    esp=-1 espelha (o maléolo passa para a direita): num par visto de frente, os dois maléolos
    apontam para o meio."""
    cv.save(); cv.translate(x, yb); cv.scale(s * esp, s); cv.translate(-CX, -BOT_L)
    if verm > 0:
        cv.drawPath(OSSO, _p(VERMELHO, int(90 * verm + 130 * brilho_verm), "stroke", (12 + 16 * brilho_verm) / s,
                             blur=10 / s, junta=True))
    cv.drawPath(OSSO, paint("#000000", 70, blur=14))
    cv.drawPath(OSSO, paint(OSSO_C, shader=sombra_osso()))
    cv.drawPath(OSSO, _p(OSSO_L, 150, "stroke", 2.5 / s, junta=True))
    if verm > 0:
        cv.drawPath(OSSO, _p(VERMELHO, int(255 * verm), "stroke", 5 / s, junta=True))
    cv.restore()


def topo(yb, s):
    return yb - ALT_L * s


# ------------------------------------------------------------------ balão de lupa (solto)
R0 = 290                     # raio de desenho; o balão vermelho é o mesmo desenho em escala menor
HB, CAM, N_CAM = 70, 17, 4   # altura da faixa, de cada camada de osso novo, nº de camadas
# sombra do balão: mesmo desenho do disco com blur 26, como gradiente radial (bem mais barato)
_RS = R0 + 60
SOMBRA_BALAO = skia.GradientShader.MakeRadial(
    skia.Point(0, 16), _RS, [C("#000000", 120), C("#000000", 120), C("#000000", 60), C("#000000", 18),
                             C("#000000", 0)],
    [0.0, (R0 - 45) / _RS, R0 / _RS, (R0 + 26) / _RS, 1.0])


def faixa_y(G):
    """Topo e base da faixa azul-clara (coordenadas do balão): a pilha cresce centrada."""
    y0 = -HB / 2 - G / 2
    return y0, y0 + HB


def _zig(yc, n=16, amp=13):
    return [(lerp(-R0, R0, i / n), yc + (amp if i % 2 else -amp)) for i in range(n + 1)]


def _poli(pts, pr):
    n = len(pts) - 1; k = clamp(pr) * n; i = int(k)
    p = skia.Path(); p.moveTo(*pts[0])
    for j in range(1, min(i, n) + 1):
        p.lineTo(*pts[j])
    if i < n:
        f = k - i; (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        p.lineTo(lerp(x0, x1, f), lerp(y0, y1, f))
    return p


def balao(cv, bx, by, r, esc, est, t):
    """Lupa redonda: marfim / faixa azul-clara (+ camadas douradas abaixo dela) / marfim.
    est: camadas (4 frações), brilho, pulso, halo, fragil, trinca, ouro, assenta, xis, aro."""
    if esc <= 0.01:
        return
    k = r / R0 * esc
    cv.save(); cv.translate(bx, by); cv.scale(k, k)
    cv.drawCircle(0, 16, R0 + 60, paint("#000000", shader=SOMBRA_BALAO))   # sombra (gradiente: sem blur)
    cv.save()
    clip = skia.Path(); clip.addCircle(0, 0, R0)
    cv.clipPath(clip, skia.ClipOp.kIntersect, True)
    sh = skia.GradientShader.MakeLinear([skia.Point(-R0, 0), skia.Point(R0, 0)],
                                        [C(OSSO_B), C(OSSO_C), C(OSSO_C), C(OSSO_B)], [0.0, 0.36, 0.64, 1.0])
    cv.drawRect(skia.Rect(-R0, -R0, R0, R0), paint(OSSO_C, shader=sh))
    camadas = est.get("camadas", (0.0,) * N_CAM)
    G = sum(CAM * f for f in camadas)
    y0, y1 = faixa_y(G)
    halo = est.get("halo", 0.0)
    if halo > 0:
        cv.drawRect(skia.Rect(-R0, y0 - 22, R0, y1 + 22), paint(NOVO_G, int(150 * halo), blur=22))
    # osso novo: camadas finas douradas logo abaixo da faixa
    y = y1
    for f in camadas:
        if f <= 0:
            continue
        h = CAM * f
        cv.drawRect(skia.Rect(-R0, y, R0, y + h), paint(NOVO))
        cv.drawLine(-R0, y + h - 1.5, R0, y + h - 1.5, paint("#B5701A", int(170 * f), "stroke", 2.5))
        y += h
    gl = est.get("brilho_novo", 0.0)
    if gl > 0 and G > 0:
        cv.drawRect(skia.Rect(-R0, y1 - 6, R0, y1 + G + 6), paint(NOVO_G, int(170 * gl), blur=16))
    cv.drawLine(-R0, y1 + G, R0, y1 + G, paint(OSSO_L, 110, "stroke", 2))
    # a faixa (cartilagem)
    cv.drawRect(skia.Rect(-R0, y0, R0, y1), paint(CART))
    cv.drawRect(skia.Rect(-R0, y0, R0, y0 + 11), paint(CART_HL, 150))
    cv.drawLine(-R0, y0, R0, y0, paint(CART_ESC, 210, "stroke", 2.5))
    cv.drawLine(-R0, y1, R0, y1, paint(CART_ESC, 210, "stroke", 2.5))
    b = est.get("brilho", 0.0)
    if b > 0:
        cv.drawRect(skia.Rect(-R0, y0 - 18, R0, y1 + 18), paint(NOVO_G, int(170 * b), blur=20))
        cv.drawRect(skia.Rect(-R0, y0, R0, y1), paint(OURO, int(120 * b)))
    pu = est.get("pulso", 0.0)
    if pu > 0:                                   # a faixa "produz" cada camada: lampejo na borda de baixo
        cv.drawRect(skia.Rect(-R0, y0, R0, y1), paint("#FFFFFF", int(110 * pu)))
        cv.drawLine(-R0, y1, R0, y1, paint(NOVO_G, int(255 * pu), "stroke", 12, blur=7))
    fr = est.get("fragil", 0.0)
    if fr > 0:
        pul = 0.55 + 0.45 * math.sin(t * 7.0)
        r_f = skia.Rect(-R0 - 12, y0 - 3, R0 + 12, y1 + 3)
        cv.drawRect(r_f, paint(ROSA, int(120 * fr * pul), "stroke", 18, blur=9))
        cv.drawRect(r_f, paint(ROSA, int(255 * fr * (0.45 + 0.55 * pul)), "stroke", 6))
    yc = (y0 + y1) / 2
    tr = est.get("trinca", 0.0)
    ou = est.get("ouro", 0.0)
    if tr > 0 and ou <= 0:
        cv.drawPath(_poli(_zig(yc), tr), _p(TRINCA, 255, "stroke", 5, junta=True))
    elif ou > 0:
        # "colar": a trinca se FECHA no tom da cartilagem (costura fina que não some); o dourado
        # é só um brilho de passagem — osso dourado dentro da faixa leria como ponte óssea na placa
        ass = est.get("assenta", 0.0)
        pth = _poli(_zig(yc, amp=lerp(13, 3, ou)), 1.0)
        gl = 190 * ou * (1 - ass)
        if gl > 1:
            cv.drawPath(pth, _p(NOVO_G, int(gl), "stroke", 16, blur=9, junta=True))
        cv.drawPath(pth, _p(mistura(TRINCA, CART_ESC, ou), int(lerp(255, 200, ou)), "stroke", lerp(5, 3, ou),
                            junta=True))
    xs = est.get("xis", 0.0)
    if xs > 0:
        L = 52 * e_out(xs)
        for sx in (-1, 1):
            cv.drawLine(-L, yc - sx * L, L, yc + sx * L, paint(FUNDO_CARTAO, int(200 * xs), "stroke", 26))
            cv.drawLine(-L, yc - sx * L, L, yc + sx * L, paint(VERMELHO, int(255 * xs), "stroke", 17))
    cv.restore()
    aro = est.get("aro", OURO)
    cv.drawCircle(0, 0, R0, paint("#000000", 90, "stroke", 26, blur=8))
    cv.drawCircle(0, 0, R0, paint(aro, 255, "stroke", 13))
    cv.drawCircle(0, 0, R0 - 10, paint("#FFFFFF", 80, "stroke", 3))
    cv.restore()


def no_balao(cv, bx, by, r, esc):
    """Entra no sistema de coordenadas do balão (para os rótulos de dentro)."""
    k = r / R0 * esc
    cv.save(); cv.translate(bx, by); cv.scale(k, k)


def pilula_seta(cv, s, y_pil, y_alvo, cor, a, tam=34):
    """Rótulo dentro do balão, com seta fina até a faixa (coordenadas do balão)."""
    if a <= 0:
        return
    lw = larg_texto(s, F_BLACK, tam)
    top, bot = y_pil - tam - 4, y_pil + tam * 0.36 + 4
    if y_alvo - bot > 18:
        cv.drawLine(0, bot + 2, 0, y_alvo - 14, paint(cor, int(255 * a), "stroke", 4))
        p = skia.Path(); p.moveTo(-11, y_alvo - 18); p.lineTo(11, y_alvo - 18); p.lineTo(0, y_alvo - 3); p.close()
        cv.drawPath(p, paint(cor, int(255 * a)))
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 20, top, lw / 2 + 20, bot), 16, 16)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(232 * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 3))
    texto(cv, s, 0, y_pil, F_BLACK, tam, cor, int(255 * a))


def escudo(cv, sx, sy, a):
    p = skia.Path()
    p.moveTo(sx, sy - 17); p.lineTo(sx + 15, sy - 11); p.lineTo(sx + 15, sy - 1)
    p.cubicTo(sx + 15, sy + 9, sx + 8, sy + 14, sx, sy + 18)
    p.cubicTo(sx - 8, sy + 14, sx - 15, sy + 9, sx - 15, sy - 1)
    p.lineTo(sx - 15, sy - 11); p.close()
    cv.drawPath(p, paint(OSSO_C, int(255 * a)))
    cv.drawPath(p, _p(OSSO_B, int(255 * a), "stroke", 2.5, junta=True))
    cv.drawLine(sx, sy - 10, sx, sy + 10, paint(OSSO_L, int(160 * a), "stroke", 2.5))


def selo_formado(cv, y, a, esc):
    """Selo marfim com escudo, sobre o marfim do balão (coordenadas do balão)."""
    if a <= 0:
        return
    tam = 32; lw = larg_texto(FORMADO, F_BLACK, tam)
    w = 30 + 14 + lw; x0 = -w / 2
    cv.save(); cv.translate(0, y); cv.scale(esc, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(x0 - 20, -34, x0 + w + 20, 22), 16, 16)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(232 * a)))
    cv.drawRRect(rr, paint(OSSO_C, int(255 * a), "stroke", 3))
    escudo(cv, x0 + 15, -6, a)
    texto(cv, FORMADO, x0 + 44, 5, F_BLACK, tam, OSSO_C, int(255 * a), centro=False)
    cv.restore()


def olho(cv, x, y, raio, a, t, t0):
    """Olho dourado (atenção), piscando devagar."""
    if a <= 0:
        return
    w_aro = max(2.5, raio * 0.075)
    cv.drawCircle(x, y, raio + 8, paint(OURO, int(80 * a * (0.7 + 0.3 * math.sin(t * 3))), blur=14))
    cv.drawCircle(x, y, raio, paint(FUNDO_CARTAO, int(238 * a)))
    cv.drawCircle(x, y, raio, paint(OURO, int(255 * a), "stroke", w_aro))
    fase = (t - t0) % 2.6
    ab = 1.0 - (0.92 * math.sin(math.pi * (fase - 1.8) / 0.8) if fase > 1.8 else 0.0)
    w = raio * 0.70; hh = raio * 0.40 * ab
    p = skia.Path(); p.moveTo(x - w, y); p.quadTo(x, y - hh * 2, x + w, y); p.quadTo(x, y + hh * 2, x - w, y); p.close()
    cv.drawPath(p, paint("#FFF4CF", int(255 * a)))
    cv.save(); cv.clipPath(p, skia.ClipOp.kIntersect, True)
    cv.drawCircle(x, y, raio * 0.28, paint(OURO, int(255 * a)))
    cv.drawCircle(x, y, raio * 0.13, paint("#1A1208", int(255 * a)))
    cv.drawCircle(x - raio * 0.08, y - raio * 0.08, raio * 0.05, paint("#FFFFFF", int(230 * a)))
    cv.restore()
    cv.drawPath(p, _p(OURO, int(255 * a), "stroke", w_aro, junta=True))


# ------------------------------------------------------------------ peças de tela
Y_TL = 1150                  # linha do tempo (folga acima da legenda karaokê de 3 linhas)


def regua(cv, x, ytop, ybot, ynivel, x_osso, a):
    """Régua lateral SEM números: a barra dourada acompanha o comprimento do osso."""
    if a <= 0:
        return
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 8, ytop, x + 8, ybot), 8, 8), paint("#FFFFFF", int(40 * a)))
    yy, i = ybot, 0
    while yy >= ytop:
        cv.drawLine(x + 13, yy, x + (26 if i % 4 == 0 else 20), yy, paint("#FFFFFF", int(120 * a), "stroke", 2))
        yy -= 40; i += 1
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 6, ynivel, x + 6, ybot), 6, 6), paint(OURO, int(255 * a)))
    cv.drawCircle(x, ynivel, 11, paint(OURO, int(255 * a)))
    cv.drawCircle(x, ynivel, 18, paint(NOVO_G, int(90 * a), blur=8))
    cv.drawLine(x + 14, ynivel, x_osso, ynivel, _p(OURO, int(200 * a), "stroke", 3, traco=(10, 8)))


def eixo(cv, x, ya, yb, pr, a):
    """Eixo tracejado reto, de ponta a ponta do osso (desenha de baixo para cima)."""
    if pr <= 0 or a <= 0:
        return
    ye = lerp(yb, ya, e_inout(pr))
    cv.drawLine(x, yb, x, ye, _p(FUNDO_CARTAO, int(170 * a), "stroke", 11, traco=(22, 12)))
    cv.drawLine(x, yb, x, ye, _p(OURO, int(255 * a), "stroke", 6, traco=(22, 12)))


def cota(cv, x, ya, yb, a, t):
    """Cota dourada entre as duas pontas (SEM número)."""
    if a <= 0:
        return
    pr = e_out(clamp(a * 1.4))
    ym = (ya + yb) / 2; m = (yb - ya) / 2 * pr
    cv.drawLine(x, ym - m, x, ym + m, paint(NOVO_G, int(110 * a * (0.7 + 0.3 * math.sin(t * 5))), "stroke", 16, blur=8))
    cv.drawLine(x, ym - m, x, ym + m, paint(OURO, int(255 * a), "stroke", 5))
    for yy in (ym - m, ym + m):
        cv.drawLine(x - 16, yy, x + 16, yy, paint(OURO, int(255 * a), "stroke", 5))


def bandeira(cv, x, ybase, t, t0, a):
    """Bandeirinha fincada no fim da linha do tempo (o pano tremula para a esquerda)."""
    k = t - t0
    if k < 0 or a <= 0:
        return
    cai = e_out(clamp(k / 0.28)); al = a * clamp(k / 0.08)
    dy = -40 * (1 - cai)                 # queda curta: o pano nunca sobe até o osso de cima
    tam = 30; lw = larg_texto(FIM, F_BLACK, tam)
    ytop = ybase - 86 + dy
    cv.drawLine(x, ytop - 8, x, ybase + 10 + dy, paint("#000000", int(80 * al), "stroke", 9, blur=4))
    cv.drawLine(x, ytop - 8, x, ybase + 10 + dy, paint("#DDE6EE", int(255 * al), "stroke", 6))
    cv.drawCircle(x, ytop - 10, 7, paint(OURO, int(255 * al)))
    x1 = x - 4; x0 = x1 - (lw + 52); hb = 48
    wv = 6 * math.sin(t * 4.5)
    p = skia.Path(); p.moveTo(x1, ytop)
    p.quadTo((x0 + x1) / 2, ytop - wv, x0, ytop + wv * 0.6)
    p.lineTo(x0 + 20, ytop + hb / 2 + wv * 0.6)                  # rabo de andorinha
    p.lineTo(x0, ytop + hb + wv * 0.6)
    p.quadTo((x0 + x1) / 2, ytop + hb - wv, x1, ytop + hb); p.close()
    cv.drawPath(p, paint("#000000", int(70 * al), blur=8))
    cv.drawPath(p, paint(OURO, int(255 * al)))
    cv.drawPath(p, _p("#8A6512", int(255 * al), "stroke", 2.5, junta=True))
    texto(cv, FIM, (x0 + 20 + x1) / 2, ytop + 35, F_BLACK, tam, FUNDO_CARTAO, int(255 * al))


def selo_bom(cv, x, y, t, t0, a):
    """Selo verde 'DO LADO BOM' entrando girando."""
    k = t - t0
    if k < 0 or a <= 0:
        return
    e = clamp(k / 0.65)
    esc = lerp(0.5, 1.0, e_back(e)); rot = lerp(-40, -4, e_out(e)); al = a * clamp(k / 0.12)
    tam = 44; lw = larg_texto(BOM, F_BLACK, tam)
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(esc, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 36, -44, lw / 2 + 36, 44), 44, 44)
    cv.drawRRect(rr, paint(VERDE, int(120 * al), blur=18))
    cv.drawRRect(rr, paint(VERDE, int(245 * al)))
    cv.drawRRect(rr, paint(VERDE_CL, int(255 * al), "stroke", 4))
    dentro = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 26, -34, lw / 2 + 26, 34), 34, 34)
    cv.drawRRect(dentro, _p("#FFFFFF", int(120 * al), "stroke", 2.5, traco=(9, 7)))
    texto(cv, BOM, 0, 16, F_BLACK, tam, "#FFFFFF", int(255 * al))
    cv.restore()


# ------------------------------------------------------------------ estado da cena
X_A, YB_A, S_A = 215, 1080, 0.62          # o osso da criança (cena 1 e 3)
BX, BY = 712, 700                          # o balão grande
XR, YT_R0, YT_R1 = 58, 300, 1080           # régua
X_SAO, X_LES, YB_B, S_B = 330, 600, 1015, 0.49   # as duas pernas (cena 2)
BR_X, BR_Y, BR_R = 600, 345, 110           # balão vermelho, acima do osso com lesão
TL_X0, TL_X1 = 90, 975                     # linha do tempo


def osso_a(t, T):
    x = lerp(540, X_A, e_inout(prog(t, T["area"] - 0.25, T["area"] + 0.2)))   # para antes de o balão nascer
    ent = lerp(0.9, 1.0, e_back(prog(t, 0.0, 0.55)))
    # o osso inteiro cresce um degrau a cada camada de osso novo que nasce no balão
    cres = (1 + 0.05 * sum(camadas(t, T))) * (1 + 0.055 * e_inout(prog(t, T["pro"] + 0.2, T["alinhado"] + 0.4)))
    return x, S_A * ent * cres


def t_camada(T, i):
    """Início da camada i: de "ali" até "aumenta" (a última cai em "aumenta"; tudo acaba antes de "Só")."""
    return T["ali"] + i * (T["aumenta"] - T["ali"]) / (N_CAM - 1)


def camadas(t, T):
    return tuple(e_out(prog(t, t_camada(T, i), t_camada(T, i) + 0.3)) for i in range(N_CAM))


def ossos_b(t, T):
    g = e_inout(prog(t, T["pode"], T["curta"] + 0.3))
    s_sao = S_B * (1 + 0.18 * g)
    s_les = S_B * (1 + min(0.18 * g, 0.04))           # o de contorno vermelho para antes
    parou = clamp((0.18 * g - 0.04) / 0.02) * (1 - prog(t, T["curta"] + 0.5, T["curta"] + 1.0))
    return s_sao, s_les, parou


def tremor(t, eventos):
    d = 0.0
    for t0, forca in eventos:
        k = t - t0
        if 0 <= k < 0.35:
            d += forca * math.sin(k * 70) * (1 - k / 0.35)
    return d


# ------------------------------------------------------------------ cena 1 e 3: o osso e a lupa
def cena_a(cv, t, T):
    x, s = osso_a(t, T)
    cena1 = 1 - prog(t, T["acidente"], T["acidente"] + 0.35)     # rótulos da cena 1 não voltam na 3

    # régua sem números (a partir de "por ali", antes da 1ª camada)
    a_reg = prog(t, T["ali"] - 0.25, T["ali"] + 0.05) * cena1
    regua(cv, XR, YT_R0, YT_R1, topo(YB_A, s), x - 40 * s, a_reg)

    osso(cv, x, YB_A, s)

    # eixo tracejado ("pro osso crescer alinhado")
    a_eixo = prog(t, T["pro"] - 0.05, T["pro"] + 0.15) * cena1
    eixo(cv, x, topo(YB_A, s) - 26, YB_A + 6, prog(t, T["pro"], T["pro"] + 0.55), a_eixo)
    brilhos(cv, x, topo(YB_A, s) + 20, t, T["alinhado"] + 0.05, n=12, raio=130)

    # "?" dourado na capa
    a_q = 1 - prog(t, T["area"] - 0.2, T["area"] + 0.2)
    if a_q > 0:
        pul = lerp(0.85, 1.0, e_back(prog(t, 0.0, 0.45))) * (1 + 0.07 * math.sin(t * 6.5))
        cv.save(); cv.translate(800, 790); cv.scale(pul, pul)
        cv.drawCircle(0, -10, 120, paint(NOVO_G, int(70 * a_q), blur=40))
        texto(cv, INTERROGA, 0, 70, F_BLACK, 220, OURO, int(255 * a_q), contorno=12)
        cv.restore()

    # o balão
    esc = e_back(prog(t, T["area"] + 0.15, T["area"] + 0.55))               # nasce com o osso já parado
    esc *= 1 + 0.06 * e_inout(prog(t, T["lado"] + 0.3, T["colar"]))        # cena 3: aproxima a lupa
    if esc <= 0.01:
        return
    by = BY + 4 * math.sin(t * 1.2)
    bx = BX + tremor(t, ((T["fratura"] + 0.02, 7),))
    cam = camadas(t, T)
    G = sum(CAM * f for f in cam)
    halo = 0.0
    if t >= T["colar"] + 0.8:
        halo = ((0.30 + 0.15 * math.sin(t * 2.6)) * prog(t, T["colar"] + 0.8, T["colar"] + 1.4)
                * (1 - prog(t, T["manda"] - 0.15, T["manda"] + 0.2)))      # apaga atrás da CTA
    est = dict(
        camadas=cam,
        brilho=prog(t, T["placa"], T["placa"] + 0.15) * (1 - prog(t, T["placa"] + 0.7, T["placa"] + 1.3)),
        pulso=max(max(0.0, 1 - abs(t - (t_camada(T, i) + 0.08)) / 0.18) for i in range(N_CAM)),
        brilho_novo=prog(t, T["ali"] - 0.2, T["ali"]) * (1 - prog(t, T["so"] - 0.1, T["so"] + 0.5)),
        halo=halo,
        fragil=prog(t, T["fragil"], T["fragil"] + 0.25) * (1 - prog(t, T["acompanhamento"], T["acompanhamento"] + 0.6)),
        trinca=e_out(prog(t, T["fratura"] + 0.02, T["fratura"] + 0.32)),
        ouro=e_inout(prog(t, T["colar"], T["colar"] + 0.8)),
        assenta=prog(t, T["colar"] + 0.8, T["colar"] + 1.4),
        aro=OURO)
    balao(cv, bx, by, R0, esc, est, t)

    y0, y1 = faixa_y(G)
    no_balao(cv, bx, by, R0, esc)
    a1 = prog(t, T["cartilagem"] - 0.1, T["cartilagem"] + 0.2) * (1 - prog(t, T["fragil"] - 0.25, T["fragil"] - 0.05))
    pilula_seta(cv, AREA, -130, y0, AZUL, a1)
    a2 = prog(t, T["fragil"], T["fragil"] + 0.2) * (1 - prog(t, T["acompanhamento"] - 0.25, T["acompanhamento"] - 0.05))
    pilula_seta(cv, FRAGIL, -130, y0, ROSA, a2)
    a3 = prog(t, T["formado"] - 0.05, T["formado"] + 0.2) * cena1
    selo_formado(cv, 150, a3, lerp(0.6, 1.0, e_back(prog(t, T["formado"] - 0.05, T["formado"] + 0.35))))
    e_olho = e_back(prog(t, T["acompanhamento"], T["acompanhamento"] + 0.4))
    a_olho = clamp(e_olho * 2) * cena1
    if a_olho > 0:
        olho(cv, 0, -150, 52 * max(0.0, e_olho), a_olho, t, T["acompanhamento"] + 0.4)
    cv.restore()

    brilhos(cv, bx, by + (y0 + y1) / 2, t, T["placa"] + 0.05, n=14, raio=230)
    brilhos(cv, bx, by + y1 + G / 2, t, T["aumenta"] + 0.3, n=14, raio=230)
    brilhos(cv, bx, by + (y0 + y1) / 2, t, T["colar"] + 0.55, n=16, raio=240)

    # título acima do balão
    a_t = prog(t, T["placa"], T["placa"] + 0.3) * cena1
    if a_t > 0:
        dy = -18 * (1 - e_out(prog(t, T["placa"], T["placa"] + 0.4)))
        texto(cv, PLACA, BX, 322 + dy, F_BLACK, 46, "#FFFFFF", int(255 * a_t), contorno=9)
        texto(cv, FISE, BX, 368 + dy, F_SEMI, 34, AZUL, int(255 * a_t), contorno=6)


# ------------------------------------------------------------------ cena 2: as duas pernas
def cena_b(cv, t, T):
    s_sao, s_les, parou = ossos_b(t, T)
    dx = tremor(t, ((T["acidente"] + 0.1, 8),))        # junto com o carimbo
    ent = [e_out(prog(t, T["acidente"] - 0.05 + 0.12 * i, T["acidente"] + 0.45 + 0.12 * i)) for i in range(2)]
    cv.drawLine(250, YB_B + 4, 830, YB_B + 4, paint("#FFFFFF", int(50 * min(ent)), "stroke", 3))
    verm = prog(t, T["lesao"], T["lesao"] + 0.3)
    # o par visto de frente: maléolos voltados para o meio (o da esquerda é espelhado)
    for i, (x, s, vm, bv, esp) in enumerate(((X_SAO, s_sao, 0.0, 0.0, -1), (X_LES, s_les, verm, parou, 1))):
        if ent[i] <= 0:
            continue
        if ent[i] < 0.5:
            cv.saveLayerAlpha(None, int(255 * clamp(ent[i] * 2)))
        else:
            cv.save()                                   # opaco: sem camada de tela cheia
        osso(cv, x + dx, YB_B + 160 * (1 - ent[i]), s, vm, bv, esp)
        cv.restore()

    # nível e cota (sem número)
    a_c = prog(t, T["curta"] - 0.05, T["curta"] + 0.3)
    if a_c > 0:
        ys, yl = topo(YB_B, s_sao), topo(YB_B, s_les)
        xc = X_LES + 105
        cv.drawLine(X_SAO - 90, ys, xc + 22, ys, _p("#FFFFFF", int(200 * a_c), "stroke", 3.5, traco=(14, 10)))
        cv.drawLine(X_LES + 40, yl, xc + 22, yl, _p("#FFFFFF", int(200 * a_c), "stroke", 3.5, traco=(14, 10)))
        cota(cv, xc, ys, yl, a_c, t)

    # balão vermelho, solto acima do osso com lesão
    esc = e_back(prog(t, T["lesao"] + 0.2, T["lesao"] + 0.6))          # nasce quando o carimbo já saiu
    est = dict(xis=prog(t, T["lesao"] + 0.5, T["lesao"] + 0.75), aro=VERMELHO)
    balao(cv, BR_X + dx, BR_Y + 5 * math.sin(t * 1.8), BR_R, esc, est, t)

    # linha do tempo: marcador (o olho) desliza até o fim do crescimento
    a_tl = prog(t, T["acompanhar"] - 0.05, T["acompanhar"] + 0.25)
    if a_tl > 0:
        k = e_inout(prog(t, T["acompanhar"] + 0.1, T["cresc2"] + 0.55))
        xm = lerp(TL_X0, TL_X1, k)
        cv.drawLine(TL_X0, Y_TL, TL_X1, Y_TL, paint("#FFFFFF", int(60 * a_tl), "stroke", 8))
        cv.drawLine(TL_X0, Y_TL, xm, Y_TL, paint(OURO, int(255 * a_tl), "stroke", 8))
        cv.drawCircle(TL_X0, Y_TL, 11, paint(OURO, int(255 * a_tl)))             # ponto de partida (sem texto)
        bandeira(cv, TL_X1, Y_TL, t, T["fim"], a_tl)
        olho(cv, xm, Y_TL, 27, a_tl, t, T["acompanhar"])
        brilhos(cv, TL_X1, Y_TL - 40, t, T["cresc2"] + 0.6, n=12, raio=120)


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    # trocas de cena sem sobreposição: uma sai inteira antes de a outra entrar
    a_a = (1 - prog(t, T["acidente"] - 0.4, T["acidente"] - 0.08)) + prog(t, T["lado"] - 0.02, T["lado"] + 0.3)
    a_b = prog(t, T["acidente"] - 0.1, T["acidente"] + 0.1) * (1 - prog(t, T["lado"] - 0.32, T["lado"] - 0.04))
    if a_b > 0:
        cv.saveLayerAlpha(None, int(255 * clamp(a_b))) if a_b < 1 else cv.save()
        cena_b(cv, t, T)
        cv.restore()
    a_a = clamp(a_a) * (1 - 0.7 * prog(t, T["manda"] - 0.15, T["manda"] + 0.25))   # CTA: o balão fica apagado
    if a_a > 0:
        cv.saveLayerAlpha(None, int(255 * a_a)) if a_a < 1 else cv.save()
        cena_a(cv, t, T)
        cv.restore()

    # carimbos
    # FRATURA: abaixo do balão, sem tocar o aro
    carimbo_vermelho(cv, FRATURA, 690, 1074, -5, T["fratura"] + 0.02, t, dur=1.5)
    # ACIDENTE GRAVE: no alto, onde o balão vermelho nasce em "lesão" — sai junto com essa entrada
    carimbo_vermelho(cv, ACIDENTE, 540, 330, -5, T["acidente"] + 0.08, t,
                     dur=clamp(T["lesao"] + 0.2 - (T["acidente"] + 0.08), 0.9, 1.9))

    a_fim = 1 - prog(t, T["manda"] - 0.35, T["manda"] - 0.1)
    selo_bom(cv, BX, 318, t, T["lado"] + 0.15, a_fim)

    capa(cv, t, T["area"], ep["gancho"][0], ep["gancho"][1])
    # entra só quando o gancho já saiu (sem sobrepor as letras que somem)
    selo_como_funciona(cv, prog(t, T["area"] + 0.45, T["area"] + 0.85) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface(cv, t, T, blocos, DESTAQUE)


# ------------------------------------------------------------------ som e prévias
def sons(T):
    ev = [(0.05, "whoosh", 0.4), (0.25, "pop", 0.5),
          (T["area"] - 0.05, "whoosh", 0.55), (T["area"] + 0.2, "pop", 0.65), (T["cartilagem"] + 0.05, "tick", 0.35),
          (T["placa"], "shimmer", 0.75), (T["placa"] + 0.05, "ping", 0.4),
          (T["ali"] - 0.05, "shimmer", 0.8)]
    ev += [(t_camada(T, i) + 0.05, "click", 0.75) for i in range(N_CAM)]
    ev += [(T["aumenta"] + 0.35, "ding", 0.45),
           (T["fragil"], "ping", 0.55), (T["formado"] - 0.02, "thump", 0.55),
           (T["fratura"] + 0.02, "tick", 1.0), (T["fratura"] + 0.04, "thump", 0.85),
           (T["acompanhamento"] + 0.05, "pop", 0.55), (T["acompanhamento"] + 0.15, "shimmer", 0.35),
           (T["pro"], "whoosh", 0.4), (T["alinhado"] + 0.05, "ding", 0.55),
           (T["acidente"] - 0.1, "whoosh", 0.45), (T["acidente"] + 0.08, "thump", 0.9),
           (T["lesao"] + 0.22, "pop", 0.7), (T["lesao"] + 0.52, "tick", 0.5)]
    n = max(2, int((T["curta"] + 0.3 - T["pode"]) / 0.22))
    ev += [(T["pode"] + 0.22 * i, "click", 0.55) for i in range(n)]               # os dois ossos crescendo
    ev += [(T["curta"], "thump", 0.6),
           (T["acompanhar"], "whoosh", 0.4), (T["fim"] + 0.2, "thump", 0.6), (T["fim"] + 0.25, "shimmer", 0.45),
           (T["cresc2"] + 0.6, "ding", 0.5),
           (T["lado"] - 0.05, "whoosh", 0.5), (T["lado"] + 0.45, "pop", 0.6),
           (T["colar"], "shimmer", 0.85), (T["colar"] + 0.6, "ding", 0.5),
           (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def tempos_previa(T):
    return [0.0, T["area"] + 0.7, T["placa"] + 0.6, T["ali"] + 0.55, T["formado"] + 0.3, T["fratura"] + 0.5,
            T["alinhado"] + 0.4, T["lesao"] + 0.7, T["curta"] + 0.5, T["fim"] + 0.7, T["colar"] + 1.6,
            T["manda"] + 1.6]


render = fazer_render(quadro, ANCORAS, sons, tempos_previa, respiro_cta=2.0)
