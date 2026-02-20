from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton, QScrollArea, QLabel, QSplitter
from PySide6.QtCore import Qt
from src.ui.common.collapsible import CollapsibleSection

class SidebarLayout:
    def setup_ui(self, widget: QWidget):
        widget.setFixedWidth(250)
        
        self.main_layout = QVBoxLayout(widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Scroll area for long sidebars
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.content_layout = QVBoxLayout(self.scroll_content)
        self.content_layout.setContentsMargins(5, 5, 5, 5)
        self.content_layout.setSpacing(0) # Spacing handled by containers
        self.scroll.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll)
        
        # Filtering
        self.filtering_content = QWidget()
        self.filter_params_layout = QVBoxLayout(self.filtering_content)
        self.filter_combo = QComboBox()
        self.filter_params_layout.addWidget(self.filter_combo)
        self.filtering_section = CollapsibleSection("Filtering", self.filtering_content)
        
        # Grouping
        self.grouping_content = QWidget()
        self.group_params_layout = QVBoxLayout(self.grouping_content)
        self.group_combo = QComboBox()
        self.group_params_layout.addWidget(self.group_combo)
        self.grouping_section = CollapsibleSection("Grouping", self.grouping_content)
        
        # Sorting
        self.sorting_content = QWidget()
        self.sort_params_layout = QVBoxLayout(self.sorting_content)
        self.sort_combo = QComboBox()
        self.sort_metric_combo = QComboBox()
        self.sort_params_layout.addWidget(QLabel("Metric:"))
        self.sort_params_layout.addWidget(self.sort_metric_combo)
        self.sort_params_layout.addWidget(QLabel("Algorithm:"))
        self.sort_params_layout.addWidget(self.sort_combo)
        self.sorting_section = CollapsibleSection("Sorting", self.sorting_content)
        
        # Splitter for expanded sections
        self.splitter = QSplitter(Qt.Vertical)
        self.content_layout.addWidget(self.splitter)
        
        # Container for collapsed sections (at the bottom)
        self.collapsed_container = QWidget()
        self.collapsed_layout = QVBoxLayout(self.collapsed_container)
        self.collapsed_layout.setContentsMargins(0, 5, 0, 0)
        self.collapsed_layout.setSpacing(5)
        self.content_layout.addWidget(self.collapsed_container)
        
        self.content_layout.addStretch()
        
        self.all_sections = [
            self.filtering_section,
            self.grouping_section,
            self.sorting_section
        ]
        
        self.reorder_sections()

    def reorder_sections(self):
        """Moves sections between the splitter (expanded) and the collapsed container."""
        # Remove sections from current parents
        for section in self.all_sections:
            section.setParent(None)
            
        expanded = [s for s in self.all_sections if s.is_expanded]
        collapsed = [s for s in self.all_sections if not s.is_expanded]
        
        # Add expanded to splitter
        if expanded:
            self.splitter.setVisible(True)
            for section in expanded:
                self.splitter.addWidget(section)
        else:
            self.splitter.setVisible(False)
            
        # Add collapsed to collapsed layout
        if collapsed:
            self.collapsed_container.setVisible(True)
            for section in collapsed:
                self.collapsed_layout.addWidget(section)
        else:
            self.collapsed_container.setVisible(False)
