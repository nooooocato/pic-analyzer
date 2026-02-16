import pytest
import os
import shutil
from src.ui.main_window.logic import MainWindow

def test_full_plugin_lifecycle_integration(qtbot, tmp_path, monkeypatch):
    # Create a temporary plugins directory
    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir()
    (plugins_dir / "sort").mkdir()
    
    plugin_content = """
from base import BasePlugin
from PySide6.QtGui import QAction

class IntegrationTestPlugin(BasePlugin):
    @property
    def name(self): return "Integration Plugin"
    @property
    def description(self): return "Testing full lifecycle"
    def run(self, path): return {"test": True}
    def initialize_ui(self, main_window):
        action = QAction("Integration Action", main_window)
        main_window.add_toolbar_action(action)
        menu = main_window.get_menu("TestMenu")
        menu.addAction(action)
        main_window._integration_action = action
"""
    with open(plugins_dir / "sort" / "integration_plugin.py", "w") as f:
        f.write(plugin_content)
    
    # Use monkeypatch to make MainWindow look at our temp plugins dir
    # We need to ensure 'base' is importable. It is in the real plugins dir.
    # In this test, we might need to add the real 'plugins' dir to sys.path
    # so that 'from base import BasePlugin' works.
    import sys
    real_plugins_path = os.path.abspath("plugins")
    if real_plugins_path not in sys.path:
        sys.path.append(real_plugins_path)

    # Monkeypatch the plugins_dir path used in MainWindow
    # Actually, PluginManager takes it as an argument.
    # In MainWindow.__init__: self.plugin_manager = PluginManager("plugins")
    
    original_init = MainWindow.__init__
    def mocked_init(self):
        # We need to call the original init but override the plugins_dir
        # This is tricky because PluginManager is instantiated inside init.
        pass
    
    # Instead, let's patch PluginManager to always use our temp dir if requested
    from src.plugin_manager import PluginManager
    original_pm_init = PluginManager.__init__
    def patched_pm_init(self, p_dir):
        original_pm_init(self, str(plugins_dir))
    
    monkeypatch.setattr("src.plugin_manager.PluginManager.__init__", patched_pm_init)
    
    window = MainWindow()
    qtbot.addWidget(window)
    
    # Verify plugin was loaded
    assert "Integration Plugin" in window.plugin_manager.plugins
    
    # Verify UI injection
    assert hasattr(window, "_integration_action")
    assert window._integration_action.text() == "Integration Action"
    
    # Verify menu creation
    menu = window.get_menu("TestMenu")
    assert menu.title() == "&TestMenu"
    assert window._integration_action in menu.actions()
    
    # Verify toolbar injection
    assert window._integration_action in window.layout_engine.toolbar.actions()
