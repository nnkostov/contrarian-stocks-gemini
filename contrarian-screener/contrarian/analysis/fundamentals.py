from contrarian.models.stock import Stock

class FundamentalAnalyzer:
    def calculate_divergence_score(self, stock: Stock) -> float:
        """
        Calculates Fundamental Divergence Score (0-100).
        High Score = Strong Fundamentals but potentially hated OR Weak Fundamentals but loved.
        
        For this MVP, we score "Fundamental Strength" (0-100) first.
        """
        if not stock.financials:
            return 50.0
            
        f = stock.financials
        score = 50.0
        
        # 1. Valuation (P/E) - Lower is better (usually)
        # Simple relative valuation vs generic market average of 20
        pe = f.pe_ratio or 25.0
        if pe < 15: score += 10
        elif pe > 35: score -= 10
        
        # 2. Growth (Revenue) - Higher is better
        rev_growth = f.revenue_growth or 0.0
        if rev_growth > 0.10: score += 10
        elif rev_growth < 0: score -= 10
        
        # 3. Profitability (Margins)
        margin = f.profit_margin or 0.0
        if margin > 0.15: score += 10
        elif margin < 0: score -= 10
        
        # 4. Financial Health (Debt/Equity)
        de = f.debt_to_equity or 100.0 # High default
        if de < 50: score += 10 # Low debt
        elif de > 150: score -= 10 # High debt
        
        # 5. Price Momentum (vs 52w High) - "Beaten down" factor
        # If stock is far from high, it might be fundamentally undervalued if other metrics are good
        pct_from_high = stock.percent_from_high or 0.0
        if pct_from_high < -30: score += 5 # Deep value potential
        
        return max(0, min(100, score))

    def get_fundamental_rating(self, score: float) -> str:
        if score >= 70: return "Strong"
        if score >= 40: return "Neutral"
        return "Weak"
