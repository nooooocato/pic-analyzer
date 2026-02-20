import pytest
from PySide6.QtWidgets import QComboBox, QPushButton, QSpinBox
from PySide6.QtCore import Qt
from src.ui.main_window.logic import MainWindow
from src.app.state import state
from src.app.communicator import Communicator

def test_apply_button_enables_on_param_change(qtbot):
    """Test that the Apply button enables when a plugin parameter is modified."""
    state.initialize()
    window = MainWindow()
    qtbot.addWidget(window)
    sidebar = window.layout_engine.sidebar
    
    # 1. Select 'Date Grouping'
    idx = sidebar.group_combo.findText("Date Grouping")
    sidebar.group_combo.setCurrentIndex(idx)
    
    # Apply button should be disabled initially after selection auto-apply
    assert sidebar.apply_btn.isEnabled() is False
    
    # 2. Find a parameter widget (Date Grouping has 'granularity' choice)
    # Let's find by type or check layout
    all_combos = sidebar.grouping_section.findChildren(QComboBox)
    # The second combo should be the parameter
    assert len(all_combos) >= 2
    granularity_combo = all_combos[1]
    
    # 3. Change parameter
    granularity_combo.setCurrentIndex((granularity_combo.currentIndex() + 1) % granularity_combo.count())
    
    # 4. Verify Apply button is enabled
    assert sidebar.apply_btn.isEnabled() is True
    
def test_apply_button_disables_after_click(qtbot):
    """Test that the Apply button disables after it is clicked."""
    state.initialize()
    window = MainWindow()
    qtbot.addWidget(window)
    sidebar = window.layout_engine.sidebar
    
    # Enable it first
    sidebar.apply_btn.setEnabled(True)
    
    # Click it
    qtbot.mouseClick(sidebar.apply_btn, Qt.LeftButton)
    
    # Verify it is disabled
    assert sidebar.apply_btn.isEnabled() is False
