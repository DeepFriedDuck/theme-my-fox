# Contributing Guide

Thank you for your interest in contributing to Theme My Fox! This guide will help you get started.

## Ways to Contribute

### 1. Report Bugs

Found a bug? Please [open an issue](https://github.com/DeepFriedDuck/theme-my-fox/issues/new) with:

- **Clear title** describing the problem
- **Python version** (`python --version`)
- **OS and Firefox version**
- **Full error message** (if applicable)
- **Minimal code** to reproduce the issue
- **Expected vs actual behavior**

**Example Bug Report:**
```markdown
## Theme switch doesn't work on macOS

**Environment:**
- Python: 3.11.5
- OS: macOS 13.4
- Firefox: 115.0

**Code:**
```python
from theme_my_fox import get_profile_path_by_index
profile_path = get_profile_path_by_index(0)
print(profile_path)
```

**Error:**
```
IndexError: profile index out of range
```

**Expected:** Should find Firefox profile
**Actual:** No profiles found

**Additional info:** Firefox is installed and working
```

### 2. Suggest Features

Have an idea for a new feature? Open an issue with:

- **Use case:** Why is this feature useful?
- **Proposed API:** How would you like to use it?
- **Alternatives:** Other ways you've considered

### 3. Improve Documentation

Documentation improvements are always welcome:

- Fix typos or unclear explanations
- Add examples
- Improve API documentation
- Translate to other languages (future)

### 4. Submit Code

Ready to write code? Great! Follow these steps:

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/theme-my-fox.git
cd theme-my-fox
```

### 2. Install PDM

Theme My Fox uses [PDM](https://pdm.fming.dev/) for dependency management:

```bash
# Install PDM
pip install --user pdm

# Or with pipx (recommended)
pipx install pdm
```

### 3. Install Dependencies

```bash
# Install in development mode
pdm install

# This will:
# - Create a virtual environment
# - Install dependencies
# - Install the package in editable mode
```

### 4. Verify Setup

```bash
# Run tests
pdm run pytest

# Check if package is importable
pdm run python -c "import theme_my_fox; print(theme_my_fox.__version__)"
```

## Making Changes

### 1. Create a Branch

```bash
git checkout -b feature/my-feature
# or
git checkout -b fix/bug-description
```

### 2. Write Your Code

Follow these guidelines:

**Code Style:**
- Use type hints for function parameters and return types
- Follow PEP 8 style guide
- Keep functions focused and single-purpose
- Add docstrings to public functions

**Example:**
```python
def get_theme_name(theme_dict: Dict) -> str:
    """Extract the theme name from a theme dictionary.
    
    Args:
        theme_dict: Theme addon dictionary from extensions.json
        
    Returns:
        Human-readable theme name, or theme ID if name not found
    """
    locale = theme_dict.get('defaultLocale', {})
    return locale.get('name', theme_dict.get('id', 'Unknown'))
```

### 3. Write Tests

Add tests for your changes in the `test/` directory:

```python
# test/test_my_feature.py
import pytest
from theme_my_fox import my_new_function

def test_my_new_function():
    result = my_new_function("input")
    assert result == "expected output"

def test_my_new_function_error_handling():
    with pytest.raises(ValueError):
        my_new_function(invalid_input)
```

### 4. Run Tests

```bash
# Run all tests
pdm run pytest

# Run specific test file
pdm run pytest test/test_my_feature.py

# Run with coverage
pdm run pytest --cov=theme_my_fox
```

### 5. Update Documentation

If you've added new features:

1. Update docstrings
2. Add examples to README if appropriate
3. Update wiki pages if needed

## Submitting Changes

### 1. Commit Your Changes

Write clear commit messages:

```bash
git add .
git commit -m "Add feature to list theme metadata

- Add get_theme_metadata() function
- Include tests for metadata extraction
- Update README with example usage"
```

**Good commit messages:**
- Start with a verb (Add, Fix, Update, Remove)
- First line is a short summary (50 chars or less)
- Add detailed description if needed
- Reference issues: "Fix #123"

### 2. Push to Your Fork

```bash
git push origin feature/my-feature
```

### 3. Create a Pull Request

1. Go to the [main repository](https://github.com/DeepFriedDuck/theme-my-fox)
2. Click "New Pull Request"
3. Select your fork and branch
4. Fill in the PR template:

**PR Template:**
```markdown
## Description
Brief description of changes

## Motivation
Why is this change needed?

## Changes
- Added X
- Fixed Y
- Updated Z

## Testing
How did you test this?

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All tests pass
- [ ] Code follows style guide
```

### 4. Review Process

- Maintainers will review your PR
- Address any feedback
- Once approved, your PR will be merged!

## Code Review Guidelines

When reviewing code:

**Look for:**
- ✅ Clear, readable code
- ✅ Appropriate test coverage
- ✅ Updated documentation
- ✅ No breaking changes (or clearly documented)
- ✅ Error handling for edge cases

**Be constructive:**
- Explain why changes are needed
- Suggest specific improvements
- Acknowledge good work

## Development Tips

### Running Code Locally

```bash
# Use PDM to run scripts
pdm run python my_script.py

# Or activate the virtual environment
eval $(pdm venv activate)
python my_script.py
```

### Testing Different Firefox Setups

Create test profiles for testing:

```bash
# Create a test profile
firefox -CreateProfile "test-profile"

# Or use a temporary profile
firefox -profile /tmp/test-profile
```

### Debugging

```python
# Add debug prints
import sys
print(f"DEBUG: variable value = {value}", file=sys.stderr)

# Use pdb for interactive debugging
import pdb; pdb.set_trace()

# Or use breakpoint() in Python 3.7+
breakpoint()
```

## Project Structure

```
theme-my-fox/
├── theme_my_fox/          # Main package
│   ├── __init__.py        # Public API exports
│   └── core.py            # Core functionality
├── test/                  # Tests
│   └── test_core.py       # Core tests
├── wiki/                  # Documentation
│   ├── Home.md
│   └── *.md
├── pyproject.toml         # Project configuration
├── pdm.lock              # Dependency lock file
├── README.md             # Main documentation
└── LICENSE               # WTFPL license
```

## Coding Standards

### Type Hints

Use type hints for better code clarity:

```python
from typing import List, Dict, Optional
from pathlib import Path

def get_themes(profile_path: Path) -> List[Dict]:
    """Get list of themes."""
    ...

def find_theme(theme_id: str) -> Optional[Dict]:
    """Find theme by ID, or None if not found."""
    ...
```

### Error Handling

Handle errors gracefully:

```python
def safe_operation():
    try:
        # Operation that might fail
        result = risky_operation()
    except FileNotFoundError:
        # Specific error handling
        logger.error("File not found")
        raise
    except Exception as e:
        # Generic fallback
        logger.error(f"Unexpected error: {e}")
        raise
```

### Documentation

Write clear docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """Short one-line description.
    
    Longer description if needed, explaining:
    - What the function does
    - Important behaviors
    - Edge cases
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is invalid
        FileNotFoundError: When file doesn't exist
        
    Example:
        >>> result = function_name("test", 42)
        >>> print(result)
        True
    """
```

## Release Process

(For maintainers)

### Version Numbering

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes

### Creating a Release

1. Update version in `pyproject.toml`
2. Update CHANGELOG (if exists)
3. Create git tag: `git tag -a v4.3.4 -m "Release v4.3.4"`
4. Push tag: `git push origin v4.3.4`
5. Create GitHub release

## Community Guidelines

### Code of Conduct

- **Be respectful** to all contributors
- **Be patient** with newcomers
- **Be constructive** in feedback
- **Be collaborative** in problem-solving

### Getting Help

- **Questions?** Open a discussion or issue
- **Stuck?** Ask for help, don't struggle silently
- **Found something unclear?** Documentation improvements welcome!

## License

By contributing, you agree that your contributions will be licensed under the WTFPL (Do What The Fuck You Want To Public License).

## Recognition

Contributors are recognized in:
- Git commit history
- GitHub contributors page
- Release notes (for significant contributions)

## Questions?

- Open an issue for technical questions
- Check existing issues and discussions
- Read the wiki for more information

Thank you for contributing to Theme My Fox! 🦊

## See Also

- [Development Setup](Development-Setup.md) - Detailed setup instructions
- [Architecture Overview](Architecture-Overview.md) - Understanding the codebase
- [Troubleshooting Guide](Troubleshooting-Guide.md) - Common issues
