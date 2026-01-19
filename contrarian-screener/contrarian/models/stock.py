from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class Financials:
    market_cap: Optional[int] = None
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    revenue_growth: Optional[float] = None
    profit_margin: Optional[float] = None
    debt_to_equity: Optional[float] = None
    free_cash_flow: Optional[int] = None

@dataclass
class Sentiment:
    analyst_buy_count: int = 0
    analyst_sell_count: int = 0
    analyst_hold_count: int = 0
    short_interest_pct: Optional[float] = None
    insider_buy_pct: Optional[float] = None
    
    # New Social Fields
    reddit_mentions: int = 0
    reddit_sentiment_score: float = 0.5  # 0.0 (Bear) - 1.0 (Bull)
    stocktwits_bull_ratio: float = 0.5   # 0.0 (Bear) - 1.0 (Bull)
    
    @property
    def analyst_consensus_score(self) -> float:
        """Returns a score from 0 (All Sell) to 100 (All Buy)."""
        total = self.analyst_buy_count + self.analyst_sell_count + self.analyst_hold_count
        if total == 0:
            return 50.0
        # Simple weighted score: Buy=1, Hold=0.5, Sell=0
        score = (self.analyst_buy_count * 1.0 + self.analyst_hold_count * 0.5) / total
        return score * 100
    
    @property
    def retail_sentiment_score(self) -> float:
        """Combined retail sentiment 0-100"""
        # Average of Reddit and StockTwits
        return ((self.reddit_sentiment_score + self.stocktwits_bull_ratio) / 2) * 100


@dataclass
class Stock:
    ticker: str
    price: float
    company_name: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    financials: Optional[Financials] = None
    sentiment: Optional[Sentiment] = None
    
    # 52-week data
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None
    
    @property
    def percent_from_high(self) -> Optional[float]:
        if self.price and self.fifty_two_week_high:
            return ((self.price - self.fifty_two_week_high) / self.fifty_two_week_high) * 100
        return None
