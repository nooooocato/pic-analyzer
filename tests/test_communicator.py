import pytest
from PySide6.QtCore import QObject, Signal
from src.app.communicator import Communicator

def test_communicator_singleton():
    """Test that Communicator follows the singleton pattern."""
    comm1 = Communicator()
    comm2 = Communicator()
    assert comm1 is comm2

def test_notify_signal(qtbot):
    """Test that the notify signal is emitted correctly."""
    comm = Communicator()
    with qtbot.waitSignal(comm.notify, timeout=1000) as blocker:
        comm.notify.emit("Test Message", "INFO")
    
    assert blocker.signal_triggered
    assert blocker.args == ["Test Message", "INFO"]
