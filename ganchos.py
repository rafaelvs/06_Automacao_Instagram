# -*- coding: utf-8 -*-
"""
Arquétipos de gancho (1ª cena) — série "Recuperação".

O gancho forte é a maior alavanca de RETENÇÃO confirmada pela pesquisa ESTRATEGIA_YOUTUBE_2026.md:
os primeiros segundos decidem se o espectador (paciente/familiar) fica ou sai. Cada arquétipo
cria uma abertura diferente, evitando que o canal pareça "templatizado em massa" (política
"Inauthentic Content" do YouTube, enforcement jan/2026).

ROTAÇÃO: determinística por episode_id (hash de caracteres % 6), com offset +3 para _kids —
garante que par adulto+infantil nunca repita o mesmo estilo de abertura.

6 ARQUÉTIPOS
───────────────────────────────────────────────────────────────────────────────────────
1. pergunta       — "Você sabia que…?" / "O que acontece quando…?"
                   Abre um loop cognitivo que o espectador quer fechar.
2. mito_vs_verdade — "Todo mundo acha X — mas a verdade é Y."
                   Gancho de ruptura de expectativa; alta saliência.
3. dado_estatistica — "9 em 10 pacientes…" / "Na maioria das cirurgias…"
                   Ancoragem por dado/proporção; autoridade clínica imediata.
4. micro_caso     — "Você saiu da cirurgia com X. O que vem a seguir?"
                   Empatia de cenário; coloca o paciente no enredo.
5. alerta         — "Atenção: esse sinal pede pronto-socorro."
                   Urgência controlada; retém quem está com o paciente em casa.
6. boa_noticia    — "Boa notícia: você pode fazer isso em casa."
                   Empoderamento e alívio; retém familiares ansiosos.
───────────────────────────────────────────────────────────────────────────────────────

USO TÍPICO ao escrever um episódio novo:
    import ganchos
    arq = ganchos.arquetipo("artrorrise")   # → "micro_caso"
    guia = ganchos.info("artrorrise")       # → dict com desc + dicas de roteiro
    # → escreva a 1ª cena seguindo o guia e adapte ao tema clínico do episódio.
"""

ARCHETYPES = [
    "pergunta",
    "mito_vs_verdade",
    "dado_estatistica",
    "micro_caso",
    "alerta",
    "boa_noticia",
]

# Descrição de cada arquétipo + dicas de roteiro (sc/vo/e)
GUIDE = {
    "pergunta": {
        "desc": "Abre um loop cognitivo — o espectador fica pra fechar a pergunta.",
        "k_sugerido": "VOCÊ SABIA?",
        "sc_dica": "A pergunta em 2 linhas curtas. Deve tocar uma dúvida real do paciente.",
        "vo_dica": "Repita a pergunta em voz e já sugira que a resposta vem a seguir.",
        "e_dica": "Palavra central da pergunta (ex.: 'artrorrise', 'implante', 'cirurgia').",
        "exemplo_sc": ["A artrorrise", "corrige o pé plano?"],
        "exemplo_vo": ("Sabia que a artrorrise corrige o pé plano com um implante pequeníssimo? "
                       "Os cuidados em casa não são complicados — mas têm detalhes que protegem o resultado."),
    },
    "mito_vs_verdade": {
        "desc": "Ruptura de expectativa: desmonta crença errada comum do paciente.",
        "k_sugerido": "MITO OU VERDADE?",
        "sc_dica": "Escreva o mito como afirmação — o espectador já discorda ou concorda e precisa saber.",
        "vo_dica": "Diga o mito, anuncie que é mito, e prometa a verdade em seguida.",
        "e_dica": "'MITO' ou a palavra-chave falsa que o paciente acredita.",
        "exemplo_sc": ["Gesso molhado?", "Deixa secar por si só."],
        "exemplo_vo": ("Muita gente acha que gesso molhado pode secar sozinho. "
                       "Isso é um mito — e pode criar úlcera de pressão em poucos dias."),
    },
    "dado_estatistica": {
        "desc": "Dado/proporção ancora autoridade clínica imediatamente.",
        "k_sugerido": "SABIA QUE...",
        "sc_dica": "Uma proporção ou achado clínico em 2 linhas. Não precisa de percentual exato — 'na maioria' vale.",
        "vo_dica": "Dê o dado, conecte ao que isso significa para o paciente.",
        "e_dica": "O número ou proporção principal.",
        "exemplo_sc": ["A maioria das", "complicações é evitável."],
        "exemplo_vo": ("A maioria das complicações do pós-operatório não surge no hospital — "
                       "surge em casa, nos primeiros dias. E quase todas são evitáveis."),
    },
    "micro_caso": {
        "desc": "Empatia de cenário: o paciente se vê no enredo.",
        "k_sugerido": "SAIU DA CIRURGIA",
        "sc_dica": "Descreva o momento exato em que o paciente está (acabou de operar, está em casa). Concreto.",
        "vo_dica": "Posicione o espectador na situação e prometa as informações que ele precisa agora.",
        "e_dica": "A palavra que nomeia a situação (ex.: 'implante', 'fixador', 'gesso').",
        "exemplo_sc": ["Um implante minúsculo,", "grande diferença."],
        "exemplo_vo": ("Você passou pela artrorrise: um implante pequeno entrou no calcanhar "
                       "pra corrigir o pé plano. O resultado de longo prazo começa nesses primeiros dias em casa."),
    },
    "alerta": {
        "desc": "Urgência controlada: retém quem está com o paciente e precisa reconhecer sinais.",
        "k_sugerido": "ATENÇÃO",
        "sc_dica": "Nomeie o sinal de alarme principal do tema. Deve ser concreto e reconhecível.",
        "vo_dica": "Diga qual é o sinal, por que importa, e que o vídeo vai explicar como agir.",
        "e_dica": "O sinal de alarme principal (ex.: 'dor crescente', 'dedos roxos').",
        "exemplo_sc": ["Dor crescente", "depois da cirurgia?"],
        "exemplo_vo": ("Dor que vai aumentando depois da cirurgia não é normal. "
                       "Pode ser um sinal precoce de complicação — e reconhecer cedo muda tudo."),
    },
    "boa_noticia": {
        "desc": "Empoderamento/alívio: retém familiares ansiosos e devolve senso de controle.",
        "k_sugerido": "BOA NOTÍCIA",
        "sc_dica": "Anuncie um benefício concreto que o paciente/família vai sentir ao terminar o vídeo.",
        "vo_dica": "Dê a boa notícia de cara, e diga que o vídeo vai mostrar como garantir esse resultado.",
        "e_dica": "O benefício principal (ex.: 'recuperação', 'segurança', 'autonomia').",
        "exemplo_sc": ["Cuidar em casa", "não é complicado."],
        "exemplo_vo": ("Boa notícia: cuidar do fixador externo em casa não é complicado. "
                       "Com alguns passos simples, você evita a complicação mais comum."),
    },
}


def arquetipo(episode_id: str) -> str:
    """Retorna o nome do arquétipo determinístico para o episódio.

    _kids recebe offset +3 para garantir variação em relação ao par adulto.
    """
    idx = sum(map(ord, str(episode_id))) % len(ARCHETYPES)
    if str(episode_id).endswith("_kids"):
        idx = (idx + 3) % len(ARCHETYPES)
    return ARCHETYPES[idx]


def info(episode_id: str) -> dict:
    """Retorna o guia completo do arquétipo atribuído ao episódio."""
    nome = arquetipo(episode_id)
    return {"arquetipo": nome, **GUIDE[nome]}


def resumo_todos() -> None:
    """Imprime tabela de arquétipos × episódios (debug/planejamento)."""
    ids = [
        "gesso_pos_op", "gesso_pos_op_kids",
        "fixador_externo", "fixador_externo_kids",
        "carga_fisio", "carga_fisio_kids",
        "artrorrise", "artrorrise_kids",
        "growth_guided", "growth_guided_kids",
    ]
    print(f"{'ID':<30} {'ARQUÉTIPO'}")
    print("-" * 50)
    for eid in ids:
        print(f"{eid:<30} {arquetipo(eid)}")


if __name__ == "__main__":
    resumo_todos()
    print()
    g = info("artrorrise")
    print(f"Artrorrise -> {g['arquetipo']}: {g['desc']}")
    print(f"  k: {g['k_sugerido']}")
    print(f"  sc: {g['exemplo_sc']}")
    print(f"  vo: {g['exemplo_vo']}")
