import os
import re

file_path = r"C:\MyBooks\LastQuietPlaceInAmerica1-Edited.md"
output_dir = r"C:\Users\bartt\.gemini\antigravity\scratch\LastQuietPlaceInAmerica"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Split by "# Chapter"
chapters = re.split(r'(?m)^# Chapter\s+', content)

print(f"Found {len(chapters) - 1} chapters.")

for i, chapter in enumerate(chapters):
    if i == 0:
        # This is the text before Chapter 1 (frontmatter or empty)
        if chapter.strip():
            with open(os.path.join(output_dir, "frontmatter.md"), 'w', encoding='utf-8') as f:
                f.write(chapter)
        continue
        
    # Get the chapter number and content
    lines = chapter.split('\n')
    title_line = lines[0].strip()
    
    # Extract number
    match = re.match(r'^(\d+)', title_line)
    if match:
        num = int(match.group(1))
        filename = f"chapter_{num:02d}.md"
    else:
        # Fallback to index
        filename = f"chapter_{i:02d}.md"
        
    # Reconstruct the content
    full_content = f"# Chapter {chapter}"
    
    with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
        f.write(full_content)
        
    print(f"Saved {filename}")
