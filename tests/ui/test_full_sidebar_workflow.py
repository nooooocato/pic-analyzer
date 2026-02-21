import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox
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
    gallery.add_item({"path": str(img1)})
    gallery.add_item({"path": str(img2)})
    
    # Wait for debounce timer
    qtbot.wait(100)
    assert gallery.count() == 2
    
    # 2. Test Filtering (.png only)
    # Add a filter item
    qtbot.mouseClick(sidebar.layout_engine.add_filter_btn, Qt.LeftButton)
    
    # Find the filter plugin combo
    filter_items = sidebar.filtering_items_layout
    wrapper = filter_items.itemAt(0).widget()
    filter_combo = wrapper.content.combo
    
    f_idx = filter_combo.findText("File Type")
    filter_combo.setCurrentIndex(f_idx) # Should auto-apply default (.jpg)
    qtbot.wait(100)
    
    # img1 is .jpg, img2 is .png. Default filter is .jpg.
    assert gallery.count() == 1
    assert gallery._visible_items[0]['path'] == str(img1)
    
    # Param combo should appear (FileType has 'extensions' list)
    # Find params layout inside wrapper.content
    params_layout = wrapper.content.params_layout
    ext_combo = None
    for i in range(params_layout.count()):
        w = params_layout.itemAt(i).widget()
        if w and w.property("is_param"):
            ext_combo = w.input_widget
            break
            
    assert ext_combo is not None
    ext_combo.setCurrentText(".png")
    
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
    
    # 4. Remove Filter
    wrapper.remove_btn.click()
    qtbot.wait(100)
    assert gallery.count() == 2

    # 5. Test Sorting (Ascending by a dummy metric)
    from unittest.mock import MagicMock
    state.db_manager = MagicMock()
    state.db_manager.get_metric_values.return_value = {str(img1): 10, str(img2): 5}
    state.db_manager.get_numeric_metrics.return_value = ["dummy_val"]
    
    sidebar._populate_dropdowns() 
    
    qtbot.mouseClick(sidebar.layout_engine.add_sort_btn, Qt.LeftButton)
    sort_wrapper = sidebar.sorting_items_layout.itemAt(0).widget()
    sort_combo = sort_wrapper.content.combo
    sort_metric_combo = sort_wrapper.content.metric_combo
    
    s_idx = sort_combo.findText("Ascending")
    sort_combo.setCurrentIndex(s_idx)
    
    m_idx = sort_metric_combo.findText("Dummy Val")
    sort_metric_combo.setCurrentIndex(m_idx)
    
    qtbot.wait(100)
    
    # Should be sorted: img2 (5) then img1 (10)
    assert gallery._visible_items[0]['path'] == str(img2)
    assert gallery._visible_items[1]['path'] == str(img1)
