"""Tests for secure configuration management."""

import pytest
import json
import os
from pathlib import Path
from unittest.mock import patch, Mock

from app.config.secrets import SecureConfig, get_config, get_api_key


class TestSecureConfig:
    """Test the SecureConfig class."""
    
    def test_config_creation(self, temp_config_dir):
        """Test that config file is created with defaults."""
        config_file = temp_config_dir / "test_config.json"
        config = SecureConfig(str(config_file))
        
        assert config_file.exists()
        
        with open(config_file) as f:
            data = json.load(f)
        
        assert "api_keys" in data
        assert "database" in data
        assert "logging" in data
    
    def test_api_key_storage_and_retrieval(self, temp_config_dir):
        """Test storing and retrieving API keys."""
        config_file = temp_config_dir / "test_config.json"
        config = SecureConfig(str(config_file))
        
        # Set API key
        config.set_api_key("fred", "test_key_123")
        
        # Retrieve API key
        retrieved_key = config.get_api_key("fred")
        assert retrieved_key == "test_key_123"
    
    @patch.dict(os.environ, {'FRED_API_KEY': 'env_key_456'})
    def test_environment_variable_priority(self, temp_config_dir):
        """Test that environment variables take priority over config file."""
        config_file = temp_config_dir / "test_config.json"
        config = SecureConfig(str(config_file))
        
        # Set API key in config file
        config.set_api_key("fred", "config_key_123")
        
        # Environment variable should take priority
        retrieved_key = config.get_api_key("fred")
        assert retrieved_key == "env_key_456"
    
    def test_missing_api_key(self, temp_config_dir):
        """Test behavior when API key is missing."""
        config_file = temp_config_dir / "test_config.json"
        config = SecureConfig(str(config_file))
        
        retrieved_key = config.get_api_key("nonexistent")
        assert retrieved_key is None
    
    def test_config_validation(self, temp_config_dir):
        """Test configuration validation."""
        config_file = temp_config_dir / "test_config.json"
        config = SecureConfig(str(config_file))
        
        # Initially, no API keys should be valid
        validation = config.validate_config()
        assert not validation["fred_api_key"]
        assert not validation["coinmarketcap_api_key"]
        
        # Add a valid API key
        config.set_api_key("fred", "valid_key")
        validation = config.validate_config()
        assert validation["fred_api_key"]
    
    def test_dot_notation_config(self, temp_config_dir):
        """Test dot notation for nested configuration."""
        config_file = temp_config_dir / "test_config.json"
        config = SecureConfig(str(config_file))
        
        # Set nested config
        config.set_config("database.cache_dir", "/custom/cache")
        
        # Retrieve with dot notation
        cache_dir = config.get_config("database.cache_dir")
        assert cache_dir == "/custom/cache"
        
        # Test default value
        missing_value = config.get_config("missing.key", "default")
        assert missing_value == "default"


class TestGlobalConfig:
    """Test global configuration functions."""
    
    def test_get_config_singleton(self):
        """Test that get_config returns the same instance."""
        config1 = get_config()
        config2 = get_config()
        assert config1 is config2
    
    @patch('app.config.secrets.get_config')
    def test_get_api_key_convenience(self, mock_get_config):
        """Test the convenience get_api_key function."""
        mock_config = Mock()
        mock_config.get_api_key.return_value = "test_key"
        mock_get_config.return_value = mock_config
        
        result = get_api_key("fred")
        assert result == "test_key"
        mock_config.get_api_key.assert_called_once_with("fred")