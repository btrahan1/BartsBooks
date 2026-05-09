import os
import re

file_path = r"C:\Users\bartt\.gemini\antigravity\scratch\ThirdPlaceTim.md"
output_dir = r"C:\Users\bartt\Projects\BartsBooks\books\ThirdPlaceTim"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Split by chapter headers
# Matches "### **Chapter N: ..." or "**Chapter N: ..."
chapters = re.split(r'(?:###\s+)?\*\*Chapter \d+:.*?\*\*', content)
titles = re.findall(r'(?:###\s+)?\*\*Chapter \d+:.*?\*\*', content)

# The first element in chapters might be empty or header before Chapter 1
# Let's check
if len(chapters) > 0 and len(chapters[0].strip()) == 0:
    chapters = chapters[1:]

print(f"Found {len(chapters)} chapters.")

for i, chapter_content in enumerate(chapters):
    filename = f"chapter_{i+1:02d}.md"
    title = titles[i] if i < len(titles) else f"Chapter {i+1}"
    
    # Clean up title for header
    clean_title = re.sub(r'[#*]', '', title).strip()
    
    full_content = f"# {clean_title}\n\n" + chapter_content.strip()
    
    with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
        f.write(full_content)
        
    print(f"Saved {filename}")

print("Done.")
