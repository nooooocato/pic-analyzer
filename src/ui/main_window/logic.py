import sys
import os
import sqlite3
import datetime
import logging
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QApplication, QStyleFactory, QMenu
from PySide6.QtCore import Qt, QThreadPool, QPoint, QEvent
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPixmap, QAction, QCursor

from src.app.state import state
from src.app.communicator import Communicator
from src.app.file_scanner import FolderScanner
from src.app.file_ops import hide_file
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
        
        # Ensure app state is initialized (if not already by main.py)
        if not state.initialized:
            state.initialize()
            
        # UI Setup
        self.layout_engine = MainWindowLayout()
        self.layout_engine.setup_ui(self)
        self.setStyleSheet(get_style())
        
        # Toast
        self.toast = Toast("", parent=self)
        
        # Backward compatibility aliases for plugins/tests
        self.plugin_manager = state.plugin_manager
        self._sort_plugins = list(state.plugin_manager.sort_plugins.values())
        
        # Initialize Sort Overlay (needs db from state)
        self.layout_engine.sort_overlay = SortOverlay(state.db_manager, self.layout_engine.gallery)
        self.layout_engine.sort_overlay.sortRequested.connect(self._on_sort_requested)
        self.layout_engine.sort_overlay.show()
        
        # Set overlays on gallery for repositioning
        self.layout_engine.gallery.set_overlays(
            self.layout_engine.selection_overlay,
            self.layout_engine.sort_overlay,
            self.layout_engine.image_viewer
        )
        
        self._setup_connections()
        self._setup_menus()

        # Initialize UI for all discovered plugins
        for plugin in state.plugin_manager.plugins.values():
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
                direction = "next" if new_index > state.current_viewer_index else "prev"
                l.image_viewer.switch_image(file_path, direction)
            else:
                l.image_viewer.show_image(file_path)
            state.current_viewer_index = new_index
            self._on_item_selected(file_path)

    def _on_next_image(self):
        l = self.layout_engine
        new_index = state.current_viewer_index + 1
        if new_index < l.gallery.count():
            self._open_image_viewer(l.gallery._visible_items[new_index]['path'])
        else:
            Communicator().notify.emit("Wrapped to first image", "INFO")
            self._open_image_viewer(l.gallery._visible_items[0]['path'])

    def _on_prev_image(self):
        l = self.layout_engine
        new_index = state.current_viewer_index - 1
        if new_index >= 0:
            self._open_image_viewer(l.gallery._visible_items[new_index]['path'])
        else:
            Communicator().notify.emit("Wrapped to last image", "INFO")
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
        plugin = state.plugin_manager.sort_plugins.get(plugin_name)
        if plugin:
            self._apply_sort(metric, plugin)

    def _apply_sort(self, metric, plugin):
        values = state.db_manager.get_metric_values(metric)
        self.layout_engine.gallery.apply_sort(metric, plugin, values)

    def _on_item_selected(self, file_path: str):
        """Notify the system that an image has been selected."""
        if os.path.exists(file_path):
            Communicator().image_selected.emit(file_path)

    # _update_inspector is now handled by the DataInspector widget itself via signals

    def _on_open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Scan")
        if folder:
            state.set_current_folder(folder)
            self._start_scan(folder)

    def _start_scan(self, path: str):
        # Cancel previous scanners
        for scanner in state.active_scanners:
            scanner.cancel()
        state.active_scanners.clear()
        
        self.layout_engine.gallery.clear()
        db_path = os.path.join(path, ".pic_analyzer.db")
        state.db_manager.switch_database(db_path)
        hide_file(db_path)
        scanner = FolderScanner(path, db_path)
        scanner.signals.file_found.connect(self.layout_engine.gallery.add_item)
        state.active_scanners.append(scanner)
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
