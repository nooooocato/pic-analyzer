"""Tests for the descending sort algorithm."""
import pytest
from . import algo

def test_descending_sort():
    """Verifies that items are correctly sorted from highest to lowest value."""
    plugin = algo.DescendingSort()
    items = [
        {"path": "a", "val": 10},
        {"path": "b", "val": 5},
        {"path": "c", "val": 20}
    ]
    sorted_items = plugin.sort(items, "val")
    assert [item["val"] for item in sorted_items] == [20, 10, 5]
