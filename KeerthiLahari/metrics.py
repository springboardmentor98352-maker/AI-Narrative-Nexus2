import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter
nltk.download("vader_lexicon", quiet=True)
sia = SentimentIntensityAnalyzer()

# ------------ BASIC METRICS ---------------- #


def word_count(text):
    return len(text.split())


def sentence_count(text):
    return len([s for s in text.split(".") if s.strip()])


def top_tokens(text, n=10):
    tokens = text.split()
    return Counter(tokens).most_common(n)


def sentiment_analysis(text):
    return sia.polarity_scores(text)


def sentiment_distribution(sentiment_scores):
    return {
        "Positive": sentiment_scores.get("pos", 0),
        "Negative": sentiment_scores.get("neg", 0),
        "Neutral": sentiment_scores.get("neu", 0)
    }


def overall_sentiment(score):
    if score > 0.2:
        return " Positive"
    elif score < -0.2:
        return " Negative "
    else:
        return " Neutral"
