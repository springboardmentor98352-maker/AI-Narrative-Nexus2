import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
def generate_summary(text, n_sentences=3):
    sents = nltk.tokenize.sent_tokenize(text)
    if len(sents) <= n_sentences:
        return " ".join(sents)
    try:
        vect = TfidfVectorizer(stop_words='english')
        X = vect.fit_transform(sents)
        scores = np.asarray(X.sum(axis=1)).ravel()
        top_idx = scores.argsort()[-n_sentences:][::-1]
        summary = " ".join([sents[i] for i in sorted(top_idx)])
        return summary
    except Exception:
        return " ".join(sents[:n_sentences])
