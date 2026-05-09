import os

file_path = r"C:\Users\bartt\.gemini\antigravity\scratch\Rook2.md"
output_dir = r"C:\Users\bartt\.gemini\antigravity\scratch\Rook2_split"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Extract notes (Lines 528 to 756, 1-based)
notes_content = lines[527:756]
with open(os.path.join(output_dir, "notes.md"), 'w', encoding='utf-8') as f:
    f.writelines(notes_content)
print("Saved notes.md")

# Define chapters (title, start line, end line)
chapters = [
    {"title": "The Third Rock", "start": 5, "end": 527},
    {"title": "The Portal", "start": 757, "end": 1100},
    {"title": "The Plateau", "start": 1101, "end": 1224},
    {"title": "The Signal", "start": 1225, "end": 1455},
    {"title": "The Command Center", "start": 1456, "end": 1612},
    {"title": "The Survivors", "start": 1613, "end": 1867},
    {"title": "The Rescue", "start": 1868, "end": 1987},
    {"title": "The Debriefing", "start": 1988, "end": 2263},
    {"title": "The King", "start": 2264, "end": 2326},
    {"title": "The Declaration", "start": 2327, "end": 2399},
    {"title": "The Countdown", "start": 2400, "end": 2475},
    {"title": "The Last Laugh", "start": 2476, "end": 2542}
]

chapter_num = 1
for ch in chapters:
    filename = f"chapter_{chapter_num:02d}.md"
    chapter_num += 1
    
    start_idx = ch["start"] - 1
    end_idx = ch["end"]
    
    content = lines[start_idx:end_idx]
            
    # Add a title header
    full_content = f"# Chapter {chapter_num-1}: {ch['title']}\n\n" + "".join(content)
    
    with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
        f.write(full_content)
        
    print(f"Saved {filename}")

print("Done.")
