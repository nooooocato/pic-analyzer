import pytest
from PySide6.QtWidgets import QComboBox, QSpinBox, QDoubleSpinBox, QLineEdit, QCheckBox
from src.ui.main_window.logic import MainWindow
from src.app.state import state
from src.app.communicator import Communicator

def test_immediate_apply_on_param_change(qtbot):
    """Test that rules are applied immediately when a plugin parameter is modified."""
    state.initialize()
    window = MainWindow()
    qtbot.addWidget(window)
    sidebar = window.layout_engine.sidebar
    
    # 1. Select 'Date Grouping' (still in grouping section)
    idx = sidebar.group_combo.findText("Date Grouping")
    
    # Mock communicator to track signals
    with qtbot.waitSignal(Communicator().rules_updated, timeout=500):
        sidebar.group_combo.setCurrentIndex(idx)
        
    # 2. Find a parameter widget (Date Grouping has 'granularity' choice)
    # The grouping section's group_params_layout now contains the parameter widgets
    all_combos = sidebar.grouping_section.findChildren(QComboBox)
    # 1 for plugin selection, others are params
    assert len(all_combos) >= 2
    
    granularity_combo = None
    for combo in all_combos:
        if combo != sidebar.group_combo:
            granularity_combo = combo
            break
            
    assert granularity_combo is not None
    
    with qtbot.waitSignal(Communicator().rules_updated, timeout=500):
        # Change granularity to 'year' (index 0) from default 'month' (index 1)
        granularity_combo.setCurrentIndex(0)

def test_immediate_apply_on_multi_item_change(qtbot):
    """Test that multi-item plugin changes trigger rules_updated."""
    state.initialize()
    window = MainWindow()
    qtbot.addWidget(window)
    sidebar = window.layout_engine.sidebar

    # Add filter
    with qtbot.waitSignal(Communicator().rules_updated, timeout=500):
        sidebar.layout_engine.add_filter_btn.click()
        
    wrapper = sidebar.filtering_items_layout.itemAt(0).widget()
    combo = wrapper.content.combo
    
    # Select File Type
    with qtbot.waitSignal(Communicator().rules_updated, timeout=500):
        idx = combo.findText("File Type")
        combo.setCurrentIndex(idx)

    # Change toggle
    with qtbot.waitSignal(Communicator().rules_updated, timeout=500):
        wrapper.enabled_cb.click()

from PySide6.QtCore import Qt
