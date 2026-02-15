import pytest
from PySide6.QtWidgets import QApplication
from src.ui.common.icon_button.logic import IconButton
from src.ui.common.card.logic import Card
from qfluentwidgets import FluentIcon

@pytest.fixture
def app(qtbot):
    return QApplication.instance() or QApplication([])

def test_icon_button(qtbot):
    btn = IconButton(FluentIcon.ADD, tooltip="Test Tooltip")
    qtbot.addWidget(btn)
    
    assert btn.toolTip() == "Test Tooltip"
    assert btn.width() == 36
    assert btn.height() == 36

def test_card(qtbot):
    card = Card()
    qtbot.addWidget(card)
    
    assert card.objectName() == "Card"
    assert card.layout() is not None
