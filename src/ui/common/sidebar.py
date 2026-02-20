from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QScrollArea, QSpinBox, QDoubleSpinBox, QLineEdit, QCheckBox
from src.app.state import state
from .collapsible import CollapsibleSection
from .widget_generator import WidgetGenerator

class SidebarContainer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(250)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Scroll area for long sidebars
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.content_layout = QVBoxLayout(self.scroll_content)
        self.content_layout.setContentsMargins(5, 5, 5, 5)
        self.content_layout.setSpacing(10)
        self.scroll.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll)
        
        # Sections
        self._setup_sections()
        
        # Apply Button
        self.apply_btn = QPushButton("Apply Changes")
        self.apply_btn.setEnabled(False)
        self.apply_btn.clicked.connect(self._on_apply_clicked)
        
        self.content_layout.addStretch()
        self.content_layout.addWidget(self.apply_btn)
        
        self._populate_dropdowns()

    def _setup_sections(self):
        # Grouping
        self.grouping_content = QWidget()
        self.group_params_layout = QVBoxLayout(self.grouping_content)
        self.group_combo = QComboBox()
        self.group_params_layout.addWidget(self.group_combo)
        self.grouping_section = CollapsibleSection("Grouping", self.grouping_content)
        self.content_layout.addWidget(self.grouping_section)
        
        # Filtering
        self.filtering_content = QWidget()
        self.filter_params_layout = QVBoxLayout(self.filtering_content)
        self.filter_combo = QComboBox()
        self.filter_params_layout.addWidget(self.filter_combo)
        self.filtering_section = CollapsibleSection("Filtering", self.filtering_content)
        self.content_layout.addWidget(self.filtering_section)
        
        # Sorting
        self.sorting_content = QWidget()
        self.sort_params_layout = QVBoxLayout(self.sorting_content)
        self.sort_combo = QComboBox()
        self.sort_metric_combo = QComboBox() # Added metric combo
        self.sort_params_layout.addWidget(QLabel("Algorithm:"))
        self.sort_params_layout.addWidget(self.sort_combo)
        self.sort_params_layout.addWidget(QLabel("Metric:"))
        self.sort_params_layout.addWidget(self.sort_metric_combo)
        self.sorting_section = CollapsibleSection("Sorting", self.sorting_content)
        self.content_layout.addWidget(self.sorting_section)
        
        # Connections
        self.group_combo.currentIndexChanged.connect(lambda: self._on_plugin_selected("group"))
        self.filter_combo.currentIndexChanged.connect(lambda: self._on_plugin_selected("filter"))
        self.sort_combo.currentIndexChanged.connect(lambda: self._on_plugin_selected("sort"))
        self.sort_metric_combo.currentIndexChanged.connect(lambda: self._on_apply_clicked())

    def _populate_dropdowns(self):
        pm = state.plugin_manager
        
        # Populate Metrics
        self.sort_metric_combo.blockSignals(True)
        self.sort_metric_combo.clear()
        metrics = state.db_manager.get_numeric_metrics()
        for m in metrics:
            self.sort_metric_combo.addItem(m.replace("_", " ").title(), m)
        self.sort_metric_combo.blockSignals(False)

        def populate(combo, plugins):
            combo.blockSignals(True)
            combo.clear()
            combo.addItem("None", None)
            for name, plugin in plugins.items():
                combo.addItem(name, plugin)
            combo.blockSignals(False)
                
        populate(self.group_combo, pm.group_plugins)
        populate(self.sort_combo, pm.sort_plugins)
        populate(self.filter_combo, pm.filter_plugins)

    def _on_plugin_selected(self, category):
        if category == "group":
            combo, layout, keep_count = self.group_combo, self.group_params_layout, 1
        elif category == "filter":
            combo, layout, keep_count = self.filter_combo, self.filter_params_layout, 1
        else: # sort
            combo, layout, keep_count = self.sort_combo, self.sort_params_layout, 4
            
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
            widget.valueChanged.connect(lambda: self.apply_btn.setEnabled(True))
        elif isinstance(widget, QLineEdit):
            widget.textChanged.connect(lambda: self.apply_btn.setEnabled(True))
        elif isinstance(widget, QComboBox):
            widget.currentIndexChanged.connect(lambda: self.apply_btn.setEnabled(True))
        elif isinstance(widget, QCheckBox):
            widget.stateChanged.connect(lambda: self.apply_btn.setEnabled(True))

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
        self.apply_btn.setEnabled(False)
        
        # Gather all rules
        rules = {
            "group": {"plugin": self.group_combo.currentData(), "params": self._get_params(self.group_params_layout, 1)},
            "filter": {"plugin": self.filter_combo.currentData(), "params": self._get_params(self.filter_params_layout, 1)},
            "sort": {
                "plugin": self.sort_combo.currentData(), 
                "metric": self.sort_metric_combo.currentData(),
                "params": self._get_params(self.sort_params_layout, 4)
            }
        }
        
        from src.app.communicator import Communicator
        Communicator().rules_updated.emit(rules)
