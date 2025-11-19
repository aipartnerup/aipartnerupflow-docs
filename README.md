# aipartnerupflow Documentation

This repository contains the documentation website for [aipartnerupflow](https://github.com/aipartnerup/aipartnerupflow), built with [MkDocs](https://www.mkdocs.org/) and [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

## Overview

This is a standalone documentation project that serves the developer documentation for the aipartnerupflow library. The documentation source files are maintained in the main [aipartnerupflow](https://github.com/aipartnerup/aipartnerupflow) repository under the `docs/` directory.

## Setup

### Prerequisites

- Python 3.10 or higher (3.12+ recommended)
- pip

### Quick Setup

Use the setup script for automatic setup:

```bash
git clone https://github.com/aipartnerup/aipartnerupflow-docs.git
cd aipartnerupflow-docs
./scripts/setup.sh
```

### Manual Setup

1. Clone this repository:
```bash
git clone https://github.com/aipartnerup/aipartnerupflow-docs.git
cd aipartnerupflow-docs
```

2. Create a virtual environment (recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Sync documentation from main repository:
```bash
python scripts/sync_docs.py
```

## Development

### Local Development Server

Start the local development server to preview the documentation:

```bash
mkdocs serve
```

The documentation will be available at `http://127.0.0.1:8000`.

### Building Documentation

Build the static site:

```bash
mkdocs build
```

The output will be in the `site/` directory.

### Syncing Documentation from Main Repository

The documentation source files are maintained in the main aipartnerupflow repository. The `docs/` directory is automatically synced during CI/CD deployment.

For local development, you can sync manually:

1. Use the sync script:
```bash
python scripts/sync_docs.py
```

2. Or use the CI/CD version:
```bash
MAIN_REPO_PATH=../aipartnerupflow python scripts/sync_docs_ci.py
```

**Note**: Website-specific files (`index.md`, `getting-started/`) are kept in version control and are NOT synced from the main repository.

## Deployment

The documentation is automatically deployed to GitHub Pages when changes are pushed to the `main` branch via GitHub Actions.

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

### Manual Deployment

To manually deploy:

```bash
mkdocs gh-deploy
```

## Project Structure

```
aipartnerupflow-docs/
├── docs/                    # Documentation source files (Markdown)
│   ├── index.md            # Home page
│   ├── getting-started/    # Getting started guides
│   ├── user-guide/         # User documentation
│   ├── architecture/       # Architecture documentation
│   ├── development/        # Development guides
│   └── ...
├── mkdocs.yml              # MkDocs configuration
├── requirements.txt        # Python dependencies
├── .github/
│   └── workflows/
│       └── deploy.yml      # GitHub Actions deployment
└── README.md               # This file
```

## Documentation Source

The documentation source files are maintained in the main repository:
- Repository: [aipartnerup/aipartnerupflow](https://github.com/aipartnerup/aipartnerupflow)
- Documentation directory: `docs/`

## Contributing

To contribute to the documentation:

1. Make changes to the documentation files in the main [aipartnerupflow](https://github.com/aipartnerup/aipartnerupflow) repository's `docs/` directory
2. Sync the changes to this repository (or use the sync script)
3. Test locally with `mkdocs serve`
4. Commit and push changes
5. The documentation will be automatically deployed

## License

Apache-2.0 (same as the main aipartnerupflow project)

