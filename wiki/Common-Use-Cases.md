# Common Use Cases

Practical examples and recipes for using Theme My Fox.

## Theme Scheduler

### Time-Based Theme Switching

Automatically switch between light and dark themes based on time of day:

```python
#!/usr/bin/env python3
"""Switch Firefox theme based on time of day."""

from datetime import datetime
from theme_my_fox import (
    get_profile_path_by_index,
    set_active_theme_in_prefs,
    set_active_theme_in_extensions,
    set_active_theme_in_addon_startup,
)

def switch_theme(profile_index, theme_id):
    """Switch to specified theme."""
    profile_path = get_profile_path_by_index(profile_index)
    set_active_theme_in_prefs(profile_path, theme_id)
    set_active_theme_in_extensions(profile_path, theme_id)
    set_active_theme_in_addon_startup(profile_path, theme_id)

def auto_theme_by_time(profile_index=0):
    """Switch theme based on time of day."""
    hour = datetime.now().hour
    
    # Light theme during day (6 AM - 6 PM)
    if 6 <= hour < 18:
        theme_id = "firefox-compact-light@mozilla.org"
        theme_name = "Light"
    # Dark theme at night
    else:
        theme_id = "firefox-compact-dark@mozilla.org"
        theme_name = "Dark"
    
    print(f"Time is {datetime.now().strftime('%I:%M %p')}")
    print(f"Switching to {theme_name} theme...")
    
    switch_theme(profile_index, theme_id)
    print("✓ Theme switched. Restart Firefox to apply.")

if __name__ == "__main__":
    auto_theme_by_time()
```

**Usage with cron (Linux):**
```bash
# Edit crontab
crontab -e

# Add these lines to switch at 6 AM and 6 PM
0 6 * * * /usr/bin/python3 /path/to/auto_theme.py
0 18 * * * /usr/bin/python3 /path/to/auto_theme.py
```

### Sunrise/Sunset Based Switching

Use astronomical data for more accurate day/night switching:

```python
#!/usr/bin/env python3
"""Switch theme based on sunrise/sunset times."""

from datetime import datetime
from theme_my_fox import (
    get_profile_path_by_index,
    set_active_theme_in_prefs,
    set_active_theme_in_extensions,
    set_active_theme_in_addon_startup,
)

# You can use libraries like 'astral' or 'suntime' for real sunrise/sunset
# pip install astral
from astral import LocationInfo
from astral.sun import sun

def is_daytime(latitude, longitude):
    """Check if it's currently daytime based on sun position."""
    city = LocationInfo("MyCity", "MyRegion", "UTC", latitude, longitude)
    s = sun(city.observer, date=datetime.now())
    
    now = datetime.now(s['sunrise'].tzinfo)
    return s['sunrise'] < now < s['sunset']

def auto_theme_by_sun(profile_index=0, latitude=51.5, longitude=-0.1):
    """Switch theme based on sunrise/sunset."""
    if is_daytime(latitude, longitude):
        theme_id = "firefox-compact-light@mozilla.org"
        theme_name = "Light"
    else:
        theme_id = "firefox-compact-dark@mozilla.org"
        theme_name = "Dark"
    
    print(f"Switching to {theme_name} theme based on sun position...")
    
    profile_path = get_profile_path_by_index(profile_index)
    set_active_theme_in_prefs(profile_path, theme_id)
    set_active_theme_in_extensions(profile_path, theme_id)
    set_active_theme_in_addon_startup(profile_path, theme_id)
    
    print("✓ Theme switched. Restart Firefox to apply.")

if __name__ == "__main__":
    # London coordinates (example)
    auto_theme_by_sun(latitude=51.5074, longitude=-0.1278)
```

## Backup and Restore

### Backup Current Theme Settings

```python
#!/usr/bin/env python3
"""Backup Firefox theme configuration."""

import json
from datetime import datetime
from pathlib import Path
from theme_my_fox import get_profile_path_by_index, get_available_themes

def backup_theme_config(profile_index=0, backup_dir="backups"):
    """Backup theme configuration to JSON file."""
    profile_path = get_profile_path_by_index(profile_index)
    themes = get_available_themes(profile_path)
    
    # Get active theme
    active_theme = None
    for theme in themes:
        if theme.get('active'):
            active_theme = theme.get('id')
            break
    
    backup_data = {
        "timestamp": datetime.now().isoformat(),
        "profile_path": str(profile_path),
        "active_theme": active_theme,
        "available_themes": [t.get('id') for t in themes]
    }
    
    # Create backup directory
    Path(backup_dir).mkdir(exist_ok=True)
    
    # Save backup
    filename = f"theme_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = Path(backup_dir) / filename
    
    with open(filepath, 'w') as f:
        json.dump(backup_data, f, indent=2)
    
    print(f"✓ Backup saved to: {filepath}")
    print(f"  Active theme: {active_theme}")
    print(f"  Available themes: {len(backup_data['available_themes'])}")
    
    return filepath

if __name__ == "__main__":
    backup_theme_config()
```

### Restore Theme from Backup

```python
#!/usr/bin/env python3
"""Restore Firefox theme from backup."""

import json
from pathlib import Path
from theme_my_fox import (
    get_profile_path_by_index,
    get_available_themes,
    set_active_theme_in_prefs,
    set_active_theme_in_extensions,
    set_active_theme_in_addon_startup,
)

def restore_theme_config(backup_file, profile_index=0):
    """Restore theme configuration from backup file."""
    with open(backup_file) as f:
        backup_data = json.load(f)
    
    active_theme = backup_data.get('active_theme')
    if not active_theme:
        print("No active theme found in backup")
        return False
    
    # Verify theme is available
    profile_path = get_profile_path_by_index(profile_index)
    themes = get_available_themes(profile_path)
    theme_ids = [t.get('id') for t in themes]
    
    if active_theme not in theme_ids:
        print(f"Error: Theme '{active_theme}' not available in profile")
        print(f"Available themes: {theme_ids}")
        return False
    
    # Restore theme
    print(f"Restoring theme: {active_theme}")
    print(f"From backup: {backup_file}")
    
    set_active_theme_in_prefs(profile_path, active_theme)
    set_active_theme_in_extensions(profile_path, active_theme)
    set_active_theme_in_addon_startup(profile_path, active_theme)
    
    print("✓ Theme restored. Restart Firefox to apply.")
    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: restore_theme.py <backup_file>")
        sys.exit(1)
    
    restore_theme_config(sys.argv[1])
```

## Command-Line Interface

### Simple CLI Theme Switcher

```python
#!/usr/bin/env python3
"""Command-line theme switcher for Firefox."""

import argparse
from theme_my_fox import (
    list_profiles,
    get_profile_path_by_index,
    get_available_themes,
    set_active_theme_in_prefs,
    set_active_theme_in_extensions,
    set_active_theme_in_addon_startup,
)

def list_profiles_cmd():
    """List all Firefox profiles."""
    profiles = list_profiles()
    print(f"Found {len(profiles)} profile(s):\n")
    for i, profile in enumerate(profiles):
        print(f"[{i}] {profile['name']}")
        print(f"    {profile['path']}\n")

def list_themes_cmd(profile_index):
    """List themes in a profile."""
    profile_path = get_profile_path_by_index(profile_index)
    themes = get_available_themes(profile_path)
    
    print(f"Themes in profile {profile_index}:\n")
    for theme in themes:
        theme_id = theme.get('id')
        name = theme.get('defaultLocale', {}).get('name', theme_id)
        active = " ✓" if theme.get('active') else ""
        print(f"{name}{active}")
        print(f"  ID: {theme_id}\n")

def switch_theme_cmd(profile_index, theme_id):
    """Switch to specified theme."""
    profile_path = get_profile_path_by_index(profile_index)
    
    # Verify theme exists
    themes = get_available_themes(profile_path)
    if not any(t.get('id') == theme_id for t in themes):
        print(f"Error: Theme '{theme_id}' not found")
        print("\nAvailable themes:")
        for t in themes:
            print(f"  {t.get('id')}")
        return False
    
    print(f"Switching to theme: {theme_id}")
    set_active_theme_in_prefs(profile_path, theme_id)
    set_active_theme_in_extensions(profile_path, theme_id)
    set_active_theme_in_addon_startup(profile_path, theme_id)
    print("✓ Theme switched. Restart Firefox to apply.")
    return True

def main():
    parser = argparse.ArgumentParser(
        description="Firefox Theme Switcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list-profiles
  %(prog)s list-themes -p 0
  %(prog)s switch -p 0 -t firefox-compact-dark@mozilla.org
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # list-profiles command
    subparsers.add_parser('list-profiles', help='List all Firefox profiles')
    
    # list-themes command
    list_themes_parser = subparsers.add_parser('list-themes', help='List themes in profile')
    list_themes_parser.add_argument('-p', '--profile', type=int, default=0,
                                    help='Profile index (default: 0)')
    
    # switch command
    switch_parser = subparsers.add_parser('switch', help='Switch to a theme')
    switch_parser.add_argument('-p', '--profile', type=int, default=0,
                               help='Profile index (default: 0)')
    switch_parser.add_argument('-t', '--theme', required=True,
                               help='Theme ID to switch to')
    
    args = parser.parse_args()
    
    if args.command == 'list-profiles':
        list_profiles_cmd()
    elif args.command == 'list-themes':
        list_themes_cmd(args.profile)
    elif args.command == 'switch':
        switch_theme_cmd(args.profile, args.theme)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
```

**Usage:**
```bash
# List profiles
./theme_switcher.py list-profiles

# List themes
./theme_switcher.py list-themes -p 0

# Switch theme
./theme_switcher.py switch -p 0 -t firefox-compact-dark@mozilla.org
```

## Theme Toggle

### Quick Dark/Light Toggle

```python
#!/usr/bin/env python3
"""Toggle between dark and light themes."""

from theme_my_fox import (
    get_profile_path_by_index,
    get_available_themes,
    set_active_theme_in_prefs,
    set_active_theme_in_extensions,
    set_active_theme_in_addon_startup,
)

LIGHT_THEME = "firefox-compact-light@mozilla.org"
DARK_THEME = "firefox-compact-dark@mozilla.org"

def get_current_theme(profile_index=0):
    """Get currently active theme ID."""
    profile_path = get_profile_path_by_index(profile_index)
    themes = get_available_themes(profile_path)
    for theme in themes:
        if theme.get('active'):
            return theme.get('id')
    return None

def toggle_theme(profile_index=0):
    """Toggle between light and dark theme."""
    current = get_current_theme(profile_index)
    
    if current == LIGHT_THEME:
        new_theme = DARK_THEME
        theme_name = "Dark"
    else:
        new_theme = LIGHT_THEME
        theme_name = "Light"
    
    print(f"Switching to {theme_name} theme...")
    
    profile_path = get_profile_path_by_index(profile_index)
    set_active_theme_in_prefs(profile_path, new_theme)
    set_active_theme_in_extensions(profile_path, new_theme)
    set_active_theme_in_addon_startup(profile_path, new_theme)
    
    print("✓ Theme toggled. Restart Firefox to apply.")

if __name__ == "__main__":
    toggle_theme()
```

## Random Theme

### Random Theme Selector

```python
#!/usr/bin/env python3
"""Select a random theme."""

import random
from theme_my_fox import (
    get_profile_path_by_index,
    get_available_themes,
    set_active_theme_in_prefs,
    set_active_theme_in_extensions,
    set_active_theme_in_addon_startup,
)

def random_theme(profile_index=0):
    """Switch to a random theme."""
    profile_path = get_profile_path_by_index(profile_index)
    themes = get_available_themes(profile_path)
    
    if not themes:
        print("No themes found!")
        return
    
    # Choose random theme
    theme = random.choice(themes)
    theme_id = theme.get('id')
    theme_name = theme.get('defaultLocale', {}).get('name', theme_id)
    
    print(f"Selected random theme: {theme_name}")
    print(f"ID: {theme_id}")
    
    set_active_theme_in_prefs(profile_path, theme_id)
    set_active_theme_in_extensions(profile_path, theme_id)
    set_active_theme_in_addon_startup(profile_path, theme_id)
    
    print("✓ Theme switched. Restart Firefox to apply.")

if __name__ == "__main__":
    random_theme()
```

## Multi-Profile Management

### Sync Theme Across Profiles

```python
#!/usr/bin/env python3
"""Sync theme across all Firefox profiles."""

from theme_my_fox import (
    list_profiles,
    get_profile_path_by_index,
    get_available_themes,
    set_active_theme_in_prefs,
    set_active_theme_in_extensions,
    set_active_theme_in_addon_startup,
)

def sync_theme_to_all_profiles(theme_id):
    """Set the same theme in all profiles."""
    profiles = list_profiles()
    
    print(f"Syncing theme '{theme_id}' to {len(profiles)} profile(s)...\n")
    
    for i, profile in enumerate(profiles):
        try:
            profile_path = get_profile_path_by_index(i)
            
            # Check if theme is available
            themes = get_available_themes(profile_path)
            if not any(t.get('id') == theme_id for t in themes):
                print(f"⚠ Skipping '{profile['name']}': theme not available")
                continue
            
            # Set theme
            set_active_theme_in_prefs(profile_path, theme_id)
            set_active_theme_in_extensions(profile_path, theme_id)
            set_active_theme_in_addon_startup(profile_path, theme_id)
            
            print(f"✓ Updated '{profile['name']}'")
            
        except Exception as e:
            print(f"✗ Error updating '{profile['name']}': {e}")
    
    print("\n✓ Sync complete. Restart Firefox to apply.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: sync_theme.py <theme_id>")
        print("\nExample:")
        print("  sync_theme.py firefox-compact-dark@mozilla.org")
        sys.exit(1)
    
    sync_theme_to_all_profiles(sys.argv[1])
```

## Integration Examples

### Desktop Notification

```python
#!/usr/bin/env python3
"""Theme switcher with desktop notification."""

import subprocess
from theme_my_fox import (
    get_profile_path_by_index,
    set_active_theme_in_prefs,
    set_active_theme_in_extensions,
    set_active_theme_in_addon_startup,
)

def notify(title, message):
    """Send desktop notification (Linux)."""
    try:
        subprocess.run(['notify-send', title, message])
    except FileNotFoundError:
        print(f"{title}: {message}")

def switch_theme_with_notification(profile_index, theme_id, theme_name):
    """Switch theme and show notification."""
    try:
        profile_path = get_profile_path_by_index(profile_index)
        set_active_theme_in_prefs(profile_path, theme_id)
        set_active_theme_in_extensions(profile_path, theme_id)
        set_active_theme_in_addon_startup(profile_path, theme_id)
        
        notify("Firefox Theme Changed", f"Switched to {theme_name}")
        return True
    except Exception as e:
        notify("Theme Switch Failed", str(e))
        return False

if __name__ == "__main__":
    switch_theme_with_notification(
        0,
        "firefox-compact-dark@mozilla.org",
        "Dark Theme"
    )
```

## See Also

- [Theme Management API](Theme-Management-API.md) - API reference
- [Quick Start Tutorial](Quick-Start-Tutorial.md) - Getting started
- [Troubleshooting Guide](Troubleshooting-Guide.md) - Common issues
