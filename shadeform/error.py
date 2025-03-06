"""Exception classes for Shadeform SDK."""

from typing import Any, Dict, Optional


class ShadeformError(Exception):
    """Base exception class for Shadeform SDK."""

    def __init__(self, message: str) -> None:
        """
        Initialize base error.

        Args:
            message: Error message
        """
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        """Return string representation of the error."""
        return self.message


class ShadeformAuthError(ShadeformError):
    """Exception raised for authentication errors."""

    def __init__(self, message: str) -> None:
        """
        Initialize authentication error.

        Args:
            message: Error message
        """
        super().__init__(message)


class ShadeformAPIError(ShadeformError):
    """Exception raised for API-related errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        error_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize API error.

        Args:
            message: Error message
            status_code: HTTP status code
            error_data: Additional error data from the API
        """
        super().__init__(message)
        self.status_code = status_code
        self.error_data = error_data or {}

    def __str__(self) -> str:
        """Return string representation of the API error."""
        base = f"API Error"
        if self.status_code:
            base = f"{base} {self.status_code}"
        return f"{base}: {self.message}"


class ShadeformValidationError(ShadeformError):
    """Exception raised for validation errors."""

    def __init__(self, message: str, field: Optional[str] = None) -> None:
        """
        Initialize validation error.

        Args:
            message: Error message
            field: Name of the field that failed validation
        """
        super().__init__(message)
        self.field = field

    def __str__(self) -> str:
        """Return string representation of the validation error."""
        if self.field:
            return f"Validation error for {self.field}: {self.message}"
        return f"Validation error: {self.message}"


class ShadeformResourceError(ShadeformError):
    """Exception raised for resource-related errors."""

    def __init__(
        self, message: str, resource_type: str, resource_id: Optional[str] = None
    ) -> None:
        """
        Initialize resource error.

        Args:
            message: Error message
            resource_type: Type of resource (instance, volume, etc.)
            resource_id: ID of the resource
        """
        super().__init__(message)
        self.resource_type = resource_type
        self.resource_id = resource_id

    def __str__(self) -> str:
        """Return string representation of the resource error."""
        base = f"{self.resource_type} error"
        if self.resource_id:
            base = f"{base} for ID {self.resource_id}"
        return f"{base}: {self.message}"


class ShadeformConfigurationError(ShadeformError):
    """Exception raised for configuration-related errors."""

    def __init__(self, message: str, config_type: str) -> None:
        """
        Initialize configuration error.

        Args:
            message: Error message
            config_type: Type of configuration
        """
        super().__init__(message)
        self.config_type = config_type

    def __str__(self) -> str:
        """Return string representation of the configuration error."""
        return f"{self.config_type} configuration error: {self.message}"