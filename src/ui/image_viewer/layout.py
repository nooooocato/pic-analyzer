from qfluentwidgets import ToolButton, FluentIcon
from PySide6.QtWidgets import QLabel, QFrame
from PySide6.QtCore import Qt, QSize

class ImageViewerLayout:
    def setup_ui(self, widget: QFrame):
        widget.setObjectName("ImageViewerOverlay")
        
        # Image Display Labels
        self.current_label = QLabel(widget)
        self.current_label.setAlignment(Qt.AlignCenter)
        
        self.next_label = QLabel(widget)
        self.next_label.setAlignment(Qt.AlignCenter)
        self.next_label.hide()
        
        # Navigation Buttons using Fluent Icons (Default colors to adapt to theme)
        self.btn_back = ToolButton(FluentIcon.PAGE_LEFT, widget)
        self.btn_back.setFixedSize(40, 40)
        self.btn_back.setIconSize(QSize(24, 24))
        self.btn_back.setObjectName("navButtonBack")
        
        self.btn_prev = ToolButton(FluentIcon.LEFT_ARROW, widget)
        self.btn_prev.setFixedSize(64, 64)
        self.btn_prev.setIconSize(QSize(32, 32))
        self.btn_prev.setObjectName("navButtonPrev")
        
        self.btn_next = ToolButton(FluentIcon.RIGHT_ARROW, widget)
        self.btn_next.setFixedSize(64, 64)
        self.btn_next.setIconSize(QSize(32, 32))
        self.btn_next.setObjectName("navButtonNext")

    def update_geometries(self, widget: QFrame):
        size = widget.size()
        self.current_label.setGeometry(0, 0, size.width(), size.height())
        
        margin = 20
        self.btn_back.move(margin, margin)
        btn_y = (size.height() - self.btn_prev.height()) // 2
        self.btn_prev.move(margin, btn_y)
        self.btn_next.move(size.width() - self.btn_next.width() - margin, btn_y)
