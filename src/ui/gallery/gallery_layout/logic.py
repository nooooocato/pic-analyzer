
from PySide6.QtWidgets import QScrollArea, QListWidgetItem, QWidget, QLabel
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QPixmap, QIcon
from src.ui.gallery.grouped_list.logic import GroupedListWidget
from src.ui.theme import Theme
from src.app.communicator import Communicator
from src.plugin.filter_engine import FilterEngine
from src.app.state import state
from .layout import GalleryLayoutUI
from .style import get_gallery_style

class GalleryLayout(QScrollArea):
    """Main container and orchestrator for the gallery component."""
    
    item_selected = Signal(str)
    item_activated = Signal(str)
    selection_mode_changed = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = GalleryLayoutUI()
        self.ui.setup_ui(self)
        self.setStyleSheet(get_gallery_style())
        
        self._items = []
        self._visible_items = []
        self._selection_mode_enabled = False
        self._group_widgets = []
        self._rules = {
            "group": {"plugin": None, "params": {}},
            "filter": {"plugin": None, "params": {}},
            "sort": {"plugin": None, "params": {}}
        }
        self._show_stats = False
        
        # Overlays (to be set by main_window)
        self.selection_overlay = None
        self.sort_overlay = None
        self.image_viewer = None
        
        Communicator().rules_updated.connect(self.set_rules)

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
        self.selection_mode_changed.emit(enabled)

    def clear(self):
        self._items = []
        self._visible_items = []
        self._clear_layout()

    def _clear_layout(self):
        while self.ui.container_layout.count() > 1:
            item = self.ui.container_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._group_widgets = []

    def add_item(self, item_data: dict):
        self._items.append(item_data)
        if not hasattr(self, "_refresh_timer"):
            self._refresh_timer = QTimer()
            self._refresh_timer.setSingleShot(True)
            self._refresh_timer.setInterval(50)
            self._refresh_timer.timeout.connect(self.refresh_view)
        
        if not self._refresh_timer.isActive():
            self._refresh_timer.start()

    def set_rules(self, rules: dict):
        self._rules = rules
        self.refresh_view()

    def set_show_stats(self, enabled):
        self._show_stats = enabled
        self.refresh_view()

    def refresh_view(self):
        self._clear_layout()
        items = list(self._items)
        
        # 1. Sequential Filters
        filters = self._rules.get("filters", [])
        if not filters and self._rules.get("filter"):
            filters = [self._rules["filter"]]
        items = FilterEngine().apply(items, filters)
            
        # 2. Sequential Sorts
        sorts = self._rules.get("sorts", [])
        if not sorts and self._rules.get("sort"):
            sorts = [self._rules["sort"]]
            
        metric_cache = {}
        for s in reversed(sorts):
            plugin = s.get("plugin")
            metric = s.get("metric")
            if plugin and metric:
                if metric not in metric_cache:
                    metric_cache[metric] = state.db_manager.get_metric_values(metric)
                values_map = metric_cache[metric]
                for it in items:
                    it[metric] = values_map.get(it['path'], 0)
                items = plugin.sort(items, metric, s.get("params", {}))
            
        self._visible_items = items
        
        # 3. Headers and Grouping Logic
        g_rule = self._rules.get("group", {})
        g_plugin = g_rule.get("plugin")
        
        filters_list = self._rules.get("filters", [])
        has_active_filter = any(f.get("type") == "plugin" and f.get("plugin") is not None for f in filters_list)
        if not has_active_filter and self._rules.get("filter") and self._rules["filter"].get("plugin"):
            has_active_filter = True

        if not g_plugin:
            title = "Filtered Images" if has_active_filter else "All Images"
            self._create_group(title, items)
        else:
            if has_active_filter:
                self._create_group("Filtered Images", [])
            groups = g_plugin.group(items, "", g_rule.get("params", {}))
            for name in sorted(groups.keys(), reverse=True):
                self._create_group(name, groups[name])

    def _create_group(self, title, items):
        group_container, group_layout = self.ui.create_group_container(title)
        
        list_widget = GroupedListWidget()
        list_widget.set_selection_mode_enabled(self._selection_mode_enabled)
        
        for item_data in items:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, item_data.get('path'))
            if item_data.get('thumb'):
                pixmap = QPixmap()
                if pixmap.loadFromData(item_data['thumb']):
                    item.setIcon(QIcon(pixmap))
            list_widget.addItem(item)
        
        list_widget.itemClicked.connect(lambda it: self.item_selected.emit(it.data(Qt.UserRole)))
        list_widget.itemDoubleClicked.connect(
            lambda it: self.item_activated.emit(it.data(Qt.UserRole))
            if not self.selection_mode_enabled else None
        )
        
        group_layout.addWidget(list_widget)
        
        s_rule = self._rules.get("sort", {})
        s_plugin = s_rule.get("plugin")
        s_metric = s_rule.get("metric")
        
        if self._show_stats and s_plugin and s_metric:
            if hasattr(s_plugin, "get_stats"):
                stats = s_plugin.get_stats(items, s_metric)
                if stats:
                    stats_str = " | ".join([f"{k.upper()}: {v:.2f}" for k, v in stats.items()])
                    label = QLabel(f"Group Statistics: {stats_str}")
                    label.setStyleSheet("color: #666; font-style: italic; padding-top: 5px;")
                    label.setAlignment(Qt.AlignRight)
                    group_layout.addWidget(label)

        self.ui.container_layout.insertWidget(self.ui.container_layout.count() - 1, group_container)
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
            return
        super().keyPressEvent(event)

    def count(self): return len(self._visible_items)
