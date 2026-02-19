import pytest
from PySide6.QtWidgets import QApplication
from src.ui.overlays.data_inspector.logic import DataInspector
from src.app.communicator import Communicator
from src.app.state import state

@pytest.fixture
def data_inspector(qtbot):
    # Ensure state is initialized for db access if needed, 
    # though we might mock it.
    widget = DataInspector()
    qtbot.addWidget(widget)
    return widget

def test_data_inspector_updates_on_signal(data_inspector, qtbot, monkeypatch):
    """Test that DataInspector updates its view when an image is selected via Communicator."""
    mock_metadata = {
        "Filename": "test.jpg",
        "Size": "100 KB",
        "Modified": "2026-01-01"
    }
    
    # Mock DBManager to return specific metadata
    class MockDB:
        def get_image_metadata(self, path):
            return mock_metadata
            
    monkeypatch.setattr(state, "db_manager", MockDB())
    
    # Mock os.path.exists to return True
    monkeypatch.setattr("os.path.exists", lambda x: True)
    
    # Emit signal (Assuming we'll add an 'image_selected' signal to Communicator)
    comm = Communicator()
    if not hasattr(comm, "image_selected"):
         pytest.skip("Communicator does not have image_selected signal yet")
         
    comm.image_selected.emit("/path/test.jpg")
    
    # Verify tree model has the data
    model = data_inspector.layout_engine.tree_view.model()
    assert model.rowCount() == 4
    assert model.item(0, 0).text() == "Filename"
    assert model.item(0, 1).text() == "test.jpg"
