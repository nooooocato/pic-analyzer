
from PySide6.QtWidgets import QListWidget, QListView, QMenu
from PySide6.QtCore import Qt, QSize, Signal, QTimer
from .gallery_item_delegate import GalleryItemDelegate

class GroupedListWidget(QListWidget):
    """Internal widget for grouped list items in the gallery."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)
        self.setMovement(QListView.Static)
        self.setSpacing(2)
        self.setIconSize(QSize(148, 148))
        self.setGridSize(QSize(150, 150))
        self.setFrameShape(QListWidget.NoFrame)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.setItemDelegate(GalleryItemDelegate(self))
        self.setFocusPolicy(Qt.NoFocus)
        
        self._selection_mode_enabled = False
        self.selectionModel().selectionChanged.connect(self._on_selection_changed)
        
        # Long press support
        self._long_press_timer = QTimer()
        self._long_press_timer.setSingleShot(True)
        self._long_press_timer.setInterval(800)
        self._long_press_timer.timeout.connect(self._on_long_press)
        self._pressed_item = None
        
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            parent_gallery = self._find_parent_gallery()
            if parent_gallery and hasattr(parent_gallery, 'selection_mode_enabled') and parent_gallery.selection_mode_enabled:
                parent_gallery.set_selection_mode_enabled(False)
                return
        super().keyPressEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._pressed_item = self.itemAt(event.pos())
            if self._pressed_item:
                self._long_press_timer.start()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self._long_press_timer.stop()
        super().mouseReleaseEvent(event)

    def _on_long_press(self):
        parent_gallery = self._find_parent_gallery()
        if parent_gallery and hasattr(parent_gallery, 'selection_mode_enabled') and not parent_gallery.selection_mode_enabled:
            parent_gallery.set_selection_mode_enabled(True)
            if self._pressed_item:
                self._pressed_item.setSelected(True)

    def _show_context_menu(self, pos):
        parent_gallery = self._find_parent_gallery()
        if not parent_gallery: return
        
        from src.ui.theme import Theme
        menu = QMenu(self)
        menu.setStyleSheet(Theme.get_menu_qss())
        
        if hasattr(parent_gallery, 'selection_mode_enabled') and not parent_gallery.selection_mode_enabled:
            act = menu.addAction("Select")
            act.triggered.connect(lambda: parent_gallery.set_selection_mode_enabled(True))
        
        item = self.itemAt(pos)
        if item:
            act = menu.addAction("Open")
            if hasattr(parent_gallery, 'item_activated'):
                act.triggered.connect(lambda: parent_gallery.item_activated.emit(item.data(Qt.UserRole)))
            
        if not menu.isEmpty():
            menu.exec(self.mapToGlobal(pos))

    def _find_parent_gallery(self):
        # We search for the parent that manages this widget, which will be GalleryLayout
        p = self.parent()
        while p:
            # We will use GalleryLayout as the parent class in the future
            # For now, let's keep searching until we find someone with the expected API
            if hasattr(p, 'selection_mode_enabled') and hasattr(p, 'set_selection_mode_enabled'):
                return p
            p = p.parent()
        return None

    def _on_selection_changed(self, selected, deselected):
        if not self._selection_mode_enabled: return
        self.blockSignals(True)
        for index in selected.indexes():
            item = self.item(index.row())
            if item: item.setCheckState(Qt.Checked)
        for index in deselected.indexes():
            item = self.item(index.row())
            if item: item.setCheckState(Qt.Unchecked)
        self.blockSignals(False)
        self.viewport().update()

    @property
    def selection_mode_enabled(self):
        return self._selection_mode_enabled

    def set_selection_mode_enabled(self, enabled):
        self._selection_mode_enabled = enabled
        self.setSelectionMode(QListWidget.MultiSelection if enabled else QListWidget.ExtendedSelection)
        for i in range(self.count()):
            item = self.item(i)
            if enabled: item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            else: item.setFlags(item.flags() & ~Qt.ItemIsUserCheckable)
        self.viewport().update()

    def adjust_height(self):
        try:
            if self.count() == 0:
                self.setFixedHeight(0)
                return
            width = self.width() if self.width() > 150 else 800
            items_per_row = max(1, width // 150)
            rows = (self.count() + items_per_row - 1) // items_per_row
            self.setFixedHeight(rows * 150 + 10)
        except RuntimeError:
            # Widget might be deleted already
            pass
