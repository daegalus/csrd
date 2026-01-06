#!/usr/bin/env python3
"""
Systematic Section Verification Script
Checks that all major sections from source exist in target files.
"""

import os
import re

SOURCE_FILE = '/var/home/yulian/workspace/code/frontend/csrd/srds/cypher-new.md'
CONTENT_DIR = '/var/home/yulian/workspace/code/frontend/csrd/content.en'

def load_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def get_all_target_content():
    """Load all content from target directory into single string"""
    all_content = ""
    for root, dirs, files in os.walk(CONTENT_DIR):
        for fname in files:
            if fname.endswith('.md'):
                filepath = os.path.join(root, fname)
                content = load_file(filepath)
                all_content += content + "\n"
    return all_content.lower()

def find_all_caps_headers(source):
    """Find major section headers (ALL CAPS lines)"""
    headers = []
    lines = source.split('\n')
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Match ALL CAPS headers that are likely section titles
        if (stripped and 
            len(stripped) > 5 and 
            len(stripped) < 80 and
            stripped.isupper() and 
            not stripped.startswith('|') and
            not stripped.startswith('-') and
            '.' not in stripped and
            ':' not in stripped):
            headers.append((i+1, stripped))
    return headers

def check_section_exists(section_name, target_content):
    """Check if a section exists in target content"""
    # Normalize to lowercase, title case variations
    normalized = section_name.lower()
    # Check for presence
    if normalized in target_content:
        return True
    # Try title case
    title_case = section_name.title().lower()
    if title_case in target_content:
        return True
    # Try with common prefixes removed
    for prefix in ['optional rule:', 'optional rules:', 'optional rules for']:
        if normalized.startswith(prefix):
            remainder = normalized[len(prefix):].strip()
            if remainder in target_content:
                return True
    return False

def main():
    print("Loading source file...")
    source = load_file(SOURCE_FILE)
    
    print("Loading target files...")
    target = get_all_target_content()
    
    print("Finding major section headers...")
    headers = find_all_caps_headers(source)
    print(f"Found {len(headers)} potential section headers")
    
    # Check each header
    found = []
    missing = []
    
    for line_num, header in headers:
        if check_section_exists(header, target):
            found.append((line_num, header))
        else:
            missing.append((line_num, header))
    
    # Report
    print("\n" + "="*70)
    print("SECTION VERIFICATION REPORT")
    print("="*70)
    print(f"\n✅ Found sections: {len(found)}")
    print(f"❌ Potentially missing sections: {len(missing)}")
    
    if missing:
        print("\n" + "-"*70)
        print("POTENTIALLY MISSING SECTIONS (may need manual verification):")
        print("-"*70)
        for line_num, header in missing[:50]:  # Limit output
            print(f"  Line {line_num:5}: {header}")
        if len(missing) > 50:
            print(f"  ... and {len(missing) - 50} more")
    
    # Categorize missing by type
    print("\n" + "-"*70)
    print("MISSING SECTIONS BY CATEGORY:")
    print("-"*70)
    
    categories = {
        'Character Options': [],
        'Creatures/NPCs': [],
        'Abilities': [],
        'Cyphers/Artifacts': [],
        'Equipment': [],
        'Rules': [],
        'Other': []
    }
    
    for line_num, header in missing:
        h = header.lower()
        if 'character' in h or 'descriptor' in h or 'type' in h or 'focus' in h:
            categories['Character Options'].append((line_num, header))
        elif 'creature' in h or 'npc' in h or 'beast' in h:
            categories['Creatures/NPCs'].append((line_num, header))
        elif 'ability' in h or 'abilities' in h or 'skill' in h:
            categories['Abilities'].append((line_num, header))
        elif 'cypher' in h or 'artifact' in h:
            categories['Cyphers/Artifacts'].append((line_num, header))
        elif 'equipment' in h or 'weapon' in h or 'armor' in h or 'item' in h:
            categories['Equipment'].append((line_num, header))
        elif 'rule' in h or 'optional' in h or 'mode' in h:
            categories['Rules'].append((line_num, header))
        else:
            categories['Other'].append((line_num, header))
    
    for cat, items in categories.items():
        if items:
            print(f"\n{cat}: {len(items)} missing")
            for line_num, header in items[:10]:
                print(f"    Line {line_num}: {header}")
            if len(items) > 10:
                print(f"    ... and {len(items) - 10} more")

if __name__ == "__main__":
    main()
