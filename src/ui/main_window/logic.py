from qfluentwidgets import FluentWindow, FluentIcon, NavigationItemPosition
from PySide6.QtCore import Qt, QThreadPool, QEvent
from PySide6.QtGui import QStandardItemModel, QStandardItem, QAction
from PySide6.QtWidgets import QFileDialog, QWidget, QVBoxLayout

import os
import datetime
import logging

from src.file_scanner import FolderScanner
from src.database import DatabaseManager
from src.file_ops import hide_file
from src.plugins.date_grouping import DateGroupingPlugin
from src.plugins.sort.manager import SortPluginManager
from src.ui.overlays.sort.logic import SortOverlay
from src.ui.common.toast.logic import Toast
from src.ui.gallery.logic import GalleryView
from src.ui.image_viewer.logic import ImageViewer
from src.ui.overlays.selection.logic import SelectionOverlay

from .layout import MainWindowLayout
from .style import get_style

logger = logging.getLogger(__name__)

class MainWindow(FluentWindow):
    """The main application window for Pic-Analyzer using Fluent Design."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pic-Analyzer")
        
        # Backend Managers
        db_path = "app_metadata.db"
        self.db_manager = DatabaseManager(db_path)
        hide_file(db_path)
        self.sort_manager = SortPluginManager()
        
        # UI Setup
        # FluentWindow handles title bar and navigation. 
        self.gallery = GalleryView(self)
        self.gallery.setObjectName("galleryInterface")
        self.addSubInterface(self.gallery, FluentIcon.PHOTO, 'Gallery')
        
        # Overlays
        self.image_viewer = ImageViewer(self.gallery)
        self.selection_overlay = SelectionOverlay(self.gallery)
        self.selection_overlay.hide()
        
        # Initialize Sort Overlay
        self.sort_overlay = SortOverlay(self.sort_manager, self.gallery)
        self.sort_overlay.sortRequested.connect(self._on_sort_requested)
        
        # Set overlays on gallery for repositioning
        self.gallery.set_overlays(
            self.selection_overlay,
            self.sort_overlay,
            self.image_viewer
        )
        
        # Toast
        self.toast = Toast("", parent=self)
        
        self.layout_engine = MainWindowLayout()
        self.tree_view = self.layout_engine.tree_view
        
        # Add Inspector to navigation
        self.inspector_widget = QWidget()
        self.inspector_widget.setObjectName("inspectorInterface")
        inspector_layout = QVBoxLayout(self.inspector_widget)
        inspector_layout.addWidget(self.tree_view)
        self.addSubInterface(self.inspector_widget, FluentIcon.INFO, 'Inspector', NavigationItemPosition.BOTTOM)

        # App State
        self.current_folder = None
        self.active_scanners = []
        self._current_viewer_index = -1
        
        self._setup_connections()
        self._setup_menus()
        
        self.setStyleSheet(get_style())

    def _setup_connections(self):
        self.gallery.item_selected.connect(self._on_item_selected)
        self.gallery.item_activated.connect(self._open_image_viewer)
        self.gallery.selection_mode_changed.connect(self.selection_overlay.setVisible)
        
        self.image_viewer.next_requested.connect(self._on_next_image)
        self.image_viewer.prev_requested.connect(self._on_prev_image)
        
        self.selection_overlay.selectAllRequested.connect(self._on_select_all)
        self.selection_overlay.invertSelectionRequested.connect(self._on_invert_selection)
        self.selection_overlay.cancelRequested.connect(self._on_cancel_selection)

    def _setup_menus(self):
        self.navigationInterface.addItem(
            routeKey='openFolder',
            icon=FluentIcon.FOLDER,
            text='Open Folder',
            onClick=self._on_open_folder,
            position=NavigationItemPosition.BOTTOM
        )

    def _open_image_viewer(self, file_path: str):
        new_index = -1
        for i in range(len(self.gallery._visible_items)):
            if self.gallery._visible_items[i]['path'] == file_path:
                new_index = i
                break
        
        if new_index != -1:
            if self.image_viewer.isVisible():
                direction = "next" if new_index > self._current_viewer_index else "prev"
                self.image_viewer.switch_image(file_path, direction)
            else:
                self.image_viewer.show_image(file_path)
            self._current_viewer_index = new_index
            self._on_item_selected(file_path)

    def _on_next_image(self):
        new_index = self._current_viewer_index + 1
        if new_index < self.gallery.count():
            self._open_image_viewer(self.gallery._visible_items[new_index]['path'])
        else:
            self.toast.show_message("Wrapped to first image", reference_widget=self.image_viewer)
            self._open_image_viewer(self.gallery._visible_items[0]['path'])

    def _on_prev_image(self):
        new_index = self._current_viewer_index - 1
        if new_index >= 0:
            self._open_image_viewer(self.gallery._visible_items[new_index]['path'])
        else:
            self.toast.show_message("Wrapped to last image", reference_widget=self.image_viewer)
            self._open_image_viewer(self.gallery._visible_items[self.gallery.count()-1]['path'])

    def _on_select_all(self):
        for group in self.gallery._group_widgets:
            for i in range(group.count()):
                group.item(i).setSelected(True)

    def _on_invert_selection(self):
        for group in self.gallery._group_widgets:
            for i in range(group.count()):
                item = group.item(i)
                item.setSelected(not item.isSelected())

    def _on_cancel_selection(self):
        self.gallery.set_selection_mode_enabled(False)

    def _on_sort_requested(self, plugin_name):
        pass

    def _on_item_selected(self, file_path: str):
        if not os.path.exists(file_path): return
        stats = os.stat(file_path)
        metadata = {
            "Filename": os.path.basename(file_path),
            "Path": file_path,
            "Size": f"{stats.st_size / 1024:.2f} KB",
            "Modified": stats.st_mtime,
        }
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
        self.tree_view.setModel(model)
        self.tree_view.expandAll()

    def _on_open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Scan")
        if folder:
            self.current_folder = folder
            self._start_scan(folder)

    def _start_scan(self, path: str):
        self.gallery.clear()
        db_path = os.path.join(path, ".pic_analyzer.db")
        self.db_manager.switch_database(db_path)
        hide_file(db_path)
        scanner = FolderScanner(path, db_path)
        scanner.signals.file_found.connect(self.gallery.add_item)
        self.active_scanners.append(scanner)
        QThreadPool.globalInstance().start(scanner)
