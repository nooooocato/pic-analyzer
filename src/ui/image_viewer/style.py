from src.ui.theme import Theme

def get_style():
    # Background for image viewer - using a semi-transparent theme-aware color
    # Typically image viewers stay dark for focus, but we can make it adapt.
    # However, for now let's just make the buttons standard Fluent ToolButtons 
    # which already handle theme.
    return """
        QFrame#ImageViewerOverlay {
            background-color: rgba(0, 0, 0, 0.85);
        }
        
        ToolButton#navButtonBack {
            border-radius: 20px;
        }
        
        ToolButton#navButtonPrev,
        ToolButton#navButtonNext {
            border-radius: 32px;
        }
    """
