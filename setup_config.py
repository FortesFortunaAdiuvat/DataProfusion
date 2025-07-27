#!/usr/bin/env python3
"""Setup script to configure API keys and application settings."""

from __future__ import annotations

import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.config.secrets import get_config


def main():
    """Interactive setup for API keys and configuration."""
    print("=== Economy Charts Configuration Setup ===\n")
    
    config = get_config()
    
    print("This script will help you configure API keys for data sources.")
    print("You can skip any service by pressing Enter without typing anything.\n")
    
    # FRED API Key
    print("1. FRED (Federal Reserve Economic Data)")
    print("   Get your free API key at: https://fred.stlouisfed.org/")
    current_fred = config.get_api_key("fred")
    if current_fred:
        print(f"   Current key: {current_fred[:8]}...")
    
    fred_key = input("   Enter FRED API key (or press Enter to skip): ").strip()
    if fred_key:
        config.set_api_key("fred", fred_key)
        print("   ✓ FRED API key saved")
    
    # CoinMarketCap API Key
    print("\n2. CoinMarketCap (Cryptocurrency Data)")
    print("   Get your API key at: https://coinmarketcap.com/api/")
    current_cmc = config.get_api_key("coinmarketcap")
    if current_cmc:
        print(f"   Current key: {current_cmc[:8]}...")
    
    cmc_key = input("   Enter CoinMarketCap API key (or press Enter to skip): ").strip()
    if cmc_key:
        config.set_api_key("coinmarketcap", cmc_key)
        print("   ✓ CoinMarketCap API key saved")
    
    # CoinGecko API Key
    print("\n3. CoinGecko (Cryptocurrency Data)")
    print("   Get your API key at: https://www.coingecko.com/en/api")
    current_gecko = config.get_api_key("coingecko")
    if current_gecko:
        print(f"   Current key: {current_gecko[:8]}...")
    
    gecko_key = input("   Enter CoinGecko API key (or press Enter to skip): ").strip()
    if gecko_key:
        config.set_api_key("coingecko", gecko_key)
        print("   ✓ CoinGecko API key saved")
    
    print("\n=== Configuration Complete ===")
    print(f"Configuration saved to: {config.config_file}")
    print("\nValidation results:")
    
    validation = config.validate_config()
    for service, is_valid in validation.items():
        status = "✓" if is_valid else "✗"
        print(f"  {status} {service}")
    
    print("\nYou can run this script again anytime to update your configuration.")
    print("Your API keys are stored securely and excluded from version control.")


if __name__ == "__main__":
    main()