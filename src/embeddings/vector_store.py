import faiss
import numpy as np
import pickle
from pathlib import Path
from typing import List, Dict


class FaissVectorStore:
    def __init__(self, dim: int, index_path: Path):
        self.dim = dim
        self.index_path = index_path
        self.index = faiss.IndexFlatIP(dim)  # cosine similarity (with normalized vectors)
        self.documents: List[Dict] = []

    def add(self, embeddings: np.ndarray, documents: List[Dict]):
        if len(embeddings) != len(documents):
            raise ValueError("Embeddings and documents size mismatch")

        self.index.add(embeddings)
        self.documents.extend(documents)

    def save(self):
        self.index_path.mkdir(parents=True, exist_ok=True)

        faiss.write_index(self.index, str(self.index_path / "index.faiss"))
        with open(self.index_path / "documents.pkl", "wb") as f:
            pickle.dump(self.documents, f)

    def load(self):
        self.index = faiss.read_index(str(self.index_path / "index.faiss"))
        with open(self.index_path / "documents.pkl", "rb") as f:
            self.documents = pickle.load(f)

    def search(self, query_embedding: np.ndarray, top_k: int):
        """
        Returns:
        [
            {
                "text": "...",
                "metadata": {...},
                "score": 0.82
            }
        ]
        """
        scores, indices = self.index.search(query_embedding, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            doc = self.documents[idx]
            results.append(
                {
                    "text": doc["text"],
                    "metadata": doc["metadata"],
                    "score": float(score)
                }
            )

        return results
