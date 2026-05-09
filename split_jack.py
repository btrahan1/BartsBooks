import os

file_path = r"C:\Users\bartt\.gemini\antigravity\scratch\JackOfAllTrades.md"
output_dir = r"C:\Users\bartt\.gemini\antigravity\scratch\JackOfAllTrades"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

scenes = [
    {"title": "The Man About Town", "start": 1},
    {"title": "Send Jack to Work", "start": 148},
    {"title": "Time and Again", "start": 270},
    {"title": "The Silver Cue", "start": 363},
    {"title": "Home Office and Piano", "start": 675},
    {"title": "Brainstorming", "start": 842, "is_notes": True},
    {"title": "Patties Place", "start": 936},
    {"title": "Miller Dynamics", "start": 1069},
    {"title": "The Factory Floor", "start": 1173},
    {"title": "Breakroom Pizza", "start": 1347},
    {"title": "The Monster Problem", "start": 1486}
]

# Convert 1-based lines to 0-based indices
for scene in scenes:
    scene["start_idx"] = scene["start"] - 1

# Add end indices
for i in range(len(scenes) - 1):
    scenes[i]["end_idx"] = scenes[i+1]["start_idx"]
scenes[-1]["end_idx"] = len(lines)

chapter_num = 1
for scene in scenes:
    if scene.get("is_notes"):
        # Save notes separately
        with open(os.path.join(output_dir, "notes.md"), 'w', encoding='utf-8') as f:
            f.writelines(lines[scene["start_idx"]:scene["end_idx"]])
        continue
        
    filename = f"chapter_{chapter_num:02d}.md"
    chapter_num += 1
    
    content = lines[scene["start_idx"]:scene["end_idx"]]
    
    # Add a title header
    full_content = f"# Chapter {chapter_num-1}: {scene['title']}\n\n" + "".join(content)
    
    with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
        f.write(full_content)
        
    print(f"Saved {filename}")
