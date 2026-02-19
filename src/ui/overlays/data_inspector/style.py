from src.ui.theme import Theme

def get_style():
    if Theme.is_dark_mode():
        bg = "#2d2d2d"
        text = "#ffffff"
        secondary = "#aaaaaa"
        header_bg = "#333333"
    else:
        bg = "#ffffff"
        text = "#000000"
        secondary = "#666666"
        header_bg = "#f3f3f3"

    return f"""
    QTreeView {{
        background-color: {bg};
        border: none;
        color: {text};
    }}
    QTreeView::item {{
        padding: 5px;
    }}
    QHeaderView::section {{
        background-color: {header_bg};
        color: {secondary};
        padding: 4px;
        border: none;
    }}
    """
