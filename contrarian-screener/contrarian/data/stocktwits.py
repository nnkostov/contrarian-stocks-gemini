import httpx
from typing import Dict, Optional

class StockTwitsClient:
    BASE_URL = "https://api.stocktwits.com/api/2/streams/symbol/{}.json"
    
    def get_sentiment(self, ticker: str) -> Dict[str, any]:
        """
        Fetches basic sentiment data from StockTwits public API.
        Note: The public stream API mainly gives messages. 
        Detailed sentiment (Bull/Bear ratio) is often inferred or requires premium access/scraping.
        For this MVP, we will infer sentiment from the 'sentiment' field in recent messages if available.
        """
        url = self.BASE_URL.format(ticker)
        try:
            with httpx.Client() as client:
                response = client.get(url)
                if response.status_code == 404:
                    return {"bull_ratio": 0.5, "message_vol": 0}
                response.raise_for_status()
                data = response.json()
                
            messages = data.get("messages", [])
            bulls = 0
            bears = 0
            
            for msg in messages:
                entities = msg.get("entities", {})
                sentiment = entities.get("sentiment", {})
                if sentiment:
                    basic = sentiment.get("basic")
                    if basic == "Bullish":
                        bulls += 1
                    elif basic == "Bearish":
                        bears += 1
            
            total = bulls + bears
            ratio = 0.5 # Neutral
            if total > 0:
                ratio = bulls / total
                
            return {
                "bull_ratio": ratio, # 0.0 to 1.0
                "message_vol": len(messages),
                "labeled_count": total
            }
            
        except Exception as e:
            # Silent fail for now as rate limits are strict
            # print(f"Error fetching StockTwits: {e}") 
            return {"bull_ratio": 0.5, "message_vol": 0}
