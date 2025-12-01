# summarizer.py

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import re

# --- NLTK DOWNLOADS ---
import nltk

# Fix for new NLTK versions
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab")

# --- END DOWNLOADS ---


def extractive_summarize(text: str, num_sentences: int) -> str:
    """
    Generates an extractive summary of the text using NLTK sentence ranking.
    """
    if not isinstance(text, str) or not text.strip():
        return "Error: Input text is empty."
    
    # 1. Tokenize into sentences
    sentences = sent_tokenize(text)
    
    # If text is too short, return it as is or handle gracefully
    if len(sentences) <= num_sentences:
        return text
    
    # 2. Prepare tokens and stopwords
    words = word_tokenize(text.lower())
    # Use standard NLTK stopwords plus punctuation
    stop_words = set(stopwords.words("english") + list(punctuation))
    
    # 3. Frequency count of non-stopwords
    word_freq = defaultdict(int)
    for word in words:
        if word not in stop_words:
            # Clean non-alphanumeric words that might have slipped through
            cleaned_word = re.sub(r'[^a-z]', '', word)
            if cleaned_word and len(cleaned_word) > 1: # Ignore single letters
                word_freq[cleaned_word] += 1

    # 4. Normalize frequencies (optional but good practice)
    if not word_freq:
        return "Error: No meaningful words found after cleaning."
        
    max_freq = max(word_freq.values())
    for word in word_freq:
        word_freq[word] = (word_freq[word] / max_freq)
        
    # 5. Calculate sentence scores
    sentence_scores = defaultdict(int)
    for i, sentence in enumerate(sentences):
        # Use lowercased, cleaned words for scoring
        for word in word_tokenize(sentence.lower()):
            cleaned_word = re.sub(r'[^a-z]', '', word)
            if cleaned_word in word_freq:
                sentence_scores[i] += word_freq[cleaned_word]
                
    # 6. Extract top N sentences
    # nlargest returns a list of the N largest values from an iterable
    select_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    
    # Sort the selected sentence indices to keep the summary chronological
    summary = [sentences[i] for i in sorted(select_sentences)]
    
    return " ".join(summary)