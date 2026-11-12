# Reels de teste com a voz clonada (12/11/2026)

Status: PROPOSTA, aguarda GO do Jessé no piloto.

## Ideia do Jessé
Postar vários reels SEM ROSTO por dia (voz clonada F + formato didático) como Reel de Teste (só não seguidores, fora da grade). O que viralizar vira reel no perfil principal, gravado com rosto em outro formato. Todo teste tem CTA de palavra, entrega um material e puxa pro diagnóstico gratuito. Perfil principal segue normal (reel + carrossel).

## O que já temos (o guia em PDF fica quase todo dispensado)
- O guia manda criar app da Meta, token novo e túnel Cloudflare. O Zernio já publica Reel de Teste: `platformSpecificData.trialParams.graduationStrategy` = `MANUAL` ou `SS_PERFORMANCE`. Mesmo Publicador, sem app novo.
- Métricas: `scripts/meta_metricas.py` (token Meta de 60 dias) lê insights do reel; acrescentar `reels_skip_rate` e `ig_reels_avg_watch_time`. Regra de decisão do guia (pulo e % assistido contra a mediana do lote, vencedor com 72 h).
- Voz: receita F, cota grátis ~5 min de GPU por dia (compartilhada com TikTok Shop).
- Formato: didático sem rosto (skill didatico), Editor de Vídeo.

## Funil por teste
1. Comentário com a PALAVRA → automação do post (follow gate, botão "Já sigo, manda!") entrega o material.
2. Opcional: áudio de 20 a 30 s com a voz F na DM explicando o diagnóstico (Zernio aceita áudio por URL).
3. Workflow do Zernio: atraso de 60 min → "E aí, deu certo? Conseguiu abrir?" → espera resposta → avisa o Jessé.
4. Jessé responde à mão com diagnóstico, consultoria ou mentoria.
Limite da Meta: mensagem automática só dentro de 24 h da última ação da pessoa (o toque no botão conta). Fora disso, só resposta digitada por pessoa (HUMAN_AGENT, até 7 dias).

## Riscos
- Cota da voz: grátis dá ~1 a 3 reels/dia. 5 a 8/dia pede Hugging Face PRO (US$ 9/mês).
- Rótulo de IA: a Meta pede rótulo em áudio realista gerado por IA. O Zernio não tem o campo pra Instagram; marcar no app ou aceitar o risco (decisão do Jessé).
- Conteúdo repetido tem alcance limitado no teste: cada teste é vídeo novo.
- Limite de testes por dia da conta é desconhecido (erro 2207078): começar com 3/dia.

## Ordem
1. Piloto: 1 reel de teste + automação + workflow de 1 h (testado com 2 min) + aviso. Conferir no app que saiu como Teste e fora da grade.
2. Lote 1: 3/dia por 5 dias, 2 ou 3 temas, mudando só o gancho.
3. Leitura 24 h (gancho) e 72 h (vencedor). Vencedor: Jessé compartilha com todos no app e grava versão com rosto.
