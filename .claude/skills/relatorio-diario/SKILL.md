---
name: relatorio-diario
description: Relatório diário do Analista do time do Instagram (métricas, otimização, radar e 3 pautas). Use quando o Jessé pedir "relatório do dia", "como foi ontem", "o que postar hoje" ou quando rodar pela rotina das 07:00
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
2b. Status no Notion. Para cada post do Instagram que o Zernio mostra como publicado ontem ou hoje, ache a linha no calendário do Notion (`notion.calendario_data_source` do `marca.json`) pela palavra-chave ou pela data e horário. Se o status estiver "Agendado", mude para "Publicado". Não mexa em mais nada da linha, não crie nem apague linha. Se a ferramenta do Notion falhar ou a linha não aparecer, anote "Notion: marcar Publicado à mão: <post>" em Ontem e siga.
2c. Limpeza do disco (decisão docs/decisoes/2026-11-12-limpeza-videos-postados.md). Para cada pasta `posts/*/` com `zernio.txt` e sem `limpeza.md`, rode `.venv/bin/python scripts/limpar_post.py posts/<pasta> --apagar`. O script só apaga se o Zernio disser publicado; se recusar, deixe quieto (sai depois). Some os MB apagados e escreva em Ontem: "Limpeza: N MB liberados (pastas)". Nunca use `--sem-zernio` aqui.
3. Otimização. Com `analytics_get_analytics` (Zernio, só leitura), pegue os posts do Instagram dos últimos 14 dias e compare cada um com a média da conta em salvamentos, compartilhamentos, comentários e alcance. Leia `pesquisa/analista-aprendizados.md` e acrescente uma linha por post novo (data · pauta · formato · acima, na média ou abaixo · o que muda). Não repita post já anotado. Sem dado, "sem dado".
4. Radar. Faça até 2 buscas na web por notícias das últimas 48 h sobre Claude, IA e automação pra dono de pequeno negócio. Traga no máximo 2, cada uma com link. Nada relevante: "sem notícia relevante". Concorrentes ficam pro radar de segunda.
5. Pautas. Leia `/Users/dmelo/Documents/03-Marketing/fusion-marketing/contexto/subcrencas.md`, `historias.md` e `diagnostico.md`. Escolha 3 pautas de hoje:
   - cada uma com uma subcrença e uma história real que a sustente (sem história, descarte);
   - nenhuma nos ângulos queimados do `diagnostico.md`, a menos que traga ângulo, história ou conclusão nova (diga qual);
   - não repita tema já publicado ou na fila (cronograma e estados);
   - se hoje tem slot vazio no cronograma (carrossel 10h ou reel 18h), priorize pautas para ele;
   - número só se estiver em `provas.md` na mesma pasta. Na dúvida, sem número.
   - use os aprendizados: tipo de pauta que ficou abaixo 2 vezes seguidas sai até ter ângulo novo.
6. Escreva `saidas/relatorios/AAAA-MM-DD.md` (sobrescreve se existir), no máximo 32 linhas, neste formato fixo:

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

## Otimização
- o que funcionou e o que muda (até 3 linhas), ou "sem dado"

## Radar
- notícia com link (até 2), ou "sem notícia relevante"

## 3 pautas pra hoje
1. formato · gancho de até 12 palavras · história que sustenta
2. ...
3. ...

Responda 1, 2 ou 3 pra eu produzir
```

7. Imprima o relatório inteiro na saída, igual ao arquivo, sem texto antes nem depois. A última linha é sempre "Responda 1, 2 ou 3 pra eu produzir".

## Regras
- Só diga que algo não saiu ou não existe se o `posts_list` ou um `estado.md` confirmar. Sem confirmação, escreva "sem confirmação".
- Não explique diferença de fuso nem especule sobre a causa de um número: só reporte o que o dado mostra.
- Máximo 32 linhas no arquivo.
- Cada pauta numa linha só.
- Conferir antes de entregar: sem travessão, sem número inventado, 3 pautas numeradas.
