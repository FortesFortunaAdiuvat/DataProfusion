"""FRED API client with local caching for economic data retrieval."""

from __future__ import annotations

import os
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import logging

from ..config.secrets import get_api_key, get_config

try:
    from fredapi import Fred
    FREDAPI_AVAILABLE = True
except ImportError:
    FREDAPI_AVAILABLE = False
    Fred = None

logger = logging.getLogger(__name__)


class FREDDataMiner:
    """Client for retrieving and caching FRED economic data."""
    
    def __init__(self, api_key: Optional[str] = None, cache_dir: Optional[str] = None):
        """Initialize FRED client with caching.
        
        Parameters
        ----------
        api_key : str, optional
            FRED API key. If None, will try secure config then FRED_API_KEY env var.
        cache_dir : str, optional
            Directory to store cached data files. If None, uses config default.
        """
        if not FREDAPI_AVAILABLE:
            raise ImportError("fredapi library not installed. Run: pip install fredapi")
        
        # Get API key from secure config system
        self.api_key = api_key or get_api_key("fred")
        if not self.api_key:
            logger.warning("No FRED API key found. Requests may be rate limited.")
            logger.info("Set FRED_API_KEY environment variable or add to config/secrets.json")
        
        self.fred = Fred(api_key=self.api_key)
        
        # Get cache directory from config
        if cache_dir is None:
            cache_dir = get_config().get_config('database.cache_dir', 'data_cache')
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Initialize SQLite cache database
        self.db_path = self.cache_dir / "fred_cache.db"
        self._init_cache_db()
    
    def _init_cache_db(self):
        """Initialize SQLite database for caching series data."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS series_data (
                    series_id TEXT,
                    date TEXT,
                    value REAL,
                    last_updated TEXT,
                    PRIMARY KEY (series_id, date)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS series_metadata (
                    series_id TEXT PRIMARY KEY,
                    title TEXT,
                    units TEXT,
                    frequency TEXT,
                    last_updated TEXT,
                    observation_start TEXT,
                    observation_end TEXT
                )
            """)
    
    def get_series(self, series_id: str, start_date: Optional[str] = None, 
                   end_date: Optional[str] = None, force_refresh: bool = False) -> pd.Series:
        """Retrieve economic time series data with caching.
        
        Parameters
        ----------
        series_id : str
            FRED series identifier (e.g., 'GDP', 'UNRATE', 'FEDFUNDS')
        start_date : str, optional
            Start date in YYYY-MM-DD format
        end_date : str, optional
            End date in YYYY-MM-DD format
        force_refresh : bool
            If True, bypass cache and fetch fresh data
            
        Returns
        -------
        pd.Series
            Time series data with dates as index
        """
        if not force_refresh:
            cached_data = self._get_cached_series(series_id, start_date, end_date)
            if cached_data is not None:
                logger.info(f"Retrieved {series_id} from cache")
                return cached_data
        
        try:
            logger.info(f"Fetching {series_id} from FRED API")
            data = self.fred.get_series(series_id, start_date, end_date)
            
            # Cache the data
            self._cache_series(series_id, data)
            
            # Cache metadata
            info = self.fred.get_series_info(series_id)
            self._cache_metadata(series_id, info)
            
            return data
            
        except Exception as e:
            logger.error(f"Failed to fetch {series_id}: {e}")
            # Try to return cached data as fallback
            cached_data = self._get_cached_series(series_id, start_date, end_date)
            if cached_data is not None:
                logger.warning(f"Using cached data for {series_id} due to API error")
                return cached_data
            raise
    
    def _get_cached_series(self, series_id: str, start_date: Optional[str], 
                          end_date: Optional[str]) -> Optional[pd.Series]:
        """Retrieve series from cache if available and recent."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                query = """
                    SELECT date, value FROM series_data 
                    WHERE series_id = ?
                """
                params = [series_id]
                
                if start_date:
                    query += " AND date >= ?"
                    params.append(start_date)
                if end_date:
                    query += " AND date <= ?"
                    params.append(end_date)
                    
                query += " ORDER BY date"
                
                df = pd.read_sql_query(query, conn, params=params)
                
                if df.empty:
                    return None
                
                # Check if data is recent (within 24 hours for daily data)
                last_update_query = """
                    SELECT last_updated FROM series_metadata WHERE series_id = ?
                """
                cursor = conn.execute(last_update_query, [series_id])
                result = cursor.fetchone()
                
                if result:
                    last_updated = datetime.fromisoformat(result[0])
                    if datetime.now() - last_updated > timedelta(hours=24):
                        return None
                
                df['date'] = pd.to_datetime(df['date'])
                return df.set_index('date')['value']
                
        except Exception as e:
            logger.error(f"Error reading cache for {series_id}: {e}")
            return None
    
    def _cache_series(self, series_id: str, data: pd.Series):
        """Store series data in cache."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Clear existing data for this series
                conn.execute("DELETE FROM series_data WHERE series_id = ?", [series_id])
                
                # Insert new data
                records = [
                    (series_id, date.strftime('%Y-%m-%d'), float(value), datetime.now().isoformat())
                    for date, value in data.items()
                    if pd.notna(value)
                ]
                
                conn.executemany(
                    "INSERT INTO series_data (series_id, date, value, last_updated) VALUES (?, ?, ?, ?)",
                    records
                )
                
        except Exception as e:
            logger.error(f"Error caching series {series_id}: {e}")
    
    def _cache_metadata(self, series_id: str, info: pd.Series):
        """Store series metadata in cache."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """INSERT OR REPLACE INTO series_metadata 
                       (series_id, title, units, frequency, last_updated, observation_start, observation_end)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (
                        series_id,
                        info.get('title', ''),
                        info.get('units', ''),
                        info.get('frequency', ''),
                        datetime.now().isoformat(),
                        info.get('observation_start', ''),
                        info.get('observation_end', '')
                    )
                )
        except Exception as e:
            logger.error(f"Error caching metadata for {series_id}: {e}")
    
    def get_multiple_series(self, series_ids: list[str], **kwargs) -> pd.DataFrame:
        """Retrieve multiple series and return as DataFrame.
        
        Parameters
        ----------
        series_ids : list[str]
            List of FRED series identifiers
        **kwargs
            Additional arguments passed to get_series()
            
        Returns
        -------
        pd.DataFrame
            DataFrame with series as columns
        """
        data = {}
        for series_id in series_ids:
            try:
                data[series_id] = self.get_series(series_id, **kwargs)
            except Exception as e:
                logger.error(f"Failed to retrieve {series_id}: {e}")
                continue
        
        return pd.DataFrame(data)
    
    def search_series(self, search_text: str, limit: int = 10) -> pd.DataFrame:
        """Search for FRED series by text.
        
        Parameters
        ----------
        search_text : str
            Search query
        limit : int
            Maximum number of results
            
        Returns
        -------
        pd.DataFrame
            Search results with series info
        """
        try:
            return self.fred.search(search_text, limit=limit)
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return pd.DataFrame()
