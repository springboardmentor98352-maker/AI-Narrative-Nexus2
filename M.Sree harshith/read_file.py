import pandas as pd
from pypdf import PdfReader

def read_file(uploaded_file):
    if uploaded_file is None:
        return "", None

    file_type = uploaded_file.type

    if file_type == "text/plain":
        return uploaded_file.read().decode("utf-8"), None

    elif file_type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text, None

    elif file_type == "text/csv":
        df = pd.read_csv(uploaded_file)
        return None, df

    return "", None
