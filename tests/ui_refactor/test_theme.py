import pytest
from src.ui.theme import Theme
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication

def test_is_dark_mode():
    # Should not crash
    Theme.is_dark_mode()

def test_get_color():
    # Needs a running app to access palette
    app = QApplication.instance() or QApplication([])
    color = Theme.get_color(QPalette.Window)
    assert isinstance(color, QColor)

def test_qss_fragments():
    qss = Theme.get_overlay_bg_qss()
    assert "background-color" in qss
    
    btn_qss = Theme.get_button_qss()
    assert "QPushButton" in btn_qss
