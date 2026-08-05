import os

import streamlit as st
from dotenv import load_dotenv

from src.config import PROVIDERS
from src.document_loader import (
    extract_csv_documents,
    extract_pdf_documents,
    load_preloaded_documents,
    split_documents,
)
from src.knowledge_base import add_documents, build_vectorstore, remove_documents
from src.llm_providers import get_chat_model, get_embeddings
from src.rag_agent import answer_question

load_dotenv()

st.set_page_config(page_title="Assistente BimBam Buy", page_icon="🛍️", layout="centered")

defaults = {
    "provider": next(iter(PROVIDERS)),
    "api_key": os.getenv("OPENAI_API_KEY") or os.getenv("GOOGLE_API_KEY") or "",
    "embeddings": None,
    "chat_model": None,
    "vectorstore": None,
    "kb_ready": False,
    "uploaded_docs": {},
    "messages": [],
}
for key, value in defaults.items():
    st.session_state.setdefault(key, value)


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

    if st.button("Salvar", type="primary", use_container_width=True):
        if not api_key:
            st.error("Informe uma chave de API.")
            return
        try:
            with st.spinner("Configurando o agente..."):
                if not st.session_state.kb_ready:
                    embeddings = get_embeddings(provider, api_key)
                    chunks = load_preloaded_documents()
                    st.session_state.vectorstore = build_vectorstore(chunks, embeddings)
                    st.session_state.embeddings = embeddings
                    st.session_state.provider = provider
                    st.session_state.kb_ready = True

                st.session_state.api_key = api_key
                st.session_state.chat_model = get_chat_model(st.session_state.provider, api_key)

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


header_col, settings_col = st.columns([6, 1])
header_col.title("🛍️ Assistente BimBam Buy")
if settings_col.button("⚙️", use_container_width=True, help="Configurações"):
    settings_dialog()

st.caption(
    "Tire dúvidas sobre pagamento, garantia, envio, devoluções e o programa de "
    "afiliados da BimBam Buy."
)

if not st.session_state.kb_ready:
    st.info("Abra a engrenagem (⚙️) acima e configure sua chave de API para começar.")

for turn in st.session_state.messages:
    with st.chat_message(turn["role"]):
        st.write(turn["content"])
        if turn.get("sources"):
            st.caption("Fontes: " + ", ".join(turn["sources"]))

question = st.chat_input(
    "Digite sua pergunta..." if st.session_state.kb_ready else "Configure sua chave de API na engrenagem acima",
    disabled=not st.session_state.kb_ready,
)
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Consultando a base de conhecimento..."):
            result = answer_question(
                st.session_state.vectorstore,
                st.session_state.chat_model,
                question,
                st.session_state.messages[:-1],
            )
        st.write(result["answer"])
        if result["sources"]:
            st.caption("Fontes: " + ", ".join(result["sources"]))

    st.session_state.messages.append(
        {"role": "assistant", "content": result["answer"], "sources": result["sources"]}
    )
