# Deployment Guide

This document explains how to deploy the aipartnerupflow documentation website.

## Automatic Deployment (GitHub Pages)

The documentation is automatically deployed to GitHub Pages when changes are pushed to the `main` branch via GitHub Actions.

### Setup GitHub Pages

1. Go to your repository settings on GitHub
2. Navigate to "Pages" in the left sidebar
3. Under "Source", select "GitHub Actions"
4. The workflow will automatically deploy on push to `main`

### Workflow

The deployment workflow (`.github/workflows/deploy.yml`) will:

1. Checkout the repository
2. Set up Python 3.12
3. Install dependencies from `requirements.txt`
4. Sync documentation from main repository
5. Build the documentation with versioning (using `scripts/build_with_versioning.sh`)
6. Deploy to GitHub Pages

The workflow uses a shared build script (`scripts/build_with_versioning.sh`) that creates the versioned directory structure (`/0.2.0/`, `/latest/`, etc.).

## Manual Deployment

### Using mkdocs gh-deploy

```bash
# Install dependencies
pip install -r requirements.txt

# Deploy to GitHub Pages
mkdocs gh-deploy
```

This will:
- Build the documentation
- Create a `gh-pages` branch (if it doesn't exist)
- Push the built site to the `gh-pages` branch
- GitHub Pages will automatically serve the site

### Using mkdocs build + manual upload

```bash
# Build the documentation
mkdocs build

# The site will be in the `site/` directory
# You can then upload it to any static hosting service
```

## Custom Domain

To use a custom domain (e.g., `docs.aipartnerup.com`):

1. Add a `CNAME` file in the `docs/` directory with your domain:
   ```
   docs.aipartnerup.com
   ```

2. Configure DNS:
   - Add a CNAME record pointing to `your-username.github.io`

3. Update `mkdocs.yml`:
   ```yaml
   site_url: https://flow.aipartnerup.com
   ```

## Scripts Overview

The project has different scripts for different purposes:

- **`start.sh`**: Start development server (live preview with hot reload)
  ```bash
  ./scripts/start.sh  # Starts at http://localhost:8000
  ```

- **`build_with_versioning.sh`**: Build static site with versioning
  ```bash
  ./scripts/build_with_versioning.sh  # Outputs to site/
  ```

- **`deploy.sh`**: Build and optionally deploy to server
  ```bash
  ./scripts/deploy.sh  # Just build
  DEPLOY_PATH=/var/www/html ./scripts/deploy.sh  # Build + deploy
  ```

## Server Deployment

For deploying directly to a server (Nginx, Apache, etc.) instead of GitHub Pages:

### Prerequisites

- Python 3.10+ (3.12+ recommended)
- Access to the server
- Web server (Nginx, Apache, etc.) configured

### Quick Start

1. **Setup (First Time Only)**:
   ```bash
   ./scripts/setup.sh
   ```

2. **Build and Deploy (Default: site/ directory)**:
   ```bash
   # Deploy to project's site/ directory (default, no sudo needed)
   ./scripts/deploy.sh
   
   # Output will be in: site/0.2.0/, site/latest/, etc.
   ```

3. **Build Only (No Deployment)**:
   ```bash
   # Just build without deploying
   DEPLOY_PATH="" ./scripts/deploy.sh
   
   # Or use the build script directly
   ./scripts/build_with_versioning.sh
   ```

4. **Deploy to Server**:
   ```bash
   # Deploy to server (specify absolute path)
   DEPLOY_PATH=/var/www/html ./scripts/deploy.sh

   # Or set it as environment variable
   export DEPLOY_PATH=/var/www/html
   ./scripts/deploy.sh
   ```

### Configuration

The deployment script supports environment variables:

```bash
# Main repository path (for syncing docs)
export MAIN_REPO_PATH=/path/to/aipartnerupflow

# Deployment path (default: site/ in project root, MkDocs convention)
# Use relative path for local deployment (e.g., "site", "dist")
# Use absolute path for server deployment (e.g., "/var/www/html")
export DEPLOY_PATH=site  # Default: project's site/ directory (MkDocs convention)
# export DEPLOY_PATH=/var/www/html  # Server deployment

# Skip documentation sync (if docs are already synced)
export SYNC_DOCS=false

# Run deployment
./scripts/deploy.sh
```

**Default Behavior:**
- By default, deploys to `site/` directory (MkDocs convention)
- No sudo required for local deployment
- Perfect for local testing or when you want to keep built files in the project
- The `site/` directory is automatically added to `.gitignore`
- Consistent with GitHub Actions workflow (also uses `site/`)

### What the Script Does

1. **Sync Documentation**: Syncs docs from main repository (if `MAIN_REPO_PATH` is set)
2. **Build with Versioning**: Uses `scripts/build_with_versioning.sh` to create versioned structure
3. **Deploy**: By default, copies built site to `html/` directory (or custom `DEPLOY_PATH`)

**Deployment Paths:**
- **Default (`site/`)**: Local project directory, no sudo needed (MkDocs convention)
  - Output: `site/0.2.0/`, `site/latest/`, etc.
  - Perfect for local testing or keeping built files in project
  - Consistent with GitHub Actions and MkDocs defaults
- **Server Path (`/var/www/html`)**: Absolute path, requires sudo
  - Output: `/var/www/html/0.2.0/`, `/var/www/html/latest/`, etc.
  - For production server deployment
- **Empty (`DEPLOY_PATH=""`)**: Only build, no deployment
  - Output: `site/` directory only
  - For CI/CD pipelines that handle deployment separately

The `deploy.sh` script uses the same `build_with_versioning.sh` script as GitHub Actions, ensuring consistent builds across both deployment methods.

## Versioning

The documentation supports versioning through a shared build script (`scripts/build_with_versioning.sh`) that:

1. Reads version from `docs/versions.json`
2. Builds documentation to a temporary directory
3. Creates versioned directory structure:
   - `/0.2.0/` - Version-specific documentation
   - `/latest/` - Alias to latest version
   - `/` - Redirects to default version

This script is used by both:
- **GitHub Actions** (`.github/workflows/deploy.yml`)
- **Server Deployment** (`scripts/deploy.sh`)

This ensures consistent versioning behavior across all deployment methods.

### Manual Versioning

If you need to manually build with versioning:

```bash
# Just build (no deployment)
./scripts/build_with_versioning.sh

# The built site will be in site/ directory
```

The `mkdocs.yml` already includes version support configuration (`version.provider: mike`).

## Search Functionality

**Yes, search works with static deployment!** 

MkDocs uses **client-side search** which means:

1. **Search Index**: Generated during build as `search_index.json`
2. **No Server Required**: Search runs entirely in the browser using JavaScript
3. **Versioned Support**: Each version directory (`/0.2.0/`, `/latest/`) has its own search index

The search plugin is already enabled in `mkdocs.yml`:
```yaml
plugins:
  - search
```

And Material theme search features are enabled:
```yaml
features:
  - search.suggest
  - search.highlight
```

**How it works:**
- When you build the site, MkDocs generates `search_index.json` in each version directory
- The Material theme's search UI loads this file and performs searches in the browser
- No server-side processing is needed - it's 100% static!

**Testing search:**
1. Build the site: `./scripts/build_with_versioning.sh`
2. Check that `site/0.2.0/search_index.json` exists
3. Deploy and test the search box in the Material theme

## Troubleshooting

### Build fails

- Check Python version (requires 3.10+)
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check for syntax errors in `mkdocs.yml`

### Deployment fails

- Ensure GitHub Actions has write permissions
- Check GitHub Pages settings
- Verify the workflow file syntax

### Site not updating

- Clear browser cache
- Check GitHub Actions logs
- Verify the deployment was successful

### Search not working

- Verify `search_index.json` exists in the version directory (e.g., `site/0.2.0/search_index.json`)
- Check browser console for JavaScript errors
- Ensure `site_url` in `mkdocs.yml` is correctly set
- For versioned deployments, each version should have its own search index

