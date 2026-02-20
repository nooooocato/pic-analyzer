"""Base class for sorting plugins."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseSortPlugin(ABC):
    """Abstract base class for all sorting algorithms in the system."""

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
        """Sorts the provided items based on the specified metric.
        
        Args:
            items: List of dictionaries, each representing an image with metadata.
            metric_key: The key in the item dictionary to sort by.

        Returns:
            A new list of sorted items.
        """
        pass

    def get_stats(self, items: List[Dict[str, Any]], metric_key: str) -> Dict[str, Any]:
        """Calculates optional statistical metadata about the sort.

        Args:
            items: List of dictionaries to analyze.
            metric_key: The key in the dictionary to use for stats.

        Returns:
            A dictionary containing statistical metrics (e.g., Mean, Sigma).
        """
        return {}
