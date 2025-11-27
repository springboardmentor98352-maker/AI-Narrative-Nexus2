# preprocessing.py

import os
import re
import pandas as pd
import nltk

# ---------- SAFE DOWNLOADS ----------
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


# Output folder
OUTPUT_DIR = "Final_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# NLP components
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


# ----------------------------------------------------
# COUNT WORDS
# ----------------------------------------------------
def count_words(text: str) -> int:
    if not isinstance(text, str):
        return 0
    return len(text.split())


# ----------------------------------------------------
# CLEAN EACH CELL OF CSV
# ----------------------------------------------------
def clean_cell(cell):
    """Clean a single CSV cell by applying clean_text."""
    if not isinstance(cell, str):
        cell = str(cell)
    return clean_text(cell)


# ----------------------------------------------------
# CLEAN TEXT (TXT / PDF)
# ----------------------------------------------------
def clean_text(text: str) -> str:
    """
    Cleans text by:
    - Lowercasing
    - Removing special characters
    - Removing stopwords
    - Lemmatizing
    """

    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9.\s]", " ", text)

    tokens = text.split()
    tokens = [t for t in tokens if t not in stop_words]
    tokens = [lemmatizer.lemmatize(t) for t in tokens]

    return " ".join(tokens)


# ----------------------------------------------------
# PREPROCESS MAIN (txt/pdf/csv)
# ----------------------------------------------------
def preprocess_text(text=None, file_type=None, df=None):
    """
    Processes TXT / PDF / CSV files and saves results in Final_data/
    """

    try:
        # ---------- TXT / PDF ----------
        if file_type in ["txt", "pdf"]:
            cleaned = clean_text(text)

            save_path = os.path.join(OUTPUT_DIR, "processed_text.txt")
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(cleaned)

            return cleaned, None

        # ---------- CSV ----------
        elif file_type == "csv":
            if df is None:
                return None, "CSV DataFrame missing."

            text_cols = df.select_dtypes(include=["object"]).columns.tolist()

            for col in text_cols:
                df[col] = df[col].apply(clean_cell)

            save_path = os.path.join(OUTPUT_DIR, "processed_csv.csv")
            df.to_csv(save_path, index=False)

            return df, None

        else:
            return None, "Unsupported file type."

    except Exception as e:
        return None, f"Preprocessing error: {str(e)}"
