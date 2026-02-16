import pytest
from sort.ascending.algo import AscendingSort
from sort.descending.algo import DescendingSort

def test_ascending_sort():
    plugin = AscendingSort()
    items = [
        {"path": "a", "val": 10},
        {"path": "b", "val": 5},
        {"path": "c", "val": 20}
    ]
    sorted_items = plugin.sort(items, "val")
    assert [item["val"] for item in sorted_items] == [5, 10, 20]

def test_descending_sort():
    plugin = DescendingSort()
    items = [
        {"path": "a", "val": 10},
        {"path": "b", "val": 5},
        {"path": "c", "val": 20}
    ]
    sorted_items = plugin.sort(items, "val")
    assert [item["val"] for item in sorted_items] == [20, 10, 5]
