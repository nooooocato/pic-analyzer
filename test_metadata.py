import os
from src.plugins.date_grouping import DateGroupingPlugin

plugin = DateGroupingPlugin()
with open("test_date.txt", "w") as f: f.write("test")
result = plugin.run("test_date.txt")
print(f"Plugin result: {result}")

if os.path.exists("test_date.txt"): os.remove("test_date.txt")