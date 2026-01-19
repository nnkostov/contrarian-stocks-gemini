from contrarian.models.stock import Sentiment

class SentimentAnalyzer:
    def calculate_concentration_score(self, sentiment: Sentiment) -> float:
        """
        Calculates the Sentiment Concentration Score (0-100).
        High Score = Very Crowded (Everyone thinks the same thing).
        Low Score = Divergent/Confused Views.
        
        Logic:
        - If everyone is Bullish (Analysts + Retail), Score -> 100
        - If everyone is Bearish (Analysts + Retail + High Short Interest), Score -> 100
        - If mixed, Score -> 0
        """
        
        # Normalize inputs to 0-1 scale
        analyst_bullishness = sentiment.analyst_consensus_score / 100.0
        retail_bullishness = sentiment.retail_sentiment_score / 100.0
        
        # Short interest factor:
        # High short interest implies strong bearish consensus
        # Cap at 20% for max effect
        short_interest_norm = min((sentiment.short_interest_pct or 0) / 20.0, 1.0)
        
        # Calculate Crowded Long Score (Everyone buying)
        # Analysts Buy + Retail Bullish + Low Short Interest
        crowded_long = (analyst_bullishness * 0.5) + (retail_bullishness * 0.4) + ((1 - short_interest_norm) * 0.1)
        
        # Calculate Crowded Short Score (Everyone selling)
        # Analysts Sell + Retail Bearish + High Short Interest
        analyst_bearishness = 1.0 - analyst_bullishness
        retail_bearishness = 1.0 - retail_bullishness
        crowded_short = (analyst_bearishness * 0.4) + (retail_bearishness * 0.3) + (short_interest_norm * 0.3)
        
        # The concentration score is the maximum of either extreme
        concentration = max(crowded_long, crowded_short) * 100
        
        return concentration

    def get_signal_description(self, sentiment: Sentiment) -> str:
        score = self.calculate_concentration_score(sentiment)
        analyst = sentiment.analyst_consensus_score
        retail = sentiment.retail_sentiment_score
        
        if score < 40:
            return "Mixed / Uncertainty (No clear crowd)"
            
        # Determine direction
        is_bullish_crowd = (analyst > 60 and retail > 60)
        is_bearish_crowd = (analyst < 40 and retail < 40) or ((sentiment.short_interest_pct or 0) > 15)
        
        if is_bullish_crowd:
            return f"Crowded Long (Consensus Bullish) - Score: {score:.0f}"
        elif is_bearish_crowd:
            return f"Crowded Short (Consensus Bearish) - Score: {score:.0f}"
        else:
            return f"High Conviction Divergence - Score: {score:.0f}"
