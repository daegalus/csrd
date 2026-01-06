#!/usr/bin/env python3
"""
Convert parenthetical paragraphs to markdown alerts.
Finds paragraphs that start with '(' and end with ')' and converts them to:
> [!NOTE]
> Content ...
"""

import os
import re

CONTENT_DIR = '/var/home/yulian/workspace/code/frontend/csrd/content.en'

def convert_parentheticals(content):
    """Convert parenthetical paragraphs to markdown alerts."""
    
    # Pattern: Paragraph starting with ( and ending with )
    # We look for ( at start of line, content, ) at end of line (ignoring trailing whitespace)
    # The content shouldn't just be a short reference like "(see page 5)" but a substantial note
    # So we'll check length > 20 characters to avoid short clarifying parens
    
    # We use a loop to process the file line by line to better handle paragraph breaks
    lines = content.split('\n')
    new_lines = []
    
    in_code_block = False
    
    for line in lines:
        if line.strip().startswith('```') or line.strip().startswith('~~~'):
            in_code_block = not in_code_block
            new_lines.append(line)
            continue
            
        if in_code_block:
            new_lines.append(line)
            continue
            
        stripped = line.strip()
        
        # Check if it's a parenthetical paragraph
        # Must start with (, end with ), be > 20 chars long
        # And not be part of a list (e.g. "1. (Something)")
        if (stripped.startswith('(') and 
            stripped.endswith(')') and 
            len(stripped) > 20 and
            not line.lstrip().startswith(('1.', '-', '*'))):
            
            # Extract inner content
            inner = stripped[1:-1].strip()
            
            # Convert to alert
            new_lines.append(f'> [!NOTE]')
            new_lines.append(f'> {inner}')
        else:
            new_lines.append(line)
            
    return '\n'.join(new_lines)

def process_file(filepath):
    """Process a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = convert_parentheticals(content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    print("Converting parenthetical notes to markdown alerts...")
    print("=" * 60)
    
    count = 0
    for root, dirs, files in os.walk(CONTENT_DIR):
        for fname in files:
            if fname.endswith('.md'):
                filepath = os.path.join(root, fname)
                if process_file(filepath):
                    print(f"  ✅ Converted notes in: {fname}")
                    count += 1
    
    print("\n" + "=" * 60)
    print(f"CONVERSION COMPLETE: Modified {count} files")

if __name__ == "__main__":
    main()
