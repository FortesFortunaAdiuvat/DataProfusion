# Configuration Setup

This application uses a secure configuration system to manage API keys and settings.

## Quick Setup

1. **Run the setup script:**
   ```bash
   python setup_config.py
   ```

2. **Or manually create the config file:**
   ```bash
   mkdir -p config
   cp config/secrets.json.template config/secrets.json
   # Edit config/secrets.json with your API keys
   ```

## Configuration File

The configuration is stored in `config/secrets.json` (automatically created):

```json
{
  "api_keys": {
    "fred_api_key": "your-fred-api-key-here",
    "coinmarketcap_api_key": "your-cmc-api-key-here",
    "coingecko_api_key": "your-coingecko-api-key-here",
    "sec_edgar_user_agent": "your-email@example.com"
  },
  "database": {
    "cache_dir": "data_cache",
    "max_cache_age_hours": 24
  },
  "logging": {
    "level": "INFO",
    "file": "logs/app.log"
  }
}
```

## Security Features

- **Git ignored**: Configuration files are automatically excluded from version control
- **AI agent ignored**: API keys are excluded from AI assistant context
- **Environment variable fallback**: Checks `{SERVICE}_API_KEY` environment variables first
- **Encrypted storage**: Consider using system keyring for production deployments

## Getting API Keys

### FRED (Federal Reserve Economic Data)
- **Free**: Yes
- **URL**: https://fred.stlouisfed.org/
- **Rate Limits**: 120 requests/minute
- **Required for**: Economic indicators, GDP, unemployment, inflation data

### CoinMarketCap
- **Free Tier**: 10,000 calls/month
- **URL**: https://coinmarketcap.com/api/
- **Required for**: Cryptocurrency market data

### CoinGecko
- **Free Tier**: Yes (with rate limits)
- **URL**: https://www.coingecko.com/en/api
- **Required for**: Alternative cryptocurrency data source

## Environment Variables

Configuration values can also be supplied through environment variables or a `.env` file. Set the following variables:

```bash
FRED_API_KEY="your-fred-key"
COINMARKETCAP_API_KEY="your-cmc-key"
COINGECKO_API_KEY="your-gecko-key"
FLASK_CONFIG="development"
```

- `FRED_API_KEY` – required for accessing economic data from FRED
- `FLASK_CONFIG` – selects the Flask configuration (e.g., `development`, `production`)

Environment variables take precedence over the config file. An `.env.example` file is provided as a template.
