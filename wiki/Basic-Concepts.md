# Basic Concepts

Understanding these core concepts will help you use Theme My Fox effectively.

## Firefox Profiles

### What is a Firefox Profile?

A Firefox profile is a collection of settings, bookmarks, extensions, and themes specific to a user. Firefox stores each profile in a separate directory.

**Profile location (Linux):** `~/.mozilla/firefox/`

Each profile directory contains:
- `prefs.js` - User preferences
- `extensions.json` - Installed addons metadata
- `addonStartup.json.lz4` - Compressed startup configuration
- Other configuration files

### Multiple Profiles

Users can have multiple profiles for different purposes:
- **Default Profile**: Created automatically on first Firefox run
- **Development Profile**: Separate profile for testing
- **Work Profile**: Profile with work-specific settings

### Profile Structure

```
~/.mozilla/firefox/
├── profiles.ini          # Profile registry
├── abc123.default/       # Profile directory
│   ├── prefs.js
│   ├── extensions.json
│   ├── addonStartup.json.lz4
│   └── ...
└── xyz789.dev/          # Another profile
    ├── prefs.js
    └── ...
```

## Firefox Themes

### Theme Addons

Themes in Firefox are a type of addon that changes the browser's appearance. Each theme is identified by a unique ID, typically in the format:

```
theme-name@author.org
```

Common built-in themes:
- `firefox-compact-light@mozilla.org` - Light theme
- `firefox-compact-dark@mozilla.org` - Dark theme
- `default-theme@mozilla.org` - System theme (follows OS setting)

### Theme Storage

Theme information is stored in three places:

#### 1. prefs.js
Contains the active theme preference:
```javascript
user_pref("extensions.activeThemeID", "firefox-compact-dark@mozilla.org");
```

#### 2. extensions.json
Contains full addon metadata:
```json
{
  "addons": [
    {
      "id": "firefox-compact-dark@mozilla.org",
      "type": "theme",
      "active": true,
      "userDisabled": false,
      ...
    }
  ]
}
```

#### 3. addonStartup.json.lz4
Compressed startup configuration with enabled addons. This file uses LZ4 compression with a special Firefox header.

### Theme States

A theme can be in different states:
- **Active**: Currently applied and visible
- **Enabled**: Available but not active
- **Disabled**: Installed but not usable

## LZ4 Compression

### Why LZ4?

Firefox uses LZ4 compression for performance. LZ4 is:
- **Fast**: Very quick compression/decompression
- **Efficient**: Good compression ratios
- **Reliable**: Well-tested algorithm

### Firefox's LZ4 Format

Firefox adds a special 8-byte header to LZ4 files:
```
mozLz40\0
```

This header helps Firefox identify its compressed files. Theme My Fox handles this automatically.

### Working with Compressed Files

```python
from theme_my_fox import compress, decompress

# Decompress for reading/editing
decompress("addonStartup.json.lz4", "addonStartup.json")

# Edit the JSON file...

# Compress back
compress("addonStartup.json", "addonStartup.json.lz4")
```

## File Safety

### When to Close Firefox

⚠️ **Always close Firefox before modifying profile files!**

Firefox caches configuration in memory. If you modify files while Firefox is running:
- Changes may be overwritten
- Firefox may crash
- Settings may become corrupted

### Backup Recommendations

Before making changes, consider backing up:

```python
import shutil
from pathlib import Path

profile_path = Path("~/.mozilla/firefox/abc123.default").expanduser()

# Backup important files
files_to_backup = ["prefs.js", "extensions.json", "addonStartup.json.lz4"]
backup_dir = Path("backup")
backup_dir.mkdir(exist_ok=True)

for filename in files_to_backup:
    src = profile_path / filename
    if src.exists():
        shutil.copy(src, backup_dir / filename)
```

## Common Patterns

### Safe Theme Switching

Always update all three locations for complete theme switching:

```python
def switch_theme_safe(profile_path, theme_id):
    """Safely switch themes by updating all necessary files."""
    from theme_my_fox import (
        set_active_theme_in_prefs,
        set_active_theme_in_extensions,
        set_active_theme_in_addon_startup
    )
    
    # Update all three files
    set_active_theme_in_prefs(profile_path, theme_id)
    set_active_theme_in_extensions(profile_path, theme_id)
    set_active_theme_in_addon_startup(profile_path, theme_id)
```

### Error Handling

Always handle potential errors:

```python
from theme_my_fox import list_profiles, get_profile_path_by_index

try:
    profiles = list_profiles()
    if not profiles:
        print("No profiles found")
        exit(1)
    
    profile_path = get_profile_path_by_index(0)
except IndexError:
    print("Profile index out of range")
except FileNotFoundError:
    print("Firefox directory not found")
except Exception as e:
    print(f"Error: {e}")
```

### Validation

Check if a theme exists before switching:

```python
def is_theme_available(profile_path, theme_id):
    """Check if a theme is installed."""
    from theme_my_fox import get_available_themes
    
    themes = get_available_themes(profile_path)
    return any(t.get('id') == theme_id for t in themes)

# Usage
if is_theme_available(profile_path, "my-theme@example.com"):
    switch_theme_safe(profile_path, "my-theme@example.com")
else:
    print("Theme not found!")
```

## Platform Differences

### Linux (Primary Support)

- Firefox path: `~/.mozilla/firefox/`
- Full support for all features
- Most tested platform

### macOS (Community Support)

- Firefox path: `~/Library/Application Support/Firefox/Profiles/`
- May need path adjustments
- Community contributions welcome

### Windows (Limited Support)

- Firefox path: `%APPDATA%\Mozilla\Firefox\Profiles\`
- Path separators differ
- Some functions may need adaptation

## Next Steps

Now that you understand the basics:

- Explore the [Profile Management API](Profile-Management-API.md)
- Learn about [Theme Management API](Theme-Management-API.md)
- Try [Common Use Cases](Common-Use-Cases.md)
- Check [Troubleshooting Guide](Troubleshooting-Guide.md) if you run into issues
