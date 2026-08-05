"""Extração de texto de PDF/CSV (em memória) e divisão em chunks para embeddings."""

import io

import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from src.config import CHUNK_OVERLAP, CHUNK_SIZE, DOCS_DIR

_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)


def extract_pdf_documents(source, filename: str) -> list[Document]:
    """Extrai um Document por página. `source` é um path ou bytes (upload em memória)."""
    reader = PdfReader(io.BytesIO(source) if isinstance(source, bytes) else source)
    pages = ((page_number, page.extract_text() or "") for page_number, page in enumerate(reader.pages, start=1))
    return [
        Document(page_content=text, metadata={"source": filename, "page": page_number})
        for page_number, text in pages
        if text.strip()
    ]


def extract_csv_documents(source, filename: str) -> list[Document]:
    """Extrai um Document por linha de um CSV. `source` é um path ou bytes (upload)."""
    df = pd.read_csv(io.BytesIO(source) if isinstance(source, bytes) else source)
    return [
        Document(
            page_content=row.to_string(),
            metadata={"source": filename, "row": row_index},
        )
        for row_index, row in df.iterrows()
    ]


def split_documents(documents: list[Document]) -> list[Document]:
    return _splitter.split_documents(documents)


def load_preloaded_documents() -> list[Document]:
    """Varre docs/BimBam Buy/*.pdf, extrai o texto e retorna os chunks prontos para embedding."""
    documents: list[Document] = []
    for pdf_path in sorted(DOCS_DIR.glob("*.pdf")):
        documents.extend(extract_pdf_documents(pdf_path, pdf_path.name))
    return split_documents(documents)
