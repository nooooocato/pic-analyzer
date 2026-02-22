
import pytest
from PySide6.QtWidgets import QApplication
from src.ui.main_window.logic import MainWindow
from src.ui.gallery.gallery_layout import GalleryLayout

def test_main_window_uses_gallery_layout(qtbot):
    """Integration test to verify MainWindow uses the refactored GalleryLayout."""
    window = MainWindow()
    qtbot.addWidget(window)
    
    # Check if the central widget's layout contains GalleryLayout
    # Or if the central widget itself is GalleryLayout
    assert isinstance(window.centralWidget(), GalleryLayout)

def test_gallery_interactions_in_main_window(qtbot):
    """Test that main window correctly interacts with the gallery."""
    window = MainWindow()
    qtbot.addWidget(window)
    gallery = window.layout_engine.gallery
    
    # Verify signals are connected
    # We can't easily check connections in PySide6 without some hacks, 
    # but we can trigger a signal and see if the slot is called.
    
    # Mock _on_item_selected
    from unittest.mock import MagicMock
    window._on_item_selected = MagicMock()
    
    gallery.item_selected.emit("test_path.jpg")
    window._on_item_selected.assert_called_with("test_path.jpg")
