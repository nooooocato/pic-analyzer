import pytest
import sqlite3
import os
from src.database import DatabaseManager

def test_get_numeric_metrics(tmp_path):
    db_path = str(tmp_path / "test.db")
    db = DatabaseManager(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Add dummy image
    cursor.execute("INSERT INTO images (path, filename) VALUES (?, ?)", ("p1", "f1"))
    img_id = cursor.lastrowid
    
    # Add metrics: some numeric, some not
    cursor.execute("INSERT INTO analysis_results (image_id, plugin_name, result_key, result_value) VALUES (?, ?, ?, ?)", 
                   (img_id, "p1", "size_kb", "10.5"))
    cursor.execute("INSERT INTO analysis_results (image_id, plugin_name, result_key, result_value) VALUES (?, ?, ?, ?)", 
                   (img_id, "p1", "color", "red"))
    cursor.execute("INSERT INTO analysis_results (image_id, plugin_name, result_key, result_value) VALUES (?, ?, ?, ?)", 
                   (img_id, "p1", "density", "0.99"))
    conn.commit()
    conn.close()
    
    # We need to implement get_numeric_metrics in DatabaseManager
    metrics = db.get_numeric_metrics()
    assert "file_size" in metrics
    assert "modified_at" in metrics
    assert "size_kb" in metrics
    assert "density" in metrics
    assert "color" not in metrics
