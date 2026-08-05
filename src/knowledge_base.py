"""Índice vetorial FAISS em memória: criação, adição e remoção de documentos."""

import uuid

from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_core.documents import Document


def build_vectorstore(chunks: list[Document], embeddings) -> FAISS:
    return FAISS.from_documents(
        chunks,
        embeddings,
        distance_strategy=DistanceStrategy.COSINE,
    )


def add_documents(vectorstore: FAISS, chunks: list[Document]) -> list[str]:
    ids = [str(uuid.uuid4()) for _ in chunks]
    vectorstore.add_documents(chunks, ids=ids)
    return ids


def remove_documents(vectorstore: FAISS, ids: list[str]) -> None:
    vectorstore.delete(ids=ids)
