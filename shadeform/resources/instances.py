"""Instance management resource for Shadeform SDK."""

from typing import Any, Dict, List, Optional

from .base import BaseResource
from ..error import ShadeformValidationError
from ..utils.helpers import validate_instance_type

class InstanceClient(BaseResource):
    """Client for managing Shadeform instances."""

    def create(
        self,
        provider: str,
        name: str,
        region: str,
        instance_type: str,
        launch_config: Dict[str, Any],
        ssh_key_id: Optional[str] = None,
        volumes: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Create a new instance.

        Args:
            provider: Cloud provider (aws, gcp, azure)
            name: Instance name
            region: Region to deploy the instance
            instance_type: Type of GPU instance
            launch_config: Launch configuration (docker or script)
            ssh_key_id: Optional SSH key ID
            volumes: Optional list of volume configurations

        Returns:
            Created instance details including id, status, public_ip, ssh_port
            and creation timestamp

        Raises:
            ShadeformValidationError: If instance type is invalid
        """
        if not validate_instance_type(instance_type):
            raise ShadeformValidationError(
                f"Invalid instance type: {instance_type}",
                field="instance_type"
            )

        payload: Dict[str, Any] = {
            "provider": provider,
            "name": name,
            "region": region,
            "instance_type": instance_type,
            "launch_configuration": launch_config
        }

        if ssh_key_id:
            payload["ssh_key_id"] = ssh_key_id

        if volumes:
            # Ensure each volume config is converted to dict format
            payload["volumes"] = [dict(vol) if hasattr(vol, "__dict__") else vol for vol in volumes]

        return self._post_dict("/instances/create", json=payload)

    def get_info(self, instance_id: str) -> Dict[str, Any]:
        """
        Get information about a specific instance.

        Args:
            instance_id: ID of the instance

        Returns:
            Instance details including id, name, status, instance_type,
            hourly_price, and uptime
        """
        return self._get_dict(f"/instances/{instance_id}/info")

    def list_all(self) -> List[Dict[str, Any]]:
        """
        List all instances.

        Returns:
            List of instances with basic information (id, name, status,
            instance_type)
        """
        response = self._get_dict("/instances")
        instances = response.get("instances", [])
        return instances if isinstance(instances, list) else []

    def update(self, instance_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an instance.

        Args:
            instance_id: ID of the instance
            updates: Update parameters (e.g., {"name": "new-name"})

        Returns:
            Success confirmation
        """
        return self._post_dict(f"/instances/{instance_id}/update", json=updates)

    def delete(self, instance_id: str) -> Dict[str, Any]:
        """
        Delete an instance.

        Args:
            instance_id: ID of the instance

        Returns:
            Success confirmation with deletion message
        """
        return self._post_dict(f"/instances/{instance_id}/delete")

    def restart(self, instance_id: str) -> Dict[str, Any]:
        """
        Restart an instance.

        Args:
            instance_id: ID of the instance

        Returns:
            Success confirmation with new status
        """
        return self._post_dict(f"/instances/{instance_id}/restart")

    def list_types(self) -> List[Dict[str, Any]]:
        """
        List available instance types.

        Returns:
            List of instance types with specifications (type, provider,
            memory_gb, vCPUs, hourly_price)
        """
        result = self._get_list("/instances/types")
        return result if isinstance(result, list) else []
