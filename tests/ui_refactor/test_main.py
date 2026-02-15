import pytest
from src.ui.main_window.logic import MainWindow

def test_main_window_init(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.windowTitle() == "Pic-Analyzer"
    assert window.layout_engine.gallery is not None
    assert window.layout_engine.image_viewer is not None
    assert window.layout_engine.sort_overlay is not None

def test_main_window_resize(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    
    initial_sort_pos = window.layout_engine.sort_overlay.pos()
    window.resize(1400, 900)
    # Positions should change on resize
    assert window.layout_engine.sort_overlay.pos() != initial_sort_pos
