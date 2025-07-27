"""Integration tests for FRED API client.

These tests require a valid FRED API key and internet connection.
They can be skipped by setting SKIP_INTEGRATION_TESTS=1 environment variable.
"""

import pytest
import os
import pandas as pd
from datetime import datetime, timedelta

from app.data.fred_client import FREDDataMiner
from app.config.secrets import get_api_key


# Skip integration tests if requested or no API key available
skip_integration = (
    os.getenv("SKIP_INTEGRATION_TESTS", "0") == "1" or 
    not get_api_key("fred")
)


@pytest.mark.skipif(skip_integration, reason="Integration tests disabled or no API key")
class TestFREDIntegration:
    """Integration tests with real FRED API."""
    
    @pytest.fixture(scope="class")
    def fred_client(self):
        """Create a FRED client for integration testing."""
        api_key = get_api_key("fred")
        if not api_key:
            pytest.skip("No FRED API key available")
        
        return FREDDataMiner(api_key=api_key)
    
    def test_api_key_validation(self, fred_client):
        """Test that the API key is valid by making a simple request."""
        try:
            # Try to fetch a small amount of GDP data
            result = fred_client.get_series("GDP", start_date="2023-01-01", end_date="2023-12-31")
            assert isinstance(result, pd.Series)
            assert len(result) > 0
            print(f"✓ API key is valid. Retrieved {len(result)} GDP data points.")
        except Exception as e:
            pytest.fail(f"API key validation failed: {e}")
    
    def test_fetch_common_indicators(self, fred_client):
        """Test fetching common economic indicators."""
        indicators = ["GDP", "UNRATE", "CPIAUCSL", "FEDFUNDS"]
        start_date = "2023-01-01"
        
        for indicator in indicators:
            try:
                result = fred_client.get_series(indicator, start_date=start_date)
                assert isinstance(result, pd.Series)
                assert len(result) > 0
                print(f"✓ Successfully fetched {indicator}: {len(result)} data points")
            except Exception as e:
                pytest.fail(f"Failed to fetch {indicator}: {e}")
    
    def test_multiple_series_fetch(self, fred_client):
        """Test fetching multiple series at once."""
        indicators = ["GDP", "UNRATE", "CPIAUCSL"]
        
        try:
            result = fred_client.get_multiple_series(indicators, start_date="2023-01-01")
            assert isinstance(result, pd.DataFrame)
            assert len(result.columns) == len(indicators)
            
            for indicator in indicators:
                assert indicator in result.columns
                assert result[indicator].notna().sum() > 0
            
            print(f"✓ Successfully fetched multiple series: {list(result.columns)}")
        except Exception as e:
            pytest.fail(f"Failed to fetch multiple series: {e}")
    
    def test_search_functionality(self, fred_client):
        """Test the search functionality."""
        try:
            results = fred_client.search_series("unemployment", limit=5)
            assert isinstance(results, pd.DataFrame)
            assert len(results) > 0
            assert 'id' in results.columns
            assert 'title' in results.columns
            
            print(f"✓ Search returned {len(results)} results for 'unemployment'")
            
            # Check that UNRATE is in the results
            unemployment_series = results[results['id'].str.contains('UNRATE', na=False)]
            assert len(unemployment_series) > 0
            
        except Exception as e:
            pytest.fail(f"Search functionality failed: {e}")
    
    def test_data_caching(self, fred_client):
        """Test that data caching works correctly."""
        series_id = "GDP"
        start_date = "2023-01-01"
        
        # First fetch - should hit API
        start_time = datetime.now()
        result1 = fred_client.get_series(series_id, start_date=start_date)
        first_fetch_time = datetime.now() - start_time
        
        # Second fetch - should use cache (much faster)
        start_time = datetime.now()
        result2 = fred_client.get_series(series_id, start_date=start_date)
        second_fetch_time = datetime.now() - start_time
        
        # Verify results are identical
        pd.testing.assert_series_equal(result1, result2)
        
        # Cache should be significantly faster
        assert second_fetch_time < first_fetch_time
        print(f"✓ Caching working: First fetch {first_fetch_time.total_seconds():.2f}s, "
              f"cached fetch {second_fetch_time.total_seconds():.2f}s")
    
    def test_force_refresh(self, fred_client):
        """Test force refresh functionality."""
        series_id = "UNRATE"
        start_date = "2023-01-01"
        
        # Initial fetch
        result1 = fred_client.get_series(series_id, start_date=start_date)
        
        # Force refresh
        result2 = fred_client.get_series(series_id, start_date=start_date, force_refresh=True)
        
        # Results should be identical (same data from API)
        pd.testing.assert_series_equal(result1, result2)
        print(f"✓ Force refresh working for {series_id}")
    
    def test_date_range_filtering(self, fred_client):
        """Test that date range filtering works correctly."""
        series_id = "GDP"
        start_date = "2020-01-01"
        end_date = "2021-12-31"
        
        try:
            result = fred_client.get_series(series_id, start_date=start_date, end_date=end_date)
            
            # Verify date range
            assert result.index.min() >= pd.to_datetime(start_date)
            assert result.index.max() <= pd.to_datetime(end_date)
            
            print(f"✓ Date filtering working: {result.index.min()} to {result.index.max()}")
            
        except Exception as e:
            pytest.fail(f"Date range filtering failed: {e}")
    
    def test_error_handling_invalid_series(self, fred_client):
        """Test error handling for invalid series IDs."""
        invalid_series = "INVALID_SERIES_ID_12345"
        
        with pytest.raises(Exception):
            fred_client.get_series(invalid_series)
        
        print("✓ Error handling working for invalid series ID")
    
    def test_rate_limiting_compliance(self, fred_client):
        """Test that we don't exceed FRED's rate limits."""
        # FRED allows 120 requests per minute
        # We'll make several requests and ensure they complete without errors
        
        series_list = ["GDP", "UNRATE", "CPIAUCSL", "FEDFUNDS", "DGS10"]
        start_time = datetime.now()
        
        try:
            for series_id in series_list:
                result = fred_client.get_series(series_id, start_date="2023-01-01")
                assert len(result) > 0
            
            elapsed_time = datetime.now() - start_time
            print(f"✓ Fetched {len(series_list)} series in {elapsed_time.total_seconds():.2f}s without rate limit issues")
            
        except Exception as e:
            if "rate limit" in str(e).lower():
                pytest.fail(f"Rate limit exceeded: {e}")
            else:
                pytest.fail(f"Unexpected error during rate limit test: {e}")


@pytest.mark.skipif(skip_integration, reason="Integration tests disabled or no API key")
def test_api_key_configuration():
    """Test that API key is properly configured."""
    api_key = get_api_key("fred")
    
    if not api_key:
        pytest.fail(
            "No FRED API key found. Please set FRED_API_KEY environment variable "
            "or add it to config/secrets.json"
        )
    
    # Basic validation - FRED API keys are typically 32 characters
    assert len(api_key) >= 20, "API key seems too short"
    assert api_key.isalnum(), "API key should be alphanumeric"
    
    print(f"✓ API key configured: {api_key[:8]}...")


if __name__ == "__main__":
    # Allow running integration tests directly
    pytest.main([__file__, "-v", "-s"])