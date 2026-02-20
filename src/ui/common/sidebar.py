from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from src.app.state import state
from .collapsible import CollapsibleSection

class SidebarContainer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(250)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        # Grouping Section
        self.grouping_content = QWidget()
        self.grouping_layout = QVBoxLayout(self.grouping_content)
        self.group_combo = QComboBox()
        self.grouping_layout.addWidget(self.group_combo)
        self.grouping_section = CollapsibleSection("Grouping", self.grouping_content)
        
        # Filtering Section
        self.filtering_content = QWidget()
        self.filtering_layout = QVBoxLayout(self.filtering_content)
        self.filter_combo = QComboBox()
        self.filtering_layout.addWidget(self.filter_combo)
        self.filtering_section = CollapsibleSection("Filtering", self.filtering_content)
        
        # Sorting Section
        self.sorting_content = QWidget()
        self.sorting_layout = QVBoxLayout(self.sorting_content)
        self.sort_combo = QComboBox()
        self.sorting_layout.addWidget(self.sort_combo)
        self.sorting_section = CollapsibleSection("Sorting", self.sorting_content)
        
        layout.addWidget(self.grouping_section)
        layout.addWidget(self.filtering_section)
        layout.addWidget(self.sorting_section)
        layout.addStretch()
        
        self._populate_dropdowns()
        
    def _populate_dropdowns(self):
        pm = state.plugin_manager
        
        # Helper to populate
        def populate(combo, plugins):
            combo.clear()
            combo.addItem("None", None)
            for name, plugin in plugins.items():
                combo.addItem(name, plugin)
                
        populate(self.group_combo, pm.group_plugins)
        populate(self.sort_combo, pm.sort_plugins)
        populate(self.filter_combo, pm.filter_plugins)
