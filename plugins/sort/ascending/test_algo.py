"""Tests for the ascending sort algorithm."""
import pytest
from . import algo

def test_ascending_sort():
    """Verifies that items are correctly sorted from lowest to highest value."""
    plugin = algo.AscendingSort()
    items = [
        {"path": "a", "val": 10},
        {"path": "b", "val": 5},
        {"path": "c", "val": 20}
    ]
    sorted_items = plugin.sort(items, "val")
    assert [item["val"] for item in sorted_items] == [5, 10, 20]
