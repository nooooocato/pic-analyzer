from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from .collapsible import CollapsibleSection

class SidebarContainer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(250)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        # Grouping Section
        self.grouping_content = QWidget()
        self.grouping_layout = QVBoxLayout(self.grouping_content)
        self.grouping_section = CollapsibleSection("Grouping", self.grouping_content)
        
        # Filtering Section
        self.filtering_content = QWidget()
        self.filtering_layout = QVBoxLayout(self.filtering_content)
        self.filtering_section = CollapsibleSection("Filtering", self.filtering_content)
        
        # Sorting Section
        self.sorting_content = QWidget()
        self.sorting_layout = QVBoxLayout(self.sorting_content)
        self.sorting_section = CollapsibleSection("Sorting", self.sorting_content)
        
        layout.addWidget(self.grouping_section)
        layout.addWidget(self.filtering_section)
        layout.addWidget(self.sorting_section)
        layout.addStretch()
