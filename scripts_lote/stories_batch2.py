# -*- coding: utf-8 -*-
"""Lote 2 de stories (story61-90) — reforço da cadência diária. python stories_batch2.py"""
import os, json
from gerar_conteudo import story, ROOT

# (id, variant, kicker, title, sub)
STORIES=[
 ("story61","dark","Lesão aguda","Gelo ou calor?","Nas primeiras 48h, gelo para inchaço e dor. Calor ajuda mais em tensão muscular crônica."),
 ("story62","light","Torceu o pé","O que NÃO fazer","Evite forçar, massagear forte ou aplicar calor nas primeiras horas. Proteja, gelo e eleve."),
 ("story63","dark","Mito","Crescer dói?","A \"dor de crescimento\" existe e é benigna, mas o crescimento em si não machuca. Dor que limita, avalie."),
 ("story64","light","Adolescente","Estalo no joelho ao agachar","Sem dor ou inchaço, costuma não preocupar. Com dor ou falseio, vale avaliar."),
 ("story65","dark","Atenção","Criança que cai demais","Quedas frequentes, tropeços e cansaço acima do normal merecem uma avaliação."),
 ("story66","light","Sinal","Dor no pé ao acordar","Pode ser do crescimento. Se persiste, é de um lado só ou faz mancar, avalie."),
 ("story67","dark","Dúvida comum","Cãibra à noite na criança","Comum e costuma ser benigna. Hidratação e alongamento ajudam; se atrapalha o sono sempre, avalie."),
 ("story68","light","Tratamento","Imobilização tem tempo certo","Tempo de mais ou de menos atrapalha. Siga o combinado e compareça aos retornos."),
 ("story69","dark","Esporte","Voltar a jogar: critérios","Não é só \"sumiu a dor\". Força, amplitude e confiança contam para evitar nova lesão."),
 ("story70","light","Mito","Alongar antes previne lesão?","Sozinho, pouco. O que protege é aquecer, fortalecer e respeitar o descanso."),
 ("story71","dark","Consolidação","O que atrapalha o osso colar","Cigarro, alguns remédios e instabilidade dificultam. Por isso o acompanhamento importa."),
 ("story72","light","Saúde óssea","Nutrição e osso na infância","Cálcio e vitamina D sustentam o crescimento ósseo. A necessidade de suplemento é individual."),
 ("story73","dark","Adolescente","Pescoço de texto","Horas no celular pesam na postura. Pausas e tela na altura dos olhos ajudam."),
 ("story74","light","Cuidado","Bota/imobilizador removível","Tirar só quando autorizado, observar a pele e seguir as orientações de apoio."),
 ("story75","dark","Bom senso","Raio-X nem sempre é preciso","O exame clínico vem primeiro. Imagem entra quando muda a conduta."),
 ("story76","light","Por que retornar","Deformidade que cresce","No crescimento, o que está leve hoje pode mudar. Acompanhar de perto evita surpresas."),
 ("story77","dark","Atenção","Joelho inchado após o jogo","Inchaço que volta sempre, com dor ou travamento, merece avaliação."),
 ("story78","light","Marcha","Pé que vira ao correr","Às vezes é só rotação do desenvolvimento. Se causa quedas ou dor, avalie."),
 ("story79","dark","Observar","Diferença de força entre os lados","Um lado nitidamente mais fraco ou \"diferente\" merece um olhar mais atento."),
 ("story80","light","Pós-operatório","Fisioterapia é parte do tratamento","A recuperação depende tanto da cirurgia quanto da reabilitação bem feita."),
 ("story81","dark","Sinal de alerta","\"Foi só uma torção\"?","Não apoiar o pé, inchaço grande ou dor que não cede podem ser mais que entorse."),
 ("story82","light","Investigar","Dor que acorda à noite","Dor que tira do sono, com febre ou perda de peso, deve ser avaliada."),
 ("story83","dark","Marcha","Andar na ponta dos pés","Comum nos primeiros anos. Se persiste ou é só de um lado, vale avaliar."),
 ("story84","light","Bebê","Quadril que estala","Nem todo estalo preocupa. Com assimetria ou dificuldade de abrir a perna, avalie."),
 ("story85","dark","Crescimento","Compare os dois lados","Assimetrias que aumentam — pernas, ombros, força — merecem avaliação."),
 ("story86","light","Antes de operar","Vale uma segunda opinião","Em casos complexos, um segundo olhar tranquiliza e às vezes abre opções."),
 ("story87","dark","De longe","Telemedicina orienta","Para quem é de fora de SP, dá para orientar e organizar o caminho à distância."),
 ("story88","light","Alongamento","Como é o acompanhamento","Tratamento de etapas: espera, afastamento gradual e consolidação, de perto."),
 ("story89","dark","Reconstrução","Por que é por etapas","Cada fase tem seu tempo e cuidado — segurança e função vêm primeiro."),
 ("story90","light","Acolhimento","Plano realista vale ouro","Sem promessas: avaliação cuidadosa, plano honesto e acompanhamento próximo. Agende pelo WhatsApp."),
]

def run():
    stories=json.load(open(os.path.join(ROOT,"stories.json"),encoding="utf-8"))
    sids={s["id"] for s in stories}; made=0
    for sid,v,k,t,sub in STORIES:
        if sid in sids: continue
        fn=sid+".jpg"; story(fn,v,k,t,sub); stories.append({"id":sid,"image":"images/"+fn}); sids.add(sid); made+=1
        json.dump(stories,open(os.path.join(ROOT,"stories.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
        print("ok",sid,flush=True)
    print("stories total:",len(stories),"| novos:",made)

if __name__=="__main__":
    run()
