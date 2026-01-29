from pathlib import Path
import tempfile
import configparser
import json
import lz4.block
import argparse
import sys
import os
from typing import List, Dict, Optional


def compress(src, dest):
    with open(src, "rb") as file:
        compressed = lz4.block.compress(file.read())
        output_file = b"mozLz40\0" + compressed
    with open(dest, "wb") as file:
        file.write(output_file)


def decompress(src, dest):
    with open(src, "rb") as file:
        if file.read(8) != b"mozLz40\0":
            raise ValueError("Invalid magic number")
        string_to_write = lz4.block.decompress(file.read())
    with open(dest, "wb") as file:
        file.write(string_to_write)


def get_firefox_path() -> Path:
    """Return the Path to the user's Firefox directory (~/.mozilla/firefox)."""
    return Path.home() / ".mozilla" / "firefox"


def list_profiles() -> List[Dict[str, str]]:
    """Parse `profiles.ini` and return a list of profiles as dicts with `name` and `path`.

    The returned `path` is absolute.
    """
    firefox_path = get_firefox_path()
    config = configparser.ConfigParser()
    config.read(firefox_path / "profiles.ini")
    profiles: List[Dict[str, str]] = []
    for section in config.sections():
        if not config.has_option(section, "Path"):
            continue
        raw_path = config.get(section, "Path")
        is_relative = config.get(section, "IsRelative", fallback="1")
        if is_relative in ("1", "true", "True"):
            profile_path = firefox_path / raw_path
        else:
            profile_path = Path(raw_path)
        profiles.append({"name": config.get(section, "Name", fallback=section), "path": str(profile_path)})
    return profiles


def get_profile_path_by_index(index: int) -> Path:
    """Return the Path for profile at 0-based index from `list_profiles()`.

    Raises IndexError if not found.
    """
    profiles = list_profiles()
    if index < 0 or index >= len(profiles):
        raise IndexError("profile index out of range")
    return Path(profiles[index]["path"])


def get_available_themes(profile_path: Path) -> List[Dict]:
    """Return the list of theme addon objects from `extensions.json` for the given profile.

    If `extensions.json` does not exist, returns an empty list.
    """
    extensions_file = Path(profile_path) / "extensions.json"
    themes: List[Dict] = []
    try:
        with open(extensions_file, "r") as fh:
            data = json.load(fh)
            for addon in data.get("addons", []):
                if addon.get("type") == "theme":
                    themes.append(addon)
    except FileNotFoundError:
        return []
    return themes


def set_active_theme_in_prefs(profile_path: Path, theme_id: str) -> None:
    """Set `extensions.activeThemeID` in `prefs.js` to `theme_id`.

    If the preference line does not exist, append it.
    """
    prefs_js_path = Path(profile_path) / "prefs.js"
    new_content = ""
    found = False
    with open(prefs_js_path, "r") as fh:
        for line in fh:
            if 'user_pref("extensions.activeThemeID", ' in line:
                new_content += f'user_pref("extensions.activeThemeID", "{theme_id}");\n'
                found = True
            else:
                new_content += line
    if not found:
        new_content += f'user_pref("extensions.activeThemeID", "{theme_id}");\n'
    with open(prefs_js_path, "w") as fh:
        fh.write(new_content)


def set_active_theme_in_extensions(profile_path: Path, theme_id: str) -> None:
    """Update `extensions.json` to enable the chosen theme and disable others."""
    extension_json_path = Path(profile_path) / "extensions.json"
    with open(extension_json_path, "r") as fh:
        data = json.load(fh)
    for addon in data.get("addons", []):
        if addon.get("type") == "theme":
            if addon.get("id") == theme_id:
                addon["userDisabled"] = False
                addon["active"] = True
            else:
                addon["userDisabled"] = True
                addon["active"] = False
    with open(extension_json_path, "w") as fh:
        json.dump(data, fh)


def set_active_theme_in_addon_startup(profile_path: Path, theme_id: str) -> None:
    """Update `addonStartup.json.lz4` enabling only `theme_id`.

    This function will decompress to a temp file, modify it, then recompress.
    """
    temp_path = Path(tempfile.gettempdir()) / "addonStartup.json"
    lz4_src = Path(profile_path) / "addonStartup.json.lz4"
    # decompress to temp file
    decompress(lz4_src, temp_path)
    with open(temp_path, "r") as fh:
        data = json.load(fh)
    addons = data.get("app-profile", {}).get("addons", {})
    for aid, addon in list(addons.items()):
        if addon.get("type") == "theme":
            addon["enabled"] = (aid == theme_id)
    with open(temp_path, "w") as fh:
        json.dump(data, fh)
    # recompress back to profile
    compress(temp_path, lz4_src)



__all__ = [
    "decompress",
    "compress",
    "get_firefox_path",
    "list_profiles",
    "get_profile_path_by_index",
    "get_available_themes",
    "set_active_theme_in_prefs",
    "set_active_theme_in_extensions",
    "set_active_theme_in_addon_startup"
]