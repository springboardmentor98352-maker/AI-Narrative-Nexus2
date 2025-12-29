import os
import random
import numpy as np
import nltk
import pandas as pd
from collections import Counter
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation, NMF

# ------------------ Ensure NLTK data ------------------
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

# ------------------ Paths ------------------
TEXT_FILE = "Final_data/processed_text.txt"
CSV_FILE = "Final_data/processed_csv.csv"

# ------------------ Load processed text ------------------
def load_processed_text():
    if not os.path.exists(TEXT_FILE):
        return None
    with open(TEXT_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

# ------------------ Chunk text by sentences ------------------
def chunk_text_by_sentences(text, chunk_size=4):
    sentences = sent_tokenize(text)
    return [
        " ".join(sentences[i:i + chunk_size])
        for i in range(0, len(sentences), chunk_size)
    ]

# ------------------ LDA keywords ------------------
def extract_keywords_lda(text, top_n=10):
    vectorizer = CountVectorizer(
        stop_words="english",
        max_df=1.0,
        min_df=1
    )
    X = vectorizer.fit_transform([text])
    lda = LatentDirichletAllocation(n_components=1, random_state=42)
    lda.fit(X)
    words = vectorizer.get_feature_names_out()
    indices = lda.components_[0].argsort()[-top_n:]
    return [words[i] for i in indices]

# ------------------ NMF keywords ------------------
def extract_keywords_nmf(text, top_n=10):
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_df=1.0,
        min_df=1,
        ngram_range=(1, 2)
    )
    X = vectorizer.fit_transform([text])
    nmf = NMF(n_components=1, random_state=42, max_iter=500)
    nmf.fit(X)
    words = vectorizer.get_feature_names_out()
    indices = nmf.components_[0].argsort()[-top_n:]
    return [words[i] for i in indices]

# ------------------ Main summary function ------------------
def generate_abstractive_summary():
    text = load_processed_text()
    if not text:
        return None, "❌ Please preprocess text first."

    chunks = chunk_text_by_sentences(text, chunk_size=4)
    if len(chunks) < 2:
        return "Fallback", text

    model_used = random.choice(["LDA", "NMF"])
    keywords = extract_keywords_nmf(text) if model_used == "NMF" else extract_keywords_lda(text)
    keyword_counts = Counter(keywords)

    scores = []
    for idx, chunk in enumerate(chunks):
        words = chunk.lower().split()
        score = sum(keyword_counts.get(w, 0) for w in words)
        score += 0.1 / (idx + 1)  # Position bias: early chunks slightly preferred
        scores.append(score)

    # Select top 30-40% chunks
    top_n = max(1, int(len(chunks) * 0.4))
    top_indices = np.argsort(scores)[-top_n:]
    top_indices.sort()

    summary = " ".join(chunks[i] for i in top_indices)
    return model_used, summary

# ------------------ CSV summary ------------------
def summarize_csv():
    if not os.path.exists(CSV_FILE):
        return None
    df = pd.read_csv(CSV_FILE)
    # Only return the describe() for numerical columns
    return df.describe()
