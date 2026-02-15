from PySide6.QtWidgets import (
    QMainWindow, QToolBar, QTreeView, QDockWidget, QMenuBar
)
from PySide6.QtCore import Qt
from src.ui.gallery.logic import GalleryView
from src.ui.image_viewer.logic import ImageViewer
from src.ui.overlays.selection.logic import SelectionOverlay
from src.ui.overlays.sort.logic import SortOverlay

class MainWindowLayout:
    def setup_ui(self, window: QMainWindow):
        window.resize(1200, 800)
        
        # Menu Bar
        self.menu_bar = window.menuBar()
        self.file_menu = self.menu_bar.addMenu("&File")
        self.view_menu = self.menu_bar.addMenu("&View")
        
        # Toolbar
        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setMovable(False)
        window.addToolBar(self.toolbar)
        
        # Inspector Dock
        self.inspector_dock = QDockWidget("Data Inspector", window)
        self.tree_view = QTreeView()
        self.tree_view.setEditTriggers(QTreeView.NoEditTriggers)
        self.inspector_dock.setWidget(self.tree_view)
        window.addDockWidget(Qt.RightDockWidgetArea, self.inspector_dock)
        
        # Central Gallery
        self.gallery = GalleryView()
        window.setCentralWidget(self.gallery)
        
        # Overlays (Children of Gallery for floating effect)
        self.image_viewer = ImageViewer(self.gallery)
        self.selection_overlay = SelectionOverlay(self.gallery)
        self.selection_overlay.hide()
        
        # Sort Overlay needs a manager, which logic will provide later
        self.sort_overlay = None 

    def update_overlay_positions(self, window: QMainWindow):
        margin = 15
        if hasattr(self, "selection_overlay"):
            self.selection_overlay.move(margin, margin)
            self.selection_overlay.raise_()
        
        if hasattr(self, "image_viewer"):
            self.image_viewer.resize(self.gallery.size())

        if self.sort_overlay:
            x = self.gallery.width() - self.sort_overlay.width() - margin
            y = margin
            self.sort_overlay.move(x, y)
            self.sort_overlay.raise_()
