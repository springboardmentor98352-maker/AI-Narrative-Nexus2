import streamlit as st
import pandas as pd
import os
from metrics import (
    word_count, sentence_count, sentiment_analysis,
    sentiment_distribution, sentiment_to_emoji,
    top_tokens, simple_summary
)

# Paths
FINAL_FOLDER = "Final_data"
PROCESSED_TEXT_FILE = os.path.join(FINAL_FOLDER, "processed_text.txt")
CSV_FILE = os.path.join(FINAL_FOLDER, "processed_csv.csv")

def render_analysis():
    st.subheader("📊 Text Analysis Dashboard")

    # Load processed text or CSV
    if os.path.exists(PROCESSED_TEXT_FILE):
        with open(PROCESSED_TEXT_FILE, "r", encoding="utf-8") as f:
            text = f.read()
        source_type = "text"
    elif os.path.exists(CSV_FILE):
        text = pd.read_csv(CSV_FILE)
        source_type = "csv"
    else:
        st.warning("⚠ No processed data found. Please upload or paste text in the 'Text Input' section.")
        return

    st.success(f"✔ Loaded processed {source_type.upper()} data")

    # ---------- METRICS ----------
    if source_type == "text":
        wc = word_count(text)
        sc = sentence_count(text)
        sentiment_scores = sentiment_analysis(text)
        sentiment = sentiment_to_emoji(sentiment_scores["compound"])
        distribution = sentiment_distribution(sentiment_scores)
        tokens = top_tokens(text, n=8)
        summary = simple_summary(text)

        # ---------------- Word Count ---------------- #
        st.markdown(f"""
            <div class="card">
                <h3>📝 Word Count</h3>
                <p>{wc}</p>
            </div>
        """, unsafe_allow_html=True)

        # ---------------- Sentence Count ---------------- #
        st.markdown(f"""
            <div class="card">
                <h3>📚 Sentence Count</h3>
                <p>{sc}</p>
            </div>
        """, unsafe_allow_html=True)

        # ---------------- Top Tokens ---------------- #
        token_html = ""
        colors = ["#FFD3B6", "#FFAAA5", "#A8E6CF", "#DCE8F2", "#B5EAD7", "#C7CEEA", "#F7D6E0", "#F9F7C9"]
        for i, (tok, cnt) in enumerate(tokens):
            color = colors[i % len(colors)]
            token_html += f"<span class='token-chip' style='background-color:{color};'>{tok} ({cnt})</span>"

        st.markdown(f"<div class='card'><h3>🔠 Top Tokens</h3>{token_html}</div>", unsafe_allow_html=True)

        # ---------------- Sentiment ---------------- #
        st.markdown(f"""
            <div class="card">
                <h3>Overall Sentiment</h3>
                <p style="font-size:25px;">{sentiment}</p>
            </div>
        """, unsafe_allow_html=True)

        # ---------------- Sentiment Distribution ---------------- #
        percent_dist = {k: v * 100 for k, v in distribution.items()}
        df_chart = pd.DataFrame({
            "Sentiment": list(percent_dist.keys()),
            "Percentage": list(percent_dist.values())
        })
        st.markdown("<div class='card'><h3>📊 Sentiment Distribution (%)</h3></div>", unsafe_allow_html=True)
        st.bar_chart(df_chart, x="Sentiment", y="Percentage", height=200)

        # ---------------- Summary ---------------- #
        st.markdown(f"""
            <div class="card">
                <h3>📝 Summary</h3>
                <p>{summary}</p>
            </div>
        """, unsafe_allow_html=True)

    else:
        # If CSV, just show head of the dataframe
        st.markdown("<div class='card'><h3>📄 CSV Data Preview</h3></div>", unsafe_allow_html=True)
        st.dataframe(text.head())
