import sys
import os
import tempfile
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt, QBuffer, QIODevice
from PySide6.QtGui import QPixmap, QColor
from src.ui.gallery.logic import GalleryView
from src.ui.image_viewer.logic import ImageViewer
from src.ui.common.toast.logic import Toast
from src.ui.theme import Theme

class VerifyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Phase 3 UI Verification - Animated Colors & Toast")
        self.resize(1000, 700)
        self.setStyleSheet(f"QMainWindow {{ background-color: {Theme.BACKGROUND_LIGHT}; }}")
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Gallery View
        self.gallery = GalleryView()
        self.layout.addWidget(self.gallery)
        
        # Image Viewer (Overlay)
        self.viewer = ImageViewer(self)
        
        # Toast component
        self.toast = Toast("", parent=self)
        
        # 准备数据
        self.image_paths = []
        colors = [QColor("red"), QColor("green"), QColor("blue"), QColor("yellow"), 
                  QColor("cyan"), QColor("magenta"), QColor("orange"), QColor("purple"),
                  QColor("brown"), QColor("gray")]
        
        temp_dir = tempfile.gettempdir()
        
        for i, color in enumerate(colors):
            pixmap = QPixmap(800, 600)
            pixmap.fill(color)
            path = os.path.join(temp_dir, f"pic_analyzer_test_{i}.png")
            pixmap.save(path, "PNG")
            self.image_paths.append(path)
            
            thumb = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            buf = QBuffer()
            buf.open(QIODevice.WriteOnly)
            thumb.save(buf, "PNG")
            self.gallery.add_item(path, buf.data().data())
            
        self.current_index = 0
        
        # 连接信号
        self.gallery.item_activated.connect(self.open_image)
        self.viewer.next_requested.connect(self.show_next)
        self.viewer.prev_requested.connect(self.show_prev)

    def open_image(self, path):
        if path in self.image_paths:
            self.current_index = self.image_paths.index(path)
            self.viewer.show_image(path)

    def show_next(self):
        old_idx = self.current_index
        self.current_index = (self.current_index + 1) % len(self.image_paths)
        if self.current_index < old_idx:
            self.toast.show_message("Wrapped to first image")
        self.viewer.switch_image(self.image_paths[self.current_index], "next")

    def show_prev(self):
        old_idx = self.current_index
        self.current_index = (self.current_index - 1) % len(self.image_paths)
        if self.current_index > old_idx:
            self.toast.show_message("Wrapped to last image")
        self.viewer.switch_image(self.image_paths[self.current_index], "prev")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VerifyWindow()
    window.show()
    sys.exit(app.exec())
