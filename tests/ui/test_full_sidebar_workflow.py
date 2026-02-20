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
    sidebar.filter_combo.setCurrentIndex(f_idx)
    # Param combo should appear
    all_combos = sidebar.filtering_section.findChildren(QComboBox)
    ext_combo = all_combos[1]
    ext_combo.setCurrentText(".png")
    
    # Click Apply
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

from PySide6.QtWidgets import QComboBox
