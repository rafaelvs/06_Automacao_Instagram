# -*- coding: utf-8 -*-
"""
Motor de SEO/metadados do YouTube — série "Recuperação".
Gera TÍTULO (padrão variado por episódio → anti-templatização), DESCRIÇÃO (com E-E-A-T + disclaimer
CFM + WhatsApp + hashtags) e TAGS. Fundamentado em ESTRATEGIA_YOUTUBE_2026.md:
 - CTR importa mas é "gated" pela retenção → título promete e o vídeo entrega (sem clickbait vazio).
 - Busca é SEMÂNTICA → título/descrição cobrem o TÓPICO e a INTENÇÃO (como o paciente pesquisa).
 - E-E-A-T (autoridade do cirurgião) é o FOSSO contra o "AI slop" + confiança do paciente (YMYL).
 - Variação: o PADRÃO do título alterna por episódio, então os títulos do canal não têm a mesma cara.

A criatividade fina (título/gancho específicos) pode ser passada à mão (input clínico = E-E-A-T);
este módulo garante ESTRUTURA, VARIAÇÃO e CONFORMIDADE de forma automática e reproduzível.
"""
SIG = ("Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901 — "
       "Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica.")
DISC = "Conteúdo educativo, não substitui a avaliação do seu médico."
WPP = "Dúvidas de rotina: WhatsApp (11) 3280-1413."

# Padrões de título variados. {foco}=tema; {pais}=sufixo p/ versão infantil. Mantêm clareza (não clickbait).
TITLE_PATTERNS = [
    "{foco}: cuidados e sinais de alarme{pais}",
    "Saiu de cirurgia? {foco}{pais}",
    "{foco} no pós-operatório — o que fazer{pais}",
    "Pós-operatório: {foco}{pais}",
    "{foco}: o essencial e quando ir ao pronto-socorro{pais}",
]

def _is_kids(eid): return str(eid).endswith("_kids")

def titulo(episode, foco, idx=None):
    """Título variado e dentro do limite (100). foco = tema curto (ex.: 'Fixador externo')."""
    eid = episode["id"]; pais = " (guia para os pais)" if _is_kids(eid) else ""
    i = (idx if idx is not None else sum(map(ord, eid))) % len(TITLE_PATTERNS)
    t = TITLE_PATTERNS[i].format(foco=foco, pais=pais)
    if "#shorts" not in t.lower():
        t = (t[:100 - len(" #Shorts")]).rstrip() + " #Shorts"
    return t[:100]

def descricao(hook, pontos, hashtags="", fontes=None):
    """Descrição com E-E-A-T + CFM. hook=1ª linha forte; pontos=lista; fontes=lista de URLs (autoridade)."""
    corpo = hook.strip() + "\n\n" + "\n".join("• " + p for p in pontos)
    bloco_fontes = ("\n\nReferências: " + " · ".join(fontes)) if fontes else ""
    tags_line = ("\n\n" + hashtags.strip()) if hashtags else ""
    return f"{corpo}\n\n{WPP}\n\n{SIG}\n{DISC}{bloco_fontes}{tags_line}"

def tags(foco, kids=False):
    base = ["ortopedia", "pós-operatório", "recuperação", "Dr. Rafael Vargas",
            "alongamento ósseo", "reconstrução óssea"]
    if kids: base += ["ortopedia pediátrica", "ortopedia infantil", "pais", "criança"]
    f = foco.lower().strip()
    return base + ([f] if f not in base else [])

def gerar(episode, foco, hook, pontos, hashtags="", fontes=None, idx=None):
    """Conveniência: retorna dict {title, description, tags} pronto p/ o publish/agendamento."""
    kids = _is_kids(episode["id"])
    return {
        "title": titulo(episode, foco, idx),
        "description": descricao(hook, pontos, hashtags, fontes),
        "tags": tags(foco, kids),
    }

if __name__ == "__main__":
    demo = {"id": "fixador_externo"}
    out = gerar(demo, "Fixador externo",
                "Está com fixador externo depois da cirurgia? Veja o cuidado com os pinos — e os sinais que pedem o pronto-socorro.",
                ["Limpe os pinos no banho com sabonete neutro; seque com papel ou ar frio.",
                 "Um material por pino — não cruze a contaminação.",
                 "Vermelhidão, calor, secreção ou febre: pronto-socorro + avise a equipe."],
                "#Shorts #fixadorexterno #ortopedia #alongamentoosseo",
                ["https://orthoinfo.aaos.org", "https://sbot.org.br"])
    print("TÍTULO:", out["title"], "\n"); print("DESCRIÇÃO:\n", out["description"], "\n"); print("TAGS:", out["tags"])
