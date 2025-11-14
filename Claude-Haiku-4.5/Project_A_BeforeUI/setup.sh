#!/bin/bash
# Setup script for Project A (Before UI Improvement)

set -e

echo "Setting up Project A (Before UI)..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright browsers
echo "Installing Playwright browsers..."
playwright install chromium

echo "Setup complete! Project A is ready."
echo ""
echo "To run tests:"
echo "  bash run_tests.sh"
