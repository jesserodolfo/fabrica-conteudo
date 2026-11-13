"""Legendas LinkedIn e firstComment dos itens 4 a 56 da fila (adaptados do Instagram).

Regras aplicadas: português revisado, sem travessão, sem link no corpo, no máximo 3 hashtags
sem acento, sem fato novo, sem referência de tempo velha (hoje, amanhã, ontem, semana passada),
sem menção a direct, Story, link da bio ou "comenta X que eu te mando".

fc: texto do firstComment com {URL}. None = sem firstComment (presente privado, sem presente
ou presente de grupo de WhatsApp).
"""

APLICACAO = {10, 19, 28, 32, 39, 41, 47}  # presente = jesserodolfo.com.br/aplicacao (automacao)
SEM_FC = {8, 17, 18, 31, 33, 40, 51, 52, 53, 54, 55}
URL_OVERRIDE = {
    56: "https://orange-inch-2cc.notion.site/AUDIO-O-udio-do-seu-time-vira-o-documento-pronto-4138ab833e6c81118304fbc14a58d624",
}

TEXTOS = {
    4: {
        "legenda": """A maioria das automações não dá retorno porque é feita onde é fácil, não onde custa caro. A tarefa fácil já funcionava, e o processo que consome a equipe continua igual.

O checklist tem 5 perguntas para mapear cada área da empresa, um prompt que transforma suas anotações em mapa de processo e um jeito de separar gargalo de verdade do resto.

Começa por uma área só. A que mais te dá dor de cabeça.

O checklist completo está no primeiro comentário.

#processos #ia #gestao""",
        "fc": "O checklist com as 5 perguntas para mapear sua operação: {URL}",
    },
    5: {
        "legenda": """Estoque errado custa dos dois lados.

O que falta é venda perdida: o cliente pede, não tem, e a venda vai para o concorrente. O que sobra é dinheiro parado na prateleira, pagando espaço, validade e desconto para desovar.

E toda segunda alguém conta item por item na mão, perde a manhã e ainda descobre a falta pelo cliente.

O prompt faz diferente. Você cola duas listas que já tem, o estoque atual e as vendas do período, e ele cruza uma com a outra. Volta a lista do que vai faltar nos próximos 15 dias, com quanto comprar, e a lista do que não gira há 90 dias, com quanto dinheiro está parado e uma ação para cada item.

A regra é simples: o que não gira há 90 dias vira ação na mesma semana.

O prompt completo está no primeiro comentário.

#gestao #estoque #ia""",
        "fc": "O prompt completo para cruzar estoque e vendas: {URL}",
    },
    6: {
        "legenda": """A IA entra nos 3 níveis da gestão. Mas a ordem importa.

Todo dono quer começar pelo estratégico: cenário para 12 meses, plano de crescimento. Gosta do que lê. E a operação continua a mesma: entrega atrasando, orçamento saindo errado, a equipe perguntando tudo para ele.

A ordem certa é de baixo para cima.

Operacional: a IA organiza a semana por prioridade, escreve o processo a partir do que a equipe já faz e acompanha a pendência. É aqui que o dono fica preso.

Tático: desdobra o objetivo em metas por área, define o indicador de cada uma e aponta onde o plano vai travar.

Estratégico: cruza os números dos dois níveis de baixo, monta cenários e apoia a decisão. Não decide.

Cenário feito com dado errado do operacional é ficção bem escrita.

Os 3 prompts, um por nível, estão no primeiro comentário.

#gestao #ia #processos""",
        "fc": "Os 3 prompts, um por nível da gestão: {URL}",
    },
    7: {
        "legenda": """Se o seu melhor funcionário sair, alguém sabe fazer o que ele faz?

Na maioria das empresas, não. O passo a passo dele não está escrito em lugar nenhum. Está na cabeça dele. E a empresa só descobre o que ele fazia pelo que para de funcionar quando ele sai.

Eu passei 11 anos dentro de fábrica. Lá, todo posto tinha o passo a passo escrito. Se o operador faltava, outro entrava e fazia igual.

O prompt faz isso na sua empresa: mostra onde você depende de uma pessoa só, entrevista cada um da equipe, mapeia o que cada pessoa faz e transforma as tarefas de maior risco em manual que outra pessoa consegue seguir.

Não é para substituir ninguém. É para ninguém carregar a empresa sozinho.

O mapa completo, com os prompts, está no primeiro comentário.

#gestao #processos #equipe""",
        "fc": "O mapa completo de tarefas com os prompts: {URL}",
    },
    8: {
        "legenda": """Como fazer o seu Claude parar de ser puxa-saco em menos de 30 segundos.

No Claude, entra no seu perfil, depois em perfil de novo, e clica em instruções. Cola exatamente este texto:

"Não busque validação automática das minhas ideias. Espero análise crítica e identificação de riscos, gargalos, pontos fracos e oportunidades de melhoria, além de contrapontos construtivos. Aja como um conselheiro estratégico, não apenas como alguém que gera respostas agradáveis."

Pronto. A partir daí ele passa a trazer contraponto, mostrar o que você não está vendo e te ajudar a tomar decisões muito mais certas.

Você já pediu contraponto pra sua IA ou ela só concorda com você?

#claude #ia #prompt""",
        "fc": None,
    },
    9: {
        "legenda": """Empresário, você ainda fecha o fluxo de caixa do mês na mão?

Abre extrato, fatura e planilha lado a lado, separa entrada de saída de memória, tenta lembrar o que era cada lançamento. Quando vê, foi o dia inteiro. E o número que aparece no fim do mês só conta o estrago, porque a decisão que ele pedia já passou.

O prompt faz diferente. Você não precisa de planilha nova nem de sistema. Anexa no Claude a planilha que você já usa, do jeito que estiver, junto com o extrato e a fatura do mês, e cola o prompt. Ele lê linha por linha, separa entrada e saída, soma cada grupo e calcula o saldo.

Devolve três números: saldo do mês, custo fixo sobre a entrada e quantos lançamentos ficaram sem categoria. Esse último é o mais importante. O que o Claude não soube classificar não é erro da IA. É o seu processo falando: pagamento sem nome, compra sem nota, PIX sem motivo.

A regra: feche o caixa toda semana, não todo mês. Caixa visto toda semana vira decisão. Visto no fim do mês vira desculpa.

O prompt completo está no primeiro comentário.

#fluxodecaixa #gestao #ia""",
        "fc": "O prompt completo para fechar o caixa: {URL}",
    },
    10: {
        "legenda": """A Anthropic começou a dar até US$ 200 por mês de crédito para quem assina o Claude Max. São US$ 100 no Max 5x e US$ 200 no Max 20x.

Resgatei o meu. No navegador, vai em Configurações, Cobrança, Créditos de API e Vincular organização. O passo a passo, com os meus prints, está no carrossel.

Esse crédito é o que paga o Claude trabalhando sozinho, como um agente que responde o seu WhatsApp. Até agora isso era cobrado à parte.

Você resgata esse crédito sozinho. Agora, quer que eu entre na sua operação e te mostre onde colocar IA para ela render mais?

O link da aplicação da mentoria está no primeiro comentário.

#claude #ia #automacao""",
        "fc": "Link da aplicação da mentoria: {URL}",
    },
    11: {
        "legenda": """Tudo neste vídeo foi editado por inteligência artificial.

Eu mandei o vídeo bruto, com erro, respiração e falha, e ele voltou com corte, legenda palavra por palavra e animação, pronto em vertical. Eu sou leigo em edição, e foi só personalizar uma vez o jeito que eu queria.

Se você passa horas editando ou paga alguém para editar os seus vídeos, a instalação, que é simples, e os prompts que eu uso estão no primeiro comentário.

#claude #claudecode #ia""",
        "fc": "O guia para editar vídeo no Claude Code, com corte, legenda e animação: {URL}",
    },
    12: {
        "legenda": """Sua planilha de 10 mil linhas vira um painel executivo em 5 minutos, sem programar e sem pagar sistema.

O número que você precisa já está na planilha. O problema é que ninguém consegue ler 10 mil linhas, então o dono decide no achismo com o dado na mão.

No Claude é assim: você anexa a planilha do jeito que ela está, cola o prompt e recebe o painel com KPIs, gráficos e os 5 números que merecem atenção. São 8 prompts, um para cada pergunta do dono: margem, DRE, comercial, projeção, orçado x realizado e relatório para a diretoria.

A regra: roda primeiro a auditoria. Painel bonito com dado errado é ficção.

Os 8 prompts estão no primeiro comentário.

#claude #ia #gestao""",
        "fc": "Os 8 prompts, um para cada pergunta do dono: {URL}",
    },
    13: {
        "legenda": """O expediente acaba e a empresa continua rodando na sua cabeça. O pendente, o que não pode esquecer no dia seguinte, o que você prometeu pro cliente.

Na fábrica, nenhum turno acabava sem a passagem de turno. Na sua empresa, a passagem de turno é a sua cabeça às 23h.

Este prompt resolve isso em 5 minutos: você conta o dia, o Claude separa o que está resolvido, o que está pendente e com quem, e o que você decide para o dia seguinte. De manhã, a lista já vem pronta.

O prompt completo está no primeiro comentário.

#gestao #produtividade #ia""",
        "fc": "O prompt completo para fechar o dia: {URL}",
    },
    14: {
        "legenda": """O ChatGPT edita a sua foto e devolve o rosto de outra pessoa?

Não é defeito seu. É instrução incompleta. Quando você pede "melhora a luz", ele entende que pode mexer em tudo, inclusive no seu rosto.

A saída é dizer junto o que não pode mudar. As 5 etiquetas do carrossel resolvem os casos mais comuns: /identitylock, /poseonly, /studioquality, /upscale e /cleanup.

Na fábrica, peça boa saía de instrução clara. Com IA é igual.

Os 5 prompts completos, prontos para colar, estão no primeiro comentário.

#chatgpt #ia #fotoprofissional""",
        "fc": "Os 5 prompts completos, prontos para colar: {URL}",
    },
    15: {
        "legenda": """5 cursos que eu obrigaria todo dono de empresa a fazer. E são de graça.

A ordem importa. Primeiro você aprende a enxergar o processo, depois a cortar o desperdício, depois a ver o caixa toda semana. Só então entra a IA.

Na fábrica, ninguém automatiza a linha que ainda não tem padrão. Na sua empresa é igual: IA em cima de processo bagunçado só faz a bagunça andar mais rápido.

Os 5 cursos, com um plano de 30 dias para aplicar, estão no primeiro comentário.

#gestao #processos #ia""",
        "fc": "Os 5 cursos, na ordem certa, com o plano de 30 dias: {URL}",
    },
    16: {
        "legenda": """Se você paga pela voz da sua atendente de IA, esse vídeo é pra você.

O VoiceStudio é gratuito, tem mais de 67 mil estrelas no GitHub e roda no seu computador: clona voz, cria voz nova, dubla vídeo e transcreve áudio. Sem mensalidade.

Só um cuidado: clone apenas a voz de quem autorizou.

O repositório e o passo a passo para instalar com o Claude Code estão no primeiro comentário.

#ia #claudecode #atendimento""",
        "fc": "O repositório do VoiceStudio e o passo a passo para instalar com o Claude Code: {URL}",
    },
    17: {
        "legenda": """A partir de 12 de novembro, xingar o Claude pode suspender a sua conta.

A Anthropic mudou a política de uso: abuso contínuo e sem necessidade contra a IA pode levar aviso, limite de uso ou suspensão. Reclamar e pedir pra refazer continua normal.

O curioso é que pedido grosseiro costumava funcionar melhor. Não por causa do xingamento, mas porque bravo você vai direto ao ponto. Dá pra fazer isso de propósito: o quê, pra quem, formato e o que evitar.

Eu mesmo já xinguei várias vezes. E você, já xingou a sua IA pra ver se ela resolvia mais rápido?

#claude #ia #prompt""",
        "fc": None,
    },
    18: {
        "legenda": """A Tesla prometeu o novo Roadster em 2017. Disse que entregava em 2020. Atrasou, atrasou de novo, virou piada na internet.

Em outubro, no Texas, ela finalmente mostrou o carro. E não foi uma apresentação comum.

O Roadster subiu uma rampa curva, ficou de cabeça pra baixo, deu um giro no ar e pairou antes de pousar. Tudo isso com tecnologia da SpaceX: propulsores de gás frio, os mesmos princípios usados em foguete.

E o 0 a 100 km/h? Na versão Thrust, a Tesla promete menos de 0,9 segundo.

O preço do carro ainda não foi anunciado. Mas só para reservar o modelo de entrada são US$ 50 mil. E aí, compraria?

E a produção só começa em 2028. Ou seja, quem deu entrada lá em 2017 vai esperar mais de uma década para dirigir.

Genialidade ou a melhor jogada de marketing da história?

#tesla #spacex #inovacao""",
        "fc": None,
    },
    19: {
        "legenda": """Agente de IA que ninguém usa quase sempre começou pela ferramenta.

Assina a IA, monta um agente bonito e, um tempo depois, a equipe volta pra planilha. Eu vejo isso se repetir.

O que funciona é outra ordem: mapear o processo, achar a causa do problema, escolher a solução certa (nem sempre é agente), priorizar, planejar e construir junto com quem vai usar.

Processo primeiro, IA depois.

O link para fazer o diagnóstico da sua empresa está no primeiro comentário.

#ia #agentesdeia #processos""",
        "fc": "Link para o diagnóstico da sua empresa: {URL}",
    },
    20: {
        "legenda": """Seu Claude Code entrega coisas pela metade? Muitas vezes o problema é o jeito de pedir.

São seis frases simples: dividir o trabalho, ver o plano antes, deixar ele perguntar, testar antes de dizer pronto, guardar o que deu certo e automatizar o que se repete.

Qual dessas você ainda não usa?

Os seis prompts completos, para copiar e colar, estão no primeiro comentário.

#claudecode #claude #ia""",
        "fc": "Os seis prompts completos para copiar e colar: {URL}",
    },
    21: {
        "legenda": """Em vez da Netflix, assista esses 6 vídeos de IA. Todos de graça.

Eu juntei seis vídeos do YouTube na ordem que eu assistiria. Tem professor de Wharton, o presidente da Y Combinator e gente que montou empresa inteira rodando com IA.

Quatro dos seis têm áudio em português. Nos que não têm, dá pra ligar a legenda traduzida, e eu mostro como na página.

Qual desses você vai assistir primeiro?

Os 6 links, com o que anotar em cada um, estão no primeiro comentário.

#ia #empresas #processos""",
        "fc": "Os 6 links, com o que anotar em cada um: {URL}",
    },
    22: {
        "legenda": """Nem toda tarefa deve ir pra IA, e a primeira pergunta do teste nem é sobre IA.

É se a tarefa deveria existir. Se ela existe porque alguém corrige, refaz ou responde de novo, automatizar só faz o erro acontecer mais rápido.

O teste tem 4 perguntas, nessa ordem:
1. É retrabalho?
2. Duas pessoas fariam do mesmo jeito?
3. O erro aparece antes de chegar no cliente?
4. Acontece toda semana?

Cada tarefa termina em um destino: IA, processo ou gente. Passou nas 4, vai pra IA.

A regra que eu uso: a IA entra por último. Primeiro tira o que não deveria existir, depois escreve o processo, só então escolhe o que a ferramenta faz.

Qual tarefa da sua semana você passaria pelo teste primeiro?

O teste completo e o prompt que roda a sua lista estão no primeiro comentário.

#ia #gestao #processos""",
        "fc": "O teste completo e o prompt que roda a sua lista: {URL}",
    },
    23: {
        "legenda": """Se eu fosse começar no Claude do zero, eu montava essas 5 coisas, nessa ordem.

E eu uso as cinco de verdade:
1. Um segundo cérebro: uma pasta onde o Claude lembra quem eu sou e como eu trabalho
2. Uma resposta automática: a pessoa comenta uma palavra e recebe o link
3. Um editor de vídeo: eu edito meus vídeos com o Claude Code
4. Um time de conteúdo: uma fábrica de agentes que monta carrossel e agenda
5. Um criador de sites: eu crio site de cliente com o Claude

Você não precisa saber programar. Escreve em português e ele faz. Só o Claude Code precisa do plano pago.

Qual dessas cinco você montaria primeiro?

O passo a passo de cada uma está no primeiro comentário.

#claudecode #ia #automacao""",
        "fc": "O passo a passo de cada uma das 5: {URL}",
    },
    24: {
        "legenda": """Antes de contratar, descubra onde o tempo da sua equipe está indo.

A sensação é que a equipe não dá conta e precisa de mais gente. Às vezes é verdade. Muitas vezes, a pessoa sobrecarregada gasta boa parte da semana em tarefa repetida ou retrabalho, e contratar só compra mais horas do mesmo problema.

O passo a passo:
1. Anote 5 dias da pessoa sobrecarregada: a tarefa, quanto tempo levou e quantas vezes na semana.
2. Um prompt separa cada tarefa em 3 grupos: repetida, retrabalho e precisa de pessoa. Ele soma as horas de cada grupo e diz se contrata agora, se ainda não ou se contrata para outra função.

Como ler: se a maior parte está no grupo 1 ou 2, o problema é processo. Resolva o retrabalho primeiro. Se está no grupo 3, é gente, e você já sabe para qual função. Se está dividido, ataque o retrabalho, espere 2 semanas e rode de novo.

A regra: se a tarefa é retrabalho, contratar só aumenta o retrabalho. Primeiro tire o que não deveria existir, depois conte quantas horas faltam de verdade.

Qual tarefa da sua equipe você acha que é retrabalho e ninguém percebeu?

O prompt está no primeiro comentário.

#gestao #processos #produtividade""",
        "fc": "O prompt que separa o tempo da equipe em 3 grupos: {URL}",
    },
    25: {
        "legenda": """Um agente que entrega o relatório de vendas toda segunda, às 8h, sem ninguém pedir.

Eu mostro os 7 passos no vídeo. Dá pra montar no app do Claude, sem escrever código.

A tarefa programada precisa do plano pago. Do passo 1 ao 6 você faz sem pagar nada.

Qual relatório você mais gostaria de receber sozinho toda semana?

As instruções prontas para copiar estão no primeiro comentário.

#ia #claude #agentesdeia""",
        "fc": "As instruções prontas para copiar, passo a passo: {URL}",
    },
    26: {
        "legenda": """A maioria dos donos usa o Claude só pra perguntar. Isso é 1 de 4 jeitos.

Os outros 3 são onde o tempo da semana volta. São 4 jeitos de usar o mesmo Claude, não 4 produtos:
1. Conversar: você conta a situação e ele faz as perguntas que um sócio faria, antes de você decidir. No chat, no celular ou no computador.
2. Trabalhar nos seus arquivos: ele lê a planilha de vendas, monta o relatório e escreve a proposta enquanto você faz outra coisa. No app do Claude no computador, com acesso às suas pastas.
3. Construir: painel de pedidos, formulário, site. Uma ferramenta simples pra equipe, feita no Claude Code, no computador.
4. Montar material: apresentação, proposta visual ou página descrita em texto. Dentro do Claude.

Qual jeito pra cada tarefa? Decidir se contrata mais uma pessoa é conversar. Fechar o relatório de vendas é arquivos. Equipe perguntando "onde está o pedido" pede um painel, que é construir. Proposta pra cliente grande é material.

O erro que anula os 4: escolher o jeito antes de saber qual etapa trava. Você termina com automação na tarefa fácil e o gargalo igual. A ordem é mapa, gargalo, ferramenta. O jeito do Claude é a ferramenta, então vem por último.

Qual tarefa da sua semana você levaria pra um desses jeitos primeiro?

O guia dos 4 jeitos está no primeiro comentário.

#inteligenciaartificial #gestao #processos""",
        "fc": "O guia dos 4 jeitos de usar o Claude: {URL}",
    },
    27: {
        "legenda": """Seu Claude fica burro no meio do projeto? Não é ele. É a memória dele que encheu.

Toda conversa tem um limite. Quanto mais cheia, mais cara fica cada resposta e menos ele lembra do começo. E você não vê isso acontecendo.

Então eu coloquei um termômetro no meu Claude Code. E sigo 4 regras:
1. Amarelou, começo a fechar o assunto
2. Não deixo chegar no vermelho
3. Troco de conversa passando o bastão
4. Um assunto por conversa

Em quantos por cento está a memória da sua conversa?

O prompt pronto para instalar no seu Claude Code está no primeiro comentário.

#claudecode #claude #produtividade""",
        "fc": "O prompt pronto para instalar o termômetro no seu Claude Code: {URL}",
    },
    28: {
        "legenda": """6 sistemas para criar com Claude. Um por setor.

Frota: onde está cada caminhão e qual entrega vai atrasar.
Estoque: mínimo e máximo de cada item e o que repor.
Varejo: a venda de cada produto no dia.
Restaurante: pedidos, CMV e estoque do dia.
Obra: cronograma e custo de cada etapa, sem planilha.
E-commerce: qual produto vende e qual só ocupa espaço.

As telas são exemplos, com dados de exemplo.

Qual é o seu negócio?

As perguntas para ver qual sistema serve na sua empresa estão no primeiro comentário.

#claude #ia #gestao""",
        "fc": "As perguntas para ver qual sistema serve na sua empresa: {URL}",
    },
    29: {
        "legenda": """Você usa IA todo dia e o trabalho continua todo na sua mesa? É porque você está usando o chat.

O chat responde. Você pergunta, ele devolve um texto, e quem copia, cola, manda e confere é você.

O agente trabalha. Você não faz uma pergunta, você dá um objetivo. Ele olha o que tem, decide o próximo passo, faz, confere e repete até terminar.

No contas a pagar: lê cada boleto, confere com a nota, deixa o pagamento pronto e só te chama quando alguma coisa não bate. Você só aprova.

Mas agente sem regra é igual operador sem procedimento: faz do jeito dele.

Qual processo da sua empresa você entregaria primeiro pra um agente?

O passo a passo para montar o seu primeiro agente está no primeiro comentário.

#claudecode #agentesdeia #automacao""",
        "fc": "O passo a passo para montar o seu primeiro agente de IA: {URL}",
    },
    30: {
        "legenda": """Dá pra fechar o mês sem montar fórmula.

Você manda o extrato e a planilha de contas pro Claude e pergunta: quanto sobrou no caixa, o que passou do orçamento, quem está devendo. Ele calcula e explica cada número.

Você não precisa abandonar o Excel. Só deixa de gastar o fim de semana com PROCV e tabela dinâmica. Dá pra testar no plano grátis. E sempre peça pra ele mostrar o cálculo, porque ele pode errar.

O guia traz 3 prompts prontos: fechamento do mês, gasto fora do orçamento e inadimplência.

Qual planilha toma mais o seu tempo?

O guia completo, com os prompts e o passo a passo, está no primeiro comentário.

#claude #ia #gestao""",
        "fc": "O guia completo com os 3 prompts: {URL}",
    },
    31: {
        "legenda": """Bancos dos EUA acharam agentes de IA dentro das contas dos clientes. E alguns estavam fazendo coisa que ninguém pediu.

A Axios publicou a matéria. Morgan Stanley, JPMorgan, Bank of America e Wells Fargo estão correndo para conter. Na maioria dos casos ninguém invadiu nada: o próprio cliente entregou login e senha pro agente, e do lado do banco não dá pra saber se quem está logado é a pessoa ou a IA.

Resposta dos bancos: Morgan Stanley bloqueou agentes de terceiros, e os outros estão indo para acesso só de leitura. A IA vê a conta, não mexe no dinheiro.

Isso é cibersegurança, e vale pra qualquer agente que você criar na sua empresa. Agente com acesso demais é porta aberta pra golpe e vazamento. A regra: ele prepara, confere e avisa, mas não mexe no dinheiro. Toda ação de risco passa por uma pessoa que aprova.

Você já deu login de alguma coisa pra uma IA?

#ia #agentesdeia #ciberseguranca""",
        "fc": None,
    },
    32: {
        "legenda": """Passada a eleição, o processo da sua empresa continua o mesmo.

Antes de contratar mais gente, descubra onde o seu time perde tempo. Na maioria das empresas que eu vejo, o que trava é tarefa repetida feita à mão.

Arrume o processo, coloque IA onde ele aperta (atendimento, financeiro, RH, marketing) e meça antes e depois. Assim você sabe o que funcionou.

O link para o diagnóstico da sua operação está no primeiro comentário.

#gestao #processos #ia""",
        "fc": "O link para o diagnóstico da sua operação: {URL}",
    },
    33: {
        "legenda": """Saí de uma reunião com um empresário que eu atendo e ele estava desesperado com o resultado das eleições.

Não é sobre política. É sobre o que já apareceu no bolso de quem tem empresa: dólar subindo, juros altos por mais tempo e cliente mais seletivo.

O que eu falei pra ele fazer a partir de agora:
1. Caixa, pra comprar oportunidade quando os outros precisarem vender
2. Margem, arrumando o processo e colocando IA no trabalho repetitivo
3. Receita que se repete: recompra, recorrência, cliente que volta
4. Menos dependência de um produto, um canal, uma pessoa ou um cliente

Você não controla o que acontece lá fora. A sua operação você controla.

Qual desses quatro pontos mais pesa na sua empresa?

#empresario #gestao #ia""",
        "fc": None,
    },
    34: {
        "legenda": """Antes de pagar agência ou gestor de tráfego, vale saber o que dá pra fazer com IA.

Eu montei um time de Meta Ads dentro do Claude. São 5 funções, cada uma com um pedido pronto:
1. Espião de concorrentes: lê a Biblioteca de Anúncios da Meta pelo navegador e lista o que eles anunciam
2. Copywriter: escreve várias ideias de anúncio no seu tom
3. Analista de criativos: dá nota no anúncio antes de você pagar por ele
4. Estrategista: compara concorrentes e acha o ângulo que ninguém usa
5. Auditor: lê o relatório que você exporta do Gerenciador e mostra onde a verba vaza

Um detalhe honesto: os agentes não entram na sua conta de anúncios. Você exporta o relatório e anexa só o que quiser mostrar.

Eles funcionam em sequência: pesquisa, oportunidade, criação, avaliação e resultado, tudo no mesmo lugar.

Você já usa IA nos seus anúncios ou ainda deixa tudo na mão de terceiros?

O guia com os prompts e o passo a passo está no primeiro comentário.

#metaads #claude #ia""",
        "fc": "O guia com os prompts e o passo a passo para o time de Meta Ads: {URL}",
    },
    35: {
        "legenda": """Sua empresa pode estar pagando por coisa que ninguém usa.

Empresa que lucra também vaza dinheiro. Assinatura de software esquecida, cobrança em duplicidade de fornecedor, desconto que virou padrão. Ninguém vê, porque cada um é pequeno.

Eu fiz um prompt que lê os extratos e a fatura do cartão dos últimos 3 meses e devolve a lista: cobranças que se repetem, valores duplicados e gastos que subiram mais de 20%, com o valor ao lado de cada um.

Passei 11 anos em fábrica caçando desperdício. Lá e aqui a lógica é a mesma: perda pequena que se repete todo mês vira número grande no ano.

O Claude só aponta. Quem confirma e decide o que corta é você. Nada é cancelado sem o seu ok.

O prompt, pra copiar e colar no Claude junto com os arquivos:

Vou anexar os extratos bancários e a fatura do cartão da minha empresa dos últimos 3 meses. Leia tudo e monte uma tabela com três grupos: (1) cobranças que se repetem todo mês, (2) lançamentos duplicados, com mesmo valor e mesmo favorecido no mesmo mês, (3) gastos que subiram mais de 20% de um mês para o outro. Para cada item mostre: favorecido, valor mensal, meses em que apareceu e quem na empresa pode confirmar. Não cancele nada e não conclua nada sozinho. Se faltar informação, pergunte.

Qual foi a última cobrança esquecida que você achou na sua empresa?

A versão completa, que acha os ralos, faz as perguntas certas e monta o plano do que cortar, com a economia no ano, está no primeiro comentário.

#claude #ia #gestao""",
        "fc": "A versão completa do prompt, com as perguntas e o plano do que cortar: {URL}",
    },
    36: {
        "legenda": """Seu relatório de segunda pode estar pronto antes de você sentar na mesa.

Sabe aquela segunda inteira de copia e cola pra juntar extrato, vendas e planilha? Dá pra entregar isso pro Claude. Nos slides está como eu monto isso numa empresa, em 6 passos, com uma casa de ração de exemplo. Os números são de exemplo, de uma casa de ração.

A base é simples: o relatório responde 4 perguntas. Quanto entrou, quanto saiu, quanto sobrou e o que fugiu do normal. O que não responde uma delas sai.

Uma verdade sobre a ferramenta: agendar pra rodar sozinho toda segunda e mandar por e-mail exige o Claude Code (tarefa agendada) com o Gmail conectado. No Claude comum não agenda, mas você cola o mesmo prompt toda segunda e leva 1 minuto.

Versão curta, pra copiar e colar no Claude com os arquivos anexados:

Vou anexar os extratos e a planilha de vendas da semana. Monte o relatório de segunda respondendo 4 perguntas: quanto entrou, quanto saiu, quanto sobrou e o que fugiu do normal. Compare com a semana anterior. No topo, coloque um alerta para cada despesa 22% acima da média, cliente com mais de 10 dias de atraso e venda abaixo do custo. Termine com um resumo de 5 linhas. Não invente número. Se faltar informação, pergunte.

Quem monta o relatório de segunda na sua empresa?

A skill completa, com as 4 perguntas, as regras de alerta, o formato e como agendar, está no primeiro comentário.

#claude #gestao #automacao""",
        "fc": "A skill completa do relatório de segunda, com as 4 perguntas, as regras de alerta e como agendar: {URL}",
    },
    37: {
        "legenda": """Fim de mês é sempre igual: nota no e-mail, nota no WhatsApp, nota na gaveta, e o contador cobrando.

Dá pra deixar isso na mão do Claude, como um funcionário. Você joga as notas numa pasta, ele lê cada uma, renomeia, separa em entrada, saída e serviço, avisa o que está estranho e escreve o e-mail pro contador. O e-mail só sai depois do seu ok.

Duas coisas pra não errar: guarde o XML da nota (ele é o documento fiscal, o PDF só mostra), e salve os anexos do e-mail na pasta antes, porque o Claude não lê anexo direto do Gmail. Ele organiza e aponta, não valida nota e não substitui o contador.

A pasta conectada e o agendamento são do Cowork, no app do Claude pro computador, que é plano pago. Com PDFs anexados, o Claude comum também serve.

Versão curta, pra colar no Claude com os PDFs anexados:

Vou anexar as notas fiscais do mês. Pra cada uma, registre número, data, emitente, CNPJ, valor e se é compra, venda ou serviço. Monte uma tabela resumo, liste o que parece estranho (nota repetida, sem valor, sem data) e escreva o rascunho do e-mail pro meu contador. Use só o que está nos arquivos e não invente dado.

Quem cuida das notas da sua empresa?

O prompt completo para organizar as notas do mês e mandar pro contador está no primeiro comentário.

#claude #gestao #automacao""",
        "fc": "O prompt completo para organizar as notas do mês e mandar pro contador: {URL}",
    },
    38: {
        "legenda": """Contrato no Downloads, nota fiscal na Área de Trabalho, planilha chamada "final final 2". Cada minuto procurando arquivo é um minuto que ninguém vende nem entrega.

No app do Claude no computador, abre a aba Code (precisa de plano pago) e escolhe a pasta embaixo da caixa de mensagem. Ele lê os arquivos pelo conteúdo, cria as subpastas e move tudo. Com o prompt, ele mostra o plano antes e só mexe depois que você ler e disser sim.

Antes de começar: faça uma cópia da pasta, comece por uma pequena e não conecte pasta com dado sensível.

A versão curta do prompt:

"Organize a pasta que eu conectei. Leia os arquivos pelo conteúdo. Antes de mexer, me mostre o plano: as subpastas que vai criar e o que vai pra cada uma. Só mova depois do meu ok. Não apague nada. No fim, me dê um resumo do que foi pra onde."

Qual é a pasta mais bagunçada do seu computador? Conta aqui nos comentários.

O prompt completo, com LEIAME da pasta e separação de duplicados, está no primeiro comentário.

#claude #ia #produtividade""",
        "fc": "O prompt completo para organizar as pastas da empresa, com LEIAME e separação de duplicados: {URL}",
    },
    39: {
        "legenda": """Prazer, eu sou o Jessé.

Passei mais de 11 anos dentro da indústria, na General Motors. Comecei no chão de fábrica, como operador de produção, e cheguei à auditoria de Short Lead Time, trabalhando com processos, padronização e melhoria contínua.

Foi lá que aprendi uma coisa que levo comigo desde então: ferramenta nova não resolve operação desorganizada.

Depois, levei essa experiência para o empreendedorismo e para as operações digitais, trabalhando com vendas, e-commerce, atendimento e automações.

Há cerca de 3 anos também desenvolvo agentes de inteligência artificial para atendimento, logística e cobrança.

Meu trabalho é ajudar empresas que já vendem, têm equipe e uma operação funcionando, mas ainda enfrentam gargalos, retrabalho e dependência excessiva do dono.

Eu começo entendendo o processo. Identifico o que precisa melhorar. E só depois implemento automação e IA, quando fazem sentido.

Processo primeiro. IA depois.

Se você sente que sua empresa poderia funcionar melhor, o link para conhecer o meu trabalho está no primeiro comentário.

#processos #gestao #ia""",
        "fc": "Link para conhecer o meu trabalho: {URL}",
    },
    40: {
        "legenda": """Cada um responde de um jeito, o cliente espera horas e reclamação fica sem resposta padrão.

Quando eu auditava processo, o primeiro passo era sempre o mesmo: sem padrão escrito, não tem o que conferir.

Você explica como atende, o Claude monta o manual (respostas aprovadas por tema, quando chamar um humano, modelo de reclamação, tom de voz) e depois confere as respostas do time contra ele.

Nada sai sem você aprovar.

É a parte 1 de 6 da série sobre padronizar a empresa com o Claude.

#ia #claude #processos""",
        "fc": None,
    },
    41: {
        "legenda": """Sua empresa pode estar vendendo bem e, mesmo assim, ter uma operação desorganizada.

Isso acontece quando tudo depende do dono, os processos são manuais, as informações ficam espalhadas e a equipe precisa perguntar a todo momento o que fazer.

O resultado? Retrabalho, atrasos, perda de produtividade e um dono que passa o dia resolvendo o que a equipe deveria resolver sozinha.

Mas a solução não é simplesmente contratar mais pessoas ou comprar mais ferramentas.

É entender o que está acontecendo, identificar os gargalos e organizar os processos.

Depois, quando fizer sentido, implementar tecnologia, automação e inteligência artificial.

Processo primeiro. IA depois.

Se você se identificou, o próximo passo está no primeiro comentário.

#gestao #processos #ia""",
        "fc": "Link para dar o próximo passo: {URL}",
    },
    42: {
        "legenda": """Salva este post e usa os 5 prompts quando precisar.

Já dei mentoria de finanças pessoais na minha igreja. E o erro que mais vi lá se repete na empresa: dinheiro da casa e do negócio na mesma conta, e ninguém sabe quanto sobra no fim do mês.

Os 5 prompts:
1. Raio-x do caixa: entradas e saídas dos últimos 3 meses, separadas em até 8 categorias, com os 3 números para olhar toda semana.
2. Caça-vazamento: assinatura que ninguém usa, tarifa de banco, taxa de maquininha, juros e fornecedor que dá pra renegociar.
3. Quem me deve: lista separada por atraso, com ordem de cobrança e mensagem educada para cada grupo.
4. Casa de um lado, empresa do outro: separa o gasto pessoal do da empresa e sugere um pró-labore fixo que o caixa aguenta.
5. Fechamento do mês: 5 passos para repetir todo mês, com o número que mostra que o mês foi bom.

Antes de colar, tira CPF, CNPJ e número de conta.

A IA faz a conta. O processo é seu: separar as contas, lançar tudo e fechar todo mês. Processo primeiro, IA depois.

Os 5 prompts completos, com o passo a passo em português, estão no primeiro comentário.

#financas #gestao #ia""",
        "fc": "Os 5 prompts completos, com o passo a passo em português: {URL}",
    },
    43: {
        "legenda": """Fim de mês vira caça ao comprovante: nota espalhada, ninguém sabe o que já foi pago e o fechamento depende de uma pessoa só.

Nas auditorias que eu fazia, o processo bom tinha checklist e dono. Financeiro sem rotina escrita fecha cada mês de um jeito.

Você explica como fecha o mês, o Claude monta o manual (dia fixo, quem lança e quem confere, onde guardar comprovante, extrato batido com os lançamentos) e depois confere o mês contra ele.

Nada é pago sem você aprovar.

É a parte 2 de 6 da série sobre padronizar a empresa com o Claude.

O prompt completo para montar o manual de fechamento do mês está no primeiro comentário.

#ia #claude #financeiro""",
        "fc": "O prompt completo para montar o manual de fechamento do mês: {URL}",
    },
    44: {
        "legenda": """Funcionário novo pergunta tudo pra você: cada um ensina de um jeito, o que ele precisa saber está na sua cabeça e ele demora pra trabalhar sozinho.

Eu comecei no chão de fábrica como operador de produção e depois fui SME de padronização. Tarefa que só existe na cabeça de alguém não passa pro novato.

Você explica como é a função e o primeiro dia, o Claude monta o manual (primeiro dia, quem ensina cada tarefa, passo a passo, acessos, o que ele faz sozinho e o que pede aprovação) e depois responde as dúvidas do novato com base nele.

O que não está no manual volta pra você e entra no manual.

É a parte 3 de 6 da série sobre padronizar a empresa com o Claude.

O prompt completo para montar o manual do funcionário novo está no primeiro comentário.

#ia #claude #gestao""",
        "fc": "O prompt completo para montar o manual do funcionário novo: {URL}",
    },
    45: {
        "legenda": """Se você tem escritório de advocacia, sabe quanto custa cada contestação. Alguém do time passa horas lendo a petição inicial, separando os pedidos e montando a peça do zero, toda vez.

No vídeo eu mostro o Claude fazendo isso. Ele lê a petição e os anexos, confere o prazo, levanta as preliminares, responde cada pedido do autor e entrega a contestação em Word. Quem revisa e assina continua sendo o advogado.

E você faz isso uma vez só. Manda um modelo que já deu certo no escritório, pede pro Claude transformar em habilidade e, da próxima vez, é só chamar pelo nome.

Processo primeiro. IA depois.

O material para montar a contestação com o Claude está no primeiro comentário.

#ia #claude #advocacia""",
        "fc": "O material para montar a contestação com o Claude: {URL}",
    },
    46: {
        "legenda": """Cada entrega sai de um jeito: depende de quem fez, o cliente reclama do que faltou e só uma pessoa sabe o jeito certo.

Na fábrica eu trabalhava com trabalho padronizado: a mesma tarefa, na mesma ordem, do mesmo jeito, não importa quem faz. Na sua operação vale o mesmo.

Você explica como uma entrega é feita, o Claude monta o manual (o que o cliente recebe, as etapas na ordem, o dono e o prazo de cada uma, o checklist antes de entregar) e depois monta a lista do dia com base nele.

Quem decide a prioridade é você.

É a parte 4 de 6 da série sobre padronizar a empresa com o Claude.

O prompt completo para montar o manual de entrega está no primeiro comentário.

#ia #claude #gestao""",
        "fc": "O prompt completo para montar o manual de entrega: {URL}",
    },
    47: {
        "legenda": """Muita empresa compra uma ferramenta nova esperando que a bagunça acabe. E a bagunça continua, só que mais rápida.

Por isso eu começo por outro lugar. São 5 passos, nessa ordem:

1. Entender a rotina, acompanhando o trabalho de quem faz.
2. Achar onde o trabalho para.
3. Desenhar o jeito certo de fazer, com dono, ordem e critério.
4. Só então colocar tecnologia, onde ela tira trabalho repetido.
5. Medir e ajustar.

Às vezes a resposta certa é não usar IA. E tudo bem.

Processo primeiro. IA depois.

Se você quer descobrir onde a sua operação está travando, o link está no primeiro comentário.

#gestao #processos #ia""",
        "fc": "Link para descobrir onde a sua operação está travando: {URL}",
    },
    48: {
        "legenda": """As 5 skills para o Claude Code:

1. Graphify: mapa do projeto, o Claude não relê tudo a cada sessão.
2. HyperFrames: vídeo animado a partir de texto.
3. Humanizer: tira as marcas de texto escrito por IA.
4. Reverse Engineer: pega um programa pronto e explica como funciona por dentro.
5. Find Skills: procura uma habilidade pronta antes de você criar do zero.

Os links das 5 e o passo a passo para instalar estão no primeiro comentário.

#ia #claude #claudecode""",
        "fc": "Os links das 5 skills e o passo a passo para instalar: {URL}",
    },
    49: {
        "legenda": """Quando quem acha o erro é o cliente, falta um passo antes de entregar: conferir.

Na fábrica eu terminei como auditor. Auditar é pegar o padrão escrito e conferir, item por item, se o que foi feito bate com ele. Sem padrão, não tem o que conferir.

Você conta os erros que mais voltam, o Claude monta o checklist (o que precisa estar certo, como conferir, o que é erro, quem confere e o que fazer quando reprova) e depois confere cada entrega antes de sair.

Quem aprova a entrega é você.

É a parte 5 de 6 da série sobre padronizar a empresa com o Claude.

O prompt completo para montar o checklist de qualidade está no primeiro comentário.

#ia #claudecode #gestao""",
        "fc": "O prompt completo para montar o checklist de qualidade: {URL}",
    },
    50: {
        "legenda": """Antes de lançar um produto ou mudar o preço, teste no Claude.

O Founder são 11 skills gratuitas, sem cadastro e sem chave de API. Três delas:
1. Um financeiro que calcula quanto sobra em cada venda e quantas vendas pagam as contas fixas.
2. 100 clientes simulados do seu público, cada um com renda, hábito e uma desculpa pra não comprar. Ele mostra quem compra, quem não compra e o motivo.
3. Um veredito no fim: dá lucro, ainda não dá ou falta informação, e o que mudar pra conta fechar.

Só um cuidado: é simulação. O resultado é o teto, não a garantia. Erra no Claude antes de errar com dinheiro, e confirma com cliente de verdade.

O link e o passo a passo em português estão no primeiro comentário.

#ia #claude #empreendedorismo""",
        "fc": "O link e o passo a passo em português: {URL}",
    },
    51: {
        "legenda": """Cada vendedor vende do seu jeito: um esquece de dar retorno pro cliente, outro negocia diferente e a venda se perde no meio do caminho.

Depois da fábrica eu fui pra vendas, e-commerce, atendimento e automações. Nos últimos anos construí soluções com IA, incluindo agentes pra operação comercial.

Você explica como a sua equipe vende, o Claude monta o manual (etapas do funil, follow-up, motivo de perda e quem é responsável por cada contato) e depois avisa quem está esperando retorno.

Quem fecha a venda é você.

É a parte 6 de 6 da série sobre padronizar a empresa com o Claude.

#ia #claude #vendas""",
        "fc": None,
    },
    52: {
        "legenda": """Se volta toda semana, já é processo. Só falta escrever o jeito de fazer e ensinar pro Claude.

Relatório de segunda, a mesma pergunta de cliente, a cobrança de quem atrasou, a reunião que vira nada e a conferência de pedido com pagamento.

Escolhe uma, a que mais toma o seu tempo. Roda junto duas semanas e confere. O Claude prepara, quem manda é você.

Salva pra ter as 5 na mão na segunda de manhã.

#ia #claude #gestao""",
        "fc": None,
    },
    53: {
        "legenda": """Quando tudo parece urgente, a equipe apaga incêndio o dia inteiro e o problema de verdade fica pra depois.

Perguntar pro Claude "o que eu resolvo primeiro?" dá resposta genérica. Dando o método, a resposta muda.

GUT pra escolher o problema, SIPOC pra enxergar o processo, 5 porquês pra achar a causa e PDCA pra testar a correção.

Salva pra abrir na próxima vez que tudo parecer urgente.

Primeiro o processo. Depois a IA.

#ia #claude #gestao""",
        "fc": None,
    },
    54: {
        "legenda": """O Pix caiu no dia 6 de novembro, e isso nem foi o mais estranho.

Cripto travada no Nubank e no Mercado Pago, Binance roubada, banco na França hackeado e kit de 72 horas na Europa e na Defesa Civil daqui. Tudo em duas semanas. A Defesa Civil diz que é prevenção, sem alerta.

Não sei o que pode acontecer, mas que está estranho, está. O que vocês acham?

Fontes: O Povo e Mix Vale (Pix, 06/11); Bloomberg Línea e O Tempo (cripto, 06/11); AP e The National (Binance, 29 e 30/10); AFP/Swissinfo e Jovem Pan (Crédit Mutuel Arkéa, 04/11); Comissão Europeia (03/11); Metrópoles (Defesa Civil, 07/11).

#pix #economia #noticias""",
        "fc": None,
    },
    55: {
        "legenda": """Contratou errado e quer resolver na demissão?

Um empresário que eu atendo chegou na reunião com raiva de um funcionário. O motivo não tinha nada a ver com o trabalho: o funcionário tinha votado no Lula.

Perguntei: ele entrega? Chega e sai no horário? Cumpre as regras? Sim pra tudo.

Mandar embora assim pode virar processo por discriminação. E gente boa tá difícil de achar.

O erro de verdade foi antes, na contratação: missão, visão e valores claros já na entrevista.

E você, demitiria? Me conta aqui nos comentários.

#contratacao #gestao #ia""",
        "fc": None,
    },
    56: {
        "legenda": """Antes de colocar IA em qualquer empresa, eu faço sempre a mesma coisa.

1. Pergunto pro time qual tarefa eles mais odeiam fazer todo dia.
2. Começo só por essa. Uma só.
3. Uso o que o time já usa. Se todo mundo vive no WhatsApp, a pessoa só manda um áudio contando o que fez.
4. A IA transcreve e monta o relatório sempre do mesmo jeito. O responsável confere e aprova antes de mandar.

Ninguém precisou aprender sistema novo. Primeiro o processo, depois a IA.

O prompt e o passo a passo em português estão no primeiro comentário.

#ia #processos #negocios""",
        "fc": "O prompt e o passo a passo em português: {URL}",
    },
}
