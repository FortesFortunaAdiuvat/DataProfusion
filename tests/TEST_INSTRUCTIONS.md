# Test Instructions

This document provides comprehensive instructions for running and understanding the test suite for the Economy Charts application.

## Overview

The test suite is organized into three main categories:

1. **Unit Tests** - Fast, isolated tests that use mocking (no external API calls)
2. **Integration Tests** - Tests that connect to real APIs and require valid credentials
3. **End-to-End Tests** - Full application tests (future implementation)

## Prerequisites

### Required Dependencies

Install test dependencies:

```bash
pip install -r requirements.txt
```

The test suite requires:
- `pytest` - Test framework
- `pytest-mock` - Mocking utilities
- `pandas` - Data manipulation (for test fixtures)

### API Keys for Integration Tests

Integration tests require a valid FRED API key. Set it up using one of these methods:

1. **Environment variable (recommended for CI/CD):**
   ```bash
   export FRED_API_KEY="your-fred-api-key-here"
   ```

2. **Configuration file:**
   ```bash
   python setup_config.py
   # Follow prompts to enter your FRED API key
   ```

3. **Manual config file creation:**
   ```bash
   mkdir -p config
   echo '{"api_keys": {"fred_api_key": "your-key-here"}}' > config/secrets.json
   ```

Get a free FRED API key at: https://fred.stlouisfed.org/

## Running Tests

### Quick Start

Use the test runner script for organized test execution:

```bash
# Run only unit tests (fast, no API calls)
python run_tests.py unit

# Run integration tests (requires API key and internet)
python run_tests.py integration

# Run all tests
python run_tests.py all
```

### Using pytest Directly

For more control, use pytest directly:

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_config.py -v

# Run specific test class
pytest tests/test_fred_client.py::TestFREDDataMiner -v

# Run specific test method
pytest tests/test_fred_integration.py::TestFREDIntegration::test_api_key_validation -v

# Run with coverage report
pytest tests/ --cov=app --cov-report=html

# Run tests in parallel (if pytest-xdist installed)
pytest tests/ -n auto
```

### Skipping Integration Tests

Integration tests can be skipped in several ways:

1. **Environment variable:**
   ```bash
   export SKIP_INTEGRATION_TESTS=1
   pytest tests/
   ```

2. **Pytest markers:**
   ```bash
   pytest tests/ -m "not integration"
   ```

3. **No API key:** Tests automatically skip if no FRED API key is found

## Test Categories

### Unit Tests

**Files:** `test_config.py`, `test_fred_client.py`, `test_economic_indicators.py`

**Purpose:** Test individual components in isolation using mocks

**Characteristics:**
- ✅ Fast execution (< 5 seconds total)
- ✅ No external dependencies
- ✅ Deterministic results
- ✅ Safe for CI/CD pipelines

**What they test:**
- Configuration management and API key handling
- FRED client caching and data processing logic
- Economic indicator constants and utilities
- Error handling and edge cases

**Run with:**
```bash
python run_tests.py unit
# or
pytest tests/test_config.py tests/test_fred_client.py tests/test_economic_indicators.py -v
```

### Integration Tests

**Files:** `test_fred_integration.py`

**Purpose:** Test real API connectivity and data quality

**Characteristics:**
- ⚠️ Requires internet connection
- ⚠️ Requires valid API key
- ⚠️ Slower execution (10-30 seconds)
- ⚠️ May fail due to network issues or API changes

**What they test:**
- API key validation
- Real data retrieval from FRED
- Rate limiting compliance
- Caching performance
- Error handling with real API responses
- Data format and quality validation

**Run with:**
```bash
python run_tests.py integration
# or
pytest tests/test_fred_integration.py -v -s
```

## Test Output and Interpretation

### Successful Test Run

```
tests/test_config.py::TestSecureConfig::test_config_creation PASSED
tests/test_fred_client.py::TestFREDDataMiner::test_initialization_with_config PASSED
tests/test_fred_integration.py::TestFREDIntegration::test_api_key_validation PASSED
✓ API key is valid. Retrieved 4 GDP data points.

========================= 15 passed in 12.34s =========================
```

### Common Failure Scenarios

#### 1. Missing API Key
```
SKIPPED [1] tests/test_fred_integration.py:20: Integration tests disabled or no API key
```
**Solution:** Set up FRED API key as described in Prerequisites

#### 2. Invalid API Key
```
FAILED tests/test_fred_integration.py::test_api_key_validation
E   pytest.fail: API key validation failed: 400 Client Error: Bad Request
```
**Solution:** Verify your FRED API key is correct and active

#### 3. Network Issues
```
FAILED tests/test_fred_integration.py::test_fetch_common_indicators
E   requests.exceptions.ConnectionError: Failed to establish a new connection
```
**Solution:** Check internet connection and FRED API status

#### 4. Rate Limiting
```
FAILED tests/test_fred_integration.py::test_rate_limiting_compliance
E   pytest.fail: Rate limit exceeded: 429 Too Many Requests
```
**Solution:** Wait a few minutes and retry, or check if you're exceeding API limits

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.13'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run unit tests
      run: python run_tests.py unit
    
    - name: Run integration tests
      env:
        FRED_API_KEY: ${{ secrets.FRED_API_KEY }}
      run: python run_tests.py integration
      if: env.FRED_API_KEY != ''
```

### Local Development Workflow

1. **During development:** Run unit tests frequently
   ```bash
   python run_tests.py unit
   ```

2. **Before committing:** Run all tests
   ```bash
   python run_tests.py all
   ```

3. **Before deployment:** Ensure integration tests pass
   ```bash
   python run_tests.py integration
   ```

## Writing New Tests

### Unit Test Example

```python
def test_new_feature(self, mock_fred_api, temp_config_dir):
    """Test description."""
    # Arrange
    mock_fred_api.some_method.return_value = expected_data
    
    # Act
    result = your_function()
    
    # Assert
    assert result == expected_result
    mock_fred_api.some_method.assert_called_once()
```

### Integration Test Example

```python
@pytest.mark.skipif(skip_integration, reason="Integration tests disabled")
def test_real_api_feature(self, fred_client):
    """Test with real API."""
    try:
        result = fred_client.some_real_method()
        assert isinstance(result, expected_type)
        print(f"✓ Feature working: {len(result)} items")
    except Exception as e:
        pytest.fail(f"Real API test failed: {e}")
```

### Test Naming Conventions

- **Unit tests:** `test_<functionality>`
- **Integration tests:** `test_<functionality>` (in integration test files)
- **Test classes:** `Test<ComponentName>`
- **Test files:** `test_<module_name>.py`

## Debugging Failed Tests

### Verbose Output

```bash
pytest tests/test_fred_integration.py -v -s --tb=long
```

### Run Single Test

```bash
pytest tests/test_fred_integration.py::test_api_key_validation -v -s
```

### Debug with Print Statements

Integration tests include helpful print statements:
```python
print(f"✓ API key is valid. Retrieved {len(result)} GDP data points.")
```

Use `-s` flag to see these outputs:
```bash
pytest tests/test_fred_integration.py -s
```

### Check Logs

The application logs to `logs/app.log` during tests. Check for detailed error information:

```bash
tail -f logs/app.log
```

## Performance Benchmarks

### Expected Test Times

- **Unit tests:** < 5 seconds
- **Integration tests:** 10-30 seconds (depending on network)
- **All tests:** < 45 seconds

### Cache Performance Test

The integration tests include a cache performance test that should show:
- First API call: 0.5-2.0 seconds
- Cached call: < 0.1 seconds

If caching isn't working properly, both calls will take similar time.

## Troubleshooting

### Common Issues

1. **Import errors:** Ensure you're running tests from the project root directory
2. **Permission errors:** Check that `data_cache/` directory is writable
3. **SSL errors:** Update certificates or check corporate firewall settings
4. **Memory errors:** Large datasets may require more RAM for integration tests

### Getting Help

1. Check the test output for specific error messages
2. Review the application logs in `logs/app.log`
3. Verify your API key is working by testing it manually at https://fred.stlouisfed.org/
4. Check FRED API status at https://fred.stlouisfed.org/docs/api/fred/

## Test Coverage

Generate a coverage report to see which code is tested:

```bash
pip install pytest-cov
pytest tests/ --cov=app --cov-report=html
open htmlcov/index.html  # View coverage report
```

Target coverage levels:
- **Unit tests:** > 90% for core modules
- **Integration tests:** > 70% for API interactions
- **Overall:** > 85% code coverage

## Future Enhancements

Planned test improvements:

1. **End-to-end tests** - Full application testing with Selenium
2. **Performance tests** - Load testing for data processing
3. **Security tests** - API key handling and data validation
4. **Mock API server** - Faster integration testing with controlled responses
5. **Property-based testing** - Using Hypothesis for edge case discovery