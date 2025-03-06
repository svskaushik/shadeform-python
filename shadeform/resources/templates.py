"""Template management resource for Shadeform SDK."""

from typing import Any, Dict, List, Optional, cast

from .base import BaseResource
from ..error import ShadeformValidationError

class TemplateClient(BaseResource):
    """Client for managing Shadeform templates."""

    def list_all(self) -> List[Dict[str, Any]]:
        """
        List all templates.

        Returns:
            List of templates with basic information (id, name, framework)
        """
        response = self._get_dict("/templates")
        templates = response.get("templates", [])
        return cast(List[Dict[str, Any]], templates if isinstance(templates, list) else [])

    def get_info(self, template_id: str) -> Dict[str, Any]:
        """
        Get information about a specific template.

        Args:
            template_id: ID of the template

        Returns:
            Template details including id, name, and configuration
        """
        return self._get_dict(f"/templates/{template_id}/info")

    def list_featured(self) -> List[Dict[str, Any]]:
        """
        List featured templates.

        Returns:
            List of featured templates with basic information 
            (id, name, description)
        """
        response = self._get_dict("/templates/featured")
        featured = response.get("featured", [])
        return cast(List[Dict[str, Any]], featured if isinstance(featured, list) else [])

    def save(
        self,
        name: str,
        config: Dict[str, Any],
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Save a new template.

        Args:
            name: Template name
            config: Template configuration
            description: Optional template description

        Returns:
            Created template info including id
        """
        payload = {
            "name": name,
            "config": config
        }
        if description:
            payload["description"] = description

        return self._post_dict("/templates/save", json=payload)

    def update(
        self,
        template_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update a template.

        Args:
            template_id: ID of the template
            updates: Update parameters

        Returns:
            Success confirmation
        """
        return self._post_dict(f"/templates/{template_id}/update", json=updates)

    def delete(self, template_id: str) -> Dict[str, Any]:
        """
        Delete a template.

        Args:
            template_id: ID of the template

        Returns:
            Success confirmation
        """
        return self._post_dict(f"/templates/{template_id}/delete")
