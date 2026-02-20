import os
import datetime
from typing import List, Dict, Any
from src.plugin.base import FilterPlugin, PluginSchema

class DateRangeFilter(FilterPlugin):
    """Filters items by their modification date range."""

    @property
    def name(self) -> str:
        return "Date Range"

    @property
    def description(self) -> str:
        return "Filter images by their last modified date range."

    @property
    def schema(self) -> PluginSchema:
        return {
            "parameters": [
                {
                    "name": "start_year",
                    "label": "Start Year",
                    "type": "int",
                    "default": 2020,
                    "min": 1900,
                    "max": 2100
                },
                {
                    "name": "end_year",
                    "label": "End Year",
                    "type": "int",
                    "default": 2026,
                    "min": 1900,
                    "max": 2100
                }
            ]
        }

    def filter(self, items: List[Dict[str, Any]], params: Dict[str, Any]) -> List[Dict[str, Any]]:
        start_year = params.get("start_year", 2020)
        end_year = params.get("end_year", 2026)
        
        filtered = []
        for item in items:
            path = item.get("path")
            if path and os.path.exists(path):
                mtime = os.path.getmtime(path)
                dt = datetime.datetime.fromtimestamp(mtime)
                if start_year <= dt.year <= end_year:
                    filtered.append(item)
        return filtered

    def run(self, image_path: str) -> dict:
        return {}
