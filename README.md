# Theme My Fox 🦊

A Python library for programmatically managing Firefox themes. Switch themes, compress/decompress Firefox configuration files, and interact with Firefox profiles from your Python code.

## Features

- 🎨 **Theme Management**: Switch between installed Firefox themes programmatically
- 🗜️ **LZ4 Compression**: Compress and decompress Firefox's LZ4-compressed files (like `addonStartup.json.lz4`)
- 📁 **Profile Management**: List and access Firefox profiles
- 🔧 **Configuration Editing**: Modify Firefox preferences and extension settings
- 🐍 **Python 3.11+**: Modern Python support

## Installation

### Using pip with Git

```bash
pip install git+https://github.com/DeepFriedDuck/theme-my-fox.git
```

### Using PDM

```bash
pdm add git+https://github.com/DeepFriedDuck/theme-my-fox.git
```

### Using Poetry

```bash
poetry add git+https://github.com/DeepFriedDuck/theme-my-fox.git
```

### From Source (Development)

```bash
git clone https://github.com/DeepFriedDuck/theme-my-fox.git
cd theme-my-fox
pdm install
```

## Quick Start

### List Firefox Profiles

```python
from theme_my_fox import list_profiles

profiles = list_profiles()
for i, profile in enumerate(profiles):
    print(f"{i}: {profile['name']} - {profile['path']}")
```

### Get Available Themes

```python
from theme_my_fox import get_profile_path_by_index, get_available_themes

# Get the first profile
profile_path = get_profile_path_by_index(0)

# List available themes
themes = get_available_themes(profile_path)
for theme in themes:
    print(f"Theme: {theme['id']}")
```

### Switch Firefox Theme

```python
from theme_my_fox import (
    get_profile_path_by_index,
    set_active_theme_in_prefs,
    set_active_theme_in_extensions,
    set_active_theme_in_addon_startup
)

# Get profile path
profile_path = get_profile_path_by_index(0)
theme_id = "firefox-compact-dark@mozilla.org"

# Set the theme in all necessary files
set_active_theme_in_prefs(profile_path, theme_id)
set_active_theme_in_extensions(profile_path, theme_id)
set_active_theme_in_addon_startup(profile_path, theme_id)

print(f"Theme switched to {theme_id}")
print("Restart Firefox to see the changes")
```

### Compress/Decompress Files

```python
from theme_my_fox import compress, decompress

# Decompress a Firefox LZ4 file
decompress("addonStartup.json.lz4", "addonStartup.json")

# Compress it back
compress("addonStartup.json", "addonStartup.json.lz4")
```

## API Reference

### Profile Management

#### `get_firefox_path() -> Path`
Returns the path to the Firefox directory (`~/.mozilla/firefox` on Linux).

#### `list_profiles() -> List[Dict[str, str]]`
Returns a list of Firefox profiles. Each profile is a dictionary with:
- `name`: Profile name
- `path`: Absolute path to the profile directory

#### `get_profile_path_by_index(index: int) -> Path`
Returns the path for a profile at the specified 0-based index.
- **Parameters**: `index` - Zero-based profile index
- **Raises**: `IndexError` if index is out of range

### Theme Management

#### `get_available_themes(profile_path: Path) -> List[Dict]`
Returns a list of installed theme addons for the given profile.
- **Parameters**: `profile_path` - Path to Firefox profile directory
- **Returns**: List of theme addon dictionaries from `extensions.json`

#### `set_active_theme_in_prefs(profile_path: Path, theme_id: str) -> None`
Sets the active theme in `prefs.js`.
- **Parameters**:
  - `profile_path` - Path to Firefox profile directory
  - `theme_id` - Theme addon ID (e.g., `"firefox-compact-dark@mozilla.org"`)

#### `set_active_theme_in_extensions(profile_path: Path, theme_id: str) -> None`
Updates `extensions.json` to enable the specified theme and disable others.
- **Parameters**:
  - `profile_path` - Path to Firefox profile directory
  - `theme_id` - Theme addon ID

#### `set_active_theme_in_addon_startup(profile_path: Path, theme_id: str) -> None`
Updates `addonStartup.json.lz4` to enable the specified theme.
- **Parameters**:
  - `profile_path` - Path to Firefox profile directory
  - `theme_id` - Theme addon ID

### File Compression

#### `compress(src: str, dest: str) -> None`
Compresses a file using LZ4 with Firefox's magic header (`mozLz40`).
- **Parameters**:
  - `src` - Source file path
  - `dest` - Destination file path

#### `decompress(src: str, dest: str) -> None`
Decompresses a Firefox LZ4 file.
- **Parameters**:
  - `src` - Source LZ4 file path
  - `dest` - Destination file path
- **Raises**: `ValueError` if the file doesn't have the correct magic number

## Use Cases

### Theme Scheduler

Create a script to change themes based on time of day:

```python
from datetime import datetime
from theme_my_fox import (
    get_profile_path_by_index,
    set_active_theme_in_prefs,
    set_active_theme_in_extensions,
    set_active_theme_in_addon_startup
)

def set_theme(profile_index, theme_id):
    profile_path = get_profile_path_by_index(profile_index)
    set_active_theme_in_prefs(profile_path, theme_id)
    set_active_theme_in_extensions(profile_path, theme_id)
    set_active_theme_in_addon_startup(profile_path, theme_id)

# Use dark theme at night, light theme during day
hour = datetime.now().hour
if 6 <= hour < 18:
    set_theme(0, "firefox-compact-light@mozilla.org")
else:
    set_theme(0, "firefox-compact-dark@mozilla.org")
```

### Backup Theme Settings

```python
import json
from theme_my_fox import get_profile_path_by_index, get_available_themes

profile_path = get_profile_path_by_index(0)
themes = get_available_themes(profile_path)

with open("theme_backup.json", "w") as f:
    json.dump(themes, f, indent=2)
```

## Requirements

- Python 3.11 or higher
- lz4 >= 4.4.5
- Firefox installed (for actual theme switching)

## Development

### Setup Development Environment

```bash
git clone https://github.com/DeepFriedDuck/theme-my-fox.git
cd theme-my-fox
pdm install
```

### Run Tests

```bash
pdm run pytest
```

## How It Works

Firefox stores theme information in multiple files within each profile:

1. **`prefs.js`**: User preferences including `extensions.activeThemeID`
2. **`extensions.json`**: Addon metadata including installed themes
3. **`addonStartup.json.lz4`**: Compressed startup configuration with enabled addons

This library provides functions to:
- Read and modify these files
- Handle LZ4 compression/decompression with Firefox's special header
- Manage theme activation across all necessary configuration files

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the WTFPL (Do What The Fuck You Want To Public License) - see the [LICENSE](LICENSE) file for details.

## Links

- [GitHub Repository](https://github.com/DeepFriedDuck/theme-my-fox)
- [Documentation Wiki](https://github.com/DeepFriedDuck/theme-my-fox/wiki)

## Troubleshooting

### Firefox Must Be Closed

Firefox caches configuration files. Always close Firefox before running scripts that modify theme settings, and restart it to see changes.

### Profile Not Found

If you get an `IndexError` when accessing profiles:
```python
profiles = list_profiles()
print(f"Found {len(profiles)} profiles")
for i, p in enumerate(profiles):
    print(f"{i}: {p['name']}")
```

### Invalid Theme ID

Theme IDs must match exactly. Use `get_available_themes()` to see valid theme IDs for your profile.

## Version History

See [CHANGELOG.md](CHANGELOG.md) for version history (if available).

---

Made with 🦊 by [DeepFriedDuck](https://github.com/DeepFriedDuck)
