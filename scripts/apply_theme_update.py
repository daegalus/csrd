#!/usr/bin/env python3
"""
Theme Selective Update Script
Updates theme files from upstream while preserving custom modifications.
"""

import os
import shutil

UPSTREAM = '/tmp/hugo-book-upstream'
LOCAL = '/var/home/yulian/workspace/code/frontend/csrd/themes/hugo-book'

# Files/folders to PRESERVE (not overwrite from upstream)
PRESERVE = [
    'assets/_custom.scss',
    'assets/_variables.scss',
    'assets/themes/',  # Custom theme files
    'layouts/_default/',  # Custom layouts
    'layouts/partials/docs/',  # Custom partials
    'layouts/shortcodes/',  # Custom shortcodes likely modified
]

# Folders to SKIP from upstream (not needed)
SKIP_UPSTREAM = [
    'exampleSite/',
    '.github/',
    'images/',
]

def should_preserve(rel_path):
    """Check if a file should be preserved."""
    for p in PRESERVE:
        if rel_path.startswith(p):
            return True
    return False

def should_skip(rel_path):
    """Check if upstream file should be skipped."""
    for p in SKIP_UPSTREAM:
        if rel_path.startswith(p):
            return True
    return False

def main():
    if not os.path.exists(UPSTREAM):
        print("ERROR: Upstream theme not found at", UPSTREAM)
        print("Run update_theme.py first to download it.")
        return
    
    print("Selective Theme Update")
    print("=" * 60)
    print(f"Upstream: {UPSTREAM}")
    print(f"Local: {LOCAL}")
    print()
    
    updated = []
    skipped_preserve = []
    skipped_upstream = []
    added = []
    
    # Walk upstream files
    for root, dirs, files in os.walk(UPSTREAM):
        # Skip .git
        dirs[:] = [d for d in dirs if d != '.git']
        
        for fname in files:
            upstream_path = os.path.join(root, fname)
            rel_path = os.path.relpath(upstream_path, UPSTREAM)
            local_path = os.path.join(LOCAL, rel_path)
            
            # Skip unwanted upstream folders
            if should_skip(rel_path):
                skipped_upstream.append(rel_path)
                continue
            
            # Preserve local customizations
            if should_preserve(rel_path):
                skipped_preserve.append(rel_path)
                continue
            
            # Copy/update file
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            if os.path.exists(local_path):
                # Compare before updating
                with open(upstream_path, 'rb') as f:
                    upstream_content = f.read()
                with open(local_path, 'rb') as f:
                    local_content = f.read()
                
                if upstream_content != local_content:
                    shutil.copy2(upstream_path, local_path)
                    updated.append(rel_path)
            else:
                shutil.copy2(upstream_path, local_path)
                added.append(rel_path)
    
    # Report
    print("=" * 60)
    print("UPDATE COMPLETE")
    print("=" * 60)
    
    print(f"\n✅ Updated: {len(updated)} files")
    for f in updated[:20]:
        print(f"   ~ {f}")
    if len(updated) > 20:
        print(f"   ... and {len(updated) - 20} more")
    
    print(f"\n➕ Added: {len(added)} files")
    for f in added[:20]:
        print(f"   + {f}")
    if len(added) > 20:
        print(f"   ... and {len(added) - 20} more")
    
    print(f"\n🔒 Preserved (local customizations): {len(skipped_preserve)} files")
    for f in skipped_preserve[:10]:
        print(f"   # {f}")
    if len(skipped_preserve) > 10:
        print(f"   ... and {len(skipped_preserve) - 10} more")
    
    print(f"\n⏭️  Skipped (not needed): {len(skipped_upstream)} files")

if __name__ == "__main__":
    main()
