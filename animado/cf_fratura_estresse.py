# -*- coding: utf-8 -*-
"""COMO FUNCIONA — fratura por estresse ("OSSO QUEBRA / SEM QUEDA?").

Mesmo estilo e mesmas peças das cenas aprovadas (fundo azul-petróleo, osso marfim liso e opaco,
carimbo ouro, rótulos, cartão de atenção, legenda karaokê, CTA com aviãozinho). Storyboard e
correções do verificador (lote5_cf/cf_fratura_estresse_storyboard.json) respeitados aqui:
  * Osso longo GENÉRICO (a fonte não nomeia osso nem local: nenhuma ponta imita um osso
    específico), marfim, liso e opaco, de pé no centro. Nenhum exame simulado (nada de fundo preto, negativo,
    filme ou osso translúcido).
  * A trinca é um traço fino ESCURO (TRINCA #2B2118, o tom do cf_discrepancia_causas e do
    cf_placa_crescimento), sem dourado e sem vermelho. Nasce em "trincar" (o espanto: é a 1ª
    coisa que se mexe na tela — traço grosso, lampejo também FORA do osso, estalo, ondas e
    aproximação de 18%) e, de "poucos" em diante, ganha um traço a cada risquinho do contador.
    Só ganha comprimento: não abre, não separa as partes e para no meio da diáfise.
  * "queda": pictograma de boneco caindo, riscado, e o carimbo ouro opaco SEM QUEDA (o osso não
    recebe impacto nenhum: o tremor é só do carimbo).
  * Contador TREINO com risquinhos de giz DESENHADOS (forma, não texto) e SEM número, em ritmo
    regular e rápido (treino intenso e repetitivo); para em "estresse" e fica parado.
  * "SEM UMA PANCADA ÚNICA" foi para um cartão de 2 linhas ("SEM UMA PANCADA" / "ÚNICA"): numa
    linha só não cabe na coluna ao lado do osso sem encostar nele.
  * Barra DOR (vermelho-suave, sem chama, sem sangue) que sobe com o tênis em contorno
    (ATIVIDADE) e desce com o ícone NEUTRO de pausa (REPOUSO) — nada de lua, cama ou noite —,
    repete o padrão uma vez, devagar, e volta a subir em "a cada treino" (tênis aceso, risquinho
    novo e pulso no mesmo ponto juntos: a tela nunca diz "treinou e ficou sem dor").
  * Alvo amarelo-suave pulsando sobre a trinca (MESMO PONTO) e de novo com mais um risquinho
    (A CADA TREINO). Cartão de atenção amarelo e sóbrio: MERECE AVALIAÇÃO / ORTOPEDIA PEDIÁTRICA,
    sem vermelho de urgência e sem cruz de pronto-socorro.
  * A barra DOR se dobra numa placa triangular de aviso (o "!" é traço + ponto DESENHADOS). O troféu
    desce, não encaixa na ponta da placa e desliza para fora — não é riscado nem quebrado.
  * Troca de cena: osso, alvo, contador, cartão e placa recuam e saem; a trinca NÃO cola. Entra a
    escada de carga em aço azul-claro (não dourada), degraus baixos que se desenham um a um; um
    deles se alarga no patamar DESCANSO (o mesmo ícone de pausa) e a escada continua subindo.
    PREVINE BOA PARTE é rótulo sóbrio: sem check, sem escudo, sem selo.
Cena PRESA ao roteiro pelas palavras-âncora (roteiro sem elas = KeyError, não vídeo torto).
Todo texto desenhado está em ep["tela"] (o render recusa o vídeo se não estiver).
"""
import math

import skia

from .cf_alongamento import (ACO, ACO_ESC, ACO_HL, F_BLACK, OSSO_B, OSSO_C, OSSO_L, OURO, W, C, clamp,
                             e_back, e_in_back, e_inout, e_out, fundo, larg_texto, lerp, lerpc, paint, prog,
                             rotulo, texto)
from .cf_comum import capa, fazer_render, interface, selo_como_funciona

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "trincar": ("trincar", 1, False), "queda": ("queda", 1, False), "treino": ("treino", 1, False),
    "repetitivo": ("repetitivo", 1, False), "poucos": ("poucos", 1, False), "pancada": ("pancada", 1, False),
    "unica": ("única", 1, False), "fratura": ("fratura", 1, False), "estresse": ("estresse", 1, False),
    "sinal": ("sinal", 1, False), "dor1": ("dor", 1, False), "atividade": ("atividade", 1, False),
    "repouso": ("repouso", 1, False), "dor2": ("dor", 2, False), "ponto": ("ponto", 1, False),
    "treino2": ("treino", 2, False), "merece": ("merece", 1, False), "avaliacao": ("avaliação", 1, False),
    "dor3": ("dor", 3, False), "aviso": ("aviso", 1, False), "trofeu": ("troféu", 1, False),
    "aumentar": ("aumentar", 1, False), "descanso": ("descanso", 1, False), "previne": ("previne", 1, False),
    "fraturas": ("fraturas", 1, False), "manda": ("manda", 1, False),
}
DESTAQUE = {"trincar", "queda", "treino", "repetitivo", "poucos", "pancada", "estresse", "atividade",
            "repouso", "ponto", "avaliação", "aviso", "troféu", "aumentar", "descanso", "previne"}

# ------------------------------------------------------------------ textos de tela (todos em ep["tela"])
SEM_QUEDA = "SEM QUEDA"
TREINO = "TREINO"
AOS_POUCOS = "AOS POUCOS"
PANCADA = ("SEM UMA PANCADA", "ÚNICA")
NOME = "FRATURA POR ESTRESSE"
DOR = "DOR"
ATIVIDADE = "ATIVIDADE"
REPOUSO = "REPOUSO"
MESMO_PONTO = "MESMO PONTO"
CADA_TREINO = "A CADA TREINO"
AVALIACAO = ("MERECE AVALIAÇÃO", "ORTOPEDIA PEDIÁTRICA")
AVISO = "DOR É AVISO"
TROFEU = "NÃO TROFÉU"
AUMENTAR = "AUMENTAR O TREINO AOS POUCOS"
DESCANSO = "DESCANSO"
PREVINE = "PREVINE BOA PARTE"

# ------------------------------------------------------------------ paleta própria
FUNDO_CARTAO = "#0B1824"
AZUL = "#9CC9FF"
TRINCA = "#2B2118"
DOR_C, DOR_CL, DOR_TXT = "#FF5A5F", "#FF8A8F", "#FFA3A6"   # vermelho-suave (sem chama, sem sangue)
AMARELO, AMARELO_ESC = "#FFD166", "#8A6A12"
GIZ = "#F2F6FA"


def _p(cor, a=255, estilo="fill", w=0, blur=0, junta=False, traco=None, canto=0):
    p = paint(cor, a, estilo, w, blur)
    if junta:
        p.setStrokeJoin(skia.Paint.kRound_Join)
    if traco:
        p.setPathEffect(skia.DashPathEffect.Make(list(traco), 0.0))
    elif canto:
        p.setPathEffect(skia.CornerPathEffect.Make(canto))
    return p


def _poli(pts, pr):
    """Polilinha desenhada até a fração `pr` (cópia do cf_placa_crescimento)."""
    n = len(pts) - 1; k = clamp(pr) * n; i = int(k)
    p = skia.Path(); p.moveTo(*pts[0])
    for j in range(1, min(i, n) + 1):
        p.lineTo(*pts[j])
    if i < n:
        f = k - i; (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        p.lineTo(lerp(x0, x1, f), lerp(y0, y1, f))
    return p


def _acaso(i, k):
    """Pseudoacaso determinístico em [0, 1) (o giz não treme de um quadro para o outro)."""
    v = math.sin(i * 12.9898 + k * 78.233) * 43758.5453
    return v - math.floor(v)


def chip(cv, s, x, y, cor, a, tam=36, cor_txt=None, esc=1.0):
    """Rótulo solto centrado em x; y = linha de base do texto (cópia do cf_discrepancia_causas)."""
    if a <= 0:
        return
    lw = larg_texto(s, F_BLACK, tam)
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 22, -tam * 1.05, lw / 2 + 22, tam * 0.36), 15, 15)
    cv.drawRRect(rr, paint("#000000", int(70 * a), blur=10))
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(228 * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 3))
    texto(cv, s, 0, 0, F_BLACK, tam, cor_txt or cor, int(255 * a))
    cv.restore()


def carimbo_opaco(cv, s, x, y, rot, t0, t, dur, tam=62, esc0=1.9):
    """Carimbo ouro torto com fundo opaco (cópia do cf_discrepancia_causas)."""
    k = t - t0
    if k < 0 or k > dur:
        return
    esc = lerp(esc0, 1.0, e_out(clamp(k / 0.16))); a = clamp(k / 0.08) * (1 - prog(k, dur - 0.35, dur))
    tre = 5 * math.sin(k * 70) * (1 - clamp(k / 0.35)) if k < 0.35 else 0.0     # tremor curto do carimbo
    cv.save(); cv.translate(x + tre, y); cv.rotate(rot); cv.scale(esc, esc)
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 24, -tam, lw / 2 + 24, tam * 0.36), 12, 12)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(240 * a))); cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 7))
    cv.drawString(s, -lw / 2, 0, f, paint(OURO, int(255 * a)))
    cv.restore()


# ------------------------------------------------------------------ o osso (genérico) e a trinca
BX, BY = 540, 735                     # centro do osso na tela
PIV = (27.0, -15.0)                   # pivô da "câmera" do osso: o meio da trinca (coordenadas locais)
H_D = 60                              # meia-largura da diáfise


def _path_osso():
    """Osso longo genérico, centrado em (0, 0), de -350 a +350. A ponta de cima é o platô do
    piloto (cf_alongamento); a de baixo alarga pouco e termina numa superfície levemente
    arredondada, SEM maléolo: não pretende ser um osso específico (a fonte não nomeia osso)."""
    h = H_D; y0, yb = -350, 350
    p = skia.Path()
    p.moveTo(-128, y0 + 40)
    p.cubicTo(-135, y0 - 6, -60, y0 - 18, -10, y0 + 6)
    p.cubicTo(30, y0 - 20, 132, y0 - 10, 126, y0 + 42)
    p.cubicTo(120, y0 + 120, h + 8, y0 + 150, h, y0 + 230)
    p.lineTo(h, yb - 190)
    p.cubicTo(h + 4, yb - 112, 98, yb - 74, 96, yb - 26)
    p.cubicTo(94, yb + 2, 44, yb - 8, 2, yb - 2)
    p.cubicTo(-42, yb + 4, -92, yb + 4, -94, yb - 28)
    p.cubicTo(-96, yb - 76, -h - 4, yb - 114, -h, yb - 190)
    p.lineTo(-h, y0 + 230)
    p.cubicTo(-h - 8, y0 + 150, -122, y0 + 120, -128, y0 + 40)
    p.close()
    return p


OSSO = _path_osso()
SH_OSSO = skia.GradientShader.MakeLinear([skia.Point(-140, 0), skia.Point(140, 0)],
                                         [C(OSSO_B), C(OSSO_C), C(OSSO_C), C(OSSO_B)], [0.0, 0.42, 0.58, 1.0])
N_SEG, N_INI = 13, 6                             # teto da trinca (não atravessa o osso) e o traço do espanto


def _trinca_pts():
    """Traço fino e IRREGULAR (passos e desvios desiguais, como uma trinca de verdade) que nasce na
    borda direita da diáfise e desce quase na vertical, parando no meio da diáfise (no canal): a
    trinca por estresse nunca chega perto da borda esquerda."""
    p0, p1 = (H_D + 2, -140.0), (-8.0, 110.0)
    passos = (1.0, 0.75, 1.2, 0.9, 1.15, 0.7, 1.0, 1.3, 0.8, 1.05, 1.1, 0.85, 1.0)[:N_SEG]
    desvio = (0, 7, -4, 9, -6, 3, 9, -5, 6, -8, 4, -6, 7, -3)[:N_SEG + 1]
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]; L = math.hypot(dx, dy); n = (-dy / L, dx / L)
    tot = sum(passos); acc = 0.0; pts = []
    for k in range(N_SEG + 1):
        f = acc / tot
        pts.append((p0[0] + dx * f + n[0] * desvio[k], p0[1] + dy * f + n[1] * desvio[k]))
        if k < N_SEG:
            acc += passos[k]
    return pts


TRINCA_PTS = _trinca_pts()
GALHOS = ((5, (12, 10)), (9, (-13, 6)))           # dois fios curtinhos (só comprimento, nada abre)


def tallies(T):
    """Instantes dos risquinhos: 15 em ritmo regular e rápido de "repetitivo" até "estresse" (o
    contador para ali) e mais 1 em "treino" (2ª)."""
    t0 = T["repetitivo"] + 0.05; t1 = T["estresse"] - 0.15
    dt = (t1 - t0) / 14
    return [t0 + i * dt for i in range(15)] + [T["treino2"] + 0.02]


def crescimentos(T):
    """Instantes em que a trinca ganha um traço: um por risquinho a partir de "poucos" (até o teto)."""
    out = []
    for ti in tallies(T)[:15]:
        if ti >= T["poucos"] - 0.05 and len(out) < N_SEG - N_INI:
            out.append(ti)
    return out


def segs(t, T):
    s = N_INI * e_out(prog(t, T["trincar"] + 0.02, T["trincar"] + 0.18))
    for ti in crescimentos(T):
        s += e_out(prog(t, ti, ti + 0.12))
    return min(s, N_SEG)


def esc_osso(t, T):
    """Escala do osso em torno da trinca: encosta no espanto, abre para o contador, aproxima
    enquanto a trinca cresce e volta antes do nome."""
    s = 1 + 0.18 * _k_espanto(t, T)
    s += 0.12 * e_inout(prog(t, T["poucos"] - 0.1, T["poucos"] + 0.6)) * (1 - e_inout(prog(t, T["fratura"] - 0.25, T["fratura"] + 0.35)))
    return s


def _k_espanto(t, T):
    """0..1: a aproximação do espanto (encosta em "trincar", abre de volta para o contador)."""
    return e_out(prog(t, T["trincar"], T["trincar"] + 0.35)) * (1 - e_inout(prog(t, T["treino"] - 0.15, T["treino"] + 0.45)))


def desce_osso(t, T):
    """Na aproximação do espanto o osso também desce um pouco: o topo não encosta no gancho."""
    return 20 * _k_espanto(t, T)


def tremor_osso(t, T):
    k = t - (T["trincar"] + 0.03)
    return 7 * math.sin(k * 70) * (1 - k / 0.35) if 0 <= k < 0.35 else 0.0


def na_tela(t, T, lx, ly):
    s = esc_osso(t, T)
    return BX + PIV[0] + (lx - PIV[0]) * s + tremor_osso(t, T), BY + PIV[1] + desce_osso(t, T) + (ly - PIV[1]) * s


def centro_trinca(t, T):
    return na_tela(t, T, *PIV)


def osso(cv, t, T):
    s = esc_osso(t, T)
    sq = 0.025 * math.sin(math.pi * prog(t, T["trincar"] + 0.02, T["trincar"] + 0.3))   # o "susto" do osso
    cv.save()
    cv.translate(BX + PIV[0] + tremor_osso(t, T), BY + PIV[1] + desce_osso(t, T)); cv.scale(s * (1 + sq), s * (1 - sq))
    cv.translate(-PIV[0], -PIV[1])
    cv.save(); cv.translate(0, 10)
    cv.drawPath(OSSO, paint("#000000", 80, blur=16))
    cv.restore()
    cv.drawPath(OSSO, paint(OSSO_C, shader=SH_OSSO))
    cv.drawRect(skia.Rect(-15, -150, 15, 150), paint(OSSO_B, 55, blur=7))          # canal (profundidade)
    cv.drawLine(-30, -300, -30, 280, paint("#FFFFFF", 50, "stroke", 6, blur=5))     # brilho do marfim
    cv.drawPath(OSSO, _p(OSSO_L, 150, "stroke", 2.5, junta=True))
    n = segs(t, T)
    if n > 0:
        # lampejo do espanto: um halo branco FORA do clip (aparece contra o fundo escuro, à direita da
        # borda onde a trinca nasce) e outro dentro do osso, ao longo do traço (nunca dourado)
        fl = (1 - prog(t, T["trincar"] + 0.05, T["trincar"] + 0.6)) if t >= T["trincar"] + 0.02 else 0.0
        if fl > 0:
            cv.drawPath(_poli(TRINCA_PTS, n / N_SEG), _p("#FFFFFF", int(230 * fl), "stroke", 30, blur=14, junta=True))
            _estalo(cv, t, T)
        cv.save(); cv.clipPath(OSSO, skia.ClipOp.kIntersect, True)
        if fl > 0:
            cv.drawPath(_poli(TRINCA_PTS, n / N_SEG), _p("#FFFFFF", int(230 * fl), "stroke", 22, blur=10, junta=True))
        for ti in crescimentos(T):
            k = t - ti
            if 0 <= k < 0.35:
                x, y = _ponto_trinca(n)
                cv.drawCircle(x, y, 18, paint("#FFFFFF", int(170 * (1 - k / 0.35)), blur=9))
        _traco_trinca(cv, n, 1.6, 2.0, "#FFFDF6", 170, 0.45)               # borda clara: traço "gravado"
        _traco_trinca(cv, n, 0, 0, TRINCA, 255, 1.0)
        for k, (dx, dy) in GALHOS:
            g = clamp((n - k - 0.4) / 0.6)
            if g > 0:
                x0, y0 = TRINCA_PTS[k]
                cv.drawLine(x0, y0, x0 + dx * g, y0 + dy * g, _p(TRINCA, 235, "stroke", 2.6))
        cv.restore()
    cv.restore()
    # ondas brancas do espanto (não é dourado: a trinca não é osso novo)
    for atraso, r1 in ((0.05, 170), (0.18, 260)):
        k = t - (T["trincar"] + atraso)
        if 0 <= k < 0.6:
            x, y = na_tela(t, T, *TRINCA_PTS[3])
            cv.drawCircle(x, y, lerp(16, r1, e_out(k / 0.6)), paint("#FFFFFF", int(255 * (1 - k / 0.6)), "stroke", 6))


def _estalo(cv, t, T):
    """Riscos curtos de "estalo" saindo da borda onde a trinca nasce, para FORA do osso (só no
    espanto; brancos, nada de sangue). Coordenadas locais do osso."""
    k = prog(t, T["trincar"] + 0.02, T["trincar"] + 0.42)
    if not 0 < k < 1:
        return
    x0, y0 = TRINCA_PTS[0]
    r0, r1 = lerp(14, 40, e_out(k)), lerp(34, 92, e_out(k))
    a = 1 - k
    for ang in (-62, -30, 0, 30, 62):
        c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        cv.drawLine(x0 + c * r0, y0 + s * r0, x0 + c * r1, y0 + s * r1, paint("#FFFFFF", int(255 * a), "stroke", 7))


def _ponto_trinca(n):
    i = min(int(n), N_SEG - 1); f = n - i
    (x0, y0), (x1, y1) = TRINCA_PTS[i], TRINCA_PTS[min(i + 1, N_SEG)]
    return lerp(x0, x1, f), lerp(y0, y1, f)


def _traco_trinca(cv, n, ox, oy, cor, alfa, esc_larg):
    """Desenha a trinca até `n` traços, afinando da borda (6,5 px) para a ponta (2,8 px)."""
    for j in range(int(math.ceil(n))):
        f = clamp(n - j)
        if f <= 0:
            break
        (x0, y0), (x1, y1) = TRINCA_PTS[j], TRINCA_PTS[j + 1]
        w = lerp(8.5, 3.6, j / (N_SEG - 1)) * esc_larg
        cv.drawLine(x0 + ox, y0 + oy, lerp(x0, x1, f) + ox, lerp(y0, y1, f) + oy, paint(cor, alfa, "stroke", w))


# ------------------------------------------------------------------ queda (pictograma riscado)
def boneco(cv, x, y, ang, a):
    """Pictograma em contorno de um boneco caindo de costas (traços brancos, sem rosto)."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.rotate(ang); cv.scale(1.15, 1.15)
    pt = paint("#FFFFFF", int(255 * a), "stroke", 9)
    cv.drawCircle(0, -66, 19, paint("#FFFFFF", int(255 * a), "stroke", 8))
    cv.drawLine(0, -42, 0, 18, pt)
    cv.drawLine(0, -30, -40, -62, pt); cv.drawLine(0, -30, 42, -54, pt)          # braços para o alto
    cv.drawLine(0, 18, -30, 66, pt); cv.drawLine(0, 18, 24, 50, pt); cv.drawLine(24, 50, 44, 72, pt)
    cv.restore()


def queda(cv, t, T):
    t0 = T["queda"] - 0.1
    a = prog(t, t0, t0 + 0.2) * (1 - prog(t, T["repetitivo"] + 0.2, T["repetitivo"] + 0.55))
    if a <= 0:
        return
    k = e_out(prog(t, t0, t0 + 0.45))
    x, y = 222, 470
    # linhas de movimento acima (o boneco está caindo)
    for i, dx in enumerate((-46, -10, 26)):
        la = a * prog(t, t0 + 0.05 * i, t0 + 0.2 + 0.05 * i)
        cv.drawLine(x + dx + 40, y - 150 + 12 * i, x + dx + 40, y - 112 + 12 * i, paint(AZUL, int(200 * la), "stroke", 5))
    cv.drawLine(x - 90, y + 92, x + 90, y + 92, paint("#FFFFFF", int(110 * a), "stroke", 4))     # chão
    boneco(cv, x, y - 40 * (1 - k), lerp(-12, -42, k), a)
    # o traço reto que risca
    r = e_out(prog(t, T["queda"] + 0.12, T["queda"] + 0.3))
    if r > 0:
        p0, p1 = (x + 92, y - 104), (x - 92, y + 96)
        pe = (lerp(p0[0], p1[0], r), lerp(p0[1], p1[1], r))
        cv.drawLine(*p0, *pe, paint(FUNDO_CARTAO, int(200 * a), "stroke", 18))
        cv.drawLine(*p0, *pe, paint(DOR_C, int(255 * a), "stroke", 10))
    t_c = T["queda"] + 0.3
    carimbo_opaco(cv, SEM_QUEDA, 248, 664, -6, t_c, t, dur=T["repetitivo"] + 0.55 - t_c, tam=56, esc0=1.8)


# ------------------------------------------------------------------ contador TREINO (risquinhos de giz)
CT_X0, CT_Y0, CT_X1, CT_Y1 = 706, 252, 1036, 466
TX0, TY0, TY1, PITCH = 738, 344, 434, 75


def tenis(cv, x, y, esc, a, cor="#FFFFFF"):
    """Tênis em contorno, de lado (cópia do cf_osgood_sever)."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    p = skia.Path()
    p.moveTo(-78, 18); p.lineTo(-78, -30)
    p.cubicTo(-78, -48, -64, -54, -50, -50)
    p.lineTo(-30, -46)
    p.cubicTo(-14, -24, 10, -18, 30, -14)
    p.cubicTo(58, -8, 80, 0, 82, 14)
    p.lineTo(82, 18); p.close()
    cv.drawPath(p, paint(FUNDO_CARTAO, int(150 * a)))
    cv.drawPath(p, _p(cor, int(255 * a), "stroke", 5, junta=True))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-84, 14, 88, 32), 9, 9), paint(OURO, int(255 * a)))
    for k in range(3):                                   # cadarço
        xx = -22 + k * 16
        cv.drawLine(xx, -36 + k * 5, xx + 12, -24 + k * 5, paint(OURO, int(255 * a), "stroke", 4))
    cv.restore()


def pausa(cv, x, y, r, a, cor="#FFFFFF"):
    """Ícone NEUTRO de pausa em contorno: duas barras verticais num anel (sem lua, sem cama)."""
    if a <= 0:
        return
    cv.drawCircle(x, y, r, paint(FUNDO_CARTAO, int(170 * a)))
    cv.drawCircle(x, y, r, paint(cor, int(255 * a), "stroke", 5))
    for dx in (-r * 0.3, r * 0.3):
        rr = skia.RRect.MakeRectXY(skia.Rect(x + dx - r * 0.13, y - r * 0.46, x + dx + r * 0.13, y + r * 0.46), 5, 5)
        cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 4.5))


def contador(cv, t, T):
    ent = e_out(prog(t, T["treino"] - 0.05, T["treino"] + 0.45))
    sai = e_in_back(prog(t, T["dor3"] - 0.1, T["dor3"] + 0.35))
    a = clamp(ent * 1.5) * (1 - prog(t, T["dor3"] + 0.1, T["dor3"] + 0.35))
    if a <= 0:
        return
    cv.save(); cv.translate(420 * (1 - ent), -260 * sai)
    rr = skia.RRect.MakeRectXY(skia.Rect(CT_X0, CT_Y0, CT_X1, CT_Y1), 22, 22)
    cv.drawRRect(rr, paint("#000000", int(90 * a), blur=14))
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(235 * a)))
    cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 3))
    texto(cv, TREINO, CT_X0 + 28, CT_Y0 + 52, F_BLACK, 38, OURO, int(255 * a), centro=False)
    tenis(cv, CT_X1 - 62, CT_Y0 + 34, 0.36, a)
    cv.drawLine(CT_X0 + 26, CT_Y0 + 70, CT_X1 - 26, CT_Y0 + 70, paint("#FFFFFF", int(40 * a), "stroke", 2))
    for i, ti in enumerate(tallies(T)):
        pr = e_out(prog(t, ti, ti + 0.1))
        if pr <= 0:
            continue
        g, j = divmod(i, 5)
        gx = TX0 + g * PITCH
        if j < 4:
            x = gx + j * 14 + 3 * (_acaso(i, 1) - 0.5)
            p0 = (x + 4 * (_acaso(i, 2) - 0.5), TY0 + 4 * _acaso(i, 3))
            p1 = (x + 5 * (_acaso(i, 4) - 0.5), TY1 - 4 * _acaso(i, 5))
        else:
            p0 = (gx - 12, TY1 - 10); p1 = (gx + 56, TY0 + 12)
        pe = (lerp(p0[0], p1[0], pr), lerp(p0[1], p1[1], pr))
        cv.drawLine(*p0, *pe, paint(GIZ, int(45 * a), "stroke", 12, blur=4))
        cv.drawLine(*p0, *pe, paint(GIZ, int(240 * a), "stroke", 6))
        fl = 1 - prog(t, ti, ti + 0.3)                                        # lampejo do giz novo
        if fl > 0:
            cv.drawCircle(*pe, 12, paint("#FFFFFF", int(150 * fl * a), blur=8))
    cv.restore()


def cartao_pancada(cv, t, T):
    k = prog(t, T["pancada"] - 0.05, T["pancada"] + 0.3)
    a = k * (1 - prog(t, T["sinal"] - 0.3, T["sinal"]))
    if a <= 0:
        return
    dy = 24 * (1 - e_out(k))
    x0, x1, y0, y1 = 666, 1036, 498 + dy, 618 + dy
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 18, 18)
    cv.drawRRect(rr, paint("#000000", int(70 * a), blur=10))
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(232 * a)))
    cv.drawRRect(rr, paint("#FFFFFF", int(150 * a), "stroke", 2.5))
    cx = (x0 + x1) / 2
    texto(cv, PANCADA[0], cx, y0 + 48, F_BLACK, 32, "#FFFFFF", int(255 * a))
    k2 = prog(t, T["unica"] - 0.05, T["unica"] + 0.25)
    texto(cv, PANCADA[1], cx, y0 + 98, F_BLACK, 40, OURO, int(255 * a * max(0.35, k2)))


# ------------------------------------------------------------------ barra DOR, ícones, placa de aviso
BAR_X, BAR_W, BAR_Y0, BAR_Y1 = 700, 56, 664, 910
IC_X = 884
TRI = ((842, 612), (994, 880), (690, 880))              # placa de aviso: ápice, base direita, base esquerda


def nivel_dor(t, T):
    n = 0.1
    n = lerp(n, 0.9, e_inout(prog(t, T["atividade"], T["atividade"] + 0.6)))
    n = lerp(n, 0.16, e_inout(prog(t, T["repouso"], T["repouso"] + 0.6)))
    n = lerp(n, 0.86, e_inout(prog(t, T["dor2"], T["dor2"] + 0.9)))            # de novo, devagar
    n = lerp(n, 0.16, e_inout(prog(t, desce2(T), desce2(T) + 0.6)))
    n = lerp(n, 0.86, e_inout(prog(t, T["treino2"], T["treino2"] + 0.5)))     # "a cada treino": volta a doer
    n = lerp(n, 1.0, e_out(prog(t, T["dor3"], T["dor3"] + 0.35)))
    return n


def desce2(T):
    return T["ponto"] + 0.2


def acesos(t, T):
    """(tênis, pausa): 0..1 de quão aceso está cada ícone."""
    def degrau(t0):
        return e_inout(prog(t, t0, t0 + 0.2))
    ten = (degrau(T["atividade"]) - degrau(T["repouso"]) + degrau(T["dor2"]) - degrau(desce2(T))
           + degrau(T["treino2"]))
    pau = degrau(T["repouso"]) - degrau(T["dor2"]) + degrau(desce2(T)) - degrau(T["treino2"])
    return clamp(ten), clamp(pau)


def _ret_arredondado(x0, y0, x1, y1):
    r = (x1 - x0) / 2; cx = (x0 + x1) / 2; pts = []
    for i in range(10):
        a = math.radians(-90 + 90 * i / 9); pts.append((cx + r * math.cos(a), y0 + r + r * math.sin(a)))
    for i in range(19):
        a = math.radians(0 + 180 * i / 18); pts.append((cx + r * math.cos(a), y1 - r + r * math.sin(a)))
    for i in range(10):
        a = math.radians(180 + 90 * i / 9); pts.append((cx + r * math.cos(a), y0 + r + r * math.sin(a)))
    return pts


def _reamostra(pts, n):
    segs_ = list(zip(pts, pts[1:] + pts[:1]))
    lens = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs_]
    tot = sum(lens); out = []
    for i in range(n):
        d = tot * i / n
        for (a, b), L in zip(segs_, lens):
            if d <= L and L > 0:
                f = d / L
                out.append((lerp(a[0], b[0], f), lerp(a[1], b[1], f))); break
            d -= L
        else:
            out.append(pts[0])
    return out


N_MORPH = 90
BAR_PTS = _reamostra(_ret_arredondado(BAR_X - BAR_W / 2, BAR_Y0, BAR_X + BAR_W / 2, BAR_Y1), N_MORPH)
TRI_PTS = _reamostra(list(TRI), N_MORPH)


def morph(t, T):
    return e_inout(prog(t, T["aviso"] - 0.1, T["aviso"] + 0.3))


def bloco_dor(cv, t, T):
    ent = e_out(prog(t, T["sinal"] - 0.05, T["sinal"] + 0.45))
    if ent <= 0:
        return
    cv.save(); cv.translate(360 * (1 - ent), 0)
    a = clamp(ent * 1.6)
    m = morph(t, T)
    nv = nivel_dor(t, T)
    # título DOR (sai quando a barra vira placa)
    a_t = a * prog(t, T["dor1"] - 0.05, T["dor1"] + 0.2) * (1 - prog(t, T["aviso"] - 0.2, T["aviso"]))
    if a_t > 0:
        texto(cv, DOR, BAR_X, BAR_Y0 - 22, F_BLACK, 38, DOR_TXT, int(255 * a_t))
    if m <= 0:
        rr = skia.RRect.MakeRectXY(skia.Rect(BAR_X - BAR_W / 2, BAR_Y0, BAR_X + BAR_W / 2, BAR_Y1), BAR_W / 2, BAR_W / 2)
        cv.drawRRect(rr, paint(FUNDO_CARTAO, int(200 * a)))
        cv.drawRRect(rr, paint("#FFFFFF", int(70 * a), "stroke", 3))
        alt = (BAR_Y1 - BAR_Y0 - 10) * nv
        if alt > 1:
            yt = BAR_Y1 - 5 - alt
            fr = skia.RRect.MakeRectXY(skia.Rect(BAR_X - BAR_W / 2 + 6, yt, BAR_X + BAR_W / 2 - 6, BAR_Y1 - 5), 22, 22)
            sh = skia.GradientShader.MakeLinear([skia.Point(0, BAR_Y1), skia.Point(0, BAR_Y0)], [C(DOR_C), C(DOR_CL)])
            cv.drawRRect(fr, paint(DOR_C, int(110 * a * nv), blur=14))
            cv.drawRRect(fr, paint(DOR_C, int(255 * a), shader=sh))
        # marcas da régua (sem número)
        for i in range(1, 5):
            yy = lerp(BAR_Y1, BAR_Y0, i / 5)
            cv.drawLine(BAR_X - BAR_W / 2 - 16, yy, BAR_X - BAR_W / 2 - 6, yy, paint("#FFFFFF", int(110 * a), "stroke", 2.5))
    else:
        # a barra se dobra e vira a placa triangular de aviso
        pts = [(lerp(b[0], c[0], m), lerp(b[1], c[1], m)) for b, c in zip(BAR_PTS, TRI_PTS)]
        pth = skia.Path(); pth.moveTo(*pts[0])
        for q in pts[1:]:
            pth.lineTo(*q)
        pth.close()
        cor = lerpc(DOR_C, AMARELO, m)
        a_p = a * (1 - prog(t, T["aumentar"] + 0.1, T["aumentar"] + 0.5))
        cv.drawPath(pth, _p(cor, int(110 * a_p), blur=18, canto=14))
        cv.drawPath(pth, _p(cor, int(255 * a_p), canto=14))
        cv.drawPath(pth, _p(lerpc("#9E2E33", AMARELO_ESC, m), int(255 * a_p), "stroke", 4, junta=True, canto=14))
        # "!" desenhado (traço + ponto), não texto
        k = e_back(prog(t, T["aviso"] + 0.25, T["aviso"] + 0.5))
        if k > 0:
            cx = TRI[0][0]
            cv.save(); cv.translate(cx, 790); cv.scale(k, k)
            cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-11, -98, 11, 4), 10, 10), paint(FUNDO_CARTAO, int(255 * a_p)))
            cv.drawCircle(0, 38, 13, paint(FUNDO_CARTAO, int(255 * a_p)))
            cv.restore()
    # ícones (somem quando a barra vira placa)
    ten, pau = acesos(t, T)
    a_i = a * (1 - prog(t, T["dor3"] - 0.1, T["dor3"] + 0.25))
    k1 = e_back(prog(t, T["atividade"] - 0.05, T["atividade"] + 0.3))
    if k1 > 0 and a_i > 0:
        al = a_i * clamp(k1 * 2) * lerp(0.32, 1.0, ten)
        if ten > 0.01:
            cv.drawCircle(IC_X, 704, 82, paint(DOR_C, int(70 * ten * a_i), blur=26))
        tenis(cv, IC_X, 712 - 10 * ten, 0.86 * k1, al, cor=lerpc("#8FA3B8", "#FFFFFF", ten))
        texto(cv, ATIVIDADE, IC_X, 792, F_BLACK, 34, lerpc("#8FA3B8", "#FFFFFF", ten), int(255 * al))
    k2 = e_back(prog(t, T["repouso"] - 0.05, T["repouso"] + 0.3))
    if k2 > 0 and a_i > 0:
        al = a_i * clamp(k2 * 2) * lerp(0.32, 1.0, pau)
        if pau > 0.01:
            cv.drawCircle(IC_X, 858, 66, paint(AZUL, int(60 * pau * a_i), blur=24))
        pausa(cv, IC_X, 858, 38 * k2, al, cor=lerpc("#8FA3B8", "#FFFFFF", pau))
        texto(cv, REPOUSO, IC_X, 940, F_BLACK, 34, lerpc("#8FA3B8", "#FFFFFF", pau), int(255 * al))
    # setinha de sentido ao lado da barra (sobe / desce)
    for t0, sobe, dur in ((T["atividade"], True, 0.6), (T["repouso"], False, 0.6), (T["dor2"], True, 0.9),
                          (desce2(T), False, 0.6), (T["treino2"], True, 0.5)):
        kk = prog(t, t0, t0 + dur)
        if 0 < kk < 1:
            aa = a * math.sin(math.pi * kk)
            y = lerp(BAR_Y1 - 40, BAR_Y0 + 40, kk if sobe else 1 - kk)
            xx = BAR_X + BAR_W / 2 + 26
            p = skia.Path()
            if sobe:
                p.moveTo(xx - 12, y + 8); p.lineTo(xx, y - 8); p.lineTo(xx + 12, y + 8)
            else:
                p.moveTo(xx - 12, y - 8); p.lineTo(xx, y + 8); p.lineTo(xx + 12, y - 8)
            cv.drawPath(p, _p(DOR_CL if sobe else AZUL, int(255 * aa), "stroke", 5, junta=True))
    cv.restore()


# ------------------------------------------------------------------ alvo (mesmo ponto)
def alvo(cv, t, T):
    a = prog(t, T["ponto"] - 0.05, T["ponto"] + 0.2) * (1 - prog(t, T["dor3"] - 0.1, T["dor3"] + 0.3))
    if a <= 0:
        return
    x, y = centro_trinca(t, T)
    for t0 in (T["ponto"], T["treino2"] + 0.02):                 # pulsa no MESMO lugar, no mesmo ritmo
        k = t - t0
        if 0 <= k < 0.7:
            r = lerp(30, 100, e_out(k / 0.7))           # não encosta na barra DOR nem no título
            cv.drawCircle(x, y, r, paint(AMARELO, int(220 * (1 - k / 0.7) * a), "stroke", 6))
    resp = 1 + 0.05 * math.sin((t - T["ponto"]) * 2 * math.pi / 0.88)
    for r, w, al in ((86, 5, 150), (58, 5, 190), (30, 5, 230)):
        cv.drawCircle(x, y, r * resp, paint(AMARELO, int(al * a), "stroke", w))
    cv.drawCircle(x, y, 92 * resp, paint(AMARELO, int(50 * a), "stroke", 14, blur=10))


# ------------------------------------------------------------------ cartão de atenção
CA_X0, CA_X1, CA_Y0, CA_Y1 = 100, 980, 968, 1196


def cartao_avaliacao(cv, t, T):
    t_in = T["avaliacao"] - 0.05
    a = prog(t, t_in, t_in + 0.3)
    if a <= 0:
        return
    dy = 50 * (1 - e_out(prog(t, t_in, t_in + 0.45)))
    cv.save(); cv.translate(0, dy)
    card = skia.RRect.MakeRectXY(skia.Rect(CA_X0, CA_Y0, CA_X1, CA_Y1), 28, 28)
    cv.drawRRect(card, paint("#000000", int(90 * a), blur=16))
    cv.drawRRect(card, paint(FUNDO_CARTAO, int(245 * a)))
    cv.drawRRect(card, paint(AMARELO, int(255 * a), "stroke", 5))
    cx = (CA_X0 + CA_X1) / 2
    esc = lerp(0.88, 1.0, e_back(prog(t, t_in, t_in + 0.4)))
    cv.save(); cv.translate(cx, CA_Y0 + 92); cv.scale(esc, esc)
    texto(cv, AVALIACAO[0], 0, 0, F_BLACK, 58, AMARELO, int(255 * a))
    cv.restore()
    cv.drawLine(cx - 300, CA_Y0 + 130, cx + 300, CA_Y0 + 130, paint(AMARELO, int(110 * a), "stroke", 2.5))
    a2 = a * prog(t, t_in + 0.25, t_in + 0.55)
    texto(cv, AVALIACAO[1], cx, CA_Y0 + 186, F_BLACK, 40, AZUL, int(255 * a2))
    cv.restore()


# ------------------------------------------------------------------ troféu
def trofeu_desenho(cv, a):
    """Troféu em contorno, base em (0, 0)."""
    copa = skia.Path()
    copa.moveTo(-56, -156); copa.lineTo(56, -156)
    copa.cubicTo(56, -98, 32, -74, 0, -72); copa.cubicTo(-32, -74, -56, -98, -56, -156); copa.close()
    cv.drawPath(copa, paint(FUNDO_CARTAO, int(200 * a)))
    cv.drawPath(copa, _p(OURO, int(255 * a), "stroke", 6, junta=True))
    for s in (-1, 1):
        al = skia.Path(); al.moveTo(56 * s, -144)
        al.cubicTo(92 * s, -144, 92 * s, -100, 44 * s, -96)
        cv.drawPath(al, _p(OURO, int(255 * a), "stroke", 6, junta=True))
    cv.drawLine(0, -72, 0, -38, paint(OURO, int(255 * a), "stroke", 12))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-36, -40, 36, -20), 6, 6), _p(OURO, int(255 * a), "stroke", 5))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-50, -20, 50, 0), 6, 6), paint(FUNDO_CARTAO, int(220 * a)))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-50, -20, 50, 0), 6, 6), _p(OURO, int(255 * a), "stroke", 5))
    cv.drawLine(-26, -142, -26, -112, paint("#FFFFFF", int(110 * a), "stroke", 5))     # brilho


def tempos_trofeu(T):
    d0 = T["aviso"] + 0.35; d1 = T["trofeu"] + 0.02
    s0 = d1 + 0.42; s1 = s0 + 0.5
    return d0, d1, s0, s1


def trofeu(cv, t, T):
    d0, d1, s0, s1 = tempos_trofeu(T)
    if t < d0 or t > s1:
        return
    ax, ay = TRI[0]
    if t < d1:                                                   # desce em direção à ponta da placa
        k = e_out(prog(t, d0, d1))
        x, y, ang = ax, lerp(-60, ay - 4, k), 0.0
    elif t < s0:                                                 # não encaixa: balança na ponta
        k = t - d1
        x, y, ang = ax, ay - 4, 13 * math.sin(k * 15) * math.exp(-1.2 * k) + 6 * prog(t, d1 + 0.2, s0)
    else:                                                        # escorrega para fora da tela
        k = e_in_back(prog(t, s0, s1), 1.2)
        x, y, ang = lerp(ax, 1260, k), lerp(ay - 4, ay + 260, k), lerp(6, 48, k)
    cv.save(); cv.translate(x, y); cv.rotate(ang)
    trofeu_desenho(cv, 1.0)
    cv.restore()


# ------------------------------------------------------------------ escada de carga
ST_X0, ST_Y0, RISE, RUN, RUN_L, LAND, N_DEG = 74, 1190, 62, 84, 224, 4, 9


def tempos_escada(T):
    """Por degrau: (t0, t1) do espelho (sobe) e do piso (anda). Degraus 0-3 até "descanso"; o 4º é o
    patamar, que se alarga em "descanso"; a escada só volta a subir depois da pausa."""
    t0 = T["aumentar"] + 0.42; tl = T["descanso"] - 0.12
    d1 = (tl - t0) / 4.4
    out = []
    for i in range(4):
        a = t0 + i * d1
        out.append(((a, a + 0.32 * d1), (a + 0.32 * d1, a + d1)))
    a = t0 + 4 * d1
    out.append(((a, a + 0.4 * d1), (T["descanso"] - 0.1, T["descanso"] + 0.5)))
    t2 = T["descanso"] + 0.95; d2 = 0.3
    for i in range(4):
        a = t2 + i * d2
        out.append(((a, a + 0.32 * d2), (a + 0.32 * d2, a + d2)))
    return out


def _cantos_escada():
    pts = [(ST_X0, ST_Y0)]; x, y = ST_X0, ST_Y0
    for i in range(N_DEG):
        y -= RISE; pts.append((x, y))
        x += RUN_L if i == LAND else RUN; pts.append((x, y))
    return pts


CANTOS = _cantos_escada()
SH_ESC = skia.GradientShader.MakeLinear([skia.Point(0, 620), skia.Point(0, 1214)],
                                        [C(ACO, 165), C(ACO_ESC, 105), C(ACO_ESC, 0)], [0.0, 0.78, 1.0])


def escada(cv, t, T):
    a = prog(t, T["aumentar"] + 0.3, T["aumentar"] + 0.5)
    if a <= 0:
        return
    te = tempos_escada(T)
    perfil = [CANTOS[0]]
    ponta_ = CANTOS[0]
    for i, ((e0, e1), (p0, p1)) in enumerate(te):
        c0, c1, c2 = CANTOS[2 * i], CANTOS[2 * i + 1], CANTOS[2 * i + 2]
        ke = e_inout(prog(t, e0, e1))
        if ke <= 0:
            break
        ponta_ = (c0[0], lerp(c0[1], c1[1], ke)); perfil.append(ponta_)
        kp = e_inout(prog(t, p0, p1))
        if kp <= 0:
            break
        ponta_ = (lerp(c1[0], c2[0], kp), c1[1]); perfil.append(ponta_)
    if len(perfil) < 2:
        return
    # bloco (aço azul-claro) por baixo do perfil
    blo = skia.Path(); blo.moveTo(ST_X0, 1210)
    for q in perfil:
        blo.lineTo(*q)
    blo.lineTo(perfil[-1][0], 1210); blo.close()
    cv.drawPath(blo, paint(ACO, int(255 * a), shader=SH_ESC))
    # espelhos: linhas verticais sutis no bloco
    for i in range(len(perfil) // 2):
        x, y = perfil[2 * i + 1] if 2 * i + 1 < len(perfil) else perfil[-1]
        cv.drawLine(x, y, x, 1200, paint(ACO_HL, int(40 * a), "stroke", 2))
    pr = skia.Path(); pr.moveTo(*perfil[0])
    for q in perfil[1:]:
        pr.lineTo(*q)
    cv.drawPath(pr, _p("#000000", int(90 * a), "stroke", 12, blur=6, junta=True))
    cv.drawPath(pr, _p(ACO, int(255 * a), "stroke", 8, junta=True))
    # bordas de cima dos pisos (brilho do aço) e o lampejo do degrau que acabou de assentar
    for i, (_, (p0, p1)) in enumerate(te):
        if t < p1:
            continue
        c1, c2 = CANTOS[2 * i + 1], CANTOS[2 * i + 2]
        cv.drawLine(c1[0] + 4, c1[1] - 3, c2[0] - 4, c2[1] - 3, paint(ACO_HL, int(230 * a), "stroke", 3))
        fl = 1 - prog(t, p1, p1 + 0.35)
        if fl > 0:
            cv.drawLine(c1[0], c1[1], c2[0], c2[1], paint("#FFFFFF", int(150 * fl * a), "stroke", 14, blur=8))
    # a ponta que desenha
    em_curso = te[0][0][0] <= t <= te[-1][1][1]
    if em_curso:
        cv.drawCircle(*ponta_, 16, paint(ACO_HL, int(110 * a), blur=10))
        cv.drawCircle(*ponta_, 7, paint("#FFFFFF", int(255 * a)))
    # o patamar: ícone de pausa e o rótulo
    c1, c2 = CANTOS[2 * LAND + 1], CANTOS[2 * LAND + 2]
    xm = (c1[0] + c2[0]) / 2
    k = e_back(prog(t, T["descanso"] + 0.15, T["descanso"] + 0.45))
    if k > 0:
        pul = 1 + 0.06 * math.sin(math.pi * prog(t, T["descanso"] + 0.45, T["descanso"] + 0.95))
        some = 1 - prog(t, T["manda"] - 0.3, T["manda"])         # some por inteiro na CTA (não briga com a frase)
        if some > 0:
            cv.drawCircle(xm, c1[1] - 54, 62, paint(AZUL, int(60 * a * clamp(k) * some), blur=22))
            pausa(cv, xm, c1[1] - 54, 38 * k * pul, a * clamp(k * 2) * some)
    chip(cv, DESCANSO, xm, c1[1] + 112, ACO_HL, a * prog(t, T["descanso"] + 0.2, T["descanso"] + 0.45), tam=32,
         cor_txt="#FFFFFF", esc=lerp(0.85, 1.0, e_back(prog(t, T["descanso"] + 0.2, T["descanso"] + 0.5))))


def rotulos_escada(cv, t, T):
    fim = 1 - prog(t, T["manda"] - 0.45, T["manda"] - 0.15)
    k = prog(t, T["aumentar"] + 0.35, T["aumentar"] + 0.65)
    chip(cv, AUMENTAR, 540, 344, ACO_HL, k * fim, tam=40, cor_txt="#FFFFFF",
         esc=lerp(0.9, 1.0, e_back(prog(t, T["aumentar"] + 0.35, T["aumentar"] + 0.7))))
    k = prog(t, T["previne"] - 0.05, T["previne"] + 0.3)
    if k > 0:
        texto(cv, PREVINE, 540, 482 + 16 * (1 - e_out(k)), F_BLACK, 50, "#FFFFFF", int(255 * k * fim), contorno=10)


# ------------------------------------------------------------------ rótulos da trinca
def rotulos_trinca(cv, t, T):
    xa, ya = na_tela(t, T, *TRINCA_PTS[max(1, min(N_SEG, int(segs(t, T))))])
    a = prog(t, T["poucos"] + 0.05, T["poucos"] + 0.3) * (1 - prog(t, T["estresse"] - 0.3, T["estresse"]))
    rotulo(cv, AOS_POUCOS, 436, 872, xa - 6, ya + 4, "#FFFFFF", a, esq=False)
    x, y = centro_trinca(t, T)
    a = prog(t, T["ponto"] + 0.05, T["ponto"] + 0.3) * (1 - prog(t, T["merece"], T["merece"] + 0.3))
    rotulo(cv, MESMO_PONTO, 436, 600, x - 88, y - 8, AMARELO, a, esq=False)


def nome(cv, t, T):
    k = prog(t, T["estresse"] - 0.05, T["estresse"] + 0.3)
    a = k * (1 - prog(t, T["avaliacao"] - 0.4, T["avaliacao"] - 0.1))
    if a <= 0:
        return
    chip(cv, NOME, 540, 1160 + 14 * (1 - e_out(k)), OSSO_B, a, tam=36, cor_txt="#FFFFFF")


# ------------------------------------------------------------------ quadro
def mundo_1(cv, t, T):
    """Tudo o que existe antes da troca de cena (osso, contador, dor, alvo, cartão, placa)."""
    osso(cv, t, T)
    alvo(cv, t, T)
    queda(cv, t, T)
    contador(cv, t, T)
    cartao_pancada(cv, t, T)
    bloco_dor(cv, t, T)
    rotulos_trinca(cv, t, T)
    nome(cv, t, T)
    a = prog(t, T["treino2"] + 0.05, T["treino2"] + 0.3) * (1 - prog(t, T["dor3"] - 0.15, T["dor3"] + 0.15))
    chip(cv, CADA_TREINO, 860, 568, OURO, a, tam=36, cor_txt="#FFFFFF",
         esc=lerp(0.85, 1.0, e_back(prog(t, T["treino2"] + 0.05, T["treino2"] + 0.4))))
    cartao_avaliacao(cv, t, T)
    # os dois chips saem ANTES da troca de cena (senão NÃO TROFÉU, encolhendo, passa por baixo do AUMENTAR)
    sai = 1 - prog(t, T["aumentar"] - 0.15, T["aumentar"] + 0.1)
    a = prog(t, T["aviso"] + 0.2, T["aviso"] + 0.45) * sai
    chip(cv, AVISO, TRI[0][0], 940, AMARELO, a, tam=40, cor_txt="#FFFFFF",
         esc=lerp(0.85, 1.0, e_back(prog(t, T["aviso"] + 0.2, T["aviso"] + 0.55))))
    trofeu(cv, t, T)
    a = prog(t, T["trofeu"] + 0.1, T["trofeu"] + 0.35) * sai
    chip(cv, TROFEU, TRI[0][0], 360, OURO, a, tam=40, cor_txt="#FFFFFF",
         esc=lerp(0.85, 1.0, e_back(prog(t, T["trofeu"] + 0.1, T["trofeu"] + 0.45))))


def troca(T):
    return T["aumentar"] + 0.05


def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    k = e_inout(prog(t, troca(T), troca(T) + 0.5))
    if k < 1:
        if k > 0:                                                # o mundo recua e sai (a trinca não cola)
            cv.saveLayerAlpha(None, int(255 * (1 - k)))
            cv.translate(540, 760); cv.scale(1 - 0.18 * k, 1 - 0.18 * k); cv.translate(-540, -760 - 60 * k)
        else:
            cv.save()
        mundo_1(cv, t, T)
        cv.restore()
    escada(cv, t, T)
    rotulos_escada(cv, t, T)
    capa(cv, t, T["queda"] - 0.2, ep["gancho"][0], ep["gancho"][1])
    selo_como_funciona(cv, prog(t, T["queda"] + 0.3, T["queda"] + 0.7) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface(cv, t, T, blocos, DESTAQUE)


# ------------------------------------------------------------------ som e prévias
def sons(T):
    ev = [(T["trincar"] + 0.02, "crackle", 0.95), (T["trincar"] + 0.03, "tick", 0.9),
          (T["queda"] - 0.12, "whoosh", 0.45), (T["queda"] + 0.14, "tick", 0.6), (T["queda"] + 0.3, "thump", 0.9),
          (T["treino"] - 0.05, "whoosh", 0.45), (T["treino"] + 0.3, "pop", 0.4)]
    ev += [(ti, "click", 0.42) for ti in tallies(T)]
    ev += [(ti + 0.02, "tick", 0.3) for ti in crescimentos(T)]
    ev += [(T["poucos"] + 0.1, "pop", 0.35), (T["pancada"], "pop", 0.5), (T["unica"], "tick", 0.4),
           (T["fratura"] - 0.2, "whoosh", 0.3), (T["estresse"], "ding", 0.45),
           (T["sinal"] - 0.05, "whoosh", 0.45), (T["dor1"], "pop", 0.45),
           (T["atividade"], "pop", 0.55), (T["atividade"] + 0.05, "whoosh", 0.35),
           (T["repouso"], "pop", 0.55), (T["repouso"] + 0.05, "whoosh", 0.3),
           (T["dor2"], "whoosh", 0.25), (T["ponto"], "ping", 0.6), (T["ponto"] + 0.05, "pop", 0.35),
           (desce2(T), "whoosh", 0.22), (T["treino2"] + 0.02, "ping", 0.5), (T["treino2"], "whoosh", 0.25),
           (T["avaliacao"] - 0.08, "whoosh", 0.45), (T["avaliacao"] + 0.3, "ding", 0.5),
           (T["dor3"] - 0.1, "whoosh", 0.4), (T["aviso"] - 0.1, "whoosh", 0.35), (T["aviso"] + 0.3, "thump", 0.8),
           (T["aviso"] + 0.35, "ping", 0.45)]
    d0, d1, s0, s1 = tempos_trofeu(T)
    ev += [(d0, "whoosh", 0.4), (d1, "click", 0.65), (d1 + 0.2, "click", 0.4), (s0 + 0.05, "whoosh", 0.5),
           (troca(T), "whoosh", 0.55)]
    for (e0, e1), (p0, p1) in tempos_escada(T):
        ev.append((p1 - 0.02, "click", 0.55))
    ev += [(T["descanso"] + 0.2, "pop", 0.6), (T["previne"], "ding", 0.45), (T["aumentar"] + 0.35, "pop", 0.4),
           (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def tempos_previa(T):
    return [0.0, T["trincar"] + 0.4, T["queda"] + 0.55, T["repetitivo"] + 1.0, T["unica"] + 0.3,
            T["estresse"] + 0.6, T["repouso"] + 0.5, T["ponto"] + 0.3, T["avaliacao"] + 0.7,
            T["trofeu"] + 0.15, T["descanso"] + 0.7, T["manda"] + 1.6]


# respiro antes da CTA: a escada completa (com o patamar DESCANSO) fica na tela para ser lida.
render = fazer_render(quadro, ANCORAS, sons, tempos_previa, respiro_cta=2.0)
