from gensim import corpora
from gensim.models.ldamodel import LdaModel
import pyLDAvis
import pyLDAvis.gensim


def extract_topics(cleaned_docs, n_topics=4):
    tokenized = [doc.split() for doc in cleaned_docs]
    dictionary = corpora.Dictionary(tokenized)
    corpus = [dictionary.doc2bow(text) for text in tokenized]

    lda = LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=n_topics,
        passes=15,
        random_state=42,
    )

    topics = []
    for i in range(n_topics):
        words = lda.show_topic(i, topn=8)
        topics.append([w for w, _ in words])

    return {"topics": topics, "lda": lda, "corpus": corpus, "dictionary": dictionary}


def generate_pyldavis(lda, corpus, dictionary):
    """Create pyLDAvis visualization and return HTML."""
    vis = pyLDAvis.gensim.prepare(lda, corpus, dictionary)
    html = pyLDAvis.prepared_data_to_html(vis)
    return html
