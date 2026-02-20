from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class SidebarContainer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(250) # Default width for sidebar
        
        layout = QVBoxLayout(self)
        
        # Initial sections as labels to pass the test
        self.grouping_label = QLabel("Grouping")
        self.filtering_label = QLabel("Filtering")
        self.sorting_label = QLabel("Sorting")
        
        layout.addWidget(self.grouping_label)
        layout.addWidget(self.filtering_label)
        layout.addWidget(self.sorting_label)
        layout.addStretch()
