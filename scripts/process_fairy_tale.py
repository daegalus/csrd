
import os

source_file = '/var/home/yulian/workspace/code/frontend/csrd/srds/cypher-new.md'
target_file = '/var/home/yulian/workspace/code/frontend/csrd/content.en/04-genres/08-fairy-tale.md'

# Block A: Intro, Basic Creatures (26574 - 26657)
block_a_start = 26574
block_a_end = 26657

# Block B: Rules, Cyphers, Artifacts, Creatures (20817 - 24730)
block_b_start = 20817
block_b_end = 24730

# Block C: Character Options (Descriptors, Foci) (47784 - 48543)
block_c_start = 47784
block_c_end = 48543

def extract_lines(filepath, start, end):
    with open(filepath, 'r') as f:
        all_lines = f.readlines()
        return all_lines[start-1:end]

block_a = extract_lines(source_file, block_a_start, block_a_end)
block_b = extract_lines(source_file, block_b_start, block_b_end)
block_c = extract_lines(source_file, block_c_start, block_c_end)

header = """---
title: Fairy Tale
weight: 8
description: The genre of fairy tales is a wide one, crossing into almost every culture and encompassing everything from early oral stories passed down from generation to generation to the more modern literary fairy tale.
---

# Fairy Tale

"""

final_content = [header] 

# Block A (Skip title if present)
if block_a[0].strip().lower() == "fairy tale":
    final_content.extend(block_a[1:])
else:
    final_content.extend(block_a)

final_content.append("\n\n")

# Block C (Character Options) - Placing it before general rules/creatures seems more logical for a chapter layout
# Intro -> Options -> Mechanics/Creatures
final_content.extend(block_c)

final_content.append("\n\n")

# Block B (Mechanics, Cyphers, Artifacts, Creatures)
final_content.extend(block_b)

with open(target_file, 'w') as f:
    f.writelines(final_content)

print(f"Successfully constructed {target_file} with {len(final_content)} lines.")
