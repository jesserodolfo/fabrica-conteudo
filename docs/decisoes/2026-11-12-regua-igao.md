# Régua de edição do @igao.ia no formato didatico (12/11/2026)

## Contexto
O Jessé achou os reels sem rosto atuais ruins e pediu pra modelar a edição do @igao.ia. Pesquisa em `pesquisa/2026-11-12-igao-edicao/RESUMO.md`: 11 reels de 95 mil a 742 mil views. A casca do `didatico` já é a dele; falta o recheio (marca oficial, produto recriado, densidade, transição, som gravado, gancho 3D).

## Decisão (GO do Jessé em 12/11)
- Evoluir a skill `~/.claude/skills/didatico`, sem trocar de motor (HyperFrames).
- Marcas oficiais em `kit/marcas/` (lobe-icons e svgl, MIT), sempre sem recolorir nem deformar.
- Sons gravados do Kenney (CC0) em `kit/sfx/`; os sintéticos viram reserva.
- Biblioteca de peças de produto (navegador, WhatsApp, ChatGPT, planilha, CTA do Instagram, cursor, ícone de app).
- `monta.py`: palco maior, mais transições, cor de acento. Roteiro antigo continua renderizando igual.
- `kit/regua.py` mede o vídeo final contra a régua calibrada nos 11 reels do Igão.
- Piloto: DIAGNÓSTICO v7 em `posts/2026-11-12-reel-diagnostico/trabalho_v7/`. A pasta `trabalho/` (v6, agendado 18h) não é tocada.
- Legenda segue no vermelho do Jessé; a cor da marca entra só no cartão.

## Descartado
- Remotion: reescrever tudo e pesa mais em 8 GB.
- simple-icons: monocromático, perde o acabamento.
- Sonniss: 9 GB ou mais por pacote.
- Print real de tela: o Igão recria tudo em código, fica nítido e animável.

## Verificação
`regua.py` no v7 tem que passar nos mesmos limites em que os 11 do Igão passam; folha lado a lado com o reel de 742 mil. Reprovou 2 vezes na mesma cena: refaz a cena do zero.

## Reverter
Backup em `~/.claude/skills/didatico/_bak/2026-11-12-pre-regua-igao/` (kit e SKILL.md).
