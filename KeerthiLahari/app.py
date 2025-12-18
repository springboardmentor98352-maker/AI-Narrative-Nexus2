import streamlit as st
from UI.layout import render_header, render_menu
from UI.about import render_about
from UI.text_input import render_text_input
from UI.analysis import render_analysis
import os

# ----------- Load global CSS ----------
def load_css():
    css_path = os.path.join("KeerthiLahari", "Styles", "main.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ----------- Render Header ----------
render_header()
load_css()

# ----------- Navigation Menu ----------
selected = render_menu()

# ----------- Render Selected Section ----------
if selected == "About":
    render_about()
elif selected == "Text Input":
    render_text_input()
elif selected == "Text Analysis":
    render_analysis()

