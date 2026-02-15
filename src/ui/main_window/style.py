from src.ui.theme import Theme

def get_style():
    return f"""
        QMainWindow {{
            background-color: {Theme.BACKGROUND_LIGHT};
        }}
        QMenuBar {{
            background-color: {Theme.SURFACE_LIGHT};
            border-bottom: 1px solid {Theme.BORDER_SUBTLE};
        }}
        QToolBar {{
            background-color: {Theme.SURFACE_LIGHT};
            border-bottom: 1px solid {Theme.BORDER_SUBTLE};
            spacing: 10px;
        }}
        QDockWidget {{
            titlebar-close-icon: url(none);
            titlebar-normal-icon: url(none);
        }}
    """
