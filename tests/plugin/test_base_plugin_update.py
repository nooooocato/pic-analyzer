import pytest
from src.plugin.base import BasePlugin

def test_base_plugin_has_initialize_ui():
    class ConcretePlugin(BasePlugin):
        @property
        def name(self): return "Test"
        @property
        def description(self): return "Test"
        def run(self, image_path): return {}
        # initialize_ui is not implemented here to test if it's required
    
    with pytest.raises(TypeError) as excinfo:
        ConcretePlugin()
    assert "initialize_ui" in str(excinfo.value)
