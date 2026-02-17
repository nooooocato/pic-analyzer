import os
import logging
from typing import Optional, List
from src.plugin.manager import PluginManager
from src.db.manager import DBManager

logger = logging.getLogger(__name__)

class AppState:
    """Centralized application-wide state and core services."""
    def __init__(self):
        self.current_folder: Optional[str] = None
        self.active_scanners: List = []
        self.current_viewer_index: int = -1
        
        # Core Services
        self.db_manager: Optional[DBManager] = None
        self.plugin_manager: Optional[PluginManager] = None
        
        self.initialized = False

    def initialize(self, plugins_dir: str = "plugins", default_db: str = "app_metadata.db"):
        """Initializes core application services."""
        if self.initialized:
            return
            
        self.plugin_manager = PluginManager(plugins_dir)
        self.db_manager = DBManager(default_db)
        self.initialized = True
        logger.info("Application state initialized.")

    def set_current_folder(self, folder: str):
        """Updates the current workspace folder."""
        self.current_folder = folder
        logger.info(f"Workspace changed to: {folder}")
        
        if self.db_manager and self.current_folder:
            # Ensure workspace exists in DB
            self.db_manager.manage_workspace("create", {
                "name": os.path.basename(self.current_folder),
                "path": self.current_folder
            })

# Global instance
state = AppState()
