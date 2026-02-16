from qfluentwidgets import ListWidget
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame, QListView
)
from PySide6.QtCore import Qt, QSize
from src.ui.theme import Theme
from .style import GalleryItemDelegate

class GalleryLayout:
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
        group_layout = QVBoxLayout(group_container)
        group_layout.setContentsMargins(0, 0, 0, 0)
        group_layout.setSpacing(Theme.SPACING_S)
        
        header = QLabel(title)
        header.setObjectName("GroupHeader")
        group_layout.addWidget(header)
        
        return group_container, group_layout

class GroupedListWidget(ListWidget):
    """Internal widget for grouped list items using Fluent ListWidget."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)
        self.setMovement(QListView.Static)
        self.setSpacing(8)
        self.setIconSize(QSize(148, 148))
        self.setGridSize(QSize(160, 160)) # Slightly larger grid for margins
        self.setFrameShape(QFrame.NoFrame)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setSelectionMode(ListWidget.ExtendedSelection)
        self.setItemDelegate(GalleryItemDelegate(self))
        self.setFocusPolicy(Qt.NoFocus)
        
        # Transparent background for the list widget itself
        self.setStyleSheet("background: transparent; border: none;")
