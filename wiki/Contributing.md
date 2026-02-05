# Contributing to Theme My Fox

Thank you for your interest in contributing to Theme My Fox! 🦊

## Ways to Contribute

There are many ways to contribute to this project:

- 🐛 **Report bugs** - Help us find and fix issues
- 💡 **Suggest features** - Share your ideas for improvements
- 📝 **Improve documentation** - Help others understand the library better
- 🔧 **Submit code** - Fix bugs or implement new features
- 🧪 **Write tests** - Improve test coverage
- 🌍 **Platform support** - Help make it work better on macOS/Windows

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- PDM (recommended) or pip
- Firefox installed (for testing)

### Setting Up Development Environment

1. **Fork and clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/theme-my-fox.git
cd theme-my-fox
```

2. **Install dependencies with PDM (recommended):**
```bash
pdm install
```

Or with pip in editable mode:
```bash
pip install -e .
pip install pytest
```

3. **Verify installation:**
```bash
# Run tests
pdm run pytest

# Or with pytest directly
pytest
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

Use descriptive branch names:
- `feature/add-windows-support`
- `fix/profile-detection-bug`
- `docs/improve-readme`

### 2. Make Your Changes

- Write clean, readable code
- Follow existing code style
- Add docstrings to new functions
- Update documentation if needed

### 3. Write Tests

Add tests for new features or bug fixes:

```python
# test/test_your_feature.py
import pytest
from theme_my_fox import your_new_function

def test_your_new_function():
    result = your_new_function()
    assert result == expected_value
```

### 4. Run Tests

```bash
# Run all tests
pdm run pytest

# Run specific test file
pdm run pytest test/test_core.py

# Run with coverage
pdm run pytest --cov=theme_my_fox
```

All tests must pass before submitting a PR.

### 5. Commit Your Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "Add support for Windows Firefox profiles"
```

Good commit message format:
```
Short summary (50 chars or less)

More detailed explanation if needed. Explain what
and why, not how (the code shows how).

Fixes #123
```

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub with:
- Clear description of changes
- Link to related issues
- Screenshots for UI changes
- Test results

## Code Style Guidelines

### Python Style

Follow PEP 8 and existing code style:

```python
# Good
def get_profile_path_by_index(index: int) -> Path:
    """Return the Path for profile at 0-based index.
    
    Args:
        index: Zero-based profile index
        
    Returns:
        Path object for the profile directory
        
    Raises:
        IndexError: If index is out of range
    """
    profiles = list_profiles()
    if index < 0 or index >= len(profiles):
        raise IndexError("profile index out of range")
    return Path(profiles[index]["path"])
```

### Docstring Format

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """Short description of what the function does.
    
    Longer description if needed. Explain behavior,
    side effects, and important details.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: Description of when this is raised
        
    Example:
        >>> function_name("test", 42)
        True
    """
    pass
```

### Type Hints

Use type hints for all functions:

```python
from typing import List, Dict, Optional
from pathlib import Path

def list_profiles() -> List[Dict[str, str]]:
    """Return list of profiles."""
    pass

def get_profile(name: Optional[str] = None) -> Path:
    """Get profile by name."""
    pass
```

## Testing Guidelines

### Writing Good Tests

```python
def test_descriptive_name(tmp_path):
    """Test description."""
    # Arrange - set up test data
    profile = tmp_path / "test_profile"
    profile.mkdir()
    
    # Act - perform the action
    result = some_function(profile)
    
    # Assert - check the result
    assert result == expected_value
```

### Test Coverage

- Aim for >80% code coverage
- Test happy paths and edge cases
- Test error conditions
- Use fixtures for reusable test data

### Using Fixtures

```python
import pytest
from pathlib import Path

@pytest.fixture
def mock_profile(tmp_path):
    """Create a mock Firefox profile for testing."""
    profile = tmp_path / "test.profile"
    profile.mkdir()
    
    # Create mock files
    (profile / "prefs.js").write_text("// test prefs\n")
    (profile / "extensions.json").write_text("{}")
    
    return profile

def test_with_fixture(mock_profile):
    """Test using the fixture."""
    assert mock_profile.exists()
```

## Areas Needing Contribution

### High Priority

1. **macOS Support**
   - Update `get_firefox_path()` to detect macOS Firefox path
   - Test on macOS and fix platform-specific issues
   - Add macOS-specific tests

2. **Windows Support**
   - Update `get_firefox_path()` to detect Windows Firefox path
   - Handle Windows path separators correctly
   - Add Windows-specific tests

3. **Error Handling**
   - Improve error messages
   - Add validation for theme IDs
   - Handle edge cases better

### Medium Priority

4. **CLI Tool**
   - Create a command-line interface
   - Support common operations
   - Add shell completion

5. **Configuration**
   - Support custom Firefox paths
   - Configuration file support
   - Environment variable overrides

6. **Performance**
   - Optimize file operations
   - Cache profile information
   - Reduce Firefox restarts needed

### Nice to Have

7. **Additional Features**
   - Theme import/export
   - Theme preview/screenshots
   - Multi-profile sync
   - Theme scheduling built-in

8. **Documentation**
   - Video tutorials
   - More examples
   - Cookbook recipes

## Pull Request Process

1. **Before submitting:**
   - Run all tests and ensure they pass
   - Update documentation for new features
   - Add/update tests for your changes
   - Check code style

2. **PR Description should include:**
   - What changes were made
   - Why the changes were needed
   - How to test the changes
   - Screenshots for UI changes
   - Link to related issues

3. **After submitting:**
   - Respond to review comments
   - Make requested changes
   - Keep the PR up to date with main branch

4. **PR Review:**
   - Maintainers will review your PR
   - Address feedback and questions
   - Once approved, your PR will be merged!

## Reporting Bugs

### Before Reporting

1. Check if the bug is already reported
2. Try the latest version
3. Check the [Troubleshooting](Troubleshooting) page

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run this code: '...'
2. See error

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Environment:**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.11.0]
- Theme My Fox version: [e.g., 4.3.3]
- Firefox version: [e.g., 122.0]

**Error messages**
```
Paste full error traceback here
```

**Additional context**
Any other relevant information.
```

## Suggesting Features

### Feature Request Template

```markdown
**Feature description**
Clear description of the feature you'd like.

**Use case**
Why is this feature needed? What problem does it solve?

**Proposed solution**
How you envision the feature working.

**Alternatives considered**
Other approaches you've thought about.

**Additional context**
Any other relevant information, examples, or mockups.
```

## Code Review Guidelines

When reviewing PRs:

- ✅ Be respectful and constructive
- ✅ Explain the reasoning behind suggestions
- ✅ Acknowledge good solutions
- ✅ Test the changes locally if possible
- ❌ Don't be condescending
- ❌ Don't demand changes without explanation

## Getting Help

Need help contributing?

- **Discord/Chat**: (Add if available)
- **GitHub Discussions**: Ask questions
- **GitHub Issues**: For bugs and features
- **Email**: deepfriedduck.opensourceapis@gmail.com

## Recognition

Contributors will be:
- Listed in the project's contributors page
- Mentioned in release notes for significant contributions
- Given credit in any related publications

## License

By contributing, you agree that your contributions will be licensed under the WTFPL (Do What The Fuck You Want To Public License), the same license as the project.

---

## Quick Reference

```bash
# Setup
git clone https://github.com/YOUR_USERNAME/theme-my-fox.git
cd theme-my-fox
pdm install

# Development
git checkout -b feature/my-feature
# ... make changes ...
pdm run pytest
git commit -m "Add my feature"
git push origin feature/my-feature
# ... create PR on GitHub ...

# Testing
pdm run pytest                    # Run all tests
pdm run pytest test/test_core.py  # Run specific test
pdm run pytest --cov              # With coverage
pdm run pytest -v                 # Verbose output
```

---

**Thank you for contributing to Theme My Fox!** 🦊

Every contribution, no matter how small, helps make this project better for everyone.
