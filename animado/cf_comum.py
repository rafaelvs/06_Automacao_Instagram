# -*- coding: utf-8 -*-
"""Peças comuns às cenas de COMO FUNCIONA a partir do lote 2 (sincronia com a voz, legenda karaokê,
capa, identificação CFM e cartão final). As duas cenas do lote 1 (cf_alongamento e cf_fratura_cola)
ficam como estão — vídeos já aprovados e renderizados; este módulo reaproveita as funções delas.

Contrato de uma cena nova `animado/cf_<nome>.py`:
  * `ANCORAS`: {chave: (palavra, ocorrência, prefixo)} — palavras do roteiro que disparam cada
    acontecimento. Palavra ausente = KeyError no render (vídeo dessincronizado não sai).
  * `DESTAQUE`: palavras que ficam douradas na legenda depois de ditas.
  * `quadro(cv, t, T, blocos, ep)` desenha o mundo e chama `interface(...)` no fim. O gancho vem de
    `ep["gancho"]` e todo rótulo desenhado tem de estar em `ep["tela"]` (o render recusa o vídeo se
    algum texto desenhado não for do episódio).
  * `render = fazer_render(quadro, ANCORAS, sons, tempos_previa)` no nível de cima do módulo (é
    isso que faz o portão reconhecer o arquivo como cena).
"""
import math
import os

import skia

from . import som, voz as _voz
from .base import codificar, previas as _previas
from .cf_alongamento import (BG_OUT, CX, F_BLACK, F_REG, F_SEMI, H, OURO, W, C, aviao, clamp, e_out,
                             larg_texto, paint, prog, texto)
from .cf_fratura_cola import alinhar, comprimir, montar_blocos  # noqa: F401 (reexportados)

SIG = "Dr. Rafael Vargas · Médico · CRM-SP 226103 · RQE 137901"
DISC = "Conteúdo educativo · não substitui avaliação médica · voz digital (IA)"


def ancoras(pal, mapa):
    """{chave: tempo} a partir de {chave: (palavra, n, prefixo)}; falta de âncora aborta."""
    T = {}
    for chave, (palavra, n, prefixo) in mapa.items():
        c = 0
        for p in pal:
            w = p["w"].lower()
            if w == palavra or (prefixo and w.startswith(palavra)):
                c += 1
                if c == n:
                    T[chave] = p["t"]; break
        else:
            raise KeyError(f"palavra-âncora não achada no roteiro: {palavra} #{n}")
    T["fim_fala"] = pal[-1]["t"] + pal[-1]["d"]
    T["total"] = T["fim_fala"] + 2.2
    return T


def legenda(cv, blocos, t, destaque, y_base=1395, tam=80):
    """Legenda karaokê (mesma tipografia e regras do lote 1)."""
    import re
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
            cor, a = (OURO, 255) if falando else ((OURO if base in destaque else "#FFFFFF"), 255) if dita else ("#FFFFFF", 105)
            esc = 1.0 + (0.06 * (1 - e_out(clamp(k / 0.16))) if dita else 0.0)
            cv.save(); cv.translate(x, y); cv.scale(esc, esc)
            texto(cv, p["tok"].upper(), 0, 0, F_BLACK, tam, cor, int(a * entrada), centro=False, contorno=12)
            cv.restore()
            x += w + esp
        y += alt


def capa(cv, t, t_sai, linha1, linha2):
    """Gancho de 2 linhas no topo; some a partir de `t_sai`."""
    from .cf_alongamento import e_inout
    sai = e_inout(prog(t, t_sai, t_sai + 0.5))
    if sai >= 1:
        return
    a = 1 - sai
    cv.drawRect(skia.Rect(0, 0, W, 360), paint(BG_OUT, 255, shader=skia.GradientShader.MakeLinear(
        [skia.Point(0, 0), skia.Point(0, 360)], [C(BG_OUT, int(235 * a)), C(BG_OUT, 0)])))
    pulso = 1 + 0.025 * math.sin(t * 5)
    cv.save(); cv.translate(CX, 205 - 60 * sai); cv.scale(pulso, pulso)
    texto(cv, linha1, 0, 0, F_BLACK, 78, "#FFFFFF", int(255 * a), contorno=10)
    texto(cv, linha2, 0, 88, F_BLACK, 78, OURO, int(255 * a), contorno=10)
    cv.restore()


def selo_como_funciona(cv, a):
    if a <= 0:
        return
    rr = skia.RRect.MakeRectXY(skia.Rect(CX - 190, 150, CX + 190, 204), 27, 27)
    cv.drawRRect(rr, paint("#FFFFFF", int(28 * a)))
    texto(cv, "COMO FUNCIONA", CX, 190, F_BLACK, 32, OURO, int(255 * a))


def carimbo(cv, s, x, y, rot, t0, t, dur=1.9, tam=62):
    k = t - t0
    if k < 0 or k > dur:
        return
    from .cf_alongamento import lerp
    esc = lerp(1.9, 1.0, e_out(clamp(k / 0.16))); a = clamp(k / 0.08) * (1 - prog(k, dur - 0.35, dur))
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(esc, esc)
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 24, -tam, lw / 2 + 24, tam * 0.36), 12, 12)
    cv.drawRRect(rr, paint("#0B1824", int(160 * a))); cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 7))
    cv.drawString(s, -lw / 2, 0, f, paint(OURO, int(255 * a)))
    cv.restore()


def interface(cv, t, T, blocos, destaque, nota=""):
    """Legenda + identificação CFM (rodapé a partir de 3 s) + cartão final com a CTA e o aviãozinho.
    `nota`: linha extra no cartão final (ex.: atribuição de caso da literatura)."""
    t_cta = T["manda"] - 0.15
    if t < t_cta:
        legenda(cv, blocos, t, destaque)
    if 3.0 <= t < t_cta:
        a = prog(t, 3.0, 3.6)
        texto(cv, SIG, CX, 1585, F_SEMI, 27, "#FFFFFF", int(200 * a))
        texto(cv, DISC, CX, 1620, F_REG, 23, "#FFFFFF", int(150 * a))
    if t >= t_cta:
        a = prog(t, t_cta, t_cta + 0.35)
        cv.drawRect(skia.Rect(0, 0, W, H), paint(BG_OUT, int(175 * a)))
        legenda(cv, blocos, t, destaque, y_base=700, tam=92)
        aviao(cv, t, T["manda"] + 0.2)
        y1 = 1214 + (44 if nota else 0)
        rr = skia.RRect.MakeRectXY(skia.Rect(150, 1060, 930, y1), 28, 28)
        cv.drawRRect(rr, paint("#0B1824", int(230 * a))); cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 3))
        texto(cv, "Dr. Rafael Vargas · Médico ortopedista", CX, 1112, F_BLACK, 36, "#FFFFFF", int(255 * a))
        texto(cv, "CRM-SP 226103 · RQE 137901 · @rafaelvargasmd", CX, 1154, F_SEMI, 28, OURO, int(255 * a))
        texto(cv, DISC, CX, 1190, F_REG, 22, "#FFFFFF", int(170 * a))
        if nota:
            texto(cv, nota, CX, 1234, F_SEMI, 24, "#9CC9FF", int(230 * a))


def fazer_render(quadro, mapa_ancoras, sons, tempos_previa, respiro_cta=1.6):
    """Monta a função `render(ep, mp4, tmp, previa)` que `animado.render` chama.
    `sons(T)` -> [(t, nome, ganho)]; `tempos_previa(T)` -> tempos dos quadros de conferência."""
    def render(ep, mp4, tmp, previa=False):
        roteiro = "\n".join(ep["roteiro"])
        voz_bruta, palavras = _voz.narrar(roteiro, _voz.RITMO_COMO_FUNCIONA, os.path.join(tmp, "voz"))
        voz_c, pal, tirado = comprimir(voz_bruta, palavras, respiro_cta=respiro_cta)
        pal = alinhar(pal, roteiro)
        T = ancoras(pal, mapa_ancoras)
        print(f"{ep['id']}: silêncio cortado {tirado:.2f}s | duração final {T['total']:.2f}s")
        blocos = montar_blocos(pal)

        def quadro_t(cv, t):
            quadro(cv, t, T, blocos, ep)

        if previa:
            return _previas(quadro_t, tempos_previa(T), tmp, ep["id"]), T["total"]
        wav = os.path.join(tmp, f"{ep['id']}_mix.wav")
        som.gravar_wav(wav, som.mixar(voz_c, T["total"], sons(T), ganho_trilha=0.40))
        codificar(quadro_t, T["total"], wav, mp4)
        return mp4, T["total"]
    return render
