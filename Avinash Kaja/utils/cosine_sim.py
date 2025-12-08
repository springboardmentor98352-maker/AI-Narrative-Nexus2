from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np


def compute_cosine_similarity(docs):
    tfidf = TfidfVectorizer().fit_transform(docs)
    sim = cosine_similarity(tfidf)

    df = pd.DataFrame(
        sim,
        index=[f"Doc {i + 1}" for i in range(len(docs))],
        columns=[f"Doc {i + 1}" for i in range(len(docs))],
    )

    sim2 = df.copy()
    np.fill_diagonal(sim2.values, -1)
    i, j = divmod(sim2.values.argmax(), sim2.shape[1])

    highest = {"pair": (df.index[i], df.columns[j]), "score": df.values[i][j]}
    return df, highest
