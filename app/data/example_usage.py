"""Example usage of FRED data mining capabilities."""

from __future__ import annotations

import os
from .fred_client import FREDDataMiner
from .economic_indicators import GDP_INDICATORS, EMPLOYMENT_INDICATORS

def main():
    """Demonstrate FRED data retrieval and caching."""
    # Initialize the data miner
    # API key can be set via environment variable FRED_API_KEY
    miner = FREDDataMiner()
    
    print("Fetching GDP data...")
    gdp_data = miner.get_series("GDP", start_date="2020-01-01")
    print(f"GDP data points: {len(gdp_data)}")
    print(f"Latest GDP: {gdp_data.iloc[-1]:.2f} (Billions of $)")
    
    print("\nFetching unemployment rate...")
    unemployment = miner.get_series("UNRATE", start_date="2020-01-01")
    print(f"Current unemployment rate: {unemployment.iloc[-1]:.1f}%")
    
    print("\nFetching multiple indicators...")
    indicators = ["GDP", "UNRATE", "CPIAUCSL", "FEDFUNDS"]
    multi_data = miner.get_multiple_series(indicators, start_date="2020-01-01")
    print(f"Retrieved {len(multi_data.columns)} indicators")
    print(f"Date range: {multi_data.index.min()} to {multi_data.index.max()}")
    
    print("\nSearching for inflation-related series...")
    search_results = miner.search_series("inflation", limit=5)
    if not search_results.empty:
        print(f"Found {len(search_results)} results")
        for idx, row in search_results.head(3).iterrows():
            print(f"- {row['id']}: {row['title']}")

if __name__ == "__main__":
    main()