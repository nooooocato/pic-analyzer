from src.ui.theme import Theme

def get_style():
    # Keep it dark for image viewing experience, using a semi-transparent black
    # Style the navigation buttons with circular semi-transparent white background
    return """
        QFrame#ImageViewerOverlay {
            background-color: rgba(0, 0, 0, 0.85);
        }
        
        TransparentToolButton#navButtonBack,
        TransparentToolButton#navButtonPrev,
        TransparentToolButton#navButtonNext {
            background-color: rgba(255, 255, 255, 0.15);
            border: none;
        }
        
        TransparentToolButton#navButtonBack:hover,
        TransparentToolButton#navButtonPrev:hover,
        TransparentToolButton#navButtonNext:hover {
            background-color: rgba(255, 255, 255, 0.3);
        }
        
        TransparentToolButton#navButtonBack:pressed,
        TransparentToolButton#navButtonPrev:pressed,
        TransparentToolButton#navButtonNext:pressed {
            background-color: rgba(255, 255, 255, 0.1);
        }
        
        TransparentToolButton#navButtonBack {
            border-radius: 20px;
        }
        
        TransparentToolButton#navButtonPrev,
        TransparentToolButton#navButtonNext {
            border-radius: 32px;
        }
    """
