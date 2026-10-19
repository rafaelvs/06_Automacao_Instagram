# -*- coding: utf-8 -*-
"""Entrada única da geração nova: `python -m animado.render <id> [--previa]`.

1. Acha o episódio em `episodios_entretenimento.py`.
2. PORTÃO CFM ANTES DE DESENHAR: todo texto que vai para a tela, para a voz e para a legenda
   passa por `cfm_guardrails.auditar`. VIOLAÇÃO = aborta (exit 1), não renderiza 1 quadro.
3. Despacha para o formato (conversa) ou para a cena (como_funciona -> animado/<cena>.py).
4. Grava `reels/_preview_<id>.mp4` (mesma convenção dos reels de voz) e confere a duração real.
`--previa` gera só quadros PNG de conferência em tmp/ (iteração rápida, sem codificar vídeo).
"""
import argparse
import importlib
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


def episodio(ep_id):
    from episodios_entretenimento import EPISODIOS_ENTRETENIMENTO
    for ep in EPISODIOS_ENTRETENIMENTO:
        if ep["id"] == ep_id:
            return ep
    raise SystemExit(f"ERRO: episódio {ep_id!r} não existe em episodios_entretenimento.py")


def textos(ep):
    """Toda superfície de texto do episódio (tela, voz e legenda)."""
    t = list(ep.get("gancho", [])) + [f["texto"] for f in ep.get("falas", [])] + list(ep.get("roteiro", []))
    return t + [ep.get("cta", ""), ep.get("legenda", ""), ep.get("personagem", "")]


def portao_cfm(ep):
    from cfm_guardrails import auditar
    from animado.base import SIG
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
    saida, total = mod.render(ep, mp4, tmp, previa=a.previa)
    if a.previa:
        print("prévias:", *saida, sep="\n  ")
        return 0
    from checar_dur import duracao_mp4
    real = duracao_mp4(mp4)
    if not real or abs(real - total) > 1.0:
        raise SystemExit(f"ERRO: {mp4} saiu com {real}s, esperado ~{total:.1f}s")
    print(f"OK {mp4} | {real:.1f}s | {os.path.getsize(mp4) / 1e6:.1f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
