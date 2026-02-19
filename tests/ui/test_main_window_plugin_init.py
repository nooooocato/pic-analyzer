import pytest
from unittest.mock import MagicMock
from src.ui.main_window.logic import MainWindow
from src.app.state import state

def test_main_window_initializes_plugins(qtbot, monkeypatch):
    mock_plugin = MagicMock()
    mock_plugin.name = "Test Plugin"
    
    # Mock PluginManager
    class MockManager:
        def __init__(self, dir):
            self.plugins = {"Test Plugin": mock_plugin}
            self.sort_plugins = {}
    
    # Mock state.plugin_manager BEFORE MainWindow init
    mock_manager = MockManager("plugins")
    monkeypatch.setattr(state, "plugin_manager", mock_manager)
    monkeypatch.setattr(state, "initialized", True)
    
    # Instantiate MainWindow
    window = MainWindow()
    qtbot.addWidget(window)
    
    # Check if initialize_ui was called
    mock_plugin.initialize_ui.assert_called_with(window)
