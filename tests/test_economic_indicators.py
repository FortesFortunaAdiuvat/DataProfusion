"""Tests for economic indicators module."""

import pytest
from app.data.economic_indicators import (
    GDP_INDICATORS, EMPLOYMENT_INDICATORS, INFLATION_INDICATORS,
    INTEREST_RATE_INDICATORS, CONSUMER_INDICATORS, HOUSING_INDICATORS,
    ALL_INDICATORS, get_indicator_info
)


class TestEconomicIndicators:
    """Test economic indicators constants and utilities."""
    
    def test_indicator_dictionaries_not_empty(self):
        """Test that all indicator dictionaries contain data."""
        assert len(GDP_INDICATORS) > 0
        assert len(EMPLOYMENT_INDICATORS) > 0
        assert len(INFLATION_INDICATORS) > 0
        assert len(INTEREST_RATE_INDICATORS) > 0
        assert len(CONSUMER_INDICATORS) > 0
        assert len(HOUSING_INDICATORS) > 0
    
    def test_common_indicators_present(self):
        """Test that common economic indicators are present."""
        # GDP indicators
        assert "GDP" in GDP_INDICATORS
        assert "GDPC1" in GDP_INDICATORS
        
        # Employment indicators
        assert "UNRATE" in EMPLOYMENT_INDICATORS
        assert "PAYEMS" in EMPLOYMENT_INDICATORS
        
        # Inflation indicators
        assert "CPIAUCSL" in INFLATION_INDICATORS
        assert "PCEPI" in INFLATION_INDICATORS
        
        # Interest rate indicators
        assert "FEDFUNDS" in INTEREST_RATE_INDICATORS
        assert "DGS10" in INTEREST_RATE_INDICATORS
    
    def test_all_indicators_aggregation(self):
        """Test that ALL_INDICATORS contains all individual indicators."""
        expected_count = (
            len(GDP_INDICATORS) + len(EMPLOYMENT_INDICATORS) + 
            len(INFLATION_INDICATORS) + len(INTEREST_RATE_INDICATORS) +
            len(CONSUMER_INDICATORS) + len(HOUSING_INDICATORS)
        )
        
        assert len(ALL_INDICATORS) == expected_count
        
        # Test that specific indicators are in ALL_INDICATORS
        assert "GDP" in ALL_INDICATORS
        assert "UNRATE" in ALL_INDICATORS
        assert "FEDFUNDS" in ALL_INDICATORS
    
    def test_get_indicator_info(self):
        """Test the get_indicator_info function."""
        # Test known indicators
        gdp_info = get_indicator_info("GDP")
        assert gdp_info["category"] == "GDP"
        assert gdp_info["series_id"] == "GDP"
        
        unrate_info = get_indicator_info("UNRATE")
        assert unrate_info["category"] == "Employment"
        assert unrate_info["series_id"] == "UNRATE"
        
        fedfunds_info = get_indicator_info("FEDFUNDS")
        assert fedfunds_info["category"] == "Interest Rates"
        assert fedfunds_info["series_id"] == "FEDFUNDS"
        
        # Test unknown indicator
        unknown_info = get_indicator_info("UNKNOWN_SERIES")
        assert unknown_info["category"] == "Other"
        assert unknown_info["series_id"] == "UNKNOWN_SERIES"
    
    def test_no_duplicate_series_ids(self):
        """Test that there are no duplicate series IDs across categories."""
        all_series_ids = []
        
        for indicators in [GDP_INDICATORS, EMPLOYMENT_INDICATORS, INFLATION_INDICATORS,
                          INTEREST_RATE_INDICATORS, CONSUMER_INDICATORS, HOUSING_INDICATORS]:
            all_series_ids.extend(indicators.keys())
        
        # Check for duplicates
        assert len(all_series_ids) == len(set(all_series_ids)), "Duplicate series IDs found"
    
    def test_series_id_format(self):
        """Test that series IDs follow expected format."""
        for series_id in ALL_INDICATORS.keys():
            # FRED series IDs are typically uppercase alphanumeric
            assert series_id.isupper(), f"Series ID {series_id} should be uppercase"
            assert series_id.replace("_", "").isalnum(), f"Series ID {series_id} should be alphanumeric (with underscores)"
            assert len(series_id) >= 2, f"Series ID {series_id} seems too short"