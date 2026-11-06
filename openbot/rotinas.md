# Rotinas do OpenBot (colar no editor de rotina de cada agente)

Criar só depois do Teste 1 e do Teste 2 passarem. Executar cada uma na mão 3 vezes antes de deixar automática.

## Rotina 1 · Analista de Social Media · 06:30 todo dia · roda em thread própria

Instrução:

Rode o fechamento diário de métricas e radar.
1. Métricas: `.venv/bin/python /Users/dmelo/Documents/03-Marketing/cerebro-jarvis/scripts/puxar-metricas.py` com a chave do `.env` da fábrica, conta Instagram do `clientes/jesse-rodolfo/marca.json`, últimos 7 dias. Grave uma linha por post por dia na tabela `metricas_diarias` do banco compartilhado (chave única post_id + data). Hoje está incompleto, não compare.
2. Radar: skill `radar-concorrentes` nos perfis de `cerebro-jarvis/contexto/referencias-modelagem.md`. Grave em `radar` (perfil, data, link, gancho, formato, por que pegou).
3. Deixe no canal Conteúdo um resumo de até 15 linhas: melhor e pior post dos 7 dias com o número, 1 padrão observado, 3 ganchos de concorrente que pegaram. Nada além disso. Não publique, não agende, não responda comentário.
Se o Zernio falhar, escreva "métricas indisponíveis nesta execução" e siga com o radar.

Destino do resultado: canal Conteúdo.

## Rotina 2 · Gerente de Marketing · 07:00 segunda a sábado · roda no canal Conteúdo

Instrução:

Relatório do dia pro Jessé. Leia o resumo que o Analista de Social Media deixou no canal às 06:30, `ESTADO.md`, `cronograma.md` e `pesquisa/2026-11-calendario.md`. Monte o relatório no formato fixo da skill `relatorio-diario` (Ontem, Hoje na fila, Métricas 7 dias, 3 pautas pra hoje), no máximo 25 linhas, sem travessão, sem número inventado. Última linha sempre: "Responda 1, 2 ou 3 pra eu produzir". Não produza nada até o Jessé responder.

Destino do resultado: canal Conteúdo (chega no celular pelo app).

## Quando desligar o launchd antigo
Depois de 3 dias seguidos com a Rotina 2 chegando certa às 07:00:
`launchctl unload ~/Library/LaunchAgents/com.fusiongrowth.relatorio-conteudo.plist`
