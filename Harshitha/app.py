import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import streamlit as st
import PyPDF2
import docx2txt
import pandas as pd
from analysis import analyze_text
from utils import generate_report
from preprocessing import clean_text
from wordcloud import WordCloud
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from collections import Counter
import numpy as np
from PIL import Image
import numpy as np

def show_wordcloud(text):
    if not text or not text.strip():
        st.warning("No text available for Word Cloud.")
        return

    wc = WordCloud(
        width=1200,
        height=800,
        background_color="white",
        max_words=60
    ).generate(text)

    img = Image.fromarray(wc.to_array())
    st.image(img, caption="Word Cloud", width=850)

st.set_page_config("NarrativeNexus", layout="wide")

st.markdown("""
<style>
body { background-color:#fff; }
div[data-baseweb="tab-list"] { justify-content: space-between; }
div[data-baseweb="tab-border"] { display:none; }
button[data-baseweb="tab"] {
    background:black !important;
    color:white !important;
    font-size:18px;
    padding:14px;
    width:100%;
    border-radius:14px;
    font-weight:600;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background:#222 !important;
}
.metric-card {
    background:#ff4b8b;
    color:white;
    padding:25px;
    border-radius:16px;
    text-align:center;
}
.metric-value {
    font-size:42px;
    font-weight:bold;
}
textarea {
    background:black !important;
    color:white !important;
    border-radius:12px !important;
}
div.stButton > button {
    background-color: #ff4b8b !important;
    color: white !important;
    font-weight: bold;
    font-size: 16px;
    padding: 10px 20px;
    border-radius: 12px;
}
div.stButton > button:hover {
    background-color: #ff1f70 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>NarrativeNexus</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;color:#ff4b8b'>The Dynamic AI Text Analysis Platform</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#000'>Sentiment • Topic Modeling • Summarization</p>", unsafe_allow_html=True)

if "analysis" not in st.session_state:
    st.session_state.analysis = None
    st.session_state.text = ""

tab1, tab2, tab3 = st.tabs(["Upload Files", "Paste Text", "Analyzed Text"])

with tab1:
    file = st.file_uploader("Upload TXT, PDF, DOCX, CSV", type=["txt", "pdf", "docx", "csv"])
    if file:
        text = ""
        try:
            if file.type == "application/pdf":
                reader = PyPDF2.PdfReader(file)
                text = " ".join(p.extract_text() for p in reader.pages if p.extract_text())
            elif file.type.endswith("csv"):
                text = " ".join(pd.read_csv(file, dtype=str).fillna("").astype(str).values.flatten())
            elif file.type.endswith("docx"):
                text = docx2txt.process(file)
            else:
                text = file.getvalue().decode("utf-8", errors="ignore")
        except Exception as e:
            st.error(e)

        if text and st.button("Analyze Text", key="upload"):
            with st.spinner("Analyzing text..."):
                st.session_state.analysis = analyze_text(text, text.lower())
                st.session_state.text = text
            st.success("Text analyzed successfully")

with tab2:
    text = st.text_area("Paste your text", height=200)
    if text and st.button("Analyze Text", key="paste"):
        with st.spinner("Analyzing text..."):
            st.session_state.analysis = analyze_text(text, text.lower())
            st.session_state.text = text
        st.success("Text analyzed successfully")

with tab3:
    if not st.session_state.analysis:
        st.info("Analyze text to view results")
    else:
        a = st.session_state.analysis
        avg_polarity = a.get("avg_polarity", 0.0)
        counts = a.get("sentiment_distribution", {})
        total = sum(counts.values())
        overall_label = a.get("overall_sentiment", "N/A")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                f"<div class='metric-card'><div style='font-size:18px;'>Word Count:</div>"
                f"<div class='metric-value'>{a.get('word_count',0)}</div></div>",
                unsafe_allow_html=True
            )
        with c2:
            st.markdown(
                f"<div class='metric-card'><div style='font-size:18px;'>Sentence Count:</div>"
                f"<div class='metric-value'>{a.get('sentence_count',0)}</div></div>",
                unsafe_allow_html=True
            )
        overall_label = a.get("overall_sentiment", "N/A")
        polarity_score = a.get("polarity_score", 0.0)

        with c3:
            st.markdown(
                f"""
                <div class='metric-card'>
                    <div style='font-size:18px;'>Overall Sentiment:</div>
                    <div class='metric-value'>{overall_label} ({polarity_score})</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.subheader("Sentence-level Sentiment Distribution:")

        def bar(label, value, color):
            pct = value / max(total, 1)
            st.markdown(
                f"""
                <div style='margin-bottom:6px'>
                    <b>{label}</b>
                    <div style='background:#ddd;height:6px;border-radius:10px;width:70%;'>
                        <div style='width:{pct*100}%;background:{color};
                             height:6px;border-radius:10px;'></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        bar("Positive", counts.get("Positive", 0), "#2ecc71")
        bar("Neutral", counts.get("Neutral", 0), "#f1c40f")
        bar("Negative", counts.get("Negative", 0), "#e74c3c")
        st.markdown(
            f"<div style='margin-top:10px;font-size:15px;'><b>Counts:</b> "
            f"Positive:{counts.get('Positive',0)} | "
            f"Neutral:{counts.get('Neutral',0)} | "
            f"Negative:{counts.get('Negative',0)}</div>",
            unsafe_allow_html=True
        )

        st.subheader("Top Keywords (Frequency Analysis):")

        words = clean_text(st.session_state.text).split()
        filtered_words = [
            w for w in words if w not in ENGLISH_STOP_WORDS and len(w) > 2
        ]

        if filtered_words:
            counter = Counter(filtered_words)
            top_words = counter.most_common(8)
            df_keywords = pd.DataFrame(top_words, columns=["Keyword", "Frequency"])

            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown(
                    "<div style='font-size:20px;font-weight:600;margin-bottom:6px;'>"
                    "Frequency Bar Chart:</div>",
                    unsafe_allow_html=True
                )
                fig, ax = plt.subplots(figsize=(5, 4))
                ax.bar(df_keywords["Keyword"], df_keywords["Frequency"], color="#ff69b4")
                ax.set_xlabel("Keywords")
                ax.set_ylabel("Frequency")
                ax.tick_params(axis="x", rotation=45)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)

            with col2:
                st.markdown(
                    "<div style='font-size:20px;font-weight:600;margin-bottom:6px;'>"
                    "Frequency Table:</div>",
                    unsafe_allow_html=True
                )
                st.table(df_keywords)
        else:
            st.info("No keywords available")

        st.subheader("Word Cloud:")
        show_wordcloud(" ".join(filtered_words[:100]))

        st.subheader("Topic Modeling:")

        lda_tab, nmf_tab = st.tabs(["LDA Topics", "NMF Topics"])

        with lda_tab:
            for t in a.get("topics", {}).get("lda", []):
                st.write("•", t)

        with nmf_tab:
            for t in a.get("topics", {}).get("nmf", []):
                st.write("•", t)

        st.subheader("Executive Summary")
        st.markdown(
                    f"<div style='max-height:300px; overflow-y:auto; padding:10px; border:1px solid #ddd; border-radius:12px; background:#f9f9f9'>{st.session_state.text}</div>",
                                 unsafe_allow_html=True)

        st.subheader("Actionable Insights:")
        for i in a.get("insights", []):
            st.write("•", i)

        report = generate_report(st.session_state.text, a)

        st.download_button(
            label="Download Report",
            data=report.encode("utf-8"),
            file_name="narrativenexus_report.txt"
        )