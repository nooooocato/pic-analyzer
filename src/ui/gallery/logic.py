from PySide6.QtWidgets import QScrollArea, QListWidgetItem, QMenu, QLabel, QWidget
from PySide6.QtCore import Qt, QSize, Signal, QTimer
from PySide6.QtGui import QPixmap, QIcon
from .layout import GalleryLayout, GroupedListWidget as BaseGroupedListWidget
from .style import get_gallery_style

class GroupedListWidget(BaseGroupedListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._selection_mode_enabled = False
        self.itemSelectionChanged.connect(self._sync_selection_and_checkstate)
        
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
            if parent_gallery and parent_gallery.selection_mode_enabled:
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
        if parent_gallery and not parent_gallery.selection_mode_enabled:
            parent_gallery.set_selection_mode_enabled(True)
            if self._pressed_item:
                self._pressed_item.setSelected(True)

    def _show_context_menu(self, pos):
        parent_gallery = self._find_parent_gallery()
        if not parent_gallery: return
        
        from src.ui.theme import Theme
        menu = QMenu(self)
        menu.setStyleSheet(Theme.get_menu_qss())
        
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
            if isinstance(p, GalleryView): return p
            p = p.parent()
        return None

    def _sync_selection_and_checkstate(self):
        if not self._selection_mode_enabled: return
        self.blockSignals(True)
        for i in range(self.count()):
            item = self.item(i)
            item.setCheckState(Qt.Checked if item.isSelected() else Qt.Unchecked)
        self.blockSignals(False)
        self.viewport().update()

    @property
    def selection_mode_enabled(self):
        return self._selection_mode_enabled

    def set_selection_mode_enabled(self, enabled):
        self._selection_mode_enabled = enabled
        self.setSelectionMode(BaseGroupedListWidget.MultiSelection if enabled else BaseGroupedListWidget.ExtendedSelection)
        for i in range(self.count()):
            item = self.item(i)
            if enabled: item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            else: item.setFlags(item.flags() & ~Qt.ItemIsUserCheckable)
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

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout_engine = GalleryLayout()
        self.layout_engine.setup_ui(self)
        self.setStyleSheet(get_gallery_style())
        
        self._items = []
        self._visible_items = []
        self._selection_mode_enabled = False
        self._group_widgets = []
        self._current_plugin = None
        self._current_granularity = "month"
        self._show_stats = False
        self._current_sort_plugin = None
        self._current_sort_metric = None
        
        # Overlays
        self.selection_overlay = None
        self.sort_overlay = None
        self.image_viewer = None

    def set_overlays(self, selection, sort, viewer):
        self.selection_overlay = selection
        self.sort_overlay = sort
        self.image_viewer = viewer
        self._reposition_overlays()

    def _reposition_overlays(self):
        margin = 15
        if self.selection_overlay:
            self.selection_overlay.move(margin, margin)
            self.selection_overlay.raise_()
        
        if self.image_viewer:
            self.image_viewer.resize(self.size())

        if self.sort_overlay:
            # We need to ensure sort_overlay size is updated before positioning
            self.sort_overlay.adjustSize()
            x = self.width() - self.sort_overlay.width() - margin
            y = margin
            self.sort_overlay.move(x, y)
            self.sort_overlay.raise_()

    @property
    def selection_mode_enabled(self):
        return self._selection_mode_enabled

    def set_selection_mode_enabled(self, enabled):
        if self._selection_mode_enabled == enabled: return
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
        self._visible_items = []
        self._clear_layout()

    def _clear_layout(self):
        while self.layout_engine.container_layout.count() > 1:
            item = self.layout_engine.container_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        self._group_widgets = []

    def add_item(self, file_path, thumb_bytes=None):
        self._items.append({'path': file_path, 'thumb': thumb_bytes})
        self.refresh_view()

    def set_grouping(self, plugin, granularity="month"):
        self._current_plugin = plugin
        self._current_granularity = granularity
        self.refresh_view()

    def set_show_stats(self, enabled):
        self._show_stats = enabled
        self.refresh_view()

    def apply_sort(self, metric, plugin, values_map):
        self._current_sort_plugin = plugin
        self._current_sort_metric = metric
        for item in self._items:
            item[metric] = values_map.get(item['path'], 0)
        self._items = plugin.sort(self._items, metric)
        self.refresh_view()

    def refresh_view(self):
        self._clear_layout()
        self._visible_items = []
        if not self._current_plugin:
            self._create_group("All Images", self._items)
        else:
            groups = {}
            for item in self._items:
                res = self._current_plugin.run(item['path'], self._current_granularity)
                group_name = res.get('date', 'Unknown')
                groups.setdefault(group_name, []).append(item)
            
            for group_name in sorted(groups.keys(), reverse=True):
                self._create_group(group_name, groups[group_name])

    def _create_group(self, title, items):
        group_container, group_layout = self.layout_engine.create_group_container(title)
        
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
        # Only emit activated signal if NOT in selection mode
        list_widget.itemDoubleClicked.connect(
            lambda it: self.item_activated.emit(it.data(Qt.UserRole)) if not self.selection_mode_enabled else None
        )
        
        group_layout.addWidget(list_widget)
        self._visible_items.extend(items)
        
        if self._show_stats and self._current_sort_plugin and self._current_sort_metric:
            stats = self._current_sort_plugin.get_stats(items, self._current_sort_metric)
            if stats:
                stats_str = " | ".join([f"{k.upper()}: {v:.2f}" for k, v in stats.items()])
                label = QLabel(f"Group Statistics: {stats_str}")
                label.setStyleSheet("color: #666; font-style: italic; padding-top: 5px;")
                label.setAlignment(Qt.AlignRight)
                group_layout.addWidget(label)

        self.layout_engine.container_layout.insertWidget(self.layout_engine.container_layout.count() - 1, group_container)
        self._group_widgets.append(list_widget)
        QTimer.singleShot(0, list_widget.adjust_height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        for group in self._group_widgets:
            group.adjust_height()
        self._reposition_overlays()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and self._selection_mode_enabled:
            self.set_selection_mode_enabled(False)
            return # Consume the event
        super().keyPressEvent(event)

    def count(self): return len(self._visible_items)
