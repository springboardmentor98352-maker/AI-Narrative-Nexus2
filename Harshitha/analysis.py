from collections import Counter
import nltk

def _load_transformer_pipeline():
    try:
        from transformers import pipeline
        return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    except Exception:
        return None

TRANSFORMER_PIPELINE = _load_transformer_pipeline()

def analyze_text(text):
    sents = nltk.tokenize.sent_tokenize(text)
    sentences = len(sents)
    words = len([w for w in text.split() if w.strip()])

    sent_by_sentence = sentence_sentiments(text)
    counts = Counter([lbl for (_s, lbl, _score) in sent_by_sentence])
    doc_sent = _document_sentiment(text)

    return {
        "word_count": words,
        "sentence_count": sentences,
        "sentiment": doc_sent,
        "sentiment_distribution": {
            "Positive": int(counts.get("Positive", 0)),
            "Neutral": int(counts.get("Neutral", 0)),
            "Negative": int(counts.get("Negative", 0))
        },
        "keywords": topic_extraction(text),
        "sentence_level": sent_by_sentence
    }

def _document_sentiment(text):
    if TRANSFORMER_PIPELINE:
        try:
            chunks = []
            words = text.split()
            size = 120
            for i in range(0, len(words), size):
                chunks.append(" ".join(words[i:i+size]))
            scores = []
            for c in chunks[:15]:
                out = TRANSFORMER_PIPELINE(c)[0]
                label = out["label"]
                score = float(out["score"])
                if score < 0.40:
                    lbl = "Neutral"
                else:
                    lbl = "Positive" if label.upper().startswith("POS") else "Negative"
                scores.append(lbl)
            if scores.count("Positive") > scores.count("Negative"):
                return {"label": "Positive"}
            if scores.count("Negative") > scores.count("Positive"):
                return {"label": "Negative"}
            return {"label": "Neutral"}
        except Exception:
            pass

    try:
        from textblob import TextBlob
        p = TextBlob(text).sentiment.polarity
        if p > 0.1:
            return {"label": "Positive", "raw_score": p}
        if p < -0.1:
            return {"label": "Negative", "raw_score": p}
        return {"label": "Neutral", "raw_score": p}
    except Exception:
        return {"label": "Neutral", "raw_score": 0.0}

def sentence_sentiments(text):
    sents = nltk.tokenize.sent_tokenize(text)
    res = []
    for s in sents[:80]:
        label, score = _sentiment_of_sentence(s)
        res.append((s, label, score))
    return res

def _sentiment_of_sentence(sentence):
    if TRANSFORMER_PIPELINE:
        try:
            out = TRANSFORMER_PIPELINE(sentence[:512])[0]
            label = out["label"]
            score = float(out["score"])
            if score < 0.40:
                return "Neutral", score
            return ("Positive", score) if label.upper().startswith("POS") else ("Negative", score)
        except Exception:
            pass

    try:
        from textblob import TextBlob
        p = TextBlob(sentence).sentiment.polarity
        if p > 0.1:
            return "Positive", p
        if p < -0.1:
            return "Negative", p
        return "Neutral", p
    except Exception:
        return "Neutral", 0.0

def generate_wordcloud_fig(cleaned_text):
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    wc = WordCloud(width=800, height=400, background_color=None, mode="RGBA").generate(cleaned_text)
    fig = plt.figure(figsize=(8,4))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    return fig

def topic_extraction(cleaned_text, n_topics=4, n_top_words=6):
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.decomposition import NMF
        tokens = cleaned_text.split()
        chunk_size = 200
        docs = [" ".join(tokens[i:i+chunk_size]) for i in range(0, len(tokens), chunk_size)]
        if len(docs) == 0:
            return []
        vec = TfidfVectorizer(max_features=2000, ngram_range=(1,2))
        X = vec.fit_transform(docs)
        n_topics = min(n_topics, X.shape[0], 6)
        nmf = NMF(n_components=n_topics, random_state=42, init="nndsvda", max_iter=400)
        H = nmf.fit_transform(X)
        comps = nmf.components_
        feat = vec.get_feature_names_out()
        topics = []
        for topic in comps:
            top = topic.argsort()[-n_top_words:][::-1]
            topics.append(", ".join([feat[i] for i in top]))
        return topics
    except Exception:
        return []
