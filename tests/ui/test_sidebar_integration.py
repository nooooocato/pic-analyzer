import pytest
from src.ui.main_window.logic import MainWindow
from PySide6.QtWidgets import QDockWidget
from src.ui.common.sidebar import SidebarContainer

def test_sidebar_integration_in_main_window(qtbot):
    """Test that SidebarContainer is integrated as a dock widget in MainWindow."""
    window = MainWindow()
    qtbot.addWidget(window)
    
    # Check if the sidebar dock exists
    assert hasattr(window.layout_engine, "sidebar_dock")
    assert isinstance(window.layout_engine.sidebar_dock, QDockWidget)
    assert window.layout_engine.sidebar_dock.windowTitle() == "Rules"
    
    # Check if the sidebar container is set
    assert isinstance(window.layout_engine.sidebar, SidebarContainer)
    assert window.layout_engine.sidebar_dock.widget() == window.layout_engine.sidebar
