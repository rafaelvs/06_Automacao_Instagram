# -*- coding: utf-8 -*-
"""QUAL DOS DOIS? — dor de crescimento (2º episódio da série-jogo, depois do piloto do pé chato).

A mecânica é a do piloto cf_qualdosdois_pe_chato, sem tirar nem pôr: 2 rodadas e 1 bônus, palpite
antes da resposta. Cada rodada: dois cartões lado a lado (A azul, B laranja), a voz pergunta, as
letras pulsam quando ditas, 2 s de contagem SEM voz (anel 2-1, tique-taque, luz que alterna em ritmo
de relógio e APAGA no fim, terminando na opção que não é a resposta) e a revelação. A opção que não
é a resposta só apaga para 45%: nunca X, nunca vermelho, nunca deboche.

O que muda é o RECHEIO dos cartões: no lugar do piso de ladrilho, um CÉU (noite ou dia) com chão, e
dentro dele PERNAS DE CRIANÇA de desenho (as aprovadas do cf_pe_virado, de frente, e do
cf_crianca_mancando, de perfil, com a manqueira). A dor é desenhada de dois jeitos, nunca os dois no
mesmo cartão:
  * dor ESPALHADA = halo vermelho macio ATRÁS da canela + ondinhas de latejar '( )' por fora dela, que
    respiram e vagam (v2: a pele fica cor de pele — em v1 a névoa pintava a canela e lia como
    inflamação/queimadura, que é justamente o que NÃO é dor de crescimento);
  * dor NUM PONTO = a estrela de dor (do cf_pe_virado) pregada num ponto do joelho.
Nada de inchaço, sangue, osso, raio-X ou rosto.

  * Rodada 1 ("Qual dessas dores é de crescimento?", resposta A, marca OURO + ding): A = NOITE (lua,
    estrelas), pernas paradas de frente com névoa nas DUAS canelas; B = DIA (sol), pernas de perfil
    andando no lugar com a MANQUEIRA (apoio longo na boa, curto na que dói, o quadril cai), névoa só
    na perna que manca. O gancho FICA durante a contagem (é a pergunta). No "dói" o B sai e o A
    cresce; no "duas" as duas névoas pulsam; no "noite" a lua cresce; no "manhã" AMANHECE (aurora,
    a lua desce e some, o sol nasce atrás do chão); no "sumiu" as névoas somem soltando faíscas
    BRANCAS; no "brinca"/"normal" as pernas PULAM duas vezes (fim neutro, sem ouro).
  * Rodada 2 ("Agora, ao contrário: qual dos dois merece avaliação?", resposta B, marca LARANJA +
    thump): os DOIS cartões à noite. (v2: "ao contrário" no lugar de "mais difícil" — avisa que a
    pergunta virou, e o A repetido deixa de ser promessa de dificuldade não cumprida.) A = névoa nas duas canelas; B = perna
    esquerda limpa e UMA estrela de dor no joelho direito. Até a revelação as névoas de A vagam e a
    estrela de B fica pregada, pulsando. Depois, no "sempre", TRÊS NOITES rápidas (âncoras "sempre",
    "ali", "mesmo"): a lua fica PARADA no canto e brilha, as estrelas piscam, o céu escurece e
    clareia; em A a dor reaparece em lugares DIFERENTES a cada noite, em B a estrela re-acerta
    EXATAMENTE o mesmo ponto e deixa um anel branco que fica mais forte a cada acerto e trava no
    "mesmo". No "lado" as DUAS pernas do B ganham contorno juntas: a da estrela em laranja grosso, a
    limpa em branco (comparação). A fica a 45%: é o controle.
  * BÔNUS ("Bônus: mancou? Avalie. Com febre? Atendimento no mesmo dia." — v2: mancar SOZINHO já
    pede avaliação, e o "no mesmo dia" ganhou de quem é: atendimento): cartão C de DIA, que já entra
    com as pernas de perfil paradas; no "mancou" elas mancam e a dor aparece; no "Avalie" a MESMA
    marca laranja do B se fecha em volta do C; no "febre" um termômetro SEM número desliza e a coluna
    sobe; no "atendimento" a marca pulsa; no "no mesmo dia" um calendário SEM número (o do
    cf_crianca_mancando) vira folhas, freia e PARA numa folha inteira, e um círculo laranja feito à
    mão se fecha nela.
O desenho da noite NUNCA mostra a criança acordando (sem cama, olho, relógio): dor que acorda à noite
é sinal de alerta no próprio acervo. A febre só entra no bônus, junto com "no mesmo dia".

Render próprio (como o do piloto): a contagem é SILÊNCIO inserido no áudio depois do `comprimir()`,
a legenda karaokê muda durante a contagem e a trilha cai para ~15% nela. Âncoras das letras por
TOKEN ('A?', 'B?', 'A!', 'B!'); sem exatamente 2 'B?' seguidos da resposta, o render aborta.

Peças por IMPORT só da base (fundo, paleta, texto, comprimir/alinhar/blocos, interface/legenda). A
gramática do jogo é CÓPIA do piloto; pernas, lua, termômetro, estrela de dor e calendário são CÓPIA
do cf_pe_virado e do cf_crianca_mancando (copiados, não importados, para este vídeo não depender do
hash daquelas cenas). Todo texto desenhado está em ep["tela"], no gancho, no roteiro (karaokê) ou na
interface.
"""
import math
import os

import numpy as np
import skia

from . import som, voz as _voz
from .base import codificar, previas as _previas
from .cf_alongamento import (BG_OUT, CX, F_BLACK, OSSO_C, OURO, PELE, VERMELHO, W, C, clamp, e_back,
                             e_in_back, e_inout, e_out, fundo, lerp, paint, prog, texto)
from .cf_comum import interface, legenda
from .cf_fratura_cola import alinhar, comprimir, montar_blocos

# ------------------------------------------------------------------ roteiro -> tempos
ANCORAS = {
    "dores": ("dores", 1), "crescimento": ("crescimento", 1), "chuta": ("chuta", 1),
    "a1": ("tok:A?", 1), "b1": ("tok:B?", 1), "resp1": ("tok:A!", 1),
    "doi1": ("dói", 1), "duas": ("duas", 1), "pernas": ("pernas", 1), "noite1": ("noite", 1),
    "manha": ("manhã", 1), "sumiu": ("sumiu", 1), "brinca": ("brinca", 1), "normal": ("normal", 1),
    "agora": ("agora", 1), "contrario": ("contrário", 1), "avaliacao1": ("avaliação", 1),
    "a2": ("tok:A?", 2), "b2": ("tok:B?", 2), "resp2": ("tok:B!", 1),
    "doi2": ("dói", 2), "sempre": ("sempre", 1), "ali": ("ali", 1), "mesmo1": ("mesmo", 1),
    "lugar": ("lugar", 1), "lado": ("lado", 1), "merece2": ("merece", 2), "avaliacao2": ("avaliação", 2),
    "bonus": ("bônus", 1), "mancou": ("mancou", 1), "avalie": ("avalie", 1), "febre": ("febre", 1),
    "atendimento": ("atendimento", 1), "no2": ("no", 2), "mesmo2": ("mesmo", 2), "dia": ("dia", 1),
    "manda": ("manda", 1), "duvida": ("dúvida", 1),
}
DESTAQUE = {"crescimento", "duas", "noite", "manhã", "sumiu", "normal", "contrário", "merece", "avaliação",
            "sempre", "ali", "lugar", "lado", "bônus", "mancou", "avalie", "febre", "atendimento", "dia", "dúvida"}
CONTAGEM = 2.0                     # segundos de palpite (silêncio inserido depois de cada "B?")
RESPOSTAS = ("A!", "B!")


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
            raise SystemExit("ERRO: depois de cada 'B?' vem a resposta ('A!' ou 'B!') — roteiro fora do jogo.")
    ins = [pal[i]["t"] + pal[i]["d"] + 0.05 for i in idx]
    partes, ult = [], 0.0
    for x in ins:
        partes.append(voz[int(ult * som.SR):int(x * som.SR)]); partes.append(np.zeros(int(dur * som.SR), voz.dtype))
        ult = x
    partes.append(voz[int(ult * som.SR):])
    novas = [dict(p, t=p["t"] + dur * sum(1 for x in ins if p["t"] > x)) for p in pal]
    return np.concatenate(partes), novas, [ins[0], ins[1] + dur]


# ------------------------------------------------------------------ paleta
COR_A, COR_B = "#4FA3E0", "#F08A4B"
FUNDO_CARTAO = "#0B1824"
NOITE_1, NOITE_2 = "#0C1F3D", "#1D3D69"            # céu de noite (alto -> horizonte)
DIA_1, DIA_2 = "#5DB3E6", "#C4E8FA"                # céu de dia
AURORA = "#F6B27A"                                 # faixa quente do amanhecer
CHAO_NOITE, CHAO_DIA = "#13304C", "#E7D6B4"
SOL = "#FFD25E"
MARFIM = OSSO_C
# pele e shorts: os mesmos tons das pernas aprovadas (cf_pe_virado / cf_crianca_mancando), copiados
PELE_CL, PELE_ESC, PELE_LINHA = "#F7CDB8", "#DA987E", "#B9765E"
SHORT, SHORT_CL, SHORT_ESC, SHORT_LINHA = "#4C86C6", "#6FA3DA", "#3A6FA8", "#2C5A8E"

CART_A = (36, 392, 528, 1230)
CART_B = (552, 392, 1044, 1230)
CART_C = (290, 392, 790, 1230)     # o cartão do BÔNUS, no centro
LARGO = (36, 392, 1044, 1230)
CHAO_H = 92                        # faixa de chão no pé de cada cartão
ESTRELAS = ((0.30, 70), (0.56, 150), (0.62, 40), (0.12, 165))   # (fração da largura, px abaixo do topo)

# par de frente: o ponto (540, 1040) do mundo do cf_pe_virado vai para (cx, y) do cartão, escala s
FRENTE_CART = (0.88, 1150)         # (escala, y) nos cartões estreitos
FRENTE_LARGO = (0.95, 1150)        # no cartão largo da rodada 1 (as pernas crescem um pouco: o pulo cabe)
# par de perfil: (x do quadril, y do chão, escala) — o mundo do cf_crianca_mancando
PERFIL_B = (772, 1170, 1.18)
PERFIL_C = (476, 1170, 1.18)
FI0 = 0.68                         # fase do passo no quadro 0 (passada aberta, a perna que manca à frente)


def _alfa(a):
    p = skia.Paint(); p.setAlphaf(clamp(a)); return p


def _rr(r, raio=30):
    return skia.RRect.MakeRectXY(skia.Rect(*r), raio, raio)


def _centro(r):
    return (r[0] + r[2]) / 2, (r[1] + r[3]) / 2


def _c(h, a=255):
    h = h.lstrip("#")
    return skia.ColorSetARGB(int(a), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _mix(c1, c2, k, a=255):
    a1 = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]; b1 = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    k = clamp(k)
    return skia.ColorSetARGB(int(a), *(int(lerp(a1[i], b1[i], k)) for i in range(3)))


def _uniao(a, b):
    return skia.Op(a, b, skia.PathOp.kUnion_PathOp) or a


def _trim(pt, k):
    """Traço desenhado até a fração k (TrimPathEffect devolve None em k = 0). (cópia do cf_crianca_mancando)"""
    if k < 0.999:
        pe = skia.TrimPathEffect.Make(0.0, max(0.002, k))
        if pe is not None:
            pt.setPathEffect(pe)
    return pt


def bump(t, t0, dur=0.35):
    """0 -> 1 -> 0 em `dur` s a partir de t0 (pulso)."""
    return math.sin(math.pi * clamp((t - t0) / dur)) if t >= t0 else 0.0


def balanco(t, t0, amp=1.5, dur=1.0):
    """Balanço curto (graus) que amortece: o 'qual dos dois?' de quem pergunta."""
    k = t - t0
    if k < 0 or k > dur:
        return 0.0
    return amp * math.sin(2 * math.pi * k / 0.5) * (1 - k / dur)


# ------------------------------------------------------------------ céu, chão, lua, sol, estrelas
def lua(cv, x, y, r, a, cor=MARFIM, brilho=0.0):
    """(cópia do cf_crianca_mancando, com `brilho` extra)"""
    if a <= 0:
        return
    p = skia.Path(); p.addCircle(x, y, r)
    q = skia.Path(); q.addCircle(x + r * 0.48, y - r * 0.26, r * 0.86)
    c = skia.Op(p, q, skia.PathOp.kDifference_PathOp) or p
    if brilho > 0:
        cv.drawCircle(x, y, r * 1.6, paint(cor, int(70 * a * brilho), blur=26))
    cv.drawPath(c, paint(cor, int(110 * a), blur=12))
    cv.drawPath(c, paint(cor, int(255 * a)))


def sol(cv, x, y, r, a, giro=0.0, esc=1.0):
    """Sol de desenho: disco amarelo, halo e 10 raios."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc); cv.rotate(giro)
    cv.drawCircle(0, 0, r * 1.55, paint(SOL, int(80 * a), blur=22))
    for i in range(10):
        cv.save(); cv.rotate(i * 36)
        cv.drawLine(0, -(r + 13), 0, -(r + 31), paint(SOL, int(255 * a), "stroke", 7))
        cv.restore()
    cv.drawCircle(0, 0, r, paint(SOL, int(255 * a)))
    cv.drawCircle(-r * 0.32, -r * 0.32, r * 0.34, paint("#FFFFFF", int(70 * a), blur=8))
    cv.restore()


def estrelas(cv, r, a, pisca=(0.0, 0.0, 0.0, 0.0)):
    if a <= 0:
        return
    x0, y0, x1, _ = r
    for (fx, dy), p in zip(ESTRELAS, pisca):
        x, y = x0 + fx * (x1 - x0), y0 + dy
        s = 1 + 1.3 * p
        cv.drawCircle(x, y, 7 * s, paint("#FFFFFF", int(50 * a), blur=5))
        cv.drawCircle(x, y, 2.6 * s, paint("#FFFFFF", int(235 * a)))


def _desenha_ceu(cv, r, dia, aurora=0.0):
    """Céu (degradê do alto ao horizonte) e a faixa de chão; `dia` 0 = noite, 1 = dia."""
    x0, y0, x1, y1 = r
    yc = y1 - CHAO_H
    sh = skia.GradientShader.MakeLinear([skia.Point(0, y0), skia.Point(0, yc)],
                                        [_mix(NOITE_1, DIA_1, dia), _mix(NOITE_2, DIA_2, dia)])
    cv.drawRect(skia.Rect(x0, y0, x1, yc), paint("#000000", 255, shader=sh))
    if aurora > 0:                                        # amanhecer: faixa quente no horizonte
        sh = skia.GradientShader.MakeLinear([skia.Point(0, yc - 330), skia.Point(0, yc)],
                                            [_c(AURORA, 0), _c(AURORA, int(235 * aurora))])
        cv.drawRect(skia.Rect(x0, yc - 330, x1, yc), paint("#000000", 255, shader=sh))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, yc), skia.Point(0, y1)],
                                        [_mix(CHAO_NOITE, CHAO_DIA, dia), _mix("#0E2438", "#D8C49E", dia)])
    cv.drawRect(skia.Rect(x0, yc, x1, y1), paint("#000000", 255, shader=sh))
    cv.drawLine(x0, yc, x1, yc, paint("#FFFFFF", int(lerp(40, 90, dia)), "stroke", 2))


def _desenha_base(cv, r, dia, aurora=0.0):
    cv.drawRRect(_rr((r[0], r[1] + 12, r[2], r[3] + 12)), paint("#000000", 110, blur=20))
    cv.save(); cv.clipRRect(_rr(r), skia.ClipOp.kIntersect, True)
    _desenha_ceu(cv, r, dia, aurora)
    cv.restore()


_BASES = {}


def base_cartao(cv, r, dia=0.0, aurora=0.0):
    """Sombra + céu + chão. Nos retângulos fixos, de noite ou de dia, vem de uma imagem pronta (como o
    piso do piloto); no amanhecer e nos retângulos que mudam, é desenhado quadro a quadro."""
    if r not in (CART_A, CART_B, CART_C, LARGO) or dia not in (0.0, 1.0) or aurora > 0:
        _desenha_base(cv, r, dia, aurora); return
    chave = (r, dia)
    if chave not in _BASES:
        m = 60
        surf = skia.Surface(int(r[2] - r[0] + 2 * m), int(r[3] - r[1] + 2 * m))
        c = surf.getCanvas(); c.clear(skia.ColorTRANSPARENT); c.translate(m - r[0], m - r[1])
        _desenha_base(c, r, dia)
        _BASES[chave] = (surf.makeImageSnapshot(), r[0] - m, r[1] - m)
    img, x, y = _BASES[chave]
    cv.drawImage(img, x, y)


def esteira(cv, r, dist, a=1.0, dia=1.0):
    """Risquinhos no chão que correm para trás (as pernas de perfil andam no lugar)."""
    if a <= 0:
        return
    x0, _, x1, y1 = r
    yc = y1 - CHAO_H
    passo = 74.0; off = dist % passo
    cor = "#B99E70" if dia > 0.5 else "#2F5376"
    x = x0 - off
    while x < x1 + passo:
        for y, w in ((yc + 24, 30), (yc + 58, 40)):
            xx = x + (0 if y < yc + 40 else passo / 2)
            cv.drawLine(xx, y, xx + w, y, paint(cor, int(200 * a), "stroke", 4))
        x += passo


# ------------------------------------------------------------------ a dor: névoa (espalhada) e estrela (num ponto)
def aura_dor(cv, x, y, ry, a, esc=1.0, ang=0.0, meia=47.0):
    """Dor ESPALHADA, parte 1 (v2): halo vermelho macio desenhado ATRÁS da perna — aparece só em volta
    dela, a pele continua cor de pele (v1 pintava a canela de vermelho e o leitor às cegas leu
    'inflamação ou queimadura'; vermelhidão é justamente o que NÃO é dor de crescimento).
    `a` > 1 reforça (o A apagado a 45% na rodada 2 continua mostrando onde dói)."""
    if a <= 0 or esc <= 0:
        return
    rx = meia + 62
    cv.save(); cv.translate(x, y); cv.rotate(ang); cv.scale(esc * rx / ry, esc)
    sh = skia.GradientShader.MakeRadial(skia.Point(0, 0), ry,
                                        [_c(VERMELHO, int(min(255, 215 * a))), _c(VERMELHO, int(min(230, 150 * a))),
                                         _c(VERMELHO, 0)], [0.0, 0.55, 1.0])
    cv.drawCircle(0, 0, ry, paint("#000000", 255, shader=sh))
    cv.restore()


def ondas_dor(cv, x, y, ry, a, t, esc=1.0, ang=0.0, meia=47.0):
    """Dor ESPALHADA, parte 2 (v2): ondinhas de 'latejar' dos DOIS lados do trecho que dói, POR FORA
    da perna — '(' à esquerda e ')' à direita, abrindo e sumindo em ciclo de 0,8 s (duas defasadas).
    É a convenção de desenho de 'isto dói', sem pintar a pele."""
    if a <= 0 or esc <= 0:
        return
    al = clamp(a)
    cv.save(); cv.translate(x, y); cv.rotate(ang); cv.scale(esc, esc)
    for lado in (-1, 1):
        for k in range(2):
            u = (t / 0.8 + k * 0.5) % 1.0
            aa = al * math.sin(math.pi * u) ** 0.8
            if aa <= 0.01:
                continue
            off = meia + 14 + 40 * u
            h = ry * (0.46 + 0.14 * u)
            p = skia.Path(); p.moveTo(lado * off, -h); p.quadTo(lado * (off + 30), 0, lado * off, h)
            cv.drawPath(p, paint(VERMELHO, int(110 * aa), "stroke", 20, blur=7))
            cv.drawPath(p, paint(VERMELHO, int(255 * aa), "stroke", 9))
    cv.restore()


def _meia_frente(y):
    """Meia-largura (mundo) da perna de FRENTE na altura y (medida no contorno de perna_path)."""
    if y <= Y_COXA:
        return 56.0
    if y <= Y_CANELA:
        return lerp(56.0, 48.0, (y - Y_COXA) / (Y_CANELA - Y_COXA))
    return lerp(48.0, 37.0, clamp((y - Y_CANELA) / (Y_BAIXO - Y_CANELA)))


def estrela_dor(cv, x, y, r, a):
    """(cópia do cf_pe_virado, aprovado)"""
    if a <= 0:
        return
    p = skia.Path(); n = 9
    for i in range(2 * n):
        ang = -math.pi / 2 + i * math.pi / n
        rr = (r if i % 4 == 0 else r * 0.84) if i % 2 == 0 else r * 0.46
        (p.moveTo if i == 0 else p.lineTo)(x + rr * math.cos(ang), y + rr * math.sin(ang))
    p.close()
    cv.drawPath(p, paint(VERMELHO, int(120 * a), blur=12))
    cv.drawPath(p, paint(VERMELHO, int(255 * a)))
    cv.drawPath(p, paint("#FFD3D4", int(200 * a), "stroke", 2.5))


def faiscas_brancas(cv, pontos, t, t0, dur=0.7, n=7):
    """As névoas somem soltando faíscas BRANCAS que sobem (nunca ouro: o ouro foi só a revelação)."""
    k = t - t0
    if k < 0 or k > dur:
        return
    u = k / dur
    for j, (x, y) in enumerate(pontos):
        for i in range(n):
            fx = ((i * 37 + j * 11) % 10) / 10 - 0.5
            px = x + fx * 120 + 30 * math.sin(i * 1.7 + j)
            py = y - 40 - 200 * e_out(u) * (0.6 + 0.4 * ((i * 53) % 10) / 10)
            s = 9 * (1 - u) + 3
            p = skia.Path(); p.moveTo(px, py - s * 2); p.lineTo(px + s * 0.5, py - s * 0.5); p.lineTo(px + s * 2, py)
            p.lineTo(px + s * 0.5, py + s * 0.5); p.lineTo(px, py + s * 2); p.lineTo(px - s * 0.5, py + s * 0.5)
            p.lineTo(px - s * 2, py); p.lineTo(px - s * 0.5, py - s * 0.5); p.close()
            cv.drawPath(p, paint("#FFFFFF", int(255 * (1 - u))))


# ------------------------------------------------------------------ pernas de FRENTE (cópia do cf_pe_virado)
XE, XD = 420, 660                 # perna da esquerda / da direita da tela
Y_PISO = 992                      # tornozelo no chão
PE_L, PE_W, K_PISO = 150, 96, 0.70
ANG_PE = 6                        # pés quase retos (ponta levemente para o meio)
ANCORA_F = (540, 1040)            # ponto do mundo que vai para (cx, y) do cartão
PE_BASE = 1112                    # ponta dos dedos (o pulo estica/amassa a partir daqui)
Y_CANELA, Y_COXA, Y_BAIXO, Y_JOELHO = 875, 665, 950, 760


def perna_path(x):
    """Coxa + joelho + canela num contorno só, arredondado (perna de desenho, sem osso)."""
    p = skia.Path()
    p.moveTo(x - 64, 470)
    p.cubicTo(x - 67, 600, x - 52, 700, x - 47, 768)
    p.cubicTo(x - 44, 815, x - 52, 860, x - 45, 900)
    p.cubicTo(x - 40, 940, x - 33, 958, x - 31, 982)
    p.arcTo(skia.Rect(x - 31, 951, x + 31, 1013), 180, -180, False)
    p.cubicTo(x + 33, 958, x + 40, 940, x + 45, 900)
    p.cubicTo(x + 52, 860, x + 44, 815, x + 47, 768)
    p.cubicTo(x + 52, 700, x + 67, 600, x + 64, 470)
    p.close()
    return p


def _piso(x, ang, lado):
    """Projeção de um ponto do chão: (ao longo do pé, através do pé) -> tela."""
    th = math.radians(ang)
    dx, dz = math.sin(th) * lado, math.cos(th)
    nx, nz = dz, -dx

    def P(a, b):
        return x + a * dx + b * nx, Y_PISO + (a * dz + b * nz) * K_PISO
    return P


def pe_forma(x, ang, lado):
    """Pé no chão saindo do tornozelo; `ang` > 0 = ponta para o meio. Devolve (contorno, dedos)."""
    P = _piso(x, ang, lado)
    p = skia.Path(); n = 56
    for i in range(n):                                 # superelipse: pé gordinho, mais largo nos dedos
        ph = 2 * math.pi * i / n
        cu, su = math.cos(ph), math.sin(ph)
        u = math.copysign(abs(cu) ** 0.7, cu)
        a = lerp(-20, PE_L, (u + 1) / 2)
        b = (PE_W / 2) * math.copysign(abs(su) ** 0.7, su) * (0.80 + 0.20 * (u + 1) / 2)
        (p.moveTo if i == 0 else p.lineTo)(*P(a, b))
    p.close()
    med = lado                                         # lado de dentro = dedão
    dedos = [(*P(PE_L - 6 + da, f * PE_W / 2 * med), r) for da, f, r in
             ((-2, 0.62, 15.5), (4, 0.27, 12.5), (4, -0.06, 12), (2, -0.38, 11), (-4, -0.66, 10))]
    return p, dedos


def _pele(cv, pth, x, w, a, sombra=True):
    sh = skia.GradientShader.MakeLinear([skia.Point(x - w / 2, 0), skia.Point(x + w / 2, 0)],
                                        [_c(PELE_ESC), _c(PELE), _c(PELE_CL), _c(PELE), _c(PELE_ESC)],
                                        [0.0, 0.22, 0.5, 0.78, 1.0])
    cv.drawPath(pth, paint(PELE, int(255 * a), shader=sh))
    cv.drawPath(pth, paint(PELE_LINHA, int(230 * a), "stroke", 3.2))


_PERNAS_F = {}


def _formas_frente(x, lado):
    if (x, lado) not in _PERNAS_F:
        pe, dedos = pe_forma(x, ANG_PE, lado)
        corpo = perna_path(x)
        _PERNAS_F[(x, lado)] = (pe, dedos, corpo, skia.Op(corpo, pe, skia.PathOp.kUnion_PathOp) or corpo)
    return _PERNAS_F[(x, lado)]


def perna_frente(cv, x, lado, contorno=0.0, cor_contorno="#FFFFFF", larg_contorno=5.0):
    """Perna de desenho sempre OPACA, cor de pele normal (o `perna` do cf_pe_virado, sem os anéis);
    `contorno` acende um contorno em volta dela (o 'pernas' e o 'lado'): faixa de `larg_contorno` px
    (mundo) POR FORA do contorno, mais o brilho."""
    pe, dedos, corpo, uni = _formas_frente(x, lado)
    _pele(cv, pe, x + 30 * lado * math.sin(math.radians(ANG_PE)), 140, 1.0)
    for dx, dy, r in dedos:
        cv.drawCircle(dx, dy, r, paint(PELE_CL, 255))
        cv.drawCircle(dx, dy, r, paint(PELE_LINHA, 230, "stroke", 2.6))
    _pele(cv, corpo, x, 130, 1.0)
    cv.drawArc(skia.Rect(x - 20, 748, x + 20, 772), 25, 130, False, paint(PELE_LINHA, 140, "stroke", 3))   # joelho
    if contorno > 0:                                   # (v2) só POR FORA da perna: a pele nunca fica tingida
        cv.save(); cv.clipPath(uni, skia.ClipOp.kDifference, True)
        cv.drawPath(uni, paint(cor_contorno, int(120 * clamp(contorno)), "stroke", larg_contorno * 4.4, blur=9))
        cv.drawPath(uni, paint(cor_contorno, int(255 * clamp(contorno)), "stroke", larg_contorno * 2))
        cv.restore()


def shorts(cv):
    p = skia.Path()
    p.moveTo(344, 424); p.lineTo(736, 424); p.lineTo(764, 566); p.lineTo(562, 572); p.lineTo(540, 530)
    p.lineTo(518, 572); p.lineTo(316, 566); p.close()
    pt = paint(SHORT); pt.setPathEffect(skia.CornerPathEffect.Make(18))
    cv.drawPath(p, paint("#000000", 70, blur=10))
    cv.drawPath(p, pt)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(342, 420, 738, 452), 14, 14), paint(SHORT_CL))
    cv.drawLine(540, 456, 540, 506, paint("#3A6FA8", 255, "stroke", 3))


def par_frente(cv, cx, y, s, nevoas=(), estrela=None, anel=None, contorno=(0.0, 0.0), cor_contorno="#FFFFFF",
               salto=(0.0, 1.0, 1.0), faiscas=None, t=0.0, larg_contorno=(5.0, 5.0)):
    """Par de pernas de criança de frente, paradas. `nevoas`: [(x, y, ry, alfa, esc)] no mundo (dor
    espalhada: halo ATRÁS da perna + ondinhas por fora, fase pelo `t`); `estrela`: (x, y, r_tela, alfa,
    brilho); `anel`: (alfa, travado); `salto`: (dy na tela, sx, sy); `faiscas`: (t, t0) para as faíscas
    brancas do 'sumiu'; `cor_contorno`: uma cor ou (esquerda, direita)."""
    dy, sx, sy = salto
    cores = cor_contorno if isinstance(cor_contorno, tuple) else (cor_contorno, cor_contorno)
    cv.save(); cv.translate(cx, y); cv.scale(s, s); cv.translate(-ANCORA_F[0], -ANCORA_F[1])
    k = 1 - 0.5 * clamp(-dy / 110)                       # a sombra encolhe enquanto o par está no ar
    for x in (XE, XD):
        cv.drawOval(skia.Rect(x - 100 * k, Y_PISO + 54, x + 100 * k, Y_PISO + 112), paint("#000000", int(85 * k), blur=12))
    cv.translate(0, dy / s)
    cv.translate(ANCORA_F[0], PE_BASE); cv.scale(sx, sy); cv.translate(-ANCORA_F[0], -PE_BASE)
    for nx, ny, ry, a, esc in nevoas:                   # o halo fica ATRÁS das pernas
        aura_dor(cv, nx, ny, ry, a, esc, 0.0, _meia_frente(ny))
    perna_frente(cv, XE, 1, contorno[0], cores[0], larg_contorno[0])
    perna_frente(cv, XD, -1, contorno[1], cores[1], larg_contorno[1])
    shorts(cv)
    for nx, ny, ry, a, esc in nevoas:                   # as ondinhas, por fora, na frente
        ondas_dor(cv, nx, ny, ry, a, t + 0.37 * (nx > ANCORA_F[0]), esc, 0.0, _meia_frente(ny))
    if estrela:
        ex, ey, r, a, br = estrela
        r /= s
        if a > 0:
            sh = skia.GradientShader.MakeRadial(skia.Point(ex, ey), 70 / s * (1 + 0.15 * br),
                                                [_c(VERMELHO, int(150 * a)), _c(VERMELHO, 0)])
            cv.drawCircle(ex, ey, 70 / s * (1 + 0.15 * br), paint("#000000", 255, shader=sh))
        if anel and anel[0] > 0:
            aa, trav = anel
            ra = 92 / s
            if trav > 0:
                cv.drawCircle(ex, ey, ra, paint("#FFFFFF", int(120 * trav), "stroke", 16 / s, blur=8 / s))
            cv.drawCircle(ex, ey, ra, paint("#FFFFFF", int(255 * aa), "stroke", lerp(2.5, 5.0, trav) / s))
        estrela_dor(cv, ex, ey, r, a)
    if faiscas:
        faiscas_brancas(cv, [(XE, Y_CANELA), (XD, Y_CANELA)], faiscas[0], faiscas[1])
    cv.restore()


# ------------------------------------------------------------------ pernas de PERFIL com a manqueira (cópia do cf_crianca_mancando)
Y_CHAO = 930                       # linha da sola
GY = Y_CHAO - 30                   # tornozelo apoiado
HX0, HY0 = 540, GY - 352
L1, L2 = 182, 182                  # coxa, perna (de criança: curtas e roliças)
F_FRENTE = 80
LIFT = 58
P_CICLO = 0.95                     # um ciclo = dois passos (apoio longo ~0,66 s na boa, curto ~0,34 s na que dói)
SD_SAO = 0.70                      # a perna boa fica MUITO tempo no chão...
S0_MAN, SD_MAN = 0.66, 0.36        # ...a que manca, POUCO (ritmo longo-curto)
VEL = 2 * F_FRENTE / (SD_SAO * P_CICLO)
R_QUAD, R_JOE, R_TOR = 37, 30, 20


def pe_no_ciclo(fi, s0, sd):
    """-> (x do tornozelo em relação ao quadril, altura, inclinação do pé, no chão?, fração da fase)."""
    u = (fi - s0) % 1.0
    if u < sd:
        return F_FRENTE - VEL * P_CICLO * u, 0.0, 0.0, True, u / sd
    w = (u - sd) / (1 - sd)
    xb = F_FRENTE - VEL * P_CICLO * sd
    return lerp(xb, F_FRENTE, e_inout(w)), LIFT * math.sin(math.pi * w), 22 * (1 - 2 * w) * math.sin(math.pi * w), False, w


def pose(fi):
    """(quadril, tornozelo da perna boa, tornozelo da que manca); o quadril CAI no apoio curto."""
    xs, ys, ps, ch_s, fs = pe_no_ciclo(fi, 0.0, SD_SAO)
    xm, ym, pm, ch_m, fm = pe_no_ciclo(fi, S0_MAN, SD_MAN)
    dy = (-6 * math.sin(math.pi * fs) if ch_s else 0.0) + (18 * math.sin(math.pi * fm) if ch_m else 0.0)
    return (HX0, HY0 + dy), (HX0 + xs, GY - ys, ps), (HX0 + xm, GY - ym, pm)


def joelho(hx, hy, ax, ay):
    """Cinemática inversa de dois segmentos; o joelho dobra para a frente (+x)."""
    dx, dy = ax - hx, ay - hy
    d = max(1.0, min(math.hypot(dx, dy), L1 + L2 - 0.5))
    fi = math.atan2(dy, dx)
    al = math.acos(clamp((L1 * L1 + d * d - L2 * L2) / (2 * L1 * d), -1.0, 1.0))
    return hx + L1 * math.cos(fi - al), hy + L1 * math.sin(fi - al)


def tubo(x0, y0, r0, x1, y1, r1):
    L = math.hypot(x1 - x0, y1 - y0) or 1.0
    nx, ny = -(y1 - y0) / L, (x1 - x0) / L
    p = skia.Path()
    p.moveTo(x0 + nx * r0, y0 + ny * r0); p.lineTo(x1 + nx * r1, y1 + ny * r1)
    p.lineTo(x1 - nx * r1, y1 - ny * r1); p.lineTo(x0 - nx * r0, y0 - ny * r0); p.close()
    c0 = skia.Path(); c0.addCircle(x0, y0, r0)
    c1 = skia.Path(); c1.addCircle(x1, y1, r1)
    return _uniao(_uniao(p, c0), c1)


def pe_path(ax, ay, inc):
    """Pé de desenho (gordinho), saindo do tornozelo, apontando para a frente; sola em y + 30."""
    p = skia.Path()
    p.moveTo(-17, -16)
    p.cubicTo(-30, -8, -33, 22, -16, 29)
    p.cubicTo(-4, 31, 30, 31, 56, 30)
    p.cubicTo(78, 29, 82, 10, 66, 5)
    p.cubicTo(46, -1, 27, -6, 18, -16)
    p.close()
    m = skia.Matrix(); m.setScale(1.12, 1.12); m.postRotate(inc); m.postTranslate(ax, ay)
    p.transform(m)
    return p


def perna_lado(cv, hip, ank, longe=False):
    """Perna de desenho (coxa + perna + pé num contorno só), sempre opaca. Devolve o joelho."""
    hx, hy = hip; ax, ay, inc = ank
    kx, ky = joelho(hx, hy, ax, ay)
    corpo = _uniao(_uniao(tubo(hx, hy, R_QUAD, kx, ky, R_JOE), tubo(kx, ky, R_JOE, ax, ay, R_TOR)), pe_path(ax, ay, inc))
    cv.save(); cv.clipPath(corpo, skia.ClipOp.kIntersect, True)
    cv.drawPath(corpo, paint(PELE))
    for x0, y0, r0, x1, y1, r1 in ((ax, ay, R_TOR, kx, ky, R_JOE), (kx, ky, R_JOE, hx, hy, R_QUAD)):
        L = math.hypot(x1 - x0, y1 - y0) or 1.0
        nx, ny = -(y1 - y0) / L, (x1 - x0) / L
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        r = (r0 + r1) / 2
        sh = skia.GradientShader.MakeLinear([skia.Point(mx - nx * r, my - ny * r), skia.Point(mx + nx * r, my + ny * r)],
                                            [_c(PELE_ESC), _c(PELE), _c(PELE_CL), _c(PELE), _c(PELE_ESC)],
                                            [0.0, 0.22, 0.5, 0.78, 1.0])
        cv.drawPath(tubo(x0, y0, r0, x1, y1, r1), paint(PELE, shader=sh))
    if longe:                                                     # perna de trás um tom mais escura
        cv.drawPath(corpo, paint("#3A2620", 70))
    cv.restore()
    cv.drawPath(corpo, paint(PELE_LINHA, 230, "stroke", 3.2))
    return kx, ky


def manga_short(hip, joe):
    """Barra do shorts (reta) no referencial da coxa -> (contorno, linha da bainha)."""
    hx, hy = hip; kx, ky = joe
    L = math.hypot(kx - hx, ky - hy) or 1.0
    ux, uy = (kx - hx) / L, (ky - hy) / L; nx, ny = -uy, ux
    ex, ey = hx + ux * 78, hy + uy * 78
    p = skia.Path()
    p.moveTo(hx + nx * 45, hy + ny * 45); p.lineTo(ex + nx * 42, ey + ny * 42)
    p.lineTo(ex - nx * 42, ey - ny * 42); p.lineTo(hx - nx * 45, hy - ny * 45); p.close()
    c = skia.Path(); c.addCircle(hx, hy, 45)
    bainha = ((ex + nx * 38 - ux * 10, ey + ny * 38 - uy * 10), (ex - nx * 38 - ux * 10, ey - ny * 38 - uy * 10))
    return _uniao(p, c), bainha


def path_cintura(hip):
    hx, hy = hip
    p = skia.Path()
    p.moveTo(hx - 58, hy - 86)
    p.lineTo(hx + 54, hy - 86)
    p.cubicTo(hx + 62, hy - 40, hx + 62, hy - 6, hx + 50, hy + 22)
    p.lineTo(hx - 38, hy + 26)
    p.cubicTo(hx - 70, hy + 16, hx - 76, hy - 34, hx - 58, hy - 86)
    p.close()
    return p


def pernas(cv, hip, sao, man):
    """Perna boa (de trás), perna que manca (da frente) e o shorts por cima, num contorno só.
    Devolve o joelho da perna que manca."""
    ks = perna_lado(cv, hip, sao, longe=True)
    m_s, b_s = manga_short(hip, ks)
    cv.drawPath(m_s, paint(SHORT_ESC)); cv.drawPath(m_s, paint(SHORT_LINHA, 220, "stroke", 2.6))
    cv.drawLine(b_s[0][0], b_s[0][1], b_s[1][0], b_s[1][1], paint(SHORT_LINHA, 150, "stroke", 2.6))
    km = perna_lado(cv, hip, man)
    m_m, b_m = manga_short(hip, km)
    sh = _uniao(path_cintura(hip), m_m)
    cv.drawPath(sh, paint("#000000", 50, blur=8))
    cv.drawPath(sh, paint(SHORT))
    hx, hy = hip
    cv.save(); cv.clipPath(sh, skia.ClipOp.kIntersect, True)
    cv.drawRect(skia.Rect(hx - 90, hy - 90, hx + 90, hy - 62), paint(SHORT_CL))              # cós
    cv.drawLine(hx - 90, hy - 62, hx + 90, hy - 62, paint(SHORT_LINHA, 120, "stroke", 2))
    cv.restore()
    cv.drawPath(sh, paint(SHORT_LINHA, 230, "stroke", 2.8))
    cv.drawLine(b_m[0][0], b_m[0][1], b_m[1][0], b_m[1][1], paint(SHORT_LINHA, 150, "stroke", 2.6))
    return km


MEIA_PERFIL = 27.0                 # meia-largura da canela de perfil (entre R_JOE e R_TOR, com o traço)


def par_perfil(cv, x, y_chao, s, fi, nev_a=1.0, nev_esc=1.0, a=1.0, t=0.0):
    """As pernas de perfil andando no lugar com a manqueira (fase `fi`); a dor (halo + ondinhas, os dois
    atrás das pernas) só na canela da que manca."""
    if a <= 0:
        return
    cv.saveLayer(None, _alfa(a)) if a < 1 else cv.save()
    cv.translate(x, y_chao); cv.scale(s, s); cv.translate(-HX0, -Y_CHAO)
    cv.drawOval(skia.Rect(HX0 - 150, Y_CHAO - 10, HX0 + 170, Y_CHAO + 18), paint("#000000", 70, blur=10))
    hip, sao, man = pose(fi)
    kx, ky = joelho(hip[0], hip[1], man[0], man[1])
    ax, ay = man[0], man[1]
    ang = math.degrees(math.atan2(ay - ky, ax - kx)) - 90
    mx, my = (kx + ax) / 2, (ky + ay) / 2
    aura_dor(cv, mx, my, 120, nev_a, nev_esc, ang, MEIA_PERFIL)       # halo e ondinhas ATRÁS das duas pernas:
    ondas_dor(cv, mx, my, 120, nev_a, t, nev_esc, ang, MEIA_PERFIL)   # nenhuma pele fica vermelha e a onda
    pernas(cv, hip, sao, man)                                         # nunca cai em cima da perna boa
    cv.restore()


def dist_esteira(fi, s):
    return fi * VEL * P_CICLO * s


# ------------------------------------------------------------------ cartão A | B (do piloto, com céu no lugar do piso)
def selo_letra(cv, letra, x, y, cor, esc=1.0, a=1.0, badge_esc=1.0):
    if a <= 0:
        return
    r = 44 * badge_esc
    x, y = x + r - 44, y + r - 44                         # o selo cresce para dentro do cartão
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    cv.drawCircle(0, 5, r, paint("#000000", int(90 * a), blur=8))
    cv.drawCircle(0, 0, r, paint(cor, int(255 * a)))
    cv.drawCircle(0, 0, r - 3, paint("#FFFFFF", int(70 * a), "stroke", 3))
    tam = 64 * badge_esc
    texto(cv, letra, 0, tam * 0.355, F_BLACK, tam, FUNDO_CARTAO, int(255 * a))
    cv.restore()


def cartao(cv, t, r, letra, cor, desenho=None, alfa=1.0, dx=0.0, dy=0.0, rot=0.0, esc=1.0, pulso=0.0,
           acende=0.0, luz=0.0, marca=None, marca_a=0.0, badge_esc=1.0, dia=0.0, aurora=0.0, astros=None,
           escuro=0.0, por_cima=None):
    """Cartão com céu e chão, `astros(cv)` (lua/sol/estrelas) e `desenho(cv)` (as pernas), recortados;
    o selo da letra (`letra=None`: sem selo). `luz` = luz da contagem (branca); `marca` = marcador da
    revelação (OURO na rodada 1; a cor do B na rodada 2 e no bônus); `escuro` = noite mais funda."""
    if alfa <= 0:
        return
    cx, cy = _centro(r)
    cv.saveLayer(None, _alfa(alfa)) if alfa < 1 else cv.save()
    cv.translate(dx, dy)
    cv.translate(cx, cy); cv.rotate(rot); cv.scale(esc, esc); cv.translate(-cx, -cy)
    rr = _rr(r)
    base_cartao(cv, r, dia, aurora)
    cv.save(); cv.clipRRect(rr, skia.ClipOp.kIntersect, True)
    if escuro > 0:
        cv.drawRect(skia.Rect(r[0], r[1], r[2], r[3] - CHAO_H), paint("#02060E", int(140 * escuro)))
    elif escuro < 0:                                      # entre uma noite e outra o céu clareia um pouco
        cv.drawRect(skia.Rect(r[0], r[1], r[2], r[3] - CHAO_H), paint("#6E9BD0", int(70 * -escuro)))
    if astros:
        astros(cv)
    if desenho:
        desenho(cv)
    cv.restore()
    if dia > 0.5:                                         # no céu claro, a borda (e a luz branca) precisa de um fio escuro por dentro
        cv.drawRRect(_rr((r[0] + 4, r[1] + 4, r[2] - 4, r[3] - 4), 26), paint(FUNDO_CARTAO, int(200 * (dia - 0.5) * 2), "stroke", 3))
    cv.drawRRect(rr, paint(cor, 255, "stroke", 3))
    if acende > 0:
        cv.drawRRect(rr, paint("#FFFFFF", int(200 * clamp(acende)), "stroke", 5))
    if luz > 0:
        cv.drawRRect(rr, paint("#FFFFFF", int(150 * luz), "stroke", 26, blur=14))
        cv.drawRRect(rr, paint("#FFFFFF", int(255 * luz), "stroke", 8))
    if marca and marca_a > 0:
        cv.drawRRect(rr, paint(marca, int(170 * marca_a), "stroke", 30, blur=16))
        cv.drawRRect(rr, paint(marca, int(255 * marca_a), "stroke", 9))
    if por_cima:
        por_cima(cv)
    if letra:
        selo_letra(cv, letra, r[0] + 62, r[1] + 62, cor, 1.0 + 0.35 * pulso, 1.0, badge_esc)
    cv.restore()


def canto_astro(r):
    """Onde ficam a lua e o sol: canto de cima à DIREITA (o selo da letra fica à esquerda)."""
    return r[2] - 92, r[1] + 96


# ------------------------------------------------------------------ contagem e luz (do piloto)
def em_contagem(t, T, rodada=None):
    r1 = T["cont1"] <= t < T["resp1"] - 0.12
    r2 = T["cont2"] <= t < T["resp2"] - 0.12
    return r1 if rodada == 1 else r2 if rodada == 2 else (r1 or r2)


def luz_de(t, T, letra):
    """Luz da contagem: alterna a cada 0,5 s (ritmo constante de relógio) e APAGA nos últimos 0,2 s.
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


def anel_contagem(cv, t, t0, x=540, y=811, r=90):
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
    """(do piloto) Estrelinhas douradas saindo da borda do cartão: a revelação comemora sem cobrir."""
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
    """0 -> 1 ANTES de o cartão final entrar (T['manda'] - 0,15): nada sob a CTA."""
    return prog(t, T["manda"] - 0.55, T["manda"] - 0.18)


# ------------------------------------------------------------------ rodada 1
def nevoas_r1(t, T, s):
    """As duas névoas do A (dor espalhada, nas DUAS pernas): respiram (0,75 <-> 1,0 em 1,6 s), derivam
    ±25 px e pulsam no 'dores', no 'A?' e no 'duas' (a da esquerda, e 0,08 s depois a da direita);
    no 'sumiu' encolhem e apagam em 0,4 s."""
    resp = 0.875 + 0.125 * math.sin(2 * math.pi * t / 1.6)
    some = prog(t, T["sumiu"], T["sumiu"] + 0.4)
    if some >= 1:
        return []
    out = []
    for i, x in enumerate((XE, XD)):
        dy = 25 / s * math.sin(2 * math.pi * t / 2.6 + i * 1.9)
        esc = (1 + 0.15 * bump(t, T["dores"], 0.4) + 0.15 * bump(t, T["a1"], 0.4)
               + 0.2 * bump(t, T["duas"] + 0.08 * i, 0.4)) * lerp(1.0, 0.3, e_inout(some))
        out.append((x, Y_CANELA + dy, 120, resp * (1 - some), esc))
    return out


def salto(t, T):
    """'brinca' e 'normal': os dois pés saem do chão (estica no ar, amassa ao pousar)."""
    dy, sx, sy = 0.0, 1.0, 1.0
    for t0, alt, dur in ((T["brinca"] - 0.02, 92, 0.32), (T["normal"] + 0.05, 66, 0.28)):
        u = (t - t0) / dur
        if 0 <= u <= 1:
            dy = -alt * 4 * u * (1 - u)
            q = math.sin(math.pi * u)
            sy, sx = 1 + 0.04 * q, 1 - 0.025 * q
        k = t - (t0 + dur)
        if 0 <= k < 0.1:
            q = math.sin(math.pi * k / 0.1)
            dy, sy, sx = 0.0, 1 - 0.08 * q, 1 + 0.05 * q
    return dy, sx, sy


def rodada1(cv, t, T):
    sai = e_inout(prog(t, T["agora"], T["agora"] + 0.6))
    if sai >= 1:
        return
    dx_all = -1120 * sai
    luz_a, luz_b = luz_de(t, T, "A"), luz_de(t, T, "B")

    # ---- B: DIA, pernas de perfil mancando (anda no lugar a partir de 0,40 s); sai pela direita no "Dói"
    sai_b = e_in_back(prog(t, T["doi1"], T["doi1"] + 0.45))
    if sai_b < 1:
        fi = FI0 + max(0.0, t - 0.40) / P_CICLO
        nev = 1 + 0.15 * bump(t, T["dores"], 0.4) + 0.2 * bump(t, T["b1"], 0.4)
        giro = 15 * e_inout(prog(t, T["crescimento"], T["crescimento"] + 0.45))

        def astros_b(cv):
            sol(cv, *canto_astro(CART_B), 46, 1.0, giro)

        def desenho_b(cv):
            xh, yc, s = PERFIL_B
            esteira(cv, CART_B, dist_esteira(fi, s))
            par_perfil(cv, xh, yc, s, fi, 1.0, nev, t=t)
        cartao(cv, t, CART_B, "B", COR_B, desenho_b, alfa=1 - 0.55 * prog(t, T["resp1"], T["resp1"] + 0.25),
               dx=dx_all + 760 * sai_b, rot=balanco(t, T["chuta"] + 0.14), esc=1 + 0.06 * bump(t, 0.40, 0.28),
               pulso=bump(t, T["b1"]) + 0.12 * luz_b, acende=bump(t, T["b1"], 0.45), luz=luz_b, dia=1.0,
               astros=astros_b)

    # ---- A: NOITE, pernas de frente com névoa nas duas; vira a resposta, cresce, amanhece e pula
    expande = e_inout(prog(t, T["doi1"], T["doi1"] + 0.5))
    r = tuple(lerp(a, b, expande) for a, b in zip(CART_A, LARGO)) if 0 < expande < 1 else (CART_A if expande <= 0 else LARGO)
    s = lerp(FRENTE_CART[0], FRENTE_LARGO[0], expande)
    cx = lerp(_centro(CART_A)[0], _centro(LARGO)[0], expande)
    y = lerp(FRENTE_CART[1], FRENTE_LARGO[1], expande)
    dia = e_inout(prog(t, T["manha"], T["manha"] + 0.8))
    aurora = math.sin(math.pi * dia) * prog(t, T["manha"], T["manha"] + 0.2)

    def astros_a(cv):
        x0, y0, x1, y1 = r
        lx, ly = canto_astro(r)
        k = e_inout(prog(t, T["manha"], T["manha"] + 0.55))           # a lua desce para a esquerda e some
        esc = 1 + 0.15 * bump(t, T["crescimento"], 0.4) + 0.2 * bump(t, T["noite1"], 0.55)   # (antes de chegar às pernas)
        lua(cv, lx - 150 * k, ly + 80 * k, 46 * esc, (1 - k) ** 2, brilho=bump(t, T["noite1"], 0.7))
        pis = [bump(t, T["noite1"] + 0.06 * i, 0.4) + 0.5 * bump(t, T["crescimento"] + 0.05 * i, 0.3) for i in range(4)]
        estrelas(cv, r, 1 - dia, pis)
        ks = e_out(prog(t, T["manha"] + 0.1, T["manha"] + 0.8))      # o sol nasce atrás da linha do chão
        if ks > 0:
            yc = y1 - CHAO_H
            cv.save(); cv.clipRect(skia.Rect(x0, y0, x1, yc))
            sol(cv, x1 - 140, lerp(yc + 70, y0 + 140, ks), 46, 1.0, 20 * ks)
            cv.restore()

    def desenho_a(cv):
        ct = bump(t, T["pernas"], 0.45)
        par_frente(cv, cx, y, s, nevoas_r1(t, T, s), contorno=(ct, ct), salto=salto(t, T), t=t,
                   faiscas=(t, T["sumiu"] + 0.05))

    marca_a = prog(t, T["resp1"], T["resp1"] + 0.12) * (1 - prog(t, T["doi1"], T["doi1"] + 0.4))
    cartao(cv, t, r, "A", COR_A, desenho_a, dx=dx_all, rot=balanco(t, T["chuta"]) * (1 - expande),
           esc=1 + 0.06 * bump(t, 0.30, 0.28),
           pulso=bump(t, T["a1"]) + 0.12 * luz_a + bump(t, T["resp1"], 0.45),
           acende=bump(t, T["a1"], 0.45), luz=luz_a, marca=OURO, marca_a=marca_a, dia=dia, aurora=aurora,
           astros=astros_a)
    brilhos_borda(cv, tuple(v + (dx_all if i % 2 == 0 else 0) for i, v in enumerate(CART_A)), t, T["resp1"] + 0.03)


# ------------------------------------------------------------------ rodada 2
NOITES_A = (((XE, Y_CANELA, 120), (XD, Y_CANELA, 120)),        # noite 1: as duas canelas
            ((XE, Y_COXA, 92), (XD, Y_CANELA, 120)),           # noite 2: coxa esquerda + canela direita
            ((XE, Y_BAIXO, 100), (XD, Y_BAIXO, 100)))          # noite 3: as duas panturrilhas, mais baixo


def noites(T):
    """As TRÊS NOITES do 'sempre': cada uma começa num acerto da estrela ('sempre', 'ali', 'mesmo')."""
    h = (T["sempre"], T["ali"], T["mesmo1"])
    return [(h[0] - 0.06, h[1] - 0.06), (h[1] - 0.06, h[2] - 0.06), (h[2] - 0.06, h[2] + 0.45)]


def noite_de(t, T):
    """-> (índice da noite, progresso 0..1) ou None fora das três noites."""
    for i, (a, b) in enumerate(noites(T)):
        if a <= t < b:
            return i, (t - a) / (b - a)
    return None


def ceu_noites(t, T):
    """Escurece no meio de cada noite e clareia um pouco entre elas (>0 escuro, <0 claro)."""
    n = noite_de(t, T)
    if n is None:
        return 0.0
    i, u = n
    env = prog(t, noites(T)[0][0], noites(T)[0][0] + 0.12) * (1 - prog(t, noites(T)[2][1] - 0.15, noites(T)[2][1]))
    v = math.sin(math.pi * u)
    return (0.9 * v if v > 0.35 else -0.8 * (0.35 - v) / 0.35) * env


def astros_r2(cv, t, T, r):
    """(v2) A lua dos cartões da rodada 2 fica PARADA no canto (v1 atravessava o cartão e reaparecia
    na esquerda a cada noite: lia como pisca-pisca e encostava no selo B). Cada noite é marcada pelo
    céu que escurece (ceu_noites), por um brilho da lua e pelas estrelas que piscam no começo dela."""
    lx, ly = canto_astro(r)
    ini = [a for a, _ in noites(T)]
    brilho = sum(bump(t, a, 0.4) for a in ini)
    lua(cv, lx, ly, 46 * (1 + 0.08 * brilho), 1.0, brilho=min(1.0, brilho))
    estrelas(cv, r, 1.0, [sum(bump(t, a + 0.05 * i, 0.35) for a in ini) for i in range(4)])


def nevoas_r2(t, T, s):
    """A da rodada 2: névoa nas duas pernas, que VAGA (sobe e desce, muda de altura: dor vaga) a
    partir do 'avaliação'; nas três noites reaparece em lugares DIFERENTES; depois continua vagando."""
    resp = (0.875 + 0.125 * math.sin(2 * math.pi * t / 1.6)) * lerp(1.0, 1.45, prog(t, T["resp2"], T["resp2"] + 0.25))
    amp = 70 * e_inout(prog(t, T["avaliacao1"] - 0.3, T["avaliacao1"] + 0.6))
    n = noite_de(t, T)
    out = []
    if n is not None:
        i, u = n
        a0, a1 = noites(T)[i]
        ent = e_back(prog(t, a0 + 0.04, a0 + 0.2))
        sai = prog(t, a1 - 0.07, a1) if i < 2 else 0.0
        for j, (x, y, ry) in enumerate(NOITES_A[i]):
            out.append((x, y + 20 * math.sin(2 * math.pi * t / 2.1 + j * 2.3), ry, resp * (1 - sai) * clamp(ent * 2),
                        max(0.0, lerp(0.4, 1.0, ent)) * (1 - 0.5 * sai)))
        return out
    depois = t >= noites(T)[2][1]
    base = NOITES_A[2] if depois else NOITES_A[0]
    if depois:
        amp = 45
    pul = 1 + 0.15 * bump(t, T["a2"], 0.4)
    for j, (x, y, ry) in enumerate(base):
        dy = amp * math.sin(2 * math.pi * (t - T["avaliacao1"]) / 2.4 + j * 2.2)
        out.append((x, y + dy, ry, resp, pul))
    return out


def estrela_r2(t, T):
    """B da rodada 2: UMA estrela de dor PREGADA no joelho direito. Pulsa no lugar (1,0 <-> 1,12 em
    0,8 s); nas três noites RE-ACERTA o mesmo ponto (o 'ali' é o maior pulso) e o anel branco fica
    mais forte a cada acerto (40% -> 70% -> 100%) e TRAVA no 'mesmo'. -> (escala, alfa, anel, trava)."""
    esc = 1 + 0.06 * (1 - math.cos(2 * math.pi * t / 0.8))
    esc += 0.25 * bump(t, T["b2"], 0.4) + 0.35 * bump(t, T["doi2"], 0.45)
    h = (T["sempre"], T["ali"], T["mesmo1"])
    anel, a = 0.0, 1.0
    for i, (t0, amp) in enumerate(zip(h, (0.25, 0.4, 0.25))):
        if t >= t0 - 0.1:
            mergulho = prog(t, t0 - 0.1, t0) * (1 - prog(t, t0, t0 + 0.04))     # some um instante e re-acerta
            esc *= 1 - 0.65 * mergulho
            esc += amp * bump(t, t0, 0.32)
        if t >= t0:
            anel = (0.4, 0.7, 1.0)[i] * prog(t, t0, t0 + 0.1)
    trava = prog(t, T["mesmo1"], T["mesmo1"] + 0.2)
    return esc, a, anel, trava


def lado_r2(t, T):
    """(v2) 'DE UM LADO SÓ': as DUAS pernas do B ganham contorno ao mesmo tempo, para se compararem —
    a limpa em BRANCO (5 px por fora), a da estrela em LARANJA grosso (9 px por fora, pulso de +5 no 'lado').
    O contorno fica até o 'merece' e apaga. -> (alfa, largura do contorno laranja)."""
    ct = prog(t, T["lado"] - 0.05, T["lado"] + 0.1) * (1 - prog(t, T["merece2"] + 0.05, T["merece2"] + 0.4))
    return ct, 9.0 + 5.0 * bump(t, T["lado"], 0.4)


def rodada2(cv, t, T):
    if t < T["agora"] + 0.05:
        return
    sai = e_inout(prog(t, T["bonus"] - 0.05, T["bonus"] + 0.3))
    if sai < 1:
        lift = e_back(prog(t, T["resp2"], T["resp2"] + 0.3)) if t >= T["resp2"] else 0.0
        esc_n = ceu_noites(t, T)
        s, y = FRENTE_CART
        for i, (r, letra, cor) in enumerate(((CART_A, "A", COR_A), (CART_B, "B", COR_B))):
            ent = e_inout(prog(t, T["agora"] + 0.05 * i, T["agora"] + 0.6 + 0.05 * i))
            cx, _ = _centro(r)
            t_l = T["a2"] if letra == "A" else T["b2"]
            luz = luz_de(t, T, letra)

            def astros(cv, r=r):
                astros_r2(cv, t, T, r)

            if letra == "A":
                def desenho(cv, cx=cx):
                    par_frente(cv, cx, y, s, nevoas_r2(t, T, s), t=t)
            else:
                ee, ea, an, tr = estrela_r2(t, T)
                ct, lg = lado_r2(t, T)

                def desenho(cv, cx=cx, ee=ee, ea=ea, an=an, tr=tr, ct=ct, lg=lg):
                    par_frente(cv, cx, y, s, estrela=(XD, Y_JOELHO, 64 * ee, ea, ee - 1), anel=(an, tr),
                               contorno=(ct, ct), cor_contorno=("#FFFFFF", COR_B), larg_contorno=(5.0, lg), t=t)
            comum = dict(dx=(1 - ent) * 1120, rot=balanco(t, T["contrario"] + 0.1 * i, amp=3.0, dur=0.7)
                         + balanco(t, T["avaliacao1"] + 0.14 * i), acende=bump(t, t_l, 0.45), luz=luz,
                         astros=astros, escuro=esc_n)
            if letra == "A":                              # não é a resposta: só apaga (e fica apagado)
                apaga = 0.55 * prog(t, T["resp2"], T["resp2"] + 0.25)
                cartao(cv, t, r, letra, cor, desenho, alfa=(1 - apaga) * (1 - sai),
                       esc=(1 - 0.03 * lift) * (1 - 0.15 * sai), pulso=bump(t, t_l) + 0.12 * luz, **comum)
            else:                                         # a resposta: sobe, cresce, borda da cor do B
                marca_a = prog(t, T["resp2"], T["resp2"] + 0.12) * (1 + 0.6 * bump(t, T["merece2"], 0.45))
                cartao(cv, t, r, letra, cor, desenho, alfa=1 - sai, dy=-7 * lift,
                       esc=(1 + 0.025 * lift) * (1 - 0.15 * sai) * (1 + 0.03 * bump(t, T["merece2"], 0.4)),
                       pulso=bump(t, t_l) + 0.12 * luz + 0.5 * bump(t, T["resp2"], 0.35),
                       marca=COR_B, marca_a=clamp(marca_a), badge_esc=1 + 0.3 * lift,
                       **dict(comum, acende=comum["acende"] + bump(t, T["avaliacao2"], 0.45)))
    bonus(cv, t, T)


# ------------------------------------------------------------------ BÔNUS: mancou + febre -> avalie no mesmo dia
def termometro(cv, x, y, nivel, a, esc=1.0):
    """(cópia do cf_crianca_mancando / cf_osteomielite) bulbo e coluna vermelha, SEM número."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-14, -50, 14, 26), 14, 14), paint("#000000", int(70 * a), blur=6))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-12, -48, 12, 24), 12, 12), paint("#EEF3F8", int(255 * a)))
    cv.drawCircle(0, 32, 19, paint("#EEF3F8", int(255 * a)))
    cv.drawCircle(0, 32, 13, paint(VERMELHO, int(255 * a)))
    h = lerp(6, 64, clamp(nivel))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-5, 26 - h, 5, 32), 5, 5), paint(VERMELHO, int(255 * a)))
    for k in range(4):
        cv.drawLine(5, -30 + k * 14, 11, -30 + k * 14, paint("#8FA3B8", int(220 * a), "stroke", 2))
    cv.restore()


CAL_V = 7.0                                                             # folhas por segundo


def freio_cal(t_in, t_para):
    """(do cf_crianca_mancando) -> (fase em que começa a frear, duração do freio): desacelera até uma
    folha INTEIRA; o freio mínimo é de meia folha."""
    fm = CAL_V * (t_para - t_in)
    r = math.ceil(fm) - fm
    if r < 0.5:
        r += 1.0
    return fm, 2 * r / CAL_V


def fase_cal(t, t_in, t_para):
    """-> (fase das folhas, parado?). Vira a CAL_V folhas/s de `t_in` a `t_para`; aí freia e PARA."""
    fm, d = freio_cal(t_in, t_para)
    if t < t_para:
        return CAL_V * (t - t_in), False
    u = min(t - t_para, d)
    return fm + CAL_V * u - CAL_V * u * u / (2 * d), t >= t_para + d


def calendario_parado(cv, x, y, t, t_in, t_para, t_circ, a, esc=1.5, cor_circ=COR_B):
    """(cópia do cf_crianca_mancando, com a cor e o instante do círculo como parâmetros) Folha sem
    número; vira desde `t_in`, freia em `t_para` e PARA; um círculo feito à mão se fecha na folha."""
    if a <= 0:
        return
    ent = lerp(0.6, 1.0, e_back(prog(t, t_in, t_in + 0.3)))
    cv.save(); cv.translate(x + 48 * esc, y + 46 * esc); cv.scale(esc * ent, esc * ent); cv.translate(-48, -46)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(3, 5, 99, 97), 12, 12), paint("#000000", int(80 * a), blur=8))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(0, 0, 96, 92), 12, 12), paint("#EEF3F8", int(255 * a)))
    cv.drawRect(skia.Rect(0, 0, 96, 24), paint(VERMELHO, int(255 * a)))
    for xx in (24, 72):
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(xx - 4, -8, xx + 4, 10), 3, 3), paint("#5E7186", int(255 * a)))
    for i in range(3):
        cv.drawLine(14, 42 + i * 16, 82, 42 + i * 16, paint("#9AA8B5", int(200 * a), "stroke", 4))
    fase, parado = fase_cal(t, t_in, t_para)
    if not parado:                                                      # a folha de cima virando
        f = fase - math.floor(fase)
        cv.save(); cv.translate(0, 24); cv.scale(1, 1 - f)
        cv.drawRect(skia.Rect(0, 0, 96, 68), paint("#FFFFFF", int(170 * a * (1 - f))))
        cv.restore()
    kc = prog(t, t_circ, t_circ + 0.35)
    if kc > 0:                                                          # círculo "à mão" (traço irregular)
        p = skia.Path(); n = 40
        for i in range(n + 1):
            u = i / n
            ang = -2.2 + u * 2 * math.pi * 1.08
            rr = 1 + 0.06 * math.sin(u * 11) + 0.05 * u
            px, py = 48 + 46 * rr * math.cos(ang), 58 + 30 * rr * math.sin(ang)
            (p.moveTo if i == 0 else p.lineTo)(px, py)
        cv.drawPath(p, _trim(paint(cor_circ, int(255 * a), "stroke", 6), e_out(kc)))
    cv.restore()


def t_cal(T):
    """(v2) O calendário entra e começa a virar no 'atendimento' (em v1 era no 'No', a 0,08 s do
    'mesmo' nesta voz: quase não virava); freia no 'mesmo'."""
    return T["atendimento"] + 0.05


def t_circulo(T):
    """O círculo começa quando a folha parou E a voz chegou ao 'dia'."""
    _, d = freio_cal(t_cal(T), T["mesmo2"])
    return max(T["mesmo2"] + d + 0.03, T["dia"] - 0.04)


def bonus(cv, t, T):
    """(v2) 'Bônus: mancou? Avalie. Com febre? Atendimento no mesmo dia.' No 'Bônus' entra o cartão C,
    de DIA, JÁ com as pernas de perfil PARADAS dentro (v1 ficava ~0,5 s só céu e chão: 'parece que
    travou'). No 'mancou' elas começam a mancar e a dor aparece na canela da que manca (as mesmas pernas
    do B da rodada 1: é a resposta para 'e o B?'); no 'Avalie' a MESMA marca laranja da resposta B se
    fecha em volta; no 'febre' o termômetro; no 'atendimento' a marca pulsa; no 'no mesmo dia' o
    calendário que freia e PARA, e o círculo laranja."""
    ent = prog(t, T["bonus"] + 0.18, T["bonus"] + 0.55)          # entra quando A e B já saíram
    if ent <= 0:
        return
    a = clamp(ent * 2.5) * (1 - saida_final(t, T))
    if a <= 0:
        return
    e = e_back(ent)
    fecha = prog(t, T["avalie"] - 0.05, T["avalie"] + 0.2)
    cx, cy = _centro(CART_C)

    def astros(cv):
        sol(cv, *canto_astro(CART_C), 46, 1.0, 15)
        k = prog(t, t_cal(T) - 0.13, t_cal(T) + 0.07)
        if k > 0:
            cv.save(); cv.translate(0, -70 * (1 - e_out(k)))
            calendario_parado(cv, 322, 442, t, t_cal(T), T["mesmo2"], t_circulo(T), clamp(k * 2), esc=1.5)
            cv.restore()

    def desenho(cv):
        xh, yc, s = PERFIL_C
        fi = FI0 + max(0.0, t - (T["mancou"] - 0.05)) / P_CICLO          # paradas até o "mancou"
        esteira(cv, CART_C, dist_esteira(fi, s))
        dor = prog(t, T["mancou"] - 0.05, T["mancou"] + 0.2)
        par_perfil(cv, xh, yc, s, fi, dor, 1 + 0.25 * bump(t, T["mancou"] + 0.1, 0.4), t=t)
        kt = prog(t, T["febre"] - 0.05, T["febre"] + 0.3)
        if kt > 0:                                           # o termômetro desliza para a direita das pernas
            nivel = lerp(0.08, 1.0, e_inout(prog(t, T["febre"] + 0.1, T["febre"] + 0.6)))
            esc = 2.2 * (1 + 0.08 * bump(t, T["febre"] + 0.55, 0.3))
            termometro(cv, lerp(860, 722, e_out(kt)), 758, nivel, clamp(kt * 3), esc)

    esc = lerp(0.82, 1.0, e) * (1 + 0.035 * bump(t, T["avalie"], 0.35) + 0.03 * bump(t, T["atendimento"], 0.4))
    cartao(cv, t, CART_C, None, "#FFFFFF", desenho, alfa=a, esc=esc, dy=40 * (1 - e), dia=1.0, astros=astros,
           marca=COR_B, marca_a=fecha, acende=bump(t, T["bonus"] + 0.3, 0.4) + bump(t, T["atendimento"], 0.45))
    if 0 < fecha < 1:                                     # a marca FECHA: um contorno que encolhe até a borda
        g = lerp(1.14, 1.0, e_out(fecha))
        cv.save(); cv.translate(cx, cy); cv.scale(g, g); cv.translate(-cx, -cy)
        cv.drawRRect(_rr(CART_C), paint(COR_B, int(220 * a * (1 - fecha)), "stroke", 9))
        cv.restore()


# ------------------------------------------------------------------ topo: gancho, selo da série, rodada (do piloto)
def capa_jogo(cv, t, T, l1, l2):
    """Gancho de 2 linhas, cada linha pulsa quando é dita ('dores' / 'crescimento'). FICA durante a
    contagem (é a pergunta) e sai para CIMA na resposta, antes de o selo entrar."""
    sai = e_inout(prog(t, T["resp1"], T["resp1"] + 0.3))
    if sai >= 1:
        return
    a = 1 - sai
    cv.drawRect(skia.Rect(0, 0, W, 360), paint(BG_OUT, 255, shader=skia.GradientShader.MakeLinear(
        [skia.Point(0, 0), skia.Point(0, 360)], [C(BG_OUT, int(235 * a)), C(BG_OUT, 0)])))
    pulso = 1 + 0.025 * math.sin(t * 5)
    cv.save(); cv.translate(CX, 205 - 170 * sai); cv.scale(pulso, pulso)
    for y, s, cor, t0 in ((0, l1, "#FFFFFF", T["dores"]), (88, l2, OURO, T["crescimento"])):
        e = 1 + 0.06 * bump(t, t0, 0.35)
        cv.save(); cv.translate(0, y - 28); cv.scale(e, e)
        texto(cv, s, 0, 28, F_BLACK, 78, cor, int(255 * a), contorno=10)
        cv.restore()
    cv.restore()


def selo_serie(cv, a):
    if a <= 0:
        return
    rr = skia.RRect.MakeRectXY(skia.Rect(CX - 190, 150, CX + 190, 204), 27, 27)
    cv.drawRRect(rr, paint("#FFFFFF", int(28 * a)))
    texto(cv, "QUAL DOS DOIS?", CX, 190, F_BLACK, 32, OURO, int(255 * a))


def pilula(cv, t, T):
    """'2 RODADAS' na capa; 'RODADA 1' / 'RODADA 2' com bolinhas de placar; 'BÔNUS' no fim."""
    a = 1 - saida_final(t, T)
    if a <= 0:
        return
    if t < T["cont1"]:
        s, n, t0 = "2 RODADAS", 0, 0.05
    elif t < T["agora"]:
        s, n, t0 = "RODADA 1", 1, T["cont1"]
    elif t < T["bonus"]:
        s, n, t0 = "RODADA 2", 2, T["agora"]
    else:
        s, n, t0 = "BÔNUS", 2, T["bonus"]
    esc = 1 + 0.15 * bump(t, t0, 0.3) + 0.18 * bump(t, T["contrario"], 0.35)
    tam = 32; lw = skia.Font(F_BLACK, tam).measureText(s)
    larg = lw + 36 + 18 + 2 * 22
    cv.save(); cv.translate(CX, 346); cv.scale(esc, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-larg / 2, -24, larg / 2, 24), 24, 24)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(225 * a)))
    cv.drawRRect(rr, paint(OURO, int(200 * a), "stroke", 2.5))
    texto(cv, s, -larg / 2 + 18, 11, F_BLACK, tam, "#FFFFFF", int(255 * a), centro=False)
    for k in range(2):
        x = -larg / 2 + 18 + lw + 18 + 11 + 22 * k
        if n > k:
            cv.drawCircle(x, 0, 8, paint(OURO, int(255 * a)))
        else:
            cv.drawCircle(x, 0, 7, paint("#FFFFFF", int(170 * a), "stroke", 2.5))
    cv.restore()


# ------------------------------------------------------------------ CTA: os dois cartões da RODADA 1 em miniatura
def minis(cv, t, T):
    k = prog(t, T["manda"] + 0.05, T["manda"] + 0.45)
    if k <= 0:
        return
    e = e_back(k)
    s, y = FRENTE_CART
    for i, (r, letra, cor, x) in enumerate(((CART_A, "A", COR_A, 458), (CART_B, "B", COR_B, 622))):
        cx, cy = _centro(r)
        rot = balanco(t, T["duvida"] + 0.13 * i, amp=4.0, dur=0.9)
        cv.save(); cv.translate(x, 368); cv.rotate(rot); cv.scale(0.28 * e, 0.28 * e); cv.translate(-cx, -cy)
        if letra == "A":
            def astros(cv, r=r):
                lua(cv, *canto_astro(r), 46, 1.0); estrelas(cv, r, 1.0)

            def desenho(cv, cx=cx):
                par_frente(cv, cx, y, s, [(XE, Y_CANELA, 120, 1.0, 1.0), (XD, Y_CANELA, 120, 1.0, 1.0)], t=t)
            dia = 0.0
        else:
            def astros(cv, r=r):
                sol(cv, *canto_astro(r), 46, 1.0, 15)

            def desenho(cv):
                xh, yc, sp = PERFIL_B
                esteira(cv, CART_B, dist_esteira(FI0, sp))
                par_perfil(cv, xh, yc, sp, FI0, t=t)
            dia = 1.0
        cartao(cv, t, r, letra, cor, desenho, alfa=clamp(k * 3), badge_esc=1.75, dia=dia, astros=astros)
        cv.restore()


# ------------------------------------------------------------------ quadro
def juntar_palpite(blocos):
    """(v2) Junta 'CHUTA:' + 'A?' + 'OU B?' (e, na rodada 2, 'A?' + 'OU B?') num bloco só do karaokê.
    Em v1 o 'A?' ficava SOZINHO na tela, em ouro, logo antes da contagem — o leitor às cegas achou que
    a legenda já tinha entregado a resposta. Com as duas opções juntas, nunca sobra uma letra só."""
    out = []
    for b in blocos:
        if out and ((out[-1][-1]["tok"].lower() == "chuta:" and b[0]["tok"] == "A?")
                    or (out[-1][-1]["tok"] == "A?" and b[0]["tok"].lower() == "ou")):
            out[-1] = out[-1] + b
        else:
            out.append(list(b))
    n = sum(1 for b in out if [p["tok"] for p in b][-3:] == ["A?", "Ou", "B?"])
    if n != 2:
        raise SystemExit(f"ERRO: o karaokê devia ter 2 blocos '... A? OU B?' (achei {n}).")
    return out


def pergunta_fixa(blocos, T):
    """O bloco da pergunta da rodada 2 ('QUAL DOS DOIS / MERECE AVALIAÇÃO?'), esticado para ficar na
    tela durante a contagem (quem vê sem som sabe o que está chutando)."""
    for b in blocos:
        if any(abs(p["t"] - T["avaliacao1"]) < 1e-6 for p in b):
            ult = dict(b[-1], d=max(b[-1]["d"], T["resp2"] - b[-1]["t"]))
            return b[:-1] + [ult]
    raise SystemExit("ERRO: bloco da pergunta da rodada 2 não achado.")


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
    ev = [(0.05, "pop", 0.5), (0.30, "pop", 0.45), (0.40, "pop", 0.4),
          (T["dores"], "tick", 0.3), (T["crescimento"], "shimmer", 0.3),
          (T["chuta"], "whoosh", 0.25), (T["a1"], "pop", 0.6), (T["b1"], "pop", 0.6)]
    for t0 in (T["cont1"], T["cont2"]):                          # tique-taque constante
        ev += [(t0 + 0.5 * i, "tick" if i % 2 == 0 else "click", 0.75 if i % 2 == 0 else 1.0) for i in range(4)]
    ev += [(T["resp1"], "ding", 0.45), (T["doi1"], "whoosh", 0.4),
           (T["duas"], "pop", 0.5), (T["duas"] + 0.08, "pop", 0.45), (T["pernas"], "tick", 0.3),
           (T["noite1"], "shimmer", 0.3), (T["manha"], "whoosh", 0.3), (T["manha"] + 0.05, "shimmer", 0.4),
           (T["sumiu"], "pop", 0.5), (T["brinca"] - 0.02, "pop", 0.6), (T["brinca"] + 0.30, "thump", 0.3),
           (T["normal"] + 0.05, "pop", 0.5), (T["normal"] + 0.33, "thump", 0.22),
           (T["agora"], "whoosh", 0.5), (T["agora"] + 0.05, "pop", 0.4), (T["contrario"], "thump", 0.4),
           (T["a2"], "pop", 0.6), (T["b2"], "pop", 0.6),
           (T["resp2"], "thump", 0.65), (T["resp2"] + 0.02, "pop", 0.5), (T["doi2"], "tick", 0.6),
           (T["sempre"], "pop", 0.45), (T["ali"], "pop", 0.45), (T["mesmo1"], "pop", 0.45),
           (T["mesmo1"] + 0.03, "shimmer", 0.35), (T["lado"], "tick", 0.5), (T["merece2"], "pop", 0.45),
           (T["bonus"] - 0.05, "whoosh", 0.35), (T["bonus"] + 0.2, "pop", 0.45), (T["mancou"], "pop", 0.55),
           (T["avalie"], "thump", 0.6), (T["avalie"] + 0.02, "pop", 0.5),
           (T["febre"], "tick", 0.6), (T["febre"] + 0.1, "shimmer", 0.3), (T["atendimento"], "pop", 0.45),
           (T["mesmo2"], "click", 0.6), (T["dia"], "pop", 0.5),
           (T["manda"] + 0.05, "whoosh", 0.5), (T["duvida"], "pop", 0.4)]
    return ev


def janelas(T):
    return [(T["cont1"], T["cont1"] + CONTAGEM), (T["cont2"], T["cont2"] + CONTAGEM)]


def _media_movel(x, w):
    """(do piloto) = np.convolve(x, np.ones(w) / w, "same"), por soma acumulada."""
    xp = np.concatenate([np.zeros(w // 2), x, np.zeros((w - 1) // 2)])
    c = np.concatenate([[0.0], np.cumsum(xp)])
    return (c[w:w + len(x)] - c[:len(x)]) / w


def mixar_jogo(voz, dur, eventos, jan, ganho_trilha=0.40, fundo_contagem=0.15, rampa=0.15):
    """(do piloto) Como som.mixar (ducking pela voz, efeitos), mais um envelope que baixa a trilha
    para ~15% nas janelas de contagem (rampa de 0,15 s): o tique-taque fica sozinho."""
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
    return (0.0, T["dores"] + 0.3, T["b1"] + 0.2, T["cont1"] + 1.2, T["resp1"] + 0.5, T["duas"] + 0.4,
            T["manha"] + 0.6, T["brinca"] + 0.25, T["contrario"] + 0.3, T["cont2"] + 1.7, T["resp2"] + 0.3,
            T["mesmo1"] + 0.3, T["lado"] + 0.2, T["merece2"] + 0.3, T["bonus"] + 0.35, T["mancou"] + 0.3,
            T["avalie"] + 0.25, T["febre"] + 0.4, T["atendimento"] + 0.3, T["dia"] + 0.3, T["manda"] + 0.8,
            T["total"] - 0.1)


def preparar(ep, tmp):
    roteiro = "\n".join(ep["roteiro"])
    voz_bruta, palavras = _voz.narrar(roteiro, _voz.RITMO_COMO_FUNCIONA, os.path.join(tmp, "voz"))
    voz_c, pal, tirado = comprimir(voz_bruta, palavras, respiro_cta=0.6)
    pal = alinhar(pal, roteiro)
    voz_c, pal, conts = inserir_contagens(voz_c, pal)
    T = ancoras_jogo(pal, ANCORAS)
    T["cont1"], T["cont2"] = conts
    if not (T["chuta"] < T["cont1"] < T["resp1"] < T["agora"] < T["cont2"] < T["resp2"] < T["sempre"]
            < T["mesmo1"] < T["lado"] < T["merece2"] < T["bonus"] < T["mancou"] < T["avalie"] < T["febre"]
            < T["atendimento"] < T["no2"] < T["mesmo2"] < T["dia"] < T["manda"]):
        raise SystemExit("ERRO: ordem do jogo fora do roteiro (rodada 1 -> rodada 2 -> bônus -> CTA).")
    return voz_c, pal, T, tirado


def render(ep, mp4, tmp, previa=False):
    voz_c, pal, T, tirado = preparar(ep, tmp)
    print(f"{ep['id']}: silêncio cortado {tirado:.2f}s | contagens em {T['cont1']:.2f}s e {T['cont2']:.2f}s"
          f" | duração final {T['total']:.2f}s")
    blocos = juntar_palpite(montar_blocos(pal))
    T["_pergunta2"] = pergunta_fixa(blocos, T)

    def quadro_t(cv, t):
        quadro(cv, t, T, blocos, ep)

    if previa:
        return _previas(quadro_t, tempos_previa(T), tmp, ep["id"]), T["total"]
    wav = os.path.join(tmp, f"{ep['id']}_mix.wav")
    som.gravar_wav(wav, mixar_jogo(voz_c, T["total"], sons(T), janelas(T)))
    codificar(quadro_t, T["total"], wav, mp4)
    return mp4, T["total"]
