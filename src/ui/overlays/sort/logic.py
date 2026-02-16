from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtWidgets import QVBoxLayout
from qfluentwidgets import SimpleCardWidget, TransparentDropDownToolButton, RoundMenu, Action, FluentIcon
from .layout import SortOverlayLayout

class SortOverlay(SimpleCardWidget):
    """Floating overlay for sorting selection using Card with DropDownToolButton."""
    sortRequested = Signal(str)  # Signal emitting the plugin name

    def __init__(self, sort_manager, parent=None):
        super().__init__(parent)
        self.sort_manager = sort_manager
        
        self.setWindowFlags(Qt.SubWindow)
        
        # Use a DropDownToolButton for a more compact and functional look
        self.btn_sort = TransparentDropDownToolButton(FluentIcon.FILTER, self)
        self.btn_sort.setFixedSize(32, 32)
        self.btn_sort.setIconSize(QSize(20, 20))
        
        # Create and set the menu
        self.sort_menu = self.create_menu()
        self.btn_sort.setMenu(self.sort_menu)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.addWidget(self.btn_sort)
        
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
