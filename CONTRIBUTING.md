# Contributing to Shadeform Python SDK

Thank you for your interest in contributing to the Shadeform Python SDK! This document provides guidelines and instructions for contributing to the project.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/svskaushik/shadeform-python.git
cd shadeform-python
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # For Unix/macOS
# or
.\venv\Scripts\activate  # For Windows
```

3. Install development dependencies:
```bash
pip install -e .[dev]
```

## Code Style and Quality

We use several tools to maintain code quality:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for style guide enforcement
- **mypy** for type checking

Run all checks with:
```bash
# Format code
black shadeform/
isort shadeform/

# Check style
flake8 shadeform/

# Type checking
mypy shadeform/
```

## Running Tests

We use pytest for testing. Run the test suite with:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=shadeform

# Run specific test file
pytest tests/test_client.py
```

## Pull Request Process

1. Fork the repository and create your branch from `main`:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and ensure they include:
   - Implementation code
   - Tests for new functionality
   - Documentation updates
   - Type hints for all functions

3. Run all tests and checks:
```bash
# Run full test suite
pytest

# Run code quality checks
black --check shadeform/
isort --check-only shadeform/
flake8 shadeform/
mypy shadeform/
```

4. Update documentation if needed:
   - Update docstrings
   - Update API reference if adding/changing public APIs
   - Add examples for new features

5. Commit your changes:
```bash
git add .
git commit -m "feat: add your feature description"
```

6. Push to your fork and create a Pull Request:
```bash
git push origin feature/your-feature-name
```

## Commit Message Guidelines

We follow conventional commits. Each commit message should be structured as:

```
<type>: <description>

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:
```
feat: add volume attachment configuration builder

Add VolumeConfiguration class with methods to create volume
attachment configurations for instance creation.

Closes #123
```

## Documentation

When adding or modifying features, please update:

1. Docstrings in the code
2. API reference in `docs/api/`
3. Examples in `docs/examples.md`
4. README.md if necessary

## Release Process

1. Update version in:
   - `shadeform/__init__.py`
   - `setup.py`

2. Update CHANGELOG.md

3. Create a release PR

4. After merge, create a GitHub release

5. The CI/CD pipeline will publish to PyPI

## Getting Help

- Open an issue for bugs or feature requests
- Join our community chat for questions
- Tag maintainers for urgent issues: @maintainer

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.