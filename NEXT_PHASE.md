# Next Phase: Data Retrieval and Integration

This document outlines how to extend the project beyond the sample chart by
ingesting real economic and financial data from a variety of sources.  The
goal is to expose students and researchers to macro‑ and micro‑economic
indicators as well as cryptocurrency market dynamics.

## 1. Federal Reserve Economic Data (FRED)

The Federal Reserve Bank of St. Louis offers a comprehensive API for its
**FRED** and **ALFRED** databases.  The API allows developers to retrieve
time‑series data such as GDP, unemployment rates, interest rates, and many
other indicators.  According to the FRED documentation, the web service
“allows developers to write programs and build applications that retrieve
economic data from the FRED and ALFRED websites” with customizable
requests by data source, release, category and series【604166066410163†L83-L90】.

### Steps

1. **Obtain an API key.**  Register for a free FRED API key at
   <https://fred.stlouisfed.org/>.  The key is optional for most calls but
   recommended for heavier usage.
2. **Install a Python client (optional).**  The
   `fredapi` library simplifies requests and automatically handles API keys.
   You can install it via:

       pip install fredapi

3. **Fetch data.**  Use `fredapi.Fred(api_key=<your_key>)` to create a client.
   For example, to retrieve U.S. GDP (series `GDP`):

       from fredapi import Fred
       fred = Fred(api_key="YOUR_API_KEY")
       gdp = fred.get_series("GDP")

4. **Integrate with Dash.**  Convert the returned pandas Series/DataFrame
   into a Plotly figure in `app/dash/charts.py` (see `sample_chart()` for
   reference) and expose it in the Dash layout.

## 2. SEC EDGAR Submissions and XBRL Data

The U.S. Securities and Exchange Commission provides RESTful APIs on
`data.sec.gov` that deliver JSON‑formatted EDGAR submission histories and
XBRL (eXtensible Business Reporting Language) data.  These APIs do not
require authentication【427360916219939†L169-L190】.  They include endpoints for a
company’s filing history, company facts, and aggregated frames of financial
metrics【427360916219939†L230-L266】.

### Steps

1. **Identify the company’s CIK.**  EDGAR uses a 10‑digit Central Index
   Key (CIK) to identify filers.  You can look up a company’s CIK via
   <https://www.sec.gov/edgar/search/>.
2. **Fetch submission history.**  To download a company’s latest filings,
   call:

       https://data.sec.gov/submissions/CIK##########.json

   Replace `##########` with the zero‑padded CIK.  This JSON contains
   metadata and a compact array of recent filings【427360916219939†L199-L210】.
3. **Retrieve company facts.**  To obtain all XBRL facts for a company:

       https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json

4. **Aggregate specific concepts.**  Use the `companyconcept` or `frames`
   endpoints to extract a single concept (e.g. net income) across time
   frames【427360916219939†L230-L266】.
5. **Parse and cache.**  Write helper functions under `app/data/` to parse
   these JSON structures into pandas DataFrames.  Due to the potentially large
   size of XBRL data, implement caching and respect the SEC’s
   rate-limit guidelines.  The APIs update throughout the day in real time【427360916219939†L190-L196】.

## 3. CoinMarketCap API (Cryptocurrency Data)

For cryptocurrency data, the **CoinMarketCap API** provides programmatic
access to prices, market capitalizations, trading volumes, and historical
data across thousands of cryptocurrencies【959207267423951†L32-L37】.  Features
include real‑time price tracking, historical OHLCV data, portfolio tracking
and more【959207267423951†L61-L68】.  Developers must register for an API key and
choose a subscription plan.  The free plan offers nine market data
endpoints with up to 10,000 API calls per month【959207267423951†L114-L127】.

### Steps

1. **Create an account and get an API key.**  Register on the
   CoinMarketCap developer portal and obtain your API key【959207267423951†L114-L120】.
2. **Select a plan.**  For proof‑of‑concept dashboards, the free tier
   (9 endpoints, 10 000 calls/month) suffices【959207267423951†L114-L127】.  For
   extended use or access to historical OHLCV endpoints, consider a paid plan.
3. **Construct requests.**  Use the `requests` library to call endpoints such
   as `/v1/cryptocurrency/listings/latest` or `/v1/cryptocurrency/quotes/latest`.
   Include your API key in the header.  For example:

       import requests

       def fetch_latest_listings(limit=100):
           url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
           headers = {"X-CMC_PRO_API_KEY": "YOUR_API_KEY", "Accept": "application/json"}
           params = {"start": 1, "limit": limit, "convert": "USD"}
           resp = requests.get(url, headers=headers, params=params)
           data = resp.json()
           return data

4. **Secure the API key.**  Never expose your API key in client‑side code.
   Instead, create a server‑side proxy in Flask that retrieves data and passes
   sanitised results to Dash components.  This approach protects your key and
   allows you to implement caching and rate‑limit handling【959207267423951†L129-L135】.

## 4. CoinGecko API (Cryptocurrency Data)

The **CoinGecko API** offers comprehensive cryptocurrency data and is free to
use.  To get started you need to create an account and obtain an API key【865428767777458†L49-L52】.  The
API exposes endpoints for listing cryptocurrencies, retrieving simple price
quotes and charting market data【865428767777458†L52-L58】.

### Steps

1. **Sign up and get an API key.**  Register on the CoinGecko website and
   obtain your personal API key【865428767777458†L49-L52】.
2. **Explore endpoints.**  Use endpoints like `/api/v3/coins/list` (list all
   coins), `/api/v3/simple/price` (current price for specified coins), and
   `/api/v3/coins/{id}/market_chart` (market chart data)【865428767777458†L55-L58】.
3. **Fetch data with `requests`.**  For example, to fetch Bitcoin prices for
   the last 30 days:

       import requests

       def fetch_bitcoin_history(days=30):
           url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
           params = {"vs_currency": "usd", "days": days}
           resp = requests.get(url, params=params)
           return resp.json()

4. **Integrate into Dash.**  Once fetched, transform the JSON into a pandas
   DataFrame and create a Plotly figure.  Add the chart to the Dash layout
   following the instructions in the **Contributing** guide.

## General tips

* **Caching:**  API calls—especially to EDGAR and crypto services—can be
  expensive or rate limited.  Implement caching layers (e.g. using
  `functools.lru_cache` or on‑disk cache) to avoid redundant calls.
* **Rate limits:**  Respect the rate limits of all external APIs.  For
  CoinMarketCap’s free plan, this is 10,000 requests per month【959207267423951†L114-L127】.
  CoinGecko also imposes per‑minute limits.  Use exponential backoff or
  request throttling as necessary.
* **Error handling:**  Wrap API calls in `try`/`except` blocks and handle
  network errors gracefully.  Provide fallback behaviour or user feedback
  when data cannot be fetched.
* **Environment variables:**  Store API keys in environment variables (e.g.
  `.env` files) and load them via `os.getenv`.  Do not commit secrets to
  version control.

With these guidelines you can expand the dashboard to cover a wide range
of economic and financial indicators, offering learners an interactive
experience across traditional markets and emerging crypto assets.