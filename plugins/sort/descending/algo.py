"""Algorithm for sorting items in descending order."""
from typing import List, Dict, Any

class DescendingSort:
    """Implementation of descending sort algorithm."""

    def sort(self, items: List[Dict[str, Any]], metric_key: str) -> List[Dict[str, Any]]:
        """Sorts the provided items based on the specified metric in descending order.

        Args:
            items: List of dictionaries, each representing an image with metadata.
            metric_key: The key in the item dictionary to sort by.

        Returns:
            A new list of sorted items.
        """
        return sorted(items, key=lambda x: x.get(metric_key, 0), reverse=True)
