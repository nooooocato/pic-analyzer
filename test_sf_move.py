import os
from src.file_ops import FileManager

fm = FileManager()
with open("test_src.txt", "w") as f: f.write("new")
with open("test_dst.txt", "w") as f: f.write("old")

# Test rename policy
new_path = fm.safe_move("test_src.txt", "test_dst.txt", conflict_policy='rename')
print(f"Moved to: {new_path}")

# Cleanup
for f in ["test_src.txt", "test_dst.txt", "test_dst_1.txt"]:
    if os.path.exists(f): os.remove(f)