import os
import pytest
import requests
from unittest.mock import patch, MagicMock
from shadeform import ShadeformClient, ShadeformError, ShadeformAPIError

def test_client_initialization_with_api_key():
    """Test client initialization with API key."""
    client = ShadeformClient(api_key="test-api-key")
    assert client.api_key == "test-api-key"
    assert client.jwt_token is None

def test_client_initialization_with_jwt():
    """Test client initialization with JWT token."""
    client = ShadeformClient(jwt_token="test-jwt-token")
    assert client.jwt_token == "test-jwt-token"
    assert client.api_key is None

def test_client_initialization_with_env_vars():
    """Test client initialization with environment variables."""
    with patch.dict(os.environ, {"SHADEFORM_API_KEY": "env-api-key"}):
        client = ShadeformClient()
        assert client.api_key == "env-api-key"

def test_client_initialization_without_auth():
    """Test client initialization fails without auth credentials."""
    with pytest.raises(ShadeformError, match="Either API key or JWT token must be provided"):
        ShadeformClient()

def test_client_headers_with_api_key():
    """Test client sets correct headers with API key."""
    client = ShadeformClient(api_key="test-api-key")
    assert client.session.headers["X-API-Key"] == "test-api-key"
    assert client.session.headers["Content-Type"] == "application/json"
    assert "Authorization" not in client.session.headers

def test_client_headers_with_jwt():
    """Test client sets correct headers with JWT token."""
    client = ShadeformClient(jwt_token="test-jwt-token")
    assert client.session.headers["Authorization"] == "Bearer test-jwt-token"
    assert client.session.headers["Content-Type"] == "application/json"
    assert "X-API-Key" not in client.session.headers

@patch('requests.Session.request')
def test_client_request_success(mock_request):
    """Test successful client request."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'{"key": "value"}'
    mock_response.json.return_value = {"key": "value"}
    mock_request.return_value = mock_response
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.request("GET", "/test")
    
    assert result == {"key": "value"}
    mock_request.assert_called_once()
    args, kwargs = mock_request.call_args
    assert args[0] == "GET"
    assert args[1] == "https://api.shadeform.ai/v1/test"

@patch('requests.Session.request')
def test_client_request_no_content(mock_request):
    """Test client request with no content returns empty dict."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b''
    mock_request.return_value = mock_response
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.request("GET", "/test")
    
    assert result == {}

@patch('requests.Session.request')
def test_client_request_204_status(mock_request):
    """Test client request with 204 status returns None."""
    mock_response = MagicMock()
    mock_response.status_code = 204
    mock_request.return_value = mock_response
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.request("POST", "/test")
    
    assert result is None

@patch('requests.Session.request')
def test_client_request_error(mock_request):
    """Test client request with error response."""
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.content = b'{"message": "Bad Request"}'
    mock_response.json.return_value = {"message": "Bad Request"}
    
    def raise_http_error(*args, **kwargs):
        raise requests.exceptions.HTTPError("400 Bad Request")
    
    mock_response.raise_for_status.side_effect = raise_http_error
    mock_request.return_value = mock_response
    
    client = ShadeformClient(api_key="test-api-key")
    
    with pytest.raises(ShadeformAPIError) as excinfo:
        client.request("GET", "/test")
    
    assert "API Error 400: Bad Request" in str(excinfo.value)

@patch('requests.Session.request')
def test_client_request_with_query_params(mock_request):
    """Test client request with query parameters."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'{"key": "value"}'
    mock_response.json.return_value = {"key": "value"}
    mock_request.return_value = mock_response
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.request("GET", "/test", params={"filter": "active"})
    
    mock_request.assert_called_once()
    args, kwargs = mock_request.call_args
    assert kwargs.get("params") == {"filter": "active"}

@patch('requests.Session.request')
def test_client_request_with_json_body(mock_request):
    """Test client request with JSON body."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'{"id": "123"}'
    mock_response.json.return_value = {"id": "123"}
    mock_request.return_value = mock_response
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.request("POST", "/test", json={"name": "test"})
    
    mock_request.assert_called_once()
    args, kwargs = mock_request.call_args
    assert kwargs.get("json") == {"name": "test"}