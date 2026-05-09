import os

file_path = r"C:\Users\bartt\.gemini\antigravity\scratch\LordTomasTheFarmer.md"
output_dir = r"C:\Users\bartt\Projects\BartsBooks\books\LordTomasTheFarmer"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Part 1: Lines 1 to 1526 (0-indexed: 0 to 1526)
# Wait, line 1526 is the last line of Part 1.
# Let's check the content of line 1526.
# In the view_file output, line 1526 was:
# "master ready for the next stage of the grind."
# So Part 1 ends there.

part1_lines = lines[0:1526]
notes_lines = lines[1526:1600]
part2_lines = lines[1600:]

with open(os.path.join(output_dir, "part_1.md"), 'w', encoding='utf-8') as f:
    f.writelines(part1_lines)
print("Saved part_1.md")

with open(os.path.join(output_dir, "notes.md"), 'w', encoding='utf-8') as f:
    f.writelines(notes_lines)
print("Saved notes.md")

with open(os.path.join(output_dir, "part_2.md"), 'w', encoding='utf-8') as f:
    f.writelines(part2_lines)
print("Saved part_2.md")

print("Done.")
