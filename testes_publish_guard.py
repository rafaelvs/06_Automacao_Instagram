# -*- coding: utf-8 -*-
"""
TESTE DE ENFORCEMENT — exercita publish._cfm_guard contra os itens REAIS do repo.

Prova as duas metades que importam e que costumam brigar entre si:
  1. a AGENDA DIARIA continua passando (sequencia publica todos os dias; se este teste
     ficar vermelho aqui, o robo para de publicar amanha);
  2. os caminhos que antes publicavam SEM CHECAGEM agora bloqueiam — story, sequencia e
     o ramo FORCE_ID=destaques.

E prova que os portoes sao INDEPENDENTES: conferir a transcricao de um item nao lava uma
violacao de conteudo. dest04 permanece bloqueado mesmo com texto_revisado=true.

NAO publica nada: _cfm_guard nao faz chamada de rede. As credenciais falsas existem so
porque publish.py aborta no import sem elas.

Rodar: python testes_publish_guard.py   (use PYTHONIOENCODING=utf-8 no Windows)
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
os.environ.setdefault("IG_USER_ID", "FAKE_NAO_USADO")
os.environ.setdefault("IG_ACCESS_TOKEN", "FAKE_NAO_USADO")

import publish  # noqa: E402


def _load(arq):
    with open(os.path.join(ROOT, arq), encoding="utf-8") as fh:
        return json.load(fh)


def tenta(rotulo, item, kind, espera_bloqueio):
    try:
        publish._cfm_guard(item, kind)
        ok = not espera_bloqueio
        print(f"{'OK ' if ok else 'XX '} {rotulo:36s} PASSOU"
              f"{'' if ok else '   <-- ESPERAVA BLOQUEIO'}")
    except RuntimeError as e:
        ok = espera_bloqueio
        print(f"{'OK ' if ok else 'XX '} {rotulo:36s} BLOQUEADO: {str(e)[:64]}"
              f"{'' if ok else '   <-- NAO DEVERIA'}")
    return ok


def main():
    seqs, stories, dests = _load("sequences.json"), _load("stories.json"), _load("destaques.json")
    r = []

    print("=== AGENDA DIARIA — tem que continuar passando ===")
    r.append(tenta("1a sequencia", seqs[0], "seq", False))
    r.append(tenta("ultima sequencia", seqs[-1], "seq", False))
    nao_pass = [s["id"] for s in seqs if not _passa(s, "seq")]
    print(f"    sequencias que NAO passam: {len(nao_pass)} {nao_pass[:5]}")
    r.append(len(nao_pass) == 0)
    sto_cod = next((s for s in stories if s.get("texto_origem") == "codigo"), None)
    if sto_cod:
        r.append(tenta(f"story com fonte em codigo ({sto_cod['id']})", sto_cod, "story", False))

    print("\n=== CAMINHOS QUE ANTES PUBLICAVAM SEM CHECAGEM ===")
    for _id in ("dest01", "dest04"):
        it = next((d for d in dests if d["id"] == _id), None)
        if it:
            r.append(tenta(f"{_id} (ramo FORCE_ID=destaques)", it, "story", True))
    for _id in ("story01", "story07"):
        it = next((s for s in stories if s["id"] == _id), None)
        if it:
            r.append(tenta(f"{_id} (transcricao nao conferida)", it, "story", True))

    print("\n=== FAIL-CLOSED ESTRUTURAL ===")
    r.append(tenta("sequencia sem 'frames'", {"id": "x", "theme": "t"}, "seq", True))
    r.append(tenta("story sem 'title'", {"id": "x", "image": "a.jpg"}, "story", True))
    r.append(tenta("post com promessa na legenda",
                   {"id": "x", "caption": "Garanto o resultado!"}, "post", True))

    print("\n=== PORTOES INDEPENDENTES (conferir != aprovar conteudo) ===")
    d01 = next((d for d in dests if d["id"] == "dest01"), None)
    d04 = next((d for d in dests if d["id"] == "dest04"), None)
    if d01:
        r.append(tenta("dest01 apos conferencia -> libera", {**d01, "texto_revisado": True},
                       "story", False))
    if d04:
        r.append(tenta("dest04 apos conferencia -> AINDA bloqueia",
                       {**d04, "texto_revisado": True}, "story", True))

    print(f"\n{sum(r)}/{len(r)} comportamentos corretos")
    return 0 if all(r) else 1


def _passa(item, kind):
    try:
        publish._cfm_guard(item, kind)
        return True
    except RuntimeError:
        return False


if __name__ == "__main__":
    sys.exit(main())
