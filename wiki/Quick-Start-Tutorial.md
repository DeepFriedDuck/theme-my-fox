# Quick Start Tutorial

This tutorial will get you up and running with Theme My Fox in minutes.

## Step 1: Import the Library

```python
import theme_my_fox
```

## Step 2: List Your Firefox Profiles

First, let's see what Firefox profiles you have:

```python
from theme_my_fox import list_profiles

profiles = list_profiles()
print(f"Found {len(profiles)} Firefox profile(s):\n")

for i, profile in enumerate(profiles):
    print(f"[{i}] {profile['name']}")
    print(f"    Path: {profile['path']}\n")
```

**Output example:**
```
Found 2 Firefox profile(s):

[0] default-release
    Path: /home/user/.mozilla/firefox/abc123.default-release

[1] dev-profile
    Path: /home/user/.mozilla/firefox/xyz789.dev-profile
```

## Step 3: Choose a Profile

For this tutorial, we'll use profile index 0 (the first profile):

```python
from theme_my_fox import get_profile_path_by_index

profile_index = 0  # Use the first profile
profile_path = get_profile_path_by_index(profile_index)
print(f"Using profile: {profile_path}")
```

## Step 4: See Available Themes

Let's check what themes are installed in this profile:

```python
from theme_my_fox import get_available_themes

themes = get_available_themes(profile_path)
print(f"\nFound {len(themes)} theme(s):\n")

for theme in themes:
    theme_id = theme.get('id', 'unknown')
    theme_name = theme.get('defaultLocale', {}).get('name', 'Unknown')
    enabled = theme.get('active', False)
    status = "✓ ACTIVE" if enabled else ""
    print(f"  {theme_name} {status}")
    print(f"    ID: {theme_id}\n")
```

**Output example:**
```
Found 3 theme(s):

  Firefox Light ✓ ACTIVE
    ID: firefox-compact-light@mozilla.org

  Firefox Dark
    ID: firefox-compact-dark@mozilla.org

  System Theme
    ID: default-theme@mozilla.org
```

## Step 5: Switch to a Different Theme

⚠️ **Important:** Close Firefox before running this code!

```python
from theme_my_fox import (
    set_active_theme_in_prefs,
    set_active_theme_in_extensions,
    set_active_theme_in_addon_startup
)

# Choose a theme ID from the list above
new_theme_id = "firefox-compact-dark@mozilla.org"

# Apply the theme
print(f"Switching to theme: {new_theme_id}")

set_active_theme_in_prefs(profile_path, new_theme_id)
print("  ✓ Updated prefs.js")

set_active_theme_in_extensions(profile_path, new_theme_id)
print("  ✓ Updated extensions.json")

set_active_theme_in_addon_startup(profile_path, new_theme_id)
print("  ✓ Updated addonStartup.json.lz4")

print("\n✓ Theme switch complete! Restart Firefox to see changes.")
```

## Step 6: Restart Firefox and Verify

1. **Close** Firefox (if it's running)
2. **Run your script** to switch the theme
3. **Start** Firefox
4. The new theme should be active!

## Complete Example Script

Here's everything together:

```python
#!/usr/bin/env python3
"""Simple theme switcher example."""

from theme_my_fox import (
    list_profiles,
    get_profile_path_by_index,
    get_available_themes,
    set_active_theme_in_prefs,
    set_active_theme_in_extensions,
    set_active_theme_in_addon_startup,
)

def main():
    # List profiles
    profiles = list_profiles()
    if not profiles:
        print("No Firefox profiles found!")
        return
    
    print("Firefox Profiles:")
    for i, p in enumerate(profiles):
        print(f"  [{i}] {p['name']}")
    
    # Use first profile
    profile_path = get_profile_path_by_index(0)
    print(f"\nUsing profile: {profiles[0]['name']}")
    
    # List themes
    themes = get_available_themes(profile_path)
    if not themes:
        print("No themes found!")
        return
    
    print(f"\nAvailable themes:")
    for i, theme in enumerate(themes):
        theme_id = theme.get('id')
        name = theme.get('defaultLocale', {}).get('name', theme_id)
        active = " (active)" if theme.get('active') else ""
        print(f"  [{i}] {name}{active}")
    
    # Switch to first non-active theme
    for theme in themes:
        if not theme.get('active'):
            theme_id = theme.get('id')
            print(f"\nSwitching to: {theme_id}")
            
            set_active_theme_in_prefs(profile_path, theme_id)
            set_active_theme_in_extensions(profile_path, theme_id)
            set_active_theme_in_addon_startup(profile_path, theme_id)
            
            print("✓ Done! Restart Firefox to see changes.")
            break
    else:
        print("\nCurrent theme is already active.")

if __name__ == "__main__":
    main()
```

## Common Mistakes

### Firefox Still Running

**Problem:** Theme doesn't change after running the script.

**Solution:** Make sure Firefox is completely closed. Check for background processes:

```bash
# Linux/macOS
ps aux | grep firefox

# Windows
tasklist | findstr firefox
```

### Wrong Theme ID

**Problem:** `KeyError` or theme doesn't switch.

**Solution:** Use exact theme IDs from `get_available_themes()`. Don't guess the ID!

### Profile Index Out of Range

**Problem:** `IndexError: profile index out of range`

**Solution:** Check how many profiles you have first:

```python
profiles = list_profiles()
print(f"Valid indices: 0 to {len(profiles) - 1}")
```

## Next Steps

Now that you've completed the quick start:

- Learn about [Profile Management API](Profile-Management-API.md)
- Explore [Theme Management API](Theme-Management-API.md)
- Check out [Common Use Cases](Common-Use-Cases.md) for more examples

## Getting Help

If something doesn't work:
1. Check the [Troubleshooting Guide](Troubleshooting-Guide.md)
2. Review [Basic Concepts](Basic-Concepts.md)
3. [Open an issue](https://github.com/DeepFriedDuck/theme-my-fox/issues) on GitHub
