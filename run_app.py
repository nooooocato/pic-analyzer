import sys
from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

app = QApplication(sys.argv)
window = MainWindow()
# Populate some dummy items in the gallery
for i in range(10):
    window.gallery.add_item(f"Image {i+1}")
window.show()
window.update_inspector({
    "Format": "JPEG",
    "Resolution": "1920x1080",
    "Analysis Status": "Complete"
})
sys.exit(app.exec())