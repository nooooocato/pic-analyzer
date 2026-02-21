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

        # Connect to folder changes to restore state
        Communicator().notify.connect(self._on_app_notify)

    def _on_app_notify(self, message, level):
        if "Scan finished" in message:
            self.restore_state()

    def restore_state(self):
        """Loads and applies saved sidebar configuration for the current workspace."""
        if not state.db_manager or not state.workspace_name:
            return
            
        config = state.db_manager.load_sidebar_state(state.workspace_name)
        if not config:
            return
            
        l = self.layout_engine
        
        # 1. Restore Grouping
        group_conf = config.get("group", {})
        plugin_name = group_conf.get("plugin_name")
        if plugin_name:
            idx = l.group_combo.findText(plugin_name)
            if idx >= 0:
                l.group_combo.blockSignals(True)
                l.group_combo.setCurrentIndex(idx)
                l.group_combo.blockSignals(False)
                self._on_plugin_selected("group")
                self._set_params(l.group_params_layout, group_conf.get("params", {}))

        # 2. Restore Filters
        while l.filtering_items_layout.count():
            item = l.filtering_items_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
            
        for f_item in config.get("filters", []):
            if f_item.get("type") == "plugin":
                wrapper = self._add_plugin_item("filter", auto_apply=False)
                if wrapper:
                    p_name = f_item.get("plugin_name")
                    idx = wrapper.content.combo.findText(p_name)
                    if idx >= 0:
                        wrapper.content.combo.setCurrentIndex(idx)
                        self._set_params(wrapper.content.params_layout, f_item.get("params", {}))
                    wrapper.enabled_cb.setChecked(f_item.get("enabled", True))
            elif f_item.get("type") == "connector":
                self._sync_connectors()
                for i in range(l.filtering_items_layout.count()-1, -1, -1):
                    w = l.filtering_items_layout.itemAt(i).widget()
                    if w and w.property("is_connector"):
                        w.setCurrentText(f_item.get("op", "AND"))
                        break

        # 3. Restore Sorts
        while l.sorting_items_layout.count():
            item = l.sorting_items_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
            
        for s_item in config.get("sorts", []):
            wrapper = self._add_plugin_item("sort", auto_apply=False)
            if wrapper:
                p_name = s_item.get("plugin_name")
                idx = wrapper.content.combo.findText(p_name)
                if idx >= 0:
                    wrapper.content.combo.setCurrentIndex(idx)
                    self._set_params(wrapper.content.params_layout, s_item.get("params", {}))
                
                metric = s_item.get("metric")
                if metric:
                    m_idx = wrapper.content.metric_combo.findData(metric)
                    if m_idx >= 0: wrapper.content.metric_combo.setCurrentIndex(m_idx)
                
                wrapper.enabled_cb.setChecked(s_item.get("enabled", True))

        self._on_apply_clicked(save_state=False)

    def _set_params(self, layout, params):
        for i in range(layout.count()):
            container = layout.itemAt(i).widget()
            if container and container.property("is_param"):
                name = container.param_name
                if name in params:
                    val = params[name]
                    w = container.input_widget
                    w.blockSignals(True)
                    if isinstance(w, (QSpinBox, QDoubleSpinBox)): w.setValue(val)
                    elif isinstance(w, QLineEdit): w.setText(val)
                    elif isinstance(w, QComboBox): w.setCurrentText(val)
                    elif isinstance(w, QCheckBox): w.setChecked(val)
                    w.blockSignals(False)

    def _reorder_and_apply(self):
        self.layout_engine.update_splitter_handles()
        l = self.layout_engine
        sizes = [1 if s.is_expanded else 0 for s in l.all_sections]
        l.splitter.setSizes(sizes)

    def _on_plugin_selected(self, category):
        l = self.layout_engine
        if category == "group":
            combo, layout = l.group_combo, l.group_params_layout
        else:
            return

        while layout.count() > 1:
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

    def _add_plugin_item(self, category, auto_apply=True):
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
        
        if category == "filter":
            self._sync_connectors()
            
        if auto_apply:
            self._on_apply_clicked()
        return wrapper

    def _sync_connectors(self):
        l = self.layout_engine
        layout = l.filtering_items_layout
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
                
        for idx, w in enumerate(wrappers):
            if idx > 0:
                connector = QComboBox()
                connector.addItems(["AND", "OR"])
                connector.setProperty("is_connector", True)
                connector.setFixedWidth(80)
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
        QTimer.singleShot(20, self._on_apply_clicked)

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

    def _on_apply_clicked(self, save_state=True):
        l = self.layout_engine
        rules = {
            "group": {
                "plugin": l.group_combo.currentData(), 
                "plugin_name": l.group_combo.currentText() if l.group_combo.currentIndex() > 0 else None,
                "params": self._get_params(l.group_params_layout)
            },
            "filters": [],
            "sorts": []
        }
        
        # Create a clean serializable config for DB
        save_config = {
            "group": {
                "plugin_name": rules["group"]["plugin_name"],
                "params": rules["group"]["params"]
            },
            "filters": [],
            "sorts": []
        }

        for i in range(l.filtering_items_layout.count()):
            widget = l.filtering_items_layout.itemAt(i).widget()
            if not widget or widget.parent() is None: continue
            if isinstance(widget, PluginItemWrapper):
                content = widget.content
                plugin = content.combo.currentData()
                if not plugin: continue # Skip 'Select Plugin...'

                f_data = {
                    "type": "plugin",
                    "plugin_name": content.combo.currentText(),
                    "enabled": widget.enabled_cb.isChecked(),
                    "params": self._get_params(content.params_layout)
                }
                save_config["filters"].append(f_data)
                if widget.enabled_cb.isChecked() and plugin:
                    rules["filters"].append({"type": "plugin", "plugin": plugin, "params": f_data["params"]})
            elif widget.property("is_connector"):
                op = widget.currentText()
                save_config["filters"].append({"type": "connector", "op": op})
                rules["filters"].append({"type": "connector", "op": op})
                    
        for i in range(l.sorting_items_layout.count()):
            item = l.sorting_items_layout.itemAt(i)
            wrapper = item.widget()
            if not wrapper or wrapper.parent() is None: continue
            if isinstance(wrapper, PluginItemWrapper):
                content = wrapper.content
                plugin = content.combo.currentData()
                if not plugin: continue # Skip placeholders

                metric = content.metric_combo.currentData() if hasattr(content, "metric_combo") else None
                s_data = {
                    "plugin_name": content.combo.currentText(),
                    "metric": metric,
                    "enabled": wrapper.enabled_cb.isChecked(),
                    "params": self._get_params(content.params_layout)
                }
                save_config["sorts"].append(s_data)
                if wrapper.enabled_cb.isChecked() and plugin and metric:
                    rules["sorts"].append({"plugin": plugin, "metric": metric, "params": s_data["params"]})
        
        if save_state and state.db_manager and state.workspace_name:
            state.db_manager.save_sidebar_state(state.workspace_name, save_config)
        Communicator().rules_updated.emit(rules)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-plugin-item"): event.accept()
        else: event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-plugin-item"): event.accept()
        else: event.ignore()

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
            return
            
        # Accept the action
        event.setDropAction(Qt.MoveAction)
        event.accept()

        # Find target index among WRAPPERS only (ignore connectors)
        drop_pos = event.pos()
        
        # Get current items in order
        items = []
        for i in range(target_layout.count()):
            w = target_layout.itemAt(i).widget()
            if isinstance(w, PluginItemWrapper):
                items.append(w)
        
        # Remove source from list if present to find its new spot
        if source_item in items:
            items.remove(source_item)
            
        # Find new position
        new_idx = 0
        for i, w in enumerate(items):
            # mapTo(self, ...) gives position in SidebarContainer coordinates
            if drop_pos.y() > w.mapTo(self, w.rect().center()).y():
                new_idx = i + 1
        
        # Re-insert at calculated position
        target_layout.insertWidget(new_idx if target_layout != l.filtering_items_layout else new_idx * 2, source_item)
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
