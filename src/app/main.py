import sys
import logging
from PySide6.QtWidgets import QApplication
from src.app.state import state
from src.app.logger import setup_logging
from src.ui.main_window.logic import MainWindow

def main():
    """Main application entry point."""
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting Pic-Analyzer...")
    
    app = QApplication(sys.argv)
    
    # Initialize global state/core services
    state.initialize()
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
