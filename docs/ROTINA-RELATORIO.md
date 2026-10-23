# Rotina do relatório diário (07:00)

Manda no Telegram: o que saiu ontem, a fila de hoje, métricas de 7 dias do Instagram (Zernio) e 3 pautas. Nada publica sozinho.

- Testar na mão: `bash scripts/relatorio_diario.sh` (leva 1 a 3 min). Gera `saidas/relatorios/AAAA-MM-DD.md`.
- Rodar de novo no mesmo dia sobrescreve o relatório. Rode na mão várias vezes antes de ligar o automático.
- Ligar o launchd (só quando estiver satisfeito): `launchctl load ~/Library/LaunchAgents/com.fusiongrowth.relatorio-conteudo.plist`
- Desligar: `launchctl unload ~/Library/LaunchAgents/com.fusiongrowth.relatorio-conteudo.plist`
- Rodar já pelo launchd (depois de carregar): `launchctl start com.fusiongrowth.relatorio-conteudo`
- Logs: `saidas/relatorios/log-AAAA-MM-DD.txt` (saída do Claude) e `~/Library/Logs/fusiongrowth/relatorio-conteudo-launchd.log` (launchd).
- Telegram: copie `.env.example` para `.env` e preencha `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID`. Sem isso, o script pula o envio e mostra notificação no macOS.
- Falta: token e chat do Telegram na pasta da fábrica. O bot do tiktok-video-ia já existe, dá pra reaproveitar o mesmo.
- O Mac precisa estar ligado e logado às 07:00. Se estiver dormindo, o launchd roda ao acordar.
- O Claude roda com `--permission-mode dontAsk` e só as ferramentas liberadas no script: ler arquivos, escrever em `saidas/relatorios/` e 3 leituras do Zernio.
- Para mudar o conteúdo do relatório, edite `.claude/skills/relatorio-diario/SKILL.md`.
