import pytest
from unittest.mock import patch, MagicMock
from shadeform import ShadeformClient

@patch('shadeform.client.ShadeformClient.request')
def test_create_instance(mock_request):
    """Test creating an instance."""
    mock_request.return_value = {"id": "instance-123", "name": "test-instance"}
    
    client = ShadeformClient(api_key="test-api-key")
    launch_config = {"type": "docker", "image": "pytorch/pytorch:latest"}
    
    result = client.instances.create(
        provider="aws",
        name="test-instance",
        region="us-west-2",
        instance_type="A100_80Gx1",
        launch_config=launch_config
    )
    
    mock_request.assert_called_once_with(
        "POST", 
        "/instances/create", 
        json={
            "provider": "aws",
            "name": "test-instance",
            "region": "us-west-2",
            "instance_type": "A100_80Gx1",
            "launch_configuration": launch_config
        }
    )
    assert result["id"] == "instance-123"

@patch('shadeform.client.ShadeformClient.request')
def test_create_instance_with_ssh_key(mock_request):
    """Test creating an instance with SSH key."""
    mock_request.return_value = {"id": "instance-123", "name": "test-instance"}
    
    client = ShadeformClient(api_key="test-api-key")
    launch_config = {"type": "docker", "image": "pytorch/pytorch:latest"}
    
    result = client.instances.create(
        provider="aws",
        name="test-instance",
        region="us-west-2",
        instance_type="A100_80Gx1",
        launch_config=launch_config,
        ssh_key_id="key-123"
    )
    
    mock_request.assert_called_once()
    args = mock_request.call_args
    assert args[1]["json"]["ssh_key_id"] == "key-123"

@patch('shadeform.client.ShadeformClient.request')
def test_create_instance_with_volumes(mock_request):
    """Test creating an instance with volumes."""
    mock_request.return_value = {"id": "instance-123", "name": "test-instance"}
    
    client = ShadeformClient(api_key="test-api-key")
    launch_config = {"type": "docker", "image": "pytorch/pytorch:latest"}
    volumes = [{"volume_id": "vol-123", "mount_path": "/data"}]
    
    result = client.instances.create(
        provider="aws",
        name="test-instance",
        region="us-west-2",
        instance_type="A100_80Gx1",
        launch_config=launch_config,
        volumes=volumes
    )
    
    mock_request.assert_called_once()
    args = mock_request.call_args
    assert args[1]["json"]["volumes"] == volumes

@patch('shadeform.client.ShadeformClient.request')
def test_get_instance_info(mock_request):
    """Test getting instance information."""
    mock_request.return_value = {"id": "instance-123", "status": "running"}
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.instances.get_info("instance-123")
    
    mock_request.assert_called_once_with("GET", "/instances/instance-123/info")
    assert result["status"] == "running"

@patch('shadeform.client.ShadeformClient.request')
def test_list_instances(mock_request):
    """Test listing instances."""
    mock_request.return_value = [
        {"id": "instance-123", "status": "running"},
        {"id": "instance-456", "status": "stopped"}
    ]
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.instances.list_all()
    
    mock_request.assert_called_once_with("GET", "/instances")
    assert len(result) == 2

@patch('shadeform.client.ShadeformClient.request')
def test_update_instance(mock_request):
    """Test updating an instance."""
    mock_request.return_value = {"success": True}
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.instances.update("instance-123", {"name": "new-name"})
    
    mock_request.assert_called_once_with(
        "POST",
        "/instances/instance-123/update",
        json={"name": "new-name"}
    )
    assert result["success"] is True

@patch('shadeform.client.ShadeformClient.request')
def test_delete_instance(mock_request):
    """Test deleting an instance."""
    mock_request.return_value = {"success": True, "message": "Instance scheduled for deletion"}
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.instances.delete("instance-123")
    
    mock_request.assert_called_once_with("POST", "/instances/instance-123/delete")
    assert result["success"] is True
    assert "message" in result

@patch('shadeform.client.ShadeformClient.request')
def test_restart_instance(mock_request):
    """Test restarting an instance."""
    mock_request.return_value = {"success": True, "status": "rebooting"}
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.instances.restart("instance-123")
    
    mock_request.assert_called_once_with("POST", "/instances/instance-123/restart")
    assert result["status"] == "rebooting"

@patch('shadeform.client.ShadeformClient.request')
def test_list_instance_types(mock_request):
    """Test listing instance types."""
    mock_request.return_value = [
        {
            "type": "A100_80Gx1",
            "provider": "aws",
            "memory_gb": 80,
            "vCPUs": 12,
            "hourly_price": 3.50
        }
    ]
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.instances.list_types()
    
    mock_request.assert_called_once_with("GET", "/instances/types")
    assert isinstance(result, list)
    assert result[0]["type"] == "A100_80Gx1"