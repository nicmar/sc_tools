#!/bin/bash
# Build script for macOS and Linux

set -e  # Exit on error

echo "========================================================================"
echo "  Space Chef Save Manager - Build Script"
echo "========================================================================"
echo

# Detect platform
PLATFORM=$(uname -s)

# Find Python
if [[ "$PLATFORM" == "Darwin" ]]; then
    # macOS - prefer Homebrew Python with Tkinter
    if [ -f "/opt/homebrew/bin/python3.13" ]; then
        PYTHON="/opt/homebrew/bin/python3.13"
    elif [ -f "/opt/homebrew/bin/python3" ]; then
        PYTHON="/opt/homebrew/bin/python3"
    else
        PYTHON="python3"
    fi
else
    # Linux
    PYTHON="python3"
fi

echo "Using Python: $PYTHON"
$PYTHON --version
echo

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON -m venv venv
    echo
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo

# Install/upgrade pip and PyInstaller
echo "Installing build dependencies..."
pip install --upgrade pip setuptools wheel
pip install pyinstaller
echo

# Clean previous build
echo "Cleaning previous build..."
python build.py clean
echo

# Build executable
echo "Building executable..."
python build.py
echo

# Create package
echo "Creating distribution package..."
python package.py
echo

# Deactivate virtual environment
deactivate

echo "========================================================================"
echo "  Build Complete!"
echo "========================================================================"
echo
echo "Check the dist/ folder for the packaged zip file."
echo
