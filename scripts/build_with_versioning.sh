#!/bin/bash
# Build script with versioning support
# This script can be used by both GitHub Actions and server deployment
#
# Usage:
#   ./scripts/build_with_versioning.sh [OUTPUT_DIR]
#   OUTPUT_DIR: Output directory (default: site)

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get output directory from argument or use default
OUTPUT_DIR="${1:-site}"

echo -e "${GREEN}==> Building documentation with versioning...${NC}"

# Check if versions.json exists
if [ ! -f "docs/versions.json" ]; then
    echo -e "${RED}Error: docs/versions.json not found!${NC}"
    echo -e "${YELLOW}Please run sync_docs.py first to generate versions.json${NC}"
    exit 1
fi

# Get version from versions.json
VERSION=$(python3 -c "import json; data = json.load(open('docs/versions.json')); print(data[0]['version'])")
echo -e "${GREEN}==> Building version: ${VERSION}${NC}"

# Build documentation to temporary directory
echo -e "${GREEN}==> Building MkDocs site...${NC}"
mkdocs build -d site_temp

# Create versioned directory structure
echo -e "${GREEN}==> Creating versioned directory structure...${NC}"
mkdir -p "$OUTPUT_DIR/$VERSION"
cp -r site_temp/* "$OUTPUT_DIR/$VERSION/"

# Create latest alias
mkdir -p "$OUTPUT_DIR/latest"
cp -r site_temp/* "$OUTPUT_DIR/latest/"

# Copy latest version content directly to root directory
# This allows root path to show latest version without redirect
echo -e "${GREEN}==> Copying latest version to root directory...${NC}"
cp -r site_temp/* "$OUTPUT_DIR/"

# Clean up temporary directory
rm -rf site_temp

echo -e "${GREEN}==> Versioned documentation structure created for $VERSION${NC}"
echo -e "${GREEN}==> Build output: $OUTPUT_DIR/${NC}"

