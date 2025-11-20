import streamlit as st
import pandas as pd
from pathlib import Path
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

st.markdown(
    """
    <h1 style='text-align:center; 
               color:white; 
               font-size:48px; 
               font-weight:700; 
               letter-spacing:3px;
               margin-top:-10px;'>
        NARRATIVENEXUS
    </h1>
    """,
    unsafe_allow_html=True,
)

css_path = Path("assets/custom.css")
if css_path.exists():
    with open(css_path, "r") as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)
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
        </style>
        """,
        unsafe_allow_html=True,
    )

st.sidebar.title("NarrativeNexus")
page = st.sidebar.radio(
    "Navigate",
    ["Upload", "Results (Tabs)", "Cosine Similarity", "Semantic Search", "Download"],
)

if "raw_docs" not in st.session_state:
    st.session_state.raw_docs = []
    st.session_state.cleaned_docs = []
    st.session_state.summary = ""
    st.session_state.topics_data = None
    st.session_state.sentiments = []

if page == "Upload":
    st.header("📂 Upload Documents or Paste Text")
    st.markdown(
        """
    <div class='glass-card'>
        <div class='card-title'>Upload Area</div>
        <div class='small-muted'>Upload PDF, DOCX, PPTX, TXT, CSV, Images (OCR), EPUB, RTF, HTML and more</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    files = st.file_uploader(
        "Supported formats:",
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

    st.markdown("### ✏ Paste Text (optional)")
    pasted_text = st.text_area(
        "Enter text here (use `---` to separate multiple documents)", height=200
    )
    topic_count = st.slider("Number of Topics (LDA)", 2, 10, 4)

    if st.button("Process"):
        docs = []
        for f in files:
            docs.append(read_file(f))

        if pasted_text.strip():
            parts = [p.strip() for p in pasted_text.split("---") if p.strip()]
            docs.extend(parts)

        if not docs:
            st.error("Please upload or paste at least one document.")
        else:
            final_docs = []
            st.info("Detecting language & translating (if needed)...")
            for i, d in enumerate(docs):
                lang = detect_language(d)
                if lang not in ["en", "unknown"]:
                    st.warning(f"Document {i + 1} is in `{lang}` — translating...")
                    d = translate_to_english(d)
                final_docs.append(d)

            st.session_state.raw_docs = final_docs
            st.session_state.cleaned_docs = [preprocess_text(d) for d in final_docs]
            st.session_state.summary = summarize(" ".join(final_docs))

            st.session_state.topics_data = extract_topics(
                st.session_state.cleaned_docs, n_topics=topic_count
            )

            st.session_state.sentiments = [get_sentiment(d) for d in final_docs]
            st.success("Processing complete. Go to Results (Tabs).")

elif page == "Results (Tabs)":
    st.header("📊 Analysis Results — Tab View")

    if not st.session_state.cleaned_docs:
        st.info("Please upload and process documents first.")
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
                    f"Document {i + 1}",
                    f"{len(d.split())} words",
                    d[:500] + ("..." if len(d) > 500 else ""),
                )

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

        with tabs[2]:
            st.markdown(
                "<div class='glass-card'><div class='card-title'>LDA Topics</div></div>",
                unsafe_allow_html=True,
            )

            topics_info = st.session_state.topics_data
            topics_list = topics_info["topics"]

            for i, t in enumerate(topics_list):
                st.markdown(f"**Topic {i + 1}:** {', '.join(t)}")

            st.markdown("---")
            st.subheader("📌 Interactive Topic Visualization (pyLDAvis)")

            if st.button("Generate pyLDAvis Visualization"):
                with st.spinner("Preparing visualization..."):
                    html = generate_pyldavis(
                        topics_info["lda"],
                        topics_info["corpus"],
                        topics_info["dictionary"],
                    )
                    with open("lda_visualization.html", "w", encoding="utf-8") as f:
                        f.write(html)

                    st.success("Visualization ready!")
                    st.components.v1.html(html, height=800, scrolling=True)

                    st.download_button(
                        "Download LDA Visualization (HTML)",
                        html.encode("utf-8"),
                        "lda_visualization.html",
                        mime="text/html",
                    )

        with tabs[3]:
            from collections import Counter

            st.markdown(
                "<div class='glass-card'><div class='card-title'>Top Keywords</div></div>",
                unsafe_allow_html=True,
            )
            tok = " ".join(st.session_state.cleaned_docs).split()
            freq = Counter(tok).most_common(20)
            st.table(pd.DataFrame(freq, columns=["Keyword", "Count"]))

        with tabs[4]:
            st.markdown(
                "<div class='glass-card'><div class='card-title'>Actionable Insights</div></div>",
                unsafe_allow_html=True,
            )
            st.write("AI-generated insights based on sentiment + topics:")
            negative_docs = [
                i + 1
                for i, s in enumerate(st.session_state.sentiments)
                if s["label"].lower().startswith("neg")
            ]
            if negative_docs:
                st.error(f"Negative sentiment detected in documents: {negative_docs}")
            else:
                st.success("No negative sentiment detected.")

            st.markdown("### Recommendations")
            st.write("- Focus on documents with extreme sentiment values.")
            st.write("- Explore key topics using the pyLDAvis map.")
            st.write("- Review frequently repeated keywords for context.")

        with tabs[5]:
            st.markdown(
                "<div class='glass-card'><div class='card-title'>Visualizations</div></div>",
                unsafe_allow_html=True,
            )
            st.subheader("Word Cloud (All Docs)")
            show_wordcloud(" ".join(st.session_state.cleaned_docs))

        with tabs[6]:
            st.subheader("Semantic Search")
            if st.button("Build Index"):
                build_index(st.session_state.raw_docs)
                st.success("Index built.")

            q = st.text_area("Ask a question or search topic")
            k = st.slider("Top K Results", 1, 10, 3)

            if st.button("Search"):
                results = query(q, top_k=k)
                for r in results:
                    show_card(
                        f"Similarity: {r['score']:.3f}",
                        "Matched Text",
                        r["doc"][:400] + "...",
                    )

        with tabs[7]:
            st.subheader("Cosine Similarity Matrix")
            df, highest = compute_cosine_similarity(st.session_state.cleaned_docs)
            plot_similarity_heatmap(df)
            st.success(
                f"Highest similarity: {highest['pair'][0]} & {highest['pair'][1]} (Score: {highest['score']:.3f})"
            )

        with tabs[8]:
            st.subheader("Export Analysis Results")

            if st.button("Generate PDF"):
                pdf_bytes = generate_pdf(
                    st.session_state.summary,
                    st.session_state.topics_data["topics"],
                    st.session_state.sentiments,
                )
                st.download_button(
                    "Download Report PDF", pdf_bytes, "NarrativeNexus_Report.pdf"
                )

            df_export = pd.DataFrame(
                {
                    "Document": st.session_state.raw_docs,
                    "Cleaned": st.session_state.cleaned_docs,
                    "Sentiment": [s["label"] for s in st.session_state.sentiments],
                }
            )
            st.download_button(
                "Download CSV", df_export.to_csv(index=False), "results.csv"
            )

elif page == "Cosine Similarity":
    st.header("Cosine Similarity")
    if st.session_state.cleaned_docs:
        df, highest = compute_cosine_similarity(st.session_state.cleaned_docs)
        plot_similarity_heatmap(df)
    else:
        st.info("Upload files first.")

elif page == "Semantic Search":
    st.header("Semantic Search")
    if not st.session_state.raw_docs:
        st.info("Upload files first.")
    else:
        if st.button("Build Index"):
            build_index(st.session_state.raw_docs)
            st.success("Ready.")

        q = st.text_area("Query")
        if st.button("Search"):
            results = query(q)
            for r in results:
                show_card(f"{r['score']:.3f}", "Matched", r["doc"][:300] + "...")

elif page == "Download":
    st.header("Download Options")
    if st.session_state.cleaned_docs:
        pdf = generate_pdf(
            st.session_state.summary,
            st.session_state.topics_data["topics"],
            st.session_state.sentiments,
        )

        st.download_button("Download PDF", pdf, "NarrativeNexus_Report.pdf")
