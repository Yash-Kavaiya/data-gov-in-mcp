"""
Tests for API client
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import httpx

from src.data_gov_in.api_client import DataGovInClient, RateLimiter
from src.data_gov_in.config import Config
from src.data_gov_in.exceptions import (
    APIKeyMissingError,
    ResourceNotFoundError,
    RateLimitError,
    InvalidParameterError,
)


class TestRateLimiter:
    """Test rate limiter functionality"""

    def test_rate_limiter_allows_calls_within_limit(self):
        """Test that calls within limit are allowed"""
        limiter = RateLimiter(max_calls=5, period=1)

        # Should not raise or sleep
        for _ in range(5):
            limiter.wait_if_needed()

    def test_rate_limiter_enforces_limit(self):
        """Test that rate limiter enforces the limit"""
        limiter = RateLimiter(max_calls=2, period=1)

        limiter.wait_if_needed()
        limiter.wait_if_needed()

        # Third call should trigger sleep
        with patch('time.sleep') as mock_sleep:
            limiter.wait_if_needed()
            assert mock_sleep.called


class TestDataGovInClient:
    """Test DataGovInClient"""

    def test_client_initialization_without_api_key(self):
        """Test client initialization without API key"""
        config = Config(api_key=None)
        client = DataGovInClient(config)
        assert client.config.api_key is None

    def test_client_initialization_with_api_key(self):
        """Test client initialization with API key"""
        config = Config(api_key="test-key")
        client = DataGovInClient(config)
        assert client.config.api_key == "test-key"

    def test_missing_api_key_raises_error(self):
        """Test that missing API key raises error on request"""
        config = Config(api_key=None)
        client = DataGovInClient(config)

        with pytest.raises(APIKeyMissingError):
            client.get_resource("test-resource")

    def test_invalid_limit_raises_error(self):
        """Test that invalid limit raises error"""
        config = Config(api_key="test-key", max_limit=100)
        client = DataGovInClient(config)

        with pytest.raises(InvalidParameterError):
            client.get_resource("test-resource", limit=200)

    @patch('httpx.Client.get')
    def test_successful_request(self, mock_get):
        """Test successful API request"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "records": [{"id": 1, "name": "test"}],
            "total": 1
        }
        mock_get.return_value = mock_response

        config = Config(api_key="test-key", cache_enabled=False)
        client = DataGovInClient(config)

        result = client.get_resource("test-resource", limit=10)

        assert "records" in result
        assert len(result["records"]) == 1
        mock_get.assert_called_once()

    @patch('httpx.Client.get')
    def test_404_error_raises_resource_not_found(self, mock_get):
        """Test that 404 raises ResourceNotFoundError"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        config = Config(api_key="test-key", cache_enabled=False)
        client = DataGovInClient(config)

        with pytest.raises(ResourceNotFoundError):
            client.get_resource("non-existent")

    @patch('httpx.Client.get')
    def test_429_error_raises_rate_limit(self, mock_get):
        """Test that 429 raises RateLimitError"""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_get.return_value = mock_response

        config = Config(api_key="test-key", cache_enabled=False)
        client = DataGovInClient(config)

        with pytest.raises(RateLimitError):
            client.get_resource("test-resource")

    @patch('httpx.Client.get')
    def test_caching_works(self, mock_get):
        """Test that caching works correctly"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"records": [], "total": 0}
        mock_get.return_value = mock_response

        config = Config(api_key="test-key", cache_enabled=True, cache_ttl=3600)
        client = DataGovInClient(config)

        # First request
        client.get_resource("test-resource", limit=10)

        # Second request should use cache
        result = client.get_resource("test-resource", limit=10)

        # Should only call API once
        assert mock_get.call_count == 1
        assert result is not None

    @patch('httpx.Client.get')
    def test_retry_logic(self, mock_get):
        """Test retry logic on network errors"""
        # First call fails, second succeeds
        mock_get.side_effect = [
            httpx.TimeoutException("Timeout"),
            Mock(status_code=200, json=lambda: {"records": [], "total": 0})
        ]

        config = Config(api_key="test-key", cache_enabled=False, max_retries=2, retry_delay=0.1)
        client = DataGovInClient(config)

        result = client.get_resource("test-resource")

        assert result is not None
        assert mock_get.call_count == 2

    def test_get_resource_fields(self):
        """Test getting resource fields"""
        config = Config(api_key="test-key", cache_enabled=False)
        client = DataGovInClient(config)

        with patch.object(client, '_make_request') as mock_request:
            mock_request.return_value = {
                "fields": [
                    {"id": "name", "type": "text"},
                    {"id": "value", "type": "number"}
                ],
                "records": []
            }

            fields = client.get_resource_fields("test-resource")

            assert len(fields) == 2
            assert fields[0]["id"] == "name"

    def test_context_manager(self):
        """Test client as context manager"""
        config = Config(api_key="test-key")

        with DataGovInClient(config) as client:
            assert client is not None

        # Client should be closed after context
        assert client.client.is_closed
