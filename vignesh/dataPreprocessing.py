import pandas as pd
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import nltk

#LOAD CSV DIRECTLY
df = pd.read_csv("train.csv", encoding="latin-1")  

print("Shape before dropping missing text:", df.shape)

#HANDLE MISSING VALUES
df = df.dropna(subset=["text"]).copy()
print("Shape after dropping missing text:", df.shape)


# TEXT CLEANING + TOKENIZATION + LEMMATIZATION

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

# Run these once only (requires internet for first download)
# nltk.download("wordnet")
# nltk.download("omw-1.4")
# nltk.download("punkt")
# nltk.download("averaged_perceptron_tagger")

lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(tag):
    """Map NLTK POS tag to wordnet POS for better lemmatization."""
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN  # default


def clean_and_tokenize(text: str):
    """Clean text, remove noise, tokenize and lemmatize."""
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\.\S+", " ", text)

    # Remove @mentions and hashtags
    text = re.sub(r"[@#]\w+", " ", text)

    # Remove anything not letters or space
    text = re.sub(r"[^a-z\s]", " ", text)

    # Collapse repeated spaces
    text = re.sub(r"\s+", " ", text).strip()

    # Tokenize
    tokens = text.split()

    # Remove stopwords
    tokens = [t for t in tokens if t not in ENGLISH_STOP_WORDS]

    # POS tagging for smarter lemmatization
    tagged = nltk.pos_tag(tokens)

    lemmas = [
        lemmatizer.lemmatize(word, get_wordnet_pos(pos)) 
        for (word, pos) in tagged
    ]

    clean_text = " ".join(lemmas)
    return clean_text, lemmas


# Apply cleaning function
clean_output = df["text"].apply(clean_and_tokenize)

df["clean_text"] = clean_output.apply(lambda x: x[0])
df["tokens"] = clean_output.apply(lambda x: x[1])


#SAVE PROCESSED FILE
output_file = "train_cleaned.csv"
df.to_csv(output_file, index=False, encoding="utf-8")

print(f"Cleaned dataset saved as: {output_file}")
print(df[["text", "clean_text", "tokens"]].head())
