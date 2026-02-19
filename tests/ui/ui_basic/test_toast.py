import pytest
from PySide6.QtCore import Qt
from src.ui.common.toast.logic import Toast

def test_toast_initial_state(qtbot):
    toast = Toast("Test Message")
    qtbot.addWidget(toast)
    assert toast.isHidden()
    assert toast.layout_engine.label.text() == "Test Message"

def test_toast_show_hide(qtbot):
    toast = Toast("Test Message", duration=100)
    qtbot.addWidget(toast)
    
    toast.show_message()
    assert toast.isVisible()
    assert toast.opacity_effect.opacity() == 0.0 # Animation starts at 0
    
    # Wait for timer and animation to finish
    qtbot.wait(500)
    assert toast.isHidden()
