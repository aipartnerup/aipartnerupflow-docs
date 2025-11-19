#!/usr/bin/env python3
"""
Script to sync documentation files from the main aipartnerupflow repository.

Usage:
    python3 scripts/sync_docs.py [--ci] [--force] [--preserve] [--path /path/to/repo]
"""

import os
import shutil
import argparse
import subprocess
import tempfile
import tempfile
from pathlib import Path

try:
    import clean_docs
except ImportError:
    # Fallback for when running as a module or from different CWD
    from scripts import clean_docs

# Configuration
DOCS_SOURCE_REL = Path("../aipartnerupflow/docs")
DOCS_TARGET = Path("docs")


def should_exclude(path: Path) -> bool:
    """Check if a file or directory should be excluded from sync."""
    # Exclude hidden files/dirs
    if path.name.startswith("."):
        return True
    # Exclude __pycache__
    if path.name == "__pycache__":
        return True
    # Exclude README.md (legacy, now renamed to index.md)
    if path.name == "README.md":
        return True
    # Note: index.md in root docs/ is handled by website-specific file preservation
    return False


def sync_docs(force: bool = False, preserve: bool = False, repo_path: str = None, git_url: str = None, git_branch: str = "main"):
    """Sync documentation files from source to target."""
    temp_dir = None
    
    try:
        if git_url:
            print(f"Cloning from {git_url} (branch: {git_branch})...")
            temp_dir = tempfile.mkdtemp()
            subprocess.run(
                ["git", "clone", "--depth", "1", "--branch", git_branch, git_url, temp_dir],
                check=True,
                capture_output=True
            )
            source_path = Path(temp_dir) / "docs"
            main_repo_path = Path(temp_dir)
        elif repo_path:
            main_repo_path = Path(repo_path)
            source_path = main_repo_path / "docs"
        else:
            # Default to relative path
            main_repo_path = Path("../aipartnerupflow")
            source_path = main_repo_path / "docs"

        if not source_path.exists():
            print(f"Error: Source directory not found: {source_path}")
            if not git_url:
                print("Please ensure the aipartnerupflow repository is in the parent directory or use --path / --git-url.")
            return False

        print(f"Syncing from: {source_path.resolve()}")
        print(f"Syncing to:   {DOCS_TARGET.resolve()}")
        print(f"Mode:         {'Force' if force else 'Incremental'}")
        print(f"Preserve:     {'Yes' if preserve else 'No'}")

        # Create target directory if it doesn't exist
        DOCS_TARGET.mkdir(parents=True, exist_ok=True)

        # Copy files
        copied_count = 0
        skipped_count = 0
        
        for root, dirs, files in os.walk(source_path):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if not should_exclude(Path(root) / d)]

            # Calculate relative path
            rel_path = Path(root).relative_to(source_path)
            
            # Skip website-specific files if preserve is True
            if preserve and clean_docs.is_website_specific(rel_path):
                continue

            target_dir = DOCS_TARGET / rel_path
            target_dir.mkdir(parents=True, exist_ok=True)

            # Copy files
            for file in files:
                if should_exclude(Path(root) / file):
                    continue

                file_rel_path = rel_path / file
                
                # Skip website-specific files if preserve is True
                if preserve and clean_docs.is_website_specific(file_rel_path):
                    skipped_count += 1
                    continue

                source_file = Path(root) / file
                target_file = target_dir / file

                # Copy file if force is True or if it's newer/missing
                if force or not target_file.exists() or source_file.stat().st_mtime > target_file.stat().st_mtime:
                    shutil.copy2(source_file, target_file)
                    copied_count += 1
                    print(f"Copied: {file_rel_path}")

        print(f"\nSync complete! Copied {copied_count} file(s).")
        if preserve:
            print(f" Skipped {skipped_count} website-specific file(s).")
        else:
            print("")
            
        # Generate versions.json
        generate_versions_json(main_repo_path, DOCS_TARGET)
            
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        return False
    finally:
        print(f"Sync complete! temp_dir: {temp_dir}")
        # Cleanup temp directory
        if temp_dir and os.path.exists(temp_dir):
            print("Cleaning up temporary directory...")
            shutil.rmtree(temp_dir)


def get_project_version(repo_path: Path) -> str:
    """Read version from pyproject.toml."""
    pyproject_path = repo_path / "pyproject.toml"
    if not pyproject_path.exists():
        print(f"Warning: pyproject.toml not found at {pyproject_path}")
        return "dev"
    
    try:
        with open(pyproject_path, "r") as f:
            for line in f:
                if line.startswith("version = "):
                    return line.split("=")[1].strip().strip('"').strip("'")
    except Exception as e:
        print(f"Warning: Failed to read version from pyproject.toml: {e}")
        
    return "dev"


def generate_versions_json(repo_path: Path, target_dir: Path):
    """Generate versions.json file."""
    version = get_project_version(repo_path)
    
    # Create a simple versions.json for local dev/mike compatibility
    # In a real mike setup, this file is managed by mike, but for local dev
    # we need it to exist to avoid 404s if the theme expects it.
    import json
    
    versions_data = [
        {
            "version": version,
            "title": version,
            "aliases": ["latest"]
        }
    ]
    
    versions_file = target_dir / "versions.json"
    with open(versions_file, "w") as f:
        json.dump(versions_data, f, indent=2)
    
    print(f"Generated versions.json with version: {version}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync documentation files.")
    parser.add_argument("--ci", action="store_true", help="Run in CI mode (implies --force, --preserve, and --clean, uses MAIN_REPO_PATH env var)")
    parser.add_argument("--force", action="store_true", help="Force copy all files regardless of timestamps")
    parser.add_argument("--preserve", action="store_true", help="Preserve website-specific files (do not overwrite from source)")
    parser.add_argument("--clean", action="store_true", help="Clean docs directory before syncing (preserves website-specific files)")
    parser.add_argument("--path", help="Path to the main repository", default=None)
    DEFAULT_GIT_URL = "https://github.com/aipartnerup/aipartnerupflow.git"
    parser.add_argument("--git-url", nargs="?", const=DEFAULT_GIT_URL, help=f"URL of the git repository to clone (default if flag used: {DEFAULT_GIT_URL})")
    parser.add_argument("--git-branch", help="Branch to clone", default="main")
    
    args = parser.parse_args()
    
    force = args.force
    preserve = args.preserve
    clean = args.clean
    repo_path = args.path
    
    if args.ci:
        force = True
        preserve = True
        clean = True
        if not repo_path:
            repo_path = os.getenv("MAIN_REPO_PATH")
            
    if clean:
        clean_docs.clean_docs()
            
    sync_docs(force=force, preserve=preserve, repo_path=repo_path, git_url=args.git_url, git_branch=args.git_branch)
