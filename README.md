# Shadeform Python SDK

[![PyPI version](https://badge.fury.io/py/shadeform.svg)](https://badge.fury.io/py/shadeform)
[![Python versions](https://img.shields.io/pypi/pyversions/shadeform.svg)](https://test.pypi.org/project/shadeform/)
[![License](https://img.shields.io/pypi/l/shadeform.svg)](https://github.com/svskaushik/shadeform-python/blob/main/LICENSE)

A Python package for managing GPU instances and infrastructure through the Shadeform API. Simplify your GPU cloud management with an intuitive, type-safe interface.

## Quick Start

### Installation

```bash
pip install --index-url https://test.pypi.org/simple/ shadeform
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
from shadeform import ShadeformClient, VolumeConfiguration

# Create a volume
volume = client.volumes.create(
    provider="aws",
    name="dataset-volume",
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
templates = client.templates.list_featured()
for template in templates:
    print(f"Template: {template['name']}")

# Save your own template
client.templates.save(
    name="custom-training",
    description="Custom PyTorch environment",
    config=launch_config
)
```

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

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Shadeform Documentation: https://docs.shadeform.ai
- Issue Tracker: https://github.com/svskaushik/shadeform-python/issues
