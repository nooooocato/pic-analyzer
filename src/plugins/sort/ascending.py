from typing import List, Dict, Any
from src.plugins.sort.base import BaseSortPlugin

class AscendingSortPlugin(BaseSortPlugin):
    """
    Sorts items in ascending order based on a numeric metric.
    """
    @property
    def name(self) -> str:
        return "Ascending"

    @property
    def description(self) -> str:
        return "Sort items from lowest to highest value."

    def sort(self, items: List[Dict[str, Any]], metric_key: str) -> List[Dict[str, Any]]:
        """
        Sorts the provided items from lowest to highest value.
        
        Args:
            items (List[Dict[str, Any]]): List of image metadata dictionaries.
            metric_key (str): The key to sort by.
            
        Returns:
            List[Dict[str, Any]]: A new sorted list.
        """
        return sorted(items, key=lambda x: x.get(metric_key, 0))
