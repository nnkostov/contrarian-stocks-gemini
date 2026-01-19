from contrarian.models.stock import Stock
from contrarian.analysis.sentiment import SentimentAnalyzer
from contrarian.analysis.fundamentals import FundamentalAnalyzer

class ContrarianScorer:
    def __init__(self):
        self.sent_analyzer = SentimentAnalyzer()
        self.fund_analyzer = FundamentalAnalyzer()
        
    def score_stock(self, stock: Stock) -> dict:
        """
        Returns full scoring profile including Contrarian Score.
        """
        # 1. Component Scores
        sentiment_conc = self.sent_analyzer.calculate_concentration_score(stock.sentiment)
        fundamental_score = self.fund_analyzer.calculate_divergence_score(stock)
        
        # 2. Logic for Contrarian Opportunity
        # Opportunity = (Crowd is Wrong)
        # Type A: Crowd Hates it (High Short/Bearish) + Fundamentals Good
        # Type B: Crowd Loves it (High Bullish) + Fundamentals Bad
        
        # Determine Crowd Direction
        # We need to re-derive direction from sentiment analyzer or check raw metrics
        analyst_bullish = stock.sentiment.analyst_consensus_score > 60
        retail_bullish = stock.sentiment.retail_sentiment_score > 60
        is_loved = analyst_bullish and retail_bullish
        
        analyst_bearish = stock.sentiment.analyst_consensus_score < 40
        retail_bearish = stock.sentiment.retail_sentiment_score < 40
        high_short = (stock.sentiment.short_interest_pct or 0) > 15
        is_hated = analyst_bearish or retail_bearish or high_short
        
        contrarian_score = 0.0
        signal_type = "Neutral"
        
        if is_hated:
            # Opportunity if Fundamentals are Strong
            # Score scales with Fundamental Strength
            contrarian_score = fundamental_score
            if fundamental_score > 60:
                signal_type = "Potential Long (Crowded Short)"
        
        elif is_loved:
            # Opportunity if Fundamentals are Weak
            # Score scales with Fundamental Weakness (inverse)
            contrarian_score = 100 - fundamental_score
            if fundamental_score < 40:
                signal_type = "Potential Short (Crowded Long)"
                
        else:
            # Divergence between Sentiment and Fundamentals
            # e.g. Sentiment=20 (Bearish), Fundamentals=80 (Strong) -> Gap=60
            gap = abs(sentiment_conc - fundamental_score) # Rough proxy
            contrarian_score = gap
            signal_type = "Watch"
            
        return {
            "contrarian_score": contrarian_score,
            "fundamental_score": fundamental_score,
            "sentiment_score": sentiment_conc,
            "signal": signal_type,
            "is_hated": is_hated,
            "is_loved": is_loved
        }
