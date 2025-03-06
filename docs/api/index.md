# Shadeform Python SDK API Reference

This documentation provides detailed information about all the classes and methods available in the Shadeform Python SDK.

## Core Components

### ShadeformClient

The main client class that provides access to all API functionality.

```python
from shadeform import ShadeformClient

client = ShadeformClient(
    api_key="your-api-key",  # or use jwt_token="your-jwt-token"
    base_url="https://api.shadeform.ai/v1"  # optional
)
```

## Resource Clients

The SDK provides several resource clients, each managing a specific type of resource:

### InstanceClient

Manage GPU instances:
```python
# Access through the main client
client.instances

# Available methods
client.instances.create(...)      # Create a new instance
client.instances.get_info(...)    # Get instance information
client.instances.list_all()       # List all instances
client.instances.update(...)      # Update an instance
client.instances.delete(...)      # Delete an instance
client.instances.restart(...)     # Restart an instance
client.instances.list_types()     # List available instance types
```

### SSHKeyClient

Manage SSH keys:
```python
# Access through the main client
client.ssh_keys

# Available methods
client.ssh_keys.add(...)         # Add a new SSH key
client.ssh_keys.get_info(...)    # Get SSH key information
client.ssh_keys.delete(...)      # Delete an SSH key
client.ssh_keys.list_all()       # List all SSH keys
client.ssh_keys.set_default(...) # Set a default SSH key
```

### VolumeClient

Manage storage volumes:
```python
# Access through the main client
client.volumes

# Available methods
client.volumes.create(...)       # Create a new volume
client.volumes.get_info(...)     # Get volume information
client.volumes.delete(...)       # Delete a volume
client.volumes.list_all()        # List all volumes
client.volumes.list_types()      # List available volume types
```

### TemplateClient

Manage deployment templates:
```python
# Access through the main client
client.templates

# Available methods
client.templates.list_all()      # List all templates
client.templates.get_info(...)   # Get template information
client.templates.get_featured()  # Get featured templates
client.templates.save(...)       # Save a new template
client.templates.update(...)     # Update a template
client.templates.delete(...)     # Delete a template
```

## Utility Classes

### LaunchConfiguration

Helper class for creating launch configurations:
```python
from shadeform import LaunchConfiguration

# Create a Docker-based configuration
docker_config = LaunchConfiguration.docker(
    image="pytorch/pytorch:latest",
    command="python train.py",
    env_vars={"BATCH_SIZE": "64"},
    ports=[8080, 6006]
)

# Create a script-based configuration
script_config = LaunchConfiguration.script(
    content="#!/bin/bash\necho 'Hello World'",
    language="bash"
)
```

### VolumeConfiguration

Helper class for creating volume configurations:
```python
from shadeform import VolumeConfiguration

# Create a volume attachment configuration
attachment = VolumeConfiguration.create_attachment(
    volume_id="vol-123",
    mount_path="/data"
)
```

## Exception Classes

The SDK defines several exception classes for error handling:

- `ShadeformError`: Base exception class
- `ShadeformAPIError`: Raised for API-related errors
- `ShadeformAuthError`: Raised for authentication errors
- `ShadeformValidationError`: Raised for validation errors

Example error handling:
```python
from shadeform import ShadeformAPIError

try:
    instance = client.instances.get_info("non-existent-id")
except ShadeformAPIError as error:
    print(f"API Error {error.status_code}: {error.message}")
```

## Environment Variables

The SDK supports the following environment variables:

- `SHADEFORM_API_KEY`: API key for authentication
- `SHADEFORM_JWT_TOKEN`: JWT token for authentication
- `SHADEFORM_BASE_URL`: Base URL for the API (optional)