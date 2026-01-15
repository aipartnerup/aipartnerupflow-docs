#!/bin/bash
# Setup script for apflow-docs

set -e

echo "==> Setting up apflow-docs..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "==> Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "==> Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "==> Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "==> Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "==> Installing dependencies..."
pip install -r requirements.txt

# Sync documentation
echo "==> Syncing documentation from main repository..."
python scripts/sync_docs.py

echo ""
echo "==> Setup complete!"
echo ""
echo "To start the development server, run:"
echo "  source venv/bin/activate"
echo "  mkdocs serve"
echo ""
echo "To build the documentation, run:"
echo "  mkdocs build"

