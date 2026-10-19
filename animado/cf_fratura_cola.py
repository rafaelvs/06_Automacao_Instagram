# -*- coding: utf-8 -*-
"""COMO FUNCIONA — "Quem cola um osso quebrado?" (como a fratura cola: consolidação óssea).

Mesmo estilo e mesmas peças do piloto do alongamento (osso marfim, osso novo dourado, rótulos,
carimbo, brilhos, legenda karaokê, CTA com aviãozinho). Roteiro e cenas escritos por roteirista e
refutados por verificador adversarial (19/10/2026); o que o verificador exigiu está aqui:
  * NENHUM exame simulado: o "raio-X" é um VISOR (quatro cantos + linha de varredura) sobre o
    MESMO osso esquemático — nada de fundo preto, negativo, filme ou osso translúcido.
  * O calo preenche o vão na MESMA largura da diáfise (o acervo não descreve formato de calo).
  * Nenhuma célula "migrando": os pontinhos de obra surgem DENTRO do vão.
A cena é PRESA ao roteiro pelas palavras-âncora (ver `montar`): mudar o roteiro sem elas quebra o
render de propósito, em vez de sair vídeo dessincronizado.
"""
import math
import os
import re

import numpy as np
import skia

from . import som, voz as _voz
from .base import codificar, previas as _previas
from .cf_alongamento import (BG_OUT, CX, F_BLACK, F_REG, F_SEMI, FPS, H, HASTE, NOVO, NOVO_G, OSSO_B, OSSO_C,
                             OSSO_L, OURO, VASO, VERMELHO, W, Y_BASE, Y_TOPO, C, aviao, brilhos, clamp,
                             desenha_regenerado, e_back, e_in_back, e_inout, e_out, fundo, larg_texto, lerp, lerpc,
                             paint, path_osso_inf, path_osso_sup, prog, rotulo, sombra_osso, tecido_linha, texto)
from .cf_alongamento import comprimir as _comprimir_piloto  # noqa: F401 (referência do método)

YF = 760                       # altura da fratura (diáfise)
GAP = 46                       # vão entre as pontas depois que quebra
COAGULO = "#8E1B22"
DESTAQUE = {"quebrado", "corpo", "coágulo", "inflamação", "obra", "calo", "ósseo", "ponte", "estável",
            "sangue", "infecção", "resistência", "maduro", "semanas", "meses", "raio-x", "colar", "manda"}


def comprimir(voz, palavras, max_gap=0.30, limiar=0.42, respiro_cta=1.6):
    """Igual ao do piloto (encurta silêncio morto entre frases), mas com respiro MAIOR antes da
    CTA: aqui o visor do raio-X precisa de ~1,5 s de tela depois da última palavra."""
    import numpy as _np
    cortes = []
    for a, b in zip(palavras, palavras[1:]):
        fim_a = a["t"] + a["d"]; gap = b["t"] - fim_a
        alvo = respiro_cta if b["w"].lower() == "manda" else max_gap
        if gap > max(limiar, alvo):
            meio = fim_a + gap / 2; tirar = gap - alvo
            cortes.append((meio - tirar / 2, meio + tirar / 2))
    partes, ult = [], 0
    for c0, c1 in cortes:
        partes.append(voz[int(ult * som.SR):int(c0 * som.SR)]); ult = c1
    partes.append(voz[int(ult * som.SR):])
    nova = _np.concatenate(partes)
    if any(b["w"].lower() == "manda" and b["t"] - (a["t"] + a["d"]) < respiro_cta
           for a, b in zip(palavras, palavras[1:])):
        # silêncio original menor que o respiro: insere o que falta antes da CTA
        i = next(k for k, p in enumerate(palavras) if p["w"].lower() == "manda")
        fim_a = palavras[i - 1]["t"] + palavras[i - 1]["d"]
        falta = respiro_cta - (palavras[i]["t"] - fim_a)
        def remap0(t):
            return t - sum(min(c1, t) - c0 for c0, c1 in cortes if t > c0)
        pos = int(remap0(fim_a + 0.05) * som.SR)
        nova = _np.concatenate([nova[:pos], _np.zeros(int(falta * som.SR)), nova[pos:]])
        cortes_extra = (fim_a + 0.05, falta)
    else:
        cortes_extra = None

    def remap(t):
        t2 = t - sum(min(c1, t) - c0 for c0, c1 in cortes if t > c0)
        if cortes_extra and t > cortes_extra[0]:
            t2 += cortes_extra[1]
        return t2
    return nova, [dict(p, t=remap(p["t"])) for p in palavras], sum(c1 - c0 for c0, c1 in cortes)


# ------------------------------------------------------------------ texto do roteiro -> palavras
def alinhar(palavras, roteiro):
    """Como no piloto, mas aceitando palavra com hífen ("raio-X"): o edge-tts devolve "raio-X"
    como UMA palavra, e o regex antigo a partia em duas — o verificador apontou o KeyError."""
    toks = re.findall(r"[\wÀ-ÿ]+(?:-[\wÀ-ÿ]+)*[.,:;!?—]*", roteiro)
    out = []; j = 0
    for p in palavras:
        alvo = p["w"].lower()
        while j < len(toks) and re.sub(r"[.,:;!?—]", "", toks[j]).lower() != alvo:
            j += 1
        tok = toks[j] if j < len(toks) else p["w"]
        out.append(dict(p, tok=tok, fim_frase=bool(re.search(r"[.!?:]$", tok)), virg=tok.endswith(",")))
        j += 1
    return out


def montar_blocos(pal):
    frases, atual = [], []
    for p in pal:
        atual.append(p)
        if p["fim_frase"]:
            frases.append(atual); atual = []
    if atual:
        frases.append(atual)
    blocos = []
    for fr in frases:
        if len(fr) <= 6 or fr[0]["w"].lower() == "manda":
            blocos.append(fr); continue
        n = math.ceil(len(fr) / 5); alvo = len(fr) / n; ini = 0
        for k in range(1, n):
            corte = round(alvo * k)
            virgs = [i + 1 for i in range(ini, len(fr) - 1) if fr[i]["virg"] and abs(i + 1 - corte) <= 1]
            corte = virgs[0] if virgs else corte
            blocos.append(fr[ini:corte]); ini = corte
        blocos.append(fr[ini:])
    return blocos


def legenda(cv, blocos, t, y_base=1395, tam=80):
    vivo = None
    for i, b in enumerate(blocos):
        ini = b[0]["t"] - 0.12
        fim = blocos[i + 1][0]["t"] - 0.12 if i + 1 < len(blocos) else b[-1]["t"] + b[-1]["d"] + 2.5
        if ini <= t < fim:
            vivo = b; break
    if not vivo:
        return
    esp = 26; linhas, linha, lw = [], [], 0
    for p in vivo:
        w = larg_texto(p["tok"].upper(), F_BLACK, tam)
        if linha and lw + esp + w > 920:
            linhas.append(linha); linha, lw = [], 0
        linha.append((p, w)); lw += (esp if lw else 0) + w
    if linha:
        linhas.append(linha)
    entrada = e_out(clamp((t - (vivo[0]["t"] - 0.12)) / 0.15))
    alt = tam * 1.18
    y = y_base - (len(linhas) - 1) * alt / 2 + (1 - entrada) * 24
    for ln in linhas:
        total = sum(w for _, w in ln) + esp * (len(ln) - 1); x = CX - total / 2
        for p, w in ln:
            k = t - p["t"]; base = re.sub(r"[.,:;!?—]", "", p["tok"]).lower()
            dita = k >= -0.03; falando = p["t"] - 0.03 <= t <= p["t"] + p["d"] + 0.06
            cor, a = (OURO, 255) if falando else ((OURO if base in DESTAQUE else "#FFFFFF"), 255) if dita else ("#FFFFFF", 105)
            esc = 1.0 + (0.06 * (1 - e_out(clamp(k / 0.16))) if dita else 0.0)
            cv.save(); cv.translate(x, y); cv.scale(esc, esc)
            texto(cv, p["tok"].upper(), 0, 0, F_BLACK, tam, cor, int(a * entrada), centro=False, contorno=12)
            cv.restore()
            x += w + esp
        y += alt


# ------------------------------------------------------------------ cronologia
def montar(pal):
    def em(palavra, n=1, prefixo=False):
        c = 0
        for p in pal:
            w = p["w"].lower()
            if w == palavra or (prefixo and w.startswith(palavra)):
                c += 1
                if c == n:
                    return p["t"]
        raise KeyError(f"palavra-âncora não achada no roteiro: {palavra} #{n}")
    fim = pal[-1]["t"] + pal[-1]["d"]
    T = dict(quebrado=em("quebrado"), corpo=em("corpo"), coagulo=em("coágulo"), inflamacao=em("inflamação"),
             etapa=em("etapa"), obra=em("obra"), tecido=em("tecido"), osseo=em("ósseo"), ponte=em("ponte"),
             pontas=em("pontas"), firmar=em("firmar"), estavel=em("estável"), sangue=em("sangue"),
             infeccao=em("infecção"), tempo=em("tempo"), resistencia=em("resistência"), maduro=em("maduro"),
             semanas=em("semanas"), raio=em("raio", prefixo=True), manda=em("manda"), fim_fala=fim)
    T["total"] = fim + 2.2
    return T


# ------------------------------------------------------------------ geometria da fratura
def _zig(y, n=9):
    x0, x1 = CX - HASTE / 2 - 6, CX + HASTE / 2 + 6
    return [(lerp(x0, x1, k / (n - 1)), y + (9 if k % 2 else -9)) for k in range(n)]


def _regiao_acima(y):
    p = skia.Path(); p.moveTo(0, 0); p.lineTo(W, 0)
    z = _zig(y)
    p.lineTo(W, z[-1][1])
    for x, yy in reversed(z):
        p.lineTo(x, yy)
    p.lineTo(0, z[0][1]); p.close(); return p


def _regiao_abaixo(y):
    p = skia.Path(); z = _zig(y)
    p.moveTo(0, z[0][1])
    for x, yy in z:
        p.lineTo(x, yy)
    p.lineTo(W, z[-1][1]); p.lineTo(W, H * 3); p.lineTo(0, H * 3); p.close(); return p


def _vao(gap, folga=0):
    """Polígono entre as duas bordas serrilhadas, na largura da diáfise (+folga)."""
    z1 = _zig(YF); z2 = _zig(YF + gap)
    p = skia.Path(); p.moveTo(z1[0][0] - folga, z1[0][1])
    for x, y in z1:
        p.lineTo(x, y)
    p.lineTo(z1[-1][0] + folga, z1[-1][1])
    p.lineTo(z2[-1][0] + folga, z2[-1][1])
    for x, y in reversed(z2):
        p.lineTo(x, y)
    p.lineTo(z2[0][0] - folga, z2[0][1]); p.close(); return p


def _osso_inteiro():
    p = path_osso_sup(Y_TOPO, YF + 2)
    p.addPath(path_osso_inf(YF - 2, Y_BASE))
    return p


def _desenha_fragmentos(cv, gap, tremor_x, brilho_pontas):
    sh = sombra_osso(); osso = _osso_inteiro()
    cv.save(); cv.clipPath(_regiao_acima(YF), skia.ClipOp.kIntersect, True)
    cv.drawPath(osso, paint("#000000", 70, blur=14)); cv.drawPath(osso, paint(OSSO_C, shader=sh))
    cv.drawPath(osso, paint(OSSO_L, 150, "stroke", 2.5))
    cv.restore()
    cv.save(); cv.translate(tremor_x, gap)
    cv.clipPath(_regiao_abaixo(YF), skia.ClipOp.kIntersect, True)
    cv.drawPath(osso, paint("#000000", 70, blur=14)); cv.drawPath(osso, paint(OSSO_C, shader=sh))
    cv.drawPath(osso, paint(OSSO_L, 150, "stroke", 2.5))
    cv.restore()
    if brilho_pontas > 0:
        for y in (YF, YF + gap):
            cv.drawRect(skia.Rect(CX - HASTE / 2, y - 14, CX + HASTE / 2, y + 14), paint("#FFFFFF", int(160 * brilho_pontas), blur=8))


# ------------------------------------------------------------------ elementos
def carimbo_ouro(cv, s, x, y, rot, t0, t, dur=1.9):
    k = t - t0
    if k < 0 or k > dur:
        return
    esc = lerp(1.9, 1.0, e_out(clamp(k / 0.16))); a = clamp(k / 0.08) * (1 - prog(k, dur - 0.35, dur))
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(esc, esc)
    f = skia.Font(F_BLACK, 62); lw = f.measureText(s)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 24, -62, lw / 2 + 24, 22), 12, 12)
    cv.drawRRect(rr, paint("#0B1824", int(160 * a))); cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 7))
    cv.drawString(s, -lw / 2, 0, f, paint(OURO, int(255 * a)))
    cv.restore()


def placa_obras(cv, x, y, a):
    if a <= 0:
        return
    w, h = 210, 96
    cv.save(); cv.translate(x, y)
    cv.drawRect(skia.Rect(-w / 2 + 20, h / 2 - 4, -w / 2 + 30, h / 2 + 60), paint("#5A4632", int(255 * a)))
    cv.drawRect(skia.Rect(w / 2 - 30, h / 2 - 4, w / 2 - 20, h / 2 + 60), paint("#5A4632", int(255 * a)))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-w / 2, -h / 2, w / 2, h / 2), 10, 10), paint("#F5C04A", int(255 * a)))
    cv.save(); cv.clipRect(skia.Rect(-w / 2, -h / 2, w / 2, h / 2))
    for k in range(-6, 8):                                     # faixas zebradas na borda
        x0 = k * 30
        p = skia.Path(); p.moveTo(x0, -h / 2); p.lineTo(x0 + 15, -h / 2); p.lineTo(x0 + 5, -h / 2 + 16); p.lineTo(x0 - 10, -h / 2 + 16); p.close()
        cv.drawPath(p, paint("#1A1A1A", int(255 * a)))
        q = skia.Path(); q.moveTo(x0, h / 2 - 16); q.lineTo(x0 + 15, h / 2 - 16); q.lineTo(x0 + 5, h / 2); q.lineTo(x0 - 10, h / 2); q.close()
        cv.drawPath(q, paint("#1A1A1A", int(255 * a)))
    cv.restore()
    texto(cv, "EM OBRAS", 0, 14, F_BLACK, 38, "#1A1A1A", int(255 * a))
    cv.restore()


def checklist(cv, itens, t, a_geral):
    if a_geral <= 0:
        return
    x0 = 640
    for k, (rot, t_ok) in enumerate(itens):
        y = 520 + k * 96
        a = a_geral
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y - 42, x0 + 50, y + 8), 10, 10), paint("#0B1824", int(220 * a)))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y - 42, x0 + 50, y + 8), 10, 10), paint(OURO, int(255 * a), "stroke", 3.5))
        if t >= t_ok:
            pr = e_out(clamp((t - t_ok) / 0.3))
            p = skia.Path(); p.moveTo(x0 + 10, y - 18)
            p.lineTo(x0 + 10 + 12 * min(1, pr * 2), y - 18 + 12 * min(1, pr * 2))
            if pr > 0.5:
                q = (pr - 0.5) * 2
                p.lineTo(x0 + 22 + 22 * q, y - 6 - 30 * q)
            cv.drawPath(p, paint(OURO, int(255 * a), "stroke", 6))
            texto(cv, rot, x0 + 66, y - 4, F_BLACK, 36, "#FFFFFF", int(255 * a * clamp((t - t_ok) / 0.2)), centro=False, contorno=8)


def calendario(cv, x, y, t, t0, a):
    if a <= 0:
        return
    cv.save(); cv.translate(x, y)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(0, 0, 96, 92), 12, 12), paint("#EEF3F8", int(255 * a)))
    cv.drawRect(skia.Rect(0, 0, 96, 24), paint(VERMELHO, int(255 * a)))
    for xx in (24, 72):
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(xx - 4, -8, xx + 4, 10), 3, 3), paint("#5E7186", int(255 * a)))
    k = (t - t0) * 5                                           # folhas virando, sem número
    fase = k - math.floor(k)
    for i in range(3):
        cv.drawLine(14, 42 + i * 16, 82, 42 + i * 16, paint("#9AA8B5", int(200 * a), "stroke", 4))
    cv.save(); cv.translate(0, 24); cv.scale(1, 1 - fase)
    cv.drawRect(skia.Rect(0, 0, 96, 68), paint("#FFFFFF", int(150 * a * (1 - fase))))
    cv.restore()
    cv.restore()


def visor(cv, t, t0, a):
    """Visor de mira sobre o osso esquemático: NÃO é exame (guardrail de raio-X)."""
    if a <= 0:
        return
    x0, y0, x1, y1 = 330, 560, 750, 1010
    L = 56
    for (x, y, dx, dy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        cv.drawLine(x, y, x + dx * L, y, paint(OURO, int(255 * a), "stroke", 6))
        cv.drawLine(x, y, x, y + dy * L, paint(OURO, int(255 * a), "stroke", 6))
    rr = skia.RRect.MakeRectXY(skia.Rect(CX - 80, y0 - 64, CX + 80, y0 - 14), 14, 14)
    cv.drawRRect(rr, paint("#0B1824", int(220 * a))); cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 3))
    texto(cv, "RAIO-X", CX, y0 - 26, F_BLACK, 32, OURO, int(255 * a))
    k = prog(t, t0 + 0.15, t0 + 0.85)
    if 0 < k < 1:
        y = lerp(y0 + 10, y1 - 10, e_inout(k))
        cv.drawLine(x0 + 14, y, x1 - 14, y, paint(OURO, int(150 * a), "stroke", 14, blur=10))
        cv.drawLine(x0 + 14, y, x1 - 14, y, paint("#FFF4CF", int(255 * a), "stroke", 3))
    if t >= t0 + 0.6:
        pr = e_out(clamp((t - t0 - 0.6) / 0.3))
        cx, cy = x1 + 40, (y0 + y1) / 2
        cv.drawCircle(cx, cy, 40, paint("#0B1824", int(230 * a * pr)))
        cv.drawCircle(cx, cy, 40, paint(OURO, int(255 * a * pr), "stroke", 4))
        p = skia.Path(); p.moveTo(cx - 18, cy); p.lineTo(cx - 5, cy + 14); p.lineTo(cx + 20, cy - 16)
        cv.drawPath(p, paint(OURO, int(255 * a * pr), "stroke", 7))
        texto(cv, "RAIO-X CONFIRMA", CX, y1 + 66, F_BLACK, 44, "#FFFFFF", int(255 * a * pr), contorno=8)


# ------------------------------------------------------------------ quadro
RNG = np.random.default_rng(23)
OBREIROS = [(RNG.uniform(-50, 50), RNG.uniform(0.2, 0.8), RNG.uniform(0, 6.28), RNG.uniform(1.5, 3.0)) for _ in range(9)]


def quadro(cv, t, T, blocos):
    fundo(cv, t)
    quebrou = e_out(prog(t, T["quebrado"] + 0.05, T["quebrado"] + 0.35))
    gap = GAP * quebrou

    # câmera: mostra o osso inteiro na capa, aproxima na fratura, recua no fim
    s = lerp(1.0, 1.42, e_inout(prog(t, T["quebrado"] + 0.3, T["coagulo"])))
    s = lerp(s, 1.12, e_inout(prog(t, T["tempo"], T["maduro"])))
    foco = lerp((Y_TOPO + Y_BASE) / 2, YF + GAP / 2, e_inout(prog(t, T["quebrado"] + 0.3, T["coagulo"])))
    tremor = 0.0
    for t0, f in ((T["quebrado"] + 0.08, 10), (T["etapa"], 5), (T["estavel"], 4)):
        k = t - t0
        if 0 <= k < 0.35:
            tremor += f * math.sin(k * 70) * (1 - k / 0.35)
    cv.save(); cv.translate(W / 2 + tremor, 790); cv.scale(s, s); cv.translate(-CX, -foco)

    # inflamação: halo pulsando atrás
    a_inf = prog(t, T["inflamacao"] - 0.1, T["inflamacao"] + 0.4) * (1 - prog(t, T["tecido"] + 1.2, T["tecido"] + 2.2))
    if a_inf > 0:
        r = 150 + 18 * math.sin(t * 3.2)
        cv.drawCircle(CX, YF + gap / 2, r, paint("#FF7A3D", int(110 * a_inf), blur=40))

    # vaso (sangue chegando), ao lado do osso
    a_vaso = prog(t, T["sangue"] - 0.1, T["sangue"] + 0.4) * (1 - prog(t, T["tempo"], T["tempo"] + 0.7))
    if a_vaso > 0:
        tecido_linha(cv, CX - 98, YF - 300, YF + gap + 300, 10, VASO, 6, a_vaso, t, 0.0)
        for i in range(7):                                     # glóbulos correndo até o calo
            f = ((t - T["sangue"]) * 0.5 + i / 7) % 1.0
            y = lerp(YF - 300, YF + gap / 2, f)
            cv.drawCircle(CX - 98 + 10 * math.sin(t * 1.4 + y * 0.12), y, 6, paint("#FF8A8F", int(255 * a_vaso)))

    # fragmentos (o de baixo treme até "estável")
    trem = 0.0
    if T["firmar"] <= t < T["estavel"]:
        trem = 3.5 * math.sin(t * 38)
    brilho_pontas = max(0.0, 1 - abs(t - (T["pontas"] + 0.15)) / 0.4)
    _desenha_fragmentos(cv, gap, trem, brilho_pontas)

    # o vão: coágulo -> obra -> calo -> osso maduro
    if gap > 1:
        cv.save(); cv.clipPath(_vao(gap, folga=4), skia.ClipOp.kIntersect, True)
        a_coag = e_back(clamp((t - T["coagulo"]) / 0.4)) if t >= T["coagulo"] else 0.0
        some = prog(t, T["tecido"], T["osseo"] + 0.6)
        if a_coag > 0 and some < 1:
            for i, (dx, fy, fase, _) in enumerate(OBREIROS[:7]):
                rr = 22 * a_coag * (0.8 + 0.2 * math.sin(t * 2 + fase))
                cv.drawCircle(CX + dx, YF + gap * fy, rr, paint(COAGULO, int(255 * (1 - some))))
        dens = e_inout(prog(t, T["tecido"], T["osseo"] + 0.2))
        brilho = prog(t, T["osseo"] - 0.1, T["osseo"] + 0.3) * (1 - prog(t, T["tempo"], T["maduro"]))
        duro = e_inout(prog(t, T["tempo"], T["maduro"]))
        if dens > 0:
            desenha_regenerado(cv, YF - 12, YF + gap + 12, dens, max(brilho, 0.3 * dens * (1 - duro)), duro, t)
        cv.restore()
        if T["tecido"] <= t < T["osseo"] + 1.0:                # "equipe de obra" trabalhando DENTRO do vão
            a = prog(t, T["tecido"], T["tecido"] + 0.3) * (1 - prog(t, T["osseo"] + 0.5, T["osseo"] + 1.0))
            for dx, fy, fase, vel in OBREIROS:
                x = CX + dx + 8 * math.sin(t * vel + fase); y = YF + gap * fy + 5 * math.cos(t * vel * 1.3 + fase)
                cv.drawCircle(x, y, 6, paint(NOVO_G, int(255 * a)))

    # ponte: arco pontilhado de uma ponta à outra
    if t >= T["ponte"] and t < T["tempo"] + 0.5:
        pr = e_out(clamp((t - T["ponte"]) / 0.7)); a = 1 - prog(t, T["tempo"], T["tempo"] + 0.5)
        n = 22
        for i in range(int(n * pr) + 1):
            ang = math.pi * (i / n)
            x = CX - HASTE / 2 - 24 - 70 * math.sin(ang); y = lerp(YF - 40, YF + gap + 40, i / n)
            cv.drawCircle(x, y, 5, paint(OURO, int(255 * a)))
    brilhos(cv, CX, YF + gap / 2, t, T["pontas"] + 0.1)

    # rótulos (espaço da câmera)
    rotulo(cv, "COÁGULO", CX - 360, YF + 40, CX - 50, YF + gap / 2, VERMELHO,
           prog(t, T["coagulo"], T["coagulo"] + 0.25) * (1 - prog(t, T["etapa"] + 0.6, T["etapa"] + 1.0)))
    rotulo(cv, "INFLAMAÇÃO", CX + 350, YF - 90, CX + 70, YF + gap / 2 - 10, "#FF9A5C",
           prog(t, T["inflamacao"], T["inflamacao"] + 0.25) * (1 - prog(t, T["etapa"] + 0.6, T["etapa"] + 1.0)), esq=False)
    rotulo(cv, "CALO ÓSSEO", CX + 350, YF + gap + 110, CX + 60, YF + gap / 2, OURO,
           prog(t, T["osseo"], T["osseo"] + 0.25) * (1 - prog(t, T["firmar"] - 0.3, T["firmar"])), esq=False)
    # à ESQUERDA: a direita é da barra de resistência, que está subindo nessa hora
    rotulo(cv, "OSSO MADURO", CX - 380, YF + gap + 200, CX - 60, YF + gap / 2, OSSO_C,
           prog(t, T["maduro"], T["maduro"] + 0.25) * (1 - prog(t, T["raio"] - 0.4, T["raio"])))

    # placa EM OBRAS (sai quando o raio-X confirma)
    entra = e_back(prog(t, T["obra"], T["obra"] + 0.5)); sai = e_in_back(prog(t, T["raio"] + 1.3, T["raio"] + 1.9))
    if t >= T["obra"]:
        placa_obras(cv, lerp(CX - 700, CX - 250, entra) - 600 * sai, YF + gap / 2 - 10, 1 - prog(t, T["raio"] + 1.7, T["raio"] + 1.9))
    carimbo_ouro(cv, "ETAPA 1", CX + 170, YF - 170, -8, T["etapa"], t)
    cv.restore()

    # ---------------- interface fixa
    sai_g = e_inout(prog(t, T["corpo"], T["corpo"] + 0.5))
    if sai_g < 1:
        a = 1 - sai_g
        cv.drawRect(skia.Rect(0, 0, W, 360), paint(BG_OUT, 255, shader=skia.GradientShader.MakeLinear(
            [skia.Point(0, 0), skia.Point(0, 360)], [C(BG_OUT, int(235 * a)), C(BG_OUT, 0)])))
        pulso = 1 + 0.025 * math.sin(t * 5)
        cv.save(); cv.translate(CX, 205 - 60 * sai_g); cv.scale(pulso, pulso)
        texto(cv, "QUEM COLA UM", 0, 0, F_BLACK, 78, "#FFFFFF", int(255 * a), contorno=10)
        texto(cv, "OSSO QUEBRADO?", 0, 88, F_BLACK, 78, OURO, int(255 * a), contorno=10)
        cv.restore()
        if t < T["quebrado"] + 0.05:                           # linha de fratura piscando (capa)
            pisca = 0.5 + 0.5 * math.sin(t * 9)
            z = _zig(YF)
            p = skia.Path(); p.moveTo(*z[0])
            for x, y in z[1:]:
                p.lineTo(x, y)
            cv.save(); cv.translate(W / 2, 790); cv.translate(-CX, -(Y_TOPO + Y_BASE) / 2)
            cv.drawPath(p, paint(VERMELHO, int(130 + 125 * pisca), "stroke", 6))
            cv.restore()
    perto = e_inout(prog(t, T["quebrado"] + 0.3, T["coagulo"])) * (1 - e_inout(prog(t, T["tempo"], T["maduro"])))
    a0 = prog(t, T["corpo"] + 0.3, T["corpo"] + 0.7) * (1 - prog(t, T["manda"] - 0.3, T["manda"])) * (1 - perto)
    if a0 > 0:
        rr = skia.RRect.MakeRectXY(skia.Rect(CX - 190, 150, CX + 190, 204), 27, 27)
        cv.drawRRect(rr, paint("#FFFFFF", int(28 * a0)))
        texto(cv, "COMO FUNCIONA", CX, 190, F_BLACK, 32, OURO, int(255 * a0))

    # indicador de fase -> calendário
    a_fase = prog(t, T["corpo"] + 0.3, T["corpo"] + 0.7) * (1 - prog(t, T["semanas"] - 0.3, T["semanas"]))
    if a_fase > 0:
        for i, (rot, t_on) in enumerate((("1 COÁGULO", T["coagulo"]), ("2 CALO", T["osseo"]), ("3 OSSO MADURO", T["maduro"]))):
            y = 268 + i * 52; on = t >= t_on
            cv.drawCircle(84, y - 12, 13, paint(OURO if on else "#FFFFFF", int(255 * a_fase) if on else int(90 * a_fase),
                                                 "fill" if on else "stroke", 0 if on else 3))
            if on:
                cv.drawCircle(84, y - 12, 18, paint(OURO, int(90 * a_fase), blur=8))
            texto(cv, rot, 110, y, F_BLACK, 32, "#FFFFFF" if on else "#8FA3B8", int(255 * a_fase), centro=False)
    a_cal = prog(t, T["semanas"] - 0.2, T["semanas"] + 0.2) * (1 - prog(t, T["manda"] - 0.3, T["manda"]))
    if a_cal > 0:
        calendario(cv, 70, 236, t, T["semanas"], a_cal)
        texto(cv, "SEMANAS A MESES", 186, 288, F_BLACK, 40, "#FFFFFF", int(255 * a_cal), centro=False, contorno=6)
        texto(cv, "sem prazo único", 188, 330, F_SEMI, 30, "#9CC9FF", int(255 * a_cal), centro=False)

    # barra RESISTÊNCIA (some durante o checklist)
    # a barra só aparece quando sobe de verdade (a partir de "tempo"): antes, os rótulos da
    # direita (inflamação, calo) ocupam esse lado e a barra cruzaria com eles
    a_bar = prog(t, T["tempo"], T["tempo"] + 0.4) * (1 - prog(t, T["manda"] - 0.3, T["manda"]))
    a_bar = clamp(a_bar)
    if a_bar > 0:
        nivel = lerp(0.12, 0.7, e_inout(prog(t, T["tempo"], T["resistencia"])))
        if t >= T["resistencia"]:
            nivel = lerp(0.7, 1.0, e_out(prog(t, T["resistencia"], T["resistencia"] + 0.6)))
        x = 968; ytop, ybot = 340, 1060
        texto(cv, "RESISTÊNCIA", x - 30, 312, F_BLACK, 26, OURO, int(255 * a_bar))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 16, ytop, x + 16, ybot), 16, 16), paint("#FFFFFF", int(40 * a_bar)))
        alt = (ybot - ytop - 8) * nivel
        if alt > 0:
            cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 12, ybot - 4 - alt, x + 12, ybot - 4), 12, 12), paint(OURO, int(255 * a_bar)))
            if nivel >= 0.99:
                cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 18, ytop, x + 18, ybot), 18, 18), paint(OURO, int(80 * a_bar), blur=12))

    # checklist do tripé
    a_ck = prog(t, T["firmar"], T["firmar"] + 0.3) * (1 - prog(t, T["tempo"], T["tempo"] + 0.5))
    checklist(cv, (("OSSO ESTÁVEL", T["estavel"]), ("SANGUE CHEGANDO", T["sangue"]), ("SEM INFECÇÃO", T["infeccao"])), t, a_ck)

    # visor do raio-X (esquemático)
    a_vis = prog(t, T["raio"] - 0.1, T["raio"] + 0.2) * (1 - prog(t, T["manda"] - 0.4, T["manda"] - 0.1))
    visor(cv, t, T["raio"], a_vis)

    t_cta = T["manda"] - 0.15
    if t < t_cta:
        legenda(cv, blocos, t)
    if 3.0 <= t < t_cta:
        a = prog(t, 3.0, 3.6)
        texto(cv, "Dr. Rafael Vargas · Médico · CRM-SP 226103 · RQE 137901", CX, 1585, F_SEMI, 27, "#FFFFFF", int(200 * a))
        texto(cv, "Conteúdo educativo · não substitui avaliação médica · voz digital (IA)", CX, 1620, F_REG, 23, "#FFFFFF", int(150 * a))
    if t >= t_cta:
        a = prog(t, t_cta, t_cta + 0.35)
        cv.drawRect(skia.Rect(0, 0, W, H), paint(BG_OUT, int(175 * a)))
        legenda(cv, blocos, t, y_base=700, tam=92)
        aviao(cv, t, T["manda"] + 0.2)
        rr = skia.RRect.MakeRectXY(skia.Rect(150, 1060, 930, 1214), 28, 28)
        cv.drawRRect(rr, paint("#0B1824", int(230 * a))); cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 3))
        texto(cv, "Dr. Rafael Vargas · Médico ortopedista", CX, 1112, F_BLACK, 36, "#FFFFFF", int(255 * a))
        texto(cv, "CRM-SP 226103 · RQE 137901 · @rafaelvargasmd", CX, 1154, F_SEMI, 28, OURO, int(255 * a))
        texto(cv, "Conteúdo educativo · não substitui avaliação médica · voz digital (IA)", CX, 1190, F_REG, 22, "#FFFFFF", int(170 * a))


# ------------------------------------------------------------------ entrada única
def render(ep, mp4, tmp, previa=False):
    roteiro = "\n".join(ep["roteiro"])
    voz_bruta, palavras = _voz.narrar(roteiro, _voz.RITMO_COMO_FUNCIONA, os.path.join(tmp, "voz"))
    voz_c, pal, tirado = comprimir(voz_bruta, palavras)
    pal = alinhar(pal, roteiro)
    T = montar(pal)
    print(f"{ep['id']}: silêncio cortado {tirado:.2f}s | duração final {T['total']:.2f}s")
    blocos = montar_blocos(pal)

    def quadro_t(cv, t):
        quadro(cv, t, T, blocos)

    if previa:
        tempos = (0.4, T["quebrado"] + 0.6, T["coagulo"] + 0.6, T["etapa"] + 0.4, T["osseo"] + 0.5, T["pontas"] + 0.3,
                  T["infeccao"] + 0.6, T["resistencia"] + 0.7, T["semanas"] + 0.5, T["raio"] + 1.2, T["manda"] + 1.6)
        return _previas(quadro_t, tempos, tmp, ep["id"]), T["total"]
    ev = [(T["quebrado"] + 0.06, "tick", 1.0), (T["quebrado"] + 0.08, "thump", 0.6), (T["corpo"], "whoosh", 0.35),
          (T["coagulo"], "pop", 0.9), (T["etapa"] - 0.02, "thump", 0.8), (T["obra"] + 0.3, "thump", 0.45),
          (T["tecido"], "shimmer", 0.35), (T["osseo"] - 0.05, "shimmer", 0.85), (T["pontas"] + 0.1, "shimmer", 0.5),
          (T["estavel"], "thump", 0.6), (T["sangue"], "whoosh", 0.3), (T["infeccao"], "ping", 0.5),
          (T["maduro"], "crackle", 0.8), (T["raio"], "whoosh", 0.4), (T["raio"] + 0.6, "ding", 0.55),
          (T["manda"] + 0.05, "whoosh", 0.5)]
    ev += [(T["tecido"] + 0.18 * i, "click", 0.7) for i in range(9)]       # a "obra" trabalhando
    wav = os.path.join(tmp, f"{ep['id']}_mix.wav")
    som.gravar_wav(wav, som.mixar(voz_c, T["total"], ev, ganho_trilha=0.40))
    codificar(quadro_t, T["total"], wav, mp4)
    return mp4, T["total"]
