import sys
import os
import sqlite3
import datetime
import logging
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QApplication, QStyleFactory, QMenu
from PySide6.QtCore import Qt, QThreadPool, QPoint, QEvent
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPixmap, QAction, QCursor

from src.file_scanner import FolderScanner
from src.database import DatabaseManager
from src.file_ops import hide_file
from src.plugin_manager import PluginManager
from src.ui.overlays.sort.logic import SortOverlay
from src.ui.common.toast.logic import Toast

from .layout import MainWindowLayout
from .style import get_style

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    """The main application window for Pic-Analyzer."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pic-Analyzer")
        
        # Backend Managers
        db_path = "app_metadata.db"
        self.db_manager = DatabaseManager(db_path)
        hide_file(db_path)
        self._sort_plugins = []
        
        # UI Setup
        self.layout_engine = MainWindowLayout()
        self.layout_engine.setup_ui(self)
        self.setStyleSheet(get_style())
        
        # Toast
        self.toast = Toast("", parent=self)
        
        # Initialize Sort Overlay (needs db)
        self.layout_engine.sort_overlay = SortOverlay(self.db_manager, self.layout_engine.gallery)
        self.layout_engine.sort_overlay.sortRequested.connect(self._on_sort_requested)
        self.layout_engine.sort_overlay.show()
        
        # Set overlays on gallery for repositioning
        self.layout_engine.gallery.set_overlays(
            self.layout_engine.selection_overlay,
            self.layout_engine.sort_overlay,
            self.layout_engine.image_viewer
        )
        
        # App State
        self.current_folder = None
        self.active_scanners = []
        self._current_viewer_index = -1
        
        self._setup_connections()
        self._setup_menus()

        # New Plugin System
        self.plugin_manager = PluginManager("plugins")
        for plugin in self.plugin_manager.plugins.values():
            try:
                plugin.initialize_ui(self)
            except Exception as e:
                logger.error(f"Failed to initialize UI for plugin {plugin.name}: {e}")

    def event(self, event):
        if event.type() == QEvent.PaletteChange:
            # System theme changed, update styles that depend on it
            self.setStyleSheet(get_style())
            if hasattr(self.layout_engine, "gallery"):
                self.layout_engine.gallery.setStyleSheet(self.layout_engine.gallery.styleSheet())
        return super().event(event)

    def _setup_connections(self):
        l = self.layout_engine
        l.gallery.item_selected.connect(self._on_item_selected)
        l.gallery.item_activated.connect(self._open_image_viewer)
        l.gallery.selection_mode_changed.connect(l.selection_overlay.setVisible)
        
        l.image_viewer.next_requested.connect(self._on_next_image)
        l.image_viewer.prev_requested.connect(self._on_prev_image)
        
        l.selection_overlay.selectAllRequested.connect(self._on_select_all)
        l.selection_overlay.invertSelectionRequested.connect(self._on_invert_selection)
        l.selection_overlay.cancelRequested.connect(self._on_cancel_selection)

    def _setup_menus(self):
        l = self.layout_engine
        self._menu_cache = {
            "File": l.file_menu,
            "View": l.view_menu
        }
        
        # File Menu
        self.open_folder_action = l.file_menu.addAction("&Open Folder")
        self.open_folder_action.setShortcut("Ctrl+O")
        self.open_folder_action.triggered.connect(self._on_open_folder)
        
        # View Menu
        self.group_menu = l.view_menu.addMenu("Group By")
        self._menu_cache["View/Group By"] = self.group_menu
        self.group_menu.addAction("None").triggered.connect(lambda: l.gallery.set_grouping(None))
        
        l.view_menu.addSeparator()
        self.show_stats_action = l.view_menu.addAction("Show Sorting Stats")
        self.show_stats_action.setCheckable(True)
        self.show_stats_action.triggered.connect(l.gallery.set_show_stats)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Positioning is now handled by l.gallery.resizeEvent

    def _open_image_viewer(self, file_path: str):
        l = self.layout_engine
        new_index = -1
        # Use visible items for correct ordering
        for i in range(len(l.gallery._visible_items)):
            if l.gallery._visible_items[i]['path'] == file_path:
                new_index = i
                break
        
        if new_index != -1:
            if l.image_viewer.isVisible():
                direction = "next" if new_index > self._current_viewer_index else "prev"
                l.image_viewer.switch_image(file_path, direction)
            else:
                l.image_viewer.show_image(file_path)
            self._current_viewer_index = new_index
            self._on_item_selected(file_path)

    def _on_next_image(self):
        l = self.layout_engine
        new_index = self._current_viewer_index + 1
        if new_index < l.gallery.count():
            self._open_image_viewer(l.gallery._visible_items[new_index]['path'])
        else:
            self.toast.show_message("Wrapped to first image", reference_widget=l.image_viewer)
            self._open_image_viewer(l.gallery._visible_items[0]['path'])

    def _on_prev_image(self):
        l = self.layout_engine
        new_index = self._current_viewer_index - 1
        if new_index >= 0:
            self._open_image_viewer(l.gallery._visible_items[new_index]['path'])
        else:
            self.toast.show_message("Wrapped to last image", reference_widget=l.image_viewer)
            self._open_image_viewer(l.gallery._visible_items[l.gallery.count()-1]['path'])

    def _on_select_all(self):
        for group in self.layout_engine.gallery._group_widgets:
            for i in range(group.count()):
                group.item(i).setSelected(True)

    def _on_invert_selection(self):
        for group in self.layout_engine.gallery._group_widgets:
            for i in range(group.count()):
                item = group.item(i)
                item.setSelected(not item.isSelected())

    def _on_cancel_selection(self):
        self.layout_engine.gallery.set_selection_mode_enabled(False)

    def _on_sort_requested(self, metric, plugin_name):
        plugin = next((p for p in self._sort_plugins if p.name == plugin_name), None)
        if plugin:
            self._apply_sort(metric, plugin)

    def _apply_sort(self, metric, plugin):
        values = self.db_manager.get_metric_values(metric)
        self.layout_engine.gallery.apply_sort(metric, plugin, values)

    def _on_item_selected(self, file_path: str):
        if not os.path.exists(file_path): return
        
        # Try to get metadata from database
        metadata = self.db_manager.get_image_metadata(file_path)
        
        if not metadata:
            # Fallback to filesystem
            stats = os.stat(file_path)
            metadata = {
                "Filename": os.path.basename(file_path),
                "Path": file_path,
                "Size": f"{stats.st_size / 1024:.2f} KB",
                "Modified": stats.st_mtime,
            }
        else:
            metadata["Path"] = file_path
            
        self._update_inspector(metadata)

    def _update_inspector(self, metadata: dict):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Property", "Value"])
        for key, value in metadata.items():
            display_value = str(value)
            if "Modified" in key or "timestamp" in key.lower():
                try:
                    dt = datetime.datetime.fromtimestamp(float(value))
                    display_value = dt.strftime("%Y-%m-%d %H:%M:%S")
                except: pass
            model.appendRow([QStandardItem(str(key)), QStandardItem(display_value)])
        self.layout_engine.tree_view.setModel(model)
        self.layout_engine.tree_view.expandAll()

    def _on_open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Scan")
        if folder:
            self.current_folder = folder
            self._start_scan(folder)

    def _start_scan(self, path: str):
        self.layout_engine.gallery.clear()
        db_path = os.path.join(path, ".pic_analyzer.db")
        self.db_manager.switch_database(db_path)
        hide_file(db_path)
        scanner = FolderScanner(path, db_path)
        scanner.signals.file_found.connect(self.layout_engine.gallery.add_item)
        self.active_scanners.append(scanner)
        QThreadPool.globalInstance().start(scanner)

    # Plugin Hooks
    def get_menu(self, path: str) -> QMenu:
        """
        Returns an existing menu by its path (e.g., 'View/Group By') or creates it.
        Uses a cache to ensure stability.
        """
        if not hasattr(self, "_menu_cache"):
            self._menu_cache = {}
        
        path = path.strip("/")
        if path in self._menu_cache:
            return self._menu_cache[path]
        
        parts = path.split("/")
        parent = self.menuBar()
        current_path = ""
        
        for part in parts:
            current_path = f"{current_path}/{part}" if current_path else part
            if current_path in self._menu_cache:
                parent = self._menu_cache[current_path]
                continue
            
            found_menu = None
            # Search in current parent's actions
            for action in parent.actions():
                if action.menu():
                    title = action.menu().title().replace("&", "")
                    if title.lower() == part.lower():
                        found_menu = action.menu()
                        break
            
            if not found_menu:
                found_menu = parent.addMenu(f"&{part}")
            
            self._menu_cache[current_path] = found_menu
            parent = found_menu
        
        return self._menu_cache[path]

    def add_toolbar_action(self, action: QAction):
        """
        Adds an action to the main toolbar.
        """
        self.layout_engine.toolbar.addAction(action)

    def register_sort_plugin(self, plugin):
        """
        Registers a sorting plugin to be used in the SortOverlay.
        """
        self._sort_plugins.append(plugin)
        # Update SortOverlay if it exists
        if self.layout_engine.sort_overlay:
            self.layout_engine.sort_overlay.add_external_plugin(plugin)
