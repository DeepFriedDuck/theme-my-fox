# FAQ - Frequently Asked Questions

Common questions about Theme My Fox.

## General Questions

### What is Theme My Fox?

Theme My Fox is a Python library that allows you to programmatically manage Firefox themes. You can switch themes, list available themes, manage profiles, and work with Firefox's LZ4-compressed configuration files - all from Python code.

### Why would I use this?

Some use cases:
- **Automatic theme switching** based on time of day (dark theme at night, light during day)
- **System theme integration** - sync Firefox theme with your OS theme
- **Multi-profile management** - apply the same theme across all your Firefox profiles
- **Automation and scripting** - integrate Firefox theme changes into your workflows
- **Backup and restore** - save and restore theme configurations

### Does this work with Firefox running?

**No!** Firefox must be completely closed before running Theme My Fox functions. Firefox caches configuration files in memory, and changes won't take effect until Firefox is restarted.

Always:
1. Close Firefox completely
2. Run your Theme My Fox script
3. Restart Firefox to see changes

### Is this safe to use?

Yes, when used correctly:
- ✅ It modifies only Firefox configuration files
- ✅ Changes are reversible (you can switch back to any installed theme)
- ✅ Firefox validates and regenerates corrupted files automatically
- ⚠️ Always close Firefox before running scripts
- ⚠️ Consider backing up your profile first (especially for development)

---

## Installation Questions

### What Python version do I need?

Python 3.11 or higher. Check your version:
```bash
python --version
```

### Can I use pip install theme-my-fox?

Not yet. Currently, you must install from the GitHub repository:
```bash
pip install git+https://github.com/DeepFriedDuck/theme-my-fox.git
```

A PyPI release may come in the future.

### Do I need to install Firefox separately?

Yes! Theme My Fox is a library for managing existing Firefox installations. You need:
- Firefox installed on your system
- At least one Firefox profile created (happens automatically on first Firefox launch)

---

## Compatibility Questions

### What operating systems are supported?

- **Linux**: ✅ Fully supported
- **macOS**: ⚠️ Partial support (requires manual Firefox path override)
- **Windows**: ⚠️ Partial support (requires manual Firefox path override)

The library is currently optimized for Linux. See [Troubleshooting](Troubleshooting#firefox-compatibility) for workarounds on other platforms.

### Does this work with Firefox ESR, Beta, Nightly?

It should work with any Firefox variant, as long as:
- They use the standard Firefox profile structure
- Configuration files are in the expected format

However, different Firefox versions may use different profile paths. You may need to adjust the Firefox path accordingly.

### Does this work with Firefox installed via Snap/Flatpak?

Possibly, but the profile path may differ:
- **Snap**: `~/snap/firefox/common/.mozilla/firefox/`
- **Flatpak**: `~/.var/app/org.mozilla.firefox/.mozilla/firefox/`

You can override the Firefox path in your code (see [Troubleshooting](Troubleshooting#firefox-compatibility)).

---

## Usage Questions

### How do I switch themes?

You need to update all three configuration files:
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

See [Usage Examples](Usage-Examples#switch-theme-complete) for more details.

### How do I find the correct theme ID?

Use `get_available_themes()`:
```python
from theme_my_fox import get_profile_path_by_index, get_available_themes

profile_path = get_profile_path_by_index(0)
themes = get_available_themes(profile_path)

for theme in themes:
    print(theme['id'])
```

Theme IDs look like:
- `firefox-compact-light@mozilla.org`
- `firefox-compact-dark@mozilla.org`
- `{custom-theme-uuid}@mozilla.org`

### Can I use this with custom themes?

Yes! Any theme installed in Firefox (built-in or custom) can be managed with Theme My Fox. Just use the theme's ID from `get_available_themes()`.

### How many profiles can I manage?

Theme My Fox can manage all Firefox profiles found in `profiles.ini`. There's no limit.

### Can I create new profiles with Theme My Fox?

No, Theme My Fox only manages existing profiles. To create a new profile:
1. Use Firefox's Profile Manager (`firefox -ProfileManager`)
2. Or create one through Firefox settings
3. Then use Theme My Fox to manage it

---

## Technical Questions

### What files does Theme My Fox modify?

For each profile, it can modify:
1. **`prefs.js`** - User preferences (sets `extensions.activeThemeID`)
2. **`extensions.json`** - Addon metadata (enables/disables themes)
3. **`addonStartup.json.lz4`** - Compressed startup config (theme enabled state)

### What is the LZ4 compression for?

Firefox uses LZ4 compression with a special header (`mozLz40\0`) for certain configuration files. Theme My Fox provides `compress()` and `decompress()` functions to work with these files.

Common LZ4 files in Firefox:
- `addonStartup.json.lz4`
- `search.json.mozlz4`

### Can I use Theme My Fox in production?

Yes, but consider:
- ✅ It's stable for the documented use cases
- ⚠️ Always test on a test profile first
- ⚠️ Have backups of important profiles
- ⚠️ The library is relatively new (test thoroughly for your use case)

### Is there a CLI tool?

Not officially, but you can easily create one using Theme My Fox! See the [Custom Theme Switcher Script](Usage-Examples#custom-theme-switcher-script) example.

### Can I contribute to Theme My Fox?

Yes! See the [Contributing](Contributing) guide for how to contribute.

---

## Troubleshooting Questions

### Theme doesn't change - what should I check?

1. **Is Firefox completely closed?**
   ```bash
   pkill firefox  # Linux
   killall Firefox  # macOS
   ```

2. **Did you update all three config files?**
   - `set_active_theme_in_prefs()`
   - `set_active_theme_in_extensions()`
   - `set_active_theme_in_addon_startup()`

3. **Is the theme ID correct?**
   - Use `get_available_themes()` to verify
   - Theme IDs are case-sensitive and must match exactly

4. **Did you restart Firefox after making changes?**

### I get "IndexError: profile index out of range"

This means the profile index doesn't exist. Check available profiles:
```python
from theme_my_fox import list_profiles

profiles = list_profiles()
print(f"Found {len(profiles)} profile(s)")
for i, p in enumerate(profiles):
    print(f"{i}: {p['name']}")
```

Use index 0 to `len(profiles) - 1`.

### I get "ValueError: Invalid magic number"

You're trying to decompress a file that isn't a Firefox LZ4 file. Only decompress files with:
- `.lz4` extension
- Located in Firefox profile directories
- Created by Firefox

### I get "PermissionError"

1. Close Firefox completely
2. Check file permissions on your Firefox profile
3. Don't run scripts with sudo
4. Make sure you're the owner of the Firefox profile directory

See [Troubleshooting](Troubleshooting#file-permission-issues) for more details.

---

## Best Practices

### Should I close Firefox before running scripts?

**Always!** Firefox caches configuration in memory and locks files. Changes won't work correctly if Firefox is running.

### Should I backup my profile before using Theme My Fox?

For peace of mind, yes. Especially if you're:
- Testing new features
- Running scripts for the first time
- Modifying critical profiles

Backup:
```bash
tar -czf firefox-profile-backup.tar.gz ~/.mozilla/firefox/
```

### Can I automate theme switching?

Yes! Common approaches:
- **Cron job** (Linux/macOS) - run at specific times
- **Task Scheduler** (Windows) - run at specific times
- **System theme hooks** - trigger on OS theme change
- **Python scripts** - integrate into your own tools

See [Usage Examples](Usage-Examples#theme-scheduler) for code samples.

### How often can I switch themes?

As often as you want, but remember:
- Firefox must be closed for changes to apply
- Changes require a Firefox restart to take effect
- Frequent restarts may be inconvenient

Consider batching changes or switching during Firefox downtime.

---

## License Questions

### What license does Theme My Fox use?

WTFPL (Do What The Fuck You Want To Public License) - a very permissive license. You can:
- Use it commercially
- Modify it
- Distribute it
- Use it for any purpose

No attribution required, but appreciated! 🦊

### Can I use this in my commercial project?

Yes! The WTFPL license allows commercial use without restrictions.

---

## Questions Not Answered Here?

- Check the [Troubleshooting](Troubleshooting) page
- Review the [API Reference](API-Reference)
- Look at [Usage Examples](Usage-Examples)
- Open an issue on [GitHub](https://github.com/DeepFriedDuck/theme-my-fox/issues)

---

**Last Updated:** 2026-02-05
