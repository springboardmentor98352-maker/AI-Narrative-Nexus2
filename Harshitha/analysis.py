import nltk
from collections import Counter
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation, NMF
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

nltk.download("punkt", quiet=True)

def analyze_text(text, cleaned_text):
    sentences = nltk.sent_tokenize(text)
    words = text.split()
    sentiment_labels = []
    sentiment_polarities = {"Positive": [], "Neutral": [], "Negative": []}

    for s in sentences:
        polarity = TextBlob(s).sentiment.polarity
        if polarity > 0.05:
            sentiment_labels.append("Positive")
            sentiment_polarities["Positive"].append(polarity)
        elif polarity < -0.05:
            sentiment_labels.append("Negative")
            sentiment_polarities["Negative"].append(polarity)
        else:
            sentiment_labels.append("Neutral")
            sentiment_polarities["Neutral"].append(polarity)

    counts = Counter(sentiment_labels)
    overall = counts.most_common(1)[0][0] if counts else "Neutral"

    overall_polarity = round(
        sum(sentiment_polarities.get(overall, [0])) / max(len(sentiment_polarities.get(overall, [])), 1),
        3
    )    
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
    words_lower = [w.lower() for w in text.split() if w.lower() not in ENGLISH_STOP_WORDS]
    word_freq = Counter(words_lower)

    sentence_scores = {}
    for s in sentences:
        score = 0
        for w in s.lower().split():
            if w in word_freq:
                score += word_freq[w]
        sentence_scores[s] = score

    num_sentences = max(1, int(len(sentences)*0.2))
    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
    summary = " ".join(summary_sentences)
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
        "polarity_score": overall_polarity,
        "sentiment_distribution": dict(counts),
        "top_keywords": top_keywords,
        "topics": topics,
        "summary": summary,
        "insights": insights
    }
