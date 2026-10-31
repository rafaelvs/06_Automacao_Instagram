# -*- coding: utf-8 -*-
"""
checar_mencoes.py — nenhum @ de perfil inexistente sai publicado (Rafael, 31/10/2026: "não pode colocar
um @ numa página inexistente... muito ruim isso para postagem" / "tem que ter guardrail").

O erro que originou: a pesquisa de 11/09 deu "@sbortopediapediatrica, 2.465 seguidores" — o perfil não
existe (o oficial da SBOP é @sbopbr, linkado em sbop.org.br) e a menção saiu em 12 peças.

Três modos:
  (padrão)       ESTÁTICO: todo @ da fila pendente (reels/posts/sequences/stories/stories_cf/destaques),
                 dos inventários, das fontes episodios*.py e de legenda.MENCOES tem de estar em
                 legenda.MENCOES_VERIFICADAS, e toda entrada da lista tem nome + prova + conferido_em.
                 Universo vazio = FALHA. Exit 0 limpo / 1 violação / 2 erro de ambiente.
  --vivo [@h…]   AO VIVO: abre instagram.com/<handle>/ como navegador (cabeçalhos Sec-Fetch de
                 navegação; sem eles o Instagram devolve a casca vazia até para perfil que existe) e
                 exige o og:title com "(@handle)". CONTROLES em todo run: o perfil do Dr. TEM de resolver
                 e um @ inventado NÃO pode resolver — se um dos dois falhar o instrumento está CEGO e não
                 conclui nada (exit 3), nunca "existe" nem "não existe". Sem handles = a lista inteira.
                 Exit 0 todos existem / 1 algum não existe / 3 cego. --cego-nao-reprova: cego vira aviso
                 (exit 0) — para o CI, onde o IP do runner pode ser barrado; o ESTÁTICO continua valendo.
  --auto-teste   controles semeados (inclusive o @ real que saiu errado).

Para incluir uma menção nova: (1) achar o perfil no SITE OFICIAL da entidade, (2) rodar
`python checar_mencoes.py --vivo @handle`, (3) só então pôr em legenda.MENCOES_VERIFICADAS com a prova.
"""
import html
import io
import json
import os
import re
import sys
import urllib.request

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import legenda  # noqa: E402

FILAS = ("reels.json", "posts.json", "sequences.json", "stories.json", "stories_cf.json", "destaques.json")
INVENTARIOS = ("reels_legado_mudos.json", "verbetes_biblioteca.json")
CONTROLE_EXISTE = "@rafaelvargasmd"
CONTROLE_NAO_EXISTE = "@zz9qx7_nao_existe_controle"
CAMPOS_PROVA = ("nome", "prova", "conferido_em")


def _carrega(nome):
    with open(os.path.join(ROOT, nome), encoding="utf-8-sig") as f:
        return json.load(f)


def _itens(d):
    if isinstance(d, list):
        return d
    if isinstance(d, dict):            # {"items": [...]} ou {id: {...}}
        for k in ("items", "itens", "stories", "fila"):
            if isinstance(d.get(k), list):
                return d[k]
        return [dict(v, id=v.get("id", k)) if isinstance(v, dict) else {"id": k, "v": v} for k, v in d.items()]
    return []


def universo(root=ROOT):
    """[(origem, texto)] de tudo que pode virar texto publicado. Publicado fica de fora (é o registro
    do que está no ar; a API não edita legenda publicada)."""
    out = []
    try:
        st = json.load(open(os.path.join(root, "state", "published.json"), encoding="utf-8-sig"))
    except FileNotFoundError:
        st = {"published": []}
    done = {str(e.get("id", "")).split("#")[0] for e in st.get("published", [])}
    for nome in FILAS:
        p = os.path.join(root, nome)
        if not os.path.exists(p):
            continue
        for x in _itens(json.load(open(p, encoding="utf-8-sig"))):
            if isinstance(x, dict) and str(x.get("id", "")) not in done:
                out.append((f"{nome}:{x.get('id', '?')}", json.dumps(x, ensure_ascii=False)))
    for nome in INVENTARIOS:
        p = os.path.join(root, nome)
        if os.path.exists(p):
            out.append((nome, open(p, encoding="utf-8-sig").read()))
    for nome in sorted(os.listdir(root)):
        if nome.startswith(("episodios", "episodio_")) and nome.endswith(".py"):
            out.append((nome, open(os.path.join(root, nome), encoding="utf-8").read()))
    for fam, linha in legenda.MENCOES.items():
        out.append((f"legenda.MENCOES[{fam}]", linha))
    return out


def checar(itens, lista=None):
    lista = legenda.MENCOES_VERIFICADAS if lista is None else lista
    if not itens:
        print("REPROVADO: universo VAZIO — zero verificados = falha, não sucesso.")
        return 1, []
    ruins = []
    for h, info in lista.items():
        falta = [c for c in CAMPOS_PROVA if not str((info or {}).get(c) or "").strip()]
        if falta or h != h.lower() or not h.startswith("@"):
            ruins.append(("MENCOES_VERIFICADAS", h, f"entrada sem {'+'.join(falta) or 'formato @minúsculo'}"))
    vistos = {}
    for origem, texto in itens:
        for m in legenda.mencoes_em(texto):
            vistos[m] = vistos.get(m, 0) + 1
            if m not in lista:
                ruins.append((origem, m, "fora da lista verificada"))
    print(f"Universo: {len(itens)} fonte(s); menções vistas: "
          + (", ".join(f"{m}×{n}" for m, n in sorted(vistos.items())) or "nenhuma"))
    for origem, m, por in ruins:
        print(f"  [VIOLAÇÃO] {origem}: {m} — {por}")
    print("OK: todo @ está na lista verificada." if not ruins else f"REPROVADO: {len(ruins)} violação(ões).")
    return (1 if ruins else 0), ruins


# ───────────────────────────── ao vivo ─────────────────────────────
_H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/130.0.0.0 Safari/537.36",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
      "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8", "Upgrade-Insecure-Requests": "1",
      "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Dest": "document", "Sec-Fetch-Site": "none", "Sec-Fetch-User": "?1",
      "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
      "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": '"Windows"'}


def titulo_do_perfil(handle, timeout=20):
    """og:title da página pública do perfil, ou None (página vazia/inexistente). Erro de rede propaga."""
    req = urllib.request.Request(f"https://www.instagram.com/{handle.lstrip('@')}/", headers=_H)
    t = urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", "replace")
    m = re.search(r'property="og:title" content="([^"]*)"', t)
    return html.unescape(m.group(1)) if m else None


def resolve(handle, titulo):
    return bool(titulo) and f"(@{handle.lstrip('@').lower()})" in titulo.lower()


def vivo(handles, buscar=titulo_do_perfil):
    """{handle: 'EXISTE'|'NAO_EXISTE'} ou 'CEGO' quando os controles não se comportam."""
    def tenta(h):
        try:
            return buscar(h)
        except Exception as e:                  # rede/429: não é "não existe", é cegueira
            print(f"  [erro de leitura] {h}: {type(e).__name__}: {e}")
            return Ellipsis
    res, cego = {}, []
    for k, h in enumerate(handles):
        if k % 3 == 0:                          # controles intercalados: bloqueio no meio do run aparece
            tp, tn = tenta(CONTROLE_EXISTE), tenta(CONTROLE_NAO_EXISTE)
            if tp is Ellipsis or not resolve(CONTROLE_EXISTE, tp):
                cego.append(f"controle POSITIVO {CONTROLE_EXISTE} não resolveu ({tp!r})")
            if tn is Ellipsis or resolve(CONTROLE_NAO_EXISTE, tn) or tn:
                cego.append(f"controle NEGATIVO {CONTROLE_NAO_EXISTE} não ficou vazio ({tn!r})")
            if cego:
                return "CEGO", cego
        t = tenta(h)
        if t is Ellipsis:
            return "CEGO", [f"leitura de {h} falhou"]
        res[h] = ("EXISTE", t) if resolve(h, t) else ("NAO_EXISTE", t)
    return res, []


def main_vivo(argv):
    alvos = [a.lower() if a.startswith("@") else "@" + a.lower() for a in argv if not a.startswith("--")]
    alvos = alvos or [h for h in legenda.MENCOES_VERIFICADAS if h != CONTROLE_EXISTE]
    res, motivos = vivo(alvos)
    if res == "CEGO":
        print("CEGO: o instrumento não distingue perfil existente de inexistente agora — nada concluído.")
        for m in motivos:
            print("  - " + m)
        if "--cego-nao-reprova" in argv:
            print("::warning::checar_mencoes --vivo CEGO neste runner; a lista branca (modo estático) segue valendo.")
            return 0
        return 3
    ruins = [h for h, (v, _) in res.items() if v != "EXISTE"]
    for h, (v, t) in res.items():
        print(f"  [{v}] {h}" + (f" — {t}" if t else ""))
    print("OK: todos existem." if not ruins else f"REPROVADO: {', '.join(ruins)} NÃO existe(m).")
    return 1 if ruins else 0


# ───────────────────────────── auto-teste ─────────────────────────────
def auto_teste():
    lista = dict(legenda.MENCOES_VERIFICADAS)
    ok = "Texto.\n\nEnvia para quem precisa disso.\n\nSociedade da área: @sbopbr\n\nDr. Rafael Vargas · Médico"
    casos = [
        ("controle NEGATIVO: menção verificada passa", [("t", ok)], lista, 0),
        ("controle POSITIVO: o @ REAL que saiu errado (@sbortopediapediatrica)",
         [("t", ok.replace("@sbopbr", "@sbortopediapediatrica"))], lista, 1),
        ("controle POSITIVO: @ inventado qualquer", [("t", ok + " @sbop_oficial")], lista, 1),
        ("controle POSITIVO: maiúscula não escapa (@SBORTOPEDIAPEDIATRICA)",
         [("t", ok.replace("@sbopbr", "@SBORTOPEDIAPEDIATRICA"))], lista, 1),
        ("controle NEGATIVO: e-mail não é menção (contato@primeiropasso.org)",
         [("t", ok + "\nEscreva para contato@primeiropasso.org")], lista, 0),
        ("controle NEGATIVO: ponto final de frase (@sbopbr.)", [("t", ok.replace("@sbopbr", "@sbopbr."))], lista, 0),
        ("controle POSITIVO: entrada da lista SEM prova", [("t", ok)],
         dict(lista, **{"@sbopbr": {"nome": "SBOP", "prova": "", "conferido_em": "2026-10-31"}}), 1),
        ("controle POSITIVO: universo vazio", [], lista, 1),
    ]
    falhas = 0
    for rotulo, itens, lst, esperado in casos:
        rc, _ = checar(itens, lst)
        passou = rc == esperado
        print(("[passou] " if passou else "[FALHOU] ") + f"{rotulo} (exit {rc}, esperado {esperado})")
        falhas += 0 if passou else 1
    # integração: as duas outras portas usam a MESMA lista
    p = legenda.validar(ok.replace("@sbopbr", "@sbortopediapediatrica") + "\nCRM RQE", "reel")
    passou = any("NÃO verificado" in x for x in p)
    print(("[passou] " if passou else "[FALHOU] ") + f"legenda.validar() reprova o @ errado ({p})")
    falhas += 0 if passou else 1
    # ao vivo, com leitor falso: cegueira nunca vira veredito
    pag = {"@rafaelvargasmd": "Dr. Rafael Vargas (@rafaelvargasmd) • Instagram", "@sbopbr": "SBOP (@sbopbr) • Instagram"}
    casos_vivo = [
        ("vivo: existe e não existe separados", lambda h: pag.get(h), ["@sbopbr", "@sbortopediapediatrica"],
         {"@sbopbr": "EXISTE", "@sbortopediapediatrica": "NAO_EXISTE"}),
        ("vivo: controle positivo vazio = CEGO (não 'não existe')", lambda h: None, ["@sbopbr"], "CEGO"),
        ("vivo: página genérica para TUDO = CEGO", lambda h: "Instagram (@" + h.lstrip("@") + ")", ["@x"], "CEGO"),
        ("vivo: erro de rede = CEGO", lambda h: (_ for _ in ()).throw(OSError("429")), ["@sbopbr"], "CEGO"),
    ]
    for rotulo, buscar, alvos, esperado in casos_vivo:
        res, _ = vivo(alvos, buscar=buscar)
        obtido = res if res == "CEGO" else {h: v for h, (v, _) in res.items()}
        passou = obtido == esperado
        print(("[passou] " if passou else "[FALHOU] ") + f"{rotulo} -> {obtido}")
        falhas += 0 if passou else 1
    print("AUTO-TESTE:", "PASSOU" if not falhas else f"REPROVOU ({falhas})")
    return 0 if not falhas else 1


if __name__ == "__main__":
    try:
        if "--auto-teste" in sys.argv:
            sys.exit(auto_teste())
        if "--vivo" in sys.argv:
            sys.exit(main_vivo(sys.argv[1:]))
        rc, _ = checar(universo())
        sys.exit(rc)
    except (OSError, ValueError) as e:
        print(f"ERRO de ambiente: {type(e).__name__}: {e}")
        sys.exit(2)
