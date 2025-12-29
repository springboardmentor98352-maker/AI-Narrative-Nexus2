import re
import string

STOP_WORDS = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
              'of', 'with', 'is', 'was', 'are', 'were', 'been', 'be', 'have', 'has',
              'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may',
              'might', 'must', 'can', 'this', 'that', 'these', 'those'}

def process_text(text):
    """Apply all preprocessing steps to text"""
    text = clean_text(text)
    text = remove_stopwords(text)
    return text

def clean_text(text):
    """Remove punctuation, numbers and extra spaces"""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\d+', '', text)
    return ' '.join(text.split())

def remove_stopwords(text):
    words = text.split()
    filtered_words = [word for word in words if word not in STOP_WORDS]
    return ' '.join(filtered_words)

def get_stats(original, cleaned):
    return {
        'original_words': len(original.split()),
        'original_chars': len(original),
        'cleaned_words': len(cleaned.split()),
        'cleaned_chars': len(cleaned)
    }