# -*- coding: utf-8 -*-
"""COMO FUNCIONA — quando voltar a pisar ("QUANDO EU POSSO / VOLTAR A PISAR?").

Mesmo estilo e mesmas peças das cenas aprovadas (contorno de perna do piloto, osso marfim, osso
novo dourado, placa azul-aço com cabeças douradas do cf_gesso_placa, rótulos, carimbos, brilhos,
legenda karaokê, CTA com aviãozinho). O mecanismo da cena: uma barra RESISTÊNCIA (o quanto o osso
colou) e uma seta CARGA sobre o pé, com uma linha tracejada saindo do nível da barra até a seta —
o teto da carga, que sobe junto com a barra. Cada coisa disparada pela palavra falada:
  * capa (t=0): a perna do piloto com um pé simples, parado no ar acima do piso; "pisar": o pé
    desce e para a um palmo do chão, com um "?" dourado; "data": calendário de parede SÓ com a
    grade (sem número, sem mês), folhas virando; "fixa": carimbo NÃO TEM DATA FIXA em cima do
    calendário, que sai pela lateral;
  * "fixação": a câmera aproxima; o osso longo marfim OPACO aparece dentro do contorno, com um
    risco de fratura no meio (sem fragmento, sem sangue); a placa desliza e encosta cruzando a
    fratura e as 4 cabeças surgem uma a uma (sem giro, sem trajeto dentro do osso);
  * "colou": barra vazia (só contorno dourado) ao lado, QUANTO O OSSO COLOU e "?" dentro; "calo":
    osso novo dourado preenche o vão na MESMA largura da diáfise; "resistência": a barra começa a
    encher devagar e o dourado do calo puxa para o marfim (sem completar);
  * "carga": a câmera recua, o pé encosta na plataforma, a seta CARGA aparece e a linha tracejada
    sai do nível da barra até ela; "progressivo": a seta curta, encostada na linha baixa, o pé
    tocando de leve; "conforme"/"evolui": dois degraus com clique — a barra sobe, a linha sobe
    junto e logo depois a seta cresce até a nova linha (nada de número; a barra não chega ao topo);
  * "dose": o pé pisa no ritmo, a seta exatamente na linha, que brilha a cada pisada, e o nome
    NA DOSE LIBERADA fica encostado na própria linha; "avisa": de cada pisada sobem ondas douradas
    em ARCO (não anéis) do pé até o calo, que pulsa — a barra NÃO dá salto; "necessário": carimbo
    dourado ACIMA do osso (não o cobre) e o contorno do osso acende;
  * "repouso": a seta some e o pé fica parado no ar; "enfraquece": o osso desbota (sem rachadura);
    "carga" (2ª): o pé volta e tudo volta ao estado anterior; "além": a seta passa da linha e o
    trecho que passou fica vermelho; "comprometer": triângulo de alerta (sem texto) ao lado do
    trecho vermelho — nada acontece com o osso nem com a placa; depois a seta recua até a linha;
  * "quem"/"equipe": prancheta QUEM LIBERA É A EQUIPE, FIXAÇÃO ganha check; "raio-X": VISOR
    (quatro cantos + varredura) sobre o MESMO osso esquemático — nada de fundo preto, negativo,
    filme ou osso translúcido — e CONSOLIDAÇÃO ganha check; "coragem": carimbo NÃO A CORAGEM à
    esquerda da prancheta (fora da barra) e o pé volta a pisar no limite da linha, sem passar;
  * "manda": cartão final com a perna apoiada, barra e seta lado a lado na mesma altura, no meio
    da barra (não cheia: nada de linha de chegada).
Nenhum exame de imagem simulado, nenhum implante de modelo comercial, nenhum número na tela. Os rótulos
nomeiam peças (FIXAÇÃO, CALO ÓSSEO, RESISTÊNCIA, CARGA, RAIO-X...); frase que a legenda já diz no mesmo
instante não vira chip ("conforme o osso evolui" = os degraus; "pode comprometer" = vermelho + alerta).
Todo texto desenhado está em ep["tela"] (o render recusa o vídeo se não estiver). A cena é PRESA ao
roteiro pelas palavras-âncora (ANCORAS): roteiro sem elas = KeyError, não vídeo torto.
"""
import math

import skia

from .cf_alongamento import (ACO, ACO_ESC, ACO_HL, CX, F_BLACK, F_SEMI, NOVO, NOVO_G, OSSO_B, OSSO_C, OSSO_L,
                             OURO, PELE, VERMELHO, W, Y_BASE, Y_TOPO, C, brilhos, clamp, e_back, e_in_back,
                             e_inout, e_out, fundo, larg_texto, lerp, lerpc, paint, path_osso_inf, path_osso_sup,
                             porca, prog, texto)
from .cf_comum import capa, carimbo as carimbo_ouro, fazer_render, interface, selo_como_funciona
from .cf_fratura_cola import _vao, _zig

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "pisar1": ("pisar", 1, False), "data": ("data", 1, False), "fixa": ("fixa", 1, False),
    "fixacao": ("fixação", 1, False), "colou": ("colou", 1, False), "calo": ("calo", 1, False),
    "resistencia": ("resistência", 1, False), "carga1": ("carga", 1, False),
    "progressivo": ("progressivo", 1, False), "conforme": ("conforme", 1, False), "evolui": ("evolui", 1, False),
    "pisar2": ("pisar", 2, False), "dose": ("dose", 1, False), "avisa": ("avisa", 1, False), "necessario": ("necessário", 1, False),
    "repouso": ("repouso", 1, False), "enfraquece": ("enfraquece", 1, False), "carga2": ("carga", 2, False),
    "alem": ("além", 1, False), "comprometer": ("comprometer", 1, False), "resultado": ("resultado", 1, False),
    "quem": ("quem", 1, False), "equipe": ("equipe", 1, False), "raio": ("raio", 1, True),
    "coragem": ("coragem", 1, False), "manda": ("manda", 1, False),
}
DESTAQUE = {"pisar", "data", "fixa", "fixação", "colou", "calo", "resistência", "carga", "progressivo",
            "evolui", "dose", "liberada", "avisa", "necessário", "repouso", "enfraquece", "além",
            "comprometer", "equipe", "raio-x", "coragem"}

# ------------------------------------------------------------------ textos de tela (todos em ep["tela"])
T_INTERROG = "?"
T_DATA = "NÃO TEM DATA FIXA"
T_FIX = "FIXAÇÃO"
T_COLOU = "QUANTO O OSSO COLOU"
T_CALO = "CALO ÓSSEO"
T_RESIST = "RESISTÊNCIA"
T_CARGA = "CARGA"
T_PROG = "PROGRESSIVO"
T_DOSE = "NA DOSE LIBERADA"
T_AVISA, T_ESTIMULO = "AVISA O OSSO", "ESTÍMULO MECÂNICO"
T_NECESS = "ELE É NECESSÁRIO"
T_REPOUSO, T_ENFRAQ = "REPOUSO DEMAIS", "ENFRAQUECE"
T_ALEM = "ALÉM DA LIBERADA"
T_EQUIPE, T_CONSOL = "QUEM LIBERA É A EQUIPE", "CONSOLIDAÇÃO"
T_RAIO = "RAIO-X"
T_CORAGEM = "NÃO A CORAGEM"

FUNDO_CARTAO = "#0B1824"
AZUL = "#9CC9FF"
APAGADO_C, APAGADO_B = "#8F989D", "#6C767C"   # osso "desbotado" (perde cor e contraste, segue opaco)

# ------------------------------------------------------------------ geometria (mundo = coordenadas do piloto)
YF = 760                                       # linha da fratura (a mesma do cf_fratura_cola: _vao usa ela)
GAP = 16                                       # o vão fino da fratura (o calo o preenche)
YM = YF + GAP / 2
H2 = 64                                        # meia largura da diáfise (HASTE do piloto / 2)
Y_SOLA = 1290                                  # sola do pé apoiado
Y_PISO = 1318                                  # linha do piso (base da plataforma)
X_SETA_M = CX + 300                            # a seta CARGA desce sobre o antepé
JAN0, JAN1 = 222, 1236                         # janela da cena (abaixo do selo, acima da legenda)
BANDA0, BANDA1 = 26, 30


def _uniao(a, b):
    return skia.Op(a, b, skia.PathOp.kUnion_PathOp)


OSSO = _uniao(path_osso_sup(Y_TOPO, YF + 2), path_osso_inf(YF - 2, Y_BASE))
VAO = _vao(GAP)
ZIG0, ZIG1 = _zig(YF), _zig(YF + GAP)


def _perna_pe():
    """Contorno da perna do piloto (cf_alongamento.perna com yb = Y_BASE) que, no tornozelo, segue
    para um pé simples de perfil (calcanhar atrás, dedos para a direita), sola reta."""
    L = Y_BASE - (Y_TOPO - 50)

    def y(f):
        return Y_TOPO - 50 + L * f
    p = skia.Path()
    p.moveTo(CX - 150, y(0.0))
    p.cubicTo(CX - 168, y(0.10), CX - 200, y(0.22), CX - 196, y(0.36))
    p.cubicTo(CX - 192, y(0.52), CX - 140, y(0.66), CX - 112, y(0.80))
    p.cubicTo(CX - 104, 1040, CX - 100, 1112, CX - 106, 1168)             # tendão (atrás)
    p.cubicTo(CX - 110, 1200, CX - 138, 1218, CX - 136, 1254)             # calcanhar
    p.cubicTo(CX - 134, 1282, CX - 114, Y_SOLA, CX - 86, Y_SOLA)
    p.lineTo(CX + 378, Y_SOLA)                                            # sola
    p.cubicTo(CX + 424, Y_SOLA, CX + 452, 1282, CX + 450, 1262)           # ponta dos dedos
    p.cubicTo(CX + 448, 1240, CX + 428, 1231, CX + 398, 1227)
    p.cubicTo(CX + 330, 1217, CX + 252, 1199, CX + 192, 1176)             # peito do pé
    p.cubicTo(CX + 142, 1156, CX + 112, 1128, CX + 106, 1088)             # tornozelo (frente)
    p.cubicTo(CX + 102, 1048, CX + 104, 1010, CX + 112, y(0.80))
    p.cubicTo(CX + 132, y(0.64), CX + 176, y(0.50), CX + 172, y(0.34))
    p.cubicTo(CX + 168, y(0.20), CX + 152, y(0.08), CX + 140, y(0.0))
    p.close()
    return p


PERNA = _perna_pe()


def _dorso(x):
    """Altura do peito do pé (borda de cima do contorno) na abscissa x do mundo."""
    y = 1150.0
    while y < Y_SOLA and not PERNA.contains(x, y):
        y += 0.5
    return y


Y_DORSO = _dorso(X_SETA_M)

# ------------------------------------------------------------------ câmera (mundo -> tela)
CAM_CAPA = (420.0, 757.0, 0.80, 770.0)         # (x na tela de CX, y na tela do foco, escala, foco no mundo)
CAM_LARGO = (330.0, 757.0, 0.80, 770.0)
CAM_PERTO = (392.0, 768.0, 1.30, YM)


def camera(t, T):
    px, py, s, fo = CAM_CAPA
    for (a, b), alvo in (((T["data"] - 0.25, T["data"] + 0.35), CAM_LARGO),
                         ((T["fixacao"] - 0.2, T["fixacao"] + 0.55), CAM_PERTO),
                         ((T["resistencia"] + 0.45, T["carga1"] + 0.12), CAM_LARGO)):
        k = e_inout(prog(t, a, b))
        px, py, s, fo = lerp(px, alvo[0], k), lerp(py, alvo[1], k), lerp(s, alvo[2], k), lerp(fo, alvo[3], k)
    tremor = 0.0
    for t0, f in ((T["fixa"], 6), (T["necessario"], 4), (T["comprometer"], 4), (T["coragem"], 6)):
        kk = t - t0
        if 0 <= kk < 0.35:
            tremor += f * math.sin(kk * 70) * (1 - kk / 0.35)
    return px + tremor, py, s, fo


def na_tela(cam, x, y):
    px, py, s, fo = cam
    return px + (x - CX) * s, py + (y - fo) * s


# medidor (tela): a base da barra fica na altura da ponta da seta com o pé apoiado (câmera larga)
X_SETA = na_tela(CAM_LARGO, X_SETA_M, 0)[0]
Y_BASE_MED = na_tela(CAM_LARGO, 0, Y_DORSO)[1]
BX, BW, BTOPO = 928, 58, 508
HB = Y_BASE_MED - BTOPO
R1, R2, R3, R_ALEM = 0.22, 0.36, 0.50, 0.70    # níveis do desenho (NÃO vão para a tela)


# ------------------------------------------------------------------ estado (tudo a partir das palavras)
def _passos(t, t0, t1, P, A):
    """Pisadas: o pé fica apoiado no começo de cada ciclo e sobe/desce no resto. Termina apoiado."""
    if t1 <= t0:
        return 0.0
    n = int((t1 - t0) / P)
    if n < 1 or t <= t0 or t >= t0 + n * P:
        return 0.0
    u = ((t - t0) / P) % 1.0
    return A * math.sin(math.pi * clamp((u - 0.38) / 0.62)) ** 1.3


def _pousos(t0, t1, P):
    n = int((t1 - t0) / P)
    return [t0 + k * P for k in range(1, n + 1)]


def janelas(T):
    """Trechos de pisada: (início, fim, período, altura)."""
    return {"leve": (T["progressivo"] - 0.05, T["conforme"] - 0.05, 0.42, 16.0),
            # começa no "Pisar" e o 2º pouso cai exatamente em "avisa" (a 1ª onda sai na palavra)
            "dose": (T["pisar2"], T["repouso"] - 0.1, (T["avisa"] - T["pisar2"]) / 2, 34.0),
            "fim": (T["coragem"] + 0.05, T["manda"] - 0.55, 0.6, 22.0)}


def levanta(t, T):
    """Quanto o pé (e a perna) está acima do apoio, em px do mundo."""
    l = 150 + 5 * math.sin(t * 2.4)                                               # capa: parado no ar
    l = lerp(l, 62 + 3 * math.sin(t * 2.4), e_inout(prog(t, T["pisar1"] - 0.05, T["pisar1"] + 0.45)))
    l = lerp(l, 0.0, e_inout(prog(t, T["carga1"] - 0.1, T["carga1"] + 0.28)))      # encosta na plataforma
    J = janelas(T)
    for chave in ("leve", "dose"):
        l += _passos(t, *J[chave])
    l = lerp(l, 80.0, e_inout(prog(t, T["repouso"], T["repouso"] + 0.45)))           # repouso: no ar, parado
    l = lerp(l, 0.0, e_inout(prog(t, T["carga2"] - 0.15, T["carga2"] + 0.18)))
    return l + _passos(t, *J["fim"])          # "coragem": volta a pisar no limite (depois do lerp do "carga")


def nivel_barra(t, T):
    r = R1 * e_inout(prog(t, T["resistencia"], T["carga1"] + 0.25))              # enche devagar
    r = lerp(r, R2, e_out(prog(t, T["conforme"], T["conforme"] + 0.22)))          # degrau 1
    r = lerp(r, R3, e_out(prog(t, T["evolui"], T["evolui"] + 0.22)))              # degrau 2
    return r


def nivel_seta(t, T):
    c = R1 * e_out(prog(t, T["carga1"] + 0.12, T["carga1"] + 0.5))
    c = lerp(c, R2, e_out(prog(t, T["conforme"] + 0.34, T["conforme"] + 0.6)))
    c = lerp(c, R3, e_out(prog(t, T["evolui"] + 0.34, T["evolui"] + 0.6)))
    c = lerp(c, R_ALEM, e_out(prog(t, T["alem"] + 0.02, T["alem"] + 0.5)))
    c = lerp(c, R3, e_inout(prog(t, T["resultado"] + 0.45, T["resultado"] + 0.9)))
    return c


def alfa_seta(t, T):
    a = prog(t, T["carga1"] + 0.08, T["carga1"] + 0.2)
    a *= 1 - prog(t, T["repouso"] + 0.05, T["repouso"] + 0.4) * (1 - prog(t, T["carga2"] + 0.0, T["carga2"] + 0.25))
    return a


def apagado(t, T):
    return e_inout(prog(t, T["enfraquece"] - 0.05, T["enfraquece"] + 0.55)) * (
        1 - e_inout(prog(t, T["carga2"] - 0.1, T["carga2"] + 0.3)))


def duro(t, T):
    """O dourado do calo puxa para o marfim enquanto a barra sobe (sem completar)."""
    return 0.62 * clamp(nivel_barra(t, T) / R3)


def ondas(T):
    """Instantes das pisadas que mandam onda (de "avisa" até antes de "repouso")."""
    t0, t1, P, _ = janelas(T)["dose"]
    return [x for x in _pousos(t0, t1, P) if T["avisa"] - 0.12 <= x < T["repouso"] - 0.25]


DUR_ONDA = 0.62


def pulso_calo(t, T):
    p = 0.0
    for x in ondas(T):
        k = t - (x + DUR_ONDA)
        if k >= 0:
            p += math.exp(-k * 5.5)
    return clamp(p)


# ------------------------------------------------------------------ utilidades de desenho
def ponta(cv, x, y, ang, tam, cor, a):
    p = skia.Path()
    p.moveTo(x + tam * math.cos(ang), y + tam * math.sin(ang))
    p.lineTo(x + tam * 0.75 * math.cos(ang + 2.45), y + tam * 0.75 * math.sin(ang + 2.45))
    p.lineTo(x + tam * 0.75 * math.cos(ang - 2.45), y + tam * 0.75 * math.sin(ang - 2.45))
    p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))


def chip(cv, s, x, y, cor, a, tam=40, borda=None, alinh="centro"):
    """Rótulo solto (sem ponteiro); y = linha de base. `alinh`: centro (x = meio), esq (x = borda
    esquerda da caixa) ou dir (x = borda direita da caixa). (cópia do cf_pe_virado, com alinhamento)"""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    x0 = {"centro": x - lw / 2 - 24, "esq": x, "dir": x - lw - 48}[alinh]
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y - tam * 1.05, x0 + lw + 48, y + tam * 0.34), 16, 16)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(220 * a)))
    cv.drawRRect(rr, paint(borda or cor, int(255 * a), "stroke", 3))
    cv.drawString(s, x0 + 24, y, f, paint(cor, int(255 * a)))


def etiqueta(cv, s, x, y, alvo, cor, a, tam=36):
    """Rótulo com linha-guia: (x, y) = borda esquerda da caixa e linha de base; `alvo` = ponto
    apontado. (cópia do cf_pseudartrose, com entrada deslizando)"""
    if a <= 0:
        return
    x += 26 * (1 - e_out(clamp(a)))
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    if alvo is not None:
        cv.drawLine(alvo[0], alvo[1], x, y - tam * 0.36, paint(FUNDO_CARTAO, int(150 * a), "stroke", 6))
        cv.drawLine(alvo[0], alvo[1], x, y - tam * 0.36, paint(cor, int(220 * a), "stroke", 2.5))
        cv.drawCircle(alvo[0], alvo[1], 7.5, paint(FUNDO_CARTAO, int(200 * a)))
        cv.drawCircle(alvo[0], alvo[1], 6, paint(cor, int(255 * a)))
    rr = skia.RRect.MakeRectXY(skia.Rect(x, y - tam * 1.08, x + lw + 30, y + tam * 0.32), 14, 14)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(225 * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 2.5))
    cv.drawString(s, x + 15, y, f, paint(cor, int(255 * a)))


def carimbo_vermelho(cv, s, x, y, rot, t0, t, dur=1.9, tam=54):
    """O carimbo vermelho do piloto com tamanho ajustável (cópia do cf_gesso_placa)."""
    k = t - t0
    if k < 0 or k > dur:
        return
    esc = lerp(1.9, 1.0, e_out(clamp(k / 0.16))); a = clamp(k / 0.08) * (1 - prog(k, dur - 0.35, dur))
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(esc, esc)
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 24, -tam, lw / 2 + 24, tam * 0.36), 12, 12)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(205 * a))); cv.drawRRect(rr, paint(VERMELHO, int(255 * a), "stroke", 7))
    cv.drawString(s, -lw / 2, 0, f, paint(VERMELHO, int(255 * a)))
    cv.restore()


def tique(cv, x, y, pr, cor, a, esc=1.0):
    """Tique em 2 traços (pr 0..1). (cópia do cf_pseudartrose)"""
    if pr <= 0 or a <= 0:
        return
    p = skia.Path(); p.moveTo(x, y)
    p.lineTo(x + 12 * esc * min(1, pr * 2), y + 12 * esc * min(1, pr * 2))
    if pr > 0.5:
        q = (pr - 0.5) * 2
        p.lineTo(x + (12 + 22 * q) * esc, y + (12 - 30 * q) * esc)
    cv.drawPath(p, paint(cor, int(255 * a), "stroke", 7 * esc))


def tracejado(cv, x0, y0, x1, y1, cor, a, larg=5, traco=18, vazio=12, fase=0.0):
    if a <= 0:
        return
    p = paint(cor, int(255 * a), "stroke", larg)
    p.setPathEffect(skia.DashPathEffect.Make([traco, vazio], fase))
    cv.drawLine(x0, y0, x1, y1, p)


# ------------------------------------------------------------------ perna, osso, placa (mundo)
def pele(cv, alfa):
    """A pele do piloto (translúcida, só contorno e véu) com o topo dissolvendo no fundo."""
    if alfa <= 0:
        return
    b = PERNA.computeTightBounds()
    sh = skia.GradientShader.MakeLinear([skia.Point(CX - 200, 0), skia.Point(CX + 180, 0)],
                                        [C(PELE, int(85 * alfa)), C(PELE, int(25 * alfa)), C(PELE, int(70 * alfa))],
                                        [0.0, 0.5, 1.0])
    caixa = skia.Rect(b.left() - 40, b.top() - 40, b.right() + 40, b.bottom() + 40)
    cv.saveLayer(caixa, None)
    cv.drawPath(PERNA, paint(PELE, 255, shader=sh))
    cv.drawPath(PERNA, paint(PELE, int(70 * alfa), "stroke", 14, blur=10))
    cv.drawPath(PERNA, paint(PELE, int(190 * alfa), "stroke", 3))
    masc = skia.Paint(AntiAlias=True)
    masc.setShader(skia.GradientShader.MakeLinear([skia.Point(0, b.top()), skia.Point(0, b.top() + 120)],
                                                  [skia.ColorSetARGB(0, 0, 0, 0), skia.ColorSetARGB(255, 0, 0, 0)]))
    masc.setBlendMode(skia.BlendMode.kDstIn)
    cv.drawRect(caixa, masc)
    cv.restore()


def osso(cv, t, T):
    """Osso longo marfim OPACO com o vão fino da fratura; entra de cima para baixo em "fixação"."""
    k = e_inout(prog(t, T["fixacao"] - 0.05, T["fixacao"] + 0.45))
    if k <= 0:
        return
    ap = apagado(t, T)
    cc = lerpc(OSSO_C, APAGADO_C, 0.75 * ap); cb = lerpc(OSSO_B, APAGADO_B, 0.75 * ap)
    sh = skia.GradientShader.MakeLinear([skia.Point(CX - 140, 0), skia.Point(CX + 140, 0)],
                                        [C(cb), C(cc), C(cc), C(cb)], [0.0, 0.42, 0.58, 1.0])
    y_fim = lerp(Y_TOPO - 40, Y_BASE + 60, k)
    cv.save()
    cv.clipRect(skia.Rect(0, Y_TOPO - 60, W * 2, y_fim))
    cv.clipPath(VAO, skia.ClipOp.kDifference, True)
    cv.drawPath(OSSO, paint("#000000", 70, blur=14))
    cv.drawPath(OSSO, paint(cc, shader=sh))
    cv.drawPath(OSSO, paint(OSSO_L, int(150 * (1 - 0.6 * ap)), "stroke", 2.5))
    for z in (ZIG0, ZIG1):                                          # bordas da fratura (o "risco")
        p = skia.Path(); p.moveTo(*z[0])
        for q in z[1:]:
            p.lineTo(*q)
        cv.save(); cv.clipPath(OSSO, skia.ClipOp.kIntersect, True)
        cv.drawPath(p, paint(OSSO_L, int(200 * (1 - 0.6 * ap)), "stroke", 3))
        cv.restore()
    cv.restore()
    if k < 1:                                                       # a borda que desenha o osso
        cv.drawLine(CX - 150, y_fim, CX + 150, y_fim, paint("#FFF4CF", int(200 * (1 - k)), "stroke", 8, blur=6))
    # "necessário": o contorno do osso acende por um instante
    kk = t - T["necessario"]
    if 0 <= kk < 1.1:
        g = math.sin(math.pi * clamp(kk / 1.1))
        cv.drawPath(OSSO, paint(NOVO_G, int(170 * g), "stroke", 14, blur=9))
        cv.drawPath(OSSO, paint("#FFE08A", int(230 * g), "stroke", 3.5))


def calo(cv, t, T):
    """Osso novo dourado no vão, na MESMA largura da diáfise; puxa para o marfim com a barra."""
    k = prog(t, T["calo"] - 0.05, T["calo"] + 0.4)
    if k <= 0:
        return
    ap = apagado(t, T)
    cor = lerpc(lerpc(NOVO, OSSO_C, duro(t, T)), APAGADO_C, 0.75 * ap)
    pul = pulso_calo(t, T)
    brilho = max(1 - prog(t, T["calo"] + 0.5, T["calo"] + 1.6), 0.25 * (1 - duro(t, T)), pul) * (1 - ap)
    if brilho > 0.01:
        cv.drawRect(skia.Rect(CX - H2 - 26, YF - 22, CX + H2 + 26, YF + GAP + 22),
                    paint(NOVO_G, int(170 * brilho), blur=20 + 10 * pul))
    cv.save()
    cv.clipRect(skia.Rect(CX - H2 + 1, YF - 30, lerp(CX - H2 + 1, CX + H2 - 1, e_out(k)), YF + GAP + 30))
    cv.drawPath(VAO, paint(cor))
    if pul > 0.02:
        cv.drawPath(VAO, paint("#FFF4CF", int(200 * pul)))
    cv.restore()


FUROS = (-136, -68, 68, 136)


def placa(cv, t, T):
    """Placa azul-aço com 4 furos (genérica) cruzando a fratura; cabeças douradas uma a uma
    (desenho do cf_gesso_placa)."""
    k = prog(t, T["fixacao"] + 0.05, T["fixacao"] + 0.45)
    if k <= 0:
        return
    dx = 720 * (1 - e_out(k))
    y0, y1 = YM - 180, YM + 180
    cv.save(); cv.translate(dx, 0)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(CX - 19, y0 + 7, CX + 29, y1 + 7), 22, 22), paint("#000000", 95, blur=7))
    rr = skia.RRect.MakeRectXY(skia.Rect(CX - 24, y0, CX + 24, y1), 22, 22)
    sh = skia.GradientShader.MakeLinear([skia.Point(CX - 24, 0), skia.Point(CX + 24, 0)],
                                        [skia.ColorSetRGB(0x7D, 0x90, 0xA4), skia.ColorSetRGB(0xC2, 0xD2, 0xE1),
                                         skia.ColorSetRGB(0xA9, 0xBC, 0xCF), skia.ColorSetRGB(0x6E, 0x82, 0x96)],
                                        [0.0, 0.38, 0.62, 1.0])
    cv.drawRRect(rr, paint(ACO, shader=sh))
    cv.drawRRect(rr, paint(ACO_ESC, 255, "stroke", 2.5))
    cv.drawLine(CX - 12, y0 + 22, CX - 12, y1 - 22, paint(ACO_HL, 120, "stroke", 2.5))
    for i, d in enumerate(FUROS):
        y = YM + d
        cv.drawCircle(CX, y, 11, paint("#44566A"))
        cv.drawCircle(CX, y, 11, paint("#2E3A46", 255, "stroke", 2))
        t_i = T["fixacao"] + 0.55 + 0.17 * i
        kk = e_back(prog(t, t_i, t_i + 0.22)) if t >= t_i else 0.0
        if kk > 0:
            cv.save(); cv.translate(CX, y); cv.scale(kk * 0.95, kk * 1.45)
            porca(cv, 0, 0, 30, 1.0)
            cv.restore()
            cv.drawCircle(CX, y, 4.2 * kk, paint("#6E4E0E"))
            if 0 <= t - t_i < 0.5:
                q = (t - t_i) / 0.5
                cv.drawCircle(CX, y, lerp(14, 42, e_out(q)), paint(OURO, int(200 * (1 - q)), "stroke", 3))
    cv.restore()


def onda(cv, t, t0):
    """Onda dourada em ARCO (não anel) subindo do tornozelo até o calo."""
    u = (t - t0) / DUR_ONDA
    if u < 0 or u > 1.25:
        return
    for j in range(3):                                   # três arcos em fila, como um sinal subindo
        uu = (u - 0.1 * j) / 1.0
        if uu < 0 or uu > 1:
            continue
        yy = lerp(1200, YM + 60, e_inout(uu)) + 34 * j
        rx = lerp(96, 70, uu) - 10 * j; ry = lerp(62, 48, uu) - 6 * j
        a = math.sin(math.pi * clamp(uu)) ** 0.7 * (1 - 0.28 * j)
        r = skia.Rect(CX - rx, yy - ry, CX + rx, yy + ry)
        cv.drawArc(r, 214, 112, False, paint("#000000", int(70 * a), "stroke", 14, blur=4))
        cv.drawArc(r, 214, 112, False, paint(NOVO_G, int(170 * a), "stroke", 22, blur=9))
        cv.drawArc(r, 214, 112, False, paint("#FFE08A", int(255 * a), "stroke", 8))


def plataforma(cv, t, T):
    """Linha do piso (desde a capa) e a plataforma que sobe dela em "carga"."""
    sh = skia.GradientShader.MakeLinear([skia.Point(CX - 520, 0), skia.Point(CX + 820, 0)],
                                        [C("#FFFFFF", 0), C("#FFFFFF", 90), C("#FFFFFF", 90), C("#FFFFFF", 0)],
                                        [0.0, 0.2, 0.8, 1.0])
    cv.drawLine(CX - 520, Y_PISO, CX + 820, Y_PISO, paint("#FFFFFF", 255, "stroke", 3, shader=sh))
    k = prog(t, T["carga1"] - 0.3, T["carga1"] + 0.05)
    if k <= 0:
        return
    dy = 22 * (1 - e_out(k))
    rr = skia.RRect.MakeRectXY(skia.Rect(CX - 210, Y_SOLA + dy, CX + 520, Y_PISO), 10, 10)
    shp = skia.GradientShader.MakeLinear([skia.Point(0, Y_SOLA), skia.Point(0, Y_PISO)],
                                         [C("#B9C8D6", int(255 * k)), C("#5E7186", int(255 * k))])
    cv.drawRRect(rr, paint(ACO, shader=shp))
    cv.drawLine(CX - 200, Y_SOLA + dy + 2, CX + 510, Y_SOLA + dy + 2, paint(ACO_HL, int(200 * k), "stroke", 2.5))


def sombra_pe(cv, l):
    a = 0.3 + 0.7 * clamp(1 - l / 200)
    enc = 1 - 0.25 * clamp(l / 150)
    cv.drawOval(skia.Rect(CX + 155 - 320 * enc, Y_SOLA - 7, CX + 155 + 320 * enc, Y_SOLA + 15),
                paint("#000000", int(120 * a), blur=8 + l * 0.12))


def pousos_todos(T):
    J = janelas(T)
    ev = [T["carga1"] + 0.18, T["carga2"] + 0.12]
    for chave in ("dose", "fim"):
        ev += _pousos(J[chave][0], J[chave][1], J[chave][2])
    return ev


def impacto(cv, t, T):
    """Pisada: um anel achatado e curto na plataforma, embaixo do pé (sem números, só o toque)."""
    for x in pousos_todos(T):
        k = t - x
        if 0 <= k < 0.45:
            q = k / 0.45
            rx = lerp(180, 330, e_out(q)); ry = rx * 0.09
            cv.drawOval(skia.Rect(CX + 150 - rx, Y_SOLA - ry, CX + 150 + rx, Y_SOLA + ry),
                        paint("#E6EEF6", int(150 * (1 - q)), "stroke", 4, blur=2))


def mundo(cv, t, T):
    l = levanta(t, T)
    plataforma(cv, t, T)
    sombra_pe(cv, l)
    impacto(cv, t, T)
    cv.save(); cv.translate(0, -l)
    pele(cv, 1.0)
    osso(cv, t, T)
    calo(cv, t, T)
    placa(cv, t, T)
    for x in ondas(T):
        onda(cv, t, x)
    cv.restore()
    brilhos(cv, CX, YM - l, t, T["calo"] + 0.3, n=12, raio=170)


# ------------------------------------------------------------------ medidor (tela): barra, linha, seta
def barra(cv, t, T, a_extra):
    k = prog(t, T["colou"] - 0.05, T["colou"] + 0.35)
    if k <= 0:
        return
    alt = HB * e_out(k)                                                # sem passar do topo (não corta o rótulo)
    a = clamp(k * 3)
    y_top = Y_BASE_MED - alt
    rr = skia.RRect.MakeRectXY(skia.Rect(BX - BW / 2, y_top, BX + BW / 2, Y_BASE_MED), 20, 20)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(170 * a)))
    r = nivel_barra(t, T)
    if r > 0.002:
        h = HB * r
        cv.save(); cv.clipRRect(rr, True)
        sh = skia.GradientShader.MakeLinear([skia.Point(BX - BW / 2, 0), skia.Point(BX + BW / 2, 0)],
                                            [C("#D99A22"), C("#FFD36B"), C(OURO), C("#C88A1A")], [0.0, 0.35, 0.6, 1.0])
        cv.drawRect(skia.Rect(BX - BW / 2, Y_BASE_MED - h, BX + BW / 2, Y_BASE_MED), paint(OURO, int(255 * a), shader=sh))
        cv.drawLine(BX - BW / 2 + 4, Y_BASE_MED - h, BX + BW / 2 - 4, Y_BASE_MED - h, paint("#FFF4CF", int(230 * a), "stroke", 3))
        cv.restore()
        for t0 in (T["conforme"], T["evolui"]):                       # clique do degrau: brilho rápido
            kk = t - t0
            if 0 <= kk < 0.6:
                cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(BX - BW / 2 - 8, Y_BASE_MED - h - 8, BX + BW / 2 + 8,
                                                             Y_BASE_MED + 8), 24, 24),
                             paint(NOVO_G, int(150 * (1 - kk / 0.6)), blur=14))
    cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 4))
    # "?" dentro da barra vazia
    aq = prog(t, T["colou"] + 0.15, T["colou"] + 0.45) * (1 - prog(t, T["resistencia"] - 0.1, T["resistencia"] + 0.3))
    if aq > 0:
        pul = 1 + 0.12 * math.sin((t - T["colou"]) * 7)
        cv.save(); cv.translate(BX, Y_BASE_MED - HB * 0.55); cv.scale(pul, pul)
        texto(cv, T_INTERROG, 0, 22, F_BLACK, 64, OURO, int(255 * aq), contorno=8)
        cv.restore()
    # rótulo da barra: QUANTO O OSSO COLOU -> RESISTÊNCIA
    a1 = prog(t, T["colou"] + 0.1, T["colou"] + 0.4) * (1 - prog(t, T["resistencia"] - 0.05, T["resistencia"] + 0.2))
    texto(cv, T_COLOU, 1030 - larg_texto(T_COLOU, F_BLACK, 32), BTOPO - 26, F_BLACK, 32, OURO, int(255 * a1),
          centro=False, contorno=8)
    a2 = prog(t, T["resistencia"], T["resistencia"] + 0.3) * a_extra
    texto(cv, T_RESIST, 1030 - larg_texto(T_RESIST, F_BLACK, 34), BTOPO - 26, F_BLACK, 34, OURO, int(255 * a2),
          centro=False, contorno=8)


def seta_carga(cv, x, y_cauda, y_ponta, a, y_linha, verm):
    """Seta azul-aço apontando para baixo (ponta no pé). O trecho acima de `y_linha` fica vermelho
    na medida de `verm`."""
    if a <= 0 or y_ponta - y_cauda < 6:
        return
    comp = y_ponta - y_cauda
    cab = min(48, comp * 0.55); hw = 32; sw = 12
    p = skia.Path()
    p.moveTo(x - sw, y_cauda); p.lineTo(x + sw, y_cauda); p.lineTo(x + sw, y_ponta - cab)
    p.lineTo(x + hw, y_ponta - cab); p.lineTo(x, y_ponta); p.lineTo(x - hw, y_ponta - cab)
    p.lineTo(x - sw, y_ponta - cab); p.close()
    cv.drawPath(p, paint("#000000", int(90 * a), blur=8))
    cv.drawPath(p, paint(FUNDO_CARTAO, int(230 * a), "stroke", 7))
    sh = skia.GradientShader.MakeLinear([skia.Point(x - hw, 0), skia.Point(x + hw, 0)],
                                        [skia.ColorSetRGB(0x7D, 0x90, 0xA4), skia.ColorSetRGB(0xD3, 0xDF, 0xEA),
                                         skia.ColorSetRGB(0x6E, 0x82, 0x96)], [0.0, 0.45, 1.0])
    pt = paint(ACO, int(255 * a), shader=sh)
    cv.drawPath(p, pt)
    if verm > 0 and y_cauda < y_linha:
        cv.save(); cv.clipRect(skia.Rect(x - 60, y_cauda - 10, x + 60, y_linha))
        cv.drawPath(p, paint(VERMELHO, int(150 * a * verm), "stroke", 18, blur=8))
        cv.drawPath(p, paint(VERMELHO, int(255 * a * verm)))
        cv.restore()


def medidor(cv, t, T, cam, a_extra):
    barra(cv, t, T, a_extra)
    a = alfa_seta(t, T)
    r = nivel_barra(t, T); c = nivel_seta(t, T)
    y_linha = Y_BASE_MED - HB * r
    # linha tracejada: sai da barra e vai até a seta (o teto da carga)
    k = e_out(prog(t, T["carga1"] + 0.2, T["carga1"] + 0.6))
    if k > 0:
        x0 = BX - BW / 2 - 6; x1 = lerp(x0, X_SETA - 46, k)
        brilho = 0.0
        if T["dose"] - 0.1 <= t < T["repouso"]:
            brilho = 0.35
            t0, t1, P, _ = janelas(T)["dose"]
            for x in [t0] + _pousos(t0, t1, P):
                kk = t - x
                if 0 <= kk < 0.45:
                    brilho = max(brilho, 1 - kk / 0.45)
        if brilho > 0:
            cv.drawLine(x0, y_linha, x1, y_linha, paint(NOVO_G, int(200 * brilho), "stroke", 16, blur=8))
        tracejado(cv, x0, y_linha, x1, y_linha, "#000000", 0.5, larg=9)
        tracejado(cv, x0, y_linha, x1, y_linha, OURO, 1.0, larg=5)
    # a seta: ponta no peito do pé (sobe junto quando o pé levanta), cauda no nível da carga
    l = levanta(t, T)
    _, y_ponta = na_tela(cam, X_SETA_M, Y_DORSO - l)
    y_ponta -= 4
    y_cauda = Y_BASE_MED - HB * c
    verm = prog(t, T["alem"] + 0.12, T["alem"] + 0.3) * (1 - prog(t, T["resultado"] + 0.45, T["resultado"] + 0.8))
    if c > 0:
        seta_carga(cv, X_SETA, min(y_cauda, y_ponta - 6), y_ponta, a, y_linha, verm)
    # rótulo CARGA ao lado da seta (acompanha o meio dela)
    a_c = prog(t, T["carga1"] + 0.25, T["carga1"] + 0.5) * a
    if a_c > 0 and c > 0:
        ym = (y_cauda + Y_BASE_MED) / 2
        chip(cv, T_CARGA, X_SETA + 46, ym + 16, "#FFFFFF", a_c, tam=34, borda=ACO, alinh="esq")
    return y_linha, y_cauda


# ------------------------------------------------------------------ calendário (só a grade)
def calendario(cv, t, T):
    t0 = T["data"]
    if t < t0 - 0.05:
        return
    entra = e_back(prog(t, t0 - 0.05, t0 + 0.35), 1.2)
    sai = e_in_back(prog(t, T["fixa"] + 0.55, T["fixa"] + 0.95))
    if sai >= 1:
        return
    x = lerp(1200, 612, entra) + 640 * sai
    y = 452
    w, h = 300, 292
    cv.save(); cv.translate(x, y); cv.rotate(3 * (1 - entra) - 6 * sai)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(6, 10, w + 6, h + 10), 18, 18), paint("#000000", 90, blur=12))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(0, 0, w, h), 18, 18), paint("#EEF3F8"))
    cv.save(); cv.clipRRect(skia.RRect.MakeRectXY(skia.Rect(0, 0, w, h), 18, 18), True)
    cv.drawRect(skia.Rect(0, 0, w, 58), paint(VERMELHO))
    cv.restore()
    for xx in (70, w - 70):                                           # argolas
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(xx - 7, -16, xx + 7, 18), 6, 6), paint("#5E7186"))

    def grade(alfa):
        for i in range(5):
            for j in range(7):
                gx = 22 + j * 37.5; gy = 76 + i * 41
                cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(gx, gy, gx + 30, gy + 33), 5, 5), paint("#C9D3DC", int(255 * alfa)))
    grade(1.0)
    # folhas virando para cima, rápido, até o carimbo
    if t < T["fixa"] + 0.05:
        k = (t - t0) * 6.5
        fase = k - math.floor(k)
        cv.save(); cv.translate(0, 58); cv.scale(1, 1 - e_inout(fase))
        cv.drawRect(skia.Rect(0, 0, w, h - 58), paint("#FFFFFF"))
        cv.translate(0, -58)
        grade(0.8)
        cv.restore()
        cv.drawLine(0, 58, w, 58, paint("#9AA8B5", 180, "stroke", 2))
    cv.restore()


# ------------------------------------------------------------------ prancheta (quem libera é a equipe)
PX0, PY0, PW, PH = 556, 268, 476, 226          # acima da barra: barra, linha e seta seguem à vista


def prancheta(cv, t, T):
    t0 = T["quem"]
    if t < t0:
        return 0.0
    entra = e_back(prog(t, t0, t0 + 0.45), 1.1)
    sai = e_in_back(prog(t, T["manda"] - 0.85, T["manda"] - 0.45))
    if sai >= 1:
        return 0.0
    dx = 560 * (1 - entra) + 620 * sai
    cv.save(); cv.translate(dx, 0)
    rr = skia.RRect.MakeRectXY(skia.Rect(PX0, PY0, PX0 + PW, PY0 + PH), 24, 24)
    cv.drawRRect(rr, paint("#000000", 110, blur=16))
    cv.drawRRect(rr, paint(FUNDO_CARTAO, 240))
    cv.drawRRect(rr, paint(OURO, 255, "stroke", 3))
    # prendedor da prancheta
    cx = PX0 + PW / 2
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(cx - 70, PY0 - 18, cx + 70, PY0 + 20), 10, 10), paint("#000000", 90, blur=6))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(cx - 66, PY0 - 22, cx + 66, PY0 + 16), 10, 10), paint(ACO))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(cx - 66, PY0 - 22, cx + 66, PY0 + 16), 10, 10), paint(ACO_ESC, 255, "stroke", 2.5))
    cv.drawCircle(cx, PY0 - 6, 7, paint(ACO_ESC))
    texto(cv, T_EQUIPE, cx, PY0 + 66, F_BLACK, 31, OURO)
    cv.drawLine(PX0 + 28, PY0 + 88, PX0 + PW - 28, PY0 + 88, paint(OURO, 110, "stroke", 2))
    for i, (s, t_ok) in enumerate(((T_FIX, T["equipe"] + 0.05), (T_CONSOL, T["raio"] + 0.75))):
        y = PY0 + 146 + i * 62
        bx = PX0 + 40
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(bx, y - 40, bx + 48, y + 8), 10, 10), paint("#13283A"))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(bx, y - 40, bx + 48, y + 8), 10, 10), paint(OURO, 255, "stroke", 3.5))
        ok = prog(t, t_ok, t_ok + 0.3)
        tique(cv, bx + 9, y - 18, e_out(ok), OURO, 1.0)
        if 0 <= t - t_ok < 0.6:
            kk = (t - t_ok) / 0.6
            cv.drawCircle(bx + 24, y - 16, lerp(20, 54, e_out(kk)), paint(OURO, int(200 * (1 - kk)), "stroke", 3))
        texto(cv, s, bx + 70, y - 2, F_BLACK, 36, "#FFFFFF", int(lerp(140, 255, ok)), centro=False)
    cv.restore()
    return clamp(entra) * (1 - sai)


# ------------------------------------------------------------------ visor do raio-X (esquemático)
def visor(cv, t, T, cam, l):
    """Quatro cantos + linha de varredura sobre o MESMO osso marfim (não é exame). Desce sobre o
    osso até a fratura e varre. (adaptado do cf_fratura_cola.visor, sem o texto de lá)"""
    t0 = T["raio"]
    a = prog(t, t0 - 0.15, t0 + 0.1) * (1 - prog(t, T["manda"] - 0.85, T["manda"] - 0.5))
    if a <= 0:
        return
    desce = e_inout(prog(t, t0 - 0.15, t0 + 0.35))
    yc = lerp(YM - 330, YM, desce) - l
    x0, y0 = na_tela(cam, CX - 150, yc - 230)
    x1, y1 = na_tela(cam, CX + 150, yc + 230)
    L = 44
    for (x, y, dx, dy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        cv.drawLine(x, y, x + dx * L, y, paint("#000000", int(120 * a), "stroke", 10))
        cv.drawLine(x, y, x, y + dy * L, paint("#000000", int(120 * a), "stroke", 10))
        cv.drawLine(x, y, x + dx * L, y, paint(OURO, int(255 * a), "stroke", 6))
        cv.drawLine(x, y, x, y + dy * L, paint(OURO, int(255 * a), "stroke", 6))
    k = prog(t, t0 + 0.35, t0 + 1.0)
    if 0 < k < 1:
        y = lerp(y0 + 10, y1 - 10, e_inout(k))
        cv.drawLine(x0 + 12, y, x1 - 12, y, paint(OURO, int(150 * a), "stroke", 14, blur=10))
        cv.drawLine(x0 + 12, y, x1 - 12, y, paint("#FFF4CF", int(255 * a), "stroke", 3))
    chip(cv, T_RAIO, (x0 + x1) / 2, y0 - 22, OURO, a, tam=32)


def brilhos_faixa(cv, x, y, t, t0, n=12, rx=330, ry=62):
    """Os brilhos do piloto (cf_alongamento.brilhos) abrindo numa faixa achatada ao longo do carimbo,
    para não subir no selo COMO FUNCIONA nem descer no topo do osso."""
    k = t - t0
    if k < 0 or k > 0.9:
        return
    for i in range(n):
        ang = i * 2 * math.pi / n + 0.3
        d = e_out(k / 0.9) * (0.6 + 0.4 * ((i * 37) % 10) / 10)
        a = int(255 * (1 - k / 0.9))
        px, py = x + rx * d * math.cos(ang), y + ry * d * math.sin(ang)
        s = 7 * (1 - k / 0.9) + 3
        p = skia.Path(); p.moveTo(px, py - s * 2); p.lineTo(px + s * 0.5, py - s * 0.5); p.lineTo(px + s * 2, py)
        p.lineTo(px + s * 0.5, py + s * 0.5); p.lineTo(px, py + s * 2); p.lineTo(px - s * 0.5, py + s * 0.5)
        p.lineTo(px - s * 2, py); p.lineTo(px - s * 0.5, py - s * 0.5); p.close()
        cv.drawPath(p, paint(OURO, a))


# ------------------------------------------------------------------ alerta (sem texto)
def triangulo(cv, x, y, esc, a):
    """Triângulo de alerta (cópia do cf_pe_virado), em escala; o "!" é desenho, não texto."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    p = skia.Path(); p.moveTo(0, -70); p.lineTo(80, 64); p.lineTo(-80, 64); p.close()
    pt = paint(VERMELHO, int(255 * a)); pt.setPathEffect(skia.CornerPathEffect.Make(18))
    gl = paint(VERMELHO, int(110 * a), blur=18); gl.setPathEffect(skia.CornerPathEffect.Make(18))
    cv.drawPath(p, gl); cv.drawPath(p, pt)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-9, -32, 9, 22), 9, 9), paint("#FFFFFF", int(255 * a)))
    cv.drawCircle(0, 43, 10, paint("#FFFFFF", int(255 * a)))
    cv.restore()


# ------------------------------------------------------------------ rótulos
def rotulos(cv, t, T, cam, y_linha, y_cauda):
    l = levanta(t, T)
    # "?" acima do pé parado no ar
    a = prog(t, T["pisar1"] + 0.3, T["pisar1"] + 0.55) * (1 - prog(t, T["fixacao"] - 0.35, T["fixacao"] - 0.1))
    if a > 0:
        x, y = na_tela(cam, CX + 330, Y_DORSO - 105 - l)
        pul = 1 + 0.1 * math.sin((t - T["pisar1"]) * 7)
        cv.save(); cv.translate(x, y); cv.scale(pul, pul)
        cv.drawCircle(0, -34, 62, paint(NOVO_G, int(60 * a), blur=18))
        texto(cv, T_INTERROG, 0, 0, F_BLACK, 112, OURO, int(255 * a), contorno=10)
        cv.restore()
    calendario(cv, t, T)
    carimbo_vermelho(cv, T_DATA, 740, 640, -7, T["fixa"] - 0.02, t, dur=T["fixacao"] - T["fixa"] - 0.05, tam=44)
    # fixação e calo (perto)
    a_perto = 1 - prog(t, T["resistencia"] + 0.35, T["resistencia"] + 0.6)
    etiqueta(cv, T_FIX, 556, 612, na_tela(cam, CX + 24, YM - 110 - l), OURO,
             prog(t, T["fixacao"] + 0.35, T["fixacao"] + 0.65) * a_perto, tam=38)
    etiqueta(cv, T_CALO, 556, 892, na_tela(cam, CX + H2 - 4, YM - l), OURO,
             prog(t, T["calo"] + 0.1, T["calo"] + 0.4) * a_perto, tam=38)
    # faixa de cima: progressivo (os degraus de "conforme o osso evolui" são o próprio medidor)
    chip(cv, T_PROG, 540, 312, "#FFFFFF",
         prog(t, T["progressivo"], T["progressivo"] + 0.25) * (1 - prog(t, T["conforme"] - 0.15, T["conforme"])),
         tam=42, borda=OURO)
    # a linha tracejada = a dose liberada: o nome fica encostado na própria linha
    a = prog(t, T["dose"], T["dose"] + 0.25) * (1 - prog(t, T["avisa"] + 0.25, T["avisa"] + 0.45))
    if a > 0:
        chip(cv, T_DOSE, 690, y_linha - 18, OURO, a, tam=32)
    # avisa o osso / estímulo mecânico
    a = prog(t, T["avisa"] + 0.1, T["avisa"] + 0.4) * (1 - prog(t, T["repouso"] - 0.15, T["repouso"] + 0.1))
    etiqueta(cv, T_AVISA, 480, 676, na_tela(cam, CX + H2 + 4, YM - l), OURO, a, tam=38)
    etiqueta(cv, T_ESTIMULO, 480, 740, None, "#FFFFFF", a * prog(t, T["avisa"] + 0.35, T["avisa"] + 0.6), tam=30)
    brilhos_faixa(cv, 540, 286, t, T["necessario"] + 0.05, ry=56)
    carimbo_ouro(cv, T_NECESS, 540, 298, -4, T["necessario"] - 0.02, t, dur=T["repouso"] - T["necessario"] - 0.1, tam=48)
    # repouso demais (à esquerda) / enfraquece
    a_rep = prog(t, T["repouso"], T["repouso"] + 0.25) * (1 - prog(t, T["carga2"] - 0.1, T["carga2"] + 0.15))
    chip(cv, T_REPOUSO, 44, 300, AZUL, a_rep, tam=40, alinh="esq")
    etiqueta(cv, T_ENFRAQ, 540, 650, na_tela(cam, CX + H2 - 6, 600 - l), "#C9D6E2",
             prog(t, T["enfraquece"], T["enfraquece"] + 0.25) * (1 - prog(t, T["carga2"] - 0.1, T["carga2"] + 0.15)),
             tam=38)
    # além da liberada (à direita, acima do trecho vermelho) + alerta
    a_alem = prog(t, T["alem"] + 0.15, T["alem"] + 0.4) * (1 - prog(t, T["resultado"] + 0.5, T["resultado"] + 0.8))
    chip(cv, T_ALEM, X_SETA + 100, y_cauda - 34, VERMELHO, a_alem, tam=34)
    k = prog(t, T["comprometer"], T["comprometer"] + 0.35)
    a_tri = clamp(k * 3) * (1 - prog(t, T["resultado"] + 0.5, T["resultado"] + 0.8))
    if a_tri > 0:
        ym = (y_cauda + y_linha) / 2
        triangulo(cv, X_SETA + 92, ym + 6, 0.5 * e_back(k), a_tri)


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    cam = camera(t, T)
    jan = skia.Rect(0, JAN0, W, JAN1)
    cv.save(); cv.clipRect(jan)
    cv.saveLayer(jan, None)
    px, py, s, fo = cam
    cv.save(); cv.translate(px, py); cv.scale(s, s); cv.translate(-CX, -fo)
    mundo(cv, t, T)
    cv.restore()
    for ya, yb, c0, c1 in ((JAN0, JAN0 + BANDA0, 0, 255), (JAN1 - BANDA1, JAN1, 255, 0)):
        masc = skia.Paint(AntiAlias=True)
        masc.setShader(skia.GradientShader.MakeLinear([skia.Point(0, ya), skia.Point(0, yb)],
                                                      [skia.ColorSetARGB(c0, 0, 0, 0), skia.ColorSetARGB(c1, 0, 0, 0)]))
        masc.setBlendMode(skia.BlendMode.kDstIn)
        cv.drawRect(skia.Rect(0, ya, W, yb), masc)
    cv.restore()
    cv.restore()

    l = levanta(t, T)
    visor(cv, t, T, cam, l)
    a_pr = 0.0
    if t >= T["quem"]:
        a_pr = clamp(prog(t, T["quem"], T["quem"] + 0.3)) * (1 - prog(t, T["manda"] - 0.85, T["manda"] - 0.5))
    y_linha, y_cauda = medidor(cv, t, T, cam, 1 - a_pr)
    rotulos(cv, t, T, cam, y_linha, y_cauda)
    prancheta(cv, t, T)
    carimbo_vermelho(cv, T_CORAGEM, 296, 322, -5, T["coragem"] - 0.02, t, dur=T["manda"] - T["coragem"] - 0.55, tam=46)

    capa(cv, t, T["fixacao"] - 0.35, ep["gancho"][0], ep["gancho"][1])
    selo_como_funciona(cv, prog(t, T["fixacao"] + 0.15, T["fixacao"] + 0.55) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface(cv, t, T, _rejunta(blocos), DESTAQUE)


# legenda: palavra de ligação nunca fecha um bloco (cópia do cf_gesso_placa, repetindo até assentar)
LIGA = {"o", "a", "os", "as", "um", "uma", "do", "da", "de", "e", "ou", "que", "por", "pra", "com", "no", "na",
        "numa", "é"}


def _rejunta(blocos):
    bl = [list(b) for b in blocos]
    for i in range(len(bl) - 1):
        while (len(bl[i]) > 1 and bl[i][-1]["w"].lower() in LIGA and not bl[i][-1]["fim_frase"]
               and not bl[i][-1]["virg"] and bl[i + 1][0]["w"].lower() != "manda"):
            bl[i + 1].insert(0, bl[i].pop())
    return bl


# ------------------------------------------------------------------ som e prévias
def sons(T):
    ev = [(T["pisar1"] - 0.05, "whoosh", 0.35), (T["pisar1"] + 0.4, "pop", 0.45),
          (T["data"] - 0.05, "whoosh", 0.45), (T["fixa"] - 0.02, "thump", 0.9), (T["fixa"] + 0.55, "whoosh", 0.4),
          (T["fixacao"] - 0.2, "whoosh", 0.4), (T["fixacao"] + 0.1, "shimmer", 0.3), (T["fixacao"] + 0.4, "ping", 0.6),
          (T["colou"], "pop", 0.55), (T["calo"] - 0.02, "shimmer", 0.85), (T["resistencia"] + 0.1, "crackle", 0.55),
          (T["resistencia"] + 0.45, "whoosh", 0.35), (T["carga1"] + 0.2, "thump", 0.5), (T["carga1"] + 0.3, "whoosh", 0.25),
          (T["progressivo"], "pop", 0.45),
          (T["conforme"], "click", 0.95), (T["conforme"] + 0.36, "click", 0.7), (T["conforme"] + 0.1, "ding", 0.25),
          (T["evolui"], "click", 0.95), (T["evolui"] + 0.36, "click", 0.7), (T["evolui"] + 0.1, "ding", 0.3),
          (T["avisa"], "shimmer", 0.45), (T["necessario"] - 0.02, "thump", 0.8), (T["necessario"] + 0.05, "shimmer", 0.6),
          (T["repouso"], "whoosh", 0.4), (T["enfraquece"], "whoosh", 0.22), (T["carga2"], "thump", 0.45),
          (T["alem"] + 0.05, "whoosh", 0.35), (T["alem"] + 0.3, "tick", 0.8), (T["comprometer"], "thump", 0.7),
          (T["resultado"] + 0.45, "whoosh", 0.3), (T["quem"], "whoosh", 0.45),
          (T["equipe"] + 0.05, "tick", 0.8), (T["equipe"] + 0.1, "ding", 0.35),
          (T["raio"] - 0.15, "whoosh", 0.35), (T["raio"] + 0.35, "shimmer", 0.4),
          (T["raio"] + 0.75, "tick", 0.8), (T["raio"] + 0.8, "ding", 0.4),
          (T["coragem"] - 0.02, "thump", 0.9), (T["manda"] - 0.85, "whoosh", 0.35),
          (T["manda"] + 0.05, "whoosh", 0.5)]
    ev += [(T["data"] + 0.08 + i / 6.5, "tick", 0.3) for i in range(int((T["fixa"] - T["data"]) * 6.5) + 1)]  # folhas
    ev += [(T["fixacao"] + 0.55 + 0.17 * i, "ping", 0.45) for i in range(4)]                                 # cabeças
    J = janelas(T)
    for chave, g in (("leve", 0.22), ("dose", 0.5), ("fim", 0.4)):
        ev += [(x, "tick", g) for x in _pousos(J[chave][0], J[chave][1], J[chave][2])]                     # pisadas
    ev += [(x + DUR_ONDA, "pop", 0.3) for x in ondas(T)]                                                     # calo responde
    return ev


def tempos_previa(T):
    # o "?" do "pisar" segue à vista no quadro do carimbo; o visor do raio-X segue à vista no do "coragem"
    return [0.3, T["fixa"] + 0.35, T["fixacao"] + 1.5, T["resistencia"] + 0.5, T["progressivo"] + 0.5,
            T["evolui"] + 0.65, T["dose"] + 0.45, T["necessario"] + 0.3, T["enfraquece"] + 0.6,
            T["comprometer"] + 0.45, T["coragem"] + 0.9, T["manda"] + 1.6]


# respiro maior antes da CTA: o carimbo NÃO A CORAGEM e o pé pisando no limite da linha ficam ~1,5 s,
# e a cena assenta no cartão final (barra e seta na mesma altura) antes do escurecimento da CTA.
render = fazer_render(quadro, ANCORAS, sons, tempos_previa, respiro_cta=2.2)
