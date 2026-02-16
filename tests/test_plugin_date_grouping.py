import pytest
import os
import time
from group.date_grouping.ui import DateGroupingPlugin

def test_date_grouping_plugin_metadata():
    plugin = DateGroupingPlugin()
    assert plugin.name == "Date Grouping (Ext)"
    assert "date" in plugin.description.lower()

def test_date_grouping_run(tmp_path):
    test_file = tmp_path / "test.jpg"
    test_file.write_text("data")
    
    # Set a specific modification time (e.g., 2024-01-01)
    # 1704067200 is 2024-01-01 00:00:00 UTC
    os.utime(test_file, (1704067200, 1704067200))
    
    plugin = DateGroupingPlugin()
    result = plugin.run(str(test_file))

    assert "date" in result
    assert result["date"] == "2024-01"

    # Test day granularity
    result_day = plugin.run(str(test_file), granularity="day")
    assert result_day["date"] == "2024-01-01"

    # Test year granularity
    result_year = plugin.run(str(test_file), granularity="year")
    assert result_year["date"] == "2024"
