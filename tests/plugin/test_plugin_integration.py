import pytest
import os
import shutil
from src.ui.main_window.logic import MainWindow
from src.plugin.manager import PluginManager
from src.app.state import state
from src.plugin.base import BasePlugin

def test_plugin_discovery_integration(qtbot, tmp_path, monkeypatch):
    """Test that plugins are discovered and categorized correctly in the full app context."""
    # Create a temporary plugins directory
    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir()
    (plugins_dir / "sort").mkdir()
    
    plugin_content = """
from src.plugin.base import SortPlugin
class MySort(SortPlugin):
    @property
    def name(self): return "Integration Sort"
    @property
    def description(self): return "desc"
    @property
    def schema(self):
        return {"parameters": [{"name": "p1", "type": "int", "default": 5, "label": "P1"}]}
    def run(self, path): return {}
    def sort(self, items, metric, params): return items
"""
    with open(plugins_dir / "sort" / "sort_plugin.py", "w") as f:
        f.write(plugin_content)
    
    # Patch PluginManager to use our temp dir
    monkeypatch.setattr(state, "plugin_manager", PluginManager(str(plugins_dir)))
    
    # Mock DB Manager
    from unittest.mock import MagicMock
    state.db_manager = MagicMock()
    state.db_manager.get_numeric_metrics.return_value = ["metric1"]
    
    state.initialized = True

    window = MainWindow()
    qtbot.addWidget(window)
    
    # Verify plugin was loaded and categorized
    assert "Integration Sort" in window.plugin_manager.sort_plugins
    plugin = window.plugin_manager.sort_plugins["Integration Sort"]
    assert plugin.name == "Integration Sort"
    
    # Verify sidebar integration (dropdown populated)
    sidebar = window.layout_engine.sidebar
    idx = sidebar.sort_combo.findText("Integration Sort")
    assert idx != -1
    
    # Verify dynamic UI generation on selection
    sidebar.sort_combo.setCurrentIndex(idx)
    # The 'is_param' widget should exist
    params = sidebar.sorting_section.findChildren(object, "is_param") # Wait, findChild with property is not direct
    # Let's just check if a QSpinBox appeared in the layout
    from PySide6.QtWidgets import QSpinBox
    spinners = sidebar.sorting_section.findChildren(QSpinBox)
    assert len(spinners) > 0
    assert spinners[0].value() == 5
