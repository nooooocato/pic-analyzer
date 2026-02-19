import pytest
import os
import shutil
from src.plugin.base import BasePlugin
from src.plugin.manager import PluginManager

class MockPlugin(BasePlugin):
    @property
    def name(self): return "Mock Plugin"
    @property
    def description(self): return "A mock plugin for testing"
    def run(self, image_path): return {"mock_result": True}
    def initialize_ui(self, main_window): pass

def test_base_plugin_interface():
    # Verify it's an abstract base class or has required methods
    with pytest.raises(TypeError):
        BasePlugin() # Should not be instantiable if using ABC

def test_plugin_manager_loading(tmp_path):
    # Create a dummy plugin file
    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir()
    
    # We need to make sure 'plugins.base' is importable or mock it
    # For simplicity, we'll write a mock base.py in the tmp_path as well
    # and add it to sys.path
    
    plugin_content = """
from src.plugin.base import BasePlugin
class TestPlugin(BasePlugin):
    @property
    def name(self): return "Test Plugin"
    @property
    def description(self): return "Test Desc"
    def run(self, image_path): return {"test": True}
    def initialize_ui(self, main_window): pass
"""
    plugin_file = plugins_dir / "test_plugin.py"
    plugin_file.write_text(plugin_content)
    
    manager = PluginManager(str(plugins_dir))
    assert "Test Plugin" in manager.plugins
    assert manager.plugins["Test Plugin"].run("dummy.jpg") == {"test": True}
