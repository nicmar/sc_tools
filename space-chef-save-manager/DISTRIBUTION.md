# Distribution Guide

## Building Standalone Executables

### Overview
PyInstaller creates **completely standalone executables** that include:
- Python interpreter (no Python installation needed)
- All your code
- Tkinter GUI library
- All dependencies

Users can run the executable **without installing anything**.

## Building Process

### 1. Install PyInstaller (One-time setup)
```bash
pip install pyinstaller
```

### 2. Build for Your Platform

**On macOS:**
```bash
python build.py
# Creates: dist/SpaceChefSaveManager
# Size: ~10-15 MB
```

**On Windows:**
```bash
python build.py
# Creates: dist/SpaceChefSaveManager.exe
# Size: ~10-15 MB
```

**On Linux:**
```bash
python build.py
# Creates: dist/SpaceChefSaveManager
# Size: ~10-15 MB
```

### 3. Test the Executable

**Before distributing, test that it works on a clean machine:**

1. Copy the executable to a different location
2. Run it WITHOUT Python installed
3. Verify all features work

## Important Notes

### Cross-Platform Building
⚠️ **You MUST build on each target platform:**
- To distribute for Windows → Build on Windows
- To distribute for Mac → Build on macOS
- To distribute for Linux → Build on Linux

PyInstaller cannot cross-compile.

### File Size
The executable will be **10-15 MB** because it includes:
- Python runtime: ~8 MB
- Tkinter libraries: ~2 MB
- Your code: < 1 MB

This is normal and expected for PyInstaller apps.

### Antivirus Warnings
Some antivirus software flags PyInstaller executables as suspicious (false positive).
To mitigate:
- Build with `--clean` flag
- Submit to antivirus vendors for whitelisting
- Code-sign your executable (requires certificate)

## Distribution Package

Create a distribution folder:

```
SpaceChefSaveManager-v1.0.0/
├── SpaceChefSaveManager.exe (or .app on Mac)
└── README.txt (user instructions)
```

### Example README.txt for Users

```
Space Chef Save Manager v1.0.0

Quick Start:
1. Double-click SpaceChefSaveManager to launch
2. The tool will auto-detect your save location
3. Select a player to manage backups

No installation required!

Default Save Locations:
- Windows: C:\Users\<YourName>\AppData\Roaming\BlueGooGames\Space Chef\Saves
- Mac: ~/Library/Application Support/BlueGooGames/Space Chef/Saves
- Linux: ~/.local/share/BlueGooGames/Space Chef/Saves

Troubleshooting:
- If save location not found, use "Browse..." button
- Make sure Space Chef has been run at least once

Support: [Your contact info]
```

## Verification Checklist

Before distributing, verify:

✅ Executable runs without Python installed
✅ All features work (scan saves, view backups, restore, create backup)
✅ Folder open buttons work
✅ Error messages display correctly
✅ File picker works
✅ Progress dialogs show during restore

## Advanced: Code Signing (Optional)

### macOS
```bash
codesign --force --deep --sign "Developer ID" dist/SpaceChefSaveManager.app
```

### Windows
Requires a code signing certificate from a CA.
Use `signtool.exe` from Windows SDK.

## Size Optimization

To reduce executable size (~30% smaller):

1. Edit `build.py` and add:
```python
cmd.extend([
    '--exclude-module=matplotlib',
    '--exclude-module=numpy',
    '--exclude-module=PIL',
])
```

2. Use UPX compression:
```bash
pip install upx
# PyInstaller will automatically use it
```

## Testing on Clean Machines

### Windows
- Use a virtual machine with fresh Windows install
- No Python, no dev tools
- Test all features

### Mac
- Test on a Mac without Homebrew/Python
- System Python is OK (but executable shouldn't use it)

### Linux
- Test on Ubuntu/Fedora fresh install
- No Python packages installed

## Common Issues

**Issue:** "DLL not found" on Windows
- Solution: Use `--hidden-import` flag in build.py

**Issue:** Executable is too large (>50 MB)
- Check for accidentally included modules
- Use `--exclude-module` for unused packages

**Issue:** Slow startup time
- Normal for first run (PyInstaller unpacks to temp)
- Consider using one-folder mode instead

## One-File vs One-Folder Mode

**One-File (default):**
- Single executable file
- Easier to distribute
- Slower startup (unpacks to temp)

**One-Folder:**
- Folder with multiple files
- Faster startup
- Harder to distribute

To use one-folder mode, edit `build.py`:
```python
cmd = [
    'pyinstaller',
    '--onedir',  # Changed from --onefile
    ...
]
```
