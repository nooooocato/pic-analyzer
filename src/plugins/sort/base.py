from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseSortPlugin(ABC):
    """
    Abstract base class for sorting plugins.
    """
    @property
    @abstractmethod
    def name(self) -> str:
        """The display name of the sorting algorithm."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """A brief description of how the algorithm sorts."""
        pass

    @abstractmethod
    def sort(self, items: List[Dict[str, Any]], metric_key: str) -> List[Dict[str, Any]]:
        """
        Sorts the provided items based on the specified metric.
        
        :param items: List of dictionaries, each representing an image with metadata.
                      Each dict should contain the metric_key.
        :param metric_key: The key in the item dictionary to sort by.
        :return: A new list of sorted items.
        """
        pass

    def get_stats(self, items: List[Dict[str, Any]], metric_key: str) -> Dict[str, Any]:
        """
        Optional: Returns statistical metadata about the sort (e.g., Mean, Sigma).
        """
        return {}
