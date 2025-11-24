#!/bin/bash
# Video Converter Setup Script
# Installs FFmpeg (system dependency) and Python packages

set -e

echo "=========================================="
echo "Video Converter - Setup Script"
echo "=========================================="
echo ""

# Check if running on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS"
    
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew is not installed."
        echo "   Please install Homebrew first: https://brew.sh"
        exit 1
    fi
    
    # Check if FFmpeg is installed
    if command -v ffmpeg &> /dev/null; then
        echo "✓ FFmpeg is already installed"
        ffmpeg -version | head -n 1
    else
        echo "Installing FFmpeg via Homebrew..."
        brew install ffmpeg
        echo "✓ FFmpeg installed successfully"
    fi
    
# Check if running on Linux
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux"
    
    # Check if FFmpeg is installed
    if command -v ffmpeg &> /dev/null; then
        echo "✓ FFmpeg is already installed"
        ffmpeg -version | head -n 1
    else
        echo "Installing FFmpeg via apt-get..."
        echo "   (You may be prompted for your password)"
        sudo apt-get update
        sudo apt-get install -y ffmpeg
        echo "✓ FFmpeg installed successfully"
    fi
    
else
    echo "⚠️  Unsupported OS: $OSTYPE"
    echo "   Please install FFmpeg manually from: https://ffmpeg.org/download.html"
fi

echo ""
echo "Installing Python packages..."
pip3 install -r requirements.txt

echo ""
echo "=========================================="
echo "✓ Setup complete!"
echo "=========================================="
echo ""
echo "You can now run the app:"
echo "  python3 convertVideo.py"
echo ""

