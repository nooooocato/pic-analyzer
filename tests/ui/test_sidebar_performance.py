import pytest
import time
from PySide6.QtCore import Qt
from src.ui.main_window.logic import MainWindow
from src.app.state import state

def test_large_set_responsiveness(qtbot):
    """Verify that adding 1000 items doesn't freeze the UI."""
    state.initialize()
    window = MainWindow()
    qtbot.addWidget(window)
    gallery = window.layout_engine.gallery
    
    start_time = time.time()
    for i in range(1000):
        gallery.add_item({"path": f"path_{i}.jpg"})
    end_time = time.time()
    
    # 1000 items should be added very quickly to the internal list
    assert end_time - start_time < 0.5
    
    # Wait for the refresh timer to fire (50ms)
    qtbot.wait(200)
    
    # Gallery should have 1000 items visible
    assert gallery.count() == 1000
