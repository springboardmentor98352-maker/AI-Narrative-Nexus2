import os
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter
import matplotlib.pyplot as plt

nltk.download("vader_lexicon", quiet=True)

sia = SentimentIntensityAnalyzer()

# ------------ BASIC METRICS ---------------- #


def word_count(text):
    return len(text.split())


def sentence_count(text):
    return len([s for s in text.split(".") if s.strip()])


def sentiment_analysis(text):
    return sia.polarity_scores(text)


def sentiment_distribution(sentiment_scores):
    return {
        "Positive": sentiment_scores.get("pos", 0),
        "Negative": sentiment_scores.get("neg", 0),
        "Neutral": sentiment_scores.get("neu", 0)
    }


def sentiment_to_emoji(score):
    """Return BIG emoji for sentiment."""
    if score > 0.2:
        return " Positive"
    elif score < -0.2:
        return " Negative "
    else:
        return " Neutral"


def sentiment_distribution_chart(distribution):
    labels = list(distribution.keys())
    values = list(distribution.values())

    fig, ax = plt.subplots()
    ax.bar(labels, values)  # default colors
    ax.set_title("Sentiment Distribution")
    ax.set_xlabel("Sentiment Type")
    ax.set_ylabel("Score")
    ax.grid(axis='y', linestyle='--', alpha=0.4)

    return fig


def top_tokens(text, n=10):
    tokens = text.split()
    return Counter(tokens).most_common(n)


def simple_summary(text):
    #extractive summary.
    sentences = text.split(".")
    if len(sentences) > 2:
        return sentences[0].strip() + ". " + sentences[-2].strip() + "."
    else:
        return text[:2000] + "..."


# ------------ LOAD PROCESSED DATA ------------- #

def load_processed_text():
    """Loads processed txt or csv from Final_data."""

    folder = "Final_data"
    txt_path = os.path.join(folder, "processed_text.txt")

    # Load processed text
    if os.path.exists(txt_path):
        with open(txt_path, "r") as f:
            return f.read(), "txt"

    # Load processed csv
    csv_path = os.path.join(folder, "processed_csv.csv")
    if os.path.exists(csv_path):
        import pandas as pd
        df = pd.read_csv(csv_path)

        # Combine all string/object columns into a single large text blob
        combined = " ".join(
            df.select_dtypes(include="object")
              .astype(str)
              .fillna("")
              .values.flatten()
        )
        return combined, "csv"

    return None, None
