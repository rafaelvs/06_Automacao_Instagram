#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sincronizar_texto_sequencias.py — grava o TEXTO dos 5 frames dentro de cada item de
`sequences.json`, para que o portão CFM tenha o que ler.

POR QUE EXISTE (auditoria v2, 19/09/2026, achado D5 — o maior furo de cobertura da casa):
um item de `sequences.json` tinha só `id`, `images`, `label` e `theme`. Nenhum texto. Como
`publish.py:_texto_auditavel` monta a superfície auditável a partir de `caption`/`label`/
`theme` e das coleções `scenes`/`slides`/`frames`, e NENHUM dos 479 itens de biblioteca
tinha qualquer uma dessas coleções, o laço era código morto em todas as rotas: o texto
efetivamente auditado por sequência era de 41 caracteres (mediana) — algo como
"SEG · O que observar\\nSemana do Joelho" — enquanto **5 telas cheias de texto clínico**
iam ao ar. Medida na janela: cobertura real de 10,2% das superfícies publicadas, contra
"~100%" declarado no changelog. `checar_cfm.py` ainda imprimia "sequences.json: 0 legendas
auditadas" e saía 0 — cobertura zero lida como resultado limpo.

A fonte da verdade continua sendo o módulo Python (`NOVAS`); este script só ESPELHA o texto
no JSON da fila, que é o que o robô carrega na hora de publicar. Não toca em `images`, não
reordena e não cria nem remove item — a ordem por FASE de `sequences.json` (runbook §9) fica
intacta.

Uso:
  python sincronizar_texto_sequencias.py --conferir   # exit 1 se algum item estiver sem texto (CI)
  python sincronizar_texto_sequencias.py              # grava/atualiza o campo `frames`
  python sincronizar_texto_sequencias.py --auto-teste # prova que o conferidor reprova de verdade
"""
import argparse
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
SEQ = os.path.join(ROOT, "sequences.json")
MODULOS = ["sequencias_avulsas_lote2", "sequencias_avulsas", "gerar_sequencias"]


def textos_por_id():
    """{id: [{"segmento","titulo","texto","chamada"} x5]} lido dos módulos-fonte."""
    out = {}
    for nome in MODULOS:
        if not os.path.exists(os.path.join(ROOT, nome + ".py")):
            continue
        try:
            mod = __import__(nome)
        except Exception as e:                                    # noqa: BLE001
            print(f"AVISO: {nome}.py existe mas NAO importou: {e}")
            continue
        for item in (getattr(mod, "NOVAS", None) or getattr(mod, "SEQUENCIAS", None) or []):
            try:
                sid, _theme, _v, frames = item
            except (ValueError, TypeError):
                continue
            out[sid] = [{"segmento": seg, "titulo": t, "texto": sub, "chamada": cue}
                        for (seg, t, sub, cue) in frames]
    return out


def carregar():
    return json.load(open(SEQ, encoding="utf-8"))


def gravar(itens):
    with open(SEQ, "w", encoding="utf-8", newline="\n") as f:
        json.dump(itens, f, ensure_ascii=False, indent=2)
        f.write("\n")


def conferir(itens=None, verbose=True):
    """(sem_texto, desatualizados, ok). Sem texto = o portão não tem o que ler naquele item."""
    itens = itens if itens is not None else carregar()
    fonte = textos_por_id()
    sem, desatual, ok = [], [], 0
    for it in itens:
        sid = it.get("id")
        atual = it.get("frames")
        esperado = fonte.get(sid)
        if not atual:
            sem.append(sid)
        elif esperado and atual != esperado:
            desatual.append(sid)
        else:
            ok += 1
    if verbose:
        print(f"sequences.json: {len(itens)} itens | com texto e em dia: {ok} | "
              f"SEM texto: {len(sem)} | desatualizado vs fonte: {len(desatual)}")
        if sem:
            print("  sem texto:", ", ".join(sem[:12]), "..." if len(sem) > 12 else "")
        if desatual:
            print("  desatualizado:", ", ".join(desatual[:12]), "..." if len(desatual) > 12 else "")
        sem_fonte = [i["id"] for i in itens if i.get("id") not in fonte]
        if sem_fonte:
            print(f"  NOTA: {len(sem_fonte)} item(ns) sem modulo-fonte neste repo "
                  f"(sequencias antigas geradas fora de NOVAS): {', '.join(sem_fonte[:6])}"
                  f"{' ...' if len(sem_fonte) > 6 else ''}")
    return sem, desatual, ok


def sincronizar():
    itens = carregar()
    fonte = textos_por_id()
    mudou = 0
    for it in itens:
        esperado = fonte.get(it.get("id"))
        if esperado and it.get("frames") != esperado:
            it["frames"] = esperado
            mudou += 1
    if mudou:
        gravar(itens)
    print(f"{mudou} item(ns) com texto gravado/atualizado em sequences.json")
    return mudou


def auto_teste():
    """Controle positivo + negativo em memória (não grava)."""
    itens = carregar()
    fonte = textos_por_id()
    alvo = next((i for i in itens if i.get("id") in fonte), None)
    if not alvo:
        sys.exit("auto-teste: nenhum item com modulo-fonte para testar.")
    guardado = alvo.get("frames")
    try:
        alvo["frames"] = None                                     # positivo: sem texto tem de acusar
        sem, _d, _ok = conferir(itens, verbose=False)
        if alvo["id"] not in sem:
            sys.exit("FALHA: item SEM texto passou — o conferidor esta cego.")
        print("auto-teste: item sem texto foi ACUSADO, como esperado.")
        alvo["frames"] = [{"segmento": "x", "titulo": "y", "texto": "z", "chamada": "w"}]
        _s, desatual, _ok = conferir(itens, verbose=False)        # positivo: texto divergente acusa
        if alvo["id"] not in desatual:
            sys.exit("FALHA: texto DIVERGENTE da fonte passou.")
        print("auto-teste: texto divergente da fonte foi ACUSADO, como esperado.")
        alvo["frames"] = fonte[alvo["id"]]                        # negativo: texto certo passa
        sem, desatual, _ok = conferir(itens, verbose=False)
        if alvo["id"] in sem or alvo["id"] in desatual:
            sys.exit("FALHA: texto CORRETO foi acusado — o conferidor reprova tudo.")
        print("auto-teste: texto correto passou, como esperado. OK")
    finally:
        alvo["frames"] = guardado
    return 0


def main():
    ap = argparse.ArgumentParser(description="Espelha o texto dos frames de story dentro de sequences.json.")
    ap.add_argument("--conferir", action="store_true", help="so confere; exit 1 se faltar/divergir")
    ap.add_argument("--auto-teste", action="store_true")
    a = ap.parse_args()
    if a.auto_teste:
        return auto_teste()
    if not a.conferir:
        sincronizar()
    sem, desatual, _ok = conferir()
    if a.conferir and (sem or desatual):
        print("REPROVADO: ha sequencia sem texto auditavel — o portao CFM nao tem o que ler nela.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
