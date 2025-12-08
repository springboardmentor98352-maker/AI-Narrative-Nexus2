import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px


def show_wordcloud(text):
    wc = WordCloud(width=800, height=300, background_color=None, mode="RGBA").generate(
        text
    )
    fig = plt.figure(figsize=(10, 3))
    plt.imshow(wc)
    plt.axis("off")
    st.pyplot(fig)


def plot_similarity_heatmap(df):
    fig = px.imshow(df, color_continuous_scale="RdPu")
    st.plotly_chart(fig, use_container_width=True)


def show_card(title, subtitle, body):
    st.markdown(
        f"""
    <div class="glass-card">
      <div class="card-title">{title}</div>
      <div class="small-muted">{subtitle}</div>
      <div style="margin-top:8px; color:#eee;">{body}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )
