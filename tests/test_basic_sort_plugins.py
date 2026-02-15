import pytest
from src.plugins.sort.ascending import AscendingSortPlugin
from src.plugins.sort.descending import DescendingSortPlugin

def test_ascending_sort():
    plugin = AscendingSortPlugin()
    items = [
        {"path": "a", "val": 10},
        {"path": "b", "val": 5},
        {"path": "c", "val": 20}
    ]
    sorted_items = plugin.sort(items, "val")
    assert [item["val"] for item in sorted_items] == [5, 10, 20]

def test_descending_sort():
    plugin = DescendingSortPlugin()
    items = [
        {"path": "a", "val": 10},
        {"path": "b", "val": 5},
        {"path": "c", "val": 20}
    ]
    sorted_items = plugin.sort(items, "val")
    assert [item["val"] for item in sorted_items] == [20, 10, 5]
