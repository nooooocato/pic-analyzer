from PySide6.QtWidgets import QFrame, QVBoxLayout
from src.ui.theme import Theme

class CardLayout:
    def setup_ui(self, widget: QFrame):
        widget.setObjectName("Card")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(Theme.SPACING_M, Theme.SPACING_M, Theme.SPACING_M, Theme.SPACING_M)
        layout.setSpacing(Theme.SPACING_S)
        return layout
