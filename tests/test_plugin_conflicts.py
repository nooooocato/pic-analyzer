import os
import pytest
import shutil
from src.plugin_manager import PluginManager

def test_plugin_manager_detects_conflicts():
    plugin1_content = """
from base import BasePlugin

class Plugin1(BasePlugin):
    @property
    def name(self): return "Duplicate Name"
    @property
    def description(self): return "Desc 1"
    def run(self, *args, **kwargs): return "1"
"""
    plugin2_content = """
from base import BasePlugin

class Plugin2(BasePlugin):
    @property
    def name(self): return "Duplicate Name"
    @property
    def description(self): return "Desc 2"
    def run(self, *args, **kwargs): return "2"
"""
    os.makedirs("plugins/cat1", exist_ok=True)
    os.makedirs("plugins/cat2", exist_ok=True)
    with open("plugins/cat1/p1.py", "w") as f: f.write(plugin1_content)
    with open("plugins/cat2/p2.py", "w") as f: f.write(plugin2_content)
    
    try:
        manager = PluginManager("plugins")
        # According to spec, it should refuse to load EITHER if there is a conflict.
        assert "Duplicate Name" not in manager.plugins
    finally:
        shutil.rmtree("plugins/cat1")
        shutil.rmtree("plugins/cat2")
