"""Common economic indicators and their FRED series IDs."""

from __future__ import annotations

# GDP and Economic Growth
GDP_INDICATORS = {
    "GDP": "GDP",  # Gross Domestic Product
    "GDPC1": "GDPC1",  # Real GDP
    "GDPPOT": "GDPPOT",  # Real Potential GDP
    "NYGDPMKTPCDWLD": "NYGDPMKTPCDWLD",  # World GDP per capita
}

# Employment and Labor
EMPLOYMENT_INDICATORS = {
    "UNRATE": "UNRATE",  # Unemployment Rate
    "CIVPART": "CIVPART",  # Labor Force Participation Rate
    "EMRATIO": "EMRATIO",  # Employment-Population Ratio
    "PAYEMS": "PAYEMS",  # All Employees: Total Nonfarm Payrolls
    "AWHMAN": "AWHMAN",  # Average Weekly Hours: Manufacturing
}

# Inflation and Prices
INFLATION_INDICATORS = {
    "CPIAUCSL": "CPIAUCSL",  # Consumer Price Index
    "CPILFESL": "CPILFESL",  # Core CPI (less food and energy)
    "PCEPI": "PCEPI",  # PCE Price Index
    "PCEPILFE": "PCEPILFE",  # Core PCE Price Index
    "DFEDTARU": "DFEDTARU",  # Federal Reserve 2% Inflation Target
}

# Interest Rates and Monetary Policy
INTEREST_RATE_INDICATORS = {
    "FEDFUNDS": "FEDFUNDS",  # Federal Funds Rate
    "DGS10": "DGS10",  # 10-Year Treasury Rate
    "DGS2": "DGS2",  # 2-Year Treasury Rate
    "DGS3MO": "DGS3MO",  # 3-Month Treasury Rate
    "MORTGAGE30US": "MORTGAGE30US",  # 30-Year Fixed Rate Mortgage
}

# Consumer Spending and Confidence
CONSUMER_INDICATORS = {
    "PCE": "PCE",  # Personal Consumption Expenditures
    "PSAVERT": "PSAVERT",  # Personal Saving Rate
    "UMCSENT": "UMCSENT",  # Consumer Sentiment Index
    "RRSFS": "RRSFS",  # Retail Sales
}

# Housing Market
HOUSING_INDICATORS = {
    "HOUST": "HOUST",  # Housing Starts
    "PERMIT": "PERMIT",  # Building Permits
    "CSUSHPISA": "CSUSHPISA",  # Case-Shiller Home Price Index
    "EXHOSLUSM495S": "EXHOSLUSM495S",  # Existing Home Sales
}

# All indicators combined
ALL_INDICATORS = {
    **GDP_INDICATORS,
    **EMPLOYMENT_INDICATORS,
    **INFLATION_INDICATORS,
    **INTEREST_RATE_INDICATORS,
    **CONSUMER_INDICATORS,
    **HOUSING_INDICATORS,
}

def get_indicator_info(series_id: str) -> dict[str, str]:
    """Get category and description for a series ID."""
    for category_name, indicators in [
        ("GDP", GDP_INDICATORS),
        ("Employment", EMPLOYMENT_INDICATORS),
        ("Inflation", INFLATION_INDICATORS),
        ("Interest Rates", INTEREST_RATE_INDICATORS),
        ("Consumer", CONSUMER_INDICATORS),
        ("Housing", HOUSING_INDICATORS),
    ]:
        if series_id in indicators:
            return {"category": category_name, "series_id": series_id}
    
    return {"category": "Other", "series_id": series_id}