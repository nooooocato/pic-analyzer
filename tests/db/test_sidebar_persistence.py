import pytest
from src.db.manager import DBManager
from src.db.models import Workspace, SidebarState
import os

@pytest.fixture
def db_manager(tmp_path):
    db_file = tmp_path / "test_persistence.db"
    manager = DBManager(str(db_file))
    return manager

def test_sidebar_state_persistence(db_manager):
    """Test saving and loading sidebar configuration from DB."""
    # 1. Setup workspace
    ws_name = "test_ws"
    db_manager.manage_workspace("create", {"name": ws_name, "path": "/mock/path"})
    
    config = {
        "group": {"plugin_name": "Date Grouping", "params": {"granularity": "day"}},
        "filters": [
            {"type": "plugin", "plugin_name": "File Type", "enabled": True, "params": {}},
            {"type": "connector", "op": "OR"}
        ],
        "sorts": []
    }
    
    # 2. Save
    success = db_manager.save_sidebar_state(ws_name, config)
    assert success is True
    
    # 3. Load
    loaded_config = db_manager.load_sidebar_state(ws_name)
    assert loaded_config["group"]["plugin_name"] == "Date Grouping"
    assert len(loaded_config["filters"]) == 2
    assert loaded_config["filters"][1]["op"] == "OR"

def test_load_non_existent_state(db_manager):
    """Loading state for a non-existent workspace should return empty dict."""
    config = db_manager.load_sidebar_state("ghost_ws")
    assert config == {}
