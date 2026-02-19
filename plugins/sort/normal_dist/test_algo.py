import pytest
import numpy as np
from .algo import NormalDistributionSort

def test_normal_distribution_sort():
    plugin = NormalDistributionSort()
    # Data centered around 10
    # Values: 10 (diff 0), 9 (diff 1), 11 (diff 1), 5 (diff 5), 15 (diff 5)
    items = [
        {"path": "a", "val": 10},
        {"path": "b", "val": 5},
        {"path": "c", "val": 15},
        {"path": "d", "val": 9},
        {"path": "e", "val": 11}
    ]
    # Mean should be (10+5+15+9+11)/5 = 50/5 = 10
    sorted_items = plugin.sort(items, "val")
    
    # Check that 10 is first
    assert sorted_items[0]["val"] == 10
    # Check that 5 and 15 are last (tied for furthest)
    assert set([sorted_items[-1]["val"], sorted_items[-2]["val"]]) == {5, 15}
    
def test_normal_distribution_stats():
    plugin = NormalDistributionSort()
    items = [
        {"path": "a", "val": 10},
        {"path": "b", "val": 20}
    ]
    stats = plugin.get_stats(items, "val")
    assert stats["mean"] == 15.0
    assert stats["sigma"] == 5.0 # std of [10, 20] is 5.0
