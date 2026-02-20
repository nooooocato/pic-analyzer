import pytest
from src.plugin.base import FilterPlugin

class MockFilter(FilterPlugin):
    @property
    def name(self): return "Mock Filter"
    @property
    def description(self): return "desc"
    @property
    def schema(self):
        return {"parameters": [{"name": "ext", "type": "str", "default": ".jpg", "label": "Ext"}]}
    
    def run(self, path): return {}
    
    def filter(self, items, params):
        ext = params.get("ext", ".jpg")
        return [item for item in items if item.get("path", "").endswith(ext)]

def test_filter_plugin_logic():
    """Test that a FilterPlugin correctly filters items based on parameters."""
    f = MockFilter()
    items = [
        {"path": "a.jpg"},
        {"path": "b.png"},
        {"path": "c.jpg"}
    ]
    
    # Test with default (.jpg)
    res = f.filter(items, {"ext": ".jpg"})
    assert len(res) == 2
    assert all(i["path"].endswith(".jpg") for i in res)
    
    # Test with .png
    res = f.filter(items, {"ext": ".png"})
    assert len(res) == 1
    assert res[0]["path"] == "b.png"
