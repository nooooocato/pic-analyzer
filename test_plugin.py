import os
from src.plugins.manager import PluginManager

# Create a dummy plugin in the actual project plugins dir for verification
plugin_path = "plugins/verify_plugin.py"
with open(plugin_path, "w") as f:
    f.write("""
from src.plugins.base import BasePlugin
class VerifyPlugin(BasePlugin):
    @property
    def name(self): return "Verify Plugin"
    @property
    def description(self): return "Verifies plugin loading"
    def run(self, image_path): return {"verified": True}
""")

manager = PluginManager("plugins")
print(f"Loaded plugins: {list(manager.plugins.keys())}")

# Cleanup
if os.path.exists(plugin_path): os.remove(plugin_path)