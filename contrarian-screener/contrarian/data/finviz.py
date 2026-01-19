import httpx
from bs4 import BeautifulSoup
from typing import Dict, Optional

class FinvizClient:
    BASE_URL = "https://finviz.com/quote.ashx"
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    def get_data(self, ticker: str) -> Dict[str, str]:
        """
        Scrapes basic data table from Finviz for a given ticker.
        Returns a dictionary of Key: Value strings.
        """
        try:
            with httpx.Client(headers=self.headers, follow_redirects=True) as client:
                response = client.get(self.BASE_URL, params={"t": ticker})
                response.raise_for_status()
                
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Finviz data is usually in a table with class 'snapshot-table2'
            table = soup.find("table", class_="snapshot-table2")
            if not table:
                return {}
            
            data = {}
            rows = table.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                # Structure is Key | Value | Key | Value ...
                for i in range(0, len(cols), 2):
                    key = cols[i].text.strip()
                    value = cols[i+1].text.strip()
                    data[key] = value
            
            return data
            
        except Exception as e:
            print(f"Error scraping Finviz for {ticker}: {e}")
            return {}

    def parse_float(self, value_str: str) -> Optional[float]:
        if not value_str or value_str == "-":
            return None
        try:
            value_str = value_str.strip('%')
            return float(value_str)
        except ValueError:
            return None

    def get_short_interest(self, ticker: str) -> Optional[float]:
        data = self.get_data(ticker)
        # Key is usually 'Short Float'
        return self.parse_float(data.get("Short Float"))
