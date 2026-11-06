# Equipe autônoma de conteúdo no OpenBot (levantamento + plano)

Data: 2026-11-05 (quarta). Início previsto: 2026-11-06 (sexta).
Status: GO dado em 2026-11-06. Agentes sem nome próprio: só cargo (Gerente de Marketing, Analista de Social Media, Copywriter, Designer, Editor de Vídeo, Publicador).

## 1. O que o OpenBot é de verdade (lido no site, no repositório e na sua máquina)

- App desktop local, versão instalada 0.60.0, provider preferido Claude, logado na assinatura Claude (sem chave de API).
- Roda o Claude pelo Agent SDK, não pelo terminal. Instruções do agente ficam num `AGENTS.md` (ou `CLAUDE.md`) na raiz do workspace dele e entram como system prompt (limite 32 mil caracteres).
- Workspace de cada agente: `~/OpenBot/Agents/<id>/`. Pasta comum: `~/OpenBot/Shared/`. Banco compartilhado entre agentes (SQLite, ferramentas `openbot.query_data` e `execute_data`).
- Skills: pasta `SKILL.md` registrada na biblioteca local e instalada em `<workspace>/.claude/skills/`. Skills de usuário em `~/.claude/skills/` são visíveis pra TODO agente (settingSources inclui `user`). Ou seja: carrossel, editar-reels, fio, jogo, palco, bastidor, minimal, ganchos-jesse, diretor já estão disponíveis. O que NÃO está: skills de projeto da fábrica (`modelar-post`, `relatorio-diario`) e os 10 subagentes em `.claude/agents/`, porque só valem com o Claude rodando dentro da pasta da fábrica.
- MCP: o OpenBot usa `strictMcpConfig`. Os conectores do claude.ai (Zernio, Notion, Kling, Gmail) NÃO chegam aos agentes. Servidores MCP têm que ser cadastrados dentro do OpenBot (painel próprio ou `save_mcp_server` com aprovação). Zernio por REST com `ZERNIO_API_KEY` já funciona (`cerebro-jarvis/scripts/puxar-metricas.py`).
- Equipe = canal. Um agente é o lead e roteia; `@nome` no início da mensagem manda direto pro membro; membros respondem entre si (`channel_reply`), repassam (`channel_transfer`) e criam subtarefa (`channel_assign`). Fora de canal: `send_message`, `list_agents`.
- Limites que mandam no desenho: 2 tarefas paralelas por canal, 4 tarefas por agente, 8 atribuições automáticas por pedido. Equipe de 10 agentes no canal não escala; 5 ou 6 sim.
- Rotinas: "uma instrução e os horários". Pertencem a um agente, rodam no chat ou numa thread própria, podem passar o resultado pra outros agentes (routine flow). Não é agendador com retry. Precisa do Mac ligado e logado. Disparo externo por webhook assinado (HMAC) ou pelo servidor local de automação.
- Memória: ferramentas `remember`, `search_memories`, `forget_memory`, revisão automática a cada 20 turnos. Memória de canal separada.
- Segurança: os agentes rodam com acesso total e sem confirmação por ação (`danger-full-access`, `approvalPolicy: never`). O README diz com todas as letras que isso é decisão de produto, não barreira. O gate de publicação tem que estar na instrução e na ausência de credencial, não na esperança.
- Preço: uso pessoal R$ 0, sem recurso travado. Licença comercial só se virar serviço pra cliente (Starter €10/mês).
- App iOS/Android conecta no Mac: dá pra receber as pautas e responder "1" do celular.

## 2. O que você já tem na máquina (não recriar)

| Peça | Onde | Estado |
|---|---|---|
| OpenBot com 3 agentes | Assistente Pessoal, Agenda, E-mail (todos Haiku) | 0 rotinas, 0 memórias, 0 canais |
| Fábrica de conteúdo | `~/Documents/03-Marketing/fabrica-conteudo` | FabIA (orquestradora no Claude Code) + 10 subagentes + skills modelar-post e relatorio-diario, scripts render.py etc., cliente jesse-rodolfo (voz.md 121 linhas, marca.json) |
| Cérebro Jarvis (Hermes aposentado 21/10) | `~/Documents/03-Marketing/cerebro-jarvis` | skills pauta-matinal, radar-concorrentes, metricas-instagram, avaliador, registrar-feedback; contexto/ com subcrenças, histórias, provas, diagnóstico |
| Relatório diário 07:00 | launchd `com.fusiongrowth.relatorio-conteudo` | `claude -p` com Zernio via conector claude.ai, Telegram sem token |
| Métricas Zernio por REST | `cerebro-jarvis/scripts/puxar-metricas.py` | funciona com `ZERNIO_API_KEY` |
| Skills de vídeo (user level) | `~/.claude/skills/{editar-reels,fio,jogo,palco,bastidor,minimal,efeitos,broll,sala}` | visíveis pro OpenBot sem fazer nada |
| Voz | `~/.venvs/chatterbox` (clone local), testes F5 e XTTS de 16/10 em `tiktok-video-ia/entrada/avatar/voz/`, Kokoro rodando no painel Jarvis, chave ElevenLabs em `~/.jesusepop_elevenlabs` | nenhum integrado ao pipeline |
| Hardware | MacBook M1, 8 GB RAM, 22 GB livres, OpenBot já ocupa 1,1 GB | gargalo principal |

## 3. Decisões

1. Equipe de 6 agentes no OpenBot, não 10. Os 10 subagentes da fábrica viram 6 papéis fundidos (tabela abaixo). Motivo: limite de 2 tarefas paralelas por canal e 8 GB de RAM. Cada agente ativo é um processo Node + sessão do Claude.
2. Os agentes do OpenBot trabalham DENTRO da pasta da fábrica, não no workspace deles. O `AGENTS.md` de cada um manda: "todo arquivo em `/Users/dmelo/Documents/03-Marketing/fabrica-conteudo`, Python sempre `.venv/bin/python`". Assim ESTADO.md, posts/, clientes/ e scripts continuam a fonte da verdade e o Claude Code daqui segue enxergando tudo.
3. Skills da fábrica e do Jarvis (modelar-post, relatorio-diario, pauta-matinal, radar-concorrentes, metricas-instagram, avaliador) vão pra biblioteca de skills do OpenBot via `create_skill`, uma vez, e cada agente instala só as suas.
4. Modelos: Gerente de Marketing e Analista em Sonnet 5.5; Copywriter e Designer em Sonnet 5.5; Publicador em Haiku 5.5. Opus só se o Sonnet falhar em copy. Motivo: custo de assinatura e RAM. (Hoje a fábrica no Claude Code usa Opus pra FabIA e pesquisador.)
5. Publicação com gate duplo: o Publicador só age quando a mensagem no canal vier do Jessé com a palavra GO, e na fase 1 ele nem tem o MCP do Zernio. Ninguém publica sozinho até você mandar.
6. Rotina no OpenBot substitui o launchd do relatório, mas só depois de 3 execuções manuais boas. Até lá os dois coexistem; depois desliga o launchd (`launchctl unload`).
7. Voz e vídeo pesado não rodam no Mac enquanto a equipe estiver de pé. Chatterbox/F5/XTTS em torch CPU com 8 GB é o que trava a máquina. Decisão pendente (item 7 das pendências).
8. Os 3 agentes atuais (Pessoal, Agenda, E-mail) ficam fora do canal de conteúdo. Arquivar ou manter é sua escolha; não gastam nada parados.
9. Nada da equipe toca MelaVitta, n8n, CRM ou WhatsApp da operação. Vai escrito no `AGENTS.md` de todos.

## 4. A equipe (canal "Conteúdo")

| Agente OpenBot | Papel | Absorve da fábrica/Jarvis | Skills instaladas | Modelo |
|---|---|---|---|---|
| Gerente de Marketing (lead do canal) | Fala com você, roteia, revisa, guarda ESTADO.md | Gerente de Marketing + revisor | modelar-post, relatorio-diario, avaliador | Sonnet |
| Analista de Social Media | Métricas Zernio, radar de concorrentes, perfil e público, pauta do dia | pesquisador + metricas-instagram + radar-concorrentes + pauta-matinal | pauta-matinal, radar-concorrentes, metricas-instagram | Sonnet |
| Copywriter | Roteiro de carrossel e reel, capa, gancho, legenda, grupo.md | copywriter + titulista + roteirista | ganchos-jesse (já user level) | Sonnet |
| Designer | Gera os 1080x1350, capas, texto na tela | designer | carrossel (user level) + scripts da fábrica | Sonnet |
| Editor de Vídeo | Escolhe formato e roda a skill de edição com o bruto | editor-de-video + diretor-de-cena | editar-reels, fio, jogo, palco, bastidor, minimal, broll, efeitos (user level) | Sonnet (fase 2) |
| Publicador | Zernio, automação de palavra-chave, Notion, grupo.md | publicador | nenhuma (REST/MCP cadastrado no OpenBot) | Haiku (fase 2) |
| SDR (pré-vendas) | Responde comentário e direct com a PALAVRA, qualifica pro diagnóstico | novo | consultor-de-ofertas, diagnostico-reverso | fase 3 |

Fluxo de um dia (fase 1 estável):

```
06:30 rotina Analista  -> métricas 7d + radar -> tabela metricas_diarias e radar no banco compartilhado -> resumo no canal
07:00 rotina Gerente de Marketing     -> lê o resumo + ESTADO.md + cronograma -> 3 pautas no canal (e no app do celular)
você                   -> responde "1", "2" ou "3" (ou "1 em reel")
Gerente de Marketing                  -> @Copywriter roteiro + capa -> checkpoint com você -> @Designer Gráfico artes -> revisa com checklist -> mostra os arquivos
você                   -> "GO 18h"
Gerente de Marketing                  -> @Assistente de Social Media (fase 2) agenda, automação, Notion, devolve grupo.md -> atualiza ESTADO.md
```

Os rascunhos de `AGENTS.md` de cada agente estão em `openbot/agentes/*.md` nesta pasta. Amanhã é copiar pra raiz do workspace de cada um.

## 5. Como se cria (ordem de amanhã)

O OpenBot não tem arquivo de configuração de agente. Criar agente, canal e rotina é na interface. O que eu faço daqui: preparar os textos, copiar `AGENTS.md` pro workspace certo, registrar skills, conferir no banco. Se preferir, eu mesmo clico no OpenBot pelo computer-use, com você olhando.

### Dia 1 · sexta 06/11

Manhã (2 h):
1. Você cria no OpenBot os 4 agentes da fase 1 (Gerente de Marketing, Analista de Social Media, Copywriter, Designer) com uma linha de descrição cada e o modelo da tabela. Eu copio o `AGENTS.md` de `openbot/agentes/` pra `~/OpenBot/Agents/<id>/AGENTS.md`.
2. Você cria o canal "Conteúdo" com Gerente de Marketing como lead e os outros 3 como membros.
3. Registro das skills na biblioteca: peço ao Gerente de Marketing, no chat dela, "crie skill a partir da pasta X" apontando pras pastas da fábrica e do Jarvis (6 skills). Depois instalo em cada agente a que lhe cabe.
4. Teste 1 (sem publicar): no canal, "@Gerente de Marketing monta o carrossel VENDAS (6 de 6) seguindo o calendário". Esperado: Gerente de Marketing chama Copywriter e Designer, PNGs aparecem em `posts/2026-11-07-vendas/saida/`, Gerente de Marketing pede seu ok. Nada no Zernio.

Tarde (1 h 30):
5. `ZERNIO_API_KEY` disponível pro Analista (arquivo `.env` na fábrica, só leitura).
6. Teste 2: "@Analista métricas dos últimos 7 dias e radar dos perfis de referência". Esperado: tabela no banco compartilhado + resumo de até 15 linhas no canal.
7. Rotinas: Analista 06:30 todo dia; Gerente de Marketing 07:00 segunda a sábado. Executar as duas na mão uma vez.

### Dia 2 · sábado 07/11
8. Decisão Zernio/Notion pro Publicador (pendência 1) e criação do Publicador com gate GO.
9. Editor de Vídeo com um bruto que você já tem (reel LUCRO ou PASTAS): storyboard, escolha de formato, render. Medir RAM durante o render.

### Semana 2 (a partir de 10/11)
10. Voz (pendência 7) e SDR (pré-vendas) (pendência 4).
11. Desligar o launchd do relatório quando a rotina do OpenBot tiver 3 dias limpos.

## 6. Verificação (como provo que está certo)

| Teste | Comando ou ação | Saída esperada | Se falhar |
|---|---|---|---|
| Agente lê a fábrica | no chat do Gerente de Marketing: "leia ESTADO.md e me diga o próximo passo" | cita o carrossel QUALIDADE/VENDAS e o reel LUCRO | AGENTS.md não foi lido: conferir caminho e reiniciar a thread |
| Skills de usuário visíveis | "liste as skills que você tem" | aparecem carrossel, editar-reels, fio, jogo... | settingSources sem `user`: abrir issue, usar cópia em `.claude/skills` do workspace |
| Delegação funciona | "@Gerente de Marketing monta o carrossel VENDAS" | no canal aparecem turnos do Copywriter e do Designer, arquivos em `posts/` | lead não roteia: mensagem com `@Copywriter` direto |
| Nada publica sozinho | mesmo teste acima | `posts_list` do Zernio sem post novo (eu confiro daqui) | retirar acesso Zernio do agente que postou |
| Rotina roda | botão de executar rotina / esperar 07:00 | mensagem no canal e `saidas/relatorios/AAAA-MM-DD.md` novo | ver thread da rotina; se o Mac dormia, ajustar energia |
| RAM | `top -l 1 -s 0 | head -12` durante o teste 1 | memória livre acima de 1 GB, sem swap crescendo | reduzir agentes em paralelo a 1 no canal |

## 7. Pendências (você decide)

1. Publicação: (a) cadastrar MCP do Zernio dentro do OpenBot (preciso da URL do MCP e da chave; conferir se o Zernio oferece), (b) reescrever o publicador pra REST do Zernio com `ZERNIO_API_KEY` de escrita, (c) manter publicação no Claude Code daqui e o OpenBot só produz. Minha recomendação: (c) na fase 1, (b) na fase 2.
2. Notion (calendário): (a) MCP do Notion cadastrado no OpenBot com token de integração, (b) o Publicador só entrega e eu registro daqui. Recomendo (b) até a fase 2.
3. Telegram do relatório: (a) abandonar, o app do OpenBot no celular já notifica, (b) manter e preencher o `.env`. Recomendo (a).
4. SDR (pré-vendas): Zernio tem inbox de comentários e menções (`comments_reply_to_inbox_post`, `mentions_reply_to_mention`), mas não direct. Pra direct: (a) só comentários via Zernio, (b) ManyChat/automação do Zernio já existente, (c) Instagram no navegador embutido do OpenBot (frágil, risco de bloqueio). Recomendo (a) + (b).
5. Agentes antigos Pessoal/Agenda/E-mail: (a) arquivar, (b) manter fora do canal.
6. Modelo do Gerente de Marketing: (a) Sonnet (recomendo), (b) Opus como hoje.
7. Voz clonada: (a) ElevenLabs API com a chave que já existe (custo por caractere, qualidade alta, zero RAM), (b) Chatterbox/F5 na VPS Hostinger (grátis, precisa conferir CPU/RAM da VPS), (c) adiar e seguir com você narrando. Recomendo (a) pra começar e (b) se o volume subir.
8. Commit deste plano e dos rascunhos na fábrica: (a) commit agora, (b) depois do GO.

## 8. Riscos

- 8 GB de RAM. Dois agentes trabalhando + OpenBot + navegador embutido já chega perto do limite. Render de vídeo com Chrome headless e TTS local são proibidos enquanto o canal estiver ativo.
- Acesso total sem confirmação. Qualquer instrução ambígua vira ação. Por isso o gate GO e a ausência de credencial de publicação na fase 1.
- Rotina depende do Mac acordado às 06:30. Configurar energia pra não dormir ou aceitar que roda ao acordar.
- Dois pipelines em paralelo (launchd + OpenBot) por alguns dias: podem gerar relatório duplicado. Aceitável até desligar o launchd.
- Licença: uso pessoal R$ 0. Se a fábrica virar serviço cobrado de cliente (clientes/_modelo), entra licença Starter €10/mês.

## 9. Arquitetura do cérebro e das skills (decidido 2026-11-06)

Decisão: híbrido com um cérebro só. OpenBot é a frente (rotinas, canal, celular, demonstração). Claude Code é a oficina (criar skill, consertar script, publicar com conector). Os dois leem a mesma pasta da fábrica.

Camadas do cérebro, da mais confiável pra menos:
1. Identidade e fatos: `clientes/<cliente>/voz.md`, `marca.json`, `cerebro-jarvis/contexto/` (subcrenças, histórias, provas, ângulos queimados). Em git. Vence tudo.
2. Procedimentos: skills (SKILL.md) e instruções de papel (AGENTS.md). Em git.
3. Estado do dia: `ESTADO.md`, `cronograma.md`, `posts/*/estado.md`, tabelas do banco compartilhado do OpenBot. Os agentes mantêm.
4. Memória automática do OpenBot (`remember`, revisão a cada 20 turnos): só aprendizado entre rotinas. Nunca fonte de verdade. Se contradisser o contexto, o contexto vence.

Skills por uso (inventário: 55 de usuário + 39 sincronizadas + 155 agentes de plugin):
- Pipeline diário (instaladas nos agentes): modelar-post, relatorio-diario, carrossel, ganchos-jesse, pauta-matinal, radar-concorrentes, metricas-instagram, avaliador, registrar-feedback.
- Vídeo (só no Editor de Vídeo): editar-reels, fio, jogo, palco, bastidor, minimal, didatico, efeitos, broll, sala, diretor.
- Conselhos de plugin (copy-master, hormozi, storytelling, brand-squad, advisory-board, traffic-masters): só no Claude Code, um por vez, pra decisão pontual. Resultado vira regra em `contexto/`. Nunca instalados em agente do OpenBot.
- Operação (fim-de-sessao, check-painel, orq-tech, graphify, melavitta-brain, morning): só no Claude Code.
- Fora do conteúdo (replica-*, cybersecurity, vercel, finance, founderos): em nenhum agente.

Regra: agente com mais de 5 skills vira genérico. Skill é procedimento com verificação. Agente é papel. Contexto é fato. Rotina é horário.

Replicação pra empresário: modelo de 4 pastas (Contexto, Procedimentos, Papéis, Rotinas) a partir de `clientes/_modelo`. Quando virar produto, a frente migra do OpenBot pra n8n na VPS com API do Claude, pra não depender do Mac.

## 10. Execução da fase 1 (2026-11-06, 10:41 a 10:47)

Criados no OpenBot 0.60.0 (interface, via computer-use em segundo plano):

| Agente | ID | Modelo |
|---|---|---|
| Gerente de Marketing (lead) | agent-739d4308-9533-4f6f-9de9-8ede937e00fe | claude-sonnet-5, médio |
| Analista de Social Media | agent-8b3658f1-3fb6-4876-aa04-3d48624b97ee | claude-sonnet-5, alto |
| Copywriter | agent-be6c0251-c46f-466d-80c6-714afb66bfb4 | claude-sonnet-5, alto |
| Designer Gráfico | agent-bec70be8-e093-4e4a-888f-880f2b27d1e4 | claude-sonnet-5, alto |

Canal "Conteúdo": d34a3652-3ea4-4713-bafa-4af8e78014d4, lead Gerente de Marketing, instruções do canal com as regras (GO, pasta, 2 em paralelo, fora de escopo).

AGENTS.md e skills instalados por `openbot/instalar-agente.sh <cargo> <id>` (idempotente). Rodar de novo após editar um rascunho em `openbot/agentes/`.

Aprendizados da interface:
- O CLI 2.1.317 só lista Claude Sonnet 5 (não 5.5). Usado Sonnet 5.
- No formulário de novo agente, Return dentro da busca de modelo cria o agente. Selecionar o modelo clicando no círculo da opção.
- O primeiro membro marcado vira lead do canal; trocar depois nas configurações do canal (coroa).
- Texto colado na caixa do canal por acessibilidade não ativa o botão Enviar; precisa de uma tecla real (espaço) e Enter.
- Memória antes de começar: 1,2 GB livre e 4,4 GB de swap. A máquina já estava apertada antes do OpenBot.
