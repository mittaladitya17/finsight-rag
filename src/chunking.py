import re
import json
from pathlib import Path
import pandas as pd

PROCESSED_DIR = Path("data/processed")
METADATA_CSV  = Path("data/metadata.csv")
CHUNKS_FILE   = Path("data/chunks.json")

CHUNK_SIZE    = 512
CHUNK_OVERLAP = 64


def clean_text(text: str) -> str:
    text = re.sub(r"\n\s*\d+\s*\n", " ", text)
    text = re.sub(r"[-_]{3,}", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_into_chunks(text: str, chunk_size: int = CHUNK_SIZE,
                      overlap: int = CHUNK_OVERLAP) -> list[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def build_chunks(metadata_csv: Path = METADATA_CSV) -> list[dict]:
    df = pd.read_csv(metadata_csv)
    all_chunks = []

    for _, row in df.iterrows():
        file_path = Path(row["file_path"])
        if not file_path.exists():
            print(f"Missing: {file_path}")
            continue

        text = file_path.read_text(encoding="utf-8", errors="ignore")
        text = clean_text(text)
        raw_chunks = split_into_chunks(text)

        for i, chunk_text in enumerate(raw_chunks):
            # Prepend metadata context into every chunk
            enriched = (
                f"[{row['company']} | {row['year']} | Section {row['section']}] "
                f"{chunk_text}"
            )
            all_chunks.append({
                "chunk_id":   f"{row['ticker']}_{row['year']}_{row['section']}_{i}",
                "ticker":     row["ticker"],
                "company":    row["company"],
                "year":       str(row["year"]),
                "section":    row["section"],
                "text":       enriched,
                "char_count": len(enriched),
            })

    print(f"Total chunks created: {len(all_chunks)}")
    return all_chunks


if __name__ == "__main__":
    chunks = build_chunks()
    with open(CHUNKS_FILE, "w") as f:
        json.dump(chunks, f, indent=2)
    print(f"Saved {len(chunks)} chunks to {CHUNKS_FILE}")