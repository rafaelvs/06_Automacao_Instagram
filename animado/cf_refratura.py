# -*- coding: utf-8 -*-
"""COMO FUNCIONA — "Quebrou de novo no mesmo lugar?" (refratura: investigar a causa antes de tratar igual).

Mesmo estilo e mesmas peças das cenas aprovadas (osso marfim com a geometria do cf_fratura_cola,
linha de fratura em zigue-zague plano, rótulo com linha-guia, carimbo ouro, prancheta-checklist,
legenda karaokê, CTA com aviãozinho). Storyboard e correções do verificador
(lote5_cf/cf_refratura_storyboard.json) respeitados aqui:
  * A marca da fratura anterior é uma FAIXA dourada chapada na largura da diáfise: sem saliência,
    sem formato de calo, sem brilho e sem rótulo. A linha nova cruza o osso EXATAMENTE sobre ela.
  * A linha nova é o zigue-zague do cf_fratura_cola em traço fino e escuro; as metades se afastam
    só alguns pixels (sem vão grande, sem sangue, tremor mínimo, som seco e discreto).
  * Nenhum exame simulado: a lupa amplia o MESMO osso esquemático, sobre vidro azul.
  * "Três POSSÍVEIS causas" (não "suspeitos"); fatores do paciente com ícone neutro de pessoa, sem
    vermelho, sem X, sem dedo apontado. Esporte = bola e relógio, sem pessoa caindo.
  * Tratamento = placas de caminho só com os nomes (nenhuma técnica desenhada); o fixador externo
    é uma miniatura do anel do cf_alongamento. O osso CONTINUA com a linha nova até o fim (nada de
    antes e depois).
Desvio consciente do storyboard: a linha nova aparece em "Quebrou" (1ª palavra, ~0,4 s) e não em
"lugar" (~2 s) — a 1ª coisa que se mexe tem de ser o espanto (cf_alongamento corta o osso na 1ª
palavra). Em "lugar" entram o rótulo MESMO LUGAR, a seta e o círculo tracejado no ponto.
Correções da revisão: racha em traço de 6 px com lampejo quente ATRÁS do osso (só vaza pela racha)
e empurrão curto da câmera; a lupa atravessa a linha, volta e está parada quando o carimbo bate;
o cartão REFRATURA fica até "causas" e aponta para a lupa sobre a linha; o 3º item acende em
"momento" (a seta desce em "carga"); MESMO LUGAR do desfecho cai em "mesmo" e a prancheta só recolhe
depois de "tratamento"; mini fixador = dois anéis e duas hastes; na CTA o poste e as placas saem
inteiros e fica só o osso com a linha, de volta ao centro (nada de texto atrás do texto).
Cena PRESA ao roteiro pelas palavras-âncora: roteiro sem elas = KeyError, não vídeo torto.
"""
import math

import skia

from .cf_alongamento import (ACO, ACO_ESC, ACO_HL, CX, F_BLACK, F_SEMI, HASTE, NOVO, OSSO_C, OSSO_L, OURO, W, Y_BASE,
                             Y_TOPO, brilhos, clamp, e_back, e_inout, e_out, fundo, lerp, lerpc, paint, path_osso_inf,
                             path_osso_sup, prog, sombra_osso, texto)
from .cf_comum import capa, fazer_render, interface, selo_como_funciona
from .cf_fratura_cola import YF, _regiao_abaixo, _regiao_acima, _zig

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "quebrou": ("quebrou", 1, False),
    "lugar1": ("lugar", 1, False),
    "antes": ("antes", 1, False),
    "investiga": ("investiga", 1, False),
    "causa": ("causa", 1, False),            # "causa." da 1ª frase ("causas" é outra palavra)
    "refratura": ("refratura", 1, False),
    "possiveis": ("possíveis", 1, False),
    "causas": ("causas", 1, False),          # a prancheta entra aqui: o cartão REFRATURA fica ~1,2 s
    "estabilidade": ("estabilidade", 1, False),
    "fatores": ("fatores", 1, False),
    "momento": ("momento", 1, False),        # "E o momento de voltar à carga": o 3º item acende já aqui
    "carga": ("carga", 1, False),
    "esporte": ("esporte", 1, False),
    "antes2": ("antes", 2, False),           # "antes da hora"
    "nova": ("nova", 1, False),
    "fratura": ("fratura", 1, False),
    "mesmo3": ("mesmo", 3, False),           # "nova fratura no MESMO lugar"
    "lugar2": ("lugar", 2, False),
    "tratamento": ("tratamento", 1, False),
    "individualizado": ("individualizado", 1, False),
    "pode": ("pode", 1, False),
    "revisao": ("revisão", 1, False),        # 'fixação' também é dita na 3ª frase
    "enxerto": ("enxerto", 1, False),
    "selecionados": ("selecionados", 1, False),
    "fixador": ("fixador", 1, False),
    "manda": ("manda", 1, False),
}
DESTAQUE = {"quebrou", "lugar", "investiga", "causa", "refratura", "causas", "estabilidade", "fatores", "carga",
            "esporte", "hora", "fratura", "individualizado", "revisão", "enxerto", "fixador", "externo"}

# ------------------------------------------------------------------ texto de tela (todo ele está em ep["tela"])
T_MESMO = "MESMO LUGAR"
T_INVEST = "INVESTIGAÇÃO DA CAUSA"
T_CARIMBO = "ANTES DE TRATAR IGUAL"
T_REFRAT = "REFRATURA"
T_REFRAT_SUB = "quebrar o mesmo osso de novo"
T_TITULO = "TRÊS POSSÍVEIS CAUSAS"
T_ESPORTE = "ESPORTE"
T_HORA = "ANTES DA HORA"
T_NOVA = "NOVA FRATURA"
T_SELO = "O TRATAMENTO É INDIVIDUALIZADO"
T_SELEC = "em casos selecionados"
ITENS = (("ESTABILIDADE DA FIXAÇÃO", "estabilidade"), ("FATORES DO PACIENTE", "fatores"), ("RETORNO À CARGA", "momento"))
PLACAS = (("REVISÃO DA FIXAÇÃO", "revisao"), ("ENXERTO ÓSSEO", "enxerto"), ("FIXADOR EXTERNO", "fixador"))

# ------------------------------------------------------------------ paleta e geometria
SY = 790                                  # âncora vertical da câmera na tela
AZUL = "#9CC9FF"
NEUTRO = "#C9D6E2"
FUNDO_CARTAO = "#0B1824"
APAGADO = "#4E6278"
LINHA = "#3B2D20"                         # traço fino e escuro da linha nova
MARFIM = "#E8DCC4"
OSSO = skia.Op(path_osso_sup(Y_TOPO, YF + 4), path_osso_inf(YF - 4, Y_BASE), skia.PathOp.kUnion_PathOp)
FRAGS = (skia.Op(OSSO, _regiao_acima(YF), skia.PathOp.kIntersect_PathOp),
         skia.Op(OSSO, _regiao_abaixo(YF), skia.PathOp.kIntersect_PathOp))
SEP = 14.0                                # quanto as metades se afastam (mundo): só alguns pixels
TRACO = 6.0                               # espessura da linha nova (legível no celular)
MEIA_FAIXA = 17                           # meia altura da faixa dourada (o zigue-zague tem ±9)

# prancheta (tela)
PX0, PY0, PX1, PY1 = 296, 262, 1036, 866
Y_TIT = 374
LUPA_TIT = (350, 359, 28)
Y_ITENS = (500, 614, 728)                 # linha de base do texto de cada item
X_ICO, X_TXT = 359, 414
Y_SUB = 816
CANTO = (1000, 232)                       # para onde a prancheta recolhe

# placas de caminho (tela)
POSTE_X, POSTE_Y0, POSTE_Y1 = 398, 432, 1182
Y_PLACAS = (546, 726, 906)
PL_X0, PL_X1, PL_TIP, PL_H = 412, 968, 46, 92


# ------------------------------------------------------------------ câmera
def camera(t, T):
    """-> (bx, s, fy): o ponto do mundo (CX, fy) vai para (bx, SY) na tela, com escala s."""
    bx, s, fy = 540.0, 0.92, 752.0                                        # capa: osso inteiro no centro
    t0 = t_racha(T)                                                       # empurrão curto quando racha
    k = e_out(prog(t, t0, t0 + 0.3)) * (1 - e_inout(prog(t, T["lugar1"] - 0.3, T["lugar1"] + 0.3)))
    s = lerp(s, S_RACHA, k)                                               # fy fixo: o topo não invade o gancho
    k = e_inout(prog(t, T["antes"] + 0.05, T["antes"] + 0.85))           # abre a direita para os rótulos
    bx = lerp(bx, 330.0, k)
    k = e_inout(prog(t, T["causas"] - 0.25, T["causas"] + 0.45))         # menor, ao fundo, embaixo à esquerda
    bx = lerp(bx, 170.0, k); s = lerp(s, 0.68, k); fy = lerp(fy, 583.5, k)
    k = e_inout(prog(t, t_colapso(T), t_colapso(T) + 0.7))               # sozinho no centro, sob o selo
    bx = lerp(bx, 540.0, k); s = lerp(s, 0.70, k); fy = lerp(fy, 774.0, k)
    k = e_inout(prog(t, T["individualizado"] + 0.9, T["individualizado"] + 1.45))   # abre lugar para o poste
    bx = lerp(bx, 205.0, k)
    k = e_inout(prog(t, T["manda"] - 0.1, T["manda"] + 0.55))            # CTA: só o osso, de volta ao centro
    bx = lerp(bx, 540.0, k)
    return bx, s, fy


S_RACHA = 1.0


def t_colapso(T):
    """Quando a prancheta recolhe (depois de 'nova fratura no mesmo lugar' ter tempo de leitura)."""
    return T["tratamento"] + 0.15


def t_racha(T):
    return T["quebrou"] + 0.3


def tremor(t, T):
    x = 0.0
    for t0, f in ((t_racha(T) + 0.2, 3), (T["causa"], 7), (T["individualizado"], 4)):
        k = t - t0
        if 0 <= k < 0.3:
            x += f * math.sin(k * 70) * (1 - k / 0.3)
    return x


def tela(cam, x, y):
    bx, s, fy = cam
    return bx + s * (x - CX), SY + s * (y - fy)


def aplica(cv, cam):
    bx, s, fy = cam
    cv.translate(bx, SY); cv.scale(s, s); cv.translate(-CX, -fy)


# ------------------------------------------------------------------ utilidades de desenho
def _alfa(a):
    p = skia.Paint()
    p.setAlphaf(clamp(a))
    return p


def ponta(cv, x, y, ang, tam, cor, a):
    """Cabeça de seta em (x, y) apontando para `ang` (radianos). (cópia do cf_pe_virado)"""
    p = skia.Path()
    p.moveTo(x + tam * math.cos(ang), y + tam * math.sin(ang))
    p.lineTo(x + tam * 0.75 * math.cos(ang + 2.45), y + tam * 0.75 * math.sin(ang + 2.45))
    p.lineTo(x + tam * 0.75 * math.cos(ang - 2.45), y + tam * 0.75 * math.sin(ang - 2.45))
    p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))


def etiqueta(cv, s, x, y, alvo, cor, a, tam=36, seta=False):
    """Rótulo com linha-guia (o `rotulo` do cf_alongamento com fonte ajustável; cópia do
    cf_pseudartrose). (x, y): borda esquerda da caixa e linha de base do texto; `alvo`: ponto
    apontado (com seta na ponta se `seta`)."""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    sx, sy = x, y - tam * 0.36
    cv.drawLine(alvo[0], alvo[1], sx, sy, paint(cor, int(220 * a), "stroke", 3))
    if seta:
        ponta(cv, alvo[0], alvo[1], math.atan2(alvo[1] - sy, alvo[0] - sx), 20, cor, a)
    else:
        cv.drawCircle(alvo[0], alvo[1], 6, paint(cor, int(255 * a)))
    rr = skia.RRect.MakeRectXY(skia.Rect(x, y - tam * 1.08, x + lw + 30, y + tam * 0.32), 14, 14)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(228 * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 2.5))
    cv.drawString(s, x + 15, y, f, paint(cor, int(255 * a)))


def chip_esq(cv, s, x, y, cor, a, tam=36):
    """Rótulo solto alinhado pela ESQUERDA da caixa (x); y = linha de base. Devolve a largura."""
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    if a > 0:
        rr = skia.RRect.MakeRectXY(skia.Rect(x, y - tam * 1.05, x + lw + 32, y + tam * 0.34), 14, 14)
        cv.drawRRect(rr, paint(FUNDO_CARTAO, int(228 * a)))
        cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 3))
        cv.drawString(s, x + 16, y, f, paint(cor, int(255 * a)))
    return lw + 32


def carimbo_opaco(cv, s, x, y, rot, t0, t, dur, tam=60, esc0=1.7):
    """Carimbo ouro torto com fundo opaco (legível sobre o osso claro). (cópia do cf_pseudartrose)"""
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


def circulo_tracejado(cv, x, y, r, cor, a, larg=5.0, fase=0.0):
    if a <= 0 or r <= 1:
        return
    p = paint(cor, int(255 * a), "stroke", larg)
    p.setPathEffect(skia.DashPathEffect.Make([16.0, 11.0], fase))
    cv.drawCircle(x, y, r, p)


# ------------------------------------------------------------------ o osso (mundo)
def _zig_path(pr=1.0):
    """O zigue-zague do cf_fratura_cola, desenhado até a fração `pr` (da esquerda para a direita)."""
    z = _zig(YF); n = len(z) - 1; alvo = pr * n
    p = skia.Path(); p.moveTo(*z[0])
    for i in range(1, n + 1):
        if i <= alvo:
            p.lineTo(*z[i])
        else:
            f = alvo - (i - 1)
            if f > 0:
                p.lineTo(lerp(z[i - 1][0], z[i][0], f), lerp(z[i - 1][1], z[i][1], f))
            break
    return p


def _faixa(cv):
    """Marca da fratura anterior: faixa chapada, na largura da diáfise (o recorte é o próprio osso)."""
    r = skia.Rect(CX - HASTE / 2 - 4, YF - MEIA_FAIXA, CX + HASTE / 2 + 4, YF + MEIA_FAIXA)
    cv.drawRect(r, paint(NOVO, 165))
    for y in (YF - MEIA_FAIXA, YF + MEIA_FAIXA):
        cv.drawLine(r.left(), y, r.right(), y, paint("#C08A2C", 130, "stroke", 2))


def osso(cv, t, T):
    t0 = t_racha(T)
    sh = sombra_osso()
    if t < t0 + 0.2:                                   # inteiro (capa) e a linha sendo riscada
        cv.drawPath(OSSO, paint("#000000", 70, blur=14))
        cv.drawPath(OSSO, paint(OSSO_C, shader=sh))
        cv.save(); cv.clipPath(OSSO, skia.ClipOp.kIntersect, True)
        _faixa(cv)
        pr = e_out(prog(t, t0, t0 + 0.18))
        if pr > 0:
            cv.drawPath(_zig_path(pr), paint(LINHA, 240, "stroke", TRACO))
        cv.restore()
        cv.drawPath(OSSO, paint(OSSO_L, 150, "stroke", 2.5))
        return
    sep = SEP * e_out(prog(t, t0 + 0.2, t0 + 0.45))
    zp = _zig_path()
    for parte, dy in ((0, -sep / 2), (1, sep / 2)):
        cv.save(); cv.translate(0, dy)
        cv.drawPath(FRAGS[parte], paint("#000000", 70, blur=14))
        cv.restore()
    k = t - (t0 + 0.2)                                 # lampejo quente ATRÁS do osso: só vaza pela racha
    if 0 <= k < 0.5:
        a = 1 - e_out(k / 0.5)
        cv.drawOval(skia.Rect(CX - 170, YF - 30, CX + 170, YF + 30), paint(OURO, int(170 * a), blur=22))
        cv.drawPath(zp, paint(OURO, int(235 * a), "stroke", 30, blur=14))
        cv.drawPath(zp, paint("#FFF4D6", int(255 * a), "stroke", 8, blur=3))
    for parte, dy in ((0, -sep / 2), (1, sep / 2)):
        cv.save(); cv.translate(0, dy)
        cv.save(); cv.clipPath(FRAGS[parte], skia.ClipOp.kIntersect, True)
        cv.drawPath(OSSO, paint(OSSO_C, shader=sh))
        _faixa(cv)
        cv.restore()
        cv.drawPath(FRAGS[parte], paint(OSSO_L, 150, "stroke", 2.5))
        # a borda da racha por cima do contorno claro (senão o contorno apaga a linha), só na diáfise
        cv.save(); cv.clipRect(skia.Rect(CX - HASTE / 2 - 1, YF - 40, CX + HASTE / 2 + 1, YF + 40), skia.ClipOp.kIntersect, True)
        cv.drawPath(zp, paint(LINHA, 240, "stroke", TRACO))
        cv.restore()
        cv.restore()


# ------------------------------------------------------------------ lupa
def lupa(cv, x, y, R, ang, a, conteudo=None, a_cont=0.0):
    """Lupa simples: aro e cabo ouro, vidro azul; `conteudo(cv)` desenha o que ela amplia."""
    if a <= 0 or R <= 1:
        return
    ca, sa = math.cos(ang), math.sin(ang)
    x0, y0, x1, y1 = x + R * ca, y + R * sa, x + R * 1.95 * ca, y + R * 1.95 * sa
    larg = max(6.0, R * 0.24)
    cv.drawLine(x0, y0, x1, y1, paint("#000000", int(90 * a), "stroke", larg + 8, blur=6))
    cv.drawLine(x0, y0, x1, y1, paint("#6B4E12", int(255 * a), "stroke", larg + 4))
    cv.drawLine(x0, y0, x1, y1, paint(OURO, int(255 * a), "stroke", larg))
    cv.drawCircle(x, y, R, paint("#000000", int(80 * a), blur=10))
    cv.drawCircle(x, y, R, paint("#1F4C66", int(235 * a)))
    if conteudo and a_cont > 0:
        n = cv.save()
        clip = skia.Path(); clip.addCircle(x, y, R)
        cv.clipPath(clip, skia.ClipOp.kIntersect, True)
        if a_cont < 1:
            cv.saveLayer(None, _alfa(a_cont * a))
        conteudo(cv)
        cv.restoreToCount(n)
    aro = max(4.0, R * 0.1)
    cv.drawArc(skia.Rect(x - R * 0.74, y - R * 0.74, x + R * 0.74, y + R * 0.74), 200, 55, False,
               paint("#FFFFFF", int(120 * a), "stroke", max(2.0, R * 0.06)))
    cv.drawCircle(x, y, R, paint("#000000", int(90 * a), "stroke", aro + 6, blur=5))
    cv.drawCircle(x, y, R, paint(OURO, int(255 * a), "stroke", aro))
    cv.drawCircle(x, y, R - aro * 0.55, paint("#FFF1C9", int(100 * a), "stroke", 2))


def colapso(t, T):
    """-> (c, escala, alfa) da prancheta recolhendo para o canto (e da lupa que está nela)."""
    c = e_inout(prog(t, t_colapso(T), t_colapso(T) + 0.65))
    return c, lerp(1.0, 0.08, c), 1 - prog(c, 0.25, 0.85)


def no_colapso(x, y, sc):
    return CANTO[0] + (x - CANTO[0]) * sc, CANTO[1] + (y - CANTO[1]) * sc


def dx_prancheta(t, T):
    return 760 * (1 - e_out(prog(t, T["causas"] + 0.05, T["causas"] + 0.6)))


def estado_lupa(t, T, cam):
    """-> (x, y, R, ângulo do cabo, alfa, alfa do conteúdo ampliado) ou None."""
    t0 = T["investiga"]
    if t < t0 - 0.05:
        return None
    px, py = tela(cam, CX, YF)
    # entra pela esquerda (a direita é dos rótulos), ATRAVESSA a linha, volta e PARA nela antes do
    # carimbo: um só movimento com ultrapassagem (e_back), parado exatamente em "causa"
    k1 = prog(t, t0 - 0.05, T["causa"])
    x = lerp(-170, px, e_back(k1, 1.9))
    y = lerp(py + 90, py, e_out(prog(t, t0 - 0.05, t0 + 0.35)))
    R, ang = 112.0, math.radians(135)
    k3 = e_inout(prog(t, T["causas"] - 0.05, T["causas"] + 0.7))       # sobe para o topo da prancheta
    x = lerp(x, LUPA_TIT[0] + dx_prancheta(t, T), k3); y = lerp(y, LUPA_TIT[1], k3); R = lerp(R, LUPA_TIT[2], k3)
    a_cont = 1 - prog(k3, 0.0, 0.4)
    c, sc, a_c = colapso(t, T)
    if c > 0:
        x, y = no_colapso(x, y, sc); R *= sc
    return x, y, R, ang, clamp(k1 * 3) * a_c, a_cont


# ------------------------------------------------------------------ rótulos da abertura (tela)
def rotulos_abertura(cv, t, T, cam):
    pxd, pyd = tela(cam, CX + HASTE / 2 + 4, YF)        # borda direita do osso, na linha
    # MESMO LUGAR, com seta para o ponto (sai quando a lupa chega)
    a = prog(t, T["lugar1"], T["lugar1"] + 0.25) * (1 - prog(t, T["investiga"] - 0.15, T["investiga"] + 0.1))
    etiqueta(cv, T_MESMO, pxd + 62, pyd - 140, (pxd + 10, pyd - 6), OURO, a, tam=40, seta=True)
    # INVESTIGAÇÃO DA CAUSA: aponta para o aro da lupa parada
    st = estado_lupa(t, T, cam)
    a = prog(t, T["investiga"] + 0.25, T["investiga"] + 0.5) * (1 - prog(t, T["refratura"] - 0.15, T["refratura"] + 0.05))
    if st and a > 0:
        lx, ly, R = st[0], st[1], st[2]
        alvo = (lx + R * math.cos(-0.45) + 6, ly + R * math.sin(-0.45) - 3)
        etiqueta(cv, T_INVEST, 490, ly - 104, alvo, OURO, a, tam=34)
    # REFRATURA (e a definição embaixo, menor, em minúsculas): cartão ao lado do osso
    k = prog(t, T["refratura"], T["refratura"] + 0.3)
    a = k * (1 - prog(t, T["causas"] - 0.1, T["causas"] + 0.1))           # sai antes de a prancheta cobrir
    if a > 0:
        _, pyf = tela(camera(T["refratura"], T), CX + HASTE / 2 + 4, YF)  # parado: a câmera já encolhe
        x0, y0, x1, y1 = 486, pyf - 186, 1030, pyf - 30
        if st:                                                          # aponta para a lupa sobre a linha
            lx, ly, R = st[0], st[1], st[2]
            alvo = (lx + (R + 8) * math.cos(0.35), ly + (R + 8) * math.sin(0.35))
        else:
            alvo = tela(cam, CX + HASTE / 2 + 2, YF)
        cv.drawLine(alvo[0], alvo[1], x0, y1 - 40, paint(OURO, int(220 * a), "stroke", 3))
        cv.drawCircle(alvo[0], alvo[1], 6, paint(OURO, int(255 * a)))
        esc = lerp(0.86, 1.0, e_back(prog(t, T["refratura"], T["refratura"] + 0.45)))
        cv.save(); cv.translate((x0 + x1) / 2, (y0 + y1) / 2); cv.scale(esc, esc); cv.translate(-(x0 + x1) / 2, -(y0 + y1) / 2)
        rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 22, 22)
        cv.drawRRect(rr, paint(FUNDO_CARTAO, int(238 * a)))
        cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 4))
        texto(cv, T_REFRAT, (x0 + x1) / 2, y0 + 78, F_BLACK, 56, OURO, int(255 * a))
        texto(cv, T_REFRAT_SUB, (x0 + x1) / 2, y0 + 128, F_SEMI, 32, AZUL, int(255 * a))
        cv.restore()


def pulso_ponto(cv, t, T, cam, t0, r0, r1):
    """Um círculo tracejado dourado que se abre e some uma vez no ponto da linha."""
    k = prog(t, t0, t0 + 0.9)
    if 0 < k < 1:
        x, y = tela(cam, CX, YF)
        circulo_tracejado(cv, x, y, lerp(r0, r1, e_out(k)), OURO, 1 - k, larg=5, fase=t * 30)


# ------------------------------------------------------------------ ícones da prancheta
def icone_placa(cv, x, y, cor, a, esc):
    """Placa simples: barra com dois pontos de parafuso (nenhum osso sendo operado)."""
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-27, -9, 27, 9), 9, 9)
    cv.drawRRect(rr, paint(cor, int(255 * a)))
    cv.drawRRect(rr, paint("#33475B", int(255 * a), "stroke", 2))
    for dx in (-14, 14):
        cv.drawCircle(dx, 0, 4.6, paint("#33475B", int(255 * a)))
        cv.drawLine(dx - 3, -2.5, dx + 3, 2.5, paint(cor, int(255 * a), "stroke", 1.6))
    cv.restore()


def icone_pessoa(cv, x, y, cor, a, esc):
    """Pessoa neutra: círculo e ombros, sem rosto."""
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    cv.drawCircle(0, -11, 10.5, paint(cor, int(255 * a)))
    p = skia.Path(); p.moveTo(-21, 23); p.cubicTo(-21, 4, -10, 2, 0, 2); p.cubicTo(10, 2, 21, 4, 21, 23); p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))
    cv.restore()


def icone_carga(cv, x, y, cor, a, esc, desce=0.0):
    """Seta para baixo sobre uma linha de chão (peso)."""
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    cv.drawLine(-26, 19, 26, 19, paint(cor, int(255 * a), "stroke", 4))
    for i in range(4):
        hx = -18 + i * 12
        cv.drawLine(hx, 22, hx - 6, 29, paint(cor, int(180 * a), "stroke", 2.4))
    cv.translate(0, -desce)
    cv.drawLine(0, -27, 0, -2, paint(cor, int(255 * a), "stroke", 7))
    p = skia.Path(); p.moveTo(-12, -4); p.lineTo(12, -4); p.lineTo(0, 12); p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))
    cv.restore()


def bola(cv, x, y, r, a, giro):
    """Bola: círculo simples com gomo central e costuras."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.rotate(giro)
    cv.drawCircle(0, 0, r, paint("#EEF3F8", int(255 * a)))
    pent = skia.Path()
    for i in range(5):
        an = -math.pi / 2 + i * 2 * math.pi / 5
        (pent.moveTo if i == 0 else pent.lineTo)(r * 0.38 * math.cos(an), r * 0.38 * math.sin(an))
    pent.close()
    cv.drawPath(pent, paint("#33475B", int(255 * a)))
    for i in range(5):
        an = -math.pi / 2 + i * 2 * math.pi / 5
        cv.drawLine(r * 0.38 * math.cos(an), r * 0.38 * math.sin(an), r * 0.95 * math.cos(an), r * 0.95 * math.sin(an),
                    paint("#33475B", int(220 * a), "stroke", 2.2))
    cv.drawCircle(0, 0, r, paint("#5E7186", int(255 * a), "stroke", 2.5))
    cv.restore()


def relogio(cv, x, y, r, a, ang):
    """Relógio simples (sem número): o ponteiro corre."""
    if a <= 0:
        return
    cv.drawCircle(x, y, r, paint(FUNDO_CARTAO, int(255 * a)))
    cv.drawCircle(x, y, r, paint("#EEF3F8", int(255 * a), "stroke", 4))
    for i in range(4):
        q = i * math.pi / 2
        cv.drawLine(x + (r - 7) * math.cos(q), y + (r - 7) * math.sin(q), x + (r - 3) * math.cos(q), y + (r - 3) * math.sin(q),
                    paint("#EEF3F8", int(200 * a), "stroke", 2.5))
    cv.drawLine(x, y, x + r * 0.42 * math.cos(ang / 12 - math.pi / 2), y + r * 0.42 * math.sin(ang / 12 - math.pi / 2),
                paint("#EEF3F8", int(255 * a), "stroke", 4))
    cv.drawLine(x, y, x + r * 0.7 * math.cos(ang - math.pi / 2), y + r * 0.7 * math.sin(ang - math.pi / 2),
                paint(OURO, int(255 * a), "stroke", 3.5))
    cv.drawCircle(x, y, 3.5, paint(OURO, int(255 * a)))


# ------------------------------------------------------------------ prancheta (tela)
def prancheta(cv, t, T):
    ent = prog(t, T["causas"] + 0.05, T["causas"] + 0.6)
    c, sc, a_c = colapso(t, T)
    a = clamp(ent * 3) * a_c
    if a <= 0:
        return
    n = cv.save()
    if a < 1:
        cv.saveLayer(None, _alfa(a))
    cv.translate(CANTO[0], CANTO[1]); cv.scale(sc, sc); cv.translate(-CANTO[0] + dx_prancheta(t, T), -CANTO[1])
    rr = skia.RRect.MakeRectXY(skia.Rect(PX0, PY0, PX1, PY1), 24, 24)
    cv.drawRRect(rr, paint("#000000", 90, blur=14))
    cv.drawRRect(rr, paint(FUNDO_CARTAO, 238))
    cv.drawRRect(rr, paint(MARFIM, 220, "stroke", 4))
    cm = (PX0 + PX1) / 2                                               # prendedor dourado
    pr = skia.RRect.MakeRectXY(skia.Rect(cm - 64, PY0 - 22, cm + 64, PY0 + 22), 11, 11)
    cv.drawRRect(pr, paint(OURO)); cv.drawRRect(pr, paint("#8A6512", 255, "stroke", 3))
    cv.drawCircle(cm, PY0 - 4, 7, paint("#8A6512"))
    texto(cv, T_TITULO, 398, Y_TIT, F_BLACK, 40, OURO, 255, centro=False)
    cv.drawLine(PX0 + 26, Y_TIT + 30, PX1 - 26, Y_TIT + 30, paint("#8FA3B8", 70, "stroke", 2))
    for i, ((s, chave), yb) in enumerate(zip(ITENS, Y_ITENS)):
        yc = yb - 14
        t0 = T[chave] - 0.1
        on = prog(t, t0, t0 + 0.3)
        caixa = skia.RRect.MakeRectXY(skia.Rect(X_ICO - 35, yc - 35, X_ICO + 35, yc + 35), 14, 14)
        brilho = on * (1 - prog(t, t0 + 0.4, t0 + 1.4))
        if brilho > 0:
            cv.drawRRect(caixa, paint(OURO, int(130 * brilho), blur=12))
        cv.drawRRect(caixa, paint("#10263A", 255))
        cv.drawRRect(caixa, paint(lerpc(APAGADO, OURO, on), 255, "stroke", 3.5))
        if on <= 0:                                                    # linha vazia
            cv.drawLine(X_TXT, yb - 12, PX1 - 40, yb - 12, paint("#33485E", 255, "stroke", 4))
            continue
        esc = lerp(0.4, 1.0, e_back(prog(t, t0, t0 + 0.45)))
        if i == 0:
            icone_placa(cv, X_ICO, yc, ACO_HL, on, esc)
        elif i == 1:
            icone_pessoa(cv, X_ICO, yc, NEUTRO, on, esc)
        else:
            desce = 16 * (1 - e_back(prog(t, T["carga"] - 0.05, T["carga"] + 0.3)))   # o peso desce em "carga"
            cv.save(); cv.clipRRect(caixa, skia.ClipOp.kIntersect, True)        # a seta erguida não vaza da caixa
            icone_carga(cv, X_ICO, yc, "#EEF3F8", on, esc, desce=desce)
            cv.restore()
        cv.drawLine(lerp(X_TXT, PX1 - 40, on), yb - 12, PX1 - 40, yb - 12, paint("#33485E", int(255 * (1 - on)), "stroke", 4))
        cor = lerpc(OURO, "#FFFFFF", prog(t, t0 + 0.7, t0 + 1.5))
        texto(cv, s, X_TXT + 26 * (1 - e_out(on)), yb, F_BLACK, 36, cor, int(255 * on), centro=False)
        brilhos(cv, X_ICO, yc, t, t0 + 0.05, n=9, raio=70)
    # esporte antes da hora: sub-linha ligada ao 3º item
    a_b = prog(t, T["esporte"] - 0.1, T["esporte"] + 0.2)
    if a_b > 0:
        y3 = Y_ITENS[2] - 14
        ko = e_out(prog(t, T["esporte"] - 0.1, T["esporte"] + 0.25))
        p = skia.Path(); p.moveTo(X_ICO, y3 + 38); p.lineTo(X_ICO, lerp(y3 + 38, Y_SUB, ko))
        if ko >= 1:
            p.lineTo(X_ICO + 34, Y_SUB)
        cv.drawPath(p, paint("#6F8399", int(255 * a_b), "stroke", 3))
        rola = e_out(prog(t, T["esporte"] - 0.1, T["esporte"] + 0.5))
        bola(cv, lerp(400, 430, rola), Y_SUB, 21 * lerp(0.6, 1.0, e_back(prog(t, T["esporte"] - 0.1, T["esporte"] + 0.35))),
             a_b, (rola - 1) * 2.4)
        texto(cv, T_ESPORTE, 464, Y_SUB + 12, F_BLACK, 32, "#FFFFFF", int(255 * a_b), centro=False)
    a_r = prog(t, T["antes2"] - 0.05, T["antes2"] + 0.2)
    if a_r > 0:
        esc = lerp(0.6, 1.0, e_back(prog(t, T["antes2"] - 0.05, T["antes2"] + 0.35)))
        cv.save(); cv.translate(652, Y_SUB); cv.scale(esc, esc)
        relogio(cv, 0, 0, 22, a_r, (t - T["antes2"]) * 7.0)
        cv.restore()
        texto(cv, T_HORA, 686, Y_SUB + 12, F_BLACK, 32, "#FFFFFF", int(255 * a_r), centro=False)
    cv.restoreToCount(n)


def ligacao_ponto(cv, t, T, cam):
    """Voltar antes da hora -> nova fratura no MESMO LUGAR: pontilhado do 3º item até o ponto."""
    c, sc, a_c = colapso(t, T)
    fora = 1 - prog(t, t_colapso(T), t_colapso(T) + 0.35)
    if fora <= 0 or t < T["nova"] - 0.05:
        return
    cx, cy = tela(cam, CX, YF)
    _, s, _ = cam
    rc = 104 * s                                                       # raio do círculo no ponto
    x0, y0 = X_ICO - 42, Y_ITENS[2] - 14
    ang = math.atan2(y0 - cy, x0 - cx)
    x2, y2 = cx + (rc + 10) * math.cos(ang), cy + (rc + 10) * math.sin(ang)
    x1, y1 = lerp(x0, x2, 0.15) - 40, lerp(y0, y2, 0.55)
    pr = e_out(prog(t, T["nova"] - 0.05, T["fratura"] + 0.25))
    N = 15
    for i in range(N + 1):
        u = i / N
        if u > pr + 1e-6:
            break
        x = (1 - u) ** 2 * x0 + 2 * (1 - u) * u * x1 + u * u * x2
        y = (1 - u) ** 2 * y0 + 2 * (1 - u) * u * y1 + u * u * y2
        cv.drawCircle(x, y, 5, paint(OURO, int(255 * fora)))
    if pr >= 1:
        ponta(cv, x2, y2, math.atan2(y2 - y1, x2 - x1), 16, OURO, fora)
    # o ponto: círculo tracejado que cai em "mesmo", pulsa de novo em "lugar" e fica
    a = prog(t, T["mesmo3"] - 0.05, T["mesmo3"] + 0.2) * fora
    if a > 0:
        esc = lerp(1.35, 1.0, e_out(prog(t, T["mesmo3"] - 0.05, T["mesmo3"] + 0.3)))
        circulo_tracejado(cv, cx, cy, rc * esc, OURO, a, larg=5, fase=t * 18)
    pulso_ponto(cv, t, T, cam, T["mesmo3"], rc, rc * 2.1)
    pulso_ponto(cv, t, T, cam, T["lugar2"], rc, rc * 1.8)
    # NOVA FRATURA ao lado de MESMO LUGAR, logo à direita do ponto
    yb = cy + rc * 0.55 + 22
    xa = cx + rc * 0.75 + 34
    a1 = prog(t, T["fratura"], T["fratura"] + 0.25) * fora
    w = chip_esq(cv, T_NOVA, xa, yb, OURO, a1, tam=36)
    if a1 > 0:
        cv.drawLine(cx + rc * 0.72, cy + rc * 0.62, xa, yb - 14, paint(OURO, int(220 * a1), "stroke", 3))
    a2 = prog(t, T["mesmo3"], T["mesmo3"] + 0.25) * fora
    chip_esq(cv, T_MESMO, xa + w + 20, yb, OURO, a2, tam=36)


# ------------------------------------------------------------------ tratamento (tela)
def selo_individual(cv, t, T):
    t0 = T["individualizado"]
    k = t - t0
    if k < -0.02:
        return
    a = clamp((k + 0.02) / 0.1) * (1 - prog(t, T["manda"] - 0.3, T["manda"]))
    if a <= 0:
        return
    esc = lerp(1.6, 1.0, e_out(clamp(k / 0.18)))
    cv.save(); cv.translate(CX, 312); cv.rotate(-2.5); cv.scale(esc, esc)
    f = skia.Font(F_BLACK, 40); lw = f.measureText(T_SELO)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 28, -50, lw / 2 + 28, 20), 14, 14)
    cv.drawRRect(rr, paint("#000000", int(80 * a), blur=10))
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(240 * a))); cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 5))
    cv.drawString(T_SELO, -lw / 2, 0, f, paint(OURO, int(255 * a)))
    cv.restore()


def fixador_mini(cv, x, y, a, esc=1.25):
    """Miniatura do fixador do cf_alongamento: dois anéis (metade de trás escura, fios, metade da
    frente) ligados por duas hastes verticais, com as porcas ouro. Ícone: nenhum osso, nenhuma técnica."""
    if a <= 0:
        return
    rx, ry, dy = 40 * esc, 11 * esc, 16 * esc
    xs = (x - rx * 0.72, x + rx * 0.72)                       # hastes na frente dos anéis
    yh = ry * 0.69
    for yr in (y - dy, y + dy):                               # metades de trás e fios
        r = skia.Rect(x - rx, yr - ry, x + rx, yr + ry)
        cv.drawArc(r, 180, 180, False, paint(ACO_ESC, int(255 * a), "stroke", 4.5 * esc))
        for s in (-1, 1):
            cv.drawLine(x - rx + 7 * esc, yr - 4 * s * esc, x + rx - 7 * esc, yr + 4 * s * esc,
                        paint("#DDE6EE", int(230 * a), "stroke", 1.6))
    for xh in xs:                                             # hastes (o mesmo aço do cf_alongamento)
        cv.drawLine(xh, y - dy + yh - 9 * esc, xh, y + dy + yh + 9 * esc, paint("#000000", int(70 * a), "stroke", 6, blur=2))
        cv.drawLine(xh, y - dy + yh - 9 * esc, xh, y + dy + yh + 9 * esc, paint("#8FA3B8", int(255 * a), "stroke", 4.5))
        cv.drawLine(xh - 1, y - dy + yh - 9 * esc, xh - 1, y + dy + yh + 9 * esc, paint(ACO_HL, int(150 * a), "stroke", 1.2))
    for yr in (y - dy, y + dy):                               # metades da frente
        r = skia.Rect(x - rx, yr - ry, x + rx, yr + ry)
        cv.drawArc(r, 0, 180, False, paint(ACO, int(255 * a), "stroke", 4.5 * esc))
        cv.drawArc(skia.Rect(r.left() + 3, r.top() + 2, r.right() - 3, r.bottom() - 1), 25, 130, False,
                   paint(ACO_HL, int(170 * a), "stroke", 1.4))
        for xh in xs:                                         # porca onde a haste cruza o anel
            cv.drawCircle(xh, yr + yh, 3.6 * esc, paint(OURO, int(255 * a)))
            cv.drawCircle(xh, yr + yh, 3.6 * esc, paint("#8A6512", int(255 * a), "stroke", 1.2))


def _placa_path(yc):
    h = PL_H / 2
    p = skia.Path(); p.moveTo(PL_X0, yc - h); p.lineTo(PL_X1, yc - h); p.lineTo(PL_X1 + PL_TIP, yc)
    p.lineTo(PL_X1, yc + h); p.lineTo(PL_X0, yc + h); p.close()
    return p


def poste_placas(cv, t, T):
    k = e_out(prog(t, T["pode"] + 0.05, T["pode"] + 0.5))
    if k <= 0:
        return
    fundo_cta = 1 - prog(t, T["manda"] - 0.4, T["manda"] - 0.05)       # sai na CTA: nada de texto atrás do texto
    if fundo_cta <= 0:
        return
    a = clamp(k * 4) * fundo_cta
    topo = lerp(POSTE_Y1, POSTE_Y0, k)
    cv.drawOval(skia.Rect(POSTE_X - 50, POSTE_Y1 - 9, POSTE_X + 50, POSTE_Y1 + 11), paint("#000000", int(80 * a), blur=7))
    sh = skia.GradientShader.MakeLinear([skia.Point(POSTE_X - 10, 0), skia.Point(POSTE_X + 10, 0)],
                                        [skia.Color(94, 113, 134), skia.Color(201, 214, 226), skia.Color(94, 113, 134)])
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(POSTE_X - 10, topo, POSTE_X + 10, POSTE_Y1), 6, 6), paint(ACO, int(255 * a), shader=sh))
    cv.drawCircle(POSTE_X, topo, 14, paint(OURO, int(255 * a)))
    cv.drawCircle(POSTE_X, topo, 14, paint("#8A6512", int(255 * a), "stroke", 2.5))
    # a vaga da 3ª placa (contorno tracejado) e o sub-rótulo, antes de a placa entrar
    yc3 = Y_PLACAS[2]
    vaga = prog(t, T["selecionados"] - 0.05, T["selecionados"] + 0.25) * (1 - prog(t, T["fixador"], T["fixador"] + 0.2))
    if vaga > 0:
        pv = paint("#8FA3B8", int(200 * vaga), "stroke", 3)
        pv.setPathEffect(skia.DashPathEffect.Make([16.0, 11.0], t * 20))
        cv.drawPath(_placa_path(yc3), pv)
    a_s = prog(t, T["selecionados"], T["selecionados"] + 0.3) * fundo_cta
    if a_s > 0:
        texto(cv, T_SELEC, PL_X0 + 22, yc3 + PL_H / 2 + 52 + 12 * (1 - e_out(a_s)), F_SEMI, 34, AZUL, int(255 * a_s), centro=False)
    for i, ((s, chave), yc) in enumerate(zip(PLACAS, Y_PLACAS)):
        t0 = T[chave] - 0.08
        kp = prog(t, t0, t0 + 0.45)
        if kp <= 0:
            continue
        abre = e_back(kp, 1.3)
        balanco = 5.0 * math.exp(-3.2 * max(0.0, t - t0)) * math.sin((t - t0) * 13) if t > t0 else 0.0
        ap = clamp(kp * 4) * fundo_cta
        cv.save(); cv.translate(POSTE_X, yc); cv.rotate(balanco); cv.scale(max(0.02, abre), 1); cv.translate(-POSTE_X, -yc)
        pth = _placa_path(yc)
        cv.drawPath(pth, paint("#000000", int(90 * ap), blur=10))
        cv.drawPath(pth, paint(FUNDO_CARTAO, int(240 * ap)))
        cv.drawPath(pth, paint(OURO, int(255 * ap), "stroke", 4))
        ins = skia.Path(); h = PL_H / 2 - 9
        ins.moveTo(PL_X0 + 9, yc - h); ins.lineTo(PL_X1 - 3, yc - h); ins.lineTo(PL_X1 + PL_TIP - 14, yc)
        ins.lineTo(PL_X1 - 3, yc + h); ins.lineTo(PL_X0 + 9, yc + h); ins.close()
        cv.drawPath(ins, paint("#FFFFFF", int(55 * ap), "stroke", 2))
        if i == 2:
            fixador_mini(cv, PL_X0 + 70, yc, ap, esc=1.25)
            texto(cv, s, PL_X0 + 140, yc + 13, F_BLACK, 38, "#FFFFFF", int(255 * ap), centro=False)
        else:
            texto(cv, s, PL_X0 + 30, yc + 13, F_BLACK, 38, "#FFFFFF", int(255 * ap), centro=False)
        cv.restore()
        # braçadeiras no poste (não giram com a placa)
        for dy in (-PL_H / 2 + 12, PL_H / 2 - 12):
            cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(POSTE_X - 15, yc + dy - 5, POSTE_X + 19, yc + dy + 5), 4, 4),
                         paint("#8FA3B8", int(255 * ap)))
        brilhos(cv, PL_X1 + PL_TIP - 10, yc, t, t0 + 0.3, n=7, raio=60)


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    bx, s, fy = camera(t, T)
    cam = (bx + tremor(t, T), s, fy)

    # mundo (câmera)
    cv.save(); aplica(cv, cam)
    osso(cv, t, T)
    cv.restore()

    # abertura: o ponto pulsa duas vezes quando racha e de novo em "lugar" (MESMO LUGAR)
    pulso_ponto(cv, t, T, cam, t_racha(T) + 0.2, 60, 190)
    pulso_ponto(cv, t, T, cam, t_racha(T) + 0.55, 60, 190)
    pulso_ponto(cv, t, T, cam, T["lugar1"], 70, 170)
    rotulos_abertura(cv, t, T, cam)

    # prancheta das três possíveis causas e a ligação com o ponto
    prancheta(cv, t, T)
    ligacao_ponto(cv, t, T, cam)

    # lupa (amplia o mesmo osso esquemático: não é exame)
    st = estado_lupa(t, T, cam)
    if st:
        lx, ly, R, ang, a, a_cont = st

        def ampliado(c2, lx=lx, ly=ly):
            c2.save(); c2.translate(lx, ly); c2.scale(1.8, 1.8); c2.translate(-lx, -ly)
            aplica(c2, cam); osso(c2, t, T)
            c2.restore()
        lupa(cv, lx, ly, R, ang, a, ampliado, a_cont)

    # tratamento
    poste_placas(cv, t, T)
    selo_individual(cv, t, T)
    carimbo_opaco(cv, T_CARIMBO, 625, 470, -6, T["causa"], t, dur=T["refratura"] + 0.45 - T["causa"], tam=52, esc0=1.6)

    capa(cv, t, T["antes"], ep["gancho"][0], ep["gancho"][1])
    selo_como_funciona(cv, prog(t, T["antes"] + 0.55, T["antes"] + 0.95) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface(cv, t, T, blocos, DESTAQUE)


# ------------------------------------------------------------------ som e prévias
def sons(T):
    t0 = t_racha(T)
    ev = [(t0, "tick", 0.9), (t0 + 0.2, "thump", 0.55), (t0 + 0.22, "shimmer", 0.2),
          (T["lugar1"], "pop", 0.45), (T["antes"] + 0.05, "whoosh", 0.3),
          (T["investiga"], "whoosh", 0.5), (T["investiga"] + 0.45, "shimmer", 0.3),
          (T["causa"] - 0.02, "thump", 0.9), (T["refratura"], "pop", 0.5),
          (T["causas"] - 0.05, "whoosh", 0.5), (T["causas"] + 0.45, "pop", 0.4),
          (T["estabilidade"] - 0.1, "ping", 0.55), (T["fatores"] - 0.1, "ping", 0.5),
          (T["momento"] - 0.1, "ping", 0.55), (T["carga"] + 0.1, "ding", 0.35),
          (T["esporte"] - 0.1, "pop", 0.45),
          (T["nova"], "whoosh", 0.3), (T["mesmo3"], "thump", 0.5), (T["lugar2"], "ping", 0.4),
          (t_colapso(T), "whoosh", 0.45), (T["individualizado"] - 0.02, "thump", 0.8),
          (T["pode"], "whoosh", 0.35), (T["selecionados"], "pop", 0.35),
          (T["manda"] - 0.1, "whoosh", 0.35), (T["manda"] + 0.05, "whoosh", 0.5)]
    for k in range(5):                                       # o relógio correndo (antes da hora)
        ev.append((T["antes2"] + 0.05 + 0.16 * k, "click", 0.35))
    for chave in ("revisao", "enxerto", "fixador"):         # cada placa encaixa no poste
        ev += [(T[chave] - 0.08, "whoosh", 0.25), (T[chave] + 0.05, "thump", 0.5), (T[chave] + 0.08, "click", 0.6)]
    ev.append((T["fixador"] + 0.12, "ping", 0.5))           # metal do anel
    return ev


def tempos_previa(T):
    return (0.0, t_racha(T) + 0.45, T["lugar1"] + 0.5, T["causa"] + 0.1, T["refratura"] + 1.0, T["causas"] + 1.0,
            T["momento"] + 0.5, T["antes2"] + 0.8, T["mesmo3"] + 0.7, T["individualizado"] + 0.6,
            T["fixador"] + 0.9, T["manda"] + 1.6)


render = fazer_render(quadro, ANCORAS, sons, tempos_previa)
