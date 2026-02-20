import pytest
from src.ui.main_window.logic import MainWindow

def test_main_window_init(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.windowTitle() == "Pic-Analyzer"
    assert window.layout_engine.gallery is not None
    assert window.layout_engine.image_viewer is not None
    assert hasattr(window.layout_engine, "sidebar")

def test_main_window_resize(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    
    # Verify that the gallery/viewer scale with the window
    initial_gallery_size = window.layout_engine.gallery.size()
    window.resize(1400, 900)
    assert window.layout_engine.gallery.size() != initial_gallery_size
