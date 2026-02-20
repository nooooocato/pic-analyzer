import pytest
from src.app.state import state

@pytest.fixture(autouse=True)
def reset_state():
    """Resets the global AppState before each test to ensure isolation."""
    state.initialized = False
    state.current_folder = None
    state.active_scanners = []
    state.current_viewer_index = -1
    state.db_manager = None
    state.plugin_manager = None
    yield
    # Optional: cleanup after test if needed
