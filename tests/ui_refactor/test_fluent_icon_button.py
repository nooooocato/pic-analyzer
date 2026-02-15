import pytest
from PySide6.QtWidgets import QApplication
from src.ui.common.icon_button.logic import IconButton
from qfluentwidgets import TransparentToolButton, FluentIcon

@pytest.fixture
def app(qtbot):
    return QApplication.instance() or QApplication([])

def test_fluent_icon_button(qtbot):
    # Test with FluentIcon
    btn = IconButton(FluentIcon.ADD, tooltip="Add Item")
    qtbot.addWidget(btn)
    
    # Should inherit from TransparentToolButton
    assert isinstance(btn, TransparentToolButton)
    
    # Verify tooltip
    assert btn.toolTip() == "Add Item"
    
    # Verify icon (FluentIcon sets the icon property)
    # Note: FluentIcon is an enum, but setIcon accepts QIcon or FluentIcon
    # checking property directly might be tricky, checking existence is good enough
    assert not btn.icon().isNull()

def test_fluent_icon_button_defaults(qtbot):
    btn = IconButton(FluentIcon.DELETE)
    qtbot.addWidget(btn)
    
    assert isinstance(btn, TransparentToolButton)
    assert not btn.icon().isNull()
