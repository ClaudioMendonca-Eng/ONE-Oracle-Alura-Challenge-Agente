import os
import uuid
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

from src.config import PROVIDERS, SUGGESTED_QUESTIONS
from src.document_loader import (
    extract_csv_documents,
    extract_pdf_documents,
    load_preloaded_documents,
    split_documents,
)
from src.knowledge_base import add_documents, build_vectorstore, remove_documents
from src.llm_providers import get_chat_model, get_embeddings
from src.rag_agent import answer_question, suggest_followups

load_dotenv()

st.set_page_config(page_title="Assistente BimBam Buy",
                   page_icon="🛍️", layout="centered")


@st.cache_data(show_spinner=False)
def _load_preloaded_chunks():
    return load_preloaded_documents()


defaults = {
    "provider": next(iter(PROVIDERS)),
    "api_key": os.getenv("OPENAI_API_KEY") or os.getenv("GOOGLE_API_KEY") or "",
    "embeddings": None,
    "chat_model": None,
    "vectorstore": None,
    "kb_ready": False,
    "uploaded_docs": {},
    "conversations": {},
    "active_conversation_id": None,
    "pending_question": None,
}
for key, value in defaults.items():
    st.session_state.setdefault(key, value)


def _new_conversation() -> str:
    conversation_id = str(uuid.uuid4())
    st.session_state.conversations[conversation_id] = {"title": "Nova conversa", "messages": []}
    st.session_state.active_conversation_id = conversation_id
    return conversation_id


if (
    st.session_state.active_conversation_id is None
    or st.session_state.active_conversation_id not in st.session_state.conversations
):
    _new_conversation()

messages = st.session_state.conversations[st.session_state.active_conversation_id]["messages"]

# Enquanto uma pergunta está sendo respondida, chips, input e a barra lateral ficam
# desabilitados — sem isso, dava para trocar de conversa ou clicar em outra sugestão
# durante o streaming e deixar a resposta pendente órfã.
answering = st.session_state.pending_question is not None

with st.sidebar:
    st.caption("Histórico de conversas")
    if st.button("Nova conversa", icon=":material/add:", width="stretch", disabled=answering):
        _new_conversation()
        st.rerun()

    for conversation_id in reversed(list(st.session_state.conversations)):
        conversation = st.session_state.conversations[conversation_id]
        is_active = conversation_id == st.session_state.active_conversation_id
        switch_col, delete_col = st.columns([5, 1], vertical_alignment="center")
        if switch_col.button(
            conversation["title"],
            key=f"switch_{conversation_id}",
            type="primary" if is_active else "secondary",
            width="stretch",
            disabled=answering,
        ):
            st.session_state.active_conversation_id = conversation_id
            st.rerun()
        if delete_col.button(
            ":material/delete:",
            key=f"delete_{conversation_id}",
            help="Excluir conversa",
            width="content",
            disabled=answering,
        ):
            del st.session_state.conversations[conversation_id]
            if conversation_id == st.session_state.active_conversation_id:
                remaining = list(st.session_state.conversations)
                st.session_state.active_conversation_id = remaining[-1] if remaining else None
            st.rerun()

    st.divider()
    st.caption(
        "**BimBam Buy Comércio Eletrônico Ltda.**  \n"
        "CNPJ (fictício): 12.345.678/0001-90  \n"
        ":material/location_on: Av. Fictícia, 1234 – São Paulo/SP  \n"
        ":material/mail: suporte@bimbambuy.example  \n"
        ":material/call: (11) 4000-0000"
    )
    st.caption(
        f"© {datetime.now().year} BimBam Buy · Empresa fictícia criada para fins "
        "educacionais (Challenge Alura/ONE)."
    )


@st.dialog("Configurações")
def settings_dialog():
    provider_options = list(PROVIDERS.keys())
    provider = st.selectbox(
        "Provedor de LLM",
        provider_options,
        index=provider_options.index(st.session_state.provider),
        disabled=st.session_state.kb_ready,
        help="Depois que a base de conhecimento é criada, o provedor fica travado nesta sessão.",
    )
    api_key = st.text_input(
        "Chave de API",
        value=st.session_state.api_key,
        type="password",
        help=PROVIDERS[provider]["api_key_help"],
    )

    st.divider()
    st.caption("Documentos adicionais desta sessão (opcional)")
    uploaded_files = st.file_uploader(
        "Anexar PDF ou CSV", type=["pdf", "csv"], accept_multiple_files=True
    )

    for name, ids in list(st.session_state.uploaded_docs.items()):
        row_label, row_button = st.columns([4, 1])
        row_label.write(f"📄 {name}")
        if row_button.button("🗑️", key=f"remove_{name}"):
            remove_documents(st.session_state.vectorstore, ids)
            del st.session_state.uploaded_docs[name]
            st.rerun()

    if st.button("Salvar", type="primary", width="stretch"):
        if not api_key:
            st.error("Informe uma chave de API.")
            return
        try:
            with st.spinner("Configurando o agente..."):
                if not st.session_state.kb_ready:
                    embeddings = get_embeddings(provider, api_key)
                    chunks = _load_preloaded_chunks()
                    st.session_state.vectorstore = build_vectorstore(
                        chunks, embeddings)
                    st.session_state.embeddings = embeddings
                    st.session_state.provider = provider
                    st.session_state.kb_ready = True

                st.session_state.api_key = api_key
                st.session_state.chat_model = get_chat_model(
                    st.session_state.provider, api_key)

                for uploaded_file in uploaded_files or []:
                    if uploaded_file.name in st.session_state.uploaded_docs:
                        continue
                    data = uploaded_file.read()
                    if uploaded_file.name.lower().endswith(".pdf"):
                        docs = extract_pdf_documents(data, uploaded_file.name)
                    else:
                        docs = extract_csv_documents(data, uploaded_file.name)
                    chunks = split_documents(docs)
                    ids = add_documents(st.session_state.vectorstore, chunks)
                    st.session_state.uploaded_docs[uploaded_file.name] = ids
        except Exception as exc:  # chave inválida, erro de rede, etc.
            st.error(f"Não foi possível configurar o agente: {exc}")
            return
        st.rerun()


with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
    st.title("🛍️ Assistente BimBam Buy")
    if st.button(":material/settings:", help="Configurações", width="content"):
        settings_dialog()

st.caption(
    "Tire dúvidas sobre pagamento, garantia, envio, devoluções e o programa de "
    "afiliados da BimBam Buy."
)

if not st.session_state.kb_ready:
    st.info(
        "Abra as configurações acima e informe sua chave de API para começar.",
        icon=":material/key:",
    )

for turn in messages:
    avatar = ":material/storefront:" if turn["role"] == "assistant" else None
    with st.chat_message(turn["role"], avatar=avatar):
        st.write(turn["content"])
        if turn.get("sources"):
            st.caption(":material/description: Fontes: " + ", ".join(turn["sources"]))

if not messages:
    suggestion_caption = "Experimente perguntar:"
    suggestion_pool = SUGGESTED_QUESTIONS
else:
    last_turn = messages[-1]
    asked = {m["content"] for m in messages if m["role"] == "user"}
    suggestion_pool = suggest_followups(last_turn.get("sources") or [], asked)
    suggestion_caption = "Continue perguntando:"

with st.bottom:
    suggestion = None
    if st.session_state.kb_ready and suggestion_pool:
        st.caption(suggestion_caption)
        # Chave muda a cada turno para descartar a seleção anterior — sem isso, o chip
        # clicado continuaria "selecionado" no rerun seguinte e reenviaria a mesma
        # pergunta indefinidamente (question = chat_input or suggestion).
        suggestion = st.pills(
            "Sugestões de perguntas",
            options=[q["text"] for q in suggestion_pool],
            format_func=lambda text: next(
                f"{q['icon']} {text}" for q in suggestion_pool if q["text"] == text
            ),
            label_visibility="collapsed",
            selection_mode="single",
            disabled=answering,
            key=f"suggestions_{len(messages)}",
        )

    question = st.chat_input(
        "Digite sua pergunta..." if st.session_state.kb_ready else "Configure sua chave de API na engrenagem acima",
        disabled=not st.session_state.kb_ready or answering,
        submit_mode="disable",
    ) or suggestion

if question and not answering:
    messages.append({"role": "user", "content": question})
    conversation = st.session_state.conversations[st.session_state.active_conversation_id]
    if conversation["title"] == "Nova conversa" and len(messages) == 1:
        conversation["title"] = question if len(question) <= 42 else question[:39] + "..."
    st.session_state.pending_question = question
    st.rerun()

if st.session_state.pending_question:
    with st.chat_message("assistant", avatar=":material/storefront:"):
        with st.spinner("Consultando a base de conhecimento..."):
            result = answer_question(
                st.session_state.vectorstore,
                st.session_state.chat_model,
                st.session_state.pending_question,
                messages[:-1],
            )
        if result["stream"] is None:
            st.write(result["answer"])
            answer = result["answer"]
        else:
            answer = st.write_stream(result["stream"])
        if result["sources"]:
            st.caption(":material/description: Fontes: " + ", ".join(result["sources"]))

    messages.append({"role": "assistant", "content": answer, "sources": result["sources"]})
    st.session_state.pending_question = None
    # Sem isso, o chip de sugestão clicado nesta rodada continuaria "selecionado" na
    # tela até a próxima interação, porque o bloco de sugestões acima já foi desenhado
    # (com a contagem antiga de mensagens) antes de chegarmos aqui.
    st.rerun()
