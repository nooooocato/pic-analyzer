import pytest
from unittest.mock import patch, MagicMock
from src.ui.theme import Theme
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication
import qfluentwidgets

def test_is_dark_mode():
    # Should use qfluentwidgets implementation or remain compatible
    # qfluentwidgets has isDarkTheme()
    with patch('qfluentwidgets.isDarkTheme', return_value=True):
        assert Theme.is_dark_mode() is True

def test_apply_theme():
    # This method should exist and call qfluentwidgets.setTheme
    app = QApplication.instance() or QApplication([])
    
    with patch('qfluentwidgets.setTheme') as mock_set_theme:
        Theme.apply_theme(app)
        # Verify it was called (arguments might vary, but at least it should be called)
        assert mock_set_theme.called

def test_get_color():
    # Needs a running app to access palette
    app = QApplication.instance() or QApplication([])
    color = Theme.get_color(QPalette.Window)
    assert isinstance(color, QColor)

def test_qss_fragments():
    # Test QSS generation methods
    with patch('qfluentwidgets.isDarkTheme', return_value=True):
        overlay_qss_dark = Theme.get_overlay_bg_qss()
        assert "background-color: #2d2d2d" in overlay_qss_dark
        
        menu_qss_dark = Theme.get_menu_qss()
        assert "background-color: #2d2d2d" in menu_qss_dark

    with patch('qfluentwidgets.isDarkTheme', return_value=False):
        overlay_qss_light = Theme.get_overlay_bg_qss()
        assert "background-color: #ffffff" in overlay_qss_light

        menu_qss_light = Theme.get_menu_qss()
        assert "background-color: #ffffff" in menu_qss_light

    btn_qss = Theme.get_button_qss()
    assert "QPushButton" in btn_qss
    assert "border-radius: 4px" in btn_qss

    btn_qss_circular = Theme.get_button_qss(circular=True)
    assert "border-radius: 18px" in btn_qss_circular
