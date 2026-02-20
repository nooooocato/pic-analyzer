from PySide6.QtWidgets import QWidget, QSpinBox, QDoubleSpinBox, QLineEdit, QCheckBox, QComboBox
from src.app.state import state
from src.app.communicator import Communicator
from src.ui.common.widget_generator import WidgetGenerator
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

    @property
    def grouping_section(self): return self.layout_engine.grouping_section
    @property
    def filtering_section(self): return self.layout_engine.filtering_section
    @property
    def sorting_section(self): return self.layout_engine.sorting_section
    @property
    def group_combo(self): return self.layout_engine.group_combo
    @property
    def filter_combo(self): return self.layout_engine.filter_combo
    @property
    def sort_combo(self): return self.layout_engine.sort_combo
    @property
    def sort_metric_combo(self): return self.layout_engine.sort_metric_combo
    @property
    def apply_btn(self): return None # Button removed
    @property
    def group_params_layout(self): return self.layout_engine.group_params_layout
    @property
    def filter_params_layout(self): return self.layout_engine.filter_params_layout
    @property
    def sort_params_layout(self): return self.layout_engine.sort_params_layout
    @property
    def content_layout(self): return self.layout_engine.content_layout

    def _setup_connections(self):
        l = self.layout_engine
        l.group_combo.currentIndexChanged.connect(lambda: self._on_plugin_selected("group"))
        l.filter_combo.currentIndexChanged.connect(lambda: self._on_plugin_selected("filter"))
        l.sort_combo.currentIndexChanged.connect(lambda: self._on_plugin_selected("sort"))
        l.sort_metric_combo.currentIndexChanged.connect(lambda: self._on_apply_clicked())

    def _populate_dropdowns(self):
        pm = state.plugin_manager
        l = self.layout_engine
        
        # Populate Metrics
        l.sort_metric_combo.blockSignals(True)
        l.sort_metric_combo.clear()
        metrics = state.db_manager.get_numeric_metrics()
        for m in metrics:
            l.sort_metric_combo.addItem(m.replace("_", " ").title(), m)
        l.sort_metric_combo.blockSignals(False)

        def populate(combo, plugins):
            combo.blockSignals(True)
            combo.clear()
            combo.addItem("None", None)
            for name, plugin in plugins.items():
                combo.addItem(name, plugin)
            combo.blockSignals(False)
                
        populate(l.group_combo, pm.group_plugins)
        populate(l.sort_combo, pm.sort_plugins)
        populate(l.filter_combo, pm.filter_plugins)

    def _on_plugin_selected(self, category):
        l = self.layout_engine
        if category == "group":
            combo, layout, keep_count = l.group_combo, l.group_params_layout, 1
        elif category == "filter":
            combo, layout, keep_count = l.filter_combo, l.filter_params_layout, 1
        else: # sort
            combo, layout, keep_count = l.sort_combo, l.sort_params_layout, 4
            
        # Clear existing dynamic widgets
        while layout.count() > keep_count:
            item = layout.takeAt(keep_count)
            if item.widget(): item.widget().deleteLater()
            
        plugin = combo.currentData()
        if plugin and hasattr(plugin, "schema"):
            for param in plugin.schema.get("parameters", []):
                w_container = WidgetGenerator.create_labeled_widget(param)
                self._connect_change_signal(w_container.input_widget)
                layout.addWidget(w_container)
        
        # Immediate update for plugin selection
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

    def _get_params(self, layout, start_index=1):
        params = {}
        for i in range(start_index, layout.count()):
            container = layout.itemAt(i).widget()
            if container and hasattr(container, "input_widget") and hasattr(container, "param_name"):
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
        
        # Gather all rules
        rules = {
            "group": {"plugin": l.group_combo.currentData(), "params": self._get_params(l.group_params_layout, 1)},
            "filter": {"plugin": l.filter_combo.currentData(), "params": self._get_params(l.filter_params_layout, 1)},
            "sort": {
                "plugin": l.sort_combo.currentData(), 
                "metric": l.sort_metric_combo.currentData(),
                "params": self._get_params(l.sort_params_layout, 4)
            }
        }
        
        Communicator().rules_updated.emit(rules)
