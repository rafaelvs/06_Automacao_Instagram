# -*- coding: utf-8 -*-
"""
LINT SEND + HOOK — enforça as 2 alavancas de DESCOBERTA da auditoria v4:
  1. GANCHO de 3s (cena 0): começar pelo conflito/pergunta/número — NUNCA com intro ("oi pessoal").
  2. SEND-ASK na CTA (última cena cta=True): pedir COMPARTILHAMENTO (send é o sinal nº1 p/ não-seguidor,
     Mosseri) com verbo de envio + destinatário específico — NUNCA cota genérica ("marca 5 amigos").
Saída: HOOK_FRACO e SEND_FRACO. Idempotente, só leitura. Rodar: python checar_send_hook.py

EXTENSÃO ADITIVA (v5, cobertura de bibliotecas):
  Além dos 89 EPISODES, agora também audita a QUALIDADE do send-ask no campo "caption" de cada item
  de reels.json e posts.json — que antes ficavam de fora. É 100% ADVISORY: só gera AVISOS (REVISAR),
  NUNCA entra em exit=1/BLOQUEIOS. Não há gancho/cenas num item de biblioteca, então só o SEND-ask se
  aplica (HOOK não). Cada caption é classificada em SEND_OK / SEND_FRACO / SEND_AUSENTE via
  classificar_caption(); auditar_captions() faz a varredura fail-open (RUIDOSO) e o gate soma o
  resultado apenas na linha de avisos. main() (episódios) permanece intacto — mesma assinatura.
"""
import unicodedata
import json
import os
from episodios_pe_no_chao import EPISODES

ROOT = os.path.dirname(os.path.abspath(__file__))


def norm(s):
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()


INTROS = ["oi pessoal", "ola pessoal", "ola, pessoal", "fala pessoal", "e ai pessoal", "e ai, galera",
          "bem-vindo", "bem vindo", "sejam bem", "ola a todos", "oi gente", "fala galera", "oi, gente"]
SEND_VERBOS = ["manda", "envia", "encaminha", "compartilh", "passa adiante", "passa pra", "mostra isso",
               "mostra pra", "marca alguem que",
               # + ADITIVO (nunca remover): imperativo 'Envie/Enviem' — norm('envie') NÃO contém 'envia'.
               "envie", "envi", "encaminhe", "mande", "mande este", "mande esse"]
# destinatário específico (bom): pra um pai/mae/avo/quem/alguem que...
DESTINATARIO = ["pra um", "pra uma", "pra quem", "pra alguem", "pro grupo", "pra aquele", "pra aquela",
                "pra outra", "pra outro", "a quem",
                # + ADITIVO: variantes com 'para ...' (caption real 'Envie para aquele pai...' escapava)
                "para um", "para uma", "para quem", "para alguem", "para aquele", "para aquela",
                "pro pai", "pra mae", "pro pai ou pra mae"]
# cota genérica (ruim — engagement bait, suprimido):
COTA = ["5 amigos", "cinco amigos", "marca 5", "marque 5", "compartilhe com todos", "manda pra todos",
        "marca todo mundo", "10 amigos"]

# ----------------------------------------------------------------------------------------------------
# EXTENSÃO ADITIVA — classificador de send-ask para captions de biblioteca (reels.json / posts.json).
# ADVISORY: alimenta SÓ 'avisos' no gate; jamais 'bloqueios'.
# ----------------------------------------------------------------------------------------------------
# CONDIÇÃO nomeada (send FORTE): papel de pessoa + condição descrita (pai/mãe/avó/... que <faz algo>),
# ou "quem <predicado descritivo>" (quem esta/tem/vive/convive/ouviu/perdeu/reparou/pensa/vai/anda...).
# São os padrões reais dos episódios: "pra um pai, mae ou avo que precisa ver", "pra quem esta
# reconstruindo um osso", "para aquele pai ou aquela mae que vive essa preocupacao".
CONDICAO_PAPEL = ["pai", "mae", "avo", "amigo", "amiga", "pre-adolescente", "adolescente",
                  "bebe", "recem-nascido", "crianca", "filho", "filha", "responsavel"]
CONDICAO_QUEM = ["quem esta", "quem tem", "quem vive", "quem convive", "quem ouviu", "quem perdeu",
                 "quem reparou", "quem pensa", "quem vai", "quem anda", "quem ja", "quem cujo",
                 "quem reconstro", "quem acompanha", "quem sofre", "quem passa", "quem cuida",
                 "quem quer"]
# GENÉRICO / ANAFÓRICO (send FRACO mesmo com verbo): destinatário vago ("alguem que precisa",
# "quem precisa" isolado) ou anafórico ("com a pessoa", "isso", "no direct com a pessoa"), sem
# condição nomeada.
GENERICO_ANAFORICO = ["alguem que precisa", "quem precisa", "com a pessoa", "pra pessoa",
                      "para a pessoa", "compartilhe no direct com a pessoa", "com todos", "todo mundo",
                      "geral", "quem quiser"]


def _test_norm_invariante():
    """Self-check (opcional, advisory): TODA entrada das listas de matching precisa SOBREVIVER a norm()
    — i.e. norm(entrada) == entrada. Uma entrada com acento (ex.: 'avó') seria inalcançável, pois o
    texto comparado já passou por norm() (que remove acentos). Não roda no gate; só sob demanda."""
    listas = {"INTROS": INTROS, "SEND_VERBOS": SEND_VERBOS, "DESTINATARIO": DESTINATARIO,
              "COTA": COTA, "CONDICAO_PAPEL": CONDICAO_PAPEL, "CONDICAO_QUEM": CONDICAO_QUEM,
              "GENERICO_ANAFORICO": GENERICO_ANAFORICO}
    mortas = [(nome, e) for nome, lst in listas.items() for e in lst if norm(e) != e]
    if mortas:
        for nome, e in mortas:
            print("   [ENTRADA MORTA] %-18s %r != norm()=%r" % (nome, e, norm(e)))
        raise AssertionError("%d entrada(s) inalcancavel(is) pos-norm — corrigir." % len(mortas))
    print("norm-invariante OK: todas as entradas das listas sobrevivem a norm().")
    return True


def classificar_caption(caption):
    """Classifica o send-ask de UMA caption de biblioteca. ADVISORY (nunca bloqueia).
    Retorna 'SEND_OK' | 'SEND_FRACO' | 'SEND_AUSENTE'.
      - SEND_AUSENTE: nenhum verbo de envio.
      - SEND_OK: verbo de envio + destinatário POR CONDIÇÃO (papel nomeado c/ condição, ou 'quem <predicado>').
      - SEND_FRACO: tem verbo mas destinatário é genérico ('quem precisa'), anafórico ('a pessoa'),
        cota ('marca 5') ou ausente/só nomeia a pessoa sem a condição.
    """
    n = norm(caption)
    # 1) COTA / engagement bait é sempre FRACO — é uma TENTATIVA de send-ask, só que ruim.
    #    Checar ANTES do verbo (ex.: "marca 5 amigos" não casa SEND_VERBOS mas é send-ask fraco).
    if any(c in n for c in COTA) or "marca 5" in n or "marca cinco" in n or "marque 5" in n:
        return "SEND_FRACO"
    # 2) sem NENHUM verbo de envio => AUSENTE
    tem_verbo = any(v in n for v in SEND_VERBOS)
    if not tem_verbo:
        return "SEND_AUSENTE"
    # 3) destinatário GENÉRICO / ANAFÓRICO ("com a pessoa", "alguem que precisa", "quem precisa"
    #    isolado) => FRACO. TEM PRECEDÊNCIA sobre a promoção por condição, senão um "quem esta..."
    #    numa pergunta retórica ("conhece quem esta com essa duvida? ... com a pessoa") viraria OK.
    puro_generico = any(g in n for g in GENERICO_ANAFORICO)
    if puro_generico:
        return "SEND_FRACO"
    # 4) condição nomeada por "quem <predicado descritivo>" => forte
    if any(q in n for q in CONDICAO_QUEM):
        return "SEND_OK"
    # 5) papel de pessoa (pai/mãe/avó...) SEGUIDO de uma condição => forte.
    #    A condição pode vir como '... que <algo>' ("um pai ... que precisa ver") OU '... de <algo>'
    #    ("pro pai ou pra mae de um pre-adolescente", "de crianca com articulacao inchada").
    tem_dest = any(d in n for d in DESTINATARIO)
    tem_papel = any(p in n for p in CONDICAO_PAPEL)
    tem_condicao = (" que " in n) or (" de um " in n) or (" de uma " in n) or (" de crianca" in n) \
        or (" cujo " in n) or (" cuja " in n)
    if tem_papel and tem_condicao:
        return "SEND_OK"
    if tem_dest and tem_condicao:
        return "SEND_OK"
    # verbo presente, mas destinatário sem condição nomeada
    return "SEND_FRACO"


def auditar_captions(arquivos=("reels.json", "posts.json")):
    """Varredura ADITIVA e ADVISORY das bibliotecas. Fail-open RUIDOSO (imprime AVISO e segue).
    Retorna dict: {'ok', 'fraco', 'ausente', 'total', 'detalhes': [(origem, id, classe, trecho)]}.
    """
    ok = fraco = ausente = 0
    detalhes = []
    for arq in arquivos:
        p = os.path.join(ROOT, arq)
        if not os.path.exists(p):
            print(f"AVISO: {arq} nao encontrado — pulando (fail-open).")
            continue
        try:
            d = json.load(open(p, encoding="utf-8"))
            itens = d if isinstance(d, list) else []
            for it in itens:
                if not isinstance(it, dict):
                    continue
                cap = it.get("caption")
                if not cap:
                    continue
                classe = classificar_caption(cap)
                if classe == "SEND_OK":
                    ok += 1
                elif classe == "SEND_FRACO":
                    fraco += 1
                    detalhes.append((arq, it.get("id", "?"), classe, norm(cap)[:80]))
                else:
                    ausente += 1
                    detalhes.append((arq, it.get("id", "?"), classe, norm(cap)[:80]))
        except Exception as e:
            print(f"AVISO: {arq}: {e} (fail-open — nao bloqueia).")
    return {"ok": ok, "fraco": fraco, "ausente": ausente,
            "total": ok + fraco + ausente, "detalhes": detalhes}


def main():
    hook_fraco, send_fraco, ok = [], [], 0
    for ep in EPISODES:
        cenas = ep.get("scenes", [])
        if not cenas:
            continue
        # 1) HOOK (cena 0)
        s0 = cenas[0]
        gancho = norm(" ".join([s0.get("k", "")] + s0.get("sc", []) + [s0.get("sub", ""), s0.get("vo", "")]))
        if any(intro in gancho for intro in INTROS):
            hook_fraco.append((ep["id"], "intro detectada no gancho"))
        # 2) SEND-ASK (última cena cta=True, senão a última)
        cta = next((c for c in reversed(cenas) if c.get("cta")), cenas[-1])
        txt = norm(" ".join([cta.get("k", "")] + cta.get("sc", []) + [cta.get("sub", ""), cta.get("vo", "")]))
        cap = norm(ep.get("caption", ""))
        tem_verbo = any(v in txt or v in cap for v in SEND_VERBOS)
        tem_dest = any(d in txt or d in cap for d in DESTINATARIO)
        tem_cota = any(c in txt or c in cap for c in COTA)
        if tem_cota:
            send_fraco.append((ep["id"], "cota genérica (engagement bait) — trocar por send-ask específico"))
        elif not tem_verbo:
            send_fraco.append((ep["id"], "sem verbo de envio na CTA — adicionar 'manda pra...'"))
        elif not tem_dest:
            send_fraco.append((ep["id"], "send-ask sem destinatário específico — nomear 'pra um pai que...'"))
        else:
            ok += 1

    print("=== LINT send+hook | %d episodios ===" % len(EPISODES))
    print("OK (gancho s/ intro + send-ask específico):", ok)
    print("HOOK_FRACO (intro no gancho):", len(hook_fraco))
    for i, d in hook_fraco:
        print("   [HOOK]", i, "-", d)
    print("SEND_FRACO (CTA fraca):", len(send_fraco))
    for i, d in send_fraco:
        print("   [SEND]", i, "-", d)
    return hook_fraco, send_fraco


def relatorio_captions():
    """Imprime o relatório ADVISORY das bibliotecas e devolve o dict de auditar_captions().
    Chamado pelo gate (soma SÓ em avisos) e no modo standalone. NUNCA bloqueia."""
    res = auditar_captions()
    print("=== LINT send-ask bibliotecas (reels/posts) | ADVISORY | %d captions ===" % res["total"])
    print("SEND (reels/posts): OK=%d FRACO=%d AUSENTE=%d" % (res["ok"], res["fraco"], res["ausente"]))
    for origem, _id, classe, trecho in res["detalhes"]:
        print("   [%s] %-10s %-16s :: %s" % (classe, origem, str(_id), trecho))
    return res


if __name__ == "__main__":
    main()
    print()
    relatorio_captions()
