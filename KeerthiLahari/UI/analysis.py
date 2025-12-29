import streamlit as st
import pandas as pd
import os
import plotly.express as px
from metrics import (
    word_count, sentence_count, sentiment_analysis, sentiment_distribution, 
    overall_sentiment, top_tokens
)
from summarise import generate_abstractive_summary

# Paths
FINAL_FOLDER = "Final_data"
PROCESSED_TEXT_FILE = os.path.join(FINAL_FOLDER, "processed_text.txt")
CSV_FILE = os.path.join(FINAL_FOLDER, "processed_csv.csv")
FINAL_SUMMARY_FOLDER = "KeerthiLahari/Final_summary"
os.makedirs(FINAL_SUMMARY_FOLDER, exist_ok=True)

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

    summary_text = ""
    metrics_text = ""

    # ---------- METRICS ----------
    if source_type == "text":
        # Generate summary
        model, summary = generate_abstractive_summary()
        if summary:
            summary_text = summary
            #st.write(summary_text)

            # Save summary
            summary_file_path = os.path.join(FINAL_SUMMARY_FOLDER, "summary.txt")
            with open(summary_file_path, "w", encoding="utf-8") as f:
                f.write(summary_text)

        # Compute metrics
        wc = word_count(text)
        sc = sentence_count(text)
        sentiment_scores = sentiment_analysis(text)
        sentiment = overall_sentiment(sentiment_scores["compound"])
        distribution = sentiment_distribution(sentiment_scores)
        tokens = top_tokens(text, n=8)

        # Build metrics text for report
        metrics_text += f"Word Count: {wc}\n"
        metrics_text += f"Sentence Count: {sc}\n"
        metrics_text += f"Top Tokens: {', '.join([t[0] for t in tokens])}\n"
        metrics_text += f"Overall Sentiment: {sentiment}\n"
        metrics_text += "Sentiment Distribution:\n"
        for k, v in distribution.items():
            metrics_text += f"  {k}: {v*100:.2f}%\n"

        # ---------------- Display Metrics ---------------- #
        st.markdown(f"""
            <div class="card">
                <h3>📝 Word Count</h3>
                <p>{wc}</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="card">
                <h3>📚 Sentence Count</h3>
                <p>{sc}</p>
            </div>
        """, unsafe_allow_html=True)

        token_html = ""
        colors = ["#FFD3B6", "#FFAAA5", "#A8E6CF", "#DCE8F2", "#B5EAD7", "#C7CEEA", "#F7D6E0", "#F9F7C9"]
        for i, (tok, cnt) in enumerate(tokens):
            color = colors[i % len(colors)]
            token_html += f"<span class='token-chip' style='background-color:{color};'>{tok} ({cnt})</span>"
        st.markdown(f"<div class='card'><h3>🔠 Top Tokens</h3>{token_html}</div>", unsafe_allow_html=True)

        st.markdown(f"""
            <div class="card">
                <h3>Overall Sentiment</h3>
                <p style="font-size:25px;">{sentiment}</p>
            </div>
        """, unsafe_allow_html=True)

        # Sentiment Distribution Chart
        percent_dist = {k: v * 100 for k, v in distribution.items()}
        df_chart = pd.DataFrame({
            "Sentiment": list(percent_dist.keys()),
            "Percentage": list(percent_dist.values())
        })
        st.markdown("<div class='card'><h3>📊 Sentiment Distribution (%)</h3></div>", unsafe_allow_html=True)
        fig = px.bar(
            df_chart,
            x="Sentiment",
            y="Percentage",
            color="Sentiment",
            text="Percentage",
            color_discrete_map={"Positive":"#2ecc71", "Neutral":"#95a5a6", "Negative":"#e74c3c"},
            height=300
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(showlegend=False, yaxis=dict(range=[0,100]), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    else:
        # CSV
        df = pd.read_csv(os.path.join(FINAL_FOLDER, "processed_csv.csv"))
        #st.dataframe(df.describe())
        summary_text = df.describe().to_string()

        # Save summary
        summary_file_path = os.path.join(FINAL_SUMMARY_FOLDER, "summary.txt")
        with open(summary_file_path, "w", encoding="utf-8") as f:
            f.write(summary_text)

    # ---------------- Download Report ---------------- #
    report_file = os.path.join(FINAL_SUMMARY_FOLDER, "metrics_report.txt")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("=== Summary ===\n")
        f.write(summary_text + "\n\n")
        if source_type == "text":
            f.write("=== Metrics ===\n")
            f.write(metrics_text)

    # Provide download button
    with open(report_file, "rb") as f:
        st.download_button(
            label="📥 Download Report",
            data=f,
            file_name="metrics_report.txt",
            mime="text/plain"
        )
