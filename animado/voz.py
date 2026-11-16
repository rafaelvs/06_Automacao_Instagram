# -*- coding: utf-8 -*-
"""Narração com o TEMPO DE CADA PALAVRA.

É o tempo das palavras que comanda a animação e a legenda: o corte acontece quando a voz diz
"cortar", a palavra falada acende na tela.

Duas engines, escolhidas por UMA constante (`ENGINE`):
- "gemini" (vigente a partir do piloto da voz F): Gemini-TTS, voz Sadaltager, modelo
  gemini-2.5-flash-tts, com prompt de estilo. Escolhida às cegas pelo Rafael em 16/11/2026 entre
  6 vozes. O Gemini NÃO devolve tempo por palavra e NÃO é determinístico (cada chamada soa um
  pouco diferente, ±5% de duração): o tempo sai do próprio áudio (animado/alinhar.py, faster-whisper
  casado ao texto conhecido) e a tomada aceita fica num CACHE VERSIONADO no repo
  (animado/voz_cache/), para que re-render do mesmo episódio dê exatamente o mesmo som.
- "edge": edge-tts pt-BR-AntonioNeural com WordBoundary — a voz de 18/10/2026 (corpo de `_tts`
  idêntico ao de 18/10). Voltar a ela NÃO é só trocar a constante: o fingerprint de `checar_voz.py`
  cobre também a engine e as funções da gemini, então a volta exige `--registrar` com evidência
  ("volta à voz Antonio de 18/10, mesma voz já aprovada") e, como `voz.py`/`alinhar.py` entram no
  hash do motor, re-render da fila (checar_entretenimento acusa "o motor mudou").

Ritmo e tom APROVADOS pelo Rafael em 18/10/2026 (pilotos A e B): +10% na narração do COMO FUNCIONA,
+8% na CONVERSA, tom +0Hz. Os chamadores (cf_*.py, conversa.py) continuam passando esses ritmos; na
engine gemini eles viram `speakingRate` por TAXA_GEMINI (medição de 16/11/2026). Mudar qualquer um
destes exige piloto (regra de 30/08/2026; `checar_voz.py` vigia).
"""
import asyncio
import base64
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import time
import wave

import numpy as np

try:
    import edge_tts
except ImportError:                     # só a engine "edge" precisa; a gemini roda sem o pacote
    edge_tts = None

from . import som

ENGINE = "gemini"

VOZ = "pt-BR-AntonioNeural"
RITMO_COMO_FUNCIONA = "+10%"
RITMO_CONVERSA = "+8%"
TOM = "+0Hz"

VOZ_GEMINI = "Sadaltager"
MODELO_GEMINI = "gemini-2.5-flash-tts"
PROMPT_GEMINI = ("Narre em português do Brasil, como um médico ortopedista explicando com calma e clareza "
                 "para pais num vídeo curto de redes sociais: tom acolhedor, natural, ritmo levemente "
                 "animado, sem exagero.")
# ritmo que o chamador passa -> speakingRate. Medição de 16/11/2026 contra a duração do Antonio:
# CONVERSA a 1,00 ficou entre -1% e -5% do Antonio a +8%; COMO FUNCIONA a 1,05 é o meio-termo
# (perna_curta/ponta_pes ~5% mais curtos, regra_milimetro/pe_torto ~5% mais longos). 1,10 fixo
# cortava perna_curta em 7,6%.
TAXA_GEMINI = {"+10%": 1.05, "+8%": 1.00}
TOMADAS_GEMINI = 3          # amostras do Gemini por texto até achar uma que a voz disse direito
URL_GEMINI = "https://texttospeech.googleapis.com/v1/text:synthesize"
PROJETO_COTA_PADRAO = "debb-b4b6d"   # x-goog-user-project quando a credencial é um token de usuário

CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voz_cache")
CACHE_VERSAO = 2            # 2: sha256 + nº de amostras do PCM no JSON, conferidos na leitura
FADE_FINAL = 0.015          # s; 1/3 das tomadas cruas do Gemini terminam no meio do fonema (-3 a -20
                            # dB no último quadro): sem rampa, o fim do áudio estala no vídeo

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


def _masterizar(entrada, wav):
    subprocess.run([ffmpeg(), "-y", "-loglevel", "error", "-i", entrada, "-af", VOICE_CHAIN, wav], check=True)


async def _tts(texto, rate, pitch):
    com = edge_tts.Communicate(texto, VOZ, rate=rate, pitch=pitch, boundary="WordBoundary")
    audio, palavras = bytearray(), []
    async for ch in com.stream():
        if ch["type"] == "audio":
            audio += ch["data"]
        elif ch["type"] == "WordBoundary":
            palavras.append({"t": ch["offset"] / 1e7, "d": ch["duration"] / 1e7, "w": ch["text"]})
    return bytes(audio), palavras


def _norm(w):
    return re.sub(r"[^\w-]", "", w.lower())


def _expandir(pal):
    """O edge-tts às vezes junta palavras num boundary só ('2 a', '3 dedos'): reparte em uma
    entrada por palavra, dividindo o tempo pelo número de letras."""
    out = []
    for p in pal:
        ws = p["w"].split()
        if len(ws) <= 1:
            out.append(p); continue
        tot = sum(len(w) for w in ws); t = p["t"]
        for w in ws:
            d = p["d"] * len(w) / tot
            out.append({"t": t, "d": d, "w": w}); t += d
    return out


SOBREPOSICAO_MAX = 0.35     # s que o fim de uma palavra pode passar do início da seguinte
PALAVRA_MAX = 4.0           # s; uma palavra "durando" mais que isso é tempo interpolado sobre buraco


def problemas_de_tempo(pal, duracao=None):
    """Tempos que quebrariam legenda/animação: fora de ordem, negativos, além do fim do áudio,
    sobreposição absurda ou palavra longa demais. -> lista de motivos (vazia = ok)."""
    out = []
    for i, p in enumerate(pal):
        t, d = p["t"], p["d"]
        if not (np.isfinite(t) and np.isfinite(d)) or t < 0 or d < 0:
            out.append(f"palavra {i} ({p['w']!r}) com tempo inválido t={t} d={d}")
        if d > PALAVRA_MAX:
            out.append(f"palavra {i} ({p['w']!r}) dura {d:.2f}s > {PALAVRA_MAX}s")
        if i and t < pal[i - 1]["t"]:
            out.append(f"palavra {i} ({p['w']!r}) começa antes da anterior ({t:.3f} < {pal[i - 1]['t']:.3f})")
        if i and pal[i - 1]["t"] + pal[i - 1]["d"] - t > SOBREPOSICAO_MAX:
            out.append(f"palavras {i - 1}/{i} sobrepostas em "
                       f"{pal[i - 1]['t'] + pal[i - 1]['d'] - t:.2f}s > {SOBREPOSICAO_MAX}s")
        if duracao is not None and t + d > duracao + 0.25:
            out.append(f"palavra {i} ({p['w']!r}) termina em {t + d:.2f}s, depois do fim do áudio ({duracao:.2f}s)")
    return out


def conferir_palavras(texto, pal, duracao=None):
    """As palavras da voz têm de ser EXATAMENTE as do texto, na ordem (a legenda acende a palavra
    pelo índice). Auditoria 19/10: no cv_muleta o boundary '2 a' deixou as 2 últimas palavras
    apagadas e o render saiu verde. Também pega narração truncada (o stream fecha sem erro).
    16/11/2026: na engine gemini as palavras vêm do texto por construção (alinhador), então o que
    pode quebrar são os TEMPOS — conferidos aqui também (monotônicos, dentro do áudio, sem
    sobreposição absurda)."""
    a = [_norm(w) for w in texto.split()]
    b = [_norm(p["w"]) for p in pal]
    if a != b:
        i = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), min(len(a), len(b)))
        raise SystemExit(f"ERRO: palavras da voz não batem com o texto (posição {i}: texto={a[i:i + 3]} "
                         f"voz={b[i:i + 3]}; {len(a)} x {len(b)}) — vídeo sairia com legenda dessincronizada.")
    probs = problemas_de_tempo(pal, duracao)
    if probs:
        raise SystemExit("ERRO: tempos das palavras da voz inválidos — legenda sairia dessincronizada:\n  "
                         + "\n  ".join(probs[:8]))


# ---------------------------------------------------------------------------------------------
# engine gemini
# ---------------------------------------------------------------------------------------------

def _credencial_google():
    """-> (token, projeto_de_cota | None). Ordem:
    1. GCP_TTS_TOKEN (token OAuth já pronto, ex.: `gcloud auth print-access-token` numa máquina de
       desenvolvimento) — cota em GCP_QUOTA_PROJECT ou no projeto padrão;
    2. GOOGLE_APPLICATION_CREDENTIALS apontando um JSON de service account (no Actions: secret
       GCP_TTS_SA_JSON gravado em arquivo temporário) — cota no próprio projeto da conta, ou em
       GCP_QUOTA_PROJECT se definido.
    Sem nenhum dos dois: falha ALTO dizendo o que falta."""
    tok = os.environ.get("GCP_TTS_TOKEN", "").strip()
    if tok:
        return tok, os.environ.get("GCP_QUOTA_PROJECT", PROJETO_COTA_PADRAO)
    cam = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "").strip()
    if cam:
        if not os.path.isfile(cam) or os.path.getsize(cam) == 0:
            raise SystemExit(f"ERRO: GOOGLE_APPLICATION_CREDENTIALS={cam!r} não existe ou está vazio "
                             f"(o secret GCP_TTS_SA_JSON foi cadastrado no repositório?).")
        try:
            from google.auth.transport.requests import Request
            from google.oauth2 import service_account
        except ImportError as e:
            raise SystemExit(f"ERRO: falta o pacote google-auth para usar a service account ({e}).")
        try:
            cred = service_account.Credentials.from_service_account_file(
                cam, scopes=["https://www.googleapis.com/auth/cloud-platform"])
            cred.refresh(Request())
        except Exception as e:                                       # noqa: BLE001
            raise SystemExit(f"ERRO: a service account de {cam!r} não autenticou no Google: {e}")
        return cred.token, os.environ.get("GCP_QUOTA_PROJECT") or None
    raise SystemExit(
        "ERRO: a voz (Gemini-TTS) precisa de credencial do Google e o texto NÃO está no cache "
        "animado/voz_cache/. Defina GOOGLE_APPLICATION_CREDENTIALS (JSON de service account; no "
        "GitHub Actions, o secret GCP_TTS_SA_JSON) ou GCP_TTS_TOKEN (token OAuth pronto). "
        "Nada foi renderizado.")


def _gemini_tts(texto, taxa, credencial, tentativas=5):
    """Uma amostra do Gemini-TTS -> bytes WAV (LINEAR16, 48 kHz). Retentativa com espera crescente
    em erro de rede, 429 e 5xx (medição 16/11: uma chamada caiu com RemoteDisconnected; cada uma
    leva 18-29 s). 400/401/403 falham na hora: credencial ou pedido errado não melhora esperando."""
    import requests
    token, cota = credencial
    cab = {"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=utf-8"}
    if cota:
        cab["x-goog-user-project"] = cota
    corpo = {"input": {"text": texto, "prompt": PROMPT_GEMINI},
             "voice": {"languageCode": "pt-BR", "name": VOZ_GEMINI, "modelName": MODELO_GEMINI},
             "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": 48000, "speakingRate": taxa}}
    erro = None
    for k in range(tentativas):
        try:
            r = requests.post(URL_GEMINI, headers=cab, json=corpo, timeout=180)
            if r.status_code == 200:
                audio = base64.b64decode(r.json().get("audioContent", ""))
                if len(audio) > 48000:                               # > ~0,5 s de PCM
                    return audio
                erro = RuntimeError(f"Gemini-TTS devolveu áudio vazio/curto ({len(audio)} bytes)")
            elif r.status_code in (400, 401, 403, 404):
                raise SystemExit(f"ERRO: Gemini-TTS recusou o pedido (HTTP {r.status_code}): {r.text[:300]}")
            else:
                erro = RuntimeError(f"HTTP {r.status_code}: {r.text[:200]}")
        # revisão 16/11: conexão que cai no meio do corpo (~4 MB de base64) é ChunkedEncodingError e
        # um 200 com HTML de proxy é ValueError (JSON/base64) — transitórios, merecem nova tentativa
        except (requests.RequestException, ValueError) as e:
            erro = e
        if k == tentativas - 1:
            break                                                    # não dorme depois da última
        espera = 5 * 2 ** k
        print(f"  [voz] Gemini-TTS falhou ({erro}); nova tentativa em {espera}s", flush=True)
        time.sleep(espera)
    raise SystemExit(f"ERRO: Gemini-TTS falhou {tentativas}x para {texto[:50]!r}: {erro}")


def _validar_audio(audio, texto):
    """Áudio não vazio, não mudo e com duração plausível para o número de palavras."""
    n = len(texto.split())
    dur = len(audio) / som.SR
    if dur < 1.0:
        return [f"áudio curto demais ({dur:.2f}s)"]
    out = []
    if float(np.sqrt(np.mean(audio ** 2))) < 0.01:
        out.append("áudio praticamente mudo")
    spp = dur / max(n, 1)                       # Antonio/Sadaltager medidos: ~0,33-0,45 s por palavra
    if not 0.18 <= spp <= 0.9:
        out.append(f"duração implausível: {dur:.1f}s para {n} palavras ({spp:.2f} s/palavra)")
    return out


def chave_cache(texto, taxa):
    return hashlib.sha256(f"gemini|{VOZ_GEMINI}|{MODELO_GEMINI}|{PROMPT_GEMINI}|{taxa}|{VOICE_CHAIN}|{texto}"
                          .encode("utf-8")).hexdigest()[:24]


def _pcm_flac(flac, wav):
    """FLAC -> WAV PCM 16 bits; -> (nº de amostras, sha256 do PCM). `-xerror`: o ffmpeg sai com
    código 0 mesmo com 'decode_frame() failed' (revisão 16/11: FLAC com 300 bytes trocados foi
    aceito com 787 mil amostras diferentes e os tempos deixaram de bater com o som)."""
    subprocess.run([ffmpeg(), "-y", "-loglevel", "error", "-xerror", "-i", flac, "-c:a", "pcm_s16le", wav],
                   check=True)
    with wave.open(wav) as f:
        n, pcm = f.getnframes() * f.getnchannels(), f.readframes(f.getnframes())
    return n, hashlib.sha256(pcm).hexdigest()


def _ler_cache(chave, texto, tmp_dir):
    flac = os.path.join(CACHE_DIR, f"{chave}.flac"); meta = os.path.join(CACHE_DIR, f"{chave}.json")
    if not (os.path.isfile(flac) and os.path.isfile(meta)):
        return None
    m = json.load(open(meta, encoding="utf-8"))
    if m.get("texto") != texto or m.get("chave") != chave:
        raise SystemExit(f"ERRO: cache de voz {chave} não corresponde ao texto pedido (arquivo trocado?).")
    if m.get("versao") != CACHE_VERSAO:
        raise SystemExit(f"ERRO: cache de voz {chave} é da versão {m.get('versao')!r}, o código espera "
                         f"{CACHE_VERSAO} — regrave a entrada (re-alinhar o áudio) antes de renderizar.")
    wav = os.path.join(tmp_dir, f"{chave}.wav")
    try:
        n, sha = _pcm_flac(flac, wav)
    except subprocess.CalledProcessError as e:
        raise SystemExit(f"ERRO: FLAC do cache de voz {chave} não decodifica ({e}) — arquivo corrompido.")
    if (n, sha) != (m.get("amostras"), m.get("pcm_sha256")):
        raise SystemExit(f"ERRO: áudio do cache de voz {chave} não confere com o JSON (amostras {n} x "
                         f"{m.get('amostras')}, sha256 {sha[:12]} x {str(m.get('pcm_sha256'))[:12]}) — "
                         f"arquivo corrompido ou trocado; os tempos das palavras não valeriam para ele.")
    return som.ler_wav(wav), [{"t": p["t"], "d": p["d"], "w": p["w"]} for p in m["palavras"]]


def _gravar_cache(chave, wav, meta, tmp_dir):
    """FLAC mono 16 bits/48 kHz (sem perda: o re-render toca exatamente o mesmo som) + JSON com o
    sha256 do PCM DECODIFICADO do próprio FLAC. Os arquivos parciais ficam em tmp_dir (nunca na
    pasta versionada: o commit do cache faz `git add` da pasta inteira)."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    flac = os.path.join(CACHE_DIR, f"{chave}.flac"); caminho = os.path.join(CACHE_DIR, f"{chave}.json")
    flac_p = os.path.join(tmp_dir, f"{chave}.parcial.flac"); json_p = os.path.join(tmp_dir, f"{chave}.parcial.json")
    subprocess.run([ffmpeg(), "-y", "-loglevel", "error", "-i", wav, "-ac", "1", "-c:a", "flac",
                    "-compression_level", "8", flac_p], check=True)
    n, sha = _pcm_flac(flac_p, os.path.join(tmp_dir, f"{chave}.conferencia.wav"))
    meta = dict(meta, versao=CACHE_VERSAO, amostras=n, pcm_sha256=sha)
    with open(json_p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
        f.write("\n")
    shutil.move(flac_p, flac)                       # áudio primeiro: json sem áudio = cache incompleto
    shutil.move(json_p, caminho)


def _arrematar(audio):
    """Rampa de FADE_FINAL s no fim (a tomada pode acabar no meio do fonema)."""
    k = min(int(FADE_FINAL * som.SR), len(audio))
    if k:
        audio = audio.copy()
        audio[-k:] *= np.cos(np.linspace(0, np.pi / 2, k)).astype(audio.dtype)
    return audio


def _narrar_gemini(texto, rate, tmp_dir, pitch):
    from . import alinhar
    if rate not in TAXA_GEMINI:
        raise SystemExit(f"ERRO: ritmo {rate!r} sem taxa aprovada para o Gemini (TAXA_GEMINI={TAXA_GEMINI}).")
    if pitch != TOM:
        raise SystemExit(f"ERRO: o Gemini-TTS não aceita tom; só o aprovado {TOM!r} (veio {pitch!r}).")
    taxa = TAXA_GEMINI[rate]
    chave = chave_cache(texto, taxa)
    hit = _ler_cache(chave, texto, tmp_dir)
    if hit is not None:
        print(f"  [voz] cache: {chave} (sem rede, sem whisper)", flush=True)
        return hit
    credencial = _credencial_google()
    tomadas, melhor = [], None
    for k in range(TOMADAS_GEMINI):
        bruto = os.path.join(tmp_dir, f"{chave}_t{k}.bruto.wav")
        wav = os.path.join(tmp_dir, f"{chave}_t{k}.wav")
        t0 = time.time()
        open(bruto, "wb").write(_gemini_tts(texto, taxa, credencial))
        _masterizar(bruto, wav)
        audio = som.ler_wav(wav)
        probs = _validar_audio(audio, texto)
        res = None
        if not probs:
            res = alinhar.alinhar(wav, texto, cpu_threads=os.cpu_count() or 4)
            probs = alinhar.problemas(res, texto) + problemas_de_tempo(res["palavras"], len(audio) / som.SR)
        resumo = {"tomada": k, "dur": round(len(audio) / som.SR, 2), "problemas": probs}
        if res is not None:
            resumo.update(fracao=round(res["fracao"], 3), buraco=res["buraco"],
                          inseridas=[x["w"] for x in res["inseridas"]], omitidas=[x["w"] for x in res["omitidas"]],
                          trocadas=[f"{x['w']}>{x['por']}" for x in res.get("trocadas", [])])
        tomadas.append(resumo)
        print(f"  [voz] tomada {k + 1}/{TOMADAS_GEMINI}: {resumo} ({time.time() - t0:.0f}s)", flush=True)
        if not probs:
            rel = len(alinhar.divergencias_relevantes(res))
            nota = (rel, len(res["inseridas"]) + len(res["omitidas"]) + len(res.get("trocadas", [])),
                    -res["fracao"])
            if melhor is None or nota < melhor[0]:
                melhor = (nota, k, wav, res)
            if rel == 0:
                break                                 # tomada limpa: não gasta outra chamada
    if melhor is None:
        raise SystemExit(f"ERRO: nenhuma das {TOMADAS_GEMINI} tomadas do Gemini-TTS passou na conferência "
                         f"(a voz não disse o texto ou o alinhamento não sustenta a legenda): {tomadas}")
    _, k, wav, res = melhor
    if alinhar.divergencias_relevantes(res):
        print(f"::warning::voz {chave}: a tomada aceita tem palavra a mais/a menos na fala "
              f"{alinhar.divergencias_relevantes(res)} — OUVIR antes de aprovar.", flush=True)
    meta = {"versao": CACHE_VERSAO, "chave": chave, "engine": "gemini", "voz": VOZ_GEMINI,
            "modelo": MODELO_GEMINI, "prompt": PROMPT_GEMINI, "ritmo": rate, "taxa": taxa,
            "gerado_em": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            "texto": texto, "duracao": round(res["duracao"], 3),
            "alinhamento": {"modelo_whisper": alinhar.MODELO, "fracao": round(res["fracao"], 4),
                            "buraco": res["buraco"], "inseridas": res["inseridas"], "omitidas": res["omitidas"],
                            "trocadas": res.get("trocadas", []), "inseridas_pontas": res.get("inseridas_pontas", []),
                            "tomada_aceita": k, "tomadas": tomadas},
            "palavras": [{"t": p["t"], "d": p["d"], "w": p["w"], "casada": p["casada"]} for p in res["palavras"]]}
    _gravar_cache(chave, wav, meta, tmp_dir)
    # lê de volta DO CACHE: o 1º render e os seguintes tocam exatamente o mesmo áudio
    return _ler_cache(chave, texto, tmp_dir)


# ---------------------------------------------------------------------------------------------
# engine edge (Antonio, 18/10/2026)
# ---------------------------------------------------------------------------------------------

def _narrar_edge(texto, rate, tmp_dir, pitch, tentativas):
    chave = hashlib.sha1(f"{VOZ}|{rate}|{pitch}|{VOICE_CHAIN}|{texto}".encode("utf-8")).hexdigest()[:16]
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
            time.sleep(3 * (k + 1))
        else:
            raise SystemExit(f"ERRO: edge-tts falhou {tentativas}x para {texto[:50]!r}: {erro}")
        mp3 = os.path.join(tmp_dir, f"{chave}.mp3")
        open(mp3, "wb").write(audio)
        _masterizar(mp3, wav)
        json.dump(pal, open(meta, "w", encoding="utf-8"), ensure_ascii=False)
    return som.ler_wav(wav), _expandir(json.load(open(meta, encoding="utf-8")))


def narrar(texto, rate, tmp_dir, pitch=TOM, tentativas=4):
    """-> (audio mono float32 48 kHz, [{t, d, w}]). Falha ALTO se o serviço não devolver áudio, se
    as palavras não baterem com o texto ou se os tempos não sustentarem a legenda.
    gemini: cache persistente em animado/voz_cache/ (chave = engine|voz|modelo|prompt|taxa|
    masterização|texto); acerto no cache não chama rede nem whisper.
    edge: cache só em tmp_dir (o edge-tts é determinístico o bastante e devolve os tempos)."""
    os.makedirs(tmp_dir, exist_ok=True)
    if ENGINE == "gemini":
        audio, pal = _narrar_gemini(texto, rate, tmp_dir, pitch)
        audio = _arrematar(audio)
    elif ENGINE == "edge":
        audio, pal = _narrar_edge(texto, rate, tmp_dir, pitch, tentativas)
    else:
        raise SystemExit(f"ERRO: ENGINE de voz desconhecida: {ENGINE!r}")
    conferir_palavras(texto, pal, len(audio) / som.SR)
    return audio, pal
