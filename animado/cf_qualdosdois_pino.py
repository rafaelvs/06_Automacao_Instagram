# -*- coding: utf-8 -*-
"""QUAL DOS DOIS? — vermelho no pino (série-jogo; 2º episódio, ter 24/11/2026 15h). v2: correções da revisão.

Mesma mecânica do piloto cf_qualdosdois_pe_chato (aprovado: "conferido, segue"): o espectador DÁ UM
PALPITE antes da resposta, em DUAS rodadas e um BÔNUS. Muda só o objeto: em vez das solas no piso,
nos dois cartões está a MESMA perna de perfil com o fixador monolateral (barra + 3 pinos), e a
diferença mora na pele em volta do pino do MEIO.

  * Rodada 1 (resposta A, OURO + ding): "Vermelho no pino: qual é o comum?" — o gancho falado é o
    próprio gancho da tela e FICA durante a contagem. A = mancha rosada PEQUENA e PARADA em volta do
    pino; B = mancha vermelha GRANDE que respira e solta ondas finas. Contagem de 2 s (anel 2-1 ENTRE
    OS PÉS, tique-taque, luz A, B, A, B que apaga no fim), revelação: "A! Reação leve na pele é
    comum." A mancha de A ganha um contorno branco e "assenta". "Vermelhidão que CRESCE, como na B":
    a mancha de B cresce à vista (sempre recortada pela perna); no "avise" a marca LARANJA se fecha
    em volta de B e o fone entra (toca até o "equipe"); a pílula só vira "RODADA 2" quando a rodada 1
    já saiu (o fone nunca aparece sob "RODADA 2").
  * Rodada 2 (resposta B, LARANJA + fone, sem ding) — v2, "mais difícil" DE VERDADE: A parece PIOR e
    é o comum (o mesmo pontinho rosado + uma gotinha TRANSPARENTE de secreção clara, azulada e
    translúcida); B = pele LIMPA e uma estrela de dor PEQUENA (a do piloto, só vermelha), NA PELE,
    afastada do metal, com um anel branco fino que lateja. "qual pede avisar sua equipe?" fica escrita
    na contagem. "B! Dor NOVA no pino: avise cedo." — no "dor" a estrela cresce; no "nova" ela some
    0,25 s e VOLTA maior com um anel que se expande da pele; no "avise" o fone entra e toca. "Pouca
    secreção clara é comum." — A volta a 100 %, a gotinha ganha contorno branco e, no "comum", A
    ganha a marca OURO (tranquiliza) enquanto B apaga um pouco.
  * BÔNUS: cartão C no centro, mesma perna e pele neutra. "pus" = gota de desenho OPACA amarelo-pus
    (sem escorrer, bem diferente da gotinha clara de A); "mau cheiro" = três linhas onduladas que
    nascem NA entrada do pino e sobem para o vão escuro entre a canela e a barra; "Avise também" = a
    MESMA marca laranja e o MESMO fone do B; "Com febre" = o fone para, o cartão C apaga para ~60 % e
    o termômetro entra fora do cartão; "pronto-socorro" = o termômetro cresce +25 % com anéis
    vermelhos pulsando (sem prédio, sirene ou ambulância).
  * CTA: os cartões A e B da rodada 1 voltam em miniatura acima da frase e balançam no "pinos".
Ouro + ding SÓ na resposta que tranquiliza; LARANJA + fone para TUDO o que pede avisar a equipe. A
opção que não é a resposta só apaga para 45%: nunca X, nunca vermelho de "errado", nunca deboche.
Rosa/vermelho só na pele em volta do pino e na estrela de dor; nada de sangue, ferida, crosta,
buraco escuro, brilho molhado ou pus escorrendo. Os pinos entram em 3/4 (62 px PARA DENTRO do
contorno da canela) para a mancha aparecer inteira em volta deles (no perfil puro ela virava
meia-lua na borda e a de A sumia na miniatura: maquete v1).

Render próprio (como o piloto): a contagem é SILÊNCIO inserido no áudio depois do `comprimir()` (que
corta qualquer pausa > 0,42 s do roteiro), o karaokê muda na contagem e a trilha cai para ~15% nela.
Âncoras das letras por TOKEN ('A?', 'B?', 'A!', 'B!', 'B:'); sem exatamente 2 'B?' seguidos da
resposta, o render aborta.

Peças por IMPORT: fundo, paleta, texto, porca (cf_alongamento), comprimir/alinhar/blocos
(cf_fratura_cola), legenda + identificação CFM + cartão final (cf_comum). CÓPIAS (para este vídeo não
depender do hash dessas cenas): do cf_qualdosdois_pe_chato as peças do jogo (âncoras por token,
contagem, luz, anel, selo da letra, pílula, selo da série, brilhos, estrela de dor, mixagem); do
cf_mitonaprova_pinos a perna, a geometria do fixador (barra, pinos, presilhas SEM número), o fone e o
termômetro. Todo texto desenhado está em ep["tela"], no gancho, no roteiro (karaokê) ou na interface.
"""
import math
import os

import numpy as np
import skia

from . import som, voz as _voz
from .base import codificar, previas as _previas
from .cf_alongamento import (ACO, ACO_ESC, ACO_HL, BG_OUT, CX, F_BLACK, OURO, PELE, VERMELHO, W, C, clamp,
                             e_back, e_inout, e_out, fundo, lerp, paint, porca, prog, texto)
from .cf_comum import interface, legenda
from .cf_fratura_cola import alinhar, comprimir, montar_blocos

# ------------------------------------------------------------------ roteiro -> tempos
ANCORAS = {
    "vermelho": ("vermelho", 1), "pino1": ("pino", 1), "comum1": ("comum", 1), "chuta": ("chuta", 1),
    "a1": ("tok:A?", 1), "b1": ("tok:B?", 1), "resp1": ("tok:A!", 1), "reacao": ("reação", 1),
    "leve": ("leve", 1), "comum2": ("comum", 2), "vermelhidao": ("vermelhidão", 1),
    "cresce": ("cresce", 1), "na_b": ("tok:B:", 1), "avise1": ("avise", 1), "equipe1": ("equipe", 1),
    "rodada": ("agora", 1), "dificil": ("difícil", 1), "qual2": ("qual", 2), "avisar": ("avisar", 1),
    "equipe2": ("equipe", 2), "a2": ("tok:A?", 2), "b2": ("tok:B?", 2), "resp2": ("tok:B!", 1),
    "dor": ("dor", 1), "nova": ("nova", 1), "pino2": ("pino", 2), "avise2": ("avise", 2), "cedo": ("cedo", 1),
    "secrecao": ("secreção", 1), "clara": ("clara", 1), "comum3": ("comum", 3),
    "bonus": ("bônus", 1), "pus": ("pus", 1), "cheiro": ("cheiro", 1), "avise3": ("avise", 3),
    "tambem": ("também", 1), "febre": ("febre", 1), "socorro": ("pronto-socorro", 1), "manda": ("manda", 1),
    "pinos": ("pinos", 1),
}
DESTAQUE = {"vermelho", "comum", "leve", "vermelhidão", "cresce", "avise", "equipe", "difícil", "dor",
            "nova", "secreção", "clara", "pus", "cheiro", "febre", "pronto-socorro"}
CONTAGEM = 2.0                     # segundos de palpite (silêncio inserido depois de cada "B?")
RESPOSTAS = ("A!", "A,", "B!", "B,")


def ancoras_jogo(pal, mapa):
    """(cópia do piloto) {chave: tempo}. 'tok:X' compara o TOKEN do roteiro (com pontuação); o resto,
    a palavra em minúscula. Âncora ausente = KeyError (vídeo dessincronizado não sai)."""
    T = {}
    for chave, (alvo, n) in mapa.items():
        c = 0
        for p in pal:
            ok = p["tok"] == alvo[4:] if alvo.startswith("tok:") else p["w"].lower() == alvo
            if ok:
                c += 1
                if c == n:
                    T[chave] = p["t"]; break
        else:
            raise KeyError(f"âncora não achada no roteiro: {alvo} #{n}")
    T["fim_fala"] = pal[-1]["t"] + pal[-1]["d"]
    T["total"] = T["fim_fala"] + 2.2
    return T


def inserir_contagens(voz, pal, dur=CONTAGEM):
    """(cópia do piloto) Insere `dur` s de silêncio logo depois de cada token 'B?' (no áudio JÁ
    comprimido) e empurra o tempo das palavras seguintes. -> (voz, pal, [início de cada contagem])."""
    idx = [i for i, p in enumerate(pal) if p["tok"] == "B?"]
    if len(idx) != 2:
        raise SystemExit(f"ERRO: o jogo precisa de exatamente 2 'B?' no roteiro (achei {len(idx)}).")
    for i in idx:
        if i + 1 >= len(pal) or pal[i + 1]["tok"] not in RESPOSTAS:
            raise SystemExit("ERRO: depois de cada 'B?' vem a resposta ('A!'/'A,' ou 'B!'/'B,') — roteiro fora do jogo.")
    ins = [pal[i]["t"] + pal[i]["d"] + 0.05 for i in idx]
    partes, ult = [], 0.0
    for x in ins:
        partes.append(voz[int(ult * som.SR):int(x * som.SR)]); partes.append(np.zeros(int(dur * som.SR), voz.dtype))
        ult = x
    partes.append(voz[int(ult * som.SR):])
    novas = [dict(p, t=p["t"] + dur * sum(1 for x in ins if p["t"] > x)) for p in pal]
    return np.concatenate(partes), novas, [ins[0], ins[1] + dur]


# ------------------------------------------------------------------ paleta e geometria do jogo
COR_A, COR_B = "#4FA3E0", "#F08A4B"
FUNDO_CARTAO = "#0B1824"
CART_A = (36, 392, 528, 1230)
CART_B = (552, 392, 1044, 1230)
CART_C = (290, 392, 790, 1230)     # o cartão do BÔNUS, no centro
# pele: os tons do cf_mitonaprova_pinos (copiados)
PELE_CL, PELE_ESC, PELE_LINHA = "#F8D0BC", "#DC9A7E", "#C4866B"
# a pele em volta do pino (só aqui entra rosa/vermelho, além da estrela de dor)
ROSA_LEVE = "#E8706E"                             # A: reação leve, pequena e parada
VERM_NUCLEO, VERM_MEIO, VERM_ONDA = "#D93A44", "#E8606A", "#EC7A78"   # B: vermelhidão que cresce
GOTA, GOTA_BORDA, GOTA_BRILHO = "#E0D266", "#8F8530", "#FFF8D0"       # bônus: gota OPACA amarelo-pus
CLARA, CLARA_BORDA = "#D8EEFA", "#5E9CC4"         # rodada 2, A: gotinha TRANSPARENTE de secreção clara
CHEIRO = "#B4C79A"                                # bônus: linhas de cheiro, verde-acinzentadas
R_DOR = (44, 54, 68)                              # estrela de dor de B: pergunta, "dor", "nova"
DX_DOR, DY_DOR = -74, -38                         # ... NA PELE, acima e à esquerda da entrada (longe do metal)
R_MANCHA, R_CRESCE = 185, 235                     # raio da mancha de B antes e depois do "cresce"

# geometria do fixador (cópia do cf_mitonaprova_pinos; coordenadas LOCAIS da perna)
PY = (250, 420, 590)                              # altura dos 3 pinos (local)
PIN_R = 23                                        # meia espessura do pino
BAR_X, BAR_W, BAR_Y0, BAR_Y1 = 215, 32, 160, 670
CLAMP_W, CLAMP_H = 70, 62
PIN_X1 = 266                                      # ponta de fora do pino (além da presilha)
_SHIN = [(-20, 104), (40, 104), (150, 99), (250, 92), (300, 88), (420, 81), (590, 73), (668, 70)]
DENTRO = 62                                       # o pino entra 62 px PARA DENTRO do contorno (vista 3/4)
FOCO = 1                                          # o pino do MEIO é o da diferença
Y_FOCO = 811                                      # ... na altura do centro do cartão (e do anel)
CAIXA = (-200, -30, 340, 850)                     # caixa local da perna + fixador (imagens prontas)
LINEAR = skia.SamplingOptions(skia.FilterMode.kLinear)


def _a(x):
    """Alfa 0..255 (nunca estoura)."""
    return int(max(0, min(255, x)))


def _alfa(a):
    p = skia.Paint(); p.setAlphaf(clamp(a)); return p


def _rr(r, raio=30):
    return skia.RRect.MakeRectXY(skia.Rect(*r), raio, raio)


def _centro(r):
    return (r[0] + r[2]) / 2, (r[1] + r[3]) / 2


def shin_x(y):
    """x (local) da pele da canela na altura y (cópia do cf_mitonaprova_pinos)."""
    for (y0, x0), (y1, x1) in zip(_SHIN, _SHIN[1:]):
        if y0 <= y <= y1:
            return lerp(x0, x1, (y - y0) / (y1 - y0))
    return _SHIN[-1][1]


def entrada(i):
    """Ponto (local) onde o pino i entra na pele, já DENTRO do contorno (vista 3/4)."""
    return shin_x(PY[i]) - DENTRO, PY[i]


def origem(r):
    """Translação da perna dentro do cartão r: o pino do meio fica em y = Y_FOCO."""
    cx = (r[0] + r[2]) / 2
    return cx - 66, Y_FOCO - PY[FOCO]


def bump(t, t0, dur=0.35):
    """0 -> 1 -> 0 em `dur` s a partir de t0 (pulso)."""
    return math.sin(math.pi * clamp((t - t0) / dur)) if t >= t0 else 0.0


def flash(t, t0, dur=0.75):
    """Acende rápido em t0 (0,12 s) e apaga devagar até t0 + dur."""
    if t < t0:
        return 0.0
    return e_out(clamp((t - t0) / 0.12)) * (1 - prog(t, t0 + 0.25, t0 + dur))


def balanco(t, t0, amp=1.5, dur=1.0):
    """Balanço curto (graus) que amortece: o 'qual dos dois?' de quem pergunta."""
    k = t - t0
    if k < 0 or k > dur:
        return 0.0
    return amp * math.sin(2 * math.pi * k / 0.5) * (1 - k / dur)


def pop_in(t, t0, dur=0.3):
    """0 -> 1 com e_back (entrada com pulo)."""
    return e_back(clamp((t - t0) / dur)) if t >= t0 else 0.0


# ------------------------------------------------------------------ a perna (cópia do cf_mitonaprova_pinos)
def _perna_path():
    """Perna em pé, vista de lado (pé para a direita): panturrilha abaulada atrás, canela quase reta
    na frente, tornozelo, calcanhar e pé com os dedos — o contorno que o leigo lê como "perna"."""
    p = skia.Path()
    p.moveTo(-110, -12)
    p.cubicTo(-120, 60, -152, 120, -150, 205)                 # panturrilha
    p.cubicTo(-148, 330, -86, 470, -66, 600)                  # afina até o tendão
    p.cubicTo(-60, 650, -64, 690, -72, 712)
    p.cubicTo(-94, 742, -98, 800, -58, 808)                   # calcanhar
    p.lineTo(228, 812)                                        # planta
    p.cubicTo(262, 812, 284, 792, 274, 772)                   # ponta dos dedos
    p.cubicTo(262, 756, 226, 750, 192, 742)                   # dorso dos dedos
    p.cubicTo(140, 726, 90, 702, 70, 668)                     # peito do pé subindo ao tornozelo
    p.cubicTo(60, 560, 82, 420, 88, 300)                      # canela
    p.cubicTo(94, 200, 112, 110, 104, 40)                     # tuberosidade e joelho
    p.cubicTo(100, 20, 98, 0, 96, -12)
    p.close()
    return p


PERNA = _perna_path()


def perna(cv):
    """Pele OPACA com sombreado cilíndrico; o topo some no cartão por máscara (é um recorte)."""
    caixa = skia.Rect(-200, -20, 330, 840)
    cv.saveLayer(caixa, None)
    cv.drawOval(skia.Rect(-120, 796, 300, 830), paint("#6B4A2A", 80, blur=10))    # sombra no chão
    cv.drawPath(PERNA, paint(PELE, 255, shader=skia.GradientShader.MakeLinear(
        [skia.Point(-152, 0), skia.Point(112, 0)],
        [C(PELE_ESC), C("#E6A387"), C(PELE), C(PELE_CL), C(PELE), C("#E2A084")],
        [0.0, 0.18, 0.42, 0.62, 0.84, 1.0])))
    cv.save(); cv.clipPath(PERNA, skia.ClipOp.kIntersect, True)                    # pé: sombra no sentido dele
    cv.drawRect(skia.Rect(-110, 690, 300, 820), paint(PELE, 255, shader=skia.GradientShader.MakeLinear(
        [skia.Point(0, 700), skia.Point(0, 815)], [C(PELE, 0), C(PELE_CL, 150), C(PELE, 200), C(PELE_ESC, 255)],
        [0.0, 0.35, 0.65, 1.0])))
    cv.drawOval(skia.Rect(-26, 632, 14, 678), paint(PELE_ESC, 90, blur=6))        # tornozelo (maléolo)
    cv.drawOval(skia.Rect(-20, 636, 6, 660), paint("#FFFFFF", 60, blur=4))
    cv.restore()
    cv.drawLine(30, 130, 18, 610, paint("#FFFFFF", 70, "stroke", 14, blur=8))     # reflexo da canela
    for dx, dy in ((252, 778), (236, 772), (220, 768)):                             # dedos
        cv.drawArc(skia.Rect(dx - 10, dy - 6, dx + 10, dy + 14), 250, 120, False, paint(PELE_LINHA, 150, "stroke", 2))
    cv.drawPath(PERNA, paint(PELE_LINHA, 220, "stroke", 2.5))
    masc = skia.Paint(AntiAlias=True)
    masc.setShader(skia.GradientShader.MakeLinear([skia.Point(0, -12), skia.Point(0, 110)],
                                                  [skia.ColorSetARGB(0, 0, 0, 0), skia.ColorSetARGB(255, 0, 0, 0)]))
    masc.setBlendMode(skia.BlendMode.kDstIn)
    cv.drawRect(caixa, masc)
    cv.restore()


# ------------------------------------------------------------------ fixador (barra + 3 pinos em 3/4)
def barra(cv):
    r = skia.Rect(BAR_X - BAR_W / 2, BAR_Y0, BAR_X + BAR_W / 2, BAR_Y1)
    cv.drawRRect(skia.RRect.MakeRectXY(r.makeOffset(6, 6), 14, 14), paint("#000000", 60, blur=8))
    cv.drawRRect(skia.RRect.MakeRectXY(r, 14, 14), paint(ACO, 255, shader=skia.GradientShader.MakeLinear(
        [skia.Point(r.left(), 0), skia.Point(r.right(), 0)], [C(ACO_ESC), C(ACO_HL), C(ACO), C(ACO_ESC)],
        [0.0, 0.3, 0.6, 1.0])))
    cv.drawRRect(skia.RRect.MakeRectXY(r, 14, 14), paint(ACO_ESC, 255, "stroke", 2))


def pino_3q(cv, i):
    """Pino em 3/4: sai de DENTRO do contorno da perna; a pele "abraça" a entrada (colar em tom de
    pele, sem buraco escuro, sem crosta, sem secreção). Sombra leve na pele."""
    x, y = entrada(i); r = PIN_R
    cv.drawOval(skia.Rect(x - 4, y - r + 6, PIN_X1, y + r + 14), paint("#6B3A2A", 60, blur=8))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, y - r), skia.Point(0, y + r)],
                                        [C(ACO_ESC), C(ACO_HL), C(ACO), C(ACO_ESC)], [0.0, 0.32, 0.62, 1.0])
    rr = skia.RRect.MakeRectXY(skia.Rect(x, y - r, PIN_X1, y + r), 10, 10)
    cv.drawRRect(rr, paint(ACO, 255, shader=sh)); cv.drawRRect(rr, paint(ACO_ESC, 210, "stroke", 1.8))
    cv.drawOval(skia.Rect(x - 12, y - r - 4, x + 12, y + r + 4), paint(PELE_LINHA, 200))
    cv.drawOval(skia.Rect(x - 6, y - r, x + 8, y + r), paint("#B87A60", 230))


def presilha(cv, i):
    """Presilha na barra com a porca (SEM número)."""
    y = PY[i]
    rc = skia.Rect(BAR_X - CLAMP_W / 2, y - CLAMP_H / 2, BAR_X + CLAMP_W / 2, y + CLAMP_H / 2)
    cv.drawRRect(skia.RRect.MakeRectXY(rc, 10, 10), paint("#4A5A6C", 255, shader=skia.GradientShader.MakeLinear(
        [skia.Point(rc.left(), 0), skia.Point(rc.right(), 0)], [C("#4A5A6C"), C("#8FA3B8"), C("#4A5A6C")])))
    cv.drawRRect(skia.RRect.MakeRectXY(rc, 10, 10), paint("#2E3A47", 255, "stroke", 2))
    cv.save(); cv.translate(BAR_X, y); cv.scale(1.5, 1.5)
    porca(cv, 0, 0, 0, 1.0)
    cv.restore()


def fixador(cv):
    barra(cv)
    for i in range(3):
        pino_3q(cv, i)
        presilha(cv, i)


def reflexo_pino(cv, i, k):
    """Brilho especular SUAVE correndo pelo trecho visível do pino (da pele até a presilha); k de 0 a 1.
    Faixa inclinada em degradê branco -> transparente, recortada pelo pino (v2: o retângulo branco
    sólido da v1 lia como esparadrapo/etiqueta colada no pino)."""
    if not 0 < k < 1:
        return
    x0, y = entrada(i); r = PIN_R
    xx = lerp(x0 + 26, BAR_X - CLAMP_W / 2 - 16, e_inout(k))
    a = _a(140 * math.sin(math.pi * k))
    sh = skia.GradientShader.MakeLinear([skia.Point(xx - 30, y - r), skia.Point(xx + 30, y + r)],
                                        [C("#FFFFFF", 0), C("#FFFFFF", a), C("#FFFFFF", 0)], [0.0, 0.5, 1.0])
    cv.save(); cv.clipRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y - r, PIN_X1, y + r), 10, 10), skia.ClipOp.kIntersect, True)
    cv.drawRect(skia.Rect(xx - 40, y - r, xx + 40, y + r), paint("#FFFFFF", 255, shader=sh))
    cv.restore()


# ------------------------------------------------------------------ imagens prontas (desenho parado)
_IMG = {}


def _imagem(nome):
    """Perna e fixador são desenhados uma vez (degradês, máscara, sombras) e copiados a cada quadro."""
    if nome not in _IMG:
        x0, y0, x1, y1 = CAIXA
        surf = skia.Surface(int(x1 - x0), int(y1 - y0))
        c = surf.getCanvas(); c.clear(skia.ColorTRANSPARENT); c.translate(-x0, -y0)
        (perna if nome == "perna" else fixador)(c)
        _IMG[nome] = surf.makeImageSnapshot()
    return _IMG[nome]


def _blit(cv, nome):
    cv.drawImage(_imagem(nome), CAIXA[0], CAIXA[1], LINEAR)


_BASES = {}


def base_cartao(cv, r):
    """Sombra + fundo escuro do cartão (imagem pronta para os retângulos fixos)."""
    if r not in _BASES:
        m = 60
        surf = skia.Surface(int(r[2] - r[0] + 2 * m), int(r[3] - r[1] + 2 * m))
        c = surf.getCanvas(); c.clear(skia.ColorTRANSPARENT); c.translate(m - r[0], m - r[1])
        c.drawRRect(_rr((r[0], r[1] + 12, r[2], r[3] + 12)), paint("#000000", 110, blur=20))
        c.drawRRect(_rr(r), paint(FUNDO_CARTAO, 230))
        _BASES[r] = (surf.makeImageSnapshot(), r[0] - m, r[1] - m)
    img, x, y = _BASES[r]
    cv.drawImage(img, x, y, LINEAR)


# ------------------------------------------------------------------ a pele em volta do pino do meio
def mancha_leve(cv, esc=1.0, contorno=0.0):
    """A: reação leve — mancha rosada PEQUENA e PARADA em volta da entrada do pino (local)."""
    x, y = entrada(FOCO)
    cv.save(); cv.clipPath(PERNA, skia.ClipOp.kIntersect, True)
    cv.translate(x, y); cv.scale(esc, esc)
    cv.drawOval(skia.Rect(-50, -46, 50, 46), paint(ROSA_LEVE, 120, blur=10))
    cv.drawOval(skia.Rect(-40, -37, 40, 37), paint(ROSA_LEVE, 150, blur=4))
    cv.restore()
    if contorno > 0:                                      # "é ESTA": contorno branco que pulsa
        e = esc * (1 + 0.10 * contorno)
        cv.save(); cv.translate(x, y); cv.scale(e, e)
        cv.drawOval(skia.Rect(-56, -52, 56, 52), paint("#FFFFFF", _a(90 * contorno), "stroke", 9, blur=5))
        cv.drawOval(skia.Rect(-56, -52, 56, 52), paint("#FFFFFF", _a(255 * contorno), "stroke", 3))
        cv.restore()


def mancha_grande(cv, raio, ondas=()):
    """B: vermelhidão GRANDE em volta do pino, recortada pelo contorno da perna (nunca vaza para o
    fundo; o metal vem por cima). `ondas`: [(raio, força)] anéis finos que saem da mancha."""
    x, y = entrada(FOCO)
    cv.save(); cv.clipPath(PERNA, skia.ClipOp.kIntersect, True)
    sh = skia.GradientShader.MakeRadial(skia.Point(x, y), raio,
                                        [C(VERM_NUCLEO, 225), C(VERM_MEIO, 150), C(VERM_MEIO, 0)], [0.0, 0.55, 1.0])
    cv.drawCircle(x, y, raio, paint(VERM_NUCLEO, 255, shader=sh))
    for rr, f in ondas:
        if f > 0:
            cv.drawCircle(x, y, rr, paint(VERM_ONDA, _a(200 * f), "stroke", 5))
    cv.restore()


def ondas_b(t, raio, extras):
    """Uma onda a cada 1,1 s (já visível no quadro 0) + ondas extras disparadas em `extras`."""
    f = ((t + 0.4) % 1.1) / 1.1
    out = [(raio * (0.85 + 0.5 * f), 0.75 * math.sin(math.pi * f))]
    for t0 in extras:
        k = (t - t0) / 0.75
        if 0 <= k <= 1:
            out.append((raio * (1.0 + 0.5 * e_out(k)), 1.0 - k))
    return out


def estrela_dor(cv, x, y, r, a):
    """Cópia do helper do piloto (que copiou do cf_pe_virado, aprovado)."""
    if a <= 0:
        return
    p = skia.Path(); n = 9
    for i in range(2 * n):
        ang = -math.pi / 2 + i * math.pi / n
        rr = (r if i % 4 == 0 else r * 0.84) if i % 2 == 0 else r * 0.46
        (p.moveTo if i == 0 else p.lineTo)(x + rr * math.cos(ang), y + rr * math.sin(ang))
    p.close()
    cv.drawPath(p, paint(VERMELHO, _a(120 * a), blur=12))
    cv.drawPath(p, paint(VERMELHO, _a(255 * a)))
    cv.drawPath(p, paint("#FFD3D4", _a(200 * a), "stroke", 2.5))


def dor_na_pele(cv, t, T, r, lateja=1.0):
    """B da rodada 2: a estrela de dor do piloto (só vermelha) NA PELE, acima e à esquerda da entrada
    do pino — longe do metal, para não ler como faísca/curto no pino. Anéis BRANCOS finos latejam
    em volta dela (recortados pela perna: dor = latejar; o vermelho que se espalha da rodada 1 usa
    anéis rosados, não brancos). No 'nova', um anel maior se expande a partir da pele."""
    x, y = entrada(FOCO)
    cx, cy = x + DX_DOR, y + DY_DOR
    cv.save(); cv.clipPath(PERNA, skia.ClipOp.kIntersect, True)
    if lateja > 0 and r > 0:
        for i in range(2):
            f = ((t * 0.9) + i * 0.5) % 1.0
            cv.drawCircle(cx, cy, r * (1.0 + 0.9 * f), paint("#FFFFFF", _a(170 * lateja * math.sin(math.pi * f)), "stroke", 3.5))
    k = (t - T["nova"] - 0.15) / 0.6                   # = quando a estrela VOLTA (raio_dor)
    if 0 <= k <= 1:
        cv.drawCircle(cx, cy, lerp(30, 190, e_out(k)), paint("#FFFFFF", _a(230 * (1 - k)), "stroke", 6))
    cv.restore()
    estrela_dor(cv, cx, cy, r, 1.0 if r > 0 else 0.0)


def gota(cv, x, y, esc, a, cor=GOTA, borda=GOTA_BORDA, brilho=GOTA_BRILHO, opaca=1.0):
    """Gota de desenho (~48 x 68 px), sem rastro, sem escorrer. Padrão: OPACA amarelo-pus (bônus);
    `opaca` < 1 + cores claras = a gotinha TRANSPARENTE de secreção clara (rodada 2, A)."""
    if a <= 0 or esc <= 0:
        return
    s = 0.62
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    g = skia.Path()
    g.moveTo(0, -56 * s); g.cubicTo(18 * s, -30 * s, 38 * s, -8 * s, 38 * s, 14 * s)
    g.cubicTo(38 * s, 38 * s, 20 * s, 54 * s, 0, 54 * s)
    g.cubicTo(-20 * s, 54 * s, -38 * s, 38 * s, -38 * s, 14 * s)
    g.cubicTo(-38 * s, -8 * s, -18 * s, -30 * s, 0, -56 * s); g.close()
    cv.drawPath(g, paint(cor, _a(255 * a * opaca))); cv.drawPath(g, paint(borda, _a(255 * a), "stroke", 3))
    cv.drawArc(skia.Rect(-14, 0, 0, 22), 120, 80, False, paint(brilho, _a(230 * a), "stroke", 4))
    if opaca < 1:                                        # brilho de cima: "água", não pus
        cv.drawCircle(-8, -4, 4.5, paint("#FFFFFF", _a(230 * a)))
    cv.restore()


def gota_clara(cv, esc, a, contorno=0.0):
    """A da rodada 2: POUCA secreção clara — gotinha translúcida azulada logo abaixo da entrada do pino
    (no mesmo lugar da gota de pus do bônus, para a diferença ser só 'clara x pus')."""
    x, y = entrada(FOCO)
    gota(cv, x - 6, y + 52, 1.0 * esc, a, cor=CLARA, borda=CLARA_BORDA, brilho="#FFFFFF", opaca=0.55)
    if contorno > 0:
        cv.drawCircle(x - 6, y + 54, 38 * esc * (1 + 0.1 * contorno), paint("#FFFFFF", _a(255 * contorno), "stroke", 3))


def linhas_cheiro(cv, t, t0, a):
    """Três linhas onduladas (o "cheiro" de desenho animado) que NASCEM na entrada do pino do meio
    (em cima do pino, onde ele encontra a pele) e sobem para a direita, para o vão ESCURO entre a
    canela e a barra, sem chegar ao pino de cima. Fora da pele, não leem como veia nem como pelo."""
    if a <= 0 or t < t0:
        return
    x, y = entrada(FOCO)
    cresce = e_out(clamp((t - t0) / 0.4))
    teto = PY[0] + PIN_R + 14                             # não encosta no pino de cima
    for i in range(3):
        x0, y0 = x + 18 + 32 * i, y - PIN_R - 6
        comp = (y0 - teto - 6 * (i % 2)) * cresce
        p = skia.Path()
        n = 18
        for j in range(n + 1):
            u = j / n
            yy = y0 - comp * u
            xx = x0 + 34 * u + 9 * math.sin(2 * math.pi * (1.4 * u) - t * 7 + i * 1.1)
            (p.moveTo if j == 0 else p.lineTo)(xx, yy)
        fim = y0 - comp - 1
        for cor, w, alfa in ((FUNDO_CARTAO, 12, 0.5), (CHEIRO, 7, 0.95)):
            sh = skia.GradientShader.MakeLinear([skia.Point(0, y0), skia.Point(0, fim)],
                                                [C(cor, _a(255 * alfa * a)), C(cor, _a(255 * alfa * a)), C(cor, 0)],
                                                [0.0, 0.6, 1.0])
            cv.drawPath(p, paint(cor, 255, "stroke", w, shader=sh))


# ------------------------------------------------------------------ fone e termômetro (cópias do mito)
def telefone(cv, x, y, a, toque, t, cor="#FFFFFF", esc=1.25):
    """Fone genérico (cópia do cf_mitonaprova_pinos / cf_dor_alongamento), sem logotipo de aplicativo."""
    if a <= 0 or esc <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc); cv.rotate(-28 + 9 * math.sin(t * 46) * toque)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-24, -42, 4, -22), 8, 8), paint(cor, _a(255 * a)))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-24, 22, 4, 42), 8, 8), paint(cor, _a(255 * a)))
    p = skia.Path(); p.moveTo(-14, -30); p.quadTo(-40, 0, -14, 30)
    cv.drawPath(p, paint(cor, _a(255 * a), "stroke", 14))
    cv.restore()
    if toque > 0:
        for i in range(2):
            f = ((t * 1.8) + i * 0.5) % 1.0
            r = 30 + 22 * f
            cv.drawArc(skia.Rect(x - r + 14, y - r, x + r + 14, y + r), -40, 80, False,
                       paint(OURO, _a(255 * a * toque * (1 - f)), "stroke", 4))


def termometro(cv, x, y, nivel, a, esc=1.0):
    """Termômetro simples, sem número (cópia do cf_mitonaprova_pinos / cf_dor_alongamento)."""
    if a <= 0 or esc <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-12, -48, 12, 24), 12, 12), paint("#FFFFFF", _a(255 * a)))
    cv.drawCircle(0, 32, 19, paint("#FFFFFF", _a(255 * a)))
    cv.drawCircle(0, 32, 12, paint("#D64045", _a(255 * a)))
    h = lerp(6, 64, clamp(nivel))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-5, 26 - h, 5, 32), 5, 5), paint("#D64045", _a(255 * a)))
    cv.restore()


def fone_no_cartao(r):
    """Canto de cima à direita do cartão: espaço livre acima da barra do fixador (os arcos do toque
    ficam dentro da borda)."""
    return r[2] - 80, r[1] + 72


# ------------------------------------------------------------------ cartão A | B | C
def selo_letra(cv, letra, x, y, cor, esc=1.0, a=1.0, badge_esc=1.0):
    if a <= 0:
        return
    r = 44 * badge_esc
    x, y = x + r - 44, y + r - 44                         # o selo cresce para dentro do cartão
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    cv.drawCircle(0, 5, r, paint("#000000", _a(90 * a), blur=8))
    cv.drawCircle(0, 0, r, paint(cor, _a(255 * a)))
    cv.drawCircle(0, 0, r - 3, paint("#FFFFFF", _a(70 * a), "stroke", 3))
    tam = 64 * badge_esc
    texto(cv, letra, 0, tam * 0.355, F_BLACK, tam, FUNDO_CARTAO, _a(255 * a))
    cv.restore()


def cartao(cv, t, r, letra, cor, pele=None, sobre=None, alfa=1.0, dx=0.0, dy=0.0, rot=0.0, esc=1.0,
           pulso=0.0, acende=0.0, luz=0.0, marca=None, marca_a=0.0, marca_brilho=0.0, badge_esc=1.0,
           por_cima=None):
    """Cartão com a perna + fixador e o selo da letra (`letra=None`: sem selo). `pele(cv)` desenha
    em coordenadas LOCAIS da perna entre a pele e o metal (a mancha); `sobre(cv)`, local, por cima do
    metal (reflexo, estrela); `por_cima(cv)`, no cartão, depois da borda (o fone). `luz` = luz da
    contagem (branca); `marca` = marcador da revelação (OURO na resposta que tranquiliza; a cor do B
    em tudo o que pede avisar a equipe)."""
    if alfa <= 0:
        return
    cx, cy = _centro(r)
    cv.saveLayer(None, _alfa(alfa)) if alfa < 1 else cv.save()
    cv.translate(dx, dy)
    cv.translate(cx, cy); cv.rotate(rot); cv.scale(esc, esc); cv.translate(-cx, -cy)
    rr = _rr(r)
    base_cartao(cv, r)
    cv.save(); cv.clipRRect(rr, skia.ClipOp.kIntersect, True)
    ox, oy = origem(r)
    cv.translate(ox, oy)
    _blit(cv, "perna")
    if pele:
        pele(cv)
    _blit(cv, "fixador")
    if sobre:
        sobre(cv)
    cv.restore()
    cv.drawRRect(rr, paint(cor, 255, "stroke", 3))
    if acende > 0:
        cv.drawRRect(rr, paint("#FFFFFF", _a(200 * clamp(acende)), "stroke", 5))
    if luz > 0:
        cv.drawRRect(rr, paint("#FFFFFF", _a(150 * luz), "stroke", 26, blur=14))
        cv.drawRRect(rr, paint("#FFFFFF", _a(255 * luz), "stroke", 8))
    if marca and marca_a > 0:
        cv.drawRRect(rr, paint(marca, _a(170 * marca_a), "stroke", 30, blur=16))
        cv.drawRRect(rr, paint(marca, _a(255 * marca_a), "stroke", 9))
        if marca_brilho > 0:
            cv.drawRRect(rr, paint(marca, _a(200 * marca_brilho * marca_a), "stroke", 48, blur=24))
            cv.drawRRect(rr, paint("#FFFFFF", _a(150 * marca_brilho * marca_a), "stroke", 4))
    if por_cima:
        por_cima(cv)
    if letra:
        selo_letra(cv, letra, r[0] + 62, r[1] + 62, cor, 1.0 + 0.35 * pulso, 1.0, badge_esc)
    cv.restore()


def marca_fecha(cv, r, fecha, a=1.0, dx=0.0, dy=0.0, esc=1.0):
    """A marca laranja FECHA: um contorno que encolhe de 1,14 até a borda do cartão."""
    if not 0 < fecha < 1:
        return
    cx, cy = _centro(r)
    g = lerp(1.14, 1.0, e_out(fecha)) * esc
    cv.save(); cv.translate(dx, dy); cv.translate(cx, cy); cv.scale(g, g); cv.translate(-cx, -cy)
    cv.drawRRect(_rr(r), paint(COR_B, _a(220 * a * (1 - fecha)), "stroke", 9))
    cv.restore()


# ------------------------------------------------------------------ contagem e luz (cópias do piloto)
def em_contagem(t, T, rodada=None):
    r1 = T["cont1"] <= t < T["resp1"] - 0.12
    r2 = T["cont2"] <= t < T["resp2"] - 0.12
    return r1 if rodada == 1 else r2 if rodada == 2 else (r1 or r2)


def luz_de(t, T, letra):
    """Luz da contagem: alterna a cada 0,5 s (ritmo constante) e APAGA nos últimos 0,2 s.
    Rodada 1: A, B, A, B; rodada 2: B, A, B, A — nas duas a luz termina na opção que NÃO é a
    resposta, e a revelação nunca se confunde com a luz que parou."""
    for i, t0 in enumerate((T["cont1"], T["cont2"])):
        k = t - t0
        if 0 <= k < CONTAGEM:
            fase = int(k / 0.5)
            ordem = ("A", "B") if i == 0 else ("B", "A")
            if ordem[fase % 2] != letra:
                return 0.0
            return clamp((k - fase * 0.5) / 0.05) * (1 - prog(k, CONTAGEM - 0.2, CONTAGEM - 0.05))
    return 0.0


def anel_contagem(cv, t, t0, x=540, y=1085, r=90):
    """(cópia do piloto) v2: ENTRE OS PÉS (y 1085), longe da presilha de A e da estrela de B."""
    k = t - t0
    if k < -0.05 or k > CONTAGEM + 0.22:
        return
    ent = e_back(clamp((k + 0.05) / 0.25))
    sai = clamp((k - CONTAGEM) / 0.22)
    esc = ent * lerp(1.0, 1.35, e_out(sai)); a = clamp((k + 0.05) / 0.08) * (1 - sai)
    cv.saveLayer(None, _alfa(a)) if a < 1 else cv.save()
    cv.translate(x, y); cv.scale(esc, esc)
    cv.drawCircle(0, 8, r + 6, paint("#000000", 120, blur=12))
    cv.drawCircle(0, 0, r, paint(FUNDO_CARTAO, 245))
    cv.drawCircle(0, 0, r - 12, paint("#FFFFFF", 38, "stroke", 12))
    resto = 1 - clamp(k / CONTAGEM)
    if resto > 0:
        cv.drawArc(skia.Rect(-(r - 12), -(r - 12), r - 12, r - 12), -90, 360 * resto, False, paint(OURO, 255, "stroke", 12))
    n = "2" if k < 1.0 else "1"
    pop = 1 + 0.25 * (1 - e_out(clamp((k - (0 if k < 1.0 else 1.0)) / 0.15)))
    cv.save(); cv.scale(pop, pop)
    texto(cv, n, 0, 44, F_BLACK, 120, "#FFFFFF", 255, contorno=0)
    cv.restore()
    cv.restore()


def brilhos_borda(cv, r, t, t0, n=20, dur=0.85):
    """Estrelinhas douradas saindo da borda do cartão (a revelação que tranquiliza comemora)."""
    k = t - t0
    if k < 0 or k > dur:
        return
    x0, y0, x1, y1 = r; lw, lh = x1 - x0, y1 - y0; per = 2 * (lw + lh)
    for i in range(n):
        d = (i + 0.5) / n * per
        if d < lw:
            px, py, nx, ny = x0 + d, y0, 0, -1
        elif d < lw + lh:
            px, py, nx, ny = x1, y0 + d - lw, 1, 0
        elif d < 2 * lw + lh:
            px, py, nx, ny = x1 - (d - lw - lh), y1, 0, 1
        else:
            px, py, nx, ny = x0, y1 - (d - 2 * lw - lh), -1, 0
        off = 40 * e_out(k / dur) * (0.6 + 0.4 * ((i * 37) % 10) / 10)
        x, y = px + nx * off, py + ny * off
        sz = 11 * (1 - k / dur) + 3; a = int(255 * (1 - k / dur))
        p = skia.Path(); p.moveTo(x, y - sz * 2); p.lineTo(x + sz * 0.5, y - sz * 0.5); p.lineTo(x + sz * 2, y)
        p.lineTo(x + sz * 0.5, y + sz * 0.5); p.lineTo(x, y + sz * 2); p.lineTo(x - sz * 0.5, y + sz * 0.5)
        p.lineTo(x - sz * 2, y); p.lineTo(x - sz * 0.5, y - sz * 0.5); p.close()
        cv.drawPath(p, paint(OURO, a))


def saida_final(t, T):
    """0 -> 1 em CRUZAMENTO com o cartão final (que entra em T['manda'] - 0,15 e escurece o fundo):
    v2 — a v1 apagava tudo antes e deixava ~0,4 s de tela quase vazia ('tempo morto'). Some por
    completo antes de as miniaturas da CTA entrarem (T['manda'] + 0,05)."""
    return prog(t, T["manda"] - 0.30, T["manda"] + 0.05)


# ------------------------------------------------------------------ estado de cada cartão
def raio_b1(t, T):
    """Raio da mancha de B na rodada 1: respira devagar (x0,97 -> 1,0 até a contagem), pulsa no
    'vermelho' e no 'vermelhidão' e CRESCE à vista no 'cresce' (185 -> 235)."""
    base = R_MANCHA * lerp(0.97, 1.0, prog(t, 0.2, T["cont1"])) * (1 + 0.012 * math.sin(2 * math.pi * t / 1.6))
    cresce = e_out(prog(t, T["cresce"], T["cresce"] + 0.6))
    base *= lerp(1.0, R_CRESCE / R_MANCHA, cresce)
    return base * (1 + 0.08 * bump(t, T["vermelho"], 0.4)) * (1 + 0.06 * bump(t, T["vermelhidao"], 0.4))


def pele_a(t, T, rodada):
    """A: a mancha pequena (as duas rodadas). Pulsa com o contorno branco quando A é dito/explicado.
    Rodada 2 (v2): + a gotinha TRANSPARENTE de secreção clara (A parece pior e é o comum); no
    'secreção clara' a gotinha pulsa com contorno branco."""
    if rodada == 1:
        esc = ((1 + 0.08 * bump(t, T["vermelho"], 0.4)) * (1 + 0.12 * bump(t, T["a1"], 0.35))
               * lerp(1.0, 0.92, e_out(prog(t, T["leve"], T["leve"] + 0.35))))
        cont = max(bump(t, T["a1"], 0.5), segura(t, T["reacao"], T["leve"] + 0.15))
        return lambda cv: mancha_leve(cv, esc, cont)
    esc = 1 + 0.12 * bump(t, T["a2"], 0.35)
    cont = bump(t, T["a2"], 0.5)
    g_esc = (1 + 0.12 * bump(t, T["a2"], 0.35)) * (1 + 0.22 * bump(t, T["clara"], 0.4))
    g_cont = segura(t, T["secrecao"], T["bonus"] - 0.1)

    def f(cv):
        mancha_leve(cv, esc, cont)
        gota_clara(cv, g_esc, 1.0, g_cont)
    return f


def segura(t, t0, ate, nivel=0.7):
    """Acende em t0 (pico 1), assenta em `nivel` e fica até `ate` (some em 0,3 s)."""
    if t < t0:
        return 0.0
    v = e_out(clamp((t - t0) / 0.12)) * lerp(1.0, nivel, prog(t, t0 + 0.3, t0 + 0.7))
    return v * (1 - prog(t, ate, ate + 0.3))


def reflexo_tres(t, t0):
    """'Pino': um brilho suave corre SÓ pelo pino do MEIO (v2: onde está a diferença; a v1 corria
    pelos 3 pinos dos dois cartões e virava 6 blocos brancos no segundo do gancho)."""
    def f(cv):
        reflexo_pino(cv, FOCO, (t - t0) / 0.7)
    return f


# ------------------------------------------------------------------ rodada 1
def rodada1(cv, t, T):
    sai = e_inout(prog(t, T["rodada"], T["rodada"] + 0.6))
    if sai >= 1:
        return
    dx_all = -1120 * sai
    luz_a, luz_b = luz_de(t, T, "A"), luz_de(t, T, "B")
    carimbo = lambda t0: 1 + 0.06 * bump(t, t0, 0.28)    # noqa: E731  re-pop do quadro 0
    refl = reflexo_tres(t, T["pino1"])

    # ---- B: a mancha grande que respira; cresce no "cresce"; marca laranja no "avise"; fone no "equipe"
    rb = raio_b1(t, T)
    ondas = ondas_b(t, rb, (T["vermelho"], T["b1"], T["cresce"], T["cresce"] + 0.28))
    volta = prog(t, T["vermelhidao"], T["vermelhidao"] + 0.25)
    alfa_b = 1 - 0.55 * prog(t, T["resp1"], T["resp1"] + 0.25) * (1 - volta)
    fecha = prog(t, T["avise1"] - 0.05, T["avise1"] + 0.2)
    fx, fy = fone_no_cartao(CART_B)
    fone_k = pop_in(t, T["avise1"] + 0.05, 0.3)          # v2: entra no "avise" (junto da marca), não no fim
    toque = (1 - prog(t, T["equipe1"] + 0.7, T["equipe1"] + 0.9)) if t >= T["avise1"] + 0.1 else 0.0
    rot_b = balanco(t, T["chuta"] + 0.14) + balanco(t, T["comum1"] + 0.12)
    cartao(cv, t, CART_B, "B", COR_B, pele=lambda c: mancha_grande(c, rb, ondas), sobre=refl,
           alfa=alfa_b, dx=dx_all, rot=rot_b, esc=carimbo(0.28),
           pulso=bump(t, T["b1"]) + 0.12 * luz_b + 0.6 * bump(t, T["na_b"], 0.3),
           acende=bump(t, T["b1"], 0.4), luz=luz_b, marca=COR_B, marca_a=fecha,
           por_cima=lambda c: telefone(c, fx, fy, clamp(fone_k * 3), toque, t, esc=1.25 * fone_k))
    marca_fecha(cv, CART_B, fecha, alfa_b, dx=dx_all)

    # ---- A: a mancha pequena; vira a resposta (OURO + brilhos), cresce no "reação", assenta no "leve"
    marca_a = prog(t, T["resp1"], T["resp1"] + 0.12) * (1 - prog(t, T["vermelhidao"], T["vermelhidao"] + 0.25))
    cresce_a = e_out(prog(t, T["reacao"], T["reacao"] + 0.3)) * (1 - e_inout(prog(t, T["comum2"], T["comum2"] + 0.35)))
    cartao(cv, t, CART_A, "A", COR_A, pele=pele_a(t, T, 1), sobre=refl,
           dx=dx_all, rot=balanco(t, T["chuta"]) + balanco(t, T["comum1"]),
           esc=carimbo(0.20) * (1 + 0.06 * cresce_a),
           pulso=bump(t, T["a1"]) + 0.12 * luz_a + bump(t, T["resp1"], 0.45),
           acende=bump(t, T["a1"], 0.4), luz=luz_a, marca=OURO, marca_a=marca_a,
           marca_brilho=bump(t, T["comum2"], 0.45))
    brilhos_borda(cv, (CART_A[0] + dx_all, CART_A[1], CART_A[2] + dx_all, CART_A[3]), t, T["resp1"] + 0.03)


# ------------------------------------------------------------------ rodada 2 + bônus
def raio_dor(t, T):
    """Raio da estrela de dor de B na rodada 2 (v2): PEQUENA na pergunta (a pista não grita); no 'dor'
    cresce um pouco; no 'nova' SOME por 0,25 s e VOLTA maior (e_back) com o anel da pele e um pop."""
    t_ac = T["rodada"] + 0.65
    if t < t_ac:
        return 0.0
    tn = T["nova"]
    if t < tn - 0.1:
        base = lerp(R_DOR[0], R_DOR[1], e_out(prog(t, T["dor"], T["dor"] + 0.2)))
        r = base * e_back(clamp((t - t_ac) / 0.3)) * (1 + 0.2 * bump(t, T["b2"], 0.35))
    elif t < tn:
        r = R_DOR[1] * (1 - (t - (tn - 0.1)) / 0.1)
    elif t < tn + 0.15:
        return 0.0
    else:
        r = R_DOR[2] * e_back(clamp((t - tn - 0.15) / 0.3))
    return r * (0.95 + 0.05 * math.cos((t - t_ac) * 9))


def rodada2(cv, t, T):
    if t < T["rodada"] + 0.05:
        return
    sai = e_inout(prog(t, T["bonus"] - 0.05, T["bonus"] + 0.3))
    if sai < 1:
        lift = e_back(prog(t, T["resp2"], T["resp2"] + 0.3)) if t >= T["resp2"] else 0.0
        explica = prog(t, T["secrecao"] - 0.1, T["secrecao"] + 0.2)    # "Pouca secreção clara é comum"
        for i, (r, letra, cor) in enumerate(((CART_A, "A", COR_A), (CART_B, "B", COR_B))):
            ent = e_inout(prog(t, T["rodada"] + 0.05 * i, T["rodada"] + 0.6 + 0.05 * i))
            t_l = T["a2"] if letra == "A" else T["b2"]
            luz = luz_de(t, T, letra)
            rot = balanco(t, T["dificil"] + 0.1 * i, amp=3.0, dur=0.7) + balanco(t, T["qual2"] + 0.14 * i)
            if letra == "A":                              # não é a resposta: apaga; VOLTA no "secreção clara"
                apaga = 0.55 * prog(t, T["resp2"], T["resp2"] + 0.25) * (1 - explica)
                ouro = prog(t, T["comum3"] - 0.05, T["comum3"] + 0.15)       # é o comum: OURO (tranquiliza)
                cartao(cv, t, r, letra, cor, pele=pele_a(t, T, 2), alfa=(1 - apaga) * (1 - sai),
                       dx=(1 - ent) * 1120 - 700 * sai, rot=rot,
                       esc=(1 - 0.03 * lift * (1 - explica)) * (1 + 0.05 * bump(t, T["secrecao"], 0.45)),
                       pulso=bump(t, t_l) + 0.12 * luz + 0.6 * bump(t, T["comum3"], 0.4),
                       acende=bump(t, t_l, 0.4), luz=luz, marca=OURO, marca_a=ouro)
            else:                                         # a resposta: marca LARANJA, sem brilho e sem ouro
                rd = raio_dor(t, T)
                kp = (t - T["pino2"]) / 0.7

                def pele(c, rd=rd):
                    dor_na_pele(c, t, T, rd)

                def sobre(c, kp=kp):
                    reflexo_pino(c, FOCO, kp)
                fx, fy = fone_no_cartao(r)
                fone_k = pop_in(t, T["avise2"] - 0.05, 0.3)
                toque = (1 - prog(t, T["cedo"] + 0.6, T["cedo"] + 0.8)) if t >= T["avise2"] else 0.0
                cartao(cv, t, r, letra, cor, pele=pele, sobre=sobre, alfa=(1 - 0.35 * explica) * (1 - sai),
                       dx=(1 - ent) * 1120 + 700 * sai, rot=rot, dy=-7 * lift * (1 - explica),
                       esc=(1 + 0.025 * lift * (1 - explica)) * (1 + 0.06 * bump(t, T["dor"], 0.5)),
                       pulso=bump(t, t_l) + 0.12 * luz + 0.5 * bump(t, T["resp2"], 0.3),
                       acende=bump(t, t_l, 0.4), luz=luz, marca=COR_B,
                       marca_a=prog(t, T["resp2"], T["resp2"] + 0.12), badge_esc=1 + 0.15 * lift * (1 - explica),
                       por_cima=lambda c, fx=fx, fy=fy, fk=fone_k, tq=toque:
                           telefone(c, fx, fy, clamp(fk * 3), tq, t, esc=1.25 * fk))
    bonus(cv, t, T)


def bonus(cv, t, T):
    """No 'Bônus': entra o cartão C (mesma perna, pele neutra, sem letra). 'pus' = gota de desenho
    amarelo-pus; 'cheiro' = linhas que nascem no pino e sobem; 'Avise também' = a MESMA marca laranja
    e o MESMO fone do B; 'Com febre' = o fone PARA, o cartão apaga para ~60 % e o termômetro entra
    fora do cartão; 'pronto-socorro' = o termômetro cresce +25 % com anéis vermelhos pulsando (a
    última palavra clínica tem o maior acontecimento do bônus)."""
    ent = prog(t, T["bonus"] + 0.18, T["bonus"] + 0.55)
    if ent <= 0:
        return
    a = clamp(ent * 2.5) * (1 - saida_final(t, T))
    if a <= 0:
        return
    e = e_back(ent)
    fecha = prog(t, T["avise3"] - 0.05, T["avise3"] + 0.2)
    gota_k = pop_in(t, T["pus"] - 0.03, 0.3)
    x, y = entrada(FOCO)

    def pele(c):
        gota(c, x - 6, y + 50, gota_k, clamp(gota_k * 3))

    def sobre(c):
        linhas_cheiro(c, t, T["cheiro"] - 0.03, 1.0)

    fx, fy = fone_no_cartao(CART_C)
    fone_k = pop_in(t, T["avise3"] - 0.02, 0.3)
    toque = (1 - prog(t, T["febre"] - 0.1, T["febre"] + 0.05)) if t >= T["avise3"] + 0.1 else 0.0
    febre = prog(t, T["febre"] - 0.05, T["febre"] + 0.25)
    esc = lerp(0.82, 1.0, e) * (1 + 0.035 * bump(t, T["avise3"], 0.35)) * (1 - 0.03 * febre)
    dy = 40 * (1 - e)
    cartao(cv, t, CART_C, None, "#FFFFFF", pele=pele, sobre=sobre, alfa=a * (1 - 0.4 * febre), esc=esc, dy=dy,
           marca=COR_B, marca_a=fecha, acende=bump(t, T["bonus"] + 0.3, 0.4),
           por_cima=lambda c: telefone(c, fx, fy, clamp(fone_k * 3), toque, t, esc=1.25 * fone_k))
    marca_fecha(cv, CART_C, fecha, a, dy=dy, esc=esc)
    # termômetro FORA do cartão, à direita; no "pronto-socorro" cresce e pulsa em vermelho
    tk = pop_in(t, T["febre"] - 0.03, 0.3)
    if tk > 0:
        a_t = clamp(tk * 3) * (1 - saida_final(t, T))
        nivel = e_out(prog(t, T["febre"] + 0.05, T["febre"] + 0.55))
        ps = e_back(prog(t, T["socorro"] - 0.02, T["socorro"] + 0.3)) if t >= T["socorro"] - 0.02 else 0.0
        cx_t, cy_t = 925, 760
        if ps > 0:
            for i in range(2):
                f = ((t - T["socorro"]) * 1.6 + i * 0.5) % 1.0
                cv.drawCircle(cx_t, cy_t + 8, lerp(78, 122, f), paint("#D64045", _a(230 * a_t * (1 - f) * clamp(ps)), "stroke", 6))
        termometro(cv, cx_t, cy_t, nivel, a_t, esc=1.8 * tk * (1 + 0.25 * ps))


# ------------------------------------------------------------------ topo: gancho, selo da série, rodada
def capa_jogo(cv, t, T, l1, l2):
    """Gancho de 2 linhas (como cf_comum.capa), cada linha pulsa quando é dita ('Vermelho' / 'comum').
    FICA durante a contagem (é a pergunta) e sai para CIMA na resposta, antes de o selo entrar."""
    sai = e_inout(prog(t, T["resp1"], T["resp1"] + 0.3))
    if sai >= 1:
        return
    a = 1 - sai
    cv.drawRect(skia.Rect(0, 0, W, 360), paint(BG_OUT, 255, shader=skia.GradientShader.MakeLinear(
        [skia.Point(0, 0), skia.Point(0, 360)], [C(BG_OUT, int(235 * a)), C(BG_OUT, 0)])))
    pulso = 1 + 0.025 * math.sin(t * 5)
    cv.save(); cv.translate(CX, 205 - 170 * sai); cv.scale(pulso, pulso)
    for y, s, cor, t0 in ((0, l1, "#FFFFFF", T["vermelho"]), (88, l2, OURO, T["comum1"])):
        e = 1 + 0.06 * bump(t, t0, 0.35)
        cv.save(); cv.translate(0, y - 28); cv.scale(e, e)
        texto(cv, s, 0, 28, F_BLACK, 78, cor, int(255 * a), contorno=10)
        cv.restore()
    cv.restore()


def selo_serie(cv, a):
    if a <= 0:
        return
    rr = skia.RRect.MakeRectXY(skia.Rect(CX - 190, 150, CX + 190, 204), 27, 27)
    cv.drawRRect(rr, paint("#FFFFFF", _a(28 * a)))
    texto(cv, "QUAL DOS DOIS?", CX, 190, F_BLACK, 32, OURO, _a(255 * a))


def pilula(cv, t, T):
    """'2 RODADAS' na capa; 'RODADA 1' / 'RODADA 2' com bolinhas de placar; 'BÔNUS' no fim."""
    a = 1 - saida_final(t, T)
    if a <= 0:
        return
    if t < T["cont1"]:
        s, n, t0 = "2 RODADAS", 0, 0.05
    elif t < T["rodada"] + 0.45:                  # v2: só vira quando a rodada 1 já saiu (o fone dela
        s, n, t0 = "RODADA 1", 1, T["cont1"]      # nunca aparece sob "RODADA 2")
    elif t < T["bonus"]:
        s, n, t0 = "RODADA 2", 2, T["rodada"] + 0.45
    else:
        s, n, t0 = "BÔNUS", 2, T["bonus"]
    esc = 1 + 0.15 * bump(t, t0, 0.3) + 0.18 * bump(t, T["dificil"], 0.35)
    tam = 32; lw = skia.Font(F_BLACK, tam).measureText(s)
    larg = lw + 36 + 18 + 2 * 22
    cv.save(); cv.translate(CX, 346); cv.scale(esc, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-larg / 2, -24, larg / 2, 24), 24, 24)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, _a(225 * a)))
    cv.drawRRect(rr, paint(OURO, _a(200 * a), "stroke", 2.5))
    texto(cv, s, -larg / 2 + 18, 11, F_BLACK, tam, "#FFFFFF", _a(255 * a), centro=False)
    for k in range(2):
        x = -larg / 2 + 18 + lw + 18 + 11 + 22 * k
        if n > k:
            cv.drawCircle(x, 0, 8, paint(OURO, _a(255 * a)))
        else:
            cv.drawCircle(x, 0, 7, paint("#FFFFFF", _a(170 * a), "stroke", 2.5))
    cv.restore()


# ------------------------------------------------------------------ CTA: os cartões da rodada 1 em miniatura
def minis(cv, t, T):
    k = prog(t, T["manda"] + 0.05, T["manda"] + 0.45)
    if k <= 0:
        return
    e = e_back(k)
    for i, (r, letra, cor, x) in enumerate(((CART_A, "A", COR_A, 458), (CART_B, "B", COR_B, 622))):
        cx, cy = _centro(r)
        rot = balanco(t, T["pinos"] + 0.13 * i, amp=4.0, dur=0.9)
        pele = (lambda c: mancha_leve(c)) if letra == "A" else (lambda c: mancha_grande(c, R_CRESCE))
        cv.save(); cv.translate(x, 368); cv.rotate(rot); cv.scale(0.28 * e, 0.28 * e); cv.translate(-cx, -cy)
        cartao(cv, t, r, letra, cor, pele=pele, alfa=clamp(k * 3), badge_esc=1.75)
        cv.restore()


# ------------------------------------------------------------------ quadro
def pergunta_fixa(blocos, T):
    """A pergunta da rodada 2 ('QUAL PEDE AVISAR / SUA EQUIPE?') esticada para ficar na tela durante a
    contagem. v2: 5 palavras = 1 bloco só (a v1 tinha 7 e o karaokê deixava 'PEDE' pendurado); se o
    montar_blocos ainda partir a pergunta, os blocos se JUNTAM aqui."""
    i_q = next((i for i, b in enumerate(blocos) if any(abs(p["t"] - T["qual2"]) < 1e-6 for p in b)), None)
    i_e = next((i for i, b in enumerate(blocos) if any(abs(p["t"] - T["equipe2"]) < 1e-6 for p in b)), None)
    if i_q is None or i_e is None or i_e < i_q:
        raise SystemExit("ERRO: blocos da pergunta da rodada 2 não achados.")
    junto = [p for b in blocos[i_q:i_e + 1] for p in b]
    if junto[0]["w"].lower() != "qual" or junto[-1]["tok"] != "equipe?":
        raise SystemExit(f"ERRO: pergunta da rodada 2 fora do esperado: {' '.join(p['tok'] for p in junto)}")
    ult = dict(junto[-1], d=max(junto[-1]["d"], T["resp2"] - junto[-1]["t"]))
    return junto[:-1] + [ult]


def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    rodada1(cv, t, T)
    rodada2(cv, t, T)
    anel_contagem(cv, t, T["cont1"])
    anel_contagem(cv, t, T["cont2"])
    capa_jogo(cv, t, T, ep["gancho"][0], ep["gancho"][1])
    selo_serie(cv, prog(t, T["resp1"] + 0.35, T["resp1"] + 0.7) * (1 - saida_final(t, T)))
    pilula(cv, t, T)
    # karaokê: a 1ª pergunta já é o gancho escrito (não duplica); na contagem 1 o gancho fica (é a
    # pergunta); na contagem 2 a pergunta da rodada fica escrita no lugar da legenda
    kara = [] if em_contagem(t, T) else [b for b in blocos if b[-1]["t"] >= T["chuta"] - 0.05]
    interface(cv, t, T, kara, DESTAQUE)
    if em_contagem(t, T, 2):
        a = prog(t, T["cont2"], T["cont2"] + 0.2)
        cv.saveLayer(None, _alfa(a)) if a < 1 else cv.save()
        legenda(cv, [T["_pergunta2"]], t, DESTAQUE)
        cv.restore()
    minis(cv, t, T)


# ------------------------------------------------------------------ som
def sons(T):
    ev = [(0.02, "pop", 0.5), (0.20, "pop", 0.45), (0.28, "pop", 0.4),
          (T["vermelho"], "pop", 0.5), (T["pino1"], "tick", 0.3),
          (T["chuta"], "whoosh", 0.25), (T["a1"], "pop", 0.6), (T["b1"], "pop", 0.6)]
    for t0 in (T["cont1"], T["cont2"]):                          # tique-taque constante
        ev += [(t0 + 0.5 * i, "tick" if i % 2 == 0 else "click", 0.75 if i % 2 == 0 else 1.0) for i in range(4)]
    ev += [(T["resp1"], "ding", 0.45), (T["reacao"], "pop", 0.35), (T["comum2"], "shimmer", 0.25),
           (T["vermelhidao"], "pop", 0.4), (T["cresce"], "thump", 0.5), (T["na_b"], "tick", 0.4),
           (T["avise1"], "click", 0.8), (T["avise1"] + 0.05, "pop", 0.4), (T["equipe1"], "tick", 0.5),
           (T["rodada"], "whoosh", 0.5), (T["rodada"] + 0.05, "pop", 0.4), (T["rodada"] + 0.55, "thump", 0.4),
           (T["dificil"], "pop", 0.45), (T["a2"], "pop", 0.6), (T["b2"], "pop", 0.6),
           (T["resp2"], "thump", 0.65), (T["resp2"] + 0.02, "pop", 0.5),
           (T["dor"], "tick", 0.6), (T["nova"] + 0.15, "pop", 0.6), (T["pino2"], "tick", 0.3), (T["avise2"], "click", 0.8),
           (T["secrecao"], "pop", 0.4), (T["clara"], "tick", 0.35), (T["comum3"], "shimmer", 0.25),
           (T["bonus"] - 0.05, "whoosh", 0.35), (T["bonus"] + 0.2, "pop", 0.45), (T["pus"], "pop", 0.45),
           (T["cheiro"], "tick", 0.4), (T["avise3"], "click", 0.8), (T["avise3"] + 0.02, "pop", 0.5),
           (T["tambem"], "thump", 0.45), (T["febre"], "pop", 0.5), (T["socorro"], "thump", 0.7),
           (T["manda"] + 0.05, "whoosh", 0.5), (T["pinos"], "pop", 0.4)]
    return ev


def janelas(T):
    return [(T["cont1"], T["cont1"] + CONTAGEM), (T["cont2"], T["cont2"] + CONTAGEM)]


def _media_movel(x, w):
    """= np.convolve(x, np.ones(w) / w, "same"), por soma acumulada (cópia do piloto)."""
    xp = np.concatenate([np.zeros(w // 2), x, np.zeros((w - 1) // 2)])
    c = np.concatenate([[0.0], np.cumsum(xp)])
    return (c[w:w + len(x)] - c[:len(x)]) / w


def mixar_jogo(voz, dur, eventos, jan, ganho_trilha=0.40, fundo_contagem=0.15, rampa=0.15):
    """(cópia do piloto) Como som.mixar (ducking pela voz, efeitos), mais um envelope que baixa a
    trilha para ~15% nas janelas de contagem: o tique-taque fica sozinho."""
    n = int(dur * som.SR)
    v = np.zeros(n); v[:min(n, len(voz))] = voz[:n]
    musica = som.trilha(dur) * ganho_trilha
    win = int(0.06 * som.SR)
    envv = np.sqrt(np.maximum(_media_movel(v ** 2, win), 0.0))
    alvo = np.where(envv > 0.02, 0.38, 1.0)
    duck = _media_movel(alvo, int(0.25 * som.SR))
    tt = np.arange(n) / som.SR
    env = np.ones(n)
    for a, b in jan:
        k = np.clip((tt - (a - rampa)) / rampa, 0, 1) * np.clip(((b + rampa) - tt) / rampa, 0, 1)
        env = np.minimum(env, 1 - (1 - fundo_contagem) * k)
    fx = np.zeros(n)
    for t0, nome, g in eventos:
        s = som.SFX[nome]()
        p = int(t0 * som.SR)
        if 0 <= p < n:
            m = min(len(s), n - p)
            fx[p:p + m] += s[:m] * g
    mix = v + musica * duck * env + fx * 0.7
    pico = np.max(np.abs(mix)) or 1.0
    return mix / pico * 0.89


# ------------------------------------------------------------------ entrada
def tempos_previa(T):
    return (0.0, T["pino1"] + 0.35, T["cont1"] + 1.2, T["resp1"] + 0.5, T["cresce"] + 0.6,
            T["equipe1"] + 0.3, T["rodada"] + 0.3, T["rodada"] + 0.8, T["cont2"] + 0.6, T["cont2"] + 1.7,
            T["resp2"] + 0.3, T["nova"] + 0.05, T["nova"] + 0.4, T["avise2"] + 0.4, T["clara"] + 0.2,
            T["comum3"] + 0.3, T["pus"] + 0.3, T["cheiro"] + 0.4, T["tambem"] + 0.2, T["febre"] + 0.4,
            T["socorro"] + 0.4, T["manda"] - 0.2, T["manda"] + 0.8, T["total"] - 0.1)


def preparar(ep, tmp):
    roteiro = "\n".join(ep["roteiro"])
    voz_bruta, palavras = _voz.narrar(roteiro, _voz.RITMO_COMO_FUNCIONA, os.path.join(tmp, "voz"))
    voz_c, pal, tirado = comprimir(voz_bruta, palavras, respiro_cta=0.6)
    pal = alinhar(pal, roteiro)
    voz_c, pal, conts = inserir_contagens(voz_c, pal)
    T = ancoras_jogo(pal, ANCORAS)
    T["cont1"], T["cont2"] = conts
    ordem = ("chuta", "cont1", "resp1", "rodada", "cont2", "resp2", "dor", "nova", "avise2", "secrecao",
             "comum3", "bonus", "pus", "cheiro", "avise3", "tambem", "febre", "socorro", "manda")
    if not all(T[a] < T[b] for a, b in zip(ordem, ordem[1:])):
        raise SystemExit("ERRO: ordem do jogo fora do roteiro (rodada 1 -> rodada 2 -> bônus -> CTA).")
    return voz_c, pal, T, tirado


def render(ep, mp4, tmp, previa=False):
    voz_c, pal, T, tirado = preparar(ep, tmp)
    print(f"{ep['id']}: silêncio cortado {tirado:.2f}s | contagens em {T['cont1']:.2f}s e {T['cont2']:.2f}s"
          f" | duração final {T['total']:.2f}s")
    blocos = montar_blocos(pal)
    T["_pergunta2"] = pergunta_fixa(blocos, T)

    def quadro_t(cv, t):
        quadro(cv, t, T, blocos, ep)

    if previa:
        return _previas(quadro_t, tempos_previa(T), tmp, ep["id"]), T["total"]
    wav = os.path.join(tmp, f"{ep['id']}_mix.wav")
    som.gravar_wav(wav, mixar_jogo(voz_c, T["total"], sons(T), janelas(T)))
    codificar(quadro_t, T["total"], wav, mp4)
    return mp4, T["total"]
