"""Pytest configuration and shared fixtures."""

import pytest
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import tempfile
import shutil
from unittest.mock import Mock, patch

from app.config.secrets import SecureConfig
from app.data.fred_client import FREDDataMiner


@pytest.fixture
def temp_config_dir():
    """Create a temporary directory for test configuration."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def mock_config(temp_config_dir):
    """Create a mock configuration for testing."""
    config_file = temp_config_dir / "test_secrets.json"
    config = SecureConfig(str(config_file))
    config.set_api_key("fred", "test_api_key_123")
    config.set_config("database.cache_dir", str(temp_config_dir / "cache"))
    return config


@pytest.fixture
def sample_fred_series():
    """Sample FRED series data for testing."""
    dates = pd.date_range(start='2020-01-01', end='2020-12-31', freq='Q')
    values = [21427.7, 19520.1, 21170.3, 21494.7]  # Sample GDP values
    return pd.Series(values, index=dates, name='GDP').rename_axis('date')


@pytest.fixture
def sample_fred_metadata():
    """Sample FRED series metadata for testing."""
    return pd.Series({
        'id': 'GDP',
        'title': 'Gross Domestic Product',
        'units': 'Billions of Dollars',
        'frequency': 'Quarterly',
        'observation_start': '1947-01-01',
        'observation_end': '2023-07-01'
    })


@pytest.fixture
def mock_fred_api():
    """Mock the fredapi.Fred class."""
    with patch('app.data.fred_client.Fred') as mock_fred_class:
        yield mock_fred_class