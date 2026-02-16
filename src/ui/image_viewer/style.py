from src.ui.theme import Theme

def get_style():
    # Keep it dark for image viewing experience, using a semi-transparent black
    # Style the navigation buttons with circular semi-transparent white background and black icons
    return """
        QFrame#ImageViewerOverlay {
            background-color: rgba(0, 0, 0, 0.85);
        }
        
        ToolButton#navButtonBack,
        ToolButton#navButtonPrev,
        ToolButton#navButtonNext {
            background-color: rgba(255, 255, 255, 0.6);
            border: none;
        }
        
        ToolButton#navButtonBack:hover,
        ToolButton#navButtonPrev:hover,
        ToolButton#navButtonNext:hover {
            background-color: rgba(255, 255, 255, 0.8);
        }
        
        ToolButton#navButtonBack:pressed,
        ToolButton#navButtonPrev:pressed,
        ToolButton#navButtonNext:pressed {
            background-color: rgba(255, 255, 255, 0.4);
        }
        
        ToolButton#navButtonBack {
            border-radius: 20px;
        }
        
        ToolButton#navButtonPrev,
        ToolButton#navButtonNext {
            border-radius: 32px;
        }
    """
