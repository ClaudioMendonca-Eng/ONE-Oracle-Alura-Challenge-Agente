# Challenge Alura Agente

O que eu entendi sobre o desafio final do curso de **Multi-cloud & OCI**, feito em conjunto com o Alura Agent.

> Fontes: material do curso na plataforma Alura e a [live de dúvidas sobre o Challenge](https://www.youtube.com/live/VQEybkw3xqs), conduzida pelas instrutoras da Alura.

## Datas importantes

- **19 de agosto, até 23:59** — prazo final para entrega do Challenge. Não é possível entregar depois dessa data/hora, mas posso entregar antes se terminar antes.
- **12 de agosto** — evento "Show Projects": uma conversa não técnica com pessoas sorteadas que já concluíram o projeto até a data, para compartilhar a experiência (bom para montar portfólio). O formulário para se candidatar ao sorteio costuma ser divulgado cerca de uma semana antes.
- Não preciso assistir a todas as trilhas/formações do programa para poder entregar o Challenge — o obrigatório é praticar e entregar o agente funcionando.

## O que preciso alcançar

- Compreender os requisitos e critérios de avaliação do Challenge Alura Agente.
- Definir uma base de conhecimento utilizando documentos em formato PDF ou CSV.
- Projetar e desenvolver um agente inteligente capaz de responder a perguntas em linguagem natural.
- Organizar e documentar um projeto profissional no GitHub.
- Elaborar um README completo com a arquitetura, instruções de uso e evidências do projeto.
- Implementar uma solução funcional utilizando ferramentas e modelos de inteligência artificial.
- Realizar o deploy (implantação) da aplicação na nuvem utilizando a Oracle Cloud Infrastructure (OCI).

## O cenário do desafio

Fui "contratado" por uma empresa fictícia — que pode ser uma fintech, uma consultoria ou uma startup — que possui muitos documentos internos, como manuais, relatórios, políticas e planilhas. O problema é que as pessoas passam horas buscando informações nesses arquivos. A solução que preciso construir é um agente de inteligência artificial que qualquer colaborador possa usar para fazer perguntas e receber respostas diretas em linguagem natural, sem precisar abrir nenhum documento.

## As três etapas que preciso cumprir

1. **Escolher um documento** (PDF ou CSV) e criar um código que leia e processe esse arquivo, isto é, que minha aplicação entenda o conteúdo dele. Posso usar mais de um documento e personalizar o agente com os arquivos que fizerem mais sentido para o meu projeto.
2. **Construir um agente de IA** que responda perguntas sobre esse documento — por exemplo, "qual foi o produto mais vendido em dezembro de 2015?" ou "quais são as linguagens de programação usadas no back-end da plataforma de vendas da empresa?". O agente precisa buscar a resposta no(s) documento(s) e devolvê-la de forma clara.
3. **Implantar esse agente na nuvem**, na Oracle Cloud Infrastructure (OCI). Isso significa tirar a aplicação do ambiente local e deixá-la acessível publicamente, rodando de fato na nuvem.

Ou seja: um projeto completo, do documento até a implantação.

## Tecnologias que pretendo usar

- **Python** para escrever o código.
- **LangChain** para montar o agente.
- **pypdf** ou **pandas** para ler os documentos.
- Um **modelo de linguagem** (Gemini, ChatGPT, Cohere, Claude ou outro de minha preferência).
- **OCI Compute** para a implantação.

Essas são apenas sugestões do curso, não obrigações — posso usar outra ferramenta se fizer mais sentido para o meu projeto. O importante é que a solução funcione.

## O que preciso entregar

- Código no **GitHub**, em um repositório organizado, com histórico de commits.
- Um **README** bem estruturado, com a arquitetura da solução, exemplos de perguntas e respostas que o agente consegue responder e instruções de execução.
- Um link ou uma captura de tela da aplicação em execução na OCI, comprovando que a implantação funcionou de fato.

## Critérios de avaliação

Para ser aprovado, minha entrega será avaliada considerando se:

- A aplicação funciona.
- A solução como um todo funciona.
- O código está organizado.
- O README explica bem o que foi feito e apresenta uma demonstração do funcionamento.

Resumindo: entregar funcionando e bem documentado.

## Dicas que vou seguir

- Começar sempre pelo **agente local** — fazer funcionar na minha máquina primeiro e só depois pensar na implantação. Se eu tentar fazer o deploy antes, fica difícil saber se um erro é do deploy ou do agente em si.
- Usar o **Google Colab** para prototipar, já que é gratuito e vem com Python configurado.
- Não ficar preso tentando criar uma interface elaborada — não há nenhuma restrição de interface (pode ser uma página web, um popup no navegador ou até um bot no Telegram). O valor do projeto está no agente funcionando, não na camada visual.
- Lembrar que o projeto é meu: posso personalizá-lo como quiser, dar outro nome, usar documentos diferentes dos sugeridos, escolher qualquer tema (não preciso me limitar aos 6 exemplos sugeridos) e trocar as tecnologias sugeridas — nenhuma tecnologia específica é obrigatória (nem Python, nem LangChain, nem LangGraph). Dá para usar n8n (inclusive exportando o projeto em JSON para o repositório), "vibe coding" ou qualquer linguagem/ferramenta que eu já conheça melhor.
- Usar o Git/GitHub **desde o primeiro dia**, commitando o progresso aos poucos. Assim, se algo quebrar depois de uma mudança, consigo voltar para o último commit em que tudo funcionava.
- Se o deploy escolhido tiver limite de tempo/uso no plano gratuito (ex.: N8N, contas grátis em geral), não preciso mantê-lo no ar o tempo todo — basta deixá-lo ativo tempo suficiente para gravar um vídeo ou tirar prints como evidência, e depois posso desligar o serviço.

## Minha documentação (base de conhecimento)

Estas são as empresas fictícias e os respectivos documentos que estou usando como base de conhecimento para o meu agente:

### [Santos Pegasus Soluciones](<Santos Pegasus Soluciones>)

Empresa de tecnologia especializada no desenvolvimento de software escalável sob arquitetura de microsserviços e soluções de Inteligência Artificial (RAG). Destaca-se por seus rigorosos padrões técnicos em engenharia back-end e front-end, garantindo excelência operacional e segurança em infraestruturas de nuvem (OCI).

- [Guia Oficial de Engenharia Back-end (PT-BR)](<Santos Pegasus Soluciones/Santo Pegasus Soluciones_ Guia Oficial de Engenharia Back-end (PT-BR) (1).pdf>)
- [Manual de Onboarding para Desenvolvedores (PT-BR)](<Santos Pegasus Soluciones/Manual de Onboarding para Desenvolvedores — Santo Pegasus Soluciones (PT-BR).pdf>)
- [Arquitetura de Microsserviços e Mapa de Domínios (PT-BR)](<Santos Pegasus Soluciones/Arquitetura de Microsserviços e Mapa de Domínios - Santo Pegasus (PT-BR).pdf>)
- [Guia Oficial de Engenharia Front-end (PT-BR)](<Santos Pegasus Soluciones/Guia Oficial de Engenharia Front-end — Santo Pegasus Soluciones (PT-BR).pdf>)
- [Manual Maestro de Resiliência e Resposta a Incidentes (v7.0)](<Santos Pegasus Soluciones/Manual Maestro de Resiliência e Resposta a Incidentes — Santo Pegasus (v7.0).pdf>)

### [BimBam Buy](<BimBam Buy>)

E-commerce multiplataforma focado na experiência de compra digital ágil e segura. Destaca-se por um modelo de negócio orientado ao cliente, com políticas robustas de reembolso, um programa de afiliados dinâmico e uma infraestrutura logística otimizada para garantir entregas rápidas e suporte constante ao usuário final.

- [FAQ Métodos de Pagamento (PT-BR)](<BimBam Buy/FAQ Métodos de Pagamento - BimBam Buy (PT-BR).pdf>)
- [Manual de Garantia (PT-BR)](<BimBam Buy/Manual de Garantia - BimBam Buy (PT-BR).pdf>)
- [Guia de Envios (PT-BR)](<BimBam Buy/Guia de Envios - BimBam Buy (PT-BR).pdf>)
- [Programa de Afiliados (PT-BR)](<BimBam Buy/Programa de Afiliados - BimBam Buy (PT-BR).pdf>)
- [Política de Reembolsos e Devoluções (PT-BR)](<BimBam Buy/Política de Reembolsos e Devoluções - BimBam Buy (PT-BR).pdf>)

### [Mercado Central 24h](<Mercado Central 24h>)

Supermercado moderno de operação contínua (24/7) que integra a experiência de loja física com serviços de delivery e aplicativo próprio. Seu foco principal é a eficiência operacional na gestão de estoque e uma forte política de atendimento ao cliente, impulsionada pelo programa de fidelidade "Cliente VIP Central".

- [Política de Atendimento, Trocas e Devoluções (PT-BR)](<Mercado Central 24h/Política de Atendimento, Trocas e Devoluções — Mercado Central 24h (PT-BR).pdf>)
- [Manual de Fornecedores e Política de Compras (PT-BR)](<Mercado Central 24h/Manual de Fornecedores e Política de Compras — Mercado Central 24h (PT-BR).pdf>)
- [Regulamento Interno e Procedimentos Operacionais (PT-BR)](<Mercado Central 24h/Regulamento Interno e Procedimentos Operacionais — Mercado Central 24h (PT-BR).pdf>)
- [Perguntas Frequentes (FAQ) — Clientes e Funcionários (PT-BR)](<Mercado Central 24h/Perguntas Frequentes (FAQ) — Clientes e Funcionários — Mercado Central 24h (PT-BR).pdf>)

> Lembrando que a escolha do documento é livre — posso adaptar para o contexto que mais me interessar, desde que o projeto resolva um problema real e demonstre minha capacidade de construir uma solução funcional com IA.

## Checklist de entregáveis

### Repositório no GitHub

- [x] Repositório público no GitHub com o código-fonte do projeto.
- [x] Histórico de commits que reflita o desenvolvimento do projeto.
- [x] Estrutura organizada e fácil de compreender.

### Documentação (README)

- [x] Descrição geral do projeto.
- [x] Arquitetura da solução implementada.
- [x] Tecnologias e ferramentas utilizadas.
- [x] Instruções para executar o projeto.
- [x] Exemplos de perguntas que o agente consegue responder.
- [x] Exemplos de respostas geradas pelo agente.

### Agente inteligente funcional

- [x] Agente de IA capaz de responder a perguntas baseadas no conteúdo de um documento (PDF ou CSV).
- [x] Código para ler e processar o documento utilizado como fonte de informação.

### Evidência do deploy

- [x] Link público da aplicação em funcionamento **ou**
- [x] Vídeo ou captura de tela (print) que mostre a aplicação sendo executada corretamente na nuvem (OCI ou outra plataforma escolhida).

A evidência (link, vídeo ou print) deve ficar registrada no README — no início ou no fim, tanto faz. Como o deploy não precisa ficar no ar para sempre, essa evidência é o que garante a comprovação mesmo depois de eu desligar o serviço.

## Como vou fazer a entrega final

- Verificar a URL do meu projeto antes de enviar — o sistema aceita **apenas URLs do GitHub** (a URL do repositório, e não a URL da aplicação deployada, tipo Streamlit/Render/Vercel/OCI).
- O repositório precisa ser **público** — se for privado, ninguém consegue avaliar o projeto.
- Depois de colocar a URL do challenge, baixar a badge e só então enviar o projeto.
- Tenho **cinco tentativas** para enviar a URL do repositório na plataforma. Se eu enviar mais de uma vez, **vale a última entrega enviada** — tanto se eu atualizar o mesmo link quanto se trocar por outro repositório.
- Posso continuar editando e commitando no repositório mesmo depois do prazo final — o que importa é que, até o prazo (19/08 às 23:59), o projeto já esteja funcionando, documentado e com a evidência do deploy. Só não posso enviar depois disso um repositório vazio ou sem essas evidências.
- Depois de baixar a insígnia, compartilhar no LinkedIn e nas redes sociais, marcando **#Alura** e **#oraclenexteducation**.

## Dúvidas que tirei na live de Q&A

Anotações das perguntas que outros alunos fizeram na live e que me ajudaram a entender melhor as regras do desafio:

- **O tema da documentação precisa ser um dos seis sugeridos?** Não. Os seis temas (e-commerce, SaaS, logística, clínica, plataforma educativa, fintech) são só sugestões de temas populares e fáceis de entender — posso escolher qualquer outro contexto, inclusive algo pessoal (ex.: um agente para a loja de um amigo ou para pontos turísticos da minha cidade).
- **Posso fazer o desafio com n8n (inclusive "vibe coding")?** Sim. Nesse caso, dá para exportar o projeto do n8n em formato JSON e subir esse arquivo no repositório do GitHub.
- **Preciso programar em Python?** Não é obrigatório. Python, LangChain, RAG, LangGraph etc. são só sugestões porque são o conteúdo ensinado no curso — o que importa é entregar o agente funcionando, então posso usar a linguagem/ferramenta que eu já conheço melhor.
- **A interface gráfica precisa seguir algum padrão?** Não há restrição — pode ser uma página web, um popup simples no navegador ou até um bot no Telegram. O foco da avaliação é a funcionalidade do agente, não o design.
- **O README pode ser em português?** Sim, não há restrição de idioma.
- **O quadro Trello do desafio é obrigatório?** Não, é só uma sugestão de organização pessoal (quebrar o projeto em etapas menores) para quem não sabe por onde começar. Posso copiá-lo e adaptar ao meu próprio ritmo, ou nem usar.
- **Preciso assistir a todas as formações/trilhas antes de fazer o Challenge?** Não. As formações são conteúdo complementar; posso estudar no meu ritmo e começar o Challenge assim que me sentir confiante para construir o agente. As trilhas mais relacionadas ao desafio são Nivelamento (para quem é iniciante), Desenvolvimento com IA Generativa e Engenharia de Agentes e Automação com IA — inclusive existe um curso específico chamado "RAG e Agentes de IA" que constrói um agente com RAG passo a passo, útil mas não obrigatório.
- **O que conta se eu enviar o link do repositório mais de uma vez?** Vale a última entrega enviada dentro do prazo (tenho até 5 tentativas).
- **Posso editar o código depois de entregar, mesmo após o prazo final?** Sim, o repositório é meu — posso continuar melhorando, fazendo novos commits e até trocando a ferramenta de deploy depois de entregar. O que conta para a avaliação é o que já foi entregue dentro do prazo.
- **A aplicação precisa ficar no ar até a correção?** Não. Como muitas ferramentas gratuitas têm limite de tempo, basta ter gravado um vídeo ou tirado prints da aplicação funcionando; depois posso desligar o serviço tranquilamente.
- **E se o cartão não for aceito para o OCI Always Free?** Nesse caso, posso contatar o suporte da Oracle diretamente ou usar outra plataforma de deploy (Streamlit Community Cloud, Render, Vercel etc.) — não sou obrigado a usar OCI.
