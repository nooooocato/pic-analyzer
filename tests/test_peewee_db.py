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

def test_manage_workspace(db_manager):
    """Test creating, loading and deleting workspaces."""
    # Create
    ws = db_manager.manage_workspace("create", {"name": "TestWS", "path": "/path/to/ws"})
    assert ws.name == "TestWS"
    assert Workspace.get(Workspace.name == "TestWS")
    
    # Load
    loaded = db_manager.manage_workspace("load", {"name": "TestWS"})
    assert loaded.id == ws.id
    
    # Delete
    db_manager.manage_workspace("delete", {"name": "TestWS"})
    with pytest.raises(Workspace.DoesNotExist):
        Workspace.get(Workspace.name == "TestWS")

def test_upsert_image(db_manager):
    """Test inserting and updating image records."""
    ws = db_manager.manage_workspace("create", {"name": "WS1", "path": "/ws1"})
    
    metadata = {
        "path": "/ws1/img1.jpg",
        "filename": "img1.jpg",
        "file_size": 1024,
        "workspace": ws
    }
    analysis_data = {"brightness": 0.8, "tags": ["nature", "sun"]}
    
    img = db_manager.upsert_image(metadata, analysis_data)
    assert img.filename == "img1.jpg"
    assert Image.get(Image.path == "/ws1/img1.jpg")
    
    # Check analysis result
    ar = AnalysisResult.get(AnalysisResult.image == img)
    assert "brightness" in ar.result_data
    
    # Update
    metadata["file_size"] = 2048
    img2 = db_manager.upsert_image(metadata, {"brightness": 0.9})
    assert img2.id == img.id
    assert img2.file_size == 2048
    
    # Check updated analysis result
    ar2 = AnalysisResult.get(AnalysisResult.image == img2)
    assert "0.9" in ar2.result_data

def test_query_images(db_manager):
    """Test querying images with filters."""
    ws = db_manager.manage_workspace("create", {"name": "WS_QUERY", "path": "/ws_query"})
    db_manager.upsert_image({"path": "/a.jpg", "filename": "a.jpg", "workspace": ws}, {})
    db_manager.upsert_image({"path": "/b.jpg", "filename": "b.jpg", "workspace": ws}, {})
    
    query = db_manager.query_images(filters={"filename": "a.jpg"})
    assert query.count() == 1
    assert query.first().filename == "a.jpg"
    
    all_query = db_manager.query_images()
    assert all_query.count() == 2

def test_update_metrics(db_manager):
    """Test updating specific metrics for an image."""
    ws = db_manager.manage_workspace("create", {"name": "WS_METRIC", "path": "/ws_metric"})
    img = db_manager.upsert_image({"path": "/m.jpg", "filename": "m.jpg", "workspace": ws}, {"old": 1})
    
    db_manager.update_metrics(img.id, {"new_metric": 100, "old": 2})
    
    ar = AnalysisResult.get(AnalysisResult.image == img)
    assert "new_metric" in ar.result_data
    assert "100" in ar.result_data
    assert "2" in ar.result_data

def test_get_image_metadata(db_manager):
    """Test fetching full metadata for an image."""
    ws = db_manager.manage_workspace("create", {"name": "WS_META", "path": "/ws_meta"})
    img = db_manager.upsert_image({"path": "/meta.jpg", "filename": "meta.jpg", "file_size": 512, "workspace": ws}, {"brightness": 0.5})
    
    metadata = db_manager.get_image_metadata("/meta.jpg")
    assert metadata["Filename"] == "meta.jpg"
    assert "0.5000" in metadata["brightness"]
    assert "0.50 KB" in metadata["Size"]

def test_get_numeric_metrics(db_manager):
    """Test retrieving list of numeric metrics."""
    ws = db_manager.manage_workspace("create", {"name": "WS_NUM", "path": "/ws_num"})
    db_manager.upsert_image({"path": "/num.jpg", "filename": "num.jpg", "workspace": ws}, {"score": 95, "label": "cat"})
    
    metrics = db_manager.get_numeric_metrics()
    assert "file_size" in metrics
    assert "modified_at" in metrics
    assert "score" in metrics
    assert "label" not in metrics

def test_get_metric_values(db_manager):
    """Test retrieving values for a specific metric."""
    ws = db_manager.manage_workspace("create", {"name": "WS_VAL", "path": "/ws_val"})
    db_manager.upsert_image({"path": "/v1.jpg", "filename": "v1.jpg", "file_size": 100, "workspace": ws}, {"val": 10.0})
    db_manager.upsert_image({"path": "/v2.jpg", "filename": "v2.jpg", "file_size": 200, "workspace": ws}, {"val": 20.0})
    
    # Internal metric
    sizes = db_manager.get_metric_values("file_size")
    assert sizes["/v1.jpg"] == 100.0
    assert sizes["/v2.jpg"] == 200.0
    
    # External metric
    vals = db_manager.get_metric_values("val")
    assert vals["/v1.jpg"] == 10.0
    assert vals["/v2.jpg"] == 20.0
