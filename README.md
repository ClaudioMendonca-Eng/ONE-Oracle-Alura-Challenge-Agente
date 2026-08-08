# Assistente BimBam Buy — ONE Oracle Alura Challenge Agente



| ![Alura - ONE Oracle Next Education](/docs/imagens/logo_alura_one.png) |
|:---:|
| Agente de IA com RAG (Retrieval-Augmented Generation) que responde, em linguagem natural, dúvidas sobre as políticas da **BimBam Buy** — um e-commerce fictício —, com base exclusivamente nos documentos internos da empresa (pagamento, garantia, envio,devoluções e programa de afiliados). Projeto desenvolvido para o **Challenge Alura Agente**, do programa [Oracle Next Education (ONE)](docs/descricao_curso.md). |
| <div align="center"> <a href="https://cursos.alura.com.br/user/claudiomendonca" target="_blank"> <img src="https://img.shields.io/badge/Alura.com.br-16537E?style=for-the-badge&logo=alura&logoColor=white" alt="Alura" style="margin-bottom: 5px;" /> </a> </div> |



> Entendimento completo do desafio, das decisões de projeto e do raciocínio por trás de
> cada escolha técnica: [docs/estudo_de_caso.md](docs/estudo_de_caso.md) e
> [docs/challenge_alura_agente.md](docs/challenge_alura_agente.md).

## O problema

Colaboradores perdem tempo procurando informações em manuais e políticas internas. A
BimBam Buy tem 5 documentos em PDF cobrindo pagamento, garantia, envio, afiliados e
reembolsos — e várias perguntas reais só fazem sentido cruzando mais de um desses
documentos (ex.: um defeito de fabricação passa primeiro pela garantia, só vai para
devolução se a garantia não cobrir). O agente existe para responder essas perguntas
diretamente, sem que ninguém precise abrir um PDF.

## Arquitetura

```mermaid
flowchart LR
    subgraph Base["Base de conhecimento"]
        PDF["5 PDFs pré-carregados\ndocs/BimBam Buy/"]
        Upload["Upload opcional\n(PDF/CSV da sessão)"]
    end

    PDF --> Split["Split em chunks"]
    Upload --> Split
    Split --> Embed["Embeddings\n(OpenAI ou Gemini)"]
    Embed --> FAISS["Índice FAISS\nem memória (cosseno)"]

    Pergunta["Pergunta do usuário"] --> Saudacao{"É só uma\nsaudação?"}
    Saudacao -->|"sim"| RespostaSaudacao["Resposta fixa de boas-vindas\n(sem chamar o LLM)"]
    Saudacao -->|"não"| Retrieval["Busca por similaridade\n(top-k)"]
    FAISS --> Retrieval
    Retrieval -->|"score < limiar"| Recusa["Recusa padrão\n(sem chamar o LLM)"]
    Retrieval -->|"score >= limiar"| Prompt["Monta prompt\n(system prompt + contexto + pergunta)"]
    Prompt --> LLM["LLM do provedor escolhido\n(streaming)"]
    LLM --> Resposta["Resposta + fontes"]
```

Tudo roda **em memória, por sessão do navegador** — não há banco de dados. Reiniciar o
app só custa reprocessar os 5 PDFs pré-carregados (rápido). A chave de API do usuário
fica só em `st.session_state`, nunca é salva em arquivo, banco ou log. Cada sessão pode
ter várias conversas em paralelo (barra lateral, ao estilo ChatGPT) — todas somem ao
fechar a aba, junto com o resto do estado da sessão.

O guardrail principal não é o prompt — é a camada de recuperação: se a melhor
similaridade encontrada no índice ficar abaixo de um limiar mínimo, o agente recusa a
pergunta **sem sequer chamar o LLM**, o que evita que o modelo "invente" uma resposta de
conhecimento geral para perguntas fora do escopo da BimBam Buy. O system prompt reforça
essa regra em toda chamada e trata qualquer texto do usuário (ou dos documentos) como
dado, nunca como instrução — mitigação contra tentativas de prompt injection / jailbreak.
Detalhes completos das ameaças consideradas e dos testes de "red team" planejados estão
em [docs/estudo_de_caso.md](docs/estudo_de_caso.md#segurança-e-guardrails-do-agente).

### Estrutura do código

```
app.py                      # interface Streamlit (chat multi-conversa + modal de config.)
src/
  config.py                 # system prompt, recusa, saudação, sugestões, limiares, provedores
  document_loader.py        # extração de texto (PDF/CSV) e chunking
  llm_providers.py          # fábricas de embeddings/chat model (OpenAI / Gemini)
  knowledge_base.py         # índice FAISS em memória (build / add / remove)
  rag_agent.py              # guardrail de similaridade + streaming + sugestões de acompanhamento
docs/BimBam Buy/            # base de conhecimento pré-carregada (5 PDFs)
```

## Tecnologias utilizadas

- **Python 3.11**
- **Streamlit** — interface de chat e modal de configuração (`st.dialog`)
- **LangChain** (`langchain`, `langchain-community`, `langchain-openai`,
  `langchain-google-genai`) — orquestração do RAG
- **FAISS** (`faiss-cpu`) — índice vetorial em memória
- **pypdf** e **pandas** — leitura de PDF e CSV
- **OpenAI** ou **Google Gemini** — modelo de linguagem e de embeddings, à escolha do
  usuário (chave própria, informada em tempo de uso — nunca fica no código)
- **Dev Container** (VS Code) — ambiente de desenvolvimento reprodutível

## Como executar

Pré-requisito: uma chave de API da **OpenAI** ou do **Google AI Studio (Gemini)** —
gratuita para testes na maioria dos provedores.

```bash
pip install -r requirements.txt
streamlit run app.py
```

O app abre em `http://localhost:8501`. Ao abrir, clique no ícone de configurações (⚙️) no
topo, escolha o provedor, cole sua chave de API e clique em **Salvar** — os 5 documentos
da BimBam Buy são indexados automaticamente nesse momento. Depois é só perguntar no chat
(a resposta chega em streaming, palavra por palavra) ou clicar em uma das sugestões de
pergunta exibidas acima do campo de texto. Opcionalmente, na mesma janela de
configuração, é possível anexar PDFs ou CSVs extras para a sessão (não são salvos em
disco, somem ao fechar a aba).

A barra lateral guarda o histórico de conversas da sessão — dá para abrir quantas
conversas paralelas quiser ("Nova conversa"), alternar entre elas e excluir as que não
interessam mais. Nada disso é persistido: fechar a aba apaga tudo.

Se estiver usando o Dev Container do VS Code (`.devcontainer/`), as dependências já são
instaladas automaticamente e a porta 8501 já vem encaminhada.

## Exemplos de perguntas que o agente responde

Baseadas no conteúdo real dos 5 documentos da BimBam Buy — a resposta abaixo é a
referência esperada de acordo com as políticas, para comparação depois de rodar o agente
com uma chave real (ver seção de evidências abaixo):

| Pergunta | Resposta de referência |
|---|---|
| Quais métodos de pagamento a BimBam Buy aceita? | Cartão de crédito, cartão de débito, transferência bancária/PIX, dinheiro em pontos habilitados (ex.: Boleto), carteiras digitais e parcelamento, variando por país. |
| Quanto tempo demora um reembolso? | De 5 a 10 dias úteis a partir da aprovação, dependendo do método de pagamento e do país. |
| Quantos dias tenho para desistir de uma compra? | 10 dias corridos após o recebimento do pedido, desde que o produto esteja sem uso. |
| O que faço se meu produto chegou danificado? | Relatar em até 48 horas após a entrega, com evidência fotográfica ou em vídeo. |
| A garantia cobre dano por queda do produto? | Não — dano por queda é uma exclusão explícita, tratado como dano acidental. |
| Meu produto quebrou sozinho depois de um mês de uso, o que eu faço? | Primeiro é avaliado pelo Manual de Garantia; se confirmado defeito de fabricação, a resolução é reparo, troca ou reembolso (cruza Garantia + Reembolsos). |
| Se o cliente de um afiliado devolver o produto, o afiliado perde a comissão? | A comissão pode ser revertida ou ajustada conforme a política interna e a elegibilidade final da venda (cruza Afiliados + Reembolsos). |

Mais exemplos, incluindo perguntas fora de escopo que o agente deve recusar (ex.: "qual a
capital da França?") e tentativas de jailbreak, estão em
[docs/estudo_de_caso.md](docs/estudo_de_caso.md#exemplos-de-perguntas-que-o-agente-deve-responder).

## Status do projeto

- [x] Leitura e processamento dos documentos (PDF pré-carregados + upload opcional)
- [x] Agente de IA funcional com RAG e guardrails de segurança
- [x] Interface de chat local (Streamlit)
- [x] Validação das respostas reais do agente com uma chave de API (substituir as
      respostas de referência acima por transcrições reais)
- [ ] Deploy na nuvem implementado no **Streamlit Cloud** 
- [ ] Evidência do deploy (link ou captura de tela)

### Evidência de implantação

_Pendente — será adicionada aqui após o deploy._
