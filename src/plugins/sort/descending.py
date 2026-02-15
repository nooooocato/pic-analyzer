from typing import List, Dict, Any
from src.plugins.sort.base import BaseSortPlugin

class DescendingSortPlugin(BaseSortPlugin):
    """
    Sorts items in descending order based on a numeric metric.
    """
    @property
    def name(self) -> str:
        return "Descending"

    @property
    def description(self) -> str:
        return "Sort items from highest to lowest value."

    def sort(self, items: List[Dict[str, Any]], metric_key: str) -> List[Dict[str, Any]]:
        """
        Sorts the provided items from highest to lowest value.
        
        Args:
            items (List[Dict[str, Any]]): List of image metadata dictionaries.
            metric_key (str): The key to sort by.
            
        Returns:
            List[Dict[str, Any]]: A new sorted list.
        """
        return sorted(items, key=lambda x: x.get(metric_key, 0), reverse=True)
