from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors

model = None
embeddings = None
nn_index = None
docs_store = None


def build_index(docs):
    global model, embeddings, nn_index, docs_store
    docs_store = docs
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(docs)
    nn_index = NearestNeighbors(metric="cosine").fit(embeddings)


def query(q, top_k=5):
    q_emb = model.encode([q])
    dist, idx = nn_index.kneighbors(q_emb, n_neighbors=top_k)
    results = []
    for d, i in zip(dist[0], idx[0]):
        results.append({"doc": docs_store[i], "score": float(1 - d)})
    return results
