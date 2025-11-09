# Contributing to data.gov.in MCP Server

Thank you for your interest in contributing to the data.gov.in MCP Server! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/Yash-Kavaiya/data-gov-in-mcp/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Detailed description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Python version and environment details
   - Relevant logs or error messages

### Suggesting Enhancements

1. Check existing issues and discussions
2. Create a new issue with:
   - Clear, descriptive title
   - Detailed description of the enhancement
   - Use cases and benefits
   - Potential implementation approach (if applicable)

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/Yash-Kavaiya/data-gov-in-mcp.git
   cd data-gov-in-mcp
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the code style guidelines below
   - Add tests for new functionality
   - Update documentation as needed

4. **Run tests**
   ```bash
   pytest
   pytest --cov=src/data_gov_in
   ```

5. **Commit your changes**
   ```bash
   git commit -m "Add: Brief description of your changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide a clear description of the changes
   - Reference any related issues
   - Ensure all tests pass

## Development Setup

### Prerequisites

- Python 3.12 or higher
- `uv` or `pip`
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/Yash-Kavaiya/data-gov-in-mcp.git
cd data-gov-in-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
uv sync
# or
pip install -e ".[dev]"

# Set up API key for testing
export DATA_GOV_IN_API_KEY="your-test-api-key"
```

## Code Style Guidelines

### Python Style

We follow PEP 8 with some modifications:

- **Line length**: 100 characters
- **Imports**: Use `isort` for import ordering
- **Formatting**: Use `black` for code formatting
- **Linting**: Use `ruff` for linting

### Type Hints

- Use type hints for all function signatures
- Use `Optional[T]` for nullable types
- Use descriptive type aliases for complex types

Example:
```python
from typing import Optional, Dict, Any

def get_resource(
    resource_id: str,
    filters: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Get resource data with optional filters."""
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of function.

    Longer description if needed.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When param1 is invalid
    """
    pass
```

### Code Organization

- Keep functions focused and single-purpose
- Use meaningful variable and function names
- Avoid magic numbers; use constants
- Keep files under 500 lines when possible

## Testing Guidelines

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names: `test_<what>_<when>_<expected>`
- Use pytest fixtures for common setup
- Mock external API calls

Example:
```python
def test_get_resource_with_valid_id_returns_data():
    """Test that valid resource ID returns data."""
    # Arrange
    client = DataGovInClient(config)

    # Act
    result = client.get_resource("valid-id")

    # Assert
    assert result is not None
    assert "records" in result
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/data_gov_in --cov-report=html

# Run specific test file
pytest tests/test_api_client.py

# Run specific test
pytest tests/test_api_client.py::test_get_resource_with_valid_id_returns_data
```

## Documentation

### Code Documentation

- Add docstrings to all public functions, classes, and modules
- Keep docstrings up-to-date with code changes
- Include examples in docstrings when helpful

### README Updates

- Update README.md when adding new features
- Keep examples current and working
- Update configuration documentation

### API Documentation

- Update `docs/API.md` when changing tool signatures
- Include request/response examples
- Document all parameters and return values

## Commit Message Guidelines

Follow the Conventional Commits specification:

```
<type>: <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat: Add dataset filtering by multiple fields

Implement multi-field filtering to allow users to filter
datasets by multiple criteria simultaneously.

Closes #123
```

```
fix: Handle rate limit errors gracefully

Add exponential backoff when rate limit is hit to prevent
cascading failures.
```

## Release Process

1. Update version in `pyproject.toml` and `src/data_gov_in/__init__.py`
2. Update `CHANGELOG.md`
3. Create a git tag: `git tag -a v1.0.0 -m "Release v1.0.0"`
4. Push tag: `git push origin v1.0.0`
5. Create GitHub release with release notes

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/Yash-Kavaiya/data-gov-in-mcp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Yash-Kavaiya/data-gov-in-mcp/discussions)
- **Email**: yash.kavaiya3@gmail.com

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to data.gov.in MCP Server!
