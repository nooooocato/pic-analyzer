from PySide6.QtWidgets import QPushButton
from .style import get_style
from .layout import IconButtonLayout

class IconButton(QPushButton):
    def __init__(self, icon=None, tooltip="", circular=False, parent=None):
        super().__init__(parent)
        self.layout_engine = IconButtonLayout()
        self.layout_engine.setup_ui(self)
        
        if icon:
            self.setIcon(icon)
        if tooltip:
            self.setToolTip(tooltip)
            
        self.setStyleSheet(get_style(circular))
