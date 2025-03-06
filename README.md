# Shadeform Python SDK

[![PyPI version](https://badge.fury.io/py/shadeform.svg)](https://badge.fury.io/py/shadeform)
[![Python versions](https://img.shields.io/pypi/pyversions/shadeform.svg)](https://pypi.org/project/shadeform/)
[![License](https://img.shields.io/pypi/l/shadeform.svg)](https://github.com/svskaushik/shadeform-python/blob/main/LICENSE)

A powerful Python SDK for managing GPU instances and infrastructure through the Shadeform API. Simplify your GPU cloud management with an intuitive, type-safe interface.

## Features

- 🚀 Easy GPU instance management
- 🔑 SSH key management for secure access
- 💾 Persistent volume management
- 📋 Template-based deployments
- 🐳 Docker and script-based launch configurations
- 🔒 Secure authentication with API keys or JWT tokens
- ✨ Type hints for better IDE support

## Quick Start

### Installation

```bash
pip install shadeform
```

### Basic Usage

```python
from shadeform import ShadeformClient, LaunchConfiguration

# Initialize client
client = ShadeformClient(api_key="your-api-key")

# Create a Docker-based launch configuration
launch_config = LaunchConfiguration.docker(
    image="pytorch/pytorch:latest",
    command="python /app/train.py",
    env_vars={"BATCH_SIZE": "64"}
)

# Launch a GPU instance
instance = client.instances.create(
    provider="aws",
    name="training-instance",
    region="us-west-2",
    instance_type="A100_80Gx1",
    launch_config=launch_config
)

print(f"Instance created with ID: {instance['id']}")
```

## Examples

### Managing Instances

```python
# List all instances
instances = client.instances.list_all()
for instance in instances:
    print(f"ID: {instance['id']}, Status: {instance['status']}")

# Get instance info
info = client.instances.get_info("instance-123")

# Restart an instance
client.instances.restart("instance-123")

# Delete an instance
client.instances.delete("instance-123")
```

### Working with Volumes

```python
# Create a volume
volume = client.volumes.create(
    provider="aws",
    name="dataset-volume",
    region="us-west-2",
    volume_type="gp3",
    size_gb=100
)

# Attach volume to instance during creation
volume_config = VolumeConfiguration.create_attachment(
    volume_id=volume["id"],
    mount_path="/data"
)

instance = client.instances.create(
    # ... other parameters ...
    volumes=[volume_config]
)
```

### Using Templates

```python
# List featured templates
templates = client.templates.get_featured()
for template in templates:
    print(f"Template: {template['name']}")

# Save your own template
client.templates.save(
    name="custom-training",
    description="Custom PyTorch environment",
    config=launch_config
)
```

## Documentation

- [API Reference](docs/api/index.md)
- [Examples](docs/examples.md)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## Development

1. Clone the repository:
```bash
git clone https://github.com/svskaushik/shadeform-python.git
cd shadeform-python
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Documentation: https://docs.shadeform.ai
- Issue Tracker: https://github.com/svskaushik/shadeform-python/issues
- Community Chat: https://discord.gg/shadeform