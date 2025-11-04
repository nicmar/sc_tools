# Multi-Platform Build Guide

This guide explains how to build Space Chef Save Manager for Windows, macOS, and Linux.

## Important: Cross-Compilation Not Possible

**PyInstaller cannot cross-compile.** You must build on each target platform:
- Windows build → Requires Windows machine
- macOS build → Requires Mac machine
- Linux build → Requires Linux machine (or Docker)

## Option 1: Automated Build (Docker + Mac)

If you have Docker installed on your Mac, you can build both macOS and Linux versions:

```bash
# Build all available platforms
./build-all.sh
```

This will:
1. ✅ Build macOS version (native)
2. ✅ Build Linux version (using Docker)
3. ℹ️ Show instructions for Windows build

### Prerequisites for Docker Build

```bash
# Install Docker Desktop for Mac
brew install --cask docker
# Or download from: https://www.docker.com/products/docker-desktop

# Start Docker Desktop
open -a Docker

# Verify Docker is running
docker --version
```

## Option 2: Manual Build on Each Platform

### macOS (Current Platform)

```bash
./build.sh
```

Output: `dist/SpaceChefSaveManager-v1.0.0-macOS.zip`

### Linux (Using Docker on Mac)

```bash
./build-docker.sh
```

Output: `dist/SpaceChefSaveManager-v1.0.0-Linux.zip`

### Windows (Need Windows Machine)

You have several options:

#### A) Native Windows Machine

1. Copy entire project folder to Windows PC
2. Open Command Prompt or PowerShell
3. Run:
   ```batch
   cd space-chef-save-manager
   build.bat
   ```
4. Copy `dist\SpaceChefSaveManager-v1.0.0-Windows.zip` back to Mac

#### B) Windows VM on Mac

**Parallels Desktop (Recommended):**
```bash
# 1. Install Parallels Desktop
brew install --cask parallels

# 2. Install Windows 11 (free for development)
# Download Windows 11 ARM from Microsoft Insider

# 3. Share project folder
# Parallels automatically shares Mac folders with Windows

# 4. In Windows VM:
cd \\Mac\Home\Documents\github\sc_tools\space-chef-save-manager
build.bat

# 5. Copy dist\*.zip back to Mac
```

**VirtualBox (Free):**
```bash
# 1. Install VirtualBox
brew install --cask virtualbox

# 2. Create Windows VM
# Download Windows 10/11 ISO from Microsoft

# 3. Install Guest Additions for folder sharing

# 4. Share project folder with VM

# 5. In Windows VM:
Z:\build.bat  # If shared as Z: drive
```

**VMware Fusion:**
```bash
# Similar to Parallels
# Download VMware Fusion from vmware.com
```

#### C) Cloud Windows Instance

**AWS EC2 Windows:**
```bash
# 1. Create Windows Server instance
# 2. Upload project via RDP or S3
# 3. Install Python on Windows
# 4. Run build.bat
# 5. Download the ZIP
```

**Azure VM:**
```bash
# Similar to AWS
# Use Azure Windows VM
```

#### D) Wine (Not Recommended - Experimental)

You can try running Windows Python with Wine, but this is **not reliable** for PyInstaller:

```bash
# Install Wine
brew install --cask wine-stable

# Install Windows Python in Wine
# Run build.bat through Wine

# WARNING: Often produces broken executables
# Only use for quick testing, not production builds
```

## Option 3: GitHub Actions (Automated Cloud Build)

The best solution for automated multi-platform builds is GitHub Actions. It's **free for public repositories**.

### Setup GitHub Actions

1. Create `.github/workflows/build.yml` in your repository
2. Push to GitHub
3. Actions will automatically build all three platforms
4. Download all ZIPs from the Actions artifacts

See `github-actions-workflow.yml` in this project for the complete workflow.

## Option 4: Outsource Builds

If you don't have access to all platforms:

1. **macOS**: Build yourself (you have a Mac)
2. **Linux**: Use Docker (free, runs on Mac)
3. **Windows**: Ask a friend/colleague, or hire on Fiverr

## Comparison of Options

| Option | macOS | Linux | Windows | Cost | Ease |
|--------|-------|-------|---------|------|------|
| Native | ✅ | ❌ | ❌ | Free | Easy |
| Docker | ✅ | ✅ | ❌ | Free | Medium |
| VM (Parallels) | ✅ | ✅ | ✅ | $100/yr | Medium |
| VM (VirtualBox) | ✅ | ✅ | ✅ | Free | Hard |
| Cloud (AWS) | ✅ | ✅ | ✅ | ~$1/build | Medium |
| GitHub Actions | ✅ | ✅ | ✅ | Free* | Easy |

*Free for public repos, limited minutes for private repos

## Recommended Workflow

**For Open Source / Public Release:**
```bash
# 1. Build macOS locally
./build.sh

# 2. Build Linux with Docker
./build-docker.sh

# 3. Use GitHub Actions for Windows
# Push to GitHub, download Windows build from Actions
```

**For Personal Use:**
```bash
# Just build for your platform
./build.sh  # macOS
```

**For Commercial Distribution:**
```bash
# Use GitHub Actions or VMs
# Build all three platforms
# Test each thoroughly before release
```

## Testing Built Executables

After building, test each executable:

### macOS
```bash
cd dist
./SpaceChefSaveManager
```

### Linux (in Docker)
```bash
docker run --rm -v "$(pwd)/dist:/dist" ubuntu:22.04 /dist/SpaceChefSaveManager
```

### Windows (in VM or native)
```batch
cd dist
SpaceChefSaveManager.exe
```

## Troubleshooting

### Docker build fails
```bash
# Check Docker is running
docker info

# Rebuild from scratch
docker system prune -a
./build-docker.sh
```

### Windows build on VM is slow
- Allocate more RAM to VM (8GB recommended)
- Use SSD for VM storage
- Consider Parallels (faster than VirtualBox)

### Can't afford Parallels?
Use VirtualBox (free) or GitHub Actions (free for public repos)

## File Transfer Between Platforms

### Mac → Windows VM
- Parallels: Automatic folder sharing
- VirtualBox: Shared folders or USB
- Cloud: S3, Dropbox, Google Drive

### Windows VM → Mac
- Copy from shared folder
- Upload to cloud storage
- Use VM's file sharing

## Quick Commands Reference

```bash
# Build current platform only
./build.sh

# Build with Docker (Linux)
./build-docker.sh

# Build all available platforms
./build-all.sh

# Check what's built
ls -lh dist/*.zip

# Clean everything
python build.py clean
rm -rf dist/ venv/
```

## GitHub Actions Setup (Recommended)

Create `.github/workflows/build.yml`:

```yaml
name: Build All Platforms

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:

jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies (Ubuntu)
        if: matrix.os == 'ubuntu-latest'
        run: |
          sudo apt-get update
          sudo apt-get install -y python3-tk

      - name: Build
        run: |
          pip install pyinstaller
          python build.py
          python package.py

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: builds
          path: dist/*.zip
```

Then download all builds from the Actions tab on GitHub!

---

**Need help?** Open an issue on GitHub or consult the README.md file.
