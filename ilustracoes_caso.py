# -*- coding: utf-8 -*-
"""
Ilustrações esquemáticas da série "Anatomia de um Caso" (30/08/2026).

Quadros paramétricos (Pillow) desenhados DENTRO da banda média vertical do reel:
y ∈ [870, 1310] — nunca acima de 860 (miolo de texto), nunca abaixo de CLAMP_Y=1330
(o footer CFM começa em fy=1380 e é intocável). Linguagem visual DA CASA (a mesma do
motivo _bone de render_reel): traços GOLD/CREAM sobre INK, espessuras 8–12, alpha em
camadas, animação progressiva por eoutc, rótulos em F(NR, 22–30) e cotas com setas finas.

Contrato com o motor: render_reel chama `desenhar(img, spec, tl, dur)` quando a CENA tem
o campo "ilustracao" = {"tipo": <nome em _TIPOS>, ...params}. Nessa cena o motivo
(_bone/_feet) é suprimido — a ilustração ocupa a banda média. Cores/fontes/easing são
lidos de render_reel EM TEMPO DE CHAMADA (import tardio: respeita _apply_palette do
episódio e o monkeypatch de fontes do harness local).

Params comuns a todo tipo:
  "dy": int          — desce a arte (nunca sobe além da banda; clamp)
  "esmaecido": bool  — arte de fundo (alpha ×0.35) p/ cena de CTA
  "citacao": [l1,l2] — cartão de citação + ícones enviar/salvar por cima (cena final)

REGRAS DO FORMATO (rotulagem obrigatória): toda cena com ilustração carrega o rótulo
persistente "ILUSTRAÇÃO ESQUEMÁTICA · CASO DA LITERATURA" (F(NR,20), MUT_L, dentro da
banda). NUNCA: radiografia realista, corpo/rosto identificável, vermelho fora de alerta,
marca comercial de fixador. Fixador circular = representação FIEL da casa: anéis
COMPLETOS (elipses) + hastes verticais.
"""
import math
from PIL import Image, ImageDraw

# ── geometria da banda (contrato com render_reel: CLAMP_Y=1330, footer fy=1380) ──
BAND_TOP, BAND_BOT = 870, 1310
ART_TOP, ART_BOT = 884, 1266     # miolo útil da arte
LABEL_Y = 1282                   # rótulo persistente (20px -> base ~1306, dentro da banda)
ROTULO_FORMATO = "ILUSTRAÇÃO ESQUEMÁTICA · CASO DA LITERATURA"


def _rr():
    import render_reel
    return render_reel


def _pp(p, ini, dur):
    """progresso local easeado (eoutc) de um elemento que entra em [ini, ini+dur] do p global."""
    return _rr().eoutc((p - ini) / max(dur, 1e-6))


def _c(cor, a):
    return cor + (max(0, min(255, int(a))),)


# ───────────────────────── primitivas de desenho ─────────────────────────

def _seta(d, p0, p1, cor, w=3, head=12):
    """linha fina com ponta de seta em p1 (cotas e chamadas)."""
    x0, y0 = p0
    x1, y1 = p1
    d.line([p0, p1], fill=cor, width=w)
    ang = math.atan2(y1 - y0, x1 - x0)
    for da in (math.radians(153), math.radians(-153)):
        d.line([(x1, y1), (x1 + head * math.cos(ang + da), y1 + head * math.sin(ang + da))],
               fill=cor, width=w)


def _cota_v(d, x, y0, y1, cor, w=3, tick=12):
    """cota vertical: setas p/ fora nas duas pontas + ticks horizontais."""
    ym = (y0 + y1) // 2
    _seta(d, (x, ym), (x, y0), cor, w=w, head=10)
    _seta(d, (x, ym), (x, y1), cor, w=w, head=10)
    d.line([(x - tick, y0), (x + tick, y0)], fill=cor, width=w)
    d.line([(x - tick, y1), (x + tick, y1)], fill=cor, width=w)


def _cota_h(d, x0, x1, y, cor, w=3, tick=12):
    xm = (x0 + x1) // 2
    _seta(d, (xm, y), (x0, y), cor, w=w, head=10)
    _seta(d, (xm, y), (x1, y), cor, w=w, head=10)
    d.line([(x0, y - tick), (x0, y + tick)], fill=cor, width=w)
    d.line([(x1, y - tick), (x1, y + tick)], fill=cor, width=w)


def _tracejada(d, p0, p1, cor, w=3, dash=12, gap=9):
    x0, y0 = p0
    x1, y1 = p1
    L = math.hypot(x1 - x0, y1 - y0)
    if L <= 0:
        return
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    t = 0.0
    while t < L:
        t2 = min(t + dash, L)
        d.line([(x0 + ux * t, y0 + uy * t), (x0 + ux * t2, y0 + uy * t2)], fill=cor, width=w)
        t += dash + gap


def _txt(d, xy, texto, tam, cor, a, negrito=False, centro=False, direita=False):
    """rótulo da casa: F(NR/NB, tam). Devolve a largura medida."""
    R = _rr()
    f = R.F(R.NB if negrito else R.NR, tam)
    wt = d.textlength(texto, font=f)
    x, y = xy
    if centro:
        x -= wt / 2
    elif direita:
        x -= wt
    d.text((x, y), texto, font=f, fill=_c(cor, a))
    return wt


def _osso_v(d, cx, y0, y1, cor, w=30):
    """barra vertical de osso com pontas arredondadas (convenção do motivo _bone)."""
    if y1 - y0 < 4:
        return
    d.line([(cx, y0), (cx, y1)], fill=cor, width=w)
    r = w // 2 + 4
    d.ellipse([cx - r, y0 - int(r * 0.7), cx + r, y0 + int(r * 0.7)], fill=cor)
    d.ellipse([cx - r, y1 - int(r * 0.7), cx + r, y1 + int(r * 0.7)], fill=cor)


def _hachura_v(d, cx, y0, y1, cor, meia_larg=13, passo=16):
    """trabéculas do osso novo (tracinhos diagonais), como no motivo _bone."""
    for yy in range(int(y0), int(y1) - 6, passo):
        d.line([(cx - meia_larg, yy), (cx + meia_larg, yy + 9)], fill=cor, width=2)


def _aneis_fixador(d, cx, ys, rx, ry, cor_anel, cor_haste, hx=None, y_haste=None):
    """fixador circular FIEL (convenção da casa): anéis COMPLETOS (elipses) + hastes verticais."""
    if y_haste is None:
        y_haste = (min(ys), max(ys))
    if hx is None:
        hx = (-rx + 8, rx - 8)
    for off in hx:
        d.line([(cx + off, y_haste[0]), (cx + off, y_haste[1])], fill=cor_haste, width=8)
    for y in ys:
        d.ellipse([cx - rx, y - ry, cx + rx, y + ry], outline=cor_anel, width=8)


def _pessoa_perfil(d, cx, chao, h, cor, w=10, passo=True, perna_dest=None):
    """pictograma humano de perfil, caminhando; sem rosto. perna_dest recebe (x_joelho,
    y_joelho, x_pe, y_pe) da perna da frente p/ acessórios (órtese)."""
    r = int(h * 0.11)
    y_cab = chao - h + r
    d.ellipse([cx - r, y_cab - r, cx + r, y_cab + r], outline=cor, width=w)
    y_ombro = y_cab + r + int(h * 0.06)
    y_quadril = chao - int(h * 0.42)
    d.line([(cx, y_cab + r), (cx, y_quadril)], fill=cor, width=w)
    # braços (balanço leve)
    y_mao = y_ombro + int(h * 0.24)
    bd = int(h * 0.13) if passo else int(h * 0.05)
    d.line([(cx, y_ombro), (cx + bd, y_mao)], fill=cor, width=w)
    d.line([(cx, y_ombro), (cx - bd, y_mao)], fill=cor, width=w)
    # pernas: frente (com joelho) e trás
    pf = int(h * 0.16) if passo else int(h * 0.04)
    xj, yj = cx + pf // 2, chao - int(h * 0.22)
    xpe, ype = cx + pf, chao
    d.line([(cx, y_quadril), (xj, yj)], fill=cor, width=w)
    d.line([(xj, yj), (xpe, ype)], fill=cor, width=w)
    d.line([(xpe, ype), (xpe + int(h * 0.07), ype)], fill=cor, width=w)  # pé
    d.line([(cx, y_quadril), (cx - pf, chao)], fill=cor, width=w)
    if perna_dest is not None:
        perna_dest.extend([xj, yj, xpe, ype])


def _pessoa_frente(d, cx, chao, h, cor, w=9, curta_lado=0, curta_dy=0, arco_lado=0,
                   pelve_tilt=0, spine_curva=False):
    """pictograma humano de FRENTE, neutro, sem rosto. curta_lado=+1/-1 encurta a perna
    daquele lado (dy px acima do chão); arco_lado curva a perna (arqueada); pelve_tilt
    inclina a linha do quadril; spine_curva desenha a coluna com curva lateral discreta."""
    r = int(h * 0.10)
    y_cab = chao - h + r
    d.ellipse([cx - r, y_cab - r, cx + r, y_cab + r], outline=cor, width=w)
    y_ombro = y_cab + r + int(h * 0.05)
    y_quadril = chao - int(h * 0.44)
    if spine_curva:
        # coluna com leve curva lateral (escoliose esquemática)
        pontos = []
        for i in range(9):
            t = i / 8
            pontos.append((cx + int(math.sin(t * math.pi) * h * 0.045),
                           y_cab + r + t * (y_quadril - y_cab - r)))
        d.line(pontos, fill=cor, width=w)
    else:
        d.line([(cx, y_cab + r), (cx, y_quadril)], fill=cor, width=w)
    # ombros/braços (curtos e altos: nunca encostam na linha do quadril — senão o braço
    # emenda visualmente com a perna e vira "joelho dobrado")
    ab = int(h * 0.11)
    d.line([(cx, y_ombro), (cx - ab, y_ombro + int(h * 0.14))], fill=cor, width=w)
    d.line([(cx, y_ombro), (cx + ab, y_ombro + int(h * 0.14))], fill=cor, width=w)
    # linha da pelve (tilt opcional) — CURTA, senão vira "banquinho" sob o tronco
    pw = int(h * 0.13)
    pv = int(pw * 0.6)
    d.line([(cx - pv, y_quadril + pelve_tilt), (cx + pv, y_quadril - pelve_tilt)], fill=cor, width=w)
    # pernas em Λ raso (perto do tronco no quadril, pouco abertas no pé); a arqueada vira
    # ARCO suave (polilinha senoidal, joint='curve'); a curta termina ACIMA do chão
    for lado in (-1, 1):
        x0 = cx + lado * int(pw * 0.30)
        x_pe = cx + lado * int(pw * 0.80)
        y_fim = chao - (curta_dy if lado == curta_lado and curta_lado != 0 else 0)
        y_ini = y_quadril + (pelve_tilt if lado == -1 else -pelve_tilt)
        if lado == arco_lado and arco_lado != 0:
            bulge = int(h * 0.055)
            pts = [(x0 + (x_pe - x0) * (i / 8) + lado * bulge * math.sin(math.pi * i / 8),
                    y_ini + (y_fim - y_ini) * (i / 8)) for i in range(9)]
            d.line(pts, fill=cor, width=w, joint="curve")
        else:
            d.line([(x0, y_ini), (x_pe, y_fim)], fill=cor, width=w)
        d.line([(x_pe, y_fim), (x_pe + lado * int(h * 0.06), y_fim)], fill=cor, width=w)


def _perna_contorno(d, cx, y0, y1, meia_larg, cor, w=6):
    """contorno esquemático de perna (joelho→pé), sem corpo: duas laterais + pé p/ a direita."""
    d.line([(cx - meia_larg, y0), (cx - int(meia_larg * 0.8), y1)], fill=cor, width=w)
    d.line([(cx + meia_larg, y0), (cx + int(meia_larg * 0.8), y1)], fill=cor, width=w)
    d.arc([cx - meia_larg, y0 - 18, cx + meia_larg, y0 + 18], 180, 360, fill=cor, width=w)
    d.line([(cx - int(meia_larg * 0.8), y1), (cx + int(meia_larg * 1.15), y1)], fill=cor, width=w)


def _regua_barras(d, x, chao, h1, h2, cor1, cor2, larg=26, gap=44):
    """duas barras verticais de comparação (a linguagem de 'régua' da casa). Devolve topos."""
    _osso_v(d, x, chao - h1, chao, cor1, w=larg)
    _osso_v(d, x + gap, chao - h2, chao, cor2, w=larg)
    return chao - h1, chao - h2


def _cartao_citacao(d, R, linhas, p, icones=True):
    """cartão de citação central (cena de CTA) + ícones enviar/salvar."""
    a = 255 * _pp(p, 0.15, 0.5)
    cx = R.W // 2
    y0, y1 = 950, 1130
    d.rounded_rectangle([cx - 380, y0, cx + 380, y1], radius=18,
                        outline=_c(R.GOLD, 0.85 * a), width=3)
    ty = y0 + 34
    for i, ln in enumerate(linhas):
        _txt(d, (cx, ty), ln, 30 if i == 0 else 25, R.CREAM if i == 0 else R.TXT_L,
             a, centro=True)
        ty += 48
    if icones:
        ai = 220 * _pp(p, 0.45, 0.5)
        # enviar (aviãozinho)
        ex, ey = cx - 60, 1188
        d.polygon([(ex - 22, ey + 10), (ex + 22, ey - 8), (ex - 8, ey + 22), (ex - 10, ey + 8)],
                  outline=_c(R.GOLD, ai), width=3)
        # salvar (bandeirinha)
        sx = cx + 60
        d.line([(sx - 14, 1172), (sx - 14, 1212), (sx, 1200), (sx + 14, 1212), (sx + 14, 1172),
                (sx - 14, 1172)], fill=_c(R.GOLD, ai), width=3, joint="curve")


# ───────────────────────── quadros por tipo ─────────────────────────
# PILOTO 1 — transporte ósseo na tíbia (Pentela 2023, PMC10226645)

def _q_osso_falha(d, spec, p, R):
    """Quadro A do piloto 1. orientacao 'h' (zoom do vão, cena 0) ou 'v' (perna inteira, cena 1)."""
    cota = spec.get("cota", "17,2 cm")
    if spec.get("orientacao", "v") == "h":
        # ZOOM: só o vão + a cota (eco horizontal do motivo _bone, em grande)
        y = 1030
        a1 = 235 * _pp(p, 0.00, 0.45)
        x0, x1, g0, g1 = 170, 910, 420, 660
        for xa, xb in ((x0, g0), (g1, x1)):
            d.line([(xa, y), (xb, y)], fill=_c(R.GOLD, a1), width=26)
        for ex, lado in ((x0, 1), (x1, -1)):
            d.ellipse([ex - 20, y - 24, ex + 20, y + 24], fill=_c(R.GOLD, a1))
        for gx in (g0, g1):
            d.ellipse([gx - 13, y - 17, gx + 13, y + 17], fill=_c(R.GOLD, a1))
        a2 = 200 * _pp(p, 0.30, 0.40)
        _tracejada(d, (g0 + 18, y - 34), (g1 - 18, y - 34), _c(R.CREAM, 0.5 * a2), w=3)
        _tracejada(d, (g0 + 18, y + 34), (g1 - 18, y + 34), _c(R.CREAM, 0.5 * a2), w=3)
        a3 = 255 * _pp(p, 0.45, 0.45)
        _cota_h(d, g0 + 6, g1 - 6, y + 96, _c(R.CREAM, 0.85 * a3), w=3)
        _txt(d, ((g0 + g1) // 2, y + 122), cota, 30, R.GOLD, a3, negrito=True, centro=True)
        _txt(d, ((g0 + g1) // 2, y - 92), "o vão no osso", 26, R.MUT_L, a3, centro=True)
        return

    # PERNA INTEIRA (vertical): silhueta + tíbia interrompida + fíbula fina + cota + nota da pele
    cx = 400
    a_sil = 110 * _pp(p, 0.00, 0.40)
    _perna_contorno(d, cx, 902, 1218, 96, _c(R.CREAM, a_sil), w=6)
    a1 = 225 * _pp(p, 0.10, 0.45)
    g0, g1 = 1016, 1128                     # o vão (terço médio)
    _osso_v(d, cx - 14, 924, g0, _c(R.GOLD, a1), w=30)      # tíbia proximal
    _osso_v(d, cx - 14, g1, 1200, _c(R.GOLD, a1), w=30)     # tíbia distal
    d.line([(cx + 44, 924), (cx + 44, 1200)], fill=_c(R.CREAM, 0.32 * a1), width=8)  # fíbula (apagada)
    a2 = 200 * _pp(p, 0.35, 0.40)
    _tracejada(d, (cx - 52, g0 + 8), (cx - 52, g1 - 8), _c(R.CREAM, 0.55 * a2), w=3)
    _tracejada(d, (cx + 22, g0 + 8), (cx + 22, g1 - 8), _c(R.CREAM, 0.55 * a2), w=3)
    a3 = 255 * _pp(p, 0.45, 0.40)
    _cota_v(d, cx - 130, g0, g1, _c(R.CREAM, 0.85 * a3), w=3)
    _txt(d, (cx - 165, (g0 + g1) // 2 - 18), cota, 30, R.GOLD, a3, negrito=True, direita=True)
    a4 = 235 * _pp(p, 0.60, 0.40)
    d.line([(cx + 30, (g0 + g1) // 2 + 6), (cx + 168, 1156)], fill=_c(R.MUT_L, 0.6 * a4), width=2)
    _txt(d, (cx + 180, 1146), spec.get("nota", "a pele também sofreu"), 25, R.MUT_L, a4)
    _txt(d, (cx + 180, 1000), "tíbia interrompida", 26, R.TXT_L, a3)
    _txt(d, (cx + 180, 1036), "no terço médio", 26, R.TXT_L, a3)


def _q_fixador_transporte(d, spec, p, R):
    """Quadro B do piloto 1: fixador de Ilizarov FIEL (4 anéis completos + hastes) e o
    segmento de transporte viajando com o progresso da cena; osso novo atrás."""
    cx = 380
    a_sil = 100 * _pp(p, 0.0, 0.35)
    d.line([(cx - 78, 900), (cx - 66, 1216)], fill=_c(R.CREAM, a_sil), width=6)
    d.line([(cx + 78, 900), (cx + 66, 1216)], fill=_c(R.CREAM, a_sil), width=6)
    # osso: segmento proximal fixo, vão distal
    a1 = 225 * _pp(p, 0.08, 0.35)
    corte_y = 986
    _osso_v(d, cx, 916, corte_y - 8, _c(R.GOLD, a1), w=28)          # proximal (acima do corte)
    _osso_v(d, cx, 1152, 1204, _c(R.GOLD, a1), w=28)                # distal (alvo do docking)
    # fixador circular FIEL: anéis completos + hastes verticais
    a_fx = 205 * _pp(p, 0.16, 0.40)
    _aneis_fixador(d, cx, [928, 1000, 1120, 1192], 128, 22,
                   _c(R.GOLD, a_fx), _c(R.CREAM, 0.55 * a_fx), hx=(-116, 6, 116),
                   y_haste=(928, 1192))
    # segmento de transporte: viaja do corte ao docking com o progresso da cena
    trav = _pp(p, 0.25, 0.62)
    seg_h = 52
    y_ini, y_fim = corte_y + 6, 1146 - seg_h
    seg_y = y_ini + (y_fim - y_ini) * trav
    a_seg = 245 * _pp(p, 0.18, 0.30)
    d.rounded_rectangle([cx - 17, seg_y, cx + 17, seg_y + seg_h], radius=12, fill=_c(R.CREAM, a_seg))
    # trilha pontilhada + seta descendente à frente do segmento
    if seg_y + seg_h < 1146 - 8:
        _tracejada(d, (cx, seg_y + seg_h + 10), (cx, 1146), _c(R.CREAM, 0.45 * a_seg), w=3)
        _seta(d, (cx, 1120), (cx, 1142), _c(R.CREAM, 0.45 * a_seg), w=3, head=9)
    # osso novo atrás (acima) do segmento, com trabéculas
    if seg_y > y_ini + 8:
        a_nv = 150 * _pp(p, 0.30, 0.40)
        d.line([(cx, y_ini), (cx, seg_y - 4)], fill=_c(R.GOLD, 0.75 * a_nv), width=22)
        _hachura_v(d, cx, y_ini + 4, seg_y - 6, _c(R.GOLD, 0.9 * a_nv))
    # rótulos (coluna da direita, fora dos anéis)
    xr = 570
    a2 = 245 * _pp(p, 0.30, 0.40)
    d.line([(cx + 24, corte_y), (xr - 14, 936)], fill=_c(R.MUT_L, 0.6 * a2), width=2)
    _txt(d, (xr, 924), spec.get("rotulo_corte", "corte no osso saudável"), 26, R.TXT_L, a2)
    a3 = 235 * _pp(p, 0.45, 0.40)
    d.line([(cx + 14, 1046), (xr - 14, 1052)], fill=_c(R.MUT_L, 0.6 * a3), width=2)
    _txt(d, (xr, 1040), spec.get("rotulo_novo", "osso novo"), 26, R.GOLD, a3)
    _txt(d, (xr, 1076), "atrás do segmento", 22, R.MUT_L, 0.85 * a3)
    a4 = 235 * _pp(p, 0.58, 0.40)
    _txt(d, (xr, 1170), spec.get("rotulo_tempo", "4 meses, aos poucos"), 26, R.TXT_L, a4)
    d.line([(xr, 1206), (xr + 236, 1206)], fill=_c(R.GOLD, 0.5 * a4), width=3)


def _q_osso_continuo(d, spec, p, R):
    """Quadro C do piloto 1: tíbia contínua com o trecho regenerado marcado (honestidade
    visual) + pictograma caminhando + selos de desfecho."""
    cx = 230
    a1 = 225 * _pp(p, 0.0, 0.40)
    _osso_v(d, cx, 916, 1204, _c(R.GOLD, a1), w=28)
    # trecho regenerado: tom mais claro + trabéculas + ticks de limite
    g0, g1 = 1010, 1122
    a2 = 210 * _pp(p, 0.18, 0.40)
    d.line([(cx, g0), (cx, g1)], fill=_c(R.CREAM, 0.55 * a2), width=28)
    _hachura_v(d, cx, g0 + 4, g1 - 4, _c(R.GOLD, 0.75 * a2))
    for yy in (g0, g1):
        d.line([(cx - 26, yy), (cx + 26, yy)], fill=_c(R.CREAM, 0.8 * a2), width=3)
    _txt(d, (cx, 1226), "osso contínuo", 24, R.MUT_L, 235 * _pp(p, 0.30, 0.4), centro=True)
    d.line([(cx + 22, (g0 + g1) // 2), (cx + 92, 1066)], fill=_c(R.MUT_L, 0.55 * a2), width=2)
    _txt(d, (cx + 102, 1054), "osso novo", 24, R.GOLD, a2)
    # figura caminhando (sem muleta) — pictograma neutro
    a3 = 235 * _pp(p, 0.25, 0.45)
    _pessoa_perfil(d, 500, 1204, 300, _c(R.CREAM, a3), w=10, passo=True)
    # selos de desfecho (chips na coluna direita)
    selos = spec.get("selos", [])
    ys = 936
    for i, s in enumerate(selos):
        a4 = 240 * _pp(p, 0.40 + 0.14 * i, 0.40)
        f = _rr().F(R.NR, 24)
        wt = d.textlength(s, font=f)
        x1 = 940                                     # chips alinhados à margem direita
        d.rounded_rectangle([x1 - wt - 44, ys - 12, x1, ys + 34], radius=16,
                            outline=_c(R.GOLD, 0.7 * a4), width=3)
        d.text((x1 - wt - 22, ys - 2), s, font=f, fill=_c(R.TXT_L, a4))
        ys += 78
    # ícone do tornozelo: arco de movimento LIMITADO (curto), junto do último selo
    if spec.get("arco_tornozelo"):
        a5 = 235 * _pp(p, 0.70, 0.35)
        ax, ay = 668, ys + 34
        d.line([(ax - 28, ay), (ax + 38, ay)], fill=_c(R.CREAM, a5), width=7)  # pé
        d.line([(ax, ay), (ax, ay - 44)], fill=_c(R.CREAM, a5), width=7)       # perna
        d.arc([ax - 40, ay - 40, ax + 40, ay + 40], 245, 292, fill=_c(R.GOLD, a5), width=5)
        _txt(d, (ax + 60, ay - 24), "arco de movimento limitado", 22, R.MUT_L, a5)


# PILOTO 2 — osteomielite, correção 17 anos depois (Hong 2023, PMC9958936)

def _q_linha_tempo(d, spec, p, R):
    """Quadro A do piloto 2: criança (perna arqueada) → 17 anos → adulto (arqueada e mais
    curta) + barras de cota. zoom=True (cena 1) aproxima só a metade adulta."""
    cota = spec.get("cota", "14 cm a menos")
    if spec.get("zoom"):
        a1 = 235 * _pp(p, 0.0, 0.45)
        d.line([(180, 1210), (700, 1210)], fill=_c(R.CREAM, 0.22 * a1), width=3)  # chão
        _pessoa_frente(d, 330, 1210, 320, _c(R.CREAM, a1), w=10,
                       curta_lado=1, curta_dy=46, arco_lado=1, pelve_tilt=10)
        t1, t2 = _regua_barras(d, 560, 1210, 250, 204, _c(R.GOLD, 0.85 * a1),
                               _c(R.GOLD, 0.55 * a1))
        a2 = 255 * _pp(p, 0.40, 0.45)
        _cota_v(d, 680, t1, t2, _c(R.CREAM, 0.85 * a2), w=3)
        _txt(d, (712, (t1 + t2) // 2 - 16), cota, 30, R.GOLD, a2, negrito=True)
        _txt(d, (712, 1080), "perna arqueada", 26, R.TXT_L, a2)
        _txt(d, (712, 1116), "e mais curta", 26, R.TXT_L, a2)
        return
    # linha do tempo completa (cena 0)
    a1 = 225 * _pp(p, 0.0, 0.40)
    d.line([(160, 1190), (330, 1190)], fill=_c(R.CREAM, 0.22 * a1), width=3)  # chão (criança)
    _pessoa_frente(d, 230, 1190, 210, _c(R.CREAM, a1), w=8, arco_lado=1)
    star_x, star_y = 262, 1128
    a_st = 235 * _pp(p, 0.15, 0.35)
    for ang in range(0, 360, 45):
        rr_ = 13 if ang % 90 == 0 else 6
        d.line([(star_x, star_y),
                (star_x + rr_ * math.cos(math.radians(ang)), star_y + rr_ * math.sin(math.radians(ang)))],
               fill=_c(R.GOLD, a_st), width=3)
    _txt(d, (150, 1224), spec.get("nota", "infecção no osso (osteomielite)"), 22, R.MUT_L, a_st)
    a2 = 235 * _pp(p, 0.28, 0.40)
    _seta(d, (330, 1044), (560, 1044), _c(R.GOLD, a2), w=4, head=14)
    _txt(d, (445, 996), spec.get("anos", "17 anos"), 28, R.GOLD, a2, negrito=True, centro=True)
    a3 = 235 * _pp(p, 0.42, 0.40)
    d.line([(600, 1210), (900, 1210)], fill=_c(R.CREAM, 0.22 * a3), width=3)  # chão (adulto)
    _pessoa_frente(d, 680, 1210, 300, _c(R.CREAM, a3), w=9,
                   curta_lado=1, curta_dy=42, arco_lado=1, pelve_tilt=9)
    t1, t2 = _regua_barras(d, 810, 1210, 236, 194, _c(R.GOLD, 0.85 * a3), _c(R.GOLD, 0.55 * a3))
    a4 = 255 * _pp(p, 0.58, 0.40)
    _cota_v(d, 900, t1, t2, _c(R.CREAM, 0.85 * a4), w=3)
    _txt(d, (832, min(t1, t2) - 66), cota, 25, R.GOLD, a4, negrito=True, centro=True)


def _q_painel_triplo(d, spec, p, R):
    """Quadro B do piloto 2: 3 painéis 1·2·3 — anéis que endireitam · placa externa · livre."""
    paineis = spec.get("paineis", [
        ("anéis", "1 mm por dia · 4 meses"),
        ("placa externa", "de perfil baixo"),
        ("livre", "15 meses depois, a placa sai"),
    ])
    xs = (146, 416, 686)
    larg = 236
    for i, (x0, (titulo, rotulo)) in enumerate(zip(xs, paineis)):
        a = 240 * _pp(p, 0.06 + 0.22 * i, 0.34)
        if a <= 0:
            continue
        cx = x0 + larg // 2
        # número do painel
        d.ellipse([x0, 896, x0 + 40, 936], outline=_c(R.GOLD, a), width=3)
        _txt(d, (x0 + 20, 902), str(i + 1), 24, R.GOLD, a, negrito=True, centro=True)
        # perna esquemática (contorno)
        _perna_contorno(d, cx, 950, 1140, 44, _c(R.CREAM, 0.55 * a), w=5)
        if i == 0:
            # anéis completos + hastes; eixo pontilhado de CURVO p/ RETO + seta de correção
            _aneis_fixador(d, cx, [968, 1016, 1084, 1130], 66, 13,
                           _c(R.GOLD, 0.9 * a), _c(R.CREAM, 0.5 * a), hx=(-58, 58),
                           y_haste=(968, 1130))
            _tracejada(d, (cx - 16, 958), (cx + 10, 1046), _c(R.CREAM, 0.65 * a), w=3, dash=8, gap=7)
            _tracejada(d, (cx + 10, 1046), (cx, 1136), _c(R.CREAM, 0.65 * a), w=3, dash=8, gap=7)
            d.arc([cx - 34, 1028, cx + 34, 1072], 300, 80, fill=_c(R.GOLD, a), width=3)
            _seta(d, (cx + 30, 1062), (cx + 22, 1072), _c(R.GOLD, a), w=3, head=8)
        elif i == 1:
            # placa externa: barra fina RETA por FORA do contorno, com parafusos (pontos)
            px = cx + 62
            d.line([(px, 972), (px, 1128)], fill=_c(R.GOLD, a), width=7)
            for yy in (988, 1024, 1076, 1112):
                d.ellipse([px - 7, yy - 7, px + 7, yy + 7], fill=_c(R.CREAM, 0.9 * a))
                d.line([(px - 7, yy), (cx + 34, yy)], fill=_c(R.CREAM, 0.4 * a), width=3)
            _tracejada(d, (cx, 958), (cx, 1136), _c(R.CREAM, 0.5 * a), w=3, dash=8, gap=7)
        else:
            # livre: eixo reto, sem aparelho
            _tracejada(d, (cx, 958), (cx, 1136), _c(R.GOLD, 0.8 * a), w=3, dash=8, gap=7)
        _txt(d, (cx, 1162), titulo, 25, R.TXT_L, a, centro=True)
        _txt(d, (cx, 1196), rotulo, 22, R.MUT_L, a, centro=True)


def _q_regua_resultado(d, spec, p, R):
    """Quadro C do piloto 2: duas pernas retas quase iguais, régua com marcador da diferença
    mínima + figura caminhando com os marcadores honestos (tornozelo/joelho)."""
    a1 = 230 * _pp(p, 0.0, 0.40)
    t1, t2 = _regua_barras(d, 250, 1204, 266, 260, _c(R.GOLD, 0.9 * a1),
                           _c(R.GOLD, 0.62 * a1), larg=30, gap=64)
    # régua fina horizontal cruzando os topos + marcador da diferença
    a2 = 245 * _pp(p, 0.28, 0.40)
    d.line([(180, t1), (420, t1)], fill=_c(R.CREAM, 0.6 * a2), width=2)
    for xx in range(190, 415, 22):
        d.line([(xx, t1), (xx, t1 - 8)], fill=_c(R.CREAM, 0.6 * a2), width=2)
    d.line([(180, t2), (420, t2)], fill=_c(R.CREAM, 0.35 * a2), width=2)
    _seta(d, (348, t2 - 56), (330, t2 - 6), _c(R.GOLD, a2), w=3, head=9)
    _txt(d, (358, t2 - 88), spec.get("cota", "0,1 cm"), 30, R.GOLD, a2, negrito=True)
    _txt(d, (168, 1230), "praticamente iguais", 24, R.MUT_L, a2)
    # figura caminhando + marcadores honestos
    a3 = 235 * _pp(p, 0.35, 0.45)
    _pessoa_perfil(d, 640, 1204, 300, _c(R.CREAM, a3), w=10, passo=True)
    a4 = 240 * _pp(p, 0.55, 0.40)
    # joelho: arco AMPLO
    d.arc([636, 1108, 712, 1184], 210, 340, fill=_c(R.GOLD, 0.85 * a4), width=4)
    _txt(d, (740, 1010), "joelho: quase normal", 24, R.TXT_L, a4)
    d.line([(700, 1120), (752, 1042)], fill=_c(R.MUT_L, 0.55 * a4), width=2)
    # tornozelo: arco REDUZIDO
    a5 = 240 * _pp(p, 0.68, 0.35)
    d.arc([664, 1168, 720, 1224], 250, 288, fill=_c(R.GOLD, a5), width=4)
    _txt(d, (748, 1156), "rigidez no tornozelo", 24, R.TXT_L, a5)
    d.line([(704, 1186), (742, 1170)], fill=_c(R.MUT_L, 0.55 * a5), width=2)


# PILOTO 4 — Silver-Russell, plano de 6 anos (Al Kaissi 2015, PMC4955504)

def _q_figura_discrepancia(d, spec, p, R):
    """Q1 do piloto 4: criança de frente, sem rosto; perna ESQUERDA mais curta (direita do
    espectador), escoliose e luxação do quadril DIREITO (esquerda do espectador) + cota."""
    a1 = 230 * _pp(p, 0.0, 0.45)
    cx = 330
    d.line([(200, 1210), (470, 1210)], fill=_c(R.CREAM, 0.22 * a1), width=3)  # chão
    _pessoa_frente(d, cx, 1210, 310, _c(R.CREAM, a1), w=9,
                   curta_lado=1, curta_dy=52, pelve_tilt=10, spine_curva=True)
    # rótulo escoliose (coluna com curva discreta)
    a2 = 235 * _pp(p, 0.25, 0.40)
    d.line([(cx + 16, 1010), (cx + 130, 964)], fill=_c(R.MUT_L, 0.55 * a2), width=2)
    _txt(d, (cx + 142, 950), "escoliose", 25, R.TXT_L, a2)
    # luxação do quadril direito (lado esquerdo do espectador): realce circular
    a3 = 235 * _pp(p, 0.38, 0.40)
    hx, hy = cx - 52, 1074
    d.ellipse([hx - 30, hy - 30, hx + 30, hy + 30], outline=_c(R.GOLD, a3), width=4)
    d.line([(hx - 16, hy + 26), (206, 1236)], fill=_c(R.MUT_L, 0.55 * a3), width=2)
    _txt(d, (150, 1236), "luxação do quadril", 24, R.TXT_L, a3)
    # barras de régua + cota da diferença (rótulo ACIMA das barras, dentro da margem)
    a4 = 245 * _pp(p, 0.50, 0.40)
    t1, t2 = _regua_barras(d, 620, 1210, 250, 198, _c(R.GOLD, 0.85 * a4), _c(R.GOLD, 0.55 * a4))
    _cota_v(d, 726, t1, t2, _c(R.CREAM, 0.85 * a4), w=3)
    _txt(d, (642, min(t1, t2) - 68), spec.get("cota", "diferença: 15 cm"), 28, R.GOLD,
         a4, negrito=True, centro=True)


def _q_trilha_cirurgias(d, spec, p, R):
    """Q2 do piloto 4: trilha 1–7 dos 7 aos 13 anos + 3 agrupamentos (quadril · coluna ·
    alongamento com fixador circular fiel e pé incluído). Marcos SÓ numerados (nota do
    storyboard: o artigo não lista as 7 uma a uma)."""
    # trilha
    a1 = 235 * _pp(p, 0.0, 0.35)
    y_tr = 1156
    d.line([(170, y_tr), (912, y_tr)], fill=_c(R.CREAM, 0.55 * a1), width=4)
    for i in range(7):
        a_m = 240 * _pp(p, 0.10 + i * 0.055, 0.25)
        x = 200 + i * 114
        d.ellipse([x - 19, y_tr - 19, x + 19, y_tr + 19], outline=_c(R.GOLD, a_m), width=4)
        _txt(d, (x, y_tr - 14), str(i + 1), 22, R.CREAM, a_m, centro=True)
    a2 = 240 * _pp(p, 0.16, 0.40)
    _txt(d, (200, y_tr + 40), spec.get("ini", "7 anos"), 25, R.TXT_L, a2, centro=True)
    _txt(d, (884, y_tr + 40), spec.get("fim", "13 anos"), 25, R.TXT_L, a2, centro=True)
    # agrupamento 1: quadril (esfera + cavidade + seta de recolocação)
    a3 = 240 * _pp(p, 0.30, 0.40)
    qx, qy = 240, 966
    d.arc([qx - 44, qy - 44, qx + 44, qy + 44], 200, 340, fill=_c(R.CREAM, a3), width=6)
    d.ellipse([qx - 17, qy + 2, qx + 17, qy + 36], outline=_c(R.GOLD, a3), width=5)
    _seta(d, (qx, qy + 78), (qx, qy + 44), _c(R.GOLD, a3), w=3, head=9)  # recolocação (p/ cima)
    _txt(d, (qx, 1056), "quadril", 26, R.TXT_L, a3, centro=True)
    # agrupamento 2: coluna (linha curva sendo alinhada por 2 hastes)
    a4 = 240 * _pp(p, 0.42, 0.40)
    cx2 = 530
    pts = [(cx2 + int(math.sin(t / 6 * math.pi) * 14), 924 + t * 16) for t in range(7)]
    d.line(pts, fill=_c(R.CREAM, a4), width=6)
    d.line([(cx2 - 26, 928), (cx2 - 26, 1028)], fill=_c(R.GOLD, a4), width=5)
    d.line([(cx2 + 26, 928), (cx2 + 26, 1028)], fill=_c(R.GOLD, a4), width=5)
    _txt(d, (cx2, 1056), "coluna", 26, R.TXT_L, a4, centro=True)
    # agrupamento 3: alongamento (mini-perna com fixador circular FIEL + pé incluído)
    a5 = 240 * _pp(p, 0.54, 0.40)
    ax = 810
    d.line([(ax - 22, 916), (ax - 18, 1034)], fill=_c(R.CREAM, 0.55 * a5), width=5)
    d.line([(ax + 22, 916), (ax + 18, 1034)], fill=_c(R.CREAM, 0.55 * a5), width=5)
    _osso_v(d, ax, 928, 966, _c(R.CREAM, 0.75 * a5), w=12)   # osso novo (tom claro) coxa
    _osso_v(d, ax, 986, 1022, _c(R.CREAM, 0.75 * a5), w=12)  # osso novo canela
    _aneis_fixador(d, ax, [934, 972, 1008], 56, 11, _c(R.GOLD, a5), _c(R.CREAM, 0.5 * a5),
                   hx=(-48, 48), y_haste=(934, 1040))
    d.ellipse([ax - 56, 1030, ax + 56, 1052], outline=_c(R.GOLD, a5), width=5)  # estribo do pé
    d.line([(ax - 14, 1034), (ax + 30, 1044)], fill=_c(R.CREAM, a5), width=5)   # pé
    _txt(d, (ax, 1076), "alongamento", 26, R.TXT_L, a5, centro=True)
    d.line([(ax + 40, 950), (ax + 96, 924)], fill=_c(R.MUT_L, 0.5 * a5), width=2)
    _txt(d, (ax + 60, 900), "osso novo", 20, R.MUT_L, a5)


def _q_ortese_resultado(d, spec, p, R):
    """Q3 do piloto 4: adolescente caminhando em perfil, órtese abaixo do joelho na perna
    esquerda + calçado com sola 5 cm mais alta; barras discretas com a cota; selo honesto."""
    a1 = 235 * _pp(p, 0.0, 0.42)
    perna = []
    chao = 1190
    d.line([(170, chao), (520, chao)], fill=_c(R.CREAM, 0.22 * a1), width=3)  # chão
    # figura menor e mais baixa: o pé da frente pousa SOBRE a sola compensada (26 px)
    _pessoa_perfil(d, 300, chao - 26, 272, _c(R.CREAM, a1), w=9, passo=True, perna_dest=perna)
    if perna:
        xj, yj, xpe, ype = perna
        # órtese abaixo do joelho: haste posterior ACOMPANHANDO a canela + apoio do pé
        a2 = 245 * _pp(p, 0.22, 0.40)
        d.line([(xj + 13, yj + 4), (xpe + 13, ype - 2)], fill=_c(R.GOLD, a2), width=7)
        d.line([(xpe - 4, ype + 9), (xpe + 34, ype + 9)], fill=_c(R.GOLD, a2), width=7)
        d.line([(xj + 3, yj + 20), (xj + 19, yj + 16)], fill=_c(R.GOLD, a2), width=5)
        d.line([((xj + xpe) // 2 + 16, (yj + ype) // 2), (452, 968)],
               fill=_c(R.MUT_L, 0.55 * a2), width=2)
        _txt(d, (464, 940), "órtese abaixo do joelho", 25, R.TXT_L, a2)
        # calçado com sola compensada (5 cm) sob o pé da frente, apoiada no chão
        a3 = 245 * _pp(p, 0.36, 0.40)
        d.rounded_rectangle([xpe - 10, chao - 26, xpe + 52, chao], radius=6,
                            fill=_c(R.GOLD, 0.6 * a3))
        _cota_v(d, xpe + 72, chao - 26, chao, _c(R.CREAM, 0.85 * a3), w=2, tick=8)
        _txt(d, (xpe + 90, chao - 30), spec.get("cota_calcado", "5 cm"), 25, R.GOLD, a3,
             negrito=True)
    # barras discretas + cota da diferença compensada (rótulo acima, dentro da margem)
    a4 = 240 * _pp(p, 0.50, 0.40)
    t1, t2 = _regua_barras(d, 790, chao, 200, 182, _c(R.GOLD, 0.7 * a4), _c(R.GOLD, 0.45 * a4),
                           larg=20, gap=38)
    _cota_v(d, 872, t1, t2, _c(R.CREAM, 0.8 * a4), w=2, tick=8)
    _txt(d, (809, min(t1, t2) - 92), "diferença: 5 cm", 24, R.GOLD, a4, negrito=True, centro=True)
    _txt(d, (809, min(t1, t2) - 60), "compensada", 22, R.MUT_L, a4, centro=True)
    # selo honesto do desfecho
    selo = spec.get("selo")
    if selo:
        a5 = 235 * _pp(p, 0.64, 0.36)
        f = _rr().F(R.NR, 22)
        wt = d.textlength(selo, font=f)
        x1 = 940
        d.rounded_rectangle([x1 - wt - 36, 1216, x1, 1258], radius=14,
                            outline=_c(R.MUT_L, 0.7 * a5), width=2)
        d.text((x1 - wt - 18, 1226), selo, font=f, fill=_c(R.MUT_L, a5))


_TIPOS = {
    "osso_falha": _q_osso_falha,
    "fixador_transporte": _q_fixador_transporte,
    "osso_continuo": _q_osso_continuo,
    "linha_tempo": _q_linha_tempo,
    "painel_triplo": _q_painel_triplo,
    "regua_resultado": _q_regua_resultado,
    "figura_discrepancia": _q_figura_discrepancia,
    "trilha_cirurgias": _q_trilha_cirurgias,
    "ortese_resultado": _q_ortese_resultado,
}


def desenhar(img, spec, tl, dur):
    """Ponto de entrada chamado pelo render_reel. img = frame RGB; spec = dict "ilustracao"
    da cena; tl = tempo dentro da cena (já com o ajuste retenção-3s da cena 0); dur = duração
    da cena. Desenha o quadro + o rótulo persistente do formato, tudo dentro da banda."""
    R = _rr()
    tipo = spec.get("tipo")
    if tipo not in _TIPOS:
        raise KeyError(f"ilustracao com tipo desconhecido: {tipo!r}")
    p = max(0.0, min(1.0, tl / max(dur, 1e-6)))
    ov = Image.new("RGBA", (R.W, R.H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    _TIPOS[tipo](d, spec, p, R)
    if spec.get("esmaecido"):
        alfa = ov.split()[3].point(lambda v: int(v * 0.15))
        ov.putalpha(alfa)
    dy = max(0, int(spec.get("dy", 0)))            # só desce (nunca invade o miolo de texto)
    if dy:
        desl = Image.new("RGBA", (R.W, R.H), (0, 0, 0, 0))
        desl.paste(ov, (0, dy), ov)
        ov = desl
    d2 = ImageDraw.Draw(ov)
    cit = spec.get("citacao")
    if cit:
        _cartao_citacao(d2, R, cit, p)
    # rótulo persistente do formato — SEMPRE, alpha cheio desde o frame 0
    f = R.F(R.NR, 20)
    wt = d2.textlength(ROTULO_FORMATO, font=f)
    d2.text(((R.W - wt) / 2, LABEL_Y), ROTULO_FORMATO, font=f, fill=_c(R.MUT_L, 255))
    img.paste(Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB"), (0, 0))
