import os
import time
import re
import csv
from pathlib import Path
from bs4 import BeautifulSoup
from sec_edgar_downloader import Downloader
from dotenv import load_dotenv

load_dotenv()

TICKERS = {
    "AFRM": "Affirm Holdings",
    "SOFI": "SoFi Technologies",
    "LC":   "LendingClub",
    "UPST": "Upstart Holdings",
    "XYZ":   "Block Inc",
    "ALLY": "Ally Financial",
}

YEARS = ["2021", "2022", "2023", "2024"]

SECTION_PATTERNS = {
    "1A": [r"item\s*1a[\.\s]*risk factors", r"risk factors"],
    "7":  [r"item\s*7[\.\s]*management", r"management.s discussion"],
    "7A": [r"item\s*7a[\.\s]*quantitative", r"quantitative.*market risk"],
}

RAW_DIR       = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
METADATA_CSV  = Path("data/metadata.csv")

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def download_filings():
    dl = Downloader("FinSightRAG", "adityamittal@msu.edu", str(RAW_DIR))
    for ticker in TICKERS:
        for year in YEARS:
            try:
                dl.get(
                    "10-K", ticker,
                    after=f"{year}-01-01",
                    before=f"{int(year)+1}-06-30",
                    limit=1,
                )
                print(f"Downloaded {ticker} {year}")
                time.sleep(0.2)
            except Exception as e:
                print(f"Skipped {ticker} {year}: {e}")


def clean_text(text: str) -> str:
    text = re.sub(r"\n\s*\d+\s*\n", " ", text)
    text = re.sub(r"[-_]{3,}", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"exhibit\s+\d+[\.\d]*", "", text, flags=re.IGNORECASE)
    return text.strip()


def extract_section(html_path: Path, section_key: str) -> str:
    try:
        with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        text = soup.get_text(separator=" ")
        text = clean_text(text)
        for pattern in SECTION_PATTERNS.get(section_key, []):
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return text[match.start(): match.start() + 15000]
    except Exception as e:
        print(f"  Error extracting {section_key} from {html_path}: {e}")
    return ""


def find_htm_files(ticker: str) -> list[Path]:
    search_dir = RAW_DIR / "sec-edgar-filings" / ticker / "10-K"
    if not search_dir.exists():
        return []
    txt_files = list(search_dir.rglob("full-submission.txt"))
    return [f for f in txt_files if f.stat().st_size > 50_000]


def process_all():
    rows = []
    for ticker, company in TICKERS.items():
        htm_files = find_htm_files(ticker)
        if not htm_files:
            print(f"No files found for {ticker}")
            continue

        for htm_path in htm_files:
            # Year from parent folder name via EDGAR accession number
            # Accession numbers look like 0001820953-24-000035 where 24 = 2024
            accession = htm_path.parent.name
            year_match = re.search(r"-(\d{2})-", accession)
            if year_match:
                year_short = year_match.group(1)
                year = f"20{year_short}"
            else:
                # fallback: search inside file
                try:
                    content = htm_path.read_text(encoding="utf-8", errors="ignore")[:500]
                    ym = re.search(r"(202[0-9])", content)
                    year = ym.group(1) if ym else "unknown"
                except:
                    year = "unknown"

            for section_key in SECTION_PATTERNS:
                text = extract_section(htm_path, section_key)
                if len(text) < 500:
                    continue

                out_filename = f"{ticker}_{year}_{section_key}.txt"
                out_path = PROCESSED_DIR / out_filename
                out_path.write_text(text, encoding="utf-8")

                rows.append({
                    "ticker": ticker,
                    "company": company,
                    "year": year,
                    "section": section_key,
                    "file_path": str(out_path),
                    "char_count": len(text),
                    "source_htm": str(htm_path),
                })
                print(f"  Saved {out_filename} ({len(text):,} chars)")

    if not rows:
        print("No sections extracted.")
        return

    with open(METADATA_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nMetadata saved: {len(rows)} sections extracted.")


# if __name__ == "__main__":
#     print("=== Step 1: Downloading filings ===")
#     download_filings()
#     print("\n=== Step 2: Extracting sections ===")
#     process_all()

if __name__ == "__main__":
    print("=== Step 2: Extracting sections ===")
    process_all()