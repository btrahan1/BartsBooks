import os

ch3_path = r"C:\Users\bartt\Projects\BartsBooks\books\ThirdPlaceTim_Book2\chapter_03.md"
notes_path = r"C:\Users\bartt\Projects\BartsBooks\books\ThirdPlaceTim_Book2\notes.md"

with open(ch3_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Lines 1 to 85 are the story
story_lines = lines[0:85]
# Lines 86 to end are the notes
note_lines = lines[85:]

# Overwrite chapter_03.md with just the story
with open(ch3_path, 'w', encoding='utf-8') as f:
    f.writelines(story_lines)

# Append notes to notes.md
with open(notes_path, 'a', encoding='utf-8') as f:
    f.write("\n\n# Additional Outlines & Notes\n\n")
    f.writelines(note_lines)

print("Cleaned up chapter_03.md and updated notes.md")
