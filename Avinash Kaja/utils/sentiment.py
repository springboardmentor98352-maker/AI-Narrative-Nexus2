from transformers import pipeline

sentiment_model = pipeline("sentiment-analysis")


def get_sentiment(text):
    out = sentiment_model(text[:512])[0]
    return {"label": out["label"], "score": float(out["score"])}
