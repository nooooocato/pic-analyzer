from PySide6.QtWidgets import QWidget, QSpinBox, QDoubleSpinBox, QLineEdit, QCheckBox, QComboBox, QVBoxLayout, QLabel
from PySide6.QtCore import QTimer, Qt
from src.app.state import state
from src.app.communicator import Communicator
from src.ui.common.widget_generator import WidgetGenerator
from src.ui.common.plugin_item import PluginItemWrapper
from .layout import SidebarLayout
from .style import get_style

class SidebarContainer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout_engine = SidebarLayout()
        self.layout_engine.setup_ui(self)
        self.setStyleSheet(get_style())
        
        self.setAcceptDrops(True) # Enable reordering
        
        self._setup_connections()
        self._populate_dropdowns()

    def _setup_connections(self):
        l = self.layout_engine
        l.group_combo.currentIndexChanged.connect(lambda: self._on_plugin_selected("group"))

        l.filtering_section.toggled.connect(self._reorder_and_apply)
        l.grouping_section.toggled.connect(self._reorder_and_apply)
        l.sorting_section.toggled.connect(self._reorder_and_apply)

        l.add_filter_btn.clicked.connect(lambda: self._add_plugin_item("filter"))
        l.add_sort_btn.clicked.connect(lambda: self._add_plugin_item("sort"))

    def _reorder_and_apply(self):
        # Trigger splitter handles management if needed
        self.layout_engine.update_splitter_handles()
        
        # Force QSplitter to shrink collapsed items
        l = self.layout_engine
        # Set sizes: expanded items take space, collapsed take 0
        sizes = [1 if s.is_expanded else 0 for s in l.all_sections]
        l.splitter.setSizes(sizes)

    def _on_plugin_selected(self, category):
        l = self.layout_engine
        if category == "group":
            combo, layout = l.group_combo, l.group_params_layout
        else:
            return

        # Clear existing dynamic widgets
        while layout.count() > 1: # Keep the combo
            item = layout.takeAt(1)
            w = item.widget()
            if w: w.deleteLater()

        plugin = combo.currentData()
        if plugin and hasattr(plugin, "schema"):
            for param in plugin.schema.get("parameters", []):
                w_container = WidgetGenerator.create_labeled_widget(param)
                self._connect_change_signal(w_container.input_widget)
                layout.addWidget(w_container)
        
        self._on_apply_clicked()

    def _populate_dropdowns(self):
        pm = state.plugin_manager
        l = self.layout_engine
        
        l.group_combo.blockSignals(True)
        l.group_combo.clear()
        l.group_combo.addItem("None", None)
        for name, plugin in pm.group_plugins.items():
            l.group_combo.addItem(name, plugin)
        l.group_combo.blockSignals(False)

    def _add_plugin_item(self, category):
        l = self.layout_engine
        pm = state.plugin_manager
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 5, 0, 5)
        
        combo = QComboBox()
        combo.addItem("Select Plugin...", None)
        plugins = pm.filter_plugins if category == "filter" else pm.sort_plugins
        for name, plugin in plugins.items():
            combo.addItem(name, plugin)
        content_layout.addWidget(combo)
        
        if category == "sort":
            content_layout.addWidget(QLabel("Metric:"))
            metric_combo = QComboBox()
            if state.db_manager:
                metrics = state.db_manager.get_numeric_metrics()
                for m in metrics:
                    metric_combo.addItem(m.replace("_", " ").title(), m)
            content_layout.addWidget(metric_combo)
            content_widget.metric_combo = metric_combo
            metric_combo.currentIndexChanged.connect(lambda: self._on_apply_clicked())

        content_widget.combo = combo
        content_widget.params_layout = QVBoxLayout()
        content_layout.addLayout(content_widget.params_layout)
        
        wrapper = PluginItemWrapper(content_widget, title=category.title())
        wrapper.removed.connect(lambda: self._remove_plugin_item(wrapper, category))
        wrapper.toggled.connect(lambda _: self._on_apply_clicked())
        
        combo.currentIndexChanged.connect(lambda: self._on_plugin_item_selected(wrapper, category))
        
        layout = l.filtering_items_layout if category == "filter" else l.sorting_items_layout
        layout.addWidget(wrapper)
        
        # Immediate sync for connectors if filter
        if category == "filter":
            self._sync_connectors()
            
        self._on_apply_clicked()

    def _sync_connectors(self):
        """Ensures AND/OR connectors are correctly placed between filters."""
        l = self.layout_engine
        layout = l.filtering_items_layout
        
        # 1. Gather all wrappers, remove all old connectors
        wrappers = []
        i = 0
        while i < layout.count():
            item = layout.itemAt(i)
            w = item.widget()
            if isinstance(w, PluginItemWrapper):
                wrappers.append(w)
                layout.takeAt(i)
            elif w and w.property("is_connector"):
                layout.takeAt(i)
                w.deleteLater()
            else:
                i += 1
                
        # 2. Re-add in order with connectors
        for idx, w in enumerate(wrappers):
            if idx > 0:
                connector = QComboBox()
                connector.addItems(["AND", "OR"])
                connector.setProperty("is_connector", True)
                connector.setFixedWidth(80)
                connector.setStyleSheet("font-size: 10px; padding: 1px;")
                connector.currentIndexChanged.connect(lambda: self._on_apply_clicked())
                layout.addWidget(connector)
            layout.addWidget(w)

    def _remove_plugin_item(self, wrapper, category):
        l = self.layout_engine
        layout = l.filtering_items_layout if category == "filter" else l.sorting_items_layout
        
        layout.removeWidget(wrapper)
        wrapper.setParent(None)
        wrapper.deleteLater()
        
        if category == "filter":
            QTimer.singleShot(0, self._sync_connectors)
        QTimer.singleShot(10, self._on_apply_clicked)

    def _on_plugin_item_selected(self, wrapper, category):
        content_widget = wrapper.content
        combo = content_widget.combo
        layout = content_widget.params_layout

        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w: w.deleteLater()

        plugin = combo.currentData()
        if plugin and hasattr(plugin, "schema"):
            for param in plugin.schema.get("parameters", []):
                w_container = WidgetGenerator.create_labeled_widget(param)
                self._connect_change_signal(w_container.input_widget)
                layout.addWidget(w_container)
        
        self._on_apply_clicked()

    def _connect_change_signal(self, widget):
        if isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            widget.valueChanged.connect(lambda: self._on_apply_clicked())
        elif isinstance(widget, QLineEdit):
            widget.textChanged.connect(lambda: self._on_apply_clicked())
        elif isinstance(widget, QComboBox):
            widget.currentIndexChanged.connect(lambda: self._on_apply_clicked())
        elif isinstance(widget, QCheckBox):
            widget.stateChanged.connect(lambda: self._on_apply_clicked())

    def _get_params(self, layout):
        params = {}
        for i in range(layout.count()):
            container = layout.itemAt(i).widget()
            if container and container.property("is_param"):
                w = container.input_widget
                val = None
                if isinstance(w, (QSpinBox, QDoubleSpinBox)): val = w.value()
                elif isinstance(w, QLineEdit): val = w.text()
                elif isinstance(w, QComboBox): val = w.currentText()
                elif isinstance(w, QCheckBox): val = w.isChecked()
                params[container.param_name] = val
        return params

    def _on_apply_clicked(self):
        l = self.layout_engine
        
        rules = {
            "group": {
                "plugin": l.group_combo.currentData(), 
                "params": self._get_params(l.group_params_layout)
            },
            "filters": [],
            "sorts": []
        }
        
        for i in range(l.filtering_items_layout.count()):
            widget = l.filtering_items_layout.itemAt(i).widget()
            if isinstance(widget, PluginItemWrapper):
                if widget.enabled_cb.isChecked():
                    content = widget.content
                    plugin = content.combo.currentData()
                    if plugin:
                        rules["filters"].append({
                            "type": "plugin",
                            "plugin": plugin,
                            "params": self._get_params(content.params_layout)
                        })
            elif widget and widget.property("is_connector"):
                rules["filters"].append({
                    "type": "connector",
                    "op": widget.currentText()
                })
                    
        for i in range(l.sorting_items_layout.count()):
            item = l.sorting_items_layout.itemAt(i)
            wrapper = item.widget()
            if isinstance(wrapper, PluginItemWrapper) and wrapper.enabled_cb.isChecked():
                content = wrapper.content
                plugin = content.combo.currentData()
                if plugin:
                    rules["sorts"].append({
                        "plugin": plugin,
                        "metric": content.metric_combo.currentData(),
                        "params": self._get_params(content.params_layout)
                    })
        
        Communicator().rules_updated.emit(rules)

    # Drag and Drop Reordering
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-plugin-item"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-plugin-item"):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        source_item = event.source()
        if not isinstance(source_item, PluginItemWrapper):
            return
            
        l = self.layout_engine
        
        # Determine target layout
        target_layout = None
        if l.filtering_section.isAncestorOf(source_item):
            target_layout = l.filtering_items_layout
        elif l.sorting_section.isAncestorOf(source_item):
            target_layout = l.sorting_items_layout
            
        if not target_layout:
            source_item.show()
            return
            
        # Find index based on drop position
        drop_pos = event.pos()
        new_index = 0
        
        for i in range(target_layout.count()):
            item = target_layout.itemAt(i)
            w = item.widget()
            if w and w.isVisible():
                if drop_pos.y() > w.mapTo(self, w.rect().center()).y():
                    new_index = i + 1
                    
        target_layout.insertWidget(new_index, source_item)
        source_item.show()
        
        if target_layout == l.filtering_items_layout:
            self._sync_connectors()
            
        self._on_apply_clicked()
        event.accept()

    @property
    def grouping_section(self): return self.layout_engine.grouping_section
    @property
    def filtering_section(self): return self.layout_engine.filtering_section
    @property
    def sorting_section(self): return self.layout_engine.sorting_section
    @property
    def group_combo(self): return self.layout_engine.group_combo
    @property
    def filtering_items_layout(self): return self.layout_engine.filtering_items_layout
    @property
    def sorting_items_layout(self): return self.layout_engine.sorting_items_layout
