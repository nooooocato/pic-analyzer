from PySide6.QtWidgets import (
    QMainWindow, QToolBar, QTreeView, QDockWidget, 
    QVBoxLayout, QWidget, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, QThreadPool
import os
from PySide6.QtGui import QStandardItemModel, QStandardItem
from src.ui.gallery_view import GalleryView
from src.file_scanner import FolderScanner
from src.database import DatabaseManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pic-Analyzer")
        self.resize(1200, 800)

        # Initialize Database in app's local dir (or current dir for now)
        self.db_manager = DatabaseManager("app_metadata.db")
        
        self.current_folder = None
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
        if self.current_folder:
            reply = QMessageBox.question(
                self, "Switch Workspace",
                f"A folder is already open: {self.current_folder}\n"
                "Do you want to close it and open a new one?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.No:
                return

        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Scan")
        if folder:
            self.current_folder = folder
            self._start_scan(folder)

    def _start_scan(self, path):
        """Starts a background scan of the selected folder."""
        # Clear UI state
        self.gallery.clear()

        # Switch database to the selected folder
        db_path = os.path.join(path, ".pic_analyzer.db")
        self.db_manager.switch_database(db_path)

        scanner = FolderScanner(path)
        scanner.signals.file_found.connect(self._on_file_found)
        QThreadPool.globalInstance().start(scanner)

    def _on_file_found(self, file_path):
        """Callback when a file is found by the scanner."""
        self.gallery.add_item(file_path)
