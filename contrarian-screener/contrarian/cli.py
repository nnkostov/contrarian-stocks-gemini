import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import typer
import json
import csv
import io
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
from concurrent.futures import ThreadPoolExecutor, as_completed
from contrarian.data.yahoo import YahooFinanceClient
from contrarian.data.finviz import FinvizClient
from contrarian.data.reddit import RedditClient
from contrarian.data.stocktwits import StockTwitsClient
from contrarian.analysis.sentiment import SentimentAnalyzer
from contrarian.analysis.scoring import ContrarianScorer
from contrarian.analysis.pipeline import fetch_and_score
from contrarian.universes.tickers import Universe
from contrarian.models.stock import Stock
from contrarian.config import config

app = typer.Typer(
    name="contrarian",
    help="Contrarian Stock Screener CLI — Find opportunities where sentiment diverges from fundamentals.",
    add_completion=False,
)
watch_app = typer.Typer(name="watch", help="Manage your watchlist")
app.add_typer(watch_app, name="watch")

console = Console()

@app.command()
def analyze(
    ticker: str = typer.Argument(..., help="Stock ticker symbol (e.g., AAPL)"),
    deep: bool = typer.Option(False, "--deep", help="Perform deep analysis including latest news"),
    format: str = typer.Option("terminal", "--format", help="Output format: terminal, json, md"),
):
    """
    Analyze a single stock for contrarian signals.
    """
    if format == "terminal":
        console.print(f"[bold blue]Analyzing {ticker.upper()}...[/bold blue]")
    
    # Use pipeline function
    data = fetch_and_score(ticker)
    
    if not data:
        console.print(f"[red]Could not fetch data for {ticker}[/red]")
        return

    stock = data["stock"]
    scores = data["scores"]

    # Display Data
    if format == "terminal":
        display_stock_dashboard(stock, scores)
    elif format == "json":
        import dataclasses
        output = {
            "ticker": stock.ticker,
            "price": stock.price,
            "scores": scores,
            "sentiment": dataclasses.asdict(stock.sentiment) if stock.sentiment else None,
            "financials": dataclasses.asdict(stock.financials) if stock.financials else None
        }
        print(json.dumps(output, indent=2))
    elif format == "md":
        print(f"# Analysis: {stock.company_name} ({stock.ticker})\n")
        print(f"**Signal:** {scores['signal']} (Score: {scores['contrarian_score']:.1f})\n")
        print("## Fundamentals")
        if stock.financials:
            print(f"- P/E: {stock.financials.pe_ratio}")
            print(f"- Revenue Growth: {stock.financials.revenue_growth}")
        print("\n## Sentiment")
        if stock.sentiment:
            print(f"- Short Interest: {stock.sentiment.short_interest_pct}%")
            print(f"- Consensus: {stock.sentiment.analyst_consensus_score}/100")

@app.command()
def screen(
    universe: str = typer.Option("sp500", "--universe", "-u", help="Stock universe to screen (sp500, nasdaq100, test)"),
    min_score: int = typer.Option(50, "--min-score", help="Minimum contrarian score filter"),
    format: str = typer.Option("terminal", "--format", help="Output format: terminal, json, csv"),
):
    """
    Screen a universe of stocks for opportunities.
    """
    tickers = Universe.get_tickers(universe)
    if format == "terminal":
        console.print(f"[bold green]Screening {len(tickers)} stocks in '{universe}'...[/bold green]")
    
    results = []
    
    if format == "terminal":
        with Progress() as progress:
            task = progress.add_task("[cyan]Scanning market...", total=len(tickers))
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {executor.submit(fetch_and_score, t): t for t in tickers}
                for future in as_completed(futures):
                    data = future.result()
                    if data and data["scores"]["contrarian_score"] >= min_score:
                        results.append(data)
                    progress.advance(task)
    else:
        # No progress bar for clean stdout
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(fetch_and_score, t): t for t in tickers}
            for future in as_completed(futures):
                data = future.result()
                if data and data["scores"]["contrarian_score"] >= min_score:
                    results.append(data)

    # Sort by Score Descending
    results.sort(key=lambda x: x["scores"]["contrarian_score"], reverse=True)
    
    # Output
    if format == "terminal":
        table = Table(title=f"Contrarian Opportunities (> {min_score})")
        table.add_column("Ticker", style="cyan", no_wrap=True)
        table.add_column("Price", style="green")
        table.add_column("Contrarian Score", style="bold yellow")
        table.add_column("Signal", style="bold magenta")
        
        for res in results:
            s = res["stock"]
            sc = res["scores"]
            table.add_row(
                s.ticker,
                f"${s.price:.2f}",
                f"{sc['contrarian_score']:.1f}",
                sc["signal"]
            )
        console.print(table)
        
    elif format == "json":
        simple_res = [{
            "ticker": r["ticker"],
            "score": r["scores"]["contrarian_score"],
            "signal": r["scores"]["signal"]
        } for r in results]
        print(json.dumps(simple_res, indent=2))
        
    elif format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Ticker", "Price", "Score", "Signal"])
        for r in results:
            writer.writerow([
                r["ticker"],
                r["stock"].price,
                r["scores"]["contrarian_score"],
                r["scores"]["signal"]
            ])
        print(output.getvalue())

@app.command()
def digest(email: str = typer.Option(None, "--email", help="Email to send digest to (simulated)")):
    """
    Generate a daily digest of opportunities.
    """
    console.print("[bold]Generating Daily Contrarian Digest...[/bold]")
    
    # Screen Top Universes
    top_picks = []
    
    # Quick scan of test universe for demo
    tickers = Universe.get_tickers("test")
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(fetch_and_score, t): t for t in tickers}
        for future in as_completed(futures):
            data = future.result()
            if data and data["scores"]["contrarian_score"] > 60:
                top_picks.append(data)
                
    top_picks.sort(key=lambda x: x["scores"]["contrarian_score"], reverse=True)
    
    # Generate Markdown
    md = f"# 🗞️ Daily Contrarian Digest - {datetime.now().strftime('%Y-%m-%d')}\n\n"
    
    if not top_picks:
        md += "No strong signals detected today.\n"
    else:
        md += "## Top Opportunities\n\n"
        md += "| Ticker | Score | Signal | Price |\n"
        md += "|--------|-------|--------|-------|\n"
        for p in top_picks:
            s = p["stock"]
            sc = p["scores"]
            md += f"| **{s.ticker}** | {sc['contrarian_score']:.1f} | {sc['signal']} | ${s.price:.2f} |\n"
    
    console.print(Panel(md, title="Digest Preview"))
    
    if email:
        console.print(f"[green]Digest emailed to {email}![/green]")
    else:
        console.print("[dim]Use --email to simulate sending this report.[/dim]")

# --- Watchlist Commands ---

WATCHLIST_FILE = config.DATA_DIR / "watchlist.json"


def load_watchlist():
    if not WATCHLIST_FILE.exists():
        return []
    with open(WATCHLIST_FILE, "r") as f:
        return json.load(f)

def save_watchlist(data):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(data, f, indent=4)

@watch_app.command("add")
def watch_add(ticker: str, note: str = ""):
    """Add a stock to watchlist."""
    data = load_watchlist()
    # Check if exists
    if any(i["ticker"] == ticker.upper() for i in data):
        console.print(f"[yellow]{ticker} is already in watchlist.[/yellow]")
        return
        
    data.append({
        "ticker": ticker.upper(),
        "note": note,
        "added_at": datetime.now().isoformat()
    })
    save_watchlist(data)
    console.print(f"[green]Added {ticker} to watchlist.[/green]")

@watch_app.command("list")
def watch_list():
    """List watched stocks."""
    data = load_watchlist()
    if not data:
        console.print("Watchlist is empty.")
        return
        
    table = Table(title="Watchlist")
    table.add_column("Ticker", style="cyan")
    table.add_column("Note", style="italic")
    table.add_column("Added", style="dim")
    
    for item in data:
        table.add_row(item["ticker"], item["note"], item["added_at"][:10])
    
    console.print(table)

@watch_app.command("remove")
def watch_remove(ticker: str):
    """Remove a stock from watchlist."""
    data = load_watchlist()
    new_data = [i for i in data if i["ticker"] != ticker.upper()]
    
    if len(data) == len(new_data):
        console.print(f"[yellow]{ticker} not found in watchlist.[/yellow]")
    else:
        save_watchlist(new_data)
        console.print(f"[green]Removed {ticker}.[/green]")

def display_stock_dashboard(stock: Stock, scores: dict):
    # Main Info
    console.print(Panel.fit(
        f"[bold active]{stock.company_name} ({stock.ticker})[/bold active]\n"
        f"Price: ${stock.price:,.2f}\n"
        f"Sector: {stock.sector} | Industry: {stock.industry}\n"
        f"[bold yellow]Signal: {scores['signal']} (Score: {scores['contrarian_score']:.1f})[/bold yellow]"
    ))

    # Fundamentals Table
    fund_table = Table(title=f"Fundamentals (Score: {scores['fundamental_score']:.1f})", show_header=True)
    fund_table.add_column("Metric", style="cyan")
    fund_table.add_column("Value", style="magenta")
    
    if stock.financials:
        f = stock.financials
        fund_table.add_row("Market Cap", f"${f.market_cap:,.0f}" if f.market_cap else "-")
        fund_table.add_row("P/E Ratio", f"{f.pe_ratio:.2f}" if f.pe_ratio else "-")
        fund_table.add_row("P/B Ratio", f"{f.pb_ratio:.2f}" if f.pb_ratio else "-")
        fund_table.add_row("Revenue Growth", f"{f.revenue_growth:.1%}" if f.revenue_growth else "-")
        fund_table.add_row("Profit Margin", f"{f.profit_margin:.1%}" if f.profit_margin else "-")
        fund_table.add_row("Debt/Equity", f"{f.debt_to_equity:.2f}" if f.debt_to_equity else "-")
    
    console.print(fund_table)

    # Sentiment Table
    sent_table = Table(title=f"Sentiment (Score: {scores['sentiment_score']:.1f})", show_header=True)
    sent_table.add_column("Metric", style="cyan")
    sent_table.add_column("Value", style="yellow")
    
    if stock.sentiment:
        s = stock.sentiment
        sent_table.add_row("Short Interest", f"{s.short_interest_pct:.2f}%" if s.short_interest_pct else "-")
        sent_table.add_row("Analyst Consensus", f"{s.analyst_consensus_score:.0f}/100")
        sent_table.add_row("Reddit Mentions (Wk)", str(s.reddit_mentions))
        sent_table.add_row("Reddit Sentiment", f"{s.reddit_sentiment_score:.0%} Bullish")
        sent_table.add_row("StockTwits Sentiment", f"{s.stocktwits_bull_ratio:.0%} Bullish")
        
    console.print(sent_table)




if __name__ == "__main__":
    app()
