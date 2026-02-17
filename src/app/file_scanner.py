import os
import logging
import datetime
from PySide6.QtCore import QRunnable, QObject, Signal
from src.ui.thumbnail_gen import ThumbnailGenerator
from src.db.manager import DBManager
from src.db.models import Image, Workspace

logger = logging.getLogger(__name__)

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

    def __init__(self, folder_path, db_path=None):
        super().__init__()
        self.folder_path = folder_path
        self.db_path = db_path
        self.signals = ScannerSignals()
        self.thumbnail_gen = ThumbnailGenerator()
        self._is_cancelled = False

    def cancel(self):
        self._is_cancelled = True

    def run(self):
        logger.info(f"Starting scan for folder: {self.folder_path}")
        db_manager = None
        workspace = None
        
        if self.db_path:
            try:
                db_manager = DBManager(self.db_path)
                logger.debug(f"Connected to database at {self.db_path}")
                # Ensure workspace exists
                workspace = db_manager.manage_workspace("create", {
                    "name": os.path.basename(self.folder_path),
                    "path": self.folder_path
                })
            except Exception as e:
                logger.error(f"Failed to connect to database: {e}")
        
        try:
            count = 0
            for root, _, files in os.walk(self.folder_path):
                if self._is_cancelled:
                    logger.info("Scan cancelled.")
                    return

                for file in files:
                    if self._is_cancelled:
                        return
                        
                    ext = os.path.splitext(file)[1].lower()
                    if ext in self.SUPPORTED_EXTENSIONS:
                        file_path = os.path.join(root, file)
                        logger.debug(f"Processing image: {file_path}")
                        
                        thumb_bytes = None
                        stats = os.stat(file_path)
                        modified_at = int(stats.st_mtime)
                        
                        if db_manager:
                            # Check if already in DB and if it has changed
                            try:
                                img = Image.get_or_none(Image.path == file_path)
                                if img and img.thumbnail:
                                    if img.file_size == int(stats.st_size) and img.modified_at == modified_at:
                                        logger.debug(f"Loading thumbnail from cache for {file}")
                                        thumb_bytes = img.thumbnail
                            except Exception as db_e:
                                logger.warning(f"Database read error for {file}: {db_e}")
                        
                        if not thumb_bytes:
                            logger.debug(f"Generating new thumbnail for {file}")
                            thumb_bytes = self.thumbnail_gen.generate(file_path)
                            if thumb_bytes and db_manager:
                                try:
                                    # Save to DB using upsert
                                    db_manager.upsert_image({
                                        "path": file_path,
                                        "filename": os.path.basename(file_path),
                                        "file_size": int(stats.st_size),
                                        "modified_at": modified_at,
                                        "workspace": workspace,
                                        "thumbnail": thumb_bytes
                                    }, {})
                                except Exception as db_e:
                                    logger.warning(f"Database write error for {file}: {db_e}")
                        
                        if thumb_bytes:
                            self.signals.file_found.emit(file_path, thumb_bytes)
                            count += 1
                        else:
                            logger.warning(f"No thumbnail generated for {file_path}")
            
            logger.info(f"Scan finished. Found {count} images.")
            self.signals.finished.emit()
        except Exception as e:
            logger.exception(f"Unexpected error during scan: {e}")
            self.signals.error.emit(str(e))
