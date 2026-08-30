#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MINUTA — checar_aprovacoes.py · Enforcement do gate de aprovação clínica (Aposta 3).

STATUS: RASCUNHO LOCAL · AGUARDA AVAL DO RAFAEL. Nada aqui toca o motor, a fila nem o repo.

O QUE FAZ
  Compara a fila (reels.json) com o registro de aprovações (aprovacoes.json) e REPROVA
  (exit 1) se qualquer item da fila não tiver aprovação registrada com hash conferido.
  "Item sem registro não entra em reels.json" — este script é o verificador; o bloqueio
  de escrita acontece nos pontos de integração descritos no fim deste docstring.

DESENHO CONTRA AS LIÇÕES DA CASA
  1. Guardrail que aprova por omissão = guardrail morto → o check NÃO VALE enquanto não
     provar que sabe reprovar: o modo --auto-teste roda controles POSITIVOS semeados
     (órfão na fila, hash adulterado, universo vazio, registro-minuta, item sem id) e exige exit 1 de
     cada um, além de controles negativos que exigem exit 0. Só depois de observar as
     reprovações ele grava a prova (checar_aprovacoes.selftest.json) amarrada ao sha256
     DESTE arquivo. Sem prova, ou com o script editado depois da prova, toda execução
     normal REPROVA mandando rodar --auto-teste de novo (uma autorização não cobre o
     script editado — vale também para o próprio verificador).
  2. Zero itens verificados = FALHA, não sucesso (ausência exige medir o universo).
  3. A mensagem de erro LISTA os ids órfãos (dado verificável, não prosa).
  4. A suíte olha o EXIT CODE real de subprocessos — nunca a redação da mensagem
     (asserta apenas códigos e a presença do id semeado, que é dado).
  5. Hash é dimensão obrigatória (--fontes é exigido): checar só presença esconderia o
     ramo "aprovou o texto A, publicou o texto B".
  6. Falhas são AGREGADAS e todas reportadas — nenhum filtro silencioso.
  7. Registro com MINUTA_AGUARDA_AVAL=true reprova SEMPRE: minuta nunca passa por
     aprovação (artefato errado vira evidência).

TAXONOMIA DE EXIT (robô que publica falha ALTO)
  0 = todos os itens do universo têm aprovação registrada e hash conferido (universo > 0)
  1 = REPROVADO (órfãos, hash divergente, universo vazio, registro-minuta, sem prova de
      auto-teste) — em CI isso derruba o job ANTES de publicar
  2 = erro de ambiente/uso (arquivo ausente, JSON inválido, argumento errado)

USO
  python checar_aprovacoes.py --fila reels.json --aprovacoes aprovacoes.json \
         --publicados state_published.json --fontes <dir dos episodios_*.py>
  python checar_aprovacoes.py --auto-teste          # roda os controles semeados e grava a prova
  python checar_aprovacoes.py --hash <id> --fontes <dir>   # hash canônico p/ registrar aprovação
  Universo padrão: ids de reels.json AINDA NÃO publicados (state_published.json);
  --tudo verifica a biblioteca inteira.

PLANO DE INTEGRAÇÃO (apenas descrito — o motor NÃO foi tocado nesta rodada)
  Onde os arquivos moram: raiz do repo de produção do motor Instagram, ao lado de
  reels.json: APROVACOES.md (humano) + aprovacoes.json (máquina) + este script.
  Três pontos de acoplamento, em ordem de entrada em vigor:
  (1) ENFILEIRAMENTO (gate primário): toda sessão/ferramenta que edita reels.json roda
      este check ANTES do commit do arquivo editado — item novo só entra se o check do
      arquivo resultante sair 0. Vale para humano e para script de fila.
  (2) CI (rede de segurança): passo no início do workflow de publicação (o job que chama
      publish.py), antes de qualquer chamada de API:
        - run: python checar_aprovacoes.py --fila reels.json --aprovacoes aprovacoes.json
               --publicados state_published.json --fontes .
      exit != 0 derruba o job VERMELHO antes de publicar. Sem retry, sem continue-on-error.
  (3) publish.py (defesa em profundidade, fase 2): chamada interna antes de next_item()
      escolher um reel — reprovação vira o mesmo caminho de "BLOQUEADO CFM" já existente
      (fila não anda sozinha; estado gravado; exit != 0).
  PRIMEIRA EXECUÇÃO REAL: vai REPROVAR (hoje 45 itens não publicados sem registro) — é o
  gate funcionando, não um bug. Caminhos de saída: (a) Rafael ratifica lotes no pacote de
  revisão e as entradas viram status "aprovado"; (b) para reel04–reel30 (formato junho,
  mudos), decisão explícita do Rafael num lote "LEGADO-PRE-GATE" assinado — nunca
  isenção silenciosa no código.
  MÉTRICA DE PROVA da Aposta 3: "check reprovou 1× no teste semeado antes de valer" —
  cumprida pelo --auto-teste (T1 é exatamente essa reprovação observada e gravada).

Env interno: CHECAR_APROVACOES_MODO_TESTE=1 é usado SÓ pelo harness do --auto-teste para
os subprocessos dos controles (pula a exigência de prova, senão o auto-teste não
conseguiria rodar antes de existir prova). Fora do harness o banner denuncia o modo.
"""

import argparse
import hashlib
import importlib
import io
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

EXIT_OK = 0
EXIT_REPROVADO = 1
EXIT_ERRO = 2

AQUI = os.path.dirname(os.path.abspath(__file__))
ME = os.path.abspath(__file__)
ARQ_PROVA = os.path.join(AQUI, "checar_aprovacoes.selftest.json")
ENV_TESTE = "CHECAR_APROVACOES_MODO_TESTE"


# ───────────────────────────── primitivas ─────────────────────────────

def sha256_arquivo(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(65536), b""):
            h.update(bloco)
    return h.hexdigest()


def hash_canonico(episodio):
    """sha256 do JSON canônico do dicionário do episódio (cobre vo, tela e caption)."""
    s = json.dumps(episodio, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(s.encode("utf-8")).hexdigest()


def carregar_json(caminho):
    with io.open(caminho, encoding="utf-8-sig") as f:  # JSONs da casa vêm com BOM
        return json.load(f)


def carregar_fontes(diretorio):
    """Importa episodios*.py do diretório e devolve {id: dict_do_episodio}.

    Varre variáveis de módulo que sejam listas de dicts com chave 'id'.
    Duplicata de id entre módulos: a primeira vence e a duplicata é reportada.
    Módulo que não importa NÃO derruba a varredura: vira erro reportado (alto),
    e os ids que dependiam dele reprovam por 'fonte não encontrada' — fail-closed.
    """
    episodios, duplicatas, erros = {}, [], []
    sys.path.insert(0, os.path.abspath(diretorio))
    try:
        nomes = sorted(n for n in os.listdir(diretorio)
                       if n.startswith(("episodios", "episodio_")) and n.endswith(".py"))
        for nome in nomes:
            try:
                mod = importlib.import_module(nome[:-3])
            except Exception as e:
                erros.append(f"{nome}: {type(e).__name__}: {e}")
                continue
            for valor in vars(mod).values():
                if isinstance(valor, list) and valor and all(
                        isinstance(e, dict) and "id" in e for e in valor):
                    for ep in valor:
                        if ep["id"] in episodios:
                            # O agregador (episodios_pe_no_chao.EPISODES) reexporta os MESMOS
                            # dicts dos módulos-fonte: identidade ou igualdade de conteúdo não
                            # é ambiguidade. Ambíguo é id repetido com CONTEÚDO divergente.
                            if episodios[ep["id"]] is ep or episodios[ep["id"]] == ep:
                                continue
                            duplicatas.append(ep["id"])
                        else:
                            episodios[ep["id"]] = ep
    finally:
        sys.path.pop(0)
    return episodios, duplicatas, erros


def indice_aprovados(registro):
    """{id: (lote, hash)} considerando SÓ lotes com status 'aprovado'."""
    indice = {}
    for lote in registro.get("lotes", []):
        if lote.get("status") != "aprovado":
            continue
        for ep in lote.get("episodios", []):
            indice.setdefault(ep.get("id"), (lote.get("lote", "?"), ep.get("hash_roteiro")))
    return indice


# ───────────────────────────── o check ─────────────────────────────

def checar(args):
    problemas = []

    # prova do auto-teste (o check não vale enquanto não provou que sabe reprovar)
    if os.environ.get(ENV_TESTE) == "1":
        print("[banner] MODO_TESTE ativo: exigência de prova suspensa SÓ para o harness "
              "do --auto-teste. Uma execução assim NUNCA vale como gate.")
    else:
        if not os.path.exists(ARQ_PROVA):
            problemas.append("SEM PROVA DE AUTO-TESTE: este check ainda não demonstrou que "
                             "sabe reprovar. Rode: python checar_aprovacoes.py --auto-teste")
        else:
            try:
                prova = carregar_json(ARQ_PROVA)
            except (ValueError, OSError):
                prova = {}
            if prova.get("script_sha256") != sha256_arquivo(ME):
                problemas.append("PROVA DE AUTO-TESTE INVÁLIDA: o script foi editado depois "
                                 "da prova (uma autorização não cobre o script editado). "
                                 "Rode --auto-teste de novo.")

    # cargas
    try:
        fila_bruta = carregar_json(args.fila)
    except OSError as e:
        print(f"ERRO de ambiente: fila ilegível ({e})"); return EXIT_ERRO
    except ValueError as e:
        print(f"ERRO de ambiente: fila com JSON inválido ({e})"); return EXIT_ERRO
    if not isinstance(fila_bruta, list):
        print("ERRO de ambiente: a fila deveria ser uma lista de itens"); return EXIT_ERRO

    try:
        registro = carregar_json(args.aprovacoes)
    except OSError as e:
        print(f"ERRO de ambiente: registro de aprovações ilegível ({e})"); return EXIT_ERRO
    except ValueError as e:
        print(f"ERRO de ambiente: registro com JSON inválido ({e})"); return EXIT_ERRO

    publicados = set()
    if args.publicados:
        try:
            estado = carregar_json(args.publicados)
            for p in estado.get("published", []):
                publicados.add(p["id"] if isinstance(p, dict) else p)
        except OSError as e:
            print(f"ERRO de ambiente: state_published ilegível ({e})"); return EXIT_ERRO
        except ValueError as e:
            print(f"ERRO de ambiente: state_published com JSON inválido ({e})"); return EXIT_ERRO

    try:
        fontes, duplicatas, erros_import = carregar_fontes(args.fontes)
    except OSError as e:
        print(f"ERRO de ambiente: diretório de fontes ilegível ({e})")
        return EXIT_ERRO
    for erro in erros_import:
        problemas.append(f"FONTE NÃO IMPORTOU (os ids dela reprovarão por fonte ausente): {erro}")
    for dup in duplicatas:
        problemas.append(f"FONTE AMBÍGUA: id '{dup}' definido em mais de um módulo de episódios")

    # universo
    ids_fila = [item.get("id") for item in fila_bruta]
    sem_id = [f"posição {i}" for i, id_ in enumerate(ids_fila)
              if not (isinstance(id_, str) and id_)]
    if sem_id:
        problemas.append(f"{len(sem_id)} ITEM(NS) DA FILA SEM CAMPO 'id' legível "
                         f"(fila malformada): " + ", ".join(sem_id))
    ids_fila = [i for i in ids_fila if isinstance(i, str) and i]
    universo = ids_fila if args.tudo else [i for i in ids_fila if i not in publicados]
    rotulo = "biblioteca inteira" if args.tudo else "itens ainda não publicados"
    if len(universo) == 0:
        problemas.append(f"UNIVERSO VAZIO: 0 itens verificados ({rotulo}). Zero verificados "
                         "= FALHA, não sucesso — confira --fila/--publicados/--tudo.")

    # registro-minuta nunca aprova
    if registro.get("MINUTA_AGUARDA_AVAL"):
        problemas.append("REGISTRO É MINUTA (MINUTA_AGUARDA_AVAL=true): aguarda aval do "
                         "Rafael; nenhum lote dele conta como aprovação.")
        indice = {}
    else:
        indice = indice_aprovados(registro)
        if not indice:
            problemas.append("REGISTRO SEM NENHUM LOTE 'aprovado': o gate não tem o que aceitar.")

    # órfãos + hashes
    orfaos, hash_ruim = [], []
    for id_ in universo:
        if id_ not in indice:
            orfaos.append(id_)
            continue
        lote, hash_registrado = indice[id_]
        if not hash_registrado:
            hash_ruim.append(f"{id_} (lote {lote}): aprovação registrada SEM hash — hash é obrigatório")
            continue
        ep = fontes.get(id_)
        if ep is None:
            hash_ruim.append(f"{id_} (lote {lote}): fonte do roteiro não encontrada em "
                             f"{args.fontes} — impossível conferir o hash")
            continue
        atual = hash_canonico(ep)
        if atual != hash_registrado:
            hash_ruim.append(f"{id_} (lote {lote}): hash divergente — aprovado "
                             f"{hash_registrado[:23]}…, fonte atual {atual[:23]}… "
                             "(a aprovação não cobre o roteiro editado)")

    if orfaos:
        problemas.append(f"{len(orfaos)} ITEM(NS) DA FILA SEM APROVAÇÃO REGISTRADA:\n    "
                         + "\n    ".join(sorted(orfaos)))
    for p in hash_ruim:
        problemas.append("HASH: " + p)

    # veredito
    print(f"Universo verificado: {len(universo)} item(ns) ({rotulo}); "
          f"aprovações válidas no registro: {len(indice)} id(s).")
    if problemas:
        print("\nREPROVADO — item sem registro não entra em reels.json. Motivos:")
        for i, p in enumerate(problemas, 1):
            print(f"  [{i}] {p}")
        return EXIT_REPROVADO
    print("OK: todos os itens do universo têm aprovação registrada e hash conferido.")
    return EXIT_OK


# ───────────────────────────── auto-teste semeado ─────────────────────────────

FIXTURE_EPS = '''# -*- coding: utf-8 -*-
# fixture do auto-teste de checar_aprovacoes.py — nunca publicar
EPS = [
 {"id": "ep_ok", "scenes": [{"k": "A", "vo": "controle negativo"}], "caption": "a"},
 {"id": "ep_hash_trocado", "scenes": [{"k": "B", "vo": "controle positivo de hash"}], "caption": "b"},
]
'''


def _roda(args_cli, env_extra=None):
    env = dict(os.environ)
    env[ENV_TESTE] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    if env_extra:
        env.update(env_extra)
    r = subprocess.run([sys.executable, ME] + args_cli,
                       capture_output=True, text=True, encoding="utf-8", env=env)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def auto_teste():
    """Controles semeados. O check só passa a valer depois que este harness OBSERVA as
    reprovações (exit 1) dos controles positivos e as aprovações (exit 0) dos negativos."""
    resultados = []
    falhas = []
    with tempfile.TemporaryDirectory() as tmp:
        fontes = os.path.join(tmp, "fontes")
        os.makedirs(fontes)
        with io.open(os.path.join(fontes, "episodios_fixture.py"), "w", encoding="utf-8") as f:
            f.write(FIXTURE_EPS)

        # hashes corretos vêm do PRÓPRIO caminho de CLI (valida --hash de quebra)
        rc, saida = _roda(["--hash", "ep_ok", "--fontes", fontes])
        if rc != 0:
            print("auto-teste ABORTADO: --hash ep_ok não rodou (exit %d)" % rc)
            return EXIT_REPROVADO
        hash_ok = saida.strip().splitlines()[-1].strip()
        rc, saida = _roda(["--hash", "ep_hash_trocado", "--fontes", fontes])
        if rc != 0:
            print("auto-teste ABORTADO: --hash ep_hash_trocado não rodou (exit %d)" % rc)
            return EXIT_REPROVADO

        def escreve(nome, obj):
            p = os.path.join(tmp, nome)
            with io.open(p, "w", encoding="utf-8") as f:
                json.dump(obj, f, ensure_ascii=False)
            return p

        def registro(lotes):
            return {"versao_schema": 1, "lotes": lotes}

        lote_ok = {"lote": "T-OK", "status": "aprovado",
                   "episodios": [{"id": "ep_ok", "hash_roteiro": hash_ok}]}

        fila_ok = escreve("fila_ok.json", [{"id": "ep_ok"}])
        fila_orfao = escreve("fila_orfao.json", [{"id": "ep_ok"}, {"id": "teste_semeado_sem_aval"}])
        fila_hash = escreve("fila_hash.json", [{"id": "ep_hash_trocado"}])
        fila_vazia = escreve("fila_vazia.json", [])
        fila_sem_id = escreve("fila_sem_id.json", [{"id": "ep_ok"}, {"caption": "item sem id"}])
        reg_ok = escreve("reg_ok.json", registro([lote_ok]))
        reg_hash_errado = escreve("reg_hash_errado.json", registro([
            {"lote": "T-HASH", "status": "aprovado",
             "episodios": [{"id": "ep_hash_trocado", "hash_roteiro": hash_ok}]}]))
        reg_minuta = escreve("reg_minuta.json",
                             dict(registro([lote_ok]), MINUTA_AGUARDA_AVAL=True))
        reg_extra = escreve("reg_extra.json", registro([lote_ok, {
            "lote": "T-EXTRA", "status": "aprovado",
            "episodios": [{"id": "ep_fora_da_fila", "hash_roteiro": hash_ok}]}]))

        base = ["--fontes", fontes, "--aprovacoes"]

        # (rótulo, args, exit esperado, id semeado que deve aparecer na saída ou None)
        casos = [
            ("T1 controle POSITIVO: órfão semeado na fila TEM de reprovar",
             ["--fila", fila_orfao] + base + [reg_ok], EXIT_REPROVADO, "teste_semeado_sem_aval"),
            ("T2 controle POSITIVO: hash adulterado TEM de reprovar",
             ["--fila", fila_hash] + base + [reg_hash_errado], EXIT_REPROVADO, "ep_hash_trocado"),
            ("T3 controle POSITIVO: universo vazio TEM de reprovar",
             ["--fila", fila_vazia] + base + [reg_ok], EXIT_REPROVADO, None),
            ("T4 controle POSITIVO: registro-minuta TEM de reprovar",
             ["--fila", fila_ok] + base + [reg_minuta], EXIT_REPROVADO, None),
            ("T7 controle POSITIVO: item de fila sem campo 'id' TEM de reprovar",
             ["--fila", fila_sem_id] + base + [reg_ok], EXIT_REPROVADO, None),
            ("T5 controle NEGATIVO: fila toda aprovada TEM de passar",
             ["--fila", fila_ok] + base + [reg_ok], EXIT_OK, None),
            ("T6 controle NEGATIVO segue válido: aprovação extra fora da fila não atrapalha",
             ["--fila", fila_ok] + base + [reg_extra], EXIT_OK, None),
        ]

        for rotulo, cli, esperado, semeado in casos:
            rc, saida = _roda(cli)
            ok = (rc == esperado) and (semeado is None or semeado in saida)
            resultados.append({"caso": rotulo, "exit_obtido": rc, "exit_esperado": esperado,
                               "id_semeado_visto": (semeado in saida) if semeado else None,
                               "passou": ok})
            print(("[passou] " if ok else "[FALHOU] ") + rotulo +
                  f"  (exit {rc}, esperado {esperado})")
            if not ok:
                falhas.append(rotulo)
                print("--- saída do caso que falhou ---")
                print(saida)
                print("--------------------------------")

    if falhas:
        print(f"\nAUTO-TESTE REPROVOU o próprio check ({len(falhas)} caso(s)). "
              "Prova NÃO gravada — o check continua sem valer.")
        return EXIT_REPROVADO

    n_pos = sum(1 for _, _, esperado, _ in casos if esperado == EXIT_REPROVADO)
    prova = {
        "script_sha256": sha256_arquivo(ME),
        "quando": datetime.now(timezone.utc).isoformat(),
        "resultados": resultados,
        "nota": (f"O check demonstrou reprovar os {n_pos} controles positivos semeados (exit 1 "
                 "observado em subprocesso real) e aprovar os negativos (exit 0). "
                 "Só a partir desta prova a execução normal passa a valer."),
    }
    with io.open(ARQ_PROVA, "w", encoding="utf-8") as f:
        json.dump(prova, f, ensure_ascii=False, indent=2)
    print(f"\nAUTO-TESTE OK: {len(casos)}/{len(casos)} controles com o exit esperado "
          f"({n_pos} reprovações observadas). Prova gravada em {ARQ_PROVA}.")
    return EXIT_OK


# ───────────────────────────── cli ─────────────────────────────

def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Gate de aprovação clínica: reprova (exit 1) item de fila sem aprovação registrada.")
    ap.add_argument("--fila", help="reels.json")
    ap.add_argument("--aprovacoes", help="aprovacoes.json")
    ap.add_argument("--publicados", help="state_published.json (universo = fila - publicados)")
    ap.add_argument("--fontes", help="diretório dos episodios_*.py (obrigatório: hash é dimensão do gate)")
    ap.add_argument("--tudo", action="store_true", help="verifica a biblioteca inteira, publicados inclusive")
    ap.add_argument("--auto-teste", action="store_true", help="roda os controles semeados e grava a prova")
    ap.add_argument("--hash", metavar="ID", help="imprime o hash canônico do episódio ID (exige --fontes)")
    args = ap.parse_args(argv)

    if args.auto_teste:
        return auto_teste()

    if args.hash:
        if not args.fontes:
            print("uso: --hash exige --fontes"); return EXIT_ERRO
        try:
            fontes, _, erros_import = carregar_fontes(args.fontes)
        except OSError as e:
            print(f"ERRO de ambiente ao importar fontes: {e}"); return EXIT_ERRO
        for erro in erros_import:
            print(f"[aviso] fonte não importou: {erro}", file=sys.stderr)
        ep = fontes.get(args.hash)
        if ep is None:
            print(f"id '{args.hash}' não encontrado nas fontes de {args.fontes}"); return EXIT_ERRO
        print(hash_canonico(ep))
        return EXIT_OK

    if not (args.fila and args.aprovacoes and args.fontes):
        ap.print_usage()
        print("erro: o check exige --fila, --aprovacoes e --fontes (hash é dimensão "
              "obrigatória do gate; checar só presença esconderia o ramo do texto editado)")
        return EXIT_ERRO
    return checar(args)


if __name__ == "__main__":
    sys.exit(main())