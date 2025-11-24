#!/bin/bash
# Fix moviepy installation - uninstall 2.x and install 1.x

echo "Fixing moviepy installation..."
echo ""

# Uninstall moviepy 2.x
pip3 uninstall -y moviepy

# Install moviepy 1.x (stable version)
pip3 install "moviepy>=1.0.3,<2.0.0"

echo ""
echo "✓ moviepy 1.x installed"
echo ""
echo "Now try running: python3 convertVideo.py"

