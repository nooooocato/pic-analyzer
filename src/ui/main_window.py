from PySide6.QtWidgets import QMainWindow, QToolBar, QTreeView, QDockWidget, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from src.ui.gallery_view import GalleryView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pic-Analyzer")
        self.resize(1200, 800)

        self._setup_ui()

    def _setup_ui(self):
        # Top Toolbar
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)
        self.toolbar.setMovable(False)
        self.toolbar.addAction("Import")
        self.toolbar.addAction("Analyze")

        # Sidebar (Data Inspector)
        self.inspector_dock = QDockWidget("Data Inspector", self)
        self.inspector_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        
        self.tree_view = QTreeView()
        self.inspector_dock.setWidget(self.tree_view)
        
        self.addDockWidget(Qt.RightDockWidgetArea, self.inspector_dock)

        # Central Widget (Gallery)
        self.gallery = GalleryView()
        self.setCentralWidget(self.gallery)
