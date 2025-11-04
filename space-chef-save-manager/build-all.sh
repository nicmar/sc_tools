#!/bin/bash
# Multi-platform build orchestrator
# This script helps coordinate building for all platforms

set -e

echo "========================================================================"
echo "  Space Chef Save Manager - Multi-Platform Build"
echo "========================================================================"
echo
echo "IMPORTANT: PyInstaller cannot cross-compile!"
echo "You must build on each target platform separately."
echo
echo "This script provides options for building on multiple platforms."
echo
echo "========================================================================"
echo

# Detect current platform
CURRENT_PLATFORM=$(uname -s)

echo "Current platform: $CURRENT_PLATFORM"
echo

# Build for current platform
echo "1. Building for current platform ($CURRENT_PLATFORM)..."
echo "========================================================================"
./build.sh
echo
echo "✓ $CURRENT_PLATFORM build complete!"
echo

# Check for Docker (for Linux builds)
if command -v docker &> /dev/null; then
    echo "2. Docker detected! Can build Linux version using Docker?"
    echo "========================================================================"
    read -p "Build Linux version with Docker? (y/n): " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Building Linux version with Docker..."
        ./build-docker.sh
        echo "✓ Linux build complete!"
        echo
    fi
else
    echo "2. Docker not installed - Linux build skipped"
    echo "   Install Docker to build Linux version on Mac"
    echo
fi

# Windows build instructions
echo "3. Windows Build"
echo "========================================================================"
echo
echo "To build for Windows, you need a Windows machine or VM."
echo
echo "Options:"
echo "  A) Windows PC/Laptop:"
echo "     1. Copy project folder to Windows machine"
echo "     2. Run: build.bat"
echo
echo "  B) Windows VM (Parallels/VMware/VirtualBox):"
echo "     1. Share project folder with VM"
echo "     2. Run: build.bat in the VM"
echo
echo "  C) Cloud Windows machine (AWS/Azure):"
echo "     1. Upload project to cloud Windows instance"
echo "     2. Run: build.bat"
echo
echo "  D) Wine on Mac (experimental, not recommended):"
echo "     Wine can run Windows Python, but builds are often unreliable"
echo
echo "========================================================================"
echo

# Summary
echo "Build Summary"
echo "========================================================================"
echo
ls -lh dist/*.zip 2>/dev/null || echo "No distribution packages found"
echo
echo "Next steps:"
echo "  - Test the executable(s) on their respective platforms"
echo "  - Build on remaining platforms as needed"
echo "  - Upload all ZIPs to GitHub releases"
echo
