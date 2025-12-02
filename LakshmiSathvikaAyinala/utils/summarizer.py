import re
import nltk
from collections import Counter
import heapq
from nltk.tokenize import sent_tokenize, word_tokenize

# Download NLTK data once
try:
    nltk.data.find('punkt')
except:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)

class SmartSummarizer:
    """Fast and intelligent summarization using extractive methods"""
    
    @staticmethod
    def summarize(text: str, use_ai: bool = False) -> str:
        """
        Generate meaningful summary from text
        Args:
            text: Input text to summarize
            use_ai: Whether to try AI summarization (slower)
        Returns:
            str: Generated summary
        """
        if not text or len(text.strip()) < 50:
            return text if text else "Text is too short for summarization."
        
        # Clean text
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Generate summary based on preference
        if use_ai:
            summary = SmartSummarizer._ai_summary(text)
        else:
            summary = SmartSummarizer._extractive_summary(text)
        
        return summary
    
    @staticmethod
    def _extractive_summary(text: str) -> str:
        """Fast extractive summary using intelligent sentence selection"""
        sentences = sent_tokenize(text)
        
        if len(sentences) <= 3:
            return ' '.join(sentences)
        
        # Calculate how many sentences we need
        num_sentences = SmartSummarizer._get_optimal_sentence_count(len(sentences))
        
        # Get important sentences
        important_indices = SmartSummarizer._get_important_sentence_indices(text, sentences, num_sentences)
        
        # Order them intelligently
        ordered_indices = SmartSummarizer._order_sentences_intelligently(important_indices, len(sentences))
        
        # Build summary
        summary_sentences = [sentences[i] for i in ordered_indices if i < len(sentences)]
        summary = ' '.join(summary_sentences)
        
        # Clean up
        summary = SmartSummarizer._clean_summary(summary)
        return summary
    
    @staticmethod
    def _get_optimal_sentence_count(total_sentences: int) -> int:
        """Calculate optimal number of sentences for summary"""
        if total_sentences <= 5:
            return max(1, total_sentences - 1)
        elif total_sentences <= 15:
            return max(3, int(total_sentences * 0.3))
        elif total_sentences <= 30:
            return max(5, int(total_sentences * 0.2))
        else:
            return max(8, int(total_sentences * 0.15))
    
    @staticmethod
    def _get_important_sentence_indices(text: str, sentences: list, target_count: int) -> list:
        """Find the most important sentences using multiple criteria"""
        
        # 1. Word frequency analysis
        stop_words = set(nltk.corpus.stopwords.words('english'))
        words = [w.lower() for w in word_tokenize(text) if w.isalnum() and w.lower() not in stop_words]
        word_freq = Counter(words)
        
        # 2. Score each sentence
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            sentence_words = [w.lower() for w in word_tokenize(sentence) if w.isalnum()]
            
            if not sentence_words:
                continue
            
            # Frequency score
            freq_score = sum(word_freq.get(word, 0) for word in sentence_words) / len(sentence_words)
            
            # Position score (first and last sentences are often important)
            if i == 0:  # First sentence
                pos_score = 1.5
            elif i == len(sentences) - 1:  # Last sentence
                pos_score = 1.3
            elif i < 3:  # Early sentences
                pos_score = 1.2
            else:
                pos_score = 1.0
            
            # Length score (prefer medium-length sentences)
            word_count = len(sentence_words)
            if word_count < 8:
                len_score = 0.7
            elif word_count > 40:
                len_score = 0.8
            else:
                len_score = 1.0
            
            # Combined score
            combined_score = freq_score * pos_score * len_score
            sentence_scores[i] = combined_score
        
        # Get top sentences
        top_count = min(target_count * 2, len(sentences))
        top_indices = heapq.nlargest(top_count, sentence_scores, key=sentence_scores.get)
        return sorted(top_indices)
    
    @staticmethod
    def _order_sentences_intelligently(important_indices: list, total_sentences: int) -> list:
        """Order sentences to maintain coherence"""
        # Keep some chronological order but prioritize importance
        if len(important_indices) <= 5:
            return sorted(important_indices)
        
        # Take first half in order, second half selected for diversity
        half = len(important_indices) // 2
        ordered = sorted(important_indices[:half])
        
        # Add some from later in the document
        remaining = [i for i in important_indices[half:] if i not in ordered]
        if remaining:
            # Take every other to maintain diversity
            ordered.extend(remaining[::2])
        
        return sorted(ordered)
    
    @staticmethod
    def _clean_summary(summary: str) -> str:
        """Clean up summary for better readability"""
        # Fix spacing around punctuation
        summary = re.sub(r'\s+([.,!?])', r'\1', summary)
        summary = re.sub(r'([.,!?])([A-Z])', r'\1 \2', summary)
        
        # Ensure proper ending
        if not summary.endswith(('.', '!', '?')):
            summary = summary.rstrip() + '.'
        
        return summary
    
    @staticmethod
    def _ai_summary(text: str) -> str:
        """AI-powered summarization (optional, can be slow)"""
        # This is kept as a placeholder for future AI integration
        # For now, it falls back to extractive
        return SmartSummarizer._extractive_summary(text)
    
    @staticmethod
    def get_summary_stats(original: str, summary: str) -> dict:
        """Get statistics about the summarization"""
        orig_words = len(original.split())
        summ_words = len(summary.split())
        
        return {
            'original_words': orig_words,
            'summary_words': summ_words,
            'compression_ratio': (summ_words / orig_words * 100) if orig_words > 0 else 0,
            'reading_time_original': f"{orig_words/200:.1f} min",
            'reading_time_summary': f"{summ_words/200:.1f} min"
        }