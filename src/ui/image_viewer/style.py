from src.ui.theme import Theme

def get_style():
    # Keep it dark for image viewing experience, using a semi-transparent black
    return """
        QFrame#ImageViewerOverlay {
            background-color: rgba(0, 0, 0, 0.85);
        }
    """
