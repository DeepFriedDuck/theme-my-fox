# Compression API

This page documents the LZ4 compression utilities for working with Firefox's compressed configuration files.

## Overview

Firefox uses LZ4 compression for certain configuration files to improve performance. Theme My Fox provides utilities to compress and decompress these files using Firefox's special format.

## Firefox LZ4 Format

Firefox's LZ4 files have a special 8-byte header:
```
mozLz40\0
```

This header identifies the file as a Firefox LZ4-compressed file. Theme My Fox handles this automatically.

## Functions

### decompress()

Decompress a Firefox LZ4 file to a regular file.

**Signature:**
```python
def decompress(src: str, dest: str) -> None
```

**Parameters:**
- `src` (str): Path to the source LZ4 file (e.g., `"addonStartup.json.lz4"`)
- `dest` (str): Path to the destination file (e.g., `"addonStartup.json"`)

**Returns:**
- None

**Raises:**
- `ValueError`: If the source file doesn't have the correct magic number (`mozLz40\0`)
- `FileNotFoundError`: If source file doesn't exist
- Other IO exceptions for file operation errors

**Example:**
```python
from theme_my_fox import decompress

# Decompress addonStartup.json.lz4 to addonStartup.json
decompress("addonStartup.json.lz4", "addonStartup.json")
print("File decompressed successfully")
```

**Full Example:**
```python
from pathlib import Path
from theme_my_fox import get_profile_path_by_index, decompress

# Get profile path
profile_path = get_profile_path_by_index(0)
lz4_file = profile_path / "addonStartup.json.lz4"
output_file = Path("/tmp/addonStartup.json")

# Decompress
decompress(str(lz4_file), str(output_file))

# Now you can read the JSON
import json
with open(output_file) as f:
    data = json.load(f)
    print(json.dumps(data, indent=2))
```

**What it does:**
1. Opens the source LZ4 file
2. Verifies the `mozLz40\0` magic header
3. Decompresses the remaining data using LZ4
4. Writes the decompressed data to the destination file

**Notes:**
- The magic number check ensures you're decompressing a valid Firefox LZ4 file
- Both `src` and `dest` can be strings or Path objects
- The destination file will be overwritten if it exists

---

### compress()

Compress a file using Firefox's LZ4 format.

**Signature:**
```python
def compress(src: str, dest: str) -> None
```

**Parameters:**
- `src` (str): Path to the source file (e.g., `"addonStartup.json"`)
- `dest` (str): Path to the destination LZ4 file (e.g., `"addonStartup.json.lz4"`)

**Returns:**
- None

**Raises:**
- `FileNotFoundError`: If source file doesn't exist
- Other IO exceptions for file operation errors

**Example:**
```python
from theme_my_fox import compress

# Compress addonStartup.json to addonStartup.json.lz4
compress("addonStartup.json", "addonStartup.json.lz4")
print("File compressed successfully")
```

**Full Example:**
```python
from pathlib import Path
import json
from theme_my_fox import get_profile_path_by_index, compress

# Create or modify JSON data
data = {
    "app-profile": {
        "addons": {
            "theme1@example.com": {
                "type": "theme",
                "enabled": True
            }
        }
    }
}

# Write JSON to temporary file
temp_file = Path("/tmp/addonStartup.json")
with open(temp_file, "w") as f:
    json.dump(data, f)

# Compress it
profile_path = get_profile_path_by_index(0)
lz4_file = profile_path / "addonStartup.json.lz4"
compress(str(temp_file), str(lz4_file))
print("Compressed and saved to profile")
```

**What it does:**
1. Reads the entire source file into memory
2. Compresses it using LZ4
3. Prepends the `mozLz40\0` magic header
4. Writes the result to the destination file

**Notes:**
- The magic header is added automatically
- Both `src` and `dest` can be strings or Path objects
- The destination file will be overwritten if it exists

## Common Use Cases

### Reading Firefox Configuration

```python
from pathlib import Path
import json
from theme_my_fox import get_profile_path_by_index, decompress

def read_addon_startup(profile_index=0):
    """Read and parse addonStartup.json.lz4."""
    profile_path = get_profile_path_by_index(profile_index)
    lz4_file = profile_path / "addonStartup.json.lz4"
    temp_file = Path("/tmp/addonStartup.json")
    
    # Decompress
    decompress(str(lz4_file), str(temp_file))
    
    # Parse JSON
    with open(temp_file) as f:
        data = json.load(f)
    
    return data

# Usage
data = read_addon_startup()
print(json.dumps(data, indent=2))
```

### Modifying Firefox Configuration

```python
from pathlib import Path
import json
from theme_my_fox import get_profile_path_by_index, decompress, compress

def modify_addon_startup(profile_index, modifier_func):
    """
    Safely modify addonStartup.json.lz4.
    
    Args:
        profile_index: Profile index
        modifier_func: Function that takes JSON data and returns modified data
    """
    profile_path = get_profile_path_by_index(profile_index)
    lz4_file = profile_path / "addonStartup.json.lz4"
    temp_file = Path("/tmp/addonStartup.json")
    
    # Decompress
    decompress(str(lz4_file), str(temp_file))
    
    # Read and modify
    with open(temp_file) as f:
        data = json.load(f)
    
    data = modifier_func(data)
    
    # Write back
    with open(temp_file, "w") as f:
        json.dump(data, f)
    
    # Compress
    compress(str(temp_file), str(lz4_file))

# Usage example: Enable a specific addon
def enable_addon(data):
    addons = data.get("app-profile", {}).get("addons", {})
    if "my-addon@example.com" in addons:
        addons["my-addon@example.com"]["enabled"] = True
    return data

modify_addon_startup(0, enable_addon)
```

### Backup and Restore

```python
from pathlib import Path
import shutil
from theme_my_fox import get_profile_path_by_index, decompress, compress

def backup_compressed_file(profile_index, filename):
    """Backup a compressed Firefox file."""
    profile_path = get_profile_path_by_index(profile_index)
    source = profile_path / filename
    backup = profile_path / f"{filename}.backup"
    
    shutil.copy(source, backup)
    print(f"Backed up {filename} to {backup}")

def restore_compressed_file(profile_index, filename):
    """Restore a compressed Firefox file from backup."""
    profile_path = get_profile_path_by_index(profile_index)
    backup = profile_path / f"{filename}.backup"
    dest = profile_path / filename
    
    if backup.exists():
        shutil.copy(backup, dest)
        print(f"Restored {filename} from backup")
    else:
        print(f"No backup found for {filename}")

# Usage
backup_compressed_file(0, "addonStartup.json.lz4")
# ... make changes ...
restore_compressed_file(0, "addonStartup.json.lz4")
```

## Advanced Usage

### Roundtrip Conversion

Decompress, modify, and recompress in one go:

```python
from pathlib import Path
import json
import tempfile
from theme_my_fox import decompress, compress

def roundtrip_edit(lz4_path, edit_func):
    """
    Decompress, edit, and recompress an LZ4 file.
    
    Args:
        lz4_path: Path to the LZ4 file
        edit_func: Function that receives JSON data and returns modified data
    """
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as temp:
        temp_path = temp.name
    
    try:
        # Decompress
        decompress(str(lz4_path), temp_path)
        
        # Load, edit, save
        with open(temp_path, 'r') as f:
            data = json.load(f)
        
        data = edit_func(data)
        
        with open(temp_path, 'w') as f:
            json.dump(data, f)
        
        # Compress back
        compress(temp_path, str(lz4_path))
        
    finally:
        # Clean up temp file
        Path(temp_path).unlink(missing_ok=True)

# Usage
from theme_my_fox import get_profile_path_by_index

profile_path = get_profile_path_by_index(0)
lz4_file = profile_path / "addonStartup.json.lz4"

def my_edit(data):
    # Modify data here
    data["custom_field"] = "custom_value"
    return data

roundtrip_edit(lz4_file, my_edit)
```

### Inspecting Compressed Files

```python
from theme_my_fox import decompress
import json
from pathlib import Path

def inspect_lz4_json(lz4_path):
    """Pretty-print a compressed JSON file."""
    temp = Path("/tmp/temp_inspect.json")
    
    try:
        decompress(str(lz4_path), str(temp))
        with open(temp) as f:
            data = json.load(f)
        print(json.dumps(data, indent=2))
    finally:
        temp.unlink(missing_ok=True)

# Usage
from theme_my_fox import get_profile_path_by_index
profile_path = get_profile_path_by_index(0)
inspect_lz4_json(profile_path / "addonStartup.json.lz4")
```

### File Size Comparison

```python
from pathlib import Path
from theme_my_fox import decompress

def compare_sizes(lz4_path):
    """Compare compressed vs uncompressed size."""
    lz4_size = Path(lz4_path).stat().st_size
    
    temp = Path("/tmp/temp.json")
    decompress(str(lz4_path), str(temp))
    json_size = temp.stat().st_size
    temp.unlink()
    
    ratio = (1 - lz4_size / json_size) * 100
    
    print(f"Compressed:   {lz4_size:,} bytes")
    print(f"Uncompressed: {json_size:,} bytes")
    print(f"Compression:  {ratio:.1f}%")

# Usage
from theme_my_fox import get_profile_path_by_index
profile_path = get_profile_path_by_index(0)
compare_sizes(profile_path / "addonStartup.json.lz4")
```

## Error Handling

### Robust Compression/Decompression

```python
from pathlib import Path
from theme_my_fox import compress, decompress

def safe_decompress(src, dest):
    """Decompress with error handling."""
    try:
        decompress(src, dest)
        return True
    except ValueError as e:
        print(f"Error: Invalid LZ4 file - {e}")
        return False
    except FileNotFoundError:
        print(f"Error: File not found: {src}")
        return False
    except PermissionError:
        print(f"Error: Permission denied")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def safe_compress(src, dest):
    """Compress with error handling."""
    try:
        compress(src, dest)
        return True
    except FileNotFoundError:
        print(f"Error: File not found: {src}")
        return False
    except PermissionError:
        print(f"Error: Permission denied")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

# Usage
if safe_decompress("file.lz4", "file.json"):
    print("Decompression successful")
else:
    print("Decompression failed")
```

## Troubleshooting

### Invalid Magic Number Error

**Problem:** `ValueError: Invalid magic number`

**Cause:** The file is not a valid Firefox LZ4 file.

**Solutions:**
1. Verify the file is actually compressed:
   ```python
   with open("file.lz4", "rb") as f:
       header = f.read(8)
       print(header)  # Should be b'mozLz40\x00'
   ```

2. Check if it's a regular JSON file instead:
   ```python
   import json
   try:
       with open("file.json") as f:
           json.load(f)
       print("This is a regular JSON file, not compressed")
   except:
       print("File is not valid JSON")
   ```

### File Not Found

Make sure Firefox profile exists and file is present:
```python
from pathlib import Path
from theme_my_fox import get_profile_path_by_index

profile_path = get_profile_path_by_index(0)
lz4_file = profile_path / "addonStartup.json.lz4"

if lz4_file.exists():
    print(f"File exists: {lz4_file}")
else:
    print(f"File not found: {lz4_file}")
    print("This is normal if Firefox hasn't created it yet")
```

### Permission Errors

Close Firefox before modifying files:
```bash
# Check if Firefox is running
ps aux | grep firefox
# or on Windows:
tasklist | findstr firefox
```

## Performance Notes

- LZ4 is very fast - compression/decompression is typically not a bottleneck
- For large files, consider using streams instead of loading everything into memory
- The library loads entire files into memory, which is fine for Firefox config files (typically < 1MB)

## See Also

- [Theme Management API](Theme-Management-API.md) - Uses compression for `addonStartup.json.lz4`
- [Basic Concepts](Basic-Concepts.md) - Understanding LZ4 compression
- [Advanced Usage](Advanced-Usage.md) - More compression techniques
