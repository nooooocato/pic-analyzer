from PySide6.QtWidgets import QMainWindow, QToolBar, QTreeView, QDockWidget, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from src.ui.gallery_view import GalleryView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pic-Analyzer")
        self.resize(1200, 800)

        self._setup_ui()

    def _setup_ui(self):
        # Menu Bar
        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu("&File")
        
        self.open_folder_action = self.file_menu.addAction("&Open Folder")
        self.open_folder_action.setShortcut("Ctrl+O")
        self.open_folder_action.triggered.connect(self._on_open_folder)

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
        self.tree_view.setEditTriggers(QTreeView.NoEditTriggers)
        self.inspector_dock.setWidget(self.tree_view)
        
        self.addDockWidget(Qt.RightDockWidgetArea, self.inspector_dock)

        # Central Widget (Gallery)
        self.gallery = GalleryView()
        self.setCentralWidget(self.gallery)

    def update_inspector(self, metadata: dict):
        """Populates the Data Inspector with image metadata."""
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Property", "Value"])
        
        for key, value in metadata.items():
            key_item = QStandardItem(str(key))
            value_item = QStandardItem(str(value))
            model.appendRow([key_item, value_item])
            
        self.tree_view.setModel(model)
        self.tree_view.expandAll()

    def _on_open_folder(self):
        """Triggered when File > Open Folder is selected."""
        pass
