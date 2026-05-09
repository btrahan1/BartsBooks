import os

file_path = r"C:\Users\bartt\.gemini\antigravity\scratch\TheNemoProtocol.md"
output_dir = r"C:\Users\bartt\.gemini\antigravity\scratch\TheNemoProtocol"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

scenes = [
    {"title": "The Sandbox", "start": 5, "end": 141},
    {"title": "The Dust and the Dashing", "start": 142, "end": 265},
    {"title": "The Hexagon", "start": 266, "end": 404},
    {"title": "The Art of the Deal", "start": 405, "end": 517},
    {"title": "Ghosts in the Water", "start": 518, "end": 597},
    {"title": "The Taboo Breaker", "start": 598, "end": 703},
    {"title": "The Second Sun", "start": 704, "end": 802},
    {"title": "The Table of Silence", "start": 853, "end": 904},
    {"title": "The Tiger's Path", "start": 905, "end": 960},
    {"title": "The Bedtime Story", "start": 961, "end": 1061},
    {"title": "The Switzerland Protocol", "start": 1062, "end": 1182},
    {"title": "Level Three", "start": 1183, "end": 1281},
    {"title": "The Hexagon Army", "start": 1282, "end": 1440},
    {"title": "The Bailout of the People", "start": 1441, "end": 1595},
    {"title": "Scorched Earth and Green Shoots", "start": 1596, "end": 1710},
    {"title": "The Ghost in the Fjord", "start": 1711, "end": 1826},
    {"title": "The Arnaud Option", "start": 1827, "end": 1939},
    {"title": "The Black Blood", "start": 1940, "end": 2046},
    {"title": "The Rainmaker", "start": 2047, "end": 2149},
    {"title": "The Parting of the Fences", "start": 2150, "end": 2247},
    {"title": "The Great Migration", "start": 2248, "end": 2304},
    {"title": "The Sound of Water", "start": 2305, "end": 2367},
    {"title": "The Last Coordinate", "start": 2368, "end": 2431},
    {"title": "The Golden Cage", "start": 2432, "end": 2593}
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
notes_lines = lines[802:852] # Lines 803 to 852
with open(os.path.join(output_dir, "notes.md"), 'w', encoding='utf-8') as f:
    f.writelines(notes_lines)
print("Saved notes.md")
