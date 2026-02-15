from qfluentwidgets import TransparentToolButton, FluentIcon
from PySide6.QtWidgets import QWidget

class IconButton(TransparentToolButton):
    def __init__(self, icon: FluentIcon, tooltip: str = "", parent: QWidget = None):
        super().__init__(parent)
        self.setIcon(icon)
        
        if tooltip:
            self.setToolTip(tooltip)
        
        # Consistent sizing (optional, can be adjusted)
        self.setFixedSize(36, 36)
        self.setIconSize(self.iconSize()) # Use default or set custom
