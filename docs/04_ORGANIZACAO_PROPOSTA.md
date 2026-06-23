# Proposta de Organização + Plano de Migração Seguro
**Gerada em 23/06/2026.** ⚠️ **Não execute moves às cegas.** Mover arquivos quebra os paths que os
workflows e os JSON referenciam. Esta é a estrutura-alvo + um plano em fases reversível.

---

## Por que não reorganizei automaticamente
O sistema está **no ar** e ligado ao Instagram real. As dependências são por **caminho de string**:
- Workflows chamam `python gerar_reel_voz.py`, `python publish.py` (nome fixo).
- JSON apontam `reels/xxx.mp4`, `images/xxx.jpg` (path fixo).
- `gerar_reel_voz.py` faz `import render_reel` e `from episodios_pe_no_chao import get`.

Mover sem ajustar TUDO junto = publicação quebrada. Então: **docs e auditoria já entram (risco zero);
a reorganização de pastas é uma fase separada, coordenada, e idealmente testada antes do merge.**

---

## Estrutura-alvo proposta
```
06_Automacao_Instagram/
├── README.md                  # visão geral + aponta para docs/
├── docs/                      # ◄ JÁ CRIADO (arquitetura, inventário, runbook, auditoria)
├── engine/                    # o motor
│   ├── render_reel.py
│   ├── gerar_reel_voz.py
│   ├── gerar_reel_narrativo.py
│   └── carrossel.py
├── content/                   # dados de episódio (fonte)
│   ├── episodios_pe_no_chao.py
│   ├── episodios_novos_2026.py
│   ├── episodios_lote_julho_2026.py
│   ├── episodio_apresentacao.py
│   └── temporadas_data.py
├── generators/                # reabastecimento (reusável)
│   ├── gerar_conteudo.py
│   ├── gerar_sequencias.py
│   └── gerar_temporadas.py
├── publisher/
│   └── publish.py
├── library/                   # as filas (JSON)
│   ├── reels.json  posts.json  sequences.json  stories.json  destaques.json
├── media/                     # mídia
│   ├── images/  reels/  audio/
├── state/published.json
├── scripts_lote/              # ◄ lotes únicos já cumpridos (arquivo histórico, não roda sozinho)
│   ├── gerar_reels.py  gerar_lote_2026.py  posts_batch1.py  posts_batch2.py
│   ├── stories_batch.py  stories_batch2.py  reels_batch.py  anexar_lote_julho.py
│   ├── publicar_narrativos.py  publish_backup_single.py
├── voz/                       # experimental (treino de voz própria) — inalterado
└── .github/workflows/         # ajustados para os novos paths
```
> `engine/`, `content/`, `generators/` exigem ajustar os `import` (módulos mudam de pasta). A forma
> mais segura é **manter os .py na raiz** (onde os imports já funcionam) e só **arquivar os 🟡 lotes**
> em `scripts_lote/` + criar `docs/` + `media/` simbólico. Ou seja: organização **incremental**.

---

## Plano de migração em fases (cada fase é reversível e testável)

### Fase 0 — JÁ FEITA (risco zero) ✅
- Criado `docs/` (arquitetura, inventário, runbook, auditoria) e `_auditoria_motor.py`.
- Nada que o sistema usa foi tocado. **Pode commitar à vontade.**

### Fase 1 — Decisões pontuais (risco baixo) — *recomendada já*
- **Voz:** DECIDIR se o treino no Kaggle ainda é desejado (ver `03_AUDITORIA §1`). Se sim, deixar como
  está; se abandonado, comentar os `schedule:` de `voz-train.yml`/`voz-watch.yml`. **Não desligar às
  cegas** (é treino ativo, não desperdício).
- (Opcional) mover `publish_backup_single.py` → `scripts_lote/` (conferir antes que é mesmo cópia morta).
- **Teste:** rodar `publish.yml` manual com um `force_id` de teste → confirma que publicação segue OK.

### Fase 2 — Arquivar lotes cumpridos (risco baixo)
- Mover os 🟡 (`posts_batch*`, `stories_batch*`, `reels_batch`, `gerar_reels`, `gerar_lote_2026`,
  `anexar_lote_julho`, `publicar_narrativos`) → `scripts_lote/`.
- Mover os workflows de lote (`render-conteudo-2026`, `render-lote-2026`, `render-lote-julho-2026`) →
  arquivar ou apagar (já cumpriram). **Nenhum desses é chamado pela agenda**, então é seguro.
- **Teste:** `python _auditoria_motor.py` continua 0 refs quebradas; `publish.yml` manual OK.

### Fase 3 — Pastas do motor (risco médio — fazer numa branch, com teste)
- Mover `render_reel.py`, `gerar_*`, `episodios_*`, `temporadas_data.py`, `carrossel.py` p/ `engine/`,
  `content/`, `generators/`.
- Ajustar **todos os `import`** e **todos os `run: python <path>`** dos workflows juntos.
- Mover mídia para `media/` exige reescrever os paths dentro dos 5 JSON (script de migração + reauditar).
- **Teste obrigatório numa branch:** rodar `render-reel-voz` e `publish.yml` (force_id) na branch antes
  de mergear. Só mergear com os dois verdes.

> **Recomendação:** fazer **Fase 0 + 1 + 2 agora** (ganho real, risco baixo) e deixar a **Fase 3**
> para um momento dedicado com teste em branch — não às cegas, não com o Rafael fora.

---

## Convenções a fixar (para não voltar a bagunçar)
1. **Preview = prefixo `_`** (`reels/_preview_*.mp4`) nunca entra em JSON.
2. **id único e estável** em todos os JSON (o estado depende disso).
3. **Toda caption** termina com bloco CFM (CRM/RQE + disclaimer).
4. **Lote que já rodou** vai para `scripts_lote/` e **não roda de novo** (evita duplicação).
5. **Rodar `_auditoria_motor.py`** antes de commitar mudança em biblioteca.
