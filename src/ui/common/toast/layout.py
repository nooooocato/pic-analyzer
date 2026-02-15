from PySide6.QtWidgets import QHBoxLayout, QLabel, QFrame
from src.ui.theme import Theme

class ToastLayout:
    def setup_ui(self, widget: QFrame):
        widget.setObjectName("Toast")
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(Theme.SPACING_L, Theme.SPACING_S, Theme.SPACING_L, Theme.SPACING_S)
        
        self.label = QLabel()
        layout.addWidget(self.label)
        return layout
