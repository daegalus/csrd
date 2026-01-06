#!/usr/bin/env python3
"""
Theme Update Script
Compares local hugo-book theme with upstream and reports differences.
"""

import os
import hashlib
import urllib.request
import zipfile
import tempfile
import shutil

LOCAL_THEME = '/var/home/yulian/workspace/code/frontend/csrd/themes/hugo-book'
UPSTREAM_URL = 'https://github.com/alex-shpak/hugo-book/archive/refs/heads/master.zip'

def get_file_hash(filepath):
    """Get MD5 hash of a file."""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def list_files(directory):
    """List all files in directory with relative paths."""
    files = {}
    for root, dirs, filenames in os.walk(directory):
        # Skip .git directories
        dirs[:] = [d for d in dirs if d != '.git']
        for fname in filenames:
            full_path = os.path.join(root, fname)
            rel_path = os.path.relpath(full_path, directory)
            files[rel_path] = get_file_hash(full_path)
    return files

def main():
    print("Theme Update Analysis")
    print("=" * 60)
    
    # List local files
    print("\n1. Scanning local theme files...")
    local_files = list_files(LOCAL_THEME)
    print(f"   Found {len(local_files)} files in local theme")
    
    # Download and extract upstream
    print("\n2. Downloading upstream theme...")
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, 'theme.zip')
            extract_dir = os.path.join(tmpdir, 'extracted')
            
            # Download
            urllib.request.urlretrieve(UPSTREAM_URL, zip_path)
            print("   Download complete")
            
            # Extract
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(extract_dir)
            
            # Find the extracted folder (usually hugo-book-master)
            extracted_folders = os.listdir(extract_dir)
            if extracted_folders:
                upstream_dir = os.path.join(extract_dir, extracted_folders[0])
            else:
                print("   ERROR: No folder found in zip")
                return
            
            print(f"   Extracted to: {extracted_folders[0]}")
            
            # List upstream files
            print("\n3. Scanning upstream theme files...")
            upstream_files = list_files(upstream_dir)
            print(f"   Found {len(upstream_files)} files in upstream theme")
            
            # Compare
            print("\n4. Comparing themes...")
            
            only_local = []
            only_upstream = []
            modified = []
            
            all_files = set(local_files.keys()) | set(upstream_files.keys())
            
            for f in sorted(all_files):
                local_hash = local_files.get(f)
                upstream_hash = upstream_files.get(f)
                
                if local_hash and not upstream_hash:
                    only_local.append(f)
                elif upstream_hash and not local_hash:
                    only_upstream.append(f)
                elif local_hash != upstream_hash:
                    modified.append(f)
            
            # Report
            print("\n" + "=" * 60)
            print("COMPARISON RESULTS")
            print("=" * 60)
            
            print(f"\n✅ Files in sync: {len(all_files) - len(only_local) - len(only_upstream) - len(modified)}")
            
            if only_local:
                print(f"\n📁 Files only in LOCAL ({len(only_local)}):")
                for f in only_local[:20]:
                    print(f"   + {f}")
                if len(only_local) > 20:
                    print(f"   ... and {len(only_local) - 20} more")
            
            if only_upstream:
                print(f"\n📥 Files only in UPSTREAM (new) ({len(only_upstream)}):")
                for f in only_upstream[:20]:
                    print(f"   ↓ {f}")
                if len(only_upstream) > 20:
                    print(f"   ... and {len(only_upstream) - 20} more")
            
            if modified:
                print(f"\n🔄 Files MODIFIED locally ({len(modified)}):")
                for f in modified[:30]:
                    print(f"   ~ {f}")
                if len(modified) > 30:
                    print(f"   ... and {len(modified) - 30} more")
            
            # Save upstream for potential update
            if only_upstream or modified:
                backup_path = '/tmp/hugo-book-upstream'
                if os.path.exists(backup_path):
                    shutil.rmtree(backup_path)
                shutil.copytree(upstream_dir, backup_path)
                print(f"\n📦 Upstream theme saved to: {backup_path}")
                print("   You can manually copy files from there to update.")
            
    except Exception as e:
        print(f"   ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
