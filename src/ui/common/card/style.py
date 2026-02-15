from src.ui.theme import Theme

def get_style():
    return f"""
        QFrame#Card {{
            {Theme.get_overlay_bg_qss()}
            border-radius: {Theme.RADIUS_M}px;
        }}
    """
