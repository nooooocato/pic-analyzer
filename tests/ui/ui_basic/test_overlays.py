import pytest
from PySide6.QtCore import Qt
from src.ui.overlays.selection.logic import SelectionOverlay
from src.ui.overlays.sort.logic import SortOverlay
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
    assert overlay.layout_engine.btn_all is not None
    assert overlay.layout_engine.btn_invert is not None
    assert overlay.layout_engine.btn_cancel is not None
    assert overlay.windowFlags() & Qt.SubWindow

def test_sort_overlay_ui(qtbot):
    mock_db = MagicMock()
    overlay = SortOverlay(mock_db)
    qtbot.addWidget(overlay)
    
    assert overlay.layout_engine.btn_sort is not None
    assert overlay.windowFlags() & Qt.SubWindow

def test_sort_overlay_menu_creation(qtbot):
    mock_db = MagicMock()
    mock_db.get_numeric_metrics.return_value = ["size"]
    
    overlay = SortOverlay(mock_db)
    qtbot.addWidget(overlay)

    plugin1 = MagicMock()
    plugin1.name = "Plugin1"
    plugin2 = MagicMock()
    plugin2.name = "Plugin2"
    overlay.add_external_plugin(plugin1)
    overlay.add_external_plugin(plugin2)
    
    menu = overlay.create_menu()
    actions = menu.actions()
    assert len(actions) == 1
    assert actions[0].text() == "Size"
    
    # Check submenu
    submenu = actions[0].menu()
    sub_actions = submenu.actions()
    assert len(sub_actions) == 2
    assert sub_actions[0].text() == "Plugin1"
    
    with qtbot.waitSignal(overlay.sortRequested, timeout=1000) as blocker:
        sub_actions[0].trigger()
    assert blocker.args == ["size", "Plugin1"]
