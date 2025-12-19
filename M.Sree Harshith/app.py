import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Import utility functions and models
from ui import page_bg 
from read_file import read_file 
from preprocessing import count_words, preprocess_text, clean_text 
from models import run_sentiment_analysis
from models import find_similar_content
from models import SONG_DATABASE
from summarize import extractive_summarize

from models import generate_word_cloud_html

# --- CONFIGURATION ---
st.set_page_config(page_title="Dynamic Text Analysis Platform", layout="wide")

# Apply background
st.markdown(page_bg, unsafe_allow_html=True) 

st.title("Dynamic Text Analysis Platform")

# --- TABS (Updated: Removed Similarity, variables are now sequential) ---
tab1, tab2, tab3, tab4 ,tab5, tab6= st.tabs([
    "Tokenization", 
    "Preprocessing", 
    "Summarization", 
    "Sentiment Analysis",
    "Cosine Similarity",
    "Visuilization and Report"
])

# ==============================================================================
# TAB 1: TEXT TOKENIZATION 
# ==============================================================================
with tab1:
    st.header("Smart Tokenization")
    user_text = st.text_area("Enter text to analyze:", height=150, key="tok_text", placeholder="Paste your article, report, or review here...")
    upload_file = st.file_uploader("Upload .txt, .pdf, or .csv for analysis:", 
                                   type=["txt", "pdf", "csv"], 
                                   key="tok_file")

    file_text, file_df = read_file(upload_file)

    combined_raw_text = (user_text or "") + "\n\n" + (file_text or "")
    
    if file_df is not None:
        st.subheader("CSV Preview")
        st.dataframe(file_df.head())
        csv_text = " ".join(
            file_df.astype(str)
            .fillna("")
            .apply(lambda row: " ".join(row.values.astype(str)), axis=1)
            .tolist()
        )
        combined_raw_text += ("\n\n" + csv_text)

    elif file_text:
        st.subheader("File Preview")
        st.write(file_text[:500] + "..." if len(file_text) > 500 else file_text)


    if st.button("Run Tokenization & Word Count"):
        if not combined_raw_text.strip():
            st.error("Please enter text or upload a file.")
        else:
            # --- 1. RAW WORD COUNT (The actual number of words in the input) ---
            raw_word_count = count_words(combined_raw_text) 
            
            # --- 2. CLEANING & TOKENIZING (For NLP analysis) ---
            cleaned_text = clean_text(combined_raw_text)
            tokens = cleaned_text.split()
            
            # --- DISPLAY RESULTS ---
            
            # A. Display the Raw Count first
            st.success(f"**Total Word Occurrences (Raw Input):** **{raw_word_count}**")
            
            st.write("---")

            st.write("### Cleaned Tokens ")
            st.write("The counts below reflect words retained for NLP models.")
            st.code(tokens[:50])
            
            # B. Display the Cleaned Counts (Tokens)
            st.success(f"**Total Unique Tokens (After Cleaning):** **{len(set(tokens))}**")
            st.success(f"**Total Token Occurrences (After Cleaning):** **{len(tokens)}**")


# ==============================================================================
# TAB 2: PREPROCESSING (This was previously tab3, now tab2)
# ==============================================================================
with tab2:
    st.header("Data Pre-processing Pipeline")
    
    preview_file = st.file_uploader("Upload .txt, .pdf, or .csv to Pre-process:", 
                                    type=["txt", "pdf", "csv"], 
                                    key="prev_file")

    if preview_file is not None:
        
        try:
            text_raw, df_raw = read_file(preview_file)
            
            st.subheader("Before Preprocessing")
            
            current_file_type = None
            
            if df_raw is not None:
                st.dataframe(df_raw.head())
                current_file_type = "csv"
            elif text_raw:
                st.write(text_raw[:1500] + "..." if len(text_raw) > 1500 else text_raw)
                current_file_type = "txt" if "txt" in preview_file.name.lower() else "pdf" 
            else:
                st.error("Could not read file content.")
                st.stop()
                
            st.write("---")
            st.subheader("After Preprocessing")

            if current_file_type in ["txt", "pdf"]:
                cleaned_output, error = preprocess_text(text=text_raw, file_type=current_file_type)

                if error:
                    st.error(error)
                else:
                    st.write(cleaned_output[:2000] + "...")
                    st.success("Text preprocessing completed and saved in Final_data/processed_text.txt")

            elif current_file_type == "csv":
                cleaned_output, error = preprocess_text(df=df_raw, file_type="csv")

                if error:
                    st.error(error)
                else:
                    st.dataframe(cleaned_output.head())
                    
                    # --- UPDATED CLARIFICATION ---
                    if isinstance(cleaned_output, pd.DataFrame):
                        # Find object columns that are NOT excluded to show what was cleaned
                        cols_to_exclude = ['date', 'time', 'ticker', 'id', 'name']
                        cleaned_cols = [col for col in cleaned_output.select_dtypes(include=["object"]).columns if col.lower() not in cols_to_exclude]
                        
                        if cleaned_cols:
                            st.success(f" CSV preprocessing completed. Unstructured text columns cleaned: **{', '.join(cleaned_cols)}**. Numerical/Structured columns preserved. Saved in Final_data/processed_csv.csv")
                        else:
                            st.success(" CSV loaded. No unstructured text columns were found for cleaning (Numerical/Date/Ticker columns preserved). Saved in Final_data/processed_csv.csv")
                    # --- END UPDATED CLARIFICATION ---

            
        except Exception as e:
            st.error(f"An unexpected error occurred in the Preprocessing tab: {e}")

# ==============================================================================
# TAB 3: SUMMARIZATION (This was previously tab4, now tab3)
# ==============================================================================
with tab3:
    st.header(" Extractive Summarization")
    st.write("Generate a concise summary of the input text.")
    
    summarize_text = st.text_area("Enter text to summarize:", height=200, key="sum_text")
    summarize_upload = st.file_uploader("Upload .txt, .pdf, or .csv file to summarize:", 
                                         type=["txt", "pdf", "csv"], 
                                         key="sum_file")
    
    # Text length check is crucial for summarization quality
    min_length = st.slider("Minimum length (sentences) of the summary:", min_value=1, max_value=10, value=3, step=1)
    
    if st.button("Generate Summary"):
        # Combine inputs
        file_text, file_df = read_file(summarize_upload)
        
        if file_df is not None:
            # For CSV, combine all text fields into one document for summarization
            combined_raw_text = summarize_text + " " + " ".join(file_df.astype(str).stack().tolist())
        else:
            combined_raw_text = summarize_text + " " + (file_text or "")
        
        if not combined_raw_text.strip():
            st.error("Please enter text or upload a file containing content to summarize.")
        elif count_words(combined_raw_text) < 50 and min_length > 1:
            st.warning("Input text is very short. A multi-sentence summary may not be meaningful.")
            st.write(combined_raw_text)
        else:
            with st.spinner("Generating summary..."):
                summary = extractive_summarize(combined_raw_text, min_length)
                
                st.write("---")
                st.subheader("Generated Summary")
                st.markdown(summary)
                st.success(f"Summary generated using the top {min_length} sentences.")

# ==============================================================================
# TAB 4: SENTIMENT ANALYSIS (This was previously tab5, now tab4)
# ==============================================================================
with tab4:
    st.header(" Sentiment Analysis")
    st.write("Analyze the overall emotional tone of your text.")
    
    sentiment_text = st.text_area("Enter text for sentiment analysis:", height=150, key="sentiment_text")
    sentiment_upload = st.file_uploader("Upload file (.txt, .csv) for batch sentiment analysis:", 
                                         type=["txt", "csv"], 
                                         key="sentiment_file")
    
    if st.button("Analyze Sentiment"):
        input_data = []
        if sentiment_text:
            input_data.append(sentiment_text)
        
        if sentiment_upload:
            file_text, file_df = read_file(sentiment_upload)
            if file_df is not None:
                input_data.extend(file_df.astype(str).stack().tolist())
            elif file_text:
                input_data.extend(file_text.split('\n'))

        if not input_data:
            st.error("Please enter text or upload a file.")
        else:
            input_data = [d.strip() for d in input_data if d.strip()]
            
            with st.spinner("Calculating Sentiment..."):
                results_df = run_sentiment_analysis(input_data)
                
                if results_df is not None and not results_df.empty:
                    
                    total_sentiment = results_df['compound'].mean()

                    st.write("---")
                    st.subheader("Overall Sentiment Summary")
                    
                    sentiment_label = "Neutral"
                    color_style = "color: black; font-weight: bold;" 

                    if total_sentiment >= 0.05:
                        sentiment_label = "Positive"
                        color_style = "color: green; font-weight: bold;" 
                    elif total_sentiment <= -0.05:
                        sentiment_label = "Negative"
                        color_style = "color: red; font-weight: bold;" 
                        
                    st.markdown(f"**Overall Sentiment:** <span style='{color_style}'>{sentiment_label}</span>", unsafe_allow_html=True)
                    st.markdown(f"**Average Compound Score:** `{total_sentiment:.3f}`")
                    
                    st.write("---")
                    st.subheader("Detailed Analysis")
                    st.dataframe(results_df) 
                else:
                    st.warning("No valid text found for sentiment analysis.")



with tab5:
    st.header("🎧 Semantic Content Recommender")
    st.write("Find songs based on similarity between your description and song metadata.")

    user_query = st.text_area(
        "Describe the content you want:",
        height=100,
        key="sim_query",
        placeholder="Example: soft calm emotional song..."
    )

    top_n = st.slider(
        "Number of recommendations:",
        min_value=1,
        max_value=len(SONG_DATABASE),
        value=3
    )

    if st.button("Find Similar Content", type="primary"):
        if not user_query.strip():
            st.warning("Please enter a description.")
            st.stop()

        with st.spinner("Calculating similarity..."):
            recommendations = find_similar_content(user_query, top_n)

        st.subheader(f"Top {top_n} Results for: _{user_query}_")
        st.write("")

        for rank, (title, score) in enumerate(recommendations, start=1):
            st.markdown(f"### {rank}. {title}")
            score_percent = score * 100
            if score_percent < 10:
                bar_html = f"""
                <div class="sim-bar-container">
                    <div class="sim-bar-fill" style="width:{score_percent:.0f}%;"></div>
                </div>
                <div style="margin-top:-12px; font-size:14px; font-weight:bold; color:black;">
                    {score:.4f}
                </div>
                """
            st.write(f"**Description:** {SONG_DATABASE[title]}")
            st.write("---")
#visuilization
with tab6:
    # --- Custom Styling for the Unified Composer ---
    st.markdown("""
<style>
/* Container styling */
.composer-wrapper {
    border: 1px solid #e5e7eb;          /* light grey border */
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 20px;
    background-color: #ffffff;          /* PURE WHITE */
}

/* Text area styling */
.stTextArea textarea {
    border: none !important;
    border-radius: 0 !important;
    padding: 15px !important;
    background-color: #ffffff !important;
    color: #111827 !important;           /* dark text for visibility */
    font-size: 15px;
}

/* File uploader styling */
[data-testid="stFileUploaderDropzone"] {
    border: none !important;
    border-top: 1px solid #e5e7eb !important;
    border-radius: 0 !important;
    padding: 0.6rem 1rem !important;
    background-color: #ffffff !important;
    color: #111827 !important;
}

/* File uploader text */
[data-testid="stFileUploaderDropzone"] span {
    color: #111827 !important;
    font-weight: 500;
}

/* Footer / helper text */
.composer-footer {
    display: flex;
    justify-content: space-between;
    padding: 6px 12px;
    background: #ffffff;                /* white footer */
    color: #6b7280;                     /* light grey text */
    font-size: 0.8rem;
}
</style>
""", unsafe_allow_html=True)


    st.header("📊 Data Import & Reporting Hub")
    st.write("Merge file uploads and manual text into a single intelligent analysis report.")

    # --- 1. THE UNIFIED COMPOSER ---
    source_text = ""
    data_source_name = "Manual Input"

    with st.container():
        # Text Input (Primary)
        manual_text = st.text_area(
            "Input Content", 
            placeholder="Type, paste content, or drop a file below...", 
            height=150, 
            label_visibility="collapsed"
        )
        
        # File Attachment (Integrated)
        uploaded_file = st.file_uploader(
            "Attach Documents", 
            type=["pdf", "csv"], 
            label_visibility="collapsed"
        )
        
        st.markdown('<div class="composer-footer"><span>Supported: PDF, CSV</span><span>Limit: 200MB</span></div>', unsafe_allow_html=True)

    # --- 2. DATA PROCESSING LOGIC ---
    # Priority 1: Handle File Upload
    if uploaded_file is not None:
        data_source_name = uploaded_file.name
        if uploaded_file.type == "application/pdf":
            try:
                import pypdf
                reader = pypdf.PdfReader(uploaded_file)
                source_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
                st.toast(f"Extracted {len(reader.pages)} pages from {uploaded_file.name}", icon="📄")
            except Exception as e:
                st.error(f"Error reading PDF: {e}")
        
        elif uploaded_file.type == "text/csv":
            try:
                df_upload = pd.read_csv(uploaded_file)
                target_col = st.selectbox("Select column to analyze:", df_upload.columns)
                source_text = " ".join(df_upload[target_col].dropna().astype(str).tolist())
                st.toast(f"Loaded {len(df_upload)} rows from CSV", icon="📈")
            except Exception as e:
                st.error(f"Error reading CSV: {e}")
    
    # Priority 2: Handle Manual Text
    if not source_text and manual_text.strip():
        source_text = manual_text
        data_source_name = "Typed Text Entry"

    # --- 3. ANALYSIS & VISUALIZATION ---
    if source_text.strip():
        st.divider()
        
        # Execution with Status Container
        with st.status("Generating Intelligence Report...", expanded=True) as status:
            from nltk.sentiment.vader import SentimentIntensityAnalyzer
            
            st.write("Crunching sentiment vectors...")
            sia = SentimentIntensityAnalyzer()
            sentiment_score = sia.polarity_scores(source_text)
            
            st.write("Processing linguistic tokens...")
            # Note: preprocess_text must be defined in your main script
            clean_tokens, _ = preprocess_text(source_text) 
            
            # Dashboard Layout
            st.write("Rendering visualizations...")
            v_col1, v_col2 = st.columns([3, 2])
            
            with v_col1:
                st.subheader("Word Frequency Analysis")
                if clean_tokens:
                    # Note: generate_word_cloud_html must be defined in your main script
                    word_cloud_html = generate_word_cloud_html(clean_tokens)
                    st.markdown(word_cloud_html, unsafe_allow_html=True)
                else:
                    st.info("Insufficient data for word cloud.")

            with v_col2:
                st.subheader("Sentiment Metrics")
                comp = sentiment_score['compound']
                mood = "Positive" if comp >= 0.05 else "Negative" if comp <= -0.05 else "Neutral"
                
                st.metric("Content Mood", mood, delta=f"{comp:.2f} Score")
                chart_data = pd.DataFrame({
                    'Metric': ['Positive', 'Neutral', 'Negative'],
                    'Score': [sentiment_score['pos'], sentiment_score['neu'], sentiment_score['neg']]
                })
                st.bar_chart(chart_data.set_index('Metric'))
            
            status.update(label="Analysis Complete!", state="complete", expanded=False)

        # --- 4. REPORTING & EXPORTS ---
        st.subheader("📑 Analysis Report")
        
        report_content = f"""TEXT ANALYSIS SUMMARY
--------------------------------------------------
SOURCE: {data_source_name}
DATE: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}

DATA PROFILE:
- Character Count: {len(source_text):,}
- Estimated Word Count: {len(source_text.split()):,}

SENTIMENT BREAKDOWN:
- Positive Weight: {sentiment_score['pos']:.2%}
- Neutral Weight:  {sentiment_score['neu']:.2%}
- Negative Weight: {sentiment_score['neg']:.2%}
- Compound Score:  {sentiment_score['compound']:.4f}

OVERALL FINDING:
The analyzed content presents a predominantly {mood.lower()} sentiment.
--------------------------------------------------
Generated by Integrated Analytics Module.
"""
        st.text_area("Report Preview", value=report_content, height=200)
        
        # Download buttons
        dl1, dl2 = st.columns(2)
        with dl1:
            st.download_button(
                "📥 Download TXT Report",
                data=report_content,
                file_name=f"report_{data_source_name.split('.')[0]}.txt",
                mime="text/plain",
                use_container_width=True
            )
        with dl2:
            csv_metrics = pd.DataFrame([sentiment_score]).to_csv(index=False).encode('utf-8')
            st.download_button(
                "📊 Export Data (CSV)",
                data=csv_metrics,
                file_name=f"metrics_{data_source_name.split('.')[0]}.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.info("Awaiting input: Upload a PDF/CSV or paste text into the composer above.")