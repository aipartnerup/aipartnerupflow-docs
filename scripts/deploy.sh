#!/bin/bash
# Server deployment script for aipartnerupflow-docs
# This script builds and deploys the documentation with versioning support

set -e

# Default values
# DEPLOY_PATH: Default to project's site/ directory (MkDocs convention)
# Set to empty to only build (no deployment)
# Set to custom path to deploy to server (e.g., /var/www/html)
DEPLOY_PATH="${DEPLOY_PATH:-site}"
MAIN_REPO_PATH="${MAIN_REPO_PATH:-../aipartnerupflow}"
SYNC_DOCS="${SYNC_DOCS:-true}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}==> Starting documentation deployment...${NC}"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}==> Virtual environment not found. Running setup...${NC}"
    ./scripts/setup.sh
fi

# Activate virtual environment
echo -e "${GREEN}==> Activating virtual environment...${NC}"
source .venv/bin/activate

# Ensure dependencies are installed
echo -e "${GREEN}==> Ensuring dependencies are installed...${NC}"
if ! python -c "import mkdocs" 2>/dev/null; then
    echo -e "${YELLOW}==> Dependencies not found, installing...${NC}"
    pip install --upgrade pip
    pip install -r requirements.txt
else
    # Check if requirements.txt has changed (optional: reinstall if needed)
    if [ -n "${FORCE_INSTALL:-}" ] && [ "$FORCE_INSTALL" = "true" ]; then
        echo -e "${YELLOW}==> Force reinstalling dependencies...${NC}"
        pip install --upgrade pip
        pip install -r requirements.txt
    else
        echo -e "${GREEN}==> Dependencies already installed${NC}"
    fi
fi

# Sync documentation from main repository
if [ "$SYNC_DOCS" = "true" ]; then
    echo -e "${GREEN}==> Syncing documentation from main repository...${NC}"
    if [ -n "$MAIN_REPO_PATH" ] && [ -d "$MAIN_REPO_PATH" ]; then
        python scripts/sync_docs.py --force --preserve --path "$MAIN_REPO_PATH"
    else
        echo -e "${YELLOW}==> Main repository path not found, skipping sync...${NC}"
        echo -e "${YELLOW}   Set MAIN_REPO_PATH environment variable to sync docs${NC}"
    fi
fi

# Determine output directory
# If DEPLOY_PATH is set, build directly to it (no intermediate site/ directory)
# Otherwise, build to site/ (for GitHub Actions or manual use)
if [ -n "$DEPLOY_PATH" ] && [ "$DEPLOY_PATH" != "" ]; then
    BUILD_OUTPUT="$DEPLOY_PATH"
    echo -e "${GREEN}==> Building directly to: $BUILD_OUTPUT${NC}"
else
    BUILD_OUTPUT="site"
    echo -e "${GREEN}==> Building to: $BUILD_OUTPUT${NC}"
fi

# Build documentation with versioning (directly to target directory)
echo -e "${GREEN}==> Building documentation with versioning...${NC}"
./scripts/build_with_versioning.sh "$BUILD_OUTPUT"

# Set permissions if deploying to a path
if [ -n "$DEPLOY_PATH" ] && [ "$DEPLOY_PATH" != "" ]; then
    echo -e "${GREEN}==> Deploying to: $DEPLOY_PATH${NC}"
    
    # Check if it's a local path (relative) or server path (absolute starting with /)
    IS_LOCAL_PATH=false
    if [[ ! "$DEPLOY_PATH" =~ ^/ ]]; then
        IS_LOCAL_PATH=true
    fi
    
    # Check if deploy path exists
    if [ ! -d "$DEPLOY_PATH" ]; then
        echo -e "${YELLOW}==> Deploy path does not exist, creating...${NC}"
        if [ "$IS_LOCAL_PATH" = true ]; then
            mkdir -p "$DEPLOY_PATH"
        else
            sudo mkdir -p "$DEPLOY_PATH"
        fi
    fi
    
    # Backup existing deployment (optional)
    if [ -d "$DEPLOY_PATH" ] && [ "$(ls -A $DEPLOY_PATH 2>/dev/null)" ]; then
        BACKUP_DIR="${DEPLOY_PATH}.backup.$(date +%Y%m%d_%H%M%S)"
        echo -e "${YELLOW}==> Backing up existing deployment to: $BACKUP_DIR${NC}"
        if [ "$IS_LOCAL_PATH" = true ]; then
            cp -r "$DEPLOY_PATH" "$BACKUP_DIR" 2>/dev/null || true
        else
            sudo cp -r "$DEPLOY_PATH" "$BACKUP_DIR" 2>/dev/null || true
        fi
    fi
    
    # Files are already in DEPLOY_PATH (built directly there)
    # Just set permissions if needed
    if [ "$IS_LOCAL_PATH" = false ]; then
        # Set proper permissions for server deployment
        echo -e "${GREEN}==> Setting permissions...${NC}"
        sudo chown -R www-data:www-data "$DEPLOY_PATH" 2>/dev/null || \
        sudo chown -R nginx:nginx "$DEPLOY_PATH" 2>/dev/null || \
        sudo chown -R $(whoami):$(whoami) "$DEPLOY_PATH"
        sudo chmod -R 755 "$DEPLOY_PATH"
    else
        chmod -R 755 "$DEPLOY_PATH"
    fi
    
    # Get version for display
    VERSION=$(python3 -c "import json; data = json.load(open('docs/versions.json')); print(data[0]['version'])")
    echo -e "${GREEN}==> Deployment complete!${NC}"
    if [ "$IS_LOCAL_PATH" = true ]; then
        echo -e "${GREEN}==> Documentation available in: $DEPLOY_PATH/$VERSION/${NC}"
    else
        echo -e "${GREEN}==> Documentation available at: http://your-domain/$VERSION/${NC}"
    fi
else
    echo -e "${GREEN}==> Build complete!${NC}"
    echo -e "${GREEN}==> Built site is available in: $BUILD_OUTPUT/${NC}"
    echo -e "${YELLOW}==> Set DEPLOY_PATH to build directly to deployment directory${NC}"
fi

echo -e "${GREEN}==> Done!${NC}"

