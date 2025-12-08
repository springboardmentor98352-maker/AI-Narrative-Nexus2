import streamlit as st
from collections import Counter

def _sentiment_meter_html(positive, neutral, negative):
    total = positive + neutral + negative
    if total == 0:
        return "<div>No sentence-level sentiments.</div>"
    p = int(round((positive/total)*100))
    n = int(round((neutral/total)*100))
    neg = int(round((negative/total)*100))
    html = f"""
    <div style="width:100%; max-width:900px;">
      <div style="margin-bottom:6px;font-weight:600;">Positive</div>
      <div style="background:#eee;border-radius:6px;height:10px;overflow:hidden;">
        <div style="width:{p}%;background:#2ecc71;height:10px;"></div>
      </div>
      <div style="margin:8px 0 6px;font-weight:600;">Neutral</div>
      <div style="background:#eee;border-radius:6px;height:10px;overflow:hidden;">
        <div style="width:{n}%;background:#f1c40f;height:10px;"></div>
      </div>
      <div style="margin:8px 0 6px;font-weight:600;">Negative</div>
      <div style="background:#eee;border-radius:6px;height:10px;overflow:hidden;">
        <div style="width:{neg}%;background:#e74c3c;height:10px;"></div>
      </div>
      <div style="font-size:12px;color:#ddd;margin-top:8px;">Counts — Positive: {positive}  Neutral: {neutral}  Negative: {negative}</div>
    </div>
    """
    return html

def show_results(raw_text, analysis_results, sent_level, wc_fig, topics, summary_text):
    cols = st.columns([1,1,2])
    with cols[0]:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Word Count")
        st.write(f"**{analysis_results.get('word_count', 0)} words**")
        st.markdown("</div>", unsafe_allow_html=True)
    with cols[1]:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Sentence Count")
        st.write(f"**{analysis_results.get('sentence_count', 0)} sentences**")
        st.markdown("</div>", unsafe_allow_html=True)
    with cols[2]:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        ds = analysis_results.get("sentiment", {})
        label = ds.get("label", "Neutral")
        score = ds.get("score", ds.get("raw_score", ""))
        st.subheader("Overall Sentiment")
        st.markdown(f"<h3 style='color:#F1C40F;'>{label}   <small style='color:#ddd;'>({score})</small></h3>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    dist = analysis_results.get("sentiment_distribution", {})
    pos = int(dist.get("Positive", 0))
    neu = int(dist.get("Neutral", 0))
    neg = int(dist.get("Negative", 0))
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Sentence-level Sentiment (meter)")
    meter_html = _sentiment_meter_html(pos, neu, neg)
    st.markdown(meter_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Executive Summary")
    st.write(summary_text)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Actionable Insights")
    from insights import generate_insights
    insights = generate_insights(raw_text)
    for it in insights:
        st.write(f"- {it}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Extracted Topics")
    if topics:
        for i, t in enumerate(topics, start=1):
            st.write(f"{i}. {t}")
    else:
        st.write("No distinct topics extracted.")
    st.markdown("</div>", unsafe_allow_html=True)

    if wc_fig is not None:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Word Cloud")
        st.pyplot(wc_fig)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Sample Sentence Sentiments")
    for s, lbl, score in sent_level[:6]:
        st.write(f"**[{lbl}]** {s[:260]}{'...' if len(s)>260 else ''}")
    st.markdown("</div>", unsafe_allow_html=True)
