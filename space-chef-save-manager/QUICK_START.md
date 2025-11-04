# Quick Start Guide

## For End Users

### Windows
1. Download `SpaceChefSaveManager-v1.0.0-Windows.zip`
2. Extract the ZIP file
3. Double-click `SpaceChefSaveManager.exe`
4. Done!

### macOS
1. Download `SpaceChefSaveManager-v1.0.0-macOS.zip`
2. Extract the ZIP file
3. Double-click `SpaceChefSaveManager`
4. If blocked: Right-click → Open → Click "Open"
5. Done!

### Linux
1. Download `SpaceChefSaveManager-v1.0.0-Linux.zip`
2. Extract the ZIP file
3. Open terminal in the folder
4. Run: `chmod +x SpaceChefSaveManager && ./SpaceChefSaveManager`
5. Done!

---

## For Developers

### First Time Setup

**macOS:**
```bash
# Install Homebrew Python with Tkinter
brew install python-tk@3.13

# Clone/download repository
cd space-chef-save-manager
```

**Windows:**
```batch
# Download and install Python from python.org
# Make sure to check "Add Python to PATH"

# Clone/download repository
cd space-chef-save-manager
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install python3 python3-pip python3-tk

# Clone/download repository
cd space-chef-save-manager
```

### Running from Source

```bash
# macOS/Linux
./run.sh

# Windows
run.bat
```

### Building Executable

```bash
# macOS/Linux
./build.sh

# Windows
build.bat
```

Output: `dist/SpaceChefSaveManager-v1.0.0-<Platform>.zip`

### Building for All Platforms

You must build on each platform:

1. **On Windows machine/VM:**
   ```batch
   build.bat
   ```

2. **On Mac:**
   ```bash
   ./build.sh
   ```

3. **On Linux machine/VM:**
   ```bash
   ./build.sh
   ```

### Cleaning Build Files

```bash
python build.py clean
```

---

## Common Commands

### Development
```bash
python main.py                 # Run application
python -m pytest              # Run tests (if added)
python build.py clean         # Clean build files
```

### Building
```bash
./build.sh                    # Full build + package (Mac/Linux)
build.bat                     # Full build + package (Windows)

python build.py               # Build executable only
python package.py             # Package into ZIP only
```

### Testing
```bash
cd dist
./SpaceChefSaveManager        # Test built executable
```

---

## File Locations

### Source Files
- `main.py` - Entry point
- `gui.py` - User interface
- `save_manager.py` - Core logic
- `config.py` - Platform paths

### Build Files
- `build.py` - Build script
- `package.py` - Packaging script
- `build.sh` / `build.bat` - Platform build scripts

### Output
- `dist/SpaceChefSaveManager` - Executable
- `dist/SpaceChefSaveManager-v1.0.0-*.zip` - Distribution package

---

## Troubleshooting

### "Python not found"
- **macOS:** `brew install python-tk@3.13`
- **Windows:** Install from python.org
- **Linux:** `sudo apt install python3`

### "No module named tkinter"
- **macOS:** `brew install python-tk@3.13`
- **Linux:** `sudo apt install python3-tk`
- **Windows:** Reinstall Python with "tcl/tk" option checked

### "PyInstaller not found"
The build scripts install it automatically, or:
```bash
pip install pyinstaller
```

### "Blank window on macOS"
Use Homebrew Python, not system Python:
```bash
brew install python-tk@3.13
./run.sh  # Uses correct Python
```

### Build fails
```bash
python build.py clean  # Clean first
./build.sh             # Try again
```

---

## Need More Help?

- **User Guide:** README.md
- **Build Guide:** BUILD_INSTRUCTIONS.md
- **Distribution:** DISTRIBUTION.md
- **Project Info:** PROJECT_SUMMARY.md

---

**Happy coding!** 🚀
