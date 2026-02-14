from PySide6.QtWidgets import QScrollArea, QWidget, QGridLayout, QLabel, QFrame
from PySide6.QtCore import Qt, QSize

class GalleryItem(QFrame):
    def __init__(self, text="Thumbnail"):
        super().__init__()
        self.setFixedSize(150, 150)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        
        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignCenter)
        
        # In a real app, this would be a thumbnail image
        self.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")

class GalleryView(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        
        self.container = QWidget()
        self.layout = QGridLayout(self.container)
        self.layout.setSpacing(10)
        self.layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        self.setWidget(self.container)
        
    def add_item(self, text):
        item = GalleryItem(text)
        count = self.layout.count()
        columns = max(1, self.width() // 160)
        row = count // columns
        col = count % columns
        self.layout.addWidget(item, row, col)

    def clear(self):
        """Removes all items from the gallery."""
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
