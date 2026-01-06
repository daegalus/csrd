
import os
import re

target_file = '/var/home/yulian/workspace/code/frontend/csrd/content.en/04-genres/10-weird-west.md'
temp_file_1 = '/var/home/yulian/workspace/code/frontend/csrd/temp_ww_creatures_1.md'
temp_file_2 = '/var/home/yulian/workspace/code/frontend/csrd/temp_ww_creatures_2.md'

def format_line(line):
    line = line.strip()
    if not line:
        return ""
    
    # NPC Header: ALCHEMIST 5 (15)
    match_npc = re.match(r'^([A-Z ]+) (\d+) \((\d+)\)$', line)
    if match_npc:
        name = match_npc.group(1).title()
        return f"#### {name} {match_npc.group(2)} ({match_npc.group(3)})"

    # Section Headers: ANIMALS, NPCs
    # But exclude the main title if it appears
    if line == "CREATURES AND NPCs OF THE WEIRD WEST":
        return "## Creatures and NPCs of the Weird West"
    
    if re.match(r'^[A-Z ]+$', line) and len(line) < 50:
        return f"### {line.title()}"
        
    # Creature Entry: Name: Stats
    # e.g., Bat: level 1
    if re.match(r'^[^:]+: level \d+', line, re.IGNORECASE):
        # Bold the name part
        return re.sub(r'^([^:]+):', r'**\1:**', line)
    
    # Just return line
    return line

def get_content():
    content = []
    
    # Process temp 1
    with open(temp_file_1, 'r') as f:
        lines = f.readlines()
        # Skip the first line if it's the main header (we handle it or insert our own)
        # The first line is "CREATURES AND NPCs OF THE WEIRD WEST"
        # We will keep it but format it.
        for line in lines:
            formatted = format_line(line)
            if formatted:
                content.append(formatted)
            elif line.strip() == "":
                content.append("")

    # Process temp 2 (lines 1-69)
    with open(temp_file_2, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i >= 69: # Stop before Artifacts
                break
            formatted = format_line(line)
            if formatted:
                content.append(formatted)
            elif line.strip() == "":
                content.append("")
                
    return content

def main():
    with open(target_file, 'r') as f:
        target_lines = f.readlines()
        
    # Find insertion point
    insert_idx = -1
    for i, line in enumerate(target_lines):
        if "### Weird West Artifacts" in line:
            insert_idx = i
            break
            
    if insert_idx == -1:
        print("Could not find ### Weird West Artifacts")
        return

    new_content = get_content()
    
    # Add some spacing
    final_lines = target_lines[:insert_idx] + ["\n"] + [l + "\n" for l in new_content] + ["\n"] + target_lines[insert_idx:]
    
    with open(target_file, 'w') as f:
        f.writelines(final_lines)
    
    print(f"Inserted {len(new_content)} lines into {target_file}")

if __name__ == "__main__":
    main()
