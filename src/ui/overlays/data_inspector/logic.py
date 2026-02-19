import os
import datetime
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QStandardItem
from src.app.state import state
from src.app.communicator import Communicator
from .layout import DataInspectorLayout
from .style import get_style

class DataInspector(QWidget):
    """Standalone widget for displaying image metadata."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout_engine = DataInspectorLayout()
        self.layout_engine.setup_ui(self)
        self.setStyleSheet(get_style())
        
        # Subscribe to global communicator
        self.communicator = Communicator()
        self.communicator.image_selected.connect(self._on_image_selected)

    def _on_image_selected(self, file_path: str):
        """Update the display when a new image is selected."""
        if not os.path.exists(file_path):
            return
            
        # Try to get metadata from database
        metadata = state.db_manager.get_image_metadata(file_path)
        
        if not metadata:
            # Fallback to filesystem
            try:
                stats = os.stat(file_path)
                metadata = {
                    "Filename": os.path.basename(file_path),
                    "Path": file_path,
                    "Size": f"{stats.st_size / 1024:.2f} KB",
                    "Modified": stats.st_mtime,
                }
            except Exception:
                return
        else:
            metadata["Path"] = file_path
            
        self.update_metadata(metadata)

    def update_metadata(self, metadata: dict):
        """Populate the tree view with metadata."""
        model = self.layout_engine.model
        model.removeRows(0, model.rowCount())
        
        for key, value in metadata.items():
            display_value = str(value)
            # Format timestamps if applicable
            if "Modified" in key or "timestamp" in key.lower() or "created" in key.lower():
                try:
                    # Handle both float/int timestamps and string ISO dates if needed
                    ts = float(value)
                    dt = datetime.datetime.fromtimestamp(ts)
                    display_value = dt.strftime("%Y-%m-%d %H:%M:%S")
                except (ValueError, TypeError):
                    pass
            
            model.appendRow([QStandardItem(str(key)), QStandardItem(display_value)])
        
        self.layout_engine.tree_view.expandAll()
