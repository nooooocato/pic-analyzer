from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QMenu
from src.ui.common.card.logic import Card
from .layout import SortOverlayLayout
from .style import get_style

class SortOverlay(Card):
    """Floating overlay for sorting selection."""
    sortRequested = Signal(str, str)  # Signal emitting (metric, plugin_name)

    def __init__(self, sort_manager, db_manager, parent=None):
        super().__init__(parent, setup_layout=False)
        self.sort_manager = sort_manager
        self.db_manager = db_manager
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
        
        metrics = self.db_manager.get_numeric_metrics()
        plugins = self.sort_manager.plugins.keys()
        
        for metric in metrics:
            metric_menu = menu.addMenu(metric.replace("_", " ").title())
            for plugin_name in plugins:
                action = metric_menu.addAction(plugin_name)
                self._connect_action(action, metric, plugin_name)
        return menu

    def _connect_action(self, action, metric, plugin_name):
        action.triggered.connect(lambda: self.sortRequested.emit(metric, plugin_name))
