import pytest
from PySide6.QtWidgets import QMainWindow, QToolBar, QTreeView, QDockWidget
from src.ui.main_window import MainWindow

def test_main_window_init(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    
    assert window.windowTitle() == "Pic-Analyzer"
    assert isinstance(window, QMainWindow)

def test_main_window_toolbar(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    
    # Check if a toolbar exists
    toolbars = window.findChildren(QToolBar)
    assert len(toolbars) > 0

def test_main_window_data_inspector(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    
    # Check if a QTreeView exists (Data Inspector)
    tree_views = window.findChildren(QTreeView)
    assert len(tree_views) > 0

def test_update_inspector(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    
    metadata = {
        "Filename": "test.jpg",
        "Size": "100 KB",
        "Date": "2024-01-01"
    }
    window.update_inspector(metadata)
    
    model = window.tree_view.model()
    assert model is not None
    assert model.rowCount() == 3
    # Check if first key is Filename
    assert model.item(0, 0).text() == "Filename"
    assert model.item(0, 1).text() == "test.jpg"
