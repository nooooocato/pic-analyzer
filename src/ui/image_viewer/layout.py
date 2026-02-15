from PySide6.QtWidgets import QLabel, QPushButton, QFrame, QStyle
from PySide6.QtCore import Qt, QSize
from .style import IMAGE_VIEWER_BUTTON_STYLE

class ImageViewerLayout:
    def setup_ui(self, widget: QFrame):
        widget.setObjectName("ImageViewerOverlay")
        
        # Image Display Labels
        self.current_label = QLabel(widget)
        self.current_label.setAlignment(Qt.AlignCenter)
        
        self.next_label = QLabel(widget)
        self.next_label.setAlignment(Qt.AlignCenter)
        self.next_label.hide()
        
        # Navigation Buttons
        self.btn_back = QPushButton(widget)
        self.btn_back.setFixedSize(40, 40)
        self.btn_back.setIcon(widget.style().standardIcon(QStyle.SP_ArrowBack))
        self.btn_back.setStyleSheet(IMAGE_VIEWER_BUTTON_STYLE)
        
        self.btn_prev = QPushButton(widget)
        self.btn_prev.setFixedSize(60, 100)
        self.btn_prev.setIcon(widget.style().standardIcon(QStyle.SP_ArrowLeft))
        self.btn_prev.setIconSize(QSize(32, 32))
        self.btn_prev.setStyleSheet(IMAGE_VIEWER_BUTTON_STYLE)
        
        self.btn_next = QPushButton(widget)
        self.btn_next.setFixedSize(60, 100)
        self.btn_next.setIcon(widget.style().standardIcon(QStyle.SP_ArrowRight))
        self.btn_next.setIconSize(QSize(32, 32))
        self.btn_next.setStyleSheet(IMAGE_VIEWER_BUTTON_STYLE)

    def update_geometries(self, widget: QFrame):
        size = widget.size()
        self.current_label.setGeometry(0, 0, size.width(), size.height())
        
        margin = 20
        self.btn_back.move(margin, margin)
        btn_y = (size.height() - self.btn_prev.height()) // 2
        self.btn_prev.move(margin, btn_y)
        self.btn_next.move(size.width() - self.btn_next.width() - margin, btn_y)
