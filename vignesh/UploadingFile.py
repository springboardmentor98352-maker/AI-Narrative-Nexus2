import streamlit as st
import pandas as pd
from io import BytesIO
import PyPDF2
import docx2txt

def extract_content(file):
    
    file_type = file.name.split('.')[-1].lower()
    
    try:
        if file_type in ['txt', 'py', 'json']:
            # Text-based files
            content = file.read().decode('utf-8')
            return content, 'text/plain'
        
        elif file_type == 'csv':
            # CSV files
            df = pd.read_csv(file)
            content = df.to_string()
            return content, 'text/plain'
        
        elif file_type == 'xlsx':
            # Excel files
            df = pd.read_excel(file)
            content = df.to_string()
            return content, 'text/plain'
        
        elif file_type == 'pdf':
            # PDF files
            pdf_reader = PyPDF2.PdfReader(file)
            content = ""
            for page in pdf_reader.pages:
                content += page.extract_text() + "\n"
            return content, 'text/plain'
        
        elif file_type == 'docx':
            # Word documents - save to temp file first
            with open("temp.docx", "wb") as f:
                f.write(file.getbuffer())
            content = docx2txt.process("temp.docx")
            return content, 'text/plain'
        
        else:
            return "Unsupported file type", 'text/plain'
    
    except Exception as e:
        return f"Error reading file: {str(e)}", 'text/plain'

st.title("File Uploader & Content Extractor")

file = st.file_uploader("Upload a file", type=["txt", "py", "json", "csv", "pdf", "docx", "xlsx"])

if file:
    with st.spinner("Extracting content..."):
        content, mime_type = extract_content(file)
    
    st.success(f"File '{file.name}' uploaded successfully!")
    
    st.text_area("File Content", content, height=300)
    
    st.download_button(
        label="Download Extracted Content",
        data=content,
        file_name=f"extracted_{file.name.split('.')[0]}.txt",
        mime=mime_type
    )