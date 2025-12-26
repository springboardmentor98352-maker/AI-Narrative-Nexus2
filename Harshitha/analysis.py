import nltk
from collections import Counter
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation, NMF

nltk.download("punkt", quiet=True)

def analyze_text(text, cleaned_text):
    sentences = nltk.sent_tokenize(text)
    words = text.split()

    sentiment_labels = []
    for s in sentences:
        polarity = TextBlob(s).sentiment.polarity
        if polarity > 0.1:
            sentiment_labels.append("Positive")
        elif polarity < -0.1:
            sentiment_labels.append("Negative")
        else:
            sentiment_labels.append("Neutral")

    counts = Counter(sentiment_labels)

    overall = counts.most_common(1)[0][0] if counts else "Neutral"

    top_keywords = [w for w, _ in Counter(cleaned_text.split()).most_common(10)]

    topics = {"lda": [], "nmf": []}
    if cleaned_text.strip() and len(cleaned_text.split()) > 5:
        cv = CountVectorizer(max_features=100, stop_words="english")
        X = cv.fit_transform([cleaned_text])
        lda = LatentDirichletAllocation(n_components=3, random_state=42)
        lda.fit(X)
        words_lda = cv.get_feature_names_out()
        for idx, topic in enumerate(lda.components_):
            top_words = [words_lda[i] for i in topic.argsort()[-6:]]
            topics["lda"].append(f"Topic {idx+1}: {', '.join(top_words)}")
        tfidf = TfidfVectorizer(max_features=100, stop_words="english")
        X2 = tfidf.fit_transform([cleaned_text])
        nmf = NMF(n_components=3, random_state=42)
        nmf.fit(X2)
        words_nmf = tfidf.get_feature_names_out()
        for idx, topic in enumerate(nmf.components_):
            top_words = [words_nmf[i] for i in topic.argsort()[-6:]]
            topics["nmf"].append(f"Topic {idx+1}: {', '.join(top_words)}")
    summary = " ".join(sentences[:3])
    insights = [
        f"Text contains {len(words)} words.",
        f"Overall sentiment is {overall}.",
        "Key themes identified using topic modeling.",
        "Refinement may improve clarity and tone."
    ]

    return {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "overall_sentiment": overall,
        "sentiment_distribution": dict(counts),
        "top_keywords": top_keywords,
        "topics": topics,
        "summary": summary,
        "insights": insights
    }
