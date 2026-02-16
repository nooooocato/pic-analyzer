from PySide6.QtWidgets import QHBoxLayout, QWidget
from qfluentwidgets import FluentIcon, ToolButton
from PySide6.QtCore import QSize

class SelectionOverlayLayout:
    def setup_ui(self, widget):
        """Sets up the UI. 'widget' is expected to be a FlyoutView."""
        # Create a container for the action buttons
        self.container = QWidget()
        layout = QHBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Select All Button
        self.btn_all = ToolButton(FluentIcon.CHECKBOX, self.container)
        self.btn_all.setFixedSize(32, 32)
        self.btn_all.setIconSize(QSize(20, 20))
        self.btn_all.setToolTip("Select All")
        
        # Invert Selection Button
        self.btn_invert = ToolButton(FluentIcon.SYNC, self.container)
        self.btn_invert.setFixedSize(32, 32)
        self.btn_invert.setIconSize(QSize(20, 20))
        self.btn_invert.setToolTip("Invert Selection")
        
        # Cancel Button
        self.btn_cancel = ToolButton(FluentIcon.CANCEL, self.container)
        self.btn_cancel.setFixedSize(32, 32)
        self.btn_cancel.setIconSize(QSize(20, 20))
        self.btn_cancel.setToolTip("Cancel")
        
        layout.addWidget(self.btn_all)
        layout.addWidget(self.btn_invert)
        layout.addWidget(self.btn_cancel)
        
        # Add the container to the FlyoutView
        widget.addWidget(self.container)
        
        return layout
