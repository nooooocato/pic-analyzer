
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame, QLabel, QSizePolicy
from src.ui.theme import Theme

class GalleryLayoutUI:
    def setup_ui(self, widget: QScrollArea):
        widget.setWidgetResizable(True)
        widget.setFrameShape(QFrame.NoFrame)
        
        self.container = QWidget()
        self.container.setStyleSheet("background: transparent;")
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(10, 10, 10, 10)
        self.container_layout.setSpacing(Theme.SPACING_XL)
        self.container_layout.addStretch()
        
        widget.setWidget(self.container)

    def create_group_container(self, title: str):
        group_container = QWidget()
        group_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        group_layout = QVBoxLayout(group_container)
        group_layout.setContentsMargins(0, 0, 0, 0)
        group_layout.setSpacing(Theme.SPACING_S)
        
        header = QLabel(title)
        header.setObjectName("GroupHeader")
        header.setFixedHeight(22)
        group_layout.addWidget(header)
        
        return group_container, group_layout
