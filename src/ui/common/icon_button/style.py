from src.ui.theme import Theme

def get_style(circular=False):
    radius = 18 if circular else Theme.RADIUS_S
    return f"""
        QPushButton {{
            background-color: {Theme.BUTTON_BG};
            border: 1px solid {Theme.BORDER_SUBTLE};
            border-radius: {radius}px;
            padding: 4px;
        }}
        QPushButton:hover {{
            background-color: rgba(0, 120, 212, 220);
            border: 1px solid {Theme.ACCENT_PRIMARY};
        }}
        QPushButton:pressed {{
            background-color: {Theme.ACCENT_TERTIARY};
        }}
    """
