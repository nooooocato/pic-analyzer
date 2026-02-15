from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QMenu
from src.ui.common.card.logic import Card
from .layout import SortOverlayLayout
from .style import get_style

class SortOverlay(Card):
    """Floating overlay for sorting selection."""
    sortRequested = Signal(str)  # Signal emitting the plugin name

    def __init__(self, sort_manager, parent=None):
        super().__init__(parent, setup_layout=False)
        self.sort_manager = sort_manager
        self.setObjectName("Card")
        self.setWindowFlags(Qt.SubWindow)
        
        self.layout_engine = SortOverlayLayout()
        self.layout_engine.setup_ui(self)
        
        self.setStyleSheet(self.styleSheet() + get_style())
        
        # Connect button to show menu
        self.layout_engine.btn_sort.clicked.connect(self._show_sort_menu)
        self.adjustSize()

    def _show_sort_menu(self):
        menu = self.create_menu()
        menu.exec(self.layout_engine.btn_sort.mapToGlobal(
            self.layout_engine.btn_sort.rect().bottomLeft()
        ))

    def create_menu(self):
        from src.ui.theme import Theme
        menu = QMenu(self)
        menu.setStyleSheet(Theme.get_menu_qss())
        plugins = self.sort_manager.plugins.keys()
        
        for plugin_name in plugins:
            action = menu.addAction(plugin_name)
            # Use a helper function to avoid lambda closure issues in a loop
            self._connect_action(action, plugin_name)
        return menu

    def _connect_action(self, action, plugin_name):
        action.triggered.connect(lambda: self.sortRequested.emit(plugin_name))
