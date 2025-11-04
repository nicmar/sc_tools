#!/usr/bin/env python3
"""
Package script for creating distribution archives
"""
import os
import platform
import shutil
import zipfile
from pathlib import Path
from datetime import datetime


VERSION = "1.0.1"


def create_readme_txt():
    """Create a user-friendly README.txt for distribution"""
    system = platform.system()

    if system == "Windows":
        executable = "SpaceChefSaveManager.exe"
        instructions = """
How to Run:
  1. Double-click SpaceChefSaveManager.exe
  2. No installation required!

Default Save Location:
  C:\\Users\\<YourName>\\AppData\\Roaming\\BlueGooGames\\Space Chef\\Saves

If the save location is not found automatically:
  - Click "Browse..." to locate your Saves folder
  - Make sure Space Chef has been run at least once
"""
    elif system == "Darwin":
        executable = "SpaceChefSaveManager"
        instructions = """
How to Run:
  1. Double-click SpaceChefSaveManager
  2. If macOS blocks it, go to System Preferences > Security & Privacy
     and click "Open Anyway"
  3. No installation required!

Default Save Location:
  ~/Library/Application Support/BlueGooGames/Space Chef/Saves

If the save location is not found automatically:
  - Click "Browse..." to locate your Saves folder
  - Make sure Space Chef has been run at least once

Note: You may need to make the file executable:
  chmod +x SpaceChefSaveManager
"""
    else:  # Linux
        executable = "SpaceChefSaveManager"
        instructions = """
How to Run:
  1. Open terminal in this folder
  2. Make executable: chmod +x SpaceChefSaveManager
  3. Run: ./SpaceChefSaveManager
  4. Or: Double-click the file in your file manager

Default Save Location:
  ~/.local/share/BlueGooGames/Space Chef/Saves

If the save location is not found automatically:
  - Click "Browse..." to locate your Saves folder
  - Make sure Space Chef has been run at least once
"""

    readme = f"""
================================================================================
        Space Chef Save Manager v{VERSION}
================================================================================

A cross-platform tool for managing Space Chef save files and backups.

{instructions}

Features:
  - View all your Space Chef saves with player names and progress
  - Create manual backups of your saves
  - Restore from any backup (with automatic safety backup)
  - Quick access to save and log folders

Usage:
  1. Launch {executable}
  2. Select a player from the list
  3. Use "View Backups" to see and restore backups
  4. Use "Create Backup" to make a manual backup
  5. Use "Open Save Folder" or "Open Player Logs" for quick access

Troubleshooting:
  - Save location not found?
    Use the "Browse..." button to manually select your Saves folder

  - No saves showing?
    Make sure you've run Space Chef at least once

  - Backup restore failed?
    Close Space Chef before restoring
    Make sure you have write permissions to the Saves folder

Support:
  This is an unofficial community tool for Space Chef players.
  Not affiliated with BlueGoo Games.

================================================================================
                    Made with love for Space Chef players
================================================================================
"""
    return readme.strip()


def create_package():
    """Create distribution package"""
    system = platform.system()

    print("="*70)
    print(f"Creating Distribution Package for {system}")
    print("="*70)
    print()

    # Determine executable name
    if system == "Windows":
        executable_name = "SpaceChefSaveManager.exe"
        platform_name = "Windows"
    elif system == "Darwin":
        executable_name = "SpaceChefSaveManager"
        platform_name = "macOS"
    else:
        executable_name = "SpaceChefSaveManager"
        platform_name = "Linux"

    # Check if executable exists
    executable_path = Path("dist") / executable_name
    if not executable_path.exists():
        print(f"ERROR: Executable not found at {executable_path}")
        print()
        print("Please run build.py first:")
        print("  python build.py")
        print()
        return False

    # Create package directory
    timestamp = datetime.now().strftime("%Y%m%d")
    package_name = f"SpaceChefSaveManager-v{VERSION}-{platform_name}"
    package_dir = Path("dist") / package_name

    # Remove old package if exists
    if package_dir.exists():
        shutil.rmtree(package_dir)

    package_dir.mkdir(parents=True)

    print(f"Package directory: {package_dir}")
    print()

    # Copy executable
    print("Copying executable...")
    shutil.copy2(executable_path, package_dir / executable_name)

    # Make executable on Unix
    if system in ["Darwin", "Linux"]:
        os.chmod(package_dir / executable_name, 0o755)

    # Create README.txt
    print("Creating README.txt...")
    readme_path = package_dir / "README.txt"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(create_readme_txt())

    # Create zip archive
    print("Creating zip archive...")
    zip_name = f"{package_name}.zip"
    zip_path = Path("dist") / zip_name

    if zip_path.exists():
        zip_path.unlink()

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in package_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(package_dir.parent)
                zipf.write(file_path, arcname)

    # Get file size
    zip_size_mb = zip_path.stat().st_size / (1024 * 1024)

    print()
    print("="*70)
    print("PACKAGE CREATED SUCCESSFULLY!")
    print("="*70)
    print()
    print(f"Distribution package: {zip_path}")
    print(f"Package size: {zip_size_mb:.1f} MB")
    print()
    print("Contents:")
    print(f"  - {executable_name}")
    print(f"  - README.txt")
    print()
    print("Ready to distribute!")
    print()

    return True


if __name__ == "__main__":
    success = create_package()
    exit(0 if success else 1)
