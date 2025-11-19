# Documentation Workflow

This document explains how the documentation is managed and synced between the main repository and the documentation website.

## Overview

The documentation follows a **single source of truth** model:
- **Main Repository** (`aipartnerup/aipartnerupflow`): Contains the source documentation files
- **Documentation Repository** (`aipartnerup/aipartnerupflow-docs`): Contains the website configuration and website-specific files

## File Categories

### 1. Synced from Main Repository

These files are automatically synced from `aipartnerupflow/docs/` during CI/CD deployment:

- `docs/architecture/` - Architecture documentation
- `docs/development/` - Development guides
- `docs/configuration/` - Configuration documentation
- `docs/planning/` - Planning documents
- `docs/usage/` - Usage guides
- `docs/index.md` - Documentation index (note: website's `docs/index.md` is homepage, preserved during sync)
- `docs/STRUCTURE.md` - Documentation structure

**These files are NOT committed to the documentation repository** (ignored by `.gitignore`).

### 2. Website-Specific Files

These files are maintained in the documentation repository and are NOT synced:

- `docs/index.md` - MkDocs homepage
- `docs/getting-started/` - Website-specific getting started guides
  - `installation.md`
  - `quick-start.md`
  - `examples.md`

**These files ARE committed to the documentation repository**.

## Workflow

### For Documentation Authors

1. **Edit documentation** in the main repository: `aipartnerupflow/docs/`
2. **Commit and push** to the main repository
3. **Documentation is automatically synced** during the next deployment

### For Website Maintainers

1. **Edit website-specific files** in the documentation repository: `aipartnerupflow-docs/docs/`
2. **Commit and push** to the documentation repository
3. **Website is automatically deployed** via GitHub Actions

### Local Development

For local development, you can manually sync documentation:

```bash
# Sync from main repository
python scripts/sync_docs.py

# Or use CI/CD version (supports custom paths)
MAIN_REPO_PATH=../aipartnerupflow python scripts/sync_docs_ci.py
```

## CI/CD Deployment

The GitHub Actions workflow automatically:

1. Checks out both repositories
2. Syncs documentation from main repository
3. Builds the MkDocs site
4. Deploys to GitHub Pages

See `.github/workflows/deploy.yml` for details.

## Adding New Documentation

### Adding to Main Repository

1. Add files to `aipartnerupflow/docs/`
2. They will be automatically synced during deployment

### Adding Website-Specific Content

1. Add files to `aipartnerupflow-docs/docs/`
2. Update `mkdocs.yml` navigation if needed
3. Commit to the documentation repository

## Troubleshooting

### Documentation not updating

- Check if files are in the correct repository (main vs docs)
- Verify sync script is running in CI/CD
- Check GitHub Actions logs

### Website-specific files missing

- Ensure files are in `docs/index.md` or `docs/getting-started/`
- Check `.gitignore` exceptions (`!docs/index.md`, `!docs/getting-started/`)

