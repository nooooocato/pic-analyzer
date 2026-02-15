from PySide6.QtWidgets import QFrame
from .style import get_style
from .layout import CardLayout

class Card(QFrame):
    def __init__(self, parent=None, setup_layout=True):
        super().__init__(parent)
        self.main_layout = None
        if setup_layout:
            self.layout_engine = CardLayout()
            self.main_layout = self.layout_engine.setup_ui(self)
        self.setStyleSheet(get_style())
    
    def addWidget(self, widget):
        if self.main_layout:
            self.main_layout.addWidget(widget)
        
    def addLayout(self, layout):
        if self.main_layout:
            self.main_layout.addLayout(layout)
