"""Base resource class for Shadeform SDK."""

from typing import Any, Dict, List, Optional, TypeVar, Union, TYPE_CHECKING

from ..error import ShadeformError

if TYPE_CHECKING:
    from ..client import ShadeformClient

T = TypeVar("T", bound="BaseResource")


class BaseResource:
    """Base class for all resource clients."""

    def __init__(self, client: "ShadeformClient") -> None:
        """
        Initialize the base resource client.

        Args:
            client: The Shadeform client instance
        """
        self.client = client

    def _make_request(
        self, method: str, endpoint: str, expect_list: bool = False, **kwargs: Any
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], None]:
        """
        Helper method to make requests to the API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            expect_list: Whether to expect a list response
            **kwargs: Additional request parameters

        Returns:
            API response data

        Raises:
            ShadeformError: If response type doesn't match expected type
        """
        response = self.client.request(method, endpoint, **kwargs)

        if response is None:
            return {} if not expect_list else []

        # Handle various response formats
        if expect_list:
            if isinstance(response, list):
                return response
            elif isinstance(response, dict):
                # Try to find a list in the dict values
                for value in response.values():
                    if isinstance(value, list):
                        return value
                return []  # Return empty list if no list found
            else:
                raise ShadeformError(f"Unexpected response type: {type(response).__name__}")
        else:
            if isinstance(response, dict):
                return response
            else:
                raise ShadeformError(f"Expected dict response, got {type(response).__name__}")

    def _get_dict(self, endpoint: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Make a GET request that returns a dictionary.

        Args:
            endpoint: API endpoint path
            **kwargs: Additional request parameters

        Returns:
            API response data as dictionary

        Raises:
            ShadeformError: If response isn't a dictionary
        """
        result = self._make_request("GET", endpoint, expect_list=False, **kwargs)
        if result is None:
            return {}
        if not isinstance(result, dict):
            raise ShadeformError(f"Expected dict response, got {type(result).__name__}")
        return result

    def _get_list(self, endpoint: str, **kwargs: Any) -> List[Dict[str, Any]]:
        """
        Make a GET request that returns a list.

        Args:
            endpoint: API endpoint path
            **kwargs: Additional request parameters

        Returns:
            API response data as list

        Raises:
            ShadeformError: If response isn't a list
        """
        result = self._make_request("GET", endpoint, expect_list=True, **kwargs)
        if result is None:
            return []
        if not isinstance(result, list):
            raise ShadeformError(f"Expected list response, got {type(result).__name__}")
        return result

    def _post_dict(self, endpoint: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Make a POST request that returns a dictionary.

        Args:
            endpoint: API endpoint path
            **kwargs: Additional request parameters

        Returns:
            API response data as dictionary

        Raises:
            ShadeformError: If response isn't a dictionary
        """
        result = self._make_request("POST", endpoint, expect_list=False, **kwargs)
        if result is None:
            return {"success": True}  # Return a default success response if None
        if not isinstance(result, dict):
            raise ShadeformError(f"Expected dict response, got {type(result).__name__}")
        return result

    def _post_none(self, endpoint: str, **kwargs: Any) -> None:
        """
        Make a POST request that returns None.

        Args:
            endpoint: API endpoint path
            **kwargs: Additional request parameters

        Raises:
            ShadeformError: If response isn't None
        """
        result = self._make_request("POST", endpoint, **kwargs)
        if result is not None:
            raise ShadeformError(f"Expected None response, got {type(result).__name__}")
        return None
