# Build Instructions

This guide explains how to build standalone executables for Windows, macOS, and Linux.

## Prerequisites

All platforms need:
- Python 3.7 or higher
- pip (Python package manager)

### Platform-Specific Requirements

#### macOS
```bash
# Install Homebrew Python with Tkinter support
brew install python-tk@3.13
```

#### Windows
- Python from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation

#### Linux
```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip python3-tk

# Fedora
sudo dnf install python3 python3-pip python3-tkinter

# Arch
sudo pacman -S python python-pip tk
```

## Quick Build (Recommended)

### macOS / Linux
```bash
./build.sh
```

### Windows
```batch
build.bat
```

These scripts will:
1. Install PyInstaller if needed
2. Clean previous builds
3. Build the executable
4. Create a distribution package (ZIP file)

## Manual Build (Step by Step)

### 1. Install Dependencies

```bash
pip install pyinstaller
```

### 2. Build Executable

**macOS (using Homebrew Python):**
```bash
/opt/homebrew/bin/python3.13 build.py
```

**Windows / Linux:**
```bash
python build.py
```

### 3. Create Distribution Package

```bash
python package.py
```

## Output

After building, you'll find:

```
dist/
├── SpaceChefSaveManager              # Executable (macOS/Linux)
│   or SpaceChefSaveManager.exe       # Executable (Windows)
│
└── SpaceChefSaveManager-v1.0.0-<Platform>.zip
    └── SpaceChefSaveManager-v1.0.0-<Platform>/
        ├── SpaceChefSaveManager(.exe)
        └── README.txt
```

The `.zip` file is ready for distribution!

## Building for Multiple Platforms

**Important:** PyInstaller cannot cross-compile. You must build on each target platform:

1. **For Windows**: Build on a Windows machine (or VM)
2. **For macOS**: Build on a Mac
3. **For Linux**: Build on Linux (or VM)

### Recommended Workflow

If you only have one platform, use virtual machines or cloud services:

- **Windows VM**: VirtualBox, Parallels, or VMware
- **macOS**: Requires real Mac hardware (or Hackintosh)
- **Linux VM**: VirtualBox, VMware, or cloud (AWS, DigitalOcean)

## Testing the Build

Before distributing, test the executable:

### macOS
```bash
cd dist
./SpaceChefSaveManager
```

If macOS blocks it:
1. Right-click → Open
2. Click "Open" in the security dialog

### Windows
1. Navigate to `dist` folder
2. Double-click `SpaceChefSaveManager.exe`

If Windows Defender blocks it:
1. Click "More info"
2. Click "Run anyway"

### Linux
```bash
cd dist
chmod +x SpaceChefSaveManager
./SpaceChefSaveManager
```

## Cleaning Build Artifacts

Remove build files:

```bash
python build.py clean
```

Or manually delete:
- `build/` folder
- `dist/` folder
- `SpaceChefSaveManager.spec` file

## Troubleshooting

### "PyInstaller not found"
```bash
pip install pyinstaller
```

### "No module named tkinter" (macOS)
```bash
brew install python-tk@3.13
```

### "No module named tkinter" (Linux)
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

### Build succeeds but executable doesn't run

**Check Python version:**
```bash
python --version
```

Make sure it's 3.7 or higher.

**Try running with console output:**

macOS/Linux:
```bash
./SpaceChefSaveManager 2>&1 | tee error.log
```

Windows:
```batch
SpaceChefSaveManager.exe > error.log 2>&1
```

### Executable is too large (>50 MB)

This is normal. PyInstaller bundles:
- Python runtime (~8-10 MB)
- Tkinter libraries (~2-3 MB)
- Your code (~1 MB)

Typical size: 10-15 MB

## Distribution Checklist

Before releasing:

- [ ] Test on clean machine (without Python installed)
- [ ] Test all features work
- [ ] Verify save location detection
- [ ] Test backup creation
- [ ] Test backup restoration
- [ ] Test "Open Folder" buttons
- [ ] Check file size is reasonable (<20 MB)
- [ ] Scan with antivirus (to avoid false positives)
- [ ] Create GitHub release with all platform builds

## Version Management

To change version number, edit:
- `config.py` → `VERSION = "1.0.0"`
- `build.py` → `VERSION = "1.0.0"`
- `package.py` → `VERSION = "1.0.0"`

## Advanced: Code Signing (Optional)

### macOS
```bash
codesign --force --deep --sign "Developer ID Application: Your Name" dist/SpaceChefSaveManager
```

Requires Apple Developer account ($99/year).

### Windows
Requires code signing certificate from a Certificate Authority.
Use `signtool.exe` from Windows SDK.

Code signing prevents security warnings but is not required for distribution.

## Need Help?

Common build commands:

```bash
# Clean and rebuild everything
python build.py clean && python build.py && python package.py

# Just rebuild (no clean)
python build.py && python package.py

# Test without building
python main.py
```

---

**Happy Building!** 🚀
