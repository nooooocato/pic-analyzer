from typing import List, Dict, Any
from .base import BaseSortPlugin

class DescendingSortPlugin(BaseSortPlugin):
    @property
    def name(self) -> str:
        return "Descending"

    @property
    def description(self) -> str:
        return "Sort items from highest to lowest value."

    def sort(self, items: List[Dict[str, Any]], metric_key: str) -> List[Dict[str, Any]]:
        return sorted(items, key=lambda x: x.get(metric_key, 0), reverse=True)
