from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QLabel, QFrame
from PySide6.QtCore import Qt, Signal

class PluginItemWrapper(QFrame):
    removed = Signal()
    toggled = Signal(bool)

    def __init__(self, content, title="Plugin Item", parent=None):
        super().__init__(parent)
        self.content = content
        self.title = title
        
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.setObjectName("PluginItemWrapper")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.setSpacing(5)
        
        # Drag handle
        self.drag_handle = QLabel("⠿")
        self.drag_handle.setObjectName("drag_handle")
        self.drag_handle.setCursor(Qt.SizeAllCursor)
        header_layout.addWidget(self.drag_handle)
        
        # Toggle checkbox
        self.enabled_cb = QCheckBox()
        self.enabled_cb.setChecked(True)
        self.enabled_cb.toggled.connect(self.toggled.emit)
        header_layout.addWidget(self.enabled_cb)
        
        # Title
        self.title_label = QLabel(title)
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        
        # Remove button
        self.remove_btn = QPushButton("✕")
        self.remove_btn.setObjectName("remove_btn")
        self.remove_btn.setFixedSize(20, 20)
        self.remove_btn.clicked.connect(self.removed.emit)
        header_layout.addWidget(self.remove_btn)
        
        layout.addLayout(header_layout)
        
        # Content
        layout.addWidget(content)
        
        # Auto-hide content when disabled? 
        # Actually, let's keep it visible but maybe grayed out or just rely on the 'enabled' state.
        # Requirement says "enable or disable it without removing".
        self.toggled.connect(self._on_toggled)

    def _on_toggled(self, checked):
        self.content.setEnabled(checked)
