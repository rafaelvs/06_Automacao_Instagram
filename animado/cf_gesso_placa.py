# -*- coding: utf-8 -*-
"""COMO FUNCIONA — quem segura o osso quebrado ("GESSO, PLACA / OU HASTE?").

Mesmo estilo e mesmas peças das cenas aprovadas (osso marfim, brilho dourado, anel/fio/haste/porca
do fixador, contorno de perna do piloto, rótulos, carimbos, brilhos, legenda karaokê, CTA com
aviãozinho). O que a cena mostra, cada coisa disparada pela palavra falada:
  * capa (t=0): o osso longo inteiro, centrado, com o gancho; "quebrado": risco branco em
    zigue-zague com tick seco e tremor, as partes se afastam poucos pixels (sem sangue, sem
    fragmento voando);
  * "firme": fios dourados pontilhados tentam ligar as pontas; "mexe": as partes balançam em
    sentidos opostos (3-4 graus) e os fios viram faíscas; "demais": carimbo vermelho e balanço
    mais forte; "segura": moldura tracejada vazia (a vaga) + QUEM SEGURA? + "?"; "cicatriza": a
    linha da fratura acende em dourado (só brilho, sem calo), mas o osso AINDA balança (pouco):
    ninguém segurou ainda;
  * "gesso": contorno da perna do piloto e uma faixa branco-gelo que se enrola de logo abaixo do
    joelho até o tornozelo (sai do quadro junto com a perna) — gesso OPACO, por fora da pele;
    "imobiliza": cadeado dourado fecha e É ELE que para o balanço (estabilidade -> cola);
  * "placa": placa azul-aço com 4 furos desliza e encosta no osso cruzando a fratura;
    "parafusos": 4 cabeças douradas aparecem uma a uma (sem giro, sem trajeto dentro do osso);
  * "haste": a placa sai; a haste aparece AO LADO do osso, sem tocá-lo; "dentro": ela some e
    reaparece como contorno tracejado azul-aço no eixo do osso marfim opaco (convenção de
    desenho técnico: nada translúcido, sem mostrar por onde entra nem o ato de inserir);
  * "fixador": a perna volta e os anéis entram pelas laterais; "atravessam": os fios avançam um
    a um até o osso, cruzando o contorno da perna; "estrutura": as hastes rosqueadas ligam os
    anéis e o conjunto acende; "fora": seta para os anéis, por fora da pele;
  * "qual": a cena encolhe para dentro do 4º de quatro cartões iguais (nenhum destacado, nenhum
    check); "caso": carimbo QUEM DECIDE É O CASO por cima dos quatro;
  * "colou": a cena sai do cartão da placa; a linha dourada se funde ao marfim; "tirar": a placa
    se levanta e hesita; "nem": volta ao lugar e entra o cartão dourado NEM SEMPRE com a linha
    "a decisão é do cirurgião" (literal da legenda).
Nenhum exame de imagem simulado, nenhum implante de modelo comercial. Todo texto desenhado está
em ep["tela"] (o render recusa o vídeo se não estiver).
"""
import math

import numpy as np
import skia

from .cf_comum import capa, carimbo as carimbo_ouro, fazer_render, interface, selo_como_funciona
from .cf_alongamento import (ACO, ACO_ESC, ACO_HL, CX, F_BLACK, F_SEMI, NOVO, NOVO_G, OSSO_B, OSSO_C,
                             OSSO_L, OURO, VERMELHO, W, Y_BASE, Y_TOPO, anel, brilhos, clamp, e_back,
                             e_in_back, e_inout, e_out, fundo, haste, larg_texto, lerp, lerpc, paint,
                             path_osso_inf, path_osso_sup, perna, porca, prog, sombra_osso, texto)
from .cf_fratura_cola import _regiao_abaixo, _regiao_acima, _vao, _zig

ANCORAS = {
    "quebrado": ("quebrado", 1, False), "firme": ("firme", 1, False), "estavel": ("estável", 1, False),
    "mexe": ("mexe", 1, False), "demais": ("demais", 1, False), "segura": ("segura", 1, False),
    "cicatriza": ("cicatriza", 1, False), "gesso": ("gesso", 1, False), "imobiliza": ("imobiliza", 1, False),
    "placa": ("placa", 1, False), "parafusos": ("parafusos", 1, False), "haste": ("haste", 1, False),
    "dentro": ("dentro", 1, False), "fixador": ("fixador", 1, False), "atravessam": ("atravessam", 1, False),
    "estrutura": ("estrutura", 1, False), "fora": ("fora", 1, False), "qual": ("qual", 1, False),
    "caso": ("caso", 1, False), "colou": ("colou", 1, False), "tirar": ("tirar", 1, False),
    "nem": ("nem", 1, False), "manda": ("manda", 1, False),
}
DESTAQUE = {"quebrado", "firme", "estável", "mexe", "demais", "segura", "cicatriza", "gesso", "imobiliza",
            "placa", "parafusos", "haste", "dentro", "fixador", "pinos", "atravessam", "estrutura", "fora",
            "caso", "colou", "nem", "sempre"}

# ------------------------------------------------------------------ textos de tela (todos em ep["tela"])
T_MEXE = "SE MEXE DEMAIS, NÃO COLA"
T_QUEM = "QUEM SEGURA?"
T_INTERROG = "?"
T_GESSO, T_IMOB = "GESSO", "IMOBILIZA"
T_PLACA = "PLACA E PARAFUSOS"
T_HASTE, T_DENTRO = "HASTE", "POR DENTRO DO OSSO"
T_FIX, T_PINOS, T_FORA = "FIXADOR", "PINOS ATÉ O OSSO", "POR FORA"
T_CASO = "QUEM DECIDE É O CASO"
T_COLOU, T_TIRAR = "COLOU?", "TIRAR A PLACA?"
T_NEM, T_CIRURGIAO = "NEM SEMPRE", "a decisão é do cirurgião"

# ------------------------------------------------------------------ geometria (mundo)
YF = 760                                  # linha da fratura (a mesma do cf_fratura_cola)
H2 = 64                                   # meia largura da diáfise (HASTE do piloto / 2)
GAP0, GAP1 = 30, 8                        # vão logo depois de quebrar / depois que "cicatriza"
Y_ANEIS = (400, 640, 880, 1080)           # dois anéis acima e dois abaixo da fratura
X_HASTES = 204                            # hastes rosqueadas do piloto
RX = 232                                  # raio do anel do piloto (cf_alongamento.RX)
Y_PERNA = Y_BASE + 45                     # tornozelo da perna desenhada: a borda reta cai na faixa
                                          # de fade da janela e o maléolo fica dentro da pele
CAST0, CAST1 = 420, Y_PERNA + 200         # gesso: logo abaixo do joelho até sair do quadro com a perna
FUNDO_CARTAO = "#0B1824"
COL = 560                                 # coluna dos rótulos (fase dos aparelhos)
JAN0, JAN1 = 226, 1230                    # janela da cena (abaixo do selo, acima da legenda)
BANDA0, BANDA1 = 28, 30                   # fade curto nas bordas da janela (borda de quadro, não névoa)


def _uniao(a, b):
    return skia.Op(a, b, skia.PathOp.kUnion_PathOp)


OSSO = _uniao(path_osso_sup(Y_TOPO, YF + 2), path_osso_inf(YF - 2, Y_BASE))
REG_SUP, REG_INF = _regiao_acima(YF), _regiao_abaixo(YF)
# as duas partes já recortadas: a sombra borrada acompanha o serrilhado (sem faixa clara no vão)
PARTE_SUP = skia.Op(OSSO, REG_SUP, skia.PathOp.kIntersect_PathOp)
PARTE_INF = skia.Op(OSSO, REG_INF, skia.PathOp.kIntersect_PathOp)
ZIG = _zig(YF)

# legenda: palavra de ligação nunca fecha um bloco ("TIRAR A PLACA NEM" / "SEMPRE É NECESSÁRIO."
# lia o contrário da mensagem; "ENTÃO ALGUÉM SEGURA O" / "OSSO...")
LIGA = {"nem", "o", "a", "os", "as", "um", "uma", "do", "da", "de", "e", "ou", "que", "por", "pra",
        "com", "no", "na", "numa"}


def _rejunta(blocos):
    bl = [list(b) for b in blocos]
    for i in range(len(bl) - 1):
        ult = bl[i][-1]
        if (len(bl[i]) > 1 and ult["w"].lower() in LIGA and not ult["fim_frase"] and not ult["virg"]
                and bl[i + 1][0]["w"].lower() != "manda"):
            bl[i + 1].insert(0, bl[i].pop())
    return bl


def zig_y(x):
    """Altura da borda serrilhada de cima (sem vão) na abscissa x."""
    pts = ZIG
    if x <= pts[0][0]:
        return pts[0][1]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return lerp(y0, y1, (x - x0) / (x1 - x0))
    return pts[-1][1]


def _perna_path():
    """O mesmo contorno de perna do piloto (cf_alongamento.perna(cv, Y_PERNA, ...)), como path
    (molde do gesso)."""
    L = Y_PERNA - (Y_TOPO - 50)

    def y(f):
        return Y_TOPO - 50 + L * f
    p = skia.Path()
    p.moveTo(CX - 150, y(0.0))
    p.cubicTo(CX - 168, y(0.10), CX - 200, y(0.22), CX - 196, y(0.36))
    p.cubicTo(CX - 192, y(0.52), CX - 140, y(0.66), CX - 112, y(0.80))
    p.cubicTo(CX - 100, y(0.88), CX - 112, y(0.96), CX - 100, y(1.04))
    p.lineTo(CX + 108, y(1.04))
    p.cubicTo(CX + 112, y(0.95), CX + 104, y(0.88), CX + 112, y(0.80))
    p.cubicTo(CX + 132, y(0.64), CX + 176, y(0.50), CX + 172, y(0.34))
    p.cubicTo(CX + 168, y(0.20), CX + 152, y(0.08), CX + 140, y(0.0))
    p.close()
    return p


def _gesso_path():
    faixa = skia.Path(); faixa.addRect(skia.Rect(0, CAST0, W, CAST1))
    base = skia.Op(_perna_path(), faixa, skia.PathOp.kIntersect_PathOp)
    grosso = skia.Paint(AntiAlias=True); grosso.setStyle(skia.Paint.kStroke_Style); grosso.setStrokeWidth(24)
    grosso.setStrokeJoin(skia.Paint.kRound_Join)
    borda = skia.Path(); grosso.getFillPath(base, borda)
    return _uniao(base, borda)


GESSO = _gesso_path()

# ------------------------------------------------------------------ tempo
def gap(t, T):
    g = GAP0 * e_out(prog(t, T["quebrado"] + 0.06, T["quebrado"] + 0.34))
    g = lerp(g, GAP1, e_inout(prog(t, T["cicatriza"] - 0.25, T["cicatriza"] + 0.35)))
    return lerp(g, 0.0, e_inout(prog(t, T["colou"] + 0.1, T["colou"] + 0.95)))


FREQ = 2.3
CLOSE = (540, 800, 1.30, YF)              # close da fratura (as pontas do osso saem pelas bordas)


def forca_balanco(t, T):
    """Fração do balanço que sobra: cai para 1/3 até "cicatriza" (a vaga ainda está vazia, o osso
    ainda mexe um pouco) e só zera quando o cadeado do gesso fecha ("imobiliza")."""
    f = 1 - 0.67 * e_inout(prog(t, T["segura"], T["cicatriza"]))
    return f * (1 - e_out(prog(t, T["imobiliza"] - 0.05, T["imobiliza"] + 0.1)))


def balanco(t, T):
    """Ângulo (graus) do balanço: as duas partes giram em sentidos opostos em volta da fratura."""
    if t < T["mexe"] or t > T["imobiliza"] + 0.15:
        return 0.0
    amp = 3.6 * e_out(prog(t, T["mexe"], T["mexe"] + 0.3))
    amp += 2.0 * prog(t, T["demais"], T["demais"] + 0.1) * (1 - prog(t, T["demais"] + 0.45, T["demais"] + 0.75))
    amp *= forca_balanco(t, T)
    return amp * math.sin(2 * math.pi * FREQ * (t - T["mexe"]))


def camera(t, T):
    """-> (px, py, s, foco): o ponto (CX, foco) do mundo vai para (px, py) da tela, escala s."""
    px, py, s, fo = 540, 790, 0.88, 725                       # capa: o osso inteiro, centrado
    # fora do close da fratura o osso inteiro (mundo 292..1186) cabe na janela nítida (240..1200)
    for (a, b), alvo in (((T["firme"] + 0.1, T["estavel"] + 0.5), CLOSE),                  # perto da fratura
                         ((T["gesso"] - 0.45, T["gesso"] + 0.25), (320, 775, 0.95, 755)),  # perna + gesso
                         ((T["placa"] - 0.25, T["placa"] + 0.35), (320, 757, 0.95, YF)),   # placa
                         ((T["haste"] - 0.35, T["haste"] + 0.25), (320, 790, 0.90, 740))):  # osso inteiro
        k = e_inout(prog(t, a, b))
        px, py, s, fo = (lerp(px, alvo[0], k), lerp(py, alvo[1], k), lerp(s, alvo[2], k), lerp(fo, alvo[3], k))
    # "qual": a cena encolhe para dentro do 4º cartão (fixador)
    k = e_inout(prog(t, T["qual"], T["qual"] + 0.4))
    if k > 0:
        cx4, cy4 = centro_icone(3)
        px, py, s = lerp(px, cx4, k), lerp(py, cy4 + 10, k), lerp(s, 0.25, k)
    # "colou": volta saindo do cartão da placa
    if t >= T["colou"] - 0.25:
        k = e_inout(prog(t, T["colou"] - 0.22, T["colou"] + 0.35))
        cx2, cy2 = centro_icone(1)
        px, py, s, fo = lerp(cx2, 320, k), lerp(cy2, 757, k), lerp(0.25, 0.95, k), YF
    tremor = 0.0
    for t0, f in ((T["quebrado"] + 0.08, 9), (T["demais"], 7), (T["placa"] + 0.38, 3), (T["nem"] + 0.12, 3)):
        kk = t - t0
        if 0 <= kk < 0.35:
            tremor += f * math.sin(kk * 70) * (1 - kk / 0.35)
    return px + tremor, py, s, fo


def na_tela(cam, x, y):
    px, py, s, fo = cam
    return px + (x - CX) * s, py + (y - fo) * s


def alfa_mundo(t, T):
    """A cena só some/volta quando já está pequena (dentro do cartão): fade longo em tamanho
    grande deixaria o osso translúcido."""
    return 1 - prog(t, T["qual"] + 0.3, T["qual"] + 0.45) * (1 - prog(t, T["colou"] - 0.22, T["colou"] - 0.1))


# ------------------------------------------------------------------ utilidades de desenho
def ponta(cv, x, y, ang, tam, cor, a):
    p = skia.Path()
    p.moveTo(x + tam * math.cos(ang), y + tam * math.sin(ang))
    p.lineTo(x + tam * 0.75 * math.cos(ang + 2.45), y + tam * 0.75 * math.sin(ang + 2.45))
    p.lineTo(x + tam * 0.75 * math.cos(ang - 2.45), y + tam * 0.75 * math.sin(ang - 2.45))
    p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))


def seta(cv, p0, c, p1, cor, a, pr=1.0, larg=6, tam=22):
    """Seta curva (bézier quadrática) de p0 a p1, desenhada até a fração `pr`; contorno escuro
    por baixo para ler sobre o osso marfim."""
    if a <= 0 or pr <= 0:
        return
    n = 24; pts = []
    for i in range(int(n * pr) + 1):
        u = i / n
        pts.append(((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * c[0] + u * u * p1[0],
                    (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * c[1] + u * u * p1[1]))
    if len(pts) < 2:
        return
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    cv.drawPath(p, paint("#0B1824", int(200 * a), "stroke", larg + 6))
    cv.drawPath(p, paint(cor, int(255 * a), "stroke", larg))
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    ang = math.atan2(y1 - y0, x1 - x0)
    ponta(cv, x1, y1, ang, tam + 5, "#0B1824", a * 0.8)
    ponta(cv, x1, y1, ang, tam, cor, a)


def etiqueta(cv, s, x, y, ancora, cor, a, tam=38, cor_txt=None, cor_linha=None):
    """Rótulo com caixa (canto esquerdo em x, linha de base em y) e linha fina até `ancora`.
    `cor_linha`: linha/ponto em outra cor, com contorno escuro (para ler sobre o gesso branco)."""
    if a <= 0:
        return
    x += 26 * (1 - e_out(a))
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    topo, base = y - tam * 1.06, y + tam * 0.36
    if ancora is not None:
        xa, ya = ancora
        cl = cor_linha or cor
        if cor_linha:
            cv.drawLine(xa, ya, x, (topo + base) / 2, paint("#0B1824", int(150 * a), "stroke", 6))
        cv.drawLine(xa, ya, x, (topo + base) / 2, paint(cl, int(210 * a), "stroke", 2.5))
        cv.drawCircle(xa, ya, 6.5, paint("#0B1824", int(200 * a)))
        cv.drawCircle(xa, ya, 5, paint(cl, int(255 * a)))
    rr = skia.RRect.MakeRectXY(skia.Rect(x, topo, x + lw + 32, base), 14, 14)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(220 * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 2.5))
    cv.drawString(s, x + 16, y, f, paint(cor_txt or cor, int(255 * a)))


def carimbo_vermelho(cv, s, x, y, rot, t0, t, dur=1.9, tam=54):
    """O carimbo vermelho do piloto, com tamanho ajustável (a frase é longa)."""
    k = t - t0
    if k < 0 or k > dur:
        return
    esc = lerp(1.9, 1.0, e_out(clamp(k / 0.16))); a = clamp(k / 0.08) * (1 - prog(k, dur - 0.35, dur))
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(esc, esc)
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 24, -tam, lw / 2 + 24, tam * 0.36), 12, 12)
    cv.drawRRect(rr, paint("#0B1824", int(185 * a))); cv.drawRRect(rr, paint(VERMELHO, int(255 * a), "stroke", 7))
    cv.drawString(s, -lw / 2, 0, f, paint(VERMELHO, int(255 * a)))
    cv.restore()


def tracejado_path(cv, pth, cor, a, larg=5, traco=20, vazio=13, fase=0.0):
    if a <= 0:
        return
    p = paint(cor, int(255 * a), "stroke", larg)
    p.setPathEffect(skia.DashPathEffect.Make([traco, vazio], fase))
    cv.drawPath(pth, p)


# ------------------------------------------------------------------ osso
def peca(cv, pth):
    cv.drawPath(pth, paint("#000000", 70, blur=14))
    cv.drawPath(pth, paint(OSSO_C, shader=sombra_osso()))
    cv.drawPath(pth, paint(OSSO_L, 150, "stroke", 2.5))


def osso(cv, g, th):
    """Osso inteiro (g = 0 e sem balanço) ou as duas partes: a de cima gira +th em volta da fratura,
    a de baixo -th em volta da sua ponta, deslocada g para baixo."""
    if g < 0.3 and abs(th) < 1e-3:
        peca(cv, OSSO); return
    for parte, ang, dy in ((PARTE_SUP, th, 0.0), (PARTE_INF, -th, g)):
        cv.save()
        cv.translate(CX, YF + dy); cv.rotate(ang); cv.translate(-CX, -YF)
        peca(cv, parte)
        if g > 1.5:                                               # borda da fratura, bem definida
            cv.save(); cv.clipPath(OSSO, skia.ClipOp.kIntersect, True)
            z = skia.Path(); z.moveTo(*ZIG[0])
            for q in ZIG[1:]:
                z.lineTo(*q)
            cv.drawPath(z, paint(OSSO_L, int(200 * clamp(g / 6)), "stroke", 3))
            cv.restore()
        cv.restore()


def risco(cv, t, T):
    """O risco branco que atravessa a diáfise na palavra "quebrado" (tick seco)."""
    k = t - T["quebrado"]
    if k < 0 or k > 0.7:
        return
    pr = e_out(clamp(k / 0.12)); a = 1 - prog(k, 0.15, 0.7)
    x_fim = lerp(ZIG[0][0], ZIG[-1][0], pr)
    z = skia.Path(); z.moveTo(*ZIG[0])
    for x, y in ZIG[1:]:
        if x > x_fim:
            z.lineTo(x_fim, zig_y(x_fim)); break
        z.lineTo(x, y)
    cv.drawPath(z, paint("#FFFFFF", int(150 * a), "stroke", 16, blur=8))
    cv.drawPath(z, paint("#FFFFFF", int(255 * a), "stroke", 5))
    if k < 0.3:
        cv.drawCircle(CX, YF, 140 * e_out(clamp(k / 0.25)), paint("#FFFFFF", int(120 * (1 - k / 0.3)), blur=30))


RNG = np.random.default_rng(41)
N_ARCO = 11


def pontos_fio(g):
    """Os pontinhos dos fios dourados: [(cadeia, ordem a partir da ponta, x, y)]. Dois arcos por
    fora do osso, de uma parte à outra, e três costuras curtas dentro do vão."""
    pts = []
    for c, sx in enumerate((-1, 1)):
        for i in range(N_ARCO):
            u = i / (N_ARCO - 1)
            x = CX + sx * (H2 + 8 + 38 * math.sin(math.pi * u))
            pts.append((c, min(i, N_ARCO - 1 - i), x, lerp(YF - 40, YF + g + 40, u)))
    for c, dx in enumerate((-32, 0, 32), start=2):
        x = CX + dx; ya = zig_y(x) + 3; yb = zig_y(x) + g - 3
        for i in range(5):
            pts.append((c, min(i, 4 - i), x, lerp(ya, yb, i / 4)))
    return pts


FAISCAS = [(RNG.uniform(0, 2 * math.pi), RNG.uniform(120, 260)) for _ in range(2 * N_ARCO + 15)]


def fios_dourados(cv, t, T, g):
    """"firme": fios dourados pontilhados crescem das duas pontas e QUASE se encontram (o ponto do
    meio pisca: a vontade de colar); "mexe": viram faíscas que se apagam."""
    t0, t1 = T["firme"], T["mexe"]
    if t < t0 or t > t1 + 0.6:
        return
    pts = pontos_fio(g)
    if t < t1:
        pr = e_out(prog(t, t0, t0 + 0.8))
        for c, ordem, x, y in pts:
            meio = ordem == (N_ARCO - 1) // 2 if c < 2 else ordem == 2
            lim = (N_ARCO // 2 + 0.5) if c < 2 else 2.5
            if ordem >= pr * lim:
                continue
            pisca = 0.65 + 0.35 * math.sin(t * 8 + c * 1.7 + ordem)
            if meio:                                              # o elo que não fecha
                pisca *= 0.5 + 0.5 * math.sin(t * 13 + c)
            cv.drawCircle(x, y, 9, paint(NOVO_G, int(100 * pisca), blur=5))
            cv.drawCircle(x, y, 4, paint("#FFE08A", int(255 * pisca)))
        return
    k = t - t1
    a = 1 - k / 0.6
    for (c, ordem, x, y), (ang, v) in zip(pts, FAISCAS):
        px = x + math.cos(ang) * v * k; py = y + math.sin(ang) * v * k + 280 * k * k
        cv.drawCircle(px, py, 10 * a, paint(NOVO_G, int(130 * a), blur=4))
        cv.drawCircle(px, py, 4.2 * a + 0.6, paint("#FFF4CF", int(255 * a)))



def linha_dourada(cv, t, T, g):
    """"cicatriza": a linha da fratura acende em dourado (só brilho); "colou": funde no marfim."""
    a = prog(t, T["cicatriza"] - 0.05, T["cicatriza"] + 0.35)
    if a <= 0:
        return
    funde = e_inout(prog(t, T["colou"] + 0.1, T["colou"] + 0.95))
    if funde >= 1:
        return
    cor = lerpc(NOVO, OSSO_C, funde)
    meio = skia.Path(); zz = _zig(YF + g / 2)
    meio.moveTo(*zz[0])
    for q in zz[1:]:
        meio.lineTo(*q)
    cv.save(); cv.clipRect(skia.Rect(CX - H2 - 12, YF - 60, CX + H2 + 12, YF + 80))
    cv.drawPath(meio, paint(NOVO_G, int(120 * a * (1 - funde)), "stroke", 30, blur=14))
    cv.restore()
    cv.save(); cv.clipRect(skia.Rect(CX - H2 + 1, YF - 40, CX + H2 - 1, YF + 60))
    if g > 0.5:
        cv.drawPath(_vao(g), paint(cor, int(255 * a)))
    cv.drawPath(meio, paint(cor, int(255 * a * (1 - funde)), "stroke", 5))
    xs = CX - H2 + ((t - T["cicatriza"]) * 110) % (2 * H2)            # brilho que corre na linha
    cv.drawCircle(xs, zig_y(xs) + g / 2, 12, paint("#FFF4CF", int(200 * a * (1 - funde)), blur=7))
    cv.restore()


def moldura(cv, t, T, g):
    """"segura": a vaga vazia em volta da fratura (tracejado branco)."""
    a = prog(t, T["segura"] - 0.05, T["segura"] + 0.3) * (1 - prog(t, T["gesso"] - 0.1, T["gesso"] + 0.3))
    if a <= 0:
        return
    esc = lerp(1.08, 1.0, e_out(prog(t, T["segura"] - 0.05, T["segura"] + 0.35)))
    cv.save(); cv.translate(CX, YF + g / 2); cv.scale(esc, esc)
    r = skia.Path(); r.addRRect(skia.RRect.MakeRectXY(skia.Rect(-178, -128 - g / 2, 178, 128 + g / 2), 26, 26))
    cv.drawPath(r, paint("#FFFFFF", int(40 * a), "stroke", 14, blur=8))
    tracejado_path(cv, r, "#FFFFFF", a, larg=5, fase=-t * 24)
    cv.restore()


# ------------------------------------------------------------------ gesso + cadeado
N_FAIXAS = 22
ONDA = 4                                  # quantas voltas se enrolam ao mesmo tempo (onda que desce)


def gesso(cv, t, T):
    pr = prog(t, T["gesso"] + 0.02, T["gesso"] + 0.7)
    a = 1 - prog(t, T["imobiliza"] + 0.55, T["imobiliza"] + 0.9)
    if pr <= 0 or a <= 0:
        return
    cv.saveLayerAlpha(skia.Rect(0, CAST0 - 40, W, CAST1 + 40), int(255 * a))
    cv.save(); cv.clipPath(GESSO, skia.ClipOp.kIntersect, True)
    xl, xr = CX - 240, CX + 240
    alt = (Y_PERNA + 20 - CAST0 + 60) / N_FAIXAS; incl = 30
    sh = skia.GradientShader.MakeLinear([skia.Point(CX - 210, 0), skia.Point(CX + 190, 0)],
                                        [skia.ColorSetRGB(0xC3, 0xCD, 0xD6),
                                         skia.ColorSetRGB(0xF6, 0xF8, 0xFA), skia.ColorSetRGB(0xF6, 0xF8, 0xFA),
                                         skia.ColorSetRGB(0xB8, 0xC3, 0xCD)], [0.0, 0.42, 0.6, 1.0])
    k = pr * (N_FAIXAS + ONDA - 1)
    for i in range(N_FAIXAS):
        f = clamp((k - i) / ONDA)
        if f <= 0:
            break
        y0 = CAST0 - 24 + i * alt
        xe = lerp(xl, xr, e_inout(f))
        p = skia.Path()
        p.moveTo(xl, y0 + incl); p.lineTo(xr, y0); p.lineTo(xr, y0 + alt + 6); p.lineTo(xl, y0 + incl + alt + 6); p.close()
        cv.save(); cv.clipRect(skia.Rect(xl, 0, xe, 3000))
        cv.drawPath(p, paint("#FFFFFF", 255, shader=sh))
        cv.drawLine(xl, y0 + incl, xr, y0, paint("#AEB9C4", 230, "stroke", 2.5))      # borda da volta
        cv.drawLine(xl, y0 + incl + 9, xr, y0 + 9, paint("#FFFFFF", 150, "stroke", 2))
        cv.restore()
        if f < 1:                                                  # a ponta da faixa dando a volta
            ye = lerp(y0 + incl, y0, (xe - xl) / (xr - xl))
            cv.drawLine(xe, ye, xe, ye + alt + 6, paint("#8E9BA8", 200, "stroke", 4, blur=2))
    cv.restore()
    # sombra do contorno só quando o gesso já está quase todo enrolado (antes era um fantasma do
    # gesso futuro atravessando o osso)
    cv.drawPath(GESSO, paint("#000000", int(60 * clamp((pr - 0.85) / 0.15)), "stroke", 6, blur=6))
    if pr >= 1:
        cv.drawPath(GESSO, paint("#9AA8B5", 255, "stroke", 2.5))
    cv.restore()


def cadeado(cv, t, T):
    t0 = T["imobiliza"]
    a = prog(t, t0 - 0.35, t0 - 0.2) * (1 - prog(t, t0 + 0.5, t0 + 0.85))
    if a <= 0:
        return
    esc = lerp(0.5, 1.0, e_back(prog(t, t0 - 0.35, t0 - 0.1)))
    fecha = e_in_back(prog(t, t0 - 0.08, t0 + 0.06), 1.2)
    off = 24 * (1 - fecha)
    x, y = CX, YF + 6
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    k = t - (t0 + 0.06)
    if 0 <= k < 0.7:                                              # clique: anel de brilho
        cv.drawCircle(0, 6, lerp(40, 120, e_out(k / 0.7)), paint(OURO, int(200 * a * (1 - k / 0.7)), "stroke", 6, blur=3))
    alca = skia.Path()
    alca.moveTo(-26, -6 - off); alca.lineTo(-26, -34 - off)
    alca.arcTo(skia.Rect(-26, -60 - off, 26, -8 - off), 180, 180, False)
    alca.lineTo(26, -6 - off * 0.2)
    cv.drawPath(alca, paint("#000000", int(80 * a), "stroke", 15, blur=4))
    cv.drawPath(alca, paint("#C9962E", int(255 * a), "stroke", 12))
    cv.drawPath(alca, paint("#FFE3A0", int(170 * a), "stroke", 3))
    corpo = skia.RRect.MakeRectXY(skia.Rect(-44, -18, 44, 50), 13, 13)
    cv.drawRRect(corpo, paint("#000000", int(90 * a), blur=8))
    cv.drawRRect(corpo, paint(OURO, int(255 * a)))
    cv.drawRRect(corpo, paint("#8A6512", int(255 * a), "stroke", 3))
    cv.drawCircle(0, 10, 8, paint("#5A3E08", int(255 * a)))
    cv.drawRect(skia.Rect(-3.5, 12, 3.5, 30), paint("#5A3E08", int(255 * a)))
    cv.restore()


# ------------------------------------------------------------------ placa e parafusos
FUROS = (-128, -62, 62, 128)


def placa_pos(t, T):
    """-> (dx, levanta, visível): desliza da lateral, sai na "haste", volta no "colou"."""
    if t >= T["colou"] - 0.4:
        lev = 16 * e_out(prog(t, T["tirar"], T["tirar"] + 0.35)) + 3 * math.sin(max(0.0, t - T["tirar"] - 0.35) * 5)
        lev *= 1 - e_in_back(prog(t, T["nem"] - 0.02, T["nem"] + 0.16), 0.8)
        if t >= T["nem"] + 0.16:
            lev = 0.0
        return 0.0, max(0.0, lev), True
    if t < T["placa"] - 0.05 or t > T["haste"] + 0.2:
        return 0.0, 0.0, False
    dx = 720 * (1 - e_out(prog(t, T["placa"] - 0.05, T["placa"] + 0.38)))
    dx += 820 * e_in_back(prog(t, T["haste"] - 0.3, T["haste"] + 0.15))
    return dx, 0.0, True


def placa(cv, t, T, g):
    dx, lev, vis = placa_pos(t, T)
    if not vis:
        return
    y0, y1 = YF - 168, YF + g + 168
    cv.save(); cv.translate(dx, 0)
    sombra = skia.RRect.MakeRectXY(skia.Rect(CX - 24 + 5 + lev * 0.5, y0 + 7 + lev * 0.6, CX + 24 + 5 + lev * 0.5,
                                             y1 + 7 + lev * 0.6), 22, 22)
    cv.drawRRect(sombra, paint("#000000", int(95 - lev * 2), blur=7 + lev * 0.5))
    cv.translate(-lev * 0.25, -lev)
    rr = skia.RRect.MakeRectXY(skia.Rect(CX - 24, y0, CX + 24, y1), 22, 22)
    sh = skia.GradientShader.MakeLinear([skia.Point(CX - 24, 0), skia.Point(CX + 24, 0)],
                                        [skia.ColorSetRGB(0x7D, 0x90, 0xA4), skia.ColorSetRGB(0xC2, 0xD2, 0xE1),
                                         skia.ColorSetRGB(0xA9, 0xBC, 0xCF), skia.ColorSetRGB(0x6E, 0x82, 0x96)],
                                        [0.0, 0.38, 0.62, 1.0])
    cv.drawRRect(rr, paint(ACO, shader=sh))
    cv.drawRRect(rr, paint(ACO_ESC, 255, "stroke", 2.5))
    cv.drawLine(CX - 12, y0 + 22, CX - 12, y1 - 22, paint(ACO_HL, 120, "stroke", 2.5))
    for i, dy in enumerate(FUROS):
        y = (YF if dy < 0 else YF + g) + dy
        cv.drawCircle(CX, y, 11, paint("#44566A"))
        cv.drawCircle(CX, y, 11, paint("#2E3A46", 255, "stroke", 2))
        # cabeças dos parafusos: uma a uma no "parafusos" (sem giro); sempre lá depois do "colou"
        t_i = T["parafusos"] + 0.17 * i
        if t >= T["colou"] - 0.4:
            k = 1.0
        else:
            k = e_back(prog(t, t_i, t_i + 0.22)) if t >= t_i else 0.0
        if k > 0:
            cv.save(); cv.translate(CX, y); cv.scale(k * 0.95, k * 1.45)
            porca(cv, 0, 0, 30, 1.0)
            cv.restore()
            cv.drawCircle(CX, y, 4.2 * k, paint("#6E4E0E"))
            if t < T["colou"] - 0.4 and 0 <= t - t_i < 0.5:
                kk = (t - t_i) / 0.5
                cv.drawCircle(CX, y, lerp(14, 40, e_out(kk)), paint(OURO, int(200 * (1 - kk)), "stroke", 3))
    cv.restore()


# ------------------------------------------------------------------ haste
def haste_lado(cv, t, T):
    a = prog(t, T["haste"] - 0.05, T["haste"] + 0.3) * (1 - prog(t, T["dentro"] - 0.05, T["dentro"] + 0.3))
    if a <= 0:
        return
    x = CX + 162; y0, y1 = 372, 1108
    k = t - T["haste"]
    cv.saveLayerAlpha(skia.Rect(x - 30, y0 - 20, x + 40, y1 + 30), int(255 * a))
    rr = skia.RRect.MakeRectXY(skia.Rect(x - 12, y0, x + 12, y1), 12, 12)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 7, y0 + 8, x + 17, y1 + 8), 12, 12), paint("#000000", 80, blur=8))
    sh = skia.GradientShader.MakeLinear([skia.Point(x - 12, 0), skia.Point(x + 12, 0)],
                                        [skia.ColorSetRGB(0x7D, 0x90, 0xA4), skia.ColorSetRGB(0xD3, 0xDF, 0xEA),
                                         skia.ColorSetRGB(0x6E, 0x82, 0x96)], [0.0, 0.4, 1.0])
    cv.drawRRect(rr, paint(ACO, shader=sh))
    cv.drawRRect(rr, paint(ACO_ESC, 255, "stroke", 2.5))
    if 0 <= k < 0.9:                                              # reflexo que corre na haste
        yy = lerp(y0, y1, e_inout(k / 0.9))
        cv.save(); cv.clipRRect(rr, True)
        cv.drawRect(skia.Rect(x - 12, yy - 40, x + 12, yy + 40), paint("#FFFFFF", int(170 * (1 - k / 0.9)), blur=10))
        cv.restore()
    cv.restore()


def haste_dentro(cv, t, T):
    """Contorno tracejado azul-aço no eixo do osso (o osso continua marfim e opaco)."""
    a = prog(t, T["dentro"], T["dentro"] + 0.35) * (1 - prog(t, T["fixador"] - 0.3, T["fixador"] + 0.1))
    if a <= 0:
        return
    r = skia.Path(); r.addRRect(skia.RRect.MakeRectXY(skia.Rect(CX - 12, 372, CX + 12, 1108), 12, 12))
    k = t - T["dentro"]
    if 0 <= k < 0.9:
        cv.drawPath(r, paint(ACO, int(150 * (1 - k / 0.9)), "stroke", 16, blur=8))
    tracejado_path(cv, r, ACO_ESC, a, larg=5, traco=18, vazio=12)


# ------------------------------------------------------------------ fixador
def fio(cv, y, s, pr, alfa):
    """Um fio do piloto (cf_alongamento.fios), sozinho: atravessa o anel, a perna e o osso."""
    if pr <= 0 or alfa <= 0:
        return
    x0, y0 = CX - RX + 18, y - 14 * s
    x1, y1 = CX + RX - 18, y + 14 * s
    xe, ye = lerp(x0, x1, pr), lerp(y0, y1, pr)
    cv.drawLine(x0, y0, xe, ye, paint("#DDE6EE", int(230 * alfa), "stroke", 3.2))
    if pr < 1:
        cv.drawCircle(xe, ye, 7, paint("#FFFFFF", int(160 * alfa), blur=4))
    else:
        cv.drawCircle(CX - 70 * s, y - 5 * s, 6, paint(OURO, int(255 * alfa)))      # oliva


def t_fio(T, i):
    return T["atravessam"] - 0.05 + 0.16 * i


def fixador_tras(cv, t, T, vis, dx):
    for i in range(4):
        anel(cv, Y_ANEIS[i], dx[i], vis[i], "tras")


def fixador_frente(cv, t, T, vis, dx):
    for i in range(8):
        r, s = divmod(i, 2)
        fio(cv, Y_ANEIS[r], 1 if s else -1, e_inout(prog(t, t_fio(T, i), t_fio(T, i) + 0.24)), vis[r])
    cresce = e_out(prog(t, T["estrutura"] - 0.05, T["estrutura"] + 0.5))
    a_h = min(vis) * prog(t, T["estrutura"] - 0.1, T["estrutura"] + 0.1)
    if a_h > 0:
        yb = lerp(Y_ANEIS[0], Y_ANEIS[3], cresce)
        for sx in (-1, 1):
            x = CX + sx * X_HASTES
            haste(cv, x, Y_ANEIS[0], yb, a_h, rosca=True, fase=0.0)
            for yy in Y_ANEIS:
                if yb >= yy - 1:
                    porca(cv, x, yy - 22 if yy != Y_ANEIS[0] else yy + 22, 15 * sx, a_h)
    for i in range(4):
        anel(cv, Y_ANEIS[i], dx[i], vis[i], "frente")
    k = t - (T["estrutura"] + 0.45)                               # o conjunto "trava" e acende
    if 0 <= k < 1.1:
        g = (1 - k / 1.1) * min(vis)
        for yy in Y_ANEIS:
            cv.drawArc(skia.Rect(CX - RX, yy - 46, CX + RX, yy + 46), 0, 360, False,
                       paint(ACO_HL, int(200 * g), "stroke", 8, blur=6))
        for sx in (-1, 1):
            cv.drawLine(CX + sx * X_HASTES, Y_ANEIS[0], CX + sx * X_HASTES, Y_ANEIS[3],
                        paint(ACO_HL, int(200 * g), "stroke", 8, blur=6))
    k = t - T["fora"]                                             # "por fora": os anéis pulsam
    if 0 <= k < 0.9:
        g = math.sin(math.pi * k / 0.9) * min(vis)
        for yy in Y_ANEIS:
            cv.drawArc(skia.Rect(CX - RX, yy - 46, CX + RX, yy + 46), 0, 180, False,
                       paint(OURO, int(170 * g), "stroke", 10, blur=5))


def estado_aneis(t, T):
    p = [e_back(prog(t, T["fixador"] + 0.07 * i, T["fixador"] + 0.07 * i + 0.55)) for i in range(4)]
    fim = t >= T["colou"] - 0.4
    vis = [0.0 if fim else clamp(p[i] * 3) for i in range(4)]
    dx = [(-900 if i < 2 else 900) * (1 - p[i]) for i in range(4)]
    return vis, dx


# ------------------------------------------------------------------ mundo
def mundo(cv, t, T):
    g = gap(t, T)
    th = balanco(t, T)
    a_perna = max(prog(t, T["gesso"] - 0.25, T["gesso"] + 0.25) * (1 - prog(t, T["imobiliza"] + 0.55, T["imobiliza"] + 0.9)),
                  prog(t, T["fixador"] - 0.1, T["fixador"] + 0.4) * (1 - prog(t, T["colou"] - 0.45, T["colou"] - 0.4)))
    perna(cv, Y_PERNA, a_perna)
    vis, dx = estado_aneis(t, T)
    fixador_tras(cv, t, T, vis, dx)
    haste_lado(cv, t, T)
    osso(cv, g, th)
    risco(cv, t, T)
    fios_dourados(cv, t, T, g)
    linha_dourada(cv, t, T, g)
    haste_dentro(cv, t, T)
    placa(cv, t, T, g)
    gesso(cv, t, T)
    # o clique do cadeado é o que para o osso: os brilhos saem de trás dele (por cima do gesso)
    brilhos(cv, CX, YF + 6, t, T["imobiliza"] + 0.1, n=12, raio=200)
    cadeado(cv, t, T)
    fixador_frente(cv, t, T, vis, dx)
    moldura(cv, t, T, g)


# ------------------------------------------------------------------ cartões (painel 2x2)
CARD_W, CARD_H = 450, 360
CARDS = ((75, 268), (555, 268), (75, 790), (555, 790))


def centro_icone(i):
    x, y = CARDS[i]
    return x + CARD_W / 2, y + 150


def _abre(cv, x, y, esc):
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)


def icone_gesso(cv, x, y, esc, alfa):
    """Copiado de animado/icones.py (gesso de perna, com a trama das faixas)."""
    A = int(255 * alfa); _abre(cv, x, y, esc)
    p = skia.Path()
    p.moveTo(-22, -52); p.lineTo(22, -52); p.lineTo(20, 18)
    p.cubicTo(22, 30, 40, 34, 46, 44); p.lineTo(46, 54); p.lineTo(-20, 54)
    p.cubicTo(-26, 40, -24, 24, -22, 12); p.close()
    cv.drawPath(p, paint("#000000", int(A * 0.35), blur=5))
    cv.drawPath(p, paint("#F4F6F8", A))
    for k in range(7):
        yy = -44 + k * 13
        cv.drawLine(-22, yy, 22, yy + 7, paint("#C9D3DC", A, "stroke", 2))
    cv.drawPath(p, paint("#9AA8B5", A, "stroke", 2.5))
    for k in range(4):
        cv.drawCircle(48 + (k % 2) * 2, 36 + k * 5, 4.2, paint("#F0B49A", A))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-26, -58, 26, -50), 4, 4), paint(OURO, A))
    cv.restore()


def icone_fixador(cv, x, y, esc, alfa):
    """Copiado de animado/icones.py (anéis, fios e hastes em volta de um osso)."""
    A = int(255 * alfa); _abre(cv, x, y, esc)
    for yy in (-30, 0, 30):
        cv.drawArc(skia.Rect(-40, yy - 9, 40, yy + 9), 180, 180, False, paint(ACO_ESC, A, "stroke", 4.5))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-10, -48, 10, 48), 6, 6), paint(OSSO_C, A))
    cv.drawRect(skia.Rect(-15, -50, 15, -40), paint(OSSO_C, A))
    for yy in (-30, 0, 30):
        cv.drawLine(-34, yy - 5, 34, yy + 5, paint("#DDE6EE", A, "stroke", 1.6))
        cv.drawLine(-34, yy + 5, 34, yy - 5, paint("#DDE6EE", A, "stroke", 1.6))
    for sx in (-34, 34):
        cv.drawLine(sx, -30, sx, 30, paint("#8FA3B8", A, "stroke", 3.5))
    for yy in (-30, 0, 30):
        cv.drawArc(skia.Rect(-40, yy - 9, 40, yy + 9), 0, 180, False, paint(ACO, A, "stroke", 4.5))
        cv.drawCircle(-34, yy + 1, 3, paint(OURO, A)); cv.drawCircle(34, yy + 1, 3, paint(OURO, A))
    cv.restore()


def _osso_mini(cv, A):
    """O osso do ícone 'osso' de animado/icones.py, sem o calo (mesmo traço dos outros ícones)."""
    p = skia.Path()
    p.moveTo(-12, -40); p.lineTo(12, -40)
    p.cubicTo(30, -40, 30, -62, 14, -58); p.cubicTo(8, -66, -8, -66, -14, -58)
    p.cubicTo(-30, -62, -30, -40, -12, -40); p.close()
    p.addRect(skia.Rect(-12, -42, 12, 42))
    q = skia.Path()
    q.moveTo(-12, 40); q.lineTo(12, 40)
    q.cubicTo(30, 40, 30, 62, 14, 58); q.cubicTo(8, 66, -8, 66, -14, 58)
    q.cubicTo(-30, 62, -30, 40, -12, 40); q.close()
    for pp in (p, q):
        cv.drawPath(pp, paint(OSSO_C, A)); cv.drawPath(pp, paint(OSSO_L, A, "stroke", 2))
    cv.drawLine(-12, 2, -4, -2, paint(OSSO_L, A, "stroke", 2)); cv.drawLine(-4, -2, 4, 2, paint(OSSO_L, A, "stroke", 2))
    cv.drawLine(4, 2, 12, -2, paint(OSSO_L, A, "stroke", 2))


def icone_placa(cv, x, y, esc, alfa):
    A = int(255 * alfa); _abre(cv, x, y, esc)
    _osso_mini(cv, A)
    rr = skia.RRect.MakeRectXY(skia.Rect(-6, -32, 6, 32), 6, 6)
    cv.drawRRect(rr, paint(ACO, A)); cv.drawRRect(rr, paint(ACO_ESC, A, "stroke", 1.6))
    for yy in (-24, -11, 11, 24):
        cv.drawCircle(0, yy, 3.2, paint(OURO, A))
    cv.restore()


def icone_haste(cv, x, y, esc, alfa):
    A = int(255 * alfa); _abre(cv, x, y, esc)
    _osso_mini(cv, A)
    r = skia.Path(); r.addRRect(skia.RRect.MakeRectXY(skia.Rect(-4.5, -52, 4.5, 52), 4.5, 4.5))
    p = paint(ACO_ESC, A, "stroke", 2.2); p.setPathEffect(skia.DashPathEffect.Make([6, 4], 0))
    cv.drawPath(r, p)
    cv.restore()


ICONES_CARTAO = ((icone_gesso, T_GESSO), (icone_placa, T_PLACA), (icone_haste, T_HASTE), (icone_fixador, T_FIX))


def cartoes(cv, t, T):
    sai = e_in_back(prog(t, T["colou"] - 0.45, T["colou"] - 0.18))
    if t < T["qual"] or sai >= 1:
        return
    for i, ((x, y), (icone, nome)) in enumerate(zip(CARDS, ICONES_CARTAO)):
        t0 = T["qual"] + (0.2, 0.28, 0.38, 0.46)[i]
        k = prog(t, t0, t0 + 0.4)
        if k <= 0:
            continue
        a = clamp(k * 3) * (1 - prog(t, T["colou"] - 0.4, T["colou"] - 0.18))
        esc = lerp(0.7, 1.0, e_back(k)) * (1 - 0.25 * sai)
        cx, cy = x + CARD_W / 2, y + CARD_H / 2
        cv.save(); cv.translate(cx, cy); cv.scale(esc, esc); cv.translate(-cx, -cy)
        rr = skia.RRect.MakeRectXY(skia.Rect(x, y, x + CARD_W, y + CARD_H), 26, 26)
        cv.drawRRect(rr, paint("#000000", int(90 * a), blur=14))
        cv.drawRRect(rr, paint(FUNDO_CARTAO, int(225 * a)))
        cv.drawRRect(rr, paint(OURO, int(190 * a), "stroke", 2.5))
        xi, yi = centro_icone(i)
        # o cartão do fixador recebe a cena encolhendo: o ícone só acende quando ela some
        a_ic = a * (prog(t, T["qual"] + 0.32, T["qual"] + 0.48) if i == 3 else 1.0)
        icone(cv, xi, yi, 1.9, a_ic)
        texto(cv, nome, cx, y + CARD_H - 34, F_BLACK, 34, "#FFFFFF", int(255 * a))
        cv.restore()
    a = prog(t, T["qual"] + 0.45, T["qual"] + 0.65) * (1 - prog(t, T["caso"] - 0.1, T["caso"] + 0.12))
    if a > 0:                                                     # "?" no centro, pulsando
        pul = 1 + 0.12 * math.sin((t - T["qual"]) * 7)
        cv.save(); cv.translate(540, 709); cv.scale(pul, pul)
        cv.drawCircle(0, 0, 50, paint(FUNDO_CARTAO, int(240 * a)))
        cv.drawCircle(0, 0, 50, paint(OURO, int(255 * a), "stroke", 4))
        cv.drawCircle(0, 0, 58, paint(OURO, int(70 * a), blur=10))
        texto(cv, T_INTERROG, 0, 25, F_BLACK, 70, OURO, int(255 * a))
        cv.restore()


# ------------------------------------------------------------------ rótulos (tela)
def rotulos(cv, t, T, cam):
    # fase 1: instabilidade
    carimbo_vermelho(cv, T_MEXE, 540, 590, -6, T["demais"] - 0.02, t, dur=T["segura"] - T["demais"] - 0.2)
    a = prog(t, T["segura"] + 0.05, T["segura"] + 0.35) * (1 - prog(t, T["gesso"] - 0.25, T["gesso"] + 0.05))
    if a > 0:
        g = gap(t, T)
        xc, ytop = na_tela(cam, CX, YF - 128)
        lw = larg_texto(T_QUEM, F_BLACK, 44)
        etiqueta(cv, T_QUEM, xc - (lw + 32) / 2 - 26 * (1 - e_out(a)), ytop - 26, None, "#FFFFFF", a, tam=44)
        xq, yq = na_tela(cam, CX + 122, YF + g / 2)
        pul = 1 + 0.14 * math.sin((t - T["segura"]) * 7.5)
        cv.save(); cv.translate(xq, yq + 30); cv.scale(pul, pul)
        texto(cv, T_INTERROG, 0, 0, F_BLACK, 86, OURO, int(255 * a), contorno=10)
        cv.restore()
    # gesso
    a_out = 1 - prog(t, T["imobiliza"] + 0.45, T["imobiliza"] + 0.8)
    etiqueta(cv, T_GESSO, COL, 560, na_tela(cam, CX + 168, 650), OURO,
             prog(t, T["gesso"] + 0.1, T["gesso"] + 0.4) * a_out)
    etiqueta(cv, T_IMOB, COL, 712, na_tela(cam, CX + 46, YF + 22), "#FFFFFF",       # linha dourada até o
             prog(t, T["imobiliza"] + 0.08, T["imobiliza"] + 0.38) * a_out, cor_linha=OURO)  # cadeado
    # placa
    a = prog(t, T["placa"] + 0.15, T["placa"] + 0.45) * (1 - prog(t, T["haste"] - 0.4, T["haste"] - 0.1))
    etiqueta(cv, T_PLACA, COL, 560, na_tela(cam, CX + 25, YF - 100), OURO, a)
    # haste
    a = prog(t, T["haste"] + 0.1, T["haste"] + 0.4) * (1 - prog(t, T["fixador"] - 0.35, T["fixador"] - 0.05))
    k = e_inout(prog(t, T["dentro"] - 0.05, T["dentro"] + 0.3))
    etiqueta(cv, T_HASTE, COL, 540, na_tela(cam, lerp(CX + 174, CX + 12, k), 560), OURO, a)
    a = prog(t, T["dentro"] + 0.15, T["dentro"] + 0.45) * (1 - prog(t, T["fixador"] - 0.35, T["fixador"] - 0.05))
    if a > 0:
        etiqueta(cv, T_DENTRO, COL, 700, None, "#FFFFFF", a, tam=34)
        x1, y1 = na_tela(cam, CX + 14, 830)
        seta(cv, (COL + 4, 690), (COL - 120, 700), (x1 + 6, y1 - 10), OURO, a,
             pr=e_out(prog(t, T["dentro"] + 0.2, T["dentro"] + 0.6)))
    # fixador
    a_fim = 1 - prog(t, T["qual"] - 0.1, T["qual"] + 0.12)
    etiqueta(cv, T_FIX, COL, 470, na_tela(cam, CX + RX * 0.8, Y_ANEIS[0] + 28), OURO,
             prog(t, T["fixador"] + 0.35, T["fixador"] + 0.65) * a_fim)
    etiqueta(cv, T_PINOS, COL, 640, na_tela(cam, CX + H2 + 4, Y_ANEIS[1] + 4), "#FFFFFF",
             prog(t, T["atravessam"] + 0.1, T["atravessam"] + 0.4) * a_fim)
    a = prog(t, T["fora"] - 0.02, T["fora"] + 0.28) * a_fim
    if a > 0:
        etiqueta(cv, T_FORA, COL + 40, 838, None, OURO, a, tam=40)
        x1, y1 = na_tela(cam, CX + RX + 4, Y_ANEIS[2] + 6)
        seta(cv, (COL + 56, 846), (COL + 10, 905), (x1 + 8, y1 + 4), OURO, a, pr=e_out(prog(t, T["fora"], T["fora"] + 0.35)))
    # cartões + carimbo
    cartoes(cv, t, T)
    carimbo_ouro(cv, T_CASO, 540, 730, -4, T["caso"] - 0.02, t, dur=T["colou"] - T["caso"] - 0.25, tam=60)
    # colou / tirar / nem sempre
    etiqueta(cv, T_COLOU, COL, 520, na_tela(cam, CX + H2 + 2, YF + 4), OURO,
             prog(t, T["colou"] + 0.1, T["colou"] + 0.4) * (1 - prog(t, T["nem"] - 0.1, T["nem"] + 0.2)))
    a_cta = 1 - prog(t, T["manda"] - 0.4, T["manda"] - 0.15)
    # âncora na metade de baixo da placa: a linha passa por baixo da de COLOU? (não se cruzam)
    etiqueta(cv, T_TIRAR, COL, 640, na_tela(cam, CX + 26, YF + 110), "#FFFFFF",
             prog(t, T["tirar"] + 0.05, T["tirar"] + 0.35) * a_cta)
    cartao_nem(cv, t, T, a_cta)


def cartao_nem(cv, t, T, a_cta):
    k = t - (T["nem"] + 0.08)
    if k < 0 or a_cta <= 0:
        return
    a = clamp(k / 0.15) * a_cta
    esc = lerp(0.6, 1.0, e_back(clamp(k / 0.4)))
    w1 = larg_texto(T_NEM, F_BLACK, 56); w2 = larg_texto(T_CIRURGIAO, F_SEMI, 34)
    w = max(w1, w2) + 56; x0, y0, h = COL, 700, 170
    cv.save(); cv.translate(x0 + w / 2, y0 + h / 2); cv.scale(esc, esc); cv.translate(-(x0 + w / 2), -(y0 + h / 2))
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x0 + w, y0 + h), 24, 24)
    acende = 1 - clamp(k / 0.9)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0 - 8, y0 - 8, x0 + w + 8, y0 + h + 8), 30, 30),
                 paint(NOVO_G, int(a * (50 + 150 * acende)), blur=18))
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(235 * a)))
    cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 4))
    texto(cv, T_NEM, x0 + w / 2, y0 + 80, F_BLACK, 56, OURO, int(255 * a))
    texto(cv, T_CIRURGIAO, x0 + w / 2, y0 + 132, F_SEMI, 34, "#FFFFFF", int(255 * a))
    cv.restore()


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    cam = camera(t, T)
    a_m = alfa_mundo(t, T)
    if a_m > 0:
        # janela da cena: entre o selo e a legenda, com fade CURTO só nas duas bordas (no close da
        # fratura as pontas do osso saem do quadro como num enquadramento, sem virar névoa).
        # Camada limitada à janela e máscara DstIn só nas duas faixas (desempenho).
        jan = skia.Rect(0, JAN0, W, JAN1)
        cv.save(); cv.clipRect(jan)
        cv.saveLayerAlpha(jan, int(255 * a_m))
        px, py, s, fo = cam
        cv.save(); cv.translate(px, py); cv.scale(s, s); cv.translate(-CX, -fo)
        mundo(cv, t, T)
        cv.restore()
        for ya, yb, c0, c1 in ((JAN0, JAN0 + BANDA0, 0, 255), (JAN1 - BANDA1, JAN1, 255, 0)):
            masc = skia.Paint(AntiAlias=True)
            masc.setShader(skia.GradientShader.MakeLinear(
                [skia.Point(0, ya), skia.Point(0, yb)],
                [skia.ColorSetARGB(c0, 0, 0, 0), skia.ColorSetARGB(c1, 0, 0, 0)]))
            masc.setBlendMode(skia.BlendMode.kDstIn)
            cv.drawRect(skia.Rect(0, ya, W, yb), masc)
        cv.restore()
        cv.restore()
    rotulos(cv, t, T, cam)
    capa(cv, t, T["firme"] - 0.1, ep["gancho"][0], ep["gancho"][1])
    selo_como_funciona(cv, prog(t, T["firme"] + 0.3, T["firme"] + 0.7) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface(cv, t, T, _rejunta(blocos), DESTAQUE)


# ------------------------------------------------------------------ som e prévias
def sons(T):
    ev = [(T["quebrado"] + 0.04, "tick", 1.0), (T["quebrado"] + 0.08, "thump", 0.55),
          (T["firme"] + 0.05, "shimmer", 0.35), (T["mexe"], "pop", 0.6), (T["demais"] - 0.02, "thump", 0.9),
          (T["segura"], "whoosh", 0.35), (T["cicatriza"] + 0.05, "shimmer", 0.8),
          (T["gesso"], "whoosh", 0.5), (T["imobiliza"] + 0.06, "tick", 0.9), (T["imobiliza"] + 0.1, "ding", 0.3),
          (T["placa"] - 0.05, "whoosh", 0.5), (T["placa"] + 0.38, "thump", 0.45),
          (T["haste"] - 0.3, "whoosh", 0.45), (T["haste"] + 0.05, "ping", 0.45), (T["dentro"], "shimmer", 0.35),
          (T["fixador"] - 0.05, "whoosh", 0.55), (T["estrutura"] + 0.45, "ding", 0.4), (T["fora"], "pop", 0.55),
          (T["qual"] + 0.05, "whoosh", 0.45), (T["caso"] - 0.02, "thump", 0.9),
          (T["colou"] - 0.22, "whoosh", 0.35), (T["colou"] + 0.12, "crackle", 0.75),
          (T["tirar"], "whoosh", 0.22), (T["nem"] + 0.14, "thump", 0.4), (T["nem"] + 0.1, "pop", 0.55),
          (T["manda"] + 0.05, "whoosh", 0.5)]
    ev += [(T["parafusos"] + 0.17 * i, "tick", 0.75) for i in range(4)]            # um tic por cabeça
    ev += [(T["fixador"] + 0.07 * i + 0.4, "ping", 0.5) for i in range(4)]        # anéis encaixando
    ev += [(t_fio(T, i) + 0.2, "ping", 0.32) for i in range(8)]                    # um fio de cada vez
    ev += [(T["estrutura"] + 0.1 * i, "click", 0.8) for i in range(4)]             # hastes travando
    ev += [(T["qual"] + d, "pop", 0.45) for d in (0.2, 0.28, 0.38, 0.46)]            # cartões
    # osso solto: um estalido em cada ida e volta do balanço, mais fraco quando o balanço diminui;
    # o último é logo antes do cadeado fechar
    k = 0
    while True:
        tk = T["mexe"] + (k + 0.5) / (2 * FREQ)
        if tk >= T["imobiliza"] - 0.05:
            break
        ev.append((tk, "click", 0.55 * forca_balanco(tk, T)))
        k += 1
    return ev


def tempos_previa(T):
    return [0.3, T["firme"] + 0.5, T["demais"] + 0.35, T["segura"] + 0.8, T["imobiliza"] + 0.3,
            T["parafusos"] + 0.8, T["dentro"] + 0.6, T["fora"] + 0.4, T["caso"] + 0.4, T["nem"] + 0.9,
            T["manda"] + 1.6]


render = fazer_render(quadro, ANCORAS, sons, tempos_previa, respiro_cta=2.0)
