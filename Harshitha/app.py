import streamlit as st
from ui import apply_custom_css
from analysis import analyze_text
from summary import generate_summary
from preprocessing import clean_text
from upload_section import upload_and_input
from results_section import show_results
import PyPDF2
import docx2txt
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

st.set_page_config(page_title="NarrativeNexus", layout="wide")
apply_custom_css()

st.markdown("<h1 class='title'>NarrativeNexus</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle' style='color:#ff4b8b;'>Dynamic AI Text Analysis Platform</p>", unsafe_allow_html=True)


uploaded_files, user_text, analyze = upload_and_input()

def extract_text_from_file(file):
    if file.type == "application/pdf":
        try:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
            return text
        except:
            try:
                return file.getvalue().decode("utf-8", errors="ignore")
            except:
                return ""
    if file.type in ("application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"):
        try:
            return docx2txt.process(file)
        except:
            try:
                return file.getvalue().decode("utf-8", errors="ignore")
            except:
                return ""
    if file.type in ("text/csv", "text/plain", "application/csv"):
        try:
            df = pd.read_csv(file)
            texts = []
            for col in df.columns:
                if df[col].dtype == object:
                    texts.append(" ".join(df[col].astype(str).tolist()))
            return "\n".join(texts) if texts else df.to_csv(index=False)
        except:
            try:
                return file.getvalue().decode("utf-8", errors="ignore")
            except:
                return ""
    try:
        return file.getvalue().decode("utf-8", errors="ignore")
    except:
        return ""

def generate_pdf(original, analysis, summary):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 50

    def write(text):
        nonlocal y
        lines = text.split("\n")
        for line in lines:
            if y < 50:
                c.showPage()
                y = height - 50
            c.drawString(50, y, line)
            y -= 16

    write("NarrativeNexus Analysis Report\n")
    write("\nOriginal Text:\n")
    write(original[:5000])

    write("\nAnalysis:\n")
    for k, v in analysis.items():
        write(f"{k}: {v}")

    write("\nSummary:\n")
    write(summary)

    c.save()
    buffer.seek(0)
    return buffer

if analyze:
    final_text = ""
    if uploaded_files:
        parts = []
        for f in uploaded_files:
            parts.append(extract_text_from_file(f))
        final_text = "\n\n".join([p for p in parts if p])
    elif user_text and user_text.strip():
        final_text = user_text
    else:
        st.error("No text provided. Paste text or upload files.")
        st.stop()

    if not final_text.strip():
        st.error("Uploaded files contained no readable text.")
        st.stop()

    cleaned = clean_text(final_text)
    analysis = analyze_text(final_text)
    summary = generate_summary(final_text)

    show_results(final_text,
                 analysis,
                 analysis.get("sentence_level", []),
                 None,
                 analysis.get("keywords", []),
                 summary)

    pdf_file = generate_pdf(final_text, analysis, summary)

    st.download_button(
        "Download PDF Report",
        data=pdf_file,
        file_name="NarrativeNexus_Report.pdf",
        mime="application/pdf"
    )
