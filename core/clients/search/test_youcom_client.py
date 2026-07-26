import pytest
import asyncio
from unittest.mock import Mock, patch
from core.clients.search.youcom_client import YouComClient


class TestYouComClient:
    """Test suite for YouComClient."""
    
    @pytest.fixture
    def client(self):
        """Create a YouComClient instance for testing."""
        return YouComClient(api_key="test_key")
    
    @pytest.fixture
    def keyless_client(self):
        """Create a keyless YouComClient instance for testing."""
        return YouComClient()
    
    def test_client_initialization_with_key(self):
        """Test client initialization with API key."""
        client = YouComClient(api_key="test_key")
        assert client.api_key == "test_key"
        assert "X-API-Key" in client.headers
        assert client.headers["X-API-Key"] == "test_key"
    
    def test_client_initialization_keyless(self):
        """Test client initialization without API key."""
        client = YouComClient()
        assert client.api_key == ""
        assert "X-API-Key" not in client.headers
    
    @patch.dict('os.environ', {'YDC_API_KEY': 'env_test_key'})
    def test_client_env_var_priority(self):
        """Test that environment variables are used when no API key is provided."""
        client = YouComClient()
        assert client.api_key == "env_test_key"
        assert client.headers["X-API-Key"] == "env_test_key"
    
    @patch('requests.get')
    @pytest.mark.asyncio
    async def test_search_success(self, mock_get, client):
        """Test successful search request."""
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {
            "results": {
                "web": [
                    {
                        "url": "https://example.com",
                        "title": "Test Result",
                        "description": "Test description"
                    }
                ]
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = await client.search("test query")
        
        assert result["data"]
        assert len(result["data"]) == 1
        assert result["data"][0]["url"] == "https://example.com"
        assert result["data"][0]["title"] == "Test Result"
        assert result["data"][0]["type"] == "web"
    
    @patch('requests.get')
    @pytest.mark.asyncio
    async def test_search_with_news_results(self, mock_get, client):
        """Test search with both web and news results."""
        # Mock response with both web and news
        mock_response = Mock()
        mock_response.json.return_value = {
            "results": {
                "web": [
                    {
                        "url": "https://example.com",
                        "title": "Web Result",
                        "description": "Web description"
                    }
                ],
                "news": [
                    {
                        "url": "https://news.example.com",
                        "title": "News Result", 
                        "description": "News description"
                    }
                ]
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = await client.search("test query")
        
        assert len(result["data"]) == 2
        assert result["data"][0]["type"] == "web"
        assert result["data"][1]["type"] == "news"
    
    @patch('requests.get')
    @pytest.mark.asyncio 
    async def test_search_http_error_401(self, mock_get, client):
        """Test handling of 401 authentication error."""
        import requests
        
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        
        mock_get.side_effect = requests.exceptions.HTTPError(response=mock_response)
        
        result = await client.search("test query")
        
        # Should return empty results on error
        assert result["data"] == []
    
    @patch('requests.get')
    @pytest.mark.asyncio
    async def test_search_rate_limit_429(self, mock_get, client):
        """Test handling of 429 rate limit error."""
        import requests
        
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.text = "Rate limit exceeded"
        
        mock_get.side_effect = requests.exceptions.HTTPError(response=mock_response)
        
        result = await client.search("test query")
        
        # Should return empty results on error
        assert result["data"] == []
    
    @patch('requests.get')
    @pytest.mark.asyncio
    async def test_search_network_error(self, mock_get, client):
        """Test handling of network connectivity error."""
        import requests
        
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")
        
        result = await client.search("test query")
        
        # Should return empty results on error
        assert result["data"] == []
    
    def test_rate_limiting_parameters(self, client):
        """Test rate limiting is properly configured."""
        assert client.rate_limit == 1  # Default rate limit
        assert hasattr(client, '_last_request_time')
    
    def test_headers_configuration(self, client):
        """Test that headers are properly configured."""
        assert client.headers["Content-Type"] == "application/json"
        assert "heurist-agent-framework" in client.headers["User-Agent"]
        assert client.headers["X-API-Key"] == "test_key"
    
    def test_keyless_headers_configuration(self, keyless_client):
        """Test headers for keyless client."""
        assert keyless_client.headers["Content-Type"] == "application/json"
        assert "heurist-agent-framework" in keyless_client.headers["User-Agent"]
        assert "X-API-Key" not in keyless_client.headers