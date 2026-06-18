"""
FinSight RAG — Financial Document Intelligence
Redesigned Streamlit app v2
"""

import os
import json
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="FinSight — SEC Filing Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
.block-container { padding-top: 0; padding-bottom: 2rem; max-width: 1140px; }

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #04080f 0%, #071428 60%, #04080f 100%);
    border-bottom: 1px solid #0f2040;
    padding: 2.2rem 2.5rem 1.8rem;
    margin: -1rem -1rem 1.5rem -1rem;
}
.hero-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.22em;
    color: #2563eb;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.hero-title {
    font-size: 2rem;
    font-weight: 700;
    color: #f0f6ff;
    margin: 0 0 0.5rem;
    line-height: 1.15;
}
.hero-title em { color: #3b82f6; font-style: normal; }
.hero-sub {
    color: #4b6080;
    font-size: 0.88rem;
    max-width: 580px;
    line-height: 1.65;
    margin: 0;
}

/* ── How it works strip ── */
.how-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.8rem;
    margin-bottom: 1.6rem;
}
.how-card {
    background: #070e1c;
    border: 1px solid #0f2040;
    border-radius: 8px;
    padding: 0.9rem 1rem;
}
.how-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: #2563eb;
    margin-bottom: 0.3rem;
    letter-spacing: 0.1em;
}
.how-title { font-size: 0.82rem; font-weight: 600; color: #cbd5e1; margin-bottom: 0.2rem; }
.how-desc { font-size: 0.75rem; color: #374a60; line-height: 1.5; }

/* ── Example cards ── */
.ex-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.6rem;
    margin-bottom: 1.2rem;
}
.ex-card {
    background: #070e1c;
    border: 1px solid #0f2040;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    cursor: pointer;
    transition: border-color 0.15s;
}
.ex-card:hover { border-color: #2563eb; }
.ex-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: #2563eb;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.ex-text { font-size: 0.8rem; color: #64748b; line-height: 1.5; }

/* ── Query area ── */
.query-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.16em;
    color: #2563eb;
    text-transform: uppercase;
    margin-bottom: 0.35rem;
}

/* ── Answer ── */
.answer-wrap {
    background: #040d1a;
    border: 1px solid #0f2040;
    border-top: 3px solid #2563eb;
    border-radius: 10px;
    padding: 1.5rem 1.8rem;
    margin-top: 1rem;
}
.answer-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    color: #2563eb;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}
.answer-body {
    color: #c8d8f0;
    font-size: 0.91rem;
    line-height: 1.8;
}
.source-strip {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
    margin-top: 1rem;
    padding-top: 0.8rem;
    border-top: 1px solid #0f2040;
}
.src-chip {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    background: #071428;
    border: 1px solid #1a3a6e;
    color: #60a5fa;
    border-radius: 4px;
    padding: 0.18rem 0.55rem;
}
.token-note {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    color: #1e3050;
    margin-top: 0.6rem;
}

/* ── Chunk card ── */
.chunk-wrap {
    background: #040d1a;
    border: 1px solid #0d1e38;
    border-radius: 7px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.5rem;
}
.chunk-meta {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    color: #2563eb;
    margin-bottom: 0.35rem;
    display: flex;
    justify-content: space-between;
}
.chunk-score { color: #22c55e; }
.chunk-body { font-size: 0.8rem; color: #334a60; line-height: 1.6; }

/* ── Corpus stats ── */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.7rem;
    margin-bottom: 1.4rem;
}
.stat-card {
    background: #070e1c;
    border: 1px solid #0f2040;
    border-radius: 8px;
    padding: 0.8rem 1rem;
}
.stat-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.5rem;
    font-weight: 600;
    color: #f0f6ff;
    line-height: 1;
}
.stat-lbl { font-size: 0.68rem; color: #2d4060; margin-top: 0.2rem; }

/* ── Section header ── */
.sec-head {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.16em;
    color: #2563eb;
    text-transform: uppercase;
    margin: 1.2rem 0 0.6rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #0f2040;
}

/* ── Mind box ── */
.mind-box {
    background: #080514;
    border: 1px solid #2e1065;
    border-left: 3px solid #6366f1;
    border-radius: 8px;
    padding: 1rem 1.3rem;
    margin: 0.8rem 0;
    font-size: 0.87rem;
    color: #a5b4fc;
    line-height: 1.75;
}
.mind-lbl {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.16em;
    color: #6366f1;
    text-transform: uppercase;
    display: block;
    margin-bottom: 0.4rem;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] { background: #030810 !important; border-right: 1px solid #0f2040; }
[data-testid="stSidebar"] * { color: #4b6080 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #94a3b8 !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    border-bottom: 1px solid #0f2040;
    background: transparent;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #2d4060;
    padding: 0.5rem 1.3rem;
    border: none;
    background: transparent;
}
.stTabs [aria-selected="true"] {
    color: #3b82f6 !important;
    border-bottom: 2px solid #3b82f6 !important;
    background: transparent !important;
}

/* ── Warn box ── */
.warn-box {
    background: #0c1a0a;
    border: 1px solid #14532d;
    border-radius: 7px;
    padding: 0.8rem 1.1rem;
    font-size: 0.82rem;
    color: #4ade80;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  LOAD PIPELINE
# ─────────────────────────────────────────────

@st.cache_resource(show_spinner="Initialising retrieval pipeline...")
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
    meta_path = Path("data/metadata.csv")
    if not meta_path.exists():
        return [], [], []
    import pandas as pd
    df = pd.read_csv(meta_path)
    df = df[df["year"].astype(str) != "unknown"]
    companies = sorted(df["company"].unique().tolist())
    years     = sorted(df["year"].unique().astype(str).tolist(), reverse=True)
    tickers   = sorted(df["ticker"].unique().tolist())
    return companies, years, tickers


retriever, all_chunks, load_error = load_pipeline()
companies, years, tickers = load_metadata()
all_chunks_clean = [c for c in all_chunks if c.get("year", "") != "unknown"]

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="padding:0.8rem 0 0.3rem;">
        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;
                    letter-spacing:0.2em;color:#2563eb;text-transform:uppercase;
                    margin-bottom:0.25rem;">FinSight</div>
        <div style="font-size:0.95rem;font-weight:600;color:#94a3b8;line-height:1.3;">
            SEC 10-K<br>Intelligence
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("**Filter results**")

    selected_companies = st.multiselect(
        "Company", companies, default=[], placeholder="All companies"
    )
    selected_years = st.multiselect(
        "Year", years, default=[], placeholder="All years"
    )
    selected_sections = st.multiselect(
        "Section",
        ["1A — Risk Factors", "7 — MD&A", "7A — Market Risk"],
        default=[],
        placeholder="All sections"
    )

    st.divider()
    top_k = st.slider("Chunks retrieved", 3, 10, 5)
    alpha = st.slider(
        "Retrieval mode",
        0.0, 1.0, 0.5, 0.1,
        help="0 = keyword-only (BM25) · 1 = semantic-only · 0.5 = hybrid"
    )

    st.divider()
    n_filings = len(set(f"{c['ticker']}_{c['year']}" for c in all_chunks_clean))
    st.markdown(f"""
    <div style="font-size:0.73rem;color:#1e3050;line-height:2;">
        {len(all_chunks_clean)} chunks &nbsp;·&nbsp; {n_filings} filings<br>
        {len(companies)} companies &nbsp;·&nbsp; {len(years)} years<br><br>
        <a href="https://github.com/mittaladitya17/finsight-rag"
           target="_blank" style="color:#1e4080;text-decoration:none;">
           GitHub ↗
        </a>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────

st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">FinSight · SEC 10-K Intelligence · RAG Pipeline</div>
    <h1 class="hero-title">Ask anything about<br><em>fintech risk disclosures</em></h1>
    <p class="hero-sub">
        Query 50+ annual filings from Affirm, SoFi, LendingClub, Upstart, and
        Ally Financial (2021–2025). Every answer is grounded in the source text
        with section-level citations — no hallucinations, no guessing.
    </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────

tab_query, tab_explore, tab_about = st.tabs([
    "Query Filings", "Explore Corpus", "About & Methods"
])

# ══════════════════════════════════════════════
#  TAB 1 — QUERY
# ══════════════════════════════════════════════

with tab_query:

    # How it works
    st.markdown("""
    <div class="how-strip">
        <div class="how-card">
            <div class="how-num">01</div>
            <div class="how-title">Ask a question</div>
            <div class="how-desc">Type any question about credit risk, macro exposure, or regulatory disclosures.</div>
        </div>
        <div class="how-card">
            <div class="how-num">02</div>
            <div class="how-title">Retrieve passages</div>
            <div class="how-desc">Hybrid BM25 + semantic search finds the most relevant filing excerpts.</div>
        </div>
        <div class="how-card">
            <div class="how-num">03</div>
            <div class="how-title">Ground the answer</div>
            <div class="how-desc">Claude synthesises a response using only the retrieved source text.</div>
        </div>
        <div class="how-card">
            <div class="how-num">04</div>
            <div class="how-title">Verify the sources</div>
            <div class="how-desc">Every claim links back to a specific company, year, and 10-K section.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Example questions
    EXAMPLES = [
        ("Single company",   "How did Affirm describe its credit loss provision methodology across its filings?"),
        ("Cross-year",       "How did Upstart's language around macroeconomic risk change between 2022 and 2024?"),
        ("Cross-company",    "Compare how Affirm and SoFi describe regulatory risk in their filings."),
        ("Credit quality",   "What did LendingClub say about rising delinquency rates and charge-offs?"),
        ("Interest rates",   "How did Ally Financial describe exposure to interest rate risk?"),
        ("Underwriting",     "Which companies highlight AI or machine learning as part of their underwriting methodology?"),
    ]

    st.markdown('<div class="sec-head">Example questions — click to use</div>', unsafe_allow_html=True)

    # Display example cards in 3 columns
    ex_cols = st.columns(3)
    clicked_example = None
    for i, (tag, text) in enumerate(EXAMPLES):
        with ex_cols[i % 3]:
            if st.button(f"**{tag}**\n\n{text}", key=f"ex_{i}", use_container_width=True):
                clicked_example = text

    st.markdown('<div class="sec-head">Your question</div>', unsafe_allow_html=True)

    query_val = clicked_example or ""
    query = st.text_area(
        "",
        value=query_val,
        height=85,
        placeholder="e.g. How did Affirm describe credit risk across its filings?",
        label_visibility="collapsed",
        key="main_query"
    )

    run = st.button("Search filings →", type="primary")

    if load_error:
        st.error(f"Pipeline failed to load: {load_error}")
        st.stop()

    if run and query.strip():
        # Resolve filters
        import pandas as pd
        filter_ticker = None
        filter_year   = None
        filter_section = None

        if len(selected_companies) == 1:
            try:
                meta = pd.read_csv("data/metadata.csv")
                row  = meta[meta["company"] == selected_companies[0]]
                if not row.empty:
                    filter_ticker = row["ticker"].iloc[0]
            except Exception:
                pass

        if len(selected_years) == 1:
            filter_year = selected_years[0]

        if len(selected_sections) == 1:
            filter_section = selected_sections[0].split("—")[0].strip()

        with st.spinner("Searching filings..."):
            try:
                retrieved = retriever.retrieve(
                    query,
                    top_k=top_k,
                    alpha=alpha,
                    filter_ticker=filter_ticker,
                    filter_year=filter_year,
                )
                if filter_section:
                    retrieved = [r for r in retrieved if r["section"] == filter_section]
            except Exception as e:
                st.error(f"Retrieval error: {e}")
                st.stop()

        if not retrieved:
            st.markdown("""
            <div class="warn-box">
                No relevant passages found. Try broadening your filters or
                rephrasing the question with different keywords.
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.spinner("Generating answer..."):
                try:
                    from src.generation import generate_answer
                    result = generate_answer(query, retrieved)
                except Exception as e:
                    st.error(f"Generation error: {e}")
                    st.stop()

            SECTION_LABELS = {"1A": "Risk Factors", "7": "MD&A", "7A": "Market Risk"}
            sources_html = "".join([
                f'<span class="src-chip">'
                f'{c["company"]} · {c["year"]} · '
                f'{SECTION_LABELS.get(c["section"], c["section"])}'
                f'</span>'
                for c in retrieved
            ])

            st.markdown(f"""
            <div class="answer-wrap">
                <div class="answer-eyebrow">Answer — grounded in source text</div>
                <div class="answer-body">{result["answer"].replace(chr(10), "<br>")}</div>
                <div class="source-strip">{sources_html}</div>
                <div class="token-note">
                    {result["input_tokens"]} input · {result["output_tokens"]} output tokens
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander(f"View {len(retrieved)} retrieved source passages"):
                SECTION_LABELS = {"1A": "Risk Factors", "7": "MD&A", "7A": "Market Risk"}
                for chunk in retrieved:
                    sec_label = SECTION_LABELS.get(chunk["section"], chunk["section"])
                    st.markdown(f"""
                    <div class="chunk-wrap">
                        <div class="chunk-meta">
                            <span>{chunk["company"]} · {chunk["year"]} · {sec_label}</span>
                            <span class="chunk-score">relevance {chunk["score"]}</span>
                        </div>
                        <div class="chunk-body">{chunk["text"][:700]}...</div>
                    </div>
                    """, unsafe_allow_html=True)

    elif run and not query.strip():
        st.warning("Enter a question or click an example above.")

# ══════════════════════════════════════════════
#  TAB 2 — EXPLORE CORPUS
# ══════════════════════════════════════════════

with tab_explore:
    import pandas as pd
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    BASE = dict(
        template="plotly_dark",
        paper_bgcolor="#030810",
        plot_bgcolor="#030810",
        font=dict(color="#4b6080", family="IBM Plex Sans"),
        margin=dict(l=40, r=20, t=40, b=40),
    )

    try:
        meta = pd.read_csv("data/metadata.csv")
        meta = meta[meta["year"].astype(str) != "unknown"]
    except Exception:
        st.warning("metadata.csv not found.")
        st.stop()

    n_filings = len(meta.groupby(["ticker", "year"]))
    st.markdown(f"""
    <div class="stat-grid">
        <div class="stat-card">
            <div class="stat-num">{len(all_chunks_clean)}</div>
            <div class="stat-lbl">Chunks indexed</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">{n_filings}</div>
            <div class="stat-lbl">Filing-years</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">{len(companies)}</div>
            <div class="stat-lbl">Companies</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">{len(years)}</div>
            <div class="stat-lbl">Years covered</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">3</div>
            <div class="stat-lbl">Sections per filing</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Coverage heatmap
        pivot = meta.groupby(["company", "year"]).size().reset_index(name="n")
        pivot_wide = pivot.pivot(index="company", columns="year", values="n").fillna(0)
        fig = go.Figure(go.Heatmap(
            z=pivot_wide.values,
            x=pivot_wide.columns.astype(str).tolist(),
            y=pivot_wide.index.tolist(),
            colorscale=[[0, "#070e1c"], [0.01, "#0f2040"], [1, "#2563eb"]],
            showscale=False,
            text=pivot_wide.values.astype(int),
            texttemplate="%{text}",
            textfont=dict(size=11, color="#94a3b8"),
        ))
        fig.update_layout(**BASE, title="Filing Coverage by Company × Year",
                          height=320)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Sections per company
        comp_counts = meta.groupby(["company", "section"]).size().reset_index(name="n")
        SECTION_LABELS = {"1A": "Risk Factors", "7": "MD&A", "7A": "Market Risk"}
        comp_counts["sec_label"] = comp_counts["section"].map(SECTION_LABELS)
        colors = {"Risk Factors": "#2563eb", "MD&A": "#0ea5e9", "Market Risk": "#6366f1"}
        fig2 = go.Figure()
        for sec in ["Risk Factors", "MD&A", "Market Risk"]:
            sub = comp_counts[comp_counts["sec_label"] == sec]
            fig2.add_trace(go.Bar(
                x=sub["company"], y=sub["n"],
                name=sec,
                marker_color=colors[sec],
                opacity=0.85,
            ))
        fig2.update_layout(**BASE, title="Sections Indexed by Company",
                           barmode="stack", height=320,
                           legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="sec-head">What each section contains</div>',
                unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        **Item 1A — Risk Factors**
        The most analyst-relevant section. Management lists every material risk the business
        faces — credit quality, regulatory exposure, competition, macro sensitivity.
        Changes in language year-over-year are a signal in themselves.
        """)
    with c2:
        st.markdown("""
        **Item 7 — MD&A**
        Management's Discussion & Analysis. Explains the *why* behind the numbers —
        revenue drivers, provision changes, portfolio performance, strategic decisions.
        More narrative than the financial statements themselves.
        """)
    with c3:
        st.markdown("""
        **Item 7A — Market Risk**
        Quantitative disclosures on interest rate, credit, and liquidity risk.
        Contains sensitivity analyses showing how earnings change under stress scenarios.
        Critical for understanding balance sheet exposure.
        """)

    st.divider()
    st.markdown("**Full corpus index**")
    st.dataframe(
        meta[["company", "year", "section", "char_count"]]
        .sort_values(["company", "year"])
        .rename(columns={"char_count": "characters"}),
        use_container_width=True,
        height=340,
    )

# ══════════════════════════════════════════════
#  TAB 3 — ABOUT
# ══════════════════════════════════════════════

with tab_about:

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("""
        ## What FinSight does

        FinSight is a **Retrieval-Augmented Generation (RAG)** system built to answer
        analyst-grade questions about fintech company risk disclosures. It ingests SEC
        10-K filings, extracts the three most analytically relevant sections, and uses
        a hybrid retrieval pipeline to find the most relevant passages for any question.
        A language model then synthesises a grounded answer — every claim is traceable
        to a specific filing, company, year, and section.

        The system was built specifically around a gap in existing tooling: most financial
        research tools surface documents but don't answer questions about them. An analyst
        covering five fintech names across four years shouldn't need to read 60 annual
        reports to track how credit risk language has evolved. FinSight does that in seconds.
        """)

        st.markdown('<div class="sec-head">Pipeline architecture</div>',
                    unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            **Data ingestion**
            - SEC EDGAR via `sec-edgar-downloader`
            - Section extraction: BeautifulSoup + regex
            - Targets: Item 1A, Item 7, Item 7A

            **Chunking & indexing**
            - 512-word windows, 64-word overlap
            - Metadata context injected per chunk
            - `all-MiniLM-L6-v2` embeddings
            - ChromaDB persistent vector store
            """)
        with c2:
            st.markdown("""
            **Retrieval**
            - Hybrid: BM25 + dense cosine similarity
            - Configurable α weighting
            - Metadata filtering by ticker / year

            **Generation**
            - Claude Sonnet (Anthropic API)
            - Strict grounding prompt — no outside knowledge
            - Section-level citation on every claim
            """)

        st.markdown('<div class="sec-head">Why hybrid retrieval?</div>',
                    unsafe_allow_html=True)
        st.markdown("""
        Dense semantic search alone misses exact financial terms. "Net charge-off rate,"
        "CECL methodology," and "Tier 1 capital" are precise enough that a semantic model
        may not surface them if the query is phrased differently. BM25 handles exact keyword
        matching; dense search handles semantic similarity. The hybrid combination
        consistently outperforms either alone on financial text — which is why it is the
        industry standard in production RAG systems for finance.
        """)

    with col2:
        st.markdown("""
        **Companies covered**
        - Affirm Holdings (AFRM) — 2021–2024
        - SoFi Technologies (SOFI) — 2022–2025
        - LendingClub (LC) — 2022–2025
        - Upstart Holdings (UPST) — 2022–2024
        - Ally Financial (ALLY) — 2022–2025
        """)

        st.markdown("""
        **Questions this system answers well**
        - Single-company, single-year factual lookups
        - Cross-year language change analysis
        - Cross-company risk framework comparison
        - Specific methodology questions (provisioning, underwriting, hedging)
        """)

        st.markdown("""
        **Honest limitations**
        - Corpus covers 3 sections per filing only — not full documents
        - 15,000-character section cap may truncate long risk factor lists
        - LendingClub 2024 filing excluded (encoding error on source file)
        - No quantitative financial data — text disclosures only
        """)

        st.markdown("""
        **Tech stack**
        `Python` · `sentence-transformers` · `ChromaDB` · `rank-bm25` ·
        `sec-edgar-downloader` · `BeautifulSoup` · `Anthropic API` · `Streamlit`
        """)

    st.markdown('<div class="sec-head">In my mind</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="mind-box">
        <span class="mind-lbl">In my mind</span>
        The hardest part of this project wasn't the RAG pipeline — it was the data.
        SEC filings are inconsistent HTML with no guaranteed structure. Some companies
        use clean section headers; others bury Item 1A inside nested tables three levels
        deep. The extraction script had to be robust enough to handle both, which meant
        accepting some failures gracefully rather than crashing the entire pipeline on one
        bad file. LendingClub's 2024 filing is a good example — the HTML had a non-standard
        encoding marker that BeautifulSoup couldn't parse. Rather than engineer around one
        edge case, I logged it and moved on. A production system would need a fallback parser.
        <br><br>
        The second thing I learned: retrieval quality matters far more than model quality.
        A better LLM cannot fix a bad chunk. If the retrieved context doesn't contain the
        answer, the model either hallucinates or correctly says it doesn't know. Every hour
        I spent on chunking strategy and hybrid retrieval paid off more than any time spent
        on prompt engineering. The α slider in the sidebar exists because the optimal balance
        between BM25 and dense search depends on the query — precise financial terminology
        favours BM25; conceptual questions favour dense. Exposing that control directly to
        the user is a design decision, not just an engineering one.
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("""
    <div style="font-size:0.75rem; color:#1e3050; text-align:center; padding: 0.5rem 0;">
        Built by
        <a href="https://github.com/mittaladitya17"
           target="_blank" style="color:#1e4080; text-decoration:none;">Aditya Mittal</a>
        &nbsp;·&nbsp;
        <a href="https://github.com/mittaladitya17/finsight-rag"
           target="_blank" style="color:#1e4080; text-decoration:none;">GitHub ↗</a>
    </div>
    """, unsafe_allow_html=True)