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


if __name__ == "__main__":
    teste_alinhador()
    teste_tempos()
    teste_cache()
    print("RESULTADO:", "PASSOU" if not FALHAS else f"REPROVOU ({len(FALHAS)}): {FALHAS}")
    sys.exit(1 if FALHAS else 0)
