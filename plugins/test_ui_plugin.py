from src.plugins.base import BasePlugin
from PySide6.QtGui import QAction

class TestUIPlugin(BasePlugin):
    @property
    def name(self): return "UI Test Plugin"
    @property
    def description(self): return "Injects a button"
    def run(self, path): return {}
    def initialize_ui(self, main_window):
        action = QAction("Plugin Action", main_window)
        main_window.add_toolbar_action(action)
        menu = main_window.get_menu("Plugins")
        menu.addAction(action)