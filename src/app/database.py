import sqlite3
import os

class DatabaseManager:
    """Manages SQLite database operations for image metadata and analysis results.

    This class handles database initialization, schema management, and provides
    methods for retrieving metrics and image-specific metadata.

    Attributes:
        db_path (str): The file path to the SQLite database.
    """

    def __init__(self, db_path: str):
        """Initializes the DatabaseManager with the specified database path.

        Args:
            db_path (str): The path to the SQLite database file.
        """
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        """Initializes the database schema if it doesn't already exist.

        Creates tables for images, analysis_results, and plugin_metadata.
        Also handles basic schema migrations for existing databases.
        """
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

    def switch_database(self, new_db_path: str):
        """Closes connection to current DB (any) and opens/initializes a new one."""
        self.db_path = new_db_path
        self._initialize_db()

    def get_numeric_metrics(self) -> list[str]:
        """
        Returns a list of keys (from images table or analysis_results) that contain numeric values.
        
        Returns:
            list[str]: A list of metric keys that can be used for numeric sorting.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Start with standard numeric columns from the images table
        numeric_keys = ["file_size", "modified_at"]
        
        # Get unique keys from analysis_results
        try:
            cursor.execute("SELECT DISTINCT result_key FROM analysis_results")
            keys = [row[0] for row in cursor.fetchall()]
            
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
        except sqlite3.OperationalError:
            # Table might not exist yet
            pass
        
        conn.close()
        return numeric_keys

    def get_metric_values(self, metric_key: str) -> dict[str, float]:
        """
        Returns a mapping of image path to its numeric value for the given metric.
        
        Args:
            metric_key (str): The metric key to fetch values for.
            
        Returns:
            dict[str, float]: A dictionary mapping file paths to numeric values.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        results = {}
        
        if metric_key in ["file_size", "modified_at"]:
            cursor.execute(f"SELECT path, {metric_key} FROM images")
            for path, val in cursor.fetchall():
                results[path] = float(val) if val is not None else 0.0
        else:
            cursor.execute("""
                SELECT images.path, analysis_results.result_value 
                FROM images 
                JOIN analysis_results ON images.id = analysis_results.image_id 
                WHERE analysis_results.result_key = ?
            """, (metric_key,))
            for path, val in cursor.fetchall():
                try:
                    results[path] = float(val)
                except (ValueError, TypeError):
                    pass
        
        conn.close()
        return results

    def get_image_metadata(self, path: str) -> dict:
        """
        Fetches all stored metadata and analysis results for a given image path.
        
        Args:
            path (str): The absolute path to the image.
            
        Returns:
            dict: A dictionary of metadata keys and values.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get basic info from images table
        cursor.execute("SELECT id, filename, file_size, modified_at FROM images WHERE path = ?", (path,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return {}
            
        img_id, filename, size, modified = row
        metadata = {
            "Filename": filename,
            "Size": f"{size / 1024:.2f} KB" if size else "Unknown",
            "Modified": modified
        }
        
        # Get analysis results
        cursor.execute("SELECT result_key, result_value FROM analysis_results WHERE image_id = ?", (img_id,))
        for key, val in cursor.fetchall():
            # Try to format numeric values
            try:
                f_val = float(val)
                metadata[key] = f"{f_val:.4f}" if "." in val else val
            except (ValueError, TypeError):
                metadata[key] = val
                
        conn.close()
        return metadata
