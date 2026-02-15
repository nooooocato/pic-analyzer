from PySide6.QtCore import Qt, Signal
from src.ui.common.card.logic import Card
from .layout import SelectionOverlayLayout
from .style import get_style

class SelectionOverlay(Card):
    """Floating overlay for batch actions in multi-selection mode."""
    selectAllRequested = Signal()
    invertSelectionRequested = Signal()
    cancelRequested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent, setup_layout=False)
        self.setObjectName("Card")
        self.setWindowFlags(Qt.SubWindow)
        
        self.layout_engine = SelectionOverlayLayout()
        self.layout_engine.setup_ui(self)
        
        # Connect signals
        self.layout_engine.btn_all.clicked.connect(self.selectAllRequested.emit)
        self.layout_engine.btn_invert.clicked.connect(self.invertSelectionRequested.emit)
        self.layout_engine.btn_cancel.clicked.connect(self.cancelRequested.emit)
        
        self.setStyleSheet(self.styleSheet() + get_style())
        self.adjustSize()
