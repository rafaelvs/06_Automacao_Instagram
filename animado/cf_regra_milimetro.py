# -*- coding: utf-8 -*-
"""COMO FUNCIONA — a regra do milímetro ("1 MM POR DIA. / POR QUE NÃO MAIS?").

Mesmo estilo e mesmas peças do cf_alongamento (tíbia marfim, osso novo dourado, anel/fio com oliva/
haste com porca do fixador, brilhos, regenerado que endurece, legenda karaokê, CTA com aviãozinho).
Código de cor: VERMELHO = errado (zona RÁPIDO DEMAIS e os carimbos de falha); DOURADO = ritmo certo
(zona do meio, DE PROPÓSITO no carimbo dourado do cf_comum, osso novo, PILOTO AUTOMÁTICO).
Um mostrador em meio círculo, SEM número e SEM rótulo na capa (3 zonas só de cor: cinza-azulado à
esquerda, dourado no meio, vermelho à direita), comanda o ritmo; cada coisa é disparada pela palavra:
  * capa (t=0): o gancho é o ÚNICO texto; a tíbia com o corte fino e dois anéis, o ponteiro no meio.
    Nada se mexe até "rápido";
  * "rápido": o ponteiro bate no vermelho (acende RÁPIDO DEMAIS) e a parte de baixo desce de uma
    vez, cliques emendados, o vão abre largo; "novo"/"forma": duas ou três faíscas douradas no vão
    se apagam (nenhum dourado se firma) e o carimbo O OSSO NOVO NÃO SE FORMA; "tecido": seis linhas
    finas cor de areia (faixa genérica, sem nervo, vaso, músculo ou vermelho) cruzam o vão; "estica":
    a parte de baixo dá mais um tranco e é ELE que as retesa (tremor de corda) — nada se rompe;
  * "isso": o filme volta (ícone de rebobinar; o mostrador apaga e o ponteiro se aquieta): o vão fecha
    até o corte fino e as linhas somem; "milímetro": o ponteiro vai ao dourado (acende 'cerca de' /
    1 MM POR DIA); a partir daí as partes se afastam em passos pequenos e iguais, um clique por passo,
    e um fio dourado fino nasce no vão ("pequenos": PEQUENOS AJUSTES); "propósito": carimbo DOURADO
    DE PROPÓSITO, que sai antes de "E devagar demais";
  * "demais": o ponteiro vai ao cinza-azulado (DEVAGAR DEMAIS), cliques bem espaçados, o vão quase
    não cresce; "endurece": a lasca dourada perde o brilho e amadurece como no piloto (dourado → marfim,
    estrias longitudinais que somem), soldando as pontas cedo (ENDURECE / ANTES DA HORA); "trava":
    DEVAGAR DEMAIS sai, cadeado fecha com estalo, a parte de baixo tenta mais um passo e só treme, e
    uma linha tracejada sem texto marca até onde o osso deveria ir (TRAVA A CORREÇÃO);
  * "certo": o cadeado abre e some, o filme volta de novo ao corte fino (o osso que endureceu NÃO
    "amolece": é outra tentativa, desde o começo), o ponteiro volta ao meio e a zona dourada pulsa
    (RITMO CERTO); "preenche": o vão abre em 8 passos (anda e PARA, um clique cada; vão final bem
    menor que o do rápido) e se enche de osso novo dourado com estrias no sentido da tração
    (desenha_regenerado do piloto) — OSSO NOVO —, e em "ponte" o dourado liga as duas pontas até a
    linha tracejada, com brilhos (PONTE);
  * "acompanhado": lupa só de contorno chega e aumenta o MESMO desenho (nada de imagem de exame) —
    ACOMPANHADO / DE PERTO, rótulo só depois que ela assenta; "equipe": o ponteiro faz pequenas
    correções e assenta no meio (PELA EQUIPE; nenhuma mão, chave ou pessoa); lupa e rótulos encolhem
    e saem no lugar; "piloto": carimbo NÃO EXISTE / PILOTO AUTOMÁTICO por cima do mostrador limpo,
    saindo junto com ele; respiro: o osso com a ponte dourada vai ao centro e entra a CTA.
Todo texto desenhado está em ep["tela"] (o render recusa o vídeo se não estiver). Nenhum número na
tela além do 1 MM POR DIA (gancho e legenda); passos e cliques não viram contador.
"""
import math

import skia

from .cf_comum import capa, carimbo, fazer_render, interface, selo_como_funciona
from .cf_alongamento import (ACO, ACO_ESC, ACO_HL, CX, F_BLACK, F_SEMI, HASTE, NOVO, NOVO_G,
                             OSSO_C, OSSO_L, OURO, VERMELHO, W, H, brilhos,
                             clamp, desenha_regenerado, e_back, e_inout, e_out, fundo, haste, larg_texto,
                             lerp, lerpc, paint, path_osso_inf, path_osso_sup, porca, prog, sombra_osso, texto)

ANCORAS = {
    "rapido": ("rápido", 1, False), "novo1": ("novo", 1, False), "forma": ("forma", 1, False),
    "tecido": ("tecido", 1, False), "estica": ("estica", 1, False), "isso": ("isso", 1, False),
    "milimetro": ("milímetro", 1, False), "pequenos": ("pequenos", 1, False),
    "proposito": ("propósito", 1, False), "devagar2": ("devagar", 2, False),
    "demais": ("demais", 1, False), "endurece": ("endurece", 1, False),
    "antes": ("antes", 1, False), "trava": ("trava", 1, False), "certo": ("certo", 1, False),
    "preenche": ("preenche", 1, False), "novo2": ("novo", 2, False), "ponte": ("ponte", 1, False),
    "acompanhado": ("acompanhado", 1, False), "perto": ("perto", 1, False), "equipe": ("equipe", 1, False),
    "piloto": ("piloto", 1, False), "manda": ("manda", 1, False),
}
DESTAQUE = {"rápido", "forma", "estica", "milímetro", "dia", "ajustes", "propósito", "demais", "endurece",
            "trava", "correção", "certo", "preenche", "ponte", "acompanhado", "equipe", "piloto", "automático"}

# ------------------------------------------------------------------ paleta própria
LENTO = "#7F95AD"            # zona cinza-azulada do mostrador
LENTO_TXT = "#B9CADB"
AREIA = "#E4CB9E"            # linhas do tecido (faixa genérica, nunca vermelha)
AMBAR = "#7A5420"            # base opaca do osso novo (nada translúcido sobre o azul)
CAIXA = "#0B1824"
AZUL = "#9CC9FF"

# ------------------------------------------------------------------ geometria (mundo, antes da câmera)
Y_TOPO, Y_CORTE, Y_BASE = 300, 640, 950      # tíbia um pouco menor que a do piloto
Y_ALTO = 282                                   # topo do platô (referência da câmera)
FENDA = 6                                      # o corte fino
H2 = HASTE / 2
RX2, RY2 = 190, 40                             # anel um pouco menor: sobra a coluna da direita
X_HASTE = 165
Y_AN_SUP, DY_AN_INF = 440, 160                 # anel de cima; anel de baixo (abaixo do topo da parte de baixo)
G_RAPIDO = 138                                 # o vão do "rápido demais" (esquema: NÃO vai para a tela)
TRANCO = 14                                    # o último puxão no "estica" (é ele que retesa o tecido)
N_RAPIDO = 12
PASSO2, PER2 = 6, 0.48                         # ritmo certo: passos pequenos e iguais
PASSO3 = 3                                     # devagar demais: quase não cresce
N4 = 8                                         # ritmo certo (ponte): 8 passos, cada um anda e PARA
G4 = 112                                       # bem menor que o vão do rápido (152): não é "rápido que deu certo"
PASSO4 = G4 / N4
LUPA_CHEGA = 0.65                              # a lupa assenta antes de "de perto"

# câmera: (x na tela do eixo do osso, y na tela do topo do platô, escala)
CAM = (400.0, 372.0, 0.98)                      # osso à esquerda; mostrador e rótulos à direita
CAM_FIM = (540.0, 372.0, 0.98)                  # respiro: osso centralizado atrás da CTA

# mostrador (tela)
DX, DY, DR = 815, 600, 128
A_LENTO, A_CERTO, A_RAPIDO = 207.0, 270.0, 333.0

X_COL = 628                                    # coluna dos rótulos (direita)


# ------------------------------------------------------------------ tempo
def degraus(t, inicios, passo, d):
    """Soma de passos iguais (anda e para): cada um leva `d` s, começando em cada `inicio`."""
    return passo * sum(e_inout(clamp((t - s) / d)) for s in inicios if t > s)


def agenda(T):
    """Instantes de cada passo e das duas voltas do filme (derivados das palavras)."""
    A = {}
    t1 = T["rapido"] + 0.06
    A["p1"] = [t1 + i * 0.047 for i in range(N_RAPIDO)]                 # cliques emendados
    A["p1b"] = [T["estica"] + 0.02]                                      # o tranco que retesa o tecido
    A["rew1"] = (T["isso"] + 0.2, T["isso"] + 0.85)
    t2 = T["milimetro"] + 0.45
    A["p2"] = [t2 + i * PER2 for i in range(40) if t2 + i * PER2 < T["demais"] - 0.15]
    A["p3"] = [T["demais"] + 0.6, T["demais"] + 1.5]                     # bem espaçados
    A["tenta"] = T["trava"] + 0.42                                       # tenta mais um passo e só treme
    A["rew2"] = (T["certo"] + 0.05, T["certo"] + 0.7)
    t4a, t4b = T["preenche"] + 0.02, T["ponte"] - 0.18
    A["p4"] = [lerp(t4a, t4b, i / (N4 - 1)) for i in range(N4)]
    A["g3"] = PASSO2 * len(A["p2"]) + PASSO3 * len(A["p3"])
    return A


def vao(t, T, A):
    """Quanto as partes já se afastaram (px do mundo, sem contar o corte fino)."""
    r1a, r1b = A["rew1"]; r2a, r2b = A["rew2"]
    if t < r1a:
        return degraus(t, A["p1"], G_RAPIDO / N_RAPIDO, 0.06) + degraus(t, A["p1b"], TRANCO, 0.08)
    if t < r1b:
        return lerp(G_RAPIDO + TRANCO, 0, e_inout(prog(t, r1a, r1b)))
    if t < r2a:
        return degraus(t, A["p2"], PASSO2, 0.14) + degraus(t, A["p3"], PASSO3, 0.3)
    if t < r2b:
        return lerp(A["g3"], 0, e_inout(prog(t, r2a, r2b)))
    return degraus(t, A["p4"], PASSO4, 0.1)                         # anda 0,1 s e PARA ~0,15 s


def tremor_trava(t, A):
    k = t - A["tenta"]
    if 0 <= k < 0.55:
        return 4.5 * math.sin(k * 58) * (1 - k / 0.55)
    return 0.0


def angulo(t, T):
    """Ponteiro: mola amortecida entre as posições (sobe e assenta, como um ponteiro de verdade)."""
    eq = T["equipe"]
    alvos = [(T["rapido"], A_RAPIDO, 7.5, 15.0), (T["milimetro"] - 0.02, A_CERTO, 5.5, 11.0),
             (T["demais"], A_LENTO, 5.5, 11.0), (T["certo"], A_CERTO, 5.5, 11.0),
             (eq + 0.05, 261.0, 6.0, 12.0), (eq + 0.42, 278.0, 6.0, 12.0), (eq + 0.8, 270.0, 5.0, 10.0)]
    ang, ant = A_CERTO, A_CERTO
    for t0, alvo, z, w in alvos:
        if t < t0:
            break
        k = t - t0
        ang = alvo + (ant - alvo) * math.exp(-z * k) * math.cos(w * k)
        ant = alvo
    # no vermelho o ponteiro não para quieto — mas se aquieta quando o filme volta (não é "voltando rápido")
    rew1 = T["isso"] + 0.2
    no_vermelho = prog(t, T["rapido"] + 0.3, T["rapido"] + 0.5) * (1 - prog(t, rew1 - 0.1, rew1 + 0.1))
    return ang + 1.8 * math.sin(t * 43) * no_vermelho


def camera(t, T):
    a = e_inout(prog(t, T["piloto"] + 1.05, T["piloto"] + 2.05))
    ax = lerp(CAM[0], CAM_FIM[0], a)
    tremor = 0.0
    for t0, forca in ((T["rapido"] + 0.62, 9), (T["forma"], 5), (T["estica"] + 0.08, 4), (T["trava"] + 0.12, 7),
                      (T["piloto"], 4)):
        k = t - t0
        if 0 <= k < 0.35:
            tremor += forca * math.sin(k * 70) * (1 - k / 0.35)
    return ax + tremor, CAM[1], CAM[2]


def aplica(cv, cam):
    ax, sy, s = cam
    cv.translate(ax, sy); cv.scale(s, s); cv.translate(-CX, -Y_ALTO)


def na_tela(cam, x, y):
    ax, sy, s = cam
    return ax + (x - CX) * s, sy + (y - Y_ALTO) * s


# ------------------------------------------------------------------ peças do mundo
def peca(cv, pth):
    cv.drawPath(pth, paint("#000000", 70, blur=14))
    cv.drawPath(pth, paint(OSSO_C, shader=sombra_osso()))
    cv.drawPath(pth, paint(OSSO_L, 150, "stroke", 2.5))


def anel(cv, y, alfa, metade):
    if alfa <= 0:
        return
    r = skia.Rect(CX - RX2, y - RY2, CX + RX2, y + RY2)
    if metade == "tras":
        cv.drawArc(r, 180, 180, False, paint(ACO_ESC, int(255 * alfa), "stroke", 14))
        return
    cv.drawArc(r, 0, 180, False, paint("#000000", int(80 * alfa), "stroke", 17, blur=6))
    cv.drawArc(r, 0, 180, False, paint(ACO, int(255 * alfa), "stroke", 14))
    cv.drawArc(skia.Rect(r.left() + 6, r.top() + 4, r.right() - 6, r.bottom() - 2), 20, 140, False,
               paint(ACO_HL, int(170 * alfa), "stroke", 3))
    for ang in (25, 90, 155):
        a = math.radians(ang)
        cv.drawCircle(CX + RX2 * math.cos(a), y + RY2 * math.sin(a), 3.2, paint(ACO_ESC, int(255 * alfa)))


def fios(cv, y, alfa):
    for s in (-1, 1):
        x0, y0, x1, y1 = CX - RX2 + 16, y - 13 * s, CX + RX2 - 16, y + 13 * s
        cv.drawLine(x0, y0, x1, y1, paint("#DDE6EE", int(230 * alfa), "stroke", 3.2))
        xo = CX - 66 * s                                            # oliva em cima do fio
        cv.drawCircle(xo, lerp(y0, y1, (xo - x0) / (x1 - x0)), 6, paint(OURO, int(255 * alfa)))


def tecido(cv, t, T, y0, y1, a):
    """Seis linhas finas cor de areia de ponta a ponta do vão: frouxas no "tecido", retesadas e
    vibrando como corda no "estica". Faixa genérica: sem nervo, vaso, músculo, vermelho ou ruptura."""
    if a <= 0 or y1 - y0 < 8:
        return
    tenso = e_inout(prog(t, T["estica"] + 0.0, T["estica"] + 0.28))   # junto com o tranco da parte de baixo
    n = 6
    for i in range(n):
        x = CX - 44 + i * 88 / (n - 1)
        rev = e_out(prog(t, T["tecido"] - 0.05 + i * 0.045, T["tecido"] + 0.3 + i * 0.045))
        if rev <= 0:
            continue
        amp = lerp(9.0, 0.0, tenso)
        vib = 4.0 * tenso * math.sin(t * 57 + i * 1.9)
        larg = lerp(4.6, 2.1, tenso)
        yf = lerp(y0, y1, rev)
        p = skia.Path(); p.moveTo(x, y0); m = 24
        for k in range(1, m + 1):
            f = k / m; yy = lerp(y0, yf, f)
            p.lineTo(x + amp * math.sin(f * math.pi * 2 + i * 1.3) + vib * math.sin(f * math.pi), yy)
        cv.drawPath(p, paint(AREIA, int(70 * a), "stroke", larg + 5, blur=4))
        cv.drawPath(p, paint(AREIA, int(255 * a), "stroke", larg))


def faiscas(cv, t, T, y0, y1):
    """Duas ou três faíscas douradas que aparecem no vão e se apagam: nenhum dourado se firma."""
    if y1 - y0 < 20:
        return
    for t0, fx, fy in ((T["novo1"] + 0.02, -22, 0.3), (T["novo1"] + 0.36, 26, 0.62), (T["forma"] + 0.04, -4, 0.82)):
        k = t - t0
        if not 0 <= k < 0.55:
            continue
        a = clamp(k / 0.07) * (1 - prog(k, 0.12, 0.55))
        x, y = CX + fx, lerp(y0, y1, fy)
        cv.drawCircle(x, y, 30, paint(NOVO_G, int(120 * a), blur=14))
        cv.drawRect(skia.Rect(x - 20, y - 9, x + 20, y + 9), paint(NOVO, int(110 * a * (1 - prog(k, 0.05, 0.4))), blur=5))
        s = 10 * (0.6 + 0.4 * a)
        p = skia.Path(); p.moveTo(x, y - s * 2); p.lineTo(x + s * 0.45, y - s * 0.45); p.lineTo(x + s * 2, y)
        p.lineTo(x + s * 0.45, y + s * 0.45); p.lineTo(x, y + s * 2); p.lineTo(x - s * 0.45, y + s * 0.45)
        p.lineTo(x - s * 2, y); p.lineTo(x - s * 0.45, y - s * 0.45); p.close()
        cv.drawPath(p, paint("#FFF1C2", int(255 * a)))


def fio_dourado(cv, y0, y1, larg, a, brilho, solda, t):
    """O fio de osso novo do ritmo certo; no "endurece" perde o brilho e amadurece como no piloto
    (desenha_regenerado com `duro` = solda: dourado → marfim, estrias LONGITUDINAIS que somem),
    alargando até soldar as pontas (osso maduro, cedo demais). Nada de traço diagonal (lê-se fissura)
    nem clarão frio (lê-se vidro)."""
    if a <= 0 or y1 - y0 < 1:
        return
    w = lerp(larg, 2 * H2, e_inout(solda)) / 2
    if brilho > 0.01:
        cv.drawRect(skia.Rect(CX - w - 22, y0 - 12, CX + w + 22, y1 + 12), paint(NOVO_G, int(150 * brilho * a), blur=16))
    r = skia.Rect(CX - w, y0, CX + w, y1)
    cv.saveLayer(None, paint("#FFFFFF", int(255 * a))) if a < 1 else cv.save()
    cv.drawRect(r, paint(AMBAR, 255))
    if solda <= 0:
        cv.drawRect(r, paint(NOVO, 255))
    else:                                                           # o regenerado do piloto, recortado no fio
        cv.save(); cv.clipRect(r, skia.ClipOp.kIntersect, True)
        desenha_regenerado(cv, y0, y1, 1.0, 0.0, solda, t)
        cv.restore()
    if solda < 0.35:                                                # estrias do fio (somem na passagem)
        for k in range(3):
            x = CX + (k - 1) * w * 0.55
            cv.drawLine(x, y0 + 2, x + math.sin(k + t * 2) * 1.2, y1 - 2,
                        paint("#B5701A", int(190 * (1 - solda / 0.35)), "stroke", 2.2))
    cv.restore()
    if solda > 0.4:                                                 # as duas costuras da solda, discretas
        b = prog(solda, 0.4, 1.0)
        cv.drawLine(CX - w, y0 - 5, CX - w, y1 + 5, paint(OSSO_L, int(90 * a * b), "stroke", 2.5))
        cv.drawLine(CX + w, y0 - 5, CX + w, y1 + 5, paint(OSSO_L, int(90 * a * b), "stroke", 2.5))


def cadeado(cv, x, y, esc, alfa, fecho):
    """Cadeado simples; `fecho` 0 = argola aberta (alta), 1 = fechada (estalo)."""
    if esc <= 0 or alfa <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    dy = lerp(-22, 0, fecho)
    cv.drawArc(skia.Rect(-24, -50 + dy, 24, -2 + dy), 180, 180, False, paint("#000000", int(80 * alfa), "stroke", 13, blur=4))
    cv.drawArc(skia.Rect(-24, -50 + dy, 24, -2 + dy), 180, 180, False, paint("#C9D3DD", int(255 * alfa), "stroke", 10))
    cv.drawLine(-24, -26 + dy, -24, -6 + dy, paint("#C9D3DD", int(255 * alfa), "stroke", 10))
    cv.drawLine(24, -26 + dy, 24, -6 + dy, paint("#C9D3DD", int(255 * alfa), "stroke", 10))
    rr = skia.RRect.MakeRectXY(skia.Rect(-38, -14, 38, 44), 10, 10)
    cv.drawRRect(rr, paint("#000000", int(90 * alfa), blur=8))
    sh = skia.GradientShader.MakeLinear([skia.Point(-38, 0), skia.Point(38, 0)],
                                        [skia.ColorSetARGB(255, 0x8B, 0x95, 0xA0), skia.ColorSetARGB(255, 0xC9, 0xD3, 0xDD),
                                         skia.ColorSetARGB(255, 0x7A, 0x84, 0x90)], [0.0, 0.45, 1.0])
    cv.drawRRect(rr, paint("#8B95A0", int(255 * alfa), shader=sh))
    cv.drawRRect(rr, paint("#4A525C", int(255 * alfa), "stroke", 3))
    cv.drawCircle(0, 10, 7, paint("#2B3138", int(255 * alfa)))
    cv.drawRect(skia.Rect(-3, 12, 3, 28), paint("#2B3138", int(255 * alfa)))
    cv.restore()


def tracejado(cv, x0, y0, x1, y1, cor, alfa, larg=4, traco=20, vazio=13, fase=0.0):
    if alfa <= 0:
        return
    p = paint(cor, int(alfa), "stroke", larg)
    p.setPathEffect(skia.DashPathEffect.Make([traco, vazio], fase))
    cv.drawLine(x0, y0, x1, y1, p)


def estado(t, T, A):
    g = vao(t, T, A)
    trem = tremor_trava(t, A)
    r1a, r1b = A["rew1"]; r2a, r2b = A["rew2"]
    e = {"g": g, "trem": trem}
    # fase rápida: tecido esticado (some na volta do filme)
    e["a_tec"] = prog(t, T["tecido"] - 0.1, T["tecido"] + 0.2) * (1 - prog(t, r1a, r1a + 0.45))
    # ritmo certo (1ª vez) + devagar demais: o fio dourado e a solda
    a_fio = clamp(g / 10) if r1b <= t < r2b else 0.0
    e["a_fio"] = a_fio * (1 - prog(t, r2b - 0.2, r2b)) if t < r2a else (1 - prog(t, r2b - 0.2, r2b))
    e["larg_fio"] = lerp(18, 40, prog(t, A["p2"][0], T["demais"]))
    lamp = 0.0
    for s in A["p2"]:                                               # lampejo a cada passo
        k = t - s
        if 0 <= k < 0.4:
            lamp = max(lamp, 1 - k / 0.4)
    perde = prog(t, T["endurece"] - 0.1, T["endurece"] + 0.4)
    e["brilho_fio"] = (0.45 + 0.5 * lamp) * (1 - perde)
    e["solda"] = e_inout(prog(t, T["endurece"] + 0.1, T["endurece"] + 0.95))
    # cadeado: fecha no "trava", abre e some no "certo"
    e["cad_esc"] = e_back(prog(t, T["trava"] - 0.2, T["trava"] + 0.05)) * (1 - prog(t, T["certo"] + 0.15, T["certo"] + 0.4))
    e["cad_fecho"] = e_out(prog(t, T["trava"] + 0.02, T["trava"] + 0.12)) * (1 - e_out(prog(t, T["certo"] - 0.1, T["certo"] + 0.1)))
    e["cad_a"] = prog(t, T["trava"] - 0.2, T["trava"] - 0.05) * (1 - prog(t, T["certo"] + 0.15, T["certo"] + 0.4))
    # alvo tracejado: aparece depois do cadeado, fica no ritmo certo e some quando o osso chega
    e["a_alvo"] = prog(t, T["trava"] + 0.55, T["trava"] + 0.9) * (1 - prog(t, T["ponte"] + 0.35, T["ponte"] + 0.9))
    e["flash_alvo"] = max(0.0, 1 - abs(t - (T["ponte"] + 0.05)) / 0.35)
    # ritmo certo (ponte): osso novo dourado enchendo o vão
    e["p4"] = t >= r2b
    e["dens"] = clamp(g / 26)
    br = prog(t, T["novo2"] - 0.1, T["novo2"] + 0.3) * (1 - 0.45 * prog(t, T["novo2"] + 1.3, T["novo2"] + 2.4))
    br = max(br, max(0.0, 1 - abs(t - (T["ponte"] + 0.1)) / 0.6))
    e["brilho4"] = max(br, 0.35 * e["dens"])
    e["varre"] = prog(t, T["ponte"] - 0.05, T["ponte"] + 0.55)
    return e


def mundo(cv, t, T, A, e):
    g = e["g"]
    yi = Y_CORTE + FENDA + g + e["trem"]                          # topo da parte de baixo
    yb = Y_BASE + FENDA + g + e["trem"]
    y_an = (Y_AN_SUP, yi + DY_AN_INF)
    for y in y_an:
        anel(cv, y, 1.0, "tras")
    tecido(cv, t, T, Y_CORTE - 2, yi + 2, e["a_tec"])

    peca(cv, path_osso_sup(Y_TOPO, Y_CORTE))
    peca(cv, path_osso_inf(yi, yb))
    k = t - A["p1"][0]                                              # rastros de velocidade na descida
    if 0 <= k < 0.85:
        ar = clamp(k / 0.08) * (1 - prog(k, 0.45, 0.85))
        for sx, dx, L in ((-1, 26, 110), (-1, 48, 70), (1, 26, 110), (1, 48, 70)):
            x = CX + sx * (H2 + dx)
            cv.drawLine(x, yi - L - 10, x, yi - 14, paint("#FFFFFF", int(150 * ar), "stroke", 4))

    y0, y1 = Y_CORTE + FENDA * 0.5, yi - FENDA * 0.5
    if e["a_fio"] > 0:
        # a solda cobre também o corte fino: as duas pontas viram uma peça só
        ya, yz = lerp(y0, Y_CORTE - 3, e["solda"]), lerp(y1, yi + 3, e["solda"])
        fio_dourado(cv, ya, yz, e["larg_fio"], e["a_fio"], e["brilho_fio"], e["solda"], t)
    if e["p4"] and g > 1:
        cv.drawRect(skia.Rect(CX - H2 + 2, y0, CX + H2 - 2, y1), paint(AMBAR, int(255 * clamp(g / 8))))
        desenha_regenerado(cv, y0, y1, e["dens"], e["brilho4"], 0.0, t)
        v = e["varre"]
        if 0 < v < 1:                                               # a ponte se fecha: um brilho corre de ponta a ponta
            yy = lerp(y0, y1, e_inout(v))
            cv.drawRect(skia.Rect(CX - H2 + 2, yy - 16, CX + H2 - 2, yy + 16),
                        paint("#FFF4CF", int(200 * math.sin(math.pi * v)), blur=10))
    faiscas(cv, t, T, Y_CORTE, yi)

    # fixador (frente): fios, hastes com rosca, porcas girando a cada passo, anéis
    for y in y_an:
        fios(cv, y, 1.0)
    gira = g * 4 + 6 * math.sin(t * 60) * (abs(e["trem"]) > 0.2)
    for sx in (-1, 1):
        x = CX + sx * X_HASTE
        haste(cv, x, y_an[0], y_an[1], 1.0, rosca=True, fase=-g * 0.5)
        porca(cv, x, y_an[0] + 24, gira + sx * 15, 1.0)
        porca(cv, x, y_an[1] - 24, -gira, 1.0)
    for y in y_an:
        anel(cv, y, 1.0, "frente")

    # até onde o osso deveria ir (sem texto)
    a = e["a_alvo"]
    if a > 0:
        y_alvo = Y_BASE + FENDA + 36 + G4
        fl = e["flash_alvo"]
        cor = lerpc("#DDE6EE", OURO, fl)
        tracejado(cv, CX - 150, y_alvo, CX + 150, y_alvo, cor, 235 * a, larg=5, fase=-t * 12)
        for sx in (-1, 1):
            cv.drawLine(CX + sx * 150, y_alvo - 14, CX + sx * 150, y_alvo + 14, paint(cor, int(235 * a), "stroke", 5))
        if fl > 0:
            cv.drawLine(CX - 150, y_alvo, CX + 150, y_alvo, paint(OURO, int(160 * fl * a), "stroke", 16, blur=10))

    # cadeado sobre o vão, de lado: a solda continua à vista
    if e["cad_a"] > 0:
        cadeado(cv, CX - 80, (Y_CORTE + yi) / 2 + 8, 1.35 * e["cad_esc"], e["cad_a"], e["cad_fecho"])
    brilhos(cv, CX, (Y_CORTE + yi) / 2, t, T["ponte"] + 0.05, n=16, raio=200)


# ------------------------------------------------------------------ mostrador (tela)
def mostrador(cv, t, T, a):
    if a <= 0:
        return
    cx, cy, r = DX, DY, DR
    R = r + 36
    placa = skia.Path()
    placa.moveTo(cx - R, cy + 26)
    placa.arcTo(skia.Rect(cx - R, cy - R, cx + R, cy + R), 180, 180, False)
    placa.lineTo(cx + R, cy + 26); placa.close()
    cv.drawPath(placa, paint("#000000", int(90 * a), blur=12))
    cv.drawPath(placa, paint(CAIXA, int(225 * a)))
    cv.drawPath(placa, paint(ACO_ESC, int(255 * a), "stroke", 3))
    rect = skia.Rect(cx - r, cy - r, cx + r, cy + r)
    ang = angulo(t, T)
    vivo = prog(t, T["rapido"], T["rapido"] + 0.12)              # na capa nenhuma zona acende
    # no rebobinar o mostrador apaga (o filme volta; não é "voltando em alta velocidade")
    vivo *= 1 - prog(t, T["isso"] + 0.1, T["isso"] + 0.3) * (1 - prog(t, T["milimetro"] - 0.05, T["milimetro"] + 0.1))
    pulso = 0.0
    if T["certo"] <= t < T["equipe"] + 1.0:
        pulso = 0.5 + 0.5 * math.sin((t - T["certo"]) * 7.0)
    zonas = ((181.5, LENTO, A_LENTO), (241.5, OURO, A_CERTO), (301.5, VERMELHO, A_RAPIDO))
    for ini, cor, centro in zonas:
        dentro = clamp(1 - abs(ang - centro) / 34)
        glow = vivo * dentro * (1.0 if cor != OURO else 0.75 + 0.25 * pulso)
        if glow > 0.01:
            p = paint(cor, int(170 * a * glow), "stroke", 48, blur=14); p.setStrokeCap(skia.Paint.kButt_Cap)
            cv.drawArc(rect, ini, 57, False, p)
        p = paint(cor, int(a * (215 + 40 * glow)), "stroke", 30); p.setStrokeCap(skia.Paint.kButt_Cap)
        cv.drawArc(rect, ini, 57, False, p)
    for k in range(13):                                             # escala sem número
        ra = math.radians(180 + 15 * k); grande = k % 4 == 0
        r0, r1 = r + 21, r + (32 if grande else 27)
        cv.drawLine(cx + r0 * math.cos(ra), cy + r0 * math.sin(ra), cx + r1 * math.cos(ra), cy + r1 * math.sin(ra),
                    paint("#FFFFFF", int(a * (150 if grande else 90)), "stroke", 3 if grande else 2))
    cv.drawArc(skia.Rect(cx - r + 22, cy - r + 22, cx + r - 22, cy + r - 22), 180, 180, False,
               paint("#FFFFFF", int(40 * a), "stroke", 2))
    rad = math.radians(ang)
    xp, yp = cx + (r - 6) * math.cos(rad), cy + (r - 6) * math.sin(rad)
    xr, yr = cx - 20 * math.cos(rad), cy - 20 * math.sin(rad)
    cv.drawLine(xr, yr, xp, yp, paint("#000000", int(110 * a), "stroke", 13, blur=4))
    cv.drawLine(xr, yr, xp, yp, paint("#FFFFFF", int(255 * a), "stroke", 8))
    cv.drawCircle(cx, cy, 17, paint(ACO_HL, int(255 * a)))
    cv.drawCircle(cx, cy, 17, paint(ACO_ESC, int(255 * a), "stroke", 3))
    cv.drawCircle(cx, cy, 6, paint(ACO_ESC, int(255 * a)))


def caixa_dial(cv, linhas, cor, a):
    """Rótulo da zona, logo abaixo do eixo do ponteiro. linhas = [(texto, fonte, tam, cor, alfa)]."""
    if a <= 0:
        return
    # linha que entra depois (PEQUENOS AJUSTES): a caixa cresce junto, sem salto
    abre = [1.0 if al >= 1 else e_out(clamp(al * 2.5)) for *_, al in linhas]
    larg = max(larg_texto(s, f, tam) * k for (s, f, tam, _, _), k in zip(linhas, abre))
    alt = sum(tam * 1.18 * k for (_, _, tam, _, _), k in zip(linhas, abre)) + 22
    y0 = DY + 44
    esc = lerp(0.82, 1.0, e_back(clamp(a)))
    cv.save(); cv.translate(DX, y0); cv.scale(esc, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-larg / 2 - 18, 0, larg / 2 + 18, alt), 14, 14)
    cv.drawRRect(rr, paint(CAIXA, int(225 * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 3))
    cv.drawLine(0, -10, 0, 0, paint(cor, int(220 * a), "stroke", 3))
    yy = 11
    for (s, f, tam, c, al), k in zip(linhas, abre):
        yy += tam * 1.18 * k
        if al > 0:
            texto(cv, s, 0, yy - tam * 0.26, f, tam, c, int(255 * a * (1.0 if al >= 1 else clamp((al - 0.3) / 0.7))))
    cv.restore()


def etiqueta(cv, linhas, x, y, ancora, cor, a):
    """Caixa de rótulo (1 ou 2 linhas) na coluna da direita, com linha fina até `ancora`.
    linhas = [(texto, fonte, tamanho, cor, alfa_da_linha)]."""
    if a <= 0:
        return
    x += 26 * (1 - e_out(a))
    # a 2ª linha entra com a palavra: a caixa cresce junto (nada de espaço vazio esperando)
    abre = [1.0] + [e_out(clamp(al * 2.5)) for *_, al in linhas[1:]]
    larg = max(larg_texto(s, f, tam) * k for (s, f, tam, _, _), k in zip(linhas, abre))
    alt = sum(tam * 1.2 * k for (_, _, tam, _, _), k in zip(linhas, abre)) + 20
    xa, ya = ancora
    cv.drawLine(xa, ya, x, y + alt / 2, paint(cor, int(200 * a), "stroke", 2.5))
    cv.drawCircle(xa, ya, 6, paint(cor, int(255 * a)))
    rr = skia.RRect.MakeRectXY(skia.Rect(x, y, x + larg + 32, y + alt), 14, 14)
    cv.drawRRect(rr, paint(CAIXA, int(215 * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 2.5))
    yy = y + 10
    for (s, f, tam, c, al), k in zip(linhas, abre):
        yy += tam * 1.2 * k
        if al > 0:
            texto(cv, s, x + 16, yy - tam * 0.28, f, tam, c, int(255 * a * clamp((al - 0.3) / 0.7)), centro=False)


def carimbo_cor(cv, s, x, y, rot, t0, t, cor=VERMELHO, dur=1.7, tam=54):
    """O carimbo do piloto com tamanho ajustável (frase longa cabe na largura do celular)."""
    k = t - t0
    if k < 0 or k > dur:
        return
    esc = lerp(1.9, 1.0, e_out(clamp(k / 0.16))); a = clamp(k / 0.08) * (1 - prog(k, dur - 0.35, dur))
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(esc, esc)
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 24, -tam, lw / 2 + 24, tam * 0.36), 12, 12)
    cv.drawRRect(rr, paint(CAIXA, int(160 * a))); cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 7))
    cv.drawString(s, -lw / 2, 0, f, paint(cor, int(255 * a)))
    cv.restore()


def carimbo_duplo(cv, l1, l2, x, y, rot, t0, t, dur=1.9):
    """NÃO EXISTE / PILOTO AUTOMÁTICO, por cima do mostrador."""
    k = t - t0
    if k < 0 or k > dur:
        return
    esc = lerp(1.9, 1.0, e_out(clamp(k / 0.16))); a = clamp(k / 0.08) * (1 - prog(k, dur - 0.35, dur))
    t1, t2 = 46, 56
    w1, w2 = larg_texto(l1, F_BLACK, t1), larg_texto(l2, F_BLACK, t2)
    lw = max(w1, w2)
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(esc, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 26, -t1 - 22, lw / 2 + 26, t2 + 26), 14, 14)
    cv.drawRRect(rr, paint(CAIXA, int(200 * a))); cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 7))
    cv.drawString(l1, -w1 / 2, 0, skia.Font(F_BLACK, t1), paint("#FFFFFF", int(255 * a)))
    cv.drawString(l2, -w2 / 2, t2 + 4, skia.Font(F_BLACK, t2), paint(OURO, int(255 * a)))
    cv.restore()


def icone_volta(cv, x, y, a):
    """Rebobinar (o filme volta ao começo): dois triângulos, sem texto."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(lerp(0.7, 1.0, e_back(clamp(a))), lerp(0.7, 1.0, e_back(clamp(a))))
    cv.drawCircle(0, 0, 40, paint(CAIXA, int(225 * a)))
    cv.drawCircle(0, 0, 40, paint(ACO_HL, int(230 * a), "stroke", 3))
    for dx in (-15, 9):
        p = skia.Path(); p.moveTo(dx + 14, -15); p.lineTo(dx + 14, 15); p.lineTo(dx - 9, 0); p.close()
        cv.drawPath(p, paint("#FFFFFF", int(255 * a)))
    cv.restore()


def lupa(cv, t, T, A, e, cam):
    """Lupa SÓ de contorno: passa devagar sobre a ponte e aumenta o mesmo desenho (nada de exame)."""
    t0 = T["acompanhado"] - 0.1
    if t < t0:
        return None
    # sai encolhendo e apagando NO LUGAR (não atravessa a caixa do rótulo) antes do carimbo do piloto
    sai = e_inout(prog(t, T["piloto"] - 0.65, T["piloto"] - 0.3))
    a = 1 - sai
    if a <= 0:
        return None
    g = e["g"]
    gx, gy = na_tela(cam, CX, Y_CORTE + (FENDA + g) / 2)
    k1 = e_inout(prog(t, t0, t0 + LUPA_CHEGA))
    k2 = e_inout(prog(t, t0 + LUPA_CHEGA, T["piloto"] - 0.65))
    x = lerp(1190, gx + 8, k1) + 4 * math.sin(t * 1.7)
    y = lerp(1080, gy - 34, k1) + 68 * k2 + 3 * math.cos(t * 1.3)
    s = 1 - 0.35 * sai
    r, m = 118 * s, 1.5
    cv.saveLayer(None, paint("#FFFFFF", int(255 * a))) if a < 1 else cv.save()
    cv.save()
    clip = skia.Path(); clip.addCircle(x, y, r)
    cv.clipPath(clip, skia.ClipOp.kIntersect, True)
    fundo(cv, t)
    cv.drawRect(skia.Rect(0, 0, W, H), paint("#FFFFFF", 24))       # lente clara: só aumenta o desenho
    cv.translate(x, y); cv.scale(m, m); cv.translate(-x, -y)
    aplica(cv, cam)
    mundo(cv, t, T, A, e)
    cv.restore()
    hx, hy = x + r * 0.71, y + r * 0.71
    L = 80 * s
    cv.drawLine(hx + 4 * s, hy + 4 * s, hx + L + 2 * s, hy + L + 2 * s, paint("#000000", 80, "stroke", 30 * s, blur=6))
    cv.drawLine(hx + 6 * s, hy + 6 * s, hx + L, hy + L, paint("#8A6512", 255, "stroke", 26 * s))
    cv.drawLine(hx + 6 * s, hy + 6 * s, hx + L, hy + L, paint(OURO, 255, "stroke", 16 * s))
    cv.drawCircle(x, y, r, paint("#000000", 80, "stroke", 20 * s, blur=6))
    cv.drawCircle(x, y, r, paint(OURO, 255, "stroke", 13 * s))
    cv.drawCircle(x, y, r - 8 * s, paint("#FFF1C2", 120, "stroke", 2.5))
    cv.drawArc(skia.Rect(x - r * 0.72, y - r * 0.72, x + r * 0.72, y + r * 0.72), 200, 55, False,
               paint("#FFFFFF", 150, "stroke", 7 * s))
    cv.restore()
    return hx + L, hy + L


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    A = agenda(T)
    e = estado(t, T, A)
    cam = camera(t, T)
    g = e["g"]

    # ================= mundo (câmera)
    cv.save(); aplica(cv, cam); mundo(cv, t, T, A, e); cv.restore()

    # ================= tela
    a_dial = 1 - prog(t, T["piloto"] + 1.0, T["piloto"] + 1.6)
    cv.saveLayer(None, paint("#FFFFFF", int(255 * a_dial))) if a_dial < 1 else cv.save()
    mostrador(cv, t, T, 1.0)
    r1a, r1b = A["rew1"]
    a = prog(t, T["rapido"] + 0.08, T["rapido"] + 0.28) * (1 - prog(t, r1a - 0.1, r1a + 0.15))
    caixa_dial(cv, [("RÁPIDO DEMAIS", F_BLACK, 40, VERMELHO, 1.0)], VERMELHO, a)
    a = prog(t, T["milimetro"] + 0.05, T["milimetro"] + 0.25) * (1 - prog(t, T["demais"] - 0.15, T["demais"] + 0.05))
    caixa_dial(cv, [("cerca de", F_SEMI, 30, AZUL, 1.0), ("1 MM POR DIA", F_BLACK, 48, OURO, 1.0),
                    ("PEQUENOS AJUSTES", F_BLACK, 30, "#FFFFFF", prog(t, T["pequenos"], T["pequenos"] + 0.2))], OURO, a)
    # DEVAGAR DEMAIS sai quando o cadeado entra (o ponteiro no cinza continua dizendo "devagar")
    a = prog(t, T["demais"] + 0.08, T["demais"] + 0.28) * (1 - prog(t, T["trava"] - 0.25, T["trava"]))
    caixa_dial(cv, [("DEVAGAR DEMAIS", F_BLACK, 40, LENTO_TXT, 1.0)], LENTO, a)
    a = prog(t, T["certo"] + 0.08, T["certo"] + 0.28) * (1 - prog(t, T["equipe"] - 0.15, T["equipe"] + 0.05))
    caixa_dial(cv, [("RITMO CERTO", F_BLACK, 40, OURO, 1.0)], OURO, a)
    # PELA EQUIPE sai antes do carimbo do piloto: ele cai num mostrador limpo
    a = prog(t, T["equipe"] + 0.05, T["equipe"] + 0.25) * (1 - prog(t, T["piloto"] - 0.4, T["piloto"] - 0.15))
    caixa_dial(cv, [("PELA EQUIPE", F_BLACK, 40, "#FFFFFF", 1.0)], OURO, a)
    cv.restore()

    # rótulos do vão (coluna da direita)
    yi = Y_CORTE + FENDA + g
    anc = na_tela(cam, CX + H2 - 6, (Y_CORTE + yi) / 2)
    sai1 = 1 - prog(t, r1a - 0.2, r1a + 0.1)
    etiqueta(cv, [("TECIDO", F_BLACK, 40, AREIA, 1.0)], X_COL, 752, anc, AREIA,
             prog(t, T["tecido"] + 0.08, T["tecido"] + 0.32) * sai1)
    etiqueta(cv, [("SÓ ESTICA", F_BLACK, 40, "#FFFFFF", 1.0)], X_COL, 846, anc, AREIA,
             prog(t, T["estica"] + 0.08, T["estica"] + 0.32) * sai1)
    r2a, r2b = A["rew2"]
    etiqueta(cv, [("ENDURECE", F_BLACK, 40, OSSO_C, 1.0),
                  ("ANTES DA HORA", F_BLACK, 34, "#FFFFFF", prog(t, T["antes"], T["antes"] + 0.2))],
             X_COL, 752, anc, OSSO_C,
             prog(t, T["endurece"] + 0.12, T["endurece"] + 0.36) * (1 - prog(t, T["certo"] - 0.2, T["certo"] + 0.1)))
    sai4 = 1 - prog(t, T["acompanhado"] - 0.35, T["acompanhado"] - 0.05)
    etiqueta(cv, [("OSSO NOVO", F_BLACK, 40, OURO, 1.0)], X_COL, 752, anc, OURO,
             prog(t, T["novo2"] - 0.05, T["novo2"] + 0.2) * sai4)
    etiqueta(cv, [("PONTE", F_BLACK, 40, "#FFFFFF", 1.0)], X_COL, 846, anc, OURO,
             prog(t, T["ponte"] + 0.02, T["ponte"] + 0.25) * sai4)

    # o filme volta ao começo (duas vezes) — numa área livre, abaixo dos rótulos que ainda estão saindo
    for ra, rb in (A["rew1"], A["rew2"]):
        a = prog(t, ra - 0.1, ra + 0.1) * (1 - prog(t, rb, rb + 0.25))
        icone_volta(cv, X_COL + 80, 1010, a)

    ponta = lupa(cv, t, T, A, e, cam)
    if ponta:
        # só depois que a lupa assenta (o cabo não passa por cima); sai junto com ela, no lugar
        a = (prog(t, T["acompanhado"] + LUPA_CHEGA - 0.07, T["acompanhado"] + LUPA_CHEGA + 0.13)
             * (1 - prog(t, T["piloto"] - 0.65, T["piloto"] - 0.35)))
        etiqueta(cv, [("ACOMPANHADO", F_BLACK, 38, OURO, 1.0),
                      ("DE PERTO", F_BLACK, 38, "#FFFFFF", prog(t, T["perto"], T["perto"] + 0.2))],
                 X_COL, 930, ponta, OURO, a)

    # carimbos: os veredictos na faixa de cima (o mecanismo fica à vista). Vermelho = errado;
    # DE PROPÓSITO é o ritmo certo: dourado, e sai antes de "E devagar demais".
    carimbo_cor(cv, "O OSSO NOVO NÃO SE FORMA", CX, 318, -4, T["forma"] - 0.02, t, VERMELHO, dur=1.75, tam=50)
    carimbo(cv, "DE PROPÓSITO", CX, 330, 5, T["proposito"] - 0.02, t, dur=T["devagar2"] - T["proposito"] - 0.05)
    carimbo_cor(cv, "TRAVA A CORREÇÃO", CX, 318, -5, T["trava"] + 0.02, t, VERMELHO, dur=1.6, tam=54)
    carimbo_duplo(cv, "NÃO EXISTE", "PILOTO AUTOMÁTICO", 660, 560, -6, T["piloto"] - 0.02, t, dur=1.3)

    capa(cv, t, T["rapido"] + 0.1, ep["gancho"][0], ep["gancho"][1])
    selo_como_funciona(cv, prog(t, T["rapido"] + 0.5, T["rapido"] + 0.9) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface(cv, t, T, blocos, DESTAQUE)


# ------------------------------------------------------------------ som e prévias
def sons(T):
    A = agenda(T)
    ev = [(T["rapido"] - 0.02, "whoosh", 0.7), (A["p1"][-1] + 0.06, "thump", 0.75)]
    ev += [(s + 0.01, "click", 1.0) for s in A["p1"]]                          # cliques emendados
    ev += [(T["novo1"] + 0.02, "pop", 0.45), (T["novo1"] + 0.36, "pop", 0.4), (T["forma"] + 0.04, "pop", 0.35),
           (T["forma"] - 0.02, "thump", 0.85), (T["tecido"], "whoosh", 0.25),
           (A["p1b"][0] + 0.01, "click", 1.0), (A["p1b"][0] + 0.09, "tick", 0.55),     # o tranco que retesa
           (A["rew1"][0] - 0.05, "whoosh", 0.6), (T["milimetro"], "ping", 0.5),
           (T["proposito"] - 0.02, "thump", 0.9), (T["demais"], "whoosh", 0.35),
           (T["endurece"] + 0.1, "crackle", 0.8), (T["trava"] + 0.04, "ping", 0.9), (T["trava"] + 0.06, "thump", 0.8),
           (A["tenta"], "tick", 0.7), (A["rew2"][0] - 0.05, "whoosh", 0.6), (T["certo"] + 0.1, "ping", 0.45),
           (T["novo2"] - 0.05, "shimmer", 0.85), (T["ponte"] + 0.05, "ding", 0.6), (T["ponte"], "shimmer", 0.45),
           (T["acompanhado"] - 0.05, "whoosh", 0.35), (T["piloto"] - 0.02, "thump", 0.9),
           (T["manda"] + 0.05, "whoosh", 0.5)]
    ev += [(s + 0.01, "click", 0.9) for s in A["p2"]]                          # um clique por passo
    ev += [(s + 0.01, "click", 0.95) for s in A["p3"]]                         # bem espaçados
    ev += [(s + 0.01, "click", 0.85) for s in A["p4"]]
    ev += [(T["equipe"] + d, "click", 0.45) for d in (0.05, 0.42, 0.8)]       # as pequenas correções
    return ev


def tempos_previa(T):
    return [0.4, T["rapido"] + 0.75, T["forma"] + 0.45, T["estica"] + 0.45, T["pequenos"] + 0.8,
            T["proposito"] + 0.4, T["endurece"] + 1.0, T["trava"] + 0.75, T["ponte"] + 0.45,
            T["acompanhado"] + 1.1, T["piloto"] + 0.5, T["manda"] + 1.6]


render = fazer_render(quadro, ANCORAS, sons, tempos_previa)
