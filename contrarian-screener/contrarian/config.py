import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Project paths
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"
    CACHE_FILE = DATA_DIR / "cache.db"
    
    # API Keys (loaded from environment variables)
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    YAHOO_RAPIDAPI_KEY = os.getenv("YAHOO_RAPIDAPI_KEY")
    FINVIZ_API_KEY = os.getenv("FINVIZ_API_KEY")
    
    # Preferences
    DEFAULT_UNIVERSE = "sp500"
    CACHE_TTL_HOURS = 4
    
    # Create data directory if it doesn't exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)

config = Config()
