# -*- coding: utf-8 -*-
"""Som do piloto: trilha e efeitos SINTETIZADOS aqui mesmo (numpy).

Por que sintetizar em vez de baixar: a publicação é pela Graph API, que não deixa escolher
música da biblioteca do Instagram — o áudio tem de vir dentro do arquivo. Trilha de terceiro
traz licença para conferir peça a peça; som gerado aqui é original, sem licença nenhuma a
gerir, e roda igual na nuvem (GitHub Actions) sem depender de banco externo.
"""
import wave
import numpy as np

SR = 48000


def _env(n, a=0.005, r=0.2):
    """Envelope ataque/decaimento exponencial, em amostras."""
    t = np.arange(n) / SR
    att = np.clip(t / max(a, 1e-4), 0, 1)
    return att * np.exp(-t / max(r, 1e-4))


def _noise(n, seed):
    return np.random.default_rng(seed).standard_normal(n)


def _onepole_lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):          # curto o bastante para laço simples (efeitos < 1 s)
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    return y


# ----------------------------------------------------------------- efeitos
def whoosh(dur=0.55, seed=1):
    n = int(dur * SR); t = np.arange(n) / SR
    x = _noise(n, seed)
    # varredura de filtro: sobe e desce (sensação de passagem)
    fc = 400 + 3600 * np.sin(np.pi * t / dur) ** 2
    y = np.zeros(n); acc = 0.0
    for i in range(n):
        a = np.exp(-2 * np.pi * fc[i] / SR)
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    return y * np.sin(np.pi * t / dur) ** 1.5 * 0.9


def ping(seed=2):
    """Metal travando (anel do fixador encaixando)."""
    n = int(0.45 * SR); t = np.arange(n) / SR
    y = sum(np.sin(2 * np.pi * f * t) * g for f, g in ((1830, .5), (2710, .35), (4120, .22), (5960, .12)))
    y = y * _env(n, 0.001, 0.09)
    y[:int(0.004 * SR)] += _noise(int(0.004 * SR), seed) * 0.6
    return y * 0.55


def tick(seed=3):
    """Corte seco."""
    n = int(0.09 * SR); t = np.arange(n) / SR
    y = np.sin(2 * np.pi * 3100 * t) * _env(n, 0.0005, 0.012) + _noise(n, seed) * _env(n, 0.0002, 0.006) * 0.8
    return y * 0.8


def thump(seed=4):
    """Carimbo."""
    n = int(0.28 * SR); t = np.arange(n) / SR
    f = 95 * np.exp(-t * 9) + 45
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.001, 0.09)
    y += _noise(n, seed) * _env(n, 0.0005, 0.01) * 0.5
    return y * 0.95


def click(seed=5):
    """Uma volta da porca (um milímetro)."""
    n = int(0.035 * SR); t = np.arange(n) / SR
    y = np.sin(2 * np.pi * 1450 * t) * _env(n, 0.0003, 0.006) + _noise(n, seed) * _env(n, 0.0002, 0.003) * 0.4
    return y * 0.32


def shimmer():
    """Brilho do osso novo: arpejo agudo e macio."""
    notas = [1046.5, 1318.5, 1568.0, 2093.0, 2637.0]
    n = int(1.4 * SR); y = np.zeros(n)
    for k, f in enumerate(notas):
        ini = int(k * 0.07 * SR); m = n - ini; t = np.arange(m) / SR
        y[ini:] += np.sin(2 * np.pi * f * t) * _env(m, 0.01, 0.45) * (0.32 - 0.04 * k)
    return y * 0.7


def crackle(seed=6):
    """Endurecendo: grãos curtos rareando."""
    n = int(1.0 * SR); y = np.zeros(n); rng = np.random.default_rng(seed)
    for i in range(38):
        p = int((i / 38) ** 1.6 * (n - 2000)); m = int(rng.uniform(200, 900))
        y[p:p + m] += rng.standard_normal(m) * _env(m, 0.0002, 0.004) * rng.uniform(0.25, 0.7) * (1 - i / 45)
    return y * 0.55


def ding():
    n = int(1.8 * SR); t = np.arange(n) / SR
    y = sum(np.sin(2 * np.pi * f * t) * g for f, g in ((1318.5, .5), (2637, .18), (3951, .07)))
    return y * _env(n, 0.002, 0.55) * 0.55


def pop():
    n = int(0.09 * SR); t = np.arange(n) / SR
    f = 900 * np.exp(-t * 30) + 300
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.001, 0.03) * 0.45


SFX = {"whoosh": whoosh, "ping": ping, "tick": tick, "thump": thump, "click": click,
       "shimmer": shimmer, "crackle": crackle, "ding": ding, "pop": pop}


# ----------------------------------------------------------------- trilha
def trilha(dur, bpm=100):
    """Base eletrônica leve, original: kick suave, hat, baixo e pad em Lá menor (Am–F–C–G)."""
    n = int(dur * SR); t = np.arange(n) / SR
    beat = 60 / bpm; bar = 4 * beat
    out = np.zeros(n)
    acordes = [(220.0, 261.63, 329.63), (174.61, 220.0, 261.63), (130.81, 164.81, 196.0), (196.0, 246.94, 293.66)]
    raizes = [110.0, 87.31, 65.41, 98.0]
    # pad: senoides com leve desafinação, ataque lento por compasso
    for b in range(int(dur / bar) + 1):
        ini = int(b * bar * SR); fim = min(n, int((b + 1) * bar * SR))
        if ini >= n:
            break
        m = fim - ini; tt = np.arange(m) / SR
        env = np.clip(tt / 0.6, 0, 1) * np.clip((m / SR - tt) / 0.4, 0, 1)
        ac = acordes[b % 4]
        for f in ac:
            for det in (-0.6, 0.6):
                out[ini:fim] += np.sin(2 * np.pi * (f + det) * tt) * env * 0.045
        # baixo nos tempos 1 e 3
        for k in (0, 2):
            p = ini + int(k * beat * SR)
            if p < fim:
                mm = min(int(beat * 1.6 * SR), n - p); t2 = np.arange(mm) / SR
                out[p:p + mm] += np.sin(2 * np.pi * raizes[b % 4] * t2) * _env(mm, 0.01, 0.35) * 0.22
    # kick e hat
    for k in range(int(dur / beat) + 1):
        p = int(k * beat * SR)
        if p >= n:
            break
        if k % 2 == 0:
            mm = min(int(0.25 * SR), n - p); t2 = np.arange(mm) / SR
            f = 110 * np.exp(-t2 * 22) + 42
            out[p:p + mm] += np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(mm, 0.001, 0.11) * 0.38
        ph = p + int(beat / 2 * SR)
        if ph < n:
            mm = min(int(0.05 * SR), n - ph)
            h = _noise(mm, 100 + k); h = h - np.convolve(h, np.ones(6) / 6, "same")
            out[ph:ph + mm] += h * _env(mm, 0.0005, 0.012) * 0.10
    # entrada e saída suaves
    fade = np.clip(t / 0.8, 0, 1) * np.clip((dur - t) / 1.5, 0, 1)
    return out * fade


# ----------------------------------------------------------------- E/S e mixagem
def ler_wav(path):
    with wave.open(path, "rb") as w:
        sr, ch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    if ch == 2:
        data = data.reshape(-1, 2).mean(axis=1)
    assert sr == SR, f"esperava {SR} Hz, veio {sr}"
    return data


def gravar_wav(path, mono):
    est = np.clip(np.stack([mono, mono], axis=1), -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((est * 32767).astype(np.int16).tobytes())


def mixar(voz, dur, eventos, ganho_trilha=0.32):
    """voz: mono float; eventos: [(t, nome, ganho)]. Trilha abaixa sozinha quando a voz fala."""
    n = int(dur * SR)
    v = np.zeros(n); v[:min(n, len(voz))] = voz[:n]
    musica = trilha(dur) * ganho_trilha
    # ducking: envelope da voz (janela de 60 ms), suavizado
    win = int(0.06 * SR)
    envv = np.sqrt(np.convolve(v ** 2, np.ones(win) / win, "same"))
    alvo = np.where(envv > 0.02, 0.38, 1.0)
    duck = np.convolve(alvo, np.ones(int(0.25 * SR)) / int(0.25 * SR), "same")
    fx = np.zeros(n)
    for t0, nome, g in eventos:
        s = SFX[nome]()
        p = int(t0 * SR)
        if 0 <= p < n:
            m = min(len(s), n - p)
            fx[p:p + m] += s[:m] * g
    mix = v * 1.0 + musica * duck + fx * 0.7
    pico = np.max(np.abs(mix)) or 1.0
    return mix / pico * 0.89
