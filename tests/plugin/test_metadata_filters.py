import pytest
import os
from plugins.filter.file_type import FileTypeFilter
from plugins.filter.file_size import FileSizeFilter
from plugins.filter.date_range import DateRangeFilter

def test_file_type_filter():
    f = FileTypeFilter()
    items = [{"path": "test.jpg"}, {"path": "test.PNG"}]
    assert len(f.filter(items, {"extension": ".jpg"})) == 1
    assert len(f.filter(items, {"extension": ".png"})) == 1

def test_file_size_filter(tmp_path):
    # Create real files for size test
    f1 = tmp_path / "small.jpg"
    f1.write_bytes(b"0" * 100) # 100 bytes
    
    f2 = tmp_path / "large.jpg"
    f2.write_bytes(b"0" * (2 * 1024 * 1024)) # 2 MB
    
    f = FileSizeFilter()
    items = [{"path": str(f1)}, {"path": str(f2)}]
    
    # Filter for > 1MB
    res = f.filter(items, {"min_mb": 1.0, "max_mb": 10.0})
    assert len(res) == 1
    assert res[0]["path"] == str(f2)

def test_date_range_filter(tmp_path):
    f_old = tmp_path / "old.jpg"
    f_old.touch()
    # We can't easily change mtime without os.utime, but let's assume current year
    current_year = 2026 # As per session context
    
    f = DateRangeFilter()
    items = [{"path": str(f_old)}]
    
    res = f.filter(items, {"start_year": current_year, "end_year": current_year})
    assert len(res) == 1
