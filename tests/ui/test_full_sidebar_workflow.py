import pytest
from PySide6.QtCore import Qt
from src.ui.main_window.logic import MainWindow
from src.app.state import state
from src.app.communicator import Communicator

def test_full_sidebar_rules_application(qtbot, tmp_path):
    """Test that selecting rules in sidebar correctly updates the gallery."""
    # 1. Setup mock data
    state.initialize()
    img1 = tmp_path / "a.jpg"
    img1.touch()
    img2 = tmp_path / "b.png"
    img2.touch()
    
    window = MainWindow()
    qtbot.addWidget(window)
    gallery = window.layout_engine.gallery
    sidebar = window.layout_engine.sidebar
    
    # Manually add items to gallery
    gallery.add_item(str(img1))
    gallery.add_item(str(img2))
    
    # Wait for debounce timer
    qtbot.wait(100)
    assert gallery.count() == 2
    
    # 2. Test Filtering (.png only)
    f_idx = sidebar.filter_combo.findText("File Type")
    sidebar.filter_combo.setCurrentIndex(f_idx) # Should auto-apply default (.jpg)
    qtbot.wait(100)
    
    # img1 is .jpg, img2 is .png. Default filter is .jpg.
    # Wait, actually FileType default is .jpg. So img1 should be visible.
    assert gallery.count() == 1
    assert gallery._visible_items[0]['path'] == str(img1)
    
    # Param combo should appear
    all_combos = sidebar.filtering_section.findChildren(QComboBox)
    ext_combo = all_combos[1]
    ext_combo.setCurrentText(".png")
    
    # Click Apply (needed for param change)
    qtbot.mouseClick(sidebar.apply_btn, Qt.LeftButton)
    qtbot.wait(100)
    
    # Gallery should show only 1 item
    assert gallery.count() == 1
    assert gallery._visible_items[0]['path'] == str(img2)
    
    # 3. Test Grouping (None -> Date Grouping)
    g_idx = sidebar.group_combo.findText("Date Grouping")
    sidebar.group_combo.setCurrentIndex(g_idx)
    qtbot.wait(100)
    
    # Should have 1 group
    assert len(gallery._group_widgets) == 1
    
    # 4. Reset Filter to None
    sidebar.filter_combo.setCurrentIndex(0) # None
    qtbot.wait(100)
    assert gallery.count() == 2

    # 5. Test Sorting (Ascending by a dummy metric)
    # We need to mock db_manager to return some values
    from unittest.mock import MagicMock
    state.db_manager = MagicMock()
    state.db_manager.get_metric_values.return_value = {str(img1): 10, str(img2): 5}
    state.db_manager.get_numeric_metrics.return_value = ["dummy_val"]
    
    # Refresh metrics combo (usually happens on init or folder open, but we mock now)
    sidebar._populate_dropdowns() 
    
    s_idx = sidebar.sort_combo.findText("Ascending")
    sidebar.sort_combo.setCurrentIndex(s_idx)
    
    m_idx = sidebar.sort_metric_combo.findText("Dummy Val")
    sidebar.sort_metric_combo.setCurrentIndex(m_idx)
    
    qtbot.mouseClick(sidebar.apply_btn, Qt.LeftButton)
    qtbot.wait(100)
    
    # Should be sorted: img2 (5) then img1 (10)
    assert gallery._visible_items[0]['path'] == str(img2)
    assert gallery._visible_items[1]['path'] == str(img1)

from PySide6.QtWidgets import QComboBox
