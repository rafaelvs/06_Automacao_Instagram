# -*- coding: utf-8 -*-
"""Narração com o TEMPO DE CADA PALAVRA (edge-tts, boundary="WordBoundary").

É o tempo das palavras que comanda a animação e a legenda: o corte acontece quando a voz diz
"cortar", a palavra falada acende na tela. Voz do canal: Antonio. Ritmo e tom APROVADOS pelo
Rafael em 18/10/2026 (pilotos A e B): +10% na narração do COMO FUNCIONA, +8% na CONVERSA,
tom +0Hz. Mudar qualquer um destes exige piloto (regra de 30/08/2026; `checar_voz.py` vigia).
"""
import asyncio
import hashlib
import json
import os
import shutil
import subprocess

import edge_tts
import numpy as np

from . import som

VOZ = "pt-BR-AntonioNeural"
RITMO_COMO_FUNCIONA = "+10%"
RITMO_CONVERSA = "+8%"
TOM = "+0Hz"

# Mesma masterização do motor (gerar_reel_voz.py), SEM o silenceremove do começo: cortar
# silêncio deslocaria todos os tempos de palavra.
VOICE_CHAIN = ("highpass=f=85,"
 "equalizer=f=300:t=q:w=1.2:g=-3,equalizer=f=180:t=q:w=1.5:g=2,"
 "equalizer=f=4000:t=q:w=1.6:g=2,equalizer=f=6500:t=q:w=2.0:g=-2,"
 "deesser=i=0.5:m=0.5:f=0.5,"
 "acompressor=threshold=-18dB:ratio=3:attack=15:release=120:makeup=4,"
 "asoftclip=type=tanh,alimiter=limit=-1dB,"
 "loudnorm=I=-16:TP=-1.5:LRA=11,aformat=sample_rates=48000:channel_layouts=stereo")


def ffmpeg():
    """ffmpeg do sistema (runner Linux) ou o embutido do imageio-ffmpeg (Windows)."""
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


async def _tts(texto, rate, pitch):
    com = edge_tts.Communicate(texto, VOZ, rate=rate, pitch=pitch, boundary="WordBoundary")
    audio, palavras = bytearray(), []
    async for ch in com.stream():
        if ch["type"] == "audio":
            audio += ch["data"]
        elif ch["type"] == "WordBoundary":
            palavras.append({"t": ch["offset"] / 1e7, "d": ch["duration"] / 1e7, "w": ch["text"]})
    return bytes(audio), palavras


def narrar(texto, rate, tmp_dir, pitch=TOM, tentativas=4):
    """-> (audio mono float32 48 kHz, [{t, d, w}]). Cacheia por (voz, ritmo, tom, texto) em tmp_dir.
    Falha ALTO se o serviço não devolver áudio ou palavras (edge-tts muda de token às vezes)."""
    os.makedirs(tmp_dir, exist_ok=True)
    chave = hashlib.sha1(f"{VOZ}|{rate}|{pitch}|{texto}".encode("utf-8")).hexdigest()[:16]
    wav = os.path.join(tmp_dir, f"{chave}.wav"); meta = os.path.join(tmp_dir, f"{chave}.json")
    if not (os.path.exists(wav) and os.path.exists(meta)):
        erro = None
        for k in range(tentativas):
            try:
                audio, pal = asyncio.run(_tts(texto, rate, pitch))
                if audio and pal:
                    break
                erro = RuntimeError("edge-tts devolveu áudio ou palavras vazios")
            except Exception as e:                                   # noqa: BLE001 — 503 intermitente
                erro = e
            import time; time.sleep(3 * (k + 1))
        else:
            raise SystemExit(f"ERRO: edge-tts falhou {tentativas}x para {texto[:50]!r}: {erro}")
        mp3 = os.path.join(tmp_dir, f"{chave}.mp3")
        open(mp3, "wb").write(audio)
        subprocess.run([ffmpeg(), "-y", "-loglevel", "error", "-i", mp3, "-af", VOICE_CHAIN, wav], check=True)
        json.dump(pal, open(meta, "w", encoding="utf-8"), ensure_ascii=False)
    return som.ler_wav(wav), json.load(open(meta, encoding="utf-8"))
