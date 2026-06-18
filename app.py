"""
FinSight — SEC 10-K Intelligence Platform v3
Clean, analyst-grade RAG + XBRL quantitative layer
"""

import os, json, time, requests
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FinSight — Fintech Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Styles ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { padding: 0 2rem 3rem; max-width: 1200px; }

/* Nav */
.nav { display:flex; align-items:center; justify-content:space-between;
       padding:1rem 0; border-bottom:1px solid #0f1929; margin-bottom:0; }
.nav-brand { font-family:'JetBrains Mono',monospace; font-size:1rem;
             font-weight:500; color:#e2eaf5; letter-spacing:0.05em; }
.nav-brand span { color:#3b82f6; }
.nav-sub { font-size:0.72rem; color:#1e3050; }

/* Hero */
.hero { padding:3.5rem 0 2.5rem; border-bottom:1px solid #0f1929; }
.hero-kicker { font-family:'JetBrains Mono',monospace; font-size:0.65rem;
               letter-spacing:0.22em; color:#3b82f6; text-transform:uppercase;
               margin-bottom:0.7rem; }
.hero-h1 { font-size:2.6rem; font-weight:700; color:#e2eaf5; line-height:1.12;
           margin:0 0 1rem; }
.hero-h1 em { color:#3b82f6; font-style:normal; }
.hero-lead { font-size:0.95rem; color:#2d4a6a; max-width:520px;
             line-height:1.75; margin:0 0 2rem; }
.hero-pills { display:flex; gap:0.5rem; flex-wrap:wrap; margin-bottom:2.5rem; }
.pill { font-family:'JetBrains Mono',monospace; font-size:0.62rem;
        letter-spacing:0.08em; background:#040d1a; border:1px solid #0f2540;
        color:#2d5080; border-radius:4px; padding:0.22rem 0.7rem; }

/* Stats row */
.stats { display:grid; grid-template-columns:repeat(5,1fr); gap:1px;
         background:#0a1628; border:1px solid #0a1628; border-radius:10px;
         overflow:hidden; margin-bottom:3rem; }
.stat { background:#030c1a; padding:1.1rem 1.4rem; }
.stat-n { font-family:'JetBrains Mono',monospace; font-size:1.6rem;
          font-weight:500; color:#e2eaf5; line-height:1; }
.stat-l { font-size:0.68rem; color:#1a3050; margin-top:0.2rem;
          letter-spacing:0.04em; }

/* How */
.how { display:grid; grid-template-columns:repeat(4,1fr); gap:1px;
       background:#0a1628; border:1px solid #0a1628; border-radius:10px;
       overflow:hidden; margin-bottom:0.5rem; }
.how-c { background:#030c1a; padding:1.1rem 1.3rem; }
.how-n { font-family:'JetBrains Mono',monospace; font-size:0.6rem;
         color:#3b82f6; letter-spacing:0.12em; margin-bottom:0.35rem; }
.how-t { font-size:0.82rem; font-weight:600; color:#94aac0; margin-bottom:0.2rem; }
.how-d { font-size:0.75rem; color:#1a3050; line-height:1.55; }

/* Section label */
.slabel { font-family:'JetBrains Mono',monospace; font-size:0.62rem;
          letter-spacing:0.18em; color:#3b82f6; text-transform:uppercase;
          margin:2rem 0 0.8rem; padding-bottom:0.4rem;
          border-bottom:1px solid #0a1628; }

/* Example buttons */
.ex-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:0.6rem;
           margin-bottom:1rem; }

/* Answer */
.answer { background:#030c1a; border:1px solid #0a1628;
          border-top:2px solid #3b82f6; border-radius:10px;
          padding:1.6rem 2rem; margin-top:1rem; }
.answer-eye { font-family:'JetBrains Mono',monospace; font-size:0.6rem;
              letter-spacing:0.18em; color:#3b82f6; text-transform:uppercase;
              margin-bottom:0.9rem; }
.answer-body { font-size:0.9rem; color:#94aac0; line-height:1.85; }
.chips { display:flex; flex-wrap:wrap; gap:0.35rem; margin-top:1rem;
         padding-top:0.8rem; border-top:1px solid #0a1628; }
.chip { font-family:'JetBrains Mono',monospace; font-size:0.6rem;
        background:#040f20; border:1px solid #0f2540; color:#3b82f6;
        border-radius:3px; padding:0.16rem 0.55rem; }
.toks { font-family:'JetBrains Mono',monospace; font-size:0.6rem;
        color:#0f2030; margin-top:0.5rem; }

/* Chunk */
.chunk { background:#020912; border:1px solid #0a1628; border-radius:7px;
         padding:0.9rem 1.1rem; margin-bottom:0.45rem; }
.chunk-m { font-family:'JetBrains Mono',monospace; font-size:0.6rem;
           color:#1a3a5a; display:flex; justify-content:space-between;
           margin-bottom:0.3rem; }
.chunk-s { color:#22c55e; }
.chunk-b { font-size:0.8rem; color:#1a3050; line-height:1.6; }

/* Metric card */
.mcard { background:#030c1a; border:1px solid #0a1628; border-radius:9px;
         padding:1.1rem 1.3rem; }
.mcard-lbl { font-family:'JetBrains Mono',monospace; font-size:0.6rem;
             color:#1a3050; letter-spacing:0.1em; text-transform:uppercase;
             margin-bottom:0.3rem; }
.mcard-val { font-size:1.4rem; font-weight:600; color:#e2eaf5; line-height:1; }
.mcard-sub { font-size:0.72rem; color:#1a3050; margin-top:0.2rem; }

/* Mind */
.mind { background:#060412; border:1px solid #1e1060;
        border-left:3px solid #6366f1; border-radius:8px;
        padding:1.1rem 1.4rem; font-size:0.87rem; color:#6366f1;
        line-height:1.8; margin:1rem 0; }
.mind-l { font-family:'JetBrains Mono',monospace; font-size:0.58rem;
          letter-spacing:0.16em; color:#4338ca; text-transform:uppercase;
          display:block; margin-bottom:0.4rem; }

/* Coverage badge */
.cov-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:0.6rem;
            margin-bottom:1rem; }
.cov-card { background:#030c1a; border:1px solid #0a1628; border-radius:8px;
            padding:0.85rem 1rem; }
.cov-ticker { font-family:'JetBrains Mono',monospace; font-size:0.72rem;
              color:#3b82f6; margin-bottom:0.2rem; }
.cov-name { font-size:0.78rem; color:#94aac0; font-weight:500; margin-bottom:0.3rem; }
.cov-years { font-size:0.68rem; color:#1a3050; }

/* Sidebar */
[data-testid="stSidebar"] { background:#020812 !important;
    border-right:1px solid #0a1628; }
[data-testid="stSidebar"] * { color:#1a3050 !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap:0; border-bottom:1px solid #0a1628;
    background:transparent; margin-top:1.5rem; }
.stTabs [data-baseweb="tab"] {
    font-family:'JetBrains Mono',monospace; font-size:0.65rem;
    letter-spacing:0.12em; text-transform:uppercase; color:#1a3050;
    padding:0.55rem 1.4rem; border:none; background:transparent; }
.stTabs [aria-selected="true"] { color:#3b82f6 !important;
    border-bottom:2px solid #3b82f6 !important; background:transparent !important; }

/* Warn */
.warn { background:#060f06; border:1px solid #0f3010; border-radius:7px;
        padding:0.8rem 1.1rem; font-size:0.82rem; color:#22c55e; }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
TICKERS_META = {
    "AFRM": {"name": "Affirm Holdings",    "sector": "BNPL",          "cik": "0001820953"},
    "SOFI": {"name": "SoFi Technologies",  "sector": "Neobank",       "cik": "0001393818"},
    "LC":   {"name": "LendingClub",        "sector": "Marketplace",   "cik": "0001409970"},
    "UPST": {"name": "Upstart Holdings",   "sector": "AI Lending",    "cik": "0001647639"},
    "ALLY": {"name": "Ally Financial",     "sector": "Digital Bank",  "cik": "0000040729"},
    "PGY":  {"name": "Pagaya Technologies","sector": "AI Credit",     "cik": "0001883085"},
    "BFH":  {"name": "Bread Financial",    "sector": "Credit Cards",  "cik": "0001101239"},
    "OPFI": {"name": "OppFi",              "sector": "Subprime",      "cik": "0001818502"},
}
SECTION_MAP = {"1A": "Risk Factors", "7": "MD&A", "7A": "Market Risk"}

# ── Load pipeline ─────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading pipeline...")
def load_pipeline():
    try:
        from src.retrieval import load_resources, HybridRetriever
        model, collection, chunks = load_resources()
        retriever = HybridRetriever(model, collection, chunks)
        return retriever, chunks, None
    except Exception as e:
        return None, [], str(e)

@st.cache_data(show_spinner=False)
def load_metadata():
    p = Path("data/metadata.csv")
    if not p.exists():
        return {}, []
    import pandas as pd
    df = pd.read_csv(p)
    df = df[df["year"].astype(str) != "unknown"]
    by_ticker = df.groupby("ticker")["year"].apply(
        lambda x: sorted(x.astype(str).unique().tolist())
    ).to_dict()
    years = sorted(df["year"].astype(str).unique().tolist(), reverse=True)
    return by_ticker, years

# ── XBRL financial data ───────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_xbrl_metric(cik: str, concept: str, unit: str = "USD"):
    """Fetch a single XBRL concept for a company from SEC."""
    url = f"https://data.sec.gov/api/xbrl/companyconcept/{cik}/{concept}.json"
    try:
        r = requests.get(url, headers={"User-Agent": "FinSightRAG aditya@msu.edu"}, timeout=8)
        if r.status_code != 200:
            return []
        data = r.json()
        facts = data.get("units", {}).get(unit, [])
        annual = [f for f in facts if f.get("form") in ("10-K", "20-F") and f.get("val") is not None]
        seen = {}
        for f in annual:
            yr = f.get("end", "")[:4]
            if yr not in seen:
                seen[yr] = f["val"]
        return [{"year": k, "value": v} for k, v in sorted(seen.items())]
    except Exception:
        return []

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_company_financials(tickers_meta: dict):
    """Fetch key financial metrics for all companies."""
    CONCEPTS = {
        "Revenue":    ("us-gaap", "Revenues", "USD"),
        "Net Income": ("us-gaap", "NetIncomeLoss", "USD"),
        "Total Assets":("us-gaap","Assets","USD"),
    }
    results = {}
    for ticker, meta in tickers_meta.items():
        cik = meta["cik"]
        results[ticker] = {}
        for label, (ns, concept, unit) in CONCEPTS.items():
            full_concept = f"{ns}/{concept}"
            data = fetch_xbrl_metric(cik, full_concept, unit)
            results[ticker][label] = data
        time.sleep(0.12)
    return results

retriever, all_chunks, load_error = load_pipeline()
ticker_years, all_years = load_metadata()
all_chunks_clean = [c for c in all_chunks if str(c.get("year","")) != "unknown"]

# ── Nav ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nav">
  <div class="nav-brand">Fin<span>Sight</span></div>
  <div class="nav-sub">SEC 10-K Intelligence · 8 companies · 2021–2025</div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_about, tab_query, tab_analytics, tab_corpus = st.tabs([
    "Overview", "Query Filings", "Financial Analytics", "Corpus"
])

# ════════════════════════════════════════════════════════════
#  TAB 0 — OVERVIEW  (first tab)
# ════════════════════════════════════════════════════════════
with tab_about:

    n_filings = len(set(f"{c['ticker']}_{c['year']}" for c in all_chunks_clean))

    st.markdown(f"""
    <div class="hero">
      <div class="hero-kicker">Fintech · SEC 10-K Intelligence · RAG + XBRL</div>
      <h1 class="hero-h1">Ask anything about<br><em>fintech risk disclosures</em></h1>
      <p class="hero-lead">
        FinSight combines a hybrid retrieval pipeline over SEC 10-K filings with
        structured XBRL financial data to give analysts both the narrative context
        and the numbers — in one place, with citations.
      </p>
      <div class="hero-pills">
        <span class="pill">8 companies</span>
        <span class="pill">{n_filings} filing-years</span>
        <span class="pill">{len(all_chunks_clean)} indexed chunks</span>
        <span class="pill">Hybrid BM25 + semantic retrieval</span>
        <span class="pill">XBRL financial metrics</span>
        <span class="pill">Claude Sonnet generation</span>
      </div>
      <div class="stats">
        <div class="stat"><div class="stat-n">{len(all_chunks_clean)}</div><div class="stat-l">Chunks indexed</div></div>
        <div class="stat"><div class="stat-n">{n_filings}</div><div class="stat-l">Filing-years</div></div>
        <div class="stat"><div class="stat-n">8</div><div class="stat-l">Companies</div></div>
        <div class="stat"><div class="stat-n">3</div><div class="stat-l">Sections / filing</div></div>
        <div class="stat"><div class="stat-n">5</div><div class="stat-l">Years covered</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Companies covered
    st.markdown('<div class="slabel">Companies covered</div>', unsafe_allow_html=True)
    rows = list(TICKERS_META.items())
    cols = st.columns(4)
    for i, (ticker, meta) in enumerate(rows):
        yrs = ticker_years.get(ticker, [])
        yr_str = f"{min(yrs)}–{max(yrs)}" if yrs else "—"
        with cols[i % 4]:
            st.markdown(f"""
            <div class="cov-card">
              <div class="cov-ticker">{ticker}</div>
              <div class="cov-name">{meta['name']}</div>
              <div class="cov-years">{meta['sector']} · {yr_str}</div>
            </div>
            """, unsafe_allow_html=True)

    # How it works
    st.markdown('<div class="slabel">How it works</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="how">
      <div class="how-c">
        <div class="how-n">01 — Ingest</div>
        <div class="how-t">SEC EDGAR filings</div>
        <div class="how-d">10-K annual reports downloaded directly from EDGAR. Items 1A, 7, and 7A extracted per filing.</div>
      </div>
      <div class="how-c">
        <div class="how-n">02 — Index</div>
        <div class="how-t">Hybrid retrieval</div>
        <div class="how-d">512-word chunks embedded with sentence-transformers. BM25 + dense cosine search at query time.</div>
      </div>
      <div class="how-c">
        <div class="how-n">03 — Answer</div>
        <div class="how-t">Grounded generation</div>
        <div class="how-d">Claude synthesises answers from retrieved passages only. Every claim cites company, year, and section.</div>
      </div>
      <div class="how-c">
        <div class="how-n">04 — Quantify</div>
        <div class="how-t">XBRL financials</div>
        <div class="how-d">Revenue, net income, and total assets pulled live from SEC's structured XBRL data API.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # What questions to ask
    st.markdown('<div class="slabel">What you can ask</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        **Single-company deep dives**
        - How did Affirm describe its credit loss provision methodology?
        - What risk factors did Upstart highlight around AI model performance?
        - How did OppFi characterise its subprime borrower exposure?
        """)
    with c2:
        st.markdown("""
        **Cross-year trend analysis**
        - How did Ally Financial's interest rate risk language change 2022–2024?
        - When did LendingClub first mention CECL in its filings?
        - How did Bread Financial's regulatory risk disclosures evolve?
        """)
    with c3:
        st.markdown("""
        **Cross-company comparison**
        - Compare how BNPL lenders describe credit quality vs. traditional banks.
        - Which companies were most explicit about macro risk in 2023?
        - How do AI-driven lenders describe model risk differently from others?
        """)

    # Architecture
    st.markdown('<div class="slabel">Why hybrid retrieval?</div>', unsafe_allow_html=True)
    st.markdown("""
    Dense semantic search alone misses exact financial terms. Phrases like
    *"net charge-off rate"*, *"CECL methodology"*, and *"Tier 1 capital"* need
    exact keyword matching that embedding similarity won't reliably surface.
    BM25 handles exact matches; dense search handles conceptual queries.
    The α slider in the Query tab lets you tune the balance for your specific question.
    """)

    st.markdown('<div class="slabel">Honest limitations</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        - 15,000-character cap per section may truncate long risk factor lists
        - LendingClub 2024 filing excluded due to HTML encoding error
        - UPST 2025 filing excluded for the same reason
        - Text sections only — no footnotes, exhibits, or financial tables
        """)
    with col2:
        st.markdown("""
        - XBRL metrics not available for all tickers/years (SEC coverage varies)
        - Nu Holdings excluded — files as foreign private issuer (20-F, not 10-K)
        - Answers are grounded in disclosed text, not verified by independent auditors
        - Not investment advice
        """)

    st.markdown("""
    <div class="mind">
      <span class="mind-l">In my mind</span>
      The hardest part wasn't the RAG pipeline — it was the data. SEC filings look
      uniform from the outside but are structurally chaotic underneath. LendingClub's
      2024 filing has a non-standard HTML encoding marker that BeautifulSoup can't
      parse. Upstart's 2025 filing has a similar issue. Rather than engineer around
      two edge cases, I logged them and moved on — a production system would need a
      fallback parser chain (lxml → html5lib → plain text extraction).
      <br><br>
      The XBRL layer came from a realisation that text answers alone aren't enough
      for an analyst. If someone asks "how did Affirm describe revenue growth" and
      the answer is qualitative, the next question is always "so what were the actual
      numbers?" The SEC's XBRL API gives us those numbers for free, structured, and
      machine-readable. Pairing text retrieval with quantitative data is what
      separates this from a demo.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:0.72rem;color:#0a1628;text-align:center;
                padding:1.5rem 0 0.5rem;border-top:1px solid #0a1628;margin-top:2rem;">
      Built by
      <a href="https://github.com/mittaladitya17" target="_blank"
         style="color:#1a3a6a;text-decoration:none;">Aditya Mittal</a>
      &nbsp;·&nbsp;
      <a href="https://github.com/mittaladitya17/finsight-rag" target="_blank"
         style="color:#1a3a6a;text-decoration:none;">GitHub ↗</a>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
#  TAB 1 — QUERY
# ════════════════════════════════════════════════════════════
with tab_query:

    if load_error:
        st.error(f"Pipeline failed to load: {load_error}")
        st.stop()

    # Filters in a clean row
    fc1, fc2, fc3, fc4 = st.columns([2, 1.5, 1.5, 1])
    with fc1:
        sel_companies = st.multiselect(
            "Company", list(TICKERS_META.keys()),
            format_func=lambda t: f"{t} — {TICKERS_META[t]['name']}",
            placeholder="All companies", label_visibility="visible"
        )
    with fc2:
        sel_years = st.multiselect("Year", all_years, placeholder="All years")
    with fc3:
        sel_section = st.selectbox(
            "Section", ["All sections", "1A — Risk Factors", "7 — MD&A", "7A — Market Risk"]
        )
    with fc4:
        top_k = st.slider("Chunks", 3, 10, 5, label_visibility="visible")

    alpha = st.slider(
        "Retrieval: ← keyword  |  semantic →",
        0.0, 1.0, 0.5, 0.1,
        help="0 = BM25 keyword-only · 1 = dense semantic-only · 0.5 = hybrid"
    )

    # Examples
    EXAMPLES = [
        ("Single company",  "How did Affirm describe its credit loss provision methodology?"),
        ("Cross-year",      "How did Upstart's language around macro risk change between 2022 and 2024?"),
        ("Cross-company",   "Compare how Affirm and SoFi describe regulatory risk."),
        ("AI underwriting", "Which companies describe using AI or ML in their underwriting process?"),
        ("Credit quality",  "What did LendingClub and OppFi say about rising delinquency rates?"),
        ("Interest rates",  "How did Ally Financial and Bread Financial describe interest rate exposure?"),
    ]

    st.markdown('<div class="slabel">Example questions</div>', unsafe_allow_html=True)
    ex_cols = st.columns(3)
    clicked = None
    for i, (tag, txt) in enumerate(EXAMPLES):
        with ex_cols[i % 3]:
            if st.button(f"**{tag}**  \n{txt}", key=f"ex{i}", use_container_width=True):
                clicked = txt

    st.markdown('<div class="slabel">Ask a question</div>', unsafe_allow_html=True)
    query = st.text_area("", value=clicked or "",
                         height=80, placeholder="Type your question here…",
                         label_visibility="collapsed", key="q")
    run = st.button("Search filings →", type="primary")

    if run and query.strip():
        import pandas as pd
        filter_ticker = sel_companies[0] if len(sel_companies) == 1 else None
        filter_year   = sel_years[0]     if len(sel_years)     == 1 else None
        filter_sec    = sel_section.split("—")[0].strip() \
                        if sel_section != "All sections" else None

        with st.spinner("Retrieving relevant passages…"):
            try:
                retrieved = retriever.retrieve(
                    query, top_k=top_k, alpha=alpha,
                    filter_ticker=filter_ticker, filter_year=filter_year,
                )
                if filter_sec:
                    retrieved = [r for r in retrieved if r["section"] == filter_sec]
            except Exception as e:
                st.error(f"Retrieval error: {e}"); st.stop()

        if not retrieved:
            st.markdown('<div class="warn">No relevant passages found. Try broadening your filters or rephrasing.</div>',
                        unsafe_allow_html=True)
        else:
            with st.spinner("Generating grounded answer…"):
                try:
                    from src.generation import generate_answer
                    result = generate_answer(query, retrieved)
                except Exception as e:
                    st.error(f"Generation error: {e}"); st.stop()

            chips = "".join(
                f'<span class="chip">{c["company"]} · {c["year"]} · {SECTION_MAP.get(c["section"],c["section"])}</span>'
                for c in retrieved
            )
            st.markdown(f"""
            <div class="answer">
              <div class="answer-eye">Answer — grounded in source text</div>
              <div class="answer-body">{result["answer"].replace(chr(10),"<br>")}</div>
              <div class="chips">{chips}</div>
              <div class="toks">{result["input_tokens"]} in · {result["output_tokens"]} out</div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander(f"Source passages ({len(retrieved)})"):
                for c in retrieved:
                    st.markdown(f"""
                    <div class="chunk">
                      <div class="chunk-m">
                        <span>{c["company"]} · {c["year"]} · {SECTION_MAP.get(c["section"],c["section"])}</span>
                        <span class="chunk-s">{c["score"]}</span>
                      </div>
                      <div class="chunk-b">{c["text"][:650]}…</div>
                    </div>
                    """, unsafe_allow_html=True)

    elif run:
        st.warning("Enter a question or click an example above.")

# ════════════════════════════════════════════════════════════
#  TAB 2 — FINANCIAL ANALYTICS  (quantitative layer)
# ════════════════════════════════════════════════════════════
with tab_analytics:
    import pandas as pd
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    BASE = dict(
        template="plotly_dark",
        paper_bgcolor="#030c1a",
        plot_bgcolor="#030c1a",
        font=dict(color="#2d4a6a", family="Inter"),
        margin=dict(l=50, r=20, t=45, b=40),
    )
    COLORS = ["#3b82f6","#22c55e","#f59e0b","#a78bfa","#f472b6",
              "#34d399","#fb923c","#60a5fa"]

    st.markdown('<div class="slabel">Live financial data from SEC XBRL API</div>',
                unsafe_allow_html=True)
    st.caption("Revenue, net income, and total assets pulled directly from SEC structured filings. "
               "Coverage varies by company and year.")

    sel_tickers = st.multiselect(
        "Select companies to compare",
        list(TICKERS_META.keys()),
        default=["AFRM","SOFI","UPST","ALLY"],
        format_func=lambda t: f"{t} — {TICKERS_META[t]['name']}"
    )

    if not sel_tickers:
        st.info("Select at least one company above.")
    else:
        with st.spinner("Fetching XBRL data from SEC…"):
            subset_meta = {t: TICKERS_META[t] for t in sel_tickers}
            fin_data = fetch_company_financials(subset_meta)

        metric = st.radio(
            "Metric",
            ["Revenue", "Net Income", "Total Assets"],
            horizontal=True
        )

        # Build time-series chart
        fig = go.Figure()
        for i, ticker in enumerate(sel_tickers):
            series = fin_data.get(ticker, {}).get(metric, [])
            if not series:
                continue
            years_  = [int(d["year"]) for d in series]
            vals    = [d["value"] / 1e9 for d in series]
            fig.add_trace(go.Scatter(
                x=years_, y=vals,
                name=f"{ticker}",
                mode="lines+markers",
                line=dict(color=COLORS[i % len(COLORS)], width=2),
                marker=dict(size=6),
                hovertemplate=f"<b>{ticker}</b><br>%{{x}}: $%{{y:.2f}}B<extra></extra>"
            ))

        unit_label = "USD Billions"
        fig.update_layout(
            **BASE,
            title=f"{metric} — {unit_label}",
            xaxis=dict(title="Year", tickformat="d", showgrid=False),
            yaxis=dict(title=unit_label, showgrid=True,
                       gridcolor="#0a1628", gridwidth=1),
            legend=dict(orientation="h", y=-0.18),
            height=420,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Latest year comparison bar
        st.markdown('<div class="slabel">Latest available value comparison</div>',
                    unsafe_allow_html=True)
        bar_data = []
        for ticker in sel_tickers:
            series = fin_data.get(ticker, {}).get(metric, [])
            if series:
                latest = sorted(series, key=lambda x: x["year"])[-1]
                bar_data.append({
                    "ticker": ticker,
                    "name": TICKERS_META[ticker]["name"],
                    "year": latest["year"],
                    "value": latest["value"] / 1e9,
                })

        if bar_data:
            bdf = pd.DataFrame(bar_data).sort_values("value", ascending=True)
            fig2 = go.Figure(go.Bar(
                x=bdf["value"],
                y=bdf["ticker"],
                orientation="h",
                marker=dict(
                    color=bdf["value"],
                    colorscale=[[0,"#0a1628"],[1,"#3b82f6"]],
                    showscale=False
                ),
                text=[f"${v:.2f}B ({yr})" for v, yr in zip(bdf["value"], bdf["year"])],
                textposition="outside",
                textfont=dict(color="#2d4a6a", size=11),
                hovertemplate="<b>%{y}</b><br>$%{x:.2f}B<extra></extra>"
            ))
            fig2.update_layout(
                **BASE,
                title=f"Latest {metric} (USD Billions)",
                xaxis_title="USD Billions",
                height=max(250, len(bar_data) * 55),
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Data table
        with st.expander("Raw data table"):
            rows_out = []
            for ticker in sel_tickers:
                for m_name in ["Revenue","Net Income","Total Assets"]:
                    for entry in fin_data.get(ticker,{}).get(m_name,[]):
                        rows_out.append({
                            "Ticker": ticker,
                            "Company": TICKERS_META[ticker]["name"],
                            "Metric": m_name,
                            "Year": entry["year"],
                            "Value ($B)": round(entry["value"]/1e9, 3),
                        })
            if rows_out:
                st.dataframe(
                    pd.DataFrame(rows_out).sort_values(["Ticker","Metric","Year"]),
                    use_container_width=True, height=350
                )
            else:
                st.info("No XBRL data returned for selected companies.")

        st.markdown("""
        <div class="mind">
          <span class="mind-l">What you're seeing</span>
          These numbers come directly from the SEC's XBRL API —
          the same structured data that Bloomberg and FactSet ingest.
          Not scraped, not estimated: machine-readable financial facts
          submitted by the companies themselves as part of their SEC filings.
          Coverage gaps exist where companies filed using non-standard XBRL
          taxonomies or where the SEC's EDGAR mapping is incomplete.
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
#  TAB 3 — CORPUS
# ════════════════════════════════════════════════════════════
with tab_corpus:
    import pandas as pd
    import plotly.graph_objects as go

    BASE2 = dict(
        template="plotly_dark",
        paper_bgcolor="#030c1a",
        plot_bgcolor="#030c1a",
        font=dict(color="#2d4a6a", family="Inter"),
        margin=dict(l=50, r=20, t=45, b=40),
    )

    try:
        meta = pd.read_csv("data/metadata.csv")
        meta = meta[meta["year"].astype(str) != "unknown"]
    except Exception:
        st.warning("metadata.csv not found.")
        st.stop()

    # Coverage heatmap
    pivot = meta.groupby(["ticker","year"]).size().reset_index(name="n")
    pivot_wide = pivot.pivot(index="ticker", columns="year", values="n").fillna(0)

    fig = go.Figure(go.Heatmap(
        z=pivot_wide.values,
        x=pivot_wide.columns.astype(str).tolist(),
        y=pivot_wide.index.tolist(),
        colorscale=[[0,"#030c1a"],[0.01,"#0a1f3a"],[1,"#3b82f6"]],
        showscale=False,
        text=pivot_wide.values.astype(int),
        texttemplate="%{text}",
        textfont=dict(size=12, color="#4a7aaa"),
    ))
    fig.update_layout(**BASE2, title="Sections indexed per company × year",
                      height=360)
    st.plotly_chart(fig, use_container_width=True)

    # Section breakdown
    col1, col2 = st.columns(2)
    with col1:
        sec_counts = meta.groupby("section").size().reset_index(name="count")
        sec_counts["label"] = sec_counts["section"].map(SECTION_MAP)
        fig2 = go.Figure(go.Bar(
            x=sec_counts["label"], y=sec_counts["count"],
            marker_color=["#3b82f6","#22c55e","#a78bfa"], opacity=0.85,
        ))
        fig2.update_layout(**BASE2, title="Sections by type", height=280)
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        comp_counts = meta.groupby("ticker").size().reset_index(name="n")
        fig3 = go.Figure(go.Bar(
            x=comp_counts["n"], y=comp_counts["ticker"],
            orientation="h",
            marker=dict(color=comp_counts["n"],
                        colorscale=[[0,"#0a1628"],[1,"#3b82f6"]],
                        showscale=False),
        ))
        fig3.update_layout(**BASE2, title="Sections per company", height=280)
        st.plotly_chart(fig3, use_container_width=True)

    # What each section covers
    st.markdown('<div class="slabel">Section reference</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        **Item 1A — Risk Factors**
        Every material risk the business faces. The most analyst-relevant
        section — changes in language year-over-year are a signal in themselves.
        A risk that appears for the first time in 2023 is worth investigating.
        """)
    with c2:
        st.markdown("""
        **Item 7 — MD&A**
        Management explains the *why* behind the numbers — revenue drivers,
        provision changes, portfolio performance, strategic shifts.
        More narrative than the financial statements, more candid than the press release.
        """)
    with c3:
        st.markdown("""
        **Item 7A — Market Risk**
        Quantitative sensitivity disclosures — how earnings change under
        rate stress scenarios. Critical for understanding balance sheet
        exposure to rising or falling interest rates.
        """)

    st.markdown('<div class="slabel">Full index</div>', unsafe_allow_html=True)
    st.dataframe(
        meta[["ticker","company","year","section","char_count"]]
        .rename(columns={"char_count":"chars"})
        .sort_values(["ticker","year"]),
        use_container_width=True, height=380
    )