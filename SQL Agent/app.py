import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from db import get_connection
from ai_helper import generate_sql

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SQL Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# Global CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Import fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── Reset & base ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 0 !important; }

    /* ── Palette ──
       Navy    #0A0F2E   (bg)
       Ink     #111827   (card bg)
       Indigo  #4F46E5   (accent primary)
       Violet  #7C3AED   (accent secondary)
       Sky     #38BDF8   (highlight)
       Muted   #6B7280
       Border  #1F2937
    */

    /* ── HEADER ── */
    .sql-header {
        background: linear-gradient(135deg, #0A0F2E 0%, #111827 60%, #1a1040 100%);
        padding: 1.5rem 2.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid #1F2937;
        margin-bottom: 0;
    }
    .sql-header-left { display: flex; align-items: center; gap: 0.85rem; }
    .sql-header-logo {
        width: 42px; height: 42px;
        background: linear-gradient(135deg, #4F46E5, #7C3AED);
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.3rem;
        box-shadow: 0 0 18px rgba(79,70,229,0.5);
    }
    .sql-header-title {
        font-size: 1.4rem; font-weight: 700;
        color: #F9FAFB; letter-spacing: -0.02em;
    }
    .sql-header-subtitle {
        font-size: 0.75rem; color: #6B7280; margin-top: 1px;
    }
    .sql-header-badge {
        background: linear-gradient(90deg, #4F46E5, #7C3AED);
        color: white; font-size: 0.68rem; font-weight: 600;
        padding: 0.25rem 0.75rem; border-radius: 999px;
        letter-spacing: 0.05em; text-transform: uppercase;
    }

    /* ── HERO STRIP ── */
    .hero-strip {
        background: linear-gradient(100deg, #0d1340 0%, #160d38 50%, #0A0F2E 100%);
        padding: 2.5rem 2.5rem 2rem;
        border-bottom: 1px solid #1F2937;
    }
    .hero-eyebrow {
        font-size: 0.72rem; font-weight: 600; letter-spacing: 0.12em;
        text-transform: uppercase; color: #38BDF8; margin-bottom: 0.6rem;
    }
    .hero-heading {
        font-size: 2.1rem; font-weight: 700; color: #F9FAFB;
        line-height: 1.2; letter-spacing: -0.03em; margin-bottom: 0.5rem;
    }
    .hero-heading span {
        background: linear-gradient(90deg, #4F46E5, #38BDF8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .hero-sub {
        color: #9CA3AF; font-size: 0.95rem; max-width: 560px; line-height: 1.6;
    }

    /* ── STAT PILLS ── */
    .stat-row { display: flex; gap: 1rem; margin-top: 1.5rem; flex-wrap: wrap; }
    .stat-pill {
        background: #111827; border: 1px solid #1F2937;
        border-radius: 10px; padding: 0.6rem 1.1rem;
        display: flex; align-items: center; gap: 0.5rem;
    }
    .stat-pill-icon { font-size: 1rem; }
    .stat-pill-label { font-size: 0.75rem; color: #6B7280; }
    .stat-pill-value { font-size: 0.85rem; font-weight: 600; color: #F9FAFB; }

    /* ── SECTION LABEL ── */
    .section-label {
        font-size: 0.7rem; font-weight: 600; letter-spacing: 0.1em;
        text-transform: uppercase; color: #6B7280;
        margin-bottom: 0.65rem; margin-top: 1.8rem;
    }

    /* ── STATUS BADGE ── */
    .status-ok {
        display: inline-flex; align-items: center; gap: 0.4rem;
        background: #052e16; border: 1px solid #166534;
        color: #4ade80; font-size: 0.8rem; font-weight: 500;
        padding: 0.35rem 0.9rem; border-radius: 999px;
    }
    .status-err {
        display: inline-flex; align-items: center; gap: 0.4rem;
        background: #2d0a0a; border: 1px solid #7f1d1d;
        color: #f87171; font-size: 0.8rem; font-weight: 500;
        padding: 0.35rem 0.9rem; border-radius: 999px;
    }

    /* ── CARD ── */
    .glass-card {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
    }
    .glass-card-title {
        font-size: 0.82rem; font-weight: 600; color: #D1D5DB;
        margin-bottom: 0.9rem; display: flex; align-items: center; gap: 0.4rem;
    }

    /* ── SUGGESTION CHIPS ── */
    .chip-grid { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem; }
    .chip {
        background: #1F2937; border: 1px solid #374151;
        color: #D1D5DB; font-size: 0.78rem; font-weight: 500;
        padding: 0.4rem 0.85rem; border-radius: 999px;
        cursor: pointer; transition: all 0.15s ease;
    }
    .chip:hover { background: #4F46E5; border-color: #4F46E5; color: white; }

    /* ── HISTORY ITEM ── */
    .history-item {
        background: #0d1117; border: 1px solid #1F2937;
        border-radius: 10px; padding: 0.75rem 1rem;
        margin-bottom: 0.55rem; cursor: pointer;
        transition: border-color 0.15s ease;
    }
    .history-item:hover { border-color: #4F46E5; }
    .history-q { font-size: 0.82rem; color: #E5E7EB; font-weight: 500; }
    .history-meta { font-size: 0.7rem; color: #4B5563; margin-top: 0.2rem; }
    .history-sql {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem; color: #6B7280;
        margin-top: 0.4rem; white-space: nowrap;
        overflow: hidden; text-overflow: ellipsis; max-width: 100%;
    }

    /* ── SQL CODE BLOCK ── */
    .sql-block {
        background: #0d1117; border: 1px solid #1F2937;
        border-radius: 10px; padding: 1rem 1.2rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem; color: #38BDF8;
        overflow-x: auto; white-space: pre-wrap;
    }

    /* ── DATAFRAME ── */
    .dataframe { border-radius: 10px !important; overflow: hidden; }

    /* ── FOOTER ── */
    .sql-footer {
        background: #0A0F2E;
        border-top: 1px solid #1F2937;
        padding: 1.2rem 2.5rem;
        margin-top: 3rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    .footer-brand { font-size: 0.8rem; color: #4B5563; }
    .footer-brand strong { color: #6B7280; }
    .footer-links { display: flex; gap: 1.5rem; }
    .footer-link { font-size: 0.75rem; color: #4B5563; text-decoration: none; }
    .footer-link:hover { color: #9CA3AF; }

    /* ── Streamlit widget overrides ── */
    .stTextInput > div > div > input {
        background: #111827 !important;
        border: 1px solid #374151 !important;
        border-radius: 10px !important;
        color: #F9FAFB !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
        padding: 0.65rem 1rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #4F46E5 !important;
        box-shadow: 0 0 0 3px rgba(79,70,229,0.2) !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #4F46E5, #7C3AED) !important;
        color: white !important; border: none !important;
        border-radius: 10px !important; font-weight: 600 !important;
        padding: 0.6rem 1.6rem !important; font-size: 0.88rem !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 4px 14px rgba(79,70,229,0.35) !important;
        transition: opacity 0.15s ease !important;
    }
    .stButton > button:hover { opacity: 0.88 !important; }
    .stFileUploader {
        background: #111827 !important;
        border: 2px dashed #374151 !important;
        border-radius: 14px !important;
    }
    .stDataFrame { border-radius: 12px; overflow: hidden; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #0d1117 !important;
        border-right: 1px solid #1F2937 !important;
    }
    [data-testid="stSidebar"] * { color: #D1D5DB !important; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: #0A0F2E; }
    ::-webkit-scrollbar-thumb { background: #1F2937; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Session State Init
# ─────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state["history"] = []   # list of {question, sql, rows}
if "prefill_question" not in st.session_state:
    st.session_state["prefill_question"] = ""


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="sql-header">
    <div class="sql-header-left">
        <div class="sql-header-logo">🤖</div>
        <div>
            <div class="sql-header-title">SQL Agent</div>
            <div class="sql-header-subtitle">Natural language → SQL, instantly</div>
        </div>
    </div>
    <div class="sql-header-badge">AI Powered</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HERO STRIP
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-strip">
    <div class="hero-eyebrow">🚀 Your data, in plain English</div>
    <div class="hero-heading">Ask questions.<br><span>Get SQL answers.</span></div>
    <div class="hero-sub">
        Upload any CSV, connect to MySQL, and query your data in plain English —
        no SQL knowledge needed. The AI writes the query, you get the results.
    </div>
    <div class="stat-row">
        <div class="stat-pill">
            <span class="stat-pill-icon">📂</span>
            <div>
                <div class="stat-pill-label">Step 1</div>
                <div class="stat-pill-value">Upload CSV</div>
            </div>
        </div>
        <div class="stat-pill">
            <span class="stat-pill-icon">🧠</span>
            <div>
                <div class="stat-pill-label">Step 2</div>
                <div class="stat-pill-value">Ask a Question</div>
            </div>
        </div>
        <div class="stat-pill">
            <span class="stat-pill-icon">⚡</span>
            <div>
                <div class="stat-pill-label">Step 3</div>
                <div class="stat-pill-value">Get Results</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR — History + Suggestions
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🕘 Query History")

    if not st.session_state["history"]:
        st.markdown(
            "<div style='color:#4B5563;font-size:0.8rem;margin-top:0.5rem;'>"
            "No queries yet. Ask your first question below.</div>",
            unsafe_allow_html=True
        )
    else:
        for i, item in enumerate(reversed(st.session_state["history"])):
            idx = len(st.session_state["history"]) - i
            with st.expander(f"#{idx}  {item['question'][:38]}…" if len(item['question']) > 38 else f"#{idx}  {item['question']}"):
                st.code(item["sql"], language="sql")
                st.caption(f"Returned {item['rows']} row(s)")
                if st.button("Re-run this question", key=f"rerun_{i}"):
                    st.session_state["prefill_question"] = item["question"]
                    st.rerun()

    st.divider()
    st.markdown("### 💡 Suggestions")
    suggestions = [
        "Show first 10 rows",
        "Count total records",
        "Find all unique values in a column",
        "Show rows where value > 100",
        "Sort by a column descending",
        "Average of numeric column",
        "Find duplicate entries",
        "Group and count by category",
    ]
    for s in suggestions:
        if st.button(s, key=f"sug_{s}"):
            st.session_state["prefill_question"] = s
            st.rerun()


# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────
main_col, spacer = st.columns([10, 1])

with main_col:

    # ── DB Connection Status ──────────────────
    st.markdown('<div class="section-label">Database Connection</div>', unsafe_allow_html=True)

    try:
        conn = get_connection()
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            st.markdown(
                f'<div class="status-ok">● Connected to <strong>{db_name}</strong></div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown('<div class="status-err">● MySQL not connected</div>', unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f'<div class="status-err">● Connection failed: {e}</div>', unsafe_allow_html=True)

    # ── Upload CSV ────────────────────────────
    st.markdown('<div class="section-label">Upload Dataset</div>', unsafe_allow_html=True)

    file = st.file_uploader(
        "Drop a CSV file here or click to browse",
        type=["csv"],
        label_visibility="collapsed"
    )

    if file is not None:
        try:
            df = pd.read_csv(file)
            original_rows = len(df)

            df = df.drop_duplicates()
            df = df.dropna(how="all")
            df.columns = (
                df.columns
                .str.strip()
                .str.replace(" ", "_")
                .str.replace("-", "_")
            )
            df = df.fillna(0)
            cleaned_rows = len(df)

            table_name = file.name.replace(".csv", "").lower()
            st.session_state["table_name"] = table_name
            st.session_state["columns"] = df.columns.tolist()

            engine = create_engine("mysql+pymysql://root:2678@localhost/sql_agent")
            df.to_sql(table_name, con=engine, if_exists="replace", index=False)

            # Success + Stats row
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Table", f"'{table_name}'")
            col2.metric("Original Rows", original_rows)
            col3.metric("Clean Rows", cleaned_rows)
            col4.metric("Columns", df.shape[1])

            st.markdown(
                f'<div class="status-ok" style="margin-bottom:1rem;">● Table <strong>{table_name}</strong> created in MySQL</div>',
                unsafe_allow_html=True
            )

            # Dataset Preview
            st.markdown('<div class="section-label">Dataset Preview</div>', unsafe_allow_html=True)
            st.dataframe(df.head(10), use_container_width=True)

            # Column list
            with st.expander("View all column names"):
                st.write(df.columns.tolist())

        except Exception as e:
            st.error(f"❌ Error saving data: {e}")

    # ── Ask Question ──────────────────────────
    if "table_name" in st.session_state:
        st.markdown('<div class="section-label">Ask Your Data</div>', unsafe_allow_html=True)

        # Suggestion chips (rendered as clickable buttons in a row)
        st.markdown("**Quick suggestions:**")
        chip_cols = st.columns(4)
        quick_chips = [
            "Show top 10 rows",
            "Count all records",
            "Find duplicates",
            "Show column averages",
        ]
        for i, chip in enumerate(quick_chips):
            with chip_cols[i]:
                if st.button(chip, key=f"chip_{chip}"):
                    st.session_state["prefill_question"] = chip
                    st.rerun()

        question = st.text_input(
            "Type your question",
            value=st.session_state["prefill_question"],
            placeholder="e.g. Show the top 5 customers by total sales",
            label_visibility="collapsed"
        )

        run_col, clear_col = st.columns([2, 8])
        with run_col:
            generate_clicked = st.button("⚡ Generate SQL", use_container_width=True)
        with clear_col:
            if st.button("Clear", use_container_width=False):
                st.session_state["prefill_question"] = ""
                st.rerun()

        if generate_clicked and question:
            try:
                table_name = st.session_state["table_name"]
                columns = st.session_state["columns"]

                with st.spinner("Generating SQL…"):
                    sql_query = generate_sql(question, table_name, columns)

                st.markdown('<div class="section-label">Generated SQL</div>', unsafe_allow_html=True)
                st.code(sql_query, language="sql")

                with st.spinner("Running query…"):
                    conn = get_connection()
                    result_df = pd.read_sql(sql_query, conn)
                    conn.close()

                st.markdown('<div class="section-label">Results</div>', unsafe_allow_html=True)

                if result_df.empty:
                    st.info("Query returned no rows.")
                else:
                    st.caption(f"{len(result_df)} row(s) returned")
                    st.dataframe(result_df, use_container_width=True)

                    csv_download = result_df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        "⬇ Download Results as CSV",
                        data=csv_download,
                        file_name="query_results.csv",
                        mime="text/csv"
                    )

                # Save to history
                st.session_state["history"].append({
                    "question": question,
                    "sql": sql_query,
                    "rows": len(result_df)
                })
                # Clear prefill after successful run
                st.session_state["prefill_question"] = ""

            except Exception as e:
                st.error(f"Error: {e}")

    elif file is None:
        # Empty-state nudge
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:2.5rem 1.5rem;margin-top:1.5rem;">
            <div style="font-size:2.5rem;margin-bottom:0.8rem;">📂</div>
            <div style="font-size:1rem;font-weight:600;color:#E5E7EB;margin-bottom:0.4rem;">
                Upload a CSV to get started
            </div>
            <div style="font-size:0.83rem;color:#6B7280;">
                Drag and drop a CSV file above. The AI will load it into MySQL<br>
                and let you query it in plain English.
            </div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="sql-footer">
    <div class="footer-brand">
        🤖 <strong>SQL Agent</strong> &nbsp;·&nbsp; Powered by AI &nbsp;·&nbsp; Built with Streamlit
    </div>
    <div class="footer-links">
        <span class="footer-link">MySQL + PyMySQL</span>
        <span class="footer-link">pandas</span>
        <span class="footer-link">SQLAlchemy</span>
    </div>
</div>
""", unsafe_allow_html=True)