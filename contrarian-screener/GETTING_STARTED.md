# Getting Started with Contrarian Screener

Welcome! This guide will take you from zero to running a professional-grade stock analysis terminal on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:
*   **Python 3.10+** (Checking: `python --version`)
*   **Node.js 18+** (Checking: `node --version`)
*   **uv** (Modern Python package manager): `curl -LsSf https://astral.sh/uv/install.sh | sh`
*   **pnpm** (Fast JS package manager): `npm install -g pnpm`

---

## 1. Installation

### Clone the Project
```bash
git clone https://github.com/nkostov/contrarian-stocks-gemini.git
cd contrarian-stocks-gemini/contrarian-screener
```

### Backend Setup (Python)
We use `uv` for lightning-fast Python dependency management.
```bash
# Installs dependencies (FastAPI, Pandas, yfinance, etc.)
uv sync
```

### Frontend Setup (JavaScript)
We use `pnpm` for the Next.js frontend.
```bash
cd frontend
pnpm install
cd ..
```

---

## 2. Running the Application (The "Sleek" UI)

To run the modern web interface, you need to run two processes simultaneously. Open two separate terminal windows.

### Terminal 1: The Brain (Backend API)
This runs the FastAPI server that fetches data and calculates scores.
```bash
cd contrarian-screener
uv run uvicorn backend.main:app --reload --port 8000
```
*You should see: `Uvicorn running on http://127.0.0.1:8000`*

### Terminal 2: The Face (Frontend UI)
This runs the Next.js interface.
```bash
cd contrarian-screener/frontend
pnpm dev
```
*You should see: `Ready in 3345`*

🎉 **Open your browser to:** [http://localhost:3345](http://localhost:3345)

---

## 3. Configuring API Keys (Optional)

The tool works out-of-the-box using free/scraped data. For better reliability and more data sources, configure API keys.

1.  Create a `.env` file in `contrarian-screener/`:
    ```bash
    touch .env
    ```
2.  Add your keys:
    ```env
    # Reddit (for sentiment analysis)
    REDDIT_CLIENT_ID="your_id_here"
    REDDIT_CLIENT_SECRET="your_secret_here"

    # Optional Premium Data
    YAHOO_RAPIDAPI_KEY=""
    FINVIZ_API_KEY=""
    ```
    *Note: To get Reddit keys, go to [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps), create a script app, and copy the ID/Secret.*

---

## 4. Using the CLI Tools

Prefer the command line? You can perform all analysis without the web UI.

**Analyze a Single Stock**
```bash
uv run python -m contrarian.cli analyze TSLA
```

**Screen the Entire S&P 500**
```bash
# This may take a minute as it fetches live data
uv run python -m contrarian.cli screen --universe sp500
```

**Manage Watchlist**
```bash
uv run python -m contrarian.cli watch add NVDA --note "Monitoring for pullback"
uv run python -m contrarian.cli watch list
```

---

## 5. Troubleshooting

**"Port 8000 is already in use"**
*   Kill the existing process: `lsof -ti:8000 | xargs kill -9` (Mac/Linux) or restart your terminal.

**"Connection Error" in Frontend**
*   Ensure the backend (Terminal 1) is running and hasn't crashed.
*   Check if you can visit `http://localhost:8000/api/universes` in your browser.

**"Rate Limited" or Empty Data**
*   You might be hitting Yahoo Finance rate limits. Wait a few minutes or add a Proxy/API key in `.env`.

---

## 6. What's Next?
*   **Explore:** Click into a stock card on the dashboard to see the Deep Dive view.
*   **Customize:** Edit `contrarian/analysis/scoring.py` to tweak how the Contrarian Score is calculated.
*   **Extend:** Add new data sources in `contrarian/data/`.
