---
name: relatorio-diario
description: Relatório diário do Time de Conteúdo. Use quando o Jessé pedir "relatório do dia", "como foi ontem", "o que postar hoje" ou quando rodar pela rotina das 07:00
---

# Relatório diário

Só lê e escreve o relatório. Não publica, não agenda, não edita post, não responde comentário. Sem travessão em nenhum texto. Nunca inventar número: sem dado, escrever "sem dado".

## Datas
Use a data que veio no pedido (AAAA-MM-DD, fuso de Brasília). Se não veio, rode `TZ=America/Sao_Paulo date +%F`. Calcule ontem com `TZ=America/Sao_Paulo date -v-1d +%F`. Anote o dia da semana de hoje.

## Passos
1. Estado local. Leia `cronograma.md` (linha de hoje e de ontem, carrossel 10h e reel 18h) e, em `posts/*/estado.md`, os que citam ontem ou hoje (use `grep -l` pela data em formato DD/MM e AAAA-MM-DD). O nome da pasta do post nem sempre é a data de publicação: valha o que o estado.md diz.
2. Zernio (só leitura), conta Instagram `account_id` do `clientes/jesse-rodolfo/marca.json`:
   - `posts_list`: não filtra por conta. Ignore tudo que não for Instagram e que não seja desse account_id. Separe publicados de ontem, agendados de hoje e falhos (`posts_list_failed`, se precisar).
   - `analytics_get_daily_metrics` dos últimos 7 dias para esse account_id: impressões, alcance, curtidas, comentários, compartilhamentos, salvamentos. O alcance diário somado não é pessoas únicas: diga "alcance somado". O dia de hoje está incompleto: não compare.
   - Se as ferramentas do Zernio não estiverem disponíveis ou derem erro, escreva "Métricas: indisponível nesta execução" e siga. Não tente outro caminho.
3. Pautas. Leia `/Users/dmelo/Documents/03-Marketing/fusion-marketing/contexto/subcrencas.md`, `historias.md` e `diagnostico.md`. Escolha 3 pautas de hoje:
   - cada uma com uma subcrença e uma história real que a sustente (sem história, descarte);
   - nenhuma nos ângulos queimados do `diagnostico.md`, a menos que traga ângulo, história ou conclusão nova (diga qual);
   - não repita tema já publicado ou na fila (cronograma e estados);
   - se hoje tem slot vazio no cronograma (carrossel 10h ou reel 18h), priorize pautas para ele;
   - número só se estiver em `provas.md` na mesma pasta. Na dúvida, sem número.
4. Escreva `saidas/relatorios/AAAA-MM-DD.md` (sobrescreve se existir), no máximo 25 linhas, neste formato fixo:

```
# Relatório do conteúdo · DD/MM (dia da semana)

## Ontem
- o que foi publicado (formato, tema, horário) ou "nada publicado"

## Hoje na fila
- carrossel 10h: ... (status: agendado, pronto, falta arte, vazio)
- reel 18h: ... (idem)
- alerta se houver post falho ou slot vazio

## Métricas (7 dias, @jesse.rodolfo)
- posts, impressões, alcance somado, curtidas, comentários, salvamentos, compartilhamentos
- melhor dia e observação curta, ou "indisponível nesta execução"

## 3 pautas pra hoje
1. formato · gancho de até 12 palavras · história que sustenta
2. ...
3. ...

Responda 1, 2 ou 3 pra eu produzir
```

5. Imprima o relatório inteiro na saída, igual ao arquivo, sem texto antes nem depois. A última linha é sempre "Responda 1, 2 ou 3 pra eu produzir".

## Regras
- Só diga que algo não saiu ou não existe se o `posts_list` ou um `estado.md` confirmar. Sem confirmação, escreva "sem confirmação".
- Não explique diferença de fuso nem especule sobre a causa de um número: só reporte o que o dado mostra.
- Máximo 25 linhas no arquivo.
- Cada pauta numa linha só.
- Conferir antes de entregar: sem travessão, sem número inventado, 3 pautas numeradas.
