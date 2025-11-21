import re

def count_words(text):
    if not text or not isinstance(text, str):
        return 0
    return len(text.strip().split())


def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_cell(value):
    if isinstance(value, str):
        value = value.lower()
        value = re.sub(r"[^\w\s]", " ", value)
        value = re.sub(r"\s+", " ", value)
    return value
