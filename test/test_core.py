import json
import tempfile
from pathlib import Path
import shutil

import pytest

from theme_my_fox import core


def test_compress_decompress_roundtrip(tmp_path):
    src = tmp_path / "orig.bin"
    src.write_bytes(b"hello world" * 10)
    compressed = tmp_path / "c.lz4"
    decompressed = tmp_path / "out.bin"

    core.compress(src, compressed)
    core.decompress(compressed, decompressed)

    assert src.read_bytes() == decompressed.read_bytes()


def test_list_profiles_and_get_by_index(monkeypatch, tmp_path):
    # create fake firefox path with profiles.ini
    firefox_dir = tmp_path / "firefox"
    firefox_dir.mkdir()
    profiles_ini = firefox_dir / "profiles.ini"
    profiles_ini.write_text(
        """
[Profile0]
Name=default
IsRelative=1
Path=profile0

[Profile1]
Name=other
IsRelative=0
Path=/absolute/path/profile1
"""
    )
    # create relative profile dir
    (firefox_dir / "profile0").mkdir()

    monkeypatch.setattr(core, "get_firefox_path", lambda: firefox_dir)

    profiles = core.list_profiles()
    assert any(p["name"] == "default" for p in profiles)
    assert any(p["name"] == "other" for p in profiles)

    # get_profile_path_by_index
    p0 = core.get_profile_path_by_index(0)
    assert str(p0).endswith("profile0")
    with pytest.raises(IndexError):
        core.get_profile_path_by_index(10)


def test_get_available_themes(tmp_path):
    profile = tmp_path / "p"
    profile.mkdir()
    ex = profile / "extensions.json"
    data = {"addons": [{"id": "a1", "type": "theme"}, {"id": "b1", "type": "extension"}]}
    ex.write_text(json.dumps(data))

    themes = core.get_available_themes(profile)
    assert len(themes) == 1
    assert themes[0]["id"] == "a1"


def test_set_active_theme_in_prefs(tmp_path):
    profile = tmp_path / "p"
    profile.mkdir()
    prefs = profile / "prefs.js"
    prefs.write_text('// prefs\n')

    core.set_active_theme_in_prefs(profile, "theme.x")
    content = prefs.read_text()
    assert 'user_pref("extensions.activeThemeID", "theme.x");' in content

    # replace existing
    prefs.write_text('user_pref("extensions.activeThemeID", "old");\n')
    core.set_active_theme_in_prefs(profile, "theme.new")
    assert 'user_pref("extensions.activeThemeID", "theme.new");' in prefs.read_text()


def test_set_active_theme_in_extensions(tmp_path):
    profile = tmp_path / "p"
    profile.mkdir()
    ex = profile / "extensions.json"
    data = {"addons": [{"id": "t1", "type": "theme", "userDisabled": True, "active": False}, {"id": "t2", "type": "theme", "userDisabled": False, "active": True}, {"id": "e1", "type": "extension"}]}
    ex.write_text(json.dumps(data))

    core.set_active_theme_in_extensions(profile, "t1")
    after = json.loads(ex.read_text())
    for a in after["addons"]:
        if a.get("type") == "theme":
            if a.get("id") == "t1":
                assert a["userDisabled"] is False
                assert a["active"] is True
            else:
                assert a["userDisabled"] is True
                assert a["active"] is False


def test_set_active_theme_in_addon_startup(tmp_path):
    profile = tmp_path / "p"
    profile.mkdir()
    lz4_file = profile / "addonStartup.json.lz4"

    # create addonStartup.json content
    data = {"app-profile": {"addons": {"t1": {"type": "theme", "enabled": False}, "t2": {"type": "theme", "enabled": True}, "e1": {"type": "extension", "enabled": True}}}}

    tmp_json = tmp_path / "addonStartup.json"
    tmp_json.write_text(json.dumps(data))

    # compress into profile
    core.compress(tmp_json, lz4_file)

    core.set_active_theme_in_addon_startup(profile, "t1")

    # decompress and inspect
    out = tmp_path / "out.json"
    core.decompress(lz4_file, out)
    after = json.loads(out.read_text())
    addons = after.get("app-profile", {}).get("addons", {})
    assert addons["t1"]["enabled"] is True
    assert addons["t2"]["enabled"] is False
