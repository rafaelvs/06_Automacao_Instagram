# -*- coding: utf-8 -*-
"""Alinhador de palavras para vozes que NÃO devolvem tempo por palavra (Gemini-TTS).

O motor animado é comandado pelo tempo de cada palavra (legenda acende a palavra falada, o corte
acontece quando a voz diz "cortar"). O edge-tts entrega isso pronto (WordBoundary); o Gemini-TTS
não. Aqui o tempo sai do próprio áudio: faster-whisper com word_timestamps reconhece as palavras e
o texto CONHECIDO é casado com elas por alinhamento de sequência.

Provado em 16/11/2026 com controle positivo (Antonio, cujo WordBoundary é a verdade, passado pela
mesma VOICE_CHAIN; 258 palavras em 3 textos): modelo `small` int8, SEM prompt, com ajuste do início
pela energia do áudio -> erro mediano 42 ms, p95 85 ms, máximo 209 ms; ~0,6x a duração do áudio em
4 threads. Na Sadaltager a fração casada ficou entre 0,96 e 1,00 nos 5 textos medidos.

alinhar(wav, texto) -> dict:
  palavras  [{t, d, w, casada}] — UMA por palavra de texto.split(), na ordem; w é a palavra DO TEXTO
            (então voz.conferir_palavras() passa por construção — o que se confere de verdade é a
            concordância abaixo).
  fracao    fração das palavras do texto casadas a uma palavra reconhecida (as outras têm o tempo
            interpolado entre vizinhas casadas).
  buraco    maior sequência de palavras seguidas sem par.
  inseridas palavras reconhecidas A MAIS entre dois trechos casados (na medição de 16/11 o Gemini
            pareceu ler "com osso novo" como "com o osso novo" — mas o Whisper fez o MESMO no controle
            do Antonio, que lê literal: palavra curta a mais/a menos é ruído do reconhecedor).
  omitidas  palavras do texto que a voz pulou entre dois trechos casados.

Quem chama decide e falha ALTO (ver `problemas`). O prompt com o texto (initial_prompt) NÃO é usado:
no controle ele fez o Whisper pular metade da narração e, quando não pula, esconde exatamente os
erros que queremos pegar (palavra a mais/a menos).
"""
import difflib
import re
import unicodedata

MODELO = "small"            # base erra "osso" -> "oco"; medium leva ~4x a duração em 4 vCPU
FRACAO_MINIMA = 0.90        # controle positivo: small sem prompt deu >= 0,939; texto errado deu 0,087
BURACO_MAXIMO = 4           # pior caso legítimo medido = 3; 8 palavras inseridas no texto = 8
DIVERGENCIA_MAXIMA = 2      # palavras RELEVANTES (>= 3 letras) a mais/a menos entre trechos casados
DIVERGENCIA_LETRAS = 3      # "o", "a", "e", "de": o próprio Whisper insere/omite (controle Antonio,
                            # 16/11: "com o osso" e "o"/"a" a mais com uma voz que lê literal) — só
                            # registra para a escuta, não reprova
LIMIAR_GRAFIA = 0.5         # par 1:1 dentro de um bloco "replace" de mesmo tamanho ("pra" x "para")
SILENCIO_DB = -40.0         # quadro de 10 ms abaixo disto (relativo ao p95 do envelope) = silêncio

_MODELOS = {}


def _norm(w):
    """Idêntica a voz._norm."""
    return re.sub(r"[^\w-]", "", w.lower())


_NUM = {"0": "zero", "1": "um", "2": "dois", "3": "tres", "4": "quatro", "5": "cinco", "6": "seis",
        "7": "sete", "8": "oito", "9": "nove", "10": "dez", "12": "doze", "15": "quinze", "20": "vinte"}


def _chave(w):
    """Chave de COMPARAÇÃO: sem acento e sem hífen, algarismo vira palavra ('3' = 'três') e grafias
    de mesmo som se igualam ('osso' = 'oço', 'correção' = 'corressão')."""
    w = _norm(w).replace("ç", "s").replace("ss", "s").replace("rr", "r")
    w = unicodedata.normalize("NFKD", w)
    w = "".join(c for c in w if not unicodedata.combining(c)).replace("-", "")
    return _NUM.get(w, w)


def _modelo(modelo, cpu_threads=0):
    if not isinstance(modelo, str):
        return modelo
    k = (modelo, cpu_threads)
    if k not in _MODELOS:
        from faster_whisper import WhisperModel
        _MODELOS[k] = WhisperModel(modelo, device="cpu", compute_type="int8", cpu_threads=cpu_threads)
    return _MODELOS[k]


def reconhecer(wav_path, modelo=MODELO, cpu_threads=0):
    """-> [{t, e, w}] palavras reconhecidas (token com espaço interno é repartido por letras)."""
    m = _modelo(modelo, cpu_threads)
    segs, _ = m.transcribe(wav_path, language="pt", word_timestamps=True, beam_size=5,
                           vad_filter=False, condition_on_previous_text=False, initial_prompt=None)
    out = []
    for s in segs:
        for w in (s.words or []):
            partes = [p for p in w.word.split() if _chave(p)]
            if not partes:
                continue
            tot = sum(len(p) for p in partes); t = w.start; dur = max(w.end - w.start, 0.0)
            for p in partes:
                d = dur * len(p) / tot
                out.append({"t": t, "e": t + d, "w": p}); t += d
    return out


def _repartir(palavras, t0, t1):
    """Reparte [t0, t1] entre as palavras por número de letras -> [(t, d)]."""
    t1 = max(t1, t0)
    tot = sum(max(len(_chave(w)), 1) for w in palavras)
    res, t = [], t0
    for w in palavras:
        d = (t1 - t0) * max(len(_chave(w)), 1) / tot
        res.append((t, d)); t += d
    return res


def alinhar_tokens(texto, rec, duracao=None):
    """Núcleo determinístico (testável sem áudio): texto + reconhecidas -> dict (ver módulo)."""
    tw = texto.split()
    a = [_chave(w) for w in tw]
    b = [_chave(r["w"]) for r in rec]
    n = len(tw)
    tempo = [None] * n
    casada = [False] * n
    inseridas, omitidas = [], []
    ops = difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes()
    for k_op, (op, i1, i2, j1, j2) in enumerate(ops):
        entre_casados = (0 < k_op < len(ops) - 1 and ops[k_op - 1][0] == "equal"
                         and ops[k_op + 1][0] == "equal")
        if op == "equal":
            for k in range(i2 - i1):
                r = rec[j1 + k]; tempo[i1 + k] = (r["t"], r["e"] - r["t"]); casada[i1 + k] = True
        elif op == "replace":
            if i2 - i1 == j2 - j1:
                for k in range(i2 - i1):
                    r = rec[j1 + k]
                    if difflib.SequenceMatcher(None, a[i1 + k], b[j1 + k]).ratio() >= LIMIAR_GRAFIA:
                        tempo[i1 + k] = (r["t"], r["e"] - r["t"]); casada[i1 + k] = True
            else:
                # "pronto-socorro" x "pronto" "socorro", "um milímetro" x "1 mm": grafia, não voz
                for k, td in enumerate(_repartir(tw[i1:i2], rec[j1]["t"], rec[j2 - 1]["e"])):
                    tempo[i1 + k] = td
        elif op == "insert" and entre_casados:
            inseridas += [{"w": r["w"], "t": round(r["t"], 3), "depois_de": i1 - 1} for r in rec[j1:j2]]
        elif op == "delete" and entre_casados:
            omitidas += [{"w": tw[i], "posicao": i} for i in range(i1, i2)]
    fim_total = duracao if duracao is not None else (rec[-1]["e"] if rec else 0.0)
    i = 0
    while i < n:
        if tempo[i] is not None:
            i += 1; continue
        j = i
        while j < n and tempo[j] is None:
            j += 1
        t0 = (tempo[i - 1][0] + tempo[i - 1][1]) if i > 0 else 0.0
        t1 = tempo[j][0] if j < n else max(fim_total, t0)
        for k, td in enumerate(_repartir(tw[i:j], t0, t1)):
            tempo[i + k] = td
        i = j
    pal, ult = [], 0.0
    for w, (t, d), c in zip(tw, tempo, casada):
        t = max(t, ult); d = max(d, 0.0)
        pal.append({"t": round(t, 4), "d": round(d, 4), "w": w, "casada": c}); ult = t
    fracao = (sum(casada) / n) if n else 0.0
    return {"palavras": pal, "fracao": fracao, "buraco": maior_buraco(pal),
            "inseridas": inseridas, "omitidas": omitidas}


def maior_buraco(pal):
    m = r = 0
    for p in pal:
        r = 0 if p.get("casada") else r + 1; m = max(m, r)
    return m


def problemas(res, texto):
    """-> lista de motivos para REJEITAR a tomada (vazia = aceitável)."""
    out = []
    if [p["w"] for p in res["palavras"]] != texto.split():
        out.append("alinhador devolveu palavras que não são as do texto")
    if res["fracao"] < FRACAO_MINIMA:
        out.append(f"casadas {res['fracao']:.1%} < {FRACAO_MINIMA:.0%}")
    if res["buraco"] > BURACO_MAXIMO:
        out.append(f"{res['buraco']} palavras seguidas sem par > {BURACO_MAXIMO}")
    rel = divergencias_relevantes(res)
    if len(rel) > DIVERGENCIA_MAXIMA:
        out.append(f"{len(rel)} palavra(s) a mais/a menos na voz > {DIVERGENCIA_MAXIMA}: {rel}")
    return out


def divergencias_relevantes(res):
    """Palavras com >= DIVERGENCIA_LETRAS letras que a voz disse a mais ou pulou entre trechos casados."""
    return ([f"+{x['w']}" for x in res["inseridas"] if len(_chave(x["w"])) >= DIVERGENCIA_LETRAS]
            + [f"-{x['w']}" for x in res["omitidas"] if len(_chave(x["w"])) >= DIVERGENCIA_LETRAS])


def envelope_db(wav_path, passo=0.01):
    """Envelope RMS em dB (quadros de `passo` s), relativo ao p95. -> (env, passo) ou (None, passo)."""
    import wave
    import numpy as np
    try:
        with wave.open(wav_path) as f:
            sr, ch, sw, n = f.getframerate(), f.getnchannels(), f.getsampwidth(), f.getnframes()
            raw = f.readframes(n)
    except Exception:                                   # noqa: BLE001 — formato que o wave não lê
        return None, passo
    if sw != 2:
        return None, passo
    x = np.frombuffer(raw, dtype="<i2").astype(np.float32).reshape(-1, ch).mean(axis=1) / 32768.0
    h = max(int(sr * passo), 1); k = len(x) // h
    if k == 0:
        return None, passo
    rms = np.sqrt((x[:k * h].reshape(k, h) ** 2).mean(axis=1) + 1e-12)
    db = 20 * np.log10(rms); return db - np.percentile(db, 95), passo


def ajustar_inicio(pal, env, passo, limiar=SILENCIO_DB, pausa_min=0.15):
    """O Whisper puxa o início da palavra que vem depois de pausa para DENTRO da pausa (controle de
    16/11: 'Manda' após ponto final saiu 0,86 s adiantado). Se nos primeiros 80% da palavra há pausa
    (silêncio contínuo >= pausa_min), o início vai para o fim da ÚLTIMA dessas pausas; se o início
    cai em silêncio curto, avança até o 1º quadro com voz. Só avança, nunca recua; o FIM da palavra
    fica onde estava. Isso levou o erro máximo de 859 para 209 ms."""
    if env is None:
        return pal
    n = len(env); minq = max(int(round(pausa_min / passo)), 1)
    for p in pal:
        i = int(p["t"] / passo); fim = min(int((p["t"] + p["d"] * 0.8) / passo), n)
        if i >= fim:
            continue
        novo_q, run = None, 0
        for j in range(i, fim):
            if env[j] <= limiar:
                run += 1
            else:
                if run >= minq or (run > 0 and run == j - i):
                    novo_q = j
                run = 0
        if novo_q is not None:
            novo = novo_q * passo
            p["d"] = round(max(p["t"] + p["d"] - novo, 0.0), 4); p["t"] = round(novo, 4)
    return pal


def alinhar(wav_path, texto, modelo=MODELO, cpu_threads=0, ajuste=True):
    """wav PCM 16 bits (o mesmo áudio que vai para o vídeo) + texto -> dict (ver módulo)."""
    import wave
    with wave.open(wav_path) as f:
        dur = f.getnframes() / f.getframerate()
    res = alinhar_tokens(texto, reconhecer(wav_path, modelo, cpu_threads), dur)
    if ajuste:
        env, passo = envelope_db(wav_path)
        ajustar_inicio(res["palavras"], env, passo)
    res["duracao"] = dur
    return res
