import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QStyle
from PySide6.QtCore import Qt
from src.ui.common.icon_button.logic import IconButton
from src.ui.common.card.logic import Card
from src.ui.theme import Theme

class VerifyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Phase 1 UI Verification")
        self.setFixedSize(400, 300)
        self.setStyleSheet(f"QMainWindow {{ background-color: {Theme.BACKGROUND_LIGHT}; }}")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 创建一个 Card
        self.card = Card()
        layout.addWidget(self.card)
        
        # 在 Card 中添加一个居中的按钮
        icon = self.style().standardIcon(QStyle.SP_DialogApplyButton)
        self.btn = IconButton(icon=icon, tooltip="Fluent Button", circular=True)
        self.card.main_layout.addWidget(self.btn, 0, Qt.AlignCenter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VerifyWindow()
    window.show()
    sys.exit(app.exec())
