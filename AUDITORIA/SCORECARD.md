# Scorecard — Auditoria Evolutiva do Instagram (@rafaelvargasmd)

Curva de notas por rodada. Cada rodada fica arquivada em `rodadas/` e **nunca é sobrescrita**.

| Rodada | Data | D1 Perfil (15%) | D2 Conteúdo (20%) | D3 Cadência (15%) | D4 Desempenho (20%) | D5 CFM/LGPD (20%) | D6 Motor (10%) | **GLOBAL** |
|---|---|---|---|---|---|---|---|---|
| **v1** (baseline) | 02/08/2026 | 42 | 48 | 55 | 16 | 64 | 63 | **46.5** |
| **v2** | 19/09/2026 | 46 | 54 | 59 | **22** | 66 | 67 | **50,85** |

## Como ler
- Nota 0-100 por dimensão; global = média ponderada pelos pesos.
- **D4 é o portão vinculante**: sem desempenho subir, subir as outras é cosmética.
- Distinga sempre **mudança real** de **correção de medição** (regra da casa).

**Diagnóstico central da v1:** O problema deste perfil nao e conteudo nem disciplina — e um circuito aberto nas duas pontas: metade das pecas (os 18 Reels) e publicada em modo de teste, fora do grid e longe dos seguidores, por um default de workflow que a propria casa ja mediu como morto e corrigiu numa branch que nunca foi integrada; e a outra metade, que chega aos 91,5% de audiencia ja seguidora, nao oferece uma unica coisa que se guarde, se responda ou se clique — dai 0 saves, 0 comentarios, 8,5% de descoberta e 2 cliques em 30 dias.

| v1.5 (máquina) | 2026-08-30 | 69,0 | Processo 34,5/54 · Resultado 34,5/46 — rodada da MÁQUINA (não compara com as rodadas de perfil); M1-M5 implementadas em `32fd4d9` antes do número; rodadas/maquina_v1.5_2026-08-30.md |
| v1.6 (máquina) | 2026-09-11 | 60,0 | Processo 30,5/54 · Resultado 29,5/46 (−9,0 vs v1.5; −4,0 alvo piorou, −5,0 régua mais honesta) — 12 dias autônomos revelaram 4 duplicatas públicas, CI inerte por gatilho morto e classificador de erro lendo o campo errado; M1-M5 implementadas e provadas em `220b651` antes do número; rodadas/maquina_v1.6_2026-09-11.md |

**v2 (19/09/2026) — o portão vinculante REPROVOU.** Global sobe 4,35 (46,5 → 50,85) e as seis dimensões
sobem, mas **D4 = 22 < 35**: pela regra escrita pelo juiz da v1, o resto é cosmético enquanto o desempenho
não sair do lugar. Diagnóstico: o circuito foi fechado de **um lado só** — a distribuição foi consertada e
entregou o previsto (trial desligado: views de reel 258 → 691, reach 240 → 439, zero reels com ≤3 views
contra 7 de 18), mas o que vem depois segue em zero MEDIDO (0 saves em 104 peças / 90 dias com o campo
`saved` respondendo 0 e não ausente; 0 sends de feed/reel; 0 replies de story em 34 dias) e o alcance por
peça cai −2,3/semana (r²=0,78) em coorte pareada por idade. A causa está nos arquivos: o conserto está em
ESTOQUE, não em vitrine — 92 das 127 legendas normalizadas nunca foram ao ar, 28 dos 29 cards da fila ainda
terminam em slide de CTA, e o D-day de vitrine de 17–18/09 não aconteceu (bio byte-idêntica em 5 dumps ao
longo de 35 dias). A janela mediu conteúdo velho publicado por um motor consertado.
Método: 13 agentes (6 auditores + 6 refutadores adversariais + 1 juiz); **as 6 notas caíram na refutação**
(52→46, 58→54, 62→58, 26→21, 71→66, 71→67) antes do juiz arbitrar. Rodada: `rodadas/v2_2026-09-19.md`.
