#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
checar_entretenimento.py — portão da GERAÇÃO NOVA (episodios_entretenimento.py + as entradas
dela em reels.json). Roda no CI (ci-testes.yml) e ANTES de cada publicação (publish.yml). Não
importa skia: roda em runner leve.

O que reprova (exit 1):
  1. Episódio mal formado (campos, tamanhos, conversa começando pelo paciente, CTA que não pede
     ENVIO a alguém — "Manda um direct" não passa).
  2. Qualquer texto do episódio (tela, voz, legenda, CTA da legenda, rótulos de tela) com VIOLAÇÃO CFM.
  3. Entrada da fila de um episódio da geração nova (achada pelo `formato` OU pelo id) com:
     formato ausente/divergente; vídeo que não é reels/_preview_<id>.mp4 ou não existe; legenda
     diferente da gerada do episódio aprovado (troca de texto sem reaprovação); sem `voz_ia: true`
     E sem a linha "voz digital (IA)" (as duas: uma liga o rótulo da Meta, a outra é a declaração
     da legenda); `scenes` diferente do texto do episódio (o portão CFM do publish lê `scenes`).
  4. Vídeo não amarrado ao texto: o arquivo-irmão reels/_preview_<id>.json (gravado pelo render)
     falta, foi gerado de OUTRO texto (hash do episódio) ou de outro motor (hash dos módulos de
     animado/ usados), ou registra texto desenhado na tela que não está no episódio.
  5. id repetido na fila; universo vazio (nenhum episódio) — vazio não é aprovação.
Os 4 FORMATOS NOVOS de vídeo (regra_reels.FORMATOS_NOVOS: qual_dos_dois, mito_na_prova, camera_lenta, chama_o_var —
Rafael, 24-26/10/2026) têm as MESMAS exigências do COMO FUNCIONA: cena com módulo, roteiro de 50-95 palavras
terminando na CTA de envio, `tela`, vídeo + irmão amarrados ao texto, legenda gerada do episódio, voz de IA declarada.

Uso:
  python checar_entretenimento.py              # confere
  python checar_entretenimento.py --auto-teste # prova que cada checagem reprova de verdade
"""
import ast
import copy
import hashlib
import json
import os
import re
import sys

# reconfigure (e nao um TextIOWrapper novo): quem importa este modulo ja pode ter
# embrulhado o stdout, e o embrulho antigo, ao ser coletado, FECHA o buffer — o
# render de 19/10 perdeu 3 videos prontos com "I/O operation on closed file".
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
ANIMADO = os.path.join(ROOT, "animado")

import regra_reels  # noqa: E402  (fonte única dos nomes dos formatos; não importa nada pesado)

# conversa + COMO FUNCIONA + os 4 formatos novos (Rafael, 24-26/10/2026). Os formatos novos são "COMO FUNCIONA com
# outra mecânica": passam pelo MESMO ramo de checagem (cena, roteiro, tela) — só a conversa tem ramo próprio.
FORMATOS = {"conversa", "como_funciona", *regra_reels.FORMATOS_NOVOS}
SIG = "Dr. Rafael Vargas · Médico · CRM-SP 226103 · RQE 137901"
DISC = "Conteúdo educativo · não substitui avaliação médica · voz digital (IA)"
TAIL_IA = "Narração com voz digital (IA)."
# texto de interface que toda peça desenha (identificação CFM, selo, estado do contato)
TELA_GENERICA = {SIG, DISC, "Dr. Rafael Vargas · Médico ortopedista", "CRM-SP 226103 · RQE 137901 · @rafaelvargasmd",
                 "COMO FUNCIONA", "digitando…", "falando…", "online"}
_PONT = re.compile(r"[.,:;!?—…\"“”()]")


def _icones_do_pacote():
    """Chaves do dict ICONES de animado/icones.py, lidas por AST (o CI leve não tem skia).
    Lista à mão dessincronizava: ícone novo desenhado e o portão ainda recusando."""
    arv = ast.parse(open(os.path.join(ANIMADO, "icones.py"), encoding="utf-8").read())
    for no in arv.body:
        if isinstance(no, ast.Assign) and any(getattr(t, "id", "") == "ICONES" for t in no.targets):
            return {k.value for k in no.value.keys}
    raise SystemExit("ERRO: animado/icones.py sem o dict ICONES — portão cego, não aprova nada.")


def _cenas_do_pacote():
    """Cena de COMO FUNCIONA = módulo animado/cf_<nome>.py que define `render` no nível de cima
    (def ou atribuição). cf_comum.py e afins, sem `render`, não são cena."""
    cenas = set()
    for f in os.listdir(ANIMADO):
        if not (f.startswith("cf_") and f.endswith(".py")):
            continue
        arv = ast.parse(open(os.path.join(ANIMADO, f), encoding="utf-8").read())
        for no in arv.body:
            if (isinstance(no, ast.FunctionDef) and no.name == "render") or (
                    isinstance(no, ast.Assign) and any(getattr(t, "id", "") == "render" for t in no.targets)):
                cenas.add(f[:-3]); break
    return cenas


ICONES = _icones_do_pacote()
CENAS = _cenas_do_pacote()


# ------------------------------------------------------------------ derivações do episódio
def textos(ep):
    """Toda superfície de texto do episódio (tela, voz, legenda) — o que o CFM audita."""
    t = list(ep.get("gancho", [])) + [f.get("texto", "") for f in ep.get("falas", [])] + list(ep.get("roteiro", []))
    t += list(ep.get("tela", []))
    return [x for x in t + [ep.get("cta", ""), ep.get("cta_legenda", ""), ep.get("legenda", ""),
                            ep.get("personagem", "")] if x]


def cenas_de(ep):
    """O texto que vai em reels.json -> scenes, que é o que os portões CFM do publish (publish._cfm_guard
    e checar_cfm.py) auditam: a fala E o texto escrito na tela (gancho, personagem, rótulos `tela`).
    Antes só a fala ia; o gancho em 86 pt ficava fora do backstop de publicação (auditoria 19/10)."""
    tela = [{"tela": s} for s in list(ep.get("gancho", [])) + ([ep["personagem"]] if ep.get("personagem") else [])
            + list(ep.get("tela", []))]
    if ep["formato"] == "conversa":
        return [{"quem": f["quem"], "vo": f["texto"]} for f in ep["falas"]] + [{"quem": "F", "vo": ep["cta"]}] + tela
    return [{"vo": s} for s in ep["roteiro"]] + tela


def legenda_de(ep):
    """A legenda que a fila TEM de ter para este episódio (o anexar grava exatamente isto)."""
    import legenda
    legenda.CTA_POR_ID[ep["id"]] = ep.get("cta_legenda") or ep["cta"]
    return legenda.normalizar(f"{ep['legenda']}\n\n{TAIL_IA}", "reel", ep["id"], fam=ep["familia"])


def video_de(ep):
    return f"reels/_preview_{ep['id']}.mp4"


def sidecar_de(ep):
    return f"reels/_preview_{ep['id']}.json"


def hash_episodio(ep):
    from checar_aprovacoes import hash_canonico
    return hash_canonico(ep)


def modulos_do_motor(ep):
    """Módulos de animado/ que produzem o vídeo do episódio: o de entrada (conversa ou a cena) e
    tudo o que ele importa de dentro do pacote, transitivamente (lido por AST)."""
    pend = ["conversa" if ep["formato"] == "conversa" else ep["cena"]]; vistos = set()
    while pend:
        m = pend.pop()
        if m in vistos or not os.path.exists(os.path.join(ANIMADO, m + ".py")):
            continue
        vistos.add(m)
        arv = ast.parse(open(os.path.join(ANIMADO, m + ".py"), encoding="utf-8").read())
        for no in ast.walk(arv):
            if isinstance(no, ast.ImportFrom) and no.level == 1:
                pend += [no.module] if no.module else [a.name for a in no.names]
    return sorted(vistos)


def hash_motor(ep):
    h = hashlib.sha256()
    for m in modulos_do_motor(ep):
        h.update(m.encode() + b"\0")
        h.update(open(os.path.join(ANIMADO, m + ".py"), "rb").read().replace(b"\r\n", b"\n"))
    return "sha256:" + h.hexdigest()


def _norm(w):
    return _PONT.sub("", w).strip().lower()


def tela_fora_do_episodio(ep, desenhados):
    """Textos desenhados que o episódio não contém. Frase/rótulo: tem de estar em `tela`, no
    gancho, no personagem ou na interface genérica. Palavra solta (legenda karaokê, balões da
    conversa): tem de ser palavra do texto falado/escrito do episódio."""
    explicito = set(ep.get("tela", [])) | set(ep.get("gancho", [])) | {ep.get("personagem", "")} | TELA_GENERICA
    palavras = set()
    for s in [f["texto"] for f in ep.get("falas", [])] + list(ep.get("roteiro", [])) + [ep.get("cta", "")]:
        palavras |= {_norm(w) for w in s.split()}
    return sorted(s for s in desenhados
                  if s not in explicito and not (len(s.split()) == 1 and _norm(s) in palavras))


def cta_ok(cta):
    import legenda
    return legenda.cta_de_envio(cta)


# ------------------------------------------------------------------ checagens
def checar_episodio(ep):
    p = []
    f = ep.get("formato")
    if f not in FORMATOS:
        return [f"formato inválido {f!r}"]
    for campo in ("id", "serie", "familia", "cta", "legenda"):
        if not ep.get(campo):
            p.append(f"falta {campo}")
    if ep.get("familia") not in ("reconstrucao", "pediatria"):
        p.append("familia tem de ser reconstrucao|pediatria")
    for campo in ("cta", "cta_legenda"):
        if campo in ep and not cta_ok(str(ep.get(campo, ""))):
            p.append(f"{campo} tem de pedir ENVIO a alguém ('Manda pra quem…'), sem contato/agenda: {ep.get(campo)!r}")
    g = ep.get("gancho", [])
    if len(g) != 2 or any(len(x) > 24 for x in g):
        p.append("gancho = 2 linhas de até 24 caracteres")
    if f == "conversa":
        if ep.get("icone") not in ICONES:
            p.append(f"icone {ep.get('icone')!r} fora de {sorted(ICONES)}")
        falas = ep.get("falas", [])
        if not falas or falas[0].get("quem") != "P":
            p.append("a conversa começa pelo paciente (P)")
        for a, b in zip(falas, falas[1:]):
            if a.get("quem") == b.get("quem"):
                p.append("falas P/F têm de alternar"); break
        for x in falas:
            lim = 50 if x.get("quem") == "P" else 110
            if len(x.get("texto", "")) > lim:
                p.append(f"fala {x.get('quem')} com {len(x['texto'])} caracteres (máx {lim}): {x['texto'][:40]!r}")
        if len(ep.get("cta", "")) > 60:
            p.append("CTA longa demais (máx 60)")
    else:
        if ep.get("cena") not in CENAS:
            p.append(f"cena {ep.get('cena')!r} sem módulo conhecido {sorted(CENAS)}")
        rot = ep.get("roteiro", [])
        if not rot or rot[-1] != ep.get("cta"):
            p.append("a última frase do roteiro tem de ser a CTA")
        n = sum(len(s.split()) for s in rot)
        if not 50 <= n <= 95:
            p.append(f"roteiro com {n} palavras (faixa 50-95)")
        tela = ep.get("tela")
        if not isinstance(tela, list) or any(not isinstance(x, str) or not x or len(x) > 40 for x in tela):
            p.append("tela = lista dos rótulos que a cena desenha (texto de até 40 caracteres)")
    from cfm_guardrails import auditar
    for s in textos(ep):
        for sev, regra, det in auditar(f"{s} · {SIG}", contexto="publico"):
            if sev == "VIOLACAO":
                p.append(f"CFM {regra}: {det} — {s[:50]!r}")
    return p


def _ler_sidecar_disco(rel):
    c = os.path.join(ROOT, rel.replace("/", os.sep))
    if not os.path.exists(c):
        return None
    with open(c, encoding="utf-8") as f:
        return json.load(f)


def _existe_disco(rel):
    return os.path.exists(os.path.join(ROOT, rel.replace("/", os.sep)))


def checar_fila(eps, reels, ler_sidecar=_ler_sidecar_disco, existe=_existe_disco):
    import legenda
    p = []
    por_id = {e["id"]: e for e in eps}
    ids = [it.get("id") for it in reels]
    for d in sorted({i for i in ids if ids.count(i) > 1}):
        p.append(f"{d}: id repetido na fila ({ids.count(d)}x) — a agenda mostraria peça que não sai")
    for it in reels:
        f = it.get("formato"); iid = it.get("id")
        if not f and iid not in por_id:
            continue                                  # lâmina antiga: fora deste portão
        if f and f not in FORMATOS:
            p.append(f"{iid}: formato {f!r} desconhecido"); continue
        ep = por_id.get(iid)
        if not ep:
            p.append(f"{iid}: entrada de formato novo SEM episódio em episodios_entretenimento.py"); continue
        if f != ep["formato"]:
            p.append(f"{iid}: formato da fila ({f!r}) diverge do episódio ({ep['formato']}) — sem ele a peça "
                     f"cairia na cota de lâminas e escaparia deste portão")
        if it.get("video") != video_de(ep):
            p.append(f"{iid}: vídeo {it.get('video')!r} não é o do episódio ({video_de(ep)})")
        elif not existe(it["video"]):
            p.append(f"{iid}: vídeo {it.get('video')!r} NÃO existe no repo — publicar falharia")
        cap = it.get("caption", "")
        for v in legenda.validar(cap, "reel"):
            p.append(f"{iid}: legenda — {v}")
        try:
            if cap != legenda_de(ep):
                p.append(f"{iid}: legenda da fila diverge da gerada do episódio aprovado — refaça com animado.anexar")
        except ValueError as x:
            p.append(f"{iid}: a legenda do episódio não normaliza ({x})")
        if it.get("voz_ia") is not True or "voz digital (ia)" not in cap.lower():
            p.append(f"{iid}: declaração de IA incompleta (exige voz_ia: true, que liga o rótulo da Meta, E a "
                     f"linha 'voz digital (IA)' na legenda)")
        if it.get("scenes") != cenas_de(ep):
            p.append(f"{iid}: `scenes` diverge do texto do episódio — o portão CFM leria outra coisa")
        sc = ler_sidecar(sidecar_de(ep))
        if sc is None:
            p.append(f"{iid}: falta {sidecar_de(ep)} — vídeo sem prova de qual texto o gerou (re-renderize)")
            continue
        if sc.get("hash_episodio") != hash_episodio(ep):
            p.append(f"{iid}: o vídeo foi renderizado de OUTRO texto (hash do episódio mudou) — re-renderize")
        if sc.get("hash_motor") != hash_motor(ep):
            p.append(f"{iid}: o motor (animado/{', '.join(modulos_do_motor(ep))}) mudou depois do render — re-renderize")
        fora = tela_fora_do_episodio(ep, sc.get("textos_tela") or [])
        if fora:
            p.append(f"{iid}: texto desenhado na tela fora do episódio: {fora[:6]}")
        if not sc.get("textos_tela"):
            p.append(f"{iid}: o render não registrou o texto desenhado — prova ausente")
    return p


def checar_declaracao_ia(reels, publicados):
    """TODO reel pendente (geração nova OU lâmina) declara a voz explicitamente e de forma coerente:
    `voz_ia` booleano E a linha "voz digital (IA)" na legenda se e só se voz_ia for verdadeiro.
    Auditoria 19/10: 16 lâminas narradas pelo Antonio (lote julho) estavam na fila sem nenhum dos
    dois — sairiam sem o rótulo de IA que a Meta exige, e nenhum portão olhava lâmina."""
    p = []
    for it in reels:
        iid = it.get("id")
        if iid in publicados:
            continue
        v = it.get("voz_ia"); marca = "voz digital (ia)" in (it.get("caption") or "").lower()
        if not isinstance(v, bool):
            p.append(f"{iid}: reel pendente sem voz_ia explícito (true/false) — não saber se tem voz não é não ter voz")
        elif v != marca:
            p.append(f"{iid}: declaração de IA incoerente: voz_ia={v} mas a legenda {'tem' if marca else 'NÃO tem'} "
                     f"'voz digital (IA)'")
    return p


def conferir(eps=None, reels=None, verbose=True, publicados=None, **kw):
    if eps is None:
        from episodios_entretenimento import EPISODIOS_ENTRETENIMENTO as eps
    if reels is None:
        reels = json.load(open(os.path.join(ROOT, "reels.json"), encoding="utf-8-sig"))
    probs = []
    if not eps:
        probs.append("universo VAZIO: nenhum episódio — vazio não é aprovação")
    ids = [e.get("id") for e in eps]
    if len(ids) != len(set(ids)):
        probs.append("id de episódio duplicado")
    for e in eps:
        probs += [f"{e.get('id')}: {x}" for x in checar_episodio(e)]
    probs += checar_fila(eps, reels, **kw)
    if publicados is None:
        publicados = {e["id"] for e in json.load(open(os.path.join(ROOT, "state", "published.json"),
                                                      encoding="utf-8"))["published"]}
    probs += checar_declaracao_ia(reels, publicados)
    if verbose:
        novos = [r for r in reels if r.get("formato") or r.get("id") in set(ids)]
        print(f"episódios: {len(eps)} | na fila da geração nova: {len(novos)} | problemas: {len(probs)}")
        for x in probs:
            print("  -", x)
    return probs


# ------------------------------------------------------------------ auto-teste
def _entrada_valida(ep):
    """Entrada exatamente como o animado.anexar monta (sem medir mp4)."""
    return {"id": ep["id"], "video": video_de(ep), "caption": legenda_de(ep), "formato": ep["formato"],
            "serie": ep["serie"], "dur": 30.0, "voz_ia": True, "scenes": cenas_de(ep)}


def _sidecar_valido(ep):
    tela = list(ep.get("tela", [])) + list(ep.get("gancho", [])) + [SIG, DISC]
    palavras = [w.upper() for w in (ep.get("roteiro") or [f["texto"] for f in ep["falas"]])[0].split()]
    return {"id": ep["id"], "hash_episodio": hash_episodio(ep), "hash_motor": hash_motor(ep),
            "textos_tela": tela + palavras}


def _render_despacha(ep):
    """Para onde o animado/render.py despacha o episódio — sem desenhar nada nem importar skia: o import da cena é
    interceptado e o portão CFM (testado à parte) fica de fora. -> 'cena:animado.<cena>' | 'recusou:<mensagem>'."""
    import shutil
    import tempfile
    import types
    from animado import render as R

    class _Despachou(Exception):
        pass

    def _importar(nome):
        raise _Despachou(nome)

    salvo = (sys.argv, R.episodio, R.portao_cfm, R.importlib)
    tmp = tempfile.mkdtemp(prefix="render_despacho_")
    try:
        sys.argv = ["render", ep["id"], "--previa", "--tmp", tmp]
        R.episodio, R.portao_cfm = (lambda _id: ep), (lambda _ep: None)
        R.importlib = types.SimpleNamespace(import_module=_importar)
        try:
            R.main()
        except _Despachou as e:
            return f"cena:{e.args[0]}"
        except SystemExit as e:
            return f"recusou:{e.code}"
        return "nada"
    finally:
        sys.argv, R.episodio, R.portao_cfm, R.importlib = salvo
        shutil.rmtree(tmp, ignore_errors=True)


def auto_teste():
    from episodios_entretenimento import EPISODIOS_ENTRETENIMENTO as reais
    reels = json.load(open(os.path.join(ROOT, "reels.json"), encoding="utf-8-sig"))
    # lâminas sintéticas (a fila real pode estar em edição): uma narrada e declarada, uma muda
    antigas = [{"id": "t_lam_ia", "caption": "x\n\nNarração com voz digital (IA).", "voz_ia": True},
               {"id": "t_lam_muda", "caption": "x", "voz_ia": False}]
    conv = next(e for e in reais if e["formato"] == "conversa")
    cf = next(e for e in reais if e["formato"] == "como_funciona")
    # um episódio sintético de CADA formato novo (cópia de um COMO FUNCIONA real com o formato trocado): o portão tem
    # de aceitá-los com as mesmas exigências — e recusar o mesmo que recusa no COMO FUNCIONA (controles abaixo)
    novos = [dict(copy.deepcopy(cf), id=f"t_{f}", formato=f) for f in regra_reels.FORMATOS_NOVOS]
    base = list(reais) + novos
    nv = novos[0]
    validas = [_entrada_valida(conv), _entrada_valida(cf)] + [_entrada_valida(e) for e in novos]
    sidecars = {sidecar_de(e): _sidecar_valido(e) for e in [conv, cf] + novos}
    k_nv = 2                                       # posição da entrada de `nv` em `validas`

    def rodar(eps=base, fila=None, side=None, existe=lambda rel: True, lam=None, publicados=frozenset()):
        side = sidecars if side is None else side
        return conferir(eps, (antigas if lam is None else lam) + (validas if fila is None else fila), verbose=False,
                        ler_sidecar=lambda rel: copy.deepcopy(side.get(rel)), existe=existe, publicados=set(publicados))

    ok = True
    pr = rodar()
    print(f"[{'ok' if not pr else 'FALHOU'}] negativo: entradas VÁLIDAS (montadas como o anexar) passam — conversa, "
          f"COMO FUNCIONA e os {len(novos)} formatos novos ({pr[:2]})")
    ok &= not pr
    falta = [f for f in regra_reels.FORMATOS_NOVOS if f not in FORMATOS]
    print(f"[{'ok' if not falta else 'FALHOU'}] os formatos novos da regra única estão em FORMATOS ({falta or 'todos'})")
    ok &= not falta
    # o RENDER (animado/render.py, rodado pelo render-animado.yml) despacha os formatos novos para a cena, como o COMO
    # FUNCIONA — sem isso nenhuma peça de formato novo ganhava vídeo + irmão e as vagas de ter/qui/sáb ficavam vazias
    # (verificação de 26/10/2026). Controle positivo: formato digitado errado é RECUSADO pelo render.
    desp = {f: _render_despacha(dict(cf, formato=f)) for f in ("como_funciona",) + tuple(regra_reels.FORMATOS_NOVOS)}
    errado = {f: d for f, d in desp.items() if d != f"cena:animado.{cf['cena']}"}
    print(f"[{'ok' if not errado else 'FALHOU'}] o render despacha COMO FUNCIONA e os {len(regra_reels.FORMATOS_NOVOS)} "
          f"formatos novos para animado/<cena>.py ({errado or 'todos'})")
    ok &= not errado
    d = _render_despacha(dict(cf, formato="qual_dos_2"))
    acertou = d.startswith("recusou:") and "formato desconhecido" in d
    print(f"[{'ok' if acertou else 'FALHOU'}] positivo: o render RECUSA formato desconhecido ('qual_dos_2') -> {d[:70]}")
    ok &= acertou
    # render.py fora do hash do motor: mexer nele não invalida vídeo aprovado (o irmão guarda só os módulos da cena)
    no_motor = [e["id"] for e in reais if "render" in modulos_do_motor(e)]
    print(f"[{'ok' if not no_motor else 'FALHOU'}] render.py fora do hash do motor de todos os {len(reais)} episódios "
          f"({no_motor[:3] or 'nenhum o inclui'})")
    ok &= not no_motor
    pr = rodar(lam=antigas + [{"id": "t_lam_velha", "caption": "x"}], publicados={"t_lam_velha"})
    print(f"[{'ok' if not pr else 'FALHOU'}] negativo: reel JÁ publicado sem voz_ia não reprova ({pr[:2]})")
    ok &= not pr

    def ep_mut(fn):
        e = copy.deepcopy(base); fn(e); return e

    def fila_mut(fn, k=0):
        f = copy.deepcopy(validas); fn(f[k]); return f

    def side_mut(fn, ep=cf):
        s = copy.deepcopy(sidecars); fn(s[sidecar_de(ep)]); return s

    def ep_nv(fn):
        return ep_mut(lambda e: fn(next(x for x in e if x["id"] == nv["id"])))

    casos = [
        ("termo vetado na legenda", 'CFM', dict(eps=ep_mut(lambda e: e[0].__setitem__("legenda", e[0]["legenda"] + " Corrige a dismetria.")))),
        ("conversa começando pelo personagem", 'começa pelo paciente', dict(eps=ep_mut(lambda e: next(x for x in e if x["id"] == conv["id"])["falas"].insert(0, {"quem": "F", "texto": "oi"})))),
        ("CTA sem pedido de envio", 'pedir ENVIO', dict(eps=ep_mut(lambda e: e[0].__setitem__("cta", "Curta e compartilhe.")))),
        ("CTA 'Manda um direct pra agendar'", 'pedir ENVIO', dict(eps=ep_mut(lambda e: next(x for x in e if x["id"] == conv["id"]).__setitem__("cta", "Manda um direct pra agendar.")))),
        ("ícone que o pacote não desenha", 'icone', dict(eps=ep_mut(lambda e: next(x for x in e if x["id"] == conv["id"]).__setitem__("icone", "skate")))),
        ("rótulo de tela com termo vetado", 'CFM', dict(eps=ep_mut(lambda e: next(x for x in e if x["id"] == cf["id"])["tela"].append("CORRIGE A DISMETRIA")))),
        ("universo vazio", 'VAZIO', dict(eps=[])),
        ("scenes diferente do episódio", '`scenes`', dict(fila=fila_mut(lambda it: it["scenes"].append({"vo": "outra coisa"})))),
        ("voz_ia ausente (legenda com a linha)", 'incompleta', dict(fila=fila_mut(lambda it: it.__setitem__("voz_ia", False)))),
        ("linha de IA tirada da legenda (voz_ia true)", 'incompleta', dict(fila=fila_mut(lambda it: it.__setitem__("caption", it["caption"].replace(TAIL_IA, ""))))),
        ("peça nova declarada SEM voz (voz_ia false, sem a linha)", 'incompleta', dict(fila=fila_mut(lambda it: (it.__setitem__("voz_ia", False), it.__setitem__("caption", it["caption"].replace(TAIL_IA, "")))))),
        ("legenda trocada em UMA palavra", 'legenda da fila diverge', dict(fila=fila_mut(lambda it: it.__setitem__("caption", it["caption"].replace("fixador", "aparelho", 1))))),
        ("vídeo de outro episódio", 'não é o do episódio', dict(fila=fila_mut(lambda it: it.__setitem__("video", "reels/_preview_cv_muleta.mp4")))),
        ("mp4 inexistente", 'NÃO existe', dict(existe=lambda rel: False)),
        ("entrada do episódio SEM formato", 'formato da fila', dict(fila=fila_mut(lambda it: it.pop("formato")))),
        ("formato divergente", 'formato da fila', dict(fila=fila_mut(lambda it: it.__setitem__("formato", "como_funciona")))),
        ("id repetido na fila", 'id repetido', dict(fila=copy.deepcopy(validas) + [copy.deepcopy(validas[0])])),
        ("sidecar ausente", 'falta reels/', dict(side={})),
        ("vídeo renderizado de outro texto", 'OUTRO texto', dict(side=side_mut(lambda s: s.__setitem__("hash_episodio", "sha256:0")))),
        ("motor mudou depois do render", 'o motor', dict(side=side_mut(lambda s: s.__setitem__("hash_motor", "sha256:0")))),
        ("texto de tela fora do episódio ('DIA 40')", 'fora do episódio', dict(side=side_mut(lambda s: s["textos_tela"].append("DIA 40")))),
        ("lâmina pendente sem voz_ia", 'sem voz_ia explícito', dict(lam=[{"id": "t_l", "caption": "x"}])),
        ("lâmina voz_ia true sem a linha na legenda", 'incoerente', dict(lam=[{"id": "t_l", "caption": "x", "voz_ia": True}])),
        ("lâmina voz_ia false COM a linha na legenda", 'incoerente', dict(lam=[{"id": "t_l", "caption": "voz digital (IA).", "voz_ia": False}])),
        ("gancho fora das scenes (backstop CFM cego)", '`scenes`', dict(fila=fila_mut(lambda it: it.__setitem__("scenes", [x for x in it["scenes"] if "tela" not in x])))),
        ("render sem registro de texto", 'não registrou', dict(side=side_mut(lambda s: s.__setitem__("textos_tela", [])))),
        # formatos novos (26/10/2026): as MESMAS exigências do COMO FUNCIONA
        ("formato novo: CTA sem pedido de envio", 'pedir ENVIO', dict(eps=ep_nv(lambda x: x.__setitem__("cta", "Curta e compartilhe.")))),
        ("formato novo: roteiro sem terminar na CTA", 'última frase', dict(eps=ep_nv(lambda x: x["roteiro"].append("Mais uma frase.")))),
        ("formato novo: cena sem módulo", 'sem módulo', dict(eps=ep_nv(lambda x: x.__setitem__("cena", "cf_nao_existe")))),
        ("formato novo: termo vetado no rótulo de tela", 'CFM', dict(eps=ep_nv(lambda x: x["tela"].append("CORRIGE A DISMETRIA")))),
        ("formato novo digitado errado no episódio ('qual_dos_2')", 'formato inválido', dict(eps=ep_nv(lambda x: x.__setitem__("formato", "qual_dos_2")))),
        ("formato novo digitado errado na fila ('qual_dos_2')", 'desconhecido', dict(fila=fila_mut(lambda it: it.__setitem__("formato", "qual_dos_2"), k=k_nv))),
        ("formato novo na fila como 'como_funciona' (diverge do episódio)", 'formato da fila', dict(fila=fila_mut(lambda it: it.__setitem__("formato", "como_funciona"), k=k_nv))),
        ("formato novo na fila SEM formato", 'formato da fila', dict(fila=fila_mut(lambda it: it.pop("formato"), k=k_nv))),
        ("formato novo sem voz_ia (rótulo de IA da Meta desligado)", 'incompleta', dict(fila=fila_mut(lambda it: it.__setitem__("voz_ia", False), k=k_nv))),
        ("formato novo sem a linha de IA na legenda", 'incompleta', dict(fila=fila_mut(lambda it: it.__setitem__("caption", it["caption"].replace(TAIL_IA, "")), k=k_nv))),
        ("formato novo com legenda trocada (uma frase a mais)", 'legenda da fila diverge', dict(fila=fila_mut(lambda it: it.__setitem__("caption", it["caption"].replace("\n", " Sempre.\n", 1)), k=k_nv))),
        ("formato novo: vídeo de outro episódio", 'não é o do episódio', dict(fila=fila_mut(lambda it: it.__setitem__("video", "reels/_preview_cv_muleta.mp4"), k=k_nv))),
        ("formato novo: irmão do vídeo ausente", 'falta reels/', dict(side={k: v for k, v in sidecars.items() if k != sidecar_de(nv)})),
        ("formato novo: vídeo renderizado de outro texto", 'OUTRO texto', dict(side=side_mut(lambda s: s.__setitem__("hash_episodio", "sha256:0"), ep=nv))),
        ("formato novo: texto de tela fora do episódio", 'fora do episódio', dict(side=side_mut(lambda s: s["textos_tela"].append("DIA 40"), ep=nv))),
    ]
    for nome, chave, kw in casos:
        # cada controle tem de disparar A SUA checagem (mensagem com `chave`), não "algum problema":
        # senão uma checagem morta passa escondida atrás de outra que dispara junto
        pr = rodar(**kw)
        acertou = any(chave in x for x in pr)
        print(f"[{'ok' if acertou else 'FALHOU'}] positivo: {nome} -> {len(pr)} problema(s)"
              f"{'' if acertou else ' — CHECAGEM MORTA (esperava ' + repr(chave) + ')'}")
        ok &= acertou
    print("AUTO-TESTE:", "PASSOU" if ok else "REPROVOU — não confiar no portão")
    return 0 if ok else 1


def main():
    if "--auto-teste" in sys.argv:
        return auto_teste()
    return 1 if conferir() else 0


if __name__ == "__main__":
    sys.exit(main())
