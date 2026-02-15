import pytest
import os
import shutil
from src.plugins.sort.manager import SortPluginManager
from src.plugins.sort.base import BaseSortPlugin

def test_sort_plugin_manager_loads_plugins(tmp_path):
    # Create a dummy plugin directory
    plugins_dir = tmp_path / "sort_plugins"
    plugins_dir.mkdir()
    
    # Create a dummy plugin file
    plugin_file = plugins_dir / "test_sort.py"
    plugin_file.write_text("""
from src.plugins.sort.base import BaseSortPlugin

class TestSortPlugin(BaseSortPlugin):
    @property
    def name(self): return "Test Sort"
    @property
    def description(self): return "Description"
    def sort(self, items, metric_key): return items
""")

    manager = SortPluginManager(str(plugins_dir))
    assert "Test Sort" in manager.plugins
    assert isinstance(manager.plugins["Test Sort"], BaseSortPlugin)
