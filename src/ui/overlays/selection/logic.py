from PySide6.QtCore import Signal
from qfluentwidgets import FlyoutView, FluentIcon
from .layout import SelectionOverlayLayout
from .style import get_style

class SelectionOverlay(FlyoutView):
    """Floating overlay for batch actions using FlyoutView style."""
    selectAllRequested = Signal()
    invertSelectionRequested = Signal()
    cancelRequested = Signal()

    def __init__(self, parent=None):
        super().__init__(
            title="Selection Mode",
            content="Manage selected items",
            icon=FluentIcon.CHECKBOX,
            isClosable=False,
            parent=parent
        )
        from PySide6.QtCore import Qt
        self.setWindowFlags(Qt.SubWindow)
        
        self.layout_engine = SelectionOverlayLayout()
        self.layout_engine.setup_ui(self)
        
        # Connect signals
        self.layout_engine.btn_all.clicked.connect(self.selectAllRequested.emit)
        self.layout_engine.btn_invert.clicked.connect(self.invertSelectionRequested.emit)
        self.layout_engine.btn_cancel.clicked.connect(self.cancelRequested.emit)
        
        # Apply additional styles if any
        custom_style = get_style()
        if custom_style:
            self.setStyleSheet(self.styleSheet() + custom_style)
            
        self.adjustSize()
