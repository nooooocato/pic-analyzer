import pytest
from PySide6.QtCore import Qt
from src.ui.overlays.selection.logic import SelectionOverlay
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
