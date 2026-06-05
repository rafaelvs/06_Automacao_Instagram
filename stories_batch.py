# -*- coding: utf-8 -*-
"""Lote de stories novos (story40-60). python stories_batch.py"""
import os, json
from gerar_conteudo import story, ROOT

# (id, variant, kicker, title, sub)
STORIES=[
 ("story40","dark","Joelho da criança","Pernas em X ou arqueadas","Costuma ser do crescimento e alinhar sozinho. Muito acentuado ou só de um lado, avalie."),
 ("story41","light","Pé da criança","Pé chato preocupa?","Quase sempre não: o arco se forma com o tempo. Dor ou rigidez merecem avaliação."),
 ("story42","dark","Teste em casa","Sinais de escoliose","Ombros e cintura tortos, e um lado das costas mais alto ao inclinar o tronco à frente."),
 ("story43","light","Adolescente atleta","Dor abaixo do joelho","Osgood-Schlatter é comum no estirão. Ajustar a carga, gelo e alongar costumam ajudar."),
 ("story44","dark","Sinal de alerta","Dor no quadril, mancando","No pré-adolescente, sem trauma claro, vale avaliar sem demora. O joelho às vezes avisa o quadril."),
 ("story45","light","Bebê","Cabeça sempre para um lado","Pode ser torcicolo congênito. Cedo, responde bem a alongamentos orientados."),
 ("story46","dark","Primeiros socorros","\"Cotovelo de babá\"","Após puxar o bracinho, a criança não mexe o braço. Não force e procure avaliação."),
 ("story47","light","Entenda","A placa de crescimento","É por onde o osso da criança cresce. Por isso fraturas infantis têm cuidado próprio."),
 ("story48","dark","Mito","Bebê precisa de sapato firme?","Descalço em casa fortalece o pé. O sapato é proteção: prefira solado flexível."),
 ("story49","light","Desenvolvimento","Quando a criança anda?","A maioria entre 12 e 15 meses. Não andar após 18 meses merece avaliação."),
 ("story50","dark","Emergência","Articulação quente e com febre","Inchaço, dor forte e recusa a mexer o membro: procure atendimento imediato."),
 ("story51","light","Reconstrução","Uma perna mais curta","Pequenas diferenças são comuns. Há opções, da palmilha ao alongamento, conforme o caso."),
 ("story52","dark","Fixador externo","Posso tomar banho?","Em geral sim, seguindo a orientação: manter limpo, secar os pinos e observar a pele."),
 ("story53","light","Reconstrução","Fratura que não cola","A pseudoartrose tem tratamento: investigar a causa, estabilizar e estimular o osso."),
 ("story54","dark","Adulto","Joelho desalinhado","O eixo torto sobrecarrega um lado e pode desgastar antes. Avaliar o alinhamento ajuda."),
 ("story55","light","Marcha","Pés para fora","Costuma ser do desenvolvimento e melhora. Muito assimétrico ou com quedas, avalie."),
 ("story56","dark","Saúde óssea","Vitamina D","Ajuda a usar o cálcio. Sol e dieta contribuem; suplemento é individual, sob avaliação."),
 ("story57","light","Jovem atleta","Dor no calcanhar","Doença de Sever: comum em quem treina. Carga equilibrada, gelo e alongamento ajudam."),
 ("story58","dark","Antes da consulta","O que levar","História do problema, exames que já tem (mesmo antigos) e suas dúvidas anotadas."),
 ("story59","light","Coluna","Dor nas costas na criança","Dor noturna, febre ou que limita merece avaliação. Na maioria é simples, mas vale investigar."),
 ("story60","dark","Acolhimento","Casos difíceis têm caminho","Avaliação cuidadosa, plano realista e acompanhamento de perto. Agende pelo WhatsApp."),
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
