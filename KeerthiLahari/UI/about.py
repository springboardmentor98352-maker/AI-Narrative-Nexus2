import streamlit as st


def render_about():
    st.markdown("""
    <div style="text-align:justify; font-size:18px;">
    Narrative Nexus is a dynamic text analysis platform designed to help users quickly summarize content,
    measure word and character counts, evaluate sentiment, and generate meaningful insights from any text.
    The application supports text uploads and manual input, processes data efficiently, and delivers clearly
    structured results that can be downloaded for further use. With features ranging from automated summarization
    to sentiment distribution visualization, Narrative Nexus provides a simple yet powerful tool for students,
    researchers, professionals, and anyone looking to understand and refine their written content with ease.
    </div>
    """, unsafe_allow_html=True)
