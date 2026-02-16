import os
import sys
# Add plugins to path for standalone test
sys.path.append(os.path.join(os.getcwd(), "plugins"))
from group.date_grouping.ui import DateGroupingPlugin

plugin = DateGroupingPlugin()
with open("test_date.txt", "w") as f: f.write("test")
result = plugin.run("test_date.txt")
print(f"Plugin result: {result}")

if os.path.exists("test_date.txt"): os.remove("test_date.txt")