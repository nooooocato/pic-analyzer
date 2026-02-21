def get_style():
    return """
        QScrollArea {
            border: none;
            background: transparent;
        }
        QSplitter::handle {
            background-color: #3d3d3d;
            height: 4px;
            margin: 2px 0;
        }
        QSplitter::handle:hover {
            background-color: #555;
        }
        QPushButton#ApplyButton {
            margin-top: 10px;
            padding: 8px;
            font-weight: bold;
        }
    """
