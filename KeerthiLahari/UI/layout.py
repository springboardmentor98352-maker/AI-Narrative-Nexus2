import streamlit as st
from streamlit_option_menu import option_menu


def render_header():
    st.set_page_config(
        page_title="Narrative Nexus",
        page_icon="🧠",
        layout="centered",
    )

    st.markdown("<h1 class='center-text'>Narrative Nexus 🧠</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='center-text spacing'>Dynamic Text Analysis Platform</h3>", unsafe_allow_html=True)
    st.markdown("<p class='center-text spacing'>summarise • analyze • get insights</p>", unsafe_allow_html=True)


def render_menu():
    return option_menu(
        menu_title=None,
        options=["About", "Input", "Analysis"],
        icons=["house", "upload", "bar-chart"],
        default_index=1,
        orientation="horizontal",
    )

