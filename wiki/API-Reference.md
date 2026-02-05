# API Reference

Complete documentation for all functions in the Theme My Fox library.

## Table of Contents

- [Profile Management](#profile-management)
  - [get_firefox_path()](#get_firefox_path)
  - [list_profiles()](#list_profiles)
  - [get_profile_path_by_index()](#get_profile_path_by_index)
- [Theme Management](#theme-management)
  - [get_available_themes()](#get_available_themes)
  - [set_active_theme_in_prefs()](#set_active_theme_in_prefs)
  - [set_active_theme_in_extensions()](#set_active_theme_in_extensions)
  - [set_active_theme_in_addon_startup()](#set_active_theme_in_addon_startup)
- [File Compression](#file-compression)
  - [compress()](#compress)
  - [decompress()](#decompress)

---

## Profile Management

Functions for discovering and accessing Firefox profiles.

### get_firefox_path()

Returns the path to the Firefox directory.

**Signature:**
```python
def get_firefox_path() -> Path
```

**Returns:**
- `Path`: Path object pointing to `~/.mozilla/firefox`

**Example:**
```python
from theme_my_fox import get_firefox_path

firefox_path = get_firefox_path()
print(f"Firefox directory: {firefox_path}")
# Output: Firefox directory: /home/user/.mozilla/firefox
```

**Notes:**
- Currently optimized for Linux systems
- Returns `Path.home() / ".mozilla" / "firefox"`
- May need adjustment for macOS and Windows systems

---

### list_profiles()

Parse `profiles.ini` and return a list of all Firefox profiles.

**Signature:**
```python
def list_profiles() -> List[Dict[str, str]]
```

**Returns:**
- `List[Dict[str, str]]`: List of profile dictionaries, each containing:
  - `name` (str): Profile name
  - `path` (str): Absolute path to the profile directory

**Example:**
```python
from theme_my_fox import list_profiles

profiles = list_profiles()
for i, profile in enumerate(profiles):
    print(f"{i}: {profile['name']}")
    print(f"   Path: {profile['path']}")

# Output:
# 0: default
#    Path: /home/user/.mozilla/firefox/abc123.default
# 1: work
#    Path: /home/user/.mozilla/firefox/def456.work
```

**Notes:**
- Reads from `~/.mozilla/firefox/profiles.ini`
- Handles both relative and absolute profile paths
- Returns absolute paths regardless of how they're stored in `profiles.ini`
- Returns an empty list if no profiles are found

---

### get_profile_path_by_index()

Get the path for a profile at a specific index.

**Signature:**
```python
def get_profile_path_by_index(index: int) -> Path
```

**Parameters:**
- `index` (int): Zero-based profile index from `list_profiles()`

**Returns:**
- `Path`: Path object for the profile directory

**Raises:**
- `IndexError`: If the index is out of range

**Example:**
```python
from theme_my_fox import get_profile_path_by_index

# Get the first profile (index 0)
try:
    profile_path = get_profile_path_by_index(0)
    print(f"Profile path: {profile_path}")
except IndexError:
    print("No profiles found!")

# Output: Profile path: /home/user/.mozilla/firefox/abc123.default
```

**Notes:**
- Index is zero-based (0 = first profile)
- Use `list_profiles()` first to see available profiles and their indices
- Raises `IndexError` for negative indices or indices >= profile count

---

## Theme Management

Functions for managing Firefox themes.

### get_available_themes()

Get a list of all installed theme addons for a profile.

**Signature:**
```python
def get_available_themes(profile_path: Path) -> List[Dict]
```

**Parameters:**
- `profile_path` (Path): Path to the Firefox profile directory

**Returns:**
- `List[Dict]`: List of theme addon dictionaries from `extensions.json`. Each dictionary contains theme metadata including:
  - `id` (str): Theme addon ID
  - `type` (str): Should be "theme"
  - `active` (bool): Whether the theme is currently active
  - `userDisabled` (bool): Whether the theme is disabled
  - Other metadata fields

**Example:**
```python
from theme_my_fox import get_profile_path_by_index, get_available_themes

profile_path = get_profile_path_by_index(0)
themes = get_available_themes(profile_path)

print(f"Found {len(themes)} theme(s):")
for theme in themes:
    status = "Active" if theme.get("active") else "Inactive"
    print(f"  {theme['id']} - {status}")

# Output:
# Found 3 theme(s):
#   firefox-compact-light@mozilla.org - Inactive
#   firefox-compact-dark@mozilla.org - Active
#   my-custom-theme@example.com - Inactive
```

**Notes:**
- Reads from `{profile_path}/extensions.json`
- Returns only addons with `type == "theme"`
- Returns an empty list if `extensions.json` doesn't exist
- Does not raise an exception for missing files

---

### set_active_theme_in_prefs()

Set the active theme in Firefox's `prefs.js` file.

**Signature:**
```python
def set_active_theme_in_prefs(profile_path: Path, theme_id: str) -> None
```

**Parameters:**
- `profile_path` (Path): Path to the Firefox profile directory
- `theme_id` (str): Theme addon ID (e.g., "firefox-compact-dark@mozilla.org")

**Returns:**
- None

**Example:**
```python
from theme_my_fox import get_profile_path_by_index, set_active_theme_in_prefs

profile_path = get_profile_path_by_index(0)
theme_id = "firefox-compact-dark@mozilla.org"

set_active_theme_in_prefs(profile_path, theme_id)
print(f"Updated prefs.js with theme: {theme_id}")
```

**Notes:**
- Modifies `{profile_path}/prefs.js`
- Sets `user_pref("extensions.activeThemeID", "{theme_id}");`
- If the preference already exists, it updates it
- If the preference doesn't exist, it appends it to the file
- **Important:** Firefox must be closed before running this function

---

### set_active_theme_in_extensions()

Update `extensions.json` to enable the specified theme and disable all others.

**Signature:**
```python
def set_active_theme_in_extensions(profile_path: Path, theme_id: str) -> None
```

**Parameters:**
- `profile_path` (Path): Path to the Firefox profile directory
- `theme_id` (str): Theme addon ID to enable

**Returns:**
- None

**Example:**
```python
from theme_my_fox import get_profile_path_by_index, set_active_theme_in_extensions

profile_path = get_profile_path_by_index(0)
theme_id = "firefox-compact-dark@mozilla.org"

set_active_theme_in_extensions(profile_path, theme_id)
print(f"Enabled theme in extensions.json: {theme_id}")
```

**Notes:**
- Modifies `{profile_path}/extensions.json`
- For the specified theme:
  - Sets `userDisabled` to `false`
  - Sets `active` to `true`
- For all other themes:
  - Sets `userDisabled` to `true`
  - Sets `active` to `false`
- Only affects addons with `type == "theme"`
- **Important:** Firefox must be closed before running this function

---

### set_active_theme_in_addon_startup()

Update the compressed `addonStartup.json.lz4` file to enable only the specified theme.

**Signature:**
```python
def set_active_theme_in_addon_startup(profile_path: Path, theme_id: str) -> None
```

**Parameters:**
- `profile_path` (Path): Path to the Firefox profile directory
- `theme_id` (str): Theme addon ID to enable

**Returns:**
- None

**Example:**
```python
from theme_my_fox import get_profile_path_by_index, set_active_theme_in_addon_startup

profile_path = get_profile_path_by_index(0)
theme_id = "firefox-compact-dark@mozilla.org"

set_active_theme_in_addon_startup(profile_path, theme_id)
print(f"Updated addonStartup.json.lz4 with theme: {theme_id}")
```

**Notes:**
- Modifies `{profile_path}/addonStartup.json.lz4`
- Automatically handles decompression and recompression
- Sets `enabled` to `true` for the specified theme
- Sets `enabled` to `false` for all other themes
- Only affects addons with `type == "theme"`
- Uses a temporary file for decompression
- **Important:** Firefox must be closed before running this function

---

## File Compression

Functions for handling Firefox's LZ4-compressed files.

### compress()

Compress a file using LZ4 with Firefox's special magic header.

**Signature:**
```python
def compress(src: str, dest: str) -> None
```

**Parameters:**
- `src` (str): Path to the source file to compress
- `dest` (str): Path where the compressed file should be saved

**Returns:**
- None

**Example:**
```python
from theme_my_fox import compress

# Compress a JSON file
compress("addonStartup.json", "addonStartup.json.lz4")
print("File compressed successfully")
```

**Notes:**
- Uses LZ4 block compression
- Adds Firefox's magic header `mozLz40\0` (8 bytes) to the beginning
- Compatible with Firefox's LZ4 compressed files
- Overwrites destination file if it exists

---

### decompress()

Decompress a Firefox LZ4 file.

**Signature:**
```python
def decompress(src: str, dest: str) -> None
```

**Parameters:**
- `src` (str): Path to the compressed LZ4 file
- `dest` (str): Path where the decompressed file should be saved

**Returns:**
- None

**Raises:**
- `ValueError`: If the file doesn't have the correct magic number (`mozLz40\0`)

**Example:**
```python
from theme_my_fox import decompress

try:
    # Decompress a Firefox LZ4 file
    decompress("addonStartup.json.lz4", "addonStartup.json")
    print("File decompressed successfully")
except ValueError as e:
    print(f"Error: {e}")
```

**Notes:**
- Validates the Firefox magic header `mozLz40\0` (8 bytes)
- Raises `ValueError` if the magic number is incorrect
- Uses LZ4 block decompression
- Overwrites destination file if it exists
- Compatible only with Firefox's LZ4 format (not standard LZ4 files)

---

## Complete Theme Switch Example

To fully switch a theme, you need to update all three configuration files:

```python
from theme_my_fox import (
    get_profile_path_by_index,
    get_available_themes,
    set_active_theme_in_prefs,
    set_active_theme_in_extensions,
    set_active_theme_in_addon_startup
)

# Get profile
profile_path = get_profile_path_by_index(0)

# List available themes
themes = get_available_themes(profile_path)
print("Available themes:")
for i, theme in enumerate(themes):
    print(f"  {i}: {theme['id']}")

# Switch to dark theme
theme_id = "firefox-compact-dark@mozilla.org"
print(f"\nSwitching to: {theme_id}")

# Update all three configuration files
set_active_theme_in_prefs(profile_path, theme_id)
set_active_theme_in_extensions(profile_path, theme_id)
set_active_theme_in_addon_startup(profile_path, theme_id)

print("Theme switched! Restart Firefox to see changes.")
```

---

**See Also:**
- [Usage Examples](Usage-Examples) for more practical examples
- [Troubleshooting](Troubleshooting) for common issues
- [FAQ](FAQ) for frequently asked questions
