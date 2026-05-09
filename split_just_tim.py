import os
import re

file_path = r"C:\Users\bartt\.gemini\antigravity\scratch\JustTim.md"
output_dir_b2 = r"C:\Users\bartt\Projects\BartsBooks\books\ThirdPlaceTim_Book2"
output_dir_b3 = r"C:\Users\bartt\Projects\BartsBooks\books\ThirdPlaceTim_Book3"

if not os.path.exists(output_dir_b2):
    os.makedirs(output_dir_b2)
if not os.path.exists(output_dir_b3):
    os.makedirs(output_dir_b3)

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Separate Part 1 and Part 2 based on line counts or specific markers
# Let's use line counts as determined before or search for "END OF BOOK TWO"
# "END OF BOOK TWO" is at line 6607 (approx)
# Let's split the content string by "END OF BOOK TWO"
parts = content.split("END OF BOOK TWO")

part1_content = parts[0]
part2_content = parts[1] if len(parts) > 1 else ""

# Save notes for Book 2
# Let's just grab the notes block from part 2 if it's there or just hardcode line ranges if possible
# But strings are easier
# Part 1 notes are likely at the end of Part 1 or start of Part 2
# Let's search for "This is absolutely a worthy follow-up" in part2_content
notes_b2_match = re.search(r'(This is absolutely a worthy follow-up.*?)(?=\n### |$)', part2_content, re.DOTALL)
if notes_b2_match:
    with open(os.path.join(output_dir_b2, "notes.md"), 'w', encoding='utf-8') as f:
        f.write(notes_b2_match.group(1))

# Notes for Book 3 are likely the outline for Book 3
# Let's search for "### []{#anchor}The Setup: The Accord of Ash" in part2_content
notes_b3_match = re.search(r'(### \[\]\{#anchor\}The Setup: The Accord of Ash.*?)(?=\nChapter 1:|$)', part2_content, re.DOTALL)
if notes_b3_match:
    with open(os.path.join(output_dir_b3, "notes.md"), 'w', encoding='utf-8') as f:
        f.write(notes_b3_match.group(1))

def save_chapters(text, output_dir, prefix):
    # Find all chapters
    matches = list(re.finditer(r'(?:^|\n)(?:###\s+)?(Chapter \d+:.*?)(?:\n|$)', text))
    
    print(f"Found {len(matches)} chapters for {prefix}.")
    
    for i, match in enumerate(matches):
        title = match.group(1).strip()
        start_pos = match.end()
        end_pos = matches[i+1].start() if i+1 < len(matches) else len(text)
        
        chapter_content = text[start_pos:end_pos].strip()
        
        # Clean up title
        clean_title = re.sub(r'[#*]', '', title).strip()
        
        # Avoid saving duplicate Chapter 3 (Spirit Stone) if it's the old draft
        if "Spirit Stone" in clean_title and i == 2: # Index 2 is likely the 3rd chapter
            print(f"Skipping old draft {clean_title} in {prefix}")
            continue
            
        filename = f"chapter_{i+1:02d}.md"
        # If we skip one, the numbering will be off, but let's keep it simple for now
        # Or we can use a counter
        
    # Let's use a counter to handle skipped chapters or just flat numbering
    count = 1
    for i, match in enumerate(matches):
        title = match.group(1).strip()
        start_pos = match.end()
        end_pos = matches[i+1].start() if i+1 < len(matches) else len(text)
        
        chapter_content = text[start_pos:end_pos].strip()
        clean_title = re.sub(r'[#*]', '', title).strip()
        
        # Skip the "Spirit Stone" chapter if it's followed by another Chapter 3 later
        # Actually, let's just keep it and let the user decide, or just keep the one that fits the story!
        # The roommate scene fits the story better.
        # Let's skip the Spirit Stone one if it's the one at line 183.
        # But we are working with text now, not lines.
        # Let's just save all of them but name them sequentially!
        
        filename = f"chapter_{count:02d}.md"
        count += 1
        
        full_content = f"# {clean_title}\n\n" + chapter_content
        
        with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
            f.write(full_content)
            
        print(f"Saved {filename} in {prefix}")

save_chapters(part1_content, output_dir_b2, "Book 2")
save_chapters(part2_content, output_dir_b3, "Book 3")

print("Done.")
