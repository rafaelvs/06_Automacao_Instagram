# -*- coding: utf-8 -*-
"""Testes OFFLINE da voz do motor animado (16/11/2026, voz F = Gemini-TTS Sadaltager).

Cobre o que não pode quebrar calado:
  1. alinhador (núcleo determinístico, sem áudio): casa o texto, tolera grafia do Whisper, acusa
     texto errado, trecho inserido e palavra de conteúdo a mais; NÃO reprova artigo a mais (ruído do
     próprio Whisper no controle do Antonio);
  2. conferência dos TEMPOS (ordem, sobreposição, fim do áudio);
  3. cache persistente: 1ª chamada sorteia tomadas (Gemini e Whisper DUBLADOS, com a assinatura
     real), rejeita a tomada ruim, grava FLAC+JSON; 2ª chamada é cache hit sem rede nem Whisper e
     devolve o MESMO áudio e os MESMOS tempos; chave muda com taxa/voz/texto;
  4. sem credencial e sem cache: falha ALTO com a mensagem do secret.
Nada toca a rede. Uso: python test_voz_animado.py   (exit 0 = tudo passou)
"""
import io
import subprocess
import os
import sys
import tempfile
import wave

import numpy as np

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from animado import alinhar as A   # noqa: E402
from animado import som, voz       # noqa: E402

FALHAS = []


def caso(nome, cond, extra=""):
    print(f"[{'ok' if cond else 'FALHOU'}] {nome}" + (f" — {extra}" if extra and not cond else ""))
    if not cond:
        FALHAS.append(nome)


def rec_de(palavras, passo=0.4, d=0.3):
    return [{"t": i * passo, "e": i * passo + d, "w": w} for i, w in enumerate(palavras)]


TEXTO = "No ritmo certo, o corpo preenche o vão com osso novo: uma ponte. Manda pra quem tá no alongamento."


def teste_alinhador():
    tw = TEXTO.split()
    r = A.alinhar_tokens(TEXTO, rec_de([w.strip(",.:") for w in tw]), 20.0)
    caso("alinhador: reconhecimento perfeito casa 100%", r["fracao"] == 1.0 and not A.problemas(r, TEXTO))
    caso("alinhador: palavras devolvidas são as DO TEXTO", [p["w"] for p in r["palavras"]] == tw)

    grafia = [w.strip(",.:") for w in tw]
    grafia[grafia.index("pra")] = "para"; grafia[grafia.index("tá")] = "está"; grafia[grafia.index("osso")] = "oço"
    r = A.alinhar_tokens(TEXTO, rec_de(grafia), 20.0)
    caso("alinhador: grafia do Whisper (pra/para, tá/está, osso/oço) não reprova", not A.problemas(r, TEXTO),
         str(A.problemas(r, TEXTO)))

    art = [w.strip(",.:") for w in tw]; art.insert(art.index("osso"), "o")
    r = A.alinhar_tokens(TEXTO, rec_de(art), 20.0)
    caso("alinhador: artigo a mais ('com o osso') é registrado", [x["w"] for x in r["inseridas"]] == ["o"])
    caso("alinhador: artigo a mais NÃO reprova (o Whisper faz isso no Antonio)", not A.problemas(r, TEXTO))

    cont = [w.strip(",.:") for w in tw]
    for w in ("grande", "bonito", "forte"):
        cont.insert(cont.index("ponte"), w)
    r = A.alinhar_tokens(TEXTO, rec_de(cont), 20.0)
    caso("alinhador: 3 palavras de conteúdo a mais reprovam", bool(A.problemas(r, TEXTO)), str(r["inseridas"]))

    falt = [w.strip(",.:") for w in tw]
    del falt[3:9]                                   # a voz pulou um trecho de 6 palavras
    r = A.alinhar_tokens(TEXTO, rec_de(falt), 20.0)
    caso("alinhador: trecho pulado (6 palavras) reprova pelo buraco", r["buraco"] >= 5 and bool(A.problemas(r, TEXTO)),
         f"buraco={r['buraco']}")

    outro = "Ele quer enfiar a régua em você pra coçar e a régua não pode entrar aqui dentro nunca".split()
    r = A.alinhar_tokens(TEXTO, rec_de(outro), 20.0)
    caso("alinhador: texto errado para o áudio reprova", r["fracao"] < 0.5 and bool(A.problemas(r, TEXTO)),
         f"fracao={r['fracao']:.2f}")

    tempos = [p["t"] for p in r["palavras"]]
    caso("alinhador: tempos interpolados são monotônicos mesmo com o texto errado", tempos == sorted(tempos))


def teste_tempos():
    ok = [{"t": 0.1, "d": 0.3, "w": "a"}, {"t": 0.5, "d": 0.3, "w": "b"}]
    caso("tempos: sequência normal passa", not voz.problemas_de_tempo(ok, 1.0))
    caso("tempos: fora de ordem acusa", bool(voz.problemas_de_tempo([ok[1], ok[0]], 1.0)))
    caso("tempos: sobreposição absurda acusa",
         bool(voz.problemas_de_tempo([{"t": 0.1, "d": 1.5, "w": "a"}, {"t": 0.5, "d": 0.3, "w": "b"}], 3.0)))
    caso("tempos: palavra além do fim do áudio acusa", bool(voz.problemas_de_tempo(ok, 0.4)))
    try:
        voz.conferir_palavras("a b", [{"t": 0.5, "d": 0.3, "w": "a"}, {"t": 0.1, "d": 0.3, "w": "b"}], 1.0)
        caso("tempos: conferir_palavras falha ALTO com tempo fora de ordem", False)
    except SystemExit as e:
        caso("tempos: conferir_palavras falha ALTO com tempo fora de ordem", "tempos" in str(e))
    try:
        voz.conferir_palavras("a b c", ok, 1.0)
        caso("palavras: conferir_palavras segue pegando narração truncada", False)
    except SystemExit:
        caso("palavras: conferir_palavras segue pegando narração truncada", True)


def _wav_falso(seg, freq):
    """WAV 48 kHz mono com 'fala' sintética (tom modulado) — bytes como os do Gemini (LINEAR16)."""
    sr = 48000; t = np.arange(int(seg * sr)) / sr
    x = 0.3 * np.sin(2 * np.pi * freq * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 3 * t))
    b = io.BytesIO()
    with wave.open(b, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((x * 32767).astype("<i2").tobytes())
    return b.getvalue()


def teste_cache():
    texto = "O pé torto já nasce virado: pra baixo e pra dentro. É comum."
    tw = texto.split()
    orig = (voz.CACHE_DIR, voz._gemini_tts, voz._credencial_google, A.alinhar)
    chamadas = {"tts": 0, "whisper": 0}
    with tempfile.TemporaryDirectory() as td:
        voz.CACHE_DIR = os.path.join(td, "voz_cache")
        try:
            def tts_falso(texto_, taxa, credencial, tentativas=5):       # mesma assinatura do real
                chamadas["tts"] += 1
                return _wav_falso(len(tw) * 0.35, 180 + 40 * chamadas["tts"])

            def alinhar_falso(wav_path, texto_, modelo=A.MODELO, cpu_threads=0, ajuste=True):
                chamadas["whisper"] += 1
                rec = rec_de([w.strip(",.:") for w in tw], passo=0.3, d=0.25)
                if chamadas["whisper"] == 1:                              # 1ª tomada: voz pulou trecho
                    rec = rec[:2] + rec[8:]
                with wave.open(wav_path) as f:
                    dur = f.getnframes() / f.getframerate()
                res = A.alinhar_tokens(texto_, rec, dur); res["duracao"] = dur
                return res

            voz._gemini_tts = tts_falso
            voz._credencial_google = lambda: ("token-de-teste", None)
            A.alinhar = alinhar_falso
            voz.ENGINE = "gemini"
            a1, p1 = voz.narrar(texto, voz.RITMO_COMO_FUNCIONA, os.path.join(td, "tmp1"))
            caso("cache: 1ª chamada rejeitou a tomada ruim e sorteou outra", chamadas["tts"] == 2,
                 f"tts={chamadas['tts']}")
            chave = voz.chave_cache(texto, voz.TAXA_GEMINI[voz.RITMO_COMO_FUNCIONA])
            flac = os.path.join(voz.CACHE_DIR, f"{chave}.flac"); meta = os.path.join(voz.CACHE_DIR, f"{chave}.json")
            caso("cache: gravou FLAC + JSON no diretório versionado", os.path.isfile(flac) and os.path.isfile(meta))
            import json
            m = json.load(open(meta, encoding="utf-8"))
            caso("cache: JSON registra a tomada aceita e a rejeitada",
                 m["alinhamento"]["tomada_aceita"] == 1 and len(m["alinhamento"]["tomadas"]) == 2
                 and m["voz"] == "Sadaltager" and m["texto"] == texto)

            def proibido(*a, **k):
                raise AssertionError("cache hit não pode chamar rede/whisper/credencial")
            voz._gemini_tts = proibido; voz._credencial_google = proibido; A.alinhar = proibido
            a2, p2 = voz.narrar(texto, voz.RITMO_COMO_FUNCIONA, os.path.join(td, "tmp2"))
            caso("cache: 2ª chamada é hit sem rede nem whisper", True)
            caso("cache: hit devolve EXATAMENTE o mesmo áudio", a1.shape == a2.shape and np.array_equal(a1, a2))
            caso("cache: hit devolve os mesmos tempos", p1 == p2)
            caso("cache: áudio do cache é mono 48 kHz", a2.ndim == 1 and abs(len(a2) / som.SR - len(tw) * 0.35) < 0.2)

            caso("chave: muda com a taxa", voz.chave_cache(texto, 1.05) != voz.chave_cache(texto, 1.00))
            caso("chave: muda com o texto", voz.chave_cache(texto, 1.05) != voz.chave_cache(texto + " ", 1.05))
            v0 = voz.VOZ_GEMINI; voz.VOZ_GEMINI = "Charon"
            caso("chave: muda com a voz", voz.chave_cache(texto, 1.05) != chave)
            voz.VOZ_GEMINI = v0

            # sem credencial e texto fora do cache -> falha ALTO com a instrução do secret
            voz._credencial_google = orig[2]
            salvo = {k: os.environ.pop(k, None) for k in ("GCP_TTS_TOKEN", "GOOGLE_APPLICATION_CREDENTIALS")}
            try:
                voz.narrar("Texto que não está no cache de jeito nenhum agora.", voz.RITMO_CONVERSA,
                           os.path.join(td, "tmp3"))
                caso("credencial: sem credencial e sem cache falha ALTO", False)
            except SystemExit as e:
                caso("credencial: sem credencial e sem cache falha ALTO", "GCP_TTS_SA_JSON" in str(e), str(e))
            finally:
                for k, v in salvo.items():
                    if v is not None:
                        os.environ[k] = v
            try:
                voz.narrar(texto, "+25%", os.path.join(td, "tmp4"))
                caso("ritmo: ritmo sem taxa aprovada falha ALTO", False)
            except SystemExit as e:
                caso("ritmo: ritmo sem taxa aprovada falha ALTO", "TAXA_GEMINI" in str(e))
            tam = os.path.getsize(flac) / 1024
            print(f"      (FLAC de {len(tw) * 0.35:.1f}s sintéticos: {tam:.0f} KiB)")
        finally:
            voz.CACHE_DIR, voz._gemini_tts, voz._credencial_google, A.alinhar = orig


def teste_revisao_alinhador():
    """Revisão adversarial de 16/11: cada caso abaixo PASSAVA calado antes da correção."""
    tw = TEXTO.split()
    limpo = [w.strip(",.:") for w in tw]

    r = A.alinhar_tokens(TEXTO, rec_de(limpo[:-3]), 20.0)            # voz cortada antes do fim
    caso("revisão: 3 palavras finais cortadas reprovam (antes: fração 0,96 e nenhum problema)",
         r["ponta_fim"] == 3 and any("finais" in p for p in A.problemas(r, TEXTO)), str(A.problemas(r, TEXTO)))
    r = A.alinhar_tokens(TEXTO, rec_de(limpo[:-1]), 20.0)
    caso("revisão: 1 palavra final sem par não reprova sozinha (ruído do Whisper)",
         not any("finais" in p for p in A.problemas(r, TEXTO)))

    frase = "O gesso não pode molhar e o tratamento leva dois meses no total, sem pressa nenhuma."
    fw = [w.strip(",.") for w in frase.split()]
    sem_nao = [w for w in fw if w != "não"]
    r = A.alinhar_tokens(frase, rec_de(sem_nao), 20.0)
    caso("revisão: 'não' omitido reprova (antes: só warning)", any("crítica" in p for p in A.problemas(r, frase)),
         str(A.problemas(r, frase)))
    doze = ["doze" if w == "dois" else w for w in fw]
    r = A.alinhar_tokens(frase, rec_de(doze), 20.0)
    caso("revisão: 'dois' dito 'doze' reprova (antes: casava pela grafia)",
         any("crítica" in p for p in A.problemas(r, frase)), str(A.problemas(r, frase)))
    r = A.alinhar_tokens(frase, rec_de(["2" if w == "dois" else w for w in fw]), 20.0)
    caso("revisão: '2' reconhecido no lugar de 'dois' casa", not A.problemas(r, frase), str(A.problemas(r, frase)))

    grande = "O osso fica grande e forte depois do tratamento."
    gw = [w.strip(".") for w in grande.split()]
    r = A.alinhar_tokens(grande, rec_de(["pequena" if w == "grande" else w for w in gw]), 20.0)
    caso("revisão: troca 1:1 ('grande' -> 'pequena') fica registrada como divergência",
         "~grande>pequena" in A.divergencias_relevantes(r), str(r["trocadas"]))

    hif = "Isso não espera: pronto-socorro na hora, avisando a equipe."
    r = A.alinhar_tokens(hif, rec_de("Isso não espera pronto socorro na hora avisando a equipe".split()), 20.0)
    caso("revisão: 'pronto-socorro' casa com 'pronto' 'socorro'", r["fracao"] == 1.0 and not A.problemas(r, hif),
         f"fracao={r['fracao']}")
    p = r["palavras"][3]
    caso("revisão: tempo da palavra com hífen cobre as duas partes", p["w"] == "pronto-socorro"
         and abs(p["t"] - 1.2) < 1e-6 and abs(p["t"] + p["d"] - 1.9) < 1e-6, str(p))

    arr = "Régua não! Arranhão aqui dentro pode infeccionar. Cobre a minha abertura."
    rec = rec_de("Régua não A ranhão aqui dentro pode infeccionar Cobra minha abertura".split())
    r = A.alinhar_tokens(arr, rec, 20.0)
    caso("revisão: Whisper partindo/juntando palavra ('A ranhão', 'Cobra') não reprova",
         not A.problemas(r, arr), str(A.problemas(r, arr)))


def _wav_sintetico(caminho, trechos, dur, sr=48000):
    """trechos = [(t0, t1, nível_dBFS)]: 'fala' (tom 220 Hz) ou ruído baixo, sobre silêncio."""
    rng = np.random.default_rng(7)
    x = np.zeros(int(dur * sr))
    for t0, t1, db, tipo in trechos:
        n0, n1 = int(t0 * sr), int(t1 * sr); t = np.arange(n1 - n0) / sr
        a = 10 ** (db / 20) * np.sqrt(2)
        x[n0:n1] += a * (np.sin(2 * np.pi * 220 * t) if tipo == "fala" else rng.standard_normal(n1 - n0) / np.sqrt(2))
    with wave.open(caminho, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


def teste_revisao_energia():
    """Fronteiras pela energia + voz fora das palavras, com o literal do incidente do cf_pe_torto:
    fim de 'crescimento.' cedo, 'Manda' começando na RESPIRAÇÃO (-31 dB)."""
    from animado.cf_fratura_cola import comprimir
    texto = "Primeiro vem a fala. Manda isso."
    with tempfile.TemporaryDirectory() as td:
        wav = os.path.join(td, "s.wav")
        fala = [(0.10, 0.50), (0.55, 0.90), (0.95, 1.20), (1.25, 1.90)]   # 'fala.' soa até 1,90
        tr = [(a, b, -12, "fala") for a, b in fala] + [(1.92, 2.30, -43, "ruido"),       # respiração
                                                          (2.40, 2.80, -12, "fala"), (2.85, 3.20, -12, "fala")]
        _wav_sintetico(wav, tr, 4.0)
        rec = [{"t": 0.10, "e": 0.50, "w": "Primeiro"}, {"t": 0.55, "e": 0.90, "w": "vem"},
               {"t": 0.95, "e": 1.20, "w": "a"}, {"t": 1.25, "e": 1.60, "w": "fala"},     # fim 0,30 s CEDO
               {"t": 1.60, "e": 2.80, "w": "Manda"}, {"t": 2.85, "e": 3.20, "w": "isso"}]  # início na pausa
        r = A.alinhar(wav, texto, rec=rec)
        p = {q["w"]: q for q in r["palavras"]}
        caso("energia: fim de 'fala.' avança até o fim do som (1,90 s)", abs(p["fala."]["t"] + p["fala."]["d"] - 1.90) <= 0.02,
             str(p["fala."]))
        caso("energia: início de 'Manda' sai da pausa/respiração para 2,40 s", abs(p["Manda"]["t"] - 2.40) <= 0.02,
             str(p["Manda"]))
        caso("energia: tomada limpa não reprova", not A.problemas(r, texto), str(A.problemas(r, texto)))
        audio = som.ler_wav(wav)
        nova, pal2, _ = comprimir(audio, r["palavras"])
        m = next(q for q in pal2 if q["w"] == "Manda")
        k = int(m["t"] * som.SR)
        antes = float(np.sqrt(np.mean(nova[k - int(0.2 * som.SR):k - int(0.02 * som.SR)] ** 2)))
        depois = float(np.sqrt(np.mean(nova[k + int(0.02 * som.SR):k + int(0.2 * som.SR)] ** 2)))
        caso("energia: depois do respiro inserido, T['manda'] cai no começo da fala", antes < 0.01 < depois,
             f"rms antes={antes:.4f} depois={depois:.4f}")
        # cortes do comprimir só em silêncio: nenhum trecho de fala some
        caso("energia: comprimir não come fala (energia total preservada)",
             abs(float(np.sum(nova ** 2)) - float(np.sum(audio ** 2))) / float(np.sum(audio ** 2)) < 0.01)

        # o Gemini REPETE a frase depois do fim: Whisper não reconheceu a repetição
        wav2 = os.path.join(td, "rep.wav")
        _wav_sintetico(wav2, tr + [(3.40, 3.70, -12, "fala"), (3.75, 3.95, -12, "fala")], 4.2)
        r2 = A.alinhar(wav2, texto, rec=rec)
        caso("energia: fala depois da última palavra (frase repetida) reprova (antes: fração 1,0 aceita)",
             any("fora das palavras" in q for q in A.problemas(r2, texto)), str(r2["fora"]))

    # comprimir com pausa ZERO antes do "Manda": o respiro não pode cair dentro da palavra
    sr = som.SR
    audio = np.ones(int(3.0 * sr), dtype=np.float32) * 0.1
    pal = [{"t": 0.1, "d": 0.9, "w": "fim."}, {"t": 1.0, "d": 0.5, "w": "Manda"}, {"t": 1.5, "d": 0.5, "w": "isso."}]
    nova, pal2, _ = comprimir(audio, pal)
    m = next(q for q in pal2 if q["w"] == "Manda")
    caso("comprimir: pausa 0 antes do 'Manda' -> 'Manda' deslocado junto com o respiro", abs(m["t"] - 2.6) < 0.01,
         f"T[manda]={m['t']:.2f}")


def teste_revisao_cache():
    """FLAC corrompido, versão errada, parciais, retentativas."""
    texto = "O pé torto já nasce virado: pra baixo e pra dentro. É comum."
    orig = (voz.CACHE_DIR, voz._gemini_tts, voz._credencial_google, A.alinhar)
    with tempfile.TemporaryDirectory() as td:
        voz.CACHE_DIR = os.path.join(td, "voz_cache")
        try:
            tw = texto.split()
            voz._gemini_tts = lambda texto_, taxa, credencial, tentativas=5: _wav_falso(len(tw) * 0.35, 200)

            def alinhar_falso(wav_path, texto_, modelo=A.MODELO, cpu_threads=0, ajuste=True, rec=None):
                with wave.open(wav_path) as f:
                    dur = f.getnframes() / f.getframerate()
                res = A.alinhar_tokens(texto_, rec_de([w.strip(",.:") for w in tw], passo=0.3, d=0.25), dur)
                res["duracao"] = dur
                return res
            voz._credencial_google = lambda: ("token-de-teste", None)
            A.alinhar = alinhar_falso
            voz.narrar(texto, voz.RITMO_COMO_FUNCIONA, os.path.join(td, "t1"))
            chave = voz.chave_cache(texto, voz.TAXA_GEMINI[voz.RITMO_COMO_FUNCIONA])
            flac = os.path.join(voz.CACHE_DIR, f"{chave}.flac"); meta = os.path.join(voz.CACHE_DIR, f"{chave}.json")
            caso("cache: nenhum arquivo parcial na pasta versionada",
                 sorted(os.listdir(voz.CACHE_DIR)) == sorted([f"{chave}.flac", f"{chave}.json"]),
                 str(os.listdir(voz.CACHE_DIR)))
            import json
            m = json.load(open(meta, encoding="utf-8"))
            caso("cache: JSON tem versão, nº de amostras e sha256 do PCM",
                 m["versao"] == voz.CACHE_VERSAO and m["amostras"] > 0 and len(m["pcm_sha256"]) == 64)
            bom = open(flac, "rb").read()
            ruim = bytearray(bom); meio = len(ruim) // 2
            ruim[meio:meio + 300] = bytes(255 - x for x in ruim[meio:meio + 300])
            open(flac, "wb").write(bytes(ruim))
            try:
                voz.narrar(texto, voz.RITMO_COMO_FUNCIONA, os.path.join(td, "t2"))
                caso("cache: FLAC com 300 bytes trocados falha ALTO", False)
            except SystemExit as e:
                caso("cache: FLAC com 300 bytes trocados falha ALTO", "cache de voz" in str(e), str(e))
            # FLAC VÁLIDO, mas de outro áudio (arquivo trocado): decodifica sem erro, o sha denuncia
            outro = os.path.join(td, "outro.wav"); open(outro, "wb").write(_wav_falso(len(tw) * 0.35, 330))
            subprocess.run([voz.ffmpeg(), "-y", "-loglevel", "error", "-i", outro, "-c:a", "flac", flac], check=True)
            try:
                voz.narrar(texto, voz.RITMO_COMO_FUNCIONA, os.path.join(td, "t2b"))
                caso("cache: FLAC válido de OUTRO áudio falha ALTO pelo sha256", False)
            except SystemExit as e:
                caso("cache: FLAC válido de OUTRO áudio falha ALTO pelo sha256", "não confere" in str(e), str(e))
            open(flac, "wb").write(bom)
            m2 = dict(m, versao=1); json.dump(m2, open(meta, "w", encoding="utf-8"))
            try:
                voz.narrar(texto, voz.RITMO_COMO_FUNCIONA, os.path.join(td, "t3"))
                caso("cache: entrada de versão antiga falha ALTO", False)
            except SystemExit as e:
                caso("cache: entrada de versão antiga falha ALTO", "versão" in str(e), str(e))
        finally:
            voz.CACHE_DIR, voz._gemini_tts, voz._credencial_google, A.alinhar = orig

    # retentativas: erro de corpo/JSON é transitório; sem espera depois da última tentativa
    import requests
    import time as _time
    esperas, chamadas = [], {"n": 0}

    class Resp:
        status_code = 200

        def json(self):
            raise ValueError("HTML de proxy")
    respostas = [requests.exceptions.ChunkedEncodingError("corpo cortado"), Resp()]

    def post_falso(*a, **k):
        chamadas["n"] += 1
        x = respostas[min(chamadas["n"] - 1, len(respostas) - 1)]
        if isinstance(x, Exception):
            raise x
        return x
    orig_post, orig_sleep = requests.post, _time.sleep
    requests.post, _time.sleep = post_falso, esperas.append
    try:
        voz._gemini_tts("texto", 1.0, ("tok", None), tentativas=5)
        caso("retentativa: falha persistente acaba em SystemExit", False)
    except SystemExit:
        caso("retentativa: ChunkedEncodingError e JSON inválido são retentados (5 chamadas)", chamadas["n"] == 5,
             f"chamadas={chamadas['n']}")
        caso("retentativa: não dorme depois da última tentativa", esperas == [5, 10, 20, 40], str(esperas))
    finally:
        requests.post, _time.sleep = orig_post, orig_sleep


def teste_caso_real_pe_torto():
    """O LITERAL do incidente: a tomada do cf_pe_torto em cache, passada pelo comprimir dos cf.
    Antes: cortes a -9,4 dB (sílabas comidas) e T['manda'] 2 s antes da fala."""
    from animado.cf_fratura_cola import _limpa, comprimir
    chave = "692f5aa341c8b679b1eafb7d"
    caminho = os.path.join(voz.CACHE_DIR, f"{chave}.json")
    if not os.path.isfile(caminho):
        caso("caso real: entrada do cf_pe_torto existe no cache", False); return
    import json
    m = json.load(open(caminho, encoding="utf-8"))
    with tempfile.TemporaryDirectory() as td:
        audio, pal = voz._ler_cache(chave, m["texto"], td)
    env = 20 * np.log10(np.sqrt((audio[:len(audio) // 480 * 480].reshape(-1, 480) ** 2).mean(1)) + 1e-9)
    env -= np.percentile(env, 95)
    pior = -99.0
    for a, b in zip(pal, pal[1:]):
        fa = a["t"] + a["d"]; g = b["t"] - fa
        alvo = 1.6 if _limpa(b["w"]) == "manda" else 0.30
        if g > max(0.42, alvo):
            meio = fa + g / 2; tir = g - alvo
            pior = max(pior, float(env[int((meio - tir / 2) / 0.01):int((meio + tir / 2) / 0.01) + 1].max()))
    caso("caso real: cortes do comprimir só em pausa/respiração (< -22 dB do p95)", pior < A.FALA_DB, f"pior={pior:.1f}")
    nova, pal2, _ = comprimir(audio, pal)
    mm = next(q for q in pal2 if q["w"] == "Manda")
    k = int(mm["t"] * som.SR)
    antes = float(np.sqrt(np.mean(nova[k - int(0.3 * som.SR):k] ** 2)))
    depois = float(np.sqrt(np.mean(nova[k:k + int(0.15 * som.SR)] ** 2)))
    caso("caso real: T['manda'] no começo da fala, depois do respiro", antes < 0.01 < depois,
         f"rms antes={antes:.4f} depois={depois:.4f}")


def teste_numeros_em_algarismo():
    """16/11/2026: 3 renders caíram porque o Whisper escreve '18', '24', '40%' e o roteiro diz 'dezoito',
    'vinte e quatro', 'quarenta por cento'. A voz estava CERTA; o conferidor é que não convertia."""
    texto = "Até os dezoito anos, cerca de quarenta por cento melhora em vinte e quatro meses, sem duas cirurgias."
    def rec_whisper(tokens):
        return rec_de([q.strip(",.") for t in tokens for q in A.numero_por_extenso(t)])
    certo = ["Até", "os", "18", "anos,", "cerca", "de", "40%", "melhora", "em", "24", "meses,", "sem", "2", "cirurgias."]
    r = A.alinhar_tokens(texto, rec_whisper(certo), 30.0)
    caso("números: algarismo do Whisper = número por extenso do roteiro (não reprova)", not A.problemas(r, texto),
         str(A.problemas(r, texto)))
    errado = list(certo); errado[2] = "19"
    r = A.alinhar_tokens(texto, rec_whisper(errado), 30.0)
    caso("números: CONTROLE — '19' no lugar de 'dezoito' continua reprovando", bool(A.problemas(r, texto)))
    caso("números: extenso de 1500, 100 e 21", A.numero_por_extenso("1500") == ["mil", "e", "quinhentos"]
         and A.numero_por_extenso("100") == ["cem"] and A.numero_por_extenso("21,") == ["vinte", "e", "um,"])


if __name__ == "__main__":
    teste_alinhador()
    teste_tempos()
    teste_cache()
    teste_revisao_alinhador()
    teste_revisao_energia()
    teste_revisao_cache()
    teste_caso_real_pe_torto()
    teste_numeros_em_algarismo()
    print("RESULTADO:", "PASSOU" if not FALHAS else f"REPROVOU ({len(FALHAS)}): {FALHAS}")
    sys.exit(1 if FALHAS else 0)
