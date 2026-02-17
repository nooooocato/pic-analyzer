import sqlite3
import pytest
import os
from src.app.database import DatabaseManager

@pytest.fixture
def db_manager(tmp_path):
    db_path = tmp_path / "test_images.db"
    return DatabaseManager(str(db_path))

def test_tables_created(db_manager):
    conn = sqlite3.connect(db_manager.db_path)
    cursor = conn.cursor()
    
    # Check for images table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='images'")
    assert cursor.fetchone() is not None
    
    # Check for analysis_results table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='analysis_results'")
    assert cursor.fetchone() is not None
    
    # Check for plugin_metadata table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='plugin_metadata'")
    assert cursor.fetchone() is not None
    
    conn.close()

def test_images_schema(db_manager):
    conn = sqlite3.connect(db_manager.db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(images)")
    columns = {col[1] for col in cursor.fetchall()}
    expected = {'id', 'path', 'filename', 'file_size', 'created_at', 'modified_at', 'thumbnail'}
    assert expected.issubset(columns)
    conn.close()

def test_switch_database(tmp_path):
    db1_path = str(tmp_path / "db1.db")
    db2_path = str(tmp_path / "db2.db")
    
    manager = DatabaseManager(db1_path)
    assert manager.db_path == db1_path
    assert os.path.exists(db1_path)
    
    manager.switch_database(db2_path)
    assert manager.db_path == db2_path
    assert os.path.exists(db2_path)
    
    # Verify tables exist in the new DB
    conn = sqlite3.connect(db2_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='images'")
    assert cursor.fetchone() is not None
    conn.close()
