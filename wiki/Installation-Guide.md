# Installation Guide

This guide covers different ways to install Theme My Fox.

## Prerequisites

- **Python**: Version 3.11 or higher
- **Operating System**: Linux (primary support), macOS and Windows (limited support)
- **Firefox**: Installed on your system (for theme switching functionality)

## Installation Methods

### Method 1: Install from Git (Recommended)

The simplest way to install Theme My Fox is using pip directly from the GitHub repository:

```bash
pip install git+https://github.com/DeepFriedDuck/theme-my-fox.git
```

To upgrade to the latest version:

```bash
pip install --upgrade git+https://github.com/DeepFriedDuck/theme-my-fox.git
```

To install a specific version (tag):

```bash
pip install git+https://github.com/DeepFriedDuck/theme-my-fox.git@v4.3.3
```

### Method 2: Using PDM

If you're using [PDM](https://pdm.fming.dev/) for dependency management:

```bash
pdm add git+https://github.com/DeepFriedDuck/theme-my-fox.git
```

### Method 3: Using Poetry

For [Poetry](https://python-poetry.org/) users:

```bash
poetry add git+https://github.com/DeepFriedDuck/theme-my-fox.git
```

### Method 4: Install from Source (Development)

For development or to contribute to the project:

```bash
# Clone the repository
git clone https://github.com/DeepFriedDuck/theme-my-fox.git
cd theme-my-fox

# Install with pip in editable mode
pip install -e .
```

### Method 5: Using PDM from Source

```bash
git clone https://github.com/DeepFriedDuck/theme-my-fox.git
cd theme-my-fox
pdm install
```

## Verifying Installation

After installation, verify it works:

```python
import theme_my_fox

# Check version
print(theme_my_fox.__version__)

# Try listing profiles (requires Firefox)
try:
    profiles = theme_my_fox.list_profiles()
    print(f"Found {len(profiles)} Firefox profiles")
except Exception as e:
    print(f"Note: {e}")
    print("This is normal if Firefox is not installed")
```

## Dependencies

Theme My Fox automatically installs these dependencies:

- **lz4** (>= 4.4.5): For compressing/decompressing Firefox files

## Platform-Specific Notes

### Linux

Theme My Fox works best on Linux. Firefox profiles are expected at `~/.mozilla/firefox/`.

### macOS

Firefox profiles are located at `~/Library/Application Support/Firefox/Profiles/`. You may need to adjust the `get_firefox_path()` function or use absolute paths.

### Windows

Firefox profiles are at `%APPDATA%\Mozilla\Firefox\Profiles\`. The library primarily targets Linux, so Windows support may require modifications.

## Troubleshooting Installation

### Python Version Issues

If you get a Python version error:

```bash
# Check your Python version
python --version

# Make sure it's 3.11 or higher
```

### Permission Errors

If you encounter permission errors:

```bash
# Install for your user only
pip install --user theme-my-fox

# Or use a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install theme-my-fox
```

### LZ4 Compilation Issues

If lz4 installation fails, you may need development tools:

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-dev build-essential
```

**Fedora/RHEL:**
```bash
sudo dnf install python3-devel gcc
```

**macOS:**
```bash
xcode-select --install
```

## Next Steps

- Continue to the [Quick Start Tutorial](Quick-Start-Tutorial.md)
- Read about [Basic Concepts](Basic-Concepts.md)
- Explore [Common Use Cases](Common-Use-Cases.md)

## Uninstallation

To uninstall Theme My Fox:

```bash
pip uninstall theme-my-fox
```

## Adding to requirements.txt

If you're using a requirements.txt file:

```
git+https://github.com/DeepFriedDuck/theme-my-fox.git
```

Or for a specific version:

```
git+https://github.com/DeepFriedDuck/theme-my-fox.git@v4.3.3
```
