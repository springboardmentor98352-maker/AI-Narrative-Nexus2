# nlp_models.py

# Removed gensim imports
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 
import pandas as pd
import logging
import nltk

# --- NLTK VADER SETUP ---
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')
analyzer = SentimentIntensityAnalyzer()
# --- END VADER SETUP ---

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# ==============================================================================
# SENTIMENT ANALYSIS
# ==============================================================================
def run_sentiment_analysis(text_list):
    """
    Performs VADER sentiment analysis on a list of texts.
    Returns a DataFrame with text, scores, and a general label.
    """
    results = []
    
    for text in text_list:
        if not text.strip():
            continue
            
        vs = analyzer.polarity_scores(text)
        
        # Determine the label based on the compound score
        if vs['compound'] >= 0.05:
            label = "Positive"
        elif vs['compound'] <= -0.05:
            label = "Negative"
        else:
            label = "Neutral"
        
        results.append({
            'text': text,
            'negative': vs['neg'],
            'neutral': vs['neu'],
            'positive': vs['pos'],
            'compound': vs['compound'],
            'label': label
        })
        
    return pd.DataFrame(results)