# -*- coding: utf-8 -*-
"""
LINT DE FRAMES — audita o TEXTO DE TELA de sequencias, stories e destaques.

POR QUE ESTE ARQUIVO EXISTE
---------------------------
checar_cfm.py varre sequences.json e stories.json procurando o campo 'caption'
(checar_cfm.py:193). Esses arquivos NAO TEM esse campo: sequences.json so guarda
id/theme/label/images e stories.json so id/image. Resultado: 239 itens auditados
como ZERO e o lint imprimindo "0 legendas auditadas" — falsa cobertura silenciosa.
destaques.json e pior: nem esta na lista de arquivos varridos (checar_cfm.py:184).

O texto que aparece na TELA desses itens nunca esteve em lugar nenhum que a
auditoria olhasse. Aqui ele e RESOLVIDO das fontes:

  SEQUENCIAS (150)
    - SEASONS (temporadas_data)                       -> 91  ids "<slug>-<dow>"
    - NOVAS (sequencias_avulsas_lote2)                -> 29  ids "s_*"
    - NEW_EPISODES via gerar_lote_2026.sequencia_de   -> 30  ids "s_*"
  STORIES (89)
    - STORIES de gerar_conteudo/stories_batch/2       -> story28..story90
    - textos_telas.json (transcricao de imagem)       -> story01, story03..27
  DESTAQUES (6, +1 orfao)
    - textos_telas.json (transcricao de imagem)       -> dest01..dest07

CONTRATO DE AUDITORIA
---------------------
Mesmo de sequencias_avulsas_lote2.py:410 — o texto do frame mais a assinatura do
rodape, que o template desenha em TODO frame:
    f"{theme} · {seg} · {title} · {sub} · {cue} · {SIG}"  -> auditar(..., "publico")
Anexar SIG e legitimo porque seq_story()/story() desenham SIG sempre (verificado em
codigo) e, para os itens transcritos, porque sig_visivel foi conferido na imagem.
Sem isso, a regra 'assinatura' dispararia falso positivo em todos os itens.

ESTADO: ADVISORY
----------------
Este lint NAO BLOQUEIA. A sequencia publica TODOS OS DIAS; ligar bloqueio antes de
a cobertura estar em 100% pararia a agenda diaria. Promover a bloqueante e decisao
do Rafael, depois de a cobertura fechar e as transcricoes serem revisadas.

FAIL-CLOSED NA RESOLUCAO: se uma fonte nao importar, isso e REGISTRADO como falha
de cobertura explicita (nunca "0 itens, tudo certo"). E a licao dos furos #3 e #10.

Rodar: python checar_frames.py   (use PYTHONIOENCODING=utf-8 no Windows)
"""
import json
import os

from cfm_guardrails import auditar

ROOT = os.path.dirname(os.path.abspath(__file__))

# Assinatura do rodape. Importada de gerar_conteudo para nao divergir; se o import
# falhar (PIL ausente), usa o literal e AVISA ALTO — nunca segue em silencio.
SIG_FALLBACK = "Dr. Rafael Vargas · Médico · CRM-SP 226103 · RQE 137901"
try:
    from gerar_conteudo import SIG
except Exception as _e:  # noqa: BLE001 — queremos capturar ImportError e erro de PIL
    SIG = SIG_FALLBACK
    print(f"AVISO: nao importou SIG de gerar_conteudo ({type(_e).__name__}: {_e}); "
          f"usando literal. Se o texto de SIG mudou la, este lint esta desatualizado.")

DOW = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]


def _erro(falhas, fonte, e):
    falhas.append((fonte, f"{type(e).__name__}: {e}"))
    print(f"FALHA DE COBERTURA: fonte '{fonte}' nao carregou -> {type(e).__name__}: {e}")


def frames_sequencias():
    """id -> {'theme': str, 'frames': [(seg, title, sub, cue), ...]}. Tambem retorna
    a lista de fontes que falharam (para NAO passar em silencio)."""
    out, falhas = {}, []

    # 1) SEASONS -> 91 ids "<slug>-<dow>"  (espelha gerar_temporadas.run(), :47-56)
    try:
        from temporadas_data import SEASONS
        for wk in SEASONS:
            slug, theme = wk["slug"], wk["theme"]
            for di, day in enumerate(wk["days"]):
                out[f"{slug}-{DOW[di]}"] = {"theme": theme, "frames": [tuple(f) for f in day]}
    except Exception as e:
        _erro(falhas, "temporadas_data.SEASONS", e)

    # 2) NOVAS -> 29 ids "s_*"  (espelha sequencias_avulsas_lote2.auditar_novas(), :405)
    try:
        from sequencias_avulsas_lote2 import NOVAS
        for sid, theme, _v, frames in NOVAS:
            out[sid] = {"theme": theme, "frames": [tuple(f) for f in frames]}
    except Exception as e:
        _erro(falhas, "sequencias_avulsas_lote2.NOVAS", e)

    # 3) NEW_EPISODES derivados -> 30 ids "s_<ep_id>"  (gerar_lote_2026.sequencia_de(), :38)
    #    O gerador so RENDERIZA; as entradas do JSON foram anexadas a mao. O texto,
    #    porem, e 100% derivavel — por isso reproduzimos a derivacao aqui.
    try:
        from episodios_novos_2026 import NEW_EPISODES
        from gerar_lote_2026 import sequencia_de
        for ep in NEW_EPISODES:
            ep_id, theme, dia = sequencia_de(ep)
            # dia vem como (variant, seg, title, sub, cue) — descartamos a variante
            out["s_" + ep_id] = {"theme": theme, "frames": [tuple(f[1:]) for f in dia]}
    except Exception as e:
        _erro(falhas, "episodios_novos_2026 + gerar_lote_2026.sequencia_de", e)

    return out, falhas


def textos_stories():
    """id -> (kicker, title, sub) para os stories com fonte viva em codigo."""
    out, falhas = {}, []
    for mod, attr in (("gerar_conteudo", "STORIES"),
                      ("stories_batch", "STORIES"),
                      ("stories_batch2", "STORIES")):
        try:
            m = __import__(mod)
            for t in getattr(m, attr):
                # tupla (id, variant, kicker, title, sub)
                if len(t) >= 5:
                    out[t[0]] = (t[2], t[3], t[4])
        except Exception as e:
            _erro(falhas, f"{mod}.{attr}", e)
    return out, falhas


def textos_transcritos():
    """id -> dict do textos_telas.json (stories orfaos + destaques)."""
    p = os.path.join(ROOT, "textos_telas.json")
    try:
        with open(p, encoding="utf-8") as fh:
            d = json.load(fh)
        return d.get("textos", {}), d.get("_meta", {}), []
    except Exception as e:
        return {}, {}, [("textos_telas.json", f"{type(e).__name__}: {e}")]


def _load(arq):
    try:
        with open(os.path.join(ROOT, arq), encoding="utf-8") as fh:
            d = json.load(fh)
        return d if isinstance(d, list) else []
    except Exception as e:
        print(f"AVISO: {arq}: {type(e).__name__}: {e}")
        return []


def relatorio(verbose=True):
    """Audita o texto de tela. Retorna dict com contagens. NAO bloqueia."""
    seq_txt, f1 = frames_sequencias()
    sto_txt, f2 = textos_stories()
    tra_txt, meta, f3 = textos_transcritos()
    falhas = f1 + f2 + f3

    violacoes, revisar, sem_texto, nao_revisados = [], [], [], []

    def audita(origem, _id, texto, sig_ok):
        # Se a assinatura NAO esta no render, nao anexamos SIG: deixamos a regra
        # 'assinatura' disparar de verdade (e um achado real, nao ruido).
        t = f"{texto} · {SIG}" if sig_ok else texto
        for sev, regra, det in auditar(t, contexto="publico"):
            (violacoes if sev == "VIOLACAO" else revisar).append((origem, _id, sev, regra, det))

    # --- SEQUENCIAS -----------------------------------------------------------
    n_seq_frames = 0
    for it in _load("sequences.json"):
        _id = it.get("id", "?")
        src = seq_txt.get(_id)
        if not src:
            sem_texto.append(("sequences.json", _id))
            continue
        theme = src["theme"]
        for i, fr in enumerate(src["frames"], 1):
            seg, title, sub, cue = (list(fr) + ["", "", "", ""])[:4]
            n_seq_frames += 1
            audita("seq:frame", f"{_id}#{i}", f"{theme} · {seg} · {title} · {sub} · {cue}", True)

    # --- STORIES --------------------------------------------------------------
    n_sto = 0
    for it in _load("stories.json"):
        _id = it.get("id", "?")
        if _id in sto_txt:
            k, t, s = sto_txt[_id]
            n_sto += 1
            audita("story:codigo", _id, f"{k} · {t} · {s}", True)
        elif _id in tra_txt:
            r = tra_txt[_id]
            n_sto += 1
            if not r.get("revisado", False):
                nao_revisados.append(("stories.json", _id))
            audita("story:transcrito", _id,
                   f"{r.get('kicker','')} · {r.get('title','')} · {r.get('sub','')}",
                   bool(r.get("sig_visivel")))
        else:
            sem_texto.append(("stories.json", _id))

    # --- DESTAQUES ------------------------------------------------------------
    # checar_cfm.py nem abre este arquivo. Aqui ele entra.
    n_dest = 0
    for it in _load("destaques.json"):
        _id = it.get("id", "?")
        r = tra_txt.get(_id)
        if not r:
            sem_texto.append(("destaques.json", _id))
            continue
        n_dest += 1
        if not r.get("revisado", False):
            nao_revisados.append(("destaques.json", _id))
        audita("destaque:transcrito", _id,
               f"{r.get('kicker','')} · {r.get('title','')} · {r.get('sub','')}",
               bool(r.get("sig_visivel")))

    # --- DISCLAIMER (achado sistemico) ---------------------------------------
    # seq_story() desenha DISC em todo frame; story() NAO desenha. Reportamos os
    # itens transcritos cujo disclaimer foi conferido AUSENTE na imagem.
    sem_disc = [k for k, v in tra_txt.items() if not v.get("disc_visivel", False)]

    if verbose:
        print("=== LINT DE FRAMES (texto de tela) — ADVISORY ===")
        print(f"sequencias: {n_seq_frames} frames auditados")
        print(f"stories:    {n_sto} itens auditados")
        print(f"destaques:  {n_dest} itens auditados  (checar_cfm.py nao audita nenhum)")
        print(f"\nVIOLACAO: {len(violacoes)}")
        for origem, _id, _sev, regra, det in violacoes[:40]:
            print(f"   [VIOLACAO] {origem:22s} {str(_id):30s} {regra}: {det}")
        from collections import Counter
        print(f"\nREVISAR: {len(revisar)} -> {dict(Counter(r[3] for r in revisar))}")
        for origem, _id, _sev, regra, det in [r for r in revisar if r[3] != 'assinatura'][:25]:
            print(f"   [REVISAR]  {origem:22s} {str(_id):30s} {regra}: {det}")

        print(f"\nSEM TEXTO RESOLVIVEL: {len(sem_texto)}")
        for arq, _id in sem_texto[:30]:
            print(f"   [SEM TEXTO] {arq:18s} {_id}")

        print(f"\nTRANSCRITOS AINDA NAO REVISADOS PELO MEDICO: {len(nao_revisados)}")
        if nao_revisados:
            print("   (texto veio de transcricao automatica de imagem; conferir antes de "
                  "promover este lint a bloqueante)")

        print(f"\nSEM DISCLAIMER NA IMAGEM: {len(sem_disc)} de {len(tra_txt)} transcritos")
        if sem_disc:
            print("   Causa raiz: gerar_conteudo.story() desenha SIG mas nao DISC "
                  "(seq_story() desenha os dois — gerar_temporadas.py:39).")

        if falhas:
            print(f"\n!!! FALHAS DE COBERTURA: {len(falhas)} fonte(s) nao carregaram")
            for fonte, err in falhas:
                print(f"   [FALHA] {fonte}: {err}")
            print("   Cobertura INCOMPLETA — os itens dessa fonte caem em SEM TEXTO acima.")

    return {
        "violacoes": violacoes, "revisar": revisar, "sem_texto": sem_texto,
        "nao_revisados": nao_revisados, "sem_disclaimer": sem_disc, "falhas": falhas,
        "n_seq_frames": n_seq_frames, "n_stories": n_sto, "n_destaques": n_dest,
    }


if __name__ == "__main__":
    relatorio()
