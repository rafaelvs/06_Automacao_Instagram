#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
canario_rotulo_ia.py — prova que a Graph API RECONHECE o parâmetro `is_ai_generated` em reel,
pelo caminho que o motor usa (graph.instagram.com, Instagram Login). NUNCA publica.

Por que existe (18/10/2026): a Central de Ajuda do Instagram exige rótulo de IA em "um reel
narrado com uma sobreposição de voz realista gerada por IA" e avisa que pode haver penalidade
sem ele. A API aceita `is_ai_generated=true` na criação do contêiner desde 22/06/2026 (changelog
oficial, "AI Info Label", Instagram Login e Facebook Login). O Rafael aprovou ligar o rótulo.

Por que DOIS testes, e não um:
  1. `is_ai_generated=true`  -> TEM de ser ACEITO (senão ligar o rótulo derrubaria todo reel).
  2. `is_ai_generated=banana`-> TEM de ser RECUSADO. Se a API aceitar lixo, ela está IGNORANDO
     o campo — e o teste 1 "passaria" sem rotular nada. Aceitar `true` sozinho não prova que o
     rótulo funciona; recusar o valor inválido prova que o campo é lido. (Lição da casa:
     verificador que nunca reprova não é verificador.)

O que faz: 2 POSTs de contêiner REELS com um vídeo que já está no perfil. O que NÃO faz:
nunca chama `media_publish`. Contêiner não publicado expira em 24 h na Meta.

Exit 0 = os dois testes passaram (o rótulo pode ser ligado). Exit 1 = qualquer outra coisa.
"""
import json
import os
import sys

import requests

IG_USER_ID = os.environ.get("IG_USER_ID", "").strip()
TOKEN = os.environ.get("IG_ACCESS_TOKEN", "").strip()
REPO = os.environ.get("GITHUB_REPOSITORY", "rafaelvs/06_Automacao_Instagram").strip()
VER = os.environ.get("GRAPH_VERSION", "v21.0").strip()
HOST = f"https://graph.instagram.com/{VER}"
VIDEO = f"https://raw.githubusercontent.com/{REPO}/main/reels/_preview_qa_banho_fixador.mp4"

if not IG_USER_ID or not TOKEN:
    print("::error::defina IG_USER_ID e IG_ACCESS_TOKEN"); sys.exit(1)


def conteiner(valor):
    payload = {"media_type": "REELS", "video_url": VIDEO,
               "caption": "canário técnico — contêiner nunca publicado",
               "is_ai_generated": valor, "access_token": TOKEN}
    r = requests.post(f"{HOST}/{IG_USER_ID}/media", data=payload, timeout=120)
    try:
        corpo = r.json()
    except Exception:
        corpo = {"_raw": r.text[:300]}
    print(f"[is_ai_generated={valor!r}] HTTP {r.status_code} | "
          + json.dumps(corpo, ensure_ascii=False)[:500].replace(TOKEN, "***"))
    err = corpo.get("error") if isinstance(corpo, dict) else None
    if isinstance(err, dict):
        code = int(err.get("code") or 0)
        if code in (190, 10, 102) or 200 <= code <= 299:
            print("::error::token/permissão inválidos — o canário não mediu nada.")
            sys.exit(1)
    return r.status_code, corpo, err


st1, c1, e1 = conteiner("true")
st2, c2, e2 = conteiner("banana")

aceitou_true = st1 < 400 and isinstance(c1, dict) and bool(c1.get("id"))
# A recusa só PROVA que a API lê o campo se for a recusa DO CAMPO: parâmetro inválido (code 100)
# citando is_ai_generated. Antes qualquer erro na 2ª chamada servia — um rate limit (4/17/32/613)
# ou erro de vídeo (2207xxx / 9004 / 9007) virava "a API lê o campo" (auditoria 19/10).
msg2 = str((e2 or {}).get("message", "")) + " " + str((e2 or {}).get("error_user_msg", ""))
recusou_lixo = (st2 >= 400 and isinstance(e2, dict) and int(e2.get("code") or 0) == 100
                and "is_ai_generated" in msg2)
inconclusivo = st2 >= 400 and isinstance(e2, dict) and not recusou_lixo

if inconclusivo:
    print(f"::error::CANÁRIO INCONCLUSIVO: a 2ª chamada falhou por outro motivo (code {e2.get('code')} / "
          f"subcode {e2.get('error_subcode')}: {msg2.strip()[:160]}) — isso NÃO prova que a API lê o campo. "
          "Rode de novo mais tarde.")
    sys.exit(1)
if aceitou_true and recusou_lixo:
    print(f"CANÁRIO PASSOU: `is_ai_generated=true` foi ACEITO (contêiner {c1['id']}, não publicado) e o "
          f"valor inválido foi RECUSADO (code {e2.get('code')} / subcode {e2.get('error_subcode')}) — "
          "a API lê o campo. Pode ligar o rótulo no publish.py.")
    sys.exit(0)
if not aceitou_true:
    print("::error::CANÁRIO FALHOU: a API RECUSOU `is_ai_generated=true` — ligar o rótulo derrubaria "
          "todo reel. NÃO ligar.")
else:
    print("::error::CANÁRIO FALHOU: a API ACEITOU `is_ai_generated=banana` — ela está ignorando o campo, "
          "e o rótulo não seria aplicado. NÃO tratar o rótulo como ligado.")
sys.exit(1)
