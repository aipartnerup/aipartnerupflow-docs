#!/usr/bin/env python3
"""
Script to sync documentation files from the main aipartnerupflow repository.

Usage:
    python3 scripts/sync_docs.py [--ci] [--force] [--preserve] [--path /path/to/repo]
"""

import os
import shutil
import argparse
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DEFAULT_MAIN_REPO_PATH = PROJECT_ROOT.parent / "aipartnerupflow"

# Files to exclude from sync (always excluded)
EXCLUDE_PATTERNS = [
    "__pycache__",
    "*.pyc",
    ".git",
    ".DS_Store",
]

# Website-specific files that should NOT be synced if --preserve or --ci is used
WEBSITE_SPECIFIC_FILES = [
    "index.md",  # MkDocs homepage
    "getting-started/",  # Website-specific getting started guides
]


def should_exclude(path: Path) -> bool:
    """Check if a path should be excluded."""
    path_str = str(path)
    for pattern in EXCLUDE_PATTERNS:
        if pattern in path_str:
            return True
    return False


def is_website_specific(rel_path: Path) -> bool:
    """Check if a file is website-specific and should not be synced."""
    path_str = str(rel_path)
    for pattern in WEBSITE_SPECIFIC_FILES:
        if path_str.startswith(pattern) or path_str == pattern:
            return True
    return False


def sync_docs(force: bool = False, preserve: bool = False, repo_path: str = None):
    """Sync documentation files from source to target."""
    
    # Determine source path
    if repo_path:
        main_repo_path = Path(repo_path)
    else:
        main_repo_path = DEFAULT_MAIN_REPO_PATH
        
    docs_source = main_repo_path / "docs"
    docs_target = PROJECT_ROOT / "docs"

    if not docs_source.exists():
        print(f"Error: Source directory not found: {docs_source}")
        print(f"Main repo path: {main_repo_path}")
        print("Please ensure the aipartnerupflow repository is accessible.")
        return False

    print(f"Syncing from: {docs_source}")
    print(f"Syncing to:   {docs_target}")
    print(f"Mode:         {'Force Copy' if force else 'Incremental'}")
    print(f"Preserve:     {'Yes' if preserve else 'No'}")

    # Create target directory if it doesn't exist
    docs_target.mkdir(parents=True, exist_ok=True)

    # Copy files
    copied_count = 0
    skipped_count = 0
    
    for root, dirs, files in os.walk(docs_source):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if not should_exclude(Path(root) / d)]

        # Calculate relative path
        rel_path = Path(root).relative_to(docs_source)
        
        # Skip website-specific files if preserve is True
        if preserve and is_website_specific(rel_path):
            continue

        target_dir = docs_target / rel_path
        target_dir.mkdir(parents=True, exist_ok=True)

        # Copy files
        for file in files:
            if should_exclude(Path(root) / file):
                continue

            file_rel_path = rel_path / file
            
            # Skip website-specific files if preserve is True
            if preserve and is_website_specific(file_rel_path):
                skipped_count += 1
                continue

            source_file = Path(root) / file
            target_file = target_dir / file

            # Copy logic
            should_copy = False
            if force:
                should_copy = True
            elif not target_file.exists():
                should_copy = True
            elif source_file.stat().st_mtime > target_file.stat().st_mtime:
                should_copy = True
            
            if should_copy:
                shutil.copy2(source_file, target_file)
                copied_count += 1
                print(f"Copied: {file_rel_path}")

    print(f"\nSync complete! Copied {copied_count} file(s).", end="")
    if preserve:
        print(f" Skipped {skipped_count} website-specific file(s).")
    else:
        print("")
        
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync documentation files.")
    parser.add_argument("--ci", action="store_true", help="Run in CI mode (implies --force and --preserve, uses MAIN_REPO_PATH env var)")
    parser.add_argument("--force", action="store_true", help="Force copy all files regardless of timestamps")
    parser.add_argument("--preserve", action="store_true", help="Preserve website-specific files (do not overwrite from source)")
    parser.add_argument("--path", help="Path to the main repository", default=None)
    
    args = parser.parse_args()
    
    force = args.force
    preserve = args.preserve
    repo_path = args.path
    
    if args.ci:
        force = True
        preserve = True
        if not repo_path:
            repo_path = os.getenv("MAIN_REPO_PATH")
            
    sync_docs(force=force, preserve=preserve, repo_path=repo_path)

