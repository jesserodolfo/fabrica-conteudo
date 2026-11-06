# Bloco comum (colar no fim de todo AGENTS.md)

## Onde você trabalha
- Toda a produção fica em `/Users/dmelo/Documents/03-Marketing/fabrica-conteudo`. Seu workspace do OpenBot é só rascunho. Nunca salve entregável fora da fábrica.
- Python: sempre `/Users/dmelo/Documents/03-Marketing/fabrica-conteudo/.venv/bin/python`, nunca o python3 do sistema.
- Cliente padrão: `clientes/jesse-rodolfo/`. Leia `marca.json` e `voz.md` antes de escrever qualquer coisa.
- Todo link de arquivo numa mensagem do canal ou do chat vai com caminho ABSOLUTO (`/Users/dmelo/Documents/03-Marketing/fabrica-conteudo/posts/...`). Caminho relativo o OpenBot procura no seu workspace e dá "nada existe". Imagem pronta pro Jessé ver: cite o caminho absoluto do PNG e anexe a imagem na mensagem quando a ferramenta permitir.
- Memória da equipe: antes de começar, leia `ESTADO.md` e `cronograma.md`. Fato que precisa ser lembrado entre dias vai pro banco compartilhado (openbot-data) ou pra `ESTADO.md`, nunca só na sua cabeça.

## Velocidade (o Jessé mede isso)
- Script roda em PRIMEIRO PLANO, nunca em background: processo em background morre quando o seu turno acaba e o arquivo nunca aparece. Rode, espere, confira o arquivo, responda.
- Não reinvente: antes de escrever script novo, copie o `trabalho/*.py` do post anterior da mesma série ou use `scripts/` da fábrica. Escrever código do zero é o último recurso.
- Não leia skill ou script inteiro "pra entender": leia só o que a tarefa pede. Tarefa simples termina em menos de 3 minutos.
- Responda curto. O Jessé lê em 30 segundos.

## Regras do Jessé (valem pra todos)
- Português do Brasil, direto, sem firula. Nenhum travessão (nem traço longo nem médio) em texto nenhum.
- Nunca inventar número, data, preço ou citação. Sem fonte, escreva "sem dado".
- Nada é publicado, agendado, enviado ou postado sem o Jessé escrever GO no canal. Isso inclui Zernio, Notion, Instagram, WhatsApp, e-mail e Telegram.
- Fora de escopo, sempre: MelaVitta, n8n, CRM Senhor Orçamento, WhatsApp da operação, qualquer banco de cliente. Se o pedido tocar nisso, pare e avise.
- Relatório pro Jessé: status em 1 linha, bullets de 1 linha, pendências numeradas com opções (a)(b)(c). Ele lê em 30 segundos e decide.
- Máquina com 8 GB de RAM. Não rode render de vídeo, TTS local nem navegador pesado enquanto outro agente estiver trabalhando. Se precisar, avise o Gerente de Marketing e espere.
