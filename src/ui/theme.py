from PySide6.QtGui import QColor

class Theme:
    """Single source of truth for global styling constants."""
    
    # Fluent Design - Neutral Colors
    BACKGROUND_LIGHT = "#f3f3f3"
    BACKGROUND_DARK = "#202020"
    
    SURFACE_LIGHT = "#ffffff"
    SURFACE_DARK = "#2d2d2d"
    
    # Accent Colors (Windows 11 Blue)
    ACCENT_PRIMARY = "#0078d4"
    ACCENT_SECONDARY = "#2b88d8"
    ACCENT_TERTIARY = "#c7e0f4"
    
    # Text Colors
    TEXT_PRIMARY = "#1b1b1b"
    TEXT_SECONDARY = "#5f5f5f"
    TEXT_INVERTED = "#ffffff"
    
    # State Colors
    SUCCESS = "#107c10"
    ERROR = "#d13438"
    WARNING = "#ffb900"
    
    # Transparency
    OVERLAY_BG = "rgba(245, 245, 245, 240)"
    BUTTON_BG = "rgba(255, 255, 255, 200)"
    BORDER_SUBTLE = "rgba(0, 0, 0, 80)"
    
    # Spacing & Radii
    SPACING_XS = 4
    SPACING_S = 8
    SPACING_M = 12
    SPACING_L = 16
    SPACING_XL = 24
    
    RADIUS_S = 4
    RADIUS_M = 8
    RADIUS_L = 12
    
    # Fonts
    FONT_FAMILY = "Segoe UI Variable, Segoe UI, sans-serif"
    FONT_SIZE_BODY = 10
    FONT_SIZE_TITLE = 14

    @staticmethod
    def get_qcolor(hex_color: str, alpha: int = 255) -> QColor:
        """Helper to convert hex string to QColor."""
        color = QColor(hex_color)
        if alpha < 255:
            color.setAlpha(alpha)
        return color

    # Common QSS Fragments
    COMMON_BUTTON_STYLE = f"""
        QPushButton {{
            background-color: {BUTTON_BG};
            border: 1px solid {BORDER_SUBTLE};
            border-radius: {RADIUS_S}px;
            padding: 4px;
            font-family: {FONT_FAMILY};
        }}
        QPushButton:hover {{
            background-color: rgba(0, 120, 212, 220);
            border: 1px solid {ACCENT_PRIMARY};
        }}
        QPushButton:pressed {{
            background-color: {ACCENT_TERTIARY};
        }}
    """
    
    CARD_STYLE = f"""
        QFrame#Card {{
            background-color: {SURFACE_LIGHT};
            border: 1px solid {BORDER_SUBTLE};
            border-radius: {RADIUS_M}px;
        }}
    """
