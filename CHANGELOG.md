# Changelog

All notable changes to the Shadeform Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-03-05

### Added
- Initial release of the Shadeform Python SDK
- Core client implementation with API key auth
- Resource clients:
  - Instances: Create, manage, and control GPU instances
  - SSH Keys: Manage SSH key access
  - Volumes: Handle persistent storage volumes
  - Templates: Work with deployment templates
- Configuration helpers:
  - LaunchConfiguration for Docker and script-based launches
  - VolumeConfiguration for volume attachments
  - Instance type validation
  - Volume size validation
- Comprehensive test suite and type hints
- Documentation:
  - API reference
  - Usage examples
  - Contributing guidelines
- Development tools and scripts:
  - Code formatting with Black and isort
  - Type checking with mypy
  - Testing with pytest
  - Publishing script for PyPI

### Security
- Secure authentication handling
- Environment variable support for sensitive credentials
- Proper error handling for API responses

## Types of changes
- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` in case of vulnerabilities

## Release Process

1. Update the version in:
   - `shadeform/__init__.py`
   - `pyproject.toml`
2. Add a new changelog entry
3. Create a pull request
4. After merge, create a GitHub release
5. Publish to PyPI using `scripts/publish.sh`