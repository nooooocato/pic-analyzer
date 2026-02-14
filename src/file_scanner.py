import os
from PySide6.QtCore import QRunnable, QObject, Signal
from src.ui.thumbnail_gen import ThumbnailGenerator

class ScannerSignals(QObject):
    """Signals for the FolderScanner."""
    file_found = Signal(str, bytes) # path, thumbnail_bytes
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
        self.thumbnail_gen = ThumbnailGenerator()

    def run(self):
        try:
            for root, _, files in os.walk(self.folder_path):
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in self.SUPPORTED_EXTENSIONS:
                        file_path = os.path.join(root, file)
                        thumb_bytes = self.thumbnail_gen.generate(file_path)
                        if thumb_bytes:
                            self.signals.file_found.emit(file_path, thumb_bytes)
            self.signals.finished.emit()
        except Exception as e:
            self.signals.error.emit(str(e))
