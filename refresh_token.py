#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renova o IG_ACCESS_TOKEN sozinho, na nuvem, e regrava o proprio secret do GitHub.

Elimina a unica manutencao recorrente do motor (trocar o token a cada ~60 dias
a mao). Roda toda semana: cada renovacao devolve +60 dias, entao o token nunca
chega perto de expirar e ha ~8 tentativas de folga antes de qualquer prazo.

Fluxo:
  1. GET graph.instagram.com/refresh_access_token  -> token novo (+60d)
  2. GET api.github.com/.../actions/secrets/public-key
  3. Criptografa com libsodium (sealed box) e faz PUT no secret IG_ACCESS_TOKEN
  4. Grava a data em state/token_refresh.json (o workflow commita)

SEGURANCA: o valor do token nunca e' impresso. E' mascarado no log do Actions
via ::add-mask:: assim que chega, e nenhuma URL e' logada (elas carregam o token
na query string). Em caso de erro, so' o status HTTP e a mensagem da Meta saem.

Env: IG_ACCESS_TOKEN   - token atual (secret do repo)
     GH_SECRETS_PAT    - PAT fine-grained com permissao Secrets: Read and write
     GITHUB_REPOSITORY - preenchido pelo Actions (owner/repo)
"""
import os, sys, json, base64, datetime as dt

import requests
from nacl import encoding, public

GRAPH = "https://graph.instagram.com/refresh_access_token"
GH_API = "https://api.github.com"
SECRET_NAME = "IG_ACCESS_TOKEN"
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "state", "token_refresh.json")
BRT = dt.timezone(dt.timedelta(hours=-3))

TOKEN = os.environ.get("IG_ACCESS_TOKEN", "").strip()
PAT   = os.environ.get("GH_SECRETS_PAT", "").strip()
REPO  = os.environ.get("GITHUB_REPOSITORY", "").strip()

if not TOKEN or not PAT or not REPO:
    faltando = [n for n, v in [("IG_ACCESS_TOKEN", TOKEN), ("GH_SECRETS_PAT", PAT),
                               ("GITHUB_REPOSITORY", REPO)] if not v]
    print(f"ERRO: faltam variaveis: {', '.join(faltando)}")
    sys.exit(1)


def mascarar(valor):
    """Impede que o valor apareca em qualquer log futuro do Actions."""
    print(f"::add-mask::{valor}")


def erro_http(resp, contexto):
    """Loga falha sem nunca expor a URL (ela carrega o token na query string)."""
    try:
        detalhe = json.dumps(resp.json(), ensure_ascii=False)[:400]
    except Exception:
        detalhe = "(resposta nao-JSON)"
    print(f"ERRO {contexto}: HTTP {resp.status_code} - {detalhe}")


# ---------------------------------------------------------------- 1. renovar
# Requisitos da Meta: token com >=24h de vida, ainda valido, e o app com a
# permissao instagram_business_basic. Token que passa de 60 dias sem renovar
# morre de vez e nao pode mais ser renovado - dai a cadencia semanal.
print("1/4 Renovando o token na Meta...")
try:
    r = requests.get(GRAPH, params={"grant_type": "ig_refresh_token",
                                    "access_token": TOKEN}, timeout=30)
except requests.RequestException as e:
    print(f"ERRO de rede ao falar com a Meta: {type(e).__name__}")
    sys.exit(1)

if r.status_code != 200:
    erro_http(r, "ao renovar na Meta")
    print("\nSe a mensagem indica token expirado/invalido, a renovacao automatica "
          "nao e' mais possivel: refaca a Parte A do README (docs/05_MANUTENCAO.md §1).")
    sys.exit(1)

dados = r.json()
novo_token = dados.get("access_token", "")
if not novo_token:
    print("ERRO: a Meta respondeu 200 mas sem access_token.")
    sys.exit(1)

mascarar(novo_token)
segundos = int(dados.get("expires_in", 0))
expira_em = dt.datetime.now(BRT) + dt.timedelta(seconds=segundos)
print(f"    OK - token novo valido por {segundos // 86400} dias "
      f"(ate {expira_em:%d/%m/%Y}).")

# ------------------------------------------------- 2. chave publica do repo
print("2/4 Buscando a chave publica do repositorio...")
cab = {"Accept": "application/vnd.github+json",
       "Authorization": f"Bearer {PAT}",
       "X-GitHub-Api-Version": "2022-11-28",
       "User-Agent": "refresh-token-instagram"}
r = requests.get(f"{GH_API}/repos/{REPO}/actions/secrets/public-key",
                 headers=cab, timeout=30)
if r.status_code != 200:
    erro_http(r, "ao buscar a chave publica")
    print("\nProvavel causa: o GH_SECRETS_PAT expirou ou nao tem a permissao "
          "'Secrets: Read and write' neste repositorio.")
    sys.exit(1)
chave = r.json()

# ------------------------------------------------------------ 3. criptografar
# O GitHub so' aceita secrets cifrados com libsodium sealed box na chave
# publica do repo - texto puro e' recusado.
print("3/4 Criptografando (libsodium sealed box)...")
pk = public.PublicKey(chave["key"].encode("utf-8"), encoding.Base64Encoder())
cifrado = base64.b64encode(
    public.SealedBox(pk).encrypt(novo_token.encode("utf-8"))
).decode("utf-8")

# -------------------------------------------------------- 4. regravar secret
print(f"4/4 Regravando o secret {SECRET_NAME}...")
r = requests.put(f"{GH_API}/repos/{REPO}/actions/secrets/{SECRET_NAME}",
                 headers=cab, timeout=30,
                 json={"encrypted_value": cifrado, "key_id": chave["key_id"]})
if r.status_code not in (201, 204):
    erro_http(r, "ao regravar o secret")
    sys.exit(1)

agora = dt.datetime.now(BRT)
print(f"    OK - secret atualizado (HTTP {r.status_code}).")

# Rastro auditavel: responde "quando foi renovado?" sem abrir o painel.
os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
try:
    with open(STATE_FILE, encoding="utf-8") as fh:
        estado = json.load(fh)
except (OSError, ValueError):
    estado = {"historico": []}

estado["ultima_renovacao"] = agora.strftime("%Y-%m-%d")
estado["expira_em"] = expira_em.strftime("%Y-%m-%d")
estado["historico"] = (estado.get("historico", []) + [agora.strftime("%Y-%m-%d")])[-30:]
with open(STATE_FILE, "w", encoding="utf-8") as fh:
    json.dump(estado, fh, ensure_ascii=False, indent=2)
    fh.write("\n")

print(f"\nPronto. Renovado em {agora:%d/%m/%Y}, valido ate {expira_em:%d/%m/%Y}.")
