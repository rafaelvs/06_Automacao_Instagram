# -*- coding: utf-8 -*-
"""
VÍDEO DE APRESENTAÇÃO do perfil (Doctoralia / Google / redes) — Dr. Rafael Vargas.
Mesmo motor dos Reels (render_reel + gerar_reel_voz): 9:16 1080x1920, voz Antonio (edge-tts),
cinetipografia + branding preto/creme/dourado, rodapé CRM-SP 226103 · RQE 137901 + disclaimer.

Estrutura de CONVERSÃO (pesquisa: hook pela dor nos 3s -> quem é -> o que trata (adulto/criança)
-> como trabalha (onde nasce a confiança) -> foco funcional -> CTA único e acolhedor). ~75s.

CFM 2.336/2023 (inegociável): educativo; SEM prometer/insinuar resultado, sem sensacionalismo,
sem "melhor/exclusivo", sem antes-e-depois, sem paciente real/identificável. Alongamento e
reconstrução SEMPRE sob FUNÇÃO/movimento — NUNCA estética/altura (reforçado na tela na cena 6).

Render: python gerar_reel_voz.py apresentacao_rafael  -> reels/_preview_apresentacao_rafael.mp4
"""

APRESENTACAO = [
 {"id":"apresentacao_rafael","ep":1,"serie":"Dr. Rafael Vargas","temporada":"apresentacao","motif_family":"bone",
  "scenes":[
   # 1) GANCHO — pela dor do paciente, não pelo nome (3s decidem)
   {"k":"Casos de difícil solução","sc":["Quase sempre","há um caminho."],"e":"caminho",
    "sub":"Perna mais curta, osso que não colou, deformidade na criança.",
    "vo":"Uma perna mais curta que a outra. Um osso que não colou depois da fratura. Uma criança com uma deformidade que preocupa. Muitos ouvem que casos assim não têm solução."},
   # 2) QUEM É — uma frase
   {"k":"Quem cuida disso","sc":["Dr. Rafael Vargas,","ortopedista."],"e":None,
    "sub":"Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica.",
    "vo":"Eu sou o Doutor Rafael Vargas, ortopedista em São Paulo. Dedico meu trabalho a duas áreas: a reconstrução e o alongamento ósseo, e a ortopedia da criança."},
   # 3) O QUE TRATA — adulto (autoridade do nicho)
   {"k":"No adulto","sc":["Corrigir o eixo,","refazer o osso."],"e":"refazer",
    "sub":"Diferença de comprimento, deformidade, pseudartrose, sequelas de trauma.",
    "vo":"No adulto, trato diferenças de comprimento entre as pernas, deformidades e ossos que não consolidaram. Com a técnica de Ilizarov e os fixadores externos, é possível corrigir o eixo e até refazer o osso que faltou."},
   # 4) O QUE TRATA — criança
   {"k":"Na criança","sc":["Olhar no tempo","certo do crescimento."],"e":"certo",
    "sub":"Deformidades dos membros, quadril e jeito de andar.",
    "vo":"Na criança, cuido de deformidades dos membros, de alterações do quadril e da marcha, e de diferenças de comprimento. Olhar no momento certo do crescimento faz toda a diferença."},
   # 5) COMO TRABALHA — onde nasce a confiança
   {"k":"Como eu trabalho","sc":["Com calma e","no milímetro."],"e":"milímetro",
    "sub":"Avaliação, planejamento e correção gradual — cada etapa explicada.",
    "vo":"Começo entendendo o caso com calma, do exame ao planejamento. A correção é gradual, no milímetro, e eu explico cada etapa pra você e pra sua família."},
   # 6) FOCO FUNCIONAL — guardrail CFM reforçado na tela
   {"k":"O foco é sempre um","sc":["Função:","voltar ao movimento."],"e":"Função",
    "sub":"Caminhar, correr, viver. Nunca sobre estética.",
    "vo":"E o foco é sempre a função: voltar a caminhar, correr, viver com mais autonomia. Aqui é sobre movimento e qualidade de vida, nunca sobre estética."},
   # 7) CTA — único, acolhedor
   {"k":"O primeiro passo","sc":["Agende uma","avaliação."],"e":"avaliação",
    "sub":"Vamos pensar juntos no melhor caminho.",
    "vo":"Se você, ou alguém que você ama, convive com um caso desses, o primeiro passo é conversar. Agende uma avaliação, e vamos pensar juntos no melhor caminho."},
  ],
  "caption":("Dr. Rafael Vargas — ortopedista em São Paulo. Reconstrução e Alongamento Ósseo e "
   "Ortopedia Pediátrica: casos de difícil solução em crianças e adultos — diferenças de comprimento "
   "dos membros, deformidades, pseudartrose e sequelas de trauma ou infecção. Avaliação cuidadosa, "
   "planejamento individual e correção gradual, sempre com foco em função e movimento. "
   "Agende uma avaliação.\n\nDr. Rafael Vargas · CRM-SP 226103 · RQE 137901")},
]
