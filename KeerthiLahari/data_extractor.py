import pandas as pd
from PyPDF2 import PdfReader
from io import StringIO

def extract_text_from_file(uploaded_file=None, pasted_text=None):
    """
    Extract text either from uploaded file OR from manually pasted text.
    Returns:
    - raw_text (string)
    - file_type (txt/pdf/csv)
    - df (for csv only)
    - error message
    """

    # Case 1: Manual text input
    if pasted_text and pasted_text.strip():
        return pasted_text, "txt", None, None

    # Case 2: No input
    if uploaded_file is None:
        return None, None, None, "No file uploaded or text pasted."

    filename = uploaded_file.name
    file_type = filename.split(".")[-1].lower()

    try:
        if file_type == "txt":
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            text = stringio.read()
            return text, "txt", None, None

        elif file_type == "pdf":
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text, "pdf", None, None

        elif file_type == "csv":
            df = pd.read_csv(uploaded_file)
            return None, "csv", df, None

        return None, None, None, "Unsupported file format."

    except Exception as e:
        return None, None, None, f"Error reading file: {str(e)}"
