# Installation Guide

This guide covers all the different ways to install Theme My Fox.

## Prerequisites

Before installing Theme My Fox, ensure you have:

- **Python 3.11 or higher** installed
- **pip** package manager (usually comes with Python)
- **Firefox** installed on your system (required for theme switching to work)

### Checking Your Python Version

```bash
python --version
# or
python3 --version
```

If you don't have Python 3.11+, download it from [python.org](https://www.python.org/downloads/).

## Installation Methods

### Method 1: Using pip with Git (Recommended)

The simplest way to install Theme My Fox:

```bash
pip install git+https://github.com/DeepFriedDuck/theme-my-fox.git
```

**Advantages:**
- Simple one-line installation
- Works with any Python environment
- No need to clone the repository

### Method 2: Using PDM

If you're using [PDM](https://pdm.fming.dev/) for dependency management:

```bash
pdm add git+https://github.com/DeepFriedDuck/theme-my-fox.git
```

**Or add to `pyproject.toml`:**

```toml
[project]
dependencies = [
    "theme-my-fox @ git+https://github.com/DeepFriedDuck/theme-my-fox.git"
]
```

Then run:
```bash
pdm install
```

### Method 3: Using Poetry

If you're using [Poetry](https://python-poetry.org/) for dependency management:

```bash
poetry add git+https://github.com/DeepFriedDuck/theme-my-fox.git
```

**Or add to `pyproject.toml`:**

```toml
[tool.poetry.dependencies]
theme-my-fox = { git = "https://github.com/DeepFriedDuck/theme-my-fox.git" }
```

Then run:
```bash
poetry install
```

### Method 4: From Source (For Development)

If you want to contribute or modify the code:

```bash
# Clone the repository
git clone https://github.com/DeepFriedDuck/theme-my-fox.git
cd theme-my-fox

# Install dependencies with PDM (recommended)
pdm install

# Or use pip in editable mode
pip install -e .
```

**Development installation allows you to:**
- Make changes to the code and test immediately
- Run tests with `pdm run pytest`
- Contribute to the project

## Verifying Installation

After installation, verify that Theme My Fox is installed correctly:

```python
import theme_my_fox

# Print available functions
print(dir(theme_my_fox))

# Try listing Firefox profiles
from theme_my_fox import list_profiles
profiles = list_profiles()
print(f"Found {len(profiles)} Firefox profile(s)")
```

## Dependencies

Theme My Fox has minimal dependencies:

- **lz4 >= 4.4.5** - For LZ4 compression/decompression

These are automatically installed when you install Theme My Fox.

## Platform-Specific Notes

### Linux

Firefox path: `~/.mozilla/firefox/`

No additional setup required. Theme My Fox works out of the box.

### macOS

Firefox path: `~/Library/Application Support/Firefox/`

**Note:** The current version is optimized for Linux. macOS support may require adjustments to the Firefox path detection.

### Windows

Firefox path: `%APPDATA%\Mozilla\Firefox\`

**Note:** The current version is optimized for Linux. Windows support may require adjustments to the Firefox path detection.

## Upgrading

To upgrade to the latest version:

```bash
# With pip
pip install --upgrade git+https://github.com/DeepFriedDuck/theme-my-fox.git

# With PDM
pdm update theme-my-fox

# With Poetry
poetry update theme-my-fox
```

## Uninstalling

To remove Theme My Fox:

```bash
# With pip
pip uninstall theme-my-fox

# With PDM
pdm remove theme-my-fox

# With Poetry
poetry remove theme-my-fox
```

## Troubleshooting Installation

### Issue: `pip` not found

**Solution:** Install pip or use `python -m pip` instead:
```bash
python -m pip install git+https://github.com/DeepFriedDuck/theme-my-fox.git
```

### Issue: Python version mismatch

**Solution:** Use a specific Python version:
```bash
python3.11 -m pip install git+https://github.com/DeepFriedDuck/theme-my-fox.git
```

### Issue: Permission denied

**Solution:** Install in user directory:
```bash
pip install --user git+https://github.com/DeepFriedDuck/theme-my-fox.git
```

### Issue: Git not installed

**Solution:** Install git first:
- **Linux**: `sudo apt-get install git` (Ubuntu/Debian) or `sudo yum install git` (RedHat/CentOS)
- **macOS**: `brew install git` or download from [git-scm.com](https://git-scm.com/)
- **Windows**: Download from [git-scm.com](https://git-scm.com/)

## Next Steps

After installation:

1. Read the **[API Reference](API-Reference)** to understand available functions
2. Check out **[Usage Examples](Usage-Examples)** for practical code samples
3. Try the Quick Start example in the main [Home](Home) page

---

**Need help?** Check the [Troubleshooting](Troubleshooting) page or open an issue on [GitHub](https://github.com/DeepFriedDuck/theme-my-fox/issues).
