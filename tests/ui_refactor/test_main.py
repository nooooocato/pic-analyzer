import pytest
from src.ui.main_window.logic import MainWindow

def test_main_window_init(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.windowTitle() == "Pic-Analyzer"
    # Gallery is now direct attribute of MainWindow
    assert window.gallery is not None
    # sort_overlay is now direct attribute of MainWindow
    assert window.sort_overlay is not None

def test_main_window_resize(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    
    gallery = window.gallery
    initial_sort_pos = window.sort_overlay.pos()
    
    # Resize the window
    window.resize(1400, 900)
    # The gallery's resizeEvent should have been triggered
    # and overlays repositioned.
    assert window.sort_overlay.pos() != initial_sort_pos
