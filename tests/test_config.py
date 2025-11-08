"""
Tests for configuration module
"""

import pytest
import os
from src.data_gov_in.config import Config


class TestConfig:
    """Test Config class"""

    def test_default_config(self):
        """Test default configuration values"""
        config = Config()

        assert config.base_url == "https://api.data.gov.in"
        assert config.timeout == 30
        assert config.cache_enabled is True
        assert config.default_limit == 10

    def test_custom_config(self):
        """Test custom configuration values"""
        config = Config(
            api_key="test-key",
            timeout=60,
            cache_enabled=False
        )

        assert config.api_key == "test-key"
        assert config.timeout == 60
        assert config.cache_enabled is False

    def test_config_from_env(self, monkeypatch):
        """Test loading configuration from environment variables"""
        monkeypatch.setenv("DATA_GOV_IN_API_KEY", "env-api-key")
        monkeypatch.setenv("DATA_GOV_IN_TIMEOUT", "45")
        monkeypatch.setenv("DATA_GOV_IN_CACHE_ENABLED", "false")
        monkeypatch.setenv("DATA_GOV_IN_MAX_LIMIT", "200")

        config = Config.from_env()

        assert config.api_key == "env-api-key"
        assert config.timeout == 45
        assert config.cache_enabled is False
        assert config.max_limit == 200

    def test_config_validation_valid(self):
        """Test validation of valid configuration"""
        config = Config(
            timeout=30,
            rate_limit_calls=100,
            rate_limit_period=60,
            default_limit=10,
            max_limit=100
        )

        # Should not raise
        config.validate()

    def test_config_validation_invalid_timeout(self):
        """Test validation fails for invalid timeout"""
        config = Config(timeout=0)

        with pytest.raises(ValueError, match="timeout must be positive"):
            config.validate()

    def test_config_validation_invalid_rate_limit(self):
        """Test validation fails for invalid rate limit"""
        config = Config(rate_limit_calls=0)

        with pytest.raises(ValueError, match="rate_limit_calls must be positive"):
            config.validate()

    def test_config_validation_invalid_default_limit(self):
        """Test validation fails for invalid default limit"""
        config = Config(default_limit=0)

        with pytest.raises(ValueError, match="default_limit must be between"):
            config.validate()

        config = Config(default_limit=200, max_limit=100)

        with pytest.raises(ValueError, match="default_limit must be between"):
            config.validate()

    def test_config_validation_negative_cache_ttl(self):
        """Test validation fails for negative cache TTL"""
        config = Config(cache_ttl=-1)

        with pytest.raises(ValueError, match="cache_ttl must be non-negative"):
            config.validate()

    def test_config_validation_negative_retries(self):
        """Test validation fails for negative max retries"""
        config = Config(max_retries=-1)

        with pytest.raises(ValueError, match="max_retries must be non-negative"):
            config.validate()
