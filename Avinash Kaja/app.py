import time
from pathlib import Path
import streamlit as st
import pandas as pd
from utils.file_utils import read_file
from utils.preprocessing import preprocess_text
from utils.topic_modeling import extract_topics, generate_pyldavis
from utils.summarizer import summarize
from utils.sentiment import get_sentiment
from utils.visualization import show_wordcloud, plot_similarity_heatmap, show_card
from utils.cosine_sim import compute_cosine_similarity
from utils.semantic_search import build_index, query
from utils.language import detect_language
from utils.translate import translate_to_english
from utils.report import generate_pdf

st.set_page_config(page_title="NarrativeNexus Pro", layout="wide", page_icon="🧠")

# ------------------ CSS (NEON TITLE + fallback styles) ------------------
assets_css = Path("assets/custom.css")
if assets_css.exists():
    with open(assets_css, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.markdown(
        """
        <style>
        .glass-card {
            padding: 15px;
            border-radius: 12px;
            background: #1c0b2c;
            color: white;
            margin-bottom: 12px;
        }
        .neon-title {
            text-align: center;
            font-size: 42px;
            font-weight: 900;
            font-family: 'Poppins', sans-serif;
            color: #ffffff;
            letter-spacing: 4px;
            text-shadow: 
                0 0 5px #00eaff,
                0 0 10px #00eaff,
                0 0 20px #00eaff,
                0 0 40px #00bcd4;
            animation: glow 1.8s infinite alternate;
            margin-top: 10px;
            margin-bottom: 20px;
        }
        @keyframes glow {
            from { text-shadow: 0 0 5px #00eaff, 0 0 20px #00bcd4; }
            to   { text-shadow: 0 0 20px #00eaff, 0 0 40px #00bcd4; }
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

# ------------- Session State ----------------
session_defaults = {
    "raw_docs": [],
    "cleaned_docs": [],
    "summary": "",
    "topics_data": None,
    "sentiments": [],
    "history": [],
}

for key, val in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ----------------- Sidebar -------------------
page = st.sidebar.radio(
    "Navigate",
    [
        "Upload",
        "Results (Tabs)",
        "Cosine Similarity",
        "Semantic Search",
        "History",
        "Download",
    ],
)

# ----------------- Neon Title ----------------
# ----------------- Neon Title ----------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700&display=swap');

.neon-title {
    font-family: 'Poppins', sans-serif;
    text-align: center;
    font-size: 46px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-top: -5px;
    margin-bottom: 10px;
    color: #e4b3ff;
    text-shadow:
        0 0 5px #a200ff,
        0 0 10px #a200ff,
        0 0 20px #ff00ff,
        0 0 40px #ff00ff,
        0 0 80px #ff00ff;
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from {
        text-shadow:
            0 0 8px #a200ff,
            0 0 16px #a200ff,
            0 0 32px #ff00ff;
    }
    to {
        text-shadow:
            0 0 14px #ff33ff,
            0 0 28px #ff33ff,
            0 0 56px #ff00ff;
    }
}
</style>

<h1 class="neon-title">NARRATIVENEXUS</h1>
""",
    unsafe_allow_html=True,
)


# ----------------- Upload Directory ----------------
UPLOAD_DIR = Path("uploaded_files")
UPLOAD_DIR.mkdir(exist_ok=True)


def save_uploaded_file(uploaded_file):
    dest = UPLOAD_DIR / uploaded_file.name
    with open(dest, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return str(dest.resolve())


def clear_current_session():
    for key in ["raw_docs", "cleaned_docs", "summary", "topics_data", "sentiments"]:
        st.session_state[key] = []
    st.session_state.summary = ""
    st.session_state.topics_data = None


# ----------------- UPLOAD PAGE ------------------
if page == "Upload":
    st.header("📂 Upload Documents or Paste Text")

    st.markdown(
        """
        <div class='glass-card'>
            <div class='card-title'>Upload Area</div>
            <div class='small-muted'>
                Upload PDF, DOCX, TXT, PPTX, CSV, Images (OCR), EPUB, RTF, HTML and more.
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    files = st.file_uploader(
        "Upload files:",
        type=[
            "txt",
            "pdf",
            "docx",
            "doc",
            "csv",
            "xlsx",
            "json",
            "html",
            "htm",
            "md",
            "rtf",
            "xml",
            "pptx",
            "epub",
            "jpg",
            "jpeg",
            "png",
            "bmp",
            "tiff",
        ],
        accept_multiple_files=True,
    )

    st.markdown("### ✏ Paste Text (Optional)")
    pasted_text = st.text_area(
        "Enter text (use --- to separate multiple docs)", height=200
    )
    topic_count = st.slider("Number of Topics (LDA)", 2, 10, 4)

    col1, col2 = st.columns([1, 1])

    # PROCESS BUTTON
    with col1:
        if st.button("Process"):
            docs = []
            saved_paths = []

            # Read uploaded files
            for f in files:
                try:
                    saved_path = save_uploaded_file(f)
                    saved_paths.append(saved_path)
                    docs.append(read_file(f))
                except Exception:
                    docs.append("")
                    saved_paths.append(None)

            # Read pasted text
            if pasted_text.strip():
                parts = [p.strip() for p in pasted_text.split("---") if p.strip()]
                docs.extend(parts)
                saved_paths.extend([None] * len(parts))

            if not docs:
                st.error("Please upload or paste at least one document.")
            else:
                final_docs = []

                st.info("Detecting languages & translating if needed...")
                for d in docs:
                    lang = detect_language(d)
                    if lang not in ["en", "unknown"]:
                        d = translate_to_english(d)
                    final_docs.append(d)

                # Save processing results
                st.session_state.raw_docs = final_docs
                st.session_state.cleaned_docs = [preprocess_text(d) for d in final_docs]
                st.session_state.summary = summarize(" ".join(final_docs))
                st.session_state.topics_data = extract_topics(
                    st.session_state.cleaned_docs, n_topics=topic_count
                )
                st.session_state.sentiments = [get_sentiment(d) for d in final_docs]

                pdf_bytes = generate_pdf(
                    st.session_state.summary,
                    st.session_state.topics_data["topics"],
                    st.session_state.sentiments,
                )

                # Store in history
                st.session_state.history.append(
                    {
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "documents": final_docs,
                        "cleaned": st.session_state.cleaned_docs,
                        "summary": st.session_state.summary,
                        "topics": st.session_state.topics_data["topics"],
                        "sentiments": st.session_state.sentiments,
                        "pdf": pdf_bytes,
                        "file_paths": saved_paths,
                    }
                )

                st.success(
                    "Processing complete! View results in Results (Tabs) or History."
                )

    # Reset Button
    with col2:
        if st.button("Reset Current Analysis"):
            clear_current_session()
            st.success("Current analysis cleared.")
            st.experimental_rerun()

# ---------------------------------------------------
# ------------------- RESULTS TAB -------------------
# ---------------------------------------------------
elif page == "Results (Tabs)":
    st.header("📊 Analysis Results")

    if not st.session_state.cleaned_docs:
        st.info("Upload and process files first.")
    else:
        tabs = st.tabs(
            [
                "Summary",
                "Sentiment",
                "Topics (pyLDAvis)",
                "Keywords",
                "Insights",
                "Visualizations",
                "Semantic Search",
                "Cosine Similarity",
                "Export",
            ]
        )

        # Summary
        with tabs[0]:
            st.markdown(
                "<div class='glass-card'><div class='card-title'>Executive Summary</div></div>",
                unsafe_allow_html=True,
            )
            st.write(st.session_state.summary)

            st.markdown(
                "<div class='glass-card'><div class='card-title'>Document Overviews</div></div>",
                unsafe_allow_html=True,
            )
            for i, d in enumerate(st.session_state.raw_docs):
                show_card(
                    f"Document {i + 1}", f"{len(d.split())} words", d[:500] + "..."
                )

        # Sentiment
        with tabs[1]:
            st.markdown(
                "<div class='glass-card'><div class='card-title'>Sentiment Distribution</div></div>",
                unsafe_allow_html=True,
            )
            df = pd.DataFrame(
                {
                    "Document": [
                        f"Doc {i + 1}" for i in range(len(st.session_state.sentiments))
                    ],
                    "Label": [s["label"] for s in st.session_state.sentiments],
                    "Score": [s["score"] for s in st.session_state.sentiments],
                }
            )
            st.dataframe(df)

            for i, s in enumerate(st.session_state.sentiments):
                show_card(f"Document {i + 1}", s["label"], f"Score: {s['score']:.3f}")

        # Topics
        with tabs[2]:
            st.markdown(
                "<div class='glass-card'><div class='card-title'>LDA Topics</div></div>",
                unsafe_allow_html=True,
            )
            topics = st.session_state.topics_data["topics"]
            for i, t in enumerate(topics):
                st.markdown(f"**Topic {i + 1}:** {', '.join(t)}")

            st.subheader("Interactive pyLDAvis Map")
            if st.button("Generate pyLDAvis Visualization"):
                html = generate_pyldavis(
                    st.session_state.topics_data["lda"],
                    st.session_state.topics_data["corpus"],
                    st.session_state.topics_data["dictionary"],
                )
                st.components.v1.html(html, height=800, scrolling=True)
                st.download_button("Download pyLDAvis", html, "lda_vis.html")

        # Keywords
        with tabs[3]:
            from collections import Counter

            words = " ".join(st.session_state.cleaned_docs).split()
            freq = Counter(words).most_common(20)
            st.table(pd.DataFrame(freq, columns=["Keyword", "Count"]))

        # Insights
        with tabs[4]:
            st.markdown(
                "<div class='glass-card'><div class='card-title'>Insights</div></div>",
                unsafe_allow_html=True,
            )
            neg = [
                i + 1
                for i, s in enumerate(st.session_state.sentiments)
                if s["label"].lower().startswith("neg")
            ]
            if neg:
                st.error(f"Negative sentiment detected in: {neg}")
            else:
                st.success("No negative sentiment detected.")

        # Visualizations
        with tabs[5]:
            st.subheader("Word Cloud")
            show_wordcloud(" ".join(st.session_state.cleaned_docs))

        # Semantic Search
        with tabs[6]:
            if st.button("Build Index"):
                build_index(st.session_state.raw_docs)
                st.success("Index ready.")
            q = st.text_area("Ask a question:")
            if st.button("Search"):
                results = query(q)
                for r in results:
                    show_card(f"{r['score']:.3f}", "Matched", r["doc"][:300] + "...")

        # Cosine Similarity
        with tabs[7]:
            df, highest = compute_cosine_similarity(st.session_state.cleaned_docs)
            plot_similarity_heatmap(df)
            st.success(
                f"Highest similarity: {highest['pair']} (Score: {highest['score']:.3f})"
            )

        # Export
        with tabs[8]:
            if st.button("Generate PDF Report"):
                pdf = generate_pdf(
                    st.session_state.summary,
                    st.session_state.topics_data["topics"],
                    st.session_state.sentiments,
                )
                st.download_button("Download Report", pdf, "NarrativeNexus_Report.pdf")

# ---------------------- HISTORY ------------------------
elif page == "History":
    st.header("🗂 Analysis History")

    if not st.session_state.history:
        st.info("No past analyses recorded.")
    else:
        for idx, rec in enumerate(reversed(st.session_state.history), 1):
            with st.expander(f"Analysis #{idx} — {rec['timestamp']}"):
                st.subheader("Summary")
                st.write(rec["summary"])

                st.subheader("Topics")
                for i, t in enumerate(rec["topics"]):
                    st.markdown(f"**Topic {i + 1}:** {', '.join(t)}")

                st.subheader("Sentiments")
                df = pd.DataFrame(
                    {
                        "Document": [
                            f"Doc {i + 1}" for i in range(len(rec["sentiments"]))
                        ],
                        "Label": [s["label"] for s in rec["sentiments"]],
                        "Score": [s["score"] for s in rec["sentiments"]],
                    }
                )
                st.dataframe(df)

                st.subheader("Files:")
                for p in rec["file_paths"]:
                    st.write(p or "Pasted Text")

                if rec["pdf"]:
                    st.download_button(
                        "Download PDF",
                        rec["pdf"],
                        f"Analysis_{rec['timestamp'].replace(' ', '_')}.pdf",
                    )

# ---------------------- DOWNLOAD PAGE ------------------------
elif page == "Download":
    st.header("Download Report")
    if st.session_state.cleaned_docs:
        pdf = generate_pdf(
            st.session_state.summary,
            st.session_state.topics_data["topics"],
            st.session_state.sentiments,
        )
        st.download_button("Download PDF", pdf, "NarrativeNexus_Report.pdf")
    else:
        st.info("No analysis to download.")
