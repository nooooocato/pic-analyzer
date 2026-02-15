from PySide6.QtWidgets import QHBoxLayout
from qfluentwidgets import FluentIcon
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
            FluentIcon.CHECKBOX,
            tooltip="Select All"
        )
        
        # Invert Selection Button
        self.btn_invert = IconButton(
            FluentIcon.SYNC,
            tooltip="Invert Selection"
        )
        
        # Cancel Button
        self.btn_cancel = IconButton(
            FluentIcon.CANCEL,
            tooltip="Cancel"
        )
        
        layout.addWidget(self.btn_all)
        layout.addWidget(self.btn_invert)
        layout.addWidget(self.btn_cancel)
        
        return layout
