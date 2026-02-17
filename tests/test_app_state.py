import pytest
import os
from src.app.state import AppState

def test_app_state_initialization(tmp_path):
    state = AppState()
    assert state.initialized is False
    assert state.current_folder is None
    
    db_path = str(tmp_path / "test.db")
    plugins_dir = str(tmp_path / "plugins")
    os.makedirs(plugins_dir, exist_ok=True)
    
    state.initialize(plugins_dir=plugins_dir, default_db=db_path)
    
    assert state.initialized is True
    assert state.db_manager is not None
    assert state.plugin_manager is not None
    assert state.plugin_manager.plugins_dir == os.path.abspath(plugins_dir)

def test_app_state_set_folder():
    state = AppState()
    state.set_current_folder("/mock/path")
    assert state.current_folder == "/mock/path"
