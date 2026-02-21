import pytest
from PySide6.QtWidgets import QWidget, QLabel, QCheckBox, QPushButton
from src.ui.common.plugin_item import PluginItemWrapper

def test_plugin_item_wrapper_initialization(qtbot):
    """Test that PluginItemWrapper initializes with content and controls."""
    content = QLabel("Test Plugin")
    wrapper = PluginItemWrapper(content, title="Filter 1")
    qtbot.addWidget(wrapper)
    
    assert wrapper.content == content
    assert wrapper.title == "Filter 1"
    
    # Check for core components
    assert wrapper.findChild(QCheckBox) is not None # Toggle
    assert wrapper.findChild(QPushButton, "remove_btn") is not None # Remove button
    assert wrapper.findChild(QLabel, "drag_handle") is not None # Drag handle

def test_plugin_item_wrapper_signals(qtbot):
    """Test that the wrapper emits appropriate signals."""
    content = QLabel("Test Plugin")
    wrapper = PluginItemWrapper(content)
    qtbot.addWidget(wrapper)
    
    # Test Toggle Signal
    toggle_cb = wrapper.findChild(QCheckBox)
    with qtbot.waitSignal(wrapper.toggled, timeout=1000) as blocker:
        qtbot.mouseClick(toggle_cb, Qt.LeftButton)
    assert blocker.args == [False] # Initial was checked (True)

    # Test Remove Signal
    remove_btn = wrapper.findChild(QPushButton, "remove_btn")
    with qtbot.waitSignal(wrapper.removed, timeout=1000):
        qtbot.mouseClick(remove_btn, Qt.LeftButton)

from PySide6.QtCore import Qt
