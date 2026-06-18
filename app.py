"""FinSight — SEC 10-K Intelligence Platform"""

import os, json, time, requests
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="FinSight — Fintech Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg:#F8FAFC; --surface:#FFFFFF; --border:#E2E8F0;
  --t1:#0F172A; --t2:#334155; --t3:#64748B;
  --accent:#2563EB; --accent-l:#EFF6FF; --accent-m:#BFDBFE;
  --pill-bg:#EFF6FF; --pill-br:#BFDBFE; --pill-t:#1D4ED8;
  --card:#FFFFFF; --card-br:#E2E8F0;
  --chunk:#F8FAFC;
  --mind-bg:#EEF2FF; --mind-br:#C7D2FE; --mind-acc:#4338CA; --mind-t:#312E81;
  --warn-bg:#F0FDF4; --warn-br:#BBF7D0; --warn-t:#15803D;
  --score:#15803D;
  --sep:#E2E8F0;
}
@media(prefers-color-scheme:dark){
  :root{
    --bg:#0F172A; --surface:#1E293B; --border:#334155;
    --t1:#F1F5F9; --t2:#CBD5E1; --t3:#64748B;
    --accent:#60A5FA; --accent-l:#172554; --accent-m:#1E3A8A;
    --pill-bg:#172554; --pill-br:#1E3A8A; --pill-t:#93C5FD;
    --card:#1E293B; --card-br:#334155;
    --chunk:#0F172A;
    --mind-bg:#1E1B4B; --mind-br:#312E81; --mind-acc:#818CF8; --mind-t:#C7D2FE;
    --warn-bg:#052E16; --warn-br:#166534; --warn-t:#4ADE80;
    --score:#4ADE80;
    --sep:#334155;
  }
}
[data-theme="dark"]{
  --bg:#0F172A!important; --surface:#1E293B!important; --border:#334155!important;
  --t1:#F1F5F9!important; --t2:#CBD5E1!important; --t3:#64748B!important;
  --accent:#60A5FA!important; --accent-l:#172554!important; --accent-m:#1E3A8A!important;
  --pill-bg:#172554!important; --pill-br:#1E3A8A!important; --pill-t:#93C5FD!important;
  --card:#1E293B!important; --card-br:#334155!important;
  --chunk:#0F172A!important;
  --mind-bg:#1E1B4B!important; --mind-br:#312E81!important;
  --mind-acc:#818CF8!important; --mind-t:#C7D2FE!important;
  --score:#4ADE80!important; --sep:#334155!important;
}

html,body,[class*="css"]{font-family:'Inter',sans-serif;}
.block-container{padding:0 2rem 3rem;max-width:1200px;}

/* Brand — renders ABOVE tabs via st.markdown before st.tabs() */
.brand{
  display:flex;align-items:center;justify-content:space-between;
  padding:1.2rem 0 0.8rem;
  border-bottom:1px solid var(--sep);
  margin-bottom:0.2rem;
}
.brand-name{
  font-family:'JetBrains Mono',monospace;font-size:1.1rem;
  font-weight:600;color:var(--t1);letter-spacing:0.04em;
}
.brand-name em{color:var(--accent);font-style:normal;}
.brand-right{font-size:0.72rem;color:var(--t3);}
.brand-right a{color:var(--accent);text-decoration:none;}

/* Hero */
.hero{padding:2.5rem 0 2rem;border-bottom:1px solid var(--sep);margin-bottom:0.5rem;}
.hero-kicker{
  font-family:'JetBrains Mono',monospace;font-size:0.62rem;
  letter-spacing:0.2em;color:var(--accent);text-transform:uppercase;margin-bottom:0.8rem;
}
.hero-h1{font-size:2.4rem;font-weight:700;color:var(--t1);line-height:1.15;margin:0 0 1rem;}
.hero-h1 em{color:var(--accent);font-style:normal;}
.hero-lead{font-size:0.95rem;color:var(--t2);max-width:540px;line-height:1.75;margin:0 0 1.8rem;}
.pills{display:flex;gap:0.45rem;flex-wrap:wrap;margin-bottom:2rem;}
.pill{
  font-family:'JetBrains Mono',monospace;font-size:0.61rem;letter-spacing:0.06em;
  background:var(--pill-bg);border:1px solid var(--pill-br);color:var(--pill-t);
  border-radius:4px;padding:0.22rem 0.65rem;
}

/* Stats */
.stats{
  display:grid;grid-template-columns:repeat(5,1fr);gap:1px;
  background:var(--sep);border:1px solid var(--sep);border-radius:10px;
  overflow:hidden;margin-bottom:2.5rem;
}
.stat{background:var(--card);padding:1.1rem 1.4rem;}
.stat-n{font-family:'JetBrains Mono',monospace;font-size:1.7rem;font-weight:600;color:var(--t1);line-height:1;}
.stat-l{font-size:0.68rem;color:var(--t3);margin-top:0.25rem;}

/* How */
.how{
  display:grid;grid-template-columns:repeat(4,1fr);gap:1px;
  background:var(--sep);border:1px solid var(--sep);border-radius:10px;overflow:hidden;
}
.how-c{background:var(--card);padding:1.1rem 1.3rem;}
.how-n{font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:var(--accent);letter-spacing:0.1em;margin-bottom:0.35rem;}
.how-t{font-size:0.82rem;font-weight:600;color:var(--t1);margin-bottom:0.25rem;}
.how-d{font-size:0.75rem;color:var(--t3);line-height:1.55;}

/* Section label */
.slabel{
  font-family:'JetBrains Mono',monospace;font-size:0.6rem;letter-spacing:0.18em;
  color:var(--accent);text-transform:uppercase;
  margin:2rem 0 0.8rem;padding-bottom:0.4rem;border-bottom:1px solid var(--sep);
}

/* Coverage card */
.cov{background:var(--card);border:1px solid var(--card-br);border-radius:8px;padding:0.9rem 1.1rem;}
.cov-t{font-family:'JetBrains Mono',monospace;font-size:0.72rem;font-weight:600;color:var(--accent);margin-bottom:0.2rem;}
.cov-n{font-size:0.8rem;font-weight:600;color:var(--t1);margin-bottom:0.25rem;}
.cov-s{font-size:0.68rem;color:var(--t3);}

/* Answer */
.answer{
  background:var(--card);border:1px solid var(--sep);
  border-top:3px solid var(--accent);border-radius:10px;
  padding:1.6rem 2rem;margin-top:1rem;
}
.answer-eye{
  font-family:'JetBrains Mono',monospace;font-size:0.6rem;letter-spacing:0.16em;
  color:var(--accent);text-transform:uppercase;margin-bottom:0.9rem;
}
.answer-body{font-size:0.92rem;color:var(--t2);line-height:1.85;}
.chips{display:flex;flex-wrap:wrap;gap:0.35rem;margin-top:1rem;padding-top:0.8rem;border-top:1px solid var(--sep);}
.chip{
  font-family:'JetBrains Mono',monospace;font-size:0.6rem;
  background:var(--accent-l);border:1px solid var(--accent-m);color:var(--accent);
  border-radius:3px;padding:0.18rem 0.55rem;
}
.toks{font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:var(--t3);margin-top:0.5rem;opacity:0.6;}

/* Chunk */
.chunk{background:var(--chunk);border:1px solid var(--sep);border-radius:7px;padding:0.9rem 1.1rem;margin-bottom:0.45rem;}
.chunk-m{font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:var(--t3);display:flex;justify-content:space-between;margin-bottom:0.3rem;}
.chunk-s{color:var(--score);font-weight:600;}
.chunk-b{font-size:0.82rem;color:var(--t2);line-height:1.65;}

/* Mind */
.mind{
  background:var(--mind-bg);border:1px solid var(--mind-br);
  border-left:3px solid var(--mind-acc);border-radius:8px;
  padding:1.1rem 1.5rem;font-size:0.88rem;color:var(--mind-t);line-height:1.8;margin:1.2rem 0;
}
.mind-l{
  font-family:'JetBrains Mono',monospace;font-size:0.58rem;letter-spacing:0.16em;
  color:var(--mind-acc);text-transform:uppercase;display:block;margin-bottom:0.45rem;
}

/* Warn */
.warn{background:var(--warn-bg);border:1px solid var(--warn-br);border-radius:7px;padding:0.8rem 1.1rem;font-size:0.84rem;color:var(--warn-t);}

/* Footer */
.foot{font-size:0.72rem;color:var(--t3);text-align:center;padding:1.5rem 0 0.5rem;border-top:1px solid var(--sep);margin-top:2rem;}
.foot a{color:var(--accent);text-decoration:none;}

/* Tabs — styled but Streamlit controls placement */
.stTabs [data-baseweb="tab-list"]{gap:0;border-bottom:2px solid var(--sep);background:transparent;}
.stTabs [data-baseweb="tab"]{
  font-family:'JetBrains Mono',monospace;font-size:0.65rem;letter-spacing:0.1em;
  text-transform:uppercase;color:var(--t3);padding:0.6rem 1.4rem;border:none;background:transparent;
}
.stTabs [aria-selected="true"]{color:var(--accent)!important;border-bottom:2px solid var(--accent)!important;background:transparent!important;font-weight:600;}
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
TICKERS_META = {
    "AFRM": {"name":"Affirm Holdings",    "sector":"BNPL",         "cik":"0001820953"},
    "SOFI": {"name":"SoFi Technologies",  "sector":"Neobank",      "cik":"0001393818"},
    "LC":   {"name":"LendingClub",        "sector":"Marketplace",  "cik":"0001409970"},
    "UPST": {"name":"Upstart Holdings",   "sector":"AI Lending",   "cik":"0001647639"},
    "ALLY": {"name":"Ally Financial",     "sector":"Digital Bank", "cik":"0000040729"},
    "PGY":  {"name":"Pagaya Technologies","sector":"AI Credit",    "cik":"0001883085"},
    "BFH":  {"name":"Bread Financial",    "sector":"Credit Cards", "cik":"0001101239"},
    "OPFI": {"name":"OppFi",              "sector":"Subprime",     "cik":"0001818502"},
}
SECTION_MAP = {"1A":"Risk Factors","7":"MD&A","7A":"Market Risk"}

# ── Pipeline ────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading pipeline...")
def load_pipeline():
    try:
        from src.retrieval import load_resources, HybridRetriever
        model, collection, chunks = load_resources()
        return HybridRetriever(model, collection, chunks), chunks, None
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
    return by_ticker, sorted(df["year"].astype(str).unique().tolist(), reverse=True)

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_xbrl(cik, concept, unit="USD"):
    url = f"https://data.sec.gov/api/xbrl/companyconcept/{cik}/{concept}.json"
    try:
        r = requests.get(url, headers={"User-Agent":"FinSightRAG aditya@msu.edu"}, timeout=8)
        if r.status_code != 200: return []
        facts = r.json().get("units",{}).get(unit,[])
        annual = [f for f in facts if f.get("form") in ("10-K","20-F") and f.get("val") is not None]
        seen = {}
        for f in annual:
            yr = f.get("end","")[:4]
            if yr not in seen: seen[yr] = f["val"]
        return [{"year":k,"value":v} for k,v in sorted(seen.items())]
    except: return []

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_financials(tickers_meta):
    CONCEPTS = {
        "Revenue":     ("us-gaap","Revenues","USD"),
        "Net Income":  ("us-gaap","NetIncomeLoss","USD"),
        "Total Assets":("us-gaap","Assets","USD"),
    }
    out = {}
    for ticker, meta in tickers_meta.items():
        out[ticker] = {}
        for label,(ns,concept,unit) in CONCEPTS.items():
            out[ticker][label] = fetch_xbrl(meta["cik"], f"{ns}/{concept}", unit)
        time.sleep(0.12)
    return out

retriever, all_chunks, load_error = load_pipeline()
ticker_years, all_years = load_metadata()
chunks_clean = [c for c in all_chunks if str(c.get("year","")) != "unknown"]

# ── BRAND BAR — rendered before st.tabs() so it sits above the tab strip ───────
n_filings = len(set(f"{c['ticker']}_{c['year']}" for c in chunks_clean))
st.markdown(f"""
<div class="brand">
  <div class="brand-name">Fin<em>Sight</em></div>
  <div class="brand-right">
    {len(chunks_clean)} chunks &nbsp;·&nbsp; {n_filings} filings &nbsp;·&nbsp;
    8 companies &nbsp;·&nbsp;
    <a href="https://github.com/mittaladitya17/finsight-rag" target="_blank">
      GitHub ↗
    </a>
  </div>
</div>
""", unsafe_allow_html=True)

# ── TABS ─────────────────────────────────────────────────────────────────────────
tab_overview, tab_query, tab_analytics, tab_corpus = st.tabs([
    "Overview", "Query Filings", "Financial Analytics", "Corpus"
])

# ════════════════════════════════════════════════════════
#  OVERVIEW
# ════════════════════════════════════════════════════════
with tab_overview:
    st.markdown(f"""
    <div class="hero">
      <div class="hero-kicker">Fintech · SEC 10-K Intelligence · RAG + XBRL</div>
      <h1 class="hero-h1">Ask anything about<br><em>fintech risk disclosures</em></h1>
      <p class="hero-lead">
        FinSight combines a hybrid retrieval pipeline over SEC 10-K filings with
        structured XBRL financial data — giving analysts both the narrative context
        and the numbers, in one place, with citations.
      </p>
      <div class="pills">
        <span class="pill">8 companies</span>
        <span class="pill">{n_filings} filing-years</span>
        <span class="pill">{len(chunks_clean)} indexed chunks</span>
        <span class="pill">Hybrid BM25 + semantic retrieval</span>
        <span class="pill">XBRL financial metrics</span>
        <span class="pill">Claude Sonnet generation</span>
      </div>
      <div class="stats">
        <div class="stat"><div class="stat-n">{len(chunks_clean)}</div><div class="stat-l">Chunks indexed</div></div>
        <div class="stat"><div class="stat-n">{n_filings}</div><div class="stat-l">Filing-years</div></div>
        <div class="stat"><div class="stat-n">8</div><div class="stat-l">Companies</div></div>
        <div class="stat"><div class="stat-n">3</div><div class="stat-l">Sections / filing</div></div>
        <div class="stat"><div class="stat-n">5</div><div class="stat-l">Years covered</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="slabel">Companies covered</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, (ticker, meta) in enumerate(TICKERS_META.items()):
        yrs = ticker_years.get(ticker, [])
        yr_str = f"{min(yrs)}–{max(yrs)}" if yrs else "—"
        with cols[i % 4]:
            st.markdown(f"""
            <div class="cov">
              <div class="cov-t">{ticker}</div>
              <div class="cov-n">{meta['name']}</div>
              <div class="cov-s">{meta['sector']} · {yr_str}</div>
            </div>
            """, unsafe_allow_html=True)

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

    st.markdown('<div class="slabel">Honest limitations</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        - 15,000-character section cap may truncate long risk factor lists
        - LendingClub 2024 and Upstart 2025 excluded due to HTML encoding errors
        - Text sections only — no footnotes, exhibits, or financial statement tables
        """)
    with col2:
        st.markdown("""
        - XBRL coverage varies by company and year
        - Nu Holdings excluded — files as foreign private issuer (20-F not 10-K)
        - Answers are grounded in disclosed text only. Not investment advice.
        """)

    st.markdown("""
    <div class="mind">
      <span class="mind-l">In my mind</span>
      The hardest part wasn't the RAG pipeline — it was the data. SEC filings look
      uniform from the outside but are structurally inconsistent underneath.
      LendingClub's 2024 filing has a non-standard HTML encoding marker that
      BeautifulSoup can't parse. Rather than engineer around one edge case,
      I logged it and moved on — a production system would need a fallback parser chain.
      <br><br>
      The XBRL layer came from realising that text answers alone aren't enough for an
      analyst. If someone asks how Affirm described revenue growth, the next question is
      always "so what were the actual numbers?" The SEC's XBRL API gives those numbers
      for free, structured, and machine-readable — the same data Bloomberg ingests.
      Pairing text retrieval with quantitative data is what separates this from a demo.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="foot">
      Built by <a href="https://github.com/mittaladitya17" target="_blank">Aditya Mittal</a>
      &nbsp;·&nbsp;
      <a href="https://github.com/mittaladitya17/finsight-rag" target="_blank">GitHub ↗</a>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
#  QUERY FILINGS
# ════════════════════════════════════════════════════════
with tab_query:
    if load_error:
        st.error(f"Pipeline failed to load: {load_error}")
        st.stop()

    fc1, fc2, fc3, fc4 = st.columns([2, 1.5, 1.5, 1])
    with fc1:
        sel_companies = st.multiselect(
            "Company", list(TICKERS_META.keys()),
            format_func=lambda t: f"{t} — {TICKERS_META[t]['name']}",
            placeholder="All companies"
        )
    with fc2:
        sel_years = st.multiselect("Year", all_years, placeholder="All years")
    with fc3:
        sel_section = st.selectbox(
            "Section", ["All sections","1A — Risk Factors","7 — MD&A","7A — Market Risk"]
        )
    with fc4:
        top_k = st.slider("Chunks", 3, 10, 5)

    alpha = st.slider(
        "Retrieval: ← keyword  |  semantic →", 0.0, 1.0, 0.5, 0.1,
        help="0 = BM25 keyword-only · 1 = dense semantic only · 0.5 = hybrid"
    )

    EXAMPLES = [
        ("Single company",  "How did Affirm describe its credit loss provision methodology?"),
        ("Cross-year",      "How did Upstart's language around macro risk change between 2022 and 2024?"),
        ("Cross-company",   "Compare how Affirm and SoFi describe regulatory risk."),
        ("AI underwriting", "Which companies describe using AI or ML in their underwriting process?"),
        ("Credit quality",  "What did LendingClub and OppFi say about rising delinquency rates?"),
        ("Interest rates",  "How did Ally Financial and Bread Financial describe interest rate exposure?"),
    ]

    st.markdown('<div class="slabel">Example questions — click to use</div>', unsafe_allow_html=True)
    ex_cols = st.columns(3)
    clicked = None
    for i, (tag, txt) in enumerate(EXAMPLES):
        with ex_cols[i % 3]:
            if st.button(f"**{tag}**  \n{txt}", key=f"ex{i}", use_container_width=True):
                clicked = txt

    st.markdown('<div class="slabel">Your question</div>', unsafe_allow_html=True)
    query = st.text_area(
        "", value=clicked or "", height=80,
        placeholder="Type your question here…",
        label_visibility="collapsed", key="q"
    )
    run = st.button("Search filings →", type="primary")

    if run and query.strip():
        import pandas as pd
        filter_ticker = sel_companies[0] if len(sel_companies) == 1 else None
        filter_year   = sel_years[0]     if len(sel_years)     == 1 else None
        filter_sec    = sel_section.split("—")[0].strip() if sel_section != "All sections" else None

        with st.spinner("Retrieving relevant passages…"):
            try:
                retrieved = retriever.retrieve(query, top_k=top_k, alpha=alpha,
                                               filter_ticker=filter_ticker, filter_year=filter_year)
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

# ════════════════════════════════════════════════════════
#  FINANCIAL ANALYTICS
# ════════════════════════════════════════════════════════
with tab_analytics:
    import pandas as pd
    import plotly.graph_objects as go

    CHART = dict(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", size=12),
        margin=dict(l=50, r=20, t=45, b=40),
    )
    COLORS = ["#2563EB","#16A34A","#D97706","#7C3AED","#DB2777","#0891B2","#EA580C","#1D4ED8"]

    st.markdown('<div class="slabel">Live financial data from SEC XBRL API</div>', unsafe_allow_html=True)
    st.caption("Revenue, net income, and total assets pulled directly from SEC structured filings. Coverage varies by company and year.")

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
            fin_data = fetch_financials({t: TICKERS_META[t] for t in sel_tickers})

        metric = st.radio("Metric", ["Revenue","Net Income","Total Assets"], horizontal=True)

        fig = go.Figure()
        for i, ticker in enumerate(sel_tickers):
            series = fin_data.get(ticker,{}).get(metric,[])
            if not series: continue
            yrs  = [int(d["year"]) for d in series]
            vals = [d["value"]/1e9  for d in series]
            fig.add_trace(go.Scatter(
                x=yrs, y=vals, name=ticker,
                mode="lines+markers",
                line=dict(color=COLORS[i%len(COLORS)], width=2.5),
                marker=dict(size=7),
                hovertemplate=f"<b>{ticker}</b><br>%{{x}}: $%{{y:.2f}}B<extra></extra>"
            ))
        fig.update_layout(**CHART,
            title=f"{metric} (USD Billions)",
            xaxis=dict(title="Year", tickformat="d", showgrid=False),
            yaxis=dict(title="USD Billions", showgrid=True, gridcolor="rgba(100,116,139,0.15)"),
            legend=dict(orientation="h", y=-0.18),
            height=420,
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('<div class="slabel">Latest available value</div>', unsafe_allow_html=True)
        bar_data = []
        for ticker in sel_tickers:
            series = fin_data.get(ticker,{}).get(metric,[])
            if series:
                latest = sorted(series, key=lambda x: x["year"])[-1]
                bar_data.append({"ticker":ticker,"year":latest["year"],"value":latest["value"]/1e9})

        if bar_data:
            bdf = pd.DataFrame(bar_data).sort_values("value", ascending=True)
            fig2 = go.Figure(go.Bar(
                x=bdf["value"], y=bdf["ticker"], orientation="h",
                marker_color=COLORS[:len(bdf)],
                text=[f"${v:.2f}B ({yr})" for v,yr in zip(bdf["value"],bdf["year"])],
                textposition="outside",
                hovertemplate="<b>%{y}</b><br>$%{x:.2f}B<extra></extra>"
            ))
            fig2.update_layout(**CHART,
                title=f"Latest {metric} (USD Billions)",
                xaxis_title="USD Billions",
                height=max(260, len(bar_data)*55),
            )
            st.plotly_chart(fig2, use_container_width=True)

        with st.expander("Raw data table"):
            rows_out = []
            for ticker in sel_tickers:
                for m in ["Revenue","Net Income","Total Assets"]:
                    for entry in fin_data.get(ticker,{}).get(m,[]):
                        rows_out.append({
                            "Ticker":ticker,"Company":TICKERS_META[ticker]["name"],
                            "Metric":m,"Year":entry["year"],
                            "Value ($B)":round(entry["value"]/1e9,3),
                        })
            if rows_out:
                st.dataframe(pd.DataFrame(rows_out).sort_values(["Ticker","Metric","Year"]),
                             use_container_width=True, height=350)
            else:
                st.info("No XBRL data returned for selected companies.")

        st.markdown("""
        <div class="mind">
          <span class="mind-l">What you're seeing</span>
          These numbers come directly from the SEC's XBRL API — the same structured data
          that Bloomberg and FactSet ingest. Not scraped, not estimated: machine-readable
          financial facts submitted by the companies as part of their SEC filings.
          Coverage gaps exist where companies filed using non-standard XBRL taxonomies.
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
#  CORPUS
# ════════════════════════════════════════════════════════
with tab_corpus:
    import pandas as pd
    import plotly.graph_objects as go

    CHART2 = dict(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", size=12),
        margin=dict(l=50, r=20, t=45, b=40),
    )

    try:
        meta = pd.read_csv("data/metadata.csv")
        meta = meta[meta["year"].astype(str) != "unknown"]
    except Exception:
        st.warning("metadata.csv not found.")
        st.stop()

    pivot = meta.groupby(["ticker","year"]).size().reset_index(name="n")
    pivot_wide = pivot.pivot(index="ticker",columns="year",values="n").fillna(0)

    fig = go.Figure(go.Heatmap(
        z=pivot_wide.values,
        x=pivot_wide.columns.astype(str).tolist(),
        y=pivot_wide.index.tolist(),
        colorscale=[[0,"#EFF6FF"],[0.01,"#BFDBFE"],[1,"#2563EB"]],
        showscale=False,
        text=pivot_wide.values.astype(int),
        texttemplate="%{text}",
        textfont=dict(size=12),
    ))
    fig.update_layout(**CHART2, title="Sections indexed per company × year", height=340)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        sec_counts = meta.groupby("section").size().reset_index(name="count")
        sec_counts["label"] = sec_counts["section"].map(SECTION_MAP)
        fig2 = go.Figure(go.Bar(
            x=sec_counts["label"], y=sec_counts["count"],
            marker_color=["#2563EB","#16A34A","#7C3AED"], opacity=0.85,
        ))
        fig2.update_layout(**CHART2, title="Sections by type", height=280)
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        cc = meta.groupby("ticker").size().reset_index(name="n").sort_values("n")
        fig3 = go.Figure(go.Bar(
            x=cc["n"], y=cc["ticker"], orientation="h",
            marker_color="#2563EB", opacity=0.85,
        ))
        fig3.update_layout(**CHART2, title="Sections per company", height=280)
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<div class="slabel">Section reference</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        **Item 1A — Risk Factors**
        Every material risk the business faces. Changes in language year-over-year
        are a signal in themselves — a new risk appearing in 2023 is worth investigating.
        """)
    with c2:
        st.markdown("""
        **Item 7 — MD&A**
        Management explains the *why* behind the numbers. More candid than the press
        release, more narrative than the financial statements.
        """)
    with c3:
        st.markdown("""
        **Item 7A — Market Risk**
        Quantitative sensitivity disclosures. Shows how earnings change under rate
        stress scenarios — critical for understanding balance sheet exposure.
        """)

    st.markdown('<div class="slabel">Full index</div>', unsafe_allow_html=True)
    st.dataframe(
        meta[["ticker","company","year","section","char_count"]]
        .rename(columns={"char_count":"chars"})
        .sort_values(["ticker","year"]),
        use_container_width=True, height=380
    )