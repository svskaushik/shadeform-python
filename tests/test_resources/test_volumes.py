import pytest
from unittest.mock import patch, MagicMock
from shadeform import ShadeformClient
from shadeform.error import ShadeformValidationError

@patch('shadeform.client.ShadeformClient.request')
def test_create_volume(mock_request):
    """Test creating a volume."""
    mock_request.return_value = {
        "id": "vol-123",
        "name": "test-volume",
        "size_gb": 100,
        "status": "creating"
    }
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.volumes.create(
        provider="aws",
        name="test-volume",
        volume_type="gp3",
        size_gb=100
    )
    
    mock_request.assert_called_once_with(
        "POST", 
        "/volumes/create", 
        json={
            "provider": "aws",
            "name": "test-volume",
            "volume_type": "gp3",
            "size_gb": 100
        }
    )
    assert result["id"] == "vol-123"
    assert result["size_gb"] == 100

@patch('shadeform.client.ShadeformClient.request')
def test_create_volume_from_snapshot(mock_request):
    """Test creating a volume from snapshot."""
    mock_request.return_value = {
        "id": "vol-123",
        "name": "test-volume",
        "size_gb": 100,
        "snapshot_id": "snap-456"
    }
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.volumes.create(
        provider="aws",
        name="test-volume",
        volume_type="gp3",
        size_gb=100,
        snapshot_id="snap-456"
    )
    
    mock_request.assert_called_once()
    args = mock_request.call_args
    assert args[1]["json"]["snapshot_id"] == "snap-456"

@patch('shadeform.client.ShadeformClient.request')
def test_get_volume_info(mock_request):
    """Test getting volume information."""
    mock_request.return_value = {
        "id": "vol-123",
        "name": "test-volume",
        "size_gb": 100,
        "status": "available"
    }
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.volumes.get_info("vol-123")
    
    mock_request.assert_called_once_with("GET", "/volumes/vol-123/info")
    assert result["status"] == "available"

@patch('shadeform.client.ShadeformClient.request')
def test_delete_volume(mock_request):
    """Test deleting a volume."""
    mock_request.return_value = {}
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.volumes.delete("vol-123")
    
    mock_request.assert_called_once_with("POST", "/volumes/vol-123/delete")
    assert result == {}

@patch('shadeform.client.ShadeformClient.request')
def test_list_volumes(mock_request):
    """Test listing volumes."""
    mock_request.return_value = [
        {
            "id": "vol-123",
            "name": "test-volume-1",
            "size_gb": 100
        },
        {
            "id": "vol-456",
            "name": "test-volume-2",
            "size_gb": 200
        }
    ]
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.volumes.list_all()
    
    mock_request.assert_called_once_with("GET", "/volumes")
    assert len(result) == 2
    assert result[0]["id"] == "vol-123"
    assert result[1]["size_gb"] == 200

@patch('shadeform.client.ShadeformClient.request')
def test_list_volume_types(mock_request):
    """Test listing volume types."""
    mock_request.return_value = [
        {
            "name": "gp3",
            "description": "General Purpose SSD",
            "min_size_gb": 1,
            "max_size_gb": 16384
        },
        {
            "name": "io2",
            "description": "Provisioned IOPS SSD",
            "min_size_gb": 4,
            "max_size_gb": 16384
        }
    ]
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.volumes.list_types()
    
    mock_request.assert_called_once_with("GET", "/volumes/types")
    assert len(result) == 2
    assert result[0]["name"] == "gp3"
    assert "min_size_gb" in result[0]

@patch('shadeform.client.ShadeformClient.request')
def test_create_volume_with_invalid_size(mock_request):
    """Test creating a volume with invalid size."""
    client = ShadeformClient(api_key="test-api-key")
    with pytest.raises(ShadeformValidationError, match="Invalid volume size"):
        client.volumes.create(
            provider="aws",
            name="test-volume",
            volume_type="gp3",
            size_gb=0
        )

@patch('shadeform.client.ShadeformClient.request')
@patch('shadeform.resources.volumes.validate_volume_type')  # Patch where it's used, not where it's defined
def test_create_volume_with_invalid_type(mock_validate_volume_type, mock_request):
    """Test creating a volume with invalid type."""
    # Set up the validation to fail
    mock_validate_volume_type.return_value = False
    
    client = ShadeformClient(api_key="test-api-key")
    with pytest.raises(ShadeformValidationError, match="Invalid volume type"):
        client.volumes.create(
            provider="aws",
            name="test-volume",
            volume_type="invalid-type",
            size_gb=100
        )
    
    # Verify validation was called with correct argument
    mock_validate_volume_type.assert_called_once_with("invalid-type")
    # Request should never be called if validation fails
    mock_request.assert_not_called()