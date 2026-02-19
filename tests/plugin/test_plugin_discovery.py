import os
import pytest
import shutil
from src.plugin.manager import PluginManager
from src.plugin.base import BasePlugin

def test_plugin_manager_discovers_external_plugins():
    # Create a dummy plugin in the new directory
    plugin_content = """
from src.plugin.base import BasePlugin

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
from src.plugin.base import BasePlugin

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

def test_plugin_manager_categorizes_plugins():
    sort_plugin_content = """
from src.plugin.base import BasePlugin
class SortPlugin(BasePlugin):
    @property
    def name(self): return "Sort Mock"
    @property
    def description(self): return "desc"
    def run(self, *args): pass
    def initialize_ui(self, main_window): pass
"""
    group_plugin_content = """
from src.plugin.base import BasePlugin
class GroupPlugin(BasePlugin):
    @property
    def name(self): return "Group Mock"
    @property
    def description(self): return "desc"
    def run(self, *args): pass
    def initialize_ui(self, main_window): pass
"""
    general_plugin_content = """
from src.plugin.base import BasePlugin
class GeneralPlugin(BasePlugin):
    @property
    def name(self): return "General Mock"
    @property
    def description(self): return "desc"
    def run(self, *args): pass
    def initialize_ui(self, main_window): pass
"""
    os.makedirs("plugins/sort", exist_ok=True)
    os.makedirs("plugins/group", exist_ok=True)
    os.makedirs("plugins/other", exist_ok=True)
    
    with open("plugins/sort/s_mock.py", "w") as f: f.write(sort_plugin_content)
    with open("plugins/group/g_mock.py", "w") as f: f.write(group_plugin_content)
    with open("plugins/other/o_mock.py", "w") as f: f.write(general_plugin_content)
    
    try:
        manager = PluginManager("plugins")
        assert "Sort Mock" in manager.sort_plugins
        assert "Group Mock" in manager.group_plugins
        assert "General Mock" in manager.general_plugins
        assert "Sort Mock" in manager.plugins
    finally:
        for p in ["plugins/sort/s_mock.py", "plugins/group/g_mock.py", "plugins/other/o_mock.py"]:
            if os.path.exists(p): os.remove(p)
