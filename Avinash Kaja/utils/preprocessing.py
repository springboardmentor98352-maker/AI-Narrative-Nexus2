import re, nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

STOP = set(stopwords.words("english"))
LEM = WordNetLemmatizer()


def preprocess_text(text):
    text = re.sub(r"[^A-Za-z\s]", " ", text.lower())
    tokens = nltk.word_tokenize(text)
    tokens = [LEM.lemmatize(t) for t in tokens if t not in STOP and len(t) > 2]
    return " ".join(tokens)
