# Fábrica de conteúdo (Claude Code)

Do link de referência até o post publicado, com um agente por função.

## Instalar (uma vez, no Mac)
Nesta pasta, rode `bash instalar.sh` (coloca os agentes e a skill em .claude/).
```
brew install python@3.12 ffmpeg yt-dlp
python3.12 -m venv .venv
.venv/bin/pip install --upgrade pip setuptools wheel
.venv/bin/pip install playwright pillow
(opcional) .venv/bin/python -m playwright install chromium   # só se não tiver o Google Chrome
```
Transcrição (opcional, leve): `brew install whisper-cpp` e baixe o modelo small (cerca de 470 MB) para `models/ggml-small.bin`.

No Claude Code, deixe os conectores do Zernio e do Notion disponíveis (os mesmos que você usa no claude.ai).

## Usar
Abra o Claude Code nesta pasta e mande a referência:
```
modele esse carrossel https://www.instagram.com/p/XXXX
```
Para outro cliente: `modele esse carrossel pro cliente padaria-x <link>`.

## Quem faz o quê
| Agente | Modelo | Função |
|---|---|---|
| orquestrador (a conversa) | Opus 5.5 (`/model opus`) | decide, conversa, aprova |
| pesquisador | Sonnet 5.5 | transcreve e checa fatos com fonte |
| copywriter | Sonnet 5.5 | análise da copy, slides e legenda |
| titulista | Sonnet 5.5 | 4 capas e prompt da imagem |
| designer | Sonnet 5.5 | gera os arquivos e confere |
| revisor | Sonnet 5.5 | controle de qualidade independente |
| publicador | Haiku | Zernio e Notion |

O modelo de cada agente fica na linha `model:` do arquivo em `.claude/agents/`. Conversa principal em Opus 5.5, publicador em Haiku, o resto em Sonnet 5.5. Para testar outro, troque ali (sonnet, opus, haiku).

## Novo cliente
1. Copie `clientes/_modelo` para `clientes/<nome>`.
2. Preencha `marca.json` (cores, @, IDs do Zernio e do Notion) e `voz.md`.
3. Coloque a foto ou logo em `fotos/`.
Os agentes e scripts não mudam.
