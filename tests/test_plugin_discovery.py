import os
import pytest
import shutil
from src.plugin_manager import PluginManager
from plugins.base import BasePlugin

def test_plugin_manager_discovers_external_plugins():
    # Create a dummy plugin in the new directory
    plugin_content = """
from plugins.base import BasePlugin

class MockExternalPlugin(BasePlugin):
    @property
    def name(self):
        return "Mock External Plugin"
    
    @property
    def description(self):
        return "A mock plugin for testing"
    
    def run(self, *args, **kwargs):
        return "Success"
    
    def initialize_ui(self, main_window):
        pass
"""
    os.makedirs("plugins/sort", exist_ok=True)
    with open("plugins/sort/mock_plugin.py", "w") as f:
        f.write(plugin_content)
    
    try:
        manager = PluginManager("plugins")
        assert "Mock External Plugin" in manager.plugins
    finally:
        if os.path.exists("plugins/sort/mock_plugin.py"):
            os.remove("plugins/sort/mock_plugin.py")

def test_plugin_manager_discovers_nested_plugins():
    # Create a dummy plugin in a nested category
    plugin_content = """
from plugins.base import BasePlugin

class NestedPlugin(BasePlugin):
    @property
    def name(self):
        return "Nested Plugin"
    
    @property
    def description(self):
        return "A nested mock plugin for testing"
    
    def run(self, *args, **kwargs):
        return "Nested Success"
    
    def initialize_ui(self, main_window):
        pass
"""
    os.makedirs("plugins/test_category", exist_ok=True)
    with open("plugins/test_category/nested_plugin.py", "w") as f:
        f.write(plugin_content)
    
    try:
        manager = PluginManager("plugins")
        assert "Nested Plugin" in manager.plugins
    finally:
        if os.path.exists("plugins/test_category"):
            shutil.rmtree("plugins/test_category")
