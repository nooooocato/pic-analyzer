import pytest
from PySide6.QtWidgets import QApplication
from src.ui.overlays.sort.logic import SortOverlay
from qfluentwidgets import SimpleCardWidget, RoundMenu, TransparentDropDownToolButton
from unittest.mock import MagicMock

@pytest.fixture
def app(qtbot):
    return QApplication.instance() or QApplication([])

def test_sort_overlay_is_card_with_dropdown(qtbot):
    mock_manager = MagicMock()
    overlay = SortOverlay(mock_manager)
    qtbot.addWidget(overlay)
    
    assert isinstance(overlay, SimpleCardWidget)
    assert isinstance(overlay.btn_sort, TransparentDropDownToolButton)
    assert hasattr(overlay, 'sortRequested')

def test_sort_overlay_menu(qtbot):
    mock_manager = MagicMock()
    mock_manager.plugins = {"Name": MagicMock(), "Size": MagicMock()}
    overlay = SortOverlay(mock_manager)
    qtbot.addWidget(overlay)
    
    menu = overlay.sort_menu
    assert isinstance(menu, RoundMenu)
    assert len(menu.actions()) == 2
