# -*- coding: utf-8 -*-
"""
LINT CFM — roda os guardrails compartilhados (cfm_guardrails.auditar) sobre TODO o conteúdo:
  - EPISODES (roteiros narrados): legenda (contexto público, exige assinatura) + texto das cenas.
  - Bibliotecas PUBLICADAS: reels.json, posts.json, sequences.json, stories.json (legendas).
Saída: lista de VIOLACAO (proibido) e REVISAR (conferir contexto). Idempotente, só leitura.
Rodar: python checar_cfm.py   (use PYTHONIOENCODING=utf-8 no Windows).
Vira gate de publicação: 0 VIOLACAO é o alvo.

COBERTURA ADITIVA (ADVISORY, não bloqueia): auditar_seo_youtube() roda os mesmos guardrails
sobre os metadados PÚBLICOS do YouTube (seo_episodios.json — title/title_alt/description/tags),
que antes NÃO passavam por auditar(). É só AVISO: não entra nas VIOLACOES/BLOQUEIOS do gate IG
(o gate IG e a pipeline do YouTube são desacoplados por design do Rafael).
"""
import json
import os
from cfm_guardrails import auditar

ROOT = os.path.dirname(os.path.abspath(__file__))


def texto_cenas(ep):
    partes = []
    for sc in ep.get("scenes", []):
        partes += [sc.get("k", "")] + sc.get("sc", []) + [sc.get("sub", ""), sc.get("vo", "")]
    return " ".join(p for p in partes if p)


def auditar_seo_youtube(caminho=None):
    """ADVISORY (aditivo) — fecha a brecha de cobertura: os metadados PÚBLICOS do YouTube
    gerados pelo motor SEO v2 (seo_episodios.json: title/title_alt/description/tags por entrada)
    NÃO passavam por cfm_guardrails.auditar. Aqui rodamos os MESMOS guardrails sobre eles:
      - title, title_alt, description  -> contexto 'publico'
      - tags (juntas)                  -> contexto 'mensagem'
    Só REPORTA (não bloqueia). Ver comentário no gate: promover isto a blocking — ou plugar
    o guardrail DENTRO da publicação do YouTube (_cfm_guard) — é decisão do Rafael.

    fail-open RUIDOSO: se seo_episodios.json não existir ou falhar o load, imprime AVISO e
    segue (retorna listas vazias) — NUNCA trava o gate.

    Retorna (violacoes, revisar): cada item = (origem, id, severidade, regra, detalhe).
    """
    violacoes = []
    revisar = []
    if caminho is None:
        caminho = os.path.join(ROOT, "seo_episodios.json")

    if not os.path.exists(caminho):
        print(f"AVISO: SEO YouTube advisory — {os.path.basename(caminho)} nao encontrado; pulando (fail-open).")
        return violacoes, revisar

    try:
        dados = json.load(open(caminho, encoding="utf-8"))
    except Exception as e:
        print(f"AVISO: SEO YouTube advisory — falha ao carregar {os.path.basename(caminho)}: {e} (fail-open).")
        return violacoes, revisar

    # aceita dict {id: entrada} (formato atual do motor v2) ou lista de entradas
    if isinstance(dados, dict):
        entradas = list(dados.items())
    elif isinstance(dados, list):
        entradas = [(e.get("id", "?") if isinstance(e, dict) else "?", e) for e in dados]
    else:
        print("AVISO: SEO YouTube advisory — formato inesperado de seo_episodios.json (fail-open).")
        return violacoes, revisar

    n = 0
    for _id, ent in entradas:
        if not isinstance(ent, dict):
            continue
        n += 1
        # title / title_alt / description: metadados públicos -> contexto 'publico'
        for campo in ("title", "title_alt", "description"):
            txt = ent.get(campo, "")
            if not txt:
                continue
            for sev, regra, det in auditar(txt, "publico"):
                # a regra 'assinatura' é irrelevante p/ title/tag/description do YT (assinatura vai no rodapé
                # do vídeo, não nos metadados) — não conta como aviso relevante desta cobertura.
                if regra == "assinatura":
                    continue
                alvo = violacoes if sev == "VIOLACAO" else revisar
                alvo.append((f"seo_yt:{campo}", _id, sev, regra, det))
        # tags juntas: contexto 'mensagem' (não exige assinatura)
        tags = ent.get("tags")
        if isinstance(tags, list) and tags:
            texto_tags = " ".join(str(t) for t in tags)
        elif isinstance(tags, str):
            texto_tags = tags
        else:
            texto_tags = ""
        if texto_tags:
            for sev, regra, det in auditar(texto_tags, "mensagem"):
                alvo = violacoes if sev == "VIOLACAO" else revisar
                alvo.append(("seo_yt:tags", _id, sev, regra, det))

    print(f"SEO YouTube auditado (advisory): {n} entradas")
    return violacoes, revisar


def main(seo_advisory_inline=True):
    """seo_advisory_inline=True imprime o bloco advisory do SEO YouTube ao fim (uso standalone).
    O gate passa False e imprime seu próprio bloco [extra] para não duplicar."""
    violacoes = []   # (origem, id, severidade, regra, detalhe)
    revisar = []

    def registra(origem, _id, issues):
        for sev, regra, det in issues:
            (violacoes if sev == "VIOLACAO" else revisar).append((origem, _id, sev, regra, det))

    # 0) INTEGRIDADE DOS MODULOS DE EPISODIOS (fail-CLOSED) — P0 #2
    # episodios_pe_no_chao.py ESTENDE EPISODES importando 4 modulos, cada um num try/except
    # que apenas imprime "AVISO: ... nao carregado" e SEGUE (fail-open). Se o lag do OneDrive
    # ou um erro de sintaxe derrubar um desses modulos, aquele guard mascara a falha e o gate
    # imprimiria PASS com uma lista EPISODES AMPUTADA. Aqui importamos os 4 modulos DIRETAMENTE
    # (sem passar pelo try/except mascarador): se QUALQUER import propagar exceccao, registramos
    # como VIOLACAO (origem="episodios:import") — assim entra em `violacoes`, o gate soma em
    # `bloqueios` e o exit vira != 0. NUNCA passar em silencio com episodios faltando.
    # NAO edita episodios_pe_no_chao.py nem os modulos de episodios (so os importa).
    import importlib
    for _mod in ("episodios_novos_2026", "episodios_lote_julho_2026",
                 "episodio_apresentacao", "episodios_pos_op"):
        try:
            importlib.import_module(_mod)
        except Exception as e:
            registra("episodios:import", _mod,
                     [("VIOLACAO", "integridade_episodios",
                       f"falha ao importar modulo de episodios '{_mod}': "
                       f"{type(e).__name__}: {e} — EPISODES ficaria amputado (fail-closed)")])
            print(f"BLOQUEIO: modulo de episodios '{_mod}' NAO importou: {type(e).__name__}: {e}")

    # 1) EPISODES
    try:
        from episodios_pe_no_chao import EPISODES
        for ep in EPISODES:
            registra("episodio:legenda", ep["id"], auditar(ep.get("caption", ""), "publico"))
            registra("episodio:cenas", ep["id"], auditar(texto_cenas(ep), "mensagem"))
        print(f"EPISODES auditados: {len(EPISODES)}")
    except Exception as e:
        print("AVISO: nao carregou EPISODES:", e)

    # 1b) CARROSSEL.POSTS — fonte publica de 1a classe (P0 #3)
    # carrossel.POSTS e conteudo publico de legenda/tela (9 carrosseis) que ANTES nao passava
    # pelos guardrails CFM. Importar `carrossel` e SEGURO: o render (loop sobre POSTS / EXEMPLO)
    # vive dentro de atualizar_todos()/main-guard, entao um `import carrossel` NAO renderiza nada.
    # Falha ao importar carrossel -> registra em REVISAR (nao passar em silencio), sem travar o gate.
    # Auditamos kicker/title/sub/body de cada slide em contexto 'mensagem' (a assinatura CRM+RQE vai
    # no RODAPE do render, nao no texto — por isso a regra 'assinatura' e ignorada aqui). VIOLACAO
    # cai em `violacoes` (bloqueia via gate); o resto em `revisar` (avisa) — via a MESMA closure.
    try:
        from carrossel import POSTS
    except Exception as e:
        registra("carrossel:POSTS", "carrossel",
                 [("REVISAR", "import_carrossel",
                   f"nao foi possivel importar carrossel.POSTS: {type(e).__name__}: {e}")])
        print("AVISO: nao importou carrossel.POSTS:", e)
    else:
        # try/except PER-POST: um post malformado (nao-dict, slides nao-dict) vira REVISAR
        # isolado daquele post e NAO aborta a auditoria dos demais posts. VIOLACAO real de
        # qualquer post bem-formado segue caindo em `violacoes` (bloqueia via gate).
        n_slides = 0
        for post in POSTS:
            try:
                pid = post.get("id", "?")
                for s in post.get("slides", []):
                    n_slides += 1
                    for campo in ("kicker", "title", "sub", "body"):
                        txt = s.get(campo, "")
                        if not txt:
                            continue
                        issues = [(sev, regra, det) for sev, regra, det in auditar(txt, "mensagem")
                                  if regra != "assinatura"]
                        if issues:
                            registra(f"carrossel:{pid}", pid, issues)
            except Exception as e:
                pid = post.get("id", "?") if isinstance(post, dict) else "?"
                registra(f"carrossel:{pid}", pid,
                         [("REVISAR", "carrossel_post_malformado",
                           f"post malformado ignorado na auditoria CFM: {type(e).__name__}: {e}")])
                print(f"AVISO: post carrossel '{pid}' malformado, pulado:", e)
        print(f"carrossel.POSTS auditado: {len(POSTS)} posts / {n_slides} slides")

    # 2) Bibliotecas publicadas
    for arq in ["reels.json", "posts.json", "sequences.json", "stories.json"]:
        p = os.path.join(ROOT, arq)
        if not os.path.exists(p):
            continue
        try:
            d = json.load(open(p, encoding="utf-8"))
            itens = d if isinstance(d, list) else []
            n = 0
            for it in itens:
                cap = it.get("caption") if isinstance(it, dict) else None
                if cap:
                    registra(arq, it.get("id", "?"), auditar(cap, "publico"))
                    n += 1
            print(f"{arq}: {n} legendas auditadas")
        except Exception as e:
            print(f"AVISO: {arq}:", e)

    # Relatório
    print("\n=== LINT CFM ===")
    print("VIOLACOES (proibido — corrigir):", len(violacoes))
    for origem, _id, sev, regra, det in violacoes:
        print(f"   [VIOLACAO] {origem:22s} {str(_id):26s} {regra}: {det}")
    # REVISAR: agrupar por regra (costuma ter muito da 'assinatura' falso-positivo de cena)
    from collections import Counter
    porreg = Counter(r[3] for r in revisar)
    print("\nREVISAR (conferir contexto):", len(revisar), "->", dict(porreg))
    # mostra os REVISAR que NAO sao 'assinatura' (esses sao os que importam)
    relevantes = [r for r in revisar if r[3] != "assinatura"]
    for origem, _id, sev, regra, det in relevantes[:40]:
        print(f"   [REVISAR]  {origem:22s} {str(_id):26s} {regra}: {det}")

    # --- COBERTURA ADITIVA (ADVISORY): metadados públicos do YouTube (seo_episodios.json) ---
    # Fecha a brecha em que title/title_alt/description/tags do motor SEO v2 NÃO passavam
    # pelos guardrails CFM. Reporta SOMENTE — NÃO entra nas VIOLACOES/BLOQUEIOS do gate IG.
    # Só imprime aqui quando NÃO for o gate a chamar (o gate imprime seu próprio bloco [extra]),
    # para evitar duplicação. Ao rodar `python checar_cfm.py` direto, mostra o advisory.
    if seo_advisory_inline:
        seo_viol, seo_rev = auditar_seo_youtube()
        imprimir_seo_advisory(seo_viol, seo_rev)

    return violacoes, revisar


def imprimir_seo_advisory(seo_viol, seo_rev):
    """Imprime o bloco ADVISORY da cobertura SEO YouTube (não afeta exit/bloqueios)."""
    print("\n--- SEO YouTube (CFM advisory — NAO bloqueia) ---")
    print(f"VIOLACAO={len(seo_viol)}  REVISAR={len(seo_rev)}")
    for origem, _id, sev, regra, det in seo_viol:
        print(f"   [VIOLACAO] {origem:16s} {str(_id):26s} {regra}: {det}")
    for origem, _id, sev, regra, det in seo_rev[:40]:
        print(f"   [REVISAR]  {origem:16s} {str(_id):26s} {regra}: {det}")


if __name__ == "__main__":
    main()
