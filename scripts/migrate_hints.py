#!/usr/bin/env python3
"""
Migrate hint shortcodes to GitHub-style markdown alerts.
{{< hint info >}} ... {{< /hint >}} → > [!NOTE]
{{< hint warning >}} ... {{< /hint >}} → > [!WARNING]
Skips {{< hint danger >}} as those are used for creature headers.
"""

import os
import re

CONTENT_DIR = '/var/home/yulian/workspace/code/frontend/csrd/content.en'

# Mapping of hint types to markdown alert types
HINT_MAP = {
    'info': 'NOTE',
    'warning': 'WARNING',
}

def convert_hint_to_alert(content):
    """Convert hint shortcodes to markdown alerts."""
    
    modified = False
    
    for hint_type, alert_type in HINT_MAP.items():
        # Pattern: {{< hint TYPE >}} content {{< /hint >}}
        # Can be single-line or multi-line
        pattern = r'\{\{<\s*hint\s+' + hint_type + r'\s*>\}\}\s*(.*?)\s*\{\{<\s*/hint\s*>\}\}'
        
        def replace_func(match):
            inner = match.group(1).strip()
            # Convert inner content to blockquote format
            lines = inner.split('\n')
            # Add > prefix to each line
            alert_lines = [f'> [!{alert_type}]']
            for line in lines:
                # Remove excessive whitespace but keep content
                cleaned = line.strip()
                if cleaned:
                    alert_lines.append(f'> {cleaned}')
                else:
                    alert_lines.append('>')
            return '\n'.join(alert_lines)
        
        new_content = re.sub(pattern, replace_func, content, flags=re.DOTALL)
        if new_content != content:
            modified = True
            content = new_content
    
    return content, modified

def process_file(filepath):
    """Process a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content, modified = convert_hint_to_alert(content)
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    print("Migrating hint shortcodes to markdown alerts...")
    print("=" * 60)
    
    files_modified = 0
    hints_converted = 0
    
    for root, dirs, files in os.walk(CONTENT_DIR):
        for fname in files:
            if fname.endswith('.md'):
                filepath = os.path.join(root, fname)
                
                # Count hints before
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                info_count = len(re.findall(r'\{\{<\s*hint\s+info\s*>\}\}', content))
                warning_count = len(re.findall(r'\{\{<\s*hint\s+warning\s*>\}\}', content))
                
                if info_count > 0 or warning_count > 0:
                    if process_file(filepath):
                        rel_path = os.path.relpath(filepath, CONTENT_DIR)
                        print(f"  ✅ {rel_path}: {info_count} info, {warning_count} warning")
                        files_modified += 1
                        hints_converted += info_count + warning_count
    
    print("\n" + "=" * 60)
    print(f"MIGRATION COMPLETE")
    print(f"  Files modified: {files_modified}")
    print(f"  Hints converted: {hints_converted}")
    print("\nNote: {{< hint danger >}} shortcodes preserved for creature headers.")

if __name__ == "__main__":
    main()
