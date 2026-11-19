# Lote de teste: espera sem teto e copy no modelo novo

Data: 17/11/2026. GO do Jessé no chat ("GO, pode fazer").

## Contexto
- Lote das 23h de 16/11 (RESPOSTA, 3 ganchos) falhou: a sessão sem interface encerrou às 23h26 e derrubou o Editor, que rodava em segundo plano. O log registrou "Background tasks still running 10m after the last turn; stopping them". Nenhum vídeo chegou no Telegram.
- Em 16/11 o Jessé reprovou a copy de tutorial de clique e o áudio técnico. O molde aprovado é o do reel CAUSA: problema do dono em palavra simples, depois a saída.

## Decisão
1. `scripts/reels_teste.sh`: exporta `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0` antes da chamada do Claude. O limite de 5 h 30 continua sendo o teto.
2. Skill `lote-teste`, execução: todo agente roda em primeiro plano; proibido encerrar o turno com agente rodando ou gravar manifesto com motivo "em andamento".
3. Skill `lote-teste`, copy: ordem fixa nova.
   1. Problema do dia a dia do dono, em cena, palavra simples, sem sigla nem nome de método.
   2. Por que ele volta (o processo que falta).
   3. "Faz assim: abre o Claude e..." em 1 a 2 frases, sem narrar clique (o clique fica só na tela).
   4. "Primeiro o processo. Depois a IA."
   5. "Comenta PALAVRA que eu te mando o prompt pronto."
   Voz em tom de conversa, ritmo 1,10.
4. `pesquisa/fila-testes.md`: 6 pautas livres reescritas nesse molde, sem tocar nos fatos conferidos. Os blocos `resposta-ganchos` e `cotacao-ganchos` saem da fila porque o corpo deles é tutorial de clique. Os 3 vídeos de 17/11 ficam descartados.

## Alternativas descartadas
- Subir o teto de espera pra 60 min: um render longo quebra de novo.
- Só a regra na skill, sem a variável: depende do modelo obedecer.
- Consertar os vídeos g1 a g3 de 17/11: copy reprovada.

## Verificação
- `bash -n scripts/reels_teste.sh` sem saída.
- Sessão sem interface com agente em segundo plano de 11 min: arquivo de prova gravado e nenhuma linha "stopping them" no log.
- Fila: 0 travessão, 6 blocos `[ ]` completos, Revisor aprovado.
- Manifesto de 18/11 com 3 itens `pronto`.

## Risco conhecido
O molde novo ainda não tem número a favor: o CAUSA estava com 93,3% de pulo em 8 h. O lote de teste é onde isso se mede.

Backups: `.bak-pre-modelo-novo` dos 3 arquivos.
