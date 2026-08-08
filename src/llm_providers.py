"""Fábricas de embeddings/chat model por provedor (OpenAI, Google Gemini ou Cohere)."""

from langchain_cohere import ChatCohere, CohereEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from src.config import PROVIDERS


def get_embeddings(provider: str, api_key: str):
    model = PROVIDERS[provider]["embedding_model"]
    if provider == "OpenAI":
        return OpenAIEmbeddings(model=model, api_key=api_key)
    if provider == "Google Gemini":
        return GoogleGenerativeAIEmbeddings(model=model, google_api_key=api_key)
    if provider == "Cohere":
        return CohereEmbeddings(model=model, cohere_api_key=api_key)
    raise ValueError(f"Provedor desconhecido: {provider}")


def get_chat_model(provider: str, api_key: str):
    model = PROVIDERS[provider]["chat_model"]
    if provider == "OpenAI":
        return ChatOpenAI(model=model, api_key=api_key, temperature=0.2)
    if provider == "Google Gemini":
        return ChatGoogleGenerativeAI(model=model, google_api_key=api_key, temperature=0.2)
    if provider == "Cohere":
        return ChatCohere(model=model, cohere_api_key=api_key, temperature=0.2)
    raise ValueError(f"Provedor desconhecido: {provider}")
