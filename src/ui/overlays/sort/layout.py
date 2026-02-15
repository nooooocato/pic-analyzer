from PySide6.QtWidgets import QHBoxLayout, QStyle
from src.ui.common.icon_button.logic import IconButton
from src.ui.common.card.logic import Card

class SortOverlayLayout:
    def setup_ui(self, widget: Card):
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.btn_sort = IconButton(
            icon=widget.style().standardIcon(QStyle.SP_TitleBarMenuButton),
            tooltip="Sort Options",
            circular=True
        )
        
        layout.addWidget(self.btn_sort)
        return layout
