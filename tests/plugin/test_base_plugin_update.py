import pytest
from src.plugin.base import BasePlugin

def test_base_plugin_abstract_methods():
    """Verify that BasePlugin cannot be instantiated without implementing abstract methods."""
    with pytest.raises(TypeError):
        BasePlugin()

def test_concrete_plugin_instantiation():
    """Verify that a subclass implementing all abstract methods can be instantiated."""
    class MyPlugin(BasePlugin):
        @property
        def name(self): return "MyPlugin"
        @property
        def description(self): return "Desc"
        def run(self, path): return {}
        
    p = MyPlugin()
    assert p.name == "MyPlugin"
    assert p.category == "general"
