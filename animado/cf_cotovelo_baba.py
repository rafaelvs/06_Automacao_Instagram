# -*- coding: utf-8 -*-
"""COMO FUNCIONA — cotovelo de babá / pronação dolorosa ("NÃO MEXE O BRAÇO / DEPOIS DO PUXÃO?").

Mesmo estilo das cenas aprovadas (fundo azul-petróleo, dourado, rótulos, carimbo ouro opaco, brilhos,
prancheta, lupa, legenda karaokê, CTA com aviãozinho). O que o verificador exigiu está aqui:
  * Braço e criança de DESENHO: pele lisa e opaca, sem osso, nada translúcido, nenhum fundo preto,
    rosto sem detalhe. A mão adulta é só mão e manga, sem pessoa e sem rosto.
  * A seta de tração estica UMA vez, sem tranco nem tremor, e sem som de estalo.
  * O balão do cotovelo mostra só a REGIÃO ampliada do próprio desenho (contorno de pele liso), sem
    dobra, prega ou lado marcado. "Um ligamento" é uma tira rosada ESQUEMÁTICA no centro do balão:
    sem anel, sem osso, sem nome. Ela desliza devagar para fora da marca tracejada e fica PARADA,
    dentro do balão, com contorno vermelho suave (som de deslize, nunca clique). "ESCORREGA" é o
    único carimbo: ouro, fundo opaco, sem tremor de câmera.
  * O braço fica esticado JUNTO ao corpo; a lupa do inchaço só aumenta o próprio desenho e não
    compara com o outro braço.
  * "NÃO PUXE NEM FORCE": a mão adulta volta apagada e leva um X; nenhuma manobra é mostrada e nada
    volta ao lugar. A correção é com o ortopedista: sem selo de resultado, sem check de resolvido.
  * Prevenção: OUTRA criança (outra roupa, outro cabelo, braços abertos sem pose de vitória), erguida
    pelas axilas (seta para cima; o check verde fica no rótulo "PELAS AXILAS", nunca no braço) e, ao
    lado, a mão adulta segurando a mãozinha, com X. "AJUDA A PREVENIR" é um selo sóbrio, sem brilho.
    Na CTA só sobra a cena da prevenção escurecida, sem X nem check.
A cena é PRESA ao roteiro pelas palavras-âncora (ANCORAS): mudar o roteiro sem elas quebra o
render de propósito (KeyError), em vez de sair vídeo dessincronizado.
"""
import math

import skia

from .cf_alongamento import (F_BLACK, F_SEMI, OURO, PELE, VERMELHO, H, W, brilhos, clamp, e_back,
                             e_inout, e_out, fundo, lerp, paint, prog, texto)
from .cf_comum import capa, fazer_render, interface, selo_como_funciona

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "puxao": ("puxão", 1, False), "mexer": ("mexer", 1, False), "tem": ("tem", 1, False),
    "cotovelo1": ("cotovelo", 1, False), "baba": ("babá", 1, False), "pronacao": ("pronação", 1, False),
    "mao2": ("mão", 2, False), "cotovelo2": ("cotovelo", 2, False), "ligamento": ("ligamento", 1, False),
    "escorrega": ("escorrega", 1, False), "braco2": ("braço", 2, False), "esticado": ("esticado", 1, False),
    "ao": ("ao", 1, False), "lado": ("lado", 1, False), "corpo": ("corpo", 1, False),
    "sem": ("sem", 1, False), "inchaco": ("inchaço", 1, False),
    "puxe": ("puxe", 1, False), "procure": ("procure", 1, False),
    "avaliacao": ("avaliação", 1, False), "ortopedista": ("ortopedista", 1, False),
    "levantar": ("levantar", 1, False), "axilas": ("axilas", 1, False), "maos": ("mãos", 1, False),
    "pulsos": ("pulsos", 1, False), "prevenir": ("prevenir", 1, False), "manda": ("manda", 1, False),
}
DESTAQUE = {"puxão", "mão", "mexer", "cotovelo", "babá", "pronação", "dolorosa", "ligamento", "escorrega",
            "esticado", "corpo", "inchaço", "puxe", "force", "avaliação", "ortopedista", "axilas", "pulsos",
            "prevenir"}

# rótulos (todos estão em ep["tela"])
R_PUXAO, R_MEXER = "PUXÃO PELA MÃO", "NÃO QUER MEXER"
R_TITULO, R_SUB = "COTOVELO DE BABÁ", "PRONAÇÃO DOLOROSA"
R_NAMAO, R_NOCOT, R_LIG, R_ESC = "NA MÃO", "NO COTOVELO", "UM LIGAMENTO", "ESCORREGA"
R_ESTIC, R_LADO, R_INCH = "BRAÇO ESTICADO", "AO LADO DO CORPO", "SEM INCHAÇO APARENTE"
R_PUXE, R_AVAL, R_ORTO = "NÃO PUXE NEM FORCE", "PROCURE AVALIAÇÃO", "A CORREÇÃO É COM O ORTOPEDISTA"
R_AXI, R_MAOS1, R_MAOS2, R_PREV = "PELAS AXILAS", "NÃO PELAS MÃOS", "OU PULSOS", "AJUDA A PREVENIR"

# ------------------------------------------------------------------ paleta
PELE_CL, PELE_ESC, PELE_LINHA = "#F7CDB8", "#DA987E", "#B9765E"
CAMISA, CAMISA_CL, CAMISA_ESC, CAMISA_LINHA = "#6FC7B1", "#9EE0CF", "#3F9A85", "#2C7464"
SHORT, SHORT_CL, SHORT_ESC = "#4C86C6", "#6FA3DA", "#3A6FA8"
CABELO = "#4A3426"
AD, AD_CL, AD_ESC, AD_LINHA = "#C98D6E", "#DDA98C", "#A56C50", "#7C4C37"     # mão adulta: outro tom
PUNHO, PUNHO_CL, PUNHO_ESC = "#3B5C84", "#5479A6", "#27415F"                # manga do adulto
LIG, LIG_CL, LIG_ESC = "#F29DB2", "#FAC9D5", "#C9708A"                       # a tira (esquema)
VERDE, VERDE_ESC = "#46C48C", "#1E7A52"
CINZA = "#9AAABB"
AZUL = "#9CC9FF"
MARFIM, MARFIM_B, MARFIM_L = "#F7EEDD", "#D5C3A2", "#8C7656"
FUNDO_CARTAO = "#0B1824"
TONS_PELE = (PELE_ESC, PELE, PELE_CL, PELE, PELE_ESC)
TONS_AD = (AD_ESC, AD, AD_CL, AD, AD_ESC)
TONS_CAMISA = (CAMISA_ESC, CAMISA, CAMISA_CL, CAMISA, CAMISA_ESC)
TONS_PUNHO = (PUNHO_ESC, PUNHO, PUNHO_CL, PUNHO, PUNHO_ESC)
# roupa de cada criança: a da prevenção é OUTRA criança (outra roupa, outro cabelo), para que nada
# na tela pareça "o braço do puxão voltou a mexer"
ROUPA_B = dict(camisa=TONS_CAMISA, camisa_linha=CAMISA_LINHA, camisa_esc=CAMISA_ESC,
               short=SHORT, short_cl=SHORT_CL, cabelo=CABELO, chiquinhas=False)
ROUPA_C = dict(camisa=("#7E68BE", "#9C86D6", "#BBA9E8", "#9C86D6", "#7E68BE"), camisa_linha="#55428A",
               camisa_esc="#6A55A8", short="#E0A43C", short_cl="#EDBE6A", cabelo="#9A5B2E", chiquinhas=True)

R1, R2 = 1150, 1214                    # linhas de rótulo (abaixo da cena, acima da legenda)


# ------------------------------------------------------------------ utilidades (copiadas de cf_escoliose / cf_pseudartrose)
def _c(h, a=255):
    h = h.lstrip("#")
    return skia.ColorSetARGB(int(a), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def camada(cv, a, cinza=0.0, escuro=0.0):
    """saveLayer com transparência (e, se pedido, tons de cinza e escurecimento: o que sai de foco)."""
    if a >= 0.999 and cinza <= 0 and escuro <= 0:
        cv.save(); return
    p = skia.Paint()
    p.setAlphaf(clamp(a))
    if cinza > 0 or escuro > 0:
        k = clamp(cinza); s = 1 - k; m = 1 - clamp(escuro)
        r, g, b = 0.2126 * k, 0.7152 * k, 0.0722 * k
        p.setColorFilter(skia.ColorFilters.Matrix([(r + s) * m, g * m, b * m, 0, 0,
                                                   r * m, (g + s) * m, b * m, 0, 0,
                                                   r * m, g * m, (b + s) * m, 0, 0,
                                                   0, 0, 0, 1, 0]))
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


def desvanecer(cv, x0, y0, x1, y1):
    """Dentro de um saveLayer: apaga em degradê de (x0, y0) [opaco] a (x1, y1) [some] (DstIn)."""
    m = skia.Paint(AntiAlias=True)
    m.setShader(skia.GradientShader.MakeLinear([skia.Point(x0, y0), skia.Point(x1, y1)],
                                               [skia.ColorSetARGB(255, 0, 0, 0), skia.ColorSetARGB(0, 0, 0, 0)]))
    m.setBlendMode(skia.BlendMode.kDstIn)
    cv.drawRect(skia.Rect(-4000, -4000, 4000, 4000), m)


def ponta(cv, x, y, ang, tam, cor, a):
    """Cabeça de seta em (x, y) apontando para `ang` (radianos)."""
    p = skia.Path()
    p.moveTo(x + tam * math.cos(ang), y + tam * math.sin(ang))
    p.lineTo(x + tam * 0.75 * math.cos(ang + 2.45), y + tam * 0.75 * math.sin(ang + 2.45))
    p.lineTo(x + tam * 0.75 * math.cos(ang - 2.45), y + tam * 0.75 * math.sin(ang - 2.45))
    p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))


def seta(cv, x0, y0, x1, y1, cor, a, larg=9, tam=30):
    if a <= 0 or math.hypot(x1 - x0, y1 - y0) < 2:
        return
    ang = math.atan2(y1 - y0, x1 - x0)
    xb, yb = x1 - tam * 0.55 * math.cos(ang), y1 - tam * 0.55 * math.sin(ang)
    cv.drawLine(x0, y0, xb, yb, paint(cor, int(90 * a), "stroke", larg + 10, blur=7))
    cv.drawLine(x0, y0, xb, yb, paint(cor, int(255 * a), "stroke", larg))
    ponta(cv, x1, y1, ang, tam, cor, a)


def chip(cv, s, x, y, cor, a, tam=42, borda=None, esc=1.0):
    """Rótulo solto centrado em x; y = linha de base do texto."""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    cv.save(); cv.translate(x, y - tam * 0.35); cv.scale(esc, esc); cv.translate(-x, -(y - tam * 0.35))
    rr = skia.RRect.MakeRectXY(skia.Rect(x - lw / 2 - 24, y - tam * 1.05, x + lw / 2 + 24, y + tam * 0.34), 16, 16)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(225 * a)))
    cv.drawRRect(rr, paint(borda or cor, int(255 * a), "stroke", 3))
    cv.drawString(s, x - lw / 2, y, f, paint(cor, int(255 * a)))
    cv.restore()


def chip_esq(cv, s, x, y, cor, a, tam=40, borda=None, dx=0.0):
    """Igual ao chip, alinhado pela ESQUERDA da caixa (x)."""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    x += dx
    rr = skia.RRect.MakeRectXY(skia.Rect(x, y - tam * 1.05, x + lw + 40, y + tam * 0.34), 16, 16)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(225 * a)))
    cv.drawRRect(rr, paint(borda or cor, int(255 * a), "stroke", 3))
    cv.drawString(s, x + 20, y, f, paint(cor, int(255 * a)))


def carimbo_opaco(cv, s, x, y, rot, t0, t, dur, tam=60, esc0=1.5):
    """Carimbo ouro torto com fundo opaco, sem tremor (padrão de condição clínica: cf_pseudartrose)."""
    k = t - t0
    if k < 0 or k > dur:
        return
    esc = lerp(esc0, 1.0, e_out(clamp(k / 0.16))); a = clamp(k / 0.08) * (1 - prog(k, dur - 0.35, dur))
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(esc, esc)
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 24, -tam, lw / 2 + 24, tam * 0.36), 12, 12)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(240 * a))); cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 7))
    cv.drawString(s, -lw / 2, 0, f, paint(OURO, int(255 * a)))
    cv.restore()


def tique(cv, x, y, pr, cor, a, esc=1.0, larg=6):
    """Tique desenhado em 2 traços (pr 0..1); (x, y) = início do traço curto."""
    if pr <= 0 or a <= 0:
        return
    p = skia.Path(); p.moveTo(x, y)
    p.lineTo(x + 12 * esc * min(1, pr * 2), y + 12 * esc * min(1, pr * 2))
    if pr > 0.5:
        q = (pr - 0.5) * 2
        p.lineTo(x + (12 + 22 * q) * esc, y + (12 - 30 * q) * esc)
    cv.drawPath(p, paint(cor, int(255 * a), "stroke", larg * esc))


def xis(cv, x, y, L, pr, a):
    """X vermelho com contorno escuro (lê sobre qualquer fundo); pr 0..1 = os dois traços."""
    if pr <= 0 or a <= 0:
        return
    for k, sx in enumerate((-1, 1)):
        q = clamp(pr * 2 - k)
        if q <= 0:
            continue
        x0, y0 = x - L, y - sx * L
        x1, y1 = lerp(x0, x + L, e_out(q)), lerp(y0, y + sx * L, e_out(q))
        cv.drawLine(x0, y0, x1, y1, paint(FUNDO_CARTAO, int(210 * a), "stroke", 30))
        cv.drawLine(x0, y0, x1, y1, paint(VERMELHO, int(255 * a), "stroke", 18))


def selo_check(cv, x, y, r, pr, a):
    """Check verde redondo (a orientação certa, não um resultado)."""
    if pr <= 0 or a <= 0:
        return
    s = e_back(clamp(pr))
    cv.save(); cv.translate(x, y); cv.scale(s, s)
    cv.drawCircle(0, 0, r + 6, paint(VERDE, int(90 * a), blur=10))
    cv.drawCircle(0, 0, r, paint(VERDE, int(255 * a)))
    cv.drawCircle(0, 0, r, paint(VERDE_ESC, int(255 * a), "stroke", 3))
    tique(cv, -r * 0.42, -r * 0.02, clamp(pr * 1.6 - 0.3), "#FFFFFF", a, esc=r / 34, larg=7)
    cv.restore()


def prancheta(cv, x, y, a, t, t0):
    """Prancheta marfim com prendedor dourado e checklist (caixinhas com tique, linhas sem texto)."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(4, 8, 92, 124), 12, 12), paint("#000000", int(80 * a), blur=8))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(0, 0, 88, 116), 12, 12), paint(MARFIM, int(255 * a)))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(0, 0, 88, 116), 12, 12), paint(MARFIM_L, int(200 * a), "stroke", 2.5))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(24, -10, 64, 14), 7, 7), paint(OURO, int(255 * a)))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(24, -10, 64, 14), 7, 7), paint("#8A6512", int(255 * a), "stroke", 2))
    for i in range(3):
        yy = 40 + i * 25
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(12, yy - 8, 28, yy + 8), 4, 4), paint("#B9AE98", int(255 * a), "stroke", 2.5))
        tique(cv, 14, yy - 1, e_out(prog(t, t0 + 0.25 + 0.15 * i, t0 + 0.5 + 0.15 * i)), "#C08A1E", a, esc=0.42, larg=8)
        cv.drawLine(36, yy, 74, yy, paint("#B9AE98", int(230 * a), "stroke", 5))
    cv.restore()


# ------------------------------------------------------------------ parte A: o braço de desenho, em diagonal
SA = (-60.0, 1100.0)                   # ombro (fora da tela: a manga entra pela esquerda)
HA = (800.0, 730.0)                    # centro da mãozinha
_DX, _DY = HA[0] - SA[0], HA[1] - SA[1]
LA = math.hypot(_DX, _DY)
UA = (_DX / LA, _DY / LA)              # eixo do braço (do ombro para a mão)
NA = (UA[1], -UA[0])                   # normal "para cima" (cima-esquerda na tela)
ANG_A = math.degrees(math.atan2(_DY, _DX))
FE = 0.5


def pa(f, off=0.0):
    return (SA[0] + UA[0] * LA * f + NA[0] * off, SA[1] + UA[1] * LA * f + NA[1] * off)


EA = pa(FE)                            # o cotovelo do desenho (meio do braço)


def path_maozinha(cx, esc=1.0):
    """Mãozinha de desenho (palma + 4 dedinhos + polegar), centrada em (cx, 0), dedos para +x."""
    k = esc
    partes = [oval_path(cx - 62 * k, -55 * k, cx + 58 * k, 55 * k),
              oval_path(cx - 48 * k, -76 * k, cx + 8 * k, -40 * k)]                 # polegar (lado de cima)
    for i, yy in enumerate((-36, -12, 12, 36)):
        xf = cx + (78 - 6 * abs(i - 1.5)) * k
        partes.append(rr_path(cx + 20 * k, (yy - 13) * k, xf, (yy + 13) * k, 13 * k))
    return uniao(*partes)


def _largura_a(x):
    """Meia-largura do braço ao longo do eixo: ombro cheio, afina de leve no cotovelo (sem prega)."""
    L = LA; xe = L * FE; xw = L - 70
    pts = ((-120, 68), (0, 68), (xe * 0.55, 64), (xe, 55), (xe + (xw - xe) * 0.28, 57), (xw, 44), (xw + 40, 44))
    for (x0, w0), (x1, w1) in zip(pts, pts[1:]):
        if x <= x1:
            u = clamp((x - x0) / (x1 - x0))
            return lerp(w0, w1, 0.5 - 0.5 * math.cos(math.pi * u))
    return pts[-1][1]


def _path_braco_a():
    """Braço liso (sem dobra nem prega) + mãozinha, no referencial do braço (x ao longo dele)."""
    L = LA; n = 90
    xs = [lerp(-120, L - 30, i / n) for i in range(n + 1)]
    p = skia.Path()
    for i, x in enumerate(xs):
        (p.moveTo if i == 0 else p.lineTo)(x, -_largura_a(x))
    for x in reversed(xs):
        p.lineTo(x, _largura_a(x))
    p.close()
    return uniao(p, path_maozinha(L - 4))


PATH_BRACO_A = _path_braco_a()


def braco_a(cv, a=1.0):
    """Manga da camiseta + braço + mãozinha (coordenadas do mundo)."""
    cv.save(); cv.translate(*SA); cv.rotate(ANG_A)
    cv.drawPath(PATH_BRACO_A, paint("#000000", int(70 * a), blur=14))
    _pele(cv, PATH_BRACO_A, (0, -70), (0, 70), a)
    manga = rr_path(-600, -90, 176, 90, 32)
    cv.drawPath(manga, paint("#000000", int(60 * a), blur=10))
    _pele(cv, manga, (0, -90), (0, 90), a, tons=TONS_CAMISA, cor_linha=CAMISA_LINHA)
    cv.drawLine(152, -82, 152, 82, paint(CAMISA_ESC, int(170 * a), "stroke", 3))
    cv.restore()


# ------------------------------------------------------------------ mão adulta (referencial: origem na mãozinha, +x = sentido da tração)
def mao_adulta_tras(cv, a, some=(330, 540)):
    """Antebraço com manga (some em degradê) e palma: fica ATRÁS da mãozinha."""
    cv.saveLayer(None, None)
    ante = rr_path(30, -46, 360, 46, 44)
    _pele(cv, ante, (0, -46), (0, 46), a, tons=TONS_AD, cor_linha=AD_LINHA)
    manga = rr_path(190, -60, 560, 60, 20)
    _pele(cv, manga, (0, -60), (0, 60), a, tons=TONS_PUNHO, cor_linha=PUNHO_ESC)
    cv.drawLine(204, -56, 204, 56, paint(PUNHO_CL, int(200 * a), "stroke", 4))
    desvanecer(cv, some[0], 0, some[1], 0)
    cv.restore()
    palma = rr_path(-36, -62, 100, 60, 46)
    _pele(cv, palma, (0, -62), (0, 60), a, tons=TONS_AD, cor_linha=AD_LINHA)


def mao_adulta_frente(cv, a):
    """Quatro dedos dobrados por cima da mãozinha + polegar (na frente dela)."""
    for i in range(4):
        x0 = -42 + i * 30
        d = rr_path(x0, -16, x0 + 32, 64, 16)
        _pele(cv, d, (x0, 0), (x0 + 32, 0), a, tons=TONS_AD, cor_linha=AD_LINHA, linha=2.5)
    pol = rr_path(-54, -76, 52, -40, 18)
    _pele(cv, pol, (0, -76), (0, -40), a, tons=TONS_AD, cor_linha=AD_LINHA, linha=2.5)


def maozinha_icone(cv, a, comp=250):
    """Mãozinha + um pedaço de antebraço que some em degradê (para os ícones)."""
    cv.saveLayer(None, None)
    ante = rr_path(-comp, -32, 0, 32, 32)
    _pele(cv, ante, (0, -32), (0, 32), a)
    desvanecer(cv, -comp * 0.45, 0, -comp, 0)
    cv.restore()
    m = path_maozinha(0, 0.86)
    _pele(cv, m, (0, -62), (0, 48), a)


def centro_icone(x, y, ang, esc, lx=40.0, ly=-50.0):
    """Centro visual do ícone de puxar (para o X), em coordenadas da tela."""
    r = math.radians(ang)
    return (x + esc * (lx * math.cos(r) - ly * math.sin(r)), y + esc * (lx * math.sin(r) + ly * math.cos(r)))


def icone_puxar(cv, x, y, ang, esc, a, cinza=0.0, crianca=True, seta_pr=1.0):
    """Ícone: mão adulta segurando (ou não) a mãozinha + seta dourada de tração."""
    if a <= 0:
        return
    camada(cv, a, cinza)
    cv.translate(x, y); cv.rotate(ang); cv.scale(esc, esc)
    mao_adulta_tras(cv, 1.0, some=(250, 420))
    if crianca:
        maozinha_icone(cv, 1.0, comp=200)
    mao_adulta_frente(cv, 1.0)
    if seta_pr > 0:
        seta(cv, -40, -140, lerp(-40, 300, e_out(seta_pr)), -140, OURO, 1.0, larg=11, tam=34)
    cv.restore()


# ------------------------------------------------------------------ parte A: câmera e tração
def puxada(t, T):
    """Deslocamento do braço ao longo do eixo na tração (UMA vez, suave, sem tranco)."""
    return 14 * e_inout(prog(t, T["puxao"] + 0.05, T["puxao"] + 0.75))


def cam_a(t, T, tA1):
    """(s, px, py): escala s em torno do pivô (px, py), que fica parado na tela. O pivô só anda
    devagar (pan contínuo): começa na mão, chega perto do cotovelo no nome, volta à mão no
    "foi na mão" e ao cotovelo no "lá no cotovelo"."""
    s = lerp(1.05, 1.0, e_inout(prog(t, T["mexer"] - 0.2, T["mexer"] + 1.4)))
    s = lerp(s, 1.045, e_inout(prog(t, T["cotovelo1"] - 0.1, T["mao2"] + 0.4)))
    s = lerp(s, 1.14, e_inout(prog(t, T["cotovelo2"] - 0.15, T["cotovelo2"] + 0.6)))   # push-in no cotovelo
    k = e_inout(prog(t, T["mexer"] + 0.6, T["cotovelo1"]))                       # mão -> cotovelo
    k = lerp(k, 0.0, e_inout(prog(t, T["mao2"] - 0.25, T["mao2"] + 0.45)))       # -> mão
    k = lerp(k, 1.0, e_inout(prog(t, T["cotovelo2"] - 0.15, T["cotovelo2"] + 0.4)))   # -> cotovelo
    px, py = lerp(HA[0], EA[0], k), lerp(HA[1], EA[1], k)
    s = lerp(s, 0.86, e_inout(prog(t, tA1 + 0.05, tA1 + 0.5)))
    return s, px, py


def na_tela(cam, x, y):
    s, px, py = cam
    return px + s * (x - px), py + s * (y - py)


def aplica(cv, cam):
    s, px, py = cam
    cv.translate(px, py); cv.scale(s, s); cv.translate(-px, -py)


# ------------------------------------------------------------------ parte A: balão do cotovelo
B_X, B_Y, B_R = 392.0, 604.0, 186.0
M_BALAO = 1.9
ESC_AD = 1.2                           # mão adulta na escala do braço em close


def _tangentes(c1, r1, c2, r2):
    d = math.hypot(c2[0] - c1[0], c2[1] - c1[1])
    if d <= abs(r2 - r1) + 2:
        return None
    phi = math.atan2(c2[1] - c1[1], c2[0] - c1[0])
    beta = math.acos(clamp((r1 - r2) / d, -1, 1))
    out = []
    for sg in (1, -1):
        g = phi + sg * beta
        out.append(((c1[0] + r1 * math.cos(g), c1[1] + r1 * math.sin(g)),
                    (c2[0] + r2 * math.cos(g), c2[1] + r2 * math.sin(g))))
    return out


def estado_tira(t, T):
    entra = e_back(prog(t, T["ligamento"], T["ligamento"] + 0.4))
    desl = 104 * e_inout(prog(t, T["escorrega"] + 0.05, T["escorrega"] + 0.75))       # devagar, e PARA
    verm = prog(t, T["escorrega"] + 0.3, T["escorrega"] + 0.8)
    return entra, desl, verm


def balao(cv, t, T, cam, tA1, off):
    abre = e_out(prog(t, T["cotovelo2"] + 0.2, T["cotovelo2"] + 0.7))
    fecha = e_inout(prog(t, tA1 - 0.05, tA1 + 0.3))
    k = abre * (1 - fecha)
    if k <= 0.01:
        return None
    ex, ey = na_tela(cam, EA[0] + off[0], EA[1] + off[1])
    r1 = 78 * cam[0]
    cx, cy = lerp(ex, B_X, k), lerp(ey, B_Y, k)
    r = lerp(r1, B_R, k)
    tg = _tangentes((ex, ey), r1, (cx, cy), r)
    if tg:
        (a1, b1), (a2, b2) = tg
        p = skia.Path(); p.moveTo(*a1); p.lineTo(*b1); p.lineTo(*b2); p.lineTo(*a2); p.close()
        cv.drawPath(p, paint("#FFFFFF", int(26 * k)))
        for (q0, q1) in tg:
            cv.drawLine(q0[0], q0[1], q1[0], q1[1], paint(OURO, int(150 * k), "stroke", 3))
    cv.drawCircle(cx, cy, r + 26, paint("#000000", int(90 * k), blur=18))
    # conteúdo: a região do cotovelo do PRÓPRIO desenho, ampliada (só o contorno de pele)
    cv.save()
    clip = skia.Path(); clip.addCircle(cx, cy, r)
    cv.clipPath(clip, skia.ClipOp.kIntersect, True)
    fundo(cv, t)
    mm = lerp(cam[0], M_BALAO, k)
    cv.translate(cx, cy); cv.scale(mm, mm); cv.translate(-(EA[0] + off[0]), -(EA[1] + off[1]))
    cv.translate(*off)
    braco_a(cv)
    cv.restore()
    # a tira: esquema puro, no centro do balão (sem anel, sem osso, sem posição anatômica)
    entra, desl, verm = estado_tira(t, T)
    sc = r / B_R
    pos = None
    a_tira = clamp(1 - fecha * 1.8)                                 # some antes de o balão fechar
    if entra > 0 and a_tira > 0:
        camada(cv, a_tira)
        cv.translate(cx, cy); cv.scale(sc, sc); cv.rotate(ANG_A)
        a_m = prog(t, T["ligamento"] + 0.2, T["ligamento"] + 0.45)
        marca = skia.RRect.MakeRectXY(skia.Rect(-76, -27, 76, 27), 22, 22)
        cv.drawRRect(marca, paint(LIG_ESC, int(70 * a_m)))                 # o lugar dela
        pm = paint("#FFFFFF", int(240 * a_m), "stroke", 3.5)
        pm.setPathEffect(skia.DashPathEffect.Make([13.0, 9.0], 0.0))
        cv.drawRRect(marca, pm)
        cv.save(); cv.translate(-desl, 0); cv.scale(entra, entra)
        tira = skia.RRect.MakeRectXY(skia.Rect(-66, -19, 66, 19), 19, 19)
        brilho = 1 - prog(t, T["ligamento"] + 0.3, T["ligamento"] + 1.0)
        if brilho > 0:
            cv.drawRRect(tira, paint(LIG_CL, int(200 * brilho), "stroke", 18, blur=12))
        sh = skia.GradientShader.MakeLinear([skia.Point(0, -19), skia.Point(0, 19)], [_c(LIG_CL), _c(LIG), _c(LIG_ESC)])
        cv.drawRRect(tira, paint(LIG, 255, shader=sh))
        cv.drawRRect(tira, paint(LIG_ESC, 255, "stroke", 3))
        if verm > 0:
            cv.drawRRect(tira, paint(VERMELHO, int(120 * verm), "stroke", 14, blur=8))
            cv.drawRRect(tira, paint(VERMELHO, int(235 * verm), "stroke", 5))
        cv.restore()
        cv.restore()
        pos = (cx - sc * desl * UA[0], cy - sc * desl * UA[1])
    # aro da lupa
    cv.drawCircle(cx, cy, r, paint("#000000", int(90 * k), "stroke", 24, blur=8))
    cv.drawCircle(cx, cy, r, paint(OURO, int(255 * k), "stroke", 12))
    cv.drawCircle(cx, cy, r - 9, paint("#FFF1C2", int(110 * k), "stroke", 2.5))
    cv.drawCircle(ex, ey, r1, paint(OURO, int(255 * k), "stroke", 6))
    return pos


def etiqueta_fio(cv, s, x, y, xa, ya, cor, a, tam=38):
    """Caixa alinhada pela esquerda em x (linha de base y) com fio até (xa, ya)."""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    x1 = x + lw + 30; ym = y - tam * 0.35
    xb = x1 if xa > x1 else x                                    # o fio sai do lado mais perto
    cv.drawLine(xb, ym, xa, ya, paint(FUNDO_CARTAO, int(150 * a), "stroke", 7))
    cv.drawLine(xb, ym, xa, ya, paint(cor, int(235 * a), "stroke", 3))
    cv.drawCircle(xa, ya, 8, paint(FUNDO_CARTAO, int(200 * a)))
    cv.drawCircle(xa, ya, 6, paint(cor, int(255 * a)))
    rr = skia.RRect.MakeRectXY(skia.Rect(x, y - tam * 1.05, x1, y + tam * 0.34), 14, 14)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(225 * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 3))
    cv.drawString(s, x + 15, y, f, paint(cor, int(255 * a)))


def arco_tracejado(cv, cx, cy, r, a0, a1, cor, a, pr):
    """Arco tracejado de movimento (ícone de dobrar), com ponta; ângulos em graus."""
    if a <= 0 or pr <= 0:
        return
    fim = lerp(a0, a1, pr)
    n = 9
    for i in range(n):
        g0 = lerp(a0, a1, i / n); g1 = lerp(a0, a1, (i + 0.6) / n)
        if (a1 > a0 and g0 >= fim) or (a1 < a0 and g0 <= fim):
            break
        g1 = min(g1, fim) if a1 > a0 else max(g1, fim)
        rect = skia.Rect(cx - r, cy - r, cx + r, cy + r)
        cv.drawArc(rect, g0, g1 - g0, False, paint(FUNDO_CARTAO, int(140 * a), "stroke", 13))
        cv.drawArc(rect, g0, g1 - g0, False, paint(cor, int(255 * a), "stroke", 7))
    g = math.radians(fim)
    tang = g + (math.pi / 2 if a1 > a0 else -math.pi / 2)
    ponta(cv, cx + r * math.cos(g), cy + r * math.sin(g), tang, 24, cor, a)


def cena_a(cv, t, T, tA1):
    a_mundo = 1 - prog(t, tA1 + 0.1, tA1 + 0.42)
    if a_mundo <= 0:
        return
    cam = cam_a(t, T, tA1)
    pux = puxada(t, T)
    off = (UA[0] * pux, UA[1] * pux)
    sai = e_inout(prog(t, T["mexer"] - 0.05, T["mexer"] + 0.6))           # a mão adulta vai embora (sem tranco)
    a_ad = 1 - prog(t, T["mexer"] + 0.2, T["mexer"] + 0.55)
    camada(cv, a_mundo)                                            # tudo da parte A some junto na troca
    cv.save()
    aplica(cv, cam)
    cv.save(); cv.translate(*off)
    hx, hy = HA[0] + UA[0] * 420 * sai, HA[1] + UA[1] * 420 * sai
    if a_ad > 0:
        cv.save(); cv.translate(hx, hy); cv.rotate(ANG_A); cv.scale(ESC_AD, ESC_AD)
        camada(cv, a_ad); mao_adulta_tras(cv, 1.0); cv.restore()
        cv.restore()
    braco_a(cv)
    if a_ad > 0:
        cv.save(); cv.translate(hx, hy); cv.rotate(ANG_A); cv.scale(ESC_AD, ESC_AD)
        camada(cv, a_ad); mao_adulta_frente(cv, 1.0); cv.restore()
        cv.restore()
    cv.restore()
    cv.restore()

    # seta de tração: estica UMA vez (sem tremor) e sai com a mão adulta
    pr = e_out(prog(t, T["puxao"], T["puxao"] + 0.6))
    a_s = prog(t, T["puxao"], T["puxao"] + 0.1) * a_ad * a_mundo
    if pr > 0 and a_s > 0:
        p0 = pa(0.6, 180); p1 = (HA[0] + UA[0] * 150 + NA[0] * 180, HA[1] + UA[1] * 150 + NA[1] * 180)
        x0, y0 = na_tela(cam, p0[0] + off[0], p0[1] + off[1])
        x1, y1 = na_tela(cam, p1[0] + off[0], p1[1] + off[1])
        seta(cv, x0, y0, lerp(x0, x1, pr), lerp(y0, y1, pr), OURO, a_s, larg=11, tam=36)

    ex, ey = na_tela(cam, EA[0] + off[0], EA[1] + off[1])
    hxs, hys = na_tela(cam, HA[0] + UA[0] * 22 + off[0], HA[1] + UA[1] * 22 + off[1])
    # não quer mexer: arco tracejado cinza junto ao cotovelo, aparece e se apaga
    # (tenta e volta: chega a ~40 graus e recolhe — nunca vira instrução de "dobre o braço")
    a_arco = prog(t, T["mexer"], T["mexer"] + 0.15) * (1 - prog(t, T["mexer"] + 1.1, T["mexer"] + 1.5)) * a_mundo
    pr_arco = e_out(prog(t, T["mexer"], T["mexer"] + 0.45)) * 0.5 * (1 - e_inout(prog(t, T["mexer"] + 0.8, T["mexer"] + 1.4)))
    arco_tracejado(cv, ex, ey, 175 * cam[0], ANG_A - 12, ANG_A - 92, CINZA, a_arco, pr_arco)
    # cotovelo de babá: brilho dourado curto no cotovelo
    k = t - T["baba"]
    if 0 <= k < 1.1:
        a_g = math.sin(math.pi * k / 1.1) * a_mundo
        cv.drawCircle(ex, ey, 100, paint(OURO, int(150 * a_g), blur=30))
        cv.drawCircle(ex, ey, 70, paint("#FFE7A6", int(90 * a_g), blur=14))
    brilhos(cv, ex, ey, t, T["baba"] + 0.05, n=12, raio=150)
    # foi na mão: anel dourado pulsa na mãozinha e depois viaja até o cotovelo
    a_anel = prog(t, T["mao2"], T["mao2"] + 0.2) * (1 - prog(t, T["cotovelo2"] + 0.3, T["cotovelo2"] + 0.45)) * a_mundo
    if a_anel > 0:
        via = e_inout(prog(t, T["cotovelo2"] - 0.15, T["cotovelo2"] + 0.35))
        xr, yr = lerp(hxs, ex, via), lerp(hys, ey, via)
        rr = lerp(104, 78, via) * cam[0]
        pul = 1 + 0.08 * math.sin(max(0.0, t - T["mao2"]) * 9) * (1 - via)
        cv.drawCircle(xr, yr, rr * pul + 6, paint(OURO, int(90 * a_anel), "stroke", 16, blur=8))
        cv.drawCircle(xr, yr, rr * pul, paint(OURO, int(255 * a_anel), "stroke", 6))
    pos = balao(cv, t, T, cam, tA1, off)

    # rótulos da parte A
    chip(cv, R_PUXAO, 540, R1, "#FFFFFF", janela(t, T["puxao"] + 0.15, T["mexer"] - 0.2, 0.25, 0.2), borda=OURO)
    chip(cv, R_MEXER, 540, R1, CINZA, janela(t, T["mexer"], T["cotovelo1"] - 0.4, 0.2, 0.3), borda=CINZA)
    chip(cv, R_NAMAO, 540, R1, OURO, janela(t, T["mao2"], T["cotovelo2"] - 0.2, 0.2, 0.2))
    chip(cv, R_NOCOT, 540, R1, OURO, janela(t, T["cotovelo2"], T["escorrega"] - 0.25, 0.2, 0.2))
    if pos is not None:
        a_l = janela(t, T["ligamento"] + 0.1, tA1 - 0.1, 0.25, 0.2)
        etiqueta_fio(cv, R_LIG, 622, 560, pos[0], pos[1], LIG_CL, a_l, tam=40)
    carimbo_opaco(cv, R_ESC, 540, R1 + 6, -4, T["escorrega"], t, dur=tA1 + 0.3 - T["escorrega"], tam=58)
    cv.restore()


def titulo(cv, t, T, tA1):
    a = prog(t, T["cotovelo1"], T["cotovelo1"] + 0.2) * (1 - prog(t, tA1 - 0.1, tA1 + 0.2))
    e_t = e_back(prog(t, T["cotovelo1"], T["cotovelo1"] + 0.35))
    if a > 0 and e_t > 0:
        cv.save(); cv.translate(540, 300); cv.scale(e_t, e_t); cv.translate(-540, -300)
        chip(cv, R_TITULO, 540, 318, OURO, clamp(a), tam=50)
        cv.restore()
    a2 = prog(t, T["pronacao"], T["pronacao"] + 0.3) * (1 - prog(t, tA1 - 0.1, tA1 + 0.2))
    if a2 > 0:
        texto(cv, R_SUB, 540, 386 + 14 * (1 - e_out(prog(t, T["pronacao"], T["pronacao"] + 0.4))), F_SEMI, 36,
              AZUL, int(255 * a2), contorno=6)


# ------------------------------------------------------------------ partes B e C: a criança de desenho (de frente)
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


def manga(cv, x0, y0, x1, y1, larg, frac=0.32, a=1.0):
    """Manga curta da camiseta: cobre o começo do braço (de (x0, y0) em direção a (x1, y1))."""
    ang = math.degrees(math.atan2(y1 - y0, x1 - x0)) - 90
    L = math.hypot(x1 - x0, y1 - y0) * frac
    cv.save(); cv.translate(x0, y0); cv.rotate(ang)
    w0, w1 = larg * 0.42, larg * 0.56
    p = skia.Path()
    p.moveTo(-w0, 0); p.cubicTo(-w0, -larg * 0.55, w0, -larg * 0.55, w0, 0)
    p.lineTo(w1, L - 7); p.quadTo(w1, L, w1 - 7, L); p.lineTo(-w1 + 7, L); p.quadTo(-w1, L, -w1, L - 7)
    p.close()
    _pele(cv, p, (-w1 - 2, 0), (w1 + 2, 0), a, tons=TONS_CAMISA, linha=2.6, cor_linha=CAMISA_LINHA)
    cv.drawLine(-w1 + 7, L - 8, w1 - 7, L - 8, paint(CAMISA_ESC, int(150 * a), "stroke", 3))
    cv.restore()


OMBRO_X, OMBRO_Y = 80.0, -462.0


def braco_pts(lado, pose):
    """lado -1 = esquerda da tela; +1 = direita (o braço do puxão). pose 0 = em pé; 1 = erguida.
    Ângulos a partir da vertical para baixo, positivos para fora."""
    if lado < 0:
        au, af = lerp(9, 128, pose), lerp(-3, 152, pose)
    else:
        au, af = lerp(2.5, 128, pose), lerp(2.5, 152, pose)
    ox, oy = OMBRO_X * lado, OMBRO_Y
    ru, rf = math.radians(au), math.radians(af)
    ex, ey = ox + lado * 124 * math.sin(ru), oy + 124 * math.cos(ru)
    wx, wy = ex + lado * 112 * math.sin(rf), ey + 112 * math.cos(rf)
    return (ox, oy), (ex, ey), (wx, wy)


def crianca_corpo(cv, roupa=ROUPA_B):
    """Pernas, shorts, camiseta, cabeça (rosto sem detalhe). Origem = chão, entre os pés."""
    r = roupa
    for s in (-1, 1):
        perna = rr_path(s * 38 - 27, -236, s * 38 + 27, -22, 27)
        _pele(cv, perna, (s * 38 - 31, 0), (s * 38 + 31, 0), 1.0, linha=2.6)
        pe = oval_path(s * 46 - 35, -34, s * 46 + 35, 4)
        _pele(cv, pe, (s * 46 - 35, 0), (s * 46 + 35, 0), 1.0, linha=2.6)
    sh = skia.Path()
    sh.moveTo(-86, -306); sh.lineTo(86, -306)
    sh.cubicTo(94, -270, 98, -232, 92, -200)
    sh.lineTo(12, -200); sh.lineTo(0, -222); sh.lineTo(-12, -200); sh.lineTo(-92, -200)
    sh.cubicTo(-98, -232, -94, -270, -86, -306); sh.close()
    cv.drawPath(sh, paint("#000000", 60, blur=8))
    cv.drawPath(sh, paint(r["short"]))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-88, -310, 88, -286), 12, 12), paint(r["short_cl"]))
    tr = skia.Path()
    tr.moveTo(-84, -290)
    tr.cubicTo(-90, -350, -94, -410, -92, -440)
    tr.cubicTo(-90, -470, -66, -486, -36, -488)
    tr.lineTo(36, -488)
    tr.cubicTo(66, -486, 90, -470, 92, -440)
    tr.cubicTo(94, -410, 90, -350, 84, -290)
    tr.close()
    cv.drawPath(tr, paint("#000000", 60, blur=10))
    _pele(cv, tr, (-96, 0), (96, 0), 1.0, tons=r["camisa"], cor_linha=r["camisa_linha"])
    pesc = rr_path(-18, -512, 18, -478, 12)
    _pele(cv, pesc, (-20, 0), (20, 0), 1.0, linha=2.4)
    cv.drawArc(skia.Rect(-30, -500, 30, -470), 20, 140, False, paint(r["camisa_esc"], 200, "stroke", 4))   # gola
    if r["chiquinhas"]:                                          # dois rabinhos (atrás da cabeça)
        for s in (-1, 1):
            cv.drawOval(skia.Rect(s * 92 - 22, -632, s * 92 + 22, -582), paint(r["cabelo"]))
            cv.drawOval(skia.Rect(s * 92 - 22, -632, s * 92 + 22, -582), paint("#000000", 60, "stroke", 2.5))
    for s in (-1, 1):
        orl = oval_path(s * 70 - 11, -588, s * 70 + 11, -556)
        _pele(cv, orl, (s * 70 - 12, 0), (s * 70 + 12, 0), 1.0, linha=2.2)
    cab = skia.Path(); cab.addCircle(0, -574, 72)
    cv.drawCircle(3, -568, 74, paint("#000000", 50, blur=8))
    _pele(cv, cab, (-74, 0), (74, 0), 1.0)
    cv.save(); cv.clipPath(cab, skia.ClipOp.kIntersect, True)
    cv.drawOval(skia.Rect(-96, -676, 96, -578), paint(r["cabelo"]))
    if r["chiquinhas"]:                                          # franja reta (outro corte de cabelo)
        cv.drawRect(skia.Rect(-80, -640, 80, -596), paint(r["cabelo"]))
    else:
        cv.drawOval(skia.Rect(-80, -604, -30, -570), paint(r["cabelo"]))
        cv.drawOval(skia.Rect(26, -606, 84, -574), paint(r["cabelo"]))
    cv.restore()


def path_braco(lado, pose):
    (ox, oy), (ex, ey), (wx, wy) = braco_pts(lado, pose)
    return uniao(tubo_path(ox, oy, ex, ey, 46), tubo_path(ex, ey, wx, wy, 42, mao=25))


def crianca_braco(cv, lado, pose, com_manga=True):
    """Braço num contorno só (braço + antebraço + mão unidos): nenhuma linha no cotovelo."""
    (ox, oy), (ex, ey), (wx, wy) = braco_pts(lado, pose)
    p = path_braco(lado, pose)
    L = math.hypot(ex - ox, ey - oy); nx, ny = -(ey - oy) / L, (ex - ox) / L
    cv.drawPath(p, paint("#000000", 50, blur=8))
    _pele(cv, p, (ox - nx * 27, oy - ny * 27), (ox + nx * 27, oy + ny * 27), 1.0, linha=2.6)
    if com_manga:
        manga(cv, ox, oy, ex, ey, 58, frac=0.42)


def maos_axilas(cv, k, a=1.0):
    """Duas mãos adultas por baixo dos braços, segurando nas laterais do tronco (polegar na frente)."""
    if k <= 0 or a <= 0:
        return
    for s in (-1, 1):
        hx, hy = s * 92, -398
        d = math.radians(64)
        ux, uy = s * math.cos(d), math.sin(d)                      # do pulso para fora (manga), para baixo
        ent = (1 - e_out(k)) * 380
        cx, cy = hx + ux * ent, hy + uy * ent
        ang = math.degrees(math.atan2(uy, ux))
        camada(cv, a * clamp(k * 3))
        cv.translate(cx, cy); cv.rotate(ang)
        cv.saveLayer(None, None)
        ante = rr_path(20, -38, 340, 38, 38)
        _pele(cv, ante, (0, -38), (0, 38), 1.0, tons=TONS_AD, cor_linha=AD_LINHA)
        mg = rr_path(170, -50, 480, 50, 18)
        _pele(cv, mg, (0, -50), (0, 50), 1.0, tons=TONS_PUNHO, cor_linha=PUNHO_ESC)
        cv.drawLine(184, -46, 184, 46, paint(PUNHO_CL, 200, "stroke", 4))
        desvanecer(cv, 290, 0, 450, 0)
        cv.restore()
        palma = rr_path(-46, -46, 54, 46, 42)
        _pele(cv, palma, (0, -46), (0, 46), 1.0, tons=TONS_AD, cor_linha=AD_LINHA)
        cv.restore()
        # polegar na frente do tronco, apontando para cima e para o meio
        camada(cv, a * clamp(k * 3))
        cv.translate(cx - hx, cy - hy)
        pol = tubo_path(s * 74, -424, s * 46, -458, 30)
        _pele(cv, pol, (s * 72 - 18, 0), (s * 72 + 18, 0), 1.0, tons=TONS_AD, cor_linha=AD_LINHA, linha=2.4)
        cv.restore()


# posições da criança: B (em pé, perto) -> C (prevenção, coluna da esquerda)
B_POS = (440.0, 1090.0, 0.97)          # a criança do braço esticado (x, chão, escala)
C_POS = (290.0, 1000.0, 0.74)          # a criança da prevenção (OUTRA cena: nada "volta ao lugar")
ERGUE = 70.0
POSE_C = 0.8                           # braços abertos para cima, sem pose de 'vitória'


def sombra(cv, x, y, e, sobe=0.0):
    cv.drawOval(skia.Rect(x - 130 * e * (1 - 0.3 * sobe), y - 16 * e, x + 130 * e * (1 - 0.3 * sobe), y + 18 * e),
                paint("#000000", int(80 * (1 - 0.45 * sobe)), blur=10))


def foco_b(t, T):
    """De "esticado" até a lupa sair: o resto da criança afunda no fundo e o braço do puxão fica em foco."""
    return e_inout(prog(t, T["esticado"] - 0.05, T["esticado"] + 0.4)) * (1 - e_inout(prog(t, T["puxe"] - 0.3, T["puxe"] + 0.2)))


TINTA = "#17384C"                      # cor do fundo: o que sai de foco "afunda" nele (opaco, nada translúcido)


def tingido(cv, desenho, k):
    """Desenha numa camada e mistura (opaco) com a cor do fundo na proporção k: tira de foco sem
    escurecer a pele para outro tom e sem deixar ver uma peça através da outra."""
    if k <= 0:
        desenho(); return
    cv.saveLayer(None, None)
    desenho()
    p = paint(TINTA, int(255 * clamp(k))); p.setBlendMode(skia.BlendMode.kSrcATop)
    cv.drawRect(skia.Rect(-3000, -3000, 3000, 3000), p)
    cv.restore()


def mundo_b(cv, t, T, tA1):
    """A criança de pé, com o braço do puxão esticado junto ao corpo (parte B). De "esticado" até a
    lupa sair, o resto da criança afunda no fundo e só o braço do puxão fica em cor."""
    x, y, e = B_POS
    glow = prog(t, T["esticado"], T["esticado"] + 0.3) * (1 - prog(t, T["sem"] - 0.3, T["sem"]))
    k = 0.42 * foco_b(t, T)
    sombra(cv, x, y, e)
    cv.save(); cv.translate(x, y); cv.scale(e, e)

    def corpo():
        crianca_corpo(cv, ROUPA_B)
        crianca_braco(cv, -1, 0.0)
    tingido(cv, corpo, k)
    if glow > 0:                                  # brilho só por FORA do braço: não mancha camiseta nem short
        cv.save(); cv.clipRect(skia.Rect(88, -2000, 2000, 2000))
        cv.drawPath(path_braco(1, 0.0), paint(OURO, int(185 * glow), "stroke", 34, blur=16))
        cv.restore()
    crianca_braco(cv, 1, 0.0, com_manga=False)                    # a pele do braço do puxão: sempre em cor
    (ox, oy), (ex, ey), _ = braco_pts(1, 0.0)
    tingido(cv, lambda: manga(cv, ox, oy, ex, ey, 58, frac=0.42), k)   # a manga é da camiseta
    cv.restore()


def no_mundo_b(t, T, lx, ly):
    x, y, e = B_POS
    return x + lx * e, y + ly * e


def pos_c(t, T):
    ergue = ERGUE * e_inout(prog(t, T["axilas"] - 0.1, T["axilas"] + 0.6))
    return C_POS[0], C_POS[1] - ergue, C_POS[2], ergue / ERGUE


def mundo_c(cv, t, T):
    """Prevenção: a criança erguida por duas mãos adultas por baixo dos braços."""
    x, y, e, sobe = pos_c(t, T)
    sombra(cv, x, C_POS[1], e, sobe)
    cv.save(); cv.translate(x, y); cv.scale(e, e)
    crianca_braco(cv, -1, POSE_C, com_manga=False)                  # braços erguidos, atrás da camiseta
    crianca_braco(cv, 1, POSE_C, com_manga=False)
    crianca_corpo(cv, ROUPA_C)                                    # OUTRA criança: outra roupa e cabelo
    maos_axilas(cv, prog(t, T["levantar"] - 0.04, T["levantar"] + 0.5))           # as mãos chegam junto com a criança
    cv.restore()


def no_mundo_c(t, T, lx, ly):
    x, y, e, _ = pos_c(t, T)
    return x + lx * e, y + ly * e


def lupa(cv, t, T, tA1):
    """Lupa pequena sobre o cotovelo do braço esticado: só aumenta o próprio desenho."""
    t0 = T["inchaco"] - 0.05
    if t < t0:
        return
    a = 1 - prog(t, T["puxe"] - 0.25, T["puxe"] + 0.1)
    if a <= 0:
        return
    _, (lx, ly), _ = braco_pts(1, 0.0)
    gx, gy = no_mundo_b(t, T, lx, ly)
    k1 = e_inout(prog(t, t0, t0 + 0.45))
    x = lerp(W + 160, gx + 6, k1) + 3 * math.sin(t * 1.7)
    y = lerp(gy - 40, gy, k1) + 3 * math.cos(t * 1.3)
    r, m = 112, 1.8
    camada(cv, a)
    cv.save()
    clip = skia.Path(); clip.addCircle(x, y, r)
    cv.clipPath(clip, skia.ClipOp.kIntersect, True)
    fundo(cv, t)
    cv.translate(x, y); cv.scale(m, m); cv.translate(-x, -y)
    cv.translate(x - (gx + 6), y - gy)
    mundo_b(cv, t, T, tA1)
    cv.restore()
    cv.drawCircle(x, y, r, paint("#FFFFFF", 22))
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


def cena_bc(cv, t, T, tA1, fim):
    a_in = prog(t, tA1 + 0.3, tA1 + 0.62)
    if a_in <= 0:
        return
    esc_in = lerp(0.94, 1.0, e_out(prog(t, tA1 + 0.3, tA1 + 0.9)))
    dim = lerp(1.0, 0.75, prog(t, T["manda"] - 0.4, T["manda"]))
    a_b = a_in * (1 - prog(t, T["levantar"] - 0.38, T["levantar"] - 0.06))
    if a_b > 0:
        esc_out = lerp(1.0, 0.94, e_inout(prog(t, T["levantar"] - 0.38, T["levantar"] - 0.06)))
        camada(cv, a_b)
        cv.translate(540, 760); cv.scale(esc_in * esc_out, esc_in * esc_out); cv.translate(-540, -760)
        mundo_b(cv, t, T, tA1)
        cv.restore()
    a_c = prog(t, T["levantar"] - 0.04, T["levantar"] + 0.28) * dim
    if a_c > 0:
        esc_c = lerp(0.92, 1.0, e_out(prog(t, T["levantar"] - 0.04, T["levantar"] + 0.45)))
        camada(cv, a_c)
        cv.translate(C_POS[0], C_POS[1]); cv.scale(esc_c, esc_c); cv.translate(-C_POS[0], -C_POS[1])
        mundo_c(cv, t, T)
        cv.restore()

    # braço esticado: régua tracejada reta ao lado do braço (sai quando entra "ao lado do corpo")
    (ox, oy), _, (wx, wy) = braco_pts(1, 0.0)
    a_r = prog(t, T["esticado"] + 0.1, T["esticado"] + 0.3) * (1 - prog(t, T["lado"] - 0.2, T["lado"] + 0.05))
    if a_r > 0:
        x0, y0 = no_mundo_b(t, T, ox + 60, oy + 24); x1, y1 = no_mundo_b(t, T, wx + 60, wy + 40)
        pr = e_out(prog(t, T["esticado"] + 0.1, T["esticado"] + 0.6))
        pm = paint(OURO, int(255 * a_r), "stroke", 5)
        pm.setPathEffect(skia.DashPathEffect.Make([16.0, 11.0], 0.0))
        cv.drawLine(x0, y0, lerp(x0, x1, pr), lerp(y0, y1, pr), pm)
    # ao lado do corpo: um laço tracejado abraça braço e tronco juntos
    a_f = prog(t, T["lado"], T["lado"] + 0.2) * (1 - prog(t, T["sem"] - 0.3, T["sem"] - 0.05))
    if a_f > 0:
        k = e_back(prog(t, T["lado"], T["lado"] + 0.4))
        x0, y0 = no_mundo_b(t, T, 14, -436); x1, y1 = no_mundo_b(t, T, 142, -286)
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        esc = lerp(1.25, 1.0, k)
        cv.save(); cv.translate(mx, my); cv.scale(esc, esc); cv.translate(-mx, -my)
        rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 52, 52)
        cv.drawRRect(rr, paint(FUNDO_CARTAO, int(170 * a_f), "stroke", 13))
        pm = paint(OURO, int(255 * a_f), "stroke", 7)
        pm.setPathEffect(skia.DashPathEffect.Make([18.0, 11.0], 0.0))
        cv.drawRRect(rr, pm)
        cv.restore()
    lupa(cv, t, T, tA1)

    # não puxe nem force: a mão adulta volta (pouco apagada), com a seta, e leva um X
    a_g = prog(t, T["puxe"] - 0.05, T["puxe"] + 0.3) * (1 - prog(t, T["levantar"] - 0.38, T["levantar"] - 0.06))
    a_g *= lerp(1.0, 0.45, prog(t, T["procure"] - 0.2, T["procure"] + 0.2))      # sai de foco: vez da avaliação
    if a_g > 0:
        dx = 60 * (1 - e_out(prog(t, T["puxe"] - 0.05, T["puxe"] + 0.4)))
        ix, iy, ia, ie = 770 + dx, 790, -35, 0.8
        icone_puxar(cv, ix, iy, ia, ie, 0.85 * a_g, cinza=0.1, crianca=True,
                    seta_pr=prog(t, T["puxe"], T["puxe"] + 0.5))
        xc, yc = centro_icone(ix, iy, ia, ie)
        xis(cv, xc, yc, 84, e_out(prog(t, T["puxe"] + 0.45, T["puxe"] + 0.75)), a_g)

    # procure avaliação + a correção é com o ortopedista (prancheta no canto)
    a_av = prog(t, T["avaliacao"] - 0.15, T["avaliacao"] + 0.15) * (1 - prog(t, T["levantar"] - 0.3, T["levantar"]))
    ent = e_back(prog(t, T["avaliacao"] - 0.15, T["avaliacao"] + 0.3))
    prancheta(cv, 62, 232 - 40 * (1 - ent), a_av, t, T["avaliacao"])
    chip_esq(cv, R_AVAL, 172, 306, "#FFFFFF", a_av, tam=40, borda=OURO)
    chip_esq(cv, R_ORTO, 62, 416, OURO,
             prog(t, T["ortopedista"], T["ortopedista"] + 0.2) * (1 - prog(t, T["levantar"] - 0.3, T["levantar"])), tam=38)

    # rótulos da parte B (linha de baixo): cada um sai antes da frase seguinte
    chip(cv, R_ESTIC, 540, R1, OURO, janela(t, T["esticado"], T["sem"] - 0.3, 0.2, 0.25))
    chip(cv, R_LADO, 540, R2, "#FFFFFF", janela(t, T["ao"], T["sem"] - 0.3, 0.2, 0.25), tam=38, borda=OURO)
    chip(cv, R_INCH, 540, R1, "#FFFFFF", janela(t, T["sem"] - 0.05, T["puxe"] - 0.25, 0.2, 0.25), borda=OURO)
    chip(cv, R_PUXE, 540, R1, "#FFFFFF", janela(t, T["puxe"], T["procure"] - 0.3, 0.2, 0.25), borda=VERMELHO)

    # ---------------- parte C: prevenção
    cena_c(cv, t, T, fim)


def cena_c(cv, t, T, fim):
    # seta dourada para cima (acima da cabeça) e check verde: a orientação
    a_up = prog(t, T["axilas"], T["axilas"] + 0.2) * fim
    if a_up > 0:
        hx, hy = no_mundo_c(t, T, 0, -670)
        pr = e_out(prog(t, T["axilas"], T["axilas"] + 0.6))
        seta(cv, hx, hy, hx, hy - 130 * pr, OURO, a_up, larg=12, tam=38)
    # o check é da ORIENTAÇÃO (fica no rótulo "PELAS AXILAS"), nunca no braço erguido
    selo_check(cv, C_POS[0] + 205, 1060, 30, prog(t, T["axilas"] + 0.35, T["axilas"] + 0.75), fim)
    chip(cv, R_AXI, C_POS[0], 1074, "#FFFFFF", prog(t, T["axilas"], T["axilas"] + 0.25) * fim, tam=40, borda=VERDE)

    # ao lado: mão adulta segurando a mãozinha, seta para cima, X vermelho
    k = prog(t, T["maos"] - 0.1, T["maos"] + 0.35)
    if k > 0:
        dim = lerp(1.0, 0.75, prog(t, T["manda"] - 0.4, T["manda"]))
        dx = 120 * (1 - e_out(k))
        ix, iy, ia, ie = 812 + dx, 800, -90, 0.62
        icone_puxar(cv, ix, iy, ia, ie, clamp(k * 2) * dim * fim, crianca=True,     # some antes da CTA
                    seta_pr=prog(t, T["maos"] + 0.05, T["maos"] + 0.5))
        xc, yc = centro_icone(ix, iy, ia, ie)
        xis(cv, xc, yc, 92, e_out(prog(t, T["pulsos"], T["pulsos"] + 0.3)), clamp(k * 2) * dim * fim)
    a_c = prog(t, T["maos"], T["maos"] + 0.25) * fim
    if a_c > 0:
        x0, x1, y0, y1 = 576, 1004, 1004, 1112
        rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 16, 16)
        cv.drawRRect(rr, paint(FUNDO_CARTAO, int(225 * a_c)))
        cv.drawRRect(rr, paint(VERMELHO, int(255 * a_c), "stroke", 3))
        texto(cv, R_MAOS1, (x0 + x1) / 2, y0 + 48, F_BLACK, 40, "#FFFFFF", int(255 * a_c))
        texto(cv, R_MAOS2, (x0 + x1) / 2, y0 + 94, F_BLACK, 40, "#FFFFFF", int(255 * a_c))

    # selo sóbrio: assenta, sem brilho
    k = prog(t, T["prevenir"], T["prevenir"] + 0.35)
    chip(cv, R_PREV, 540, R2 - 4, AZUL, clamp(k * 2) * fim, tam=40, borda=AZUL, esc=lerp(1.12, 1.0, e_out(k)))


# ------------------------------------------------------------------ quadro
def t_troca(T):
    """Fecha o balão e troca o braço em close pela criança inteira ("O braço fica esticado")."""
    return T["braco2"] + 0.2


def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    tA1 = t_troca(T)                                         # troca: braço em close -> criança inteira
    fim = 1 - prog(t, T["manda"] - 0.45, T["manda"] - 0.1)   # a CTA fica limpa de rótulos

    if t < tA1 + 0.7:
        cena_a(cv, t, T, tA1)
        titulo(cv, t, T, tA1)
    if t >= tA1:
        cena_bc(cv, t, T, tA1, fim)

    capa(cv, t, T["tem"], ep["gancho"][0], ep["gancho"][1])
    selo_como_funciona(cv, prog(t, T["tem"] + 0.35, T["tem"] + 0.7) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface(cv, t, T, blocos, DESTAQUE)


def sons(T):
    tA1 = t_troca(T)
    return [(T["puxao"] + 0.02, "whoosh", 0.45), (T["puxao"] + 0.18, "pop", 0.35),
            (T["mexer"] - 0.05, "whoosh", 0.35), (T["mexer"] + 0.1, "pop", 0.25),
            (T["cotovelo1"] + 0.02, "pop", 0.5), (T["baba"] + 0.05, "shimmer", 0.45),
            (T["pronacao"] + 0.02, "pop", 0.35),
            (T["mao2"] + 0.02, "ping", 0.5),
            (T["cotovelo2"] - 0.1, "whoosh", 0.4), (T["cotovelo2"] + 0.35, "pop", 0.5),
            (T["ligamento"] + 0.02, "ping", 0.5), (T["ligamento"] + 0.12, "shimmer", 0.3),
            (T["escorrega"] + 0.02, "whoosh", 0.4), (T["escorrega"], "pop", 0.3),      # deslize leve, sem estalo
            (tA1, "whoosh", 0.45), (T["esticado"] + 0.02, "ping", 0.5), (T["lado"] + 0.02, "pop", 0.45),
            (T["inchaco"] - 0.1, "whoosh", 0.4), (T["inchaco"] + 0.35, "pop", 0.35),
            (T["puxe"] - 0.02, "pop", 0.45), (T["puxe"] + 0.45, "thump", 0.6),
            (T["avaliacao"] - 0.12, "pop", 0.5), (T["ortopedista"] + 0.02, "pop", 0.45),
            (T["levantar"] - 0.02, "whoosh", 0.45), (T["axilas"] - 0.05, "whoosh", 0.35), (T["axilas"] + 0.4, "ding", 0.5),
            (T["maos"] - 0.05, "pop", 0.45), (T["pulsos"] + 0.02, "thump", 0.6),
            (T["prevenir"] + 0.02, "pop", 0.5), (T["manda"] + 0.05, "whoosh", 0.5)]


def tempos_previa(T):
    return (0.0, T["puxao"] + 0.9, T["mexer"] + 0.7, T["pronacao"] + 0.6, T["ligamento"] + 0.45,
            T["escorrega"] + 0.9, T["lado"] + 0.6, T["inchaco"] + 0.8, T["puxe"] + 0.9,
            T["ortopedista"] + 0.6, T["prevenir"] + 0.9, T["manda"] + 1.2)


# respiro antes da CTA: o selo "AJUDA A PREVENIR" e a cena de prevenção ficam ~2 s na tela
render = fazer_render(quadro, ANCORAS, sons, tempos_previa, respiro_cta=2.0)
