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
4. Build the documentation with `mkdocs build`
5. Deploy to GitHub Pages

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

## Versioning

To support multiple versions of the documentation:

1. Install `mike`:
   ```bash
   pip install mike
   ```

2. Deploy a version:
   ```bash
   mike deploy 0.1.0
   ```

3. Set default version:
   ```bash
   mike set-default 0.1.0
   ```

The `mkdocs.yml` already includes version support configuration.

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

