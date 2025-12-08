from collections import Counter
import math
def generate_insights(text):
    words = [w for w in text.split() if w.strip()]
    word_count = len(words)
    sentences = text.split(".")
    sentences = [s for s in sentences if s.strip()]
    avg_sent_len = (sum(len(s.split()) for s in sentences) / len(sentences)) if sentences else 0
    cleaned = [w.strip().lower() for w in words if len(w) > 3]
    freq = Counter(cleaned)
    top = [w for w,_ in freq.most_common(6)]
    insights = [
        f"Word count: {word_count}",
        f"Average sentence length (words): {avg_sent_len:.1f}",
        f"Top keywords: {', '.join(top) if top else 'N/A'}",
        "Consider breaking long paragraphs into bullet points for clarity.",
        "If you need a more robust emotional breakdown, enable the transformer-based sentiment (requires model download)."
    ]
    return insights
