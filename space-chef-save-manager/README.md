# Space Chef Save Manager

A cross-platform GUI tool for managing Space Chef save files and backups.

## Features

- 🎮 **View all save files** - See all your Space Chef saves with player names and progress
- 💾 **Backup management** - View, restore, and create backups of your save files
- 🔄 **Safe restore** - Automatically creates a safety backup before restoring
- 📁 **Quick access** - Open save and log folders with one click
- 🖥️ **Cross-platform** - Works on Windows, macOS, and Linux

## For Users

### Installation

#### Option 1: Download Executable (Recommended)
1. Download the appropriate executable for your system:
   - **Windows**: `SpaceChefSaveManager.exe`
   - **macOS**: `SpaceChefSaveManager.app` or `SpaceChefSaveManager`
   - **Linux**: `SpaceChefSaveManager`

2. Run the executable - no installation required!

#### Option 2: Run from Source
If you have Python 3.7+ installed:

**macOS/Linux:**
```bash
./run.sh
```
Or:
```bash
python main.py
```

**Windows:**
```batch
run.bat
```
Or:
```batch
python main.py
```

**Note for macOS users:** If you get a tkinter error, use the system Python:
```bash
/usr/bin/python3 main.py
```

### Usage

1. **Launch the application**
   - The tool will auto-detect your Space Chef save location
   - If not found, use the "Browse..." button to locate your Saves folder

2. **Select a player**
   - All your save files will be listed with player names and progress
   - Click on a save to select it

3. **View Backups**
   - Click "View Backups" to see all available backups for the selected player
   - Backups are sorted by date (newest first)

4. **Restore a Backup**
   - Select a backup from the list
   - Click "Restore Selected"
   - Confirm the action
   - Your current save will be automatically backed up before restoring

5. **Create Manual Backup**
   - Select a player
   - Click "Create Backup"
   - A timestamped backup will be created in the Backup folder

6. **Quick Actions**
   - **Open Save Folder**: Opens your Saves folder in file explorer
   - **Open Player Logs**: Opens the Space Chef logs folder

### Default Save Locations

- **Windows**: `%USERPROFILE%\AppData\LocalLow\BlueGooGames\Space Chef\Saves`
  - Usually: `C:\Users\<YourName>\AppData\LocalLow\BlueGooGames\Space Chef\Saves`
  - Alternative: `C:\Users\<YourName>\AppData\Roaming\BlueGooGames\Space Chef\Saves`
  - The tool automatically detects which location has your saves

- **macOS**: `~/Library/Application Support/BlueGooGames/Space Chef/Saves`

- **Linux**: `~/.local/share/BlueGooGames/Space Chef/Saves`

### Troubleshooting

**Save location not found?**
- Use the "Browse..." button to manually select your Saves folder
- Make sure Space Chef has been run at least once
- Check if the game is installed in a custom location

**Backup restore failed?**
- Make sure the backup file is not corrupted
- Check that you have write permissions to the Saves folder
- Try closing Space Chef if it's running

**Player name shows as "Player X"?**
- The save file might be corrupted or in an older format
- Try opening the save in Space Chef first

## For Developers

### Requirements

- Python 3.7 or higher
- tkinter (usually included with Python)
- PyInstaller (for building executables)

### Setup Development Environment

1. Clone or download the source code:
```bash
cd space-chef-save-manager
```

2. Install build dependencies:
```bash
pip install -r requirements.txt
```

### Running from Source

```bash
python main.py
```

### Project Structure

```
space-chef-save-manager/
├── main.py              # Application entry point
├── gui.py               # Tkinter GUI implementation
├── save_manager.py      # Core save file operations
├── models.py            # Data models (SaveFile, Backup)
├── config.py            # Platform-specific configuration
├── build.py             # Build script for PyInstaller
├── run.sh               # Launch script for macOS/Linux
├── run.bat              # Launch script for Windows
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

### Building Executables

**Quick Build:**

```bash
# macOS / Linux
./build.sh

# Windows
build.bat
```

This will create a complete distribution package (ZIP file) ready for distribution.

**Manual Build:**

```bash
# 1. Install dependencies
pip install pyinstaller

# 2. Build executable
python build.py

# 3. Create distribution package
python package.py
```

**Output:** `dist/SpaceChefSaveManager-v1.0.0-<Platform>.zip`

For detailed instructions, see [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)

### Building for All Platforms

PyInstaller cannot cross-compile. You must build on each platform:
- **Windows**: Build on Windows (or Windows VM)
- **macOS**: Build on Mac
- **Linux**: Build on Linux (or Linux VM)

### How It Works

1. **Save Detection**: Scans the Saves folder for files matching pattern `save####.*`
2. **Player Name Extraction**: Reads `uniquePlayersData.playerName` from save JSON files
3. **Backup Management**: Lists and manages .zip files in `Saves/Backup/` folder
4. **Safe Restore**: Creates `saveXXXX_current_TIMESTAMP.zip` before any restore operation

## Technical Details

- **Language**: Python 3.7+
- **GUI Framework**: Tkinter (cross-platform, no external dependencies)
- **Build Tool**: PyInstaller
- **Save Format**: JSON + ZIP archives

## License

This tool is provided as-is for Space Chef players. Not officially affiliated with BlueGoo Games.

## Support

For issues, questions, or feature requests, please contact the developer or check the project repository.

---

Made with ❤️ for Space Chef players
