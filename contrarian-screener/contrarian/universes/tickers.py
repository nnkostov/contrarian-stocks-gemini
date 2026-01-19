from typing import List

class Universe:
    @staticmethod
    def get_tickers(universe_name: str) -> List[str]:
        universe_name = universe_name.lower()
        if universe_name == "sp500":
            return Universe.sp500()
        elif universe_name == "nasdaq100":
            return Universe.nasdaq100()
        elif universe_name == "test":
            return ["AAPL", "TSLA", "GME", "AMC", "MSFT", "NVDA", "GOOGL", "AMD", "PLTR", "COIN"]
        else:
            return []

    @staticmethod
    def sp500() -> List[str]:
        # For this MVP, we return a top 20 subset to respect rate limits and speed
        # In a real app, we would fetch the full list from Wikipedia or Slickcharts
        return [
            "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "BRK.B", "LLY", "V",
            "TSM", "AVGO", "NVO", "JPM", "WMT", "XOM", "MA", "UNH", "PG", "JNJ"
        ]

    @staticmethod
    def nasdaq100() -> List[str]:
        # Top 15 Nasdaq
        return [
            "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "AVGO", "ASML", "COST",
            "PEP", "CSCO", "NFLX", "AMD", "INTC"
        ]
