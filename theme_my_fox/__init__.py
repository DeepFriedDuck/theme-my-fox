"""Theme My Fox - core package

Expose the high-level helpers from the internal `core` module and a
package-level `__version__` for consumers and CI.
"""

from importlib.metadata import PackageNotFoundError, version as _get_version
from pathlib import Path

try:
	__version__ = _get_version("theme-my-fox")
except PackageNotFoundError:
	try:
		import tomllib

		py = Path(__file__).resolve().parents[1] / "pyproject.toml"
		__version__ = tomllib.loads(py.read_text())["project"]["version"]
	except Exception:
		__version__ = "0.0.0"

from .core import (
	compress,
	decompress,
	get_firefox_path,
	list_profiles,
	get_profile_path_by_index,
	get_available_themes,
	set_active_theme_in_prefs,
	set_active_theme_in_extensions,
	set_active_theme_in_addon_startup,
)

__all__ = [
	"__version__",
	"compress",
	"decompress",
	"get_firefox_path",
	"list_profiles",
	"get_profile_path_by_index",
	"get_available_themes",
	"set_active_theme_in_prefs",
	"set_active_theme_in_extensions",
	"set_active_theme_in_addon_startup",
]

