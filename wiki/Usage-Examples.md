# Usage Examples

Practical examples demonstrating how to use Theme My Fox in real-world scenarios.

## Table of Contents

- [Basic Examples](#basic-examples)
- [Theme Scheduler](#theme-scheduler)
- [Multi-Profile Management](#multi-profile-management)
- [Theme Backup and Restore](#theme-backup-and-restore)
- [Custom Theme Switcher Script](#custom-theme-switcher-script)
- [Integration with System Theme](#integration-with-system-theme)

---

## Basic Examples

### List All Firefox Profiles

```python
from theme_my_fox import list_profiles

profiles = list_profiles()

print(f"Found {len(profiles)} Firefox profile(s):\n")
for i, profile in enumerate(profiles):
    print(f"Profile {i}:")
    print(f"  Name: {profile['name']}")
    print(f"  Path: {profile['path']}")
    print()
```

**Output:**
```
Found 2 Firefox profile(s):

Profile 0:
  Name: default-release
  Path: /home/user/.mozilla/firefox/abc123.default-release

Profile 1:
  Name: dev-profile
  Path: /home/user/.mozilla/firefox/xyz789.dev-profile
```

### List Available Themes

```python
from theme_my_fox import get_profile_path_by_index, get_available_themes

# Get the first profile
profile_path = get_profile_path_by_index(0)

# Get available themes
themes = get_available_themes(profile_path)

print(f"Found {len(themes)} theme(s):\n")
for theme in themes:
    status = "✓ Active" if theme.get("active") else "  Inactive"
    print(f"{status}: {theme['id']}")
```

**Output:**
```
Found 3 theme(s):

  Inactive: firefox-compact-light@mozilla.org
✓ Active: firefox-compact-dark@mozilla.org
  Inactive: my-custom-theme@example.com
```

### Switch Theme (Complete)

```python
from theme_my_fox import (
    get_profile_path_by_index,
    set_active_theme_in_prefs,
    set_active_theme_in_extensions,
    set_active_theme_in_addon_startup
)

def switch_theme(profile_index, theme_id):
    """Switch to a specific theme."""
    profile_path = get_profile_path_by_index(profile_index)
    
    # Update all three configuration files
    set_active_theme_in_prefs(profile_path, theme_id)
    set_active_theme_in_extensions(profile_path, theme_id)
    set_active_theme_in_addon_startup(profile_path, theme_id)
    
    print(f"Theme switched to: {theme_id}")
    print("Please restart Firefox to see the changes.")

# Switch to dark theme
switch_theme(0, "firefox-compact-dark@mozilla.org")
```

### Compress and Decompress Files

```python
from theme_my_fox import compress, decompress

# Decompress a Firefox LZ4 file to inspect or modify
decompress("addonStartup.json.lz4", "addonStartup.json")
print("File decompressed. You can now view/edit addonStartup.json")

# After making changes, compress it back
compress("addonStartup.json", "addonStartup.json.lz4")
print("File compressed back to LZ4 format")
```

---

## Theme Scheduler

Automatically switch themes based on time of day - dark theme at night, light theme during the day.

```python
from datetime import datetime
from theme_my_fox import (
    get_profile_path_by_index,
    set_active_theme_in_prefs,
    set_active_theme_in_extensions,
    set_active_theme_in_addon_startup
)

def set_theme(profile_index, theme_id):
    """Helper function to set theme in all config files."""
    profile_path = get_profile_path_by_index(profile_index)
    set_active_theme_in_prefs(profile_path, theme_id)
    set_active_theme_in_extensions(profile_path, theme_id)
    set_active_theme_in_addon_startup(profile_path, theme_id)

def auto_switch_theme():
    """Switch theme based on time of day."""
    hour = datetime.now().hour
    
    # Light theme during day (6 AM to 6 PM)
    # Dark theme at night (6 PM to 6 AM)
    if 6 <= hour < 18:
        theme_id = "firefox-compact-light@mozilla.org"
        print(f"Daytime detected ({hour}:00). Switching to light theme...")
    else:
        theme_id = "firefox-compact-dark@mozilla.org"
        print(f"Nighttime detected ({hour}:00). Switching to dark theme...")
    
    set_theme(0, theme_id)
    print(f"Theme set to: {theme_id}")
    print("Restart Firefox to apply changes.")

# Run the auto-switcher
auto_switch_theme()
```

**To run automatically:**

Create a cron job (Linux/macOS):
```bash
# Edit crontab
crontab -e

# Add entry to run at 6 AM and 6 PM daily
0 6,18 * * * /usr/bin/python3 /path/to/your/theme_scheduler.py
```

Or use Windows Task Scheduler for Windows systems.

---

## Multi-Profile Management

Switch themes across multiple Firefox profiles at once.

```python
from theme_my_fox import (
    list_profiles,
    get_profile_path_by_index,
    set_active_theme_in_prefs,
    set_active_theme_in_extensions,
    set_active_theme_in_addon_startup
)

def set_theme_all_profiles(theme_id):
    """Set the same theme for all Firefox profiles."""
    profiles = list_profiles()
    
    if not profiles:
        print("No Firefox profiles found!")
        return
    
    print(f"Setting theme '{theme_id}' for all profiles...")
    
    for i, profile in enumerate(profiles):
        try:
            print(f"\nProfile {i}: {profile['name']}")
            profile_path = get_profile_path_by_index(i)
            
            set_active_theme_in_prefs(profile_path, theme_id)
            set_active_theme_in_extensions(profile_path, theme_id)
            set_active_theme_in_addon_startup(profile_path, theme_id)
            
            print(f"  ✓ Theme set successfully")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print("\nAll profiles updated! Restart Firefox to see changes.")

# Set dark theme for all profiles
set_theme_all_profiles("firefox-compact-dark@mozilla.org")
```

---

## Theme Backup and Restore

Save and restore theme configurations.

### Backup Theme Configuration

```python
import json
from datetime import datetime
from theme_my_fox import (
    get_profile_path_by_index,
    get_available_themes
)

def backup_theme_config(profile_index, backup_file=None):
    """Backup theme configuration to a JSON file."""
    if backup_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"theme_backup_{timestamp}.json"
    
    profile_path = get_profile_path_by_index(profile_index)
    themes = get_available_themes(profile_path)
    
    # Find active theme
    active_theme = None
    for theme in themes:
        if theme.get("active"):
            active_theme = theme["id"]
            break
    
    backup_data = {
        "backup_date": datetime.now().isoformat(),
        "profile_index": profile_index,
        "active_theme": active_theme,
        "available_themes": [t["id"] for t in themes]
    }
    
    with open(backup_file, "w") as f:
        json.dump(backup_data, f, indent=2)
    
    print(f"Theme configuration backed up to: {backup_file}")
    print(f"Active theme: {active_theme}")
    return backup_file

# Create backup
backup_backup_theme_config(0)
```

### Restore Theme Configuration

```python
import json
from theme_my_fox import (
    get_profile_path_by_index,
    set_active_theme_in_prefs,
    set_active_theme_in_extensions,
    set_active_theme_in_addon_startup
)

def restore_theme_config(backup_file):
    """Restore theme configuration from a backup file."""
    with open(backup_file, "r") as f:
        backup_data = json.load(f)
    
    profile_index = backup_data["profile_index"]
    theme_id = backup_data["active_theme"]
    
    if theme_id is None:
        print("No active theme found in backup!")
        return
    
    print(f"Restoring theme: {theme_id}")
    print(f"To profile index: {profile_index}")
    
    profile_path = get_profile_path_by_index(profile_index)
    
    set_active_theme_in_prefs(profile_path, theme_id)
    set_active_theme_in_extensions(profile_path, theme_id)
    set_active_theme_in_addon_startup(profile_path, theme_id)
    
    print(f"Theme restored! Restart Firefox to see changes.")

# Restore from backup
restore_theme_config("theme_backup_20260205_103000.json")
```

---

## Custom Theme Switcher Script

Interactive command-line theme switcher.

```python
from theme_my_fox import (
    list_profiles,
    get_profile_path_by_index,
    get_available_themes,
    set_active_theme_in_prefs,
    set_active_theme_in_extensions,
    set_active_theme_in_addon_startup
)

def interactive_theme_switcher():
    """Interactive theme switcher with menu."""
    # Step 1: Select profile
    profiles = list_profiles()
    
    if not profiles:
        print("No Firefox profiles found!")
        return
    
    print("=== Firefox Theme Switcher ===\n")
    print("Available profiles:")
    for i, profile in enumerate(profiles):
        print(f"  {i}: {profile['name']}")
    
    profile_idx = int(input("\nSelect profile number: "))
    profile_path = get_profile_path_by_index(profile_idx)
    
    # Step 2: Get available themes
    themes = get_available_themes(profile_path)
    
    if not themes:
        print("No themes found for this profile!")
        return
    
    print(f"\nAvailable themes for '{profiles[profile_idx]['name']}':")
    for i, theme in enumerate(themes):
        active_marker = " (current)" if theme.get("active") else ""
        print(f"  {i}: {theme['id']}{active_marker}")
    
    theme_idx = int(input("\nSelect theme number: "))
    selected_theme = themes[theme_idx]["id"]
    
    # Step 3: Apply theme
    print(f"\nApplying theme: {selected_theme}")
    
    set_active_theme_in_prefs(profile_path, selected_theme)
    set_active_theme_in_extensions(profile_path, selected_theme)
    set_active_theme_in_addon_startup(profile_path, selected_theme)
    
    print("\n✓ Theme applied successfully!")
    print("Please restart Firefox to see the changes.")

# Run the interactive switcher
if __name__ == "__main__":
    try:
        interactive_theme_switcher()
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
    except Exception as e:
        print(f"\nError: {e}")
```

---

## Integration with System Theme

Automatically sync Firefox theme with your system's dark/light mode.

### Linux (GNOME)

```python
import subprocess
from theme_my_fox import (
    get_profile_path_by_index,
    set_active_theme_in_prefs,
    set_active_theme_in_extensions,
    set_active_theme_in_addon_startup
)

def get_gnome_theme():
    """Get current GNOME theme preference."""
    try:
        result = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
            capture_output=True,
            text=True
        )
        theme = result.stdout.strip().strip("'")
        return "dark" if "dark" in theme else "light"
    except Exception:
        return None

def sync_with_system_theme():
    """Sync Firefox theme with system theme."""
    system_theme = get_gnome_theme()
    
    if system_theme is None:
        print("Could not detect system theme")
        return
    
    print(f"System theme: {system_theme}")
    
    # Map system theme to Firefox theme
    if system_theme == "dark":
        theme_id = "firefox-compact-dark@mozilla.org"
    else:
        theme_id = "firefox-compact-light@mozilla.org"
    
    print(f"Setting Firefox theme: {theme_id}")
    
    profile_path = get_profile_path_by_index(0)
    set_active_theme_in_prefs(profile_path, theme_id)
    set_active_theme_in_extensions(profile_path, theme_id)
    set_active_theme_in_addon_startup(profile_path, theme_id)
    
    print("Firefox theme synced with system!")
    print("Restart Firefox to see changes.")

# Run sync
sync_with_system_theme()
```

### macOS

```python
import subprocess
from theme_my_fox import (
    get_profile_path_by_index,
    set_active_theme_in_prefs,
    set_active_theme_in_extensions,
    set_active_theme_in_addon_startup
)

def get_macos_theme():
    """Get current macOS theme preference."""
    try:
        result = subprocess.run(
            ["defaults", "read", "-g", "AppleInterfaceStyle"],
            capture_output=True,
            text=True
        )
        # If the command succeeds, dark mode is enabled
        return "dark" if result.returncode == 0 else "light"
    except Exception:
        return "light"

def sync_with_system_theme():
    """Sync Firefox theme with macOS system theme."""
    system_theme = get_macos_theme()
    print(f"macOS theme: {system_theme}")
    
    if system_theme == "dark":
        theme_id = "firefox-compact-dark@mozilla.org"
    else:
        theme_id = "firefox-compact-light@mozilla.org"
    
    print(f"Setting Firefox theme: {theme_id}")
    
    profile_path = get_profile_path_by_index(0)
    set_active_theme_in_prefs(profile_path, theme_id)
    set_active_theme_in_extensions(profile_path, theme_id)
    set_active_theme_in_addon_startup(profile_path, theme_id)
    
    print("Firefox theme synced!")
    print("Restart Firefox to see changes.")

# Run sync
sync_with_system_theme()
```

---

## Error Handling Example

Robust theme switcher with error handling:

```python
from pathlib import Path
from theme_my_fox import (
    list_profiles,
    get_profile_path_by_index,
    get_available_themes,
    set_active_theme_in_prefs,
    set_active_theme_in_extensions,
    set_active_theme_in_addon_startup
)

def safe_theme_switch(profile_index, theme_id):
    """Switch theme with comprehensive error handling."""
    try:
        # Validate profile exists
        profiles = list_profiles()
        if not profiles:
            print("Error: No Firefox profiles found!")
            print("Make sure Firefox is installed.")
            return False
        
        if profile_index < 0 or profile_index >= len(profiles):
            print(f"Error: Profile index {profile_index} is out of range.")
            print(f"Available indices: 0 to {len(profiles) - 1}")
            return False
        
        # Get profile path
        profile_path = get_profile_path_by_index(profile_index)
        
        # Check if profile directory exists
        if not Path(profile_path).exists():
            print(f"Error: Profile directory not found: {profile_path}")
            return False
        
        # Validate theme exists
        themes = get_available_themes(profile_path)
        theme_ids = [t["id"] for t in themes]
        
        if theme_id not in theme_ids:
            print(f"Error: Theme '{theme_id}' not found in profile.")
            print(f"Available themes: {', '.join(theme_ids)}")
            return False
        
        # Apply theme
        print(f"Switching to theme: {theme_id}")
        set_active_theme_in_prefs(profile_path, theme_id)
        set_active_theme_in_extensions(profile_path, theme_id)
        set_active_theme_in_addon_startup(profile_path, theme_id)
        
        print("✓ Theme switched successfully!")
        print("Restart Firefox to see changes.")
        return True
        
    except PermissionError as e:
        print(f"Error: Permission denied. {e}")
        print("Make sure Firefox is closed and you have write permissions.")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

# Use the safe switcher
success = safe_theme_switch(0, "firefox-compact-dark@mozilla.org")
if not success:
    print("\nTheme switch failed!")
```

---

**See Also:**
- [API Reference](API-Reference) for detailed function documentation
- [Troubleshooting](Troubleshooting) for common issues
- [FAQ](FAQ) for frequently asked questions
