from PySide6.QtGui import QPalette, QColor, QGuiApplication
from PySide6.QtCore import Qt

class Theme:
    """Provides system-aware colors and Fluent Design geometry/style templates."""
    
    @staticmethod
    def is_dark_mode():
        return QGuiApplication.styleHints().colorScheme() == Qt.ColorScheme.Dark

    @staticmethod
    def get_color(role: QPalette.ColorRole) -> QColor:
        return QGuiApplication.palette().color(role)

    # Fluent Design Geometry
    SPACING_XS = 4
    SPACING_S = 8
    SPACING_M = 12
    SPACING_L = 16
    SPACING_XL = 24
    
    # Windows 11 Standard Radii
    RADIUS_S = 4
    RADIUS_M = 8
    RADIUS_L = 12
    
    FONT_FAMILY = "Segoe UI Variable, Segoe UI, sans-serif"
    
    @staticmethod
    def get_overlay_bg_qss():
        if Theme.is_dark_mode():
            return "background-color: #2d2d2d; border: 1px solid #3d3d3d;"
        else:
            return "background-color: #ffffff; border: 1px solid #d1d1d1;"

    @staticmethod
    def get_menu_qss():
        """Explicitly style QMenu to prevent transparent/black background issues."""
        if Theme.is_dark_mode():
            bg = "#2d2d2d"
            text = "#ffffff"
            hover = "#3d3d3d"
        else:
            bg = "#ffffff"
            text = "#000000"
            hover = "#f0f0f0"
            
        return f"""
            QMenu {{
                background-color: {bg};
                color: {text};
                border: 1px solid rgba(128, 128, 128, 60);
                padding: 4px;
            }}
            QMenu::item {{
                padding: 6px 24px;
                border-radius: {Theme.RADIUS_S}px;
            }}
            QMenu::item:selected {{
                background-color: {hover};
            }}
        """

    @staticmethod
    def get_button_qss(circular=False):
        radius = 18 if circular else Theme.RADIUS_S
        return f"""
            QPushButton {{
                border-radius: {radius}px;
                padding: 5px 10px;
                background-color: transparent;
            }}
            QPushButton:hover {{
                background-color: rgba(128, 128, 128, 40);
            }}
        """
