"""
Shadeform Python SDK

A Python SDK for managing GPU instances and infrastructure through the Shadeform API.
"""

from .client import ShadeformClient
from .error import (
    ShadeformError,
    ShadeformAPIError,
    ShadeformAuthError,
    ShadeformValidationError,
    ShadeformResourceError,
    ShadeformConfigurationError,
)
from .utils.helpers import LaunchConfiguration, VolumeConfiguration

__version__ = "0.1.0"
__author__ = "Shadeform, Inc."
__license__ = "MIT"

# Version info for project dependencies
__minimum_python_version__ = "3.8.0"
__api_version__ = "v1"

__all__ = [
    "ShadeformClient",
    "ShadeformError",
    "ShadeformAPIError",
    "ShadeformAuthError",
    "ShadeformValidationError",
    "ShadeformResourceError",
    "ShadeformConfigurationError",
    "LaunchConfiguration",
    "VolumeConfiguration",
]

# Type aliases for better code documentation
InstanceID = str
VolumeID = str
SSHKeyID = str
TemplateID = str

# Configuration type hints
LaunchConfigType = dict
VolumeAttachmentType = dict

def get_version() -> str:
    """Return the current version of the SDK."""
    return __version__

def get_api_version() -> str:
    """Return the current API version supported by the SDK."""
    return __api_version__