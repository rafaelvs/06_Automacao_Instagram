# -*- coding: utf-8 -*-
"""Entrada única da geração nova: `python -m animado.render <id> [--previa]`.

1. Acha o episódio em `episodios_entretenimento.py`.
2. PORTÃO ANTES DE DESENHAR: o episódio passa por `checar_entretenimento.checar_episodio` (forma,
   CTA de envio, rótulos de tela) e todo texto dele por `cfm_guardrails.auditar`. Problema = aborta
   (exit 1), não renderiza 1 quadro.
3. Despacha para o formato (conversa) ou para a cena (como_funciona -> animado/<cena>.py), com o
   canvas anotando todo texto desenhado em todos os quadros.
4. Grava `reels/_preview_<id>.mp4` (mesma convenção dos reels de voz), confere a duração real e
   RECUSA o vídeo se algum texto desenhado não estiver no episódio (rótulo só no código = fora do
   hash de aprovação e do CFM — auditoria 19/10).
5. Grava o arquivo-irmão `reels/_preview_<id>.json`: hash do episódio, hash dos módulos do motor e
   o texto desenhado. O checar_entretenimento (CI e antes de publicar) recusa vídeo cujo irmão não
   bate com o episódio e o motor atuais — vídeo velho não sai com legenda nova.
`--previa` gera só quadros PNG de conferência em tmp/ (iteração rápida, sem codificar vídeo).
"""
import argparse
import importlib
import io
import os
import sys

# reconfigure (e nao um TextIOWrapper novo): quem importa este modulo ja pode ter
# embrulhado o stdout, e o embrulho antigo, ao ser coletado, FECHA o buffer — o
# render de 19/10 perdeu 3 videos prontos com "I/O operation on closed file".
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


def episodio(ep_id):
    from episodios_entretenimento import EPISODIOS_ENTRETENIMENTO
    for ep in EPISODIOS_ENTRETENIMENTO:
        if ep["id"] == ep_id:
            return ep
    raise SystemExit(f"ERRO: episódio {ep_id!r} não existe em episodios_entretenimento.py")


def portao_cfm(ep):
    from cfm_guardrails import auditar
    from animado.base import SIG
    from checar_entretenimento import checar_episodio, textos
    probs = checar_episodio(ep)
    if probs:
        for x in probs:
            print(f"  [EPISÓDIO] {x}")
        raise SystemExit(f"ABORTADO: {len(probs)} problema(s) em {ep['id']} — nada foi renderizado.")
    viol, rev = [], []
    for s in [x for x in textos(ep) if x]:
        # a assinatura vai em todo quadro (rodapé) e na legenda: entra no texto auditado
        for sev, regra, det in auditar(f"{s} · {SIG}", contexto="publico"):
            (viol if sev == "VIOLACAO" else rev).append((regra, det, s[:60]))
    for r in rev:
        print(f"  [REVISAR] {r[0]}: {r[1]} — {r[2]!r}")
    if viol:
        for v in viol:
            print(f"  [VIOLACAO] {v[0]}: {v[1]} — {v[2]!r}")
        raise SystemExit(f"ABORTADO: {len(viol)} violação(ões) CFM em {ep['id']} — nada foi renderizado.")
    print(f"  portão CFM: {ep['id']} limpo ({len(rev)} aviso(s) de revisão)")


def main():
    ap = argparse.ArgumentParser(description="Renderiza um episódio da geração nova (conversa / como funciona).")
    ap.add_argument("id")
    ap.add_argument("--previa", action="store_true", help="só quadros PNG de conferência, sem vídeo")
    ap.add_argument("--saida", default="", help="mp4 de saída (padrão reels/_preview_<id>.mp4)")
    ap.add_argument("--tmp", default="", help="pasta de trabalho (padrão .animado_tmp/<id>)")
    a = ap.parse_args()

    ep = episodio(a.id)
    portao_cfm(ep)
    tmp = a.tmp or os.path.join(ROOT, ".animado_tmp", ep["id"])
    os.makedirs(tmp, exist_ok=True)
    mp4 = a.saida or os.path.join(ROOT, "reels", f"_preview_{ep['id']}.mp4")
    if ep["formato"] == "conversa":
        from animado import conversa as mod
    elif ep["formato"] == "como_funciona":
        mod = importlib.import_module(f"animado.{ep['cena']}")
    else:
        raise SystemExit(f"ERRO: formato desconhecido {ep['formato']!r}")
    from animado import base
    base.REGISTRO_ATIVO = set()
    if a.previa:
        saida, total = mod.render(ep, mp4, tmp, previa=True)
        print("prévias:", *saida, sep="\n  ")
        return 0
    # grava num PARCIAL e só promove ao caminho final depois de todas as checagens: render que
    # falha no meio fechava um mp4 válido e curto por cima do vídeo bom (auditoria 19/10)
    parcial = mp4 + ".parcial.mp4"
    try:
        _, total = mod.render(ep, parcial, tmp, previa=False)
        from checar_dur import duracao_mp4
        real = duracao_mp4(parcial)
        if not real or abs(real - total) > 1.0:
            raise SystemExit(f"ERRO: o vídeo saiu com {real}s, esperado ~{total:.1f}s")
        import checar_entretenimento as ce
        desenhados = sorted(base.REGISTRO_ATIVO)
        fora = ce.tela_fora_do_episodio(ep, desenhados)
        if not desenhados or fora:
            raise SystemExit(f"ERRO: texto desenhado fora do episódio {fora[:8] or '(nenhum registrado)'} — ponha no "
                             f"campo `tela` (que passa por aprovação e CFM) ou tire do desenho.")
    except BaseException:
        if os.path.exists(parcial):
            os.remove(parcial)
        print(f"render de {ep['id']} FALHOU — {mp4} ficou intocado")
        raise
    os.replace(parcial, mp4)
    if not a.saida:                                   # só o vídeo da fila ganha o arquivo-irmão
        import datetime as dt
        import json
        irmao = os.path.join(ROOT, ce.sidecar_de(ep).replace("/", os.sep))
        with open(irmao, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"id": ep["id"], "hash_episodio": ce.hash_episodio(ep), "hash_motor": ce.hash_motor(ep),
                       "modulos": ce.modulos_do_motor(ep), "textos_tela": desenhados, "dur": round(real, 2),
                       "renderizado_em": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")},
                      f, ensure_ascii=False, indent=1)
            f.write("\n")
        print(f"irmão: {ce.sidecar_de(ep)} ({len(desenhados)} textos desenhados, todos do episódio)")
    print(f"OK {mp4} | {real:.1f}s | {os.path.getsize(mp4) / 1e6:.1f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
