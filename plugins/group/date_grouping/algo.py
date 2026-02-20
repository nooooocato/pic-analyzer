import os
import datetime
from typing import List, Dict, Any
from src.plugin.base import GroupPlugin, PluginSchema

class DateGroupingPlugin(GroupPlugin):
    """Refactored Date Grouping Plugin using the new logic-only interface."""

    @property
    def name(self) -> str:
        return "Date Grouping"

    @property
    def description(self) -> str:
        return "Groups images by their file modification date."

    @property
    def schema(self) -> PluginSchema:
        return {
            "parameters": [
                {
                    "name": "granularity",
                    "label": "Granularity",
                    "type": "choice",
                    "default": "month",
                    "options": ["year", "month", "day"]
                }
            ]
        }

    def group(self, items: List[Dict[str, Any]], metric_key: str, params: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Groups items by their modification date based on the specified granularity."""
        granularity = params.get("granularity", "month")
        groups = {}
        
        for item in items:
            path = item.get("path")
            if not path or not os.path.exists(path):
                continue
                
            mtime = os.path.getmtime(path)
            dt = datetime.datetime.fromtimestamp(mtime)
            
            if granularity == "year":
                key = dt.strftime('%Y')
            elif granularity == "day":
                key = dt.strftime('%Y-%m-%d')
            else: # month
                key = dt.strftime('%Y-%m')
            
            if key not in groups:
                groups[key] = []
            groups[key].append(item)
            
        return groups

    def run(self, image_path: str) -> dict:
        """Original run method for per-image analysis if needed."""
        # For grouping, we might still want to return the date as a metric
        if not os.path.exists(image_path):
            return {}
        mtime = os.path.getmtime(image_path)
        dt = datetime.datetime.fromtimestamp(mtime)
        return {"date": dt.strftime('%Y-%m-%d')}
