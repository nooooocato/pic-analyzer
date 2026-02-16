from PySide6.QtWidgets import QTreeView, QFrame
from qfluentwidgets import TreeView

class MainWindowLayout:
    """Helper class to provide components for MainWindow."""
    def __init__(self):
        # We use qfluentwidgets.TreeView for a better look
        self.tree_view = TreeView()
        self.tree_view.setEditTriggers(QTreeView.NoEditTriggers)
        self.tree_view.setHeaderHidden(False)
