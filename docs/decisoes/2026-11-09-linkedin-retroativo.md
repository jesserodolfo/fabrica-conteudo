# LinkedIn: republicar tudo do Instagram (2026-11-09)

## Decisão
Tudo que já saiu no Instagram (@jesse.rodolfo) também sai no LinkedIn pessoal do Jessé, pela conta nova do Zernio (contato@example.com).

- Chave: `ZERNIO_LINKEDIN_API_KEY` no `.env` (fora do git). Conta LinkedIn `6af20e7ac552269948f1684e`, profile `6af20e3344dccfd44e276e9b`.
- Retroativo: 57 posts do Instagram (39 carrosséis, 18 reels), do mais antigo pro mais novo, 3 por dia às 8h, 12h e 18h BRT, até alcançar o dia atual. Depois, todo post novo do Instagram entra também no LinkedIn.
- Fora: repostagens repetidas (fica só a primeira) e vídeos do TikTok Shop.
- Carrossel vira documento PDF (os mesmos slides, `documentTitle` = título da capa). Reel vai como vídeo.
- Legenda adaptada pro LinkedIn: texto corrido, no máximo 3 hashtags, sem link no corpo, nenhum fato novo, sem travessão.
- Entrega do presente: a mesma página do Notion. No LinkedIn não há DM, então a automação de comentário responde em público com o link, e o link também vai no `firstComment`. Antes de agendar, conferir pela getPublicPageData se o presente está público.
- Agendamento só com GO do Jessé. Os 3 primeiros passam por prévia.

## Alternativas descartadas
- Imagens soltas no lugar do PDF: o LinkedIn mostra pior, e o PDF é o carrossel nativo.
- Link na legenda: o LinkedIn reduz o alcance do post com link.
- Refazer as artes sem "Comenta PALAVRA": daria mais trabalho, e a resposta pública da automação já cumpre o CTA.
