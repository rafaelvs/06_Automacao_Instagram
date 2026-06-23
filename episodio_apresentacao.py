# -*- coding: utf-8 -*-
"""
VÍDEO DE APRESENTAÇÃO do perfil (Doctoralia / Google / redes) — Dr. Rafael Vargas.
Mesmo motor dos Reels (render_reel + gerar_reel_voz): 9:16 1080x1920, voz Antonio (edge-tts),
cinetipografia + branding preto/creme/dourado, rodapé CRM-SP 226103 · RQE 137901 + disclaimer.

NARRAÇÃO EM 3ª PESSOA (a voz é sintética; um narrador apresenta o Dr. Rafael — NÃO fala "eu sou",
que soaria mal numa voz automática). Estrutura de CONVERSÃO (hook pela dor nos 3s -> quem é -> o que
trata (adulto/criança) -> como trabalha -> foco funcional -> CTA único e acolhedor). ~85s.

NOTA: série começa com "Dr." -> render OCULTA o número de episódio; cena final SEM cta:True (não
exibe o "enviar no direct" do Instagram).

CFM 2.336/2023: educativo; SEM prometer/insinuar resultado, sem sensacionalismo, sem "melhor/exclusivo",
sem antes-e-depois, sem paciente real/identificável. Enquadramento sob FUNÇÃO/movimento. (Decisão do
Rafael: NÃO declarar "nunca estética" no marketing — não afastar pacientes particulares; segue-se sem
prometer resultado estético, mas sem a negação explícita.)

Render: python gerar_reel_voz.py apresentacao_rafael  -> reels/_preview_apresentacao_rafael.mp4
"""

APRESENTACAO = [
 {"id":"apresentacao_rafael","ep":1,"serie":"Dr. Rafael Vargas","temporada":"apresentacao","motif_family":"bone",
  "scenes":[
   # 1) GANCHO — pela dor do paciente (impessoal)
   {"k":"Casos de difícil solução","sc":["Quase sempre","há um caminho."],"e":"caminho",
    "sub":"Perna mais curta, osso que não colou, deformidade na criança.",
    "vo":"Uma perna mais curta que a outra. Um osso que não colou depois da fratura. Uma criança com uma deformidade que preocupa. Muitos ouvem que casos assim não têm solução."},
   # 2) QUEM É — 3ª pessoa
   {"k":"Quem cuida disso","sc":["Dr. Rafael Vargas,","ortopedista."],"e":None,
    "sub":"Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica.",
    "vo":"O Doutor Rafael Vargas é ortopedista em São Paulo, dedicado a duas áreas: a reconstrução e o alongamento ósseo, e a ortopedia da criança."},
   # 3) O QUE TRATA — adulto
   {"k":"No adulto","sc":["Corrigir o eixo,","refazer o osso."],"e":"refazer",
    "sub":"Diferença de comprimento, deformidade, pseudartrose, sequelas de trauma.",
    "vo":"No adulto, ele trata diferenças de comprimento entre as pernas, deformidades e ossos que não consolidaram. Com a técnica de Ilizarov e os fixadores externos, é possível corrigir o eixo e até refazer o osso que faltou."},
   # 4) O QUE TRATA — criança
   {"k":"Na criança","sc":["Olhar no tempo","certo do crescimento."],"e":"certo",
    "sub":"Deformidades dos membros, quadril e jeito de andar.",
    "vo":"Na criança, cuida de deformidades dos membros, de alterações do quadril e da marcha, e de diferenças de comprimento. Olhar no momento certo do crescimento faz toda a diferença."},
   # 5) COMO TRABALHA — onde nasce a confiança
   {"k":"O método","sc":["Com calma e","no milímetro."],"e":"milímetro",
    "sub":"Avaliação, planejamento e correção gradual — cada etapa explicada.",
    "vo":"O cuidado começa por entender cada caso com calma, do exame ao planejamento. A correção é gradual, no milímetro, e cada etapa é explicada ao paciente e à família."},
   # 6) FOCO FUNCIONAL
   {"k":"O foco é sempre um","sc":["Função:","voltar ao movimento."],"e":"Função",
    "sub":"Caminhar, correr, viver com mais autonomia.",
    "vo":"E o foco é sempre a função e o movimento: voltar a caminhar, correr e viver com mais autonomia e qualidade de vida."},
   # 7) CTA — único, acolhedor
   {"k":"O primeiro passo","sc":["Agende uma","avaliação."],"e":"avaliação",
    "sub":"Vamos pensar juntos no melhor caminho.",
    "vo":"Se você, ou alguém que você ama, convive com um caso desses, o primeiro passo é conversar. Agende uma avaliação e entenda as opções para o seu caso."},
  ],
  "caption":("Dr. Rafael Vargas — ortopedista em São Paulo. Reconstrução e Alongamento Ósseo e "
   "Ortopedia Pediátrica: casos de difícil solução em crianças e adultos — diferenças de comprimento "
   "dos membros, deformidades, pseudartrose e sequelas de trauma ou infecção. Avaliação cuidadosa, "
   "planejamento individual e correção gradual, com foco em função e movimento. "
   "Agende uma avaliação.\n\nDr. Rafael Vargas · CRM-SP 226103 · RQE 137901")},
]
