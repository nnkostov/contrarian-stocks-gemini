# Contrarian Stock Screener — Claude Code Build Plan

## Project Overview

Build a CLI-based contrarian stock screener that identifies investment opportunities where market sentiment diverges from fundamentals. The tool should surface stocks where consensus is strongly positioned one way, but underlying data suggests a potential mispricing.

**Core Thesis**: Markets often overshoot on both optimism and pessimism. This tool finds where the crowd is most concentrated and flags potential opportunities to bet against consensus.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTRARIAN SCREENER                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Data       │  │  Sentiment   │  │  Fundamental │       │
│  │   Ingestion  │  │  Analysis    │  │  Analysis    │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                 │                 │                │
│         └────────────┬────┴────────────────┘                │
│                      ▼                                       │
│              ┌───────────────┐                               │
│              │  Divergence   │                               │
│              │  Scoring      │                               │
│              └───────┬───────┘                               │
│                      ▼                                       │
│              ┌───────────────┐                               │
│              │  Output &     │                               │
│              │  Alerts       │                               │
│              └───────────────┘                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Sources (Free/Freemium Tier Focus)

### Sentiment Data
| Source | Data | Access |
|--------|------|--------|
| **Yahoo Finance** | Analyst ratings, price targets, recommendations | `yfinance` library OR RapidAPI (with key) |
| **Finviz** | Short interest, analyst consensus, insider transactions | Scraping (free) OR Elite API (with key) |
| **Reddit (r/wallstreetbets, r/stocks)** | Retail sentiment, mention frequency | Reddit API (PRAW) |
| **StockTwits** | Real-time retail sentiment, bull/bear ratios | Public API |
| **Fear & Greed Index** | Market-wide sentiment | CNN API/scrape |
| **AAII Sentiment Survey** | Institutional/retail positioning | Weekly data |

### Fundamental Data
| Source | Data | Access |
|--------|------|--------|
| **Yahoo Finance** | P/E, P/B, revenue growth, margins, debt ratios | `yfinance` library OR RapidAPI (with key) |
| **SEC EDGAR** | Insider transactions, 13F filings | SEC API |
| **Financial Modeling Prep** | Historical financials, DCF estimates | Free tier API |

### Price/Technical Data
| Source | Data | Access |
|--------|------|--------|
| **Yahoo Finance** | Price history, volume, 52-week range | `yfinance` library OR RapidAPI (with key) |
| **Alpha Vantage** | Technical indicators | Free API key |

---

## API Key Strategy

The tool uses a **"best available" approach** — it will use premium APIs when keys are provided, otherwise fall back to free methods.

| Service | Free Method | Premium Method | Benefits of Premium |
|---------|-------------|----------------|---------------------|
| **Yahoo Finance** | `yfinance` library | RapidAPI Yahoo Finance | Higher rate limits, more reliable |
| **Finviz** | Web scraping | Finviz Elite API | No scraping blocks, faster, more data |

### Getting API Keys (Optional)

**Yahoo Finance via RapidAPI:**
1. Go to https://rapidapi.com/apidojo/api/yahoo-finance1
2. Subscribe to free tier (500 requests/month) or paid
3. Copy your RapidAPI key

**Finviz Elite:**
1. Subscribe at https://finviz.com/elite.ashx (~$25/month)
2. Go to https://finviz.com/api.ashx after subscribing
3. Copy your API key

Both are optional — the tool works fine without them, just with more conservative rate limiting.

---

## Contrarian Scoring Methodology

### 1. Sentiment Concentration Score (0-100)
Measures how "crowded" the consensus is:

```python
# Inputs
analyst_buy_pct      # % of analysts with Buy/Strong Buy
analyst_sell_pct     # % of analysts with Sell/Strong Sell  
short_interest_pct   # Short interest as % of float
retail_sentiment     # Bull/bear ratio from StockTwits/Reddit
insider_activity     # Net insider buying/selling

# Scoring Logic
if analyst_buy_pct > 80:
    crowded_long = True
    concentration_score = analyst_buy_pct
elif analyst_sell_pct > 50 or short_interest > 20:
    crowded_short = True  
    concentration_score = max(analyst_sell_pct, short_interest * 2)
```

### 2. Fundamental Divergence Score (0-100)
Measures gap between sentiment and fundamentals:

```python
# For crowded longs (everyone loves it):
# Look for warning signs
- Slowing revenue growth vs. peers
- Margin compression
- Rising debt levels
- Insider selling
- Valuation stretched vs. history

# For crowded shorts (everyone hates it):
# Look for hidden strength  
- Stabilizing/improving margins
- Insider buying
- Cash flow positive
- Valuation at historical lows
- Catalyst potential (new product, management, etc.)
```

### 3. Contrarian Opportunity Score (Combined)
```python
contrarian_score = (
    sentiment_concentration * 0.4 +
    fundamental_divergence * 0.4 +
    technical_setup * 0.2
)

# Flag as opportunity if:
# - Crowded long + weak fundamentals = POTENTIAL SHORT
# - Crowded short + strong fundamentals = POTENTIAL LONG
```

---

## CLI Commands & Features

### Core Commands

```bash
# Screen entire universe
contrarian screen --universe sp500 --min-score 70

# Analyze single stock
contrarian analyze TSLA --deep

# Find crowded longs (potential shorts)
contrarian crowded-longs --universe nasdaq100

# Find crowded shorts (potential longs)  
contrarian crowded-shorts --min-short-interest 15

# Daily digest
contrarian digest --email nikolay@ribbit.com

# Watch list management
contrarian watch add COIN "monitoring for sentiment shift"
contrarian watch list
contrarian watch alerts
```

### Output Formats

```bash
# Terminal table (default)
contrarian screen --universe sp500

# JSON for piping
contrarian screen --format json | jq '.[] | select(.score > 80)'

# Markdown report
contrarian analyze TSLA --format md > reports/tsla-analysis.md

# CSV export
contrarian screen --format csv > screens/2024-01-15.csv
```

### Sample Output

```
╭──────────────────────────────────────────────────────────────────╮
│                 CONTRARIAN OPPORTUNITIES                          │
│                 Generated: 2024-01-15 09:30 ET                    │
╰──────────────────────────────────────────────────────────────────╯

CROWDED SHORTS (Potential Longs)
┌────────┬───────┬────────────┬──────────┬───────────┬─────────────┐
│ Ticker │ Score │ Short Int. │ Analysts │ Sentiment │ Signal      │
├────────┼───────┼────────────┼──────────┼───────────┼─────────────┤
│ COIN   │  87   │   18.2%    │  2.1/5   │ 🐻 23%   │ CONTRARIAN  │
│ SNAP   │  82   │   12.4%    │  2.4/5   │ 🐻 31%   │ CONTRARIAN  │
│ PARA   │  79   │   22.1%    │  2.0/5   │ 🐻 18%   │ CONTRARIAN  │
└────────┴───────┴────────────┴──────────┴───────────┴─────────────┘

CROWDED LONGS (Potential Shorts)  
┌────────┬───────┬────────────┬──────────┬───────────┬─────────────┐
│ Ticker │ Score │ Short Int. │ Analysts │ Sentiment │ Signal      │
├────────┼───────┼────────────┼──────────┼───────────┼─────────────┤
│ NVDA   │  74   │    1.2%    │  4.8/5   │ 🐂 94%   │ WATCH       │
│ PLTR   │  71   │    3.4%    │  4.2/5   │ 🐂 89%   │ WATCH       │
└────────┴───────┴────────────┴──────────┴───────────┴─────────────┘

Run `contrarian analyze <TICKER>` for deep dive
```

---

## Implementation Phases

### Phase 1: Foundation (Day 1-2)
**Goal**: Basic data pipeline and single-stock analysis

```
Tasks:
□ Set up Python project structure with Poetry/uv
□ Implement yfinance data fetcher (price, fundamentals, analyst ratings)
□ Implement Finviz scraper (short interest, insider data)
□ Create basic Stock dataclass/model
□ Build `contrarian analyze <TICKER>` command
□ Simple terminal output with Rich library
```

**Deliverable**: Can run `contrarian analyze AAPL` and see basic metrics

### Phase 2: Sentiment Layer (Day 3-4)
**Goal**: Add sentiment data sources

```
Tasks:
□ Reddit API integration (PRAW) - mention frequency, sentiment
□ StockTwits API - bull/bear ratios
□ Build sentiment aggregation logic
□ Implement Sentiment Concentration Score
□ Add sentiment data to analyze output
```

**Deliverable**: Sentiment scores included in analysis

### Phase 3: Screening Engine (Day 5-6)
**Goal**: Screen across stock universes

```
Tasks:
□ Define universes (S&P 500, NASDAQ 100, Russell 2000, custom)
□ Build parallel data fetching (async/threading)
□ Implement Fundamental Divergence Score
□ Implement Combined Contrarian Score
□ Build `contrarian screen` command
□ Add filtering and sorting options
□ Caching layer (SQLite) to avoid API hammering
```

**Deliverable**: Can screen S&P 500 and get ranked opportunities

### Phase 4: Polish & Automation (Day 7)
**Goal**: Production-ready features

```
Tasks:
□ Watchlist functionality with alerts
□ Daily digest generation (markdown report)
□ JSON/CSV export formats
□ Configuration file for API keys, preferences
□ Rate limiting and error handling
□ Basic backtesting: "how did past signals perform?"
□ README and usage documentation
```

**Deliverable**: Full-featured CLI ready for daily use

---

## Project Structure

```
contrarian-screener/
├── pyproject.toml
├── README.md
├── .env.example
├── contrarian/
│   ├── __init__.py
│   ├── cli.py                 # Click/Typer CLI definitions
│   ├── config.py              # Settings and API keys
│   ├── models/
│   │   ├── __init__.py
│   │   ├── stock.py           # Stock dataclass
│   │   └── sentiment.py       # Sentiment models
│   ├── data/
│   │   ├── __init__.py
│   │   ├── yahoo.py           # yfinance wrapper
│   │   ├── finviz.py          # Finviz scraper
│   │   ├── reddit.py          # Reddit/PRAW integration
│   │   ├── stocktwits.py      # StockTwits API
│   │   └── cache.py           # SQLite caching
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── sentiment.py       # Sentiment scoring
│   │   ├── fundamentals.py    # Fundamental analysis
│   │   └── scoring.py         # Combined contrarian score
│   ├── output/
│   │   ├── __init__.py
│   │   ├── terminal.py        # Rich terminal output
│   │   ├── export.py          # JSON/CSV/MD export
│   │   └── digest.py          # Daily report generation
│   └── universes/
│       ├── __init__.py
│       └── tickers.py         # Universe definitions
├── tests/
│   └── ...
└── data/
    ├── cache.db               # SQLite cache
    └── watchlist.json         # Saved watchlist
```

---

## Key Dependencies

```toml
[tool.poetry.dependencies]
python = "^3.11"
typer = "^0.9.0"           # CLI framework
rich = "^13.0"             # Beautiful terminal output
yfinance = "^0.2.0"        # Yahoo Finance data
praw = "^7.7.0"            # Reddit API
httpx = "^0.25.0"          # Async HTTP client
beautifulsoup4 = "^4.12"   # Finviz scraping
pandas = "^2.0"            # Data manipulation
sqlite-utils = "^3.35"     # Easy SQLite caching
python-dotenv = "^1.0"     # Environment variables
```

---

## Configuration

```toml
# config.toml
[api_keys]
# Reddit (required for sentiment)
reddit_client_id = "xxx"
reddit_client_secret = "xxx"

# Optional - uses free methods if not provided
yahoo_rapidapi_key = ""      # RapidAPI key for Yahoo Finance
finviz_api_key = ""          # Finviz Elite API key
alpha_vantage = ""           # Alpha Vantage key

[preferences]
default_universe = "sp500"
min_market_cap = 1_000_000_000  # $1B minimum
cache_ttl_hours = 4
output_format = "terminal"

# Data source preferences (auto, api, free)
# "auto" = use API if key provided, else free method
yahoo_source = "auto"
finviz_source = "auto"

[scoring]
sentiment_weight = 0.4
fundamental_weight = 0.4
technical_weight = 0.2
min_short_interest_for_crowded = 15  # %
min_analyst_consensus_for_crowded = 80  # %

[rate_limits]
# Requests per minute (adjusted based on API vs scraping)
yahoo_free_rpm = 5
yahoo_api_rpm = 30
finviz_free_rpm = 2
finviz_api_rpm = 60

[watchlist]
alert_on_score_change = 10  # points
```

---

## Example Claude Code Prompts

Use these prompts sequentially with Claude Code:

### Prompt 1: Project Setup
```
Initialize a new Python project called "contrarian-screener" using uv or Poetry. 
Set up the directory structure as specified in the plan. Install core dependencies:
typer, rich, yfinance, httpx, beautifulsoup4, pandas, sqlite-utils, python-dotenv.
Create a basic CLI entry point that responds to `contrarian --help`.
```

### Prompt 2: Data Layer
```
Implement the data fetching layer:
1. Create a Yahoo Finance wrapper in data/yahoo.py that fetches:
   - Current price and 52-week range
   - P/E, P/B, market cap
   - Analyst recommendations (buy/hold/sell counts)
   - Revenue growth, profit margins
2. Create a Finviz scraper in data/finviz.py that fetches:
   - Short interest (% of float)
   - Insider transactions (last 3 months)
3. Both should return typed dataclasses defined in models/
4. Add basic caching with SQLite to avoid repeated API calls
```

### Prompt 3: Sentiment Analysis
```
Implement sentiment scoring in analysis/sentiment.py:
1. Calculate Sentiment Concentration Score (0-100) based on:
   - Analyst consensus (% buy vs sell)
   - Short interest level
   - Insider buying/selling pattern
2. Classify stocks as "crowded_long", "crowded_short", or "neutral"
3. Create the `contrarian analyze <TICKER>` command that shows all metrics
```

### Prompt 4: Screening Engine
```
Build the screening engine:
1. Define stock universes in universes/tickers.py (S&P 500, NASDAQ 100, etc.)
2. Implement parallel data fetching with proper rate limiting
3. Calculate Fundamental Divergence Score based on plan methodology
4. Combine into final Contrarian Score
5. Create `contrarian screen --universe <name>` command
6. Output sorted table using Rich library
```

### Prompt 5: Polish
```
Add finishing touches:
1. Watchlist functionality (add, remove, list, check alerts)
2. Export formats: --format json, --format csv, --format md
3. Daily digest command that generates a markdown report
4. Proper error handling and helpful error messages
5. README with usage examples
```

---

## Success Criteria

The tool is complete when you can run:

```bash
# Morning routine
contrarian digest > ~/Desktop/morning-screen.md

# Quick check on a name
contrarian analyze COIN --deep

# Weekly full screen
contrarian screen --universe sp500 --min-score 70 --format csv > screens/weekly.csv

# Track interesting names
contrarian watch add SNAP "sentiment extremely negative, fundamentals stabilizing"
contrarian watch alerts
```

---

## Future Enhancements (V2)

- **Backtesting module**: How did historical signals perform?
- **Options flow integration**: Unusual options activity as sentiment signal
- **13F tracking**: What are top funds buying/selling?
- **Earnings surprise correlation**: Do contrarian setups predict earnings surprises?
- **Slack/Discord bot**: Push alerts to messaging
- **Web dashboard**: Simple Flask/FastAPI UI for non-CLI users
- **LLM-powered analysis**: Use Claude API to generate narrative summaries

---

## Notes for Nikolay

A few things to keep in mind:

1. **API Rate Limits**: Yahoo Finance and Finviz don't require API keys but will rate limit aggressive scraping. The caching layer is essential.

2. **Reddit API**: You'll need to create a Reddit app at reddit.com/prefs/apps to get API credentials. Free tier is generous.

3. **This is a starting point**: The scoring methodology is intentionally simple. Tune the weights based on what you find predictive in practice.

4. **Not investment advice**: Obviously this is a research tool, not a trading system. The contrarian signal is one input among many!

Good luck, and let me know if you want me to help iterate on any section.
