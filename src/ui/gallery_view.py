from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, 
    QListView, QScrollArea, QFrame, QApplication, QStyle, QStyledItemDelegate, QMenu
)
from PySide6.QtCore import Qt, QSize, Signal, QTimer, QPoint, QRect
from PySide6.QtGui import QIcon, QPixmap, QColor, QFont, QPen
import logging

logger = logging.getLogger(__name__)

class GalleryItemDelegate(QStyledItemDelegate):
    """Custom delegate for rendering gallery items with overlaid checkboxes."""
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        """Paints the item icon and selection checkbox."""
        self.initStyleOption(option, index)
        painter.save()
        
        # Draw background/selection border if selected or hovered
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, QColor(0, 120, 212, 60))
            pen = QPen(QColor(0, 120, 212), 2)
            painter.setPen(pen)
            painter.drawRect(option.rect.adjusted(1, 1, -1, -1))
        elif option.state & QStyle.State_MouseOver:
            painter.fillRect(option.rect, QColor(0, 120, 212, 30))
            pen = QPen(QColor(0, 120, 212, 100), 1)
            painter.setPen(pen)
            painter.drawRect(option.rect.adjusted(1, 1, -1, -1))

        # Draw Icon (Image)
        icon = index.data(Qt.DecorationRole)
        if icon:
            icon_rect = option.rect.adjusted(4, 4, -4, -4)
            icon.paint(painter, icon_rect, Qt.AlignCenter)

        # Draw Checkbox if in selection mode
        view = self.parent()
        if hasattr(view, "selection_mode_enabled") and view.selection_mode_enabled:
            is_checked = option.state & QStyle.State_Selected
            
            # Position checkbox at top-left with some margin
            cb_size = 22
            cb_rect = QRect(option.rect.left() + 8, option.rect.top() + 8, cb_size, cb_size)
            
            # Background for checkbox with subtle shadow/border
            painter.setPen(QPen(QColor(0, 0, 0, 60), 1))
            if is_checked:
                painter.setBrush(QColor(0, 120, 212))
            else:
                painter.setBrush(QColor(255, 255, 255, 220))
            
            painter.drawRoundedRect(cb_rect, 4, 4)
            
            # Draw Checkmark if checked
            if is_checked:
                painter.setPen(QPen(Qt.white, 2))
                # Simple checkmark lines
                p1 = QPoint(cb_rect.left() + 5, cb_rect.top() + 11)
                p2 = QPoint(cb_rect.left() + 9, cb_rect.top() + 15)
                p3 = QPoint(cb_rect.left() + 17, cb_rect.top() + 7)
                painter.drawLine(p1, p2)
                painter.drawLine(p2, p3)
        
        painter.restore()

    def sizeHint(self, option, index) -> QSize:
        return QSize(150, 150)

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
        self.setStyleSheet("GroupedListWidget { background: transparent; outline: none; }")
        self.setItemDelegate(GalleryItemDelegate(self))
        self.setFocusPolicy(Qt.NoFocus)
        self._selection_mode_enabled = False
        
        # Synchronize selection and check state
        self.itemSelectionChanged.connect(self._sync_selection_and_checkstate)

        # Long press support
        self._long_press_timer = QTimer()
        self._long_press_timer.setSingleShot(True)
        self._long_press_timer.setInterval(800)
        self._long_press_timer.timeout.connect(self._on_long_press)
        self._pressed_item = None
        
        # Context menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

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
        if parent_gallery and not parent_gallery.selection_mode_enabled:
            parent_gallery.set_selection_mode_enabled(True)
            if self._pressed_item:
                self._pressed_item.setSelected(True)

    def _show_context_menu(self, pos):
        parent_gallery = self._find_parent_gallery()
        if not parent_gallery: return
        
        menu = QMenu(self)
        menu.setAttribute(Qt.WA_TranslucentBackground, False)
        menu.setAutoFillBackground(True)
        
        if not parent_gallery.selection_mode_enabled:
            act = menu.addAction("Select")
            act.triggered.connect(lambda: parent_gallery.set_selection_mode_enabled(True))
        
        item = self.itemAt(pos)
        if item:
            act = menu.addAction("Open")
            act.triggered.connect(lambda: parent_gallery.item_activated.emit(item.data(Qt.UserRole)))
            
        if not menu.isEmpty():
            menu.exec(self.mapToGlobal(pos))

    def _find_parent_gallery(self):
        p = self.parent()
        while p:
            if isinstance(p, GalleryView):
                return p
            p = p.parent()
        return None

    def _sync_selection_and_checkstate(self):
        """Synchronizes checkbox check state with item selection state."""
        if not self._selection_mode_enabled:
            return
            
        # Temporarily block signals to avoid recursion
        self.blockSignals(True)
        for i in range(self.count()):
            item = self.item(i)
            is_sel = item.isSelected()
            expected_check = Qt.Checked if is_sel else Qt.Unchecked
            if item.checkState() != expected_check:
                item.setCheckState(expected_check)
        self.blockSignals(False)
        self.viewport().update()

    @property
    def selection_mode_enabled(self):
        return self._selection_mode_enabled

    def set_selection_mode_enabled(self, enabled):
        self._selection_mode_enabled = enabled
        self.setSelectionMode(QListWidget.MultiSelection if enabled else QListWidget.ExtendedSelection)
        self.viewport().update()

    def adjust_height(self):
        if self.count() == 0:
            self.setFixedHeight(0)
            return
        width = self.width() if self.width() > 150 else 800
        items_per_row = max(1, width // 150)
        rows = (self.count() + items_per_row - 1) // items_per_row
        self.setFixedHeight(rows * 150 + 10)

class GalleryView(QScrollArea):
    item_selected = Signal(str)
    item_activated = Signal(str)
    selection_mode_changed = Signal(bool)

    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        
        self.container = QWidget()
        self.container.setStyleSheet("background: transparent;")
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(10, 10, 10, 10)
        self.container_layout.setSpacing(20)
        self.container_layout.addStretch()
        
        self.setWidget(self.container)
        
        self._items = []
        self._selection_mode_enabled = False
        self._group_widgets = []
        self._current_plugin = None
        self._current_granularity = "month"

    @property
    def selection_mode_enabled(self):
        return self._selection_mode_enabled

    def set_selection_mode_enabled(self, enabled):
        if self._selection_mode_enabled == enabled:
            return
        self._selection_mode_enabled = enabled
        for group in self._group_widgets:
            group.set_selection_mode_enabled(enabled)
            if not enabled:
                group.clearSelection()
                for i in range(group.count()):
                    group.item(i).setCheckState(Qt.Unchecked)
        self.selection_mode_changed.emit(enabled)

    def clear(self):
        self._items = []
        self._clear_layout()

    def _clear_layout(self):
        while self.container_layout.count() > 1:
            item = self.container_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._group_widgets = []

    def add_item(self, file_path, thumb_bytes):
        self._items.append({'path': file_path, 'thumb': thumb_bytes})
        self.refresh_view()

    def set_grouping(self, plugin, granularity="month"):
        self._current_plugin = plugin
        self._current_granularity = granularity
        self.refresh_view()

    def apply_sort(self, metric, plugin, values_map):
        """
        Sorts all items using the provided plugin and metric, then refreshes the view.
        """
        # Inject values into items for sorting
        for item in self._items:
            item[metric] = values_map.get(item['path'], 0)
            
        self._items = plugin.sort(self._items, metric)
        self.refresh_view()

    def refresh_view(self):
        self._clear_layout()
        if not self._current_plugin:
            self._create_group("All Images", self._items)
        else:
            groups = {}
            for item in self._items:
                res = self._current_plugin.run(item['path'], self._current_granularity)
                group_name = res.get('date', 'Unknown')
                if group_name not in groups:
                    groups[group_name] = []
                groups[group_name].append(item)
            
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
        list_widget.set_selection_mode_enabled(self._selection_mode_enabled)
        for item_data in items:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, item_data['path'])
            if item_data['thumb']:
                pixmap = QPixmap()
                if pixmap.loadFromData(item_data['thumb']):
                    item.setIcon(QIcon(pixmap))
            list_widget.addItem(item)
        
        list_widget.itemClicked.connect(lambda it: self.item_selected.emit(it.data(Qt.UserRole)))
        list_widget.itemDoubleClicked.connect(lambda it: self.item_activated.emit(it.data(Qt.UserRole)))
        
        group_layout.addWidget(header)
        group_layout.addWidget(list_widget)
        
        self.container_layout.insertWidget(self.container_layout.count() - 1, group_container)
        self._group_widgets.append(list_widget)
        QTimer.singleShot(0, list_widget.adjust_height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        for group in self._group_widgets:
            group.adjust_height()

    def count(self):
        return len(self._items)

    def item(self, index):
        class MockItem:
            def __init__(self, data): self.data_map = data
            def data(self, role): return self.data_map['path'] if role == Qt.UserRole else None
        if 0 <= index < len(self._items):
            return MockItem(self._items[index])
        return None
