import pytest
from PySide6.QtCore import Qt
from src.ui.overlays.selection.logic import SelectionOverlay
from src.ui.overlays.sort.logic import SortOverlay
from qfluentwidgets import FlyoutView, SimpleCardWidget
from unittest.mock import MagicMock

def test_selection_overlay_signals(qtbot):
    overlay = SelectionOverlay()
    qtbot.addWidget(overlay)
    
    with qtbot.waitSignal(overlay.selectAllRequested, timeout=1000):
        qtbot.mouseClick(overlay.layout_engine.btn_all, Qt.LeftButton)
        
    with qtbot.waitSignal(overlay.invertSelectionRequested, timeout=1000):
        qtbot.mouseClick(overlay.layout_engine.btn_invert, Qt.LeftButton)
        
    with qtbot.waitSignal(overlay.cancelRequested, timeout=1000):
        qtbot.mouseClick(overlay.layout_engine.btn_cancel, Qt.LeftButton)

def test_selection_overlay_ui_elements(qtbot):
    overlay = SelectionOverlay()
    assert isinstance(overlay, FlyoutView)
    assert overlay.layout_engine.btn_all is not None
    assert overlay.layout_engine.btn_invert is not None
    assert overlay.layout_engine.btn_cancel is not None
    assert overlay.windowFlags() & Qt.SubWindow

def test_sort_overlay_ui(qtbot):
    mock_manager = MagicMock()
    overlay = SortOverlay(mock_manager)
    qtbot.addWidget(overlay)
    
    assert isinstance(overlay, SimpleCardWidget)
    assert overlay.sort_action is not None
    assert overlay.windowFlags() & Qt.SubWindow

def test_sort_overlay_menu_creation(qtbot):
    mock_manager = MagicMock()
    mock_manager.plugins = {"Plugin1": MagicMock(), "Plugin2": MagicMock()}
    overlay = SortOverlay(mock_manager)
    qtbot.addWidget(overlay)
    
    menu = overlay.create_menu()
    actions = menu.actions()
    assert len(actions) == 2
    assert "Plugin1" in actions[0].text()
    assert "Plugin2" in actions[1].text()
    
    with qtbot.waitSignal(overlay.sortRequested, timeout=1000) as blocker:
        actions[0].trigger()
    assert blocker.args == ["Plugin1"]
