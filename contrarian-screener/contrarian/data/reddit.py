from typing import List, Dict, Optional
import praw
from praw.models import Submission
from collections import Counter
from datetime import datetime, timedelta
from contrarian.config import config

class RedditClient:
    def __init__(self):
        if config.REDDIT_CLIENT_ID and config.REDDIT_CLIENT_SECRET:
            self.reddit = praw.Reddit(
                client_id=config.REDDIT_CLIENT_ID,
                client_secret=config.REDDIT_CLIENT_SECRET,
                user_agent="ContrarianScreener/1.0"
            )
            self.enabled = True
        else:
            print("Warning: Reddit credentials not found. Reddit analysis disabled.")
            self.enabled = False

    def get_sentiment(self, ticker: str, limit: int = 100) -> Dict[str, any]:
        """
        Analyzes recent posts in r/wallstreetbets and r/stocks for a given ticker.
        Returns mention count and simplified sentiment (based on keywords).
        """
        if not self.enabled:
            return {"mentions": 0, "sentiment_score": 0.5, "sample_size": 0}

        subreddits = ["wallstreetbets", "stocks", "investing"]
        mentions = 0
        bullish_keywords = ["call", "moon", "buy", "long", "bull", "gain", "rocket"]
        bearish_keywords = ["put", "drill", "sell", "short", "bear", "loss", "tank"]
        
        bull_score = 0
        bear_score = 0
        
        # Determine strict search query to avoid false positives (e.g. "ALL" matching "all")
        # For common tickers like $AAPL, search "AAPL" or "$AAPL"
        query = f"{ticker} OR ${ticker}"
        
        try:
            for sub_name in subreddits:
                subreddit = self.reddit.subreddit(sub_name)
                # Search last week
                for submission in subreddit.search(query, sort="new", time_filter="week", limit=limit):
                    mentions += 1
                    text = (submission.title + " " + submission.selftext).lower()
                    
                    bull_count = sum(text.count(w) for w in bullish_keywords)
                    bear_count = sum(text.count(w) for w in bearish_keywords)
                    
                    bull_score += bull_count
                    bear_score += bear_count
            
            total_score = bull_score + bear_score
            sentiment_ratio = 0.5 # Neutral default
            
            if total_score > 0:
                sentiment_ratio = bull_score / total_score
                
            return {
                "mentions": mentions,
                "sentiment_score": sentiment_ratio, # 0.0 (Bearish) to 1.0 (Bullish)
                "sample_size": mentions
            }

        except Exception as e:
            print(f"Error fetching Reddit data: {e}")
            return {"mentions": 0, "sentiment_score": 0.5, "sample_size": 0}
