from qfluentwidgets import SimpleCardWidget
from PySide6.QtWidgets import QVBoxLayout
from src.ui.theme import Theme

class Card(SimpleCardWidget):
    def __init__(self, parent=None, setup_layout=True):
        super().__init__(parent)
        self.setObjectName("Card")
        
        self.main_layout = None
        if setup_layout:
            # Setup layout
            self.main_layout = QVBoxLayout(self)
            self.main_layout.setContentsMargins(Theme.SPACING_M, Theme.SPACING_M, Theme.SPACING_M, Theme.SPACING_M)
            self.main_layout.setSpacing(Theme.SPACING_S)
        
    def addWidget(self, widget):
        if self.main_layout:
            self.main_layout.addWidget(widget)
        
    def addLayout(self, layout):
        if self.main_layout:
            self.main_layout.addLayout(layout)
