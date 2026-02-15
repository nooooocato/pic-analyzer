import pytest
from PySide6.QtWidgets import QApplication, QLabel
from src.ui.common.card.logic import Card
from qfluentwidgets import SimpleCardWidget

@pytest.fixture
def app(qtbot):
    return QApplication.instance() or QApplication([])

def test_fluent_card(qtbot):
    card = Card()
    qtbot.addWidget(card)
    
    assert isinstance(card, SimpleCardWidget)
    
    # Test adding widget
    label = QLabel("Test Content")
    card.addWidget(label)
    
    # SimpleCardWidget usually manages layout internally or we set it?
    # Actually SimpleCardWidget doesn't have addWidget method by default unless we subclass/wrapper.
    # So we need to verify if Card wraps it or subclasses it and adds helper methods.
    
    # Check if label is child of card
    assert label.parent() == card or label.parent().parent() == card

def test_card_layout_access(qtbot):
    card = Card()
    qtbot.addWidget(card)
    # Check if we can access layout to add items
    # The original Card had addLayout method.
    assert hasattr(card, 'addLayout')
