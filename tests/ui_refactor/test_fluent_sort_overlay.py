import pytest
from PySide6.QtWidgets import QApplication
from src.ui.overlays.sort.logic import SortOverlay
from qfluentwidgets import CommandBar, RoundMenu
from unittest.mock import MagicMock

@pytest.fixture
def app(qtbot):
    return QApplication.instance() or QApplication([])

def test_sort_overlay_is_command_bar(qtbot):
    mock_manager = MagicMock()
    overlay = SortOverlay(mock_manager)
    qtbot.addWidget(overlay)
    
    assert isinstance(overlay, CommandBar)
    assert hasattr(overlay, 'sortRequested')

def test_sort_overlay_menu(qtbot):
    mock_manager = MagicMock()
    mock_manager.plugins = {"Name": MagicMock(), "Size": MagicMock()}
    overlay = SortOverlay(mock_manager)
    qtbot.addWidget(overlay)
    
    # Check if menu can be created/accessed
    menu = overlay.create_menu()
    assert isinstance(menu, RoundMenu)
    assert len(menu.actions()) == 2
