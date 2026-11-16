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

Revisão adversarial de 16/11/2026 (o que mudou e por quê):
  * O FIM da palavra do Whisper sai 130-310 ms cedo antes de pausa, e o início da palavra depois de
    pausa cai DENTRO da respiração do Gemini (que fica entre -31 e -36 dB, acima do antigo limiar
    de -40). O `comprimir` dos cf_* corta e insere silêncio NO MEIO das pausas entre palavras: com
    o fim cedo ele comia o "z" de "gravidez", o "Ge" de "Gessos", e o respiro antes do "Manda" era
    inserido dentro de "crescimen|to" (T["manda"] 2 s antes da fala). Agora as fronteiras são
    refinadas pela energia (`refinar_fronteiras`: o fim avança e o início recua enquanto há voz; o
    início avança para depois de pausa/respiração) e `voz_fora_das_palavras` REPROVA a tomada se
    sobrar voz entre palavras, antes da primeira ou depois da última — o que também pega o Gemini
    repetindo a frase (CTA do cv_gesso_filho dita 2x e aceita com fração 1,0).
  * Corte no fim/começo não contava como omissão (só "entre trechos casados"): 3-4 palavras finais
    cortadas passavam. Agora conta, e mais de PONTA_MAXIMA palavras sem par numa ponta reprova.
  * Palavra CRÍTICA (não, nunca, nem, sem, números) a mais, a menos ou trocada reprova sempre: um
    "não" omitido invertia o sentido clínico e só dava warning. Número exige chave EXATA ("dois" x
    "doze" casava pela regra de grafia).
  * Troca 1:1 abaixo do limiar de grafia ("grande" -> "pequena") agora é divergência registrada.
  * Palavra com hífen ("pronto-socorro", "raio-X") casa pelas partes (o Whisper devolve
    "pronto" "socorro"); o tempo da palavra vai do início da 1ª parte ao fim da última.

alinhar(wav, texto) -> dict:
  palavras  [{t, d, w, casada}] — UMA por palavra de texto.split(), na ordem; w é a palavra DO TEXTO
            (então voz.conferir_palavras() passa por construção — o que se confere de verdade é a
            concordância abaixo).
  fracao    fração das palavras do texto casadas a uma palavra reconhecida (as outras têm o tempo
            interpolado entre vizinhas casadas).
  buraco    maior sequência de palavras seguidas sem par.
  ponta_ini / ponta_fim  palavras seguidas sem par no começo / no fim do texto.
  inseridas palavras reconhecidas A MAIS entre dois trechos casados (palavra curta a mais/a menos é
            ruído do próprio Whisper: no controle do Antonio, que lê literal, ele pôs "o"/"a" a mais).
  omitidas  palavras do texto que a voz pulou (inclusive nas pontas).
  trocadas  palavras do texto no lugar das quais a voz disse outra.
  criticas  divergências que envolvem palavra crítica ou número (qualquer uma reprova).
  fora      trechos de VOZ fora de qualquer palavra alinhada (qualquer um reprova).

Quem chama decide e falha ALTO (ver `problemas`). O prompt com o texto (initial_prompt) NÃO é usado:
no controle ele fez o Whisper pular metade da narração e, quando não pula, esconde exatamente os
erros que queremos pegar (palavra a mais/a menos).
"""
import difflib
import re
import unicodedata

import numpy as np

MODELO = "small"            # base erra "osso" -> "oco"; medium leva ~4x a duração em 4 vCPU
FRACAO_MINIMA = 0.90        # controle positivo: small sem prompt deu >= 0,939; texto errado deu 0,087
BURACO_MAXIMO = 4           # pior caso legítimo medido = 3; 8 palavras inseridas no texto = 8
PONTA_MAXIMA = 1            # palavras sem par seguidas no começo ou no fim (corte da narração)
DIVERGENCIA_MAXIMA = 2      # palavras RELEVANTES (>= 3 letras) a mais/a menos/trocadas
DIVERGENCIA_LETRAS = 3      # "o", "a", "e", "de": o próprio Whisper insere/omite (controle Antonio,
                            # 16/11: "com o osso" e "o"/"a" a mais com uma voz que lê literal) — só
                            # registra para a escuta, não reprova
LIMIAR_GRAFIA = 0.5         # par 1:1 dentro de um bloco "replace" de mesmo tamanho ("pra" x "para")
LIMIAR_JUNTO = 0.75         # bloco "replace" de tamanhos diferentes comparado com as letras juntas
FALA_DB = -22.0             # quadro de 10 ms acima disto (relativo ao p95 do envelope) = FALA. A
                            # respiração do Gemini medida fica entre -27 e -36 dB e os estalos de
                            # boca em ~-23 dB por 20 ms: ficam na pausa (e o corte pode levá-los)
CAUDA_DB = -35.0            # rampa de subida/descida da fala que ainda pertence à palavra
CAUDA_MAX = 0.06            # s de rampa (abaixo de FALA_DB) absorvidos em cada ponta da palavra
PAUSA_MIN = 0.15            # pausa (ou respiração) no começo de uma palavra que move o início
PONTE_MAX = 0.13            # s sem fala DENTRO da palavra que o fim atravessa (oclusão do "t" de
                            # "impor|ta" mede 60 ms; pausa de frase do Gemini >= 0,15 s)
FORA_MAX = 0.08             # s de FALA contínua fora de qualquer palavra: reprova a tomada

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
    w = _NUM.get(w, w)
    return {"duas": "dois", "duzentas": "duzentos", "trezentas": "trezentos", "quatorze": "catorze"}.get(w, w)


# Palavras cuja troca/omissão muda o SENTIDO da frase: tolerância zero. "um"/"uma" ficam de fora
# (são artigo na maioria das vezes, e o Whisper troca um pelo outro).
_CRITICAS = {_chave(w) for w in (
    "não nunca nem sem jamais nenhum nenhuma nada ninguém zero dois duas três quatro cinco seis "
    "sete oito nove dez onze doze treze catorze quatorze quinze dezesseis dezessete dezoito "
    "dezenove vinte trinta quarenta cinquenta sessenta setenta oitenta noventa cem cento duzentos "
    "trezentos mil meio meia dobro metade").split()}


_UNID = "zero um dois tres quatro cinco seis sete oito nove dez onze doze treze catorze quinze dezesseis dezessete dezoito dezenove".split()
_DEZ = "_ _ vinte trinta quarenta cinquenta sessenta setenta oitenta noventa".split()
_CEM = "_ cento duzentos trezentos quatrocentos quinhentos seiscentos setecentos oitocentos novecentos".split()


def _extenso(n):
    """Inteiro 0..9999 -> palavras em português ('24' -> ['vinte', 'e', 'quatro'])."""
    if n < 20:
        return [_UNID[n]]
    if n < 100:
        d, u = divmod(n, 10)
        return [_DEZ[d]] + (["e"] + _extenso(u) if u else [])
    if n < 1000:
        if n == 100:
            return ["cem"]
        c, r = divmod(n, 100)
        return [_CEM[c]] + (["e"] + _extenso(r) if r else [])
    m, r = divmod(n, 1000)
    return ([] if m == 1 else _extenso(m)) + ["mil"] + ((["e"] if r < 100 or r % 100 == 0 else []) + _extenso(r) if r else [])


def numero_por_extenso(tok):
    """O Whisper escreve número em ALGARISMO ('18', '24', '40%') e o roteiro, por extenso ('dezoito',
    'vinte e quatro', 'quarenta por cento'). Sem isto a conferência de palavra crítica reprovava toda
    tomada CORRETA com número (16/11/2026: cf_* com 'dezoito', 'catorze', 'vinte e quatro' e
    'por cento' caíram nas 3 tomadas). Token sem algarismo volta como está."""
    m = re.fullmatch(r"([^\w%]*)(\d{1,4})(%?)([^\w%]*)", tok)
    if not m:
        return ["por", "cento"] if tok.strip(".,;:!?") == "%" else [tok]
    out = _extenso(int(m.group(2))) + (["por", "cento"] if m.group(3) else [])
    out[-1] = out[-1] + m.group(4)          # devolve a pontuação final (vírgula/ponto) à última palavra
    return out


def critica(w):
    """Palavra crítica (negação, número por extenso ou algarismo)?"""
    k = _chave(w)
    return k in _CRITICAS or any(c.isdigit() for c in k)


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
            partes = [q for p in w.word.split() for q in numero_por_extenso(p) if _chave(q)]
            if not partes:
                continue
            tot = sum(len(p) for p in partes); t = w.start; dur = max(w.end - w.start, 0.0)
            for p in partes:
                d = dur * len(p) / tot
                out.append({"t": t, "e": t + d, "w": p}); t += d
    return out


def _partir_hifen(rec):
    """'pronto-socorro' reconhecido como UM token vira dois, tempo repartido por letras."""
    out = []
    for r in rec:
        partes = [p for p in _norm(r["w"]).split("-") if _chave(p)]
        if len(partes) <= 1:
            out.append(r); continue
        tot = sum(len(p) for p in partes); t = r["t"]; dur = max(r["e"] - r["t"], 0.0)
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
    n = len(tw)
    # sub-palavras: "pronto-socorro" casa pelas partes; dono[k] = índice da palavra do texto
    sub, dono = [], []
    for i, w in enumerate(tw):
        partes = [p for p in _norm(w).split("-") if _chave(p)] or [w]
        sub += partes; dono += [i] * len(partes)
    rec = _partir_hifen(rec)
    a = [_chave(w) for w in sub]
    b = [_chave(r["w"]) for r in rec]
    m = len(sub)
    tempo = [None] * m
    casada = [False] * m
    inseridas, omitidas, trocadas, criticas, ins_pontas = [], [], [], [], []
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
                    r = rec[j1 + k]; x, y = a[i1 + k], b[j1 + k]
                    tempo[i1 + k] = (r["t"], r["e"] - r["t"])      # posição certa, mesmo se trocada
                    if critica(sub[i1 + k]) or critica(r["w"]):
                        ok = x == y                                  # número/negação: chave EXATA
                    else:
                        ok = difflib.SequenceMatcher(None, x, y).ratio() >= LIMIAR_GRAFIA
                    if ok:
                        casada[i1 + k] = True
                    else:
                        trocadas.append({"w": tw[dono[i1 + k]], "por": r["w"], "posicao": dono[i1 + k]})
                        if critica(sub[i1 + k]) or critica(r["w"]):
                            criticas.append(f"{tw[dono[i1 + k]]}->{r['w']}")
            else:
                for k, td in enumerate(_repartir(sub[i1:i2], rec[j1]["t"], rec[j2 - 1]["e"])):
                    tempo[i1 + k] = td
                voz_dita = " ".join(r["w"] for r in rec[j1:j2])
                crit = [s for s in sub[i1:i2] if critica(s)] + [r["w"] for r in rec[j1:j2] if critica(r["w"])]
                junto = difflib.SequenceMatcher(None, "".join(a[i1:i2]), "".join(b[j1:j2])).ratio()
                if not crit and junto >= LIMIAR_JUNTO:
                    # o Whisper partiu/juntou palavras ("Arranhão" -> "A ranhão", "Ar frio" ->
                    # "Arfrio", "Cobre a" -> "Cobra"): mesmo som, grafia diferente
                    for k in range(i1, i2):
                        casada[k] = True
                else:
                    for k in range(i1, i2):
                        trocadas.append({"w": tw[dono[k]], "por": voz_dita, "posicao": dono[k]})
                    if crit:
                        criticas.append(f"{' '.join(sub[i1:i2])}->{voz_dita}")
        elif op == "insert":
            novas = [{"w": r["w"], "t": round(r["t"], 3), "depois_de": (dono[i1 - 1] if i1 else -1)}
                     for r in rec[j1:j2]]
            if entre_casados:
                inseridas += novas
                criticas += [f"+{x['w']}" for x in novas if critica(x["w"])]
            else:
                # nas pontas: alucinação típica do Whisper em silêncio; voz real a mais nas pontas é
                # pega pela energia (voz_fora_das_palavras)
                ins_pontas += novas
        elif op == "delete":
            for k in range(i1, i2):
                if not omitidas or omitidas[-1]["posicao"] != dono[k]:
                    omitidas.append({"w": tw[dono[k]], "posicao": dono[k]})
                if critica(sub[k]):
                    criticas.append(f"-{tw[dono[k]]}")
    fim_total = duracao if duracao is not None else (rec[-1]["e"] if rec else 0.0)
    i = 0
    while i < m:
        if tempo[i] is not None:
            i += 1; continue
        j = i
        while j < m and tempo[j] is None:
            j += 1
        t0 = (tempo[i - 1][0] + tempo[i - 1][1]) if i > 0 else 0.0
        t1 = tempo[j][0] if j < m else max(fim_total, t0)
        for k, td in enumerate(_repartir(sub[i:j], t0, t1)):
            tempo[i + k] = td
        i = j
    # sub-palavras -> palavras do texto
    ini_w, fim_w, cas_w = [None] * n, [0.0] * n, [True] * n
    for k in range(m):
        i = dono[k]; t, d = tempo[k]
        ini_w[i] = t if ini_w[i] is None else min(ini_w[i], t)
        fim_w[i] = max(fim_w[i], t + d)
        cas_w[i] = cas_w[i] and casada[k]
    pal, ult = [], 0.0
    for w, t, e, c in zip(tw, ini_w, fim_w, cas_w):
        t = max(t, ult); d = max(e - t, 0.0)
        pal.append({"t": round(t, 4), "d": round(d, 4), "w": w, "casada": c}); ult = t
    fracao = (sum(cas_w) / n) if n else 0.0
    ponta_ini = next((k for k, c in enumerate(cas_w) if c), n)
    ponta_fim = next((k for k, c in enumerate(reversed(cas_w)) if c), n)
    return {"palavras": pal, "fracao": fracao, "buraco": maior_buraco(pal),
            "ponta_ini": ponta_ini, "ponta_fim": ponta_fim,
            "inseridas": inseridas, "omitidas": omitidas, "trocadas": trocadas,
            "criticas": criticas, "inseridas_pontas": ins_pontas, "fora": []}


def maior_buraco(pal):
    m = r = 0
    for p in pal:
        r = 0 if p.get("casada") else r + 1; m = max(m, r)
    return m


def problemas(res, texto):
    """-> lista de motivos para REJEITAR a tomada (vazia = aceitável)."""
    out = []
    tw = texto.split()
    if [p["w"] for p in res["palavras"]] != tw:
        out.append("alinhador devolveu palavras que não são as do texto")
    if res["fracao"] < FRACAO_MINIMA:
        out.append(f"casadas {res['fracao']:.1%} < {FRACAO_MINIMA:.0%}")
    if res["buraco"] > BURACO_MAXIMO:
        out.append(f"{res['buraco']} palavras seguidas sem par > {BURACO_MAXIMO}")
    if res.get("ponta_fim", 0) > PONTA_MAXIMA:
        out.append(f"{res['ponta_fim']} palavra(s) finais sem par ({tw[-res['ponta_fim']:]}) — a voz pode "
                   f"ter cortado o fim")
    if res.get("ponta_ini", 0) > PONTA_MAXIMA:
        out.append(f"{res['ponta_ini']} palavra(s) iniciais sem par ({tw[:res['ponta_ini']]}) — a voz pode "
                   f"ter pulado o começo")
    if res.get("criticas"):
        out.append(f"palavra crítica (negação/número) divergente na voz: {res['criticas']}")
    rel = divergencias_relevantes(res)
    if len(rel) > DIVERGENCIA_MAXIMA:
        out.append(f"{len(rel)} palavra(s) a mais/a menos/trocadas na voz > {DIVERGENCIA_MAXIMA}: {rel}")
    if res.get("fora"):
        out.append("voz fora das palavras alinhadas (palavra não reconhecida, repetição ou tempo errado — "
                   f"o corte de silêncio comeria fala): {res['fora'][:4]}")
    return out


def divergencias_relevantes(res):
    """Palavras com >= DIVERGENCIA_LETRAS letras que a voz disse a mais, pulou ou trocou."""
    return ([f"+{x['w']}" for x in res["inseridas"] if len(_chave(x["w"])) >= DIVERGENCIA_LETRAS]
            + [f"-{x['w']}" for x in res["omitidas"] if len(_chave(x["w"])) >= DIVERGENCIA_LETRAS]
            + [f"~{x['w']}>{x['por']}" for x in res.get("trocadas", [])
               if len(_chave(x["w"])) >= DIVERGENCIA_LETRAS])


def envelope_db(wav_path, passo=0.01):
    """Envelope RMS em dB (quadros de `passo` s), relativo ao p95. -> (env, passo) ou (None, passo)."""
    import wave
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


def ajustar_inicio(pal, env, passo, limiar=FALA_DB, pausa_min=PAUSA_MIN):
    """O Whisper puxa o início da palavra que vem depois de pausa para DENTRO da pausa (controle de
    16/11: 'Manda' após ponto final saiu 0,86 s adiantado; no Gemini, para dentro da RESPIRAÇÃO).
    Se nos primeiros 80% da palavra há pausa (sem fala por >= pausa_min), o início vai para o fim
    da ÚLTIMA dessas pausas; se o início cai em silêncio curto, avança até o 1º quadro com fala.
    Só avança; o recuo (rampa de subida) e o fim são tratados em `refinar_fronteiras`."""
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


def refinar_fronteiras(pal, env, passo, duracao, limiar=FALA_DB):
    """Fronteiras pela ENERGIA, para que toda a fala caia DENTRO de alguma palavra (o `comprimir`
    dos cf_* corta e insere silêncio na pausa entre palavras; a CONVERSA corta o áudio em
    fim+0,12 s). Revisão 16/11: o fim do Whisper saía 130-310 ms cedo antes de pausa.
      fim:    avança pela fala, atravessando trechos sem fala de até PONTE_MAX (oclusão de
              consoante) se a fala volta depois; então absorve a rampa de descida (> CAUDA_DB, até
              CAUDA_MAX). Nunca passa do início da palavra seguinte.
      início: recua pela fala contígua e pela rampa de subida (até CAUDA_MAX), nunca antes do fim
              da palavra anterior.
    Respiração e estalo de boca (abaixo de `limiar`) ficam de fora, na pausa."""
    if env is None or not pal:
        return pal
    n = len(env)
    lim_audio = min(n, int(round(duracao / passo))) if duracao else n
    ponte = max(int(round(PONTE_MAX / passo)), 1); cauda = max(int(round(CAUDA_MAX / passo)), 1)
    for k, p in enumerate(pal):
        teto_t = pal[k + 1]["t"] if k + 1 < len(pal) else lim_audio * passo
        qt = min(int(teto_t / passo), lim_audio)
        q = int(round((p["t"] + p["d"]) / passo))
        ult = None                                    # último quadro com fala pertencente à palavra
        while q < qt:
            if env[q] > limiar:
                ult = q; q += 1; continue
            prox = next((j for j in range(q, min(q + ponte, qt)) if env[j] > limiar), None)
            if prox is None:
                break
            q = prox
        if ult is None:
            ult = int(round((p["t"] + p["d"]) / passo)) - 1
        r = ult + 1
        while r < qt and r - ult <= cauda and env[r] > CAUDA_DB:
            r += 1
        novo_fim = min(r * passo, teto_t)
        if novo_fim > p["t"] + p["d"]:
            p["d"] = round(novo_fim - p["t"], 4)
    for k, p in enumerate(pal):
        piso_t = (pal[k - 1]["t"] + pal[k - 1]["d"]) if k else 0.0
        qp = int(np.ceil(piso_t / passo - 1e-9)) if k else 0
        q = int(round(p["t"] / passo)) - 1
        while q >= qp and q < n and env[q] > limiar:
            q -= 1
        r = q
        while r >= qp and q - r < cauda and r < n and env[r] > CAUDA_DB:
            r -= 1
        novo = max((r + 1) * passo, piso_t)
        if novo < p["t"]:
            p["d"] = round(p["t"] + p["d"] - novo, 4); p["t"] = round(novo, 4)
    return pal


def voz_fora_das_palavras(pal, env, passo, limiar=FALA_DB, minimo=FORA_MAX):
    """Trechos de fala (>= `minimo` s acima de `limiar`) que não caem em nenhuma palavra: palavra que
    o Whisper não reconheceu, frase REPETIDA pelo Gemini ou fronteira errada. -> [{de, ate, onde}]"""
    if env is None:
        return []
    n = len(env)
    dentro = np.zeros(n, dtype=bool)
    for p in pal:
        dentro[int(p["t"] / passo):min(int(np.ceil((p["t"] + p["d"]) / passo)), n)] = True
    voz = (np.asarray(env) > limiar) & ~dentro
    out, q = [], 0
    minq = max(int(round(minimo / passo)), 1)
    while q < n:
        if not voz[q]:
            q += 1; continue
        r = q
        while r < n and voz[r]:
            r += 1
        if r - q >= minq:
            t0, t1 = q * passo, r * passo
            antes = [p["w"] for p in pal if p["t"] + p["d"] <= t0 + 1e-6]
            out.append({"de": round(t0, 2), "ate": round(t1, 2),
                        "onde": f"depois de {antes[-1]!r}" if antes else "antes da 1ª palavra"})
        q = r
    return out


def alinhar(wav_path, texto, modelo=MODELO, cpu_threads=0, ajuste=True, rec=None):
    """wav PCM 16 bits (o mesmo áudio que vai para o vídeo) + texto -> dict (ver módulo).
    `rec` (palavras já reconhecidas) só para medição/teste: pula o Whisper."""
    import wave
    with wave.open(wav_path) as f:
        dur = f.getnframes() / f.getframerate()
    if rec is None:
        rec = reconhecer(wav_path, modelo, cpu_threads)
    res = alinhar_tokens(texto, rec, dur)
    if ajuste:
        env, passo = envelope_db(wav_path)
        if env is None:
            raise SystemExit(f"ERRO: não consegui ler a energia de {wav_path!r} (WAV PCM 16 bits) — sem ela "
                             f"o alinhamento não é conferido.")
        ajustar_inicio(res["palavras"], env, passo)
        refinar_fronteiras(res["palavras"], env, passo, dur)
        res["fora"] = voz_fora_das_palavras(res["palavras"], env, passo)
    res["duracao"] = dur
    return res
