from typing import List, Dict, Any
from .base import BaseSortPlugin

class AscendingSortPlugin(BaseSortPlugin):
    @property
    def name(self) -> str:
        return "Ascending"

    @property
    def description(self) -> str:
        return "Sort items from lowest to highest value."

    def sort(self, items: List[Dict[str, Any]], metric_key: str) -> List[Dict[str, Any]]:
        return sorted(items, key=lambda x: x.get(metric_key, 0))
