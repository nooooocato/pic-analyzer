from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy
from PySide6.QtCore import Qt, Signal

class CollapsibleSection(QWidget):
    toggled = Signal(bool)

    def __init__(self, title, content_widget, header_widget=None, parent=None):
        super().__init__(parent)
        self._raw_title = title
        self.content_widget = content_widget
        self.is_expanded = True
        
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Header
        self.header_container = QWidget()
        self.header_layout = QHBoxLayout(self.header_container)
        self.header_layout.setContentsMargins(4, 0, 4, 0) # Give it some space
        self.header_layout.setSpacing(5)
        
        # Header toggle button
        self.toggle_button = QPushButton()
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(True)
        self.toggle_button.toggled.connect(self._on_toggled)
        self.toggle_button.setStyleSheet("text-align: left; border: none; padding-left: 0px;")
        self.toggle_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self._update_header_text()
        
        self.header_layout.addWidget(self.toggle_button)

        if header_widget:
            self.header_layout.addWidget(header_widget)
        
        self.main_layout.addWidget(self.header_container)
        self.main_layout.addWidget(self.content_widget)
        
    def _update_header_text(self):
        indicator = "▼" if self.is_expanded else "▶"
        self.toggle_button.setText(f"{indicator} {self._raw_title}")

    @property
    def title(self):
        return self._raw_title

    def _on_toggled(self, checked):
        self.is_expanded = checked
        self.content_widget.setVisible(checked)
        self._update_header_text()
        self.updateGeometry()
        self.toggled.emit(checked)

    def toggle(self):
        """Manually toggle the expansion state."""
        self.toggle_button.toggle()
