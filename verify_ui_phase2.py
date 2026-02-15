import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt
from src.ui.overlays.selection.logic import SelectionOverlay
from src.ui.overlays.sort.logic import SortOverlay
from src.ui.theme import Theme
from unittest.mock import MagicMock

class VerifyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Phase 2 UI Verification")
        self.setFixedSize(600, 400)
        self.setStyleSheet(f"QMainWindow {{ background-color: {Theme.BACKGROUND_LIGHT}; }}")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        layout.addWidget(QLabel("Selection Overlay (Card based):"))
        self.selection = SelectionOverlay(self)
        layout.addWidget(self.selection)
        
        layout.addSpacing(20)
        
        layout.addWidget(QLabel("Sort Overlay (Transparent):"))
        # Mock Sort Manager
        mock_manager = MagicMock()
        mock_manager.get_plugins.return_value = ["Date", "Name", "Size", "Type"]
        self.sort = SortOverlay(mock_manager, self)
        layout.addWidget(self.sort)
        
        # Connect signals to print to console
        self.selection.selectAllRequested.connect(lambda: print("Select All Requested"))
        self.selection.invertSelectionRequested.connect(lambda: print("Invert Selection Requested"))
        self.selection.cancelRequested.connect(lambda: print("Cancel Requested"))
        self.sort.sortRequested.connect(lambda p: print(f"Sort Requested: {p}"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VerifyWindow()
    window.show()
    sys.exit(app.exec())
