# Shadeform SDK Examples

This document provides practical examples of common use cases when working with the Shadeform SDK.

## Installation and Setup

```bash
# Install the package
pip install shadeform

# Set environment variables (optional)
export SHADEFORM_API_KEY="your-api-key"
export SHADEFORM_BASE_URL="https://api.shadeform.ai/v1"
```

## Basic Client Setup

```python
from shadeform import ShadeformClient

# Using API key directly
client = ShadeformClient(api_key="your-api-key")

# Or using JWT token
client = ShadeformClient(jwt_token="your-jwt-token")

# Or using environment variables
client = ShadeformClient()  # Will use SHADEFORM_API_KEY or SHADEFORM_JWT_TOKEN
```

## Managing GPU Instances

### Creating a Docker-based Instance

```python
from shadeform import ShadeformClient, LaunchConfiguration

# Initialize client
client = ShadeformClient(api_key="your-api-key")

# Create Docker launch configuration
launch_config = LaunchConfiguration.docker(
    image="pytorch/pytorch:latest",
    command="python /app/train.py",
    env_vars={
        "BATCH_SIZE": "64",
        "LEARNING_RATE": "0.001",
        "NUM_EPOCHS": "100"
    },
    ports=[8080, 6006]  # Expose ports for web server and TensorBoard
)

# Create instance
instance = client.instances.create(
    provider="aws",
    name="pytorch-training",
    region="us-west-2",
    instance_type="A100_80Gx1",
    launch_config=launch_config
)

print(f"Instance created with ID: {instance['id']}")
```

### Creating a Script-based Instance

```python
from shadeform import ShadeformClient, LaunchConfiguration

# Initialize client
client = ShadeformClient(api_key="your-api-key")

# Create script launch configuration
script_content = """#!/bin/bash
apt-get update
apt-get install -y python3-pip git
pip install torch torchvision
git clone https://github.com/user/project.git
cd project
python3 train.py
"""

launch_config = LaunchConfiguration.script(
    content=script_content,
    language="bash"
)

# Create instance
instance = client.instances.create(
    provider="aws",
    name="training-script",
    region="us-west-2",
    instance_type="A100_80Gx1",
    launch_config=launch_config
)
```

### Managing Instance Lifecycle

```python
from shadeform import ShadeformClient

client = ShadeformClient(api_key="your-api-key")

# List all instances
instances = client.instances.list_all()
for instance in instances:
    print(f"ID: {instance['id']}, Name: {instance['name']}, Status: {instance['status']}")

# Get specific instance info
instance_info = client.instances.get_info("instance-123")
print(f"Instance details: {instance_info}")

# Update instance name
client.instances.update("instance-123", {"name": "new-name"})

# Restart instance
client.instances.restart("instance-123")

# Delete instance
client.instances.delete("instance-123")
```

## Working with SSH Keys

```python
from shadeform import ShadeformClient

client = ShadeformClient(api_key="your-api-key")

# Add a new SSH key
ssh_key = client.ssh_keys.add(
    name="laptop-key",
    public_key="ssh-rsa AAAA..."
)

# List all SSH keys
keys = client.ssh_keys.list_all()
for key in keys:
    print(f"ID: {key['id']}, Name: {key['name']}")

# Set as default key
client.ssh_keys.set_default(ssh_key["id"])

# Create instance with SSH key
instance = client.instances.create(
    provider="aws",
    name="ssh-enabled-instance",
    region="us-west-2",
    instance_type="A100_80Gx1",
    launch_config=launch_config,
    ssh_key_id=ssh_key["id"]
)
```

## Managing Storage Volumes

```python
from shadeform import ShadeformClient, VolumeConfiguration

client = ShadeformClient(api_key="your-api-key")

# Create a new volume
volume = client.volumes.create(
    provider="aws",
    name="dataset-volume",
    region="us-west-2",
    volume_type="gp3",
    size_gb=100
)

# Create volume attachment configuration
volume_attachment = VolumeConfiguration.create_attachment(
    volume_id=volume["id"],
    mount_path="/data"
)

# Create instance with attached volume
instance = client.instances.create(
    provider="aws",
    name="instance-with-volume",
    region="us-west-2",
    instance_type="A100_80Gx1",
    launch_config=launch_config,
    volumes=[volume_attachment]
)
```

## Working with Templates

```python
from shadeform import ShadeformClient, LaunchConfiguration

client = ShadeformClient(api_key="your-api-key")

# Create a template configuration
launch_config = LaunchConfiguration.docker(
    image="pytorch/pytorch:latest",
    command="python train.py",
    env_vars={"BATCH_SIZE": "64"}
)

# Save template
template = client.templates.save(
    name="pytorch-training",
    description="PyTorch training environment",
    launch_config=launch_config,
    provider="aws",
    instance_type="A100_80Gx1"
)

# List available templates
templates = client.templates.list_all()
for tmpl in templates:
    print(f"Template: {tmpl['name']} - {tmpl['description']}")

# Get featured templates
featured = client.templates.get_featured()
for tmpl in featured:
    print(f"Featured template: {tmpl['name']}")
```

## Error Handling

```python
from shadeform import (
    ShadeformClient,
    ShadeformError,
    ShadeformAPIError,
    ShadeformAuthError
)

client = ShadeformClient(api_key="your-api-key")

try:
    # Attempt to get info for non-existent instance
    instance = client.instances.get_info("non-existent-id")
except ShadeformAPIError as e:
    print(f"API Error {e.status_code}: {e.message}")
except ShadeformAuthError as e:
    print(f"Authentication error: {e}")
except ShadeformError as e:
    print(f"General error: {e}")
```

## Environment Variables

The SDK supports several environment variables for configuration:

```bash
# Required (one of these)
export SHADEFORM_API_KEY="your-api-key"
export SHADEFORM_JWT_TOKEN="your-jwt-token"

# Optional
export SHADEFORM_BASE_URL="https://api.shadeform.ai/v1"
```

These variables can be used instead of passing the values directly to the client constructor.