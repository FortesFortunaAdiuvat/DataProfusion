"""Secure configuration management for API keys and secrets."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class SecureConfig:
    """Manages secure configuration including API keys."""
    
    def __init__(self, config_file: str = "config/secrets.json"):
        """Initialize secure configuration.
        
        Parameters
        ----------
        config_file : str
            Path to the JSON configuration file containing secrets
        """
        self.config_file = Path(config_file)
        self.config_dir = self.config_file.parent
        self._config_data: Dict[str, Any] = {}
        
        # Ensure config directory exists
        self.config_dir.mkdir(exist_ok=True)
        
        # Load configuration
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from file if it exists."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self._config_data = json.load(f)
                logger.info(f"Loaded configuration from {self.config_file}")
            except (json.JSONDecodeError, IOError) as e:
                logger.error(f"Failed to load config file {self.config_file}: {e}")
                self._config_data = {}
        else:
            logger.info(f"Config file {self.config_file} not found, using defaults")
            self._create_default_config()
    
    def _create_default_config(self) -> None:
        """Create a default configuration file template."""
        default_config = {
            "api_keys": {
                "fred_api_key": "",
                "coinmarketcap_api_key": "",
                "coingecko_api_key": "",
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
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            
            logger.info(f"Created default config file at {self.config_file}")
            logger.warning(f"Please edit {self.config_file} and add your API keys")
            
            self._config_data = default_config
            
        except IOError as e:
            logger.error(f"Failed to create default config file: {e}")
            self._config_data = default_config
    
    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a service, checking environment variables first.
        
        Parameters
        ----------
        service : str
            Service name (e.g., 'fred', 'coinmarketcap', 'coingecko')
            
        Returns
        -------
        str or None
            API key if found, None otherwise
        """
        # Check environment variables first
        env_var_name = f"{service.upper()}_API_KEY"
        api_key = os.getenv(env_var_name)
        
        if api_key:
            logger.debug(f"Using {service} API key from environment variable")
            return api_key
        
        # Fall back to config file
        config_key = f"{service.lower()}_api_key"
        api_key = self._config_data.get("api_keys", {}).get(config_key)
        
        if api_key:
            logger.debug(f"Using {service} API key from config file")
            return api_key
        
        logger.warning(f"No API key found for {service}")
        return None
    
    def set_api_key(self, service: str, api_key: str) -> None:
        """Set API key for a service in the config file.
        
        Parameters
        ----------
        service : str
            Service name
        api_key : str
            API key to store
        """
        if "api_keys" not in self._config_data:
            self._config_data["api_keys"] = {}
        
        config_key = f"{service.lower()}_api_key"
        self._config_data["api_keys"][config_key] = api_key
        
        self._save_config()
        logger.info(f"Updated API key for {service}")
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.
        
        Parameters
        ----------
        key : str
            Configuration key (supports dot notation, e.g., 'database.cache_dir')
        default : Any
            Default value if key not found
            
        Returns
        -------
        Any
            Configuration value
        """
        keys = key.split('.')
        value = self._config_data
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set_config(self, key: str, value: Any) -> None:
        """Set a configuration value.
        
        Parameters
        ----------
        key : str
            Configuration key (supports dot notation)
        value : Any
            Value to set
        """
        keys = key.split('.')
        config = self._config_data
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
        self._save_config()
    
    def _save_config(self) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self._config_data, f, indent=2)
            logger.debug(f"Saved configuration to {self.config_file}")
        except IOError as e:
            logger.error(f"Failed to save config file: {e}")
    
    def validate_config(self) -> Dict[str, bool]:
        """Validate that required configuration is present.
        
        Returns
        -------
        dict
            Dictionary mapping service names to whether they have valid config
        """
        validation_results = {}
        
        # Check API keys
        services = ['fred', 'coinmarketcap', 'coingecko']
        for service in services:
            api_key = self.get_api_key(service)
            validation_results[f"{service}_api_key"] = bool(api_key and api_key.strip())
        
        # Check other required config
        cache_dir = self.get_config('database.cache_dir')
        validation_results['cache_dir'] = bool(cache_dir)
        
        return validation_results


# Global configuration instance
_config_instance: Optional[SecureConfig] = None


def get_config() -> SecureConfig:
    """Get the global configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = SecureConfig()
    return _config_instance


def get_api_key(service: str) -> Optional[str]:
    """Convenience function to get an API key."""
    return get_config().get_api_key(service)