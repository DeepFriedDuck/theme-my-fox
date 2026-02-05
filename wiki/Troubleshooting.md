# Troubleshooting

Common issues and their solutions when using Theme My Fox.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Profile Issues](#profile-issues)
- [Theme Switching Issues](#theme-switching-issues)
- [File Permission Issues](#file-permission-issues)
- [Firefox Compatibility](#firefox-compatibility)
- [Platform-Specific Issues](#platform-specific-issues)

---

## Installation Issues

### Issue: `pip install` fails with "No module named 'pip'"`

**Cause:** pip is not installed or not in PATH.

**Solution:**
```bash
# Use Python's ensurepip module
python -m ensurepip --upgrade

# Or install pip manually
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

### Issue: "Python version mismatch" or "requires Python 3.11+"

**Cause:** Theme My Fox requires Python 3.11 or higher.

**Solution:**
1. Check your Python version:
```bash
python --version
# or
python3 --version
```

2. If you have an older version, install Python 3.11+:
   - **Linux**: Use your package manager (e.g., `sudo apt install python3.11`)
   - **macOS**: Use Homebrew (`brew install python@3.11`) or download from python.org
   - **Windows**: Download from [python.org](https://www.python.org/downloads/)

3. Use the specific Python version:
```bash
python3.11 -m pip install git+https://github.com/DeepFriedDuck/theme-my-fox.git
```

### Issue: "git: command not found"

**Cause:** Git is not installed.

**Solution:**
```bash
# Linux (Debian/Ubuntu)
sudo apt-get install git

# Linux (RedHat/CentOS)
sudo yum install git

# macOS
brew install git

# Windows: Download from https://git-scm.com/
```

### Issue: lz4 installation fails

**Cause:** Missing build dependencies for the lz4 Python package.

**Solution:**
```bash
# Linux (Debian/Ubuntu)
sudo apt-get install python3-dev build-essential

# Linux (RedHat/CentOS)
sudo yum install python3-devel gcc

# macOS (usually not needed with Xcode Command Line Tools)
xcode-select --install

# Then retry installation
pip install git+https://github.com/DeepFriedDuck/theme-my-fox.git
```

---

## Profile Issues

### Issue: `IndexError: profile index out of range`

**Cause:** The profile index you specified doesn't exist.

**Solution:**
```python
from theme_my_fox import list_profiles

# First, check available profiles
profiles = list_profiles()
print(f"Found {len(profiles)} profile(s):")
for i, profile in enumerate(profiles):
    print(f"  {i}: {profile['name']}")

# Then use a valid index (0 to len(profiles)-1)
```

### Issue: "No Firefox profiles found" or empty list returned

**Cause:** Firefox is not installed, or profiles.ini is missing/corrupted.

**Solution:**

1. **Verify Firefox is installed:**
```bash
# Linux
which firefox
ls ~/.mozilla/firefox/

# Check if profiles.ini exists
cat ~/.mozilla/firefox/profiles.ini
```

2. **Launch Firefox at least once** to create the default profile:
```bash
firefox &
# Close Firefox after it opens
```

3. **Verify Theme My Fox can find the Firefox path:**
```python
from theme_my_fox import get_firefox_path
import os

firefox_path = get_firefox_path()
print(f"Firefox path: {firefox_path}")
print(f"Exists: {os.path.exists(firefox_path)}")

profiles_ini = firefox_path / "profiles.ini"
print(f"profiles.ini exists: {os.path.exists(profiles_ini)}")
```

### Issue: Profile path is wrong or doesn't exist

**Cause:** The profile directory was deleted or moved.

**Solution:**

1. Check if the profile directory actually exists:
```python
from pathlib import Path
from theme_my_fox import list_profiles

profiles = list_profiles()
for profile in profiles:
    path = Path(profile['path'])
    print(f"{profile['name']}: {path.exists()}")
```

2. If missing, either:
   - Restore the profile from backup
   - Create a new profile in Firefox
   - Remove the invalid profile entry from `profiles.ini`

---

## Theme Switching Issues

### Issue: Theme doesn't change after running the script

**Cause:** Firefox was running when you made changes, or Firefox hasn't been restarted.

**Solution:**

1. **Always close Firefox completely** before running theme switch scripts:
```bash
# Linux
pkill firefox

# macOS
killall Firefox

# Windows (PowerShell)
Stop-Process -Name firefox
```

2. **Run your theme switching script**

3. **Start Firefox** to see the changes

### Issue: "Theme ID not found" or theme_id doesn't work

**Cause:** The theme ID is incorrect or the theme isn't installed.

**Solution:**

1. **List available themes** to get the correct ID:
```python
from theme_my_fox import get_profile_path_by_index, get_available_themes

profile_path = get_profile_path_by_index(0)
themes = get_available_themes(profile_path)

print("Available theme IDs:")
for theme in themes:
    print(f"  - {theme['id']}")
```

2. **Use the exact ID** (copy-paste to avoid typos):
```python
# ✓ Correct
theme_id = "firefox-compact-dark@mozilla.org"

# ✗ Wrong (missing @mozilla.org)
theme_id = "firefox-compact-dark"
```

3. **Install the theme in Firefox** if it's not available:
   - Open Firefox
   - Go to Add-ons (Ctrl+Shift+A)
   - Search for and install the theme you want
   - Run `get_available_themes()` again to see the new theme

### Issue: Theme changes but some elements still show old theme

**Cause:** Not all configuration files were updated.

**Solution:**

Always update **all three** configuration files:
```python
from theme_my_fox import (
    get_profile_path_by_index,
    set_active_theme_in_prefs,
    set_active_theme_in_extensions,
    set_active_theme_in_addon_startup
)

profile_path = get_profile_path_by_index(0)
theme_id = "firefox-compact-dark@mozilla.org"

# Must call all three
set_active_theme_in_prefs(profile_path, theme_id)
set_active_theme_in_extensions(profile_path, theme_id)
set_active_theme_in_addon_startup(profile_path, theme_id)
```

### Issue: `ValueError: Invalid magic number` when decompressing

**Cause:** The file is not a valid Firefox LZ4 file, or it's corrupted.

**Solution:**

1. **Verify the file is a Firefox LZ4 file:**
```bash
# Check the magic header
hexdump -C addonStartup.json.lz4 | head -1
# Should show: 6d 6f 7a 4c 7a 34 30 00 (mozLz40\0)
```

2. **Don't try to decompress regular files:**
   - Only decompress files with `.lz4` extension from Firefox profile
   - Common Firefox LZ4 files: `addonStartup.json.lz4`, `search.json.mozlz4`

3. **If corrupted, restore from backup** or let Firefox regenerate:
```bash
# Backup the corrupted file
mv addonStartup.json.lz4 addonStartup.json.lz4.backup

# Start Firefox - it will regenerate the file
firefox &
```

---

## File Permission Issues

### Issue: `PermissionError: [Errno 13] Permission denied`

**Cause:** No write permission to Firefox profile directory.

**Solution:**

1. **Check file permissions:**
```bash
ls -la ~/.mozilla/firefox/*.default*/prefs.js
```

2. **Fix permissions if needed:**
```bash
# Make profile directory writable
chmod u+w ~/.mozilla/firefox/*.default*

# Fix ownership if needed
sudo chown -R $USER:$USER ~/.mozilla/firefox/
```

3. **Close Firefox** before running scripts (Firefox locks files)

4. **Don't run scripts as root/sudo** (can mess up permissions)

### Issue: Changes are reverted after Firefox starts

**Cause:** Firefox sync or another process is overwriting changes.

**Solution:**

1. **Disable Firefox Sync temporarily:**
   - Open Firefox
   - Go to Settings → Sync
   - Turn off theme syncing

2. **Check for profile lock:**
```bash
# Remove lock file if Firefox isn't actually running
rm ~/.mozilla/firefox/*.default*/.parentlock
```

---

## Firefox Compatibility

### Issue: Works on Linux but not macOS/Windows

**Cause:** Current version is optimized for Linux. Firefox paths differ by OS.

**Current Firefox paths:**
- **Linux**: `~/.mozilla/firefox/`
- **macOS**: `~/Library/Application Support/Firefox/`
- **Windows**: `%APPDATA%\Mozilla\Firefox\`

**Solution for macOS:**

Temporarily modify the Firefox path:
```python
from pathlib import Path
from theme_my_fox import core

# Override the get_firefox_path function for macOS
def get_firefox_path_macos():
    return Path.home() / "Library" / "Application Support" / "Firefox"

core.get_firefox_path = get_firefox_path_macos

# Now use Theme My Fox normally
from theme_my_fox import list_profiles
profiles = list_profiles()
```

**Solution for Windows:**

```python
from pathlib import Path
import os
from theme_my_fox import core

# Override for Windows
def get_firefox_path_windows():
    appdata = os.environ.get('APPDATA')
    return Path(appdata) / "Mozilla" / "Firefox"

core.get_firefox_path = get_firefox_path_windows

# Now use Theme My Fox normally
from theme_my_fox import list_profiles
profiles = list_profiles()
```

---

## Platform-Specific Issues

### Linux: "No such file or directory: profiles.ini"

**Solution:**
```bash
# Check Firefox path
ls -la ~/.mozilla/firefox/

# If missing, Firefox may not be installed via official method
# Snap/Flatpak versions may use different paths
# Try: ~/.var/app/org.mozilla.firefox/.mozilla/firefox/
```

### macOS: Library folder not visible

**Solution:**
```bash
# Make Library folder visible in Finder
chflags nohidden ~/Library/

# Or use Terminal to access
cd ~/Library/Application\ Support/Firefox/
```

### Windows: APPDATA path issues

**Solution:**
```python
import os

# Verify APPDATA is set
appdata = os.environ.get('APPDATA')
print(f"APPDATA: {appdata}")

# Manual path if needed
firefox_path = Path("C:/Users/YourUsername/AppData/Roaming/Mozilla/Firefox")
```

---

## Debugging Tips

### Enable verbose output

```python
import logging

logging.basicConfig(level=logging.DEBUG)

# Now run your code - you'll see more detailed output
```

### Verify file contents manually

```bash
# Check prefs.js
grep "activeThemeID" ~/.mozilla/firefox/*.default*/prefs.js

# Check extensions.json (formatted)
python -m json.tool ~/.mozilla/firefox/*.default*/extensions.json | grep -A5 '"type": "theme"'

# Decompress and check addonStartup.json.lz4
cd /tmp
python3 << 'EOF'
from theme_my_fox import decompress
decompress("/home/user/.mozilla/firefox/xyz.default/addonStartup.json.lz4", "addon.json")
EOF
python -m json.tool addon.json | less
```

### Test with a fresh profile

```python
# Create a test profile in Firefox
# Tools → More Tools → Profile Manager
# Create new profile named "test"

# Then use it
from theme_my_fox import list_profiles

profiles = list_profiles()
for i, p in enumerate(profiles):
    if p['name'] == 'test':
        print(f"Test profile index: {i}")
```

---

## Still Having Issues?

If none of these solutions work:

1. **Check the logs** for error messages
2. **Create a minimal reproducible example**
3. **Open an issue** on [GitHub](https://github.com/DeepFriedDuck/theme-my-fox/issues) with:
   - Your OS and Python version
   - Complete error message
   - Code that reproduces the issue
   - Output of `list_profiles()` and `get_firefox_path()`

---

**See Also:**
- [FAQ](FAQ) for frequently asked questions
- [API Reference](API-Reference) for function documentation
- [Usage Examples](Usage-Examples) for working code examples
