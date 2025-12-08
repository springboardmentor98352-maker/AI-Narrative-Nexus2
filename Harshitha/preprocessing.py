import re
import nltk
try:
    nltk.data.find("tokenizers/punkt")
except Exception:
    nltk.download("punkt")
try:
    nltk.data.find("corpora/stopwords")
except Exception:
    nltk.download("stopwords")
try:
    nltk.data.find("corpora/wordnet")
except Exception:
    nltk.download("wordnet")
try:
    nltk.data.find("taggers/averaged_perceptron_tagger")
except Exception:
    nltk.download("averaged_perceptron_tagger")
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
STOP = set(stopwords.words("english"))
LEMM = WordNetLemmatizer()
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[\r\n\t]+', ' ', text)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t.isalpha() and t not in STOP and len(t) > 2]
    lemmed = [LEMM.lemmatize(t) for t in tokens]
    return " ".join(lemmed)
