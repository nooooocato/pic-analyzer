import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create images table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT NOT NULL UNIQUE,
                filename TEXT NOT NULL,
                file_size INTEGER,
                created_at TIMESTAMP,
                modified_at TIMESTAMP,
                thumbnail BLOB
            )
        ''')

        # Create analysis_results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_id INTEGER,
                plugin_name TEXT,
                result_key TEXT,
                result_value TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (image_id) REFERENCES images (id)
            )
        ''')

        # Create plugin_metadata table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plugin_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                version TEXT,
                description TEXT,
                enabled INTEGER DEFAULT 1
            )
        ''')

        conn.commit()
        
        # Schema migration: check for thumbnail column
        try:
            cursor.execute("PRAGMA table_info(images)")
            columns = [col[1] for col in cursor.fetchall()]
            if 'thumbnail' not in columns:
                cursor.execute("ALTER TABLE images ADD COLUMN thumbnail BLOB")
                conn.commit()
        except Exception:
            pass
            
        conn.close()

    def switch_database(self, new_db_path):
        """Closes connection to current DB (if any) and opens/initializes a new one."""
        self.db_path = new_db_path
        self._initialize_db()

    def get_numeric_metrics(self):
        """
        Returns a list of result_keys that contain numeric values in the analysis_results table.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get unique keys
        cursor.execute("SELECT DISTINCT result_key FROM analysis_results")
        keys = [row[0] for row in cursor.fetchall()]
        
        numeric_keys = []
        for key in keys:
            # Check if the first value for this key is numeric
            cursor.execute("SELECT result_value FROM analysis_results WHERE result_key = ? LIMIT 1", (key,))
            row = cursor.fetchone()
            if row:
                try:
                    float(row[0])
                    numeric_keys.append(key)
                except (ValueError, TypeError):
                    pass
        
        conn.close()
        return numeric_keys
