import pytest
from PySide6.QtWidgets import QWidget
from src.ui.common.toast.logic import Toast
from src.app.communicator import Communicator

def test_toast_subscribes_to_communicator(qtbot):
    """Test that Toast automatically shows when Communicator.notify is emitted."""
    parent = QWidget()
    toast = Toast("", parent=parent)
    qtbot.addWidget(parent)
    parent.show()
    
    # Initially hidden
    assert not toast.isVisible()
    
    # Emit signal
    comm = Communicator()
    comm.notify.emit("Decoupled Message", "INFO")
    
    # Wait for show (animations might be involved but we can check if it was triggered)
    # Since show_message is called, isVisible() should eventually be true.
    # Note: We might need a small delay or processEvents if there's no animation blocking.
    qtbot.wait_until(lambda: toast.isVisible(), timeout=1000)
    
    assert toast.layout_engine.label.text() == "Decoupled Message"
