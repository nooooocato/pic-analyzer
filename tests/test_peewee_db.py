import pytest
import os
from src.db.manager import DBManager
from src.db.models import Workspace, Image, AnalysisResult
from peewee import SqliteDatabase

@pytest.fixture
def db_path(tmp_path):
    return str(tmp_path / "test.db")

@pytest.fixture
def db_manager(db_path):
    manager = DBManager(db_path)
    return manager

def test_db_initialization(db_manager, db_path):
    """Test that the database is initialized and tables are created."""
    assert os.path.exists(db_path)
    assert isinstance(db_manager.db, SqliteDatabase)
    
    # Check if tables exist
    assert Workspace.table_exists()
    assert Image.table_exists()
    assert AnalysisResult.table_exists()

def test_models_schema(db_manager):
    """Test that models have the expected fields."""
    # Workspace
    workspace_fields = Workspace._meta.fields
    assert 'name' in workspace_fields
    assert 'path' in workspace_fields
    
    # Image
    image_fields = Image._meta.fields
    assert 'path' in image_fields
    assert 'filename' in image_fields
    assert 'workspace' in image_fields
    
    # AnalysisResult
    analysis_fields = AnalysisResult._meta.fields
    assert 'image' in analysis_fields
    assert 'plugin_name' in analysis_fields
    assert 'result_data' in analysis_fields

def test_db_switch(tmp_path):
    """Test switching between database files."""
    db1_path = str(tmp_path / "db1.db")
    db2_path = str(tmp_path / "db2.db")
    
    manager = DBManager(db1_path)
    assert manager.db_path == db1_path
    assert os.path.exists(db1_path)
    
    manager.switch_database(db2_path)
    assert manager.db_path == db2_path
    assert os.path.exists(db2_path)
    assert Image.table_exists()
