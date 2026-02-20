import pytest
from PySide6.QtWidgets import QComboBox
from PySide6.QtCore import Qt
from src.ui.main_window.logic import MainWindow
from src.app.state import state
from src.app.communicator import Communicator

def test_immediate_apply_on_param_change(qtbot):
    """Test that rules are applied immediately when a plugin parameter is modified."""
    state.initialize()
    window = MainWindow()
    qtbot.addWidget(window)
    sidebar = window.layout_engine.sidebar
    
    # 1. Select 'Date Grouping'
    idx = sidebar.group_combo.findText("Date Grouping")
    
    # Mock communicator to track signals
    with qtbot.waitSignal(Communicator().rules_updated, timeout=500):
        sidebar.group_combo.setCurrentIndex(idx)
    
    # 2. Find a parameter widget (Date Grouping has 'granularity' choice)
    all_combos = sidebar.grouping_section.findChildren(QComboBox)
    assert len(all_combos) >= 2
    granularity_combo = all_combos[1]
    
    # 3. Change parameter and verify immediate signal
    with qtbot.waitSignal(Communicator().rules_updated, timeout=500) as blocker:
        granularity_combo.setCurrentIndex((granularity_combo.currentIndex() + 1) % granularity_combo.count())
    
    # Verify signal content
    rules = blocker.args[0]
    assert rules["group"]["plugin"].name == "Date Grouping"
    assert "granularity" in rules["group"]["params"]
