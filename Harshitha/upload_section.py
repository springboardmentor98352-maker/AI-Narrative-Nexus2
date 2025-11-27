import streamlit as st

def upload_and_input():
    if "text_input" not in st.session_state:
        st.session_state.text_input = ""
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []

    # Smaller black upload text
    st.markdown(
        "<h5 style='color:black; font-size:16px;'>Upload Document (csv, pdf, txt, docx)</h5>",
        unsafe_allow_html=True
    )

    # Disable uploader if user typed something
    uploader_disabled = True if st.session_state.text_input.strip() else False

    uploaded_files = st.file_uploader(
        "Drag and drop files here",
        type=["csv", "pdf", "txt", "docx"],
        accept_multiple_files=True,
        disabled=uploader_disabled
    )

    if uploaded_files:
        st.session_state.uploaded_files = uploaded_files

    text_disabled = False
    selected_files = []

    if uploaded_files:
        uploaded_names = [f.name for f in uploaded_files]
        selected_names = st.multiselect(
            "Select file(s) to analyze",
            uploaded_names,
        )
        selected_files = [f for f in uploaded_files if f.name in selected_names]

        if selected_files:
            text_disabled = True

    text = st.text_area(
        "Or paste text here (paste OR upload files, not both)",
        value=st.session_state.text_input,
        height=200,
        disabled=text_disabled
    )

    if text.strip():
        st.session_state.text_input = text

    analyze = st.button("Analyze Text")

    return selected_files, text, analyze
