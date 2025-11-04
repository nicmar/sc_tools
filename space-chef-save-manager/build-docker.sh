#!/bin/bash
# Build Linux version using Docker on Mac/Windows

set -e

echo "========================================================================"
echo "  Building Linux Version with Docker"
echo "========================================================================"
echo

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed!"
    echo
    echo "Install Docker Desktop:"
    echo "  macOS: https://www.docker.com/products/docker-desktop"
    echo "  Windows: https://www.docker.com/products/docker-desktop"
    echo
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "ERROR: Docker is not running!"
    echo
    echo "Please start Docker Desktop and try again."
    echo
    exit 1
fi

echo "Docker is ready!"
echo

# Create Dockerfile if it doesn't exist
if [ ! -f "Dockerfile.build" ]; then
    echo "Creating Dockerfile.build..."
    cat > Dockerfile.build << 'EOF'
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-tk \
    binutils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir pyinstaller

# Build the executable
RUN python build.py

# The dist folder will contain the executable
CMD ["ls", "-lh", "dist/"]
EOF
    echo "✓ Dockerfile.build created"
    echo
fi

# Build Docker image
echo "Building Docker image (this may take a few minutes)..."
docker build -f Dockerfile.build -t space-chef-save-manager-builder .
echo
echo "✓ Docker image built"
echo

# Run the build in Docker
echo "Building Linux executable in Docker container..."
docker run --rm -v "$(pwd)/dist:/app/dist" space-chef-save-manager-builder python build.py
echo
echo "✓ Linux executable built"
echo

# Create package
echo "Creating Linux distribution package..."
docker run --rm -v "$(pwd)/dist:/app/dist" space-chef-save-manager-builder python package.py
echo

echo "========================================================================"
echo "  Linux Build Complete!"
echo "========================================================================"
echo
echo "Output: dist/SpaceChefSaveManager-v1.0.0-Linux.zip"
echo
ls -lh dist/SpaceChefSaveManager-v1.0.0-Linux.zip 2>/dev/null || echo "Package not found - check dist/ folder"
echo
