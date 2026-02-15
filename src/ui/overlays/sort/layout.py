from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtCore import QSize
from qfluentwidgets import FluentIcon
from src.ui.common.icon_button.logic import IconButton
from src.ui.common.card.logic import Card

class SortOverlayLayout:
    def setup_ui(self, widget: Card):
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.btn_sort = IconButton(
            FluentIcon.FILTER,
            tooltip="Sort Options"
        )
        
        # Increase icon size slightly if needed, but default is usually fine for Fluent
        # self.btn_sort.setIconSize(QSize(20, 20)) 
        
        layout.addWidget(self.btn_sort)
        return layout
