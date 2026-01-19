# Contrarian Stock Screener - Project Status

**Date:** Saturday, January 17, 2026
**Status:** Feature Complete (v0.2.0 - Modern UI)

## 🚀 Project Overview
A comprehensive platform to identify investment opportunities where market sentiment diverges from fundamentals. The tool calculates a "Contrarian Score" by analyzing data from Yahoo Finance, Finviz, Reddit, and StockTwits.

## 🤖 Agent Protocols
**Mandatory Instruction for AI Agent:**
- **Auto-Push:** After completing any major task, refactor, or feature implementation, the Agent **MUST** automatically commit and push the changes to GitHub.
- **Commit Message:** Use clear, descriptive commit messages (e.g., "Feat: Added new sentiment source", "Fix: Resolved API timeout").
- **Command:** Use `./upload.sh "Message"` or standard git commands.
- **Do NOT ask for permission** to push if the changes were requested by the user; just do it to keep the repo in sync.

## ✅ Completed Features

### 1. Data Pipeline
- **Yahoo Finance:** Fetches price, valuation metrics (P/E, P/B), and financial health (Debt/Eq).
- **Finviz:** Scrapes Short Interest % and insider transaction context.
- **Social Sentiment:**
  - **Reddit:** Scrapes mention volume and sentiment from r/wallstreetbets & r/stocks (using PRAW).
  - **StockTwits:** Fetches Bull/Bear message ratios.
- **Caching:** SQLite caching implemented to respect rate limits.

### 2. Analysis Engine
- **Sentiment Concentration Score:** Detects crowded trades (e.g., everyone is bullish).
- **Fundamental Divergence Score:** Scores fundamental strength vs. market perception.
- **Contrarian Score:** Combined metric (0-100) identifying "Crowded Longs" (Potential Shorts) and "Crowded Shorts" (Potential Longs).

### 3. CLI Interfaces (`contrarian.cli`)
- `analyze <TICKER>`: Deep dive into a single stock (supports JSON/MD output).
- `screen --universe <NAME>`: Parallel scanning of S&P 500, Nasdaq 100, etc.
- `watch`: Manage a personal watchlist of stocks.
- `digest`: Generates a daily markdown report of top opportunities.

### 4. Modern Web Interface (New!)
- **Architecture:** Separated Backend (FastAPI) and Frontend (Next.js).
- **Frontend:** Sleek, dark-mode UI built with Tailwind CSS and Shadcn/UI.
- **Backend API:** Robust JSON API serving analysis logic.
- **Features:** Real-time dashboard, interactive screener grid, watchlist management.
- **Port:** Runs on port **3345** (customizable).

### 5. Legacy Interface (Streamlit)
- Simple python-only dashboard for quick prototyping.

## 🛠️ Tech Stack
- **Backend:** Python 3.10+, FastAPI, Uvicorn
- **Frontend:** Next.js 14, React, Tailwind CSS, Shadcn/UI, Recharts
- **CLI:** `typer` + `rich`
- **Data:** `yfinance`, `beautifulsoup4`, `praw`
- **Package Manager:** `uv` (Python), `pnpm` (JS)

## 📋 Next Steps / Roadmap
- [ ] **Authentication:** Add real user auth for the Web UI.
- [ ] **Deployment:** Dockerize the application (frontend + backend containers).
- [ ] **Advanced Data:** Integrate 13F filings (Institutional ownership) and Options Flow.
- [ ] **Backtesting:** Module to test historical performance of the Contrarian Score.

## 📝 Quick Start

### Modern UI
```bash
# Terminal 1: Backend
uv run uvicorn backend.main:app --reload --port 8000

# Terminal 2: Frontend
cd contrarian-screener/frontend
pnpm dev
# Open http://localhost:3345
```

### CLI
```bash
uv run python -m contrarian.cli --help
```
