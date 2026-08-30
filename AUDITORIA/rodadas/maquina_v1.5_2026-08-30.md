# Auditoria evolutiva — Motor Instagram · MÁQUINA · v1.5 · 30/08/2026

**v1 (02/08) = sem placar separado da máquina (auditoria integral) · v1.5 = 69,0/100 (baseline da régua nova)**
Escala desta rodada: **profunda** (fan-out por dimensão + cético adversarial por dimensão) · Gatilho: `Grande Revisão 29–30/08 entregou a camada nova da máquina (gates, fila intercalada, verbetes, casos); a janela protegida 16/08→15/09 exige auditar a MÁQUINA sem tocar perfil/fila publicável`

> Escopo: código, gates, telemetria, estoque e processo. Desempenho do perfil é objeto da v2
> (16/09). Nenhuma melhoria desta rodada toca perfil ou fila publicável dentro da janela;
> código/CI/registro pode. Fonte: clone FRESCO de produção (`scratchpad/prodclone`, HEAD=48eae74)
> + `gh` somente leitura. Toda evidência citada foi executada nesta rodada.

---

## 1. O que a v1 (02/08) e o plano prometeram — conferido item a item

**Universo: 32 linhas do backlog v1 (20 ações ranqueadas + 12 linhas de anexo) + 9 apostas + 17 decisões. 32 + 9 + 17 conferidos, zero abandono silencioso admitido nesta tabela.**

Placar do backlog v1: **14 ENTREGUE** (4 deles parciais, com a parte faltante anotada) · **18 NÃO FEITO** (5 com adiamento/substituição REGISTRADA em decisão) · **1 RECUSADO** (sticker de CTA, recusa da própria API Meta). `ENTREGUE` abaixo sempre por evidência de EFEITO, nunca de existência.

### 1a. Backlog da v1

| # | item da v1 | estado | evidência de EFEITO / motivo |
|---|---|---|---|
| 1 | Trial Reels desligado por default | ENTREGUE | `publish.yml:48` default false + `gh api .../actions/variables` vazio; `state/published.json` grava `modo_reel='normal'` em 100% dos reels desde 21/08; reach 30–31 vs 0–8 na era trial |
| 2 | Rafael conferir selo de teste no app | NÃO FEITO (morreu obsoleto) | hipótese fechada por via independente (logs de run + medição 25/07 + `docs/06_TRIAL_REELS.md`); registrado aqui que morreu obsoleto, não abandonado |
| 3 | Card-resumo no último slide dos carrosséis | NÃO FEITO no essencial | `grep -c 'Converse comigo'` = 19/18 nos geradores; zero commits em `carrossel.py`/`posts_batch*.py` desde 10/08; só 1 peça one-off (0dae7b5). **O changelog SOBREVENDE** ("gerador alterado") — ver achado A3 |
| 4 | CTA idêntica → pergunta fechada | ENTREGUE (e direção revertida por decisão) | commit 1f1a7f8; comentários 0→2 na era 3; reversão registrada (plano §8 + rubrica v2 item 1); lotes novos usam send/save |
| 5 | Termo com demanda medida nas legendas | ENTREGUE parcial | 1f1a7f8: "discrepância de membro" em 34 legendas; **"anisomelia" (único termo com demanda GSC) em só 2** — resto no pacote SEO do D-day |
| 6 | Marcador de origem no wa.me da bio | NÃO FEITO — adiado com registro | bio = perfil = intocável na janela; execução no D-day 17–18/09 (Aposta 2f, changelog [PLANEJADO]) |
| 7 | perfil.json versionado | ENTREGUE | commits 70682ad+d74cb03; pulso congela biography/website em cada dump (`insights_pulse.py`) — D1 deixou de ser inauditável. Falta: perfil.json no gate |
| 8 | Medição diária de stories | ENTREGUE | `stories.yml` cron; `state/stories_serie.json` com 28 dias contínuos (03→30/08); 72% cegos viraram série |
| 9 | 4 defeitos de medição do pulso | ENTREGUE 3/4 | commit 9f02f5c; dump 15/08 com reach_unico_janela/followers_count/watch_ms; falta (d): erros genéricos + `except: pass` no breakdown + exit 0 com erros |
| 10 | Ramo trial/fallback gravado no state | ENTREGUE | `publish.py:286-324`; produção grava `modo_reel` em todos os reels 21–30/08 |
| 11 | Gate CFM em todas as rotas + severidades | ENTREGUE com 2 lacunas | `_cfm_guard` nas 4 rotas (e0d02cf+f23b683+D17); `checar_cfm` → 0 VIOLAÇÃO no acervo; lacunas: texto de frames de sequência não auditado no lint; "0 auditáveis" silencioso |
| 12 | "Médico" na identificação | ENTREGUE com regressão | a8956a8: rodapé queimado em todo frame; REGRESSÃO: legendas dos lotes novos sem "Médico" porque `cfm_guardrails.py:146` checa só crm+rqe |
| 13 | Snapshot views/reach 24h/72h | NÃO FEITO — substituído com registro | substituto: dumps por era + tarefa agendada de dumps + regra "peças <4 dias fora de médias" (rubrica v2 item 3); decaimento em idade fixa segue NÃO medível — declarar na v2 |
| 14 | Bomba do prepend de narrativos | ENTREGUE | f23b683: `reels=reels+novos` (APPEND) com comentário citando o achado; workflow segue dispatch-only |
| 15 | Corrida de leitura do state (duplicata de 15/07) | NÃO FEITO | `grep 'git fetch/origin/main/media?limit'` em publish.py = vazio; dedup segue por checkout congelado; duplicata de sequência seria invisível |
| 16 | Apagar duplicata 18109531369972268 + runbook | NÃO FEITO — agendado D10 (16/09) | decisão registrada (plano §4); runbook segue sem o parágrafo; rubrica v2 já exclui a duplicata das médias |
| 17 | Pipeline de voz morto desligado | ENTREGUE (28 dias após a v1) | `gh api workflows`: voz-train/voz-watch `disabled_manually`; ZERO runs após 29/08 22:31Z; falta higiene: `voz/` + `voz_train.py` seguem no repo |
| 18 | Lockup e "pela WhatsApp" | NÃO FEITO (metade) | "pela WhatsApp" zerado nos posts mas vivo em reel16/reel17; lockup "Ortopedia · São Paulo" segue em 3 geradores — sem o nicho |
| 19 | Decisão sobre dest04 | NÃO FEITO — absorvido no D-day | zero registro (grep dest04 = 0); D8 prevê destaques novos 17–18/09; incluir explicitamente no roteiro do D-day senão a peça sobrevive por omissão |
| 20 | Escalonar filas + destino dos 88 stories | NÃO FEITO no núcleo | posts e sequências seguem esgotando na mesma semana (~04–08/11); stories.json segue inflando runway; zero telemetria de estoque — **reincidente** |
| A-CI | Teste/gate em CI na main | NÃO FEITO | grep nos workflows = só checar_voz; gate-cfm.yml AUSENTE da main (registro fantasma "active" aponta p/ branch) |
| A-timeout | timeout-minutes no publish.yml | NÃO FEITO | grep = 0; job travado congela a fila por até 6h |
| A-token | Renovação + monitor do PAT | ENTREGUE parcial | renovação: 4 segundas verdes consecutivas, expira 23/10 (efeito provado); monitor do PAT (`pat_expira_em`): NÃO FEITO |
| A-auditor | `_auditoria_motor.py` cego + frases falsas | NÃO FEITO | `except: return None` + `or []` seguem; frases falsas do prefixo `_` seguem |
| A-dur | Campo dur errado + lint | NÃO FEITO | dur=20.0 (real 59,2s) segue; mitigado: rubrica v2 usa watch absoluto; itens novos gravam dur real |
| A-Art11 | Padrões de capacidade privilegiada (Art. 11 IX) | NÃO FEITO | grep 'IX\|privilegiad\|outros n' = 0; D17 é ganho real mas tema DIFERENTE |
| A-LGPD | Aviso de privacidade/canal seguro | NÃO FEITO | fora do pacote D1–D16; atenuante: CTA migrou p/ send/save; vira pergunta fechada pós-v2 |
| A-CFM2454 | Selo/disclosure de voz IA | ENTREGUE por via melhor | D6: "Narração com voz digital (IA)." já nas legendas da fila (verificado em reels.json); bio no D-day; selo opt-in: aguardar (registrado) |
| A-miúda | 6 itens de medição miúda | NÃO FEITO ×6 | quando/UTC, kind post01, órfãs, reach<5, DISC no feed, hashtags — greps = 0 |
| A-nicho | Conteúdo do nicho fora da fila | ENTREGUE e superado | fe3e8ad+5ca3e3e: 23 narrados aprovados na frente de reel04, com hash + PROGRAMACAO + quebra da janela ANOTADA |
| A-Dday | Pinos, capas, corpo post18-24, horário; sticker | NÃO FEITO (parte registrada / 4 órfãos) · sticker RECUSADO | registrados p/ D-day: pinos, capas, CTA textual; RECUSADO: sticker via API ("not supported", plano §8); **4 órfãos sem estado** (corpo post18-24, agendamento em captions antigas, variação slides, horário de sequência) — ganham estado nesta ata: adiados pós-janela, dono assistente |
| A-render | Retry verde-mentiroso nos renders + Piper morto | NÃO FEITO | loop de push sem ok/exit 1 em render-reel-voz.yml; `\|\| echo FALHOU` nos 3 lotes; Piper aponta p/ .onnx inexistente — Aposta 4b prometeu "AGORA" |

### 1b. Apostas 1–9 e decisões D1–D17

| aposta/decisão | estado | evidência de EFEITO / motivo |
|---|---|---|
| A1 — fila não regride | ENTREGUE | 26 narrados nas posições 51–76 de reels.json na frente de reel04; decisão registrada no changelog ANTES do prazo 02/09 |
| A2 — telemetria | ON TRACK com 2 furos | sinais_por_peca.csv (95 linhas) reexecutável; dumps agendados de verdade (cron `0 21 5,12,15 9`); furos: SKILL.md da v2 sem `fechar_rubrica.py` nem séries de fadiga |
| A3 — gate de aprovação | FERRAMENTA PROVADA, ENFORCEMENT ZERO | selftest persistido (7/7, 5 reprovações vistas); reprova a fila real (exit 1, 44 legados); **nenhum workflow/CI o executa** — ver achado A2 |
| A4a/D7 — Kaggle desligado | ENTREGUE | `disabled_manually`, zero runs pós 29/08; arquivamento de `voz/` pendente (higiene) |
| A4b — fail-loud dos renders | PROMETIDO E NÃO ENTREGUE | retry verde vive em 3 workflows de lote; nenhum tem checar_voz; Piper morto segue — ver achado A1 |
| A5 — fábrica de verbetes | ENTREGUE adiantada | 20 verbetes renderizados, 2 runs verdes, commits do bot só em verbetes/ (posts.json intocado); gate próprio reprova semeados |
| A6 — Anatomia de um Caso | ENTREGUE | 3 pilotos aprovados/hasheados, enfileirados 23/09–07/10 (pós-janela); banco_casos = 29, 0 refutados |
| A7 — D-day vitrine | nada devido antes de 16/09 | pacote [PLANEJADO] completo no changelog; máquina deve preparar o canário como script antes de 17/09 |
| A8 — loop de comunidade | POS_16_09, sem atraso hoje | template de CTA de reply ainda não existe — construir com render de prova ANTES de 16/09 |
| A9 — YouTube (D11) | ENTREGUE (deste chat) | série 3 LIBERADA 30/08; nota: padrão de UTM não formalizado no plano — dívida da frente YouTube |
| D1,D2(adulto),D3,D4,D6(legendas),D7,D12,D13,D17 | EXECUTADAS com efeito | commits fe3e8ad/5ca3e3e/ef150ab/d661640/33fdb5b + `checar_cfm` exit 0 com régua endurecida |
| D5, D8, D9, D10, D14, D15, ratificação do legado, lotes kids/pós-op | DEPENDEM DO RAFAEL | não é dívida da máquina; pacote de sessões de 15 min já montado (APROVACOES.md §§2–3); sem decisão até 15/09 → registrar escolha por omissão |
| D16 | por design na v2.1 (28/10) | — |

---

## 2. Checklist binário (não pontua — existe ou não existe)

| guarda | estado |
|---|---|
| Gate CFM nas 4 rotas do publish (`_cfm_guard`) | SIM (provado por semeadura em texto de cena) |
| D17 (estético/estatura = VIOLAÇÃO) vivo no caminho de publicação | SIM |
| Fail-loud do publish provado por suíte que cobra EXIT | SIM (`teste_publish_exit.py` exit 0) |
| voz-train/voz-watch desligados na fonte (GitHub API) | SIM (`disabled_manually`) |
| Dumps da janela agendados e armados | SIM (cron confere com a tabela do changelog) |
| Selftest do gate de aprovação persistido e visto REPROVAR | SIM (5 positivos exit 1 + 2 negativos exit 0) |
| checar_aprovacoes plugado em algum caminho mecânico | **NÃO** |
| Guarda-freio de voz em TODOS os workflows que sintetizam voz | **NÃO (1 de 4)** |
| CI de teste/CFM na main | **NÃO** (gate-cfm.yml = registro fantasma da branch) |
| timeout-minutes no publish.yml | **NÃO** |
| Telemetria de estoque (runway + warning <30d) | **NÃO** (reincidente da v1) |
| Push com ok-flag/exit 1 em TODOS os workflows que commitam | **NÃO** (publish.yml e render-verbetes SIM; render-reel-voz e stories NÃO) |
| Decisão do Rafael sobre exposição do repo público | PENDENTE (fila do Rafael) |

---

## 3. Placar da MÁQUINA

**Peso mede DANO ao usuário final (Rafael, pacientes, conta) — não esforço.** Cada dimensão declara como foi medida (comando reexecutável no clone fresco). Divisão P/R declarada por dimensão; a coluna que soma está em PONTOS.

| # | dimensão (dano dominante se falhar) | peso | divisão P+R | proc | res | pts v1.5 |
|---|---|---|---|---|---|---|
| 1 | Conformidade clínica e guardrails — sanção CFM, dano a paciente | 26 | 14+12 | 10,5 | 10,5 | 21,0 |
| 2 | Confiabilidade do caminho de publicação — duplicata/peça errada no ar | 22 | 12+10 | 8,0 | 8,5 | 16,5 |
| 3 | Governança de aprovação e voz — publicar sem aval clínico; voz alterada | 20 | 11+9 | 5,5 | 6,0 | 11,5 |
| 4 | Telemetria e registro da janela — v2 cega, decisão sem dado | 14 | 8+6 | 5,0 | 4,0 | 9,0 |
| 5 | Estoque e pipelines — perfil seca ou publica legado mudo | 10 | 5+5 | 3,0 | 3,5 | 6,5 |
| 6 | Segurança e higiene do repo público — exposição de governança clínica | 8 | 4+4 | 2,5 | 2,0 | 4,5 |
| | **total** | **100** | | 34,5 | 34,5 | **69,0** |

**Par (Processo, Resultado): Processo 34,5/54 · Resultado 34,5/46** (denominadores = soma das divisões P e R; normalizado: processo 63,9 · resultado 75,0)

**Delta separado:** o alvo não tem série anterior nesta régua (v1 foi integral, sem placar da máquina) → **todo o 69,0 é baseline; a régua ficou mais honesta, o alvo ainda não mediu delta**. A v2.1 (28/10) mede o delta do alvo contra este baseline.

Como cada dimensão foi medida (fonte da verdade, reexecutável):

1. **Conformidade** — `python checar_cfm.py` (0 VIOLAÇÃO/30 REVISAR em 139+120+89 itens); semeadura positiva via `publish._cfm_guard({'scenes':[...]})` → RuntimeError BLOQUEADO; controles positivos e negativos em `cfm_guardrails.auditar`; re-varredura dos 20 verbetes pós-D17 (0/0, com controle positivo disparando no mesmo ambiente). Desconto: gate-cfm ausente da main, lint cego a sequences (150 itens, 0 auditados, exit 0), `nunca ` genérico absolve, D17 evadível por interpolação numérica, Art. 11 IX ausente, `_cfm_guard` fail-open se o import falhar (stderr de job verde).
2. **Confiabilidade** — `python teste_publish_exit.py` exit 0 cobrando EXIT codes; 70 reels pendentes com 0 vídeos ausentes contra `git ls-tree -r HEAD` (clone é sparse — filesystem daria 70 falsos ausentes); 0/176 pendentes bloqueariam no `_cfm_guard`; 0 colisões de id; FIFO simulado = PROGRAMACAO 27/27; produção de 30/08 = exatamente o projetado (10/10 runs verdes). Desconto: corrida de leitura do state aberta (já produziu duplicata pública), sem timeout-minutes, render-reel-voz/stories engolem falha de push, retry verde nos 3 lotes.
3. **Governança** — sha da prova do selftest == script (blob LF); `--auto-teste` re-rodado 7/7; 26 hashes conferem com as fontes (0 divergências); run real #106 com o step do guarda verde. Desconto pesado: ZERO enforcement (grep workflows+publish.py = 0), 27/44 legados sem fonte importável (ratificação impossível hoje), guarda de voz em 1/4 workflows, dispatch dribla o fingerprint, **o registro humano da voz contradiz o estado fingerprintado** (evidência diz pitch -4Hz; o arquivo abençoado tem +0Hz), gate autentica conteúdo e não aprovação (remover `aprovado_por` não muda a saída), CRLF auto-invalida a prova em clone Windows.
4. **Telemetria** — `python telemetria_sinais.py` verde reproduzindo o slope -0,31/sem do plano; dumps agendados com cron correto e auto-delete necessário; stories 28 dias contínuos. Desconto: D17 e verbetes FORA do changelog (regra 1 do próprio changelog furada), ferramenta da v2 irreproduzível fora desta sessão (BASE=scratchpad; monta_master/analise só no scratchpad), `git log --since` derruba 21 commits em silêncio, race do `gh run list` pode salvar dump velho como evidência de hoje, validação do dump não exige followers_count e `insights_pulse` sai 0 com erros.
5. **Estoque** — runway simulado por FIFO (reels 30/12, posts 08/11, seqs 04/11); 100% da mídia pendente trackeada; verbetes 20/20 íntegros e limpos pós-D17 com controle positivo; banco_casos 29/29 coerente; reel-casos pós-janela nas datas exatas. Desconto: penhasco 18/10 (27 mudos legados na frente de 16 narrados, 6 no ar antes da v2.1), D-day dos verbetes sem gatilho nem vigia, telemetria de estoque inexistente (reincidente), PROGRAMACAO truncada e manual, stories órfãos, lote KIDS fantasma.
6. **Segurança** — greps de segredos/PII nos arquivos novos e working tree = só placeholders; banco_casos juridicamente correto; curl anônimo prova previews baixáveis (HTTP 206). Desconto: governança clínica exposta em repo público (54/60 sem registro de aprovação, com CRM, ao lado do calendário futuro), citações verbatim do chat + username em 6 pontos, ~782 MiB crescendo, histórico nunca varrido por conteúdo, logs de Actions públicos não medidos como superfície.

```bash
python "C:\Users\rafae\Claude Code\_Ferramentas_Comuns\auditoria\fechar_rubrica.py" "C:\Users\rafae\AppData\Local\Temp\claude\C--Users-rafae-Claude-Code\525827ef-fe65-4881-a060-53ff1e22e671\scratchpad\rodada_maquina_v15.md"
```

---

## 4. Achados ranqueados — só CONFIRMADO/AJUSTADO pelo cético (1 REFUTADO descartado)

44 achados propostos nas 6 dimensões · 1 refutado (selftest "envelhece" — o check JÁ existe em `checar_aprovacoes.py:176-186` e foi visto REPROVAR; o auditor leu o JSON e nunca executou o script) · 7 AJUSTADOS (moldura/dano corrigidos) · 8 lacunas do cético promovidas a achados por virem com prova reexecutável.

### P0 — consertos desta rodada (código/CI/registro; nenhum toca perfil/fila na janela)

| id | achado (veredito) | conserto em 1 frase |
|---|---|---|
| A1 | **Voz sem freio e verde-mentiroso nos renders**: 3 workflows de lote ativos sintetizam voz e commitam nos MESMOS `_preview_*.mp4` que 90/120 itens da fila publicam, sem `checar_voz` — e o pitch DEFAULT deles (-4Hz) já difere do fingerprintado (+0Hz); render-reel-voz.yml e stories.yml engolem falha de push (job verde, artefato perdido) (AJUSTADO — dano maior que o descrito) | Step `python checar_voz.py` + coletar falhas e `exit 1` nos 3 lotes; copiar o padrão ok-flag de `render-verbetes.yml:52-62` para `render-reel-voz.yml:54-58` e `stories.yml:45-47`; remover o ramo Piper morto e re-registrar o fingerprint. |
| A2 | **Gate de aprovação sem NENHUM enforcement** — existe, prova-se, e nada o executa (grep workflows+publish.py = 0); agravantes provados: autentica conteúdo e não aprovação (remover `aprovado_por`/`evidencia` não muda a saída) e auto-invalida em clone Windows (CRLF muda o sha da prova) (CONFIRMADO + 2 lacunas provadas) | Workflow `gate-aprovacoes.yml` (on: push em reels.json/aprovacoes.json/episodios_*.py) escopado a id NOVO pós-30/08 (legado isento até ratificação); exigir `aprovado_por`+`evidencia` não-vazios em lote aprovado; hash com EOL normalizado (ou `.gitattributes eol=lf`) — cada check novo visto FALHAR uma vez. |
| A3 | **Registro da janela infiel** — "artefato errado vira evidência": D17 (mudança no guardrail central DENTRO da janela) e a fábrica de verbetes fora do changelog; entrada 16/08 afirma "gerador alterado" que o git desmente; rodapés "AGUARDA AVAL" vencidos em 3 artefatos promovidos; PROGRAMACAO anuncia "~18h" quando o motor publica ~15h BRT — janela de revisão passiva 3h menor que a prometida (CONFIRMADO ×5) | Entradas D17/verbetes/ação-14 no `AUDITORIA/CHANGELOG_JANELA_V2.md` + corrigir a entrada de 16/08 + apagar rodapé l.81 (sincronizando a cópia da oficina); rebaixar a minuta do APROVACOES.md e o header de `checar_aprovacoes.py:4-6` a histórico; `PROGRAMACAO.md:8` "~18h"→"~15h (BRT)". |
| A4 | **Ferramenta de medição da v2 irreproduzível**: `telemetria_sinais.py` com BASE no scratchpad DESTA sessão; `monta_master.py`/`analise_series_temas.py`/`resultado_series_temas.json` sem cópia durável; `git log --since` sem hora derruba 21 commits em silêncio; dump agendado pode salvar run VELHO como evidência de hoje e passa verde sem followers_count (CONFIRMADO/AJUSTADO + lacunas provadas) | Copiar os 3 arquivos p/ `_GRANDE_REVISAO_2026-08/` com `BASE=os.path.dirname(__file__)`; no SKILL.md da v2: `fechar_rubrica.py`, séries de fadiga, `git log --since-as-filter="2026-08-16 00:00:00 -0300"`, prazo 18/10 do reel04–30, item 9 sem lista fixa; no SKILL.md dos dumps: selecionar run por `createdAt` pós-dispatch, validar `janela` = hoje, exigir `followers_count`. |
| A5 | **Zero checador no caminho VIVO que publica**: publish.yml (único cron que publica) roda pip→publish→estado; a única barreira é o `_cfm_guard` in-process, que é fail-open com aviso em stderr se o import falhar — e stderr de job verde ninguém lê (lacuna do cético, provada por leitura integral do yml) | Step advisory `python checar_cfm.py` no publish.yml antes de `publish.py` + `timeout-minutes: 15` no job + CI `ci-testes.yml` (push/PR) rodando `teste_publish_exit.py` e `test_publicacao.py` — visto FALHAR uma vez antes de valer. |

### P1 — abertos com dono e prazo (não cabem nesta rodada ou exigem decisão)

| id | achado (veredito) | conserto em 1 frase | dono/prazo |
|---|---|---|---|
| B1 | Governança clínica exposta em repo público: APROVACOES.md declara 54/60 sem registro de aprovação, com CRM/RQE, ao lado do calendário futuro e previews baixáveis (HTTP 206 anônimo); virar privado sem conferir billing pode PARAR a publicação (AJUSTADO) | Default recomendado: mover APROVACOES.md + AUDITORIA/ + PROGRAMACAO.md p/ espelho privado; repo privado inteiro só após conferir quota de Actions; registrar a decisão em qualquer hipótese | Rafael · pauta da v2 (16/09) |
| B2 | Corrida de leitura do state segue aberta (produziu duplicata pública em 15/07; duplicata de sequência seria invisível) (CONFIRMADO, reincidente) | `git fetch origin main` + conferir `origin/main:state/published.json` (ou GET `/media?limit=5`) antes de cada publish_*, com teste semeado visto FALHAR | assistente · antes do D-day |
| B3 | Penhasco 18/10: 27 reels MUDOS `pendente_ratificacao` entram na frente de 16 narrados novos; 6 vão ao ar antes da v2.1; ratificação IMPOSSÍVEL hoje para os 27 sem fonte importável (hash nulo reprova) (AJUSTADO ×2) | Pauta explícita da v2: decidir reel04–30 antes de 18/10 + definir mecanismo de exceção assinada p/ lote sem fonte ANTES de levar ao Rafael; NÃO acoplar o gate como bloqueio do publish | Rafael (decisão) + assistente (mecanismo) · 16/09 |
| B4 | D-day dos verbetes (17–18/09) sem gatilho nem vigia: 0 menções em 40 tarefas agendadas, 0 lote de aprovação — "gatilho sem vigia não dispara" (CONFIRMADO) | Passo no adendo da v2 (ou tarefa 17/09): cunhar lote VERBETES-2026-09 + enfileirar 2/sem + regenerar PROGRAMACAO; idem estado p/ o lote KIDS fantasma (11 roteiros pendentes sem dono) | assistente · antes de 16/09 |
| B5 | CI de conformidade CFM nunca chegou à main — workflow "active" fantasma aponta p/ branch não mesclada; violação nova só é pega às 15h do dia de publicar (CONFIRMADO) | Cherry-pick da cadeia b8932df..1f0781a p/ main (ou matar a branch e o registro); parte já coberta pelo step advisory de A5 | assistente · com A5 |
| B6 | Registro humano da voz contradiz o estado fingerprintado: evidência diz "rate -8%, pitch -4Hz aceitos pelo Rafael"; o arquivo abençoado pelo hash tem +0Hz — não há como saber, só pelo repo, qual voz ele aceitou (lacuna do cético, provada) | Apurar o pitch dos mp4 publicados recentes, corrigir evidência OU default, e re-registrar via `checar_voz.py --registrar` citando o piloto | assistente · com A1 |
| B7 | Telemetria de estoque inexistente — P1 da v1 REINCIDENTE intacto; sequências zeram 04/11 sem alarme e sem pipeline de reposição (commit mais recente em sequences.json: 03/07) (CONFIRMADO) | Implementar a ação já escrita na v1: `::warning::` <30 dias + `::error::` ao zerar em publish.py + runway por tipo no pulso; tirar stories.json do RUNWAY do `_auditoria_motor.py:16` | assistente · pós-A1–A5 |

### P2

| id | achado (veredito) | conserto em 1 frase |
|---|---|---|
| C1 | RUNBOOK §2 ensina a enfileirar SEM o gate e SEM regenerar PROGRAMACAO — os dois processos criados em 30/08 falham no primeiro uso por terceiro (AJUSTADO: doc já; CI só pós-ratificação ou escopado) | Passos 2b (lote+hash+checar até exit 0) e 4 (regenerar PROGRAMACAO) no `docs/02_RUNBOOK.md` §2. |
| C2 | PROTOCOLO_Deploy_e_Guardrails_IG.md descreve severidades FALSAS no guardrail central (estética/assinatura como REVISAR; são VIOLAÇÃO) e ignora módulos/gates de 30/08 (CONFIRMADO) | Atualizar §§2/4/6 + TL;DR + entrada no LOG citando 33fdb5b; pôr ponteiro do protocolo dentro do repo. |
| C3 | `nunca `/`jamais` genéricos na lista NEGACAO absolvem violação real ("Nunca foi tão fácil fazer alongamento estético…" → zero issue) (CONFIRMADO) | Ancorar as formas (`nunca por estetic`, `jamais promet`) em `cfm_guardrails.py:56,68` + semear o caso no smoke. |
| C4 | D17 evadível por interpolação numérica ("ganhar 8 cm de estatura" passa limpo) e por sinônimo ("crescer alguns centímetros") (CONFIRMADO ×2) | Co-ocorrência com janela regex `(ganhar|aumentar)\W+(\w+\W+){0,4}estatura` + colocações de centímetros em ESTETICA_TERMOS e `_ANGULO_VETADO`, com controle positivo novo visto REPROVAR. |
| C5 | checar_cfm audita só `caption`: sequences.json com 150 itens, 0 auditados, exit 0 — a lição dos ~13% virou guarda no publish e não no lint irmão (CONFIRMADO) | Reutilizar `_texto_auditavel` no loop de `checar_cfm.py:~193` e tratar "itens>0, 0 auditados" como aviso ruidoso. |
| C6 | "Médico" ausente das legendas novas porque `cfm_guardrails.py:146` checa só crm+rqe — a desalinha código×docstring que a v1 mandou fechar (CONFIRMADO, regressão) | Incluir 'medico' na condição da assinatura (medir bloqueio retroativo com checar_cfm antes); texto das legendas só pós-15/09. |
| C7 | Citações verbatim do chat privado + nome de sessão interna + caminho local com username em repo público (6 pontos + APROVACOES.md:55) (CONFIRMADO) | Neutralizar para "chat de 30/08 com o Rafael" e referência sem caminho local; seguro p/ o gate (hash não cobre esses campos) — rodar checar_aprovacoes depois como prova. |
| C8 | Repo ~782 MiB, cruza 1 GiB em ~2,7 meses no ritmo de agosto (média ~3 MB/dia com picos de render de 47 MB) (AJUSTADO: taxa corrigida na fonte) | Previews como Release assets/artifacts ou branch órfã truncável; validar com o Rafael os links novos antes de cortar os raw. |
| C9 | `pat_expira_em` inexistente — quando o PAT expirar, a renovação de token morre com aviso fraco (CONFIRMADO) | Gravar `pat_expira_em` em `state/token_refresh.json` e checar os DOIS prazos em `_avisar_validade_do_token`. |
| C10 | Art. 11 IX/XIII sem regra (família "o que outros não resolveram" — a vedação que mais morde no nicho, e pega o dest04) (CONFIRMADO) | Família nova com severidade REVISAR em cfm_guardrails.py, com controle negativo. |
| C11 | `insights_pulse.py` sai exit 0 com `erros` não-vazio + parse do breakdown em `except: pass` — dump parcial passa verde e a série perde o ponto em silêncio (CONFIRMADO) | Nomear a métrica no append de erros e `sys.exit(1)` quando `erros != []` (registrar no changelog: muda comportamento de workflow na janela). |
| C12 | PROGRAMACAO.md manual e truncada (26/70 reels, 11/40 posts) — o trecho pendente de ratificação nunca aparece na janela de aval passiva (CONFIRMADO) | `gerar_programacao.py` (a projeção FIFO já validada por comando) cobrindo a fila inteira com coluna de status de aprovação. |

### P3

| id | achado | conserto em 1 frase |
|---|---|---|
| D1 | stories.json: 88 órfãos desde 07/06 inflando o RUNWAY | decisão do Rafael sobre destino; mínimo: tirar do dict em `_auditoria_motor.py:16`. |
| D2 | dur errado na biblioteca velha, sem lint | backfill via mvhd + lint `|dur_decl−dur_real|>2s` no gate. |
| D3 | Docstrings STALE: gerar_verbetes.py:39-42/:486-489 ("o auditar NÃO cobre") desmentidas pelo D17; `_auditoria_motor.py:88` e `gerar_reel_voz.py:8` com frases falsas | atualizar as notas; trocar a métrica por "mp4 não referenciados por reels.json". |
| D4 | Lock `motor-instagram` instruído mas inexistente em recursos.json — dois nomes p/ a mesma seção crítica | registrar o recurso OU trocar a instrução da PROGRAMACAO.md:5 p/ `deploy-instagram`. |
| D5 | Evidências de ratificação apontam p/ minutas que só existem na oficina OneDrive (inauditáveis do repo) | copiar p/ AUDITORIA/ ou reescrever a referência com caminho completo + aviso. |
| D6 | voz-train/voz-watch invisíveis como desligados em clone (YMLs com cron sem nota; inventário diz "treina voz") | comentário-cabeçalho de desativação nos 2 YMLs + corrigir `docs/01_INVENTARIO.md:77-78`. |
| D7 | Dispatch manual com rate/pitch custom não passa pelo fingerprint (ato humano deliberado) | registrar como limitação no docstring; opcional: step falha se inputs ≠ default sem `VOZ_PILOTO=1`. |
| D8 | 4 FALTA termo→popular no gate_publicacao, todos em lotes APROVADOS — conserto colide com o hash (AJUSTADO: 4 de 4, colisão mais ampla) | decisão dupla pós-janela: jargão precisa de popular? + documentar fluxo de re-aprovação de texto em APROVACOES.md. |
| D9 | `voz/`, `voz_train.py`, YMLs mortos seguem no repo (código morto pontua; re-enable religa cron) | commit de limpeza p/ `docs/arquivo_voz/` pós-janela via coord_git.py. |
| D10 | Locks inverificáveis por desenho (coordenar.py sem journal) — universo declarado, não conclusão de ausência | fila do dono da Coordenação: JSONL de lock/unlock/takeover. |
| D11 | Prova de byte-identidade dos reel-casos só no texto do commit | persistir como artefato; gate de morte barata (<150 views) fica p/ v2.1. |
| D12 | Histórico do git nunca varrido por CONTEÚDO (probe só por filename); logs públicos de Actions não medidos como superfície | gitleaks por revisão + entrar no MESMO pacote de decisão B1. |

---

## 5. Melhorias DESTA rodada (regra nº 1: implementar antes de publicar número)

Top 5, todas código/CI/registro — **nenhuma toca perfil nem fila publicável dentro da janela**. Especificação em nível de arquivo; cada check novo tem de ser visto FALHAR uma vez antes de valer; commits SÓ via `coord_git.py` com lock `deploy-instagram`.

**M1 — Freio de voz e fail-loud nos renders (achado A1, dano: voz alterada/artefato perdido em job verde)**
- `render-lote-2026.yml` (~l.36), `render-lote-julho-2026.yml` (~l.35), `render-todos-reels.yml` (~l.28): step `run: python checar_voz.py` após o pip install; no loop de render, coletar falhas e `exit 1` no fim (matar o `|| echo FALHOU`; corrigir a concatenação de echos em render-todos-reels.yml:38); alinhar EDGE_PITCH default com o aprovado.
- `render-reel-voz.yml:54-58` e `stories.yml:45-47`: copiar o padrão ok-flag/`exit 1` de `render-verbetes.yml:52-62`.
- `gerar_reel_voz.py:22,46`: remover o ramo Piper morto (aponta p/ `.onnx` inexistente) e re-registrar o fingerprint via `checar_voz.py --registrar` citando o piloto — resolvendo junto o B6 (apurar se a voz aceita é -4Hz ou +0Hz ANTES de re-registrar).
- Prova: 1 run semeado com falha que fique VERMELHO, id registrado no changelog.

**M2 — Enforcement mínimo do gate de aprovação (achado A2, dano: publicar sem aval clínico)**
- Novo `.github/workflows/gate-aprovacoes.yml`: `on: push` com paths `reels.json`, `aprovacoes.json`, `episodios_*.py`; roda `checar_aprovacoes.py` com flag nova `--escopo pos-2026-08-30` (reprova só id novo sem lote aprovado; LEGADO-PRE-GATE isento até ratificação).
- `checar_aprovacoes.py`: (i) exigir `aprovado_por` e `evidencia` não-vazios quando `status='aprovado'` (controle positivo novo no `--auto-teste`); (ii) `sha256_arquivo()` (l.98) hasheando conteúdo com EOL normalizado a `\n` — mata o falso "PROVA INVÁLIDA" em clone Windows; (iii) trocar o header MINUTA (l.4-6) por status real.
- Prova: workflow visto REPROVAR com id semeado sem lote; visto PASSAR na fila real atual.

**M3 — Registro fiel da janela (achado A3, dano: artefato errado vira evidência na v2)**
- `AUDITORIA/CHANGELOG_JANELA_V2.md` (repo, e sincronizar a cópia da oficina): entrada D17 (33fdb5b, contaminação nula no acervo, efeito prospectivo); entrada da fábrica de verbetes (6910fa1/d5f9900/021b2ab) + 1 linha na entrada do D-day; ação 14 na entrada de 16/08; corrigir "gerador alterado" → "card one-off criado; geradores NÃO alterados"; apagar o rodapé vencido (l.81); citar 5ca3e3e na entrada D1.
- `APROVACOES.md`: rebaixar §§1-6 a "ANEXO HISTÓRICO — minuta de 30/08 (superada)" e reescrever §5.1 apontando p/ os 5 lotes do aprovacoes.json.
- `PROGRAMACAO.md:8`: "~18h" → "~15h (BRT)".

**M4 — Ferramenta da v2 durável e à prova de armadilha (achado A4, dano: v2 abre cega)**
- Copiar `resultado_series_temas.json`, `monta_master.py`, `analise_series_temas.py` do scratchpad p/ `_GRANDE_REVISAO_2026-08/`; trocar BASE por `os.path.dirname(__file__)` em `telemetria_sinais.py:16` e nos 2 copiados; rodar 1 vez do caminho novo (prova).
- `C:/Users/rafae/.claude/scheduled-tasks/instagram-auditoria-v2/SKILL.md`: (i) rodar `fechar_rubrica.py` antes de publicar número; (ii) fadiga pelas séries reach-seguidores-30d/likes-por-peça/saldo, nunca o 512→390; (iii) `git log --since-as-filter="2026-08-16 00:00:00 -0300"`; (iv) pauta: decidir reel04–30 antes de 18/10 + re-rodar `--auto-teste` antes de julgar o gate; (v) item 9: auditar aprovacoes.json inteiro, sem lista fixa; (vi) passo D-day dos verbetes (lote VERBETES-2026-09 + 2/sem + regenerar PROGRAMACAO) e estado do lote KIDS.
- `.../instagram-dumps-janela-v2/SKILL.md`: selecionar runs por `gh run list --json databaseId,createdAt` com `createdAt` pós-dispatch; validar que `janela` do JSON termina HOJE; rotular _30d/_90d pelo conteúdo; exigir `conta.followers_count` (e `reach_por_follow_type` no 30d).

**M5 — Checador no caminho vivo + tetos (achado A5, dano: fila congelada 6h / violação só descoberta às 15h)**
- `publish.yml`: `timeout-minutes: 15` no job; step advisory `python checar_cfm.py` antes de `python publish.py`.
- Novo `.github/workflows/ci-testes.yml` (push/PR): `teste_publish_exit.py` + `test_publicacao.py` (offline, segundos).
- Prova: cada um visto FALHAR uma vez (semear violação em branch de teste / exit forçado) antes de valer.

**Critério de parada honrado:** B1 (exposição), B3 (ratificação), D8 (jargões) e o destino dos stories exigem o Rafael — foram para a fila dele, não para "backlog genérico".

---

## 6. Fila do Rafael (só ele pode fazer)

| o que | por que só ele | bloqueia o quê |
|---|---|---|
| Decidir exposição do repo público (privado × espelho × aceite consciente) — com aviso da quota de Actions | decisão de governança/custo | B1, C7, C8, D12 |
| Ratificar (ou não) o LEGADO-PRE-GATE + decidir reel04–30 antes de 18/10 | aprovação clínica é dele | B3, penhasco 18/10 |
| Aprovar lote KIDS (11) e cunhar lote VERBETES no D-day | idem | B4, meta ≥30 até 30/09 (está em 26) |
| D5 (conta Azure), D8/D9/D10 no app (16–18/09), D14 (dia da caixinha), D15 (consentimentos) | contas/ações no app dele | Apostas 4d, 7, 8 |
| Jargões do gate_publicacao (4 FALTA termo→popular em lotes aprovados) + fluxo de re-aprovação de texto | pode ser decisão, não defeito | D8 |
| Destino dos 88 stories órfãos | decisão editorial | D1 |

---

## 7. Meta-auditoria

**Que erro a v1/Grande Revisão cometeu que esta rodada pegou:**
1. **Registro que sobrevende** — o changelog afirmou "gerador alterado (card-resumo)" e o git desmente: a ação mais vendida da v1 está substancialmente NÃO FEITA. Artefato errado vira evidência (lição da casa, agora com caso próprio da frente).
2. **"Instalado" tratado como "em vigor"** — a Aposta 3 declarou o gate de aprovação instalado; ele existe, prova-se, e NADA o executa. Existência voltou a passar por efeito exatamente onde o protocolo manda cobrar efeito.
3. **Promessa de fail-loud entregue só no workflow novo** — a Aposta 4b prometeu matar o retry verde "AGORA"; o padrão correto foi escrito no publish.yml *citando como origem* o render-reel-voz.yml, que NÃO o tem — a guarda nasceu no lugar errado e o comentário aponta para o irmão doente como se fosse são.
4. **O fingerprint abençoou um estado que o registro humano desmente** (pitch +0Hz hasheado × "-4Hz aceito pelo Rafael" na evidência) — um humano auditando o registro aprovaria a crença errada.
5. **Adendo da v2 nasceu com lista fixa** que apodreceu no mesmo dia (2 lotes → 3 em 11 horas). Lista em prosa de estado vivo é registro que nasce vencido.

**Alguma nota mudou sem o objeto mudar?** Não se aplica — não há série anterior nesta régua; 69,0 é baseline declarado. O delta "régua mais honesta × alvo melhorou" começa a valer na v2.1.

**O que NÃO foi medido nesta rodada (declarado, não "está bom"):**
- Conteúdo VISUAL dos mp4/jpg (só texto-fonte, byte-trackeamento e byte-identidade); acentuação além de spot-checks.
- Histórico do git por CONTEÚDO (probe só por filename; gitleaks pendente — D12) e logs públicos de Actions como superfície.
- Desempenho do perfil (por desenho — v2 de 16/09) e decaimento em idade fixa (substituto declarado).
- Saturação do agendador nativo (limite global de 3 slots, `ULTIMO_OK.txt`) — as 2 tarefas existem e estão `enabled`, mas o agendador em si não foi sondado; **medir antes de 05/09**, senão os 3 dumps viram não-ocorrência silenciosa.
- Uso de locks nos 12 pushes de hoje — inverificável por desenho (sem journal); universo declarado, sem conclusão de ausência.
- Plano/quota de Actions da conta (bloqueia a opção "repo privado" de B1).

**Conclusões de ausência publicadas — universo medido?**
- "Nenhum segredo" — LIMITADA explicitamente a arquivos novos + working tree (universo declarado; histórico fica em D12).
- "checar_aprovacoes em 0 workflows" / "checar_voz em 1 de 4" — universo = TODOS os `.yml` de `.github/workflows/` (grep no diretório inteiro + `gh api workflows` como segunda fonte).
- "0 vídeos ausentes" — medido contra `git ls-tree -r HEAD` porque o clone é sparse; medir no filesystem daria 70 falsos ausentes (armadilha de instrumento registrada).
- "verbete não citado em tarefa agendada" — universo = as 40 tarefas do diretório, não só as 2 do Instagram.

**O que o humano teve de corrigir?** Nenhuma correção do Rafael nesta rodada (rodada de máquina, sem entrega nova a ele). As regras dele já dadas (piloto de voz 30/08, revisão passiva) foram usadas como régua — e a rodada achou 3 portas que as contornam (A1, B6, D7).

**A guarda vale no projeto irmão?** Três casos de guarda num irmão e não no outro, todos achados desta rodada: fail-loud de push (publish.yml/render-verbetes SIM; render-reel-voz/stories NÃO), `_texto_auditavel` (publish SIM; checar_cfm NÃO), lição da transcrição/minuta (APROVACOES.md diagnosticou a doença da referência externa e o próprio lote LEGADO a comete). M1/C5/D5 fecham os três.

**A suíte foi exercitada ao contrário?** Sim: `checar_aprovacoes --auto-teste` re-rodado com 5 reprovações OBSERVADAS em subprocesso (exit 1); `checar_voz --auto-teste` com 3 positivos detectados; controles positivos novos semeados em cfm_guardrails (disparam), no gate de verbetes (2 erros) e no publish `_cfm_guard` (RuntimeError). O único achado REFUTADO da rodada caiu exatamente por isso: o auditor leu o JSON do selftest e nunca executou o script — o cético executou e o check "faltante" reprovou de verdade.

**Indicadores do processo:** achados propostos ~44 + 8 lacunas do cético promovidas · refutados 1 (2%) · AJUSTADOS 7 · reincidentes da v1: 6 (telemetria de estoque, corrida do state, CI na main, fail-loud dos renders, dur, Art. 11 IX) — **reincidência é o indicador mais feio da rodada** · tempo até implementar na v1: itens executados na própria sessão saíram; o mais lento dos entregues levou 28 dias (ação 17) · a implementar nesta sessão: M1–M5 (a rodada só publica o 69,0 como oficial depois delas).

**Defeito encontrado no próprio protocolo:** nenhum novo; duas confirmações fortes de regras existentes (efeito ≠ existência; gatilho sem vigia). Candidatas a lição transversal da casa (memória): (i) hash de arquivo em repo multi-OS precisa normalizar EOL, senão a prova se auto-invalida no clone Windows; (ii) `git log --since` sem hora explícita preenche com a hora ATUAL e corta o primeiro dia em silêncio — usar `--since-as-filter` com hora E fuso; (iii) gate que autentica CONTEÚDO não autentica APROVAÇÃO — exigir os campos de quem aprovou; (iv) workflow "active" na API pode apontar p/ arquivo que nunca existiu na main — registro fantasma engana painel; (v) fingerprint só vale se o REGISTRO humano do aceite bater com o estado hasheado.

---
*Melhorias M1-M5 implementadas e mergeadas em `32fd4d9` (30/08/2026) ANTES da publicação deste número, conforme a regra nº 1 do protocolo. `fechar_rubrica.py`: ok (1 rubrica, 0 defeitos).*
