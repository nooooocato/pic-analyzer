from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QSize

class IconButtonLayout:
    def setup_ui(self, widget: QPushButton, size: int = 36, icon_size: int = 24):
        widget.setFixedSize(size, size)
        widget.setIconSize(QSize(icon_size, icon_size))
