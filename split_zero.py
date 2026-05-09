import os

file_path = r"C:\Users\bartt\.gemini\antigravity\scratch\Zero.md"
output_dir = r"C:\Users\bartt\.gemini\antigravity\scratch\Zero"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

scenes = [
    {"title": "The Adjustment", "start": 5, "end": 202},
    {"title": "The Freeze", "start": 203, "end": 362},
    {"title": "The Run", "start": 363, "end": 529},
    {"title": "The Exodus", "start": 530, "end": 684},
    {"title": "The Paper Chase", "start": 685, "end": 938},
    {"title": "The Lecture", "start": 939, "end": 1078},
    {"title": "The Restoration", "start": 1079, "end": 1234}
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

print("Done.")
