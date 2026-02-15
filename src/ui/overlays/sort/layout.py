from PySide6.QtWidgets import QHBoxLayout, QStyle
from PySide6.QtCore import QSize
from src.ui.common.icon_button.logic import IconButton
from src.ui.common.card.logic import Card

class SortOverlayLayout:
    def setup_ui(self, widget: Card):
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.btn_sort = IconButton(
            icon=widget.style().standardIcon(QStyle.SP_FileDialogDetailedView),
            tooltip="Sort Options",
            circular=True
        )
        # Increase icon size to fill more of the 36x36 button
        self.btn_sort.setIconSize(QSize(30, 30))
        
        layout.addWidget(self.btn_sort)
        return layout
