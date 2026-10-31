# -*- coding: utf-8 -*-
"""CHAMA O VAR — "SENTAR EM W: / PODE OU NÃO PODE?" (os primeiros anos), episódio da série.

Mesma linguagem do piloto cf_chamaovar_rotina_fixador e dos episódios aprovados (cf_var_primeiros_socorros,
cf_var_gesso): selo VAR + chip, ritual lance -> "pode?"/congela -> CHECANDO -> carimbo -> porquê mostrado ->
JEITO CERTO; paleta ardósia/ciano/âmbar/verde; TV que desliga; apito que passa adiante; CTA de envio. Os
helpers do piloto e dos dois episódios foram COPIADOS para cá (nenhum arquivo existente de animado/ foi
editado). A criança parte do bebê do cf_andador (COPIADO e adaptado: camiseta verde-água, bermuda azul,
cabeça lisa com topete, sem rosto), agora com pernas articuladas — e SEM andador em cena.

Storyboard: lab/formato_novo/cf_var_andar/storyboard.json (10 cenas, 40 fontes). v2 (31/10): corrigido pelo
leitor às cegas e pelo revisor — ver "v2" abaixo.
  1. "Sentar em W: pode?" -> VALIDADO + DE VEZ EM QUANDO. Quadro 0 = o lance JÁ CONGELADO: a criança sentada
     em W no tapete de EVA, vista de frente e de cima, o W TRAÇADO em ciano sobre as pernas (traço, não letra),
     círculo e pausa; "VAR" rebobina (ela volta a ficar de pé com o bloco); "Sentar" desce; "W" o traço corre;
     "pode?" congela. "de vez em quando": folheado (cruzada, de lado, W = variar). "não vira deformidade": ela
     levanta SOZINHA do W (nenhum adulto, nenhuma bola) e anda dois passos; o traço do W segue as pernas que
     se esticam e fica verde, contorno verde nas pernas retas; o chip continua VALIDADO (o jeito certo NÃO é
     tirá-la do W). "Só senta assim?": três mini-quadros, os três em W com o W traçado em cada um;
     "consulta": o busto da profissional de saúde com o apito na mão, anel verde.
  2. "Comparar com o filho do vizinho que andou antes: pode?" -> ANULADO. Dois quintais divididos por uma
     cerquinha baixa; a nossa criança em pé apoiada no sofá da varanda, o vizinho (camiseta listrada, cabelo
     curtinho) dando passos soltos À FRENTE (mais perto da câmera). "Comparar": a LINHA DE IMPEDIMENTO — uma
     linha no pé da frente de cada criança e a faixa ciano no vão entre elas (a "vantagem" medida). O círculo
     no vizinho só existe em "vizinho" e sai no congelado; no CHECANDO quem pulsa é a FAIXA. "Anulado": o
     carimbo cai NA FAIXA, entre as duas, na altura da cerca (nunca em gente), a faixa racha dos dois lados e
     apaga; "ritmo": a cerca vira duas raias, cada uma com o seu pulso; "individual": as duas raias acendem —
     NINGUÉM sai do quadro; replay JEITO CERTO (sem fala e sem legenda): palminhas baixas e um passo de lado.
  3. "Treinar e cair, em espaço seguro: pode?" -> VALIDADO + ESPAÇO SEGURO. Sala de chão livre (tapete grande
     areia, móveis na parede, protetor de quina, brinquedos no cesto); passos bambos com o arco ciano de
     oscilação; "seguro": contorno no tapete e na quina protegida; "pode?": congela no MEIO da sentada, no ar;
     "Validado": senta de bumbum no tapete ('fofo', nunca cômico) e levanta sozinha; "cada queda": replay ▶▶
     com DOIS tombos de bumbum no tapete (o 1º em "queda") e o arco estreitando a cada levantada (12 -> 7,5 ->
     3,5); "equilíbrio": de pé firme, o arco fica verde (o leque some quando estreito: nada sobre a cabeça).
  Fim: apito final, a TV desliga; no monitor escuro cada sinal âmbar (sem texto, sem número) entra GRANDE no
  centro na sua fala (com a legenda que o diz) e depois encolhe para a fileira do alto: calendário que vira,
  a criança de pé que vira fantasma tracejado + a estrela que apaga, as marquinhas de tombo que crescem, as
  pegadas com a marca sempre no MESMO pé; "avaliação": a fileira dos 4 fica acima da profissional (anel verde,
  apito); selo CHAMA O VAR.
  v2 — legenda: a pergunta "pode?" sai INTEIRA num bloco (até 3 linhas, letra 64); o sinal "ou tropeçar sempre
  do mesmo lado" num bloco só; os carimbos nunca passam da borda da tela (nem na batida).
Guardrails: crianças sem rosto, sempre vestidas, pele opaca de desenho; nenhuma perna torta, nenhum
machucado, choro ou queda de cabeça (o tombo é sentar de bumbum no tapete); nenhum exame nem osso; nenhum
cartão; o veredito do lance 2 cai na faixa da comparação, nunca em pessoa; nenhum adulto identificável (só
antebraço e mão, manga teal); nenhum andador; nenhum número/idade escrito; âmbar só em carimbo e pictogramas.
Todo texto desenhado está em ep["tela"] (o render recusa o vídeo se não estiver). Cena PRESA ao roteiro pelas
palavras-âncora (roteiro sem elas = KeyError).

Render próprio (cópia do fazer_render_var dos episódios): só INSERE silêncio — vão de CHECANDO depois de cada
"pode?", vão antes de "Comparar" (o anel verde respira antes do LANCE 2), antes de "Treinar" (o replay do
jeito certo do lance 2, sem fala, 1,15 s) e antes do 2º "não" (apito final + TV desligando), e 0,25 s de apito
antes da 1ª palavra.
"""
import math
import os

import numpy as np
import skia

from . import som, voz as _voz
from .base import codificar, previas as _previas
from .cf_alongamento import (BG_OUT, CX, F_BLACK, F_REG, F_SEMI, H, OURO, W, aviao, clamp, e_back, e_inout,
                             e_out, larg_texto, lerp, lerpc, paint, prog, texto)
from .cf_comum import DISC, SIG
from .cf_fratura_cola import alinhar, comprimir

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    # lance 1 — sentar em W
    "chama": ("chama", 1, False), "var": ("var", 1, False), "sentar": ("sentar", 1, False), "w": ("w", 1, False),
    "pode1": ("pode", 1, False), "validado1": ("validado", 1, False), "vez": ("vez", 1, False),
    "quando": ("quando", 1, False), "nao1": ("não", 1, False), "deformidade": ("deformidade", 1, False),
    "so": ("só", 1, False),
    "assim": ("assim", 1, False), "comenta": ("comenta", 1, False), "consulta": ("consulta", 1, False),
    # lance 2 — comparar com o filho do vizinho
    "comparar": ("comparar", 1, False), "vizinho": ("vizinho", 1, False), "andou": ("andou", 1, False),
    "pode2": ("pode", 2, False), "anulado": ("anulado", 1, False), "ritmo": ("ritmo", 1, False),
    "individual": ("individual", 1, False),
    # lance 3 — treinar e cair
    "treinar": ("treinar", 1, False), "cair1": ("cair", 1, False), "espaco": ("espaço", 1, False),
    "seguro": ("seguro", 1, False), "pode3": ("pode", 3, False), "validado2": ("validado", 2, False),
    "cada1": ("cada", 1, False), "queda": ("queda", 1, False), "equilibrio": ("equilíbrio", 1, False),
    # fecho
    "nao2": ("não", 2, False), "meses": ("meses", 1, False), "perder": ("perder", 1, False),
    "fazia": ("fazia", 1, False), "cair2": ("cair", 2, False), "tropecar": ("tropeçar", 1, False),
    "lado": ("lado", 1, False), "avaliacao": ("avaliação", 1, False), "manda": ("manda", 1, False),
}
FIM_DE = ("w", "pode1", "pode2", "pode3", "deformidade", "consulta", "individual", "equilibrio", "avaliacao",
          "seguro", "andou", "meses", "fazia", "lado")
DESTAQUE = {"var", "w", "deformidade", "consulta", "vizinho", "individual", "seguro", "equilíbrio", "avaliação"}

# rótulos (todos estão em ep["tela"])
T_VAR = "VAR"
T_LANCE = ("LANCE 1", "LANCE 2", "LANCE 3")
T_CHEC = "CHECANDO"
T_ANUL = "ANULADO"
T_VALID = "VALIDADO"
T_VEZ = "DE VEZ EM QUANDO"
T_SEGURO = "ESPAÇO SEGURO"
T_CERTO = "JEITO CERTO"
T_SERIE = "CHAMA O VAR"

# ------------------------------------------------------------------ paleta (a da série)
ARD_IN, ARD_OUT = "#22303F", "#121A24"
CIANO = "#4FD1FF"
VERDE = "#3DDC84"
AMBAR = "#FFA53A"
CARTAO = "#0B1824"
SELO_BG = "#1E2A44"
TEAL = "#5FC4B6"
PELE_AD = ("#B98163", "#D9A07F", "#E8B998", "#D9A07F", "#B98163"); LINHA_AD = "#9A6648"
MANGA_AD = ("#3E9C90", "#5FC4B6", "#84D6CB", "#5FC4B6", "#3E9C90"); MANGA_LINHA = "#2E7A70"     # manga teal


def _tons(c, cl, esc):
    return (esc, c, cl, c, esc)


# a criança (= o bebê do cf_andador: pele, verde-água e cabelo) e a do vizinho
PELE_LINHA = "#B9765E"
TONS_PELE = _tons("#F0B49A", "#F7CDB8", "#DA987E")
EST_NOSSA = dict(pele=TONS_PELE, pele_linha=PELE_LINHA,
                 camisa=_tons("#6FC7B1", "#9EE0CF", "#3F9A85"), camisa_linha="#2C7464",
                 bermuda=_tons("#4C86C6", "#6FA3DA", "#2F5E94"), bermuda_linha="#24507F",
                 cabelo="#4A3426", penteado="topete")
EST_VIZ = dict(pele=_tons("#9C6544", "#B67D58", "#7E4F33"), pele_linha="#5E3A24",
               camisa=_tons("#F7A866", "#FBC795", "#D9853F"), camisa_linha="#9A5A26", listras="#FFF4E6",
               bermuda=_tons("#8C7FC0", "#ADA2DA", "#675A9C"), bermuda_linha="#4E437E",
               cabelo="#2B211C", penteado="curto")     # camiseta laranja-clara LISTRADA (lê como roupa); cabelo curtinho

# sala
PAREDE_A, PAREDE_B = "#EDE6DA", "#DBD1C2"
RODAPE = "#F7F4EE"
PISO_A, PISO_B, PISO_LINHA = "#D3AE86", "#BE956C", "#A47D57"
SOFA, SOFA_CL, SOFA_ESC = "#3F516B", "#566B88", "#2C3A4E"
ALMOF, ALMOF_CL, ALMOF_ESC = "#7EA6CF", "#A3C2E2", "#5A80A8"
EVA = ("#F2C14E", "#6FC7B1", "#F08A7A", "#7EA6CF", "#B3A5DD")
AREIA, AREIA_CL, AREIA_ESC = "#E3D3B3", "#EFE4CC", "#C9B48E"
MESA, MESA_CL, MESA_ESC = "#B88A5E", "#CFA478", "#8E6646"
PROTETOR = "#DDF2FF"
CESTO, CESTO_ESC = "#C99A5B", "#9C7340"
CUBOS = ("#E8604C", "#F2C14E", "#4C86C6", "#5CB85C")
# quintais
CEU_A, CEU_B = "#9FD3F2", "#DDEFF8"
GRAMA_A, GRAMA_B, FAIXA_GRAMA = "#86C46A", "#4F9A41", "#97CF7A"
MADEIRA, MADEIRA_CL, MADEIRA_ESC = "#B98A5C", "#D2A576", "#8C6440"
DECK, DECK_LINHA = "#C9A27A", "#A47D57"

# ------------------------------------------------------------------ o monitor (janela da cena) — igual ao piloto
JX0, JY0, JX1, JY1 = 28.0, 300.0, 1052.0, 1226.0
JCX, JCY = (JX0 + JX1) / 2, (JY0 + JY1) / 2
JAN = skia.Rect(JX0, JY0, JX1, JY1)
JAN_R = 26


# ------------------------------------------------------------------ utilidades (cópias do piloto)
def _c(h, a=255):
    h = h.lstrip("#")
    return skia.ColorSetARGB(int(a), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def esc_cor(h, k):
    return lerpc(h, "#000000", k)


def janela(t, t0, t1, d_in=0.25, d_out=0.3):
    return prog(t, t0, t0 + d_in) * (1 - prog(t, t1, t1 + d_out))


def uniao(*ps):
    out = ps[0]
    for q in ps[1:]:
        out = skia.Op(out, q, skia.PathOp.kUnion_PathOp) or out
    return out


def rr_path(x0, y0, x1, y1, r):
    p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), r, r)); return p


def oval_path(x0, y0, x1, y1):
    p = skia.Path(); p.addOval(skia.Rect(x0, y0, x1, y1)); return p


def poli(pts, fechar=True):
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if fechar:
        p.close()
    return p


def suave(pts, fechar=True):
    n = len(pts)
    p = skia.Path()
    if fechar:
        m0 = ((pts[-1][0] + pts[0][0]) / 2, (pts[-1][1] + pts[0][1]) / 2)
        p.moveTo(*m0)
        for i in range(n):
            a_, b_ = pts[i], pts[(i + 1) % n]
            p.quadTo(a_[0], a_[1], (a_[0] + b_[0]) / 2, (a_[1] + b_[1]) / 2)
        p.close()
    else:
        p.moveTo(*pts[0])
        for i in range(1, n - 1):
            a_, b_ = pts[i], pts[i + 1]
            p.quadTo(a_[0], a_[1], (a_[0] + b_[0]) / 2, (a_[1] + b_[1]) / 2)
        p.lineTo(*pts[-1])
    return p


def capsula(p0, p1, w0, w1):
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]; L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    p = poli([(p0[0] + nx * w0 / 2, p0[1] + ny * w0 / 2), (p1[0] + nx * w1 / 2, p1[1] + ny * w1 / 2),
              (p1[0] - nx * w1 / 2, p1[1] - ny * w1 / 2), (p0[0] - nx * w0 / 2, p0[1] - ny * w0 / 2)])
    c0 = skia.Path(); c0.addCircle(p0[0], p0[1], w0 / 2)
    c1 = skia.Path(); c1.addCircle(p1[0], p1[1], w1 / 2)
    return uniao(p, c0, c1)


def pinta(cv, path, p0, p1, w, tons, a, linha=None, larg_linha=2.5):
    """Preenche com sombreado cilíndrico perpendicular ao eixo p0->p1 (cópia do piloto)."""
    if a <= 0:
        return
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]; L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    g0 = skia.Point(mx - nx * w * 0.62, my - ny * w * 0.62); g1 = skia.Point(mx + nx * w * 0.62, my + ny * w * 0.62)
    sh = skia.GradientShader.MakeLinear([g0, g1], [_c(c) for c in tons], [0.0, 0.2, 0.48, 0.8, 1.0])
    cv.drawPath(path, paint(tons[1], int(255 * a), shader=sh))
    if linha:
        cv.drawPath(path, paint(linha, int(200 * a), "stroke", larg_linha))


def ponta(cv, x, y, ang, tam, cor, a):
    p = skia.Path()
    p.moveTo(x + tam * math.cos(ang), y + tam * math.sin(ang))
    p.lineTo(x + tam * 0.75 * math.cos(ang + 2.45), y + tam * 0.75 * math.sin(ang + 2.45))
    p.lineTo(x + tam * 0.75 * math.cos(ang - 2.45), y + tam * 0.75 * math.sin(ang - 2.45))
    p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))


def _trim(pt, k):
    if k < 0.999:
        pe = skia.TrimPathEffect.Make(0.0, max(0.002, k))
        if pe is not None:
            pt.setPathEffect(pe)
    return pt


def lerp2(p, q, k):
    return (lerp(p[0], q[0], k), lerp(p[1], q[1], k))


def lerp3(p, q, k):
    return tuple(lerp(p[i], q[i], k) for i in range(len(p)))


_CACHE = {}
LINEAR = skia.SamplingOptions(skia.FilterMode.kLinear)


def cacheado(chave, w, h, desenha):
    if chave not in _CACHE:
        sf = skia.Surface(int(w), int(h)); c = sf.getCanvas(); c.clear(skia.ColorTRANSPARENT)
        desenha(c)
        _CACHE[chave] = sf.makeImageSnapshot()
    return _CACHE[chave]


def aplica(cv, cam):
    s, fx, fy = cam
    cv.translate(JCX, JCY); cv.scale(s, s); cv.translate(-fx, -fy)


def na_tela(cam, x, y):
    s, fx, fy = cam
    return JCX + (x - fx) * s, JCY + (y - fy) * s


def polilinha_parcial(pts, k):
    """O trecho [0, k] (fração do comprimento) de uma polilinha: (path, ponta)."""
    Ls = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
    alvo = sum(Ls) * clamp(k)
    p = skia.Path(); p.moveTo(*pts[0]); acc = 0.0
    for (a, b), l in zip(zip(pts, pts[1:]), Ls):
        if acc + l >= alvo:
            u = (alvo - acc) / l if l else 0.0
            q = lerp2(a, b, u); p.lineTo(*q)
            return p, q
        p.lineTo(*b); acc += l
    return p, pts[-1]


# ================================================================== A CRIANÇA (de frente; do bebê do cf_andador)
# Coordenadas LOCAIS: origem = o chão sob a pelve (onde o bumbum encosta quando ela senta); y para baixo; de pé
# ela tem ~490 de altura. A pose dá a pelve, os joelhos, os tornozelos, o vetor de cada pé (tornozelo -> ponta)
# e as mãos; o tronco gira `inc` graus em volta da pelve. E = lado esquerdo da TELA, D = direito.
OMBRO_L = (70.0, -150.0)            # ombro relativo à pelve (antes de girar)
QUADRIL_L = (34.0, 22.0)            # junta do quadril relativa à pelve
CABECA_DY, CABECA_R = -246.0, 76.0
L_BR = 58.0                          # braço e antebraço


def P(**kw):
    """Pose: completa com a criança de pé, braços soltos."""
    base = dict(pel=(0.0, -170.0), inc=0.0, giro=0.0, kE=(-36.0, -92.0), kD=(36.0, -92.0),
                aE=(-38.0, -30.0), aD=(38.0, -30.0), pE=(-14.0, 12.0), pD=(14.0, 12.0),
                mE=(-98.0, -212.0), mD=(98.0, -212.0), bloco=0.0, ordem="coxa", cotE=1.0, cotD=1.0)
    base.update(kw)
    return base


PE = P()
PE_BLOCO = P(mE=(-32.0, -236.0), mD=(32.0, -236.0), bloco=1.0)
AGACHA = P(pel=(0.0, -104.0), kE=(-66.0, -44.0), kD=(66.0, -44.0), aE=(-42.0, -28.0), aD=(42.0, -28.0),
           mE=(-60.0, -128.0), mD=(60.0, -128.0))
W_SENTA = P(pel=(0.0, -46.0), kE=(-56.0, 64.0), kD=(56.0, 64.0), aE=(-138.0, -4.0), aD=(138.0, -4.0),
            pE=(-48.0, -8.0), pD=(48.0, -8.0), mE=(-30.0, -92.0), mD=(30.0, -92.0), cotE=1.0, cotD=1.0)
W_BLOCO = dict(W_SENTA, bloco=1.0)
CRUZADA = P(pel=(0.0, -46.0), kE=(-122.0, 18.0), kD=(122.0, 18.0), aE=(36.0, 58.0), aD=(-36.0, 50.0),
            pE=(30.0, 4.0), pD=(-30.0, 4.0), mE=(-84.0, -64.0), mD=(84.0, -64.0), ordem="canela")
DE_LADO = P(pel=(-12.0, -46.0), inc=-5.0, kE=(18.0, 62.0), kD=(86.0, 44.0), aE=(142.0, 18.0), aD=(160.0, -12.0),
            pE=(34.0, -2.0), pD=(32.0, -10.0), mE=(-112.0, -40.0), mD=(70.0, -70.0))
W_GIRO = dict(W_SENTA, inc=7.0, giro=0.55, mD=(150.0, -96.0), mE=(-20.0, -96.0))
SENTADA = P(pel=(0.0, -46.0), kE=(-120.0, 10.0), kD=(120.0, 10.0), aE=(-58.0, 66.0), aD=(58.0, 66.0),
            pE=(24.0, 8.0), pD=(-24.0, 8.0), mE=(-124.0, -40.0), mD=(124.0, -40.0), ordem="canela")   # sentada no tapete
ABERTO = P(mE=(-178.0, -296.0), mD=(178.0, -296.0))
NO_AR = P(pel=(0.0, -126.0), kE=(-112.0, -82.0), kD=(112.0, -82.0), aE=(-96.0, -8.0), aD=(100.0, -30.0),
          pE=(4.0, 18.0), pD=(-2.0, 14.0), mE=(-150.0, -336.0), mD=(172.0, -308.0))   # o bumbum a um palmo do tapete
NO_SOFA = P(inc=-3.0, mE=(-150.0, -196.0), mD=(96.0, -210.0))


def mix(p, q, u):
    out = {}
    for k_, v0 in p.items():
        v1 = q.get(k_, v0)
        if isinstance(v0, tuple):
            out[k_] = lerp2(v0, v1, u)
        elif isinstance(v0, (int, float)) and not isinstance(v0, bool):
            out[k_] = lerp(v0, v1, u)
        else:
            out[k_] = v1 if u >= 0.5 else v0
    return out


def seq(t, chaves_):
    """[(t, pose)] -> pose interpolada (suave) no tempo t."""
    if t <= chaves_[0][0]:
        return dict(chaves_[0][1])
    for (t0, p0), (t1, p1) in zip(chaves_, chaves_[1:]):
        if t < t1:
            return mix(p0, p1, e_inout(prog(t, t0, t1)))
    return dict(chaves_[-1][1])


def passo(base, fase, amp=1.0, lado_ini=0):
    """Andar de frente: ergue alternadamente um joelho; o tronco pende para a perna de apoio."""
    f = (fase + 0.5 * lado_ini) % 1.0
    lado = "E" if f < 0.5 else "D"
    u = math.sin(math.pi * ((f % 0.5) / 0.5)) * amp
    s = -1 if lado == "E" else 1
    p = dict(base)
    k_, a_ = base["k" + lado], base["a" + lado]
    p["k" + lado] = (k_[0] + s * 6 * u, k_[1] - 22 * u)
    p["a" + lado] = (a_[0] + s * 4 * u, a_[1] - 40 * u)
    p["pel"] = (base["pel"][0] - s * 4 * u, base["pel"][1] - 6 * u)
    p["inc"] = base["inc"] - s * 4 * u
    return p


def ik_braco(sh, m, lado, para_baixo=1.0):
    """Cotovelo do braço (braço = antebraço = L_BR) ligando ombro e mão; dobra para fora/baixo."""
    d = math.hypot(m[0] - sh[0], m[1] - sh[1])
    if d >= 2 * L_BR - 0.5:
        return lerp2(sh, m, 0.5)
    h = math.sqrt(max(0.0, L_BR ** 2 - (d / 2) ** 2))
    mx, my = (sh[0] + m[0]) / 2, (sh[1] + m[1]) / 2
    nx, ny = -(m[1] - sh[1]) / d, (m[0] - sh[0]) / d
    c1, c2 = (mx + nx * h, my + ny * h), (mx - nx * h, my - ny * h)
    sc = (lambda c: lado * c[0] + 0.6 * para_baixo * c[1])
    return c1 if sc(c1) > sc(c2) else c2


def _gira(p, c, graus):
    r = math.radians(graus); cs, sn = math.cos(r), math.sin(r)
    dx, dy = p[0] - c[0], p[1] - c[1]
    return (c[0] + dx * cs - dy * sn, c[1] + dx * sn + dy * cs)


def juntas(pose):
    """Juntas LOCAIS da criança (tudo o que o desenho e o telestrador precisam)."""
    pel = pose["pel"]; inc = pose["inc"]
    j = dict(pel=pel)
    for lado, s in (("E", -1), ("D", 1)):
        j["h" + lado] = (pel[0] + s * QUADRIL_L[0], pel[1] + QUADRIL_L[1])
        j["k" + lado] = pose["k" + lado]; j["a" + lado] = pose["a" + lado]
        j["t" + lado] = (pose["a" + lado][0] + pose["p" + lado][0], pose["a" + lado][1] + pose["p" + lado][1])
        j["o" + lado] = _gira((pel[0] + s * OMBRO_L[0], pel[1] + OMBRO_L[1]), pel, inc)
        j["m" + lado] = pose["m" + lado]
        j["c" + lado] = ik_braco(j["o" + lado], pose["m" + lado], s, pose.get("cot" + lado, 1.0))
    j["cab"] = _gira((pel[0] + 14 * pose["giro"], pel[1] + CABECA_DY), pel, inc)
    j["virilha"] = (pel[0], pel[1] + 30)
    return j


def no_mundo(pos, k, p):
    return (pos[0] + p[0] * k, pos[1] + p[1] * k)


def _camisa_path():
    p = skia.Path()
    p.moveTo(-50, -170)
    p.cubicTo(-82, -160, -94, -114, -92, -64)
    p.cubicTo(-90, -28, -88, -6, -84, 10)
    p.quadTo(0, 20, 84, 10)
    p.cubicTo(88, -6, 90, -28, 92, -64)
    p.cubicTo(94, -114, 82, -160, 50, -170)
    p.close()
    return p


CAMISA = _camisa_path()


LARG_COXA, LARG_JOELHO, LARG_TORNOZ, LARG_PE = 74.0, 62.0, 50.0, 46.0


def perna_contorno(j, lado):
    return uniao(capsula(j["h" + lado], j["k" + lado], LARG_COXA, LARG_JOELHO),
                 capsula(j["k" + lado], j["a" + lado], LARG_JOELHO, LARG_TORNOZ),
                 capsula((j["a" + lado][0], j["a" + lado][1] + 3), j["t" + lado], LARG_PE, LARG_PE - 4))


def _perna(cv, j, lado, e, a, ordem):
    H_, K_, A_, T_ = j["h" + lado], j["k" + lado], j["a" + lado], j["t" + lado]
    tons, lin = e["pele"], e["pele_linha"]
    pe = capsula((A_[0], A_[1] + 3), T_, LARG_PE, LARG_PE - 4)
    coxa = capsula(H_, K_, LARG_COXA, LARG_JOELHO); canela = capsula(K_, A_, LARG_JOELHO, LARG_TORNOZ)
    cv.drawPath(uniao(coxa, canela, pe), paint("#000000", int(45 * a), blur=7))
    pinta(cv, pe, A_, T_, LARG_PE, tons, a)
    if ordem == "canela":
        pinta(cv, coxa, H_, K_, LARG_COXA, tons, a); pinta(cv, canela, K_, A_, LARG_JOELHO, tons, a)
    else:
        pinta(cv, canela, K_, A_, LARG_JOELHO, tons, a); pinta(cv, coxa, H_, K_, LARG_COXA, tons, a)
    cv.drawPath(uniao(coxa, canela, pe), paint(lin, int(220 * a), "stroke", 2.6))
    # dobra do joelho (uma ruguinha) e os dedinhos na ponta do pé
    cv.drawArc(skia.Rect(K_[0] - 12, K_[1] - 6, K_[0] + 12, K_[1] + 10), 200, 140, False,
               paint(lin, int(120 * a), "stroke", 2.0))


def _bermuda(cv, j, e, a):
    pel = j["pel"]
    pth = rr_path(pel[0] - 86, pel[1] - 16, pel[0] + 86, pel[1] + 44, 30)
    for lado in ("E", "D"):
        H_, K_ = j["h" + lado], j["k" + lado]
        pth = uniao(pth, capsula(H_, lerp2(H_, K_, 0.44), 88, 82))
    pinta(cv, pth, (pel[0], pel[1] - 30), (pel[0], pel[1] + 50), 190, e["bermuda"], a)
    cv.drawPath(pth, paint(e["bermuda_linha"], int(220 * a), "stroke", 2.6))
    for lado in ("E", "D"):                               # a barra da bermuda
        H_, K_ = j["h" + lado], j["k" + lado]
        c = lerp2(H_, K_, 0.44); d = (K_[0] - H_[0], K_[1] - H_[1]); L = math.hypot(*d) or 1
        n = (-d[1] / L, d[0] / L)
        cv.drawLine(c[0] - n[0] * 34, c[1] - n[1] * 34, c[0] + n[0] * 34, c[1] + n[1] * 34,
                    paint(e["bermuda_linha"], int(150 * a), "stroke", 2.4))


def _braco(cv, j, lado, e, a):
    sh, cot, m = j["o" + lado], j["c" + lado], j["m" + lado]
    tons, lin = e["pele"], e["pele_linha"]
    pulso = lerp2(cot, m, 0.78)
    br = uniao(capsula(sh, cot, 40, 36), capsula(cot, pulso, 36, 32))
    mao_ = skia.Path(); mao_.addCircle(m[0], m[1], 21)
    cv.drawPath(uniao(br, mao_), paint("#000000", int(45 * a), blur=7))
    pinta(cv, capsula(sh, cot, 40, 36), sh, cot, 40, tons, a)
    pinta(cv, capsula(cot, pulso, 36, 32), cot, pulso, 36, tons, a)
    pinta(cv, mao_, pulso, m, 42, tons, a)
    cv.drawPath(uniao(br, mao_), paint(lin, int(220 * a), "stroke", 2.4))
    mg = capsula(sh, lerp2(sh, cot, 0.55), 56, 50)                       # manga curta
    pinta(cv, mg, sh, cot, 56, e["camisa"], a)
    if e.get("listras"):
        _listras(cv, mg, e["listras"], a)
    cv.drawPath(mg, paint(e["camisa_linha"], int(220 * a), "stroke", 2.4))


def _listras(cv, pth, cor, a, passo_=24.0, larg=9.0):
    cv.save(); cv.clipPath(pth, skia.ClipOp.kIntersect, True)
    b = pth.getBounds()
    y = b.top() + 8
    while y < b.bottom():
        cv.drawLine(b.left() - 4, y, b.right() + 4, y, paint(cor, int(235 * a), "stroke", larg)); y += passo_
    cv.restore()


def _cabeca(cv, j, pose, e, a):
    cx, cy = j["cab"]; r = CABECA_R; giro = pose["giro"]
    cv.save(); cv.translate(cx, cy); cv.rotate(pose["inc"] * 0.6)
    for s in (-1, 1):                                    # orelhas (a do lado para onde gira some)
        if s * giro > 0.4:
            continue
        ox = s * (r - 6) - 10 * giro
        orl = oval_path(ox - 13, -22, ox + 13, 18)
        pinta(cv, orl, (ox, -22), (ox, 18), 26, e["pele"], a, linha=e["pele_linha"], larg_linha=2.2)
    cab = skia.Path(); cab.addCircle(0, 0, r)
    cv.drawCircle(3, 6, r + 2, paint("#000000", int(50 * a), blur=8))
    sh = skia.GradientShader.MakeRadial(skia.Point(-18 + 20 * giro, -22), r * 1.5,
                                        [_c(e["pele"][2]), _c(e["pele"][1]), _c(e["pele"][0])], [0.0, 0.55, 1.0])
    cv.drawPath(cab, paint(e["pele"][1], int(255 * a), shader=sh))
    cv.drawPath(cab, paint(e["pele_linha"], int(220 * a), "stroke", 2.6))
    cv.save(); cv.clipPath(cab, skia.ClipOp.kIntersect, True)
    if e["penteado"] == "curto":
        cv.drawOval(skia.Rect(-r - 8, -r - 24, r + 8, -r + 50), paint(e["cabelo"], int(255 * a)))
    else:
        cv.drawOval(skia.Rect(-70 + 10 * giro, -r - 22, 70 + 10 * giro, -r + 36), paint(e["cabelo"], int(255 * a)))
    cv.restore()
    if e["penteado"] == "topete":                        # o topete do bebê do cf_andador
        top = skia.Path(); top.moveTo(-6, -r + 2)
        top.cubicTo(-4, -r - 32, 34, -r - 30, 28, -r - 8); top.cubicTo(24, -r + 4, 8, -r - 2, 14, -r - 14)
        cv.drawPath(top, paint(e["cabelo"], int(255 * a), "stroke", 8))
    elif e["penteado"] == "curto":                      # cabelo curtinho crespo (a criança do vizinho)
        for i in range(10):
            ang = math.radians(196 + i * 16.4)
            cv.drawCircle((r - 4) * math.cos(ang), (r - 4) * math.sin(ang) + 6, 14, paint(e["cabelo"], int(255 * a)))
    cv.restore()


def cubo(cv, x, y, r, cor, a=1.0):
    """Bloco de montar SEM letras nem números: frente, topo e lado."""
    if a <= 0:
        return
    cv.drawOval(skia.Rect(x - r * 1.1, y + r * 0.7, x + r * 1.3, y + r * 1.15), paint("#000000", int(55 * a), blur=6))
    topo = poli([(x - r, y - r), (x - r + r * 0.45, y - r * 1.4), (x + r * 1.45, y - r * 1.4), (x + r, y - r)])
    lado_ = poli([(x + r, y - r), (x + r * 1.45, y - r * 1.4), (x + r * 1.45, y + r * 0.6), (x + r, y + r)])
    cv.drawPath(topo, paint(lerpc(cor, "#FFFFFF", 0.35), int(255 * a)))
    cv.drawPath(lado_, paint(esc_cor(cor, 0.22), int(255 * a)))
    fr = skia.RRect.MakeRectXY(skia.Rect(x - r, y - r, x + r, y + r), 4, 4)
    cv.drawRRect(fr, paint(cor, int(255 * a)))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - r * 0.55, y - r * 0.55, x + r * 0.55, y + r * 0.55), 6, 6),
                 paint(lerpc(cor, "#FFFFFF", 0.18), int(200 * a)))
    for pth in (topo, lado_):
        cv.drawPath(pth, paint(esc_cor(cor, 0.4), int(180 * a), "stroke", 1.8))
    cv.drawRRect(fr, paint(esc_cor(cor, 0.4), int(200 * a), "stroke", 2))


def bola(cv, x, y, r, a=1.0, giro=0.0):
    """Bola de brinquedo em gomos (sem desenho, sem letra)."""
    if a <= 0:
        return
    cv.drawOval(skia.Rect(x - r * 1.05, y + r * 0.72, x + r * 1.05, y + r * 1.12), paint("#000000", int(60 * a), blur=7))
    c = skia.Path(); c.addCircle(x, y, r)
    cv.save(); cv.clipPath(c, skia.ClipOp.kIntersect, True)
    cores = ("#E8604C", "#FFFFFF", "#4C86C6", "#FFFFFF", "#F2C14E", "#FFFFFF")
    for i, cor in enumerate(cores):
        a0 = giro + i * 60
        p = skia.Path(); p.moveTo(x, y); p.arcTo(skia.Rect(x - r, y - r, x + r, y + r), a0, 60, False); p.close()
        cv.drawPath(p, paint(cor, int(255 * a)))
    cv.drawCircle(x - r * 0.35, y - r * 0.4, r * 0.32, paint("#FFFFFF", int(90 * a), blur=6))
    cv.restore()
    cv.drawCircle(x, y, r, paint("#5B6676", int(200 * a), "stroke", 2.5))
    cv.drawCircle(x, y, r * 0.12, paint("#FFFFFF", int(255 * a)))


def crianca(cv, pose, pos, k, e=EST_NOSSA, a=1.0, verde=0.0, sombra=True, cor_bloco=CUBOS[1]):
    """Desenha a criança na pose, com a origem local em `pos` (mundo) e escala k."""
    if a <= 0:
        return
    j = juntas(pose)
    cv.save(); cv.translate(pos[0], pos[1]); cv.scale(k, k)
    if sombra:
        xs = [j["aE"][0], j["aD"][0], j["kE"][0], j["kD"][0], j["tE"][0], j["tD"][0]]
        x0, x1 = min(xs + [-80]) - 30, max(xs + [80]) + 30
        alto = min(1.0, max(0.0, -pose["pel"][1] - 46) / 120)
        cv.drawOval(skia.Rect(x0, -16 + 6 * alto, x1, 20 - 4 * alto), paint("#000000", int((70 - 30 * alto) * a), blur=10))
    ordem = pose.get("ordem", "coxa")
    if verde > 0:                                        # contorno verde nas pernas (o jeito certo)
        cont = uniao(perna_contorno(j, "E"), perna_contorno(j, "D"))
        cv.drawPath(cont, paint(VERDE, int(150 * verde * a), "stroke", 22, blur=10))
    for lado in (("D", "E") if ordem == "canela" else ("E", "D")):
        _perna(cv, j, lado, e, a, ordem)
    if verde > 0:
        cv.drawPath(uniao(perna_contorno(j, "E"), perna_contorno(j, "D")),
                    paint(VERDE, int(255 * verde * a), "stroke", 6))
    _bermuda(cv, j, e, a)
    pel = j["pel"]
    cv.save(); cv.translate(pel[0], pel[1]); cv.rotate(pose["inc"])
    cv.drawPath(CAMISA, paint("#000000", int(55 * a), blur=10))
    pinta(cv, CAMISA, (0, -170), (0, 14), 190, e["camisa"], a)
    if e.get("listras"):
        _listras(cv, CAMISA, e["listras"], a, 30.0, 12.0)
    cv.drawPath(CAMISA, paint(e["camisa_linha"], int(220 * a), "stroke", 2.6))
    gx = 12 * pose["giro"]
    gola = skia.Path(); gola.moveTo(-34 + gx, -166); gola.quadTo(gx, -138, 34 + gx, -166)
    cv.drawPath(gola, paint(e["camisa_linha"], int(200 * a), "stroke", 4))
    cv.restore()
    if pose.get("bloco", 0) > 0:                         # o bloco nas mãos
        mb = lerp2(j["mE"], j["mD"], 0.5)
        cubo(cv, mb[0], mb[1] + 6, 30, cor_bloco, a * pose["bloco"])
    for lado in ("E", "D"):
        _braco(cv, j, lado, e, a)
    _cabeca(cv, j, pose, e, a)
    cv.restore()


def juntas_mundo(pose, pos, k):
    return {n: no_mundo(pos, k, v) for n, v in juntas(pose).items()}


def mao_adulto(cv, pulso, ponta_, a=1.0, lado=1, esc=1.0):
    """Mão de adulto do punho até a ponta dos dedos (cópia do cf_var_primeiros_socorros; `esc` engrossa)."""
    d = (ponta_[0] - pulso[0], ponta_[1] - pulso[1]); L = math.hypot(*d) or 1.0
    u = (d[0] / L, d[1] / L); n = (-u[1] * lado, u[0] * lado)
    q = lambda f, g=0.0: (pulso[0] + u[0] * L * f + n[0] * g * esc, pulso[1] + u[1] * L * f + n[1] * g * esc)   # noqa: E731
    pol = capsula(q(0.18, 13), q(0.62, 20), 15 * esc, 12 * esc)
    pinta(cv, pol, q(0.18, 13), q(0.62, 20), 15 * esc, PELE_AD, a, linha=LINHA_AD, larg_linha=2)
    corpo_ = uniao(capsula(q(0.0), q(0.56), 31 * esc, 36 * esc), capsula(q(0.5), q(1.0, -2), 35 * esc, 28 * esc))
    pinta(cv, corpo_, q(0.0), q(1.0), 36 * esc, PELE_AD, a, linha=LINHA_AD, larg_linha=2.2)
    for g in (-8.5, 0.0, 8.5):
        p0_, p1_ = q(0.62, g), q(0.97, g * 0.85)
        cv.drawLine(p0_[0], p0_[1], p1_[0], p1_[1], paint(LINHA_AD, int(190 * a), "stroke", 2.2))


def antebraco_adulto(cv, pulso, ang, L=420.0, a=1.0, esc=1.0):
    """Antebraço vestido (manga teal, com dobras e punho) saindo da borda do quadro até o punho."""
    if a <= 0:
        return
    u = (math.cos(math.radians(ang)), math.sin(math.radians(ang)))
    om = (pulso[0] + u[0] * L, pulso[1] + u[1] * L)
    pinta(cv, capsula(om, pulso, 60 * esc, 50 * esc), om, pulso, 60 * esc, MANGA_AD, a, linha=MANGA_LINHA)
    n = (-u[1], u[0])
    for f, g in ((0.35, 1), (0.5, -1), (0.65, 1)):
        c = lerp2(pulso, om, f)
        cv.drawLine(c[0] - n[0] * 16 * esc * g, c[1] - n[1] * 16 * esc * g, c[0] - u[0] * 12 * esc + n[0] * 6 * esc * g,
                    c[1] - u[1] * 12 * esc + n[1] * 6 * esc * g, paint(MANGA_LINHA, int(150 * a), "stroke", 2.4))
    q = lerp2(pulso, om, 0.1)
    cv.drawPath(capsula(q, pulso, 54 * esc, 54 * esc), paint(esc_cor(MANGA_AD[1], 0.18), int(255 * a)))


# ================================================================== CENÁRIO: a sala (lances 1 e 3)
PISO_Y = 560.0                       # rodapé (parede -> chão)
VP_SALA = (540.0, 150.0)             # ponto de fuga das tábuas
SALA_X0, SALA_Y0, SALA_X1, SALA_Y1, SALA_ESC = -360.0, 120.0, 1440.0, 1480.0, 1.5


def sala(cv, variante):
    def _d(c):
        c.scale(SALA_ESC, SALA_ESC); c.translate(-SALA_X0, -SALA_Y0); _sala(c, variante)
    img = cacheado("sala_" + variante, (SALA_X1 - SALA_X0) * SALA_ESC, (SALA_Y1 - SALA_Y0) * SALA_ESC, _d)
    cv.save(); cv.translate(SALA_X0, SALA_Y0); cv.scale(1 / SALA_ESC, 1 / SALA_ESC)
    cv.drawImage(img, 0, 0, LINEAR)
    cv.restore()


def _x_piso(xb, y):
    """x no chão (altura y) da tábua que encosta no rodapé em xb (linhas que vão ao ponto de fuga)."""
    return VP_SALA[0] + (xb - VP_SALA[0]) * (y - VP_SALA[1]) / (PISO_Y - VP_SALA[1])


def quad_pt(c00, c10, c01, c11, u, v):
    top = lerp2(c00, c10, u); bot = lerp2(c01, c11, u)
    return lerp2(top, bot, v)


def sofa(cv, x0, x1, y_chao, prof=1.0):
    """Sofá azul (do piloto do gesso) encostado na parede: encosto, assento, almofadas, pés."""
    alt = 250.0
    y_top = y_chao - alt
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0 - 10, y_chao - 30, x1 + 10, y_chao + 18), 20, 20), paint("#000000", 70, blur=14))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, y_top), skia.Point(0, y_chao)], [_c(SOFA_CL), _c(SOFA), _c(SOFA_ESC)])
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y_top, x1, y_chao - 8), 34, 34), paint(SOFA, shader=sh))
    # almofadas do encosto
    n = max(2, int((x1 - x0 - 80) // 160))
    w_ = (x1 - x0 - 80) / n
    for i in range(n):
        ax0 = x0 + 40 + i * w_ + 6; ax1 = ax0 + w_ - 12
        r = skia.RRect.MakeRectXY(skia.Rect(ax0, y_top + 22, ax1, y_top + 120), 26, 26)
        sh2 = skia.GradientShader.MakeLinear([skia.Point(0, y_top + 22), skia.Point(0, y_top + 120)], [_c(ALMOF_CL), _c(ALMOF)])
        cv.drawRRect(r, paint(ALMOF, shader=sh2)); cv.drawRRect(r, paint(ALMOF_ESC, 200, "stroke", 3))
    # assento
    sa = skia.RRect.MakeRectXY(skia.Rect(x0 + 24, y_top + 112, x1 - 24, y_top + 168), 22, 22)
    sh3 = skia.GradientShader.MakeLinear([skia.Point(0, y_top + 112), skia.Point(0, y_top + 168)], [_c(ALMOF_CL), _c(ALMOF_ESC)])
    cv.drawRRect(sa, paint(ALMOF, shader=sh3)); cv.drawRRect(sa, paint(ALMOF_ESC, 220, "stroke", 3))
    # braços
    for bx in (x0, x1 - 62):
        b = skia.RRect.MakeRectXY(skia.Rect(bx, y_top + 60, bx + 62, y_chao - 14), 28, 28)
        cv.drawRRect(b, paint(SOFA_CL)); cv.drawRRect(b, paint(SOFA_ESC, 220, "stroke", 3))
    for px in (x0 + 30, x1 - 44):
        cv.drawRect(skia.Rect(px, y_chao - 14, px + 14, y_chao + 6), paint("#3A2E25"))
    return y_top + 112                                    # altura do assento (onde a mão apoia)


def cesto(cv, x, y, a=1.0):
    """Cesto de brinquedos guardados (bola, bloco, bichinho de pano sem rosto)."""
    bola(cv, x - 36, y - 92, 30, a, 20)
    cubo(cv, x + 30, y - 88, 22, CUBOS[2], a)
    cv.drawOval(skia.Rect(x - 4, y - 130, x + 42, y - 84), paint("#D9B3E8", int(255 * a)))       # bichinho (orelhas)
    cv.drawCircle(x + 4, y - 128, 11, paint("#D9B3E8", int(255 * a))); cv.drawCircle(x + 34, y - 128, 11, paint("#D9B3E8", int(255 * a)))
    corpo_ = skia.Path()
    corpo_.moveTo(x - 90, y - 92); corpo_.lineTo(x + 90, y - 92); corpo_.lineTo(x + 74, y); corpo_.lineTo(x - 74, y); corpo_.close()
    cv.drawOval(skia.Rect(x - 92, y - 12, x + 92, y + 14), paint("#000000", int(60 * a), blur=8))
    cv.drawPath(corpo_, paint(CESTO, int(255 * a)))
    cv.save(); cv.clipPath(corpo_, skia.ClipOp.kIntersect, True)
    for yy in range(int(y - 86), int(y), 14):
        cv.drawLine(x - 100, yy, x + 100, yy, paint(CESTO_ESC, int(150 * a), "stroke", 3))
    for xx in range(int(x - 90), int(x + 90), 18):
        cv.drawLine(xx, y - 92, xx + 4, y, paint(CESTO_ESC, int(90 * a), "stroke", 2))
    cv.restore()
    cv.drawLine(x - 92, y - 92, x + 92, y - 92, paint(CESTO_ESC, int(255 * a), "stroke", 8))


def mesinha(cv, x0, x1, y_chao):
    """Mesinha baixa encostada na parede, com protetor de quina nas duas quinas da frente."""
    yt = y_chao - MESA_ALT
    for px in (x0 + 16, x1 - 34):
        cv.drawRect(skia.Rect(px, yt + 20, px + 18, y_chao), paint(MESA_ESC))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0 - 8, y_chao - 8, x1 + 8, y_chao + 10), 10, 10), paint("#000000", 50, blur=10))
    tampo = skia.RRect.MakeRectXY(skia.Rect(x0, yt, x1, yt + 26), 6, 6)
    cv.drawRect(skia.Rect(x0 + 10, yt - 18, x1 - 10, yt), paint(MESA_CL))
    cv.drawRRect(tampo, paint(MESA)); cv.drawRRect(tampo, paint(MESA_ESC, 220, "stroke", 2.5))
    for qx in (x0, x1):                                  # protetores de quina (macios, arredondados, azul-claro)
        pr = skia.RRect.MakeRectXY(skia.Rect(qx - 26, yt - 12, qx + 26, yt + 40), 20, 20)
        cv.drawRRect(pr, paint("#000000", 50, blur=5))
        cv.drawRRect(pr, paint(PROTETOR)); cv.drawRRect(pr, paint("#5FA6D0", 255, "stroke", 4))
        cv.drawArc(skia.Rect(qx - 16, yt - 4, qx + 16, yt + 28), 200, 120, False, paint("#FFFFFF", 220, "stroke", 4))
    # um vaso de planta em cima (sem texto)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x1 - 110, yt - 70, x1 - 60, yt - 18), 8, 8), paint("#E7ECF1"))
    for i, (dx, dy) in enumerate(((-12, -40), (0, -56), (14, -42), (-4, -30))):
        cv.drawOval(skia.Rect(x1 - 85 + dx - 12, yt - 70 + dy - 22, x1 - 85 + dx + 12, yt - 70 + dy + 22), paint("#5E9E5A" if i % 2 else "#4B8A4A"))
    return (x0, yt + 12), (x1, yt + 12)


def _sala(cv, variante):
    sh = skia.GradientShader.MakeLinear([skia.Point(0, 120), skia.Point(0, PISO_Y)], [_c(PAREDE_A), _c(PAREDE_B)])
    cv.drawRect(skia.Rect(-600, -200, 1800, PISO_Y + 2), paint(PAREDE_A, shader=sh))
    # janela (luz do dia) e um quadro com desenho (montanha e sol), sem texto
    jx0, jy0, jx1, jy1 = 880, 210, 1130, 450
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(jx0 - 14, jy0 - 14, jx1 + 14, jy1 + 14), 8, 8), paint("#F7F9FB"))
    vid = skia.GradientShader.MakeLinear([skia.Point(jx0, jy0), skia.Point(jx1, jy1)], [_c("#BFE3F7"), _c("#E9F6FD")])
    cv.drawRect(skia.Rect(jx0, jy0, jx1, jy1), paint("#CFEAF8", shader=vid))
    cv.drawLine((jx0 + jx1) / 2, jy0, (jx0 + jx1) / 2, jy1, paint("#F7F9FB", 255, "stroke", 10))
    cv.drawLine(jx0, (jy0 + jy1) / 2, jx1, (jy0 + jy1) / 2, paint("#F7F9FB", 255, "stroke", 10))
    qx0, qy0, qx1, qy1 = 40, 190, 230, 320
    cv.drawRect(skia.Rect(qx0 - 10, qy0 - 10, qx1 + 10, qy1 + 10), paint("#8E6646"))
    cv.drawRect(skia.Rect(qx0, qy0, qx1, qy1), paint("#FBF4E6"))
    cv.drawPath(poli([(qx0 + 10, qy1 - 10), (qx0 + 80, qy0 + 40), (qx0 + 130, qy1 - 40), (qx0 + 160, qy0 + 70), (qx1 - 8, qy1 - 10)]),
                paint("#7FB38A"))
    cv.drawCircle(qx1 - 40, qy0 + 32, 18, paint("#F2C14E"))
    # rodapé e piso de tábuas que vão ao ponto de fuga (o chão visto um pouco de cima)
    shp = skia.GradientShader.MakeLinear([skia.Point(0, PISO_Y), skia.Point(0, 1480)], [_c(PISO_B), _c(PISO_A)])
    cv.drawRect(skia.Rect(-600, PISO_Y, 1800, 1700), paint(PISO_A, shader=shp))
    for xb in range(-400, 1600, 56):
        cv.drawLine(xb, PISO_Y, _x_piso(xb, 1700), 1700, paint(PISO_LINHA, 110, "stroke", 2))
    y = PISO_Y + 20; dy = 30
    while y < 1700:
        cv.drawLine(-600, y, 1800, y, paint(PISO_LINHA, 40, "stroke", 1.5)); y += dy; dy *= 1.18
    cv.drawRect(skia.Rect(-600, PISO_Y - 16, 1800, PISO_Y + 2), paint(RODAPE))
    cv.drawLine(-600, PISO_Y + 2, 1800, PISO_Y + 2, paint("#000000", 40, "stroke", 4, blur=3))
    if variante == "eva":
        sofa(cv, -40, 470, 640)
        cesto(cv, 930, 650)
        # tapete de EVA colorido (placas encaixadas) em perspectiva
        c00, c10, c01, c11 = (190, 700), (890, 700), (-40, 1240), (1120, 1240)
        cv.drawPath(poli([c00, c10, c11, c01]), paint("#000000", 50, blur=12))
        n_u, n_v = 5, 4
        for i in range(n_u):
            for jj in range(n_v):
                v0, v1 = (jj / n_v) ** 1.12, ((jj + 1) / n_v) ** 1.12
                pts = [quad_pt(c00, c10, c01, c11, i / n_u, v0), quad_pt(c00, c10, c01, c11, (i + 1) / n_u, v0),
                       quad_pt(c00, c10, c01, c11, (i + 1) / n_u, v1), quad_pt(c00, c10, c01, c11, i / n_u, v1)]
                cor = EVA[(i + 2 * jj) % len(EVA)]
                pth = poli(pts)
                cv.drawPath(pth, paint(cor))
                cv.drawPath(pth, paint(esc_cor(cor, 0.25), 180, "stroke", 3))
                # os dentinhos de encaixe na aresta de cima de cada placa
                for f in (0.3, 0.7):
                    q = lerp2(pts[0], pts[1], f)
                    cv.drawRect(skia.Rect(q[0] - 9, q[1] - 4, q[0] + 9, q[1] + 4), paint(esc_cor(cor, 0.12)))
        cv.drawPath(poli([c00, c10, c11, c01]), paint("#FFFFFF", 90, "stroke", 4))
    else:
        sofa(cv, -120, 330, 640)
        cesto(cv, 470, 640)
        mesinha(cv, MESA_X0, MESA_X1, MESA_CHAO)
        # tapete grande e macio (areia), cantos arredondados, felpa
        tp = TAPETE_PTS
        cv.drawPath(suave(tp), paint("#000000", 55, blur=14))
        shr = skia.GradientShader.MakeLinear([skia.Point(0, 700), skia.Point(0, 1260)], [_c(AREIA_ESC), _c(AREIA), _c(AREIA_CL)])
        cv.drawPath(suave(tp), paint(AREIA, shader=shr))
        rng = np.random.default_rng(3)
        cv.save(); cv.clipPath(suave(tp), skia.ClipOp.kIntersect, True)
        for _ in range(900):
            x = rng.uniform(-100, 1200); yy = rng.uniform(690, 1280)
            cv.drawLine(x, yy, x + rng.uniform(-3, 3), yy - 4 - 6 * (yy - 690) / 600, paint("#FFFFFF", 50, "stroke", 1.6))
        cv.restore()
        cv.drawPath(suave(tp), paint(AREIA_ESC, 200, "stroke", 4))


TAPETE_PTS = [(170, 704), (540, 690), (910, 704), (1090, 980), (1180, 1250), (540, 1290), (-100, 1250), (-10, 980)]
MESA_X0, MESA_X1, MESA_CHAO, MESA_ALT = 690.0, 1050.0, 664.0, 150.0


# ================================================================== CENÁRIO: os dois quintais (lance 2)
HORIZ2 = 548.0
VP2 = (566.0, HORIZ2 - 4)
CERCA_X0, CERCA_Y0 = 520.0, 1300.0               # a cerquinha começa embaixo, no meio, e vai ao ponto de fuga
QUINT_X0, QUINT_Y0, QUINT_X1, QUINT_Y1, QUINT_ESC = -360.0, 120.0, 1440.0, 1480.0, 1.5


def cerca_x(y):
    return CERCA_X0 + (VP2[0] - CERCA_X0) * (CERCA_Y0 - y) / (CERCA_Y0 - VP2[1])


def esc_prof(y):
    """Escala de profundidade no chão do quintal (1 embaixo, 0 no horizonte)."""
    return clamp((y - VP2[1]) / (CERCA_Y0 - VP2[1]))


def quintal(cv):
    def _d(c):
        c.scale(QUINT_ESC, QUINT_ESC); c.translate(-QUINT_X0, -QUINT_Y0); _quintal(c)
    img = cacheado("quintal", (QUINT_X1 - QUINT_X0) * QUINT_ESC, (QUINT_Y1 - QUINT_Y0) * QUINT_ESC, _d)
    cv.save(); cv.translate(QUINT_X0, QUINT_Y0); cv.scale(1 / QUINT_ESC, 1 / QUINT_ESC)
    cv.drawImage(img, 0, 0, LINEAR)
    cv.restore()


def _casa(cv, x0, x1, y_base, alto, parede, telhado):
    cv.drawRect(skia.Rect(x0, y_base - alto, x1, y_base), paint(parede))
    cv.drawPath(poli([(x0 - 30, y_base - alto + 6), ((x0 + x1) / 2, y_base - alto - 120), (x1 + 30, y_base - alto + 6)]),
                paint(telhado))
    for wx in (x0 + 60, x1 - 200):
        cv.drawRect(skia.Rect(wx - 6, y_base - alto + 54, wx + 146, y_base - alto + 166), paint("#FFFFFF"))
        cv.drawRect(skia.Rect(wx, y_base - alto + 60, wx + 140, y_base - alto + 160), paint("#BFE3F7"))
        cv.drawLine(wx + 70, y_base - alto + 60, wx + 70, y_base - alto + 160, paint("#FFFFFF", 255, "stroke", 6))


def _quintal(cv):
    sh = skia.GradientShader.MakeLinear([skia.Point(0, 120), skia.Point(0, HORIZ2)], [_c(CEU_A), _c(CEU_B)])
    cv.drawRect(skia.Rect(-600, -200, 1800, HORIZ2 + 2), paint(CEU_A, shader=sh))
    for (x, y, r) in ((90, 210, 48), (150, 200, 64), (215, 214, 44), (800, 180, 52), (870, 168, 70), (940, 186, 48)):
        cv.drawCircle(x, y, r, paint("#FFFFFF", 170))
    # a nossa casa (à esquerda, amarelinha) e a do vizinho (à direita, azul-clara), sem número nem placa
    _casa(cv, -300, 470, HORIZ2 + 4, 250, "#F3E3C3", "#C27B5E")
    _casa(cv, 640, 1400, HORIZ2 + 4, 230, "#DCE7EF", "#8F6E9E")
    for i in range(30):                                 # cerca viva ao fundo
        x = -400 + i * 64
        cv.drawCircle(x, HORIZ2 - 6, 40 + 6 * math.sin(i * 1.7), paint("#5E9E5A" if i % 2 else "#4B8A4A"))
    shg = skia.GradientShader.MakeLinear([skia.Point(0, HORIZ2), skia.Point(0, 1480)], [_c(GRAMA_A), _c(GRAMA_B)])
    cv.drawRect(skia.Rect(-600, HORIZ2, 1800, 1700), paint(GRAMA_A, shader=shg))
    y, k = HORIZ2, 0
    while y < 1700:
        hb = 10 + 9 * k ** 1.25
        if k % 2 == 0:
            cv.drawRect(skia.Rect(-600, y, 1800, y + hb), paint(FAIXA_GRAMA, 60))
        y += hb; k += 1
    rng = np.random.default_rng(9)
    for _ in range(320):
        x = rng.uniform(-600, 1800); yy = rng.uniform(HORIZ2 + 30, 1480)
        h_ = 4 + 10 * (yy - HORIZ2) / 900
        cv.drawLine(x, yy, x - 2, yy - h_, paint("#3E8530", 110, "stroke", 1.4 + 1.4 * (yy - HORIZ2) / 900))
    # a varanda de madeira do nosso lado (o sofá fica nela)
    deck = poli([(-600, HORIZ2 + 20), (420, HORIZ2 + 20), (360, 980), (-600, 980)])
    cv.drawPath(deck, paint(DECK))
    cv.save(); cv.clipPath(deck, skia.ClipOp.kIntersect, True)
    yy, dy = HORIZ2 + 34, 16
    while yy < 990:
        cv.drawLine(-600, yy, 500, yy, paint(DECK_LINHA, 150, "stroke", 2)); yy += dy; dy *= 1.12
    cv.restore()
    cv.drawLine(420, HORIZ2 + 20, 360, 980, paint(DECK_LINHA, 255, "stroke", 5))
    cv.drawLine(-600, 980, 360, 980, paint(DECK_LINHA, 255, "stroke", 6))
    sofa(cv, -180, 250, 870)


def cerca(cv, a=1.0, x_desloca=0.0):
    """Cerquinha baixa de madeira (ripas pontudas e duas travessas) que divide os dois quintais: vai do pé do
    quadro ao ponto de fuga, mais baixa que a cintura das crianças."""
    if a <= 0:
        return
    ripas = []
    d = 0.0
    while True:
        f = 1.0 / (1.0 + d)
        y = VP2[1] + (CERCA_Y0 - VP2[1]) * f
        if f < 0.06:
            break
        if y < 1290:
            ripas.append((cerca_x(y) + x_desloca, y, 230 * f, 4 + 24 * f, f))
        d += 0.11
    for frac, larg in ((0.30, 13.0), (0.78, 15.0)):            # travessas (atrás das ripas)
        for (x0, y0, h0, _, f0), (x1, y1, h1, _, f1) in zip(ripas, ripas[1:]):
            w = 2 + larg * (f0 + f1) / 2
            cv.drawLine(x0 + 3 * f0, y0 - h0 * frac, x1 + 3 * f1, y1 - h1 * frac, paint(MADEIRA_ESC, int(255 * a), "stroke", w + 3))
            cv.drawLine(x0 + 3 * f0, y0 - h0 * frac, x1 + 3 * f1, y1 - h1 * frac, paint(MADEIRA, int(255 * a), "stroke", w))
    for (x, y, h, w, f) in reversed(ripas):                    # ripas, do fundo para a frente
        rip = poli([(x - w / 2, y), (x - w / 2, y - h), (x, y - h - w * 0.7), (x + w / 2, y - h), (x + w / 2, y)])
        cv.drawPath(rip, paint(MADEIRA_CL if f > 0.3 else MADEIRA, int(255 * a)))
        cv.drawRect(skia.Rect(x + w * 0.1, y - h, x + w / 2, y), paint(MADEIRA, int(255 * a)))
        cv.drawPath(rip, paint(MADEIRA_ESC, int(220 * a), "stroke", 1 + 2 * f))
        cv.drawOval(skia.Rect(x - w, y - 4 * f, x + w, y + 6 * f), paint("#000000", int(40 * a), blur=3))


def raias(cv, a, x_viz=0.0, t=0.0, brilho=0.0):
    """As duas raias (a cerca virou divisória de raia): bordas tracejadas que vão ao ponto de fuga."""
    if a <= 0:
        return
    for (xb, dx, alfa_f) in ((-120.0, 0.0, 0.0), (CERCA_X0, 0.0, 1.0), (1180.0, x_viz, 0.0)):
        pts0 = (xb + dx, CERCA_Y0); pts1 = (VP2[0] + dx, VP2[1] + 60)
        pe = paint(CIANO, int(230 * a), "stroke", 7)
        pe.setPathEffect(skia.DashPathEffect.Make([28.0, 18.0], -t * 60))
        cv.drawLine(pts0[0], pts0[1], lerp(pts0[0], pts1[0], 0.92), lerp(pts0[1], pts1[1], 0.92), paint(CARTAO, int(120 * a), "stroke", 13))
        cv.drawLine(pts0[0], pts0[1], lerp(pts0[0], pts1[0], 0.92), lerp(pts0[1], pts1[1], 0.92), pe)
    for (x0b, x1b, dx) in ((-120.0, CERCA_X0, 0.0), (CERCA_X0, 1180.0, x_viz)):
        faixa = poli([(x0b + (dx if x0b != CERCA_X0 else dx), CERCA_Y0), (x1b + dx, CERCA_Y0),
                      (lerp(x1b + dx, VP2[0] + dx, 0.92), lerp(CERCA_Y0, VP2[1] + 60, 0.92)),
                      (lerp(x0b + dx, VP2[0] + dx, 0.92), lerp(CERCA_Y0, VP2[1] + 60, 0.92))])
        cv.drawPath(faixa, paint(CIANO, int((28 + 40 * brilho) * a)))


def pulso_raia(cv, x, y, esc, t, periodo, a, fase=0.0):
    """Metrônomo visual: anéis que saem do pé da criança no compasso dela (sem número, sem relógio)."""
    if a <= 0:
        return
    for k in range(2):
        u = ((t + fase) / periodo + k * 0.5) % 1.0
        r = (50 + 150 * u) * esc
        cv.drawOval(skia.Rect(x - r, y - r * 0.28, x + r, y + r * 0.28), paint(CIANO, int(230 * a * (1 - u) ** 1.2), "stroke", 6 * esc + 1))
    kb = max(0.0, 1 - (((t + fase) / periodo) % 1.0) / 0.25)
    cv.drawOval(skia.Rect(x - 46 * esc, y - 13 * esc, x + 46 * esc, y + 13 * esc), paint(CIANO, int(110 * a * kb), blur=6))


# ================================================================== LANCE 1 — sentar em W
K1 = 0.95
POS1 = (540.0, 930.0)
BOLA1 = (840.0, 958.0)
X_ANDA = 700.0
CUBOS1 = ((420.0, 1030.0, CUBOS[0]), (650.0, 1040.0, CUBOS[2]), (560.0, 1072.0, CUBOS[3]))
CAM_Q0 = (1.4, 540.0, 893.0)
CAM_L1 = (1.0, 560.0, 772.0)
CAM_CHEC1 = (1.32, 400.0, 866.0)            # a criança vai para a direita: o carimbo cabe à esquerda
CAM_VEZ = (1.10, 450.0, 800.0)              # ainda à direita: o carimbo DE VEZ EM QUANDO não encosta na cabeça
CAM_ANDA = (1.25, 600.0, 800.0)             # perto das pernas retas, andando


def t_l1(t, T):
    """Tempo efetivo do lance 1 (o quadro congela de 'pode?' até o veredito)."""
    if T["pode1"] <= t < T["validado1"]:
        return T["pode1"]
    return t


def pose_l1(t, T):
    """(pose, posição) da criança no lance 1."""
    tt = t_l1(t, T)
    x = POS1[0]
    if tt < T["var"]:
        return dict(W_BLOCO), POS1
    if tt < T["var"] + 0.5:                               # rebobina: do W de volta a ficar de pé
        u = prog(tt, T["var"], T["var"] + 0.5)
        p = mix(W_BLOCO, AGACHA, e_inout(u * 2)) if u < 0.5 else mix(dict(AGACHA, bloco=1.0), PE_BLOCO, e_inout(u * 2 - 1))
        p["bloco"] = 1.0
        return p, POS1
    ts = T["sentar"]
    if tt < ts:
        p = dict(PE_BLOCO); p["pel"] = (0.0, -170 + 3 * math.sin(tt * 6))
        return p, POS1
    if tt < ts + 0.85:                                    # desce para o tapete
        p = seq(tt, [(ts, PE_BLOCO), (ts + 0.4, dict(AGACHA, bloco=1.0)), (ts + 0.85, W_BLOCO)])
        p["bloco"] = 1.0
        return p, POS1
    tv = T["vez"]
    if tt < tv - 0.04:                                    # brinca com o bloco no colo
        p = dict(W_BLOCO)
        b = 6 * math.sin((tt - ts) * 7)
        p["mE"] = (W_BLOCO["mE"][0], W_BLOCO["mE"][1] + b); p["mD"] = (W_BLOCO["mD"][0], W_BLOCO["mD"][1] + b)
        return p, POS1
    if tt < tv + 0.26:                                    # folheado: cruzada, de lado, W (variar a posição)
        return dict(CRUZADA), POS1
    if tt < tv + 0.56:
        return dict(DE_LADO), POS1
    tn = T["nao1"]
    if tt < tn:                                           # de volta ao W, sem o bloco
        return dict(W_SENTA), POS1
    if tt < tn + 0.6:                                     # "não vira deformidade": levanta SOZINHA
        return seq(tt, [(tn, W_SENTA), (tn + 0.3, AGACHA), (tn + 0.6, PE)]), POS1
    ta = tn + 0.6; tf = ta + 0.75                         # e anda dois passos, pernas retas
    if tt < tf:
        u = prog(tt, ta, tf)
        x = lerp(POS1[0], X_ANDA, e_inout(u))
        return passo(PE, u * 2.0, 1.0), (x, POS1[1])
    return dict(PE), (X_ANDA, POS1[1])


def cam_l1(t, T):
    if t < T["var"]:
        return CAM_Q0
    cam = lerp3(CAM_Q0, CAM_L1, e_inout(prog(t, T["var"], T["var"] + 0.55)))
    cam = lerp3(cam, CAM_CHEC1, e_inout(prog(t, T["pode1"] + 0.05, T["pode1"] + 0.55)))
    cam = lerp3(cam, CAM_VEZ, e_inout(prog(t, T["validado1"] + 0.5, T["vez"] + 0.1)))
    cam = lerp3(cam, CAM_ANDA, e_inout(prog(t, T["nao1"] + 0.2, T["nao1"] + 1.3)))
    return cam


def cena_l1(cv, t, T):
    cam = cam_l1(t, T)
    pose, pos = pose_l1(t, T)
    cv.save(); aplica(cv, cam)
    sala(cv, "eva")
    tt = t_l1(t, T)
    some_cubos = 1.0
    for (x, y, cor) in CUBOS1:
        cubo(cv, x, y, 26, cor, some_cubos)
    if tt >= T["vez"] - 0.04:                             # o bloco que ela soltou, no chão ao lado
        cubo(cv, 470, 975, 26, CUBOS[1])
    verde = prog(tt, T["deformidade"] - 0.05, T["deformidade"] + 0.25)     # pernas retas: contorno verde
    crianca(cv, pose, pos, K1, verde=verde)
    cv.restore()
    return dict(lance=1, cam=cam, pose=pose, pos=pos, k=K1)


def cena_l1_mini(cv, rect, a=1.0):
    """Um mini-quadro (rect em tela) com a criança SEMPRE em W no tapete de EVA."""
    x0, y0, x1, y1 = rect
    cam = (0.62 * (x1 - x0) / 300.0, 540.0, 850.0)
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 16, 16)
    cv.save(); cv.clipRRect(rr, skia.ClipOp.kIntersect, True)
    cx_, cy_ = (x0 + x1) / 2, (y0 + y1) / 2
    cv.translate(cx_, cy_); cv.scale(cam[0], cam[0]); cv.translate(-cam[1], -cam[2])
    sala(cv, "eva")
    for (x, y, cor) in CUBOS1:
        cubo(cv, x, y, 26, cor)
    crianca(cv, W_BLOCO, POS1, K1)
    jw = juntas_mundo(W_BLOCO, POS1, K1)
    traco_tele(cv, [jw[n] for n in ("tE", "aE", "kE", "virilha", "kD", "aD", "tD")], 1.0, a, larg=13, caneta=False)
    cv.restore()
    return cam


# ================================================================== LANCE 2 — o filho do vizinho
K2 = 0.80
POS2 = (318.0, 872.0)
VIZ_X = 900.0
VIZ_Y0, VIZ_Y1 = 950.0, 1050.0                  # o vizinho anda À FRENTE (mais baixo no quadro): a "vantagem"
VIZ_K0, VIZ_K1 = 0.84, 0.92
CAM_L2 = (1.0, 540.0, 772.0)
CAM_CHEC2 = (1.05, 585.0, 830.0)            # as duas inteiras no quadro, cada uma do seu lado da cerca
CAM_L2_CERTO = (1.28, 300.0, 748.0)
ABERTO_ANDA = P(mE=(-128.0, -270.0), mD=(128.0, -270.0))


def t_l2(t, T):
    if T["pode2"] <= t < T["anulado"]:
        return T["pode2"]
    return t


def viz_l2(t, T):
    """(pose, pos, k) da criança do vizinho: passos soltos vindo para a frente; depois, no ritmo dela."""
    tt = t_l2(t, T)
    t0 = T["corte2"]
    u = prog(tt, t0, T["pode2"])
    y = lerp(VIZ_Y0, VIZ_Y1, u)
    k = lerp(VIZ_K0, VIZ_K1, u)
    fase = (tt - t0) * 1.7
    return passo(ABERTO_ANDA, fase, 1.0), (VIZ_X, y), k


def nossa_l2(t, T):
    tt = t_l2(t, T)
    p = dict(NO_SOFA)
    b = 4 * math.sin(tt * 4.2)
    p["pel"] = (0.0, -170 + b); p["kE"] = (-36.0, -92 + b * 0.5); p["kD"] = (36.0, -92 + b * 0.5)
    return p


def cam_l2(t, T):
    """Aproxima no 'pode?' e FICA: as duas crianças seguem no quadro até o replay (ninguém sai)."""
    return lerp3(CAM_L2, CAM_CHEC2, e_inout(prog(t, T["pode2"] + 0.05, T["pode2"] + 0.55)))


def linhas_l2(T, t=None):
    """y (mundo) das duas linhas de impedimento, no pé da FRENTE de cada criança: (nossa, vizinho)."""
    _, pos_v, k_v = viz_l2(T["pode2"] if t is None else t, T)
    return POS2[1] + 12 * K2, pos_v[1] + 12 * k_v


def linha_impedimento(cv, t, T, a_extra=1.0):
    """A LINHA DE IMPEDIMENTO do VAR: uma linha no pé da frente de cada criança (o vizinho está À FRENTE) e a
    faixa ciano preenchendo o vão entre elas — a "vantagem" que os pais medem. Pulsa no CHECANDO; no ANULADO o
    carimbo cai NA FAIXA (entre as duas, na altura da cerca), ela racha dos dois lados e apaga."""
    k = e_out(prog(t, T["comparar"] - 0.04, T["comparar"] + 0.55))
    a = k * (1 - prog(t, T["anulado"] + 0.55, T["anulado"] + 1.0)) * a_extra
    if a <= 0:
        return None
    y_n, y_v = linhas_l2(T, t)
    ym = (y_n + y_v) / 2
    xc = cerca_x(ym)
    x0, x1 = xc - 1000 * k, xc + 1000 * k
    pul = 0.5 + 0.5 * math.sin(t * 8) if T["pode2_fim"] < t < T["anulado"] else 0.0
    faixa = poli([(x0, y_n), (x1, y_n), (x1, y_v), (x0, y_v)])
    cv.drawPath(faixa, paint(CIANO, int((60 + 55 * pul) * a)))
    for y in (y_v, y_n):
        cv.drawLine(x0, y, x1, y, paint(CARTAO, int(150 * a), "stroke", 12))
        cv.drawLine(x0, y, x1, y, paint(CIANO, int(255 * a), "stroke", 6))
    rach = prog(t, T["anulado"] + 0.1, T["anulado"] + 0.32)
    if rach > 0:                                          # rachaduras em zigue-zague dos dois lados do carimbo
        for xm in (xc - 212, xc + 212):
            pts = [(xm, y_n - 14)]
            for i in range(1, 6):
                pts.append((xm + (-14 if i % 2 else 14), lerp(y_n, y_v, i / 6)))
            pts.append((xm, y_v + 14))
            pth, _ = polilinha_parcial(pts, rach)
            cv.drawPath(pth, paint(CARTAO, int(255 * a), "stroke", 9))
            cv.drawPath(pth, paint("#FFFFFF", int(230 * a), "stroke", 3))
    return (xc, ym)


def palminhas(cv, t, t0, base, a=1.0):
    """Mãos adultas (manga teal), na altura da criança, batendo palminhas baixas duas vezes."""
    if a <= 0:
        return
    bate = 0.0
    for tb in (t0 + 0.12, t0 + 0.42):
        bate = max(bate, max(0.0, 1 - abs(t - tb) / 0.12))
    abre = 26 * (1 - bate) + 4
    x, y = base
    for lado, dy, ang in ((1, 16.0, 38.0), (-1, 0.0, 18.0)):       # os antebraços vêm do canto de baixo, à direita
        hx = x + lado * abre
        pulso = (hx + 36, y + 42 + dy)
        ponta_ = (hx - 6, y - 44 + dy)
        antebraco_adulto(cv, pulso, ang, 230.0, a, esc=0.82)
        mao_adulto(cv, pulso, ponta_, a, lado=lado, esc=1.0)
    if bate > 0.3:
        for ang in (-60, -90, -120):
            r0, r1 = 64, 90
            c = math.cos(math.radians(ang)); s = math.sin(math.radians(ang))
            cv.drawLine(x + c * r0, y - 40 + s * r0, x + c * r1, y - 40 + s * r1, paint("#FFFFFF", int(230 * a * bate), "stroke", 5))


def cena_l2(cv, t, T, certo=False):
    if certo:
        cam = CAM_L2_CERTO
    else:
        cam = cam_l2(t, T)
    cv.save(); aplica(cv, cam)
    quintal(cv)
    x_viz = 0.0                                           # ninguém sai do quadro
    a_raia = prog(t, T["ritmo"] - 0.05, T["ritmo"] + 0.3)
    brilho = janela(t, T["individual"] - 0.05, T["individual_fim"] + 0.4, 0.2, 0.3)
    cerca(cv, 1 - a_raia * 0.85)
    raias(cv, a_raia * (0.0 if certo else 1.0), x_viz, t, brilho)
    pose_v, pos_v, k_v = viz_l2(t, T)
    marca = None
    if not certo:
        if a_raia > 0:                                    # cada raia com o seu compasso
            pulso_raia(cv, POS2[0], POS2[1], 1.0, t, 1.05, a_raia)
            pulso_raia(cv, pos_v[0], pos_v[1], 1.1, t, 0.58, a_raia, 0.2)
        marca = linha_impedimento(cv, t, T)
    if certo:                                             # replay: passo de lado, apoiada no sofá
        tc = T["wipe2"]
        u = prog(t, tc + 0.1, tc + 0.65)
        p = dict(NO_SOFA)
        if 0 < u < 1:
            p = passo(NO_SOFA, 0.5 * u + 0.0, 0.8)
        dx = -34 * e_inout(u)
        p["mE"] = (NO_SOFA["mE"][0] - dx * 0.0, NO_SOFA["mE"][1])
        crianca(cv, p, (POS2[0] + dx, POS2[1]), K2, verde=0.0)
        palminhas(cv, t, tc + 0.1, (POS2[0] + 200, POS2[1] - 130), 1.0)
    else:
        crianca(cv, nossa_l2(t, T), POS2, K2)
        crianca(cv, pose_v, pos_v, k_v, e=EST_VIZ)
    cv.restore()
    return dict(lance=2, cam=cam, viz=(pose_v, (pos_v[0] + x_viz, pos_v[1]), k_v), marca=marca, certa=certo)


# ================================================================== LANCE 3 — treinar e cair
K3 = 0.95
Y3 = 950.0
X3_0, X3_1 = 420.0, 560.0
CAM_L3 = (1.0, 545.0, 772.0)
CAM_CHEC3 = (1.22, 410.0, 850.0)
CAM_L3R = (1.08, 450.0, 790.0)              # a criança à direita: o carimbo ESPAÇO SEGURO sai sem tocar nela
CANTO_MESA = (MESA_X0, MESA_CHAO - MESA_ALT + 14)


def t_l3(t, T):
    if T["pode3"] <= t < T["validado2"]:
        return T["pode3"]
    return t


def balanco_l3(t, T):
    """Inclinação do tronco (graus) da equilibrista: amplitude do arco de oscilação."""
    tt = t_l3(t, T)
    amp = 7.0
    amp += 6.0 * prog(tt, T["cair1"] - 0.1, T["cair1"] + 0.3)
    return amp, amp * math.sin(tt * 7.5)


def pose_l3(t, T):
    tt = t_l3(t, T)
    t0 = T["corte3"]; tq = T["pode3"] - 0.5
    amp, inc = balanco_l3(t, T)
    if tt < tq:                                           # passos bambos, braços abertos
        u = prog(tt, t0 + 0.15, T["cair1"] + 0.35)
        x = lerp(X3_0, X3_1, e_inout(u))
        p = passo(ABERTO, u * 3.0, 1.0) if 0 < u < 1 else dict(ABERTO)
        p["inc"] = p["inc"] + inc
        return p, (x, Y3), dict(amp=amp, ang=inc)
    if tt < T["pode3"] + 0.01:                            # perde o equilíbrio para trás e senta
        p = seq(tt, [(tq, dict(ABERTO, inc=inc)), (T["pode3"], NO_AR)])
        return p, (X3_1, Y3), dict(amp=amp, ang=lerp(inc, -amp, prog(tt, tq, T["pode3"])))
    tv = T["validado2"]
    if tt < tv + 0.8:                                     # senta de bumbum no tapete e levanta sozinha
        p = seq(tt, [(tv, NO_AR), (tv + 0.2, SENTADA), (tv + 0.42, SENTADA), (tv + 0.62, AGACHA), (tv + 0.8, ABERTO)])
        return p, (X3_1, Y3), None
    tr = T["cada1"]; te = T["equilibrio"]
    if tt < te:                                           # replay ▶▶: cai, senta, levanta — e o arco estreita
        cic = ciclos_replay(T)
        for (a0, sent, a1, amp0, amp1) in cic:
            if tt < a1 or (a0, sent, a1, amp0, amp1) == cic[-1]:
                break
        tt_ = max(tt, a0)
        p = seq(tt_, [(a0, ABERTO), (sent - 0.1, NO_AR), (sent, SENTADA), (sent + 0.1, AGACHA), (a1, ABERTO)])
        amp_r = lerp(amp0, amp1, e_inout(prog(tt, sent + 0.1, a1)))
        de_pe = 1 - janela(tt, sent - 0.12, a1 - 0.06, 0.05, 0.06)
        ang = amp_r * math.sin((tt - tr) * 18.0) * de_pe
        p["inc"] = p["inc"] + ang
        return p, (X3_1, Y3), dict(amp=amp_r, ang=ang, ff=True)
    p = seq(tt, [(te, ABERTO), (te + 0.6, PE)])
    a2 = 3.5                                              # o arco estreito (mas legível) fica verde
    return p, (X3_1, Y3), dict(amp=a2, ang=0.0, verde=prog(tt, te - 0.05, te + 0.25))


def ciclos_replay(T):
    """Os 2 tombos do replay ▶▶: (de pé, bumbum no tapete, de pé de novo, amplitude antes, depois). O 1º bumbum
    no tapete cai em "queda"; a cada levantada o arco estreita (12 -> 7,5 -> 3,5)."""
    tr, tq, te = T["cada1"], T["queda"], T["equilibrio"]
    a1 = tq + 0.3
    s2 = a1 + (te - a1) * 0.45
    return ((tr, tq, a1, 12.0, 7.5), (a1, s2, te, 7.5, 3.5))


def cam_l3(t, T):
    cam = lerp3(CAM_L3, CAM_CHEC3, e_inout(prog(t, T["pode3"] + 0.05, T["pode3"] + 0.55)))
    cam = lerp3(cam, CAM_L3R, e_inout(prog(t, T["validado2"] + 0.5, T["validado2"] + 1.1)))
    return cam


def cena_l3(cv, t, T):
    cam = cam_l3(t, T)
    pose, pos, arco = pose_l3(t, T)
    cv.save(); aplica(cv, cam)
    sala(cv, "tapete")
    a_t = janela(t, T["espaco"] - 0.04, T["pode3"] - 0.1, 0.12, 0.3)
    if a_t > 0:                                          # 'espaço': o chão livre, contornado no próprio tapete
        pth = suave(TAPETE_PTS)
        k_t = e_out(prog(t, T["espaco"] - 0.04, T["espaco"] + 0.5))
        cv.drawPath(pth, _trim(paint(CARTAO, int(120 * a_t), "stroke", 15), k_t))
        cv.drawPath(pth, _trim(paint(CIANO, int(110 * a_t), "stroke", 22, blur=8), k_t))
        cv.drawPath(pth, _trim(paint(CIANO, int(255 * a_t), "stroke", 8), k_t))
    tq = T["pode3"] - 0.5
    a_ml = prog(t, tq + 0.1, tq + 0.3) * (1 - prog(t, T["validado2"], T["validado2"] + 0.12))
    if a_ml > 0:                                         # linhas de movimento: ela está DESCENDO (sentada)
        jw = juntas_mundo(pose, pos, K3)
        bx, by = jw["pel"]
        for dx, l_ in ((-92, 70), (-70, 100), (70, 100), (92, 70)):
            x = bx + dx * K3
            cv.drawLine(x, by - 120 * K3, x, by - (120 + l_) * K3, paint("#FFFFFF", int(230 * a_ml), "stroke", 7))
    crianca(cv, pose, pos, K3)
    cv.restore()
    return dict(lance=3, cam=cam, pose=pose, pos=pos, k=K3, arco=arco)


# ================================================================== HUD do VAR (cópia do piloto / episódios)
def fundo(cv, t):
    def _d(c):
        sh = skia.GradientShader.MakeRadial(skia.Point(W / 2, H * 0.42), H * 0.75, [_c(ARD_IN), _c(ARD_OUT)])
        c.drawRect(skia.Rect(0, 0, W, H), paint(ARD_IN, shader=sh))
    cv.drawImage(cacheado("fundo", W, H, _d), 0, 0)


def vinheta(cv):
    def _d(c):
        c.translate(-JX0, -JY0)
        vin = skia.GradientShader.MakeRadial(skia.Point(JCX, JCY), 760, [_c("#000000", 0), _c("#000000", 0), _c("#000000", 90)],
                                             [0.0, 0.62, 1.0])
        c.drawRect(JAN, paint("#000000", shader=vin))
    cv.drawImage(cacheado("vinheta", JX1 - JX0, JY1 - JY0, _d), JX0, JY0)


def capa(cv, t, t_sai, linha1, linha2):
    """Gancho de 2 linhas ACIMA do monitor (não encosta na janela da cena)."""
    sai = e_inout(prog(t, t_sai, t_sai + 0.45))
    if sai >= 1:
        return
    a = 1 - sai
    pulso = 1 + 0.02 * math.sin(t * 5)
    cv.save(); cv.translate(CX, 168 - 50 * sai); cv.scale(pulso, pulso)
    texto(cv, linha1, 0, 0, F_BLACK, 74, "#FFFFFF", int(255 * a), contorno=10)
    texto(cv, linha2, 0, 84, F_BLACK, 74, "#F5C04A", int(255 * a), contorno=10)
    cv.restore()


def moldura(cv, t, a, varre=0.0):
    if a <= 0:
        return
    rr = skia.RRect.MakeRectXY(JAN, JAN_R, JAN_R)
    cv.drawRRect(rr, paint(CIANO, int(70 * a), "stroke", 2))
    cv.save(); cv.clipRRect(rr, skia.ClipOp.kIntersect, True)
    inner = skia.RRect.MakeRectXY(skia.Rect(JX0 + 36, JY0 + 36, JX1 - 36, JY1 - 36), 10, 10)
    cv.clipRRect(inner, skia.ClipOp.kDifference, True)
    off = (t * 24) % 6
    y = JY0 + off
    pl = paint("#FFFFFF", int(26 * a), "stroke", 2)
    while y < JY1:
        cv.drawLine(JX0, y, JX1, y, pl); y += 6
    cv.restore()
    if varre > 0:
        cv.save(); cv.clipRRect(rr, skia.ClipOp.kIntersect, True)
        y = lerp(JY0 - 80, JY1 + 20, varre)
        sh = skia.GradientShader.MakeLinear([skia.Point(0, y - 70), skia.Point(0, y + 10)],
                                            [_c(CIANO, 0), _c(CIANO, int(70 * a)), _c(CIANO, 0)], [0.0, 0.8, 1.0])
        cv.drawRect(skia.Rect(JX0, y - 70, JX1, y + 10), paint(CIANO, shader=sh))
        cv.drawLine(JX0, y, JX1, y, paint(CIANO, int(120 * a), "stroke", 2))
        cv.restore()
    for (x, y, sx, sy) in ((JX0, JY0, 1, 1), (JX1, JY0, -1, 1), (JX0, JY1, 1, -1), (JX1, JY1, -1, -1)):
        p = skia.Path(); p.moveTo(x + 6 * sx, y + 76 * sy); p.lineTo(x + 6 * sx, y + 6 * sy); p.lineTo(x + 76 * sx, y + 6 * sy)
        cv.drawPath(p, paint("#000000", int(110 * a), "stroke", 13, blur=3))
        cv.drawPath(p, paint("#FFFFFF", int(255 * a), "stroke", 7))
        cv.drawPath(p, paint(CIANO, int(255 * a), "stroke", 2))


def selo_var(cv, t, x, y, esc, a, chip=None, a_chip=1.0, pontos=-1.0, cor_chip="#FFFFFF", flash=0.0):
    """Caixa VAR + chip de estado à direita (x, y = canto sup. esq.)."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    f = skia.Font(F_BLACK, 52); lw = f.measureText(T_VAR)
    rr = skia.RRect.MakeRectXY(skia.Rect(0, 0, lw + 36, 64), 10, 10)
    cv.drawRRect(rr, paint("#000000", int(100 * a), blur=10))
    cv.drawRRect(rr, paint(SELO_BG, int(250 * a)))
    cv.drawRRect(rr, paint(CIANO, int(255 * a), "stroke", 4))
    texto(cv, T_VAR, 18, 52, F_BLACK, 52, "#FFFFFF", int(255 * a), centro=False)
    if chip and a_chip > 0:
        aa = a * a_chip
        fc = skia.Font(F_BLACK, 34); cw = fc.measureText(chip)
        extra = 70 if pontos >= 0 else 0
        x0 = lw + 50
        r2 = skia.RRect.MakeRectXY(skia.Rect(x0, 8, x0 + cw + 70 + extra, 56), 24, 24)
        cv.drawRRect(r2, paint(CARTAO, int(235 * aa)))
        if flash > 0:
            cv.drawRRect(r2, paint("#FFFFFF", int(200 * flash * aa)))
        cv.drawRRect(r2, paint(cor_chip, int((230 if cor_chip != "#FFFFFF" else 60) * aa), "stroke", 3 if cor_chip != "#FFFFFF" else 2))
        pisca = 0.55 + 0.45 * math.sin(t * 9)
        ponto = cor_chip if cor_chip != "#FFFFFF" else CIANO
        cv.drawCircle(x0 + 26, 32, 8, paint(ponto, int(255 * aa * (1.0 if cor_chip != "#FFFFFF" else pisca))))
        texto(cv, chip, x0 + 46, 44, F_BLACK, 34, cor_chip, int(255 * aa), centro=False)
        if pontos >= 0:
            for i in range(3):
                acesa = pontos > i / 3 + 0.02
                cv.drawCircle(x0 + 46 + cw + 22 + i * 22, 33, 7, paint(CIANO if acesa else "#FFFFFF", int(255 * aa) if acesa else int(70 * aa)))
    cv.restore()


def icone_pausa(cv, x, y, a):
    if a <= 0:
        return
    for dx in (-14, 14):
        r = skia.RRect.MakeRectXY(skia.Rect(x + dx - 8, y - 26, x + dx + 8, y + 26), 4, 4)
        cv.drawRRect(r, paint("#000000", int(110 * a), blur=6))
        cv.drawRRect(r, paint(CIANO, int(255 * a)))


def icone_rebobina(cv, x, y, a, avanca=False):
    """Rebobina (◀◀) ou, com `avanca`, o replay acelerado (▶▶): desenho, sem texto."""
    if a <= 0:
        return
    for dx in (-24, 8):
        if avanca:
            p = poli([(x + dx - 8, y - 24), (x + dx - 8, y + 24), (x + dx + 26, y)])
        else:
            p = poli([(x + dx + 26, y - 24), (x + dx + 26, y + 24), (x + dx - 8, y)])
        cv.drawPath(p, paint("#000000", int(110 * a), blur=6))
        cv.drawPath(p, paint(CIANO, int(255 * a)))


def circulo_tele(cv, x, y, rx, ry, k, a, seed=0.0, pulso=0.0, cor=CIANO):
    """Círculo de caneta do telestrador: traço com tremor, desenhado em `k` (0..1)."""
    if a <= 0 or k <= 0:
        return
    n = 72
    pts = []
    for i in range(n + 10):
        u = i / n
        ang = -math.pi * 0.62 + 2 * math.pi * u
        wob = 1 + 0.035 * math.sin(u * 2 * math.pi * 3 + seed) + 0.018 * math.sin(u * 2 * math.pi * 7 + 2 * seed)
        sp = 1 + 0.07 * u
        esc = (1 + 0.05 * pulso) * wob * sp
        pts.append((x + rx * esc * math.cos(ang), y + ry * esc * math.sin(ang)))
    p = poli(pts, fechar=False)
    cv.drawPath(p, _trim(paint(CARTAO, int(150 * a), "stroke", 15), k))
    cv.drawPath(p, _trim(paint(cor, int(110 * a * (0.6 + 0.4 * pulso)), "stroke", 18, blur=8), k))
    cv.drawPath(p, _trim(paint(cor, int(255 * a), "stroke", 8), k))


def traco_tele(cv, pts, k, a, cor=CIANO, larg=8, caneta=True):
    """Traço TRACEJADO do telestrador ao longo de uma polilinha, desenhado até `k` (o W nas pernas)."""
    if a <= 0 or k <= 0:
        return
    pth, q = polilinha_parcial(pts, k)
    for cor_, l_, al in ((CARTAO, larg + 8, 150), (cor, larg, 255)):
        pt = paint(cor_, int(al * a), "stroke", l_)
        pt.setStrokeJoin(skia.Paint.kRound_Join)
        pt.setPathEffect(skia.DashPathEffect.Make([24.0, 13.0], 0.0))
        cv.drawPath(pth, pt)
    if caneta and k < 0.999:
        cv.drawCircle(q[0], q[1], larg * 1.4, paint(cor, int(120 * a), blur=6))
        cv.drawCircle(q[0], q[1], larg * 0.9, paint("#FFFFFF", int(255 * a)))


def carimbo_cor(cv, s, x, y, rot, t0, t, dur, cor, tam=88, esc0=1.9, sub=None, tam_sub=44):
    """Carimbo do veredito (cópia do cf_var_gesso, com a 2ª linha da condição). O retângulo inteiro (escala
    da batida incluída) fica sempre dentro de x em [44, W-44]: na batida o centro desliza, nunca corta."""
    k = t - t0
    if k < 0 or k > dur:
        return
    esc = lerp(esc0, 1.0, e_out(clamp(k / 0.16)))
    sai = prog(k, dur - 0.28, dur)
    esc *= lerp(1.0, 0.35, e_inout(sai))
    a = clamp(k / 0.06) * (1 - sai)
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    baixo = tam * 0.38 + (tam_sub * 1.25 if sub else 0)
    lw2 = skia.Font(F_BLACK, tam_sub).measureText(sub) if sub else 0
    meia = max(lw, lw2) / 2
    meia_tela = (meia + 32) * esc * 1.02 + 6                  # meia largura na tela (+ a rotação de 5°)
    x = min(max(x, 44 + meia_tela), W - 44 - meia_tela)
    xx = lerp(x, 330, e_inout(sai)); yy = lerp(y, 180, e_inout(sai))
    cv.save(); cv.translate(xx, yy); cv.rotate(rot * (1 - sai)); cv.scale(esc, esc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-meia - 32, -tam * 1.02, meia + 32, baixo), 16, 16)
    cv.drawRRect(rr, paint("#000000", int(110 * a), blur=16))
    cv.drawRRect(rr, paint(CARTAO, int(245 * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 9))
    rr2 = skia.RRect.MakeRectXY(skia.Rect(-meia - 20, -tam * 0.9, meia + 20, baixo - tam * 0.12), 10, 10)
    cv.drawRRect(rr2, paint(cor, int(120 * a), "stroke", 2.5))
    cv.drawString(s, -lw / 2, 0, f, paint(cor, int(255 * a)))
    if sub:
        cv.drawLine(-meia + 6, tam * 0.2, meia - 6, tam * 0.2, paint(cor, int(150 * a), "stroke", 2.5))
        texto(cv, sub, 0, tam * 0.2 + tam_sub * 1.02, F_BLACK, tam_sub, "#FFFFFF", int(255 * a))
    cv.restore()


def ruido_vhs(cv, t, a):
    if a <= 0:
        return
    rng = np.random.default_rng(int(t * 60))
    cv.save(); cv.clipRRect(skia.RRect.MakeRectXY(JAN, JAN_R, JAN_R), skia.ClipOp.kIntersect, True)
    for k in range(3):
        yc = JY0 + ((t * (900 + 300 * k) + k * 330) % (JY1 - JY0))
        hb = 14 + 8 * k
        cv.drawRect(skia.Rect(JX0, yc, JX1, yc + hb), paint("#FFFFFF", int(40 * a)))
        for _ in range(26):
            x = rng.uniform(JX0, JX1); w = rng.uniform(10, 90); yy = yc + rng.uniform(0, hb)
            cv.drawLine(x, yy, x + w, yy, paint("#FFFFFF", int(rng.uniform(80, 200) * a), "stroke", rng.uniform(1, 3)))
    cv.restore()


def apito_icone(cv, x, y, esc, a, rot=-14.0):
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(esc, esc)
    cv.drawArc(skia.Rect(-96, -40, -24, 40), 60, 240, False, paint(CIANO, int(230 * a), "stroke", 6))
    corpo_ = skia.Path(); corpo_.addCircle(0, 6, 38)
    corpo_ = uniao(corpo_, rr_path(-6, -34, 92, 2, 10))
    cv.drawPath(corpo_, paint("#000000", int(100 * a), blur=10))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, -34), skia.Point(0, 44)], [_c("#F4F8FB"), _c("#B9C6D3")])
    cv.drawPath(corpo_, paint("#DDE6EE", int(255 * a), shader=sh))
    cv.drawPath(corpo_, paint(CIANO, int(255 * a), "stroke", 4))
    cv.drawCircle(-4, 10, 13, paint(SELO_BG, int(255 * a)))
    cv.drawRect(skia.Rect(70, -30, 86, -2), paint(SELO_BG, int(200 * a)))
    cv.drawCircle(-40, 0, 7, paint(CIANO, int(255 * a), "stroke", 4))
    cv.restore()


def profissional(cv, x, y, esc, a, mao_k=1.0):
    """Profissional de saúde de frente, sem rosto (cópia do cf_var_primeiros_socorros): jaleco, estetoscópio e
    a mão erguida (onde o apito pousa)."""
    if a <= 0:
        return None
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    om = (70, -6); cot = (128, -40); mao_p = (124, lerp(-60, -132, mao_k))
    pinta(cv, capsula(om, cot, 46, 40), om, cot, 46, ("#C9D3DE", "#EEF2F6", "#FFFFFF", "#EEF2F6", "#C9D3DE"), a, linha="#9AA8B6")
    pinta(cv, capsula(cot, mao_p, 40, 36), cot, mao_p, 40, ("#C9D3DE", "#EEF2F6", "#FFFFFF", "#EEF2F6", "#C9D3DE"), a, linha="#9AA8B6")
    mp = capsula((mao_p[0], mao_p[1] + 4), (mao_p[0] + 2, mao_p[1] - 26), 34, 30)
    pinta(cv, mp, (mao_p[0], mao_p[1] + 4), (mao_p[0], mao_p[1] - 26), 34, PELE_AD, a, linha=LINHA_AD)
    om_p = skia.Path(); om_p.addRRect(skia.RRect.MakeRectXY(skia.Rect(-96, -20, 96, 140), 70, 70))
    clip = skia.Path(); clip.addRect(skia.Rect(-110, -30, 110, 110))
    om_p = skia.Op(om_p, clip, skia.PathOp.kIntersect_PathOp)
    cv.drawPath(om_p, paint("#000000", int(80 * a), blur=10))
    shj = skia.GradientShader.MakeLinear([skia.Point(-96, 0), skia.Point(96, 0)], [_c("#D5DDE6"), _c("#FFFFFF"), _c("#D5DDE6")])
    cv.drawPath(om_p, paint("#F4F7FA", int(255 * a), shader=shj))
    cv.drawPath(om_p, paint("#9AA8B6", int(220 * a), "stroke", 3))
    cv.drawPath(poli([(-30, -16), (30, -16), (0, 46)]), paint(TEAL, int(255 * a)))
    cv.drawPath(poli([(-34, -18), (-6, 60), (-22, 108)], fechar=False), paint("#B9C6D3", int(255 * a), "stroke", 4))
    cv.drawPath(poli([(34, -18), (6, 60), (22, 108)], fechar=False), paint("#B9C6D3", int(255 * a), "stroke", 4))
    est = suave([(-30, -18), (-44, 30), (-30, 66), (0, 76), (14, 70)], fechar=False)
    cv.drawPath(est, paint("#5B6676", int(255 * a), "stroke", 6))
    cv.drawPath(suave([(30, -18), (40, 20), (34, 50)], fechar=False), paint("#5B6676", int(255 * a), "stroke", 6))
    cv.drawCircle(16, 74, 11, paint("#C6D3DF", int(255 * a))); cv.drawCircle(16, 74, 11, paint("#5B6676", int(255 * a), "stroke", 3))
    cv.drawCircle(0, -58, 40, paint("#000000", int(80 * a), blur=6))
    sh_c = skia.GradientShader.MakeRadial(skia.Point(-10, -70), 56, [_c(PELE_AD[2]), _c(PELE_AD[1]), _c(PELE_AD[0])], [0, 0.55, 1])
    cv.drawCircle(0, -58, 40, paint(PELE_AD[1], int(255 * a), shader=sh_c))
    cv.drawArc(skia.Rect(-42, -100, 42, -16), 190, 160, False, paint("#3A2A20", int(255 * a), "stroke", 16))
    cv.drawCircle(0, -104, 16, paint("#3A2A20", int(255 * a)))
    cv.restore()
    return (x + mao_p[0] * esc, y + (mao_p[1] - 22) * esc)


def profissional_com_apito(cv, t, cx, cy, esc, t_ent, t_apito, a, de=(140.0, 330.0)):
    """A profissional entra (anel verde) e o apito voa até a mão dela."""
    if a <= 0:
        return
    ent = e_back(prog(t, t_ent, t_ent + 0.4))
    cv.drawCircle(cx + 10, cy - 70 * esc, 175 * esc, paint(VERDE, int(40 * a), blur=40))
    k_anel = e_out(prog(t, t_apito - 0.05, t_apito + 0.35))
    pul = max(0.0, 1 - abs(t - t_apito - 0.3) / 0.25)
    cv.drawCircle(cx + 10, cy - 60 * esc, 150 * esc * (1 + 0.05 * pul),
                  _trim(paint(VERDE, int(255 * a), "stroke", 7 + 3 * pul), max(0.002, k_anel)))
    mk = e_out(prog(t, t_ent + 0.1, t_ent + 0.45))
    alvo = profissional(cv, cx, cy + 30 * (1 - clamp(ent)), esc * clamp(ent, 0, 1.1), a, mk)
    ka = e_out(prog(t, t_ent + 0.05, t_apito + 0.1))
    if ka > 0 and alvo is not None:
        x = lerp(de[0], alvo[0], ka); y = lerp(de[1], alvo[1], ka) - 60 * math.sin(math.pi * ka)
        balanco = 10 * math.sin(max(0.0, t - t_apito) * 9) * math.exp(-max(0.0, t - t_apito) * 3)
        apito_icone(cv, x, y, lerp(0.6, 0.85, ka) * esc / 1.6, a * clamp(ka * 3), -14 + balanco)


def selo_serie(cv, a):
    if a <= 0:
        return
    lw = larg_texto(T_SERIE, F_BLACK, 36)
    rr = skia.RRect.MakeRectXY(skia.Rect(CX - lw / 2 - 34, 148, CX + lw / 2 + 34, 208), 30, 30)
    cv.drawRRect(rr, paint(SELO_BG, int(235 * a)))
    cv.drawRRect(rr, paint(CIANO, int(255 * a), "stroke", 3))
    texto(cv, T_SERIE, CX, 191, F_BLACK, 36, CIANO, int(255 * a))


def marca_x(cv, x, y, r, cor, a):
    if a <= 0:
        return
    cv.drawCircle(x, y, r + 6, paint("#000000", int(90 * a), blur=8))
    cv.drawCircle(x, y, r, paint(CARTAO, int(235 * a)))
    cv.drawCircle(x, y, r, paint(cor, int(255 * a), "stroke", 5))
    d = r * 0.45
    cv.drawLine(x - d, y - d, x + d, y + d, paint(cor, int(255 * a), "stroke", 9))
    cv.drawLine(x - d, y + d, x + d, y - d, paint(cor, int(255 * a), "stroke", 9))


def marca_ok(cv, x, y, r, cor, a):
    if a <= 0:
        return
    cv.drawCircle(x, y, r + 6, paint("#000000", int(90 * a), blur=8))
    cv.drawCircle(x, y, r, paint(CARTAO, int(235 * a)))
    cv.drawCircle(x, y, r, paint(cor, int(255 * a), "stroke", 5))
    p = poli([(x - r * 0.45, y + r * 0.02), (x - r * 0.12, y + r * 0.35), (x + r * 0.5, y - r * 0.32)], fechar=False)
    pt = paint(cor, int(255 * a), "stroke", 9); pt.setStrokeCap(skia.Paint.kRound_Cap); pt.setStrokeJoin(skia.Paint.kRound_Join)
    cv.drawPath(p, pt)


def arco_oscilacao(cv, cx, cy, R, amp, ang, a, cor=CIANO, leque=1.0):
    """Arco de oscilação acima da cabeça: o leque (só uma faixa junto do arco, nunca sobre a criança) mostra o
    quanto o corpo balança; o ponto, para onde está. Estreito ou verde: só o traço do arco e o ponto."""
    if a <= 0:
        return
    amp = max(1.5, amp) * 2.2
    rect = skia.Rect(cx - R, cy - R, cx + R, cy + R)
    a_lq = leque * clamp((amp - 9.0) / 10.0)
    if a_lq > 0:
        lq = skia.Path(); lq.moveTo(cx, cy); lq.arcTo(rect, -90 - amp, 2 * amp, False); lq.close()
        cv.save(); cv.clipRect(skia.Rect(cx - R - 40, cy - R - 40, cx + R + 40, cy - R * 0.94), True)
        cv.drawPath(lq, paint(cor, int(40 * a * a_lq)))
        cv.restore()
    arc = skia.Path(); arc.addArc(rect, -90 - amp, 2 * amp)
    cv.drawPath(arc, paint(CARTAO, int(150 * a), "stroke", 15))
    cv.drawPath(arc, paint(cor, int(255 * a), "stroke", 8))
    for s in (-1, 1):
        q = math.radians(-90 + s * amp)
        cv.drawLine(cx + (R - 16) * math.cos(q), cy + (R - 16) * math.sin(q), cx + (R + 16) * math.cos(q), cy + (R + 16) * math.sin(q),
                    paint(cor, int(255 * a), "stroke", 6))
    q = math.radians(-90 + ang * 2.2)
    px, py = cx + R * math.cos(q), cy + R * math.sin(q)
    cv.drawCircle(px, py, 13, paint(CARTAO, int(200 * a)))
    cv.drawCircle(px, py, 9, paint("#FFFFFF", int(255 * a)))


# ================================================================== FECHO — os 4 pictogramas (âmbar, sem texto)
PICTO_GRANDE = (CX, 806.0)          # o sinal da vez: grande, no meio do monitor, junto da legenda que o diz
PICTO_ESC_GRANDE = 1.2
PICTO_FILA_Y = 418.0                # depois: miniatura na fileira do alto (fica até o fim, com a profissional)


def picto_vaga(i, final):
    return (CX + (i - 1.5) * 236.0, PICTO_FILA_Y), lerp(0.40, 0.46, final)


def _traco(cor, a, larg=8):
    pt = paint(cor, int(255 * a), "stroke", larg)
    pt.setStrokeJoin(skia.Paint.kRound_Join); pt.setStrokeCap(skia.Paint.kRound_Cap)
    return pt


def boneco(cv, x, y, esc, a, sentado=False, cor=AMBAR, tracejado=False):
    """Criança-pictograma (traço grosso, sem rosto): cabeça, tronco e pernas; de pé ou sentada. `tracejado`: o
    "fantasma" do que ela já fazia."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    pt = _traco(cor, a, 9)
    if tracejado:
        pt.setPathEffect(skia.DashPathEffect.Make([14.0, 11.0], 0.0))
    if sentado:
        cv.drawCircle(0, -112, 26, pt)
        cv.drawPath(rr_path(-30, -82, 30, -10, 22), pt)
        cv.drawPath(suave([(-26, -14), (-30, 6), (6, 8), (54, 6)], fechar=False), pt)
        cv.drawPath(suave([(26, -14), (30, 4), (60, 8), (72, 2)], fechar=False), pt)
        cv.drawLine(-28, -66, -58, -26, pt); cv.drawLine(28, -66, 58, -26, pt)
    else:
        cv.drawCircle(0, -150, 26, pt)
        cv.drawPath(rr_path(-30, -120, 30, -50, 22), pt)
        cv.drawLine(-14, -50, -18, 0, pt); cv.drawLine(14, -50, 18, 0, pt)
        cv.drawLine(-28, -104, -50, -64, pt); cv.drawLine(28, -104, 50, -64, pt)
    cv.restore()


def calendario(cv, x, y, esc, a, giros):
    """Folhinha de calendário (sem números): a folha da frente vira `giros` vezes (fração = virando)."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    pt = _traco(AMBAR, a, 8)
    base = rr_path(-70, -70, 70, 70, 12)
    cv.drawPath(base, paint(CARTAO, int(230 * a)))
    for dy in (6, 3):
        cv.drawPath(rr_path(-70 + dy, -70 + dy * 2, 70 + dy, 70 + dy * 2, 12), paint(AMBAR, int(70 * a), "stroke", 4))
    cv.drawPath(base, pt)
    cv.drawLine(-70, -36, 70, -36, pt)
    for gx in (-38, 0, 38):                                 # a grade (só casas vazias)
        for gy in (-8, 26, 56):
            cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(gx - 12, gy - 10, gx + 12, gy + 10), 3, 3), paint(AMBAR, int(150 * a), "stroke", 3))
    for rx in (-36, 36):
        cv.drawLine(rx, -86, rx, -58, _traco(AMBAR, a, 9))
    f = giros % 1.0
    if 0 < f < 0.98:                                       # a folha virando para cima
        h = 140 * math.cos(math.pi * f)
        fo = rr_path(-70, -70, 70, -70 + h, 10) if h > 0 else rr_path(-70, -70 + h, 70, -70, 10)
        cv.drawPath(fo, paint("#2A1E10", int(235 * a)))
        cv.drawPath(fo, _traco(AMBAR, a, 6))
    cv.restore()


def estrela(cv, x, y, r, a, acesa):
    if a <= 0:
        return
    pts = []
    for i in range(10):
        rr_ = r if i % 2 == 0 else r * 0.45
        q = -math.pi / 2 + i * math.pi / 5
        pts.append((x + rr_ * math.cos(q), y + rr_ * math.sin(q)))
    p = poli(pts)
    if acesa > 0:
        cv.drawPath(p, paint(AMBAR, int(110 * a * acesa), blur=14))
        cv.drawPath(p, paint(AMBAR, int(255 * a * acesa)))
    cv.drawPath(p, _traco(AMBAR, a * lerp(0.35, 1.0, acesa), 7))


def marquinha(cv, x, y, r, a):
    """Marquinha de tombo (estrelinha de impacto, sem texto)."""
    if a <= 0:
        return
    pt = _traco(AMBAR, a, 6)
    for i in range(6):
        q = i * math.pi / 3 + 0.3
        cv.drawLine(x + r * 0.35 * math.cos(q), y + r * 0.35 * math.sin(q), x + r * math.cos(q), y + r * math.sin(q), pt)


_SOLA = None


def _sola():
    p = skia.Path()
    p.moveTo(2, 58)
    p.cubicTo(-16, 58, -24, 44, -24, 26)
    p.cubicTo(-24, 8, -28, -10, -27, -26)
    p.cubicTo(-26, -44, -12, -52, 3, -52)
    p.cubicTo(19, -52, 28, -42, 26, -26)
    p.cubicTo(24, -12, 11, -3, 12, 14)
    p.cubicTo(13, 30, 21, 40, 18, 50)
    p.cubicTo(15, 56, 8, 58, 2, 58)
    p.close()
    return p


DEDOS = ((15, -67, 10.5), (0, -71, 7.6), (-11, -67, 6.8), (-20, -60, 6.2), (-27, -50, 5.4))


def pegadinha(cv, x, y, esc, cor, a, espelho=False, larg=4.5):
    """Pegadinha de bebê só no contorno (a do cf_andador / cf_quadril_bebe)."""
    global _SOLA
    if a <= 0:
        return
    if _SOLA is None:
        _SOLA = _sola()
    cv.save(); cv.translate(x, y); cv.scale(-esc if espelho else esc, esc)
    cv.drawPath(_SOLA, paint(cor, int(255 * a), "stroke", larg))
    for dx, dy, r in DEDOS:
        cv.drawCircle(dx, dy, r, paint(cor, int(255 * a), "stroke", larg * 0.8))
    cv.restore()


def pictogramas(cv, t, T, a=1.0, recua=0.0):
    """Os 4 sinais de alerta, um por fala: cada um entra GRANDE no centro enquanto a legenda o diz e, quando
    entra o próximo, encolhe para a sua vaga na fileira do alto. Em 'avaliação' a fileira dos 4 fica (um pouco
    maior) acima da profissional."""
    if a <= 0:
        return
    tempos = (T["nao2"] + 0.05, T["perder"] - 0.05, T["cair2"] - 0.05, T["tropecar"] - 0.05)
    fins = tempos[1:] + (T["avaliacao"] - 0.1,)
    for i in (3, 2, 1, 0):                                # a da vez (a mais nova) por cima
        t0 = tempos[i]
        k = e_back(prog(t, t0, t0 + 0.35))
        if k <= 0:
            continue
        vai = e_inout(prog(t, fins[i] - 0.05, fins[i] + 0.3))
        (vx, vy), ve = picto_vaga(i, recua)
        aa = a * clamp(k * 2)
        alvo = (lerp(PICTO_GRANDE[0], vx, vai), lerp(PICTO_GRANDE[1], vy, vai))
        esc = lerp(PICTO_ESC_GRANDE * clamp(k, 0, 1.15), ve, vai)
        cv.save(); cv.translate(*alvo); cv.scale(esc, esc)
        r = skia.RRect.MakeRectXY(skia.Rect(-226, -190, 226, 190), 26, 26)
        cv.drawRRect(r, paint("#000000", int(110 * aa * (1 - vai)), blur=24))
        cv.drawRRect(r, paint("#1A2532", int(235 * aa)))
        cv.drawRRect(r, paint(AMBAR, int(lerp(150, 110, vai) * aa), "stroke", lerp(4, 6, vai)))
        pul = max(0.0, 1 - abs(t - t0 - 0.3) / 0.3)
        if pul > 0:
            cv.drawRRect(r, paint(AMBAR, int(150 * aa * pul), "stroke", 8, blur=6))
        cv.translate(0, 6); cv.scale(1.16, 1.16)
        if i == 0:                                        # não andar: sentada + o calendário virando
            boneco(cv, -96, 112, 1.25, aa, sentado=True)
            giros = 3.0 * prog(t, t0 + 0.25, T["meses_fim"] + 0.1)
            calendario(cv, 104, -4, 1.0, aa, giros if giros < 3.0 else 0.0)
        elif i == 1:                                      # perder o que já fazia: de pé vira fantasma, a estrela apaga
            ka = prog(t, T["perder"] + 0.35, T["perder"] + 0.75)
            boneco(cv, -128, 130, 1.25, aa * (1 - ka), sentado=False)
            boneco(cv, -128, 130, 1.25, aa * ka * 0.75, sentado=False, tracejado=True)
            boneco(cv, -6, 112, 1.25, aa * ka, sentado=True)
            estrela(cv, 128, -66, 58, aa, 1 - ka)
        elif i == 2:                                      # cair cada vez mais: a pilha de marquinhas cresce
            boneco(cv, -100, 112, 1.25, aa, sentado=True)
            n = 1 + int(4 * prog(t, t0 + 0.2, T["tropecar"] - 0.2))
            for m in range(min(5, n)):
                marquinha(cv, 110 + (16 if m % 2 else -16), 120 - m * 56, 26, aa)
            cv.drawLine(186, 110, 186, -120, _traco(AMBAR, aa * prog(t, t0 + 0.3, t0 + 0.6), 7))
            ponta(cv, 186, -126, -math.pi / 2, 24, AMBAR, aa * prog(t, t0 + 0.3, t0 + 0.6))
        else:                                             # tropeçar sempre do mesmo lado: a marca cai no MESMO pé
            n = 6
            for m in range(n):
                km = prog(t, t0 + 0.08 + m * 0.18, t0 + 0.2 + m * 0.18)
                if km <= 0:
                    continue
                dirt = (m % 2 == 1)
                px_ = -40 + (70 if dirt else 0) + (m - 2.5) * 14
                py_ = 140 - m * 52
                pegadinha(cv, px_, py_, 0.62, "#DDE6EE", aa * km, espelho=not dirt, larg=4)
                if dirt:
                    marquinha(cv, px_ + 44, py_ - 18, 22, aa * km)
        cv.restore()


# ================================================================== legenda (cópia do cf_var_gesso)
LIGACAO = {"a", "o", "as", "os", "e", "de", "da", "do", "das", "dos", "em", "no", "na", "nos", "nas", "um", "uma",
           "pra", "que", "com", "é", "sua", "seu", "lá", "ele", "ou", "uns", "até", "já"}
ESP_LEG, LARG_LEG = 26, 920
TAM_LEG_3 = 64                                           # bloco de 3 linhas (a pergunta inteira) um pouco menor


def _base_tok(p):
    import re
    return re.sub(r"[.,:;!?—]", "", p["tok"]).lower()


def partir_linhas(bloco, tam):
    from itertools import combinations
    ws = [(p, larg_texto(p["tok"].upper(), F_BLACK, tam)) for p in bloco]

    def larg(seg):
        return sum(w for _, w in seg) + ESP_LEG * (len(seg) - 1)
    gul, linha, lw = [], [], 0
    for p, w in ws:
        if linha and lw + ESP_LEG + w > LARG_LEG:
            gul.append(linha); linha, lw = [], 0
        linha.append((p, w)); lw += (ESP_LEG if lw else 0) + w
    if linha:
        gul.append(linha)
    k = len(gul)
    if k <= 1 or len(ws) > 12:
        return gul
    melhor = None
    for cortes in combinations(range(1, len(ws)), k - 1):
        lims = (0,) + cortes + (len(ws),)
        lns = [ws[lims[j]:lims[j + 1]] for j in range(k)]
        if any(larg(ln) > LARG_LEG for ln in lns):
            continue
        sc = max(larg(ln) for ln in lns)
        for ln in lns[:-1]:
            if _base_tok(ln[-1][0]) in LIGACAO:
                sc += 400
            if ln[-1][0].get("virg"):
                sc -= 60
        if len(lns[-1]) == 1 and len(ws) > k:
            sc += 150
        if melhor is None or sc < melhor[0]:
            melhor = (sc, lns)
    return melhor[1] if melhor else gul


def montar_blocos_var(pal):
    """Blocos da legenda (lógica do cf_var_gesso): frase por frase; a pergunta 'pode?' gruda na frase que ela
    pergunta ('SENTAR EM W: PODE?' / 'QUE ANDOU ANTES: PODE?'); bloco de até 6 palavras e 2 linhas, dividido no
    melhor ponto (nunca depois de palavra de ligação, de preferência na vírgula). A CTA fica inteira."""
    frases, atual = [], []
    for p in pal:
        atual.append(p)
        if p["fim_frase"]:
            frases.append(atual); atual = []
    if atual:
        frases.append(atual)
    juntas_ = []
    for fr in frases:
        if juntas_ and len(fr) == 1 and fr[0]["tok"].endswith("?") and juntas_[-1][-1]["tok"].endswith(":"):
            juntas_[-1] = juntas_[-1] + fr
        elif len(fr) > 8 and fr[0]["w"].lower() != "manda":    # frase longa (o fecho): uma oração por vez
            atual = []
            for p in fr:
                atual.append(p)
                if p.get("virg"):
                    juntas_.append(atual); atual = []
            if atual:
                juntas_.append(atual)
        else:
            juntas_.append(fr)

    def dividir(fr):
        if fr[0]["w"].lower() == "manda" or (len(fr) <= 6 and len(partir_linhas(fr, 80)) <= 2):
            return [fr]
        if len(fr) <= 6 and len(partir_linhas(fr, TAM_LEG_3)) <= 2:
            return [fr]                                        # o sinal inteiro num bloco (letra um pouco menor)
        if fr[-1]["tok"].lower() == "pode?" and len(fr) <= 10 and len(partir_linhas(fr, TAM_LEG_3)) <= 3:
            return [fr]                                        # a pergunta inteira: "pode" o QUÊ fica na tela
        melhor = None
        for i in range(1, len(fr)):
            sc = abs(i - (len(fr) - i))
            if _base_tok(fr[i - 1]) in LIGACAO:
                sc += 100
            if fr[i - 1].get("virg"):
                sc -= 3
            if fr[-1]["tok"].endswith("?") and len(fr) - i <= 4:
                sc -= 2.5                                     # a pergunta fica com o que ela pergunta
            if _base_tok(fr[i]) in ("e", "mas", "ou", "pede"):          # corta ANTES de "ou"/"pede" (o sinal inteiro)
                sc -= 5
            if i == 1 or len(fr) - i == 1:
                sc += 3
            if i < len(fr) - i:
                sc += 0.25
            if melhor is None or sc < melhor[0]:
                melhor = (sc, i)
        i = melhor[1]
        return dividir(fr[:i]) + dividir(fr[i:])
    blocos = []
    for fr in juntas_:
        blocos += dividir(fr)
    return blocos


def legenda_var(cv, blocos, t, destaque, y_base=1395, tam=80, a_extra=1.0):
    import re
    if a_extra <= 0:
        return
    vivo = None
    for i, b in enumerate(blocos):
        ini = b[0]["t"] - 0.12
        fim = blocos[i + 1][0]["t"] - 0.12 if i + 1 < len(blocos) else b[-1]["t"] + b[-1]["d"] + 2.5
        if ini <= t < fim:
            vivo = b; break
    if not vivo:
        return
    esp = ESP_LEG
    linhas = partir_linhas(vivo, tam)
    if len(linhas) > 2:
        tam = TAM_LEG_3
        linhas = partir_linhas(vivo, tam)
    entrada = e_out(clamp((t - (vivo[0]["t"] - 0.12)) / 0.15))
    a_x = clamp(a_extra)
    alt = tam * 1.18
    y = y_base - (len(linhas) - 1) * alt / 2 + (1 - entrada) * 24
    for ln in linhas:
        total = sum(w for _, w in ln) + esp * (len(ln) - 1); x = CX - total / 2
        for p, w in ln:
            k = t - p["t"]; base = re.sub(r"[.,:;!?—]", "", p["tok"]).lower()
            dita = k >= -0.03; falando = p["t"] - 0.03 <= t <= p["t"] + p["d"] + 0.06
            cor, a = (OURO, 255) if falando else ((OURO if base in destaque else "#FFFFFF"), 255) if dita else ("#FFFFFF", 105)
            esc = 1.0 + (min(0.06, 14.0 / max(w, 1.0)) * (1 - e_out(clamp(k / 0.16))) if dita else 0.0)
            cv.save(); cv.translate(x + w / 2, y); cv.scale(esc, esc)
            texto(cv, p["tok"].upper(), -w / 2, 0, F_BLACK, tam, cor, int(a * entrada * a_x), centro=False, contorno=12)
            cv.restore()
            x += w + esp
        y += alt


def interface_var(cv, t, T, blocos, destaque):
    """Legenda (some durante os CHECANDO) + rodapé CFM desde 3 s + cartão final (cópia dos episódios)."""
    t_cta = T["manda"] - 0.15
    checando = any(T[pd + "_fim"] + 0.1 < t < T[vd] - 0.12 for pd, vd, *_ in VEREDITOS)
    checando = checando or T["wipe2"] + 0.12 < t < T["corte3"] + 0.1      # replay sem fala: só a imagem
    if t < t_cta and not checando:
        legenda_var(cv, blocos, t, destaque)
    if 3.0 <= t < t_cta:
        a = prog(t, 3.0, 3.6)
        texto(cv, SIG, CX, 1585, F_SEMI, 27, "#FFFFFF", int(200 * a))
        texto(cv, DISC, CX, 1620, F_REG, 23, "#FFFFFF", int(150 * a))
    if t >= t_cta:
        a = prog(t, t_cta, t_cta + 0.35)
        cv.drawRect(skia.Rect(0, 0, W, H), paint(BG_OUT, int(175 * a)))
        if t >= T["manda"] - 0.12:                       # no cartão final, só a frase da CTA
            legenda_var(cv, blocos, t, destaque, y_base=700, tam=92)
        aviao(cv, t, T["manda"] + 0.2)
        rr = skia.RRect.MakeRectXY(skia.Rect(150, 1060, 930, 1214), 28, 28)
        cv.drawRRect(rr, paint("#0B1824", int(230 * a))); cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 3))
        texto(cv, "Dr. Rafael Vargas · Médico ortopedista", CX, 1112, F_BLACK, 36, "#FFFFFF", int(255 * a))
        texto(cv, "CRM-SP 226103 · RQE 137901 · @rafaelvargasmd", CX, 1154, F_SEMI, 28, OURO, int(255 * a))
        texto(cv, DISC, CX, 1190, F_REG, 22, "#FFFFFF", int(170 * a))


# ================================================================== quadro
VEREDITOS = (("pode1", "validado1", T_VALID, VERDE, T_VEZ), ("pode2", "anulado", T_ANUL, AMBAR, None),
             ("pode3", "validado2", T_VALID, VERDE, T_SEGURO))
DUR_CARIMBOS = (1.35, 1.25, 1.15)
TAM_CARIMBOS = ((80, 40, 1.3), (72, 40, 1.2), (80, 40, 1.3))       # (tam, tam_sub, escala da batida)


def pos_carimbo(k, T):
    """Onde o carimbo assenta (tela), nunca em cima de criança. Lances 1 e 3: alto à esquerda (a câmera
    empurrou a criança para a direita). Lance 2: NA FAIXA ciano entre as duas linhas, na altura da cerca —
    o ANULADO cai na comparação (a vantagem medida), não em gente."""
    if k != 1:
        return (300.0, 478.0)
    y_n, y_v = linhas_l2(T)
    ym = (y_n + y_v) / 2
    x, y = na_tela(CAM_CHEC2, cerca_x(ym), ym)
    tam = TAM_CARIMBOS[1][0]
    return (x, y + (tam * 1.02 - tam * 0.38) / 2)              # centro do retângulo no meio da faixa


def chip_estado(t, T):
    """(texto, alfa, pontos, cor, flash): LANCE n -> CHECANDO -> (carimbo) -> veredito -> JEITO CERTO."""
    cortes = (0.0, T["corte2"], T["corte3"], 1e9)
    for k, (pd, vd, s, cor, _) in enumerate(VEREDITOS):
        if not (cortes[k] <= t < cortes[k + 1]):
            continue
        flash = 0.0
        if t < T[pd + "_fim"] + 0.04:
            if k == 0:
                a = prog(t, T["chama"] - 0.04, T["chama"] + 0.14)
            else:
                a = prog(t, cortes[k] + 0.45, cortes[k] + 0.6)
                flash = 1 - prog(t, cortes[k] + 0.5, cortes[k] + 0.75)
            return T_LANCE[k], a, -1, "#FFFFFF", flash
        if t < T[vd] - 0.04:
            t0 = T[pd + "_fim"] + 0.04
            return T_CHEC, 1.0, prog(t, t0, T[vd] - 0.12), "#FFFFFF", 0.0
        dur = DUR_CARIMBOS[k]
        if t < T[vd] + dur - 0.05:
            return None, 0.0, -1, "#FFFFFF", 0.0
        a_in = prog(t, T[vd] + dur - 0.1, T[vd] + dur + 0.1)
        if k == 0:
            if t >= T["so"] - 0.1:
                return None, 0.0, -1, "#FFFFFF", 0.0
            return s, a_in, -1, cor, 0.0
        if k == 1:
            if t >= T["wipe2"] + 0.14:
                return T_CERTO, prog(t, T["wipe2"] + 0.14, T["wipe2"] + 0.32), -1, VERDE, 0.0
            return s, a_in * (1 - prog(t, T["wipe2"], T["wipe2"] + 0.12)), -1, cor, 0.0
        return s, a_in, -1, cor, 0.0
    return None, 0.0, -1, "#FFFFFF", 0.0


def cena(cv, t, T):
    if t < T["corte_so"]:
        return cena_l1(cv, t, T)
    if t < T["corte2"]:
        return dict(lance=1, ressalva=True)
    if t < T["corte3"]:
        kw = prog(t, T["wipe2"], T["wipe2"] + 0.36)
        if kw <= 0:
            return cena_l2(cv, t, T)
        xw = lerp(JX0 - 10, JX1 + 10, e_inout(kw))
        if kw < 1:
            cv.save(); cv.clipRect(skia.Rect(xw, 0, W, H), True)
            cena_l2(cv, t, T)
            cv.restore()
        cv.save(); cv.clipRect(skia.Rect(0, 0, xw, H), True)
        info2 = cena_l2(cv, t, T, certo=True)
        cv.restore()
        if kw < 1:
            cv.drawLine(xw, JY0, xw, JY1, paint(CIANO, 160, "stroke", 26, blur=10))
            cv.drawLine(xw, JY0, xw, JY1, paint("#FFFFFF", 255, "stroke", 6))
        info2["xw"] = xw if kw < 1 else W + 10
        return info2
    return cena_l3(cv, t, T)


def estudio(cv, t, a=1.0):
    """Fundo da tela de análise (ressalva do lance 1): ardósia com grade fina, sem texto."""
    cv.drawRect(JAN, paint("#1B2633", int(255 * a)))
    for x in range(int(JX0), int(JX1), 48):
        cv.drawLine(x, JY0, x, JY1, paint(CIANO, int(14 * a), "stroke", 1))
    for y in range(int(JY0), int(JY1), 48):
        cv.drawLine(JX0, y, JX1, y, paint(CIANO, int(14 * a), "stroke", 1))


def ressalva(cv, t, T):
    """'Só senta assim?': três mini-quadros, os três em W (pulso ciano); 'consulta': a profissional com o apito."""
    estudio(cv, t)
    t0 = T["corte_so"]; tc = T["consulta"]
    sobe = e_inout(prog(t, tc - 0.15, tc + 0.3))
    for i in range(3):
        ki = e_back(prog(t, t0 + 0.05 + 0.16 * i, t0 + 0.4 + 0.16 * i))
        if ki <= 0:
            continue
        cx_ = lerp(206 + 334 * i, 300 + 240 * i, sobe); cy_ = lerp(690, 450, sobe)
        meio = lerp(150, 100, sobe) * clamp(ki, 0, 1.1)
        rect = (cx_ - meio, cy_ - meio * 1.1, cx_ + meio, cy_ + meio * 1.1)
        a_m = lerp(1.0, 0.75, sobe)
        cv.save()
        p = skia.Paint(); p.setAlphaf(clamp(a_m))
        cv.saveLayer(None, p)
        cena_l1_mini(cv, rect)
        cv.restore()
        cv.restore()
        pul = 0.5 + 0.5 * math.sin((t - t0) * 8 - i * 1.3)
        rr = skia.RRect.MakeRectXY(skia.Rect(*rect), 16, 16)
        cv.drawRRect(rr, paint(CIANO, int(90 * pul * a_m), "stroke", 14, blur=8))
        cv.drawRRect(rr, paint(CIANO, int(255 * a_m), "stroke", 5))
    a_pr = prog(t, tc - 0.1, tc + 0.15)
    profissional_com_apito(cv, t, CX - 20, 1010, 1.55, tc - 0.1, tc + 0.3, a_pr, de=(96.0, 300.0))


def hud_lance(cv, t, T, info):
    """Grafismos do VAR sobre a imagem (coordenadas de tela), por lance."""
    lance = info.get("lance")
    cam = info.get("cam")
    if lance == 1 and not info.get("ressalva"):
        s = cam[0]
        jw = juntas_mundo(info["pose"], info["pos"], info["k"])
        sc = lambda n: na_tela(cam, *jw[n])                                     # noqa: E731
        pts = [sc("tE"), sc("aE"), sc("kE"), sc("virilha"), sc("kD"), sc("aD"), sc("tD")]
        tt = t_l1(t, T)
        # o W nas pernas: quadro 0 inteiro; depois corre em "W" e fica até o folheado; volta no W final; apaga
        a_w, k_w = 0.0, 0.0
        if t < T["var"]:
            a_w, k_w = 1.0, 1.0
        elif t < T["var"] + 0.15:
            a_w, k_w = 1 - prog(t, T["var"], T["var"] + 0.15), 1.0
        elif tt >= T["w"] - 0.06:
            k_w = e_inout(prog(tt, T["w"] - 0.06, T["w"] + 0.45))
            a_w = 1.0 if tt < T["vez"] - 0.04 or tt >= T["vez"] + 0.56 else 0.0
            a_w *= 1 - prog(tt, T["deformidade"] + 0.45, T["deformidade"] + 0.75)
        # "não vira deformidade": o traço segue as pernas que se esticam (o W se desfaz) e fica verde
        cor_w = lerpc(CIANO, VERDE, prog(tt, T["deformidade"] - 0.15, T["deformidade"] + 0.15))
        traco_tele(cv, pts, k_w, a_w, cor=cor_w, larg=8 * max(0.8, s / 1.3), caneta=t >= T["var"])
        # círculo nas pernas (quadro 0 e o CHECANDO)
        cxl = (jw["tE"][0] + jw["tD"][0]) / 2; cyl = (jw["kE"][1] + jw["aE"][1]) / 2 - 6
        cx_, cy_ = na_tela(cam, cxl, cyl)
        rx = (jw["tD"][0] - jw["tE"][0]) / 2 * s + 60; ry = 110 * s
        k0 = 1.0 if t < T["var"] else 0.0
        a0 = k0 * (1 - prog(t, T["var"], T["var"] + 0.12))
        k1 = e_out(prog(t, T["pode1"] + 0.12, T["pode1"] + 0.47))
        fora = 1 - prog(t, T["validado1"] + 0.3, T["validado1"] + 0.55)
        pul = 0.5 + 0.5 * math.sin(t * 8) if t < T["var"] or T["pode1_fim"] < t < T["validado1"] else 0.0
        pul += 1.5 * max(0.0, 1 - abs(t - T["chama"] - 0.1) / 0.18)
        circulo_tele(cv, cx_, cy_, rx, ry, 1.0 if t < T["var"] else k1, max(a0, k1 * fora), 0.7, pul)
    elif lance == 2 and not info.get("certa"):
        s = cam[0]
        pose_v, pos_v, k_v = info["viz"]
        # círculo na criança do vizinho em "vizinho"; sai no congelado (no CHECANDO quem pulsa é a FAIXA)
        a_c = prog(t, T["vizinho"] - 0.05, T["vizinho"] + 0.1) * (1 - prog(t, T["pode2_fim"], T["pode2_fim"] + 0.3))
        if a_c > 0:
            jv = juntas_mundo(pose_v, pos_v, k_v)
            cx_, cy_ = na_tela(cam, pos_v[0], (jv["cab"][1] + pos_v[1]) / 2)
            circulo_tele(cv, cx_, cy_, 150 * s * k_v / 0.8, 260 * s * k_v / 0.8,
                         e_out(prog(t, T["vizinho"] - 0.05, T["vizinho"] + 0.35)), a_c, 2.3, 0.0)
    elif lance == 3:
        s = cam[0]
        jw = juntas_mundo(info["pose"], info["pos"], info["k"])
        arco = info.get("arco")
        tt = t_l3(t, T)
        # o palmo entre o bumbum e o tapete, medido pelo telestrador no congelado
        a_g = prog(t, T["pode3"] + 0.12, T["pode3"] + 0.3) * (1 - prog(t, T["validado2"], T["validado2"] + 0.1))
        if a_g > 0:
            bx, by = na_tela(cam, jw["pel"][0], jw["pel"][1] + 44 * info["k"])
            fx_, fy_ = na_tela(cam, info["pos"][0], info["pos"][1])
            for yy in (by, fy_):
                cv.drawLine(bx - 40 * s, yy, bx + 40 * s, yy, paint(CARTAO, int(150 * a_g), "stroke", 12))
                cv.drawLine(bx - 40 * s, yy, bx + 40 * s, yy, paint(CIANO, int(255 * a_g), "stroke", 6))
            pt = paint(CIANO, int(255 * a_g), "stroke", 6)
            pt.setPathEffect(skia.DashPathEffect.Make([12.0, 9.0], 0.0))
            cv.drawLine(bx, by + 8, bx, fy_ - 8, pt)
        a_q = janela(t, T["seguro"] - 0.04, T["pode3"] + 0.2, 0.1, 0.3)
        if a_q > 0:
            qx, qy = na_tela(cam, *CANTO_MESA)
            circulo_tele(cv, qx, qy, 58 * s, 52 * s, e_out(prog(t, T["seguro"] - 0.04, T["seguro"] + 0.3)), a_q, 1.9, 0.0)
        if arco is not None:
            hx, hy = na_tela(cam, info["pos"][0], info["pos"][1])
            R = ((170.0 - CABECA_DY + CABECA_R) * info["k"] + 72) * s     # fixo: a altura dela DE PÉ (+ folga)
            verde_ = arco.get("verde", 0.0)
            a_a = prog(t, T["treinar"] - 0.1, T["treinar"] + 0.2)
            a_a *= 1 - prog(t, T["pode3"] + 0.02, T["pode3"] + 0.25)    # no zoom do CHECANDO ele sairia do monitor
            if arco.get("ff") or t >= T["cada1"]:          # o replay ▶▶ (e o arco verde) começam em "cada"
                a_a = prog(t, T["cada1"] - 0.08, T["cada1"] + 0.08)
            cor = lerpc(CIANO, VERDE, verde_)
            arco_oscilacao(cv, hx, hy, R, arco["amp"], arco["ang"], a_a, cor, leque=1 - verde_)
            if verde_ > 0.5:
                marca_ok(cv, hx + R * 0.62, hy - R * 0.92, 34, VERDE, prog(t, T["equilibrio"] + 0.15, T["equilibrio"] + 0.35))


def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    t_off = T["off"]
    k_v = prog(t, t_off, t_off + 0.22) ** 2; k_h = e_inout(prog(t, t_off + 0.2, t_off + 0.36))
    tela_ligada = t < t_off + 0.38
    jan_rr = skia.RRect.MakeRectXY(JAN, JAN_R, JAN_R)
    # depois de desligar, o monitor fica ESCURO (os pictogramas acendem nele) e sai em "avaliação"
    a_tv = 1 - prog(t, T["avaliacao"] + 0.2, T["avaliacao"] + 0.6)
    if a_tv > 0:
        cv.drawRRect(jan_rr, paint("#0E151D", int(255 * a_tv)))
        if t > t_off + 0.6:
            cv.drawRRect(jan_rr, paint(CIANO, int(40 * a_tv), "stroke", 2))
    info = {}
    if tela_ligada:
        cv.save()
        if t >= t_off:
            sy = max(0.006, 1 - clamp(k_v)); sx = max(0.01, 1 - k_h)
            cv.translate(JCX, JCY); cv.scale(sx, sy); cv.translate(-JCX, -JCY)
        cv.clipRRect(jan_rr, skia.ClipOp.kIntersect, True)
        rebob = janela(t, T["var"], T["var"] + 0.5, 0.03, 0.06)
        if rebob > 0:
            cv.translate(6 * math.sin(t * 97) * rebob, 0)
        info = cena(cv, t, T)
        if info.get("ressalva"):
            ressalva(cv, t, T)
        vinheta(cv)
        if t >= t_off:
            cv.drawRect(JAN, paint("#FFFFFF", int(220 * clamp(k_v * 1.2))))
        cv.restore()
        ruido_vhs(cv, t, rebob)
    if t_off <= t < t_off + 0.62:
        k = prog(t, t_off + 0.16, t_off + 0.62)
        a_lin = clamp((0.3 - (1 - k_v)) / 0.25)
        if t < t_off + 0.36 and a_lin > 0:
            w = (JX1 - JX0) / 2 * max(0.02, 1 - k_h)
            cv.drawLine(JCX - w, JCY, JCX + w, JCY, paint("#FFFFFF", int(240 * a_lin), "stroke", 6, blur=3))
            cv.drawLine(JCX - w, JCY, JCX + w, JCY, paint("#DFF6FF", int(255 * a_lin), "stroke", 3))
        r = lerp(10, 2, k)
        a_pt = prog(t, t_off + 0.18, t_off + 0.26) * (1 - k)
        cv.drawCircle(JCX, JCY, r * 3, paint(CIANO, int(120 * a_pt), blur=10))
        cv.drawCircle(JCX, JCY, r, paint("#FFFFFF", int(255 * a_pt)))

    a_hud = 1 - prog(t, t_off + 0.2, t_off + 0.45)
    if tela_ligada and a_hud > 0:
        cv.save(); cv.clipRRect(jan_rr, skia.ClipOp.kIntersect, True)
        if t < t_off + 0.04:                             # a TV desligando leva junto o grafismo do lance
            hud_lance(cv, t, T, info)
        for t0, forca in ((T["pode1"], 150), (T["pode2"], 150), (T["pode3"], 150), (T["corte_so"], 170),
                          (T["corte2"], 190), (T["corte3"], 190)):
            k = t - t0
            if 0 <= k < 0.16:
                cv.drawRect(JAN, paint("#FFFFFF", int(forca * (1 - k / 0.16))))
        cv.restore()
        varre = 0.0
        for pd, vd, *_ in VEREDITOS:
            if T[pd + "_fim"] < t < T[vd]:
                varre = prog(t, T[pd + "_fim"], T[vd] - 0.05)
        moldura(cv, t, a_hud, varre)
        congelado = t < T["var"] or any(T[pd] + 0.02 <= t < T[vd] for pd, vd, *_ in VEREDITOS)
        icone_pausa(cv, JX1 - 70, JY1 - 74, a_hud * (1.0 if congelado else 0.0))
        a_reb = janela(t, T["var"], T["var"] + 0.5, 0.03, 0.08)
        icone_rebobina(cv, JX1 - 76, JY1 - 74, a_hud * a_reb)
        a_ff = janela(t, T["cada1"] - 0.02, T["equilibrio"], 0.06, 0.12)
        icone_rebobina(cv, JX1 - 76, JY1 - 74, a_hud * a_ff, avanca=True)
        for k_, ((pd, vd, s_, cor, sub), dur, (tam_, tam_s, e0)) in enumerate(zip(VEREDITOS, DUR_CARIMBOS, TAM_CARIMBOS)):
            px, py = pos_carimbo(k_, T)
            carimbo_cor(cv, s_, px, py, -5 if k_ != 1 else -3, T[vd] - 0.02, t, dur, cor, tam=tam_, esc0=e0, sub=sub,
                        tam_sub=tam_s)
        for t0, s in ((T["corte2"], T_LANCE[1]), (T["corte3"], T_LANCE[2])):
            k = t - t0
            if -0.02 <= k < 0.6:
                a = prog(k, 0.0, 0.08) * (1 - prog(k, 0.42, 0.6))
                esc = lerp(1.25, 1.0, e_out(prog(k, 0.0, 0.16)))
                cv.save(); cv.translate(JX0 + 210, JY0 + 112); cv.scale(esc, esc)
                f = skia.Font(F_BLACK, 70); lw = f.measureText(s)
                rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 34, -70, lw / 2 + 34, 26), 16, 16)
                cv.drawRRect(rr, paint(CARTAO, int(225 * a))); cv.drawRRect(rr, paint(CIANO, int(255 * a), "stroke", 4))
                texto(cv, s, 0, 0, F_BLACK, 70, "#FFFFFF", int(255 * a))
                cv.restore()

    t_capa = T["pode1_fim"] + 0.06
    sobe = e_inout(prog(t, t_capa + 0.45, t_capa + 0.85))
    chip, a_chip, pontos, cor_chip, flash = chip_estado(t, T)
    k_s = prog(t, T["chama"] - 0.04, T["chama"] + 0.14)
    esc_s = lerp(0.92, 1.08, sobe) * (1 + 0.25 * (1 - e_back(k_s))) if k_s < 1 else lerp(0.92, 1.08, sobe)
    selo_var(cv, t, lerp(56, 64, sobe), lerp(JY0 + 24, 146, sobe), esc_s, a_hud * clamp(k_s * 1.5), chip, a_chip,
             pontos, cor_chip, flash)

    # ---------- fecho: os 4 pictogramas no monitor escuro; em "avaliação" o apito passa para a profissional
    if t >= t_off + 0.4:
        a_p = 1 - prog(t, T["manda"] - 0.35, T["manda"] - 0.1)
        recua = e_inout(prog(t, T["avaliacao"] - 0.05, T["avaliacao"] + 0.4))
        pictogramas(cv, t, T, a_p, recua)
        a_pr = prog(t, T["avaliacao"] - 0.05, T["avaliacao"] + 0.2) * a_p
        profissional_com_apito(cv, t, CX - 20, 1000, 1.75, T["avaliacao"] - 0.05, T["avaliacao"] + 0.3, a_pr)
    selo_serie(cv, prog(t, T["avaliacao"] + 0.1, T["avaliacao"] + 0.4) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))

    capa(cv, t, t_capa, ep["gancho"][0], ep["gancho"][1])
    interface_var(cv, t, T, blocos, DESTAQUE)


# ================================================================== som (sintetizado aqui, sem licença)
SR = som.SR


def _env(n, a=0.005, r=0.2):
    return som._env(n, a, r)


def _passa_banda(x, f_lo, f_hi):
    lp = som._onepole_lp(x, f_hi)
    return lp - som._onepole_lp(lp, f_lo)


def apito(dur=0.30, seed=11, ganho=0.55, solta=0.04):
    n = int(dur * SR); t = np.arange(n) / SR
    fm = 3150 + 130 * np.sin(2 * np.pi * 41 * t)
    ph = 2 * np.pi * np.cumsum(fm) / SR
    am = 1 - 0.55 * (0.5 + 0.5 * np.sin(2 * np.pi * 41 * t + 0.7))
    tom = (np.sin(ph) + 0.22 * np.sin(2 * ph) + 0.08 * np.sin(3 * ph)) * am
    sopro = _passa_banda(np.random.default_rng(seed).standard_normal(n), 2000, 6000) * 0.5
    env = np.clip(t / 0.012, 0, 1) * np.clip((dur - t) / solta, 0, 1)
    return (tom + sopro * 0.6) * env * ganho


def apito_final():
    return np.concatenate([apito(0.14, 21), np.zeros(int(0.07 * SR)), apito(0.42, 23, solta=0.14)])


def rebobinar(seed=31):
    n = int(0.5 * SR); t = np.arange(n) / SR
    x = np.random.default_rng(seed).standard_normal(n)
    fc = 600 + 2600 * np.abs(np.sin(np.pi * t / 0.5 * 1.5))
    y = np.zeros(n); acc = 0.0
    for i in range(n):
        a = np.exp(-2 * np.pi * fc[i] / SR); acc = (1 - a) * x[i] + a * acc; y[i] = acc
    f = 900 * np.exp(-t * 3.2) + 200
    saw = 2 * ((np.cumsum(f) / SR) % 1.0) - 1
    env = np.clip(t / 0.02, 0, 1) * np.clip((0.5 - t) / 0.05, 0, 1)
    return (y * 0.9 + saw * 0.18 + x * 0.04) * env * 0.8


def bipe(f=1600.0, dur=0.075):
    n = int(dur * SR); t = np.arange(n) / SR
    env = np.clip(t / 0.004, 0, 1) * np.clip((dur - t) / 0.02, 0, 1)
    return np.sin(2 * np.pi * f * t) * env * 0.42


def bipe_alto():
    return bipe(2100.0, 0.11)


def obturador(seed=41):
    a = som.tick(seed) * 0.8
    gap = np.zeros(int(0.05 * SR))
    n = int(0.06 * SR)
    ruido = np.random.default_rng(seed).standard_normal(n) * _env(n, 0.001, 0.015) * 0.35
    b = som.tick(seed + 1) * 0.6
    return np.concatenate([a, gap, b + np.pad(ruido, (0, max(0, len(b) - n)))[:len(b)]])


def tv_desliga(seed=71):
    n = int(0.36 * SR); t = np.arange(n) / SR
    f = 1200 * np.exp(-t * 10) + 60
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.002, 0.22) * 0.55
    rng = np.random.default_rng(seed)
    for _ in range(14):
        p = int(rng.uniform(0, n - 600)); m = int(rng.uniform(80, 400))
        y[p:p + m] += rng.standard_normal(m) * _env(m, 0.0002, 0.003) * 0.35
    return y


def fofo(seed=101):
    """Coisa mole cedendo: 'pfff' grave e abafado + baque mole (cópia do piloto) — a sentada no tapete."""
    n = int(0.42 * SR); t = np.arange(n) / SR
    x = som._onepole_lp(np.random.default_rng(seed).standard_normal(n), 600)
    y = x * np.sin(np.pi * t / 0.42) ** 1.2 * 3.0
    return y + np.pad(som.thump(seed) * 0.35, (0, max(0, n - len(som.thump(seed)))))[:n]


def ziper(seed=51, dur=0.45):
    """Caneta do telestrador riscando a linha (cópia do cf_var_primeiros_socorros)."""
    n = int(dur * SR); t = np.arange(n) / SR
    x = _passa_banda(np.random.default_rng(seed).standard_normal(n), 1500, 7000)
    catraca = (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * (60 + 40 * t / dur) * t))) ** 2
    return x * catraca * np.sin(np.pi * t / dur) ** 0.6 * 0.7


def passo_macio(seed=95):
    """Passinho de pé descalço/meia no chão (abafado)."""
    n = int(0.09 * SR); t = np.arange(n) / SR
    return som._onepole_lp(np.random.default_rng(seed).standard_normal(n), 700) * np.exp(-t * 45) * 1.3


def blocos(seed=161):
    """Clack de bloco de madeira: ruído em banda 1,5–3 kHz, ataque seco, 60 ms."""
    n = int(0.06 * SR); t = np.arange(n) / SR
    x = _passa_banda(np.random.default_rng(seed).standard_normal(n), 1500, 3000)
    tom = np.sin(2 * np.pi * 1900 * t) * 0.5
    return (x * 1.6 + tom) * np.exp(-t / 0.012) * 0.9


def palmas_baixas(seed=171):
    """Duas palminhas suaves (ruído filtrado, ganho baixo), 0,3 s entre elas."""
    def uma(s):
        n = int(0.07 * SR); t = np.arange(n) / SR
        return _passa_banda(np.random.default_rng(s).standard_normal(n), 800, 4500) * np.exp(-t / 0.014) * 1.2
    a = uma(seed); b = uma(seed + 1)
    return np.concatenate([a, np.zeros(int(0.23 * SR)), b])


def pulso_tick(seed=181):
    """Tick suave do metrônomo de cada raia."""
    n = int(0.05 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * 1250 * t) * np.exp(-t / 0.01) * 0.5


def folha(seed=191):
    """Folha de calendário virando: 'frr' curto e seco."""
    n = int(0.12 * SR); t = np.arange(n) / SR
    x = _passa_banda(np.random.default_rng(seed).standard_normal(n), 2500, 8000)
    return x * np.sin(np.pi * t / 0.12) * 0.8


SFX = dict(som.SFX)
SFX.update({"apito": apito, "apito_final": apito_final, "rebobinar": rebobinar, "bipe": bipe, "bipe_alto": bipe_alto,
            "obturador": obturador, "tv_desliga": tv_desliga, "fofo": fofo, "ziper": ziper, "passo": passo_macio,
            "blocos": blocos, "palmas": palmas_baixas, "pulso": pulso_tick, "folha": folha})


def _media_movel(x, w):
    n = len(x)
    c = np.concatenate([[0.0], np.cumsum(x)])
    i = np.arange(n)
    lo = np.clip(i - w // 2, 0, n); hi = np.clip(i + (w - 1) // 2 + 1, 0, n)
    return (c[hi] - c[lo]) / w


def mixar(voz, dur, eventos, ganho_trilha=0.40, baixas=()):
    """Cópia do mixar do cf_var_primeiros_socorros (trilha cai a ~15% nos CHECANDO)."""
    n = int(dur * SR)
    v = np.zeros(n); v[:min(n, len(voz))] = voz[:n]
    musica = som.trilha(dur) * ganho_trilha
    win = int(0.06 * SR)
    envv = np.sqrt(np.maximum(_media_movel(v ** 2, win), 0.0))
    alvo = np.where(envv > 0.02, 0.38, 1.0)
    for t0, t1 in baixas:
        alvo[int(t0 * SR):int(t1 * SR)] = 0.15
    duck = _media_movel(alvo, int(0.25 * SR))
    fx = np.zeros(n)
    cache = {}
    for t0, nome, g in eventos:
        if nome not in cache:
            cache[nome] = SFX[nome]()
        s = cache[nome]
        p = int(t0 * SR)
        if 0 <= p < n:
            m = min(len(s), n - p)
            fx[p:p + m] += s[:m] * g
    mix = v * 1.0 + musica * duck + fx * 0.7
    pico = np.max(np.abs(mix)) or 1.0
    return mix / pico * 0.89


def sons(T):
    ev = [(0.0, "apito", 0.85), (T["chama"] + 0.02, "pop", 0.25), (T["var"] - 0.02, "rebobinar", 0.7)]
    for pd, vd, *_ in VEREDITOS:
        ev.append((T[pd] - 0.01, "obturador", 0.85))
        t0 = T[pd + "_fim"] + 0.07
        ev += [(t0, "bipe", 0.75), (t0 + 0.2, "bipe", 0.75), (t0 + 0.4, "bipe_alto", 0.8)]
        ev.append((T[vd] - 0.02, "thump", 0.9))
    ev += [(T["validado1"] - 0.26, "apito", 0.45), (T["validado2"] - 0.26, "apito", 0.45)]
    # lance 1 — senta em W, folheado, a bola oferecida, levanta e anda
    ts = T["sentar"]
    ev += [(ts + 0.05, "whoosh", 0.2), (ts + 0.8, "blocos", 0.5), (ts + 0.95, "blocos", 0.4), (T["w"] - 0.04, "ziper", 0.45)]
    ev += [(T["vez"] - 0.04 + 0.3 * i, "tick", 0.45) for i in range(3)]
    ev += [(T["vez"] - 0.02, "blocos", 0.35)]
    tn = T["nao1"]
    ev += [(tn + 0.05, "whoosh", 0.2)] + [(tn + 0.75 + 0.37 * i, "passo", 0.45) for i in range(2)]
    ev += [(T["deformidade"] + 0.1, "shimmer", 0.3)]
    # ressalva — os três mini-quadros e a profissional com o apito
    ev += [(T["corte_so"] - 0.02, "tick", 0.5)] + [(T["corte_so"] + 0.1 + 0.16 * i, "pop", 0.26) for i in range(3)]
    ev += [(T["consulta"] + 0.3, "pop", 0.3), (T["consulta"] + 0.35, "shimmer", 0.35)]
    # lance 2 — a linha de impedimento, o X na linha, as raias, a raia que sai, o replay
    ev += [(T["corte2"] - 0.03, "tick", 0.55), (T["corte2"] + 0.02, "whoosh", 0.4), (T["comparar"] - 0.02, "ziper", 0.55)]
    ev += [(T["corte2"] + 0.3 + 0.6 * i, "passo", 0.25) for i in range(4)]
    ev += [(T["vizinho"] + 0.05, "ziper", 0.3), (T["anulado"] + 0.1, "pop", 0.4), (T["anulado"] + 0.2, "tick", 0.55)]
    t = T["ritmo"]
    while t < T["individual"] + 0.3:
        ev.append((t, "pulso", 0.22)); t += 1.05
    t = T["ritmo"] + 0.2
    while t < T["individual"] + 0.1:
        ev.append((t, "pulso", 0.15)); t += 0.58
    ev += [(T["individual"] + 0.05, "whoosh", 0.35)]
    ev += [(T["wipe2"] - 0.02, "whoosh", 0.42), (T["wipe2"] + 0.2, "palmas", 0.45), (T["wipe2"] + 0.45, "passo", 0.35),
           (T["wipe2"] + 0.55, "shimmer", 0.25)]
    # lance 3 — passos bambos, contorno do tapete e da quina, a sentada macia, o replay e o equilíbrio
    ev += [(T["corte3"] - 0.03, "tick", 0.55), (T["corte3"] + 0.02, "whoosh", 0.4)]
    ev += [(T["treinar"] + 0.05 + 0.32 * i, "passo", 0.4) for i in range(3)]
    ev += [(T["espaco"] - 0.02, "ziper", 0.35), (T["seguro"] - 0.02, "ziper", 0.3), (T["pode3"] - 0.45, "whoosh", 0.22)]
    ev += [(T["validado2"] + 0.16, "fofo", 0.5), (T["validado2"] + 0.7, "passo", 0.3)]
    ev += [(T["cada1"] - 0.02, "rebobinar", 0.22)]
    for (a0, sent, a1, *_), g in zip(ciclos_replay(T), (0.32, 0.26)):
        ev += [(sent - 0.12, "whoosh", 0.16), (sent - 0.04, "fofo", g)]
    ev += [(T["equilibrio"] + 0.2, "shimmer", 0.35), (T["equilibrio"] + 0.25, "ping", 0.3)]
    # apito final, TV desligando, os pictogramas, a avaliação, CTA
    ev += [(T["apito_f"], "apito_final", 0.6), (T["off"] + 0.02, "tv_desliga", 0.75)]
    for t0 in (T["nao2"] + 0.05, T["perder"] - 0.05, T["cair2"] - 0.05, T["tropecar"] - 0.05):
        ev.append((t0 + 0.05, "pop", 0.3))
    ev += [(T["nao2"] + 0.3 + 0.35 * i, "folha", 0.35) for i in range(3)]
    ev += [(T["avaliacao"] + 0.3, "pop", 0.32), (T["avaliacao"] + 0.3, "shimmer", 0.4), (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def baixas_trilha(T):
    return [(T[pd + "_fim"] + 0.05, T[vd]) for pd, vd, *_ in VEREDITOS]


def tempos_previa(T):
    return [0.0, T["chama"] + 0.2, T["var"] + 0.25, T["sentar"] + 0.4, T["w"] + 0.3, T["pode1"] + 0.55,
            T["validado1"] + 0.3, T["vez"] + 0.1, T["vez"] + 0.4, T["vez"] + 0.7, T["nao1"] + 0.3,
            T["deformidade"] + 0.3, T["deformidade"] + 0.8, T["corte_so"] + 0.6, T["consulta"] + 0.45,
            T["corte2"] + 0.2, T["comparar"] + 0.5, T["vizinho"] + 0.3, T["pode2"] + 0.5, T["anulado"] + 0.1,
            T["anulado"] + 0.4, T["ritmo"] + 0.3, T["individual"] + 0.35, T["wipe2"] + 0.2, T["wipe2"] + 0.6,
            T["corte3"] + 0.2, T["treinar"] + 0.3, T["espaco"] + 0.3, T["seguro"] + 0.2, T["pode3"] + 0.5,
            T["validado2"] + 0.3, T["validado2"] + 0.6, T["cada1"] + 0.1, T["queda"], T["queda"] + 0.45,
            T["equilibrio"] + 0.4, T["off"] - 0.1, T["off"] + 0.1, T["nao2"] + 0.6, T["perder"] + 0.6,
            T["cair2"] + 0.6, T["tropecar"] + 0.6, T["avaliacao"] + 0.5, T["manda"] + 0.5, T["manda"] + 1.6]


# ================================================================== render (cópia do fazer_render_var dos episódios)
VAO_CHECANDO = 0.80
VAOS_EXTRA = (("comparar", 1, 0.50),     # o anel verde da profissional respira antes do LANCE 2
              ("treinar", 1, 1.15),      # replay do JEITO CERTO do lance 2 (palminhas + passo de lado), sem fala
              ("não", 2, 1.05))          # apito final + TV desligando
PRE_APITO = 0.25


def pausa_checando(audio, pal, vao=VAO_CHECANDO):
    """Insere silêncio depois de cada pergunta ('?' de 'pode?') até o vão chegar a `vao` (cópia do episódio)."""
    ins = []
    for i in range(len(pal) - 1):
        if pal[i]["tok"].lower() == "pode?":
            fim = pal[i]["t"] + pal[i]["d"]; gap = pal[i + 1]["t"] - fim
            if gap < vao:
                ins.append((fim + 0.04, vao - gap))
    if len(ins) != 3:
        raise KeyError(f"esperava 3 perguntas 'pode?' no roteiro, achei {len(ins)}")
    partes, ult = [], 0
    for t0, extra in ins:
        p = int(t0 * SR); partes += [audio[ult:p], np.zeros(int(extra * SR), dtype=audio.dtype)]; ult = p
    partes.append(audio[ult:])
    novo = np.concatenate(partes)

    def remap(t):
        return t + sum(extra for t0, extra in ins if t > t0)
    return novo, [dict(p, t=remap(p["t"])) for p in pal], ins


def garantir_vao(audio, pal, palavra, n, vao):
    c = 0
    for i, p in enumerate(pal):
        if p["w"].lower() == palavra:
            c += 1
            if c == n:
                break
    else:
        raise KeyError(f"palavra não achada para a pausa: {palavra} #{n}")
    fim = pal[i - 1]["t"] + pal[i - 1]["d"]; gap = p["t"] - fim
    if gap >= vao:
        return audio, pal
    t0 = fim + 0.04; extra = vao - gap; k = int(t0 * SR)
    audio = np.concatenate([audio[:k], np.zeros(int(extra * SR), dtype=audio.dtype), audio[k:]])
    return audio, [dict(q, t=q["t"] + (extra if q["t"] > t0 else 0.0)) for q in pal]


def montar_T(pal, mapa):
    T = {}
    for chave, (palavra, n, prefixo) in mapa.items():
        c = 0
        for p in pal:
            w = p["w"].lower()
            if w == palavra or (prefixo and w.startswith(palavra)):
                c += 1
                if c == n:
                    T[chave] = p["t"]
                    if chave in FIM_DE:
                        T[chave + "_fim"] = p["t"] + p["d"]
                    break
        else:
            raise KeyError(f"palavra-âncora não achada no roteiro: {palavra} #{n}")
    T["fim_fala"] = pal[-1]["t"] + pal[-1]["d"]
    T["total"] = T["fim_fala"] + 2.2
    T["corte_so"] = T["so"] - 0.08                      # o lance 1 vira a tela de análise (3 mini-quadros)
    T["corte2"] = T["comparar"] - 0.10
    T["wipe2"] = T["individual_fim"] + 0.06              # cortina: o jeito certo do lance 2, sem fala
    T["corte3"] = T["treinar"] - 0.32
    T["apito_f"] = T["nao2"] - 1.0
    T["off"] = T["nao2"] - 0.48
    return T


def calcular_T(ep, tmp, respiro_cta=0.8):
    roteiro = "\n".join(ep["roteiro"])
    voz_bruta, palavras = _voz.narrar(roteiro, _voz.RITMO_COMO_FUNCIONA, os.path.join(tmp, "voz"))
    voz_c, pal, tirado = comprimir(voz_bruta, palavras, respiro_cta=respiro_cta)
    pal = alinhar(pal, roteiro)
    voz_c, pal, ins = pausa_checando(voz_c, pal)
    for palavra, n, vao in VAOS_EXTRA:
        voz_c, pal = garantir_vao(voz_c, pal, palavra, n, vao)
    voz_c = np.concatenate([np.zeros(int(PRE_APITO * SR), dtype=voz_c.dtype), voz_c])
    pal = [dict(p, t=p["t"] + PRE_APITO) for p in pal]
    T = montar_T(pal, ANCORAS)
    return voz_c, pal, T, tirado, ins


def fazer_render_var(quadro_fn, sons_fn, tempos_fn, respiro_cta=0.8):
    def render(ep, mp4, tmp, previa=False):
        voz_c, pal, T, tirado, ins = calcular_T(ep, tmp, respiro_cta)
        print(f"{ep['id']}: silêncio cortado {tirado:.2f}s | CHECANDO {[round(x[1], 2) for x in ins]} | "
              f"duração final {T['total']:.2f}s")
        blocos_ = montar_blocos_var(pal)

        def quadro_t(cv, t):
            quadro_fn(cv, t, T, blocos_, ep)

        if previa:
            return _previas(quadro_t, tempos_fn(T), tmp, ep["id"]), T["total"]
        wav = os.path.join(tmp, f"{ep['id']}_mix.wav")
        som.gravar_wav(wav, mixar(voz_c, T["total"], sons_fn(T), baixas=baixas_trilha(T)))
        codificar(quadro_t, T["total"], wav, mp4)
        return mp4, T["total"]
    return render


render = fazer_render_var(quadro, sons, tempos_previa, respiro_cta=0.8)
