# Profile Management API

This page documents all functions related to Firefox profile management.

## Overview

Firefox profiles are independent collections of user settings, bookmarks, and extensions. Theme My Fox provides functions to discover and work with these profiles.

## Functions

### get_firefox_path()

Returns the path to the Firefox directory.

**Signature:**
```python
def get_firefox_path() -> Path
```

**Returns:**
- `Path`: Path object pointing to `~/.mozilla/firefox` (on Linux)

**Example:**
```python
from theme_my_fox import get_firefox_path

firefox_dir = get_firefox_path()
print(f"Firefox directory: {firefox_dir}")
# Output: Firefox directory: /home/user/.mozilla/firefox
```

**Notes:**
- Currently assumes Linux path structure
- For other platforms, you may need to override this or use absolute paths

---

### list_profiles()

Parse `profiles.ini` and return a list of all Firefox profiles.

**Signature:**
```python
def list_profiles() -> List[Dict[str, str]]
```

**Returns:**
- `List[Dict[str, str]]`: List of profile dictionaries, each containing:
  - `name` (str): Profile name as shown in Firefox
  - `path` (str): Absolute path to the profile directory

**Example:**
```python
from theme_my_fox import list_profiles

profiles = list_profiles()
for profile in profiles:
    print(f"Name: {profile['name']}")
    print(f"Path: {profile['path']}\n")
```

**Output:**
```
Name: default-release
Path: /home/user/.mozilla/firefox/abc123.default-release

Name: dev
Path: /home/user/.mozilla/firefox/xyz789.dev
```

**Notes:**
- Handles both relative and absolute profile paths from `profiles.ini`
- Returns empty list if `profiles.ini` doesn't exist or has no profiles
- Profile paths are always absolute, even if stored as relative in `profiles.ini`

**Error Handling:**
```python
from theme_my_fox import list_profiles

try:
    profiles = list_profiles()
    if not profiles:
        print("No Firefox profiles found")
except FileNotFoundError:
    print("Firefox directory not found")
except Exception as e:
    print(f"Error reading profiles: {e}")
```

---

### get_profile_path_by_index()

Get the path to a specific profile by its index in the profiles list.

**Signature:**
```python
def get_profile_path_by_index(index: int) -> Path
```

**Parameters:**
- `index` (int): Zero-based index of the profile (0 for first, 1 for second, etc.)

**Returns:**
- `Path`: Path object pointing to the profile directory

**Raises:**
- `IndexError`: If the index is out of range (negative or >= number of profiles)

**Example:**
```python
from theme_my_fox import get_profile_path_by_index

# Get first profile
profile_path = get_profile_path_by_index(0)
print(profile_path)
# Output: /home/user/.mozilla/firefox/abc123.default-release
```

**Safe Usage:**
```python
from theme_my_fox import list_profiles, get_profile_path_by_index

# Check available profiles first
profiles = list_profiles()
print(f"Found {len(profiles)} profile(s)")

if profiles:
    # Safe to access index 0
    profile_path = get_profile_path_by_index(0)
else:
    print("No profiles available")
```

**Error Handling:**
```python
from theme_my_fox import get_profile_path_by_index

try:
    profile_path = get_profile_path_by_index(5)
except IndexError:
    print("Profile index out of range")
    # Fall back to index 0 or prompt user
    profile_path = get_profile_path_by_index(0)
```

## Complete Example: Profile Selector

Here's a complete example that lets users select a profile:

```python
#!/usr/bin/env python3
"""Interactive profile selector."""

from theme_my_fox import list_profiles, get_profile_path_by_index

def select_profile():
    """Let user select a Firefox profile."""
    profiles = list_profiles()
    
    if not profiles:
        print("No Firefox profiles found!")
        print("Make sure Firefox is installed and has been run at least once.")
        return None
    
    print("Available Firefox Profiles:\n")
    for i, profile in enumerate(profiles):
        print(f"  [{i}] {profile['name']}")
        print(f"      {profile['path']}\n")
    
    while True:
        try:
            choice = input(f"Select profile (0-{len(profiles)-1}): ")
            index = int(choice)
            profile_path = get_profile_path_by_index(index)
            print(f"\nSelected: {profiles[index]['name']}")
            return profile_path
        except ValueError:
            print("Please enter a number")
        except IndexError:
            print(f"Please enter a number between 0 and {len(profiles)-1}")
        except KeyboardInterrupt:
            print("\nCancelled")
            return None

if __name__ == "__main__":
    profile = select_profile()
    if profile:
        print(f"Profile path: {profile}")
```

## Advanced Usage

### Finding a Profile by Name

```python
from theme_my_fox import list_profiles

def find_profile_by_name(name):
    """Find a profile by its name."""
    profiles = list_profiles()
    for profile in profiles:
        if profile['name'] == name:
            return profile['path']
    return None

# Usage
dev_profile = find_profile_by_name("dev")
if dev_profile:
    print(f"Found dev profile at: {dev_profile}")
else:
    print("Dev profile not found")
```

### Checking if a Profile Exists

```python
from pathlib import Path
from theme_my_fox import get_profile_path_by_index

def profile_exists(index):
    """Check if a profile exists and is accessible."""
    try:
        profile_path = get_profile_path_by_index(index)
        return profile_path.exists() and profile_path.is_dir()
    except IndexError:
        return False

# Usage
if profile_exists(0):
    print("Profile 0 exists and is accessible")
else:
    print("Profile 0 not found or not accessible")
```

### Getting Default Profile

The first profile (index 0) is typically the default:

```python
from theme_my_fox import get_profile_path_by_index, list_profiles

def get_default_profile():
    """Get the default profile (first in the list)."""
    profiles = list_profiles()
    if profiles:
        return get_profile_path_by_index(0)
    return None
```

## Troubleshooting

### No Profiles Found

If `list_profiles()` returns an empty list:

1. **Firefox not installed**: Install Firefox
2. **Firefox never run**: Launch Firefox at least once to create a profile
3. **Non-standard location**: Firefox might be installed in a custom location

### Permission Errors

If you get permission errors:
```python
import os
from theme_my_fox import get_firefox_path

firefox_path = get_firefox_path()
print(f"Firefox directory: {firefox_path}")
print(f"Exists: {firefox_path.exists()}")
print(f"Readable: {os.access(firefox_path, os.R_OK)}")
```

### Platform-Specific Issues

For non-Linux platforms, you might need to provide custom paths:

```python
from pathlib import Path

# macOS
firefox_path = Path.home() / "Library/Application Support/Firefox/Profiles"

# Windows
firefox_path = Path(os.environ['APPDATA']) / "Mozilla/Firefox/Profiles"
```

## See Also

- [Basic Concepts](Basic-Concepts.md) - Understanding Firefox profiles
- [Theme Management API](Theme-Management-API.md) - Working with themes in profiles
- [Quick Start Tutorial](Quick-Start-Tutorial.md) - Getting started guide
