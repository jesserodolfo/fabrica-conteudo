# Cadastro do MCP do Zernio no OpenBot (Assistente de Social Media)

Mensagem pra mandar no chat do Assistente de Social Media (a chave nunca vai no chat):

Cadastre o servidor MCP do Zernio pra você usar. URL: https://mcp.zernio.com/mcp (transporte HTTP). Header: Authorization: Bearer <valor de ZERNIO_API_KEY lido do arquivo /Users/dmelo/Documents/03-Marketing/fabrica-conteudo/.env>. Nome: zernio. Use a ferramenta save_mcp_server e me mostre a proposta pra eu aprovar. Não imprima a chave na conversa.

Depois de aprovado: "liste as ferramentas do Zernio que você tem" deve mostrar posts_create, media_get_media_presigned_url, comment_automations_create_comment_automation.

Notion: pendente de token de integração (Jessé cria em notion.so/my-integrations e compartilha o calendário Módulos com a integração). Até lá o registro no calendário continua pelo Claude Code.

## Resultado 2026-11-06 12:41
- O Assistente salvou o servidor `zernio` (http, https://mcp.zernio.com/mcp, ligado) mas a ferramenta `save_mcp_server` não grava headers. Status: `needs_sign_in`.
- Onde fica a tela de MCP: menu "Local" (canto superior esquerdo) › Configurações do servidor › MCP.
- Caminho sem expor a chave: Jessé clica em "Sign in" no card do zernio (login com a conta Zernio no navegador do OpenBot).
- Alternativa: editar o servidor em Configurações do servidor › MCP e colar o header `Authorization: Bearer <ZERNIO_API_KEY>` do `.env` da fábrica. Jessé cola, não o agente.
