import yfinance as yf
from typing import Optional
from contrarian.models.stock import Stock, Financials, Sentiment

class YahooFinanceClient:
    def get_stock_data(self, ticker: str) -> Optional[Stock]:
        try:
            ticker_obj = yf.Ticker(ticker)
            info = ticker_obj.info
            
            # Map Financials
            financials = Financials(
                market_cap=info.get("marketCap"),
                pe_ratio=info.get("trailingPE"),
                pb_ratio=info.get("priceToBook"),
                revenue_growth=info.get("revenueGrowth"),
                profit_margin=info.get("profitMargins"),
                debt_to_equity=info.get("debtToEquity"),
                free_cash_flow=info.get("freeCashflow")
            )
            
            # Map Sentiment (Analyst Data)
            # yfinance often provides recommendationMean or recommendationKey
            # but detailed counts might be in 'recommendations' dataframe or similar.
            # For simplicity, we'll try to use 'numberOfAnalystOpinions' or approximate from 'recommendationKey' if available,
            # but yfinance 'info' dict has limited structured analyst counts. 
            # We will use placeholders or infer from available keys.
            
            # Let's try to get structured recommendation data if possible, otherwise default to 0
            # Note: yfinance `recommendations` property returns a DataFrame history.
            
            # For this MVP, we will rely on 'info' for broad consensus if available, 
            # or skip granular counts if not easily accessible in single call.
            # 'recommendationKey' gives 'buy', 'hold', etc.
            
            rec_key = info.get("recommendationKey", "none")
            buy_count = 0
            hold_count = 0
            sell_count = 0
            
            if rec_key in ["strong_buy", "buy"]:
                buy_count = 10 # Dummy weight to indicate consensus
            elif rec_key == "hold":
                hold_count = 10
            elif rec_key in ["underperform", "sell"]:
                sell_count = 10
                
            sentiment = Sentiment(
                analyst_buy_count=buy_count,
                analyst_hold_count=hold_count,
                analyst_sell_count=sell_count,
                short_interest_pct=info.get("shortPercentOfFloat") # yfinance sometimes has this!
            )

            stock = Stock(
                ticker=ticker.upper(),
                company_name=info.get("longName"),
                price=info.get("currentPrice", info.get("regularMarketPrice", 0.0)),
                sector=info.get("sector"),
                industry=info.get("industry"),
                financials=financials,
                sentiment=sentiment,
                fifty_two_week_high=info.get("fiftyTwoWeekHigh"),
                fifty_two_week_low=info.get("fiftyTwoWeekLow")
            )
            
            return stock
            
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return None
