from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QLabel, QFrame
from PySide6.QtCore import Qt, Signal, QMimeData
from PySide6.QtGui import QDrag, QPixmap

class PluginItemWrapper(QFrame):
    removed = Signal()
    toggled = Signal(bool)
    reordered = Signal()

    def __init__(self, content, title="Plugin Item", parent=None):
        super().__init__(parent)
        self.content = content
        self.title = title
        
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setObjectName("PluginItemWrapper")
        # Ensure it has a solid background to see it during drag
        self.setAutoFillBackground(True)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(2, 2, 2, 2)
        header_layout.setSpacing(4)
        
        # Drag handle
        self.drag_handle = QLabel("⠿")
        self.drag_handle.setObjectName("drag_handle")
        self.drag_handle.setCursor(Qt.SizeAllCursor)
        self.drag_handle.setToolTip("Drag to reorder")
        header_layout.addWidget(self.drag_handle)
        
        # Toggle checkbox
        self.enabled_cb = QCheckBox()
        self.enabled_cb.setChecked(True)
        self.enabled_cb.toggled.connect(self.toggled.emit)
        header_layout.addWidget(self.enabled_cb)
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-size: 10px; font-weight: bold; color: #ccc;")
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        
        # Remove button
        self.remove_btn = QPushButton("✕")
        self.remove_btn.setObjectName("remove_btn")
        self.remove_btn.setFixedSize(22, 22)
        self.remove_btn.clicked.connect(self.removed.emit)
        header_layout.addWidget(self.remove_btn)
        
        layout.addLayout(header_layout)
        
        # Content
        layout.addWidget(content)
        
        self.toggled.connect(self._on_toggled)
        self._drag_start_pos = None

    def _on_toggled(self, checked):
        self.content.setEnabled(checked)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.drag_handle.underMouse():
            self._drag_start_pos = event.pos()
        else:
            self._drag_start_pos = None
            super().mousePressEvent(event)
            
    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton) or self._drag_start_pos is None:
            super().mouseMoveEvent(event)
            return
            
        if (event.pos() - self._drag_start_pos).manhattanLength() < 5:
            return
            
        drag = QDrag(self)
        mime = QMimeData()
        # We use a custom pointer to the widget itself for internal drag/drop
        mime.setData("application/x-plugin-item", b"")
        drag.setMimeData(mime)
        
        # Create a preview
        pixmap = self.grab()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        
        # Hide while dragging
        self.hide()
        result = drag.exec_(Qt.MoveAction)
        if result == Qt.IgnoreAction:
            self.show()
