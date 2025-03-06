"""SSH key management resource for Shadeform SDK."""

from typing import Any, Dict, List, Optional, cast

from .base import BaseResource
from ..error import ShadeformValidationError

class SSHKeyClient(BaseResource):
    """Client for managing Shadeform SSH keys."""

    def add(
        self,
        name: str,
        public_key: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add a new SSH key.

        Args:
            name: Key name
            public_key: Public key content
            description: Optional key description

        Returns:
            Created SSH key details including id, name, and fingerprint

        Raises:
            ShadeformValidationError: If public key is invalid
        """
        if not public_key.strip():
            raise ShadeformValidationError(
                "Public key cannot be empty",
                field="public_key"
            )

        payload = {
            "name": name,
            "public_key": public_key
        }
        if description:
            payload["description"] = description

        return self._post_dict("/sshkeys/add", json=payload)

    def get_info(self, key_id: str) -> Dict[str, Any]:
        """
        Get information about a specific SSH key.

        Args:
            key_id: ID of the SSH key

        Returns:
            SSH key details including id, name, creation timestamp,
            and default status
        """
        return self._get_dict(f"/sshkeys/{key_id}/info")

    def set_default(self, key_id: str) -> Dict[str, Any]:
        """
        Set an SSH key as the default key.

        Args:
            key_id: ID of the SSH key

        Returns:
            Success confirmation with new default key ID
        """
        return self._post_dict(f"/sshkeys/{key_id}/setdefault")

    def delete(self, key_id: str) -> Dict[str, Any]:
        """
        Delete an SSH key.

        Args:
            key_id: ID of the SSH key

        Returns:
            Success confirmation
        """
        return self._post_dict(f"/sshkeys/{key_id}/delete")

    def list_all(self) -> List[Dict[str, Any]]:
        """
        List all SSH keys.

        Returns:
            List of SSH keys with basic information (id, name, is_default)
        """
        response = self._get_dict("/sshkeys")
        ssh_keys = response.get("ssh_keys", [])
        return cast(List[Dict[str, Any]], ssh_keys if isinstance(ssh_keys, list) else [])
