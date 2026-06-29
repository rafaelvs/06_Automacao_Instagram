# -*- coding: utf-8 -*-
"""
LINT SEND + HOOK — enforça as 2 alavancas de DESCOBERTA da auditoria v4:
  1. GANCHO de 3s (cena 0): começar pelo conflito/pergunta/número — NUNCA com intro ("oi pessoal").
  2. SEND-ASK na CTA (última cena cta=True): pedir COMPARTILHAMENTO (send é o sinal nº1 p/ não-seguidor,
     Mosseri) com verbo de envio + destinatário específico — NUNCA cota genérica ("marca 5 amigos").
Saída: HOOK_FRACO e SEND_FRACO. Idempotente, só leitura. Rodar: python checar_send_hook.py
"""
import unicodedata
from episodios_pe_no_chao import EPISODES


def norm(s):
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()


INTROS = ["oi pessoal", "ola pessoal", "ola, pessoal", "fala pessoal", "e ai pessoal", "e ai, galera",
          "bem-vindo", "bem vindo", "sejam bem", "ola a todos", "oi gente", "fala galera", "oi, gente"]
SEND_VERBOS = ["manda", "envia", "encaminha", "compartilh", "passa adiante", "passa pra", "mostra isso",
               "mostra pra", "marca alguem que"]
# destinatário específico (bom): pra um pai/mae/avo/quem/alguem que...
DESTINATARIO = ["pra um", "pra uma", "pra quem", "pra alguem", "pro grupo", "pra aquele", "pra aquela",
                "pra outra", "pra outro", "a quem"]
# cota genérica (ruim — engagement bait, suprimido):
COTA = ["5 amigos", "cinco amigos", "marca 5", "marque 5", "compartilhe com todos", "manda pra todos",
        "marca todo mundo", "10 amigos"]


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


if __name__ == "__main__":
    main()
