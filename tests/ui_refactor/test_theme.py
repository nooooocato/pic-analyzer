from src.ui.theme import Theme
from PySide6.QtGui import QColor

def test_theme_colors():
    assert Theme.ACCENT_PRIMARY == "#0078d4"
    assert Theme.BACKGROUND_LIGHT == "#f3f3f3"

def test_get_qcolor():
    color = Theme.get_qcolor(Theme.ACCENT_PRIMARY)
    assert isinstance(color, QColor)
    assert color.name() == "#0078d4"

def test_spacing_constants():
    assert Theme.SPACING_M == 12
    assert Theme.RADIUS_M == 8

def test_qss_fragments():
    assert "QPushButton" in Theme.COMMON_BUTTON_STYLE
    assert Theme.ACCENT_PRIMARY in Theme.COMMON_BUTTON_STYLE
