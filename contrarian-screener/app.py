import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from contrarian.universes.tickers import Universe
from contrarian.analysis.pipeline import batch_screen, fetch_and_score
from contrarian.config import config
import json

# Page Config
st.set_page_config(
    page_title="Contrarian Screener",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
st.sidebar.title("🦅 Contrarian")
page = st.sidebar.radio("Navigation", ["Scanner", "Deep Dive", "Watchlist"])

# Helper: Gauge Chart
def create_gauge(score, title):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        title = {'text': title},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 40], 'color': "lightgray"},
                {'range': [40, 70], 'color': "gray"},
                {'range': [70, 100], 'color': "lightblue"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 80
            }
        }
    ))
    fig.update_layout(height=250, margin=dict(l=10, r=10, t=30, b=10))
    return fig

# --- Page: Scanner ---
if page == "Scanner":
    st.title("🔎 Market Scanner")
    st.markdown("Find opportunities where **sentiment diverges from fundamentals**.")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        universe = st.selectbox("Universe", ["sp500", "nasdaq100", "test"], index=0)
    with col2:
        min_score = st.slider("Minimum Score", 0, 100, 50)
        
    if st.button("Run Screen", type="primary"):
        tickers = Universe.get_tickers(universe)
        
        with st.spinner(f"Scanning {len(tickers)} stocks..."):
            results = batch_screen(tickers)
            
        if not results:
            st.warning("No stocks found or error fetching data.")
        else:
            # Process for Display
            rows = []
            for r in results:
                s = r["stock"]
                sc = r["scores"]
                if sc["contrarian_score"] >= min_score:
                    rows.append({
                        "Ticker": s.ticker,
                        "Price": f"${s.price:.2f}",
                        "Score": f"{sc['contrarian_score']:.1f}",
                        "Signal": sc["signal"],
                        "Fund. Score": f"{sc['fundamental_score']:.1f}",
                        "Sent. Score": f"{sc['sentiment_score']:.1f}",
                        "Sector": s.sector
                    })
            
            df = pd.DataFrame(rows)
            if not df.empty:
                # Sort by Score descending
                df["SortKey"] = df["Score"].astype(float)
                df = df.sort_values("SortKey", ascending=False).drop(columns=["SortKey"])
                
                st.success(f"Found {len(df)} opportunities!")
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No stocks met the minimum score criteria.")

# --- Page: Deep Dive ---
elif page == "Deep Dive":
    st.title("🔬 Deep Dive Analysis")
    
    ticker_input = st.text_input("Enter Ticker", value="AAPL").upper()
    
    if st.button("Analyze", type="primary") or ticker_input:
        if ticker_input:
            with st.spinner(f"Analyzing {ticker_input}..."):
                data = fetch_and_score(ticker_input)
                
            if not data:
                st.error(f"Could not fetch data for {ticker_input}")
            else:
                stock = data["stock"]
                scores = data["scores"]
                
                # Header
                st.header(f"{stock.company_name} ({stock.ticker})")
                st.subheader(f"${stock.price:,.2f} | {scores['signal']}")
                
                # Scores Row
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.plotly_chart(create_gauge(scores['contrarian_score'], "Contrarian Score"), use_container_width=True)
                with c2:
                    st.metric("Fundamental Score", f"{scores['fundamental_score']:.1f}")
                    st.metric("Sentiment Score", f"{scores['sentiment_score']:.1f}")
                with c3:
                    st.info(f"Sector: {stock.sector}\n\nIndustry: {stock.industry}")

                # Fundamentals & Sentiment Columns
                col_fund, col_sent = st.columns(2)
                
                with col_fund:
                    st.subheader("Fundamentals")
                    if stock.financials:
                        f = stock.financials
                        metrics = {
                            "Market Cap": f"${f.market_cap:,.0f}" if f.market_cap else "-",
                            "P/E Ratio": f"{f.pe_ratio:.2f}" if f.pe_ratio else "-",
                            "P/B Ratio": f"{f.pb_ratio:.2f}" if f.pb_ratio else "-",
                            "Rev Growth": f"{f.revenue_growth:.1%}" if f.revenue_growth else "-",
                            "Profit Margin": f"{f.profit_margin:.1%}" if f.profit_margin else "-",
                            "Debt/Equity": f"{f.debt_to_equity:.2f}" if f.debt_to_equity else "-"
                        }
                        st.table(pd.DataFrame(metrics.items(), columns=["Metric", "Value"]))
                
                with col_sent:
                    st.subheader("Sentiment")
                    if stock.sentiment:
                        s = stock.sentiment
                        metrics = {
                            "Short Interest": f"{s.short_interest_pct:.2f}%" if s.short_interest_pct else "-",
                            "Analyst Consensus": f"{s.analyst_consensus_score:.0f}/100",
                            "Reddit Mentions": str(s.reddit_mentions),
                            "Reddit Sentiment": f"{s.reddit_sentiment_score:.0%} Bull",
                            "StockTwits": f"{s.stocktwits_bull_ratio:.0%} Bull"
                        }
                        st.table(pd.DataFrame(metrics.items(), columns=["Metric", "Value"]))

# --- Page: Watchlist ---
elif page == "Watchlist":
    st.title("👀 Watchlist")
    
    WATCHLIST_FILE = config.DATA_DIR / "watchlist.json"
    
    def load_watchlist():
        if not WATCHLIST_FILE.exists():
            return []
        with open(WATCHLIST_FILE, "r") as f:
            return json.load(f)

    data = load_watchlist()
    
    if not data:
        st.info("Watchlist is empty. Add stocks via CLI for now.")
    else:
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.caption("Note: Watchlist editing is currently CLI-only (uv run python -m contrarian.cli watch).")
