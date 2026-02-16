from PySide6.QtCore import Qt, Signal
from qfluentwidgets import SimpleCardWidget, CommandBar, RoundMenu, Action, FluentIcon
from .layout import SortOverlayLayout

class SortOverlay(SimpleCardWidget):
    """Floating overlay for sorting selection using Card with CommandBar."""
    sortRequested = Signal(str)  # Signal emitting the plugin name

    def __init__(self, sort_manager, parent=None):
        super().__init__(parent)
        self.sort_manager = sort_manager
        
        self.setWindowFlags(Qt.SubWindow)
        
        # Use a CommandBar inside the Card for standard Fluent look
        self.command_bar = CommandBar(self)
        
        self.layout_engine = SortOverlayLayout()
        self.sort_action = self.layout_engine.setup_ui(self.command_bar)
        
        # Create and set the menu
        self.sort_menu = self.create_menu()
        self.sort_action.setMenu(self.sort_menu)
        
        # Ensure the command bar is positioned correctly within the Card
        # or use a layout in the Card
        from PySide6.QtWidgets import QVBoxLayout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.command_bar)
        
        self.adjustSize()

    def create_menu(self):
        menu = RoundMenu(parent=self)
        plugins = self.sort_manager.plugins.keys()
        for plugin_name in plugins:
            action = Action(FluentIcon.TAG, plugin_name, self)
            menu.addAction(action)
            self._connect_action(action, plugin_name)
        return menu

    def _connect_action(self, action, plugin_name):
        action.triggered.connect(lambda: self.sortRequested.emit(plugin_name))
