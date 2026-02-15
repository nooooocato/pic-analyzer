from PySide6.QtWidgets import (
    QMainWindow, QToolBar, QTreeView, QDockWidget,
    QVBoxLayout, QWidget, QFileDialog, QMessageBox,
    QPushButton, QHBoxLayout, QFrame, QStyle, QApplication
)
from PySide6.QtCore import Qt, QThreadPool, QSize, QPoint
import os
import sqlite3
import datetime
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon, QAction, QPixmap, QPalette, QColor
     
from src.file_scanner import FolderScanner
from src.database import DatabaseManager
from src.file_ops import hide_file
from src.ui.gallery_view import GalleryView
from src.ui.image_viewer import ImageViewer
from src.plugins.date_grouping import DateGroupingPlugin
from src.plugins.sort.manager import SortPluginManager
import logging

logger = logging.getLogger(__name__)

class SelectionOverlay(QFrame):
    """Floating overlay with batch actions for multi-selection mode."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("SelectionOverlay")
        self.setWindowFlags(Qt.SubWindow)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        button_style = """
            QPushButton {
                background-color: rgba(255, 255, 255, 200);
                border: 1px solid rgba(0, 0, 0, 80);
                border-radius: 4px;
                padding: 4px;
            }
            QPushButton:hover {
                background-color: rgba(0, 120, 212, 220);
                border: 1px solid #0078d4;
            }
        """
        
        self.btn_all = QPushButton()
        self.btn_all.setFixedSize(36, 36)
        self.btn_all.setToolTip("Select All")
        self.btn_all.setStyleSheet(button_style)
        
        self.btn_invert = QPushButton()
        self.btn_invert.setFixedSize(36, 36)
        self.btn_invert.setToolTip("Invert Selection")
        self.btn_invert.setStyleSheet(button_style)
        
        self.btn_cancel = QPushButton()
        self.btn_cancel.setFixedSize(36, 36)
        self.btn_cancel.setToolTip("Cancel")
        self.btn_cancel.setStyleSheet(button_style)
        
        layout.addWidget(self.btn_all)
        layout.addWidget(self.btn_invert)
        layout.addWidget(self.btn_cancel)
        
        self.btn_all.setIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton))     
        self.btn_invert.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))      
        self.btn_cancel.setIcon(self.style().standardIcon(QStyle.SP_DialogCancelButton)) 
        
        self.setStyleSheet("""
            #SelectionOverlay {
                background-color: rgba(245, 245, 245, 240);
                border-radius: 8px;
                border: 1px solid rgba(0, 0, 0, 80);
            }
        """)
        self.adjustSize()

class SortOverlay(QFrame):
    """Floating overlay for sorting selection."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("SortOverlay")
        self.setWindowFlags(Qt.SubWindow)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.btn_sort = QPushButton()
        self.btn_sort.setFixedSize(36, 36)
        self.btn_sort.setToolTip("Sort Options")
        self.btn_sort.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMenuButton))
        self.btn_sort.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 200);
                border: 1px solid rgba(0, 0, 0, 80);
                border-radius: 18px;
            }
            QPushButton:hover {
                background-color: rgba(0, 120, 212, 220);
            }
        """)
        
        layout.addWidget(self.btn_sort)
        
        self.setStyleSheet("""
            #SortOverlay {
                background-color: transparent;
            }
        """)
        self.adjustSize()

class MainWindow(QMainWindow):
    """The main application window for Pic-Analyzer."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pic-Analyzer")
        self.resize(1200, 800)

        # Initialize Database
        db_path = "app_metadata.db"
        self.db_manager = DatabaseManager(db_path)
        hide_file(db_path)
        
        self.sort_manager = SortPluginManager()
        self.current_folder = None
        self.active_scanners = []
        self._current_viewer_index = -1
        self._setup_ui()

    def _setup_ui(self):
        """Initializes and arranges UI components."""
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
        
        analyze_action = self.toolbar.addAction("Analyze")
        
        # Grouping Menu
        self.view_menu = self.menu_bar.addMenu("&View")
        self.group_menu = self.view_menu.addMenu("Group By")
        
        group_none_action = self.group_menu.addAction("None")
        group_none_action.triggered.connect(lambda: self.gallery.set_grouping(None))
        
        group_date_menu = self.group_menu.addMenu("Date")
        
        date_year_action = group_date_menu.addAction("Year")
        date_year_action.triggered.connect(lambda: self._on_group_by_date("year"))
        
        date_month_action = group_date_menu.addAction("Month")
        date_month_action.triggered.connect(lambda: self._on_group_by_date("month"))
        
        date_day_action = group_date_menu.addAction("Day")
        date_day_action.triggered.connect(lambda: self._on_group_by_date("day"))

        # Sidebar (Data Inspector)
        self.inspector_dock = QDockWidget("Data Inspector", self)
        self.inspector_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        
        self.tree_view = QTreeView()
        self.tree_view.setEditTriggers(QTreeView.NoEditTriggers)
        self.inspector_dock.setWidget(self.tree_view)
        self.addDockWidget(Qt.RightDockWidgetArea, self.inspector_dock)

        # Central Widget (Gallery)
        self.gallery = GalleryView()
        self.gallery.item_selected.connect(self._on_item_selected)
        self.gallery.item_activated.connect(self._open_image_viewer)
        self.setCentralWidget(self.gallery)

        # Image Viewer Overlay
        self.image_viewer = ImageViewer(self.gallery)
        self.image_viewer.next_requested.connect(self._on_next_image)
        self.image_viewer.prev_requested.connect(self._on_prev_image)

        # Selection Overlay (Context Sensitive)
        self.selection_overlay = SelectionOverlay(self.gallery)
        self.selection_overlay.setVisible(False)
        self.selection_overlay.btn_all.clicked.connect(self._on_select_all)
        self.selection_overlay.btn_invert.clicked.connect(self._on_invert_selection)     
        self.selection_overlay.btn_cancel.clicked.connect(self._on_cancel_selection)     
        self.gallery.selection_mode_changed.connect(self.selection_overlay.setVisible)   

        # Sort Overlay
        self.sort_overlay = SortOverlay(self.gallery)
        self.sort_overlay.btn_sort.clicked.connect(self._show_sort_menu)
        self.sort_overlay.show()

    def resizeEvent(self, event):
        """Maintains position of overlays on window resize."""
        super().resizeEvent(event)
        margin = 15
        
        if hasattr(self, "selection_overlay"):
            # Move to top-left
            self.selection_overlay.move(margin, margin)
            self.selection_overlay.raise_()
        
        if hasattr(self, "image_viewer"):
            self.image_viewer.resize(self.gallery.size())

        if hasattr(self, "sort_overlay"):
            # Keep at top-right
            x = self.gallery.width() - self.sort_overlay.width() - margin
            y = margin
            self.sort_overlay.move(x, y)
            self.sort_overlay.raise_()

    def _open_image_viewer(self, file_path: str):
        """Opens the full-screen image viewer for the specified file."""
        logger.info(f"Opening image viewer for: {file_path}")
        self._on_item_selected(file_path)
        
        new_index = -1
        for i in range(self.gallery.count()):
            if self.gallery.item(i).data(Qt.UserRole) == file_path:
                new_index = i
                break
        
        if new_index != -1:
            full_pixmap = QPixmap(file_path)
            if self.image_viewer.isVisible():
                direction = "next" if new_index > self._current_viewer_index else "prev" 
                self.image_viewer.switch_image(file_path, direction)
            else:
                self.image_viewer.show_image(file_path)
            self._current_viewer_index = new_index

    def _on_next_image(self):
        """Navigates to the next image in the gallery."""
        new_index = self._current_viewer_index + 1
        if new_index < self.gallery.count():
            item = self.gallery.item(new_index)
            self._open_image_viewer(item.data(Qt.UserRole))

    def _on_prev_image(self):
        """Navigates to the previous image in the gallery."""
        new_index = self._current_viewer_index - 1
        if new_index >= 0:
            item = self.gallery.item(new_index)
            self._open_image_viewer(item.data(Qt.UserRole))

    def _on_select_all(self):
        """Selects all items in the gallery."""
        for group in self.gallery._group_widgets:
            for i in range(group.count()):
                item = group.item(i)
                item.setCheckState(Qt.Checked)
                item.setSelected(True)

    def _on_invert_selection(self):
        """Inverts the current selection in the gallery."""
        for group in self.gallery._group_widgets:
            for i in range(group.count()):
                item = group.item(i)
                new_state = Qt.Unchecked if item.checkState() == Qt.Checked else Qt.Checked  
                item.setCheckState(new_state)
                item.setSelected(new_state == Qt.Checked)

    def _on_cancel_selection(self):
        """Exits multi-selection mode."""
        self.gallery.set_selection_mode_enabled(False)

    def _show_sort_menu(self):
        """Displays a menu to select sort metric and algorithm."""
        from PySide6.QtWidgets import QMenu
        from PySide6.QtGui import QAction
        
        menu = QMenu(self)
        menu.setAttribute(Qt.WA_TranslucentBackground, False)
        menu.setAutoFillBackground(True)
        
        metrics = self.db_manager.get_numeric_metrics()
        
        for metric in metrics:
            metric_menu = menu.addMenu(metric.replace("_", " ").title())
            for plugin_name, plugin in self.sort_manager.plugins.items():
                action = QAction(plugin_name, self)
                action.triggered.connect(lambda checked=False, m=metric, p=plugin: self._apply_sort(m, p))
                metric_menu.addAction(action)
        
        menu.exec(self.sort_overlay.btn_sort.mapToGlobal(QPoint(0, self.sort_overlay.btn_sort.height())))

    def _apply_sort(self, metric, plugin):
        """Applies the selected sorting plugin to the gallery."""
        logger.info(f"Applying sort: {plugin.name} on {metric}")
        values = self.db_manager.get_metric_values(metric)
        self.gallery.apply_sort(metric, plugin, values)

    def mousePressEvent(self, event):
        """Handles Mouse 4/5 for navigation and mode exit."""
        if event.button() == Qt.XButton1: # Mouse 4 (Back)
            if self.image_viewer.isVisible():
                self.image_viewer.close_viewer()
            elif self.gallery.selection_mode_enabled:
                self.selection_overlay.btn_cancel.click()
        elif event.button() == Qt.XButton2: # Mouse 5 (Forward)
            if not self.image_viewer.isVisible():
                item = self.gallery.itemAt(self.gallery.mapFromGlobal(QCursor.pos()))    
                if item:
                    self._open_image_viewer(item.data(Qt.UserRole))
        super().mousePressEvent(event)

    def keyPressEvent(self, event):
        """Handles global key events (Esc to exit modes)."""
        if event.key() == Qt.Key_Escape:
            if self.gallery.selection_mode_enabled:
                self.selection_overlay.btn_cancel.click()
                return
        super().keyPressEvent(event)

    def update_inspector(self, metadata: dict):
        """Populates the Data Inspector with image metadata."""
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
            reply = QMessageBox.question(
                self, "Switch Workspace",
                f"A folder is already open: {self.current_folder}\nDo you want to close it and open a new one?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.No:
                return

        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Scan")
        if folder:
            self.current_folder = folder
            self._start_scan(folder)

    def _start_scan(self, path: str):
        """Starts a background scan of the selected folder."""
        self.gallery.clear()
        db_path = os.path.join(path, ".pic_analyzer.db")
        self.db_manager.switch_database(db_path)
        hide_file(db_path)

        scanner = FolderScanner(path, db_path)
        scanner.signals.file_found.connect(self._on_file_found)
        scanner.signals.error.connect(self._on_scanner_error)
        scanner.signals.finished.connect(lambda s=scanner: self._on_scan_finished(s))
        self.active_scanners.append(scanner)
        QThreadPool.globalInstance().start(scanner)

    def _on_item_selected(self, file_path: str):
        """Triggered when an image is selected to update metadata."""
        if not os.path.exists(file_path):
            return

        stats = os.stat(file_path)
        metadata = {
            "Filename": os.path.basename(file_path),
            "Path": file_path,
            "Size": f"{stats.st_size / 1024:.2f} KB",
            "Modified": os.path.getmtime(file_path),
        }

        try:
            conn = sqlite3.connect(self.db_manager.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM images WHERE path = ?", (file_path,))
            row = cursor.fetchone()
            if row:
                img_id = row[0]
                metadata["DB ID"] = img_id
                cursor.execute("SELECT plugin_name, result_key, result_value FROM analysis_results WHERE image_id = ?", (img_id,))
                for plugin, key, val in cursor.fetchall():
                    metadata[f"{plugin}:{key}"] = val
            conn.close()
        except Exception as e:
            logger.error(f"Error fetching DB metadata: {e}")

        self.update_inspector(metadata)

    def _on_scan_finished(self, scanner: FolderScanner):
        """Cleanup after folder scan completes."""
        if scanner in self.active_scanners:
            self.active_scanners.remove(scanner)

    def _on_group_by_date(self, granularity="month"):
        """Groups gallery items by date using the DateGroupingPlugin."""
        plugin = DateGroupingPlugin()
        self.gallery.set_grouping(plugin, granularity)

    def _on_file_found(self, file_path: str, thumb_bytes: bytes):
        """Callback when a file is found by the scanner."""
        self.gallery.add_item(file_path, thumb_bytes)

    def _on_scanner_error(self, error_msg: str):
        """Displays error message if scanner fails."""
        logger.error(f"Scanner error: {error_msg}")
        QMessageBox.critical(self, "Scanner Error", f"An error occurred during scan:\n{error_msg}")
