# Contrarian Stock Screener

A comprehensive tool for identifying investment opportunities where market sentiment diverges from fundamentals. Includes a high-performance CLI, a legacy Streamlit dashboard, and a modern Next.js Web UI.

## Installation

1. Clone the repository
2. Install Python dependencies:
```bash
cd contrarian-screener
uv sync
```
3. Install Frontend dependencies:
```bash
cd contrarian-screener/frontend
pnpm install
```

## Usage

### 1. Modern Web UI (Recommended)
The new sleek interface runs on **http://localhost:3345**.

**Step 1: Start the Backend API** (Terminal 1)
```bash
cd contrarian-screener
uv run uvicorn backend.main:app --reload --port 8000
```

**Step 2: Start the Frontend** (Terminal 2)
```bash
cd contrarian-screener/frontend
pnpm dev
```

### 2. CLI Tools
Powerful command-line interface for scripting and quick checks.

**Analyze a Stock**
```bash
uv run python -m contrarian.cli analyze AAPL
```

**Screen the Market**
```bash
# Screen S&P 500
uv run python -m contrarian.cli screen

# Export to CSV
uv run python -m contrarian.cli screen --format csv > results.csv
```

**Watchlist Management**
```bash
uv run python -m contrarian.cli watch add SNAP --note "Wait for earnings"
uv run python -m contrarian.cli watch list
```

### 3. Legacy Dashboard (Streamlit)
Simple python-only dashboard.
```bash
cd contrarian-screener
uv run streamlit run app.py
```

## Configuration
Edit `.env` to add API keys for richer data:
- `REDDIT_CLIENT_ID`
- `REDDIT_CLIENT_SECRET`
- `YAHOO_RAPIDAPI_KEY` (Optional)
- `FINVIZ_API_KEY` (Optional)

## Methodology
The **Contrarian Score (0-100)** is calculated based on:
1. **Sentiment Concentration:** Is the crowd heavily positioned one way? (Analyst ratings, Short Interest, Reddit/StockTwits sentiment).
2. **Fundamental Divergence:** Does the valuation support the sentiment?
   - *Crowded Long* (High Sentiment) + Weak Fundamentals = **Potential Short**
   - *Crowded Short* (Low Sentiment) + Strong Fundamentals = **Potential Long**