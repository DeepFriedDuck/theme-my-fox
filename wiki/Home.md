# Theme My Fox 🦊

Welcome to the **Theme My Fox** wiki! This Python library enables programmatic management of Firefox themes, allowing you to automate theme switching, manage Firefox profiles, and work with Firefox's internal configuration files.

## Quick Links

- 📦 **[Installation Guide](Installation)** - Get started with theme-my-fox
- 📖 **[API Reference](API-Reference)** - Complete function documentation
- 💡 **[Usage Examples](Usage-Examples)** - Practical code examples
- 🔧 **[Troubleshooting](Troubleshooting)** - Common issues and solutions
- ❓ **[FAQ](FAQ)** - Frequently asked questions
- 🤝 **[Contributing](Contributing)** - How to contribute to the project

## What is Theme My Fox?

Theme My Fox is a Python library that provides a simple, pythonic interface for:

- 🎨 **Theme Management** - Programmatically switch between installed Firefox themes
- 🗜️ **LZ4 Compression** - Work with Firefox's LZ4-compressed configuration files
- 📁 **Profile Management** - List and access Firefox profiles
- 🔧 **Configuration Editing** - Modify Firefox preferences and extension settings

## Key Features

### Easy Theme Switching
```python
from theme_my_fox import (
    get_profile_path_by_index,
    set_active_theme_in_prefs,
    set_active_theme_in_extensions,
    set_active_theme_in_addon_startup
)

profile_path = get_profile_path_by_index(0)
theme_id = "firefox-compact-dark@mozilla.org"

set_active_theme_in_prefs(profile_path, theme_id)
set_active_theme_in_extensions(profile_path, theme_id)
set_active_theme_in_addon_startup(profile_path, theme_id)
```

### Profile Discovery
```python
from theme_my_fox import list_profiles

profiles = list_profiles()
for i, profile in enumerate(profiles):
    print(f"{i}: {profile['name']} - {profile['path']}")
```

### LZ4 File Handling
```python
from theme_my_fox import compress, decompress

# Work with Firefox's compressed configuration files
decompress("addonStartup.json.lz4", "addonStartup.json")
compress("addonStartup.json", "addonStartup.json.lz4")
```

## How It Works

Firefox stores theme information in multiple files within each profile directory:

1. **`prefs.js`** - User preferences including `extensions.activeThemeID`
2. **`extensions.json`** - Addon metadata including installed themes
3. **`addonStartup.json.lz4`** - Compressed startup configuration with enabled addons

Theme My Fox provides functions to read and modify these files while handling Firefox's special LZ4 compression format (with `mozLz40` magic header).

## Use Cases

- 🌗 **Automatic theme switching** based on time of day, system theme, or any other trigger
- 🔄 **Theme synchronization** across multiple Firefox profiles
- 💾 **Backup and restore** theme configurations
- 🤖 **Automation scripts** for Firefox customization
- 🧪 **Testing** different theme configurations programmatically

## Requirements

- Python 3.11 or higher
- lz4 >= 4.4.5
- Firefox installed (for actual theme switching functionality)

## Getting Help

- Check the **[Troubleshooting](Troubleshooting)** page for common issues
- Review **[Usage Examples](Usage-Examples)** for practical code samples
- See **[FAQ](FAQ)** for frequently asked questions
- Open an issue on [GitHub](https://github.com/DeepFriedDuck/theme-my-fox/issues)

## Project Links

- **GitHub Repository**: https://github.com/DeepFriedDuck/theme-my-fox
- **License**: WTFPL (Do What The Fuck You Want To Public License)

---

Made with 🦊 by [DeepFriedDuck](https://github.com/DeepFriedDuck)
