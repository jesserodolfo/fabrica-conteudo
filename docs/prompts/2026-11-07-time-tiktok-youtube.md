# Prompts pra montar o time no TikTok e no YouTube (2026-11-07)

Cole o prompt na sessão de cada projeto. Os dois usam o time do Instagram como modelo e não apagam o que já funciona.

---

## Prompt 1 · Sessão do TikTok (pasta /Users/dmelo/Documents/03-Marketing/tiktok-video-ia)

```
Modo Prumo. Quero o time do TikTok no mesmo formato do time do Instagram da fábrica de conteúdo, sem quebrar nada que já roda aqui.

MODELO (só leitura, não altere nada lá):
- /Users/dmelo/Documents/03-Marketing/fabrica-conteudo/docs/decisoes/2026-11-06-time-instagram.md
- /Users/dmelo/Documents/03-Marketing/fabrica-conteudo/CLAUDE.md (seções "Gerente de Marketing", "Time do Instagram", "Sequência do dia")
- /Users/dmelo/Documents/03-Marketing/fabrica-conteudo/.claude/agents/ (analista, copywriter, designer, editor-de-video, revisor, publicador)
- /Users/dmelo/Documents/03-Marketing/fabrica-conteudo/.claude/skills/relatorio-diario/SKILL.md
- /Users/dmelo/Documents/03-Marketing/fabrica-conteudo/scripts/relatorio_diario.sh

O QUE JÁ EXISTE AQUI E FICA (não recriar):
- As 9 regras e o pipeline do CLAUDE.md desta pasta: molde de 26 a 29 s, /prompt-flow, /flow, /validar, /partitura, /video, limite de 3 clipes e 30 créditos por clipe, zero ferramenta paga.
- Postagem automática com aprovação no Telegram (docs/decisoes/2026-10-18-postagem-automatica.md) e as rotinas launchd com.jesseia.aprovar, com.jesseia.limpar e com.jesseia.vigia. Confira o que cada uma faz antes de propor qualquer coisa.
- Posts agendados no Zernio.
- saida/fila.csv como base das métricas (views 48 h, cliques na bio, vendas).
- Projetos irmãos (../my-video, ../cortes, ../flow-queue): reaproveitar, não duplicar.

FORMATO A COPIAR, ADAPTADO AO TIKTOK:
- Conversa principal = Gerente de TikTok. Organograma: Jessé (CEO) › Gerente › funções. Agentes sem nome próprio, só a função.
- Regra de modelo: quem pensa em Opus, quem executa script em Sonnet, quem publica em Haiku.
- Funções mapeadas no pipeline que já existe: Analista (métricas, trends, produtos e prompts da biblioteca), Copywriter (prompt em inglês, legenda e comentario.txt), Editor de Vídeo (/flow, /partitura, /video), Revisor (/validar e checklist), Publicador (Zernio, só depois do ok no Telegram). Cada função diz quais comandos usa.
- Analista com 4 blocos: (1) todo dia: métricas, concorrentes (Pereira, Kairo, Airon IA, Diego Kamhaji, só leitura), trends e 3 pautas (produto + formato + partitura); (2) otimização: confere se as pautas que ele mesmo deu deram resultado (views 48 h, cliques na bio, vendas por formato, produto, partitura e horário) e corrige a própria pesquisa, gravando em um arquivo de aprendizados; (3) radar na segunda; (4) confirma fatos com fonte.
- Relatório diário: ver se o vigia já faz parte disso. Se fizer, melhorar o vigia em vez de criar rotina nova. Se não fizer, propor o relatório no Telegram fora das 07:00 (horário do relatório do Instagram).

ETAPA 1 · AUDITORIA (antes de propor qualquer coisa):
1. Liste agentes, skills, comandos, scripts e rotinas launchd daqui e o que cada um faz hoje.
2. Tabela "Instagram x TikTok": cada peça do modelo e o estado aqui (✅ igual, 🟡 existe mas fraca, 🔴 não existe).
3. Analista e métricas: o saida/fila.csv está preenchido? Quem preenche views 48 h, cliques e vendas: à mão ou de forma automática? Puxe os últimos 14 dias do Zernio (analytics do TikTok), compare com a fila e diga o que falta pra fechar o ciclo pauta › resultado › ajuste sem depender do Jessé.
4. Liste o que está ATIVO e não pode parar.

ETAPA 2 · ESPECIFICAÇÃO (sem código ainda):
- Divisão em subagentes, arquivos novos e alterados, decisões e alternativas descartadas com o motivo.
- Criar docs/decisoes/2026-11-07-time-tiktok.md antes de implementar.

ETAPA 3 · VERIFICAÇÃO DEFINIDA:
- Rodar o relatório (ou o vigia melhorado) manualmente uma vez e mostrar a saída real; agendados do Zernio iguais antes e depois; launchctl list mostra as rotinas com.jesseia.* e as novas carregadas.

REGRAS:
- Backup .bak-pre-time de todo arquivo antes de mexer. Nada é apagado.
- Não gastar crédito do Flow nesta tarefa.
- Português, sem travessão, report técnico curto.
- Pare depois das etapas 1, 2 e 3 e espere meu GO.
```

---

## Prompt 2 · Sessão do YouTube (pasta /Users/dmelo/Documents/03-Marketing/Jesusepop)

```
Siga as 3 regras do CLAUDE.md desta pasta. Quero o time do YouTube dos canais Jesus é Pop (PT) e Jesús es Pop (ES) no mesmo formato do time do Instagram da fábrica de conteúdo, mantendo tudo que já está ativo aqui.

MODELO (só leitura, não altere nada lá):
- /Users/dmelo/Documents/03-Marketing/fabrica-conteudo/docs/decisoes/2026-11-06-time-instagram.md
- /Users/dmelo/Documents/03-Marketing/fabrica-conteudo/CLAUDE.md (seções "Gerente de Marketing", "Time do Instagram", "Sequência do dia")
- /Users/dmelo/Documents/03-Marketing/fabrica-conteudo/.claude/agents/ (analista, copywriter, designer, editor-de-video, revisor, publicador)
- /Users/dmelo/Documents/03-Marketing/fabrica-conteudo/.claude/skills/relatorio-diario/SKILL.md
- /Users/dmelo/Documents/03-Marketing/fabrica-conteudo/scripts/relatorio_diario.sh
A voz e a marca são as do Jesus é Pop, não as do @jesse.rodolfo. Não copie voz.md nem marca.json da fábrica.

O QUE JÁ EXISTE AQUI E FICA (não recriar):
- Rotinas launchd: coleta 06:00, oração 11:30, verificação 20:45, sábado 06:30.
- Skills yt-audit, yt-chapters, yt-comment, yt-edit, yt-package, yt-plan, yt-retention, yt-script, yt-seo, yt-shorts, yt-viral. O time chama essas skills, não escreve outras iguais.

FORMATO A COPIAR, ADAPTADO AO YOUTUBE:
- Conversa principal = Gerente de YouTube. Organograma: Jessé (CEO) › Gerente › funções. Agentes sem nome próprio.
- Regra de modelo: quem pensa em Opus, quem executa script em Sonnet, quem publica em Haiku.
- Funções: Analista, Copywriter (título, roteiro longo e Shorts, descrição, capítulos), Designer (thumbnail), Editor de Vídeo (longo e Shorts), Revisor, Publicador. Cada uma diz quais skills yt-* usa.
- Analista com 4 blocos: (1) todo dia: métricas dos 2 canais, concorrentes, notícias e 3 pautas; (2) otimização: confere se as pautas que ele deu deram resultado (views, retenção, CTR da thumbnail, inscritos ganhos, PT x ES) e corrige a própria pesquisa, gravando em um arquivo de aprendizados; (3) radar na segunda; (4) confirma fatos e versículos com fonte.
- Relatório diário: ver se a coleta das 06:00 já faz isso. Se fizer, melhorar a coleta em vez de criar rotina nova. Se não fizer, propor relatório depois da coleta, fora das 07:00 (horário do relatório do Instagram).

ETAPA 1 · AUDITORIA (antes de propor qualquer coisa):
1. Liste agentes, skills, scripts e rotinas launchd daqui e o que cada rotina faz hoje.
2. Tabela "Instagram x YouTube": cada peça do modelo e o estado aqui (✅ igual, 🟡 existe mas fraca, 🔴 não existe).
3. Analista: puxe as métricas reais dos últimos 14 dias dos 2 canais (Zernio ou a fonte que a coleta usa) e diga o que a análise atual entrega, o que falta e o que melhorar. Fecha o ciclo pauta › resultado › ajuste? Grava aprendizados? Se faltar dado (retenção, CTR), diga de onde dá pra puxar.
4. Liste o que está ATIVO e não pode parar.

ETAPA 2 · ESPECIFICAÇÃO (sem código ainda):
- Divisão em subagentes, arquivos novos e alterados, decisões e alternativas descartadas com o motivo.
- Criar JesusEPop_producao/docs/decisoes/2026-11-07-time-youtube.md antes de implementar.

ETAPA 3 · VERIFICAÇÃO DEFINIDA:
- Rodar o relatório (ou a coleta melhorada) manualmente uma vez e mostrar a saída real; vídeos agendados iguais antes e depois; launchctl list mostra as rotinas antigas e as novas carregadas.

REGRAS:
- Backup .bak-pre-time de todo arquivo antes de mexer. Nada é apagado.
- Não ler nem mostrar credenciais (~/.jesusepop_*, ~/.hermes/profiles/jarvis/.env).
- Nunca postar no @jesse.rodolfo pelo Zernio.
- Português, sem travessão, report técnico curto.
- Pare depois das etapas 1, 2 e 3 e espere meu GO.
```

---

## Depois dos dois

Quando os dois times estiverem rodando, rode este na sessão do Instagram pra puxar de volta o que der certo:

```
Leia /Users/dmelo/Documents/03-Marketing/tiktok-video-ia/docs/decisoes/2026-11-07-time-tiktok.md e /Users/dmelo/Documents/03-Marketing/Jesusepop/JesusEPop_producao/docs/decisoes/2026-11-07-time-youtube.md e diga o que o Analista de lá faz melhor que o daqui. Proponha a mudança no .claude/agents/analista.md com backup, sem aplicar.
```
