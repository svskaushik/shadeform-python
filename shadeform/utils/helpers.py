"""Helper utilities for Shadeform SDK."""

from typing import Any, Dict, List, Optional, Union


class LaunchConfiguration:
    """Utility class for creating launch configurations."""

    @staticmethod
    def docker(
        image: str,
        command: Optional[str] = None,
        env_vars: Optional[Dict[str, str]] = None,
        ports: Optional[List[int]] = None,
    ) -> Dict[str, Any]:
        """
        Create a Docker-based launch configuration.

        Args:
            image: Docker image name
            command: Command to run in the container
            env_vars: Environment variables to set
            ports: Ports to expose

        Returns:
            Launch configuration dictionary
        """
        config: Dict[str, Any] = {"type": "docker", "image": image}

        if command is not None:
            config["command"] = command
        if env_vars is not None:
            config["environment"] = env_vars
        if ports is not None:
            config["ports"] = ports

        return config

    @staticmethod
    def script(content: str, language: str = "bash") -> Dict[str, Any]:
        """
        Create a script-based launch configuration.

        Args:
            content: Script content
            language: Script language (default: bash)

        Returns:
            Launch configuration dictionary
        """
        return {"type": "script", "language": language, "content": content}


class VolumeConfiguration:
    """Utility class for creating volume configurations."""

    @staticmethod
    def create_attachment(volume_id: str, mount_path: str) -> Dict[str, str]:
        """
        Create a volume attachment configuration.

        Args:
            volume_id: ID of the volume to attach
            mount_path: Path where the volume should be mounted

        Returns:
            Volume attachment configuration dictionary
        """
        if not mount_path.startswith("/"):
            mount_path = f"/{mount_path}"

        return {"volume_id": volume_id, "mount_path": mount_path}


def validate_instance_type(instance_type: str) -> bool:
    """
    Validate that an instance type string is properly formatted.

    Args:
        instance_type: Instance type string (e.g., 'A100_80Gx1')

    Returns:
        True if valid, False otherwise
    """
    # Basic format check
    if not instance_type or "_" not in instance_type:
        return False

    # Split into components
    try:
        gpu_type, config = instance_type.split("_", 1)
        specs, count = config.rsplit("x", 1)

        # Validate count is a positive integer
        if not count.isdigit() or int(count) < 1:
            return False

        # Known GPU types (can be expanded)
        valid_gpu_types = ["A100", "A10", "V100", "T4"]
        if gpu_type not in valid_gpu_types:
            return False

        return True
    except ValueError:
        return False


def validate_volume_size(size_gb: int) -> bool:
    """
    Validate that a volume size is within acceptable bounds.

    Args:
        size_gb: Volume size in gigabytes

    Returns:
        True if valid, False otherwise
    """
    MIN_SIZE = 1
    MAX_SIZE = 16384  # 16TB

    return MIN_SIZE <= size_gb <= MAX_SIZE


def validate_volume_type(volume_type: str) -> bool:
    """
    Validate that a volume type is supported.

    Args:
        volume_type: Volume type string (e.g., 'gp3', 'io2')

    Returns:
        True if valid, False otherwise
    """
    # List of known volume types (can be expanded)
    valid_volume_types = ["gp3", "io2", "standard", "st1", "sc1"]
    return volume_type in valid_volume_types
