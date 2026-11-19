# Content Factory: a team of AI agents that makes my Instagram posts

Content Factory turns a reference (an Instagram post, a reel or a news link) into a finished post in my own voice and brand, and publishes it. It runs inside Claude Code on my Mac, with one agent per job, the same way a small marketing team works.

I use it every day for my personal Instagram (carousels, reels, stories) and I approve each post on Telegram before it goes out.

## How it works

1. **Analyst** finds ideas, transcribes the reference and checks every fact with a source.
2. **Copywriter** writes the slides or the reel script, four cover options and the caption.
3. **Designer** renders the 1080x1350 images with the Python scripts in `scripts/`.
4. **Video editor** cuts and assembles reels; **scene director** writes AI video prompts.
5. **Reviewer** checks everything without having written any of it.
6. **Publisher** uploads to the scheduler (Zernio), posts or schedules, and logs it in Notion.

A daily report skill reads the metrics, and a test-batch skill runs small reel experiments and keeps the winners.

## Project structure

- `.claude/agents/`: one Markdown file per agent (role, model, rules)
- `.claude/skills/`: `modelar-post` (the main pipeline), `relatorio-diario` (daily report), `lote-teste` (test batches)
- `scripts/`: renderers for covers and slides (Pillow, Playwright), video slides (ffmpeg), uploads, Telegram approval bot, voice and metrics helpers
- `openbot/`: the same team set up as autonomous agents
- `nuvem/`: a portable version to run in the cloud
- `clientes/_modelo/`: brand template (`marca.json` + `voz.md`) that each brand fills in
- `docs/decisoes/`: short records of every design decision

## Built with

Claude Code (agents and skills), Python 3.12 (Pillow, Playwright), Node.js, ffmpeg, yt-dlp, whisper.cpp for transcription, the Zernio API for publishing, Notion for the content calendar, and a Telegram bot for approvals.

## How to run

```bash
brew install python@3.12 ffmpeg yt-dlp
python3.12 -m venv .venv
.venv/bin/pip install playwright pillow
bash instalar.sh                 # installs the agents and skills into .claude/
cp .env.example .env             # fill in your own keys
```

Then copy `clientes/_modelo` to `clientes/<your-brand>`, fill in `marca.json` and `voz.md`, open Claude Code in this folder and send a reference: `modele esse carrossel <link>`.

Full instructions in Portuguese: [README.pt-BR.md](README.pt-BR.md).

## Status

Active personal project. Planned work is in [ROADMAP.md](ROADMAP.md).

## License

MIT, see [LICENSE](LICENSE).
