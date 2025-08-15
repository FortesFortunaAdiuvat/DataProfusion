"""Tests for FRED API client."""

import pytest
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from app.data.fred_client import FREDDataMiner


class TestFREDDataMiner:
    """Test the FREDDataMiner class."""
    
    def test_initialization_without_fredapi(self):
        """Test that initialization fails gracefully without fredapi."""
        with patch('app.data.fred_client.FREDAPI_AVAILABLE', False):
            with pytest.raises(ImportError, match="fredapi library not installed"):
                FREDDataMiner()
    
    @patch('app.data.fred_client.get_api_key')
    @patch('app.data.fred_client.get_config')
    def test_initialization_with_config(self, mock_get_config, mock_get_api_key, mock_fred_api, temp_config_dir):
        """Test initialization with configuration."""
        mock_get_api_key.return_value = "test_key_123"
        mock_config = Mock()
        mock_config.get_config.return_value = str(temp_config_dir / "cache")
        mock_get_config.return_value = mock_config
        
        miner = FREDDataMiner()
        
        assert miner.api_key == "test_key_123"
        assert miner.cache_dir.name == "cache"
        mock_fred_api.assert_called_once_with(api_key="test_key_123")
    
    @patch('app.data.fred_client.get_api_key')
    @patch('app.data.fred_client.get_config')
    def test_initialization_without_api_key(self, mock_get_config, mock_get_api_key, mock_fred_api, temp_config_dir):
        """Test initialization without API key."""
        mock_get_api_key.return_value = None
        mock_config = Mock()
        mock_config.get_config.return_value = str(temp_config_dir / "cache")
        mock_get_config.return_value = mock_config
        
        miner = FREDDataMiner()
        
        assert miner.api_key is None
        mock_fred_api.assert_called_once_with(api_key=None)
    
    @patch('app.data.fred_client.get_api_key')
    @patch('app.data.fred_client.get_config')
    def test_cache_database_initialization(self, mock_get_config, mock_get_api_key, mock_fred_api, temp_config_dir):
        """Test that cache database is properly initialized."""
        mock_get_api_key.return_value = "test_key"
        mock_config = Mock()
        mock_config.get_config.return_value = str(temp_config_dir / "cache")
        mock_get_config.return_value = mock_config
        
        miner = FREDDataMiner()
        
        # Check that database file exists
        assert miner.db_path.exists()
        
        # Check that tables are created
        with sqlite3.connect(miner.db_path) as conn:
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            assert "series_data" in tables
            assert "series_metadata" in tables
    
    @patch('app.data.fred_client.get_api_key')
    @patch('app.data.fred_client.get_config')
    def test_get_series_from_api(self, mock_get_config, mock_get_api_key, mock_fred_api, temp_config_dir, sample_fred_series, sample_fred_metadata):
        """Test fetching series data from API."""
        mock_get_api_key.return_value = "test_key"
        mock_config = Mock()
        mock_config.get_config.return_value = str(temp_config_dir / "cache")
        mock_get_config.return_value = mock_config
        
        # Mock API responses
        mock_fred_api.return_value.get_series.return_value = sample_fred_series
        mock_fred_api.return_value.get_series_info.return_value = sample_fred_metadata
        
        miner = FREDDataMiner()
        result = miner.get_series("GDP", start_date="2020-01-01")
        
        # Verify API was called correctly
        mock_fred_api.return_value.get_series.assert_called_once_with("GDP", "2020-01-01", None)
        mock_fred_api.return_value.get_series_info.assert_called_once_with("GDP")
        
        # Verify result
        pd.testing.assert_series_equal(result, sample_fred_series)
    
    @patch('app.data.fred_client.get_api_key')
    @patch('app.data.fred_client.get_config')
    def test_get_series_from_cache(self, mock_get_config, mock_get_api_key, mock_fred_api, temp_config_dir, sample_fred_series, sample_fred_metadata):
        """Test retrieving series data from cache."""
        mock_get_api_key.return_value = "test_key"
        mock_config = Mock()
        mock_config.get_config.return_value = str(temp_config_dir / "cache")
        mock_get_config.return_value = mock_config
        
        # Mock API responses for initial fetch
        mock_fred_api.return_value.get_series.return_value = sample_fred_series
        mock_fred_api.return_value.get_series_info.return_value = sample_fred_metadata
        
        miner = FREDDataMiner()
        
        # First call - should fetch from API and cache
        result1 = miner.get_series("GDP")
        
        # Reset mock to verify second call doesn't hit API
        mock_fred_api.return_value.reset_mock()
        
        # Second call - should use cache
        result2 = miner.get_series("GDP")
        
        # Verify API was not called second time
        mock_fred_api.return_value.get_series.assert_not_called()
        
        # Verify results are the same
        pd.testing.assert_series_equal(result1, result2)
    
    @patch('app.data.fred_client.get_api_key')
    @patch('app.data.fred_client.get_config')
    def test_force_refresh(self, mock_get_config, mock_get_api_key, mock_fred_api, temp_config_dir, sample_fred_series, sample_fred_metadata):
        """Test force refresh bypasses cache."""
        mock_get_api_key.return_value = "test_key"
        mock_config = Mock()
        mock_config.get_config.return_value = str(temp_config_dir / "cache")
        mock_get_config.return_value = mock_config
        
        # Mock API responses
        mock_fred_api.return_value.get_series.return_value = sample_fred_series
        mock_fred_api.return_value.get_series_info.return_value = sample_fred_metadata
        
        miner = FREDDataMiner()
        
        # First call to populate cache
        miner.get_series("GDP")
        
        # Reset mock
        mock_fred_api.return_value.reset_mock()
        mock_fred_api.return_value.get_series.return_value = sample_fred_series
        mock_fred_api.return_value.get_series_info.return_value = sample_fred_metadata
        
        # Force refresh should hit API again
        result = miner.get_series("GDP", force_refresh=True)
        
        mock_fred_api.return_value.get_series.assert_called_once()
        pd.testing.assert_series_equal(result, sample_fred_series)
    
    @patch('app.data.fred_client.get_api_key')
    @patch('app.data.fred_client.get_config')
    def test_api_error_fallback_to_cache(self, mock_get_config, mock_get_api_key, mock_fred_api, temp_config_dir, sample_fred_series, sample_fred_metadata):
        """Test fallback to cache when API fails."""
        mock_get_api_key.return_value = "test_key"
        mock_config = Mock()
        mock_config.get_config.return_value = str(temp_config_dir / "cache")
        mock_get_config.return_value = mock_config
        
        miner = FREDDataMiner()
        
        # First, populate cache
        mock_fred_api.return_value.get_series.return_value = sample_fred_series
        mock_fred_api.return_value.get_series_info.return_value = sample_fred_metadata
        miner.get_series("GDP")
        
        # Now make API fail
        mock_fred_api.return_value.get_series.side_effect = Exception("API Error")
        
        # Should fallback to cache
        result = miner.get_series("GDP", force_refresh=True)
        pd.testing.assert_series_equal(result, sample_fred_series)
    
    @patch('app.data.fred_client.get_api_key')
    @patch('app.data.fred_client.get_config')
    def test_get_multiple_series(self, mock_get_config, mock_get_api_key, mock_fred_api, temp_config_dir):
        """Test fetching multiple series."""
        mock_get_api_key.return_value = "test_key"
        mock_config = Mock()
        mock_config.get_config.return_value = str(temp_config_dir / "cache")
        mock_get_config.return_value = mock_config
        
        # Mock different series data
        gdp_data = pd.Series([100, 101, 102], index=pd.date_range('2020-01-01', periods=3, freq='Q'))
        unrate_data = pd.Series([3.5, 3.6, 3.4], index=pd.date_range('2020-01-01', periods=3, freq='M'))
        
        def mock_get_series(series_id, *args, **kwargs):
            if series_id == "GDP":
                return gdp_data
            elif series_id == "UNRATE":
                return unrate_data
            else:
                raise ValueError(f"Unknown series: {series_id}")

        mock_fred_api.return_value.get_series.side_effect = mock_get_series
        mock_fred_api.return_value.get_series_info.return_value = pd.Series({'title': 'Test'})
        
        miner = FREDDataMiner()
        result = miner.get_multiple_series(["GDP", "UNRATE"])
        
        assert "GDP" in result.columns
        assert "UNRATE" in result.columns
        assert len(result.columns) == 2
    
    @patch('app.data.fred_client.get_api_key')
    @patch('app.data.fred_client.get_config')
    def test_search_series(self, mock_get_config, mock_get_api_key, mock_fred_api, temp_config_dir):
        """Test searching for series."""
        mock_get_api_key.return_value = "test_key"
        mock_config = Mock()
        mock_config.get_config.return_value = str(temp_config_dir / "cache")
        mock_get_config.return_value = mock_config
        
        # Mock search results
        search_results = pd.DataFrame({
            'id': ['GDP', 'GDPC1'],
            'title': ['Gross Domestic Product', 'Real GDP'],
            'units': ['Billions of Dollars', 'Billions of Chained 2012 Dollars']
        })
        
        mock_fred_api.return_value.search.return_value = search_results
        
        miner = FREDDataMiner()
        result = miner.search_series("GDP", limit=5)
        
        mock_fred_api.return_value.search.assert_called_once_with("GDP", limit=5)
        pd.testing.assert_frame_equal(result, search_results)
    
    @patch('app.data.fred_client.get_api_key')
    @patch('app.data.fred_client.get_config')
    def test_cache_expiration(self, mock_get_config, mock_get_api_key, mock_fred_api, temp_config_dir, sample_fred_series, sample_fred_metadata):
        """Test that old cache data is refreshed."""
        mock_get_api_key.return_value = "test_key"
        mock_config = Mock()
        mock_config.get_config.return_value = str(temp_config_dir / "cache")
        mock_get_config.return_value = mock_config
        
        miner = FREDDataMiner()
        
        # Manually insert old data into cache
        old_timestamp = (datetime.now() - timedelta(hours=25)).isoformat()
        with sqlite3.connect(miner.db_path) as conn:
            conn.execute(
                "INSERT INTO series_metadata (series_id, title, last_updated) VALUES (?, ?, ?)",
                ("GDP", "Test GDP", old_timestamp)
            )
            conn.execute(
                "INSERT INTO series_data (series_id, date, value, last_updated) VALUES (?, ?, ?, ?)",
                ("GDP", "2020-01-01", 100.0, old_timestamp)
            )
        
        # Mock fresh API response
        mock_fred_api.return_value.get_series.return_value = sample_fred_series
        mock_fred_api.return_value.get_series_info.return_value = sample_fred_metadata
        
        # Should fetch fresh data due to cache expiration
        result = miner.get_series("GDP")

        mock_fred_api.return_value.get_series.assert_called_once()
        pd.testing.assert_series_equal(result, sample_fred_series)