import streamlit as st
from utils.file_reader import read_file
from utils.text_processor import process_text, get_stats
from utils.summarizer import SmartSummarizer
from utils.sentiment_analyzer import SentimentAnalyzer

# Load CSS
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.set_page_config(
    page_title="NarrativeNexus",
    page_icon="📊",
    layout="wide",
)

def main():
    # Header
    st.markdown("<h1>📊 NarrativeNexus</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Advanced Text Analysis & Processing Platform</p>", unsafe_allow_html=True)

    # File upload section
    st.markdown("<div class='content-section'>", unsafe_allow_html=True)
    st.markdown("### 📤 Upload Your File")
    
    uploaded_file = st.file_uploader(
        "Choose a file for analysis",
        type=['txt', 'csv', 'docx', 'pdf', 'json', 'xml', 'html'],
        help="Upload any text-based file"
    )

    if uploaded_file:
        file_details = f"""
        **File Details:**
        - Name: {uploaded_file.name}
        - Size: {uploaded_file.size:,} bytes
        - Type: {uploaded_file.type if uploaded_file.type else 'Text file'}
        """
        st.info(file_details)
        
        if st.button(" Process Text", use_container_width=True):
            with st.spinner("Processing your file..."):
                try:
                    # Read file
                    raw_text = read_file(uploaded_file)
                    
                    # Process text (your original processing)
                    processed_text = process_text(raw_text)
                    
                    # Get stats
                    stats = get_stats(raw_text, processed_text)
                    
                    # Generate meaningful summary (new)
                    summary = SmartSummarizer.summarize(raw_text, use_ai=False)
                    
                    # Analyze sentiment (new)
                    sentiment_analyzer = SentimentAnalyzer()
                    sentiment_data = sentiment_analyzer.analyze(raw_text)
                    
                    # Store in session state
                    st.session_state.update({
                        'original': raw_text,
                        'processed': processed_text,
                        'stats': stats,
                        'summary': summary,
                        'sentiment_data': sentiment_data,
                        'sentiment_analyzer': sentiment_analyzer
                    })
                    
                    st.success("✅ File processed successfully!")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    st.markdown("</div>", unsafe_allow_html=True)

    # Display results 
    if 'stats' in st.session_state:
        display_statistics()
        display_sentiment_analysis()
        display_summary()
        display_text_comparison()

def display_statistics():
    st.markdown("<div class='content-section'>", unsafe_allow_html=True)
    st.markdown("### 📊 Text Statistics")
    
    stats = st.session_state.stats
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        (stats['original_words'], 'Original Words', 'metric-card-sky'),
        (stats['original_chars'], 'Original Characters', 'metric-card-purple'),
        (stats['cleaned_words'], 'Cleaned Words', 'metric-card-sky'),
        (stats['cleaned_chars'], 'Cleaned Characters', 'metric-card-purple')
    ]
    
    for col, (value, label, css_class) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(f"""
                <div class='{css_class}'>
                    <div class='metric-value'>{value:,}</div>
                    <div class='metric-label'>{label}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
def display_sentiment_analysis():
    """Display sentiment analysis with single attractive bar chart"""
    if 'sentiment_data' in st.session_state:
        st.markdown("<div class='content-section'>", unsafe_allow_html=True)
        st.markdown("### 📈 Sentiment Analysis")
        
        sentiment_data = st.session_state.sentiment_data
        analyzer = st.session_state.sentiment_analyzer
        
        # Key metrics in a single row
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div class='sentiment-metric-card overall-card'>
                    <div class='sentiment-metric-value'>{sentiment_data['sentiment']}</div>
                    <div class='sentiment-metric-label'>Overall Sentiment</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class='sentiment-metric-card'>
                    <div class='sentiment-metric-value'>{sentiment_data['confidence']:.1f}%</div>
                    <div class='sentiment-metric-label'>Confidence</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            compound = sentiment_data['scores']['compound']
            st.markdown(f"""
                <div class='sentiment-metric-card'>
                    <div class='sentiment-metric-value'>{compound:.3f}</div>
                    <div class='sentiment-metric-label'>Compound Score</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Single attractive bar chart - full width
        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
        bar_chart = analyzer.create_sentiment_barchart(sentiment_data, height=450)
        st.plotly_chart(bar_chart, use_container_width=True)
        
        # Sentiment percentages below the chart
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("##### 📊 Detailed Percentages")
        
        scores = sentiment_data['scores']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Positive", f"{scores['pos']:.1%}")
        with col2:
            st.metric("Neutral", f"{scores['neu']:.1%}")
        with col3:
            st.metric("Negative", f"{scores['neg']:.1%}")
        
        st.markdown("</div>", unsafe_allow_html=True)

def display_summary():
    """Display summary section (updated)"""
    if 'summary' in st.session_state:
        st.markdown("<div class='content-section'>", unsafe_allow_html=True)
        st.markdown("### 📝 Document Summary")
        
        summary = st.session_state.summary
        summary_words = len(summary.split())
        original_words = st.session_state.stats['original_words']
        compression_ratio = (summary_words / original_words * 100) if original_words > 0 else 0
        
        # Summary stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Summary Length", f"{summary_words:,} words")
        with col2:
            st.metric("Compression", f"{compression_ratio:.1f}%")
        with col3:
            st.metric("Reading Time", f"{summary_words/200:.1f} min")
        
        # Summary text with styling
        st.markdown("##### 📋 Summary Content")
        st.markdown(f"""
            <div class='summary-box'>
                <p style='font-size: 16px; line-height: 1.6;'>
                    {summary}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Download button for summary
        st.download_button(
            label="⬇️ Download Summary",
            data=summary,
            file_name="document_summary.txt",
            mime="text/plain",
            use_container_width=True,
            key="download_summary"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)

def display_text_comparison():
    """Display text comparison - ONLY side by side column"""
    st.markdown("<div class='content-section'>", unsafe_allow_html=True)
    st.markdown("### 📝 Text Comparison")
    
    # Only side-by-side view (no tabs)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Original Text**")
        st.text_area("", st.session_state.original[:2000], height=300, label_visibility="collapsed")
    
    with col2:
        st.markdown("**Processed Text**")
        st.text_area("", st.session_state.processed[:2000], height=300, label_visibility="collapsed")
    
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()