from PySide6.QtWidgets import QHBoxLayout, QWidget
from qfluentwidgets import FluentIcon
from src.ui.common.icon_button.logic import IconButton

class SelectionOverlayLayout:
    def setup_ui(self, widget):
        """Sets up the UI. 'widget' is expected to be a FlyoutView."""
        # Create a container for the action buttons
        self.container = QWidget()
        layout = QHBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)
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
        
        # Add the container to the FlyoutView
        widget.addWidget(self.container)
        
        return layout
