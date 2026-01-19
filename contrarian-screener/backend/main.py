from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

# Import core logic
# Assumes app is run from the root directory (contrarian-screener)
from contrarian.analysis.pipeline import fetch_and_score, batch_screen
from contrarian.universes.tickers import Universe
from contrarian.config import config

app = FastAPI(title="Contrarian Screener API", version="0.1.0")

# CORS - Allow frontend (localhost:3345)
origins = [
    "http://localhost:3345",
    "http://127.0.0.1:3345",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Helpers ---
def serialize_stock_data(data: dict):
    """Convert dataclasses to dicts for JSON serialization"""
    if not data:
        return None
    
    stock = data["stock"]
    return {
        "ticker": data["ticker"],
        "scores": data["scores"],
        "price": stock.price,
        "company_name": stock.company_name,
        "sector": stock.sector,
        "industry": stock.industry,
        "financials": asdict(stock.financials) if stock.financials else None,
        "sentiment": asdict(stock.sentiment) if stock.sentiment else None,
        "fifty_two_week_high": stock.fifty_two_week_high,
        "fifty_two_week_low": stock.fifty_two_week_low
    }

WATCHLIST_FILE = config.DATA_DIR / "watchlist.json"

def load_watchlist_data():
    if not WATCHLIST_FILE.exists():
        return []
    try:
        with open(WATCHLIST_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_watchlist_data(data):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- Endpoints ---

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Contrarian Screener API is running"}

@app.get("/api/stock/{ticker}")
def get_stock(ticker: str):
    """Analyze a single stock"""
    data = fetch_and_score(ticker.upper())
    if not data:
        raise HTTPException(status_code=404, detail="Stock not found or could not fetch data")
    return serialize_stock_data(data)

@app.get("/api/screen")
def run_screen(universe: str = "sp500", min_score: int = 50, limit: int = 50):
    """Run a screen on a universe"""
    tickers = Universe.get_tickers(universe)
    if not tickers:
        raise HTTPException(status_code=400, detail="Invalid universe")
    
    # In a real app, this should be a background task or cached
    # For MVP, we'll limit the number of tickers to prevent timeouts if needed
    # But batch_screen uses threading, so it's relatively fast
    
    results = batch_screen(tickers, max_workers=10)
    
    # Filter and Sort
    filtered = []
    for res in results:
        if res["scores"]["contrarian_score"] >= min_score:
            filtered.append(serialize_stock_data(res))
            
    # Sort desc by score
    filtered.sort(key=lambda x: x["scores"]["contrarian_score"], reverse=True)
    
    return filtered[:limit]

@app.get("/api/watchlist")
def get_watchlist():
    return load_watchlist_data()

@app.post("/api/watchlist")
def add_to_watchlist(ticker: str, note: str = ""):
    data = load_watchlist_data()
    ticker_upper = ticker.upper()
    
    if any(item["ticker"] == ticker_upper for item in data):
        return {"message": "Already in watchlist"}
    
    data.append({
        "ticker": ticker_upper,
        "note": note,
        "added_at": datetime.now().isoformat()
    })
    save_watchlist_data(data)
    return {"message": "Added", "ticker": ticker_upper}

@app.delete("/api/watchlist/{ticker}")
def remove_from_watchlist(ticker: str):
    data = load_watchlist_data()
    ticker_upper = ticker.upper()
    
    new_data = [item for item in data if item["ticker"] != ticker_upper]
    
    if len(data) == len(new_data):
        raise HTTPException(status_code=404, detail="Ticker not found in watchlist")
        
    save_watchlist_data(new_data)
    return {"message": "Removed", "ticker": ticker_upper}

@app.get("/api/universes")
def get_universes():
    return ["sp500", "nasdaq100", "test"]
