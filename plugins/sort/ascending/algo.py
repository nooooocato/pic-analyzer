from typing import List, Dict, Any
from src.plugin.base import SortPlugin

class AscendingPlugin(SortPlugin):
    """Refactored Ascending Sort Plugin using the new logic-only interface."""

    @property
    def name(self) -> str:
        return "Ascending"

    @property
    def description(self) -> str:
        return "Sort items from lowest to highest value."

    def sort(self, items: List[Dict[str, Any]], metric_key: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Sorts the provided items based on the specified metric in ascending order."""
        return sorted(items, key=lambda x: x.get(metric_key, 0))

    def run(self, image_path: str) -> dict:
        return {}
