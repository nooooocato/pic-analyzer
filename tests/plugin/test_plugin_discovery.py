import os
import pytest
import shutil
from src.plugin.manager import PluginManager
from src.plugin.base import SortPlugin, GroupPlugin, FilterPlugin, BasePlugin

def test_plugin_manager_categorizes_by_class_type():
    """Test that PluginManager categorizes plugins based on their base class/category property."""
    sort_plugin_content = """
from src.plugin.base import SortPlugin
class MySort(SortPlugin):
    @property
    def name(self): return "Sort Refactor"
    @property
    def description(self): return "desc"
    def run(self, *args): pass
    def sort(self, items, metric, params): return items
"""
    filter_plugin_content = """
from src.plugin.base import FilterPlugin
class MyFilter(FilterPlugin):
    @property
    def name(self): return "Filter Refactor"
    @property
    def description(self): return "desc"
    def run(self, *args): pass
    def filter(self, items, params): return items
"""
    
    os.makedirs("plugins/test_refactor", exist_ok=True)
    with open("plugins/test_refactor/s_ref.py", "w") as f: f.write(sort_plugin_content)
    with open("plugins/test_refactor/f_ref.py", "w") as f: f.write(filter_plugin_content)
    
    try:
        manager = PluginManager("plugins")
        assert "Sort Refactor" in manager.sort_plugins
        assert "Filter Refactor" in manager.filter_plugins
        assert "Sort Refactor" in manager.plugins
    finally:
        if os.path.exists("plugins/test_refactor"):
            shutil.rmtree("plugins/test_refactor")

def test_plugin_manager_schema_access():
    """Test that the manager can access plugin schemas."""
    plugin_with_schema = """
from src.plugin.base import SortPlugin
class SchemaSort(SortPlugin):
    @property
    def name(self): return "Schema Sort"
    @property
    def description(self): return "desc"
    @property
    def schema(self):
        return {"parameters": [{"name": "p1", "type": "int", "default": 1, "label": "P1"}]}
    def run(self, *args): pass
    def sort(self, items, metric, params): return items
"""
    os.makedirs("plugins/test_schema", exist_ok=True)
    with open("plugins/test_schema/sch_ref.py", "w") as f: f.write(plugin_with_schema)
    
    try:
        manager = PluginManager("plugins")
        plugin = manager.plugins["Schema Sort"]
        assert len(plugin.schema["parameters"]) == 1
        assert plugin.schema["parameters"][0]["name"] == "p1"
    finally:
        if os.path.exists("plugins/test_schema"):
            shutil.rmtree("plugins/test_schema")
