import os
import re

file_path = r"C:\Users\bartt\.gemini\antigravity\scratch\LevelOneLeon.md"
output_dir = r"C:\Users\bartt\Projects\BartsBooks\books\LevelOneLeon"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all chapters
# Pattern matches "Chapter Word:" or "Chapter Word-Word:"
matches = list(re.finditer(r'(?:^|\n)(Chapter [A-Za-z-]+:.*?)(?:\n|$)', content))

print(f"Found {len(matches)} chapters.")

# Extract notes (lines before Chapter One or specific blocks)
# Let's search for the "Thoughts on Punching Up" block
notes_match = re.search(r'(### \[\]\{#anchor\}Thoughts on "Punching Up".*?)(?=\nChapter |$)', content, re.DOTALL)
notes_content = ""
if notes_match:
    notes_content += notes_match.group(1) + "\n\n"

# Also look for other "###" blocks
other_notes = re.findall(r'(### \[\]\{#anchor\}.*?)(?=\nChapter |$)', content, re.DOTALL)
for note in other_notes:
    if "Thoughts on \"Punching Up\"" not in note:
        notes_content += note + "\n\n"

if notes_content:
    with open(os.path.join(output_dir, "notes.md"), 'w', encoding='utf-8') as f:
        f.write(notes_content)
    print("Saved notes.md")

# Save chapters
for i, match in enumerate(matches):
    title = match.group(1).strip()
    start_pos = match.end()
    end_pos = matches[i+1].start() if i+1 < len(matches) else len(content)
    
    chapter_content = content[start_pos:end_pos].strip()
    
    # Clean up conversational bits before the chapter if any
    # Usually they are before the match, but sometimes inside if the match is just the title!
    # In this file, the conversational bits seem to be BEFORE the chapter match!
    # E.g. "Here is Chapter Two..." is before "Chapter Two: Hazard Removal".
    # So the chapter_content should be clean!
    
    filename = f"chapter_{i+1:02d}.md"
    
    # Clean up title for file content
    clean_title = re.sub(r'[#*]', '', title).strip()
    
    full_content = f"# {clean_title}\n\n" + chapter_content
    
    with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
        f.write(full_content)
        
    print(f"Saved {filename}")

print("Done.")
