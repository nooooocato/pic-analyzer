from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFrame
from PySide6.QtCore import Qt

class CollapsibleSection(QWidget):
    def __init__(self, title, content_widget, parent=None):
        super().__init__(parent)
        self.title = title
        self.content_widget = content_widget
        self.is_expanded = True
        
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Header button
        self.toggle_button = QPushButton(title)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(True)
        self.toggle_button.toggled.connect(self._on_toggled)
        
        self.main_layout.addWidget(self.toggle_button)
        self.main_layout.addWidget(self.content_widget)
        
    def _on_toggled(self, checked):
        self.is_expanded = checked
        self.content_widget.setVisible(checked)

    def toggle(self):
        """Manually toggle the expansion state."""
        self.toggle_button.toggle()
