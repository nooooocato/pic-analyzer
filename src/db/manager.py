from peewee import SqliteDatabase
from .models import db_proxy, Workspace, Image, AnalysisResult
import os

class DBManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.db = None
        self._initialize_db()

    def _initialize_db(self):
        """Initializes the database connection and creates tables if they don't exist."""
        self.db = SqliteDatabase(self.db_path)
        db_proxy.initialize(self.db)
        
        # Ensure tables exist
        self.db.create_tables([Workspace, Image, AnalysisResult])

    def switch_database(self, new_db_path: str):
        """Closes the current connection and opens a new one."""
        if self.db:
            self.db.close()
        
        self.db_path = new_db_path
        self._initialize_db()

    def get_db(self):
        return self.db
