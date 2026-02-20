import os
from typing import List, Dict, Any
from src.plugin.base import FilterPlugin, PluginSchema

class FileSizeFilter(FilterPlugin):
    """Filters items by their file size."""

    @property
    def name(self) -> str:
        return "File Size"

    @property
    def description(self) -> str:
        return "Filter images by file size (MB)."

    @property
    def schema(self) -> PluginSchema:
        return {
            "parameters": [
                {
                    "name": "min_mb",
                    "label": "Min Size (MB)",
                    "type": "float",
                    "default": 0.0,
                    "min": 0.0,
                    "max": 100.0
                },
                {
                    "name": "max_mb",
                    "label": "Max Size (MB)",
                    "type": "float",
                    "default": 10.0,
                    "min": 0.0,
                    "max": 500.0
                }
            ]
        }

    def filter(self, items: List[Dict[str, Any]], params: Dict[str, Any]) -> List[Dict[str, Any]]:
        min_bytes = params.get("min_mb", 0.0) * 1024 * 1024
        max_bytes = params.get("max_mb", 10.0) * 1024 * 1024
        
        filtered = []
        for item in items:
            path = item.get("path")
            if path and os.path.exists(path):
                size = os.path.getsize(path)
                if min_bytes <= size <= max_bytes:
                    filtered.append(item)
        return filtered

    def run(self, image_path: str) -> dict:
        return {}
