# -*- coding: utf-8 -*-
"""
LOTE 2026 — POSTS (carrosséis) + STORIES (sequências) DERIVADOS dos 30 reels narrados.
Princípio (Arquitetura de Ganchos 2026 · "semana sincronizada"): story → reel → carrossel falam
do MESMO tema. Em vez de reescrever clínica nova (e arriscar imprecisão), derivamos posts e stories
do conteúdo dos episódios JÁ REVISADO (medicamente + CFM + guardrail). Cada reel ganha:
  • 1 carrossel (capa + slides de conteúdo + CTA) que aprofunda e vira o "salva".
  • 1 sequência de stories (5 frames) que teasa e manda pro reel/carrossel.

Saídas: images/c_<id>_*.jpg (carrossel) e images/s_<id>_*.jpg (stories).
IDs no banco: carrossel "c_<id>", sequência "s_<id>". Roda no GitHub Actions (sem sync OneDrive).
"""
import os
from episodios_novos_2026 import NEW_EPISODES
import carrossel as C
import gerar_sequencias as G

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(ROOT, "images")

def _join(sc):  # ["A","B"] -> "A B" (vira título legível no carrossel/story)
    return " ".join(sc).strip()

CUES = ["deslize →", "continua →", "continua →", "quase lá →"]

def carrossel_de(ep):
    """Deriva os slides do carrossel a partir das cenas do episódio."""
    S = ep["scenes"]
    capa = {"kicker": "Educativo", "title": _join(S[0]["sc"]), "sub": S[0].get("sub", "")}
    slides = [capa]
    for s in S[1:-1]:  # cenas de conteúdo (pula capa e a cena final de "passa adiante")
        slides.append({"kicker": s["k"], "title": _join(s["sc"]), "body": s.get("sub", "")})
    last = S[-1]
    slides.append({"cta": True, "kicker": "Passa adiante",
                   "title": "Salva e compartilha", "sub": last.get("sub", "")})
    return {"id": "c_" + ep["id"], "slides": slides}

def sequencia_de(ep):
    """Deriva os 5 frames da sequência de stories a partir das cenas do episódio."""
    S = ep["scenes"]; n = len(S); theme = ep["serie"]
    dia = []
    for i, s in enumerate(S):
        seg = s["k"]
        title = _join(s["sc"])
        sub = s.get("sub", "")
        if i < n - 1:
            cue = CUES[i] if i < len(CUES) else "continua →"
        else:
            cue = "Salva e manda pra quem precisa ver. 📺 O reel completo está no feed."
        dia.append(("dark", seg, title, sub, cue))
    return ep["id"], theme, dia

def render_tudo():
    os.makedirs(IMG, exist_ok=True)
    posts_imgs = {}; seq_imgs = {}
    for ep in NEW_EPISODES:
        post = carrossel_de(ep)
        paths = C.render_post(post, IMG)
        posts_imgs[post["id"]] = paths
        print("CARROSSEL", post["id"], len(paths), "slides", flush=True)
        sid, theme, dia = sequencia_de(ep)
        out = G.render_dia("s_" + sid, theme, dia)  # salva s_<id>_1..5.jpg em images/
        seq_imgs["s_" + sid] = out
        print("STORIES   s_" + sid, len(out), "frames", flush=True)
    return posts_imgs, seq_imgs

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--one":
        # smoke: renderiza só o 1º episódio
        ep = NEW_EPISODES[0]
        C.render_post(carrossel_de(ep), IMG)
        sid, theme, dia = sequencia_de(ep)
        G.render_dia("s_" + ep["id"], theme, dia)
        print("SMOKE OK:", ep["id"])
    else:
        p, s = render_tudo()
        print("TOTAL carrosséis:", len(p), "| sequências:", len(s))
