from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton, QScrollArea, QLabel
from src.ui.common.collapsible import CollapsibleSection

class SidebarLayout:
    def setup_ui(self, widget: QWidget):
        widget.setFixedWidth(250)
        
        main_layout = QVBoxLayout(widget)
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
        self.sort_metric_combo = QComboBox()
        self.sort_params_layout.addWidget(QLabel("Algorithm:"))
        self.sort_params_layout.addWidget(self.sort_combo)
        self.sort_params_layout.addWidget(QLabel("Metric:"))
        self.sort_params_layout.addWidget(self.sort_metric_combo)
        self.sorting_section = CollapsibleSection("Sorting", self.sorting_content)
        self.content_layout.addWidget(self.sorting_section)
        
        self.content_layout.addStretch()
