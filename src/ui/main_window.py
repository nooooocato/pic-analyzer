from PySide6.QtWidgets import (
    QMainWindow, QToolBar, QTreeView, QDockWidget, 
    QVBoxLayout, QWidget, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, QThreadPool
import os
import sqlite3
from PySide6.QtGui import QStandardItemModel, QStandardItem
from src.file_scanner import FolderScanner
from src.database import DatabaseManager
from src.file_ops import hide_file
from src.ui.gallery_view import GalleryView
import logging

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pic-Analyzer")
        self.resize(1200, 800)

        # Initialize Database in app's local dir (or current dir for now)
        db_path = "app_metadata.db"
        self.db_manager = DatabaseManager(db_path)
        hide_file(db_path)
        
        self.current_folder = None
        self.active_scanners = []
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
        self.gallery.item_clicked.connect(self._on_item_selected)
        self.setCentralWidget(self.gallery)

    def update_inspector(self, metadata: dict):
        """Populates the Data Inspector with image metadata."""
        import datetime
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Property", "Value"])
        
        for key, value in metadata.items():
            display_value = str(value)
            if "Modified" in key or "timestamp" in key.lower():
                try:
                    dt = datetime.datetime.fromtimestamp(float(value))
                    display_value = dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    pass
                    
            key_item = QStandardItem(str(key))
            value_item = QStandardItem(display_value)
            model.appendRow([key_item, value_item])
            
        self.tree_view.setModel(model)
        self.tree_view.expandAll()

    def _on_open_folder(self):
        """Triggered when File > Open Folder is selected."""
        logger.info("Open Folder action triggered")
        if self.current_folder:
            logger.debug(f"Current folder active: {self.current_folder}, prompting user")
            reply = QMessageBox.question(
                self, "Switch Workspace",
                f"A folder is already open: {self.current_folder}\n"
                "Do you want to close it and open a new one?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.No:
                logger.info("User cancelled folder switch")
                return

        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Scan")
        if folder:
            logger.info(f"User selected folder: {folder}")
            self.current_folder = folder
            self._start_scan(folder)
        else:
            logger.info("User cancelled folder selection")

    def _start_scan(self, path):
        """Starts a background scan of the selected folder."""
        logger.info(f"Starting scan for path: {path}")
        # Clear UI state
        self.gallery.clear()

        # Switch database to the selected folder
        db_path = os.path.join(path, ".pic_analyzer.db")
        self.db_manager.switch_database(db_path)
        hide_file(db_path)

        scanner = FolderScanner(path, db_path)
        scanner.signals.file_found.connect(self._on_file_found)
        scanner.signals.error.connect(self._on_scanner_error)
        scanner.signals.finished.connect(lambda s=scanner: self._on_scan_finished(s))
        
        self.active_scanners.append(scanner)
        QThreadPool.globalInstance().start(scanner)

    def _on_item_selected(self, file_path):
        """Triggered when an image is clicked in the gallery."""
        logger.info(f"Item selected: {file_path}")
        
        if not os.path.exists(file_path):
            logger.warning(f"File not found: {file_path}")
            return

        # Basic File Metadata
        stats = os.stat(file_path)
        metadata = {
            "Filename": os.path.basename(file_path),
            "Path": file_path,
            "Size": f"{stats.st_size / 1024:.2f} KB",
            "Modified": os.path.getmtime(file_path),
        }

        # Try to get more info from DB
        try:
            conn = sqlite3.connect(self.db_manager.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM images WHERE path = ?", (file_path,))
            row = cursor.fetchone()
            if row:
                img_id = row[0]
                metadata["DB ID"] = img_id
                
                # Fetch analysis results if any
                cursor.execute("SELECT plugin_name, result_key, result_value FROM analysis_results WHERE image_id = ?", (img_id,))
                for plugin, key, val in cursor.fetchall():
                    metadata[f"{plugin}:{key}"] = val
            conn.close()
        except Exception as e:
            logger.error(f"Error fetching DB metadata: {e}")

        self.update_inspector(metadata)

    def _on_scan_finished(self, scanner):
        logger.info("Scan finished successfully")
        if scanner in self.active_scanners:
            self.active_scanners.remove(scanner)

    def _on_file_found(self, file_path, thumb_bytes):
        """Callback when a file is found by the scanner."""
        logger.debug(f"File found signal received for: {file_path}")
        self.gallery.add_item(file_path, thumb_bytes)

    def _on_scanner_error(self, error_msg):
        logger.error(f"Scanner error: {error_msg}")
        # Cleanup
        # We need the scanner object to remove it, but error signal only sends msg.
        # For simplicity, we'll just clear the list if it's one at a time, 
        # but let's just log for now.
        QMessageBox.critical(self, "Scanner Error", f"An error occurred during scan:\n{error_msg}")
