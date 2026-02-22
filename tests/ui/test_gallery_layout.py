
import pytest
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from unittest.mock import MagicMock

# This import will fail initially, which is expected for the red phase.
from src.ui.gallery.gallery_layout import GalleryLayout

@pytest.fixture
def layout_widget(qtbot, monkeypatch):
    """Fixture to create a GalleryLayout instance with mocked dependencies."""
    from src.app.state import state
    mock_db = MagicMock()
    mock_db.get_metric_values.return_value = {}
    monkeypatch.setattr(state, "db_manager", mock_db)
    
    lw = GalleryLayout()
    qtbot.addWidget(lw)
    return lw

def test_gallery_layout_instantiation(layout_widget):
    """Test that the GalleryLayout can be instantiated."""
    assert layout_widget is not None
    assert isinstance(layout_widget, QScrollArea)

def test_add_item_triggers_refresh(layout_widget, qtbot):
    """Test that adding an item eventually creates a group."""
    item_data = {"path": "test.jpg", "thumb": None}
    layout_widget.add_item(item_data)
    
    # Wait for the refresh timer
    qtbot.wait(100)
    
    from src.ui.gallery.grouped_list_widget import GroupedListWidget
    list_widget = layout_widget.findChild(GroupedListWidget)
    assert list_widget is not None
    assert list_widget.count() == 1
