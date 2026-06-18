"""
FinSight RAG — Financial Document Intelligence
Streamlit MVP app
"""

import os
import sys
import json
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="FinSight — SEC Filing Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  STYLE
# ─────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1100px;
}

/* ── Header ── */
.fs-header {
    background: #0a0f1e;
    border: 1px solid #1e2d4a;
    border-left: 4px solid #2563eb;
    border-radius: 8px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
}
.fs-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    color: #3b82f6;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.fs-title {
    font-size: 1.9rem;
    font-weight: 600;
    color: #f0f4ff;
    margin: 0 0 0.4rem 0;
    line-height: 1.2;
}
.fs-title span { color: #3b82f6; }
.fs-desc {
    color: #64748b;
    font-size: 0.88rem;
    margin: 0;
    max-width: 560px;
    line-height: 1.6;
}

/* ── Corpus stats ── */
.corpus-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.corpus-card {
    flex: 1;
    background: #0d1424;
    border: 1px solid #1e2d4a;
    border-radius: 8px;
    padding: 0.9rem 1.1rem;
}
.corpus-card .num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.5rem;
    font-weight: 600;
    color: #f0f4ff;
    line-height: 1;
}
.corpus-card .lbl {
    font-size: 0.72rem;
    color: #475569;
    margin-top: 0.25rem;
    letter-spacing: 0.04em;
}

/* ── Query box ── */
.query-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.14em;
    color: #3b82f6;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}

/* ── Answer card ── */
.answer-card {
    background: #0d1424;
    border: 1px solid #1e2d4a;
    border-radius: 10px;
    padding: 1.5rem 1.8rem;
    margin-top: 1rem;
}
.answer-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.16em;
    color: #3b82f6;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e2d4a;
}
.answer-body {
    color: #cbd5e1;
    font-size: 0.92rem;
    line-height: 1.75;
}

/* ── Source chip ── */
.source-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-top: 1rem;
    padding-top: 0.8rem;
    border-top: 1px solid #1e2d4a;
}
.source-chip {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    background: #0f1f3d;
    border: 1px solid #1e3a6e;
    color: #93c5fd;
    border-radius: 4px;
    padding: 0.2rem 0.6rem;
}

/* ── Chunk card ── */
.chunk-card {
    background: #080e1c;
    border: 1px solid #1e2d4a;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
}
.chunk-meta {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: #3b82f6;
    margin-bottom: 0.4rem;
    letter-spacing: 0.08em;
}
.chunk-score {
    float: right;
    color: #22c55e;
}
.chunk-text {
    font-size: 0.82rem;
    color: #64748b;
    line-height: 1.6;
}

/* ── Token badge ── */
.token-badge {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: #475569;
    margin-top: 0.5rem;
}

/* ── No result ── */
.no-result {
    background: #0d1a0d;
    border: 1px solid #14532d;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    color: #86efac;
    font-size: 0.88rem;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #070c18 !important;
    border-right: 1px solid #1e2d4a;
}
[data-testid="stSidebar"] * { color: #94a3b8 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label {
    color: #3b82f6 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    border-bottom: 1px solid #1e2d4a;
    background: transparent;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #475569;
    padding: 0.5rem 1.2rem;
    border: none;
    background: transparent;
}
.stTabs [aria-selected="true"] {
    color: #3b82f6 !important;
    border-bottom: 2px solid #3b82f6 !important;
    background: transparent !important;
}

/* ── Mind box ── */
.mind-box {
    background: #0f0a1e;
    border: 1px solid #3730a3;
    border-left: 3px solid #6366f1;
    border-radius: 8px;
    padding: 1rem 1.3rem;
    margin: 0.8rem 0;
    font-size: 0.88rem;
    color: #c7d2fe;
    line-height: 1.7;
}
.mind-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    color: #6366f1;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
    display: block;
}

/* ── Divider ── */
.fs-divider {
    border: none;
    border-top: 1px solid #1e2d4a;
    margin: 1.2rem 0;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  LOAD PIPELINE (cached)
# ─────────────────────────────────────────────

@st.cache_resource(show_spinner="Loading retrieval pipeline...")
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
    companies = sorted(df["company"].unique().tolist())
    years = sorted(df["year"].unique().astype(str).tolist(), reverse=True)
    tickers = sorted(df["ticker"].unique().tolist())
    return companies, years, tickers


retriever, all_chunks, load_error = load_pipeline()
companies, years, tickers = load_metadata()

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="padding: 0.8rem 0 0.5rem;">
        <div style="font-family:'IBM Plex Mono',monospace; font-size:0.62rem;
                    letter-spacing:0.18em; color:#3b82f6; text-transform:uppercase;
                    margin-bottom:0.3rem;">FinSight</div>
        <div style="font-size:1rem; font-weight:600; color:#f0f4ff; line-height:1.3;">
            SEC Filing<br>Intelligence
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""<div style="font-family:'IBM Plex Mono',monospace; font-size:0.65rem;
        letter-spacing:0.12em; color:#3b82f6; text-transform:uppercase;
        margin-bottom:0.4rem;">Filter by Company</div>""", unsafe_allow_html=True)
    selected_companies = st.multiselect(
        "", companies,
        default=[],
        label_visibility="collapsed",
        placeholder="All companies"
    )

    st.markdown("""<div style="font-family:'IBM Plex Mono',monospace; font-size:0.65rem;
        letter-spacing:0.12em; color:#3b82f6; text-transform:uppercase;
        margin: 0.8rem 0 0.4rem;">Filter by Year</div>""", unsafe_allow_html=True)
    selected_years = st.multiselect(
        "", years,
        default=[],
        label_visibility="collapsed",
        placeholder="All years"
    )

    st.divider()

    top_k = st.slider("Retrieved chunks", min_value=3, max_value=10, value=5)
    alpha = st.slider("BM25 / Dense balance", min_value=0.0, max_value=1.0,
                      value=0.5, step=0.1,
                      help="0 = BM25 only, 1 = Dense only, 0.5 = hybrid")

    st.divider()
    st.markdown(f"""
    <div style="font-size:0.75rem; color:#334155; line-height:1.8;">
        <span style="color:#475569;">Corpus</span><br>
        {len(all_chunks)} chunks indexed<br>
        {len(companies)} companies<br>
        {len(years)} filing years<br><br>
        <span style="color:#475569;">Built by</span><br>
        <a href="https://www.linkedin.com/in/mittaladitya17/"
           target="_blank" style="color:#3b82f6; text-decoration:none;">Aditya Mittal</a>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────

st.markdown("""
<div class="fs-header">
    <div class="fs-eyebrow">SEC 10-K Intelligence · RAG Pipeline · Fintech Coverage</div>
    <h1 class="fs-title">Ask anything about <span>fintech risk disclosures</span></h1>
    <p class="fs-desc">
        Natural language queries over 50+ SEC 10-K filings from Affirm, SoFi,
        LendingClub, Upstart, and Ally Financial (2021–2024).
        Every answer is grounded in source text with citations.
    </p>
</div>
""", unsafe_allow_html=True)

# Corpus stats bar
n_filings = len(set(f"{c['ticker']}_{c['year']}" for c in all_chunks))
n_sections = len(set(c["section"] for c in all_chunks))

st.markdown(f"""
<div class="corpus-row">
    <div class="corpus-card">
        <div class="num">{len(all_chunks)}</div>
        <div class="lbl">Indexed chunks</div>
    </div>
    <div class="corpus-card">
        <div class="num">{n_filings}</div>
        <div class="lbl">Filing-years</div>
    </div>
    <div class="corpus-card">
        <div class="num">{len(companies)}</div>
        <div class="lbl">Companies</div>
    </div>
    <div class="corpus-card">
        <div class="num">{len(years)}</div>
        <div class="lbl">Years covered</div>
    </div>
    <div class="corpus-card">
        <div class="num">{n_sections}</div>
        <div class="lbl">10-K sections</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────

tab_query, tab_explore, tab_about = st.tabs([
    "Query Filings", "Explore Corpus", "About this Project"
])

# ══════════════════════════════
#  TAB 1 — QUERY
# ══════════════════════════════

with tab_query:

    if load_error:
        st.error(f"Pipeline failed to load: {load_error}")
        st.stop()

    # Example queries
    EXAMPLES = [
        "How did Affirm describe credit risk in their filings?",
        "What risk factors did Upstart highlight related to macroeconomic conditions?",
        "How did LendingClub describe their credit loss provision methodology?",
        "Compare how Affirm and SoFi describe regulatory risk.",
        "How did Ally Financial's language around credit risk change over time?",
    ]

    st.markdown('<div class="query-label">Enter your question</div>',
                unsafe_allow_html=True)

    query = st.text_area(
        "",
        height=90,
        placeholder="e.g. How did Affirm describe credit risk across their filings?",
        label_visibility="collapsed",
        key="query_input"
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        run = st.button("Search Filings →", type="primary", use_container_width=True)
    with col2:
        example_pick = st.selectbox(
            "Or try an example",
            [""] + EXAMPLES,
            label_visibility="collapsed"
        )
        if example_pick:
            query = example_pick

    if run or example_pick:
        if not query.strip():
            st.warning("Enter a question first.")
        else:
            # Build filters
            filter_ticker = None
            filter_year = None
            if len(selected_companies) == 1:
                # Map company name back to ticker
                import pandas as pd
                meta = pd.read_csv("data/metadata.csv")
                row = meta[meta["company"] == selected_companies[0]]
                if not row.empty:
                    filter_ticker = row["ticker"].iloc[0]
            if len(selected_years) == 1:
                filter_year = selected_years[0]

            with st.spinner("Searching filings..."):
                try:
                    retrieved = retriever.retrieve(
                        query,
                        top_k=top_k,
                        alpha=alpha,
                        filter_ticker=filter_ticker,
                        filter_year=filter_year,
                    )
                except Exception as e:
                    st.error(f"Retrieval error: {e}")
                    st.stop()

            if not retrieved:
                st.markdown("""
                <div class="no-result">
                    No relevant chunks found. Try broadening your filters or
                    rephrasing the question.
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

                # Answer
                sources_html = "".join([
                    f'<span class="source-chip">{s}</span>'
                    for s in result["sources"]
                ])
                st.markdown(f"""
                <div class="answer-card">
                    <div class="answer-header">Answer</div>
                    <div class="answer-body">{result["answer"].replace(chr(10), "<br>")}</div>
                    <div class="source-row">{sources_html}</div>
                    <div class="token-badge">
                        {result["input_tokens"]} input tokens ·
                        {result["output_tokens"]} output tokens
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Retrieved chunks
                with st.expander(f"View {len(retrieved)} retrieved source chunks"):
                    for chunk in retrieved:
                        st.markdown(f"""
                        <div class="chunk-card">
                            <div class="chunk-meta">
                                {chunk['company']} · {chunk['year']} ·
                                Section {chunk['section']}
                                <span class="chunk-score">score {chunk['score']}</span>
                            </div>
                            <div class="chunk-text">{chunk['text'][:600]}...</div>
                        </div>
                        """, unsafe_allow_html=True)

# ══════════════════════════════
#  TAB 2 — EXPLORE CORPUS
# ══════════════════════════════

with tab_explore:
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go

    PLOTLY_BASE = dict(
        template="plotly_dark",
        paper_bgcolor="#070c18",
        plot_bgcolor="#070c18",
        font=dict(color="#94a3b8", family="IBM Plex Sans"),
        margin=dict(l=40, r=20, t=40, b=40),
    )

    try:
        meta = pd.read_csv("data/metadata.csv")
    except Exception:
        st.warning("metadata.csv not found.")
        st.stop()

    col1, col2 = st.columns(2)

    with col1:
        # Chunks per company
        company_counts = meta.groupby("company").size().reset_index(name="chunks")
        company_counts = company_counts.sort_values("chunks")
        fig = go.Figure(go.Bar(
            x=company_counts["chunks"],
            y=company_counts["company"],
            orientation="h",
            marker_color="#2563eb",
            opacity=0.85,
        ))
        fig.update_layout(**PLOTLY_BASE, title="Sections per Company",
                          height=300, xaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Coverage heatmap: company × year
        pivot = meta.groupby(["company", "year"]).size().reset_index(name="sections")
        pivot_wide = pivot.pivot(index="company", columns="year", values="sections").fillna(0)
        fig2 = go.Figure(go.Heatmap(
            z=pivot_wide.values,
            x=pivot_wide.columns.astype(str).tolist(),
            y=pivot_wide.index.tolist(),
            colorscale=[[0, "#0d1424"], [1, "#2563eb"]],
            showscale=False,
            text=pivot_wide.values.astype(int),
            texttemplate="%{text}",
        ))
        fig2.update_layout(**PLOTLY_BASE, title="Filing Coverage (sections)",
                           height=300)
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # Section breakdown
    sec_counts = meta.groupby("section").size().reset_index(name="count")
    sec_map = {"1A": "Risk Factors", "7": "MD&A", "7A": "Market Risk"}
    sec_counts["label"] = sec_counts["section"].map(sec_map).fillna(sec_counts["section"])

    col3, col4 = st.columns(2)
    with col3:
        fig3 = go.Figure(go.Bar(
            x=sec_counts["label"],
            y=sec_counts["count"],
            marker_color=["#2563eb", "#0ea5e9", "#6366f1"],
            opacity=0.85,
        ))
        fig3.update_layout(**PLOTLY_BASE, title="Sections by Type",
                           height=280, yaxis_title="Count")
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        # Char count distribution
        fig4 = go.Figure(go.Histogram(
            x=meta["char_count"],
            nbinsx=20,
            marker_color="#2563eb",
            opacity=0.8,
        ))
        fig4.update_layout(**PLOTLY_BASE, title="Section Length Distribution",
                           height=280, xaxis_title="Characters", yaxis_title="Count")
        st.plotly_chart(fig4, use_container_width=True)

    st.divider()
    st.markdown("**Full corpus metadata**")
    st.dataframe(
        meta[["company", "year", "section", "char_count"]].sort_values(
            ["company", "year"]),
        use_container_width=True,
        height=300,
    )

# ══════════════════════════════
#  TAB 3 — ABOUT
# ══════════════════════════════

with tab_about:

    st.markdown("""
    <div style="max-width: 700px;">
    <h3 style="color: #f0f4ff; font-weight: 600; margin-bottom: 0.3rem;">
        What this project does
    </h3>
    <p style="color: #64748b; font-size: 0.9rem; line-height: 1.75;">
        FinSight is a Retrieval-Augmented Generation (RAG) system built to answer
        analyst-grade questions about fintech company risk disclosures. It ingests
        SEC 10-K filings, extracts the three most analytically relevant sections,
        chunks and embeds them into a vector store, and retrieves relevant passages
        to ground a language model's answers. Every claim in an answer is traceable
        to a specific filing, year, and section.
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="fs-divider">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Pipeline architecture**
        - SEC EDGAR ingestion via `sec-edgar-downloader`
        - Section extraction: BeautifulSoup + regex
        - Chunking: 512-word windows, 64-word overlap
        - Embeddings: `all-MiniLM-L6-v2` (sentence-transformers)
        - Vector store: ChromaDB (cosine similarity)
        - Retrieval: Hybrid BM25 + dense (configurable α)
        - Generation: Claude Sonnet via Anthropic API
        """)
    with col2:
        st.markdown("""
        **Coverage**
        - Affirm Holdings (AFRM)
        - SoFi Technologies (SOFI)
        - LendingClub (LC)
        - Upstart Holdings (UPST)
        - Ally Financial (ALLY)

        **Sections indexed per filing**
        - Item 1A — Risk Factors
        - Item 7 — MD&A
        - Item 7A — Quantitative Market Risk
        """)

    st.markdown('<hr class="fs-divider">', unsafe_allow_html=True)

    st.markdown("""
    <div class="mind-box">
        <span class="mind-label">In my mind</span>
        The hardest part of this project wasn't the RAG pipeline — it was the data.
        SEC filings are inconsistent HTML with no standard structure. Some filings
        deliver clean section headers; others bury Item 1A three levels deep inside
        nested tables. The ingestion script had to be robust enough to handle both,
        which meant defaulting to regex over DOM traversal and accepting that some
        filings would fail gracefully rather than crash the pipeline.
        <br><br>
        The second thing I learned: retrieval quality matters more than model quality.
        A better LLM can't fix a bad chunk. If the retrieved context doesn't contain
        the answer, the model either hallucinates or correctly says "I don't know."
        The hybrid BM25 + dense approach was specifically motivated by financial text —
        terms like "net charge-off rate" and "CECL methodology" need exact keyword
        matching that semantic search alone misses.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="fs-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size: 0.78rem; color: #334155; line-height: 1.8;">
        Built by <a href="https://www.linkedin.com/in/mittaladitya17/"
        target="_blank" style="color: #3b82f6; text-decoration: none;">
        Aditya Mittal</a> · MS Data Science, Michigan State University ·
        <a href="https://github.com/mittaladitya17/finsight-rag"
        target="_blank" style="color: #3b82f6; text-decoration: none;">GitHub</a>
    </div>
    """, unsafe_allow_html=True)