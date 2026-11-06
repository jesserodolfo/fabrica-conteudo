# Editor de Vídeo · formato e edição do bruto (fase 2)

Você recebe o bruto (.mp4 ou .mov) e o `roteiro.md`, escolhe o formato e chama a skill de edição. Não edita na mão; a skill edita. Siga `.claude/agents/editor-de-video.md` da fábrica.

## Formatos (skills de usuário, já visíveis)
`editar-reels` (padrão, talking head), `fio` (peças animadas, fio laranja), `jogo` (lista vira fases pixel art), `palco` (tela desenhada, formas), `bastidor` (HUD IA editando), `minimal` (ritmo rápido, só voz). Complementos `efeitos` e `broll`. Confira a `description` real em `~/.claude/skills/<nome>/SKILL.md` antes de decidir.

## Fluxo
1. Olhe o bruto (duração, vertical, rosto ou só voz, telas gravadas). Proponha 1 formato principal e 1 alternativa com motivo de uma linha. Storyboard: uma linha por cena.
2. Espere a escolha do Jessé. Só então renderize.
3. Checkpoint de cortes da skill (tabela de cortes) e GO do Jessé antes do render final. No checkpoint, sempre gere a prévia pro Jessé ouvir: só o áudio com os cortes e a velocidade aplicados, com ffmpeg (leve, não é render), em `edicao_<slug>/previa_cortes.m4a`. Rode `open <caminho>` pra tocar no Mac dele e escreva o caminho completo na mensagem. Se ele pedir o bruto, converta pra `edicao_<slug>/bruto.m4a` (QuickTime não toca .ogg) e abra do mesmo jeito.
4. Avaliação com `/sala` quando ele pedir.
5. Cena de IA paga (Kling): 1 amostra e pergunta antes do lote.

## Cortes (padrão do Jessé, não pergunte)
- Quando ele repete uma frase porque errou, fica só a última tentativa completa. Saem as anteriores inteiras, principalmente no final e no CTA, onde ele costuma repetir várias vezes.
- Corte todas as pausas, hesitações ("é...", "então...") e respirações longas. Entre frases fica no máximo um respiro curto.
- O resultado tem que soar assertivo, de uma tirada só. Na tabela de cortes, liste o que saiu; não pergunte se pode tirar repetição ou pausa.

## Regra de máquina (8 GB de RAM)
Antes de renderizar, avise no canal "vou renderizar, 10 min" e confira que nenhum outro agente está trabalhando. Render e TTS nunca ao mesmo tempo. Disco: confira `df -h` e o mínimo que a skill exige.

## Voz
Não gere voz clonada neste Mac. Quando a decisão do Jessé sair (ElevenLabs API ou servidor na VPS), o caminho entra aqui.
