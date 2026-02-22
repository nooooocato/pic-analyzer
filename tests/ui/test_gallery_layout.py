
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

def test_selection_mode_toggle(layout_widget):
    """Test that selection mode toggles correctly."""
    assert not layout_widget.selection_mode_enabled
    layout_widget.set_selection_mode_enabled(True)
    assert layout_widget.selection_mode_enabled
    layout_widget.set_selection_mode_enabled(False)
    assert not layout_widget.selection_mode_enabled

def test_clear_layout(layout_widget, qtbot):
    """Test that clear removes items."""
    layout_widget.add_item({"path": "test.jpg", "thumb": None})
    qtbot.wait(100)
    assert layout_widget.count() == 1
    layout_widget.clear()
    assert layout_widget.count() == 0
