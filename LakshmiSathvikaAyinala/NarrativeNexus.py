import streamlit as st
from utils.file_reader import read_file
from utils.text_processor import process_text, get_stats

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
                    # Read and process file
                    raw_text = read_file(uploaded_file)
                    processed_text = process_text(raw_text)
                    
                    # Store in session state
                    st.session_state.update({
                        'original': raw_text,
                        'processed': processed_text,
                        'stats': get_stats(raw_text, processed_text)
                    })
                    
                    st.success("✅ File processed successfully!")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    st.markdown("</div>", unsafe_allow_html=True)

    # Display results 
    if 'stats' in st.session_state:
        display_statistics()
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

def display_text_comparison():
    st.markdown("<div class='content-section'>", unsafe_allow_html=True)
    st.markdown("### 📝 Text Comparison")
    
    tab1, tab2, tab3 = st.tabs(["🔄 Side by Side", "📄 Original Text", "✨ Processed Text"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Original Text**")
            st.text_area("", st.session_state.original[:2000], height=300, label_visibility="collapsed")
        with col2:
            st.markdown("**Processed Text**")
            st.text_area("", st.session_state.processed[:2000], height=300, label_visibility="collapsed")
    
    with tab2:
        st.text_area("", st.session_state.original, height=400, label_visibility="collapsed")
    
    with tab3:
        st.text_area("", st.session_state.processed, height=400, label_visibility="collapsed")
        st.download_button(
            label="⬇️ Download Processed Text",
            data=st.session_state.processed,
            file_name="processed_text.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()