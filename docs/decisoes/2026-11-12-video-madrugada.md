# Rotina das 23h: 3 reels de teste por dia com a voz clonada (12/11/2026)

## Decisão do Jessé (12/11, 20h)
- Todo dia às 23h00 a rotina começa (o limite de uso renova às 22h20) e pode rodar a madrugada inteira.
- Ela produz 3 reels SEM ROSTO no padrão DIDÁTICO régua Igão (`docs/decisoes/2026-11-12-regua-igao.md`), com a voz clonada F, modelando os vídeos mais viralizados.
- Cada vídeo pronto chega no Telegram do Jessé. De manhã ele aprova e dá o GO.
- Com o GO, o Publicador agenda os aprovados no mesmo dia como Reel de teste (só não seguidores), com automação por palavra.
- Um vídeo do lote é escolhido pra ir também ao perfil principal.
- Complementa `docs/decisoes/2026-11-12-reels-de-teste.md` (funil, métricas, riscos), que deixa de ser proposta.

## Como roda
- `scripts/reels_teste.sh` (launchd `com.fusiongrowth.reels-teste`, 23h00) chama o Claude Code sem interface com a skill `lote-teste`.
- Pauta: a rotina NÃO pesquisa na internet de madrugada. Ela pega as 3 primeiras pautas de `pesquisa/fila-testes.md`, que o Analista abastece de dia (relatório das 7h e pedidos do Jessé) com fato já conferido e referência viral.
- Por vídeo: Copywriter (fala, legenda, DM, palavra) → voz clonada → Editor de Vídeo em Fable 5.2 (didatico, `"regua": "igao"`) → `regua.py` APROVADO → Revisor → capa → Telegram.
- Um vídeo por vez (Mac de 8 GB). Reprovou 2 vezes na régua ou no Revisor: não vai pro Telegram como pronto, vai como aviso com o motivo.
- Nada é publicado de madrugada. Publicar depende do GO do Jessé.

## Aprovação
- v1: os vídeos chegam no Telegram numerados; o Jessé responde o GO na conversa do Claude ("GO 1 2 3" ou "GO 1 e 3, 2 refaz") e o Gerente passa pro Publicador.
- Motivo: já existe um ouvinte de Telegram do projeto TikTok (`com.jesseia.aprovar`); um segundo ouvinte no mesmo bot conflita. Botão de aprovar direto no Telegram fica pra v2.
- Horários dos testes aprovados: 12h, 16h e 20h, salvo outra ordem do Jessé.

## Descartado
- Pesquisar viral de madrugada sem ninguém olhando: abre a rotina pra conteúdo de terceiros com acesso ao terminal. A pesquisa fica de dia.
- Publicar sozinho sem GO: contraria a regra de aprovação da arte final.
- Rodar na VPS: sem placa de vídeo e sem o kit.

## Riscos
- Cota da voz (dividida com o TikTok Shop): se acabar, a rotina entrega os que deu e avisa.
- Mac precisa estar acordado às 23h: `sudo pmset repeat wakeorpoweron MTWRFSU 22:55:00` (o Jessé roda uma vez) e o script usa `caffeinate`.
- Conteúdo repetido: o Zernio recusa a mesma legenda em 24 h na mesma conta; vídeo que for pro perfil sai com mais de 24 h de distância do teste.
- Rótulo de IA da Meta: marcar no app.

## Verificação
Ensaio em 12/11: envio de vídeo de teste no Telegram, checagem de sintaxe, `launchctl list` mostrando o serviço e 1 rodada real na noite de 12/11 conferida no dia seguinte (quantos chegaram, régua de cada um, motivo dos que falharam).

## Adendo 12/11, 20h25: aprovação por botão e fluxo teste > perfil (pedido do Jessé)
- Bot próprio `@meuinstagramjesse_bot` (não é o do TikTok), então dá pra ter ouvinte sem conflito. A v1 "GO na conversa do Claude" continua valendo como reserva.
- Cada vídeo chega no Telegram com 2 botões: **Aprovado** e **Ajuste**.
  - Aprovado: o Publicador agenda como Reel de teste no próximo horário livre do dia (11h, 14h, 17h) com automação da palavra e registro no Notion, e o bot responde com o horário.
  - Ajuste: o bot pergunta o que ajustar; a resposta em texto do Jessé vira o pedido pro Editor, que conserta, passa na régua e reenvia o vídeo com os botões de novo.
- Só o chat do Jessé (`TELEGRAM_CHAT_ID`) é aceito. Mensagem de qualquer outro chat é ignorada.
- Os 3 do dia saem SEMPRE como teste. No dia seguinte, o melhor teste de ontem (mais visualizações em `scripts/meta_metricas.py`) vai pro perfil principal às 18h, com LinkedIn junto. O bot manda de manhã "melhor de ontem: X" com botões **Postar 18h** e **Escolher outro**.
- Horários dos testes mudam de 12h, 16h, 20h pra 11h, 14h, 17h: o Zernio recusa a mesma legenda em menos de 24 h na mesma conta, e assim o perfil às 18h do dia seguinte sempre passa.
- Os que mais viralizarem no perfil viram outros formatos (com rosto), decisão caso a caso com o Jessé.
- Descartado: publicar no perfil sem toque nenhum (fica 1 toque, por ser a grade principal).

## Adendo 12/11, 22h30: testa gancho, não tema (GO do Jessé, regra do guia)
- A partir da rotina de 13/11 (vídeos de 14/11), cada noite produz 1 TEMA com 3 GANCHOS diferentes: o corpo do vídeo é o mesmo, mudam só os 3 primeiros segundos (fala e cena de abertura) e a primeira linha da legenda.
- A noite de 12/11 roda como já estava: 3 temas (ATRASO, RESPOSTA, COTACAO), 1 gancho cada. Esses 3 vídeos viram o corpo das noites seguintes: 13/11 ATRASO com 3 ganchos novos, 14/11 RESPOSTA, 15/11 COTACAO.
- Motivo: comparar ganchos no mesmo dia e contra a mediana do próprio lote, como manda o guia. De quebra gasta menos voz (só o bloco do gancho é novo) e menos render.
- Na fila, o bloco de ganchos tem os campos `Corpo de:` e `Ganchos:` e vale sozinho pelo lote da noite. Bloco sem esses campos segue no modo antigo.
- A legenda de cada variação começa diferente (o Zernio recusa legenda idêntica em 24 h). A PALAVRA e a entrega na DM são as mesmas nas 3.

## Adendo 13/11/2026 11h45: limite do Fable
- Decisão do Jessé: se o Fable 5.2 bater o limite de uso, a rotina troca sozinha pro Opus 5.5 e continua de onde parou (a skill lote-teste não refaz vídeo com status pronto).
- Como: `scripts/claude_com_reserva.sh`, usado por `reels_teste.sh` e `ajustar_teste.sh`. Só troca com a mensagem de limite na saída da própria chamada; erro comum e tempo estourado não trocam. O Telegram avisa quando trocou.
- Descartado: parar e avisar (perde a noite, como em 13/11 00h04).
