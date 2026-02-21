import sys
import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from src.app.state import state
from src.app.logger import setup_logging
from src.ui.main_window.logic import MainWindow

def main():
    """Main application entry point."""
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting Pic-Analyzer...")
    
    app = QApplication(sys.argv)
    
    # Set global default font to avoid QFont::setPointSize warnings
    default_font = QFont("Segoe UI Variable", 10)
    if default_font.exactMatch():
        app.setFont(default_font)
    else:
        app.setFont(QFont("Segoe UI", 10))
    
    # Initialize global state/core services
    state.initialize()
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
