# -*- coding: utf-8 -*-
"""Formato CONVERSA — "Se o seu ___ pudesse responder" (piloto B aprovado em 18/10/2026).

O paciente reclama em balão de texto (dourado, à direita); o personagem responde em primeira
pessoa (balão claro, à esquerda), FALADO pela voz do canal — a palavra que está sendo dita
acende. O balão é a própria legenda: funciona sem som. Começa por um gancho escrito (que também
é a capa no perfil) e fecha com a CTA de envio dirigida a alguém específico + identificação CFM.

Totalmente guiado por dados — o episódio é um dict em `episodios_entretenimento.py`:
  {"id", "formato": "conversa", "icone": "fixador|gesso|muleta|pinos|osso", "personagem",
   "gancho": [linha1, linha2], "falas": [{"quem": "P"|"F", "texto"}...], "cta", "caption"}
"""
import math
import os

import numpy as np
import skia

from . import icones, som, voz
from .base import (BG_OUT, OURO, OURO_ESC, W, H, C, cartao_id, clamp, codificar, e_back, e_out, fundo_gradiente,
                   lerp, paint, previas, prog, quebrar, rodape_cfm, texto)

BAL_F, TXT_F = "#EEF3F8", "#13283A"
Y_TOPO_MSG, Y_BASE_MSG = 330, 1420          # área da conversa (acima da faixa do Instagram)
TAM_MSG = 56; LMAX = 760; ALT_LIN = 72; GAP_MSG = 30
T_GANCHO = 2.5                              # o gancho escrito fica sozinho na tela até aqui


def _validar(ep):
    falas = ep["falas"]
    assert ep.get("formato") == "conversa", ep.get("formato")
    assert ep.get("icone") in icones.ICONES, f"icone desconhecido: {ep.get('icone')}"
    assert len(ep["gancho"]) == 2, "gancho = 2 linhas"
    assert falas and falas[0]["quem"] == "P", "a conversa começa pelo paciente"
    assert all(f["quem"] in ("P", "F") for f in falas)
    assert any(f["quem"] == "F" for f in falas)
    assert ep["cta"].startswith(("Manda ", "Envia ")), "CTA de envio"


def _falas_com_voz(ep, tmp):
    out = {}
    for i, f in enumerate(ep["falas"]):
        if f["quem"] == "F":
            out[i] = f["texto"]
    out["cta"] = ep["cta"]
    res = {}
    for k, txt in out.items():
        v, pal = voz.narrar(txt, voz.RITMO_CONVERSA, tmp)
        ini = max(0.0, pal[0]["t"] - 0.04)                     # apara o silêncio inicial
        v = v[int(ini * som.SR):]; pal = [dict(q, t=q["t"] - ini) for q in pal]
        fim = pal[-1]["t"] + pal[-1]["d"]
        res[k] = {"audio": v[:int((fim + 0.12) * som.SR)], "pal": pal, "dur": fim + 0.12}
    return res


def _cronologia(ep, vz):
    t = T_GANCHO; msgs, ev = [], []
    for i, f in enumerate(ep["falas"]):
        if f["quem"] == "P":
            msgs.append({"q": "P", "txt": f["texto"], "t": t}); ev.append((t, "pop", 0.8))
            t += clamp(0.45 + 0.036 * len(f["texto"]), 0.95, 1.6)      # tempo de leitura
        else:
            d = vz[i]
            msgs.append({"q": "F", "txt": f["texto"], "t_dig": t, "t": t + 0.75, "pal": d["pal"], "voz": d["audio"]})
            ev += [(t + 0.1 + k * 0.15, "click", 0.5) for k in range(4)] + [(t + 0.72, "whoosh", 0.25)]
            t = t + 0.75 + d["dur"] + 0.32
    cta = {"t": t + 0.25, "pal": vz["cta"]["pal"], "voz": vz["cta"]["audio"]}
    ev += [(cta["t"] - 0.1, "whoosh", 0.55), (cta["t"] + vz["cta"]["dur"] + 0.2, "ding", 0.55)]
    return msgs, cta, ev, cta["t"] + vz["cta"]["dur"] + 2.0


def _altura(m):
    linhas, _ = quebrar(m["txt"].split(), "semi", TAM_MSG, LMAX)
    return 46 + len(linhas) * ALT_LIN + 16


def _balao(cv, m, y, t):
    pal = m["txt"].split()
    linhas, esp = quebrar(pal, "semi", TAM_MSG, LMAX)
    larg = max(sum(w for _, _, w in ln) + esp * (len(ln) - 1) for ln in linhas) + 64
    alt = _altura(m); k = t - m["t"]
    esc = e_back(clamp(k / 0.32)); a = clamp(k / 0.12)
    dir_ = m["q"] == "P"
    x0 = (W - 70 - larg) if dir_ else 70; top = y - alt
    cv.save()
    ox = x0 + (larg if dir_ else 0); oy = y
    cv.translate(ox, oy); cv.scale(esc, esc); cv.translate(-ox, -oy)
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, top, x0 + larg, y), 34, 34)
    cv.drawRRect(rr, paint("#000000", int(70 * a), blur=12))
    cv.drawRRect(rr, paint(OURO if dir_ else BAL_F, int(255 * a)))
    cauda = skia.Path()
    if dir_:
        cauda.moveTo(x0 + larg - 30, y - 4); cauda.lineTo(x0 + larg + 16, y + 6); cauda.lineTo(x0 + larg - 6, y - 30)
    else:
        cauda.moveTo(x0 + 30, y - 4); cauda.lineTo(x0 - 16, y + 6); cauda.lineTo(x0 + 6, y - 30)
    cauda.close(); cv.drawPath(cauda, paint(OURO if dir_ else BAL_F, int(255 * a)))
    yy = top + 78
    for ln in linhas:
        x = x0 + 32
        for i, w, ww in ln:
            if dir_:
                cor, aa, papel = "#1A1206", 255, "semi"
            else:
                p = m["pal"][i] if i < len(m["pal"]) else None
                dita = p is not None and t >= m["t"] + p["t"] - 0.03
                falando = p is not None and m["t"] + p["t"] - 0.03 <= t <= m["t"] + p["t"] + p["d"] + 0.06
                cor = OURO_ESC if falando else TXT_F; aa = 255 if dita else 95
                papel = "bold" if falando else "semi"
            texto(cv, w, x, yy, papel, TAM_MSG, cor, int(aa * a), centro=False)
            x += ww + esp
        yy += ALT_LIN
    cv.restore()


def _digitando(cv, y, t, t0, t1):
    if not (t0 <= t < t1):
        return
    a = clamp((t - t0) / 0.12)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(70, y - 96, 250, y), 34, 34), paint(BAL_F, int(255 * a)))
    for k in range(3):
        dy = -10 * max(0.0, math.sin((t - t0) * 9 - k * 0.9))
        cv.drawCircle(120 + k * 40, y - 48 + dy, 11, paint("#7D8FA3", int(255 * a)))


def _alvo_rolagem(t, msgs):
    y = Y_TOPO_MSG + 40
    for m in msgs:
        if m["q"] == "F" and m["t_dig"] <= t < m["t"]:
            y += 100 + GAP_MSG; break
        if t < m["t"]:
            break
        y += _altura(m) + GAP_MSG
    return max(0.0, y - GAP_MSG - Y_BASE_MSG)


def _rolagem(t, msgs):
    marcos = sorted({m["t"] for m in msgs} | {m["t_dig"] for m in msgs if m["q"] == "F"})
    ant = [x for x in marcos if x <= t]
    if not ant:
        return 0.0
    te = ant[-1]
    return lerp(_alvo_rolagem(te - 1e-3, msgs), _alvo_rolagem(te, msgs), e_out(prog(t, te, te + 0.4)))


RNG = np.random.default_rng(11)
PADRAO = [(RNG.uniform(0, W), RNG.uniform(0, H), RNG.uniform(10, 26)) for _ in range(26)]


def _quadro_fn(ep, msgs, cta):
    icone = icones.ICONES[ep["icone"]]
    destaque_cta = {w.strip(".,!?").lower() for w in ep.get("cta_destaque", ["manda"])}

    def quadro(cv, t):
        fundo_gradiente(cv)
        for x, y, r in PADRAO:                                   # textura discreta
            yy = (y - t * 10) % H
            cv.drawArc(skia.Rect(x - r * 2, yy - r * 0.5, x + r * 2, yy + r * 0.5), 0, 360, False,
                       paint("#BFE3FF", 22, "stroke", 2))
        # mensagens: começam no topo e rolam quando passam do fim da área
        cv.save(); cv.clipRect(skia.Rect(0, 292, W, Y_BASE_MSG + 40))
        rol = _rolagem(t, msgs); y = Y_TOPO_MSG + 40
        for m in msgs:
            h = _altura(m)
            if m["q"] == "F" and m["t_dig"] <= t < m["t"]:
                _digitando(cv, y + 100 - rol, t, m["t_dig"], m["t"]); break
            if t < m["t"]:
                break
            _balao(cv, m, y + h - rol, t); y += h + GAP_MSG
        cv.restore()
        # cabeçalho
        a_h = prog(t, T_GANCHO - 0.3, T_GANCHO + 0.1)
        if a_h > 0:
            cv.drawRect(skia.Rect(0, 150, W, 290), paint("#0B1824", int(235 * a_h)))
            cv.drawCircle(150, 220, 46, paint("#21445A", int(255 * a_h)))
            icone(cv, 150, 222, 0.82, a_h, 10 * math.sin(t * 6) if t >= cta["t"] else 0.0)
            texto(cv, ep["personagem"], 222, 214, "black", 44, "#FFFFFF", int(255 * a_h), centro=False)
            digit = any(m["q"] == "F" and m["t_dig"] <= t < m["t"] for m in msgs)
            fala = any(m["q"] == "F" and m["t"] <= t < m["t"] + m["pal"][-1]["t"] + m["pal"][-1]["d"] for m in msgs)
            status = "digitando…" if digit else ("falando…" if fala else "online")
            texto(cv, status, 224, 258, "semi", 30, OURO if status != "online" else "#7FD1A8", int(255 * a_h), centro=False)
        # gancho escrito (primeiro quadro = capa)
        if t < T_GANCHO + 0.1:
            a = 1 - prog(t, T_GANCHO - 0.4, T_GANCHO + 0.1)
            cv.drawRect(skia.Rect(0, 0, W, H), paint(BG_OUT, int(150 * a)))
            esc = 1 + 0.03 * math.sin(t * 5)
            cv.save(); cv.translate(W / 2, 760); cv.scale(esc, esc)
            icone(cv, 0, -230, 2.6, a, 8 * math.sin(t * 4))
            texto(cv, ep["gancho"][0], 0, 0, "black", 86, "#FFFFFF", int(255 * a), contorno=10)
            texto(cv, ep["gancho"][1], 0, 100, "black", 86, OURO, int(255 * a), contorno=10)
            cv.restore()
        rodape_cfm(cv, t, cta["t"] - 0.15)
        # CTA
        if t >= cta["t"] - 0.15:
            a = prog(t, cta["t"] - 0.15, cta["t"] + 0.3)
            cv.drawRect(skia.Rect(0, 0, W, H), paint(BG_OUT, int(248 * a)))
            icone(cv, W / 2, 470, 2.4, a, 10 * math.sin(t * 6))
            pal = ep["cta"].split(); linhas, esp = quebrar([w.upper() for w in pal], "black", 88, 900)
            yy = 720
            for ln in linhas:
                tot = sum(w for _, _, w in ln) + esp * (len(ln) - 1); x = W / 2 - tot / 2
                for i, w, ww in ln:
                    p = cta["pal"][i] if i < len(cta["pal"]) else None
                    dita = p is not None and t >= cta["t"] + p["t"] - 0.03
                    falando = p is not None and cta["t"] + p["t"] - 0.03 <= t <= cta["t"] + p["t"] + p["d"] + 0.06
                    cor = OURO if (falando or w.strip(".,!?").lower() in destaque_cta) else "#FFFFFF"
                    texto(cv, w, x, yy, "black", 88, cor, int((255 if dita else 100) * a), centro=False, contorno=10)
                    x += ww + esp
                yy += 104
            cartao_id(cv, a)
    return quadro


def render(ep, mp4, tmp, previa=False):
    _validar(ep)
    vz = _falas_com_voz(ep, os.path.join(tmp, "voz"))
    msgs, cta, ev, total = _cronologia(ep, vz)
    print(f"{ep['id']}: duração {total:.2f}s | {sum(1 for m in msgs if m['q'] == 'F')} falas do personagem")
    quadro = _quadro_fn(ep, msgs, cta)
    if previa:
        tempos = [0.5, T_GANCHO + 0.4] + [m["t"] + 1.0 for m in msgs if m["q"] == "F"] + [cta["t"] + 1.6]
        return previas(quadro, tempos, tmp, ep["id"]), total
    n = int(total * som.SR); trilha_voz = np.zeros(n)
    for m in msgs + [cta]:
        if "voz" in m:
            p = int(m["t"] * som.SR); v = m["voz"]; trilha_voz[p:p + len(v)] += v[:max(0, n - p)]
    wav = os.path.join(tmp, f"{ep['id']}_mix.wav")
    som.gravar_wav(wav, som.mixar(trilha_voz, total, ev, ganho_trilha=0.40))
    codificar(quadro, total, wav, mp4)
    return mp4, total
