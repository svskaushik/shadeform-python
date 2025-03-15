import pytest
from unittest.mock import patch, MagicMock
from shadeform import ShadeformClient

@patch('shadeform.client.ShadeformClient.request')
def test_list_templates(mock_request):
    """Test listing templates."""
    mock_request.return_value = [
        {
            "id": "tmpl-123",
            "name": "pytorch-template",
            "description": "PyTorch environment"
        },
        {
            "id": "tmpl-456",
            "name": "tensorflow-template",
            "description": "TensorFlow environment"
        }
    ]
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.templates.list_all()
    
    mock_request.assert_called_once_with("GET", "/templates")
    assert len(result) == 2
    assert result[0]["name"] == "pytorch-template"

@patch('shadeform.client.ShadeformClient.request')
def test_get_template_info(mock_request):
    """Test getting template information."""
    mock_request.return_value = {
        "id": "tmpl-123",
        "name": "pytorch-template",
        "description": "PyTorch environment",
        "launch_configuration": {
            "type": "docker",
            "image": "pytorch/pytorch:latest"
        }
    }
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.templates.get_info("tmpl-123")
    
    mock_request.assert_called_once_with("GET", "/templates/tmpl-123/info")
    assert result["name"] == "pytorch-template"
    assert "launch_configuration" in result

@patch('shadeform.client.ShadeformClient.request')
def test_get_featured_templates(mock_request):
    """Test getting featured templates."""
    mock_request.return_value = [
        {
            "id": "tmpl-123",
            "name": "pytorch-template",
            "featured": True
        },
        {
            "id": "tmpl-456",
            "name": "tensorflow-template",
            "featured": True
        }
    ]
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.templates.list_featured()
    
    mock_request.assert_called_once_with("GET", "/templates/featured")
    assert len(result) == 2
    assert all(t["featured"] for t in result)

@patch('shadeform.client.ShadeformClient.request')
def test_save_template(mock_request):
    """Test saving a template."""
    mock_request.return_value = {
        "id": "tmpl-123",
        "name": "custom-template",
        "description": "Custom PyTorch environment"
    }
    
    client = ShadeformClient(api_key="test-api-key")
    launch_config = {"type": "docker", "image": "pytorch/pytorch:latest"}
    
    result = client.templates.save(
        name="custom-template",
        description="Custom PyTorch environment",
        config=launch_config
    )
    
    mock_request.assert_called_once_with(
        "POST", 
        "/templates/save", 
        json={
            "name": "custom-template",
            "description": "Custom PyTorch environment",
            "launch_configuration": launch_config
        }
    )
    assert result["id"] == "tmpl-123"

@patch('shadeform.client.ShadeformClient.request')
def test_save_template_minimal(mock_request):
    """Test saving a template with minimal parameters."""
    mock_request.return_value = {
        "id": "tmpl-123",
        "name": "minimal-template"
    }
    
    client = ShadeformClient(api_key="test-api-key")
    launch_config = {"type": "docker", "image": "pytorch/pytorch:latest"}
    
    result = client.templates.save(
        name="minimal-template",
        description="Minimal template",
        config=launch_config
    )
    
    mock_request.assert_called_once()
    args = mock_request.call_args
    assert "provider" not in args[1]["json"]
    assert "instance_type" not in args[1]["json"]

@patch('shadeform.client.ShadeformClient.request')
def test_update_template(mock_request):
    """Test updating a template."""
    mock_request.return_value = {
        "id": "tmpl-123",
        "name": "updated-template",
        "description": "Updated description"
    }
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.templates.update(
        "tmpl-123",
        {
            "name": "updated-template",
            "description": "Updated description"
        }
    )
    
    mock_request.assert_called_once_with(
        "POST", 
        "/templates/tmpl-123/update",
        json={
            "name": "updated-template",
            "description": "Updated description"
        }
    )
    assert result["name"] == "updated-template"

@patch('shadeform.client.ShadeformClient.request')
def test_delete_template(mock_request):
    """Test deleting a template."""
    mock_request.return_value = {}
    
    client = ShadeformClient(api_key="test-api-key")
    result = client.templates.delete("tmpl-123")
    
    mock_request.assert_called_once_with("POST", "/templates/tmpl-123/delete")
    assert result == {}

@patch('shadeform.client.ShadeformClient.request')
def test_save_template_with_invalid_name(mock_request):
    """Test saving a template with invalid name."""
    mock_request.side_effect = ValueError("Invalid template name")
    
    client = ShadeformClient(api_key="test-api-key")
    launch_config = {"type": "docker", "image": "pytorch/pytorch:latest"}
    
    with pytest.raises(ValueError):
        client.templates.save(
            name="",
            description="Invalid template",
            config=launch_config
        )

@patch('shadeform.client.ShadeformClient.request')
def test_save_template_with_invalid_config(mock_request):
    """Test saving a template with invalid launch configuration."""
    mock_request.side_effect = ValueError("Invalid launch configuration")
    
    client = ShadeformClient(api_key="test-api-key")
    
    with pytest.raises(ValueError):
        client.templates.save(
            name="invalid-template",
            description="Invalid template",
            config={}  # Empty config
        )