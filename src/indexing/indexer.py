# src/indexing/indexer.py

import os
from config.config import (
    HOLDINGS_CSV,
    TRADES_CSV,
    EMBEDDING_MODEL_NAME,
    VECTOR_STORE_DIR
)

from src.ingestion.load_data import load_all_data
from src.ingestion.document_builder import build_documents
from src.embeddings.embedder import TextEmbedder
from src.embeddings.vector_store import FaissVectorStore


def index_exists() -> bool:
    return (
        (VECTOR_STORE_DIR / "index.faiss").exists()
        and (VECTOR_STORE_DIR / "documents.pkl").exists()
        and (VECTOR_STORE_DIR / "funds.pkl").exists()
    )


def build_or_load_index():
    """
    This function is SAFE to call multiple times.
    Indexing happens only once.
    """

    embedder = TextEmbedder(EMBEDDING_MODEL_NAME)

    if index_exists():
        vector_store = FaissVectorStore(
            dim=embedder.embed_texts(["test"]).shape[1],
            index_path=VECTOR_STORE_DIR
        )
        vector_store.load()
        import pickle
        with open(VECTOR_STORE_DIR / "funds.pkl", "rb") as f:
            unique_funds = pickle.load(f)
        return vector_store, embedder, unique_funds

    # --------- Build index (first run only) ---------

    df = load_all_data(HOLDINGS_CSV, TRADES_CSV)
    documents = build_documents(df)

    texts = [doc["text"] for doc in documents]
    embeddings = embedder.embed_texts(texts)

    vector_store = FaissVectorStore(
        dim=embeddings.shape[1],
        index_path=VECTOR_STORE_DIR
    )

    vector_store.add(embeddings, documents)
    vector_store.save()

    fund_column = None
    for col in df.columns:
        col_lower = col.lower()
        if "fund" in col_lower or "portfolio" in col_lower:
            fund_column = col
            break
    
    unique_funds = sorted(df[fund_column].dropna().unique().tolist()) if fund_column else []

    import pickle
    with open(VECTOR_STORE_DIR / "funds.pkl", "wb") as f:
        pickle.dump(unique_funds, f)

    return vector_store, embedder, unique_funds
