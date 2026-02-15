from PySide6.QtWidgets import QHBoxLayout, QStyle
from PySide6.QtCore import Qt
from src.ui.common.icon_button.logic import IconButton
from src.ui.common.card.logic import Card

class SelectionOverlayLayout:
    def setup_ui(self, widget: Card):
        # Change Card's default vertical layout to horizontal for the overlay
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Select All Button
        self.btn_all = IconButton(
            icon=widget.style().standardIcon(QStyle.SP_DialogApplyButton),
            tooltip="Select All"
        )
        
        # Invert Selection Button
        self.btn_invert = IconButton(
            icon=widget.style().standardIcon(QStyle.SP_BrowserReload),
            tooltip="Invert Selection"
        )
        
        # Cancel Button
        self.btn_cancel = IconButton(
            icon=widget.style().standardIcon(QStyle.SP_DialogCancelButton),
            tooltip="Cancel"
        )
        
        layout.addWidget(self.btn_all)
        layout.addWidget(self.btn_invert)
        layout.addWidget(self.btn_cancel)
        
        return layout
