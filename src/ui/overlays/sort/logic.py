from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction
from qfluentwidgets import CommandBar, RoundMenu, Action, FluentIcon
from .layout import SortOverlayLayout

class SortOverlay(CommandBar):
    """Floating overlay for sorting selection using CommandBar."""
    sortRequested = Signal(str)  # Signal emitting the plugin name

    def __init__(self, sort_manager, parent=None):
        super().__init__(parent)
        self.sort_manager = sort_manager
        
        self.setWindowFlags(Qt.SubWindow)
        
        self.layout_engine = SortOverlayLayout()
        self.sort_action = self.layout_engine.setup_ui(self)
        
        # Create and set the menu
        self.sort_menu = self.create_menu()
        self.sort_action.setMenu(self.sort_menu)
        
        self.adjustSize()

    def create_menu(self):
        menu = RoundMenu(parent=self)
        
        plugins = self.sort_manager.plugins.keys()
        for plugin_name in plugins:
            # Use qfluentwidgets.Action for better compatibility with RoundMenu
            # We don't have specific icons for each plugin yet, using a generic one
            action = Action(FluentIcon.TAG, plugin_name, self)
            menu.addAction(action)
            self._connect_action(action, plugin_name)
        return menu

    def _connect_action(self, action, plugin_name):
        action.triggered.connect(lambda: self.sortRequested.emit(plugin_name))
