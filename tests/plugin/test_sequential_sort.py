import pytest

class MockSortPlugin:
    def __init__(self, reverse=False):
        self.reverse = reverse
        
    def sort(self, items, metric, params):
        # Stable sort in Python is guaranteed by sorted() and list.sort()
        return sorted(items, key=lambda x: x.get(metric, 0), reverse=self.reverse)

@pytest.fixture
def items():
    return [
        {"path": "a.jpg", "size": 100, "date": 2021},
        {"path": "b.jpg", "size": 200, "date": 2020},
        {"path": "c.jpg", "size": 100, "date": 2020},
        {"path": "d.jpg", "size": 200, "date": 2021}
    ]

def test_stable_sequential_sorting(items):
    """
    Test that applying sorts in sequence (S1, then S2) 
    results in S2 being the PRIMARY sort and S1 being the SECONDARY sort 
    (because each subsequent sort re-orders the list).
    
    Wait, usually 'Then By' means:
    1. Sort by Primary
    2. For items equal in Primary, sort by Secondary.
    
    In Python, to achieve this with stable sorts, you apply them in REVERSE order:
    items = sort_secondary(items)
    items = sort_primary(items)
    
    Our implementation in refresh_view currently does:
    for s in sorts:
        items = s.sort(items, ...)
        
    This means the LAST sort in the list becomes the PRIMARY sort.
    We should fix this in GalleryView if we want Top-to-Bottom UI priority.
    """
    s_size = MockSortPlugin() # Ascending
    s_date = MockSortPlugin() # Ascending
    
    # UI Order: Size (Primary), Date (Secondary)
    # Expected result: Sort by Size, then by Date for equal sizes.
    
    # If we apply Size then Date:
    # 1. Size: [a(100), c(100), b(200), d(200)]
    # 2. Date: [c(2020), b(2020), a(2021), d(2021)] -> Size order within dates is lost? No, it's stable.
    # Result: [c(100, 2020), b(200, 2020), a(100, 2021), d(200, 2021)]
    # This is NOT "Size then Date". This is "Date then Size".
    
    # Correct implementation for UI "Size then Date":
    # Apply in REVERSE: Date first, then Size.
    
    # Let's verify our current implementation's behavior (which we might need to fix)
    # Current:
    items = s_size.sort(items, "size", {})
    items = s_date.sort(items, "date", {})
    
    # Primary is Date
    assert items[0]['path'] == "c.jpg" # 2020
    assert items[1]['path'] == "b.jpg" # 2020
    
def test_sequential_priority_fix(items):
    """We want the FIRST sort in the list to be PRIMARY."""
    s_primary = MockSortPlugin() # Size
    s_secondary = MockSortPlugin() # Date
    
    sorts = [
        {"plugin": s_primary, "metric": "size"},
        {"plugin": s_secondary, "metric": "date"}
    ]
    
    # To have s_primary as PRIMARY, we must apply in reverse order
    for s in reversed(sorts):
        items = s['plugin'].sort(items, s['metric'], {})
        
    # Result should be:
    # 1. Size 100: [c(2020), a(2021)]
    # 2. Size 200: [b(2020), d(2021)]
    assert items[0]['path'] == "c.jpg"
    assert items[1]['path'] == "a.jpg"
    assert items[2]['path'] == "b.jpg"
    assert items[3]['path'] == "d.jpg"
