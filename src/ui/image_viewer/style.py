from src.ui.theme import Theme

def get_style():
    # Always dark for image viewer
    return f"""
        QFrame#ImageViewerOverlay {{
            background-color: rgba(0, 0, 0, 230);
        }}
    """

IMAGE_VIEWER_BUTTON_STYLE = """
    QPushButton {
        background-color: rgba(255, 255, 255, 30);
        border: none;
        border-radius: 20px;
        color: white;
    }
    QPushButton:hover {
        background-color: rgba(255, 255, 255, 70);
    }
    QPushButton:pressed {
        background-color: rgba(255, 255, 255, 100);
    }
"""
