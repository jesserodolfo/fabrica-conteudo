# Time do Instagram no Claude Code (2026-11-06)

## Decisão
- A fábrica sai do OpenBot e volta pro Claude Code. Motivo: Mac de 8 GB travava com vários agentes do OpenBot ao mesmo tempo (swap 5,5 de 6 GB). Subagentes do Claude Code rodam dentro da sessão, sem processo novo por agente.
- Chefe do time: Gerente de Marketing (conversa principal), no lugar da FabIA. Organograma: Jessé › Gerente de Marketing › funções. Agentes sem nome próprio, só a função.
- Primeiro time só pro Instagram. YouTube vira outro time depois, reaproveitando estes.
- Regra de modelo: quem pensa em Opus 5.5, quem executa script em Sonnet 5.5, quem publica em Haiku 5.5.

## Time
| Função | Arquivo | Modelo |
|---|---|---|
| Gerente de Marketing | conversa principal (CLAUDE.md) | Opus 5.5 |
| Analista (radar, métricas, ideias e otimização) | agents/analista.md | Opus |
| Copywriter (roteiro, capa e legenda) | agents/copywriter.md | Opus |
| Designer | agents/designer.md | Sonnet |
| Editor de Vídeo | agents/editor-de-video.md | Opus |
| Revisor | agents/revisor.md | Sonnet |
| Publicador | agents/publicador.md | Haiku |

## Escolhas do Jessé (pendências 1, 2 e 3)
- 1a: Copywriter absorve titulista e roteirista (texto sai de uma voz só).
- 2b: Otimizador fica dentro do Analista, porque ele precisa ver se a própria pesquisa está dando resultado e corrigir sozinho.
- 3b: OpenBot desligado. Rotina 06:00 do Analista no Claude Code; relatório 07:00 já roda pelo launchd.

## Alternativas descartadas
- Manter o OpenBot: lentidão da máquina.
- Otimizador separado: sem dado suficiente ainda (menos de 2 semanas de posts no formato novo).
- Nome próprio pros agentes (AnalistIA, KopyIA, VisuIA): Jessé preferiu só a função.

## Fora do time Instagram (continuam em .claude/agents)
- diretor-de-cena (Kling) e parcerias.
- pesquisador, titulista e roteirista arquivados em `.claude/bak-pre-time-instagram/agents/`.
