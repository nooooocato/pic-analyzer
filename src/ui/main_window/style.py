from src.ui.theme import Theme

def get_style():
    # Let standard widgets use system palette for colors
    return f"""
        QMainWindow {{
            border: none;
        }}
        QMenuBar {{
            border-bottom: 1px solid rgba(128, 128, 128, 30);
            padding: 2px;
        }}
        QToolBar {{
            border-bottom: 1px solid rgba(128, 128, 128, 30);
            spacing: 8px;
            padding: 8px;
        }}
        QDockWidget {{
            border: 1px solid rgba(128, 128, 128, 30);
            margin: 4px;
        }}
    """
