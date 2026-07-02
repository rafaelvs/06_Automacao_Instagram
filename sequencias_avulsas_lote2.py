# -*- coding: utf-8 -*-
"""Sequências AVULSAS — LOTE 2 (fix P0.3 auditoria v5): +28 sequências de stories
(14 "Pé no Chão" — ortopedia pediátrica + 14 "Osso Novo" — reconstrução/alongamento no adulto).

Renderiza 5 frames por sequência com o MESMO template seq_story() das sequências
existentes e ANEXA os itens a sequences.json (não mexe em nada já publicado).

Rode:  python sequencias_avulsas_lote2.py           -> audita CFM, renderiza e anexa
       python sequencias_avulsas_lote2.py --audit   -> só roda a auditoria CFM (sem renderizar)

Conformidade CFM 2.336/2023: educativo, sem promessa de resultado, sem estética/altura,
sem "dismetria", assinatura (SIG: CRM-SP 226103 · RQE 137901 · Médico) no rodapé de todo frame.
"""
import os
import sys
import json

import gerar_conteudo as gc

# ---- Fallback de fontes p/ render local no Windows (nuvem usa Liberation em /usr/share/fonts) ----
if not os.path.isdir(gc.FD):
    from PIL import ImageFont
    _WINF = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
    # Arial/Times são metricamente compatíveis com Liberation Sans/Serif
    _MAP = {
        "LiberationSerif-Bold.ttf": "timesbd.ttf",
        "LiberationSans-Regular.ttf": "arial.ttf",
        "LiberationSans-Bold.ttf": "arialbd.ttf",
    }

    def _F(n, s):
        return ImageFont.truetype(os.path.join(_WINF, _MAP.get(n, n)), s)

    gc.F = _F

from gerar_sequencias import seq_story  # importa DEPOIS do patch de fonte
from cfm_guardrails import auditar

SIG = gc.SIG
ROOT = gc.ROOT
IMG = gc.IMG

# ---------------------------------------------------------------------------
# 28 sequências novas. Formato: (id, theme, variant, [(segmento, titulo, sub, cue) x5])
# label do item = segmento do frame 1 (mesmo padrão das avulsas existentes).
# ---------------------------------------------------------------------------
NOVAS = [

# ======================= PÉ NO CHÃO (14) =======================

("s_pnc_torcicolo_bebe", "Pé no Chão", "dark", [
 ("Pé no Chão · Pescoço torto do bebê", "Cabeça sempre virada pro mesmo lado?",
  "Pode ser torcicolo congênito (um encurtamento no músculo do pescoço). Quanto mais cedo se percebe, mais simples costuma ser o cuidado.", "deslize →"),
 ("O que é", "Um músculo mais curto",
  "No torcicolo congênito, um músculo do pescoço (o esternocleidomastóideo) nasce mais tenso de um lado. A cabeça inclina para um lado e gira para o outro.", "continua →"),
 ("Como perceber", "Sinais no dia a dia",
  "Bebê que só mama bem de um lado, cabeça inclinada nas fotos, achatamento atrás da cabeça sempre do mesmo lado: vale avaliação.", "continua →"),
 ("O que ajuda", "Estímulo e fisioterapia",
  "Alternar o lado no berço e no colo, estimular o bebê a olhar para os dois lados e fisioterapia orientada costumam responder bem na maioria dos casos.", "quase lá →"),
 ("Guarde isso", "Percebeu? Avalie cedo",
  "Avaliação precoce simplifica o acompanhamento. Compartilha com quem tem bebê em casa.", "Dúvidas? Manda DM →")]),

("s_pnc_charutinho_quadril", "Pé no Chão", "light", [
 ("Pé no Chão · Perninhas livres", "Enfaixar o bebê apertado faz mal?",
  "O famoso charutinho acalma, mas do jeito errado pode atrapalhar o quadril. Vem entender a posição que protege.", "deslize →"),
 ("O que acontece", "O quadril gosta de flexão",
  "O quadril do bebê ainda está amadurecendo. Pernas esticadas e apertadas por muito tempo dificultam o encaixe natural da articulação.", "continua →"),
 ("O jeito certo", "Enrole folgado embaixo",
  "Se for enfaixar, deixe as perninhas soltas, dobradas e abertas — livres para mexer. Aperto só do tronco pra cima, e por períodos curtos.", "continua →"),
 ("No canguru", "Posição de M",
  "No carregador, joelhos mais altos que o bumbum, como um M. Essa posição respeita o desenvolvimento do quadril.", "quase lá →"),
 ("Guarde isso", "Perninhas livres, quadril protegido",
  "Salva e manda pra quem vai ter bebê. Ficou com dúvida sobre o quadril do seu bebê? Manda DM.", "Compartilha com quem precisa →")]),

("s_pnc_osso_forte", "Pé no Chão", "dark", [
 ("Pé no Chão · Poupança de osso", "Osso forte se constrói na infância",
  "A infância e a adolescência são a janela de ouro para formar massa óssea. O que dá pra fazer em casa? Vem ver.", "deslize →"),
 ("No prato", "Cálcio todo dia",
  "Leite e derivados, feijão, vegetais verde-escuros. O cálcio é o tijolo do osso — e a necessidade aumenta na adolescência.", "continua →"),
 ("No sol", "Vitamina D de verdade",
  "Sol no dia a dia, com bom senso, ajuda o corpo a produzir vitamina D — ela leva o cálcio até o osso. Suplemento, só com orientação.", "continua →"),
 ("No movimento", "Pular, correr, pendurar",
  "Impacto leve e variado (correr, pular corda, subir em árvore) estimula o osso a ficar mais denso. Tela demais rouba esse tempo.", "quase lá →"),
 ("Guarde isso", "É poupança para a vida",
  "O osso que se forma agora é a reserva lá na frente. Salva pra lembrar.", "Compartilha com quem tem filhos →")]),

("s_pnc_hipermobilidade", "Pé no Chão", "light", [
 ("Pé no Chão · Elástica demais?", "Criança que dobra demais as juntas",
  "Dedos que vão longe, cotovelo que passa da linha, posições impossíveis no chão. Flexibilidade normal ou algo mais?", "deslize →"),
 ("O que é", "Hipermobilidade articular",
  "É quando as articulações têm mais amplitude que o habitual (juntas mais 'soltas'). Em muitas crianças é só uma característica, sem doença.", "continua →"),
 ("Quando observar", "Dor, entorses, cansaço",
  "Dor frequente depois de atividade, tornozelos que torcem toda hora ou cansaço para acompanhar os colegas: vale avaliação.", "continua →"),
 ("O que ajuda", "Músculo dá estabilidade",
  "Fortalecer com atividade regular ajuda a estabilizar articulações mais frouxas. Esporte orientado costuma ser aliado, não vilão.", "quase lá →"),
 ("Guarde isso", "Flexível pode. Com dor, avalie",
  "Salva esse resumo e manda pra quem tem uma criança 'elástica' em casa.", "Dúvidas? Manda DM →")]),

("s_pnc_capacete_protecao", "Pé no Chão", "dark", [
 ("Pé no Chão · Sobre rodinhas", "Patinete, bike e skate com proteção",
  "As rodinhas fazem bem ao corpo em crescimento — e boa parte das quedas com fratura tem um ponto em comum: faltou equipamento.", "deslize →"),
 ("O ponto fraco", "Punho é o primeiro a sofrer",
  "Ao cair, a mão vai na frente. Fraturas de punho e antebraço estão entre as mais comuns da infância sobre rodinhas.", "continua →"),
 ("O kit que importa", "Capacete + punho + joelho",
  "Capacete do tamanho certo, protetor de punho, joelheira e cotoveleira. No patinete elétrico, redobre a atenção: velocidade muda tudo.", "continua →"),
 ("O combinado", "Regra da casa, sem exceção",
  "Proteção desde o primeiro dia, mesmo no trajeto curto. Criança copia o exemplo: adulto de capacete ensina mais que discurso.", "quase lá →"),
 ("Guarde isso", "Diversão sim, proteção junto",
  "Salva e compartilha com a família que tem rodinhas em casa.", "Compartilha com quem precisa →")]),

("s_pnc_crescer_dormindo", "Pé no Chão", "light", [
 ("Pé no Chão · Crescer dormindo", "Seu filho cresce enquanto dorme",
  "É durante o sono profundo que o corpo libera a maior parte do hormônio do crescimento. Rotina de sono é assunto de osso também.", "deslize →"),
 ("Como funciona", "O pico é à noite",
  "O hormônio do crescimento (GH) tem seus maiores picos nas primeiras horas de sono profundo. Noites muito curtas encurtam esse estímulo.", "continua →"),
 ("Quanto precisa", "Horas por idade",
  "Em média: pré-escolar, 10 a 13h; escolar, 9 a 12h; adolescente, 8 a 10h. O padrão da semana importa mais que um dia ruim.", "continua →"),
 ("O que atrapalha", "Tela na cama",
  "Luz de tela à noite atrasa o sono. Quarto escuro, horário regular e tela fora do quarto ajudam mais do que parecem.", "quase lá →"),
 ("Guarde isso", "Sono também é crescimento",
  "Salva pra rever na próxima negociação de horário de dormir.", "Compartilha com outros pais →")]),

("s_pnc_primeira_consulta", "Pé no Chão", "dark", [
 ("Pé no Chão · A primeira consulta", "Vai ao ortopedista infantil? Leve isso",
  "Uma consulta rende mais quando a família chega preparada. Quatro coisas que ajudam muito na avaliação.", "deslize →"),
 ("Dica 1", "Filme a queixa em casa",
  "Mancar, andar 'torto', pé pra dentro: o celular mostra o que a criança nem sempre repete no consultório. Vídeos curtos, de frente e de costas.", "continua →"),
 ("Dica 2", "Linha do tempo da queixa",
  "Quando começou, o que piora, o que melhora, se houve queda ou febre. Anotar antes evita esquecer na hora.", "continua →"),
 ("Dicas 3 e 4", "Roupa prática e exames antigos",
  "Shorts facilita examinar joelhos e quadris. E leve relatórios e exames anteriores, se existirem — o histórico vale ouro.", "quase lá →"),
 ("Guarde isso", "Preparo ajuda o diagnóstico",
  "Salva essa lista pra véspera da consulta.", "Dúvidas? Manda DM →")]),

("s_pnc_gesso_em_casa", "Pé no Chão", "light", [
 ("Pé no Chão · Gesso sem drama", "Criança de gesso em casa: guia rápido",
  "O gesso protege — mas a rotina muda. O que pode, o que não pode e os sinais que pedem contato imediato.", "deslize →"),
 ("O que não pode", "Molhar e cutucar",
  "Gesso molhado perde a função e machuca a pele. E nada de enfiar objetos para coçar — arranhões escondidos podem infeccionar.", "continua →"),
 ("O que ajuda", "Coceira e inchaço",
  "Ar frio de secador (nunca quente) alivia a coceira. Manter o membro elevado nos primeiros dias reduz o inchaço.", "continua →"),
 ("Sinais de alerta", "Dor que só aumenta",
  "Dedos roxos, gelados ou dormentes, dor que cresce apesar do remédio, cheiro forte ou febre: entre em contato no mesmo dia.", "quase lá →"),
 ("Guarde isso", "Gesso tranquilo é gesso vigiado",
  "Salva pra consultar durante as semanas de gesso.", "Compartilha com quem precisa →")]),

("s_pnc_depois_do_gesso", "Pé no Chão", "dark", [
 ("Pé no Chão · Depois do gesso", "Tirou o gesso e o braço está fininho?",
  "Calma: isso é esperado. Entenda o que acontece com o músculo e como costuma ser a volta ao normal.", "deslize →"),
 ("O que aconteceu", "Músculo parado encolhe",
  "Semanas sem uso levam à atrofia (perda temporária de massa muscular). A pele descama e a articulação fica rígida no começo.", "continua →"),
 ("A volta", "Movimento é o caminho",
  "O uso no dia a dia recupera boa parte sozinho. Em alguns casos, a fisioterapia organiza e encurta essa fase.", "continua →"),
 ("No esporte", "Retorno em etapas",
  "Brincadeira leve primeiro, esporte com contato por último, conforme a liberação médica. Pressa aqui costuma custar caro.", "quase lá →"),
 ("Guarde isso", "Fininho é fase",
  "Salva pra lembrar quando chegar o dia de tirar o gesso.", "Dúvidas? Manda DM →")]),

("s_pnc_joanete_adolescente", "Pé no Chão", "light", [
 ("Pé no Chão · Joanete jovem", "Joanete não é só coisa de avó",
  "O hálux valgo juvenil (o joanete do adolescente) existe — e costuma ter história de família. O que observar cedo.", "deslize →"),
 ("O que é", "O dedão que desvia",
  "No hálux valgo (joanete), o dedão aponta para os outros dedos e o 'osso' salta na lateral do pé. No jovem, tende a progredir com o crescimento.", "continua →"),
 ("Por que aparece", "Genética na frente do sapato",
  "A herança familiar pesa mais que o calçado. Sapato apertado e de bico fino não cria o joanete, mas pode incomodar mais.", "continua →"),
 ("O que fazer", "Conforto e acompanhamento",
  "Calçado confortável e avaliação periódica. Cirurgia no adolescente é decisão criteriosa, estudada caso a caso com a família.", "quase lá →"),
 ("Guarde isso", "Dedão desviando? Observa e avalia",
  "Compartilha com quem já notou o pé parecido com o da família.", "Dúvidas? Manda DM →")]),

("s_pnc_musculacao", "Pé no Chão", "dark", [
 ("Pé no Chão · Musculação trava?", "Musculação trava o crescimento?",
  "O mito que atravessa gerações de academia. O que a ortopedia pediátrica diz sobre treino de força na adolescência.", "deslize →"),
 ("O mito", "De onde veio a ideia",
  "O medo era machucar a cartilagem de crescimento. Mas treino de força bem orientado não mostrou esse efeito nos estudos.", "continua →"),
 ("A verdade", "Força bem feita ajuda",
  "Com técnica, progressão e supervisão, o treino de força fortalece músculo e osso — e pode reduzir lesões no esporte.", "continua →"),
 ("O cuidado real", "O problema é o exagero",
  "O risco mora na técnica ruim, na carga além da conta e na competição de ego. Adolescente não treina como adulto — e não precisa.", "quase lá →"),
 ("Guarde isso", "Supervisão vale mais que proibição",
  "Manda pra quem ainda repete esse mito no grupo da família.", "Compartilha com quem precisa →")]),

("s_pnc_esporte_apos_fratura", "Pé no Chão", "light", [
 ("Pé no Chão · De volta ao jogo", "Fraturou. Quando volta ao esporte?",
  "A pergunta mais ouvida no consultório depois que o gesso sai. A resposta tem etapas — e bons motivos.", "deslize →"),
 ("Etapa 1", "O osso colar não basta",
  "A consolidação (o osso 'colar') é só o começo. Músculo, movimento e confiança também precisam voltar.", "continua →"),
 ("Etapa 2", "Do leve ao contato",
  "Primeiro o dia a dia sem dor, depois corrida e habilidades, por último contato e competição. Cada fase é liberada na consulta.", "continua →"),
 ("O porquê", "Refraturar é o risco real",
  "Voltar antes da hora aumenta a chance de nova fratura no mesmo lugar. Semanas de paciência agora costumam poupar meses depois.", "quase lá →"),
 ("Guarde isso", "Volta em fases, não em datas",
  "Salva pra mostrar pro atleta apressado da casa.", "Dúvidas? Manda DM →")]),

("s_pnc_cama_elastica", "Pé no Chão", "dark", [
 ("Pé no Chão · Pula-pula em foco", "Cama elástica: diversão com regras",
  "É uma das grandes fontes de fratura infantil em festas e parques. Dá pra pular com menos risco? Dá — com 4 regras.", "deslize →"),
 ("Regra 1", "Um por vez",
  "A maioria das lesões acontece com duas ou mais crianças pulando juntas — e o menor costuma levar a pior no quique duplo.", "continua →"),
 ("Regra 2", "Idade mínima importa",
  "Menores de 6 anos têm ossos e coordenação ainda em construção; para eles, o risco é desproporcional. Melhor esperar.", "continua →"),
 ("Regras 3 e 4", "Rede fechada, zero acrobacia",
  "Rede de proteção fechada, molas cobertas e nada de mortal ou estrela — as lesões mais graves costumam vir de acrobacia.", "quase lá →"),
 ("Guarde isso", "Festa boa termina sem gesso",
  "Compartilha com quem vai alugar pula-pula na próxima festa.", "Compartilha com quem precisa →")]),

("s_pnc_casa_segura", "Pé no Chão", "light", [
 ("Pé no Chão · Casa à prova de tombo", "Onde a criança fratura? Muitas vezes em casa",
  "Boa parte das fraturas infantis acontece dentro de casa. Quatro pontos para revisar hoje, cômodo por cômodo.", "deslize →"),
 ("Ponto 1", "Beliche e altura",
  "Cama de cima só depois dos 6 anos, e com grade. Quedas de beliche, escada e trocador estão entre as mais sérias.", "continua →"),
 ("Ponto 2", "Janela e sacada",
  "Rede de proteção instalada e móveis longe das janelas. Criança escala antes de entender o risco.", "continua →"),
 ("Pontos 3 e 4", "Tapete solto e chão molhado",
  "Tapete com antiderrapante, brinquedo fora do caminho e atenção redobrada no banheiro — o cenário do escorregão clássico.", "quase lá →"),
 ("Guarde isso", "Prevenir é revisar",
  "Salva e faz o tour pela casa ainda hoje.", "Compartilha com quem tem criança em casa →")]),

# ======================= OSSO NOVO (14) =======================

("s_on_fixador_rotina", "Osso Novo", "dark", [
 ("Osso Novo · A vida com o fixador", "Dá pra viver bem com fixador externo?",
  "Roupa, sono, banho, sair de casa: o aparelho assusta no início, mas a rotina se adapta. Guia prático em 4 pontos.", "deslize →"),
 ("Roupa", "Largo, com botão ou velcro",
  "Calças largas, abertas na lateral ou adaptadas com velcro vestem por cima do fixador. Uma costureira pode virar aliada do tratamento.", "continua →"),
 ("Sono", "Travesseiro é ferramenta",
  "Apoiar a perna em travesseiros protege o aparelho e o outro membro. Capa de tecido no fixador evita enroscar no lençol.", "continua →"),
 ("Rua", "Sair de casa, sim",
  "Com o apoio liberado e muletas quando indicadas, a maioria circula, estuda e convive normalmente durante o tratamento.", "quase lá →"),
 ("Guarde isso", "O aparelho vira rotina",
  "Manda pra quem vai começar um tratamento com fixador.", "Dúvidas? Manda DM →")]),

("s_on_dirigir_trabalho", "Osso Novo", "light", [
 ("Osso Novo · Trabalho e direção", "Posso trabalhar e dirigir no tratamento?",
  "Duas das primeiras perguntas de quem usa fixador ou está em recuperação óssea. A resposta honesta: depende — e de quê.", "deslize →"),
 ("Trabalho", "Depende da função",
  "Trabalho de escritório costuma voltar mais cedo, com adaptações. Trabalho físico pesado espera mais — o osso em formação dita o ritmo.", "continua →"),
 ("Direção", "Perna, câmbio e remédio",
  "Pesam: qual membro foi operado, câmbio manual ou automático e analgésicos que reduzem o reflexo. Sem liberação médica, não dirija.", "continua →"),
 ("O caminho", "Combine, não arrisque",
  "Cada liberação é individual e entra no plano de tratamento. Levar as demandas do seu trabalho à consulta ajuda a planejar as etapas.", "quase lá →"),
 ("Guarde isso", "A rotina volta por etapas",
  "Salva pra organizar essa conversa com o seu médico.", "Dúvidas? Manda DM →")]),

("s_on_pisar_ou_nao", "Osso Novo", "dark", [
 ("Osso Novo · Pisa ou não pisa?", "Pisar com o fixador: pode?",
  "Muita gente acha que osso em tratamento pede repouso absoluto. Na reconstrução, muitas vezes é o contrário.", "deslize →"),
 ("O princípio", "Osso responde a estímulo",
  "Carga controlada 'avisa' o osso de que ele é necessário — o estímulo mecânico participa da consolidação (o colar do osso).", "continua →"),
 ("Na prática", "Apoio progressivo",
  "Começa parcial, com muletas ou andador, e evolui conforme a fase. Quem define o quanto pisar é o plano de tratamento — não a coragem.", "continua →"),
 ("O equilíbrio", "Nem falta, nem excesso",
  "Repouso demais enfraquece músculo e osso; carga além da liberada sobrecarrega a montagem. O meio-termo é individual.", "quase lá →"),
 ("Guarde isso", "Pisar faz parte do tratamento",
  "Compartilha com quem está nessa fase e tem medo de apoiar.", "Dúvidas? Manda DM →")]),

("s_on_comida_do_osso", "Osso Novo", "light", [
 ("Osso Novo · O prato do osso", "O que comer enquanto o osso consolida?",
  "Nenhum alimento cola osso sozinho — mas a falta de alguns atrapalha, e muito. O que costuma entrar no radar nessa fase.", "deslize →"),
 ("Proteína", "O tijolo esquecido",
  "A base do osso é colágeno — proteína. Carnes, ovos, leguminosas e laticínios todos os dias: na consolidação, a necessidade aumenta.", "continua →"),
 ("Cálcio e vitamina D", "A dupla clássica",
  "Cálcio é matéria-prima; a vitamina D o leva até o osso. Sol com bom senso e, se o exame de sangue indicar, suplemento com orientação.", "continua →"),
 ("O que atrapalha", "Cigarro, álcool e dieta pobre",
  "Cigarro reduz a chegada de sangue ao osso; álcool em excesso e dieta pobre atrasam o processo. Hidratação também conta.", "quase lá →"),
 ("Guarde isso", "O prato é parte do tratamento",
  "Salva e revisa sua semana de refeições.", "Compartilha com quem precisa →")]),

("s_on_muletas_sem_erro", "Osso Novo", "dark", [
 ("Osso Novo · Muleta sem erro", "Muleta mal ajustada atrapalha",
  "Altura errada, apoio errado, medo de cair: os erros mais comuns — e os acertos que mudam a marcha na recuperação.", "deslize →"),
 ("Erro 1", "Apoiar na axila",
  "O peso vai nas mãos, não na axila. Apoio axilar comprime nervos e pode causar formigamento e fraqueza no braço.", "continua →"),
 ("Erro 2", "Altura errada",
  "Em pé: o topo da muleta fica 2 a 3 dedos abaixo da axila, com o cotovelo levemente dobrado no apoio das mãos. Ajustar vale a pena.", "continua →"),
 ("Escada", "A regra da escada",
  "Subir: perna boa primeiro. Descer: muletas e perna em tratamento primeiro. Corrimão sempre que existir.", "quase lá →"),
 ("Guarde isso", "Ajuste fino, marcha melhor",
  "Manda pra quem acabou de sair da cirurgia com muletas.", "Dúvidas? Manda DM →")]),

("s_on_dia_da_retirada", "Osso Novo", "light", [
 ("Osso Novo · O dia de tirar", "Chegou o dia de tirar o fixador. E agora?",
  "A retirada é comemorada — e também abre uma fase que merece respeito: o osso novo ainda está amadurecendo.", "deslize →"),
 ("Como é", "A retirada em si",
  "Em geral é um procedimento rápido, muitas vezes com sedação leve. Os pequenos orifícios dos pinos cicatrizam em poucos dias.", "continua →"),
 ("A fase seguinte", "O osso ainda amadurece",
  "O regenerado (o osso recém-formado) segue ganhando resistência por meses. Por isso alguns casos usam órtese ou carga controlada.", "continua →"),
 ("O cuidado", "Proteção sem prisão",
  "A vida avança, mas impacto e torção esperam a liberação por etapas. É a reta final — ainda não a linha de chegada.", "quase lá →"),
 ("Guarde isso", "Depois do fixador vem a maturação",
  "Compartilha com quem está contando os dias pra retirada.", "Dúvidas? Manda DM →")]),

("s_on_enxerto_osseo", "Osso Novo", "dark", [
 ("Osso Novo · Osso emprestado", "Enxerto ósseo: a ajuda que o osso recebe",
  "Em falhas ósseas e consolidações difíceis, dá para 'emprestar' osso. De onde ele vem e como funciona, sem mistério.", "deslize →"),
 ("O que é", "Um estímulo biológico",
  "O enxerto preenche a falha e leva células e estrutura que estimulam o corpo a formar osso novo naquele lugar.", "continua →"),
 ("De onde vem", "Do próprio corpo ou do banco",
  "O mais comum é usar osso do próprio paciente (como o da bacia). Também existem enxertos de banco de tecidos e substitutos sintéticos.", "continua →"),
 ("Quando entra", "Cada caso, uma estratégia",
  "Pseudoartrose (quando o osso não cola), falhas após trauma ou infecção: o enxerto é uma das ferramentas — às vezes somado ao transporte ósseo.", "quase lá →"),
 ("Guarde isso", "Falha óssea tem opções de tratamento",
  "Salva e manda pra quem ouviu falar em enxerto na consulta.", "Dúvidas? Manda DM →")]),

("s_on_fratura_exposta", "Osso Novo", "light", [
 ("Osso Novo · Fratura exposta", "Fratura exposta: por que é outra história",
  "Quando o osso rompe a pele, o cuidado muda de patamar. Entenda por que esse trauma exige mais etapas.", "deslize →"),
 ("O problema", "A porta aberta",
  "Com a pele rompida, bactérias alcançam o osso. O risco de infecção é o que diferencia a fratura exposta das demais.", "continua →"),
 ("O tratamento", "Limpeza antes de tudo",
  "Limpeza cirúrgica, antibiótico precoce e estabilização — muitas vezes com fixador externo — vêm antes da reconstrução definitiva.", "continua →"),
 ("O caminho", "Etapas, não pressa",
  "Casos graves são tratados por fases: primeiro controlar ferida e infecção, depois reconstruir osso e cobertura. Cada etapa tem seu porquê.", "quase lá →"),
 ("Guarde isso", "Trauma grave pede plano",
  "Compartilha — entender o processo acalma quem está vivendo isso.", "Dúvidas? Manda DM →")]),

("s_on_ilizarov_quem_foi", "Osso Novo", "dark", [
 ("Osso Novo · Quem foi Ilizarov", "O médico que mudou a reconstrução óssea",
  "A técnica que uso na reconstrução tem nome e história: Gavriil Ilizarov, um médico da Sibéria nos anos 1950.", "deslize →"),
 ("A história", "Da Sibéria para o mundo",
  "Atendendo feridos de guerra com poucos recursos, Ilizarov criou um anel de fixação externa — e observou algo inesperado.", "continua →"),
 ("A descoberta", "O osso que se regenera",
  "Afastado aos poucos (a chamada osteogênese por distração), o osso forma osso novo no espaço. Nascia a base do alongamento e do transporte ósseo.", "continua →"),
 ("O legado", "Método vivo até hoje",
  "Décadas depois, os princípios de Ilizarov seguem na base dos fixadores circulares e das reconstruções modernas, com tecnologia somada.", "quase lá →"),
 ("Guarde isso", "Ciência com história",
  "Salva e compartilha com quem gosta de saber de onde vêm as técnicas.", "Compartilha com quem precisa →")]),

("s_on_consulta_de_controle", "Osso Novo", "light", [
 ("Osso Novo · A consulta de controle", "Por que tantos retornos no alongamento?",
  "Quem trata osso com fixador vive de consulta em consulta. Não é exagero: é o método. O que se ajusta em cada visita.", "deslize →"),
 ("O que se avalia", "Ritmo e alinhamento",
  "A formação do osso novo é acompanhada de perto para ajustar velocidade e direção. Osso vivo muda — e o plano acompanha.", "continua →"),
 ("O que se ajusta", "Milímetros e prazos",
  "Ajustes finos no aparelho, na carga liberada e na fisioterapia. Pequenas correções cedo costumam evitar grandes desvios depois.", "continua →"),
 ("Seu papel", "Anote entre as consultas",
  "Dor nova, secreção no pino, dificuldade no ajuste: anotar e avisar cedo faz diferença. Consulta boa é via de mão dupla.", "quase lá →"),
 ("Guarde isso", "Controle de perto, plano no rumo",
  "Salva pra lembrar de anotar antes do próximo retorno.", "Dúvidas? Manda DM →")]),

("s_on_esporte_depois", "Osso Novo", "dark", [
 ("Osso Novo · De volta ao movimento", "Esporte depois da reconstrução: dá?",
  "Depois de meses de fixador ou haste, o corpo pede movimento. A volta é possível em muitos casos — e tem método.", "deslize →"),
 ("Fase 1", "Base antes de impacto",
  "Força, equilíbrio e amplitude vêm primeiro. Bicicleta ergométrica, piscina e musculação orientada costumam abrir o caminho.", "continua →"),
 ("Fase 2", "Impacto progressivo",
  "Caminhada vira trote, trote vira corrida — conforme a maturação do osso e a resposta do corpo. Sem pular etapas.", "continua →"),
 ("A régua", "O osso dita o calendário",
  "Cada liberação depende da resistência do osso reconstruído, avaliada nas consultas. Cada osso tem seu tempo — comparação não ajuda.", "quase lá →"),
 ("Guarde isso", "Movimento é meta, não pressa",
  "Manda pra quem está nessa jornada e sonha com a volta.", "Dúvidas? Manda DM →")]),

("s_on_colou_torto", "Osso Novo", "light", [
 ("Osso Novo · Colou torto. E agora?", "Osso que colou torto: e agora?",
  "A consolidação viciosa (quando a fratura cola fora do lugar) pode incomodar anos depois. Entenda quando tratar — e como.", "deslize →"),
 ("O que é", "Consolidação viciosa",
  "O osso é eficiente em colar, mas nem sempre no alinhamento ideal. Desvios maiores mudam a mecânica de joelho, tornozelo e quadril.", "continua →"),
 ("Sinais", "Dor e sobrecarga fora de hora",
  "Dor articular, sensação de membro torto ou mais curto (discrepância de membro) e desgaste de um lado só: vale investigar a origem.", "continua →"),
 ("O tratamento", "Replanejar o alinhamento",
  "Com osteotomia (um corte planejado no osso) e fixação, é possível realinhar. Cada caso é estudado — nem todo desvio precisa de cirurgia.", "quase lá →"),
 ("Guarde isso", "Torto não é sentença",
  "Compartilha com quem convive com sequela de fratura antiga.", "Dúvidas? Manda DM →")]),

("s_on_dor_no_alongamento", "Osso Novo", "dark", [
 ("Osso Novo · E a dor?", "Alongamento ósseo dói?",
  "Pergunta honesta merece resposta honesta: existe desconforto, sim — e existe manejo. O que esperar em cada fase.", "deslize →"),
 ("O esperado", "Desconforto que acompanha",
  "Nos dias de ajuste, sensação de pressão e dor muscular são comuns. Analgesia planejada e fisioterapia fazem parte do plano desde o início.", "continua →"),
 ("O que ajuda", "Manejo em camadas",
  "Medicação em horários certos, alongamento muscular, posicionamento e sono cuidado. Dor controlada é meta de tratamento, não luxo.", "continua →"),
 ("O alerta", "Dor que muda de padrão",
  "Dor que dispara de repente, não cede com a medicação ou vem com vermelhidão e febre: avise a equipe — pode pedir ajuste do plano.", "quase lá →"),
 ("Guarde isso", "Dor se conversa, não se aguenta",
  "Manda pra quem vai começar e tem essa dúvida calada.", "Dúvidas? Manda DM →")]),

("s_on_remedio_que_atrapalha", "Osso Novo", "light", [
 ("Osso Novo · Remédio que atrapalha", "O anti-inflamatório pode atrasar seu osso",
  "Pouca gente sabe: alguns remédios comuns interferem na consolidação. Vale ler antes de tomar por conta própria.", "deslize →"),
 ("O motivo", "Inflamação é etapa",
  "A primeira fase do osso colar é inflamatória. Bloquear demais esse processo com anti-inflamatórios pode atrapalhar o início da consolidação.", "continua →"),
 ("Quais", "AINEs em uso prolongado",
  "Anti-inflamatórios não esteroides (ibuprofeno, diclofenaco e similares) em uso prolongado são os principais suspeitos nos estudos.", "continua →"),
 ("O caminho", "Dor tem alternativa",
  "Existem analgésicos que não interferem no osso. A equipe monta o esquema para cada fase — sempre informe tudo o que você toma.", "quase lá →"),
 ("Guarde isso", "Remédio também é assunto de consulta",
  "Compartilha com quem está consolidando uma fratura.", "Dúvidas? Manda DM →")]),
]


def auditar_novas(verbose=True):
    """Roda cfm_guardrails.auditar sobre TODOS os textos novos (frame completo + SIG do rodapé,
    que é desenhado em todo frame pelo template seq_story). Retorna (violacoes, revisar)."""
    viol, rev = [], []
    for sid, theme, _v, frames in NOVAS:
        for i, (seg, title, sub, cue) in enumerate(frames, 1):
            texto = f"{theme} · {seg} · {title} · {sub} · {cue} · {SIG}"
            for sev, regra, det in auditar(texto, contexto="publico"):
                item = (sid, i, sev, regra, det)
                (viol if sev == "VIOLACAO" else rev).append(item)
    if verbose:
        for it in viol + rev:
            print(" ", it)
        print(f"AUDITORIA CFM: {len(viol)} VIOLACAO | {len(rev)} REVISAR "
              f"em {sum(len(f) for _, _, _, f in NOVAS)} frames de {len(NOVAS)} sequencias")
    return viol, rev


def run():
    path = os.path.join(ROOT, "sequences.json")
    seqs = json.load(open(path, encoding="utf-8"))
    existentes = {s["id"] for s in seqs}
    img_existentes = {os.path.basename(p) for s in seqs for p in s["images"]}

    # trava de conformidade: nada renderiza/anexa com violacao CFM
    viol, _rev = auditar_novas()
    if viol:
        raise SystemExit(f"ABORTADO: {len(viol)} violacao(oes) CFM — corrija os textos.")

    novos = []
    for sid, theme, v, frames in NOVAS:
        if sid in existentes:
            print("pula (ja existe):", sid)
            continue
        n = len(frames)
        assert n == 5, f"{sid}: precisa de 5 frames, tem {n}"
        imgs = []
        for i, (seg, title, sub, cue) in enumerate(frames, 1):
            fn = f"{sid}_{i}.jpg"
            assert fn not in img_existentes, f"colisao de imagem: {fn}"
            seq_story(fn, v, theme, i, n, seg, title, sub, cue)
            imgs.append("images/" + fn)
        novos.append({"id": sid, "theme": theme, "label": frames[0][0], "images": imgs})
        print("ok", sid, flush=True)

    seqs.extend(novos)
    json.dump(seqs, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"ANEXADAS: {len(novos)} sequencias | TOTAL agora: {len(seqs)}")


if __name__ == "__main__":
    if "--audit" in sys.argv:
        viol, _ = auditar_novas()
        sys.exit(1 if viol else 0)
    run()
