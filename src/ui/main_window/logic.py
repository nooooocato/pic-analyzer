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
        
        # Set overlays on gallery for repositioning
        self.layout_engine.gallery.set_overlays(
            self.layout_engine.selection_overlay,
            None, # Sort Overlay removed
            self.layout_engine.image_viewer
        )
        
        self._setup_connections()
        self._setup_menus()

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
        
        Communicator().rules_updated.connect(self._on_rules_updated)

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

    def _on_rules_updated(self, rules: dict):
        self.layout_engine.gallery.set_rules(rules)

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
