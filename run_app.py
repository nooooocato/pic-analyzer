import sys
import os
from PySide6.QtWidgets import QApplication

# Add plugins directory to sys.path
plugins_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "plugins"))
if plugins_path not in sys.path:
    sys.path.append(plugins_path)

from src.ui.main_window.logic import MainWindow
from src.logger import setup_logging

def main():
    """Main entry point for the Pic-Analyzer application."""
    setup_logging()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
