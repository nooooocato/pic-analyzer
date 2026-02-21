import pytest
from PySide6.QtWidgets import QComboBox, QPushButton
from src.ui.main_window.logic import MainWindow
from src.app.state import state

def test_sidebar_dropdowns_populated(qtbot):
    """Test that sidebar dropdowns are populated with plugins."""
    # Ensure state is initialized so plugins are loaded
    state.initialize()
    
    window = MainWindow()
    qtbot.addWidget(window)
    sidebar = window.layout_engine.sidebar
    
    # 1. Check Grouping (still single combo)
    group_dropdown = sidebar.grouping_section.findChild(QComboBox)
    assert group_dropdown is not None
    assert group_dropdown.count() > 0
    items = [group_dropdown.itemText(i) for i in range(group_dropdown.count())]
    assert "Date Grouping" in items

    # 2. Check Filtering (need to add item first)
    qtbot.mouseClick(sidebar.layout_engine.add_filter_btn, Qt.LeftButton)
    # Find combo in the filtering items
    filter_items = sidebar.findChildren(QComboBox) # This is broad, let's be more specific
    # Filter combo is inside a PluginItemWrapper
    filter_dropdown = None
    for combo in sidebar.findChildren(QComboBox):
        if "Select Plugin..." in [combo.itemText(i) for i in range(combo.count())]:
            # This is likely a filter or sort combo
            # We check its parentage
            if sidebar.layout_engine.filtering_section.isAncestorOf(combo):
                filter_dropdown = combo
                break
    
    assert filter_dropdown is not None
    filter_items = [filter_dropdown.itemText(i) for i in range(filter_dropdown.count())]
    assert "File Size" in filter_items

    # 3. Check Sorting
    qtbot.mouseClick(sidebar.layout_engine.add_sort_btn, Qt.LeftButton)
    sort_dropdown = None
    for combo in sidebar.findChildren(QComboBox):
        if "Select Plugin..." in [combo.itemText(i) for i in range(combo.count())]:
            if sidebar.layout_engine.sorting_section.isAncestorOf(combo):
                sort_dropdown = combo
                break
    
    assert sort_dropdown is not None
    sort_items = [sort_dropdown.itemText(i) for i in range(sort_dropdown.count())]
    assert "Ascending" in sort_items
    assert "Descending" in sort_items

from PySide6.QtCore import Qt
