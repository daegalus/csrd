#!/usr/bin/env python3
"""
Content Formatting Script for CSRD - Phase 2
Converts ### creature headers to Hugo shortcode format.
"""

import os
import re

def convert_hash_headers_to_hugo(content):
    """Convert ### Name N (M) headers to Hugo columns2 shortcode."""
    
    # Pattern: ### Name N (M) or ### Name: Level N (M)
    # Handles special characters in name (like @), optional colon, optional 'Level' text
    pattern = r'^###\s+(.+?)(?::)?\s+(?:Level\s+)?(\d+)\s+\((\d+)\)\s*$'
    
    def replace_func(match):
        name = match.group(1).strip()
        level = match.group(2)
        difficulty = match.group(3)
        
        # If name is all CAPS, convert to Title Case (e.g. ANGEL OF THE APOCALYPSE -> Angel Of The Apocalypse)
        if name.isupper() and len(name) > 3:
            name = name.title()
            
        return f'{{{{< hint danger >}}}} {{{{< columns2 >}}}} {name} <---> {level} ({difficulty}) {{{{< /columns2 >}}}}{{{{< /hint >}}}}'
    
    content = re.sub(pattern, replace_func, content, flags=re.MULTILINE)
    
    return content

def format_inline_creatures(content):
    """Format inline creature entries like 'Bagheera: Description... Level N;'"""
    
    # Pattern for inline creature followed by description then level info
    # e.g., "Bagheera: This cunning... Level 7; stalking..."
    # These typically start a paragraph with Name: and have Level somewhere
    
    # First, bold the creature name at start of block
    pattern = r'^([A-Z][a-zA-Z\s\'\-,]+):\s+((?:This|These|A |An |The |Sometimes|Interacting|Smart)[^L]*)(Level\s+\d+)'
    
    def replace_func(match):
        name = match.group(1).strip()
        description = match.group(2)
        level = match.group(3)
        return f'**{name}:** {description}{level}'
    
    content = re.sub(pattern, replace_func, content, flags=re.MULTILINE)
    
    return content

def fix_merged_stat_lines(content):
    """Fix stat entries that got merged on one line."""
    
    # Pattern: "Environment: text Health: N"
    content = re.sub(
        r'(\*\*Environment:\*\*[^*\n]+)\s+Health:\s*(\d+)',
        r'\1\n\n**Health:** \2',
        content
    )
    
    # Pattern: "Modifications: text Combat:"
    content = re.sub(
        r'(\*\*Modifications:\*\*[^*\n]+)\s+Combat:',
        r'\1\n\n**Combat:**',
        content
    )
    
    return content

def process_file(filepath):
    """Process a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Apply formatting
    content = convert_hash_headers_to_hugo(content)
    content = format_inline_creatures(content)
    content = fix_merged_stat_lines(content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    content_dir = '/var/home/yulian/workspace/code/frontend/csrd/content.en'
    
    files_to_process = []
    
    # Focus on genre files where creatures are most common
    genres_dir = os.path.join(content_dir, '04-genres')
    gm_dir = os.path.join(content_dir, '05-game-mastering')
    
    for directory in [genres_dir, gm_dir]:
        if os.path.exists(directory):
            for fname in os.listdir(directory):
                if fname.endswith('.md'):
                    files_to_process.append(os.path.join(directory, fname))
    
    print(f"Processing {len(files_to_process)} files (Phase 2 - Hugo shortcode conversion)...")
    
    modified_count = 0
    for filepath in files_to_process:
        fname = os.path.basename(filepath)
        if process_file(filepath):
            print(f"  ✅ Modified: {fname}")
            modified_count += 1
        else:
            print(f"  ⏩ No changes: {fname}")
    
    print(f"\nSummary: {modified_count} files modified")

if __name__ == "__main__":
    main()
