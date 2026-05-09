import os

file_path = r"C:\Users\bartt\.gemini\antigravity\scratch\TheBookKeeper2.md"
output_dir = r"C:\Users\bartt\.gemini\antigravity\scratch\TheBookKeeper"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Define note ranges to extract (1-based lines)
note_ranges = [
    (143, 149), (290, 295), (417, 419), (576, 582), (652, 658),
    (755, 761), (838, 869), (955, 959), (1051, 1054), (1162, 1166),
    (1268, 1270), (1354, 1358), (1441, 1444), (1545, 1549), (1628, 1633),
    (1721, 1724), (1796, 1800), (1894, 1897), (1984, 1988), (2053, 2057),
    (2132, 2138), (2223, 2224), (2259, 2263), (2360, 2365), (2417, 2455),
    (2530, 2534), (2595, 2599), (2695, 2699), (2755, 2760)
]

# Convert to 0-based indices
notes_indices = []
for start, end in note_ranges:
    notes_indices.extend(range(start - 1, end))

# Extract notes
notes_content = []
for idx in sorted(set(notes_indices)):
    if idx < len(lines):
        notes_content.append(lines[idx])

with open(os.path.join(output_dir, "notes.md"), 'w', encoding='utf-8') as f:
    f.writelines(notes_content)
print("Saved notes.md")

# Define chapters (title, start line, end line)
# We will exclude the lines that are in notes_indices
chapters = [
    {"title": "The Signal and the Noise", "start": 7, "end": 142},
    {"title": "A Parasite's Game", "start": 150, "end": 289},
    {"title": "The Physics of Chance", "start": 296, "end": 416},
    {"title": "The House Edge", "start": 420, "end": 651}, # Spans across a note block
    {"title": "The Final Tally", "start": 659, "end": 754},
    {"title": "A New Set of Variables", "start": 762, "end": 837},
    {"title": "Calculating the Margins of a New Life", "start": 870, "end": 954},
    {"title": "The Aberration", "start": 960, "end": 1050},
    {"title": "The Keeper of the Pages", "start": 1055, "end": 1161},
    {"title": "The Unaccounted Variable", "start": 1167, "end": 1267},
    {"title": "A New Chapter", "start": 1359, "end": 1440},
    {"title": "The Locked Room", "start": 1445, "end": 1544},
    {"title": "Eleanor's Room", "start": 1550, "end": 1627},
    {"title": "The Transfer of Trust", "start": 1634, "end": 1720},
    {"title": "The Memento", "start": 1725, "end": 1795},
    {"title": "Command and Control", "start": 1801, "end": 1893},
    {"title": "The Great Un-Shelving", "start": 1898, "end": 1983},
    {"title": "The General Contractor", "start": 1989, "end": 2052},
    {"title": "The Coup de Grâce", "start": 2058, "end": 2131},
    {"title": "The Unveiling", "start": 2139, "end": 2222},
    {"title": "A Different Kind of Payout", "start": 2225, "end": 2258},
    {"title": "The Librarian", "start": 2264, "end": 2359},
    {"title": "The Bridge", "start": 2366, "end": 2416},
    {"title": "The New Baseline", "start": 2456, "end": 2529},
    {"title": "A Fair Cut", "start": 2535, "end": 2594},
    {"title": "The Advantage Play", "start": 2600, "end": 2694},
    {"title": "The Funnel", "start": 2700, "end": 2754},
    {"title": "Epilogue: The Final Calculation", "start": 2761, "end": 2859}
]

chapter_num = 1
for ch in chapters:
    filename = f"chapter_{chapter_num:02d}.md"
    chapter_num += 1
    
    start_idx = ch["start"] - 1
    end_idx = ch["end"]
    
    content = []
    for idx in range(start_idx, end_idx):
        if idx not in notes_indices and idx < len(lines):
            content.append(lines[idx])
            
    # Add a title header
    full_content = f"# Chapter {chapter_num-1}: {ch['title']}\n\n" + "".join(content)
    
    with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
        f.write(full_content)
        
    print(f"Saved {filename}")

print("Done.")
