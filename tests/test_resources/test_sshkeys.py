import pytest
from unittest.mock import patch, MagicMock
from shadeform import ShadeformClient

@patch('shadeform.client.ShadeformClient.request')
def test_add_ssh_key(mock_request):
    """Test adding an SSH key."""
    mock_request.return_value = {
        "id": "key-123",
        "name": "test-key",
        "public_key": "ssh-rsa AAAA..."
    }
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.ssh_keys.add(
        name="test-key",
        public_key="ssh-rsa AAAA..."
    )
    
    mock_request.assert_called_once_with(
        "POST", 
        "/sshkeys/add", 
        json={
            "name": "test-key",
            "public_key": "ssh-rsa AAAA..."
        }
    )
    assert result["id"] == "key-123"
    assert result["name"] == "test-key"

@patch('shadeform.client.ShadeformClient.request')
def test_get_ssh_key_info(mock_request):
    """Test getting SSH key information."""
    mock_request.return_value = {
        "id": "key-123",
        "name": "test-key",
        "public_key": "ssh-rsa AAAA...",
        "created_at": "2025-03-05T12:00:00Z"
    }
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.ssh_keys.get_info("key-123")
    
    mock_request.assert_called_once_with("GET", "/sshkeys/key-123/info")
    assert result["id"] == "key-123"
    assert "created_at" in result

@patch('shadeform.client.ShadeformClient.request')
def test_delete_ssh_key(mock_request):
    """Test deleting an SSH key."""
    mock_request.return_value = None
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.ssh_keys.delete("key-123")
    
    mock_request.assert_called_once_with("POST", "/sshkeys/key-123/delete")
    assert result is None

@patch('shadeform.client.ShadeformClient.request')
def test_list_ssh_keys(mock_request):
    """Test listing SSH keys."""
    mock_request.return_value = [
        {
            "id": "key-123",
            "name": "test-key-1",
            "public_key": "ssh-rsa AAAA..."
        },
        {
            "id": "key-456",
            "name": "test-key-2",
            "public_key": "ssh-rsa BBBB..."
        }
    ]
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.ssh_keys.list_all()
    
    mock_request.assert_called_once_with("GET", "/sshkeys")
    assert len(result) == 2
    assert result[0]["id"] == "key-123"
    assert result[1]["id"] == "key-456"

@patch('shadeform.client.ShadeformClient.request')
def test_set_default_ssh_key(mock_request):
    """Test setting a default SSH key."""
    mock_request.return_value = {
        "id": "key-123",
        "name": "test-key",
        "is_default": True
    }
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.ssh_keys.set_default("key-123")
    
    mock_request.assert_called_once_with("POST", "/sshkeys/key-123/setdefault")
    assert result["is_default"] is True

@patch('shadeform.client.ShadeformClient.request')
def test_add_ssh_key_with_invalid_name(mock_request):
    """Test adding an SSH key with invalid name."""
    mock_request.side_effect = ValueError("Invalid SSH key name")
    
    client = ShadeformClient(api_key="test-api-key")
    with pytest.raises(ValueError):
        client.ssh_keys.add(name="", public_key="ssh-rsa AAAA...")

@patch('shadeform.client.ShadeformClient.request')
def test_add_ssh_key_with_invalid_key(mock_request):
    """Test adding an SSH key with invalid public key."""
    mock_request.side_effect = ValueError("Invalid SSH public key format")
    
    client = ShadeformClient(api_key="test-api-key")
    with pytest.raises(ValueError):
        client.ssh_keys.add(name="test-key", public_key="invalid-key")

@patch('shadeform.client.ShadeformClient.request')
def test_get_nonexistent_ssh_key(mock_request):
    """Test getting information about a non-existent SSH key."""
    mock_request.return_value = None
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.ssh_keys.get_info("nonexistent-key")
    
    mock_request.assert_called_once_with("GET", "/sshkeys/nonexistent-key/info")
    assert result is None