from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, Dict, List
from contrarian.data.yahoo import YahooFinanceClient
from contrarian.data.finviz import FinvizClient
from contrarian.data.reddit import RedditClient
from contrarian.data.stocktwits import StockTwitsClient
from contrarian.analysis.sentiment import SentimentAnalyzer
from contrarian.analysis.scoring import ContrarianScorer
from contrarian.models.stock import Stock

def fetch_and_score(ticker: str) -> Optional[Dict]:
    """
    Fetches all data and scores a single ticker.
    Returns a dict with 'ticker', 'stock', and 'scores' keys.
    """
    try:
        # 1. Fetch Data
        yahoo = YahooFinanceClient()
        stock = yahoo.get_stock_data(ticker)
        if not stock: return None
        
        # 2. Add Sentiment
        finviz = FinvizClient()
        short_int = finviz.get_short_interest(ticker)
        if stock.sentiment and short_int:
            stock.sentiment.short_interest_pct = short_int
            
        # Social logic (Optional/Graceful degradation)
        # In a real heavy-load scenario, we might toggle this off for bulk screening
        try:
            # Reddit
            reddit_client = RedditClient()
            r_data = reddit_client.get_sentiment(ticker)
            if stock.sentiment:
                stock.sentiment.reddit_mentions = r_data["mentions"]
                stock.sentiment.reddit_sentiment_score = r_data["sentiment_score"]
                
            # StockTwits
            st_client = StockTwitsClient()
            st_data = st_client.get_sentiment(ticker)
            if stock.sentiment:
                stock.sentiment.stocktwits_bull_ratio = st_data["bull_ratio"]
        except Exception:
            pass # Continue if social fails
        
        # 3. Score
        scorer = ContrarianScorer()
        scores = scorer.score_stock(stock)
        
        return {
            "ticker": ticker,
            "stock": stock,
            "scores": scores
        }
    except Exception as e:
        return None

def batch_screen(tickers: List[str], max_workers: int = 10) -> List[Dict]:
    """
    Screens a list of tickers in parallel.
    """
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_and_score, t): t for t in tickers}
        for future in as_completed(futures):
            data = future.result()
            if data:
                results.append(data)
    return results
