# Removed gensim imports
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 
import pandas as pd
import logging
import nltk
import re
import collections
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords



# --- NLTK VADER SETUP ---
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')
analyzer = SentimentIntensityAnalyzer()
# --- END VADER SETUP ---

# --- NLTK STOPWORDS SETUP (Required for TF-IDF) ---
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
# --- END STOPWORDS SETUP ---


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


SONG_DATABASE = {
    "Perfect": "A powerful, romantic ballad featuring piano and strings, known for its emotional melody and soft vocals. Excellent for weddings or calm listening.",
    "Bohemian Rhapsody": "A six-minute suite known for its complex structure, operatic sections, and hard rock elements. Features high-energy guitar solos and powerful drums.",
    "Clair de Lune": "A classical piano piece characterized by a gentle, flowing tempo and a highly reflective, dreamlike melody. Often used for relaxation.",
    "Stairway to Heaven": "An iconic rock anthem that starts with slow, acoustic folk elements and gradually builds to a heavy rock crescendo and complex guitar solo.",
    "Shape of You": "A minimalist pop song with dancehall influences, featuring a simple, infectious rhythm and repeated loop structure. Very upbeat and rhythmic.",
    "Hallelujah (Leonard Cohen)": "A poignant folk-rock track with deep, complex lyrics and a slow, haunting melody. Known for its emotional depth and acoustic guitar.",
    "Moonlit Harbor": "Soft piano, gentle strings, peaceful nighttime mood, emotional and slow.",
    "Neon Highway": "Synthwave, retro 80s vibe, driving bassline, nostalgic and energetic.",
    "Crystal Valley": "Fantasy-themed orchestral piece, flutes, light percussion, magical atmosphere.",
    "Shadowstep": "Dark electronic beat, low bass, stealthy and tense, cinematic thriller feel.",
    "Golden Fields": "Warm acoustic guitar, hopeful melody, relaxed countryside vibe.",
    "Rogue Circuit": "Glitch electronics, chopped samples, fast tempo, chaotic cyber feel.",
    "Velvet Lounge": "Smooth jazz trio, soft saxophone, intimate late-night atmosphere.",
    "Arctic Silence": "Minimal ambient pads, cold textures, distant wind sounds, extremely calming.",
    "Night Drive Club": "Deep house, smooth bass, soft vocals, luxury nightlife mood.",
    "Forest Whispers": "Calm ambient nature track, birds, wind, very serene and meditative.",
    "Thunder Forge": "Epic metal orchestration, heavy drums, powerful heroic energy.",
    "Coffee & Rain": "Lo-fi chill beat, warm piano, rainy-day comfort, mellow and cozy.",
    "Galactic Drift": "Space ambient, slow synth sweeps, mysterious and floating.",
    "Retro Roadtrip": "Classic rock vibe, groovy guitar riffs, upbeat and fun driving tune.",
    "Urban Shadows": "Hip-hop beat, dark piano loop, gritty street tone.",
    "Pixel Dreams": "Retro 8-bit melodies, light chiptune tune, nostalgic and cheerful.",
    "Emerald Oasis": "Middle-Eastern inspired strings, hand percussion, exotic and warm.",
    "Winter Cabin Fireplace": "Folk guitar, soft humming, extremely cozy, slow and warm.",
    "Solar Bloom": "Dream pop, airy vocals, shimmering synths, uplifting dreamy mood.",
    "Quantum Echo": "Experimental sci-fi synths, irregular beats, futuristic atmosphere.",
    "Saffron Market": "Indian classical fusion, sitar riffs, tabla rhythm, colorful and lively.",
    "City Sunset": "Chill R&B groove, smooth vocals, relaxing and warm evening vibe.",
    "Iron Runner": "Fast-paced techno, industrial energy, relentless mechanical rhythm.",
    "Butterfly Garden": "Gentle harp, light bells, magical melodic theme.",
    "Storm Riders": "Epic hybrid soundtrack, pounding drums, big cinematic action feel.",
    "Whispering Tides": "Soft ambient waves, slow evolving pads, peaceful shoreline mood.",
    "Lonely Streetlight": "Slow blues guitar, emotional bend notes, late-night sadness.",
    "Jungle Pulse": "Tribal percussion, rhythmic chanting, energetic and primal.",
    "Electric Romance": "Electro-pop, bright synth chords, uplifting chorus, youthful energy.",
    "Dusty Vinyl Memories": "Old-school boom-bap beat, nostalgic sample loops, relaxed and emotional."

}


def find_similar_content(user_query: str, top_n: int = 3):
    """
    Finds songs whose descriptions are most similar to the user's query 
    using TF-IDF Vectorization and Cosine Similarity.
    """
    
    if not user_query or not SONG_DATABASE:
        return []

    
    descriptions = list(SONG_DATABASE.values())
    all_documents = [user_query] + descriptions                   #description
    vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))
    tfidf_matrix = vectorizer.fit_transform(all_documents)
    
    cosine_scores = cosine_similarity(tfidf_matrix[0], tfidf_matrix)        #calculate cosine 
    similarity_scores = cosine_scores.flatten()[1:]
    song_titles = list(SONG_DATABASE.keys())
    indexed_scores = list(zip(song_titles, similarity_scores))
    recommendations = sorted(indexed_scores, key=lambda x: x[1], reverse=True)
    return recommendations[:top_n]


# ==============================================================================
# 3. SENTIMENT ANALYSIS (Existing Code)
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



#Word cloud
def generate_word_cloud_html(text, max_words=30):
    """
    Mocks a word cloud generator using basic HTML/CSS to size words based on frequency.
    Requires text to be cleaned/tokenized.
    """
    if not text:
        return "<p>No text to display for word cloud.</p>"

    tokens = text.split()
    word_counts = collections.Counter(tokens)
    
    # Get the top N words
    most_common = word_counts.most_common(max_words)
    
    if not most_common:
        return "<p>No significant words found after cleaning.</p>"

    # Determine max and min counts for scaling
    max_count = most_common[0][1]
    min_count = most_common[-1][1]
    
    # Simple scaling for font size (from 14px to 48px)
    def scale_size(count):
        if max_count == min_count:
            return 30
        # Linear scaling
        scaled = 14 + (count - min_count) / (max_count - min_count) * (48 - 14)
        return int(scaled)

    # Build the HTML/CSS for the word cloud
    html_parts = []
    
    # Sort words alphabetically for stable display, while keeping size
    sorted_words = sorted([(word, scale_size(count)) for word, count in most_common])

    for word, size in sorted_words:
        # Simple color cycle based on size
        if size > 40:
             color = "#ef4444" # Red
        elif size > 30:
            color = "#3b82f6" # Blue
        elif size > 20:
            color = "#10b981" # Green
        else:
            color = "#4b5563" # Gray
            
        html_parts.append(
            f'<span style="font-size: {size}px; margin: 5px 10px; color: {color}; font-weight: 700;">{word}</span>'
        )

    # The outer div uses flex wrap to arrange the words like a cloud
    cloud_html = f"""
    <div style="display: flex; flex-wrap: wrap; justify-content: center; align-items: center; 
                padding: 20px; border: 1px dashed #ccc; border-radius: 10px; min-height: 250px;">
        {' '.join(html_parts)}
    </div>
    """
    return cloud_html
