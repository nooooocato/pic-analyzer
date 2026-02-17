import pytest
import os
import shutil
from src.ui.main_window.logic import MainWindow
from src.plugin.manager import PluginManager
from src.app.state import state

def test_full_plugin_lifecycle_integration(qtbot, tmp_path, monkeypatch):
    # Create a temporary plugins directory
    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir()
    (plugins_dir / "sort").mkdir()
    
    plugin_content = """
from src.plugin.base import BasePlugin
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
    
    # Patch PluginManager to always use our temp dir if requested
    original_pm_init = PluginManager.__init__
    def patched_pm_init(self, p_dir):
        original_pm_init(self, str(plugins_dir))

    monkeypatch.setattr("src.plugin.manager.PluginManager.__init__", patched_pm_init) 
    
    # Reset and re-initialize state to use the patched PluginManager
    state.initialized = False
    state.initialize(plugins_dir=str(plugins_dir))

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
