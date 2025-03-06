"""Volume management resource for Shadeform SDK."""

from typing import Any, Dict, List, Optional

from .base import BaseResource
from ..error import ShadeformValidationError
from ..utils.helpers import validate_volume_size


class VolumeClient(BaseResource):
    """Client for managing Shadeform volumes."""

    def create(
        self,
        provider: str,
        name: str,
        size_gb: int,
        volume_type: str,
        description: Optional[str] = None,
        snapshot_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new volume.

        Args:
            provider: Cloud provider (aws, gcp, azure)
            name: Volume name
            size_gb: Size in gigabytes
            volume_type: Type of volume (e.g., 'gp3')
            description: Optional volume description
            snapshot_id: Optional snapshot ID to create from

        Returns:
            Created volume details including id, status, and mount command

        Raises:
            ShadeformValidationError: If volume size is invalid
        """
        if not validate_volume_size(size_gb):
            raise ShadeformValidationError(
                f"Invalid volume size: {size_gb}GB", field="size_gb"
            )

        payload = {
            "provider": provider,
            "name": name,
            "size_gb": size_gb,
            "volume_type": volume_type,
        }

        if description:
            payload["description"] = description
        if snapshot_id:
            payload["snapshot_id"] = snapshot_id

        return self._post_dict("/volumes/create", json=payload)

    def get_info(self, volume_id: str) -> Dict[str, Any]:
        """
        Get information about a specific volume.

        Args:
            volume_id: ID of the volume

        Returns:
            Volume details including id, name, size, attachment status,
            and hourly cost
        """
        return self._get_dict(f"/volumes/{volume_id}/info")

    def list_all(self) -> List[Dict[str, Any]]:
        """
        List all volumes.

        Returns:
            List of volumes with basic information (id, name, status)
        """
        response = self._get_dict("/volumes")
        volumes = response.get("volumes", [])
        return volumes if isinstance(volumes, list) else []

    def delete(self, volume_id: str) -> Dict[str, Any]:
        """
        Delete a volume.

        Args:
            volume_id: ID of the volume

        Returns:
            Success confirmation
        """
        return self._post_dict(f"/volumes/{volume_id}/delete")

    def list_types(self) -> List[Dict[str, Any]]:
        """
        List available volume types.

        Returns:
            List of volume types with specifications (type, max_iops,
            min/max size)
        """
        result = self._get_list("/volumes/types")
        return result if isinstance(result, list) else []
