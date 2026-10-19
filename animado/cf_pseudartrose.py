# -*- coding: utf-8 -*-
"""COMO FUNCIONA — "Cigarro atrasa o osso a colar?" (tabagismo e pseudartrose).

Mesmo estilo e mesmas peças das cenas aprovadas (osso marfim, vão da fratura com a geometria do
cf_fratura_cola, brilho dourado, arco pontilhado da "ponte", carimbo ouro, checklist, legenda
karaokê, CTA com aviãozinho). Storyboard e correções do verificador
(lote3_cf/cf_pseudartrose_storyboard.json) respeitados aqui:
  * Nada de calo "brotando das pontas": no vão só há brilho dourado ESPARSO na MESMA largura do
    osso e o arco pontilhado da ponte, que nasce na ponta de cima, desacelera e PARA NA METADE
    (o resto do caminho fica só tracejado em cinza: a ponte não fecha).
  * O vaso é a linha de VASO do cf_fratura_cola, em tubo esquemático com glóbulos; a nicotina o
    aperta numa cintura suave. Nada de sangue derramado; o cigarro é um bastão branco com ponta
    laranja, sem fumaça e sem brasa.
  * Tratamento: checklist de DOIS itens (estabilizar melhor / estimular o osso) + selo CASO A
    CASO. "Parar de fumar" é um cartão SEPARADO (outra fonte) e o vaso NÃO reabre na tela.
    Nenhum aparelho é desenhado; o arco não se completa e o vão não fecha (nada de antes/depois).
  * RISCO MAIOR em tom neutro: sem vermelho de alarme, sem X, sem dedo apontado.
Cena PRESA ao roteiro pelas palavras-âncora: roteiro sem elas = KeyError, não vídeo torto.
"""
import math

import skia

from .cf_alongamento import (CX, F_BLACK, F_SEMI, HASTE, NOVO_G, OSSO_C, OSSO_L, OURO, VASO, W, Y_BASE, Y_TOPO, C, brilhos,
                             clamp, e_back, e_in_back, e_inout, e_out, fundo, lerp, lerpc, paint, path_osso_inf,
                             path_osso_sup, prog, sombra_osso, texto)
from .cf_comum import capa, fazer_render, interface, selo_como_funciona
from .cf_fratura_cola import GAP, YF, _regiao_abaixo, _regiao_acima, _vao, _zig

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "cigarro": ("cigarro", 1, False),
    "atrasa": ("atrasa", 2, False),          # a RESPOSTA ("Atrasa."), não a pergunta
    "tripe": ("tripé", 1, False),
    "firmeza": ("firmeza", 1, False),
    "sangue": ("sangue", 1, False),
    "chegando": ("chegando", 1, False),
    "infeccao": ("infecção", 1, False),
    "nicotina": ("nicotina", 1, False),
    "aperta": ("aperta", 1, False),
    "menos": ("menos", 1, False),
    "pouco": ("pouco", 1, False),
    "lenta": ("lenta", 1, False),
    "ponte": ("ponte", 1, False),
    "mexe": ("mexe", 1, False),
    "falsa": ("falsa", 1, False),
    "pseudartrose": ("pseudartrose", 1, False),
    "risco": ("risco", 1, False),
    "caminho": ("caminho", 1, False),
    "estabilizar": ("estabilizar", 1, False),
    "estimular": ("estimular", 1, False),
    "parar": ("parar", 1, False),
    "diferenca": ("diferença", 1, False),
    "manda": ("manda", 1, False),
}
DESTAQUE = {"cigarro", "atrasa", "tripé", "firmeza", "sangue", "infecção", "nicotina", "vasos", "oxigênio",
            "lenta", "ponte", "mexe", "falsa", "junta", "pseudartrose", "risco", "caminho", "estabilizar",
            "estimular", "parar", "diferença"}

# ------------------------------------------------------------------ geometria e paleta
SY = 790                                  # âncora vertical da câmera na tela
PIVO = (CX, YF + GAP / 2)                 # centro do vão: a "dobradiça" da falsa junta
# união de verdade (o addPath do cf_fratura_cola deixa 2 traços horizontais no meio, escondidos lá pelo calo)
OSSO = skia.Op(path_osso_sup(Y_TOPO, YF + 4), path_osso_inf(YF - 4, Y_BASE), skia.PathOp.kUnion_PathOp)
Y_PE = OSSO.computeTightBounds().fBottom + GAP          # pé real do osso (a metade de baixo desce GAP)
AZUL = "#9CC9FF"
NEUTRO = "#C9D6E2"
GLOB = "#FF8A8F"
FUNDO_CARTAO = "#0B1824"
CANTO = (115, 262)                        # onde o cigarro fica "de olho" (canto superior esquerdo)
TRI_X, TRI_Y = 790, 335                   # centro do assento do tripé (tela)
X_LISTA = 470                             # coluna da direita: lista do tripé, rótulos, checklist
BX_VASO, S_VASO, FY_VASO = 270.0, 1.2, 930.0     # câmera no vaso: cintura em (401, 814) na tela, pé do osso em 1152
CIG_VASO = (770, 968, -8, 0.85)           # cigarro ao lado do vaso ampliado (tela)
Y_ROT_VASO = 852                          # linha de base das etiquetas do vaso (logo abaixo da lista)


# ------------------------------------------------------------------ câmera
def camera(t, T):
    """-> (bx, s, fy): o ponto do mundo (CX, fy) vai para (bx, SY) na tela, com escala s."""
    bx, s, fy = 540.0, 0.90, 752.0                                     # pé do osso em y≈1222: fora da legenda
    k = e_inout(prog(t, T["atrasa"] + 0.9, T["tripe"] - 0.1))          # abre a coluna da direita
    bx = lerp(bx, 300.0, k)
    k = (e_inout(prog(t, T["nicotina"] - 0.1, T["nicotina"] + 0.6))     # aproxima no vaso (nicotina -> pouco)
         * (1 - e_inout(prog(t, T["pouco"] - 0.1, T["pouco"] + 0.5))))
    bx = lerp(bx, BX_VASO, k); s = lerp(s, S_VASO, k); fy = lerp(fy, FY_VASO, k)
    k = e_inout(prog(t, T["ponte"] - 0.2, T["ponte"] + 0.7))           # aproxima no vão
    bx = lerp(bx, 560.0, k); s = lerp(s, 1.4, k); fy = lerp(fy, PIVO[1], k)
    k = e_inout(prog(t, T["pseudartrose"] - 0.25, T["pseudartrose"] + 0.45))   # recua para o nome
    bx = lerp(bx, 300.0, k); s = lerp(s, 0.92, k); fy = lerp(fy, 770.0, k)
    return bx, s, fy


def tremor(t, T):
    x = 0.0
    for t0, f in ((T["atrasa"], 9), (T["falsa"], 7)):                  # o tranco dos carimbos
        k = t - t0
        if 0 <= k < 0.35:
            x += f * math.sin(k * 70) * (1 - k / 0.35)
    return x


def tela(cam, x, y):
    bx, s, fy = cam
    return bx + s * (x - CX), SY + s * (y - fy)


def zoom_fator(t, T):
    """1 durante as aproximações (no vaso e no vão): o selo some, como no cf_fratura_cola, porque a
    ponta de cima do osso ampliado passa pela faixa dele."""
    vaso = prog(t, T["nicotina"] - 0.1, T["nicotina"] + 0.2) * (1 - prog(t, T["pouco"] + 0.2, T["pouco"] + 0.5))
    vao = prog(t, T["ponte"] - 0.2, T["ponte"] + 0.2) * (1 - prog(t, T["pseudartrose"] + 0.2, T["pseudartrose"] + 0.6))
    return max(vaso, vao)


# ------------------------------------------------------------------ utilidades de desenho
def ponta(cv, x, y, ang, tam, cor, a):
    """Cabeça de seta em (x, y) apontando para `ang` (radianos). (cópia do cf_pe_virado)"""
    p = skia.Path()
    p.moveTo(x + tam * math.cos(ang), y + tam * math.sin(ang))
    p.lineTo(x + tam * 0.75 * math.cos(ang + 2.45), y + tam * 0.75 * math.sin(ang + 2.45))
    p.lineTo(x + tam * 0.75 * math.cos(ang - 2.45), y + tam * 0.75 * math.sin(ang - 2.45))
    p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))


def seta_pts(cv, pts, cor, a, larg=7, tam=22):
    """Seta por uma lista de pontos; a cabeça segue a tangente do último trecho. (cópia do cf_pe_virado)"""
    if a <= 0 or len(pts) < 2:
        return
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    cv.drawPath(p, paint(cor, int(90 * a), "stroke", larg + 8, blur=6))
    cv.drawPath(p, paint(cor, int(255 * a), "stroke", larg))
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    ponta(cv, x1, y1, math.atan2(y1 - y0, x1 - x0), tam, cor, a)


def chip(cv, s, x, y, cor, a, tam=40, borda=None):
    """Rótulo solto (sem ponteiro), centrado em x; y = linha de base do texto. (cópia do cf_pe_virado)"""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    rr = skia.RRect.MakeRectXY(skia.Rect(x - lw / 2 - 24, y - tam * 1.05, x + lw / 2 + 24, y + tam * 0.34), 16, 16)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(220 * a)))
    cv.drawRRect(rr, paint(borda or cor, int(255 * a), "stroke", 3))
    cv.drawString(s, x - lw / 2, y, f, paint(cor, int(255 * a)))


def etiqueta(cv, s, x, y, alvo, cor, a, tam=36, saida=None):
    """Rótulo com linha-guia (o `rotulo` do cf_alongamento com fonte ajustável).
    (x, y): borda esquerda da caixa e linha de base do texto; `alvo`: ponto apontado;
    `saida`: de onde a linha sai da caixa (padrão: meio da borda esquerda)."""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    sx, sy = saida if saida else (x, y - tam * 0.36)
    cv.drawLine(alvo[0], alvo[1], sx, sy, paint(cor, int(200 * a), "stroke", 2.5))
    cv.drawCircle(alvo[0], alvo[1], 6, paint(cor, int(255 * a)))
    rr = skia.RRect.MakeRectXY(skia.Rect(x, y - tam * 1.08, x + lw + 30, y + tam * 0.32), 14, 14)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(225 * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 2.5))
    cv.drawString(s, x + 15, y, f, paint(cor, int(255 * a)))


def carimbo_opaco(cv, s, x, y, rot, t0, t, dur, tam=62, esc0=1.9):
    """Carimbo ouro torto com fundo opaco (legível sobre o osso claro). (cópia do cf_osteomielite)"""
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


def tique(cv, x, y, pr, cor, a, esc=1.0):
    """Tique desenhado em 2 traços (pr 0..1); (x, y) = início do traço curto."""
    if pr <= 0 or a <= 0:
        return
    p = skia.Path(); p.moveTo(x, y)
    p.lineTo(x + 12 * esc * min(1, pr * 2), y + 12 * esc * min(1, pr * 2))
    if pr > 0.5:
        q = (pr - 0.5) * 2
        p.lineTo(x + (12 + 22 * q) * esc, y + (12 - 30 * q) * esc)
    cv.drawPath(p, paint(cor, int(255 * a), "stroke", 6 * esc))


def estrela4(cv, x, y, s, cor, a):
    p = skia.Path(); p.moveTo(x, y - s * 2); p.lineTo(x + s * 0.5, y - s * 0.5); p.lineTo(x + s * 2, y)
    p.lineTo(x + s * 0.5, y + s * 0.5); p.lineTo(x, y + s * 2); p.lineTo(x - s * 0.5, y + s * 0.5)
    p.lineTo(x - s * 2, y); p.lineTo(x - s * 0.5, y - s * 0.5); p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))


# ------------------------------------------------------------------ cigarro (tela)
def cigarro(cv, x, y, ang, esc, a):
    """Bastão branco com ponta (filtro) laranja. Sem fumaça, sem brasa, sem marca."""
    if a <= 0 or esc <= 0:
        return
    L, R, LF = 260, 19, 74
    cv.save(); cv.translate(x, y); cv.rotate(ang); cv.scale(esc, esc)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-L / 2 + 4, -R + 10, L / 2 + 4, R + 10), 10, 10),
                 paint("#000000", int(70 * a), blur=10))
    corpo = skia.RRect.MakeRectXY(skia.Rect(-L / 2 + LF - 8, -R, L / 2, R), 8, 8)
    sh = skia.GradientShader.MakeLinear([skia.Point(0, -R), skia.Point(0, R)],
                                        [C("#FFFFFF", int(255 * a)), C("#F1F3F5", int(255 * a)), C("#C9D1D9", int(255 * a))],
                                        [0.0, 0.45, 1.0])
    cv.drawRRect(corpo, paint("#FFFFFF", 255, shader=sh))
    cv.drawOval(skia.Rect(L / 2 - 9, -R + 1, L / 2 + 7, R - 1), paint("#D9CBB3", int(255 * a)))    # papel na ponta
    filtro = skia.RRect.MakeRectXY(skia.Rect(-L / 2, -R, -L / 2 + LF, R), 9, 9)
    shf = skia.GradientShader.MakeLinear([skia.Point(0, -R), skia.Point(0, R)],
                                         [C("#F6B060", int(255 * a)), C("#E8913A", int(255 * a)), C("#B8681F", int(255 * a))],
                                         [0.0, 0.5, 1.0])
    cv.drawRRect(filtro, paint("#E8913A", 255, shader=shf))
    for i, (dx, dy) in enumerate(((-110, -8), (-96, 6), (-82, -4), (-118, 9), (-101, -12), (-88, 11), (-74, 0))):
        cv.drawCircle(dx, dy, 2.6, paint("#A8591A", int(170 * a)))                          # pintinhas do filtro
    cv.drawLine(-L / 2 + LF, -R, -L / 2 + LF, R, paint("#C8A04A", int(255 * a), "stroke", 3))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-L / 2, -R, L / 2, R), 9, 9), paint("#5E7186", int(150 * a), "stroke", 2))
    cv.restore()


def estado_cigarro(t, T):
    """-> (x, y, ang, esc, alfa) do cigarro (tela)."""
    lado = (250, 838, -6, 1.0)
    canto = (CANTO[0], CANTO[1], -14, 0.5)
    # já está na capa (o gancho fala dele) e termina de deslizar até o osso enquanto a voz diz "cigarro"
    k = e_out(prog(t, 0.0, T["cigarro"] + 0.6))
    x, y, ang, esc = lerp(140, lado[0], k), lado[1], lado[2], lado[3]
    k = e_inout(prog(t, T["atrasa"] + 0.15, T["atrasa"] + 0.9))       # encolhe e vai para o canto (nada no caminho)
    if k > 0:
        x, y, ang, esc = lerp(x, canto[0], k), lerp(y, canto[1], k), lerp(ang, canto[2], k), lerp(esc, canto[3], k)
    # canto -> vaso -> canto: "some aqui, aparece lá" (não cruza a lista nem o osso)
    for t0, alvo in ((T["nicotina"] - 0.05, CIG_VASO), (T["pouco"], canto)):
        if t < t0:
            break
        if t < t0 + 0.18:
            esc *= 1 - e_in_back(prog(t, t0, t0 + 0.18))
        else:
            x, y, ang = alvo[0], alvo[1], alvo[2]
            esc = alvo[3] * e_back(prog(t, t0 + 0.18, t0 + 0.5))
    sai = e_in_back(prog(t, T["parar"] + 0.1, T["parar"] + 0.8))         # apaga e sai de cena
    x -= 260 * sai
    a = 1 - prog(t, T["parar"] + 0.1, T["parar"] + 0.7)
    return x, y, ang, esc, a


# ------------------------------------------------------------------ vão, fragmentos, ponte (mundo)
def balanco(t, T):
    """Ângulo (graus) da dobradiça: começa em "mexe", para em "estabilizar"."""
    amp = 3.0 * e_inout(prog(t, T["mexe"] - 0.05, T["mexe"] + 0.5)) * (1 - e_inout(prog(t, T["estabilizar"], T["estabilizar"] + 0.7)))
    return amp * math.sin(2 * math.pi * 1.1 * (t - T["mexe"])), amp / 3.0


def brilho_vao(t, T):
    """Intensidade do brilho dourado do vão: acende no tripé e esmaece em "lenta". Em "estimular"
    NÃO volta (o vão cheio de ouro diria "colou"): ali só as faíscas acendem (vao_faiscas)."""
    return prog(t, T["tripe"], T["tripe"] + 0.6) * (1 - 0.78 * e_inout(prog(t, T["lenta"], T["lenta"] + 1.2)))


def vao_brilho(cv, t, T):
    """Brilho dourado na MESMA largura do osso, recortado no vão (sem formato de calo)."""
    g = min(1.0, brilho_vao(t, T))
    if g <= 0:
        return
    h = HASTE / 2
    cv.save(); cv.clipPath(_vao(GAP), skia.ClipOp.kIntersect, True)
    cv.clipRect(skia.Rect(CX - h, YF - 20, CX + h, YF + GAP + 20))          # nem 1 px fora da largura do osso
    cv.drawRect(skia.Rect(CX - h + 4, YF - 6, CX + h - 4, YF + GAP + 6), paint(NOVO_G, int(205 * g), blur=14))
    cv.drawRect(skia.Rect(CX - h + 20, YF + 10, CX + h - 20, YF + GAP - 10), paint("#FFF1C9", int(150 * g), blur=10))
    cv.restore()


FAISCAS = [(-44, 0.30, 0.0), (-20, 0.62, 1.3), (6, 0.38, 2.1), (30, 0.66, 0.7), (44, 0.42, 3.0),
           (-34, 0.50, 4.2), (18, 0.52, 5.1), (-6, 0.70, 2.7), (-50, 0.62, 1.9), (40, 0.28, 4.6)]


def vao_faiscas(cv, t, T):
    """Pontinhos dourados ESPARSOS dentro do vão (não é calo, não cresce das pontas)."""
    est = prog(t, T["estimular"], T["estimular"] + 0.4)
    g = max(brilho_vao(t, T), 0.6 * est)                 # fator próprio: só as estrelinhas acendem
    if g <= 0:
        return
    cv.save(); cv.clipPath(_vao(GAP), skia.ClipOp.kIntersect, True)
    for i, (dx, fy, ph) in enumerate(FAISCAS):
        if i >= 6 and est <= 0:                     # esparso; em "estimular" acendem mais alguns
            continue
        pis = 0.5 + 0.5 * math.sin(t * 4.2 + ph)
        a = clamp(g * (0.35 + 0.65 * pis)) * (est if i >= 6 else 1.0)
        s = 2.2 + 1.8 * pis + 2.4 * est
        estrela4(cv, CX + dx, YF + GAP * fy, s, "#FFE6A8", a)
    cv.restore()


# cada metade já recortada (a sombra contorna as pontas serrilhadas; sem recorte reto que vaze em "caixa")
FRAGS = (skia.Op(OSSO, _regiao_acima(YF), skia.PathOp.kIntersect_PathOp),
         skia.Op(OSSO, _regiao_abaixo(YF), skia.PathOp.kIntersect_PathOp))


def fragmentos(cv, ang):
    sh = sombra_osso()
    zp = skia.Path(); z = _zig(YF); zp.moveTo(*z[0])
    for x, y in z[1:]:
        zp.lineTo(x, y)
    for parte in (0, 1):
        cv.save()
        cv.translate(*PIVO); cv.rotate(ang if parte == 0 else -ang); cv.translate(-PIVO[0], -PIVO[1])
        if parte == 1:
            cv.translate(0, GAP)
        cv.drawPath(FRAGS[parte], paint("#000000", 70, blur=14))
        cv.clipPath(_regiao_acima(YF) if parte == 0 else _regiao_abaixo(YF), skia.ClipOp.kIntersect, True)
        cv.drawPath(OSSO, paint(OSSO_C, shader=sh))
        cv.drawPath(OSSO, paint(OSSO_L, 150, "stroke", 2.5))
        cv.clipPath(OSSO, skia.ClipOp.kIntersect, True)
        cv.drawPath(zp, paint(OSSO_L, 200, "stroke", 3))                  # borda serrilhada da ponta
        cv.restore()


N_ARCO = 24


def ponto_arco(i):
    ang = math.pi * (i / N_ARCO)
    return CX - HASTE / 2 - 22 - 100 * math.sin(ang), lerp(YF - 70, YF + GAP + 70, i / N_ARCO)


def avanco_ponte(t, T):
    """Fração do arco já desenhada: avança no tripé, desacelera com o aperto e para na METADE."""
    ks = ((T["tripe"] + 0.2, 0.0, 0.10), (T["aperta"], 0.34, 0.075), (T["lenta"], 0.47, 0.02),
          (T["lenta"] + 1.6, 0.5, 0.0))
    if t <= ks[0][0]:
        return 0.0
    for (t0, p0, m0), (t1, p1, m1) in zip(ks, ks[1:]):
        if t <= t1:
            h = t1 - t0; u = (t - t0) / h
            return ((2 * u ** 3 - 3 * u ** 2 + 1) * p0 + (u ** 3 - 2 * u ** 2 + u) * h * m0
                    + (-2 * u ** 3 + 3 * u ** 2) * p1 + (u ** 3 - u ** 2) * h * m1)
    return 0.5


def ponte_arco(cv, t, T, ang):
    pr = avanco_ponte(t, T)
    if pr <= 0:
        return
    n_ok = pr * N_ARCO
    fantasma = prog(t, T["ponte"], T["ponte"] + 0.5)
    # o caminho que falta: contorno tênue desde o início; em "ponte" fica cinza firme (não fecha)
    a_f = lerp(55, 150, fantasma) * prog(t, T["tripe"], T["tripe"] + 0.5)
    for i in range(int(n_ok) + 1, N_ARCO + 1):
        x, y = ponto_arco(i)
        cv.drawCircle(x, y, 6.5, paint("#8FA3B8", int(a_f), "stroke", 2.4))
    cv.save()
    cv.translate(*PIVO); cv.rotate(ang); cv.translate(-PIVO[0], -PIVO[1])          # preso à metade de cima
    for i in range(int(n_ok) + 1):
        x, y = ponto_arco(i)
        cv.drawCircle(x, y, 7.5, paint(OURO, 255))
    # a ponta do arco: pulsa enquanto avança, mais devagar em "lenta"; depois de "ponte", pisca parada
    x, y = ponto_arco(n_ok)
    pul = 0.5 + 0.5 * math.sin(t * (9 if fantasma > 0 else (2.5 if t >= T["lenta"] else 5)))
    cv.drawCircle(x, y, 15, paint(OURO, int(120 * pul), blur=7))
    cv.drawCircle(x, y, 8.5, paint("#FFF1C9", 255))
    for t0 in (T["tripe"] + 0.25, T["lenta"]):           # o olho vai para a ponta: é ela que constrói a ponte
        brilhos(cv, x, y, t, t0, n=7, raio=50)
    cv.restore()


def setas_balanco(cv, t, T, amp):
    """Duas setas curvas de ida e volta, em arco em volta da dobradiça, à direita do osso
    (fora do marfim): uma acompanha a metade de cima, a outra a de baixo."""
    amp *= 1 - prog(t, T["pseudartrose"] + 0.1, T["pseudartrose"] + 0.4)   # saem quando o cartão do nome entra
    if amp <= 0.01:
        return
    R = 172
    for centro in (-43, 43):
        for lado in (-1, 1):
            pts = []
            for k in range(10):
                g = math.radians(centro + lado * lerp(1.5, 15, k / 9))
                pts.append((PIVO[0] + R * math.cos(g), PIVO[1] + R * math.sin(g)))
            seta_pts(cv, pts, "#E6EEF6", amp, larg=6, tam=20)


# ------------------------------------------------------------------ vaso (mundo)
HW = 20.0                                  # meia largura do tubo (legível no celular)
U_CINTURA = 0.3                            # onde a nicotina aperta
R_GLOB = 10.5                              # raio dos glóbulos


def _bez(u):
    p = ((CX + 112, 1120), (CX + 112, 900), (CX + 106, PIVO[1]), (CX + 40, PIVO[1]))
    v = 1 - u
    return (v ** 3 * p[0][0] + 3 * v * v * u * p[1][0] + 3 * v * u * u * p[2][0] + u ** 3 * p[3][0],
            v ** 3 * p[0][1] + 3 * v * v * u * p[1][1] + 3 * v * u * u * p[2][1] + u ** 3 * p[3][1])


def meia_largura(u, aperto):
    return HW * (1 - 0.72 * aperto * math.exp(-((u - U_CINTURA) / 0.11) ** 2))


def fase_globulos(t, T):
    """Fase integrada (sem salto): velocidade cai de v0 para v1 a partir de "menos"."""
    v0, v1, r = 0.42, 0.14, 0.8
    f = v0 * (t - T["chegando"])
    x = t - T["menos"]
    if x > 0:
        f += (v1 - v0) * (x * x / (2 * r) if x < r else r / 2 + (x - r))
    return f


def vaso(cv, t, T):
    a = prog(t, T["sangue"] - 0.05, T["sangue"] + 0.25) * (1 - prog(t, T["ponte"] - 0.5, T["ponte"] - 0.2))
    if a <= 0:
        return
    cresce = e_out(prog(t, T["sangue"], T["chegando"] + 0.3))
    aperto = e_inout(prog(t, T["aperta"], T["aperta"] + 0.7))
    n = 64; esq, dir_, meio = [], [], []
    for k in range(n + 1):
        u = cresce * k / n
        x, y = _bez(u); x2, y2 = _bez(min(1, u + 0.004)); x1, y1 = _bez(max(0, u - 0.004))
        dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        on = 3.0 * math.sin(k * 0.55 + t * 1.4) * math.sin(math.pi * k / n)          # ondulação leve
        x += nx * on; y += ny * on
        hw = meia_largura(u, aperto)
        esq.append((x + nx * hw, y + ny * hw)); dir_.append((x - nx * hw, y - ny * hw)); meio.append((x, y))
    if len(meio) < 2:
        return
    cv.saveLayer(skia.Rect(CX - 40, YF - 80, CX + 200, 1200), None)
    tubo = skia.Path(); tubo.moveTo(*esq[0])
    for q in esq[1:]:
        tubo.lineTo(*q)
    for q in reversed(dir_):
        tubo.lineTo(*q)
    tubo.close()
    cv.drawPath(tubo, paint(VASO, int(80 * a), blur=6))
    cv.drawPath(tubo, paint("#5A1A22", int(170 * a)))
    for lado in (esq, dir_):
        p = skia.Path(); p.moveTo(*lado[0])
        for q in lado[1:]:
            p.lineTo(*q)
        cv.drawPath(p, paint(VASO, int(255 * a), "stroke", 4.5))
    # glóbulos (esquemáticos), correndo até o vão; raros e lentos depois do aperto
    if t < T["chegando"]:
        _apaga_base(cv)
        return
    raro = prog(t, T["menos"], T["menos"] + 0.8)
    fase = fase_globulos(t, T); N = 9
    for i in range(N):
        u = (fase + i / N) % 1.0
        if u > cresce:
            continue
        ag = a * prog(t, T["chegando"], T["chegando"] + 0.3) * clamp(u / 0.06) * (1 - prog(u, 0.9, 1.0))
        if i % 3:
            ag *= 1 - raro
        if ag <= 0:
            continue
        k = u / max(cresce, 1e-6) * n
        j = min(int(k), n - 1); r_ = k - j
        x = lerp(meio[j][0], meio[j + 1][0], r_); y = lerp(meio[j][1], meio[j + 1][1], r_)
        esp = clamp(meia_largura(u, aperto) / HW, 0.4, 1.0)
        r = R_GLOB
        cv.drawOval(skia.Rect(x - r * esp, y - r, x + r * esp, y + r), paint(GLOB, int(255 * ag)))
        cv.drawOval(skia.Rect(x - r * esp, y - r, x + r * esp, y + r), paint("#B8323A", int(200 * ag), "stroke", 1.8))
    _apaga_base(cv)


def _apaga_base(cv):
    """Fecha a camada do vaso apagando a ponta de baixo em degradê (o tubo não termina cortado)."""
    masc = skia.Paint(AntiAlias=True)
    masc.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 1125), skia.Point(0, 1035)],
                                                  [skia.ColorSetARGB(0, 0, 0, 0), skia.ColorSetARGB(255, 0, 0, 0)]))
    masc.setBlendMode(skia.BlendMode.kDstIn)
    cv.drawRect(skia.Rect(CX - 40, YF - 80, CX + 200, 1200), masc)
    cv.restore()


# ------------------------------------------------------------------ tripé (tela)
PERNAS = ((-78, 18, -142, 232), (0, 26, 0, 250), (78, 18, 142, 232))     # esquerda, frente, direita


def a_tripe(t, T):
    return prog(t, T["tripe"] - 0.05, T["tripe"] + 0.25) * (1 - prog(t, T["ponte"] - 0.5, T["ponte"] - 0.15))


def tripe(cv, t, T):
    a = a_tripe(t, T)
    if a <= 0:
        return
    pop = lerp(0.55, 1.0, e_back(prog(t, T["tripe"], T["tripe"] + 0.45)))
    cai = e_back(prog(t, T["pouco"] + 0.1, T["pouco"] + 0.75))              # a perna do sangue falha
    tilt = 10.0 * cai + (1.2 * math.sin((t - T["pouco"]) * 9) * (1 - prog(t, T["pouco"] + 0.7, T["pouco"] + 1.6))
                         if t > T["pouco"] + 0.1 else 0.0)
    acesa = (T["firmeza"], T["chegando"], T["infeccao"])
    completo = prog(t, T["infeccao"], T["infeccao"] + 0.3) * (1 - prog(t, T["pouco"], T["pouco"] + 0.4))
    # sombra no chão (não inclina)
    cv.drawOval(skia.Rect(TRI_X - 175, TRI_Y + 236, TRI_X + 175, TRI_Y + 262), paint("#000000", int(70 * a), blur=8))
    cv.save(); cv.translate(TRI_X, TRI_Y); cv.scale(pop, pop); cv.rotate(tilt)
    for i, (x0, y0, x1, y1) in enumerate(PERNAS):
        if i == 1:
            y1 = lerp(y1, y0 + (y1 - y0) * 0.62, cai)
        on = e_out(prog(t, acesa[i], acesa[i] + 0.3))
        cor = lerpc("#6F8399", OURO, on)
        if i == 1:
            cor = lerpc(cor, "#46566A", cai)
        if on > 0 and not (i == 1 and cai > 0.5):
            cv.drawLine(x0, y0, x1, y1, paint(OURO, int(90 * a * on * (1 - cai if i == 1 else 1)), "stroke", 28, blur=9))
        cv.drawLine(x0, y0, x1, y1, paint(cor, int(255 * a), "stroke", 14))
    # assento (laje com borda)
    cv.drawOval(skia.Rect(-120, -14, 120, 40), paint("#1C3A4F", int(255 * a)))
    cv.drawRect(skia.Rect(-120, 0, 120, 13), paint("#1C3A4F", int(255 * a)))
    cv.drawOval(skia.Rect(-120, -27, 120, 27), paint("#33566F", int(255 * a)))
    borda = lerpc("#8FA3B8", OURO, completo)
    cv.drawOval(skia.Rect(-120, -27, 120, 27), paint(borda, int(255 * a), "stroke", 4))
    cv.drawArc(skia.Rect(-120, -14, 120, 40), 0, 180, False, paint(borda, int(200 * a), "stroke", 3))
    if completo > 0:
        cv.drawOval(skia.Rect(-128, -33, 128, 33), paint(OURO, int(80 * a * completo), "stroke", 10, blur=8))
    cv.restore()
    for i, t0 in enumerate(acesa):                                        # faísca ao acender cada perna
        x0, y0, x1, y1 = PERNAS[i]
        brilhos(cv, TRI_X + (x0 + x1) / 2, TRI_Y + (y0 + y1) / 2, t, t0 + 0.05, n=9, raio=80)
    # tripé completo: o nome sai e o foco vai para o mecanismo (pernas e animação continuam)
    chip(cv, "TRIPÉ", TRI_X, TRI_Y - 52, OURO,
         a * prog(t, T["tripe"], T["tripe"] + 0.25) * (1 - prog(t, T["infeccao"] + 0.8, T["infeccao"] + 1.2)), tam=36)


def lista_tripe(cv, t, T):
    a_g = a_tripe(t, T)
    if a_g <= 0:
        return
    itens = (("FIRMEZA", T["firmeza"]), ("SANGUE CHEGANDO", T["chegando"]), ("NENHUMA INFECÇÃO", T["infeccao"]))
    falha = prog(t, T["pouco"] + 0.1, T["pouco"] + 0.5)
    foco = prog(t, T["nicotina"], T["nicotina"] + 0.4)       # da nicotina em diante só SANGUE CHEGANDO em destaque
    for k, (rot, t0) in enumerate(itens):
        on = prog(t, t0 - 0.05, t0 + 0.25)
        if on <= 0:
            continue
        y = 640 + k * 62
        a = a_g * on * (1 - 0.65 * foco if k != 1 else 1.0)
        x = X_LISTA + 30 * (1 - e_out(on))
        cinza = falha if k == 1 else 0.0
        cor = lerpc(OURO, "#55687D", cinza)
        cv.drawCircle(x + 14, y - 13, 18, paint(cor, int(80 * a * (1 - cinza)), blur=7))
        cv.drawCircle(x + 14, y - 13, 11, paint(cor, int(255 * a)))
        texto(cv, rot, x + 42, y, F_BLACK, 36, lerpc("#FFFFFF", "#7E8FA3", cinza), int(255 * a), centro=False, contorno=7)
        if k == 2:
            lw = skia.Font(F_BLACK, 36).measureText(rot)
            tique(cv, x + 42 + lw + 22, y - 16, e_out(prog(t, t0 + 0.2, t0 + 0.5)), OURO, a)


# ------------------------------------------------------------------ rótulos do mecanismo (tela)
def rotulos(cv, t, T, cam, amp):
    # cigarro (abertura) e nicotina: chip em cima do cigarro
    x, y, ang, esc, a_c = estado_cigarro(t, T)
    a = prog(t, T["cigarro"] + 0.3, T["cigarro"] + 0.55) * (1 - prog(t, T["atrasa"] - 0.1, T["atrasa"] + 0.15))
    chip(cv, "CIGARRO", x, y - 56, NEUTRO, a * a_c, tam=40)
    a = prog(t, T["nicotina"] + 0.45, T["nicotina"] + 0.7) * (1 - prog(t, T["pouco"] - 0.15, T["pouco"] + 0.1))
    chip(cv, "NICOTINA", x, y + 82, NEUTRO, a * a_c, tam=40)              # embaixo: em cima fica a etiqueta do vaso
    # causa -> efeito sem texto: seta do cigarro até a cintura do vaso, desenhada aos poucos
    aperto = e_inout(prog(t, T["aperta"], T["aperta"] + 0.7))
    xw, yw = _bez(U_CINTURA)
    a = prog(t, T["nicotina"] + 0.5, T["nicotina"] + 0.65) * (1 - prog(t, T["pouco"] - 0.2, T["pouco"]))
    if a > 0:
        x0, y0 = x - 128 * esc, y + 14
        x2, y2 = tela(cam, xw + meia_largura(U_CINTURA, aperto) + 16, yw + 30)
        x1, y1 = lerp(x0, x2, 0.45), max(y0, y2) + 10
        pr = e_out(prog(t, T["nicotina"] + 0.5, T["nicotina"] + 0.85))
        pts = []
        for i in range(int(2 + 18 * pr)):
            u = pr * i / max(1, int(1 + 18 * pr))
            pts.append(((1 - u) ** 2 * x0 + 2 * (1 - u) * u * x1 + u * u * x2,
                        (1 - u) ** 2 * y0 + 2 * (1 - u) * u * y1 + u * u * y2))
        seta_pts(cv, pts, NEUTRO, a * a_c, larg=5, tam=18)
    # aperta os vasos -> menos sangue e oxigênio (mesmo lugar, um depois do outro); o ponto-guia fica
    # FORA do tubo, ao lado da cintura (não em cima dela)
    a = prog(t, T["aperta"], T["aperta"] + 0.25) * (1 - prog(t, T["menos"] - 0.2, T["menos"]))
    etiqueta(cv, "APERTA OS VASOS", X_LISTA + 10, Y_ROT_VASO,
             tela(cam, xw + meia_largura(U_CINTURA, aperto) + 22, yw - 18), GLOB, a)
    a = prog(t, T["menos"], T["menos"] + 0.25) * (1 - prog(t, T["pouco"] - 0.15, T["pouco"] + 0.1))
    xm, ym = _bez(0.5)
    etiqueta(cv, "MENOS SANGUE E OXIGÊNIO", X_LISTA - 15, Y_ROT_VASO, tela(cam, xm + HW + 22, ym), GLOB, a, tam=34)
    # cura lenta: aponta para o vão, cujo brilho esmaece
    a = prog(t, T["lenta"], T["lenta"] + 0.25) * (1 - prog(t, T["ponte"] - 0.3, T["ponte"] - 0.05))
    etiqueta(cv, "CURA LENTA OU NENHUMA", X_LISTA - 15, 848, tela(cam, CX + 44, PIVO[1]), AZUL, a, tam=34)
    # a ponte não fecha: aponta para a ponta do arco, parada na metade
    a = prog(t, T["ponte"] + 0.35, T["ponte"] + 0.6) * (1 - prog(t, T["falsa"] - 0.3, T["falsa"] - 0.05))
    xa, ya = ponto_arco(avanco_ponte(t, T) * N_ARCO)
    etiqueta(cv, "A PONTE NÃO FECHA", 40, 600, tela(cam, xa - 10, ya), OURO, a, saida=(250, 612))
    # ponto que mexe: à direita do vão
    a = prog(t, T["mexe"] + 0.1, T["mexe"] + 0.35) * (1 - prog(t, T["pseudartrose"] - 0.2, T["pseudartrose"] + 0.05))
    etiqueta(cv, "PONTO QUE MEXE", 676, 806, tela(cam, CX + HASTE / 2 + 2, PIVO[1]), "#E6EEF6", a, tam=34)
    # risco maior: tom neutro, ao lado do cigarro do canto
    a = prog(t, T["risco"], T["risco"] + 0.25) * (1 - prog(t, T["parar"], T["parar"] + 0.35))
    chip(cv, "RISCO MAIOR", 352, 286, NEUTRO, a * a_c, tam=36, borda="#8FA3B8")


def titulo(cv, t, T, cam):
    t0 = T["pseudartrose"] + 0.25                      # depois de a câmera abrir a coluna da direita
    a = prog(t, t0, t0 + 0.25) * (1 - prog(t, T["caminho"] - 0.35, T["caminho"] - 0.05))
    if a <= 0:
        return
    esc = lerp(0.88, 1.0, e_back(prog(t, t0, t0 + 0.45)))
    x0, y0, x1, y1 = 452, 712, 1032, 878
    xa, ya = tela(cam, CX + HASTE / 2 + 2, PIVO[1])
    cv.drawLine(xa, ya, x0, (y0 + y1) / 2, paint(OURO, int(200 * a), "stroke", 2.5))
    cv.drawCircle(xa, ya, 6, paint(OURO, int(255 * a)))
    cv.save(); cv.translate((x0 + x1) / 2, (y0 + y1) / 2); cv.scale(esc, esc); cv.translate(-(x0 + x1) / 2, -(y0 + y1) / 2)
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 22, 22)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(235 * a)))
    cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 4))
    texto(cv, "PSEUDARTROSE", (x0 + x1) / 2, y0 + 82, F_BLACK, 58, OURO, int(255 * a))
    texto(cv, "a fratura que não cola", (x0 + x1) / 2, y0 + 134, F_SEMI, 34, AZUL, int(255 * a))
    cv.restore()


def checklist_caminho(cv, t, T):
    a_g = prog(t, T["caminho"], T["caminho"] + 0.3) * (1 - prog(t, T["manda"] - 0.45, T["manda"] - 0.1))
    if a_g <= 0:
        return
    x0 = X_LISTA + 60 * (1 - e_out(prog(t, T["caminho"], T["caminho"] + 0.4)))
    for k, (rot, t_ok) in enumerate((("ESTABILIZAR MELHOR", T["estabilizar"]), ("ESTIMULAR O OSSO", T["estimular"]))):
        y = 580 + k * 96
        rr = skia.RRect.MakeRectXY(skia.Rect(x0, y - 42, x0 + 50, y + 8), 10, 10)
        cv.drawRRect(rr, paint(FUNDO_CARTAO, int(220 * a_g))); cv.drawRRect(rr, paint(OURO, int(255 * a_g), "stroke", 3.5))
        ok = prog(t, t_ok, t_ok + 0.25)
        tique(cv, x0 + 10, y - 18, e_out(prog(t, t_ok, t_ok + 0.3)), OURO, a_g)
        texto(cv, rot, x0 + 66, y - 4, F_BLACK, 36, lerpc("#8FA3B8", "#FFFFFF", ok), int(255 * a_g), centro=False, contorno=8)
    # selo pequeno CASO A CASO
    k = prog(t, T["caminho"] + 0.35, T["caminho"] + 0.6)
    if k > 0:
        a = a_g * k
        cv.save(); cv.translate(X_LISTA + 150, 752); cv.rotate(-4); cv.scale(lerp(1.35, 1.0, e_out(k)), lerp(1.35, 1.0, e_out(k)))
        f = skia.Font(F_BLACK, 30); lw = f.measureText("CASO A CASO")
        rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 18, -32, lw / 2 + 18, 12), 10, 10)
        cv.drawRRect(rr, paint(FUNDO_CARTAO, int(235 * a))); cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 3.5))
        cv.drawString("CASO A CASO", -lw / 2, 0, f, paint(OURO, int(255 * a)))
        cv.restore()


def cartao_parar(cv, t, T):
    """Cartão SEPARADO do checklist: parar de fumar vem de outra fonte (recuperação)."""
    k = prog(t, T["parar"], T["parar"] + 0.3)
    a = k * (1 - prog(t, T["manda"] - 0.45, T["manda"] - 0.1))
    if a <= 0:
        return
    esc = lerp(0.85, 1.0, e_back(prog(t, T["parar"], T["parar"] + 0.45)))
    x0, y0, x1, y1 = 470, 846, 1010, 1012
    cv.save(); cv.translate((x0 + x1) / 2, (y0 + y1) / 2); cv.scale(esc, esc); cv.translate(-(x0 + x1) / 2, -(y0 + y1) / 2)
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 22, 22)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(240 * a)))
    cv.drawRRect(rr, paint(AZUL, int(255 * a), "stroke", 4))
    texto(cv, "PARAR DE FUMAR", (x0 + x1) / 2, y0 + 66, F_BLACK, 44, "#FFFFFF", int(255 * a))
    texto(cv, "FAZ DIFERENÇA", (x0 + x1) / 2, y0 + 128, F_BLACK, 44, AZUL, int(255 * a))
    cv.restore()


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    bx, s, fy = camera(t, T)
    cam = (bx + tremor(t, T), s, fy)
    ang, amp = balanco(t, T)

    # mundo (câmera), numa camada: o osso nunca invade a faixa da legenda (y > 1230)
    cv.saveLayer(None, None)
    cv.save(); cv.translate(cam[0], SY); cv.scale(s, s); cv.translate(-CX, -fy)
    vaso(cv, t, T)                       # atrás do osso: só aparece fora dele e dentro do vão
    fragmentos(cv, ang)
    vao_brilho(cv, t, T)
    vao_faiscas(cv, t, T)
    ponte_arco(cv, t, T, ang)
    setas_balanco(cv, t, T, amp)
    cv.restore()
    z = clamp((SY + s * (Y_PE - fy) - 1225) / 40)          # quanto o pé do osso passaria de y≈1230
    if z > 0:
        masc = skia.Paint(AntiAlias=True)
        masc.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 1120), skia.Point(0, 1228)],
                                                      [skia.ColorSetARGB(255, 0, 0, 0),
                                                       skia.ColorSetARGB(int(255 * (1 - z)), 0, 0, 0)]))
        masc.setBlendMode(skia.BlendMode.kDstIn)
        cv.drawRect(skia.Rect(0, 1000, W, 1920), masc)
    cv.restore()

    # tela
    tripe(cv, t, T)
    lista_tripe(cv, t, T)
    titulo(cv, t, T, cam)
    checklist_caminho(cv, t, T)
    cartao_parar(cv, t, T)
    x, y, a_ang, esc, a = estado_cigarro(t, T)
    cigarro(cv, x, y, a_ang, esc, a)
    rotulos(cv, t, T, cam, amp)
    carimbo_opaco(cv, "ATRASA", 540, 610, -7, T["atrasa"], t, dur=1.7, esc0=1.7)
    carimbo_opaco(cv, "FALSA JUNTA", 430, 612, -6, T["falsa"], t, dur=T["pseudartrose"] - T["falsa"] + 0.15, esc0=1.5)

    capa(cv, t, T["atrasa"], ep["gancho"][0], ep["gancho"][1])
    selo_como_funciona(cv, prog(t, T["atrasa"] + 0.55, T["atrasa"] + 0.95) * (1 - prog(t, T["manda"] - 0.3, T["manda"]))
                       * (1 - zoom_fator(t, T)))
    interface(cv, t, T, blocos, DESTAQUE)


# ------------------------------------------------------------------ som e prévias
def sons(T):
    ev = [(T["cigarro"] + 0.02, "whoosh", 0.4), (T["atrasa"] - 0.02, "thump", 0.9), (T["atrasa"] + 0.2, "whoosh", 0.3),
          (T["tripe"] + 0.05, "pop", 0.6), (T["tripe"] + 0.2, "shimmer", 0.3),
          (T["firmeza"], "ping", 0.5), (T["sangue"], "whoosh", 0.25), (T["chegando"], "ping", 0.5),
          (T["infeccao"], "ping", 0.5), (T["infeccao"] + 0.25, "ding", 0.35),
          (T["nicotina"], "whoosh", 0.45), (T["nicotina"] + 0.15, "pop", 0.4), (T["aperta"] + 0.1, "pop", 0.45),
          (T["pouco"], "whoosh", 0.3), (T["pouco"] + 0.2, "pop", 0.35), (T["pouco"] + 0.25, "thump", 0.5),
          (T["ponte"] - 0.15, "whoosh", 0.4), (T["ponte"] + 0.5, "tick", 0.5),
          (T["falsa"] - 0.02, "thump", 0.9), (T["pseudartrose"], "whoosh", 0.35), (T["pseudartrose"] + 0.2, "ding", 0.5),
          (T["risco"], "pop", 0.45), (T["caminho"], "whoosh", 0.35), (T["estabilizar"], "ping", 0.55),
          (T["estimular"], "ping", 0.5), (T["estimular"] + 0.1, "shimmer", 0.6), (T["parar"], "pop", 0.5),
          (T["parar"] + 0.15, "whoosh", 0.3), (T["manda"] + 0.05, "whoosh", 0.5)]
    # a falsa junta rangendo de leve: um clique a cada virada do balanço, até estabilizar
    k = 0
    while True:
        tk = T["mexe"] + 0.23 + k / 2.2
        if tk >= T["estabilizar"] + 0.2:
            break
        ev.append((tk, "click", 0.45)); k += 1
    return ev


def tempos_previa(T):
    return (0.9, T["atrasa"] + 0.35, T["infeccao"] + 0.6, T["aperta"] + 0.9, T["menos"] + 0.9, T["lenta"] + 0.7,
            T["ponte"] + 1.0, T["falsa"] + 0.4, T["risco"] + 0.5, T["estimular"] + 0.6, T["diferenca"] + 0.8,
            T["manda"] + 1.6)


render = fazer_render(quadro, ANCORAS, sons, tempos_previa)
