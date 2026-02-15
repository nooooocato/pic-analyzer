from src.ui.theme import Theme

def get_style():
    return f"""
        QFrame#Card {{
            background-color: {Theme.OVERLAY_BG};
            border: 1px solid {Theme.BORDER_SUBTLE};
            border-radius: {Theme.RADIUS_M}px;
        }}
    """
