import pytest
from PySide6.QtWidgets import QComboBox
from src.ui.main_window.logic import MainWindow
from src.app.state import state

def test_sidebar_dropdowns_populated(qtbot):
    """Test that sidebar dropdowns are populated with plugins."""
    # Ensure state is initialized so plugins are loaded
    state.initialize()
    
    window = MainWindow()
    qtbot.addWidget(window)
    sidebar = window.layout_engine.sidebar
    
    # We expect each section to eventually have a dropdown
    # Let's check for QComboBox in each section
    group_dropdown = sidebar.grouping_section.findChild(QComboBox)
    filter_dropdown = sidebar.filtering_section.findChild(QComboBox)
    sort_dropdown = sidebar.sorting_section.findChild(QComboBox)
    
    assert group_dropdown is not None
    assert filter_dropdown is not None
    assert sort_dropdown is not None
    
    # Check if they have items (at least 'None' or the discovered plugins)
    assert group_dropdown.count() > 0
    assert sort_dropdown.count() > 0
    
    # Specific plugins we know should be there from Phase 2
    items = [group_dropdown.itemText(i) for i in range(group_dropdown.count())]
    assert "Date Grouping" in items
    
    sort_items = [sort_dropdown.itemText(i) for i in range(sort_dropdown.count())]
    assert "Ascending" in sort_items
    assert "Descending" in sort_items
