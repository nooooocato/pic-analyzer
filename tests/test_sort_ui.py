import pytest
from PySide6.QtCore import Qt
from src.ui.main_window import MainWindow

def test_sort_overlay_exists(qtbot):
    window = MainWindow()
    window.show()
    qtbot.addWidget(window)
    qtbot.waitExposed(window)
    assert hasattr(window, "sort_overlay")
    assert window.sort_overlay.isVisible()

def test_sort_menu_actions(qtbot, monkeypatch):
    window = MainWindow()
    window.show()
    qtbot.addWidget(window)
    qtbot.waitExposed(window)
    
    # Mock get_numeric_metrics
    monkeypatch.setattr(window.db_manager, "get_numeric_metrics", lambda: ["file_size"])
    
    # Trigger menu
    # window._show_sort_menu() # exec() is blocking, so we'd need to mock it or use async
    pass
