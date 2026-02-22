
def get_gallery_style():
    return """
        QScrollArea { background: transparent; border: none; }
        GroupedListWidget { background: transparent; outline: none; }
        QLabel#GroupHeader {
            font-weight: bold;
            font-size: 11px;
            color: #ccc;
            padding: 0 8px;
            background-color: #222;
            border-bottom: 1px solid #333;
        }
    """
