import pytest
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt
from src.ui.overlays.selection.logic import SelectionOverlay
from qfluentwidgets import FlyoutView

@pytest.fixture
def app(qtbot):
    return QApplication.instance() or QApplication([])

def test_selection_overlay_is_flyout_view(qtbot):
    overlay = SelectionOverlay()
    qtbot.addWidget(overlay)
    
    # It should inherit FlyoutView or contain one
    # If I refactor it to inherit FlyoutView:
    assert isinstance(overlay, FlyoutView)
    
    # Check signals existence
    assert hasattr(overlay, 'selectAllRequested')
    assert hasattr(overlay, 'invertSelectionRequested')
    assert hasattr(overlay, 'cancelRequested')

def test_selection_overlay_layout(qtbot):
    overlay = SelectionOverlay()
    qtbot.addWidget(overlay)
    
    # It should have the buttons
    assert overlay.layout_engine.btn_all is not None
    assert overlay.layout_engine.btn_invert is not None
    assert overlay.layout_engine.btn_cancel is not None
