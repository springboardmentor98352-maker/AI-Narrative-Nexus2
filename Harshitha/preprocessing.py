import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

STOP = set(stopwords.words("english"))
LEM = WordNetLemmatizer()

def clean_text(text):
    text = re.sub(r"[^a-zA-Z ]", " ", text.lower())
    tokens = [LEM.lemmatize(t) for t in text.split() if t not in STOP and len(t) > 2]
    return " ".join(tokens)
