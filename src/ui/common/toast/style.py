from src.ui.theme import Theme

def get_style():
    return f"""
        QFrame#Toast {{
            background-color: rgba(32, 32, 32, 200);
            border-radius: {Theme.RADIUS_M}px;
            border: 1px solid rgba(255, 255, 255, 30);
        }}
        QLabel {{
            color: white;
            font-family: {Theme.FONT_FAMILY};
            font-size: 12px;
        }}
    """
