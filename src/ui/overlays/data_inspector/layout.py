from PySide6.QtWidgets import QVBoxLayout, QTreeView, QWidget
from PySide6.QtGui import QStandardItemModel

class DataInspectorLayout:
    def setup_ui(self, widget: QWidget):
        self.layout = QVBoxLayout(widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.tree_view = QTreeView()
        self.tree_view.setEditTriggers(QTreeView.NoEditTriggers)
        self.layout.addWidget(self.tree_view)
        
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Property", "Value"])
        self.tree_view.setModel(self.model)
