# 🩺 GUIA DE PRODUÇÃO — série "Recuperação"

> ⚠️ **Documento RECONSTRUÍDO em 25/07/2026.** O original foi perdido na troca de máquina
> (vivia fora do Git). Este texto foi remontado a partir das regras **já codificadas** em
> [`_lint_recuperacao.py`](../_lint_recuperacao.py) e das convenções no cabeçalho de
> [`episodios_pos_op.py`](../episodios_pos_op.py) — que o citam como fonte normativa.
> Se o original reaparecer, prevalece o original.

Vídeos **pós-operatórios para o paciente** (faceless, voz Antonio). Diferente de "Pé no Chão" e
"Osso Novo": registro em **2ª pessoa**, fala direta com quem operou, instrução clínica clara.
Saída serve como Short do YouTube **e** como link para enviar ao paciente na consulta.

---

## 1. As 7 convenções da série

Do cabeçalho de [`episodios_pos_op.py:7-19`](../episodios_pos_op.py#L7-L19). Todo episódio novo segue.

### C1 — Par adulto + infantil
Todo tema rende **dois** episódios: o adulto (fala com o paciente) e a irmã infantil (fala com
os **pais** sobre "seu filho"). O id infantil é `<tema>_kids`. Nunca publicar um sem planejar o outro.

### C2 — Alarme vai ao pronto-socorro, nunca ao WhatsApp
Sinal de alarme → **pronto-socorro imediato**, avisando a equipe **no caminho** (em paralelo, não
antes). O WhatsApp **(11) 3280-1413** é só para **dúvida de rotina**, e aparece na cena de resumo.
Esta é a regra de segurança mais importante da série.

### C3 — Alarme infantil são os "3 A"
A criança pequena não localiza nem descreve a dor, então os sinais clássicos chegam tarde. Os
gatilhos pediátricos precedem:

- **A**nalgesia ↑ — precisando de mais analgésico do que o esperado
- **A**nsiedade — criança que não se acalma
- **A**gitação — inquietação desproporcional

Somados a **dedos roxos ou frios** e **não mexe o membro**.

### C4 — Edema: elevar sempre, gelo nunca sobre o gesso
Elevar o membro **acima do coração** sempre que em repouso, **durante toda a recuperação** — não
só nos primeiros dias. **Sem gelo sobre o gesso** (o linter sinaliza qualquer menção a "gelo").

### C5 — Carga: nunca afirmar regra fixa
A frase-padrão é *"varia conforme a cirurgia; em geral proibida no início — siga sua equipe."*
Nenhum episódio prescreve quando pisar. Isso é decisão do cirurgião do caso.

### C6 — CFM (Res. 2.336/2023)
Conteúdo **educativo**. Sem prometer resultado, sem paciente real, sem antes/depois. Rodapé com
**CRM/RQE + disclaimer** em todo material.

### C7 — Processo: literatura → aprovação → render
Cada roteiro nasce de **revisão de literatura com fontes** e é **aprovado pelo Rafael (RQE) ANTES
do render**. Não existe render de roteiro não aprovado.

**Voz:** edge **Antonio**, `rate -8%`, `pitch -4Hz`.

> 📌 **Pendência conhecida.** O cabeçalho aponta os roteiros para `projeto YouTube/videos_pos_operatorio/`.
> Essa pasta **não veio na troca de máquina** e não está em nenhum repositório — ver
> [`03_AUDITORIA.md`](03_AUDITORIA.md). Os episódios em si estão preservados em
> `episodios_pos_op.py`; o que falta são os roteiros-fonte e as notas de literatura.

---

## 2. Estrutura de um episódio

```python
{"id": "gesso_pos_op", "ep": 1, "temporada": "pos_operatorio",
 "serie": "Recuperação", "motif_family": "bone",
 "scenes": [
   {"k":  "Pós-operatório",                    # kicker (rótulo curto no topo)
    "sc": ["Saiu de gesso", "depois da cirurgia?"],   # 1-2 linhas na tela
    "e":  None,                                 # ênfase: substring de sc, ou None
    "sub":"Os cuidados que protegem o resultado.",    # subtítulo
    "vo": "Você operou e saiu de gesso..."},    # narração
 ],
 "caption": "..."}
```

| Campo | Regra |
|---|---|
| `sc` | lista de **1 ou 2** linhas. Nunca 0, nunca 3+ |
| `e` | `None` **ou** substring exata de alguma linha de `sc` |
| `vo` | não-vazio, sempre |
| `caption` | precisa conter `CRM`, `RQE` e `não substitui` |

**Total de cenas: 6 a 9** (ideal 8).

---

## 3. As regras R1-R7 do linter

Codificadas em [`_lint_recuperacao.py:10-18`](../_lint_recuperacao.py#L10-L18).
**ERRO bloqueia** (exit 1); **WARN** apenas sinaliza.

| Regra | O que valida | Falha como |
|---|---|---|
| **R1** | `serie == "Recuperação"` | ERRO |
| **R2** | 6-9 cenas; `sc` com 1-2 linhas; `vo` não-vazio; `e` é substring de `sc` | ERRO (contagem de cenas → WARN) |
| **R3** | Ao menos uma cena cita **"pronto-socorro"** | ERRO |
| **R4** | `caption` tem o bloco CFM: `CRM`, `RQE`, `não substitui` | ERRO |
| **R5** | `caption` ou alguma cena cita o canal de rotina (**WhatsApp**) | WARN |
| **R6** | Todo id base tem irmã `<id>_kids` | WARN (base sem irmã) / ERRO (`_kids` órfã) |
| **R7** | Termos sensíveis CFM/clínicos → revisão humana | WARN |

### R7 — a lista de termos a revisar

```
garant · cura  ·  cura. · estétic · estatura · mais alto · ficar alto
ganhar altura · aumentar a altura · milagr · melhor médico · sem dor
```
Mais uma checagem separada para **"gelo"** (regex de palavra inteira).

**Por que "altura" é tabu — e por que nem sempre:** o tabu é a altura **estética** do alongamento
ósseo (ficar mais alto, ganhar centímetros). *"Acima da altura do coração"* é elevação legítima e
**não** é infração — o comentário em [`_lint_recuperacao.py:24-25`](../_lint_recuperacao.py#L24-L25)
registra essa distinção. Daí a lista mirar `estatura`, `mais alto`, `ganhar altura` em vez de
`altura` sozinho.

### Rodando

```bash
python _lint_recuperacao.py            # valida a série inteira
python _lint_recuperacao.py gesso_pos_op   # valida um episódio
```

Sai com **código 1** se houver qualquer ERRO. Avisos não bloqueiam, mas cada um pede olhada humana
antes de aprovar.

---

## 4. Fluxo de produção

```
1. Escolher o tema          → conferir que o par adulto+infantil está planejado (C1)
2. Revisão de literatura    → reunir fontes (C7)
3. Escrever o roteiro       → gancho por ganchos.info(id); 6-9 cenas; alarme → PS (C2/R3)
4. Metadados                → seo_youtube.gerar() + score_seo() ≥ 90
5. python _lint_recuperacao.py <id>   → 0 ERROS
6. Aprovação do Rafael (RQE)          → OBRIGATÓRIA, antes do render (C7)
7. Render                   → voz Antonio, rate -8%, pitch -4Hz
8. Publicar
```

Os passos 5 e 6 não são opcionais e não trocam de ordem: o linter roda **antes** da aprovação,
para que o revisor humano não gaste atenção com o que a máquina já pega.

---

## 5. Checklist rápido

- [ ] `serie` = "Recuperação" e o par `_kids` existe ou está planejado
- [ ] 6-9 cenas, `sc` com 1-2 linhas, todo `vo` preenchido
- [ ] Cada `e` é substring literal da sua `sc`
- [ ] Alguma cena manda ao **pronto-socorro**
- [ ] Se infantil: os **3 A** aparecem (C3)
- [ ] Edema → elevar; nenhuma menção a **gelo** sobre gesso (C4)
- [ ] Carga com a ressalva "siga sua equipe" (C5)
- [ ] Caption com **CRM + RQE + "não substitui"**
- [ ] WhatsApp presente e **só** como dúvida de rotina (C2)
- [ ] Nenhum termo R7 sem justificativa
- [ ] Linter limpo → aprovação RQE → render

---

## Referências cruzadas

- [`ESTRATEGIA_YOUTUBE_2026.md`](ESTRATEGIA_YOUTUBE_2026.md) — ganchos, título, descrição, tags, gate de SEO
- [`00_ARQUITETURA.md`](00_ARQUITETURA.md) — pipeline ponta a ponta
- [`SETUP_MODAL.md`](SETUP_MODAL.md) — infra da voz pt-BR
