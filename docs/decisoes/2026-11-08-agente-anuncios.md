# Agente de anúncios e métricas da Meta (08/11/2026)

## Contexto
- Portfólio Jessé IA (1765543101373143) com a página Jessé Rodolfo (1442101138983576), o Instagram @jesse.rodolfo (17841400511140821) e a conta de anúncio act_659760893074530 (Mastercard *7443, já usada em posts turbinados).
- Token de usuário de 60 dias no `.env` (META_USER_TOKEN), app Fabrica Jesse.
- IDs em `clientes/jesse-rodolfo/marca.json`, chave `meta`.

## Decisão
1. Novo agente `gestor-de-trafego` (Sonnet, só roda script). Sobe anúncio pausado e só ativa com o GO do Jessé e o valor escrito por ele.
2. `scripts/meta_ads.py`: contas, impulsionar (perfil, engajamento, direct; post existente ou arquivo novo), ativar com `--confirmo-gasto`, pausar, apagar, relatório com quebra por idade, gênero e posicionamento, listar. Registro em `anuncios/registro.jsonl`.
3. `scripts/meta_metricas.py`: só leitura. Conta, público, métricas por post, histórico dos anúncios e página. Sai em `pesquisa/metricas/`. O Analista usa no relatório e no briefing de criativo.
4. Teto de verba: nenhum por enquanto (`anuncios/limites.json` com null). O Jessé define o valor na primeira campanha.
5. Os três objetivos ficam disponíveis: visitas ao perfil, engajamento e direct.

## Alternativas descartadas
- SDK `facebook_business`: dependência a mais pra poucas chamadas. Ficou `requests`.
- Criativo só novo: o post que já saiu tem prova social e é o jeito das campanhas antigas. Os dois modos existem; o padrão é o post existente.
- Anúncio no Facebook: página com 0 seguidores. Posicionamento só Instagram por enquanto.
- Teto fixo de R$ 30 por dia: o Jessé preferiu decidir na primeira campanha.

## Risco
- Criar anúncio pode pedir permissão a mais (ex.: pages_manage_ads). Se pedir, gerar token novo com a permissão, sem contornar.
- Token vence em 06/01/2027 (META_TOKEN_EXPIRA no .env).

## Atualização (08/11/2026, fala do Jessé)
- As 17 campanhas da act_659760893074530 são de um produto antigo que ele vendia. Não servem de referência pra este público. Ficam pausadas.
- Público-alvo dos anúncios: dono de empresa que precisa da implementação (processo primeiro, IA depois), o mesmo da bio.
- O Jessé vai criar uma conta de anúncio nova no portfólio Jessé IA. Quando existir, trocar `meta.ad_account` no marca.json e começar o histórico do zero.

## Atualização (10/11/2026, fala do Jessé)
- A Meta ainda não deixa criar outra conta no portfólio Jessé IA. A primeira campanha (diagnóstico gratuito, 2 vídeos + 1 carrossel modelados no @olucaslopesc, R$ 50/dia) roda na própria act_659760893074530.
- O Jessé excluiu as 17 campanhas antigas (10/11). A conta está limpa. O histórico deste público começa nesta campanha.
