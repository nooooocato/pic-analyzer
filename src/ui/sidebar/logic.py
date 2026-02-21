from PySide6.QtWidgets import QWidget, QSpinBox, QDoubleSpinBox, QLineEdit, QCheckBox, QComboBox, QVBoxLayout, QLabel
from PySide6.QtCore import QTimer
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
        
        self._setup_connections()
        self._populate_dropdowns()

    def _setup_connections(self):
        l = self.layout_engine
        l.group_combo.currentIndexChanged.connect(lambda: self._on_plugin_selected("group"))

        l.filtering_section.toggled.connect(l.reorder_sections)
        l.grouping_section.toggled.connect(l.reorder_sections)
        l.sorting_section.toggled.connect(l.reorder_sections)

        l.add_filter_btn.clicked.connect(lambda: self._add_plugin_item("filter"))
        l.add_sort_btn.clicked.connect(lambda: self._add_plugin_item("sort"))

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
        # Grouping still uses single combo for now
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
        
        # Create plugin content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 5, 0, 5)
        
        # Plugin selection combo
        combo = QComboBox()
        combo.addItem("Select Plugin...", None)
        plugins = pm.filter_plugins if category == "filter" else pm.sort_plugins
        for name, plugin in plugins.items():
            combo.addItem(name, plugin)
        content_layout.addWidget(combo)
        
        if category == "sort":
            # Add metric selection for sort
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
        
        # Wrapper
        wrapper = PluginItemWrapper(content_widget, title=category.title())
        wrapper.removed.connect(lambda: self._remove_plugin_item(wrapper, category))
        wrapper.toggled.connect(lambda _: self._on_apply_clicked())
        
        combo.currentIndexChanged.connect(lambda: self._on_plugin_item_selected(wrapper, category))
        
        if category == "filter":
            # Add AND/OR connector if not first
            if l.filtering_items_layout.count() > 0:
                connector = QComboBox()
                connector.addItems(["AND", "OR"])
                connector.setProperty("is_connector", True)
                connector.currentIndexChanged.connect(lambda: self._on_apply_clicked())
                l.filtering_items_layout.addWidget(connector)
            l.filtering_items_layout.addWidget(wrapper)
        else:
            l.sorting_items_layout.addWidget(wrapper)
            
        self._on_apply_clicked()

    def _remove_plugin_item(self, wrapper, category):
        l = self.layout_engine
        layout = l.filtering_items_layout if category == "filter" else l.sorting_items_layout
        
        if category == "filter":
            index = layout.indexOf(wrapper)
            if index > 0:
                # Remove connector before
                item = layout.itemAt(index - 1)
                if item and item.widget() and item.widget().property("is_connector"):
                    w = layout.takeAt(index - 1).widget()
                    w.deleteLater()
            elif index == 0 and layout.count() > 1:
                # Remove connector after
                item = layout.itemAt(index + 1)
                if item and item.widget() and item.widget().property("is_connector"):
                    w = layout.takeAt(index + 1).widget()
                    w.deleteLater()

        wrapper.deleteLater()
        QTimer.singleShot(0, self._on_apply_clicked)

    def _on_plugin_item_selected(self, wrapper, category):
        content_widget = wrapper.content
        combo = content_widget.combo
        layout = content_widget.params_layout

        # Clear existing dynamic widgets
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
        
        # Grouping (Single)
        rules = {
            "group": {
                "plugin": l.group_combo.currentData(), 
                "params": self._get_params(l.group_params_layout)
            },
            "filters": [],
            "sorts": []
        }
        
        # Filters (Multi)
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
                    
        # Sorts (Multi)
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

    # Properties for testing
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
