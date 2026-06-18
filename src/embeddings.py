import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb

CHUNKS_FILE  = Path("data/chunks.json")
VECTOR_DIR   = Path("data/vectorstore")

MODEL_NAME   = "all-MiniLM-L6-v2"  # fast, good quality, 384-dim
BATCH_SIZE   = 32
COLLECTION   = "sec_filings"


def build_vector_store():
    print(f"Loading chunks from {CHUNKS_FILE}...")
    with open(CHUNKS_FILE) as f:
        chunks = json.load(f)

    print(f"Loading embedding model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    print("Connecting to ChromaDB...")
    client = chromadb.PersistentClient(path=str(VECTOR_DIR))

    # Delete existing collection if rebuilding
    try:
        client.delete_collection(COLLECTION)
        print("Deleted existing collection.")
    except:
        pass

    collection = client.get_or_create_collection(
        name=COLLECTION,
        metadata={"hnsw:space": "cosine"}
    )

    texts     = [c["text"]     for c in chunks]
    ids       = [c["chunk_id"] for c in chunks]
    metadatas = [{
        "ticker":   c["ticker"],
        "company":  c["company"],
        "year":     c["year"],
        "section":  c["section"],
        "chunk_id": c["chunk_id"],
    } for c in chunks]

    print(f"Embedding {len(texts)} chunks in batches of {BATCH_SIZE}...")
    for i in range(0, len(texts), BATCH_SIZE):
        batch_texts = texts[i:i + BATCH_SIZE]
        batch_ids   = ids[i:i + BATCH_SIZE]
        batch_meta  = metadatas[i:i + BATCH_SIZE]

        embeddings = model.encode(
            batch_texts,
            show_progress_bar=False,
            convert_to_numpy=True
        ).tolist()

        collection.add(
            ids=batch_ids,
            embeddings=embeddings,
            documents=batch_texts,
            metadatas=batch_meta,
        )
        print(f"  Indexed {min(i + BATCH_SIZE, len(texts))}/{len(texts)}")

    print(f"\nDone. {collection.count()} chunks indexed in ChromaDB.")
    return collection


if __name__ == "__main__":
    build_vector_store()