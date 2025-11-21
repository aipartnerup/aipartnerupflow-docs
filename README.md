# aipartnerupflow Documentation

This repository contains the documentation website for [aipartnerupflow](https://github.com/aipartnerup/aipartnerupflow), built with [MkDocs](https://www.mkdocs.org/) and [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

## Overview

This is a standalone documentation project that serves the developer documentation for the aipartnerupflow library. The documentation source files are maintained in the main [aipartnerupflow](https://github.com/aipartnerup/aipartnerupflow) repository under the `docs/` directory.

## Quick Start

Choose one of the following methods to run the documentation locally.

### Option 1: Docker (Recommended)

**Prerequisites:**
- Docker
- Docker Compose

**Start the server:**

```bash
docker-compose up
```

The documentation will be available at `http://localhost:8000`.

> [!TIP]
> **Docker Usage Guide**
> *   **Content Changes**: Modifications to `docs/*.md` files are applied automatically (Live Reload).
> *   **Configuration Changes**: Modifications to `mkdocs.yml` usually reload automatically. If not, run `docker-compose restart`.
> *   **Dependency Changes**: If you modify `requirements.txt` or `Dockerfile`, you **must** rebuild the image:
>     ```bash
>     docker-compose up --build
>     ```

### Option 2: Local Development

**Prerequisites:**
- Python 3.10 or higher (3.12+ recommended)
- pip

**1. Setup:**

Use the setup script to create a virtual environment and install dependencies:

```bash
./scripts/setup.sh
```

**2. Start the server:**

Use the start script to launch the development server:

```bash
./scripts/start.sh
```

The documentation will be available at `http://localhost:8000`.

## Configuration

### Port Configuration

You can configure the application port using a `.env` file or environment variables. This works for both Docker and Local Development.

1. **Create configuration file:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set your desired port, e.g., `PORT=8001`.

2. **Or use environment variables:**
   
   **Docker:**
   ```bash
   PORT=8001 docker-compose up
   ```

   **Local:**
   ```bash
   export PORT=8001
   ./scripts/start.sh
   ```

## Advanced Usage

### Manual Setup

If you prefer not to use the scripts:

1.  Create a virtual environment: `python -m venv .venv`
2.  Activate it: `source .venv/bin/activate`
3.  Install dependencies: `pip install -r requirements.txt`
4.  Sync docs: `python scripts/sync_docs.py`
5.  Serve: `mkdocs serve`

### Building Documentation

**For Development (Live Preview)**:
```bash
# Start development server with live reload
./scripts/start.sh
```
This starts a development server at `http://localhost:8000` with automatic reload on file changes.

**For Production (Static Build)**:
```bash
# Build and deploy to site/ directory (default, recommended)
./scripts/deploy.sh

# Or just build without deploying
DEPLOY_PATH="" ./scripts/deploy.sh

# Or use the build script directly
./scripts/build_with_versioning.sh

# Or traditional mkdocs build (no versioning)
mkdocs build
```

**Output Locations:**
- Default: `site/0.2.0/`, `site/latest/` (when using `./scripts/deploy.sh`)
- Server: `/var/www/html/0.2.0/` (when `DEPLOY_PATH=/var/www/html`)
- All use the same `site/` directory convention (MkDocs standard)

### Syncing Documentation

The documentation source files are maintained in the main `aipartnerupflow` repository.

- **Local Sync**:
  ```bash
  python scripts/sync_docs.py
  ```

- **CI/CD Sync**:
  ```bash
  # Syncs and forces overwrite, skipping website-specific files
  python scripts/sync_docs.py --ci --path ../aipartnerupflow
  ```

## Deployment

The documentation is automatically deployed to GitHub Pages when changes are pushed to the `main` branch via GitHub Actions. See [DEPLOYMENT.md](DEPLOYMENT.md) for details.

To manually deploy:
```bash
mkdocs gh-deploy
```

## Project Structure

```
aipartnerupflow-docs/
├── docs/                    # Documentation source files (Markdown)
├── mkdocs.yml              # MkDocs configuration
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose configuration
├── scripts/
│   ├── setup.sh            # Setup script
│   ├── start.sh            # Start script
│   └── sync_docs.py        # Documentation sync script
└── README.md               # This file
```

## Contributing

1. Make changes to the documentation files in the main [aipartnerupflow](https://github.com/aipartnerup/aipartnerupflow) repository's `docs/` directory.
2. Sync the changes to this repository.
3. Test locally.
4. Commit and push.

## License

Apache-2.0
