# Theme Management API

This page documents all functions for managing and switching Firefox themes.

## Overview

Firefox themes are stored across multiple configuration files. Theme My Fox provides functions to query available themes and switch between them safely.

## Functions

### get_available_themes()

Get the list of theme addons installed in a Firefox profile.

**Signature:**
```python
def get_available_themes(profile_path: Path) -> List[Dict]
```

**Parameters:**
- `profile_path` (Path): Path to the Firefox profile directory

**Returns:**
- `List[Dict]`: List of theme addon objects from `extensions.json`
- Returns empty list if `extensions.json` doesn't exist

**Example:**
```python
from theme_my_fox import get_profile_path_by_index, get_available_themes

profile_path = get_profile_path_by_index(0)
themes = get_available_themes(profile_path)

for theme in themes:
    theme_id = theme.get('id')
    name = theme.get('defaultLocale', {}).get('name', theme_id)
    active = theme.get('active', False)
    
    status = "✓ ACTIVE" if active else ""
    print(f"{name} {status}")
    print(f"  ID: {theme_id}\n")
```

**Theme Dictionary Structure:**

Each theme dictionary contains:
```python
{
    "id": "firefox-compact-dark@mozilla.org",
    "type": "theme",
    "active": True,
    "userDisabled": False,
    "defaultLocale": {
        "name": "Firefox Dark",
        "description": "..."
    },
    # ... other fields
}
```

**Notes:**
- Only returns addons with `"type": "theme"`
- Returns empty list if no themes or file doesn't exist
- Safe to call even if profile has no themes installed

---

### set_active_theme_in_prefs()

Set the active theme in the `prefs.js` file.

**Signature:**
```python
def set_active_theme_in_prefs(profile_path: Path, theme_id: str) -> None
```

**Parameters:**
- `profile_path` (Path): Path to the Firefox profile directory
- `theme_id` (str): The theme addon ID (e.g., `"firefox-compact-dark@mozilla.org"`)

**Returns:**
- None

**Example:**
```python
from theme_my_fox import get_profile_path_by_index, set_active_theme_in_prefs

profile_path = get_profile_path_by_index(0)
theme_id = "firefox-compact-dark@mozilla.org"

set_active_theme_in_prefs(profile_path, theme_id)
print("Updated prefs.js")
```

**What it does:**
- Searches for the `extensions.activeThemeID` preference line
- Updates it if found, or appends it if not found
- Writes the modified `prefs.js` back to disk

**Notes:**
- ⚠️ Close Firefox before calling this function
- Creates the preference if it doesn't exist
- Overwrites existing preference value

---

### set_active_theme_in_extensions()

Update `extensions.json` to enable the specified theme and disable others.

**Signature:**
```python
def set_active_theme_in_extensions(profile_path: Path, theme_id: str) -> None
```

**Parameters:**
- `profile_path` (Path): Path to the Firefox profile directory
- `theme_id` (str): The theme addon ID to activate

**Returns:**
- None

**Example:**
```python
from theme_my_fox import get_profile_path_by_index, set_active_theme_in_extensions

profile_path = get_profile_path_by_index(0)
set_active_theme_in_extensions(profile_path, "firefox-compact-light@mozilla.org")
print("Updated extensions.json")
```

**What it does:**
- Loads `extensions.json`
- For each theme addon:
  - If ID matches `theme_id`: sets `userDisabled=False` and `active=True`
  - Otherwise: sets `userDisabled=True` and `active=False`
- Writes the updated JSON back to disk

**Notes:**
- ⚠️ Close Firefox before calling this function
- Only affects addons with `"type": "theme"`
- Other addon types (extensions) are not modified

---

### set_active_theme_in_addon_startup()

Update `addonStartup.json.lz4` to enable only the specified theme.

**Signature:**
```python
def set_active_theme_in_addon_startup(profile_path: Path, theme_id: str) -> None
```

**Parameters:**
- `profile_path` (Path): Path to the Firefox profile directory
- `theme_id` (str): The theme addon ID to enable

**Returns:**
- None

**Example:**
```python
from theme_my_fox import get_profile_path_by_index, set_active_theme_in_addon_startup

profile_path = get_profile_path_by_index(0)
set_active_theme_in_addon_startup(profile_path, "default-theme@mozilla.org")
print("Updated addonStartup.json.lz4")
```

**What it does:**
1. Decompresses `addonStartup.json.lz4` to a temporary file
2. Loads the JSON and updates theme enabled states
3. Sets `enabled=True` for the target theme, `enabled=False` for others
4. Recompresses and writes back to `addonStartup.json.lz4`

**Notes:**
- ⚠️ Close Firefox before calling this function
- Uses temporary file for decompression/recompression
- Only modifies theme addons, not extensions

## Complete Theme Switch

For a complete theme switch, call all three functions:

```python
from theme_my_fox import (
    get_profile_path_by_index,
    set_active_theme_in_prefs,
    set_active_theme_in_extensions,
    set_active_theme_in_addon_startup
)

def switch_theme(profile_index, theme_id):
    """Completely switch to a new theme."""
    profile_path = get_profile_path_by_index(profile_index)
    
    print(f"Switching to theme: {theme_id}")
    
    set_active_theme_in_prefs(profile_path, theme_id)
    print("  ✓ Updated prefs.js")
    
    set_active_theme_in_extensions(profile_path, theme_id)
    print("  ✓ Updated extensions.json")
    
    set_active_theme_in_addon_startup(profile_path, theme_id)
    print("  ✓ Updated addonStartup.json.lz4")
    
    print("\n✓ Theme switch complete!")
    print("Restart Firefox to see the changes.")

# Usage
switch_theme(0, "firefox-compact-dark@mozilla.org")
```

## Advanced Usage

### Validate Theme Before Switching

Always validate that a theme exists before switching:

```python
from theme_my_fox import get_available_themes

def is_valid_theme(profile_path, theme_id):
    """Check if theme ID is valid for this profile."""
    themes = get_available_themes(profile_path)
    return any(t.get('id') == theme_id for t in themes)

# Usage
if is_valid_theme(profile_path, "my-theme@example.com"):
    switch_theme(0, "my-theme@example.com")
else:
    print("Error: Theme not found!")
    print("Available themes:")
    for theme in get_available_themes(profile_path):
        print(f"  - {theme.get('id')}")
```

### Get Currently Active Theme

```python
from theme_my_fox import get_available_themes

def get_active_theme(profile_path):
    """Get the ID of the currently active theme."""
    themes = get_available_themes(profile_path)
    for theme in themes:
        if theme.get('active'):
            return theme.get('id')
    return None

# Usage
current = get_active_theme(profile_path)
print(f"Current theme: {current}")
```

### Interactive Theme Selector

```python
from theme_my_fox import get_profile_path_by_index, get_available_themes

def select_and_switch_theme(profile_index=0):
    """Interactive theme selector."""
    profile_path = get_profile_path_by_index(profile_index)
    themes = get_available_themes(profile_path)
    
    if not themes:
        print("No themes found!")
        return
    
    print("Available themes:\n")
    for i, theme in enumerate(themes):
        name = theme.get('defaultLocale', {}).get('name', theme.get('id'))
        active = " (current)" if theme.get('active') else ""
        print(f"  [{i}] {name}{active}")
    
    try:
        choice = int(input(f"\nSelect theme (0-{len(themes)-1}): "))
        if 0 <= choice < len(themes):
            theme_id = themes[choice].get('id')
            switch_theme(profile_index, theme_id)
        else:
            print("Invalid choice")
    except ValueError:
        print("Please enter a number")
    except KeyboardInterrupt:
        print("\nCancelled")

# Usage
select_and_switch_theme()
```

### Theme Information Utility

```python
from theme_my_fox import get_available_themes

def print_theme_info(profile_path):
    """Print detailed information about all themes."""
    themes = get_available_themes(profile_path)
    
    print(f"Found {len(themes)} theme(s):\n")
    
    for theme in themes:
        theme_id = theme.get('id')
        locale = theme.get('defaultLocale', {})
        name = locale.get('name', 'Unknown')
        description = locale.get('description', 'No description')
        active = theme.get('active', False)
        disabled = theme.get('userDisabled', False)
        
        print(f"{'='*60}")
        print(f"Name:        {name}")
        print(f"ID:          {theme_id}")
        print(f"Description: {description}")
        print(f"Status:      {'Active' if active else 'Inactive'}")
        print(f"Disabled:    {'Yes' if disabled else 'No'}")
        print()

# Usage
profile_path = get_profile_path_by_index(0)
print_theme_info(profile_path)
```

## Common Theme IDs

Built-in Firefox themes:

```python
# Light theme
"firefox-compact-light@mozilla.org"

# Dark theme
"firefox-compact-dark@mozilla.org"

# System theme (follows OS theme)
"default-theme@mozilla.org"
```

## Error Handling

### Robust Theme Switching

```python
from pathlib import Path
from theme_my_fox import (
    get_profile_path_by_index,
    get_available_themes,
    set_active_theme_in_prefs,
    set_active_theme_in_extensions,
    set_active_theme_in_addon_startup
)

def safe_switch_theme(profile_index, theme_id):
    """Switch themes with full error handling."""
    try:
        # Get profile
        profile_path = get_profile_path_by_index(profile_index)
        
        # Validate profile exists
        if not profile_path.exists():
            print(f"Error: Profile directory not found: {profile_path}")
            return False
        
        # Validate theme exists
        themes = get_available_themes(profile_path)
        if not any(t.get('id') == theme_id for t in themes):
            print(f"Error: Theme '{theme_id}' not found")
            print("Available themes:")
            for t in themes:
                print(f"  - {t.get('id')}")
            return False
        
        # Switch theme
        print(f"Switching to: {theme_id}")
        set_active_theme_in_prefs(profile_path, theme_id)
        set_active_theme_in_extensions(profile_path, theme_id)
        set_active_theme_in_addon_startup(profile_path, theme_id)
        
        print("✓ Theme switched successfully!")
        print("Restart Firefox to apply changes.")
        return True
        
    except IndexError:
        print(f"Error: Profile index {profile_index} out of range")
        return False
    except FileNotFoundError as e:
        print(f"Error: Required file not found: {e}")
        return False
    except PermissionError as e:
        print(f"Error: Permission denied: {e}")
        print("Make sure Firefox is closed")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

# Usage
if not safe_switch_theme(0, "firefox-compact-dark@mozilla.org"):
    print("Theme switch failed")
```

## Troubleshooting

### Changes Don't Take Effect

1. **Firefox is running**: Close Firefox completely before switching themes
2. **Cache issues**: Clear Firefox cache after switching
3. **Incomplete switch**: Make sure all three functions are called

### Theme Not Found

If a theme ID doesn't work:
```python
# List all available theme IDs
themes = get_available_themes(profile_path)
print("Valid theme IDs:")
for theme in themes:
    print(f"  {theme.get('id')}")
```

### File Permission Errors

If you get permission errors:
- Make sure Firefox is closed
- Check file permissions in the profile directory
- Run your script with appropriate permissions

## See Also

- [Profile Management API](Profile-Management-API.md) - Working with profiles
- [Compression API](Compression-API.md) - LZ4 compression utilities
- [Basic Concepts](Basic-Concepts.md) - Understanding themes
- [Common Use Cases](Common-Use-Cases.md) - Practical examples
