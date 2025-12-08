def apply_custom_css():
    css = """
    <style>
    body {
        background-color: #0f0c29;
        background-image: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white !important;
    }

    .title {
        text-align: center;
        font-size: 45px;
        font-weight: bold;
        color: white;
        margin-top: -30px;
    }

    .subtitle {
        text-align: center;
        font-size: 20px;
        color: #d7d7ff;
        margin-bottom: 20px;
    }

    .stButton>button {
        background-color: #ff4b8b;
        color: white;
        padding: 10px 25px;
        border-radius: 10px;
        border: none;
        font-size: 18px;
        font-weight: bold;
        width: 200px;
    }

    .stButton>button:hover {
        background-color: #ff2d75;
        color: white;
    }

    .stTextArea textarea {
        background-color: #1a1535;
        color: white;
        border-radius: 10px;
    }

    .css-1d391kg {
        background-color: transparent !important;
    }

    .stFileUploader {
        color: white !important;
    }
    </style>
    """
    import streamlit as st
    st.markdown(css, unsafe_allow_html=True)
