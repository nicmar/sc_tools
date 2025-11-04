#!/usr/bin/env python3
"""
Build script for creating standalone executables using PyInstaller
Supports Windows, macOS, and Linux
"""
import os
import platform
import subprocess
import sys
import shutil
from pathlib import Path
from datetime import datetime


VERSION = "1.0.1"


def get_python_executable():
    """Get the correct Python executable for the current platform"""
    system = platform.system()

    if system == "Darwin":  # macOS
        # Prefer Homebrew Python with Tkinter support
        homebrew_python = "/opt/homebrew/bin/python3.13"
        if os.path.exists(homebrew_python):
            return homebrew_python

    return sys.executable


def build_executable():
    """Build standalone executable for current platform"""
    system = platform.system()

    print("="*70)
    print(f"Building Space Chef Save Manager v{VERSION} for {system}")
    print("="*70)
    print()

    # Base PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',                    # Single file executable
        '--windowed',                   # No console window (GUI app)
        '--name=SpaceChefSaveManager',  # Output name
        '--clean',                      # Clean cache
        'main.py'
    ]

    # Platform-specific options
    if system == "Darwin":  # macOS
        cmd.extend([
            '--osx-bundle-identifier=com.bluegoogames.spacechefsavemanager',
        ])
        output_name = "SpaceChefSaveManager"
        print("Building macOS executable...")

    elif system == "Windows":
        # Add Windows-specific options
        output_name = "SpaceChefSaveManager.exe"
        print("Building Windows executable...")

    elif system == "Linux":
        output_name = "SpaceChefSaveManager"
        print("Building Linux executable...")

    else:
        output_name = "SpaceChefSaveManager"
        print(f"Warning: Unknown platform {system}, building anyway...")

    print()
    print("PyInstaller command:")
    print(" ".join(cmd))
    print()

    # Run PyInstaller
    try:
        subprocess.run(cmd, check=True)

        print()
        print("="*70)
        print("BUILD SUCCESSFUL!")
        print("="*70)
        print()

        # Show output location
        dist_path = Path("dist") / output_name
        print(f"Executable location: {dist_path}")

        if dist_path.exists():
            size_mb = dist_path.stat().st_size / (1024 * 1024)
            print(f"File size: {size_mb:.1f} MB")

        print()
        print("Next steps:")
        print("1. Test the executable by running it")
        print("2. Run './package.sh' (or 'python package.py') to create distribution package")
        print()

    except subprocess.CalledProcessError as e:
        print()
        print("="*70)
        print("BUILD FAILED!")
        print("="*70)
        print(f"\nError: {e}", file=sys.stderr)
        print()
        print("Common issues:")
        print("- PyInstaller not installed: pip install pyinstaller")
        print("- Missing dependencies: pip install -r requirements.txt")
        sys.exit(1)


def clean():
    """Clean build artifacts"""
    dirs_to_remove = ['build', 'dist', '__pycache__']
    files_to_remove = ['SpaceChefSaveManager.spec']

    print("Cleaning build artifacts...")
    print()

    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  ✓ Removed {dir_name}/")

    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"  ✓ Removed {file_name}")

    print()
    print("Clean complete!")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        clean()
    else:
        build_executable()
