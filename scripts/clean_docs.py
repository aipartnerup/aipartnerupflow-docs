#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

# Configuration
DOCS_TARGET = Path("docs")

# Files that are specific to the website and should be preserved
# This MUST match the list in sync_docs.py and .gitignore logic
WEBSITE_SPECIFIC_FILES = {
    "index.md",
    "assets",  # Directory
    "versions.json",
}

def is_website_specific(rel_path: Path) -> bool:
    """Check if a file or directory is website-specific."""
    path_str = str(rel_path)
    
    # Exact match
    if path_str in WEBSITE_SPECIFIC_FILES:
        return True
        
    # Check if it's inside a preserved directory
    for specific in WEBSITE_SPECIFIC_FILES:
        # If specific is a directory (no extension usually implies dir in this context, 
        # but better to be explicit or check if it matches start of path)
        if path_str.startswith(f"{specific}/"):
            return True
            
    return False

def clean_docs():
    """Clean up docs directory, preserving website-specific files."""
    if not DOCS_TARGET.exists():
        print(f"Docs directory not found: {DOCS_TARGET}")
        return

    print(f"Cleaning up {DOCS_TARGET}...")
    
    deleted_count = 0
    preserved_count = 0
    
    # Get all top-level items in docs/
    for item in DOCS_TARGET.iterdir():
        rel_path = item.relative_to(DOCS_TARGET)
        
        if is_website_specific(rel_path):
            print(f"Preserved: {rel_path}")
            preserved_count += 1
            continue
            
        try:
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
            print(f"Deleted:   {rel_path}")
            deleted_count += 1
        except Exception as e:
            print(f"Error deleting {rel_path}: {e}")

    print(f"\nCleanup complete!")
    print(f"Deleted:   {deleted_count}")
    print(f"Preserved: {preserved_count}")

if __name__ == "__main__":
    clean_docs()
