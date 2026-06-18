import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb
from rank_bm25 import BM25Okapi

VECTOR_DIR = Path("data/vectorstore")
CHUNKS_FILE = Path("data/chunks.json")
MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION = "sec_filings"


def load_resources():
    model = SentenceTransformer(MODEL_NAME)
    client = chromadb.PersistentClient(path=str(VECTOR_DIR))
    collection = client.get_collection(COLLECTION)
    with open(CHUNKS_FILE) as f:
        chunks = json.load(f)
    return model, collection, chunks


class HybridRetriever:
    def __init__(self, model, collection, chunks):
        self.model = model
        self.collection = collection
        self.chunks = chunks
        self.chunk_ids = [c["chunk_id"] for c in chunks]

        print("Building BM25 index...")
        tokenized = [c["text"].lower().split() for c in chunks]
        self.bm25 = BM25Okapi(tokenized)
        print("BM25 ready.")

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        alpha: float = 0.5,
        filter_ticker: str = None,
        filter_year: str = None,
    ) -> list[dict]:

        # Build metadata filter
        where_clause = {}
        if filter_ticker:
            where_clause["ticker"] = filter_ticker
        if filter_year:
            where_clause["year"] = str(filter_year)

        # Dense retrieval
        q_emb = self.model.encode([query]).tolist()[0]
        dense_results = self.collection.query(
            query_embeddings=[q_emb],
            n_results=min(top_k * 3, self.collection.count()),
            where=where_clause if where_clause else None,
            include=["documents", "metadatas", "distances"],
        )
        dense_scores = {
            dense_results["metadatas"][0][i]["chunk_id"]:
            1 - dense_results["distances"][0][i]
            for i in range(len(dense_results["documents"][0]))
        }

        # BM25 retrieval
        tokenized_query = query.lower().split()
        bm25_raw = self.bm25.get_scores(tokenized_query)
        bm25_max = max(bm25_raw) if max(bm25_raw) > 0 else 1.0
        bm25_scores = {
            self.chunk_ids[i]: bm25_raw[i] / bm25_max
            for i in range(len(self.chunk_ids))
        }

        # Combine scores
        all_ids = set(dense_scores) | set(bm25_scores)
        combined = {
            cid: alpha * dense_scores.get(cid, 0) +
                 (1 - alpha) * bm25_scores.get(cid, 0)
            for cid in all_ids
        }

        top_ids = sorted(combined, key=combined.get, reverse=True)[:top_k]
        id_to_chunk = {c["chunk_id"]: c for c in self.chunks}

        return [
            {
                **id_to_chunk[cid],
                "score": round(combined[cid], 4),
            }
            for cid in top_ids if cid in id_to_chunk
        ]


if __name__ == "__main__":
    model, collection, chunks = load_resources()
    retriever = HybridRetriever(model, collection, chunks)

    # Quick test
    query = "What credit risks did Affirm highlight in their filings?"
    results = retriever.retrieve(query, top_k=3)
    print(f"\nQuery: {query}\n")
    for r in results:
        print(f"[{r['company']} | {r['year']} | Section {r['section']}] score={r['score']}")
        print(f"{r['text'][:300]}\n")