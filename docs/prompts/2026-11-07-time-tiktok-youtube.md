# Prompts pra montar o time no TikTok e no YouTube (2026-11-07)

Cole o prompt na sessão de cada projeto. Os dois usam o time do Instagram como modelo e não apagam o que já funciona.

---

## Prompt 1 · Sessão do TikTok

```
Modo Prumo. Quero o time do TikTok no mesmo formato do time do Instagram, sem quebrar nada que já está rodando aqui.

MODELO (só leitura, não altere nada lá):
- /Users/dmelo/Documents/03-Marketing/fabrica-conteudo/docs/decisoes/2026-11-06-time-instagram.md
- /Users/dmelo/Documents/03-Marketing/fabrica-conteudo/CLAUDE.md (seções "Gerente de Marketing", "Time do Instagram", "Sequência do dia")
- /Users/dmelo/Documents/03-Marketing/fabrica-conteudo/.claude/agents/ (analista, copywriter, designer, editor-de-video, revisor, publicador)
- /Users/dmelo/Documents/03-Marketing/fabrica-conteudo/.claude/skills/relatorio-diario/SKILL.md
- /Users/dmelo/Documents/03-Marketing/fabrica-conteudo/scripts/relatorio_diario.sh e ~/Library/LaunchAgents/com.fusiongrowth.relatorio-conteudo.plist

FORMATO A COPIAR:
- Conversa principal = Gerente de TikTok (chefe do time). Organograma: Jessé (CEO) › Gerente › funções. Agentes sem nome próprio, só a função.
- Regra de modelo: quem pensa em Opus, quem executa script em Sonnet, quem publica em Haiku.
- Analista com 4 blocos: (1) todo dia: métricas, concorrentes, notícias e 3 pautas; (2) otimização: confere se as pautas que ele mesmo deu deram resultado e corrige a própria pesquisa, anotando em um arquivo de aprendizados; (3) radar de ferramentas na segunda; (4) confirma fatos com fonte.
- Relatório diário automático (skill + script + launchd) com: ontem, fila, métricas 7 dias, otimização, radar e 3 pautas. Manda no Telegram.
- Sequência do dia numerada, igual à do Instagram, adaptada ao TikTok.

ETAPA 1 · AUDITORIA (antes de propor qualquer coisa):
1. Liste o que já existe aqui: agentes, skills, scripts, launchd/cron, contas no Zernio, rotina diária de postagem, onde ficam as métricas.
2. Tabela "Instagram x TikTok": cada peça do modelo e se ela existe aqui (✅ igual, 🟡 existe mas fraca, 🔴 não existe).
3. Analista: puxe as métricas reais dos últimos 14 dias no Zernio (analytics do TikTok) e diga o que o Analista atual entrega, o que falta e o que melhorar. Ele mede por vídeo? Compara formato, produto e horário? Fecha o ciclo pauta › resultado › ajuste? Grava aprendizados?
4. Liste o que está ATIVO e não pode parar (postagem automática, agendados, automações). Isso fica intocado.

ETAPA 2 · ESPECIFICAÇÃO (sem código ainda):
- Divisão em subagentes pra executar, arquivos novos e alterados, decisões e alternativas descartadas com o motivo.
- Criar docs/decisoes/2026-11-07-time-tiktok.md antes de implementar.

ETAPA 3 · VERIFICAÇÃO DEFINIDA:
- Como vou provar: rodar o relatório manualmente uma vez e mostrar a saída real; checar que os agendados do Zernio continuam iguais (lista antes e depois); launchd carregado (launchctl list | grep ...).

REGRAS:
- Backup .bak-pre-time de todo arquivo antes de mexer. Nada é apagado; o que sair do time vai pra pasta bak.
- Não mexer nos posts agendados nem na rotina que já posta.
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
Leia docs/decisoes/2026-11-07-time-tiktok.md (pasta do TikTok) e /Users/dmelo/Documents/03-Marketing/Jesusepop/JesusEPop_producao/docs/decisoes/2026-11-07-time-youtube.md e diga o que o Analista de lá faz melhor que o daqui. Proponha a mudança no .claude/agents/analista.md com backup, sem aplicar.
```
