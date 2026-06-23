# Auditoria de Saúde do Motor
**Gerada em 23/06/2026** por `_auditoria_motor.py` (script não-destrutivo, só leitura — fica no repo;
rode `python _auditoria_motor.py` a qualquer momento para refazer).

---

## ✅ O que está saudável
- **0 referências de mídia quebradas** em 389 itens (posts+reels+sequences+stories+destaques). Toda a
  fila aponta para arquivos que existem → publicações não vão falhar por arquivo faltando.
- **Todos os 28 scripts compilam** (sem erro de sintaxe).
- **Todos os JSON são válidos** e **sem ids duplicados**.
- **Runway enorme** (conteúdo pronto na fila):

| Tipo | Total | Publicados | **Na fila** |
|---|---|---|---|
| Posts | 89 | 9 | **80** |
| Reels | 84 | 11 | **73** |
| Sequências | 121 | 16 | **105** |
| Stories | 89 | 1 | **88** |

> Com a cadência atual, são **meses** de conteúdo já produzido. O gargalo não é conteúdo.

---

## ⚠️ Pontos de atenção (não quebram nada, mas valem ação)

### 1. Pipeline de voz própria — VERIFICAR se ainda é desejado (NÃO desligar às cegas)
`voz-train.yml` (Seg/Qua/Sex 06:00) e `voz-watch.yml` (a cada 4h) **não são desperdício**: orquestram
um **treino real de voz pt-BR clonada em GPU do Kaggle** (resume de checkpoint, ~27h/sem sob a cota de
30h GPU do Kaggle; heartbeat no HuggingFace; auto-retry). Os jobs do **GitHub Actions** em si são
minúsculos (segundos: só `launch`/`watch`) — o custo de Actions é trivial; o trabalho pesado roda no
Kaggle. A voz de **produção hoje é a edge-tts (Antonio)** e funciona; este pipeline visa uma voz
**própria/clonada** futura.
**Ação:** **não desligar sem decidir.** Verificar se o treino ainda está ativo/desejado (heartbeat no
HF, secrets `KAGGLE_*`/`HF_TOKEN` válidos). Se **sim** → deixar rodando. Se **abandonado** → aí sim
comentar os `schedule:` (mantendo `workflow_dispatch`) para pausar sem apagar nada. Decisão do Rafael.

### 2. Código duplicado/morto
- `publish_backup_single.py` é cópia antiga do `publish.py`. **Remover** ou mover p/ `scripts_lote/`.
- `voz/voz_kernel.py` e `voz_train.py` têm **docstring vazia** (prováveis stubs). Revisar.

### 3. 17 imagens órfãs
17 `images/*.jpg` não são referenciadas por nenhum JSON (de 1168). Provável resíduo de iterações.
Limpeza opcional (não urgente). A pasta `images/_removidos_estetica/` é intencional (higiene CFM).

### 4. Workflows de lote já cumpridos
`render-conteudo-2026.yml`, `render-lote-2026.yml`, `render-lote-julho-2026.yml` produziram lotes que
já estão nas bibliotecas. Manuais (não gastam à toa), mas poluem a lista. **Arquivar** quando organizar.

### 5. Token (lembrete, não falha agora)
`IG_ACCESS_TOKEN` expira ~60 dias. Sem renovação, tudo para. Ver `02_RUNBOOK §5`. Vale um lembrete a
cada ~55 dias.

---

## Resumo executivo
O motor está **saudável e cheio** (fila pronta para meses). O item de impacto real é **(5) o token a
renovar** (~60d). O **(1) pipeline de voz** precisa de uma **decisão** (manter o treino ou pausar) —
não de desligamento automático. O resto é organização cosmética.
A reorganização proposta (`04_ORGANIZACAO_PROPOSTA`) é **opcional** e deve ser feita com cuidado, porque
mover arquivos quebra os paths que os workflows e JSON referenciam.

---

### Como reproduzir esta auditoria
```bash
cd <repo>
python _auditoria_motor.py        # imprime runway, refs quebradas, inventário, workflows, órfãos
```
