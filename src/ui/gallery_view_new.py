from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, 
    QListView, QScrollArea, QFrame, QApplication
)
from PySide6.QtCore import Qt, QSize, Signal, QTimer, QPoint
from PySide6.QtGui import QIcon, QPixmap, QColor, QFont
import logging
from .gallery_view import GalleryItemDelegate # Re-use the existing delegate

logger = logging.getLogger(__name__)

class GroupedListWidget(QListWidget):
    """A specialized QListWidget for a single group in the gallery."""
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
        self.setStyleSheet("background: transparent; outline: none;")
        self.setItemDelegate(GalleryItemDelegate(self))
        self.setFocusPolicy(Qt.NoFocus)

    def adjust_height(self):
        """Adjusts the widget height based on the number of items and current width."""
        if self.count() == 0:
            self.setFixedHeight(0)
            return
            
        width = self.width() if self.width() > 0 else 800
        items_per_row = max(1, width // 150)
        rows = (self.count() + items_per_row - 1) // items_per_row
        self.setFixedHeight(rows * 150 + 10)

class GalleryView(QScrollArea):
    """
    A scrollable gallery that supports true grouping with full-width headers.
    """
    item_selected = Signal(str)
    item_activated = Signal(str)
    selection_mode_changed = Signal(bool)

    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet("QScrollArea { background-color: white; }")
        
        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(20)
        self.layout.addStretch()
        
        self.setWidget(self.container)
        
        self._items = [] # Store raw data: {'path': str, 'thumb': bytes}
        self._selection_mode_enabled = False
        self._group_widgets = [] # Keep track of group widgets

    @property
    def selection_mode_enabled(self):
        return self._selection_mode_enabled

    def set_selection_mode_enabled(self, enabled):
        self._selection_mode_enabled = enabled
        for group in self._group_widgets:
            group.list_widget.set_selection_mode_enabled(enabled)
        self.selection_mode_changed.emit(enabled)

    def clear(self):
        """Clears all items and groups."""
        self._items = []
        self._clear_layout()

    def _clear_layout(self):
        """Removes all group widgets from the layout."""
        while self.layout.count() > 1: # Keep the stretch
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._group_widgets = []

    def add_item(self, file_path, thumb_bytes):
        """Adds a raw item and refreshes the view."""
        self._items.append({'path': file_path, 'thumb': thumb_bytes})
        # For performance in MVP, we refresh the whole view on new items 
        # In a real app, we'd append to the existing 'None' group or active group
        self.refresh_view()

    def set_grouping(self, plugin, granularity="month"):
        self._current_plugin = plugin
        self._current_granularity = granularity
        self.refresh_view()

    def refresh_view(self):
        """Rebuilds the UI based on current items and grouping settings."""
        self._clear_layout()
        
        if not hasattr(self, '_current_plugin') or not self._current_plugin:
            # Simple single group
            self._create_group("All Images", self._items)
        else:
            # Group items
            groups = {}
            for item in self._items:
                res = self._current_plugin.run(item['path'], self._current_granularity)
                group_name = res.get('date', 'Unknown')
                if group_name not in groups:
                    groups[group_name] = []
                groups[group_name].append(item)
            
            # Sort keys descending
            for group_name in sorted(groups.keys(), reverse=True):
                self._create_group(group_name, groups[group_name])

    def _create_group(self, title, items):
        group_container = QWidget()
        group_layout = QVBoxLayout(group_container)
        group_layout.setContentsMargins(0, 0, 0, 0)
        group_layout.setSpacing(5)
        
        header = QLabel(title)
        font = QFont()
        font.setBold(True)
        font.setPointSize(12)
        header.setFont(font)
        header.setStyleSheet("color: #333; padding-bottom: 5px; border-bottom: 1px solid #ddd;")
        
        list_widget = GroupedListWidget()
        for item_data in items:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, item_data['path'])
            if item_data['thumb']:
                pixmap = QPixmap()
                if pixmap.loadFromData(item_data['thumb']):
                    item.setIcon(QIcon(pixmap))
            list_widget.addItem(item)
        
        # Connect signals
        list_widget.itemClicked.connect(lambda it: self.item_selected.emit(it.data(Qt.UserRole)))
        list_widget.itemDoubleClicked.connect(lambda it: self.item_activated.emit(it.data(Qt.UserRole)))
        
        group_layout.addWidget(header)
        group_layout.addWidget(list_widget)
        
        # Add to main layout before the stretch
        self.layout.insertWidget(self.layout.count() - 1, group_container)
        self._group_widgets.append(list_widget)
        
        # Initial height adjustment
        QTimer.singleShot(0, list_widget.adjust_height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        for group in self._group_widgets:
            group.adjust_height()

    def count(self):
        return len(self._items)

    def item(self, index):
        # This is a bit of a hack to maintain compatibility with MainWindow's index-based access
        # In a real app, we'd refactor MainWindow to use the internal _items list
        class MockItem:
            def __init__(self, data): self.data_map = data
            def data(self, role): return self.data_map['path'] if role == Qt.UserRole else None
        
        if 0 <= index < len(self._items):
            return MockItem(self._items[index])
        return None
