import pytest
from unittest.mock import MagicMock
from src.ui.main_window.logic import MainWindow
from src.plugins.manager import PluginManager

def test_main_window_calls_initialize_ui_on_plugins(qtbot):
    # Mock PluginManager to return a mock plugin
    mock_plugin = MagicMock()
    mock_plugin.name = "Test Plugin"
    
    # We need to mock PluginManager.load_plugins or similar to return our mock
    # Actually, it's easier to just patch the manager attribute on MainWindow after init
    # or mock the whole PluginManager class.
    
    with MagicMock() as mock_manager_class:
        mock_manager_class.return_value.plugins = {"Test Plugin": mock_plugin}
        # In a real scenario, we'd use something like 'unittest.mock.patch'
        # but here let's see how MainWindow creates its manager.
        pass

def test_main_window_initializes_plugins(qtbot, monkeypatch):
    mock_plugin = MagicMock()
    mock_plugin.name = "Test Plugin"
    
    # Mock PluginManager
    class MockManager:
        def __init__(self, dir):
            self.plugins = {"Test Plugin": mock_plugin}
    
    monkeypatch.setattr("src.ui.main_window.logic.PluginManager", MockManager)
    
    # Instantiate MainWindow
    window = MainWindow()
    qtbot.addWidget(window)
    
    # Check if initialize_ui was called
    mock_plugin.initialize_ui.assert_called_with(window)
