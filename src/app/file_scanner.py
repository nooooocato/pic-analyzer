import os
import sqlite3
import logging
from PySide6.QtCore import QRunnable, QObject, Signal
from src.ui.thumbnail_gen import ThumbnailGenerator

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

    def run(self):
        logger.info(f"Starting scan for folder: {self.folder_path}")
        conn = None
        if self.db_path:
            try:
                conn = sqlite3.connect(self.db_path)
                logger.debug(f"Connected to database at {self.db_path}")
            except Exception as e:
                logger.error(f"Failed to connect to database: {e}")
        
        try:
            count = 0
            for root, _, files in os.walk(self.folder_path):
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in self.SUPPORTED_EXTENSIONS:
                        file_path = os.path.join(root, file)
                        logger.debug(f"Processing image: {file_path}")
                        
                        thumb_bytes = None
                        stats = os.stat(file_path)
                        if conn:
                            # Check if already in DB and if it has changed
                            try:
                                cursor = conn.cursor()
                                cursor.execute(
                                    "SELECT thumbnail, file_size, modified_at FROM images WHERE path = ?", 
                                    (file_path,)
                                )
                                row = cursor.fetchone()
                                if row and row[0]:
                                    db_thumb, db_size, db_mtime = row
                                    if db_size == int(stats.st_size) and db_mtime == int(stats.st_mtime):
                                        logger.debug(f"Loading thumbnail from cache for {file}")
                                        thumb_bytes = db_thumb
                            except Exception as db_e:
                                logger.warning(f"Database read error for {file}: {db_e}")
                        
                        if not thumb_bytes:
                            logger.debug(f"Generating new thumbnail for {file}")
                            thumb_bytes = self.thumbnail_gen.generate(file_path)
                            if thumb_bytes and conn:
                                try:
                                    # Save to DB
                                    filename = os.path.basename(file_path)
                                    cursor = conn.cursor()
                                    cursor.execute(
                                        """INSERT OR REPLACE INTO images 
                                        (path, filename, file_size, modified_at, thumbnail) 
                                        VALUES (?, ?, ?, ?, ?)""",
                                        (file_path, filename, int(stats.st_size), 
                                         int(stats.st_mtime), thumb_bytes)
                                    )
                                    conn.commit()
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
        finally:
            if conn:
                conn.close()
