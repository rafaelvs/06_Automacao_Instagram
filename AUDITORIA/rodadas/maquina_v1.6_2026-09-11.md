# Auditoria evolutiva — Motor Instagram · MÁQUINA · v1.6 · 11/09/2026

**v1.5 (30/08) = 69,0 · v1.6 = 60,0 (−9,0)** — decomposto: **alvo piorou −4,0 · régua ficou mais honesta −5,0**
Escala desta rodada: **profunda** (fan-out por 4 dimensões + cético adversarial por dimensão + juiz) · Gatilho: `12 dias de operação AUTÔNOMA desde o merge da v1.5 (único commit humano: nenhum) + 4 runs vermelhos + perda do dump de 05/09, a 5 dias da auditoria v2 e a 6 do D-day`

> Escopo: código, gates, CI, telemetria, estoque e processo. Desempenho do perfil é a v2 (16/09).
> Nenhuma melhoria desta rodada tocou perfil ou fila publicável; código/CI/registro/doc pode.
> Fonte: clone FRESCO de produção (`scratchpad/prodclone`, HEAD=`9f3b78e`) + `gh` somente leitura +
> dumps da Graph API na oficina. Toda evidência citada foi **executada nesta rodada pelo juiz**,
> não herdada dos auditores — onde auditor e cético divergiram, o desempate está marcado.

---

## 1. Passo 1 — o que a v1.5 entregou, conferido por EFEITO

**Universo: 5 melhorias (M1–M5) + 7 itens P1 (B1–B7) + 12 P2 (C1–C12) + 12 P3 (D1–D12) = 36 linhas. 36 conferidas.**

### 1a. As cinco melhorias da v1.5

| M | o que prometia | veredito | evidência de EFEITO (ou da falta dele) |
|---|---|---|---|
| **M1** | Freio de voz em todos os workflows que sintetizam voz + fim do verde-mentiroso nos renders | **INSTALADO SEM EXERCÍCIO** | Código correto e provado: `grep -ln checar_voz .github/workflows/*.yml` devolve **os mesmos 4 arquivos** que `grep -ln "edge-tts\|gerar_reel_voz\|VOZ_ENGINE"` — cobertura 4/4 (era 1/4); `checar_voz.py --auto-teste` = 3 positivos + 1 negativo. **Mas nenhuma linha do M1 rodou em CI**: `render-lote-2026` e `render-lote-julho-2026` últimos runs em **27/07**, `render-todos-reels` em **15/06**, `render-reel-voz` em **30/08 15:09Z — antes do merge (`32fd4d9`, 30/08 21:44Z)**. Guarda instalada, zero exercícios. |
| **M2** | Enforcement do gate de aprovação em CI | **QUEBRADO no efeito** (metade-código ENTREGUE) | `gh run list --workflow gate-aprovacoes.yml --limit 50` → **4 runs, todos de 30/08**. Causa medida: `git log --since-as-filter="2026-08-30 22:00:00 -0300" --pretty=%an \| sort \| uniq -c` → **38 commits, 100% `github-actions[bot]`**; push com `GITHUB_TOKEN` não dispara workflow. O gatilho escolhido é **estruturalmente inalcançável** pelo padrão de commit deste repo. Metade-código viva e provada: `--auto-teste` 11/11 com 8 reprovações observadas, e o gate real sai **exit 0** num clone Windows (a normalização de EOL matou o falso "PROVA INVÁLIDA"). |
| **M3** | Registro fiel da janela | **ENTREGUE e já vencido** | As correções de 30/08 estão lá (`PROGRAMACAO.md` com "~15h (BRT)", entradas D17/verbetes, rodapé vencido removido). Mas `git log -1 -- AUDITORIA/CHANGELOG_JANELA_V2.md` → **`950d2fa`, 30/08 18:38** — nenhuma linha em 12 dias; a entrada da v1.5 ainda dizia "aguarda merge do dono" e pedia "registrar a data do merge aqui", sendo que o merge ocorreu **6 minutos depois** (`32fd4d9`, 18:43:56). M3 consertou artefatos; não instalou mecanismo. |
| **M4** | Ferramenta de telemetria durável | **EFEITO PROVADO (dados congelados)** | `telemetria_sinais.py` roda do caminho durável (`_GRANDE_REVISAO_2026-08/`, `BASE = dirname(__file__)`), exit 0, reproduz `slope −0,313`. Ressalva vinculante: `monta_master.py:26-29` carrega snapshots por NOME FIXO de 29/08 e `master.json` carimba `gerado_em: 2026-08-29` — rodada em 16/09 sem conserto, ela devolve como "medição" o mundo de 30/08 (`n: 95`). |
| **M5** | `timeout-minutes` + checador advisory no caminho vivo + `ci-testes.yml` | **QUEBRADO em 2 de 3** | (a) `timeout-minutes: 15` presente, **nunca acionado** (pior run: 5 min) — instalado sem exercício. (b) O step advisory é um **detector MORTO**: `checar_cfm.py` não tem um único `sys.exit` e o `main()` descarta o retorno, então o script **sempre sai 0** e o `\|\| echo "::warning::"` do `publish.yml:51` é código inalcançável. Provado por controle positivo semeado nesta rodada: legenda com "estético/ganhar estatura/garantido" → **5 VIOLAÇÕES impressas, EXIT=0**. (c) `ci-testes.yml`: **7 runs, todos de 30/08** (mesma causa do M2). |

**Placar das melhorias: 1 EFEITO PROVADO (M4) · 1 ENTREGUE-E-VENCIDO (M3) · 2 INSTALADO SEM EXERCÍCIO (M1, timeout do M5) · 2 QUEBRADO (M2, advisory + CI do M5).**

> **Desempate do juiz (dois auditores erraram aqui):** três das quatro dimensões relataram que o step
> advisory "dispara `::warning::` em 100% dos runs" e que "`checar_cfm` sai != 0 por causa do PIL".
> É falso — o que elas leram foi o **eco do comando** no log (`##[group]Run python checar_cfm.py || echo "::warning::..."`),
> que contém o texto literal do aviso. Medi o exit real duas vezes, com acervo limpo (0) e com
> violação semeada (também 0, antes do patch desta rodada). O M5 não é "advisory ruidoso": é advisory **mudo**.

### 1b. Backlog P1/P2/P3 da v1.5 — 31 itens, 31 conferidos

| item | estado | evidência |
|---|---|---|
| B1 exposição do repo público | **NÃO FEITO — fila do Rafael** | repo segue `"visibility": "public"`; e agora com acoplamento medido: 26 links `raw.githubusercontent` na `PROGRAMACAO.md` respondem **HTTP 206** — virar privado quebra em silêncio a janela de revisão passiva dele |
| B2 corrida de leitura do state | **NÃO FEITO — e DISPAROU** | `grep -n "git fetch\|origin/main\|media?limit" publish.py` → vazio. Produziu duplicata pública em 08/09 (achado P0-2) |
| B3 penhasco 18/10 | **NÃO FEITO — fila do Rafael** | `LEGADO-PRE-GATE` segue `pendente_ratificacao`, **45 episódios, 45/45 com `hash_roteiro: None`**; FIFO recalculada hoje confirma **reel04 em 18/10/2026**, sem deriva |
| B4 D-day dos verbetes com gatilho | **NÃO FEITO** | `grep -i VERBETE aprovacoes.json` → **0**; nenhuma tarefa agendada entre 16/09 e 20/09; 20 verbetes renderizados e 0 enfileirados |
| B5 gate-cfm.yml fantasma | **NÃO FEITO** | `gh workflow list --all` → `Gate CFM (conformidade) active`; `git ls-tree -r HEAD \| grep gate-cfm` → vazio; último run 25/07 |
| B6 pitch da voz × registro humano | **ENTREGUE** | `EDGE_PITCH` default `-4Hz` alinhado ao registro do piloto |
| B7 telemetria de estoque | **NÃO FEITO — 3ª rodada** | `grep -n "::warning::\|runway\|estoque" publish.py` → só os 4 avisos de token |
| C1 RUNBOOK sem o gate | **NÃO FEITO** | `docs/02_RUNBOOK.md:37-53` ensina "adicione ao reels.json → commit"; reproduzi o passo com o exemplo do próprio doc e o gate **reprovou (exit 1)** |
| C2 PROTOCOLO de deploy | **NÃO FEITO** | mtime `6 jul`; ensina severidade INVERTIDA (estética/assinatura como REVISAR; são VIOLAÇÃO desde D17/`33fdb5b`) e publica baseline falso "EXIT=0, FALTA 0" — hoje `gate_publicacao.py` dá **EXIT=1, 4 BLOQUEIOS** |
| C3 `nunca`/`jamais` genéricos | NÃO FEITO | `grep -n "nunca por estetic\|jamais promet" cfm_guardrails.py` → vazio |
| C4 D17 evadível | NÃO FEITO | sem janela de co-ocorrência numérica |
| C5 lint cego a sequences/stories | **NÃO FEITO** | `python checar_cfm.py` → `sequences.json: 0 legendas auditadas` · `stories.json: 0` (150 + 89 itens), exit 0 |
| C6 "Médico" na assinatura | NÃO FEITO | `cfm_guardrails.py:146` segue só `crm`+`rqe` |
| C7 vazamento no repo público | **NÃO FEITO — e PIOROU** | ver P1-9: a própria ata da v1.5 publicou UUID de sessão + `C:\Users\<user>` + caminho `.claude/` |
| C8 peso do repo | **REFUTADO como fluxo** | crescimento real em 12 dias = **5.697 bytes** (3 arquivos de state), não ~3 MB/dia; o problema é estoque (782,7 MiB; 30 s de checkout em ~13 runs/dia) |
| C9 `pat_expira_em` | NÃO FEITO | `grep -rn pat_expira_em *.py` → vazio |
| C10 Art. 11 IX | NÃO FEITO | — |
| C11 dump parcial passa verde | **NÃO FEITO — e mordeu** | os 3 dumps novos de 11/09 saíram com `erros` não-vazio e passaram nas 4 validações do SKILL |
| C12 `gerar_programacao.py` | **NÃO FEITO** | arquivo inexistente; `PROGRAMACAO.md` acaba em **12/10**, seis dias antes do penhasco |
| D1 stories órfãos no RUNWAY | NÃO FEITO | `_auditoria_motor.py:16` segue com `stories.json` (88 órfãos) |
| D2–D12 (11 itens) | NÃO FEITO ×10 · D12 **parcialmente fechado** | varredura do histórico por CONTEÚDO = 0 ocorrências de padrão de segredo (limite declarado: clone `blob:none`, binários e logs de Actions fora) |

**Zero commits humanos em 12 dias.** Todo o backlog P1–P3 da v1.5 está aberto, e o item que a v1.5
adiou com dono e prazo ("B2, assistente, antes do D-day") é exatamente o que publicou conteúdo
duplicado no perfil 9 dias depois.

---

## 2. O que foi IMPLEMENTADO nesta rodada (regra nº 1 — antes do número)

Cinco entregas, todas fora do caminho que publica e fora da fila. Nada foi commitado (ordem da
sessão); o que é código está **provado por execução** e entregue como patch aplicável.

| # | o que mudou | arquivo | teste que prova | reprovava a versão antiga? |
|---|---|---|---|---|
| **M1** | **Classificador de erro da Meta passa a ler o `error_subcode`** — a família `2207xxx` chega no subcode com `code` genérico (24/9007/9004) e virava `AuthError`, abortando a fila e mandando renovar um token vivo | `publish.py:93-94` (+2207027, +2207052) e `publish.py:105-113` (2 linhas novas, **depois** de `AUTH_CODES`) | `test_publicacao.py` +4 casos com os payloads REAIS colhidos dos runs `33408793664`/`34042496969`/`32043350962` | **SIM** — rodei a suíte ANTES do patch: `EXIT=1`, 3 FALHAS nominais. Depois: `TODOS PASSARAM`. Controles positivos intactos, incluindo o caso novo `190 + subcode 2207006` (token morto com subcode de mídia junto **continua** vermelho) |
| **M2** | **`checar_cfm.py` ganha exit real** — não tinha `sys.exit` nenhum; o `\|\| echo "::warning::"` do `publish.yml:51` era código morto desde 30/08 | `checar_cfm.py` (bloco `__main__`) | controle **negativo**: acervo limpo → `VIOLACOES 0`, **EXIT=0** (sem falso alarme, e os ~30 REVISAR crônicos seguem não pontuando); controle **positivo**: violação semeada → `VIOLACOES 5`, **EXIT=1** | **SIM** — o mesmo controle positivo dava EXIT=0 antes |
| **M3** | **Pulso de insights deixa de mentir por omissão**: nomeia a métrica que falhou, persiste a série DIÁRIA de `follower_count` (coletada e jogada fora), pagina `/media` (o 90d saturava em 100 e comia o início da própria janela) e reprova o dump por erro **fora** da lista de conhecidos | `insights_pulse.py:53-58, 85-86, 110-114, 116-123, fim` | `py_compile` OK + teste isolado do portão com 4 controles: só-crônico→0, métrica nova→1, `/media` falhou→1, sem erro→0 | **SIM** — hoje qualquer erro sai exit 0 e o dump passa pelas 4 validações do SKILL |
| **M4** | **Os dois CI ganham batimento cardíaco**: `schedule` diário em `ci-testes.yml` (06:40 BRT) e `gate-aprovacoes.yml` (09:00 BRT) — `on: push` é inalcançável num repo cujo único committer é o bot | `.github/workflows/ci-testes.yml:6-15` e `gate-aprovacoes.yml:20-27` | YAML parseado: gatilhos `['push','pull_request','schedule','workflow_dispatch']` e `['push','workflow_dispatch','schedule']` | **SIM** — 38 pushes/12 dias, 0 runs |
| **M5** | **Os dois SKILL.md que decidem a v2 e os 4 dumps restantes** + hedge do gatilho da própria v2 | `.claude/scheduled-tasks/instagram-dumps-janela-v2/SKILL.md` e `.../instagram-auditoria-v2/SKILL.md` | mudanças em vigor **agora** no agendador (a tarefa `instagram-auditoria-v2` passou de one-time 16/09 para cron `0 9 16,17,18 9 *`, com guarda de idempotência no passo 0) | — |

**Detalhe do M5 (é o que protege a v2):**
- **Dumps:** validação **(e)** `erros` só pode conter o crônico conhecido (`total_interactions+follow_type`, que falha na Meta desde 02/08 — reprovar por `erros != []`, como o C11 mandava ao pé da letra, derrubaria **5 de 5** dumps bons); **(f)** teste de truncamento (peça mais antiga × início da `janela`) — foi ele que pegou o `_90d` de 12/09; **(g)** nunca sobrescrever arquivo existente; e **`-f days=31` no dia 15/09**, o único recorte que fecha exatamente 16/08→15/09 (nenhum dump existente está ancorado em 16/08).
- **Auditoria v2:** Adendo 3 com clone FRESCO obrigatório (o clone que o SKILL apontava está em `99924b1`, **26 dias atrasado**, sem `aprovacoes.json` nem os dois CI), glob dos dumps em vez de lista de datas vencida, critério de aceite da telemetria (`n > 95`), as **4 duplicatas e os 7 dias de stories contaminados** com os `media_id` nominais, a cobrança de **contagem de execuções** das guardas, e `coordenar.py registrar` + lock `deploy-instagram`.
- **Registro:** entradas datadas no `CHANGELOG_JANELA_V2.md` (cópia durável da oficina) — merge da v1.5, as 4 duplicatas com media_id, os 4 runs vermelhos com alarme falso, a **NÃO-ocorrência de 05/09**, o dump recuperado de 02/09, e as mudanças de coleta feitas hoje. A tabela "Registro de coleta" saiu de `[PLANEJADO]` para o estado real.
- **Patch aplicável (M1–M4), pronto para `coord_git.py`:**
  `<workspace>/Presenca_Online/06_Automacao_Instagram/AUDITORIA/patches/v16_2026-09-11_classificador-lint-pulso.diff`
  (6 arquivos, +97/−9; suítes `test_publicacao.py` e `teste_publish_exit.py` verdes depois dele).

**Critério de parada honrado:** parei no que exige o Rafael (aprovar o lote VERBETES, decidir as 2
peças duplicadas no grid, ratificar o legado, exposição do repo) e no que muda o COMPORTAMENTO do
caminho que publica dentro da janela (`ref: main` no checkout, write-ahead da sequência, reconciliação
do push) — esses estão especificados por arquivo/linha em §5 e devem entrar **em 16/09**, não hoje.

---

## 3. Checklist binário (não pontua — existe ou não existe)

| guarda | v1.5 | v1.6 |
|---|---|---|
| Gate CFM in-process nas 4 rotas (`_cfm_guard`) | SIM | SIM |
| D17 (estético/estatura = VIOLAÇÃO) vivo no caminho de publicação | SIM | SIM |
| Fail-loud do publish provado por suíte que cobra EXIT | SIM | SIM (`teste_publish_exit.py` exit 0) |
| Guarda-freio de voz em TODOS os workflows que sintetizam voz | NÃO (1/4) | **SIM (4/4)** — nunca exercitada |
| `timeout-minutes` no publish.yml | NÃO | **SIM** — nunca acionado |
| CI de teste/CFM **executado** na main | NÃO | **NÃO** (7 e 4 runs, todos de 30/08) |
| Checador CFM do caminho vivo capaz de acusar VIOLAÇÃO | *creditado* | **NÃO** (exit fixo em 0; patch pronto) |
| Lint de CFM enxerga os carrosséis em produção | — | **NÃO** (sem Pillow: 0 de 54 slides) |
| `checar_aprovacoes` plugado em caminho mecânico que ROda | NÃO | **NÃO** |
| Gate de aprovação cobre posts.json e sequences.json | — | **NÃO** (20 de 151 itens pendentes) |
| Duplicata de publicação detectável por dado (não por log) | NÃO | **NÃO** (`state/published.json`: 0 ids e 0 media_id duplicados, com 4 duplicatas reais no ar) |
| Telemetria de estoque (runway + warning <30d) | NÃO | **NÃO** (3ª rodada) |
| Dump de insights reprova quando é parcial | NÃO | **NÃO** (patch pronto; validação (e) já em vigor no SKILL) |
| Dumps da janela ocorrendo nas datas | SIM (armados) | **NÃO** — 05/09 perdido, tarefa sem `lastRunAt` |
| Gatilho da auditoria v2 com redundância | NÃO | **SIM** (cron 16,17,18/09 + guarda de idempotência) |
| Decisão do Rafael sobre exposição do repo | PENDENTE | PENDENTE |

---

## 4. Placar da MÁQUINA

Mesmas 6 dimensões e **mesmos pesos da v1.5** (comparabilidade; nenhum peso mudou). Divisão P+R
idêntica. A coluna que soma está em PONTOS.

| # | dimensão (dano dominante se falhar) | peso | divisão P+R | v1.5 | proc | res | pts v1.6 |
|---|---|---|---|---|---|---|---|
| 1 | Conformidade clínica e guardrails — sanção CFM, dano a paciente | 26 | 14+12 | 21,0 | 9,5 | 10,5 | 20,0 |
| 2 | Confiabilidade do caminho de publicação — duplicata/peça errada no ar | 22 | 12+10 | 16,5 | 6,0 | 5,5 | 11,5 |
| 3 | Governança de aprovação e voz — publicar sem aval clínico; voz alterada | 20 | 11+9 | 11,5 | 5,0 | 5,0 | 10,0 |
| 4 | Telemetria e registro da janela — v2 cega, decisão sem dado | 14 | 8+6 | 9,0 | 5,0 | 3,5 | 8,5 |
| 5 | Estoque e pipelines — perfil seca ou publica legado mudo | 10 | 5+5 | 6,5 | 2,5 | 3,5 | 6,0 |
| 6 | Segurança e higiene do repo público — exposição de governança clínica | 8 | 4+4 | 4,5 | 2,5 | 1,5 | 4,0 |
| | **total** | **100** | | **69,0** | 30,5 | 29,5 | **60,0** |

**Par (Processo, Resultado): Processo 30,5/54 · Resultado 29,5/46** (normalizado: processo 56,5 · resultado 64,1).
Na v1.5: P 34,5/54 (63,9) · R 34,5/46 (75,0). **O Resultado caiu mais que o Processo** — e isso é
a notícia: pela primeira vez nesta frente o dano saiu do papel e chegou ao perfil.

### Delta separado — o que é alvo e o que é régua

| dimensão | Δ | **alvo piorou** (fato novo nos 12 dias) | **régua mais honesta** (sempre foi assim; agora medimos) |
|---|---|---|---|
| 1 Conformidade | −1,0 | — | −1,0: o step advisory do M5 é detector MUDO (exit fixo 0, provado com semente) e o lint audita **0 de 54 slides** de carrossel no CI (sem Pillow). A v1.5 creditou visibilidade que nunca existiu |
| 2 Confiabilidade | −5,0 | **−3,0**: 4 publicações duplicadas na janela, 2 delas **permanentes no feed** e vivas hoje; 11 frames de story duplicados só desde a v1.5; 3 peças da janela publicadas com 1h18–2h26 de atraso | −2,0: o classificador de auth lê o campo errado desde sempre (6 runs vermelhos na janela por essa causa), e o instrumento que a v1.5 usou para dizer "0 colisões de id" é cego a duplicata por construção |
| 3 Governança | −1,5 | −0,5: 20 das 28 peças publicadas desde 30/08 (posts+sequências) não têm aval clínico registrado em lote nenhum | −1,0: o enforcement do M2 não está só ausente — é **inalcançável** pelo gatilho escolhido; e o universo do gate é **20 de 151** itens pendentes (posts.json e sequences.json não entram nem no `--fila` nem no `paths:`) |
| 4 Telemetria | −0,5 | −0,5: ponto de 05/09 perdido em definitivo; 90d truncado; changelog 12 dias sem linha | +0,0 líquido: a régua ficou mais dura (erros anônimos, truncamento silencioso, `dia` = medição e não publicação) **e** esta rodada já instalou as validações — o que compensa exatamente a perda de processo |
| 5 Estoque | −0,5 | — | −0,5: 3ª reincidência do B7 e C12 nunca escrito; a fila em si entregou 8/8 reels e 7/7 posts nas datas projetadas |
| 6 Segurança | −0,5 | −0,5: a **ata da v1.5 publicou no repo público** o UUID da sessão, o username e o caminho `.claude/` — a rodada que escreveu o achado C7 cometeu o C7 | +0,0: varredura do histórico por conteúdo (0) e refutação do crescimento de 3 MB/dia melhoraram a régua para cima e para baixo, e se anulam |
| **total** | **−9,0** | **−4,0** | **−5,0** |

```bash
python "<workspace>/_Ferramentas_Comuns\auditoria\fechar_rubrica.py" "<scratchpad-da-sessao>"
```

**Como cada dimensão foi medida (reexecutável, executado pelo juiz):**

1. **Conformidade** — `PYTHONIOENCODING=utf-8 python checar_cfm.py; echo $?` → `VIOLACOES 0`, **EXIT=0**; com violação semeada em `reels.json[0]` → `VIOLACOES 5`, **ainda EXIT=0** (antes do patch). `sequences.json: 0 legendas auditadas`, `stories.json: 0`. Em CI, `No module named 'PIL'` ⇒ `carrossel.POSTS` (9 posts / 54 slides) nunca auditado; local, com Pillow, audita os 54. `gate_publicacao.py` → 4 BLOQUEIOS, EXIT=1, **não plugado em workflow nenhum** (`git grep gate_publicacao -- .github/` = 0) — e isso está DOCUMENTADO como decisão no protocolo de deploy, não é gate burlado.
2. **Confiabilidade** — `gh run list --workflow publish.yml --status failure --limit 100` → **13 runs vermelhos operacionais dentro da janela 16/08→15/09** (17/08 ×4, 19/08, 20/08, 23/08 ×2, 29/08, 31/08, 02/09, 06/09, 08/09) + 1 semeado pela própria v1.5. Desde o merge: **159 runs, 155 verdes, 4 vermelhos**. Duplicatas conferidas contra a Graph API (`insights_2026-09-12_90d.json`) e contra `state/stories_serie.json`. `state/published.json`: 216 registros, **0 ids e 0 media_id duplicados**. Nada foi pulado: 28 peças desde 30/08 (13 seq em 13 dias corridos, 8 reels, 7 posts). Taxa de entrega do cron: ~13,2 runs/dia contra ~62 nominais (**~21%**).
3. **Governança** — `checar_aprovacoes.py --auto-teste` = 11/11 com 8 reprovações observadas; gate real na fila → exit 0, **"Universo verificado: 20 item(ns) (43 isentado(s))"** contra 151 itens pendentes (63 reels + 34 posts + 54 sequências); `grep -i VERBETE aprovacoes.json` = 0; `LEGADO-PRE-GATE` 45/45 com `hash_roteiro: None`. `gh run list --workflow gate-aprovacoes.yml` = 4 runs, todos de 30/08.
4. **Telemetria** — 5 dumps existentes, **todos** com `erros: ["***/insights: An unknown error has occurred."]` e **todos** sem `total_interactions_por_follow_type` (métrica identificada por eliminação: o loop pede views/reach/total_interactions e só essa falta). `_90d` de 12/09: 100 peças, janela declara 14/06, peça mais antiga **19/06** — truncado sem erro. `stories_serie.json`: 40 dias, 9 fora do baseline 5, 7 deles na janela. `instagram-dumps-janela-v2` **sem `lastRunAt`**.
5. **Estoque** — FIFO com as regras de `publish.py`: reels 63 pendentes → 30/12; posts 34 → 08/11; sequências 54 → 04/11 (último commit em `sequences.json`: **03/07**, 70 dias). `stories.json` com 88 órfãos ainda inflando o RUNWAY. `gerar_programacao.py` inexistente; `PROGRAMACAO.md` cobre 18 de 63 reels (29%) e acaba em 12/10; reel04 em **18/10** — projeção da v1.5 confirmada sem deriva.
6. **Segurança** — `git grep -I -E "(EAA…|ghp_…|github_pat_…|IGQ…|sk-…)"` → só placeholder; histórico por CONTEÚDO → 0 (limite: clone `blob:none`, binários e logs de Actions não varridos). `AUDITORIA/rodadas/maquina_v1.5_2026-08-30.md`: 2 ocorrências de `C:\Users`, 1 UUID de sessão, 1 caminho `.claude/` — e o controle negativo (ata da v1) dá 0/0/0/0. Crescimento em 12 dias: **5.697 bytes**.

---

## 5. Achados ranqueados — só CONFIRMADO/AJUSTADO (3 REFUTADOS descartados)

**~60 achados propostos nas 4 dimensões · 3 REFUTADOS · 18 AJUSTADOS pelo cético · 4 lacunas promovidas.**
Refutados: (i) "o PIL derrubou os runs vermelhos" — a linha aparece idêntica em runs VERDES; (ii)
"`wait_finished` causou os 400" — aritmética de timestamp nos 5 logs mostra intervalo de 4,6–6,4 s,
ou seja **zero** `sleep(6)`: o primeiro poll devolveu FINISHED e o `return True` de esgotamento nunca
rodou (o defeito de aprovar por omissão é real, mas é P2, não causa); (iii) "as duas cópias do
changelog divergem" — `diff --strip-trailing-cr` sai vazio, a diferença era CRLF.

### P0 — causa raiz do dano público (conserto em 1 frase)

| id | achado | conserto |
|---|---|---|
| **P0-1** | **Erro de mídia da Meta classificado como token morto.** `publish.py:96-107` procura a família `2207xxx` só no `code`, e a Meta a manda no `error_subcode` com `code` genérico: `{code:24, sub:2207006}` (31/08, 02/09), `{code:9007, sub:2207027}` (06/09), `{code:9004, sub:2207052}` (17/08 ×4). Cai no catch-all `type == OAuthException` → `AuthError` → aborta **todos** os blocos do dia e imprime "renove o secret IG_ACCESS_TOKEN" com o token vivo (renovado 31/08 e 07/09, expira 06/11). 6 runs vermelhos na janela por essa causa. | **JÁ IMPLEMENTADO** nesta rodada (M1): duas linhas lendo `sub`, inseridas **depois** de `AUTH_CODES` — inseri-las antes, como uma das dimensões propôs, faria `{code:190, sub:2207006}` deixar de acender o alarme de token morto (medido). |
| **P0-2** | **4 publicações duplicadas dentro da janela limpa, 2 delas permanentes no feed.** `18108017225169506`+`18101453204354733` (reel `qa_pe_torto_bebe`, 19/08, 2 min de diferença) e `18037328645821486`+`18581696311066646` (carrossel `post45`, 20/08) estão **vivas na conta** e dentro do `detalhe_pecas` que a v2 vai ler; o state registra só o primeiro de cada par. Mais 20 frames de story a mais na janela (18/08 +1, 24/08 +7, 30/08 +1, 01/09 +2, 03/09 +2, 07/09 +2, 09/09 +5). Duas causas: o P0-1 (sequência morre no frame 3, frames 1-2 ficam no ar sem registro, o run seguinte republica do 1) e o P0-3. | Registro **já feito** no changelog com os media_id; deduplicação instruída no SKILL da v2 (M5). Código: write-ahead em `publish.py:274-284` (gravar cada `mid` à medida que sai) + retomada por frame em `publish.py:406-415` — **16/09**, porque muda o comportamento do publicador. |
| **P0-3** | **`actions/checkout@v4` sem `ref:` fixa o SHA do evento.** Em 08/09, dois runs nasceram a 50 s de distância com o **mesmo `headSha` `1524aa37`**; o primeiro publicou e empurrou `ab0bdd6` às 15:31:47Z; o segundo fez checkout do SHA velho às 15:32:21Z (**34 s depois** do push), viu o item pendente e republicou os 5 frames. `concurrency` serializou os jobs — não reabriu a leitura. | `publish.yml:38` → `with: {ref: main, fetch-depth: 0}` **e** releitura de `origin/main:state/published.json` antes de decidir, com teste semeado visto FALHAR. **16/09**. Mitigação de custo zero para os 4 dias restantes: tirar o `30` do cron `30,40,50 15 * * *`, que colide de propósito com o dispatch do cron-job.org das 15:30:07 (o par que duplicou). |
| **P0-4** | **O retry de push não pode convergir.** `publish.yml:90-100` repete `git pull --rebase` e `git rebase --abort` 5×; contra conflito de CONTEÚDO no mesmo JSON o resultado é idêntico nas 5 tentativas. Medido em 4 runs (19/08, 20/08, 23/08, 08/09): `CONFLICT (content)` ×5 e `Estado NAO salvo apos 5 tentativas` — **com a peça já no ar**. É a origem direta dos 2 órfãos de feed. | Reconciliação por conteúdo (união de `published[]` por `id`+`media_id`, `last_*_date` = máximo) em vez de rebase textual; ou `state/published.d/<RUN_ID>.json` append-only. O mesmo laço cego está copiado em `stories.yml:48-58` e `render-verbetes.yml:52-62` — a guarda vale no irmão. **16/09**. |
| **P0-5** | **O dump de 05/09 se perdeu e é irrecuperável no corte temporal.** Tarefa `enabled`, cron de dias esparsos, **sem `lastRunAt`**. A v1.5 escreveu na própria meta-auditoria "medir antes de 05/09, senão os 3 dumps viram não-ocorrência silenciosa" — ninguém mediu. Mecanismo do agendador **desconhecido**, não "app fechado": em 01/09 duas tarefas one-time com `fireAt` a 30 min de distância tiveram destinos opostos (`gbp-video-verificacao` recuperou às 23:39Z; `lembrete-blanc-repasse-cremesp-pj` nunca rodou e segue zumbi há 10 dias). | **JÁ IMPLEMENTADO** (M5): cron dos dumps em dias consecutivos, validações novas, e a **própria v2 deixou de ser one-time** (cron 16,17,18/09 + guarda de idempotência). O que falta e é do Rafael: decidir o zumbi de outra frente. Recuperação parcial já feita: dump de 02/09 extraído do log do run `33649533537` e salvo com bloco `_procedencia`. |

### P1

| id | achado | conserto |
|---|---|---|
| **P1-6** | **A rede de CI da v1.5 está inerte há 12 dias**: `ci-testes.yml` (`on: push` sem filtro) teve **0 runs em 38 pushes**, porque 38 de 38 commits são do `github-actions[bot]` e push com `GITHUB_TOKEN` não dispara workflow. "Instalado ≠ em vigor" reincidiu **dentro do conserto escrito para curá-lo**. | **JÁ IMPLEMENTADO** (M4): `schedule` diário nos dois. Prova exigida depois do merge: um run com `event: schedule` em `gh run list --json event`. |
| **P1-7** | **O checador do caminho vivo é mudo e meio-cego**: exit fixo em 0 (M2 desta rodada conserta) **e** sem Pillow no CI ele audita **0 de 54 slides** de carrossel, contabilizando a própria falha de import como uma linha REVISAR entre 29. | `requirements.txt` (ou um `pip install pillow` só no step) + tratar `import_carrossel` como erro de INSTRUMENTO, nunca como item auditado. |
| **P1-8** | **O gate de aprovação cobre 20 de 151 itens pendentes.** `--fila` aceita um arquivo só; `posts.json` (34 pendentes) e `sequences.json` (54) não estão no comando nem no `paths:`. Os 30 posts `c_on_*`/`c_pnc_*` começam a ir ao ar em **19/09**. | `--fila` múltiplo + declarar no log os itens publicáveis fora do escopo + cunhar `LEGADO-FEED-PRE-GATE` para a dívida ficar nomeada em vez de inexistente. |
| **P1-9** | **A ata da v1.5 vazou no repo público** o UUID da sessão, `C:\Users\<user>` (2×) e o caminho `.claude/scheduled-tasks/` — controle negativo: a ata da v1 dá 0 nas quatro contagens. O C7 original segue aberto (`APROVACOES.md:7` cita fala do Rafael verbatim; `aprovacoes.json` ×3 cita o nome da sessão interna). | Neutralizar as 4 ocorrências; **prova já executada**: reescrevi as 3 citações numa cópia e rodei o gate → `OK … hash conferido`, exit 0 — o campo `evidencia` não entra no hash, a edição é segura. |
| **P1-10** | **`PROGRAMACAO.md` acaba 6 dias antes do penhasco.** Acerta 18/18 reels e 5/5 posts futuros, mas para em 12/10, e reel04 entra em **18/10**; 12 dos 25 ids citados já foram publicados. É a única superfície de revisão passiva do Rafael. | Escrever o `gerar_programacao.py` que o C12 especificou (a FIFO já foi validada por comando em três rodadas) e chamá-lo do `stories.yml`, que roda todo dia e já commita. |
| **P1-11** | **Registro sem mecanismo**: o changelog ficou 12 dias sem uma linha e anunciava como "em branch" o que estava em produção desde 30/08 18:43. | Registro do passado **já feito** (M5). Mecanismo: step no `stories.yml` que acrescenta linha automática quando o run termina vermelho ou quando `stories_ativos != 5`. |
| **P1-12** | **D-day de 17–18/09 sem nada pronto do lado da máquina**: lote `VERBETES-2026-09` inexistente (`grep` = 0), nenhum enfileiramento verbete→`posts.json` (é vedado por desenho em `gerar_verbetes.py:24,554`), marcador de origem do wa.me só diagnosticado em `perfil.json:27`, CTA de reply exigiria re-render (itens de `sequences.json` só têm `id/theme/label/images`), canário de arquivamento sem script. | Cunhar o lote pendente com hashes **antes de 16/09** (é registro, permitido) para o Rafael só assinar; escrever `enfileirar_verbetes.py` com `--dry-run` e recusa por data; canário como script 100% leitura, lendo a peça por ID **e** varrendo a edge (a `/media` satura em 100 e daria falso "sumiu"). |

### P2

| id | achado | conserto |
|---|---|---|
| P2-13 | `wait_finished` (`publish.py:191-197`) devolve `True` ao esgotar as tentativas — aprova por omissão. Não causou os 400 observados (refutado por cronometragem), mas é fail-open no caminho do ato irreversível. | `raise RuntimeError` no estouro, com teste que force `IN_PROGRESS` sempre. |
| P2-14 | A suíte que aprovava o classificador era **verde e cega**: os 6 controles positivos usavam o número de mídia no `code`, forma que a produção nunca manda. | **JÁ CONSERTADO** (M1); acrescentar geração automática do par `{code:n}` × `{code:24, sub:n}` para a lista e a suíte não divergirem de novo. |
| P2-15 | Telemetria durável e **congelada**: `master.json.gerado_em = 2026-08-29`, `n: 95`, snapshots por nome fixo. | Glob em `monta_master.py:26-29` + `exit 1` se o snapshot mais novo for anterior a hoje−5d. Critério de aceite **já escrito** no SKILL da v2. |
| P2-16 | Taxa de entrega do cron: **~21%** do prometido (13,2 runs/dia contra ~62; gap mediano 80 min, p90 ~4,6 h, máximo ~8 h). O comentário "catch-all backup a cada 30 min" no `publish.yml:8` é a premissa declarada da tolerância a falha e está factualmente errada. | Corrigir o comentário para a taxa medida; para o D-day usar `workflow_dispatch` explícito, nunca o cron. |
| P2-17 | `stories_serie.json`: o campo `dia` é o dia da **medição**, não o da publicação (leitura ~07h UTC, 24 h para trás; as sequências saem 15:30 UTC). Cruzar peça com `dia` joga 100% dos pontos no dia errado. O `timestamp` por story é coletado e descartado (`stories_pulse.py:62` × `:102`). | Persistir `ts_min`/`dia_publicacao`; **não** reconstruir a série antiga em silêncio — o `quando` por story está nos logs do Actions (retenção 90 dias), então o backfill é da FONTE, não reconstrução, e precisa sair antes de ~01/12. |
| P2-18 | `PROTOCOLO_Deploy_e_Guardrails_IG.md` (mtime 6/jul) ensina severidade **invertida** em 2 de 5 regras e publica baseline falso ("EXIT=0, FALTA 0") — hoje é EXIT=1 e 4 FALTAs, o que faz todo deploy futuro parecer regressão do próprio commit. | Baseline **datado e reexecutável** + severidades corrigidas citando `33fdb5b` + ponteiro dentro do repo. |
| P2-19 | `docs/02_RUNBOOK.md` §2 leva a um CI vermelho determinístico (reproduzi com o exemplo do próprio doc: `REPROVADO — item sem registro`, exit 1) e os dois workflows de 30/08 têm **0 menções** em README + 3 docs. | Passo 2b (lote + hash + gate até exit 0) e passo 4 (regenerar PROGRAMACAO) + linha dos dois CI no inventário. |

### P3

| id | achado | conserto |
|---|---|---|
| P3-20 | `gate-cfm.yml` fantasma: `active` na API, arquivo inexistente na main, 0 runs em 48 dias. | Matar a branch e o registro (o advisory do publish cobre o caminho vivo). |
| P3-21 | `docs/01_INVENTARIO.md` anuncia dois crons de voz desligados desde 29/08 e uma fila com 84 reels (são 120) e 11 publicados (são 216 registros). | Estado dos YMLs + trocar número em prosa por comando datado. |
| P3-22 | Graph API `v21.0` fixada em 4 executáveis com override `GRAPH_VERSION` **nunca cabeado** (`git grep GRAPH_VERSION -- .github/` = vazio; `actions/variables` vazio). Prazo citado (21/01/2027) **não tem fonte no repo** — não publicar como fato. | Criar a variável de repo e passá-la no `env` dos 3 workflows; confirmar a data de sunset na doc da Meta na v2. |
| P3-23 | `insights.yml` não sobe artefato (`artifacts.total_count = 0`) — o dump só existe como log, com retenção de 90 dias. | `actions/upload-artifact` com `retention-days: 90`: transforma "recuperável raspando log" em "baixável". |
| P3-24 | `stories.json`: 88 órfãos desde 07/06 inflando o RUNWAY; rota viva só por `FORCE_ID`. | Rotular como **manual** no relatório de runway (não apagar a linha: some a visibilidade de uma rota que um dispatch ainda dispara). |

---

## 6. Fila do Rafael (só ele pode fazer) — por prazo

| prazo | o que | por que só ele | bloqueia |
|---|---|---|---|
| **antes de 16/09** | Decidir o que fazer com as **2 peças duplicadas vivas no grid** (`18101453204354733` reel de 19/08 e `18581696311066646` carrossel de 20/08): apagar (muda o grid e o `media_count` dentro da janela — exige entrada no changelog) ou manter e deduplicar só na leitura | ação pública irreversível no perfil | leitura limpa da v2 |
| **antes de 16/09** | **Aprovar o lote `VERBETES-2026-09`** (20 verbetes prontos desde 30/08) | aprovação clínica | D-day 17–18/09 inteiro; é o único item que a máquina não recupera em 6 dias |
| 16/09 (pauta da v2) | Ratificar (ou não) o `LEGADO-PRE-GATE` (45 eps, **45/45 sem hash**) e decidir **reel04–reel30 antes de 18/10** | aprovação clínica | penhasco de 18/10; 7 legados mudos vão ao ar antes da v2.1 |
| 16/09 | Lote `ALONGAMENTO-KIDS` (11 eps, `pendente` desde 30/08) e os 4 jargões do `gate_publicacao` (D8) | idem | gate sai FAIL há 12 dias |
| 16/09 | Exposição do repo público — **com o acoplamento novo**: os previews da `PROGRAMACAO.md` respondem HTTP 206 hoje; repo privado quebra a janela de revisão passiva dele (e Release assets herdam a visibilidade, não servem de saída) | governança/custo | B1, C7, C8, D12 |
| quando puder | Encerrar/desabilitar o zumbi `lembrete-blanc-repasse-cremesp-pj` (outra frente, 10 dias vencido, `nextRunAt` no passado) | é tarefa dele, de outra frente | higiene do agendador |
| 17–18/09 | D-day no app: pinos, Reorder Grid, destaques, bio com marcador de origem | ações no app | Apostas 7 e 8 |

---

## 7. Meta-auditoria

**Que erro a v1.5 cometeu que esta rodada pegou (4):**
1. **Creditou um detector que nunca podia acusar.** O M5 pôs `checar_cfm.py || echo "::warning::"` no caminho vivo e a v1.5 registrou isso como visibilidade entregue. O script não tem `sys.exit`: o `||` é inalcançável. A v1.5 provou que o *check* funciona e nunca perguntou se o *exit* existia — exatamente o vício que ela mesma catalogou ("cobrar o exit, nunca a redação da mensagem"), cometido na linha seguinte.
2. **Provou o check e não o gatilho.** M2 e M5-CI foram declarados instalados com base em runs vermelhos→verdes de 30/08, todos de push HUMANO. Ninguém perguntou **quem empurra commits neste repo no dia a dia** — a resposta era mensurável e é 100% bot. 12 dias, 38 pushes, 0 runs.
3. **Rebaixou um achado por ele ser invisível.** B2 foi para P1 com a justificativa de que "duplicata de sequência seria invisível". Aconteceu 4 vezes, duas delas **visíveis e permanentes no feed**, e o detector que a tornaria visível (`stories_ativos` no pulso diário) já estava no repo desde 03/08 — coletado e não lido.
4. **Escreveu a data e não o vigia.** A própria meta-auditoria da v1.5 diz "medir antes de 05/09, senão os 3 dumps viram não-ocorrência silenciosa". A data chegou, ninguém mediu, e o dump se perdeu **no dia exato**.

**Achados REINCIDENTES — o indicador mais feio, e piorou:** a v1.5 tinha 6; a v1.6 tem **9**:
telemetria de estoque (3ª rodada), corrida de leitura do state (2ª — e disparou), CI de conformidade
na main (3ª), `gerar_programacao.py` (2ª), lint cego a sequences/stories (2ª), dump parcial passa
verde (2ª), vazamento no repo público (2ª — e piorou), `pat_expira_em` (2ª), "instalado ≠ em vigor"
(3ª rodada seguida, agora uma camada mais funda). Contra isso, o dado bom: **5 de 5 melhorias da v1.5
foram efetivamente implementadas e mergeadas**; o que falhou não foi a execução, foi a escolha do
gatilho e do critério de aceite.

**Alguma nota mudou sem o objeto mudar?** Sim, e está decomposto na tabela do §4: −5,0 dos −9,0 são
régua mais honesta (o objeto sempre foi assim; passamos a medir), e −4,0 são dano novo e datável.
Publicar −9,0 sem essa separação seria dizer que a máquina piorou duas vezes mais do que piorou.

**O que esta rodada NÃO mediu (declarado, não "está bom"):**
- Se as 2 peças duplicadas de feed **continuam publicadas neste minuto** — a prova é o dump de 12/09 (horas atrás), não uma leitura de agora; e a `/media` satura em 100, então **pode haver outros pares fora do teto**, em junho/julho.
- Se o `_cfm_guard` chegou a rodar nas peças republicadas; e o controle positivo dele em `theme`/`label` de sequência nunca foi semeado em nenhuma rodada.
- A retenção real da Graph API para `since`/`until` terminando em 05/09 — o script não tem parâmetro `until`, então o backfill nunca foi **tentado**; declarar "irrecuperável" é inferência, não medição.
- Conteúdo visual dos mp4/jpg; binários e logs públicos de Actions como superfície de segredo (o dump de 02/09 recuperado de um log público **prova** que essa superfície é ativa).
- A regra interna de recuperação do agendador (medimos o comportamento, não o mecanismo — e ele tem contraexemplo).
- Desempenho do perfil (por desenho — v2).

**Conclusões de ausência publicadas — universo medido?** "Nada foi pulado" = universo `state/published.json`
(28 peças, 13 sequências em 13 dias corridos), com o limite declarado: a fonte é o estado do robô, e
foi exatamente por aí que as 4 duplicatas se esconderam. "0 runs de ci-testes/gate-aprovacoes" =
`gh run list --workflow <arquivo> --limit 50` (n=7 e n=4, universo completo) cruzado com os 38 pushes.
"Nenhum segredo no histórico" = varredura por CONTEÚDO em `*.py|*.yml|*.json|*.md`, **num clone
`blob:none`** — limite declarado, a confirmação exige clone `--no-filter`.

**O que o humano teve de corrigir?** Nada nesta rodada (rodada de máquina). Mas duas regras dele
foram contrariadas pela máquina sem ninguém notar: o seguidor viu a mesma tela duas vezes em 4 dias
da janela, e o único canal de alarme real ("gere um novo token") foi saturado por 6 alarmes falsos em
26 dias — o próximo alarme verdadeiro chega num canal já desacreditado.

**A guarda vale no projeto irmão?** Três casos nesta rodada: o laço de push cego está igual em
`publish.yml`, `stories.yml` e `render-verbetes.yml` (consertar só um repete a lição de 29/08);
`_texto_auditavel` segue no `publish.py` e não no `checar_cfm.py` (C5, 2ª rodada); e o `sys.exit`
que faltava no `checar_cfm.py` existe no `checar_aprovacoes.py` e no `checar_voz.py` desde sempre.

**A suíte foi exercitada ao contrário?** Sim, quatro vezes, todas nesta sessão e todas **vistas
reprovar antes de valer**: os 3 payloads reais da Meta em `test_publicacao.py` (EXIT=1 antes, 0
depois); `checar_cfm.py` com violação semeada (EXIT=0 antes, 1 depois) e com acervo limpo (0 nos dois
— sem falso alarme); o portão do dump com 4 controles; e o gate de aprovação com o exemplo literal do
RUNBOOK (reprovou, como devia).

**Indicadores do processo:** achados propostos ~60 · **refutados 3 (5%)** · AJUSTADOS 18 ·
reincidentes **9** (era 6) · implementados na mesma sessão **5** · itens do backlog anterior
implementados por terceiros em 12 dias: **0** · tempo até implementar: os 5 M da v1.5 saíram na
própria sessão; nenhum item adiado foi entregue depois.

**O padrão que 12 dias autônomos revelaram — avaliação honesta.** A máquina **publica** muito bem: 28
de 28 peças, nas datas exatas da projeção, sem pular nada, com 155 de 159 runs verdes. O que ela não
faz é **saber o que fez**. Todos os defeitos caros desta rodada são da mesma família: o robô age, o
registro do ato falha, e nenhum instrumento interno consegue ver a diferença — a duplicata não aparece
no state, o alarme falso é indistinguível do verdadeiro, o dump perdido não acusa, o detector do
caminho vivo não pode acusar, o CI não roda e ninguém nota. **A camada de execução amadureceu; a
camada de evidência não.** E o dado de processo mais duro é este: dos 31 itens de backlog que a v1.5
deixou com dono e prazo, **zero** foram feitos em 12 dias — o item mais barato da lista (telemetria de
estoque, 30 minutos) está aberto há três rodadas, e o único com prazo explícito ("B2, antes do D-day")
virou o incidente que ele previa. A regra nº 1 do protocolo acaba de produzir seu caso mais caro.

**Defeito no próprio protocolo → duas regras novas para o changelog:**
1. **"Provar que o check reprova" e "provar que o gatilho dispara" são etapas separadas** — e a
   segunda exige declarar **quem gera o evento na operação normal** e **se essa classe de evento toca
   o que o check guarda**. Sem a segunda metade, instala-se um cron e chama-se enforcement.
2. **Rebaixar um achado porque "o dano seria invisível" exige entregar junto o detector que o torna
   visível** — senão o rebaixamento é a própria causa de o dano passar despercebido.

**Candidatas a lição transversal da casa (memória):** (a) erro de API pode chegar num campo
**irmão** do consultado — classificador que lê só `code` transforma falha transitória em falso alarme
de credencial; (b) **push com `GITHUB_TOKEN` não dispara workflow**: `on: push` é gatilho morto em
repo cujo committer diário é o robô; (c) **script sem `sys.exit` torna `|| echo` código morto** —
`grep -c sys.exit` é o teste de vida de qualquer checador antes de creditá-lo; (d) agendador local
não é infraestrutura: medir disponibilidade e **hedgear prazo com redundância**, porque o mecanismo
de recuperação tem contraexemplo; (e) eco de comando no log do Actions **não é saída do comando** —
dois auditores desta rodada leram o eco e reportaram um aviso que nunca foi emitido.

---

## 8. Recomendação sobre a auditoria v2 de 16/09

**Veredito: RODA — com o SKILL já ajustado (feito hoje) e com ressalva declarada na abertura da ata.**
Não adiar: a janela fecha em 15/09 e adiar só envelhece os dados.

Três condições, duas já cumpridas por esta rodada:

1. **✔ Cumprida — o gatilho.** A v2 era uma tarefa one-time num agendador com modo de falha
   comprovado e desconhecido (uma one-time recuperou e outra, 30 min depois, não). Agora é
   `0 9 16,17,18 9 *` com guarda de idempotência no passo 0.
2. **✔ Cumprida — o que ela lê.** Adendo 3 no SKILL: clone FRESCO (o que ela apontava está 26 dias
   atrasado e sem metade dos artefatos que ela vai auditar), glob dos dumps em vez de lista de datas
   vencida, critério de aceite da telemetria (`n > 95`, senão a ferramenta rodou sobre o passado), e
   as contaminações nominais.
3. **⚠ Depende do Rafael e dos 4 dias restantes — a ressalva que a ata da v2 tem de abrir declarando:**
   - a janela **não está limpa**: 2 peças duplicadas vivas no feed (deduplicar por par antes de
     qualquer média) e 7 dias de stories com frames a mais (excluir ou normalizar);
   - **não há ponto interno entre 15/08 e 12/09** — o de 05/09 não existe, e o de 02/09 é recuperado
     de log (proveniência diferente, marcada em `_procedencia`);
   - o `_90d` de 12/09 está **truncado em 100 peças**: a era 1/2 não está no arquivo, então
     comparação de coortes antigas pela janela de 90 dias é impossível com o que existe hoje;
   - nenhum dump está ancorado em 16/08 — só o `days=31` de 15/09 (já instruído) fecha a janela;
   - a métrica `total_interactions_por_follow_type` **nunca foi coletada** desde 02/08: é ausência
     estrutural, não queda;
   - as janelas de 30d são **rolantes e deslocadas** (29/08 e 12/09 compartilham 17 dias) — "−9,8% de
     reach NF" não é queda das mesmas peças.

**O que a v2 vai encontrar, para não confundir com efeito de conteúdo** (medido hoje): reach NF 30d
163 → 149 → 147; `followers_count` 1311 → 1309 → 1311 com ~21 novos por janela (**saldo líquido zero
em 14 dias**); `saves` 0 nos três pontos; `media_count` 76 → 91. Mais produção, menos alcance frio. A
meta NF ≥ 800 será perdida, como a Grande Revisão já previu por escrito.

**E o item que a v2 precisa herdar como pergunta, não como resposta:** o D-day de 17–18/09 é a única
alavanca de distribuição no calendário, e 4 dos seus 6 itens dependem de código que não existe. Se o
lote `VERBETES-2026-09` não for aprovado antes de 16/09, a estreia dos verbetes não acontece — e essa
é a decisão mais cara da semana.

---
*Melhorias M1–M5 desta rodada implementadas ANTES da publicação deste número, conforme a regra nº 1
do protocolo: M1–M4 provados por execução no clone (suítes vistas REPROVAR antes do patch) e entregues
como patch em `AUDITORIA/patches/v16_2026-09-11_classificador-lint-pulso.diff` — **não commitados**,
por ordem da sessão; M5 (os dois SKILL.md, o gatilho da v2 e as entradas do changelog) está **em vigor
agora**. Nenhuma ação tocou perfil ou fila publicável dentro da janela.
`fechar_rubrica.py`: **ok (1 rubrica, 0 defeitos)** — pesos somam 100; coluna de pontos soma 60,0;
denominadores do par conferem (P 14+12+11+8+5+4 = 54 · R 12+10+9+6+5+4 = 46).*
