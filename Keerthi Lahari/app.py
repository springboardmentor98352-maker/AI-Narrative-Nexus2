import streamlit as st
import pandas as pd
import json
from io import StringIO
from PyPDF2 import PdfReader
import docx

st.set_page_config(page_title="Dynamic Text Summarisation", layout="wide")
st.title("Dynamic Text Summarisation App")

st.write(
    "Upload your file below (supported: `.txt`, `.csv`, "
    "`.json`, `.pdf`, `.docx`) ")


# Step 1: Upload file
uploaded_file = st.file_uploader(
    "Choose a file", 
    type=["txt", "csv", "json", "pdf", "docx"]
)

if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()  # preprocessing
    st.info(f"Uploaded file type detected: `{file_type}`")

    text_data = ""  # Initialize variable to hold extracted text

    try:
        # Step 2: Detect and extract text
        if file_type == "txt":
            # Read plain text files
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            text_data = stringio.read()

        elif file_type == "csv":
            df = pd.read_csv(uploaded_file)
            text_data = df.to_string(index=False)

        elif file_type == "json":
            data = json.load(uploaded_file)
            text_data = json.dumps(data, indent=2)

        elif file_type == "pdf":
            reader = PdfReader(uploaded_file)
            text_data = ""
            for page in reader.pages:
                text_data += page.extract_text() or ""

        elif file_type == "docx":
            doc = docx.Document(uploaded_file)
            text_data = "\n".join([para.text for para in doc.paragraphs])

        else:
            st.error("Unsupported file type.")
            text_data = None

        # Step 3: Check if text was successfully extracted
        if text_data and text_data.strip():
            st.success("Text data detected in the uploaded file!")
            with st.expander("📜 View Extracted Text"):
                st.write(
                    text_data[:2000] +
                    ("..." if len(text_data) > 2000 else "")
                )
        else:
            st.warning(
                "⚠️ The uploaded file does not seem to contain "
                "readable text data."
            )

    except Exception as e:
        st.error(f"Error reading file: {e}")

else:
    st.info("Please upload a file to begin.")
