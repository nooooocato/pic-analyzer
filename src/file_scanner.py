import os
from PySide6.QtCore import QRunnable, QObject, Signal

class ScannerSignals(QObject):
    """Signals for the FolderScanner."""
    file_found = Signal(str)
    finished = Signal()
    error = Signal(str)

class FolderScanner(QRunnable):
    """
    Worker thread for recursively scanning a folder for image files.
    """
    SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}

    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path
        self.signals = ScannerSignals()

    def run(self):
        try:
            for root, _, files in os.walk(self.folder_path):
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in self.SUPPORTED_EXTENSIONS:
                        file_path = os.path.join(root, file)
                        self.signals.file_found.emit(file_path)
            self.signals.finished.emit()
        except Exception as e:
            self.signals.error.emit(str(e))
