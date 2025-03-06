"""Main client class for Shadeform SDK."""

import os
from typing import Any, Dict, List, Optional, Union

import requests
from requests.models import Response

from .error import ShadeformAPIError, ShadeformAuthError, ShadeformError
from .resources.instances import InstanceClient
from .resources.sshkeys import SSHKeyClient
from .resources.templates import TemplateClient
from .resources.volumes import VolumeClient

DEFAULT_BASE_URL = "https://api.shadeform.ai/v1"

class ShadeformClient:
    """
    Main client class for interacting with the Shadeform API.
    
    This class provides access to all API resources and handles authentication
    and request management.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        jwt_token: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> None:
        """
        Initialize the Shadeform client.

        Args:
            api_key: API key for authentication
            jwt_token: JWT token for authentication
            base_url: Base URL for API requests

        Raises:
            ShadeformAuthError: If neither API key nor JWT token is provided
        """
        self.api_key = api_key or os.getenv("SHADEFORM_API_KEY")
        self.jwt_token = jwt_token or os.getenv("SHADEFORM_JWT_TOKEN")
        self.base_url = base_url or os.getenv("SHADEFORM_BASE_URL", DEFAULT_BASE_URL)

        if not self.api_key and not self.jwt_token:
            raise ShadeformAuthError("Either API key or JWT token must be provided")

        self.session = requests.Session()
        self._setup_session()

        # Initialize resource clients
        self.instances = InstanceClient(self)
        self.ssh_keys = SSHKeyClient(self)
        self.volumes = VolumeClient(self)
        self.templates = TemplateClient(self)

    def _setup_session(self) -> None:
        """Configure the requests session with appropriate headers."""
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"shadeform-python/{self._get_version()}"
        })

        if self.api_key:
            self.session.headers.update({
                "X-API-Key": self.api_key
            })
        elif self.jwt_token:
            self.session.headers.update({
                "Authorization": f"Bearer {self.jwt_token}"
            })

    def request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], None]:
        """
        Make a request to the API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            **kwargs: Additional request parameters

        Returns:
            API response data

        Raises:
            ShadeformAPIError: For API-related errors
            ShadeformError: For other errors
        """
        base = DEFAULT_BASE_URL if self.base_url is None else self.base_url
        url = f"{base.rstrip('/')}/{endpoint.lstrip('/')}"

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()

            return self._process_response(response)

        except requests.exceptions.HTTPError as error:
            error_data = {}
            try:
                error_data = error.response.json()
            except (ValueError, AttributeError):
                pass

            message = error_data.get("message", str(error))
            raise ShadeformAPIError(
                message,
                status_code=error.response.status_code if error.response else None,
                error_data=error_data
            )

        except requests.exceptions.RequestException as error:
            raise ShadeformError(f"Request failed: {str(error)}")

        except ValueError as error:
            raise ShadeformError(f"Invalid JSON response: {str(error)}")

    def _process_response(
        self, response: Response
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], None]:
        """
        Process the API response.

        Args:
            response: Response from the API

        Returns:
            Processed response data

        Raises:
            ShadeformError: For invalid response formats
        """
        # Handle 204 No Content responses
        if response.status_code == 204:
            return None

        # Return empty dict for empty responses
        if not response.content:
            return {}

        try:
            data = response.json()
            if not isinstance(data, (dict, list)):
                raise ShadeformError(
                    f"Invalid response type: {type(data).__name__}"
                )
            return data
        except ValueError as e:
            raise ShadeformError(f"Invalid JSON response: {str(e)}")

    @staticmethod
    def _get_version() -> str:
        """Get the current version of the SDK."""
        try:
            from . import __version__
            return __version__
        except ImportError:
            return "unknown"

    def __repr__(self) -> str:
        """Return string representation of the client."""
        auth_type = "API Key" if self.api_key else "JWT Token"
        return f"ShadeformClient(auth_type={auth_type}, base_url={self.base_url})"