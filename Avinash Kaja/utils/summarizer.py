from transformers import pipeline

summarize_model = pipeline(
    "summarization", model="sshleifer/distilbart-cnn-12-6", revision="a4f8"
)


def chunk_text(text, max_words=700):
    words = text.split()
    for i in range(0, len(words), max_words):
        yield " ".join(words[i : i + max_words])


def summarize(text):
    text = text.strip()
    if len(text.split()) < 40:
        return text

    summaries = []
    for chunk in chunk_text(text):
        try:
            summary = summarize_model(
                chunk, max_length=150, min_length=50, do_sample=False
            )[0]["summary_text"]
            summaries.append(summary)
        except Exception:
            summaries.append(chunk[:300])

    return " ".join(summaries)
