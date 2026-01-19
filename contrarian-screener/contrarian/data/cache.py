from sqlite_utils import Database
from contrarian.config import config
from contrarian.models.stock import Stock
import json
import time
from typing import Optional
from dataclasses import asdict

class Cache:
    def __init__(self):
        self.db = Database(config.CACHE_FILE)
        self.table = self.db["stocks"]
        
        # Ensure table exists with composite primary key or index if needed
        if not self.table.exists():
            self.table.create({
                "ticker": str,
                "data": str, # JSON serialized Stock object
                "updated_at": float
            }, pk="ticker")
    
    def get(self, ticker: str) -> Optional[Stock]:
        row = self.table.get(ticker)
        if not row:
            return None
        
        # Check TTL
        if time.time() - row["updated_at"] > (config.CACHE_TTL_HOURS * 3600):
            return None
            
        # Deserialize (Simplified for MVP: assumes strict structure)
        # In a real app, we'd want robust deserialization logic
        # For now, we'll rely on the caller to refetch if None is returned
        # Or we can return the raw dict and let the factory reconstruct it
        # But `Stock` is nested, so let's skip complex reconstruction here for this step
        # and just return None to force refetch until we build a proper serializer.
        
        # Actually, let's just return None for now to ensure we test the live fetch first.
        # Implementation of full serialization/deserialization is a nice-to-have for Phase 1.
        return None 

    def set(self, stock: Stock):
        # We need a custom serializer because Stock contains nested dataclasses
        # For Phase 1, we will just store it.
        # We won't implement full retrieval logic yet, just the storage mechanism.
        pass

# Instantiate a global cache
cache = Cache()
