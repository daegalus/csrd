#!/usr/bin/env python3
"""
Systematic Content Verification Script
Compares source content (cypher-new.md) against extracted target files
to identify any missing text content.
"""

import os
import re
from collections import defaultdict

SOURCE_FILE = '/var/home/yulian/workspace/code/frontend/csrd/srds/cypher-new.md'
CONTENT_DIR = '/var/home/yulian/workspace/code/frontend/csrd/content.en'

def normalize_text(text):
    """Normalize text for comparison - remove formatting, extra whitespace, case"""
    # Remove markdown formatting
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*([^*]+)\*', r'\1', text)  # Italic
    text = re.sub(r'`([^`]+)`', r'\1', text)  # Code
    text = re.sub(r'{{<[^>]+>}}', '', text)  # Hugo shortcodes
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)  # Headers
    text = re.sub(r'\|', ' ', text)  # Table pipes
    text = re.sub(r'-{3,}', '', text)  # Horizontal rules
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    return text.lower().strip()

def extract_sentences(text, min_length=50):
    """Extract sentences/phrases of significant length for matching"""
    # Split on sentence boundaries
    sentences = re.split(r'[.!?]\s+', text)
    # Filter to meaningful length
    return [s.strip() for s in sentences if len(s.strip()) >= min_length]

def load_file(filepath):
    """Load file content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def get_all_target_content():
    """Load all content from target directory"""
    all_content = []
    for root, dirs, files in os.walk(CONTENT_DIR):
        for fname in files:
            if fname.endswith('.md'):
                filepath = os.path.join(root, fname)
                content = load_file(filepath)
                all_content.append((filepath, normalize_text(content)))
    return all_content

def find_section_in_source(source_lines, section_name):
    """Find line range for a section in source"""
    start_idx = None
    for i, line in enumerate(source_lines):
        if section_name.upper() in line.upper():
            start_idx = i
            break
    return start_idx

def check_content_coverage():
    """Main verification function"""
    print("Loading source file...")
    source_content = load_file(SOURCE_FILE)
    source_lines = source_content.split('\n')
    
    print("Loading target files...")
    targets = get_all_target_content()
    all_target_text = ' '.join([t[1] for t in targets])
    
    print(f"Source: {len(source_lines)} lines")
    print(f"Targets: {len(targets)} files")
    print()
    
    # Key sections to verify
    sections = [
        ("HOW TO PLAY THE CYPHER SYSTEM", 0, 400),
        ("WARRIOR", 436, 700),
        ("ADEPT", 668, 900),
        ("EXPLORER", 889, 1150),
        ("SPEAKER", 1144, 1400),
        ("FLAVOR", 1400, 1800),
        ("DESCRIPTOR", 1800, 4500),
        ("FOCUS", 4500, 14600),
        ("ABILITIES", 14600, 14700),  # Just check header presence
        ("RULES OF THE GAME", None, None),
        ("FANTASY", 14600, 15500),
        ("MODERN", 15500, 16000),
        ("SCIENCE FICTION", 16000, 18000),
        ("HORROR", 24700, 26100),
        ("SUPERHERO", 19900, 20400),
        ("POST-APOCALYPTIC", 48544, 49200),
        ("FAIRY TALE", 20400, 24700),
        ("WEIRD WEST", 45241, 46050),
        ("HISTORICAL", 26640, 26700),
    ]
    
    results = []
    
    for section_name, approx_start, approx_end in sections:
        print(f"Checking: {section_name}...")
        
        # Find actual section start
        actual_start = find_section_in_source(source_lines, section_name)
        if actual_start is None:
            results.append((section_name, "NOT FOUND IN SOURCE", 0))
            continue
        
        # Sample some sentences from the section
        if approx_end:
            section_text = '\n'.join(source_lines[actual_start:min(actual_start+500, approx_end)])
        else:
            section_text = '\n'.join(source_lines[actual_start:actual_start+300])
        
        normalized_section = normalize_text(section_text)
        sample_sentences = extract_sentences(normalized_section, min_length=40)[:10]
        
        if not sample_sentences:
            results.append((section_name, "NO SAMPLE SENTENCES", 0))
            continue
        
        # Check how many sample sentences are found in targets
        found_count = 0
        missing_samples = []
        for sentence in sample_sentences:
            if sentence in all_target_text:
                found_count += 1
            else:
                # Try partial match (first 60 chars)
                partial = sentence[:60]
                if partial in all_target_text:
                    found_count += 1
                else:
                    missing_samples.append(sentence[:80] + "...")
        
        coverage = (found_count / len(sample_sentences)) * 100 if sample_sentences else 0
        results.append((section_name, f"{coverage:.0f}% ({found_count}/{len(sample_sentences)})", coverage, missing_samples[:3]))
    
    # Print results
    print("\n" + "="*70)
    print("CONTENT COVERAGE REPORT")
    print("="*70)
    
    for result in results:
        section = result[0]
        status = result[1]
        coverage = result[2] if len(result) > 2 else 0
        
        if coverage >= 80:
            indicator = "✅"
        elif coverage >= 50:
            indicator = "⚠️"
        else:
            indicator = "❌"
        
        print(f"{indicator} {section:30} {status}")
        
        # Show missing samples for low coverage
        if len(result) > 3 and result[3] and coverage < 80:
            print(f"   Missing samples:")
            for sample in result[3]:
                print(f"   - {sample}")
    
    print("\n" + "="*70)
    print("Legend: ✅ >= 80% | ⚠️ 50-79% | ❌ < 50%")
    print("="*70)

if __name__ == "__main__":
    check_content_coverage()
