import pytest
from src.plugin.filter_engine import FilterEngine

class MockFilterPlugin:
    def __init__(self, name, result_paths):
        self.name = name
        self.result_paths = result_paths
        
    def filter(self, items, params):
        return [it for it in items if it['path'] in self.result_paths]

@pytest.fixture
def items():
    return [
        {"path": "1.jpg", "tags": ["nature"]},
        {"path": "2.jpg", "tags": ["urban"]},
        {"path": "3.jpg", "tags": ["nature", "urban"]},
        {"path": "4.jpg", "tags": []}
    ]

def test_sequential_and_filtering(items):
    """F1 AND F2: Should return only items passing both."""
    f1 = MockFilterPlugin("F1", ["1.jpg", "3.jpg"])
    f2 = MockFilterPlugin("F2", ["2.jpg", "3.jpg"])
    
    rules = [
        {"type": "plugin", "plugin": f1, "params": {}},
        {"type": "connector", "op": "AND"},
        {"type": "plugin", "plugin": f2, "params": {}}
    ]
    
    engine = FilterEngine()
    result = engine.apply(items, rules)
    
    # Only 3.jpg passes both
    assert len(result) == 1
    assert result[0]['path'] == "3.jpg"

def test_sequential_or_filtering(items):
    """F1 OR F2: Should return items passing either."""
    f1 = MockFilterPlugin("F1", ["1.jpg"])
    f2 = MockFilterPlugin("F2", ["2.jpg"])
    
    rules = [
        {"type": "plugin", "plugin": f1, "params": {}},
        {"type": "connector", "op": "OR"},
        {"type": "plugin", "plugin": f2, "params": {}}
    ]
    
    engine = FilterEngine()
    result = engine.apply(items, rules)
    
    # 1.jpg and 2.jpg should pass
    assert len(result) == 2
    paths = [it['path'] for it in result]
    assert "1.jpg" in paths
    assert "2.jpg" in paths

def test_complex_chain_filtering(items):
    """(F1 OR F2) AND F3: 
    Note: Our UI is sequential, so it's ((F1 Op F2) Op F3).
    """
    f1 = MockFilterPlugin("F1", ["1.jpg"])
    f2 = MockFilterPlugin("F2", ["2.jpg"])
    f3 = MockFilterPlugin("F3", ["1.jpg", "3.jpg"])
    
    # ((F1 OR F2) AND F3)
    # (1.jpg, 2.jpg) AND (1.jpg, 3.jpg) -> 1.jpg
    rules = [
        {"type": "plugin", "plugin": f1, "params": {}},
        {"type": "connector", "op": "OR"},
        {"type": "plugin", "plugin": f2, "params": {}},
        {"type": "connector", "op": "AND"},
        {"type": "plugin", "plugin": f3, "params": {}}
    ]
    
    engine = FilterEngine()
    result = engine.apply(items, rules)
    
    assert len(result) == 1
    assert result[0]['path'] == "1.jpg"
