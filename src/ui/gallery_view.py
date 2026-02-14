from PySide6.QtWidgets import QScrollArea, QWidget, QGridLayout, QLabel, QFrame, QVBoxLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap

class GalleryItem(QFrame):
    def __init__(self, text="Thumbnail", thumb_bytes=None):
        super().__init__()
        self.setFixedSize(160, 180) # Adjusted for label
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        
        layout = QVBoxLayout(self)
        
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(140, 140)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: #ddd;")
        
        if thumb_bytes:
            pixmap = QPixmap()
            if pixmap.loadFromData(thumb_bytes):
                # Scale pixmap to fit label while maintaining aspect ratio
                scaled_pixmap = pixmap.scaled(
                    self.image_label.size(), 
                    Qt.KeepAspectRatio, 
                    Qt.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_pixmap)
            else:
                self.image_label.setText("Error")
        else:
            self.image_label.setText("No Image")
            
        layout.addWidget(self.image_label)
        
        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignCenter)
        # Simple filename eliding if needed
        layout.addWidget(self.label)
        
        self.setStyleSheet("GalleryItem { border: 1px solid #ccc; background-color: #f9f9f9; }")

    def pixmap(self):
        return self.image_label.pixmap()

class GalleryView(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        
        self.container = QWidget()
        self.layout = QGridLayout(self.container)
        self.layout.setSpacing(10)
        self.layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        self.setWidget(self.container)
        
    def add_item(self, text, thumb_bytes=None):
        import os
        filename = os.path.basename(text)
        item = GalleryItem(filename, thumb_bytes)
        count = self.layout.count()
        columns = max(1, self.width() // 170)
        row = count // columns
        col = count % columns
        self.layout.addWidget(item, row, col)

    def clear(self):
        """Removes all items from the gallery."""
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
