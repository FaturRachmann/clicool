# Contributing to CLICOOL

First off, thank you for considering contributing to clicool! It's people like you that make clicool such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps to reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed and what behavior you expected**
* **Include screenshots if possible**
* **Include environment details** (OS, shell, terminal emulator)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a detailed description of the suggested enhancement**
* **Explain why this enhancement would be useful**
* **List some examples of how this enhancement would be used**

### Pull Requests

* Fill in the required template
* Follow the Python style guide
* Include tests if applicable
* Update documentation as needed
* Add an entry to the changelog

## Development Setup

### Prerequisites

* Python 3.11 or higher
* pip
* git

### Setting Up Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/clicool.git
cd clicool

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
.\venv\Scripts\activate  # Windows

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=clicool

# Run specific test file
pytest tests/unit/test_theme_loader.py
```

### Code Style

We use several tools to maintain code quality:

```bash
# Check code style
ruff check clicool

# Format code
black clicool

# Type checking
mypy clicool
```

### Building Documentation

```bash
# Documentation is in README.md and docs/
# No build process required for now
```

## Creating Themes

### Theme Structure

Themes are JSON files that follow the v2 schema:

```json
{
  "name": "My Theme",
  "version": "1.0.0",
  "description": "Description of my theme",
  "tags": ["tag1", "tag2"],
  "prompt": {
    "format": "neon",
    "template": "{user}@{host}:{path} λ",
    "colors": {...},
    "icons": {...}
  },
  "features": {...},
  "terminal": {...},
  "widgets": [],
  "banner": {...}
}
```

### Validating Themes

```bash
# Validate your theme
clicool theme validate path/to/theme.json
```

### Submitting Themes

To submit a theme to the built-in collection:

1. Create your theme JSON file
2. Validate it passes schema validation
3. Test it with `clicool enable`
4. Submit a PR with:
   - Theme JSON file in `themes/builtin/`
   - Screenshot in docs/screenshots/
   - Update README.md theme list

## Creating Layers

Layers are modular add-ons that enhance prompts:

```json
{
  "name": "My Layer",
  "type": "layer",
  "version": "1.0.0",
  "widget": {
    "name": "my-widget",
    "position": "prompt-suffix",
    "config": {...}
  }
}
```

## Creating Plugins

Plugins extend clicool functionality:

```python
# Example plugin structure
def init():
    """Initialize plugin."""
    pass

def enable():
    """Enable plugin."""
    pass

def disable():
    """Disable plugin."""
    pass
```

## Testing Guidelines

### Unit Tests

* Test individual functions and classes
* Mock external dependencies
* Aim for high code coverage
* Use descriptive test names

### Integration Tests

* Test complete workflows
* Test with actual shell configs (in isolated environment)
* Test backup/restore cycles

### Manual Testing

Before submitting a PR, manually test:

* Theme enable/disable
* Backup creation and restoration
* Layer stacking
* Different shells (bash, zsh, fish)
* Different terminal emulators

## Documentation

### Writing Documentation

* Use clear, concise language
* Include examples
* Use code blocks for commands and output
* Add screenshots where helpful

### Documentation Style

* Use present tense
* Use second person ("you")
* Be inclusive and welcoming

## Release Process

Releases are managed by the maintainers. The process:

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create git tag
4. Build and publish to PyPI
5. Create GitHub release

## Questions?

Feel free to open an issue with the "question" label if you have any questions about contributing!

---

<div align="center">

**Thank you for contributing to clicool! 🎉**

</div>
