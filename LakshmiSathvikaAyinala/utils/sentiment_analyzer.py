import plotly.graph_objects as go
import plotly.express as px
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download NLTK data once
try:
    nltk.data.find('vader_lexicon')
except:
    nltk.download('vader_lexicon', quiet=True)

class SentimentAnalyzer:
    """Analyze sentiment with attractive bar graph"""
    
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
    
    def analyze(self, text: str) -> dict:
        """Analyze text sentiment - FIXED LOGIC"""
        scores = self.analyzer.polarity_scores(text)
        
        # FIXED: Correct sentiment determination
        if scores['pos'] > scores['neg'] and scores['pos'] > scores['neu']:
            sentiment = 'Positive'
            color = '#87CEEB'
        elif scores['neg'] > scores['pos'] and scores['neg'] > scores['neu']:
            sentiment = 'Negative'
            color = '#9370DB'
        else:
            sentiment = 'Neutral'
            color = '#A0A0A0'
        
        return {
            'sentiment': sentiment,
            'color': color,
            'scores': scores,
            'confidence': max(scores['pos'], scores['neg'], scores['neu']) * 100
        }
    
    def create_sentiment_barchart(self, sentiment_data: dict, height: int = 400):
        """Create attractive sentiment bar chart with outlines"""
        scores = sentiment_data['scores']
        
        # Prepare data
        categories = ['Positive', 'Neutral', 'Negative']
        values = [scores['pos'] * 100, scores['neu'] * 100, scores['neg'] * 100]
        
        # Attractive colors with matching outlines
        bar_colors = ['#87CEEB', '#A0A0A0', '#9370DB']
        outline_colors = ['#5F9EA0', '#708090', '#6A5ACD']
        
        # Create bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            marker_color=bar_colors,
            marker_line_color=outline_colors,
            marker_line_width=3,
            text=[f'{val:.1f}%' for val in values],
            textposition='outside',
            textfont=dict(size=16, color='white'),
            hovertemplate='<b>%{x}</b><br>%{y:.1f}%<extra></extra>',
            width=0.6  # Bar width
        ))
        
        # Update layout for attractiveness
        fig.update_layout(
            title=dict(
                text='Sentiment Analysis',
                font=dict(size=24, color='white', family='Arial'),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                title='Sentiment Categories',
                title_font=dict(size=16, color='white'),
                tickfont=dict(size=14, color='white'),
                showgrid=False
            ),
            yaxis=dict(
                title='Percentage (%)',
                title_font=dict(size=16, color='white'),
                tickfont=dict(size=14, color='white'),
                range=[0, 100],
                gridcolor='rgba(255, 255, 255, 0.1)',
                gridwidth=1
            ),
            height=height,
            margin=dict(l=50, r=50, t=80, b=50),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            bargap=0.3  # Gap between bars
        )
        
        # Add custom grid
        fig.update_xaxes(showline=True, linewidth=1, linecolor='rgba(255, 255, 255, 0.2)')
        fig.update_yaxes(showline=True, linewidth=1, linecolor='rgba(255, 255, 255, 0.2)')
        
        return fig