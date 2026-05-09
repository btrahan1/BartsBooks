import os

file_path = r"C:\Users\bartt\.gemini\antigravity\scratch\TheUrbanRunner.md"
output_dir = r"C:\Users\bartt\.gemini\antigravity\scratch\TheUrbanRunner"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

scenes = [
    {"title": "The Urban Runner", "start": 1, "end": 142},
    {"title": "Camouflage and AI", "start": 147, "end": 249},
    {"title": "The Lion's Den", "start": 251, "end": 375},
    {"title": "The Heart of the Run", "start": 379, "end": 456},
    {"title": "Free to Fly", "start": 460, "end": 556},
    {"title": "The View from the Tree", "start": 560, "end": 634},
    {"title": "Play Your Game", "start": 638, "end": 717},
    {"title": "The War Room", "start": 720, "end": 803},
    {"title": "The Execution", "start": 807, "end": 887},
    {"title": "Upgrading the Team", "start": 890, "end": 987},
    {"title": "The Sacrifice", "start": 992, "end": 1077},
    {"title": "Running on 80 percent", "start": 1082, "end": 1146},
    {"title": "Win for Each Other", "start": 1151, "end": 1238},
    {"title": "The Shootout", "start": 1242, "end": 1321},
    {"title": "What Would Tyler Do", "start": 1325, "end": 1415},
    {"title": "A Borrowed Clarity", "start": 1418, "end": 1506},
    {"title": "The Cathedral of Sport", "start": 1507, "end": 1591},
    {"title": "The Yellow Beacon", "start": 1595, "end": 1675},
    {"title": "The Wall", "start": 1678, "end": 1763},
    {"title": "The Duel", "start": 1766, "end": 1854},
    {"title": "The Final Act", "start": 1857, "end": 1966},
    {"title": "Epilogue: LA Noodles", "start": 1970, "end": 2063}
]

chapter_num = 1
for scene in scenes:
    filename = f"chapter_{chapter_num:02d}.md"
    chapter_num += 1
    
    # Convert 1-based lines to 0-based indices
    start_idx = scene["start"] - 1
    end_idx = scene["end"]
    
    content = lines[start_idx:end_idx]
    
    # Add a title header
    full_content = f"# Chapter {chapter_num-1}: {scene['title']}\n\n" + "".join(content)
    
    with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
        f.write(full_content)
        
    print(f"Saved {filename}")

# Save the notes separately just in case
notes_lines = []
all_ranges = [(s["start"]-1, s["end"]) for s in scenes]
for idx, line in enumerate(lines):
    in_scene = False
    for r in all_ranges:
        if r[0] <= idx < r[1]:
            in_scene = True
            break
    if not in_scene and line.strip():
        notes_lines.append(line)

with open(os.path.join(output_dir, "notes.md"), 'w', encoding='utf-8') as f:
    f.writelines(notes_lines)
print("Saved notes.md")
