
import pytest
from PySide6.QtWidgets import QListView, QWidget
from PySide6.QtCore import Qt
from unittest.mock import MagicMock

# This import will fail initially, which is expected for the red phase.
from src.ui.gallery.grouped_list_widget import GroupedListWidget

@pytest.fixture
def widget(qtbot):
    """Fixture to create a GroupedListWidget instance."""
    w = GroupedListWidget()
    qtbot.addWidget(w)
    return w

def test_grouped_list_widget_instantiation(widget):
    """Test that the GroupedListWidget can be instantiated."""
    assert widget is not None
    assert isinstance(widget, QListView)

def test_add_item(widget):
    """Test that adding an item works."""
    from PySide6.QtWidgets import QListWidgetItem
    item = QListWidgetItem("Test Item")
    widget.addItem(item)
    assert widget.count() == 1
    assert widget.item(0).text() == "Test Item"

def test_selection_mode_enabled(widget):
    """Test that selection mode can be enabled and disabled."""
    assert not widget.selection_mode_enabled
    widget.set_selection_mode_enabled(True)
    assert widget.selection_mode_enabled
    widget.set_selection_mode_enabled(False)
    assert not widget.selection_mode_enabled

def test_adjust_height_empty(widget):
    """Test adjust_height on an empty widget."""
    widget.adjust_height()
    assert widget.height() == 0
