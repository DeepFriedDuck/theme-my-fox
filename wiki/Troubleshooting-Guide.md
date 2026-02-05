# Troubleshooting Guide

Solutions to common problems when using Theme My Fox.

## Installation Issues

### Python Version Error

**Problem:** Installation fails with Python version error

**Error Message:**
```
ERROR: Package requires Python >=3.11 but you have 3.9
```

**Solution:**
1. Check your Python version:
   ```bash
   python --version
   python3 --version
   ```

2. Install Python 3.11 or higher:
   ```bash
   # Ubuntu/Debian
   sudo apt install python3.11
   
   # macOS with Homebrew
   brew install python@3.11
   ```

3. Use the correct Python version:
   ```bash
   python3.11 -m pip install git+https://github.com/DeepFriedDuck/theme-my-fox.git
   ```

### LZ4 Compilation Fails

**Problem:** `lz4` dependency fails to compile

**Error Message:**
```
error: command 'gcc' failed with exit status 1
```

**Solution:**

**Ubuntu/Debian:**
```bash
sudo apt-get update
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

**Windows:**
Install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

### Permission Denied During Installation

**Problem:** Permission error when installing

**Solution 1:** Install for your user only:
```bash
pip install --user git+https://github.com/DeepFriedDuck/theme-my-fox.git
```

**Solution 2:** Use a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install git+https://github.com/DeepFriedDuck/theme-my-fox.git
```

## Runtime Errors

### No Profiles Found

**Problem:** `list_profiles()` returns empty list

**Possible Causes:**
1. Firefox is not installed
2. Firefox has never been run
3. Non-standard Firefox installation path

**Solutions:**

**Check if Firefox is installed:**
```bash
# Linux
which firefox
ls ~/.mozilla/firefox/

# macOS
ls ~/Library/Application\ Support/Firefox/Profiles/

# Windows
dir "%APPDATA%\Mozilla\Firefox\Profiles"
```

**Run Firefox once:**
If Firefox is installed but never run, it won't have profiles. Launch Firefox at least once to create a default profile.

**Check for profiles manually:**
```python
from pathlib import Path
import configparser

firefox_path = Path.home() / ".mozilla" / "firefox"
profiles_ini = firefox_path / "profiles.ini"

if profiles_ini.exists():
    config = configparser.ConfigParser()
    config.read(profiles_ini)
    print("Sections:", config.sections())
else:
    print(f"profiles.ini not found at {profiles_ini}")
```

### Profile Index Out of Range

**Problem:** `IndexError: profile index out of range`

**Error:**
```python
profile_path = get_profile_path_by_index(5)
# IndexError: profile index out of range
```

**Solution:**

Check how many profiles exist first:
```python
from theme_my_fox import list_profiles

profiles = list_profiles()
print(f"Number of profiles: {len(profiles)}")
print(f"Valid indices: 0 to {len(profiles) - 1}")

# Use safe indexing
if len(profiles) > 0:
    profile_path = get_profile_path_by_index(0)
else:
    print("No profiles available")
```

### Theme Changes Don't Take Effect

**Problem:** Theme is switched but Firefox still shows the old theme

**Causes:**
1. Firefox is running while changes are made
2. Not all three configuration files were updated
3. Firefox cache issues

**Solutions:**

**1. Close Firefox completely:**
```bash
# Linux/macOS - check for Firefox processes
ps aux | grep firefox

# Kill Firefox if running
pkill firefox

# Windows
tasklist | findstr firefox
taskkill /IM firefox.exe /F
```

**2. Update all three files:**
```python
from theme_my_fox import (
    get_profile_path_by_index,
    set_active_theme_in_prefs,
    set_active_theme_in_extensions,
    set_active_theme_in_addon_startup,
)

profile_path = get_profile_path_by_index(0)
theme_id = "firefox-compact-dark@mozilla.org"

# Must call all three functions
set_active_theme_in_prefs(profile_path, theme_id)
set_active_theme_in_extensions(profile_path, theme_id)
set_active_theme_in_addon_startup(profile_path, theme_id)
```

**3. Clear Firefox cache:**
In Firefox, go to: `Preferences` → `Privacy & Security` → `Clear Data` → Clear cache

### Theme ID Not Found

**Problem:** Specified theme ID doesn't exist

**Error:**
```
KeyError: theme not found
```

**Solution:**

List all available themes:
```python
from theme_my_fox import get_profile_path_by_index, get_available_themes

profile_path = get_profile_path_by_index(0)
themes = get_available_themes(profile_path)

print("Available theme IDs:")
for theme in themes:
    theme_id = theme.get('id')
    name = theme.get('defaultLocale', {}).get('name', theme_id)
    print(f"  {name}")
    print(f"    ID: {theme_id}")
```

Common built-in theme IDs:
- `firefox-compact-light@mozilla.org`
- `firefox-compact-dark@mozilla.org`
- `default-theme@mozilla.org`

### Invalid LZ4 Magic Number

**Problem:** `ValueError: Invalid magic number` when decompressing

**Cause:** File is not a valid Firefox LZ4 file

**Solution:**

Verify the file header:
```python
with open("file.lz4", "rb") as f:
    header = f.read(8)
    if header == b'mozLz40\x00':
        print("Valid Firefox LZ4 file")
    else:
        print(f"Invalid header: {header}")
        print("This is not a Firefox LZ4 file")
```

### Permission Denied Error

**Problem:** `PermissionError` when modifying profile files

**Causes:**
1. Firefox is running (most common)
2. Insufficient file permissions
3. Profile directory is read-only

**Solutions:**

**1. Close Firefox:**
Make sure Firefox is completely closed before running your script.

**2. Check file permissions:**
```bash
ls -la ~/.mozilla/firefox/*/prefs.js
# Should be readable and writable by your user
```

**3. Check if profile is locked:**
```python
from pathlib import Path
from theme_my_fox import get_profile_path_by_index

profile_path = get_profile_path_by_index(0)
lock_file = profile_path / ".parentlock"

if lock_file.exists():
    print("Profile is locked (Firefox is running)")
else:
    print("Profile is not locked")
```

### File Not Found Error

**Problem:** Required configuration file doesn't exist

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: '.../prefs.js'
```

**Causes:**
1. Profile has never been used
2. Profile is corrupted
3. Wrong profile path

**Solution:**

Check which files exist:
```python
from pathlib import Path
from theme_my_fox import get_profile_path_by_index

profile_path = get_profile_path_by_index(0)

required_files = ["prefs.js", "extensions.json", "addonStartup.json.lz4"]

print(f"Checking profile: {profile_path}\n")
for filename in required_files:
    filepath = profile_path / filename
    exists = "✓" if filepath.exists() else "✗"
    print(f"{exists} {filename}")
```

If files are missing, launch Firefox with that profile to create them.

## Platform-Specific Issues

### macOS: Profile Not Found

**Problem:** Can't find Firefox profiles on macOS

**Solution:**

Firefox profiles are in a different location on macOS:

```python
from pathlib import Path

# macOS Firefox path
firefox_path = Path.home() / "Library/Application Support/Firefox/Profiles"

if firefox_path.exists():
    print(f"Firefox profiles found at: {firefox_path}")
    for profile in firefox_path.iterdir():
        if profile.is_dir():
            print(f"  - {profile.name}")
else:
    print("Firefox profiles directory not found")
```

You may need to use absolute paths instead of `get_firefox_path()`.

### Windows: Path Issues

**Problem:** Path separators or special characters cause issues

**Solution:**

Use `Path` objects instead of strings:
```python
from pathlib import Path
import os

# Windows Firefox path
firefox_path = Path(os.environ['APPDATA']) / "Mozilla/Firefox/Profiles"

# Use raw strings for Windows paths
# profile_path = Path(r"C:\Users\Username\AppData\Roaming\Mozilla\Firefox\Profiles\...")
```

### Linux: Snap/Flatpak Firefox

**Problem:** Firefox installed via Snap or Flatpak has different paths

**Solution:**

**Snap:**
```python
firefox_path = Path.home() / "snap/firefox/common/.mozilla/firefox"
```

**Flatpak:**
```python
firefox_path = Path.home() / ".var/app/org.mozilla.firefox/.mozilla/firefox"
```

## Debugging Tips

### Enable Verbose Output

Add debugging information to your scripts:

```python
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Use in your code
logger.debug(f"Profile path: {profile_path}")
logger.debug(f"Theme ID: {theme_id}")
```

### Inspect Configuration Files

Check what's actually in the files:

```python
from theme_my_fox import get_profile_path_by_index
from pathlib import Path

profile_path = get_profile_path_by_index(0)

# Read prefs.js
prefs_js = profile_path / "prefs.js"
with open(prefs_js) as f:
    for line in f:
        if "activeThemeID" in line:
            print(line.strip())

# Read extensions.json
import json
extensions_json = profile_path / "extensions.json"
with open(extensions_json) as f:
    data = json.load(f)
    for addon in data.get('addons', []):
        if addon.get('type') == 'theme':
            print(f"Theme: {addon.get('id')}, Active: {addon.get('active')}")
```

### Verify Theme Switch

After switching, verify the change:

```python
from theme_my_fox import get_available_themes

def verify_theme_switch(profile_path, expected_theme_id):
    """Verify that theme was switched successfully."""
    themes = get_available_themes(profile_path)
    
    for theme in themes:
        theme_id = theme.get('id')
        active = theme.get('active', False)
        
        if theme_id == expected_theme_id:
            if active:
                print(f"✓ Theme '{theme_id}' is active")
                return True
            else:
                print(f"✗ Theme '{theme_id}' is not marked as active")
                return False
    
    print(f"✗ Theme '{expected_theme_id}' not found")
    return False

# Usage
verify_theme_switch(profile_path, "firefox-compact-dark@mozilla.org")
```

## Getting Help

If you're still stuck:

1. **Check existing issues:** [GitHub Issues](https://github.com/DeepFriedDuck/theme-my-fox/issues)
2. **Search the wiki:** Look through other wiki pages
3. **Ask for help:** Open a new issue with:
   - Your Python version
   - Your OS and Firefox version
   - Full error message
   - Minimal code to reproduce the problem

### Creating a Good Bug Report

```python
# Include this information in bug reports
import sys
import platform
from theme_my_fox import __version__

print(f"Theme My Fox: {__version__}")
print(f"Python: {sys.version}")
print(f"Platform: {platform.platform()}")
print(f"Firefox path: {get_firefox_path()}")
```

## See Also

- [Quick Start Tutorial](Quick-Start-Tutorial.md) - Getting started
- [Basic Concepts](Basic-Concepts.md) - Understanding how it works
- [API Documentation](Profile-Management-API.md) - Function reference
- [Common Use Cases](Common-Use-Cases.md) - Example scripts
