#!/bin/bash
# Setup script to fix OpenCV dependency issue
# This script should be run after installing requirements.txt

echo "Checking for opencv-python installation..."
if pip show opencv-python > /dev/null 2>&1; then
    echo "Found opencv-python - uninstalling to avoid OpenGL dependency issues..."
    pip uninstall opencv-python -y
    echo "opencv-python uninstalled successfully"
else
    echo "opencv-python not found - skipping"
fi

echo "Verifying opencv-python-headless is installed..."
if pip show opencv-python-headless > /dev/null 2>&1; then
    echo "opencv-python-headless is installed ✓"
else
    echo "Installing opencv-python-headless..."
    pip install opencv-python-headless>=4.8.0
fi

echo "Setup complete!"

