import streamlit as st
from streamlit_option_menu import option_menu
from data_extractor import extract_text_from_file
from data_preprocessing import preprocess_text
from metrics import (
        load_processed_text,
        word_count,
        sentence_count,
        sentiment_analysis,
        sentiment_distribution,
        sentiment_to_emoji,
        top_tokens,
        simple_summary
    )


# ---------- GLOBAL CSS FIXES need to be worked in future------------
st.markdown("""
<style>
.block-container {
    padding-top: 1rem !important;
}

.center-text {
    text-align: center;
}

.spacing {
    margin-top: -20px;
}
</style>
""", unsafe_allow_html=True)

# -----------settings----------------
title = "Narrative Nexus"
caption = "Dynamic Text Analysis Platform"
subheader = " summarise . Analyze . Get Insights "
icon = "🧠"
layout = "centered"

# -------------Heading part-------------------------
st.set_page_config(page_title=title, page_icon=icon, layout=layout)
st.markdown(f"<h1 class='center-text'>{title} {icon}</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 class='center-text spacing'>{caption}</h3>", unsafe_allow_html=True)
st.markdown(f"<p class='center-text spacing'>{subheader}</p>", unsafe_allow_html=True)

# ----------- Navigation Menu --------------
selected = option_menu(
            menu_title=None,
            options=["About", "Text Input", "Text Analysis"],
            icons=["house", "upload", "bar-chart"],
            default_index=1,
            orientation="horizontal",
)
# -------------About Section-----------------
if selected == "About":
    st.subheader("About Narrative Nexus")
    entered_text = """
    <div style="text-align: Justify;font:arial; font-size:20px;">
    Narrative Nexus is a dynamic text analysis platform designed to help users quickly summarize content,
    measure word and character counts, evaluate sentiment, and generate meaningful insights from any text.
    The application supports text uploads and manual input, processes data efficiently, and delivers clearly
    structured results that can be downloaded for further use. With features ranging from automated summarization
    to sentiment distribution visualization, Narrative Nexus provides a simple yet powerful tool for students,
    researchers, professionals, and anyone looking to understand and refine their written content with ease.
    </div>
    """
    st.markdown(entered_text, unsafe_allow_html=True)

# -------------Text Input Section----------------
elif selected == "Text Input":

    st.subheader("Upload a file OR paste text")

    uploaded_file = st.file_uploader("Upload TXT / CSV / PDF", type=["txt", "csv", "pdf"])
    pasted_text = st.text_area("Or paste text here...", height=200)

    if st.button("Process Text"):
        raw_text, file_type, df_data, error = extract_text_from_file(
            uploaded_file=uploaded_file,
            pasted_text=pasted_text
        )

        if error:
            st.error(error)

        else:
            st.success(f"Extracted ({file_type.upper()}) successfully!")
            
            if file_type in ["txt", "pdf"]:
                processed, err = preprocess_text(raw_text, file_type)
                if err:
                    st.error(err)
                else:
                    st.success("Preprocessing complete!")
                    st.write(processed[:2000])

            elif file_type == "csv":
                processed_df, err = preprocess_text(
                    text=None,
                    file_type="csv",
                    df=df_data
                )
                if err:
                    st.error(err)
                else:
                    st.success("CSV preprocessing complete!")
                    st.dataframe(processed_df.head())

            st.info(" Move to the 'Text Analysis' tab for insights.")

# ---------------- TEXT ANALYSIS Section------------------
elif selected == "Text Analysis":
    st.subheader("📊 Text Analysis Dashboard")
    text, source_type = load_processed_text()

    if text is None:
        st.warning("⚠ No processed text found. Please upload or paste text in the 'Text Input' section.")
    else:
        st.success(f"✔ Loaded processed {source_type.upper()} data")

        # ---------- METRICS ----------
        wc = word_count(text)
        sc = sentence_count(text)
        sentiment_scores = sentiment_analysis(text)
        sentiment = sentiment_to_emoji(sentiment_scores["compound"])
        print(sentiment)
        distribution = sentiment_distribution(sentiment_scores)
        tokens = top_tokens(text, n=8)
        summary = simple_summary(text)

        # ---------- CARD STYLE ----------
        st.markdown("""
        <style>
        .card {
            background-color: #f5f7ff;
            padding: 18px;
            border-radius: 12px;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 15px;
        }
        .card h3 {
            font-size: 22px;
            margin: 0;
            color: #333;
        }
        .card p {
            font-size: 18px;
            margin: 5px;
            color: #444;
        }
        .token-box {
            background-color: #eef1ff;
            border: 1px solid #cfd2ff;
            padding: 6px 10px;
            border-radius: 10px;
            margin: 4px;
            display: inline-block;
            font-size: 14px;
        }
        </style>
        """, unsafe_allow_html=True)

        # ---------------- ROW 1 – Word Count ---------------- #
        st.markdown(f"""
        <div class="card">
            <h3>📝 Word Count</h3>
            <p>{wc}</p>
        </div>
        """, unsafe_allow_html=True)

        # ---------------- ROW 2 – Sentence Count ---------------- #
        st.markdown(f"""
        <div class="card">
            <h3>📚 Sentence Count</h3>
            <p>{sc}</p>
        </div>
        """, unsafe_allow_html=True)

       # ---------------- ROW 3 – Top Tokens ---------------- #
        st.markdown("""
        <style>
        .token-chip {
            padding: 6px 12px;
            border-radius: 15px;
            margin: 4px;
            display: inline-block;
            font-size: 14px;
            font-weight: 500;
            color: #222;
        }
        </style>
        """, unsafe_allow_html=True)

        # beautiful pastel color palette
        colors = [
            "#FFD3B6", "#FFAAA5", "#A8E6CF",
            "#DCE8F2", "#B5EAD7", "#C7CEEA",
            "#F7D6E0", "#F9F7C9"
        ]

        st.markdown("<div class='card' style='text-align:left;'>"
                    "<h3>🔠 Top Tokens</h3>", unsafe_allow_html=True)

        token_html = ""
        for i, (tok, cnt) in enumerate(tokens):
            color = colors[i % len(colors)]
            token_html += f"""
                <span class="token-chip" style="background-color:{color};">
                    {tok} ({cnt})
                </span>
            """

        st.markdown(token_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


        # ---------- ROW 4 – Sentiment Emoji ---------------- #
        st.markdown(f"""
        <div class="card" style="text-align:left;">
            <h3>Overall Sentiment</h3>
            <p style="font-size:25px; margin-top:10px;">{sentiment}</p>
        </div>
        """, unsafe_allow_html=True)

        # ---------- ROW 5 – Sentiment Distribution Line Chart ----- #
        import pandas as pd

        percent_dist = {
            "Positive": distribution["Positive"] * 100,
            "Neutral": distribution["Neutral"] * 100,
            "Negative": distribution["Negative"] * 100
        }

        df_chart = pd.DataFrame({
            "Sentiment": list(percent_dist.keys()),
            "Percentage": list(percent_dist.values())
        })

        st.markdown("""
        <div class="card">
            <h3>📊 Sentiment Distribution (%)</h3>
        </div>
        """, unsafe_allow_html=True)

        st.bar_chart(df_chart, x="Sentiment", y="Percentage", height=200)
        

