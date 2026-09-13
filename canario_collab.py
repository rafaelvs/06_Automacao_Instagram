#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
canario_collab.py — REFUTADOR do parâmetro `collaborators` (plano de saída da estagnação, B3).

Pergunta que ele responde: a Graph API via graph.instagram.com (Instagram Login) RECUSA um
container cujo `collaborators` traz um username inexistente? Se recusa, o motor pode confiar
que um username errado numa peça real vai falhar ALTO (e não publicar em silêncio sem o
parceiro). Se NÃO recusa (container criado), o check está morto e o canário sai VERMELHO —
refutador que nunca falhou não é refutador (lição da casa).

O que faz: cria UM container de imagem (a mesma `images/dest01.jpg` que já está no perfil como
capa de Destaque) com collaborators=["<username inválido com timestamp>"] e lê a resposta.
O que NÃO faz: NUNCA chama `media_publish`. Container não publicado expira em 24 h na Meta.

Exit: 0 = a API recusou (canário PASSOU); 1 = a API aceitou (check morto) ou token/ambiente
inválido. Só leitura + 1 POST de container.
"""
import json
import os
import sys
import time

import requests

IG_USER_ID = os.environ.get("IG_USER_ID", "").strip()
TOKEN = os.environ.get("IG_ACCESS_TOKEN", "").strip()
REPO = os.environ.get("GITHUB_REPOSITORY", "rafaelvs/06_Automacao_Instagram").strip()
VER = os.environ.get("GRAPH_VERSION", "v21.0").strip()
HOST = f"https://graph.instagram.com/{VER}"
IMG = f"https://raw.githubusercontent.com/{REPO}/main/images/dest01.jpg"

if not IG_USER_ID or not TOKEN:
    print("::error::defina IG_USER_ID e IG_ACCESS_TOKEN"); sys.exit(1)

invalido = f"canario_inexistente_{int(time.time())}_zz"
payload = {"image_url": IMG, "caption": "canário técnico — container nunca publicado",
           "collaborators": json.dumps([invalido]), "access_token": TOKEN}
r = requests.post(f"{HOST}/{IG_USER_ID}/media", data=payload, timeout=120)
try:
    corpo = r.json()
except Exception:
    corpo = {"_raw": r.text[:300]}
err = corpo.get("error") if isinstance(corpo, dict) else None
print(f"HTTP {r.status_code} | username semeado: {invalido}")
print("resposta:", json.dumps(corpo, ensure_ascii=False)[:600].replace(TOKEN, "***"))

if isinstance(err, dict) and err.get("code") in (190, 10, 102) or (isinstance(err, dict) and 200 <= int(err.get("code") or 0) <= 299):
    print("::error::token/permissão inválidos — o canário não mediu nada (não é resultado de collab).")
    sys.exit(1)
if r.status_code >= 400 and err:
    print(f"CANÁRIO PASSOU: a API RECUSOU o container com collaborator inválido "
          f"(code {err.get('code')} / subcode {err.get('error_subcode')}). "
          "Username errado numa peça real vai falhar ALTO no publish.py.")
    sys.exit(0)
if r.status_code < 400 and isinstance(corpo, dict) and corpo.get("id"):
    print(f"::error::CANÁRIO FALHOU: a API ACEITOU o container {corpo['id']} com username inexistente — "
          "o check de collaborators está MORTO por este caminho (graph.instagram.com). "
          "Não usar `collaborators` em peça real até entender o comportamento. (Container não foi publicado; expira em 24 h.)")
    sys.exit(1)
print("::error::resposta inesperada — tratar como reprovado.")
sys.exit(1)
