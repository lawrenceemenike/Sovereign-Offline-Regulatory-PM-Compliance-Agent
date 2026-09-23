import os
import json
import logging
from typing import List, Dict, Any, Optional
import numpy as np
import faiss
import httpx

logger = logging.getLogger("lexguard.rag")
logger.setLevel(logging.INFO)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
VECTOR_STORE_DIR = os.getenv("VECTOR_STORE_DIR", "./backend/data/vector_store")
VECTOR_DIM = 768


class LocalEmbeddingProvider:
    """Zero-cloud local embedding provider with Ollama primary and deterministic fallback."""

    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = OLLAMA_EMBED_MODEL):
        self.base_url = base_url
        self.model = model

    def get_embedding(self, text: str) -> np.ndarray:
        try:
            with httpx.Client(timeout=10.0) as client:
                res = client.post(
                    f"{self.base_url}/api/embeddings",
                    json={"model": self.model, "prompt": text},
                )
                if res.status_code == 200:
                    data = res.json()
                    vec = np.array(data.get("embedding", []), dtype=np.float32)
                    if len(vec) == VECTOR_DIM:
                        norm = np.linalg.norm(vec)
                        return vec / (norm + 1e-9)
        except Exception as e:
            logger.warning(f"Ollama embedding unavailable ({e}), using sovereign deterministic vector fallback.")

        # Deterministic offline feature projection fallback
        return self._deterministic_vector(text)

    def _deterministic_vector(self, text: str) -> np.ndarray:
        """Deterministic 768-dim pseudo-semantic hash projection for offline reliability."""
        import hashlib
        vec = np.zeros(VECTOR_DIM, dtype=np.float32)
        words = text.lower().split()
        for idx, word in enumerate(words):
            h = int(hashlib.sha256(word.encode()).hexdigest(), 16)
            pos = h % VECTOR_DIM
            weight = 1.0 / (idx + 1) ** 0.5
            sign = 1.0 if (h >> 8) % 2 == 0 else -1.0
            vec[pos] += sign * weight

        # Regulatory keyword boosting
        keywords = {
            "ndpr": 10, "privacy": 11, "protection": 12, "consent": 13, "breach": 14,
            "petroleum": 20, "nmdpra": 21, "pipeline": 22, "flare": 23, "crude": 24,
            "governor": 30, "land": 31, "occupancy": 32, "eia": 33, "permit": 34,
            "sovereign": 40, "cloud": 41, "nitda": 42, "biometrics": 43, "residency": 44,
            "seed": 50, "fertilizer": 51, "nasc": 52, "nafdac": 53, "agriculture": 54
        }
        for kw, slot in keywords.items():
            if kw in text.lower():
                vec[slot % VECTOR_DIM] += 2.5

        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec


class KnowledgeBase:
    """Manages the local FAISS regulatory vector index."""

    def __init__(self, store_dir: str = VECTOR_STORE_DIR):
        self.store_dir = store_dir
        self.index_path = os.path.join(store_dir, "faiss_index.bin")
        self.meta_path = os.path.join(store_dir, "metadata.json")
        self.embedder = LocalEmbeddingProvider()
        self.metadata: List[Dict[str, Any]] = []
        self.index: faiss.IndexFlatIP = faiss.IndexFlatIP(VECTOR_DIM)
        self.load()

    def load(self):
        """Loads index and metadata from disk if available."""
        if os.path.exists(self.index_path) and os.path.exists(self.meta_path):
            try:
                self.index = faiss.read_index(self.index_path)
                with open(self.meta_path, "r", encoding="utf-8") as f:
                    self.metadata = json.load(f)
                logger.info(f"Loaded FAISS index with {self.index.ntotal} clauses from {self.store_dir}")
            except Exception as e:
                logger.error(f"Error loading FAISS index: {e}. Reinitializing empty index.")
                self.index = faiss.IndexFlatIP(VECTOR_DIM)
                self.metadata = []

    def save(self):
        """Saves current FAISS index and metadata to disk."""
        os.makedirs(self.store_dir, exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved FAISS index ({self.index.ntotal} records) to {self.store_dir}")

    def add_chunks(self, chunks: List[Dict[str, Any]]) -> int:
        """Adds vectorized regulatory chunks into FAISS index."""
        if not chunks:
            return 0
        vectors = []
        for chunk in chunks:
            text = f"{chunk.get('framework', '')} {chunk.get('title', '')} {chunk.get('content', '')}"
            vec = self.embedder.get_embedding(text)
            vectors.append(vec)

        matrix = np.vstack(vectors).astype(np.float32)
        self.index.add(matrix)
        self.metadata.extend(chunks)
        self.save()
        return len(chunks)

    def search(
        self,
        query: str,
        category: Optional[str] = None,
        k: int = 4
    ) -> List[Dict[str, Any]]:
        """Semantic search against regulatory clauses with optional sector/category filter."""
        if self.index.ntotal == 0:
            return []

        q_vec = self.embedder.get_embedding(query).reshape(1, -1).astype(np.float32)
        fetch_k = min(k * 4 if category else k, self.index.ntotal)
        scores, indices = self.index.search(q_vec, fetch_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(self.metadata):
                continue
            item = self.metadata[idx].copy()
            item["similarity_score"] = float(score)

            if category and item.get("category", "").lower() != category.lower():
                continue

            results.append(item)
            if len(results) >= k:
                break

        # Fallback to general results if category filter was overly restrictive
        if not results and category:
            for score, idx in zip(scores[0], indices[0]):
                if idx < 0 or idx >= len(self.metadata):
                    continue
                item = self.metadata[idx].copy()
                item["similarity_score"] = float(score)
                results.append(item)
                if len(results) >= k:
                    break

        return results

    def get_summary(self) -> Dict[str, Any]:
        """Returns statistics on the indexed regulatory corpus."""
        categories = {}
        for m in self.metadata:
            cat = m.get("category", "General")
            categories[cat] = categories.get(cat, 0) + 1

        return {
            "total_clauses": len(self.metadata),
            "vector_dimension": VECTOR_DIM,
            "categories": categories,
            "index_path": self.index_path
        }


# Singleton instance
kb_instance = KnowledgeBase()


def get_knowledge_base() -> KnowledgeBase:
    return kb_instance
