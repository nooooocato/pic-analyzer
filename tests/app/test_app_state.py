"""Tests for the global application state."""
import pytest
import os
from src.app import state

def test_app_state_initialization(tmp_path):
    """Verifies state initialization and resource setup."""
    app_state = state.AppState()
    assert app_state.initialized is False
    assert app_state.current_folder is None
    
    db_path = str(tmp_path / "test.db")
    plugins_dir = str(tmp_path / "plugins")
    os.makedirs(plugins_dir, exist_ok=True)
    
    app_state.initialize(plugins_dir=plugins_dir, default_db=db_path)
    
    assert app_state.initialized is True
    assert app_state.db_manager is not None
    assert app_state.plugin_manager is not None
    assert app_state.plugin_manager.plugins_dir == os.path.abspath(plugins_dir)

def test_app_state_set_folder():
    """Verifies that setting the current folder updates the state."""
    app_state = state.AppState()
    app_state.set_current_folder("/mock/path")
    assert app_state.current_folder == "/mock/path"
