from PySide6.QtWidgets import (
    QMainWindow, QToolBar, QTreeView, QDockWidget, QMenuBar
)
from PySide6.QtCore import Qt
from src.ui.gallery.logic import GalleryView
from src.ui.image_viewer.logic import ImageViewer
from src.ui.overlays.selection.logic import SelectionOverlay
from src.ui.overlays.data_inspector.logic import DataInspector
from src.ui.sidebar import SidebarContainer

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
        
        # Sidebar Dock (Left)
        self.sidebar_dock = QDockWidget("Rules", window)
        self.sidebar = SidebarContainer()
        self.sidebar_dock.setWidget(self.sidebar)
        window.addDockWidget(Qt.LeftDockWidgetArea, self.sidebar_dock)
        
        # Inspector Dock
        self.inspector_dock = QDockWidget("Data Inspector", window)
        self.data_inspector = DataInspector()
        self.inspector_dock.setWidget(self.data_inspector)
        window.addDockWidget(Qt.RightDockWidgetArea, self.inspector_dock)
        
        # Central Gallery
        self.gallery = GalleryView()
        window.setCentralWidget(self.gallery)
        
        # Overlays (Children of Gallery for floating effect)
        self.image_viewer = ImageViewer(self.gallery)
        self.selection_overlay = SelectionOverlay(self.gallery)
        self.selection_overlay.hide()

    def update_overlay_positions(self, window: QMainWindow):
        margin = 15
        if hasattr(self, "selection_overlay"):
            self.selection_overlay.move(margin, margin)
            self.selection_overlay.raise_()
        
        if hasattr(self, "image_viewer"):
            self.image_viewer.resize(self.gallery.size())
