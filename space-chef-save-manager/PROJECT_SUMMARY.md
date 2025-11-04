# Space Chef Save Manager - Project Summary

## Overview

A cross-platform GUI tool for managing Space Chef save files and backups. Built with Python and Tkinter.

**Version:** 1.0.0
**Platforms:** Windows, macOS, Linux
**License:** MIT (or your choice)

## Features

✅ View all save files with player names and progress
✅ Create manual backups
✅ Restore from any backup (with automatic safety backup)
✅ Quick access to save and log folders
✅ Cross-platform GUI
✅ Standalone executables (no Python required for end users)

## Project Structure

```
space-chef-save-manager/
├── main.py                   # Application entry point
├── gui.py                    # Tkinter GUI (pack-based layout)
├── save_manager.py           # Core save file operations
├── models.py                 # Data classes (SaveFile, Backup)
├── config.py                 # Platform-specific paths
├── build.py                  # PyInstaller build script
├── package.py                # Distribution packaging script
├── build.sh                  # Build script for macOS/Linux
├── build.bat                 # Build script for Windows
├── run.sh                    # Launch script for macOS/Linux
├── run.bat                   # Launch script for Windows
├── requirements.txt          # Python dependencies
├── .gitignore                # Git ignore patterns
├── README.md                 # Main documentation
├── BUILD_INSTRUCTIONS.md     # Detailed build guide
├── DISTRIBUTION.md           # Distribution guide
└── PROJECT_SUMMARY.md        # This file
```

## Quick Start

### For Users

**Download & Run:**
1. Download the appropriate ZIP file for your OS
2. Extract the ZIP
3. Run the executable (no installation needed)

### For Developers

**Run from source:**
```bash
# macOS/Linux
./run.sh

# Windows
run.bat
```

**Build executable:**
```bash
# macOS/Linux
./build.sh

# Windows
build.bat
```

## Technical Details

### Architecture

- **Language:** Python 3.7+
- **GUI Framework:** Tkinter (built-in)
- **Build Tool:** PyInstaller
- **Save Format:** JSON + ZIP archives

### Key Components

1. **SaveManager** (`save_manager.py`)
   - Scans save files
   - Extracts player names from JSON (`uniquePlayersData[0].playerName`)
   - Extracts day numbers from JSON (`lastSnapShotDay`)
   - Creates and restores backups
   - Handles ZIP file operations

2. **GUI** (`gui.py`)
   - Main window with save list
   - Backup viewer window
   - Pack-based layout (more reliable than grid on macOS)
   - Cross-platform folder opening

3. **Config** (`config.py`)
   - Platform detection
   - Default save paths for Windows/Mac/Linux
   - Log folder paths

4. **Models** (`models.py`)
   - SaveFile dataclass
   - Backup dataclass
   - Display formatting methods

### Platform-Specific Details

#### Windows
- Save location: `%AppData%\BlueGooGames\Space Chef\Saves`
- Logs: `%USERPROFILE%\AppData\LocalLow\BlueGooGames\Space Chef`
- Executable: `SpaceChefSaveManager.exe`
- Typical size: ~12 MB

#### macOS
- Save location: `~/Library/Application Support/BlueGooGames/Space Chef/Saves`
- Requires Homebrew Python with Tkinter: `brew install python-tk@3.13`
- System Python has Tkinter rendering bugs
- Executable: `SpaceChefSaveManager`
- Typical size: ~14 MB

#### Linux
- Save location: `~/.local/share/BlueGooGames/Space Chef/Saves` (XDG standard)
- Requires python3-tk package
- Executable: `SpaceChefSaveManager`
- Typical size: ~13 MB

## Development

### Prerequisites

- Python 3.7+
- Tkinter (usually bundled, or install separately)
- PyInstaller (for building)

### Setup

```bash
# Clone/download repository
cd space-chef-save-manager

# Run from source (for development)
python main.py  # or ./run.sh on Mac/Linux

# Install build tools
pip install pyinstaller

# Build executable
python build.py

# Create distribution package
python package.py
```

### Testing

```bash
# Test save scanning
python -c "from save_manager import SaveManager; from pathlib import Path; m = SaveManager(Path.home() / 'Library/Application Support/BlueGooGames/Space Chef/Saves'); print(m.scan_saves())"

# Test GUI
python main.py

# Test built executable
cd dist
./SpaceChefSaveManager  # Mac/Linux
SpaceChefSaveManager.exe  # Windows
```

## Build Process

### How It Works

1. **build.py** runs PyInstaller with platform-specific options
2. PyInstaller analyzes dependencies and bundles:
   - Python interpreter
   - Tkinter libraries
   - All Python modules
   - Your code
3. Creates single executable in `dist/` folder
4. **package.py** creates distribution ZIP with README

### Virtual Environment

The build script uses a virtual environment to avoid conflicts with system Python packages:

```bash
venv/                    # Virtual environment (auto-created)
├── bin/python          # Isolated Python
└── lib/python*/        # Isolated packages
```

This is ignored by Git (`.gitignore`).

## Distribution

### Files Included in ZIP

```
SpaceChefSaveManager-v1.0.0-<Platform>/
├── SpaceChefSaveManager(.exe)    # Executable
└── README.txt                     # User instructions
```

### Distribution Checklist

- [ ] Build on all three platforms (Windows, Mac, Linux)
- [ ] Test each executable on clean machine
- [ ] Verify all features work
- [ ] Check file sizes are reasonable
- [ ] Create GitHub release with all ZIPs
- [ ] Update version numbers in code
- [ ] Create release notes

## Troubleshooting

### Common Issues

**"Blank window on macOS"**
- System Python's Tkinter has rendering bugs
- Solution: Use Homebrew Python with `brew install python-tk@3.13`
- Or: Build executable which bundles working Tkinter

**"No module named '_tkinter'"**
- Tkinter not installed
- macOS: `brew install python-tk@3.13`
- Linux: `sudo apt install python3-tk`

**"PyInstaller externally-managed-environment"**
- Python 3.13+ from Homebrew requires virtual env
- Solution: Use `build.sh` which handles this automatically

**"Windows Defender blocks executable"**
- Common false positive for PyInstaller apps
- Solution: Click "More info" → "Run anyway"
- Or: Submit to Microsoft for whitelisting

## Future Enhancements

Possible improvements:

- [ ] Add icon file for better branding
- [ ] Implement backup scheduling
- [ ] Add save file comparison/diff
- [ ] Support for cloud backup (Google Drive, Dropbox)
- [ ] Auto-update functionality
- [ ] Backup compression optimization
- [ ] Backup encryption
- [ ] Multiple save locations
- [ ] Backup notes/tags
- [ ] Search/filter saves

## Contributing

To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on your platform
5. Submit pull request

## Support

For issues or questions:
- Check README.md
- Check BUILD_INSTRUCTIONS.md
- Open GitHub issue
- Contact developer

## License

[Add your license here - MIT recommended for open source]

---

**Made with ❤️ for Space Chef players**

Last updated: 2025-11-04
