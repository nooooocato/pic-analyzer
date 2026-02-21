from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton, QScrollArea, QLabel, QSplitter, QSizePolicy
from PySide6.QtCore import Qt
from src.ui.common.collapsible import CollapsibleSection

class SidebarLayout:
    def setup_ui(self, widget: QWidget):
        widget.setFixedWidth(250)
        
        self.main_layout = QVBoxLayout(widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Scroll area for long sidebars
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QScrollArea.NoFrame)
        self.scroll_content = QWidget()
        self.content_layout = QVBoxLayout(self.scroll_content)
        self.content_layout.setContentsMargins(2, 2, 2, 2)
        self.content_layout.setSpacing(0)
        self.scroll.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll)
        
        # Filtering
        self.filtering_content = QWidget()
        self.filtering_layout = QVBoxLayout(self.filtering_content)
        self.filtering_layout.setContentsMargins(5, 5, 5, 5)
        self.filtering_items_layout = QVBoxLayout()
        self.filtering_items_layout.setSpacing(2)
        self.filtering_layout.addLayout(self.filtering_items_layout)
        
        self.add_filter_btn = QPushButton("+ Add Filter")
        self.filtering_layout.addWidget(self.add_filter_btn)
        self.filtering_section = CollapsibleSection("Filtering", self.filtering_content)
        
        # Grouping
        self.grouping_content = QWidget()
        self.group_params_layout = QVBoxLayout(self.grouping_content)
        self.group_params_layout.setContentsMargins(5, 5, 5, 5)
        self.group_combo = QComboBox()
        self.group_params_layout.addWidget(self.group_combo)
        self.grouping_section = CollapsibleSection("Grouping", self.grouping_content)
        
        # Sorting
        self.sorting_content = QWidget()
        self.sorting_layout = QVBoxLayout(self.sorting_content)
        self.sorting_layout.setContentsMargins(5, 5, 5, 5)
        self.sorting_items_layout = QVBoxLayout()
        self.sorting_items_layout.setSpacing(2)
        self.sorting_layout.addLayout(self.sorting_items_layout)
        
        self.add_sort_btn = QPushButton("+ Add Sort")
        self.sorting_layout.addWidget(self.add_sort_btn)
        self.sorting_section = CollapsibleSection("Sorting", self.sorting_content)
        
        # Splitter for all sections
        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setHandleWidth(1) # Extra thin handle
        
        self.all_sections = [
            self.filtering_section,
            self.grouping_section,
            self.sorting_section
        ]
        
        for section in self.all_sections:
            self.splitter.addWidget(section)
            # Ensure they don't grow unnecessarily
            section.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
            
        self.content_layout.addWidget(self.splitter)
        self.content_layout.addStretch() # This will only work if splitter allows it

        # Initial handles update
        self.update_splitter_handles()

    def update_splitter_handles(self):
        """Forces handles to be hidden if sections are collapsed or if we want tight packing."""
        # For each handle (i=1 to n-1)
        for i in range(1, self.splitter.count()):
            handle = self.splitter.handle(i)
            # If the widget before OR after is collapsed, hide handle logic can be added here
            # But QSplitter handles are not easily hideable individually without sub-classing.
            # We rely on the 1px handle being almost invisible.
            pass
